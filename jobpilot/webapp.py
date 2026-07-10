#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import mimetypes
import re
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ai_job_assistant.evaluator import evaluate_fit
from ai_job_assistant.generator import render_cover_letter, render_cv
from ai_job_assistant.job import parse_job_description
from ai_job_assistant.profile import Profile
from cli import default_profile_data

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output" / "web"
DEFAULT_JOB = (BASE_DIR / "sample_data" / "sample_job.md").read_text(encoding="utf-8")


def _split_skills(value: str) -> List[str]:
    return sorted({item.strip().lower() for item in re.split(r"[,，\n;；]+", value) if item.strip()})


def build_profile_from_form(form: Dict[str, str]) -> Profile:
    required = {"name": "姓名", "email": "邮箱", "summary": "个人简介", "job": "岗位 JD"}
    missing = [label for key, label in required.items() if not form.get(key, "").strip()]
    if missing:
        raise ValueError("请填写：" + "、".join(missing))

    data = default_profile_data()
    data.update(
        {
            "name": form.get("name", "").strip(),
            "email": form.get("email", "").strip(),
            "phone": form.get("phone", "").strip(),
            "summary": form.get("summary", "").strip(),
            "skills": _split_skills(form.get("skills", "")),
        }
    )
    return Profile.from_dict(data)


