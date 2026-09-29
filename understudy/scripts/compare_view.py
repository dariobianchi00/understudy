#!/usr/bin/env python3
"""
compare_view.py — the Mode D comparison as structure, for the interactive report.

The compare lens writes one `## Differences matrix` (agents/lens-compare.md):
a table whose first column is the dimension, whose middle columns are one
site each, and whose last is the verdict. `render_report.comparison_section`
lifts that table whole for the PDF. This module reads the same table — never a
second copy — into structure the interactive page can lay out: the sites with
their logos and their own per-check scores, the lead/trail/level tally, and
for each competitor the rows where it does better or worse than the client's
site, read from the ✓ ⚠ ✗ markers the lens put in each cell.

Nothing here scores. Every number is the lens's own: the verdict column is
the lens's verdict, a "does better" row is one where the lens marked their
cell ✓ and ours ⚠ or ✗, and a per-site score is the `- **Score:**` line that
site's lens wrote. A cell without a marker is not counted either way.

Stdlib only, like every script here.
"""
import json
import os
import re
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_report as rr  # noqa: E402
import run_layout  # noqa: E402

VERDICTS = ("leads", "trails", "level", "not comparable")
MARK = {"✓": 2, "⚠": 1, "✗": 0}


def _strip(text):
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", text or "")
    return re.sub(r"`([^`]+)`", r"\1", t).strip()


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def _host(url):
    h = urllib.parse.urlparse(url or "").netloc.lower()
    return h[4:] if h.startswith("www.") else h


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def matrix_rows(md):
    """(headers, rows) of the table under `## Differences matrix`, or ([], [])."""
    m = re.search(r"^##\s+Differences matrix\s*$", md, re.M)
    if not m:
        return [], []
    rest = md[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    body = rest[:nxt.start()] if nxt else rest
    lines = [l for l in body.split("\n") if l.strip().startswith("|")]
    if len(lines) < 3:
        return [], []
    head = _cells(lines[0])
    rows = []
    for l in lines[2:]:
        c = _cells(l)
        if len(c) != len(head):
            continue
        verdict = _strip(c[-1]).lower().strip()
        rows.append({"dim": c[0], "cells": c[1:-1], "verdict": verdict})
    return head, rows


def mark(cell):
    """2 for ✓, 1 for ⚠, 0 for ✗, None when the lens put no marker."""
    c = (cell or "").strip()
    return MARK.get(c[:1]) if c else None


def _section(md, heading_re):
    """Markdown under the first H2 matching `heading_re`, or ""."""
    m = re.search(r"^##\s+(" + heading_re + r")\s*$", md, re.M | re.I)
    if not m:
        return "", ""
    rest = md[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    return m.group(1).strip(), (rest[:nxt.start()] if nxt else rest).strip()


def _lead_and_note(md):
    """The verdict paragraph and the boxed note above the first H2."""
    head = re.sub(r"^#\s+.*\n", "", md, count=1)
    head = head.split("\n## ")[0]
    note = " ".join(l.lstrip("> ").strip() for l in head.split("\n") if l.startswith(">"))
    paras = [p.strip() for p in re.split(r"\n\s*\n", head) if p.strip() and not p.strip().startswith(">")]
    return (paras[0] if paras else ""), re.sub(r"\*\*", "", note).strip()


def sites_for(run, meta):
    """[{slug, dir, url, role}] — the client's site first, then competitors
    in `compare/index.json` order (or folder order)."""
    roles = run_layout.site_roles(run, meta)
    index = {}
    order = []
    try:
        idx = json.loads(rr._read(os.path.join(run, "compare", "index.json")))
        for s in idx.get("sites") or []:
            if isinstance(s, dict) and s.get("slug"):
                index[s["slug"]] = s
                order.append(s["slug"])
    except (OSError, ValueError):
        pass
    out = []
    for d in run_layout.compare_sites(run):
        slug = d.split("/", 1)[1]
        rec = index.get(slug, {})
        out.append({"slug": slug, "dir": d, "url": rec.get("url") or "",
                    "name": rec.get("name") or "", "role": roles.get(d, "competitor")})
    # A run where the client's own lenses live at the root has no compare/<ours>.
    if not any(s["role"] == "ours" for s in out):
        out.insert(0, {"slug": "ours", "dir": "", "url": meta.get("base_url") or "",
                       "name": meta.get("product_name") or "", "role": "ours"})
    for s in out:
        if not s["url"]:
            # the manifest lists competitor URLs; match by host
            for u in meta.get("competitors") or []:
                if _norm(s["slug"]) in _norm(_host(u)) or _norm(_host(u)).startswith(_norm(s["slug"])):
                    s["url"] = u
                    break
    if order:
        pos = {s: i for i, s in enumerate(order)}
        out.sort(key=lambda s: (s["role"] != "ours", pos.get(s["slug"], len(pos))))
    else:
        out.sort(key=lambda s: s["role"] != "ours")
    return out


def _match_columns(headers, sites, product):
    """Which matrix column each site is. Header 'Ours' or the product name is
    the client's; a competitor's header is matched to its slug or host, else
    taken in order."""
    cols = headers[1:-1]
    taken = set()
    col_of = {}
    for s in sites:
        keys = {_norm(s["slug"]), _norm(_host(s["url"])), _norm(s["name"])}
        if s["role"] == "ours":
            keys |= {"ours", _norm(product)}
        for i, h in enumerate(cols):
            if i in taken:
                continue
            hn = _norm(re.sub(r"\(.*?\)", "", h))
            if s["role"] == "ours" and hn.startswith("ours"):
                col_of[s["slug"]] = i; taken.add(i); break
            if hn and any(k and (k == hn or k in hn or hn in k) for k in keys):
                col_of[s["slug"]] = i; taken.add(i); break
    for s in sites:
        if s["slug"] not in col_of:
            free = [i for i in range(len(cols)) if i not in taken]
            if free:
                col_of[s["slug"]] = free[0]; taken.add(free[0])
    return col_of, cols


def _site_scores(run, site):
    """{lens: {score, why}} from the site's own lens exec-summaries."""
    base = os.path.join(run, site["dir"]) if site["dir"] else run
    out = {}
    if not os.path.isdir(base):
        return out
    for d in sorted(os.listdir(base)):
        if d == "compare" or d.startswith((".", "persona-", "_")):
            continue
        if not os.path.exists(os.path.join(base, d, "findings-final.md")):
            continue
        sc = rr.read_score(run, os.path.join(site["dir"], d) if site["dir"] else d)
        if sc:
            out[d] = sc
    return out


def payload(run, meta):
    """The comparison as a dict for the page's JSON, or None when the run
    has no differences matrix."""
    path = os.path.join(run, "compare", "exec-summary.md")
    if not os.path.exists(path):
        return None
    md = rr._read(path, errors="replace")
    headers, rows = matrix_rows(md)
    if not rows:
        return None

    product = meta.get("product_name") or meta.get("target_slug") or "Ours"
    sites = sites_for(run, meta)
    col_of, cols = _match_columns(headers, sites, product)
    ours = next((s for s in sites if s["role"] == "ours"), None)

    site_out = []
    for s in sites:
        i = col_of.get(s["slug"])
        name = product if s["role"] == "ours" else \
            (re.sub(r"\s*\(.*?\)\s*", "", cols[i]).strip() if i is not None else "") \
            or s["name"] or _host(s["url"]) or s["slug"]
        folder = os.path.join(run, s["dir"]) if s["dir"] else run
        logo = rr.fetch_logo(folder, s["url"]) if s["url"] else ""
        site_out.append({"slug": s["slug"], "name": name, "url": s["url"],
                         "host": _host(s["url"]), "ours": s["role"] == "ours",
                         "logo": logo, "col": i, "scores": _site_scores(run, s)})

    # Which checks ran on every site, so a mean is like for like.
    shared = None
    for s in site_out:
        keys = set(s["scores"])
        shared = keys if shared is None else shared & keys
    shared = sorted(shared or [], key=rr.lens_rank)
    for s in site_out:
        vals = [s["scores"][k]["score"] for k in shared if k in s["scores"]]
        s["mean"] = round(sum(vals) / len(vals), 1) if vals else None

    tally = {v: sum(1 for r in rows if r["verdict"] == v) for v in VERDICTS}

    # Per competitor: the rows where the lens marked them ahead of us, behind
    # us, or level — from the markers, never from the verdict column, which
    # is about the field as a whole.
    oc = col_of.get(ours["slug"]) if ours else None
    for s in site_out:
        if s["ours"] or s["col"] is None or oc is None:
            s["better"], s["worse"], s["same"] = [], [], []
            continue
        better, worse, same = [], [], []
        for r in rows:
            if r["verdict"] == "not comparable":
                continue
            a, b = mark(r["cells"][oc]), mark(r["cells"][s["col"]])
            if a is None or b is None:
                continue
            item = {"dim": r["dim"], "ours": r["cells"][oc], "theirs": r["cells"][s["col"]]}
            (better if b > a else worse if b < a else same).append(item)
        s["better"], s["worse"], s["same"] = better, worse, same

    verdict, note = _lead_and_note(md)
    narrative = []
    for h, body in rr_sections(md):
        key = rr._norm_head(h)
        if not key or key.startswith(("differences matrix", "score")):
            continue
        narrative.append({"title": h, "html": rr.render_markdown(body, {}, {}, "cmp-")})

    return {
        "product": product,
        "verdict": _strip(verdict),
        "note": note,
        "sites": site_out,
        "sharedChecks": shared,
        "checkLabels": {k: rr.lens_label(k) for k in shared},
        "headers": headers,
        "rows": rows,
        "tally": tally,
        "narrative": narrative,
    }


def rr_sections(md):
    parts, cur, buf = [], "", []
    for line in md.split("\n"):
        m = re.match(r"^##\s+(.*)", line)
        if m:
            parts.append((cur, "\n".join(buf).strip()))
            cur, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    parts.append((cur, "\n".join(buf).strip()))
    return parts


def no_score_reason(run, lens_dir="compare"):
    """Why a lens gave no number: the first bullet under its `## Score`
    when no `- **Score:** N/10` line exists. The compare lens writes one."""
    path = os.path.join(run, lens_dir, "exec-summary.md")
    if not os.path.exists(path):
        return ""
    md = rr._read(path, errors="replace")
    if rr.SCORE.search(md):
        return ""
    _, body = _section(md, "Score")
    for l in body.split("\n"):
        l = l.strip()
        if l.startswith(("-", "*")):
            return re.sub(r"\*\*", "", l[1:].strip())
    return ""
