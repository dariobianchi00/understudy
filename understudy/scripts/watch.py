#!/usr/bin/env python3
"""Watch an understudy run as it happens, from a second terminal pane.

    watch.py <run_folder>              live dashboard (curses); q quits
    watch.py <runs_parent>             same, on the newest run under that folder
    watch.py <run> --line              one line, for a Claude Code status line
    watch.py <run> --replay [--speed N]  replay a finished run's persona feed

Everything shown is read off the run folder, which the traversal writes as it
goes: session.log after every action, screenshots the moment they are taken,
lens folders as each scorer finishes. The orchestrator adds a small
status.json (via mark.py) naming the phase and the lenses it launched; the
watcher works without it, with less to say.

stdlib only, like every script in this folder.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import time

LOG_LINE = re.compile(r"^\[(\d{2}):(\d{2})(?: persona)?\]\s*(.*)$")
PAUSE_RE = re.compile(r"PAUSED", re.I)
RESUME_RE = re.compile(r"wall cleared|resuming", re.I)
LENS_DIRS = ("ux", "bugs", "onboarding", "content", "clarity", "conversion", "trust",
             "technical", "seo", "aeo", "compare", "objectives")


def _read(path, default=""):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return default


def _json(path):
    try:
        return json.loads(_read(path, "null"))
    except ValueError:
        return None


def find_run(path):
    """A run folder, or the newest run under a parent folder."""
    path = os.path.expanduser(path.rstrip("/"))
    if os.path.exists(os.path.join(path, "manifest.json")):
        return path
    runs = []
    try:
        names = os.listdir(path)
    except OSError:
        return None
    for name in names:
        m = _json(os.path.join(path, name, "manifest.json"))
        if isinstance(m, dict):
            runs.append((m.get("started_utc") or "", os.path.join(path, name)))
    return max(runs)[1] if runs else None


def parse_log(text):
    """(persona_seconds_of_last_action, paused, lines) from a session.log."""
    last = 0
    paused = False
    lines = []
    for raw in text.splitlines():
        m = LOG_LINE.match(raw)
        if m:
            last = int(m.group(1)) * 60 + int(m.group(2))
            body = m.group(3)
        else:
            body = raw
        if PAUSE_RE.search(raw):
            paused = True
        elif RESUME_RE.search(raw):
            paused = False
        lines.append((m.group(1) + ":" + m.group(2) if m else "", body))
    return last, paused, lines


def read_state(run):
    """Everything the dashboard shows, as plain data. Pure: reads files only."""
    manifest = _json(os.path.join(run, "manifest.json")) or {}
    status = _json(os.path.join(run, "status.json")) or {}
    personas = []
    active = None
    for p in manifest.get("personas") or []:
        name = p.get("name", "")
        pdir = os.path.join(run, f"persona-{name}")
        log = _read(os.path.join(pdir, "session.log"))
        shots = 0
        latest_shot = ""
        try:
            pngs = sorted(f for f in os.listdir(os.path.join(pdir, "screenshots"))
                          if f.endswith(".png"))
            shots = len(pngs)
            latest_shot = pngs[-1] if pngs else ""
        except OSError:
            pass
        last, paused, lines = parse_log(log)
        if os.path.exists(os.path.join(pdir, "persona-debrief.md")):
            state = "done"
        elif log:
            state = "running"
        else:
            state = "pending"
        entry = {"name": name, "device": p.get("device", ""), "state": state,
                 "seconds": last, "shots": shots, "latest_shot": latest_shot,
                 "paused": paused and state == "running", "lines": lines}
        personas.append(entry)
        if state == "running" and active is None:
            active = entry
    if active is None:
        running = [p for p in personas if p["state"] == "running"]
        active = running[-1] if running else (personas[-1] if personas and personas[-1]["lines"] else None)

    launched = {l["name"]: l.get("model", "") for l in status.get("lenses") or []}
    lenses = []
    for name in manifest.get("objectives") or []:
        done = os.path.exists(os.path.join(run, name, "findings-final.md"))
        model = launched.get(name) or (manifest.get("models", {}).get("scoring", {}) or {}).get(name, "")
        lenses.append({"name": name, "model": model,
                       "state": "done" if done else ("running" if name in launched else "pending")})
    if manifest.get("objectives_under_test"):
        done = os.path.exists(os.path.join(run, "objectives", "results.md"))
        lenses.append({"name": "objectives", "model": launched.get("objectives", ""),
                       "state": "done" if done else ("running" if "objectives" in launched else "pending")})

    # The manifest's phases are init_run/close_run vocabulary ("2a-capture",
    # "2b-scoring", "complete"); the dashboard's are the four a person watches.
    mphase = {"2a-capture": "capture", "2b-scoring": "scoring"}.get(
        manifest.get("phase"), manifest.get("phase"))
    phase = status.get("phase") or mphase or "capture"
    if mphase == "complete":
        phase = "complete"
    n_done = sum(1 for p in personas if p["state"] == "done")
    return {
        "run": run,
        "product": manifest.get("product_name") or manifest.get("target_slug") or os.path.basename(run),
        "run_id": manifest.get("run_id", ""),
        "phase": phase,
        "note": status.get("note", ""),
        "cap": int(manifest.get("time_cap_minutes") or 0) * 60,
        "started_utc": manifest.get("started_utc"),
        "personas": personas,
        "active": active,
        "persona_progress": (n_done + (1 if active and active["state"] == "running" else 0), len(personas)),
        "lenses": lenses,
        "traversal_model": (manifest.get("models") or {}).get("traversal", ""),
    }


def mmss(seconds):
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def bar(frac, width):
    frac = max(0.0, min(1.0, frac))
    n = int(round(frac * width))
    return "▓" * n + "░" * (width - n)


def status_line(state, colour=True):
    """One line for a Claude Code status line."""
    C = (lambda code, s: f"\033[{code}m{s}\033[0m") if colour else (lambda code, s: s)
    a = state["active"]
    phase = state["phase"]
    if phase == "complete":
        return C("32", "understudy ✓") + f" {state['product']} · run {state['run_id']} complete"
    if a and a["state"] == "running":
        if a["paused"]:
            head = C("33", "understudy ⏸") + f" {a['name']} — authenticate in the browser, then confirm"
            return head
        cap = f"/{mmss(state['cap'])}" if state["cap"] else ""
        last = next((b for _, b in reversed(a["lines"]) if b and not b.startswith("---")), "")
        last = (last[:70] + "…") if len(last) > 70 else last
        return (C("36", "understudy ▶") + f" {a['name']} {mmss(a['seconds'])}{cap} · "
                f"{a['shots']} shots · {last}")
    running = [l["name"] for l in state["lenses"] if l["state"] == "running"]
    done = [l["name"] for l in state["lenses"] if l["state"] == "done"]
    if running or done:
        return (C("35", "understudy ◆ scoring") + f" {len(done)}/{len(state['lenses'])} done"
                + (f" · running: {', '.join(running)}" if running else ""))
    p_done, p_all = state["persona_progress"]
    return C("36", "understudy ·") + f" {state['product']} · capture {p_done}/{p_all}"


# ---- curses dashboard -------------------------------------------------------

def _wrap(text, width):
    words, out, cur = text.split(" "), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w) if cur else w
    if cur:
        out.append(cur)
    return out or [""]


def draw(stdscr, state, tick):
    import curses
    stdscr.erase()
    h, w = stdscr.getmaxyx()
    if h < 8 or w < 60:
        stdscr.addstr(0, 0, "window too small")
        stdscr.refresh()
        return
    a = state["active"]
    p_done, p_all = state["persona_progress"]
    phase_txt = {"capture": f"CAPTURE {p_done} of {p_all}", "scoring": "SCORING",
                 "closing": "CLOSING", "complete": "COMPLETE"}.get(state["phase"], state["phase"].upper())
    head = f" {state['product']} · run {state['run_id']} · {phase_txt}"
    if a and state["cap"]:
        prog = f"{bar(a['seconds'] / state['cap'], 14)}  {mmss(a['seconds'])} / {mmss(state['cap'])} "
        stdscr.addstr(0, 0, head[:w - 1], curses.A_BOLD)
        if w - len(prog) - 1 > len(head):
            stdscr.addstr(0, w - len(prog) - 1, prog)
    else:
        stdscr.addstr(0, 0, head[:w - 1], curses.A_BOLD)
    stdscr.addstr(1, 0, "─" * (w - 1))

    left_w = min(44, w // 2)
    col = left_w + 1
    y = 2
    stdscr.addstr(y, 1, "WHO IS DOING WHAT", curses.A_BOLD)
    y += 1
    marks = {"done": "✓", "running": "▶", "pending": "·"}
    for p in state["personas"]:
        extra = ""
        if p["state"] == "done":
            extra = f"{mmss(p['seconds'])}  {p['shots']} shots"
        elif p["state"] == "running":
            extra = ("paused" if p["paused"] else f"{mmss(p['seconds'])}") + f"  {p['shots']} shots"
        else:
            extra = p["device"]
        line = f" {marks[p['state']]} {p['name']:<18} {extra}"
        attr = curses.A_BOLD if p["state"] == "running" else curses.A_NORMAL
        stdscr.addstr(y, 0, line[:left_w], attr)
        y += 1
    y += 1
    stdscr.addstr(y, 1, "LENSES" + ("" if state["phase"] != "capture" else " (after capture)"), curses.A_BOLD)
    y += 1
    for l in state["lenses"]:
        line = f" {marks[l['state']]} {l['name']:<12} {l['model']}"
        attr = curses.A_BOLD if l["state"] == "running" else curses.A_NORMAL
        if y < h - 2:
            stdscr.addstr(y, 0, line[:left_w], attr)
        y += 1
    if a and a["latest_shot"] and y < h - 2:
        y += 1
        stdscr.addstr(y, 1, f"last shot  {a['latest_shot']}"[:left_w - 1])
    if state["note"] and y + 1 < h - 2:
        y += 1
        stdscr.addstr(y, 1, state["note"][:left_w - 1])

    for row in range(2, h - 1):
        stdscr.addstr(row, left_w, "│")

    feed_w = w - col - 2
    if a:
        title = f"PERSONA · {a['name']} · {a['device']}"
        stdscr.addstr(2, col + 1, title[:feed_w], curses.A_BOLD)
        rows = []
        for ts, body in a["lines"]:
            if not body:
                continue
            first = True
            for seg in _wrap(body, feed_w - 8):
                rows.append((f"[{ts}] " if first and ts else "        ", seg))
                first = False
        avail = h - 4 - (1 if a["paused"] else 0)
        for i, (pre, seg) in enumerate(rows[-avail:]):
            stdscr.addstr(3 + i, col + 1, (pre + seg)[:feed_w])
    else:
        stdscr.addstr(2, col + 1, "waiting for the first persona…"[:feed_w])

    foot = " q quits · refreshes every second"
    if a and a["paused"]:
        foot = " ⏸ PAUSED at the auth wall — log in in the browser, then confirm in Claude Code"
        stdscr.addstr(h - 1, 0, foot[:w - 1], curses.A_BOLD | curses.A_REVERSE)
    elif state["phase"] == "complete":
        stdscr.addstr(h - 1, 0, " ✓ run complete — the deliverable is in the run folder"[:w - 1], curses.A_BOLD)
    else:
        stdscr.addstr(h - 1, 0, foot[:w - 1], curses.A_DIM)
    stdscr.refresh()


def live(run, interval=1.0, frames=None):
    import curses

    def main(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        tick = 0
        while frames is None or tick < frames:
            try:
                draw(stdscr, read_state(run), tick)
            except curses.error:
                pass
            for _ in range(int(interval * 10)):
                ch = stdscr.getch()
                if ch in (ord("q"), ord("Q"), 27):
                    return
                if ch == curses.KEY_RESIZE:
                    break
                time.sleep(0.1)
            tick += 1
    curses.wrapper(main)


def replay(run, speed=20.0):
    """Print a finished run's persona feeds at `speed`× the persona clock."""
    state = read_state(run)
    print(f"{state['product']} · run {state['run_id']} · replay at {speed:g}×\n")
    for p in state["personas"]:
        print(f"── {p['name']} · {p['device']} ──")
        prev = 0
        for ts, body in p["lines"]:
            if ts:
                secs = int(ts[:2]) * 60 + int(ts[3:])
                time.sleep(max(0, secs - prev) / speed)
                prev = secs
            print(f"[{ts}] {body}" if ts else body)
        print()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="a run folder, or a folder of runs (the newest is watched)")
    ap.add_argument("--line", action="store_true", help="print one status line and exit")
    ap.add_argument("--no-colour", action="store_true")
    ap.add_argument("--replay", action="store_true")
    ap.add_argument("--speed", type=float, default=20.0)
    ap.add_argument("--interval", type=float, default=1.0)
    ap.add_argument("--frames", type=int, default=None, help=argparse.SUPPRESS)
    a = ap.parse_args()
    run = find_run(a.path)
    if not run:
        if a.line:
            print("understudy · no run")
            return
        sys.exit(f"no run with a manifest.json at or under {a.path}")
    if a.line:
        print(status_line(read_state(run), colour=not a.no_colour))
    elif a.replay:
        replay(run, a.speed)
    else:
        live(run, a.interval, a.frames)


if __name__ == "__main__":
    main()
