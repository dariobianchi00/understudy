# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability, indexability, sitemap, titles/meta, canonicals, headings, structured data, internal linking
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — Mode C, no persona
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 9b002a15cccb — Pricing page is noindexed, hiding it from search results
- **Severity:** P0
- **So what:** The one page that answers "what does it cost" cannot appear in search results at all.
- **Framework tags:** noindex
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json` records `"robots_meta": "noindex"`.
  - `crawl/html/3-pricing.html` line 3: `<meta name="robots" content="noindex">`.
  - No other crawled page carries a `noindex` directive.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html:3`
- **Repro:**
  1. Fetch `http://localhost:8765/pricing.html`.
  2. Inspect `<head>` — `<meta name="robots" content="noindex">` is present.
- **Fix:** Remove the `noindex` directive from the pricing page template.

### 89e7446257ef — Global navigation links to a Features page that 404s
- **Severity:** P1
- **So what:** Every crawled page's primary nav sends crawlers and visitors to a dead page, wasting crawl budget and passing no value onward.
- **Framework tags:** non-200 internal link
- **Flow:** crawl:page
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/2-features.json`: `"status": 404`, title `"Not found — Nimbus Notes"`.
  - `href="features.html"` appears in the header `<nav>` of every crawled page: `crawl/html/1-index.html:6`, `3-pricing.html:6`, `4-about.html` (nav), `5-privacy.html:6`.
  - `crawl/index.json` lists `pages/2-features.json` under `crawled`, not `not_crawled` — the 404 is real, not a skip.
- **Evidence:** `crawl/pages/2-features.json` · `crawl/html/1-index.html:6`
- **Repro:**
  1. From any crawled page, click "Features" in the header nav.
  2. `http://localhost:8765/features.html` returns HTTP 404.
- **Fix:** Restore the Features page, or remove the nav link until it exists.

### c228905da58e — Declared sitemap returns 404
- **Severity:** P2
- **So what:** The sitemap `robots.txt` promises to search engines does not exist, breaking the one discovery shortcut the site declares for itself.
- **Framework tags:** sitemap
- **Flow:** crawl:site
- **Locator:** https://example-nimbus-notes.test/sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - `crawl/site.json` `robots_txt.sitemap_declared`: `"https://example-nimbus-notes.test/sitemap.xml"`.
  - `crawl/site.json` `sitemap`: `{"status": 404, "url_count": 0, "reachable": false}`.
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Read `robots.txt` — it declares a `Sitemap:` line.
  2. Fetch that URL — HTTP 404.
- **Fix:** Publish a valid `sitemap.xml` at the declared URL, or remove the declaration until one exists.

### 5028f13f825f — About and Privacy pages share an identical generic title tag
- **Severity:** P2
- **So what:** Two different pages tell search engines they are the same page, and neither title says what the page is about.
- **Framework tags:** duplicate title
- **Flow:** crawl:page
- **Locator:** /about.html, /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/4-about.json` `title`: `"Nimbus Notes"` (12 chars).
  - `crawl/pages/5-privacy.json` `title`: `"Nimbus Notes"` (12 chars) — byte-identical.
  - Both are well under the roughly-30-60-character guideline and carry no page-specific content.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Compare `<title>` in `crawl/html/4-about.html:3` and `crawl/html/5-privacy.html:3`.
- **Fix:** Give each page a unique, descriptive title, e.g. "About — Nimbus Notes" and "Privacy Policy — Nimbus Notes".

### 1856ed4d49d8 — Pricing and Privacy pages have no meta description
- **Severity:** P3
- **So what:** Search engines fall back to auto-generated snippets for these pages, which the site cannot control.
- **Framework tags:** missing meta description
- **Flow:** crawl:page
- **Locator:** /pricing.html, /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json` `meta_description_length`: 0.
  - `crawl/pages/5-privacy.json` `meta_description_length`: 0.
  - The other three crawled pages (`/`, `/about.html`, and the 404 `/features.html`) either have one or are non-indexable already.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Inspect `<head>` of `crawl/html/3-pricing.html` and `crawl/html/5-privacy.html` — no `<meta name="description">` element.
- **Fix:** Add a unique 70-160 character meta description to each page.

