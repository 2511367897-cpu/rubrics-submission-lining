# 李宁｜AI 评测与应用项目集

[![CI](https://github.com/2511367897-cpu/rubrics-submission-lining/actions/workflows/ci.yml/badge.svg)](https://github.com/2511367897-cpu/rubrics-submission-lining/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Focus](https://img.shields.io/badge/Focus-LLM%20Evaluation%20%7C%20AI%20Application-1f6feb)

> 面向 **大模型评测 / Prompt 工程 / AI 数据质量 / Python AI 应用开发实习** 的个人项目集。

这个仓库包含两个可以实际运行、可以在面试中演示的项目：

| 项目 | 解决的问题 | 核心技术 | 入口 |
|---|---|---|---|
| **EvalPilot** | 用透明、可复核的 Rubric 规则评测模型回答 | Python、FastAPI、规则引擎、pytest、Docker | [查看 EvalPilot](#evalpilotllm-rubric-评测平台) |
| **JobPilot** | 解析岗位 JD、计算技能匹配度并生成申请材料 | Python、HTTP Server、JSON、CLI、正则匹配、GitHub Actions | [进入 JobPilot](./jobpilot) |

---

## EvalPilot：LLM Rubric 评测平台

EvalPilot 是一个轻量级、可解释的模型回答评测原型。

### 核心流程

```text
评测任务 + 模型回答
→ 检查必需关键点
→ 检查错误模式
→ 检查回答结构与边界条件
→ 输出分数、等级、错误类型、证据和修改建议
```

### 已实现功能

- `POST /evaluate`：单条回答评测；
- `POST /batch-evaluate`：批量评测与汇总报告；
- `GET /health`：服务健康检查；
- 0-10 分透明评分，输出 `pass / partial / fail`；
- 记录扣分证据、错误类型和修改建议；
- pytest 回归测试、Docker 与 GitHub Actions CI。

### 项目特点

EvalPilot 不只返回一个分数，而是尽量回答：

- 为什么扣分；
- 命中了什么错误；
- 缺少哪些关键点；
- 下一步应该怎样修改。

这类“可解释、可复核”的设计更接近真实的大模型评测和数据质检工作。

### 快速运行

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

启动后可访问：

```text
http://127.0.0.1:8000/docs
```

---

## JobPilot：岗位匹配与申请材料生成工具

JobPilot 是一个可在本机直接运行的求职辅助工具。

### 核心流程

```text
候选人信息 + 岗位 JD
→ 识别中英文技能关键词
→ 计算技能覆盖率
→ 输出匹配技能、缺失技能和学习建议
→ 生成 Markdown 简历与求职信
```

### Windows 一键运行

进入 `jobpilot` 文件夹，双击：

```text
start_windows.bat
```

也可以在终端运行：

```bash
cd jobpilot
py run.py
```

启动后浏览器会打开类似地址：

```text
http://127.0.0.1:8000
```

更多说明见：[JobPilot README](./jobpilot/README.md)

面试讲解与学习路径见：[JobPilot 面试指南](./jobpilot/docs/interview_guide.md)

---

## 仓库结构

```text
.
├── app/                       # EvalPilot FastAPI 服务与评测逻辑
├── frontend/                  # EvalPilot 前端原型
├── tests/                     # EvalPilot 测试
├── jobpilot/                  # JobPilot 完整项目
├── examples/                  # Rubric 示例
├── prompts/                   # Prompt 模板
├── docs/                      # 项目说明
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml   # 自动化测试
```

---

## 面试展示顺序

### 展示 EvalPilot

```text
打开 FastAPI 文档
→ 输入模型回答与评分规则
→ 调用 /evaluate
→ 展示分数、错误类型和扣分证据
→ 说明如何保证评分可解释、可复核
```

### 展示 JobPilot

```text
打开本地网页
→ 填写候选人技能
→ 粘贴岗位 JD
→ 展示匹配分与技能差距
→ 下载简历和求职信
```

---

## 项目边界

- EvalPilot 当前是透明的规则型评测原型，不代表完整的商业 LLM-as-a-Judge 系统。
- JobPilot 当前根据已识别技术关键词计算覆盖率，不代表真实录用概率。
- 两个项目都强调可运行性、可解释性、测试和工程流程，不虚构模型训练或线上部署能力。

## 求职方向

- 大模型评测 / LLM Evaluation
- Prompt 工程与评测数据构建
- AI 数据质量与内容质检
- Python AI 应用开发
