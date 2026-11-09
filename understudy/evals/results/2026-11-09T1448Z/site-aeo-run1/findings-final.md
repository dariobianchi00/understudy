# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: AEO v1 — schema.org coverage, answer-block extractability, entity clarity, llms.txt (static markup only)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (not used by this lens)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope: no live answer engines queried; nothing here says whether the site is cited today

---

## Findings

### f67ddba4ba56 — No Organization schema on any page, so no machine-readable publisher identity
- **Severity:** P1
- **So what:** An answer engine cannot attribute any claim to a named publisher with a logo, URL or sameAs links.
- **Framework tags:** AEO-schema, AEO-entity
- **Flow:** crawl:site
- **Locator:** site:organization-schema
- **Personas hit:** n/a
- **Observed:**
  - 0 of 5 crawled pages declare `Organization`; only 2 pages carry any JSON-LD.
  - Visible text names "Nimbus Notes Ltd", Bristol, founder Priya Raman, company number 14482201 — none of it in schema.
  - No `sameAs`, `logo` or `WebSite` schema anywhere.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/html/4-about.html:10`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman"
- **Repro:**
  1. Open `crawl/pages/*.json` and list `structured_data` types.
  2. Observe only an invalid SoftwareApplication and a FAQPage; no Organization.
- **Fix:** Add `Organization` JSON-LD site-wide with name "Nimbus Notes Ltd", url, logo, foundingDate 2023, founder, address and sameAs profile links.

### 45783deb97cd — Homepage SoftwareApplication JSON-LD is invalid and cannot be parsed
- **Severity:** P2
- **So what:** The only product schema on the site is discarded by parsers, so the product has no machine-readable description.
- **Framework tags:** AEO-schema
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - Crawl recorded `valid: false`, error "Expecting value: line 1 column 111".
  - `"price": }` has no value and the object is never closed.
  - Overlaps seo on validity; reported here for its effect on extraction.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:3`
  > "\"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open `crawl/html/1-index.html` line 3.
  2. Parse the ld+json block as JSON; it fails.
- **Fix:** Rewrite the block as valid JSON with applicationCategory, a real Offer price/priceCurrency matching the pricing page, and close all braces.

### ac746a1afe67 — FAQPage schema omits one of the three visible FAQ answers
- **Severity:** P2
- **So what:** Engines reading schema get 2 answers and miss the data-residency answer, which is the one buyers ask most.
- **Framework tags:** AEO-schema, AEO-answer-blocks
- **Flow:** crawl:page
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - Page shows 3 question headings; `FAQPage.mainEntity` holds 2 Questions.
  - Missing: "Where is my data stored?" — "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
  - The 3 visible blocks are otherwise self-contained and lead with the answer.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html:16`
  > "Where is my data stored?"
- **Repro:**
  1. Compare `answer_blocks` (3) with `structured_data[0]` mainEntity (2) in `crawl/pages/4-about.json`.
- **Fix:** Add the third Question/Answer to the FAQPage block, and generate schema from the same source as the visible FAQ.

### afe5dbe1560f — Homepage has zero extractable answer blocks and no question-shaped headings
- **Severity:** P2
- **So what:** The highest-traffic page offers nothing an engine can lift as a standalone answer to "what is Nimbus Notes?".
- **Framework tags:** AEO-answer-blocks
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks` is empty; H2s are "How it works", "Loved by teams", "Book a demo".
  - Copy is marketing prose that depends on context: "Nimbus remembers everything so you never start from zero."
  - Only 1 of 5 pages (about.html) has answer blocks (3).
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:11`
  > "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
- **Repro:**
  1. Open `crawl/pages/1-index.json`; read `h2` and `answer_blocks`.
- **Fix:** Add a "What is Nimbus Notes?" H2 with a two-sentence plain answer naming maker and category, plus a short FAQ on the homepage.

### ffa3fe52687a — Pricing page gives no extractable price or plan answer and has no schema
- **Severity:** P2
- **So what:** Asked what Nimbus Notes costs, an engine finds no figure, plan detail or Offer data to quote.
- **Framework tags:** AEO-schema, AEO-answer-blocks
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `structured_data` empty; 0 H2s; 60 words; three plan cards all say "Contact sales".
  - Only pricing statement: "Pricing depends on your workspace type and sync topology."
  - Page also carries `noindex` (seo's finding; noted only as context).
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html:16`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/html/3-pricing.html`; search for a currency figure — none.
- **Fix:** Publish a price or starting price per plan in text, add `Offer` schema matching it, and add "How much does Nimbus Notes cost?" as a heading with a direct answer.

### 5348aa76f417 — Entity facts live only in one prose paragraph and the product category is never stated plainly
- **Severity:** P2
- **So what:** Engines cannot state in one clean sentence who makes Nimbus Notes or what kind of product it is.
- **Framework tags:** AEO-entity
- **Flow:** crawl:site
- **Locator:** site:entity-clarity
- **Personas hit:** n/a
- **Observed:**
  - `og` is empty on all 5 pages (no `og:site_name`); titles of about.html and privacy.html are the bare "Nimbus Notes".
  - Category appears only as jargon: "bi-directional sync graph with a zero-knowledge vault"; "note-taking app" is never written.
  - Name is consistent ("Nimbus Notes"); legal entity "Nimbus Notes Ltd" appears only on about.html and in the footer.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/html/1-index.html:3`
  > "Nimbus Notes keeps every thought in a bi-directional sync graph with a zero-knowledge vault."
- **Repro:**
  1. Read `og`, `title`, `meta_description` across `crawl/pages/*.json`.
- **Fix:** Open the homepage and meta description with "Nimbus Notes is a note-taking app made by Nimbus Notes Ltd"; add `og:site_name`.

### db348adca6a3 — Homepage testimonials are unattributed and cannot be quoted as claims
- **Severity:** P3
- **So what:** Quotes name no person or company, so an engine has no one to attribute the claim to.
- **Framework tags:** AEO-answer-blocks, AEO-entity
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - 3 blockquotes attributed to "a happy customer", "a user", "anonymous".
  - No `Review` or `Rating` schema.
- **Evidence:** `crawl/html/1-index.html:24`
  > "\"It changed how we work.\" — a happy customer"
- **Repro:**
  1. Open `crawl/html/1-index.html` lines 24–26.
- **Fix:** Attribute each quote to a named person, role and company with permission, or remove the section.

### 4e2f4bfc0532 — llms.txt is absent
- **Severity:** P3
- **So what:** Agents get no curated summary or canonical page list; an emerging convention with uneven support.
- **Framework tags:** AEO-llms-txt
- **Flow:** crawl:site
- **Locator:** /llms.txt
- **Personas hit:** n/a
- **Observed:**
  - `llms_txt.present` is false, status 404.
- **Evidence:** `crawl/site.json`
  > "llms_txt": {"present": false, "status": 404}
- **Repro:**
  1. Request `/llms.txt`; receive 404.
- **Fix:** Publish `/llms.txt` with a one-paragraph description of Nimbus Notes and links to /, /pricing.html and /about.html.

---

## Dropped for want of evidence
- None.

## For other lenses
- `pricing.html` has `noindex`, two H1s, no meta description — seo.
- `features.html` returns 404 yet is linked in every nav — technical / seo.
- Pricing hides cost behind "Contact sales" — conversion.

## Coverage gaps
- `/app/login.html` not crawled (robots.txt disallow `/app/`); off-domain tracker and font URLs not crawled.
- `features.html` is a 404, so the product-features page could not be assessed.
- Live answer-engine behaviour not tested (out of scope in v1).

## Appendices
- A. Persona debriefs — not used by this lens
- B. Session timelines — not used by this lens
- C. Screenshot index — none cited
