# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) · Layer B (HAX — applies: "Memories" is a user-facing AI surface) · Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Objective under test: "A new user can write a note and find it again" — **failed for both personas**

---

## Findings

### 7af4bccaa564 — Save shows "Saved ✓" but the note never reaches "Your cards" or search
- **Severity:** P0
- **So what:** Both personas lost every note they wrote and were told it was safe; this is the reason both said they would not return.
- **Framework tags:** A1, A9, A5, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice saved "Dentist" twice (03:05, 03:50); "Saved ✓" each time; dashboard still "Nothing here yet."; search "No results for 'Dentist'."
  - Power-user saved "Roadmap" at 01:00; same "Saved ✓", empty list, no search result; stopped at 03:00.
  - Network shows `POST /api/notes → 500` at each save; the UI reported success anyway (cited as evidence only).
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-novice/network-full.txt:5` · `persona-novice/timeline.json` objectives[0].gave_up = true
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." (novice)
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." (power-user)
- **Repro:**
  1. Sign up, open "New block".
  2. Enter a title and body, click Save.
  3. Observe "Saved ✓", then the dashboard's "Nothing here yet." and an empty search for the title.
- **Fix:** Show "Saved ✓" only after the save request succeeds; on failure keep the form filled and show a plain error with Retry.

### c8ffc1a29fac — Memories page states invented facts about a brand-new novice, who then stopped trusting Saved
- **Severity:** P0
- **So what:** Confident false claims about her own life made the novice doubt every other message, including the save confirmation.
- **Framework tags:** B-G1, B-G2, B-G11, B-G9, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - At 04:30, four minutes into a new account with zero saved notes, "What Nimbus remembers about you" lists three claims.
  - Claims: "You prefer to schedule meetings on Tuesday afternoons." · "Your team uses Jira and Slack." · "You are working on a product launch in Q4."
  - No source, no edit or delete control; footnote says "Memories are built from your notes and connected accounts."
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:24` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
  > "the "memories" it does have aren't mine."
- **Repro:**
  1. Create a fresh account; connect nothing.
  2. Open "Memories" from the top nav.
  3. Observe three specific personal facts the user never supplied.
- **Fix:** On a new account show an empty Memories state explaining how memories form; attach a source and a remove control to each memory.
- Severity note: rubric lists "confident nonsense about the persona's own data" as P0; torn with P1, took P0.

### fe3551c8b4d3 — Power user dismisses Memories as a demo panel because nothing labels the facts as sample data
- **Severity:** P2
- **So what:** The expert contained the damage by guessing it was fake, but wrote off the headline "remembers" feature as untrustworthy.
- **Framework tags:** B-G2, B-G11, A1
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - At 02:30 read the same three claims (Tuesday meetings, Jira, Q4 launch); shrugged and moved on.
  - Treated the page as a demo, not as product output; did not act on it.
  - Debrief cites it against the promise: "claims things I didn't".
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4 · `persona-novice/screenshots/06-memories.png` (same page content)
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a fresh account.
  2. Open "Memories".
  3. Observe unlabelled example facts presented as the user's own.
- **Fix:** If sample memories are intended, label them "Example" on the Memories page and replace them with real ones once notes exist.

### 093bb613a876 — Signup forces an irreversible workspace type in unexplained terms before the product is shown
- **Severity:** P2
- **So what:** A first-time user makes a permanent choice by guessing, at second 5, before seeing any value — a likely exit point for less patient users.
- **Framework tags:** A2, A3, A5, A10, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh"; no descriptions, no default.
  - Warning "This cannot be changed later." sits under the options.
  - Novice hesitated 43 s (00:05–00:48) and picked "Hybrid mesh" because "it sounds like it includes the other two".
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear login, land on /app/signup.html.
  2. Observe three options with no explanation and "This cannot be changed later."
- **Fix:** Default the workspace type silently, or add one plain sentence per option and make it changeable in Settings.

