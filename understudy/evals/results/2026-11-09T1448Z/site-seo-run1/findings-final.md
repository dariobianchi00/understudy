# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawl-based SEO checklist (crawlability, sitemap, titles/meta, canonicals, headings, structured data, basics)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens (persona_mode generic)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 5d23635deb8c — Pricing page carries noindex and is hidden from search
- **Severity:** P0
- **So what:** The page that answers "what does it cost" is told not to be indexed, so search engines will drop it.
- **Framework tags:** indexability
- **Flow:** crawl:site
- **Locator:** crawl/pages/3-pricing.json#robots_meta
- **Personas hit:** n/a
- **Observed:**
  - `robots_meta` is "noindex" on http://localhost:8765/pricing.html (status 200).
  - `x_robots_tag` is empty, so the directive comes from the meta tag.
  - Page is linked from the nav of all 5 crawled pages.
- **Evidence:** `crawl/pages/3-pricing.json:12` · `crawl/html/3-pricing.html`
- **Repro:**
  1. Open crawl/pages/3-pricing.json.
  2. Read `robots_meta`.
- **Fix:** Remove `<meta name="robots" content="noindex">` from pricing.html.

### b78fb3394140 — Features page returns 404 while linked from all 5 pages
- **Severity:** P1
- **So what:** Every page links to a dead URL, wasting crawl budget and leaving the product's features page unindexable.
- **Framework tags:** crawlability, internal linking
- **Flow:** crawl:site
- **Locator:** crawl/pages/2-features.json#status
- **Personas hit:** n/a
- **Observed:**
  - http://localhost:8765/features.html returned 404 with title "Not found — Nimbus Notes".
  - Linked in `internal_links` of all 5 crawled pages.
  - Not in the not-crawled list; it was fetched and failed.
- **Evidence:** `crawl/index.json` · `crawl/pages/2-features.json:4`
- **Repro:**
  1. Request /features.html.
  2. Observe 404.
- **Fix:** Publish features.html at that URL, or repoint the nav link to the real page and 301 the old URL.

### a12ad7e35810 — Declared sitemap returns 404
- **Severity:** P1
- **So what:** Crawlers get no URL list from the only sitemap declared, so discovery relies on links alone.
- **Framework tags:** sitemap
- **Flow:** crawl:site
- **Locator:** crawl/site.json#sitemap
- **Personas hit:** n/a
- **Observed:**
  - robots.txt declares `https://example-nimbus-notes.test/sitemap.xml`; status 404, `url_count` 0.
  - Declared host differs from the crawled host (localhost:8765).
  - No other sitemap location was recorded.
- **Evidence:** `crawl/site.json:12` · `crawl/site.json:18`
  > "Sitemap: https://example-nimbus-notes.test/sitemap.xml"
- **Repro:**
  1. Read robots.txt.
  2. Fetch the declared sitemap URL.
- **Fix:** Publish sitemap.xml at the declared URL listing the live indexable pages, or correct the Sitemap line in robots.txt.

### 33c4ad6801bf — Home page JSON-LD is invalid and unparseable
- **Severity:** P2
- **So what:** Search engines discard the SoftwareApplication markup, so no rich result is possible from it.
- **Framework tags:** structured data
- **Flow:** crawl:site
- **Locator:** crawl/pages/1-index.json#structured_data
- **Personas hit:** n/a
- **Observed:**
  - JSON-LD block on the entry page is `valid: false`: "Expecting value: line 1 column 111".
  - The Offer has `"price": }` with no value and no closing braces.
- **Evidence:** `crawl/pages/1-index.json:27` · `crawl/html/1-index.html`
- **Repro:**
  1. Extract the ld+json block from the home page.
  2. Parse as JSON.
- **Fix:** Supply the Offer price value, close the object, and validate the block.

### 8e8f59683e69 — About and privacy pages share the bare title Nimbus Notes
- **Severity:** P2
- **So what:** Two different pages present identical, 12-character titles, which tells search engines they are the same.
- **Framework tags:** titles
- **Flow:** crawl:site
- **Locator:** crawl/pages/4-about.json#title
- **Personas hit:** n/a
- **Observed:**
  - about.html and privacy.html both have title "Nimbus Notes" (12 chars, under ~30).
  - Home, pricing use distinct titles of 41 and 22 chars.
