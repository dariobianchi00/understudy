#!/usr/bin/env python3
"""Render a run's markdown into one self-contained HTML file, or a PDF.

    render_report.py <run_folder> --format html|pdf --scope summary|<lens>|all

Markdown in the run folder stays canonical. This produces a *copy* for reading
or forwarding — never the only place a finding lives.

Two design constraints, both deliberate:

**Stdlib only.** Playwright MCP is already a hard prerequisite; adding pandoc or
weasyprint on top would fail for exactly the users least able to fix it. So the
markdown subset understood here is the subset `report-template.md` actually
emits — headings, bullets, ordered lists, tables, blockquotes, fenced code,
bold, inline code, links. Not a general markdown parser and it does not pretend
to be.

**Screenshots are embedded, not linked.** A report whose evidence dies when it
is forwarded is worse than one with no evidence, because it still looks
complete. Each unique image becomes one CSS class holding a data URI, so an
image cited by five findings costs its bytes once.

PDF goes through headless Chromium — Playwright's bundled copy if present, else
a system Chrome. If neither is found the HTML is written and the caller is told
to print it, which is honest rather than silently producing nothing.
"""
import argparse
import base64
import glob
import html
import json
import os
import re
import subprocess
import sys

MAX_EMBED_BYTES = 40 * 1024 * 1024


# ---------------------------------------------------------------- images ----
def find_images(run):
    """Every screenshot in the run, keyed by the paths a report might cite it by."""
    by_key = {}
    for path in glob.glob(os.path.join(run, "**", "*.png"), recursive=True):
        rel = os.path.relpath(path, run)
        by_key[rel] = path
        by_key[os.path.basename(path)] = path      # cited bare
        by_key[rel.replace("persona-", "")] = path  # cited without the prefix
    return by_key


def css_class(rel):
    return "shot-" + re.sub(r"[^a-z0-9]+", "-", rel.lower()).strip("-")


def embed(images_used):
    """One CSS class per unique image, so repeated citations cost bytes once."""
    rules, total = [], 0
    for rel, path in sorted(images_used.items()):
        try:
            raw = open(path, "rb").read()
        except OSError:
            continue
        total += len(raw)
        if total > MAX_EMBED_BYTES:
            print(f"warning: over {MAX_EMBED_BYTES // 1024 // 1024}MB of images — "
                  f"stopped embedding at {rel}", file=sys.stderr)
            break
        uri = "data:image/png;base64," + base64.b64encode(raw).decode()
        rules.append(f".{css_class(rel)}{{background-image:url({uri})}}")
    return "\n".join(rules)


# -------------------------------------------------------------- markdown ----
INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def inline(text, images, used):
    """Escape, then re-introduce the inline markup we support."""
    out = html.escape(text)

    def code(m):
        body = m.group(1)
        # An evidence citation that resolves to a real screenshot becomes a
        # thumbnail as well as a code span — the claim and its proof together.
        key = html.unescape(body)
        hit = images.get(key) or images.get(os.path.basename(key))
        if hit and key.lower().endswith(".png"):
            rel = os.path.relpath(hit, images["__run__"])
            used[rel] = hit
            return (f'<code>{body}</code>'
                    f'<span class="shot {css_class(rel)}" '
                    f'title="{html.escape(rel)}"></span>')
        return f"<code>{body}</code>"

    out = INLINE_CODE.sub(code, out)
    out = BOLD.sub(r"<strong>\1</strong>", out)
    out = ITALIC.sub(r"<em>\1</em>", out)
    out = LINK.sub(r'<a href="\2">\1</a>', out)
    return out


def slug(text, prefix=""):
    s = re.sub(r"<[^>]+>", "", text)
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return f"{prefix}{s[:60]}"


