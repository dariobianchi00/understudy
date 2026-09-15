# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability, indexability, titles/meta, canonicals, headings, structured data, internal linking, sitemap/robots
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens, scored from crawl records only
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 3051286ce7c9 — Pricing page is noindex, removing it from search results
- **Severity:** P0
- **So what:** A search engine will not index or rank `/pricing.html`, so the page most likely to answer "what does this cost" cannot surface in organic search at all.
- **Framework tags:** Crawlability and indexability — noindex on a page that should rank
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json` records `"robots_meta": "noindex"` for `http://localhost:8765/pricing.html`, status 200.
  - The page is linked from main nav on every other page, so it is meant to be found.
  - No other page in the crawl carries this tag.
- **Evidence:** `crawl/pages/3-pricing.json:12`
  > "robots_meta": "noindex"
- **Repro:**
  1. Fetch `http://localhost:8765/pricing.html`.
  2. Inspect the `<meta name="robots">` tag or response header — value is `noindex`.
- **Fix:** Remove the `noindex` directive from the pricing page's meta robots tag.

### 4800e37140c6 — Declared sitemap returns 404, leaving the site with no machine-readable page list
- **Severity:** P1
- **So what:** `robots.txt` promises a sitemap at a specific URL; a crawler that trusts it gets a 404 instead of a page list, so it must fall back to link discovery alone.
- **Framework tags:** Sitemap — present but unreachable, contradicts robots.txt
- **Flow:** crawl:site
- **Locator:** site.json:sitemap
- **Personas hit:** n/a
- **Observed:**
  - `robots.txt` declares `Sitemap: https://example-nimbus-notes.test/sitemap.xml`.
  - `crawl/site.json` records that URL as `"status": 404`, `"reachable": false`, `"url_count": 0`.
- **Evidence:** `crawl/site.json:17` (robots_txt.sitemap_declared) · `crawl/site.json:20` (sitemap.status)
  > "sitemap": {"declared": "https://example-nimbus-notes.test/sitemap.xml", "status": 404, "url_count": 0, "reachable": false}
- **Repro:**
  1. Read `robots.txt` — note the declared sitemap URL.
  2. Fetch that URL — 404.
- **Fix:** Publish a valid XML sitemap at the declared URL listing the site's indexable pages.

### ee71c711f4e7 — Main navigation links to /features.html on every page, which 404s
- **Severity:** P1
- **So what:** Every crawl of every page — home, pricing, about, privacy — follows the same nav link into a dead end, repeatedly wasting crawl budget on a non-existent page.
- **Framework tags:** Crawlability — non-200 page linked internally, site-wide
- **Flow:** crawl:site
- **Locator:** nav:/features.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/html/1-index.html` and every other crawled page's `<nav>` includes `<a href="features.html">Features</a>`.
  - `crawl/pages/2-features.json` records `"status": 404` for that URL, and the 404 page itself repeats the same nav link back to itself.
- **Evidence:** `crawl/html/1-index.html:6` · `crawl/pages/2-features.json:4`
  > "<a href=\"features.html\">Features</a>" ... "status": 404
- **Repro:**
  1. Load any crawled page.
  2. Click "Features" in the header nav — 404.
- **Fix:** Either publish `/features.html` or remove/repoint the nav link on all pages.

### 3b3c44773e3c — Duplicate title tag "Nimbus Notes" across About and Privacy pages
- **Severity:** P2
- **So what:** Identical, generic `<title>` values tell a search engine these two distinct pages may be the same content, which can suppress one from results.
- **Framework tags:** Titles and meta — duplication
- **Flow:** crawl:page
- **Locator:** /about.html,/privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/4-about.json` records `"title": "Nimbus Notes"` (12 chars).
  - `crawl/pages/5-privacy.json` records the identical `"title": "Nimbus Notes"` (12 chars).
  - Both titles are also well under the ~30–60 character guideline and carry no page-specific information.
- **Evidence:** `crawl/pages/4-about.json:6` · `crawl/pages/5-privacy.json:6`
  > "title": "Nimbus Notes"
- **Repro:**
  1. Compare `<title>` on `/about.html` and `/privacy.html`.
- **Fix:** Give each page a distinct, descriptive title, e.g. "About — Nimbus Notes" and "Privacy Policy — Nimbus Notes".

### be8c9bc7866a — Meta description missing on Pricing and Privacy pages
- **Severity:** P2
- **So what:** Without a meta description, a search engine writes its own snippet for these pages, which the site cannot control and often reads worse than the on-page copy.
- **Framework tags:** Titles and meta — missing description
- **Flow:** crawl:page
- **Locator:** /pricing.html,/privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json` records `"meta_description": ""`, length 0.
  - `crawl/pages/5-privacy.json` records `"meta_description": ""`, length 0.
  - `/` and `/about.html` both carry populated descriptions, so this is inconsistent within the site, not a site-wide omission.
- **Evidence:** `crawl/pages/3-pricing.json:9` · `crawl/pages/5-privacy.json:9`
  > "meta_description": ""
- **Repro:**
  1. Inspect `<meta name="description">` on `/pricing.html` and `/privacy.html` — absent.
- **Fix:** Add a unique, ~70–160 character meta description to each page.

### 57174eacfb2c — Invalid JSON-LD on the homepage: malformed price value breaks the SoftwareApplication block
- **Severity:** P2
- **So what:** The structured data block fails to parse, so search engines get no `SoftwareApplication` markup from the homepage at all — a silent all-or-nothing loss, not a partial one.
- **Framework tags:** Structured data — invalid JSON
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json` records `"valid": false`, `"error": "Expecting value: line 1 column 111"`.
  - The raw JSON-LD has `"price": }` — the price value was never written before the object closed.
