#!/usr/bin/env python3
from __future__ import annotations

import argparse
import socket
import threading
import time
import webbrowser

import uvicorn


def find_port(host: str, preferred: int) -> int:
    for port in range(preferred, preferred + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                return port
            except OSError:
                continue
    raise OSError("没有找到可用端口。")


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch EvalPilot local web app")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    port = find_port(args.host, args.port)
    url = f"http://{args.host}:{port}"
    print("EvalPilot 已启动：" + url)
    print("按 Control+C 停止。")
    if not args.no_browser:
        threading.Thread(
            target=lambda: (time.sleep(1), webbrowser.open(url)),
            daemon=True,
        ).start()
    uvicorn.run("app.main:app", host=args.host, port=port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
