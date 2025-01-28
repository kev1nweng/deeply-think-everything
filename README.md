# DeeplyThinkEverything

> “探索未至之境”&nbsp;&nbsp;&nbsp;&nbsp;—— DeepSeek

赋予任何大模型深度思考的能力 | Empower any LLM with the ability to "DeepSeek".

## 原理

利用 `system` 提示词使模型先对问题进行详细的分析与反思，再将将输出的分析内容作为 `system` 提示词注入到负责回答问题的 AI 中，从而实现类深度思考。

## 立即尝试

### Linux（以 Debian 系为例）

1. 克隆该 Git 仓库

```bash
git clone https://github.com/kev1nweng/deeply-think-everything.git
```

2. 安装依赖

```bash
sudo apt install python3 python3-openai python3-rich python3-wcwidth python3-pylatexenc python3-prompt-toolkit
```

> 除了 Debian 系之外的 Linux 发行版似乎可以直接用 pip 安装这些依赖

3. 将 `config.example.ini` 重命名为 `config.ini` 并修改其中的 API 地址和密钥

4. 运行

```bash
python3 app.py
```

### Windows

0. 安装 Python 和 Git

1. 克隆该 Git 仓库

```bash
git clone https://github.com/kev1nweng/deeply-think-everything.git
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 将 `config.example.ini` 重命名为 `config.ini` 并修改其中的 API 地址和密钥

4. 运行

```bash
python app.py
```

## 效果

### 示例问题1：`how old is the earth?`

- DeepSeek V3（不启用深度思考）和 gpt-4o-mini 模型回答对比：

```markdown
DeepSeek V3

The Earth is approximately **4.54 billion years old**, with an uncertainty of about **50 million years**. This age is determined through radiometric dating of the oldest rocks on Earth, as well as meteorites that formed around the same time as the solar system. The oldest known Earth rocks are about 4 billion years old, while zircon crystals found in younger rocks have been dated to as old as 4.4 billion years.
```

```markdown
gpt-4o-mini

The Earth is approximately 4.54 billion years old, with an uncertainty of about 1%. This age has been determined through various dating methods, including radiometric dating of the oldest rocks and meteorites.
```
- DeepSeek R1（深度思考启用）和 gpt-4o-mini（DeeplyThinkEverything）模型回答对比：

```markdown
DeepSeek R1

The Earth is approximately **4.54 billion years old**, with a margin of error of about ±50 million years. This age is determined primarily through **radiometric dating** of meteorites and the oldest Earth rocks, as well as lunar samples. Here's a concise breakdown:

1. **Methods**:
   - Scientists use isotopes like uranium-238 and lead-206 to measure decay rates in ancient rocks and meteorites.
   - Meteorites, remnants from the solar system's formation, provide the most consistent dates because Earth's oldest rocks (about 4 billion years old) have been altered by geological activity.

2. **Consensus**:
   - The estimate aligns with multiple dating techniques (e.g., lead-lead dating, argon-argon) and studies of lunar samples (4.4–4.5 billion years old).
   - The Earth formed shortly after the solar system began coalescing around 4.568 billion years ago.

3. **Context**:
   - The universe is much older, about **13.8 billion years**, while the Sun and solar system (including Earth) formed roughly 4.5–4.6 billion years ago.

This age is widely accepted in the scientific community and supported by extensive cross-disciplinary evidence.
```

```markdown
gpt-4o-mini + DeeplyThinkEverything（2025年1月28日版本）

Hello! I'm DeeplyThinkEverythingAI. 🌟
The Earth is approximately 4.6 billion years old! This estimate comes from various scientific methods, primarily using radiometric dating techniques, such as uranium-lead dating, which analyze the decay of radioactive isotopes in rocks.

Here’s a bit more context for you:

 1 Formation Process: The Earth formed from the dust and gas surrounding the young Sun, which itself is about 4.6 billion years old.

 2 Dating Techniques:

 • Radiometric Dating: This method involves measuring the abundance of radioactive isotopes and their decay products in rocks and minerals.

 • Geological Evidence: The age is also supported by studying rock layers and fossil records.

 3 Comparison with Other Celestial Bodies: The age of Earth is similar to that of other planets in the solar system, like Mars and the Moon.

If you're curious about how we measure the age of the Earth or its implications for life and evolution, feel free to ask! 🌍✨
```


```markdown
gpt-4o-mini + DeeplyThinkEverything（2025年1月26日版本）

The Earth is approximately 4.54 billion years old! 🌍✨ This estimate comes from scientists who have measured the age of the oldest rocks on Earth, as well as meteorites, using techniques such as radioactive isotope dating.

To break it down a bit:

1. **Scientific Methods**: Scientists use methods like uranium-lead dating to determine the ages of rocks. This is similar to weighing an object to find out its mass—it's a reliable way to measure time.

