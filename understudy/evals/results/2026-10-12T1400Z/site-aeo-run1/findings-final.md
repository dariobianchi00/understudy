# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: AEO v1 — schema.org coverage, answer-block extractability, entity clarity, llms.txt (static markup only)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens (manifest `persona_mode: generic`; not used here)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope: extractability only. No live answer engines queried; nothing here says whether the site is cited.

---

## Findings

### 5a026d0d22a1 — No Organization schema on any of 5 crawled pages, so the publisher is unattributable
- **Severity:** P1
- **So what:** An engine cannot tie answers to a named, verifiable publisher; this is the foundation of attribution.
- **Framework tags:** schema-coverage, entity-clarity
- **Flow:** crawl:site
- **Locator:** site:schema/Organization
- **Personas hit:** n/a
- **Observed:**
  - 0 of 5 crawled pages declare `Organization` (only FAQPage on one page; one invalid SoftwareApplication).
  - Organisation facts exist only as prose on /about.html: "Nimbus Notes Ltd", "Priya Raman", "Bristol", "Company number 14482201".
  - No `WebSite`, `logo`, `sameAs` or `og:site_name` anywhere.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html` · `crawl/pages/1-index.json`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023"
- **Repro:**
  1. Open each `crawl/pages/*.json` and read `structured_data`.
  2. Search all five for `Organization`; none found.
- **Fix:** Add one `Organization` JSON-LD block sitewide with name "Nimbus Notes Ltd", url, logo, founder, address and `sameAs` profile links.

### 875bd628ed10 — Homepage JSON-LD is invalid, so the SoftwareApplication data cannot be parsed
- **Severity:** P2
- **So what:** The only product schema on the site is discarded by parsers, leaving the product undescribed in structured form.
- **Framework tags:** schema-validity
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `"price": }` has no value; parse error "Expecting value: line 1 column 111".
  - Block declares only `name` and `offers`; no `applicationCategory` or `operatingSystem`.
  - Overlaps with seo on validity; reported here for its effect on extraction.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "\"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open `crawl/html/1-index.html` and find the `application/ld+json` script.
  2. Run it through any JSON parser.
- **Fix:** Fix the JSON on `/`: supply a real price (or drop `offers`) and add `applicationCategory`, `operatingSystem`, `description`.

### c2a20f5ae612 — FAQ markup covers 2 of the 3 visible Q&As, leaving the data-location answer unmarked
- **Severity:** P2
- **So what:** The one answer about where data lives, a common buyer question, is missing from the structured set.
- **Framework tags:** answer-blocks, schema-coverage
- **Flow:** crawl:page
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - `FAQPage` lists "Does Nimbus Notes work offline?" and "Can I export my notes?"; the third visible question is absent.
  - The third answer opens with "In the EU (Frankfurt) by default." without naming the product.
  - Two marked answers do name the product and lift out cleanly; the third does not.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "Where is my data stored?" → "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Compare `answer_blocks` (3 entries) with the FAQPage `mainEntity` (2 entries).
- **Fix:** Add the third Question to the FAQPage and rewrite as "Nimbus Notes stores data in the EU (Frankfurt) by default."

### 0d9f543e6822 — Homepage, pricing and privacy pages have zero extractable answer blocks
- **Severity:** P2
- **So what:** 3 of 4 live content pages offer nothing an engine can lift as a standalone answer.
- **Framework tags:** answer-blocks
- **Flow:** crawl:site
- **Locator:** site:answer-blocks
- **Personas hit:** n/a
- **Observed:**
  - Only /about.html has answer blocks: 3 across 1 of 5 pages.
  - Homepage H2s are "How it works", "Loved by teams", "Book a demo"; none is question-shaped.
  - Homepage answer text is marketing prose: "Nimbus remembers everything so you never start from zero."
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
  > "Nimbus remembers everything so you never start from zero."
- **Repro:**
  1. Read `answer_blocks` in pages 1, 3 and 5; all are `[]`.
- **Fix:** Add question headings with 1–2 sentence self-contained answers on `/` (what is it, is it secure) and /privacy.html (what data is kept).

### 7534922984de — Pricing page states no prices or plan facts an engine could quote
- **Severity:** P2
- **So what:** "How much does Nimbus Notes cost?" has no quotable answer on the site; engines would have nothing to attribute.
- **Framework tags:** answer-blocks, schema-coverage
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - 3 plan cards (Starter, Team, Enterprise) each say only "Contact sales"; 60 words total, no figures.
  - No `Product`/`Offer` schema; page also carries `robots: noindex` (seo owns that).
  - Two H1s: "Pricing" and "Plans for every team".
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/html/3-pricing.html`; search for a currency symbol or number; none.
- **Fix:** Publish plan prices (or the pricing rule) as text on /pricing.html and mark them up with `Offer` schema matching the visible figures.

### b1a909c44350 — Nothing on the site states what category Nimbus Notes is in
- **Severity:** P2
- **So what:** A machine cannot state "Nimbus Notes is a note-taking app" from the site's own words.
- **Framework tags:** entity-clarity
- **Flow:** crawl:site
- **Locator:** site:entity
- **Personas hit:** n/a
- **Observed:**
  - Homepage defines the product by jargon: "A bi-directional sync graph with a zero-knowledge vault".
  - Titles on /about.html and /privacy.html are bare "Nimbus Notes"; no `og:site_name` on any page.
  - Name and maker are consistent ("Nimbus Notes"/"Nimbus Notes Ltd"), but category is never stated.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
  > "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
- **Repro:**
  1. Read h1, meta description and first paragraph of `/`; no category noun such as "note-taking app".
- **Fix:** Open the homepage and meta description with "Nimbus Notes is a note-taking app for teams that…" and set `og:site_name`.

### e49d6dbd783c — Testimonials are unattributed so no claim can be credited to a named source
- **Severity:** P3
- **So what:** Quotes from "a happy customer" cannot be attributed, so an engine has no source to name.
- **Framework tags:** attribution
- **Flow:** crawl:page
- **Locator:** /#proof
- **Personas hit:** n/a
- **Observed:**
  - 3 blockquotes, none with a name, role, company or `Review` markup.
- **Evidence:** `crawl/html/1-index.html`
  > "10/10 would recommend." — anonymous
- **Repro:**
  1. Open `crawl/html/1-index.html`, section `#proof`.
- **Fix:** Attribute each quote to a named person and company, or remove the section; add `Review` markup only for real, named reviews.

### d881d6c3fa06 — llms.txt is absent (404)
- **Severity:** P3
- **So what:** No machine-readable site summary pointing agents at canonical pages; an emerging convention with uneven support.
- **Framework tags:** llms-txt
- **Flow:** crawl:site
- **Locator:** /llms.txt
- **Personas hit:** n/a
- **Observed:**
  - `llms_txt.present: false`, status 404.
- **Evidence:** `crawl/site.json`
  > "llms_txt": {"present": false, "status": 404}
- **Repro:**
  1. Request /llms.txt.
- **Fix:** Add /llms.txt with a one-line description of Nimbus Notes and links to /about.html, /pricing.html and /privacy.html.

---

## Dropped for want of evidence
- Whether any engine currently cites the site — out of scope; no evidence obtainable in v1.

## For other lenses
- Pricing page `noindex`, missing canonicals, missing meta descriptions, unreachable sitemap, 404 on /features.html — seo.
- Demo form asks for phone number and company before any pricing — conversion.

## Coverage gaps
- /app/login.html not crawled (robots.txt disallow /app/); two off-domain assets not crawled.
- /features.html returned 404, so no feature content was assessed.
- Live answer-engine behaviour not queried (v1 scope).
