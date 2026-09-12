# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: conversion — hierarchy, availability, burden, match, dead ends, wrong-kind friction, competing asks; scored against the stated goal
- Goal under test (manifest `conversion_goal`): "Start a free trial without talking to sales"
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Outcome measure: debrief Q3 — evaluator "Nothing"; sceptic "Leave"
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Note on `persona-evaluator/screenshots/03-demo-form.png`: the file is blank white. Field counts below come from the captured DOM (`crawl/html/1-index.html:29-34`), not the persona's estimate.

---

## Findings

### 3bd545a96666 — No free-trial path exists on any page; the only action on every plan is "Contact sales"
- **Severity:** P0
- **So what:** The goal is a self-serve trial; the site offers none, so no visitor can do what the business wants without talking to sales.
- **Framework tags:** availability, match, wrong-kind friction
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Pricing page: three plans (Starter, Team, Enterprise), each with one button, "Contact sales", all linking to `index.html#demo`.
  - No "trial", "sign up", "get started", "free" or "register" string on any of the 5 captured pages.
  - Only other actions on the site: "Log in" (existing users), newsletter, "Book a demo".
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17` · `crawl/html/3-pricing.html:12` (DOM: `<a class="cta" href="index.html#demo">Contact sales</a>` ×3) · `persona-evaluator/persona-debrief.md` Q3
  > "Three cards: Starter, Team, Enterprise. Every one says 'Contact sales'. No numbers anywhere."
- **Repro:**
  1. Open `/pricing.html`.
  2. Look for any action other than "Contact sales" on the three plan cards — none.
  3. Search page source of all five pages for "trial" — no match.
- **Fix:** Add a "Start free trial" button as the primary action on the Starter and Team cards and in the hero, linking to a self-serve signup; keep "Contact sales" for Enterprise only.

### 7291764370cf — Hero button "See it in action" links to "#" and does nothing when clicked
- **Severity:** P1
- **So what:** The only next step above the fold is inert on desktop and mobile; both personas tried it and got nothing, and the sceptic ended the visit on it.
- **Framework tags:** availability, hierarchy
- **Flow:** shape_v1
- **Locator:** /index.html a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator clicked twice at 00:40; sceptic tapped at 02:20; page did not move or change either time.
  - DOM: `<a class="cta" href="#">See it in action</a>` — no target.
  - No other call to action is visible in the fold on either viewport.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `crawl/html/1-index.html:12`
  > "Clicked 'See it in action'. Nothing happened. The page didn't move. Clicked again. Still nothing."
- **Repro:**
  1. Open `/index.html` on any viewport.
  2. Click "See it in action" under the hero image.
  3. Observe no navigation, scroll or modal.
- **Fix:** Point "See it in action" at a real destination (a product demo section or the trial signup), and make it the filled primary button, not the outlined one.

### b2397256c9ca — No plan shows a price, so the evaluator could not decide and left to find an alternative
- **Severity:** P1
- **So what:** The visitor who came to check cost could not; without a number they cannot take the offer to their team, and said they would search elsewhere.
- **Framework tags:** availability, match
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three plan cards carry a name, one line of copy and "Contact sales"; no figure, currency or period on any.
  - Footnote reads "Pricing depends on your workspace type and sync topology." — evaluator: "I don't know what my workspace type is."
  - `timeline.json` shape_v3: `price_found: false`, `price_understood: false`; objective attempt `gave_up: true` at 02:30.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/session.log:19` · `persona-evaluator/timeline.json` · `persona-evaluator/persona-debrief.md` Q3
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."
- **Repro:**
  1. Open `/pricing.html`.
  2. Look for a price on Starter, Team or Enterprise — none.
- **Fix:** Put a monthly price per seat on the Starter and Team cards, and replace "workspace type and sync topology" with plain-language plan differences; Enterprise may stay "Contact sales".

### 387eab4bf3b5 — "Contact sales" lands on a 7-field demo form requiring a phone number before any product is shown
- **Severity:** P1
- **So what:** The one route to a price or a look at the product demands identity, employer and phone from a visitor who has seen nothing yet; the evaluator backed out.
- **Framework tags:** burden, match, wrong-kind friction
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - 7 fields counted in the DOM: First name, Last name, Work email, Phone number, Company, Company size, "What do you want to see?".
  - 5 carry `required`: First name, Last name, Work email, Phone number, Company. Company size and the free-text field do not.
  - Form is headed "Book a demo"; nothing on it says what the visitor gets or when.
- **Evidence:** `crawl/html/1-index.html:29` (DOM: `<label>Phone number</label><input type="tel" required>`) · `persona-evaluator/session.log:20` · `persona-evaluator/session.log:21` · `persona-evaluator/session.log:22` · `persona-evaluator/screenshots/01-scrolled.png` (form head visible; `03-demo-form.png` captured blank)
  > "Seven. Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html`, click any "Contact sales".
  2. Land on `/index.html#demo`; count fields and `required` markers.
