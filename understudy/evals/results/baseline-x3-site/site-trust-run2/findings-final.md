# Nimbus Notes — trust findings — Run 2026-09-08 (fixture01)

## Method
- Framework: the four trust questions — is this real · what does it cost · who is behind it · what happens to my data — plus objections answered / partly / ignored / made worse
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (evaluator on desktop 1440×900, sceptic on iPhone 13)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Not a compliance review; nothing here says whether any policy is legally sufficient
- Every finding is what the site says or does not say — never what the company does

---

## Findings

> **⚑ This block is machine-parsed.** `check_report.py` reads it field by field
> and fails closed — a field it cannot find is treated as absent, and an absent
> `Flow` silently changes the finding's ID. **Keep every field on its own
> bullet; never merge them onto one line with `·` separators.** A `·` inside a
> field's value is fine and expected (several artifacts on one Evidence line);
> it is only the field bullets themselves that must stay separate.
>
> **The `<finding-id>` is computed, never composed** — see the lens agent's
> Output section for the `finding_id.py` invocation. Write the block first, then
> hash exactly the `flow`, `locator` and `title` strings you wrote.

### 7a4fb3a2e97c — Cookie bar says no tracking cookies while a third-party tracker loads and the privacy page says cookies are used
- **Severity:** P0
- **So what:** Both personas caught the contradiction unprompted; it undid the trust the About page had built and was the sceptic's stated reason to leave.
- **Framework tags:** data-handling, consistency
- **Flow:** V3
- **Locator:** /index.html#cookie-bar
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Landing bar reads "We use no tracking cookies on this site."; privacy page reads "We use cookies and similar technologies."
  - Network log on landing: `analytics.example-tracker.test/t.js` (38 KB, third-party) then `POST …/collect?uid=8f3a…` → 204, before any consent choice is recorded.
  - Whether that call sets a cookie is not in the capture; the visible contradiction and the uid-bearing tracker call are.
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/network-full.txt:4` · `persona-evaluator/network-full.txt:5` · `persona-sceptic/screenshots/00-landing.png` · `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/network-full.txt:2` · `persona-sceptic/network-full.txt:3` · `persona-evaluator/session.log:27` · `persona-sceptic/session.log:10`
  > "The cookie bar said no tracking. This page says they use cookies and share with partners. Which is it?" — evaluator, 05:20
  > "The bar said no tracking cookies. This page says they use cookies. One of those is wrong." — sceptic, 01:05
- **Repro:**
  1. Open `/` with network recording on; read the black bar at the bottom.
  2. Note the requests to `analytics.example-tracker.test` fired on load.
  3. Open `/privacy.html` and read the second and third sentences.
- **Fix:** Make the bar and the policy say the same thing — either remove the third-party tracker and keep "no tracking cookies", or replace the bar with a banner that names the analytics provider and what it collects.

### be3098951ecc — No plan shows a price; every card says Contact sales and the footnote adds jargon instead of a reason
- **Severity:** P1
- **So what:** The evaluator came to check price, gave up at 02:30, and said "Money, no" — the site lost the one visitor who was ready to compare.
- **Framework tags:** pricing-transparency, claim-quality
- **Flow:** V3
- **Locator:** /pricing.html
- **Personas hit:** evaluator
- **Observed:**
  - Three cards — "Starter", "Team", "Enterprise" — each with a single "Contact sales" button and no number.
  - Footnote: "Pricing depends on your workspace type and sync topology." The evaluator: "I don't know what my workspace type is."
  - "Contact sales" routes to the seven-field demo form on the home page; the sceptic never looked for a price (objective not attempted).
- **Evidence:** `persona-evaluator/screenshots/02-pricing.png` · `persona-evaluator/session.log:17` · `persona-evaluator/session.log:18` · `persona-evaluator/session.log:19` · `persona-evaluator/timeline.json` (`price_found: false`, `gave_up: true`) · `persona-evaluator/persona-debrief.md`
  > "Every one says 'Contact sales'. No numbers anywhere." — evaluator, 01:55
  > "Money, no — I don't know what they'd charge." — evaluator debrief Q5
- **Repro:**
  1. Click "Pricing" in the top nav.
  2. Look for any currency figure on the three cards or the footnote.
  3. Click "Contact sales" — lands on the home-page demo form.
- **Fix:** Put a number on "Starter" (even "Free" or "from £X/user/month"), and replace the footnote with a plain-English reason enterprise pricing is quoted.

### 472ead18f72a-a — Privacy page names no partners the site shares data with
- **Severity:** P1
- **So what:** The sceptic's whole visit was "what happens to my notes"; the site answered "partners and service providers" and lost her at 02:40.
- **Framework tags:** data-handling, claim-quality
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** sceptic
- **Observed:**
  - Policy is one paragraph: "We may share information with partners and service providers to improve your experience." No partner, provider or category is named.
  - "We may update this policy at any time." — no date, no version, no contact other than "Questions? Use the demo form."
  - `questions_unanswered` in the sceptic timeline: "Who are the partners you share with?"; verdict "left; data handling unclear".
- **Evidence:** `persona-sceptic/screenshots/01-privacy.png` · `persona-sceptic/session.log:9` · `persona-sceptic/session.log:14` · `persona-sceptic/timeline.json` · `persona-sceptic/persona-debrief.md`
  > "With whom? Not said. 'We may update this policy at any time.' That's not a privacy policy, that's a shrug." — sceptic, 00:45
  > "Leave. The cookie bar and the privacy page disagree, and the privacy page won't say who the partners are." — sceptic debrief Q3
- **Repro:**
  1. Tap "Privacy" in the footer on a phone.
  2. Read the single paragraph; look for any named third party.
- **Fix:** On `/privacy.html`, list the categories of third party (hosting, analytics, email) with the actual providers, and add a last-updated date and a privacy contact address.

### 472ead18f72a-b — Privacy page names no partners the site shares data with
- **Severity:** P2
- **So what:** For the evaluator the vague policy was a trust nick, not the exit — price was — but it left "Data, unsure" as the debrief answer.
- **Framework tags:** data-handling
- **Flow:** V3
- **Locator:** /privacy.html
- **Personas hit:** evaluator
- **Observed:**
  - Same page, same paragraph; evaluator listed "Who are the partners you share data with?" as unanswered.
  - Reached Privacy at 04:50 after About had made the company "feel real"; the policy then "undid that".
- **Evidence:** `persona-evaluator/screenshots/06-privacy.png` · `persona-evaluator/session.log:26` · `persona-evaluator/timeline.json` · `persona-evaluator/persona-debrief.md`
  > "'We may share information with partners and service providers.' Which partners? It doesn't say." — evaluator, 04:50
  > "Data, unsure. The About page made them feel real (a named founder, an address). The privacy page and the cookie bar contradicting each other undid that." — evaluator debrief Q5
- **Repro:**
  1. Click "Privacy" in the footer on desktop.
  2. Read the paragraph; look for any named third party.
- **Fix:** Same as 472ead18f72a-a — name the providers and date the policy.

### 95ad446aa3a2 — The site's only concrete trust answers live on About, not on Privacy or the home page
- **Severity:** P2
- **So what:** Founder, address, company number and "data in Frankfurt" were the only things either persona believed — and both found them by accident, after trust had already dropped.
- **Framework tags:** provenance, data-handling, consistency
- **Flow:** V3
- **Locator:** /about.html
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - About: "Nimbus Notes Ltd, a company of eight people founded in 2023 by Priya Raman … 14 Harbourside Walk, Bristol … Company number 14482201."
  - About FAQ answers "Where is my data stored? In the EU (Frankfurt) by default." — the privacy page says nothing about location.
  - Both personas logged About as `trust_up`; evaluator reached it at 03:50, sceptic at 01:30, neither via the privacy page or the home page.
- **Evidence:** `persona-evaluator/screenshots/05-about.png` · `persona-sceptic/screenshots/02-about.png` · `persona-evaluator/session.log:24` · `persona-evaluator/session.log:25` · `persona-sceptic/session.log:11` · `persona-sceptic/session.log:12`
  > "That's the first thing on this site that felt like a real business." — evaluator, 03:50
  > "That's the answer I wanted and it's on the About page, not the Privacy page." — sceptic, 01:50
  > "Those are actual answers. Why isn't this on the home page?" — evaluator, 04:20
- **Repro:**
  1. Open `/privacy.html` — no storage location, no company identity.
  2. Open `/about.html` — both present.
- **Fix:** Repeat the company line and the Frankfurt answer on `/privacy.html`, and add a one-line "Made by Nimbus Notes Ltd, Bristol · data stored in the EU" strip to the home-page footer.

### a213ae12f121 — See it in action does nothing, so nothing on the site shows the product exists
- **Severity:** P2
- **So what:** The only offer of proof the product is real is a dead button; the sceptic's promise check ("it remembers everything") ended "No".
- **Framework tags:** proof, claim-quality
- **Flow:** V3
- **Locator:** /index.html#see-it-in-action
- **Personas hit:** evaluator, sceptic
- **Observed:**
  - Outlined button "See it in action" under the hero; evaluator clicked twice at 00:40, sceptic tapped at 02:20 — no navigation, no scroll, no modal.
  - No screenshot, video, or product image anywhere in the capture; the hero is two abstract circles.
  - Sceptic logged it under `trust_down`; her Q6 answer: "nothing on the site shows it remembering anything; the button that might have doesn't work."
- **Evidence:** `persona-evaluator/screenshots/00-landing.png` · `persona-sceptic/screenshots/00-landing.png` · `persona-evaluator/session.log:12` · `persona-sceptic/session.log:13` · `persona-sceptic/timeline.json` · `persona-sceptic/persona-debrief.md`
  > "I want to see it 'remember' something. The button does nothing when I tap it." — sceptic, 02:20
- **Repro:**
  1. Open `/`, click "See it in action".
  2. Observe no change in URL, scroll position or DOM.
- **Fix:** Point "See it in action" at a 30-second product recording or a real screenshot of a note syncing, and put that image in the hero in place of the circles.

### dd6906d4dfe5 — All three testimonials are anonymous and the visitor said outright they did not believe them
- **Severity:** P2
- **So what:** The "Loved by teams" section is the site's only social proof and it subtracted trust instead of adding it.
- **Framework tags:** proof
- **Flow:** V2
- **Locator:** /index.html#loved-by-teams
- **Personas hit:** evaluator
- **Observed:**
  - Three quotes attributed to "— a happy customer", "— a user", "— anonymous". No name, company, role or number.
  - Evaluator logged it as `trust_down: "Anonymous testimonials"` at 01:25 — also the `point_of_lost_interest`.
  - Sceptic went straight to the footer and did not read this section (`sections_seen: 1`).
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:15` · `persona-evaluator/timeline.json`
  > "'— a happy customer', '— a user', '— anonymous'. Nobody has a name. I don't believe these." — evaluator, 01:25
