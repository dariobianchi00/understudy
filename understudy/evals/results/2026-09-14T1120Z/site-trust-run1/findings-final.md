# Nimbus Notes — trust findings — Run 2026-09-14 (fixture01)

## Method
- Framework: the four questions a visitor asks — is this real · what does it cost · who is behind this · what happens to my data
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED, not researched
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope: only what the personas could see or the capture recorded on this site; no company register, news or outside knowledge was used, and no compliance judgement is offered

---

## Findings

### 3b1b53d69a2c — Cookie bar says "no tracking cookies" while the page loads a third-party analytics tracker
- **Severity:** P0
- **So what:** The only statement the site volunteers about data is contradicted by its own page load, which puts every other claim in doubt.
- **Framework tags:** Data handling · Consistency · Q4
- **Flow:** V1
- **Locator:** /index.html cookie bar
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The bar on the fold reads "We use no tracking cookies on this site." with a single OK button; both personas dismissed it without a choice offered.
  - On the same page load the capture recorded `GET https://analytics.example-tracker.test/t.js → 200` and `POST https://analytics.example-tracker.test/collect?uid=8f3a… → 204`, a per-visitor id, for both personas.
  - Neither persona could see the network log; from the site alone the bar simply reads as a promise.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt:4` · `persona-sceptic/network-full.txt:3` · DOM `crawl/html/1-index.html` line 3 `<script src="https://analytics.example-tracker.test/t.js" async>`
  > "The bar said no tracking cookies. This page says they use cookies."
- **Repro:**
  1. Open `http://localhost:8765/` with the network panel recording.
  2. Read the black bar at the bottom of the fold.
  3. Compare it with the requests to `analytics.example-tracker.test` fired on the same load.
- **Fix:** Either remove the `analytics.example-tracker.test` script from `index.html`, or replace the bar's text with what actually runs and give a real reject option.

### e8d9bb44c604 — No price on any of three plans, and the only route to a number is a seven-field form
- **Severity:** P0
- **So what:** The evaluator arrived to find out what it costs, could not, and left to look for a competitor that shows a number.
- **Framework tags:** Pricing transparency · Q2
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise each carry one button, "Contact sales"; no currency appears anywhere on the page.
  - The stated reason — "Pricing depends on your workspace type and sync topology" — used a term the persona did not have: "I don't know what my workspace type is. I haven't got one."
  - "Contact sales" returns to `index.html#demo`, a seven-field form; `price_found: false`, `price_understood: false`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17` · `persona-evaluator/session.log:19` · `persona-evaluator/timeline.json`
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. Land on `/index.html`, click "Pricing" in the nav.
  2. Read all three cards and the grey line below them.
  3. Click any "Contact sales".
- **Fix:** Put a starting price in currency on each of the three cards on `/pricing.html`, with a one-line note on what pushes it up.
- **Note:** Severity is borderline P0/P1 — the site is not broken, but this was the run's objective under test and the persona abandoned the site over it; scored high per the rubric's tie-break.

### c0b68f91bef8 — Cookie bar and privacy page give opposite answers on whether cookies are used
- **Severity:** P1
- **So what:** The sceptic ended the visit here, and the evaluator's "would you trust them with your data" answer dropped from yes to unsure.
- **Framework tags:** Consistency · Data handling · Q4
- **Flow:** V3
- **Locator:** /privacy.html cookie statement
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The bar says "We use no tracking cookies on this site."; `/privacy.html` says "We use cookies and similar technologies."
  - Both personas spotted it unprompted — the sceptic at 01:05 on mobile, the evaluator at 05:20 on desktop.
  - Neither page acknowledges the other or explains which kind of cookie is meant.
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:10` · `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:27`
  > "The privacy page and the cookie bar contradicting each other undid that."
- **Repro:**
  1. Land on `/index.html` and read the bar at the bottom.
  2. Open Privacy from the footer and read sentence three.
- **Fix:** Write one sentence on `/privacy.html` naming the cookie categories actually set, and make the bar's wording repeat it verbatim.

