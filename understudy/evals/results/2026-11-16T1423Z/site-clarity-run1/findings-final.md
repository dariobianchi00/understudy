# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: clarity lens — what / who / next step, time to comprehension, undefined terms, fold as met
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### ece4cdb54a91 — Neither visitor could say what Nimbus Notes is from the page; comprehension was never reached
- **Severity:** P0
- **So what:** 2 of 2 visitors left guessing from the brand name; the page itself never told them what the product is.
- **Framework tags:** clarity-what, time-to-comprehension
- **Flow:** shape_v1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` and `understood_what: false` for both personas; both flagged `guessed: true`
  - Fold offers only "Your thoughts, everywhere." plus an abstract two-circle illustration — no noun naming the product
  - P0 not P1: the visit's first value (understanding) was never reached by anyone; downgrade only if the name alone is deemed sufficient
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-sceptic/session.log:6` · `timeline.json shape_v1`
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." (evaluator, Q1)
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." (sceptic, Q1)
- **Repro:**
  1. Open `/` at 1440×900 or 390×844, cookie bar up
  2. Without scrolling, try to state what the product is using only page text
- **Fix:** Rewrite the H1 to name the thing in plain words, e.g. "Notes that sync between your laptop and phone — and stay private".

### 700216c0e2ad — Landing page never names who Nimbus Notes is for; both visitors ended unable to answer
- **Severity:** P1
- **So what:** The evaluator came to judge team fit and left not knowing whether it is for individuals or teams.
- **Framework tags:** clarity-who
- **Flow:** shape_v1
- **Locator:** /index.html #hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` for both; no audience named above the fold at either viewport
  - Only audience signal is "Loved by teams" below the fold; Pricing then says Starter is "For individuals."
  - Evaluator's unanswered list still includes "Is it for individuals or teams?" at session end
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6` · `timeline.json shape_v3.questions_unanswered`
  > "I can't tell. The top of the page names nobody." (evaluator, Q2)
  > "The page doesn't say. Possibly me." (sceptic, Q2)
- **Repro:**
  1. Open `/`
  2. Look for any statement of the intended user above the fold
- **Fix:** Add an audience line under the H1, e.g. "For individuals and small teams who write on more than one device".

### 327b0fdec40e — See it in action does nothing, so the site never shows what remembers everything means
- **Severity:** P1
- **So what:** The promise that brought both visitors is never demonstrated; the sceptic tried, failed, and stopped.
- **Framework tags:** clarity-next-step, promise-match
- **Flow:** shape_v2
- **Locator:** /index.html a.cta[href='#']
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is `<a class="cta" href="#">` — clicking does nothing (evaluator twice at 00:40; sceptic at 02:20)
  - "Nimbus remembers everything so you never start from zero." appears only as one card line, never shown
  - Sceptic stopped 20 s after the dead tap
- **Evidence:** `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/session.log:14` · `persona-evaluator/screenshots/00-landing.png` · `crawl/html/1-index.html:12`
  > "I want to see it 'remember' something. The button does nothing when I tap it." (sceptic)
  > "nothing on the site shows it remembering anything; the button that might have doesn't work." (sceptic, Q6)
- **Repro:**
  1. Open `/`
  2. Click "See it in action"
  3. Page does not move or open anything
- **Fix:** Point "See it in action" at a 30-second clip or screenshots showing a note written on laptop and recalled on phone.

### 89e796d474de — Hero subhead explains the product in undefined jargon: sync graph and zero-knowledge vault
- **Severity:** P2
- **So what:** The only explanatory sentence on the fold is the one the visitor could not parse, so it explains nothing.
- **Framework tags:** clarity-jargon
- **Flow:** shape_v1
- **Locator:** /index.html #hero p
- **Personas hit:** evaluator
- **Observed:**
  - Subhead: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator could define neither term and fell back to "I'll assume it syncs"
  - "What a 'sync graph' is" remains in the evaluator's Q4 unanswered list
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `crawl/html/1-index.html:11`
  > "'bi-directional sync graph with a zero-knowledge vault' — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open `/`
  2. Read the line under the H1
- **Fix:** Replace the subhead with outcomes: "Write on any device, find it on every other. Encrypted so only you can read it."

### ba0b5ce2c4bf — The plain-English explanation of the product sits on the About FAQ, not the landing page
- **Severity:** P2
- **So what:** The clearest sentences on the site were reached by persistent visitors only, minutes after first impressions formed.
- **Framework tags:** clarity-placement
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Nimbus Notes stores every note on your device first and syncs when a connection returns." — clearest "what" on the site
  - Also there: Markdown export on every plan; data "In the EU (Frankfurt) by default."
  - Evaluator reached it at 03:50, sceptic at 01:30; both called these the real answers
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "Those are actual answers. Why isn't this on the home page?" (evaluator)
  > "That's the answer I wanted and it's on the About page, not the Privacy page." (sceptic)
- **Repro:**
  1. Open `/`, note no offline/export/data-location statement
  2. Open `/about.html`, read the FAQ
- **Fix:** Lift the three About FAQ answers into a home-page section directly under the hero.

### 500de2ac5930 — Pricing page explains cost with undefined terms: workspace type and sync topology
- **Severity:** P2
- **So what:** The one sentence about how pricing works uses words the visitor had no referent for.
- **Framework tags:** clarity-jargon
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Footnote: "Pricing depends on your workspace type and sync topology."
  - Neither term is defined anywhere on the crawled site
  - "What is a workspace type?" is in the evaluator's unanswered list
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `crawl/html/3-pricing.html:16`
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`
  2. Read the line under the plan cards