- **Repro:**
  1. Open `/`, scroll to "Loved by teams".
  2. Read the attribution under each quote.
- **Fix:** Replace the three quotes with one named customer (person, company, what changed, a number) — or remove the section until one exists.

### 784bad2d71d8 — Demo form requires a phone number before the visitor has seen the product
- **Severity:** P2
- **So what:** The only route to a price asks for seven fields including a required phone; the evaluator backed out at 03:15 without submitting.
- **Framework tags:** data-handling, pricing-transparency
- **Flow:** V3
- **Locator:** /index.html#demo
- **Personas hit:** evaluator
- **Observed:**
  - Fields counted by the persona: first name, last name, work email, phone number, company, company size, what do you want to see — seven; phone required.
  - "Contact sales" on every pricing card and "Questions? Use the demo form." on Privacy both land here.
  - Evaluator logged `trust_down: "Phone number required for a demo"`; `forms_opened: 1`, `forms_submitted: 0`.
- **Evidence:** `persona-evaluator/screenshots/01-scrolled.png` · `persona-evaluator/session.log:20` · `persona-evaluator/session.log:21` · `persona-evaluator/session.log:22` · `persona-evaluator/timeline.json`
  > "Seven. Phone is required. I haven't seen the product and they want my phone number." — evaluator, 02:58
