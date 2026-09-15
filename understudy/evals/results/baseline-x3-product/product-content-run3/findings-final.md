# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery (first-value Q4) + Nielsen A2/A4/A9 for copy, reading level, jargon density, error and empty-state copy
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED (novice, power-user; both desktop 1440×900)
- Scoring model: opus (traversal: fixture-hand-authored)
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B (HAX): applied only to the Memories panel — the one surface that presents inferred content

---

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" — "a notes app that fills itself in from things I already have" | Empty workspace; note "Saved ✓" twice, never listed, never searchable; Memories panel with 3 facts not hers | **Fail** | Quit at 06:30 with 0 notes; "I'd stop here" (`persona-novice/session.log:25`) |
| power-user | "remembers everything so you never start from zero" — "fast capture, good search, keyboard-driven" | Note saved then lost; search returns nothing; no shortcuts; Memories not his | **Fail** | Quit at 03:00; "Nothing else matters until those work" (`persona-power-user/session.log:15`) |

- Persona Q4 answers: novice **No**, power-user **No**. Analyst reading agrees with both — no disagreement to reconcile.
- Root cause for the report: the product's own words ("Saved ✓", "What Nimbus remembers about you") assert states that are false. Every downstream finding is cheaper to fix than to explain.

## Jargon inventory (terms the persona met, undefined anywhere in the session)

| Term | Screen | Defined? | Novice reaction |
|---|---|---|---|
| "Federated graph" | signup, settings | No | "I don't know what any of these are" |
| "Sovereign vault" | signup | No | same |
| "Hybrid mesh" | signup | No | picked it "because it sounds like it includes the other two" |
| "Enable webhook sync" | settings | No | "No idea" |
| "Federated graph replication" | settings | No | "No idea"; power-user: "Same words, no link" |
| "Vault attestation" | settings | No | "No idea" |
| "block" / "cards" / "notes" | nav, dashboard, search | No | "Cards and blocks — same thing?" |

- 7 undefined terms across 4 screens; 6 are infrastructure vocabulary with no user-facing meaning.
- Reading level: sentences are short (≤ 8 words); the barrier is vocabulary, not syntax. Copy volume is tiny — ~60 words of UI text total — so every word carries weight.

---

## Findings

> **⚑ This block is machine-parsed.** Every field on its own bullet. IDs computed with `finding_id.py`.

### 9a7556c2e72e — "Saved ✓" confirms a save the product did not perform
- **Severity:** P0
- **So what:** Both personas stopped believing anything the product said after the second "Saved ✓" with an empty list — trust gone in under 4 minutes.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Toast reads "Saved ✓" after Save; dashboard then shows "Your cards — Nothing here yet."; search for the exact title returns "No results".
  - Novice repeated the write twice with the same result; power-user once.
  - No on-screen text explains where a saved item goes or why the list is empty.
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:18` · `persona-novice/session.log:20` · `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/session.log:11` · `persona-power-user/screenshots/03-search-empty.png`
  > "Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
  > "Nothing yet — it accepts a note and then loses it."
- **Repro:**
  1. Sign up, pick any workspace type, land on dashboard.
  2. Click "New block", enter title "Dentist" and a body, click Save.
  3. Observe "Saved ✓" toast, then dashboard "Nothing here yet."; search "Dentist" → "No results for 'Dentist'."
- **Fix:** Make the "Saved ✓" confirmation conditional on the card actually being persisted and listed; until the save path works, the toast must not fire. Route the underlying save/list defect to engineering.

### 3216812aca8c — Product contradicts its pitch: "remembers everything" delivers an empty workspace and lost notes
- **Severity:** P1
- **So what:** The one line that brought both personas here is the one thing the product visibly fails at; both answered Q4 "No" and would pay nothing.
- **Framework tags:** A2, C-SOWHAT, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Pre-session promise for both: "remembers everything so you never start from zero".
  - First screen after signup is "Your cards — Nothing here yet." — the persona starts from zero.
  - Nothing in the app names what "remembers" means, where remembered content comes from, or how to feed it.
- **Evidence:** `persona-novice/session.log:2` · `persona-novice/session.log:12` · `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/persona-debrief.md` · `persona-power-user/session.log:2` · `persona-power-user/persona-debrief.md`
  > "I arrived with "remembers everything so you never start from zero". No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine."
  > ""Remembers everything." No. It remembers nothing I gave it and claims things I didn't."
- **Repro:**
  1. Read the marketing line "Nimbus remembers everything so you never start from zero".
  2. Sign up and land on the dashboard.
  3. Compare: empty list, no import, no connected-account prompt, no explanation of what will be remembered.
- **Fix:** Either the dashboard's first state must show what Nimbus already remembers (import, connect, or a worked sample clearly labelled as sample), or the marketing line must change to what the product does today.

### 74a5133b7427-a — "What Nimbus remembers about you" lists facts that are not the user's
- **Severity:** P0
- **So what:** She now doubts every confirmation in the product — "if it's making these up, is it making up the 'Saved' too?" — which is the rubric's definition of trust broken irreparably.
- **Framework tags:** A2, B-G1, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** screen:memories
- **Personas hit:** novice
- **Observed:**
  - Panel heading "What Nimbus remembers about you" followed by "You prefer to schedule meetings on Tuesday afternoons." / "Your team uses Jira and Slack." / "You are working on a product launch in Q4."
  - Footer states "Memories are built from your notes and connected accounts." — she has one note about a dentist and no connected accounts.
  - No label marks the content as sample, demo, or placeholder.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/session.log:24`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Sign up as a new user, write one note about a dentist.
  2. Click "Memories" in the top nav.
  3. Read three second-person statements about meetings, Jira/Slack and a Q4 launch.
