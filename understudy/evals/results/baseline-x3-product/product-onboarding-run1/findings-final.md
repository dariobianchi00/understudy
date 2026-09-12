# Nimbus Notes — onboarding findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer C activation (C-TTFV, C-STEPS, C-ABANDON, C-SOWHAT) + first-value definition; funnel built from `timeline.json` per persona
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — INFERRED
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Funnel

| Stage | novice | power-user |
|---|---|---|
| Reached entry point (signup, post-wall) | ✓ 00:00 | ✓ 00:00 |
| Workspace type chosen | ✓ 00:48 | ✓ <00:30 |
| Dashboard reached | ✓ 00:55 | ✓ 00:30 |
| Found "New block" | ✓ 01:40 | ✓ 01:00 |
| Note composed | ✓ 01:55–03:05 | ✓ 01:00 |
| Note persisted (visible in "Your cards") | ✗ 03:12 | ✗ 01:00 |
| Note found via search | ✗ 03:30 | ✗ 01:00 |
| **First value reached** | ⚠ 02:41 (live preview; retracted at debrief) | ✗ |
| Returned to a second task | ✗ | ✗ |
| Abandoned (not timed out) | 06:30 | 03:00 |

**Steps to value (product-required):** 5 · **Time to value:** novice 02:41 marginal / power-user not reached · **Drop-off:** Save on `/app/new.html` → empty `/app/dashboard.html`, both personas

- `timeline.json` novice: `seconds_to_first_value: 161`, `steps_to_first_value: 5`, `times_had_to_hunt: 2`, `permission_prompts: 0`, objective `gave_up: true`.
- `timeline.json` power-user: `first_value_reached: false`, `times_had_to_hunt: 1`, `permission_prompts: 0`, objective `gave_up: true`.
- Both abandonments are voluntary; the 90-minute cap was never approached.

---

## Findings

> **⚑ This block is machine-parsed.** `check_report.py` reads it field by field
> and fails closed — a field it cannot find is treated as absent, and an absent
> `Flow` silently changes the finding's ID. **Keep every field on its own
> bullet; never merge them onto one line with `·` separators.** A `·` inside a
> field's value is fine and expected (several artifacts on one Evidence line);
> it is only the field bullets themselves that must stay separate.
>
> **The `<finding-id>` is computed, never composed** — see the lens agent's
> Output section for the `finding_id.py` invocation. Write the block first, then
> hash exactly the `flow`, `locator` and `title` strings you wrote.

### bb5a95b34cd3 — "Saved ✓" confirms a note the server rejected with 500 — every note written is lost and unfindable
- **Severity:** P0
- **So what:** Both personas abandoned here with zero notes persisted; the product's only value-producing step fails while claiming success.
- **Framework tags:** C-ABANDON, C-TTFV, A1, A9
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Save on "New block" fires `POST /api/notes → 500`; the UI still shows a green "Saved ✓" toast and returns to the dashboard.
  - Dashboard "Your cards" stays "Nothing here yet." after the save; search for the note's own title returns "No results".
  - Novice retried the identical save at 03:50 and got the same 500 and the same toast — 2 of 2 saves lost.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:20` · `persona-power-user/session.log:11` · `persona-novice/network-full.txt` `[POST] http://localhost:8765/api/notes → 500 internal error (03:05)` · `persona-power-user/network-full.txt` `[POST] http://localhost:8765/api/notes → 500 internal error (01:00)` · `persona-novice/console-full.txt` `[error] new.html:1 POST http://localhost:8765/api/notes 500 (Internal Server Error)`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work."
- **Repro:**
  1. Clear the login wall; choose any workspace type; land on `/app/dashboard.html`.
  2. Click "New block"; enter title "Dentist" and a body line; click "Save".
  3. Observe the "Saved ✓" toast and the redirect to the dashboard; observe "Your cards" still reads "Nothing here yet."
  4. Type "Dentist" in "Search your notes"; observe "No results for 'Dentist'".
