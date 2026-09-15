"""Synthetic run folders for the plumbing tests.

Built in a temp directory at test time rather than committed, because the
repo's .gitignore refuses every capture artifact by name — *.png,
session.log, timeline.json, findings-raw.json — and it must keep doing so
(CLAUDE.md §7). A fixture that has to fight the gitignore is a fixture that
will one day be committed with a real screenshot in it.

Every fixture describes a FICTIONAL product. If a real product name would
make a test clearer, the test is wrong.
"""
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.normpath(os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, SCRIPTS)
from finding_id import finding_id  # noqa: E402

# A valid 1x1 transparent PNG — the smallest file that is really an image.
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")

PRODUCT = "Nimbus Notes"


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def write_png(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(PNG)


def manifest(run, **over):
    m = {
        "run_id": "t0000001", "target_slug": "nimbus-notes", "product_name": PRODUCT,
        "base_url": "https://example-nimbus-notes.test",
        "started_utc": "2026-09-01T09:00:00+00:00", "finished_utc": None,
        "models": {"traversal": "model-a", "scoring": {"clarity": "model-b"}},
        "assessment_type": "website", "coverage_depth": "standard",
        "conversion_goal": "Start a free trial", "competitors": [],
        "persona_mode": "generic",
        "personas": [{"name": "p", "device": "desktop-1440x900"}],
        "objectives": ["clarity"], "scope_exclusions": [],
        "time_cap_minutes": 25, "understudy_version": "0.0.0",
        "phase": "2a-capture", "captures": {},
    }
    m.update(over)
    write(os.path.join(run, "manifest.json"), json.dumps(m, indent=1))
    return m


def persona(run, name="p", base=None, log=None, shots=("01-landing.png",)):
    """A complete, clean persona capture."""
    pdir = os.path.join(base or run, f"persona-{name}")
    os.makedirs(os.path.join(pdir, "screenshots"), exist_ok=True)
    for s in shots:
        with open(os.path.join(pdir, "screenshots", s), "wb") as f:
            f.write(PNG)
    write(os.path.join(pdir, "session.log"), log or
          "[pre-session] Arrived via: search\n"
          "[pre-session] What I was told: \"notes that remember\"\n"
          "[00:00] I land on the page. Big headline, a photo of a cloud.\n"
          "[00:12] I can't tell what this is for. Is it for teams?\n"
          "[01:40] Looking for a price. Nothing in the nav.\n")
    write(os.path.join(pdir, "timeline.json"), json.dumps(
        {"shape_v1": {"time_to_comprehension_seconds": None}}))
    write(os.path.join(pdir, "persona-debrief.md"),
          "# Debrief\n\nQ1 — I think it's some kind of notes app, but I'm guessing.\n")
    write(os.path.join(pdir, "findings-raw.json"), json.dumps(
        [{"t": "00:12", "screen": "01-landing.png", "flow": "V1",
          "reaction": "I can't tell what this is for."}]))
    return pdir


def finding(lens, title, sev="P1", flow="V1", locator="/", evidence=None,
            fid=None, fix="Say who it is for in the headline", extra=""):
    ev = evidence or "`persona-p/screenshots/01-landing.png` · `persona-p/session.log:3`"
    fid = fid or finding_id(lens, flow, locator, title)
    return (f"### {fid} — {title}\n"
            f"- **Severity:** {sev}\n"
            f"- **So what:** She could not say what it was for.\n"
            f"- **Flow:** {flow}\n"
            f"- **Locator:** {locator}\n"
            f"- **Personas hit:** p\n"
            f"- **Observed:**\n  - The fold names no audience.\n"
            f"- **Evidence:** {ev}\n"
            f"- **Fix:** {fix}\n{extra}\n")


def lens(run, name, findings, score=4, verdict="A visitor cannot say who this is for.",
         top3="1. **[P1] The fold names no audience** — she guessed (p)\n",
         base=None, score_line=None, matrix=None):
    """A lens's two files, in the contract's shape."""
    d = os.path.join(base or run, name)
    tail = name.rpartition("/")[2]
    sl = score_line if score_line is not None else \
        f"- **Score:** {score}/10 — the fold names no audience and no price is shown\n"
    write(os.path.join(d, "exec-summary.md"),
          f"# {PRODUCT} — {tail} — Run 2026-09-01 (t0000001)\n\n{verdict}\n\n"
          f"## Top 3\n{top3}\n## Score\n{sl}\n"
          + (f"## Differences matrix\n{matrix}\n" if matrix else "")
          + "## Limits on this read\n- **Personas:** p — ⚠ INFERRED (generic)\n")
    write(os.path.join(d, "findings-final.md"),
          f"# {PRODUCT} — {tail} findings — Run 2026-09-01 (t0000001)\n\n## Method\n"
          f"- Framework: test\n\n---\n\n## Findings\n\n" + "\n".join(findings)
          + "\n---\n\n## Dropped for want of evidence\n- none\n")
    return d


def run_summary(run, product=PRODUCT):
    write(os.path.join(run, "exec-summary.md"),
          f"# {product} — Website assessment — 1 September 2026\n\n"
          "## What this is\n- A fictional notes product used only in tests.\n\n"
          "## How it was produced\n- One simulated visitor, 25 minutes, desktop.\n\n"
          "## Contents\n\n"
          "## Top 5 — fix these first\nThe site never says who it is for.\n\n"
          "| # | Severity | What is happening | What it costs | Effort |\n|---|---|---|---|---|\n"
          "| 1 | P1 | The fold names no audience | She guessed | Copy change |\n\n"
          "## What each check looked for\n| Check | Question it answers |\n|---|---|\n"
          "| **Clarity** | Can a visitor say what this is? |\n\n"
          "## How each area scores\n\n"
          "## Raised by more than one check\n\n"
          "## Limits of this assessment\n- Personas were constructed, not researched.\n")


def clean_run(tmp, with_lens=True):
    """A run that passes both gates."""
    run = os.path.join(tmp, "2026-09-01-run-t0000001")
    manifest(run)
    persona(run)
    if with_lens:
        lens(run, "clarity", [finding("clarity", "The fold names no audience")])
    return run
