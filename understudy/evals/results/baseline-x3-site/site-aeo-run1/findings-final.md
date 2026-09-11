# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: AEO extractability — schema.org coverage, extractable answer blocks, entity clarity, llms.txt
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — this lens is not persona-scored (`persona_mode: generic` for the run overall)
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope: static markup only, extractability never citation — no live answer engine was queried

---

## Findings

### 9236db0ce5f4 — Homepage JSON-LD is invalid and truncated, the only schema attempt on the site
- **Severity:** P1
- **So what:** The single structured-data block outside /about fails to parse, so an answer engine gets nothing machine-readable from the homepage at all.
- **Framework tags:** schema.org coverage — invalid JSON-LD
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json` records `structured_data[0].valid: false`, error `"Expecting value: line 1 column 111"`
  - The raw block ends mid-value: `"offers": {"@type": "Offer", "price": }` — no price value was ever written
  - This is the only JSON-LD on the homepage; there is no fallback Organization or WebSite block
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:3`
  > "{\"@context\": \"https://schema.org\", \"@type\": \"SoftwareApplication\", \"name\": \"Nimbus Notes\", \"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open `crawl/html/1-index.html`, inspect the `<script type="application/ld+json">` block in `<head>`.
  2. Parse it as JSON — it fails on the unterminated `price` value.
- **Fix:** Close out the `offers.price` value (or drop the incomplete `offers` object) and validate the block with a JSON-LD linter before shipping.

