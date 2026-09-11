#!/usr/bin/env python3
"""Score the frozen fixture with the real lenses, and grade what comes back.

    run_evals.py --capture site --lens clarity --lens trust [--runs 3]
                 [--model opus] [--judge-model sonnet] [--budget-usd 4]
                 [--out understudy/evals/results] [--dry-run]
    run_evals.py --trend            # rebuild results/trend.md from history.csv

Each (lens, run) copies the frozen capture to a temp folder, invokes the
lens through `claude -p` with the lens agent's own file as the system
prompt, then grades the two files it wrote:

  contract   check_report.py on the output — binary, a gate (invariant)
  recall     for every defect planted for this lens, did ANY finding
             correspond to it, in any wording — an LLM judge, best of N
  clean      did it report one of the deliberately clean items — hallucination
  band       did each caught defect land in its planted severity band
  contained  did it report anything outside its lens
  score      the 0-10 the lens gave itself

Only `contract` is pass/fail. Everything else is a number written to
history.csv and trended; §11.8 says individual findings are not
reproducible, so no metric here is ever a gate.

Stdlib only. Needs the `claude` CLI on PATH for a real run; --dry-run and
the grading functions need nothing.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
NOT_USABLE = re.compile(r"not logged in|please run /login|invalid.{0,20}api key|authentication|hit your (session|usage) limit", re.I)
PLUGIN = os.path.normpath(os.path.join(HERE, ".."))
SCRIPTS = os.path.join(PLUGIN, "scripts")
sys.path.insert(0, SCRIPTS)
import check_report  # noqa: E402

FIXTURE = os.path.join(HERE, "fixture-run")
KEY = json.load(open(os.path.join(HERE, "fixture-site", "planted.json")))
RESULTS = os.path.join(HERE, "results")

LENS_TOOLS = ["Read", "Write", "Edit", "Glob", "Grep", "Bash(python3:*)", "Bash(ls:*)",
              "Bash(cat:*)", "Bash(find:*)", "Bash(wc:*)", "Bash(head:*)", "Bash(tail:*)",
              "Bash(grep:*)", "Bash(mkdir:*)"]
SEV_ORDER = ["P0", "P1", "P2", "P3"]

# ---------------------------------------------------------------- prompts --

def lens_system_prompt(lens, work):
    """The lens agent's own file, with the plugin root resolved, plus the
    run-specific frame the orchestrator would give it."""
    body = open(os.path.join(PLUGIN, "agents", f"lens-{lens}.md")).read()
    body = body.split("---", 2)[2] if body.startswith("---") else body
    body = body.replace("${CLAUDE_PLUGIN_ROOT}", PLUGIN)
    return (f"You are the understudy `lens-{lens}` scoring agent, running as a subagent.\n"
            f"Plugin root: {PLUGIN}\n"
            f"Run folder: {work}\n\n"
            f"Write exactly two files: {work}/{lens}/exec-summary.md and "
            f"{work}/{lens}/findings-final.md, per the output contract. Read only the "
            f"run folder and the plugin references. Never read another lens's folder. "
            f"Compute every finding id with {SCRIPTS}/finding_id.py.\n\n" + body)


def lens_user_prompt(lens, work):
    return (f"Score the run at {work} through the {lens} lens. Read manifest.json first, "
            f"then the evidence. Write the two files, run "
            f"`python3 {SCRIPTS}/check_report.py {work} --lens {lens}` and fix any failure "
            f"it reports, then reply with the verdict sentence and the count by severity.")


def planted_for(capture, lens):
    return [d for d in KEY[capture] if lens in d["lenses"]]


def clean_for(capture):
    return KEY[f"{capture}_clean"]


JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "caught": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "caught": {"type": "boolean"},
            "finding_title": {"type": "string"}}, "required": ["id", "caught", "finding_title"]}},
        "clean_reported": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "reported": {"type": "boolean"},
            "finding_title": {"type": "string"}}, "required": ["id", "reported", "finding_title"]}},
        "out_of_lens": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["caught", "clean_reported", "out_of_lens"],
}


def judge_prompt(capture, lens, findings_md):
    planted = planted_for(capture, lens)
    clean = clean_for(capture)
    return f"""You are grading a `{lens}` report written by an evaluation tool against a FICTIONAL
website with defects planted on purpose. Judge themes, not wording: a planted defect is
"caught" if ANY finding in the report describes the same problem, however it is phrased,
grouped or ranked. Be strict about substance — a finding about a different thing on the
same page is not a catch.

PLANTED DEFECTS this lens should have found (id — description):
{chr(10).join(f"- {d['id']} — {d['what']}" for d in planted)}

