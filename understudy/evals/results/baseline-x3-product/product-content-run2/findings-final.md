# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery (Q4), Nielsen A2/A4/A9, reading level, jargon density, error and empty-state copy
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user; both desktop 1440×900)
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope exclusion applied: the login wall at `/app/login.html` is never scored

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | Empty "Your cards", note lost twice behind "Saved ✓", Memories page stating things that are not true | Fail | Quit at 06:30 with zero notes; Q3 "No. Nothing, until saving works." |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Save lost, search finds nothing, no shortcuts, Memories not theirs | Fail | Quit at 03:00; Q3 "No. Nothing." |

- Persona Q4 answers: novice "No", power-user "No". My reading agrees with both; no disagreement to note.
- The promise failure is the root of the two P0s: copy claims memory ("Saved ✓", "What Nimbus remembers about you") the product cannot back.

## Reading level and jargon
- Sentence structure is simple throughout (≤ 10 words per line); the difficulty is vocabulary, not syntax.
- Jargon terms met before first value: "Federated graph", "Sovereign vault", "Hybrid mesh", "block", "cards" — 5 terms in the first 2 screens.
- Jargon terms in Settings: "Enable webhook sync", "Federated graph replication", "Vault attestation" — 3 of 4 controls.
- Clear copy that worked: "0 words" / "Preview below" (`persona-novice/screenshots/03-new-note.png`), "Export — Markdown, all cards" (`persona-novice/screenshots/07-settings.png`, `session.log:23`).

---

## Findings

### b80be1050d42 — "Saved ✓" confirms a save the server rejected, and no error copy ever appears
- **Severity:** P0
- **So what:** Both personas were told their note was kept when it was not; the novice concluded "It is lying to me" and stopped trusting every other message.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Green "Saved ✓" toast shown after Save while `POST /api/notes` returned 500 (novice twice, power-user once).
  - Dashboard then shows "Nothing here yet."; search returns "No results for 'Dentist'" / "No results for 'Roadmap'".
  - No error, retry or explanation copy shown at any point; the only wording the user sees is a success message.
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:20` · `persona-novice/network-full.txt` (POST /api/notes → 500 at 03:05 and 03:50) · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "Nothing yet — it accepts a note and then loses it."
- **Repro:**
  1. Sign up, choose any workspace type, open "New block".
  2. Enter a title and body, click "Save".
  3. Observe "Saved ✓" toast; return to dashboard and search the title.
- **Fix:** Gate the "Saved ✓" toast on a 2xx response, and on failure show an error that names what happened and offers retry.

### 5c5e3aa8adf2-a — "What Nimbus remembers about you" lists three facts about the user that are invented
- **Severity:** P0
- **So what:** The novice read confident statements about herself that were false, then doubted every other claim the product made — "is it making up the 'Saved' too?"
- **Framework tags:** A2, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Page shows "You prefer to schedule meetings on Tuesday afternoons." "Your team uses Jira and Slack." "You are working on a product launch in Q4."
  - Caption reads "Memories are built from your notes and connected accounts." — the persona had zero saved notes and no connected accounts.
  - No label marks the content as sample, demo or placeholder.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a fresh workspace with no notes saved and no accounts connected.
  2. Click "Memories" in the top nav.
- **Fix:** On /app/memories.html, never show placeholder memories as the user's own; show an empty state that says where memories come from and how to create the first one.

### 5c5e3aa8adf2-b — "What Nimbus remembers about you" lists three facts about the user that are invented
- **Severity:** P1
- **So what:** The power-user wrote the page off as "a demo panel" and declared it untrustworthy — the headline feature of the pitch was dismissed in 30 seconds.
- **Framework tags:** A2, B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three statements shown to a workspace with no saved notes and no connected accounts.
  - Persona assumed demo content rather than a lie, but explicitly refused to trust it.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` · `persona-novice/screenshots/06-memories.png` (same page, same copy)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > "It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Create a fresh workspace, save nothing.
  2. Click "Memories".
- **Fix:** Same surface: replace the placeholder statements with an honest empty state, or label them "Example" so nobody reads them as their own.

### 87014dd5487f — The product contradicts its pitch: "remembers everything" opens on "Nothing here yet." and forgets the first note
- **Severity:** P1
- **So what:** Both personas arrived for memory and got amnesia; both answered Q4 "No" and Q3 "Nothing", so the pitch is actively costing the product its first session.
- **Framework tags:** A2, B-G1, C-SOWHAT, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Pre-session promise for both: "remembers everything so you never start from zero".
  - First screen after signup: "Your cards" — "Nothing here yet." with no copy explaining how Nimbus will remember anything.
  - Nothing in the app names a source of memory (import, connect, sync) until the false caption on Memories.
