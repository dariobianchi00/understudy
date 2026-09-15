"""The gates must fire — for the right reason.

A gate that never fails is indistinguishable from one that always passes.
Every test here builds a run that is clean except for exactly one thing,
runs the real CLI, and asserts both the exit code AND which check number
the failure was filed under. Failing for the wrong reason is a passing test
in a suite that only looks at exit codes.
"""
import os
import re
import subprocess
import sys
import tempfile
import unittest

import fixtures as fx


def _read(*a, **k):
    with open(*a, **k) as fh:
        return fh.read()


def _write(path, text):
    with open(path, "w") as fh:
        fh.write(text)


PY = sys.executable
CAPTURE = os.path.join(fx.SCRIPTS, "check_capture.py")
REPORT = os.path.join(fx.SCRIPTS, "check_report.py")


def gate(script, run, *args):
    p = subprocess.run([PY, script, run, *args], capture_output=True, text=True)
    out = p.stdout + p.stderr
    checks = set(int(n) for n in re.findall(r"gate check (\d)\)", out))
    if "--expect-lenses" in out and "FAILED" in out:
        checks.add(8)
    if "human-legible run folder" in out:
        checks.add(0)
    return p.returncode, checks, out


class Clean(unittest.TestCase):
    def test_clean_run_passes_both_gates(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 0, out)
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 0, out)
            self.assertIn("clarity: 1 finding(s)", out)

    def test_every_dash_parses_the_same(self):
        for dash in ("—", "–", "-"):
            with tempfile.TemporaryDirectory() as t:
                run = fx.clean_run(t)
                p = os.path.join(run, "clarity", "findings-final.md")
                s = _read(p).replace(" — The fold", f" {dash} The fold", 1)
                _write(p, s)
                rc, checks, out = gate(REPORT, run)
                self.assertEqual(rc, 0, (dash, out))
                self.assertIn("clarity: 1 finding(s)", out, dash)


