"""The export is what a client reads. These pin the properties §11.5 fought
for: fixed reading order, a generated index that cannot drift, an overall
score nobody authored, competitor sections that never count, the matrix
last, screenshots beside the findings that cite them, and no filesystem
path in prose.
"""
import os
import re
import subprocess
import sys
import tempfile
import unittest

import fixtures as fx

sys.path.insert(0, fx.SCRIPTS)
import render_report as rr  # noqa: E402


def _read(*a, **k):
    with open(*a, **k) as fh:
        return fh.read()


def _write(path, text):
    with open(path, "w") as fh:
        fh.write(text)


RENDER = os.path.join(fx.SCRIPTS, "render_report.py")


def build(t):
    """A website run with lenses written in the WRONG order on disk, a compare
    lens with a matrix, and one competitor site scored 10/10."""
    run = fx.clean_run(t, with_lens=False)
    fx.manifest(run, objectives=["clarity", "technical", "ux", "compare"],
                competitors=["https://example-stratus.test"])
    fx.run_summary(run)
    fx.lens(run, "ux", [fx.finding("ux", "Settings toggle has no explanation", sev="P2",
                                   flow="surfaces", locator="/settings")], score=7)
    fx.lens(run, "technical", [fx.finding("technical", "Hero image is 1.8 MB", sev="P1",
                                          flow="measure:/:mobile", locator="/")], score=5)
    fx.lens(run, "clarity", [fx.finding("clarity", "The fold names no audience", sev="P1")], score=4)
    fx.lens(run, "compare", [fx.finding("compare", "Trails on price findable", sev="P1",
                                        flow="compare:trust:price", locator="/pricing")],
            score=4, matrix="| Dimension | Ours | Stratus | Verdict |\n|---|---|---|---|\n"
                            "| Price findable | ✗ absent | ✓ 3 tiers | **trails** |\n")
    fx.persona(run, base=os.path.join(run, "compare", "comp-stratus"))
    fx.lens(run, "compare/comp-stratus/clarity",
            [fx.finding("clarity", "Competitor fold is clear", sev="P3")], score=10,
            verdict="The competitor's fold is clear.")
    return run


