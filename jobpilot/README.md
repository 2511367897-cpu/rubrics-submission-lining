# JobPilot：AI 求职助手

JobPilot 是一个轻量级 Python 求职辅助工具，完成以下流程：

```text
个人画像 → 岗位 JD 解析 → 技能匹配度评估 → 差距建议 → 简历生成 → 求职信生成
```

项目重点展示：Python 工程化、文本结构化、规则评估、CLI 工具、文档生成和自动化测试。

## 环境要求

- Python 3.8 或以上。
- 支持 Windows、macOS、Linux。
- **无必装第三方依赖**：纯 Python 标准库即可运行。
- Jinja2 仅为可选项；未安装时会自动使用内置 Markdown 生成器。

## 最简单用法

进入 `jobpilot` 目录后运行：

```bash
python quickstart.py
```

macOS/Linux 也可使用：

```bash
python3 quickstart.py
```

Windows 也可使用：

```bat
py quickstart.py
```

成功后会生成：

```text
output/demo_profile.json
output/report.json
output/cv.md
output/letter.md
```

并显示：

```text
SUCCESS: JobPilot completed without errors.
```

## 运行前自检

```bash
python doctor.py
```

它会检查 Python 版本、项目文件和核心模块导入情况。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

测试覆盖：

- 技能关键词边界匹配，避免把 `interested` 误识别成 `rest`。
- Windows CRLF 换行格式。
- 空技能岗位评分。
- 无 Jinja2、无模板文件时的内置生成器。
- 错误 JSON 的可读提示。
- CLI 防止误覆盖个人档案。
- quickstart 端到端流程。

GitHub Actions 会在 Python 3.8、3.10、3.12 上执行诊断、编译、单元测试和一键运行。

## 手动使用

### 1. 创建个人档案

```bash
python cli.py init-profile --output my_profile.json
```

文件已存在时不会直接覆盖。确认需要覆盖时：

```bash
python cli.py init-profile --output my_profile.json --force
```

### 2. 评估岗位匹配度

```bash
python cli.py evaluate-job \
  --profile my_profile.json \
  --job sample_data/sample_job.md \
  --output output/report.json
```

报告包含：

```text
score
matched_skills
missing_skills
recommendations
summary
detected_job_skills
```

### 3. 生成简历

```bash
python cli.py generate-cv \
  --profile my_profile.json \
  --job sample_data/sample_job.md \
  --output output/cv.md
```

### 4. 生成求职信

```bash
python cli.py generate-cover-letter \
  --profile my_profile.json \
  --job sample_data/sample_job.md \
  --output output/letter.md
```

模板参数已有默认值，因此不必手动输入模板路径。

## 项目结构

```text
jobpilot/
├── README.md
├── cli.py
├── quickstart.py
├── doctor.py
├── requirements.txt
├── ai_job_assistant/
│   ├── profile.py
│   ├── job.py
│   ├── evaluator.py
│   └── generator.py
├── templates/
├── sample_data/
└── tests/
```

## 简历写法

```text
JobPilot：AI 求职助手 / 岗位匹配与申请材料生成系统｜个人项目
技术栈：Python、JSON、CLI、规则引擎、Jinja2（可选）、GitHub Actions

- 设计候选人画像、岗位 JD 解析、技能匹配度评估和申请材料生成流程。
- 使用 dataclass 构建 Profile、Job 等数据结构，将非结构化岗位文本转为结构化技能数据。
- 实现关键词边界匹配与技能差距分析，输出匹配分、已匹配技能、缺失技能和改进建议。
- 实现无第三方依赖的 Markdown 简历与求职信生成器，并支持可选 Jinja2 自定义模板。
- 编写环境诊断、端到端 quickstart、8 项回归测试及 Python 3.8/3.10/3.12 CI 流程。
```

## 项目边界

当前版本是规则型 AI 应用原型，不会调用真实大模型，也不会自动投递岗位。后续可接入 LLM API、Web 页面、岗位数据库和 PDF 导出功能。
