# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: comprehension on three axes (what / who / next step), time-to-comprehension, jargon the visitor could not define
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator @ 1440×900, sceptic @ 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Flow values map to visit shapes: shape_v1 = Land, shape_v2 = Orient, shape_v3 = Evaluate

---

## Findings

### 4361895a5508 — Fold never says what Nimbus Notes is; both personas guessed 'notes app' from the name
- **Severity:** P0
- **So what:** Neither visitor could say what the product is from the page; both left, one inside 3 minutes.
- **Framework tags:** C-WHAT, C-TTC
- **Flow:** shape_v1
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Headline "Your thoughts, everywhere." names no product category; `time_to_comprehension_seconds` is `null` for both personas.
  - Evaluator: "the 'notes app' part is from the name, not the page." Sceptic: "guessing from the name and from what my friend said, not from the page."
  - Severity note: torn P0/P1 — the guess happened to be right, but the page itself never confirmed it, so comprehension is recorded as never reached.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-sceptic/session.log:6` · `persona-evaluator/timeline.json` shape_v1 · `persona-sceptic/timeline.json` shape_v1
  > "What do I think this is? Some kind of notes app, from the name. The headline doesn't say."
- **Repro:**
  1. Open `/` at 1440×900 or 390×844.
  2. Read the fold without scrolling.
  3. Try to state the product category from the page text alone.
- **Fix:** Replace the H1 with a category-naming line, e.g. "Notes that sync between your laptop and phone, and never forget", and keep "Your thoughts, everywhere." as the eyebrow.

### 03f0a02fe269 — Hero subhead is two undefined terms: 'bi-directional sync graph' and 'zero-knowledge vault'
- **Severity:** P1
- **So what:** The one sentence meant to explain the product is unreadable to the visitor, who fell back to "I'll assume it syncs."
- **Framework tags:** C-JARGON, C-WHAT
- **Flow:** shape_v1
- **Locator:** /index.html
- **Personas hit:** evaluator
- **Observed:**
  - Subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator at 00:18: "I don't know what either of those means."
  - "What is a sync graph?" is listed in the evaluator's `questions_unanswered` at session end.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/persona-debrief.md` Q4 · `persona-evaluator/timeline.json` shape_v3.questions_unanswered
  > "'bi-directional sync graph', 'zero-knowledge vault' — I don't know what either means."
- **Repro:**
  1. Open `/` at 1440×900.
  2. Read the grey subhead under the H1.
- **Fix:** Rewrite the subhead in the visitor's words: "Write on any device; every note is on all of them, encrypted so only you can read it."

### 369996aec440 — Fold names no audience; 'Loved by teams' and 'Starter: For individuals.' leave who-for unanswered
- **Severity:** P1
- **So what:** The evaluator came to check "whether this could replace what my team uses" and left saying "Maybe me, maybe not."
- **Framework tags:** C-WHO
- **Flow:** shape_v1
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Fold text names nobody; `understood_who` is `false` for both personas.
  - Landing section reads "Loved by teams"; Pricing "Starter" card reads "For individuals." — the two pages point at different audiences.
  - Evaluator Q2: "I can't tell. The top of the page names nobody." Sceptic Q2: "The page doesn't say."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6` · `persona-evaluator/persona-debrief.md` Q2 · `persona-sceptic/persona-debrief.md` Q2
  > "Who is it for? No idea. Me? Teams? It says 'Loved by teams' further down but the top doesn't say."
- **Repro:**
  1. Open `/` and read the fold; note no audience is named.
  2. Scroll to "Loved by teams".
  3. Open `/pricing.html`; read "Starter — For individuals."
- **Fix:** Add one audience line under the H1 ("For individuals and small teams") and use the same wording on the Pricing page.

### 5d08b9fba56e — 'See it in action', the only route to seeing the product, does nothing on click or tap
- **Severity:** P1
- **So what:** Both personas tried to see the product to understand it; the button failed, so "what it does" was never shown.
- **Framework tags:** C-NEXT, C-WHAT
- **Flow:** shape_v2
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator at 00:40: "Clicked 'See it in action'. Nothing happened. The page didn't move. Clicked again. Still nothing."
  - Sceptic at 02:20: "I want to see it 'remember' something. The button does nothing when I tap it."
  - Evaluator `understood_next_step` is `false`; the "Get the Nimbus newsletter" box directly below is larger and brighter than the button.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13`
  > "The button that might have doesn't work."
- **Repro:**
  1. Open `/` on desktop or phone.
  2. Click or tap "See it in action".
  3. Observe no scroll, modal, or navigation.
- **Fix:** Point "See it in action" at a real product screenshot or 20-second demo section on the landing page, and make it the visually dominant control above the newsletter box.

