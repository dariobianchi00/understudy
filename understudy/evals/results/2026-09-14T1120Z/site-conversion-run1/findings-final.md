# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: hierarchy · availability · burden · match · dead ends · competing asks, scored against the stated goal "Start a free trial without talking to sales"
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (`persona_mode: generic`)
- Scoring model: opus
- Forms were opened and abandoned by design; nothing here judges post-submission behaviour
- Every finding cites an artifact; unsupported observations are listed at the end

---

## Findings

### 179e40ad9525 — No self-serve trial exists: the only site-wide actions are Log in and Contact sales
- **Severity:** P0
- **So what:** The action the business wants a visitor to take cannot be started from any page of the site.
- **Framework tags:** availability, match, friction-of-the-wrong-kind
- **Flow:** shape_3
- **Locator:** site-wide
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Every crawled page carries the same header: Home, Features, Pricing, About, and one filled button, `<a class="btn" href="app/login.html">Log in</a>` — no sign-up or trial link.
  - The only conversion destinations on the site are the newsletter box and the "Book a demo" form; all three pricing CTAs point at `index.html#demo`.
  - Both personas reached the end of their visit having taken no product action.
- **Evidence:** `crawl/html/1-index.html` · `crawl/html/3-pricing.html` · `crawl/html/4-about.html` · `persona-evaluator/timeline.json` (`forms_submitted: 0`) · `persona-evaluator/persona-debrief.md`
  > "Nothing. I came to find out what it costs and I couldn't. I'd search for an alternative with a price on the page."
- **Repro:**
  1. Open `/index.html` logged out; read the header and the hero.
  2. Visit `/pricing.html` and `/about.html`; read every button and link.
  3. Note that no control on any page begins a trial or creates an account.
- **Fix:** Add a "Start free trial" button as the filled primary in the header beside "Log in", and repeat it in the hero and on every pricing card.

### 14b293812aed — Pricing page shows no price: all three plans say only Contact sales
- **Severity:** P0
- **So what:** The evaluator came to find the cost, could not, and stopped evaluating at 02:30.
- **Framework tags:** availability, match, friction-of-the-wrong-kind
- **Flow:** shape_3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise cards carry a description and one outlined "Contact sales" button; no figure, no range, no "from £", no free tier.
  - The only pricing statement is "Pricing depends on your workspace type and sync topology."
  - `timeline.json` records `price_found: false`, `price_understood: false`, and the objective under test `gave_up: true`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17` · `persona-evaluator/session.log:19` · `persona-evaluator/timeline.json`
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. Click "Pricing" in the header.
  2. Read all three cards and the line beneath them.
  3. Try to work out what the Starter plan would cost one person.
- **Fix:** Publish a monthly per-seat number on Starter and Team, keep "Contact sales" for Enterprise only, and replace "workspace type and sync topology" with the two things that actually change the price.

### 45c8d3014cd5 — The newsletter band is the loudest call to action on the home page
- **Severity:** P1
- **So what:** The page's visual hierarchy sells an email list, not the product, so the strongest signal points away from the goal.
- **Framework tags:** hierarchy, competing asks
- **Flow:** shape_2
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The newsletter sits in a full-width solid purple band with a white "Subscribe" button; the product CTA "See it in action" is a small outlined ghost button.
  - Both personas named the imbalance unprompted, on desktop and on mobile.
  - The hero CTA is `<a class="cta" href="#">`, so from 00:40 the evaluator had no working product action above the demo form — a separate defect, noted for `bugs`.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:11` · `persona-sceptic/session.log:6`
  > "There's a small outlined 'See it in action' button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Load `/index.html` and rank the four asks by visual weight.
  2. Observe the order: newsletter band, "Log in", "Request demo", "See it in action".
- **Fix:** Make the primary trial CTA the only filled purple button above the fold, and demote the newsletter to a single-line link in the footer.

### d2aba8fd3d0a — Demo form asks seven fields with phone required before the product is shown
- **Severity:** P1
- **So what:** The only route out of Pricing demands a phone number from a visitor who has not yet seen the product work.
- **Framework tags:** burden, match
- **Flow:** shape_3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Counted from the markup: first name, last name, work email, phone number, company, company size, "What do you want to see?" — 7 fields, with `required` on the first five.
  - All three pricing CTAs route here, so this form is the site's answer to "what does it cost".
  - The evaluator opened it at 02:44 and abandoned it at 03:15 without typing (`forms_opened: 1`, `forms_submitted: 0`).
