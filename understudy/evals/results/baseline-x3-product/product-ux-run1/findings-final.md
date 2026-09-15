# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) · Layer B (HAX) — applied to the Memories surface only · Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user; both desktop 1440×900)
- Scoring model: opus · traversal: fixture-hand-authored
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B: the product has one user-facing inference surface (`Memories`, "built from your notes and connected accounts"); B tags appear on that finding only
- Scope exclusion applied: the login wall at `/app/login.html` is never a finding
- Console errors and 500s are cited as evidence for usability findings only; the defects themselves belong to `bugs`

---

## Findings

### 9d6089836d16 — Save shows "Saved ✓" then the note is absent from the list and from search
- **Severity:** P0
- **So what:** Both personas lost every note they wrote, were told it worked, and quit; the one job the product exists for fails.
- **Framework tags:** A1, A9, C-ABANDON, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice saved "Dentist" twice; each time a green "Saved ✓" toast, redirect to dashboard, "Your cards — Nothing here yet.", search "No results for 'Dentist'".
  - Power-user saved "Roadmap" once; same toast, empty list, search "No results". Gave up on the objective at 01:30.
  - Each save is a `POST /api/notes → 500` (network-full.txt:5,7; power-user:3); the UI shows success anyway.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:20` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-novice/timeline.json` objectives[0].gave_up=true · `persona-power-user/timeline.json` objectives[0].gave_up=true
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." — novice, 03:50
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." — power-user, 03:00
- **Repro:**
  1. Sign up, pick any workspace type, land on `/app/dashboard.html`.
  2. Click "New block", enter a title and body, click "Save".
  3. Observe the "Saved ✓" toast, then "Nothing here yet." on the dashboard; search the title → "No results".
- **Fix:** On `/app/new.html`, show "Saved ✓" only on a 2xx from `/api/notes`; on failure keep the draft in the editor and show an inline "Couldn't save — try again" with a retry button.

### 7a94aec62bb2-a — Memories page states facts about the user that the user never gave it
- **Severity:** P0
- **So what:** The novice read three false facts about herself, concluded the product fabricates, and named it as the moment she would stop.
- **Framework tags:** A1, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Page titled "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Novice had written one note ("Dentist") and connected no accounts; footer says "Memories are built from your notes and connected accounts."
  - No source, date, or "why" is shown for any memory; no way to dismiss or correct one is visible.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?" — novice, 04:50
  > "I've spent six minutes and I have zero notes saved and a page telling me things about myself that aren't true. I'd stop here." — novice, 06:30
- **Repro:**
  1. Create a fresh workspace with no connected accounts.
  2. Open "Memories" in the top nav.
  3. Observe three pre-filled memories unrelated to anything entered.
- **Fix:** On `/app/memories.html`, show an empty state ("Nothing remembered yet — write a few notes") for new workspaces; if sample data must stay, label each card "Example" and add a source line per memory.

### 7a94aec62bb2-b — Memories page states facts about the user that the user never gave it
- **Severity:** P1
- **So what:** The power-user rationalised the false memories as a demo panel and moved on, but explicitly withdrew trust from the surface; he would not pay.
- **Framework tags:** B-G1, B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three memories ("Tuesday meetings, Jira, Q4 launch") shown after one note and no connected accounts.
  - Persona guessed "a demo panel"; nothing on the page says whether it is sample or real.
  - Severity ambiguity: the rubric's blocker tier covers "confident nonsense about the persona's own data"; held one tier lower because this persona did not cite it as a quit reason.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` t=02:30 · `persona-power-user/persona-debrief.md` Q4
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it." — power-user, 02:30
  > ""Remembers everything." No. It remembers nothing I gave it and claims things I didn't." — power-user debrief Q4
- **Repro:**
  1. Create a fresh workspace, write one note.
  2. Open "Memories".
  3. Observe three memories with no source and no sample/real marker.
- **Fix:** Same as -a: empty state for new workspaces, or an explicit "Example" badge and a per-memory "from: <note>" source line.

