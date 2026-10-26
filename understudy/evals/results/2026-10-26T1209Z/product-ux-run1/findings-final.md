# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10), Layer B (HAX, Memories surface only), Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Screenshot caveat: `04-note-saved-toast.png` and power-user `03-search-empty.png` do not show the toast or the query; those moments rest on `session.log`

---

## Findings

### a07ef75e9e8e — Save shows "Saved ✓" but the note never appears in the cards list or search
- **Severity:** P0
- **So what:** The product's one job fails silently; both personas gave up on the objective and said they would pay nothing.
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Clicking Save shows green "Saved ✓", returns to dashboard, which still reads "Nothing here yet."
  - Searching the exact title ("Dentist", "Roadmap") returns "No results"; novice repeated the whole save once more, same result
  - Each Save coincides with `POST /api/notes → 500`; the UI still reports success
- **Evidence:** `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-novice/network-full.txt` (`[POST] /api/notes → 500 internal error (03:05)`, `(03:50)`) · `persona-novice/persona-debrief.md` Q1, Q3 · `persona-power-user/persona-debrief.md` Q1
  > "Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "Save doesn't save and search doesn't search. Nothing else matters until those work."
- **Repro:**
  1. Create a workspace, click "New block".
  2. Enter a title and body, click Save; note the "Saved ✓" toast.
  3. Observe "Your cards" still reads "Nothing here yet."; search the title — "No results".
- **Fix:** Show "Saved ✓" only after the server confirms the write; on failure show an error with a Retry and keep the draft in the form.

### 9d81a8114afd — Memories page states invented facts about a brand-new user, and the novice stops trusting "Saved" too
- **Severity:** P0
- **So what:** Confident claims about her life she knows are false made the novice doubt every other message the product shows.
- **Framework tags:** B-G11, B-G2, B-G9, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — she had no saved notes and connected nothing
  - No source, edit or remove control on any memory; she quit within two minutes
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a new workspace; connect nothing, save nothing.
  2. Click "Memories" in the top nav.
  3. Observe three specific claims about the user with no source.
- **Fix:** Show an empty state on Memories until real data exists; for each memory, name its source note and offer Remove.

### ed838a3d9352 — Memories page states invented facts the power user dismisses as a demo and refuses to trust
- **Severity:** P1
- **So what:** The team evaluator wrote the feature off and cited it in his "No" verdict — the headline "remembers" promise reads as fake.
- **Framework tags:** B-G11, B-G2, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html#power-user
- **Personas hit:** power-user
- **Observed:**
  - Same three memories shown: Tuesday meetings, Jira and Slack, Q4 launch
  - He assumed "a demo panel" and moved on rather than abandoning on the spot
  - Debrief names it as a reason for "No": the product "claims things I didn't"
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4 · `persona-novice/screenshots/06-memories.png` (same surface, same content)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > ""Remembers everything." No. It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Create a new workspace and open "Memories".
  2. Observe claims unrelated to anything entered.
- **Fix:** If these are sample data, label them "Example" with a dismiss control; otherwise remove them until derived from the user's notes.

### c08875ca235d — Signup forces an irreversible workspace-type choice between three unexplained terms before the product is seen
- **Severity:** P2
- **So what:** A novice makes a permanent decision by guessing, before any value; a less patient user leaves at second 20.
- **Framework tags:** A5, A2, A3, A10, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Options "Federated graph", "Sovereign vault", "Hybrid mesh"; no descriptions, no default, no help link
  - Warning "This cannot be changed later." sits directly above "Create workspace"
  - Novice spent 43 seconds, picked "Hybrid mesh" because it "sounds like it includes the other two"; power-user unbothered
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall and land on /app/signup.html.
  2. Observe three unexplained radio options and "This cannot be changed later."
- **Fix:** Default the workspace type silently, or add a one-line plain-language description under each option and make it changeable later.

