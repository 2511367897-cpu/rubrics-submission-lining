# JobPilot：AI 求职助手

JobPilot 是一个参考高星 AI 求职项目思路实现的轻量级 Python 工具，用来完成：

```text
个人画像 → 岗位 JD 解析 → 匹配度评分 → 技能差距建议 → 简历生成 → 求职信生成
```

它适合用于展示 **AI 应用开发、Prompt 工程、岗位文本分析、结构化数据处理、文档生成和命令行工具开发** 能力。

## 功能特点

- **Profile 管理**：用 JSON 保存候选人的姓名、联系方式、技能、经历和教育背景。
- **Job Parser**：从岗位描述文本中解析职位名、公司名、岗位要求和关键词。
- **Fit Evaluator**：计算候选人技能与岗位关键词的匹配度，输出 matched skills、missing skills 和 recommendations。
- **CV Generator**：使用 Jinja2 模板生成定制化 Markdown 简历。
- **Cover Letter Generator**：根据岗位信息和匹配结果生成求职信草稿。
- **CLI 工具**：提供初始化档案、评估岗位、生成简历、生成求职信等命令。

## 项目结构

```text
jobpilot/
├── README.md
├── cli.py
├── requirements.txt
├── ai_job_assistant/
│   ├── __init__.py
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

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 初始化个人档案

```bash
python cli.py init-profile --output my_profile.json
```

然后打开 `my_profile.json`，把里面的姓名、技能、经历改成你的真实内容。

### 2. 评估岗位匹配度

```bash
python cli.py evaluate-job \
  --profile my_profile.json \
  --job sample_data/sample_job.md \
  --output report.json
```

输出示例：

```json
{
  "score": 62.5,
  "matched_skills": ["python", "javascript", "prompt"],
  "missing_skills": ["fastapi", "rest", "html"],
  "recommendations": [
    "Consider learning or improving your 'fastapi' skills to better match this job."
  ]
}
```

### 3. 生成定制简历

```bash
python cli.py generate-cv \
  --profile my_profile.json \
  --job sample_data/sample_job.md \
  --cv-template templates/cv_template.md \
  --output output/cv.md
```

### 4. 生成求职信

```bash
python cli.py generate-cover-letter \
  --profile my_profile.json \
  --job sample_data/sample_job.md \
  --letter-template templates/cover_letter_template.md \
  --output output/letter.md
```

## 简历写法

```text
JobPilot：AI 求职助手 / 简历匹配与求职信生成系统｜个人项目
技术栈：Python、Jinja2、JSON、CLI、Prompt Engineering

- 参考 GitHub 高星 AI 求职项目思路，设计岗位 JD 解析、候选人画像、技能匹配度评估和文档生成流程。
- 使用 Python dataclass 构建 Profile、Job 等核心数据结构，将非结构化岗位文本转化为可分析的结构化数据。
- 实现技能匹配度评估模块，输出 matched_skills、missing_skills 和 recommendations，用于辅助简历优化和岗位选择。
- 基于 Jinja2 模板生成定制版 Markdown 简历和求职信，模拟 AI 求职助手从岗位分析到申请材料生成的完整流程。
- 提供命令行工具，支持初始化个人档案、评估岗位匹配度、生成简历和求职信，具备较好的项目可运行性和展示性。
```

## 可扩展方向

- 接入 OpenAI / Claude API，让模型直接分析 JD 和生成简历优化建议。
- 增加岗位爬虫模块，自动抓取 Boss 直聘、实习僧等岗位信息。
- 增加前端 Dashboard，展示投递岗位、匹配度和学习路线。
- 增加 PDF 导出，将 Markdown 简历转换为可投递 PDF。