- **Fix:** For a self-serve trial, replace this form with email-only signup; if a demo form stays, cut it to work email + company size and drop the phone requirement.

### 729ddd5ac711 — Newsletter box outweighs the primary call to action in size and colour
- **Severity:** P2
- **So what:** The loudest element on the landing page asks for an email list signup, not the trial; both personas' eyes went to it before any product action.
- **Framework tags:** hierarchy, competing asks
- **Flow:** shape_v2
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is a small outlined button; "Get the Nimbus newsletter" is a full-width solid purple block with a white button directly below it.
  - Evaluator at 00:11: newsletter box "much bigger and brighter than that button"; sceptic at 00:08: "a big purple newsletter box".
  - The newsletter block sits immediately under the hero, before "How it works".
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6` · `persona-evaluator/findings-raw.json` (t 01:10)
  > "The newsletter box is bigger and brighter than the button that shows the product."
- **Repro:**
  1. Open `/index.html` at 1440×900; scroll one screen.
  2. Compare the visual weight of "Subscribe" vs "See it in action".
- **Fix:** Move the newsletter block to the footer as a plain single-line field and give the primary trial button the solid purple treatment.

### 1cbb9374354b — "Features" in the nav dead-ends on a bare 404 with no onward link
- **Severity:** P2
- **So what:** A visitor trying to learn what the product does hits a server error page with no nav, no link back and nothing to do next.
- **Framework tags:** dead ends, availability
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - Nav item "Features" on every page links to `features.html`; crawl recorded status 404.
  - Error page shows only "Error response / Error code: 404 / File not found." — no header, footer or link.
  - Evaluator recovered only by using the browser to reach "About".
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `crawl/index.json:12` (status 404) · `crawl/html/1-index.html:6` (DOM: `<a href="features.html">Features</a>`)
  > "Clicked 'Features' in the nav. Got a 404 page: 'That page does not exist.'"
- **Repro:**
  1. Click "Features" in the top nav on any page.
- **Fix:** Publish `/features.html` or remove the nav item; until then, serve a branded 404 with the site nav and a "Start free trial" link.

### 172fb10c349e — About page, where trust peaked for both personas, offers no next step
- **Severity:** P2
- **So what:** Both personas said this page made the company feel real; neither could act on that because the page has no call to action.
- **Framework tags:** availability, dead ends
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Page content: company facts, three FAQ answers, footer links (Privacy, About, Pricing); no button or trial link.
  - Evaluator 03:50: "the first thing on this site that felt like a real business"; sceptic 01:30: "That is a real company."
  - `timeline.json` `trust_up` for both personas names the About page; the visit still ended with no action.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24` · `persona-sceptic/session.log:11` · `crawl/html/4-about.html` (DOM: no `class="cta"` element)
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/about.html`; scroll to the end.
  2. Look for any action beyond the footer links — none.
- **Fix:** Add a "Start free trial" button under the FAQ on `/about.html`, and lift the three FAQ answers onto the home page above "Book a demo".

### f6b7aad2bfdf — Privacy page says "Questions? Use the demo form." with no link to the form
- **Severity:** P3
- **So what:** The only onward pointer on the page is plain text; a visitor with a question has to find the form themselves.
- **Framework tags:** availability, dead ends
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** sceptic, evaluator
- **Observed:**
  - Last line of body copy: "Questions? Use the demo form." rendered as unlinked text.
  - No other action on the page besides footer links.
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-sceptic/session.log:8`
- **Repro:**
  1. Open `/privacy.html`; read to the end.
  2. Try to click "Use the demo form." — not a link.
- **Fix:** Link "demo form" to `/index.html#demo`, or better, replace it with a contact email address.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The demo form may give no confirmation or error state on submit — persona backed out by design; nothing after submission was observed.
- The "Log in" button may lead to an unavailable `app/login.html` — neither persona clicked it; no screenshot or status recorded.

## For other lenses
- Hero copy "bi-directional sync graph with a zero-knowledge vault" undefined for both personas; `time_to_comprehension_seconds: null` for both — clarity.
- Cookie bar "We use no tracking cookies on this site." contradicts privacy page and a third-party `analytics.example-tracker.test/t.js` script in the head — trust, technical.
- Three testimonials attributed to "a happy customer", "a user", "anonymous" — trust.
- `features.html` returns 404 from the nav; `<a class="cta" href="#">` in the hero — bugs, seo.
- Privacy page names no partners; "We may update this policy at any time." — trust.

## Coverage gaps
- Sceptic never opened Pricing or the demo form (`objectives[0].attempted: false`), so form burden and price absence are single-persona findings.
- `persona-evaluator/screenshots/03-demo-form.png` is blank; the form was read from the DOM only.
- "Log in" (`app/login.html`) never opened by either persona.
- No tablet viewport; no returning-visitor state.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator: 00-landing, 01-scrolled, 02-pricing, 03-demo-form (blank), 04-features-404, 05-about, 06-privacy · sceptic: 00-landing, 01-privacy, 02-about