### d7ad1adddcbe-a — Irreversible workspace type demanded in three undefined terms before any value is shown
- **Severity:** P1
- **So what:** The first screen after signup stalled the novice for 43 seconds on a decision she was told she could never undo, about a product she had not seen.
- **Framework tags:** A2, A3, A5, A6, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Screen "Before we begin, choose your workspace type": "Federated graph", "Sovereign vault", "Hybrid mesh"; no description of any; footnote "This cannot be changed later."
  - Novice read at 00:05, still deciding at 00:20, guessed "Hybrid mesh" at 00:48 "because it sounds like it includes the other two".
  - Severity ambiguity: P2 (jargon) vs P1 (irreversible, unexplained, first 60 seconds); higher taken because the persona said she could not undo it and had seen nothing yet.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-novice/findings-raw.json` t=00:20
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo." — novice, 00:20
- **Repro:**
  1. Click "Create an account" on the login page and complete signup.
  2. Observe the workspace-type screen with three unexplained radio options and "This cannot be changed later."
- **Fix:** On `/app/signup.html`, pre-select a default, add one plain-language line under each option, and either allow changing it later in Settings or say why it is locked.

### d7ad1adddcbe-b — Irreversible workspace type demanded in three undefined terms before any value is shown
- **Severity:** P3
- **So what:** The power-user picked in under 30 seconds and moved on; the screen cost him nothing he noticed.
- **Framework tags:** A2, A3
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Same screen; persona chose "Federated graph" without comment on meaning.
  - Reached the dashboard at 00:30 (timeline shape_1 end).
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-power-user/session.log:8` · `persona-power-user/timeline.json` shape_1.end=00:30
  > "Workspace type: Federated graph / Sovereign vault / Hybrid mesh, cannot be changed. Fine — I've seen worse. Picked Federated graph." — power-user, 00:00
- **Repro:**
  1. Complete signup; observe the workspace-type screen.
- **Fix:** Same as -a; the change costs the power-user nothing.

### 3cc3d73e0abb — Empty dashboard says "Nothing here yet." and offers no next step
- **Severity:** P2
- **So what:** The novice arrived expecting her data, found a blank card and no instruction, and spent 45 seconds probing search and nav before finding "New block".
- **Framework tags:** A6, A10, C-TTFV, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard shows a search box and a "Your cards" panel with the single line "Nothing here yet."; no button, link or hint inside the empty state.
  - Novice tried search first ("meeting" → "No results"), then read the nav, then clicked "New block" at 01:40.
  - Power-user went straight to search and did not remark on the empty state.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14` · `persona-novice/timeline.json` shape_2.times_had_to_hunt=2
  > "Dashboard. "Your cards" — "Nothing here yet." Nothing tells me what to do. I thought it would have my stuff." — novice, 00:55
- **Repro:**
  1. Create a new workspace and land on `/app/dashboard.html`.
  2. Observe the "Your cards" panel with "Nothing here yet." and no call to action.
- **Fix:** Replace "Nothing here yet." on `/app/dashboard.html` with a primary "Write your first note" button linking to `/app/new.html` and one line saying what a card is.

### 829c957658f3 — Same object is called "Cards", "block" and "notes" across nav, heading and search
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" would create one of "Your cards", and had to click to find out.
- **Framework tags:** A4, A2, A6
- **Flow:** shape_1
- **Locator:** /app/dashboard.html nav
- **Personas hit:** novice
- **Observed:**
  - Top nav: "Cards", "New block"; panel heading "Your cards"; search placeholder "Search your notes"; editor heading "New block"; export label "Markdown, all cards".
  - Novice paused on the nav at 01:40 before choosing "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` t=01:40
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing? Clicked "New block"." — novice, 01:40
- **Repro:**
  1. Open `/app/dashboard.html`.
  2. Compare the nav item "New block", the panel "Your cards" and the placeholder "Search your notes".