FINDING_H3 = re.compile(r"^###\s+`?([0-9a-f]{6,16}(?:-[a-z])?)`?\s*[—-]\s*(.+?)\s*$")
SEV_BULLET = re.compile(r"^-\s+\*\*Severity:\*\*\s*(P[0-3])", re.M)
SOWHAT = re.compile(r"^-\s+\*\*So what:\*\*\s*(.+?)\s*$", re.M)


def extract_findings(md, prefix):
    """Findings index: id, severity, title, so-what — built from the markdown
    so the reader can triage before reading a single finding."""
    out, lines = [], md.split("\n")
    for n, line in enumerate(lines):
        m = FINDING_H3.match(line)
        if not m:
            continue
        block = "\n".join(lines[n + 1:n + 14])
        sev = SEV_BULLET.search(block)
        so = SOWHAT.search(block)
        out.append({
            "id": m.group(1),
            "title": m.group(2),
            "sev": sev.group(1) if sev else "—",
            "sowhat": so.group(1) if so else "",
            "anchor": slug(m.group(2), prefix),
        })
    return out


def render_markdown(md, images, used, prefix=""):
    lines = md.split("\n")
    html_out, i = [], 0
    list_stack = []            # 'ul' | 'ol'
    in_code = False

    def close_lists(to=0):
        while len(list_stack) > to:
            html_out.append(f"</{list_stack.pop()}>")

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # fenced code
        if stripped.startswith("```"):
            if in_code:
                html_out.append("</code></pre>"); in_code = False
            else:
                close_lists(); html_out.append("<pre><code>"); in_code = True
            i += 1; continue
        if in_code:
            html_out.append(html.escape(line)); i += 1; continue

        if not stripped:
            # A blank line does NOT end a list if the next content is another
            # item — otherwise every "1." after a wrapped entry restarts an <ol>
            # and a Top 3 renders as "1. 1. 1.".
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if not (j < len(lines) and list_stack
                    and re.match(r"^\s*([-*]|\d+\.)\s+", lines[j])):
                close_lists()
            i += 1; continue

        # table — header, separator, rows
        if stripped.startswith("|") and i + 1 < len(lines) and \
                re.fullmatch(r"\|[\s:|-]+\|", lines[i + 1].strip()):
            close_lists()
            head = [c.strip() for c in stripped.strip("|").split("|")]
            html_out.append("<table><thead><tr>" +
                            "".join(f"<th>{inline(c, images, used)}</th>" for c in head) +
                            "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                html_out.append("<tr>" + "".join(
                    f"<td>{inline(c, images, used)}</td>" for c in cells) + "</tr>")
                i += 1
            html_out.append("</tbody></table>")
            continue

        # heading — every one gets an anchor so the contents list can reach it
        m = re.match(r"(#{1,6})\s+(.*)", stripped)
        if m:
            close_lists()
            lvl = len(m.group(1))
            text = m.group(2)
            fm = FINDING_H3.match(stripped)
            if fm:
                anchor = slug(fm.group(2), prefix)
                block = "\n".join(lines[i + 1:i + 14])
                sm = SEV_BULLET.search(block)
                sev = sm.group(1) if sm else ""
                badge = (f'<span class="badge b{sev.lower()}">{sev}</span>' if sev else "")
                html_out.append(
                    f'<h3 id="{anchor}" class="finding">{badge}'
                    f'<span class="fid">{fm.group(1)}</span> '
                    f'{inline(fm.group(2), images, used)}</h3>')
            else:
                html_out.append(f'<h{lvl} id="{slug(text, prefix)}">'
                                f'{inline(text, images, used)}</h{lvl}>')
            i += 1; continue

        # blockquote
        if stripped.startswith(">"):
            close_lists()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip()); i += 1
            html_out.append("<blockquote>" +
                            inline(" ".join(quote), images, used) + "</blockquote>")
            continue

        # horizontal rule
        if re.fullmatch(r"-{3,}", stripped):
            close_lists(); html_out.append("<hr>"); i += 1; continue

        # list items — depth from indentation
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", line)
        if m:
            depth = len(m.group(1)) // 2 + 1
            kind = "ul" if m.group(2) in "-*" else "ol"
            while len(list_stack) > depth:
                html_out.append(f"</{list_stack.pop()}>")
            while len(list_stack) < depth:
                html_out.append(f"<{kind}>"); list_stack.append(kind)
            html_out.append(f"<li>{inline(m.group(3), images, used)}</li>")
            i += 1; continue

        # Indented continuation of the item above — belongs inside that <li>,
        # not in a paragraph that would close the list.
        indent = len(line) - len(line.lstrip())
        if list_stack and indent >= 2 and html_out and html_out[-1].endswith("</li>"):
            html_out[-1] = (html_out[-1][:-len("</li>")] + " " +
                            inline(stripped, images, used) + "</li>")
            i += 1; continue

        close_lists()
        html_out.append(f"<p>{inline(stripped, images, used)}</p>")
        i += 1

    close_lists()
    if in_code:
        html_out.append("</code></pre>")
    return "\n".join(html_out)


