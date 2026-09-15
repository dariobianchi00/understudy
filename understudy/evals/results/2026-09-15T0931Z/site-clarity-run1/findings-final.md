# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: comprehension on three axes — what / who / next step — scored against reality, not effort
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 721df09c8000 — Neither persona could say what Nimbus Notes does; both answered from the brand name
- **Severity:** P0
- **So what:** Two visitors spent a combined 9 minutes on the site and left still guessing what it sells.
- **Framework tags:** what, time-to-comprehension
- **Flow:** shape_v1
- **Locator:** /index.html .hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds` is `null` in both `timeline.json` files; `understood_what: false`, `guessed: true` for both.
  - Both Q1 answers are explicitly sourced from the brand name, not from any page.
  - Scroll depth reached 100% for both personas without changing the answer.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-sceptic/persona-debrief.md`
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said."
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page."
- **Repro:**
  1. Open `http://localhost:8765/` at 1440×900, logged out.
  2. Read only what is above the fold — `"Your thoughts, everywhere."` and the subhead.
  3. Try to state what the company sells without using the word "Nimbus".
- **Fix:** Rewrite the `<h1>`/subhead pair on `/index.html` to name the category and the job in plain words — e.g. "Notes that sync across your laptop and phone, and work offline" — before any brand line.

### 6601fca71003 — The only sentence describing the product uses three terms the visitor could not define
- **Severity:** P1
- **So what:** The one explanatory line on the fold spends its whole budget on words the visitor has to skip.
- **Framework tags:** what, jargon
- **Flow:** shape_v1
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - The evaluator named two of the terms as undefined at 00:18 and fell back to an assumption.
  - "What a 'sync graph' is" is listed in the evaluator's Q4 — a question the site never answered.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json`
  > "'bi-directional sync graph with a zero-knowledge vault' — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open `/index.html` at 1440×900.
  2. Read the paragraph directly under the headline.
- **Fix:** Replace the hero paragraph on `/index.html` with the About page's own wording — "stores every note on your device first and syncs when a connection returns" — and move "zero-knowledge" to a security section where it can be explained.

### 6985e24d19db — The clearest plain-English description of the product is two clicks away on the About page
- **Severity:** P1
- **So what:** The sentence that would have answered "what is this" in ten seconds is on the page a visitor reaches last, if ever.
- **Framework tags:** what, placement
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` answers offline behaviour, export and data location in three jargon-free question-and-answer pairs.
  - The evaluator reached it at 03:50, after a 404, a pricing dead end and a seven-field form, and asked why it was not on the home page.
  - The sceptic found their data-location answer there too, and noted it was not on the page that should carry it.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/index.html`, read the hero.
  2. Open `/about.html` and read "Frequently asked questions".
  3. Compare which page tells you what the product does.
- **Fix:** Promote the three About FAQ answers onto `/index.html` as a "How it works" replacement, and keep `/about.html` for the company details.

### 02328b34014b — The site never names its audience above the fold; the only audience words sit on the pricing page
- **Severity:** P1
- **So what:** Both visitors finished the session unable to say whether the product was meant for them.
- **Framework tags:** who
- **Flow:** shape_v1
- **Locator:** /index.html section.proof h2
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` for both personas in `timeline.json`.
  - The only audience words on `/index.html` are the heading "Loved by teams", below the fold at 01:25.
  - `/pricing.html` does segment — "For individuals." and "For growing teams." — but the evaluator read that page at 01:55 and still answered "I can't tell".
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/findings-raw.json`
  > "I can't tell. The top of the page names nobody. 'Loved by teams' lower down suggests teams. Maybe me, maybe not."
  > "For who? Doesn't say."
- **Repro:**
  1. Open `/index.html` and read the fold.
  2. Open `/pricing.html` and read the plan subtitles.
  3. Note that neither surface states who the product is for in the visitor's own terms.
- **Fix:** Add an audience line to the `/index.html` hero — name individuals and teams explicitly — and repeat it as a "Which plan am I?" line on `/pricing.html`.

### 84a2e660e0dc — At 390px the headline and the explanatory sentence are cut off mid-word
- **Severity:** P1
- **So what:** On the device the sceptic used, the sentence meant to explain the product is physically unreadable.
- **Framework tags:** what, fold, mobile
- **Flow:** shape_v1
- **Locator:** /index.html .hero at 390x844
- **Personas hit:** sceptic
- **Observed:**
  - At 390×844 the `<h1>` renders as "Your thoughts, everywh" and the subhead as "…with a zero-kno" / "…ever lost or e", clipped at the right edge.
  - The "About" nav item is clipped to "Abo" in the same capture.
  - An independent measurement capture at the same viewport shows identical clipping, so this is the rendered page, not a screenshot artifact.
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `measure/screenshots/index-mobile.png` · `persona-sceptic/session.log:6`
  > "What is it? Notes, I think. For who? Doesn't say."
