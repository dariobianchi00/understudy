# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layers A (Nielsen 10), B (HAX — applies: "Memories" is a user-facing inference surface), C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on invented personas
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Network/console lines cited only as supporting evidence for a usability finding; the errors themselves belong to `bugs`

---

## Findings

### b329b370329d — Save confirms "Saved ✓" but the note never appears in the cards list or search
- **Severity:** P0
- **So what:** Both personas lost every note they wrote, were told it was safe, and abandoned the core job.
- **Framework tags:** A1, A9, C-ABANDON, C-SOWHAT, C-TTFV
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice saved "Dentist" twice; both times "Saved ✓" toast, then "Nothing here yet." and search "No results for 'Dentist'."
  - Power user saved "Roadmap"; "Saved ✓", list empty, search for title returned nothing.
  - Both gave up on the objective (`timeline.json` `gave_up: true`); both debriefs answer Q1 "nothing".
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-novice/network-full.txt:5` (POST /api/notes → 500 at 03:05, while toast said saved)
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." (novice)
  > "Save doesn't save and search doesn't search. Nothing else matters until those work." (power-user)
- **Repro:**
  1. Create a workspace; open "New block".
  2. Enter a title and body; click Save.
  3. Observe "Saved ✓", then the dashboard shows "Nothing here yet."; search the title → no results.
- **Fix:** Show "Saved ✓" only after the server confirms the write; on failure keep the editor open with the text and a "Couldn't save — retry" message.

### 30f0eceb9f04 — Memories page presents invented facts as the novice's own, and she stops trusting "Saved" too
- **Severity:** P0
- **So what:** Confident claims about her that are false made her doubt every other message the product shows — trust broken at minute 5.
- **Framework tags:** B-G1, B-G2, B-G11, A2, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — she had zero saved notes, no connected accounts.
  - She generalised the distrust to save confirmation, then stopped at 06:30.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
  > "the "memories" it does have aren't mine."
- **Repro:**
  1. Create a fresh workspace with no notes and no connected accounts.
  2. Click "Memories" in the top nav.
  3. Observe three specific personal claims with no source.
- **Fix:** Show an empty state on /app/memories.html until real memories exist, and link each memory to the note it came from.
- Torn P0/P1: rubric's P0 example is "confident nonsense about the persona's own data"; she also extended the distrust to "Saved", so P0.

### 2e8b88bb637c — Memories page shows facts the power user never gave, and he writes it off as a demo panel
- **Severity:** P2
- **So what:** He dismissed the product's headline "remembers everything" feature as fake; churn risk once save works.
- **Framework tags:** B-G1, B-G11
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Saw "Tuesday meetings, Jira, Q4 launch"; said "Not me."
  - Assumed demo content and moved on without changing course.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4 · `persona-novice/screenshots/06-memories.png` (same page content)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > "It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Create a fresh workspace.
  2. Open "Memories".
  3. Observe unsourced claims unrelated to the user.
- **Fix:** If sample memories are intended, label them "Example" on the page; otherwise replace with an empty state until real data exists.

### 78909f81f063 — Signup forces an irreversible workspace-type choice in unexplained jargon before any product is shown
- **Severity:** P2
- **So what:** The novice guessed an undoable setting she didn't understand within 50 seconds of arriving; a less patient user leaves here.
- **Framework tags:** A2, A3, A5, A10, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Options "Federated graph", "Sovereign vault", "Hybrid mesh" with no description; note "This cannot be changed later."
  - Novice paused 28 s (00:20–00:48), then picked "Hybrid mesh" "because it sounds like it includes the other two".
  - Power user accepted it ("Fine — I've seen worse") — non-issue for him.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Create an account.
  2. Land on "Before we begin, choose your workspace type".
  3. Observe three unexplained options and "This cannot be changed later."
- **Fix:** Default the workspace type and move it to Settings, or add one plain-language line per option and make it changeable.

### 73f121dc2431 — Empty dashboard says "Nothing here yet." with no prompt to write a first note
- **Severity:** P2
- **So what:** The novice expected her content, searched an empty app, and hunted twice before finding how to start.
- **Framework tags:** A6, A10, C-TTFV, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel shows only "Nothing here yet." — no button, no hint.
  - Novice searched "meeting" (no results), then scanned the nav before clicking "New block" at 01:40.
  - `timeline.json` `times_had_to_hunt: 2`.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14`
  > "Dashboard. "Your cards" — "Nothing here yet." ... Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a new workspace.
  2. Observe the dashboard empty state.
