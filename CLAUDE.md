# understudy

An agent that stands in for a user, drives a live web product, and reports back through a chosen lens.

**This file is the design spec and the standing conventions for this repo.** It records what the architecture is, why it is shaped this way, and which properties must not be traded away. The build sequence that produced it has been deleted; §10 keeps only the decisions from it that are load-bearing.

---

## 0. Read this first (for the agent building this repo)

### Vocabulary — three things with confusingly similar names

Get these straight before reading further. Conflating them is the easiest way to misread this spec.

| Term | Means |
|---|---|
| **the reference skill** | The pre-existing single-product, single-lens skill this repo generalises. It already works, validated over three real runs. It is the *source* of the methodology, not part of this repo. Its location is in `BUILD_NOTES.local.md`. |
| **Pass 1 / Pass 2** | The two halves of a single run at execution time — see below. Not to be confused with the build phases the repo was constructed in, which are gone. |
| **Pass 1 / Pass 2** | The two halves of a single run at execution time. Pass 1 = the naive persona gathers evidence; Pass 2 = the analyst scores it. The anti-bias design (§6, invariant 1). |

Throughout this file, **"the reference skill"** never means a build phase and **"Phase N"** never means the reference skill.

### ⚑ Check this before starting

This repo is greenfield. The methodology it extracts is **not reproduced in this file** and must not be guessed at.

`BUILD_NOTES.local.md` — gitignored, never committed — holds the reference skill's location, the four methodology files to read, and the migration inventory.

**Can you read `BUILD_NOTES.local.md`, and the path it names?**

- **Yes** → read the four methodology files it lists before writing anything, plus the reference skill's own `SKILL.md`. They carry hard-won detail — MCP viewport bugs, the two-pass anti-bias design, the evidence rule — that must survive the port. Then follow its migration table.
- **No** → **stop and tell the user.** Roughly 190 lines across four files cover: Nielsen's 10 heuristics and Microsoft's HAX 18 condensed into a Layer A/B/C cheat sheet · a P0–P3 severity rubric with worked examples · the exec-summary and findings templates · and Playwright-MCP call patterns with documented upstream workarounds. Reinventing these produces a plausible-looking framework that will not reproduce the reference skill's findings. **The build cannot proceed without them.**

*(Why the pointers are not inlined here: this file ships in a public repo and §7 forbids product-identifying content — including paths that name a product. `BUILD_NOTES.local.md` exists for that reason alone.)*

**Two files from the reference skill must never be copied into this repo** under any circumstances — its personas file and its product config. They contain real customer segmentation and a real product's commercial data. `BUILD_NOTES.local.md` names them. See §7.

---

## 1. What this is

The reference skill answered *"is this product's UX any good?"* for one product. understudy answers **any evaluative question about any web product**, by separating three things the reference skill had fused together:

- **the target** — which product, which personas, which credentials *(never in this repo)*
- **the traversal** — how evidence gets gathered
- **the lens** — how that evidence gets scored into a report

Add a lens by writing one agent file. Add a product by answering an interview. Neither requires touching the harness.

---

## 2. The architecture — traversal modes

Objectives do not group by topic. They group by **what the agent physically has to do to gather the evidence.** This is the whole design.

| Mode | Evidence gathering | Lenses |
|---|---|---|
| **A — Journey** | A persona with a goal drives the product. **One traversal, many scorings.** | ux · bugs · onboarding · content |
| **A-visit — Visit** | A persona with a *question* reads a site. Same machinery, different flow shapes, ~1/4 the time. | clarity · conversion · trust · content |
| **B — Instrumented** | Scripted and measured, no persona. Own traversal. | technical · accessibility · responsive · security-surface |
| **C — Crawl** | No session, often no login. | seo · aeo · compliance |
| **D — Comparative** | N runs of A, A-visit or C, then a diff pass. | compare · parity · pricing |

**A-visit is a variant of A, not a fifth mode.** The evidence-gathering is identical — a persona drives a browser and leaves artifacts. Only the flow shapes differ, so it reuses the traversal skill, the capture gate, the evidence rules and the two-pass separation unchanged. Inventing a mode for it would duplicate all of that to express one difference.

**Why the shapes differ:** a product user's journey is entry → activation → first value → surfaces → debrief. A site visitor's is **land → orient → evaluate → decide**, and their "first value" is *"did I understand what this is and decide whether to care?"* — reached in twenty seconds or never. Forcing a visitor through product shapes produces findings about a signup flow they were never going to reach.

### The orchestrator contract

> **Group the requested objectives by mode → capture ONCE per mode → fan out every scoring for that mode.**

