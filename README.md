# JobPilot：AI 求职助手 / 简历匹配与求职信生成系统

这是一个参考 GitHub 高星项目 **ai-job-search** 思路改造的个人项目，定位为：

> **AI Career Copilot：岗位解析 → 简历匹配度评估 → 技能差距分析 → 定制简历 → 求职信生成**

项目不再只是简单的 Rubric 文档，而是一个可以直接运行的 Python 小工具，适合放在简历里展示 **Prompt 工程、AI 应用开发、岗位 JD 分析、文档生成、Python 工程化** 能力。

## 为什么这个项目更适合放简历

很多 AI 岗位、Prompt 岗位、数据评测岗位都会要求候选人具备：

- 能理解岗位 JD 和业务需求；
- 能把非结构化文本转成结构化数据；
- 能设计评分规则和匹配逻辑；
- 能使用 AI/模板工具生成简历、求职信、报告；
- 能把想法做成一个可运行的工具。

JobPilot 正好覆盖这些点。

## 项目入口

核心项目在：[`jobpilot/`](./jobpilot)

```text
jobpilot/
├── README.md
├── cli.py
├── requirements.txt
├── ai_job_assistant/
│   ├── profile.py
│   ├── job.py
│   ├── evaluator.py
│   └── generator.py
├── templates/
│   ├── cv_template.md
│   └── cover_letter_template.md
├── sample_data/
│   └── sample_job.md
└── docs/
    └── interview_pitch.md
```

## 核心功能

- **个人档案管理**：用 JSON 保存姓名、联系方式、技能、经历和教育背景。
- **岗位 JD 解析**：从岗位文本中解析职位名、公司名、要求和关键词。
- **匹配度评分**：计算个人技能与岗位关键词的匹配度，输出 matched skills / missing skills / recommendations。
- **简历生成**：根据岗位信息自动生成定制版 Markdown 简历。
- **求职信生成**：根据岗位和匹配度自动生成求职信草稿。
- **CLI 命令行工具**：支持初始化档案、评估岗位、生成简历和求职信。

## 快速运行

```bash
cd jobpilot
pip install -r requirements.txt
python cli.py init-profile --output my_profile.json
python cli.py evaluate-job --profile my_profile.json --job sample_data/sample_job.md --output report.json
python cli.py generate-cv --profile my_profile.json --job sample_data/sample_job.md --cv-template templates/cv_template.md --output output/cv.md
python cli.py generate-cover-letter --profile my_profile.json --job sample_data/sample_job.md --letter-template templates/cover_letter_template.md --output output/letter.md
```

## 简历写法

```text
JobPilot：AI 求职助手 / 简历匹配与求职信生成系统｜个人项目
技术栈：Python、Jinja2、JSON、CLI、Prompt Engineering

- 参考 GitHub 高星 AI 求职项目思路，设计岗位 JD 解析、候选人画像、技能匹配度评估和文档生成流程。
- 使用 Python dataclass 构建 Profile、Job 等核心数据结构，将非结构化岗位文本转化为可分析的结构化数据。
- 实现技能匹配度评估模块，输出 matched_skills、missing_skills 和学习建议，用于辅助简历优化和岗位选择。
- 基于 Jinja2 模板生成定制版 Markdown 简历和求职信，模拟 AI 求职助手从岗位分析到申请材料生成的完整流程。
- 提供命令行工具，支持初始化个人档案、评估岗位匹配度、生成简历和求职信，具备较好的项目可运行性和展示性。
```

## 面试介绍

这个项目是一个 AI 求职助手原型，参考了 GitHub 上高星的 AI job search 项目思路。  
我把求职流程拆成了候选人画像、岗位解析、匹配度评估、技能差距分析和材料生成几个模块。  
项目用 Python 实现了核心流程，并通过 Jinja2 模板自动生成定制简历和求职信。  
它主要展示的是我对 AI 应用层产品、岗位文本分析、Prompt/模板生成和工程实现的理解。
