# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: schema.org coverage · extractable answer blocks · entity clarity · llms.txt (static markup only — no live answer-engine queries)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — this lens scores extractability, not persona experience
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 5b225ea181c5 — Homepage SoftwareApplication schema is invalid JSON-LD
- **Severity:** P1
- **So what:** The only structured data on the homepage fails to parse, so an answer engine gets nothing machine-readable from the entry page — no name, no price, no offer.
- **Framework tags:** schema.org coverage — invalid JSON-LD, Product/Offer contradiction risk
- **Flow:** crawl:page
- **Locator:** crawl/pages/1-index.json
- **Personas hit:** n/a
- **Observed:**
  - `structured_data[0].valid` is `false` with error `"Expecting value: line 1 column 111"`
  - Raw block ends mid-object: `"offers": {"@type": "Offer", "price": }` — the price value was never written
  - No other JSON-LD block exists on the homepage
- **Evidence:** `crawl/pages/1-index.json:27-33` · `crawl/html/1-index.html`
  > "{\"@context\": \"https://schema.org\", \"@type\": \"SoftwareApplication\", \"name\": \"Nimbus Notes\", \"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Fetch `http://localhost:8765/`
  2. Parse the single `<script type="application/ld+json">` block
  3. JSON parsing fails at the truncated `price` key
- **Fix:** Complete the `Offer.price` value (or remove the incomplete `offers` block) and validate the JSON-LD before deploy.

### 56397350575f — No Organization schema anywhere on the site
- **Severity:** P1
- **So what:** Nothing on any of the 5 crawled pages tells a machine, unambiguously, who this company is — its legal name, URL, logo or where else it is defined (`sameAs`).
- **Framework tags:** schema.org coverage — Organization (foundation of attribution)
- **Flow:** crawl:site
- **Locator:** crawl/pages/1-index.json
- **Personas hit:** n/a
- **Observed:**
  - `structured_data` across index, pricing, about and privacy contains only one `SoftwareApplication` (invalid) and one `FAQPage` block — no `Organization` or `WebSite` type anywhere
  - `og` and `twitter` objects are empty (`{}`) on every crawled page — no `og:site_name` fallback either
  - The legal entity ("Nimbus Notes Ltd", founded 2023, Bristol UK, company number 14482201) exists only as prose on `about.html`, not as schema
- **Evidence:** `crawl/pages/1-index.json:27,25` · `crawl/pages/3-pricing.json:24,22` · `crawl/pages/4-about.json:25,23` · `crawl/pages/5-privacy.json:23,21`
  > "Nimbus Notes is made by <strong>Nimbus Notes Ltd</strong>, a company of eight people founded in <strong>2023</strong> by <strong>Priya Raman</strong>..."
- **Repro:**
  1. Fetch each crawled page
  2. Search `structured_data` for `@type: "Organization"` or `og:site_name`
  3. Neither appears on any page
- **Fix:** Add a single `Organization` JSON-LD block (name, url, logo, sameAs) site-wide, e.g. via a shared header partial, sourced from the facts already on `about.html`.

### bb4355206428 — FAQPage schema omits one of three displayed Q&A pairs
- **Severity:** P2
- **So what:** An answer engine parsing the About page's schema can attribute two answers but not the third, which is only visible in HTML prose.
- **Framework tags:** schema.org coverage — FAQPage completeness; extractable answer blocks
- **Flow:** crawl:page
- **Locator:** crawl/pages/4-about.json
- **Personas hit:** n/a
- **Observed:**
  - The page's `answer_blocks` array lists 3 Q&A pairs, but `structured_data[0].raw` (`FAQPage.mainEntity`) contains only 2 `Question` entries
  - The missing pair — "Where is my data stored?" / "In the EU (Frankfurt) by default. Enterprise plans can choose a region." — appears as an `<h3>`/`<p>` in the HTML but has no matching JSON-LD entity
  - The two markup-backed answers ("Does Nimbus Notes work offline?", "Can I export my notes?") are self-contained and lead with the answer
