# LLM Rubric Evaluation Kit

面向 **Prompt 工程 / LLM 评测 / 编程题质检 / Rubric 数据构建** 的个人展示项目。  
本项目用于展示如何把一个“经验判断”拆成可复核的评分规则、错误类型、Gold Answer、Pass/Fail 示例与结构化输出格式。

> 适合放在简历 GitHub 项目栏：`LLM Rubric Evaluation Kit｜Prompt + Rubric + Gold Answer + Evaluation Cases`

## 项目亮点

- **Rubric 设计**：将回答质量拆成正确性、完整性、可解释性、格式规范、边界条件等维度。
- **Gold Answer**：为编程题提供参考实现、关键步骤、边界条件与可判分点。
- **Pass/Fail 示例**：用正反样例说明什么答案应该通过，什么答案应该扣分。
- **结构化评测**：输出 `score / evidence / error_type / suggestion`，便于人工复核与批量质检。
- **Prompt 模板**：提供可直接改写的 LLM 评分 Prompt，适合面试讲解和岗位投递展示。

## 目录结构

```text
.
├── README.md
├── requirements.txt
├── prompts/
│   └── rubric_template.md
├── examples/
│   ├── coding_task_sample.md
│   └── evaluation_cases.jsonl
├── tools/
│   └── evaluate_submission.py
└── docs/
    └── interview_qa.md
```

## 快速运行

```bash
python tools/evaluate_submission.py examples/evaluation_cases.jsonl
```

示例输出：

```json
{
  "case_id": "prime_001",
  "score": 9,
  "level": "pass",
  "error_types": [],
  "suggestion": "答案覆盖了核心逻辑、边界条件和复杂度说明。"
}
```

## 评分维度示例

| 维度 | 分值 | 评估重点 |
| --- | ---: | --- |
| 正确性 | 5 | 是否解决核心问题，逻辑是否正确 |
| 完整性 | 2 | 是否覆盖输入、输出、边界条件 |
| 可解释性 | 2 | 是否说明思路、复杂度、关键判断 |
| 格式规范 | 1 | 是否按要求输出，是否便于复核 |

## 简历写法参考

```text
LLM Rubric Evaluation Kit｜个人项目
- 构建面向编程题质检的 Rubric 评分模板，拆分正确性、完整性、可解释性、格式规范等维度。
- 设计 Gold Answer、错误类型字典与 Pass/Fail 示例，用于提升评测数据的一致性与可复核性。
- 编写 Python 脚本模拟结构化评分输出，支持输出 score、error_type、evidence 与 suggestion。
```

## 面试介绍话术

这个项目主要是为了展示我对 LLM 评测和 Rubric 数据构建的理解。  
我把编程题质检流程拆成 Prompt、Gold Answer、评分维度、错误类型和结构化输出几个部分。  
项目里不仅有评分模板，也有正反样例和一个简单的 Python 评测脚本，方便面试官看到我对“可判分、可复核、一致性”的理解。
