# cardinal-design

The design system every CardinalCore app consumes: `cardinal.css`,
`tokens.css`, `components.css`, one shared visual language for
TopLeaseMap, LeaseIndex, and CharlieBot.

## Consumption model

Apps pin a jsDelivr CDN URL to a git tag (`@v5.0.0`), or vendor
`tokens.css` in directly (TopLeaseMap does this for its token layer).
See README.md for both patterns.

## The hard rule

A tag must be pushed before any consumer pins it. An unpushed tag is
a 404 on the CDN pin. Never hand a consumer app a tag that only exists
locally.

## Workflow

Spec, then plan, then tag, then bump consumers. Write the spec in
`docs/superpowers/specs/`, the plan in `docs/superpowers/plans/`, make
the change, tag it, then go update the pinned version in each
consuming app. No app auto-follows a moving target.

## Where to look

- README.md — the class reference and the versioning policy.
- `docs/superpowers/tools/contrast.py` — run this to verify any
  palette change holds WCAG contrast before it ships.
