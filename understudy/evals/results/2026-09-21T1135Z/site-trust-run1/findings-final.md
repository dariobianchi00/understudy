# Nimbus Notes — trust findings — Run 2026-09-21 (fixture01)

## Method
- Framework: four visitor questions — is this real · what does it cost · who is behind it · what happens to my data
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED, not researched
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope: only what the personas could verify on the site. No external lookup, no compliance judgement.

---

## Findings

### 7cd332db3f02 — Cookie bar's no-tracking claim is contradicted by the privacy page and by the network log
- **Severity:** P0
- **So what:** The only hard claim the site makes about data is disproved on the same page load, and both visitors stopped trusting everything else after it.
- **Framework tags:** data-handling, consistency, claim-quality
- **Flow:** shape_v3
- **Locator:** /index.html#cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Bar reads "We use no tracking cookies on this site."; its only control is an OK button that removes the element, with no refuse option.
  - The landing-page load fetches `https://analytics.example-tracker.test/t.js` (38 KB, third-party) and POSTs `…/collect?uid=8f3a…` — a per-visitor id — in both persona sessions.
  - `/privacy.html` states "We use cookies and similar technologies."
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/network-full.txt:2-3` · `persona-evaluator/network-full.txt:4-5` · `crawl/html/1-index.html:3` · `crawl/html/1-index.html:37` · `persona-sceptic/session.log:10` · `persona-evaluator/session.log:27`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong."
- **Repro:**
  1. Open `http://localhost:8765/` in a fresh context with the network log recording.
  2. Read the black bar at the foot of the screen.
  3. Compare against the requests to `analytics.example-tracker.test` and against `/privacy.html`.
- **Fix:** Either remove the `analytics.example-tracker.test` script tag from `index.html` and keep the claim, or replace the bar with an accurate notice plus a working refuse option — and make `/privacy.html` say the same thing.

### b21c1b15bbbc — Privacy page names no partners, and the sceptic left the site over it
- **Severity:** P1
- **So what:** The visitor who came specifically to find out what happens to her notes ended the visit on this page, 70 seconds after the About page had won her over.
- **Framework tags:** data-handling, provenance
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Whole policy is four sentences: "We may share information with partners and service providers to improve your experience." No partner is named, no data category, no retention period.
  - Closes with "We may update this policy at any time." and "Questions? Use the demo form." — the only contact route is the seven-field sales form.
  - Sceptic reached it at 00:30, read it, and stopped the session at 02:40 with verdict "left; data handling unclear".
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/timeline.json` (`shape_v4.verdict`, `trust_down[0]`) · `crawl/html/5-privacy.html:10`
  > "That's not a privacy policy, that's a shrug."
- **Repro:**
  1. Open `http://localhost:8765/` on a 390×844 viewport.
  2. Scroll to the footer, tap Privacy.
  3. Try to establish who data is shared with.
- **Fix:** Name the processors on `/privacy.html` (analytics, hosting, email), state what each receives, and give an email address instead of routing privacy questions to the demo form.

### 50e2e95e0727 — Privacy page vagueness left the evaluator unsure about his data, but he stayed
- **Severity:** P2
- **So what:** The same page that ended one visit only dented the other — the evaluator read it, downgraded data trust to "unsure", and kept going.
- **Framework tags:** data-handling, consistency
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Read at 04:50, three minutes after the About page had raised his trust; he continued to the home page and the debrief rather than leaving.
  - Logged "Who are the partners you share data with?" as unanswered in `questions_unanswered`.
  - Q5 rates money "no" and data "unsure", attributing the change to this page plus the cookie bar.
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/timeline.json` (`shape_v3.questions_unanswered`) · `persona-evaluator/persona-debrief.md` Q5
  > "The About page made them feel real (a named founder, an address). The privacy page and the cookie bar contradicting each other undid that."
- **Repro:**
  1. Open `http://localhost:8765/`, browse pricing and about first.
  2. Open Privacy from the footer at the end of the visit.
  3. Note that the question "who are the partners" survives the page.
- **Fix:** Same edit as `b21c1b15bbbc`; the flip means this page decides whether a cautious visitor stays at all, so it should be treated as a conversion surface, not boilerplate.

### e48cb219ecf6 — Every pricing plan says Contact sales, and the reason given is unusable
- **Severity:** P1
- **So what:** The evaluator arrived to find out what it costs, spent 42 seconds failing, and said he would go and find a competitor with a price on the page.
- **Framework tags:** pricing-transparency, claim-quality
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three cards — Starter, Team, Enterprise — each with a "Contact sales" button and no number, no unit, no trial.
  - The page's explanation reads "Pricing depends on your workspace type and sync topology." — terms the visitor could not apply to himself.
  - `timeline.json` records `price_found: false`, `price_understood: false`, `gave_up: true` for the run's stated objective.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` (`objectives[0]`) · `crawl/html/3-pricing.html`
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `http://localhost:8765/` and click Pricing in the nav.
  2. Attempt to work out what the Starter plan costs.
- **Fix:** Put a number and a unit on Starter and Team ("£X per person per month"), keep Contact sales for Enterprise only, and delete the "workspace type and sync topology" sentence.

### 42ad5b757dbc — The only route to a price is a seven-field demo form with a required phone number
- **Severity:** P1
- **So what:** The visitor abandoned the form at 03:15 rather than give a phone number for a product he had not yet seen working.
- **Framework tags:** pricing-transparency, data-handling
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - "Contact sales" on every pricing card returns to `#demo` on the home page, not to a price.
  - Seven fields — first name, last name, work email, phone number, company, company size, what do you want to see — with phone marked `required`.
  - He counted them at 02:58 and backed out at 03:15 without submitting (`forms_submitted: 0`).
