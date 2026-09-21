# Nimbus Notes — conversion findings — Run 2026-09-08 (fixture01)

## Method
- Framework: hierarchy · availability · burden · match · dead ends · competing asks, scored against `conversion_goal`
- Goal supplied: **"Start a free trial without talking to sales"** — every judgement below is measured against it
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — **INFERRED**, not researched
- Scoring model: opus
- Forms were opened and abandoned by design; nothing here describes post-submission behaviour
- Field counts taken from the crawled DOM, not from the persona's estimate
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 97618a555295 — No self-serve trial route exists: every plan CTA is "Contact sales"
- **Severity:** P0
- **So what:** The goal the site was measured against cannot be attempted at all — there is no trial to start.
- **Framework tags:** availability, match, friction-of-the-wrong-kind
- **Flow:** shape_v3
- **Locator:** /pricing.html .price-card .cta
- **Personas hit:** evaluator
- **Observed:**
  - All three plan cards — Starter, Team, Enterprise — carry the identical CTA "Contact sales", each linking to `index.html#demo`.
  - The words "trial", "sign up", "get started" and "free" occur zero times across all five crawled pages.
  - The only account action in the global nav is "Log in"; there is no route to create an account.
- **Evidence:** `crawl/html/3-pricing.html` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17`
  > "Pricing page. Screenshot 02-pricing.png. Three cards: Starter, Team, Enterprise. Every one says \"Contact sales\". No numbers anywhere."
- **Repro:**
  1. Open `/pricing.html` logged out.
  2. Try to begin using the product without contacting a human — check the nav, the three plan cards and the footer.
  3. Every path terminates at the demo form on `/index.html#demo`.
- **Fix:** Add a "Start free trial" button to the header and to the Starter and Team cards, pointing at a self-serve signup; keep "Contact sales" on Enterprise only.

### 3184baf575d2 — Pricing page carries no numbers, and the visitor who came to price it gave up
- **Severity:** P1
- **So what:** The one visitor who came to find out what it costs left to look for a competitor that shows a price.
- **Framework tags:** availability, match, dead-ends
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - No figure, currency or unit appears anywhere on `/pricing.html`; the only explanation is "Pricing depends on your workspace type and sync topology."
  - `timeline.json` records `price_found: false`, `price_understood: false`, and the objective under test as `gave_up: true`.
  - The evaluator's pre-session note said what would make them leave: "no price, or a page that is all adjectives".
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:19` · `persona-evaluator/timeline.json`
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. Open `/pricing.html`.
  2. Attempt to work out the monthly cost for one person on Starter.
  3. No number is available on the page or anywhere it links to.
- **Fix:** Publish a per-person monthly price and the included limits on the Starter and Team cards, and delete the "workspace type and sync topology" line.

### afe40dfeaf19 — Demo form asks seven fields, five required including phone, before the product is shown
- **Severity:** P1
- **So what:** The site's single conversion point demands a phone call's worth of detail from a visitor who has not yet seen the product work, and this visitor backed out.
- **Framework tags:** burden, match, friction-of-the-wrong-kind
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - DOM shows seven inputs — first name, last name, work email, phone number, company, company size, "What do you want to see?" — of which five carry `required`, including `<input type="tel" required>`.
  - The evaluator opened it at 02:44 and backed out at 03:15 without submitting; `forms_opened: 1`, `forms_submitted: 0`.
  - This form is the destination of all three pricing CTAs and of the privacy page's "Questions?" line, so it is the only ask on the site.
- **Evidence:** `crawl/html/1-index.html` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:21`
  > "Seven. Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. From `/pricing.html`, click any "Contact sales".
  2. Land on the "Book a demo" section of `/index.html`.
  3. Count the inputs and the `required` attributes before anything has demonstrated the product.
- **Fix:** Cut the form to work email and company, make phone and company size optional, and put a self-serve trial button above it.