### 1e91389b3c10 — Homepage JSON-LD is invalid and will be ignored by crawlers
- **Severity:** P2
- **So what:** The homepage's only structured-data block is unparseable, so it earns no rich-result eligibility at all.
- **Framework tags:** invalid structured data
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json` `structured_data[0].valid`: `false`, `error`: `"Expecting value: line 1 column 111"`.
  - `crawl/html/1-index.html:3` — the `application/ld+json` block ends `"offers": {"@type": "Offer", "price": }` — the `price` value is missing, breaking the JSON.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:3`
- **Repro:**
  1. Extract the `<script type="application/ld+json">` block from the homepage.
  2. Parse as JSON — fails on the empty `price` value.
- **Fix:** Supply a `price` value (or remove the incomplete `offers` block) so the JSON-LD parses.

### 8557480b1ff9 — No crawled page declares a canonical URL
- **Severity:** P3
- **So what:** Without a self-referencing canonical, search engines are left to guess the preferred URL for every page, including the two with duplicate titles.
- **Framework tags:** missing canonical
- **Flow:** crawl:page
- **Locator:** site-wide (5/5 crawled pages)
- **Personas hit:** n/a
- **Observed:**
  - All five page records (`1-index.json`, `2-features.json`, `3-pricing.json`, `4-about.json`, `5-privacy.json`) show `"canonical": ""` and `"canonical_is_self": false`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Check `<head>` of any crawled page for `<link rel="canonical">` — absent in all five.
- **Fix:** Add a self-referencing canonical `<link>` to every indexable page template.

### fe04f13e9145 — Heading hierarchy broken on Pricing and Privacy pages
- **Severity:** P3
- **So what:** Malformed heading structure weakens the outline a crawler uses to understand what each page is primarily about.
- **Framework tags:** heading structure
- **Flow:** crawl:page
- **Locator:** /pricing.html, /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json`: `"h1": ["Pricing", "Plans for every team"]` — two H1 elements; `heading_order_valid: false`.
  - `crawl/pages/5-privacy.json`: `"h1": []`, `"h2": ["Privacy"]` — no H1, jumps straight to H2; `heading_order_valid: false`.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json` · `crawl/html/3-pricing.html:9-10` · `crawl/html/5-privacy.html:9`
- **Repro:**
  1. View source of `/pricing.html` — two `<h1>` tags.
  2. View source of `/privacy.html` — first heading is `<h2>Privacy</h2>`, no `<h1>`.
- **Fix:** Give Pricing one H1 and demote the second; add a single H1 to Privacy above the existing H2.

### fb8ebc3ad0d3 — Homepage hero image has no alt text
- **Severity:** P3
- **So what:** The entry page's only image carries no accessible or crawlable description.
- **Framework tags:** missing alt text
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json`: `"images_missing_alt": 1`, `"images_total": 1`.
  - `crawl/html/1-index.html:13`: `<img src="assets/hero.svg" alt="">`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:13`
- **Repro:**
  1. View source of `/` — the hero `<img>` has an empty `alt=""`.
- **Fix:** Add descriptive alt text if the image conveys meaning, or confirm it is purely decorative.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- None — every observation checked against the crawl had a corresponding record.

## For other lenses
- Pricing page displays no actual price ("Pricing depends on your workspace type and sync topology") — conversion lens.
- Homepage loads a third-party analytics script (`analytics.example-tracker.test/t.js`) and external font CSS, both off-domain and uncrawled — technical/trust lens.
- About page carries a valid `FAQPage` structured-data block with 3 Q&A pairs — answer-engine quotability is aeo's call, not scored here.
- `llms.txt` absent (`crawl/site.json` `llms_txt.present: false`) — aeo's territory, not scored here.

## Coverage gaps
- `/app/login.html` — disallowed by `robots.txt` (`/app/`), correctly excluded from this crawl and not scored.
- Two off-domain resources (analytics script, font CDN) were not fetched — expected, off-domain.
- No pages beyond the 5 found were capped or timed out; `cap: 15` was not reached.

## Appendices
- A. Persona debriefs — n/a, no persona for this lens
- B. Session timelines — n/a, this lens reads crawl records only
- C. Screenshot index — n/a, this lens has no screenshots; see `crawl/html/*.html` for raw markup
