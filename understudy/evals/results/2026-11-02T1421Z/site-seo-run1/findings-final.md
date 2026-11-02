# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability, indexability, sitemap, titles/meta, canonicals, headings, structured data, linking
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — crawl-based lens (persona_mode generic)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 36a5bfa8f1cc — Pricing page is noindex, so it cannot appear in search
- **Severity:** P0
- **So what:** The page that answers "what does it cost" is excluded from the index and can never be found via search.
- **Framework tags:** indexability
- **Flow:** crawl:site
- **Locator:** crawl/pages/3-pricing.json#robots_meta
- **Personas hit:** n/a
- **Observed:**
  - `<meta name="robots" content="noindex">` on /pricing.html (status 200).
  - Linked from the nav on all 5 crawled pages.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html:3`
  > `<meta name="robots" content="noindex">`
- **Repro:**
  1. Open crawl/html/3-pricing.html, line 3.
- **Fix:** Remove the `noindex` meta robots tag from /pricing.html.

### ebf160ce40f6 — Every page links to /features.html, which returns 404
- **Severity:** P1
- **So what:** A main nav item dead-ends on all 5 pages, wasting crawl budget and leaving the features content unindexable.
- **Framework tags:** crawlability, internal-linking
- **Flow:** crawl:site
- **Locator:** crawl/pages/2-features.json#status
- **Personas hit:** n/a
- **Observed:**
  - /features.html returns 404 (title "Not found — Nimbus Notes").
  - All 5 crawled pages list it in internal_links.
- **Evidence:** `crawl/index.json` · `crawl/pages/2-features.json`
- **Repro:**
  1. Request http://localhost:8765/features.html.
- **Fix:** Publish the features page at /features.html, or remove or redirect the nav link.

### 60e8afe2952a — Declared sitemap returns 404 and points at a different host
- **Severity:** P1
- **So what:** Crawlers get no URL list, and the declared host does not match the site crawled.
- **Framework tags:** sitemap
- **Flow:** crawl:site
- **Locator:** crawl/site.json#sitemap
- **Personas hit:** n/a
- **Observed:**
  - robots.txt declares `https://example-nimbus-notes.test/sitemap.xml`; status 404, url_count 0.
  - Declared host differs from crawled host localhost:8765.
- **Evidence:** `crawl/site.json` (sitemap, robots_txt)
  > "Sitemap: https://example-nimbus-notes.test/sitemap.xml"
- **Repro:**
  1. Read robots.txt, then request the declared sitemap URL.
- **Fix:** Publish a sitemap at the declared URL on the production host and list only 200, indexable pages.

### 88ccf5103cd8 — Homepage JSON-LD is invalid and will be ignored
- **Severity:** P2
- **So what:** The SoftwareApplication markup fails to parse, so no structured data is read from the entry page.
- **Framework tags:** structured-data
- **Flow:** crawl:site
- **Locator:** crawl/pages/1-index.json#structured_data
- **Personas hit:** n/a
- **Observed:**
  - `"price": }` has no value; parser error "Expecting value: line 1 column 111".
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:3`
  > "\"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Parse the ld+json block in crawl/html/1-index.html.
- **Fix:** Supply a price value (and priceCurrency) in the Offer, or remove the property; validate the JSON.

### f327c017f53e — About and Privacy share the bare title Nimbus Notes
- **Severity:** P2
- **So what:** Duplicate, generic titles tell a search engine the pages are the same and carry no topic.
- **Framework tags:** titles
- **Flow:** crawl:site
- **Locator:** crawl/pages/4-about.json#title
- **Personas hit:** n/a
- **Observed:**
  - /about.html and /privacy.html both titled "Nimbus Notes" (12 characters, under the roughly 30 minimum).
  - Pricing uses "Pricing — Nimbus Notes", so the pattern exists.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
  > "Nimbus Notes"
- **Repro:**
  1. Compare title fields of the two page records.
- **Fix:** Retitle as "About — Nimbus Notes" and "Privacy — Nimbus Notes".

### b161eeb0bb6b — 2 of 4 live pages have no meta description
- **Severity:** P2
- **So what:** Search engines will auto-generate snippets for /pricing.html and /privacy.html.
- **Framework tags:** meta
- **Flow:** crawl:site
- **Locator:** crawl/pages/5-privacy.json#meta_description
- **Personas hit:** n/a
- **Observed:**
  - meta_description empty on /pricing.html and /privacy.html.
  - Home (92 chars) and About (56 chars; under roughly 70) have one; 404 page excluded.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read meta_description in each page record.
- **Fix:** Add a unique 70–160 character description to each page; lengthen About's.

### d6c622eabcc5 — Pricing has two h1s and Privacy has none
- **Severity:** P3
- **So what:** Weaker page-topic signal on two pages; low consequence at this size.
- **Framework tags:** headings
- **Flow:** crawl:site
- **Locator:** crawl/pages/3-pricing.json#h1
- **Personas hit:** n/a
- **Observed:**
  - /pricing.html h1s: "Pricing", "Plans for every team"; heading_order_valid false.
  - /privacy.html has no h1; only h2 "Privacy".
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json` · `crawl/html/3-pricing.html:9`
- **Repro:**
  1. Read h1 arrays in the two page records.
- **Fix:** Keep one h1 on Pricing; promote "Privacy" to h1 on /privacy.html.

---

## Dropped for want of evidence
- Homepage image "missing alt" (images_missing_alt 1) — html shows `alt=""`, a valid decorative marker, so not a defect.
- Missing canonicals on all 5 pages — no conflicting URLs observed; note only, not reported.

## For other lenses
- FAQPage JSON-LD valid on /about.html, 3 answer blocks; no `llms.txt` (404) — aeo.
- External analytics script and font CSS on the home page — technical.

## Coverage gaps
- /app/login.html not crawled (disallowed by robots.txt, /app/); two off-domain assets skipped.
- Crawl covered 5 pages, under the cap of 15; no page was dropped by the cap.
- Client-rendering: `nimbusBootstrap()` on home not assessed beyond static markup.

## Appendices
- A. Persona debriefs — n/a
- B. Session timelines — n/a
- C. Screenshot index — n/a
