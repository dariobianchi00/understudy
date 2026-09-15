#!/usr/bin/env python3
"""Phase 2a gate check.

Enforces the two gate conditions capture is responsible for (CLAUDE.md §10):

  Check 2 — naive/analyst separation held. No scoring vocabulary anywhere in
            the capture artifacts. A single hit means the traversal was
            contaminated and its evidence cannot be trusted: a persona who
            knows the framework produces observations shaped like findings,
            and the report then confirms its own priors.

  Check 5 — manifest complete. Both model levels recorded, persona mode
            recorded, the exclusions key present (an empty list is valid).

Plus the human-legibility condition: can someone open this folder and follow
what the persona did?

Exit 0 = gate passes. Exit 1 = it does not. There is no partial credit;
that is the point of a gate.

Usage:  check_capture.py <run_folder> [--quiet]
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_layout  # noqa: E402


def _read(*a, **k):
    with open(*a, **k) as fh:
        return fh.read()


# CLAUDE.md §6 invariant 1. The list lives in ONE place —
# references/banned-vocabulary.md — read by this script and quoted by the
# shape files. Observed 2026-09-11: the prose banned 19 terms and said
# "checked mechanically"; the script checked 14.
def _load_banned():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "references", "banned-vocabulary.md")
    terms = []
    for line in _read(path, errors="replace").splitlines():
        line = line.strip()
        if line.startswith("- "):
            terms.append(line[2:].split("  ")[0].strip().lower())
    if not terms:
        sys.exit("references/banned-vocabulary.md has no '- term' lines")
    return terms


BANNED = _load_banned()
# Whole-word matching: "p1" must not fire on "p1000", "hax" not on "haxby".
BANNED_RE = {b: re.compile(r"(?<![A-Za-z0-9])" + re.escape(b) + r"(?![A-Za-z0-9])", re.I)
             for b in BANNED if b != "ux"}
# "UX" only as a standalone token — the persona may write "ux" inside a URL.
BANNED_RE["ux"] = re.compile(r"(?<![A-Za-z0-9/._-])ux(?![A-Za-z0-9/._-])", re.I)
# A hit inside a URL-shaped token is a page the persona visited, not a word
# they chose: /plans/p1, /docs/cta-guide. Quoted page text is NOT exempt — a
# persona quoting "P1" is still a persona who has seen the framework.
_URLISH = re.compile(r"\S*(?:://|/)\S*")

# reading.md is Mode D's per-site persona reading (traversal-compare); it is
# first-person prose and carries the same contamination risk as a session log.
SCANNED = ("session.log", "persona-debrief.md", "findings-raw.json", "reading.md")
# Console and network dumps a capture is expected to leave beside the log —
# lens-bugs calls them its primary evidence.
DUMPS = ("console-full.txt", "network-full.txt")

REQUIRED_MANIFEST = [
    ("run_id", "run id"),
    ("target_slug", "target slug"),
    ("started_utc", "start timestamp"),
    ("persona_mode", "persona mode (generic vs supplied)"),
    ("models", "models block"),
]
# Must be PRESENT; an empty list is a valid answer ("nothing excluded").
REQUIRED_KEYS = [("scope_exclusions", "scope exclusions list (may be empty)")]


class Result:
    def __init__(self):
        self.failures, self.warnings, self.notes = [], [], []

    def fail(self, check, msg):
        self.failures.append((check, msg))

    def warn(self, msg):
        self.warnings.append(msg)

    def note(self, msg):
        self.notes.append(msg)


def _allowlist(run):
    """manifest.vocabulary_allowlist — terms waived for this run, e.g. a
    product whose own nav says "Usability". Every waiver is printed, so the
    gate output says what was not checked."""
    try:
        m = json.loads(_read(os.path.join(run, "manifest.json")))
        return {t.lower() for t in (m.get("vocabulary_allowlist") or []) if isinstance(t, str)}
    except (OSError, ValueError):
        return set()


def check_banned_vocabulary(run, r):
    """Check 2 — the separation held."""
    scanned = 0
    waived = _allowlist(run)
    if waived:
        r.warn(f"vocabulary allowlist in manifest — NOT checked: {', '.join(sorted(waived))}")
    for dirpath, _, filenames in os.walk(run):
        for fn in filenames:
            if fn not in SCANNED:
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, run)
            scanned += 1
            try:
                lines = _read(path, errors="replace").split("\n")
            except OSError as e:
                r.fail(2, f"{rel}: unreadable ({e})")
                continue
            for n, line in enumerate(lines, 1):
                scrubbed = _URLISH.sub(" ", line)
                for term, rx in BANNED_RE.items():
                    if term in waived:
                        continue
                    if rx.search(scrubbed):
                        r.fail(2, f"{rel}:{n} contains banned term '{term}'\n"
                                  f"        > {line.strip()[:100]}")
    if scanned == 0:
        # Modes B and C write no persona prose, and a crawler has no priors to
        # contaminate — the separation check is vacuously satisfied. Failing it
        # here would block a perfectly valid capture.
        if os.path.isdir(os.path.join(run, "crawl")) or \
                os.path.isdir(os.path.join(run, "measure")):
            r.note("separation check n/a — no-persona capture (crawl/measure), "
                   "nothing that could carry framework vocabulary")
            return
        if run_layout.compare_sites(run):
            # Mode D's mechanical capture records facts and no reactions, by
            # design (traversal-compare). The persona reading happens in the
            # per-site lens agents, whose output only check_report sees — so
            # the separation is enforced structurally, not by this scan. Say
            # so rather than fail a valid capture.
            r.note("separation check n/a — Mode D mechanical capture writes no "
                   "persona prose; independence is structural (one reader per site)")
            return
        r.fail(2, "no capture artifacts found to scan — "
                  "a traversal that wrote nothing has not been verified, it has been skipped")
    else:
        r.note(f"scanned {scanned} capture artifact(s) for scoring vocabulary")


def check_manifest(run, r):
    """Check 5 — the manifest is complete."""
    path = os.path.join(run, "manifest.json")
    if not os.path.exists(path):
        r.fail(5, "manifest.json missing — write it at run start, not at the end")
        return None
    try:
        m = json.loads(_read(path))
    except (OSError, json.JSONDecodeError) as e:
        r.fail(5, f"manifest.json unreadable: {e}")
        return None

    for key, label in REQUIRED_MANIFEST:
        if m.get(key) in (None, "", {}, []):
            r.fail(5, f"manifest missing {label} ('{key}')")
    for key, label in REQUIRED_KEYS:
        if key not in m:
            r.fail(5, f"manifest missing {label} ('{key}')")

    models = m.get("models") or {}
    if not models.get("traversal"):
        r.fail(5, "manifest records no traversal model — this is the one that changes "
                  "without anyone deciding it, so a run without it cannot be honestly diffed")
    if "scoring" not in models:
        r.fail(5, "manifest has no scoring model block")

    if m.get("persona_mode") == "generic":
        r.note("persona_mode=generic — the report MUST state on its face that "
               "findings rest on inferred personas")
    return m


def check_crawl(crawl_dir, r):
    """Mode C. The index is load-bearing: a lens that does not know a section
    was skipped will report its absence as a finding about the site."""
    index = os.path.join(crawl_dir, "index.json")
    if not os.path.exists(index):
        r.fail(0, "crawl/index.json missing — without it a lens cannot tell "
                  "'not crawled' from 'not present', and will report absences "
                  "that are artifacts of the crawl")
        return
    try:
        idx = json.loads(_read(index))
    except json.JSONDecodeError as e:
        r.fail(0, f"crawl/index.json is not valid JSON ({e})")
        return

    if not os.path.exists(os.path.join(crawl_dir, "site.json")):
        r.fail(0, "crawl/site.json missing — robots, sitemap and llms.txt are "
                  "site-level facts the seo and aeo lenses both depend on")

    pages_dir = os.path.join(crawl_dir, "pages")
    n_pages = len([f for f in os.listdir(pages_dir) if f.endswith(".json")]) \
        if os.path.isdir(pages_dir) else 0
    if n_pages == 0:
        r.fail(0, "crawl/pages/ has no page records — nothing was crawled")
    else:
        r.note(f"crawl: {n_pages} page record(s)")

    if isinstance(idx, dict) and "not_crawled" not in idx:
        r.warn("crawl/index.json has no 'not_crawled' list — a lens cannot "
               "distinguish a skipped section from a missing one")


def check_measure(measure_dir, r):
    """Mode B. A measurement whose viewport was not verified is not evidence —
    it looks authoritative and describes a page nobody saw."""
    files = [f for f in os.listdir(measure_dir) if f.endswith(".json")]
    if not files:
        r.fail(0, "measure/ has no measurement records — nothing was measured")
        return

    viewports = set()
    for f in sorted(files):
        path = os.path.join(measure_dir, f)
        try:
            d = json.loads(_read(path))
        except json.JSONDecodeError as e:
            r.fail(0, f"measure/{f} is not valid JSON ({e})")
            continue
        if not d.get("viewport_verified"):
            r.fail(0, f"measure/{f}: viewport_verified is not true — a "
                      f"device-specific measurement taken at the wrong viewport "
                      f"is worse than none, because it still looks authoritative")
        vp = d.get("viewport") or {}
        if vp.get("width"):
            viewports.add(vp["width"])
        if (d.get("tier1") or {}).get("lcp_ms") == 0:
            r.warn(f"measure/{f}: LCP is 0 — the observer was probably installed "
                   f"after the entry fired. Re-measure rather than report 0")

    if len(viewports) < 2:
        r.warn("measure: only one viewport measured — mobile and desktop must be "
               "measured and reported separately, or the flattering number hides "
               "the real one")
    r.note(f"measure: {len(files)} measurement record(s), {len(viewports)} viewport(s)")


def _is_empty_persona(pdir):
    shots = os.path.join(pdir, "screenshots")
    n = len(os.listdir(shots)) if os.path.isdir(shots) else 0
    return n == 0 and not os.path.exists(os.path.join(pdir, "session.log"))


def check_compare_sites(run, sites, r):
    """Mode D. Each compare/<site>/ is a capture in its own right: either
    persona-* folders (a visit traversal) or a mechanical capture — screenshots
    plus site.json, no session log by design (traversal-compare). Until
    2026-09-11 nothing looked here at all."""
    for site in sites:
        sdir = os.path.join(run, site)
        if not os.path.exists(os.path.join(sdir, "site.json")):
            r.fail(0, f"{site}: site.json missing — url, mode, when, and what was "
                      f"unreachable; the diff pass cannot tell a gap from a difference")
        personas = sorted(p for p in os.listdir(sdir)
                          if p.startswith("persona-") and os.path.isdir(os.path.join(sdir, p)))
        shots = os.path.join(sdir, "screenshots")
        n_shots = len([f for f in os.listdir(shots)
                       if f.lower().endswith((".png", ".jpg", ".jpeg"))]) if os.path.isdir(shots) else 0
        if personas:
            for p in personas:
                _check_persona(os.path.join(sdir, p), f"{site}/{p}", r)
        elif n_shots == 0:
            r.fail(0, f"{site}: no persona folder and no screenshots — nothing was captured")
        else:
            r.note(f"{site}: mechanical capture, {n_shots} screenshot(s)")
    if not os.path.exists(os.path.join(run, "compare", "index.json")):
        r.fail(0, "compare/index.json missing — the sites, and what could not be "
                  "reached on which, or the diff reports a coverage gap as a difference")


def _check_persona(pdir, d, r):
    """One persona folder — screenshots, a timestamped log, the four files."""
    shots = os.path.join(pdir, "screenshots")
    n_shots = len([f for f in os.listdir(shots)
                   if f.lower().endswith((".png", ".jpg", ".jpeg"))]) if os.path.isdir(shots) else 0

    log = os.path.join(pdir, "session.log")
    has_log = os.path.exists(log) and os.path.getsize(log) > 0

    if n_shots == 0:
        r.fail(0, f"{d}: no screenshots — evidence not on disk does not exist, "
                  f"and every finding it would have supported gets dropped")
    if not has_log:
        r.fail(0, f"{d}: session.log missing or empty — the journey cannot be followed")
    else:
        text = _read(log, errors="replace")
        if not re.search(r"\[\d{2}:\d{2}\]", text):
            r.fail(0, f"{d}: session.log has no [MM:SS] timestamps — "
                      f"a finding without a time cannot be placed in the journey")
        if "[pre-session]" not in text:
            r.warn(f"{d}: no [pre-session] entry expectation logged — "
                   f"the promise-vs-delivery question has nothing to compare against")

    for required in ("timeline.json", "persona-debrief.md", "findings-raw.json"):
        if not os.path.exists(os.path.join(pdir, required)):
            r.fail(0, f"{d}: {required} missing")
    for dump in DUMPS:
        if not os.path.exists(os.path.join(pdir, dump)):
            r.warn(f"{d}: {dump} missing — the bugs and trust lenses read it as "
                   f"primary evidence; a finding that needed it will be dropped")

    tl = os.path.join(pdir, "timeline.json")
    if os.path.exists(tl):
        try:
            json.loads(_read(tl))
        except json.JSONDecodeError as e:
            r.fail(0, f"{d}: timeline.json is not valid JSON ({e})")

    fr = os.path.join(pdir, "findings-raw.json")
    if os.path.exists(fr):
        try:
            raw = json.loads(_read(fr))
            if isinstance(raw, list) and not raw:
                r.warn(f"{d}: findings-raw.json is empty — a persona who "
                       f"reacted to nothing is unusual enough to check")
        except json.JSONDecodeError as e:
            r.fail(0, f"{d}: findings-raw.json is not valid JSON ({e})")

    r.note(f"{d}: {n_shots} screenshot(s)")



def check_human_legible(run, r, manifest):
    """The 2a gate's human condition: can someone follow what happened?"""
    persona_dirs = sorted(
        d for d in os.listdir(run)
        if d.startswith("persona-") and os.path.isdir(os.path.join(run, d))
    )
    crawl_dir   = os.path.join(run, "crawl")
    measure_dir = os.path.join(run, "measure")
    has_crawl   = os.path.isdir(crawl_dir)
    has_measure = os.path.isdir(measure_dir)
    sites       = run_layout.compare_sites(run)
    if sites:
        check_compare_sites(run, sites, r)

    # Modes B and C have no persona by design. Demanding a persona folder from
    # a crawl or a measurement fails a capture that is perfectly valid — so
    # check what the mode actually produces.
    if has_crawl:
        check_crawl(crawl_dir, r)
    if has_measure:
        check_measure(measure_dir, r)

    if not persona_dirs:
        if has_crawl or has_measure or sites:
            return          # a no-persona capture, already checked above
        r.fail(0, "no persona-* folders and no crawl/ or measure/ — nothing was captured")
        return

    declared = {f"persona-{p['name']}" for p in (manifest or {}).get("personas", [])
                if isinstance(p, dict) and p.get("name")}
    if declared and set(persona_dirs) != declared:
        missing = declared - set(persona_dirs)
        if missing:
            r.warn(f"manifest declares personas with no folder: {', '.join(sorted(missing))}")

    for d in persona_dirs:
        pdir = os.path.join(run, d)
        if sites and _is_empty_persona(pdir):
            # init_run creates root persona folders from the target file; a
            # Mode D mechanical capture writes under compare/<site>/ instead
            # and leaves them untouched. Empty is expected, not a failure.
            r.note(f"{d}: unused — Mode D captures live under compare/<site>/")
            continue
        _check_persona(pdir, d, r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_folder")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    run = os.path.expanduser(args.run_folder)
    if not os.path.isdir(run):
        sys.exit(f"not a directory: {run}")

    r = Result()
    manifest = check_manifest(run, r)
    check_banned_vocabulary(run, r)
    check_human_legible(run, r, manifest)

    if not args.quiet:
        for n in r.notes:
            print(f"  · {n}")
        for w in r.warnings:
            print(f"  ⚠ {w}")

    print()
    if r.failures:
        by_check = {}
        for check, msg in r.failures:
            by_check.setdefault(check, []).append(msg)
        labels = {0: "human-legible run folder",
                  2: "naive/analyst separation (gate check 2)",
                  5: "manifest complete (gate check 5)"}
        print(f"✗ PHASE 2a GATE FAILED — {len(r.failures)} problem(s)\n")
        for check in sorted(by_check):
            print(f"  {labels.get(check, check)}:")
            for msg in by_check[check]:
                print(f"    - {msg}")
            print()
        if 2 in by_check:
            print("  Check 2 is not a style nit. Scoring vocabulary in a capture artifact")
            print("  means the traversal saw the framework, and its evidence confirms its")
            print("  own priors. Re-run the traversal; do not edit the words out.")
        return 1

    print("✓ PHASE 2a GATE PASSED")
    print("  · separation held — no scoring vocabulary in capture artifacts")
    print("  · manifest complete — both model levels recorded")
    print("  · run folder is human-legible")
    return 0


if __name__ == "__main__":
    sys.exit(main())