- **Evidence:** `crawl/pages/1-index.json:29-32`
  > "raw": "{\"@context\": \"https://schema.org\", \"@type\": \"SoftwareApplication\", \"name\": \"Nimbus Notes\", \"offers\": {\"@type\": \"Offer\", \"price\": }", "valid": false, "error": "Expecting value: line 1 column 111"
- **Repro:**
  1. View source on `/`.
  2. Extract the `application/ld+json` block and run it through a JSON parser — fails on the empty `price` value.
- **Fix:** Set an actual numeric `price` (and `priceCurrency`) in the `Offer`, or remove the incomplete `offers` block until it has real values.

### deb0abbeda7c — No page on the site sets a canonical tag
- **Severity:** P3
- **So what:** Without self-referencing canonicals, the site leaves indexing preference entirely to the search engine's own duplicate-detection heuristics.
- **Framework tags:** Canonicals — missing, site-wide
- **Flow:** crawl:site
- **Locator:** canonical:all-pages
- **Personas hit:** n/a
- **Observed:**
  - All five crawled pages (`1-index.json` through `5-privacy.json`) record `"canonical": ""` and `"canonical_is_self": false`.
  - No URL parameters or alternate paths were observed in the crawl that would make this urgent today.
- **Evidence:** `crawl/pages/1-index.json:10` · `crawl/pages/3-pricing.json:10` · `crawl/pages/4-about.json:10` · `crawl/pages/5-privacy.json:10`
  > "canonical": "", "canonical_is_self": false
- **Repro:**
  1. Inspect `<link rel="canonical">` on any crawled page — absent.
- **Fix:** Add a self-referencing canonical tag to every page.

### 8ecaed853f10 — Heading structure broken: Privacy has no H1, Pricing has two
- **Severity:** P3
- **So what:** Inconsistent heading hierarchy makes it harder for a search engine to identify each page's primary topic from markup alone.
- **Framework tags:** Headings — missing H1 / multiple H1
- **Flow:** crawl:page
- **Locator:** /privacy.html,/pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/5-privacy.json` records `"h1": []` and `"heading_order_valid": false`.
  - `crawl/pages/3-pricing.json` records `"h1": ["Pricing", "Plans for every team"]` — two H1s — and `"heading_order_valid": false`.
- **Evidence:** `crawl/pages/5-privacy.json:14` · `crawl/pages/3-pricing.json:14-17`
  > "h1": [] ... "h1": ["Pricing", "Plans for every team"]
- **Repro:**
  1. Inspect heading tags on `/privacy.html` — no `<h1>`.
  2. Inspect `/pricing.html` — two `<h1>` elements.
- **Fix:** Add a single descriptive `<h1>` to the privacy page; reduce pricing to one `<h1>` and demote the second to `<h2>`.

### dbf1cff297f2 — Homepage hero image has an empty alt attribute
- **Severity:** P3
- **So what:** The hero image carries no accessible text, so search engines and screen readers get no description of it.
- **Framework tags:** Basics — image without alt
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json` records `"images_missing_alt": 1`, `"images_total": 1`.
  - `crawl/html/1-index.html` shows `<img src="assets/hero.svg" alt="">` — the attribute exists but is empty.
- **Evidence:** `crawl/pages/1-index.json:46-47` · `crawl/html/1-index.html:12`
  > "images_missing_alt": 1, "images_total": 1
- **Repro:**
  1. View source on `/` — locate `<img src="assets/hero.svg" alt="">`.
- **Fix:** Add descriptive alt text if the image is content, or leave empty alt only if confirmed purely decorative.

---

## Dropped for want of evidence
- None — all observations above are backed by crawl records.

## For other lenses
- `llms_txt.present: false` and homepage JSON-LD (once fixed) would affect answer-engine quotability — that's the AEO lens's call, not scored here.
- Homepage has a marketing form with four required fields ("Book a demo") — conversion-lens territory, not an SEO concern.

## Coverage gaps
- `/app/login.html` — disallowed by robots.txt, not crawled (expected, auth wall).
- Off-domain assets (`analytics.example-tracker.test/t.js`, `fonts.example-cdn.test/all.css`) — out of crawl scope by design.
- No pages beyond the 5 found were capped or timed out; coverage of discovered pages is complete.

## Appendices
- A. Persona debriefs — n/a, no-persona lens.
- B. Session timelines — n/a, static crawl only.
- C. Screenshot index — n/a, no screenshots captured for this lens.
