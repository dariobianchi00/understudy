# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: clarity lens — can a first-time visitor say what this is, who it is for, and what to do next, and how fast
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (`persona_mode: generic`); findings rest on invented personas, not researched ones
- Personas run: evaluator (desktop 1440×900, verified) · sceptic (iPhone 13, 390×844, verified)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 9b557ff62a73 — Neither persona could say what Nimbus Notes is from the page; comprehension never reached
- **Severity:** P0
- **So what:** Both visitors left guessing "notes app" from the brand name; the page itself never told them, so nothing else on it could land.
- **Framework tags:** comprehension-what, time-to-comprehension, V1
- **Flow:** shape_v1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` and `understood_what: false`, `guessed: true` for both personas
  - Headline "Your thoughts, everywhere." names no product category, task, or outcome
  - Both Q1 answers credit the name, not the page; evaluator still unsure at 05:45 after visiting five pages
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-evaluator/session.log:28` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." (evaluator, Q1)
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." (sceptic, Q1)
- **Repro:**
  1. Open `/index.html` at 1440×900 or 390×844, cookie bar up.
  2. Read only the fold; try to state what the product does without using the word "Notes" from the logo.
- **Fix:** Rewrite the hero H1 to name the thing and the job in plain words (e.g. "Notes that sync between your laptop and phone"); keep "Your thoughts, everywhere." as an eyebrow if wanted.
- **P0 rationale:** torn with P1; chosen P0 because a visit's first value is comprehension and neither persona ever reached it.

### ee18f86df1f0 — Hero subhead explains the product only in undefinable jargon
- **Severity:** P2
- **So what:** The one descriptive line above the fold carried no meaning to the visitor, so it could not rescue the vague headline.
- **Framework tags:** jargon, comprehension-what, V1
- **Flow:** shape_v1
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator could define neither "bi-directional sync graph" nor "zero-knowledge vault"; fell back to assuming "it syncs"
  - "What is a sync graph?" recorded in `questions_unanswered` and repeated in debrief Q4
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/persona-debrief.md` Q4 · `crawl/html/1-index.html:11`
  > "'bi-directional sync graph with a zero-knowledge vault' — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open `/index.html`.
  2. Read the line under the H1.
- **Fix:** Replace the subhead with the outcome in everyday words ("Write on any device; it's on the others in seconds, and only you can read it"); move the technical terms to a details section.

### 0acee2ba13f9 — Evaluator could not tell whether the product is for individuals or teams
- **Severity:** P1
- **So what:** He came to judge whether it could replace his team's tool; the site never told him, and he ended the visit without an answer.
- **Framework tags:** comprehension-who, V1, V3
- **Flow:** shape_v1
- **Locator:** /index.html hero audience
- **Personas hit:** evaluator
- **Observed:**
  - Fold names no audience; first audience signal is "Loved by teams", several screens down
  - Pricing says "Plans for every team" above a "Starter — For individuals." card, so the signal stays mixed
  - "Is it for individuals or teams?" left in `questions_unanswered`; debrief Q2 "I can't tell"
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:3` · `persona-evaluator/session.log:7` · `persona-evaluator/session.log:29`
  > "I can't tell. The top of the page names nobody. \"Loved by teams\" lower down suggests teams. Maybe me, maybe not." (Q2)
- **Repro:**
  1. Open `/index.html` at 1440×900.
  2. Look for who the product is for above the fold; then check `/pricing.html`.
- **Fix:** Add one audience line to the hero (e.g. "For individuals and small teams") and make the pricing heading match it.

### 57997046e363 — Sceptic could not tell who the product is for
- **Severity:** P2
- **So what:** She shrugged it off because her question was about data, but a visitor checking fit would have had no answer on the phone fold.
- **Framework tags:** comprehension-who, V1
- **Flow:** shape_v1
- **Locator:** /index.html hero audience (mobile)
- **Personas hit:** sceptic
- **Observed:**
  - `understood_who: false`; she never scrolled the landing page (`sections_seen: 1`)
  - Mobile fold shows no audience statement
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:6` · `persona-sceptic/timeline.json` shape_v1
  > "The page doesn't say. Possibly me." (Q2)
- **Repro:**
  1. Open `/index.html` at 390×844.
  2. Look for who the product is for without scrolling.
- **Fix:** Same hero audience line as the desktop fix; check it fits the 390px fold without truncation.

### dc5c710e0f0a — Clearest product explanation sits on the About page, not the landing page
- **Severity:** P2
- **So what:** The plain answers that would have explained the product were found only by visitors who went looking for the company, not the product.
- **Framework tags:** placement, comprehension-what, V3
- **Flow:** shape_v3
- **Locator:** /about.html FAQ
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ says "Nimbus Notes stores every note on your device first and syncs when a connection returns." — the clearest description anywhere on the site
  - Also on About only: "Settings → Export produces a folder of Markdown files", data "In the EU (Frankfurt) by default"
  - Evaluator asked why it is not on the home page; sceptic found her answer there, not on Privacy
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/screenshots/02-about.png` · `persona-sceptic/session.log:12`
  > "Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/about.html`.
  2. Compare the FAQ answers with the copy on `/index.html`.
- **Fix:** Move the three FAQ answers (offline-first sync, Markdown export, Frankfurt storage) onto the landing page under the hero.

