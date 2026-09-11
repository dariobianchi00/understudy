# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT), with Layer A tags where the funnel breaks on usability
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: opus
- Layer B (AI guidelines) applied only to Memories, the one surface that claims inference
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### 4ff871ce9e74 — Save shows "Saved ✓" on a 500, and the note never reaches the cards list or search
- **Severity:** P0
- **So what:** Both personas lost the only thing they gave the product, and both quit within four minutes of saving.
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST /api/notes` returned `500 internal error` three times across the two sessions; the UI showed a green "Saved ✓" each time.
  - Dashboard still read "Nothing here yet." after each save; search for the note title returned "No results".
  - Novice saved the same note twice to test it, got "Saved ✓" twice, and concluded the product was lying.
- **Evidence:** `persona-novice/network-full.txt:5` · `persona-novice/network-full.txt:7` · `persona-power-user/network-full.txt:3` · `persona-novice/session.log:17-20` · `persona-power-user/session.log:11` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png`
  > "Saved twice, empty twice. It is lying to me."
- **Repro:**
  1. Clear the auth wall and create a workspace.
  2. Open "New block", enter a title and body, click Save.
  3. Observe "Saved ✓" while `POST /api/notes` returns 500.
  4. Return to the dashboard: "Nothing here yet." Search the title: "No results".
- **Fix:** Gate the "Saved ✓" toast on a 2xx from `POST /api/notes`; on failure keep the draft on screen and show a retry with the plain-language reason.

### 3e02584db960 — Onboarding has no import or connect step, so the promised pre-filled start is an empty workspace
- **Severity:** P1
- **So what:** Both personas arrived expecting their existing material and got a blank page, so the product's core promise fails at minute one.
- **Framework tags:** A2, B-G1, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Both arrived on the promise "remembers everything so you never start from zero"; signup offered only a workspace-type radio group, no import or account connection.
  - First screen after signup is "Your cards" / "Nothing here yet."
  - Memories then claims it is "built from your notes and connected accounts" — a connection step neither persona was ever offered.
- **Evidence:** `persona-novice/session.log:1-2` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/06-memories.png` · `persona-power-user/persona-debrief.md`
  > "Dashboard. 'Your cards' — 'Nothing here yet.' Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Arrive from the marketing promise and complete signup.
  2. Look for any way to bring in existing notes or connect an account.
  3. Observe none exists anywhere in signup, the dashboard, or Settings.
- **Fix:** Add an "Import notes / connect an account" step to signup, or change the dashboard empty state to state plainly that Nimbus starts blank.

### a0b9955d3ccb — Signup gates the product behind an irreversible choice between three terms the novice does not know
- **Severity:** P1
- **So what:** The novice guessed at a permanent decision 48 seconds before she had seen the product do anything.
- **Framework tags:** A2, A3, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - First post-wall screen reads "Before we begin, choose your workspace type" with "Federated graph", "Sovereign vault", "Hybrid mesh" and the note "This cannot be changed later."
  - No explanation, default, tooltip, or "decide later" option is offered.
  - Novice stalled 28 seconds, then picked "Hybrid mesh" on the guess that it included the other two.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9-11` · `persona-novice/findings-raw.json` (t=00:20)
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the auth wall; land on `/app/signup.html`.
  2. Read the three options and the "This cannot be changed later." line.
  3. Observe there is no way to skip, default, or learn what they mean.
- **Fix:** Default new workspaces to one type, move the choice into Settings as reversible, and describe each option in one plain sentence.