DELIBERATELY CLEAN ITEMS — a finding that reports one of these as a problem is a hallucination:
{chr(10).join(f"- {c['id']} — {c['what']}" for c in clean)}

OUT OF LENS — list the title of any finding that clearly belongs to a different check
(for example an SEO or page-speed finding in a clarity report). Empty if none.

THE REPORT:
{findings_md}

Return JSON only, matching the schema. For every planted id give caught true/false and the
title of the matching finding (empty string if none). For every clean id give reported
true/false and the offending title (empty if none)."""


# ---------------------------------------------------------------- graders --

def parse_findings(md):
    """(title, severity) pairs, via the gate's own parser."""
    out = []
    for f in check_report.parse_findings(md):
        sev = (f["fields"].get("severity") or "").upper()[:2]
        out.append({"title": f["title"], "severity": sev if sev in SEV_ORDER else ""})
    return out


def read_score(exec_md):
    m = check_report.SCORE_FIELD.search(exec_md or "")
    return int(m.group(1)) if m else None


def grade_band(capture, lens, judge, findings):
    """For each caught defect, is the matched finding's severity in the
    planted band? A severity is the least stable field (§11.8), so this is a
    metric, never a gate."""
    band = {d["id"]: d["band"] for d in planted_for(capture, lens)}
    sev_of = {f["title"].strip().lower(): f["severity"] for f in findings}
    rows = []
    for c in judge.get("caught", []):
        if not c.get("caught"):
            continue
        sev = sev_of.get((c.get("finding_title") or "").strip().lower(), "")
        ok = sev in band.get(c["id"], []) if sev else None
        rows.append({"id": c["id"], "severity": sev, "band": band.get(c["id"]), "in_band": ok})
    return rows


def summarise(capture, lens, judge, findings, contract_pass, score):
    planted = planted_for(capture, lens)
    caught = [c for c in judge.get("caught", []) if c.get("caught")]
    clean_hits = [c for c in judge.get("clean_reported", []) if c.get("reported")]
    band = grade_band(capture, lens, judge, findings)
    judged = [b for b in band if b["in_band"] is not None]
    return {
        "contract_pass": contract_pass,
        "planted": len(planted), "caught": len(caught),
        "recall": round(len(caught) / len(planted), 3) if planted else None,
        "caught_ids": sorted(c["id"] for c in caught),
        "missed_ids": sorted(set(d["id"] for d in planted) - set(c["id"] for c in caught)),
        "hallucinations": [c["id"] for c in clean_hits],
        "out_of_lens": judge.get("out_of_lens", []),
        "band_ok": sum(1 for b in judged if b["in_band"]), "band_judged": len(judged),
        "band_rows": band,
        "n_findings": len(findings),
        "severities": {s: sum(1 for f in findings if f["severity"] == s) for s in SEV_ORDER},
        "score": score,
    }


HISTORY_COLS = ["date", "capture", "lens", "model", "run", "contract_pass", "recall",
                "caught", "planted", "hallucinations", "out_of_lens", "band_ok",
                "band_judged", "n_findings", "score", "cost_usd", "seconds", "results_dir"]


def history_row(stamp, capture, lens, model, run, s, cost, seconds, results_dir):
    return {"date": stamp, "capture": capture, "lens": lens, "model": model, "run": run,
            "contract_pass": int(bool(s["contract_pass"])), "recall": s["recall"],
            "caught": s["caught"], "planted": s["planted"],
            "hallucinations": len(s["hallucinations"]), "out_of_lens": len(s["out_of_lens"]),
            "band_ok": s["band_ok"], "band_judged": s["band_judged"],
            "n_findings": s["n_findings"], "score": s["score"] if s["score"] is not None else "",
            "cost_usd": round(cost, 4) if cost is not None else "", "seconds": round(seconds, 1),
            "results_dir": os.path.relpath(results_dir, HERE)}


# ------------------------------------------------------------------ claude --

def preflight(model):
    """One cheap call. If the CLI is not signed in or the key is bad, every
    lens would 'fail' in a second with $0.00 spent and the history would fill
    with zeros that mean nothing. Observed 2026-09-11 on the first CI run:
    'Not logged in · Please run /login' recorded as recall 0/3 across eight
    lenses. Exit 2 — infrastructure, not a result."""
    try:
        p = subprocess.run(["claude", "-p", "Reply with the single word OK.", "--model", model,
                            "--output-format", "json", "--no-session-persistence",
                            "--max-budget-usd", "0.05"], capture_output=True, text=True, timeout=120)
        out = json.loads(p.stdout) if p.stdout.strip().startswith("{") else {"result": p.stdout + p.stderr}
    except (subprocess.TimeoutExpired, ValueError) as e:
        sys.exit(f"preflight: claude did not answer ({e}); nothing recorded")
    txt = (out.get("result") or "") + p.stderr
    if out.get("is_error") or NOT_USABLE.search(txt) or "OK" not in txt.upper():
        sys.exit(f"preflight: claude is not usable here — {txt.strip()[:160]!r}. "
                 f"Set ANTHROPIC_API_KEY (an API key, sk-ant-…) or sign in; nothing recorded")
    return True


