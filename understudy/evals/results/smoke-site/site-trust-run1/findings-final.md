# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions — is this real · what does it cost · who is behind it · what happens to my data — scored from `trust_up`/`trust_down`, the objections raised, and debrief Q5
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Not a compliance review; nothing here states whether the privacy policy is legally sufficient
- Everything below is what the site does or does not say; nothing is sourced outside the capture

---

## Findings

### 913559c419c1 — Cookie bar promises no tracking cookies; a third-party tracker fires on load and the privacy page says otherwise
- **Severity:** P0
- **So what:** the one explicit data promise the site makes is contradicted by its own network traffic and its own policy; both visitors caught the contradiction and named it as the reason they stopped trusting the site.
- **Framework tags:** Q4 data handling · consistency · claim quality
- **Flow:** shape_v3
- **Locator:** /index.html cookie-bar
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Bar on first load reads "We use no tracking cookies on this site." with a single "OK" button, on desktop and mobile.
  - Before the bar is dismissed the page has already loaded `analytics.example-tracker.test/t.js` (38 KB) and POSTed to `/collect?uid=…` with a per-visitor uid — in both personas' logs.
  - Privacy page reads "We use cookies and similar technologies." and "We may share information with partners and service providers."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-sceptic/screenshots/01-privacy.png` · `persona-evaluator/network-full.txt:4-5` · `persona-sceptic/network-full.txt:2-3` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong."
  > "The About page made them real — a founder with a name, an address, a company number, and my data in Frankfurt. The privacy page took it back."
- **Repro:**
  1. Open `/` in a fresh context; note the bar text "We use no tracking cookies on this site."
  2. Open the network panel: `GET analytics.example-tracker.test/t.js` and `POST …/collect?uid=` fire before any consent.
  3. Click footer "Privacy"; read "We use cookies and similar technologies."
- **Fix:** Either remove the `analytics.example-tracker.test` script from first load, or rewrite the bar and the privacy page to state exactly which cookies are set and who receives the data — the three surfaces must say the same thing.

### 4e25dacaac44 — Pricing page shows no price on any plan and explains it with jargon the visitor cannot answer
- **Severity:** P1
- **So what:** the evaluator came to check the price, could not, answered "Money, no" to Q5, and left to search for a competitor with a price on the page.
- **Framework tags:** Q2 pricing transparency · claim quality
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three cards — "Starter", "Team", "Enterprise" — each with a "Contact sales" button; no number, currency, period or trial anywhere on the page.
  - The only explanation is "Pricing depends on your workspace type and sync topology."; neither term is defined on this page or any page visited.
  - "Contact sales" routes to the seven-field demo form on the home page; the evaluator backed out at 03:15.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-20` · `persona-evaluator/timeline.json` (`price_found: false`, `price_understood: false`, objective `gave_up: true`)
  > "Pricing page. Three cards: Starter, Team, Enterprise. Every one says 'Contact sales'. No numbers anywhere."
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/`; click "Pricing" in the nav.
  2. Read the three cards; look for any figure.
  3. Click any "Contact sales"; land on the `#demo` form.
- **Fix:** Put a starting price (or "free up to N notes") on the Starter card and a per-seat price on Team; if Enterprise must stay "Contact sales", say in one line what drives the quote instead of "workspace type and sync topology".

### 973a5ede98c3 — Privacy page names no partners, no data categories and no cookie behaviour
- **Severity:** P1
- **So what:** the sceptic's entire visit was "what happens to my notes"; the privacy page answered with four generic sentences and "Use the demo form", and he left at 02:40.
- **Framework tags:** Q4 data handling · claim quality
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Whole policy is one paragraph: "We collect information you provide and information about how you use the service. We may share information with partners and service providers to improve your experience. We use cookies and similar technologies. We may update this policy at any time."
  - No partner or service provider is named, no data category listed, no retention or location stated; the only contact route is "Questions? Use the demo form."
  - Both personas logged "Who are the partners you share data with?" in `questions_unanswered`.
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-sceptic/session.log:9` · `persona-evaluator/session.log:26` · `persona-sceptic/timeline.json` (`trust_down`: "Privacy page names no partners")
  > "'We may share information with partners and service providers.' With whom? Not said. 'We may update this policy at any time.' That's not a privacy policy, that's a shrug."
- **Repro:**
  1. Open `/`; tap footer "Privacy".
  2. Read the page; look for any named third party or data category.
- **Fix:** Rewrite `/privacy.html` as a list: what is collected, the named processors it goes to (starting with the analytics vendor), where it is stored, how long, and a contact address that is not the sales form.

### 028e5826ff78 — Every testimonial is anonymous, so the persona disbelieved all three
- **Severity:** P2
- **So what:** the "Loved by teams" section is the site's only customer proof, and the one visitor who reached it rejected it outright and lost interest at that point.
- **Framework tags:** Q1 proof · claim quality
- **Flow:** shape_v2
- **Locator:** /index.html testimonials
- **Personas hit:** evaluator
- **Observed:**
  - Section headed "Loved by teams" carries three quotes attributed "— a happy customer", "— a user", "— anonymous".
  - No customer name, company, logo, or number appears anywhere on the home page.
  - `timeline.json` marks `point_of_lost_interest: "01:25"`, the moment the testimonials were read.
- **Evidence:** `persona-evaluator/session.log:14` · `persona-evaluator/findings-raw.json` (t 01:25) · `persona-evaluator/timeline.json` (`trust_down`: "Anonymous testimonials")
  > "'Loved by teams' — three quotes. '— a happy customer', '— a user', '— anonymous'. Nobody has a name. I don't believe these."
- **Repro:**
  1. Open `/`; scroll to "Loved by teams".
  2. Read the attributions under the three quotes.
- **Fix:** Replace the three quotes with one or two attributed to a named person at a named team, with a number ("cut our meeting notes from 40 min to 5") — or remove the section until one exists.

### d73c7ae5cb95 — Demo form requires a phone number before the visitor has seen the product
- **Severity:** P2
- **So what:** the only route past "Contact sales" asks for seven fields including a mandatory phone number from someone who has not yet seen a screenshot; the evaluator listed it as a reason not to trust the site and backed out.
- **Framework tags:** Q1 proof · Q2 pricing transparency
- **Flow:** shape_v3
- **Locator:** /index.html demo-form
- **Personas hit:** evaluator
- **Observed:**
  - Fields: first name, last name, work email, phone number, company, company size, what do you want to see — seven; phone marked required.
  - Reached from every "Contact sales" button on `/pricing.html`.
  - Evaluator backed out at 03:15 without submitting; `forms_opened: 1`, `forms_submitted: 0`.
- **Evidence:** `persona-evaluator/session.log:20-22` · `persona-evaluator/findings-raw.json` (t 02:58) · `persona-evaluator/timeline.json` (`trust_down`: "Phone number required for a demo")
  > "Seven. Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html`; click "Contact sales" on any card.
  2. Count the fields on the `#demo` form; note the required marker on phone.