### a291b5ab1dd1 — Memories asserts three facts the novice never provided, and she then doubts the Saved confirmation too
- **Severity:** P1
- **So what:** An invented profile in session one turned a save bug into a reason to distrust everything the product says.
- **Framework tags:** A1, B-G1, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer reads "Memories are built from your notes and connected accounts."; the novice had zero saved notes and no connected account.
  - She stopped 100 seconds later, citing the false profile alongside the lost notes.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-novice/session.log:25`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
- **Repro:**
  1. Complete signup with a fresh workspace.
  2. Click "Memories" in the nav before saving anything.
  3. Observe three first-person claims about a user the product has no data on.
- **Fix:** Show an empty Memories state until a memory is derived from real user content, and label each memory with the note it came from.

### ff5537b33490 — Power user writes Memories off as a demo panel and stops trusting what the product claims
- **Severity:** P2
- **So what:** The expert discounts a headline feature within 30 seconds of seeing it, so it cannot contribute to his buying case.
- **Framework tags:** B-G1, B-G2, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three fabricated memories shown to a workspace with no saved content.
  - He read them as seeded demo data rather than a fault, and disengaged without investigating.
  - Memories appears in neither of the two things he could name the product doing.
- **Evidence:** `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` (t=02:30) · `persona-power-user/persona-debrief.md` · `persona-novice/screenshots/06-memories.png`
  > "Memories aren't mine. A demo panel, I assume."
- **Repro:**
  1. Complete signup as a new workspace.
  2. Open "Memories" with nothing saved.
  3. Observe generic claims with no provenance and no empty state.
- **Fix:** Mark any pre-seeded content as "Example" on the Memories page, or suppress it entirely for workspaces with no user content.

### af6ea29f25a1 — Empty dashboard names no first action, costing the novice 45 seconds of hunting before New block
- **Severity:** P1
- **So what:** The first screen after signup gives a new user nothing to do, and she went looking in the search box instead.
- **Framework tags:** A6, A8, C-STEPS, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard shows a search field, "Your cards", and "Nothing here yet." — no button, link, or prompt to create anything.
  - Novice searched "meeting" on an empty workspace at 01:20 before finding the nav at 01:40.
  - 45 seconds elapsed between reaching the dashboard and opening "New block"; `timeline.json` records 2 hunts.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12-14` · `persona-novice/timeline.json` (`shape_2.times_had_to_hunt`: 2)
  > "'Nothing here yet.' Nothing tells me what to do."
- **Repro:**
  1. Create a workspace and land on `/app/dashboard.html`.
  2. Read the "Your cards" panel with no content.
  3. Observe no call to action anywhere on the screen.
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button that opens the New block form.

### db87f9827639 — One object carries three names across the nav and the empty states: cards, blocks, notes
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" would produce the "cards" she was looking at, which is why she hesitated to click it.
- **Framework tags:** A2, A4, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - One screen shows "Search your notes" above a panel headed "Your cards"; the nav offers "Cards" and "New block".
  - Novice asked whether cards and blocks were the same thing before clicking.
  - The form she reached is titled "New block" and saves into "Your cards".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` (t=01:40)
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Open `/app/dashboard.html` and read the search placeholder and the panel heading.
  2. Read the nav items "Cards" and "New block".
  3. Open the form and read its title.
- **Fix:** Pick one noun — "note" — and use it in the nav, the search placeholder, the list heading, and the form title.

### 4dcc9176a7c7 — Settings repeats the irreversible signup choice as a toggle with no sign it is the same decision
- **Severity:** P2
- **So what:** The power user could not confirm what he had permanently chosen, on the one decision the product told him he could not undo.
- **Framework tags:** A1, A4, A6
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - He selected "Federated graph" at signup under "This cannot be changed later."
  - Settings shows "Federated graph replication" as a checked checkbox beside "Enable webhook sync" and "Vault attestation", with no explanation or back-reference.
  - He could not tell whether the toggle reflected his choice or was a separate, editable setting.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:8` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json` (t=02:00)
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Pick "Federated graph" at signup.
  2. Open `/app/settings.html`.
  3. Observe "Federated graph replication" checked, with no statement that it is the signup choice.
- **Fix:** Add a read-only "Workspace type: Federated graph (set at signup)" row in Settings, and rename the toggle so it cannot be confused with it.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast may block or overlay the dashboard redirect — the screenshot named `04-note-saved-toast.png` does not contain a toast, so its appearance and duration are unverified.
- Whether a first-run tour or tooltip exists and was dismissed before capture — no screenshot between the wall clearing and the workspace-type screen.
- Whether the novice's guessed workspace type changed anything she saw — only one type was exercised per persona.

## For other lenses
- `POST /api/notes` → 500 and `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load — `bugs`.
- No keyboard shortcuts: Ctrl+K, Ctrl+N and `/` all inert for the power user — `ux`.
- Settings labels "Enable webhook sync", "Federated graph replication", "Vault attestation" are unglossed jargon on a consumer surface — `content`.
- "Memories are built from your notes and connected accounts." is false for a new workspace — `content`.

## Coverage gaps
- `persona-novice/screenshots/04-note-saved-toast.png` shows an empty "New block" form at "0 words", not the "Saved ✓" toast — the toast is evidenced only by `session.log:17`.
- Neither `05-notes-list-missing.png` nor `03-search-empty.png` shows a typed query or the "No results" string; both show the empty cards list. The search results are evidenced by the session logs.
- `persona-novice/screenshots/00-wall-cleared.png` duplicates `01-signup-workspace-type.png`; no capture of the moment the wall cleared.
- The "Cards" nav item was never clicked by either persona.
- No second session, so whether anything survives a return visit is untested.
- One viewport only (desktop-1440x900); no mobile funnel.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — `persona-novice/screenshots/` (8) · `persona-power-user/screenshots/` (4)
