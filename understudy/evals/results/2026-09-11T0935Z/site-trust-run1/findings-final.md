# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four questions a visitor asks — is this real · what does it cost · who is behind it · what happens to my data
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (`persona_mode: generic` in `manifest.json`)
- Scoring model: opus
- Scope: only what the personas could verify from the site; no register, news or outside knowledge — every absence is "the site does not say"
- Not a compliance review: nothing here judges whether the privacy policy is legally sufficient
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 4877166e71a7 — Cookie bar claims no tracking cookies while the page loads a third-party tracker and posts a user id
- **Severity:** P0
- **So what:** The only promise on the site a visitor can check is contradicted on the same page load, which devalues every other claim.
- **Framework tags:** Q4-DATA, CONSISTENCY, CLAIM
- **Flow:** shape_v1
- **Locator:** /index.html #cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Bar reads "We use no tracking cookies on this site." with a single OK button; no choice is offered.
  - Same page load fetches `https://analytics.example-tracker.test/t.js` and POSTs `collect?uid=8f3a…` → 204, on both personas.
  - The site's own privacy page then says "We use cookies and similar technologies."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt` (lines 4–5) · `persona-sceptic/network-full.txt` (lines 2–3) · `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:27` · `crawl/html/1-index.html` (`<script src="https://analytics.example-tracker.test/t.js" async>`)
  > "The cookie bar said no tracking. This page says they use cookies and share with partners. Which is it?"
- **Repro:**
  1. Open `http://localhost:8765/` in a fresh context and read the black bar at the bottom.
  2. Watch the network panel on the same load: `t.js` from `analytics.example-tracker.test`, then `POST /collect?uid=…` → 204.
  3. Open `/privacy.html` and read sentence three.
- **Fix:** Remove the `analytics.example-tracker.test` script from the home page, or replace the bar's text with an accept/reject choice that matches what actually loads.

### a22eec0091b7 — Privacy page names no partners, and the sceptic left the site at 02:40 because of it
- **Severity:** P1
- **So what:** The visitor whose whole question was "what happens to my notes" ended the visit unable to answer it, and left.
- **Framework tags:** Q4-DATA, PROVENANCE
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Whole policy is four sentences: "We may share information with partners and service providers to improve your experience."
  - No partner, processor or category is named; no retention, no deletion, no contact route except "Questions? Use the demo form."
  - She reached it at 00:30, the second page of her visit, and stopped the session at 02:40 with verdict "left; data handling unclear".
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/timeline.json` (`shape_v4.verdict`, `questions_unanswered`) · `persona-sceptic/persona-debrief.md`
  > "'We may share information with partners and service providers.' With whom? Not said. 'We may update this policy at any time.' That's not a privacy policy, that's a shrug."
- **Repro:**
  1. Open `http://localhost:8765/` on a 390×844 viewport.
  2. Tap Privacy in the footer and read the page.
- **Fix:** Name the third parties on `/privacy.html` — the analytics vendor and the hosting provider at minimum — with what each receives, and give a contact address that is not the demo form.

