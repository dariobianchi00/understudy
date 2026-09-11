# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: clarity — could a first-time visitor say what this is, who it is for, and what to do next, and how long did it take
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Flow values: `shape_v1` land · `shape_v2` orient · `shape_v3` evaluate (visit shapes)

---

## Findings

### 0e2fadb02a78 — Landing fold never says what the product is; both personas guessed 'notes' from the name
- **Severity:** P1
- **So what:** Every visitor who does not already know the product leaves with a guess; `time_to_comprehension_seconds` is `null` for both personas.
- **Framework tags:** what-axis, time-to-comprehension
- **Flow:** shape_v1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Fold at 1440×900 shows "Your thoughts, everywhere.", a jargon subhead, an abstract blob image and an outlined button; no sentence says what Nimbus Notes is.
  - Evaluator at 00:06: "Some kind of notes app, from the name. The headline doesn't say." Sceptic at 00:08: "Notes, I think."
  - Both `timeline.json` files: `understood_what: false`, `guessed: true`, `time_to_comprehension_seconds: null`.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1 · `persona-evaluator/persona-debrief.md` Q1 · `persona-sceptic/persona-debrief.md` Q1
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said."
- **Repro:**
  1. Open `/index.html` at 1440×900 or 390×844, logged out.
  2. Without scrolling, try to state what the product is using only the words on screen.
- **Fix:** Replace the hero copy with one plain sentence naming the category and the job — e.g. "A notes app that keeps every note on every device" — above "Your thoughts, everywhere."

### e145f210ba5e — The only 'See it in action' button goes nowhere, so nothing on the site ever shows the product
- **Severity:** P1
- **So what:** The single element that promised to show what the product does is dead; both personas clicked it, saw nothing, and left without ever seeing Nimbus Notes.
- **Framework tags:** next-step-axis, promise-match
- **Flow:** shape_v1
- **Locator:** /index.html .cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator clicked "See it in action" twice at 00:40: "Nothing happened. The page didn't move."
  - Sceptic tapped it at 02:20: "The button does nothing when I tap it." Left at 02:40.
  - Crawl markup: `<a class="cta" href="#">See it in action</a>` — the anchor has no destination.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/persona-debrief.md` Q6 · `crawl/html/1-index.html`
  > "It remembers everything." No — nothing on the site shows it remembering anything; the button that might have doesn't work.
- **Repro:**
  1. Open `/index.html`.
  2. Click "See it in action" in the hero.
  3. Observe no navigation, scroll or modal.
- **Fix:** Point "See it in action" at a real screenshot, short video or product tour section on the landing page, and make it the visually primary button.

### 0eec2f9911d4 — Hero subhead is jargon the visitor cannot parse: 'bi-directional sync graph', 'zero-knowledge vault'
- **Severity:** P2
- **So what:** The one explanatory sentence above the fold is made of terms the visitor cannot define, so it explains nothing and the guess from the name stays a guess.
- **Framework tags:** what-axis, jargon
- **Flow:** shape_v1
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator
- **Observed:**
  - Subhead reads: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator at 00:18: "I don't know what either of those means. I'll assume it syncs."
  - "What is a sync graph?" is in the evaluator's `questions_unanswered` and debrief Q4.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` t=00:18 · `persona-evaluator/persona-debrief.md` Q4
  > "'bi-directional sync graph', 'zero-knowledge vault' — I don't know what either means."
- **Repro:**
  1. Open `/index.html`.
  2. Read the sentence under the headline; try to define "sync graph" and "zero-knowledge vault" from the page.
- **Fix:** Rewrite the subhead in the visitor's words — "syncs between your laptop and phone; only you can read your notes" — and move the technical terms to Features.

### 77a357f2d026 — Landing page never says who the product is for; the answer sits on the pricing cards
- **Severity:** P2
- **So what:** A visitor evaluating for a team cannot tell if this is a personal tool or a team tool, so cannot decide whether to keep reading.
- **Framework tags:** who-axis, placement
- **Flow:** shape_v1
- **Locator:** /index.html .hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator at 00:09: "Who is it for? No idea. Me? Teams?" Sceptic at 00:08: "For who? Doesn't say."
  - Both `timeline.json`: `understood_who: false`. "Is it for individuals or teams?" stays in the evaluator's `questions_unanswered` after 6:30.
  - The only audience statements on the site are the pricing cards: "For individuals." / "For growing teams." — one click away, never on the landing page.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6` · `persona-evaluator/persona-debrief.md` Q2 · `persona-sceptic/persona-debrief.md` Q2
  > "I can't tell. The top of the page names nobody. 'Loved by teams' lower down suggests teams. Maybe me, maybe not."
- **Repro:**
  1. Open `/index.html`; read the fold and the "How it works" section.
  2. Try to name the intended user; note that only `/pricing.html` says "For individuals." / "For growing teams."
- **Fix:** Add an audience line to the hero — "for individuals and small teams" — and reuse the pricing-card wording on the landing page.

### fe44f9d609a6 — The clearest description of the product is on the About page, two clicks from the landing
- **Severity:** P2
- **So what:** The sentences that finally made the product concrete — offline, export, EU data — are on a page most visitors never open; the landing page carries the vague ones.
- **Framework tags:** placement, what-axis
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ states: "stores every note on your device first and syncs when a connection returns", "Export produces a folder of Markdown files", "In the EU (Frankfurt) by default."
  - Evaluator at 04:20: "Those are actual answers. Why isn't this on the home page?"
  - Sceptic reached the Frankfurt answer at 01:50, on About, after finding nothing on Privacy.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/index.html`; note no concrete capability is stated.
  2. Open `/about.html`; read "Frequently asked questions".
