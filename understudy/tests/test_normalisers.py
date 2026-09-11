"""Title similarity — used by compare_runs to pair reworded findings across
runs and by render_report to spot the same finding raised by two lenses.

Two properties, both from §11.8: a rewording must pair (or --since reports
100% churn on an unchanged product); a genuinely different finding must NOT
pair (or a new problem hides inside an old one — the worse error).
"""
import sys
import unittest

import fixtures as fx

sys.path.insert(0, fx.SCRIPTS)
import compare_runs as cr    # noqa: E402
import render_report as rr   # noqa: E402

THRESHOLD = cr.TITLE_MATCH

MUST_PAIR = [
    ("No customer, quote, logo or number appears anywhere on the site",
     "No customer, quote, logo or number anywhere on the site"),
    ("Listener is never explained in the marketing",
     "Listener is never explained in marketing copy"),
    ("The fold names no audience",
     "The fold does not name an audience"),
]
MUST_NOT_PAIR = [
    ("Pricing is missing from the landing page",
     "Cookie banner does not match observed analytics behaviour"),
    ("Sitemap declared in robots.txt returns 404",
     "Canonical points off-site on the pricing page"),
]
# C4 — negation stripped by both stop lists, so these pair at 1.0 today.
NEGATION = [
    ("Pricing is shown on the landing page",
     "Pricing is not shown on the landing page"),
    ("The fold names an audience",
     "The fold never names an audience"),
]


class Similarity(unittest.TestCase):
    def test_rewordings_pair(self):
        for a, b in MUST_PAIR:
            for fn, name in ((cr._similar, "compare_runs"), (rr._similar, "render_report")):
                self.assertGreaterEqual(fn(a, b), THRESHOLD, (name, a, b))

    def test_different_findings_do_not_pair(self):
        for a, b in MUST_NOT_PAIR:
            for fn, name in ((cr._similar, "compare_runs"), (rr._similar, "render_report")):
                self.assertLess(fn(a, b), THRESHOLD, (name, a, b))

    @unittest.expectedFailure
    def test_negation_does_not_pair(self):
        for a, b in NEGATION:
            for fn, name in ((cr._similar, "compare_runs"), (rr._similar, "render_report")):
                self.assertLess(fn(a, b), THRESHOLD, (name, a, b))

    def test_both_scripts_agree(self):
        for a, b in MUST_PAIR + MUST_NOT_PAIR + NEGATION:
            self.assertAlmostEqual(cr._similar(a, b), rr._similar(a, b), places=6, msg=(a, b))

    def test_compare_runs_self_test(self):
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cr.self_test(), 0)


if __name__ == "__main__":
    unittest.main()
