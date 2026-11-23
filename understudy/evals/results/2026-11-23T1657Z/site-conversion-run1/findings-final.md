# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion goal "Start a free trial without talking to sales" — hierarchy, availability, burden, match, dead ends
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 527fcf5e8f83 — No self-serve free trial exists anywhere on the site; every route to a next step ends at sales
- **Severity:** P0
- **So what:** The stated goal cannot be reached by anyone; the only offered paths are "Contact sales", "Request demo" and a newsletter.
- **Framework tags:** Availability, Friction of the wrong kind
- **Flow:** shape_v3
- **Locator:** /index.html header nav
- **Personas hit:** evaluator
- **Observed:**
  - No "trial", "sign up" or "start free" link or button on any of the 5 crawled pages; header nav ends in "Log in" only
  - All three pricing cards link "Contact sales" to `index.html#demo`, a form titled "Book a demo"
  - Evaluator followed the only route offered and gave up; Q3 answer: "Nothing"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:20` · `persona-evaluator/session.log:29` · `crawl/html/1-index.html:6` · `crawl/html/3-pricing.html:12-14`
  > "Would I do anything next? No. Without a price I can't take this to my team. I'd search for an alternative."
- **Repro:**
  1. Open `/` and read the header nav and hero
  2. Open Pricing; click any "Contact sales"
  3. Note you land on "Book a demo"; no trial path exists
- **Fix:** Add a "Start free trial" button to the header, the hero and each pricing card, linking to a self-serve signup with no sales step.

### a4f3fe97a311 — Pricing page shows no price on any plan, so the visitor cannot judge whether to start
- **Severity:** P1
- **So what:** Price was the evaluator's stated reason to visit; with none shown they abandoned the site to look for an alternative.
- **Framework tags:** Friction of the wrong kind, Match
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise cards carry no number; each says only "Contact sales"
  - Footnote reads "Pricing depends on your workspace type and sync topology."
  - `timeline.json` objective: `price_found: false`, `gave_up: true` at 02:30
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` (objectives[0])
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. Open `/pricing.html`
  2. Look for a currency amount on any card
- **Fix:** Print a monthly price on Starter and Team cards, keep "Contact sales" only on Enterprise, and replace the "sync topology" footnote.

### 735eb1224a54 — Demo form asks seven fields, five required including phone, before any product is shown
- **Severity:** P1
- **So what:** The evaluator had seen no product and no price, was asked for a phone number, and backed out.
- **Framework tags:** Burden, Match
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Fields counted from DOM: first name, last name, work email, phone, company, company size, "What do you want to see?" — 7 total
  - 5 carry `required`: first name, last name, work email, phone (`type="tel"`), company
  - Persona's own count matches (7, phone required); they did not submit
- **Evidence:** `crawl/html/1-index.html:28-34` · `persona-evaluator/screenshots/01-scrolled.png` (form heading and first field) · `persona-evaluator/session.log:21-22`
  > "Seven. Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. From `/pricing.html` click "Contact sales"
  2. Read the "Book a demo" form fields and required markers
- **Fix:** Cut the form to work email plus an optional note, drop phone entirely, and place it after the trial path rather than instead of it.

### 5e6f863c35cc — Newsletter box and Log in button outweigh the hero call to action
- **Severity:** P2
- **So what:** The loudest asks on the home page serve existing users and email capture, not a first-time visitor's next step.
- **Framework tags:** Hierarchy, Competing asks
- **Flow:** shape_v1
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is a small outlined button; the newsletter is a full-width solid purple band directly below the hero
  - The only filled button above the fold is "Log in" in the header
  - Both personas named the newsletter box as more prominent than the hero button
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6`
  > "There's a small outlined "See it in action" button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/` at 1440×900
  2. Compare visual weight of "See it in action", "Log in" and the newsletter band
- **Fix:** Make a solid "Start free trial" the hero's primary button and demote the newsletter to a single footer line; size of the effect is untested.

### c0d7916c8acd — About page, where trust peaked for both personas, offers no onward action
- **Severity:** P2
- **So what:** The one page both personas found convincing ends in a footer, so readiness peaks with nothing to act on.
- **Framework tags:** Dead ends, Availability
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Page has company facts and 3 FAQ answers, then footer links only; no button in the body
  - Evaluator: "That's the first thing on this site that felt like a real business"
  - Sceptic: "Good. That is a real company." — then returned home and left
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `crawl/html/4-about.html:9-19` · `persona-evaluator/session.log:24` · `persona-sceptic/session.log:11`
  > "OK — a real company, eight people, founded 2023 by Priya Raman, Bristol, a company number."
- **Repro:**
  1. Open `/about.html`
  2. Scroll to the end of the FAQ; look for an action other than nav and footer links
- **Fix:** Add a "Start free trial" button below the FAQ on /about.html.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Form layout and required markers as rendered — `persona-evaluator/screenshots/03-demo-form.png` is blank white; field count above rests on DOM and the persona's log instead.
- Mobile CTA reachability on scroll (sticky or not) — sceptic did not scroll the home page past the first screen; `shape_v2.sections_seen: 1`.

## For other lenses
- "See it in action" has `href="#"` and does nothing when clicked or tapped (`session.log:12`, sceptic `session.log:13`) — bugs
- Nav "Features" returns a 404 (`04-features-404.png`) — bugs
- Cookie bar "no tracking cookies" contradicts privacy page; sceptic left over this (sceptic debrief Q3) — trust
- Anonymous testimonials ("— a happy customer", "— anonymous") — trust
- Headline "Your thoughts, everywhere." and "bi-directional sync graph" do not say what or for whom — clarity

## Coverage gaps
- Sceptic never looked for a price or a signup route (`objectives[0].attempted: false`)
- No persona opened the newsletter or the "Log in" target `app/login.html`
- Only one form opened; none submitted (by design)

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-*/timeline.json`
- C. Screenshot index — evaluator 00–06, sceptic 00–02
