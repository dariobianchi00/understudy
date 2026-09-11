# Nimbus Notes — content findings — Run 2026-09-08 (fixture02)

## Method
- Framework: promise-vs-delivery first, then Nielsen A2/A4/A9 on reading level, jargon density, error and empty-state copy
- Pass 1 naive capture → Pass 2 analyst scoring
- Personas: **generic — INFERRED**, not researched; every persona-specific judgement below is weaker for it
- Scoring model: `opus`
- Every finding cites an artifact; unsupported observations dropped, listed at the end
- Layer B (AI-specific) is not applied: no AI surface was exercised, though the Memories page implies one

## Promise vs delivery

| Persona | Arrived expecting | Product delivered | Match | Cost |
|---|---|---|---|---|
| novice | "remembers everything so you never start from zero" | "Nothing here yet.", one note lost twice, three memories about a stranger | **Fail** | Quit at 06:30 with zero notes saved; "It is lying to me" |
| power-user | "remembers everything so you never start from zero" | Empty dashboard, save that does not persist, search that returns nothing | **Fail** | Quit at 03:00; "Save doesn't save and search doesn't search" |

- Both personas' own Q4 answers agree with this reading: novice "No", power-user "No". No disagreement to reconcile.
- The promise is inverted, not merely unmet: the pitch says *remembers everything*, the product forgets what it was given and remembers things it was not.
- That inversion is the root cause of the two P0s below, and both personas named it unprompted.

---

## Findings

### e4503247aa0e — Green "Saved ✓" confirms a save that returned HTTP 500; no failure copy exists
- **Severity:** P0
- **So what:** Both personas believed their note was kept, navigated away, and lost it — the product's own words caused the data loss to go unnoticed.
- **Framework tags:** A1, A9, C-ABANDON
- **Flow:** shape_2
- **Locator:** /app/new.html
- **Personas hit:** novice, power-user
- **Observed:**
  - `POST /api/notes` returned `500 internal error` at 03:05 and again at 03:50 for the novice, at 01:00 for the power-user.
  - The UI rendered a green "Saved ✓" toast on every one of those failures.
  - No error string was shown at any point in either session; the product has no observed failure copy.
- **Evidence:** `persona-novice/session.log:17` · `persona-novice/session.log:20` · `persona-novice/network-full.txt` · `persona-power-user/session.log:11` · `persona-novice/console-full.txt`
  > "[03:50] Went back to New block. Wrote it again, saved again, "Saved ✓" again, dashboard empty again. It is lying to me."
- **Repro:**
  1. Open `/app/new.html`, enter a title and body.
  2. Click **Save** while `POST /api/notes` is failing.
  3. Observe the green "Saved ✓" toast; return to the dashboard and observe the note is absent.
- **Fix:** Gate the "Saved ✓" string on a 2xx response, and write a failure string for the save form that names what happened and tells the user their text is still in the editor.