### 522634e8c888 — Empty dashboard says "Nothing here yet." with no next step toward a first note
- **Severity:** P2
- **So what:** The novice expected her "stuff" from the "never start from zero" promise and got a blank page with no direction.
- **Framework tags:** A6, A10, C-TTFV, C-SOWHAT
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel shows only "Nothing here yet." — no button, link or hint
  - Novice searched "meeting" on an empty workspace, then scanned the nav before finding "New block" at 01:40
  - 45 seconds from dashboard to the create form
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a new workspace.
  2. Observe the dashboard "Your cards" panel.
- **Fix:** Put a "Write your first note" button inside the empty "Your cards" panel, plus one line on what Nimbus will do with it.

### 81093bda2b09 — Same object is called card, block and note on adjacent UI
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, delaying her first note.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** nav: Cards / New block
- **Personas hit:** novice
- **Observed:**
  - Top nav: "Cards", "New block"; dashboard heading "Your cards"; search placeholder "Search your notes"
  - Create form titled "New block"; Settings export reads "Markdown, all cards"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` (t 01:40)
  > "Cards and blocks — same thing?"
- **Repro:**
  1. Open the dashboard; read the nav, heading and search placeholder.
  2. Click "New block"; compare the form title.
- **Fix:** Pick one noun ("note") and use it in the nav, the dashboard heading, the create form and the export label.

### 7ae40cccfd41 — No keyboard shortcuts for new note or search
- **Severity:** P2
- **So what:** The power user came for "keyboard-driven" capture; three standard shortcuts did nothing, eroding his switch case.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** global keyboard shortcuts
- **Personas hit:** power-user
- **Observed:**
  - Ctrl+K, Ctrl+N and "/" pressed on the dashboard; no response to any
  - No shortcut hints visible anywhere in the UI
- **Evidence:** `persona-power-user/session.log:3` · `persona-power-user/session.log:12` · `persona-power-user/screenshots/02-dashboard.png` · `persona-power-user/findings-raw.json` (t 01:30)
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Open the dashboard.
  2. Press Ctrl+K, Ctrl+N, then "/".
  3. Observe no search focus and no new-note form.
- **Fix:** Bind "/" to focus search and a new-note shortcut, and show the hints beside the search box and "New block".

### 0e8f7d419e42 — Settings toggles use unexplained infrastructure labels, one echoing the signup choice with no link
- **Severity:** P2
- **So what:** Neither persona could tell what the toggles do or whether they affect their irreversible signup choice.
- **Framework tags:** A2, A4, A6
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Toggles "Enable webhook sync", "Federated graph replication", "Vault attestation" have no descriptions
  - "Federated graph replication" is pre-checked for both personas, though novice chose "Hybrid mesh" and power-user "Federated graph"
  - Both identified "Export — Markdown, all cards" as the one clear control
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json` (t 02:00)
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
  > ""Enable webhook sync", "Federated graph replication", "Vault attestation". No idea."
- **Repro:**
  1. Create a workspace choosing "Hybrid mesh".
  2. Open Settings; observe "Federated graph replication" checked with no explanation.
- **Fix:** Add a one-line description under each toggle and state how "Federated graph replication" relates to the signup workspace type.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast visuals (placement, duration) — `04-note-saved-toast.png` shows the empty form, not the toast
- Power-user search query and "No results" message — `03-search-empty.png` shows only the empty dashboard
- Whether Export actually produces a usable file — never clicked by either persona

## For other lenses
- `POST /api/notes → 500` on every save; `renderGraphOverlay is not defined` on dashboard loads — bugs
- Workspace and settings vocabulary ("Sovereign vault", "Vault attestation") as copy — content
- "Remembers everything so you never start from zero" promise vs empty first screen — onboarding, content
- Accessibility not scored — no lens covers it yet

## Coverage gaps
- No note ever persisted, so view, edit, delete and real search were unreachable
- Export never clicked; Memories editing never available to test
- Desktop 1440×900 only; no mobile run

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice 01, 02, 03, 04, 05, 06, 07; power-user 02, 03, 07 (00-* auth wall, excluded)
