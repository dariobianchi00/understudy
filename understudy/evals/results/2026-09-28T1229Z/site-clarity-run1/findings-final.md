# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: comprehension on three axes (what / who / next step) plus time-to-comprehension, judged at each persona's viewport
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator @ desktop 1440×900, sceptic @ iPhone 13 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 12eae4ce1c04 — Neither persona could say what Nimbus Notes is from the page; comprehension never arrived
- **Severity:** P1
- **So what:** Both visitors guessed the product from its name, then left or gave up without the page ever confirming the guess.
- **Framework tags:** C-WHAT, C-TTC-never
- **Flow:** shape_v1
- **Locator:** /index.html hero h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` and `understood_what: false`, `guessed: true` for both personas
  - Headline "Your thoughts, everywhere." names no product category; the fold shows abstract purple circles
  - Evaluator still "notes that sync" at 05:45; sceptic left at 02:50 (`left_early: true`)
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:14` · `persona-evaluator/session.log:28` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." (evaluator, Q1)
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." (sceptic, Q1)
- **Repro:**
  1. Open the home page at 1440×900 or 390×844.
  2. Read only the fold for 10 seconds; try to name the product category and what it does.
- **Fix:** Rewrite the hero h1 to name the category and job in plain words (e.g. "Notes that sync between your laptop and phone"), keep the slogan as an eyebrow.

### af20ddbac96a — Hero subhead explains the product in jargon neither persona could parse
- **Severity:** P2
- **So what:** The one sentence meant to explain the product was unreadable, so the visitor "assumed it syncs" and moved on uninformed.
- **Framework tags:** C-JARGON, C-WHAT
- **Flow:** shape_v1
- **Locator:** /index.html hero subhead
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator could define neither "sync graph" nor "zero-knowledge vault"; listed "sync graph" as unanswered in Q4
  - Sceptic's Q1 does not mention sync, graph or vault at all
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/findings-raw.json` t=00:18 · `persona-evaluator/timeline.json` questions_unanswered
  > "'bi-directional sync graph', 'zero-knowledge vault' — I don't know what either means."
- **Repro:**
  1. Open the home page.
  2. Read the grey line under the headline and try to restate it without the terms "graph" or "vault".
- **Fix:** Replace the subhead with the plain benefit ("Your notes stay in sync on every device, encrypted so only you can read them").

### 3ae8ad9901d8 — Landing page never says who it is for; the only audience lines sit on the Pricing page
- **Severity:** P2
- **So what:** The evaluator, choosing for a team, could not tell if this was for individuals or teams — a question the site answers two clicks deep.
- **Framework tags:** C-WHO, C-PLACEMENT
- **Flow:** shape_v1
- **Locator:** /index.html hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` for both personas; nothing above the fold names an audience
  - First audience signal is "Loved by teams", below the newsletter box
  - Pricing cards say "For individuals." and "For growing teams." — the site's clearest who-statement
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6`
  > "I can't tell. The top of the page names nobody. \"Loved by teams\" lower down suggests teams. Maybe me, maybe not." (evaluator, Q2)
  > "The page doesn't say. Possibly me." (sceptic, Q2)
- **Repro:**
  1. Open the home page; read the fold.
  2. Look for any line naming who the product is for.
  3. Open Pricing; note "For individuals." / "For growing teams."
- **Fix:** Add one audience line under the hero h1 ("For individuals and small teams"), lifted from the Pricing card copy.

### ce7a83b1106e — The See it in action button does nothing, so the remembers-everything promise is never shown
- **Severity:** P2
- **So what:** Both visitors arrived on "remembers everything"; the only route to seeing that was dead, so the core promise stayed an abstraction.
- **Framework tags:** C-NEXT, C-PROMISE
- **Flow:** shape_v2
- **Locator:** /index.html See it in action button
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator clicked "See it in action" twice at 00:40; page did not move
  - Sceptic tapped it at 02:20 to see it "remember" something; nothing happened; stopped at 02:40
  - Q6 promise match: evaluator "Close but off", sceptic "No"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/session.log:14` · `persona-evaluator/console-full.txt`
  > "\"It remembers everything.\" No — nothing on the site shows it remembering anything; the button that might have doesn't work." (sceptic, Q6)
- **Repro:**
  1. Open the home page; dismiss the cookie bar.
  2. Click "See it in action" twice.
- **Fix:** Wire "See it in action" to a 20-second screen recording of a note written on laptop appearing on phone.

