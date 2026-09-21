# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Crawlability/indexability checklist — robots, sitemap, titles/meta, canonicals, headings, structured data, internal linking, basics
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — Mode C, crawl-only, no persona invoked
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 1de4b2bc0526 — Pricing page is noindexed, blocking cost information from search results
- **Severity:** P0
- **So what:** The one page that answers "what does it cost" cannot appear in search results at all.
- **Framework tags:** Crawlability, Indexability
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `robots_meta` on /pricing.html is `"noindex"` — crawl/pages/3-pricing.json:12
  - Raw markup carries `<meta name="robots" content="noindex">` — crawl/html/3-pricing.html:3
  - The page itself returns 200 and is linked from every other page's nav
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
- **Repro:**
  1. Fetch http://localhost:8765/pricing.html
  2. Read the `<meta name="robots">` tag in the `<head>`
- **Fix:** Remove the `noindex` directive from pricing.html unless it is deliberately kept out of search — if deliberate, flag the conflict with the objective of letting visitors find pricing without contact.

### 7fa988851e82 — Declared sitemap returns 404 and lists zero URLs
- **Severity:** P1
- **So what:** Search engines are told a sitemap exists, follow the link, and get an error — undermining trust in the site's other signals.
- **Framework tags:** Sitemap
- **Flow:** crawl:site
- **Locator:** https://example-nimbus-notes.test/sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - robots.txt declares `Sitemap: https://example-nimbus-notes.test/sitemap.xml` — crawl/site.json:16
  - Fetching that URL returns status 404, `"url_count": 0`, `"reachable": false` — crawl/site.json:19-23
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Read robots.txt at http://localhost:8765/robots.txt
  2. Fetch the declared sitemap URL
- **Fix:** Publish a working XML sitemap at the declared URL listing the site's real, indexable pages.

### b71013110dcd — Global nav links to /features.html, which returns a 404 on every page
- **Severity:** P1
- **So what:** Every crawl of the site's primary navigation ends in a dead page, wasting crawl budget and signalling a missing or removed page.
- **Framework tags:** Internal linking, Non-200 pages linked internally
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - `/features.html` returns status 404 with title "Not found — Nimbus Notes" — crawl/pages/2-features.json:4-6
  - Linked from the header nav on the homepage and pricing page (and, by the same template, about/privacy) — crawl/html/1-index.html:6, crawl/html/3-pricing.html:6
  - The 404 page's own nav links to `/features.html` again — crawl/pages/2-features.json:26
- **Evidence:** `crawl/pages/2-features.json` · `crawl/html/1-index.html` · `crawl/html/3-pricing.html`
- **Repro:**
  1. Load any page on the site
  2. Click "Features" in the header nav
- **Fix:** Restore the features page or remove the "Features" nav link until the page exists.

### 6ca0c20867c0 — Homepage structured data is invalid JSON and fails to parse
- **Severity:** P2
- **So what:** The SoftwareApplication schema on the entry page cannot be read by any parser, so it earns zero rich-result value.
- **Framework tags:** Structured data
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - JSON-LD's `"price":` key has no value before the closing brace — crawl/pages/1-index.json:29-32
  - Parse error recorded verbatim: "Expecting value: line 1 column 111" — crawl/pages/1-index.json:31
  - Raw script tag confirms the malformed source — crawl/html/1-index.html:3
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
- **Repro:**
  1. View source of http://localhost:8765/
  2. Extract and JSON-parse the `<script type="application/ld+json">` contents
- **Fix:** Set a numeric value for `offers.price` in the JSON-LD and validate with a JSON-LD linter before publishing.

### 76e9bc993fd6 — About and privacy pages share an identical, generic page title
- **Severity:** P2
- **So what:** Two different pages present the same 12-character title "Nimbus Notes" in search results, so a searcher can't tell them apart before clicking.
- **Framework tags:** Titles
- **Flow:** crawl:site
- **Locator:** /about.html,/privacy.html
- **Personas hit:** n/a
- **Observed:**
  - /about.html `<title>` is "Nimbus Notes" (12 chars) — crawl/pages/4-about.json:6-7
  - /privacy.html `<title>` is also "Nimbus Notes" (12 chars) — crawl/pages/5-privacy.json:6-7
  - Both are well under the ~30–60 character range and carry no page-specific words
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Fetch /about.html and /privacy.html
  2. Compare `<title>` tags