- **Fix:** Make phone optional and cut the form to email plus one free-text field; show a product screenshot or short clip beside the form so the visitor sees something before giving anything.

### b6aa5f6d8b61 — The site's only concrete data answers sit on About, not on Privacy
- **Severity:** P2
- **So what:** the answers that actually raised trust — data in Frankfurt, export on every plan, offline-first — are on a page neither persona went to for them; a visitor who reads Privacy and leaves never sees them.
- **Framework tags:** Q4 data handling · Q3 provenance · consistency
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Where is my data stored? In the EU (Frankfurt) by default." · "Can I export my notes? Yes. Settings → Export produces a folder of Markdown files at any time, on every plan." · "Does Nimbus Notes work offline? Yes."
  - Privacy page states no location, no export right, no retention; it points to the demo form.
  - Both personas found About only after Privacy had already lowered trust (evaluator 04:20 after 03:50; sceptic 01:50 after 00:45).
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-sceptic/session.log:12` · `persona-evaluator/session.log:25`
  > "'Where is my data stored? In the EU (Frankfurt) by default.' That's the answer I wanted and it's on the About page, not the Privacy page."
  > "Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/privacy.html`; note no storage location or export statement.
  2. Open `/about.html`; read the three FAQ answers.
- **Fix:** Copy the three FAQ answers into `/privacy.html` under "Where your notes live" and add the Frankfurt line to the home page near the "zero-knowledge vault" claim.

### 596a6728313f — No visible product anywhere: the only demo button does nothing, so 'remembers everything' stays a claim
- **Severity:** P2
- **So what:** both visitors arrived on the promise "remembers everything", tried the one button that might show it, and got nothing; the "is this real" question was never answered by the product itself, only by the About page.
- **Framework tags:** Q1 proof · claim quality
- **Flow:** shape_v2
- **Locator:** /index.html see-it-in-action
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero: "Your thoughts, everywhere." · "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed." · one outlined button "See it in action"; the hero image is two overlapping circles.
  - Clicking/tapping "See it in action" produced no navigation, scroll or modal on desktop (00:40, twice) or mobile (02:20).
  - No screenshot, clip, or example note appears on any page visited; the sceptic's Q6 verdict is "No".
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/timeline.json` (`trust_down`: "'See it in action' does nothing")
  > "'It remembers everything.' No — nothing on the site shows it remembering anything; the button that might have doesn't work."
- **Repro:**
  1. Open `/`; click "See it in action".
  2. Observe no change; scroll the full page looking for a product image.
- **Fix:** Make "See it in action" open a 30-second clip or an annotated screenshot of a note captured on one device and appearing on another; replace the placeholder hero image with a real product frame.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Home-page "How it works" copy ("card" vs "blocks") may read as inconsistent — `01-scrolled.png` is a blank capture, and this is clarity's question anyway.
- Whether the tracker sets a cookie (as opposed to a uid in the URL) — no cookie jar was captured; the P0 rests on the banner text vs the network log and the privacy page, not on cookie storage.

## For other lenses
- "Features" nav item returns 404 (`persona-evaluator/screenshots/04-features-404.png`, `network-full.txt:8`) — bugs, conversion.
- "See it in action" click produces no action on either device — bugs (the defect); trust scores only its consequence.
- Seven-field demo form as the only conversion path; newsletter box outweighs the primary CTA — conversion.
- "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology" undefined — clarity.
- 3.9 MB hero PNG and render-blocking third-party font — technical.

## Coverage gaps
- Sceptic never opened Pricing or scrolled to the testimonials; severity flips on those findings could not be observed.
- /features.html never rendered (404); no persona saw a features page.
- `persona-evaluator/screenshots/01-scrolled.png` and `03-demo-form.png` are blank; testimonial and form findings rest on log lines only.
- No terms-of-service page exists in the nav or footer; neither persona looked for one.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00-landing, 01-scrolled (blank), 02-pricing, 03-demo-form (blank), 04-features-404, 05-about, 06-privacy · sceptic 00-landing, 01-privacy, 02-about