The six Mode-A lenses all score the *same* persona traversal. One expensive browser session, N cheap analyst passes in parallel. Running one agent per objective through the product would cost ~6× for identical evidence.

**Structural precedent:** `~/.claude/plugins/marketplaces/claude-code-plugins/plugins/pr-review-toolkit/` ships one command fanning out to six specialist agents over one artifact. Read it — it is the shape this repo implements.

---

## 3. Scope — two assessment types, one architecture

**The user's first question is not "which mode" — it is "what am I evaluating?"** Modes are an implementation detail. The entry fork is:

| | **Product assessment** | **Website assessment** |
|---|---|---|
| The thing | An app someone signs into and uses | A site someone reads and decides from |
| The persona's goal | Accomplish a task | Answer a question: *is this for me?* |
| Success | Reached first value | Understood the offer and knew what to do next |
| Time per persona | ~90 min | ~15–25 min |
| Auth | Usually a wall, human-in-the-loop | Usually none |
| Competitors | Blocked by their auth wall | **Fully reachable — this is where Mode D works** |

Each resolves to a lens bundle. Same harness, same gates, same two-pass separation.

### Product assessment — Mode A + C

1. **ux** — Nielsen 10 + Microsoft HAX 18 + activation *(ported from the reference skill unchanged)*
2. **bugs** — console errors, failed requests, dead ends, broken states. Output is repro steps + environment, not a findings list
3. **onboarding** — steps-to-value, time-to-first-value, drop-off points. Output is a funnel
4. **content** — promise-vs-delivery match, reading level, jargon density

### Website assessment — Mode A-visit + B + C + D

5. **clarity** — can a visitor say what this is, who it's for, and what to do next? Time-to-comprehension, the point they lost interest, what they misunderstood
6. **conversion** — is the next step obvious at every scroll depth? CTA hierarchy, form burden, dead-end pages, the gap between what the page asks for and what the visitor is ready to give
7. **trust** — proof, pricing transparency, who is behind this, what happens to my data. The objections a sceptic raises and whether the site answers them
8. **technical** — the metric set in §3.1. Mode B, **pulled forward from "extension point" because a website assessment without it is incomplete**
9. **seo** — crawlability, meta, canonical, structured data, internal linking, sitemap, indexability
10. **aeo** — schema.org coverage, extractable answer blocks, entity clarity, `llms.txt`. **Static markup only in v1**; querying live answer engines is deferred — see §11.3
11. **compare** — the same lenses across 2+ sites, then a diff pass producing a differences matrix

**⚑ `compare` is the key question for website assessment**, not an afterthought. Build it *with* the website bundle, not in a later phase — a site audit that cannot answer *"how do we look next to them?"* is answering the easier question.

**Competitors are always user-supplied.** understudy never infers who they are. A wrong competitor set produces a confident, useless comparison, and the user is the only one who knows whether the site they're worried about is the obvious one or the one nobody names.

### 3.1 Technical metrics — the recommended set

All obtainable from Playwright MCP with no extra tooling: Navigation Timing, `PerformanceObserver`, the network log, response headers.

| Tier | Metrics | Why |
|---|---|---|
| **1 — Experience** | LCP · CLS · TBT (INP proxy) · FCP · TTFB | The Core Web Vitals, plus the two that explain them |
| **2 — Delivery** | Page weight · request count · 5 largest assets · image hygiene (format; natural vs displayed dimensions) · compression · cache headers · render-blocking resources · **third-party weight and count** | Where a fast site went slow. Oversized images and third parties account for most of it |
| **3 — Hygiene** | HTTPS + HSTS · mixed content · viewport meta · redirect chains · 404s on linked assets · console errors on load | Cheap to check, embarrassing to miss |

**⚑ These are lab numbers and the report must say so on its face.** One measurement, one machine, one connection. They identify what is wrong with the *page* — a 4 MB hero image is a fact at any sample size. They do **not** describe what users experience, which needs field data understudy cannot reach. Presenting a lab LCP as "your users' LCP" is confidently wrong, and it is the kind of error that gets a whole tool distrusted.

**Measure mobile and desktop separately.** For most marketing sites the mobile number is the real one and the desktop number is the flattering one.

---

## 4. Onboarding contract

Runs on every invocation. Never assumes. One question at a time.

