"""The eval runner's plumbing — everything that does not need a model."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

import fixtures as fx

EVALS = os.path.normpath(os.path.join(fx.HERE, "..", "evals"))
sys.path.insert(0, EVALS)
import run_evals as ev  # noqa: E402


class Prompts(unittest.TestCase):
    def test_system_prompt_is_the_agent_file_with_root_resolved(self):
        s = ev.lens_system_prompt("clarity", "/tmp/work")
        self.assertIn("Lens: Clarity", s)
        self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", s)
        self.assertIn("/tmp/work/clarity/findings-final.md", s)
        self.assertNotIn("\nname: lens-clarity", s)     # frontmatter stripped

    def test_planted_lookup(self):
        ids = {d["id"] for d in ev.planted_for("site", "trust")}
        self.assertIn("cookie-banner-mismatch", ids)
        self.assertNotIn("pricing-noindex", ids)
        self.assertEqual(ev.planted_for("product", "seo"), [])

    def test_judge_prompt_names_every_planted_and_clean_item(self):
        p = ev.judge_prompt("site", "aeo", "## Findings\n")
        for d in ev.planted_for("site", "aeo"):
            self.assertIn(d["id"], p)
        for c in ev.clean_for("site"):
            self.assertIn(c["id"], p)


class Grading(unittest.TestCase):
    FINDINGS = [{"title": "The fold names no audience", "severity": "P1"},
                {"title": "Sync graph and vault are never defined", "severity": "P2"},
                {"title": "Pricing page is noindexed", "severity": "P0"}]
    JUDGE = {"caught": [{"id": "no-audience", "caught": True, "finding_title": "The fold names no audience"},
                        {"id": "jargon-fold", "caught": True, "finding_title": "Sync graph and vault are never defined"},
                        {"id": "dead-cta", "caught": False, "finding_title": ""}],
             "clean_reported": [{"id": "about-provenance", "reported": False, "finding_title": ""}],
             "out_of_lens": ["Pricing page is noindexed"]}

    def test_summary_counts(self):
        s = ev.summarise("site", "clarity", self.JUDGE, self.FINDINGS, True, 4)
        self.assertEqual(s["planted"], len(ev.planted_for("site", "clarity")))
        self.assertEqual(s["caught"], 2)
        self.assertIn("dead-cta", s["missed_ids"])
        self.assertEqual(s["hallucinations"], [])
        self.assertEqual(s["out_of_lens"], ["Pricing page is noindexed"])
        self.assertEqual(s["n_findings"], 3)
        self.assertEqual(s["score"], 4)

    def test_band_uses_the_matched_findings_severity(self):
        rows = ev.grade_band("site", "clarity", self.JUDGE, self.FINDINGS)
        by = {r["id"]: r for r in rows}
        self.assertTrue(by["no-audience"]["in_band"])      # P1 in [P1, P2]
        self.assertTrue(by["jargon-fold"]["in_band"])      # P2 in [P2]
        self.assertNotIn("dead-cta", by)                   # not caught → not judged

    def test_judge_parse_prefers_structured_output(self):
        self.assertEqual(ev.judge_parse({"structured_output": {"caught": [1]}}), {"caught": [1]})
        got = ev.judge_parse({"result": 'noise {"caught": [], "clean_reported": [], "out_of_lens": []} tail'})
        self.assertEqual(got["caught"], [])
        self.assertIn("_unparsed", ev.judge_parse({"result": "not json"}))

    def test_parse_findings_via_gate_parser(self):
        md = "## Findings\n" + fx.finding("clarity", "The fold names no audience", sev="P1")
        self.assertEqual(ev.parse_findings(md), [{"title": "The fold names no audience", "severity": "P1"}])

    def test_history_row_shape(self):
        s = ev.summarise("site", "clarity", self.JUDGE, self.FINDINGS, True, 4)
        r = ev.history_row("2026-09-11T0000Z", "site", "clarity", "opus", 1, s, 1.234, 61.2, "/x/results/r")
        self.assertEqual(list(r.keys()), ev.HISTORY_COLS)
        self.assertEqual(r["contract_pass"], 1)
        self.assertEqual(r["cost_usd"], 1.234)


class DryRun(unittest.TestCase):
    def test_dry_run_writes_prompts_and_calls_nothing(self):
        with tempfile.TemporaryDirectory() as t:
            p = subprocess.run([sys.executable, os.path.join(EVALS, "run_evals.py"), "--capture", "site",
                                "--lens", "clarity", "--dry-run", "--out", t],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue(os.path.exists(os.path.join(t, "site-clarity-run1", "system-prompt.txt")))
            self.assertIn("dry-run", p.stdout)


if __name__ == "__main__":
    unittest.main()