# ------------------------------------------------------------------ page ----
CSS = """
:root{--ink:#16181d;--mut:#5d6470;--line:#e3e6ea;--bg:#fff;--accent:#1a56db;
--p0:#b42318;--p1:#c4320a;--p2:#a15c07;--p3:#475467;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;}
.wrap{max-width:830px;margin:0 auto;padding:48px 28px 80px}
h1{font-size:27px;line-height:1.25;margin:0 0 6px;letter-spacing:-.01em}
h2{font-size:19px;margin:38px 0 10px;padding-top:14px;border-top:1px solid var(--line)}
h3{font-size:16px;margin:26px 0 8px}
h1+p{font-size:17px;line-height:1.5;color:var(--ink);margin:0 0 24px;
border-left:3px solid var(--accent);padding-left:14px}
p{margin:.5em 0}
ul,ol{margin:.4em 0;padding-left:22px}
li{margin:.25em 0}
code{font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
background:#f3f4f6;padding:1px 5px;border-radius:4px;word-break:break-word}
pre{background:#f7f8fa;border:1px solid var(--line);border-radius:8px;
padding:12px 14px;overflow-x:auto}
pre code{background:none;padding:0}
blockquote{margin:.6em 0;padding:.4em 0 .4em 14px;border-left:3px solid var(--line);
color:var(--mut);font-style:italic}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px;display:block;
overflow-x:auto}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f7f8fa;font-weight:600}
hr{border:0;border-top:1px solid var(--line);margin:26px 0}
a{color:var(--accent)}
.sev-p0{color:var(--p0)}.sev-p1{color:var(--p1)}
.sev-p2{color:var(--p2)}.sev-p3{color:var(--p3)}
.shot{display:block;width:100%;max-width:400px;aspect-ratio:16/10;margin:8px 0 4px;
border:1px solid var(--line);border-radius:8px;background-size:cover;
background-position:top center;background-repeat:no-repeat}
.doc+.doc{margin-top:56px;padding-top:18px;border-top:3px double var(--line)}
.meta{color:var(--mut);font-size:13px;margin:0 0 30px}
.mut{color:var(--mut);font-weight:400}
/* contents */
.toc{margin:34px 0 8px;padding:18px 22px;background:#f7f8fa;border:1px solid var(--line);
border-radius:10px}
.toc h2{margin:0 0 8px;border:0;padding:0;font-size:16px}
.toc ul{list-style:none;padding-left:0;margin:0}
.toc>ul>li{margin:10px 0;font-weight:600}
.toc .sub{margin:3px 0 0 0;padding-left:14px;font-weight:400;font-size:13.5px;
columns:2;column-gap:26px}
.toc .sub li{margin:1px 0;break-inside:avoid}
.toc a{text-decoration:none}
.toc a:hover{text-decoration:underline}
/* findings index */
h2.idx{margin-top:30px}
table.fidx{font-size:13.5px}
table.fidx td:first-child{width:48px;font-weight:700;text-align:center}
table.fidx td:nth-child(2){font-weight:600}
table.fidx a{text-decoration:none}
tr.rp0 td:first-child{color:var(--p0)}tr.rp1 td:first-child{color:var(--p1)}
tr.rp2 td:first-child{color:var(--p2)}tr.rp3 td:first-child{color:var(--p3)}
/* finding heading */
h3.finding{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;
margin:30px 0 8px;padding-top:8px;border-top:1px solid var(--line)}
.badge{font-size:11px;font-weight:700;letter-spacing:.04em;color:#fff;
padding:2px 7px;border-radius:5px;background:var(--p3)}
.badge.bp0{background:var(--p0)}.badge.bp1{background:var(--p1)}
.badge.bp2{background:var(--p2)}.badge.bp3{background:var(--p3)}
.fid{font:11.5px ui-monospace,Menlo,monospace;color:var(--mut);font-weight:400}
@media print{
  .wrap{max-width:none;padding:0}
  h2{break-after:avoid}h3{break-after:avoid;break-inside:avoid}
  .shot{break-inside:avoid;max-width:330px}
  .toc{break-inside:avoid;background:none}
  h3.finding{break-inside:avoid}
  .badge{color:#000;background:none;border:1px solid currentColor;padding:1px 5px}
  table,blockquote,pre{break-inside:avoid}
  .doc+.doc{break-before:page}
  a{color:inherit;text-decoration:none}
}
@media (prefers-color-scheme:dark){
  :root{--ink:#e6e8ec;--mut:#9aa3b2;--line:#2a2f39;--bg:#14161a;--accent:#7aa2f7;
  --p0:#ff8a80;--p1:#ffab70;--p2:#ffd479;--p3:#a6b0c0;}
  code{background:#1e222a}pre{background:#1a1d23}th{background:#1a1d23}
}
"""