- **Repro:**
  1. Open `http://localhost:8765/` at 390×844.
  2. Observe the headline and hero paragraph truncated at the right viewport edge.
- **Fix:** Constrain `.hero` and `header nav` to the viewport width on `/index.html` — wrap the nav and allow the `h1` to break — so the whole headline and subhead are readable at 390px.

### bfc737a56ff4 — Pricing is explained in terms the visitor cannot apply to themselves
- **Severity:** P2
- **So what:** The one line that could have explained the pricing model asks the visitor a question about themselves they cannot answer.
- **Framework tags:** jargon, next-step
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - `/pricing.html` closes with "Pricing depends on your workspace type and sync topology."
  - The evaluator could not map either term to anything they had.
  - "What a 'workspace type' is" appears in their Q4 list of things the site never told them.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/persona-debrief.md`
  > "'Pricing depends on your workspace type and sync topology.' I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the grey line under the three plan cards.
- **Fix:** Replace that line on `/pricing.html` with the variables a visitor knows — number of people and storage — or delete it.

### 07d6fd69bdaa — The newsletter box outweighs the only product CTA on the desktop fold
- **Severity:** P2
- **So what:** The evaluator read the page's loudest element as the ask, and finished the fold unsure what the site wanted.
- **Framework tags:** next-step
- **Flow:** shape_v1
- **Locator:** /index.html .news
- **Personas hit:** evaluator
- **Observed:**
  - "See it in action" is a small outlined link; the newsletter block immediately below is a full-width solid purple panel with an input and a Subscribe button.
  - `understood_next_step: false` for the evaluator in `timeline.json`.
  - The sceptic, at 390px, did identify the CTA — `understood_next_step: true` — so this does not hold across both personas.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8`
  > "There's a small outlined 'See it in action' button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open `/index.html` at 1440×900.
  2. Compare the visual weight of "See it in action" with the "Get the Nimbus newsletter" panel.
- **Fix:** Make "See it in action" the solid primary button on `/index.html` and demote the newsletter block to a plain footer row.

### 38cb93a7c1b3 — Adjacent How it works cards call the same object a card and a block
- **Severity:** P2
- **So what:** The section meant to explain the product introduced a second unexplained noun instead.
- **Framework tags:** what, consistency
- **Flow:** shape_v2
- **Locator:** /index.html section.how .card
- **Personas hit:** evaluator
- **Observed:**
  - "Capture" reads "Write a card. It joins the graph instantly."; "Sync" reads "Blocks flow between devices through the vault."
  - The evaluator asked at 01:10 whether these were different things, and the page never says.
  - "How it works" is the site's only attempt to describe the mechanism on the landing page.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say 'card', the sync one says 'blocks'. Are those different things?"
- **Repro:**
  1. Open `/index.html` and scroll to "How it works".
  2. Read the "Capture" and "Sync" cards in sequence.
- **Fix:** Pick one noun — "note" — and use it in all three "How it works" cards on `/index.html`.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The hero image may itself be misread as the product UI — no persona said anything about what the purple graphic depicts.
- "Zero-knowledge" may mislead about what staff can read — no persona stated an interpretation of the term, only that they could not define it.
- Whether a clearer `/features.html` existed — the page 404s, so nothing about its copy was observed.

## For other lenses
- "See it in action" is a `href="#"` that does nothing when clicked or tapped — technical.
- No price in currency anywhere; "Contact sales" leads to a seven-field form with a required phone number — conversion.
- Cookie bar says "We use no tracking cookies on this site" while `/privacy.html` describes cookies and unnamed partners — trust.
- Three testimonials attributed to "a happy customer", "a user", "anonymous" — trust.
- `/features.html` 404s from the primary nav — technical, seo.

## Coverage gaps
- `/features.html` never read — the nav link 404s.
- Pricing and the demo form were never opened on mobile; the sceptic left at 02:50.
- No tablet viewport tested.
- Logged-in app never seen by either persona.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00-06`, `persona-sceptic/screenshots/00-02`, `measure/screenshots/index-mobile.png`
