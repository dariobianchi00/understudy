# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) · Layer B (HAX, applies to the AI "Memories" surface) · Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B applies only to `/app/memories.html`, the one user-facing AI surface observed

---

## Findings

### 13b62768461f — Save shows a success toast but the note never reaches the cards list or search
- **Severity:** P0
- **So what:** Both personas wrote a note, were told "Saved ✓", then could not find it. Both gave up on the core job and would pay nothing.
- **Framework tags:** A1, A9, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice saved "Dentist" twice and saw "Saved ✓" both times. The dashboard still read "Nothing here yet." and a search for "Dentist" returned "No results for 'Dentist'."
  - Power user saved "Roadmap" and saw "Saved ✓". The list stayed empty and a search for "Roadmap" returned no results.
  - Both timelines record `gave_up: true` on the objective. Both debriefs answer Q3 with "No".
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/timeline.json` objectives[0].gave_up · network `POST /api/notes → 500` (cited only as the cause)
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "Nothing yet — it accepts a note and then loses it." (power-user debrief Q1)
- **Repro:**
  1. Create a workspace, then open "New block".
  2. Enter a title and body, then click Save.
  3. See "Saved ✓". Return to the dashboard: "Nothing here yet."
  4. Search for the title: no results.
- **Fix:** Show "Saved ✓" only after the server confirms the save. On failure, keep the editor open with the text and say "Not saved — retry".

### 7a140e7d2290 — Memories page states invented facts as the novice's own, so she stops trusting Save too
- **Severity:** P0
- **So what:** Invented "memories" made the novice doubt every other message, including the Save confirmation. Trust broke beyond the one screen.
- **Framework tags:** B-G2, B-G11, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - The page is headed "What Nimbus remembers about you" and lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack." and "You are working on a product launch in Q4."
  - The footer says "Memories are built from your notes and connected accounts." The novice had written only one note, about a dentist, and connected no accounts.
  - The novice chose to stop at 06:30. Her debrief says the memories "aren't mine".
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a fresh workspace and connect no accounts.
  2. Open Memories.
  3. Three specific personal claims appear that no user input supports.
- **Fix:** Show memories only when they come from the user's own notes, and link each one to its source. On a new account, show an empty state explaining how memories form.
- Torn between P0 and P1: P0 because the novice tied the false memories to her distrust of Save, which is the core flow.

### c96c9c729d99 — Memories page states invented facts as the power user's own, so he writes it off as a demo
- **Severity:** P1
- **So what:** The headline "remembers everything" feature was dismissed as fake. The evaluator will not rely on it for his team.
- **Framework tags:** B-G2, B-G11, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - He saw the same three claims: Tuesday meetings, Jira and Slack, Q4 launch.
  - He read them as a demo panel and said outright that he would not trust it.
  - His debrief Q4: it "claims things I didn't".
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4 · `persona-novice/screenshots/06-memories.png` (same page, same content)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a fresh workspace.
  2. Open Memories.
  3. Unsourced personal claims appear.
- **Fix:** If this is sample content, label it "Example" on the page. Otherwise, show only memories derived from real notes, each with a source link.

### e4af59929810 — Signup forces an irreversible workspace-type choice in unexplained terms before any product is shown
- **Severity:** P2
- **So what:** The novice spent 43s guessing at a permanent decision before seeing anything. A less patient user may leave here.
- **Framework tags:** A2, A3, A5, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - The screen titled "Before we begin, choose your workspace type" offers "Federated graph", "Sovereign vault" and "Hybrid mesh", with no description of any of them.
  - The page warns "This cannot be changed later." and offers no default and no skip.
  - The novice picked "Hybrid mesh" at 00:48 "because it sounds like it includes the other two".
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall and land on `/app/signup.html`.
  2. You are asked for a workspace type with three undefined options, marked "This cannot be changed later."
- **Fix:** Preselect a default and add a one-line description under each option. Either allow changing it in Settings or defer the choice until after the first note.

### f2dba2e590d1 — Empty dashboard says only Nothing here yet with no pointer to writing a first note
- **Severity:** P2
- **So what:** The novice expected her stuff and got a blank card. She searched an empty account before finding "New block" 45s later.
- **Framework tags:** A6, A10, C-TTFV
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" shows only "Nothing here yet.", with no button or hint.
  - The novice searched "meeting" in an empty account at 01:20, then reached "New block" through the top nav at 01:40.
  - Her timeline records 2 hunts (`times_had_to_hunt: 2`).
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/timeline.json` shape_2.times_had_to_hunt
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a new workspace.
  2. The dashboard's empty state has no call to action.
