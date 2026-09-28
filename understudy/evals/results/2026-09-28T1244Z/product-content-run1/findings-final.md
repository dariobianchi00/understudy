# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery first, then A2 jargon/reading level, A4 naming, A9 error and empty-state copy
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on invented personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | "Nothing here yet."; two "Saved ✓" notes that never appeared; three "memories" that are not hers | Fail | Stopped at 06:30 with zero notes; distrust spread from Memories to "Saved" |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Capture that said "Saved ✓" and kept nothing; search that found nothing; invented memories | Fail | Gave up at 03:00; "Nothing" he would pay |

- Persona Q4 agrees with this reading for both: novice "No — it started completely empty, it lost what I gave it"; power-user "It remembers nothing I gave it and claims things I didn't."
- The pitch's own verb — "remembers" — is contradicted twice: user content forgotten, fabricated content "remembered".

## Reading level and jargon (copy the personas met)

- Signup: "Federated graph", "Sovereign vault", "Hybrid mesh" — 3 jargon terms, 0 explanations; graduate/engineering register.
- Settings: "Enable webhook sync", "Federated graph replication", "Vault attestation" — 3 jargon terms, 0 explanations.
- Everyday screens ("Title", "Body", "0 words", "Preview below", "Save") — plain, fine for both personas.
- Jargon clusters at the two moments a novice must decide something, including one labelled "This cannot be changed later."

---

## Findings

### 62068f5beace — "Saved ✓" confirmation claims a save that the cards list and search never show
- **Severity:** P0
- **So what:** The product's own words told both personas their note was kept; it was not, so every later message reads as a lie.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows "Saved ✓"; dashboard then reads "Nothing here yet." (novice twice, power-user once)
  - Search for the saved title returns "No results for 'Dentist'." — no reason, no next step
  - Screenshots 03 and 04 both show the empty New block form; the toast itself is not captured, only logged
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/session.log:11`
  > "It said saved." · "It is lying to me." · "Save doesn't save and search doesn't search."
- **Repro:**
  1. Open New block, enter title "Dentist" and body text, click Save.
  2. Note the "Saved ✓" confirmation.
  3. Return to dashboard: "Nothing here yet."; search "Dentist": "No results for 'Dentist'."
- **Fix:** Show "Saved ✓" only after the card appears in "Your cards"; on failure, say the note was not saved and offer retry.

### 685e6b947e0f — Memories page presents invented facts as "What Nimbus remembers about you"
- **Severity:** P0
- **So what:** Confident nonsense about her own life made the novice doubt every other claim the product made, including "Saved".
- **Framework tags:** A2, B-G2, C-ABANDON
- **Flow:** shape_2b
- **Locator:** nav > Memories
- **Personas hit:** novice
- **Observed:**
  - Heading "What Nimbus remembers about you" over "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footnote "Memories are built from your notes and connected accounts." — she had no saved notes and connected nothing
  - Directly delivers the pitch's word "remembers" with content that is not hers
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a fresh workspace; connect nothing.
  2. Click Memories in the top nav.
  3. Read three specific personal claims attributed to "your notes and connected accounts".
- **Fix:** Remove seeded memories; with no sources, show an empty state that says memories come from notes the user saves.

### b531f46fe21d — Invented Memories are written off by the power user as a demo panel he will not trust
- **Severity:** P1
- **So what:** The feature carrying the product's headline promise is dismissed on sight by the evaluator deciding whether to switch a team.
- **Framework tags:** A2, B-G2
- **Flow:** shape_2b
- **Locator:** nav > Memories
- **Personas hit:** power-user
- **Observed:**
  - Read the same three claims: "Tuesday meetings, Jira, Q4 launch. Not me."
  - Classified the page as fake rather than broken: "a demo panel, I assume"
  - Debrief Q4 cites it: "claims things I didn't"
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md`
  > "Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a fresh workspace.
  2. Open Memories.
  3. Read claims unrelated to anything entered.
- **Fix:** Label any sample content as sample on the Memories page, or ship it empty until real notes exist.

