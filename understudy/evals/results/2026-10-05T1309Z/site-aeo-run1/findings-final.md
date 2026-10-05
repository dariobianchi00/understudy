# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: schema.org coverage, answer-block extractability, entity clarity, llms.txt — extractability only, never citation
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (not used by this lens)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Not crawled (read first): /app/login.html (robots.txt), two off-domain assets; /features.html returned 404
- Structured-data validity is shared with seo; reported here only where it blocks extraction

---

## Findings

### 804269d6e3e5 — No Organization schema on any of the 5 crawled pages, so no machine-readable publisher, logo or sameAs
- **Severity:** P1
- **So what:** An engine cannot attribute claims to a named publisher from markup; identity facts live only in /about.html prose.
- **Framework tags:** AEO-schema, AEO-entity
- **Flow:** crawl:site
- **Locator:** site:structured_data
- **Personas hit:** n/a
- **Observed:**
  - 0 of 5 pages declare Organization; only FAQPage (/about.html) and a broken SoftwareApplication (/) exist.
  - No WebSite, BreadcrumbList or logo/sameAs anywhere.
  - Facts exist only as prose: "made by Nimbus Notes Ltd … founded in 2023 by Priya Raman … Bristol".
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman"
- **Repro:**
  1. Open each `crawl/pages/*.json` and list `structured_data` types.
  2. Observe no Organization type on any page.
- **Fix:** Add an Organization JSON-LD block (name "Nimbus Notes Ltd", url, logo, foundingDate 2023, founder, address, sameAs) to every page template.

### 82bb1301d005 — Homepage JSON-LD is invalid JSON, so the only product schema on the site is unreadable
- **Severity:** P1
- **So what:** The one declaration of what Nimbus Notes is (SoftwareApplication) is discarded by any parser.
- **Framework tags:** AEO-schema
- **Flow:** crawl:page
- **Locator:** / (JSON-LD)
- **Personas hit:** n/a
- **Observed:**
  - Crawl recorded `valid: false`, error "Expecting value: line 1 column 111".
  - The `price` property has no value and the object is unclosed.
  - Overlaps seo on validity; reported here because it removes the product entity.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "\"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open `crawl/html/1-index.html`, find the `application/ld+json` script.
  2. Parse it as JSON; it fails at column 111.
- **Fix:** Rewrite the homepage JSON-LD as valid SoftwareApplication with name, applicationCategory, operatingSystem and a real Offer, or remove price until one is published.

### 2c838d74944d — Pricing page states no price in text or schema, so no plan cost can be quoted
- **Severity:** P2
- **So what:** The most common product question, "what does it cost", has no extractable answer.
- **Framework tags:** AEO-answer-blocks, AEO-schema
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - 0 structured data; 0 answer blocks; 60 words; all three plans point to "Contact sales".
  - Only statement: "Pricing depends on your workspace type and sync topology."
  - The page has `noindex` (seo's concern; noted once).
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/html/3-pricing.html`.
  2. Search for a currency amount; none found.
- **Fix:** Publish a price or "from" price per plan in visible text and mark each up as Offer inside the SoftwareApplication schema.

### afe5dbe1560f — Homepage has zero extractable answer blocks: no question-shaped headings
- **Severity:** P2
- **So what:** The highest-traffic page offers nothing an engine can lift out and quote cleanly.
- **Framework tags:** AEO-answer-blocks
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks` is empty; H2s are "How it works", "Loved by teams", "Book a demo".
  - Answer text depends on context: "Nimbus remembers everything so you never start from zero."
  - Testimonials are unattributed: "— a happy customer", "— anonymous".
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
- **Repro:**
  1. Open `crawl/pages/1-index.json`; read `answer_blocks` and `h2`.
- **Fix:** Add a "What is Nimbus Notes?" H2 with a one-sentence plain-language definition, and attribute testimonials to named people.

### 6db55c7b0103 — FAQPage schema lists 2 questions but the page shows 3, omitting the data-residency answer
- **Severity:** P2
- **So what:** Schema and visible content disagree, so an engine reading schema misses "Where is my data stored?".
- **Framework tags:** AEO-schema, AEO-answer-blocks
- **Flow:** crawl:page
- **Locator:** /about.html (FAQPage)
- **Personas hit:** n/a
- **Observed:**
  - 3 visible Q&As in `answer_blocks`; 2 in `mainEntity`.
  - The three visible answers lead with the answer and stand alone (strength).
  - The missing answer: "In the EU (Frankfurt) by default. Enterprise plans can choose a region." — "Enterprise plans" is unexplained without the pricing page.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Compare `answer_blocks` (3) with the FAQPage `mainEntity` (2) in `crawl/pages/4-about.json`.
- **Fix:** Add the "Where is my data stored?" Question to the FAQPage mainEntity, generated from the same source as the visible list.

### c4a34fba4921 — Entity and category are never stated plainly: no og:site_name, generic titles, jargon-only description
- **Severity:** P2
- **So what:** A machine cannot state in one line that Nimbus Notes is a note-taking app, nor reconcile the name across pages.
- **Framework tags:** AEO-entity
- **Flow:** crawl:site
- **Locator:** site:entity
- **Personas hit:** n/a
- **Observed:**
  - `og` is empty on 5 of 5 pages; no og:site_name.
  - Titles vary: "Nimbus Notes — Your thoughts, everywhere.", "Nimbus Notes" (x2), "Pricing — Nimbus Notes".
  - Category appears only as "bi-directional sync graph with a zero-knowledge vault"; "note-taking app" is not stated.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
  > "Nimbus Notes keeps every thought in a bi-directional sync graph with a zero-knowledge vault."
- **Repro:**
  1. Read `og`, `title` and `meta_description` across `crawl/pages/*.json`.
- **Fix:** Add og:site_name "Nimbus Notes" and rewrite the homepage description to open "Nimbus Notes is a note-taking app that …".

### d881d6c3fa06 — llms.txt is absent (404)
- **Severity:** P3
- **So what:** Agents get no curated summary or canonical page list; emerging convention, so low weight.
- **Framework tags:** AEO-llms-txt
- **Flow:** crawl:site
- **Locator:** /llms.txt
- **Personas hit:** n/a
- **Observed:**
  - `llms_txt.present` is false, status 404.
- **Evidence:** `crawl/site.json`
  > "llms_txt": {"present": false, "status": 404}
- **Repro:**
  1. Request `/llms.txt` at the site root.
- **Fix:** Publish /llms.txt with a two-line description of Nimbus Notes and links to /about.html and /pricing.html.

---

## Dropped for want of evidence
- Whether any answer engine cites Nimbus Notes today — out of scope; no live querying in v1.

## For other lenses
- Pricing page has two H1s and `noindex`; sitemap declared on a different host returns 404 — seo.
- Unattributed testimonials, "(fictional)" in footer — trust.
- Pricing hidden behind "Contact sales" — conversion.

## Coverage gaps
- /features.html returned 404 and was not assessable.
- /app/login.html disallowed by robots.txt.
- Live answer engines not queried (not in v1).
