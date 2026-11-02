# Nimbus Notes — clarity findings — Run 2026-09-08 (fixture01)

## Method
- Framework: comprehension on three axes (what / who / next step), timed against the V1 fold
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator, desktop 1440×900; sceptic, iPhone 13 390×844)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 4cb8133d3618 — Neither visitor could say what Nimbus Notes does; both guessed "notes app" from the brand name
- **Severity:** P0
- **So what:** Comprehension never arrived for either visitor (`time_to_comprehension_seconds: null` ×2); the page did not explain the product.
- **Framework tags:** C-WHAT, C-TTC
- **Flow:** V1 — Land
- **Locator:** .hero h1
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Headline "Your thoughts, everywhere." names no product category, no job, no outcome
  - Both visitors said their "notes app" answer came from the name "Nimbus Notes", not the page
  - Evaluator still could not say what it does "beyond 'notes that sync'" at 05:45, after five pages
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:6` · `persona-evaluator/session.log:9` · `persona-evaluator/session.log:28` · `persona-sceptic/session.log:6` · `timeline.json` → `shape_v1.time_to_comprehension_seconds: null` (both)
  > "Some kind of notes app that syncs between devices — I'm going from the name and one line halfway down the page; the headline never said." — evaluator, Q1
  > "A notes app that is supposed to remember things — I'm guessing from the name and from what my friend said, not from the page." — sceptic, Q1
- **Repro:**
  1. Open `/index.html` at 1440×900 or 390×844
  2. Read only the fold; try to state what the product does without using the word in the brand name
- **Fix:** Rewrite the h1 to say what it is and does in plain words (e.g. "Notes that sync between your laptop and phone"), keeping the slogan as a subline.
- P0 not P1: neither persona completed the V1 job; graded P0 per the "torn → P0" rule, a reader may downgrade to P1.

### 2d7b2b49d87d — Nothing above the fold says who Nimbus Notes is for; individuals vs teams is left unanswered
- **Severity:** P2
- **So what:** The evaluator came to judge whether it "could replace what my team uses" and could not place himself; churn risk for every team buyer.
- **Framework tags:** C-WHO
- **Flow:** V1 — Land
- **Locator:** .hero
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Fold names no audience; first audience signal is "Loved by teams", mid-page
  - Pricing then says "Plans for every team" yet Starter is "For individuals."
  - Evaluator listed "Whether it's for individuals or teams" in Q4; sceptic: "The page doesn't say."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:7` · `persona-sceptic/session.log:6`
  > "I can't tell. The top of the page names nobody. "Loved by teams" lower down suggests teams. Maybe me, maybe not." — evaluator, Q2
- **Repro:**
  1. Open `/index.html`
  2. Look for any named audience in the fold — there is none
- **Fix:** Add the audience to the hero subline ("for individuals and small teams") and match it to the plan names on /pricing.html.

### 189b1f13e746 — Fold subhead "bi-directional sync graph" and "zero-knowledge vault" is jargon the visitor could not define
- **Severity:** P2
- **So what:** The only descriptive sentence on the fold explained nothing; the visitor had to "assume it syncs".
- **Framework tags:** C-JARGON, C-WHAT
- **Flow:** V1 — Land
- **Locator:** .hero p
- **Personas hit:** evaluator
- **Observed:**
  - Subhead: "A bi-directional sync graph with a zero-knowledge vault, so nothing you write is ever lost or exposed."
  - Evaluator could define neither term at 00:18; "What a "sync graph" is" recurs in Q4
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:10` · `persona-evaluator/findings-raw.json` (00:18)
  > "'bi-directional sync graph', 'zero-knowledge vault' — I don't know what either means."
- **Repro:**
  1. Open `/index.html`
  2. Read the line under the h1
- **Fix:** Replace the subhead with the plain outcome ("Everything you write is saved on your device, synced everywhere, and encrypted so only you can read it").

### f53ed3049a9d — The promise that brought both visitors, "remembers everything", is buried in the third How-it-works card
- **Severity:** P2
- **So what:** Both arrived on "remembers everything"; the fold never confirmed they were in the right place, and both rated promise match "close but off" / "no".
- **Framework tags:** C-WHAT, C-PROMISE
- **Flow:** V2 — Orient
- **Locator:** #how
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "Nimbus remembers everything so you never start from zero." appears only in the "Remember" card, below the newsletter box
  - Evaluator found it at 00:55, after scrolling; sceptic never scrolled to it
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:2` · `persona-evaluator/session.log:13` · `persona-sceptic/session.log:2`
  > "Close but off — the line is on the page, but nothing shows me it happening, and the page around it is about vaults and graphs." — evaluator, Q6