- **Fix:** Add a "Write your first note" button and one line saying what to do, inside the "Your cards" empty state.

### f52424794183 — The same object is called card, block and note across nav, editor and search
- **Severity:** P2
- **So what:** The novice stopped to ask whether these were different things before she could create anything.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** global nav
- **Personas hit:** novice
- **Observed:**
  - The nav reads "Cards" and "New block". The search placeholder reads "Search your notes". The list heading reads "Your cards".
  - The editor heading is "New block". Export reads "Markdown, all cards".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Open the dashboard and read the nav, the search placeholder and the list heading.
  2. Open "New block".
- **Fix:** Pick one noun, "note", and use it in the nav, editor heading, list heading, search placeholder and Export label.

### fde917274374 — Settings pre-checks Federated graph replication with no link to the signup workspace choice
- **Severity:** P2
- **So what:** Neither persona could tell what the switches do or whether they relate to their signup choice. Settings felt unsafe to touch.
- **Framework tags:** A2, A4, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - The toggles read "Enable webhook sync", "Federated graph replication" (checked) and "Vault attestation", with no descriptions.
  - The novice picked "Hybrid mesh", yet "Federated graph replication" is checked. The power user picked "Federated graph" and asked whether it is the same thing.
  - Both personas called "Export — Markdown, all cards" the one clear control.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-power-user/session.log:13`
  > "'Federated graph replication' is on by default. I picked that at signup — is this the same thing?"
- **Repro:**
  1. Sign up with any workspace type.
  2. Open Settings. "Federated graph replication" is checked and has no explanation.
- **Fix:** Add a one-line description under each toggle. Show the chosen workspace type as a read-only row, and state how it relates to replication.

### 728949c5900d — No keyboard shortcuts for creating or searching notes
- **Severity:** P2
- **So what:** The power user came for keyboard-driven capture and found none. One of his three stated expectations went unmet.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - He tried Ctrl+K, Ctrl+N and / and got no response.
  - His pre-session expectation was "fast capture, good search, keyboard-driven".
- **Evidence:** `persona-power-user/session.log:3` · `persona-power-user/session.log:12` · `persona-power-user/screenshots/02-dashboard.png`
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Open the dashboard.
  2. Press Ctrl+K, Ctrl+N or /. Nothing happens.
- **Fix:** Bind / or Ctrl+K to focus search and Ctrl+N to open a new note. List the shortcuts in a "?" overlay.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast is not visible in `persona-novice/screenshots/04-note-saved-toast.png`, which shows the blank editor. The toast claim rests on the session.log lines only.
- The "No results for '…'" text is not visible in `persona-power-user/screenshots/03-search-empty.png`, which shows an empty search box. The claim rests on session.log only.
- Radio buttons and checkboxes sit centred, away from their labels (signup, settings). This is visible, but no persona reacted to it.
- Markdown export was never clicked, so whether it works is unknown.
- The live preview did not render visibly in `03-new-note.png` (0 words, empty). The novice's 02:41 "first value" rests on the log only.

## For other lenses
- `POST /api/notes → 500` on every save, and `Uncaught ReferenceError: renderGraphOverlay is not defined` on the dashboard — bugs
- Jargon density: "Federated graph", "Sovereign vault", "Hybrid mesh", "Vault attestation", "webhook sync" — content
- An irreversible setup step placed before first value, and the funnel stopping at the objective for 2/2 personas — onboarding
- The promise "remembers everything so you never start from zero" against an empty start — content / onboarding

## Coverage gaps
- Mobile was not tested; both personas used desktop 1440x900
- The Export download was not exercised
- Editing and deleting a note was never reached, because no note ever saved
- "Connected accounts" (cited by Memories) was never found or opened
- WCAG / accessibility: no lens covers it yet

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01–07 · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
