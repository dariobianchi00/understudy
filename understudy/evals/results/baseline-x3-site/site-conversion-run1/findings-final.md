# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion — hierarchy, availability, burden, match, dead ends, wrong-kind friction, competing asks; scored against the goal "Start a free trial without talking to sales"
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Forms were opened and backed out of, never submitted; nothing here speculates about post-submission behaviour
- `03-demo-form.png` captured blank; form fields counted from `crawl/html/1-index.html:29-34`

---

## Findings

### ed10f8056661 — No self-serve trial path exists: every call to action routes to sales or log-in
- **Severity:** P0
- **So what:** The goal the business set — a trial without talking to sales — has no route on the site, so no visitor can reach it however convinced they are.
- **Framework tags:** availability, dead-end, match
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - All three pricing cards carry only "Contact sales", each linking to `index.html#demo` — the demo-request form
  - Home page offers "See it in action" (inert), a newsletter box, and "Book a demo"; no trial, signup or "get started" anywhere on 5 pages
  - Nav's only filled button is "Log in" — for existing users
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `crawl/html/3-pricing.html:12-14` · `persona-evaluator/session.log:17` · `persona-evaluator/session.log:20`
  > "Three cards: Starter, Team, Enterprise. Every one says "Contact sales". No numbers anywhere."
- **Repro:**
  1. Open `/index.html`; scan header, hero, and every section to the footer for a trial or signup action
  2. Open `/pricing.html`; note every card's button reads "Contact sales" and links to `index.html#demo`
- **Fix:** Add a "Start free trial" button to the Starter and Team cards on `/pricing.html` and to the hero on `/index.html`, linking to a signup page that asks for an email only.

### 6745582f5edf — Pricing page shows no price on any of its three plans
- **Severity:** P0
- **So what:** The evaluator came to find the cost, could not, and left to search for an alternative — a visitor who cannot work out what they would pay cannot take a next step.
- **Framework tags:** wrong-kind friction, match, dead-end
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter "For individuals.", Team "For growing teams.", Enterprise "SSO, audit log, vault residency." — no number, no currency, no "free" on any card
  - Footnote "Pricing depends on your workspace type and sync topology." — the evaluator did not know what a workspace type is
  - `timeline.json` shape_v3: `price_found: false`, `price_understood: false`; objective attempt 01:48–02:30, `gave_up: true`
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/session.log:29` · `persona-evaluator/timeline.json` shape_v3 · `persona-evaluator/persona-debrief.md` Q3
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."
- **Repro:**
  1. Open `/pricing.html` on desktop
  2. Search the page for a currency symbol or a number — none present
- **Fix:** Print a monthly price (or "Free") on the Starter and Team cards, and replace the "workspace type and sync topology" footnote with a plain sentence on what changes the price.

### 0e0827610a78 — Hero call to action See it in action does nothing when clicked
- **Severity:** P1
- **So what:** The only action above the fold on both devices is inert, so a visitor convinced at the fold has nowhere to go and both personas registered it as the site not working.
- **Framework tags:** availability, hierarchy
- **Flow:** shape_v1
- **Locator:** /index.html a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Markup: `<a class="cta" href="#">See it in action</a>` — anchor to nothing
  - Evaluator clicked twice at 00:40, "Nothing happened. The page didn't move."
  - Sceptic tapped at 02:20 on iPhone 13, "The button does nothing when I tap it." — cited in debrief Q6 as why the promise was not met
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `crawl/html/1-index.html:12` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/persona-debrief.md` Q6
  > "No — nothing on the site shows it remembering anything; the button that might have doesn't work."
- **Repro:**
  1. Open `/index.html` at 1440×900 or 390×844
  2. Click "See it in action" — URL gains `#`, no scroll, no modal, no navigation
- **Fix:** Point "See it in action" at a real destination — a product video or the trial signup — and restyle it as the filled primary button.

### f78cef47eb65 — Demo form demands 7 fields, 5 required including phone, before any product is shown
- **Severity:** P1
- **So what:** This form is the only way off the Pricing page, and the ask — phone and company before a price or a screenshot — made the evaluator back out at 03:15.
- **Framework tags:** burden, match, wrong-kind friction
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Fields from markup: First name*, Last name*, Work email*, Phone number*, Company*, Company size (select), What do you want to see? — 7 fields, 5 `required`
  - No required markers rendered in the labels; the visitor learns which are mandatory only on submit
  - Reached from "Contact sales" on Pricing — the visitor asked for a price and was handed a demo request instead
- **Evidence:** `crawl/html/1-index.html:29-34` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:20-22` · `persona-evaluator/timeline.json` shape_v3 `forms_opened: 1, forms_submitted: 0`
  > "Counting fields: first name, last name, work email, phone number, company, company size, what do you want to see. Seven. Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html`, click "Contact sales" on any card → lands at `index.html#demo`
  2. Inspect the "Book a demo" form: 7 controls, `required` on 5 inputs, phone `type="tel" required`
- **Fix:** Cut the demo form to work email plus an optional "what do you want to see", make phone optional, and mark required fields in the labels.