- **Evidence:** `persona-novice/session.log:2` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/persona-debrief.md` · `persona-power-user/session.log:2` · `persona-power-user/screenshots/02-dashboard.png` · `persona-power-user/persona-debrief.md`
  > "I arrived with "remembers everything so you never start from zero". No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine."
  > ""Remembers everything." No. It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Read the marketing line "Nimbus remembers everything so you never start from zero".
  2. Sign up and land on /app/dashboard.html.
  3. Compare the first screen against the line.
- **Fix:** Either make the first dashboard state say how "remembering" starts (connect, import, or write) and deliver it, or change the marketing line to match what a new workspace does.

### c2721593a4a1-a — Signup forces an irreversible choice between "Federated graph", "Sovereign vault" and "Hybrid mesh" with no definitions
- **Severity:** P1
- **So what:** The novice spent 48 seconds guessing at a decision she was told she "cannot" undo, before seeing a single screen of the product.
- **Framework tags:** A2, A3, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Heading "Before we begin, choose your workspace type"; three radio labels, no description under any of them.
  - Helper text: "This cannot be changed later."
  - Persona picked "Hybrid mesh" "because it sounds like it includes the other two".
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall and land on /app/signup.html.
  2. Read the three options and the helper text.
- **Fix:** Add one plain-language line under each option saying who it is for and what it changes, or default the choice and move it to Settings.

### c2721593a4a1-b — Signup forces an irreversible choice between "Federated graph", "Sovereign vault" and "Hybrid mesh" with no definitions
- **Severity:** P3
- **So what:** The power-user shrugged ("I've seen worse") but later could not tell whether "Federated graph replication" in Settings was the same thing.
- **Framework tags:** A2, A4
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Same screen, same three undefined labels; persona picked "Federated graph" without comment in under 30 seconds.
  - At 02:00 asked whether the Settings toggle "Federated graph replication" was the signup choice — "Same words, no link."
- **Evidence:** `persona-power-user/session.log:8` · `persona-power-user/session.log:13` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/screenshots/01-signup-workspace-type.png` (same screen)
  > "Workspace type: Federated graph / Sovereign vault / Hybrid mesh, cannot be changed. Fine — I've seen worse."
- **Repro:**
  1. On /app/signup.html pick "Federated graph".
  2. Open Settings and read "Federated graph replication".
- **Fix:** Define each option in one line on signup, and reuse the exact same term where it reappears in Settings.

### 07d8d3a2fc56 — One object is called "cards", "block" and "notes" on the same screen
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, so the path to writing her first note was a guess.
- **Framework tags:** A4, A6
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; section heading "Your cards"; search placeholder "Search your notes"; page title "New block"; export label "Markdown, all cards".
  - Three words for one object on a single screen; a fourth ("Memories") is introduced with no relationship stated.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing? Clicked "New block"."
- **Repro:**
  1. Land on /app/dashboard.html and read the nav, heading and search placeholder.
  2. Click "New block" and read the page title.
- **Fix:** Pick one noun for the object and use it in the nav, the section heading, the search placeholder, the create page and the export label.

### 31ad74b3ec06 — Settings toggles use engineering vocabulary with no explanation: "Enable webhook sync", "Federated graph replication", "Vault attestation"
- **Severity:** P2
- **So what:** Three of four controls on the page were opaque to the novice and ambiguous to the power-user; a switch nobody can explain is a switch nobody dares touch.
- **Framework tags:** A2, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Labels "Enable webhook sync", "Federated graph replication" (checked by default), "Vault attestation"; no helper text under any.
  - Novice: "No idea." Power-user could not tell whether "Federated graph replication" was the signup choice.
  - The one control with a plain description — "Export" "Markdown, all cards" — both personas understood immediately.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24` · `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13`
  > "Settings. "Enable webhook sync", "Federated graph replication", "Vault attestation". No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Click "Settings" in the top nav.
  2. Read the three toggle labels.
- **Fix:** Add a one-line plain-language description under each toggle saying what turning it on does to the user's notes.

### d3573a5fe206 — Empty state "Nothing here yet." offers no next step
- **Severity:** P2
- **So what:** The novice's first screen gave her no instruction, so she spent 45 seconds searching an empty workspace before guessing at "New block".
- **Framework tags:** A6, A10, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" section body reads only "Nothing here yet." — no link, button or instruction.
  - Persona typed "meeting" into search at 01:20 and got "No results for 'meeting'" before finding the create action at 01:40.
  - Power-user found the search box and moved on; no complaint recorded, so this is scored for the novice only.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14`
  > "Dashboard. "Your cards" — "Nothing here yet." Screenshot 02-dashboard-empty.png. Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Sign up and land on /app/dashboard.html with no notes.
  2. Read the "Your cards" section.
- **Fix:** Replace "Nothing here yet." with a sentence that says what a card is and a button that creates the first one.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "No results for '…'" copy may not distinguish "nothing saved" from "no match" — the no-results state was never screenshotted (`persona-power-user/screenshots/03-search-empty.png` shows an empty search box, not the message); log-only.
- "Saved ✓" toast wording and placement — `persona-novice/screenshots/04-note-saved-toast.png` shows the empty form, not the toast; the wording is taken from `session.log:17` only.

## For other lenses
- `POST /api/notes` → 500 on every save; `renderGraphOverlay is not defined` on every dashboard load — bugs.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, / all inert) — ux.
- Novice TTFV 2:41 on a preview, not a saved note; power-user never reached first value — onboarding.
- Irreversible signup choice with no undo — ux (A3).

## Coverage gaps
- Marketing site itself never captured; the promise is taken from the pre-session line only.
- "Cards" nav item never clicked by either persona; unknown whether it is the dashboard or a separate list.
- Export never clicked; whether it exports anything for an empty workspace is unknown.
- Desktop 1440×900 only; no mobile.
- Both personas quit before 07:00; no copy past the first session was seen.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index: `persona-novice/screenshots/00-start.png` … `07-settings.png`; `persona-power-user/screenshots/00-start.png`, `02-dashboard.png`, `03-search-empty.png`, `07-settings.png`
