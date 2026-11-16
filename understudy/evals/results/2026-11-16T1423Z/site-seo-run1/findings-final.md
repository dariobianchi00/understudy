# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability → sitemap → titles/meta → canonicals → headings → structured data → links → basics
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — crawl-based lens (persona_mode generic)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### f7c653e0bdc6 — Pricing page is noindex, so it cannot be indexed
- **Severity:** P0
- **So what:** The pricing page is removed from search results, so a buyer searching for cost cannot land on it.
- **Framework tags:** crawlability, noindex
- **Flow:** crawl:site
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `robots_meta` is "noindex" on /pricing.html (status 200).
  - Page is linked from the nav on all 5 crawled pages.
- **Evidence:** `crawl/pages/3-pricing.json` (robots_meta) · `crawl/html/3-pricing.html`
- **Repro:**
  1. Open crawl/pages/3-pricing.json and read `robots_meta`.
- **Fix:** Remove the noindex meta robots tag from pricing.html unless the page is deliberately private.

### dcacc2f78eef — Declared sitemap returns 404 and points to a different host
- **Severity:** P1
- **So what:** Crawlers get no sitemap, so discovery relies on links alone.
- **Framework tags:** sitemap
- **Flow:** crawl:site
- **Locator:** /robots.txt
- **Personas hit:** n/a
- **Observed:**
  - robots.txt declares "Sitemap: https://example-nimbus-notes.test/sitemap.xml".
  - That URL returned 404 with url_count 0.
  - The host differs from the crawled host localhost:8765.
- **Evidence:** `crawl/site.json` (robots_txt.sitemap_declared, sitemap.status 404)
- **Repro:**
  1. Read crawl/site.json → sitemap.
- **Fix:** Publish a sitemap.xml listing the live URLs and make the robots.txt Sitemap line point to it on the production host.

### e1d9c167db12 — Internal link /features.html returns 404 from all 5 crawled pages
- **Severity:** P1
- **So what:** The main nav sends crawlers and users to a dead page on every page of the site.
- **Framework tags:** internal-linking, non-200
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - /features.html returned 404 (title "Not found — Nimbus Notes").
  - It appears in internal_links on all 5 crawled pages.
- **Evidence:** `crawl/index.json` (crawled[1].status 404) · `crawl/pages/2-features.json`
- **Repro:**
  1. Request /features.html and check the status.
- **Fix:** Publish the features page at /features.html, or update the nav link to the real URL.

### 683d24244ff1 — Homepage JSON-LD is invalid JSON and will be ignored
- **Severity:** P2
- **So what:** Search engines drop the SoftwareApplication markup, so it earns no rich-result eligibility.
- **Framework tags:** structured-data
- **Flow:** crawl:site
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - The SoftwareApplication block has `"price": }` with no value.
  - The parser reports "Expecting value: line 1 column 111".
- **Evidence:** `crawl/pages/1-index.json` (structured_data[0].valid false)
- **Repro:**
  1. Read structured_data in crawl/pages/1-index.json.
- **Fix:** Give offers.price a value (a quoted number) and validate the JSON-LD.

### 62e7b769bd16 — About and privacy pages share the generic title Nimbus Notes
- **Severity:** P2
- **So what:** Identical titles tell a search engine the two pages are the same, and they also repeat the bare brand name.
- **Framework tags:** titles, duplication
- **Flow:** crawl:site
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - /about.html and /privacy.html both have the title "Nimbus Notes" (12 characters, under 30).
  - The other pages use the "Page — Nimbus Notes" pattern.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Compare `title` in both page records.
- **Fix:** Set distinct titles such as "About — Nimbus Notes" and "Privacy — Nimbus Notes".

### 9116b830472c — Meta descriptions missing on pricing and privacy pages
- **Severity:** P2
- **So what:** Search engines will write the snippet themselves, and for pricing that is a page that should be selling.
- **Framework tags:** meta
- **Flow:** crawl:site
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - /pricing.html and /privacy.html have meta_description_length 0.
  - The 404 page is also empty and is excluded from the count.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read `meta_description` in both page records.
- **Fix:** Add a 70–160 character meta description to each of the two pages.

### 3d9811bfab95 — Heading structure broken: pricing has 2 h1s, privacy has none
- **Severity:** P2
- **So what:** The privacy page has no primary heading and the pricing page has two, so topic signals are unclear.
- **Framework tags:** headings
- **Flow:** crawl:site
- **Locator:** /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - /pricing.html h1: "Pricing", "Plans for every team".
  - /privacy.html h1 is empty and its only heading is the h2 "Privacy".
  - Both records show heading_order_valid false.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read `h1` and `heading_order_valid` in both records.
- **Fix:** Keep one h1 on pricing and change the privacy "Privacy" h2 to an h1.

### 3fda9e8c69af — No canonical link on any crawled page
- **Severity:** P3
- **So what:** There is no explicit preferred URL, which leaves duplicate-URL handling to the search engine.
- **Framework tags:** canonicals
- **Flow:** crawl:site
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `canonical` is empty on all 5 page records.
  - No off-site canonicals were found.
- **Evidence:** `crawl/pages/1-index.json` (canonical "")
- **Repro:**
  1. Read `canonical` in every page record.
- **Fix:** Add a self-referencing rel=canonical to each indexable page.

### 6da6e14a8f54 — Only image on homepage has no alt text
- **Severity:** P3
- **So what:** The image cannot be understood by a crawler, and it is also an accessibility gap.
- **Framework tags:** basics, images
- **Flow:** crawl:site
- **Locator:** /index.html
- **Personas hit:** n/a
- **Observed:**
  - images_total 1 and images_missing_alt 1 on the homepage.
  - Whether the image is content or decoration was not checked.
- **Evidence:** `crawl/pages/1-index.json` (images_missing_alt) · `crawl/html/1-index.html`
- **Repro:**
  1. Read `images_missing_alt` in the homepage record.
- **Fix:** Add descriptive alt text, or alt="" if the image is decorative.

---

## Dropped for want of evidence
- Any claim that a features page is absent from the site — the URL exists in the crawl and returned 404; whether content lives elsewhere was not crawled.

## For other lenses
- FAQPage JSON-LD is valid on /about.html, so answer-engine coverage is worth checking — aeo.
- /app/login.html is disallowed by robots.txt, which is infrastructure and not reported — n/a.
- The pricing noindex also affects whether a visitor can find the price — conversion.

## Coverage gaps
- Sitemap contents could not be checked: the declared URL returned 404.
- Not crawled: /app/login.html (disallowed by robots.txt), 2 off-domain assets (analytics script and fonts CSS).
- JavaScript-rendered content was not checked.

## Appendices
- A. Persona debriefs — none (crawl lens)
- B. Session timelines — none
- C. Screenshot index — none
