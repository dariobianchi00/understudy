# Nimbus Notes — ux findings — Run 2026-09-08 (fixture02)

## Method
- Framework: Layer A (Nielsen 10) · Layer B (HAX — applies; "Memories" is a user-facing AI surface) · Layer C (activation)
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: generic — ⚠ INFERRED, not researched
- Scoring model: opus
- Every finding cites an artifact; unsupported observations dropped, listed at the end

---

## Findings

### eed102c5daad — Save reports success but the note never appears in the cards list or search
- **Severity:** P0
- **So what:** The single objective under test failed for both personas, and both quit rather than try a third time.
- **Framework tags:** A1, A9, A5, C-ABANDON, C-TTFV, C-SOWHAT
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Both personas typed a note, clicked Save, and saw a green "Saved ✓" toast; both were returned to a dashboard reading "Nothing here yet."
  - Searching the note's own title returned "No results for 'Dentist'" and "No results for 'Roadmap'".
  - The novice repeated the whole sequence once and got the identical false confirmation; `timeline.json` records `gave_up: true` for both.
- **Evidence:** `persona-novice/screenshots/05-notes-list-missing.png` · `persona-power-user/screenshots/03-search-empty.png` · `persona-novice/session.log:17-20` · `persona-power-user/session.log:11` · `persona-novice/timeline.json` objectives[0].gave_up
  > "Saved twice, empty twice. It is lying to me."
- **Repro:**
  1. Open `/app/new.html`, enter a title and body.
  2. Click Save; observe the "Saved ✓" toast and the redirect to the dashboard.
  3. Observe "Your cards" still reads "Nothing here yet."; search the title and get no results.
- **Fix:** Make the Save button surface the write's actual outcome — keep the user on the form with the draft intact and an error when the write fails, and only show "Saved ✓" after the note is confirmed in the list.

### 7956c85815ae — Memories states three facts that are not the user's, and the novice stops trusting Save as a result
- **Severity:** P0
- **So what:** A confident false claim about her own data cost the product her trust in every other confirmation it gave her.
- **Framework tags:** A1, B-G1, B-G2, B-G11, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - The page is headed "What Nimbus remembers about you" and lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - Footer copy asserts a source: "Memories are built from your notes and connected accounts." The persona had written one note, about a dentist, and connected nothing.
  - She generalised the distrust to the rest of the product 30 seconds later, then ended the session at 06:30.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21-22` · `persona-novice/session.log:25`
  > "None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the 'Saved' too?"
- **Repro:**
  1. Create a workspace and write one note.
  2. Open Memories from the top nav.
  3. Observe three specific claims about the user unrelated to anything they entered.
- **Fix:** Show an empty Memories state until real notes exist, and attach a visible source note to each memory linking back to the card it was derived from.

### 1628c36798fa — Memories states three facts that are not the user's, and the power user writes the feature off as a demo panel
- **Severity:** P2
- **So what:** The headline differentiator was silently reclassified as decoration by the buyer evaluating it for a team.
- **Framework tags:** B-G1, B-G2, C-SOWHAT
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three claims seen at 02:30; he did not stop, and moved on within the same minute.
  - He assigned his own explanation rather than the product's, and pre-emptively withheld trust.
  - In the debrief he could not name Memories among things he would use.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json` t=02:30
  > "Memories aren't mine. A demo panel, I assume."
- **Repro:**
  1. Create a workspace as a new user.
  2. Open Memories before writing anything.
  3. Observe seeded third-party claims with no "example" or "demo" label.
- **Fix:** If the panel ships with sample content, label it "Example" on the card itself; otherwise populate it only from the user's own notes.

### 19b57540c074 — Signup forces an irreversible workspace-type choice between three undefined terms before the product is visible
- **Severity:** P2
- **So what:** The novice made a permanent decision by guessing, 48 seconds into a product she had not yet seen.
- **Framework tags:** A2, A5, A10, B-G11
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - Screen reads "Before we begin, choose your workspace type" with radio options "Federated graph", "Sovereign vault", "Hybrid mesh" and the line "This cannot be changed later."
  - No definition, tooltip, help link or default is offered for any option.
  - 28 seconds of hesitation, then a guess; she continued rather than leaving.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:9-11`
  > "Picked 'Hybrid mesh' because it sounds like it includes the other two."
  > "I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Open `/app/signup.html` as a new user.
  2. Observe three unexplained options and "This cannot be changed later."
- **Fix:** Add one plain-language sentence under each option, preselect a sensible default, and either make the choice reversible or move it into Settings after first value.

### 8b240ac04f8b — Cards, blocks and notes name the same object across nav, headings and search placeholder
- **Severity:** P2
- **So what:** The novice had to stop and test which menu item created a note, costing her a hunt on the way to first value.
- **Framework tags:** A2, A4, A6
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - One screen carries all three words: nav items "Cards" and "New block", heading "Your cards", search placeholder "Search your notes".
  - The persona paused at 01:40 to ask whether they were the same thing, then clicked "New block" to find out.
  - `timeline.json` records `times_had_to_hunt: 2` for this persona.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:14` · `persona-novice/findings-raw.json` t=01:40
  > "Cards, blocks, notes — are these the same thing?"
