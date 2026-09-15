# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: AEO extractability — schema.org coverage, extractable answer blocks, entity clarity, llms.txt (static markup only, no live answer-engine queries)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### c1ef3cc0ef52 — No Organization schema anywhere on the site
- **Severity:** P1
- **So what:** An answer engine has no machine-readable statement of who runs Nimbus Notes, even though the fact exists in plain text on `about.html`.
- **Framework tags:** schema.org coverage — Organization
- **Flow:** crawl:site
- **Locator:** crawl/pages (site-wide: 1-index.json, 3-pricing.json, 4-about.json, 5-privacy.json)
- **Personas hit:** n/a
- **Observed:**
  - None of the 4 crawled, live pages (index, pricing, about, privacy) carry an `Organization` JSON-LD block.
  - `about.html` states the facts an Organization block would need in prose only: "Nimbus Notes is made by **Nimbus Notes Ltd**, a company of eight people founded in **2023** by **Priya Raman**... Company number 14482201."
  - No `og:site_name`, `sameAs`, or `logo` anywhere in the crawl — no cross-reference for an engine to confirm identity.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "Nimbus Notes is made by <strong>Nimbus Notes Ltd</strong>, a company of eight people founded in <strong>2023</strong> by <strong>Priya Raman</strong>, and based at 14 Harbourside Walk, <strong>Bristol</strong>, United Kingdom. Company number 14482201."
- **Repro:**
  1. Open `crawl/pages/1-index.json`, `3-pricing.json`, `4-about.json`, `5-privacy.json`.
  2. Inspect `structured_data` on each — only index (invalid) and about (FAQPage only) contain any JSON-LD.
  3. Confirm no `@type: Organization` appears in any of them.
- **Fix:** Add a single `Organization` JSON-LD block (name, url, logo, sameAs, founder) referenced from every page, sourced from the facts already on `about.html`.

### de0c02a93a07 — Homepage's only JSON-LD block is invalid and unparseable
- **Severity:** P2
- **So what:** The one schema attempt on the entry page cannot be parsed at all, so it contributes nothing to extraction — worse than having no schema, because it signals unreliability if an engine attempts to parse it.
- **Framework tags:** schema.org coverage — validity (shared with `seo`; noted here only for its extraction impact)
- **Flow:** crawl:page
- **Locator:** crawl/pages/1-index.json#structured_data
- **Personas hit:** n/a
- **Observed:**
  - The homepage's single JSON-LD block is a `SoftwareApplication` with a truncated `Offer.price` — no value token before the closing brace.
  - The crawl recorded it as invalid: `"valid": false, "error": "Expecting value: line 1 column 111"`.
  - No fallback schema exists on this page to attribute the product name or category.
- **Evidence:** `crawl/pages/1-index.json`
  > `{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Nimbus Notes", "offers": {"@type": "Offer", "price": }`
- **Repro:**
  1. Open `crawl/html/1-index.html`, locate the `<script type="application/ld+json">` block in `<head>`.
  2. Attempt to parse the raw string — `price` has no value, JSON parsing fails.
- **Fix:** Complete the `Offer.price` field (or remove the `offers` block entirely) and validate with a JSON-LD linter before deploy.

### a2d7ecf22b70 — Homepage has zero extractable answer blocks
- **Severity:** P2
- **So what:** The highest-traffic page is pure marketing prose — an answer engine has nothing question-shaped to lift and quote about what Nimbus Notes does or costs.
- **Framework tags:** extractable answer blocks
- **Flow:** crawl:page
- **Locator:** crawl/pages/1-index.json#answer_blocks
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks: []` for the homepage in the crawl record.
  - All three `h2`s are topic labels, not questions: "How it works", "Loved by teams", "Book a demo".
  - Content under each heading is feature description or a lead-gen form, not a self-contained answer.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html`
  > "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
- **Repro:**
  1. Open `crawl/pages/1-index.json`, check `h2` and `answer_blocks` fields.
  2. Confirm no heading is phrased as a question and `answer_blocks` is empty.
- **Fix:** Add a short, self-contained "What is Nimbus Notes?" / "How does sync work?" Q&A block near the top of the homepage, marked up with `FAQPage` where applicable.

