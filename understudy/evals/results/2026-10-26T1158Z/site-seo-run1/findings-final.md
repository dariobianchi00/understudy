# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability, indexability, metadata, structure and structured-data checklist, from crawl records only
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (not used by this lens)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 8355e2ef347b — Pricing page is noindex, so it cannot appear in search
- **Severity:** P0
- **So what:** A crawler is told to drop the pricing page from the index, so it cannot be found by search.
- **Framework tags:** crawlability, indexability
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `robots_meta` is "noindex" on http://localhost:8765/pricing.html (status 200).
  - `x_robots_tag` is empty; the directive comes from the meta tag.
  - Pricing is linked from the nav of all 5 crawled pages.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
- **Repro:**
  1. Open crawl/pages/3-pricing.json.
  2. Read the `robots_meta` field.
- **Fix:** Remove the noindex meta robots tag from pricing.html (or serve index, follow).

### abca3bb324f9 — Nav link to /features.html returns 404 from all 5 crawled pages
- **Severity:** P1
- **So what:** Every page sends crawlers and visitors to a dead end, wasting crawl budget and link equity.
- **Framework tags:** crawlability, internal linking
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - http://localhost:8765/features.html has status 404, title "Not found — Nimbus Notes".
  - The "Features" nav link appears on all 5 crawled pages, including the 404 page.
  - It is linked from the header on every page.
- **Evidence:** `crawl/pages/2-features.json` · `crawl/index.json` · `crawl/html/2-features.html`
- **Repro:**
  1. Open crawl/index.json; see features.html status 404.
  2. Grep `features.html` in crawl/html/*.html.
- **Fix:** Publish a features page at /features.html, or remove the "Features" link from the shared header.

### b3c1c9c35899 — About and privacy pages share the same generic title Nimbus Notes
- **Severity:** P1
- **So what:** Duplicate titles tell a search engine the two pages are the same and say nothing about either.
- **Framework tags:** titles
- **Flow:** crawl:page
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - about.html and privacy.html both have title "Nimbus Notes" (12 characters, under the ~30 floor).
  - Other pages use a "<Page> — Nimbus Notes" pattern, so these two break it.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Compare the `title` field in the two page records.
- **Fix:** Give each a unique title, e.g. "About — Nimbus Notes" and "Privacy — Nimbus Notes".

### 6e5ff340d45f — Home page JSON-LD is invalid and will be ignored
- **Severity:** P2
- **So what:** The SoftwareApplication markup on the entry page fails to parse, so it earns nothing.
- **Framework tags:** structured data
- **Flow:** crawl:page
- **Locator:** /index.html
- **Personas hit:** n/a
- **Observed:**
  - One JSON-LD block, `valid: false`, error "Expecting value: line 1 column 111".
  - The `price` property inside `offers` has no value.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "\"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open crawl/pages/1-index.json, read `structured_data`.
- **Fix:** Supply a numeric `price` and `priceCurrency` in the Offer, or remove the block; validate before publishing.

### c228905da58e — Declared sitemap returns 404
- **Severity:** P2
- **So what:** Crawlers are pointed at a sitemap that does not exist, so discovery relies on links alone.
- **Framework tags:** sitemap
- **Flow:** crawl:site
- **Locator:** /sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - robots.txt declares https://example-nimbus-notes.test/sitemap.xml; status 404, `url_count` 0.
  - The declared host differs from the crawled host (localhost:8765).
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Open crawl/site.json, read `sitemap` and `robots_txt`.
- **Fix:** Publish sitemap.xml on the live host and correct the Sitemap line in robots.txt to its real URL.

### 9aec705a577a — Pricing has two h1s and privacy has no h1
- **Severity:** P2
- **So what:** Unclear primary heading on two pages weakens how a crawler reads their topic.
- **Framework tags:** headings
- **Flow:** crawl:page
- **Locator:** /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - pricing.html has h1 "Pricing" and h1 "Plans for every team"; `heading_order_valid` false.
  - privacy.html has no h1, only h2 "Privacy"; `heading_order_valid` false.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read the `h1` and `h2` fields in both records.
- **Fix:** Keep one h1 on pricing (demote the second to h2) and make "Privacy" the h1 on privacy.html.

### 95fe978183de — Pricing and privacy pages have no meta description
- **Severity:** P2
- **So what:** Search engines will invent the snippet for 2 of 4 live pages.
- **Framework tags:** meta
- **Flow:** crawl:site
- **Locator:** /meta-description
- **Personas hit:** n/a
- **Observed:**
  - pricing.html and privacy.html: `meta_description_length` 0.
  - The 404 page also has none; excluded from the count.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read `meta_description` in each record.
- **Fix:** Add a unique 70–160 character meta description to each page.

### 992857445394 — No crawled page declares a canonical URL
- **Severity:** P3
- **So what:** Without canonicals, URL variants such as index.html#demo give search engines no preferred address.
- **Framework tags:** canonicals
- **Flow:** crawl:site
- **Locator:** /canonical
- **Personas hit:** n/a
- **Observed:**
  - `canonical` is empty on all 4 pages returning 200.
  - Home is reachable as both / and index.html (linked from the header).
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json`
- **Repro:**
  1. Read `canonical` in every page record.
- **Fix:** Add a self-referencing rel=canonical to each page, using the absolute production URL.

### 3d4c49581eb8 — Home page image has no alt text
- **Severity:** P3
- **So what:** The only image on the entry page gives a crawler nothing to read.
- **Framework tags:** basics, images
- **Flow:** crawl:page
- **Locator:** /index.html
- **Personas hit:** n/a
- **Observed:**
  - `images_missing_alt` 1 of `images_total` 1 on the home page.
  - Whether it is content or decoration was not determined.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
- **Repro:**
  1. Read `images_missing_alt` in the home record.
- **Fix:** Add descriptive alt text, or alt="" if the image is purely decorative.

---

## Dropped for want of evidence
- Deep-page depth and orphan checks — only 5 pages crawled, all linked from the header; nothing to report.
- Redirect chains — `redirect_chain` empty on every record; not a finding.

## For other lenses
- FAQPage JSON-LD on about.html is valid; answer-engine value belongs to aeo.
- No llms.txt (404) — aeo.

## Coverage gaps
- /app/login.html not crawled: disallowed by robots.txt (/app/).
- Two off-domain assets (analytics, fonts) not crawled.
- Sitemap contents not checked; the file was unreachable.
- Crawl was 5 pages against a cap of 15; no pages were cut off by the cap.

## Appendices
- A. Persona debriefs
- B. Session timelines
- C. Screenshot index