def collect(run, scope):
    """Which markdown files go into the export, in reading order."""
    docs = []
    summary = os.path.join(run, "exec-summary.md")

    def _lens_dirs(base, prefix=""):
        """Lens folders hold findings-final.md. Mode D nests them one level
        deeper under compare/<site>/<lens>/, and compare/ itself is a lens —
        a flat scan misses every one of them and exports an empty report."""
        found = []
        if not os.path.isdir(base):
            return found
        for d in sorted(os.listdir(base)):
            full = os.path.join(base, d)
            if not os.path.isdir(full):
                continue
            if os.path.exists(os.path.join(full, "findings-final.md")):
                found.append(prefix + d)
            # compare/ holds BOTH its own diff report and one folder per site,
            # so it must be recursed into as well as counted — stopping at the
            # first findings-final.md silently drops every per-site lens.
            if d == "compare" or prefix:
                found += _lens_dirs(full, f"{prefix}{d}/")
        return found

    lenses = _lens_dirs(run)

    if scope == "summary":
        if not os.path.exists(summary):
            # A Mode D run may carry its headline at compare/exec-summary.md.
            alt = os.path.join(run, "compare", "exec-summary.md")
            if os.path.exists(alt):
                return [alt] + [os.path.join(run, l, "findings-final.md") for l in lenses]
            sys.exit("no exec-summary.md at the run root or in compare/ — "
                     "the orchestrator writes it; see run.md §3.6")
        # The summary alone is a dead end — a verdict with no route to the
        # findings behind it. Carry every lens's findings file too; the renderer
        # emits their triage tables and drops the detail.
        return [summary] + [os.path.join(run, l, "findings-final.md") for l in lenses]

    if scope == "all":
        if os.path.exists(summary):
            docs.append(summary)
        # Mode D: compare/exec-summary.md is the run's headline when no
        # run-root summary exists, and belongs before the per-site detail.
        cmp_summary = os.path.join(run, "compare", "exec-summary.md")
        if os.path.exists(cmp_summary) and cmp_summary not in docs:
            docs.append(cmp_summary)
        for l in lenses:
            docs += [os.path.join(run, l, "exec-summary.md"),
                     os.path.join(run, l, "findings-final.md")]
        # Preserve order, drop duplicates — compare/exec-summary.md is reachable
        # both as the run headline and as a lens.
        seen, uniq = set(), []
        for d in docs:
            if os.path.exists(d) and d not in seen:
                seen.add(d); uniq.append(d)
        return uniq

    if scope not in lenses:
        sys.exit(f"no lens '{scope}' in this run — found: {', '.join(lenses) or 'none'}")
    return [p for p in (os.path.join(run, scope, "exec-summary.md"),
                        os.path.join(run, scope, "findings-final.md"))
            if os.path.exists(p)]


