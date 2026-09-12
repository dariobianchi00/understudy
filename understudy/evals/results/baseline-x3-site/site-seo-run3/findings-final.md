# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability → sitemap → titles/meta → canonicals → headings → structured data → internal linking → basics
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — this lens reads crawl records only, no persona traversal
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 5b778b39940f — Pricing page is noindexed
- **Severity:** P0
- **So what:** A search engine will not index `/pricing.html`; anyone searching for the product's cost cannot find this page in results.
- **Framework tags:** Crawlability and indexability
- **Flow:** crawl:page
- **Locator:** pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `robots_meta` on `/pricing.html` is `"noindex"`.
  - No other page in the crawl carries a noindex directive.
  - The page returns 200 and is otherwise reachable via internal links from every page.
- **Evidence:** `crawl/pages/3-pricing.json:12`
- **Repro:**
  1. Open `crawl/pages/3-pricing.json`.
  2. Read the `robots_meta` field.
- **Fix:** Remove the `noindex` meta robots tag from `/pricing.html` so it can be indexed.

### 4e97ca5dfa55 — Primary nav links to a 404 page on every crawled page
- **Severity:** P1
- **So what:** Crawlers spend crawl budget on a dead link reachable from 100% of pages, and it signals a broken content section.
- **Framework tags:** Crawlability and indexability; Internal linking
- **Flow:** crawl:site
- **Locator:** features.html
- **Personas hit:** n/a
- **Observed:**
  - `/features.html` returns HTTP 404 (`crawl/pages/2-features.json:4`).
  - It appears in `internal_links` on all 5 crawled pages, including the homepage nav (`crawl/pages/1-index.json:36`, `crawl/pages/3-pricing.json:27`, `crawl/pages/4-about.json:36`, `crawl/pages/5-privacy.json:26`).
  - It is not listed in the sitemap (sitemap itself unreachable, see separate finding).
- **Evidence:** `crawl/pages/2-features.json:4` · `crawl/pages/1-index.json:36`
- **Repro:**
  1. Open any of the 5 page records and check `internal_links` for `/features.html`.
  2. Open `crawl/pages/2-features.json` and confirm `status: 404`.
- **Fix:** Restore the `/features.html` page or update the site-wide nav link to a page that exists.

### e7ada69bc541 — Declared sitemap returns 404
- **Severity:** P2
- **So what:** A crawler following robots.txt to discover the full site gets a broken URL and 0 pages — it must rely on internal links alone.
- **Framework tags:** Sitemap
- **Flow:** crawl:site
- **Locator:** sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - `robots.txt` declares `Sitemap: https://example-nimbus-notes.test/sitemap.xml`.
  - The sitemap fetch returns `status: 404`, `url_count: 0`, `reachable: false`.
- **Evidence:** `crawl/site.json:16` (robots_txt.sitemap_declared) · `crawl/site.json:19` (sitemap block)
- **Repro:**
  1. Open `crawl/site.json`.
  2. Compare `robots_txt.sitemap_declared` against the `sitemap` block's `status`/`reachable` fields.
- **Fix:** Publish a valid sitemap.xml at the declared URL listing the site's indexable pages.

### 8d4ef7b1e0b7 — Homepage JSON-LD is invalid and fails to parse
- **Severity:** P2
- **So what:** The `SoftwareApplication` structured data on the homepage is malformed JSON, so search engines cannot read it at all — not even partially.
- **Framework tags:** Structured data
- **Flow:** crawl:page
- **Locator:** index.html
- **Personas hit:** n/a
- **Observed:**
  - The JSON-LD block's `offers.price` value is empty (`"price": }`), producing a JSON syntax error.
  - Crawl record marks it `"valid": false` with `"error": "Expecting value: line 1 column 111"`.
- **Evidence:** `crawl/pages/1-index.json:29-32`
- **Repro:**
  1. Open `crawl/pages/1-index.json`, inspect `structured_data[0].raw` and `.valid`.
- **Fix:** Fix the malformed `offers.price` value in the homepage JSON-LD so it parses as valid JSON.

### c7cc2064c426 — Duplicate title tag "Nimbus Notes" across pages
- **Severity:** P2
- **So what:** Two different pages present identical, generic titles, telling search engines the pages may be the same content.
- **Framework tags:** Titles and meta
- **Flow:** crawl:site
- **Locator:** about.html, privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `/about.html` title is `"Nimbus Notes"` (12 chars).
  - `/privacy.html` title is also `"Nimbus Notes"` (12 chars) — identical string.
  - Neither title describes the page's actual content.
