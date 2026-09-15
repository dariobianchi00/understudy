# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: AEO extractability — schema.org coverage, answer-block self-containment, entity clarity, llms.txt
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens; `persona_mode` is `generic` in manifest
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- **Out of scope, stated once:** no live answer engine was queried; no finding here claims the site is or is not cited today

---

## Findings

### 0b4c2b1364e2 — No Organization schema anywhere on the site
- **Severity:** P1
- **So what:** An answer engine has no structured way to confirm who makes Nimbus Notes, so any attribution it gives is guessed from prose, not asserted by the site.
- **Framework tags:** schema-coverage, entity-clarity
- **Flow:** crawl:site
- **Locator:** crawl/pages/ (all pages, structured_data)
- **Personas hit:** n/a
- **Observed:**
  - None of the 5 crawled pages (`1-index.json`, `2-features.json`, `3-pricing.json`, `4-about.json`, `5-privacy.json`) contain an `Organization` type in `structured_data`.
  - The entity facts exist only as prose on the About page: "Nimbus Notes is made by **Nimbus Notes Ltd**, a company of eight people founded in **2023** by **Priya Raman**... Company number 14482201."
  - No `sameAs` links to an external, canonical definition of the entity appear anywhere in the crawl.
- **Evidence:** `crawl/pages/1-index.json:27-33` · `crawl/pages/4-about.json:25-33` · `crawl/html/4-about.html:10`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman and based at 14 Harbourside Walk, Bristol, United Kingdom. Company number 14482201."
- **Repro:**
  1. Open `crawl/pages/1-index.json`, `4-about.json`, and the remaining three page records.
  2. Inspect each `structured_data` array for a `@type` of `Organization`.
  3. None is present; the only types present are an invalid `SoftwareApplication` (home) and a valid `FAQPage` (about).
- **Fix:** Add a site-wide `Organization` JSON-LD block (name, url, logo, sameAs) using the facts already published in the About page prose.

### 31b983e2b07f — Homepage only structured data block is invalid JSON-LD
- **Severity:** P2
- **So what:** The homepage is the entity's primary page and its only schema attempt fails to parse, so it contributes zero machine-readable facts.
- **Framework tags:** schema-coverage, invalid-json-ld
- **Flow:** crawl:page
- **Locator:** crawl/pages/1-index.json structured_data
- **Personas hit:** n/a
- **Observed:**
  - `structured_data[0].valid` is `false`, with crawl-recorded error `"Expecting value: line 1 column 111"`.
  - The raw JSON-LD is truncated mid-object: `{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Nimbus Notes", "offers": {"@type": "Offer", "price": }`.
  - This is the only structured-data block on the homepage; no other schema is present to fall back on.
- **Evidence:** `crawl/pages/1-index.json:28-32` · `crawl/html/1-index.html:3`
  > "Expecting value: line 1 column 111"
- **Repro:**
  1. Open `crawl/pages/1-index.json`, field `structured_data[0]`.
  2. Note `"valid": false` and the truncated `"price": }` in `raw`.
- **Fix:** Complete the `Offer.price` value (and `priceCurrency`) or remove the incomplete block until it validates. Note for SEO: JSON-LD validity is shared ground with the seo lens; this finding is scored here only for its effect on extraction.

### 6ec746df805e — Homepage has zero extractable answer blocks
- **Severity:** P2
- **So what:** An answer engine summarizing "what is Nimbus Notes" from the homepage has nothing question-shaped to quote — only slogans and unattributed testimonials.
- **Framework tags:** answer-blocks
- **Flow:** crawl:page
- **Locator:** crawl/pages/1-index.json answer_blocks
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks` is `[]` for the homepage.
  - The three `h2`s are "How it works", "Loved by teams", "Book a demo" — none is question-shaped.
  - The only claim-like content is three testimonials: `"It changed how we work." — a happy customer`, `"Finally, notes that sync." — a user`, `"10/10 would recommend." — anonymous`.
- **Evidence:** `crawl/pages/1-index.json:17-21,50` · `crawl/html/1-index.html:24-26`
  > "It changed how we work." — a happy customer
- **Repro:**
  1. Open `crawl/pages/1-index.json`; `h2` array and `answer_blocks: []`.
  2. Open `crawl/html/1-index.html`, section `#proof`, for the raw testimonial markup.
- **Fix:** Add 2-3 question-shaped subheadings on the homepage ("What is Nimbus Notes?", "Who is it for?") each followed by a self-contained one-paragraph answer.

