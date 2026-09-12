# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion — hierarchy, availability, burden, match, dead ends, wrong-kind friction, competing asks; scored against the stated goal
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator on desktop-1440x900, sceptic on iphone-13)
- Scoring model: opus
- Goal scored against: "Start a free trial without talking to sales" (`manifest.json` → `conversion_goal`)
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Forms were opened and backed out of, never submitted; nothing here speaks to what happens after submission

---

## Findings

### d431a51d9851 — No self-serve trial exists; every path to the product ends at Contact sales
- **Severity:** P0
- **So what:** The stated goal — start a free trial without talking to sales — cannot be taken anywhere on the site, by either visitor.
- **Framework tags:** C-AVAILABILITY, C-WRONG-FRICTION
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - All three pricing cards — "Starter", "Team", "Enterprise" — carry the same single button, "Contact sales"; no trial, signup or "get started" link on any card.
  - The only account-shaped link on any page is nav "Log in" (`app/login.html`), which serves existing users, not new ones.
  - The home page's only conversion form is headed "Book a demo" and submits as "Request demo"; the evaluator gave up on the objective at 02:30.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:17` · `persona-evaluator/timeline.json` → `objectives[0].gave_up: true` · DOM `crawl/html/1-index.html:6,29,34`
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." — evaluator, debrief Q3
- **Repro:**
  1. Open `/pricing.html` at 1440×900.
  2. Read the three plan cards — every button is "Contact sales".
  3. Return to `/index.html`; the only form is "Book a demo"; the only nav button is "Log in".
- **Fix:** Put a "Start free trial" button on the Starter and Team cards and in the hero, linking to a self-serve signup that asks for email and password only.

### c1d9c77a862c — Pricing page shows no numbers, so the visitor cannot work out what they would pay
- **Severity:** P1
- **So what:** The evaluator arrived to learn the cost, could not, and left to search for an alternative — the site lost its most ready visitor on this page.
- **Framework tags:** C-AVAILABILITY, C-MATCH
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three cards, zero prices; the only explanatory line is "Pricing depends on your workspace type and sync topology."
  - Evaluator at 02:10: "I don't know what my workspace type is. I haven't got one."
  - `timeline.json` → `shape_v3.price_found: false`, `price_understood: false`; objective attempt ended at 02:30 with `gave_up: true`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json`
  > "So I can't find out what it costs. That's the thing I came to check." — evaluator, session.log:19
- **Repro:**
  1. Click nav "Pricing" from the home page.
  2. Look for any currency figure on the page — there is none.
- **Fix:** Print a monthly price per seat on the Starter and Team cards, and replace "workspace type and sync topology" with the one variable that actually changes the price.
- Rated one band below blocker on purpose: the evaluator's exit was caused by this, but the blocking defect for the stated goal is the missing trial path (d431a51d9851); a price alone would still not let them start.

### 1bbde20643d3 — The only above-fold call to action goes nowhere, leaving the fold with no next step
- **Severity:** P1
- **So what:** Both visitors tried the one action the hero offers and got nothing; the fold, where most visitors decide, moves nobody toward the goal.
- **Framework tags:** C-HIERARCHY, C-AVAILABILITY
- **Flow:** V1
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero holds one CTA, an outlined "See it in action" whose markup is `<a class="cta" href="#">`; no trial or signup control above the fold on desktop or mobile.
  - Evaluator clicked it twice at 00:40: "Nothing happened. The page didn't move."
  - Sceptic tapped it at 02:20 looking for the product: "The button does nothing when I tap it."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · DOM `crawl/html/1-index.html:12`
  > "'It remembers everything.' No — nothing on the site shows it remembering anything; the button that might have doesn't work." — sceptic, debrief Q6
- **Repro:**
  1. Load `/index.html` on desktop or iPhone 13.
  2. Click "See it in action" — no navigation, no scroll, no modal.
- **Fix:** Make the hero's primary button "Start free trial" linking to signup, and demote "See it in action" to a secondary link that actually scrolls to or plays a product demo.

### 12af4d847c66 — Demo form demands 7 fields, 5 required including phone, before any product is shown
- **Severity:** P1
- **So what:** The one working conversion point on the site asks a visitor who has seen no screenshot and no price for a phone number; the evaluator backed out at 03:15.
- **Framework tags:** C-BURDEN, C-MATCH, C-WRONG-FRICTION
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Fields counted from markup: First name (required), Last name (required), Work email (required), Phone number (required), Company (required), Company size (select), What do you want to see? — 7 fields, 5 required.
  - No required markers are shown to the visitor on the labels; the `required` attribute is present only in markup.
  - The page offers no product screenshot, video or price before the form; the hero image is a placeholder graphic.
- **Evidence:** `persona-evaluator/session.log:21-22` · `persona-evaluator/screenshots/01-scrolled.png` (form head, "Book a demo", "First name", "Last name") · DOM `crawl/html/1-index.html:29-34` · `persona-evaluator/timeline.json` → `forms_opened: 1, forms_submitted: 0`
  > "Seven. Phone is required. I haven't seen the product and they want my phone number." — evaluator, session.log:21
- **Repro:**
  1. On `/index.html` scroll to "Book a demo" (or click any "Contact sales" on `/pricing.html`).
  2. Count the inputs; try to submit empty — five fields block.
- **Fix:** Cut the demo form to work email plus an optional "what do you want to see?" field, drop phone entirely, and place a product screenshot or 30-second clip above it.
- Note: `03-demo-form.png` captured blank; the field count and required state come from the served markup and the session log, not the screenshot.

### 38509741a83c — Newsletter box and Log in outrank the primary call to action in visual weight
- **Severity:** P2
- **So what:** The two loudest elements on the home page serve list-building and existing users; a new visitor's eye is pulled away from any path to trying the product.
- **Framework tags:** C-HIERARCHY, C-COMPETING
- **Flow:** V2
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "Get the Nimbus newsletter" sits in a full-width solid purple band with a white "Subscribe" button, directly beneath the hero.
  - Nav "Log in" is the only solid-filled button in the fold; "See it in action" is a small outlined ghost button.
  - Evaluator at 00:11: "The newsletter box below it is much bigger and brighter than that button."; sceptic at 00:08 also named the "big purple newsletter box" as what the page wants.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6` · `persona-evaluator/findings-raw.json` (t 01:10)
  > "The newsletter box is bigger and brighter than the button that shows the product." — evaluator, findings-raw.json
