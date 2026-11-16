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
    p = subprocess.run([sys.executable, RENDER, run, "--format", "print", "--scope", scope],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    with open(p.stdout.strip().split("\n")[-1]) as f:
        return f.read()


class Order(unittest.TestCase):
    def test_sections_follow_lens_order_not_disk_order(self):
        # v0.8.0: the summary lists issues by category, in the fixed category
        # order; the full export keeps every lens section, in LENS_ORDER.
        with tempfile.TemporaryDirectory() as t:
            run = build(t)
            html = render(run, "summary")
            pos = [html.find(f"</span> {l} — ") for l in ("Clarity", "Conversion", "Technical")]
            self.assertTrue(all(p > 0 for p in pos), pos)
            self.assertEqual(pos, sorted(pos), "categories are not in their fixed order")
            full = render(run, "all")
            labels = ["clarity", "compare", "technical", "ux"]
            pos = [full.find(f"— {l} — Run") for l in labels]
            self.assertTrue(all(p > 0 for p in pos), pos)
            self.assertEqual(pos, sorted(pos), "lens sections are not in LENS_ORDER")

    def test_lens_order_constant_matches_spec(self):
        self.assertEqual(rr.LENS_ORDER, ["clarity", "conversion", "trust", "icp", "compare", "seo",
                                         "aeo", "technical", "ux", "bugs", "onboarding", "content"])


class Index(unittest.TestCase):
    def test_contents_lists_every_section_once(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            idx = re.search(r'<ul class="idxlist">(.*?)</ul>', html, re.S).group(1)
            items = re.findall(r"<li>", idx)
            # 7 summary H2s + 3 categories (clarity, conversion, technical) + matrix
            self.assertEqual(len(items), 7 + 3 + 1, idx)
            self.assertIn("Site-by-site comparison", idx)


class Scores(unittest.TestCase):
    def test_overall_is_mean_of_client_lenses_only(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            overall = re.search(r'scorebig[^>]*>([\d.]+)', html).group(1)
            # categories: Clarity 4 · Conversion (ux) 7 · Technical 5 → 5.3, as the
            # HTML. The compare diff lens is the comparison, not a category, and
            # the competitor's 10 never counts.
            self.assertEqual(overall, "5.3")
            self.assertIn("Mean of the 3 categories", html)

    def test_competitor_section_is_labelled_context(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "all")
            self.assertIn("Competitor site — shown for comparison only", html)

    def test_cover_tally_excludes_competitor(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            cover = html[:html.find("</section>")]
            # 4 client findings, not 5 with the competitor's P3; the fixture's
            # findings share one screenshot pair, so they group into one issue
            self.assertIn("4 — one issue can be raised by several checks", cover)
            issues_row = re.search(r"<dt>Issues</dt><dd>([^<]*)</dd>", cover).group(1)
            self.assertNotIn("low", issues_row)      # the competitor's P3 is not an issue


ICP_PROFILES = (
    "## ICP profiles\n"
    "### 1. Solo course creator — PRIMARY · fit 4.5 · propensity 4.0\n"
    "- **Who:** One person selling a course they already teach live, no team.\n"
    "- **Find fifty of them:** Creator communities; a search for \"sell my course\".\n"
    "- **Job to be done:** Get paid without building a site.\n"
    "- **Trigger:** First cohort sells out.\n"
    "- **Why this product wins for them:**\n  - Pricing per person, not per seat (`persona-p/screenshots/03-pricing.png`)\n"
    "- **What it lacks for them:** nothing observed\n"
    "- **Fit:** pain 5 · alignment 4 · evidence 4 · clarity 5 → 4.5\n"
    "- **Propensity:** reach 4 · trigger 4 · pay 4 · openness 4 → 4.0\n"
    "- **Case against (reasoning, not evidence):**\n  - Instead they use: the status quo, a payment link\n"
    "  - Switching cost: low\n  - The fact that would kill it: they never sell twice\n"
    "  - Cheapest test: five conversations\n"
    "- **Not inferable from this run:** willingness to pay above the free tier\n"
    "- **Re-run persona:**\n  ```yaml\n  - name: creator\n    device: desktop-1440x900\n"
    "    goal: \"Sell my next cohort by Friday\"\n    gives_up_when: \"I have to build a page first\"\n  ```\n"
    "### The trap — Agencies · fit 2.0 · propensity 4.5\n"
    "Easy to sell, would churn: nothing in the product is multi-client.\n"
    "### Candidates considered\n"
    "| Candidate | Source | Fit | Propensity | Outcome |\n|---|---|---|---|---|\n"
    "| Solo course creator | named by site | 4.5 | 4.0 | primary |\n"
    "| Agencies | adjacent | 2.0 | 4.5 | trap |\n"
)


def build_icp(t):
    """A both-type run whose icp lens has profiles and one P2 gap only —
    the case a P0/P1-only summary would otherwise drop."""
    run = fx.clean_run(t, with_lens=False)
    fx.manifest(run, objectives=["clarity", "icp"], assessment_type="both")
    fx.run_summary(run)
    fx.lens(run, "clarity", [fx.finding("clarity", "The fold names no audience", sev="P1")], score=4)
    exec_extra = ICP_PROFILES
    fx.lens(run, "icp", [fx.finding("icp", "Pricing page never says who each tier is for", sev="P2",
                                    flow="V-ICP", locator="/pricing")],
            score=6, verdict="The site says who it is for; the product narrows it further.",
            top3="1. **Solo course creator** — PRIMARY · fit 4.5 · propensity 4.0\n",
            matrix=None)
    # append the profiles section to the lens's exec summary, after the score
    p = os.path.join(run, "icp", "exec-summary.md")
    _write(p, _read(p).replace("## Limits on this read", exec_extra + "\n## Limits on this read"))
    return run


class Content(unittest.TestCase):
    def test_icp_profiles_are_lifted_into_the_summary(self):
        with tempfile.TemporaryDirectory() as t:
            html = render(build_icp(t), "summary")
            self.assertIn("Ideal Customer Profiles", html)
            self.assertIn("Solo course creator", html)
            self.assertIn("The trap", html)
            self.assertIn("Candidates considered", html)
            self.assertIn("gives_up_when", html)
            # the fixture's icp gaps share evidence with category findings, so
            # they are filed where the fix lives and the section says so
            self.assertIn("filed under the area where its fix lives", html)
            # order: Clarity before Ideal Customer Profiles
            self.assertLess(html.find("</span> Clarity"), html.find("</span> Ideal Customer Profiles"))

    def test_icp_section_absent_without_the_heading(self):
        with tempfile.TemporaryDirectory() as t:
            run = build_icp(t)
            p = os.path.join(run, "icp", "exec-summary.md")
            _write(p, _read(p).replace("## ICP profiles", "## Profiles"))
            self.assertEqual(rr.icp_section(run, {}, {}), "")

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
            self.assertIn("<th>Fix</th>", html)
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

    def _toc(self, *specs):
        """specs: (lens_dir, title, sev, evidence, extra) -> a toc like main() builds."""
        toc = [None]
        for lens, title, sev, ev, extra in specs:
            md = fx.finding(lens, title, sev=sev, evidence=ev, extra=extra)
            f = rr.extract_findings("## Findings\n" + md, lens + "-")
            toc.append({"lens": rr.lens_label(lens), "dir": lens, "find": f})
        return toc

    def test_ui_labels_in_quotes_do_not_corroborate(self):
        # Two lenses both mention "Capture a note" — a button, not an
        # observation. The 2026-09-14 run paired 34 of 45 findings this way.
        toc = self._toc(
            ("ux", "Hover card eats the first click", "P2",
             "`persona-a/screenshots/01-home.png`", '- **Repro:**\n  1. Click "Capture a note" on the card\n'),
            ("content", "Today greeting is a nine-line paragraph", "P2",
             "`persona-a/screenshots/02-today.png`", '- **Repro:**\n  1. Read the greeting above "Capture a note"\n'))
        self.assertEqual(rr.corroborate(toc), [])
        self.assertEqual(rr.corroboration_clusters(toc), [])

    def test_same_screenshots_cluster_into_one_problem(self):
        # Three lenses, three wordings, one problem — same two screenshots.
        ev = "`persona-a/screenshots/05-reply.png` · `persona-a/screenshots/06-memory.png`"
        toc = self._toc(
            ("ux", "Companion asserts a gym business the user does not have", "P1", ev, ""),
            ("bugs", "Companion invents and repeats a false personal business", "P0", ev, ""),
            ("content", "'Knows you' copy invents facts from a stored memory", "P1", ev, ""))
        shared = rr.corroborate(toc)
        self.assertEqual(len(shared), 3)
        clusters = rr.corroboration_clusters(toc)
        self.assertEqual(len(clusters), 1)
        c = clusters[0]
        self.assertEqual(c["sev"], "P0")
        self.assertEqual(c["rep"]["title"], "Companion invents and repeats a false personal business")
        self.assertEqual([l for l, _ in c["raised"]], ["Defects", "Usability", "Content"])
        self.assertEqual([s for _, s in c["raised"]], ["P0", "P1", "P1"])

    def test_one_shared_screenshot_needs_a_second_signal(self):
        # A busy home screen shows two unrelated problems; one shared shot
        # and dissimilar titles must not pair them.
        toc = self._toc(
            ("ux", "Left nav offers three unexplained labels", "P2",
             "`persona-a/screenshots/01-home.png`", ""),
            ("content", "Floating photos are decorative and not clickable", "P3",
             "`persona-a/screenshots/01-home.png`", ""))
        self.assertEqual(rr.corroborate(toc), [])

    def test_summary_scope_lists_a_shared_problem_once(self):
        t = tempfile.mkdtemp(prefix="understudy-t-")
        run = build(t)
        ev = "`persona-a/screenshots/05-reply.png` · `persona-a/screenshots/06-memory.png`"
        fx.lens(run, "ux", [
            fx.finding("ux", "Companion asserts a gym business the user does not have",
                       sev="P1", evidence=ev),
            fx.finding("ux", "Settings toggle has no explanation", sev="P2", flow="surfaces",
                       locator="/settings")], score=5)
        fx.lens(run, "clarity", [
            fx.finding("clarity", "Companion invents a false personal business", sev="P0",
                       evidence=ev)], score=4)
        out = render(run, "summary")
        text = re.sub(r"<[^>]+>", " ", out)
        # One issue, under the category where its fix lives, naming both checks;
        # the merged original is not listed a second time.
        self.assertEqual(out.count("Companion invents a false personal business"), 1)
        self.assertEqual(out.count("Companion asserts a gym business"), 0)
        self.assertIn("Raised by Clarity, Usability", text)
        self.assertIn("The fold names no audience.", text)      # Observed bullets survive
        self.assertIn("Issues", text)

    def test_extract_findings_reads_the_whole_block(self):
        md = fx.finding("ux", "Long repro", sev="P2", extra="- **Repro:**\n" +
                        "".join(f"  {i}. step\n" for i in range(1, 20)))
        f = rr.extract_findings("## Findings\n" + md, "d1-")[0]
        self.assertEqual(f["sev"], "P2")
        self.assertEqual(f["fix"], "Say who it is for in the headline")


if __name__ == "__main__":
    unittest.main()


class Presentation(unittest.TestCase):
    def test_score_reason_is_sentence_cased_with_full_stop(self):
        self.assertEqual(rr.sentence("every visitor saw a price"), "Every visitor saw a price.")
        self.assertEqual(rr.sentence("Two left."), "Two left.")
        self.assertEqual(rr.sentence(""), "")

    def test_where_cell_links_sources_and_thumbnails_screenshots(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            pdir = next(d for d in os.listdir(run) if d.startswith("persona-"))
            shots = os.path.join(run, pdir, "screenshots")
            os.makedirs(shots, exist_ok=True)
            with open(os.path.join(shots, "07-pricing.png"), "wb") as f:
                f.write(b"\x89PNG\r\n\x1a\n")
            images = rr.find_images(run); images["__run__"] = run
            used = {}
            cell = f"{pdir}/session.log:41 · 07-pricing.png · Top 5 row 2 · something else"
            out = rr.where_cell(cell, images, used, prefix="d0-")
            self.assertIn('href="file://', out)
            self.assertIn("log · line 41", out)
            self.assertIn('class="shot ', out)          # thumbnail for the screenshot
            self.assertIn('href="#d0-top-5-fix-these-first"', out)
            self.assertIn("something else", out)         # unknown token left as text
            self.assertTrue(used)                        # screenshot registered for embedding

    def test_cover_carries_logo_when_cached(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            with open(os.path.join(run, "site-logo.png"), "wb") as f:
                f.write(b"\x89PNG\r\n\x1a\n" + b"0" * 300)
            uri = rr.site_logo(run, {"base_url": "https://example.invalid"})
            self.assertTrue(uri.startswith("data:image/png;base64,"))
            html_out = rr.cover({"product_name": "X"}, "X", "", 0, {}, logo=uri)
            self.assertIn('class="logo"', html_out)
            # no cache and no network: the cover still renders, without a logo
            self.assertEqual(rr.cover({"product_name": "X"}, "X", "", 0, {}).count('class="logo"'), 0)


class Interactive(unittest.TestCase):
    """--format html is the interactive report: one self-contained file with
    the run's data as JSON, every view driven from it, no network."""
    def test_html_format_builds_the_interactive_page(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            p = subprocess.run([sys.executable, RENDER, run, "--format", "html", "--scope", "all"],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            path = p.stdout.strip().splitlines()[-1]
            page = open(path, encoding="utf-8").read()
            self.assertIn('<script id="data" type="application/json">', page)
            self.assertIn('id="btnPresent"', page)
            self.assertIn('class="drawer"', page)
            self.assertNotIn("__DATA__", page)          # payload injected
            self.assertNotIn("__TITLE__", page)
            self.assertNotIn("https://cdn.", page)      # nothing fetched at open
            import json as _json
            m = re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.S)
            data = _json.loads(m.group(1).replace("<\\/", "</"))
            self.assertIn("findings", data)
            self.assertIn("lenses", data)
            self.assertIn("personas", data)
            self.assertTrue(all("id" in f and "sev" in f for f in data["findings"]))
            # the print layout is not written alongside the interactive one
            self.assertFalse(os.path.exists(path.replace(".html", "-print.html")))

    def _data(self, page):
        import json as _json
        m = re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.S)
        return _json.loads(m.group(1).replace("<\\/", "</"))

    def _html(self, run, scope="summary"):
        p = subprocess.run([sys.executable, RENDER, run, "--format", "html", "--scope", scope],
                           capture_output=True, text=True, env={**os.environ, "UNDERSTUDY_SITE_LOGO": "off"})
        self.assertEqual(p.returncode, 0, p.stderr)
        return open(p.stdout.strip().splitlines()[-1], encoding="utf-8").read(), p.stderr

    def test_mode_d_run_carries_the_comparison(self):
        """The bug of 2026-09-28: the interactive report dropped the matrix and
        the run summary's 'Against comparable sites' while the PDF kept both."""
        with tempfile.TemporaryDirectory() as t:
            run = build(t)
            p = os.path.join(run, "exec-summary.md")
            _write(p, _read(p).replace("## Limits of this assessment",
                   "## Against comparable sites\n- **Lead · trail · level:** trails on 1.\n\n"
                   "## Limits of this assessment"))
            page, _ = self._html(run)
            # v0.8.0: the matrix card is "Full matrix"; the summary's own
            # section is shown verbatim under it, so both must be in the page.
            self.assertIn("Full matrix", page)
            self.assertIn("${D.sections.against}", page)
            d = self._data(page)
            c = d["compare"]
            self.assertEqual(c["tally"], {"leads": 0, "trails": 1, "level": 0, "not comparable": 0})
            self.assertEqual([r["verdict"] for r in c["rows"]], ["trails"])
            self.assertEqual(c["sites"][0]["ours"], True)
            self.assertEqual(c["sites"][0]["name"], fx.PRODUCT)          # never "Ours"
            self.assertEqual(c["sites"][1]["name"], "Stratus")            # the matrix's own header
            self.assertEqual(c["sites"][1]["scores"]["clarity"]["score"], 10)
            self.assertEqual(c["sites"][1]["better"][0]["dim"], "Price findable")
            self.assertIn("Lead · trail · level", d["sections"]["against"])
            comp = next(l for l in d["lenses"] if l["dir"] == "compare")
            self.assertEqual(comp["tally"]["trails"], 1)
            # competitor lenses never enter the run's lens list or its mean
            self.assertFalse(any(l["dir"].startswith("compare/") for l in d["lenses"]))

    def test_run_without_compare_has_no_comparison(self):
        with tempfile.TemporaryDirectory() as t:
            page, _ = self._html(fx.clean_run(t), "all")
            self.assertIsNone(self._data(page)["compare"])

    def test_compare_lens_without_a_score_says_why(self):
        with tempfile.TemporaryDirectory() as t:
            run = build(t)
            p = os.path.join(run, "compare", "exec-summary.md")
            _write(p, re.sub(r"- \*\*Score:\*\*.*", "- No score for this lens. A position is not a quality score.", _read(p)))
            d = self._data(self._html(run)[0])
            comp = next(l for l in d["lenses"] if l["dir"] == "compare")
            self.assertIsNone(comp["score"])
            self.assertTrue(comp["noScore"])
            self.assertIn("position is not a quality score", comp["why"])

    def test_unknown_summary_section_is_kept_not_dropped(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.run_summary(run)
            p = os.path.join(run, "exec-summary.md")
            _write(p, _read(p).replace("## Limits of this assessment",
                   "## A note from the operator\n- Severity is by user impact.\n\n## Limits of this assessment"))
            page, err = self._html(run, "all")
            d = self._data(page)
            self.assertEqual([x["title"] for x in d["extraSections"]], ["A note from the operator"])
            self.assertIn("Severity is by user impact", d["extraSections"][0]["html"])
            self.assertIn("A note from the operator", err)

    def test_cut_sections_never_reach_the_pdf(self):
        # An older summary still declares both; the print path drops them, so
        # "Raised by more than one check" cannot print as an empty section.
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.run_summary(run)
            p = os.path.join(run, "exec-summary.md")
            _write(p, _read(p).replace("## Limits of this assessment",
                   "## How to read these findings\n- P0 blocks.\n\n"
                   "## Raised by more than one check\n\n## Limits of this assessment"))
            html = render(run, "summary")
            self.assertNotIn("Raised by more than one check", html)
            self.assertNotIn("How to read these findings", html)

    def test_cut_sections_stay_cut(self):
        # v0.8.0: an older run summary still carries the two cut sections;
        # neither reaches the page, not even under "More from the summary".
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.run_summary(run)
            p = os.path.join(run, "exec-summary.md")
            _write(p, _read(p).replace("## Limits of this assessment",
                   "## How to read these findings\n- Severity is by user impact.\n\n## Limits of this assessment"))
            page, err = self._html(run, "all")
            self.assertEqual(self._data(page)["extraSections"], [])
            self.assertNotIn("How to read these findings", err)

    def test_export_menu_offers_the_four_outputs_and_a_print_document(self):
        # One Export menu replaced Triage + Print. Views fill only when opened,
        # so printing builds its own document; without it the PDF was blank pages.
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            fx.run_summary(run)
            page, _ = self._html(run, "all")
            for kind in ("md", "pdf", "csv", "agent", "json", "clear"):
                self.assertIn(f'data-x="{kind}"', page)
            self.assertNotIn('id="btnPrint"', page)
            self.assertIn('id="v-print"', page)
            self.assertIn("beforeprint", page)

    def test_print_format_writes_the_document_layout_only(self):
        with tempfile.TemporaryDirectory() as t:
            run = fx.clean_run(t)
            p = subprocess.run([sys.executable, RENDER, run, "--format", "print", "--scope", "all"],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            files = os.listdir(run)
            self.assertIn("report-all-print.html", files)
            self.assertNotIn("report-all.html", files)

    def test_finding_block_parser_keeps_every_field(self):
        import interactive_report as ir
        block = ("- **Severity:** P1\n- **So what:** It costs.\n- **Flow:** shape_2\n"
                 "- **Locator:** /x — button\n- **Personas hit:** a, b\n- **Observed:**\n"
                 "  - first thing\n  - second thing\n- **Evidence:** `persona-a/screenshots/01-x.png` · `persona-a/session.log:4`\n"
                 "  > \"I could not find it anywhere on the page\"\n- **Repro:**\n  1. open\n  2. click\n- **Fix:** Say so.\n")
        fields, order, quotes, shots, logs = ir.parse_finding_block(block)
        self.assertEqual(fields["Severity"]["text"], "P1")
        self.assertEqual(fields["Observed"]["items"], ["first thing", "second thing"])
        self.assertEqual(fields["Repro"]["items"], ["open", "click"])
        self.assertEqual(shots, ["persona-a/screenshots/01-x.png"])
        self.assertEqual(logs, ["persona-a/session.log:4"])
        self.assertEqual(quotes, ["I could not find it anywhere on the page"])


class IcpCards(unittest.TestCase):
    def test_profiles_render_as_cards_with_a_face_and_a_name(self):
        import icp_profiles as ip
        body = ICP_PROFILES.split("## ICP profiles\n", 1)[1]
        d = ip.parse(body)
        self.assertEqual(len(d["profiles"]), 1)
        p = d["profiles"][0]
        self.assertEqual(p["role"], "PRIMARY")
        self.assertEqual(p["fit"], "4.5")
        self.assertTrue(p["invented"])                       # no Meet: line → placeholder
        self.assertIn("gives_up_when", p["rerun"])
        self.assertEqual(d["trap"]["title"], "Agencies · fit 2.0 · propensity 4.5")
        self.assertEqual(len(d["candidates"]["rows"]), 2)
        html_out = ip.cards_html(body, open_details=True)
        self.assertNotIn("<svg", html_out)                    # no face by default
        self.assertIn("placeholder name", html_out)
        self.assertIn("The case against", html_out)
        self.assertIn("<details class=\"icp-rerun\" open>", html_out)
        self.assertNotIn("class=\"shot", html_out)            # no thumbnails in a profile
        self.assertNotIn("`", html_out)                       # citations as plain text

    def test_meet_line_names_the_profile(self):
        import icp_profiles as ip
        body = ICP_PROFILES.split("## ICP profiles\n", 1)[1].replace(
            "- **Who:**", "- **Meet:** Dana, 34 — teaches pottery from a shared studio\n- **Who:**", 1)
        p = ip.parse(body)["profiles"][0]
        self.assertEqual(p["name"], "Dana")
        self.assertFalse(p["invented"])
        self.assertIn("Dana, 34", ip.cards_html(body))
        self.assertEqual(p["avatar"], "")                     # faces are opt-in


class Categories(unittest.TestCase):
    """v0.8.0: five categories over the checks, per-site comparison lenses
    out of every area, one issue per finding via report-overlay.json."""

    def _html(self, run):
        return Interactive._html(self, run)

    def _data(self, page):
        return Interactive._data(self, page)

    def _build(self, t, overlay=None, ours_site=False):
        """clarity 4 + content 6 → Clarity 5.0 · ux 7 + onboarding 3 →
        Conversion 5.0 · bugs 8 → Technical 8.0. Overall 6.0; the mean of
        the five checks would be 5.6."""
        run = fx.clean_run(t, with_lens=False)
        fx.manifest(run, objectives=["clarity", "content", "ux", "onboarding", "bugs"])
        fx.run_summary(run)
        ev = "`persona-p/screenshots/01-landing.png` · `persona-p/screenshots/02-pricing.png`"
        fx.lens(run, "clarity", [fx.finding("clarity", "The fold names no audience", evidence=ev,
                                            fid="cla-1")], score=4)
        fx.lens(run, "content", [fx.finding("content", "Headline does not say who the notes app is for",
                                            sev="P2", evidence=ev, fid="con-1")], score=6)
        fx.lens(run, "ux", [fx.finding("ux", "Settings toggle has no explanation", sev="P2",
                                       flow="surfaces", locator="/settings", fid="ux-1", evidence="`persona-p/screenshots/03-settings.png`")], score=7)
        fx.lens(run, "onboarding", [fx.finding("onboarding", "Signup asks for a card first",
                                               flow="entry", locator="/signup", fid="onb-1", evidence="`persona-p/screenshots/04-signup.png`")], score=3)
        fx.lens(run, "bugs", [fx.finding("bugs", "Pricing toggle throws a console error", sev="P0",
                                         flow="surfaces", locator="/pricing", fid="bug-1", evidence="`persona-p/screenshots/05-pricing-error.png`")], score=8)
        if ours_site:
            fx.lens(run, "compare/ours-nimbus/clarity",
                    [fx.finding("clarity", "Our fold, captured for the comparison", sev="P3")],
                    score=10)
            fx.lens(run, "compare", [fx.finding("compare", "Trails on price findable", sev="P1",
                                                flow="compare:trust:price", locator="/pricing")],
                    score=4, matrix="| Dimension | Ours | Verdict |\n|---|---|---|\n"
                                    "| Price findable | ✗ absent | **trails** |\n")
        if overlay is not None:
            _write(os.path.join(run, "report-overlay.json"), __import__("json").dumps(overlay))
        return run

    def test_every_check_sits_in_exactly_one_category(self):
        import interactive_report as ir
        dirs = [d for c in ir.CATEGORIES for d in c[5]]
        self.assertEqual(len(dirs), len(set(dirs)))
        self.assertEqual(set(dirs), set(rr.LENS_ORDER) - {"icp", "compare"})
        self.assertEqual(len(ir.CATEGORIES), 5)

    def test_overall_is_the_mean_of_the_categories(self):
        with tempfile.TemporaryDirectory() as t:
            d = self._data(self._html(self._build(t))[0])
            self.assertEqual({c["key"]: c["score"] for c in d["categories"]},
                             {"clarity": 5.0, "conversion": 5.0, "technical": 8.0})
            self.assertEqual(d["overall"], 6.0)
            self.assertEqual(d["scoring"], "categories-v1")

    def test_our_own_comparison_capture_is_not_an_area(self):
        # 2026-11-15: compare/<our-site>/<lens> counted as areas, 5.5 → 5.9.
        with tempfile.TemporaryDirectory() as t:
            run = self._build(t, ours_site=True)
            d = self._data(self._html(run)[0])
            self.assertFalse([l for l in d["lenses"] if l["dir"].startswith("compare/")])
            self.assertEqual(d["overall"], 6.0)
            # the print layout: the per-site 10/10 never reaches the cover
            html = render(run, "summary")
            self.assertEqual(re.search(r'scorebig[^>]*>([\d.]+)', html).group(1), "6.0")  # = the HTML

    def test_is_area(self):
        import run_layout
        self.assertTrue(run_layout.is_area("clarity"))
        self.assertTrue(run_layout.is_area("compare"))
        self.assertFalse(run_layout.is_area("compare/ours-nimbus/clarity"))
        self.assertFalse(run_layout.is_area("compare/comp-stratus/clarity"))

    def test_a_site_that_could_not_be_read_gets_no_column(self):
        import json
        with tempfile.TemporaryDirectory() as t:
            run = build(t)
            fx.persona(run, base=os.path.join(run, "compare", "comp-cirrus"))
            fx.lens(run, "compare/comp-cirrus/clarity", [], score=None, score_line="")
            fx.lens(run, "compare", [fx.finding("compare", "Trails on price findable", sev="P1",
                                                flow="compare:trust:price", locator="/pricing")],
                    score=4, matrix="| Dimension | Ours | Stratus | Cirrus | Verdict |\n|---|---|---|---|---|\n"
                                    "| Price findable | ✗ absent | ✓ 3 tiers | — not read | **trails** |\n")
            _write(os.path.join(run, "compare", "index.json"), json.dumps({"sites": [
                {"slug": "comp-stratus", "name": "Stratus", "role": "competitor",
                 "url": "https://example-stratus.test"},
                {"slug": "comp-cirrus", "name": "Cirrus", "role": "competitor",
                 "url": "https://example-cirrus.test", "comparable": False,
                 "unreachable": [{"url": "/", "reason": "HTTP 403 bot challenge"}]}]}))
            c = self._data(self._html(run)[0])["compare"]
            self.assertNotIn("Cirrus", [s["name"] for s in c["sites"]])
            self.assertNotIn("Cirrus", c["headers"])
            self.assertTrue(all(len(r["cells"]) == len(c["headers"]) - 2 for r in c["rows"]))
            self.assertEqual([x["line"] for x in c["notCompared"]],
                             ["Cirrus blocked automated browsers, so it wasn't compared."])

    def test_overlay_merges_shortens_and_picks_the_top5(self):
        ov = {"version": 1, "verdict": "Visitors cannot tell who it is for.",
              "groups": {"cla-1": ["con-1"]},
              "short": {"cla-1": {"title": "Fold names no audience", "fix": "Name the audience."}},
              "top5": [{"id": "bug-1", "effort": "Build"}, {"id": "cla-1", "effort": "Copy"}]}
        with tempfile.TemporaryDirectory() as t:
            d = self._data(self._html(self._build(t, overlay=ov))[0])
            ids = [f["id"] for f in d["findings"]]
            self.assertNotIn("con-1", ids)
            prim = next(f for f in d["findings"] if f["id"] == "cla-1")
            self.assertEqual([m["id"] for m in prim["merged"]], ["con-1"])
            self.assertEqual((prim["short"], prim["shortFix"]), ("Fold names no audience", "Name the audience."))
            self.assertEqual([r["id"] for r in d["top5"]], ["bug-1", "cla-1"])
            self.assertEqual(d["verdict"], "Visitors cannot tell who it is for.")
            self.assertEqual((d["merge"]["source"], d["merge"]["ignored"]), ("overlay", 0))

    def test_merge_takes_the_highest_severity_and_says_whose(self):
        ov = {"version": 1, "groups": {"con-1": ["cla-1"]}}
        with tempfile.TemporaryDirectory() as t:
            d = self._data(self._html(self._build(t, overlay=ov))[0])
            prim = next(f for f in d["findings"] if f["id"] == "con-1")
            self.assertEqual((prim["sev"], prim["sevFrom"]), ("P1", "Clarity"))

    def test_without_an_overlay_clusters_still_merge_and_the_page_says_so(self):
        with tempfile.TemporaryDirectory() as t:
            d = self._data(self._html(self._build(t))[0])
            self.assertEqual(d["merge"]["source"], "clusters")
            self.assertIn("not merged by the merge step", d["merge"]["note"])
            ids = [f["id"] for f in d["findings"]]
            self.assertEqual(len(ids), 4)          # five findings, one shared problem
            self.assertEqual([f["short"] for f in d["findings"] if f["id"] == "ux-1"],
                             ["Settings toggle has no explanation"])

    def test_without_an_overlay_a_category_check_leads_the_group(self):
        # 2026-11-16: a cluster led by its icp member was filed under no
        # category, and the issue dropped out of every scorecard.
        with tempfile.TemporaryDirectory() as t:
            run = self._build(t)
            ev = "`persona-p/screenshots/01-landing.png` · `persona-p/screenshots/02-pricing.png`"
            fx.lens(run, "icp", [fx.finding("icp", "The fold names no audience for the notes app",
                                            sev="P0", evidence=ev, fid="icp-1")], score=5)
            d = self._data(self._html(run)[0])
            ids = [f["id"] for f in d["findings"]]
            self.assertNotIn("icp-1", ids)
            prim = next(f for f in d["findings"] if "icp-1" in [m["id"] for m in f.get("merged", [])])
            self.assertIn(prim["cat"], {c["key"] for c in d["categories"]})
            self.assertEqual((prim["sev"], prim["sevFrom"]), ("P0", "Ideal Customer Profiles"))

    def test_a_bad_overlay_is_counted_never_fatal(self):
        ov = {"version": 1,
              "groups": {"nope": ["cla-1"], "cla-1": ["con-1", "cla-1", "ghost"], "ux-1": ["con-1"]},
              "top5": [{"id": "con-1"}, {"id": "ghost"}, {"id": "bug-1"}]}
        with tempfile.TemporaryDirectory() as t:
            d = self._data(self._html(self._build(t, overlay=ov))[0])
            self.assertEqual(sorted(f["id"] for f in d["findings"]), ["bug-1", "cla-1", "onb-1", "ux-1"])
            self.assertEqual([r["id"] for r in d["top5"]], ["bug-1"])
            # nope · cla-1 self · ghost · con-1 twice · top5 con-1 (merged) · top5 ghost
            self.assertEqual(d["merge"]["ignored"], 6)

    def test_an_overlay_of_another_version_falls_back(self):
        with tempfile.TemporaryDirectory() as t:
            d = self._data(self._html(self._build(t, overlay={"version": 2, "groups": {}}))[0])
            self.assertEqual(d["merge"]["source"], "clusters")
