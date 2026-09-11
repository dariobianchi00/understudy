# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: AEO — schema.org coverage, extractable answer blocks, entity clarity, llms.txt (static markup only, no live answer-engine queries)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens; run `persona_mode` is `generic` (manifest.json) but does not affect this lens
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### f08623d5c2a7 — Homepage only structured data is invalid JSON-LD
- **Severity:** P1
- **So what:** An answer engine parsing the entry page's JSON-LD gets nothing — the only schema block on the homepage fails to parse.
- **Framework tags:** schema-coverage, invalid-jsonld
- **Flow:** crawl:page
- **Locator:** crawl/pages/1-index.json
- **Personas hit:** n/a
- **Observed:**
  - The homepage's `<script type="application/ld+json">` is truncated: `{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Nimbus Notes", "offers": {"@type": "Offer", "price": }` — the `price` key has no value and the object never closes.
  - The crawl recorded it as invalid: `"valid": false, "error": "Expecting value: line 1 column 111"`.
  - No other structured-data block exists on the homepage to fall back on — `structured_data` has exactly this one, broken, entry.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:3`
  > "{\"@context\": \"https://schema.org\", \"@type\": \"SoftwareApplication\", \"name\": \"Nimbus Notes\", \"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open `crawl/pages/1-index.json`.
  2. Read `structured_data[0]` — `valid: false`, `error: "Expecting value: line 1 column 111"`.
- **Fix:** Close the malformed `Offer` object with a real price (or drop the `Offer` block entirely) so the JSON-LD parses.

### dc05824fa0c1 — No Organization schema anywhere on the site
- **Severity:** P1
- **So what:** Nothing on the site declares, in machine-readable form, who this company is — an extractor must parse prose on one page to learn the legal entity.
- **Framework tags:** schema-coverage, entity-clarity
- **Flow:** crawl:site
- **Locator:** site-wide: crawl/pages/1-index.json, crawl/pages/3-pricing.json, crawl/pages/4-about.json, crawl/pages/5-privacy.json
- **Personas hit:** n/a
- **Observed:**
  - `structured_data` across all 5 crawled pages contains only one invalid `SoftwareApplication` (index) and one valid `FAQPage` (about) — no `Organization` type anywhere, including `sameAs`, `logo`, or `url`.
  - `og` is an empty object (`{}`) on every crawled page — no `og:site_name` to cross-check the name either.
  - The only place entity facts (legal name, founder, incorporation number, address) appear at all is unstructured prose on `/about.html`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json` · `crawl/html/4-about.html:10`
  > "Nimbus Notes is made by Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman and based at 14 Harbourside Walk, Bristol, United Kingdom. Company number 14482201."
- **Repro:**
  1. Grep `structured_data` and `og` fields across `crawl/pages/*.json`.
  2. Confirm no entry has `"@type": "Organization"` and every `og` object is empty.
- **Fix:** Add a site-wide `Organization` JSON-LD block (name, url, logo, `sameAs`) built from the facts already stated in the About page prose, and set `og:site_name` consistently.

### 060946b4d283 — FAQPage schema on about.html omits one of three visible Q&A pairs
- **Severity:** P2
- **So what:** An extractor that trusts the FAQPage schema over the raw page will miss the data-residency answer entirely — it has no structured representation.
- **Framework tags:** schema-coverage, answer-blocks
- **Flow:** crawl:page
- **Locator:** crawl/pages/4-about.json
- **Personas hit:** n/a
- **Observed:**
  - `/about.html` visibly shows three question/answer pairs: "Does Nimbus Notes work offline?", "Can I export my notes?", and "Where is my data stored?".
  - The page's `FAQPage` JSON-LD `mainEntity` array contains only the first two `Question` entries; the third has no matching schema entry.
  - The crawl's own `answer_blocks` extraction independently records all three, confirming the DOM content exists regardless of the schema gap.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html:16-17`
  > "Where is my data stored?" / "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Open `crawl/pages/4-about.json`, compare `structured_data[0].raw` (2 Questions) against `answer_blocks` (3 entries).
  2. Confirm the third `answer_blocks` question has no matching `Question` object in the JSON-LD.
