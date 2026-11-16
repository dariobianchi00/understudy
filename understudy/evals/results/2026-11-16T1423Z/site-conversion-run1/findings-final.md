# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion against the stated goal — hierarchy, availability, burden, match, dead ends, wrong-kind friction, competing asks
- **Goal scored against:** "Start a free trial without talking to sales" (`manifest.json` → `conversion_goal`)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (`persona_mode: generic`); findings rest on invented personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- `persona-evaluator/screenshots/03-demo-form.png` is a blank white frame; the form is scored from the DOM (`crawl/html/1-index.html:29-35`) and the top of the form in `01-scrolled.png`

---

## Findings

### f8cb4003bda3 — No free-trial or sign-up action exists anywhere; every plan routes to Contact sales
- **Severity:** P0
- **So what:** The stated goal — a trial without sales — cannot be completed by any visitor; the only path is the sales path.
- **Framework tags:** Availability, Friction of the wrong kind
- **Flow:** shape_3
- **Locator:** /pricing.html .price-card .cta
- **Personas hit:** evaluator
- **Observed:**
  - All three plans ("Starter", "Team", "Enterprise") carry one button, "Contact sales", linking to `index.html#demo`
  - No "trial", "sign up" or "get started" link on any crawled page; header offers only "Log in"
  - Home page asks are "See it in action" (`href="#"`), newsletter "Subscribe", and "Request demo"
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/screenshots/00-landing.png` · `crawl/html/3-pricing.html:12-14` · `crawl/html/1-index.html:6,12,15,34` · `persona-evaluator/session.log:17,20`
  > "Clicked "Contact sales" — it took me back to the demo form on the home page."
- **Repro:**
  1. Open `/pricing.html`
  2. Look for any self-serve start on Starter ("For individuals.")
  3. Click "Contact sales" — lands on "Book a demo"
- **Fix:** Replace "Contact sales" on Starter and Team with "Start free trial" linking to an email-only sign-up; keep sales for Enterprise.

### 0dc045d1ba50 — No plan shows a price, so the evaluator gave up and would look for an alternative
- **Severity:** P1
- **So what:** The visitor who came to check cost left with no next step and named a competitor search as their action.
- **Framework tags:** Availability, Match
- **Flow:** shape_3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three plan cards, zero numbers; only note is "Pricing depends on your workspace type and sync topology."
  - Evaluator stopped the price hunt at 02:30 and declined to proceed at 06:10
  - `timeline.json` → `price_found: false`, objective `gave_up: true`
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19,29` · `persona-evaluator/timeline.json` (`shape_v3.price_found`, `objectives[0].gave_up`) · `persona-evaluator/persona-debrief.md` Q3
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."
- **Repro:**
  1. Open `/pricing.html`
  2. Look for a per-seat or per-month figure on any card
- **Fix:** Print a monthly price (or "Free for N days, then £X/month") on Starter and Team; drop the "workspace type and sync topology" line.

### b8a791e0f147 — Contact sales leads to a seven-field demo form that requires a phone number before any product is shown
- **Severity:** P1
- **So what:** A visitor with no price and no product view is asked for five required fields including phone, and backs out.
- **Framework tags:** Burden, Match, Friction of the wrong kind
- **Flow:** shape_3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Seven fields counted from DOM: First name, Last name, Work email, Phone number, Company, Company size, "What do you want to see?"
  - Five carry `required`, including `type="tel"` Phone number; no required markers are visible on labels in `01-scrolled.png`
  - Evaluator opened the form at 02:44 and backed out at 03:15 without submitting
- **Evidence:** `crawl/html/1-index.html:29-34` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:20-22` · `persona-evaluator/timeline.json` (`forms_opened: 1`, `forms_submitted: 0`)
  > "Seven. Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html`, click any "Contact sales"
  2. Read the "Book a demo" form at `/index.html#demo`
- **Fix:** Cut the demo form to work email plus an optional note, make phone optional, and offer the trial beside it.

### ea510313ebe8 — Newsletter box outweighs the only hero call to action, so the loudest ask is not the goal
- **Severity:** P2
- **So what:** The page's visual priority sends attention to a newsletter, not toward starting a trial; untested how much this costs.
- **Framework tags:** Hierarchy, Competing asks
- **Flow:** shape_2
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero action "See it in action" is a small outlined button; newsletter is a full-width solid purple band with white "Subscribe"
  - "See it in action" links to `href="#"`; both personas pressed it and nothing happened
  - No call to action toward the goal appears at any scroll depth before "Book a demo"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `crawl/html/1-index.html:12,15` · `persona-evaluator/session.log:8,12` · `persona-sceptic/session.log:6,13`
  > "The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/index.html` at 1440×900
  2. Compare the "See it in action" button with the "Get the Nimbus newsletter" band
- **Fix:** Make "Start free trial" the solid primary hero button and demote the newsletter to a plain footer field.

### 2b2c181cc438 — About page, where the evaluator's trust peaked, offers no next step
- **Severity:** P2
- **So what:** The one page that persuaded both personas ends with no action, so the moment of highest readiness is wasted.
- **Framework tags:** Dead ends, Availability
- **Flow:** shape_3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Page body is company facts and three FAQ answers; no button or link in `<main>`
  - Evaluator called it "the first thing on this site that felt like a real business"; sceptic: "That is a real company."
  - Both moved on to other pages; neither acted from it
- **Evidence:** `crawl/html/4-about.html` (`<main>` block) · `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:24-26` · `persona-sceptic/session.log:11-13`
  > "Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/about.html`
  2. Read to the end of the FAQ; look for an onward action
- **Fix:** Add a "Start free trial" button under the FAQ on `/about.html`.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Demo form field layout and visible required markers on desktop — `03-demo-form.png` is blank; only the first two labels are visible in `01-scrolled.png`.
- Mobile call-to-action hierarchy on iPhone 13 — no mobile screenshot of the newsletter band or demo form was captured.
- What happens after "Request demo" or "Subscribe" — never submitted, by design; not speculated.

## For other lenses
- "See it in action" is a dead link (`href="#"`), hit by both personas — bugs
- "Features" in the nav returns a 404 — bugs
- No price is also a trust signal: evaluator "Money, no — I don't know what they'd charge" — trust
- Cookie bar "We use no tracking cookies" contradicts Privacy page "We use cookies"; sceptic left over it — trust
- Anonymous testimonials ("— a happy customer", "— anonymous") — trust
- "bi-directional sync graph with a zero-knowledge vault" not understood — clarity
- Privacy page says "Questions? Use the demo form." with no link — trust

## Coverage gaps
- No sign-up or trial flow exists to traverse, so trial-form burden could not be scored
- Sceptic never attempted pricing or any form; left at 02:40 on trust grounds
- `03-demo-form.png` captured blank; recapture needed

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06 · sceptic 00–02