### 2fb6262a2417 — Memories page states three facts about the novice that are not hers, captioned as built from her notes
- **Severity:** P0
- **So what:** She concluded the product fabricates, then retro-actively distrusted every other message it had shown her, including "Saved".
- **Framework tags:** A2, A9, C-ABANDON
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** novice
- **Observed:**
  - The page is headed "What Nimbus remembers about you" and lists "You prefer to schedule meetings on Tuesday afternoons.", "Your team uses Jira and Slack.", "You are working on a product launch in Q4."
  - The caption reads "Memories are built from your notes and connected accounts." — the novice had written one note, about a dentist, and connected no accounts.
  - The caption is the defect: it asserts a provenance for the content that the session record contradicts.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-novice/session.log:21` · `persona-novice/session.log:22` · `persona-novice/persona-debrief.md`
  > "[04:50] None of that is true. I've written one note about a dentist. Where is this from? If it's making these up, is it making up the "Saved" too?"
- **Repro:**
  1. Create a new workspace and write exactly one note.
  2. Open `/app/memories.html`.
  3. Observe three memories referencing meetings, Jira, Slack and a Q4 launch, under a caption claiming they came from your notes.
- **Fix:** Remove the seeded memory entries from a new workspace, and rewrite the caption on `/app/memories.html` so it states which note each memory came from.

### 78c27ad006fc — Power-user reads the Memories page as demo filler and discounts the whole surface
- **Severity:** P2
- **So what:** He did not panic, he wrote the feature off — the headline capability is dead to an evaluating buyer before he ever tests it.
- **Framework tags:** A2, A4
- **Flow:** shape_2b
- **Locator:** /app/memories.html
- **Personas hit:** power-user
- **Observed:**
  - Same three seeded entries and the same "Memories are built from your notes and connected accounts." caption.
  - He read them as sample content rather than as a claim about him, and moved on in under 30 seconds.
  - Nothing on the page labels the entries as examples, which is what would have made his reading correct.
- **Evidence:** `persona-novice/screenshots/06-memories.png` · `persona-power-user/session.log:14` · `persona-power-user/findings-raw.json`
  > "[02:30] Memories. Tuesday meetings, Jira, Q4 launch. Not me. Whatever — a demo panel, I assume. Not going to trust it."
- **Repro:**
  1. Create a workspace as an evaluating user and open `/app/memories.html` before writing anything.
  2. Observe entries that read as generic sample data with no "example" or "sample" label.
- **Fix:** If seeded entries stay, label them "Example" on `/app/memories.html` and say in one line what a real memory will look like; otherwise ship the page empty with copy naming what fills it.

### a12564f0a23f — No screen restates the "never start from zero" promise; both personas answer Q4 "No"
- **Severity:** P1
- **So what:** Both arrived expecting a workspace that fills itself in, met "Nothing here yet.", and never found a line of copy reconciling the two.
- **Framework tags:** A2, B-G1, C-SOWHAT
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Both personas' pre-session note records the same promise: "remembers everything so you never start from zero".
  - The first post-signup screen shows "Your cards" and "Nothing here yet." with no reference to importing, connecting or remembering anything.
  - Both answered Q4 "No"; the only surface that gestures at the promise, `/app/memories.html`, does so with content neither persona supplied.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-power-user/screenshots/02-dashboard.png` · `persona-novice/session.log:1` · `persona-novice/session.log:12` · `persona-power-user/persona-debrief.md`
  > "I arrived with "remembers everything so you never start from zero". No — it started completely empty, it lost what I gave it, and the "memories" it does have aren't mine."
- **Repro:**
  1. Arrive from the marketing promise "remembers everything so you never start from zero".
  2. Complete signup and land on `/app/dashboard.html`.
  3. Read every string on the screen; none mentions remembering, importing or connecting.
- **Fix:** Add a line to the post-signup dashboard naming what Nimbus will remember and from where, or change the marketing line to promise capture rather than recall.

### 022fb4062d3a — Irreversible first choice is labelled with three undefined terms and no description
- **Severity:** P1
- **So what:** The novice guessed on a decision the copy told her she could never change, 48 seconds into the product.
- **Framework tags:** A2, A5, C-ABANDON
- **Flow:** shape_1
- **Locator:** /app/signup.html
- **Personas hit:** novice
- **Observed:**
  - The screen reads "Before we begin, choose your workspace type" with radio labels "Federated graph", "Sovereign vault", "Hybrid mesh".
  - The only supporting copy is "This cannot be changed later." — there is no description of any option.
  - She chose "Hybrid mesh" on the reasoning that the word "hybrid" implied the other two.
- **Evidence:** `persona-novice/screenshots/01-signup-workspace-type.png` · `persona-novice/session.log:10` · `persona-novice/session.log:11` · `persona-novice/findings-raw.json`
  > "[00:20] I don't know what any of these are. It says I can't change it. I haven't seen the product yet and it wants a decision I can't undo."