- **Evidence:** `crawl/pages/4-about.json:6` · `crawl/pages/5-privacy.json:6`
- **Repro:**
  1. Compare `title` in pages 4 and 5.
- **Fix:** Give each page a unique title, e.g. "About — Nimbus Notes" and "Privacy Policy — Nimbus Notes".

### 3002f146fc04 — 3 of 4 live pages have no meta description
- **Severity:** P2
- **So what:** Pricing and privacy leave snippet text to the engine's guess.
- **Framework tags:** meta
- **Flow:** crawl:site
- **Locator:** crawl/pages/3-pricing.json#meta_description
- **Personas hit:** n/a
- **Observed:**
  - Empty on pricing.html and privacy.html (2 of 4 live 200 pages); the 404 page also has none.
  - Home (92 chars) and about (56 chars, under ~70) have one.
- **Evidence:** `crawl/pages/3-pricing.json:8` · `crawl/pages/5-privacy.json:8` · `crawl/pages/2-features.json:8`
- **Repro:**
  1. Read `meta_description` in each page record.
- **Fix:** Add a unique 70–160 character meta description to pricing.html and privacy.html.

### fe3be0130df9 — Pricing has two h1s and privacy has none
- **Severity:** P2
- **So what:** Heading structure gives engines a muddled primary topic on two pages.
- **Framework tags:** headings
- **Flow:** crawl:site
- **Locator:** crawl/pages/5-privacy.json#h1
- **Personas hit:** n/a
- **Observed:**
  - pricing.html h1: "Pricing" and "Plans for every team"; `heading_order_valid` false.
  - privacy.html has no h1; only h2 "Privacy"; `heading_order_valid` false.
- **Evidence:** `crawl/pages/3-pricing.json:14` · `crawl/pages/5-privacy.json:14`
- **Repro:**
  1. Read `h1` in each record.
- **Fix:** Keep one h1 on pricing; change privacy's "Privacy" h2 to an h1.

### ef9fa93eaa10 — Home page image has no alt text
- **Severity:** P3
- **So what:** The single image on the entry page gives no text to image search or accessibility tooling.
- **Framework tags:** basics
- **Flow:** crawl:site
- **Locator:** crawl/pages/1-index.json#images_missing_alt
- **Personas hit:** n/a
- **Observed:**
  - `images_missing_alt` 1 of `images_total` 1 on the home page.
  - Content vs decoration not determined from the record.
- **Evidence:** `crawl/pages/1-index.json:46`
- **Repro:**
  1. Read the home page's image tags.
- **Fix:** Add descriptive alt text, or alt="" if the image is decorative.

### 7bff96a06ca8 — No crawled page declares a canonical
- **Severity:** P3
- **So what:** No self-referencing canonical on any page, so URL variants such as /index.html#demo are not consolidated.
- **Framework tags:** canonicals
- **Flow:** crawl:site
- **Locator:** crawl/pages/1-index.json#canonical
- **Personas hit:** n/a
- **Observed:**
  - `canonical` is empty on all 5 page records.
  - Pricing links to `/index.html#demo`, a second URL for the home page.
- **Evidence:** `crawl/pages/1-index.json:10` · `crawl/pages/3-pricing.json:32`
- **Repro:**
  1. Read `canonical` in each record.
- **Fix:** Add a self-referencing `<link rel="canonical">` to every indexable page.

---

## Dropped for want of evidence
- Missing pages (e.g. login, features content) — /app/ was disallowed by robots.txt; not a finding.

## For other lenses
- FAQPage JSON-LD on about.html is valid; answer-engine quotability is out of scope here — aeo.
- llms.txt returned 404 — aeo.
- External analytics script on the home page — technical.

## Coverage gaps
- Not crawled: /app/login.html (disallowed by robots.txt), 2 off-domain assets. Not an absence claim.
- Redirect chains: entry URL has none; no other redirects recorded.
- Page depth and orphans: all pages linked from nav, depth 1; no orphans found.
- JavaScript-rendering need not recorded.

## Appendices
- A. Persona debriefs — n/a
- B. Session timelines — n/a
- C. Screenshot index — n/a
