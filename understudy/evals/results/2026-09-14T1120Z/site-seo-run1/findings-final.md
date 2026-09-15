# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability → indexability → sitemap → on-page (titles/meta/canonical/headings) → structured data → internal linking
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — crawl-only lens (Mode C), no persona ran
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 7d5730c85007 — Pricing page is noindex, blocking it from search results
- **Severity:** P0
- **So what:** The one page that answers "what does it cost" cannot appear in search results, no matter how well the rest of the site ranks.
- **Framework tags:** Crawlability and indexability
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json` records `"robots_meta": "noindex"` on the 200-status pricing page.
  - Raw markup confirms `<meta name="robots" content="noindex">` in `<head>`.
  - No `x_robots_tag` header override recorded — the directive is meta-only but still honoured.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
- **Repro:**
  1. Fetch `http://localhost:8765/pricing.html`.
  2. Read `<meta name="robots">` in the response `<head>`.
- **Fix:** Remove the `noindex` directive from `/pricing.html` unless it is deliberately excluded from search — nothing else in the crawl suggests it should be.

### de861e2be88d — Declared sitemap returns 404, giving crawlers no URL list
- **Severity:** P1
- **So what:** Crawlers relying on the sitemap for discovery and priority get nothing — they fall back to link-following alone.
- **Framework tags:** Sitemap
- **Flow:** crawl:site
- **Locator:** /sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - `robots.txt` declares `Sitemap: https://example-nimbus-notes.test/sitemap.xml`.
  - `crawl/site.json` records that URL returning `"status": 404`, `"url_count": 0`, `"reachable": false`.
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Fetch `robots.txt`, read the `Sitemap:` line.
  2. Fetch that URL — 404.
- **Fix:** Publish a sitemap.xml at the declared URL listing the site's indexable pages, or remove the `Sitemap:` line from robots.txt until one exists.

### c3666b8009fd — Primary nav links to /features.html on every page, and it 404s
- **Severity:** P1
- **So what:** Every crawled page, including the entry page, sends crawlers and visitors to a dead Features page — wasted crawl budget and a broken quality signal.
- **Framework tags:** Crawlability and indexability, Internal linking
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - `internal_links` in every page record (`1-index.json`, `3-pricing.json`, `4-about.json`, `5-privacy.json`, and `2-features.json` itself) include `http://localhost:8765/features.html`.
  - `crawl/pages/2-features.json` records `"status": 404` for that URL, titled "Not found — Nimbus Notes".
  - `crawl/index.json` confirms the crawl reached it and recorded the 404 rather than skipping it.
- **Evidence:** `crawl/pages/2-features.json` · `crawl/index.json`
- **Repro:**
  1. Load any crawled page, follow the "Features" nav link.
  2. Response is a 404 page.
- **Fix:** Restore `/features.html` with real content, or remove/repoint the nav link sitewide until it exists.

### 3e01edf2f513 — About and privacy pages share an identical, undersized title tag
- **Severity:** P2
- **So what:** A search engine sees two different pages both titled "Nimbus Notes" and cannot tell them apart in results.
- **Framework tags:** Titles and meta
- **Flow:** crawl:site
- **Locator:** /about.html and /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/4-about.json`: `"title": "Nimbus Notes"`, `"title_length": 12`.
  - `crawl/pages/5-privacy.json`: `"title": "Nimbus Notes"`, `"title_length": 12` — identical string.
  - Both are well under the roughly 30–60 character guideline and carry no page-specific words.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Compare `<title>` on `/about.html` and `/privacy.html`.
- **Fix:** Give each page a distinct, descriptive title, e.g. "About — Nimbus Notes" and "Privacy — Nimbus Notes".

### c79e080c58d2 — Pricing and privacy pages have no meta description
- **Severity:** P3
- **So what:** Search results fall back to an auto-generated snippet for these two pages instead of a controlled one.
- **Framework tags:** Titles and meta
- **Flow:** crawl:site
- **Locator:** /pricing.html and /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json`: `"meta_description": ""`, `"meta_description_length": 0`.
  - `crawl/pages/5-privacy.json`: `"meta_description": ""`, `"meta_description_length": 0`.
  - No `<meta name="description">` tag in either page's raw markup.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json` · `crawl/html/3-pricing.html` · `crawl/html/5-privacy.html`
- **Repro:**
  1. Inspect `<head>` on `/pricing.html` and `/privacy.html` — no description tag.
