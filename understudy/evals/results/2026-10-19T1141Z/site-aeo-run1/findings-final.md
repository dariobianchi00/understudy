# Nimbus Notes — aeo findings — Run 2026-10-19 (fixture01)

## Method
- Framework: extractability of schema.org, answer blocks, entity clarity, llms.txt (static markup only; no live engines queried)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens (manifest persona_mode: generic)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Not-crawled list read first: /app/ (robots), 2 off-domain assets; none bears on AEO

---

## Findings

### 7f339929e6d7 — No Organization schema on any of 4 crawled pages, so the publisher cannot be attributed
- **Severity:** P1
- **So what:** Engines cannot tie any quoted fact to a named, linked organisation.
- **Framework tags:** schema.org/Organization, attribution
- **Flow:** crawl:site
- **Locator:** site:structured_data
- **Personas hit:** n/a
- **Observed:**
  - Only two JSON-LD blocks exist: SoftwareApplication (homepage, invalid) and FAQPage (/about.html).
  - No `Organization`, `logo`, `sameAs` or `WebSite` anywhere; pricing and privacy have none.
  - Visible facts exist: "Nimbus Notes Ltd", founded 2023, Bristol, company number 14482201.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman"
- **Repro:**
  1. Open `crawl/pages/*.json` and list `structured_data` types.
  2. Confirm no Organization type.
- **Fix:** Add Organization JSON-LD (name, url, logo, sameAs, foundingDate, founder) to every page template, and a WebSite block on the homepage.

### c39c24bc9e51 — Homepage JSON-LD is invalid, so its only structured data cannot be parsed
- **Severity:** P2
- **So what:** The product's only declared schema is discarded; the Offer price is empty.
- **Framework tags:** schema.org/SoftwareApplication, JSON-LD validity
- **Flow:** crawl:page
- **Locator:** / script[type=application/ld+json]
- **Personas hit:** n/a
- **Observed:**
  - Crawl recorded `valid: false`, error "Expecting value: line 1 column 111".
  - Block ends `"price": }` and is also unclosed; no applicationCategory.
  - Validity overlap with seo lens noted once; reported here because it blocks extraction.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "\"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open `crawl/html/1-index.html`, read the ld+json script.
  2. Parse it as JSON; it fails.
- **Fix:** Rewrite as valid SoftwareApplication JSON-LD with applicationCategory and a real Offer price, or drop the Offer until pricing is public.

### 192306b8b7ae — FAQPage schema covers 2 of the 3 visible FAQ answers
- **Severity:** P3
- **So what:** Schema and page disagree on scope; the data-storage answer is unmarked.
- **Framework tags:** schema.org/FAQPage, schema-content parity
- **Flow:** crawl:page
- **Locator:** /about.html FAQPage
- **Personas hit:** n/a
- **Observed:**
  - Page has 3 question-shaped `h3` blocks; JSON-LD lists 2 questions.
  - Present answers lead with "Yes." and stand alone — good extractable blocks.
  - Missing: "Where is my data stored?"
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Compare `answer_blocks` (3) to FAQPage `mainEntity` (2) in `crawl/pages/4-about.json`.
- **Fix:** Add the "Where is my data stored?" Question/Answer to the FAQPage mainEntity; name the subject ("Nimbus Notes stores data in…").

### 0f5a823a7279 — Pricing page states no price or plan facts an engine could quote
- **Severity:** P2
- **So what:** A pricing question yields nothing quotable; the only sentence is non-committal.
- **Framework tags:** answer blocks, Product/Offer schema
- **Flow:** crawl:page
- **Locator:** /pricing.html main
- **Personas hit:** n/a
- **Observed:**
  - Three plan cards (Starter, Team, Enterprise) carry one-line blurbs and "Contact sales"; no amounts.
  - 0 headings below h1 (two h1s), no schema, `robots: noindex`; answer_blocks empty.
  - Quote below is the entire pricing explanation.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/html/3-pricing.html`; search for a currency amount.
- **Fix:** Publish a price or range per plan, with a question heading ("How much does Nimbus Notes cost?") and matching Offer schema.

### 0c57810ca1d6 — Entity is named three ways and its category is never stated in plain words
- **Severity:** P2
- **So what:** A machine cannot say plainly "Nimbus Notes is a note-taking app made by Nimbus Notes Ltd".
- **Framework tags:** entity clarity, og:site_name
- **Flow:** crawl:site
- **Locator:** site:entity-naming
- **Personas hit:** n/a
- **Observed:**
  - Names: "Nimbus Notes", "Nimbus Notes Ltd", "Nimbus"; titles on /about.html and /privacy.html are just "Nimbus Notes"; no `og:site_name` (og empty on all pages).
  - Category wording is jargon: "A bi-directional sync graph with a zero-knowledge vault".
  - Only /about.html names the company, founder and location.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html` · `crawl/html/4-about.html`
  > "Nimbus remembers everything so you never start from zero."
- **Repro:**
  1. Grep html for "Nimbus"; list variants.
  2. Check `og` in each page JSON (all `{}`).
- **Fix:** Use one name, add og:site_name, and open the homepage with "Nimbus Notes is a note-taking app for teams, made by Nimbus Notes Ltd."

### d370691445e9 — Homepage has zero question-shaped headings, so zero extractable answer blocks
- **Severity:** P2
- **So what:** The homepage offers no self-contained answer to lift; its claims are marketing prose.
- **Framework tags:** answer blocks
- **Flow:** crawl:page
- **Locator:** / main h2
- **Personas hit:** n/a
- **Observed:**
  - h2s: "How it works", "Loved by teams", "Book a demo"; `answer_blocks` is empty.
  - Testimonials are unattributable: "a happy customer", "anonymous".
  - Pricing, privacy and 404 pages also have 0 blocks; only /about.html has 3.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "\"It changed how we work.\" — a happy customer"
- **Repro:**
  1. Read `answer_blocks` in `crawl/pages/1-index.json` and the h2 list.
- **Fix:** Add a short FAQ section to the homepage with question headings (e.g. "What is Nimbus Notes?") whose answers lead with the answer and name the subject.

### 8e4d8f38d4d6 — No llms.txt at the site root
- **Severity:** P3
- **So what:** Agents get no curated summary or pointer to canonical pages; an emerging convention, low urgency.
- **Framework tags:** llms.txt
- **Flow:** crawl:site
- **Locator:** /llms.txt
- **Personas hit:** n/a
- **Observed:**
  - `llms_txt.present: false`, status 404.
  - Declared sitemap is also unreachable (404) — seo lens's matter.
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Request `/llms.txt`; receive 404.
- **Fix:** Publish /llms.txt with a one-paragraph description and links to /about.html, /pricing.html and the privacy page.

---

## Dropped for want of evidence
- Whether any engine cites Nimbus Notes today — out of v1 scope; no evidence obtainable.

## For other lenses
- Pricing page has two h1s and `noindex`; /privacy.html has no h1; no canonicals — seo.
- Declared sitemap returns 404 — seo.
- Cookie banner and "Contact sales" for all plans — conversion/trust.

## Coverage gaps
- /features.html returned 404; /app/ disallowed; no live answer-engine queries (not in v1).

## Appendices
- A. Persona debriefs — not used by this lens
- B. Session timelines — not used by this lens
- C. Screenshot index — not used by this lens
