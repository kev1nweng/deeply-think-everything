#!/usr/bin/env python3

import os
import time
import openai
import configparser
import re
import warnings
import json
from typing import Generator
from rich.markdown import Markdown
from rich.console import Console
from rich.syntax import Syntax
from wcwidth import wcswidth
from pylatexenc.latex2text import LatexNodes2Text
from prompt_toolkit import prompt

warnings.filterwarnings("ignore", category=SyntaxWarning)

# 读取配置文件
script_dir = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()

# 读取各种配置
try:
    config.read(f"{script_dir}/config.ini")
except Exception as e:
    print("读取配置文件失败:", e)

try:
    with open(f"{script_dir}/prompts.json", "r") as f:
        prompts = json.load(f)
        if (not prompts["think_prompt"]) or not (prompts["answer_prompt"]):
            raise Exception("提示词文件格式错误")
except Exception as e:
    print("读取提示词文件失败:", e)
    exit(1)

try:
    class Config:
        API_KEY = config.get("dte", "api_key")
        API_BASE = config.get("dte", "api_url")
        MODEL_NAME = config.get("dte", "model_name")
except Exception as e:
    print("读取配置参数失败:", e)
    exit(1)

# 初始化OpenAI客户端和Rich控制台
client = openai.OpenAI(api_key=Config.API_KEY, base_url=Config.API_BASE)
console = Console(record=True)


def dynamic_separator(title: str) -> str:
    """生成动态居中分隔线
    根据终端宽度自动调整分隔线长度，确保标题居中显示
    wcswidth用于准确计算包含中文等宽字符的显示宽度
    """

    term_width = console.width
    title = f" {title} "
    title_width = wcswidth(title)
    available_width = term_width - title_width
    if available_width < 2:
        return "=" * term_width
    sep_len = available_width // 2
    return f"[dim]{'='*sep_len}[/][bold]{title}[/][dim]{'='*(available_width - sep_len)}[/]"


def _handle_block_latex(match: re.Match) -> str:
    """处理块级LaTeX公式
    将LaTeX数学公式转换为纯文本格式，并添加美观的边框
    """

    formula = match.group(1) or match.group(2)
    converted = LatexNodes2Text().latex_to_text(formula).strip()
    return f"\n┌ {' LaTeX ':-^8} ┐\n{converted}\n└ {'-'*8} ┘\n"


def _process_latex_in_text(text: str) -> str:
    r"""处理非代码块中的LaTeX公式
    1. 处理行内公式: $formula$ -> ┆formula┆
    2. 处理块级公式: $$formula$$ 或 \[formula\] -> 带框显示
    3. 避免处理已转义的LaTeX标记
    """

    # 处理行内公式（排除转义$的情况）
    text = re.sub(
        r"(?<!\\)\$(.*?)(?<!\\)\$",
        lambda m: f"[dim]┆[/] {LatexNodes2Text().latex_to_text(m.group(1)).strip()} [dim]┆[/]",
        text,
        flags=re.DOTALL,
    )
    # 处理块级公式（排除转义情况）
    return re.sub(
        r"(?<!\\)\$\$([\s\S]*?)(?<!\\)\$\$|(?<!\\)\\\[([\s\S]*?)(?<!\\)\\\]",
        _handle_block_latex,
        text,
        flags=re.DOTALL,
    )


def preprocess_latex(content: str) -> str:
    """改进后的LaTeX预处理
    使用正则表达式分割内容，确保代码块中的LaTeX符号不被处理
    奇数索引的部分是代码块，直接保留
    偶数索引的部分是普通文本，需要处理LaTeX
    """

    parts = re.split(r"(```[\s\S]*?```)", content)
    processed = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            processed.append(part)
            continue
        processed.append(_process_latex_in_text(part))
    return "".join(processed)


def render_stream_markdown(content: str):
    """改进后的流式Markdown渲染处理器
    1. 预处理所有LaTeX公式
    2. 特殊处理代码块，支持语法高亮
    3. 普通文本使用Markdown渲染
    """

    content = preprocess_latex(content)
    in_code_block = False
    code_buffer = []
    current_lang = "text"

    lines = content.split("\n")
    for line in lines:
        if line.strip().startswith("```"):
            if in_code_block:
                console.print(
                    Syntax(
                        "\n".join(code_buffer),
                        current_lang,
                        theme="monokai",
                        line_numbers=False,
                    )
                )
                code_buffer = []
                in_code_block = False
            else:
                lang = line.strip()[3:].strip()
                current_lang = lang if lang else "text"
                in_code_block = True
            continue
        if in_code_block:
            code_buffer.append(line)
        else:
            console.print(Markdown(line))