- **Repro:**
  1. Load `/index.html`; note the purple band and "Subscribe" immediately below the hero.
  2. Compare its size and fill to "See it in action".
- **Fix:** Move the newsletter band to the footer as a single line, and give the hero's trial button the solid purple fill currently spent on "Log in" and "Subscribe".

### e3e1e2e1e485 — About page, the site's strongest trust moment, offers no onward action
- **Severity:** P2
- **So what:** Both visitors said this page made the company feel real, and neither could act on that feeling without leaving the page and hunting.
- **Framework tags:** C-DEAD-END, C-AVAILABILITY
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` contains company facts and three FAQ answers, then the footer; no button, no link to pricing or a trial in the body.
  - Evaluator at 03:50: "That's the first thing on this site that felt like a real business." — then went to Privacy and left.
  - Sceptic at 01:50 found the data-location answer here, then went back to the home page and stopped at 02:40.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12`
  > "Those are actual answers. Why isn't this on the home page?" — evaluator, session.log:25
- **Repro:**
  1. Open `/about.html`.
  2. Scroll to the end — the FAQ is followed only by the footer.
- **Fix:** Add a "Start free trial" button under the FAQ on `/about.html`, and repeat the three FAQ answers on the home page above the demo form.

### 09d6a7d964df — Contact sales button on pricing lands on the Book a demo form, not a sales contact
- **Severity:** P3
- **So what:** The visitor who asked to talk about price is handed a demo request with no mention of price, so the click does not deliver what its label promised.
- **Framework tags:** C-MATCH, C-DEAD-END
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Evaluator clicked "Contact sales" at 02:44 and arrived at `/index.html#demo`, headed "Book a demo".
  - The form's free-text field is "What do you want to see?"; no field or copy refers to pricing or a quote.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:20` · `persona-evaluator/timeline.json` → `pages_visited` includes `/index.html#demo`
  > "Clicked 'Contact sales' — it took me back to the demo form on the home page." — evaluator, session.log:20
- **Repro:**
  1. On `/pricing.html` click any "Contact sales".
  2. Observe the destination heading "Book a demo".
- **Fix:** Either relabel the pricing buttons "Request a demo" or give them a short "Get a quote" form that mentions price in its heading.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether the demo form submits, and what the visitor receives for it — by design, no form was submitted this run.
- Whether `app/login.html` contains a signup path — neither persona opened it; not reachable as a visitor step this run.
- The mobile scroll of the home page below the hero — the sceptic went straight to the footer, so no mobile screenshot of the newsletter band or demo form exists.

## For other lenses
- Nav "Features" returns a 404 ("Error response … 404") — `persona-evaluator/screenshots/04-features-404.png`, `session.log:23` — bugs
- "See it in action" is `href="#"` with no handler — `crawl/html/1-index.html:12` — bugs
- Cookie bar "We use no tracking cookies on this site." contradicts the Privacy page's cookies-and-partners wording — both debriefs Q5 — trust
- Testimonials attributed to "a happy customer", "a user", "anonymous" — `01-scrolled.png` — trust
- "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology" undefined — both session logs — clarity
- `03-demo-form.png` captured as a blank white frame — capture quality

## Coverage gaps
- Sceptic (iphone-13) never opened Pricing or the demo form; mobile conversion surfaces below the fold untested.
- `app/login.html` never opened by either persona.
- `/features.html` returned 404, so any conversion content intended there was unseen.
- Persona mode `generic`: both personas are inferred, not researched.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00-landing.png`, `01-scrolled.png`, `02-pricing.png`, `03-demo-form.png` (blank), `04-features-404.png`, `05-about.png`, `06-privacy.png`; `persona-sceptic/screenshots/00-landing.png`, `01-privacy.png`, `02-about.png`
