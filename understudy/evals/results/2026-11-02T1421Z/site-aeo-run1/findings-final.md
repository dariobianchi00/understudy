# Nimbus Notes — aeo findings — Run 2026-11-02 (fixture01)

## Method
- Framework: AEO extractability — schema.org, answer blocks, entity clarity, llms.txt (static markup only)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a (no-persona lens)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope: live answer engines were not queried; nothing here speaks to current citation

---

## Findings

### 252b2f60d648 — No Organization schema on any of 5 crawled pages, so the publisher cannot be attributed from markup
- **Severity:** P1
- **So what:** An engine quoting the site has no machine-readable name, url, logo or sameAs to attribute to.
- **Framework tags:** schema.org Organization, attribution
- **Flow:** crawl:site
- **Locator:** site:organization-schema
- **Personas hit:** n/a
- **Observed:**
  - Only types found: SoftwareApplication (invalid, home) and FAQPage (about); 3 pages have none.
  - No Organization, WebSite or BreadcrumbList anywhere.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/html/4-about.html`
- **Repro:**
  1. Open each crawl/pages/*.json and read structured_data.
- **Fix:** Add one Organization JSON-LD block (name "Nimbus Notes Ltd", url, logo, sameAs) to the shared page template.

### 240d84554632 — Home page's only JSON-LD block is invalid and unparseable, leaving the page with zero usable structured data
- **Severity:** P2
- **So what:** The highest-traffic page declares a SoftwareApplication that no parser can read, so price and product facts are lost.
- **Framework tags:** schema.org validity (overlaps seo)
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - Crawl recorded valid=false: "Expecting value: line 1 column 111".
  - The Offer has `"price": }` with no value.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "\"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Read structured_data[0] in crawl/pages/1-index.json.
- **Fix:** Fix the JSON in index.html: supply a real price or remove the Offer, then add applicationCategory and operatingSystem.

### 6fec245ffdc5 — Pricing page states no prices and carries no schema, so no cost answer can be extracted
- **Severity:** P2
- **So what:** "What does Nimbus Notes cost?" has no quotable answer anywhere on the site.
- **Framework tags:** answer blocks, Product/Offer schema
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - 3 plan cards (Starter, Team, Enterprise) each only say "Contact sales"; no figures.
  - structured_data is empty; 0 answer blocks; robots meta is noindex.
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Read answer_blocks and structured_data in crawl/pages/3-pricing.json.
- **Fix:** Publish prices per plan in text, add an Offer per plan in JSON-LD, and add a "How much does Nimbus Notes cost?" heading with a one-sentence answer.

### 5fd508a97c76 — Home page has zero extractable answer blocks and never says in plain words what category Nimbus Notes is
- **Severity:** P2
- **So what:** The home page is marketing prose; nothing on it can be lifted as a self-contained answer.
- **Framework tags:** answer blocks, entity clarity
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - answer_blocks is empty; h2s are "How it works", "Loved by teams", "Book a demo", none question-shaped.
  - Describes the product as "A bi-directional sync graph with a zero-knowledge vault"; the words note-taking app do not appear.
  - Testimonials unattributed: "— a happy customer", "— anonymous".
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "Nimbus remembers everything so you never start from zero."
- **Repro:**
  1. Read answer_blocks and h2 in crawl/pages/1-index.json.
- **Fix:** Add a first sentence "Nimbus Notes is a note-taking app that…" and a question-headed block such as "What is Nimbus Notes?".

### a6d64e075cd3 — Entity facts sit only in one About paragraph, with no sameAs, og:site_name or consistent page titles
- **Severity:** P2
- **So what:** A machine cannot state who makes Nimbus Notes without parsing prose on a single page.
- **Framework tags:** entity clarity, sameAs
- **Flow:** crawl:site
- **Locator:** site:entity-identity
- **Personas hit:** n/a
- **Observed:**
  - Legal name, founder, year and address appear only in /about.html prose; og is empty on all 5 pages.
  - Titles "Nimbus Notes" on About and Privacy, "Nimbus Notes — Your thoughts, everywhere." on home; footer adds "(fictional)".
  - No external profile links (sameAs) on any page.
- **Evidence:** `crawl/html/4-about.html` · `crawl/pages/5-privacy.json`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman"
- **Repro:**
  1. Compare og, title and external_links across crawl/pages/*.json.
- **Fix:** Put the About facts in Organization JSON-LD, add og:site_name "Nimbus Notes", and link official profiles via sameAs.

### 10167baf79c4 — FAQPage schema lists 2 of the 3 visible FAQ answers, leaving the data-storage answer unmarked
- **Severity:** P3
- **So what:** The EU-storage answer is visible but only extractable as unmarked HTML, a minor inconsistency.
- **Framework tags:** FAQPage, schema/content mismatch
- **Flow:** crawl:page
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - 3 answer blocks recorded; JSON-LD mainEntity has 2 Questions.
  - Visible Q3 "Where is my data stored?" is absent from the schema.
  - The 3 answers that exist are self-contained and lead with the answer.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Count mainEntity items vs answer_blocks in crawl/pages/4-about.json.
- **Fix:** Add the "Where is my data stored?" Question to the FAQPage JSON-LD in about.html.

### 8e4d8f38d4d6 — No llms.txt at the site root
- **Severity:** P3
- **So what:** Agents get no curated map of canonical pages; an emerging convention with uneven support.
- **Framework tags:** llms.txt
- **Flow:** crawl:site
- **Locator:** /llms.txt
- **Personas hit:** n/a
- **Observed:**
  - site.json: llms_txt present=false, status 404.
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Request /llms.txt; 404.
- **Fix:** Publish /llms.txt describing Nimbus Notes in two lines, linking /about.html and a pricing page with real prices.

---

## Dropped for want of evidence
- Whether the site is cited by any answer engine — out of scope; no evidence obtainable.

## For other lenses
- Missing canonicals, noindex on /pricing.html, dead sitemap, /features.html 404, two h1 on pricing — seo.

## Coverage gaps
- /app/ disallowed by robots.txt; /features.html returned 404; v1 does not query live answer engines.

## Appendices
- A. Persona debriefs — n/a
- B. Session timelines — n/a
- C. Screenshot index — n/a
