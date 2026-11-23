# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) · Layer B (HAX — applies: the Memories page is an inferred-profile surface) · Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user); findings rest on personas the agent invented
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Scope exclusion applied: "The login wall at /app/login.html — infrastructure, not a defect." (70 s / 40 s waits not scored)

---

## Findings

### edc94a3be15a — Save confirms success but the note never appears in list or search
- **Severity:** P0
- **So what:** Both personas lost every note they wrote, were told it was saved, and quit the product.
- **Framework tags:** A1, A9, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice saved "Dentist" twice (03:05, 03:50); "Saved ✓" both times; dashboard stayed "Nothing here yet."; search returned "No results for 'Dentist'."
  - Power-user saved "Roadmap" at 01:00; list empty; search for "Roadmap" returned nothing; stopped at 03:00
  - Both objectives logged `gave_up: true`; network shows `POST /api/notes → 500` at each save, never surfaced to the user
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-novice/timeline.json` · `persona-novice/network-full.txt`
  > "Saved twice, empty twice. It is lying to me."
  > "Save doesn't save and search doesn't search. Nothing else matters until those work."
- **Repro:**
  1. Create a workspace, open "New block".
  2. Enter a title and body, click Save.
  3. Observe "Saved ✓", then the dashboard still reading "Nothing here yet."
  4. Search the title — "No results".
- **Fix:** Show "Saved ✓" only after the save succeeds; on failure show an error, keep the draft, and offer Retry.

### 8ea73c1ed19e-a — Memories page presents invented facts about the user as remembered
- **Severity:** P0
- **So what:** The novice read fabricated "memories" as proof the product lies, and extended that distrust to "Saved".
- **Framework tags:** B-G2, B-G11, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer claims "Memories are built from your notes and connected accounts." — the persona had zero saved notes and no connected accounts
  - Novice stopped 1:40 later: "I'd stop here."
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a fresh workspace; connect nothing.
  2. Click "Memories" in the top nav.
  3. Observe three specific claims about the user with no source.
- **Fix:** Show only memories derived from the user's own notes, each linked to its source; show an empty state otherwise.

### 8ea73c1ed19e-b — Memories page presents invented facts about the user as remembered
- **Severity:** P1
- **So what:** The power-user dismissed Memories as a demo and cited it in the debrief as a reason not to trust the product.
- **Framework tags:** B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Saw the same three claims: Tuesday meetings, Jira, Q4 launch
  - Read them as a demo panel and moved on, but explicitly withheld trust
  - Debrief Q4 named it: "claims things I didn't"
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` · `persona-novice/screenshots/06-memories.png`
  > "Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a fresh workspace; connect nothing.
  2. Click "Memories".
  3. Observe claims with no source and no "sample" label.
- **Fix:** If these are sample memories, label them "Example" and replace them with the user's own once notes exist.

### e811aa9a5a4d — Irreversible workspace-type choice uses undefined jargon before the user sees the product
- **Severity:** P2
- **So what:** The novice spent 43 s guessing an unexplained, permanent choice before seeing anything; a less patient user leaves here.
- **Framework tags:** A2, A3, A5, A10, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Options "Federated graph", "Sovereign vault", "Hybrid mesh" with no descriptions; warning "This cannot be changed later."
  - Novice arrived 00:05, chose at 00:48 by guessing: "sounds like it includes the other two"
  - Power-user chose in under 30 s: "Fine — I've seen worse." — no friction for this persona
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/session.log:8`
  > "I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; land on /app/signup.html.
  2. Observe three unexplained radio options and "This cannot be changed later."
- **Fix:** Default the workspace type silently, or add one plain-language line per option and make it changeable in Settings.

### 506fe9bb7b5f — Empty dashboard offers no next step towards a first note
- **Severity:** P2
- **So what:** The novice expected their stuff, got "Nothing here yet.", and hunted the nav for 45 s before creating anything.
- **Framework tags:** A10, A6, C-TTFV
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel reads only "Nothing here yet." — no button, no hint
  - Novice searched an empty workspace ("meeting") before finding "New block" at 01:40
  - Timeline records `times_had_to_hunt: 2`
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14` · `persona-novice/timeline.json`
  > "Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a fresh workspace.
  2. Observe the dashboard empty state.
