# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions — is this real · what does it cost · who is behind it · what happens to my data
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Only what the personas could check on the site is reported; nothing comes from outside the capture; not a compliance review

---

## Findings

### 0e7fc27dc06f — Cookie banner says "no tracking cookies" while a third-party tracker loads and posts a user ID
- **Severity:** P0
- **So what:** The first data promise both visitors saw is contradicted by the page's own traffic; both cited the mismatch as what undid their trust.
- **Framework tags:** T-DATA, T-CONSISTENCY
- **Flow:** V1
- **Locator:** /index.html#cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Banner reads "We use no tracking cookies on this site." with only an "OK" button — no choice offered
  - Both sessions load `analytics.example-tracker.test/t.js` and POST `/collect?uid=…` (204) on the landing page
  - The tracker `<script>` is in `<head>` unconditionally; "OK" only removes the banner element
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt` (`[GET] https://analytics.example-tracker.test/t.js → 200` · `[POST] https://analytics.example-tracker.test/collect?uid=8f3a… → 204`) · `persona-sceptic/network-full.txt` (`[POST] https://analytics.example-tracker.test/collect?uid=2c91… → 204`) · `crawl/html/1-index.html:3` · `crawl/html/1-index.html:37` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." — sceptic
- **Repro:**
  1. Open `/` with network logging on.
  2. Read the bottom bar: "We use no tracking cookies on this site."
  3. Observe the GET to `analytics.example-tracker.test/t.js` and POST to `/collect?uid=…` before or without any click.
- **Fix:** Remove the "no tracking cookies" banner text and either drop the analytics tag or load it only after an explicit opt-in, naming the vendor.

### 11a29d918e6c — Pricing page shows no price on any plan — every tier says "Contact sales"
- **Severity:** P1
- **So what:** The evaluator came to learn the cost, could not, and would not take it to their team — "Money, no".
- **Framework tags:** T-PRICE
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise each show only a "Contact sales" button, no currency figure
  - The only explanation is "Pricing depends on your workspace type and sync topology."
  - Evaluator gave up on the price objective at 02:30 (`gave_up: true`) and ended "would not proceed; no price"
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17` · `persona-evaluator/session.log:18` · `persona-evaluator/session.log:19` · `persona-evaluator/session.log:29` · `persona-evaluator/timeline.json` (`price_found: false`, `objectives[0].gave_up: true`)
  > "Money, no — I don't know what they'd charge." — evaluator, debrief Q5
- **Repro:**
  1. From `/`, click "Pricing" in the nav.
  2. Look for a number on any of the three plans.
- **Fix:** Put a per-seat or per-month price on Starter and Team, keep "Contact sales" for Enterprise only, and replace "sync topology" with what actually changes the price.

### 954bad349009 — Privacy page names no partners and contradicts the cookie banner — the sceptic left over it
- **Severity:** P1
- **So what:** The sceptic arrived asking what happens to her notes, read the policy at 00:45, and left the site because of it.
- **Framework tags:** T-DATA, T-CONSISTENCY
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Full policy is four sentences: "We may share information with partners and service providers to improve your experience."
  - No partner, processor, or cookie is named; "We use cookies and similar technologies." sits against the banner's "no tracking cookies"
  - "Questions? Use the demo form." — the only contact route is a sales form
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/session.log:10` · `persona-sceptic/session.log:14` · `persona-sceptic/timeline.json` (`left_early: true`, verdict "left; data handling unclear")
  > "That's not a privacy policy, that's a shrug." — sceptic
  > "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." — sceptic, debrief Q3
- **Repro:**
  1. From `/`, tap "Privacy" in the footer.
  2. Look for the names of partners, the cookies set, and a contact for data questions.
- **Fix:** Name every third party that receives data, list the cookies set, and give a privacy contact address instead of "Use the demo form".

