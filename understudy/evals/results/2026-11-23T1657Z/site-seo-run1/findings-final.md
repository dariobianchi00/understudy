# Nimbus Notes — seo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: crawlability → indexability → sitemap → titles/meta → headings → structured data
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (n/a for this lens; crawl-only)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 5e7e83b08d13 — Pricing page is noindex, so search engines are told to drop it
- **Severity:** P0
- **So what:** The page that answers "what does it cost" cannot appear in search results at all.
- **Framework tags:** Indexability, noindex
- **Flow:** crawl:site
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `robots_meta` is "noindex" on /pricing.html; no other crawled page carries it.
  - Page is linked from the nav and footer of every crawled page, so it is meant to be public.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > `<meta name="robots" content="noindex">`
- **Repro:**
  1. Open crawl/html/3-pricing.html and read the `<head>`.
- **Fix:** Remove `<meta name="robots" content="noindex">` from pricing.html unless the page is deliberately private.

### 1f92c72dfa0a — Declared sitemap returns 404 and sits on a different host than the site
- **Severity:** P1
- **So what:** Crawlers get no URL list, and the declared host is not the host that was crawled.
- **Framework tags:** Sitemap
- **Flow:** crawl:site
- **Locator:** /sitemap.xml
- **Personas hit:** n/a
- **Observed:**
  - robots.txt declares `https://example-nimbus-notes.test/sitemap.xml`; the crawl recorded status 404, url_count 0.
  - Declared host differs from the crawled `localhost:8765`; may be a staging artefact, which this crawl cannot tell.
- **Evidence:** `crawl/site.json` (sitemap, robots_txt)
  > "Sitemap: https://example-nimbus-notes.test/sitemap.xml"
- **Repro:**
  1. Read robots_txt.sitemap_declared and sitemap.status in site.json.
- **Fix:** Publish sitemap.xml at the production host, list the 200 pages, and update the Sitemap line in robots.txt.

### 696e2538ccaf — Features page 404s but is linked from the nav of all 5 crawled pages
- **Severity:** P1
- **So what:** Every page sends crawlers and visitors to a dead end, and any features content cannot rank.
- **Framework tags:** Non-200 internal links
- **Flow:** crawl:site
- **Locator:** /features.html
- **Personas hit:** n/a
- **Observed:**
  - /features.html returned 404 with title "Not found — Nimbus Notes".
  - Link "Features" appears in the header nav of all 5 crawled pages' internal_links.
  - The 404 page is served with a true 404 status; that part is correct.
- **Evidence:** `crawl/index.json` (crawled[1]) · `crawl/pages/2-features.json`
- **Repro:**
  1. Request /features.html; observe 404.
- **Fix:** Publish the features page at /features.html, or remove the "Features" link from the shared header.

### 4ec16892d082 — Home page JSON-LD is invalid and unparseable
- **Severity:** P2
- **So what:** The SoftwareApplication markup is discarded, so the home page earns no rich-result eligibility.
- **Framework tags:** Structured data validity
- **Flow:** crawl:site
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - Crawl recorded `valid: false`, error "Expecting value: line 1 column 111".
  - The Offer has `"price": }` with no value.
- **Evidence:** `crawl/pages/1-index.json` (structured_data[0]) · `crawl/html/1-index.html`
  > `"offers": {"@type": "Offer", "price": }`
- **Repro:**
  1. Paste the ld+json block from 1-index.html into a JSON validator.
- **Fix:** Give Offer a real `price` and `priceCurrency`, or delete the offers object; validate the block.

### 62e7b769bd16 — About and privacy pages share the generic title Nimbus Notes
- **Severity:** P2
- **So what:** Two pages carry a 12-character title that says nothing about their content, and are duplicated.
- **Framework tags:** Titles
- **Flow:** crawl:site
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - /about.html and /privacy.html both have title "Nimbus Notes" (12 chars, under the ~30 floor).
  - Other pages have distinct titles of 22–41 chars.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Compare `title` in pages/4-about.json and pages/5-privacy.json.
- **Fix:** Set unique titles, e.g. "About — Nimbus Notes" and "Privacy Policy — Nimbus Notes", padded to describe each page.

### cca79720ac9d — Pricing and privacy pages have no meta description
- **Severity:** P2
- **So what:** Search engines write their own snippet for the pricing page, the one that matters commercially.
- **Framework tags:** Meta descriptions
- **Flow:** crawl:site
- **Locator:** /privacy.html
- **Personas hit:** n/a
- **Observed:**
  - 2 of 4 live (200) pages lack a meta description: /pricing.html and /privacy.html.
  - Home (92 chars) and about (56 chars, under ~70) have one.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read `meta_description_length` in each page record: 0.
- **Fix:** Add a 70–160 character description to pricing.html and privacy.html; lengthen the about description.

### 3446f5cd4a8a — Pricing has two h1 elements and privacy has none
- **Severity:** P2
- **So what:** Page topic is ambiguous on pricing and unstated on privacy.
- **Framework tags:** Headings
- **Flow:** crawl:site
- **Locator:** /pricing.html#h1
- **Personas hit:** n/a
- **Observed:**
  - /pricing.html h1: "Pricing", "Plans for every team"; heading_order_valid false.
  - /privacy.html h1 empty; only h2 "Privacy"; heading_order_valid false.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
- **Repro:**
  1. Read `h1` arrays in both page records.
- **Fix:** Make "Pricing" the sole h1 on pricing.html; change the privacy h2 to an h1.

### d7a818cdb71a — No crawled page declares a canonical URL
- **Severity:** P3
- **So what:** Pricing links to `index.html#demo` while home is `/`, so duplicate URLs have nothing to consolidate them.
- **Framework tags:** Canonicals
- **Flow:** crawl:site
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `canonical` is empty on all 5 pages.
  - Nav links to `index.html` and `/` are both used.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json`
- **Repro:**
  1. Read `canonical` in each page record.
- **Fix:** Add a self-referencing `<link rel="canonical">` to every page, using `/` for the home page.

---

## Dropped for want of evidence
- "Images without alt" on home (1 of 1) — markup shows `alt=""`, a valid decorative image; the crawl count is a false positive.
- Client-rendered content concern — `nimbusBootstrap()` runs on load, but all content is present in raw HTML; nothing recorded shows it is needed.
- "No features page exists" — not claimed; /features.html was crawled and 404s.

## For other lenses
- FAQPage JSON-LD lists 2 of 3 on-page questions — aeo.
- No llms.txt (404) and no OG/Twitter tags — aeo.
- Home "See it in action" CTA is `href="#"`; pricing has no prices — conversion.

## Coverage gaps
- /app/login.html disallowed by robots.txt (/app/) — intentional, not a finding.
- 2 off-domain assets (tracker script, font CSS) not crawled.
- Crawl cap 15; only 5 URLs found, so no cap truncation. Heading and anchor-text depth beyond these pages not checked.
- Image alt check done from raw HTML only.