- **Fix:** Replace "Nothing here yet." with a "Write your first note" button opening the editor.

### d2981bf762b9 — One object carries three names: cards, blocks and notes
- **Severity:** P2
- **So what:** The novice could not tell whether "Cards" and "New block" were the same thing, slowing the first create.
- **Framework tags:** A4, A2
- **Flow:** shape_2
- **Locator:** top nav
- **Personas hit:** novice
- **Observed:**
  - Nav reads "Cards" and "New block"; dashboard heading "Your cards"; search placeholder "Search your notes"
  - Editor heading is "New block"; Settings export says "Markdown, all cards"
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json`
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Open the dashboard.
  2. Compare the nav labels, "Your cards" heading and "Search your notes" placeholder.
- **Fix:** Pick one noun — "note" — and use it in the nav, editor heading, dashboard, search and export.

### b575f1eaa1f9 — Settings toggles use unexplained jargon and do not echo the signup choice
- **Severity:** P2
- **So what:** Neither persona could tell what the toggles do, or whether one is the permanent signup choice.
- **Framework tags:** A2, A4, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Toggles "Enable webhook sync", "Federated graph replication" (checked), "Vault attestation" with no descriptions
  - "Federated graph replication" is checked for the novice, who picked "Hybrid mesh" at signup
  - Both personas found "Export — Markdown, all cards" clear
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-power-user/session.log:13`
  > "'Federated graph replication' is on by default. I picked that at signup — is this the same thing?"
- **Repro:**
  1. Pick "Hybrid mesh" at signup.
  2. Open Settings.
  3. Observe "Federated graph replication" checked and no explanation on any toggle.
- **Fix:** Add a one-line description under each toggle and show the chosen workspace type, read-only, at the top of Settings.

### a0e8dc828698 — No keyboard shortcuts for capture or search
- **Severity:** P2
- **So what:** The keyboard-driven evaluator found none of the expected shortcuts — a mark against switching the team.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html keyboard
- **Personas hit:** power-user
- **Observed:**
  - Tried Ctrl+K, Ctrl+N and "/" on the dashboard at 01:30 — none did anything
  - Persona's stated expectation pre-session: "fast capture, good search, keyboard-driven"
- **Evidence:** `persona-power-user/session.log:3` · `persona-power-user/session.log:12` · `persona-power-user/screenshots/02-dashboard.png`
  > "No keyboard shortcuts at all."
- **Repro:**
  1. Open the dashboard.
  2. Press Ctrl+K, Ctrl+N, then "/".
  3. Observe no response.
- **Fix:** Bind "/" to focus search and Ctrl+N to "New block", and list both in a shortcuts hint.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- "Saved ✓" toast placement/visibility — `persona-novice/screenshots/04-note-saved-toast.png` shows the empty editor, not the toast; toast cited from log only.
- Whether search works on existing notes — no note was ever stored, so search could not be tested independently of Save.
- Export button behaviour — neither persona clicked Export.

## For other lenses
- `POST /api/notes → 500` on every save; `renderGraphOverlay is not defined` on dashboard — bugs
- "Federated graph", "Sovereign vault", "Vault attestation" jargon density — content
- Marketing promise "remembers everything so you never start from zero" vs empty first run — onboarding
- WCAG / accessibility — no lens covers it; radio and checkbox controls sit detached above their labels (screenshots 01, 07)

## Coverage gaps
- Mobile viewport never tested; both personas desktop 1440×900
- Note edit, delete and Export never exercised
- No persona connected an account, so the Memories source claim was not testable

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — novice 00–07 (8 files), power-user 00, 02, 03, 07 (4 files); all opened