- **Evidence:** `persona-evaluator/session.log:20-23` · `crawl/html/1-index.html:29-35` · `persona-evaluator/timeline.json` (`shape_v3.forms_opened: 1`, `forms_submitted: 0`, `trust_down[3]`)
  > "Seven fields. Phone required. I haven't seen the product."
- **Repro:**
  1. Open `/pricing.html` and click any "Contact sales".
  2. Count the required fields on the Book a demo form.
- **Fix:** Drop phone, company and company size to optional, cut the form to email plus one question, and add a self-serve trial link beside it.

### db00a08c5d5a — All three testimonials are unattributed and the visitor said he did not believe them
- **Severity:** P2
- **So what:** The site's only proof section actively lowered trust rather than raising it, and it is where the evaluator lost interest.
- **Framework tags:** proof, claim-quality
- **Flow:** shape_v2
- **Locator:** /index.html#proof
- **Personas hit:** evaluator
- **Observed:**
  - Section headed "Loved by teams"; the three quotes are signed "— a happy customer", "— a user", "— anonymous".
  - No named person, company, role, number or case study anywhere on the site.
  - `point_of_lost_interest` is recorded at 01:25 — the moment he read them.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/findings-raw.json` (t 01:25) · `persona-evaluator/timeline.json` (`shape_v2.point_of_lost_interest`, `trust_down[0]`) · `crawl/html/1-index.html:24-26`
  > "Three quotes, nobody has a name. I don't believe these."
- **Repro:**
  1. Open `http://localhost:8765/` and scroll to "Loved by teams".
  2. Try to identify who said any of it.
- **Fix:** Replace the three quotes with one testimonial carrying a real name, role and company — or delete the section until you have one.

### 9fd96d8e8730 — Home page carries no company, data-location or FAQ information; all of it is on About
- **Severity:** P2
- **So what:** The only content that raised trust for either persona sits on a page a visitor has no reason to open, so most will never see it.
- **Framework tags:** provenance, proof
- **Flow:** shape_v3
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Both personas' `trust_up` lists contain only items from `/about.html`: named founder Priya Raman, Bristol address, company number 14482201, eight people, founded 2023.
  - The About FAQ answers works-offline, export, and "In the EU (Frankfurt) by default" — the sceptic's main question, answered on the wrong page.
  - The home page instead offers anonymous quotes and a newsletter box; the evaluator reached About only at 03:50.
- **Evidence:** `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:12` · both `timeline.json` (`shape_v3.trust_up`)
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Read `http://localhost:8765/` end to end.
  2. Look for who makes this, where they are, and where data is stored.
- **Fix:** Move the three About FAQ answers and the "made by Nimbus Notes Ltd, Bristol" line onto the home page, above the newsletter box.

### f6f0028cf93d — Zero-knowledge vault is the site's strongest claim and nothing on the site supports it
- **Severity:** P2
- **So what:** The page's main security promise was meaningless to both visitors, so it bought no trust and left the privacy page to answer for it.
- **Framework tags:** claim-quality, consistency
- **Flow:** shape_v1
- **Locator:** /index.html#hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Sub-headline: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - No page on the site explains the mechanism; Features, where it might live, returns 404.
  - The only page that discusses data says "We may share information with partners and service providers", which the personas could not square with the claim.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `crawl/html/1-index.html:11` · `crawl/html/5-privacy.html:10` · `persona-evaluator/findings-raw.json` (t 00:18) · `persona-evaluator/timeline.json` (`questions_unanswered`: "What is a sync graph?")
  > "'bi-directional sync graph', 'zero-knowledge vault' — I don't know what either means."
- **Repro:**
  1. Open `http://localhost:8765/` and read the sub-headline.
  2. Follow any link on the site that would explain "zero-knowledge vault".
- **Fix:** Either state in one plain sentence what is encrypted and who cannot read it, with a link to a page that shows it, or drop the phrase.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether the tracker fired before the cookie bar was dismissed — the script tag sits in `<head>` and the request is in the landing-page log, but no timestamped ordering against the OK tap was captured.
- Whether the demo form transmits anything on submit — neither persona submitted, correctly.
- Whether cookies were actually written to the browser — no cookie jar dump captured; the finding rests on the third-party tracker request and the privacy page's own wording.

## For other lenses
- "See it in action" does nothing when clicked, in both sessions (`persona-evaluator/session.log:12`, `persona-sceptic/session.log:13`) — conversion / technical.
- Features in the main nav returns 404 (`persona-evaluator/screenshots/04-features-404.png`) — technical.
- Hero image is 3.9 MB (`network-full.txt`) — technical.
- JSON-LD `offers.price` is malformed and empty (`crawl/html/1-index.html:3`) — seo.
- Neither persona could say who the product is for; "workspace type", "sync graph", "blocks" vs "cards" undefined — clarity.
- Newsletter box is larger and brighter than the primary CTA (`persona-evaluator/session.log:8`) — conversion.

## Coverage gaps
- `/features.html` never seen (404), so any proof or mechanism intended to live there was not assessed.
- No form submitted, by design — post-submission trust signals (confirmation, what happens next) unobserved.
- `persona-evaluator/screenshots/03-demo-form.png` renders blank; the field count rests on `session.log:21-22` and `crawl/html/1-index.html:29-35`.
- Sceptic never opened `/pricing.html`, so the price findings carry one persona only and a flip on pricing could not be observed.
- Logged-in app (`app/login.html`) never entered — out of scope for a visit.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/` (00-landing, 01-scrolled, 02-pricing, 03-demo-form, 04-features-404, 05-about, 06-privacy) · `persona-sceptic/screenshots/` (00-landing, 01-privacy, 02-about)