### 1116bc75d983 — Newsletter box outweighs the only product call to action
- **Severity:** P2
- **So what:** The loudest ask on the home page collects an email for a newsletter, not a trial, so the visual hierarchy pulls visitors toward the action furthest from the goal.
- **Framework tags:** hierarchy, competing asks
- **Flow:** shape_v2
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Newsletter band is full-width solid purple with an input and "Subscribe" button; "See it in action" is a small outlined button at hero bottom-left
  - Evaluator at 00:11: "The newsletter box below it is much bigger and brighter than that button."
  - Sceptic at 00:08 on mobile: "a button "See it in action" and under it a big purple newsletter box."
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:9` · `persona-sceptic/session.log:6` · `persona-evaluator/findings-raw.json` 01:10
  > "The newsletter box is bigger and brighter than the button that shows the product."
- **Repro:**
  1. Open `/index.html`, scroll one screen
  2. Compare the purple "Get the Nimbus newsletter" band with the outlined hero button
- **Fix:** Demote the newsletter band to a footer line and give the filled purple treatment to the primary trial button.

### b3de5c757a43 — About page, the peak-trust moment, offers no onward action
- **Severity:** P2
- **So what:** Both personas said About was the first thing that felt real, and the page gives them nothing to do with that feeling — a leak at the exact point they were most ready.
- **Framework tags:** dead-end, availability
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Page body: company paragraph, three FAQ answers, footer links "Privacy · About · Pricing" — no button, no trial, no contact
  - Evaluator 03:50: "That's the first thing on this site that felt like a real business."
  - Sceptic 01:30–01:50 got the answer they came for here, then went back to the home page and left
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12` · `persona-evaluator/timeline.json` shape_v3 `trust_up`
  > "OK — a real company, eight people, founded 2023 by Priya Raman, Bristol, a company number. That's the first thing on this site that felt like a real business."
- **Repro:**
  1. Open `/about.html`; scroll to the end
  2. Note no call to action between the last FAQ answer and the footer
- **Fix:** Add a "Start free trial" button under the FAQ on `/about.html`, and move the three FAQ answers onto the home page above "Book a demo".

### a3a89259716e — Features nav link lands on a bare 404 with no route back
- **Severity:** P2
- **So what:** The page a visitor opens to learn what the product does is a server error with no header, nav, or link, so the visit stalls until they use the browser back button.
- **Framework tags:** dead-end, availability
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - "Error response · Error code: 404 · Message: File not found." — default server page, no site chrome
  - "Features" is the second item in the header nav on every page
  - Evaluator hit it at 03:30, immediately after backing out of the demo form
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `crawl/html/1-index.html:6`
  > "Clicked "Features" in the nav. Got a 404 page: "That page does not exist.""
- **Repro:**
  1. Open `/index.html`, click "Features" in the header
  2. Observe the raw 404 with no navigation
- **Fix:** Either publish `/features.html` or remove "Features" from the nav until it exists; in both cases serve a branded 404 with the header and a trial link.

### 803e66ca44f5 — Log in is the only filled button in the nav, outranking every new-visitor action
- **Severity:** P3
- **So what:** The most prominent persistent element on every page serves existing customers, while a new visitor has no equivalently weighted action on any page.
- **Framework tags:** hierarchy
- **Flow:** shape_v1
- **Locator:** /index.html nav a.btn
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Header on all 5 pages: "Home · Features · Pricing · About" as text links, "Log in" as a solid purple filled button
  - No "Sign up" or "Try free" beside it
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-sceptic/screenshots/00-landing.png` · `crawl/html/1-index.html:6`
- **Repro:**
  1. Open any page; compare the header buttons
- **Fix:** Add a filled "Start free trial" button beside "Log in" in the header and render "Log in" as a text link.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Required-field markers may be absent in the rendered form — inferred from markup only; `03-demo-form.png` captured blank, so the rendered labels were never seen
- Newsletter "Subscribe" may accept an empty email — the persona never interacted with it; no evidence
- Mobile fold may hide the hero button below the cookie bar — `persona-sceptic/screenshots/00-landing.png` shows the button above the bar; no evidence of occlusion

## For other lenses
- Cookie bar "We use no tracking cookies on this site." contradicts privacy page cookies-and-partners wording — `trust`
- "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology" undefined; time-to-comprehension null for both personas — `clarity`
- Testimonials attributed to "a happy customer", "a user", "anonymous" — `trust`
- Hero image renders a fallback-text overlay ("…a real capture serves assets/generated/hero.png…") — `technical`
- `/features.html` returns 404 from a nav link on every page — `seo`, `technical`

## Coverage gaps
- `app/login.html` never opened
- `/features.html` content never seen (404)
- Demo form rendered state unverified — screenshot blank
- No form submitted, by design; post-submission behaviour unknown and unscored
- Sceptic never opened Pricing or the demo form; mobile pricing and form experience unobserved

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00-landing.png` … `06-privacy.png`; `persona-sceptic/screenshots/00-landing.png` … `02-about.png`
