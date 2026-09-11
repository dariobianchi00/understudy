# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: hierarchy · availability · burden · match · dead ends · competing asks, scored against the stated conversion goal
- Conversion goal, verbatim from `manifest.json`: **"Start a free trial without talking to sales"**
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — **INFERRED** (`persona_mode: generic`); every judgement below rests on personas the capture invented
- Scoring model: opus
- Field counts taken from the DOM, not from the persona's description
- Every finding cites an artifact; unsupported observations are listed at the end

---

## Findings

### 6114dbce2d89 — No self-serve trial exists — every route to the product ends at a sales form
- **Severity:** P0
- **So what:** The action the business says it wants is not offered anywhere, so no visitor can take it however convinced they are.
- **Framework tags:** availability, match, friction-of-the-wrong-kind
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Case-insensitive search of all five crawled pages for "free trial", "sign up", "try it", "trial", "get started", "create account", "register" returns zero matches.
  - All three plan cards link to the same target: `<a class="cta" href="index.html#demo">Contact sales</a>` — including Starter, described as "For individuals."
  - The only filled, high-contrast nav button is "Log in", which serves existing accounts, not new ones.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `crawl/html/3-pricing.html:12-14` · `persona-evaluator/session.log:17` · `persona-evaluator/timeline.json` (`shape_v4.verdict: "would not proceed; no price"`)
  > "Three cards: Starter, Team, Enterprise. Every one says 'Contact sales'. No numbers anywhere."
- **Repro:**
  1. Open `/` logged out.
  2. Look for any way to start using the product without contacting a person — check the hero, the nav, the footer and `/pricing.html`.
  3. Observe that the only self-serve control is "Log in", and every plan CTA reads "Contact sales".
- **Fix:** Add a "Start free trial" button as the primary CTA in the hero and on the Starter and Team pricing cards, pointing at a self-serve signup, not `index.html#demo`.

### 6c73d3f78df0 — Pricing lists three plans and no price, so a visitor cannot work out what they would pay
- **Severity:** P0
- **So what:** The evaluator's reason for the whole visit went unanswered, and she left to find a competitor that publishes a number.
- **Framework tags:** availability, match, friction-of-the-wrong-kind
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - The page shows three cards — Starter, Team, Enterprise — with no currency figure, no "from", and no unit anywhere on the page.
  - The only explanation given is "Pricing depends on your workspace type and sync topology."
  - The objective under test — "A visitor can find out what it costs without giving an email" — failed: `price_found: false`, `price_understood: false`, `gave_up: true`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `crawl/html/3-pricing.html:16` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` (`objectives[0].gave_up: true`)
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/` and click "Pricing" in the nav.
  2. Read all three cards and the footnote.
  3. Observe no currency amount appears on the page or anywhere within three clicks of the landing page.
- **Fix:** Put a monthly per-seat price in currency on the Starter and Team cards, and keep "Contact sales" only on Enterprise.

### 85814751339f — The site's only form asks seven fields and requires a phone number before showing the product
- **Severity:** P1
- **So what:** The ask is sized for a qualified sales lead, but it is the first thing a visitor meets who has not yet seen the product work.
- **Framework tags:** burden, match
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Counted from the DOM: 7 fields — First name, Last name, Work email, Phone number, Company, Company size (select), "What do you want to see?". Five carry `required`, including `<label>Phone number</label><input type="tel" required>`.
  - The form is reached by clicking "Contact sales" on any plan, i.e. it is the destination of every pricing decision.
  - The evaluator opened it and backed out without submitting: `forms_opened: 1`, `forms_submitted: 0`.
- **Evidence:** `crawl/html/1-index.html:29-35` · `persona-evaluator/session.log:20-22` · `persona-evaluator/timeline.json` (`shape_v3.forms_opened: 1`, `forms_submitted: 0`) · `persona-evaluator/findings-raw.json` (t=02:58)
  > "Seven fields. Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html` and click any "Contact sales".
  2. Land on `/index.html#demo` and count the fields and their required markers.
  3. Observe phone number is required before any product view has been offered.
- **Fix:** Cut the demo form to work email plus company, make phone optional, and label what the visitor gets back and when.

