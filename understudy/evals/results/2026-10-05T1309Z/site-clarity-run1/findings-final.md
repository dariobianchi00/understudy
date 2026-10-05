# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: clarity lens — what / who / next step, time to comprehension, jargon, placement of the clearest explanation
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### ca1e95f4510d — Headline never says what Nimbus Notes is — both visitors guessed it from the brand name
- **Severity:** P0
- **So what:** Neither visitor ever understood the product; both left without acting. P0 not P1 because comprehension, the flow this lens scores, never completed.
- **Framework tags:** what, time-to-comprehension
- **Flow:** shape_1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Fold shows "Your thoughts, everywhere." plus jargon subhead; no noun saying what the product is.
  - `time_to_comprehension_seconds: null` and `understood_what: false`, `guessed: true` for both personas.
  - Both Q1 answers cite the name, not the page, as their source.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." (evaluator, Q1)
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." (sceptic, Q1)
  > "I still don't know what it costs or exactly what it does beyond 'notes that sync'." (evaluator, session.log:28, 05:45)
- **Repro:**
  1. Open `/` at 1440×900 or 390×844.
  2. Read only the fold; try to say what the product is without using the word "Notes" from the logo.
- **Fix:** Rewrite the H1 or add an eyebrow that names the category and job in plain words, e.g. "Notes that sync across laptop and phone".

### 64812e75eb00 — Hero subhead rests on two terms visitors cannot define — sync graph and zero-knowledge vault
- **Severity:** P2
- **So what:** The only explanatory line above the fold explained nothing; the visitor substituted a guess and moved on.
- **Framework tags:** jargon, what
- **Flow:** shape_1
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator
- **Observed:**
  - Subhead: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator could define neither term at 00:18 and listed "What a 'sync graph' is" in Q4.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` (00:18)
  > "'bi-directional sync graph with a zero-knowledge vault' — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open `/`.
  2. Read the line under the H1.
- **Fix:** Replace the subhead with the benefit in plain words ("Write on any device; it's on all of them, encrypted so only you can read it").

### b5ec8ec58fef — Landing page never says who Nimbus is for; the only audience lines sit on the pricing page
- **Severity:** P2
- **So what:** A team buyer could not tell if this fits a team; churn risk for anyone qualifying themselves on the home page.
- **Framework tags:** who, placement
- **Flow:** shape_1
- **Locator:** /index.html .hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` for both; fold names no audience.
  - Only home-page hint is the "Loved by teams" heading, below the fold.
  - `/pricing.html` does say "For individuals." and "For growing teams." — never on the home page.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:9` · `persona-sceptic/session.log:6`
  > "I can't tell. The top of the page names nobody. 'Loved by teams' lower down suggests teams. Maybe me, maybe not." (evaluator, Q2)
  > "The page doesn't say. Possibly me." (sceptic, Q2)
- **Repro:**
  1. Open `/`; look for any statement of audience above the fold.
  2. Open `/pricing.html`; note "For individuals." / "For growing teams.".
- **Fix:** Add one line under the H1 naming the audience, reusing the pricing copy: "For individuals and growing teams."

### 9329d3aeeac7 — Plainest explanation of the product is buried in the About FAQ, not on the home page
- **Severity:** P2
- **So what:** The sentences that answer "what does it do" exist, but only visitors who reach About ever read them.
- **Framework tags:** placement, what
- **Flow:** shape_3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Nimbus Notes stores every note on your device first and syncs when a connection returns."
  - Also there: "Settings → Export produces a folder of Markdown files" and "In the EU (Frankfurt) by default."
  - Evaluator reached it at 04:20; sceptic at 01:50 — after the fold had already failed.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "Those are actual answers. Why isn't this on the home page?" (evaluator, 04:20)
  > "That's the answer I wanted and it's on the About page, not the Privacy page." (sceptic, 01:50)
- **Repro:**
  1. Open `/about.html`; read the FAQ.
  2. Open `/`; search for the same facts — absent.
- **Fix:** Move the three FAQ answers onto the home page as the "How it works" cards, in their existing plain wording.

### 6c747aac1f76 — See it in action does nothing, so the remembers-everything promise is never shown
- **Severity:** P2
- **So what:** The only route to seeing the product is dead; both visitors' arrival promise stayed unverified. Risk: visitors who wanted proof leave.
- **Framework tags:** next step, promise match
- **Flow:** shape_2
- **Locator:** /index.html .hero a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is `href="#"`; clicked twice by evaluator, tapped by sceptic — nothing happened.
  - Q6 promise match: evaluator "Close but off", sceptic "No".
  - Evaluator also read the outlined button as weaker than the newsletter box (`understood_next_step: false`).
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:8` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `crawl/html/1-index.html:12`
  > "'It remembers everything.' No — nothing on the site shows it remembering anything; the button that might have doesn't work." (sceptic, Q6)
- **Repro:**
  1. Open `/`.
  2. Click "See it in action" — page does not move.
- **Fix:** Point "See it in action" at a 30-second clip or screenshot sequence of a note being written on one device and found on another.

