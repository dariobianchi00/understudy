---
description: "Compare a website against user-supplied competitors — same lenses, same method, then a differences matrix"
argument-hint: "[target-slug or site URL]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill", "Task"]
---

# understudy compare

Run the same assessment across your site and 1–3 competitors, then diff them.

**Argument (optional):** "$ARGUMENTS" — a saved target slug, or your site's URL.

---

## What this command does

1. **Pre-flight** — the browser dependency, same as `/understudy:run`.
2. **Confirm the competitor set** — user-supplied, always.
3. **Capture each site independently**, then score each independently.
4. **Diff** — one matrix.

**Mode D is logged-out only.** Marketing sites, public pages, no accounts anywhere. This is where `compare` genuinely works and it is why website assessment is where it ships.

---

## Stage 1 — Pre-flight

Same as `/understudy:run` Stage 1: confirm Playwright MCP responds, report the session model, and stop rather than approximate if the browser is unavailable.

---

## Stage 2 — The competitor set

**⚑ Competitors are user-supplied. Never inferred, in any circumstance.**

If the target file already lists them, echo them back and confirm they are still the right set — a target saved three months ago may name a competitor who has since pivoted.

If it does not, ask for 1–3 URLs. **"None" is a valid answer**: say plainly that `compare` cannot run, and offer a single-site website assessment via `/understudy:run` instead.

> A wrong competitor set produces a confident, useless comparison. The user is the only one who knows whether the site they worry about is the obvious one or the one nobody names — and a plausible guess is indistinguishable from a real answer once it is in the matrix.

Then confirm the shape and its cost, because **Mode D multiplies everything**:

```
compare — 3 sites
  capture   3 × Mode A-visit  (25 min cap each)   ≈ 75 min
  scoring   3 lenses × 3 sites, in parallel        ≈ 25 min
  diff      1 pass                                 ≈ 10 min
                                                   ─────────
                                                   ≈ 1h 50m
```

Wait for an explicit go.

---

## Stage 3 — Capture, one site at a time

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/init_run.py --target ~/.understudy/targets/<slug>.yaml \
                    --traversal-model "<session model>"
```

Then invoke the **`traversal-compare`** skill. It owns the capture contract:

- **Fresh context per site, logged out**, the user's site first.
- **Identical method across sites** — same persona, device, cap, coverage depth. Any asymmetry invalidates the comparison, and nothing in the output will reveal why.
- **No account is created anywhere. No form is submitted anywhere.** On a competitor's site a submitted form is a real lead in a real CRM — a cost imposed on a business that did not ask to be tested.
- **No persona ever sees two sites.**

Verify each capture as it lands:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check_capture.py <run_folder>
```

---

## Stage 4 — Score each site independently

Fan out the run's lenses over **each site's capture separately**, exactly as a single-site run would. Site A's `clarity` agent never sees site B's evidence.

**Pass the model explicitly** from `manifest.json`. As in `/understudy:run`, **check the files actually landed** — some hosts block subagent writes, and a lens that returned text needs persisting by you.

---

## Stage 5 — Diff

Only when every site is captured **and** scored, invoke the `lens-compare` agent.

It is the one lens permitted to read others, and only across sites for the same lens — never merging lenses within a site.

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/check_report.py <run_folder>
```

**Confirm the lens count in the gate output matches what you dispatched.** The gate discovers lenses by directory: a lens whose files never landed is not failed, it is unchecked, and the run still prints `PASSED`.

---

## Stage 6 — Hand over

Run-level `exec-summary.md` follows the `/understudy:run` §3.6 template like any other
run — description first, then the Top 5. **Do not paste the matrix into it:**
`render_report.py` lifts the `## Differences matrix` from `compare/exec-summary.md` and
appends it as the report's closing section on its own landscape page, so a copy in the
summary is a second version of a table built from N captures. Then offer the export — **PDF or HTML**, scoped to **summary · one lens · everything** — via `render_report.py`.

**State on the face of the report that only public websites were compared.** A reader who sees a successful marketing-site comparison will reasonably assume the products behind them were compared too. They were not, and they cannot be: you cannot human-in-the-loop past a competitor's auth wall, and creating an account on their product to try is not something this tool will do.

---

## Invariants

1. **Competitors are user-supplied.** Never inferred.
2. **Logged out everywhere.** No account is ever created on a site the user does not own.
3. **Nothing is submitted** — no forms, demos, trials, chat messages.
4. **Identical method across sites.** Equal caps, equal depth, equal persona.
5. **No persona sees two sites.** The contrast is Pass 2's job.
6. **A site that could not be read is `not comparable`**, never a site that scored badly.
7. **Competitor findings are not defects to fix.** They locate your site; they are not a critique of a business that did not ask for one.
8. **Nothing real enters the repo.** All output under `~/.understudy/`.
