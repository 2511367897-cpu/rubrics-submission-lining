# EvalPilot：LLM 自动化评测与 Rubric 评分平台

一个面向 **Prompt 工程、LLM 评测、编程题质检、Rubric 数据构建** 的个人项目。  
项目目标不是简单写几个评分规则，而是模拟真实公司里的大模型评测流程：**题目导入 → Gold Answer → Rubric 配置 → 模型回答评分 → 错误类型归因 → 统计报告输出 → 人工复核**。

> 简历项目名建议写：`EvalPilot：LLM 自动化评测与 Rubric 评分平台｜FastAPI + Rubric Engine + Evaluation Dashboard`

## 项目价值

大模型评测不是只看“回答对不对”，而是要解决三个问题：

1. **怎么把主观判断拆成可执行的评分规则？**
2. **怎么让不同评测员的打分尽量一致？**
3. **怎么定位模型常见错误，并形成可复盘的数据报告？**

EvalPilot 用一个小型评测平台的形式，把这些能力展示出来。

## 核心功能

- **Rubric 配置化评分**：支持按正确性、完整性、可解释性、格式规范、边界条件等维度打分。
- **错误类型归因**：自动标记 `logic_error`、`missing_edge_case`、`format_error`、`incomplete_answer` 等错误。
- **Gold Answer 对照**：基于参考答案要点检查模型回答覆盖情况。
- **批量评测**：支持 JSONL 数据批量导入，输出结构化评分结果。
- **统计报告**：统计平均分、通过率、错误类型分布、低分样本。
- **API 服务**：提供 FastAPI 接口，模拟真实评测平台后端。
- **Dashboard 原型**：提供前端数据看板原型，展示分数分布与错误分布。
- **面试材料**：内置项目讲解、面试问答和简历写法。

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 后端 API | Python, FastAPI, Pydantic |
| 评测引擎 | Rule-based Rubric Engine |
| 数据格式 | JSONL, JSON |
| 前端原型 | HTML, CSS, JavaScript |
| 工程化 | pytest, GitHub Actions, Docker |
| 方向关键词 | Prompt Engineering, LLM Evaluation, Rubric, Gold Answer, Error Taxonomy |

## 项目结构

```text
.
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── services/
│       ├── rubric_engine.py
│       └── report_service.py
├── frontend/
│   └── index.html
├── examples/
│   ├── coding_task_sample.md
│   ├── evaluation_cases.jsonl
│   └── rubric_config.json
├── prompts/
│   └── rubric_template.md
├── tests/
│   └── test_rubric_engine.py
├── docs/
│   ├── project_pitch.md
│   └── interview_qa.md
└── .github/
    └── workflows/
        └── ci.yml
```

## 快速运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 API 服务

```bash
uvicorn app.main:app --reload
```

打开：

```text
http://127.0.0.1:8000/docs
```

### 3. 批量评测示例

```bash
python tools/evaluate_submission.py examples/evaluation_cases.jsonl
```

### 4. 打开前端看板

直接打开：

```text
frontend/index.html
```

## API 示例

### POST `/evaluate`

输入：

```json
{
  "case_id": "prime_001",
  "task": "判断整数是否为质数",
  "model_output": "质数是大于 1 且只能被 1 和自身整除的整数...",
  "required_keywords": ["大于 1", "sqrt", "false", "true"],
  "fail_patterns": ["1 是质数", "只判断奇偶"]
}
```

输出：

```json
{
  "case_id": "prime_001",
  "score": 10,
  "level": "pass",
  "error_types": [],
  "evidence": ["覆盖关键点：大于 1", "覆盖关键点：sqrt"],
  "suggestion": "答案覆盖核心逻辑、边界条件和复杂度说明。"
}
```

## 简历写法

```text
EvalPilot：LLM 自动化评测与 Rubric 评分平台｜个人项目
- 设计面向编程题质检场景的 Rubric 评分引擎，拆分正确性、完整性、可解释性、格式规范和边界条件等维度。
- 基于 Gold Answer 和错误类型字典构建结构化评测流程，支持 score、level、error_types、evidence、suggestion 输出。
- 使用 FastAPI 搭建评测接口，支持单条评测与批量评测，并通过报告服务统计平均分、通过率和错误类型分布。
- 设计前端 Dashboard 原型展示评分结果、错误分布和低分样本，模拟真实 LLM 评测平台的数据闭环。
```

## 面试介绍

这个项目是一个 LLM 评测平台原型，主要展示我对 Prompt 工程、Rubric 评分、Gold Answer、错误类型归因和批量质检流程的理解。  
我把编程题评测拆成评分维度、关键点覆盖、错误模式识别和结构化报告几个模块，并用 FastAPI 做了 API 服务，用前端页面模拟评测 Dashboard。  
这个项目重点不是训练大模型，而是展示我对大模型应用层评测流程、数据质量控制和人机协同复核的理解。
