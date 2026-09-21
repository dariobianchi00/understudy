# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C (activation) — TTFV, steps to value, drop-off points, self-explanation; Layer A cited where it caused the drop-off
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED, not researched
- Scoring model: opus
- Layer B (AI-specific) applied only to the "Memories" panel, the one surface presented as inferred
- Every finding cites an artifact; unsupported observations dropped, listed at the end

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (post-wall signup) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen (irreversible) | ✓ 00:48 | ✓ ≤00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Editor found | ✓ 01:55 | ✓ 01:00 |
| Note composed | ✓ 02:41 | ✓ 01:00 |
| **First value reached** | ✓ 02:41 (live preview only) | ✗ never |
| Note saved and retrievable (the objective) | ✗ abandoned 03:50 | ✗ abandoned 01:30 |
| Returned to a second task | ✗ quit 06:30 | ✗ quit 03:00 |

**Steps to value:** 5 required · **Time to value:** 02:41 (novice), not reached (power-user) · **Drop-off:** Save → "Your cards"

- Required path to the objective: choose workspace type → Create workspace → New block → type → Save → return to list.
- Neither persona timed out; both stopped voluntarily, far inside the 90-minute cap.
- Wandering above the required path: novice `times_had_to_hunt: 2`, power-user `1`.

---

## Findings

### 6103db56ddee — "Saved ✓" confirms a save that never happens, and both personas quit there
- **Severity:** P0
- **So what:** Every persona lost the note they wrote and then stopped using the product; the funnel has no survivors past this step.
- **Framework tags:** A1, A9, C-TTFV, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html#save
- **Personas hit:** novice, power-user
- **Observed:**
  - Save posts to `/api/notes` and gets `500 internal error`; the UI still shows a green "Saved ✓" toast and returns to the dashboard.
  - "Your cards" still reads "Nothing here yet." and search for the note's own title returns "No results".
  - Novice repeated the whole write-and-save twice before concluding the product was lying.
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/network-full.txt` — `[POST] http://localhost:8765/api/notes → 500 internal error (03:05)`
  > "Saved twice, empty twice. It is lying to me."
- **Repro:**
  1. Sign up, choose any workspace type, land on `/app/dashboard.html`.
  2. Click "New block", enter a title and body, click "Save".
  3. Observe the green "Saved ✓" toast while `POST /api/notes` returns 500.
  4. Return to the dashboard: "Your cards" is empty; search the title returns "No results".
- **Fix:** Fix the 500 on `POST /api/notes`, and gate the "Saved ✓" toast on a 2xx response — on failure keep the user in the editor with their text and a plain-language retry.

### 882ea470dc02 — Fabricated "memories" made the novice distrust the save confirmation and stop
- **Severity:** P1
- **So what:** The novice generalised from invented facts to every claim the product makes, and ended the session rather than try a third save.
- **Framework tags:** A1, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - "What Nimbus remembers about you" lists three statements about Tuesday meetings, Jira/Slack and a Q4 launch for an account one minute old.
  - Footnote reads "Memories are built from your notes and connected accounts." — the novice had written one note, about a dentist, and connected nothing.
  - She then questioned the save confirmation on the same grounds and quit at 06:30.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:25`
  > "None of that is true. Where is this from? If it's making these up, is it making up the 'Saved' too?"
- **Repro:**
  1. Create a new workspace and write one note.
  2. Open "Memories" from the top nav.
  3. Observe three specific claims about the user that no session data supports.
- **Fix:** On `/app/memories.html`, show an empty state ("Nothing yet — memories appear once you've written a few notes") instead of seeded sample content, and label any sample content "Example" on its face.

### 095dd325bc1f — Power-user wrote off "Memories" as a demo panel and stopped trusting the surface
- **Severity:** P2
- **So what:** A feature the marketing promise is built on was silently discounted as fake, so it can never earn the evaluation it needs.
- **Framework tags:** B-G2, B-G11, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three seeded statements shown to an account with no notes and no connected sources.
  - Power-user did not investigate, did not report a bug, and carried on — then quit 30 seconds later for unrelated reasons.
  - Named it a demo panel rather than a defect, so the product got neither a trial nor a complaint.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json`
  > "Memories aren't mine. A demo panel, I assume."
