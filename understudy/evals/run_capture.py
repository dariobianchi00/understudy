#!/usr/bin/env python3
"""Capture evals — drive the fixture site for real, through the real skill.

    run_capture.py [--persona evaluator] [--model opus] [--judge-model sonnet]
                   [--budget-usd 6] [--timeout 1800] [--port 8765]
                   [--out understudy/evals/results] [--dry-run]

The one eval layer that needs a browser. It serves evals/fixture-site/ on
localhost, creates a run folder with init_run.py from a fixture target, and
hands the traversal-visit skill to `claude -p` with a Playwright MCP server
attached — the same skill, the same references, the same pause rules a real
run uses. Then it grades the capture that comes out. It never scores.

What is graded, and how:

  gate          check_capture.py passes — banned vocabulary, manifest,
                legibility                                        invariant
  cited-shots   every screenshot an artifact names is on disk, and every
                screenshot on disk is named by some artifact — the
                log, findings-raw.json, timeline or debrief         invariant
  moved-as-you-go screenshot mtimes are spread across the session, not
                clustered at the end: the "move immediately" rule  invariant
  pre-session   the entry expectation is logged before the first
                timestamped line                                   invariant
  no-submit     timeline says forms_submitted == 0 and the network dump
                shows no POST to the site                          invariant
  viewport      the timeline or the log records a verified viewport  invariant
  hygiene       no .playwright-mcp/ or *.png left in the working dir invariant
  debrief       Q1–Q6 answered                                     invariant
  persona       an LLM judge on the log: first person, present tense,
                reactions not diagnoses, skims rather than reads    metric

Stdlib only. Needs `claude`, `npx` (for @playwright/mcp) and a Chromium
Playwright can launch. --dry-run needs none of them.
"""
import argparse
import csv
import datetime as dt
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.normpath(os.path.join(HERE, ".."))
SCRIPTS = os.path.join(PLUGIN, "scripts")
SITE = os.path.join(HERE, "fixture-site")
RESULTS = os.path.join(HERE, "results")
NOT_USABLE = re.compile(r"not logged in|please run /login|invalid.{0,20}api key|hit your (session|usage) limit|credit balance", re.I)

PERSONAS = {
    "evaluator": {"device": "desktop-1440x900", "viewport": (1440, 900),
                  "brief": "You are evaluating whether this could replace what your team uses for notes. "
                           "You have five minutes and you want to know what it costs. You leave if the "
                           "page is all adjectives and no product, or if you cannot find a price."},
    "sceptic": {"device": "iphone-13", "viewport": (390, 844),
                "brief": "A friend said 'try this, it remembers everything'. You want to know who is "
                         "behind it and what happens to your notes before you consider it. You leave "
                         "if the privacy page is a generic policy."},
}
SKILL_REFS = ["visit-shapes.md", "playwright-patterns.md", "evidence-rules.md", "banned-vocabulary.md"]
AGENT_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash(python3:*)", "Bash(mv:*)", "Bash(mkdir:*)",
               "Bash(ls:*)", "Bash(rm -rf ./.playwright-mcp:*)", "Bash(rm -rf .playwright-mcp:*)",
               "Bash(git status:*)", "Bash(date:*)", "mcp__playwright__*"]


# ------------------------------------------------------------- run folder --

def target_yaml(port, persona, out_dir):
    p = PERSONAS[persona]
    return f"""slug: nimbus-notes-site
product_name: Nimbus Notes
base_url: http://localhost:{port}/
public_site: true
assessment_type: website
auth:
  wall: false
  wall_location: null
competitors: []
conversion_goal: "Start a free trial without talking to sales"
objectives:
  - clarity
  - trust
coverage_depth: standard
objectives_under_test: []
persona_mode: generic
personas:
  - name: {persona}
    device: {p['device']}
    goal: "{p['brief'].split('.')[0]}."
    gives_up_when: "{p['brief'].split('You leave if ')[-1].rstrip('.')}."
models:
  scoring_shape: balanced
  scoring:
    clarity: opus
    trust: opus
time_cap_minutes: 20
checkpoints: [10]
scope_exclusions: []
vocabulary_allowlist: []
output_dir: {out_dir}
"""


def init_run(port, persona, tmp):
    out = os.path.join(tmp, "runs")
    tp = os.path.join(tmp, "target.yaml")
    open(tp, "w").write(target_yaml(port, persona, out))
    p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "init_run.py"), "--target", tp,
                        "--traversal-model", "capture-eval"], capture_output=True, text=True)
    if p.returncode:
        sys.exit(f"init_run failed: {p.stderr}")
    return p.stdout.strip().split("\n")[-1]


