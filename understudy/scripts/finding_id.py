#!/usr/bin/env python3
"""Stable finding IDs.

    id = sha256(lens + flow + normalized_locator + normalized_title)[:12]

Why this exists (CLAUDE.md §6): it enables
`understudy report --since <run-id>` to classify findings as
**new · persisting · resolved**. It CANNOT be retrofitted — findings written
without stable IDs can never be diffed against findings written with them.
Everything else about diffing is cheap whenever you want it. This part is not.

The whole value depends on the ID being stable across runs for what a human
would call "the same problem", and different for genuinely different problems.
Normalisation is where that is won or lost, so it is deliberately aggressive
about run-specific noise and deliberately conservative about meaning.

⚑ THE ID DEPENDS ON THE TOOLING, NOT ONLY ON THE FINDING.

When a report omits an explicit locator, `check_report.py` INFERS one — the
first `/path` in the body, else the first artifact its EVIDENCE_ARTIFACT regex
matches. So changing that regex, or the inference order, changes the inferred
locator, which changes the hash, which silently re-IDs findings that nobody
touched. Observed on 2026-09-04: widening the artifact extensions to accept
Mode-C `.html`/`.txt` evidence re-IDed one existing finding, because a `.txt`
citation that previously fell through now matched.

Two consequences, both load-bearing:

  1. **Treat a change to locator inference as a schema migration**, not a bug
     fix. Re-ID existing runs deliberately and say so; a `--since` diff across
     the change is otherwise pure noise dressed as findings.
  2. **Lenses should pass `--locator` explicitly.** An explicit locator is
     immune to inference changes. This is why the output contract calls the
     locator "the trap" and tells lenses to pass it rather than rely on
     inference.

Usage:
    finding_id.py --lens ux --flow shape_1 \\
                  --locator "/signup #workspace-type" \\
                  --title "Workspace type demanded before any value shown"
    finding_id.py --self-test
"""
import argparse
import hashlib
import re
import sys
import unicodedata

ID_LENGTH = 12

# Run-specific noise that must never change an ID.
_UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
_HEX = re.compile(r"\b[0-9a-f]{16,}\b", re.I)
_DIGITS = re.compile(r"\d+")
_SESSION_PARAM = re.compile(r"[?&](session|sid|token|ts|t|_|cb|v)=[^&#]*", re.I)
_FRAGMENT = re.compile(r"#.*$")
_SCHEME_HOST = re.compile(r"^[a-z]+://[^/]+", re.I)
_ALIAS = re.compile(r"[\w.+-]+@[\w.-]+")
_WS = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s/#.\[\]=-]")

# Words that carry no distinguishing meaning in a finding title. Dropping them
# keeps "The signup form is confusing" and "Signup form confusing" identical.
_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "of", "to", "in", "on", "at", "for", "with", "by", "from", "as",
    "that", "this", "these", "those", "it", "its", "and", "or", "but",
    "there", "here", "when", "then", "than", "so", "very", "just",
}


def normalize_locator(locator: str) -> str:
    """Where the problem lives — a path, a selector, a screen name.

    Strips scheme and host (staging vs prod is the same problem), query
    noise, fragments, and run-specific ids. Keeps path shape and any
    stable element hint.
    """
    if not locator:
        return ""
    s = locator.strip().lower()
    s = _SCHEME_HOST.sub("", s)
    s = _SESSION_PARAM.sub("", s)
    s = _FRAGMENT.sub("", s)
    s = _UUID.sub("{id}", s)
    s = _HEX.sub("{id}", s)
    s = _ALIAS.sub("{email}", s)
    # Numeric path segments are almost always record ids: /orders/8821 -> /orders/{n}
    s = re.sub(r"(?<=/)\d+(?=/|$)", "{n}", s)
    s = _DIGITS.sub("{n}", s)
    s = s.rstrip("/")
    s = _WS.sub(" ", s).strip()
    return s


