# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: clarity lens — what / who / next step, time to comprehension, undefined terms
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 5e054cb75af1 — Neither persona could say what Nimbus Notes is — comprehension never reached
- **Severity:** P0
- **So what:** Both visitors guessed "notes app" from the brand name alone; the page itself never told them, so the site's first job failed.
- **Framework tags:** what ✗ · who ✗ · time-to-comprehension never
- **Flow:** shape_v1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` and `understood_what: false`, `guessed: true` for both personas
  - Headline "Your thoughts, everywhere." names no product category, task or outcome
  - Line that brought the evaluator ("Nimbus remembers everything so you never start from zero") sits below the fold, found at 00:55
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:14` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." (evaluator, Q1)
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." (sceptic, Q1)
- **Repro:**
  1. Open `/index.html` at 1440×900 or 390×844
  2. Read only the fold for 10 seconds
  3. Try to state what the product does without using the word "Notes" from the logo
- **Fix:** Replace the headline with a literal statement of the product, e.g. "Notes that sync across your laptop and phone and remember everything".
- **Torn P0/P1:** chosen P0 because no persona ever reached comprehension; neither left solely because of it.

### 9c85d6951d1b — Hero subhead explains the product only in jargon the visitor could not parse
- **Severity:** P2
- **So what:** The one descriptive line above the fold was unreadable, so the visitor fell back on guessing from the brand name.
- **Framework tags:** what · undefined terms
- **Flow:** shape_v1
- **Locator:** /index.html hero subhead
- **Personas hit:** evaluator
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator could define neither "bi-directional sync graph" nor "zero-knowledge vault"
  - "What is a sync graph?" is listed in `questions_unanswered`
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` (00:18)
  > "'bi-directional sync graph', 'zero-knowledge vault' — I don't know what either means."
- **Repro:**
  1. Open `/index.html`
  2. Read the subhead under the headline
- **Fix:** Rewrite the subhead in plain outcomes, e.g. "Write on any device, see it everywhere, encrypted so only you can read it".

### fab43a7e5140 — Landing page never says who the product is for; audience appears only on Pricing
- **Severity:** P2
- **So what:** The evaluator came to judge a team tool and could not tell whether it was for individuals or teams.
- **Framework tags:** who ✗ · placement
- **Flow:** shape_v1
- **Locator:** /index.html hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` for both personas
  - Only audience signal on the home page is a "Loved by teams" heading below the fold
  - Pricing cards say "For individuals." and "For growing teams." — the clearest audience statement is two clicks away
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6`
  > "I can't tell. The top of the page names nobody. \"Loved by teams\" lower down suggests teams. Maybe me, maybe not." (evaluator, Q2)
  > "The page doesn't say. Possibly me." (sceptic, Q2)
- **Repro:**
  1. Open `/index.html`
  2. Look for any statement of audience above the fold
- **Fix:** Add one line under the headline naming the audience, e.g. "For individuals and small teams", matching the Pricing card wording.

### e29dae8bdbf0 — The only route to seeing the product, See it in action, does nothing when clicked
- **Severity:** P2
- **So what:** Both visitors tried to watch the product work and saw nothing, so the promise "remembers everything" stayed abstract; churn risk for anyone who came to see it.
- **Framework tags:** next step · show-don't-tell
- **Flow:** shape_v2
- **Locator:** /index.html See it in action button
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator clicked "See it in action" twice at 00:40; page did not move
  - Sceptic tapped it at 02:20 to see it "remember" something; nothing happened, stopped at 02:40
  - Button is small and outlined; the newsletter box below is larger and brighter (`understood_next_step: false` for evaluator)
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:11` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13`
  > "'It remembers everything.' No — nothing on the site shows it remembering anything; the button that might have doesn't work." (sceptic, Q6)
- **Repro:**
  1. Open `/index.html`
  2. Click "See it in action"
  3. Observe no scroll, navigation or media
- **Fix:** Make "See it in action" open a short product demo, and make it visually the primary button above the newsletter box.

### fcbd63a0e7fd — Hero image is two abstract circles that show nothing of the product
- **Severity:** P2
- **So what:** The largest element on the fold could have shown a note syncing; instead it gave the visitor no clue what the product is.
- **Framework tags:** what · fold
- **Flow:** shape_v1
- **Locator:** /index.html hero image
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero area is two overlapping lavender circles on a pale panel
  - On the phone it fills most of the 844px fold below the headline
  - Both personas described it only as "a purple picture" / "a purple blob picture"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:5` · `persona-sceptic/session.log:5`
  > "Headline \"Your thoughts, everywhere.\" and a purple picture that takes the whole screen." (sceptic)