1. **Check for a saved target.** If `~/.understudy/targets/` matches → *"Found target `<slug>` (last run `<date>`). Reuse / edit / start fresh?"*
2. **⚑ Assessment type — the first question, asked before anything else:**
   ```
   What are you evaluating?

     (a) A product — something people sign into and use.
         Lenses: ux · bugs · onboarding · content
         ~90 min per persona.

     (b) A website — something people read and decide from.
         Lenses: clarity · conversion · trust · technical · seo · aeo · compare
         ~15-25 min per persona, plus a crawl.

     (c) Both — a marketing site with a product behind it.
         Runs (b) on the site, then (a) on the product. Two captures.
   ```
   *This is asked first because it determines every later question. A product interview asks about first value and auth walls; a website interview asks about competitors and conversion goals. Asking them in the wrong order produces an interview that does not fit what the user has.*
3. **Interview:**
   - Product or site name + base URL. Public, or behind auth?
   - **If website assessment: competitor URLs.** Ask for 1–3. **Never infer them** — a wrong competitor set produces a confident, useless comparison. "None" is a valid answer; say that comparison will be skipped.
   - **If website assessment: what should a visitor do next?** The conversion goal — sign up, book a call, read the docs, buy. Without it, `conversion` has no target to score against and degrades into generic CTA advice.
   - **Objectives** — multi-select, defaulted from the assessment type. Show which mode each belongs to and what that costs in traversals.
   - **⚑ Personas — an explicit fork, asked every run:**
     - **(a) Generic** — the agent proposes N personas from the product type and objective alone (defaults: novice · power-user · sceptic). Fast, zero input. **The report must state on its face that findings rest on inferred personas.**
     - **(b) Supplied** — the user pastes or points at their own persona definitions. The agent parses them and does not invent.
     - *This fork exists because persona quality, not the harness, is what makes the output good — and persona quality cannot ship in a public repo. Making it a visible choice turns a silent limitation into a stated one.*
   - Device profile per persona
   - **⚑ Models — confirmed, not assumed (both levels):**
     - **Traversal model** = the current session model. understudy reports what it is and whether it's the strongest one available. It **cannot switch** — if the user wants a different one they run `/model` and re-invoke. Say why it matters: traversal is the irreversible part.
     - **Scoring models** — show the per-lens default allocation and the spend it implies. Offer three shapes: *thorough* (opus across the board) · *balanced* (the default split) · *cheap* (sonnet across the board). Per-lens override allowed.
     - *This is asked because an evaluation is a real spend, and trading cost against depth is the user's call. It is also the last honest moment to ask — after this, cost is being incurred.*
   - Time cap per traversal
   - Auth: is there a wall, and where? Confirm the human-in-the-loop pause
   - Output destination — default `~/.understudy/runs/<slug>/`
   - **Scope exclusions** — anything that must NOT be reported as a finding *(precedent from the reference skill: an identity-proxy gate in front of the product is infrastructure, not a UX defect)*
4. **Echo the plan back** — assessment type, modes, traversals required, lenses per mode, estimated wall time. Wait for go.
5. **Offer to save:** *"Save this target for next time? Goes to `~/.understudy/targets/<slug>.yaml`, outside the repo, gitignored. Credentials are never saved."*

---

## 5. Auth contract

**The agent never handles a credential.** Not from a file, not from an env var, not from the user in chat.

```
→ [persona] traversal — auth wall detected at <url>
⏸  PAUSED — authenticate in the open browser, then confirm
→ [persona] traversal — resuming at <path>
```

Two rules inherited from the reference skill, both load-bearing:
- **The auth wall is never a finding.** It is infrastructure — excluded from all scoring and from the exec summary.
- **The persona never drives an identity provider's UI.** It stops at the wall and hands over.

---

## 6. Lens specification

A lens is one agent file plus one reference. That is the entire extension surface.

```yaml
---
name: lens-<slug>
description: <when the orchestrator should invoke this>
mode: A | B | C | D
model: inherit | opus | sonnet | haiku   # confirmed by the user at onboarding
---
```

Body: the framework, the severity rubric, the output schema, the evidence rule.

### Two invariants — never relax these

1. **Naive/analyst separation.** The traversal agent never sees the framework. Banned during capture: *heuristic · severity · usability · Nielsen · HAX · P0/P1/P2/P3*. Contaminating the traversal is how you get a report that confirms its own priors. This is the single most valuable thing the reference skill proved.
2. **Every finding cites evidence.** No screenshot, log line or DOM excerpt → the finding is dropped. No exceptions, including for findings that are obviously true.

### Model policy

**What the harness can and cannot control** — this is a mechanism constraint, not a preference:

| Level | Who sets it | How |
|---|---|---|
| **Session model** (runs the traversal) | **The user, only.** `/model`, or config. | understudy cannot change it. It can read it, report it, and recommend — nothing more. |
| **Subagent model** (runs each scoring lens) | **The harness.** | `model:` in the lens agent's frontmatter (`inherit` · `opus` · `sonnet` · `haiku`), overridable per run via the `Agent` tool's `model` parameter. |

