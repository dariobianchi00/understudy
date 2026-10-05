# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: trust lens — four questions (is this real · what does it cost · who is behind it · what happens to my data), plus objection handling
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900 · sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Only what the personas could verify from the site; no outside checks on the company

---

## Findings

### 5a870b21a38a — Cookie banner says "no tracking cookies" while every visit sends a visitor ID to a third-party tracker
- **Severity:** P0
- **So what:** The site's first data claim is contradicted by its own traffic; both personas caught the contradiction and it erased the trust About had built.
- **Framework tags:** data-handling, consistency, cookie-banner-mismatch
- **Flow:** V3
- **Locator:** /index.html#cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Banner on landing, both devices: "We use no tracking cookies on this site." — its OK button only hides the bar
  - Both network logs show `analytics.example-tracker.test/t.js` loaded, then a `POST /collect?uid=…` → 204, with no consent choice offered
  - Privacy page says "We use cookies and similar technologies." Cookie jar not captured; the mismatch rests on the banner versus the tracker calls
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt:4-5` (`[GET] https://analytics.example-tracker.test/t.js → 200` · `[POST] https://analytics.example-tracker.test/collect?uid=8f3a… → 204`) · `persona-sceptic/network-full.txt:2-3` (`[POST] …/collect?uid=2c91… → 204`) · `crawl/html/1-index.html:3` (`<script src="https://analytics.example-tracker.test/t.js" async>`, unconditional) · `crawl/html/1-index.html:37` · `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." — sceptic
  > "The privacy page and the cookie bar contradicting each other undid that." — evaluator, Q5
- **Repro:**
  1. Open `/` in a fresh context with network logging on
  2. Read the bottom bar: "We use no tracking cookies on this site."
  3. Observe `t.js` load and `POST /collect?uid=…` fire before or regardless of tapping OK
- **Fix:** Either remove the third-party tracker or replace the banner with one that names it and offers a real choice before it loads.

### d18a7d49f772 — No plan shows a price, so the evaluator could not learn the cost and gave up
- **Severity:** P1
- **So what:** The evaluator came to check cost, found none, and said they would search for an alternative instead.
- **Framework tags:** pricing-transparency, objection-made-worse
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise all show only "Contact sales"; no number, range or unit anywhere
  - Only explanation: "Pricing depends on your workspace type and sync topology." — the evaluator did not know what either meant
  - Objective "find out what it costs without giving an email" attempted 01:48–02:30, `gave_up: true`
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17-19` · `persona-evaluator/timeline.json` → `price_found: false`, `objectives[0].gave_up: true` · `persona-evaluator/persona-debrief.md` Q3, Q5
  > "So I can't find out what it costs. That's the thing I came to check."
  > "Money, no — I don't know what they'd charge."
- **Repro:**
  1. Open `/`, click "Pricing" in the nav
  2. Look for any figure on the three plan cards
  3. Read the footnote under the cards
- **Fix:** Put a starting price (or per-seat range) on Starter and Team; reserve "Contact sales" for Enterprise.

### f7278a9c7e73 — Privacy page names no partners, and the sceptic left because of it
- **Severity:** P1
- **So what:** The sceptic arrived asking what happens to her notes, could not find out, and left at 02:40.
- **Framework tags:** data-handling, objection-made-worse, severity-flip
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Whole policy is four sentences: "We may share information with partners and service providers to improve your experience."
  - No partner, processor, data category or retention period is named; "We may update this policy at any time."
  - Pre-session leave condition was "a privacy page that is a link to a generic policy"; she left (`left_early: true`)
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:4` · `persona-sceptic/session.log:9` · `persona-sceptic/session.log:14` · `persona-sceptic/timeline.json` → `left_early: true`, `verdict: "left; data handling unclear"` · `persona-sceptic/persona-debrief.md` Q3
  > "That's not a privacy policy, that's a shrug."
  > "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are."