def process_submission(
    form: Dict[str, str], output_dir: Optional[Path] = None
) -> Tuple[Dict[str, object], str, str, Dict[str, Path]]:
    profile = build_profile_from_form(form)
    job = parse_job_description(form.get("job", ""))
    report = evaluate_fit(profile, job)

    target = output_dir or OUTPUT_DIR
    target.mkdir(parents=True, exist_ok=True)
    paths = {
        "report": target / "report.json",
        "cv": target / "cv.md",
        "letter": target / "cover_letter.md",
        "profile": target / "profile.json",
    }

    paths["report"].write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    render_cv(profile, job, BASE_DIR / "templates" / "cv_template.md", paths["cv"])
    render_cover_letter(
        profile,
        job,
        BASE_DIR / "templates" / "cover_letter_template.md",
        paths["letter"],
    )
    paths["profile"].write_text(
        json.dumps(profile.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
    )

    cv = paths["cv"].read_text(encoding="utf-8")
    letter = paths["letter"].read_text(encoding="utf-8")
    return report, cv, letter, paths


def _page(
    form: Optional[Dict[str, str]] = None,
    result: Optional[Tuple[Dict[str, object], str, str, Dict[str, Path]]] = None,
    error: str = "",
) -> str:
    defaults = default_profile_data()
    values = {
        "name": str(defaults["name"]),
        "email": str(defaults["email"]),
        "phone": str(defaults["phone"]),
        "summary": str(defaults["summary"]),
        "skills": ", ".join(defaults["skills"]),
        "job": DEFAULT_JOB,
    }
    if form:
        values.update(form)

    def esc(key: str) -> str:
        return html.escape(values.get(key, ""), quote=True)

    result_html = ""
    if result:
        report, cv, letter, _paths = result
        matched = "、".join(report["matched_skills"]) or "暂无"
        missing = "、".join(report["missing_skills"]) or "暂无"
        recs = "".join(
            "<li>{}</li>".format(html.escape(item))
            for item in report["recommendations"]
        )
        result_html = """
        <section class='results'>
          <div class='score'><strong>{score}%</strong><span>{summary}</span></div>
          <div class='grid'><div><h3>已匹配技能</h3><p>{matched}</p></div><div><h3>建议补充</h3><p>{missing}</p></div></div>
          <h3>行动建议</h3><ul>{recs}</ul>
          <div class='downloads'><a href='/download?file=report'>下载报告</a><a href='/download?file=cv'>下载简历</a><a href='/download?file=letter'>下载求职信</a><a href='/download?file=profile'>下载个人档案</a></div>
          <details><summary>预览简历</summary><pre>{cv}</pre></details>
          <details><summary>预览求职信</summary><pre>{letter}</pre></details>
        </section>
        """.format(
            score=report["score"],
            summary=html.escape(str(report["summary"])),
            matched=html.escape(matched),
            missing=html.escape(missing),
            recs=recs,
            cv=html.escape(cv),
            letter=html.escape(letter),
        )

    error_html = "<div class='error'>{}</div>".format(html.escape(error)) if error else ""
    return """<!doctype html>
<html lang='zh-CN'>
<head>
<meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>JobPilot</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f4f7fb;color:#172033}
header{background:#111827;color:white;padding:34px 20px}header div,main{max-width:1100px;margin:auto}h1{margin:0 0 8px}main{padding:24px 20px}
form,.results{background:white;border:1px solid #dbe3ef;border-radius:18px;padding:22px;box-shadow:0 12px 30px rgba(15,23,42,.08);margin-bottom:22px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}label{display:block;font-weight:700;margin-bottom:6px}input,textarea{width:100%;border:1px solid #cbd5e1;border-radius:10px;padding:11px;font:inherit}textarea{min-height:120px;resize:vertical}.field{margin-bottom:16px}
button{border:0;border-radius:10px;background:#2563eb;color:#fff;padding:12px 18px;font-weight:700;cursor:pointer}.score{display:flex;align-items:center;gap:20px;border-bottom:1px solid #e5e7eb;padding-bottom:18px;margin-bottom:18px}.score strong{font-size:42px;color:#2563eb}
.downloads{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}.downloads a{text-decoration:none;background:#eef2ff;color:#1d4ed8;padding:10px 14px;border-radius:9px;font-weight:700}pre{white-space:pre-wrap;background:#0f172a;color:#e2e8f0;padding:16px;border-radius:10px;overflow:auto}.error{background:#fee2e2;color:#991b1b;padding:13px;border-radius:10px;margin-bottom:18px}
@media(max-width:720px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body><header><div><h1>JobPilot AI 求职助手</h1><p>填写个人信息和岗位 JD，一键生成匹配报告、定制简历和求职信。</p></div></header>
<main>{error}
<form method='post' action='/analyze'>
<div class='grid'><div class='field'><label>姓名</label><input name='name' value='{name}'></div><div class='field'><label>邮箱</label><input name='email' value='{email}'></div></div>
<div class='field'><label>电话</label><input name='phone' value='{phone}'></div>
<div class='field'><label>个人简介</label><textarea name='summary'>{summary}</textarea></div>
<div class='field'><label>技能（逗号或换行分隔）</label><textarea name='skills'>{skills}</textarea></div>
<div class='field'><label>岗位 JD（第一行岗位名，第二行公司名）</label><textarea name='job' style='min-height:260px'>{job}</textarea></div>
<button type='submit'>开始分析并生成材料</button></form>{result}</main></body></html>""".format(
        error=error_html,
        name=esc("name"),
        email=esc("email"),
        phone=esc("phone"),
        summary=esc("summary"),
        skills=esc("skills"),
        job=esc("job"),
        result=result_html,
    )


class JobPilotHandler(BaseHTTPRequestHandler):
    def _send_html(self, content: str, status: int = 200) -> None:
        data = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            self._send_html(_page())
            return
        if parsed.path == "/health":
            payload = b'{"status":"ok"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        if parsed.path == "/download":
            key = urllib.parse.parse_qs(parsed.query).get("file", [""])[0]
            mapping = {
                "report": OUTPUT_DIR / "report.json",
                "cv": OUTPUT_DIR / "cv.md",
                "letter": OUTPUT_DIR / "cover_letter.md",
                "profile": OUTPUT_DIR / "profile.json",
            }
            path = mapping.get(key)
            if path is None or not path.exists():
                self.send_error(404, "File not generated yet")
                return
            data = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(path.name)[0] or "application/octet-stream")
            self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(path.name))
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if self.path != "/analyze":
            self.send_error(404)
            return
        form = None
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 2_000_000:
                raise ValueError("提交内容过大。")
            raw = self.rfile.read(length).decode("utf-8")
            parsed = urllib.parse.parse_qs(raw, keep_blank_values=True)
            form = {key: values[0] for key, values in parsed.items()}
            result = process_submission(form)
            self._send_html(_page(form=form, result=result))
        except (ValueError, OSError) as exc:
            self._send_html(_page(form=form, error=str(exc)), status=400)

    def log_message(self, format: str, *args: object) -> None:
        return


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), JobPilotHandler)


def serve(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = create_server(host, port)
    print("JobPilot is running at http://{0}:{1}".format(host, server.server_address[1]))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    serve()