- **Fix:** Make `POST /api/notes` return 2xx and persist the note; on the New block form, show the "Saved ✓" toast only on a 2xx and an inline "Couldn't save — try again" on any error.

### 0beb959d74b4-a — "What Nimbus remembers about you" lists three facts the persona never gave it — trust in "Saved" collapses
- **Severity:** P1
- **So what:** After one dentist note, the novice reads fabricated claims about herself and concludes the product may be lying about everything, including saves.
- **Framework tags:** C-ABANDON, C-SOWHAT, A1
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Memories page shows "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer reads "Memories are built from your notes and connected accounts." — the persona has zero persisted notes and no connected accounts.
  - Persona ties the fabricated memories directly to distrust of the save toast and stops at 06:30.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:24` · `persona-novice/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
  > "No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine."
- **Repro:**
  1. Sign up as a fresh workspace with no notes persisted.
  2. Click "Memories" in the top nav.
  3. Observe three pre-filled statements about the user that no note or account produced.
- **Fix:** On `/app/memories.html`, show an honest empty state ("Nothing remembered yet — write a few notes and Nimbus will start here") until at least one persisted note exists; never seed placeholder facts.

### 0beb959d74b4-b — "What Nimbus remembers about you" lists three facts the persona never gave it — trust in "Saved" collapses
- **Severity:** P2
- **So what:** The power-user dismisses the panel as demo content but explicitly refuses to trust it — a feature the pitch leads with is written off on sight.
- **Framework tags:** C-SOWHAT, A1
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three fabricated memories shown to a workspace with zero persisted notes.
  - Persona assumes it is a demo panel and moves on; names it as "claims things I didn't" in the debrief.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` · `persona-power-user/network-full.txt` `[GET] http://localhost:8765/app/memories.html → 200`
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > ""Remembers everything." No. It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Sign up as a fresh workspace with no notes persisted.
  2. Click "Memories" in the top nav.
  3. Observe three pre-filled statements unrelated to anything the user entered.
- **Fix:** Same as `0beb959d74b4-a`; if demo content must stay, label it "Example — not yet built from your notes".

### fd024b4b3a47-a — Irreversible "workspace type" choice between three unexplained terms gates the product before the first screen
- **Severity:** P2
- **So what:** The novice's first 48 s go to an undoable decision she cannot understand, before the product has shown her anything — the wrong first impression for a "never start from zero" pitch.
- **Framework tags:** C-STEPS, C-ABANDON, A2, B-G11
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Screen reads "Before we begin, choose your workspace type" with radios "Federated graph", "Sovereign vault", "Hybrid mesh" and the note "This cannot be changed later."
  - No description, default or "skip" for any option; persona picked "Hybrid mesh" on a guess at 00:48.
  - Persona spent 00:05–00:48 on the screen (43 s of a 55 s shape 1).
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-novice/findings-raw.json`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; land on `/app/signup.html`.
  2. Observe the three unlabelled workspace-type radios and "This cannot be changed later."
- **Fix:** Remove the gate from signup — default every new workspace and move the choice to Settings with a one-line description per option; if it must stay, pre-select a default and add "Most people choose this".

### fd024b4b3a47-b — Irreversible "workspace type" choice between three unexplained terms gates the product before the first screen
- **Severity:** P3
- **So what:** The power-user tolerates it in under 30 s but later cannot tell whether "Federated graph replication" in Settings is the thing he chose — a loose thread, not a blocker.
- **Framework tags:** C-STEPS, A4
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Persona picked "Federated graph" without hesitation; shape 1 completed in 00:30.
  - At 02:00 the Settings toggle "Federated graph replication" is on by default and the persona asks whether it is the same setting.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:8` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json`
  > "Workspace type: Federated graph / Sovereign vault / Hybrid mesh, cannot be changed. Fine — I've seen worse. Picked Federated graph."
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. At signup choose "Federated graph"; open "Settings".
  2. Observe "Federated graph replication" checked with no reference to the signup choice.
- **Fix:** In Settings, caption the replication toggle "Set by your workspace type (Federated graph)" or drop the signup gate entirely per `fd024b4b3a47-a`.

### a829a497d844 — Empty dashboard says "Nothing here yet." with no call to action — the first note is a hunt, not a step
- **Severity:** P2
- **So what:** The novice's first 45 s on the product screen are spent guessing what to click; the product she was promised would be pre-filled instead offers nothing.
- **Framework tags:** C-STEPS, C-TTFV, A6, B-G1
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard shows a "Search your notes" box and "Your cards — Nothing here yet."; no button, link or hint to create anything.
  - Persona tried search first (01:20, "No results for 'meeting'"), then guessed "New block" from the nav at 01:40.
  - `timeline.json` records `times_had_to_hunt: 2` for the novice; this is the first of the two.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14` · `persona-novice/timeline.json`
  > "Dashboard. "Your cards" — "Nothing here yet." Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup; land on `/app/dashboard.html` with no notes.
  2. Observe the empty "Your cards" panel offers no action.
