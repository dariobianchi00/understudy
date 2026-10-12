# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) · Layer B (HAX — applies: the Memories page is a user-facing AI surface) · Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Every screenshot cited below was opened; where a screenshot does not show what its filename claims, the log line carries the claim

---

## Findings

### df9b5e2adb6e — Save confirms with a success toast but the note never appears in the cards list or search
- **Severity:** P0
- **So what:** Both personas lost every note they wrote and gave up; the core objective "write a note and find it again" failed 3 of 3 attempts.
- **Framework tags:** A1, A9, C-ABANDON, C-TTFV, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice saved "Dentist" twice; "Saved ✓" appeared both times; dashboard still showed "Nothing here yet."; search returned "No results for 'Dentist'."
  - Power-user saved "Roadmap"; "Saved ✓"; dashboard empty; search for the title returned nothing.
  - Both timelines record the objective as `gave_up: true`; power-user `first_value_reached: false`.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/timeline.json` objectives[0].gave_up · `persona-power-user/timeline.json` objectives[0].gave_up
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "Nothing yet — it accepts a note and then loses it." (power-user debrief Q1)
- **Repro:**
  1. Create a workspace and click "New block".
  2. Enter a title and body; click "Save".
  3. Observe "Saved ✓", then the dashboard showing "Nothing here yet."
  4. Search the title; observe "No results".
- **Fix:** Show "Saved ✓" only after the note is persisted, and render the new card on the dashboard immediately so search finds it.

### dca4ed1b2aaf — Memories page asserts invented facts about the user, and the novice extends that distrust to Save
- **Severity:** P0
- **So what:** Confident claims about her own life that are false made the novice doubt every other message the product shows, including "Saved".
- **Framework tags:** B-G2, B-G11, B-G9, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** nav: Memories
- **Personas hit:** novice
- **Observed:**
  - Page "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footnote "Memories are built from your notes and connected accounts." — the persona had no saved notes and connected no accounts.
  - No control to remove or correct a memory is visible.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a fresh workspace with no notes and no connected accounts.
  2. Click "Memories" in the top nav.
  3. Observe three specific claims about the user.
- **Fix:** Show an empty Memories state until real notes exist, and attach each memory to the note it came from with a delete control.

### 3373b09c9d0b — Memories page asserts invented facts that the power user writes off as a demo and will not trust
- **Severity:** P1
- **So what:** The power user discounted the product's headline "remembers everything" feature as fake and said so in the debrief.
- **Framework tags:** B-G2, B-G11, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** nav: Memories
- **Personas hit:** power-user
- **Observed:**
  - Saw the same three memories (Tuesday meetings, Jira, Q4 launch) and judged them "Not me".
  - Classified the page as a demo panel and stated he would not trust it.
  - No power-user screenshot of Memories exists; finding rests on the log and debrief.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4 · `persona-novice/screenshots/06-memories.png` (same page content)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > "It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Create a fresh workspace.
  2. Click "Memories".
  3. Observe claims unrelated to any user input.
- **Fix:** Remove the seeded memories; if sample content is wanted, label it "Example" on the page itself.

### d1802c00058b — Signup forces an irreversible workspace-type choice between three unexplained terms
- **Severity:** P2
- **So what:** The novice guessed blind on a permanent decision before seeing the product; a less patient novice stops here.
- **Framework tags:** A2, A5, A3, A10, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Options "Federated graph", "Sovereign vault", "Hybrid mesh"; no descriptions; note "This cannot be changed later."
  - Novice hesitated 28 s (00:20–00:48), then picked "Hybrid mesh" "because it sounds like it includes the other two".
  - Power-user picked "Federated graph" without friction ("Fine — I've seen worse").
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Complete signup.
  2. Observe the "Before we begin, choose your workspace type" screen.
- **Fix:** Default the workspace type silently, or add one plain-language line per option and make it changeable in Settings.

### 1176b807d38f — Empty dashboard gives no next step and no way to start a first note
- **Severity:** P2
- **So what:** The novice's first screen after signup told her nothing to do; she searched an empty box before finding "New block".
- **Framework tags:** A10, A6, C-TTFV, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel shows only "Nothing here yet."; no button or prompt to create a note.
  - Novice searched "meeting" (01:20) before trying the nav at 01:40; timeline records `times_had_to_hunt: 2`.
  - She expected pre-filled content from the "remembers everything" promise.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/timeline.json` shape_2.times_had_to_hunt
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a new workspace.
  2. Observe the dashboard: "Nothing here yet." and no create action in the panel.
- **Fix:** Replace "Nothing here yet." with a "Write your first note" button opening the editor.

