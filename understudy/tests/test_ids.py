"""Stable finding IDs — the one thing that cannot be retrofitted (§6).

`expected-ids.json` is a frozen corpus. If a change to normalisation or to
locator inference makes any row differ, that change is a schema migration:
re-ID the runs on disk deliberately, then regenerate the corpus on purpose.
A red test here is the tripwire the spec asks for.
"""
import json
import os
import sys
import unittest

import fixtures as fx

sys.path.insert(0, fx.SCRIPTS)
import finding_id as fi          # noqa: E402
import check_report as cr        # noqa: E402


def _read(*a, **k):
    with open(*a, **k) as fh:
        return fh.read()


CORPUS = os.path.join(fx.HERE, "expected-ids.json")


class Corpus(unittest.TestCase):
    def test_every_row_recomputes(self):
        rows = json.loads(_read(CORPUS))
        self.assertGreaterEqual(len(rows), 10)
        for r in rows:
            got = fi.finding_id(r["lens"], r["flow"], r["locator"], r["title"])
            self.assertEqual(got, r["id"],
                             f"ID changed for {r['lens']}/{r['title'][:40]!r} — "
                             f"this is a schema migration, not a bug fix; see test docstring")

    def test_self_test_passes(self):
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(fi.self_test(), 0)


class Normalisation(unittest.TestCase):
    def test_negation_is_a_different_finding(self):
        a = fi.finding_id("trust", "V3", "/pricing", "Pricing is shown on the landing page")
        b = fi.finding_id("trust", "V3", "/pricing", "Pricing is not shown on the landing page")
        self.assertNotEqual(a, b)

    def test_locator_noise_is_stripped(self):
        self.assertEqual(fi.normalize_locator("https://staging.x.test/orders/8821/edit?sid=abc#top"),
                         "/orders/{n}/edit")
        self.assertEqual(fi.normalize_locator("/users/3f2a9c1e-1111-2222-3333-444444444444"),
                         "/users/{id}")


class LocatorInference(unittest.TestCase):
    """The gate infers a locator when the report omits the field. Changing
    this order re-IDs findings nobody edited (observed 2026-09-04)."""

    def test_first_slash_path_in_body_wins(self):
        loc = cr._infer_locator("`persona-p/screenshots/01.png`",
                                "- **Observed:**\n  - Looked at `/pricing` then `/about`.\n")
        self.assertEqual(loc, "/pricing")

    def test_falls_back_to_first_artifact(self):
        loc = cr._infer_locator("`persona-p/screenshots/01.png` · `session.log:4`", "no paths here")
        self.assertEqual(loc, "persona-p/screenshots/01.png")

    def test_mode_c_txt_evidence_is_an_artifact(self):
        loc = cr._infer_locator("`crawl/robots.txt`", "")
        self.assertEqual(loc, "crawl/robots.txt")

    def test_nothing_gives_empty(self):
        self.assertEqual(cr._infer_locator("the persona seemed confused", ""), "")


if __name__ == "__main__":
    unittest.main()
