"""init_run.py — the manifest written at run start, and the two refusals."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

import fixtures as fx

sys.path.insert(0, fx.SCRIPTS)
import init_run as ir  # noqa: E402

INIT = os.path.join(fx.SCRIPTS, "init_run.py")

TARGET = """slug: nimbus-notes
product_name: Nimbus Notes
base_url: https://example-nimbus-notes.test/#pricing   # a fragment, not a comment
auth:
  wall: true
  wall_location: "/login #main"
alias_email: "qa@example-nimbus-notes.test"
persona_mode: {mode}
personas:
  - name: novice
    device: desktop-1440x900
objectives:
  - clarity
competitors:
  - https://example-stratus.test/#top
scope_exclusions: []
output_dir: {out}
"""


def init(t, mode="generic", out=None):
    out = out or os.path.join(t, "runs")
    tp = os.path.join(t, "target.yaml")
    open(tp, "w").write(TARGET.format(mode=mode, out=out))
    p = subprocess.run([sys.executable, INIT, "--target", tp, "--traversal-model", "m"],
                       capture_output=True, text=True)
    return p


class Yaml(unittest.TestCase):
    def test_hash_inside_values_survives(self):
        d = ir._minimal_yaml(TARGET.format(mode="generic", out="/tmp/x"))
        self.assertEqual(d["base_url"], "https://example-nimbus-notes.test/#pricing")
        self.assertEqual(d["auth"]["wall_location"], "/login #main")
        self.assertEqual(d["competitors"], ["https://example-stratus.test/#top"])
        self.assertEqual(d["scope_exclusions"], [])

    def test_real_comments_are_stripped(self):
        self.assertEqual(ir._strip_comment("key: value   # note"), "key: value   ")
        self.assertEqual(ir._strip_comment("# whole line"), "")
        self.assertEqual(ir._strip_comment("url: https://x.test/#a"), "url: https://x.test/#a")


class Manifest(unittest.TestCase):
    def test_alias_and_allowlist_reach_the_manifest(self):
        with tempfile.TemporaryDirectory() as t:
            p = init(t)
            self.assertEqual(p.returncode, 0, p.stderr)
            m = json.load(open(os.path.join(p.stdout.strip(), "manifest.json")))
            self.assertEqual(m["alias_email"], "qa@example-nimbus-notes.test")
            self.assertEqual(m["vocabulary_allowlist"], [])
            self.assertIn("scope_exclusions", m)


class Refusals(unittest.TestCase):
    def test_unknown_persona_mode_is_refused(self):
        with tempfile.TemporaryDirectory() as t:
            p = init(t, mode="transcript_derived")
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("persona_mode", p.stderr)

    def test_output_inside_the_plugin_is_refused(self):
        with tempfile.TemporaryDirectory() as t:
            p = init(t, out=os.path.join(fx.SCRIPTS, "..", "runs"))
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("understudy plugin", p.stderr)

    def test_users_repo_allowed_when_gitignored(self):
        with tempfile.TemporaryDirectory() as t:
            repo = os.path.join(t, "theirrepo")
            os.makedirs(repo)
            subprocess.run(["git", "init", "-q", repo], check=True)
            open(os.path.join(repo, ".gitignore"), "w").write("understudy-runs/\n")
            p = init(t, out=os.path.join(repo, "understudy-runs", "nimbus"))
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertNotIn("WARNING", p.stderr)

    def test_users_repo_refused_when_not_gitignored(self):
        with tempfile.TemporaryDirectory() as t:
            repo = os.path.join(t, "theirrepo")
            os.makedirs(repo)
            subprocess.run(["git", "init", "-q", repo], check=True)
            p = init(t, out=os.path.join(repo, "understudy-runs", "nimbus"))
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("not gitignored", p.stderr)

    def test_deliverable_defaults_and_validation(self):
        with tempfile.TemporaryDirectory() as t:
            p = init(t)
            m = json.load(open(os.path.join(p.stdout.strip(), "manifest.json")))
            self.assertEqual(m["deliverable"], {"format": "pdf", "scope": "summary", "path": None})
            self.assertTrue(m["output_dir"].startswith(t))
        with tempfile.TemporaryDirectory() as t:
            tp = os.path.join(t, "target.yaml")
            open(tp, "w").write(TARGET.format(mode="generic", out=os.path.join(t, "runs"))
                                + "deliverable:\n  format: docx\n")
            p = subprocess.run([sys.executable, INIT, "--target", tp, "--traversal-model", "m"],
                               capture_output=True, text=True)
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("deliverable.format", p.stderr)

if __name__ == "__main__":
    unittest.main()
