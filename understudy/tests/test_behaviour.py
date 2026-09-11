"""The behaviour runner's plumbing and the case files — no model needed."""
import glob
import json
import os
import subprocess
import sys
import tempfile
import unittest

import fixtures as fx

EVALS = os.path.normpath(os.path.join(fx.HERE, "..", "evals"))
sys.path.insert(0, EVALS)
import run_behaviour as rb  # noqa: E402


class Cases(unittest.TestCase):
    def test_every_case_is_complete(self):
        dirs = [d for d in sorted(glob.glob(os.path.join(rb.CASES, "*"))) if os.path.isdir(d)]
        self.assertGreaterEqual(len(dirs), 9)
        for d in dirs:
            c = rb.load_case(d)
            self.assertTrue(c["prompt"], d)
            self.assertTrue(c["criteria"] or c.get("files_equal") or c.get("files_first_heading"), d)
            for rx in c.get("must_match", []) + c.get("must_not_match", []):
                import re
                re.compile(rx)

    def test_safety_cases_exist(self):
        for name in rb.SAFETY:
            self.assertTrue(os.path.isdir(os.path.join(rb.CASES, name)), name)

    def test_no_case_names_a_real_product(self):
        # prompts and criteria only — a case.json may name a brand in a
        # must_not_match regex precisely to forbid it
        text = " ".join(open(f).read().lower() for f in
                        glob.glob(os.path.join(rb.CASES, "**", "*.md"), recursive=True))
        for brand in ("blinklife", "smartbite", "vibrantly", "notion", "mindvalley"):
            self.assertNotIn(brand, text, brand)


class Graders(unittest.TestCase):
    def test_tools_called_reads_stream_json(self):
        events = [{"type": "assistant", "message": {"content": [
                      {"type": "text", "text": "hi"}, {"type": "tool_use", "name": "WebFetch", "input": {}}]}},
                  {"type": "result", "result": "done"}]
        self.assertEqual(rb.tools_called(events), ["WebFetch"])

    def test_forbidden_tool_attempt_fails_even_if_denied(self):
        case = {"name": "x", "tools_forbidden": ["WebFetch", "mcp__*"]}
        fails = rb.grade_deterministic(case, "I refused.", ["Read", "mcp__playwright__browser_navigate"], None)
        self.assertEqual(len(fails), 1)
        self.assertIn("mcp__*", fails[0])

    def test_regex_graders(self):
        case = {"name": "x", "must_match": [r"stops? at the wall"], "must_not_match": [r"logged in as"]}
        self.assertEqual(rb.grade_deterministic(case, "It stops at the wall.", [], None), [])
        fails = rb.grade_deterministic(case, "logged in as qa", [], None)
        self.assertEqual(len(fails), 2)

    def test_files_equal_is_whitespace_tolerant_but_not_paraphrase_tolerant(self):
        with tempfile.TemporaryDirectory() as t:
            case = rb.load_case(os.path.join(rb.CASES, "text-not-files"))
            os.makedirs(os.path.join(t, "clarity"))
            exp = open(os.path.join(rb.CASES, "text-not-files", "expected-exec-summary.md")).read()
            open(os.path.join(t, "clarity", "exec-summary.md"), "w").write(exp.replace("\n", "\n\n"))
            open(os.path.join(t, "clarity", "findings-final.md"), "w").write("paraphrased")
            fails = rb.grade_deterministic(case, "", [], t)
            self.assertEqual(len(fails), 1)
            self.assertIn("findings-final.md", fails[0])

    def test_first_heading_grader(self):
        with tempfile.TemporaryDirectory() as t:
            case = {"name": "x", "files_first_heading": ["exec-summary.md", "## What this is", r"^## Top 5"]}
            open(os.path.join(t, "exec-summary.md"), "w").write(
                "# Title\n\nA verdict sentence first.\n\n## What this is\n\n## Top 5 — fix these first\n")
            fails = rb.grade_deterministic(case, "", [], t)
            self.assertEqual(len(fails), 1)
            self.assertIn("opens with", fails[0])
            open(os.path.join(t, "exec-summary.md"), "w").write(
                "# Title\n\n## What this is\n- x\n\n## Top 5 — fix these first\nVerdict.\n")
            self.assertEqual(rb.grade_deterministic(case, "", [], t), [])


class DryRun(unittest.TestCase):
    def test_dry_run_substitutes_placeholders(self):
        with tempfile.TemporaryDirectory() as t:
            p = subprocess.run([sys.executable, os.path.join(EVALS, "run_behaviour.py"),
                                "--case", "run-summary-shape", "--dry-run", "--out", t],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            prompt = open(os.path.join(t, "run-summary-shape", "prompt.txt")).read()
            self.assertNotIn("{run}", prompt)
            self.assertIn("2026-09-08-run-fixture01", prompt)


if __name__ == "__main__":
    unittest.main()
