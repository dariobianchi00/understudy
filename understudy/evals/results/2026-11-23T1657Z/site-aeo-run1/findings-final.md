# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: extractability of static markup — schema.org, answer blocks, entity clarity, llms.txt
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (not used by this lens; findings rest on crawl records)
- Scoring model: sonnet
- Scope: static markup only; no live answer engines queried; nothing here claims the site is or is not cited
- Not crawled (read first): `/app/login.html` (robots.txt disallow), two off-domain assets — none bear on extractability
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### af9ec056e9cd — No Organization schema on any of 4 crawled 200 pages, so the publisher cannot be attributed from markup
- **Severity:** P1
- **So what:** A machine has no declared name, url, logo or sameAs to attach the site's claims to.
- **Framework tags:** schema.org Organization, entity clarity
- **Flow:** crawl:site
- **Locator:** crawl/pages/*.json#structured_data
- **Personas hit:** n/a
- **Observed:**
  - Only 2 of 5 crawled pages (home, about) carry any JSON-LD; types are SoftwareApplication (invalid) and FAQPage.
  - The publisher facts exist only as prose on /about.html: "Nimbus Notes Ltd", founded "2023", "Priya Raman", "Bristol", "Company number 14482201".
  - No WebSite, no logo, no sameAs anywhere.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman"
- **Repro:**
  1. Open `crawl/pages/*.json` and list `structured_data[].types`.
  2. Observe no Organization type on any page.
- **Fix:** Add Organization JSON-LD (name, url, logo, sameAs, foundingDate, founder) to the homepage and /about.html, plus WebSite.

### 014a752ceb9a — Homepage JSON-LD is invalid (empty price value), so its only SoftwareApplication data cannot be parsed
- **Severity:** P1
- **So what:** The one block describing the product is discarded by any parser, leaving the homepage with no usable structured data.
- **Framework tags:** schema.org validity (overlap with seo noted once)
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - Crawl records `valid: false`, error "Expecting value: line 1 column 111".
  - The `price` key has no value; even if fixed, there is no `applicationCategory` and no priced Offer on the page to match.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "\"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open `crawl/html/1-index.html` and find the `application/ld+json` script.
  2. Parse it as JSON; it fails at the empty `price`.
- **Fix:** Repair the JSON-LD: give `price` a real value matching the page (or remove `offers`), and add `applicationCategory`.

### 942171b46aa6 — Homepage has zero extractable answer blocks and never names its category in plain words
- **Severity:** P2
- **So what:** An engine asked "what is Nimbus Notes?" finds jargon, not a quotable sentence.
- **Framework tags:** answer blocks, entity clarity
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks` is empty; h2s are "How it works", "Loved by teams", "Book a demo" — none question-shaped.
  - The lead sentence never says "note-taking app": "A bi-directional sync graph with a zero-knowledge vault".
  - Testimonials are unattributable: "— a happy customer", "— anonymous".
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "Nimbus remembers everything so you never start from zero."
- **Repro:**
  1. Read `answer_blocks` and `h2` in `crawl/pages/1-index.json`.
- **Fix:** Add an h2 "What is Nimbus Notes?" answered in one self-contained sentence naming the category; attribute testimonials to named people.

### e7acf8aa606d — Pricing page states no price and carries no Offer schema, so nothing about cost is extractable
- **Severity:** P2
- **So what:** "How much does Nimbus Notes cost?" has no quotable answer anywhere in the crawl.
- **Framework tags:** answer blocks, Product/Offer schema
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - 3 plan cards (Starter, Team, Enterprise), each only "Contact sales"; 0 prices, 0 structured data, 0 answer blocks.
  - No schema-vs-page contradiction exists, because neither side states a price.
  - Page also has two h1s and `noindex` (seo's findings).
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/html/3-pricing.html`; search for a currency amount or `ld+json`; none.
- **Fix:** Publish a price or an explicit "free tier / from $X" statement, then mark up each plan with Offer schema matching it.

### 02949a11cb81 — Entity name is inconsistent across pages and no og:site_name or sameAs exists
- **Severity:** P2
- **So what:** Engines cannot confirm which entity is meant or link it to profiles elsewhere.
- **Framework tags:** entity clarity
- **Flow:** crawl:site
- **Locator:** crawl/pages/*.json#og
- **Personas hit:** n/a
- **Observed:**
  - `og` is empty on all 5 pages; no `og:site_name`.
  - Titles vary: "Nimbus Notes — Your thoughts, everywhere.", "Pricing — Nimbus Notes", bare "Nimbus Notes" on /about.html and /privacy.html.
  - Body mixes "Nimbus Notes", "Nimbus" ("Get the Nimbus newsletter") and legal "Nimbus Notes Ltd".
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json`
  > "Get the Nimbus newsletter"
- **Repro:**
  1. Compare `title` and `og` across `crawl/pages/*.json`.
- **Fix:** Use one product name, set `og:site_name` to it, and add `sameAs` links in Organization schema.

### d24e23c5976d — FAQPage schema lists 2 of the 3 visible questions, leaving the data-location answer unmarked
- **Severity:** P3
- **So what:** The one answer about where data lives is visible but not machine-declared; the other two are well formed.
- **Framework tags:** FAQPage, answer blocks
- **Flow:** crawl:page
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - 3 answer blocks recorded; schema `mainEntity` holds 2.
  - Answers are self-contained and lead with "Yes."; this is the site's only extractable content (3 blocks, 1 page).
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Compare `answer_blocks` (3) with the FAQPage `mainEntity` (2) in `crawl/pages/4-about.json`.
- **Fix:** Add the "Where is my data stored?" Question/Answer to the FAQPage JSON-LD on /about.html.

### d881d6c3fa06 — llms.txt is absent (404)
- **Severity:** P3
- **So what:** No agent-facing summary or canonical-page list exists; an emerging convention with uneven support.
- **Framework tags:** llms.txt
- **Flow:** crawl:site
- **Locator:** /llms.txt
- **Personas hit:** n/a
- **Observed:**
  - `llms_txt.present` is false, status 404.
- **Evidence:** `crawl/site.json`
  > "llms_txt": {"present": false, "status": 404}
- **Repro:**
  1. Request `/llms.txt`; receive 404.
- **Fix:** Publish /llms.txt with a two-line description of Nimbus Notes and links to /about.html, /pricing.html, /privacy.html.

---

## Dropped for want of evidence
- None.

## For other lenses
- Pricing page has `noindex` and two h1s; homepage has no canonical; sitemap URL returns 404 — seo.
- Homepage hero image has empty alt; /features.html 404 — technical/seo.

## Coverage gaps
- /features.html returned 404, so no product-feature content could be assessed.
- Live answer engines not queried (out of v1 scope).

## Appendices
- A. Persona debriefs — not used by this lens
- B. Session timelines — not used by this lens
- C. Screenshot index — not used by this lens