- **Fix:** Add the third Question/Answer pair ("Where is my data stored?") to the `FAQPage` JSON-LD `mainEntity` array on `/about.html`.

### 957b4db4be30 — Home, pricing and privacy pages have zero extractable answer blocks
- **Severity:** P2
- **So what:** Three of the five crawled pages have no content an answer engine could lift out and quote directly — only the About page offers any.
- **Framework tags:** answer-blocks
- **Flow:** crawl:site
- **Locator:** crawl/pages/1-index.json, crawl/pages/3-pricing.json, crawl/pages/5-privacy.json
- **Personas hit:** n/a
- **Observed:**
  - `1-index.json`: `answer_blocks: []` — h2s are "How it works", "Loved by teams", "Book a demo", none question-shaped; body is marketing prose ("A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed.").
  - `3-pricing.json`: `answer_blocks: []` — h1s are "Pricing" / "Plans for every team", no h2s, every tier ("Starter", "Team", "Enterprise") shows only a "Contact sales" link, no stated price.
  - `5-privacy.json`: `answer_blocks: []` — single h2 "Privacy", no h1, no question-shaped structure.
  - Only `/about.html` (1 of 5 crawled pages) has any recorded `answer_blocks` (3).
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/pages/5-privacy.json`
  > "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
- **Repro:**
  1. Open `crawl/pages/1-index.json`, `crawl/pages/3-pricing.json`, `crawl/pages/5-privacy.json`.
  2. Confirm `answer_blocks: []` on each and that no `h2`/`h3` is phrased as a question.
- **Fix:** Turn core marketing and pricing claims into question-shaped headings with self-contained answers underneath, following the pattern already proven on `/about.html`.

### c5513bb4e062 — llms.txt is absent
- **Severity:** P3
- **So what:** Agents that check `llms.txt` first find nothing pointing them at a plain-language description of the site or its canonical pages.
- **Framework tags:** llms-txt
- **Flow:** crawl:site
- **Locator:** crawl/site.json
- **Personas hit:** n/a
- **Observed:**
  - `crawl/site.json` records `llms_txt: {"present": false, "status": 404, "content": null}`.
- **Evidence:** `crawl/site.json`
- **Repro:**
  1. Open `crawl/site.json`, read the `llms_txt` object.
- **Fix:** Publish a root `llms.txt` describing Nimbus Notes and linking to the homepage, `/about.html`, and `/pricing.html`.

---

## Dropped for want of evidence
None — every observation pursued had a corresponding crawl or HTML artifact.

## For other lenses
- `/pricing.html` is served with `robots_meta: "noindex"` — indexability, not extraction; SEO's call.
- `/pricing.html` has two `<h1>` elements ("Pricing" and "Plans for every team") — heading structure, SEO's call.
- The primary nav's "Features" link 404s on every page (`/features.html`) — broken navigation, SEO/technical's call.
- `robots.txt` declares a sitemap at `https://example-nimbus-notes.test/sitemap.xml` that returns 404 — SEO's call.

## Coverage gaps
- `/app/login.html` — not crawled, disallowed by `robots.txt` (`/app/`); not reported per the auth-wall rule.
- `https://analytics.example-tracker.test/t.js`, `https://fonts.example-cdn.test/all.css` — off-domain, not crawled.
- `/features.html` returned 404, so no content was available to assess for extractability on that page.

## Appendices
- A. Persona debriefs — n/a, no-persona lens.
- B. Session timelines — n/a, this lens scores a static crawl, not a session.
- C. Screenshot index — n/a, no screenshots captured for this lens; evidence is crawl JSON/HTML.
