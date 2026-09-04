---
name: traversal-crawl
description: Mode C capture. Crawls a public site with no session and no persona, recording per-page markup facts — titles, meta, canonicals, headings, structured data, internal links, robots and sitemap. Gathers evidence only; it never scores or diagnoses. Use when running the capture half of an seo or aeo objective.
---

# Traversal — Mode C crawl

**No persona. No session. No login.** This is a machine reading markup, and its output is a set of facts, not impressions.

There is no naive/analyst tension here — a crawler has no priors to contaminate. But the evidence rule holds exactly as it does everywhere else: **the lens can only report what this capture recorded.** A crawl that skipped a field produces a lens that cannot mention it.

## Load before starting

- `${CLAUDE_PLUGIN_ROOT}/references/playwright-patterns.md` — driving the browser
- `${CLAUDE_PLUGIN_ROOT}/references/evidence-rules.md` — what capture owes scoring

## Scope

Set at interview and recorded in the manifest.

| `coverage_depth` | Crawl |
|---|---|
| `overview` | The entry URL only |
| `standard` *(default)* | Entry URL + every internal link in the primary navigation (typically 5–15 pages) |
| `deep` | Breadth-first from the entry URL, same registrable domain, to a **hard cap of 50 pages** |

**Never leave the registrable domain.** Never follow a link that changes host, even a subdomain, unless the target explicitly lists it. Record external links as facts; do not fetch them.

**Respect `robots.txt`.** Fetch it first. If a path is disallowed for `*`, do not crawl it — record that it is disallowed, which is itself an `seo` fact. **A tool that ignores robots.txt is a tool nobody can run against a client's site.**

**Rate-limit yourself.** One page at a time, a short pause between. You are a guest.

---

## Run order

### 1. Site-level, once

```
→ crawl — <base-url>, depth <standard>, cap <n> pages
```

Fetch and record, verbatim, into `crawl/site.json`:

- `robots.txt` — full text, plus whether it exists at all
- `sitemap.xml` — from `robots.txt` if declared, else the conventional path. URL count, and whether the URLs are reachable
- `llms.txt` — present or absent, and its content if present *(an `aeo` fact; record it here so the crawl is the only thing that fetches)*
- The final URL after redirects from the entry URL, and the chain
- Response headers on the entry URL

### 2. Per page

For every crawled URL, record into `crawl/pages/<n>-<slug>.json`:

```json
{
  "url": "", "final_url": "", "status": 0, "redirect_chain": [],
  "title": "", "title_length": 0,
  "meta_description": "", "meta_description_length": 0,
  "canonical": "", "canonical_is_self": true,
  "robots_meta": "", "x_robots_tag": "",
  "h1": [], "h2": [], "heading_order_valid": true,
  "lang": "", "charset": "",
  "og": {}, "twitter": {},
  "structured_data": [],
  "internal_links": [], "external_links": [],
  "images_missing_alt": 0, "images_total": 0,
  "word_count": 0,
  "has_main_landmark": true,
  "answer_blocks": []
}
```

**`structured_data`** — every `<script type="application/ld+json">` parsed, plus any microdata/RDFa types found. Record the raw JSON, not a summary. **Record invalid JSON as invalid** — do not silently skip it; a broken block is a finding and skipping it makes the site look clean.

**`answer_blocks`** — for `aeo`: any question-shaped heading (`How…`, `What…`, `Why…`, `Can…`, `Is…`) with the text that follows it, plus any FAQ/definition-list markup. Record the pairs verbatim.

**`heading_order_valid`** — false if levels skip (h1 → h3) or if there is no h1 or more than one.

### 3. Capture the raw HTML too

Save each page's rendered HTML into `crawl/html/<n>-<slug>.html`. **Cheap now, irreplaceable later** — a lens that needs to check one attribute you did not think to extract can look, instead of guessing or dropping the finding.

### 4. Write the index

`crawl/index.json`: every URL crawled, its status, and the file holding its record. Plus what was **not** crawled and why — disallowed, off-domain, over the cap, or timed out.

**The not-crawled list matters as much as the crawled one.** A lens that does not know a section was skipped will report its absence as a finding about the site.

### 5. Verify

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check_capture.py <run_folder>
```

---

## Things that go wrong

| Situation | Do |
|---|---|
| A page needs JavaScript to render content | You are driving a real browser — wait for the content, then extract. Note that it was client-rendered; that is an `seo` fact. |
| Infinite URL space (calendars, filters, session ids) | Stop at the cap, record that the space is unbounded. That is itself a finding for `seo`. |
| A page 500s or times out | Record status and move on. Do not retry more than once. |
| `robots.txt` disallows almost everything | Record it and stop. Do not work around it, ever. |
| A login wall appears | Record and stop at it. Mode C never authenticates. |
| The sitemap lists thousands of URLs | Record the count, sample the first 20 for reachability, say you sampled. |

---

## What you do not do

- **Do not score, rank or diagnose.** No "this title is too long" — record the length; the lens judges it.
- **Do not fix or normalise.** Record what is there, including the empty string and the malformed block.
- **Do not follow external links.**
- **Do not submit forms or trigger any state change.**
- **Do not ignore `robots.txt`.**
