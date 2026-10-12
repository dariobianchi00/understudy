# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: next-step availability, CTA hierarchy, ask-vs-readiness, dead ends — scored against the stated conversion goal
- Goal: "Start a free trial without talking to sales"
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 9e6a01656035 — No free-trial path exists; every route to sign-up ends at sales or a demo form
- **Severity:** P0
- **So what:** The stated goal cannot be reached by anyone; the site only offers "Contact sales", "Request demo", a newsletter and "Log in".
- **Framework tags:** Availability, Friction of the wrong kind, Match
- **Flow:** shape_v3
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Crawl of all 5 pages finds no "trial", "sign up", "get started" or "free" link or button.
  - Hero's only action, "See it in action", is `href="#"`; both personas clicked it and nothing happened.
  - All three pricing plans link to `index.html#demo` ("Book a demo"), i.e. a sales conversation.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `crawl/html/1-index.html:12` · `crawl/html/3-pricing.html:12-14`
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page." (evaluator, debrief Q3)
- **Repro:**
  1. Open `/index.html`; look for a trial or sign-up action at any scroll depth.
  2. Open `/pricing.html`; every plan's button reads "Contact sales" and lands on the demo form.
- **Fix:** Add a filled "Start free trial" button to the hero, header and each pricing card, linking to self-serve sign-up.

### 355038c9eae8 — Pricing page shows no prices and sends all three plans, including the individual tier, to sales
- **Severity:** P1
- **So what:** The evaluator came to learn the cost, could not, and said she would search for an alternative instead.
- **Framework tags:** Friction of the wrong kind, Match, Burden
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three cards — Starter "For individuals.", Team "For growing teams.", Enterprise — no figure on any.
  - Each button reads "Contact sales"; the only pricing copy is "Pricing depends on your workspace type and sync topology."
  - Objective "find out what it costs without giving an email": attempted 01:48–02:30, `gave_up: true`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` (`price_found: false`, `objectives[0].gave_up: true`)
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. Click "Pricing" in the nav.
  2. Look for any price on the Starter, Team or Enterprise card.
- **Fix:** Publish a monthly price on Starter and Team, and replace their "Contact sales" with "Start free trial"; keep sales for Enterprise only.

### ca96595ed66d — Demo form demands five required fields, including phone, before any product is shown
- **Severity:** P1
- **So what:** The evaluator opened the only conversion form, saw a phone number required before seeing the product, and backed out.
- **Framework tags:** Burden, Match
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Counted from markup: 7 controls — First name, Last name, Work email, Phone number, Company (all `required`), Company size (select), "What do you want to see?" (optional).
  - Reached from "Contact sales" on the Starter "For individuals." card — a demo ask for a single user.
  - Form was opened, not submitted (`forms_opened: 1`, `forms_submitted: 0`).
- **Evidence:** `crawl/html/1-index.html:28-35` · `persona-evaluator/screenshots/01-scrolled.png` (form heading and first field) · `persona-evaluator/session.log:20-22` · `persona-evaluator/timeline.json`
  > "Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. On `/pricing.html`, click "Contact sales" on Starter.
  2. Land on "Book a demo"; inspect required fields.
- **Fix:** Drop the phone field and make Company optional; better, route individual and team plans to trial sign-up, not this form.

### 23f2c215e18b — Newsletter box outweighs every goal-related action on the home page
- **Severity:** P2
- **So what:** The loudest ask on the page is the lowest-intent one; the evaluator noticed and read past it, but the hierarchy points away from the goal.
- **Framework tags:** Hierarchy, Competing asks
- **Flow:** shape_v2
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "Get the Nimbus newsletter" is a full-width solid purple block; "See it in action" is a small outlined button.
  - The header's only filled button is "Log in", which serves existing users, not new ones.
  - No action stays pinned as the visitor scrolls.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6`
  > "The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/index.html` at 1440×900.
  2. Compare visual weight of "See it in action", "Log in" and the newsletter block.
- **Fix:** Make the trial button the only filled, high-contrast element above the fold; demote the newsletter to a footer text field.

### 9e7d01e6ec8e — About page, the most persuasive page reached, offers no onward action
- **Severity:** P2
- **So what:** The evaluator's trust peaked on About and the page gave her nothing to do next, so the moment was lost.
- **Framework tags:** Dead ends, Availability
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Body holds the company facts and three FAQs; no button or link in `<main>`.
  - Only exits are the shared nav, "Log in" and footer links.
  - Evaluator called it "the first thing on this site that felt like a real business".
- **Evidence:** `crawl/html/4-about.html:8-19` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12`
  > "Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/about.html`.
  2. Scroll to the end of the FAQ; look for a next step.
- **Fix:** Add a "Start free trial" button after the FAQ on `/about.html`.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Required-field markers on the demo form — `persona-evaluator/screenshots/03-demo-form.png` is a blank white frame; field count comes from markup, visual markers unverifiable.
- Mobile CTA reachability — sceptic never scrolled the home page beyond the hero (`sections_seen: 1`); no mobile view of the form or pricing.

## For other lenses
- "See it in action" (`href="#"`) does nothing on click — bugs.
- "Features" nav link returns a 404 — bugs.
- Cookie bar "We use no tracking cookies on this site." contradicts privacy page and a third-party analytics script — trust.
- Anonymous testimonials ("— a happy customer", "— a user", "— anonymous") — trust.
- Headline names neither product type nor audience; "bi-directional sync graph" jargon — clarity.
- Broken `"price": }` in JSON-LD on the home page — seo.
- Demo-form screenshot captured blank — capture quality.

## Coverage gaps
- No form submitted, by design; nothing scored after submission.
- `app/login.html` not opened.
- Sceptic (mobile) never reached pricing or the demo form.
- Persona mode generic: both personas inferred.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06, sceptic 00–02; 03-demo-form.png blank