**Traversal runs in the main session and therefore at the session model.** This is forced by §5: the auth pause hands the open browser to a human, and a subagent cannot perform that handover. Traversal cannot be pinned.

Two consequences the spec must not paper over:

- **"Traversal always gets the strongest model" is a recommendation, not a guarantee.** Pre-flight surfaces the session model and says plainly that traversal is the irreversible part — the persona is deciding what to do next, and a weak journey cannot be rescued by good scoring. Then it asks. **Check and ask; never switch.**
- **"Strongest available" is not expressible in frontmatter.** The field takes literal model names, not a ranking. A pin means *that model*, not *the best one* — so a hardcoded pin silently downgrades a session running something newer. Prefer `inherit` plus an explicit confirmed choice over a pin that ages badly.

**⚑ Lens files never use `inherit`.** The official plugin guidance recommends `inherit` as a default; understudy deliberately does not follow it. `inherit` resolves to the *session* model, which silently re-couples the two levels: a user on a cheap session model would receive cheap scoring while believing they had chosen `balanced`, and the manifest would record a model nobody selected. The independence of the two levels is the entire point of this section, so lens frontmatter always names a model explicitly.

**Resolution happens at onboarding, not in the lens file.** This keeps explicit naming from ageing badly:

- The lens's `model:` frontmatter is a **declared default** — documentation and fallback, not the operative value.
- The **orchestrator always passes an explicit `model` to the `Agent` tool at call time**, taken from the user's confirmed choice in the target file.
- The onboarding shape (*thorough · balanced · cheap*) resolves to concrete model names **against what is available at that moment**, so a newer model is picked up by the shape without editing six lens files.

Net effect: no silent coupling, no stale pins, and the manifest records a model the user actually chose.

**⚑ The user confirms both levels during onboarding, before any cost is incurred.** Defaults are offered, not assumed — an evaluation is a real spend, and whether to spend more on scoring or less is the user's call, not the harness's. See §4, step 5a.

**Default scoring allocation** (offered, overridable per lens): opus for `ux` · `content` · `onboarding` · `compare` — judgement-heavy, where a weaker model produces plausible findings that are wrong. sonnet for `bugs` · `seo` · `aeo` — closer to extraction against a checklist, where the framework does the work.

**⚑ The run manifest records the model used for the traversal AND per lens.** Findings are not comparable across models; a cross-model diff must be flagged, never silently presented. The traversal model matters most here, because it is the one that changes without anyone deciding it — a user who switched models between Tuesday and Friday has two runs that cannot be honestly diffed.

### Stable finding IDs — build in Phase 2, not later

Every finding carries `hash(lens + flow + normalized-locator + normalized-title)`.

⚑ **The locator may be inferred, and inference is part of the tooling.** When a lens omits an explicit locator, `check_report.py` derives one from the report text — the first `/path`, else the first artifact its regex matches. Changing that derivation re-IDs findings nobody edited, and a `--since` diff across the change is noise dressed as findings. Observed 2026-09-04: widening the artifact extensions to accept Mode-C `.html`/`.txt` evidence re-IDed an existing finding. **Treat any change to locator inference as a schema migration** — re-ID existing runs deliberately and record it. Lenses avoid the problem entirely by passing `--locator` explicitly, which is why the output contract calls it the trap.

This enables `understudy report --since <run-id>` → **new · persisting · resolved**. **It cannot be retrofitted** — findings written without stable IDs can never be diffed against findings written with them. Everything else about diffing is cheap whenever you want it; this part is not.

---

## 7. What never enters this repo

By construction, not by discipline:

- Product names, URLs, or any real target
- Credentials, tokens, cookies, session state
- Personas derived from real customer research
- Pricing, marketing copy, commercial terms
- Output paths that reveal a filesystem or an employer
- Screenshots or traces from any real run

`examples/target.example.yaml` uses a **fictional** product. If a real product name would make an example clearer, the example is wrong.

Everything real lives outside the repo:

```
~/.understudy/
├── targets/<slug>.yaml     written only on explicit confirmation
├── runs/<slug>/            default output
├── profiles/<slug>/        browser profiles
└── creds/                  USER-CREATED ONLY. The agent never writes here.
```

`.gitignore` must cover `**/targets/`, `**/runs/`, `*.env`, `*.png`, `*.webm`, `*.zip` from day one — before the first commit, not after.

---

## 8. Repo layout

