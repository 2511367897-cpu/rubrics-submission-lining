#!/bin/zsh
set -e

cd "$(dirname "$0")"

DEEPSEEK_KEY="$(security find-generic-password -a "$USER" -s "codex-deepseek-projects" -w 2>/dev/null || true)"
if [[ -z "$DEEPSEEK_KEY" ]]; then
  echo "没有在 Mac 钥匙串中找到 DeepSeek API Key。"
  echo "请先运行项目说明中的密钥配置步骤。"
  read -k 1 "?按任意键退出…"
  exit 1
fi
export DEEPSEEK_API_KEY="$DEEPSEEK_KEY"
export DEEPSEEK_MODEL="${DEEPSEEK_MODEL:-deepseek-v4-flash}"
unset DEEPSEEK_KEY

if [[ ! -x ".venv/bin/python" ]]; then
  echo "第一次启动，正在准备运行环境…"
  python3 -m venv .venv
  .venv/bin/python -m pip install -r requirements.txt
fi

echo "EvalPilot 正在启动，浏览器会自动打开。"
exec .venv/bin/python run.py
