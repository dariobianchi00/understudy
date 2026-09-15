# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A Nielsen's 10 · Layer B Microsoft HAX (Memories surface only) · Layer C activation metrics
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED. Findings rest on personas understudy invented, not researched ones.
- Scoring model: opus · traversal: fixture-hand-authored
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B applied only to `/app/memories.html` ("What Nimbus remembers about you"). No other user-facing AI surface was observed.
- Auth wall at `/app/login.html` excluded per manifest; clock starts after the wall for both personas.

---

## Findings

### 95eb354d0378 — Save shows a green toast but the note never appears in the cards list or in search
- **Severity:** P0
- **So what:** Both personas lost every note they wrote, called the product a liar, and quit — nobody reaches value.
- **Framework tags:** A1, A9, C-ABANDON, C-TTFV, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice saved "Dentist" twice; each time "Saved ✓" appeared, dashboard returned "Nothing here yet.", search "Dentist" returned "No results".
  - Power-user saved "Roadmap" once; same toast, empty list, search "Roadmap" returned nothing; stopped at 03:00.
  - Both debriefs answer "what does it do for you" with nothing; novice gave up at 06:30 with "zero notes saved".
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:19` · `persona-novice/session.log:20` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-power-user/session.log:15` · `persona-novice/timeline.json` objectives[0].gave_up=true · `persona-power-user/timeline.json` objectives[0].gave_up=true
  > "Went back to New block. Wrote it again, saved again, 'Saved ✓' again, dashboard empty again. It is lying to me." — novice
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." — power-user
- **Repro:**
  1. Sign up, pick any workspace type, land on `/app/dashboard.html`.
  2. Click "New block", enter a title and body, click "Save".
  3. Observe green "Saved ✓" toast, then redirect to dashboard showing "Nothing here yet."
  4. Type the title into "Search your notes" — "No results for '<title>'".
- **Fix:** Make Save persist the card and show it at the top of "Your cards" on redirect; if persistence fails, replace "Saved ✓" with an error that names the problem and keeps the draft on screen.

### 140458ac9b31-a — Memories page states three facts about the user that are false for an account with zero notes
- **Severity:** P0
- **So what:** The novice read fabricated facts about herself and immediately doubted every other claim the product made, including "Saved".
- **Framework tags:** A1, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Page "What Nimbus remembers about you" lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer says "Memories are built from your notes and connected accounts." — novice had one unsaved note and no connected accounts.
  - No label marks the items as sample, demo, or placeholder; no source or "why" per item.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:24` · `persona-novice/persona-debrief.md` Q4
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
  > "surface: Memories — I don't trust it."
- **Repro:**
  1. Create a fresh account with no notes and no connected accounts.
  2. Click "Memories" in the top nav.
  3. Observe three specific personal claims presented as remembered facts.
- **Fix:** On `/app/memories.html`, show an empty state ("Nothing remembered yet — write a few notes") until real memories exist; if sample content must stay, label each row "Example" and add a per-item "Why?" source link.
- Why this call: torn between blocker and critical friction; took blocker because the rubric names "confident nonsense about the persona's own data" as one, and the novice's quote links it directly to distrusting Save.

### 140458ac9b31-b — Memories page states three facts about the user that are false for an account with zero notes
- **Severity:** P1
- **So what:** The power-user wrote the panel off as a demo and stopped trusting it — the "remembers everything" promise is dead on arrival for an evaluator.
- **Framework tags:** B-G2, B-G11
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same page as above; power-user spent ~30s, assumed it was a demo panel, and did not return.
  - Debrief Q4: the product "remembers nothing I gave it and claims things I didn't."
- **Evidence:** `persona-novice/screenshots/06-memories.png` (same screen; power-user took no screenshot of it) · `persona-power-user/session.log:14` · `persona-power-user/persona-debrief.md` Q4
  > "Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a fresh account, click "Memories".
  2. Observe three claims about the user with no source and no "example" label.
- **Fix:** Same as 140458ac9b31-a — empty state until real memories exist, or label sample rows "Example" with a source.
- Flip: the novice variant 140458ac9b31-a is a blocker; this one is critical friction. The power-user compartmentalised the distrust; the novice did not.

### 525f82ff64cd-a — Signup forces an irreversible choice between three undefined workspace types before the product is seen
- **Severity:** P1
- **So what:** The novice's first 48 seconds were a guess she was told she could never undo — "this feels risky" before any value is shown.
- **Framework tags:** A2, A3, A5, A6, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Screen "Before we begin, choose your workspace type" offers "Federated graph", "Sovereign vault", "Hybrid mesh" with no description of any option.
  - Below the radios: "This cannot be changed later." No default is pre-selected; no skip.
  - Novice deliberated from 00:05 to 00:48 (43s) and picked "Hybrid mesh" "because it sounds like it includes the other two."
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-novice/findings-raw.json` t=00:20
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Click "Create an account" from `/app/login.html`.
  2. Land on `/app/signup.html`; observe three unexplained radio options and "This cannot be changed later."