### 339aaa6d4d73 — Pricing page explains cost in undefined terms — workspace type and sync topology
- **Severity:** P2
- **So what:** The one sentence explaining price used terms the visitor did not have; they gave up on cost at 02:30.
- **Framework tags:** jargon
- **Flow:** shape_3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Copy: "Pricing depends on your workspace type and sync topology."
  - "What a 'workspace type' is" listed in evaluator Q4.
  - Abandonment itself was driven by no numbers (other lens); the jargon removed the only explanation.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/session.log:19`
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the line under the plan cards.
- **Fix:** Replace the line with what actually changes the price in visitor terms (number of people, devices, storage) — or delete it.

### 84573557e128 — Mobile fold clips the headline and subhead off the right edge at 390px
- **Severity:** P2
- **So what:** On a phone the only words that might explain the product are cut mid-word; the fold reads as broken.
- **Framework tags:** what, fold
- **Flow:** shape_1
- **Locator:** /index.html h1 @390px
- **Personas hit:** sceptic
- **Observed:**
  - H1 renders as "Your thoughts, everywh…"; subhead ends "zero-kno…" and "lost or e…".
  - Nav "About" also clipped; hero image overflows the right edge.
  - Sceptic did not comment on it; `understood_what: false`.
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:5`
- **Repro:**
  1. Open `/` at 390×844 (iPhone 13).
  2. Observe H1 and subhead overflow.
- **Fix:** Let the H1 and subhead wrap at narrow widths (remove fixed width / nowrap on `.hero`) and re-check at 390px.

### ef045bad6ab2 — How it works calls the same thing a card, a block, the graph and the vault, defining none
- **Severity:** P2
- **So what:** The section meant to explain the product added four nouns and left the visitor unsure what they would actually write.
- **Framework tags:** jargon, what
- **Flow:** shape_2
- **Locator:** /index.html #how
- **Personas hit:** evaluator
- **Observed:**
  - "Write a card. It joins the graph instantly." / "Blocks flow between devices through the vault."
  - Evaluator asked whether cards and blocks differ at 01:10.
  - Interest died 15 s later, at 01:25 (`point_of_lost_interest`), on the testimonials below.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14` · `persona-evaluator/timeline.json` shape_v2
  > "The cards say 'card', the sync one says 'blocks'. Are those different things?"
- **Repro:**
  1. Open `/`; scroll to "How it works".
  2. Read the three cards.
- **Fix:** Use one word — "note" — across all three cards and drop "graph", "blocks" and "vault" from this section.

### 19db056086f8 — Features nav link returns a 404, removing the page meant to explain the product
- **Severity:** P2
- **So what:** A visitor who went looking for what Nimbus does hit a dead end at 03:30.
- **Framework tags:** placement, what
- **Flow:** shape_3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - Nav "Features" → 404 error page.
  - Crawl records `/features.html` status 404.
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `crawl/index.json`
  > "Features in the nav goes to a 404."
- **Repro:**
  1. Open `/`.
  2. Click "Features" in the nav.
- **Fix:** Publish `/features.html` with a plain-language list of what the product does, or remove the nav item until it exists.

### c625ed222352 — Hero visual is two abstract circles that show nothing of the product
- **Severity:** P3
- **So what:** The largest element on the fold carries no information; on mobile it fills the screen.
- **Framework tags:** what, fold
- **Flow:** shape_1
- **Locator:** /index.html .hero img
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero image is two overlapping purple circles, `alt=""`.
  - Personas described it only as "A purple blob picture" / "a purple picture that takes the whole screen".
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:5` · `persona-sceptic/session.log:5`
- **Repro:**
  1. Open `/`; look at the hero image.
- **Fix:** Replace the circles with a real screenshot of a note open on laptop and phone side by side.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Hero image caption text ("…hero.svg — a real capture serves assets/generated/hero.png…") visible in both fold screenshots — appears to be a fixture placeholder; no persona reacted, cannot confirm a real visitor sees it.
- Evaluator log says the 404 read "That page does not exist."; screenshot shows a generic server error page — wording of the real 404 unconfirmed.

## For other lenses
- No prices on any plan; "Contact sales" routes to a seven-field form with required phone — conversion.
- Anonymous testimonials ("— a happy customer", "— a user", "— anonymous") — trust.
- Cookie bar "We use no tracking cookies on this site." vs privacy page and third-party analytics script — trust / technical.
- Newsletter box visually outweighs the hero CTA — conversion.
- `/features.html` 404 and broken JSON-LD `"price": }` in landing head — technical / seo.
- Meta description repeats "bi-directional sync graph with a zero-knowledge vault" — seo / aeo.

## Coverage gaps
- Sceptic (mobile) never scrolled the landing page body or opened `/pricing.html`; mobile rendering of "How it works" unseen.
- `/app/login.html` not reached (auth wall — not reported).
- Only two inferred personas; no individual-user persona tested the "who" axis.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00-landing, 01-scrolled, 02-pricing, 03-demo-form, 04-features-404, 05-about, 06-privacy · sceptic 00-landing, 01-privacy, 02-about
