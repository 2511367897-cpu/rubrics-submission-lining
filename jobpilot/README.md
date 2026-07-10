# JobPilot：AI 求职助手

JobPilot 是一个可以在本机直接运行的求职辅助工具：

```text
填写个人信息和岗位 JD
→ 识别中英文技术关键词
→ 计算技能匹配度
→ 输出能力差距和学习建议
→ 生成定制简历与求职信
```

项目使用 Python 标准库即可运行，不需要 API Key，也不会把个人信息上传到外部服务器。

## 直接使用图形页面

### Windows

下载或克隆项目后，进入 `jobpilot` 文件夹，双击：

```text
start_windows.bat
```

也可以在终端运行：

```bat
py run.py
```

### macOS

进入 `jobpilot` 文件夹后运行：

```bash
python3 run.py
```

仓库里也提供了 `start_macos.command`。由于 ZIP 下载或 GitHub 文件权限可能丢失，首次使用可运行：

```bash
chmod +x start_macos.command
./start_macos.command
```

### Linux

```bash
python3 run.py
```

启动后程序会自动寻找可用端口并打开浏览器。没有自动打开时，终端会显示类似地址：

```text
http://127.0.0.1:8000
```

在网页中填写姓名、邮箱、简介、技能和岗位 JD，点击“开始分析并生成材料”即可。

## 网页版会生成什么

生成结果保存在本机：

```text
output/web/profile.json
output/web/report.json
output/web/cv.md
output/web/cover_letter.md
```

网页中也可以直接下载这四个文件。

匹配报告包含：

```text
score
matched_skills
missing_skills
recommendations
summary
detected_job_skills
```

## 支持的岗位内容

岗位 JD 可以是中文或英文。当前规则库可识别的部分关键词包括：

- Python、JavaScript、TypeScript、HTML、CSS、FastAPI、Flask、Django；
- SQL、MySQL、PostgreSQL、Git、GitHub、Docker、Linux；
- LLM、大模型、Prompt Engineering、提示词工程；
- LLM Evaluation、模型评测、Rubric、评分标准；
- RAG、Agent、机器学习、深度学习、PyTorch、TensorFlow；
- Vue、React、Spring Boot 等。

英文关键词采用边界匹配，避免把 `interested` 中的 `rest` 错误识别成 REST 技能。

## 环境要求

- Python 3.8 或以上；
- Windows、macOS、Linux；
- 无必装第三方依赖；
- Jinja2 是可选依赖，未安装时自动使用内置 Markdown 生成器。

## 运行自检和测试

先检查环境：

```bash
python doctor.py
```

macOS/Linux 可将 `python` 换成 `python3`。

运行全部回归测试：

```bash
python -m unittest discover -s tests -v
```

测试覆盖：

- 中英文技能关键词识别；
- 英文单词边界和误匹配防护；
- Windows CRLF 换行；
- 空技能岗位评分；
- 错误 JSON 的可读提示；
- 无 Jinja2、无模板文件时的材料生成；
- CLI 文件覆盖保护；
- 网页表单验证和网页版端到端生成；
- quickstart 完整流程。

GitHub Actions 会在 Python 3.8、3.10、3.12 上执行诊断、代码编译、测试和一键运行。

## 命令行一键演示

不使用网页时，可以运行：

```bash
python quickstart.py
```

成功后会生成：

```text
output/demo_profile.json
output/report.json
output/cv.md
output/letter.md
```

## 命令行手动使用

创建个人档案：

```bash
python cli.py init-profile --output my_profile.json
```

已有文件默认不会覆盖。确定覆盖时：

```bash
python cli.py init-profile --output my_profile.json --force
```

评估岗位：

```bash
python cli.py evaluate-job \
  --profile my_profile.json \
  --job sample_data/sample_job.md \
  --output output/report.json
```

生成简历：

```bash
python cli.py generate-cv \
  --profile my_profile.json \
  --job sample_data/sample_job.md \
  --output output/cv.md
```

生成求职信：

```bash
python cli.py generate-cover-letter \
  --profile my_profile.json \
  --job sample_data/sample_job.md \
  --output output/letter.md
```

## 项目结构

```text
jobpilot/
├── run.py                  # 自动打开网页版
├── webapp.py               # 标准库 Web 应用
├── start_windows.bat       # Windows 启动器
├── start_macos.command     # macOS 启动器
├── cli.py                  # 命令行工具
├── quickstart.py           # 一键演示
├── doctor.py               # 环境诊断
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
技术栈：Python、HTTP Server、JSON、HTML/CSS、CLI、规则引擎、GitHub Actions

- 设计候选人画像、岗位 JD 解析、技能匹配度评估和申请材料生成流程。
- 构建中英文技能关键词库与正则边界匹配逻辑，将非结构化岗位文本转为结构化技能数据。
- 使用 Python 标准库实现本地 Web 应用，支持表单输入、结果预览和报告/简历/求职信下载。
- 实现无第三方依赖的 Markdown 简历与求职信生成器，并支持可选 Jinja2 自定义模板。
- 编写环境诊断、端到端流程、回归测试和 Python 3.8/3.10/3.12 CI。
```

## 项目边界

当前版本是**规则型 AI 应用原型**，匹配分代表已识别技术关键词的覆盖率，不代表真实招聘录用概率。项目目前不会调用真实大模型，也不会自动投递岗位。
