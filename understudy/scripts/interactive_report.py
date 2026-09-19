#!/usr/bin/env python3
"""
interactive_report.py — pack a run into the interactive HTML report.

`render_report.py --format html` calls `build()` with the run it has already
parsed; this module turns that into one self-contained page: the template in
`report_template.html` with a JSON payload and the screenshots (downscaled)
embedded. The page is for presenting the run — a dashboard that drills into
findings, personas and profiles, a guided full-screen walkthrough, a
screenshot lightbox, a session replay per persona, and browser-side triage
with export. The printed PDF stays a document; this is the same evidence as
an instrument.

Nothing here scores, ranks or rewrites. Every number is read from the lens
files; every quote and screenshot is the run's own. The template is data-
driven so that a run from any product renders without a code change, and the
JS holds no product knowledge.

Design rules, all binding:
  * One file, no network. Screenshots and the logo are data URIs; there is no
    CDN, font or script fetched at open time. A report handed to a client
    must open on a plane.
  * Degrade, never die. Pillow missing → full-size PNGs. No logo → no logo.
    A lens file missing a field → the field is blank in the UI.
  * The markdown stays canonical. The gate checks the .md; this renders it.
"""

import base64
import html
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_report as rr  # noqa: E402

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report_template.html")

# Screenshots are embedded downscaled: a 1440×900 PNG is ~600 KB, a 1280-wide
# JPEG of the same screen ~120 KB, and a run has 40–80 of them. Full-size
# copies stay in the run folder; the lightbox shows these.
SHOT_MAX_W = 1280
SHOT_JPEG_Q = 72
EMBED_CAP = 60 * 1024 * 1024


# ------------------------------------------------------------- images ----
def shrink(path):
    """(data_uri, w, h) for a screenshot, downscaled when Pillow is present."""
    try:
        from PIL import Image  # noqa: WPS433
    except Exception:
        Image = None
    raw = rr._read(path, "rb")
    if Image is None:
        return "data:image/png;base64," + base64.b64encode(raw).decode(), 0, 0
    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
        w, h = im.size
        if w > SHOT_MAX_W:
            nh = round(h * SHOT_MAX_W / w)
            im = im.resize((SHOT_MAX_W, nh), Image.LANCZOS)
            w, h = im.size
        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1])
            im = bg
        elif im.mode != "RGB":
            im = im.convert("RGB")
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=SHOT_JPEG_Q, optimize=True, progressive=True)
        out = buf.getvalue()
        if len(out) >= len(raw):            # a flat UI PNG can already be smaller
            return "data:image/png;base64," + base64.b64encode(raw).decode(), w, h
        return "data:image/jpeg;base64," + base64.b64encode(out).decode(), w, h
    except Exception:
        return "data:image/png;base64," + base64.b64encode(raw).decode(), 0, 0


def accent_from_logo(run):
    """The site's accent colour, from its icon — the one branding signal a
    run always has. Falls back to the report's own blue."""
    default = "#1a56db"
    path = next((os.path.join(run, rr.LOGO_STEM + e) for e in rr.LOGO_MIME
                 if os.path.exists(os.path.join(run, rr.LOGO_STEM + e))), None)
    if not path or path.endswith(".svg"):
        return default
    try:
        from PIL import Image
        im = Image.open(path).convert("RGBA").resize((48, 48))
        best, score = None, 0
        for r, g, b, a in im.getdata():
            if a < 200:
                continue
            mx, mn = max(r, g, b), min(r, g, b)
            sat = 0 if mx == 0 else (mx - mn) / mx
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if sat < 0.35 or lum > 215 or lum < 25:
                continue
            s = sat * (1 - abs(lum - 128) / 128)
            if s > score:
                best, score = (r, g, b), s
        if not best:
            return default
        r, g, b = best
        # Text on white must stay readable: pull a light accent down.
        while 0.2126 * r + 0.7152 * g + 0.0722 * b > 150:
            r, g, b = int(r * .85), int(g * .85), int(b * .85)
        return "#%02x%02x%02x" % (r, g, b)
    except Exception:
        return default


# ----------------------------------------------------------- markdown ----
def md_sections(md):
    """[(h2 text, body markdown)] for a document, in order. Text before the
    first H2 is returned under the key ""."""
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


