# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the three comprehension axes — **what** / **who** / **what next** — scored against reality, plus time-to-comprehension
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: **generic — ⚠ INFERRED**, not researched
- Scoring model: opus
- Tags: `C-WHAT` `C-WHO` `C-NEXT` `C-TTC` (time to comprehension) `C-JARGON` `C-PLACE` (placement) `C-FOLD` `C-CONSIST`
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### f93791b1efec — Neither visitor could say what Nimbus Notes does from the page; both guessed from the brand name
- **Severity:** P0
- **So what:** The site's only job above the fold went undone for both visitors, and neither recovered it in the whole session.
- **Framework tags:** C-WHAT, C-TTC
- **Flow:** shape_v1
- **Locator:** /index.html div.hero h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` and `understood_what: false` in both timelines; `guessed: true` for both.
  - Both Q1 answers name the source of the guess as the brand name or a friend — not the page.
  - The fold says "Your thoughts, everywhere." The word "notes" appears only in the logo.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json` · `persona-evaluator/session.log:9` · `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said."
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page."
- **Repro:**
  1. Open `http://localhost:8765/` logged out at 1440x900.
  2. Read only what is above the fold; do not scroll.
  3. Try to state what the company sells without using the logo.
- **Fix:** Replace the H1 "Your thoughts, everywhere." with a plain-language line that names the product category and the job — e.g. "Notes that stay in sync on every device, and work offline."
- **Note:** Scored P0 rather than P1 because comprehension is the whole flow this lens measures and neither persona completed it; a reader who counts their rough "notes app" guess as a pass can downgrade it to P1.

### 2d3dfadd8473 — The fold's only call to action, “See it in action”, does nothing when clicked
- **Severity:** P1
- **So what:** The page's own answer to "what do I do next" is a dead link, and both visitors hit it.
- **Framework tags:** C-NEXT
- **Flow:** shape_v1
- **Locator:** /index.html a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Markup is `<a class="cta" href="#">See it in action</a>` — no target.
  - Evaluator clicked it twice at 00:40; nothing happened.
  - Sceptic tapped it at 02:20 as their route to seeing the product "remember" something, then left at 02:50.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `crawl/html/1-index.html:12`
  > "Clicked 'See it in action'. Nothing happened. The page didn't move. Clicked again. Still nothing."
  > "It remembers everything." No — nothing on the site shows it remembering anything; the button that might have doesn't work."
- **Repro:**
  1. Open the home page.
  2. Click "See it in action".
  3. Observe no navigation, no scroll, no modal.
- **Fix:** Point "See it in action" at a real product demo — a looping capture-and-sync video or an interactive sandbox — and remove `href="#"`.

### 0503cd91ea19 — The clearest description of the product is buried in the About FAQ, two clicks from the fold
- **Severity:** P2
- **So what:** The one sentence that would have answered "what is this" arrived at 04:20 for one visitor and never for the other.
- **Framework tags:** C-PLACE, C-WHAT
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` FAQ says "Nimbus Notes stores every note on your device first and syncs when a connection returns." — the plainest sentence on the site.
  - Evaluator reached it at 04:20, after `point_of_lost_interest` at 01:25, and asked why it was not on the home page.
  - Sceptic left at 02:50; found only the data-location answer there and noted it was on the wrong page.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12` · `persona-evaluator/timeline.json`
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Read the home page top to bottom.
  2. Open `/about.html` and read the FAQ.
  3. Compare which page explains the product.
- **Fix:** Move the three About FAQ answers (offline, export, EU data location) onto the home page directly under the hero, and keep About for the company.

