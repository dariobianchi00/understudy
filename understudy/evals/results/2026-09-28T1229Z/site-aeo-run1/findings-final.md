# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: schema.org coverage · extractable answer blocks · entity clarity · llms.txt
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens (manifest `persona_mode` is `generic`, not used here)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope: static markup only — extractability, never citation. See exec-summary for the full scope note.

---

## Findings

### 080ca69bf223 — No Organization schema anywhere on the site
- **Severity:** P1
- **So what:** An answer engine has no machine-readable source for who Nimbus Notes is — no schema `name`, `url`, `logo`, or `sameAs`.
- **Framework tags:** schema.org coverage, entity clarity
- **Flow:** crawl:site
- **Locator:** site-wide
- **Personas hit:** n/a
- **Observed:**
  - Zero `Organization` schema across all 5 crawled pages (index, pricing, about, privacy, features-404).
  - `og.site_name` is empty on every page (`"og": {}` recorded in each page JSON).
  - Entity facts (legal name, founding year, founder, address, company number) exist only as unmarked prose on `/about.html`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "Nimbus Notes is made by <strong>Nimbus Notes Ltd</strong>, a company of eight people founded in <strong>2023</strong> by <strong>Priya Raman</strong>, and based at 14 Harbourside Walk, <strong>Bristol</strong>, United Kingdom. Company number 14482201."
- **Repro:**
  1. Open each `crawl/pages/*.json` and inspect `structured_data` — only index (invalid) and about (FAQPage) carry any JSON-LD.
  2. Search all 5 pages for `"@type": "Organization"` — zero matches.
- **Fix:** Add a site-wide `Organization` schema block (name, url, logo, sameAs) sourced from the About page facts, e.g. via a shared head/footer partial.

### 62d086e12aee — Homepage JSON-LD is malformed and fails to parse
- **Severity:** P1
- **So what:** The homepage's only structured-data attempt is unparsable, so an answer engine extracts nothing from it.
- **Framework tags:** schema.org coverage — validity (overlaps `seo`'s structured-data checks; noted once here, scored on extraction impact)
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - Homepage's single JSON-LD block declares `SoftwareApplication` with a truncated `Offer`: `"price": }`.
  - Crawl recorded it as invalid, error "Expecting value: line 1 column 111".
  - No fallback `Organization` or `Product` schema exists on the page to compensate.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "{\"@context\": \"https://schema.org\", \"@type\": \"SoftwareApplication\", \"name\": \"Nimbus Notes\", \"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open `crawl/pages/1-index.json` → `structured_data[0].valid` is `false`, with the parse error given.
  2. View `crawl/html/1-index.html` → the `<script type="application/ld+json">` tag has a truncated `price` value.
- **Fix:** Complete the `Offer.price` with a real value (or drop `offers` if no public price exists), and validate JSON-LD before publishing.

### 0d6526079e41 — Pricing page states no prices, structured or visual
- **Severity:** P2
- **So what:** An answer engine cannot extract a price for any plan; every tier's content ends at "Contact sales."
- **Framework tags:** extractable answer blocks, schema.org coverage (no Product/Offer)
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - Three plan cards (Starter, Team, Enterprise) each carry a one-line description and a "Contact sales" CTA — no digit or currency symbol anywhere in the page's 60 words.
  - Page carries zero `structured_data` entries — no Product/Offer schema either.
  - Only price-adjacent text on the page: "Pricing depends on your workspace type and sync topology."
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/html/3-pricing.html` — search plan cards for a price: none present.
  2. `crawl/pages/3-pricing.json` → `structured_data: []`.
- **Fix:** Publish at least indicative pricing, or a stated "custom pricing, contact sales" answer, marked up as `Product`/`Offer` or `FAQPage`.

### 32dbc83cc1c8 — Homepage has zero extractable answer blocks
- **Severity:** P2
- **So what:** An answer engine has no question-shaped content to quote from the page most likely to be crawled first.
- **Framework tags:** extractable answer blocks
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - Homepage headings are "How it works", "Loved by teams", "Book a demo" — none question-shaped.
  - Crawl records `"answer_blocks": []` for the homepage.
  - The only product-description content is three three-word taglines (Capture / Sync / Remember) with one-sentence captions; `/features.html`, the page that might otherwise describe capabilities, returns 404.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html` · `crawl/pages/2-features.json`
  > "Write a card. It joins the graph instantly."
- **Repro:**
  1. `crawl/pages/1-index.json` → `answer_blocks: []`.
  2. `crawl/pages/2-features.json` → `status: 404`.
- **Fix:** Add a question-shaped section (e.g. "What is Nimbus Notes?", "How does sync work?") with self-contained answers, marked up as `FAQPage`.

### 7fb7572d5943 — About page FAQPage schema omits a third visible Q&A
- **Severity:** P2
- **So what:** An answer engine reading only the schema misses the "Where is my data stored?" answer a person reading the page would see.
- **Framework tags:** schema.org coverage — contradiction between schema and visible content
- **Flow:** crawl:page
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - Page visually lists 3 Q&As under "Frequently asked questions": offline support, export, data location.
  - `FAQPage` JSON-LD `mainEntity` contains only 2 `Question` entries — offline support and export. "Where is my data stored?" is absent from the schema.
  - Crawl's own `answer_blocks` extraction found all 3, confirming the third is visually well-formed (`<h3>`+`<p>`) but unmarked in schema.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "Where is my data stored?" / "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. `crawl/pages/4-about.json` → `structured_data[0].raw` `mainEntity` array has 2 entries.
  2. `crawl/pages/4-about.json` → `answer_blocks` array has 3 entries.
- **Fix:** Add the third Q&A ("Where is my data stored?") to the `FAQPage` `mainEntity` array.

### f03b16e45ade — llms.txt is absent
- **Severity:** P3
- **So what:** Agents that check `llms.txt` for a canonical, agent-facing summary find nothing.
- **Framework tags:** llms.txt
- **Flow:** crawl:site
- **Locator:** site-wide
- **Personas hit:** n/a
- **Observed:**
  - `crawl/site.json` records `llms_txt.present: false`, `status: 404`.
- **Evidence:** `crawl/site.json`
  > "llms_txt": {"present": false, "status": 404, "content": null}
- **Repro:**
  1. Open `crawl/site.json` → `llms_txt.present` is `false`.
- **Fix:** Publish a root `/llms.txt` describing the product and pointing to `/about.html` and `/pricing.html`.

---

## Dropped for want of evidence
None — every observation chased to a citable artifact.

## For other lenses
- Declared sitemap (`https://example-nimbus-notes.test/sitemap.xml`) returns 404, unreachable — `seo`.
- `/features.html` returns 404, breaking a primary nav link — `seo`/`technical`.
- `/pricing.html` carries `<meta name="robots" content="noindex">` — `seo`.
- `/pricing.html` has two `<h1>` tags ("Pricing", "Plans for every team") — `seo`.

## Coverage gaps
- `/app/login.html` — not crawled, disallowed by `robots.txt` (`/app/`). Not reported (infrastructure/auth wall).
- `https://analytics.example-tracker.test/t.js`, `https://fonts.example-cdn.test/all.css` — not crawled, off-domain.
- `/features.html` — crawled but returns 404; no content to assess beyond the error page.

## Appendices
- A. Persona debriefs — n/a, no-persona lens.
- B. Session timelines — n/a, no-persona lens.
- C. Screenshot index — n/a, this lens scores static markup only; no screenshots captured.
