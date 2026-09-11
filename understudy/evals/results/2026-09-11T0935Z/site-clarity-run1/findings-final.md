# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: could a first-time visitor say what this is, who it is for, and what to do next — and how long it took
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED (`persona_mode: generic`); findings rest on personas the capture invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 5822d5e41655 — Neither persona could say what the product does; both guessed it from the brand name
- **Severity:** P0
- **So what:** Every later judgement — price, trust, next step — was made by two visitors who never found out what they were looking at.
- **Framework tags:** what, time-to-comprehension
- **Flow:** shape_v1
- **Locator:** /index.html hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` and `understood_what: false` for both personas; `guessed: true` for both.
  - The word "notes" appears on the fold only in the logo; the headline is "Your thoughts, everywhere."
  - The evaluator still could not describe the product after 5:45 of reading five pages.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json` · `session.log:6` · `session.log:28`
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said."
- **Repro:**
  1. Open `http://localhost:8765/` logged out at 1440×900.
  2. Read only what is above the fold and state what the company sells.
  3. Note that no word on the fold names the product category.
- **Fix:** Replace the hero H1 with a sentence that names the category and the job — e.g. "Notes that sync across every device and never lose a thing" — and keep "Your thoughts, everywhere." as the strapline beneath it.

### f2ef631e4075 — The fold's only explanation is two terms neither persona could define
- **Severity:** P1
- **So what:** The single sentence carrying the value proposition transmits nothing, so the visitor has to reconstruct the product from the brand name.
- **Framework tags:** what, jargon
- **Flow:** shape_v1
- **Locator:** /index.html hero subhead
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - The evaluator could define neither term and moved on with an assumption at 00:18.
  - "What is a sync graph?" is logged as an unanswered question at the end of a 6.5-minute session.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `session.log:10` · `persona-evaluator/findings-raw.json` · `persona-evaluator/timeline.json`
  > "'bi-directional sync graph', 'zero-knowledge vault' — I don't know what either means."
- **Repro:**
  1. Open `http://localhost:8765/`.
  2. Read the paragraph under the H1.
  3. Ask what a "sync graph" is; the site never defines it on any page.
- **Fix:** Rewrite the hero paragraph in the About FAQ's plain language — every note stored on your device first, synced when you reconnect, encrypted so only you can read it.

### bc120b0122b1 — The home page names no audience, so both personas answered "who is it for" with a guess
- **Severity:** P1
- **So what:** A visitor who cannot place themselves on the page has no reason to read the rest of it.
- **Framework tags:** who
- **Flow:** shape_v1
- **Locator:** /index.html hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` for both personas.
  - The only audience signal on the home page is the section heading "Loved by teams", 01:25 into the scroll.
  - The explicit audience statements — "For individuals." and "For growing teams." — are on `/pricing.html`, one click away.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/02-pricing.png` · `session.log:7` · `persona-sceptic/timeline.json`
  > "I can't tell. The top of the page names nobody. \"Loved by teams\" lower down suggests teams. Maybe me, maybe not."
- **Repro:**
  1. Open the home page and look for any statement of who the product is for.
  2. Find only "Loved by teams" mid-page.
  3. Open Pricing and find "For individuals." and "For growing teams." on the cards.
- **Fix:** Put the audience in the hero — "for individuals and small teams" — and move the Starter/Team one-liners from the pricing cards into the home page's "How it works" section.

### 3c4469c8992f — At 390px the headline and the explanatory sentence are cut off at the right edge
- **Severity:** P1
- **So what:** The phone visitor never sees the end of either line, so the page's only two explanatory strings arrive incomplete.
- **Framework tags:** what, fold, mobile
- **Flow:** shape_v1
- **Locator:** /index.html hero at 390px
- **Personas hit:** sceptic
- **Observed:**
  - At the sceptic's verified 390×844 viewport the H1 renders as "Your thoughts, everywh…" with the rest off-screen.
  - The subhead is clipped on both lines ("a zero-kno…", "lost or e…"), as is the nav ("Abo…").
  - The independent measurement capture at the same viewport reproduces the clipping.
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `measure/screenshots/index-mobile.png` · `measure/index-mobile.json` · `session.log:5`
  > "Headline \"Your thoughts, everywhere.\" and a purple picture that takes the whole screen."
- **Repro:**
  1. Open `http://localhost:8765/` at 390×844.
  2. Observe the H1 and the paragraph below it truncated at the right edge without wrapping.
- **Fix:** Constrain the hero and header to the viewport width (`max-width: 100%`, wrapping H1) so the headline and subhead wrap instead of overflowing at 390px.