### 24d0ff074a0c — The site's clearest product answers sit in the About FAQ, two clicks from the landing page
- **Severity:** P2
- **So what:** The only plain-language facts about the product (offline, Markdown export, EU storage) are where a visitor looking for "what is this" never goes.
- **Framework tags:** C-PLACEMENT, C-WHAT
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Yes. Nimbus Notes stores every note on your device first and syncs when a connection returns." / "Settings → Export produces a folder of Markdown files" / "In the EU (Frankfurt) by default."
  - Evaluator at 04:20: "Those are actual answers. Why isn't this on the home page?"
  - Sceptic at 01:50: "That's the answer I wanted and it's on the About page, not the Privacy page."
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/`; scroll fully; note no plain feature facts.
  2. Open `/about.html`; read "Frequently asked questions".
- **Fix:** Move the three FAQ answers onto the landing page under "How it works", and link "Where is my data stored?" from the Privacy page.

### 4bd9912a01cc — 'Features' nav link returns a 404, so the page that would explain the product does not exist
- **Severity:** P2
- **So what:** The one nav item that promises "what does it do" delivers a raw server error, leaving the question unanswered.
- **Framework tags:** C-WHAT, C-DEADEND
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - Nav item "Features" is present on every page; clicking it renders "Error response / Error code: 404 / Message: File not found."
  - Evaluator at 03:30: "Clicked 'Features' in the nav. Got a 404 page."
  - Evaluator's debrief still says "I still don't know … exactly what it does beyond 'notes that sync'."
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `persona-evaluator/session.log:28`
  > "Features in the nav goes to a 404."
- **Repro:**
  1. Open `/`.
  2. Click "Features" in the top nav.
- **Fix:** Publish `/features.html` with the three "How it works" steps expanded in plain words, or remove "Features" from the nav until it exists.

### 2da6e29c2d9b — 'How it works' uses card, blocks, graph and vault without defining them; persona asked if they differ
- **Severity:** P2
- **So what:** The section meant to explain the mechanism introduces four nouns the visitor cannot map to anything, so it explains nothing.
- **Framework tags:** C-JARGON, C-WHAT
- **Flow:** shape_v2
- **Locator:** /index.html
- **Personas hit:** evaluator
- **Observed:**
  - Cards read "Write a card. It joins the graph instantly." / "Blocks flow between devices through the vault." / "Nimbus remembers everything so you never start from zero."
  - Evaluator at 01:10: "The cards say 'card', the sync one says 'blocks'. Are those different things?"
  - Only the third card ("Remember") matched the promise that brought the evaluator to the site.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:13` · `persona-evaluator/session.log:14`
  > "The cards say 'card', the sync one says 'blocks'. Are those different things?"
- **Repro:**
  1. Open `/`; scroll to "How it works".
  2. Read the three cards; note "card", "graph", "Blocks", "vault" are never defined.
- **Fix:** Use one word for the thing the user writes ("note") across all three cards, and drop "graph" and "vault" from the landing page.

### 65d19630ee3f — 'Pricing depends on your workspace type and sync topology': visitor cannot define either term
- **Severity:** P2
- **So what:** The only sentence explaining how price is set uses two terms the visitor cannot apply to themselves ("I haven't got one").
- **Framework tags:** C-JARGON
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Pricing footnote reads "Pricing depends on your workspace type and sync topology."
  - Evaluator at 02:10: "I don't know what my workspace type is. I haven't got one."
  - "What is a workspace type?" is in the evaluator's `questions_unanswered`.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `persona-evaluator/persona-debrief.md` Q4
  > "'Pricing depends on your workspace type and sync topology.' I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the grey line under the three plan cards.
- **Fix:** Replace the footnote with the actual variables in visitor terms ("price depends on how many people and how many devices") or delete it.

### ffc98c3d30e6 — At 390px the headline and subhead are clipped off the right edge of the fold
- **Severity:** P2
- **So what:** The phone visitor's fold reads "Your thoughts, everywh" and "zero-kno… lost or e"; the little explanation there is cannot be read in full.
- **Framework tags:** C-FOLD, C-MOBILE
- **Flow:** shape_v1
- **Locator:** /index.html
- **Personas hit:** sceptic
- **Observed:**
  - At 390×844 the H1, subhead, nav ("Abo") and hero image overflow the viewport horizontally.
  - Cookie bar "OK" button is outside the visible fold in the landing capture.
  - Sceptic's `understood_what` is `false`; the only fold copy visible was the truncated headline.
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/timeline.json` viewport · `persona-sceptic/session.log:5`
  > "Headline 'Your thoughts, everywhere.' and a purple picture that takes the whole screen."
- **Repro:**
  1. Open `/` at 390×844.
  2. Do not scroll; observe the H1 and subhead cut at the right viewport edge.
- **Fix:** Set the hero container to `max-width: 100%` with wrapping text and a fluid image so the H1 and subhead fit a 390px viewport.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Sceptic may also have missed the subhead entirely on mobile — no log line says whether she read it before tapping the cookie bar.
- Newsletter box may draw the eye away from the CTA on mobile — no mobile screenshot below the fold was captured.

## For other lenses
- Cookie bar "We use no tracking cookies on this site." contradicts Privacy page cookie/partner wording — trust.
- Testimonials attributed to "a happy customer", "a user", "anonymous" — trust.
- All three pricing plans say "Contact sales"; no numbers anywhere; objective "find out what it costs" failed — conversion, objectives.
- "Book a demo" form has seven fields with phone required before seeing the product — conversion.
- "See it in action" button has no working handler — bugs / technical.
- "Features" nav → 404 — seo, technical.
- Hero image alt/placeholder text ("a real capture serves assets/generated/hero.png") visible in the rendered hero — technical.

## Coverage gaps
- Sceptic never opened Pricing or Features (left early at 2:50; "That wasn't my question").
- No mobile capture of Pricing, Features, or below-the-fold landing sections.
- `/features.html` content never seen by any persona (404).

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/00-06`, `persona-sceptic/screenshots/00-02`
