# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the three comprehension axes — what / who / next step — scored against `shape_v1` before any scrolling
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — **⚠ INFERRED** (`persona_mode: generic`)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 11bffa267e42 — Neither persona could say what the product does; the landing page never names the category
- **Severity:** P0
- **So what:** Two of two visitors left a 200-word page still guessing the category from the brand name.
- **Framework tags:** V1-what, time-to-comprehension
- **Flow:** shape_v1
- **Locator:** /index.html h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `time_to_comprehension_seconds: null` and `understood_what: false` for both personas; both `guessed: true`.
  - The h1 is "Your thoughts, everywhere." — a benefit with no noun for what is being sold.
  - "notes" appears on the landing page once as a common noun, inside the unattributed quote "Finally, notes that sync." — a user.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md` · `crawl/html/1-index.html`
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said."
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page."
- **Repro:**
  1. Open `http://localhost:8765/` at 1440×900, logged out.
  2. Without scrolling, name the product category using only words visible on screen.
  3. The only available noun is the wordmark "Nimbus Notes".
- **Fix:** Add a plain-language line under the h1 naming the category and the job — e.g. "Nimbus Notes is a notes app that keeps every note on your devices, in sync and offline."

### 2169d8fd212b — The nav item that promises an explanation of the product returns a 404
- **Severity:** P1
- **So what:** The one destination named for explaining what the product does has no page behind it.
- **Framework tags:** V3-dead-end, V1-what
- **Flow:** shape_v3
- **Locator:** /features.html
- **Personas hit:** evaluator
- **Observed:**
  - `Features` is the second item in the header nav on every page.
  - It returns HTTP 404: `<h1>404</h1><p>That page does not exist.</p>`.
  - The evaluator clicked it at 03:30, 100 seconds after failing to find a price.
- **Evidence:** `persona-evaluator/screenshots/04-features-404.png` · `persona-evaluator/session.log:23` · `crawl/index.json` (`features.html`, status 404) · `crawl/html/2-features.html`
  > "Clicked 'Features' in the nav. Got a 404 page: 'That page does not exist.'"
- **Repro:**
  1. From any page, click `Features` in the header nav.
  2. A 404 page renders.
- **Fix:** Publish `/features.html` with one plain-language section per capability, or remove the nav item until it exists.

### cb71072a74e6 — The plainest description of the product is on the About page, two clicks from the fold
- **Severity:** P1
- **So what:** The site already owns the sentence that would have fixed comprehension and keeps it where nobody lands.
- **Framework tags:** placement, V1-what
- **Flow:** shape_v3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `/about.html` answers in plain words: "Nimbus Notes stores every note on your device first and syncs when a connection returns."
  - The same page answers export ("a folder of Markdown files") and data location ("In the EU (Frankfurt) by default").
  - Both personas found it and both said it belonged elsewhere; the evaluator reached it at 03:50, the sceptic at 01:30.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12` · `crawl/html/4-about.html`
  > "The About page has questions and answers — works offline, can export, data in Frankfurt. Those are actual answers. Why isn't this on the home page?"
  > "That's the answer I wanted and it's on the About page, not the Privacy page."
- **Repro:**
  1. Read the landing page fold; note no plain description of the product.
  2. Open `/about.html` and read the FAQ answers.
- **Fix:** Move the three About FAQ answers onto the landing page as a "What it does" section, and keep About for the company.

### 4bc2c2ec9d54 — The hero's only descriptive sentence rests on two terms neither persona could define
- **Severity:** P1
- **So what:** The single sentence that explains the product is unreadable to the visitor it is aimed at.
- **Framework tags:** jargon, V1-what
- **Flow:** shape_v1
- **Locator:** /index.html .hero p
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The subhead reads "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - The evaluator named both terms as undefinable at 00:18, 18 seconds in.
  - "What is a sync graph?" was still in `questions_unanswered` at the end of a 6.5-minute session.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` · `persona-evaluator/timeline.json` (`shape_v3.questions_unanswered`) · `persona-evaluator/persona-debrief.md`
  > "'bi-directional sync graph with a zero-knowledge vault' — I don't know what either of those means. I'll assume it syncs."
- **Repro:**
  1. Open the landing page and read the sentence below the h1.
  2. State what "bi-directional sync graph" and "zero-knowledge vault" mean to a buyer of a notes app.
