# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions — is it real · what does it cost · who is behind it · what happens to my data — scored against `trust_up`/`trust_down` and debrief Q5
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (evaluator on desktop, sceptic on iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Only what the persona could verify from the site is reported; nothing was checked outside the capture. This is not a compliance review.

---

## Findings

### d7470c89ca1f — Cookie bar says no tracking cookies while a third-party tracker fires and the privacy page says cookies are used
- **Severity:** P0
- **So what:** The site's first written promise is contradicted by its own network traffic and its own privacy page; both personas caught the copy contradiction and stopped believing the rest.
- **Framework tags:** Data handling · Consistency
- **Flow:** shape_v3
- **Locator:** /index.html cookie bar
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Landing banner reads "We use no tracking cookies on this site." (both viewports).
  - On landing, `analytics.example-tracker.test/t.js` loads (38 KB) and `POST /collect?uid=…` returns 204 — before any consent click.
  - `/privacy.html` reads "We use cookies and similar technologies." and "We may share information with partners and service providers."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/network-full.txt:4` · `persona-evaluator/network-full.txt:5` · `persona-sceptic/network-full.txt:2` · `persona-sceptic/network-full.txt:3` · `persona-evaluator/screenshots/06-privacy.png` · `persona-sceptic/screenshots/01-privacy.png` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10`
  > "The cookie bar said no tracking. This page says they use cookies and share with partners. Which is it?" — evaluator
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." — sceptic
- **Repro:**
  1. Open `/` in a fresh context; read the black bar at the bottom.
  2. Open the network panel: observe `t.js` and `POST /collect?uid=` to `analytics.example-tracker.test`.
  3. Click footer "Privacy"; read the third sentence.
- **Fix:** Either remove the `analytics.example-tracker.test` script or rewrite the banner to say what actually loads, and make `/privacy.html` say the same thing in the same words.

### 0310e531246b — No plan shows a price; all three say Contact sales and the footnote adds an unknown
- **Severity:** P1
- **So what:** The evaluator came to learn the price, could not, and left to "search for an alternative with a price on the page" — the run's stated objective fails here.
- **Framework tags:** Pricing transparency · Claim quality
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three cards — Starter, Team, Enterprise — each with only "Contact sales"; no number, no currency, no "free" anywhere on the page.
  - Footnote: "Pricing depends on your workspace type and sync topology." Neither term is defined on the site.
  - "Contact sales" routes to the home-page demo form; the evaluator gave up at 02:30 (`price_found: false`, `gave_up: true`).
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17` · `persona-evaluator/session.log:18` · `persona-evaluator/session.log:19` · `persona-evaluator/timeline.json` (shape_v3.price_found=false, objectives[0].gave_up=true)
  > "Money, no — I don't know what they'd charge." — evaluator, debrief Q5
- **Repro:**
  1. Click "Pricing" in the top nav.
  2. Read all three cards and the grey footnote.
  3. Click any "Contact sales" button.
- **Fix:** Put a number (or "Free") on the Starter card and a per-seat number on Team; keep "Contact sales" for Enterprise only, and replace the footnote with a one-line definition of what changes the price.

### 69aaf3f1d3ab-a — Privacy page names no partners, no data types, and routes questions to the demo form
- **Severity:** P1
- **So what:** The sceptic's whole visit was the data question; the privacy page answered none of it and they left at 02:40 — "left; data handling unclear".
- **Framework tags:** Data handling · Provenance
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Four sentences: "We collect information you provide and information about how you use the service. We may share information with partners and service providers to improve your experience. We use cookies and similar technologies. We may update this policy at any time."
  - No partner named, no data category listed, no retention, no contact — "Questions? Use the demo form."
  - The one concrete data answer ("In the EU (Frankfurt) by default") is on `/about.html`, not here.
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/session.log:12` · `persona-sceptic/session.log:14` · `persona-sceptic/timeline.json` (shape_v4.verdict)
  > "That's not a privacy policy, that's a shrug." — sceptic
  > "The About page made them real … The privacy page took it back." — sceptic, debrief Q5
- **Repro:**
  1. On iPhone viewport, open `/`, tap footer "Privacy".
  2. Read the page; look for any named partner or a contact route other than the demo form.
- **Fix:** On `/privacy.html`, list the third parties by name (including the analytics provider), what is collected, where it is stored (Frankfurt — move the About answer here), and a privacy contact email instead of "Use the demo form."

### 69aaf3f1d3ab-b — Privacy page names no partners, no data types, and routes questions to the demo form
- **Severity:** P2
- **So what:** For the evaluator this did not drive the exit (price did) but it turned "data: yes" into "data: unsure" after the About page had won them over.
- **Framework tags:** Data handling · Consistency
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Same page and same copy as `69aaf3f1d3ab-a`; reached at 04:50 after the About page.
  - Evaluator's unanswered list includes "Who are the partners you share data with?"
  - Debrief Q5: money no, data unsure — the privacy page is what made it unsure.
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/timeline.json` (shape_v3.questions_unanswered)
  > "Data, unsure. The About page made them feel real (a named founder, an address). The privacy page and the cookie bar contradicting each other undid that." — evaluator, debrief Q5
- **Repro:**
  1. On desktop, open `/about.html`, then footer "Privacy".
  2. Look for the word "partners" and any name attached to it.
- **Fix:** Same as `69aaf3f1d3ab-a`.

### db09f2784f98 — All three testimonials are anonymous
- **Severity:** P2
- **So what:** "Loved by teams" is the only proof section on the site and the evaluator dismissed it outright, so the site's "is this real?" answer rests entirely on the About page.
- **Framework tags:** Proof · Claim quality
- **Flow:** shape_v2
- **Locator:** /index.html Loved by teams
- **Personas hit:** evaluator
- **Observed:**
  - Three quotes attributed to "— a happy customer", "— a user", "— anonymous".
  - No customer name, company, logo, or number anywhere on the page; the heading "Loved by teams" is the only claim of scale.
  - Sceptic scrolled straight to the footer and never read this section, so a second reading was not observed.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14` · `persona-evaluator/findings-raw.json` (t=01:25)
  > "Nobody has a name. I don't believe these." — evaluator
- **Repro:**
  1. Open `/`, scroll to "Loved by teams".
  2. Read the attribution on each of the three cards.
- **Fix:** Replace the three cards with one or two named quotes (person, role, company) or a single specific number; delete any quote that cannot carry a name.

### e3e6490bbfaf — Demo form demands a phone number before the visitor has seen the product
- **Severity:** P2
- **So what:** The only route to a price is a seven-field form with a required phone number; the evaluator listed it under trust-down and backed out without submitting.
- **Framework tags:** Data handling · Pricing transparency
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - "Contact sales" on every pricing card lands on the home-page "Book a demo" form.
  - Fields logged: first name, last name, work email, phone number, company, company size, what do you want to see — seven; phone required.
  - The capture's form screenshot rendered blank, so the field list rests on the session log; the form heading and first two fields are visible in `01-scrolled.png`.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:20` · `persona-evaluator/session.log:21` · `persona-evaluator/session.log:22` · `persona-evaluator/timeline.json` (shape_v3.trust_down)
  > "Phone is required. I haven't seen the product and they want my phone number." — evaluator
- **Repro:**
  1. Open `/pricing.html`, click "Contact sales" on Starter.
  2. Count the fields on "Book a demo"; note which are marked required.
- **Fix:** Make phone optional on the "Book a demo" form and cut it to name, work email, and the free-text question; state next to the button what happens after submitting.

### 5f0141fe66ca — The data-residency and export answers live on About, not on Privacy or the home page
- **Severity:** P2
- **So what:** The site's most trust-building answers were found by accident on the third or fourth page; a visitor who leaves after Privacy never sees them.
- **Framework tags:** Data handling · Provenance · Consistency
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` FAQ answers "Where is my data stored? In the EU (Frankfurt) by default." and "Can I export my notes? Yes… on every plan."
  - `/privacy.html` says nothing about storage location or export; the home page says nothing about either.
  - Both personas recorded About as trust-up and asked why the answers were not where they looked for them.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12` · `persona-evaluator/screenshots/06-privacy.png`
  > "That's the answer I wanted and it's on the About page, not the Privacy page." — sceptic
  > "Those are actual answers. Why isn't this on the home page?" — evaluator
- **Repro:**
  1. Open `/privacy.html`; search for "Frankfurt" or "export" — absent.
  2. Open `/about.html`; read the FAQ.
- **Fix:** Copy the three FAQ answers onto `/privacy.html` (storage, export) and add a one-line "Made by Nimbus Notes Ltd, Bristol · data stored in Frankfurt" strip to the home page above the fold.

### b2f2b68c3599 — Hero promises nothing is ever lost or exposed but the site never shows the product
- **Severity:** P2
- **So what:** Both personas arrived on a promise ("remembers everything"), could find nothing that demonstrates it, and rated the promise "close but off" / "no".
- **Framework tags:** Proof · Claim quality
- **Flow:** shape_v2
- **Locator:** /index.html hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Sub-headline: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed." No mechanism, screenshot, or number follows.
  - The hero image is a placeholder of two circles; the only product link, "See it in action", did nothing on two desktop clicks and one mobile tap.
  - "Features" in the nav returns a 404, so there is no page that shows the product either.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-evaluator/screenshots/04-features-404.png`
  > "nothing on the site shows it remembering anything; the button that might have doesn't work." — sceptic, debrief Q6
  > "the line is on the page, but nothing shows me it happening, and the page around it is about vaults and graphs." — evaluator, debrief Q6
- **Repro:**
  1. Open `/`; click "See it in action" — no navigation, no modal.
  2. Click "Features" in the nav — 404.
- **Fix:** Wire "See it in action" to a real screenshot or 30-second capture of a note syncing between two devices, and replace "zero-knowledge vault" with one plain sentence on what "never exposed" means.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The demo form may set or read cookies on submit — no submission was made and no network entry exists for the form.
- Newsletter box may collect email without a stated purpose — neither persona interacted with it and no reaction was logged.

## For other lenses
- "Features" nav link returns 404 (`persona-evaluator/screenshots/04-features-404.png`, `network-full.txt:8`) — bugs, seo
- "See it in action" button does nothing on click/tap — bugs, conversion
- Seven-field demo form as the only conversion path; no self-serve trial found despite goal "Start a free trial without talking to sales" — conversion
- "workspace type", "sync topology", "sync graph", "zero-knowledge vault" undefined — clarity
- Newsletter box visually outranks the product CTA — conversion

## Coverage gaps
- Sceptic never opened `/pricing.html` and did not read testimonials — pricing and proof findings are single-persona.
- `persona-evaluator/screenshots/03-demo-form.png` is blank; the demo-form field list rests on `session.log:21` only.
- No terms-of-service page exists in the nav or footer; neither persona looked for one.
- No page with a named human other than the founder line on `/about.html` was reached.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06 (`00-landing`, `01-scrolled`, `02-pricing`, `03-demo-form` (blank), `04-features-404`, `05-about`, `06-privacy`); sceptic 00–02 (`00-landing`, `01-privacy`, `02-about`)