- **Fix:** Add a unique 70–160 character meta description to each page.

### e3171073b468 — Pricing has two H1s, privacy has none
- **Severity:** P2
- **So what:** A crawler cannot reliably identify the primary topic of either page from its heading structure.
- **Framework tags:** Headings
- **Flow:** crawl:site
- **Locator:** /pricing.html and /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json`: `"h1": ["Pricing", "Plans for every team"]`, `"heading_order_valid": false`.
  - `crawl/pages/5-privacy.json`: `"h1": []`, top heading is `<h2>Privacy</h2>`, `"heading_order_valid": false`.
  - Raw markup confirms two consecutive `<h1>` tags on pricing and no `<h1>` on privacy.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json` · `crawl/html/3-pricing.html` · `crawl/html/5-privacy.html`
- **Repro:**
  1. Count `<h1>` elements on `/pricing.html` — two.
  2. Count `<h1>` elements on `/privacy.html` — zero.
- **Fix:** Give pricing one H1 ("Pricing") and demote the second to H2; add a single H1 to privacy ("Privacy").

### d99d90530177 — No page carries a canonical tag
- **Severity:** P2
- **So what:** Without a self-referencing canonical, the site leaves it to the crawler to guess which URL form is authoritative for each page.
- **Framework tags:** Canonicals
- **Flow:** crawl:site
- **Locator:** all crawled pages
- **Personas hit:** n/a
- **Observed:**
  - `canonical: ""` and `canonical_is_self: false` in every page record: `1-index.json`, `2-features.json`, `3-pricing.json`, `4-about.json`, `5-privacy.json`.
  - No `<link rel="canonical">` in any of the five raw HTML files.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Inspect `<head>` on any crawled page — no canonical link element.
- **Fix:** Add a self-referencing `<link rel="canonical">` to every indexable page.

### 3682670eee87 — Homepage JSON-LD is malformed and fails to parse
- **Severity:** P2
- **So what:** The `SoftwareApplication` structured data on the entry page is invalid and will be ignored by anything that parses JSON-LD.
- **Framework tags:** Structured data
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json` records the block with `"valid": false`, `"error": "Expecting value: line 1 column 111"`.
  - Raw markup shows the cause: `"offers": {"@type": "Offer", "price": }` — the `price` value is missing.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
- **Repro:**
  1. Extract the `<script type="application/ld+json">` block from `/`.
  2. Parse as JSON — fails at column 111.
- **Fix:** Fill in the `price` value (or remove the `offers` object) so the JSON-LD parses.

### fb8ebc3ad0d3 — Homepage hero image has no alt text
- **Severity:** P3
- **So what:** The one image on the entry page carries no accessible or crawlable description of its content.
- **Framework tags:** Basics
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json`: `"images_missing_alt": 1`, `"images_total": 1`.
  - Raw markup: `<img src="assets/hero.svg" alt="">` — empty alt attribute.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
- **Repro:**
  1. Inspect the hero `<img>` on `/` — `alt=""`.
- **Fix:** If the hero image is purely decorative, empty alt is correct — otherwise add a short description of what it depicts.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether `nimbusBootstrap()` injects further indexable content client-side — no JS execution was captured this crawl, only static markup.

## For other lenses
- `llms.txt` absent (`crawl/site.json`: `"present": false`) and no answer-block markup outside `/about.html` — AEO.
- `/about.html` carries a valid `FAQPage` schema with three `answer_blocks` — relevant to AEO quotability, not scored here.
- Homepage loads a third-party analytics script (`https://analytics.example-tracker.test/t.js`) synchronously while displaying "We use no tracking cookies on this site" — trust/privacy.

## Coverage gaps
- `/app/login.html` — not crawled, disallowed by `robots.txt` (`/app/`). Auth wall, excluded from scoring.
- `https://analytics.example-tracker.test/t.js` and `https://fonts.example-cdn.test/all.css` — not crawled, off-domain.
- Sitemap-vs-crawl comparison could not be performed: the declared sitemap 404s (see finding above), so there is no sitemap URL list to compare against what the crawl found.

## Appendices
- A. Persona debriefs — n/a, no persona ran for this lens.
- B. Session timelines — n/a, crawl-only lens; see `crawl/index.json` for the crawl order.
- C. Screenshot index — n/a, no screenshots; evidence is `crawl/pages/*.json` and `crawl/html/*.html`.