- **Repro:**
  1. From any page, tap "Privacy" in the footer
  2. Look for the names of the "partners and service providers"
- **Fix:** Name every third party that receives data (including the analytics provider), what each gets, and why, on `/privacy`.

### 0ae40e904b8d — Unnamed partners on the privacy page left the evaluator unsure about data, but not gone
- **Severity:** P2
- **So what:** Same page, lower stakes: the evaluator was already leaving over price, but listed the partners as an unanswered question.
- **Framework tags:** data-handling, severity-flip
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Read "We may share information with partners and service providers" at 04:50
  - Asked "Which partners? It doesn't say." and moved on; departure was driven by price
  - Q5 data answer: "unsure"
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/timeline.json` → `questions_unanswered` "Who are the partners you share data with?" · `persona-evaluator/persona-debrief.md` Q5
  > "Which partners? It doesn't say."
- **Repro:**
  1. Open `/privacy.html`
  2. Look for named partners
- **Fix:** Same change as for the sceptic: list the named third parties on `/privacy`.

### 2898ecfd61b5 — All three testimonials are anonymous, and the evaluator did not believe them
- **Severity:** P2
- **So what:** The only proof on the site carries no name, company or number, so it subtracted trust instead of adding it.
- **Framework tags:** proof, claim-quality
- **Flow:** V2
- **Locator:** /index.html
- **Personas hit:** evaluator
- **Observed:**
  - "Loved by teams": "It changed how we work." — "a happy customer"; "Finally, notes that sync." — "a user"; "10/10 would recommend." — "anonymous"
  - No customer names, logos, usage numbers or case studies found on any page visited
  - Logged in `trust_down`; evaluator kept browsing
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `persona-evaluator/timeline.json` → `trust_down` "Anonymous testimonials"
  > "Nobody has a name. I don't believe these."
- **Repro:**
  1. Open `/`, scroll to "Loved by teams"
  2. Read the attribution on each quote
- **Fix:** Replace the three quotes with one or two attributed to a named person and company, ideally with a number.

### f752da687911 — The only route to a price demands a phone number before the product has been shown
- **Severity:** P2
- **So what:** Asking for a phone number before showing anything read as a data grab; the evaluator backed out rather than hand it over.
- **Framework tags:** data-handling, objection-made-worse
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - "Contact sales" on Pricing lands on "Book a demo" on the home page
  - Seven fields; first name, last name, work email, "Phone number" and company are all `required`
  - Evaluator counted the fields, then backed out at 03:15 without submitting
- **Evidence:** `persona-evaluator/session.log:20-22` · `crawl/html/1-index.html:30-32` (`<label>Phone number</label><input type="tel" required>`) · `persona-evaluator/timeline.json` → `trust_down` "Phone number required for a demo" · `persona-evaluator/screenshots/01-scrolled.png` (form heading visible)
  > "Phone is required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Open `/pricing.html`, click any "Contact sales"
  2. Read the required fields on "Book a demo"
- **Fix:** Make phone optional on the demo form, and stop routing price questions through it.

### 4b3bc82ed518 — The product is never shown, and the one button that promises it does nothing
- **Severity:** P2
- **So what:** Neither persona saw the product exist; "is this real?" stayed half-answered for both, and the sceptic named it in Q6.
- **Framework tags:** proof, is-this-real
- **Flow:** V2
- **Locator:** /index.html#see-it-in-action
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero image is two abstract circles; no product screen on landing, pricing, about or privacy
  - "See it in action" did nothing on desktop (two clicks) or phone (tap)
  - Features page, the other possible route, returned 404
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-evaluator/screenshots/04-features-404.png` · `persona-sceptic/persona-debrief.md` Q6
  > "nothing on the site shows it remembering anything; the button that might have doesn't work." — sceptic
- **Repro:**
  1. Open `/`
  2. Click "See it in action"
  3. Look for any screenshot or video of the product on any page
