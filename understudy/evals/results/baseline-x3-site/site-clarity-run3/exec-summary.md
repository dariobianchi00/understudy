# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Neither visitor could say what Nimbus Notes is from the page itself — both guessed "a notes app" from the name, nobody learned who it is for, and the clearest explanation on the site is buried in the About FAQ.

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator (desktop 1440×900) | ✗ (guessed from name) | ✗ | ✗ | never |
| sceptic (iPhone 13) | ✗ (guessed from name + friend) | ✗ | partly | never |

## Top 3
1. **[P0] Neither visitor could say what Nimbus Notes is from the page; both guessed from the name** — `time_to_comprehension_seconds: null` for 2/2 personas; the site's first job never happens (evaluator, sceptic)
2. **[P1] Hero subhead "bi-directional sync graph with a zero-knowledge vault" undefined for both visitors** — the only descriptive line above the fold is two terms the visitor cannot parse (evaluator, sceptic)
3. **[P1] Clearest description of the product sits in the About FAQ, two clicks from the home page** — "works offline, syncs, exports Markdown" is the answer; it is on /about.html, not / (evaluator, sceptic)

## Score
- **Score:** 2/10 — 2 of 2 visitors never understood what the product is or who it is for; the one page that explains it is About, and the one button that would show it does nothing

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic). Findings rest on personas the run invented, not researched users.
- **Not reached:** /features.html (404 for evaluator; sceptic never tried); demo form never submitted; sceptic never opened Pricing
- **Excluded:** none in manifest — auth wall always excluded
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never | not reached | Fail | Partial ("close but off") |
| sceptic | never | not reached | Fail | Fail ("no") |

- Point of lost interest — evaluator 01:25 (anonymous "Loved by teams" quotes, `01-scrolled.png`); sceptic 00:30 (went straight to footer, `00-landing.png`)
- Terms neither persona could define: "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology", "card" vs "blocks"
- Sessions: evaluator 6.5 min, 5 pages, 5 unanswered questions; sceptic 2.9 min, left early, 3 unanswered questions

## Severity flips
- **Next step:** evaluator `understood_next_step: false` (newsletter box outweighs the CTA, P2); sceptic `true` — same fold, one persona read the CTA and one did not. Flagged as ce97b8a98b83, evaluator only.
- All other findings land at the same severity for both personas.

## Next action
- Rewrite the hero so the headline and subhead say "notes app that syncs across your devices and works offline" in plain words, name the audience, and move the About FAQ answers onto /.