# ---------------------------------------------------------------- prompts --

def system_prompt(persona, run, port):
    skill = open(os.path.join(PLUGIN, "skills", "traversal-visit", "SKILL.md")).read()
    skill = skill.split("---", 2)[2] if skill.startswith("---") else skill
    refs = "\n\n".join(f"<!-- references/{r} -->\n" + open(os.path.join(PLUGIN, "references", r)).read()
                       for r in SKILL_REFS)
    p = PERSONAS[persona]
    w, h = p["viewport"]
    text = (f"You are running the understudy traversal-visit skill, as the persona below. "
            f"Plugin root: {PLUGIN}\nRun folder: {run}\nPersona folder: {run}/persona-{persona}\n"
            f"Site: http://localhost:{port}/  (a local test site; it is fine to browse it)\n"
            f"Device: {p['device']} — viewport {w}x{h}. Verify it after setting it.\n\n"
            f"PERSONA BRIEF: {p['brief']}\n\n"
            f"Drive the browser with the Playwright MCP tools (mcp__playwright__browser_*). "
            f"Screenshots are written by the server into the current working directory or its "
            f".playwright-mcp/; move each into the persona's screenshots/ folder immediately after "
            f"taking it. Write session.log, timeline.json, persona-debrief.md, findings-raw.json, "
            f"console-full.txt and network-full.txt into the persona folder. Never submit a form. "
            f"Stop within 12 minutes of wall-clock time. Close the browser and sweep .playwright-mcp "
            f"when done, then run python3 {SCRIPTS}/check_capture.py {run} and fix what it reports.\n\n"
            f"=== SKILL ===\n{skill}\n\n=== REFERENCES ===\n{refs}")
    return text.replace("${CLAUDE_PLUGIN_ROOT}", PLUGIN)


USER_PROMPT = ("Begin the visit now. Announce each shape transition on one line. When the debrief "
               "is written and the gate passes, reply with the persona's one-sentence answer to Q1 "
               "and the number of screenshots taken.")


# ---------------------------------------------------------------- graders --

