#!/usr/bin/env python3
"""Mark where a run is, for watch.py.

    mark.py <run> --phase capture|scoring|closing|complete
    mark.py <run> --lens ux:opus --lens bugs:sonnet     lenses just launched
    mark.py <run> --note "text"                          one line for the dashboard

Writes status.json in the run folder. It is a courtesy to the watcher, not a
record: the manifest stays the source of truth and is written by init_run.py
and close_run.py, never here. Everything the watcher shows about personas —
progress, pauses, screenshots, the feed — comes from the traversal's own
files and needs no mark.
"""
import argparse
import datetime as dt
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--phase", choices=["capture", "scoring", "closing", "complete"])
    ap.add_argument("--lens", action="append", default=[],
                    help="name[:model] of a lens agent just launched; repeatable")
    ap.add_argument("--note", default=None)
    a = ap.parse_args()
    run = os.path.expanduser(a.run.rstrip("/"))
    if not os.path.exists(os.path.join(run, "manifest.json")):
        sys.exit(f"not a run folder (no manifest.json): {run}")
    path = os.path.join(run, "status.json")
    try:
        with open(path, encoding="utf-8") as fh:
            status = json.load(fh)
    except (OSError, ValueError):
        status = {}
    if a.phase:
        status["phase"] = a.phase
    if a.lens:
        seen = {l["name"]: l for l in status.get("lenses") or []}
        for spec in a.lens:
            name, _, model = spec.partition(":")
            seen[name] = {"name": name, "model": model}
        status["lenses"] = list(seen.values())
    if a.note is not None:
        status["note"] = a.note
    status["updated_utc"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(status, fh, indent=1)
    print(path)


if __name__ == "__main__":
    main()