- **Fix:** Pre-select a sensible default, add one plain-language line under each option saying what it changes, and either drop "This cannot be changed later." or move the choice into Settings after first value.
- Why this call: torn between critical friction and friction; took the higher because an unexplained irreversible commitment in the first minute is closer to the rubric's "permissions feel invasive without explanation" than to "jargon in copy".

### 525f82ff64cd-b — Signup forces an irreversible choice between three undefined workspace types before the product is seen
- **Severity:** P3
- **So what:** The power-user noticed, shrugged, and picked one in under 30 seconds — no behaviour changed.
- **Framework tags:** A2, A3
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Same screen; chose "Federated graph" without deliberation; reached dashboard by 00:30.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` (same screen; power-user took no screenshot of it) · `persona-power-user/session.log:8` · `persona-power-user/timeline.json` shape_1.end=00:30
  > "Workspace type: Federated graph / Sovereign vault / Hybrid mesh, cannot be changed. Fine — I've seen worse. Picked Federated graph."
- **Repro:**
  1. As above.
- **Fix:** Same as 525f82ff64cd-a.
- Flip: the novice variant 525f82ff64cd-a is critical friction; this one is polish — the product has silently picked a user who already knows these words.

### 1aec13a4fcee — The same object is called cards, blocks and notes across the nav, heading and search box
- **Severity:** P2
- **So what:** The novice could not tell whether "New block" would create one of "Your cards", and hesitated before the only action that leads to value.
- **Framework tags:** A2, A4
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Top nav: "Cards", "New block". Dashboard heading: "Your cards". Search placeholder: "Search your notes". Settings export: "Markdown, all cards".
  - Novice paused at the nav at 01:40 asking whether cards and blocks are the same thing before clicking "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` t=01:40
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing? Clicked 'New block'."
- **Repro:**
  1. Land on `/app/dashboard.html`; read the nav, the section heading and the search placeholder.
- **Fix:** Pick one word (the marketing site says "notes") and use it in the nav item, the create button, the heading, the placeholder and the export label.

### 76a47aadd5a7 — Empty dashboard says Nothing here yet and offers no way to create the first note
- **Severity:** P2
- **So what:** The novice's first screen after signup contradicted the promise she arrived with and gave her nothing to click.
- **Framework tags:** A6, A10, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" section contains only "Nothing here yet." — no button, no link, no hint pointing at "New block" in the nav.
  - Novice spent 00:55 → 01:40 (45s) on the empty dashboard, including a search of an empty workspace, before finding the nav item.
  - timeline.json records times_had_to_hunt=2 during shape_2.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14` · `persona-novice/timeline.json` shape_2.times_had_to_hunt=2
  > "Dashboard. 'Your cards' — 'Nothing here yet.' Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup and land on `/app/dashboard.html` with no notes.
  2. Observe the "Nothing here yet." empty state with no call to action.
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button that opens `/app/new.html`, plus one line saying what appears here once saved.
- Power-user not hit: found the search box in 15s and went straight to "New block" (`persona-power-user/session.log:9`).

### 35d225b6f2d2 — Settings toggles use undefined terms and the default-on one is not linked to the signup choice
- **Severity:** P2
- **So what:** Neither persona could tell what any toggle does; the power-user could not tell whether "Federated graph replication" is the thing he chose at signup.
- **Framework tags:** A2, A4, A6
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Three checkboxes: "Enable webhook sync" (off), "Federated graph replication" (on), "Vault attestation" (off). No help text on any.
  - "Federated graph replication" is checked by default for the power-user who chose "Federated graph" at signup; nothing says they are related.
  - Both personas identified "Export — Markdown, all cards" as the only clear control on the page.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json` t=02:00
  > "'Enable webhook sync', 'Federated graph replication', 'Vault attestation'. No idea. There's an Export button — 'Markdown, all cards'. At least that's clear." — novice
  > "'Federated graph replication' is on by default. I picked that at signup — is this the same thing?" — power-user
- **Repro:**
  1. Click "Settings" in the top nav.
  2. Observe three unlabelled-purpose checkboxes and no help text.