- **Fix:** Replace "Nothing here yet." with a primary button "Write your first note" linking to `/app/new.html`, plus one line on what a note does for the user once saved.

### 9f9635d9e560 — The same object is called "cards", "block" and "notes" across the nav, form and search — the persona cannot tell what to create
- **Severity:** P2
- **So what:** A novice looking for "notes" (the product name and the search placeholder) has to guess that "New block" makes a "card" — a vocabulary hunt inside the critical path.
- **Framework tags:** C-STEPS, A2, A4
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Top nav reads "Cards" and "New block"; the search placeholder reads "Search your notes"; the list header reads "Your cards"; Export reads "Markdown, all cards".
  - Persona paused on the nav at 01:40 asking whether cards and blocks are the same thing before clicking "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing? Clicked "New block"."
- **Repro:**
  1. Land on `/app/dashboard.html`; read the nav, the search placeholder and the list header.
  2. Click "New block"; observe the form heading "New block" for an item listed under "Your cards".
- **Fix:** Pick one noun — "note" — and use it in the nav ("Notes", "New note"), the form heading, the list header and Export.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself was never captured on screen — `persona-novice/screenshots/04-note-saved-toast.png` shows an empty form with no toast; the P0 rests on log and network lines instead.
- Whether the power-user's dashboard at 00:30 was identical to the novice's — `persona-power-user/screenshots/02-dashboard.png` was opened and matches, but no log line records the persona's read of it beyond "Search box — good".

## For other lenses
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) on the dashboard — `persona-power-user/session.log:12` — ux.
- Settings toggles "Enable webhook sync", "Federated graph replication", "Vault attestation" have no explanation — `persona-novice/session.log:23` — content, ux.
- `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load, both personas — `persona-novice/console-full.txt` — bugs.
- `POST /api/notes → 500` on every save — `persona-novice/network-full.txt`, `persona-power-user/network-full.txt` — bugs (root cause of the P0 here).
- Marketing promise "remembers everything so you never start from zero" vs empty first screen and fabricated memories — both debriefs Q4 — content.

## Coverage gaps
- "Cards" nav item never clicked as its own surface by either persona.
- No populated dashboard state was ever observed — every list view in the run is empty.
- Export button seen by both personas, clicked by neither.
- Desktop 1440×900 only; no mobile device in this run.
- Single session per persona; the "returned to a second task" stage could only be inferred from in-session retries.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index — novice: `00-start`, `00-wall-cleared`, `01-signup-workspace-type`, `02-dashboard-empty`, `03-new-note`, `04-note-saved-toast`, `05-notes-list-missing`, `06-memories`, `07-settings` · power-user: `00-start`, `02-dashboard`, `03-search-empty`, `07-settings`