2. **Formation of the Earth**: The Earth formed from the dust and gas surrounding the young Sun, a process that involved the gradual accumulation of material over time.

3. **Key Events**: After its formation, the Earth cooled down, oceans formed, and eventually, life began to emerge.

4. **Cosmic Context**: It's also interesting to note that while the Earth is about 4.54 billion years old, the universe itself is estimated to be around 13.8 billion years old! This helps us understand the Earth's place in the broader cosmos.

If you're curious to learn more, you might want to check out resources related to Earth sciences or astronomy! 📚🔭

```

- DeepSeek R1（深度思考启用）和 gpt-4o-mini（DeeplyThinkEverything）模型思考过程对比：

```markdown
DeepSeek R1

Okay, the user is asking how old the Earth is. Let me start by recalling what I know about this. I remember that scientists estimate the Earth's age using radiometric dating, particularly with uranium-lead dating on meteorites and the oldest Earth rocks. The figure I've come across before is around 4.5 billion years. But I should make sure that's accurate.
Wait, why do they use meteorites? Oh right, because Earth's surface is constantly changing due to geological processes like erosion and plate tectonics, so the oldest rocks on Earth aren't as old as the planet itself. Meteorites, on the other hand, are remnants from the early solar system and can give a more accurate estimate of when the Earth formed.
Let me check the methods again. Radiometric dating involves measuring the decay of radioactive isotopes. For example, uranium-238 decays into lead-206 with a half-life of about 4.5 billion years. By comparing the ratio of uranium to lead in samples, scientists can calculate how much time has passed since the rock solidified. The oldest Earth rocks found are about 4 billion years old, but meteorites have been dated to around 4.56 billion years. That's why the Earth's age is pegged at approximately 4.5 to 4.6 billion years.
I should also consider other dating methods to see if they corroborate this. For instance, lead-lead dating and studying the ages of the Moon rocks, which are around 4.4 to 4.5 billion years old. The consensus among scientists is pretty strong here, so the answer should confidently state that the Earth is about 4.54 billion years old, with a small margin of error. I should mention that this age is consistent across various dating methods and samples, reinforcing its accuracy. Also, maybe note that this age is for the Earth's formation, not the universe or the solar system as a whole, though they are related. The solar system formed around the same time, so the Earth's age is very close to that of the solar system.
Wait, the user might not know the difference between the age of the Earth and the universe. Maybe add a brief note about the universe being much older, around 13.8 billion years, just to provide context. But the main answer should focus on the Earth's age.
So putting it all together: The Earth is approximately 4.54 billion years old, determined through radiometric dating of meteorites and the oldest Earth minerals. This estimate is supported by multiple lines of evidence and is widely accepted in the scientific community.
I should also mention the margin of error, which is usually around 50 million years, so the age is often stated as 4.5 billion years with some uncertainty. Clarifying that the exact number is about 4.54 but commonly rounded to 4.5 or 4.6 billion. Also, perhaps a brief history of how this was determined, like the work of Clair Patterson in the 1950s using lead isotopes in meteorites. That might add some context, but maybe that's more detailed than needed. The user probably wants a concise answer.
Double-checking sources: According to the latest scientific consensus, the age is 4.54 ± 0.05 billion years. So yes, 4.54 billion is accurate. I'll present that as the answer, explaining the methods briefly and noting the agreement among different dating techniques. Avoid any potential misunderstandings, such as confusing Earth's age with the age of life or the universe. Keep it clear and straightforward.
```

```markdown
gpt-4o-mini + DeeplyThinkEverything（2025年1月28日版本）

用户说英语。
分析：
首先，用户询问地球的年龄，这是一个涉及地球科学、天文学和地质学的跨学科问题。为了有效地回答这个问题，我需要考虑几个方面。

1. 需求解构：
   a. 显性需求解析
   - 用户直接询问地球的年龄，涉及的关键概念是“地球”和“年龄”。
   - 操作指令是“询问”，希望得到一个具体的数值或范围。
   b. 隐性需求推理
   - 用户可能是对科学感兴趣的普通公众，或者是学生。
   - 可能希望了解地球的形成过程或相关的科学背景。
   c. 建立认知基线
   - 用户可能需要一些基础知识，如地球的形成理论（如大爆炸理论、地球的冷却过程等）。
   - 可能需要了解放射性同位素测年法的基本原理。

2. 知识图谱构建：
   a. 核心概念裂解
   - 地球的年龄通常是通过地质学和天文学的证据来推算的，涉及放射性同位素测年、岩石层分析等。
   b. 建立三维关联：
   - 纵向：地球形成的历史背景（如太阳系的形成）。
   - 横向：与其他天体的比较（如月球、火星的年龄）。
   - 轴向：科学方法（如碳测年法、铀铅测年法）。
   c. 植入反事实节点：
   - “如果没有放射性同位素测年法，我们如何估算地球的年龄？”

