# Nimbus Notes — aeo findings — Run 2026-09-08 (fixture01)

## Method
- Framework: AEO — schema.org coverage, extractable answer blocks, entity clarity, llms.txt (static markup only, no live answer-engine queries)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: n/a — no-persona lens
- Scoring model: sonnet
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### c51832b5a582 — No Organization schema anywhere; entity identity exists only in prose
- **Severity:** P1
- **So what:** An answer engine has no machine-readable way to confirm who Nimbus Notes is, who owns it, or where else it is defined — it would have to parse prose to attribute the site at all.
- **Framework tags:** schema.org coverage, entity clarity
- **Flow:** crawl:site
- **Locator:** crawl/pages/*.json#structured_data
- **Personas hit:** n/a
- **Observed:**
  - No page's `structured_data` array contains an `Organization` type, across index, pricing, about, or privacy.
  - The only entity facts (legal name, founding year, founder, address, company number) appear solely as unstructured prose on About.
  - No page emits `sameAs`, `logo`, or `og:site_name` (all `og` objects are empty `{}`).
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json` · `crawl/html/4-about.html`
  > "Nimbus Notes is made by <strong>Nimbus Notes Ltd</strong>, a company of eight people founded in <strong>2023</strong> by <strong>Priya Raman</strong>, and based at 14 Harbourside Walk, <strong>Bristol</strong>, United Kingdom. Company number 14482201."
- **Repro:**
  1. Open `crawl/pages/4-about.json` and inspect `structured_data` — only `FAQPage` is present, no `Organization`.
  2. Repeat for index, pricing, privacy — none carry an `Organization` block either.
- **Fix:** Add a site-wide `Organization` JSON-LD block (name, url, logo, sameAs) in the shared header/footer template so every page emits it.

---

### 0cffca802be7 — Homepage's only JSON-LD is invalid and unparsable
- **Severity:** P1
- **So what:** The one structured description of the product itself — on the page most likely to be crawled first — fails to parse, so an answer engine gets zero machine-readable product data from the homepage.
- **Framework tags:** schema.org coverage, invalid JSON-LD
- **Flow:** crawl:page
- **Locator:** crawl/pages/1-index.json#structured_data
- **Personas hit:** n/a
- **Observed:**
  - The crawl recorded `"valid": false` with `"error": "Expecting value: line 1 column 111"`.
  - The raw JSON-LD is truncated mid-object: `"offers": {"@type": "Offer", "price": }` — the `price` value is missing and the object is never closed.
  - No other structured data exists on the homepage to fall back on.
- **Evidence:** `crawl/pages/1-index.json` (structured_data[0]) · `crawl/html/1-index.html:3`
  > "{\"@context\": \"https://schema.org\", \"@type\": \"SoftwareApplication\", \"name\": \"Nimbus Notes\", \"offers\": {\"@type\": \"Offer\", \"price\": }"
- **Repro:**
  1. Open `crawl/pages/1-index.json`, read `structured_data[0].raw`.
  2. Attempt to parse it as JSON — it fails at the point the `price` value should be.
- **Fix:** Close the truncated `Offer` object with a valid price (or remove the price claim) and validate the block before publishing.

---

### 7d80038a1ce0 — Four of five crawled pages have zero extractable answer blocks
- **Severity:** P1
- **So what:** Question-shaped, quotable content exists on one page only; an engine answering "what does Nimbus Notes do" or "how much does it cost" from any other page has nothing self-contained to lift.
- **Framework tags:** extractable answer blocks
- **Flow:** crawl:site
- **Locator:** crawl/pages/*.json#answer_blocks
- **Personas hit:** n/a
- **Observed:**
  - `answer_blocks` is `[]` on index, pricing, and privacy; features.html returns 404 and has none either.
  - Pricing — the page whose entire purpose is answering "what does it cost" — states no price anywhere, only "Contact sales" buttons and one vague line.
  - Homepage content is card-shaped marketing copy ("Capture", "Sync", "Remember"), not question-and-answer.
- **Evidence:** `crawl/pages/1-index.json` (answer_blocks: []) · `crawl/pages/3-pricing.json` (answer_blocks: []) · `crawl/html/3-pricing.html:16`
  > "Pricing depends on your workspace type and sync topology."
- **Repro:**
  1. Open `crawl/pages/3-pricing.json`, note `answer_blocks: []` and no `structured_data`.
  2. Open `crawl/html/3-pricing.html` — three plan cards ("Starter", "Team", "Enterprise") carry no price, only a "Contact sales" link.
- **Fix:** Add question-shaped headings with self-contained, stated answers (e.g. actual price ranges) to the pricing and homepage content, marked up as `FAQPage` or `Product`/`Offer`.

---

### 8e6d7f7b5340 — FAQPage schema on About omits one of three visible Q&A pairs
- **Severity:** P2
- **So what:** An engine parsing the FAQPage schema would miss the "where is my data stored" answer entirely, even though it is visible and self-contained on the page.
- **Framework tags:** schema.org coverage, contradiction between schema and content
- **Flow:** crawl:page
- **Locator:** crawl/pages/4-about.json#structured_data
- **Personas hit:** n/a
- **Observed:**
  - `structured_data[0].mainEntity` contains only 2 `Question` entries (offline, export).
  - `answer_blocks` (the crawl's own extraction of visible content) contains 3 Q&A pairs — the third is not represented in the JSON-LD at all.
  - The missing pair is otherwise well-formed: a question-shaped `<h3>` followed by a direct, self-contained answer.
- **Evidence:** `crawl/pages/4-about.json` (answer_blocks[2]) · `crawl/html/4-about.html:16`
  > "Where is my data stored?" / "In the EU (Frankfurt) by default. Enterprise plans can choose a region."
- **Repro:**
  1. Open `crawl/pages/4-about.json`, count `structured_data[0].mainEntity` entries: 2.
  2. Count `answer_blocks` entries on the same page: 3.
- **Fix:** Add the third question/answer pair to the `FAQPage` `mainEntity` array so the schema matches what is visibly on the page.

---

### 013e9c56fb69 — No Open Graph metadata on any page
- **Severity:** P2
- **So what:** Engines that use `og:site_name`/`og:title` as an entity-identity signal get nothing from this site, on any page.
- **Framework tags:** entity clarity
- **Flow:** crawl:site
- **Locator:** crawl/pages/*.json#og
- **Personas hit:** n/a
- **Observed:**
  - `og` is an empty object `{}` on all 5 crawled pages (index, features-404, pricing, about, privacy).
  - `twitter` is likewise empty on every page.
  - The visible page `<title>` and header both say "Nimbus Notes" consistently, but this is never echoed into `og:site_name`.
- **Evidence:** `crawl/pages/1-index.json` · `crawl/pages/3-pricing.json` · `crawl/pages/4-about.json` · `crawl/pages/5-privacy.json` (all show `"og": {}`)
- **Repro:**
  1. Open any `crawl/pages/*.json` file and inspect the `og` field — empty on every page.
- **Fix:** Add `og:site_name`, `og:title`, and `og:description` meta tags to the shared page template.

---

### f6f770d54492 — llms.txt absent at root
- **Severity:** P3
- **So what:** Agents that check `llms.txt` for a canonical, agent-facing description of the site find nothing — a minor, emerging-convention gap, not a critical one.
- **Framework tags:** llms.txt
- **Flow:** crawl:site
- **Locator:** crawl/site.json#llms_txt
- **Personas hit:** n/a
- **Observed:**
  - `crawl/site.json` records `llms_txt.present: false` with `status: 404`.
- **Evidence:** `crawl/site.json`
  > "\"llms_txt\": {\"present\": false, \"status\": 404, \"content\": null}"
- **Repro:**
  1. Open `crawl/site.json`, read the `llms_txt` object.
- **Fix:** Publish a plain-text `llms.txt` at the root describing the product and linking to the canonical pricing, about, and product pages.

---

## Dropped for want of evidence
- Sitemap unreachable (404) may compound discovery — not scored here; sitemap validity belongs to the seo lens, and this crawl gave no evidence of AEO-specific impact beyond what is already captured.

## For other lenses
- `robots_meta: "noindex"` on the pricing page and the 404 sitemap are indexability issues — seo lens.
- `features.html` returning 404 is a broken internal link — technical/seo lens; for AEO it simply means no product-capability content exists to extract from that URL (folded into the answer-blocks finding above).
- Homepage testimonial blockquotes attributed to "a happy customer" / "a user" / "anonymous" — unattributable claims; trust lens territory, not extraction.

## Coverage gaps
- `/app/login.html` — not crawled (disallowed by robots.txt `/app/`), excluded as the auth wall.
- `features.html` — crawled but returned 404; no feature-description content available at that URL.
- Off-domain analytics and font-CDN requests — not crawled (off-domain), irrelevant to on-site extractability.

## Appendices
- A. Persona debriefs — n/a, no-persona lens.
- B. Session timelines — n/a, static crawl only.
- C. Screenshot index — n/a, this lens scores markup, not rendered screenshots.
