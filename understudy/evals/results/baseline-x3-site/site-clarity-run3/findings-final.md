# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: comprehension on three axes — what / who / next step — scored against reality, timed from V1 (visit-shapes.md)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED. Two invented visitors (evaluator, desktop 1440×900; sceptic, iPhone 13 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Persuasion and believability are out of scope here (conversion, trust); only whether the visitor understood is scored

---

## Findings

### 6a6a238718c2 — Neither visitor could say what Nimbus Notes is from the page; both guessed from the name
- **Severity:** P0
- **So what:** The site's first and only job — "what is this" — was not done for 2 of 2 visitors; everything after is a visitor working around the fold.
- **Framework tags:** what-axis, V1
- **Flow:** shape_v1
- **Locator:** / h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Headline "Your thoughts, everywhere." names no category; both timelines record `time_to_comprehension_seconds: null`, `understood_what: false`, `guessed: true`.
  - Evaluator's Q1 answer is sourced from the product name and one line "halfway down the page"; sceptic's from the name and a friend.
  - Evaluator still could not say what it does at 05:45, after five pages.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-evaluator/session.log:28` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1 · `persona-evaluator/persona-debrief.md` Q1 · `persona-sceptic/persona-debrief.md` Q1
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said."
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page."
- **Repro:**
  1. Open / at 1440×900 or 390×844, do not scroll.
  2. Cover the wordmark "Nimbus Notes" and ask what the product is.
  3. Nothing above the fold answers; the guess comes from the name alone.
- **Fix:** Replace the hero headline and subhead with a plain-language category statement — e.g. "A notes app that syncs every device and works offline" — before any metaphor.
- Severity note: torn between P0 and P1; chose P0 because the lens treats a null comprehension time as the flow not completing, and it was null for both personas.

### badc617d2303 — Hero subhead "bi-directional sync graph with a zero-knowledge vault" undefined for both visitors
- **Severity:** P1
- **So what:** The only descriptive sentence above the fold is two terms the visitor cannot parse, so the fold explains nothing.
- **Framework tags:** what-axis, jargon, V1
- **Flow:** shape_v1
- **Locator:** / .hero p
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator at 00:18: could define neither term; assumed "it syncs". "What a 'sync graph' is" is in the evaluator's Q4 list.
  - Sceptic's Q4 asks what "remembers everything" actually does — the subhead did not tell them.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` t=00:18 · `persona-evaluator/persona-debrief.md` Q4
  > "'bi-directional sync graph with a zero-knowledge vault' — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open / and read the sentence under the headline.
  2. Ask a non-technical reader to say what "sync graph" and "zero-knowledge vault" mean.
- **Fix:** Rewrite the subhead in the visitor's words — "Your notes sync between laptop and phone, work offline, and are encrypted so only you can read them."

