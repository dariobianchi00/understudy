#!/usr/bin/env python3
"""Phase 2b gate check.

Enforces the four gate conditions scoring is responsible for (CLAUDE.md §10):

  Check 1 — evidence rule holds. Every finding cites a screenshot, log line,
            console message, or DOM excerpt. Zero exceptions.
  Check 3 — cited artifacts exist. Every artifact a finding cites is on disk
            and can be opened, whatever the severity; a P0 must cite at least
            one.
  Check 4 — stable IDs present and correct. Every finding carries an id, and
            recomputing it from the finding's own fields reproduces it. This
            is deterministic: it tests the ID function, not the model.
  Check 6 — the report leads with a verdict. First non-heading block is a
            single sentence; a top-3 appears above any detailed findings.
            Applies to LENS summaries only. The run-level summary opens with a
            description of the thing assessed and carries its verdict in the
            Top 5 — see commands/run.md §3.6.
  Check 7 — a lens's self-assigned score is not contradicted by its own
            severities. The lens that read the evidence picks the 0-10; this
            refuses the combinations that cannot both be true.

Checks 2 and 5 belong to capture — see check_capture.py.

Exit 0 = gate passes. Exit 1 = it does not.

Usage:  check_report.py <run_folder> [--lens <name>]
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from finding_id import finding_id, FINDING_HEADING  # noqa: E402
import run_layout  # noqa: E402

SEVERITY = re.compile(r"\*\*Severity:\*\*\s*(P[0-3])", re.I)
TAG_FIELD = re.compile(r"^\s*-\s*\*\*(?P<key>[A-Za-z ][A-Za-z ]*?):\*\*\s*(?P<val>.*)$")
# The finding heading. ONE regex, shared with the renderer and the differ —
# see finding_id.FINDING_HEADING for why three copies were a gate bypass.
FINDING_H = FINDING_HEADING
# Extensions a capture can legitimately produce. Mode C writes raw .html and
# .txt/.xml (robots, sitemap, llms), Mode B writes .json, Mode A writes .png and
# .log — a gate that rejects any of them rejects valid evidence, which pushes
# lenses toward citing nothing rather than citing the file they actually read.
EVIDENCE_ARTIFACT = re.compile(
    r"(?P<path>[\w./-]+\.(?:png|jpe?g|webp|webm|zip|json|log|md|html?|txt|xml|csv|har))"
    r"(?::(?P<line>\d+))?"
)
CONSOLE_OR_DOM = re.compile(r"(console|network|status\s+\d{3}|<[a-z]+[\s>]|DOM)", re.I)


class Result:
    def __init__(self):
        self.failures = []
        self.notes = []

    def fail(self, check, msg):
        self.failures.append((check, msg))

    def note(self, m):
        self.notes.append(m)


def parse_findings(text):
    """Split findings-final.md into findings, stopping at the dropped list —
    dropped entries are explicitly NOT findings and must not be graded."""
    findings, current = [], None
    in_body = True
    for n, line in enumerate(text.split("\n"), 1):
        if re.match(r"^##\s+(Dropped for want of evidence|For other lenses|Appendices)", line, re.I):
            in_body = False
        elif re.match(r"^##\s+Findings", line, re.I):
            in_body = True
        if not in_body:
            continue
        m = FINDING_H.match(line)
        if m:
            current = {"id": m.group("id"), "title": m.group("title"),
                       "line": n, "fields": {}, "raw": []}
            findings.append(current)
            continue
        if current is not None:
            current["raw"].append(line)
            fm = TAG_FIELD.match(line)
            if fm:
                current["fields"][fm.group("key").strip().lower()] = fm.group("val").strip()
    return findings


def stray_headings(text):
    """`###` lines under Findings that did NOT parse as findings.

    A heading the parser cannot read is a finding the gate did not check —
    and until 2026-09-11 that printed as "no findings reported" and PASSED.
    """
    stray, in_body = [], True
    for n, line in enumerate(text.split("\n"), 1):
        if re.match(r"^##\s+(Dropped for want of evidence|For other lenses|Appendices)", line, re.I):
            in_body = False
        elif re.match(r"^##\s+Findings", line, re.I):
            in_body = True
        if in_body and line.startswith("### ") and not FINDING_H.match(line):
            stray.append((n, line.strip()))
    return stray


SCORE_FIELD = re.compile(r"^-\s+\*\*Score:\*\*\s*(\d{1,2})\s*/\s*10\s*[—–-]?\s*(.*?)\s*$",
                         re.M)

# The ceiling a lens may claim while carrying a finding of each severity.
# Deliberately loose: it catches a score that cannot be defended, not one it
# merely disagrees with. Scoring is a judgement (§11.8) and the gate is not
# here to relitigate it — only to stop "9/10" sitting above a P0.
SCORE_CEILING = {"P0": 5, "P1": 7, "P2": 9}


def check_score(path, findings_path, r, lens):
    """Check 7 — the score and the severities must be able to coexist."""
    if not os.path.exists(path):
        return
    findings = (parse_findings(open(findings_path, errors="replace").read())
                if os.path.exists(findings_path) else [])
    text = open(path, errors="replace").read()
    m = SCORE_FIELD.search(text)
    if not m:
        r.note(f"{lens}: no '- **Score:** N/10 — why' line; "
               f"the run report will omit this check from its score table")
        return
    score, why = int(m.group(1)), m.group(2).strip()
    if not 0 <= score <= 10:
        r.fail(7, f"{lens}: score {score} is outside 0-10")
        return
    if len(why) < 15:
        r.fail(7, f"{lens}: score {score}/10 has no reason. "
                  f"'Why that score' is a column a client reads.")
    worst = None
    for sev in ("P0", "P1", "P2"):
        if any(f["fields"].get("severity", "").upper().startswith(sev) for f in findings):
            worst = sev
            break
    if worst and score > SCORE_CEILING[worst]:
        r.fail(7, f"{lens}: scored {score}/10 while carrying a {worst}. "
                  f"A lens with a {worst} cannot score above "
                  f"{SCORE_CEILING[worst]}/10.")


def check_verdict(path, r, lens):
    """Check 6 — verdict first, then a top 3."""
    if not os.path.exists(path):
        r.fail(6, f"{lens}: exec-summary.md missing")
        return
    lines = open(path, errors="replace").read().split("\n")

    first_block, idx = [], None
    for i, line in enumerate(lines):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        idx = i
        break
    if idx is None:
        r.fail(6, f"{lens}: exec-summary.md has no content below the heading")
        return
    for line in lines[idx:]:
        if not line.strip():
            break
        first_block.append(line.strip())
    verdict = " ".join(first_block).strip()

    if verdict.startswith(("-", "*", "|", "1.")):
        r.fail(6, f"{lens}: exec-summary opens with a list, not a verdict sentence. "
                  f"The one-sentence verdict is the only thing standing between the "
                  f"reader and an unread report.")
        return

    # One sentence: at most one terminal punctuation mark, not counting
    # abbreviations or decimals.
    body = re.sub(r"\b\w\.\w\.", "", verdict)
    body = re.sub(r"\d\.\d", "", body)
    terminals = len(re.findall(r"[.!?](?:\s|$)", body))
    if terminals > 1:
        r.fail(6, f"{lens}: verdict is {terminals} sentences, not one.\n"
                  f"        > {verdict[:160]}")
    elif terminals == 0 and len(verdict) > 0:
        r.note(f"{lens}: verdict has no terminal punctuation — check it reads as a sentence")

    if len(verdict) > 400:
        r.fail(6, f"{lens}: verdict is {len(verdict)} characters. If it cannot be said "
                  f"shortly, the analysis is not finished.")

    text = "\n".join(lines)
    top3_at = text.lower().find("## top 3")
    if top3_at == -1:
        r.fail(6, f"{lens}: exec-summary has no '## Top 3' section")
    else:
        for marker in ("## findings", "### "):
            at = text.lower().find(marker)
            if at != -1 and at < top3_at:
                r.fail(6, f"{lens}: detailed findings appear above the top 3")
                break


def check_findings(path, r, lens, run):
    if not os.path.exists(path):
        r.fail(1, f"{lens}: findings-final.md missing")
        return
    text = open(path, errors="replace").read()
    findings = parse_findings(text)
    for n, line in stray_headings(text):
        r.fail(1, f"{lens}:{n} heading did not parse as a finding, so nothing "
                  f"below it was checked. The format is `### <id> — <title>`.\n"
                  f"        > {line[:100]}")
    if not findings:
        r.note(f"{lens}: no findings reported")
        return

    seen = {}
    for f in findings:
        fid, title, ln = f["id"], f["title"], f["line"]
        fields = f["fields"]
        body = "\n".join(f["raw"])

        # ---- Check 1: evidence -----------------------------------------
        ev = fields.get("evidence", "")
        artifacts = list(EVIDENCE_ARTIFACT.finditer(ev))
        if not ev:
            r.fail(1, f"{lens}:{ln} finding '{title[:60]}' has no Evidence field")
        elif not artifacts and not CONSOLE_OR_DOM.search(ev):
            r.fail(1, f"{lens}:{ln} finding '{title[:60]}' cites no artifact\n"
                      f"        Evidence: {ev[:100]}")

        # ---- Check 3: cited artifacts exist on disk ----------------------
        # Every severity. "The file you cite is really there" is the cheapest
        # anti-confabulation check the harness has; until 2026-09-11 it
        # covered only P0, the smallest class.
        sev_m = SEVERITY.search(body)
        sev = sev_m.group(1).upper() if sev_m else None
        if not sev:
            r.fail(1, f"{lens}:{ln} finding '{title[:60]}' has no Severity field")
        elif artifacts or sev == "P0":
            resolved = False
            for m in artifacts:
                if _artifact_exists(run, lens, m.group("path")):
                    resolved = True
                    break
            if not resolved:
                if artifacts:
                    missing = ", ".join(m.group("path") for m in artifacts)
                    r.fail(3, f"{lens}:{ln} {sev} '{title[:60]}' cites artifact(s) that do "
                              f"not exist on disk: {missing}")
                else:
                    r.fail(3, f"{lens}:{ln} P0 '{title[:60]}' cites no openable artifact. "
                              f"A P0 a reader cannot verify is the most expensive kind of "
                              f"wrong finding.")

        # ---- Check 4: stable IDs ---------------------------------------
        if fid in seen:
            r.fail(4, f"{lens}:{ln} duplicate finding id {fid} "
                      f"(also at line {seen[fid]})")
        seen[fid] = ln

        flow = fields.get("flow", "")
        locator = fields.get("locator") or _infer_locator(ev, body)
        base = re.sub(r"-[a-z]$", "", fid)  # persona variants: <id>-a, <id>-b
        # The ID hashes the lens NAME (`clarity`), never its folder. A Mode D
        # per-site lens lives at compare/<site>/clarity and still hashes as
        # `clarity` — that is what its agent was told and what it passed to
        # finding_id.py.
        lens_name = lens.rpartition("/")[2]
        expect = finding_id(lens_name, flow, locator, title)
        if not re.fullmatch(r"[0-9a-f]{6,16}", base):
            r.fail(4, f"{lens}:{ln} id '{fid}' is not a hash — sequence numbers "
                      f"cannot be diffed across runs")
        elif expect[:len(base)] != base:
            r.fail(4, f"{lens}:{ln} id {fid} does not match recomputation.\n"
                      f"        expected {expect} from lens='{lens_name}' flow='{flow}' "
                      f"locator='{locator}' title='{title[:50]}'")

    # Count by the Severity FIELD, not the substring — a finding that quotes a
    # page's own "P0" label was being counted as a P0 (found dogfooding, 2026-09-12).
    r.note(f"{lens}: {len(findings)} finding(s), "
           f"{sum(1 for f in findings if f['fields'].get('severity', '').upper().startswith('P0'))} P0")


def _artifact_exists(run, lens, path):
    """A citation is relative to the run root — or, as the contract's own
    example `session.log:NN` shows, to the persona folder it came from. Try
    the root, the lens folder, then any capture folder in the run."""
    if os.path.exists(os.path.join(run, path)):
        return True
    if os.path.exists(os.path.join(run, lens, path)):
        return True
    import glob
    return bool(glob.glob(os.path.join(run, "**", path), recursive=True))


def _infer_locator(evidence, body):
    m = re.search(r"`(/[^`\s]*)`", body)
    if m:
        return m.group(1)
    m = EVIDENCE_ARTIFACT.search(evidence)
    return m.group("path") if m else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_folder")
    ap.add_argument("--lens", default=None, help="check only this lens")
    ap.add_argument("--expect-lenses", type=int, default=None,
                    help="how many lens reports the orchestrator dispatched; "
                         "fewer on disk fails the gate")
    a = ap.parse_args()

    run = os.path.expanduser(a.run_folder)
    if not os.path.isdir(run):
        sys.exit(f"not a directory: {run}")

    # Discovery is shared with the renderer, so a Mode D run's per-site lenses
    # under compare/<site>/ are checked here exactly where the export will
    # show them. Until 2026-09-11 this listed one level deep and a compare run
    # passed with three of its four reports never opened.
    lenses = run_layout.lens_dirs(run)
    if a.lens:
        lenses = [l for l in lenses if l == a.lens or l.endswith("/" + a.lens)]
    if not lenses:
        sys.exit("no lens output found — expected <run>/<lens>/findings-final.md")

    r = Result()
    if a.expect_lenses is not None and len(lenses) < a.expect_lenses:
        r.fail(8, f"{len(lenses)} lens report(s) on disk, {a.expect_lenses} "
                  f"dispatched: {', '.join(lenses)}. A lens whose files never "
                  f"landed is not failed by the checks below — it is not "
                  f"checked. Persist the missing output before re-running.")
    for lens in lenses:
        d = os.path.join(run, lens)
        check_verdict(os.path.join(d, "exec-summary.md"), r, lens)
        check_findings(os.path.join(d, "findings-final.md"), r, lens, run)
        check_score(os.path.join(d, "exec-summary.md"),
                    os.path.join(d, "findings-final.md"), r, lens)

    # A note, never a failure: the run is sound, its record of itself is not.
    # Warning here is what stops the close step being forgotten — the gate is
    # the last thing that runs, and it is the thing nobody skips.
    try:
        mf = json.load(open(os.path.join(run, "manifest.json")))
        if mf.get("phase") != "complete" or not mf.get("finished_utc"):
            r.note("manifest still open (phase "
                   f"'{mf.get('phase')}', finished_utc {mf.get('finished_utc')}) — "
                   "run scripts/close_run.py <run_folder> to record what was "
                   "captured and when it finished")
    except Exception:
        pass

    for n in r.notes:
        print(f"  · {n}")
    print()

    if r.failures:
        labels = {1: "evidence rule (gate check 1)",
                  3: "zero unsupported P0s (gate check 3)",
                  4: "stable finding IDs (gate check 4)",
                  6: "report leads with a verdict (gate check 6)",
                  7: "score consistent with severities (gate check 7)",
                  8: "every dispatched lens landed (--expect-lenses)"}
        by = {}
        for c, m in r.failures:
            by.setdefault(c, []).append(m)
        print(f"✗ PHASE 2b GATE FAILED — {len(r.failures)} problem(s)\n")
        for c in sorted(by):
            print(f"  {labels[c]}:")
            for m in by[c]:
                print(f"    - {m}")
            print()
        return 1

    print("✓ PHASE 2b GATE PASSED")
    for c, label in [(1, "every finding cites evidence"),
                     (3, "every P0 traces to an artifact on disk"),
                     (4, "stable IDs present and reproducible"),
                     (6, "report leads with a one-sentence verdict")]:
        print(f"  · {label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
