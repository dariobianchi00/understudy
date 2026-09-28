# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Crawlability, indexability, sitemap/robots, titles/meta, canonicals, headings, structured data, internal linking — checklist audit against the crawl record
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — this lens scores from the crawl record only (Mode C, no persona)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### bb1ce8898384 — Pricing page is noindexed, blocking it from search results
- **Severity:** P0
- **So what:** The page a search engine would use to answer "what does this cost" can never appear in results — it is explicitly excluded.
- **Framework tags:** noindex
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json` records `"robots_meta": "noindex"` on a 200-status page
  - The raw markup confirms it: `<meta name="robots" content="noindex">`
  - No other crawled page carries a noindex directive
- **Evidence:** `crawl/pages/3-pricing.json:12` · `crawl/html/3-pricing.html:3`
- **Repro:**
  1. Fetch `http://localhost:8765/pricing.html`
  2. Inspect `<head>` — `<meta name="robots" content="noindex">` is present
- **Fix:** Remove the `noindex` directive from pricing.html so it can be indexed.

---

### c80906885df1 — Primary nav links to /features.html on every page, which 404s
- **Severity:** P1
- **So what:** Every crawled page, including the homepage, sends both users and crawlers into a dead end via the main navigation — link equity and crawl budget are spent on a page that doesn't exist.
- **Framework tags:** non-200 page linked internally
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/index.json` records `pages/2-features.json` with `"status": 404`
  - `internal_links` in all 5 crawled page records (index, features, pricing, about, privacy) include `http://localhost:8765/features.html`
  - The header `<nav>` markup with the Features link is identical across all 5 pages' HTML
- **Evidence:** `crawl/pages/2-features.json:4` · `crawl/pages/1-index.json:36` · `crawl/html/1-index.html:6`
- **Repro:**
  1. Fetch `http://localhost:8765/features.html`
  2. Response is 404 with title "Not found — Nimbus Notes"
  3. Note the same URL is linked from the nav of every other crawled page
- **Fix:** Either publish the features page or remove the nav link until it exists; do not link to a 404 sitewide.

---

### f5ad42bd1338 — Declared sitemap returns 404 and cannot be crawled
- **Severity:** P2
- **So what:** The site tells crawlers where to find its sitemap, then breaks the promise — no sitemap-based discovery or freshness signal is possible.
- **Framework tags:** sitemap
- **Flow:** crawl:site
- **Locator:** https://example-nimbus-notes.test/sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - `robots.txt` declares `Sitemap: https://example-nimbus-notes.test/sitemap.xml`
  - `crawl/site.json` records the sitemap fetch as `"status": 404`, `"url_count": 0`, `"reachable": false`
  - Internal linking still lets a crawler reach all 5 non-404 pages, so this is a lost efficiency signal rather than a hard block
- **Evidence:** `crawl/site.json:11-23`
- **Repro:**
  1. Fetch `http://localhost:8765/robots.txt` — note the declared Sitemap line
  2. Fetch `https://example-nimbus-notes.test/sitemap.xml` — 404
- **Fix:** Publish a working sitemap.xml at the declared URL, listing the site's indexable pages.

---

### 74753f577302 — No page carries a canonical tag
- **Severity:** P2
- **So what:** Without a canonical, a search engine has to guess which URL variant is authoritative — and the site already has two live spellings of the homepage.
- **Framework tags:** canonical
- **Flow:** crawl:site
- **Locator:** canonical tag (all pages)
- **Personas hit:** n/a
- **Observed:**
  - All 5 crawled page records show `"canonical": ""` and `"canonical_is_self": false` (index, features, pricing, about, privacy)
  - The site's own nav links to `index.html` (e.g. `crawl/pages/3-pricing.json` internal_links) while `crawl/site.json` records the entry URL as `http://localhost:8765/` — two URL forms for the same page, with nothing declaring which is canonical
- **Evidence:** `crawl/pages/1-index.json:11` · `crawl/pages/3-pricing.json:11,32` · `crawl/site.json:2-3`
- **Repro:**
  1. Inspect `<head>` on any crawled page — no `<link rel="canonical">` present
  2. Compare `site.json` entry_url (`/`) against nav hrefs (`index.html`)
- **Fix:** Add a self-referencing canonical tag to every page, using the `/` form of the homepage.

---

### 7955c7921f22 — About and Privacy pages share an identical, generic title tag
- **Severity:** P2
- **So what:** Two different pages tell a search engine they are the same page — one of them will likely be dropped from results in favour of the other.
- **Framework tags:** title
- **Flow:** crawl:page
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/4-about.json` title: `"Nimbus Notes"` (12 characters)
  - `crawl/pages/5-privacy.json` title: `"Nimbus Notes"` (12 characters) — byte-identical
  - Neither title describes the page's actual content ("About" or "Privacy")
- **Evidence:** `crawl/pages/4-about.json:6-7` · `crawl/pages/5-privacy.json:6-7`
- **Repro:**
  1. Compare `<title>` in `crawl/html/4-about.html` and `crawl/html/5-privacy.html`
- **Fix:** Give each page a distinct, descriptive title, e.g. "About — Nimbus Notes" and "Privacy Policy — Nimbus Notes".

---

### f52f3c7d83dc — Homepage JSON-LD is invalid and fails to parse
- **Severity:** P2
- **So what:** The entry page's structured data cannot be read by a search engine at all — it is dead weight, not a rich-result signal.
- **Framework tags:** structured data
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json` records `"valid": false, "error": "Expecting value: line 1 column 111"` for the page's only JSON-LD block
  - Raw markup shows a truncated `Offer` object: `"offers": {"@type": "Offer", "price": }` — the price value was never written
