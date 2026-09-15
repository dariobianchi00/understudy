# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: comprehension at the fold — what / who / next step, scored against reality, not effort
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### e6e6f92888aa — Neither persona could say what Nimbus Notes does; both guessed from the brand name
- **Severity:** P0
- **So what:** Two visitors spent 6:30 and 2:50 on the site and left still describing it from the logo.
- **Framework tags:** V1-WHAT, C-COMPREHENSION
- **Flow:** shape_1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` in both timelines; `guessed: true` in both.
  - The h1 is "Your thoughts, everywhere." — no noun for the product, no verb for what it does.
  - Both personas attributed their answer to the name or a friend, explicitly not to the page.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` (`shape_v1`) · `crawl/pages/1-index.json` (`h1`)
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." (`persona-evaluator/persona-debrief.md`, Q1)
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." (`persona-sceptic/persona-debrief.md`, Q1)
- **Repro:**
  1. Open `http://localhost:8765/` logged out at 1440×900.
  2. Read only what is above the fold; do not scroll.
  3. Try to state what the company sells without using the word in the logo.
- **Fix:** Replace the h1 "Your thoughts, everywhere." with a line that names the category and the job — e.g. "Notes that sync across your laptop and phone, and work offline."

### 005bc072be9b — The only explanatory sentence above the fold turns on two terms the visitor could not define
- **Severity:** P1
- **So what:** The one slot on the page that had to explain the product spent itself on words the buyer cannot parse.
- **Framework tags:** V1-WHAT, V2-JARGON
- **Flow:** shape_1
- **Locator:** /index.html hero subhead
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - The evaluator flagged both terms as meaningless at 00:18 and fell back to an assumption.
  - "What is a 'sync graph'?" is still an open question in the debrief, 6:30 later.
  - Torn between P2 (jargon in copy) and P1: taken higher because this sentence is the fold's only explanation.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` (t=00:18) · `crawl/pages/1-index.json` (`meta_description`)
  > "'bi-directional sync graph', 'zero-knowledge vault' — I don't know what either means."
- **Repro:**
  1. Open `http://localhost:8765/` logged out.
  2. Read the line under the headline.
  3. Ask a non-technical reader to define "bi-directional sync graph" and "zero-knowledge vault".
- **Fix:** Rewrite the hero subhead in outcome terms — what the visitor gets — and move "zero-knowledge" to the privacy section where it can be explained.

### da2ec8489c8d — Nothing above the fold names an audience; the only audience statement sits two clicks away on pricing
- **Severity:** P1
- **So what:** Neither visitor could tell whether the product was meant for them, so neither had a reason to continue.
- **Framework tags:** V1-WHO, V3-PLACEMENT
- **Flow:** shape_1
- **Locator:** /index.html hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` in both timelines.
  - `/pricing.html` does answer it — "Starter / For individuals." and "Team / For growing teams." — but the landing page never does.
  - The only landing-page signal, the h2 "Loved by teams", appears below the fold and points one way only.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/findings-raw.json` (t=00:08) · `persona-sceptic/timeline.json` (`shape_v1`)
  > "I can't tell. The top of the page names nobody. 'Loved by teams' lower down suggests teams. Maybe me, maybe not." (`persona-evaluator/persona-debrief.md`, Q2)
  > "For who? Doesn't say." (`persona-sceptic/session.log:6`)
- **Repro:**
  1. Open `http://localhost:8765/` logged out.
  2. Look for any noun naming a user above the fold.
  3. Open `/pricing.html` and find "For individuals." — the answer the landing page withheld.
- **Fix:** Put the audience in the hero — an eyebrow or subhead line saying who it is for, reusing the pricing page's own "individuals and growing teams".

### 4d317d26d08f — The clearest sentence about the product sits on the About page, four minutes from where the visitor needed it
- **Severity:** P1
- **So what:** The site can explain itself in one line and does — on the page a visitor reaches only after deciding to leave.
- **Framework tags:** V3-PLACEMENT, V1-WHAT
- **Flow:** shape_3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` FAQ: "Yes. Nimbus Notes stores every note on your device first and syncs when a connection returns." — plain, concrete, jargon-free.
  - The evaluator reached it at 04:20, 2:55 after `point_of_lost_interest` (01:25).
  - The sceptic reached the About page at 01:30 and still listed "What 'remembers everything' actually do?" as unanswered.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `crawl/pages/4-about.json` (`answer_blocks`) · `persona-sceptic/timeline.json` (`questions_unanswered`)
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `http://localhost:8765/` and read the hero.
  2. Open `/about.html` and read the three FAQ answers.
  3. Compare which text lets you describe the product to someone else.
- **Fix:** Promote the three About-page FAQ answers to the landing page, directly under the hero, and keep the About copy as the canonical wording.

### a02badbbd682 — At 390px the headline and the explanatory subhead are clipped off the right edge
- **Severity:** P1
- **So what:** On the phone the page's only explanation is physically unreadable, so the mobile visitor had nothing to comprehend.
- **Framework tags:** V1-WHAT, C-VIEWPORT
- **Flow:** shape_1
- **Locator:** /index.html hero at 390px
- **Personas hit:** sceptic
- **Observed:**
  - At 390×844 the h1 renders as "Your thoughts, everywh…"; the subhead is cut mid-word at "zero-kno…" and "lost or e…".
  - The nav item "About" is also cut, so the page is wider than the viewport, not merely wrapped.
  - Reproduced independently in the measurement capture at the same viewport, and again on `/about.html`.
  - Severity flip: the identical copy reads in full at 1440×900 for the evaluator.
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `measure/screenshots/index-mobile.png` · `persona-sceptic/screenshots/02-about.png` · `measure/index-mobile.json` (`viewport_verified: true`)
  > "Headline 'Your thoughts, everywhere.' and a purple picture that takes the whole screen." (`persona-sceptic/session.log:5`)