- **Fix:** Rewrite the subhead in the outcome the visitor wants ("works offline, syncs when you reconnect, encrypted so only you can read it") and move the two technical terms to a features page.

### a6888f2a3732 — The site never says who it is for, and the two pages that hint at it disagree
- **Severity:** P1
- **So what:** Neither persona could decide whether the product was for them, so neither could act.
- **Framework tags:** V1-who
- **Flow:** shape_v1
- **Locator:** /index.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - `understood_who: false` for both personas.
  - The only audience signal on the landing page is the below-fold heading "Loved by teams".
  - `/pricing.html` heads "Plans for every team" while its first card reads "Starter — For individuals."
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6` · `crawl/html/3-pricing.html` · `persona-evaluator/persona-debrief.md`
  > "I can't tell. The top of the page names nobody. 'Loved by teams' lower down suggests teams. Maybe me, maybe not."
  > "Is it for individuals or teams?"
- **Repro:**
  1. Read the landing page fold and name the intended user.
  2. Open `/pricing.html` and compare "Plans for every team" with "Starter — For individuals."
- **Fix:** Name the audience in the hero, and make the pricing page consistent with it — one heading, one audience, per plan card.

### 3a76ff1ab094 — At 390px the headline is clipped and the entire subhead is unreadable off the right edge
- **Severity:** P1
- **So what:** On a phone the only sentence that explains the product does not exist on screen.
- **Framework tags:** mobile-fold, V1-what
- **Flow:** shape_v1
- **Locator:** /index.html at 390px
- **Personas hit:** sceptic
- **Observed:**
  - At the sceptic's verified 390×844 viewport the h1 renders as "Your thoughts, everywh" and is cut by the right edge.
  - Both subhead lines are cut mid-word: "A bi-directional sync graph with a zero-kno" and "vault, so nothing you write is ever lost or e".
  - Reproduced independently in the measurement capture at the same width, so it is not a screenshot artifact.
  - The sceptic saw one section and lost interest at 00:30.
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `measure/screenshots/index-mobile.png` · `persona-sceptic/timeline.json` (`viewport_verified: true`, `sections_seen: 1`, `point_of_lost_interest: "00:30"`)
  > "Headline 'Your thoughts, everywhere.' and a purple picture that takes the whole screen."
- **Repro:**
  1. Open `http://localhost:8765/` at 390×844.
  2. The h1 and both subhead lines overflow the right edge; no horizontal scroll recovers them in the fold.
- **Fix:** Constrain `.hero h1` and `.hero p` to the viewport width with wrapping, and re-test the fold at 360px and 390px.

### cfe5c7db8c3d — Nothing on the site depicts the product; the hero image is a decorative abstract
- **Severity:** P1
- **So what:** The visitor has no non-verbal route to comprehension, so the copy failure has no backstop.
- **Framework tags:** demonstration, V1-what
- **Flow:** shape_v1
- **Locator:** /index.html .hero img
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - The hero image is two overlapping purple circles, marked up as `<img src="assets/hero.svg" alt="">` — decorative, no product content.
  - No screenshot, recording or interactive demo appears on any of the four pages that returned 200.
  - Both personas said in the debrief that nothing showed the promise happening.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `crawl/html/1-index.html` · `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
  > "Close but off — the line is on the page, but nothing shows me it happening, and the page around it is about vaults and graphs."
  > "No — nothing on the site shows it remembering anything; the button that might have doesn't work."
- **Repro:**
  1. Open the landing page and every nav destination.
  2. Look for any depiction of the product interface. There is none.
- **Fix:** Replace the abstract hero with an annotated screenshot of a note syncing between two devices, captioned in plain words.
- **Note:** Readable as P2 on its own; both personas raised it unprompted in the debrief, which decided the higher grade.

### 2b4cd29e4e6d — The How it works section calls the same object a card, a block, a graph and a vault
- **Severity:** P2
- **So what:** The one section meant to explain the product left the visitor counting nouns instead of understanding it.
- **Framework tags:** consistency, jargon
- **Flow:** shape_v2
- **Locator:** /index.html .card
- **Personas hit:** evaluator
- **Observed:**
  - Capture: "Write a card. It joins the graph instantly." Sync: "Blocks flow between devices through the vault."
  - Four nouns — card, block, graph, vault — appear across three cards with nothing defining any of them.
  - The evaluator asked at 01:10 whether a card and a block were different things.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14` · `crawl/html/1-index.html`
  > "The cards say 'card', the sync one says 'blocks'. Are those different things?"