- **Repro:**
  1. Open `/index.html`
  2. Scroll past the hero and newsletter to "How it works" to find the line
- **Fix:** Promote "Nimbus remembers everything so you never start from zero" into the hero, above or as the h1.

### 766e80bcfe3c — "See it in action" does nothing, so neither visitor ever saw what the product does
- **Severity:** P2
- **So what:** The one route to seeing the product was dead; both visitors' unanswered "what does it actually do" stayed unanswered.
- **Framework tags:** C-WHAT, C-NEXT
- **Flow:** V2 — Orient
- **Locator:** .hero a.cta
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Evaluator clicked twice at 00:40; page did not move
  - Sceptic returned at 02:20 specifically to see it "remember"; tap did nothing; left at 02:40
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/session.log:14` · DOM: `<a class="cta" href="#">See it in action</a>`
  > "No — nothing on the site shows it remembering anything; the button that might have doesn't work." — sceptic, Q6
- **Repro:**
  1. Open `/index.html`
  2. Click "See it in action" — nothing happens
- **Fix:** Point "See it in action" at a 30-second product clip or screenshot sequence showing a note captured on one device and found on another.

### dca4b59348c5 — The newsletter box outweighs the only product button, so the fold's next step reads as "subscribe"
- **Severity:** P2
- **So what:** The visitor's eye went to an email ask before any product explanation; next step was misread or skipped.
- **Framework tags:** C-NEXT
- **Flow:** V1 — Land
- **Locator:** .news
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - "See it in action" is a small outlined button; "Get the Nimbus newsletter" is a full-width solid purple band
  - Both visitors named the newsletter box in their first "what does it want me to do" answer
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:8` · `persona-evaluator/session.log:14` · `persona-sceptic/session.log:6`
  > "The newsletter box is bigger and brighter than the button that shows the product."
- **Repro:**
  1. Open `/index.html`
  2. Compare the visual weight of "See it in action" with the "Get the Nimbus newsletter" band
- **Fix:** Make one solid primary CTA in the hero ("Start free trial" or "See it in action") and move the newsletter band to the footer.

### a90589d46625 — Pricing note "workspace type and sync topology" uses terms the visitor could not define
- **Severity:** P2
- **So what:** The only explanation of price was unintelligible; the evaluator could not even tell which plan he was.
- **Framework tags:** C-JARGON
- **Flow:** V3 — Evaluate
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Pricing footnote: "Pricing depends on your workspace type and sync topology."
  - Evaluator at 02:10: does not know his workspace type; listed "What a "workspace type" is" in Q4
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:18` · `timeline.json` → `shape_v3.questions_unanswered`
  > "I don't know what my workspace type is. I haven't got one."
- **Repro:**
  1. Open `/pricing.html`
  2. Read the line under the three plan cards
- **Fix:** Replace the footnote with what the price actually depends on, in visitor terms (e.g. "per person, per month").

### d18324f7559b — How it works uses "card", "blocks", "graph" and "vault" without saying if they are the same thing
- **Severity:** P2
- **So what:** Four undefined nouns in three cards; the section meant to explain the product added confusion instead.
- **Framework tags:** C-JARGON
- **Flow:** V2 — Orient
- **Locator:** #how .card
- **Personas hit:** evaluator
- **Observed:**
  - "Write a card. It joins the graph instantly." / "Blocks flow between devices through the vault."
  - Evaluator at 01:10 asked whether cards and blocks differ; nowhere says "note"
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:14`
  > "The cards say "card", the sync one says "blocks". Are those different things?"