def claude(prompt, model, system=None, tools=None, schema=None, budget=None, cwd=None,
           add_dir=None, timeout=1800):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json",
           "--no-session-persistence"]
    if system:
        cmd += ["--system-prompt", system]
    if tools:
        cmd += ["--allowedTools", *tools, "--permission-mode", "acceptEdits"]
    if schema:
        cmd += ["--json-schema", json.dumps(schema)]
    if budget:
        cmd += ["--max-budget-usd", str(budget)]
    if add_dir:
        cmd += ["--add-dir", add_dir]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout)
    try:
        out = json.loads(p.stdout)
    except ValueError:
        out = {"result": p.stdout, "is_error": True, "stderr": p.stderr[-2000:]}
    out.setdefault("stderr", p.stderr[-2000:] if p.returncode else "")
    return out


def judge_parse(out):
    """The judge's JSON — from structured_output when the CLI supports it,
    else the first JSON object in the result text."""
    if isinstance(out.get("structured_output"), dict):
        return out["structured_output"]
    txt = out.get("result") or ""
    m = re.search(r"\{.*\}", txt, re.S)
    if m:
        try:
            return json.loads(m.group(0))
        except ValueError:
            pass
    return {"caught": [], "clean_reported": [], "out_of_lens": [], "_unparsed": txt[:500]}


# -------------------------------------------------------------------- run --

def one(capture, lens, run_no, model, judge_model, budget, results_dir, dry):
    src = os.path.join(FIXTURE, capture)
    manifest = json.load(open(os.path.join(src, "manifest.json")))
    model = model or manifest["models"]["scoring"].get(lens) or "sonnet"
    tmp = tempfile.mkdtemp(prefix=f"understudy-eval-{capture}-{lens}-")
    work = os.path.join(tmp, os.path.basename(src))
    shutil.copytree(src, work)
    out_dir = os.path.join(results_dir, f"{capture}-{lens}-run{run_no}")
    os.makedirs(out_dir, exist_ok=True)

    sysprompt = lens_system_prompt(lens, work)
    user = lens_user_prompt(lens, work)
    if dry:
        open(os.path.join(out_dir, "system-prompt.txt"), "w").write(sysprompt)
        open(os.path.join(out_dir, "user-prompt.txt"), "w").write(user)
        print(f"  dry-run: {capture}/{lens} run {run_no} on {model} → {out_dir}")
        shutil.rmtree(tmp, ignore_errors=True)
        return None

    t0 = dt.datetime.now()
    res = claude(user, model, system=sysprompt, tools=LENS_TOOLS, budget=budget,
                 cwd=work, add_dir=work)
    seconds = (dt.datetime.now() - t0).total_seconds()
    open(os.path.join(out_dir, "lens-response.json"), "w").write(json.dumps(res, indent=1))

    lens_dir = os.path.join(work, lens)
    exec_md = findings_md = ""
    files_written = os.path.exists(os.path.join(lens_dir, "findings-final.md"))
    if files_written:
        exec_md = open(os.path.join(lens_dir, "exec-summary.md"), errors="replace").read() \
            if os.path.exists(os.path.join(lens_dir, "exec-summary.md")) else ""
        findings_md = open(os.path.join(lens_dir, "findings-final.md"), errors="replace").read()
        shutil.copy(os.path.join(lens_dir, "findings-final.md"), out_dir)
        if exec_md:
            shutil.copy(os.path.join(lens_dir, "exec-summary.md"), out_dir)
    else:
        open(os.path.join(out_dir, "returned-text.md"), "w").write(res.get("result") or "")

    gate = subprocess.run([sys.executable, os.path.join(SCRIPTS, "check_report.py"), work,
                           "--lens", lens, "--expect-lenses", "1"],
                          capture_output=True, text=True)
    contract_pass = gate.returncode == 0 and files_written
    open(os.path.join(out_dir, "gate.txt"), "w").write(gate.stdout + gate.stderr)

    findings = parse_findings(findings_md) if findings_md else []
    judge = {"caught": [], "clean_reported": [], "out_of_lens": []}
    jres = None
    if findings_md:
        jres = claude(judge_prompt(capture, lens, findings_md), judge_model,
                      schema=JUDGE_SCHEMA, budget=1.0)
        judge = judge_parse(jres)
        open(os.path.join(out_dir, "judge-response.json"), "w").write(json.dumps(jres, indent=1))

    s = summarise(capture, lens, judge, findings, contract_pass, read_score(exec_md))
    s.update({"capture": capture, "lens": lens, "model": model, "run": run_no,
              "files_written": files_written, "seconds": seconds,
              "cost_usd": (res.get("total_cost_usd") or 0) + ((jres or {}).get("total_cost_usd") or 0),
              "lens_turns": res.get("num_turns"), "lens_error": bool(res.get("is_error"))})
    json.dump(s, open(os.path.join(out_dir, "result.json"), "w"), indent=1)
    shutil.rmtree(tmp, ignore_errors=True)
    return s


