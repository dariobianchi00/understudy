# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Nielsen A2/A4/A9 for copy; HAX B-G2/B-G11 for the Memories surface; promise-vs-delivery (Q4) first
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on invented personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope exclusion applied: "The login wall at /app/login.html — infrastructure, not a defect."

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | Empty dashboard; two notes "Saved ✓" then gone; Memories full of facts that aren't hers | Fail | Gave up at 06:30 with zero notes; would pay nothing |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Note "Saved ✓" then gone; search finds nothing; Memories not his | Fail | Left at 03:00; "No. Nothing." |

- Both Q4 answers agree with this reading: novice "No — it started completely empty, it lost what I gave it"; power-user "It remembers nothing I gave it and claims things I didn't."
- Root cause: the pitch is "remembers", and both remembering surfaces (save, Memories) say things that are false. Most findings below are downstream of that.

---

## Findings

### 72dce02a52ad — "Saved ✓" confirms notes that never appear, breaking the "remembers everything" promise
- **Severity:** P0
- **So what:** The product's one promise is memory; its own confirmation copy is the line that proves it false, and both personas quit on it.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows "Saved ✓", then the dashboard still reads "Nothing here yet." (novice twice, power-user once)
  - Searching the saved title returns "No results for 'Dentist'." / no results for "Roadmap"
  - Novice generalised the false confirmation to the whole product: "It is lying to me."
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17-20` · `persona-power-user/session.log:11` · `persona-novice/persona-debrief.md` (Q4)
  > "Dashboard still says "Nothing here yet." … Where did it go?"
  > "It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Open New block, enter a title and body, click Save
  2. Observe "Saved ✓"; return to dashboard — "Nothing here yet."
  3. Search the title — no results
- **Fix:** Show "Saved ✓" only after the note is persisted and listed; on failure, say it was not saved and how to retry.

### 68239adf6184-a — Memories page asserts three facts about the user that neither persona ever supplied
- **Severity:** P0
- **So what:** Confident false statements about her own life made the novice doubt every other claim, including "Saved".
- **Framework tags:** A2, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/06-memories.png
- **Personas hit:** novice
- **Observed:**
  - Heading "What Nimbus remembers about you" over "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — she had zero saved notes and no connected accounts
  - No way to see why a memory exists or remove it
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a new workspace; save no notes, connect nothing
  2. Open Memories
- **Fix:** Show an empty Memories state until real memories exist, and label each memory with the note or account it came from.

### 68239adf6184-b — Memories page asserts three facts about the user that neither persona ever supplied
- **Severity:** P1
- **So what:** The power-user wrote it off as a demo and stated distrust; the surface that embodies "remembers everything" became noise.
- **Framework tags:** A2, B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/06-memories.png
- **Personas hit:** power-user
- **Observed:**
  - Same three statements: "Tuesday meetings, Jira, Q4 launch. Not me."
  - Read it as a placeholder rather than a lie; did not extend distrust to Save
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` (02:30) · `persona-novice/screenshots/06-memories.png` (same surface; no power-user screenshot captured)
  > "Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a new workspace; save no notes
  2. Open Memories
- **Fix:** Same as -a: empty state until real data, with a visible source on every memory.

### 35e93b11cad4 — Irreversible workspace choice is offered only in undefined jargon, before the user has seen the product
- **Severity:** P2
- **So what:** A novice guessed an irreversible setting from the sound of the words; the first screen tells her the product isn't for her.
- **Framework tags:** A2, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh" — no descriptions
  - "This cannot be changed later." sits under three undefined options
  - 3 of 3 options are jargon; novice picked by guess at 00:48
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9-11`
  > "I don't know what any of these are. It says I can't change it."
  > "Picked "Hybrid mesh" because it sounds like it includes the other two."
- **Repro:**
  1. Clear the login wall; land on signup
  2. Read the three workspace types
- **Fix:** Say in plain words what each workspace type means for the user's notes, or default it and move the choice into Settings.

### a8199d98ce86 — Settings labels three toggles in engineering jargon with no explanation
- **Severity:** P2
- **So what:** A non-technical user can't tell which setting affects her notes; only the Export line reads as plain English.
- **Framework tags:** A2, A10
- **Flow:** shape_2b
- **Locator:** persona-novice/screenshots/07-settings.png
- **Personas hit:** novice
- **Observed:**
  - "Enable webhook sync", "Federated graph replication", "Vault attestation" — no helper text
  - 3 of 4 settings require engineering vocabulary; "Markdown, all cards" was the one she understood
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23`
  > "No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Open Settings