### 836bc5d0dc55 — Above the fold names no audience; neither visitor could say who it is for
- **Severity:** P1
- **So what:** A visitor who cannot tell whether this is for them has no reason to scroll; both left with "possibly me".
- **Framework tags:** who-axis, V1
- **Flow:** shape_v1
- **Locator:** / .hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Both timelines record `understood_who: false`; both debriefs answer Q2 with "can't tell" / "doesn't say".
  - The only audience signal on / is the section heading "Loved by teams", below the fold at 1440×900.
  - Audience wording exists only on /pricing.html — "For individuals." / "For growing teams." — a page the sceptic never opened.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6` · `persona-evaluator/persona-debrief.md` Q2 · `persona-sceptic/persona-debrief.md` Q2
  > "I can't tell. The top of the page names nobody. 'Loved by teams' lower down suggests teams. Maybe me, maybe not."
  > "The page doesn't say. Possibly me."
- **Repro:**
  1. Open / at either viewport without scrolling.
  2. Look for any noun naming a person, role, or team size — there is none.
- **Fix:** Add one audience line under the headline on / — "For individuals and small teams who take notes on more than one device" — and repeat it at the top of /pricing.html.

### 2c205fa21945 — Clearest description of the product sits in the About FAQ, two clicks from the home page
- **Severity:** P1
- **So what:** The sentences that finally made the product make sense are on /about.html, where a visitor who leaves at the fold never goes.
- **Framework tags:** what-axis, placement, V3
- **Flow:** shape_v3
- **Locator:** /about.html #faq
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - /about.html FAQ states in plain words: "stores every note on your device first and syncs when a connection returns" and "Export produces a folder of Markdown files".
  - Evaluator at 04:20 called these "actual answers" and asked why they are not on the home page.
  - Sceptic found the data-location answer on About, not on Privacy where they looked first.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open / and read the hero and "How it works" — no mention of offline, export, or where data lives.
  2. Open /about.html and read "Frequently asked questions" — all three are answered.
- **Fix:** Move the three FAQ answers onto / as the "How it works" copy, and keep the FAQ on About as a duplicate.

### 89830467369b — 'How it works' cards use card, graph, blocks and vault without defining any of them
- **Severity:** P2
- **So what:** The section that should resolve the fold's confusion introduces four more undefined nouns, so the visitor leaves it less sure than they arrived.
- **Framework tags:** what-axis, jargon, V2
- **Flow:** shape_v2
- **Locator:** / #how-it-works
- **Personas hit:** evaluator
- **Observed:**
  - Cards read "Write a card. It joins the graph instantly." / "Blocks flow between devices through the vault." / "Nimbus remembers everything so you never start from zero."
  - Evaluator at 01:10 asked whether "card" and "blocks" are different things; no answer on the page.
  - Section is at 100% scroll depth for the evaluator, so it was seen in full.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say 'card', the sync one says 'blocks'. Are those different things?"
- **Repro:**
  1. Open / and scroll to "How it works".
  2. Count the nouns a first-time visitor must already know: card, graph, blocks, vault.
- **Fix:** Rewrite the three cards with one consistent noun — "note" — and describe the action, e.g. "Write a note. It's on your phone a second later."

### c81898854633 — 'See it in action' does nothing, so 'remembers everything' is never shown to the visitor
- **Severity:** P1
- **So what:** Both visitors arrived on the promise "remembers everything"; the one control that could demonstrate it is inert, and both said the site never shows it.
- **Framework tags:** what-axis, next-step-axis, V2
- **Flow:** shape_v2
- **Locator:** / a.see-it-in-action
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator clicked "See it in action" twice at 00:40; page did not move. Sceptic tapped it at 02:20; nothing happened.
  - Both Q6 answers say nothing on the site shows the product remembering anything.
  - Sceptic's `trust_down` lists "'See it in action' does nothing".
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-evaluator/persona-debrief.md` Q6 · `persona-sceptic/persona-debrief.md` Q6
  > "Clicked 'See it in action'. Nothing happened. The page didn't move. Clicked again. Still nothing."
  > "No — nothing on the site shows it remembering anything; the button that might have doesn't work."
- **Repro:**
  1. Open / at either viewport, dismiss the cookie bar.
  2. Click "See it in action" — no navigation, no scroll, no modal.
- **Fix:** Point "See it in action" at a real demonstration — a 20-second clip or three screenshots of a note appearing on a second device — placed directly under the hero.

### ce97b8a98b83 — Newsletter box outweighs 'See it in action'; evaluator could not tell what the page wants
- **Severity:** P2
- **So what:** The evaluator read the loudest element as the ask and could not say what the page wanted them to do.
- **Framework tags:** next-step-axis, V1
- **Flow:** shape_v1
- **Locator:** / .newsletter
- **Personas hit:** evaluator
- **Observed:**
  - "See it in action" is a small outlined button; "Get the Nimbus newsletter" is a full-width solid purple block immediately below it.
  - Evaluator timeline: `understood_next_step: false`; log at 00:11 names the newsletter box as "much bigger and brighter".
  - Severity flip: sceptic recorded `understood_next_step: true` on the same fold; not a finding for them.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-evaluator/findings-raw.json` t=01:10 · `persona-evaluator/timeline.json` shape_v1
  > "There's a small outlined 'See it in action' button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open / at 1440×900 and scroll one screen.
  2. Compare the visual weight of "See it in action" against "Get the Nimbus newsletter".
- **Fix:** Make "See it in action" the solid primary button in the hero and demote the newsletter block to the footer.

### d7e868027227 — Pricing footnote 'workspace type and sync topology' is unparseable to a first-time visitor
- **Severity:** P2
- **So what:** The one sentence explaining how price is set uses two terms the visitor has no way to define, so they cannot even estimate.
- **Framework tags:** what-axis, jargon, V3
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - /pricing.html footnote: "Pricing depends on your workspace type and sync topology."
  - Evaluator at 02:10: "I don't know what my workspace type is. I haven't got one." — "What a 'workspace type' is" is in their Q4 list and in `questions_unanswered`.
  - The absence of numbers is a conversion matter; scored here only as comprehension of the sentence that stands in for them.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/persona-debrief.md` Q4 · `persona-evaluator/timeline.json` shape_v3.questions_unanswered
  > "'Pricing depends on your workspace type and sync topology.' I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open /pricing.html.
  2. Read the grey line under the three plan cards.
