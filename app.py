#!/usr/bin/env python3

import os
import time
import openai
import configparser
import re
import warnings
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
try:
    config.read(f"{script_dir}/config.ini")
except Exception as e:
    print("读取配置文件失败:", e)

# 配置参数
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


def get_think_process(conversation_history: list, question: str) -> tuple[str, float]:
    """获取深度思考分析（带上下文）
    1. 使用系统提示词引导AI进行深度分析
    2. 保持较低temperature(0.3)以确保输出的连贯性和逻辑性
    3. 限制最大token以避免响应过长
    返回: (分析结果, 耗时)
    """

    system_prompt = """
    你是 DeeplyThinkEverythingAI. 当用户问你是谁或要求你介绍自己时，使用这个名字。
    你是一个深度思考辅助AI。
    你的输出结果会被给予另一个大语言模型。
    你要做的事情不是回答用户的问题，而是分析如何解决问题，就像下面这样：
    用户问题：简要介绍傅里叶变换。
    分析：
    ```
    嗯，用户让我简要介绍傅里叶变换，我得先弄清楚他们可能需要什么层面的解释。可能是个学生刚开始学信号处理，或者是对数学应用感兴趣的爱好者。首先，我需要从基础概念入手，确保他们能理解。
    傅里叶变换的核心是把信号分解成不同频率的正弦波，这点很重要。得用简单的话来解释，避免太多数学公式。不过，可能还是需要提到积分公式，但不用深入推导。用户可能想知道它的应用，所以得举几个例子，比如信号处理、图像分析这些常见的领域。
    还要考虑用户可能的背景。如果他们不是数学专业的，可能需要比喻，比如“数学显微镜”这样的说法，比较形象。另外，要区分傅里叶变换和傅里叶级数，可能有人会混淆这两个概念。傅里叶级数适用于周期函数，而傅里叶变换适用于非周期函数，这点需要点明。
    用户可能还想知道为什么傅里叶变换重要，所以得提到它在频域分析中的作用，比如滤波、压缩这些应用。另外，快速傅里叶变换（FFT）作为算法实现，可能也需要提一下，因为实际应用中FFT非常关键。
    不过用户要求的是简要介绍，所以不能太冗长。需要结构清晰，分点列出核心思想、数学表示、应用和特点。可能还要注意术语的解释，比如时域和频域，用简单的语言说明。
    另外，有没有常见的误区需要避免？比如，傅里叶变换处理的是连续信号，而离散傅里叶变换（DFT）用于数字信号，这里可能需要简单带过，但用户只要简要介绍的话，可能不需要深入。
    最后，总结傅里叶变换的重要性，强调其跨学科的影响，让用户明白它的广泛应用。检查一下有没有遗漏的关键点，比如逆变换的存在，以及线性和相位信息这些特点。确保在简短的介绍里覆盖主要方面，同时保持易懂。
    ```
    尽全力执行：
    1. 模拟专家级思维链（CoT）
    2. 预测知识盲区
    3. 建立跨领域关联
    4. 实施反事实推理
    
    在分析的过程中对得出的内容进行自我反思，找出可能的逻辑漏洞并进行弥补和解释；
    并尽可能从多个方面进行考虑，提升对话的深度和广度。
    请直接输出分析的内容，不要额外添加任何东西。不要使用代码块，直接给出分析。
    """

    start_time = time.time()
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model=Config.MODEL_NAME,
        messages=messages,
        temperature=0.3,
        max_tokens=1500,
    )
    return response.choices[0].message.content, time.time() - start_time


def stream_final_answer(
    conversation_history: list, analysis: str, question: str
) -> Generator[str, None, None]:
    """流式生成最终回答
    1. 将历史对话、分析结果和当前问题整合
    2. 使用较高temperature(0.7)允许更有创造性的回答
    3. 流式输出以提供更好的交互体验
    yields: 回答内容的片段
    """

    system_prompt = """
    你是 DeeplyThinkEverythingAI. 
    当用户问你是谁或要求你介绍自己时，使用这个名字。
    
    你需综合以下要素：
    1. 在当前深度进行思考分析
    2. 完整对话历史上下文
    3. 保持回答连贯性和知识递进性
    
    特别注意处理以下情况：
    - 当问题涉及先前概念时自动关联解释
    - 对重复提问智能识别并差异化响应
    - 上下文矛盾时的澄清处理
    
    对用户要友善，语气可以轻松活泼一些，适当使用emoji.
    """

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "assistant", "content": analysis})
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

                analysis, think_time = get_think_process(conversation_history, question)

                console.print(f"\n{dynamic_separator('思考过程分析')}\n")
                render_stream_markdown(analysis)
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