- **Repro:**
  1. Click "Pricing" → "Contact sales" on any card.
  2. Count the fields in "Book a demo"; note the required marker on phone.
- **Fix:** Drop phone (or make it optional) and cut the form to name, work email and one free-text field until the visitor has seen a price or a demo.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Privacy page routes questions to the sales demo form ("Questions? Use the demo form.") — visible in `06-privacy.png` but no persona reacted to it; listed so a future run watches for it.
- The demo form itself — `persona-evaluator/screenshots/03-demo-form.png` captured blank; field count rests on `session.log:21` and the top of `01-scrolled.png` only.
- Whether the third-party analytics call sets a cookie — network log shows the tracker and a uid; no cookie jar was captured.

## For other lenses
- "Features" in the nav returns a 404 (`persona-evaluator/screenshots/04-features-404.png`, `session.log:23`) — bugs, conversion.
- "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology" undefined — clarity.
- Newsletter box outweighs the primary CTA; no self-serve trial anywhere despite conversion goal "Start a free trial without talking to sales" — conversion.
- Hero image is a 3.9 MB PNG with a placeholder caption visible in the screenshot — technical.

## Coverage gaps
- Sceptic never opened `/pricing.html` — price findings rest on the evaluator alone.
- Sceptic did not read "Loved by teams" or the demo form.
- No terms page exists in the nav or footer; neither persona looked for one.
- `03-demo-form.png` is blank — the form's required markers were not captured visually.
- Single visit per persona; the objective "find price without giving an email" was attempted by one persona only.

## Appendices
- A. Persona debriefs — `persona-evaluator/persona-debrief.md`, `persona-sceptic/persona-debrief.md`
- B. Session timelines — `persona-evaluator/timeline.json`, `persona-sceptic/timeline.json`
- C. Screenshot index — evaluator: 00-landing, 01-scrolled, 02-pricing, 03-demo-form (blank), 04-features-404, 05-about, 06-privacy · sceptic: 00-landing, 01-privacy, 02-about
