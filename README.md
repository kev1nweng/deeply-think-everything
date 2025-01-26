# DeeplyThinkEverything

> “探索未至之境”&nbsp;&nbsp;&nbsp;&nbsp;—— DeepSeek

赋予任何大模型深度思考的能力 | Empower any LLM with the ability to "DeepSeek". 

## 原理

利用 `system` 提示词使模型先对问题进行详细的分析与反思，再将将输出的分析内容作为 `system` 提示词注入到负责回答问题的 AI 中，从而实现类深度思考。

## 立即尝试

1. 克隆该 git 仓库

```sh
git clone https://github.com/DeepSeekEverything/DeeplySeekEverything.git
```

2. 安装依赖

```sh
sudo apt install python3 python3-openai python3-rich python3-wcwidth
```

3. 重命名配置文件 `config.example.ini` 并修改配置文件 `config.ini`

4. 运行

```sh
python3 app.py
```
## 效果

**示例问题：`how old is the earth`?** 

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
gpt-4o-mini + DeeplyThinkEverything

The Earth is approximately 4.54 billion years old! 🌍✨ This estimate comes from scientists who have measured the age of the oldest rocks on Earth, as well as meteorites, using techniques such as radioactive isotope dating.

To break it down a bit:

1. **Scientific Methods**: Scientists use methods like uranium-lead dating to determine the ages of rocks. This is similar to weighing an object to find out its mass—it's a reliable way to measure time.

2. **Formation of the Earth**: The Earth formed from the dust and gas surrounding the young Sun, a process that involved the gradual accumulation of material over time.

3. **Key Events**: After its formation, the Earth cooled down, oceans formed, and eventually, life began to emerge.

4. **Cosmic Context**: It's also interesting to note that while the Earth is about 4.54 billion years old, the universe itself is estimated to be around 13.8 billion years old! This helps us understand the Earth's place in the broader cosmos.

If you're curious to learn more, you might want to check out resources related to Earth sciences or   
astronomy! 📚🔭
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
gpt-4o-mini + DeeplyThinkEverything

用户询问地球的年龄，这个问题涉及到地质学、天文学和物理学等多个领域。首先，我需要确认用户是想要一个科学的估计，还是对这个话题的历史背景感兴趣。科学上，地球的年龄大约是45.4亿年，这个数据主要来源于对地球上最古老岩石和陨石的放射性同位素测定。
在解释时，我需要考虑用户的背景知识。如果用户对科学不太熟悉，我可能需要用更简单的语言来描述，比如提到“ 地球的年龄是通过科学方法测量的，就像测量一个物体的重量一样”。同时，可能需要解释放射性同位素的概念，简单说明它是如何帮助科学家确定地球年龄的。
此外，用户可能对地球形成的过程感兴趣，因此可以提到地球是如何从太阳系的形成过程中逐渐演变而来的，这涉及到星云理论和行星形成的过程。可以简要提到一些关键事件，比如地球的冷却、海洋的形成以及生命的起源等。
同时，我也要注意可能的误区，比如有些人可能会混淆地球的年龄与宇宙的年龄。宇宙的年龄大约是138亿年，这个 信息也可以提及，以便用户更全面地理解地球在宇宙中的位置。
最后，我需要确保信息的准确性和权威性，引用一些科学机构的研究结果，比如NASA或地质学会的相关数据。同时，考虑到用户可能对这个话题的进一步探索感兴趣，可以建议他们查阅一些关于地球科学或宇宙学的书籍或资料，以便深入了解。
```
该 Demo 展示了在普通模型上实现的，与 DeepSeek 深度思考较为接近的结果。