- **Fix:** Replace "Nothing here yet." with a "Write your first note" button that opens the editor.

### 99c0cc36c19f — One object is called "cards", "block" and "notes" across nav, editor and search
- **Severity:** P2
- **So what:** The novice could not tell whether the thing she was creating was the thing the list would show.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** top nav
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; list heading "Your cards"; search placeholder "Search your notes"; export "Markdown, all cards".
  - Novice asked aloud whether cards and blocks are the same before clicking "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14`
  > "Cards, blocks, notes — are these the same thing?" (`persona-novice/findings-raw.json`, 01:40)
- **Repro:**
  1. Open the dashboard.
  2. Compare the nav labels, the "Your cards" heading and the "Search your notes" placeholder.
- **Fix:** Pick one noun ("note") and use it in the nav, editor heading, list heading, search placeholder and export label.

### c4c5e5d2f66b — Settings toggles are unexplained jargon, and "Federated graph replication" is not tied to the signup choice
- **Severity:** P2
- **So what:** Neither persona could tell what the settings control; the power user couldn't connect one to his irreversible signup pick.
- **Framework tags:** A2, A4, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Toggles "Enable webhook sync", "Federated graph replication" (on by default), "Vault attestation" — no descriptions.
  - Novice: "No idea"; power user asked if "Federated graph replication" was what he picked at signup.
  - Both found the "Export — Markdown, all cards" control clear.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-power-user/session.log:13`
  > ""Federated graph replication" is on by default. I picked that at signup — is this the same thing?" (power-user)
- **Repro:**
  1. Open Settings.
  2. Observe three toggles with no explanation.
- **Fix:** Add one plain-language line under each toggle and show the chosen workspace type by name on /app/settings.html.

### 6f04a230f94a — No keyboard shortcuts for capture or search
- **Severity:** P2
- **So what:** The keyboard-driven team evaluator found none of the expected accelerators; a mark against switching his team.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** keyboard: Ctrl+K, Ctrl+N, /
- **Personas hit:** power-user
- **Observed:**
  - Tried Ctrl+K, Ctrl+N and "/" — nothing happened.
  - No shortcut hints visible on the dashboard.
- **Evidence:** `persona-power-user/session.log:12` · `persona-power-user/screenshots/02-dashboard.png`
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Open the dashboard.
  2. Press Ctrl+K, Ctrl+N or "/".
  3. Observe no response.
- **Fix:** Bind "/" or Ctrl+K to focus search and Ctrl+N to open a new note; list them in a "?" shortcut sheet.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast styling and timing — `persona-novice/screenshots/04-note-saved-toast.png` shows an empty editor with no toast; toast is attested by `session.log:17` only.
- Radio buttons and checkboxes render centred, detached from their labels on signup and settings — visible in screenshots, but no persona reacted to it.
- Top nav ("Cards", "Memories", …) shows on the workspace-setup screen before a workspace exists — visible, no persona reaction.
- Live word count and preview in the editor — novice's only positive moment (`session.log:16`), but `03-new-note.png` shows "0 words" with an empty form; not captured mid-typing.

## For other lenses
- POST /api/notes → 500 on every save while UI shows "Saved ✓" — bugs.
- `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load — bugs.
- Marketing promise "remembers everything so you never start from zero" vs empty start — onboarding / content.
- Jargon density: "Federated graph", "Sovereign vault", "Hybrid mesh", "Vault attestation" — content.
- Accessibility (detached labels on radios/checkboxes) — no lens covers WCAG.

## Coverage gaps
- Export was never clicked; whether it works is unknown.
- "Cards" nav item never clicked separately from the dashboard.
- No mobile device tested; desktop 1440×900 only.
- No persona connected an account, so the "connected accounts" memory source is unverified.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — novice 00–07 (00-start, 00-wall-cleared, 01–07); power-user 00, 02, 03, 07
