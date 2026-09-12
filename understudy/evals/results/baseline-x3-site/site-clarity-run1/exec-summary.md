# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Neither visitor could say what Nimbus Notes is from the page itself — both guessed "notes app" from the name, neither learned who it is for, and the one button that would have shown the product does nothing.

## Top 3
1. **[P0] Fold never says what Nimbus Notes is; both personas guessed 'notes app' from the name** — time-to-comprehension is `null` for both; the headline "Your thoughts, everywhere." names no category (evaluator, sceptic)
2. **[P1] Hero subhead is two undefined terms: 'bi-directional sync graph' and 'zero-knowledge vault'** — the only explanatory sentence above the fold was unreadable; "I'll assume it syncs" (evaluator)
3. **[P1] 'See it in action', the only route to seeing the product, does nothing on click or tap** — both visitors tried it to understand the product; nothing happened (evaluator, sceptic)

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator | partly (guessed from name) | ✗ | ✗ | never |
| sceptic | partly (guessed from name + friend) | ✗ | partly (saw button; it failed) | never |

## Score
- **Score:** 2/10 — the site never tells a visitor what it is or who it is for; both personas left with guesses and no next step.

## Limits on this read
- **Personas:** evaluator (desktop 1440×900), sceptic (iPhone 13, 390×844) — ⚠ INFERRED (generic)
- **Not reached:** `/features.html` content (404 for evaluator); Pricing and Features never opened on mobile
- **Excluded:** none (auth wall always)
- **Models:** traversal `fixture-hand-authored` · scoring `opus`

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never | at risk (interest lost 01:25) | Fail | Partial ("close but off") |
| sceptic | never | at risk (interest lost 00:30) | Fail | Fail ("no") |

- Jargon the visitor could not define: "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology", "card" vs "blocks" vs "graph" vs "vault".
- Point of lost interest — evaluator 01:25 at anonymous "Loved by teams" quotes; sceptic 00:30, straight to footer after the cookie bar.
- Clearest product copy on the site is the About FAQ (offline, export, Frankfurt), two clicks from landing.
- Mobile fold clips the H1 to "Your thoughts, everywh" and the subhead mid-word.

## Severity flips
- None; both personas failed what and who identically. Next step: evaluator ✗ (no obvious control), sceptic partly (found the button; it did nothing) — same finding, not a flip.

## Next action
- Rewrite the fold: an H1 that names the category and audience in plain words, a subhead without "graph"/"vault", and a working "See it in action" that shows a note syncing.
