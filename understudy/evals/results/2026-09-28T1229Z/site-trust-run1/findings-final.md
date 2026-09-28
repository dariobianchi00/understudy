# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions — is this real · what does it cost · who is behind it · what happens to my data
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop; sceptic, iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Only what the personas could verify from the site is reported; this is not a compliance review

---

## Findings

### 099d7f9ddb29 — Cookie banner says "no tracking cookies" while a third-party analytics tracker loads and posts a visitor ID
- **Severity:** P0
- **So what:** The site's first data claim is contradicted by its own network traffic, and both personas said the contradiction undid their trust.
- **Framework tags:** data-handling, consistency
- **Flow:** shape_v1
- **Locator:** /index.html#cookie
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Banner on landing reads "We use no tracking cookies on this site." with a single "OK" button.
  - Both sessions load `analytics.example-tracker.test/t.js` and send `POST …/collect?uid=…` (204) on landing.
  - The script tag sits in `<head>` and loads regardless of the banner; the privacy page says "We use cookies and similar technologies."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/network-full.txt` (`[GET] https://analytics.example-tracker.test/t.js → 200`, `[POST] https://analytics.example-tracker.test/collect?uid=8f3a… → 204`) · `persona-sceptic/network-full.txt` (`[POST] https://analytics.example-tracker.test/collect?uid=2c91… → 204`) · `crawl/html/1-index.html:3`, `:37` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10`
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." — sceptic
  > "The privacy page and the cookie bar contradicting each other undid that." — evaluator, Q5
- **Repro:**
  1. Open `/` with a network inspector running.
  2. Read the bottom banner: "We use no tracking cookies on this site."
  3. Observe `t.js` and a `collect?uid=` POST to `analytics.example-tracker.test` before any interaction.
- **Fix:** Either remove the analytics script from `<head>` or replace the banner text with an accurate statement naming the analytics provider, loaded only after consent.

### efb286af0672 — Privacy page names no partners and no specifics, and the sceptic left over it
- **Severity:** P1
- **So what:** The sceptic came to learn what happens to their notes, got four generic sentences, and left the site.
- **Framework tags:** data-handling
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Whole policy is one paragraph: "We may share information with partners and service providers to improve your experience."
  - No partner, no data category, no retention; "We may update this policy at any time."
  - Contact route is "Questions? Use the demo form." — the form requiring a phone number.
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9`, `:14` · `persona-sceptic/persona-debrief.md` Q3
  > "That's not a privacy policy, that's a shrug."
  > "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." — Q3
- **Repro:**
  1. Tap "Privacy" in the footer.
  2. Look for a named partner, a list of data collected, or a data location.
- **Fix:** Rewrite /privacy.html to list what is collected, name each third party (including the analytics provider), state the Frankfurt storage location, and give a direct privacy contact.

### 914daf13221c — Privacy page names no partners and no specifics; the evaluator noted it and carried on
- **Severity:** P2
- **So what:** The evaluator's data trust dropped to "unsure"; price, not privacy, was what ended their visit.
- **Framework tags:** data-handling
- **Flow:** shape_v3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Evaluator read the same one-paragraph policy at 04:50.
  - Listed "Who they share my data with" among unanswered questions.
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/persona-debrief.md` Q4, Q5
  > "Which partners? It doesn't say."
- **Repro:**
  1. Click "Privacy" in the footer on desktop.
  2. Look for who "partners and service providers" are.
- **Fix:** Same rewrite as the sceptic variant: name the third parties and list the data collected on /privacy.html.