```
understudy/                              (public, MIT)
├── .claude-plugin/marketplace.json      one repo = one marketplace
├── CLAUDE.md                            this file
├── README.md                            install + first run
├── LICENSE                              MIT
├── .gitignore
└── understudy/
    ├── .claude-plugin/plugin.json
    ├── commands/
    │   ├── run.md      ✅               entry point: onboarding → orchestrate
    │   ├── report.md   ✅               re-score existing evidence; --since for diffs
    │   └── compare.md                   Mode D entry point
    ├── agents/                          one per lens — the Pass-2 scorers
    │   ├── lens-ux.md ✅   lens-bugs.md ✅   lens-onboarding.md ✅
    │   ├── lens-content.md ✅
    │   ├── lens-clarity.md  lens-conversion.md  lens-trust.md    (3a)
    │   ├── lens-seo.md      lens-aeo.md         lens-technical.md (3b)
    │   └── lens-compare.md                                        (3c)
    ├── skills/
    │   ├── onboarding/                  the interview                    ✅ built
    │   ├── traversal-journey/           Mode A capture                   ✅ built
    │   ├── traversal-visit/             Mode A-visit capture             (3a)
    │   ├── traversal-crawl/             Mode C crawl                     (3b)
    │   ├── traversal-measure/           Mode B technical metrics         (3b)
    │   └── traversal-compare/           Mode D orchestration             (3c)
    ├── references/                      [M] methodology, ported from reference skill
    │   ├── playwright-patterns.md ✅  flow-shapes.md        ✅
    │   ├── first-value.md         ✅  evidence-rules.md     ✅
    │   ├── heuristics-framework.md ✅ severity-rubric.md    ✅
    │   ├── report-template.md     ✅
    │   ├── visit-shapes.md            land→orient→evaluate→decide  (3a)
    │   └── technical-metrics.md       the §3.1 set + lab caveat    (3b)
    ├── scripts/
    │   ├── render_report.py ✅  md → self-contained HTML / PDF; stdlib only
    │   ├── init_run.py     ✅   creates run folder + manifest at run START
    │   ├── check_capture.py ✅  phase-2a gate: checks 2 + 5, mechanically
    │   ├── finding_id.py   ✅   stable IDs + self-test
    │   ├── check_report.py ✅   phase-2b gate: checks 1, 3, 4, 6 + 7
    │   ├── close_run.py    ✅   closes the manifest at run END — captures,
    │   │                        findings, finished_utc, all read off the disk
    │   └── compare_runs.py      Phase 4 — new/persisting/resolved + overlap %
    └── examples/                        fictional product only
        ├── target.example.yaml ✅   sample-findings.md ✅
```

---

## 9. Publishing to GitHub

The repo **is** a Claude Code plugin marketplace. Users install with two commands.

1. **`.claude-plugin/marketplace.json`** at the repo root — name `understudy`, owner block, one entry in `plugins[]` with `"source": "./understudy"`. Model it on `~/.claude/plugins/marketplaces/pm-skills/.claude-plugin/marketplace.json`.
2. **`understudy/.claude-plugin/plugin.json`** — name, version, description, author, keywords, homepage, `"license": "MIT"`.
3. **`LICENSE`** — MIT. A permissive licence keeps the tool usable wherever it is needed, with the fewest questions asked. The file carries `Copyright (c) 2026 Dario Bianchi`.

   Product-specific material never ships (§7), so what this repo licenses is the harness and the methodology, not any evaluation performed with it.
4. **`README.md`** must carry:
   - What it is, in two sentences
   - Install:
     ```
     /plugin marketplace add dariobianchi00/understudy
     /plugin install understudy
     ```
   - First run: `/understudy run`
   - **The Playwright MCP prerequisite, stated prominently** — including the two version-dependent quirks: the older-version `browser_resize` numeric-argument bug (with the `setViewportSize` fallback, and the point that the *verification* is what matters), and the fact that the server confines writes to its own output roots so screenshots must transit and be moved. See §11 risk 1.
   - The lens table and how to add one
   - An explicit "this tool never stores your credentials or product data" section — it is the main thing a client will ask about
5. **Version from v0.1.0.** Tag releases; the marketplace resolves against the repo.
6. **Public from the first commit.** There is nothing sensitive in the repo by construction (§7), and a repo that starts private and flips public is exactly how secrets end up in git history.

---

## 10. Design decisions worth keeping

The build sequence that produced this repo has been deleted, as §10 always said it would be once the work shipped. Four decisions from it are load-bearing and are recorded here so they are not undone by someone who wasn't there.