3. 认知推演：
   a. 专家思维链重建
   - 地质学家的视角：通过岩石层和化石记录推算地球的历史。
   - 天文学家的视角：通过对太阳系的形成理论进行推导。
   b. 多模态验证：
   - 科学文献中关于地球年龄的研究和数据支持。
   - 通过天文观测和地质证据的相互印证。
   c. 建立误差传播模型：
   - 量化不同测年方法的误差范围（如放射性衰变的稳定性）。

4. 风险防御：
   a. 常见谬误预判
   - 可能有人认为地球的年龄是一个固定不变的数字，实际上是一个估算值。
   - 需要避免混淆地球的年龄与人类历史的时间尺度。
   b. 历史教训整合
   - 引用科学史上关于地球年龄的争议（如19世纪的估算与现代的差异）。
   c. 建立置信度标尺：
   - 对于地球年龄的估算，标注为“理论证明”级别的共识。

5. 适应性封装：
   a. 知识粒度调节
   - 核心数字：地球的年龄大约为46亿年。
   - 解释其背后的科学依据，如放射性同位素的衰变过程。
   b. 构建认知阶梯：
   - 基础层：地球的年龄是通过科学方法推算的。
   - 深化层：与太阳系其他天体的年龄比较。
   - 拓展层：开放研究问题（如地球年龄对生命演化的影响）。
   c. 埋设思维钩子：
   - “地球的年龄与我们对宇宙的理解有何关系？”

通过以上分析，我可以为用户提供一个关于地球年龄的清晰、科学的回答，同时也能引导他们思考更深层次的问题。
```

```markdown
gpt-4o-mini + DeeplyThinkEverything（2025年1月26日版本）

用户询问地球的年龄，这个问题涉及到地质学、天文学和物理学等多个领域。首先，我需要确认用户是想要一个科学的估计，还是对这个话题的历史背景感兴趣。科学上，地球的年龄大约是45.4亿年，这个数据主要来源于对地球上最古老岩石和陨石的放射性同位素测定。
在解释时，我需要考虑用户的背景知识。如果用户对科学不太熟悉，我可能需要用更简单的语言来描述，比如提到“ 地球的年龄是通过科学方法测量的，就像测量一个物体的重量一样”。同时，可能需要解释放射性同位素的概念，简单说明它是如何帮助科学家确定地球年龄的。
此外，用户可能对地球形成的过程感兴趣，因此可以提到地球是如何从太阳系的形成过程中逐渐演变而来的，这涉及到星云理论和行星形成的过程。可以简要提到一些关键事件，比如地球的冷却、海洋的形成以及生命的起源等。
同时，我也要注意可能的误区，比如有些人可能会混淆地球的年龄与宇宙的年龄。宇宙的年龄大约是138亿年，这个 信息也可以提及，以便用户更全面地理解地球在宇宙中的位置。
最后，我需要确保信息的准确性和权威性，引用一些科学机构的研究结果，比如NASA或地质学会的相关数据。同时，考虑到用户可能对这个话题的进一步探索感兴趣，可以建议他们查阅一些关于地球科学或宇宙学的书籍或资料，以便深入了解。
```
该 Demo 展示了在普通模型上实现的，与 DeepSeek 深度思考较为接近的结果。

### 示例问题2：写一个网页贪吃蛇游戏

- 纯 gpt-4o-mini：虽然可以运行，但是十分简陋，没有实时分数显示，而且没有考虑到键盘事件可能会用于页面滚动而影响游戏体验；此外，也没有在程序里写任何的注释。

```html
<!DOCTYPE html>
<html lang="zh">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>贪吃蛇游戏</title>
    <style>
      body {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #f0f0f0;
      }
      canvas {
        background-color: #fff;
        border: 1px solid #000;
      }
    </style>
  </head>
  <body>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <script>
      const canvas = document.getElementById("gameCanvas");
      const ctx = canvas.getContext("2d");

      const box = 20;
      let snake = [{ x: 9 * box, y: 9 * box }];
      let direction = "RIGHT";
      let food = {
        x: Math.floor(Math.random() * 20) * box,
        y: Math.floor(Math.random() * 20) * box,
      };
      let score = 0;

      document.addEventListener("keydown", directionControl);

      function directionControl(event) {
        if (event.keyCode === 37 && direction !== "RIGHT") direction = "LEFT";
        else if (event.keyCode === 38 && direction !== "DOWN") direction = "UP";
        else if (event.keyCode === 39 && direction !== "LEFT")
          direction = "RIGHT";
        else if (event.keyCode === 40 && direction !== "UP") direction = "DOWN";
      }

      function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < snake.length; i++) {
          ctx.fillStyle = i === 0 ? "green" : "lightgreen";
          ctx.fillRect(snake[i].x, snake[i].y, box, box);
          ctx.strokeStyle = "darkgreen";
          ctx.strokeRect(snake[i].x, snake[i].y, box, box);
        }

        ctx.fillStyle = "red";
        ctx.fillRect(food.x, food.y, box, box);

        let snakeX = snake[0].x;
        let snakeY = snake[0].y;

        if (direction === "LEFT") snakeX -= box;
        if (direction === "UP") snakeY -= box;
        if (direction === "RIGHT") snakeX += box;
        if (direction === "DOWN") snakeY += box;

        if (snakeX === food.x && snakeY === food.y) {
          score++;
          food = {
            x: Math.floor(Math.random() * 20) * box,
            y: Math.floor(Math.random() * 20) * box,
          };
        } else {
          snake.pop();
        }

        const newHead = { x: snakeX, y: snakeY };

        if (
          snakeX < 0 ||
          snakeY < 0 ||
          snakeX >= canvas.width ||
          snakeY >= canvas.height ||
          collision(newHead, snake)
        ) {
          clearInterval(game);
          alert("游戏结束！得分: " + score);
        }

        snake.unshift(newHead);
      }

      function collision(head, array) {
        for (let i = 0; i < array.length; i++) {
          if (head.x === array[i].x && head.y === array[i].y) {
            return true;
          }
        }
        return false;
      }

      const game = setInterval(draw, 100);
    </script>
  </body>
