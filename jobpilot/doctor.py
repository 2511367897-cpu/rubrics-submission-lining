#!/usr/bin/env python3
from __future__ import annotations

import platform
import sys
from pathlib import Path


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    print("JobPilot diagnostics")
    print("Python:", sys.version.split()[0])
    print("Platform:", platform.platform())
    print("Project:", base_dir)
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or newer is required.")
        return 1
    required = [
        base_dir / "cli.py",
        base_dir / "quickstart.py",
        base_dir / "sample_data" / "sample_job.md",
        base_dir / "ai_job_assistant" / "profile.py",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print("ERROR: Missing project files:")
        for item in missing:
            print("-", item)
        return 1
    try:
        import ai_job_assistant.profile  # noqa: F401
        import ai_job_assistant.job  # noqa: F401
        import ai_job_assistant.evaluator  # noqa: F401
        import ai_job_assistant.generator  # noqa: F401
    except Exception as exc:
        print("ERROR: Import failed:", exc)
        return 1
    print("OK: environment and project files look valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
