#!/usr/bin/env python3
"""
icp_profiles.py — the ICP profiles as cards, for the PDF and the interactive
report alike.

The icp lens writes each profile as a dozen named bullets under
`## ICP profiles` (agents/lens-icp.md). Rendering that markdown as-is gives
a wall of bullets, and the screenshot references inside it become thumbnails
that add nothing — the profile is an inference, not an observation. This
module parses the section into structure and renders each profile as a card:
a generated face, a name, the one-line "who", then the details.

Two rules:
  * The face is drawn, never fetched — a deterministic SVG from the profile's
    name, so the same profile looks the same on every render and no real
    person is ever pictured. The name is the lens's `Meet:` line when it
    wrote one, else a fixed placeholder name chosen by the same hash, and the
    card says it is invented either way.
  * No screenshots. Citations stay as text; nothing in a profile card is a
    thumbnail.

Both renderers call `cards_html()`; the interactive report also gets the
parsed structure for its Present mode.
"""

import base64
import hashlib
import html
import os
import re
import urllib.parse
import urllib.request

# The illustrated faces come from DiceBear's "Open Peeps" set (Pablo Stanley,
# CC BY 4.0 — the section note credits it). Fetched once per profile at render
# time and cached in the run folder, so a re-render needs no network; if the
# first render is offline the drawn silhouette below stands in.
AVATAR_STYLE = os.environ.get("UNDERSTUDY_AVATAR_STYLE", "open-peeps")
AVATAR_QUERY = {
    "open-peeps": "face=smile,smileBig,cute,calm,cheeky,driven,explaining&accessoriesProbability=25"
                  "&maskProbability=0&backgroundColor=dbe4ff,d9f2e6,fde8d8,ece4ff,fff4cc&radius=22&size=240",
}
AVATAR_CREDIT = {"open-peeps": "Faces: Open Peeps by Pablo Stanley (CC BY 4.0), via DiceBear."}

PROFILE_H3 = re.compile(r"^###\s+(\d+)\.\s+(.*?)\s+[—–-]\s+(PRIMARY|EXPANSION|NEXT-BEST|SECOND PRIMARY)"
                        r"\s*·\s*fit\s*([\d.?]+)\s*·\s*propensity\s*([\d.?]+)\s*$", re.I | re.M)
TRAP_H3 = re.compile(r"^###\s+The trap\s+[—–-]\s+(.*?)\s*$", re.M)
CAND_H3 = re.compile(r"^###\s+Candidates considered\s*$", re.M)
FIELD = re.compile(r"^-\s+\*\*([^*]+?):\*\*\s*(.*)$")

# Fixed, obviously-placeholder names: a profile without a `Meet:` line still
# gets a face and a name, and a reader can tell at a glance it was assigned,
# not researched. Pairs are gender-neutral-ish and international on purpose.
FIRST = ["Alex", "Sam", "Noor", "Jun", "Ida", "Luca", "Maya", "Tomás", "Priya", "Elias",
         "Aiko", "Omar", "Lena", "Kai", "Sofia", "Rafael", "Hana", "Mateo", "Nia", "Jonas",
         "Zara", "Theo", "Amara", "Ravi"]
LAST = ["Okafor", "Lindqvist", "Haddad", "Moreau", "Tanaka", "Silva", "Novak", "Mensah",
        "Kowalski", "Rossi", "Nguyen", "Fischer", "Almeida", "Petrov", "Duarte", "Iyer"]
PALETTE = [("#1a56db", "#7aa7ff"), ("#0f766e", "#5eead4"), ("#7c3aed", "#c4b5fd"),
           ("#b45309", "#fcd34d"), ("#be123c", "#fda4af"), ("#166534", "#86efac"),
           ("#0e7490", "#67e8f9"), ("#6d28d9", "#a78bfa")]


def _h(s):
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16)


def placeholder_name(seed):
    n = _h(seed)
    return f"{FIRST[n % len(FIRST)]} {LAST[(n // 7) % len(LAST)]}"