### a92665603fa3 — Newsletter box is the loudest ask on the page and outranks every product action
- **Severity:** P2
- **So what:** The brightest element on the home page collects a mailing-list address instead of moving the visitor toward the product.
- **Framework tags:** hierarchy, competing-asks
- **Flow:** shape_v2
- **Locator:** /index.html .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The newsletter block is a full-width solid purple panel with a filled "Subscribe" button, directly beneath a thin outlined "See it in action" link.
  - Both personas named it unprompted when asked what the page wanted them to do.
  - Ranked by visual weight the asks run: Subscribe, then "Log in", then "See it in action" — the reverse of the stated goal's order.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:11`
  > "There's a small outlined \"See it in action\" button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Load `/index.html` at 1440x900 and again at 390x844.
  2. Compare the fill, width and contrast of the "Subscribe" button with the hero CTA.
- **Fix:** Make "Start free trial" a solid filled button in the hero and demote the newsletter to one line in the footer.

### 36f5f5d14349 — About page wins the visitor over and then offers no next step
- **Severity:** P2
- **So what:** Both visitors reached peak willingness to act on a page with nothing to act on, and neither returned to a conversion point afterwards.
- **Framework tags:** dead-ends, availability, match
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` answers offline use, export and data location, and names the founder, address and company number; its `<main>` contains no button or link.
  - Both personas logged it as the page that raised their confidence — `trust_up` in each `timeline.json`.
  - The evaluator ended the session 1m55s later with "Nothing"; the sceptic left ten minutes of session time early.
- **Evidence:** `crawl/html/4-about.html` · `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24`
  > "That's the first thing on this site that felt like a real business."
- **Repro:**
  1. Open `/about.html`.
  2. Read to the end of the FAQ and look for a way to proceed.
  3. Only the global nav and footer links are available.
- **Fix:** Add a "Start free trial" button under the FAQ on `/about.html`, and move the three FAQ answers onto the home page.

### 8a76ffc692ed — Privacy page's only onward step is unlinked text pointing at the sales form
- **Severity:** P3
- **So what:** The visitor with the most doubt is offered no clickable way to resolve it, and the one offered is a sales form.
- **Framework tags:** dead-ends, match
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** sceptic, evaluator
- **Observed:**
  - The page's closing line is plain text — `<p>Questions? Use the demo form.</p>` — with no anchor, while the footer links beside it are underlined.
  - It routes a privacy question to a seven-field demo request rather than to a person or an address.
  - Both personas opened `/privacy.html`; the sceptic reached it 30 seconds into the visit.
- **Evidence:** `crawl/html/5-privacy.html` · `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:8`
  > "Tapped Privacy."
- **Repro:**
  1. Open `/privacy.html` on a 390px viewport.
  2. Try to click "Use the demo form".
- **Fix:** Replace that sentence on `/privacy.html` with a linked "Ask a privacy question" contact address, not the demo form.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- `persona-evaluator/screenshots/03-demo-form.png` renders as a blank white image, so the form's on-screen appearance at the moment of abandonment is unverified — finding afe40dfeaf19 rests on the crawled DOM, `01-scrolled.png` and the log instead.
- Whether the demo form's required-field validation blocks submission — no form was submitted, by design, so nothing is known about post-submit behaviour.
- Whether the mobile fold shows any product CTA below the hero — the sceptic reached 100% scroll in 15 seconds and no mid-page mobile screenshot was captured.
- Effect size of any fix here is untested: one visitor per device, no traffic data.

## For other lenses
- The hero CTA "See it in action" has `href="#"` and does nothing when clicked, on both devices — **bugs**.
- "Features" in the global nav returns a 404 page — **bugs**.
- Cookie bar says "We use no tracking cookies on this site" while `/privacy.html` says cookies are used and data shared with unnamed partners — **trust**.
- Anonymous testimonials — "a happy customer", "a user", "anonymous" — **trust**.
- "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology" undefined; neither persona could say what the product does — **clarity**.
- `/pricing.html` carries `<meta name="robots" content="noindex">` — **seo**.

## Coverage gaps
- `app/login.html` never opened — logged-out run.
- No form submitted on either device, so no conversion was completed end to end.
- The sceptic never visited `/pricing.html`, so the pricing findings rest on one persona.
- Tablet and any viewport between 390px and 1440px untested.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/` (7) · `persona-sceptic/screenshots/` (3)