- **Repro:**
  1. Open `http://localhost:8765/` at 390×844.
  2. Observe the h1 and subhead truncated at the right edge.
  3. Confirm the nav's "About" is also clipped — the layout overflows horizontally.
- **Fix:** Constrain the hero and nav to the viewport width at ≤430px (wrap the h1, remove the fixed-width overflow) so the headline and subhead render in full.

### 1f846d28b401 — The only show-me affordance is inert, leaving comprehension to copy alone
- **Severity:** P2
- **So what:** Both visitors tried to be shown what the product does and were shown nothing, so the copy had to carry the whole explanation and did not.
- **Framework tags:** V2-DEMONSTRATION, V1-NEXT
- **Flow:** shape_2
- **Locator:** /index.html hero CTA
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" produces no navigation and no state change; the evaluator clicked twice, the sceptic tapped once.
  - The landing page load throws `ReferenceError: nimbusBootstrap is not defined`.
  - Both Q6 answers cite the absence of any demonstration as why the promise was not met.
- **Evidence:** `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-evaluator/findings-raw.json` (t=00:40) · `measure/index-mobile.json` (`console_errors_on_load`)
  > "No — nothing on the site shows it remembering anything; the button that might have doesn't work." (`persona-sceptic/persona-debrief.md`, Q6)
- **Repro:**
  1. Open `http://localhost:8765/` logged out.
  2. Click "See it in action".
  3. Observe no navigation, no modal, no scroll.
- **Fix:** Point "See it in action" at a working product recording or an inline animation of a note syncing between two devices.

### 1894f54ff671 — Four names for one product across three adjacent cards: card, graph, blocks, vault
- **Severity:** P2
- **So what:** The visitor could not tell whether the site was describing one thing or four, so the "How it works" section explained nothing.
- **Framework tags:** V2-JARGON, C-CONSISTENCY
- **Flow:** shape_2
- **Locator:** /index.html How it works
- **Personas hit:** evaluator
- **Observed:**
  - Capture: "Write a card. It joins the graph instantly." Sync: "Blocks flow between devices through the vault."
  - The words "card", "graph", "blocks" and "vault" are introduced together and none is defined.
  - The evaluator asked directly whether cards and blocks were different things and moved on without an answer.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say 'card', the sync one says 'blocks'. Are those different things?"
- **Repro:**
  1. Open `http://localhost:8765/` and scroll to "How it works".
  2. Read the Capture and Sync cards in order.
  3. Count the distinct nouns used for the product's content.
- **Fix:** Pick one noun for the unit of content across the whole site and rewrite the three "How it works" cards to use only that word.

### 3dc70fe41a07 — The pricing explanation turns on two terms the visitor cannot apply to themselves
- **Severity:** P2
- **So what:** The one line offered in place of a number asks the visitor a question about themselves they cannot answer.
- **Framework tags:** V3-JARGON, V1-WHO
- **Flow:** shape_3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - `/pricing.html` closes with "Pricing depends on your workspace type and sync topology."
  - Neither term is defined anywhere the evaluator visited; both appear in the debrief's list of things the site never told them.
  - The evaluator could not place themselves in either variable.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/timeline.json` (`questions_unanswered`)
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the line beneath the three plan cards.
  3. Try to determine which workspace type and sync topology you have.
- **Fix:** Delete "workspace type and sync topology" and state the two variables a buyer knows — number of people and storage.

### afa893335139 — The newsletter box outweighs the primary action and the desktop visitor could not say what the page wanted
- **Severity:** P2
- **So what:** The loudest element on the page asks for an email address instead of explaining the product.
- **Framework tags:** V1-NEXT, C-HIERARCHY
- **Flow:** shape_1
- **Locator:** /index.html newsletter band
- **Personas hit:** evaluator
- **Observed:**
  - "See it in action" is a small outlined button; the "Get the Nimbus newsletter" band below is full-width and solid purple.
  - `understood_next_step: false` for the evaluator at 1440×900.
  - Severity flip: the sceptic, at 390px, named the button as the next step without hesitation (`understood_next_step: true`).
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:11` · `persona-evaluator/timeline.json` (`shape_v1`)
  > "There's a small outlined 'See it in action' button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `http://localhost:8765/` at 1440×900.
  2. Name the single element the page most wants clicked.
  3. Compare its visual weight with the newsletter band.
- **Fix:** Make "See it in action" a solid primary button and demote the newsletter band to a single footer line.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The hero image may be carrying explanatory weight it cannot bear — no persona commented on what the two purple circles were meant to depict.
- Whether the h1 is understood by visitors arriving without a referral — both personas arrived with a promise in hand, so neither read the page cold.

## For other lenses
- Every plan says "Contact sales"; no price anywhere — `conversion`
- Seven-field demo form with phone required before any product is seen — `conversion`
- "Features" in the main nav returns a 404 — `technical`
- Cookie bar says "We use no tracking cookies on this site" while `/privacy.html` describes cookies and unnamed partners — `trust`
- Three testimonials attributed to "a happy customer", "a user", "anonymous" — `trust`
- `ReferenceError: nimbusBootstrap is not defined` on load; 3.9 MB hero PNG; invalid `SoftwareApplication` JSON-LD — `technical`, `seo`

## Coverage gaps
- `/features.html` never seen — the nav link 404s, so the page a visitor would use to answer "what is it" was unreachable.
- The sceptic never opened `/pricing.html`, so the audience statement there was tested on one persona only.
- No tablet viewport tested; the 390px clipping was observed only at iPhone 13 dimensions.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/` (00–06) · `persona-sceptic/screenshots/` (00–02) · `measure/screenshots/`