- **Fix:** Show an honest empty state on Memories for a new account ("Nothing remembered yet — memories appear as you write"), and if sample content stays, label every row "Example".

### 74a5133b7427-b — "What Nimbus remembers about you" lists facts that are not the user's
- **Severity:** P1
- **So what:** He rationalised it as a demo panel but explicitly refuses to trust the feature that carries the product's whole pitch.
- **Framework tags:** A2, B-G1, B-G2, C-ABANDON
- **Flow:** shape_2b
- **Locator:** screen:memories
- **Personas hit:** power-user
- **Observed:**
  - Same three statements shown to a second fresh account with a different workspace type and a different note ("Roadmap").
  - Content is identical across both personas — it is static, not derived from the user's data as the footer claims.
- **Evidence:** `persona-power-user/session.log:14` · `persona-novice/screenshots/06-memories.png` · `persona-power-user/persona-debrief.md`
  > "Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Sign up as a second fresh user, pick "Federated graph", write a note titled "Roadmap".
  2. Open "Memories"; observe the identical three statements.
- **Fix:** Same as -a; additionally remove or rewrite the footer "Memories are built from your notes and connected accounts." until it is true.

### 46c2bac6d1d6-a — Irreversible "workspace type" choice uses three undefined terms before the product is seen
- **Severity:** P1
- **So what:** Her first decision in the product was a guess she was told she cannot undo — 48 seconds of anxiety before seeing a single feature.
- **Framework tags:** A2, A3, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Heading "Before we begin, choose your workspace type"; options "Federated graph", "Sovereign vault", "Hybrid mesh"; footnote "This cannot be changed later."
  - No description, tooltip, default, or "not sure?" path on any option.
  - She chose "Hybrid mesh" on the sound of the word alone.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9` · `persona-novice/session.log:10` · `persona-novice/session.log:11`
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Clear the login wall; land on /app/signup.html.
  2. Read the three radio labels and the footnote.
- **Fix:** Add a one-line plain-language consequence under each option and a recommended default, or move this choice out of signup entirely.

### 46c2bac6d1d6-b — Irreversible "workspace type" choice uses three undefined terms before the product is seen
- **Severity:** P3
- **So what:** He tolerated it ("Fine — I've seen worse") but the same words later resurfaced in Settings without a link back, so the choice never became meaningful.
- **Framework tags:** A2, A4
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** power-user
- **Observed:**
  - Picked "Federated graph" without comment at 00:00.
  - At 02:00 found "Federated graph replication" pre-checked in Settings and could not tell if it was the same thing.
- **Evidence:** `persona-power-user/session.log:8` · `persona-power-user/session.log:13` · `persona-power-user/screenshots/07-settings.png`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Pick "Federated graph" at signup.
  2. Open Settings; observe "Federated graph replication" checked with no reference to the signup choice.
- **Fix:** In Settings, show the chosen workspace type by name and state which toggles it controls.

### 07d8d3a2fc56 — One object is called "notes", "cards" and "block" on the same screen
- **Severity:** P2
- **So what:** She could not tell whether "New block" was the way to make a "card" that "Search your notes" would find — three words for the first thing she needed to do.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - Dashboard: search placeholder "Search your notes"; list heading "Your cards"; nav item "Cards"; nav item "New block"; form heading "New block".
  - Settings: "Export — Markdown, all cards".
  - The marketing name is "Nimbus Notes"; the word "note" appears only in the search placeholder.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing?"
- **Repro:**
  1. Land on the dashboard; read the search placeholder, list heading and nav.
  2. Click "New block"; read the form heading.
- **Fix:** Pick one noun for the user's unit of writing and use it in nav, list heading, search placeholder, form heading and export label.

### 875ef9b8073e — Empty state "Nothing here yet." gives no way to fill it
- **Severity:** P2
- **So what:** The first screen after signup told her nothing about what to do; she searched an empty workspace before finding the create path at 01:40.
- **Framework tags:** A6, A10, C-STEPS
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - "Your cards" panel shows only "Nothing here yet." — no button, link, or instruction.
  - Create path is "New block" in the top nav, unreferenced from the empty state.
  - 45 seconds from dashboard to clicking "New block", via a search that returned nothing.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/session.log:14`
  > "Dashboard. "Your cards" — "Nothing here yet." Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup; land on the dashboard.
  2. Read the "Your cards" panel.