def md_table(body):
    """Rows of the first markdown table in `body`, as lists of cell strings."""
    lines = [l for l in body.split("\n") if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    head = [c.strip() for c in lines[0].strip().strip("|").split("|")]
    rows = []
    for l in lines[2:]:
        rows.append([c.strip() for c in l.strip().strip("|").split("|")])
    return head, rows


def md_bullets(body):
    return [re.sub(r"^\s*[-*]\s+", "", l).strip() for l in body.split("\n")
            if re.match(r"^\s*[-*]\s+", l)]


def strip_md(text):
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", text or "")
    t = re.sub(r"`([^`]+)`", r"\1", t)
    return t.strip()


def to_html(md, images, used, prefix=""):
    return rr.render_markdown(md, images, used, prefix)


# ----------------------------------------------------------- findings ----
FIELD = re.compile(r"^-\s+\*\*([^*]+?):\*\*\s*(.*)$")


def parse_finding_block(block):
    """Every `- **Field:** value` bullet of a finding, with nested bullets as
    lists, plus the persona quotes and the screenshots it cites."""
    fields, order = {}, []
    cur = None
    for line in block.split("\n"):
        m = FIELD.match(line)
        if m:
            cur = m.group(1).strip()
            fields[cur] = {"text": m.group(2).strip(), "items": []}
            order.append(cur)
            continue
        if cur and re.match(r"^\s{2,}-\s+", line):
            fields[cur]["items"].append(re.sub(r"^\s+-\s+", "", line).strip())
        elif cur and re.match(r"^\s{2,}\d+\.\s+", line):
            fields[cur]["items"].append(re.sub(r"^\s+\d+\.\s+", "", line).strip())
    quotes = [q.strip() for q in rr.PERSONA_QUOTE.findall(block)]
    ev = fields.get("Evidence", {}).get("text", "") + " " + " ".join(fields.get("Evidence", {}).get("items", []))
    shots = re.findall(r"[\w\-./]+\.png", ev)
    logs = re.findall(r"[\w\-./]*(?:session\.log|persona-debrief\.md|findings-raw\.json):[\d,\-]+", ev)
    return fields, order, quotes, shots, logs


def findings_for(entry, images, used):
    """Full findings for one lens entry, keyed to the parsed summaries
    render_report already produced (ids, anchors, clusters)."""
    md = entry["md"]
    lines = md.split("\n")
    out = []
    starts = [(n, rr.FINDING_H3.match(l)) for n, l in enumerate(lines)]
    starts = [(n, m) for n, m in starts if m]
    for k, (n, m) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        block = "\n".join(lines[n + 1:end])
        fields, order, quotes, shots, logs = parse_finding_block(block)
        shot_keys = []
        for s in shots:
            hit = images.get(s) or images.get(os.path.basename(s))
            if hit:
                rel = os.path.relpath(hit, images["__run__"])
                used[rel] = hit
                if rel not in shot_keys:
                    shot_keys.append(rel)
        personas = [p.strip() for p in re.split(r"[,·]", fields.get("Personas hit", {}).get("text", "")) if p.strip()]
        out.append({
            "id": m.group(1),
            "title": m.group(2),
            "lens": entry["dir"],
            "lensLabel": entry["lens"],
            "sev": fields.get("Severity", {}).get("text", "")[:2] or "—",
            "sowhat": strip_md(fields.get("So what", {}).get("text", "")),
            "flow": strip_md(fields.get("Flow", {}).get("text", "")),
            "locator": strip_md(fields.get("Locator", {}).get("text", "")),
            "tags": strip_md(fields.get("Framework tags", {}).get("text", "")),
            "personas": personas,
            "observed": [strip_md(x) for x in fields.get("Observed", {}).get("items", [])] or
                        ([strip_md(fields["Observed"]["text"])] if fields.get("Observed", {}).get("text") else []),
            "evidence": strip_md(fields.get("Evidence", {}).get("text", "")),
            "logs": logs,
            "quotes": quotes,
            "repro": [strip_md(x) for x in fields.get("Repro", {}).get("items", [])],
            "fix": strip_md(fields.get("Fix", {}).get("text", "")),
            "shots": shot_keys,
            "extra": {k: strip_md(v["text"]) for k, v in fields.items()
                      if k not in ("Severity", "So what", "Flow", "Locator", "Framework tags",
                                   "Personas hit", "Observed", "Evidence", "Repro", "Fix")
                      and v["text"]},
        })
    return out


# ------------------------------------------------------------ personas ----
LOG_LINE = re.compile(r"^\[(\d\d:\d\d|pre-session|capture(?: note)?|shape \d)\]\s*(.*)$")


def persona_payload(run, name, images, used):
    pdir = os.path.join(run, f"persona-{name}")
    if not os.path.isdir(pdir):
        return None
    shots = sorted(f for f in os.listdir(os.path.join(pdir, "screenshots"))
                   if f.lower().endswith(".png")) if os.path.isdir(os.path.join(pdir, "screenshots")) else []
    shot_rels = []
    for f in shots:
        rel = os.path.join(f"persona-{name}", "screenshots", f)
        used[rel] = os.path.join(pdir, "screenshots", f)
        shot_rels.append(rel)
    idx_by_num = {}
    for rel in shot_rels:
        mm = re.match(r"(\d+)", os.path.basename(rel))
        if mm:
            idx_by_num.setdefault(int(mm.group(1)), rel)

    reactions = []
    try:
        raw = json.loads(rr._read(os.path.join(pdir, "findings-raw.json"), errors="replace"))
        items = raw.get("reactions", raw) if isinstance(raw, dict) else raw
        for r in items or []:
            if not isinstance(r, dict):
                continue
            shot = r.get("screenshot") or r.get("screen") or ""
            shot_rel = ""
            if shot:
                hit = images.get(shot) or images.get(os.path.basename(shot)) \
                    or images.get(os.path.join(f"persona-{name}", "screenshots", os.path.basename(shot)))
                if hit:
                    shot_rel = os.path.relpath(hit, run)
            reactions.append({"t": r.get("at") or r.get("t") or "",
                              "text": r.get("what") or r.get("reaction") or "",
                              "where": r.get("where") or r.get("screen") or "",
                              "feeling": r.get("feeling") or "",
                              "flow": r.get("flow") or "",
                              "shot": shot_rel})
    except Exception:
        pass

    log = []
    try:
        cur_shot = shot_rels[0] if shot_rels else ""
        react_by_t = {}
        for r in reactions:
            if r["shot"] and r["t"]:
                react_by_t.setdefault(r["t"], r["shot"])
        for line in rr._read(os.path.join(pdir, "session.log"), errors="replace").split("\n"):
            m = LOG_LINE.match(line.strip())
            if not m:
                if log and line.strip():
                    log[-1]["text"] += " " + line.strip()
                continue
            t, text = m.group(1), m.group(2)
            # Which screen was on when this line was written: an explicit
            # "Screenshot NN" / "NN-name.png" mention wins, then a reaction
            # logged at the same time, then whatever was showing before.
            mm = re.search(r"\b(\d\d)-[\w\-]+\.png", text) or \
                re.search(r"[Ss]creenshots?\s+(\d\d)\b", text)
            if mm and int(mm.group(1)) in idx_by_num:
                cur_shot = idx_by_num[int(mm.group(1))]
            elif t in react_by_t:
                cur_shot = react_by_t[t]
            log.append({"t": t, "text": text, "shot": cur_shot})
    except Exception:
        pass

    timeline = {}
    try:
        timeline = json.loads(rr._read(os.path.join(pdir, "timeline.json"), errors="replace"))
    except Exception:
        pass
    debrief = ""
    try:
        debrief = to_html(re.sub(r"^#\s+.*\n", "", rr._read(os.path.join(pdir, "persona-debrief.md"), errors="replace"), count=1),
                          images, used, f"p-{name}-")
    except Exception:
        pass
    return {"name": name, "dir": f"persona-{name}", "shots": shot_rels, "reactions": reactions,
            "log": log, "timeline": timeline, "debrief": debrief}


def persona_facts(p, manifest_p):
    """A few plain facts for the persona card, from timeline.json whichever
    capture shape wrote it."""
    t = p.get("timeline") or {}
    facts = {"device": (manifest_p or {}).get("device") or t.get("device") or ""}
    kind = "journey" if "shape_1" in t or "shape_2" in t else ("visit" if "shape_v1" in t else "")
    facts["kind"] = kind
    if kind == "journey":
        s2 = t.get("shape_2") or {}
        facts["firstValue"] = s2.get("first_value_reached")
        facts["ttfv"] = s2.get("seconds_to_first_value")
        facts["what"] = s2.get("first_value") or ""
    elif kind == "visit":
        s1 = t.get("shape_v1") or {}
        facts["comprehension"] = s1.get("time_to_comprehension_seconds")
        facts["who"] = s1.get("understood_who")
        s3 = t.get("shape_v3") or {}
        facts["priceFound"] = s3.get("price_found")
        facts["verdict"] = (t.get("shape_v4") or {}).get("verdict") or ""
    facts["leftEarly"] = t.get("left_early")
    facts["minutes"] = t.get("session_end_minutes")
    facts["note"] = t.get("device_note") or (t.get("shape_0") or {}).get("note") or ""
    return facts


# --------------------------------------------------------------- build ----
def build(run, meta, entries, images, used, a_scope, logo_uri, provenance):
    """The interactive page as a string. `entries` is render_report's parsed
    list (summary first, lenses after, LENS_ORDER applied, clusters marked)."""
    summary = entries[0]
    lenses = [e for e in entries[1:] if e.get("ours", True)]

    # ---- run-level sections, both as HTML and as structure -----------------
    secs = md_sections(summary["md"])
    sec_html, sec_struct = {}, {}
    for h, body in secs:
        key = rr._norm_head(h)
        if not key:
            continue
        sec_html[key] = to_html(body, images, used, "s-")
        head, rows = md_table(body)
        sec_struct[key] = {"title": h, "head": head, "rows": rows,
                           "bullets": md_bullets(body),
                           "lead": next((l.strip() for l in body.split("\n")
                                         if l.strip() and not l.strip().startswith(("|", "-", "*", "#"))), "")}

    def sec(*names):
        for n in names:
            for k in sec_struct:
                if k.startswith(n):
                    return sec_struct[k], sec_html.get(k, "")
        return None, ""

    top5_s, top5_h = sec("top 5")
    quotes_s, _ = sec("in their own words")
    buyer_s, buyer_h = sec("what a buyer could")
    well_s, _ = sec("what the site does well", "what the product does well", "what works")
    limits_s, limits_h = sec("limits of this assessment", "limits")
    what_s, what_h = sec("what this is")
    how_s, how_h = sec("how it was produced")
    checks_s, _ = sec("what each check looked for")
    objectives_s, objectives_h = sec("objectives")

    top5 = []
    for r in (top5_s or {}).get("rows", []):
        if len(r) >= 5:
            top5.append({"n": r[0], "sev": strip_md(r[1])[:2], "what": strip_md(r[2]),
                         "cost": strip_md(r[3]), "effort": strip_md(r[4])})
    verdict = (top5_s or {}).get("lead", "")

    quotes = []
    for r in (quotes_s or {}).get("rows", []):
        if len(r) >= 3:
            where = r[3] if len(r) > 3 else ""
            shots = []
            for tok in re.split(r"\s+·\s+", where):
                tok = tok.strip("` ")
                hit = images.get(tok) or images.get(os.path.basename(tok))
                if hit and tok.lower().endswith(".png"):
                    rel = os.path.relpath(hit, run)
                    used[rel] = hit
                    shots.append(rel)
            top = re.search(r"Top\s*5\s*(?:[·,—-]\s*)?row\s*(\d+)", where, re.I)
            quotes.append({"who": strip_md(r[0]), "when": strip_md(r[1]),
                           "text": strip_md(r[2]).strip("“”\""), "shots": shots,
                           "top5": int(top.group(1)) if top else None,
                           "where": strip_md(where)})

    checks = {}
    for r in (checks_s or {}).get("rows", []):
        if len(r) >= 2:
            checks[strip_md(r[0]).lower()] = strip_md(r[1])

    # ---- lenses and findings -------------------------------------------------
    lens_payload, findings = [], []
    for e in lenses:
        sc = e.get("score") or {}
        fs = findings_for(e, images, used)
        by_id = {f["id"]: f for f in e["find"]}
        for f in fs:
            f["cluster"] = by_id.get(f["id"], {}).get("cluster")
        findings += fs
        # the lens's own verdict = first paragraph of its exec summary
        verdict_l = ""
        try:
            verdict_l = rr.first_verdict(rr._read(os.path.join(run, e["dir"], "exec-summary.md"), errors="replace")) \
                if hasattr(rr, "first_verdict") else ""
        except Exception:
            pass
        if not verdict_l:
            try:
                md = rr._read(os.path.join(run, e["dir"], "exec-summary.md"), errors="replace")
                body = re.sub(r"^#\s+.*\n", "", md, count=1).strip()
                verdict_l = body.split("\n\n")[0].strip()
            except Exception:
                verdict_l = ""
        lens_payload.append({
            "dir": e["dir"], "label": e["lens"],
            "score": sc.get("score"), "why": rr.sentence(sc.get("why", "")),
            "verdict": strip_md(verdict_l),
            "looksFor": checks.get(e["lens"].lower(), ""),
            "count": len(fs),
            "sev": {s: sum(1 for f in fs if f["sev"] == s) for s in ("P0", "P1", "P2", "P3")},
        })
    scored = [l["score"] for l in lens_payload if isinstance(l.get("score"), int)]
    overall = round(sum(scored) / len(scored), 1) if scored else None

    clusters = []
    try:
        for c in rr.corroboration_clusters(entries):
            clusters.append({"sev": c["sev"], "title": c["rep"]["title"],
                             "ids": [m["id"] for m in c["members"]],
                             "raised": [f"{l} {s}" for l, s in c["raised"]]})
    except Exception:
        pass

    # ---- ICP profiles ----------------------------------------------------------
    icp_html, icp_struct = "", None
    body = rr.lifted_section(run, "icp", "ICP profiles")
    if body:
        import icp_profiles
        icp_html = icp_profiles.cards_html(body, run=run)
        icp_struct = icp_profiles.parse(body, run)

    # ---- personas ------------------------------------------------------------
    personas = []
    manifest_people = {p.get("name"): p for p in (meta.get("personas") or []) if isinstance(p, dict)}
    names = list(manifest_people.keys())
    for d in sorted(os.listdir(run)):
        if d.startswith("persona-") and os.path.isdir(os.path.join(run, d)) and d[8:] not in names:
            names.append(d[8:])
    for n in names:
        p = persona_payload(run, n, images, used)
        if not p:
            continue
        p["facts"] = persona_facts(p, manifest_people.get(n))
        # A finding belongs to the persona whose screenshots it cites; the
        # name in "Personas hit" is the fallback, because on a *both* run the
        # visit and the journey share a name and only the folder tells them
        # apart.
        def hits(f):
            dirs = {s.split("/")[0] for s in f["shots"] if s.startswith("persona-")}
            if dirs:
                return f"persona-{n}" in dirs
            return n in f["personas"]
        p["findings"] = [f["id"] for f in findings if hits(f)]
        p["timeline"] = {k: v for k, v in (p.get("timeline") or {}).items()
                         if k in ("shape_0", "shape_1", "shape_2", "shape_2b", "shape_3",
                                  "shape_v1", "shape_v2", "shape_v3", "shape_v_icp", "shape_v4",
                                  "why_stopped", "left_early", "cap_hit", "session_end_minutes",
                                  "device", "device_note")}
        personas.append(p)

    # ---- images ------------------------------------------------------------
    img = {}
    total = 0
    for rel, path in sorted(used.items()):
        try:
            uri, w, h = shrink(path)
        except OSError:
            continue
        total += len(uri)
        if total > EMBED_CAP:
            print(f"warning: over {EMBED_CAP // 1024 // 1024}MB of images — stopped at {rel}",
                  file=sys.stderr)
            break
        img[rel] = {"src": uri, "w": w, "h": h}

    counts = {s: sum(1 for f in findings if f["sev"] == s) for s in ("P0", "P1", "P2", "P3")}
    data = {
        "meta": {
            "product": meta.get("product_name") or meta.get("target_slug") or "",
            "url": meta.get("base_url", ""),
            "kind": rr.ASSESSMENT_LABEL.get(meta.get("assessment_type", ""), "Assessment"),
            "date": rr.human_date(meta.get("started_utc")),
            "runId": meta.get("run_id", ""),
            "version": meta.get("understudy_version", ""),
            "personaMode": meta.get("persona_mode", ""),
            "conversionGoal": meta.get("conversion_goal", ""),
            "traversalModel": (meta.get("models") or {}).get("traversal", ""),
            "scoringModels": (meta.get("models") or {}).get("scoring", {}),
            "provenance": provenance,
            "scope": a_scope,
            "logo": logo_uri,
            "accent": accent_from_logo(run),
        },
        "overall": overall,
        "verdict": strip_md(verdict),
        "counts": counts,
        "nFindings": len(findings),
        "nProblems": len(findings) - sum(len(c["ids"]) - 1 for c in clusters),
        "sections": {
            "whatThisIs": what_h, "howProduced": how_h, "top5": top5_h,
            "buyer": buyer_h, "limits": limits_h, "objectives": objectives_h,
        },
        "top5": top5,
        "quotes": quotes,
        "doesWell": [strip_md(b) for b in (well_s or {}).get("bullets", [])],
        "limits": [strip_md(b) for b in (limits_s or {}).get("bullets", [])],
        "lenses": lens_payload,
        "findings": findings,
        "clusters": clusters,
        "icp": icp_html,
        "icpProfiles": (icp_struct or {}).get("profiles", []),
        "icpTrap": (icp_struct or {}).get("trap", {}),
        "personas": personas,
        "images": img,
    }

    tpl = rr._read(TEMPLATE)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = tpl.replace("/*__DATA__*/null", payload, 1)
    page = page.replace("__TITLE__", html.escape(f"{data['meta']['product']} — understudy report"))
    from icp_profiles import CSS as icp_css
    page = page.replace("/*__ICP_CSS__*/", icp_css, 1)
    return page