- **Repro:**
  1. Scroll to "How it works" on the landing page.
  2. Read the three card bodies and count the distinct nouns for the thing being synced.
- **Fix:** Use one noun — "note" — in all three cards, and drop "graph" and "vault" from this section.

### 20afda009f6d — Pricing explains cost by workspace type and sync topology, terms the visitor cannot self-assess
- **Severity:** P2
- **So what:** The sentence meant to explain the price asks the visitor a question about themselves they cannot answer.
- **Framework tags:** jargon, V1-next
- **Flow:** shape_v3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - `/pricing.html` closes with "Pricing depends on your workspace type and sync topology."
  - Neither term is defined anywhere on the four pages that returned 200.
  - "What is a workspace type?" remained in the evaluator's `questions_unanswered` at the debrief.
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `crawl/html/3-pricing.html` · `persona-evaluator/persona-debrief.md`
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`.
  2. Read the grey line under the plan cards and try to place yourself in it.
- **Fix:** Replace that line with the two variables a buyer knows — number of people and storage — or delete it.

### eb2661bbcf18 — The fold's only product CTA is outlined and low-contrast while the brightest block is the newsletter
- **Severity:** P2
- **So what:** The evaluator could not tell what the page wanted them to do, so the next-step axis failed outright.
- **Framework tags:** V1-next
- **Flow:** shape_v1
- **Locator:** /index.html .hero a.cta
- **Personas hit:** evaluator
- **Observed:**
  - `understood_next_step: false` for the evaluator; the only fold CTA is a thin outlined "See it in action" at the bottom edge of the 900px fold.
  - Immediately below the hero, the solid purple "Get the Nimbus newsletter / Subscribe" block is the highest-contrast element on the page.
  - The nav offers only "Log in" — no trial or signup affordance, though the stated conversion goal is a self-serve trial.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-evaluator/timeline.json` (`shape_v1.understood_next_step: false`)
  > "There's a small outlined 'See it in action' button. The newsletter box below it is much bigger and brighter than that button."
- **Repro:**
  1. Open the landing page at 1440×900 and name the action the page wants.
  2. Scroll one screen; the newsletter block outweighs the hero CTA.
- **Fix:** Make the hero CTA the solid primary button, demote the newsletter box to the footer, and add a self-serve trial link to the nav.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Mobile comprehension may also be delayed by the 5.8s LCP — no persona log line ties the sceptic's confusion to load time.
- The hero image caption text visible in both landing screenshots is fixture scaffolding, not site copy — not scored.
- Whether a clearer explanation exists behind the login — `/app/` was not crawled (robots.txt) and the auth wall is never reported.

## For other lenses
- "See it in action" is `href="#"` and does nothing on click or tap — **technical** (`persona-evaluator/session.log:12`, `persona-sceptic/session.log:13`).
- No price in currency anywhere; every plan says "Contact sales", leading to a seven-field form with a required phone number — **conversion**.
- Cookie bar says "We use no tracking cookies on this site" while `/privacy.html` describes cookies and unnamed partners — **trust**.
- Three testimonials attributed to "a happy customer", "a user", "anonymous" — **trust**.
- `ReferenceError: nimbusBootstrap is not defined` on load at both viewports; mobile LCP 5800ms; 3.9MB hero PNG — **technical**.
- `/pricing.html` carries `meta name="robots" content="noindex"` — **seo**.

## Coverage gaps
- `/features.html` — the page that would explain the product returned 404, so its content could not be assessed.
- Desktop mobile-fold behaviour between 390px and 1440px never sampled; only the two persona viewports were captured.
- The sceptic never opened `/pricing.html`, so the pricing-comprehension findings rest on one persona.
- Nothing behind `Log in` was seen; `/app/` is disallowed by robots.txt.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md` · `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json` · `persona-sceptic/timeline.json`
- C. Screenshot index — `persona-evaluator/screenshots/` (7) · `persona-sceptic/screenshots/` (3) · `measure/screenshots/` (4)