def grade(run, persona, cwd, t_start, t_end):
    """Every deterministic check. Returns (failures, facts)."""
    pdir = os.path.join(run, f"persona-{persona}")
    fails, facts = [], {}

    gate = subprocess.run([sys.executable, os.path.join(SCRIPTS, "check_capture.py"), run],
                          capture_output=True, text=True)
    facts["gate"] = gate.stdout + gate.stderr
    if gate.returncode:
        fails.append("check_capture failed")

    log_path = os.path.join(pdir, "session.log")
    log = open(log_path, errors="replace").read() if os.path.exists(log_path) else ""
    shots_dir = os.path.join(pdir, "screenshots")
    shots = sorted(glob.glob(os.path.join(shots_dir, "*.png")))
    facts["screenshots"] = len(shots)
    if len(shots) < 3:
        fails.append(f"only {len(shots)} screenshot(s)")

    # A screenshot is "named" if any capture artifact cites it — the log,
    # the raw reactions or the timeline. The first real run named four of
    # eight in findings-raw.json only, which is a citation a lens can use.
    cited_in = log
    for extra in ("findings-raw.json", "timeline.json", "persona-debrief.md"):
        ep = os.path.join(pdir, extra)
        if os.path.exists(ep):
            cited_in += "\n" + open(ep, errors="replace").read()
    named = set(re.findall(r"\b(\d\d-[\w-]+\.png)", cited_in))
    on_disk = {os.path.basename(s) for s in shots}
    if named - on_disk:
        fails.append(f"artifacts name screenshots not on disk: {sorted(named - on_disk)[:4]}")
    if on_disk - named:
        fails.append(f"screenshots on disk that no artifact names: {sorted(on_disk - named)[:4]}")

    # moved-as-you-go: mtimes should spread over the session, not sit in
    # the last slice of it. mv preserves mtime, so this survives the move.
    if shots and t_end > t_start:
        mt = sorted(os.path.getmtime(s) for s in shots)
        span = t_end - t_start
        first_frac = (mt[0] - t_start) / span
        spread_frac = (mt[-1] - mt[0]) / span
        facts["first_shot_at_pct"] = round(first_frac * 100)
        facts["shots_spread_pct"] = round(spread_frac * 100)
        if len(shots) >= 3 and spread_frac < 0.25:
            fails.append(f"screenshots clustered — spread over {spread_frac:.0%} of the session; "
                         f"were they moved in a batch at the end?")

    pre = [i for i, l in enumerate(log.splitlines()) if l.startswith("[pre-session]")]
    stamped = [i for i, l in enumerate(log.splitlines()) if re.match(r"\[\d\d:\d\d\]", l)]
    if not pre:
        fails.append("no [pre-session] entry expectation")
    elif stamped and min(pre) > min(stamped):
        fails.append("[pre-session] lines come after the first timestamped action")

    tl_path = os.path.join(pdir, "timeline.json")
    try:
        tl = json.load(open(tl_path))
    except (OSError, ValueError):
        tl = {}
        fails.append("timeline.json missing or invalid")
    v3 = tl.get("shape_v3") or {}
    if v3.get("forms_submitted") not in (0, None):
        fails.append(f"timeline says forms_submitted={v3.get('forms_submitted')}")
    net_path = os.path.join(pdir, "network-full.txt")
    net = open(net_path, errors="replace").read() if os.path.exists(net_path) else ""
    posts = [l for l in net.splitlines() if re.search(r"\bPOST\b", l) and "localhost" in l]
    if posts:
        fails.append(f"POST to the site in the network dump: {posts[0][:80]}")
    vp = tl.get("viewport") or {}
    if not (vp.get("verified") or re.search(r"innerWidth|viewport verified", log, re.I)):
        fails.append("viewport never verified (timeline.viewport.verified, or 'viewport verified' / innerWidth in the log)")
    facts["time_to_comprehension"] = (tl.get("shape_v1") or {}).get("time_to_comprehension_seconds")
    facts["left_early"] = tl.get("left_early")

    deb_path = os.path.join(pdir, "persona-debrief.md")
    deb = open(deb_path, errors="replace").read() if os.path.exists(deb_path) else ""
    missing_q = [q for q in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6") if q not in deb]
    if missing_q:
        fails.append(f"debrief missing {', '.join(missing_q)}")

    if os.path.exists(os.path.join(cwd, ".playwright-mcp")):
        fails.append(".playwright-mcp/ left in the working directory")
    if glob.glob(os.path.join(cwd, "*.png")):
        fails.append("*.png left in the working directory")
    return fails, facts


JUDGE_SCHEMA = {"type": "object", "properties": {"pass": {"type": "boolean"}, "reason": {"type": "string"},
                                                 "read_everything": {"type": "boolean"},
                                                 "diagnosed": {"type": "boolean"}},
                "required": ["pass", "reason", "read_everything", "diagnosed"]}


def judge_persona(log, debrief, model):
    prompt = f"""You are grading whether a browser session log was written AS A VISITOR, not as an analyst.
A visitor writes in first person, present tense; reacts ("I can't find the price") rather than
diagnoses ("pricing is poorly placed"); skims rather than reads every word; and leaves when it
stops being worth it. An analyst explores every page dutifully, uses evaluation vocabulary, and
explains causes.

SESSION LOG:
{log[:6000]}

DEBRIEF:
{debrief[:2500]}

Return JSON: pass (true if it reads as a visitor throughout), reason (one line),
read_everything (true if the persona dutifully opened every page rather than following its own
question), diagnosed (true if any line explains a cause instead of recording a reaction)."""
    p = subprocess.run(["claude", "-p", prompt, "--model", model, "--output-format", "json",
                        "--no-session-persistence", "--json-schema", json.dumps(JUDGE_SCHEMA),
                        "--max-budget-usd", "0.5"], capture_output=True, text=True, timeout=300)
    try:
        out = json.loads(p.stdout)
    except ValueError:
        return {"pass": None, "reason": "judge returned no JSON", "cost": 0}
    so = out.get("structured_output")
    if not isinstance(so, dict):
        m = re.search(r"\{.*\}", out.get("result") or "", re.S)
        so = json.loads(m.group(0)) if m else {"pass": None, "reason": "unparsed"}
    so["cost"] = out.get("total_cost_usd") or 0
    return so


# ------------------------------------------------------------------- run --

def mcp_config():
    return json.dumps({"mcpServers": {"playwright": {
        "command": "npx", "args": ["-y", "@playwright/mcp@latest", "--headless", "--isolated"]}}})


def serve(port):
    p = subprocess.Popen([sys.executable, os.path.join(SITE, "serve.py"), str(port)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        try:
            import urllib.request
            urllib.request.urlopen(f"http://localhost:{port}/index.html", timeout=1)
            return p
        except Exception:
            time.sleep(0.5)
    p.kill()
    sys.exit("fixture site did not come up")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--persona", default="evaluator", choices=sorted(PERSONAS))
    ap.add_argument("--model", default="opus", help="the traversal runs on the session model in a real run")
    ap.add_argument("--judge-model", default="sonnet")
    ap.add_argument("--budget-usd", type=float, default=6.0)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--out", default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    out_dir = a.out or os.path.join(RESULTS, f"capture-{stamp}-{a.persona}")
    os.makedirs(out_dir, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="understudy-capture-")
    run = init_run(a.port, a.persona, tmp)
    sysp = system_prompt(a.persona, run, a.port)
    open(os.path.join(out_dir, "system-prompt.txt"), "w").write(sysp)
    if a.dry_run:
        print(f"dry-run: run folder {run}; prompts in {out_dir}")
        shutil.rmtree(tmp, ignore_errors=True)
        return 0

    server = serve(a.port)
    t0 = time.time()
    try:
        cmd = ["claude", "-p", USER_PROMPT, "--model", a.model, "--system-prompt", sysp,
               "--output-format", "json", "--no-session-persistence",
               "--mcp-config", mcp_config(), "--strict-mcp-config",
               "--allowedTools", *AGENT_TOOLS, "--permission-mode", "acceptEdits",
               "--max-budget-usd", str(a.budget_usd), "--add-dir", tmp]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, cwd=tmp, timeout=a.timeout)
            res = json.loads(p.stdout) if p.stdout.strip().startswith("{") else {"result": p.stdout, "is_error": True}
            res["stderr"] = p.stderr[-2000:]
        except subprocess.TimeoutExpired:
            res = {"result": "", "is_error": True, "timeout": True}
    finally:
        server.kill()
    t1 = time.time()
    open(os.path.join(out_dir, "agent-response.json"), "w").write(json.dumps(res, indent=1))

    if NOT_USABLE.search(res.get("result") or ""):
        print(f"SKIPPED — claude not usable: {(res.get('result') or '')[:100]}")
        shutil.rmtree(tmp, ignore_errors=True)
        return 2

    fails, facts = grade(run, a.persona, tmp, t0, t1)
    pdir = os.path.join(run, f"persona-{a.persona}")
    for f in ("session.log", "timeline.json", "persona-debrief.md", "findings-raw.json",
              "console-full.txt", "network-full.txt"):
        if os.path.exists(os.path.join(pdir, f)):
            shutil.copy(os.path.join(pdir, f), out_dir)
    log = open(os.path.join(pdir, "session.log"), errors="replace").read() \
        if os.path.exists(os.path.join(pdir, "session.log")) else ""
    deb = open(os.path.join(pdir, "persona-debrief.md"), errors="replace").read() \
        if os.path.exists(os.path.join(pdir, "persona-debrief.md")) else ""
    jd = judge_persona(log, deb, a.judge_model) if log else None

    r = {"persona": a.persona, "model": a.model, "pass": not fails, "failures": fails, "facts": facts,
         "judge": jd, "seconds": round(t1 - t0), "agent_turns": res.get("num_turns"),
         "cost_usd": round((res.get("total_cost_usd") or 0) + ((jd or {}).get("cost") or 0), 4),
         "timeout": bool(res.get("timeout"))}
    json.dump(r, open(os.path.join(out_dir, "result.json"), "w"), indent=1)
    shutil.rmtree(tmp, ignore_errors=True)

    print(f"{'PASS' if r['pass'] else 'FAIL'} · {facts.get('screenshots', 0)} shots · "
          f"first at {facts.get('first_shot_at_pct', '?')}% · spread {facts.get('shots_spread_pct', '?')}% · "
          f"persona {'-' if not jd else ('ok' if jd.get('pass') else 'analyst-ish')} · "
          f"${r['cost_usd']:.2f} · {r['seconds']}s")
    for f in fails:
        print(f"  - {f}")
    if jd:
        print(f"  judge: {jd.get('reason')}")
    hist = os.path.join(RESULTS, "capture-history.csv")
    new = not os.path.exists(hist)
    with open(hist, "a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["date", "persona", "model", "pass", "failures", "screenshots", "spread_pct",
                        "persona_ok", "cost_usd", "seconds", "results_dir"])
        w.writerow([stamp, a.persona, a.model, int(r["pass"]), len(fails), facts.get("screenshots", 0),
                    facts.get("shots_spread_pct", ""), "" if not jd else int(bool(jd.get("pass"))),
                    r["cost_usd"], r["seconds"], os.path.relpath(out_dir, HERE)])
    return 0 if r["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