- **Fix:** Lift the three About FAQ answers onto the landing page under "How it works", replacing "Blocks flow between devices through the vault."

### 500de2ac5930 — Pricing page explains cost with undefined terms 'workspace type' and 'sync topology'
- **Severity:** P2
- **So what:** The only sentence about how price is set uses two words the visitor cannot map to themselves, so even the shape of the cost is not understood.
- **Framework tags:** jargon, what-axis
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Page footer line: "Pricing depends on your workspace type and sync topology."
  - Evaluator at 02:10: "I don't know what my workspace type is. I haven't got one."
  - "What is a workspace type?" is in `questions_unanswered` and debrief Q4; `price_understood: false`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/timeline.json` shape_v3 · `persona-evaluator/persona-debrief.md` Q4
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the line beneath the three plan cards; try to work out which "workspace type" applies to you.
- **Fix:** Replace the line with the actual variables in plain words — e.g. "Price depends on how many people and how many devices" — or delete it.

### f9ebf22b3987 — Features nav link returns a 404, so the page meant to explain the product does not exist
- **Severity:** P2
- **So what:** A visitor who cannot understand the product from the hero goes to "Features" for the answer and gets an error page instead.
- **Framework tags:** what-axis, dead-end
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - "Features" is the second item in the site nav on every page.
  - Evaluator at 03:30 clicked it and received "Error response / Error code: 404 / Message: File not found."
  - No other page on the site describes features; the visitor is returned to guessing.
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `persona-evaluator/findings-raw.json` t=03:30
  > "Features in the nav goes to a 404."
- **Repro:**
  1. Open `/index.html`.
  2. Click "Features" in the header nav.
- **Fix:** Publish `/features.html` with the About FAQ content and plain-language feature descriptions, or remove "Features" from the nav until it exists.

### 4c8c3e74a4c7 — How it works section uses 'card' and 'blocks' for what may be the same thing
- **Severity:** P3
- **So what:** The section meant to make the product concrete introduces two nouns the visitor cannot reconcile, adding a question instead of answering one.
- **Framework tags:** vocabulary, what-axis
- **Flow:** shape_v2
- **Locator:** /index.html #how
- **Personas hit:** evaluator
- **Observed:**
  - "Capture: Write a card. It joins the graph instantly." then "Sync: Blocks flow between devices through the vault."
  - Evaluator at 01:10: "The cards say 'card', the sync one says 'blocks'. Are those different things?"
- **Evidence:** `persona-evaluator/session.log:14` · `crawl/html/1-index.html`
  > "The cards say "card", the sync one says "blocks". Are those different things?"
- **Repro:**
  1. Open `/index.html`; scroll to "How it works".
  2. Compare the nouns in the "Capture" and "Sync" cards.
- **Fix:** Use one word — "note" — in all three "How it works" cards.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The mobile fold may truncate the headline ("Your thoughts, everywh…") — `persona-sceptic/screenshots/00-landing.png` is 390px wide but shows content clipped at the right edge; unclear if that is the page or the capture, and the sceptic did not remark on it.
- Below-fold landing sections could not be visually verified — `persona-evaluator/screenshots/01-scrolled.png` is blank; "How it works" and "Loved by teams" are cited from `session.log` and crawl markup only.

## For other lenses
- Newsletter box is bigger and brighter than the product CTA (`session.log:8`, `findings-raw.json` t=01:10) — conversion
- Three plans, all "Contact sales", no numbers; seven-field demo form with phone required (`02-pricing.png`, `03-demo-form.png`) — conversion, objectives
- Cookie bar "We use no tracking cookies" contradicts privacy page cookies/partners wording (`06-privacy.png`, `persona-sceptic/screenshots/01-privacy.png`) — trust
- Anonymous testimonials "— a happy customer", "— a user", "— anonymous" (`session.log:15`) — trust
- `/features.html` 404 and `href="#"` CTA — bugs / seo
- `hero.svg` renders a placeholder caption inside the hero image — technical

## Coverage gaps
- `/features.html` never rendered (404).
- `01-scrolled.png` captured blank — below-fold desktop view not visually verified.
- Sceptic never opened Pricing; mobile pricing comprehension untested.
- No auditor-mode exploration; `coverage_depth: standard`.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00–06`, `persona-sceptic/screenshots/00–02`
