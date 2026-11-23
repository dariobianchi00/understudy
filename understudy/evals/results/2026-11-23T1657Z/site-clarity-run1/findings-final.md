# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: comprehension on three axes (what / who / next step), timed against the V1 first-impression answers
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 5ee20ccdacde — Headline "Your thoughts, everywhere." never says what Nimbus Notes is
- **Severity:** P1
- **So what:** Neither persona could say what the product is from the page; both guessed "notes app" from the brand name and never got further.
- **Framework tags:** C-WHAT, C-TTC
- **Flow:** V1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` and `understood_what: false` for both personas; `guessed: true` for both
  - Evaluator at 05:45, after reading every page: "I still don't know … exactly what it does beyond 'notes that sync'"
  - Sceptic's Q1 answer was sourced from a friend, "not from the page"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-evaluator/session.log:28` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." (evaluator, Q1)
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." (sceptic, Q1)
- **Repro:**
  1. Open `/` at 1440×900 or 390×844
  2. Read only the fold: headline, subheadline, hero image
  3. Try to name the product category without using the word "Notes" from the logo
- **Fix:** Replace the h1 with a plain category statement, e.g. "A notes app that syncs across your laptop and phone"; keep the slogan as an eyebrow.

### 668807df44e6 — Landing page never says who it is for — evaluator cannot tell if it fits his team
- **Severity:** P1
- **So what:** He came to judge a replacement for his team's tool and left still asking "individuals or teams?" — the audience question was never resolved.
- **Framework tags:** C-WHO
- **Flow:** V1
- **Locator:** /index.html hero
- **Personas hit:** evaluator
- **Observed:**
  - Fold names no audience; first audience signal is "Loved by teams", below the fold
  - `questions_unanswered` at session end includes "Is it for individuals or teams?"
  - Session ended "would not proceed"; audience was one of five unanswered questions
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:3` · `persona-evaluator/session.log:7` · `persona-evaluator/timeline.json` shape_v3.questions_unanswered
  > "I can't tell. The top of the page names nobody. "Loved by teams" lower down suggests teams. Maybe me, maybe not." (Q2)
- **Repro:**
  1. Open `/` at 1440×900
  2. Look for any audience statement above the fold — there is none
  3. Scroll to "Loved by teams"; compare with Pricing's "For individuals." / "For growing teams."
- **Fix:** Add one audience line under the h1, e.g. "For individuals and small teams"; the Pricing page already has the words.

### 2aa26e4d245d — Landing page never says who it is for — sceptic shrugs and moves on
- **Severity:** P2
- **So what:** She noticed the gap but it did not drive her exit; a visitor less set on a privacy question would have no reason to self-identify.
- **Framework tags:** C-WHO
- **Flow:** V1
- **Locator:** /index.html hero
- **Personas hit:** sceptic
- **Observed:**
  - `understood_who: false` at 00:08
  - Her exit reason was data handling, not audience
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:6` · `persona-sceptic/timeline.json` shape_v1
  > "The page doesn't say. Possibly me." (Q2)
- **Repro:**
  1. Open `/` on iPhone 13 (390×844)
  2. Look for an audience statement on the fold — there is none
- **Fix:** Same audience line under the h1 as for the desktop finding; it must fit within the 390px fold.

### ff01328c1616 — Subheadline jargon "bi-directional sync graph" and "zero-knowledge vault" goes undefined
- **Severity:** P2
- **So what:** The only descriptive sentence on the fold is in terms the visitor could not parse, so it explained nothing; he fell back to "I'll assume it syncs."
- **Framework tags:** C-JARGON, C-WHAT
- **Flow:** V1
- **Locator:** /index.html hero subheadline
- **Personas hit:** evaluator
- **Observed:**
  - Subheadline: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Neither term is defined anywhere the persona visited
  - "sync graph" re-listed in Q4 as something the site never explained
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` (00:18)
  > "\"bi-directional sync graph with a zero-knowledge vault\" — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open `/`
  2. Read the subheadline under "Your thoughts, everywhere."
- **Fix:** Rewrite the subheadline in outcome words, e.g. "Your notes sync instantly between devices and are encrypted so only you can read them."

### 67daf6f0785b — Pricing note "workspace type and sync topology" uses terms the visitor cannot apply to himself
- **Severity:** P2
- **So what:** The one sentence explaining what drives price is unanswerable by a first-time visitor, so he could not even estimate which plan he needed.
- **Framework tags:** C-JARGON
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Footnote: "Pricing depends on your workspace type and sync topology."
  - "workspace type" listed in Q4 and `questions_unanswered`
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/timeline.json` shape_v3.questions_unanswered
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`
  2. Read the line under the three plan cards
- **Fix:** Replace the footnote with the plain driver of price (e.g. number of people, devices) stated in the visitor's terms.

### 70e42637b50c — Clearest plain-language answers sit on the About page, not the landing page
- **Severity:** P2
- **So what:** The only concrete product facts — offline, export to Markdown, data in Frankfurt — are two clicks deep; both personas asked why they weren't up front.
- **Framework tags:** C-PLACEMENT, C-WHAT
- **Flow:** V3
- **Locator:** /about.html FAQ
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Nimbus Notes stores every note on your device first and syncs when a connection returns."
  - Also: "Settings → Export produces a folder of Markdown files" and "In the EU (Frankfurt) by default."
  - Evaluator reached it at 04:20; sceptic at 01:50 — after both had formed their first impression
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "Those are actual answers. Why isn't this on the home page?" (evaluator)
  > "That's the answer I wanted and it's on the About page, not the Privacy page." (sceptic)
- **Repro:**
  1. Open `/`; note no concrete product facts above or below the fold
  2. Open `/about.html`; read the FAQ
- **Fix:** Move the offline / export / data-location answers onto the landing page, directly under the hero.

### e6b428d3ab32 — Only next step "See it in action" is outweighed by the newsletter box and does nothing
- **Severity:** P2
- **So what:** The evaluator could not tell what the site wanted him to do; the newsletter, not the product, reads as the main action.
- **Framework tags:** C-NEXT
- **Flow:** V1
- **Locator:** /index.html See it in action
- **Personas hit:** evaluator
- **Observed:**
  - `understood_next_step: false` for evaluator; sceptic `true` — see severity flip in exec summary
  - Small outlined button; full-width purple "Get the Nimbus newsletter" block directly below
  - Two clicks at 00:40 produced no visible change
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-evaluator/session.log:12` · `persona-evaluator/timeline.json` shape_v1
  > "There's a small outlined \"See it in action\" button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/` at 1440×900
  2. Compare the "See it in action" button with the newsletter block
  3. Click "See it in action"