- **Fix:** Replace the footnote with plain criteria, e.g. "Price depends on number of people and devices", or delete it.

### 842eec66936c — Newsletter box outweighs the only product CTA, so the next step reads as subscribe
- **Severity:** P2
- **So what:** The evaluator's V1 answer to "what next" was a fail; the loudest ask is an email capture, not the product.
- **Framework tags:** clarity-next-step
- **Flow:** shape_v1
- **Locator:** /index.html newsletter
- **Personas hit:** evaluator
- **Observed:**
  - "See it in action" is a small outlined button; "Get the Nimbus newsletter" is a full-width solid purple band directly beneath
  - Evaluator `understood_next_step: false`; sceptic `true` — severity differs by persona, see flips
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8`
  > "There's a small outlined 'See it in action' button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/` at 1440×900
  2. Compare the hero button with the newsletter band below
- **Fix:** Make the hero CTA the solid, highest-contrast element and move the newsletter band to the footer.

### 50fb337a58b4 — How it works calls the same thing a card, a block and a note without saying so
- **Severity:** P2
- **So what:** The section meant to explain the product introduced a new question instead of answering one.
- **Framework tags:** clarity-vocabulary
- **Flow:** shape_v2
- **Locator:** /index.html #how
- **Personas hit:** evaluator
- **Observed:**
  - Capture: "Write a card. It joins the graph instantly."
  - Sync: "Blocks flow between devices through the vault."
  - Product name says "Notes"; evaluator asked whether cards and blocks differ
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14` · `crawl/html/1-index.html:18`
  > "The cards say 'card', the sync one says 'blocks'. Are those different things?"
- **Repro:**
  1. Open `/`, scroll to "How it works"
  2. Read the three cards in order
- **Fix:** Use "note" everywhere in How it works; drop "card", "block", "graph" and "vault".

### 233468ca3ed0 — Hero headline and subhead are clipped off the right edge on a 390px phone
- **Severity:** P2
- **So what:** On mobile the fold shows "Your thoughts, everywh" and half a subhead, weakening an already unclear message.
- **Framework tags:** clarity-fold, mobile
- **Flow:** shape_v1
- **Locator:** /index.html h1 @390px
- **Personas hit:** sceptic
- **Observed:**
  - At 390×844 the H1, subhead, nav ("Abo…") and illustration run past the right edge
  - Sceptic did not comment; risk is for mobile visitors who read only what is visible
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `measure/screenshots/index-mobile.png`
- **Repro:**
  1. Open `/` on an iPhone 13 viewport (390×844)
  2. Read the headline without scrolling sideways
- **Fix:** Let the hero H1 and subhead wrap at narrow widths and constrain the hero image to the viewport.

---

## Dropped for want of evidence
- None.

## For other lenses
- All three plans say "Contact sales"; no price anywhere; evaluator gave up on the cost objective — conversion
- Demo form: seven fields, phone required, before seeing the product — conversion
- "Features" nav link returns 404 — technical
- Cookie bar "We use no tracking cookies" contradicts privacy page; partners unnamed — trust
- Anonymous testimonials ("— a happy customer", "— anonymous"); evaluator's point of lost interest at 01:25 — trust
- 3.9 MB hero PNG, LCP 5.8 s mobile — technical

## Coverage gaps
- Sceptic never opened Pricing or scrolled the home page beyond one section; mobile pricing comprehension untested by a persona
- Features page unreachable (404), so any explanation there could not be assessed

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06 · sceptic 00–02 · `measure/screenshots/`
