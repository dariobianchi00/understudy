# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: comprehension on three axes (what / who / next step), timed against the visit shapes
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### e7eeba1b1a8c — Hero never says what the product is; both visitors guessed notes app from the brand name
- **Severity:** P1
- **So what:** Neither visitor ever understood the product; the evaluator left at 06:30 still unable to say what it does beyond "notes that sync".
- **Framework tags:** what, C-COMPREHENSION-NEVER
- **Flow:** shape_1
- **Locator:** /index.html .hero h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Headline "Your thoughts, everywhere." names no product category, task or outcome; hero image is two abstract purple circles
  - `time_to_comprehension_seconds: null` and `guessed: true` for both personas
  - Both Q1 answers credit the brand name, not the page, for "notes app"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:14` · `persona-evaluator/session.log:28` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." (evaluator, Q1)
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." (sceptic, Q1)
- **Repro:**
  1. Open `/index.html` at 1440×900 or 390×844
  2. Read only the fold; try to state what the product does without using the word "Notes" from the logo
- **Fix:** Replace the H1 with a literal one-line description, e.g. "Notes that sync between your laptop and phone, and remember everything".

### b7f071ad31bd — Hero subhead explains the product in terms the visitor cannot define
- **Severity:** P2
- **So what:** The only explanatory sentence on the fold explained nothing; the evaluator had to "assume it syncs".
- **Framework tags:** what, C-JARGON
- **Flow:** shape_1
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator could define neither "sync graph" nor "zero-knowledge vault"; both appear in Q4 unanswered list
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/persona-debrief.md` Q4
  > "\"bi-directional sync graph with a zero-knowledge vault\" — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open `/index.html`
  2. Read the grey subhead under the H1
- **Fix:** Rewrite the subhead in user outcomes ("Write on any device, see it on all of them; only you can read it") and drop "sync graph" and "zero-knowledge vault".

### 6bb87b2c6395 — Hero headline and subhead are cut off mid-word at 390px on iPhone
- **Severity:** P2
- **So what:** On mobile the fold shows "Your thoughts, everywh" and half-sentences, so the little explanation there is is not even fully visible.
- **Framework tags:** what, C-FOLD-MOBILE
- **Flow:** shape_1
- **Locator:** /index.html .hero
- **Personas hit:** sceptic
- **Observed:**
  - H1 cropped at the right edge: "Your thoughts, everywh"
  - Subhead lines end "zero-kno" and "lost or e"; nav "About" also cropped to "Abo"
  - Hero image overflows the right edge; cookie bar covers the bottom of the fold
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:5` · `persona-sceptic/timeline.json` viewport 390×844
- **Repro:**
  1. Open `/index.html` at 390×844 (iPhone 13)
  2. Look at the H1 and subhead without scrolling horizontally
- **Fix:** Make the hero text and image wrap to the viewport width on mobile (no fixed widths, allow H1 to wrap).

### 77cbad1703f2 — Nothing above the fold names who the product is for
- **Severity:** P2
- **So what:** The evaluator came to judge it for their team and could not tell if it was for individuals or teams.
- **Framework tags:** who
- **Flow:** shape_1
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Fold names no audience; first audience hint is "Loved by teams" several screens down
  - "For individuals." / "For growing teams." appear only on the pricing page
  - `understood_who: false` for both personas
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:9` · `persona-sceptic/session.log:6`
  > "I can't tell. The top of the page names nobody. \"Loved by teams\" lower down suggests teams. Maybe me, maybe not." (evaluator, Q2)
  > "The page doesn't say. Possibly me." (sceptic, Q2)
- **Repro:**
  1. Open `/index.html`
  2. Look for any mention of individuals, teams or a role in the first viewport
- **Fix:** Add an audience line to the hero, e.g. "For individuals and small teams who switch between laptop and phone".

