# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion against the stated goal — hierarchy, availability, burden, match, dead ends, wrong friction, competing asks
- Goal scored against: "Start a free trial without talking to sales"
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 9940875fe3cc — No self-serve trial exists anywhere on the site; every path to the product runs through sales
- **Severity:** P0
- **So what:** The stated goal cannot be completed by any visitor; the only routes on offer are "Contact sales", "Request demo" or a newsletter.
- **Framework tags:** Availability · Friction of the wrong kind · Match
- **Flow:** shape_v3
- **Locator:** /
- **Personas hit:** evaluator
- **Observed:**
  - No "trial", "sign up" or "get started" link on any of the 5 crawled pages; the actions available are "Log in", "See it in action" (`href="#"`), "Subscribe", "Request demo", "Contact sales"
  - All 3 pricing plans send the visitor to `index.html#demo`, a "Book a demo" form
  - Evaluator ended the visit with no step taken and named an alternative as the next move
- **Evidence:** `crawl/html/1-index.html:6,12,15,34` · `crawl/html/3-pricing.html:12-14` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:29` · `persona-evaluator/persona-debrief.md` Q3
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."
- **Repro:**
  1. Open `/` and every page in the nav and footer
  2. Look for any control that starts a trial without a sales contact — there is none
- **Fix:** Add a "Start free trial" button to the header, hero and every pricing card, leading straight to account creation with no sales step.

### e148b3d3fc9d — Pricing page shows no price on any plan, so the evaluator could not take a next step
- **Severity:** P1
- **So what:** The evaluator came to check cost, found none, and stopped — the trial decision never got made.
- **Framework tags:** Friction of the wrong kind · Availability
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise cards each show only "Contact sales"; no figure anywhere on the page
  - Only explanation: "Pricing depends on your workspace type and sync topology."
  - `timeline.json` objective "find out what it costs without giving an email": `gave_up: true` at 02:30
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` objectives[0]
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. Open `/pricing.html`
  2. Look for a price on any plan
- **Fix:** Show a monthly price on Starter and Team, with "Start free trial" as the card button; keep "Contact sales" for Enterprise only.

### 8ef7224cb932 — Contact sales lands on a demo form with five required fields, including phone, before any product is shown
- **Severity:** P1
- **So what:** A visitor who has seen no price and no product is asked for a phone number; the evaluator backed out.
- **Framework tags:** Burden · Match · Friction of the wrong kind
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - 7 fields counted from the markup: First name, Last name, Work email, Phone number, Company (all `required`), Company size, "What do you want to see?" (optional)
  - Same form serves "Starter — For individuals.", yet asks for Company and Company size
  - Evaluator opened 1 form, submitted 0, and backed out at 03:15
- **Evidence:** `crawl/html/1-index.html:29-34` · `persona-evaluator/session.log:20-22` · `persona-evaluator/timeline.json` shape_v3.forms_opened / forms_submitted · `persona-evaluator/screenshots/01-scrolled.png` (top of form)
  > "Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html` and click any "Contact sales"
  2. Count fields and `required` markers on the "Book a demo" form
- **Fix:** Cut the demo form to work email plus an optional message, make phone optional or remove it, and keep it for Enterprise only.

### 23bdef2ce210 — Hero's only call to action does nothing when clicked, leaving no next step above the fold
- **Severity:** P2
- **So what:** At the moment interest is highest, the one product action fails; both personas tried it and moved on empty-handed.
- **Framework tags:** Availability · Hierarchy
- **Flow:** shape_v2
- **Locator:** /index.html .hero a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is `<a class="cta" href="#">`; the evaluator clicked it twice with no movement
  - Sceptic tapped it on mobile, nothing happened, and stopped 20 seconds later
  - Both carried on or left for other stated reasons, so scored P2, not P1
- **Evidence:** `crawl/html/1-index.html:12` · `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:13-14`
  > "I want to see it \"remember\" something. The button does nothing when I tap it."
- **Repro:**
  1. Open `/` on desktop or mobile
  2. Click "See it in action"
- **Fix:** Replace the hero button with "Start free trial" linking to signup, with "See it in action" as a secondary link to a real product clip.

### 52924d72893b — Newsletter box and Log in button outweigh the product call to action on the home page
- **Severity:** P2
- **So what:** The loudest asks serve existing users and email capture, not the trial the business wants started.
- **Framework tags:** Hierarchy · Competing asks
- **Flow:** shape_v1
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Visual weight, highest first: full-width filled purple "Get the Nimbus newsletter" block · filled "Log in" button · outlined "See it in action"
  - Both personas named the newsletter box as bigger than the product button within 15 seconds
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6`
  > "The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/` at 1440×900
  2. Compare the fill and size of "Log in", "See it in action" and the newsletter block
- **Fix:** Give a filled "Start free trial" button the strongest weight on the page; demote the newsletter to a footer line.

### 172fb10c349e — About page, where both personas' trust peaked, offers no next step
- **Severity:** P2
- **So what:** Both personas felt most convinced here, and the page gives them nothing to act on except nav links.
- **Framework tags:** Dead ends · Availability
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Page body is company facts and 3 FAQ answers; no button or link in `<main>`
  - Evaluator: "the first thing on this site that felt like a real business"; sceptic: "That is a real company."
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `crawl/html/4-about.html:8-19` · `persona-evaluator/session.log:24` · `persona-sceptic/session.log:11`
  > "That's the first thing on this site that felt like a real business."
- **Repro:**
  1. Open `/about.html`
  2. Scroll to the footer; no onward action in the page body
- **Fix:** End the About page with a "Start free trial" button under the FAQ.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Demo form layout and required markers as rendered — `persona-evaluator/screenshots/03-demo-form.png` is blank; field count taken from markup instead
- Whether "Log in" leads to a signup option — `app/login.html` was never opened
- Mobile sticky CTA behaviour while scrolling — sceptic saw 1 section, no scroll screenshots

## For other lenses
- "See it in action" `href="#"` is a dead link — bugs
- "Features" nav link returns a 404 — bugs
- Hero image shows placeholder text "…a real capture serves assets/generated/hero.png…" — bugs
- Cookie bar "We use no tracking cookies on this site." contradicts the privacy page — trust
- Anonymous testimonials ("— a happy customer", "— anonymous") — trust
- "bi-directional sync graph with a zero-knowledge vault" not understood — clarity
- Home page JSON-LD `"price": }` is invalid — seo / technical

## Coverage gaps
- `app/login.html` never opened
- Sceptic never visited `/pricing.html` or opened a form
- No mobile capture of the pricing page or demo form

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06 · sceptic 00–02