- **Evidence:** `crawl/pages/4-about.json:47-60` (answer_blocks) vs. `crawl/pages/4-about.json:27` (structured_data)
  > "Where is my data stored?" / "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Fetch `about.html`
  2. Compare the three `<h3>` questions in the FAQ section against `FAQPage.mainEntity` in the JSON-LD
  3. The third question has no corresponding entity
- **Fix:** Add the data-residency Q&A as a third `Question`/`acceptedAnswer` pair in the existing `FAQPage` block.

### ab39f5e7c385 — 3 of 5 crawled pages have zero extractable answer blocks
- **Severity:** P2
- **So what:** An answer engine has nothing question-shaped to lift from the homepage, pricing page or privacy page — only marketing/legal prose.
- **Framework tags:** extractable answer blocks
- **Flow:** crawl:site
- **Locator:** crawl/pages/1-index.json
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks: []` on `1-index.json`, `3-pricing.json` and `5-privacy.json`
  - Homepage's "How it works" section uses non-question card headings ("Capture", "Sync", "Remember") — descriptive, not answer-shaped
  - Pricing page states no actual number anywhere in the markup: three plan cards read "For individuals.", "For growing teams.", "SSO, audit log, vault residency." with only "Contact sales" CTAs and "Pricing depends on your workspace type and sync topology."
- **Evidence:** `crawl/pages/1-index.json:50` · `crawl/pages/3-pricing.json:39` · `crawl/pages/5-privacy.json:37` · `crawl/html/3-pricing.html`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Fetch `index.html`, `pricing.html`, `privacy.html`
  2. Inspect each for question-shaped `<h2>`/`<h3>` followed by a self-contained answer
  3. None found; only marketing copy, testimonial quotes, and a legal paragraph
- **Fix:** Add a short FAQ block to the homepage and pricing page (e.g. "What does Nimbus Notes cost?", "Does it work offline?") marked up with `FAQPage`, leading with the answer.

### c5513bb4e062 — llms.txt is absent
- **Severity:** P3
- **So what:** Agents that check for the emerging `llms.txt` convention get no site-level description or pointer to canonical pages.
- **Framework tags:** llms.txt
- **Flow:** crawl:site
- **Locator:** crawl/site.json
- **Personas hit:** n/a
- **Observed:**
  - `llms_txt.present` is `false`, `status` is `404`, `content` is `null`
- **Evidence:** `crawl/site.json` (llms_txt object)
  > "\"llms_txt\": {\"present\": false, \"status\": 404, \"content\": null}"
- **Repro:**
  1. Fetch `http://localhost:8765/llms.txt`
  2. Returns 404
- **Fix:** Add an `llms.txt` at the root describing the product and linking to about/pricing/FAQ pages.

---

## Dropped for want of evidence
- Pricing page `robots_meta: "noindex"` possibly suppressing answer-engine crawlers that honor robots meta — no evidence this crawl's `not_crawled` list attributes any skip to that tag; overlaps SEO's territory more directly.

## For other lenses
- `pricing.html` carries `robots_meta: "noindex"` and no canonical — seo.
- Homepage has 1 image missing `alt` text — seo/ux, not an extraction blocker on its own.
- Heading order invalid on `pricing.html` (two `<h1>`s) and `privacy.html` (no `<h1>`, only `<h2>`) — seo.

## Coverage gaps
- `features.html` returned 404 — could not assess its schema or answer blocks.
- `/app/login.html` not crawled (disallowed by robots.txt `/app/`) — auth wall, excluded per contract.
- Off-domain assets (analytics script, font CSS) not crawled — out of scope, off-domain.

## Appendices
- A. Persona debriefs — n/a, no-persona lens.
- B. Session timelines — n/a, Mode-C crawl has no session timeline.
- C. Screenshot index — n/a, this run captured `crawl/html/*.html`, not screenshots.