- **Evidence:** `crawl/pages/1-index.json:27-33` · `crawl/html/1-index.html:3`
- **Repro:**
  1. Extract the `<script type="application/ld+json">` block from `crawl/html/1-index.html`
  2. Parse as JSON — fails at column 111, the empty `price` value
- **Fix:** Fix the malformed `price` field (supply a value or remove the `offers` object) so the JSON-LD parses.

---

### 0f56bed64969 — Pricing page renders two H1 elements
- **Severity:** P2
- **So what:** Two competing top-level headings give a crawler no single signal for what the page is primarily about.
- **Framework tags:** headings
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json` lists `"h1": ["Pricing", "Plans for every team"]` and `"heading_order_valid": false`
  - Raw markup confirms two sibling `<h1>` tags before any `<h2>`
- **Evidence:** `crawl/pages/3-pricing.json:14-19` · `crawl/html/3-pricing.html:9-10`
- **Repro:**
  1. Inspect `<main>` in `crawl/html/3-pricing.html` — two `<h1>` elements, no `<h2>`
- **Fix:** Keep one H1 ("Pricing") and demote "Plans for every team" to an H2.

---

### 01923d68c55e — Pricing and Privacy pages have no meta description
- **Severity:** P2
- **So what:** Search results for these two pages fall back to an auto-generated snippet the site does not control, on the page most likely to be clicked from a price-comparison search.
- **Framework tags:** meta description
- **Flow:** crawl:site
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json` records `"meta_description": "", "meta_description_length": 0`
  - `crawl/pages/5-privacy.json` records the same — empty, length 0
  - The other two indexable pages (index, about) both carry one within the ~70-160 character range
- **Evidence:** `crawl/pages/3-pricing.json:8-9` · `crawl/pages/5-privacy.json:8-9`
- **Repro:**
  1. Inspect `<head>` in `crawl/html/3-pricing.html` and `crawl/html/5-privacy.html` — no `<meta name="description">` tag present
- **Fix:** Add a unique, ~70-160 character meta description to pricing.html and privacy.html.

---

### 417f964e9578 — Privacy page has no H1, starts at H2
- **Severity:** P3
- **So what:** The page's topic is never asserted at the top heading level, a small clarity loss for a low-traffic legal page.
- **Framework tags:** headings
- **Flow:** crawl:page
- **Locator:** /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/5-privacy.json` records `"h1": []`, `"h2": ["Privacy"]`, `"heading_order_valid": false`
  - Raw markup opens `<main>` directly with `<h2>Privacy</h2>`, skipping H1
- **Evidence:** `crawl/pages/5-privacy.json:14-18` · `crawl/html/5-privacy.html:9`
- **Repro:**
  1. Inspect `<main>` in `crawl/html/5-privacy.html` — first heading is `<h2>`, no `<h1>` anywhere on the page
- **Fix:** Add an `<h1>Privacy</h1>` and demote the existing heading to H2 or below as needed.

---

### a226a6f49d73 — Homepage hero image has an empty alt attribute
- **Severity:** P3
- **So what:** The site's one image carries no alt text, a minor loss for image search even if the image is decorative.
- **Framework tags:** images/alt
- **Flow:** crawl:page
- **Locator:** assets/hero.svg
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json` records `"images_missing_alt": 1, "images_total": 1`
  - Raw markup: `<img src="assets/hero.svg" alt="">` — the only image on the site, in the hero section
- **Evidence:** `crawl/pages/1-index.json:46-47` · `crawl/html/1-index.html:13`
- **Repro:**
  1. Inspect the hero `<img>` in `crawl/html/1-index.html` — `alt=""`
- **Fix:** If the SVG conveys meaning, add descriptive alt text; if purely decorative, leave empty alt but confirm intent (currently indistinguishable from an oversight).

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether content requires JavaScript to render — the crawl record captures rendered markup but no JS-disabled comparison, so client-rendering dependency cannot be confirmed either way.

## For other lenses
- Pricing page lists no actual prices, only "Contact sales" cards — clarity/conversion.
- About page's FAQPage JSON-LD marks up only 2 of the 3 visible FAQ answers (`crawl/pages/4-about.json` answer_blocks vs structured_data mainEntity) — aeo.
- No Open Graph or Twitter Card tags on any page (`og: {}`, `twitter: {}` on every crawled page) — aeo/social.
- `llms.txt` absent (`crawl/site.json`: `"present": false, "status": 404`) — aeo, per lens scope.

## Coverage gaps
- `/app/login.html` — disallowed by robots.txt, not crawled (infrastructure, correctly excluded).
- Two off-domain assets (analytics tracker script, font CDN) were not fetched — off-domain, not pages.
- No pages were skipped for being over the crawl cap (cap 15, only 5 pages + 1 404 found) — coverage is complete for what the site exposes.

## Appendices
- A. Persona debriefs — n/a, no persona for this lens.
- B. Session timelines — n/a, crawl record only.
- C. Screenshot index — n/a, this lens works from `crawl/` records, not screenshots.