- **Fix:** Pick one word (the persona's own word is "note") and use it in the nav item, the panel heading, the editor title, the search placeholder and the export label.

### bc807b42b1f7 — Settings toggles carry undefined labels with no explanation
- **Severity:** P2
- **So what:** The novice found three switches she could not interpret and only one control she understood; trust in the product's other claims eroded further.
- **Framework tags:** A2, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice
- **Observed:**
  - Settings shows three checkboxes — "Enable webhook sync", "Federated graph replication" (checked), "Vault attestation" — with no helper text.
  - "Export" with "Markdown, all cards" was the only control the persona could act on.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24`
  > "Settings. "Enable webhook sync", "Federated graph replication", "Vault attestation". No idea. There's an Export button — "Markdown, all cards". At least that's clear." — novice, 05:20
- **Repro:**
  1. Open "Settings" in the top nav.
  2. Observe three toggles with no description.
- **Fix:** On `/app/settings.html`, add one plain sentence under each toggle saying what it does and when to turn it on; hide toggles that are not user-facing.

### 6c35f7a379af — Signup workspace choice reappears as a settings toggle with no link between them
- **Severity:** P2
- **So what:** The power-user could not tell whether "Federated graph replication" was the thing he had just chosen, or whether the "cannot be changed" choice had a switch after all.
- **Framework tags:** A4, A6
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - Signup offers "Federated graph" as an unchangeable workspace type; Settings shows "Federated graph replication" as a checked checkbox.
  - Novice chose "Hybrid mesh", yet her Settings screenshot shows the identical checked "Federated graph replication" — the toggle does not reflect the signup choice.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json` t=02:00
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link." — power-user, 02:00
- **Repro:**
  1. Sign up choosing "Hybrid mesh".
  2. Open "Settings"; observe "Federated graph replication" checked.
- **Fix:** On `/app/settings.html`, show the workspace type as a read-only line ("Workspace type: Hybrid mesh — set at signup") and rename or remove the replication toggle so the two cannot be confused.

### 15a5120b49e8 — No keyboard shortcuts respond on the dashboard
- **Severity:** P2
- **So what:** The power-user's stated reason for evaluating was "fast capture … keyboard-driven"; three common shortcuts did nothing, removing his reason to switch.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - Persona pressed Ctrl+K, Ctrl+N and "/" on the dashboard; no response to any.
  - No shortcut hint is visible on the dashboard or in the search placeholder.
- **Evidence:** `persona-power-user/screenshots/02-dashboard.png` · `persona-power-user/session.log:3` · `persona-power-user/session.log:12` · `persona-power-user/findings-raw.json` t=01:30
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts." — power-user, 01:30
- **Repro:**
  1. Open `/app/dashboard.html`.
  2. Press Ctrl+K, then Ctrl+N, then "/".
- **Fix:** Bind "/" or Ctrl+K to focus search and Ctrl+N to open `/app/new.html`; show the key in the search placeholder ("Search your notes  /").

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Radio and checkbox controls sit centred above left-aligned labels on signup and settings (`01-signup-workspace-type.png`, `07-settings.png`) — visible, but neither persona reacted; no persona grounding.
- Save redirects to the dashboard immediately, losing editor context — novice noted "Then it went back to the dashboard" without complaint; no consequence observed.
- Toast copy or duration may be inadequate — `04-note-saved-toast.png` captures the empty form, not the toast; toast wording is known only from the session log.

## For other lenses
- `POST /api/notes → 500` on every save and `renderGraphOverlay is not defined` on every dashboard load — `bugs`.
- Promise "remembers everything so you never start from zero" vs a product that starts empty and keeps nothing — both debriefs Q4 fail — `content`.
- Both personas quit inside 7 minutes with the objective failed; funnel shape and drop-off timing — `onboarding`.
- Workspace-type and settings labels ("Federated graph", "Sovereign vault", "Vault attestation") as jargon density — `content`.
- Accessibility (label association of the detached radios/checkboxes) — no lens covers it; not scored here.

## Coverage gaps
- "Cards" nav item never opened by either persona.
- "Export" never clicked; Markdown export unverified.
- No note ever persisted, so note detail view, edit, delete and non-empty search were never reached.
- Desktop 1440×900 only; no mobile capture.
- `04-note-saved-toast.png` does not show the toast; the "Saved ✓" wording rests on session logs.
- Both traversals were hand-authored fixtures (manifest `traversal: fixture-hand-authored`).

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index
  - novice: 00-start, 00-wall-cleared, 01-signup-workspace-type, 02-dashboard-empty, 03-new-note, 04-note-saved-toast, 05-notes-list-missing, 06-memories, 07-settings
  - power-user: 00-start, 02-dashboard, 03-search-empty, 07-settings
