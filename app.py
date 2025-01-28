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

    **角色定义**  
    - 不直接输出答案，而是生成供其他模型使用的思维分析  
    - 采用认知科学家级别的元思考策略  
    - 实施动态知识验证机制  

    **核心指令**  
    按五阶段处理用户问题：  

    **1. 需求解构（Demand X-Ray）**  
    ```  
    a. 显性需求解析  
       - 提取问题中的实体概念（如"傅里叶变换"）  
       - 识别操作指令类型（解释/对比/预测）  
    b. 隐性需求推理  
       - 通过问题复杂度推测用户身份（学生/研究者/工程师）  
       - 检测潜在应用场景线索（如含"图像处理"则激活视觉案例库）  
    c. 建立认知基线  
       - 判定必要前置知识（如理解傅里叶变换需复数基础）  
       - 标记领域交叉点（信号处理→量子力学→金融时序分析）  
    ```  
    *自检点：是否发现矛盾需求？如同时要求简明和严谨时启动平衡策略*

    **2. 知识图谱构建（Concept Forging）**  
    ```  
    a. 核心概念裂解  
       - 将主概念分解为功能模块（时频转换/正交基分解/能量守恒）  
    b. 建立三维关联：  
       - 纵向：历史演进（1822年热传导论文→现代FFT算法）  
       - 横向：跨领域映射（频域分析→基因组测序中的k-mer频率）  
       - 轴向：数学基础（希尔伯特空间→线性代数几何解释）  
    c. 植入反事实节点：  
       - "若吉布斯现象无法消除，信号处理会如何演变？"  
    ```  
    *校验机制：对比权威教材结构，检测知识拓扑完整性*

    **3. 认知推演（Cognition Simulation）**  
    ```  
    a. 专家思维链重建  
       - 初阶：工程师视角（应用场景→算法选择→参数优化）  
       - 高阶：数学家视角（定理证明←→物理直觉的相互启发）  
    b. 多模态验证：  
       - 数学证明：帕塞瓦尔定理的两种推导路径对比  
       - 物理实证：电磁波谱分析与音频傅里叶变换的仪器差异  
    c. 建立误差传播模型：  
       - 量化假设错误的影响（如忽略相位信息的信号重建失真度）  
    ```  
    *强制中断：每推进3个推理步骤即进行逆向质疑*

    **4. 风险防御（Fallacy Shield）**  
    ```  
    a. 常见谬误预判  
       - 列举领域内典型误解（如"傅里叶变换适用于任何信号"）  
       - 植入自我纠正触发器："此处是否混淆了连续与离散变换？"  
    b. 历史教训整合  
       - 引用著名错误案例（傅里叶论文审查争议）  
    c. 建立置信度标尺：  
       - 对每个结论标注：经验验证/理论证明/学界共识等级  
    ```  
    *启用对抗训练模式：生成两个对立观点进行辩论*

    **5. 适应性封装（Adaptive Packaging）**  
    ```  
    a. 知识粒度调节  
       - 核心公式的三种呈现方式：  
         1. 符号化抽象：X(ω)=∫x(t)e^{-iωt}dt  
         2. 几何解释：时域信号在正交基向量上的投影  
         3. 工程隐喻：信号成分的"化学元素分析仪"  
    b. 构建认知阶梯：  
       - 基础层：必要定义与直观解释  
       - 深化层：与已有知识的连接接口  
       - 拓展层：开放研究问题（如非平稳信号处理局限）  
    c. 埋设思维钩子：  
       - "注意到频域分辨率与时域精度的此消彼长了吗？这引出了..."  
    ```  
    *最终输出要求：消除所有二阶导数（避免嵌套过深的逻辑层级）*

    **执行约束**  
    - 每完成一个阶段立即进行跨阶段一致性检查  
    - 强制引入至少两个非常规关联领域（如音乐理论→量子计算）  
    - 保持自我对话可视性：用【认知旁白】形式保留质疑过程  
    
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
    
    保持回答连贯性和知识递进性。
    
    特别注意处理以下情况：
    - 当问题涉及先前概念时自动关联解释
    - 对重复提问智能识别并差异化响应
    - 上下文矛盾时的澄清处理
    
    对用户要友善，语气可以轻松活泼一些，适当使用emoji.
    尽量给出结构化的回答，可以使用分点等手段。
    
    接下来给出分析结果，请根据分析内容回答用户问题：
    """

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
