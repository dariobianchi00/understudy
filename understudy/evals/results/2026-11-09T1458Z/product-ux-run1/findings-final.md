# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10), Layer B (HAX — applies: "Memories" is a user-facing AI surface), Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Screenshot caveat: `04-note-saved-toast.png` shows the blank "New block" form, not the toast; the toast rests on `session.log` lines

---

## Findings

### 0926f034f60c — Save shows "Saved ✓" but the note never appears in "Your cards" or search
- **Severity:** P0
- **So what:** Both personas failed the core objective, called the product a liar, and said they would not return or pay.
- **Framework tags:** A1, A9, C-ABANDON, C-TTFV, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice saved "Dentist" twice; each time "Saved ✓", then "Nothing here yet." and search returned "No results for 'Dentist'."
  - Power user saved "Roadmap"; "Saved ✓", list empty, search for "Roadmap" found nothing.
  - Both timelines record `gave_up: true` on "A new user can write a note and find it again".
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-novice/timeline.json` objectives[0].gave_up · `persona-power-user/timeline.json` objectives[0].gave_up
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." (novice)
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." (power-user)
  > "No. Nothing, until saving works." (novice debrief Q3)
- **Repro:**
  1. Create a workspace at `/app/signup.html`.
  2. Click "New block", enter a title and body, click "Save".
  3. Observe "Saved ✓", then "Nothing here yet." on the dashboard; search the title — "No results".
- **Fix:** Only show "Saved ✓" after the card is persisted, and land the user on the new card in "Your cards" with it searchable immediately.

### dae80cf0beb3 — Memories page states invented facts about a brand-new user, and the novice stops trusting every confirmation
- **Severity:** P0
- **So what:** Confident claims about her own life that are false made the novice doubt the "Saved" toast too — trust broke product-wide.
- **Framework tags:** B-G2, B-G11, B-G9, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** Memories
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists Tuesday meetings, "Jira and Slack", "a product launch in Q4".
  - Footer says "Memories are built from your notes and connected accounts." — she had no saved notes and connected nothing.
  - No control to remove or correct a memory is visible.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
  > "the "memories" it does have aren't mine." (debrief Q4)
- **Repro:**
  1. Create a fresh workspace; connect nothing.
  2. Click "Memories" in the top nav.
  3. Observe three specific claims about the user with no source.
- **Fix:** Show an honest empty state on Memories until real notes exist, and attach a source link plus a "This is wrong" remove control to each memory.

### 58e5a14c9840 — Memories page states invented facts the power user dismisses as a demo but cites against the promise
- **Severity:** P1
- **So what:** The power user wrote the panel off as fake and named it in his debrief as proof the promise is false.
- **Framework tags:** B-G2, B-G11, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** Memories#power-user
- **Personas hit:** power-user
- **Observed:**
  - Read the same three memories; assumed "a demo panel".
  - Explicitly declined to trust the surface, then ended the session 30 s later.
- **Evidence:** `persona-novice/screenshots/06-memories.png` (same surface; power user took no screenshot of it) · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > "It remembers nothing I gave it and claims things I didn't." (debrief Q4)
- **Repro:**
  1. Create a fresh workspace.
  2. Open "Memories".
  3. Observe unsourced claims unrelated to the user.
- **Fix:** Same as the novice variant: empty state until real data exists; label any sample content explicitly as "Example".

### 1bf17f8f98a9 — Signup forces an irreversible workspace-type choice between three undefined terms before the user sees the product
- **Severity:** P2
- **So what:** The novice guessed blind on a permanent decision 20 seconds in; a less stubborn user leaves here.
- **Framework tags:** A2, A3, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Federated graph", "Sovereign vault", "Hybrid mesh" with no descriptions; "This cannot be changed later."
  - Novice paused 28 s (00:20 → 00:48), then picked "Hybrid mesh" by guesswork.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Open `/app/signup.html`.
  2. Observe three unexplained options and "This cannot be changed later."
- **Fix:** Default the workspace type silently, or add one plain-language line per option and make it changeable in Settings.

### 007c5c817cf0 — Empty dashboard says only "Nothing here yet." with no next step, contradicting the "remembers everything" promise
- **Severity:** P2
- **So what:** The novice arrived expecting her stuff, got a blank page with no prompt, and spent 45 s searching an empty box.
- **Framework tags:** A1, A10, C-TTFV, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" — "Nothing here yet." with no button or hint.
  - Novice searched "meeting" (01:20) before finding "New block" at 01:40.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:1` · `persona-novice/session.log:12` · `persona-novice/session.log:13`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a fresh workspace.
  2. Land on the dashboard; observe "Nothing here yet." and no call to action.
