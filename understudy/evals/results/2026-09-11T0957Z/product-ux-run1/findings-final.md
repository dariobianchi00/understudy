# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) + Layer B (HAX, Memories surface only) + Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED, not researched
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### d1b9b1da0962 — Save reports "Saved ✓" but the note never appears in the list or in search
- **Severity:** P0
- **So what:** Both personas believe they lost their work and stop trusting anything the product tells them.
- **Framework tags:** A1, A9, A5, C-ABANDON, C-TTFV
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Both personas saw a green "Saved ✓" confirmation, were returned to the dashboard, and found "Nothing here yet."
  - Searching the note's own title returned "No results for 'Dentist'" and "No results for 'Roadmap'".
  - Novice repeated the whole save a second time and got the same success message and the same empty list.
- **Evidence:** `persona-novice/session.log:17-20` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/timeline.json` (`gave_up: true`) · `persona-novice/network-full.txt:5,7` (`POST /api/notes → 500`, cited only as proof the save never completed)
  > "Saved twice, empty twice. It is lying to me."
- **Repro:**
  1. Open `/app/new.html`, enter a title and body.
  2. Click Save; observe the "Saved ✓" toast and the return to `/app/dashboard.html`.
  3. Observe "Your cards" still reads "Nothing here yet."; search the title and get "No results".
- **Fix:** Show the toast only on a persisted write; on failure keep the user on the compose form with the text intact and an inline "Couldn't save — retry" message.

### 790a6c8df52e — Memories asserts three facts about the user that they never provided
- **Severity:** P0
- **So what:** The novice concluded the product invents things about her, which retrospectively destroyed her belief in the "Saved ✓" message.
- **Framework tags:** A1, B-G1, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - The page headed "What Nimbus remembers about you" listed "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - The novice had written one note, about a dentist, and connected no accounts.
  - Footnote reads "Memories are built from your notes and connected accounts." — neither source exists for this user, and no per-item provenance is shown.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
- **Repro:**
  1. Create a new workspace and write one note.
  2. Open `/app/memories.html`.
  3. Observe three assertions about the user unrelated to anything they entered.
- **Fix:** Show an empty state on `/app/memories.html` until real memories exist, and attach a "from <note title>" source link to every item once they do.

### d1199242754f — Memories cites sources the evaluator never connected, so the surface is written off as a demo
- **Severity:** P2
- **So what:** The power-user files a headline feature as fake and stops counting it toward the buying decision.
- **Framework tags:** B-G2, B-G11, A1
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three fabricated memories, reached at 02:30 while evaluating the product for a team switch.
  - Persona classified the surface as placeholder content rather than a defect, and discounted it.
  - No labelling on the page distinguishes sample content from real inference.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` (t 02:30) · `persona-novice/screenshots/06-memories.png` (same page, captured under `persona-novice`)
  > "Memories aren't mine. A demo panel, I assume."
- **Repro:**
  1. Sign up as a new user, write one note.
  2. Open `/app/memories.html` and compare the listed memories against what was entered.
- **Fix:** If the panel ever ships seeded content, label it "Example" on the page; otherwise render it empty until a memory is derived from the user's own notes.

### 7c1ffccac013 — Signup demands an irreversible workspace type from three terms the novice cannot decode
- **Severity:** P1
- **So what:** The novice made a permanent architectural choice by guessing, 55 seconds before seeing what the product is.
- **Framework tags:** A2, A3, A5, A10, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Screen reads "Before we begin, choose your workspace type" with "Federated graph", "Sovereign vault", "Hybrid mesh" and "This cannot be changed later."
  - No description, tooltip, help link or default is offered for any of the three options.
  - Persona stalled 28 seconds, then chose "Hybrid mesh" on the reasoning that it "sounds like it includes the other two".
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9-11` · `persona-novice/findings-raw.json` (t 00:20)
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the auth wall and land on `/app/signup.html`.
  2. Read the three radio labels and the "This cannot be changed later." caption.
- **Fix:** Give each option a one-line plain-English description, preselect a sensible default, and either defer the choice to Settings or drop "This cannot be changed later."

### 99e9cc7669c9 — Power user makes the irreversible workspace choice blind but shrugs it off
- **Severity:** P3
- **So what:** The same screen costs an experienced evaluator nothing, which is why the novice's 28-second stall reads as the product picking its user.
- **Framework tags:** A2, A5
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Persona selected "Federated graph" within 30 seconds without asking what it meant.
  - Same absent descriptions and same "This cannot be changed later." caption.
  - Recorded as tolerated, not understood — the choice was still made without information.
- **Evidence:** `persona-power-user/session.log:8` · `persona-power-user/timeline.json` (`shape_1` 00:00–00:30) · `persona-novice/screenshots/01-signup-workspace-type.png` (same screen)
  > "Fine — I've seen worse. Picked Federated graph."
- **Repro:**
  1. Land on `/app/signup.html` as a returning-category user.
  2. Select any option and continue; note that no consequence of the choice is ever surfaced.
- **Fix:** Add the same one-line descriptions as above, and state on the screen what the choice actually changes in the product.

### ba8d78fc0b6b — Cards, blocks and notes are three names for the same object across nav, list and search
- **Severity:** P2
- **So what:** The novice hesitated over which menu item creates a note, and hunted twice for the one she had written.
- **Framework tags:** A4, A2, A6
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Nav reads "Cards" and "New block"; the list heading reads "Your cards"; the search placeholder reads "Search your notes".
  - Persona asked whether cards and blocks were the same thing before clicking "New block".
  - `timeline.json` records `times_had_to_hunt: 2` for this persona.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` (t 01:40)
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Open `/app/dashboard.html` and read the nav, the list heading and the search placeholder.
  2. Open `/app/new.html` and read the page title.
