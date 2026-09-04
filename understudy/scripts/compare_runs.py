#!/usr/bin/env python3
"""Diff two runs of the same target by stable finding ID.

    compare_runs.py <old_run> <new_run> [--lens <name>] [--json] [--self-test]

Classifies every finding as **new · persisting · resolved** and reports the
overlap percentage — the number that tells you how much this harness disagrees
with itself.

Why by ID and not by title: findings get reworded between runs. Matching on text
silently drops anything a model phrased differently, which inflates both "new"
and "resolved" and makes the diff look busier than reality. The ID is a pure
function of (lens, flow, normalised locator, normalised title) precisely so a
rewording does not create a false "new".

⚑ Two comparisons this tool refuses to present silently:

  - **A model change.** Findings are not comparable across models. A "resolved"
    finding may just be a weaker model that failed to notice it.
  - **A persona-mode change.** A `generic` run diffed against a `supplied` run is
    comparing two different questions.

Both are printed above the diff, not below it, and `--json` carries them as
`warnings` so a caller cannot drop them by accident.
"""
import argparse
import json
import os
import re
import sys

FINDING_H3 = re.compile(r"^###\s+`?([0-9a-f]{6,16}(?:-[a-z])?)`?\s*[—-]\s*(.+?)\s*$")
SEVERITY = re.compile(r"^-\s+\*\*Severity:\*\*\s*(P[0-3])", re.M)
DROPPED = re.compile(r"^##\s+Dropped for want of evidence", re.M)


def load_run(run):
    """Every finding in a run, keyed by id. Findings below the 'Dropped for want
    of evidence' heading are excluded — they are explicitly not findings, and
    counting them would make a run look like it regressed when it got honest."""
    run = os.path.expanduser(run.rstrip("/"))
    if not os.path.isdir(run):
        sys.exit(f"not a directory: {run}")

    manifest = {}
    mpath = os.path.join(run, "manifest.json")
    if os.path.exists(mpath):
        try:
            manifest = json.load(open(mpath))
        except (OSError, ValueError):
            pass

    findings = {}
    for lens in sorted(os.listdir(run)):
        fpath = os.path.join(run, lens, "findings-final.md")
        if not os.path.isfile(fpath):
            continue
        text = open(fpath, errors="replace").read()
        cut = DROPPED.search(text)
        if cut:
            text = text[:cut.start()]
        lines = text.split("\n")
        for n, line in enumerate(lines):
            m = FINDING_H3.match(line)
            if not m:
                continue
            block = "\n".join(lines[n + 1:n + 16])
            sev = SEVERITY.search(block)
            findings[m.group(1)] = {
                "id": m.group(1),
                "lens": lens,
                "title": m.group(2),
                "severity": sev.group(1) if sev else "—",
            }
    return {"path": run, "manifest": manifest, "findings": findings}


def comparability_warnings(old, new):
    """Everything that makes a diff dishonest if presented without comment."""
    w = []
    om, nm = old["manifest"], new["manifest"]

    if om.get("target_slug") and nm.get("target_slug") and \
            om["target_slug"] != nm["target_slug"]:
        w.append(f"DIFFERENT TARGETS: '{om['target_slug']}' vs '{nm['target_slug']}' "
                 f"— this is not a diff of the same product.")

    ot = (om.get("models") or {}).get("traversal")
    nt = (nm.get("models") or {}).get("traversal")
    if ot and nt and ot != nt:
        w.append(f"TRAVERSAL MODEL CHANGED: {ot} → {nt}. Findings are not "
                 f"comparable across models; a 'resolved' finding may be a model "
                 f"that failed to notice it.")

    os_, ns = (om.get("models") or {}).get("scoring") or {}, \
              (nm.get("models") or {}).get("scoring") or {}
    changed = [f"{k}: {os_.get(k)} → {ns.get(k)}"
               for k in sorted(set(os_) | set(ns)) if os_.get(k) != ns.get(k)]
    if changed:
        w.append("SCORING MODEL CHANGED — " + "; ".join(changed))

    if om.get("persona_mode") and nm.get("persona_mode") and \
            om["persona_mode"] != nm["persona_mode"]:
        w.append(f"PERSONA MODE CHANGED: {om['persona_mode']} → {nm['persona_mode']}. "
                 f"A generic run and a supplied run answer different questions.")

    oc, nc = om.get("coverage_depth"), nm.get("coverage_depth")
    if oc and nc and oc != nc:
        w.append(f"COVERAGE DEPTH CHANGED: {oc} → {nc}. A deeper run finds more "
                 f"because it looked at more, not because the product got worse.")

    ol = {f["lens"] for f in old["findings"].values()}
    nl = {f["lens"] for f in new["findings"].values()}
    if ol != nl:
        only_old, only_new = sorted(ol - nl), sorted(nl - ol)
        bits = []
        if only_old:
            bits.append(f"only in old: {', '.join(only_old)}")
        if only_new:
            bits.append(f"only in new: {', '.join(only_new)}")
        w.append("LENS SET CHANGED — " + "; ".join(bits) +
                 ". A lens that did not run cannot resolve anything.")
    return w