### 75ac9a4381c3 — The hero's only explanatory sentence is built from two terms the visitor could not define
- **Severity:** P2
- **So what:** The single line asked to explain the product spent both its nouns on jargon, so it explained nothing.
- **Framework tags:** C-JARGON, C-WHAT
- **Flow:** shape_v1
- **Locator:** /index.html div.hero p
- **Personas hit:** evaluator
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator could define neither term at 00:18 and substituted a guess: "I'll assume it syncs."
  - Both terms are repeated in the `<meta name="description">`, so search snippets carry the same wording.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` · `crawl/html/1-index.html:11`
  > "'bi-directional sync graph with a zero-knowledge vault' — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open the home page.
  2. Read the sentence under the H1.
  3. Attempt to state what the product does using only that sentence.
- **Fix:** Rewrite the hero subhead in the user's words — what gets synced, between what, and what happens offline — and move "zero-knowledge" to the privacy section where it is a claim, not an explanation.

### 0000977862fe — The site never says who it is for, and the two places that imply it contradict each other
- **Severity:** P2
- **So what:** Neither visitor could tell whether the product was meant for them, so neither could decide to care.
- **Framework tags:** C-WHO, C-CONSIST
- **Flow:** shape_v2
- **Locator:** /index.html section#proof
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` in both timelines; both Q2 answers say the page does not say.
  - Home page heading is "Loved by teams"; `/pricing.html` opens "Starter — For individuals."
  - "Is it for individuals or teams?" is logged in the evaluator's `questions_unanswered`.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-evaluator/timeline.json` · `persona-sceptic/findings-raw.json`
  > "I can't tell. The top of the page names nobody. 'Loved by teams' lower down suggests teams. Maybe me, maybe not."
- **Repro:**
  1. Read the fold and the "Loved by teams" section.
  2. Open `/pricing.html` and read the Starter card.
  3. Try to decide which one describes you.
- **Fix:** Name the audience in the hero ("For individuals and small teams") and make the pricing tiers say who each is for in the same words.

### 48b798b42f8c — “Features” in the nav — the one page that would explain the product — returns a 404
- **Severity:** P2
- **So what:** The visitor's own attempt to fix their confusion hit a dead end with no route back.
- **Framework tags:** C-WHAT, C-NEXT
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - Evaluator clicked "Features" at 03:30 while still unable to say what the product does.
  - Response is the bare server error page: "Error code: 404 / Message: File not found." No nav, no branding, no way back.
  - `features.html` is linked from the header of every crawled page.
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `crawl/html/1-index.html:6`
  > "Clicked 'Features' in the nav. Got a 404 page: 'That page does not exist.'"
- **Repro:**
  1. Open the home page.
  2. Click "Features" in the header nav.
  3. Observe the unstyled 404.
- **Fix:** Publish `/features.html` with a plain description of what the product does, or remove the nav link until it exists.

