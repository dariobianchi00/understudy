# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability, indexability, sitemap, titles/meta, canonicals, headings, structured data, linking
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (none used; crawl-only lens)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 5e7e83b08d13 — Pricing page is noindex, so search engines are told to drop it
- **Severity:** P0
- **So what:** The page a buyer searches for ("Pricing") cannot appear in results at all.
- **Framework tags:** Indexability, robots meta
- **Flow:** crawl:site
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `robots_meta` is `noindex` on `/pricing.html`; no other crawled page has it.
  - `X-Robots-Tag` is empty, so the directive is in the markup only.
  - The page is linked from the nav and footer of all 5 crawled pages.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "<meta name="robots" content="noindex">"
- **Repro:**
  1. Open `crawl/html/3-pricing.html`.
  2. Read the `<head>`.
- **Fix:** Delete the `<meta name="robots" content="noindex">` tag from `pricing.html`.

### 4163987271fb — Features page returns 404 yet is linked from the nav on every page
- **Severity:** P1
- **So what:** Crawlers hit a dead end from every page, and the site has no indexable features content.
- **Framework tags:** Non-200 internal links
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - `/features.html` returned 404, title "Not found — Nimbus Notes".
  - All 5 crawled pages link to it in the nav.
  - The 404 page has no `noindex`.
- **Evidence:** `crawl/index.json` · `crawl/pages/2-features.json` · `crawl/pages/1-index.json`
- **Repro:**
  1. Open `crawl/index.json`.
  2. Find `features.html` with status 404.
- **Fix:** Publish `features.html`, or remove the "Features" link from the nav on every page.

### 788b8a050a3a — Home page JSON-LD is invalid and cannot be parsed
- **Severity:** P1
- **So what:** The entry page's SoftwareApplication data is discarded, so no rich result can come from it.
- **Framework tags:** Structured data validity
- **Flow:** crawl:site
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `structured_data[0].valid` is false: "Expecting value: line 1 column 111".
  - The `price` property has no value.
  - The block is a `SoftwareApplication` with an `Offer`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > ""offers": {"@type": "Offer", "price": }"
- **Repro:**
  1. Open `crawl/html/1-index.html`.
  2. Parse the `application/ld+json` block as JSON.
- **Fix:** Give `price` a value (and `priceCurrency`) in the home page JSON-LD, then validate it.

### 27b936886d52 — Sitemap declared in robots.txt returns 404 and points at a different host
- **Severity:** P2
- **So what:** Crawlers get no sitemap, so discovery relies on links alone.
- **Framework tags:** Sitemap
- **Flow:** crawl:site
- **Locator:** /robots.txt
- **Personas hit:** n/a
- **Observed:**
  - robots.txt declares `https://example-nimbus-notes.test/sitemap.xml`; status 404, `url_count` 0.
  - The declared host differs from the crawled host `localhost:8765`.
  - Site is small (5 pages), so the cost is limited.
- **Evidence:** `crawl/site.json`
  > "Sitemap: https://example-nimbus-notes.test/sitemap.xml"
- **Repro:**
  1. Open `crawl/site.json`.
  2. Read `sitemap.status`.
- **Fix:** Publish a sitemap.xml on the live host listing the indexable pages, and correct the `Sitemap:` line in robots.txt.

### 62e7b769bd16 — About and privacy pages share the generic title Nimbus Notes
- **Severity:** P2
- **So what:** Duplicate, brand-only titles tell a search engine the two pages are the same.
- **Framework tags:** Titles
- **Flow:** crawl:site
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - `/about.html` and `/privacy.html` both have title "Nimbus Notes" (12 characters, under the ~30 floor).
  - Pricing's title is 22 characters, also under 30.
  - Home (41) is within range.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json` · `crawl/pages/3-pricing.json`
  > "title": "Nimbus Notes"
- **Repro:**
  1. Compare `title` in `crawl/pages/4-about.json` and `5-privacy.json`.
- **Fix:** Give each page a unique title of ~30–60 characters, such as "About Nimbus Notes — Who We Are".

### ed8a92033b3a — 3 of 4 live pages have no meta description
- **Severity:** P2
- **So what:** Search engines write the snippet themselves for pricing and privacy.
- **Framework tags:** Meta description
- **Flow:** crawl:site
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `/pricing.html` and `/privacy.html` have an empty `meta_description`.
  - Home (92 characters) has one; About (56) has one under the ~70 floor.
  - The 404 page is excluded from the count.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Check `meta_description` across `crawl/pages/*.json`.
- **Fix:** Add a unique 70–160 character meta description to pricing and privacy; lengthen the about page's.

### 5e451c366731 — Heading structure is broken on pricing (two h1) and privacy (no h1)
- **Severity:** P2
- **So what:** Pages without a single clear h1 give crawlers a weaker statement of topic.
- **Framework tags:** Headings
- **Flow:** crawl:site
- **Locator:** /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `/pricing.html` has two h1: "Pricing" and "Plans for every team".
  - `/privacy.html` has no h1; "Privacy" is an h2.
  - Both are flagged `heading_order_valid: false`.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json` · `crawl/html/5-privacy.html`
  > "<h2>Privacy</h2>"
- **Repro:**
  1. Read `h1` in the two page records.
- **Fix:** Keep "Pricing" as the only h1 on pricing and demote the second to h2; change privacy's h2 to an h1.

### 7a643a0462d1 — No page declares a canonical URL
- **Severity:** P3
- **So what:** Nothing disambiguates alternate URL forms; low risk at 5 pages.
- **Framework tags:** Canonicals
- **Flow:** crawl:site
- **Locator:** site
- **Personas hit:** n/a
- **Observed:**
  - `canonical` is empty on all 5 crawled pages.
  - Nav links use `index.html`-style paths alongside `/`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json`
- **Repro:**
  1. Check `canonical` across `crawl/pages/*.json`.
- **Fix:** Add a self-referencing `<link rel="canonical">` to every indexable page.

---

## Dropped for want of evidence
- Hero image missing alt — crawl counts 1, but markup shows `alt=""`, a valid decorative image; not a finding.
- Client-rendered content risk — `nimbusBootstrap()` runs on load, but nothing recorded shows content depends on it.

## For other lenses
- FAQPage schema lists 2 of the 3 visible questions; "Where is my data stored?" is missing — aeo.
- Pricing shows no prices, only "Contact sales" — conversion.
- `llms.txt` absent (404) — aeo.

## Coverage gaps
- `/app/login.html` disallowed by robots.txt — not crawled; not a missing page.
- Sitemap unreachable, so URL-to-crawl matching was not performed.

## Appendices
- A. Persona debriefs — n/a (no persona in this lens)
- B. Session timelines — n/a
- C. Screenshot index — n/a