def write_dense_markdown(run, docs):
    """One dense markdown carrying everything — the canonical report.

    The per-lens files stay as they are (each lens owns its own deliverable),
    but a reader who wants the whole run should not have to open seven files
    and reconstruct the order. This is that file, and every export is rendered
    from the same content.
    """
    parts = []
    for path in docs:
        rel = os.path.relpath(path, run)
        parts.append(f"<!-- source: {rel} -->\n\n"
                     + open(path, errors="replace").read().rstrip() + "\n")
    out = os.path.join(run, "report-full.md")
    with open(out, "w") as f:
        f.write("\n\n---\n\n".join(parts))
    return out


def find_chromium():
    pats = [
        os.path.expanduser("~/Library/Caches/ms-playwright/chromium-*/chrome-mac/"
                           "Chromium.app/Contents/MacOS/Chromium"),
        os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    ]
    for p in pats:
        hits = sorted(glob.glob(p))
        if hits:
            return hits[-1]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_folder")
    ap.add_argument("--format", default="html", choices=["html", "pdf"])
    ap.add_argument("--scope", default="all",
                    help="summary | all | <lens name>")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    run = os.path.expanduser(a.run_folder.rstrip("/"))
    if not os.path.isdir(run):
        sys.exit(f"not a directory: {run}")

    title = os.path.basename(run)
    try:
        m = json.load(open(os.path.join(run, "manifest.json")))
        title = f"{m.get('product_name') or m.get('target_slug')} — understudy"
        subtitle = (f"run {m.get('run_id')} · {(m.get('started_utc') or '')[:10]}"
                    f" · traversal {m.get('models', {}).get('traversal', '?')}")
    except Exception:
        subtitle = ""

    images = find_images(run)
    images["__run__"] = run
    used = {}

    # The dense markdown is written on every invocation, whatever the scope —
    # it is the canonical report, and an export is always a view of it.
    dense = write_dense_markdown(run, collect(run, "all"))

    docs = collect(run, a.scope)
    body, toc = [], []

    for n, path in enumerate(docs):
        md = open(path, errors="replace").read()
        prefix = f"d{n}-"
        rel = os.path.relpath(path, run)

        # Section title for the contents list
        h1 = re.search(r"^#\s+(.*)", md, re.M)
        label = h1.group(1) if h1 else rel
        entry = {"anchor": slug(label, prefix), "label": label, "sub": [], "find": []}
        for h2 in re.findall(r"^##\s+(.*)", md, re.M):
            entry["sub"].append({"anchor": slug(h2, prefix), "label": h2})
        entry["find"] = extract_findings(md, prefix)
        toc.append(entry)

        # summary scope: a lens contributes its triage table only, never detail
        if a.scope == "summary" and n > 0:
            if not entry["find"]:
                continue
            lens_name = os.path.basename(os.path.dirname(path))
            rows = "".join(
                f'<tr class="r{f["sev"].lower()}"><td>{f["sev"]}</td>'
                f'<td>{html.escape(f["title"])}</td>'
                f'<td>{html.escape(f["sowhat"])}</td></tr>'
                for f in sorted(entry["find"], key=lambda x: x["sev"]))
            body.append(
                f'<section class="doc" id="{entry["anchor"]}">'
                f'<h2 id="{slug(lens_name, prefix)}">{html.escape(lens_name)} '
                f'— {len(entry["find"])} findings</h2>'
                f'<table class="fidx"><thead><tr><th>Sev</th><th>Finding</th>'
                f'<th>So what</th></tr></thead><tbody>{rows}</tbody></table>'
                f'<p class="mut">Full detail, evidence and repro steps: '
                f'<code>{lens_name}/findings-final.md</code> in the run folder, '
                f'or the complete export.</p></section>')
            entry["sub"] = []
            continue

        rendered = render_markdown(md, images, used, prefix)

        # A findings file gets a triage table before the findings themselves —
        # severity and cost at a glance, so nobody reads 20 findings to learn
        # which 3 matter.
        if entry["find"]:
            rows = "".join(
                f'<tr class="r{f["sev"].lower()}"><td>{f["sev"]}</td>'
                f'<td><a href="#{f["anchor"]}">{html.escape(f["title"])}</a></td>'
                f'<td>{html.escape(f["sowhat"])}</td></tr>'
                for f in sorted(entry["find"], key=lambda x: x["sev"]))
            index = ('<h2 class="idx">Findings at a glance</h2><table class="fidx">'
                     '<thead><tr><th>Sev</th><th>Finding</th><th>So what</th></tr>'
                     f'</thead><tbody>{rows}</tbody></table>')
            marker = '<h3 id="' + entry["find"][0]["anchor"] + '"'
            rendered = rendered.replace(marker, index + marker, 1)

        body.append(f'<section class="doc" id="{entry["anchor"]}">{rendered}</section>')

    # Contents — after the first document (the exec summary), never before it.
    if len(docs) > 1:
        items = []
        for e in toc[1:] if len(toc) > 1 else toc:
            subs = "".join(f'<li><a href="#{s["anchor"]}">{html.escape(s["label"])}</a></li>'
                           for s in e["sub"][:6])
            count = (f' <span class="mut">— {len(e["find"])} findings</span>'
                     if e["find"] else "")
            items.append(f'<li><a href="#{e["anchor"]}">{html.escape(e["label"])}</a>'
                         f'{count}<ul class="sub">{subs}</ul></li>')
        contents = ('<nav class="toc"><h2 id="contents">Contents</h2><ul>'
                    + "".join(items) + "</ul></nav>")
        body.insert(1, contents)

    page = (f"<!doctype html><html><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(title)}</title><style>{CSS}\n{embed(used)}</style>"
            f"</head><body><div class=wrap>"
            f"<p class=meta>{html.escape(subtitle)}</p>"
            + "\n".join(body) + "</div></body></html>")

    stem = a.out or os.path.join(run, f"report-{a.scope}")
    html_path = stem if stem.endswith(".html") else stem + ".html"
    with open(html_path, "w") as f:
        f.write(page)

    if a.format == "html":
        print(html_path)
        print(f"canonical markdown: {dense}", file=sys.stderr)
        return 0

    chrome = find_chromium()
    pdf_path = re.sub(r"\.html$", ".pdf", html_path)
    if not chrome:
        print(html_path)
        print("PDF skipped: no Chromium or Chrome found. The HTML above is "
              "print-ready — open it and use Print → Save as PDF.", file=sys.stderr)
        return 0
    try:
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf_path}", f"file://{os.path.abspath(html_path)}"],
            check=True, capture_output=True, timeout=180)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(html_path)
        print(f"PDF generation failed ({type(e).__name__}). The HTML above is "
              f"print-ready — open it and use Print → Save as PDF.", file=sys.stderr)
        return 0
    print(pdf_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
