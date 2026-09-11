# Banned vocabulary during capture

**[M] methodology.** The one list. `check_capture.py` reads it from this file;
`flow-shapes.md` and `visit-shapes.md` point here rather than keeping copies.
Observed 2026-09-11: the two shape files listed 19 terms and said "checked
mechanically", the script checked 14. A list that lives in two places is two
lists.

**Why:** a persona who writes in the analyst's vocabulary has seen the
analyst's framework, and the report then confirms its own priors (CLAUDE.md
§6, invariant 1). The persona may say *"this was hard to use"* or *"I couldn't
find the price"*. They may not say *"a P2 usability issue"* or *"the CTA is
below the fold"*.

**How it is checked:** whole-word, case-insensitive, in `session.log`,
`persona-debrief.md`, `findings-raw.json` and Mode D's `reading.md`. A hit
inside a URL-shaped token (`/plans/p1`) is ignored — that is a page the persona
visited, not a word they chose. Quoted page text is **not** exempt. A run may
waive terms via `vocabulary_allowlist` in the target file — for a product whose
own navigation says "Usability" — and the gate prints every waiver.

**One hit fails the gate. The fix is to re-run the traversal, never to edit
the words out.**

## The list — one term per line, `- term`

- heuristic
- nielsen
- hax
- amershi
- severity
- p0
- p1
- p2
- p3
- usability
- ux
- wcag
- accessibility audit
- activation funnel
- conversion funnel
- ttfv
- friction
- cta
- above the fold
