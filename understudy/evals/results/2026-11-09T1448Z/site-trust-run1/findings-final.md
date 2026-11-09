# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions (real? cost? who? data?) plus objection tracking, scored against debrief Q5
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Only what the personas could verify on the site is reported; this is not a compliance review

---

## Findings

### c7ef0f4afbd3 — Cookie bar says no tracking cookies while a third-party analytics script posts a visitor ID on load
- **Severity:** P0
- **So what:** The site's first data promise is contradicted by its own traffic; the sceptic left over it and the evaluator lost data trust.
- **Framework tags:** data-handling, consistency, Q4-data
- **Flow:** V1
- **Locator:** /index.html#cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Banner reads "We use no tracking cookies on this site." on both devices
  - Same page load fetches `analytics.example-tracker.test/t.js` and POSTs to `/collect?uid=…`, in both personas' captures
  - Privacy page says "We use cookies and similar technologies." — both personas spotted the contradiction
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt:4-5` · `persona-sceptic/network-full.txt:2-3` · `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10` · `crawl/html/1-index.html:3,37`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." — sceptic
  > "The privacy page and the cookie bar contradicting each other undid that." — evaluator, Q5
- **Repro:**
  1. Load the home page with network capture on
  2. Read the bottom bar: "We use no tracking cookies on this site."
  3. Observe the third-party analytics script and its `collect?uid=` POST, before any consent action
- **Fix:** Either remove the third-party analytics script or rewrite the banner to name it and offer a real choice before it loads.

### 4f737335f10e — Pricing page shows no price on any plan, so the evaluator could not learn the cost and gave up
- **Severity:** P1
- **So what:** The evaluator came to learn the cost, could not, and would search for an alternative with a price on the page.
- **Framework tags:** pricing-transparency, Q2-cost, objective-unmet
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise each show only "Contact sales"; no figure anywhere
  - Only explanation: "Pricing depends on your workspace type and sync topology." — evaluator did not know what a workspace type is
  - Objective "find out what it costs without giving an email" attempted 01:48–02:30, `gave_up: true`
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19,29` · `persona-evaluator/timeline.json` (objectives, `price_found: false`)
  > "So I can't find out what it costs. That's the thing I came to check."
  > "Money, no — I don't know what they'd charge." — Q5
- **Repro:**
  1. Click "Pricing" in the nav
  2. Look for any number on the three plan cards
- **Fix:** Show a price, or a starting-from figure, on at least Starter and Team; define "workspace type" or drop the phrase.

### a958af11958e — Privacy page names no partners, and the sceptic left over it
- **Severity:** P1
- **So what:** The sceptic came specifically to learn what happens to their notes and left without an answer.
- **Framework tags:** data-handling, Q4-data, severity-flip
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Policy is four sentences: "We may share information with partners and service providers to improve your experience."
  - No partner, data type or retention period named; "We may update this policy at any time."
  - Only contact route offered: "Questions? Use the demo form."
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9,14` · `persona-sceptic/persona-debrief.md` (Q3, Q5) · `crawl/html/5-privacy.html`
  > "That's not a privacy policy, that's a shrug."
  > "Leave. … the privacy page won't say who the partners are." — Q3
- **Repro:**
  1. Tap "Privacy" in the footer
  2. Look for a named partner, data category or retention period
- **Fix:** Name each third party and what it receives, list data collected, and give a privacy contact that is not the demo form.

### d478c5e2306e — Privacy page names no partners, leaving the evaluator unsure about data
- **Severity:** P2
- **So what:** Same page, lower stakes: the evaluator's decision turned on price, but data trust stayed at "unsure".
- **Framework tags:** data-handling, Q4-data, severity-flip
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Read "We may share information with partners and service providers." at 04:50
  - Listed "Who they share my data with" among unanswered questions
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/persona-debrief.md` (Q4, Q5)
  > "Which partners? It doesn't say."
  > "Data, unsure." — Q5
- **Repro:**
  1. Click "Privacy" in the footer
  2. Look for who the partners are
- **Fix:** Same as the sceptic variant: name the partners and what each receives on the privacy page.

### bf5cd3f9d43b — The only route to a price demands a phone number before any product is shown, and the evaluator backed out
- **Severity:** P1
- **So what:** "Contact sales" asks for seven fields and a required phone number from someone who has seen no product; the evaluator abandoned it.
- **Framework tags:** pricing-transparency, Q2-cost, objection-ignored
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - "Contact sales" lands on the home-page "Book a demo" form
  - Seven fields; "Phone number" marked required
  - Evaluator backed out without submitting (`forms_submitted: 0`)