### 84fc60b294c4 — No plan shows a price, so the evaluator gave up on learning the cost
- **Severity:** P1
- **So what:** The evaluator came to check cost, could not, and said they would search for an alternative — the stated objective failed.
- **Framework tags:** pricing-transparency
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Starter, Team and Enterprise all show only "Contact sales"; no number on the page.
  - Only explanation: "Pricing depends on your workspace type and sync topology."
  - Objective "find out what it costs without giving an email": `gave_up: true`, `price_found: false`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17`–`19`, `:29` · `persona-evaluator/timeline.json` objectives[0] · `persona-evaluator/persona-debrief.md` Q3, Q5
  > "Money, no — I don't know what they'd charge." — Q5
- **Repro:**
  1. Click "Pricing" in the nav.
  2. Look for any price or price range on the three plans.
- **Fix:** Put a starting price (or per-seat range) on each plan card on /pricing.html, at least for Starter and Team.

### 418802c9fbf4 — The only route to a price demands a phone number before any product is shown, and the evaluator backed out
- **Severity:** P1
- **So what:** Asking for a phone number before showing anything turned a pricing question into a data demand, and the evaluator refused.
- **Framework tags:** data-handling, pricing-transparency
- **Flow:** shape_v3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - "Contact sales" on every plan leads to the home-page "Book a demo" form.
  - Seven fields; "Phone number" is `type="tel" required`.
  - Evaluator backed out without submitting (`forms_submitted: 0`).
- **Evidence:** `persona-evaluator/session.log:20`–`22` · `crawl/html/1-index.html:31` (`<label>Phone number</label><input type="tel" required>`) · `persona-evaluator/timeline.json` shape_v3.trust_down
  > "I haven't seen the product and they want my phone number."
- **Repro:**
  1. On /pricing.html click any "Contact sales".
  2. Land on the "Book a demo" form; try to submit without a phone number.
- **Fix:** Make the phone field optional on the demo form, and stop routing price questions through it.

### b87aaea96a93 — All three testimonials are anonymous, and the evaluator did not believe them
- **Severity:** P2
- **So what:** The only proof on the home page was discounted outright, leaving "is this real?" to the About page.
- **Framework tags:** proof
- **Flow:** shape_v2
- **Locator:** /index.html#loved-by-teams
- **Personas hit:** evaluator
- **Observed:**
  - "Loved by teams" quotes are attributed to "— a happy customer", "— a user", "— anonymous".
  - No name, company, role or number on any quote.
  - Timeline marks 01:25 as the evaluator's point of lost interest.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `persona-evaluator/timeline.json` shape_v2.point_of_lost_interest
  > "Nobody has a name. I don't believe these."
- **Repro:**
  1. Scroll the home page to "Loved by teams".
  2. Read the attribution under each quote.
- **Fix:** Replace the three quotes with one or two named customers (person, company, a concrete result), or remove the section.

### 2306d6df3ca7 — The product is never shown: "See it in action" does nothing for either persona
- **Severity:** P2
- **So what:** Neither persona could see the "remembers everything" promise working, so "is this real?" stayed half-answered.
- **Framework tags:** proof
- **Flow:** shape_v2
- **Locator:** /index.html#see-it-in-action
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator clicked twice at 00:40; sceptic tapped at 02:20; the page did not change.
  - The hero image is abstract circles; no product screenshot was seen on any visited page.
  - Console shows `Uncaught ReferenceError: nimbusBootstrap is not defined` on both devices.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-evaluator/console-full.txt` · `persona-sceptic/console-full.txt` · `persona-sceptic/timeline.json` shape_v3.trust_down
  > "'It remembers everything.' No — nothing on the site shows it remembering anything; the button that might have doesn't work." — sceptic, Q6
- **Repro:**
  1. Open `/`.
  2. Click "See it in action".
- **Fix:** Make "See it in action" open a short product video or real screenshots showing a note being recalled.

### 3624665aa713 — The site's strongest trust answers sit only on the About page
- **Severity:** P2
- **So what:** Founder, address, company number and data location won both personas over, but only after other pages had already lost them.
- **Framework tags:** provenance, data-handling
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About names "Priya Raman", "14 Harbourside Walk, Bristol", "Company number 14482201", eight people, founded 2023.
  - "Where is my data stored? In the EU (Frankfurt) by default." appears here, not on /privacy.html.
  - Evaluator reached it at 03:50, after giving up on price; both list it as their trust_up.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24`–`25` · `persona-sceptic/session.log:11`–`12`
  > "That's the answer I wanted and it's on the About page, not the Privacy page." — sceptic
  > "Those are actual answers. Why isn't this on the home page?" — evaluator
- **Repro:**
  1. Visit `/` and /privacy.html; note no founder, company number or data location.
  2. Visit /about.html; all three are there.
- **Fix:** Add the Frankfurt storage answer to /privacy.html and a one-line company/founder strip to the home page footer.

### 0cb23a94240a — Hero promises nothing is "ever lost or exposed" with no mechanism, and the privacy page says data may be shared
- **Severity:** P2
- **So what:** The headline security claim could not be understood, and the site's own policy undercuts it.
- **Framework tags:** claim-quality, consistency
- **Flow:** shape_v1
- **Locator:** /index.html#hero
- **Personas hit:** evaluator
- **Observed:**
  - Hero: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - No page visited explains the vault or what "zero-knowledge" covers.
  - /privacy.html: "We may share information with partners and service providers."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:10`
  > "'bi-directional sync graph with a zero-knowledge vault' — I don't know what either of those means."
- **Repro:**
  1. Read the hero sub-headline on `/`.
  2. Look for an explanation of the vault; then read /privacy.html.
- **Fix:** Replace the hero line with a plain claim ("your notes are encrypted on your device; we can't read them") and state on /privacy.html which data that covers.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether the tracker sets a cookie — the network log shows the request and a `uid`, but no `Set-Cookie` or cookie store was captured.
- What the phone number is used for once submitted — form never submitted.

## For other lenses
- "Features" in the nav returns a 404 — technical / conversion.
- Hero placeholder shows the text "a real capture serves assets/generated/hero.png"; hero.png is 3.9 MB — technical.
- Newsletter box outweighs "See it in action" visually — conversion.
- JSON-LD `"price": }` is malformed on `/` — seo.
- "Workspace type" and "sync topology" jargon on /pricing.html — clarity.

## Coverage gaps
- `persona-evaluator/screenshots/03-demo-form.png` is blank; the demo form is evidenced from the log and crawl HTML instead.
- Sceptic never opened /pricing.html, so no pricing flip could be observed.
- No sign-up or trial surface was reached by either persona.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06 · sceptic 00–02