### 126a9b43ec51 — Above the fold the loudest button is Log in, and the newsletter box outweighs the product CTA
- **Severity:** P1
- **So what:** Visual priority goes to returning users and an email list, so a first-time visitor's strongest cue is not the action the business wants.
- **Framework tags:** hierarchy, competing asks
- **Flow:** shape_v2
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - On desktop the only filled, saturated button above the fold is "Log in" in the header; the hero CTA "See it in action" is a small outlined link sitting below the hero image, at the bottom edge of the 900px fold.
  - Immediately below the hero sits `<div class="news">Get the Nimbus newsletter <input placeholder="you@company.com"> <button>Subscribe</button></div>` — one field, no statement of what is sent or how often.
  - Both personas named the newsletter box as the visually dominant element on first read.
- **Evidence:** `measure/screenshots/index-desktop.png` · `crawl/html/1-index.html:12-15` · `persona-evaluator/session.log:11` · `persona-sceptic/session.log:6` · `persona-evaluator/findings-raw.json` (t=01:10)
  > "The newsletter box is bigger and brighter than the button that shows the product."
- **Repro:**
  1. Open `/` at 1440x900, logged out, without scrolling.
  2. Rank the visible controls by size and fill contrast.
  3. Observe "Log in" ranks first, the newsletter box second, and the hero CTA last.
- **Fix:** Make the hero CTA a filled primary button placed directly under the subhead, demote "Log in" to a text link, and move the newsletter box to the footer.

### 1a36652546b7 — About and Privacy are dead ends — the pages that built confidence offer no next step
- **Severity:** P2
- **So what:** The evaluator hit the one page that made the company feel real and had nothing to click, so the confidence it earned was spent on nothing.
- **Framework tags:** dead ends, availability
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` carries the named founder, the address, the company number and three FAQ answers, and contains no call to action in `<main>` — only the header nav and the footer links.
  - `/privacy.html` offers one onward step and it points back at the sales form: "Questions? Use the demo form."
  - Both personas reached About, recorded it as the moment trust rose, and then stopped: the sceptic ended the session two pages later, the evaluator returned to the home page and left.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `crawl/html/4-about.html:9-19` · `crawl/html/5-privacy.html:11` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-14`
  > "OK — a real company, eight people, founded 2023 by Priya Raman, Bristol, a company number. That's the first thing on this site that felt like a real business."
- **Repro:**
  1. Open `/about.html`.
  2. Read to the bottom of the FAQ.
  3. Observe there is no action offered below the content; the only onward links are nav and footer.
- **Fix:** Add a closing CTA block to `/about.html` and `/privacy.html` — one line plus a "Start free trial" button — and move the three FAQ answers onto the home page.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- What the demo form does on submit — confirmation, timing, or what the visitor gets back. The form was opened and backed out of by design (`forms_submitted: 0`); nothing was observed and nothing is claimed.
- Whether a trial or a self-serve plan exists behind `app/login.html` — auth wall, never scored.
- What the newsletter "Subscribe" button does, or what it sends — never clicked by either persona.
- Whether the missing price costs more on mobile than desktop — the sceptic never looked for a price (`objectives[0].attempted: false`).

## For other lenses
- The hero CTA is `<a class="cta" href="#">See it in action</a>` and does nothing when clicked; both personas tried it — **bugs**.
- "Features" in the primary nav returns a 404, "That page does not exist." — **bugs**.
- The cookie bar says "We use no tracking cookies on this site." while `/privacy.html` says "We use cookies and similar technologies." — **trust**.
- Three testimonials attributed to "a happy customer", "a user", "anonymous" — **trust**.
- "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology" were all undefined to both personas — **clarity**.
- `/pricing.html` carries `<meta name="robots" content="noindex">` — **seo**.
- The `SoftwareApplication` JSON-LD is malformed at the `offers.price` key and does not parse — **seo / aeo**.

## Coverage gaps
- `persona-evaluator/screenshots/03-demo-form.png` and `01-scrolled.png` rendered as blank white images; field counts and section order were taken from `crawl/html/1-index.html` instead.
- No mobile capture of the pricing page or the demo form — the sceptic never visited either, so form burden on a 390px viewport is unmeasured.
- `/features.html` was never seen as a working page, so any CTAs intended to live there are untested.
- Neither persona scrolled the home page slowly enough to record where the demo form first becomes visible; scroll-depth-to-CTA is unmeasured.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00-06` · `persona-sceptic/screenshots/00-02` · `measure/screenshots/`