</html>
```

- gpt-4o-mini + DeeplyThinkEverything：添加了许多实用的游戏特性，并且写了样式使得页面溢出得到正确处理；将程序进行了更可维护的分文件处理；程序中也给出了必要的注释。

```html
<!DOCTYPE html>
<html lang="zh">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>贪吃蛇游戏</title>
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <h1>贪吃蛇游戏</h1>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <div id="scoreBoard">得分: <span id="score">0</span></div>
    <script src="script.js"></script>
  </body>
</html>
```

```css
body {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: Arial, sans-serif;
}

canvas {
  border: 2px solid #000;
  background-color: #f0f0f0;
}

#scoreBoard {
  margin-top: 10px;
  font-size: 20px;
}
```

```javascript
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const box = 20; // 每个方块的大小
let snake = [{ x: 9 * box, y: 9 * box }]; // 蛇的初始位置
let direction = "RIGHT"; // 蛇的初始方向
let food = {
  x: Math.floor(Math.random() * 20) * box,
  y: Math.floor(Math.random() * 20) * box,
};
let score = 0;

// 控制蛇的移动
document.addEventListener("keydown", directionControl);

function directionControl(event) {
  if (event.keyCode == 37 && direction != "RIGHT") direction = "LEFT";
  else if (event.keyCode == 38 && direction != "DOWN") direction = "UP";
  else if (event.keyCode == 39 && direction != "LEFT") direction = "RIGHT";
  else if (event.keyCode == 40 && direction != "UP") direction = "DOWN";
}

// 绘制游戏界面
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 绘制蛇
  for (let i = 0; i < snake.length; i++) {
    ctx.fillStyle = i === 0 ? "green" : "lightgreen";
    ctx.fillRect(snake[i].x, snake[i].y, box, box);
    ctx.strokeStyle = "darkgreen";
    ctx.strokeRect(snake[i].x, snake[i].y, box, box);
  }

  // 绘制食物
  ctx.fillStyle = "red";
  ctx.fillRect(food.x, food.y, box, box);

  // 蛇的移动逻辑
  let snakeX = snake[0].x;
  let snakeY = snake[0].y;

  if (direction === "LEFT") snakeX -= box;
  if (direction === "UP") snakeY -= box;
  if (direction === "RIGHT") snakeX += box;
  if (direction === "DOWN") snakeY += box;

  // 蛇吃到食物
  if (snakeX === food.x && snakeY === food.y) {
    score++;
    document.getElementById("score").innerText = score;
    food = {
      x: Math.floor(Math.random() * 20) * box,
      y: Math.floor(Math.random() * 20) * box,
    };
  } else {
    snake.pop(); // 移除最后一个部分
  }

  // 检测碰撞
  const newHead = { x: snakeX, y: snakeY };

  // 游戏结束条件
  if (
    snakeX < 0 ||
    snakeY < 0 ||
    snakeX >= canvas.width ||
    snakeY >= canvas.height ||
    collision(newHead, snake)
  ) {
    clearInterval(game);
    alert("游戏结束！得分: " + score);
  }

  snake.unshift(newHead); // 新增蛇头
}

// 检测蛇与自身的碰撞
function collision(head, array) {
  for (let i = 0; i < array.length; i++) {
    if (head.x === array[i].x && head.y === array[i].y) {
      return true;
    }
  }
  return false;
}

// 启动游戏循环
let game = setInterval(draw, 100);
```