- **Fix:** Pick one noun — "note" — and use it in the nav ("Notes", "New note"), the list heading and the search placeholder.

### 525cd73b380f — Empty dashboard offers no next step, against a promise of a workspace that fills itself
- **Severity:** P2
- **So what:** The novice arrived expecting her existing material and got a blank page with nothing to click.
- **Framework tags:** A1, A6, A10, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" shows only "Nothing here yet." — no call to action, no import path, no link to create anything.
  - Persona arrived from marketing copy "remembers everything so you never start from zero" and expected existing material to be present.
  - She tried the search box on an empty account before finding the create path in the nav.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12-13` · `persona-novice/persona-debrief.md` Q4
  > "'Nothing here yet.' Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup and land on `/app/dashboard.html` with no content.
  2. Observe the empty state text and the absence of any action.
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button plus an "Import from…" link, so the empty state is the first step rather than a dead end.

### 5084fecf04fe — Settings toggles are labelled in internal infrastructure terms with no explanation
- **Severity:** P2
- **So what:** The novice cannot tell what any switch on her own account does, and one is already on.
- **Framework tags:** A2, A8, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice
- **Observed:**
  - Three checkboxes read "Enable webhook sync", "Federated graph replication", "Vault attestation", with no help text.
  - "Federated graph replication" is checked by default; the other two are unchecked.
  - The only control the persona understood was "Export" with the caption "Markdown, all cards".
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23-24` · `persona-novice/findings-raw.json` (t 05:20)
  > "Webhook sync, graph replication, vault attestation — no idea. Export is clear."
- **Repro:**
  1. Open `/app/settings.html`.
  2. Read the three toggle labels; note no description accompanies any of them.
- **Fix:** Add a one-line plain-English description under each toggle on `/app/settings.html`, or move developer-only switches behind an "Advanced" section.

### db25dc387fa3 — Settings repeats the signup workspace term with no indication the two are the same setting
- **Severity:** P2
- **So what:** The evaluator cannot tell whether a toggle here would undo a choice signup said was permanent.
- **Framework tags:** A4, A1, A3
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - Persona selected "Federated graph" at signup, then found "Federated graph replication" checked on in Settings.
  - Nothing on the Settings page states which workspace type is active or whether the toggle relates to it.
  - Signup said the workspace type "cannot be changed later", so an apparently editable checkbox with the same words is contradictory.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:8,13` · `persona-power-user/findings-raw.json` (t 02:00)
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Choose "Federated graph" at `/app/signup.html`.
  2. Open `/app/settings.html` and compare the checked toggle's label with the signup choice.
- **Fix:** Show the active workspace type as read-only text at the top of `/app/settings.html` and rename the toggle so it cannot be confused with it.

### 8dfc8d48899c — No keyboard shortcuts: Ctrl+K, Ctrl+N and / all do nothing
- **Severity:** P2
- **So what:** The persona evaluating a team switch found the capture speed he came for is absent.
- **Framework tags:** A7, C-TTFV
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - Persona arrived expecting "fast capture, good search, keyboard-driven".
  - Tried Ctrl+K, Ctrl+N and "/" on the dashboard at 01:30; none had any effect.
  - Every action in the session required the mouse and the top nav.
- **Evidence:** `persona-power-user/session.log:3,12` · `persona-power-user/screenshots/02-dashboard.png` · `persona-power-user/findings-raw.json` (t 01:30)
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Open `/app/dashboard.html`.
  2. Press Ctrl+K, then Ctrl+N, then "/"; observe no focus change and no palette.
- **Fix:** Bind "/" to focus the search box and Ctrl+N to open the compose form, and list both in a shortcuts hint on the dashboard.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast may not be dismissible or may auto-hide too quickly — the toast is not visible in any captured screenshot, only described in `persona-novice/session.log:17`.
- The live preview may be the product's strongest moment for other users — only one persona reacted to it (`persona-novice/session.log:16`), too thin to score.
- The Cards nav item may lead to a different list from the dashboard — neither persona clicked "Cards", so its destination was never captured.
- Export may produce nothing given no notes persist — neither persona clicked Export; no output artifact exists.

## For other lenses
- `POST /api/notes → 500` twice and repeated `Uncaught ReferenceError: renderGraphOverlay is not defined` on the dashboard — `bugs`.
- Jargon density and reading level of the signup, Memories and Settings copy — `content`.
- Marketing promise "remembers everything so you never start from zero" versus an empty first-run state — `onboarding` and `content`.
- Drop-off shape: both personas abandoned inside `shape_2` without completing the objective — `onboarding`.

## Coverage gaps
- `persona-novice/screenshots/04-note-saved-toast.png` shows the reset compose form with no toast visible; the "Saved ✓" wording rests on `session.log:17` alone.
- `persona-power-user/screenshots/03-search-empty.png` shows the dashboard with an empty search box, not a rendered "No results" state; the result text rests on `session.log:11`.
- Power-user captured no signup or compose screenshot — that persona's `shape_1` is evidenced by log and timeline only.
- Cards list with content, search with results, note editing, note deletion and Export output were never reached.
- Desktop 1440x900 only; no mobile or tablet viewport tested.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — `persona-novice/screenshots/00-start.png`, `00-wall-cleared.png`, `01-signup-workspace-type.png`, `02-dashboard-empty.png`, `03-new-note.png`, `04-note-saved-toast.png`, `05-notes-list-missing.png`, `06-memories.png`, `07-settings.png` · `persona-power-user/screenshots/00-start.png`, `02-dashboard.png`, `03-search-empty.png`, `07-settings.png`