### 06159d48723f — Mobile fold clips the headline and subhead off the right edge
- **Severity:** P2
- **So what:** On a phone the visitor sees "Your thoughts, everywh…" and half a subhead, so even the weak hero copy arrives incomplete.
- **Framework tags:** fold, viewport, V1
- **Flow:** shape_v1
- **Locator:** /index.html .hero (390px)
- **Personas hit:** sceptic
- **Observed:**
  - At 390×844 the H1 and subhead run off the right edge: "Your thoughts, everywh", "with a zero-kno"
  - Nav is clipped too ("Abo"); "Log in" button is off-screen
  - Hero image fills most of the remaining fold; cookie bar covers the bottom
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/session.log:5`
  > "Headline \"Your thoughts, everywhere.\" and a purple picture that takes the whole screen."
- **Repro:**
  1. Open `/index.html` at 390×844 (iPhone 13).
  2. Look at the hero without scrolling horizontally.
- **Fix:** Let the hero H1, subhead and nav wrap at narrow widths so the full lines show within 390px.

### d4f9179febac — The only button promising to show the product does nothing
- **Severity:** P2
- **So what:** The one route to seeing the product work was dead, so neither visitor ever saw what "remembers everything" means.
- **Framework tags:** comprehension-next-step, promise-match, V2
- **Flow:** shape_v2
- **Locator:** /index.html a.cta "See it in action"
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" points to `href="#"`; evaluator clicked twice, sceptic tapped once — nothing happened
  - Evaluator rated next step unclear: the outlined button is smaller than the newsletter box below it
  - Both Q6 answers say nothing on the site shows the promised behaviour
- **Evidence:** `persona-evaluator/session.log:8` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-evaluator/screenshots/00-landing.png` · `crawl/html/1-index.html:12`
  > "\"It remembers everything.\" No — nothing on the site shows it remembering anything; the button that might have doesn't work." (sceptic, Q6)
- **Repro:**
  1. Open `/index.html`.
  2. Click "See it in action".
- **Fix:** Point "See it in action" at a short screen recording or interactive demo of a note syncing between two devices.

### 37d5cd3484b1 — Pricing note explains cost in terms the visitor cannot parse
- **Severity:** P2
- **So what:** The only sentence about how price is set was meaningless to him, so he could not even estimate which plan was his.
- **Framework tags:** jargon, V3
- **Flow:** shape_v3
- **Locator:** /pricing.html pricing note
- **Personas hit:** evaluator
- **Observed:**
  - Note reads "Pricing depends on your workspace type and sync topology."
  - "What is a workspace type?" recorded in `questions_unanswered` and debrief Q4
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18`
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the line under the plan cards.
- **Fix:** Replace the note with the actual pricing variable in plain words (e.g. "Priced per person per month").

### af74f42e5af8 — Landing page uses four nouns for the same unit without defining any
- **Severity:** P2
- **So what:** The visitor could not tell whether "card", "blocks", "graph" and "vault" were one thing or several, deepening the "what is this" gap.
- **Framework tags:** terminology, comprehension-what, V2
- **Flow:** shape_v2
- **Locator:** /index.html #how
- **Personas hit:** evaluator
- **Observed:**
  - "How it works" cards: "Write a card. It joins the graph instantly." / "Blocks flow between devices through the vault."
  - Product name says "Notes"; the page never uses "note" in these steps
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say \"card\", the sync one says \"blocks\". Are those different things?"
- **Repro:**
  1. Open `/index.html` and scroll to "How it works".
  2. Read the three cards.
- **Fix:** Call the unit "note" everywhere on the landing page and drop "card", "blocks", "graph" and "vault" from the How-it-works copy.

### 2b5a1fc33e41 — Hero visual is abstract circles that show nothing about the product
- **Severity:** P3
- **So what:** The largest element in the fold added no information; the visitor read it as "a purple blob".
- **Framework tags:** fold, V1
- **Flow:** shape_v1
- **Locator:** /index.html .hero img
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero image is two overlapping lilac circles; no interface, note, or device shown
  - On mobile it takes most of the fold below the CTA
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:5`
  > "A purple blob picture."
- **Repro:**
  1. Open `/index.html`.
  2. Look at the hero image.
- **Fix:** Replace the hero image with a screenshot of a note open on a laptop and a phone side by side.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Visible text in the hero image area ("…o.svg — a real capture serves assets/generated/hero.png…") — appears to be a fixture asset substitution, not site copy; no persona reacted to it.

## For other lenses
- Pricing shows no numbers; every plan "Contact sales"; evaluator gave up on the cost objective — conversion
- Demo form: seven fields, phone required — conversion
- Newsletter box visually outranks the primary CTA — conversion
- Anonymous testimonials ("— a happy customer", "— a user", "— anonymous") — trust
- Cookie bar "We use no tracking cookies on this site." vs privacy page cookies and unnamed partners — trust
- "Features" nav link returns a server 404 (`04-features-404.png`) — technical
- "See it in action" `href="#"` is a dead link — technical
- Meta description and JSON-LD reuse the "bi-directional sync graph" jargon; JSON-LD `price` is empty — seo / aeo

## Coverage gaps
- Sceptic never scrolled the landing page (`sections_seen: 1`); mobile mid-page comprehension untested
- `/features.html` returned 404, so any explanation it was meant to hold was never seen
- No persona arrived cold; both came primed with "notes" or "remembers everything", which likely flattered comprehension

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator: `00-landing` · `01-scrolled` · `02-pricing` · `03-demo-form` · `04-features-404` · `05-about` · `06-privacy`; sceptic: `00-landing` · `01-privacy` · `02-about`