- **Fix:** Put a "Write your first note" button and one line on what Nimbus will remember inside the empty "Your cards" panel.

### 2a0639bf7484 — One object has three names: "Cards", "New block" and "Search your notes"
- **Severity:** P2
- **So what:** The novice could not tell whether creating a "block" would make a "card", adding hesitation to the first write.
- **Framework tags:** A4, A2
- **Flow:** shape_2
- **Locator:** nav
- **Personas hit:** novice
- **Observed:**
  - Nav reads "Cards", "New block"; search placeholder reads "Search your notes"; dashboard heading "Your cards".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14`
  > "Cards and blocks — same thing?"
- **Repro:**
  1. Open the dashboard.
  2. Compare the nav labels, the "Your cards" heading and the search placeholder.
- **Fix:** Pick one noun ("note") and use it in the nav, the create button, the list heading and the search placeholder.

### 0b263ad05a1c — Settings pre-checks "Federated graph replication" with no link to the signup choice of the same name
- **Severity:** P2
- **So what:** Neither persona could tell what the toggles do or whether they undo the "cannot be changed" signup choice.
- **Framework tags:** A4, A2, A6
- **Flow:** shape_2b
- **Locator:** Settings
- **Personas hit:** power-user, novice
- **Observed:**
  - Checkboxes "Enable webhook sync", "Federated graph replication" (checked), "Vault attestation" — no descriptions.
  - Power user had picked "Federated graph" at signup; novice picked "Hybrid mesh" yet the same box is checked for her.
  - "Export — Markdown, all cards" was the one control both understood.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-novice/screenshots/07-settings.png` · `persona-power-user/session.log:13` · `persona-novice/session.log:23`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link." (power-user)
  > "No idea. There's an Export button — "Markdown, all cards". At least that's clear." (novice)
- **Repro:**
  1. Create a workspace choosing any type.
  2. Open "Settings"; observe "Federated graph replication" checked with no explanation.
- **Fix:** Add a one-line description under each toggle and show the signup workspace type as read-only text, separate from the replication toggle.

### 1d28d5db2e97 — No keyboard shortcuts for capture or search; Ctrl+K, Ctrl+N and / do nothing
- **Severity:** P2
- **So what:** The power user came for "keyboard-driven" capture; finding none erodes the case for switching his team.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** keyboard
- **Personas hit:** power-user
- **Observed:**
  - Tried Ctrl+K, Ctrl+N and / on the dashboard; nothing happened.
  - He continued to Settings and Memories; he quit over saving, not shortcuts.
- **Evidence:** `persona-power-user/screenshots/02-dashboard.png` · `persona-power-user/session.log:3` · `persona-power-user/session.log:12`
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Open the dashboard.
  2. Press Ctrl+K, Ctrl+N, then /.
  3. Observe no response.
- **Fix:** Bind / to focus search and Ctrl+N to "New block", and list shortcuts in a "?" overlay.

---

## What worked
- Live word count and preview on "New block" — novice: "that's the first thing it's done for me" (`persona-novice/session.log:16`).
- "Export — Markdown, all cards" was understood instantly by both personas.

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast placement and duration — `04-note-saved-toast.png` captured the blank form, not the toast.
- Whether the novice's typed text reached the preview — `03-new-note.png` shows the form empty (0 words).
- Power user's "No results for 'Roadmap'" message — `03-search-empty.png` shows an empty dashboard, search term not visible; the claim rests on the log only.

## For other lenses
- Note silently not persisted after save — bugs (check network/console for the save request).
- Jargon density: "Federated graph", "Sovereign vault", "Vault attestation", "webhook sync" — content.
- Irreversible pre-product choice as a funnel step — onboarding.
- Accessibility: radio buttons and checkboxes render visually detached from their labels in `01-signup-workspace-type.png` and `07-settings.png` — no lens covers WCAG yet.

## Coverage gaps
- Export was never clicked by either persona; whether it produces a file is unknown.
- No card was ever displayed, so card view, edit and delete were never reached.
- "Connected accounts" (referenced on Memories) was never found or opened.
- Desktop 1440×900 only; no mobile run.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast, 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