def stream_think_process(
    conversation_history: list, question: str
) -> Generator[str, None, None]:
    """获取深度思考分析（带上下文）
    1. 使用系统提示词引导AI进行深度分析
    2. 保持较低temperature(0.3)以确保输出的连贯性和逻辑性
    3. 限制最大token以避免响应过长
    返回: (分析结果, 耗时)
    """

    system_prompt = prompts["think_prompt"]

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=Config.MODEL_NAME,
        messages=messages,
        temperature=0.3,
        max_tokens=1500,
        stream=True,
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def stream_final_answer(
    conversation_history: list, analysis: str, question: str
) -> Generator[str, None, None]:
    """流式生成最终回答
    1. 将历史对话、分析结果和当前问题整合
    2. 使用较高temperature(0.7)允许更有创造性的回答
    3. 流式输出以提供更好的交互体验
    yields: 回答内容的片段
    """

    system_prompt = prompts["answer_prompt"]

    messages = [{"role": "system", "content": system_prompt + "\n" + analysis}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": f"基于分析内容，请回答：{question}"})

    response = client.chat.completions.create(
        model=Config.MODEL_NAME,
        messages=messages,
        stream=True,
        temperature=0.7,
        max_tokens=4096,
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def format_time(seconds: float) -> str:
    """将秒数格式化为易读时间"""
    return f"{seconds:.2f}s" if seconds >= 1 else f"{seconds*1000:.0f}ms"


if __name__ == "__main__":
    console.print(
        "[bold magenta]👋 欢迎来到 DeeplyThinkEverything！\n输入 @new 可以清除上下文并开启新对话。[/]"
    )
    conversation_history = []

    try:
        while True:
            try:
                question = prompt("\n>> ", multiline=False).strip()
                if not question:
                    continue

                if question.lower() == "@new":
                    conversation_history.clear()
                    console.clear()
                    console.print("\n🌟 [cyan]上下文已重置，开启新对话[/]")
                    continue

                console.print("\n🤔 [yellow]正在深度思考...[/]")
                console.print(f"\n{dynamic_separator('思考过程分析')}\n")

                # 流式处理思考过程
                start_time = time.time()
                analysis_content = []
                buffer = ""

                for chunk in stream_think_process(conversation_history, question):
                    buffer += chunk
                    processed_part = _process_latex_in_text(buffer)
                    console.print(processed_part, end="")
                    analysis_content.append(processed_part)
                    buffer = ""

                # 处理剩余内容
                if buffer:
                    processed_part = _process_latex_in_text(buffer)
                    console.print(processed_part, end="")
                    analysis_content.append(processed_part)

                think_time = time.time() - start_time
                analysis = "".join(analysis_content)
                console.print(f"\n🔍 [dim]深度思考耗时: {format_time(think_time)}[/]")

                console.print(f"\n{dynamic_separator('最终答案生成')}\n")
                answer_buffer = []
                start_time = time.time()
                full_content = ""

                try:
                    for chunk in stream_final_answer(
                        conversation_history, analysis, question
                    ):
                        full_content += chunk
                        answer_buffer.append(chunk)

                    render_stream_markdown(full_content)

                except Exception as e:
                    if full_content:
                        render_stream_markdown(full_content)
                    console.print(f"\n⚠️ [red]生成中断: {str(e)}[/]")
                finally:
                    if full_content:
                        conversation_history.extend(
                            [
                                {"role": "user", "content": question},
                                {"role": "assistant", "content": full_content},
                            ]
                        )

                    total_time = time.time() - start_time
                    console.print("\n" + "=" * console.width)
                    console.print(
                        f"✅ [green]生成完成[/] | [dim]耗时: {format_time(total_time)}[/] | "
                        f"[dim]上下文长度: {len(conversation_history)//2}轮[/]"
                    )

            except KeyboardInterrupt:
                console.print(
                    "\n🛑 [red]操作已取消，在 1s 内再次按下 Ctrl+C 退出程序[/]"
                )
                time.sleep(1)

    except KeyboardInterrupt:
        console.print("\n👋 再见！")
        exit()
    except Exception as e:
        console.print(f"\n❌ [red]处理错误: {str(e)}[/]")
        conversation_history.clear()