### e6a497c507dd — The site's only concrete, jargon-free sentences sit on the About page, four minutes in
- **Severity:** P1
- **So what:** The copy that would have answered the visitors' questions exists, and neither persona met it until after they had decided to leave.
- **Framework tags:** what, placement
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` answers offline use, export and data location in plain words; the home page answers none of them.
  - The evaluator reached it at 03:50, after the pricing dead end and the 404.
  - The sceptic found the data-location answer at 01:50 on About, having gone to Privacy for it.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `session.log:25` · `persona-sceptic/session.log:12`
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Read the home page and list what you learned about the product.
  2. Open `/about.html` and read the FAQ.
  3. Compare: the specific claims exist only on the second page.
- **Fix:** Lift the three About FAQ answers onto the home page as a "Questions" block below "How it works", and link it from the hero.

### 2985e7c15d1e — The home page calls the same object a card, a block and a graph
- **Severity:** P2
- **So what:** The visitor cannot tell whether Nimbus has one thing or three, so the "How it works" section fails to build a model.
- **Framework tags:** what, vocabulary
- **Flow:** shape_v2
- **Locator:** /index.html#how
- **Personas hit:** evaluator
- **Observed:**
  - "Capture" says "Write a card. It joins the graph instantly."; "Sync" says "Blocks flow between devices through the vault."
  - The evaluator asked, at 01:10, whether cards and blocks are different things; the site never says.
  - None of "card", "block", "graph" or "vault" is defined anywhere on the site.
- **Evidence:** `persona-evaluator/findings-raw.json` · `session.log:14` · `crawl/html/1-index.html`
  > "The cards say \"card\", the sync one says \"blocks\". Are those different things?"
- **Repro:**
  1. Open the home page and scroll to "How it works".
  2. Read the three cards in order and note three different names for the unit of content.
- **Fix:** Pick one noun for the unit of content — "note" — and use it in all three "How it works" cards.

### af7278a7e0e0 — Price is explained by "workspace type and sync topology", which the visitor cannot identify for themselves
- **Severity:** P2
- **So what:** The one sentence offered instead of a number asks the visitor a question about themselves they have no way to answer.
- **Framework tags:** what, jargon
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - The pricing page's only explanatory line is "Pricing depends on your workspace type and sync topology."
  - The evaluator did not know what a workspace type was and had not got one.
  - "What is a workspace type?" remains in the unanswered list at session end.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `session.log:18` · `persona-evaluator/timeline.json`
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the line beneath the three plan cards.
  3. Try to determine your own workspace type; nothing on the site defines one.
- **Fix:** Replace that line with what actually varies the price in plain terms — number of people and storage — or delete it.

### ebc0c93ad872 — The newsletter box outshouts the only product action, leaving the next step ambiguous
- **Severity:** P2
- **So what:** The loudest thing on the page asks for an email address rather than showing the product, so the visitor cannot tell what the site wants.
- **Framework tags:** next-step
- **Flow:** shape_v1
- **Locator:** /index.html newsletter block
- **Personas hit:** evaluator
- **Observed:**
  - The fold carries one outlined link, "See it in action"; the newsletter block below it is a large filled panel.
  - `understood_next_step: false` for the evaluator, recorded at 00:11 before any click.
  - The evaluator's debrief answer to "what would you do next" is "Nothing."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `session.log:8` · `persona-evaluator/timeline.json` · `crawl/html/1-index.html`
  > "There's a small outlined \"See it in action\" button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open the home page at 1440×900.
  2. Compare the visual weight of "See it in action" with the newsletter panel beneath the hero.
- **Fix:** Make "See it in action" the filled primary button, and demote the newsletter block to a single line in the footer.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "How it works" and "Loved by teams" sections may read differently at 390px — the sceptic never scrolled them and `01-scrolled.png` was captured blank.
- Whether a clearer explanation exists on `/features.html` — the page 404s, so no copy was ever seen.

## For other lenses
- Every plan says "Contact sales"; no price anywhere and the demo form requires a phone number — `conversion`.
- Cookie bar says "We use no tracking cookies on this site." while the privacy page names cookies and unnamed partners — `trust`.
- All three testimonials are unattributed ("— a happy customer", "— a user", "— anonymous") — `trust`.
- "See it in action" is an `href="#"` and does nothing; `nimbusBootstrap is not defined` on load; Features 404s from the nav — `technical`.

## Coverage gaps
- `/features.html` never seen by either persona (404).
- The sceptic never scrolled the home page body; mobile comprehension is judged on the fold only.
- `persona-evaluator/screenshots/01-scrolled.png` is blank, so the mid-page sections were scored from `session.log` and `crawl/html/1-index.html`, not from an image.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/` (7) · `persona-sceptic/screenshots/` (3) · `measure/screenshots/` (4)