def fetch_avatar(name, seed, run):
    """An illustrated face as a data URI, cached at <run>/icp/avatars/. "" when
    the network is not there and nothing is cached — the caller falls back."""
    if not run:
        return ""
    d = os.path.join(run, "icp", "avatars")
    key = hashlib.md5(f"{AVATAR_STYLE}|{seed}".encode()).hexdigest()[:12]
    path = os.path.join(d, f"{key}.svg")
    if not os.path.exists(path):
        q = AVATAR_QUERY.get(AVATAR_STYLE, "radius=22&size=240")
        url = (f"https://api.dicebear.com/9.x/{AVATAR_STYLE}/svg?seed="
               f"{urllib.parse.quote(seed)}&{q}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "understudy report renderer"})
            with urllib.request.urlopen(req, timeout=8) as r:
                raw = r.read(400_000)
            if not raw.lstrip().startswith(b"<svg"):
                return ""
            os.makedirs(d, exist_ok=True)
            with open(path, "wb") as f:
                f.write(raw)
        except Exception:
            return ""
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError:
        return ""
    return "data:image/svg+xml;base64," + base64.b64encode(raw).decode()


def avatar_html(name, seed, run):
    uri = fetch_avatar(name, seed, run)
    if uri:
        return f'<img class="icp-avatar" src="{uri}" alt="{html.escape(name)}" width="110" height="110">'
    return avatar_svg(name, seed, 110)


def avatar_svg(name, seed, size=88):
    """A face for the card: gradient tile, a white head-and-shoulders
    silhouette, the person's initials. Deterministic from `seed`."""
    n = _h(seed)
    c1, c2 = PALETTE[n % len(PALETTE)]
    words = re.findall(r"[A-Za-zÀ-ÿ]+", name)
    initials = ("".join(w[0] for w in words[:2]) if len(words) > 1 else (words[0][:2] if words else "?")).upper()
    gid = "g" + hashlib.md5(seed.encode()).hexdigest()[:8]
    return (f'<svg class="icp-avatar" width="{size}" height="{size}" viewBox="0 0 100 100" '
            f'role="img" aria-label="{html.escape(name)}">'
            f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
            f'<rect width="100" height="100" rx="22" fill="url(#{gid})"/>'
            f'<circle cx="50" cy="38" r="17" fill="#fff" fill-opacity=".92"/>'
            f'<path d="M18 92c2-22 15-32 32-32s30 10 32 32z" fill="#fff" fill-opacity=".92"/>'
            f'<rect x="58" y="60" width="34" height="22" rx="11" fill="#16181d" fill-opacity=".72"/>'
            f'<text x="75" y="75.5" text-anchor="middle" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" '
            f'font-size="12" font-weight="700" fill="#fff">{html.escape(initials)}</text></svg>')


# ------------------------------------------------------------------ parse ----
def _fields(block):
    fields, cur, yaml_lines, in_yaml = {}, None, [], False
    for line in block.split("\n"):
        if line.strip().startswith("```"):
            in_yaml = not in_yaml
            continue
        if in_yaml:
            yaml_lines.append(line.strip())
            continue
        m = FIELD.match(line)
        if m:
            cur = m.group(1).strip()
            fields[cur] = {"text": m.group(2).strip(), "items": []}
            continue
        if cur and re.match(r"^\s{2,}-\s+", line):
            fields[cur]["items"].append(re.sub(r"^\s+-\s+", "", line).strip())
    return fields, "\n".join(l for l in yaml_lines if l)


def _strip(t):
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t or "")
    t = t.replace("`", "")          # citations stay, as plain text
    return t.strip()


def _get(fields, *names):
    for n in names:
        for k, v in fields.items():
            if k.lower().startswith(n.lower()):
                return v
    return {"text": "", "items": []}