- **Repro:**
  1. Open `/app/signup.html` as a first-time non-technical user.
  2. Read the three option labels and the helper line.
  3. Observe there is no text explaining what any option does or which to pick.
- **Fix:** Add a one-line plain-language description under each workspace-type option on `/app/signup.html` saying who it is for, or default the choice and move it into Settings.

### 544c9fc67077 — Three Settings toggles are labelled in engineering vocabulary with no description
- **Severity:** P2
- **So what:** The novice could not tell what any of the three switches controlled, including the one already switched on for her.
- **Framework tags:** A2, A6
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** novice
- **Observed:**
  - The page offers "Enable webhook sync", "Federated graph replication" and "Vault attestation", each a bare checkbox with no helper text.
  - "Federated graph replication" is checked by default.
  - The one control she understood was the one written in plain words: "Export" / "Markdown, all cards".
- **Evidence:** `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:23` · `persona-novice/session.log:24`
  > "[06:00] surface: Memories — I don't trust it. surface: Settings — words I don't know, one button I do."
- **Repro:**
  1. Open `/app/settings.html` as a non-technical user.
  2. Read the three toggle labels.
  3. Observe no description, tooltip or help link on any of them.
- **Fix:** Add a one-line description under each toggle on `/app/settings.html` stating what turning it on does for the user, in the register used by the Export row.

### a422a9490d7e — "Federated graph replication" reuses the signup term without saying they are the same thing
- **Severity:** P2
- **So what:** The power-user could not tell whether the Settings toggle was the workspace type he had already chosen and could not change.
- **Framework tags:** A4, A2
- **Flow:** shape_2b
- **Locator:** /app/settings.html
- **Personas hit:** power-user
- **Observed:**
  - Signup offers a workspace type called "Federated graph"; Settings offers a toggle called "Federated graph replication".
  - No copy on either screen states whether they are the same setting, related, or independent.
  - The toggle is checked in both personas' Settings screenshots, including the novice's, who chose "Hybrid mesh" at signup.
- **Evidence:** `persona-power-user/screenshots/07-settings.png` · `persona-novice/screenshots/07-settings.png` · `persona-power-user/session.log:13` · `persona-power-user/findings-raw.json`
  > "Is 'Federated graph replication' the thing I picked at signup? Same words, no link."
- **Repro:**
  1. Choose "Federated graph" at `/app/signup.html`.
  2. Open `/app/settings.html` and read the "Federated graph replication" row.
  3. Observe no copy linking it to, or distinguishing it from, the signup choice.
- **Fix:** On `/app/settings.html`, state the workspace type in words next to the replication toggle and say explicitly whether the toggle changes it.