class Capture(unittest.TestCase):
    def test_check2_banned_vocabulary(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.persona(run, log="[00:01] This is a P1 usability issue with the heuristic.\n")
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {2}, out)

    def test_check2_ux_in_a_url_is_not_a_hit(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.persona(run, log="[00:01] I open /docs/ux/getting-started and read.\n")
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 0, out)

    def test_check2_visit_vocabulary_is_banned_too(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.persona(run, log="[00:01] The CTA is above the fold but the conversion funnel leaks.\n")
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {2}, out)

    def test_check2_url_token_is_not_a_hit(self):
        """/plans/p1 is a page the persona visited, not a word they chose."""
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.persona(run, log="[00:01] I open https://x.test/plans/p1 and /docs/cta-guide.\n")
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 0, out)

    def test_check2_allowlist_waives_and_is_printed(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.manifest(run, vocabulary_allowlist=["usability"])
            fx.persona(run, log="[00:01] The nav has a tab called Usability.\n")
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 0, out)
            self.assertIn("NOT checked: usability", out)

    def test_check2_reading_md_is_scanned(self):
        """Mode D's per-site reading is first-person prose; it is scanned."""
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.write(os.path.join(run, "compare", "comp-a", "reading.md"),
                     "I think this fold has a P2 severity problem.\n")
            fx.write(os.path.join(run, "compare", "comp-a", "site.json"), "{}")
            fx.write(os.path.join(run, "compare", "index.json"), '{"sites": []}')
            os.makedirs(os.path.join(run, "compare", "comp-a", "screenshots"))
            fx.write_png(os.path.join(run, "compare", "comp-a", "screenshots", "0.png"))
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 1)
            self.assertIn(2, checks, out)

    def test_check5_exclusions_key_must_exist_but_may_be_empty(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            import json
            m = json.loads(_read(os.path.join(run, "manifest.json")))
            del m["scope_exclusions"]
            _write(os.path.join(run, "manifest.json"), json.dumps(m))
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {5}, out)

    def test_missing_dumps_warn_not_fail(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 0, out)
            self.assertIn("console-full.txt missing", out)

    def test_check5_missing_traversal_model(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.manifest(run, models={"scoring": {}})
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {5}, out)

    def test_check5_missing_persona_mode(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.manifest(run, persona_mode=None)
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {5}, out)

    def test_legibility_no_screenshots(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            for f in os.listdir(os.path.join(run, "persona-p", "screenshots")):
                os.remove(os.path.join(run, "persona-p", "screenshots", f))
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 1)
            self.assertIn("no screenshots", out)

    def test_legibility_log_without_timestamps(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.persona(run, log="I landed and looked around.\n")
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 1)
            self.assertIn("no [MM:SS] timestamps", out)

    def test_mode_d_mechanical_capture_passes(self):
        """compare/<site>/ with screenshots + site.json and no persona prose is a
        valid capture; the unused root persona folder is expected."""
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            # init_run made this from the target; a mechanical capture never fills it
            for f in os.listdir(os.path.join(run, "persona-p")):
                p = os.path.join(run, "persona-p", f)
                if os.path.isfile(p):
                    os.remove(p)
            for f in os.listdir(os.path.join(run, "persona-p", "screenshots")):
                os.remove(os.path.join(run, "persona-p", "screenshots", f))
            for site in ("ours-nimbus", "comp-a"):
                sd = os.path.join(run, "compare", site)
                os.makedirs(os.path.join(sd, "screenshots"))
                fx.write_png(os.path.join(sd, "screenshots", "00-fold.png"))
                fx.write(os.path.join(sd, "site.json"), '{"url": "https://x.test"}')
            fx.write(os.path.join(run, "compare", "index.json"), '{"sites": []}')
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 0, out)
            self.assertIn("mechanical capture", out)
            self.assertIn("unused", out)

    def test_mode_d_site_without_site_json_fails(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            sd = os.path.join(run, "compare", "comp-a")
            os.makedirs(os.path.join(sd, "screenshots"))
            fx.write_png(os.path.join(sd, "screenshots", "00-fold.png"))
            fx.write(os.path.join(run, "compare", "index.json"), '{"sites": []}')
            rc, checks, out = gate(CAPTURE, run)
            self.assertEqual(rc, 1)
            self.assertIn("site.json missing", out)


class Report(unittest.TestCase):
    def one(self, t, **kw):
        run = fx.clean_run(t, with_lens=False)
        fx.lens(run, "clarity", [fx.finding("clarity", "The fold names no audience", **kw)])
        return run

    def test_check1_no_evidence_field(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            f = fx.finding("clarity", "The fold names no audience")
            f = "\n".join(l for l in f.split("\n") if not l.startswith("- **Evidence:**"))
            fx.lens(run, "clarity", [f])
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {1}, out)

    def test_check1_evidence_cites_nothing(self):
        with tempfile.TemporaryDirectory() as t:
            run = self.one(t, evidence="the persona seemed confused")
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {1}, out)

    def test_check1_stray_heading_fails_not_skips(self):
        """A `###` under Findings that does not parse used to print 'no
        findings reported' and PASS. It is a finding the gate never checked."""
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            fx.lens(run, "clarity", ["### Finding one\n- **Severity:** P0\n- **Evidence:** none\n"])
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {1}, out)
            self.assertIn("did not parse", out)

    def test_check3_p0_cites_missing_artifact(self):
        with tempfile.TemporaryDirectory() as t:
            run = self.one(t, sev="P0", evidence="`persona-p/screenshots/99-nope.png`")
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertIn(3, checks, out)

    def test_check3_p1_cites_missing_artifact(self):
        with tempfile.TemporaryDirectory() as t:
            run = self.one(t, sev="P1", evidence="`persona-p/screenshots/99-nope.png`")
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertIn(3, checks, out)

    def test_check3_bare_session_log_citation_resolves(self):
        """The contract's own example cites `session.log:NN` without the
        persona prefix; that resolves against the persona folder."""
        with tempfile.TemporaryDirectory() as t:
            run = self.one(t, sev="P1", evidence="`session.log:3` · `screenshots/01-landing.png`")
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 0, out)

    def test_check4_sequence_number(self):
        with tempfile.TemporaryDirectory() as t:
            run = self.one(t, fid="3")
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {4}, out)

    def test_check4_wrong_hash(self):
        with tempfile.TemporaryDirectory() as t:
            run = self.one(t, fid="0123456789ab")
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {4}, out)

    def test_check4_duplicate_id(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            f = fx.finding("clarity", "The fold names no audience")
            fx.lens(run, "clarity", [f, f])
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {4}, out)

    def test_check4_locator_inferred_when_field_absent(self):
        """No Locator field → the gate infers one from the first `/path` in the
        body. The ID must have been hashed with that same string."""
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            f = fx.finding("clarity", "The fold names no audience", locator="/pricing")
            f = "\n".join(l for l in f.split("\n") if not l.startswith("- **Locator:**"))
            f = f.replace("- **Observed:**\n", "- **Observed:**\n  - Looked at `/pricing` first.\n")
            fx.lens(run, "clarity", [f])
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 0, out)

    def test_check6_verdict_is_a_list(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            fx.lens(run, "clarity", [fx.finding("clarity", "x")], verdict="- a bullet, not a verdict")
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {6}, out)

    def test_check6_two_sentences(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            fx.lens(run, "clarity", [fx.finding("clarity", "x")],
                    verdict="The fold is unclear. Nobody can say who it is for.")
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {6}, out)

    def test_check6_no_top_3(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            fx.lens(run, "clarity", [fx.finding("clarity", "x")])
            p = os.path.join(run, "clarity", "exec-summary.md")
            _write(p, _read(p).replace("## Top 3", "## Headlines"))
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {6}, out)

    def test_check7_score_contradicts_p0(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            fx.lens(run, "clarity", [fx.finding("clarity", "x", sev="P0")], score=9)
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {7}, out)

    def test_check7_score_without_reason(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            fx.lens(run, "clarity", [fx.finding("clarity", "x")],
                    score_line="- **Score:** 4/10 — ok\n")
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {7}, out)

    def test_check7_score_within_ceiling_passes(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            fx.lens(run, "clarity", [fx.finding("clarity", "x", sev="P0")], score=5)
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 0, out)

    def test_expect_lenses_shortfall_fails(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            rc, checks, out = gate(REPORT, run, "--expect-lenses", "2")
            self.assertEqual(rc, 1)
            self.assertIn(8, checks, out)
            rc, checks, out = gate(REPORT, run, "--expect-lenses", "1")
            self.assertEqual(rc, 0, out)

    def test_mode_d_nested_lens_is_checked(self):
        """compare/<site>/<lens> is discovered, hashed by lens NAME, and gated."""
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            os.makedirs(os.path.join(run, "compare", "comp-a"))
            fx.persona(run, base=os.path.join(run, "compare", "comp-a"))
            fx.lens(run, "compare/comp-a/clarity",
                    [fx.finding("clarity", "Competitor fold is clear", sev="P3")])
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 0, out)
            self.assertIn("compare/comp-a/clarity: 1 finding(s)", out)
            # and a broken one under compare/ is failed, not skipped
            fx.lens(run, "compare/comp-a/clarity",
                    [fx.finding("clarity", "Competitor fold is clear", sev="P3", fid="1")])
            rc, checks, out = gate(REPORT, run)
            self.assertEqual(rc, 1)
            self.assertEqual(checks, {4}, out)


if __name__ == "__main__":
    unittest.main()
