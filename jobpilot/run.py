#!/usr/bin/env python3
from __future__ import annotations

import argparse
import socket
import threading
import time
import webbrowser

from webapp import create_server


def find_port(host: str, preferred: int) -> int:
    for port in range(preferred, preferred + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((host, port))
                return port
            except OSError:
                continue
    raise OSError("No available port found between {0} and {1}".format(preferred, preferred + 49))


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch JobPilot local web app")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    port = find_port(args.host, args.port)
    server = create_server(args.host, port)
    url = "http://{0}:{1}".format(args.host, port)
    print("JobPilot 已启动：" + url)
    print("按 Ctrl+C 停止。")

    if not args.no_browser:
        threading.Thread(
            target=lambda: (time.sleep(0.5), webbrowser.open(url)), daemon=True
        ).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nJobPilot 已停止。")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
