# cardinal-design

The shared, CSS-only design system for CardinalCore apps. The package owns the
versioned CSS and showcase; consumers pin a released git tag or vendor a
specific file. See [README.md](README.md) for the class reference and
consumption patterns.

## Load-bearing rules

- `cardinal.css` imports `tokens.css`, then `components.css`; there is no build
  step or JavaScript package.
- Consumers use a git tag, never `main`. A tag must be pushed before a
  jsDelivr URL is given to a consumer; verify the CDN pin before bumping an app.
- `tokens.css` is the token source of truth, including the `.cds-dark` scope.
  TopLeaseMap vendors it and must re-copy the whole file on a tag bump.
- `components.css` contains the shared `cds-*` grammar. TopLeaseMap vendors
  its Card section as `src/cardinal-cards.css` when its repo guidance requires it.
- Run `python docs/superpowers/tools/contrast.py` for palette changes; both the
  light layer and `.cds-dark` must exit 0.

The dark-scope rationale is in
`docs/superpowers/specs/2026-08-25-dark-scope-v6-design.md`. Current package
priorities are maintained by the workspace and consuming repos.