- **Fix:** Add a one-line plain-language description under each toggle saying what it does to the user's notes.

### 46cc70161508 — Settings shows "Federated graph replication" on with no link to the workspace type chosen at signup
- **Severity:** P2
- **So what:** Reusing the signup term without explanation makes even the expert unsure what he committed to irreversibly.
- **Framework tags:** A4, A1
- **Flow:** shape_2b
- **Locator:** persona-power-user/screenshots/07-settings.png
- **Personas hit:** power-user
- **Observed:**
  - "Federated graph replication" is checked by default
  - Signup offered "Federated graph" as a workspace type; novice chose "Hybrid mesh" and her Settings shows the same box checked
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-novice/screenshots/07-settings.png` · `persona-power-user/session.log:13`
  > "I picked that at signup — is this the same thing?"
- **Repro:**
  1. Sign up choosing "Hybrid mesh" (or "Federated graph")
  2. Open Settings — "Federated graph replication" is on in both cases
- **Fix:** Rename one of the two terms, or state the chosen workspace type on the Settings page beside this toggle.

### 911f40b36747 — One object is called note, card and block across the core screens
- **Severity:** P2
- **So what:** The novice couldn't tell if "Cards" and "New block" were the same thing, adding a hunt to her first task.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** persona-novice/screenshots/02-dashboard-empty.png
- **Personas hit:** novice
- **Observed:**
  - Dashboard: "Search your notes" above "Your cards"; nav: "Cards", "New block"
  - Editor heading "New block"; Settings export "Markdown, all cards"
  - 3 names for 1 concept on 4 screens
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Cards and blocks — same thing?"
- **Repro:**
  1. Read the nav, dashboard heading, search placeholder and editor heading
- **Fix:** Pick one noun (the marketing word "notes") and use it in nav, headings, placeholders and export.

### 01de2b3dd8e6 — Dashboard empty state "Nothing here yet." gives no next step
- **Severity:** P2
- **So what:** A user promised "never start from zero" lands on zero with no instruction; the first activation moment is wasted.
- **Framework tags:** A2, A10, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" / "Nothing here yet." — no button, no pointer to "New block", no mention of imports
  - Novice spent 00:55–01:40 searching an empty product before finding New block
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12-14`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a new workspace; land on the dashboard
- **Fix:** Make the empty state tell the user how to add a first note and link straight to the editor.

### 47444cc73ec1 — Search no-results copy gives no reason or next step after a confirmed save
- **Severity:** P2
- **So what:** "No results" for a title the product just called saved offers no explanation, so the user can only conclude it lied.
- **Framework tags:** A9
- **Flow:** shape_2
- **Locator:** persona-power-user/screenshots/03-search-empty.png
- **Personas hit:** novice, power-user
- **Observed:**
  - "No results for 'Dentist'." seconds after "Saved ✓"
  - No suggestion, no indexing notice, no link to the note list
  - Screenshot 03-search-empty.png shows the empty dashboard, not the message; wording comes from the log
- **Evidence:** `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:19` · `persona-power-user/session.log:11`
  > "Typed "Dentist" in search. "No results for 'Dentist'." It said saved."
- **Repro:**
  1. Save a note titled "Dentist"
  2. Search "Dentist"
- **Fix:** When search is empty, say what was searched and offer a next action (check spelling, browse all notes, create one).

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast styling/placement — `04-note-saved-toast.png` shows a blank New block form, not the toast; wording rests on the log only
- Marketing-site wording beyond the one quoted promise — the site was never captured

## For other lenses
- Save does not persist and search returns nothing — bugs
- No keyboard shortcuts (Ctrl+K, Ctrl+N, / do nothing) for the power-user — ux
- Signup radio buttons render centred, detached from their labels — ux
- Irreversible choice before first value — onboarding

## Coverage gaps
- No power-user screenshot of Memories; -b variant cites the novice's
- Toast never captured on screen (04 shows the empty form)
- Marketing page carrying the promise not captured; promise known only from the pre-session note
- No error states other than search no-results were reached

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-*/timeline.json`
- C. Screenshot index — novice 00–07 (no 04 toast visible); power-user 00, 02, 03, 07