### 3aa05e7a00e6 — Pricing explains its missing numbers with “workspace type and sync topology”
- **Severity:** P2
- **So what:** The sentence meant to explain why there is no price used two terms the visitor could not apply to themselves.
- **Framework tags:** C-JARGON
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - `/pricing.html` closes with "Pricing depends on your workspace type and sync topology."
  - Evaluator could not map either term onto anything they had: "I haven't got one."
  - "What is a workspace type?" is logged in `questions_unanswered`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/timeline.json` · `crawl/html/3-pricing.html:16`
  > "'Pricing depends on your workspace type and sync topology.' I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the grey line under the three cards.
  3. Try to work out which workspace type you are.
- **Fix:** Replace that line with the actual variables in plain terms — "Price depends on how many people are on the account" — or state a per-person price.

### 205d65b94683 — At 390px the headline and the explanatory subhead are cut off at the right edge
- **Severity:** P2
- **So what:** The phone visitor was shown half of the only sentence that tries to explain the product.
- **Framework tags:** C-FOLD, C-WHAT
- **Flow:** shape_v1
- **Locator:** /index.html div.hero @390px
- **Personas hit:** sceptic
- **Observed:**
  - H1 renders as "Your thoughts, everywh…"; the subhead lines end "a zero-kno…" and "lost or e…".
  - Nav truncates mid-word at "Abo"; the "Log in" button is off-screen.
  - Reproduced independently in the 390x844 measurement capture, so it is not a screenshot artifact.
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `measure/screenshots/index-mobile.png` · `measure/index-mobile.json` · `persona-sceptic/session.log:5`
  > "On my phone. Landed. Headline 'Your thoughts, everywhere.' and a purple picture that takes the whole screen."
- **Repro:**
  1. Open the home page at a 390x844 viewport.
  2. Do not scroll or zoom.
  3. Observe the H1, subhead and nav clipped at the right edge.
- **Fix:** Constrain `.hero` and `header nav` to the viewport width and allow the H1 and subhead to wrap at 390px.

### 460945532303 — The newsletter box is the loudest element on the page, louder than the product itself
- **Severity:** P2
- **So what:** The brightest thing on the page asks for an email before the visitor knows what the product is.
- **Framework tags:** C-NEXT
- **Flow:** shape_v2
- **Locator:** /index.html div.news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Solid purple newsletter panel sits directly below the hero, above "How it works".
  - The product CTA is a small outlined button; the evaluator named the contrast at 00:11 when asked what the page wanted.
  - Sceptic described the same ordering on mobile at 00:06.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-sceptic/session.log:6` · `crawl/html/1-index.html:15`
  > "There's a small outlined 'See it in action' button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open the home page.
  2. Scroll one screen.
  3. Compare the visual weight of the newsletter panel with the hero CTA.
- **Fix:** Make "See it in action" the solid primary button and move the newsletter signup to the footer.

### e9fdfbb96e49 — Three adjacent cards call the same thing a card, a block and a graph
- **Severity:** P3
- **So what:** The visitor stopped to work out whether three words meant three things.
- **Framework tags:** C-CONSIST, C-JARGON
- **Flow:** shape_v2
- **Locator:** /index.html section#how
- **Personas hit:** evaluator
- **Observed:**
  - "How it works" reads: "Write a card. It joins the graph instantly." / "Blocks flow between devices through the vault." / "Nimbus remembers everything…".
  - Evaluator asked at 01:10 whether cards and blocks were different things, and moved on without an answer.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14` · `crawl/html/1-index.html:18`
  > "The cards say 'card', the sync one says 'blocks'. Are those different things?"
- **Repro:**
  1. Open the home page.
  2. Read the three "How it works" cards in order.
- **Fix:** Pick one noun for the unit of content — "note" — and use it in all three cards.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Whether the mobile clipping caused the sceptic's comprehension failure — they never mentioned the truncation, so the link is unproven.
- Whether the hero image communicates anything — both personas called it "a purple blob"/"a purple picture" with no further reaction; no evidence it helped or hindered comprehension.
- Whether "Loved by teams" was read as an audience statement rather than proof — the evaluator cited it both ways in one session.

## For other lenses
- Three plans, all "Contact sales", no numbers; objective "find out what it costs without giving an email" failed — **conversion**.
- Seven-field demo form with phone required before the product has been seen — **conversion**.
- Cookie bar says "We use no tracking cookies on this site." while `/privacy.html` describes cookies and unnamed partners — **trust**.
- Three anonymous testimonials: "a happy customer", "a user", "anonymous" — **trust**.
- `ReferenceError: nimbusBootstrap is not defined` on load, 3.9 MB hero PNG, 5.8 s LCP on mobile — **technical**.
- `/features.html` is 404 while linked sitewide; `/pricing.html` carries `meta robots=noindex`; truncated JSON-LD `offers.price` — **seo**.

## Coverage gaps
- Sceptic never opened `/pricing.html` or `/features.html` — no mobile evidence for those pages.
- Evaluator's log cites `06-privacy.png` at 04:50 but no such file exists in `persona-evaluator/screenshots/`.
- No tablet viewport tested; no second visit or returning-visitor state.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00-05` · `persona-sceptic/screenshots/00-02` · `measure/screenshots/`