### 5533888d8710 — Privacy page cancels the About page's credibility for the evaluator at 05:20
- **Severity:** P2
- **So what:** The one page that earned this visitor's trust is undone four minutes later, turning a clear "yes" on data into "unsure".
- **Framework tags:** Q4-DATA, CONSISTENCY
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - At 03:50 the About page produced his only trust gain: "the first thing on this site that felt like a real business".
  - At 04:50–05:20 the privacy page gave "partners" with no names and "We may update this policy at any time."
  - He carried on reading rather than leaving; the cost shows only in the debrief answer.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/persona-debrief.md` (Q5)
  > "The About page made them feel real (a named founder, an address). The privacy page and the cookie bar contradicting each other undid that."
- **Repro:**
  1. Open `/about.html`, then `/privacy.html`, and compare how specific each is.
- **Fix:** Bring the About page's specificity to `/privacy.html` — same named-company voice, named recipients, dated last-updated line.

### c229d0beace3 — No price anywhere: three plans all say Contact sales and the only route is a seven-field form
- **Severity:** P1
- **So what:** The visitor could not answer "what does it cost", so he would not recommend the product internally and said he would look elsewhere.
- **Framework tags:** Q2-COST, PRICING-TRANSPARENCY
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise cards each carry only "Contact sales"; no number, range, unit or free tier appears on the page.
  - The page's explanation is "Pricing depends on your workspace type and sync topology." — terms he could not map to himself.
  - He looked at `/pricing.html` then `/index.html#demo` between 01:48 and 02:30, then gave up (`gave_up: true`).
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17` · `persona-evaluator/session.log:19` · `persona-evaluator/timeline.json` (`price_found: false`, objective `gave_up: true`) · `crawl/html/3-pricing.html`
  > "So I can't find out what it costs. That's the thing I came to check."
- **Repro:**
  1. Open `/pricing.html` and read all three cards and the line beneath them.
  2. Click any "Contact sales" — it lands on the seven-field demo form on the home page.
- **Fix:** Put a real number on Starter and Team on `/pricing.html` (with the billing unit and what renewal costs), and keep "Contact sales" for Enterprise only.

### 0fc63c07cdd3 — Nothing on the site shows the product working and the only demonstration link goes nowhere
- **Severity:** P1
- **So what:** Neither visitor saw evidence the product exists, so the promise that brought them was never substantiated.
- **Framework tags:** Q1-REAL, PROOF
- **Flow:** shape_v2
- **Locator:** /index.html a.cta[href="#"]
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is `<a class="cta" href="#">`; both personas clicked or tapped it and nothing happened.
  - The only image on the home page is a decorative blob; no screenshot, video or interface appears on any page reached.
  - Sceptic's Q6 answer is a flat "No" on whether the site matches the promise.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `crawl/html/1-index.html` (`<a class="cta" href="#">See it in action</a>`)
  > "Back to the home page. I want to see it 'remember' something. The button does nothing when I tap it."
- **Repro:**
  1. Open the home page and click "See it in action".
  2. Observe the page does not move and no product is shown.
- **Fix:** Point "See it in action" at a short product recording or an annotated screenshot of a note syncing, and put one product image above the fold.

### 268e9477ee31 — Three testimonials on the home page carry no names and the evaluator disbelieved them
- **Severity:** P2
- **So what:** The site's only social proof reads as invented, so the "Loved by teams" section costs credibility rather than adding it.
- **Framework tags:** Q1-REAL, PROOF, CLAIM
- **Flow:** shape_v2
- **Locator:** /index.html #proof
- **Personas hit:** evaluator
- **Observed:**
  - Attributions are "— a happy customer", "— a user", "— anonymous"; no person, company, role or number appears.
  - "10/10 would recommend." is the strongest claim and the least attributed.
  - The section is headed "Loved by teams" — the same phrase he used to guess who the product is for.
- **Evidence:** `crawl/html/1-index.html` (`<blockquote>"10/10 would recommend." — anonymous</blockquote>`) · `persona-evaluator/session.log:15` · `persona-evaluator/findings-raw.json` (t 01:25)
  > "'Loved by teams' — three quotes. '— a happy customer', '— a user', '— anonymous'. Nobody has a name. I don't believe these."
- **Repro:**
  1. Open the home page and scroll to "Loved by teams".
  2. Read the three attributions.
- **Fix:** Replace the three quotes with one named customer — person, role, company and a number they can stand behind — or delete the section.

### e3e6490bbfaf — Demo form demands a phone number before the visitor has seen the product
- **Severity:** P2
- **So what:** The only route to a price asks for a phone call in exchange for nothing the visitor has yet seen, so he backed out.
- **Framework tags:** Q2-COST, Q4-DATA
- **Flow:** shape_v3
- **Locator:** /index.html #demo
- **Personas hit:** evaluator
- **Observed:**
  - Seven fields: first name, last name, work email, phone number, company, company size, what do you want to see.
  - First name, last name, work email, phone number and company are all `required` in the markup.
  - He opened it at 02:44 and backed out at 03:15 without submitting (`forms_submitted: 0`).
- **Evidence:** `crawl/html/1-index.html` (`<label>Phone number</label><input type="tel" required>`) · `persona-evaluator/session.log:21` · `persona-evaluator/session.log:22` · `persona-evaluator/timeline.json` (`forms_opened: 1`, `forms_submitted: 0`)
  > "Seven fields. Phone required. I haven't seen the product and they want my phone number."
- **Repro:**
  1. Click "Contact sales" on `/pricing.html`, landing on `/index.html#demo`.
  2. Count the fields and check which carry `required`.