def parse(body, run=None):
    """Structure from the markdown under `## ICP profiles`. With `run`, each
    profile carries an illustrated face (fetched and cached there)."""
    heads = list(PROFILE_H3.finditer(body))
    trap = TRAP_H3.search(body)
    cand = CAND_H3.search(body)
    profiles = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else \
            min(x for x in (trap.start() if trap else len(body), cand.start() if cand else len(body)))
        block = body[m.end():end]
        f, yaml = _fields(block)
        title = _strip(m.group(2))
        meet = _strip(_get(f, "Meet").get("text", ""))
        name = meet.split(",")[0].split("—")[0].strip() if meet else placeholder_name(title)
        profiles.append({
            "n": int(m.group(1)), "title": title, "role": m.group(3).upper(),
            "fit": m.group(4), "propensity": m.group(5),
            "name": name, "meet": meet, "invented": not meet,
            "who": _strip(_get(f, "Who").get("text", "")),
            "find": _strip(_get(f, "Find fifty").get("text", "")),
            "job": _strip(_get(f, "Job to be done").get("text", "")),
            "trigger": _strip(_get(f, "Trigger").get("text", "")),
            "wins": [_strip(x) for x in _get(f, "Why this product wins").get("items", [])] or
                    ([_strip(_get(f, "Why this product wins").get("text", ""))] if _get(f, "Why this product wins").get("text") else []),
            "lacks": [_strip(x) for x in _get(f, "What it lacks").get("items", [])] or
                     ([_strip(_get(f, "What it lacks").get("text", ""))] if _get(f, "What it lacks").get("text") else []),
            "fitLine": _strip(_get(f, "Fit").get("text", "")),
            "propLine": _strip(_get(f, "Propensity").get("text", "")),
            "against": [_strip(x) for x in _get(f, "Case against").get("items", [])],
            "notInferable": _strip(_get(f, "Not inferable").get("text", "")),
            "rerun": yaml,
            "avatar": avatar_html(name, title, run),
        })
    trap_txt = ""
    trap_title = ""
    if trap:
        trap_title = _strip(trap.group(1))
        seg_end = cand.start() if cand and cand.start() > trap.end() else len(body)
        trap_txt = _strip(body[trap.end():seg_end])
    cand_rows, cand_head = [], []
    if cand:
        lines = [l for l in body[cand.end():].split("\n") if l.strip().startswith("|")]
        if len(lines) >= 2:
            cand_head = [c.strip() for c in lines[0].strip().strip("|").split("|")]
            cand_rows = [[_strip(c.strip()) for c in l.strip().strip("|").split("|")] for l in lines[2:]]
    return {"profiles": profiles, "trap": {"title": trap_title, "text": trap_txt},
            "candidates": {"head": cand_head, "rows": cand_rows}}


# ----------------------------------------------------------------- render ----
def _score_bar(line, label):
    """`pain 4 · alignment 4 · evidence 3 · clarity 5 → 4.0` as small bars."""
    if not line:
        return ""
    parts = re.findall(r"([A-Za-z][A-Za-z ]*?)\s+([\d.]+|\?)", line.split("→")[0])
    total = re.search(r"→\s*([\d.]+)", line)
    cells = "".join(
        f'<div class="icp-bar"><span>{html.escape(k.strip())}</span>'
        f'<i><b style="width:{0 if v == "?" else min(100, float(v) * 20)}%"></b></i><em>{html.escape(v)}</em></div>'
        for k, v in parts)
    return (f'<div class="icp-scores"><div class="icp-scores-h">{label}'
            f'{f" <strong>{html.escape(total.group(1))}</strong>" if total else ""}</div>{cells}</div>')


def card_html(p, open_details=False):
    li = lambda xs: "".join(f"<li>{html.escape(x)}</li>" for x in xs)
    meet = html.escape(p["meet"]) if p["meet"] else \
        f'{html.escape(p["name"])} <span class="icp-inv">(placeholder name)</span>'
    det = " open" if open_details else ""
    return f'''<div class="icp-card icp-{p["role"].lower().replace(" ", "-")}">
  <div class="icp-head">{p["avatar"]}
    <div><div class="icp-role">{html.escape(p["role"])} · fit {html.escape(p["fit"])} · propensity {html.escape(p["propensity"])}</div>
      <h3 class="icp-title">{p["n"]}. {html.escape(p["title"])}</h3>
      <div class="icp-meet">{meet}</div></div></div>
  <p class="icp-who">{html.escape(p["who"])}</p>
  <dl class="icp-dl">
    <dt>Job to be done</dt><dd>{html.escape(p["job"])}</dd>
    <dt>Trigger</dt><dd>{html.escape(p["trigger"])}</dd>
    <dt>Find fifty of them</dt><dd>{html.escape(p["find"])}</dd>
  </dl>
  <div class="icp-two">
    <div><h4>Why this product wins for them</h4><ul>{li(p["wins"]) or "<li>—</li>"}</ul></div>
    <div><h4>What it lacks for them</h4><ul>{li(p["lacks"]) or "<li>nothing observed</li>"}</ul></div>
  </div>
  <div class="icp-two">{_score_bar(p["fitLine"], "Fit")}{_score_bar(p["propLine"], "Propensity")}</div>
  {f'<div class="icp-against"><h4>The case against — reasoning, not evidence</h4><ul>{li(p["against"])}</ul></div>' if p["against"] else ""}
  {f'<p class="icp-ni"><b>Not inferable from this run:</b> {html.escape(p["notInferable"])}</p>' if p["notInferable"] else ""}
  {f'<details class="icp-rerun"{det}><summary>Re-run persona</summary><pre>{html.escape(p["rerun"])}</pre></details>' if p["rerun"] else ""}
</div>'''