- **Fix:** Replace the hero blobs with a real product screenshot, and make "See it in action" open a short demo clip.

### 865f731bb534 — The best trust answers on the site — founder, address, data in Frankfurt — live only on About
- **Severity:** P2
- **So what:** The one page that built trust was found by chance; a visitor who stops on the home page never sees it.
- **Framework tags:** provenance, data-handling
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About: "Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman", Bristol address, "Company number 14482201"
  - FAQ: "In the EU (Frankfurt) by default." — not on Privacy or the home page
  - Both personas logged About as their only `trust_up` moments
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24-25` · `persona-sceptic/session.log:11-12` · both `timeline.json` → `trust_up`
  > "That's the answer I wanted and it's on the About page, not the Privacy page." — sceptic
  > "Those are actual answers. Why isn't this on the home page?" — evaluator
- **Repro:**
  1. Open `/privacy.html` and `/`; look for where data is stored or who runs the company
  2. Open `/about.html`; both answers are there
- **Fix:** Copy the Frankfurt storage answer into `/privacy`, and add a one-line "made by Nimbus Notes Ltd, Bristol" with the founder to the home page.

### d78aac1f9926 — Hero says nothing is ever "exposed" while the privacy page says data is shared with partners
- **Severity:** P3
- **So what:** An absolute promise with no mechanism sits against a vague sharing clause; a careful reader can set one against the other.
- **Framework tags:** claim-quality, consistency
- **Flow:** V1
- **Locator:** /index.html#hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - No page visited explains what "zero-knowledge" means here or how it works
  - Privacy: "We may share information with partners and service providers." Neither persona linked the two lines explicitly
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/06-privacy.png` · `crawl/html/1-index.html:11` · `persona-evaluator/session.log:18`
  > "I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Read the hero subline on `/`
  2. Read the second sentence on `/privacy.html`
- **Fix:** State on `/privacy` exactly what the vault keeps out of reach of Nimbus and its partners, or soften the hero claim.

### c2f4e75a36a1 — Privacy page routes data questions to the sales demo form
- **Severity:** P3
- **So what:** A visitor with a data question is sent to a form that requires their phone number; there is no privacy contact.
- **Framework tags:** data-handling, provenance
- **Flow:** V3
- **Locator:** /privacy.html#questions
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Privacy page ends: "Questions? Use the demo form."
  - No email address or named contact for data questions on any page visited
  - Neither persona commented on it
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-sceptic/screenshots/01-privacy.png` · `crawl/html/1-index.html:31`
- **Repro:**
  1. Open `/privacy.html`
  2. Read the last line
- **Fix:** Add a dedicated privacy contact address to `/privacy` in place of "Use the demo form."

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Demo-form appearance — `persona-evaluator/screenshots/03-demo-form.png` is a blank white image; form content cited from `session.log` and crawl HTML instead.
- Whether the tracker sets a cookie — no cookie jar captured; the P0 rests on the banner versus the network calls.
- Sceptic's reaction to pricing — she never looked; absence of price is not evidenced for her.

## For other lenses
- "See it in action" button does nothing on desktop and mobile — conversion / technical
- Nav "Features" returns 404 — technical
- Hero jargon "bi-directional sync graph", "zero-knowledge vault", "workspace type and sync topology" — clarity
- Newsletter box outweighs the primary button — conversion
- Hero image 3.9 MB, render-blocking third-party font CSS — technical
- JSON-LD `"offers": {"price": }` is malformed — seo / aeo

## Coverage gaps
- Sceptic never opened Pricing or the demo form
- Terms page not found or not visited by either persona
- Cookie storage not captured; behaviour after declining is unknowable (no decline option exists)
- Logged-in product not in scope for a visit

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00-landing, 01-scrolled, 02-pricing, 03-demo-form (blank), 04-features-404, 05-about, 06-privacy · sceptic 00-landing, 01-privacy, 02-about
