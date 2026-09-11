"""Docs that disagree with the code are bugs a model reads literally.

Everything here is a grep with a reason. None of it needs a model.
"""
import glob
import json
import os
import re
import unittest

import fixtures as fx

ROOT = os.path.normpath(os.path.join(fx.HERE, "..", ".."))
PLUGIN = os.path.join(ROOT, "understudy")


def read(*p):
    return open(os.path.join(ROOT, *p), errors="replace").read()


class Versions(unittest.TestCase):
    def test_plugin_and_marketplace_agree(self):
        a = json.load(open(os.path.join(PLUGIN, ".claude-plugin", "plugin.json")))["version"]
        b = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json")))["version"]
        self.assertEqual(a, b)

    @unittest.expectedFailure   # D4 — README says v0.1.0
    def test_readme_names_the_current_version(self):
        v = json.load(open(os.path.join(PLUGIN, ".claude-plugin", "plugin.json")))["version"]
        self.assertIn(f"v{v}", read("README.md"))


class References(unittest.TestCase):
    def test_every_plugin_root_path_exists(self):
        """`${CLAUDE_PLUGIN_ROOT}/x/y.md` in an agent or skill must be a file."""
        missing = []
        for f in glob.glob(os.path.join(PLUGIN, "**", "*.md"), recursive=True):
            for m in re.finditer(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+)", open(f).read()):
                p = os.path.join(PLUGIN, m.group(1))
                if not os.path.exists(p) and not os.path.exists(p.rstrip("/")):
                    missing.append((os.path.relpath(f, ROOT), m.group(1)))
        self.assertEqual(missing, [])

    @unittest.expectedFailure   # D3 — "CLAUDE.md Phase 4, R1/O2" points at deleted sections
    def test_claude_md_references_resolve(self):
        spec = read("CLAUDE.md")
        sections = set(re.findall(r"^##+\s+(\d+(?:\.\d+)?)\.?\s", spec, re.M))
        bad = []
        for f in glob.glob(os.path.join(PLUGIN, "**", "*"), recursive=True):
            if not f.endswith((".md", ".py")):
                continue
            for m in re.finditer(r"CLAUDE\.md[,\s]+(?:§\s*(\d+(?:\.\d+)?)|Phase (\d+))", open(f).read()):
                if m.group(2) or m.group(1) not in sections:
                    bad.append((os.path.relpath(f, ROOT), m.group(0)))
        self.assertEqual(bad, [])

    def test_every_lens_in_run_md_has_an_agent(self):
        table = read("understudy", "commands", "run.md")
        for lens in re.findall(r"^\| `(\w+)` \| `(lens-\w+)` \|", table, re.M):
            self.assertTrue(os.path.exists(os.path.join(PLUGIN, "agents", lens[1] + ".md")), lens)

    def test_lens_frontmatter_never_inherits(self):
        for f in glob.glob(os.path.join(PLUGIN, "agents", "*.md")):
            head = open(f).read().split("---")[1]
            m = re.search(r"^model:\s*(\S+)", head, re.M)
            self.assertIsNotNone(m, f)
            self.assertNotEqual(m.group(1), "inherit", f)
            self.assertIn(m.group(1), ("opus", "sonnet", "haiku"), f)


class BannedVocabulary(unittest.TestCase):
    """The prose says 'checked mechanically'. The script must check it."""

    def prose_terms(self, name):
        text = read("understudy", "references", name)
        block = re.search(r"## Banned vocabulary.*?\n> (.+?)\n", text, re.S).group(1)
        terms = []
        for t in block.split("·"):
            t = re.sub(r"\(.*?\)", "", t).strip().lower()
            if t:
                terms.append(t)
        return terms

    def script_terms(self):
        import sys
        sys.path.insert(0, fx.SCRIPTS)
        import check_capture
        return set(check_capture.BANNED) | {"ux"}

    def test_flow_shapes_terms_are_enforced(self):
        missing = [t for t in self.prose_terms("flow-shapes.md") if t not in self.script_terms()]
        self.assertEqual(missing, ["friction"])   # known gap, documented in C5

    @unittest.expectedFailure   # C5
    def test_visit_shapes_terms_are_enforced(self):
        missing = [t for t in self.prose_terms("visit-shapes.md") if t not in self.script_terms()]
        self.assertEqual(missing, [])


class Layout(unittest.TestCase):
    def test_scripts_listed_in_spec_exist(self):
        spec = read("CLAUDE.md")
        for s in re.findall(r"(\w+\.py)", spec):
            self.assertTrue(os.path.exists(os.path.join(PLUGIN, "scripts", s)), s)

    def test_gitignore_still_refuses_run_artifacts(self):
        gi = read(".gitignore")
        for pat in ("**/runs/", "**/targets/", "*.png", "session.log", ".playwright-mcp/"):
            self.assertIn(pat, gi)


if __name__ == "__main__":
    unittest.main()