- **Fix:** Make one filled primary button in the hero that names the action (e.g. "Start free trial"), and demote the newsletter below "How it works".

### 44c56f6aca68 — Hero visual is two abstract circles, so "remembers everything" is never shown
- **Severity:** P2
- **So what:** The largest element on the fold shows no product, so the promise that brought both personas in is never illustrated.
- **Framework tags:** C-WHAT, C-PROMISE
- **Flow:** V1
- **Locator:** /index.html hero image
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero is two overlapping lilac circles; on mobile it fills the screen below the subheadline
  - Q6 for both: the "remembers everything" promise is stated but never shown
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:5` · `persona-sceptic/session.log:5`
  > "Big headline: \"Your thoughts, everywhere.\" A purple blob picture." (evaluator)
  > "nothing on the site shows it remembering anything" (sceptic, Q6)
- **Repro:**
  1. Open `/`
  2. Look at the hero image
- **Fix:** Replace the hero with a real screenshot of a note being recalled on a second device.

### 9e24b01ff858 — Mobile fold clips the headline and subheadline at the right edge on iPhone 13
- **Severity:** P2
- **So what:** At 390px the only descriptive sentence is cut mid-word, so the mobile visitor's fold carries even less meaning than desktop's.
- **Framework tags:** C-FOLD
- **Flow:** V1
- **Locator:** /index.html hero at 390px
- **Personas hit:** sceptic
- **Observed:**
  - Headline renders as "Your thoughts, everywh…"; subheadline "zero-kno… / … lost or e…"; nav "Abo…"
  - Persona did not comment on the clipping — P2, not P1
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:5`
- **Repro:**
  1. Open `/` at 390×844
  2. Read the headline and subheadline to the right edge
- **Fix:** Let the hero text wrap at mobile widths (remove the fixed width / nowrap) and collapse the nav into a menu.

### 0e1da759caa0 — How-it-works cards call the same unit a "card" and "blocks"
- **Severity:** P3
- **So what:** Two nouns for one thing made the evaluator wonder if there were two kinds of object; minor, but it adds to the vocabulary load.
- **Framework tags:** C-JARGON
- **Flow:** V2
- **Locator:** /index.html How it works
- **Personas hit:** evaluator
- **Observed:**
  - Capture: "Write a card. It joins the graph instantly."
  - Sync: "Blocks flow between devices through the vault."
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say \"card\", the sync one says \"blocks\". Are those different things?"
- **Repro:**
  1. Open `/`; scroll to "How it works"
  2. Compare the Capture and Sync card copy
- **Fix:** Use one word throughout — "note" — in all three How-it-works cards.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Hero image overlay text ("…svg — a real capture serves assets/generated/hero.png") — likely a fixture/capture artefact; no persona saw or mentioned it.
- Whether the Features page would have explained the product — it returned 404, so no copy was captured.

## For other lenses
- "See it in action" does nothing on click/tap — technical
- No price on any plan; every CTA is "Contact sales" → seven-field form with phone required — conversion
- Cookie bar "We use no tracking cookies" contradicts privacy page; partners unnamed — trust
- Testimonials anonymous ("— a happy customer", "— a user", "— anonymous") — trust
- Features nav link returns 404 — technical
- hero.png is 3.9 MB, LCP 5.8 s on mobile — technical

## Coverage gaps
- Features page never seen (404)
- Sceptic never opened Pricing or scrolled the home page past the fold sections (`sections_seen: 1`)
- No tablet viewport

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-*/timeline.json`, `persona-*/session.log`
- C. Screenshot index — evaluator 00–06, sceptic 00–02
