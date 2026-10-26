# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion lens — hierarchy, availability, burden, match, dead ends, wrong-kind friction, competing asks
- Scored against the stated goal: "Start a free trial without talking to sales"
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### c11dad5b20ee — No free trial or self-serve signup exists; every route to start goes through sales
- **Severity:** P0
- **So what:** The stated goal cannot be completed by anyone; the only paths forward are "Contact sales", "Request demo" or a newsletter.
- **Framework tags:** availability, friction-wrong-kind
- **Flow:** shape_3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - No "trial", "sign up" or "get started" link on any of the 5 crawled pages; header offers only "Log in".
  - All three plan cards (Starter, Team, Enterprise) link to `index.html#demo` with "Contact sales".
  - Evaluator gave up on the next step at 06:10 and would look for an alternative.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `crawl/html/3-pricing.html:12-14` · `crawl/html/1-index.html:6,12,15,34` · `persona-evaluator/session.log:20,29`
  > "Would I do anything next? No. Without a price I can't take this to my team. I'd search for an alternative."
- **Repro:**
  1. Open `/index.html`, `/pricing.html`, `/about.html`, `/privacy.html`.
  2. Look for any control that starts a trial or account without sales contact.
  3. Note that none exists; every plan button reads "Contact sales".
- **Fix:** Add a "Start free trial" button to the header, the hero and the Starter and Team cards, linking to self-serve signup.
- Note: the persona was not looking for a trial by name; P0 because the goal's flow does not exist on the site, not because a persona was seen failing it.

### f13583a64662 — Pricing page shows no price on any of its three plans
- **Severity:** P1
- **So what:** The evaluator came to learn the cost, could not, and abandoned — the visitor cannot judge whether a trial is worth starting.
- **Framework tags:** availability, match
- **Flow:** shape_3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - 3 plans, 0 numbers; only footnote: "Pricing depends on your workspace type and sync topology."
  - `timeline.json`: `price_found: false`, objective "find out what it costs without giving an email" → `gave_up: true`.
  - Debrief Q3 answer is "Nothing."
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` (objectives[0]) · `persona-evaluator/persona-debrief.md` Q3
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the Starter, Team and Enterprise cards.
  3. Note that no card shows a price or a "free" tier.
- **Fix:** Print a monthly price (or "Free for N days, then £X") on the Starter and Team cards; keep "Contact sales" only on Enterprise.

### 5e30896640cf — Contact sales leads to a 7-field demo form that requires a phone number before any product is shown
- **Severity:** P1
- **So what:** The evaluator backed out at the form; the ask is far heavier than this visitor's readiness, who had seen no product and no price.
- **Framework tags:** burden, match, friction-wrong-kind
- **Flow:** shape_3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - DOM count: 7 fields — First name*, Last name*, Work email*, Phone number*, Company*, Company size, "What do you want to see?" (5 required).
  - Promised return is only "Request demo"; no trial, no price, no response time.
  - Persona: "Backing out. Not filling that in." at 03:15.
- **Evidence:** `crawl/html/1-index.html:28-34` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/03-demo-form.png` (captured blank) · `persona-evaluator/session.log:20-22`
  > "Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html`, click any "Contact sales".
  2. Land on `/index.html#demo` ("Book a demo").
  3. Count fields and `required` markers.
- **Fix:** Replace the plan buttons with self-serve trial signup (email + password); if the demo form stays, cut it to name and work email and make phone optional.
- Note: field count taken from the DOM because `03-demo-form.png` is a blank capture; it matches the persona's count of seven.

### f370dbd5e665 — Newsletter box is visually louder than the hero's only call to action
- **Severity:** P2
- **So what:** The loudest ask on the home page is a newsletter, not a step toward a trial; both personas read it that way in the first 15 seconds.
- **Framework tags:** hierarchy, competing-asks
- **Flow:** shape_1
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is a small outlined button; the newsletter is a full-width solid purple band with "Subscribe".
  - Hero offers no trial or signup action; the next real ask ("Book a demo") is at the bottom of the page.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6`
  > "There's a small outlined "See it in action" button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/index.html` at 1440×900 or on iPhone 13.
  2. Compare the hero button with the purple newsletter band below it.
- **Fix:** Make a solid "Start free trial" the hero's primary button and demote the newsletter to a plain footer field; size of uplift is untested.

### c1e80671871f — About page answers buying questions but offers no next step
- **Severity:** P2
- **So what:** The one page that raised both personas' confidence ends without an action, so the moment of highest readiness is wasted.
- **Framework tags:** dead-ends, availability
- **Flow:** shape_3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Page body: company facts and 3 FAQ answers (offline, export, Frankfurt); no button or link in `<main>`.
  - Only onward routes are the shared header and footer navigation.
- **Evidence:** `crawl/html/4-about.html:8-19` · `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/screenshots/02-about.png` · `persona-sceptic/session.log:11-12`
  > "That's the first thing on this site that felt like a real business."
- **Repro:**
  1. Open `/about.html`.
  2. Scroll to the end of the FAQ.
  3. Note that there is no call to action in the page body.
- **Fix:** End the About FAQ with a "Start free trial" button and a link to `/pricing.html`.

---

## Dropped for want of evidence
- Demo form field count from screenshot — `03-demo-form.png` is blank; counted from the DOM instead (kept, see 5e30896640cf).
- Sceptic's readiness to convert — she never reached pricing or a form; no conversion moment to score.

## For other lenses
- "See it in action" (`href="#"`) does nothing when clicked or tapped, for both personas — bugs.
- "Features" nav link returns a 404 — bugs.
- Cookie bar "We use no tracking cookies" contradicts the privacy page; sceptic left over it (Q3: "Leave.") — trust.
- Anonymous testimonials ("— a happy customer", "— a user", "— anonymous") — trust.
- Headline "Your thoughts, everywhere." and "bi-directional sync graph with a zero-knowledge vault" did not say what the product is — clarity.
- Mobile header nav is clipped; "Log in" off-screen at 390px — technical.

## Coverage gaps
- No form submitted (by design); nothing after submission is scored.
- `app/login.html` not visited.
- Sceptic (mobile) never opened `/pricing.html` or the demo form.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator `00-landing`, `01-scrolled`, `02-pricing`, `03-demo-form` (blank), `04-features-404`, `05-about`, `06-privacy`; sceptic `00-landing`, `01-privacy`, `02-about`
