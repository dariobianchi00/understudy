# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion mechanics against the stated goal — hierarchy, availability, burden, match, dead ends, wrong-kind friction, competing asks
- Goal scored against: "Start a free trial without talking to sales" (`manifest.json` → `conversion_goal`)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Form fields counted from the crawled DOM: `persona-evaluator/screenshots/03-demo-form.png` is blank white

---

## Findings

### 3bc930799e1f — No self-serve free trial exists anywhere; every plan routes to sales
- **Severity:** P0
- **So what:** The stated goal — start a trial without talking to sales — cannot be done on this site at all.
- **Framework tags:** Availability, Friction of the wrong kind, Match
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - All three plan cards carry one action, "Contact sales", each linking to `index.html#demo`
  - No crawled page contains "trial", "sign up", "get started" or "free"; the only filled nav button is "Log in"
  - The only home-page conversion form is "Book a demo"
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `crawl/html/3-pricing.html:12-14` · `crawl/html/1-index.html:6,28` · `persona-evaluator/session.log:20`
  > "Clicked "Contact sales" — it took me back to the demo form on the home page."
- **Repro:**
  1. Open `/pricing.html`
  2. Look for any action other than "Contact sales" on Starter, Team or Enterprise
  3. Check the nav and footer on every page for a trial or signup link
- **Fix:** Replace "Contact sales" on Starter and Team with a "Start free trial" button to a self-serve signup; keep sales on Enterprise only.

### 6745582f5edf — Pricing page shows no price on any of its three plans
- **Severity:** P1
- **So what:** The evaluator came to learn the cost, could not, and said they would search for an alternative.
- **Framework tags:** Availability, Friction of the wrong kind
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three cards — Starter, Team, Enterprise — with no figure, unit or billing period
  - Only explanation: "Pricing depends on your workspace type and sync topology."
  - Evaluator gave up the cost objective at 02:30 (`timeline.json` → `objectives[0].gave_up: true`)
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `session.log:17-19` · `persona-evaluator/timeline.json` · `persona-evaluator/persona-debrief.md` Q3
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."
- **Repro:**
  1. Open `/pricing.html`
  2. Look for a number on any plan card
- **Fix:** Print a monthly price and unit on Starter and Team (e.g. "£X per user / month"); delete the "workspace type and sync topology" line.

### 92f29a30fbe4 — Contact sales lands on a seven-field demo form that requires a phone number
- **Severity:** P1
- **So what:** The evaluator backed out of the only available conversion point, before seeing any of the product.
- **Framework tags:** Burden, Match
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - 7 fields: First name, Last name, Work email, Phone number, Company, Company size, "What do you want to see?"
  - 5 marked `required`, including "Phone number"; asked before any product, price or demo is shown
  - Evaluator counted the same seven at 02:58 and backed out at 03:15
- **Evidence:** `crawl/html/1-index.html:28-34` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:21-22`
  > "Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. On `/pricing.html`, click any "Contact sales"
  2. Read the "Book a demo" form at `/index.html#demo`
- **Fix:** Cut the demo form to work email plus optional company; make phone optional or remove it.

### 1a581c17943a — Newsletter box outweighs the only product call to action on the home page
- **Severity:** P2
- **So what:** The loudest ask on the home page is the one furthest from a trial; the product ask reads as secondary.
- **Framework tags:** Hierarchy, Competing asks
- **Flow:** shape_v2
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Above the fold: one small outlined button, "See it in action"
  - Directly below: a full-width solid purple "Get the Nimbus newsletter" band with a "Subscribe" button
  - Both personas noticed the imbalance within 11 seconds of landing
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6`
  > "There's a small outlined "See it in action" button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/index.html` at 1440×900 or on a phone
  2. Compare the "See it in action" button with the newsletter band
- **Fix:** Make a filled "Start free trial" the hero button; demote the newsletter to a single line in the footer.

### 1a23103d4fdd — About page answers buying objections, then offers no next step
- **Severity:** P2
- **So what:** The page where both personas' trust rose ends in a footer; a convinced visitor has nowhere to act.
- **Framework tags:** Dead ends, Availability
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Named founder, address, company number, and FAQ on offline use, export, data location
  - No button or link after the FAQ — only nav and footer (Privacy, About, Pricing)
  - Evaluator: "first thing on this site that felt like a real business"
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `crawl/html/4-about.html:9-20` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12`
  > "Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/about.html`
  2. Scroll to the end of the FAQ and look for an action
- **Fix:** Add a "Start free trial" button under the FAQ on /about.html.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Mobile layout of the demo form — the sceptic never opened it; no mobile screenshot of it exists.
- Whether a sticky or repeated call to action appears while scrolling — the evaluator's mid-page screenshot shows none, but no screenshot of the page bottom on mobile.

## For other lenses
- "See it in action" (`href="#"`) did nothing on click or tap, for both personas — bugs
- Nav "Features" returns a 404 — bugs
- Cookie bar "We use no tracking cookies" vs privacy page and a third-party analytics script — trust
- Anonymous testimonials ("— a happy customer", "— a user", "— anonymous") — trust
- "bi-directional sync graph with a zero-knowledge vault" undefined — clarity
- Malformed JSON-LD `"price": }` on the home page — seo

## Coverage gaps
- No submission of any form, by design; nothing scored after submit
- Sceptic never visited `/pricing.html` or opened the demo form
- `/app/login.html` not visited; no signup surface found to visit
- `persona-evaluator/screenshots/03-demo-form.png` is blank; form scored from DOM

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06, sceptic 00–02