- **Evidence:** `crawl/pages/4-about.json:6` · `crawl/pages/5-privacy.json:6`
- **Repro:**
  1. Compare the `title` field in `crawl/pages/4-about.json` and `crawl/pages/5-privacy.json`.
- **Fix:** Give each page a unique, descriptive title, e.g. "About — Nimbus Notes" and "Privacy Policy — Nimbus Notes".

### c7d47fcf93c9 — Meta description missing on two pages
- **Severity:** P3
- **So what:** Search engines fall back to auto-generated snippets for these pages, which is less controllable and often less compelling.
- **Framework tags:** Titles and meta
- **Flow:** crawl:site
- **Locator:** pricing.html, privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `/pricing.html` has `meta_description: ""` (length 0).
  - `/privacy.html` has `meta_description: ""` (length 0).
- **Evidence:** `crawl/pages/3-pricing.json:8-9` · `crawl/pages/5-privacy.json:8-9`
- **Repro:**
  1. Check `meta_description_length` in both page records.
- **Fix:** Add a unique 70-160 character meta description to `/pricing.html` and `/privacy.html`.

### 07375c178cad — Heading structure broken on two pages
- **Severity:** P3
- **So what:** Inconsistent heading structure makes page hierarchy ambiguous to crawlers and assistive tech.
- **Framework tags:** Headings
- **Flow:** crawl:site
- **Locator:** pricing.html, privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `/pricing.html` has two H1s: "Pricing" and "Plans for every team"; `heading_order_valid: false`.
  - `/privacy.html` has zero H1s (only an H2 "Privacy"); `heading_order_valid: false`.
- **Evidence:** `crawl/pages/3-pricing.json:14-19` · `crawl/pages/5-privacy.json:14-18`
- **Repro:**
  1. Inspect `h1`, `h2`, and `heading_order_valid` fields in both page records.
- **Fix:** Give `/pricing.html` a single H1 and add a top-level H1 to `/privacy.html`.

### 7b810274775c — Canonical tag missing on every crawled page
- **Severity:** P3
- **So what:** Without self-referencing canonicals, the site relies entirely on crawlers guessing the preferred URL for each page.
- **Framework tags:** Canonicals
- **Flow:** crawl:site
- **Locator:** all pages
- **Personas hit:** n/a
- **Observed:**
  - All 5 crawled pages have `canonical: ""` and `canonical_is_self: false`.
  - No page in the crawl declares a canonical of any kind.
- **Evidence:** `crawl/pages/1-index.json:10-11` · `crawl/pages/3-pricing.json:10-11` · `crawl/pages/4-about.json:10-11` · `crawl/pages/5-privacy.json:10-11`
- **Repro:**
  1. Check `canonical` and `canonical_is_self` in each page record.
- **Fix:** Add a self-referencing `<link rel="canonical">` to each indexable page.

### 21407d82b89c — Homepage image missing alt text
- **Severity:** P3
- **So what:** The site's only crawled image has no alt text, giving search engines and screen readers nothing to describe it.
- **Framework tags:** Basics
- **Flow:** crawl:page
- **Locator:** index.html
- **Personas hit:** n/a
- **Observed:**
  - Homepage record shows `images_total: 1`, `images_missing_alt: 1`.
- **Evidence:** `crawl/pages/1-index.json:46-47`
- **Repro:**
  1. Check `images_total` vs `images_missing_alt` in `crawl/pages/1-index.json`.
- **Fix:** Add descriptive alt text to the homepage image (or empty `alt=""` if purely decorative).

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- None.

## For other lenses
- `llms.txt` absent (`crawl/site.json`: `llms_txt.present: false`) and homepage JSON-LD/FAQPage schema coverage — both bear on answer-engine visibility, in scope for `aeo`.

## Coverage gaps
- `/app/login.html` — disallowed by robots.txt, correctly not crawled; excluded as the auth wall.
- Sitemap contents — could not be checked against crawl results because the declared sitemap 404s (0 URLs).

## Appendices
- A. Persona debriefs — n/a (no persona traversal for this lens)
- B. Session timelines — n/a
- C. Screenshot index — n/a (crawl lens uses page records and raw HTML, not screenshots)
