# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery (first-value Q4) first; then A2 jargon/reading level, A4 naming, A9 error and empty-state copy
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on inferred personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | Empty "Nothing here yet."; her note vanished twice; Memories listed facts that are not hers | Fail | Quit at 06:30 with zero notes; "I'd stop here" |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Save that does not save, search that finds nothing, fabricated Memories | Fail | Stopped at 03:00; would not switch the team or pay |

- Both Q4 answers agree with this reading: novice "No — it started completely empty, it lost what I gave it"; power-user "It remembers nothing I gave it and claims things I didn't."
- Root cause: the pitch is "remembers"; the product forgets what it is given and "remembers" what it was never given. Findings 1–3 are three faces of that one contradiction.

## Copy sample — reading level and jargon
- Persona-facing copy is short, ~grade 6–8 sentence level; the problem is vocabulary, not sentence length.
- Jargon a novice cannot explain to a friend, 6 terms on 2 screens: "Federated graph", "Sovereign vault", "Hybrid mesh", "webhook sync", "graph replication", "Vault attestation".
- Clear copy, praised by both personas: "Export" / "Markdown, all cards"; "0 words" / "Preview below".

---

## Findings

### 3e67f197f45d — "Saved ✓" confirms a save that never reaches the list or search
- **Severity:** P0
- **So what:** The product's own confirmation is false; both personas concluded it lies and stopped trusting every other message.
- **Framework tags:** A1, A9, B-trust, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save shows green "Saved ✓", returns to dashboard, which still reads "Nothing here yet."
  - Searching the exact title returns "No results for 'Dentist'." / no results for "Roadmap"
  - Novice repeated it twice with the same result; both gave up on the objective
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png`
  > "Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "Save doesn't save and search doesn't search."
- **Repro:**
  1. Open "New block", enter a title and body
  2. Click Save; observe "Saved ✓"
  3. Observe "Your cards" still reads "Nothing here yet."; search the title
- **Fix:** Show "Saved ✓" only after the save is confirmed, and show a plain-language failure message with a retry when it is not.

### c8bda5d64211 — Memories page presents invented facts as "What Nimbus remembers about you"
- **Severity:** P0
- **So what:** Confident false statements about the user's own life; novice extended the distrust to "Saved", power-user wrote the feature off.
- **Framework tags:** A2, B-trust, C-TRUST
- **Flow:** shape_2b
- **Locator:** Memories page
- **Personas hit:** novice, power-user
- **Observed:**
  - Page lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — no accounts connected, no note saved
  - Nothing labels these as examples or demo data
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-power-user/session.log:14`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a new workspace with no connected accounts
  2. Click "Memories"
- **Fix:** Remove the placeholder memories; when there are none, say so and state what the user must do for Nimbus to start remembering.

### 284a601091f7 — Empty first screen contradicts the "never start from zero" promise
- **Severity:** P1
- **So what:** The novice came for a notes app that fills itself in; the first screen proves the pitch false and she quit at 06:30.
- **Framework tags:** A2, B-G1, C-TTFV, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Arrived on "remembers everything so you never start from zero", expecting it to fill itself in
  - First screen after signup: "Your cards" / "Nothing here yet."
  - No copy explains where remembered content would come from or how to connect it
- **Evidence:** `persona-novice/session.log:2` · `persona-novice/session.log:3` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/persona-debrief.md`
  > "I thought it would have my stuff."
  > "No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine."
- **Repro:**
  1. Arrive from the marketing site line "remembers everything so you never start from zero"
  2. Sign up and land on the dashboard
- **Fix:** Either change the marketing line to match an empty-start notes app, or make the first screen deliver on it by importing or connecting the user's existing material.

### cdf144ad506b — Irreversible workspace choice is offered only in undefined jargon
- **Severity:** P2
- **So what:** The novice made a permanent decision by guessing from the name; a less persistent user stops here before seeing the product.
- **Framework tags:** A2, A5, B-G2
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh" — no descriptions
  - "This cannot be changed later." beneath the options
  - Novice picked "Hybrid mesh" because it "sounds like it includes the other two"
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall and reach /app/signup.html
  2. Read the three workspace options
- **Fix:** Describe each workspace type in one line of everyday language on the signup screen, stating what the user gains or loses with each.

### 8de4f7260f55 — Settings toggles use engineering terms with no explanation
- **Severity:** P2
- **So what:** The novice cannot tell what any toggle does, so she cannot safely change anything; trust in the product erodes.
- **Framework tags:** A2, A10
- **Flow:** shape_2b
- **Locator:** Settings page
- **Personas hit:** novice
- **Observed:**
  - Three toggles labelled "Enable webhook sync", "Federated graph replication", "Vault attestation", with no helper text
  - "Federated graph replication" is on by default
  - The only item she understood was "Export" / "Markdown, all cards"
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23`
  > ""Enable webhook sync", "Federated graph replication", "Vault attestation". No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Click "Settings"