- **Fix:** Add one plain-language line under each toggle saying what it does and when to turn it on; show the workspace type chosen at signup on this page so the replication toggle has context.
- Note: a caveat only — the novice checkbox states were captured on a "Hybrid mesh" workspace and match the power-user's "Federated graph" workspace exactly, so the default may not follow the signup choice at all. Not scored; no way to separate from evidence.

### bbaccd27db34 — No keyboard shortcut opens search or a new note
- **Severity:** P2
- **So what:** The power-user's stated reason for evaluating — "fast capture, good search, keyboard-driven" — has no keyboard path at all.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - On the dashboard, Ctrl+K, Ctrl+N and "/" produced no response.
  - No shortcut hint is shown in the search placeholder or nav.
- **Evidence:** `persona-power-user/screenshots/02-dashboard.png` · `persona-power-user/session.log:3` · `persona-power-user/session.log:12` · `persona-power-user/findings-raw.json` t=01:30
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. On `/app/dashboard.html`, press Ctrl+K, then Ctrl+N, then "/".
  2. Observe no focus change and no new-note screen.
- **Fix:** Bind "/" or Ctrl+K to focus "Search your notes" and Ctrl+N to open `/app/new.html`; show the shortcut inside the search placeholder.
- Novice not hit: never attempted a shortcut.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- Search may be broken independently of Save — no note ever persisted, so a working search returning nothing cannot be separated from a broken one.
- The "Saved ✓" toast may disappear too fast to read — `04-note-saved-toast.png` was captured after it dismissed and shows only the empty form; no timing captured.
- Save redirecting to the dashboard instead of staying on the note may be its own A3 issue — neither persona commented on the redirect itself.
- Settings defaults may not follow the signup choice (novice "Hybrid mesh" and power-user "Federated graph" show identical checkbox states) — no persona probed it.

## For other lenses
- "Saved ✓" with no persisted record — probably a failed or missing write; console/network at `persona-*/network-full.txt` — `bugs`.
- Marketing promise "remembers everything so you never start from zero" vs. an empty workspace and fabricated memories; both debriefs Q4 fail promise match — `content`.
- "Federated graph", "Sovereign vault", "Hybrid mesh", "Vault attestation", "webhook sync" — jargon density — `content`.
- Novice hunt count 2, TTFV 2:41 to a preview that was then lost; power-user first value never reached — `onboarding`.
- Radio buttons and checkboxes render detached from their labels (control centred, label left-aligned below) on `/app/signup.html` and `/app/settings.html` — accessibility; no lens covers it yet.

## Coverage gaps
- "Cards" nav item never clicked by either persona — unknown whether it differs from the dashboard.
- "Export — Markdown, all cards" never clicked — unknown whether it works or what it exports when empty.
- No "connected accounts" flow was found or attempted; the Memories footer implies one exists.
- No screenshot shows the "Saved ✓" toast itself; evidence for it is session-log only (`persona-novice/session.log:17`, `persona-power-user/session.log:11`).
- Power-user took no screenshots of signup or Memories; novice screenshots of the same screens are cited for those variants.
- Desktop 1440×900 only; no mobile device tested.
- Neither persona logged back in to test whether notes survive a session; no auth-cleared second visit.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index:
  - `persona-novice/screenshots/00-start.png` — login wall (excluded)
  - `persona-novice/screenshots/00-wall-cleared.png` — signup workspace-type screen at clock start
  - `persona-novice/screenshots/01-signup-workspace-type.png` — workspace-type radios, "This cannot be changed later."
  - `persona-novice/screenshots/02-dashboard-empty.png` — search box + "Your cards" / "Nothing here yet."
  - `persona-novice/screenshots/03-new-note.png` — "New block" form: Title, Body, "0 words", "Preview below", Save
  - `persona-novice/screenshots/04-note-saved-toast.png` — "New block" form, empty; toast not visible
  - `persona-novice/screenshots/05-notes-list-missing.png` — dashboard after save, still "Nothing here yet."
  - `persona-novice/screenshots/06-memories.png` — "What Nimbus remembers about you", three claims
  - `persona-novice/screenshots/07-settings.png` — three checkboxes + Export
  - `persona-power-user/screenshots/00-start.png` — login wall (excluded)
  - `persona-power-user/screenshots/02-dashboard.png` — empty dashboard
  - `persona-power-user/screenshots/03-search-empty.png` — dashboard after searching "Roadmap"; list empty, search box shows placeholder
  - `persona-power-user/screenshots/07-settings.png` — identical to novice settings
