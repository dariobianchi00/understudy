# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) · Layer B (HAX — applied to the Memories surface only) · Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user; both desktop 1440×900)
- Scoring model: opus · traversal: fixture-hand-authored
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B: the product has one user-facing inference surface (`Memories` — "What Nimbus remembers about you"). B tags apply there and nowhere else.
- Scope exclusion applied: the login wall at `/app/login.html` is never scored. Both clocks start after it.

---

## Findings

### 86ec1eb6f867 — "Saved ✓" confirms a save that never happened; the note never appears in Cards or search
- **Severity:** P0
- **So what:** Both personas lost every note they wrote, were told it was saved, and quit within 7 minutes calling the product a liar.
- **Framework tags:** A1, A9, C-ABANDON, C-TTFV
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Novice: Save → green "Saved ✓" toast → redirect to dashboard → "Your cards" still "Nothing here yet."; search "Dentist" → "No results for 'Dentist'". Repeated once, same result (03:05–03:50).
  - Power-user: title "Roadmap", Save, "Saved ✓", dashboard empty, search "Roadmap" → no results (01:00). Gave up at 03:00.
  - No error, no retry, no "nothing saved" state is ever shown; the success toast is the only feedback.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-power-user/screenshots/03-search-empty.png` · `persona-power-user/session.log:11` · `persona-novice/network-full.txt:5` (POST /api/notes → 500 at 03:05, cited only as corroboration; the defect itself is the bugs lens's) · `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me." — novice
  > "Enough. Save doesn't save and search doesn't search. Nothing else matters until those work." — power-user
- **Repro:**
  1. Clear the login wall; land on `/app/dashboard.html`.
  2. Click "New block"; enter a title and body; click "Save".
  3. Observe the "Saved ✓" toast, then the redirect to an empty "Your cards" list.
  4. Search the title in "Search your notes"; observe "No results".
- **Fix:** On `/app/new.html`, show "Saved ✓" only after the server confirms the write; on failure keep the form filled and show "Couldn't save — try again" with a retry button.

### 9a8bce9cc28e-a — Memories page states three facts about the user that are not true
- **Severity:** P0
- **So what:** The novice read fabricated claims about themself and immediately doubted every other message the product had shown — including "Saved".
- **Framework tags:** B-G2, B-G11, A1, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - Under "What Nimbus remembers about you": "You prefer to schedule meetings on Tuesday afternoons." / "Your team uses Jira and Slack." / "You are working on a product launch in Q4."
  - Footer says "Memories are built from your notes and connected accounts." — the persona had written one note about a dentist and connected nothing.
  - No source, date, confidence, or "delete this memory" control on any item.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/persona-debrief.md`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
  > "it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine." — debrief Q4
- **Repro:**
  1. Create a fresh workspace; write at most one note.
  2. Click "Memories" in the top nav.
  3. Observe three pre-populated statements unrelated to anything entered.
- **Fix:** On `/app/memories.html`, remove the placeholder memories for new workspaces, show an honest empty state ("Nothing remembered yet — memories build from your notes"), and put a source + "Forget this" control on every real memory.
- Torn between P0 and P1: taken as P0 because the rubric names "confident nonsense about the persona's own data" as a blocker and the novice's own words tie it to distrust of the save.

### 9a8bce9cc28e-b — Memories page states three facts about the user that are not true
- **Severity:** P1
- **So what:** The power-user wrote the surface off as a demo panel — the headline "remembers everything" feature is now something they have decided never to trust.
- **Framework tags:** B-G2, B-G11, A1
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three statements as above, seen at 02:30 after one note ("Roadmap").
  - Persona assumed it was seeded demo content, not an inference about them.
- **Evidence:** `persona-novice/screenshots/06-memories.png` (same screen; the power-user capture has no Memories screenshot) · `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` · `persona-power-user/persona-debrief.md`
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
  > "It remembers nothing I gave it and claims things I didn't." — debrief Q4
- **Repro:**
  1. Create a fresh workspace; write one note.
  2. Click "Memories".
  3. Observe three statements unrelated to the note.
- **Fix:** Same as `9a8bce9cc28e-a`; if seeded examples must stay, label each one "Example" and add a one-click "Clear examples".

### f1eb36263701 — Signup demands an irreversible choice between three undefined workspace types before showing the product
- **Severity:** P1
- **So what:** The novice's very first screen after the wall is an unexplained one-way decision; they stalled 43 seconds and picked by guessing.
- **Framework tags:** A2, A3, A5, A6, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Screen "Before we begin, choose your workspace type": radio options "Federated graph", "Sovereign vault", "Hybrid mesh"; caption "This cannot be changed later."; one button "Create workspace".
  - No description under any option, no default, no "skip", no link to what each means.
  - Novice picked "Hybrid mesh" at 00:48 "because it sounds like it includes the other two".
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-novice/findings-raw.json`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; arrive at `/app/signup.html`.
  2. Observe the three radio labels with no explanation and the caption "This cannot be changed later."
