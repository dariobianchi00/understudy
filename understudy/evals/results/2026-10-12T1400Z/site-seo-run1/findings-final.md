# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability, indexability, sitemap, titles/meta, canonicals, headings, structured data, linking
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (not used by this lens; crawl-only)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### e4190755c119 — Pricing page is noindex, so the page that answers "what does it cost" cannot be found in search
- **Severity:** P0
- **So what:** A search engine will drop /pricing.html from its index, hiding the cost page from search.
- **Framework tags:** Indexability
- **Flow:** crawl:site
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `robots_meta` is "noindex" on /pricing.html; the raw HTML carries `<meta name="robots" content="noindex">`.
  - No other crawled page is noindex; /pricing.html is linked from the nav and footer of all pages.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > `<meta name="robots" content="noindex">`
- **Repro:**
  1. Open `crawl/html/3-pricing.html` and read the `<head>`.
- **Fix:** Remove `<meta name="robots" content="noindex">` from pricing.html, or confirm deliberately if the page is meant to stay private.

### a31b8a59f6b8 — Primary nav links to /features.html, which returns 404 from all 5 crawled pages
- **Severity:** P1
- **So what:** Crawlers follow a dead link on every page, and the main product page does not exist for search.
- **Framework tags:** Crawlability, internal linking
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - /features.html returned 404 and is linked in the nav of all 5 crawled pages.
  - The 404 page has a 24-character title and no meta description.
- **Evidence:** `crawl/index.json` · `crawl/pages/2-features.json` · `crawl/html/1-index.html`
  > `<a href="features.html">Features</a>`
- **Repro:**
  1. Fetch http://localhost:8765/features.html.
- **Fix:** Publish a features page at /features.html, or remove "Features" from the nav on every page.

### 0fc762a5e26d — Sitemap declared in robots.txt returns 404 and points at a different host
- **Severity:** P2
- **So what:** Crawlers have no sitemap to discover pages from, and the declared host differs from the crawled one.
- **Framework tags:** Sitemap
- **Flow:** crawl:site
- **Locator:** /sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - robots.txt declares `Sitemap: https://example-nimbus-notes.test/sitemap.xml`; the crawl recorded status 404, url_count 0.
  - The declared host is not the crawled host (localhost:8765); this may be a fixture artefact.
- **Evidence:** `crawl/site.json`
  > "Sitemap: https://example-nimbus-notes.test/sitemap.xml"
- **Repro:**
  1. Read `robots_txt` and `sitemap` in `crawl/site.json`.
- **Fix:** Publish sitemap.xml on the production host listing the live pages, and point the robots.txt Sitemap line at it.

### 4efdcb03d52a — Homepage JSON-LD is invalid JSON and will be ignored
- **Severity:** P2
- **So what:** The SoftwareApplication markup on the entry page is unparseable, so search engines get no structured data from it.
- **Framework tags:** Structured data
- **Flow:** crawl:site
- **Locator:** /index.html#jsonld
- **Personas hit:** n/a
- **Observed:**
  - JSON-LD block recorded `valid: false`, error "Expecting value: line 1 column 111".
  - The `price` property of the Offer has no value: `"price": }`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > `"offers": {"@type": "Offer", "price": }`
- **Repro:**
  1. Parse the ld+json script in `crawl/html/1-index.html` as JSON.
- **Fix:** Supply a real `price` (and `priceCurrency`) in the Offer, or remove the Offer, then validate the block.

### 28d986a5e619 — Titles on /about.html and /privacy.html are both the bare "Nimbus Notes"
- **Severity:** P2
- **So what:** Two pages share an identical 12-character title, so search results cannot tell them apart.
- **Framework tags:** Titles and meta
- **Flow:** crawl:site
- **Locator:** title
- **Personas hit:** n/a
- **Observed:**
  - /about.html and /privacy.html both have title "Nimbus Notes" (12 characters, under ~30).
  - /pricing.html is 22 characters, also short, but unique.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
  > "Nimbus Notes"
- **Repro:**
  1. Compare `title` in the two page records.
- **Fix:** Give each page a unique title, e.g. "About — Nimbus Notes" and "Privacy policy — Nimbus Notes".

### 1d45aef4dad6 — 2 of 4 live pages (/pricing.html, /privacy.html) have no meta description
- **Severity:** P2
- **So what:** Search engines will invent snippets for the pricing and privacy pages.
- **Framework tags:** Titles and meta
- **Flow:** crawl:site
- **Locator:** meta[name=description]
- **Personas hit:** n/a
- **Observed:**
  - `meta_description_length` is 0 on /pricing.html and /privacy.html.
  - The home page (92 chars) and /about.html (56 chars, under ~70) have one.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read `meta_description` in the two page records.
- **Fix:** Add a 70–160 character description to pricing.html and privacy.html, and lengthen the one on about.html.

### 244a5e89f76d — Pricing has two h1s and privacy has no h1
- **Severity:** P2
- **So what:** The page outline is ambiguous on pricing and missing its top heading on privacy.
- **Framework tags:** Headings
- **Flow:** crawl:site
- **Locator:** h1
- **Personas hit:** n/a
- **Observed:**
  - /pricing.html has h1 "Pricing" and h1 "Plans for every team"; `heading_order_valid` false.
  - /privacy.html has no h1, only h2 "Privacy"; `heading_order_valid` false.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json` · `crawl/html/5-privacy.html`
  > `<h2>Privacy</h2>`
- **Repro:**
  1. Read `h1` and `heading_order_valid` in the two page records.
- **Fix:** Make "Plans for every team" an h2 on pricing.html, and change the privacy `<h2>` to `<h1>`.

### 1c9cec89e60d — No page declares a canonical URL
- **Severity:** P3
- **So what:** Crawlers must guess the preferred URL; /index.html#demo and "/" are both linked.
- **Framework tags:** Canonicals
- **Flow:** crawl:site
- **Locator:** link[rel=canonical]
- **Personas hit:** n/a
- **Observed:**
  - `canonical` is empty on all 5 crawled pages.
  - /pricing.html links to `index.html#demo` while the home page is crawled as "/".
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json`
- **Repro:**
  1. Read `canonical` in each page record.
- **Fix:** Add a self-referencing `<link rel="canonical">` to every indexable page.

---

## Dropped for want of evidence
- Hero image missing alt — the record counts 1 missing, but raw HTML shows `alt=""` (decorative); not a defect.
- Client-rendered content — `nimbusBootstrap()` runs on load, but the markup holds all content; no evidence of dependence.

## For other lenses
- FAQPage JSON-LD on /about.html covers 2 of 3 on-page questions — aeo.
- No `llms.txt` (404) — aeo.
- Pricing shows only "Contact sales", no prices — conversion.

## Coverage gaps
- /app/login.html not crawled: disallowed by robots.txt (/app/); infrastructure, not reported.
- Two off-domain assets not fetched (analytics, fonts).
- Crawl depth `standard`, cap 15; 5 pages fetched, cap not reached.
- Backlinks, rankings and traffic are unknowable from a crawl.

## Appendices
- A. Persona debriefs — n/a
- B. Session timelines — n/a
- C. Screenshot index — n/a