### 1da978a49de2 — One concept is called "cards", "blocks" and "notes" across four adjacent labels
- **Severity:** P2
- **So what:** The novice stopped to work out whether "New block" would produce the thing she wanted before she could write anything.
- **Framework tags:** A4, A2
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - One screen carries nav items "Cards" and "New block", the heading "Your cards", and the search placeholder "Search your notes".
  - The editor page is titled "New block"; Settings describes the export as "Markdown, all cards".
  - Nothing defines any of the three words or relates them to each other.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/screenshots/03-new-note.png` · `persona-novice/screenshots/07-settings.png` · `persona-novice/session.log:14`
  > "[01:40] Top menu: Cards, New block, Memories, Settings. Cards and blocks — same thing? Clicked "New block"."
- **Repro:**
  1. Land on `/app/dashboard.html` after signup.
  2. Read the nav, the list heading and the search placeholder together.
  3. Observe three different nouns for the same object.
- **Fix:** Pick one noun for the object and apply it to the nav item, the list heading, the search placeholder, the editor title and the export label.

### 4d2fa313b730 — Empty state "Nothing here yet." names no next action
- **Severity:** P2
- **So what:** The novice's first screen after signup told her nothing about what to do, costing her 45 seconds of hunting before she found the editor.
- **Framework tags:** A2, A10, C-TTFV
- **Flow:** shape_1
- **Locator:** /app/dashboard.html
- **Personas hit:** novice
- **Observed:**
  - The "Your cards" panel contains the single string "Nothing here yet." with no button, link or instruction.
  - She reached the dashboard at 00:55 and did not open the editor until 01:40.
  - She first tried the search box on an empty workspace before finding "New block" in the nav.
- **Evidence:** `persona-novice/screenshots/02-dashboard-empty.png` · `persona-novice/session.log:12` · `persona-novice/session.log:13` · `persona-novice/timeline.json`
  > "[00:55] Dashboard. "Your cards" — "Nothing here yet." Nothing tells me what to do. I thought it would have my stuff."
- **Repro:**
  1. Complete signup and land on `/app/dashboard.html` with no content.
  2. Read the empty panel.
  3. Observe it states a condition and offers no action.
- **Fix:** Replace "Nothing here yet." with copy naming the first action and place the primary create control inside the empty panel.

### b7aafa96f111 — Search failure copy names the query and offers no next step
- **Severity:** P2
- **So what:** After a save the product had confirmed, search told the novice "No results" without hinting that anything had gone wrong or what to try.
- **Framework tags:** A9, A2
- **Flow:** shape_2
- **Locator:** /app/dashboard.html
- **Personas hit:** novice, power-user
- **Observed:**
  - Search returns only "No results for 'meeting'.", "No results for 'Dentist'.", "No results for 'test'.", "No results for 'Roadmap'."
  - The message is identical whether the workspace is empty or the user is searching for something they just saved.
  - Neither persona could distinguish "you have nothing" from "your note is missing" from this string.
- **Evidence:** `persona-novice/session.log:13` · `persona-novice/session.log:19` · `persona-power-user/session.log:10` · `persona-power-user/screenshots/03-search-empty.png`
  > "[03:30] Typed "Dentist" in search. "No results for 'Dentist'." It said saved."
- **Repro:**
  1. Save a note, then search its exact title from `/app/dashboard.html`.
  2. Observe "No results for '<title>'." and no further text.
- **Fix:** Split the search zero-result copy into an empty-workspace variant that points at the editor and a no-match variant that suggests what to try next.

---

## Dropped for want of evidence
Observations that did not meet the evidence rule. **Not findings.**

- The exact toast wording and colour — `persona-novice/screenshots/04-note-saved-toast.png` shows the empty "New block" form, not a toast; the string "Saved ✓" rests on `session.log` alone.
- The exact rendered "No results" string — no screenshot captured it; `persona-power-user/screenshots/03-search-empty.png` shows the dashboard with an empty search box.
- Reading level of the "Cards" list once populated — no persona ever saw a populated list.
- Whether any help or documentation copy exists — no help surface was opened in either session.

## For other lenses
- `POST /api/notes` returns 500 on every save, and `renderGraphOverlay is not defined` throws on every dashboard load — `bugs`.
- "Federated graph replication" is checked on for a persona who chose "Hybrid mesh" at signup — `bugs`.
- No keyboard shortcuts (Ctrl+K, Ctrl+N, `/`) respond for the power-user — `ux`.
- Dashboard offers no primary create control, forcing nav discovery — `ux`, `onboarding`.

## Coverage gaps
- `/app/cards.html` (the "Cards" nav item) was never opened by either persona.
- No error, consent, permissions or help screen was rendered in either session.
- No mobile or tablet viewport; both personas ran desktop-1440x900.
- No populated-state copy was ever observed, because no save succeeded.

## Appendices
- A. Persona debriefs — `persona-novice/persona-debrief.md` · `persona-power-user/persona-debrief.md`
- B. Session timelines — `persona-novice/timeline.json` · `persona-power-user/timeline.json`
- C. Screenshot index — `persona-novice/screenshots/` (8) · `persona-power-user/screenshots/` (4)