- **Fix:** Replace "Nothing here yet." with a primary action that opens the create form and one line saying what appears here once it exists.

### be15f6ac8e3c — Settings labels are engineering vocabulary with no explanation
- **Severity:** P2
- **So what:** Both personas met three toggles they could not evaluate — one pre-checked — and left the screen having learned only what "Export" does.
- **Framework tags:** A2, A6
- **Flow:** shape_2b
- **Locator:** screen:settings
- **Personas hit:** novice, power-user
- **Observed:**
  - Toggles: "Enable webhook sync" (off), "Federated graph replication" (on), "Vault attestation" (off); no helper text on any.
  - Only "Export — Markdown, all cards" was understood by both.
  - Persona-defined-as-non-technical could explain none of the three terms; the power-user could explain none in the product's own context.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24` · `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:13`
  > "Settings. "Enable webhook sync", "Federated graph replication", "Vault attestation". No idea. There's an Export button — "Markdown, all cards". At least that's clear."
- **Repro:**
  1. Click "Settings" in the top nav.
  2. Read the three checkbox labels.
- **Fix:** Add a one-line, user-outcome description under each toggle, and move any toggle with no user-facing outcome out of Settings.

### e8958b7397ca — Search "No results" copy offers no next step
- **Severity:** P3
- **So what:** On an empty workspace the message reads as a failure rather than a nudge to create; after the save defect it read as a second lie.
- **Framework tags:** A9
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - "No results for 'meeting'." / "No results for 'Dentist'." / "No results for 'test'." — same string regardless of whether the workspace has zero cards.
  - No link to create, no hint that the workspace is empty.
- **Evidence:** `persona-novice/session.log:13` · `persona-novice/session.log:19` · `persona-power-user/session.log:10` · `persona-power-user/screenshots/03-search-empty.png`
  > "Typed "meeting". "No results for 'meeting'." Well, there's nothing in it."
- **Repro:**
  1. On a fresh dashboard, type any word in "Search your notes" and press Enter.
- **Fix:** When the workspace has zero cards, replace the no-results line with the empty-workspace message and a create action.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The "Saved ✓" toast itself was never captured — `04-note-saved-toast.png` shows the empty form, no toast. The P0 rests on session-log lines and the post-save screenshots.
- The memories footer "connected accounts" implies an account-connection flow that no persona found; no screenshot of a connect surface exists.

## For other lenses
- Save/list/search defect (note never persisted or never listed) — **bugs**; the content finding above is the false confirmation, not the root cause.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, /) — **ux** (`persona-power-user/session.log:12`).
- Novice first value at 2:41 was the live preview, not the promised memory — **onboarding**.
- Radio/checkbox controls visually detached from their labels (`01-signup-workspace-type.png`, `07-settings.png`) — **ux**.

## Coverage gaps
- The marketing site itself was not captured; the promise is taken from the pre-session note only.
- "Cards" nav item never opened as a distinct screen.
- Export button never clicked; export output copy unassessed.
- No mobile device; both personas desktop 1440×900.
- Memories screenshot exists for novice only; power-user observation is log-only.

## Appendices
- A. Persona debriefs: `persona-novice/persona-debrief.md`, `persona-power-user/persona-debrief.md`
- B. Session timelines: `persona-novice/timeline.json`, `persona-power-user/timeline.json`
- C. Screenshot index: `persona-novice/screenshots/00-start.png` … `07-settings.png` (9); `persona-power-user/screenshots/00-start.png`, `02-dashboard.png`, `03-search-empty.png`, `07-settings.png` (4)
