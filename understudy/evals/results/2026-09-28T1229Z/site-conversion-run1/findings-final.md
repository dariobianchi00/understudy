# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion. Hierarchy, availability, burden, match, dead ends and competing asks, scored against the stated goal
- Goal scored against: "Start a free trial without talking to sales"
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact. Unsupported observations are dropped and listed at the end

---

## Findings

### 1f716db724ee — No self-serve free trial exists anywhere on the site
- **Severity:** P0
- **So what:** The stated goal cannot be completed. The only way in for a new visitor is to talk to sales, which the goal rules out.
- **Framework tags:** Availability, Friction of the wrong kind
- **Flow:** V3
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - None of the 5 crawled pages contains "trial", "sign up" or "get started".
  - The actions on offer are "See it in action", newsletter "Subscribe", "Request demo", 3× "Contact sales" and "Log in" (existing users only).
  - The evaluator's Q3 answer was "Nothing". The sceptic's was "Leave". Neither found a self-serve step.
- **Evidence:** `crawl/html/1-index.html:6,12,15,34` · `crawl/html/3-pricing.html:12-14` · `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:29` · `persona-evaluator/persona-debrief.md` Q3
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."
- **Repro:**
  1. Open `/index.html` and every page linked from the nav and footer.
  2. Look for any action that starts a trial without a sales contact. There is none.
- **Fix:** Add a filled "Start free trial" button to the hero, the nav (beside "Log in") and every pricing card. It should go to a self-serve signup.

### 95c494e5366e — Pricing page shows no prices; all three plans route to Contact sales
- **Severity:** P1
- **So what:** The evaluator came to check the cost, could not find it, and gave up on the site. The trial goal was dead from that point.
- **Framework tags:** Availability, Match, Friction of the wrong kind
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - There are 3 cards (Starter, Team, Enterprise) and no figure on any of them. Each card's only button is "Contact sales".
  - Even "Starter — For individuals." requires contacting sales.
  - Under the cards: "Pricing depends on your workspace type and sync topology." The persona did not know what their workspace type was.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` objectives[0].gave_up = true · `crawl/html/3-pricing.html:12-16`
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. Click "Pricing" in the nav.
  2. Read all three cards. There is no price, and the only action is "Contact sales".
- **Fix:** Show a monthly price on Starter and Team, and change their buttons to "Start free trial". Keep "Contact sales" on Enterprise only.

### 12af4d847c66 — Demo form demands 7 fields, 5 required including phone, before any product is shown
- **Severity:** P1
- **So what:** The form asks too much for how ready the visitor was. The evaluator had seen no product and no price, so they backed out.
- **Framework tags:** Burden, Match
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - The fields, counted from the DOM, are: first name, last name, work email, phone number, company, company size and "What do you want to see?". That is 7 fields.
  - 5 of them are `required`: first name, last name, work email, phone and company. None is visibly marked as required or optional.
  - Every "Contact sales" button on the pricing page lands here. This form is the only route forward from pricing.
- **Evidence:** `crawl/html/1-index.html:28-35` · `persona-evaluator/screenshots/01-scrolled.png` (form heading and first field) · `persona-evaluator/session.log:20-22` · `persona-evaluator/screenshots/03-demo-form.png` (captured blank, so the field count comes from the DOM)
  > "Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. On `/pricing.html`, click any "Contact sales".
  2. The "Book a demo" form opens with 7 fields, 5 of them required, including phone.
- **Fix:** Offer self-serve signup (email only) as the main path. Cut the demo form to name, work email and company, and make phone optional.

### 3edd6a6ae496 — Newsletter box outweighs the only product call to action on the home page
- **Severity:** P2
- **So what:** The loudest ask on the home page leads away from the goal. A visitor who is ready to try the product is steered to a mailing list instead.
- **Framework tags:** Hierarchy, Competing asks
- **Flow:** V2
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is a small outlined button. The newsletter box right below it is a full-width, solid purple band.
  - The only filled button in the header is "Log in", which serves people who already have an account.
  - Both personas noticed the imbalance and carried on.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:6`
  > "The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Load `/index.html` at 1440×900 or on an iPhone 13.
  2. Compare the visual weight of "See it in action" with the "Get the Nimbus newsletter" band.
- **Fix:** Make "Start free trial" the one filled hero button. Shrink the newsletter to a plain inline link lower on the page or in the footer.

### 004f04646dc9 — About page has no onward action at the point both personas trusted the company most
- **Severity:** P2
- **So what:** Both visitors felt most convinced on About, and the page offered them nothing to do next. That moment was lost to the layout.
- **Framework tags:** Dead ends, Availability
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The About body has no button or link to try, buy or sign up. The only exits are the nav and footer links.
  - The evaluator called it "the first thing on this site that felt like a real business". The sceptic said "That is a real company."
  - Both left About for Privacy, and both sessions ended without converting.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:24-26` · `persona-sceptic/screenshots/02-about.png` · `persona-sceptic/session.log:11` · `crawl/html/4-about.html:6`
  > "That's the first thing on this site that felt like a real business."
- **Repro:**
  1. Open `/about.html`.
  2. Scroll to the end. There is no call to action in the page body.
- **Fix:** Close the About page with a "Start free trial" button. Move its FAQ answers (offline, export, Frankfurt) onto the home page beside that button.

---

## Dropped for want of evidence
- Whether the demo form is followed by a sales call, or how fast. No submission was made, by design, so this is not scored.
- The field count as shown in the screenshot. `03-demo-form.png` was captured blank, so the count rests on the crawled DOM instead.

## For other lenses
- "See it in action" (`href="#"`) does nothing when clicked. Both personas tried it (evaluator session.log:12, sceptic session.log:13). — bugs
- "Features" in the nav returns a 404. — bugs
- The cookie bar ("We use no tracking cookies") contradicts the privacy page, and this drove the sceptic's "Leave". — trust
- The headline and subhead don't say what the product is or who it is for ("bi-directional sync graph", "zero-knowledge vault"). — clarity
- The testimonials are anonymous ("— a happy customer", "— anonymous"). — trust
- The JSON-LD `offers.price` is empty and invalid. — technical / seo

## Coverage gaps
- The sceptic did not look for a price or open any form, so no burden evidence exists on mobile.
- `/app/login.html` was never opened, so it is unknown whether a signup path exists behind "Log in".
- The demo form was not captured visually (blank screenshot).

## Appendices
- A. Persona debriefs: `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines: `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index: evaluator 00-landing, 01-scrolled, 02-pricing, 03-demo-form (blank), 04-features-404, 05-about, 06-privacy · sceptic 00-landing, 01-privacy, 02-about
