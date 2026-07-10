from pathlib import Path

from ai_job_assistant.evaluator import evaluate_fit
from ai_job_assistant.generator import render_cover_letter, render_cv
from ai_job_assistant.job import parse_job_description
from ai_job_assistant.profile import Education, Experience, Profile


def build_profile():
    return Profile(
        name="Li Ning",
        email="2511367897@qq.com",
        phone="13163586952",
        summary="AI undergraduate focused on Prompt Engineering and LLM evaluation.",
        skills=["python", "llm", "prompt engineering", "llm evaluation", "rubric", "json", "markdown"],
        experience=[Experience(company="TalentsAI", role="Evaluator", description="Reviewed model outputs.", start_year=2025)],
        education=[Education(institution="Henan Institute of Technology", degree="Bachelor", field="Artificial Intelligence", start_year=2024, end_year=2028)],
    )


def test_parser_avoids_substring_false_positive():
    job = parse_job_description("Prompt Intern\nExample Company\nWe are interested in prompt engineering and Python.")
    assert "rest" not in job.skills
    assert "prompt engineering" in job.skills
    assert "python" in job.skills


def test_fit_report_is_structured():
    profile = build_profile()
    job = parse_job_description("Prompt Intern\nExample Company\nPython, LLM evaluation, rubric and JSON.")
    report = evaluate_fit(profile, job)
    assert report["score"] == 100.0
    assert report["missing_skills"] == []


def test_generators_work_without_template_files(tmp_path: Path):
    profile = build_profile()
    job = parse_job_description("Prompt Intern\nExample Company\nPython and prompt engineering.")
    cv_path = tmp_path / "cv.md"
    letter_path = tmp_path / "letter.md"
    missing_template = tmp_path / "missing-template.md"

    render_cv(profile, job, missing_template, cv_path)
    render_cover_letter(profile, job, missing_template, letter_path)

    assert cv_path.exists()
    assert letter_path.exists()
    assert "Li Ning" in cv_path.read_text(encoding="utf-8")
    assert "Prompt Intern" in letter_path.read_text(encoding="utf-8")
