# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: static-markup extractability — schema.org, answer blocks, entity clarity, llms.txt
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (not used by this lens)
- Scoring model: sonnet
- Scope: extractability only; no live answer engines queried, nothing claimed about current citation
- Not-crawled list read first: /app/login.html (robots), 2 off-domain assets — no absence claimed for them
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 70e4d2a71d16 — No Organization schema anywhere on the site
- **Severity:** P1
- **So what:** A machine cannot attribute any quoted claim to a named publisher, so every extraction is unattributable.
- **Framework tags:** schema-coverage, entity-clarity
- **Flow:** crawl:site
- **Locator:** site:organization-schema
- **Personas hit:** n/a
- **Observed:**
  - 0 of 5 crawled pages declare `Organization`; the only types present are `SoftwareApplication` (invalid) and `FAQPage`.
  - No `WebSite` schema either; /about.html states "Nimbus Notes Ltd", Bristol, 2023, Priya Raman only as visible prose.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/pages/1-index.json` · `crawl/html/4-about.html`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman"
- **Repro:**
  1. Open `structured_data` in each of the 5 `crawl/pages/*.json`.
  2. Search for `Organization` — no match.
- **Fix:** Add `Organization` JSON-LD (name "Nimbus Notes Ltd", url, logo, sameAs, foundingDate, founder) site-wide, built from the /about.html facts.

### 8ab7e441def7 — Homepage SoftwareApplication JSON-LD is invalid and unparseable
- **Severity:** P2
- **So what:** The homepage's only structured data is discarded by any parser, so the product has no machine-readable description.
- **Framework tags:** schema-validity
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `"price": }` has no value; the crawl recorded `valid: false`, "Expecting value: line 1 column 111".
  - Block also lacks `applicationCategory`, `description` and `url`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > {"@type": "Offer", "price": }
- **Repro:**
  1. Open `crawl/html/1-index.html`, find the `application/ld+json` script.
  2. Parse it as JSON — fails at column 111.
- **Fix:** Fix the homepage block: give `price` a real value matching the page, and add `applicationCategory` and `description`. Validity overlaps `seo`.

### c5253e965db7 — Homepage and pricing have zero extractable answer blocks
- **Severity:** P2
- **So what:** The questions people ask most (what is it, what does it cost) have no quotable answer on the pages that should hold them.
- **Framework tags:** answer-blocks
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks` is `[]` for `/`, `/pricing.html`, `/privacy.html` — 0 question-shaped headings; h2s are "How it works", "Loved by teams", "Book a demo".
  - /pricing.html shows no price or `Offer`: "Pricing depends on your workspace type and sync topology."
  - Homepage prose cannot be lifted out: "Nimbus remembers everything so you never start from zero."
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Read `answer_blocks` in `crawl/pages/1-index.json`, `3-pricing.json`, `5-privacy.json`.
  2. Read the h2 lists — none is a question.
- **Fix:** Add question headings with a one-sentence answer under each, e.g. "What does Nimbus Notes cost?" on /pricing.html with plan prices stated.

### 1d563e6b5690 — FAQPage schema covers 2 of the 3 visible FAQ answers
- **Severity:** P2
- **So what:** Engines reading the schema miss the data-residency answer that the visible page gives.
- **Framework tags:** schema-coverage, answer-blocks
- **Flow:** crawl:page
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - Visible h3 questions: 3; `FAQPage.mainEntity` entries: 2. "Where is my data stored?" is not marked up.
  - The three visible answers themselves are self-contained and lead with the answer — good.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Count `Question` items in the JSON-LD in `crawl/html/4-about.html` (2).
  2. Count h3 questions under "Frequently asked questions" (3).
- **Fix:** Add the "Where is my data stored?" `Question` and `Answer` to the FAQPage JSON-LD on /about.html.

### 423e7cb5ece4 — Entity is not stated unambiguously: no plain category, name variants, no sameAs
- **Severity:** P2
- **So what:** A machine asked "what is Nimbus Notes?" has only jargon to quote and cannot tie it to the company.
- **Framework tags:** entity-clarity
- **Flow:** crawl:site
- **Locator:** site:entity-clarity
- **Personas hit:** n/a
- **Observed:**
  - No page calls it a note-taking app; homepage says "A bi-directional sync graph with a zero-knowledge vault".
  - `og` is empty on all 5 pages (no `og:site_name`); titles vary: "Nimbus Notes — Your thoughts, everywhere." vs bare "Nimbus Notes" on /about.html and /privacy.html. Footer says "Nimbus Notes Ltd (fictional)".
  - No `sameAs` links anywhere.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/html/1-index.html`
  > "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
- **Repro:**
  1. Read `og` and `title` in each `crawl/pages/*.json`.
  2. Search the HTML for "note-taking" — no match.
- **Fix:** Open the homepage hero with "Nimbus Notes is a note-taking app …", set `og:site_name`, and add `sameAs` in Organization schema.

### 4e2f4bfc0532 — llms.txt is absent
- **Severity:** P3
- **So what:** Agents get no curated summary or canonical page list; support for the convention is uneven, so the cost is small.
- **Framework tags:** llms-txt
- **Flow:** crawl:site
- **Locator:** /llms.txt
- **Personas hit:** n/a
- **Observed:**
  - `llms_txt.present` is false, status 404.
- **Evidence:** `crawl/site.json`
  > "llms_txt": {"present": false, "status": 404
- **Repro:**
  1. Request /llms.txt — 404.
- **Fix:** Publish /llms.txt: one-line description of Nimbus Notes plus links to /about.html and /pricing.html.

---

## Dropped for want of evidence
- Whether engines currently cite or misquote Nimbus Notes — out of scope; no live engine was queried.

## For other lenses
- /pricing.html carries `noindex` and two `h1`s; sitemap 404 and no canonicals — seo
- Pricing page shows no prices, only "Contact sales" — conversion
- /features.html is a 404 linked from every nav — technical

## Coverage gaps
- /app/login.html not crawled (robots.txt); off-domain assets not crawled
- /features.html returned 404, so any product-feature content was not assessable

## Appendices
- A. Persona debriefs — not used by this lens
- B. Session timelines — not used by this lens
- C. Screenshot index — not used by this lens