### 901eba7c9d31 — The promise that brought both visitors sits below the newsletter, not in the hero
- **Severity:** P2
- **So what:** The one sentence that matched why they came is three sections down; the mobile visitor never scrolled to it.
- **Framework tags:** what, C-PLACEMENT, C-PROMISE
- **Flow:** shape_2
- **Locator:** /index.html #how
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "Nimbus remembers everything so you never start from zero." appears only in the third "How it works" card, under the newsletter box
  - Evaluator found it at 00:55; sceptic saw 1 section and left the home page at 00:30
  - Both Q6 answers: promise not matched by the page
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:13` · `persona-sceptic/session.log:8` · `persona-sceptic/timeline.json` shape_v2.sections_seen
  > "Close but off — the line is on the page, but nothing shows me it happening, and the page around it is about vaults and graphs." (evaluator, Q6)
- **Repro:**
  1. Open `/index.html`
  2. Scroll past the hero and newsletter to "How it works"
- **Fix:** Move "Nimbus remembers everything so you never start from zero" into the hero, above or in place of the current subhead.

### 88a61aef96ac — See it in action, the only way to see the product, does nothing when clicked
- **Severity:** P2
- **So what:** Both visitors tried to see the product to understand it and got nothing; the evaluator lost the next-step axis entirely.
- **Framework tags:** next step, what
- **Flow:** shape_2
- **Locator:** /index.html .hero a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is a small outlined button; the newsletter box below is larger and brighter
  - Clicked twice (evaluator, 00:40) and tapped (sceptic, 02:20): page did not move
  - Site shows no screenshot, video or example of the product anywhere
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:11` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `crawl/html/1-index.html:12`
  > "\"It remembers everything.\" No — nothing on the site shows it remembering anything; the button that might have doesn't work." (sceptic, Q6)
- **Repro:**
  1. Open `/index.html`
  2. Click "See it in action"
- **Fix:** Point "See it in action" at a short product video or screenshot tour, and make it the dominant hero button.

### 9bc2ad4b1522 — The clearest plain-language explanation of the product is buried in the About page FAQ
- **Severity:** P2
- **So what:** The answers that made the product concrete (offline, export, Frankfurt) were found only by visitors who went looking two clicks deep.
- **Framework tags:** what, C-PLACEMENT
- **Flow:** shape_3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Nimbus Notes stores every note on your device first and syncs when a connection returns."
  - Also: "Settings → Export produces a folder of Markdown files" and "In the EU (Frankfurt) by default."
  - None of this appears on the home page
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/screenshots/02-about.png` · `persona-sceptic/session.log:12`
  > "Those are actual answers. Why isn't this on the home page?" (evaluator)
- **Repro:**
  1. Open `/about.html`
  2. Read the "Frequently asked questions" section; compare with `/index.html`
- **Fix:** Copy the About FAQ's offline, export and data-location answers onto the home page under the hero.

### 78727204633c — Pricing page explains plans with undefined terms workspace type and sync topology
- **Severity:** P2
- **So what:** The only explanation of how plans differ uses words the visitor could not map to themselves.
- **Framework tags:** who, C-JARGON
- **Flow:** shape_3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Footnote reads "Pricing depends on your workspace type and sync topology."
  - Neither term is defined anywhere the persona visited
  - "What is a workspace type?" listed in `questions_unanswered`
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/timeline.json` shape_v3.questions_unanswered
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`
  2. Read the line beneath the three plan cards
- **Fix:** Replace the footnote with a plain line naming what changes the plan (e.g. number of users, devices) and drop "workspace type" and "sync topology".

### 57e27b290601 — How it works calls the same object a card, a block and a note
- **Severity:** P3
- **So what:** The visitor stopped to ask whether these were different things in the section meant to explain the product.
- **Framework tags:** what, C-VOCABULARY
- **Flow:** shape_2
- **Locator:** /index.html #how
- **Personas hit:** evaluator
- **Observed:**
  - "Write a card. It joins the graph instantly." then "Blocks flow between devices through the vault."
  - Brand and testimonials call them notes
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say \"card\", the sync one says \"blocks\". Are those different things?"
- **Repro:**
  1. Open `/index.html`
  2. Read the three "How it works" cards
- **Fix:** Use "note" consistently across the How it works cards.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Hero image shows stray caption text ("…a real capture serves assets/generated/hero.png…") — visible in both `00-landing.png`, but no persona reacted; looks like a fixture placeholder, not a clarity effect.

## For other lenses
- All three plans say "Contact sales" with no price; evaluator gave up on the objective at 02:30 — conversion
- "Contact sales" routes to a seven-field demo form with phone required — conversion
- "Features" nav link returns 404 — technical
- Anonymous testimonials ("— a happy customer", "— anonymous"); evaluator's point of lost interest 01:25 — trust
- Cookie bar "We use no tracking cookies" contradicts privacy page; sceptic left over it — trust

## Coverage gaps
- Sceptic (mobile) never scrolled the home page past the hero; mobile rendering of "How it works" untested by a persona
- `/features.html` never rendered (404), so any explanation there was not seen
- Generic, inferred personas only

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06, sceptic 00–02