- **Evidence:** `persona-evaluator/screenshots/03-demo-form.png` · `persona-evaluator/session.log:20-22` · `crawl/html/1-index.html:31`
  > "I haven't seen the product and they want my phone number."
  > "Backing out. Not filling that in."
- **Repro:**
  1. On /pricing.html click any "Contact sales"
  2. Count the fields and try to submit without a phone number
- **Fix:** Make phone optional on the demo form, and stop routing price questions through it.

### 234a61f9f612 — All three testimonials are anonymous, and the evaluator disbelieved them
- **Severity:** P2
- **So what:** The only social proof on the site lowered trust instead of raising it.
- **Framework tags:** proof, Q1-real, made-worse
- **Flow:** V2
- **Locator:** /index.html#proof
- **Personas hit:** evaluator
- **Observed:**
  - "Loved by teams" quotes attributed to "— a happy customer", "— a user", "— anonymous"
  - No company, name, number or case study anywhere visited
  - Logged in `trust_down`; the sceptic did not scroll this far
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `crawl/html/1-index.html:24-26`
  > "Nobody has a name. I don't believe these."
- **Repro:**
  1. Scroll the home page to "Loved by teams"
  2. Read the attributions
- **Fix:** Replace the three quotes with one or two named customers (person, company) with permission, or remove the section.

### d95af0c3d0e6 — The site's strongest trust signals sit on About, not on the home or privacy pages
- **Severity:** P2
- **So what:** The facts that made both personas believe the company exist only on a page a less determined visitor never opens.
- **Framework tags:** provenance, data-handling, Q3-who
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About names Priya Raman, Bristol address, founded 2023, company number 14482201, eight people
  - "Where is my data stored? In the EU (Frankfurt) by default." appears on About, not on Privacy
  - Both personas logged these as their only `trust_up` items
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12`
  > "That's the first thing on this site that felt like a real business." — evaluator
  > "That's the answer I wanted and it's on the About page, not the Privacy page." — sceptic
- **Repro:**
  1. Open the home page and the privacy page; look for who runs the company or where data is stored
  2. Open About and compare
- **Fix:** Put the company line and the Frankfurt storage answer on the home page footer and at the top of the privacy page.

### 14143e43f64f — No screen of the product is visible anywhere visited, and See it in action does nothing
- **Severity:** P2
- **So what:** "Is this real?" goes unanswered by the product itself; the sceptic logged the dead button as a trust loss.
- **Framework tags:** proof, Q1-real
- **Flow:** V2
- **Locator:** /index.html a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" has `href="#"`; clicked twice by the evaluator, tapped by the sceptic — nothing happened
  - Hero image is abstract circles; no product screenshot on any page visited
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/timeline.json` (`trust_down`) · `crawl/html/1-index.html:12`
  > "nothing on the site shows it remembering anything; the button that might have doesn't work." — sceptic, Q6
- **Repro:**
  1. Click "See it in action" on the home page
  2. Observe no navigation, video or scroll
- **Fix:** Link "See it in action" to a short screen recording or real product screenshots of a note being recalled.

### 5a29248c2c7c — Hero claims nothing is ever lost or exposed with no mechanism a visitor can check
- **Severity:** P3
- **So what:** An absolute security claim with no explanation is easy to doubt; no persona reacted to it on trust grounds.
- **Framework tags:** claim-quality
- **Flow:** V1
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - "Zero-knowledge vault" is not explained on any page visited
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:18` · `crawl/html/1-index.html:11`
  > "I don't know what either of those means."
- **Repro:**
  1. Read the hero subheading
  2. Search the visited pages for what "zero-knowledge vault" means
- **Fix:** Add one plain sentence (e.g. on About or Privacy) explaining who can read notes and how encryption works.

---

## Dropped for want of evidence
- Whether the analytics call sets a cookie — network log shows the script and `collect?uid=` POST, not cookie headers; finding rests on the tracking call, not on cookies
- Renewal terms, what plans exclude — no price exists to attach them to; not separately observable

## For other lenses
- "Features" nav link returns 404 — technical
- Hero does not say what the product is or who it is for; "sync graph", "zero-knowledge vault", "workspace type" jargon — clarity
- Newsletter box outweighs the primary CTA; no self-serve trial path — conversion
- 3.9 MB hero PNG; JSON-LD `"price": }` is malformed — technical / seo

## Coverage gaps
- Sceptic did not open Pricing or scroll to testimonials; cost and proof rest on the evaluator alone
- Log-in and app surfaces not visited
- No persona submitted a form; post-submit handling unseen

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshots — evaluator 00–06 · sceptic 00–02
