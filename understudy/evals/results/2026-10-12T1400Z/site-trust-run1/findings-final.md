# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: four trust questions (real? · cost? · who? · data?) + objection ledger, scored from `trust_up` / `trust_down` and debrief Q5
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900 · sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Only what the personas could verify on the site; no outside sources. Not a compliance review.

---

## Findings

### 98dd4cbfc295 — Cookie bar says "no tracking cookies" while a third-party tracker loads and posts a user ID
- **Severity:** P0
- **So what:** The site's only explicit data promise is false on page load; any visitor who checks loses all trust at once.
- **Framework tags:** data-handling, consistency
- **Flow:** V1
- **Locator:** /
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Banner on landing reads "We use no tracking cookies on this site."
  - Same page load requests `analytics.example-tracker.test/t.js` and POSTs `/collect?uid=…` for both personas.
  - Privacy page says "We use cookies and similar technologies"; both personas flagged the contradiction.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt:4-5` · `persona-sceptic/network-full.txt:2-3` · `persona-evaluator/session.log:11` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong."
- **Repro:**
  1. Open `/` in a fresh context with network logging on.
  2. Read the bottom bar: "We use no tracking cookies on this site."
  3. Observe GET `https://analytics.example-tracker.test/t.js` and POST `…/collect?uid=…` → 204 before any interaction.
- **Fix:** Either remove the analytics tracker from every page, or rewrite the banner to name it and offer a choice before it loads.

### 96a80864fb6c — Privacy page names no partners and contradicts the cookie bar, so the sceptic left
- **Severity:** P1
- **So what:** The sceptic came to learn what happens to her notes; the privacy page answered nothing and she left at 02:40.
- **Framework tags:** data-handling, consistency
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Policy is one paragraph: "We may share information with partners and service providers to improve your experience."
  - No partner, data category, or retention period named; "We may update this policy at any time."
  - Debrief Q3: "Leave." Q5: "The privacy page took it back."
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/session.log:14` · `persona-sceptic/persona-debrief.md` (Q3, Q5) · `persona-sceptic/timeline.json` (`left_early: true`)
  > "That's not a privacy policy, that's a shrug."
- **Repro:**
  1. On mobile, tap Privacy in the footer.
  2. Search the page for any named partner or third party — there is none.
- **Fix:** Rewrite /privacy.html to list each third party by name, what it receives, and why, and state the cookie behaviour consistently with the banner.

### 8e26fcea2679 — Privacy page names no partners, leaving the evaluator unsure about their data
- **Severity:** P2
- **So what:** It undid the trust the About page had just built; a buyer taking this to a team cannot answer the data question.
- **Framework tags:** data-handling
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Evaluator read "We may share information with partners and service providers" and asked "Which partners?"
  - Listed "Who are the partners you share data with?" under questions unanswered.
  - Left over price, not data; Q5 on data: "unsure".
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/persona-debrief.md` (Q4, Q5)
  > "Data, unsure. The About page made them feel real… The privacy page and the cookie bar contradicting each other undid that."
- **Repro:**
  1. On desktop, click Privacy in the footer.
  2. Look for the names of the "partners and service providers" — none are given.
- **Fix:** Same rewrite as the sceptic variant: name every partner on /privacy.html and link it from the cookie banner.

