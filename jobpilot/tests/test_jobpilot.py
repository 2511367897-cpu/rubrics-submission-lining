import tempfile
import unittest
from pathlib import Path

from ai_job_assistant.evaluator import evaluate_fit
from ai_job_assistant.generator import render_cover_letter, render_cv
from ai_job_assistant.job import parse_job_description
from ai_job_assistant.profile import Education, Experience, Profile, load_profile
from cli import main as cli_main


class JobPilotTests(unittest.TestCase):
    def build_profile(self):
        return Profile(
            name="Li Ning",
            email="2511367897@qq.com",
            phone="13163586952",
            summary="AI undergraduate focused on Prompt Engineering and LLM evaluation.",
            skills=["python", "llm", "prompt engineering", "llm evaluation", "rubric", "json", "markdown"],
            experience=[Experience(company="TalentsAI", role="Evaluator", description="Reviewed model outputs.", start_year=2025)],
            education=[Education(institution="Henan Institute of Technology", degree="Bachelor", field="Artificial Intelligence", start_year=2024, end_year=2028)],
        )

    def test_parser_avoids_substring_false_positive(self):
        job = parse_job_description("Prompt Intern\nExample Company\nWe are interested in prompt engineering and Python.")
        self.assertNotIn("rest", job.skills)
        self.assertIn("prompt engineering", job.skills)
        self.assertIn("python", job.skills)

    def test_parser_supports_crlf(self):
        job = parse_job_description("Intern\r\nCompany\r\n- Python\r\n- JSON")
        self.assertEqual(job.company, "Company")
        self.assertEqual(len(job.requirements), 2)

    def test_fit_report_is_structured(self):
        report = evaluate_fit(self.build_profile(), parse_job_description("Prompt Intern\nExample Company\nPython, LLM evaluation, rubric and JSON."))
        self.assertEqual(report["score"], 100.0)
        self.assertEqual(report["missing_skills"], [])
        self.assertIn("summary", report)
        self.assertIn("detected_job_skills", report)

    def test_no_skill_job_returns_zero(self):
        report = evaluate_fit(self.build_profile(), parse_job_description("Office Intern\nExample Company\nHelp with general office work."))
        self.assertEqual(report["score"], 0.0)

    def test_generators_work_without_template_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = self.build_profile()
            job = parse_job_description("Prompt Intern\nExample Company\nPython and prompt engineering.")
            cv_path = root / "cv.md"
            letter_path = root / "letter.md"
            render_cv(profile, job, root / "missing.md", cv_path)
            render_cover_letter(profile, job, root / "missing.md", letter_path)
            self.assertIn("Li Ning", cv_path.read_text(encoding="utf-8"))
            self.assertIn("Prompt Intern", letter_path.read_text(encoding="utf-8"))

    def test_invalid_profile_json_has_readable_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{bad", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "line 1"):
                load_profile(path)

    def test_cli_init_refuses_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "profile.json"
            self.assertEqual(cli_main(["init-profile", "--output", str(path)]), 0)
            self.assertEqual(cli_main(["init-profile", "--output", str(path)]), 1)
            self.assertEqual(cli_main(["init-profile", "--output", str(path), "--force"]), 0)

    def test_quickstart_end_to_end(self):
        import quickstart
        self.assertEqual(quickstart.main(), 0)
        self.assertTrue((Path(__file__).resolve().parents[1] / "output" / "report.json").exists())


if __name__ == "__main__":
    unittest.main()
