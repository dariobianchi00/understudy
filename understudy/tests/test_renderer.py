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
        with tempfile.TemporaryDirectory() as t:
            html = render(build(t), "summary")
            labels = ["Clarity", "Competitive comparison", "Performance and delivery", "Usability"]
            pos = [html.find(f"</span> {l} — ") for l in labels]
            self.assertTrue(all(p > 0 for p in pos), pos)
            self.assertEqual(pos, sorted(pos), "sections are not in LENS_ORDER")

    def test_lens_order_constant_matches_spec(self):
        self.assertEqual(rr.LENS_ORDER, ["clarity", "conversion", "trust", "icp", "compare", "seo",
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
            # no P0/P1 gap, yet the section is present and says so
            self.assertIn("No P0/P1 gaps were observed", html)
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
        # The problem appears in the corroboration table only, not again per lens.
        self.assertEqual(out.count("Companion invents a false personal business"), 1)
        self.assertEqual(out.count("Companion asserts a gym business"), 0)
        self.assertIn("Raised by Clarity (P0) · Usability (P1)", text)
        self.assertIn("The fold names no audience.", text)      # Observed bullets survive
        self.assertIn("Distinct problems", text)
        self.assertNotIn("Settings toggle has no explanation", out)  # P2 singleton → full export

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
        self.assertIn("<svg", html_out)                       # the drawn face
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
        # the same seed draws the same face every time
        self.assertEqual(ip.avatar_svg("Dana", p["title"]), ip.avatar_svg("Dana", p["title"]))