### 3a9ffccfb568 — Empty dashboard says only "Nothing here yet." with no first step, contradicting "never start from zero"
- **Severity:** P2
- **So what:** The novice arrived expecting her stuff; the blank page gave no next action and broke the marketing promise at minute 1.
- **Framework tags:** A10, A6, C-SOWHAT, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel reads "Nothing here yet." — no button, no hint, no import.
  - Novice searched "meeting" on an empty account, then hunted the nav before finding "New block" at 01:40.
  - Debrief: "it started completely empty".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/persona-debrief.md` Q4
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup.
  2. Observe the dashboard with only "Nothing here yet." and a search box.
- **Fix:** Put a "Write your first note" button inside the empty "Your cards" panel, with one line on what Nimbus will remember.

### 39cd897e737b — Same object is called cards, block and notes across nav, dashboard and search
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" creates the thing listed under "Your cards", slowing her first action.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** top nav · /app/dashboard.html · /app/new.html
- **Personas hit:** novice
- **Observed:**
  - Nav: "Cards", "New block"; dashboard heading "Your cards"; search placeholder "Search your notes"; editor heading "New block".
  - Novice paused to ask whether cards and blocks are the same, then clicked "New block" to find out.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Open the dashboard.
  2. Compare "Cards", "New block", "Your cards" and "Search your notes".
- **Fix:** Pick one noun ("note") and use it in the nav, dashboard heading, editor heading and search placeholder.

### 19142670f66e — Settings toggles use unexplained terms and "Federated graph replication" is on whichever workspace type was chosen
- **Severity:** P2
- **So what:** Neither persona could tell what the toggles do or whether they relate to the "cannot be changed" signup choice.
- **Framework tags:** A2, A4, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Toggles "Enable webhook sync", "Federated graph replication" (checked), "Vault attestation" — no helper text.
  - Novice chose "Hybrid mesh", power-user chose "Federated graph"; both screenshots show "Federated graph replication" checked.
  - Both found "Export — Markdown, all cards" clear.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-power-user/session.log:13`
  > "Webhook sync, graph replication, vault attestation — no idea. Export is clear." (novice)
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link." (power-user)
- **Repro:**
  1. Sign up choosing "Hybrid mesh".
  2. Open Settings.
  3. Observe "Federated graph replication" checked with no explanation.
- **Fix:** Add one line of helper text per toggle and show the chosen workspace type in Settings, linked to its related options.

### 3d2941957085 — No keyboard shortcuts for new note or search; Ctrl+K, Ctrl+N and / do nothing
- **Severity:** P2
- **So what:** The power user came for "keyboard-driven" capture and found none — a switching blocker once saving works.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - At 01:30 tried Ctrl+K, Ctrl+N and / on the dashboard; nothing happened.
  - Pre-session expectation: "fast capture, good search, keyboard-driven".
- **Evidence:** `persona-power-user/session.log:3` · `persona-power-user/session.log:12` · `persona-power-user/screenshots/02-dashboard.png`
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Open the dashboard.
  2. Press Ctrl+K, Ctrl+N, then /.
  3. Observe no response.
- **Fix:** Bind / to focus search and Ctrl+N (or N) to "New block", and list shortcuts in Settings.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Top nav (Cards, Memories, Settings) visible on the signup screen before a workspace exists — in screenshot, but no persona reacted; no observed consequence.
- `persona-novice/screenshots/04-note-saved-toast.png` shows an empty New block form, not the "Saved ✓" toast — toast evidence rests on `session.log:17` and `:20` only.
- `persona-novice/screenshots/03-new-note.png` shows an empty form — live word count and preview (novice's one value moment) rest on `session.log:16` only.
- `persona-power-user/screenshots/03-search-empty.png` shows an empty search box, not a "Roadmap" query or a "No results" message — search failure rests on `session.log:11`.

## For other lenses
- `POST /api/notes → 500` on every save, and `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load — bugs.
- Jargon density in signup and Settings ("Sovereign vault", "Vault attestation") — content.
- Irreversible pre-value choice as the first onboarding step; give-up at 03:00 and 06:30 — onboarding.
- Promise "remembers everything so you never start from zero" vs an empty start — content / onboarding.

## Coverage gaps
- Export was seen but never clicked; whether it produces a file is unknown.
- Search never tested against a note that had actually saved — search could not be judged on its own.
- Desktop 1440×900 only; no mobile.
- Accessibility (WCAG) not assessed — no lens covers it.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast, 05-notes-list-missing, 06-memories, 07-settings · power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
