# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: clarity lens — what / who / next step, time to comprehension, undefined terms
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 89bc20de83aa — Neither visitor could say what Nimbus Notes is from the page; both guessed it from the brand name
- **Severity:** P1
- **So what:** Both visitors left without the site ever telling them what it does; any guess they carried away came from the logo text.
- **Framework tags:** C-WHAT, C-TTC
- **Flow:** shape_v1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` and `understood_what: false`, `guessed: true` for both personas
  - Headline "Your thoughts, everywhere." names no product category, no task, no outcome
  - Neither recovered by the end: Q1 answers are explicitly guesses from the name, a friend, or a testimonial
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1 · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-evaluator/session.log:28` · `persona-sceptic/session.log:6`
  > "Some kind of notes app, from the name. The headline doesn't say." (evaluator, 00:06)
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." (evaluator, Q1)
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." (sceptic, Q1)
- **Repro:**
  1. Open `/` at 1440×900 or 390×844.
  2. Read only the fold, without scrolling.
  3. Try to say what the product does using only words on screen.
- **Fix:** Rewrite the H1 to name the product and its job in plain words, e.g. "Notes that sync between your laptop and phone"; keep "Your thoughts, everywhere." as the eyebrow.

### edc0170bd82b — The hero subhead uses jargon the visitor could not define
- **Severity:** P2
- **So what:** The one sentence meant to explain the product was skipped as unreadable, so it explained nothing.
- **Framework tags:** C-JARGON, C-WHAT
- **Flow:** shape_v1
- **Locator:** /index.html .hero subhead
- **Personas hit:** evaluator
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Visitor could define neither "bi-directional sync graph" nor "zero-knowledge vault"; assumed "it syncs"
  - "What is a sync graph?" is in `questions_unanswered` at the end of the visit
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/timeline.json` shape_v3.questions_unanswered · `crawl/html/1-index.html` meta description
  > "\"bi-directional sync graph with a zero-knowledge vault\" — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open `/`.
  2. Read the grey line under the H1.
- **Fix:** Replace the subhead with outcome language: what syncs, between which devices, and that only you can read it; drop "graph" and "vault".

### f0b28db67001 — The fold never says who Nimbus Notes is for
- **Severity:** P2
- **So what:** The evaluator came to judge it for their team and finished still asking whether it is for individuals or teams.
- **Framework tags:** C-WHO
- **Flow:** shape_v1
- **Locator:** /index.html .hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` for both personas
  - Only audience cue on the home page is the "Loved by teams" heading, below the fold
  - The pricing page says "For individuals." and "For growing teams.", but the evaluator still listed "Is it for individuals or teams?" as unanswered
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6` · `persona-evaluator/persona-debrief.md` Q2
  > "I can't tell. The top of the page names nobody. \"Loved by teams\" lower down suggests teams. Maybe me, maybe not." (evaluator, Q2)
  > "The page doesn't say. Possibly me." (sceptic, Q2)
- **Repro:**
  1. Open `/`.
  2. Look for an audience (person, role, team size) above the fold.
- **Fix:** Name the audience in the hero, e.g. "for individuals and small teams", matching the Starter and Team plan labels.

### 276bc5e0f6c9 — The See it in action button goes nowhere, so the product is never shown
- **Severity:** P2
- **So what:** The only route to seeing what the product does is dead, so "remembers everything" stays an unexplained claim.
- **Framework tags:** C-NEXT, C-WHAT
- **Flow:** shape_v1
- **Locator:** /index.html a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is the hero's only button; markup is `<a class="cta" href="#">`
  - Evaluator clicked twice at 00:40, sceptic tapped at 02:20; the page did not change either time
  - Sceptic's Q4 includes "What \"remembers everything\" looks like"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `crawl/html/1-index.html:12`
  > "\"It remembers everything.\" No — nothing on the site shows it remembering anything; the button that might have doesn't work." (sceptic, Q6)
- **Repro:**
  1. Open `/`.
  2. Click "See it in action".
  3. Observe that nothing happens.
- **Fix:** Point "See it in action" at a 30-second product clip or an interactive sample note on the home page.

### 2bdc943ad6ff — The newsletter box outweighs the product button, so the next step reads as subscribe
- **Severity:** P2
- **So what:** The visitor could not tell what the page wanted them to do; the biggest, brightest ask is a newsletter for a product they cannot yet name.
- **Framework tags:** C-NEXT
- **Flow:** shape_v1
- **Locator:** /index.html newsletter section
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero button is a small outlined "See it in action"; directly below sits a full-width filled purple "Get the Nimbus newsletter" panel
  - Evaluator `understood_next_step: false`
  - Both personas named the newsletter box as the dominant element under the button
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1
  > "There's a small outlined \"See it in action\" button. The newsletter box below it is much bigger and brighter than that button." (evaluator, 00:11)
- **Repro:**
  1. Open `/` at 1440×900.
  2. Scroll one screen and compare the hero button with the newsletter panel.
- **Fix:** Make the hero action a filled primary button and move the newsletter panel to the footer.

### c41c7dda5d27 — The clearest description of what Nimbus does is in the About page FAQ, not on the home page
- **Severity:** P2
- **So what:** Visitors who skip About never learn it works offline, exports to Markdown, and stores data in Frankfurt.
- **Framework tags:** C-WHAT, C-PLACEMENT
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Nimbus Notes stores every note on your device first and syncs when a connection returns."
  - Also: "Settings → Export produces a folder of Markdown files" and "In the EU (Frankfurt) by default."
  - Both personas found it only after leaving the home page; the evaluator asked why it was not there
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "Those are actual answers. Why isn't this on the home page?" (evaluator, 04:20)
  > "That's the answer I wanted and it's on the About page, not the Privacy page." (sceptic, 01:50)
- **Repro:**
  1. Open `/`; note no mention of offline, export or data location.
  2. Open `/about.html` and read the FAQ.
- **Fix:** Lift the three About FAQ answers into a home-page section directly under the hero.

### faf683073a7a — The pricing page explains itself with workspace type and sync topology, terms the visitor did not have
- **Severity:** P2
- **So what:** The visitor could not work out which plan applied to them, because the deciding terms are never defined.
- **Framework tags:** C-JARGON
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Footnote reads "Pricing depends on your workspace type and sync topology."
  - "What is a workspace type?" is in `questions_unanswered`
  - Enterprise card adds "vault residency", also undefined
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/timeline.json` shape_v3.questions_unanswered
  > "I don't know what my workspace type is. I haven't got one." (evaluator, 02:10)
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the line under the three plan cards.
- **Fix:** Replace the footnote with the plain factor that changes the plan, e.g. number of people and devices.