def render(run, scope):
    p = subprocess.run([sys.executable, RENDER, run, "--format", "html", "--scope", scope],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    with open(p.stdout.strip().split("\n")[-1]) as f:
        return f.read()


class Order(unittest.TestCase):
    def test_sections_follow_lens_order_not_disk_order(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            labels = ["Clarity", "Competitive comparison", "Performance and delivery", "Usability"]
            pos = [html.find(f"</span> {l} — ") for l in labels]
            self.assertTrue(all(p > 0 for p in pos), pos)
            self.assertEqual(pos, sorted(pos), "sections are not in LENS_ORDER")

    def test_lens_order_constant_matches_spec(self):
        self.assertEqual(rr.LENS_ORDER, ["clarity", "conversion", "trust", "compare", "seo",
                                         "aeo", "technical", "ux", "bugs", "onboarding", "content"])


class Index(unittest.TestCase):
    def test_contents_lists_every_section_once(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            idx = re.search(r'<ul class="idxlist">(.*?)</ul>', html, re.S).group(1)
            items = re.findall(r"<li>", idx)
            # 8 summary H2s + 4 client lenses + competitor lens + matrix
            self.assertEqual(len(items), 8 + 4 + 1 + 1, idx)
            self.assertIn("Site-by-site comparison", idx)


class Scores(unittest.TestCase):
    def test_overall_is_mean_of_client_lenses_only(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            overall = re.search(r'scorebig[^>]*>([\d.]+)', html).group(1)
            # ux 7, technical 5, clarity 4, compare 4 → 5.0; competitor 10 excluded
            self.assertEqual(overall, "5.0")
            self.assertIn("Mean of the 4 checks", html)

    def test_competitor_section_is_labelled_context(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            self.assertIn("Competitor site — shown for comparison only", html)

    def test_cover_tally_excludes_competitor(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            cover = html[:html.find("</section>")]
            self.assertIn("4 — 3 P1 · 1 P2", cover)   # not "5 — … 1 P3"


class Content(unittest.TestCase):
    def test_matrix_is_the_last_section(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            last = html.rfind("<section")
            self.assertIn('id="site-by-site"', html[last:])
            self.assertIn("<strong>trails</strong>", html) if "<strong>trails" in html else \
                self.assertIn('class="vd vtrails">trails', html)

    def test_fix_column_is_rendered(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            self.assertIn("Recommended fix", html)
            self.assertIn("Say who it is for in the headline", html)

    def test_summary_scope_embeds_a_screenshot(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            self.assertIn("data:image/png;base64,", html)

    def test_no_filesystem_path_in_output(self):
        with tempfile.TemporaryDirectory() as t:
            run = build(t)
            html = render(run, "all")
            self.assertNotIn(t, html)
            self.assertNotIn(run, html)

    def test_generic_persona_caveat_on_cover(self):
        with tempfile.TemporaryDirectory() as t:
            cover = render(build(t), "summary").split("</section>")[0]
            self.assertIn("constructed, not researched", cover)

    def test_unknown_persona_mode_still_gets_caveat(self):
        with tempfile.TemporaryDirectory() as t:
            run = build(t)
            fx.manifest(run, persona_mode="transcript_derived")
            cover = render(run, "summary").split("</section>")[0]
            self.assertIn("constructed, not researched", cover)

    def test_dense_markdown_written_on_every_render(self):
        with tempfile.TemporaryDirectory() as t:
            run = build(t)
            render(run, "clarity")
            self.assertTrue(os.path.exists(os.path.join(run, "report-full.md")))


class Objectives(unittest.TestCase):
    def test_results_fill_the_declared_heading(self):
        with tempfile.TemporaryDirectory() as t:
            run = build(t)
            fx.write(os.path.join(run, "objectives", "results.md"),
                     "# Objectives\n\nOne of one met.\n\n## Results\n| # | Objective | Verdict |\n"
                     "|---|---|---|\n| 1 | Find the price | **Not achieved** |\n")
            p = os.path.join(run, "exec-summary.md")
            _write(p, _read(p).replace("## Contents\n\n", "## Contents\n\n## Objectives\n\n"))
            html = render(run, "summary")
            i = html.find("Objectives</h2>")
            self.assertGreater(i, 0)
            self.assertIn("Not achieved", html[i:i + 800])

    def test_results_still_rendered_without_the_heading(self):
        with tempfile.TemporaryDirectory() as t:
            run = build(t)
            fx.write(os.path.join(run, "objectives", "results.md"), "# O\n\nZero of one met.\n")
            html = render(run, "summary")
            self.assertIn("Zero of one met", html)


class Images(unittest.TestCase):
    def test_bare_filename_only_resolves_when_unique(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t, with_lens=False)
            fx.persona(run, "q")          # second persona, same 01-landing.png
            imgs = rr.find_images(run)
            self.assertNotIn("01-landing.png", imgs)
            self.assertIn("persona-p/screenshots/01-landing.png", imgs)
            self.assertIn("persona-q/screenshots/01-landing.png", imgs)


class Units(unittest.TestCase):
    def test_human_date(self):
        self.assertEqual(rr.human_date("2026-09-04T10:01:19+00:00"), "4 September 2026")
        self.assertEqual(rr.human_date(""), "")

    def test_lens_label_keeps_site(self):
        self.assertEqual(rr.lens_label("aeo"), "Answer-engine readiness")
        self.assertEqual(rr.lens_label("compare/comp-a/trust"), "Trust and credibility — comp-a")

    def test_extract_findings_reads_the_whole_block(self):
        md = fx.finding("ux", "Long repro", sev="P2", extra="- **Repro:**\n" +
                        "".join(f"  {i}. step\n" for i in range(1, 20)))
        f = rr.extract_findings("## Findings\n" + md, "d1-")[0]
        self.assertEqual(f["sev"], "P2")
        self.assertEqual(f["fix"], "Say who it is for in the headline")


if __name__ == "__main__":
    unittest.main()