### f2c96e21dd21 — No `Organization` schema anywhere on the site
- **Severity:** P1
- **So what:** An answer engine has no machine-readable way to state who Nimbus Notes is — the company name, founder and address exist only as prose on one page.
- **Framework tags:** schema.org coverage — Organization (foundation of attribution)
- **Flow:** crawl:site
- **Locator:** crawl/pages/*.json
- **Personas hit:** n/a
- **Observed:**
  - `structured_data` across all 5 crawled pages contains no `Organization` type — only a broken `SoftwareApplication` (home) and a valid `FAQPage` (about)
  - Entity facts ("Nimbus Notes Ltd", founded 2023, founder Priya Raman, Bristol address, company number 14482201) appear only as unmarked prose on /about
  - `og.site_name` and `twitter` blocks are empty (`{}`) on every page — no fallback entity signal either
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/4-about.json` · `crawl/html/4-about.html:10`
  > "Nimbus Notes is made by <strong>Nimbus Notes Ltd</strong>, a company of eight people founded in <strong>2023</strong> by <strong>Priya Raman</strong> and based at 14 Harbourside Walk, <strong>Bristol</strong>, United Kingdom. Company number 14482201."
- **Repro:**
  1. Search every file in `crawl/pages/*.json` for `"Organization"` — no match.
  2. Compare against the prose entity facts on `crawl/html/4-about.html`.
- **Fix:** Add a site-wide `Organization` JSON-LD block (name, url, logo, `sameAs`) — the about-page prose already has the facts to populate it.

### 32dbc83cc1c8 — Homepage has zero extractable answer blocks
- **Severity:** P2
- **So what:** The highest-traffic page on the site gives an answer engine nothing it can lift and quote — every heading is a label, not a question.
- **Framework tags:** extractable answer blocks
- **Flow:** crawl:page
- **Locator:** /
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/1-index.json` records `"answer_blocks": []`
  - The page's only headings are `h1: "Your thoughts, everywhere."` and `h2: "How it works" / "Loved by teams" / "Book a demo"` — none are question-shaped
  - Body content under those headings is short marketing copy ("Write a card. It joins the graph instantly.") not self-contained answers
- **Evidence:** `crawl/pages/1-index.json` · `crawl/html/1-index.html:16-21`
  > "How it works ... Capture — Write a card. It joins the graph instantly."
- **Repro:**
  1. Open `crawl/html/1-index.html`, read the `<h2>` and following copy in the `#how` section.
  2. None of it answers a stated question.
- **Fix:** Turn at least the "How it works" section into question-shaped headings ("How does syncing work?") each followed by a self-contained one- or two-sentence answer.

### f7c75278c154 — FAQPage schema omits one of three on-page Q&A pairs
- **Severity:** P2
- **So what:** An answer engine parsing the FAQPage schema will never see the data-residency answer, even though a visitor reading the page would.
- **Framework tags:** schema.org coverage — contradiction between schema and visible content
- **Flow:** crawl:page
- **Locator:** /about.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/4-about.json` `answer_blocks` lists 3 Q&A pairs, including "Where is my data stored?"
  - The page's `structured_data[0]` (`FAQPage`) `mainEntity` array contains only 2 `Question` entries — "Does Nimbus Notes work offline?" and "Can I export my notes?"
  - The visible `<h3>Where is my data stored?</h3>` / answer pair on the page has no matching JSON-LD entry
- **Evidence:** `crawl/pages/4-about.json` · `crawl/html/4-about.html:16-17`
  > "Where is my data stored? — In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Compare `crawl/pages/4-about.json` `answer_blocks` (3 items) against `structured_data[0].raw` `mainEntity` (2 items).
  2. The third question/answer pair is missing from the JSON-LD.
- **Fix:** Add the "Where is my data stored?" Q&A pair as a third `Question`/`acceptedAnswer` entry in the FAQPage JSON-LD.

### 72e1f1cbb6db — Pricing page has no extractable price for any plan
- **Severity:** P2
- **So what:** An answer engine asked "how much does Nimbus Notes cost" has nothing to quote — every tier routes to sales instead of stating a number.
- **Framework tags:** extractable answer blocks · schema.org coverage (no Product/Offer schema)
- **Flow:** crawl:page
- **Locator:** /pricing.html
- **Personas hit:** n/a
- **Observed:**
  - `crawl/pages/3-pricing.json` records `"structured_data": []` and `"answer_blocks": []`
  - All three tiers (Starter, Team, Enterprise) show only a description and a "Contact sales" CTA — no `<price>` value on the page
  - The only price-adjacent text is a disclaimer: "Pricing depends on your workspace type and sync topology."
- **Evidence:** `crawl/pages/3-pricing.json` · `crawl/html/3-pricing.html:12-16`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/html/3-pricing.html`, read the three `.price-card` blocks.
  2. None contains a number; all three CTAs are "Contact sales."
- **Fix:** Publish at least indicative prices per tier, marked up with `Product`/`Offer` schema, even if final pricing is negotiated for Enterprise.

### d710ce31aa38 — `llms.txt` is absent
- **Severity:** P3
- **So what:** Agents that check for the emerging `llms.txt` convention get nothing pointing them at canonical pages — low cost today, but free to fix.
- **Framework tags:** llms.txt
- **Flow:** crawl:site
- **Locator:** llms.txt
- **Personas hit:** n/a
- **Observed:**
  - `crawl/site.json` records `"llms_txt": {"present": false, "status": 404, "content": null}`
- **Evidence:** `crawl/site.json`
  > "llms_txt": {"present": false, "status": 404, "content": null}
- **Repro:**
  1. Request `/llms.txt` on the crawled host — 404.
- **Fix:** Publish an `llms.txt` at the root describing the product and pointing at /about, /pricing and the canonical marketing page.

---

## Dropped for want of evidence
None — all observations below the evidence bar were excluded before this section.

## For other lenses
- Homepage `robots.txt` disallows `/app/`, and the declared sitemap 404s with zero URLs (`crawl/site.json`) — sitemap/crawlability is `seo`'s territory.
- `/features.html` returns 404 and is still linked from the header nav on every page — broken internal link, `seo`'s territory.
- `/pricing.html` and generic-titled pages (`/about.html`, `/privacy.html` both titled just "Nimbus Notes") — title/meta duplication is `seo`'s territory.
- Pricing page's "Contact sales"-only tiers with no visible number — pricing-transparency angle belongs to `trust`/`conversion`; this report covers only the extractability consequence.

## Coverage gaps
- `/app/login.html` — never crawled (robots-disallowed); no content to assess.
- Off-domain analytics/font assets — never crawled (off-domain); irrelevant to page content.
- `/features.html` — crawled but returns 404; no page content exists to extract.

## Appendices
- A. Persona debriefs — n/a, no persona traversal in this lens
- B. Session timelines — n/a, crawl-based lens; see `crawl/index.json` for crawl order
- C. Screenshot index — n/a, this lens reads crawl records, not screenshots
