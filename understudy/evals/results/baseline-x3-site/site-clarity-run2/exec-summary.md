# Nimbus Notes — clarity — Run 2026-09-08 (fixture01)

Neither visitor ever learned from the site what Nimbus Notes is — both guessed "notes app" from the brand name, and the one button that might have shown them does nothing.

## Top 3
1. **[P1] Headline never says what the product is; both visitors guessed from the name** — time to comprehension is `null` for 2 of 2 personas; everything they "knew" came from the logo and a friend (evaluator, sceptic)
2. **[P1] The only path to seeing the product, "See it in action", does nothing** — 3 clicks/taps across 2 personas, zero response; the promise "remembers everything" is never demonstrated (evaluator, sceptic)
3. **[P1] Features nav link returns a 404 where the product explanation should be** — the visitor looking for "what does it do" hits "File not found" (evaluator)

## Comprehension
| Persona | What is it? | Who's it for? | What next? | Time to understand |
|---|---|---|---|---|
| evaluator (desktop 1440×900) | ✗ — guessed from name | ✗ | ✗ — newsletter box louder than CTA | never |
| sceptic (iPhone 13) | ✗ — guessed from name + friend | ✗ | partly — saw the button; it did nothing | never |

## Score
- **Score:** 3/10 — two of two visitors left without the site ever telling them what it is, who it is for, or showing it working; the real answers exist but sit on About and a 404.

## Limits on this read
- **Personas:** evaluator, sceptic — ⚠ INFERRED (generic). Findings rest on personas the run invented, not researched ones.
- **Not reached:** /features.html (404 for evaluator; never attempted by sceptic); no logged-in surface
- **Excluded:** none in manifest — auth wall always
- **Models:** traversal `fixture-hand-authored` · scoring `opus`
- Hero image in every capture carries a leaked placeholder caption ("…a real capture serves assets/generated/hero.png…") — treated as fixture artefact, not scored.

## Numbers
| Persona | TTFV | Reading | Self-explanatory | Promise match |
|---|---|---|---|---|
| evaluator | never | not reached | Fail | Partial — "close but off" |
| sceptic | never | not reached | Fail | Fail — "No" |

- Point of lost interest: evaluator 01:25 (anonymous testimonials on screen); sceptic 00:30 (hero — went straight to footer)
- Undefined terms quoted by personas: "bi-directional sync graph", "zero-knowledge vault", "workspace type", "sync topology", "card" vs "blocks"
- Session length: evaluator 6.5 min; sceptic 2.9 min, left early

## Severity flips
- Phone-width clipping (`beb91f02fa77`) hit only the sceptic — at 390px the headline and subhead are cut off mid-word; at 1440px they render whole. Not a flip in judgement, a device-only defect.
- No behaviour scored differently across the two personas where both met it.

## Next action
- Rewrite the hero to one plain sentence — what it is, who it is for — and make "See it in action" open something.
