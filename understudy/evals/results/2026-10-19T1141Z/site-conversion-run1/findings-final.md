# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion lens. Hierarchy, availability, burden, match, dead ends and competing asks, all scored against the stated goal
- Goal under test: "Start a free trial without talking to sales" (`manifest.json` → `conversion_goal`)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, sceptic)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Size of every recommended change is untested: this run had one visitor per persona and no traffic data

---

## Findings

### 4a83e1b82e2f — No free-trial path exists on any page; every route to the product ends at sales
- **Severity:** P0
- **So what:** The stated goal cannot be reached by any visitor. A convinced visitor's only way forward is the sales route the goal rules out.
- **Framework tags:** Availability, Match, Friction of the wrong kind
- **Flow:** V3
- **Locator:** /index.html
- **Personas hit:** evaluator
- **Observed:**
  - The landing page has 4 actions: "Log in", "See it in action" (`href="#"`), "Subscribe" and "Request demo". None of them starts a trial.
  - All 3 pricing plans say "Contact sales" and link to `index.html#demo`. The privacy page says "Questions? Use the demo form."
  - The only filled button in the nav is "Log in", which is for people who already have an account. No page in the crawl contains "trial" or "sign up".
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:20` · `persona-evaluator/session.log:29` · `crawl/html/1-index.html` lines 6, 12, 15, 34 · `crawl/html/3-pricing.html` lines 12–14 · `crawl/html/5-privacy.html` line 11
  > "Would I do anything next? No. Without a price I can't take this to my team. I'd search for an alternative."
- **Repro:**
  1. Open `/index.html` logged out and list every button and link.
  2. Open `/pricing.html` and click any "Contact sales".
  3. Note that it lands on "Book a demo" and that no trial or sign-up entry exists anywhere.
- **Fix:** Add a filled "Start free trial" button to the hero, the nav (beside "Log in") and every pricing card, linking to a self-serve sign-up page.

### c7ba53336fe5 — Pricing page shows no price on any plan, so the visitor cannot judge the trial is worth starting
- **Severity:** P1
- **So what:** The evaluator came to learn the cost, could not, and gave up. That ended their visit as a conversion prospect.
- **Framework tags:** Friction of the wrong kind, Burden
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - The page has 3 cards: "Starter", "Team" and "Enterprise". There is no currency figure anywhere, and every card says "Contact sales".
  - The only explanation is "Pricing depends on your workspace type and sync topology."
  - The objective "find out what it costs without giving an email" was attempted 01:48–02:30, and `gave_up: true`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17` · `persona-evaluator/session.log:19` · `persona-evaluator/timeline.json` → `objectives[0].gave_up`, `shape_v3.price_found: false`
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. From `/index.html`, click "Pricing" in the nav.
  2. Look for a currency figure on any plan. There is none.
- **Fix:** Print a monthly price on "Starter" and "Team", and keep "Contact sales" for "Enterprise" only.

### a1273ff6a5cb — The only form asks for 5 required fields including phone before any product is shown
- **Severity:** P1
- **So what:** This is the only conversion form on the site, and it asks for a phone number before the visitor has seen anything. The evaluator refused to fill it in.
- **Framework tags:** Burden, Match
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - I counted the fields in the DOM: 7 in total. "First name", "Last name", "Work email", "Phone number" and "Company" are marked `required`. "Company size" is a select and "What do you want to see?" is optional.
  - The form is reached from "Contact sales" on pricing. At that point the visitor has seen no product: "See it in action" does nothing.
  - The persona backed out at 03:15 without submitting.
- **Evidence:** `crawl/html/1-index.html` lines 29–34 · `persona-evaluator/screenshots/01-scrolled.png` (form top visible) · `persona-evaluator/session.log:21` · `persona-evaluator/session.log:22` · `persona-evaluator/screenshots/03-demo-form.png` (blank capture, see Coverage gaps)
  > "Seven. Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html` and click any "Contact sales".
  2. On "Book a demo", count the fields and the `required` attributes.
- **Fix:** Drop "Phone number" and "Last name" from the demo form, make "Company" optional, and offer the trial beside it as the no-call alternative.

### 37335f52e4a7 — Newsletter box outweighs the primary call to action above the fold
- **Severity:** P2
- **So what:** The loudest ask on the landing page is a newsletter, not a step towards the product, so a visitor ready to act is pointed at the wrong thing.
- **Framework tags:** Hierarchy, Competing asks
- **Flow:** V1
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The hero's only action is "See it in action": a small button with an outline and no fill.
  - Directly below it, "Get the Nimbus newsletter" is a full-width, solid purple band with an input and a "Subscribe" button.
  - Both personas named the imbalance within the first 11 seconds and kept going.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6` · `crawl/html/1-index.html` lines 12, 15
  > "There's a small outlined "See it in action" button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/index.html` at 1440×900 or on an iPhone 13.
  2. Compare the weight of "See it in action" with the "Get the Nimbus newsletter" band.
- **Fix:** Make the hero button a filled "Start free trial", and move the newsletter to the footer as a plain one-line input.

### ffe37a77e4b9 — About page is where both personas' trust rose, and it offers no next step
- **Severity:** P2
- **So what:** The page that persuaded both personas has no call to action, so their moment of greatest readiness has nowhere to go.
- **Framework tags:** Dead ends, Availability
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The page body is the company facts plus 3 FAQ answers. It has no button or link in the body, only the shared nav and footer.
  - The evaluator called it "the first thing on this site that felt like a real business". The sceptic said "Good. That is a real company."
  - Both went from here to privacy or back to the home page. Neither found an action.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24` · `persona-sceptic/session.log:11` · `crawl/html/4-about.html` lines 7–19
  > "OK — a real company, eight people, founded 2023 by Priya Raman, Bristol, a company number. That's the first thing on this site that felt like a real business."
- **Repro:**
  1. Open `/about.html`.
  2. Scroll to the end of the FAQ and look for any action in the page body. There is none.
- **Fix:** End `/about.html` with a "Start free trial" button under the FAQ, and add the same button to `/privacy.html`.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The demo form may look heavier on mobile. The sceptic never opened it, and the evaluator's form screenshot is blank.
- What happens after "Request demo" or "Subscribe" is submitted. Nothing was submitted, by design, so this is not judged.

## For other lenses
- "See it in action" is `href="#"` and did nothing for either persona (evaluator `session.log:12`, sceptic `session.log:13`) — bugs
- The "Features" nav link returns a 404 (`persona-evaluator/screenshots/04-features-404.png`) — bugs
- The cookie bar says "We use no tracking cookies on this site.", the privacy page says "We use cookies and similar technologies.", and the landing page loads `analytics.example-tracker.test/t.js`. The sceptic left over this — trust
- The privacy page says "We may share information with partners" and names none — trust
- The hero copy "bi-directional sync graph with a zero-knowledge vault" was not understood by either persona — clarity
- The testimonials are attributed to "a happy customer", "a user" and "anonymous" — trust
- The hero image shows placeholder text ("a real capture serves assets/generated/hero.png") — technical
- The JSON-LD `"offers": {"price": }` is malformed — seo

## Coverage gaps
- `persona-evaluator/screenshots/03-demo-form.png` is blank. The form was scored from the DOM and the partial view in `01-scrolled.png`.
- The sceptic never visited `/pricing.html` or the demo form, so mobile conversion surfaces were not observed.
- Sign-up and trial could not be tested because no such surface exists.

## Appendices
- A. Persona debriefs: `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines: `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshots opened: evaluator 00, 01, 02, 03 (blank), 05 · sceptic 00, 02