**Capture and scoring are separate deliverables, not two halves of one step.** Capture failures and scoring failures look nothing alike, and one gate for both makes a red light ambiguous. Because they are separate, scoring re-runs against saved artifacts for free — no browser, no time cap — which is what makes lens iteration cheap. It also makes the naive/analyst separation *structural*: the capture cannot see a framework that is not loaded.

**The gate is structural, not statistical.** "Reproduces a known-good set of findings" cannot be evaluated — run-to-run variance is large enough that a near-miss is indistinguishable from ordinary noise (see §11.8, and the measured figure in the README). So the gate checks what the harness is actually responsible for: evidence cited, separation held, no unsupported P0, IDs reproducible, manifest complete, verdict first. All six are mechanically checkable against one run's artifacts.

Plus one human check that is not automatable and should not pretend to be: **read the exec summary. Is it sign-off-ready without rewriting?**

**Website assessment before reproducibility.** Website runs are cheap, need no auth, and carry no destructive-action hazard, so they exercise the harness at low cost — and they make a self-overlap baseline affordable, because a 20-minute visit costs a fraction of a 90-minute product traversal.

**`compare` shipped with the website bundle, not after it.** A site audit that cannot answer *"how do we look next to them?"* is answering the easier question. Website assessment is also the only place Mode D genuinely works: there is no auth wall to human-in-the-loop past.

---

## 11. Known risks

8. **⚑ Individual findings are not reproducible. Themes are.** Measured 2026-09-04: scoring byte-identical evidence twice, with the same lenses on the same models, gave **30.4% overlap** matched by similarity and **1.7%** by exact finding ID. P0+P1 overlap was 42.9%, and one finding scored P0 in the first run and P1 in the second.

   Both runs saw the same things. What varied was how observations were grouped, worded and scored — a lens chooses which observations become findings, and that choice is not stable.

   **Consequences, all of them load-bearing:**
   - **`report --since` cannot rely on hash equality.** `compare_runs.py` matches on similarity as well as ID and prints both numbers, so a rewording reads as *reworded* rather than as churn. An earlier claim that ID normalisation made rewordings safe was wrong; this measurement is what caught it.
   - **Do not tighten ID normalisation to force rewordings to collide.** Stripping enough words to merge two phrasings also merges genuinely different findings, which hides a new problem inside an old one — the worse error.
   - **The README publishes the number.** A tool that says how much it disagrees with itself is more trustworthy than one that does not mention it, and a user who treats a single P1 as a verdict is over-reading the output.
   - **Severity is the least stable field.** Anything that turns on a single severity — a threshold, an alert, an SLA — is building on sand.


1. **⚑ The core dependency is flaky and this repo is public.** Playwright MCP failed to connect on 2026-09-02. Publishing a tool whose main dependency breaks and needs an undocumented workaround makes you the support desk. **Mitigation: hard pre-flight check with an explicit "this is upstream, here is the workaround" message, and say so in the README.**

   ✅ **Partly revised 2026-09-04 after the first real run.** Two corrections, both from observation rather than inheritance:

   - **The `browser_resize` bug did not reproduce.** `browser_resize(1440, 900)` worked and internally called `setViewportSize`. The bug is real in *some* versions, so the fallback stays — but the docs now state it as version-dependent rather than as a fact about the tool, and the run-code tool's name varies (`browser_run_code` / `browser_run_code_unsafe`). **The load-bearing rule was never the workaround; it is the `browser_evaluate` verification, which runs on every path.**
   - **A quirk the reference skill did not document: the server confines file writes to its own output roots.** An absolute path into `~/.understudy/runs/` is refused, so screenshots and console/network dumps must be captured with a plain filename and moved immediately. The transit directory sits inside this repo, which makes §7 hygiene an active step (`rm -rf .playwright-mcp`, verify `git status` clean), not merely a `.gitignore` entry.

   *General lesson worth keeping: an inherited caveat is a hypothesis about a dependency, and it ages. State the version and the date, keep the fallback, and make the verification — not the workaround — the thing that always runs.*
2. **"Generic" is doing a lot of work.** ✅ Mitigated by the persona fork (§4). *Residual: nothing stops a user choosing generic every time and trusting the output anyway.*
3. **AEO is half a product not yet built.** ✅ **Settled 2026-09-02: v1 ships the static half only** — schema.org coverage, extractable answer blocks, entity clarity, `llms.txt`. Querying live answer engines (rate limits, non-determinism, per-query cost) is out of v1 and budgeted separately. **This must be stated explicitly in both `lens-aeo.md` and the README** — a missing half that is named is a scope decision; an unnamed one is a bug report waiting to happen.
4. **Mode D multiplies everything, and competitors have their own auth walls** you cannot human-in-the-loop past without accounts. **Mode D is realistically logged-out-only for competitors.** ✅ Largely resolved by scoping: website assessment (§3) is logged-out by nature, so this is where `compare` actually works and where it now ships (Phase 3c). *Residual: `compare` on two logged-in products remains out of reach, and the README must say so — a user who compares two marketing sites successfully will reasonably expect to compare the products behind them.*

