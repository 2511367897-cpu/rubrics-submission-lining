# EvalPilot 项目讲解稿

## 一句话介绍

EvalPilot 是一个面向编程题质检和 LLM 回答评测的自动化评分平台原型，支持 Rubric 配置、Gold Answer 对照、错误类型归因、批量评测和统计报告输出。

## 为什么做这个项目

在大模型评测工作里，难点不是简单判断“回答对不对”，而是要把评测标准拆成可执行、可复核、可统计的规则。  
因此我做了这个项目，用工程化方式模拟真实评测流程。

## 核心流程

1. 输入题目、模型回答、Gold Answer 关键点和错误模式。
2. Rubric Engine 根据关键点覆盖情况、错误模式、格式结构和边界意识进行评分。
3. 输出 score、level、error_types、evidence 和 suggestion。
4. Report Service 汇总平均分、通过率、错误类型分布和低分样本。
5. Dashboard 展示整体评测结果，辅助人工复核。

## 我负责的部分

- 设计 Rubric 评分维度：正确性、完整性、可解释性、格式规范。
- 设计错误类型字典：logic_error、missing_edge_case、format_error 等。
- 编写 FastAPI 接口，支持单条评测和批量评测。
- 编写评分引擎和报告服务，输出结构化评测结果。
- 设计前端 Dashboard 原型，展示评分数据和错误分布。
- 编写测试和 CI 配置，提升项目工程化程度。

## 这个项目体现什么能力

- Prompt / Rubric 设计能力。
- 编程题质检和 Gold Answer 构建能力。
- LLM 评测流程理解能力。
- Python 后端 API 开发基础。
- 数据结构化输出和报告分析能力。
- 项目文档、测试和 GitHub 展示能力。

## 面试时可以怎么说

这个项目重点不是训练大模型，而是解决大模型评测里的数据质量问题。  
我把评测流程拆成了 Rubric、Gold Answer、错误类型、评分证据和人工复核几个部分，并用 FastAPI 和前端 Dashboard 做了一个平台原型。  
它能够展示我对 LLM 应用层、Prompt 工程和评测数据构建的理解，也能体现一定的工程实现能力。