def normalize_title(title: str) -> str:
    """What the problem is.

    Case, punctuation, stopwords and word order are all discarded — two
    analysts describing the same defect should collide. Numbers become {n}
    so "took 47 seconds" and "took 52 seconds" are one persisting finding
    rather than two.
    """
    if not title:
        return ""
    s = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    s = s.lower()
    s = _ALIAS.sub("", s)
    s = _DIGITS.sub("{n}", s)
    s = _PUNCT.sub(" ", s)
    words = [w for w in _WS.split(s) if w and w not in _STOPWORDS]
    # Sorted: word order should not create a new finding.
    return " ".join(sorted(words))


def finding_id(lens: str, flow: str, locator: str, title: str) -> str:
    parts = [
        (lens or "").strip().lower(),
        (flow or "").strip().lower(),
        normalize_locator(locator),
        normalize_title(title),
    ]
    digest = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()
    return digest[:ID_LENGTH]


# ---------------------------------------------------------------------------

_CASES = [
    # (should_match, a, b, why)
    (True,
     ("ux", "shape_1", "https://app.example.com/signup?session=abc123", "Workspace type demanded before any value is shown"),
     ("ux", "shape_1", "https://staging.example.com/signup", "workspace type demanded before any value shown"),
     "host, scheme and session param are run noise"),
    (True,
     ("ux", "shape_1", "/signup", "The signup form is confusing"),
     ("ux", "shape_1", "/signup/", "Signup form confusing"),
     "trailing slash, stopwords, case"),
    (True,
     ("onboarding", "shape_2", "/setup", "First value took 47 seconds"),
     ("onboarding", "shape_2", "/setup", "First value took 52 seconds"),
     "a timing change is the same finding persisting"),
    (True,
     ("ux", "shape_1", "/orders/8821/edit", "Cannot cancel"),
     ("ux", "shape_1", "/orders/1204/edit", "cannot cancel"),
     "record ids in a path are noise"),
    (True,
     ("ux", "shape_1", "/signup", "Confusing workspace picker"),
     ("ux", "shape_1", "/signup", "Workspace picker confusing"),
     "word order must not create a new finding"),
    (False,
     ("ux", "shape_1", "/signup", "Workspace type demanded before any value is shown"),
     ("bugs", "shape_1", "/signup", "Workspace type demanded before any value is shown"),
     "different lens is a different finding"),
    (False,
     ("ux", "shape_1", "/signup", "Workspace picker confusing"),
     ("ux", "shape_2", "/signup", "Workspace picker confusing"),
     "different flow is a different finding"),
    (False,
     ("ux", "shape_1", "/signup", "Workspace picker confusing"),
     ("ux", "shape_1", "/settings", "Workspace picker confusing"),
     "different location is a different finding"),
    (False,
     ("ux", "shape_1", "/signup", "Workspace picker confusing"),
     ("ux", "shape_1", "/signup", "Password rules not stated"),
     "different problem is a different finding"),
]


def self_test() -> int:
    failures = 0
    for should_match, a, b, why in _CASES:
        ida, idb = finding_id(*a), finding_id(*b)
        ok = (ida == idb) if should_match else (ida != idb)
        verb = "==" if should_match else "!="
        print(f"{'✓' if ok else '✗'} {ida} {verb} {idb}   {why}")
        if not ok:
            failures += 1
            print(f"    A: {a}\n    B: {b}")

    # Determinism: the same input must survive a process restart.
    fixed = finding_id("ux", "shape_1", "/signup", "Workspace picker confusing")
    expected = hashlib.sha256(
        "\x1f".join(["ux", "shape_1", "/signup", "confusing picker workspace"]).encode()
    ).hexdigest()[:ID_LENGTH]
    if fixed != expected:
        print(f"✗ determinism: {fixed} != {expected}")
        failures += 1
    else:
        print(f"✓ deterministic: {fixed}")

    print()
    print("PASS" if not failures else f"FAIL — {failures} case(s)")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lens")
    ap.add_argument("--flow")
    ap.add_argument("--locator")
    ap.add_argument("--title")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not (a.lens and a.title):
        ap.error("--lens and --title are required (or use --self-test)")
    print(finding_id(a.lens, a.flow or "", a.locator or "", a.title))
    return 0


if __name__ == "__main__":
    sys.exit(main())