6. **⚑ Lab metrics read as field metrics.** The Mode B `technical` numbers are one measurement from one machine on one connection. They are sound evidence about the page and no evidence at all about what users experience. A report presenting a lab LCP as "your users' LCP" is confidently wrong, and that error discredits every other number beside it. **Mitigation: the caveat sits in the report body, not a footnote; mobile and desktop are measured and reported separately; §3.1 states the limit.**

7. **Website assessment looks cheap, so it will be over-trusted.** A 20-minute visit traversal costs a quarter of a product run, which invites running it casually and treating the output as equivalent. It is not — a visitor traversal sees the pages a visitor sees and nothing behind them. **Mitigation: the report states what was and was not reached, and `clarity` never speculates about a product it did not open.**
9. **⚑ A manifest written at the start is only half a manifest.** `init_run.py` deliberately writes it at run start, so it records what ran rather than what someone remembers — but nothing ever wrote the other half, and every run on disk claimed `phase: 2a-capture`, `finished_utc: null`, `captures: {}`. Four completed runs, all lying about themselves. Since `report --since` compares runs by what their manifests say they contain, an unclosed run cannot be honestly diffed, and the failure is silent.

   **Fixed 2026-09-05 by `close_run.py`**, which keeps the same principle: every field is read off the disk, never taken from the caller. `finished_utc` comes from the newest evidence or findings file, not the wall clock — excluding exports, so re-rendering a report months later cannot move the date a run finished. `check_report.py` warns while a manifest is still open, because the gate is the last thing that runs and the thing nobody skips.

   *General lesson: a field that nothing writes and nothing reads is not a field, it is a comment. Either populate it or delete it — a schema that lies is worse than one that is missing.*