### 519872cd4d21 — The promise that brought visitors in sits in one card below the fold and is never shown working
- **Severity:** P2
- **So what:** Both visitors arrived on "remembers everything" and left without knowing what that means in practice.
- **Framework tags:** C-WHAT, C-PROMISE
- **Flow:** shape_v2
- **Locator:** /index.html how-it-works Remember card
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "Nimbus remembers everything so you never start from zero." appears only as the third How it works card
  - Evaluator Q6: "close but off"; sceptic Q6: "No"
  - Sceptic `questions_unanswered` includes "What does 'remembers everything' actually do?"
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:2` · `persona-evaluator/session.log:13` · `persona-sceptic/session.log:2` · `persona-sceptic/timeline.json` shape_v3.questions_unanswered
  > "Close but off — the line is on the page, but nothing shows me it happening, and the page around it is about vaults and graphs." (evaluator, Q6)
- **Repro:**
  1. Open `/` and scroll to How it works.
  2. Find the Remember card; look for an example of remembering.
- **Fix:** Show one concrete example under the Remember card, e.g. an old note surfacing while you type, with a screenshot.

### 1f635e8ee637 — The Features nav link returns a 404, removing the page meant to explain the product
- **Severity:** P2
- **So what:** A visitor looking for what it does follows the obvious nav item and gets a raw server error.
- **Framework tags:** C-WHAT, C-DEADEND
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - Nav item "Features" links to `features.html`
  - Page shows a bare "Error response / Error code: 404 / Message: File not found."
  - Crawl records `features.html` status 404
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `crawl/index.json` · `crawl/html/1-index.html:6`
- **Repro:**
  1. Open `/`.
  2. Click "Features" in the nav.
- **Fix:** Publish a Features page with plain descriptions of capture, sync and remember, or remove the nav item.

### ebcf3576f95f — On a 390px phone the headline and subhead are cut off at the right edge
- **Severity:** P2
- **So what:** On a phone the only explanatory sentence on the fold cannot be read in full.
- **Framework tags:** C-FOLD, C-WHAT
- **Flow:** shape_v1
- **Locator:** /index.html hero at 390px
- **Personas hit:** sceptic
- **Observed:**
  - Headline is clipped to "Your thoughts, everywh"
  - Subhead lines end mid-word, "zero-kno" and "lost or e"; nav "About" is clipped to "Abo"
  - Illustration fills the rest of the fold; the cookie bar covers the bottom
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:5` · `persona-sceptic/timeline.json` viewport
- **Repro:**
  1. Open `/` at 390×844.
  2. Read the headline and subhead without scrolling sideways.
