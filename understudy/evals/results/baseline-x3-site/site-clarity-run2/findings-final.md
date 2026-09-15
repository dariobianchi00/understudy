# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: Clarity — what / who / next-step comprehension, time-to-comprehension, point of lost interest, undefined vocabulary
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (evaluator on desktop 1440×900, sceptic on iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Landing-page hero carries a leaked placeholder caption in every capture; treated as a fixture artefact, not scored

---

## Findings

### 50c14d12de62 — Headline never says what the product is; both visitors guessed from the name
- **Severity:** P1
- **So what:** Two of two visitors left without the site ever telling them what Nimbus Notes is; a confident visitor cannot recommend or buy what they cannot describe.
- **Framework tags:** what-axis, time-to-comprehension
- **Flow:** shape_v1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Fold shows "Your thoughts, everywhere." and an abstract image; no noun for the product anywhere above the fold.
  - `timeline.json` → `shape_v1.time_to_comprehension_seconds: null`, `understood_what: false`, `guessed: true` for both personas.
  - Both Q1 debrief answers credit the brand name or a friend, not the page.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-sceptic/session.log:6` · `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said."
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page."
- **Repro:**
  1. Open `/index.html` cold in a fresh context at 1440×900 or 390×844.
  2. Without scrolling, try to state what the product does using only on-screen words.
- **Fix:** Replace the hero headline and subhead with one sentence naming the category and outcome, e.g. "A notes app that keeps every note on every device — private by default."

### 8e030a76b0ac — The only path to seeing the product, See it in action, does nothing
- **Severity:** P1
- **So what:** The single element that could resolve "what is this" is dead, so the promise that brought both visitors ("remembers everything") is never shown; the sceptic left on it.
- **Framework tags:** next-step-axis, dead-end
- **Flow:** shape_v2
- **Locator:** /index.html .hero cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator clicked "See it in action" twice at 00:40; page did not move.
  - Sceptic tapped it at 02:20 wanting to "see it remember something"; nothing happened.
  - No other element on `/index.html` shows the product working.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/persona-debrief.md`
  > "Clicked 'See it in action'. Nothing happened. The page didn't move. Clicked again. Still nothing."
  > "nothing on the site shows it remembering anything; the button that might have doesn't work."
- **Repro:**
  1. Open `/index.html`; dismiss the cookie bar.
  2. Click "See it in action" in the hero.
- **Fix:** Make "See it in action" open a 30-second product clip or scroll to a real screenshot of a note syncing between two devices; until that exists, remove the button.

### d286141b81ca — Features nav link returns a 404 where the product explanation should be
- **Severity:** P1
- **So what:** The visitor who still could not say what the product does went to the one nav item promising an answer and got "File not found"; comprehension never recovered.
- **Framework tags:** what-axis, dead-end
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - Nav item "Features" is present on every page; clicking it at 03:30 rendered a bare server 404 ("Error code: 404 · Message: File not found.").
  - No product description page exists anywhere else in the nav.
  - Sceptic never attempted it; severity would be ambiguous for a visitor who never tries — chose the higher.
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `persona-evaluator/findings-raw.json`
  > "Clicked "Features" in the nav. Got a 404 page: "That page does not exist.""
- **Repro:**
  1. Open `/index.html`.
  2. Click "Features" in the top nav.
- **Fix:** Ship `/features.html` with three plain-language sections (capture, sync, remember) and screenshots, or remove "Features" from the nav until it exists.

### 5a5cec370596 — Landing page never says who the product is for
- **Severity:** P2
- **So what:** Both visitors could not tell whether this is for them or their team, so neither could decide whether to keep reading; the only hint ("Loved by teams") is below the fold and contradicted by Pricing ("For individuals").
- **Framework tags:** who-axis
- **Flow:** shape_v1
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `shape_v1.understood_who: false` for both personas.
  - Above the fold names no audience; "Loved by teams" appears only after scrolling (`01-scrolled.png`).
  - `/pricing.html` heading "Plans for every team" with a Starter card "For individuals." — the audience is stated in two conflicting places, neither on the landing fold.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6` · `persona-evaluator/persona-debrief.md`
  > "I can't tell. The top of the page names nobody. "Loved by teams" lower down suggests teams. Maybe me, maybe not."
  > "The page doesn't say. Possibly me."
- **Repro:**
  1. Open `/index.html`; do not scroll.
  2. Try to answer "who is this for" from on-screen words.
- **Fix:** Add one audience line under the headline ("For individuals and small teams who work across laptop and phone") and use the same wording on `/pricing.html`.

### ae4f9f37618a — Hero subhead is jargon the visitor cannot define
- **Severity:** P2
- **So what:** The only explanatory sentence above the fold — "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed." — was read and not understood, so the fold explains nothing.
- **Framework tags:** what-axis, jargon
- **Flow:** shape_v1
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator at 00:18: could not define "bi-directional sync graph" or "zero-knowledge vault"; fell back to "I'll assume it syncs".
  - Sceptic at 00:08 answered "Notes, I think" after reading the same fold; no term from the subhead appears in their answer.
  - Both terms recur in `questions_unanswered` ("What is a sync graph?").
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` · `persona-evaluator/timeline.json`
  > ""bi-directional sync graph with a zero-knowledge vault" — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open `/index.html` at 1440×900.
  2. Read the grey line under the headline.
- **Fix:** Rewrite the subhead in plain words — "Every note syncs between your laptop and phone, and only you can read them" — and move the vault/graph terms to `/features.html` with definitions.

### beb91f02fa77 — Headline and subhead clip off-screen at phone width
- **Severity:** P2
- **So what:** At 390px the sceptic met "Your thoughts, everywh" and "…with a zero-kno / …ever lost or e" — the fold's only explanatory text is physically unreadable on the device they used.
- **Framework tags:** what-axis, fold-at-viewport
- **Flow:** shape_v1
- **Locator:** /index.html @390px
- **Personas hit:** sceptic
- **Observed:**
  - Sceptic's `00-landing.png` at verified 390×844 shows the headline, subhead and nav ("Abo") cut at the right edge; the page overflows horizontally.
  - Independent measurement capture `measure/screenshots/index-mobile.png` shows the same clipping.
  - Persona did not remark on it — they answered "Notes, I think" from the name and moved on; the defect is visible in the artifact, not in the log.
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `measure/screenshots/index-mobile.png` · `persona-sceptic/timeline.json`
- **Repro:**
  1. Open `/index.html` at 390×844 (iPhone 13).
  2. Observe the headline and subhead are cut mid-word at the right viewport edge.
- **Fix:** Constrain the hero and nav to `max-width: 100vw` with wrapping text at ≤ 430px, and verify the fold on a phone before release.

### b7877d9809cc — Newsletter box outweighs the product CTA so the next step reads as subscribe
- **Severity:** P2
- **So what:** Asked "what does it want me to do", the evaluator's answer was the newsletter, not the product — the page's visual hierarchy tells the visitor the wrong next step.
- **Framework tags:** next-step-axis, hierarchy
- **Flow:** shape_v1
- **Locator:** /index.html newsletter
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is a small outlined button; directly beneath it a full-width solid purple block reads "Get the Nimbus newsletter" with a "Subscribe" button.
  - Evaluator at 00:11 and 01:10: the newsletter box is "bigger and brighter than the button that shows the product".
  - Sceptic at 00:08 lists both, describing the newsletter as "a big purple newsletter box".
  - `shape_v1.understood_next_step: false` for the evaluator.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-evaluator/findings-raw.json` · `persona-sceptic/session.log:6`
  > "There's a small outlined "See it in action" button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/index.html` at 1440×900; dismiss the cookie bar.
  2. Compare the weight of "See it in action" against the purple newsletter block beneath it.
- **Fix:** Make "See it in action" the solid primary button in the hero and move the newsletter block to the footer as a single-line form.

### cef320af6057 — Hero image shows abstract shapes, not the product
- **Severity:** P2
- **So what:** The largest element on the fold — the whole first screen on a phone — carries zero information about what the product is, wasting the visitor's first glance.
- **Framework tags:** what-axis, fold
- **Flow:** shape_v1
- **Locator:** /index.html .hero img
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero graphic is two overlapping lavender circles on a pale panel; no interface, notes or devices depicted.
  - Evaluator: "A purple blob picture." Sceptic: "a purple picture that takes the whole screen."
  - Neither persona's V1 answers reference the image.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:5` · `persona-sceptic/session.log:5`
  > "Headline "Your thoughts, everywhere." and a purple picture that takes the whole screen."
- **Repro:**
  1. Open `/index.html` at 390×844.
  2. Note the hero image fills the viewport below the subhead with no product content.
- **Fix:** Replace the hero graphic with a real screenshot of a note visible on a laptop and a phone at once.

### d0f5755bbc8c — The clearest plain-English answers live on About, two clicks from the landing page
- **Severity:** P2
- **So what:** The only sentences either visitor called "actual answers" — works offline, exports Markdown, data in Frankfurt — are on `/about.html`, reached by the evaluator at 04:20 and the sceptic at 01:50; the landing page never uses them.
- **Framework tags:** placement, what-axis
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` FAQ: "Yes. Nimbus Notes stores every note on your device first and syncs when a connection returns." — the plainest product description on the site.
  - Evaluator: "Those are actual answers. Why isn't this on the home page?"
  - Sceptic: the Frankfurt answer "is on the About page, not the Privacy page."
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12` · `persona-evaluator/timeline.json`
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/index.html`; read every sentence.
  2. Open `/about.html`; compare the FAQ answers with the landing copy.
- **Fix:** Lift the three FAQ answers onto `/index.html` as the "How it works" copy, and link "Where is my data stored?" from the privacy page.

### 159b0dea8262 — Pricing note workspace type and sync topology is undefined jargon
- **Severity:** P2
- **So what:** The one sentence explaining why there is no price — "Pricing depends on your workspace type and sync topology." — uses two terms the visitor cannot map to themselves, so it reads as evasion rather than explanation.
- **Framework tags:** jargon
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Evaluator at 02:10: "I don't know what my workspace type is. I haven't got one."
  - "What is a workspace type?" recorded in `questions_unanswered`.
  - Neither term is defined anywhere in the five pages captured.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/timeline.json` · `persona-evaluator/persona-debrief.md`
  > ""Pricing depends on your workspace type and sync topology." I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the grey line beneath the three plan cards.
- **Fix:** Replace the note with the two or three concrete factors in the visitor's words ("number of people, and whether you need EU-only storage").

### a22e07cb0c99 — How it works uses card, blocks and graph without defining them
- **Severity:** P3
- **So what:** The section meant to explain the product introduces three new nouns — "card", "blocks", "graph" — and the evaluator could not tell whether they were the same thing.
- **Framework tags:** jargon
- **Flow:** shape_v2
- **Locator:** /index.html How it works
- **Personas hit:** evaluator
- **Observed:**
  - Capture card: "Write a card. It joins the graph instantly." Sync card: "Blocks flow between devices through the vault."
  - Evaluator at 01:10: "The cards say "card", the sync one says "blocks". Are those different things?"
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say "card", the sync one says "blocks". Are those different things?"
- **Repro:**
  1. Open `/index.html`; scroll to "How it works".
  2. Read the three cards in sequence.
- **Fix:** Use one noun — "note" — in all three cards, and drop "graph" and "vault" from this section.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The sceptic may have found the phone fold unreadable — no log line or debrief quote says so; the clipping finding rests on the screenshot alone.
- "Log in" as the only solid nav button may signal "existing customers only" to a new visitor — neither persona remarked on it.

## For other lenses
- No price on any plan; "Contact sales" → seven-field demo form with required phone — conversion, objectives-scorer
- Cookie bar "We use no tracking cookies" contradicts privacy page cookie/partner wording — trust
- Anonymous testimonials ("— a happy customer", "— a user", "— anonymous") — trust
- "See it in action" click does nothing; "Features" nav → server 404; hero image renders a leaked placeholder caption — bugs, technical
- Horizontal overflow at 390px — technical

## Coverage gaps
- `/features.html` never rendered (404); no persona saw a features page
- No logged-in or trial surface reached; conversion goal "start a free trial" has no entry point on any captured page
- Sceptic did not open `/pricing.html`; pricing jargon finding rests on one persona

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00-landing.png … 06-privacy.png`, `persona-sceptic/screenshots/00-landing.png … 02-about.png`
