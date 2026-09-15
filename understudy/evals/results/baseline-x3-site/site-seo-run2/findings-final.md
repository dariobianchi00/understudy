# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability/indexability/sitemap/titles/canonicals/headings/structured-data/internal-linking checklist
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — Mode C, no persona
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 59a6a6888d6c — Pricing page is noindexed, removing it from search results
- **Severity:** P0
- **So what:** The one page a prospective buyer is most likely to search for cannot appear in search results at all.
- **Framework tags:** noindex
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `pages/3-pricing.json` records `"robots_meta": "noindex"`
  - `crawl/html/3-pricing.html` line 3: `<meta name="robots" content="noindex">`
  - Page returns 200 and is linked from every crawled page's nav
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html:3`
- **Repro:**
  1. Fetch `http://localhost:8765/pricing.html`
  2. Inspect `<head>` — `<meta name="robots" content="noindex">` is present
- **Fix:** Remove the `noindex` meta tag from `/pricing.html` unless the exclusion is deliberate; if deliberate, confirm it with the team since it contradicts the page being linked sitewide.

### 66ab6ba875a6 — Nav "Features" link 404s on every crawled page
- **Severity:** P1
- **So what:** A crawler following the header nav from any of the 5 pages lands on a dead page, wasting crawl budget and signalling an unreliable site.
- **Framework tags:** non-200 internal link
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - `pages/2-features.json` records `"status": 404` for `http://localhost:8765/features.html`
  - `http://localhost:8765/features.html` appears in `internal_links` of all 5 crawled pages (index, features, pricing, about, privacy)
  - Homepage nav markup: `<a href="features.html">Features</a>` (`crawl/html/1-index.html:6`)
- **Evidence:** `crawl/pages/2-features.json` · `crawl/html/1-index.html:6`
- **Repro:**
  1. From any crawled page, follow the "Features" nav link
  2. Response is 404, title "Not found — Nimbus Notes"
- **Fix:** Publish `/features.html` or remove/repoint the nav link across all templates.

### 72c4879ec5da — About and Privacy pages share an identical, non-descriptive title
- **Severity:** P1
- **So what:** Duplicate titles tell a search engine the two pages are interchangeable, and neither title describes its page's content.
- **Framework tags:** duplicate title, title length
- **Flow:** crawl:site
- **Locator:** /about.html, /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `pages/4-about.json`: `"title": "Nimbus Notes"`, `"title_length": 12`
  - `pages/5-privacy.json`: `"title": "Nimbus Notes"`, `"title_length": 12`
  - Both are well below the ~30–60 character guideline and identical to each other
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Compare `<title>` on `/about.html` and `/privacy.html`
  2. Both read exactly "Nimbus Notes"
- **Fix:** Give each page a distinct, descriptive title, e.g. "About — Nimbus Notes" and "Privacy Policy — Nimbus Notes".

### 1385b0f4af58 — Declared sitemap is unreachable
- **Severity:** P2
- **So what:** The site tells crawlers where its sitemap is, then serves a 404 there — crawlers get no authoritative URL list and no confirmation of what should be indexed.
- **Framework tags:** sitemap
- **Flow:** crawl:site
- **Locator:** /sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - `robots.txt` declares `Sitemap: https://example-nimbus-notes.test/sitemap.xml`
  - `crawl/site.json` records `"sitemap": {"status": 404, "url_count": 0, "reachable": false}`
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Fetch the sitemap URL declared in `robots.txt`
  2. Response is 404
- **Fix:** Publish a valid `sitemap.xml` listing the 4 indexable pages, or remove the `Sitemap:` line from `robots.txt` until one exists.

### ec577498161d — Meta description missing on two of five crawled pages
- **Severity:** P2
- **So what:** Search engines fall back to auto-generated snippets on these pages, which the site cannot control.
- **Framework tags:** meta description
- **Flow:** crawl:site
- **Locator:** /pricing.html, /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `pages/3-pricing.json`: `"meta_description": "", "meta_description_length": 0`
  - `pages/5-privacy.json`: `"meta_description": "", "meta_description_length": 0`
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Inspect `<head>` of `/pricing.html` and `/privacy.html`
  2. No `<meta name="description">` tag present