- **Fix:** Make phone number and company size optional on the demo form, and say on the form what the visitor gets in return and who will contact them.

### a0a1521ef110 — The only concrete answer about data location sits on the About page, not the privacy page
- **Severity:** P2
- **So what:** The answer both visitors wanted exists and is good, but they had to find it on the page they had no reason to open.
- **Framework tags:** Q4-DATA, PROVENANCE
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` states "In the EU (Frankfurt) by default. Enterprise plans can choose a region.", plus offline behaviour and Markdown export on every plan.
  - `/privacy.html` states none of this; it never mentions where data is stored.
  - Both personas recorded the About page as a trust gain and both still ended unable to answer the data question.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-sceptic/session.log:12` · `persona-evaluator/session.log:25` · `crawl/html/4-about.html`
  > "'Where is my data stored? In the EU (Frankfurt) by default.' That's the answer I wanted and it's on the About page, not the Privacy page."
- **Repro:**
  1. Open `/privacy.html` and search for where data is stored — it is absent.
  2. Open `/about.html` and read the third FAQ.
- **Fix:** Move the storage-location, offline and export answers onto `/privacy.html` and link to them from the home page.

### ffe5a762c5fa — Zero-knowledge vault is claimed with no explanation anywhere on the site
- **Severity:** P2
- **So what:** The strongest security claim on the site is unexplained and sits beside a privacy page that says data is shared, so it reads as decoration.
- **Framework tags:** CLAIM, Q4-DATA
- **Flow:** shape_v1
- **Locator:** /index.html .hero
- **Personas hit:** evaluator
- **Observed:**
  - Subhead: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - No page reached explains what the vault is, who holds keys, or how "never exposed" coexists with sharing data with partners.
  - The evaluator read it at 00:18 and could define neither term.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` (t 00:18) · `crawl/html/1-index.html`
  > "'bi-directional sync graph with a zero-knowledge vault' — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open the home page and read the subhead.
  2. Follow every nav and footer link looking for an explanation of the vault — none exists.
- **Fix:** Either state in one plain line who can read the notes and who holds the keys, or drop "zero-knowledge vault" from the hero.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether the tracker fires before the cookie bar is dismissed — the network log has no timestamps relative to the OK click, only that both requests occur on the page load.
- Whether cookies are actually written to the browser — no cookie jar or storage dump was captured, so the finding rests on the tracker request, not on stored cookies.
- Whether `/features.html` would have carried proof or pricing — the page 404s, so nothing about its intended content can be claimed.
- Whether the sceptic would have accepted an unpriced plan — she never looked for a price, so the price finding could not be flipped across personas.

## For other lenses
- "See it in action" is a dead `href="#"` and the nav's Features link 404s — technical, conversion.
- "workspace type", "sync topology", "card" vs "blocks" were undefined for the persona — clarity.
- The newsletter box outweighs the primary call to action above the fold — conversion.
- `/pricing.html` carries `<meta name="robots" content="noindex">` and the home page's JSON-LD `Offer` is malformed — seo.

## Coverage gaps
- `/features.html` never seen (404); no logged-in surface, no product screen.
- Sceptic left at 02:54 and never opened `/pricing.html`, so the cost question has one persona only.
- `persona-evaluator/screenshots/01-scrolled.png` and `03-demo-form.png` rendered blank in this capture; the testimonial and form findings rest on the session log and the crawled DOM instead.
- No cookie/storage capture, so the banner check rests on network requests alone.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/` · `persona-sceptic/screenshots/`