- **Repro:**
  1. Sign up as a new user, write nothing.
  2. Open "Memories".
  3. Observe pre-populated claims with no provenance and no "Example" label.
- **Fix:** Add a provenance line under each memory on `/app/memories.html` naming the note or account it came from, and suppress the panel entirely until there is one.

### 91f29faee434 — Empty dashboard names no next step, costing the novice 60 seconds of hunting
- **Severity:** P2
- **So what:** A minute of the first three is spent looking for the editor, on a screen that could have pointed at it.
- **Framework tags:** A6, A10, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html#your-cards
- **Personas hit:** novice
- **Observed:**
  - Post-signup dashboard shows a search box and "Your cards — Nothing here yet." with no button, prompt or link.
  - Novice searched the empty product for "meeting" at 01:20 before reading the nav at 01:40.
  - Editor reached at 01:55, 60 seconds after landing; `timeline.json` records `times_had_to_hunt: 2`.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/timeline.json`
  > "'Nothing here yet.' Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup.
  2. Land on `/app/dashboard.html` with no cards.
  3. Observe the empty state offers no action.
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button that opens `/app/new.html`.

### b9b29572f9c4 — One object has four names across nav, list and search
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" would produce the thing "Your cards" was waiting for, and stalled deciding.
- **Framework tags:** A2, A4, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html#nav
- **Personas hit:** novice
- **Observed:**
  - Nav reads "Cards" and "New block"; the list panel is headed "Your cards"; the search placeholder reads "Search your notes"; the editor is headed "New block".
  - Novice paused at the nav at 01:40 asking whether cards and blocks were the same thing.
  - She clicked "New block" without confirmation that it was the right target.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json`
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Open `/app/dashboard.html` and read the nav, the list heading and the search placeholder.
  2. Open "New block" and read its heading.
  3. Observe four labels for one object.
- **Fix:** Pick one noun — "note" — and use it in the nav ("Notes", "New note"), the list heading ("Your notes") and the editor heading.

### 990dc70e5d23 — Irreversible workspace type is chosen before any product exposure and never explained after
- **Severity:** P2
- **So what:** The first screen asks for a permanent decision neither persona could make on evidence, and neither could later confirm what they picked.
- **Framework tags:** A2, A3, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html#workspace-type
- **Personas hit:** novice, power-user
- **Observed:**
  - "Before we begin, choose your workspace type" offers "Federated graph", "Sovereign vault", "Hybrid mesh" with the sole explanation "This cannot be changed later."
  - Novice hesitated 28 seconds (00:20 → 00:48) and picked "Hybrid mesh" on the guess that it included the other two.
  - Settings later shows "Federated graph replication" checked, with no statement that it is the signup choice; the power-user asked and could not tell.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the auth wall and land on `/app/signup.html`.
  2. Read the three options and the "This cannot be changed later." line.
  3. Complete signup, open `/app/settings.html`, and try to identify which setting reflects the choice.
- **Fix:** Add a one-line plain-English description under each option, default to one, move the choice into Settings post-signup, and label it there "Workspace type (chosen at signup)".

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself was never captured — `persona-novice/screenshots/04-note-saved-toast.png` shows the empty "New block" form with no toast and no typed content. The toast rests on `session.log:17` alone.
- "No results for 'Dentist'" and "No results for 'Roadmap'" appear only in the logs; both search screenshots show an empty, unsubmitted search box.
- Whether a second session would show the note (server-side save that the list fails to render) — no persona returned after quitting.
- Whether Export produces anything — both personas praised the button, neither clicked it.

## For other lenses
- `POST /api/notes → 500` and `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load — `bugs`.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, `/` all inert) for a power-user evaluating a team switch — `ux`.
- Settings labels "Enable webhook sync", "Federated graph replication", "Vault attestation" shown to a non-technical first-time user — `content`.
- The marketing promise "remembers everything so you never start from zero" against a product that starts empty — `content`.

## Coverage gaps
- Mobile and tablet never tested — both personas ran desktop-1440x900.
- No persona returned for a second session, so retention past the first abandonment is unmeasured.
- Editing, deleting or opening an existing card never reached — no card ever existed.
- Export, the one control both personas found clear, was never exercised.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — `persona-novice/screenshots/` (8) · `persona-power-user/screenshots/` (4)
