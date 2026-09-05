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

**No page numbers in the PDF footer, deliberately.** Measured 2026-09-05:
Chromium ignores CSS page-margin boxes (`@bottom-center{content:counter(page)}`
produces nothing), and its own header/footer stamps the `file://` URL of the
source — a filesystem path in a client deliverable, which §7 forbids. A custom
footer needs CDP, which needs a websocket client the stdlib does not have.
So sections and findings are numbered in the flow instead (1., 1.4). That is
stable across paper sizes and zoom, which a page number is not, and it is what
a reader cites in a meeting anyway.
"""
import argparse
import base64
import difflib
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


def human_date(iso):
    """`2026-09-04T10:01:19+00:00` -> `4 September 2026`."""
    if not iso:
        return ""
    try:
        y, mo, d = int(iso[:4]), int(iso[5:7]), int(iso[8:10])
    except (ValueError, IndexError):
        return iso[:10]
    months = ("January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December")
    return f"{d} {months[mo - 1]} {y}"


def image_class(key, images, used):
    """CSS class for a cited screenshot, registering it for embedding."""
    hit = images.get(key) or images.get(os.path.basename(key))
    if not hit:
        return ""
    rel = os.path.relpath(hit, images["__run__"])
    used[rel] = hit
    return css_class(rel)


ASSESSMENT_LABEL = {"website": "Website assessment",
                    "product": "Product assessment",
                    "both": "Website and product assessment"}


def cover(meta, title, subtitle, n_find, counts, overall=None, provenance=""):
    """A title page, because the deliverable is read by someone who was not
    in the room when it was commissioned — and it carries the caveat that
    everything else depends on (§4, persona fork; §11.2)."""
    product = meta.get("product_name") or meta.get("target_slug") or title
    kind = ASSESSMENT_LABEL.get(meta.get("assessment_type", ""), "Assessment")
    rows = []

    def row(dt, dd):
        if dd:
            rows.append(f"<dt>{html.escape(dt)}</dt><dd>{html.escape(str(dd))}</dd>")

    website = meta.get("assessment_type") == "website"
    row("Scope", meta.get("base_url"))
    people = meta.get("personas") or []
    row("Simulated buyers" if website else "Simulated users",
        ", ".join(p.get("name", "") for p in people))
    row("Devices", ", ".join(sorted({p.get("device", "") for p in people if p.get("device")})))
    row("Checks applied", ", ".join(lens_label(o) for o in meta.get("objectives") or []))
    if n_find:
        sev = " · ".join(f"{counts[k]} {k}" for k in ("P0", "P1", "P2", "P3") if counts[k])
        row("Findings", f"{n_find} — {sev}")
    row("Conversion goal", meta.get("conversion_goal"))
    # "logged out" is only known to be true for a website assessment (§3). A
    # product run signs in, and claiming otherwise on the cover is a factual
    # error about the method on the first page of the report.
    row("Method", "Automated traversal in a live browser"
        + (", logged out" if website else ""))
    row("Prepared with", f"understudy v{meta.get('understudy_version', '')}".rstrip(" v"))

    headline = ""
    if overall is not None:
        hue = ("var(--p0)" if overall <= 3 else "var(--p1)" if overall <= 5
               else "var(--p2)" if overall <= 7 else "#2f855a")
        headline = (f'<p class="scorehead">Overall score</p>'
                    f'<p class="scorebig" style="color:{hue}">{overall}<span '
                    f'class="mut" style="font-size:20px">/10</span></p>')

    caveat = ""
    if meta.get("persona_mode") == "generic":
        who = "buyers" if website else "users"
        thing = "site" if website else "product"
        caveat = (f'<p class="caveat"><strong>The {who} in this assessment were '
                  f'constructed, not researched.</strong> No customer of this '
                  f'{thing} was interviewed or observed. This report shows what a '
                  f'capable first-time {"visitor" if website else "user"} can and '
                  f'cannot work out from the {thing}; it does not show what actual '
                  f'customers do.</p>')

    return (f'<section class="cover">'
            f'<p class="kicker">{html.escape(kind)}</p>'
            f'<h1>{html.escape(product)}</h1>'
            f'<p class="sub">{html.escape(subtitle)}</p>'
            f'{headline}<dl>{"".join(rows)}</dl>{caveat}'
            f'<p class="meta prov">{html.escape(provenance)}</p></section>')


def slug(text, prefix=""):
    s = re.sub(r"<[^>]+>", "", text)
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return f"{prefix}{s[:60]}"


FINDING_H3 = re.compile(r"^###\s+`?([0-9a-f]{6,16}(?:-[a-z])?)`?\s*[—-]\s*(.+?)\s*$")
SEV_BULLET = re.compile(r"^-\s+\*\*Severity:\*\*\s*(P[0-3])", re.M)
SOWHAT = re.compile(r"^-\s+\*\*So what:\*\*\s*(.+?)\s*$", re.M)
FIX = re.compile(r"^-\s+\*\*Fix:\*\*\s*(.+?)\s*$", re.M)
EVIDENCE = re.compile(r"^-\s+\*\*Evidence:\*\*\s*(.+?)\s*$", re.M)
LOCATOR = re.compile(r"^-\s+\*\*Locator:\*\*\s*(.+?)\s*$", re.M)
# `- **Score:** 4/10 — <why>` in a lens exec-summary. The lens that read the
# evidence assigns it; check_report.py refuses a score its own severities
# contradict.
SCORE = re.compile(r"^-\s+\*\*Score:\*\*\s*(\d{1,2})\s*/\s*10\s*[—–-]?\s*(.*?)\s*$", re.M)
# Verbatim site copy a finding quotes. Two lenses quoting the same string are
# almost always describing the same thing — see corroborate().
QUOTED = re.compile(r'"([^"]{12,90})"')

# Lens folder names are code identifiers. A client reads a name, not a slug.
LENS_LABELS = {
    "ux": "Usability",
    "bugs": "Defects",
    "onboarding": "Activation",
    "content": "Content",
    "clarity": "Clarity",
    "conversion": "Conversion",
    "trust": "Trust and credibility",
    "technical": "Performance and delivery",
    "seo": "Search visibility",
    "aeo": "Answer-engine readiness",
    "compare": "Competitive comparison",
}
SEV_WEIGHT = {"P0": 1000, "P1": 100, "P2": 10, "P3": 1}
SEV_EMOJI = {"P0": "\U0001F534", "P1": "\U0001F7E0",
             "P2": "\U0001F7E1", "P3": "\u26AA"}

# ⚑ Reading order is FIXED, not computed. It was severity-weighted for a day;
# a reader who cannot predict where a section lives has to consult the index
# for every jump, and two runs of the same site produced different orders,
# which made them impossible to read side by side. The order below runs from
# what a visitor meets first to what only a machine sees, and the run summary's
# own "what each check looked for" table uses it too — the two disagreeing is
# what the order exists to prevent.
LENS_ORDER = ["clarity", "conversion", "trust", "compare", "seo", "aeo",
              "technical", "ux", "bugs", "onboarding", "content"]


def lens_rank(name):
    tail = name.rpartition("/")[2]
    return (LENS_ORDER.index(tail) if tail in LENS_ORDER else len(LENS_ORDER), name)


def sev_cell(sev):
    """Severity as it appears in every table: emoji, bold, coloured."""
    return (f'<span class="sevchip s{sev.lower()}">{SEV_EMOJI.get(sev, "")} '
            f'<strong>{sev}</strong></span>')


def lens_label(name):
    """Human name for a lens folder, keeping any Mode-D `compare/<site>` prefix."""
    head, _, tail = name.rpartition("/")
    label = LENS_LABELS.get(tail, tail.replace("-", " ").capitalize())
    site = head[len("compare/"):] if head.startswith("compare/") else head
    return f"{label} — {site.rstrip('/')}" if site else label


def extract_findings(md, prefix):
    """Findings index: id, severity, title, so-what — built from the markdown
    so the reader can triage before reading a single finding."""
    out, lines = [], md.split("\n")
    for n, line in enumerate(lines):
        m = FINDING_H3.match(line)
        if not m:
            continue
        # A finding runs to the next H3 or the end; the fix bullet is last, so
        # a fixed lookahead would miss it on any finding with long repro steps.
        end = len(lines)
        for k in range(n + 1, len(lines)):
            if FINDING_H3.match(lines[k]):
                end = k
                break
        block = "\n".join(lines[n + 1:end])
        sev = SEV_BULLET.search(block)
        so = SOWHAT.search(block)
        fix = FIX.search(block)
        ev = EVIDENCE.search(block)
        loc = LOCATOR.search(block)
        out.append({
            "id": m.group(1),
            "title": m.group(2),
            "sev": sev.group(1) if sev else "—",
            "sowhat": so.group(1) if so else "",
            "fix": fix.group(1) if fix else "",
            "shot": first_shot(ev.group(1)) if ev else "",
            "locator": loc.group(1).strip("`") if loc else "",
            "quotes": {q.lower() for q in QUOTED.findall(m.group(2) + " " + block)},
            "anchor": slug(m.group(2), prefix),
        })
    return out


def first_shot(evidence):
    """The first screenshot an Evidence bullet cites, if any."""
    m = re.search(r"`?([^`\s]+\.png)`?", evidence)
    return m.group(1) if m else ""


def read_score(run, lens_dir):
    """The 0-10 score a lens gave itself, with its reason."""
    path = os.path.join(run, lens_dir, "exec-summary.md")
    if not os.path.exists(path):
        return None
    m = SCORE.search(open(path, errors="replace").read())
    if not m:
        return None
    return {"score": max(0, min(10, int(m.group(1)))), "why": m.group(2).strip()}


def score_table(entries, run):
    """Per-check scores and the overall, or "" when no lens published one.

    The overall is computed here and never authored, so the number on the cover
    and the number in the table cannot disagree — and a reader who adds up the
    rows gets the figure the report shows.
    """
    rows, vals = [], []
    for e in entries[1:]:
        sc = e.get("score")
        if not sc:
            continue
        vals.append(sc["score"])
        hue = ("var(--p0)" if sc["score"] <= 3 else "var(--p1)" if sc["score"] <= 5
               else "var(--p2)" if sc["score"] <= 7 else "#2f855a")
        rows.append(
            f'<tr><td><strong>{html.escape(e["lens"])}</strong></td>'
            f'<td>{sc["score"]}/10<span class="bar">'
            f'<i style="width:{sc["score"] * 10}%;background:{hue}"></i></span></td>'
            f'<td>{html.escape(sc["why"])}</td></tr>')
    if not rows:
        return "", None
    overall = round(sum(vals) / len(vals), 1)
    rows.append(f'<tr class="overall"><td>Overall</td><td>{overall}/10</td>'
                f'<td>Mean of the {len(vals)} checks above, each weighted equally.</td></tr>')
    return ('<table class="scores"><thead><tr><th>Check</th><th>Score</th>'
            f'<th>Why that score</th></tr></thead><tbody>{"".join(rows)}</tbody>'
            '</table>', overall)


def _norm_head(t):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"<[^>]+>", "", t).lower()).strip()


def has_section(exec_secs, names):
    return any(_norm_head(t) in names for _, _, t in exec_secs)


def number_exec_sections(html_str, exec_secs):
    """Prefix every H2 of the run summary with its section number, in order."""
    it = iter(exec_secs)

    def sub(m):
        try:
            no, _, _ = next(it)
        except StopIteration:
            return m.group(0)
        return f'{m.group(1)}<span class="secno">{no}.</span> {m.group(2)}</h2>'

    return re.sub(r"(<h2\b[^>]*>)(.*?)</h2>", sub, html_str)


def fill_section(html_str, exec_secs, names, payload):
    """Drop generated content immediately under a heading the summary declared.

    The summary writes `## Contents` and `## How each area scores` and leaves
    them empty; the index and the score table are built from what actually ran,
    so neither can contradict the document it sits in.
    """
    for no, anchor_id, text in exec_secs:
        if _norm_head(text) not in names:
            continue
        m = re.search(r"<h2\b[^>]*id=\"" + re.escape(anchor_id) + r"\"[^>]*>.*?</h2>",
                      html_str)
        if m:
            return html_str[:m.end()] + payload + html_str[m.end():]
    return html_str


def build_index(exec_secs, entries, scope, matrix_no=None):
    """The document's index: every top-level section, numbered and linked.

    Rendered as real anchors, which Chromium turns into PDF GoTo annotations —
    verified 2026-09-05 — so the index is clickable in the exported PDF and not
    only in the HTML.
    """
    items = []
    for no, anchor_id, text in exec_secs:
        items.append(f'<li><span class="secno">{no}.</span> '
                     f'<a href="#{anchor_id}">{html.escape(re.sub(r"<[^>]+>", "", text))}</a></li>')
    for e in entries[1:]:
        label = e["lens"] if (scope == "summary" and e["find"]) else e["label"]
        count = (f' <span class="mut">— {len(e["find"])} findings</span>'
                 if e["find"] else "")
        items.append(f'<li><span class="secno">{e["secno"]}.</span> '
                     f'<a href="#{e["anchor"]}">{html.escape(label)}</a>{count}</li>')
    if matrix_no:
        items.append(f'<li><span class="secno">{matrix_no}.</span> '
                     f'<a href="#site-by-site">Site-by-site comparison</a></li>')
    return f'<ul class="idxlist">{"".join(items)}</ul>'


VERDICT_WORDS = ("leads", "trails", "level", "not comparable")


def comparison_section(run, meta, images, used, prefix="cmp-"):
    """The compare lens's differences matrix, lifted whole.

    The matrix is a contract (`agents/lens-compare.md`): a `## Differences
    matrix` heading followed by one table whose first column is the dimension,
    whose middle columns are one site each, and whose last is the verdict. It
    is the only place in the run where the competitors' own observed values
    exist side by side — the run summary's "Against comparable sites" carries
    only our column — so a report that omits it answers "how do we look next to
    them?" with half the evidence.

    Lifted rather than re-authored: re-typing a matrix built from four captures
    is how a number changes between two pages of one document.
    """
    path = os.path.join(run, "compare", "exec-summary.md")
    if not os.path.exists(path):
        return ""
    md = open(path, errors="replace").read()
    m = re.search(r"^##\s+Differences matrix\s*$", md, re.M)
    if not m:
        return ""
    rest = md[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    body = rest[:nxt.start()] if nxt else rest
    if "|" not in body:
        return ""

    # "Ours" is how the lens addresses the user's site; the client reads a name.
    product = meta.get("product_name") or meta.get("target_slug") or "Ours"
    body = re.sub(r"\|\s*Ours\s*\([^)]*\)\s*\|", f"| {product} |", body, count=1)
    body = re.sub(r"\|\s*Ours\s*\|", f"| {product} |", body, count=1)

    out = render_markdown(body, images, used, prefix)
    out = out.replace("<table>", '<table class="matrix">', 1)
    for w in VERDICT_WORDS:
        out = out.replace(f"<strong>{w}</strong>",
                          f'<span class="vd v{w.split()[0]}">{w}</span>')
    return out


def corroborate(toc):
    """Mark findings that two or more lenses raised independently.

    Nothing is merged, re-scored or dropped — §11.5 keeps lens reports
    standalone, and §11.8 warns that normalising hard enough to collide two
    phrasings also collides two genuinely different findings. This only
    annotates, so a false pair costs a misleading footnote, not a lost finding.

    Two signals, either sufficient:
      * the same verbatim quoted string (>=12 chars) — site copy both lenses
        transcribed, the strongest evidence they are looking at one thing;
      * a normalised title similarity >=0.62 at the same locator.
    """
    flat = [(e, f) for e in toc[1:] for f in e["find"]]
    for _, f in flat:
        f["also"] = set()
    for i, (ei, fi) in enumerate(flat):
        for ej, fj in flat[i + 1:]:
            if ei is ej:
                continue
            same_quote = bool(fi["quotes"] & fj["quotes"])
            same_place = (fi["locator"] and fi["locator"] == fj["locator"]
                          and _similar(fi["title"], fj["title"]) >= 0.62)
            if same_quote or same_place:
                fi["also"].add(ej["lens"])
                fj["also"].add(ei["lens"])
    return [f for _, f in flat if f["also"]]


_STOP = {"the", "a", "an", "is", "are", "was", "on", "in", "of", "to", "it", "its",
         "and", "or", "that", "this", "any", "anywhere", "appears", "only",
         "never", "not", "no", "site", "page", "product", "user", "with", "for"}


def _norm_title(t):
    t = re.sub(r"[^a-z0-9 ]", " ", t.lower())
    return " ".join(w for w in t.split() if w not in _STOP)


def _similar(a, b):
    return difflib.SequenceMatcher(None, _norm_title(a), _norm_title(b)).ratio()


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
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;
vertical-align:top;overflow-wrap:break-word}
th{background:#f7f8fa;font-weight:600}
hr{border:0;border-top:1px solid var(--line);margin:26px 0}
a{color:var(--accent)}
.sev-p0{color:var(--p0)}.sev-p1{color:var(--p1)}
.sev-p2{color:var(--p2)}.sev-p3{color:var(--p3)}
.shot{display:block;width:100%;max-width:400px;aspect-ratio:16/10;margin:8px 0 4px;
border:1px solid var(--line);border-radius:8px;background-size:cover;
background-position:top center;background-repeat:no-repeat}
.doc+.doc{margin-top:30px}
.doc>h2:first-child{margin-top:22px}
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
.idxlist{list-style:none;padding-left:0;margin:10px 0}
.idxlist li{margin:7px 0;font-size:14.5px}
.idxlist a{text-decoration:none;font-weight:600}
.idxlist .secno{display:inline-block;min-width:26px}
/* findings index */
h2.idx{margin-top:30px}
table.fidx{font-size:13.5px;table-layout:fixed}
table.fidx td:first-child,table.fidx th:first-child{width:58px;
text-align:center;overflow-wrap:normal}
table.fidx td:first-child{font-weight:700}
table.fidx th:nth-child(2),table.fidx td:nth-child(2){width:33%}
table.fidx th:nth-child(3),table.fidx td:nth-child(3){width:29%}
table.corr th:nth-child(2),table.corr td:nth-child(2){width:52%}
table.corr th:nth-child(3),table.corr td:nth-child(3){width:auto}
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
/* cover */
.cover{min-height:80vh;display:flex;flex-direction:column;justify-content:center}
.cover .kicker{font-size:12px;letter-spacing:.12em;text-transform:uppercase;
color:var(--mut);margin:0 0 18px}
.cover h1{font-size:38px;line-height:1.15;margin:0 0 14px}
.cover .sub{font-size:19px;color:var(--mut);margin:0 0 34px;border:0;padding:0}
.cover dl{display:grid;grid-template-columns:170px 1fr;gap:7px 18px;margin:0;
font-size:14px;border-top:1px solid var(--line);padding-top:20px}
.cover dt{color:var(--mut)}
.cover dd{margin:0}
.cover .prov{margin:26px 0 0;font-size:12px}
.cover .caveat{margin:30px 0 0;padding:12px 16px;border-left:3px solid var(--p1);
background:#fdf6f3;font-size:13.5px;color:var(--ink)}
/* severity roll-up */
.tally{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 6px;padding:0;list-style:none}
.tally li{border:1px solid var(--line);border-radius:8px;padding:8px 14px;font-size:13px;
min-width:78px}
.tally b{display:block;font-size:21px;line-height:1.2;font-weight:700}
.tally .l0 b{color:var(--p0)}.tally .l1 b{color:var(--p1)}
.tally .l2 b{color:var(--p2)}.tally .l3 b{color:var(--p3)}
/* evidence figures */
.ev{display:flex;flex-wrap:wrap;gap:16px;margin:16px 0 4px}
.ev figure{margin:0;flex:1 1 300px;max-width:390px}
.ev .shot{background-size:contain;background-color:#fbfbfc;aspect-ratio:16/11}
.ev figcaption{font-size:12.5px;color:var(--mut);margin-top:5px;line-height:1.45}
.ev .sev{font-weight:700}
/* cross-lens corroboration */
.also{display:block;font-weight:400;font-size:12px;color:var(--mut);margin-top:3px}
table.corr td:first-child{width:48px;font-weight:700;text-align:center}
.secno{color:var(--mut);font-weight:400}
/* site-by-site matrix */
table.matrix{font-size:11.5px;line-height:1.42}
table.matrix th,table.matrix td{padding:5px 8px}
table.matrix th:first-child,table.matrix td:first-child{width:20%;font-weight:600}
table.matrix th:nth-child(2),table.matrix td:nth-child(2){background:#f4f7fb}
table.matrix th:nth-child(2){font-weight:700}
.vd{font-weight:700;text-transform:uppercase;font-size:11px;letter-spacing:.04em;
white-space:nowrap}
.vd.vleads{color:#2f855a}.vd.vtrails{color:var(--p0)}
.vd.vlevel{color:var(--mut)}.vd.vnot{color:var(--mut)}
/* severity chip — emoji + bold + colour, identical in every table */
.sevchip{white-space:nowrap;font-size:12.5px;
font-family:"Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",inherit}
.sevchip strong{font-family:inherit}
.sevchip.sp0 strong{color:var(--p0)}.sevchip.sp1 strong{color:var(--p1)}
.sevchip.sp2 strong{color:var(--p2)}.sevchip.sp3 strong{color:var(--p3)}
/* scores */
table.scores td:nth-child(2){font-weight:700;text-align:center;white-space:nowrap}
table.scores th:nth-child(2){text-align:center}
tr.overall{background:#f7f8fa}
tr.overall td{border-top:2px solid var(--ink);font-weight:700}
.bar{display:inline-block;width:74px;height:7px;border-radius:4px;
background:var(--line);vertical-align:middle;margin-left:8px;overflow:hidden}
.bar i{display:block;height:100%;border-radius:4px}
.scorehead{font-size:15px;color:var(--mut);margin:0 0 4px}
.scorebig{font-size:34px;font-weight:700;line-height:1.1;margin:0 0 20px}
@page{size:A4;margin:16mm 15mm 18mm}
/* A four-site matrix is unreadable squeezed into portrait width. Chromium
   honours named pages with their own orientation — verified 2026-09-05. */
@page wide{size:A4 landscape;margin:14mm}
@media print{
  .wrap{max-width:none;padding:0 2px 0 0}
  h2{break-after:avoid}h3{break-after:avoid;break-inside:avoid}
  .shot{break-inside:avoid;max-width:330px}
  .toc{break-inside:avoid;background:none}
  h3.finding{break-inside:avoid}
  .badge{color:#000;background:none;border:1px solid currentColor;padding:1px 5px}
  .sevchip{white-space:nowrap}
  blockquote,pre{break-inside:avoid}
  /* A table must be allowed to split, or a long one strands a whole page.
     Rows stay atomic and the header repeats, so a continuation is readable
     on its own. `display:block` (screen-only, for horizontal scroll) would
     defeat table-header-group, so it is reset here. */
  table{display:table;break-inside:auto}
  thead{display:table-header-group}
  tfoot{display:table-footer-group}
  tbody tr{break-inside:avoid;break-after:auto}
  /* Lens sections flow. Forcing a page per lens cost ~3.5 blank pages in 15
     on the first client run; the running header is what tells a reader where
     they are, not a page break. */
  .doc{break-before:auto}
  .doc>h2{break-before:auto}
  .doc.wide{page:wide;break-before:page}
  .cover{break-after:page;min-height:auto;display:block;padding-top:34mm}
  .cover .caveat{background:none}
  .ev figure{break-inside:avoid}
  .tally{break-inside:avoid}
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
    meta, subtitle, provenance = {}, "", ""
    try:
        meta = json.load(open(os.path.join(run, "manifest.json")))
        title = f"{meta.get('product_name') or meta.get('target_slug')} — understudy"
        subtitle = human_date(meta.get("started_utc"))
        provenance = (f"run {meta.get('run_id')} · traversal model "
                      f"{meta.get('models', {}).get('traversal', '?')}")
    except Exception:
        pass

    images = find_images(run)
    images["__run__"] = run
    used = {}

    # The dense markdown is written on every invocation, whatever the scope —
    # it is the canonical report, and an export is always a view of it.
    dense = write_dense_markdown(run, collect(run, "all"))

    docs = collect(run, a.scope)

    # Pass 1 — parse every document, so lenses can be ordered by what they
    # found. Rendering happens in pass 2, after that order is known.
    entries = []
    for n, path in enumerate(docs):
        md = open(path, errors="replace").read()
        prefix = f"d{n}-"
        rel = os.path.relpath(path, run)
        h1 = re.search(r"^#\s+(.*)", md, re.M)
        label = h1.group(1) if h1 else rel
        lens = os.path.relpath(os.path.dirname(path), run)
        entries.append({
            "anchor": slug(label, prefix), "label": label, "md": md,
            "prefix": prefix, "path": path,
            "dir": lens if n > 0 else "",
            "lens": lens_label(lens) if n > 0 else label,
            "sub": [{"anchor": slug(h2, prefix), "label": h2}
                    for h2 in re.findall(r"^##\s+(.*)", md, re.M)],
            "find": extract_findings(md, prefix),
            "score": read_score(run, lens) if n > 0 else None,
        })

    # Reading order for the lens sections — LENS_ORDER, always.
    head, tail = entries[:1], sorted(entries[1:], key=lambda e: lens_rank(e["dir"]))
    entries = head + tail
    toc = entries

    # ---- section numbers, fixed before anything is rendered ----------------
    # The exec summary owns sections 1..k (its H2s, in the order it wrote
    # them); each lens takes the next number. Computing this up front means a
    # finding can print "6.4" without the renderer having to look ahead.
    exec_h2 = [h for h in re.findall(r"^##\s+(.*)", entries[0]["md"], re.M)]
    exec_secs = [(i + 1, slug(h, entries[0]["prefix"]), h)
                 for i, h in enumerate(exec_h2)]
    base = len(exec_h2)
    for i, e in enumerate(entries[1:], 1):
        e["secno"] = base + i

    scores_html, overall = score_table(entries, run)

    # The site-by-site matrix closes the document: it is reference material a
    # reader consults after the findings, not a thing they read on the way in.
    # It is appended by the renderer rather than declared in the summary,
    # because a section the summary declares lands among sections 1..k and this
    # one has to come last.
    matrix_html = comparison_section(run, meta, images, used)
    matrix_no = base + len(entries) if matrix_html else None

    shared = corroborate(entries)
    all_find = [f for e in entries[1:] for f in e["find"]]
    counts = {k: sum(1 for f in all_find if f["sev"] == k) for k in ("P0", "P1", "P2", "P3")}

    corr_html = ""
    if shared:
        corr_rows = "".join(
            f'<tr class="r{f["sev"].lower()}"><td>{sev_cell(f["sev"])}</td>'
            f'<td><strong>{html.escape(f["title"])}</strong></td>'
            f'<td>{html.escape(", ".join(sorted(f["also"])))}</td></tr>'
            for f in sorted(shared, key=lambda x: (x["sev"], -len(x["also"])))[:8])
        corr_html = ('<table class="fidx corr"><thead><tr><th>Sev</th>'
                     '<th>Finding</th><th>Also raised by</th></tr></thead>'
                     f'<tbody>{corr_rows}</tbody></table>')

    def also_note(f):
        if not f.get("also"):
            return ""
        names = ", ".join(sorted(f["also"]))
        return f'<span class="also">Also raised by {html.escape(names)}</span>'

    def fidx_table(find, link=False, numbered=None):
        rows = []
        for i, f in enumerate(sorted(find, key=lambda x: x["sev"]), 1):
            no = f'<span class="secno">{numbered}.{i}</span> ' if numbered else ""
            title = html.escape(f["title"])
            title = f'<a href="#{f["anchor"]}">{title}</a>' if link else title
            fix = html.escape(f["fix"]) if f["fix"] else '<span class="mut">—</span>'
            rows.append(
                f'<tr class="r{f["sev"].lower()}"><td>{sev_cell(f["sev"])}</td>'
                f'<td>{no}{title}{also_note(f)}</td>'
                f'<td>{html.escape(f["sowhat"])}</td><td>{fix}</td></tr>')
        return ('<table class="fidx"><thead><tr><th>Sev</th><th>Finding</th>'
                '<th>What it costs</th><th>Recommended fix</th></tr></thead>'
                f'<tbody>{"".join(rows)}</tbody></table>')

    def evidence_block(find, cap=2):
        """Screenshots for the worst findings, inline where the client reads.

        Evidence that lives only in the full export is evidence the reader of
        the deliverable never sees, which makes every finding a claim to take
        on faith (§6, invariant 2)."""
        figs = []
        for f in sorted(find, key=lambda x: x["sev"]):
            if f["sev"] not in ("P0", "P1") or not f["shot"]:
                continue
            cls = image_class(f["shot"], images, used)
            if not cls:
                continue
            figs.append(
                f'<figure><span class="shot {cls}"></span>'
                f'<figcaption><span class="sev sev-{f["sev"].lower()}">{f["sev"]}</span> '
                f'{html.escape(f["title"])}</figcaption></figure>')
            if len(figs) >= cap:
                break
        return f'<div class="ev">{"".join(figs)}</div>' if figs else ""

    body = []
    for n, e in enumerate(entries):
        prefix = e["prefix"]

        # summary scope: a lens contributes its triage table only, never detail
        if a.scope == "summary" and n > 0:
            if not e["find"]:
                continue
            body.append(
                f'<section class="doc" id="{e["anchor"]}">'
                f'<h2 id="{slug(e["lens"], prefix)}">'
                f'<span class="secno">{e["secno"]}.</span> {html.escape(e["lens"])} '
                f'— {len(e["find"])} findings</h2>'
                + fidx_table(e["find"], numbered=e["secno"])
                + evidence_block(e["find"])
                + '<p class="mut">Full detail, evidence and reproduction steps '
                  'for these findings are in the complete export.</p></section>')
            e["sub"] = []
            continue

        rendered = render_markdown(e["md"], images, used, prefix)

        if n == 0:
            rendered = re.sub(r"^<h1\b[^>]*>.*?</h1>", "", rendered, count=1)
            rendered = number_exec_sections(rendered, exec_secs)
            # Two sections the summary declares and the renderer fills, so the
            # index and the scores cannot drift from what actually ran.
            rendered = fill_section(rendered, exec_secs, ("contents", "index"),
                                    build_index(exec_secs, entries, a.scope, matrix_no))
            if scores_html:
                rendered = fill_section(rendered, exec_secs,
                                        ("how each area scores", "scores",
                                         "how the site scores", "how it scores"),
                                        scores_html)
            if corr_html:
                rendered = fill_section(rendered, exec_secs, ("raised by more than one check", "corroborated", "raised by more than one"),
                                        corr_html)

        # A findings file gets a triage table before the findings themselves —
        # severity and cost at a glance, so nobody reads 20 findings to learn
        # which 3 matter.
        if e["find"]:
            index = ('<h2 class="idx">Findings at a glance</h2>'
                     + fidx_table(e["find"], link=True))
            marker = '<h3 id="' + e["find"][0]["anchor"] + '"'
            rendered = rendered.replace(marker, index + marker, 1)

        body.append(f'<section class="doc" id="{e["anchor"]}">{rendered}</section>')

    if matrix_html:
        body.append(
            f'<section class="doc wide" id="site-by-site">'
            f'<h2><span class="secno">{matrix_no}.</span> Site-by-site '
            f'comparison</h2>{matrix_html}</section>')

    # Fallbacks only. A summary written to the current template declares
    # Contents, How each area scores and Raised by more than one check as its
    # own numbered sections and the renderer fills them in place; these blocks
    # exist so a run from an older template still gets the content, unnumbered,
    # rather than losing it.
    #
    # The severity tally that used to sit here is gone — the cover carries the
    # same four numbers, and a second copy three pages later was the reader's
    # first hint that two parts of the document were written by different
    # things.
    front = []
    if len(docs) > 1 and not has_section(exec_secs, ("contents", "index")):
        front.append('<nav class="toc"><h2 id="contents">Contents</h2>'
                     + build_index(exec_secs, entries, a.scope, matrix_no) + "</nav>")
    if scores_html and not has_section(exec_secs, ("how each area scores", "scores",
                                                   "how the site scores", "how it scores")):
        front.append('<section class="doc"><h2 id="scores">How each area scores</h2>'
                     + scores_html + "</section>")
    if corr_html and not has_section(exec_secs, ("raised by more than one check", "corroborated", "raised by more than one")):
        front.append('<section class="doc"><h2 id="corroborated">Raised by more '
                     'than one check</h2>' + corr_html + "</section>")

    for block in reversed(front):
        body.insert(1, block)
    body.insert(0, cover(meta, title, subtitle, len(all_find), counts,
                         overall, provenance))

    page = (f"<!doctype html><html><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(title)}</title><style>{CSS}\n{embed(used)}</style>"
            f"</head><body><div class=wrap>"
            + "\n".join(body)
            + "</div></body></html>")

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