def append_history(rows):
    path = os.path.join(RESULTS, "history.csv")
    new = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        wri = csv.DictWriter(f, fieldnames=HISTORY_COLS)
        if new:
            wri.writeheader()
        for r in rows:
            wri.writerow(r)


def trend():
    path = os.path.join(RESULTS, "history.csv")
    if not os.path.exists(path):
        return "no history yet"
    rows = list(csv.DictReader(open(path)))
    by = {}
    for r in rows:
        by.setdefault((r["capture"], r["lens"]), []).append(r)
    lines = ["# Eval trend", "", "Metrics, never gates (§11.8). One row per lens; the last "
             "five runs, newest first. `contract` is the only pass/fail column.", "",
             "| capture | lens | runs | contract | recall (last 5) | halluc. | out of lens | band ok | score | cost |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for (cap, lens), rs in sorted(by.items()):
        last = rs[-5:][::-1]
        rec = " ".join(r["recall"] or "–" for r in last)
        contract = f"{sum(int(r['contract_pass']) for r in rs)}/{len(rs)}"
        hal = " ".join(r["hallucinations"] for r in last)
        ool = " ".join(r["out_of_lens"] for r in last)
        band = " ".join(f"{r['band_ok']}/{r['band_judged']}" for r in last)
        score = " ".join(r["score"] or "–" for r in last)
        cost = f"${sum(float(r['cost_usd'] or 0) for r in rs):.2f}"
        lines.append(f"| {cap} | {lens} | {len(rs)} | {contract} | {rec} | {hal} | {ool} | {band} | {score} | {cost} |")
    text = "\n".join(lines) + "\n"
    open(os.path.join(RESULTS, "trend.md"), "w").write(text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", choices=["site", "product"])
    ap.add_argument("--lens", action="append", default=[])
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--model", default=None, help="override the manifest's allocation")
    ap.add_argument("--judge-model", default="sonnet")
    ap.add_argument("--budget-usd", type=float, default=4.0, help="per lens invocation")
    ap.add_argument("--out", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--trend", action="store_true")
    a = ap.parse_args()

    if a.trend:
        print(trend())
        return 0
    if not a.capture or not a.lens:
        ap.error("--capture and at least one --lens are required")

    if not a.dry_run:
        preflight(a.judge_model)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    results_dir = a.out or os.path.join(RESULTS, stamp)
    os.makedirs(results_dir, exist_ok=True)
    if a.lens == ["all"]:
        # the lenses this capture was made for — the manifest's objectives —
        # not every lens the answer key happens to mention
        m = json.load(open(os.path.join(FIXTURE, a.capture, "manifest.json")))
        lenses = list(m.get("objectives") or [])
    else:
        lenses = a.lens
    lenses = sorted(set(l for l in lenses if planted_for(a.capture, l)))

    rows, results = [], []
    for lens in lenses:
        for i in range(1, a.runs + 1):
            print(f"→ {a.capture}/{lens} run {i}/{a.runs}")
            s = one(a.capture, lens, i, a.model, a.judge_model, a.budget_usd, results_dir, a.dry_run)
            if s is None:
                continue
            results.append(s)
            rows.append(history_row(stamp, a.capture, lens, s["model"], i, s, s["cost_usd"],
                                    s["seconds"], results_dir))
            print(f"  contract {'PASS' if s['contract_pass'] else 'FAIL'} · recall "
                  f"{s['caught']}/{s['planted']} · hallucinations {len(s['hallucinations'])} · "
                  f"out-of-lens {len(s['out_of_lens'])} · band {s['band_ok']}/{s['band_judged']} · "
                  f"score {s['score']} · ${s['cost_usd']:.2f} · {s['seconds']:.0f}s")
            if s["missed_ids"]:
                print(f"  missed: {', '.join(s['missed_ids'])}")
    if results:
        json.dump(results, open(os.path.join(results_dir, "summary.json"), "w"), indent=1)
        append_history(rows)
        trend()
        print(f"\nresults: {results_dir}\nhistory: {os.path.join(RESULTS, 'history.csv')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
