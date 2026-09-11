"""The frozen fixture must stay a valid capture, and the answer key must
stay consistent with it. A fixture that drifts out of the contract silently
turns every lens eval into a test of the drift.
"""
import glob
import json
import os
import re
import subprocess
import sys
import unittest

import fixtures as fx

EVALS = os.path.normpath(os.path.join(fx.HERE, "..", "evals"))
SITE = os.path.join(EVALS, "fixture-site")
RUNS = {"site": os.path.join(EVALS, "fixture-run", "site"),
        "product": os.path.join(EVALS, "fixture-run", "product")}
CAPTURE = os.path.join(fx.SCRIPTS, "check_capture.py")
KEY = json.load(open(os.path.join(SITE, "planted.json")))


class Captures(unittest.TestCase):
    def test_both_frozen_runs_pass_the_capture_gate(self):
        for name, run in RUNS.items():
            p = subprocess.run([sys.executable, CAPTURE, run], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, (name, p.stdout + p.stderr))

    def test_every_screenshot_cited_in_a_log_exists(self):
        for name, run in RUNS.items():
            for pdir in glob.glob(os.path.join(run, "persona-*")):
                log = open(os.path.join(pdir, "session.log")).read()
                for shot in set(re.findall(r"\b(\d\d-[\w-]+\.png)", log)):
                    self.assertTrue(os.path.exists(os.path.join(pdir, "screenshots", shot)),
                                    f"{name}/{os.path.basename(pdir)} cites {shot}")

    def test_dumps_present_for_every_persona(self):
        for run in RUNS.values():
            for pdir in glob.glob(os.path.join(run, "persona-*")):
                for f in ("console-full.txt", "network-full.txt"):
                    self.assertTrue(os.path.exists(os.path.join(pdir, f)), (pdir, f))

    def test_screenshots_are_real_images_of_modest_size(self):
        for run in RUNS.values():
            for png in glob.glob(os.path.join(run, "**", "*.png"), recursive=True):
                size = os.path.getsize(png)
                self.assertGreater(size, 2000, png)
                self.assertLess(size, 400_000, f"{png} is {size} bytes — keep the fixture light")
                self.assertEqual(open(png, "rb").read(8), b"\x89PNG\r\n\x1a\n", png)

    def test_crawl_html_matches_the_site(self):
        html = os.path.join(RUNS["site"], "crawl", "html")
        self.assertEqual(open(os.path.join(html, "1-index.html")).read(),
                         open(os.path.join(SITE, "index.html")).read())
        self.assertEqual(open(os.path.join(html, "3-pricing.html")).read(),
                         open(os.path.join(SITE, "pricing.html")).read())

    def test_criterion_is_withheld_from_the_manifest(self):
        for run in RUNS.values():
            m = json.load(open(os.path.join(run, "manifest.json")))
            for o in m["objectives_under_test"]:
                self.assertNotIn("expected", o)
            self.assertTrue(os.path.exists(os.path.join(run, "objectives", "criteria.json")))


class AnswerKey(unittest.TestCase):
    def test_ids_unique_and_fields_present(self):
        seen = set()
        for group in ("site", "product"):
            for d in KEY[group]:
                self.assertNotIn(d["id"], seen, d["id"])
                seen.add(d["id"])
                for k in ("lenses", "band", "what", "where"):
                    self.assertIn(k, d, d["id"])
                for b in d["band"]:
                    self.assertIn(b, ("P0", "P1", "P2", "P3"))
        for group in ("site_clean", "product_clean"):
            for c in KEY[group]:
                self.assertIn("what", c)

    def test_lenses_named_in_the_key_exist(self):
        agents = {os.path.basename(f)[5:-3] for f in
                  glob.glob(os.path.join(fx.HERE, "..", "agents", "lens-*.md"))}
        for group in ("site", "product"):
            for d in KEY[group]:
                for lens in d["lenses"]:
                    self.assertIn(lens, agents, (d["id"], lens))

    def test_planted_text_is_really_on_the_pages(self):
        """A few load-bearing plants, checked against the HTML so the key and
        the site cannot drift apart."""
        idx = open(os.path.join(SITE, "index.html")).read()
        self.assertIn("We use no tracking cookies", idx)
        self.assertIn("analytics.example-tracker.test", idx)
        self.assertIn('href="#">See it in action', idx)
        self.assertIn('"price": }', idx)                       # invalid JSON-LD
        self.assertIn('name="robots" content="noindex"', open(os.path.join(SITE, "pricing.html")).read())
        about = open(os.path.join(SITE, "about.html")).read()
        self.assertIn("Priya Raman", about)                    # the clean item
        self.assertIn("FAQPage", about)
        app = os.path.join(SITE, "app")
        self.assertIn("Saved ✓", open(os.path.join(app, "new.html")).read())
        self.assertIn("Tuesday afternoons", open(os.path.join(app, "memories.html")).read())

    def test_fixture_names_no_real_product(self):
        """§7. The fixture is fictional; a real brand here is a bug."""
        # The fixture itself — not results/ (which hold whatever a model wrote)
        # and not behaviour/ (whose graders may name brands to forbid them).
        text = " ".join(open(f, errors="replace").read().lower()
                        for d in (SITE, os.path.dirname(RUNS["site"]))
                        for f in glob.glob(os.path.join(d, "**", "*"), recursive=True)
                        if f.endswith((".html", ".md", ".json", ".log", ".txt", ".py")))
        for brand in ("notion", "evernote", "obsidian", "blinklife", "smartbite", "vibrantly", "mindvalley"):
            self.assertNotIn(brand, text, brand)


if __name__ == "__main__":
    unittest.main()