### 50de035bc44a — Newsletter box outweighs the only product button, so the next step reads as subscribe
- **Severity:** P2
- **So what:** The evaluator could not name a next step at 00:11; the page's loudest ask is an email for a newsletter, not the product.
- **Framework tags:** C-NEXT, C-HIERARCHY
- **Flow:** shape_v1
- **Locator:** /index.html newsletter box
- **Personas hit:** evaluator
- **Observed:**
  - Evaluator `understood_next_step: false`; sceptic `true` (read "See it in action" as the next step)
  - "See it in action" is a small outlined button; "Get the Nimbus newsletter" is a full-width solid purple band directly below
  - No "start free" or signup action appears anywhere on the home page
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-evaluator/findings-raw.json` t=01:10 · `persona-sceptic/session.log:6`
  > "There's a small outlined \"See it in action\" button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open the home page at 1440×900.
  2. Compare the visual weight of "See it in action" and the newsletter band.
- **Fix:** Make the product action a solid primary button in the hero and demote the newsletter to a footer text field.

### 80061997dbef — The clearest plain-English explanation of the product is buried in the About page FAQ
- **Severity:** P2
- **So what:** The only concrete answers — offline, sync, Markdown export, Frankfurt storage — reached the evaluator at 04:20, after comprehension had already failed.
- **Framework tags:** C-PLACEMENT, C-WHAT
- **Flow:** shape_v3
- **Locator:** /about.html FAQ
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "stores every note on your device first and syncs when a connection returns"; "a folder of Markdown files"
  - Evaluator asked why this was not on the home page
  - Sceptic found the storage answer on About, not Privacy or home
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/screenshots/02-about.png` · `persona-sceptic/session.log:12`
  > "Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open the home page; note what it says the product does.
  2. Open About; read the three FAQ answers.
- **Fix:** Move the three About FAQ answers onto the home page as the "How it works" cards.

### ee42969daaa8 — Pricing is explained with undefined terms workspace type and sync topology
- **Severity:** P2
- **So what:** The one sentence explaining price used two terms the visitor had never met, so even the rule for pricing was unreadable.
- **Framework tags:** C-JARGON
- **Flow:** shape_v3
- **Locator:** /pricing.html footnote
- **Personas hit:** evaluator
- **Observed:**
  - Pricing footnote: "Pricing depends on your workspace type and sync topology."
  - Neither term is defined anywhere the evaluator visited
  - "What is a workspace type?" recorded in `questions_unanswered`
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/timeline.json` questions_unanswered
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open Pricing.
  2. Read the line under the three plan cards.
- **Fix:** Replace the footnote with plain drivers ("Price depends on how many people and devices you sync").

### 1f635e8ee637 — The Features nav link returns a 404, removing the page meant to explain the product
- **Severity:** P2
- **So what:** A visitor still trying to learn what it does hit "That page does not exist." on the most obvious explanatory page.
- **Framework tags:** C-WHAT, C-NAV
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - Evaluator clicked "Features" in the top nav at 03:30
  - Page shows "That page does not exist."
  - Evaluator moved on to About; no product explanation gained
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `persona-evaluator/findings-raw.json` t=03:30
  > "Features in the nav goes to a 404."
- **Repro:**
  1. Open any page.
  2. Click "Features" in the top nav.
- **Fix:** Publish a Features page, or point the nav item to the home page's "How it works" section until one exists.

### ebcf3576f95f — On a 390px phone the headline and subhead are cut off at the right edge
- **Severity:** P2
- **So what:** The phone fold loses the end of both explanatory lines, including the only stated benefit, "never lost or exposed".
- **Framework tags:** C-FOLD, C-WHAT
- **Flow:** shape_v1
- **Locator:** /index.html hero at 390px
- **Personas hit:** sceptic
- **Observed:**
  - Fold shows "Your thoughts, everywh" and "A bi-directional sync graph with a zero-kno" — rest off-screen
  - Nav is clipped the same way ("Abo")
  - Desktop fold at 1440×900 shows both lines in full; sceptic did not remark on it
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/session.log:5`
- **Repro:**
  1. Open the home page on an iPhone 13 (390×844).
  2. Read the headline and subhead without scrolling sideways.
- **Fix:** Let the hero h1 and subhead wrap at mobile width and remove whatever forces the page wider than 390px.

### 6c43bad81678 — How it works calls the same unit a card in one step and blocks in the next
- **Severity:** P3
- **So what:** A visitor already short on vocabulary is left wondering whether cards and blocks are different things.
- **Framework tags:** C-JARGON, C-CONSISTENCY
- **Flow:** shape_v2
- **Locator:** /index.html How it works
- **Personas hit:** evaluator
- **Observed:**
  - Capture: "Write a card. It joins the graph instantly."
  - Sync: "Blocks flow between devices through the vault."
  - Evaluator asked if they differ, then kept scrolling
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say \"card\", the sync one says \"blocks\". Are those different things?"
- **Repro:**
  1. Scroll the home page to "How it works".
  2. Compare the Capture and Sync cards.
- **Fix:** Use "note" in all three How it works cards and drop "card", "blocks", "graph" and "vault".

---

## Dropped for want of evidence
- Hero image caption reads ".svg — a real capture serves assets/generated/hero.png, 3.9…" — fixture placeholder text; neither persona reacted, no evidence it exists on the live site.

## For other lenses
- Pricing shows no numbers; every plan is "Contact sales" — conversion
- Demo form: seven fields, phone required — conversion
- Anonymous testimonials ("— a happy customer", "— anonymous") — trust
- Cookie bar "We use no tracking cookies" contradicts the Privacy page; partners unnamed — trust
- `ReferenceError: nimbusBootstrap is not defined` on load; 3.9 MB hero PNG, LCP 5.8 s mobile — technical

## Coverage gaps
- Sceptic never scrolled the home page body (1 section seen) or opened Pricing; no mobile reading of "How it works"
- Features page could not be read by either persona (404)
- Only one persona per device; no mobile evaluator, no desktop sceptic

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00–06`, `persona-sceptic/screenshots/00–02`
