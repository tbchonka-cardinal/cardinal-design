# Cardinal Design System

The shared visual language for the CardinalCore app suite (TopLeaseMap, LeaseIndex,
CharlieBot): a layered heritage-parchment system — a warm off-white canvas, crisp
white surfaces raised on soft shadow, a lapis masthead, and brass rings and fills.
Depth comes from three shadow steps, not texture; the faint paper grain lives on the
canvas alone. Type is one system UI sans for everything (numbers in tabular figures);
Garamond is the wordmark alone and Source Code Pro is reserved for code. Apps link one
file, `cardinal.css`, which imports the font, then `tokens.css`, then `components.css`.
No build step. Versioned by git tag. v4 adds the Stripe-craft mechanics: hairline rings
instead of borders, two-tint shadows, a five-size type scale, and a single-accent rule
(brass means actionable). v4.2 sharpens it: near-square radii (3px controls inside 4px
containers), a definite 1px ring, Garamond off everything but the wordmark, and the
chrome color out of card headers. v5.0.0 replaced the chrome ramp outright: lapis in,
oxblood gone, no trace of the old color left anywhere in the suite. v6.0.0 adds the
dark scope: one class, `.cds-dark`, swings the neutral ramp to a warm near-black and
lifts brass and lapis to their light tiers. Nothing else changes with it.

Live showcase: open `index.html` in this repo, or view it hosted once GitHub Pages
is turned on. It renders every token and every `cds-` component with copy-paste
snippets.

## Consumption

Link the whole system (font + tokens + components):

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tbchonka-cardinal/cardinal-design@v6.0.0/cardinal.css">
```

Token-only alternative, for an app that wants the color/spacing/type variables but
keeps its own component CSS:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tbchonka-cardinal/cardinal-design@v6.0.0/tokens.css">
```

Or vendor `tokens.css` into the consuming app's own repo (copy the file in,
comment the version it was pinned at) so the app stays self-contained offline and
in local dev, and pull a fresh copy by hand when you want to bump.

## Versioning policy

- Pin every consumer to a git tag (`@v6.0.0`), never `@main`. jsDelivr caches tags
  aggressively; `@main` will not reliably pick up changes and gives you no way to
  roll back.
- Workflow to change anything: edit the CSS in this repo, tag a new version
  (`vX.Y.Z`), then go bump the pinned tag in each consuming app deliberately. No
  app auto-follows a moving target.
- Non-goals: no JS behaviors, no build pipeline or npm package, no React.
  ("No dark theme" was a non-goal through v5; Thatcher reversed it on
  2026-08-24 and v6.0.0 ships the scope.)

## Dark

Dark is a scope class, not a second stylesheet and not a media query. Put
`.cds-dark` on any element and every color role beneath it rewires onto the warm
dark ramp (`--dk-900` ground through `--dk-0` text). Everything that is not color
holds: same spacing, same radii, same 1px ring weight, same type scale, same
150ms motion.

```html
<div class="cds-dark cds-card"> ... </div>   <!-- one dark card on a light page -->
<body class="cds-dark"> ... </body>          <!-- or the whole app -->
```

Brass stays the only actionable color and lapis stays the chrome. Where either is
text, the scope lifts it to the light end of its ramp (`--gold-deep` becomes
`#D9BC7E`, link hover becomes `#A8C4EA`); where either is a fill or a band, the
value stands. Both layers are gated by `docs/superpowers/tools/contrast.py`.

Two rules for consumers. Route color through a role or a v3 alias, never a
neutral primitive, or the scope cannot reach it. And give the scoped element a
background from `--bg` or `--bg-surface`, because `.cds-dark` sets `color` but a
component's own background rule wins over the scope's.

Details, including every value and why: `docs/superpowers/specs/2026-08-25-dark-scope-v6-design.md`.

## Class reference

| Class | What it is |
|---|---|
| `.cds-dark` | Theme scope: rewires every color role beneath it onto the warm dark ramp. Lives in `tokens.css`, so token-only consumers get it |
| `.cds-card` | Elevated white card container: surface background, hairline ring, soft resting shadow |
| `.cds-card-header` | Raised neutral header band for a card, brass hairline beneath |
| `.cds-card-body` | Padded, scrollable card content area |
| `.cds-card-footer` | White action band completing the three-band edit card; tints the body via `:has()` |
| `.cds-empty` | Dashed-border empty state with a centered muted message |
| `.cds-banner` | Neutral inline notice; `-success`/`-error`/`-warning`/`-info` variants use the feedback tint pairs |
| `.cds-btn` | Base button shape shared by all button variants |
| `.cds-btn-primary` | Brass-glass gradient button, for the main action |
| `.cds-btn-ghost` | White secondary button; its ring darkens and its shadow lifts on hover |
| `.cds-btn-danger` | Solid hot-red button, for destructive actions |
| `.cds-btn-icon` | 28px square icon button for one inline SVG (close, add, edit, menu) |
| `.cds-panel` | Floating white surface with a hairline ring, for sidebars/filters |
| `.cds-table` | Data table: sticky ink-on-paper-2 headers, zebra rows, hairline dividers |
| `.cds-num` | Right-aligned, tabular-numeral table cell for numeric columns |
| `.cds-field` | Wrapper around a labeled form control, sets bottom margin |
| `.cds-label` | Standalone brass (`--gold-deep`) uppercase field label (used outside `.cds-field`) |
| `.cds-input` | Text input styled to the white surface field treatment with a brass focus ring |
| `.cds-select` | Select dropdown styled to match `.cds-input` |
| `.cds-badge` | Small status label on a feedback tint |
| `.cds-badge-success` | Badge modifier, emerald, for a good/synced state |
| `.cds-badge-error` | Badge modifier, brick red, for a failed/error state |
| `.cds-badge-warning` | Badge modifier, amber, for a caution/pending state |
| `.cds-badge-info` | Badge modifier, ink-blue, for a neutral informational state |
| `.cds-badge-muted` | Badge modifier, muted italic, for an empty/inactive state |
| `.cds-pill` | Filter chip on a hairline ring; `.active` marks it with a 2px ink ring |
| `.cds-eyebrow` | Uppercase, letterspaced, brass (`--gold-deep`) section label |
| `.cds-tabs` | Flex row container for a tab strip |
| `.cds-tab` | Individual tab; current tab marked with `.active` |
| `.active` | Shared state modifier: 2px ink ring on `.cds-pill`, underline dot on `.cds-tab` |
| `.cds-stat` | Label-over-value stat pair container |
| `.cds-stat-label` | Brass (`--gold-deep`) uppercase label for a stat |
| `.cds-stat-value` | Tabular-numeral value for a stat |
| `.cds-switch` | Toggle switch wrapper (label element around a checkbox) |
| `.cds-switch-slider` | The switch's visible track and knob, siblings the checkbox input |

## TopLeaseMap

TopLeaseMap is the reference implementation. It vendors the token layer only
(`tokens.css`, copied in as `src/cardinal-tokens.css` at a pinned version) and
keeps its own `bb-*` / `sb-*` / `ppq-*` component classes as-is. It does not
consume `components.css` or the `cds-` classes. See `src/CLAUDE.md` in the
TopLeaseMap repo for the refresh procedure.

For the v6 bump it needs the whole of `tokens.css` re-copied, not a patch: the file
gained the `--dk-*` ramp and `--brass-900` / `--lapis-200` in the primitive layer, a
`--link-hover` role, and the `.cds-dark` block at the bottom. Then put `cds-dark` on
the element that should go dark. Terminus starts with `#lease-card`, which already
paints its own background, so the scope only has to supply the roles.