- **Fix:** Add a unique, ~70–160 character meta description to each page.

### d7a77d64fc03 — No canonical tag on any crawled page
- **Severity:** P2
- **So what:** Without a canonical, search engines must guess which URL variant is authoritative for each page.
- **Framework tags:** canonical
- **Flow:** crawl:site
- **Locator:** all crawled pages
- **Personas hit:** n/a
- **Observed:**
  - All 5 page records (`1-index.json` through `5-privacy.json`) show `"canonical": "", "canonical_is_self": false`
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/2-features.json` · `crawl/pages/3-pricing.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Inspect `<head>` of any crawled page
  2. No `<link rel="canonical">` present
- **Fix:** Add a self-referencing canonical `<link>` to every page template.

### 315b090663fc — Heading structure broken on two pages
- **Severity:** P2
- **So what:** Inconsistent heading structure makes page topic and hierarchy harder for a crawler to parse correctly.
- **Framework tags:** headings
- **Flow:** crawl:site
- **Locator:** /pricing.html, /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `pages/3-pricing.json`: two H1s — `"h1": ["Pricing", "Plans for every team"]`, `"heading_order_valid": false`; confirmed in `crawl/html/3-pricing.html:9-10`
  - `pages/5-privacy.json`: no H1 at all — `"h1": []`, only an H2 ("Privacy"), `"heading_order_valid": false`
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html:9` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Inspect `/pricing.html` markup — two `<h1>` elements present
  2. Inspect `/privacy.html` markup — no `<h1>`, page opens on an `<h2>`
- **Fix:** Give `/pricing.html` a single H1 and demote "Plans for every team" to H2; add a single H1 to `/privacy.html`.

### 72c370c237c1 — Homepage JSON-LD is invalid and ignored by parsers
- **Severity:** P2
- **So what:** The intended `SoftwareApplication` structured data is dropped entirely by any parser, so none of it reaches search engines.
- **Framework tags:** structured data
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `pages/1-index.json` `structured_data[0].valid: false`, `error: "Expecting value: line 1 column 111"`
  - Raw JSON-LD cuts off mid-value: `..."offers": {"@type": "Offer", "price": }` — `price` has no value
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:3`
- **Repro:**
  1. Extract the `<script type="application/ld+json">` block from `/`
  2. Parse as JSON — fails on the empty `"price":` value
- **Fix:** Fill in the `price` value (or remove the `offers` block) so the JSON-LD parses.

### 58ca41bc844e — Hero image has an empty alt attribute
- **Severity:** P3
- **So what:** A screen reader or image-indexing crawler gets no description for the homepage's lead visual.
- **Framework tags:** images/alt
- **Flow:** crawl:page
- **Locator:** / hero image
- **Personas hit:** n/a
- **Observed:**
  - `pages/1-index.json`: `"images_missing_alt": 1, "images_total": 1`
  - `crawl/html/1-index.html:13`: `<img src="assets/hero.svg" alt="">`
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:13`
- **Repro:**
  1. Inspect the hero image markup on `/`
  2. `alt=""` — empty, not descriptive
- **Fix:** If the image is purely decorative, `alt=""` is correct and this can be closed; if it conveys meaning, add descriptive alt text.

---

## Dropped for want of evidence
None — every observation below had a supporting crawl record.

## For other lenses
- Homepage CTA `<a class="cta" href="#">See it in action</a>` resolves to nothing — conversion/UX lens.
- FAQPage structured data on `/about.html` is valid and could support answer-engine visibility — aeo lens.
- `llms.txt` absent (`crawl/site.json`: `"llms_txt": {"present": false}`) — aeo lens.

## Coverage gaps
- `/app/login.html` — disallowed by `robots.txt`, correctly not crawled.
- `analytics.example-tracker.test/t.js`, `fonts.example-cdn.test/all.css` — off-domain, correctly not crawled.
- No pages were skipped for cap or timeout reasons; crawl found and processed all 5 in-domain, allowed pages at `standard` depth.

## Appendices
- A. Persona debriefs — n/a, no persona in this mode
- B. Session timelines — n/a, crawl records only
- C. Screenshot index — n/a, no screenshots captured in this mode