### a7ef933d0c3d — Same object is called card, block and note across nav, heading and search
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, adding a guess to every navigation step.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** nav: Cards / New block
- **Personas hit:** novice
- **Observed:**
  - Nav reads "Cards" and "New block"; dashboard heading "Your cards"; search placeholder "Search your notes".
  - Novice paused at 01:40 asking whether cards and blocks are the same, then clicked "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14`
  > "Cards and blocks — same thing?"
- **Repro:**
  1. Open the dashboard.
  2. Compare the nav labels, the "Your cards" heading and the "Search your notes" placeholder.
- **Fix:** Pick one noun ("note") and use it in the nav, the editor heading, the dashboard and the search placeholder.

### 7dd627905337 — Settings toggles use unexplained infrastructure terms with no help text
- **Severity:** P2
- **So what:** The novice understood one control out of four on Settings, so she cannot tell what any toggle does to her notes.
- **Framework tags:** A2, A10
- **Flow:** shape_2b
- **Locator:** nav: Settings
- **Personas hit:** novice
- **Observed:**
  - Toggles "Enable webhook sync", "Federated graph replication" (on by default), "Vault attestation"; no descriptions.
  - Only "Export" / "Markdown, all cards" was understood.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23`
  > "No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Click "Settings".
  2. Observe three toggles with no explanatory text.
- **Fix:** Add one plain-language line under each toggle saying what it changes for the user's notes.

### d332fafd695d — Settings reuses a signup option name as a toggle with no link between the two
- **Severity:** P2
- **So what:** The power user could not tell whether the toggle overrides his "cannot be changed" signup choice, undermining trust in both screens.
- **Framework tags:** A4, A1
- **Flow:** shape_2b
- **Locator:** nav: Settings
- **Personas hit:** power-user
- **Observed:**
  - Signup option "Federated graph"; Settings toggle "Federated graph replication", checked by default.
  - Power-user asked whether they were the same thing; no copy answers it.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-power-user/session.log:8` · `persona-power-user/session.log:13`
  > "'Federated graph replication' is on by default. I picked that at signup — is this the same thing?"
- **Repro:**
  1. Pick "Federated graph" at signup.
  2. Open "Settings"; observe "Federated graph replication" with no reference to the signup choice.
- **Fix:** Show the chosen workspace type on Settings and state how the replication toggle relates to it.

### c6772f8c77d1 — No keyboard shortcuts exist for capture or search
- **Severity:** P2
- **So what:** The power user came for keyboard-driven capture; Ctrl+K, Ctrl+N and / all did nothing.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - Tried Ctrl+K, Ctrl+N and "/" at 01:30; none produced a response.
  - Pre-session expectation: "fast capture, good search, keyboard-driven".
- **Evidence:** `persona-power-user/session.log:3` · `persona-power-user/session.log:12`
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Open the dashboard.
  2. Press Ctrl+K, Ctrl+N, then "/".
  3. Observe no response.
- **Fix:** Bind "/" to focus search and Ctrl+N to open a new note, and list them in a shortcut hint.

---

## What worked
- Live word count and preview in the editor — novice's first positive moment at 02:41 (`persona-novice/session.log:16`).
- Export "Markdown, all cards" understood by both personas (`persona-novice/session.log:23` · `persona-power-user/session.log:13`).

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself — `persona-novice/screenshots/04-note-saved-toast.png` shows an empty editor, no toast; the toast rests on log lines only.
- Typed note content — `persona-novice/screenshots/03-new-note.png` shows "0 words" and empty fields, not the "Dentist" note.
- Search "No results for …" message — `persona-power-user/screenshots/03-search-empty.png` shows the bare dashboard, no query or result text.
- Power-user memories screenshot — his raw finding cites `02-dashboard.png`, which shows the dashboard, not Memories.
- Novice timeline reports `first_value_reached: true` at 161 s — contradicted by the log; the preview is not a saved note.

## For other lenses
- Save reports success while nothing persists — bugs (check the save request and response).
- Jargon density on signup and Settings ("Sovereign vault", "Vault attestation") — content.
- Irreversible pre-product choice as a signup step; empty first-run state — onboarding.
- "Remembers everything" promise versus an empty start — content / onboarding.
- Accessibility (radio buttons and checkboxes rendered far from their labels) — no lens covers it.

## Coverage gaps
- Export never clicked; whether it produces a file is unknown.
- Mobile not tested; both personas on desktop-1440x900.
- Note edit, delete and the "Cards" nav item never exercised.
- Neither persona reached a saved note, so retrieval and organisation were never tested.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast, 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
