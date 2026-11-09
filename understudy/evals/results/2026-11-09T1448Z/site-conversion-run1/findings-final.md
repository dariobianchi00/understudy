# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion lens — hierarchy, availability, burden, match, dead ends, wrong friction, competing asks
- Scored against goal: "Start a free trial without talking to sales"
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 00456c9ed7bd — No free trial or self-serve signup exists; every call to action routes to sales
- **Severity:** P0
- **So what:** The stated goal cannot be reached on this site; a visitor ready to try it has nowhere to go but sales.
- **Framework tags:** Availability, Friction of the wrong kind, Match
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - No crawled page contains "trial", "sign up" or any self-serve start; only "Log in" for existing users
  - Every plan's button reads "Contact sales" and links to `index.html#demo`, a "Book a demo" form
  - Hero's only action is "See it in action" (`href="#"`); both personas got nothing from it
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `crawl/html/3-pricing.html:12-14` · `crawl/html/1-index.html:6,12,28` · `persona-evaluator/session.log:20,29`
  > "Would I do anything next? No. Without a price I can't take this to my team. I'd search for an alternative."
- **Repro:**
  1. Open `/` and `/pricing.html`
  2. Look for any button that starts a trial or creates an account
  3. Every action resolves to "Log in" or "Contact sales" → "Book a demo"
- **Fix:** Add a "Start free trial" button (email + password only) to the hero, header and each pricing card, replacing "Contact sales" on Starter and Team.

### 3a9fef67e137 — Pricing page shows no price on any of its three plans
- **Severity:** P0
- **So what:** The evaluator came to learn the cost, could not, and left to find an alternative.
- **Framework tags:** Friction of the wrong kind, Match
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three cards — Starter, Team, Enterprise — no figures; all say "Contact sales"
  - Only explanation: "Pricing depends on your workspace type and sync topology."
  - Objective "find out what it costs without giving an email": `gave_up: true`, `price_found: false`
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` (objectives[0], shape_v3.price_found) · `persona-evaluator/persona-debrief.md` Q3
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."
- **Repro:**
  1. Open `/pricing.html`
  2. Look for a number on any plan
- **Fix:** Print a per-seat monthly price on Starter and Team; keep "Contact sales" for Enterprise only.
- P0 rather than P1: the persona could not complete the objective flow and gave up; a reader may downgrade if price is not part of the goal.

### e7da6392739d — Demo form requires five fields, including phone, before any product is shown
- **Severity:** P1
- **So what:** The only path offered demands a phone number from someone who has seen nothing; the evaluator backed out.
- **Framework tags:** Burden, Match
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Counted from DOM: 7 fields — First name, Last name, Work email, Phone number, Company, Company size, "What do you want to see?"
  - 5 marked `required`: first name, last name, work email, phone, company
  - Reached from every "Contact sales" button; no product view, demo video or price precedes it
- **Evidence:** `crawl/html/1-index.html:28-34` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:20-22` · `persona-evaluator/timeline.json` (forms_opened 1, forms_submitted 0)
  > "Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. On `/pricing.html`, click any "Contact sales"
  2. Land on "Book a demo"; count fields and `required` attributes
- **Fix:** Cut the demo form to work email plus optional message; drop phone entirely or make it optional.
- Note: `03-demo-form.png` captured blank; field count is from the DOM and the partial view in `01-scrolled.png`.

### 69ba17becd72 — Newsletter banner outweighs the primary hero call to action
- **Severity:** P2
- **So what:** The loudest ask on the home page is a newsletter, not the next step towards a trial.
- **Framework tags:** Hierarchy, Competing asks
- **Flow:** V2
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action": small outlined button, bottom-left of hero
  - "Get the Nimbus newsletter": full-width filled purple banner with input and "Subscribe", directly below
  - Both personas named the newsletter as the bigger thing
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6`
  > "The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/` at 1440×900
  2. Compare the hero button with the purple banner below it
- **Fix:** Make the trial button the filled, primary-coloured hero button; move the newsletter to a small footer line.

### 86c4a67f73e3 — About page, where trust peaked, offers no onward action
- **Severity:** P2
- **So what:** Both personas felt most convinced on About and found no button to act on that conviction.
- **Framework tags:** Dead ends, Availability
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Page body: company facts and 3 FAQs; no call to action — only nav, "Log in" and footer links
  - Evaluator: "first thing on this site that felt like a real business"
  - Sceptic: "Good. That is a real company."
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `crawl/html/4-about.html:8-19` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12`
  > "Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/about.html`
  2. Scroll to the end; look for any action other than navigation
- **Fix:** Add a "Start free trial" button after the FAQ on `/about.html`.

---

## Dropped for want of evidence
- Demo form layout and required markers as rendered — `03-demo-form.png` is blank; DOM used instead
- Mobile visibility of "Log in" / nav overflow on iPhone — out of lens, and no tap on it in the session

## For other lenses
- "See it in action" has `href="#"` and does nothing when clicked — bugs
- "Features" in the nav returns a 404 — bugs
- Cookie bar "We use no tracking cookies" contradicts privacy page; sceptic left over it — trust
- Anonymous testimonials ("— a happy customer", "— a user", "— anonymous") — trust
- Hero subhead "bi-directional sync graph with a zero-knowledge vault" not understood — clarity
- Hero image renders placeholder text instead of an image — technical

## Coverage gaps
- No form was submitted, by design; post-submission behaviour not scored
- Sceptic never opened Pricing or the demo form
- Mobile pricing page seen only in `measure/`, not by a persona

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00–06`, `persona-sceptic/screenshots/00–02`