### 6add0568742c — FAQPage schema covers only 2 of 3 visible Q&A pairs
- **Severity:** P2
- **So what:** An answer engine relying on structured data alone will miss the "Where is my data stored?" answer entirely, even though it is visually identical to the two that are marked up.
- **Framework tags:** schema.org coverage — FAQPage, required properties
- **Flow:** crawl:page
- **Locator:** crawl/pages/4-about.json#structured_data
- **Personas hit:** n/a
- **Observed:**
  - The page's `FAQPage` JSON-LD `mainEntity` array lists only "Does Nimbus Notes work offline?" and "Can I export my notes?".
  - The crawl's `answer_blocks` field (parsed from visible markup) records a third pair, "Where is my data stored?" / "In the EU (Frankfurt) by default. Enterprise plans can choose a region.", with no corresponding schema entry.
  - The raw HTML confirms the third `<h3>`/`<p>` pair exists outside the `<script type="application/ld+json">` block.
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html`
  > "Where is my data stored?" / "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Open `crawl/pages/4-about.json`, count `answer_blocks` entries (3) vs. `structured_data[0].raw` `mainEntity` entries (2).
  2. Confirm the third Q&A is absent from the JSON-LD.
- **Fix:** Add the third question/answer pair to the `FAQPage` `mainEntity` array so schema matches the visible content 1:1.

### e22fb5aaa12a — Pricing page states no price and has zero extractable answer blocks
- **Severity:** P2
- **So what:** An answer engine asked "how much does Nimbus Notes cost" has nothing to quote from this site — every tier routes to "Contact sales" with no figure anywhere.
- **Framework tags:** extractable answer blocks, schema/content contradiction (adjacent — no price to contradict, but none to extract either)
- **Flow:** crawl:page
- **Locator:** crawl/pages/3-pricing.json#answer_blocks
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks: []` and `structured_data: []` for the pricing page in the crawl record.
  - All three plan cards (Starter, Team, Enterprise) show only a name, a one-line description, and a "Contact sales" link — no dollar amount anywhere on the page.
  - The only pricing-adjacent line is vague: "Pricing depends on your workspace type and sync topology."
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/pages/3-pricing.json`, confirm `structured_data` and `answer_blocks` are both empty arrays.
  2. Open `crawl/html/3-pricing.html`, confirm no numeric price appears in any `.price-card`.
- **Fix:** Publish at least indicative pricing (or an explicit "custom pricing" statement) as a self-contained answer block, and add `Product`/`Offer` schema once a real price exists.

### c5513bb4e062 — llms.txt is absent
- **Severity:** P3
- **So what:** Agents that check `llms.txt` for a canonical site summary find nothing, though this is an emerging convention with uneven support.
- **Framework tags:** llms.txt
- **Flow:** crawl:site
- **Locator:** crawl/site.json#llms_txt
- **Personas hit:** n/a
- **Observed:**
  - `crawl/site.json` records `"llms_txt": {"present": false, "status": 404, "content": null}`.
- **Evidence:** `crawl/site.json`
  > `"llms_txt": {"present": false, "status": 404, "content": null}`
- **Repro:**
  1. Open `crawl/site.json`, check the `llms_txt` field.
- **Fix:** Publish a root `llms.txt` describing the product in one paragraph and linking the canonical marketing, pricing and about pages.

---

## Dropped for want of evidence
None — all observations above are supported by crawl records.

## For other lenses
- `pricing.html` carries `robots_meta: "noindex"` — indexability, belongs to `seo`.
- Duplicate `<h1>` elements on `pricing.html` ("Pricing" and "Plans for every team") and missing `<h1>` on `privacy.html` — heading structure, belongs to `seo`.
- 1 image missing `alt` text on the homepage — accessibility/SEO, belongs to `seo`.
- `features.html` returns 404 despite being linked from every page's nav — broken link, belongs to `seo` or `bugs`.
- Sitemap declared in `robots.txt` returns 404 — belongs to `seo`.

## Coverage gaps
- `/app/login.html` — excluded by `robots.txt` (`Disallow: /app/`), not crawled.
- `features.html` — returned 404, no content to assess for extractability.
- Off-domain assets (analytics script, font CDN) — out of crawl scope, off-domain.

## Appendices
- A. Persona debriefs — n/a (no-persona lens)
- B. Session timelines — n/a (crawl mode, not traversal)
- C. Screenshot index — n/a (no screenshots in a Mode-C crawl)