### 704038142e10 — Privacy page left the evaluator "unsure" about data, though price drove the exit
- **Severity:** P2
- **So what:** Same page as the sceptic's exit, but the evaluator pushed through; it erased the About page's credit rather than ending the visit.
- **Framework tags:** T-DATA
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Evaluator read "We may share information with partners…" at 04:50 and asked "Which partners? It doesn't say."
  - Logged the cookie contradiction at 05:20, then returned home and kept reading
  - Stated exit reason was price, not data (`session.log:29`)
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/session.log:27` · `persona-evaluator/session.log:29`
  > "Data, unsure. The About page made them feel real … The privacy page and the cookie bar contradicting each other undid that." — evaluator, debrief Q5
- **Repro:**
  1. From `/pricing.html`, click "Privacy" in the footer.
  2. Read for named partners.
- **Fix:** Same change as the sceptic's finding: name the partners and cookies on `/privacy.html`.

### 234a61f9f612 — All three testimonials are anonymous and the evaluator disbelieved them
- **Severity:** P2
- **So what:** The site's only social proof made the evaluator less sure it was real, not more.
- **Framework tags:** T-PROOF
- **Flow:** V2
- **Locator:** /index.html#proof
- **Personas hit:** evaluator
- **Observed:**
  - "Loved by teams" quotes are attributed "— a happy customer", "— a user", "— anonymous"
  - No customer name, company, logo, or number anywhere on the pages visited
  - Evaluator marked this as the point of lost interest (01:25)
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `crawl/html/1-index.html:24-26` · `persona-evaluator/timeline.json` (`point_of_lost_interest: "01:25"`, `trust_down: "Anonymous testimonials"`)
  > "Nobody has a name. I don't believe these." — evaluator
- **Repro:**
  1. Scroll `/` to "Loved by teams".
  2. Read the attributions.
- **Fix:** Replace the three quotes with one or two named customers (person, role, company) with a specific result, or remove the section.

### 33971a240c6b — The only route to a price is a seven-field demo form with a required phone number
- **Severity:** P2
- **So what:** "Contact sales" asks for a phone number before showing anything, which read as a demand, not an answer; the evaluator backed out.
- **Framework tags:** T-PRICE, T-DATA
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Every "Contact sales" lands on "Book a demo" on the home page
  - Seven fields; first name, last name, work email, phone number and company are `required`
  - Evaluator: "Backing out. Not filling that in." (03:15); `forms_submitted: 0`
- **Evidence:** `persona-evaluator/session.log:20` · `persona-evaluator/session.log:21` · `persona-evaluator/session.log:22` · `crawl/html/1-index.html:29-35` · `persona-evaluator/timeline.json` (`trust_down: "Phone number required for a demo"`)
  > "Phone is required. I haven't seen the product and they want my phone number." — evaluator
- **Repro:**
  1. On `/pricing.html`, click any "Contact sales".
  2. Count the required fields on "Book a demo".
- **Fix:** Make phone optional, cut the form to name and work email, and show price before asking for either.

### e75cbc7c8159 — "See it in action" does nothing, so the product is never shown existing
- **Severity:** P2
- **So what:** Neither persona saw the product, so "is this real?" rested on a blob image; the sceptic logged the dead button as a trust loss.
- **Framework tags:** T-REAL
- **Flow:** V2
- **Locator:** /index.html .hero a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Button is `href="#"`; evaluator clicked twice at 00:40, sceptic tapped at 02:20 — nothing happened
  - Console: `Uncaught ReferenceError: nimbusBootstrap is not defined` in both sessions
  - No product screenshot or demo on any page visited; the hero is two circles
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/console-full.txt` · `crawl/html/1-index.html:12` · `persona-sceptic/timeline.json` (`trust_down: "'See it in action' does nothing"`)
  > "I want to see it 'remember' something. The button does nothing when I tap it." — sceptic
- **Repro:**
  1. Load `/`.
  2. Click "See it in action".
- **Fix:** Point "See it in action" at a short product video or real screenshots of a note being recalled across devices.

### 93b38f524844 — The strongest trust answers — company, Frankfurt storage, export — appear only on About
- **Severity:** P2
- **So what:** The one page that raised trust for both personas is reached only by those who go looking; the home and privacy pages carry none of it.
- **Framework tags:** T-WHO, T-DATA
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About names "Nimbus Notes Ltd", "Priya Raman", "14 Harbourside Walk, Bristol", "Company number 14482201", eight people, 2023
  - FAQ answers "In the EU (Frankfurt) by default" and Markdown export "on every plan"
  - None of this appears on `/` or `/privacy.html`
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "That's the answer I wanted and it's on the About page, not the Privacy page." — sceptic
  > "Those are actual answers. Why isn't this on the home page?" — evaluator
- **Repro:**
  1. Read `/` and `/privacy.html` for company, location, or data residency.
  2. Open `/about.html` and compare.
- **Fix:** Add the company line and the Frankfurt/export answers to the home page footer area and to `/privacy.html`.

### 6ca7dab416f1 — Hero says nothing is "ever lost or exposed" while Privacy says data is shared with partners
- **Severity:** P3
- **So what:** An absolute claim with no mechanism, contradicted on another page; no persona tied the two together this run, but a careful reader would.
- **Framework tags:** T-CLAIM, T-CONSISTENCY
- **Flow:** V1
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Privacy: "We may share information with partners and service providers"
  - Evaluator could not say what "zero-knowledge vault" means (00:18)
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:10` · `crawl/html/1-index.html:11`
- **Repro:**
  1. Read the hero sub-line on `/`.
  2. Read `/privacy.html`.
- **Fix:** State on `/privacy.html` what "zero-knowledge" covers (note content vs. usage data) so the hero claim and the sharing clause agree.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Demo form appearance — `persona-evaluator/screenshots/03-demo-form.png` is blank; form content taken from crawl HTML only.
- Whether the tracker sets a cookie (vs. only beacons) — network log shows requests, not `Set-Cookie` headers.
- Ordering of the tracker POST relative to the "OK" click — network log has no timestamps; the unconditional `<head>` script is the basis instead.

## For other lenses
- "Features" in the nav returns 404 "That page does not exist." — technical / conversion
- JSON-LD `"price": }` is malformed on `/` — seo / aeo
- Hero image 3.9 MB and render-blocking third-party font CSS — technical
- Newsletter box outweighs "See it in action" visually — conversion / clarity
- Headline does not say what the product is or who it is for — clarity

## Coverage gaps
- Sceptic never opened `/pricing.html`, so price trust could not be compared across personas.
- No persona opened the login or app; `/features.html` does not exist.
- Only `persona-evaluator` saw the demo form, and its screenshot is blank.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06 · sceptic 00–02
