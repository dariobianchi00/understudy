#!/usr/bin/env python3
"""Close out a run's manifest — what was captured, when it finished, what phase.

    close_run.py <run_folder> [--phase 2b-scoring|complete]

`init_run.py` writes the manifest at run start with `phase: "2a-capture"`,
`finished_utc: null` and `captures: {}` — deliberately, because a manifest
assembled from memory at the end records what someone remembers rather than
what ran. Nothing ever filled the other three in, so every run on disk claimed
it never got past capture. Observed 2026-09-05 across four completed runs.

This is the missing half, and it keeps the same principle: **every field here is
read off the disk, never from the caller.** The counts are what is actually in
the run folder. A run that says it captured twelve screenshots captured twelve
screenshots.

Stdlib only, like every script here.
"""
import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone


def _count(pattern):
    return len(glob.glob(pattern))


def survey(run):
    """What this run actually produced, read off the disk."""
    caps = {}
    for d in sorted(os.listdir(run)):
        full = os.path.join(run, d)
        if not os.path.isdir(full):
            continue

        if d.startswith("persona-") or d.startswith("competitor-"):
            entry = {"screenshots": _count(os.path.join(full, "screenshots", "*.png"))}
            for name in ("session.log", "timeline.json", "debrief.md"):
                if os.path.exists(os.path.join(full, name)):
                    entry[name.split(".")[0]] = True
            caps[d] = entry

        elif d == "crawl":
            # The crawl skill has written its fetched pages under both
            # `pages/` and `html/` across runs, and index.json is the record
            # of record — count all three rather than trust one convention.
            n = _count(os.path.join(full, "pages", "*")) + \
                _count(os.path.join(full, "html", "*"))
            if not n:
                try:
                    idx = json.load(open(os.path.join(full, "index.json")))
                    n = len(idx.get("pages") or idx.get("crawled") or [])
                except Exception:
                    n = 0
            caps["crawl"] = {"pages": n}

        elif d == "measure":
            caps["measure"] = {"profiles": _count(os.path.join(full, "*.json"))}

    return caps


def last_activity(run):
    """When this run last wrote something — read off the disk, like everything
    else here. Wall-clock would stamp a run closed months later with today."""
    newest = 0.0
    for root, dirs, files in os.walk(run):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in files:
            # Exports are derived, and re-rendering one months later must not
            # move the date the run finished. Only evidence and findings count.
            if root == run and (f == "manifest.json" or f.startswith("report-")
                                or f.endswith((".pdf", ".html"))):
                continue
            try:
                newest = max(newest, os.path.getmtime(os.path.join(root, f)))
            except OSError:
                pass
    if not newest:
        return datetime.now(timezone.utc).isoformat(timespec="seconds")
    return datetime.fromtimestamp(newest, timezone.utc).isoformat(timespec="seconds")


def scored(run):
    """Lenses that produced a findings file, and how many findings each holds."""
    out = {}
    for d in sorted(os.listdir(run)):
        f = os.path.join(run, d, "findings-final.md")
        if os.path.exists(f):
            text = open(f, errors="replace").read()
            out[d] = sum(1 for ln in text.split("\n") if ln.startswith("### "))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_folder")
    ap.add_argument("--phase", default="complete",
                    choices=["2a-capture", "2b-scoring", "complete"])
    ap.add_argument("--reopen", action="store_true",
                    help="clear finished_utc — for a run being added to")
    a = ap.parse_args()

    run = os.path.expanduser(a.run_folder.rstrip("/"))
    path = os.path.join(run, "manifest.json")
    if not os.path.exists(path):
        sys.exit(f"no manifest.json in {run} — init_run.py writes it at run start")

    m = json.load(open(path))
    m["captures"] = survey(run)
    m["findings"] = scored(run)
    m["phase"] = a.phase

    # finished_utc is stamped once, when the run first completes. A re-score
    # that adds a lens does not change when the run happened.
    if a.reopen:
        m["finished_utc"] = None
    elif a.phase == "complete" and not m.get("finished_utc"):
        m["finished_utc"] = last_activity(run)

    with open(path, "w") as f:
        json.dump(m, f, indent=2)

    caps = ", ".join(f"{k} ({v.get('screenshots', v.get('pages', v.get('profiles', 0)))})"
                     for k, v in m["captures"].items()) or "none"
    print(f"manifest closed — phase: {m['phase']}")
    print(f"  captured: {caps}")
    print(f"  scored:   {', '.join(f'{k} ({n})' for k, n in m['findings'].items()) or 'none'}")
    if m.get("finished_utc"):
        print(f"  finished: {m['finished_utc']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