- **Fix:** Give each page a distinct, descriptive title, e.g. "About — Nimbus Notes" and "Privacy Policy — Nimbus Notes".

### bf2d3c039d0b — Pricing and privacy pages have no meta description
- **Severity:** P2
- **So what:** Search results for these pages fall back to an auto-generated snippet the site doesn't control.
- **Framework tags:** Meta descriptions
- **Flow:** crawl:site
- **Locator:** /pricing.html,/privacy.html
- **Personas hit:** n/a
- **Observed:**
  - /pricing.html `meta_description_length` is 0 — crawl/pages/3-pricing.json:8-9
  - /privacy.html `meta_description_length` is 0 — crawl/pages/5-privacy.json:8-9
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Fetch /pricing.html and /privacy.html
  2. Check for a `<meta name="description">` tag in `<head>`
- **Fix:** Write a unique 70–160 character meta description for each page.

### 946f7f6ed9ab — Heading hierarchy breaks on pricing (two h1s) and privacy (no h1)
- **Severity:** P2
- **So what:** Search engines lose a clear signal of each page's primary topic.
- **Framework tags:** Headings
- **Flow:** crawl:site
- **Locator:** /pricing.html,/privacy.html
- **Personas hit:** n/a
- **Observed:**
  - /pricing.html has two `<h1>` elements, "Pricing" and "Plans for every team"; `heading_order_valid: false` — crawl/pages/3-pricing.json:14-19, crawl/html/3-pricing.html:9-10
  - /privacy.html has zero `<h1>` elements, only an `<h2>` "Privacy"; `heading_order_valid: false` — crawl/pages/5-privacy.json:14-18
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Fetch /pricing.html and /privacy.html
  2. Count `<h1>` elements on each
- **Fix:** Collapse pricing to a single `<h1>` and demote the second heading; add one `<h1>` to the privacy page.

### f36a58a09139 — No page defines a canonical tag
- **Severity:** P3
- **So what:** Search engines are left to infer the canonical URL themselves rather than being told directly, though no duplicate-URL variants were observed in this crawl.
- **Framework tags:** Canonicals
- **Flow:** crawl:site
- **Locator:** /,/pricing.html,/about.html,/privacy.html
- **Personas hit:** n/a
- **Observed:**
  - `canonical` is empty and `canonical_is_self` is `false` on all four 200-status pages — crawl/pages/1-index.json:10-11, crawl/pages/3-pricing.json:10-11, crawl/pages/4-about.json:10-11, crawl/pages/5-privacy.json:10-11
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Fetch each page
  2. Look for `<link rel="canonical">` in `<head>`
- **Fix:** Add a self-referencing canonical tag to every indexable page.

### fb8ebc3ad0d3 — Homepage hero image has no alt text
- **Severity:** P3
- **So what:** The one image on the entry page carries no text alternative for crawlers or accessibility tools to read.
- **Framework tags:** Basics (images/alt)
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `images_missing_alt: 1` of `images_total: 1` on the homepage — crawl/pages/1-index.json:46-47
  - Markup: `<img src="assets/hero.svg" alt="">` — crawl/html/1-index.html:13
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
- **Repro:**
  1. View source of http://localhost:8765/
  2. Inspect the `<img>` tag inside `.hero`
- **Fix:** Add descriptive alt text to the hero image, or document that it is decorative and keep `alt=""` deliberately.

---

## Dropped for want of evidence
None — every observation below the naive-capture threshold had a citable artifact.

## For other lenses
- About page's FAQPage JSON-LD lists 2 Q&As while the page's `answer_blocks` show 3 — schema/content completeness relevant to AEO, not scored here.
- `og`/`twitter` social meta is empty on every page — social-preview quality, not a crawl-indexability check.

## Coverage gaps
- Anchor text quality — the crawl recorded link targets, not visible anchor text, so "click here"-style anchors could not be checked.
- Client-side rendering dependency — no signal was captured either way; markup appears server-rendered but this was not directly tested.
- `/app/login.html` — disallowed by robots.txt, correctly excluded as the auth wall.

## Appendices
- A. Persona debriefs — n/a, no persona for this lens
- B. Session timelines — n/a, no persona for this lens
- C. Screenshot index — n/a, crawl-based lens; see `crawl/html/*.html` for raw markup instead
