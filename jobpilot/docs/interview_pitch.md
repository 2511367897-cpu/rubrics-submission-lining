# JobPilot 面试讲解稿

## 一句话介绍

JobPilot 是一个 AI 求职助手原型，参考高星 AI 求职项目的思路，实现岗位 JD 解析、个人画像、匹配度评分、技能差距建议、简历生成和求职信生成。

## 为什么做这个项目

我想展示的不只是“会写简历”，而是把求职流程产品化：  
先把候选人的经历结构化，再把岗位 JD 结构化，然后通过匹配算法判断岗位适配度，最后用模板生成针对性的申请材料。

## 核心流程

```text
Profile JSON → Job Description → Parser → Fit Evaluator → CV / Cover Letter Generator
```

## 我负责的模块

- Profile 模块：定义候选人姓名、联系方式、技能、经历、教育背景等结构化字段。
- Job Parser 模块：解析岗位文本，提取职位名、公司名、岗位要求和关键词。
- Evaluator 模块：计算技能匹配度，输出 matched_skills、missing_skills 和 recommendations。
- Generator 模块：基于 Jinja2 模板生成 Markdown 简历和求职信。
- CLI 模块：提供 init-profile、evaluate-job、generate-cv、generate-cover-letter 命令。

## 这个项目体现的能力

- Python 工程开发基础。
- 非结构化文本到结构化数据的处理能力。
- Prompt / 模板生成思维。
- 岗位 JD 分析和简历优化理解。
- 命令行工具设计能力。
- AI 应用产品化思维。

## 面试回答示例

面试官问：这个项目和 AI 有什么关系？

可以回答：

这个项目本身是 AI 求职助手的工程原型，目前用规则和模板实现基础流程。后续可以接入 LLM API，让模型自动总结岗位要求、优化简历措辞、生成求职信，并根据面试反馈继续改进用户画像。它体现的是我对 AI 应用流程的理解：先结构化数据，再进行匹配评估，最后生成个性化内容。

## 后续扩展

- 接入 OpenAI / Claude API 做 JD 总结和简历优化。
- 增加 Web 页面，让用户上传简历和岗位 JD。
- 增加 PDF 导出。
- 增加岗位投递记录和学习路线推荐。