- **Fix:** Replace the footnote with the two or three plain factors that actually set price — e.g. "Price depends on how many people and how many devices" — and define each in one line.

### 47b6db207700 — 'Features' nav item, the one page promising to explain the product, returns a 404
- **Severity:** P2
- **So what:** The only nav label that promises "what does it do" leads to "Error code: 404", so the visitor's most direct route to comprehension is dead.
- **Framework tags:** what-axis, dead-end, V3
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - Nav on every page lists "Features"; clicking it at 03:30 produced a bare server error page "Error code: 404 / Message: File not found."
  - Evaluator went there specifically after failing to learn what it does from / and /pricing.html.
  - Sceptic never tried the link; the 404 itself belongs to bugs — scored here for what it withholds.
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `persona-evaluator/findings-raw.json` t=03:30
  > "Clicked 'Features' in the nav. Got a 404 page: 'That page does not exist.'"
- **Repro:**
  1. Open / and click "Features" in the top nav.
  2. Observe the 404 response.
- **Fix:** Publish /features.html with the plain-language product description, or remove "Features" from the nav until it exists.

### 0e2cdca73272 — Headline and subhead clipped at the right edge of the iPhone 13 viewport
- **Severity:** P2
- **So what:** On the phone the fold shows "Your thoughts, everywh" and "zero-kno" — the two lines meant to explain the product are cut off before they finish.
- **Framework tags:** what-axis, mobile-fold, V1
- **Flow:** shape_v1
- **Locator:** / h1 (390px)
- **Personas hit:** sceptic
- **Observed:**
  - `persona-sceptic/screenshots/00-landing.png` at 390×844 shows the headline, subhead, nav ("Abo…") and hero image overflowing the right edge.
  - The sceptic logged the full headline at 00:00, so they recovered it — but the fold as captured does not show it.
  - Not observed at 1440×900, where the same text fits.
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:5` · `persona-sceptic/timeline.json` viewport
- **Repro:**
  1. Open / at 390×844.
  2. Do not scroll; observe the headline and subhead truncated at the viewport edge.
- **Fix:** Constrain the hero container and image to 100vw on small screens so the headline and subhead wrap instead of overflowing.
- Severity note: torn between P2 and P3 because the persona did not complain; chose P2 because the screenshot is the fold as a phone visitor meets it.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The hero image carries visible placeholder text ("…svg — a real capture serves assets/generated/hero.png…") — fixture artefact; neither persona remarked on it, so no comprehension effect was observed.
- "Log in" is the only solid nav button, which may read as "existing customers only" — no persona said so.

## For other lenses
- Cookie bar "We use no tracking cookies" contradicts /privacy.html "we use cookies… share with partners" — trust (`persona-evaluator/session.log:27`, `persona-sceptic/session.log:10`).
- All three pricing tiers say "Contact sales" with no numbers; run objective not met for evaluator — conversion, objectives (`persona-evaluator/screenshots/02-pricing.png`).
- "Contact sales" routes to a 7-field demo form with phone required — conversion (`persona-evaluator/screenshots/03-demo-form.png`).
- Testimonials attributed to "a happy customer", "a user", "anonymous" — trust (`persona-evaluator/screenshots/01-scrolled.png`).
- /features.html 404 from the primary nav — bugs, seo (`persona-evaluator/screenshots/04-features-404.png`).
- Privacy policy names no partners and "may update at any time" — trust (`persona-sceptic/session.log:9`).

## Coverage gaps
- /features.html never rendered for any persona (404).
- Sceptic never opened /pricing.html; pricing comprehension rests on one persona.
- Demo form never submitted (by design).
- No researched personas; both visitors are generic inferences.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator: 00-landing, 01-scrolled, 02-pricing, 03-demo-form, 04-features-404, 05-about, 06-privacy; sceptic: 00-landing, 01-privacy, 02-about