5. **Seven lenses can produce a great deal of unread output.** The report template must force a one-sentence verdict and a top-3 before anything else. The reference skill did this, and it is why its exec summary was usable. **Enforced by gate check 6 in `check_report.py`** — this mitigation is a gate, not an intention.

   ✅ **Extended 2026-09-04, after the first real run made the risk concrete.** A 3-lens run produced 39 findings of which ~25 were distinct: `bugs` contributed 3 findings `ux` did not have, and `onboarding` contributed none (its value was the funnel, not its findings list). Verdict-first was being applied *per lens*, which multiplies the problem it was meant to solve — four competing exec summaries for three lenses, eight for seven.

   Settled output contract:

   - **Lens reports stay standalone and are NOT deduplicated against each other.** Each is read alone by a different audience. Overlap is the price.
   - **Overlap is reconciled once, at the run level, as corroboration** — "flagged independently by ux, bugs and onboarding". The lenses never read each other, so agreement is real signal rather than an echo, and this is the only layer that can observe it. One slot in the top 3, never three.
   - **Cross-lens ranking is legitimate** because `severity-rubric.md` is shared and lens-agnostic — P0–P3 are defined by user impact, not by lens. Merging or re-scoring another lens's finding is not.
   - **House style is binding on every line of every report:** conclusion first, bullets, no prose paragraphs, ≤25 words per bullet, numbers over adjectives. Concision applies to the *reasoning*; evidence, repro steps and severity are never compressed.
   - **Run-level exec summary always exists**, roughly one page per lens run (soft).
   - **Markdown is canonical; export is a copy.** Offered every run — HTML or PDF, scoped to summary / one lens / everything. HTML is self-contained with screenshots embedded beside the findings citing them, because a report whose evidence dies when forwarded is worse than one with no evidence: it still looks complete.

   ✅ **Extended again 2026-09-05, after the first assessment sent to a client.** The content passed; the *artifact* read as generated. Seven corrections, all in `render_report.py` and the templates, none in the lenses:

   - **A table must be allowed to break across pages.** `break-inside:avoid` on `table` stranded ~3.5 blank pages in 15, because a long table that does not fit is pushed whole to the next page. Rows stay atomic, `thead` repeats, and the forced page break per lens is gone — a running heading tells a reader where they are, a blank half-page does not.
   - **Lens sections are ordered by severity weight, not alphabetically.** `sorted(os.listdir())` put `aeo` — the most niche check — first, and `trust` with 8 P1s last. A reader who stops halfway must have read the important half.
   - **`Fix` is rendered, so it is client-facing.** The lenses always wrote it; the export dropped it. Sixty findings with no recommended action is the thing a client is paying for, sitting unused on disk.
   - **The summary export carries screenshots.** Evidence that lives only in the full export is evidence the deliverable's reader never sees, which quietly turns invariant 2 into a promise rather than a property.
   - **Cross-lens corroboration is computed as well as written.** Pairing on a shared verbatim quotation, or a similar title at the same locator, turns four separate reports of one problem into one finding with three witnesses. It annotates only — never merges, re-scores or drops (§11.8). The orchestrator's own count stays authoritative.
   - **Folder names are not report headings.** `aeo` identifies a directory; "Answer-engine readiness" is what a client reads. Likewise no run-folder path appears in prose the client sees.
   - **A cover page carries the caveat.** Assessment type, scope, buyers, checks, severity tally — and, when `persona_mode` is `generic`, the inferred-persona warning on the front page rather than on page 6 (§11.2).

   *Page numbers are the one thing not fixed: Chromium ignores CSS page-margin boxes and its built-in footer stamps the source `file://` path, which §7 forbids. Numbered sections and findings serve the same purpose and survive a change of paper size.*

   ✅ **Reshaped again 2026-09-05, on the same client's reading of it.** The production fixes above held; what changed is the document's shape and what it now claims.

   - **⚑ Reading order is FIXED, not computed.** `LENS_ORDER` — Clarity · Conversion · Trust · Compare · SEO · AEO · Technical, then Usability · Defects · Activation · Content. Severity-weighted ordering lasted a day: a reader cannot predict where a section lives, and two runs of one site ordered differently cannot be read side by side. **The summary's own "what each check looked for" table must use this order** — the two disagreeing is the bug the fixed order exists to prevent.
   - **The run summary opens with a description, not a verdict.** Two or three lines saying what the product actually is, for a reader who has never seen it; a verdict about something they cannot picture is unusable. The verdict moves to the head of the Top 5, directly above its evidence. **Gate check 6 now applies to lens summaries only** — they are read by people who already know the product.
   - **Top 5, always five, drawn from every check.** Ranked by severity with P0s first and filled from P1 when a run has fewer than five P0s, never padded with P2/P3. A corroborated finding still takes one slot, not four.
   - **⚑ Every check publishes a 0–10 score, and the lens assigns it.** Only the agent that read the evidence can defend a number, so it writes `- **Score:** N/10 — why` in its own summary. **Gate check 7 refuses a score its severities contradict** (>5 with a P0, >7 with a P1, >9 with a P2) — a loose ceiling that catches the indefensible without relitigating a judgement. The overall is the mean, computed by the renderer and never authored, so the cover and the table cannot disagree.
   - **Sections are numbered by the renderer and the index is generated.** Numbering by hand drifts the moment a section is inserted. Three headings are written empty and filled from what actually ran — Contents, How each area scores, Raised by more than one check — so none of them can contradict the document around them. Internal anchors survive Chromium's PDF export as GoTo annotations (verified), so the index is clickable in the PDF.
   - **Severity is one component everywhere:** emoji, bold, colour — 🔴 P0 · 🟠 P1 · 🟡 P2 · ⚪ P3. Emoji only for severity; a client forwards this to a board, and icons on headings buy scanability at the cost of being taken seriously.
   - **Three sections deleted.** "Recommended first action" (the ranked Top 5 already is one, and two copies drift), "technical facts worth separating out" (technical belongs to the Technical check), and the body severity tally (the cover carries it).
   - **⚑ The site-by-site matrix closes the report, lifted whole.** `compare` already builds a `## Differences matrix` with every competitor's own observed value; only the export was dropping it, so the summary could say the site *trailed* without ever showing what the other three did — an unfalsifiable claim in the one section whose whole purpose is comparison. The renderer now appends it verbatim as the final numbered section. **Never re-typed:** it is built from N separate captures, and a hand-copied second version is how one number comes to differ between two pages of one document. Chromium honours named pages with their own orientation (verified 2026-09-05), so it gets a landscape page and a four-site matrix stays legible.

---

## 12. Migration inventory

Lives in `BUILD_NOTES.local.md` §3, not here — the table names real paths and a real
product, which §7 forbids in this file.

It also carries the **scrub rule**: the reference skill hardcodes four persona names
and a product name. Grep every ported file for both before it lands in this repo. A
ported file that still names a persona or a product is a bug, not a detail.