- **Fix:** Let the hero headline and subhead wrap at mobile widths and fit the nav to 390px.

### 0acb5b993625 — How it works calls the same thing a card, a block and a graph
- **Severity:** P3
- **So what:** Three nouns for one thing made the visitor wonder whether they are different objects.
- **Framework tags:** C-JARGON
- **Flow:** shape_v2
- **Locator:** /index.html how-it-works cards
- **Personas hit:** evaluator
- **Observed:**
  - Capture card: "Write a card. It joins the graph instantly."
  - Sync card: "Blocks flow between devices through the vault."
  - Visitor read on without resolving it
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say \"card\", the sync one says \"blocks\". Are those different things?" (evaluator, 01:10)
- **Repro:**
  1. Open `/` and scroll to How it works.
  2. Compare the nouns in the Capture and Sync cards.
- **Fix:** Call it a "note" everywhere, matching the product name.

### bc3b843ba9c6 — The hero illustration is two abstract circles and a placeholder caption that show no product
- **Severity:** P3
- **So what:** The largest element on the fold, the whole fold on a phone, says nothing about what the product does.
- **Framework tags:** C-FOLD
- **Flow:** shape_v1
- **Locator:** /index.html hero illustration
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Two overlapping lilac circles with a clipped caption reading "a real capture serves assets/generated/hero.png"
  - Personas described it only as "A purple blob picture" and "a purple picture that takes the whole screen"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:5` · `persona-sceptic/session.log:5`
- **Repro:**
  1. Open `/`.
  2. Look at the illustration under the subhead.
- **Fix:** Replace the circles with a real screenshot of a note open on a laptop and a phone side by side.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**
- Evaluator's log quotes the 404 page as "That page does not exist."; the screenshot shows a generic server error — cited the screenshot, not the log wording.
- Whether the sceptic read the clipped mobile headline in full — the log quotes it whole; no evidence either way.

## For other lenses
- Pricing shows no figures; every plan says "Contact sales" — conversion
- "Contact sales" opens a seven-field demo form with required phone — conversion
- Cookie bar "We use no tracking cookies on this site." contradicts the privacy page; page loads an off-domain analytics script — trust, technical
- Privacy page names no partners: "We may share information with partners and service providers." — trust
- Testimonials are anonymous ("— a happy customer", "— a user", "— anonymous"); evaluator lost interest here at 01:25 — trust
- `See it in action` `href="#"`; JSON-LD `offers.price` is empty, invalid JSON — technical, seo, aeo

## Coverage gaps
- Sceptic never scrolled the home page body or opened Pricing; mobile rendering of How it works and Pricing unobserved
- No persona arrived by ad; both arrived with a prior promise (search snippet, friend)
- Two generic personas only; no researched persona

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06 · sceptic 00–02
