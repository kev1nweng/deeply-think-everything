import time
import openai
from typing import Generator
from rich.markdown import Markdown
from rich.console import Console
from rich.syntax import Syntax
from wcwidth import wcswidth  # 用于准确计算字符显示宽度
import configparser


# 读取配置文件
config = configparser.ConfigParser()
try:
    config.read("config.ini")
except Exception as e:
    print("读取配置文件失败:", e)


# 配置参数
class Config:
    API_KEY = config.get("dte", "api_key")
    API_BASE = config.get("dte", "api_url")
    MODEL_NAME = config.get("dte", "model_name")


# 初始化OpenAI客户端和Rich控制台
client = openai.OpenAI(api_key=Config.API_KEY, base_url=Config.API_BASE)
console = Console(record=True)


def dynamic_separator(title: str) -> str:
    """生成动态居中分隔线"""
    term_width = console.width
    title = f" {title} "  # 为标题添加两侧空格
    title_width = wcswidth(title)

    # 计算可用空间
    available_width = term_width - title_width
    if available_width < 2:
        return "=" * term_width

    # 计算两侧等号数量
    sep_len = available_width // 2
    return f"[dim]{'='*sep_len}[/][bold]{title}[/][dim]{'='*(available_width - sep_len)}[/]"


def render_stream_markdown(content: str):
    """流式Markdown渲染处理器"""
    in_code_block = False
    code_buffer = []
    current_lang = "text"

    lines = content.split("\n")
    for line in lines:
        # 处理代码块标记
        if line.strip().startswith("```"):
            if in_code_block:
                # 渲染代码块
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
                # 解析代码语言
                lang = line.strip()[3:].strip()
                current_lang = lang if lang else "text"
                in_code_block = True
            continue

        if in_code_block:
            code_buffer.append(line)
        else:
            # 渲染普通Markdown内容
            console.print(Markdown(line))

    # 处理未闭合的代码块
    if in_code_block and code_buffer:
        console.print(
            Syntax(
                "\n".join(code_buffer),
                current_lang,
                theme="monokai",
                line_numbers=False,
            )
        )


def get_think_process(conversation_history: list, question: str) -> tuple[str, float]:
    """获取深度思考分析（带上下文）"""
    system_prompt = """你是一个深度思考辅助AI，分析时需考虑对话历史：
    - 识别当前问题与历史记录的关联性
    - 分析上下文演进中的知识积累
    - 注意用户可能存在的追问或概念延伸
    保持原有分析框架，但需特别标注与历史对话的关联点。输出保持markdown代码块格式。
    以下是一个例子：用户问题：简要介绍傅里叶变换。
    分析：嗯，用户让我简要介绍傅里叶变换，我得先弄清楚他们可能需要什么层面的解释。可能是个学生刚开始学信号处理，或者是对数学应用感兴趣的爱好者。首先，我需要从基础概念入手，确保他们能理解。
    傅里叶变换的核心是把信号分解成不同频率的正弦波，这点很重要。得用简单的话来解释，避免太多数学公式。不过，可能还是需要提到积分公式，但不用深入推导。用户可能想知道它的应用，所以得举几个例子，比如信号处理、图像分析这些常见的领域。
    还要考虑用户可能的背景。如果他们不是数学专业的，可能需要比喻，比如“数学显微镜”这样的说法，比较形象。另外，要区分傅里叶变换和傅里叶级数，可能有人会混淆这两个概念。傅里叶级数适用于周期函数，而傅里叶变换适用于非周期函数，这点需要点明。
    用户可能还想知道为什么傅里叶变换重要，所以得提到它在频域分析中的作用，比如滤波、压缩这些应用。另外，快速傅里叶变换（FFT）作为算法实现，可能也需要提一下，因为实际应用中FFT非常关键。
    不过用户要求的是简要介绍，所以不能太冗长。需要结构清晰，分点列出核心思想、数学表示、应用和特点。可能还要注意术语的解释，比如时域和频域，用简单的语言说明。
    另外，有没有常见的误区需要避免？比如，傅里叶变换处理的是连续信号，而离散傅里叶变换（DFT）用于数字信号，这里可能需要简单带过，但用户只要简要介绍的话，可能不需要深入。
    最后，总结傅里叶变换的重要性，强调其跨学科的影响，让用户明白它的广泛应用。检查一下有没有遗漏的关键点，比如逆变换的存在，以及线性和相位信息这些特点。确保在简短的介绍里覆盖主要方面，同时保持易懂。
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
    """流式生成最终回答（带上下文）"""
    system_prompt = """你是回答生成AI，需综合以下要素：
    1. 当前深度思考分析
    2. 完整对话历史上下文
    3. 保持回答连贯性和知识递进性
    特别注意处理以下情况：
    - 当问题涉及先前概念时自动关联解释
    - 对重复提问智能识别并差异化响应
    - 上下文矛盾时的澄清处理"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "assistant", "content": analysis})
    messages.append(
        {"role": "user", "content": f"基于分析和历史对话，请回答：{question}"}
    )

    response = client.chat.completions.create(
        model=Config.MODEL_NAME,
        messages=messages,
        stream=True,
        temperature=0.7,
        max_tokens=2000,
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
                question = input("\n>> ").strip()
                if not question:
                    continue

                # 上下文重置指令
                if question.lower() == "@new":
                    conversation_history.clear()
                    console.clear()
                    console.print("\n🌟 [cyan]上下文已重置，开启新对话[/]")
                    continue

                console.print("\n🤔 [yellow]正在深度思考...[/]")

                # 阶段1：带上下文的思考分析
                analysis, think_time = get_think_process(conversation_history, question)

                # 显示思考过程
                console.print(f"\n{dynamic_separator('思考过程分析')}\n")
                console.print(Markdown(analysis))
                console.print(f"\n🔍 [dim]深度思考耗时: {format_time(think_time)}[/]")

                # 阶段2：带上下文的流式回答
                console.print(f"\n{dynamic_separator('最终答案生成')}\n")
                answer_buffer = []
                start_time = time.time()
                full_content = ""

                try:
                    # 流式接收但统一渲染
                    for chunk in stream_final_answer(
                        conversation_history, analysis, question
                    ):
                        full_content += chunk
                        answer_buffer.append(chunk)

                    # 统一渲染Markdown
                    render_stream_markdown(full_content)

                except Exception as e:
                    # 尝试渲染已接收内容
                    if full_content:
                        render_stream_markdown(full_content)
                    console.print(f"\n⚠️ [red]生成中断: {str(e)}[/]")
                finally:
                    # 更新对话上下文
                    if full_content:
                        conversation_history.extend(
                            [
                                {"role": "user", "content": question},
                                {"role": "assistant", "content": full_content},
                            ]
                        )

                    # 性能统计
                    total_time = time.time() - start_time
                    console.print("\n" + "=" * console.width)
                    console.print(
                        f"✅ [green]生成完成[/] | [dim]总耗时: {format_time(total_time)}[/] | "
                        f"[dim]上下文长度: {len(conversation_history)//2}轮[/]"
                    )

            except KeyboardInterrupt:
                console.print("\n🛑 [red]操作已取消，再次按下 Ctrl+C 退出程序[/]")
                time.sleep(1)  # 等待第二次中断

    except KeyboardInterrupt:
        console.print("\n👋 再见！")
        exit()
    except Exception as e:
        console.print(f"\n❌ [red]处理错误: {str(e)}[/]")
        conversation_history.clear()
