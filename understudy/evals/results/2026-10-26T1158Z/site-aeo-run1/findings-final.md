# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: static-markup extractability — schema.org, answer blocks, entity clarity, llms.txt
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a (no-persona lens; manifest persona_mode is generic)
- Scoring model: sonnet
- Scope: extractability only; no live answer engines queried, no claim about current citation
- Not-crawled list read first: /app/login.html (robots), 2 off-domain assets. None bear on these findings.
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 29ceb3019d39 — No Organization schema on any of 5 crawled pages, so no machine-readable publisher identity
- **Severity:** P1
- **So what:** An engine cannot tie any quoted answer to a named, linkable publisher.
- **Framework tags:** schema-coverage, entity-clarity
- **Flow:** crawl:site
- **Locator:** site:organization-schema
- **Personas hit:** n/a
- **Observed:**
  - 0 of 5 pages declare `Organization`; only `SoftwareApplication` (invalid) and `FAQPage` exist.
  - Identity facts exist only as prose on about.html: "Nimbus Notes Ltd", Bristol, founded 2023, company number 14482201.
  - No `logo`, `url` or `sameAs` is declared anywhere.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html` · `crawl/pages/1-index.json`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman"
- **Repro:**
  1. Search the 5 files in crawl/html for `"@type": "Organization"`.
  2. Observe zero matches.
- **Fix:** Add a site-wide `Organization` JSON-LD with name, url, logo, sameAs, foundingDate and founder, using the facts from about.html.

### 2901999fbcca — Home-page JSON-LD is invalid, so the only product schema cannot be parsed
- **Severity:** P1
- **So what:** The home page's only structured data is discarded, leaving the product undescribed to machines.
- **Framework tags:** schema-validity, SoftwareApplication
- **Flow:** crawl:page
- **Locator:** / (script[type=application/ld+json])
- **Personas hit:** n/a
- **Observed:**
  - Crawl recorded `valid: false`, error "Expecting value: line 1 column 111".
  - `"price": }` has no value, so the Offer is also empty.
  - Block has no `applicationCategory` or `operatingSystem`. Overlaps `seo` on validity; reported here for extraction.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > {"@type": "Offer", "price": }
- **Repro:**
  1. Open crawl/html/1-index.html and copy the ld+json script body.
  2. Parse as JSON; it fails at column 111.
- **Fix:** Repair the JSON on index.html; supply a real price (or drop `offers`) and add `applicationCategory`.

### 26564baa6ce2 — FAQPage schema lists 2 of the 3 visible FAQ answers
- **Severity:** P2
- **So what:** The data-residency answer is visible but absent from schema, so extraction is inconsistent.
- **Framework tags:** schema-vs-content, FAQPage
- **Flow:** crawl:page
- **Locator:** /about.html (FAQPage mainEntity)
- **Personas hit:** n/a
- **Observed:**
  - Crawl recorded 3 answer blocks; schema has 2 `Question` entries.
  - Missing: "Where is my data stored?" → "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
  - The two schema answers are self-contained and lead with "Yes."; this page is the site's strongest asset.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Count `<h3>` questions in about.html: 3.
  2. Count `Question` objects in its JSON-LD: 2.
- **Fix:** Add the third Question/Answer to the FAQPage mainEntity on about.html.

### 24b8b13889bb — Pricing page states no price an engine could quote
- **Severity:** P2
- **So what:** "What does Nimbus Notes cost?" has no extractable answer anywhere on the site.
- **Framework tags:** answer-blocks, Product/Offer
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - 60 words, 0 figures; each plan card ends in "Contact sales".
  - Only statement: "Pricing depends on your workspace type and sync topology."
  - No `Product`/`Offer` schema; no question headings (h2 count 0).
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open crawl/html/3-pricing.html.
  2. Search for a currency symbol or digit in plan cards: none.
- **Fix:** Publish a price (or a stated "from" price) per plan in text, add a "How much does Nimbus Notes cost?" heading, and matching `Offer` schema.

### 5807bd824c52 — Only 1 of 5 pages has question-shaped headings; the home page has zero extractable blocks
- **Severity:** P2
- **So what:** The home page is marketing prose; an engine has nothing self-contained to lift about what the product is.
- **Framework tags:** answer-blocks
- **Flow:** crawl:site
- **Locator:** site:question-headings
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks` is empty on /, /pricing.html, /privacy.html, /features.html (404); 3 blocks on /about.html only.
  - Home h2s: "How it works", "Loved by teams", "Book a demo" — none question-shaped.
  - Home answer text depends on context: "Nimbus remembers everything so you never start from zero."
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "Nimbus remembers everything so you never start from zero."
- **Repro:**
  1. Read `answer_blocks` in each crawl/pages/*.json.
  2. Only 4-about.json is non-empty.
- **Fix:** On index.html add "What is Nimbus Notes?" with a one-sentence plain answer first; add a short FAQ to privacy.html.

### 805a03f8719e — Entity is never stated plainly: no sameAs, no og:site_name, jargon category, two pages titled just Nimbus Notes
- **Severity:** P2
- **So what:** A machine cannot state what category Nimbus Notes is in or confirm it elsewhere.
- **Framework tags:** entity-clarity
- **Flow:** crawl:site
- **Locator:** site:entity-clarity
- **Personas hit:** n/a
- **Observed:**
  - `og` is empty on all 5 pages; no `og:site_name`, no `sameAs` links.
  - Category described only as "A bi-directional sync graph with a zero-knowledge vault"; the words "note-taking app" never appear on the home page.
  - /about.html and /privacy.html both have title "Nimbus Notes".
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
  > "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
- **Repro:**
  1. Read `og` and `title` in each crawl/pages/*.json.
  2. Grep home html for "note-taking": no match.
- **Fix:** Open the home page with "Nimbus Notes is a note-taking app for teams…", add og:site_name, and link profiles in sameAs.

### 4e2f4bfc0532 — llms.txt is absent
- **Severity:** P3
- **So what:** Agents get no curated map of canonical pages; emerging convention, so low weight.
- **Framework tags:** llms-txt
- **Flow:** crawl:site
- **Locator:** /llms.txt
- **Personas hit:** n/a
- **Observed:**
  - `llms_txt.present` is false, status 404.
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Request /llms.txt; receive 404.
- **Fix:** Publish /llms.txt describing Nimbus Notes in two lines and linking about.html, pricing.html and privacy.html.

---

## Dropped for want of evidence
- Whether the site is cited by answer engines — out of scope for v1, no evidence obtainable.

## For other lenses
- Pricing page is `noindex`, has two h1s, no canonicals, sitemap 404 — seo
- Anonymous testimonials ("— anonymous") carry no attribution — trust

## Coverage gaps
- Live answer-engine querying not performed (v1 scope).
- /features.html 404; /app/login.html robots-disallowed.

## Appendices
- A. n/a — no personas