def cards_html(body, open_details=False, run=None):
    """The whole section: three cards, the trap, the candidates table.
    `open_details` expands the re-run persona blocks — for print, where a
    collapsed <details> is simply missing."""
    d = parse(body, run)
    if not d["profiles"]:
        return ""
    out = ['<div class="icp-cards">' + "".join(card_html(p, open_details) for p in d["profiles"]) + "</div>"]
    if d["trap"]["title"]:
        out.append(f'<div class="icp-trap"><h3>The trap — {html.escape(d["trap"]["title"])}</h3>'
                   f'<p>{html.escape(d["trap"]["text"])}</p></div>')
    c = d["candidates"]
    if c["rows"]:
        out.append('<h3>Candidates considered</h3><table class="icp-cand"><thead><tr>'
                   + "".join(f"<th>{html.escape(h)}</th>" for h in c["head"]) + "</tr></thead><tbody>"
                   + "".join("<tr>" + "".join(f"<td>{html.escape(x)}</td>" for x in r) + "</tr>" for r in c["rows"])
                   + "</tbody></table>")
    credit = AVATAR_CREDIT.get(AVATAR_STYLE, "") if any("<img" in p["avatar"] for p in d["profiles"]) else ""
    out.append('<p class="icp-note">The faces and names are illustrations chosen for the report; '
               'no real person is pictured or described. Profiles are inferred from the recorded '
               f'sessions only. {credit}</p>')
    return "\n".join(out)


CSS = """
.icp-cards{display:grid;gap:16px;margin:8px 0 18px}
.icp-card{border:1px solid #e3e6ea;border-radius:14px;padding:18px 20px;background:#fff}
.icp-head,.icp-scores,.icp-trap,.icp-bar{break-inside:avoid}
.icp-primary{border-color:#1a56db;box-shadow:inset 4px 0 0 #1a56db}
.icp-head{display:flex;gap:18px;align-items:center;margin-bottom:12px}
.icp-avatar{flex:none;width:110px;height:110px;border-radius:22px}
.icp-role{font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:#5d6470}
.icp-title{margin:2px 0 4px;font-size:18px}
.icp-meet{font-size:14px;color:#16181d;font-weight:600}
.icp-inv{font-weight:400;color:#5d6470;font-size:12px}
.icp-who{font-size:15px;margin:4px 0 12px}
.icp-dl{display:grid;grid-template-columns:130px 1fr;gap:4px 12px;margin:0 0 12px;font-size:13.5px}
.icp-dl dt{color:#5d6470;font-weight:600}.icp-dl dd{margin:0}
.icp-two{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:0 0 10px}
.icp-two h4,.icp-against h4{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#5d6470;margin:0 0 4px}
.icp-two ul,.icp-against ul{margin:0;padding-left:18px;font-size:13.5px}
.icp-scores-h{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#5d6470;margin-bottom:4px}
.icp-scores-h strong{color:#16181d;font-size:14px;letter-spacing:0;text-transform:none}
.icp-bar{display:grid;grid-template-columns:86px 1fr 26px;gap:8px;align-items:center;font-size:12.5px;margin:2px 0}
.icp-bar i{display:block;height:6px;background:#eceff3;border-radius:3px;overflow:hidden}
.icp-bar b{display:block;height:100%;background:#1a56db}
.icp-bar em{font-style:normal;text-align:right;color:#5d6470}
.icp-against{background:#f7f9fc;border-radius:10px;padding:10px 14px;margin:8px 0}
.icp-ni{font-size:13px;color:#5d6470;margin:8px 0 0}
.icp-rerun summary{cursor:pointer;font-size:13px;color:#1a56db;margin-top:8px}
.icp-rerun pre{font-size:12px;background:#f7f9fc;padding:10px;border-radius:8px;white-space:pre-wrap}
.icp-trap{border:1px dashed #c4620a;border-radius:12px;padding:12px 16px;margin:0 0 16px;background:#fff8f2}
.icp-trap h3{margin:0 0 4px;font-size:15px;color:#c4620a}.icp-trap p{margin:0;font-size:14px}
.icp-cand{font-size:13px}
.icp-note{font-size:12px;color:#5d6470}
@media (max-width:760px){.icp-two{grid-template-columns:1fr}.icp-dl{grid-template-columns:1fr}}
@media print{section.icp-section{break-before:page}.icp-card{break-before:auto}.icp-card+.icp-card{break-before:page}}
"""