- **Repro:**
  1. Open `/index.html` on desktop and on a 390px phone
  2. Look at the hero image
- **Fix:** Replace the hero art with a real screenshot of a note appearing on laptop and phone.

### cab2123679db — On a 390px phone the headline and subhead are cut off at the right edge
- **Severity:** P2
- **So what:** A mobile visitor reads "Your thoughts, everywh" and half a subhead, losing the little explanation the fold offers.
- **Framework tags:** fold · mobile
- **Flow:** shape_v1
- **Locator:** /index.html at 390px
- **Personas hit:** sceptic
- **Observed:**
  - Headline renders "Your thoughts, everywh…" clipped at 390px
  - Subhead clipped at "zero-kno…" and "lost or e…"; nav "About" clipped to "Abo"
  - Persona did not remark on it; `understood_what: false` at 00:08
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:6`
- **Repro:**
  1. Open `/index.html` at 390×844
  2. Read the headline and subhead without horizontal scrolling
- **Fix:** Make the hero text wrap within the viewport on mobile and collapse the nav into a menu.

### 0937269a48ca — The clearest description of the product is buried in the About page FAQ
- **Severity:** P2
- **So what:** Plain answers that explain the product exist, but visitors only find them after the home page has already failed them.
- **Framework tags:** placement · what
- **Flow:** shape_v3
- **Locator:** /about.html FAQ
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ says "Nimbus Notes stores every note on your device first and syncs when a connection returns."
  - Also "Settings → Export produces a folder of Markdown files" and "In the EU (Frankfurt) by default."
  - Evaluator reached it at 04:20, sceptic at 01:50; neither saw anything this plain on the home page
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "Those are actual answers. Why isn't this on the home page?" (evaluator)
- **Repro:**
  1. Open `/about.html`
  2. Compare the FAQ answers with the `/index.html` hero copy
- **Fix:** Move the offline, export and data-location answers onto the home page directly under the hero.

### 9ce1586be634 — Pricing page explains cost with undefined terms the visitor could not apply to themselves
- **Severity:** P2
- **So what:** The only explanation of price used vocabulary the visitor did not have, so they could not even estimate which plan applied.
- **Framework tags:** undefined terms · pricing comprehension
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Footnote reads "Pricing depends on your workspace type and sync topology."
  - Evaluator: "I don't know what my workspace type is. I haven't got one."
  - "What is a workspace type?" listed in `questions_unanswered`
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/persona-debrief.md` Q4
  > "What it costs. What a \"workspace type\" is. What a \"sync graph\" is." (evaluator, Q4)
- **Repro:**
  1. Open `/pricing.html`
  2. Read the line under the plan cards
- **Fix:** Replace the footnote with plain criteria, e.g. "Price depends on number of users and devices", or define both terms inline.

### 0e43f7c3610d — How it works names one thing four ways: card, blocks, graph, vault
- **Severity:** P3
- **So what:** Shifting nouns made the visitor wonder whether these were different objects, adding doubt to an already unclear product.
- **Framework tags:** terminology consistency
- **Flow:** shape_v2
- **Locator:** /index.html How it works
- **Personas hit:** evaluator
- **Observed:**
  - Capture card: "Write a card. It joins the graph instantly."
  - Sync card: "Blocks flow between devices through the vault."
  - Evaluator asked whether "card" and "blocks" were different things
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say \"card\", the sync one says \"blocks\". Are those different things?"
- **Repro:**
  1. Open `/index.html` and scroll to "How it works"
  2. Read the three cards in order
- **Fix:** Use one word, "note", in all three How it works cards.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- None

## For other lenses
- Every plan on `/pricing.html` says "Contact sales"; no price — conversion
- "Contact sales" leads to a seven-field demo form with required phone — conversion
- Nav "Features" returns a 404 (`persona-evaluator/screenshots/04-features-404.png`) — technical
- Hero panel shows filename text "…svg — a real capture serves assets/generated/hero.png…" — technical
- Anonymous testimonials ("— a happy customer", "— anonymous") were the evaluator's point of lost interest (01:25) — trust
- Cookie bar "We use no tracking cookies" contradicts the privacy page — trust

## Coverage gaps
- Sceptic never scrolled the home page beyond the fold (`sections_seen: 1`); How it works not seen on mobile
- `/features.html` 404 — any explanation it was meant to hold was never seen
- Demo content behind "See it in action" never reached by either persona

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator 00–06, sceptic 00–02