### 34d40361c0f4 — About page FAQPage schema omits one of three visible Q&A pairs
- **Severity:** P2
- **So what:** A visitor's third question is answered on the page but invisible to any engine reading only the structured data, so it will not surface as a cited answer.
- **Framework tags:** schema-coverage, answer-blocks
- **Flow:** crawl:page
- **Locator:** crawl/pages/4-about.json structured_data mainEntity
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks` on the About page lists 3 Q&A pairs, including "Where is my data stored?" / "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
  - The `FAQPage` JSON-LD `mainEntity` array contains only 2 `Question` entries — "Does Nimbus Notes work offline?" and "Can I export my notes?".
  - The third question exists in the visible HTML (`<h3>Where is my data stored?</h3>`) but not in the `<script type="application/ld+json">` block.
- **Evidence:** `crawl/pages/4-about.json:27,47-59` · `crawl/html/4-about.html:3,16-17`
  > "Where is my data stored?" / "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Open `crawl/pages/4-about.json`, compare `answer_blocks` (3 entries) against `structured_data[0].raw` `mainEntity` (2 entries).
  2. Confirm the third heading/paragraph pair in `crawl/html/4-about.html` lines 16-17.
- **Fix:** Add the "Where is my data stored?" question and answer to the `FAQPage` `mainEntity` array so all three visible Q&A pairs are marked up.

### 3279d7d22788 — Pricing page has no Product or Offer schema for its three plans
- **Severity:** P2
- **So what:** An answer engine cannot state what Nimbus Notes' plans are called or what they include, because no structured data exists on the one page whose job is to answer that.
- **Framework tags:** schema-coverage
- **Flow:** crawl:page
- **Locator:** crawl/pages/3-pricing.json structured_data
- **Personas hit:** n/a
- **Observed:**
  - `structured_data` is `[]` on the pricing page.
  - The page names three tiers — Starter, Team, Enterprise — with one feature line each ("SSO, audit log, vault residency" for Enterprise) but no `Product` or `Offer` markup.
  - Every tier's only call to action is "Contact sales"; no price appears anywhere on the page.
- **Evidence:** `crawl/pages/3-pricing.json:24` · `crawl/html/3-pricing.html:11-16`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/pages/3-pricing.json`; `structured_data: []`.
  2. Open `crawl/html/3-pricing.html`, the three `.price-card` divs, for the plan names and features with no accompanying schema.
- **Fix:** Add `Product`/`Offer` schema per tier naming the plan and its included features, even where price is "Contact sales".

### 654d5bf2bef4 — llms.txt is absent
- **Severity:** P3
- **So what:** Agents that check for an `llms.txt` convention get nothing pointing them at canonical pages or a plain-language site description.
- **Framework tags:** llms-txt
- **Flow:** crawl:site
- **Locator:** crawl/site.json llms_txt
- **Personas hit:** n/a
- **Observed:**
  - `llms_txt.present` is `false`, `status` is `404`, `content` is `null`.
- **Evidence:** `crawl/site.json:24-28`
  > "\"llms_txt\": {\"present\": false, \"status\": 404, \"content\": null}"
- **Repro:**
  1. Open `crawl/site.json`, field `llms_txt`.
- **Fix:** Publish an `llms.txt` at the root describing the product and linking the About, Pricing and FAQ pages.

### dfe173205902 — Homepage testimonials are unattributed and uncitable
- **Severity:** P3
- **So what:** Three customer quotes carry no name or source, so an answer engine cannot cite them as evidence of anything.
- **Framework tags:** answer-blocks, entity-clarity
- **Flow:** crawl:page
- **Locator:** crawl/html/1-index.html proof section
- **Personas hit:** n/a
- **Observed:**
  - All three blockquotes in the `#proof` section are attributed only to "a happy customer", "a user", and "anonymous".
  - No name, company, or link accompanies any of the three quotes.
- **Evidence:** `crawl/html/1-index.html:24-26`
  > "10/10 would recommend." — anonymous
- **Repro:**
  1. Open `crawl/html/1-index.html`, section `#proof`.
- **Fix:** Replace at least one testimonial with a named, attributable customer (name, role, company) or remove the section.

---

## Dropped for want of evidence
- Whether the pricing tiers differ in actual capability beyond the one Enterprise line — the crawl recorded only "SSO, audit log, vault residency" for Enterprise and no feature list for Starter/Team.

## For other lenses
- Pricing page carries `<meta name="robots" content="noindex">` — seo.
- Pricing page has two `<h1>` elements and `heading_order_valid: false` — seo.
- Homepage loads a tracking script and font CDN from off-domain hosts recorded as not-crawled — technical.
- Sitemap declared in robots.txt returns 404 with 0 URLs — seo.
- JSON-LD syntax validity is shared ground with seo; flagged here only where it affects extraction (see finding `31b983e2b07f`).

## Coverage gaps
- `/app/login.html` — not crawled, disallowed by robots.txt (`/app/`). Auth-walled surface, not reported as a finding per policy.
- `https://analytics.example-tracker.test/t.js` and `https://fonts.example-cdn.test/all.css` — off-domain, not crawled; neither carries entity or answer content.
- `features.html` returned 404; any answer content intended for that page was not observed.

## Appendices
- A. Persona debriefs — n/a, no-persona lens.
- B. Session timelines — n/a, static crawl only.
- C. Screenshot index — n/a, this lens scores recorded markup, not rendered screenshots.