- **Repro:**
  1. Open `/index.html#how`
  2. Read the Capture and Sync cards
- **Fix:** Use one word — "note" — across the How-it-works cards and drop "graph", "blocks" and "vault" from that section.

### e1e4f2a7619d — The site's clearest plain-English answers sit in the About-page FAQ, not on the home page
- **Severity:** P2
- **So what:** Offline, export and data location are answered plainly — two clicks deep, where the sceptic found them only by accident.
- **Framework tags:** C-PLACEMENT, C-WHAT
- **Flow:** V3 — Evaluate
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About FAQ: "Nimbus Notes stores every note on your device first and syncs when a connection returns."
  - Evaluator 04:20: "Why isn't this on the home page?"; sceptic 01:50 found data location here, not on Privacy
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:12`
  > "Those are actual answers. Why isn't this on the home page?"
- **Repro:**
  1. Open `/about.html`
  2. Compare the FAQ answers with the home-page hero copy
- **Fix:** Move the three About-page FAQ answers onto the home page directly below the hero.

### 1d9ae407f309 — Hero visual is two abstract circles that show nothing of the product
- **Severity:** P2
- **So what:** The largest element on the fold — the whole phone screen — carried zero information about what Nimbus does.
- **Framework tags:** C-WHAT
- **Flow:** V1 — Land
- **Locator:** .hero img
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Hero image is two overlapping lilac circles; no interface, no note, no device
  - Both visitors described it only as a "purple" picture
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:5` · `persona-sceptic/session.log:5`
  > "Headline "Your thoughts, everywhere." and a purple picture that takes the whole screen." — sceptic
- **Repro:**
  1. Open `/index.html`
  2. Look at the hero image
- **Fix:** Replace the hero image with a product screenshot showing the same note on a laptop and a phone.

### 6918ff16421d — On iPhone 13 the fold clips the headline and the only descriptive sentence mid-word
- **Severity:** P2
- **So what:** On mobile even the weak explanation that exists is cut off: "everywh…", "zero-kno…", "lost or e…".
- **Framework tags:** C-FOLD
- **Flow:** V1 — Land
- **Locator:** .hero (390px)
- **Personas hit:** sceptic
- **Observed:**
  - At 390px the h1, subhead, nav ("Abo…") and hero image overflow the right edge
  - Sceptic did not remark on the clipping; no observed behaviour change, hence P2 not P1
- **Evidence:** `persona-sceptic/screenshots/00-landing.png` · `timeline.json` → `viewport: 390×844, verified: true`
- **Repro:**
  1. Open `/index.html` at 390×844
  2. Observe headline and subhead cut at the right edge
- **Fix:** Constrain the hero text and image to the viewport width on mobile so the h1 and subhead wrap instead of overflowing.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Features page might explain the product better — the persona got a 404, so its content was never seen.

## For other lenses
- Pricing shows "Contact sales" on all three plans, no numbers — conversion
- "Contact sales" lands on a seven-field demo form with phone required — conversion
- Cookie bar "We use no tracking cookies" vs privacy page cookies and unnamed partners — trust
- Testimonials attributed to "a happy customer", "a user", "anonymous" — trust
- "Features" nav link returned a 404 for the evaluator (`04-features-404.png`) — technical
- Hero image area renders fallback text instead of an image (`00-landing.png`) — technical

## Coverage gaps
- Sceptic (mobile) never scrolled the home page or opened /pricing.html; mobile mid-page comprehension untested
- Features page content never seen by any persona (404)
- No persona reached the free-trial path in `conversion_goal`; none exists on the pages visited

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-*/timeline.json`, `persona-*/session.log`
- C. Screenshot index — `persona-evaluator/screenshots/00–06`, `persona-sceptic/screenshots/00–02`