- **Fix:** On `/app/signup.html`, pre-select a sensible default, add one plain-language line under each option, and either drop "This cannot be changed later." or move the choice into Settings after first value.
- Severity flip: the power-user shrugged ("Fine — I've seen worse", `persona-power-user/session.log:8`) and chose in under 30 s — a non-issue for them, so no variant is scored.

### 1017bc386765 — Nav, heading and search call the same object "block", "cards" and "notes"
- **Severity:** P2
- **So what:** The novice had to ask whether "Cards" and "New block" were the same thing before finding where to write; the vocabulary is the first hunt.
- **Framework tags:** A4, A2, A6
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Top nav: "Cards", "New block". Dashboard heading: "Your cards". Search placeholder: "Search your notes". Settings export: "Markdown, all cards".
  - Novice paused at 01:40 on the nav before clicking "New block".
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Land on `/app/dashboard.html`.
  2. Read the nav, the list heading and the search placeholder together.
- **Fix:** Pick one noun (the product name says "Notes") and use it in the nav, the list heading, the search placeholder, the "New" button and the export label.

### 7990feefb7ac — Empty dashboard says "Nothing here yet." with no route to creating a first note
- **Severity:** P2
- **So what:** The novice arrived expecting the product to have their stuff, found an empty box, and spent 45 s searching an empty workspace before finding "New block".
- **Framework tags:** A1, A6, C-TTFV, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel contains only the text "Nothing here yet." — no button, no link, no hint.
  - Novice typed "meeting" into search at 01:20 and got "No results for 'meeting'" before trying the nav.
  - Timeline: `times_had_to_hunt: 2`, 5 steps and 2:41 to the first thing the product did for them.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/timeline.json`
  > "Dashboard. "Your cards" — "Nothing here yet." Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Create a fresh workspace.
  2. Observe the "Your cards" empty state on `/app/dashboard.html`.
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button and one line saying what happens after.

### 967e2da00185 — No keyboard shortcuts: Ctrl+K, Ctrl+N and / do nothing
- **Severity:** P2
- **So what:** The power-user's stated reason to switch was "fast capture, keyboard-driven"; every shortcut they tried was dead.
- **Framework tags:** A7
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - At 01:30 the persona pressed Ctrl+K, Ctrl+N and `/` on the dashboard; nothing happened.
  - No shortcut hint appears anywhere on the dashboard, the editor or Settings.
- **Evidence:** `persona-power-user/screenshots/02-dashboard.png` · `persona-power-user/session.log:12` · `persona-power-user/findings-raw.json`
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Focus `/app/dashboard.html`.
  2. Press Ctrl+K, Ctrl+N, then `/`.
- **Fix:** Bind `/` or Ctrl+K to focus "Search your notes" and Ctrl+N to "New block"; show the keys as hints inside the search placeholder and on the nav item.

### 7d60af3190ea — Settings toggles use unexplained jargon: "Enable webhook sync", "Federated graph replication", "Vault attestation"
- **Severity:** P2
- **So what:** The novice could not tell what any of the three toggles would do to their notes, so the only control they trusted was Export.
- **Framework tags:** A2, A10
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice
- **Observed:**
  - Three checkboxes labelled "Enable webhook sync", "Federated graph replication" (checked), "Vault attestation"; no helper text, no link, no tooltip.
  - The one control with a plain label — "Export" · "Markdown, all cards" — was the only one the persona understood.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24`
  > "Enable webhook sync", "Federated graph replication", "Vault attestation". No idea. There's an Export button — "Markdown, all cards". At least that's clear.