- **Evidence:** `crawl/html/1-index.html` (`<label>Phone number</label><input type="tel" required>`) · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:21`
  > "Seven fields. Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. From `/pricing.html`, click any "Contact sales".
  2. Land on `#demo` and count the inputs and the required markers.
- **Fix:** Cut the demo form to work email plus company, make the phone number optional, and point pricing cards at a trial sign-up instead of at this form.

### 743ebcff76bc — About page carries no next step at the moment the visitor is most convinced
- **Severity:** P2
- **So what:** The one page that earned both personas' confidence leaves them with nowhere to go but the browser back button.
- **Framework tags:** dead ends, availability
- **Flow:** shape_3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` contains a company paragraph and three FAQ answers, and no button or in-body link of any kind — only the header nav and the footer.
  - Both personas recorded their trust peaking here; `timeline.json` lists "About page: named founder, address, company number" under `trust_up` for both.
  - The evaluator asked why this content was not on the home page and then left the page without acting.
- **Evidence:** `crawl/html/4-about.html` · `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:11`
  > "OK — a real company, eight people, founded 2023 by Priya Raman, Bristol, a company number. That's the first thing on this site that felt like a real business."
- **Repro:**
  1. Open `/about.html` and read to the bottom of the FAQ.
  2. Look for any offered next step.
- **Fix:** Close the About page and each FAQ answer with a "Start free trial" button, and lift the three FAQ answers onto the home page.

### cab2c04aacad — Features 404 is a bare server error page with no link back into the site
- **Severity:** P2
- **So what:** A visitor who clicks the nav item for what the product does lands on a page with no header, no footer and no way onward.
- **Framework tags:** dead ends, availability
- **Flow:** shape_3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - The page rendered is the default server error body: "Error response", "Error code: 404", "Message: File not found." — no nav, no footer, no links.
  - "Features" is present in the header of all four real pages, so every page offers this dead end.
  - The broken link itself belongs to `bugs`; the finding here is that the destination offers zero onward action.
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `persona-evaluator/findings-raw.json`
  > "Clicked 'Features' in the nav. Got a 404 page: 'That page does not exist.'"
- **Repro:**
  1. Click "Features" in the header from any page.
  2. Observe the error page and look for any link.
- **Fix:** Serve a branded 404 carrying the site header, a line of apology and a "Start free trial" button — and restore or remove the Features nav item.

### c745eda85f90 — Newsletter asks for an email without saying what is sent or how often
- **Severity:** P3
- **So what:** The site's loudest ask offers the visitor nothing in return that they can name.
- **Framework tags:** burden, match
- **Flow:** shape_2
- **Locator:** /index.html .news input
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The whole ask is "Get the Nimbus newsletter" plus a placeholder `you@company.com` and a "Subscribe" button.
  - There is no label on the input, no frequency, no description of content, and no privacy line.
  - Neither persona subscribed; the sceptic noted only its size, not its offer.
- **Evidence:** `crawl/html/1-index.html` (`<div class="news">Get the Nimbus newsletter <input placeholder="you@company.com">`) · `persona-evaluator/screenshots/01-scrolled.png` · `persona-sceptic/session.log:6`
  > "There's a button 'See it in action' and under it a big purple newsletter box."
- **Repro:**
  1. Scroll `/index.html` to the purple band.
  2. Read everything offered in exchange for the email address.
- **Fix:** State what the newsletter contains and how often it arrives beside the field, or drop it and reuse the space for the trial CTA.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether mobile visitors can reach the demo form at all — the sceptic never scrolled the home page past the hero, so no mobile evidence of the form in view exists.
- Whether the "Log in" button leads to a working sign-in — behind the auth wall, never scored.
- Whether the required phone number deters submission in aggregate — one visitor, no traffic data; the size of any fix here is untested.

## For other lenses
- Hero CTA "See it in action" is `href="#"` and does nothing when clicked twice (`persona-evaluator/session.log:12`) — `bugs`.
- "Features" in the nav 404s on every page — `bugs`.
- "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology" were all undefined to the visitor — `clarity`.
- Cookie bar says "We use no tracking cookies on this site" while `/privacy.html` describes cookies and unnamed partners — `trust`.
- Testimonials signed "a happy customer", "a user", "anonymous" — `trust`.
- `/pricing.html` carries `<meta name="robots" content="noindex">` — `seo`.

## Coverage gaps
- `persona-evaluator/screenshots/03-demo-form.png` rendered blank white; field counts in this report come from the page markup and the session log, not that image.
- Mobile (iPhone 13) was never taken to `/pricing.html` or the demo form — no mobile evidence on the two P0 surfaces.
- No persona tested the newsletter or demo form submission, by design.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/`, `persona-sceptic/screenshots/`