- **Fix:** Add one line of plain-language helper text under each Settings toggle saying what it does for the user.

### e2ab5a323e69 — Settings reuses the signup term "Federated graph" without saying if they are linked
- **Severity:** P2
- **So what:** The user cannot tell whether this toggle controls the permanent signup choice; it is on even for the novice who chose "Hybrid mesh".
- **Framework tags:** A4, A2
- **Flow:** shape_2b
- **Locator:** Settings page: Federated graph replication
- **Personas hit:** power-user, novice
- **Observed:**
  - Signup offers "Federated graph" as a workspace type; Settings shows "Federated graph replication" checked
  - The toggle is checked in the novice's Settings although she picked "Hybrid mesh"
  - No copy links or distinguishes the two
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:11` · `persona-novice/screenshots/01-signup-workspace-type.png`
  > ""Federated graph replication" is on by default. I picked that at signup — is this the same thing?"
- **Repro:**
  1. Sign up choosing "Hybrid mesh"
  2. Open Settings; observe "Federated graph replication" checked
- **Fix:** Rename the Settings toggle so it shares no words with the workspace types, or state on it which workspace type it belongs to.

### 2c88ec46d436 — One object is called "notes", "cards" and "block" on four surfaces
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, slowing her first attempt to write.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** top nav: Cards / New block
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; dashboard: "Search your notes" above "Your cards"
  - Editor heading: "New block"; Settings export: "Markdown, all cards"
  - Marketing promise and persona both say "notes"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Land on the dashboard; read the nav, search placeholder and list heading
  2. Click "New block"
- **Fix:** Pick one noun ("notes" matches the search box and the persona) and use it in the nav, editor heading, list heading and export label.

### fa98af3b394b — Dashboard empty state "Nothing here yet." gives no next step
- **Severity:** P2
- **So what:** The first screen misses the activation moment; the novice searched an empty product before finding how to write.
- **Framework tags:** A9, A10, B-G1
- **Flow:** shape_1
- **Locator:** /app/dashboard.html empty state
- **Personas hit:** novice
- **Observed:**
  - "Your cards" shows only "Nothing here yet."
  - No link or instruction to create a first note
  - Novice searched "meeting" before finding "New block" at 01:40
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14`
  > "Nothing tells me what to do."
- **Repro:**
  1. Sign up and land on the dashboard with no notes
- **Fix:** Add to the dashboard empty state one sentence saying how to add a first note, with a button that opens the editor.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Wording of the "Saved ✓" toast itself — `persona-novice/screenshots/04-note-saved-toast.png` shows the empty editor, not the toast; the claim rests on `session.log:17` only.
- Wording of search no-results messages ("No results for 'meeting'.") — in the log, never screenshotted; copy is accurate given an empty store.

## For other lenses
- Notes are not persisted and search returns nothing after save — bugs.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — ux (`persona-power-user/session.log:12`).
- Radio buttons sit visually detached from their labels on signup and Settings — ux.
- Irreversible decision placed before any value — onboarding.

## Coverage gaps
- Marketing site never captured; promise rests on the pre-session note only.
- Export not exercised, so its output copy is unverified.
- Power-user did not screenshot Memories; his reaction is cited from the log.
- No error states other than empty search were reached.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast, 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
