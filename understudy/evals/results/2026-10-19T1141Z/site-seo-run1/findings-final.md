# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability, indexability, sitemap, titles/meta, canonicals, headings, structured data, linking
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — crawl-only lens (persona_mode generic, no persona used)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### f01da2d3e00e — Pricing page is noindex and will be dropped from search results
- **Severity:** P0
- **So what:** A page that should rank is told to stay out of the index, so pricing searches cannot land on it.
- **Framework tags:** indexability
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `robots_meta` is "noindex" on http://localhost:8765/pricing.html (status 200).
  - robots.txt does not disallow it; the page is crawlable but excluded from the index.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
- **Repro:**
  1. Open crawl/pages/3-pricing.json and read `robots_meta`.
- **Fix:** Remove the `noindex` meta robots tag from pricing.html unless the page is meant to be hidden.

### ec87d2dc1d01 — Features page returns 404 yet is linked from every page
- **Severity:** P1
- **So what:** Crawlers follow a main-nav link into a dead end on all 5 crawled pages, wasting crawl budget and link equity.
- **Framework tags:** crawlability, internal-links
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - /features.html returns 404, title "Not found — Nimbus Notes".
  - Linked from all 5 crawled pages' `internal_links`.
- **Evidence:** `crawl/index.json` · `crawl/pages/2-features.json`
- **Repro:**
  1. Read crawl/index.json: features.html status 404.
  2. Grep `internal_links` in each page record.
- **Fix:** Publish the features page at /features.html, or remove or redirect the link in the shared nav.

### fbfe38887814 — Declared sitemap returns 404 and points to a different host
- **Severity:** P1
- **So what:** Search engines get no URL list, and the declared host differs from the crawled site.
- **Framework tags:** sitemap
- **Flow:** crawl:site
- **Locator:** /sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - robots.txt declares "Sitemap: https://example-nimbus-notes.test/sitemap.xml".
  - Sitemap check recorded status 404, `reachable` false, `url_count` 0.
  - The declared host is not the crawled host (localhost:8765).
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Read `sitemap` and `robots_txt` in crawl/site.json.
- **Fix:** Publish a valid sitemap.xml on the production host and declare that exact URL in robots.txt.

### e117d2fa5e06 — Homepage JSON-LD is invalid and will be ignored
- **Severity:** P2
- **So what:** The SoftwareApplication markup on the entry page is unparseable, so no search engine can use it.
- **Framework tags:** structured-data
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `valid` is false: "Expecting value: line 1 column 111".
  - The `offers.price` property has no value: `"price": }`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
- **Repro:**
  1. Read `structured_data[0]` in crawl/pages/1-index.json.
- **Fix:** Give `offers.price` a value (plus `priceCurrency`) in the homepage JSON-LD and validate it.

### 415e47944ba8 — About and privacy pages share the same generic title
- **Severity:** P2
- **So what:** Duplicate 12-character titles tell a search engine the two pages are the same.
- **Framework tags:** titles
- **Flow:** crawl:site
- **Locator:** title
- **Personas hit:** n/a
- **Observed:**
  - about.html and privacy.html both have the title "Nimbus Notes" (12 characters, below the ~30 guide).
  - Pricing (22 characters) is also under 30.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json` · `crawl/pages/3-pricing.json`
- **Repro:**
  1. Compare `title` across the page records.
- **Fix:** Give each page a unique title of about 30–60 characters, for example "About — Nimbus Notes" and "Privacy Policy — Nimbus Notes".

### 04230238842c — Pricing and privacy pages have no meta description
- **Severity:** P2
- **So what:** 2 of 4 live pages leave the search snippet to be auto-generated.
- **Framework tags:** meta
- **Flow:** crawl:site
- **Locator:** meta-description
- **Personas hit:** n/a
- **Observed:**
  - `meta_description_length` is 0 on pricing.html and privacy.html.
  - Homepage (92) and about (56) have one; about is under the ~70 guide.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read `meta_description` in each page record.
- **Fix:** Add a unique 70–160 character meta description to pricing.html and privacy.html.

### 1fd981161e45 — Pricing has two h1 and privacy has none
- **Severity:** P2
- **So what:** Ambiguous or absent main headings weaken how a crawler understands what each page is about.
- **Framework tags:** headings
- **Flow:** crawl:site
- **Locator:** h1
- **Personas hit:** n/a
- **Observed:**
  - pricing.html h1: "Pricing" and "Plans for every team"; `heading_order_valid` false.
  - privacy.html has no h1; its only heading is the h2 "Privacy".
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read `h1` and `heading_order_valid` in both records.
- **Fix:** Keep one h1 on pricing.html (demote "Plans for every team" to h2) and promote "Privacy" to h1 on privacy.html.

### 1c9cec89e60d — No page declares a canonical URL
- **Severity:** P3
- **So what:** Duplicate URL variants, such as /index.html versus /, have no declared preferred form.
- **Framework tags:** canonicals
- **Flow:** crawl:site
- **Locator:** link[rel=canonical]
- **Personas hit:** n/a
- **Observed:**
  - `canonical` is empty on all 5 crawled pages.
  - pricing.html links to "http://localhost:8765/index.html#demo", an alternate form of the homepage.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json`
- **Repro:**
  1. Read `canonical` in each page record.
- **Fix:** Add a self-referencing `<link rel="canonical">` to every indexable page.

### f0ab3d47fb66 — Only image on the homepage has no alt text
- **Severity:** P3
- **So what:** 1 of 1 images lacks alt, so it gives no image-search context; whether it is decorative was not recorded.
- **Framework tags:** basics, images
- **Flow:** crawl:page
- **Locator:** img
- **Personas hit:** n/a
- **Observed:**
  - `images_missing_alt` 1 of `images_total` 1 on the homepage.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
- **Repro:**
  1. Read `images_missing_alt` in crawl/pages/1-index.json.
- **Fix:** Add descriptive alt text, or `alt=""` if the image is purely decorative.

---

## Dropped for want of evidence
- Missing features page content — the URL was crawled and returned 404, so this is reported as a broken link, not an absence claim.
- Redirect chains, depth, orphan pages — no redirects recorded, and all pages are linked from the home page, so nothing to report.

## For other lenses
- Homepage FAQ-style content on about.html with valid FAQPage JSON-LD (3 answer blocks, 2 in schema) — aeo.
- No llms.txt (404) — aeo.
- Homepage third-party script `analytics.example-tracker.test/t.js` — technical.

## Coverage gaps
- /app/login.html not crawled: disallowed by robots.txt (/app/). Intended, not a finding.
- 2 off-domain resources not crawled (analytics script, fonts CSS).
- Crawl was not capped: 5 of 15 pages used. No sitemap to compare against.
- No og/twitter metadata recorded on any page; not scored.

## Appendices
- A. Persona debriefs — n/a
- B. Session timelines — n/a
- C. Screenshot index — n/a