### 8231a37ef42a — Empty home screen says only "Nothing here yet." against a promise of "never start from zero"
- **Severity:** P1
- **So what:** The first screen contradicts the pitch and gives no next step; the novice's first action was a search in an empty product.
- **Framework tags:** A2, A9, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" empty state reads "Nothing here yet." — no explanation, no link to create or import
  - Novice expected "a notes app that fills itself in from things I already have"
  - Searched "meeting" first; hunted twice before finding "New block"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:3` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/timeline.json`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a workspace.
  2. Land on dashboard.
  3. Read the "Your cards" panel.
- **Fix:** Rewrite the dashboard empty state to say what fills it and link directly to creating the first note.

### f0d878bdfe1a — Irreversible workspace choice is written in unexplained infrastructure jargon
- **Severity:** P2
- **So what:** The novice made a permanent decision by guessing, before seeing the product; a less patient user leaves here.
- **Framework tags:** A2, A5
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Options "Federated graph", "Sovereign vault", "Hybrid mesh" carry no descriptions
  - Warning "This cannot be changed later." sits directly under them
  - Picked "Hybrid mesh" after 43s because it "sounds like it includes the other two"
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it."
- **Repro:**
  1. Clear the login wall; land on signup.
  2. Read "Before we begin, choose your workspace type".
- **Fix:** Give each workspace option a one-line plain-language description and a recommended default, or defer the choice.

### 162dccd5f51b — One object is called card, block and note across nav, dashboard and search
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, adding a hunt to her first task.
- **Framework tags:** A4
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; dashboard heading "Your cards"; search placeholder "Search your notes"
  - Form heading "New block"; export label "Markdown, all cards"
  - Pitch and personas both say "notes"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Cards and blocks — same thing?"
- **Repro:**
  1. Read the top nav, the dashboard heading and the search placeholder.
  2. Open New block and read its heading.
- **Fix:** Pick one user-facing noun (the pitch uses "notes") and apply it to nav, headings, placeholder and export label.

### 054ca8451ebc — Settings labels are unexplained engineering terms a non-technical user cannot act on
- **Severity:** P2
- **So what:** Three of four settings are unreadable to the novice, so Settings offers her nothing beyond Export.
- **Framework tags:** A2
- **Flow:** shape_2b
- **Locator:** nav > Settings
- **Personas hit:** novice
- **Observed:**
  - "Enable webhook sync", "Federated graph replication", "Vault attestation" — no helper text
  - "Federated graph replication" is on by default
  - "Export" with "Markdown, all cards" was the one label she understood
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24`
  > "No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Click Settings in the top nav.
  2. Read the three checkbox labels.
- **Fix:** Add a one-line plain-language description under each Settings toggle saying what it changes for the user.

### c5fad9f12d22 — Settings "Federated graph replication" reuses the signup term without saying if it is the same thing
- **Severity:** P2
- **So what:** The evaluator could not tell whether his irreversible signup choice was now a toggle, undermining the "cannot be changed" warning.
- **Framework tags:** A4, A2
- **Flow:** shape_2b
- **Locator:** nav > Settings
- **Personas hit:** power-user
- **Observed:**
  - Chose "Federated graph" at signup, told "This cannot be changed later."
  - Settings shows "Federated graph replication" checked, with no link to the workspace type
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-power-user/session.log:8` · `persona-power-user/session.log:13`
  > "I picked that at signup — is this the same thing?"
- **Repro:**
  1. Pick "Federated graph" at signup.
  2. Open Settings and read "Federated graph replication".
- **Fix:** Show the chosen workspace type on Settings as read-only text, and rename the toggle so it is visibly a separate option.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Wording of the "Saved ✓" toast and "No results for '…'" copy — only logged; 04-note-saved-toast.png shows the empty form, no toast.
- Novice's typed note and live preview — 03-new-note.png shows an empty form ("0 words"), so preview copy could not be checked.

## For other lenses
- Notes not persisted; search returns nothing for saved titles — bugs.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux.
- Irreversible choice demanded before any product exposure — onboarding.

## Coverage gaps
- Marketing page carrying "remembers everything so you never start from zero" was not captured; promise taken from pre-session lines.
- No connected-accounts flow exists or was reached, so the Memories footnote's source claim could not be tested.
- Export output never opened.
- Desktop 1440×900 only.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — novice 00–07; power-user 00, 02, 03, 07
