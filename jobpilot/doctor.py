#!/usr/bin/env python3
from __future__ import annotations

import importlib
import platform
import sys
from pathlib import Path


REQUIRED_FILES = [
    "cli.py",
    "quickstart.py",
    "webapp.py",
    "run.py",
    "sample_data/sample_job.md",
    "ai_job_assistant/profile.py",
    "ai_job_assistant/job.py",
    "ai_job_assistant/evaluator.py",
    "ai_job_assistant/generator.py",
]

REQUIRED_MODULES = [
    "ai_job_assistant.profile",
    "ai_job_assistant.job",
    "ai_job_assistant.evaluator",
    "ai_job_assistant.generator",
    "webapp",
]


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    print("JobPilot diagnostics")
    print("Python:", sys.version.split()[0])
    print("Platform:", platform.platform())
    print("Project:", base_dir)

    errors = []
    if sys.version_info < (3, 8):
        errors.append("Python 3.8 or newer is required.")

    for relative in REQUIRED_FILES:
        if not (base_dir / relative).exists():
            errors.append("Missing project file: " + relative)

    for module_name in REQUIRED_MODULES:
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            errors.append("Import failed for {0}: {1}".format(module_name, exc))

    if errors:
        for item in errors:
            print("ERROR:", item)
        return 1

    print("OK: environment and project files look valid.")
    print("Run 'python run.py' to open the local web app.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