- **Repro:**
  1. Click "Settings" in the top nav.
  2. Read the three toggle labels.
- **Fix:** Under each toggle on `/app/settings.html`, add one sentence in the user's terms saying what it does and what changes if turned on; move developer-only toggles behind an "Advanced" section.

### c5d8e631e72c — Settings shows "Federated graph replication" pre-checked with no link to the "Federated graph" chosen at signup
- **Severity:** P2
- **So what:** The power-user could not tell whether this toggle was the irreversible signup choice again — and therefore whether unticking it was safe.
- **Framework tags:** A4, A5
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - Signup offered "Federated graph" with "This cannot be changed later."; Settings shows a checkbox "Federated graph replication", on by default, with no reference to the workspace type.
  - The same two words appear on two screens with different affordances (locked radio vs. editable checkbox).
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json`
  > ""Federated graph replication" is on by default. I picked that at signup — is this the same thing?"
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. At signup choose "Federated graph".
  2. Open "Settings"; observe "Federated graph replication" checked.
- **Fix:** On `/app/settings.html`, show the chosen workspace type as a read-only line ("Workspace type: Federated graph") and rename or explain the replication toggle so it cannot be read as the same setting.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself was never captured — `persona-novice/screenshots/04-note-saved-toast.png` shows the blank "New block" form, not a toast. The P0 rests on both session logs, the dashboard/search screenshots and the debriefs; the toast's exact rendering is unverified.
- Post-save redirect discards the typed content with no "your draft was lost" state — implied by the novice re-typing the note (`session.log:20`), but no screenshot of the editor after the failed save exists.
- The "Cards" nav item may be identical to the dashboard — neither persona clicked it, so no artifact.

## For other lenses
- `POST /api/notes → 500` on every save, and `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load (`persona-novice/console-full.txt`, `network-full.txt`) — `bugs`.
- Marketing promise "remembers everything so you never start from zero" vs. a workspace that starts empty and loses notes — `content` (promise match).
- Funnel: both personas abandoned at the first save (novice 03:50, power-user 01:30); 0 of 2 reached the objective — `onboarding`.
- Jargon density of the workspace-type and Settings labels — `content`.
- Accessibility (radio/checkbox controls visually detached from their labels on `/app/signup.html` and `/app/settings.html`) — no lens covers WCAG in this run; noted, not scored.

## Coverage gaps
- "Cards" nav item never opened by either persona.
- Export button never clicked; export output never seen.
- No mobile device; both personas on desktop 1440×900.
- No screenshot of the Memories page from the power-user capture; the novice's screenshot is cited for both variants.
- No screenshot of the toast state or of the editor after a failed save.
- Login wall excluded by manifest; nothing scored before "Clock starts".

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index
  - `persona-novice/screenshots/00-start.png` — login wall (excluded)
  - `persona-novice/screenshots/00-wall-cleared.png` — workspace-type screen at clock start
  - `persona-novice/screenshots/01-signup-workspace-type.png` — workspace-type screen
  - `persona-novice/screenshots/02-dashboard-empty.png` — empty dashboard
  - `persona-novice/screenshots/03-new-note.png` — "New block" editor, empty
  - `persona-novice/screenshots/04-note-saved-toast.png` — "New block" editor, empty (no toast visible)
  - `persona-novice/screenshots/05-notes-list-missing.png` — dashboard after save, still empty
  - `persona-novice/screenshots/06-memories.png` — Memories page with three seeded statements
  - `persona-novice/screenshots/07-settings.png` — Settings page
  - `persona-power-user/screenshots/00-start.png` — login wall (excluded)
  - `persona-power-user/screenshots/02-dashboard.png` — empty dashboard
  - `persona-power-user/screenshots/03-search-empty.png` — dashboard after searching "Roadmap", empty
  - `persona-power-user/screenshots/07-settings.png` — Settings page