def diff(old, new, lens=None):
    of, nf = old["findings"], new["findings"]
    if lens:
        of = {k: v for k, v in of.items() if v["lens"] == lens}
        nf = {k: v for k, v in nf.items() if v["lens"] == lens}

    persisting = sorted(set(of) & set(nf))
    resolved   = sorted(set(of) - set(nf))
    added      = sorted(set(nf) - set(of))

    union = len(set(of) | set(nf))
    overlap = (len(persisting) / union * 100) if union else 100.0

    return {
        "new":        [nf[i] for i in added],
        "persisting": [nf[i] for i in persisting],
        "resolved":   [of[i] for i in resolved],
        "counts": {"new": len(added), "persisting": len(persisting),
                   "resolved": len(resolved),
                   "old_total": len(of), "new_total": len(nf)},
        "overlap_pct": round(overlap, 1),
    }


def render(old, new, d, warnings):
    out = []
    o, n = os.path.basename(old["path"]), os.path.basename(new["path"])
    out.append(f"understudy diff — {o}  →  {n}\n")

    if warnings:
        out.append("⚠ COMPARABILITY — read before the numbers")
        for w in warnings:
            out.append(f"  · {w}")
        out.append("")

    c = d["counts"]
    out.append(f"  new         {c['new']:>3}")
    out.append(f"  persisting  {c['persisting']:>3}")
    out.append(f"  resolved    {c['resolved']:>3}")
    out.append(f"  overlap     {d['overlap_pct']}%   "
               f"({c['old_total']} findings → {c['new_total']})")
    out.append("")

    for label, key in (("NEW", "new"), ("RESOLVED", "resolved"),
                       ("PERSISTING", "persisting")):
        if not d[key]:
            continue
        out.append(f"{label}")
        for f in sorted(d[key], key=lambda x: (x["severity"], x["lens"])):
            out.append(f"  {f['severity']:<3} {f['lens']:<12} {f['id']}  {f['title']}")
        out.append("")

    if d["counts"]["resolved"] and warnings:
        out.append("Note: 'resolved' means the finding is absent from the new run. "
                   "With the warnings above, absence may not mean fixed.")
    return "\n".join(out)


# ------------------------------------------------------------------ tests ----
def self_test():
    """Exercises the classification and the overlap arithmetic on synthetic
    data — no run folders needed, so this stays runnable in CI."""
    def mk(ids):
        return {"path": "/x", "manifest": {},
                "findings": {i: {"id": i, "lens": "ux", "title": f"t{i}",
                                 "severity": "P1"} for i in ids}}

    d = diff(mk(["a", "b", "c"]), mk(["b", "c", "d"]))
    assert d["counts"] == {"new": 1, "persisting": 2, "resolved": 1,
                           "old_total": 3, "new_total": 3}, d["counts"]
    assert d["overlap_pct"] == 50.0, d["overlap_pct"]   # 2 shared of 4 union

    d = diff(mk(["a", "b"]), mk(["a", "b"]))
    assert d["overlap_pct"] == 100.0

    d = diff(mk([]), mk([]))
    assert d["overlap_pct"] == 100.0, "empty vs empty must not divide by zero"

    d = diff(mk(["a"]), mk(["b"]))
    assert d["overlap_pct"] == 0.0

    # a lens filter must not leak findings from other lenses
    two = {"path": "/x", "manifest": {}, "findings": {
        "a": {"id": "a", "lens": "ux", "title": "t", "severity": "P1"},
        "b": {"id": "b", "lens": "bugs", "title": "t", "severity": "P1"}}}
    d = diff(two, two, lens="ux")
    assert d["counts"]["persisting"] == 1 and d["counts"]["old_total"] == 1

    # warnings must fire on a model change
    o = {"path": "/x", "findings": {}, "manifest":
         {"models": {"traversal": "m1", "scoring": {}}, "persona_mode": "generic"}}
    n = {"path": "/y", "findings": {}, "manifest":
         {"models": {"traversal": "m2", "scoring": {}}, "persona_mode": "supplied"}}
    w = comparability_warnings(o, n)
    assert any("TRAVERSAL MODEL CHANGED" in x for x in w)
    assert any("PERSONA MODE CHANGED" in x for x in w)

    print("PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("old_run", nargs="?")
    ap.add_argument("new_run", nargs="?")
    ap.add_argument("--lens", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not a.old_run or not a.new_run:
        ap.error("need <old_run> and <new_run>, or --self-test")

    old, new = load_run(a.old_run), load_run(a.new_run)
    if not old["findings"] and not new["findings"]:
        sys.exit("no findings in either run — is <lens>/findings-final.md present?")

    warnings = comparability_warnings(old, new)
    d = diff(old, new, a.lens)

    if a.json:
        print(json.dumps({"old": old["path"], "new": new["path"],
                          "warnings": warnings, **d}, indent=2))
    else:
        print(render(old, new, d, warnings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