- **Repro:**
  1. Open `/app/dashboard.html`.
  2. Compare the nav labels, the section heading and the search placeholder.
- **Fix:** Pick one noun — "note" — and use it in the nav, the list heading, the create button and the search placeholder.

### 3a88dad0ccdf — Empty dashboard names no next step after signup
- **Severity:** P2
- **So what:** The first screen after signup told her nothing to do, and contradicted the promise that brought her in.
- **Framework tags:** A1, A6, A8, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - The only content is a search box, the heading "Your cards" and the line "Nothing here yet." — no button, link or prompt.
  - She searched an empty workspace at 01:20 before finding the create path at 01:40.
  - She arrived expecting pre-filled content: "I thought it would have my stuff."
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12-13`
  > "'Nothing here yet.' Nothing tells me what to do."
- **Repro:**
  1. Complete signup.
  2. Observe the dashboard empty state with no call to action.
- **Fix:** Replace "Nothing here yet." with a primary "Write your first note" button and one line saying what happens after that.

### 8e744d427864 — Settings exposes three infrastructure toggles neither persona could define
- **Severity:** P2
- **So what:** The only settings screen is unusable to both personas except for the one control written in plain English.
- **Framework tags:** A2, A10, A8
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Three checkboxes labelled "Enable webhook sync", "Federated graph replication" and "Vault attestation", with no description under any of them.
  - The only element either persona understood was the "Export" button, captioned "Markdown, all cards".
  - Both named Export as legible and the toggles as not.
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-power-user/screenshots/07-settings.png` · `persona-novice/session.log:23-24` · `persona-power-user/session.log:13`
  > "'Enable webhook sync', 'Federated graph replication', 'Vault attestation'. No idea. There's an Export button — 'Markdown, all cards'. At least that's clear."
- **Repro:**
  1. Open `/app/settings.html`.
  2. Observe three unlabelled-purpose toggles beside one plainly captioned button.
- **Fix:** Add a one-line description under each toggle in the same register as "Markdown, all cards", or move developer-only settings behind an "Advanced" disclosure.

### 4c0b0708ef66 — Settings toggle repeats the signup workspace-type wording with no stated relationship to that choice
- **Severity:** P2
- **So what:** The power user could not tell whether he was looking at the permanent choice he made at signup or a separate switch he could flip.
- **Framework tags:** A4, A2, A3
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - He selected "Federated graph" at signup, on a screen saying "This cannot be changed later."
  - Settings shows a checked checkbox reading "Federated graph replication" with no reference back to that choice.
  - He raised the ambiguity and moved on without resolving it.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-power-user/session.log:8` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json` t=02:00
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Choose "Federated graph" at signup.
  2. Open Settings and observe "Federated graph replication" checked, with no stated link to the signup choice.
- **Fix:** Show the chosen workspace type as read-only text at the top of Settings, and rename the toggle so it does not reuse that wording.

### 7996c92bea2e — No keyboard shortcuts on any surface
- **Severity:** P2
- **So what:** The persona evaluating this for a team tested the thing he came for in the first 90 seconds and found it absent.
- **Framework tags:** A7, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** power-user
- **Observed:**
  - He arrived expecting "fast capture, good search, keyboard-driven".
  - He tried Ctrl+K, Ctrl+N and `/` at 01:30; none did anything.
  - No shortcut hint appears in the nav or on the search box.
- **Evidence:** `persona-power-user/screenshots/02-dashboard.png` · `persona-power-user/session.log:1` · `persona-power-user/session.log:12` · `persona-power-user/findings-raw.json` t=01:30
  > "Tried keyboard: Ctrl+K, Ctrl+N, / — nothing. No shortcuts."
- **Repro:**
  1. Open `/app/dashboard.html`.
  2. Press Ctrl+K, Ctrl+N and `/`; observe no response.
- **Fix:** Bind `/` to focus search and Ctrl+N to new note, and show the hint in the search placeholder.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The live word count and preview may be the product's strongest moment — only the novice saw it, and only one line records it; no second persona to corroborate.
- Export may produce nothing given no note persists — neither persona clicked it, so no artifact exists.
- Whether Memories is generated or hardcoded seed data — no observation distinguishes the two.

## For other lenses
- `POST /api/notes → 500` on both save attempts, and `Uncaught ReferenceError: renderGraphOverlay is not defined` on every dashboard load — `bugs`.
- "Federated graph", "Sovereign vault", "Vault attestation" as consumer-facing register — `content`.
- Marketing promise "remembers everything so you never start from zero" against a product that starts empty — `content`.
- Both personas dropping at the same step in shape_2 — `onboarding`.
- Accessibility: not assessed — no lens covers WCAG in this method.

## Coverage gaps
- `persona-novice/screenshots/04-note-saved-toast.png` does not show the "Saved ✓" toast or the typed note — it is a pixel-identical capture of the empty `New block` form. The toast is evidenced by `session.log:17` only.
- No screenshot of the Cards surface holding a note — no note ever persisted.
- No screenshot of a search results state with results.
- Mobile and tablet viewports never tested; both personas ran desktop-1440x900.
- Note edit and delete flows never reached.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — 9 novice captures, 4 power-user captures; all opened during scoring