### 97c8ad7c6a85 — Privacy page names none of the partners it says it shares data with
- **Severity:** P1
- **So what:** The sceptic's single reason for visiting went unanswered, and she left rather than ask.
- **Framework tags:** Data handling · Claim quality · Q4
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The whole policy is four sentences, including "We may share information with partners and service providers to improve your experience."
  - No partner, category or purpose is named, and "We may update this policy at any time." closes it.
  - The only contact route offered is "Questions? Use the demo form." — the seven-field sales form.
  - Both personas listed the partners question in `questions_unanswered`.
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-evaluator/session.log:26` · `persona-sceptic/timeline.json`
  > "That's not a privacy policy, that's a shrug."
- **Repro:**
  1. Open `/privacy.html` from the footer on any page.
  2. Look for the name of any third party.
- **Fix:** List the third parties by name on `/privacy.html` with what each receives, and give a plain email address instead of the demo form.

### 434bbd328593 — Nothing on the site shows the product working and "See it in action" does nothing
- **Severity:** P1
- **So what:** Both personas finished the visit with no evidence the product exists, so "is this real" stayed half-answered.
- **Framework tags:** Proof · Q1
- **Flow:** V1
- **Locator:** /index.html hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The hero image is two abstract circles; no screen, screenshot or recording of the product appears on any page the personas opened.
  - "See it in action" is `href="#"`; the evaluator clicked twice and the sceptic tapped once, with no response.
  - The console throws `Uncaught ReferenceError: nimbusBootstrap is not defined` on every landing for both personas.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · console `persona-evaluator/console-full.txt:1`
  > "No — nothing on the site shows it remembering anything; the button that might have doesn't work."
- **Repro:**
  1. Land on `/index.html`.
  2. Click "See it in action" and watch the page and the console.
- **Fix:** Point "See it in action" at a short product recording, and put one real screenshot of the app in the hero in place of the abstract graphic.

### db9cef058ef0 — Only proof on the site is three quotes signed "a happy customer", "a user" and "anonymous"
- **Severity:** P1
- **So what:** The one section meant to build confidence is the moment the evaluator stopped reading.
- **Framework tags:** Proof · Claim quality · Q1
- **Flow:** V2
- **Locator:** /index.html proof section
- **Personas hit:** evaluator
- **Observed:**
  - Under the heading "Loved by teams", three quotes carry no name, role, company or number.
  - `point_of_lost_interest` is 01:25 — the same second the evaluator read them.
  - No customer, logo, case study or usage figure appears anywhere else the personas went.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `persona-evaluator/timeline.json` · `persona-evaluator/findings-raw.json`
  > "Three quotes, nobody has a name. I don't believe these."
- **Repro:**
  1. Land on `/index.html` and scroll to "Loved by teams".
  2. Read the attribution on each of the three quotes.
- **Fix:** Replace the three quotes with one testimonial carrying a real name, role and company, or delete the section until you have one.

### 134ce6cde568 — Demo form requires a phone number before the visitor has seen the product
- **Severity:** P2
- **So what:** The only path to a price asks for a phone call from someone who has not yet seen a screenshot, and the evaluator backed out.
- **Framework tags:** Pricing transparency · Data handling · Q2
- **Flow:** V3
- **Locator:** /index.html demo form
- **Personas hit:** evaluator
- **Observed:**
  - Seven fields: first name, last name, work email, phone number, company, company size, what do you want to see; phone is `required`.
  - The evaluator counted the fields at 02:58 and abandoned at 03:15 without submitting (`forms_submitted: 0`).
  - No explanation appears on the form for why a phone number is needed.
- **Evidence:** `persona-evaluator/session.log:21` · `persona-evaluator/session.log:22` · DOM `crawl/html/1-index.html` line 31 `<label>Phone number</label><input type="tel" required>`
  > "Seven fields. Phone required. I haven't seen the product."
- **Repro:**
  1. Click any "Contact sales" on `/pricing.html`.
  2. Count the fields on the demo form and note which are required.
- **Fix:** Make phone number optional on the `#demo` form and cut it to name, work email and company.

### 0afaf944197d — Every substantive answer about the company and the data sits on the About page
- **Severity:** P2
- **So what:** The material that raised trust for both personas is a page most visitors never open, while the pages that raise the questions carry none of it.
- **Framework tags:** Provenance · Data handling · Q3
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` carries the founder's name, a Bristol address, the year, headcount and a company number, plus three FAQ answers.
  - "Where is my data stored? In the EU (Frankfurt) by default." is the answer the sceptic came for — and it is not on `/privacy.html`.
  - Both personas logged it as the only thing that raised trust; both remarked it was in the wrong place.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "Why isn't this on the home page?"
- **Repro:**
  1. Open `/privacy.html` and look for where data is stored — absent.
  2. Open `/about.html` and read the third FAQ answer.
- **Fix:** Move the data-location, offline and export answers onto `/privacy.html` and the home page, keeping the About copy as well.

### 3810277c1371 — Fold has one data-safety claim, an unexplained "zero-knowledge vault"
- **Severity:** P3
- **So what:** The site's strongest security claim did no trust work, because neither persona could tell what it meant.
- **Framework tags:** Claim quality · Q4
- **Flow:** V1
- **Locator:** /index.html hero copy
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - No page the personas opened explains the mechanism or repeats the claim.
  - The sceptic, whose question was what happens to her notes, read the fold and went straight to the footer at 00:30 instead.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-sceptic/session.log:8` · `persona-evaluator/timeline.json`
  > "'bi-directional sync graph', 'zero-knowledge vault' — I don't know what either of those means."
- **Repro:**
  1. Read the hero subhead on `/index.html`.
  2. Look for any page that explains what the vault does.
- **Fix:** Replace "zero-knowledge vault" in the hero with one plain sentence on who can read the notes, and link it to a page that explains how.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether the analytics script sets a cookie before consent — the capture records the request and a `uid` parameter, not the cookie jar.
- Whether the testimonials would have hurt the sceptic too — she left at 00:30 without scrolling to the proof section.
- Whether the "(fictional)" in the footer copyright was noticed — neither persona mentioned it in any log line or debrief.
- Whether any renewal, contract term or what-is-not-included exists — no plan detail was reachable without submitting the form.

## For other lenses
- "Features" in the nav returns a 404 — technical.
- `/pricing.html` carries `<meta name="robots" content="noindex">` and no meta description — seo.
- "See it in action" being a dead `href="#"` as a next-step failure — conversion.
- "workspace type", "sync topology", "sync graph", "cards" versus "blocks" as comprehension failures — clarity.
- Hero image served at 3.9 MB — technical.

## Coverage gaps
- `persona-evaluator/screenshots/03-demo-form.png` is blank white; the form finding rests on the session log and the DOM instead.
- `/features.html` was never seen (404), so any trust material on it is unassessed.
- Neither persona scrolled the home page on mobile past the fold, so the proof section was tested on desktop only.
- No persona reached the logged-in app, so nothing about in-product data handling was observed.
- One device per persona; a trust severity flip between a sceptic and an eager buyer could not be observed on pricing, because the sceptic never looked for it.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/` (00-landing, 01-scrolled, 02-pricing, 03-demo-form, 04-features-404, 05-about, 06-privacy) · `persona-sceptic/screenshots/` (00-landing, 01-privacy, 02-about)
