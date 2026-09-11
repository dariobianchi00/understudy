"""The capture-eval runner's graders and setup — no browser, no model."""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest

import fixtures as fx

EVALS = os.path.normpath(os.path.join(fx.HERE, "..", "evals"))
sys.path.insert(0, EVALS)
import run_capture as rc  # noqa: E402


def good_run(t, persona="evaluator"):
    run = fx.clean_run(t, with_lens=False)
    fx.manifest(run, personas=[{"name": persona, "device": "desktop-1440x900"}], objectives=["clarity"])
    pdir = fx.persona(run, persona, shots=("00-landing.png", "01-scrolled.png", "02-pricing.png"),
                      log="[pre-session] Arrived via: search\n[pre-session] What I was told: \"x\"\n"
                          "[00:00] Landed. Screenshot 00-landing.png. innerWidth 1440.\n"
                          "[00:40] Scrolled. Screenshot 01-scrolled.png.\n"
                          "[01:30] Pricing. Screenshot 02-pricing.png.\n")
    fx.write(os.path.join(pdir, "timeline.json"), json.dumps(
        {"viewport": {"width": 1440, "height": 900, "verified": True},
         "shape_v1": {"time_to_comprehension_seconds": None},
         "shape_v3": {"forms_submitted": 0}, "left_early": False}))
    fx.write(os.path.join(pdir, "persona-debrief.md"),
             "**Q1** a\n**Q2** b\n**Q3** c\n**Q4** d\n**Q5** e\n**Q6** f\n")
    fx.write(os.path.join(pdir, "network-full.txt"), "[GET] http://localhost:8765/ → 200\n")
    fx.write(os.path.join(pdir, "console-full.txt"), "")
    # spread the screenshot mtimes across a 100 s session
    now = time.time()
    for i, s in enumerate(("00-landing.png", "01-scrolled.png", "02-pricing.png")):
        os.utime(os.path.join(pdir, "screenshots", s), (now - 90 + i * 40, now - 90 + i * 40))
    return run, pdir, now - 100, now


class Graders(unittest.TestCase):
    def test_good_capture_passes(self):
        with tempfile.TemporaryDirectory() as t:
            run, pdir, t0, t1 = good_run(t)
            fails, facts = rc.grade(run, "evaluator", t, t0, t1)
            self.assertEqual(fails, [], facts.get("gate"))
            self.assertEqual(facts["screenshots"], 3)
            self.assertGreaterEqual(facts["shots_spread_pct"], 25)

    def test_batched_screenshots_fail(self):
        with tempfile.TemporaryDirectory() as t:
            run, pdir, t0, t1 = good_run(t)
            for s in os.listdir(os.path.join(pdir, "screenshots")):
                os.utime(os.path.join(pdir, "screenshots", s), (t1 - 1, t1 - 1))
            fails, _ = rc.grade(run, "evaluator", t, t0, t1)
            self.assertTrue(any("clustered" in f for f in fails), fails)

    def test_unnamed_screenshot_fails(self):
        with tempfile.TemporaryDirectory() as t:
            run, pdir, t0, t1 = good_run(t)
            open(os.path.join(pdir, "screenshots", "09-stray.png"), "wb").write(fx.PNG)
            fails, _ = rc.grade(run, "evaluator", t, t0, t1)
            self.assertTrue(any("never names" in f for f in fails), fails)

    def test_pre_session_after_first_action_fails(self):
        with tempfile.TemporaryDirectory() as t:
            run, pdir, t0, t1 = good_run(t)
            p = os.path.join(pdir, "session.log")
            lines = open(p).read().splitlines()
            open(p, "w").write("\n".join(lines[2:3] + lines[:2] + lines[3:]) + "\n")
            fails, _ = rc.grade(run, "evaluator", t, t0, t1)
            self.assertTrue(any("pre-session" in f for f in fails), fails)

    def test_form_submission_fails(self):
        with tempfile.TemporaryDirectory() as t:
            run, pdir, t0, t1 = good_run(t)
            fx.write(os.path.join(pdir, "network-full.txt"), "[POST] http://localhost:8765/demo → 200\n")
            fails, _ = rc.grade(run, "evaluator", t, t0, t1)
            self.assertTrue(any("POST" in f for f in fails), fails)

    def test_transit_dir_left_behind_fails(self):
        with tempfile.TemporaryDirectory() as t:
            run, pdir, t0, t1 = good_run(t)
            os.makedirs(os.path.join(t, ".playwright-mcp"))
            fails, _ = rc.grade(run, "evaluator", t, t0, t1)
            self.assertTrue(any(".playwright-mcp" in f for f in fails), fails)

    def test_banned_word_fails_through_the_gate(self):
        with tempfile.TemporaryDirectory() as t:
            run, pdir, t0, t1 = good_run(t)
            with open(os.path.join(pdir, "session.log"), "a") as f:
                f.write("[02:00] The CTA is weak.\n")
            fails, facts = rc.grade(run, "evaluator", t, t0, t1)
            self.assertIn("check_capture failed", fails)
            self.assertIn("banned term 'cta'", facts["gate"])


class Setup(unittest.TestCase):
    def test_target_initialises_a_run(self):
        with tempfile.TemporaryDirectory() as t:
            run = rc.init_run(8765, "evaluator", t)
            m = json.load(open(os.path.join(run, "manifest.json")))
            self.assertEqual(m["assessment_type"], "website")
            self.assertEqual(m["personas"][0]["name"], "evaluator")
            self.assertTrue(os.path.isdir(os.path.join(run, "persona-evaluator", "screenshots")))

    def test_system_prompt_carries_skill_and_references(self):
        s = rc.system_prompt("sceptic", "/tmp/run", 8765)
        self.assertIn("Mode A-visit capture", s)
        self.assertIn("references/visit-shapes.md", s)
        self.assertIn("references/banned-vocabulary.md", s)
        self.assertIn("390x844", s)
        self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", s)
        # the persona must not receive the scoring framework
        for banned in ("heuristics-framework", "severity-rubric", "report-template"):
            self.assertNotIn(banned, s)

    def test_mcp_config_is_valid_json(self):
        cfg = json.loads(rc.mcp_config())
        self.assertIn("playwright", cfg["mcpServers"])

    def test_dry_run(self):
        with tempfile.TemporaryDirectory() as t:
            p = subprocess.run([sys.executable, os.path.join(EVALS, "run_capture.py"), "--dry-run",
                                "--out", t], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue(os.path.exists(os.path.join(t, "system-prompt.txt")))


if __name__ == "__main__":
    unittest.main()