### a24d8617401b — No price on any plan — every tier says "Contact sales", so the evaluator gave up
- **Severity:** P1
- **So what:** The evaluator's first question was cost; with no number they would "search for an alternative with a price on the page".
- **Framework tags:** pricing-transparency
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise all show only a "Contact sales" button; no figure anywhere.
  - The only explanation is "Pricing depends on your workspace type and sync topology." — terms the evaluator could not define.
  - Objective "find out what it costs without giving an email": `gave_up: true` at 02:30.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` (`price_found: false`, objective `gave_up: true`) · `persona-evaluator/persona-debrief.md` (Q3, Q5)
  > "Money, no — I don't know what they'd charge."
- **Repro:**
  1. Click Pricing in the nav.
  2. Look for any number on the three plan cards — there is none.
- **Fix:** Put a starting price (or "from £X per user per month") on Starter and Team, and replace "workspace type and sync topology" with what actually changes the price.

### 41e5b7364318 — Demo form requires a phone number before any product is shown, and the evaluator backed out
- **Severity:** P1
- **So what:** The only route to a price asks for a phone number up front; the evaluator refused and the path ended.
- **Framework tags:** data-handling, pricing-transparency
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - "Contact sales" on every plan leads to the home-page demo form.
  - Seven fields; phone number required.
  - Evaluator backed out without submitting.
- **Evidence:** `persona-evaluator/session.log:20-22` · `persona-evaluator/findings-raw.json` (02:58) · `persona-evaluator/timeline.json` (`trust_down`: "Phone number required for a demo")
  > "I haven't seen the product and they want my phone number."
- **Repro:**
  1. On /pricing.html click any "Contact sales".
  2. Note the "Book a demo" form on the home page; phone is required.
- **Fix:** Make phone optional on the "Book a demo" form, and say next to it what the number is used for.

### 9ef782cc07c7 — All three testimonials are anonymous, so the only proof on the site was disbelieved
- **Severity:** P2
- **So what:** "Is this real?" got no help from the home page; only the About page later answered it.
- **Framework tags:** proof
- **Flow:** V2
- **Locator:** /index.html
- **Personas hit:** evaluator
- **Observed:**
  - "Loved by teams" quotes are attributed to "— a happy customer", "— a user", "— anonymous".
  - No named customer, number, or case study on any visited page.
  - Evaluator kept going; logged under `trust_down`.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15`
  > "Nobody has a name. I don't believe these."
- **Repro:**
  1. Scroll the home page to "Loved by teams".
  2. Read the attributions.
- **Fix:** Replace the three quotes with one or two from named people at named teams, ideally with a specific result, or remove the section.

### 1880a3f86f82 — Nothing on the site shows the product working — "See it in action" does nothing
- **Severity:** P2
- **So what:** Both visitors arrived on "remembers everything" and saw no evidence the product exists beyond the copy.
- **Framework tags:** proof, claim-quality
- **Flow:** V3
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" did nothing on desktop (clicked twice) or mobile (tapped).
  - Hero image is an abstract graphic; no product screenshot on any visited page.
  - Sceptic logged it under `trust_down`; Q6 "nothing on the site shows it remembering anything".
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/persona-debrief.md` (Q6)
  > "It remembers everything." No — nothing on the site shows it remembering anything; the button that might have doesn't work.
- **Repro:**
  1. Open `/`.
  2. Click "See it in action" — the page does not change.
- **Fix:** Point "See it in action" at a short product video or real screenshots showing a note being recalled.

### 2becfe36dd92 — The data-location answer ("Frankfurt") sits on About, not on Privacy
- **Severity:** P3
- **So what:** The site's best data answer is on the page a privacy-minded visitor reads last, or never.
- **Framework tags:** data-handling, consistency
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Where is my data stored? In the EU (Frankfurt) by default."
  - Privacy page does not mention storage location.
  - Both personas counted this answer as `trust_up`.
- **Evidence:** `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/session.log:12` · `persona-evaluator/session.log:25`
  > "That's the answer I wanted and it's on the About page, not the Privacy page."
- **Repro:**
  1. Open /privacy.html — no storage location.
  2. Open /about.html — "In the EU (Frankfurt) by default."
- **Fix:** Copy the storage, offline and export answers onto /privacy.html and the home page.

---

## What earned trust
- About page: "Nimbus Notes Ltd", eight people, founded 2023 by Priya Raman, 14 Harbourside Walk, Bristol, company number 14482201 — both personas' strongest `trust_up`.
- FAQ answers on offline use, Markdown export "on every plan", and EU storage — evaluator: "Those are actual answers."

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Demo form field layout — `persona-evaluator/screenshots/03-demo-form.png` is blank; the form finding rests on the session log only.
- Hero claim "nothing you write is ever lost or exposed" with no stated mechanism — neither persona reacted to it as a trust issue.
- Privacy page routes questions to "Use the demo form." — no persona remarked on it.

## For other lenses
- "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology" not understood — clarity
- "Features" nav link returns 404 — technical
- Newsletter box outweighs "See it in action"; "Contact sales" is the only route to price — conversion
- 3.9 MB hero image; render-blocking third-party font CSS — technical

## Coverage gaps
- Sceptic never opened /pricing.html; price-trust flip not observable.
- No terms page, security page or customer page was visited; no consent-choice UI beyond "OK" was tested.
- Cookie storage itself was not captured — the mismatch rests on network requests plus the privacy text.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00-landing, 01-scrolled, 02-pricing, 03-demo-form (blank), 04-features-404, 05-about, 06-privacy · sceptic 00-landing, 01-privacy, 02-about
