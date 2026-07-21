# Cardinal Design System

The shared visual language for the Cardinality app suite (TopLeaseMap, LeaseIndex,
CharlieBot): a layered heritage-parchment system — a warm off-white canvas, crisp
white surfaces raised on soft shadow, deep oxblood chrome, and brass rings and fills.
Depth comes from three shadow steps, not texture; the faint paper grain lives on the
canvas alone. A three-role humanist type system (Garamond for display, Source Sans 3
for UI and for data — numbers render in the UI sans with tabular figures — and Source
Code Pro reserved for code). One CSS file, no build step, versioned by git tag.

Live showcase: open `index.html` in this repo, or view it hosted once GitHub Pages
is turned on. It renders every token and every `cds-` component with copy-paste
snippets.

## Consumption

Link the whole system (font + tokens + components):

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tbchonka-cardinal/cardinal-design@v3.1.0/cardinal.css">
```

Token-only alternative, for an app that wants the color/spacing/type variables but
keeps its own component CSS:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tbchonka-cardinal/cardinal-design@v3.1.0/tokens.css">
```

Or vendor `tokens.css` into the consuming app's own repo (copy the file in,
comment the version it was pinned at) so the app stays self-contained offline and
in local dev, and pull a fresh copy by hand when you want to bump.

## Versioning policy

- Pin every consumer to a git tag (`@v2.0.0`), never `@main`. jsDelivr caches tags
  aggressively; `@main` will not reliably pick up changes and gives you no way to
  roll back.
- Workflow to change anything: edit the CSS in this repo, tag a new version
  (`v1.x.y`), then go bump the pinned tag in each consuming app deliberately. No
  app auto-follows a moving target.
- Non-goals: no dark theme, no JS behaviors, no build pipeline or npm
  package, no React.

## Class reference

| Class | What it is |
|---|---|
| `.cds-card` | Elevated white card container: surface background, hairline rule border, soft resting shadow |
| `.cds-card-header` | Oxblood gradient header bar for a card, uppercase meta text |
| `.cds-card-body` | Padded, scrollable card content area |
| `.cds-btn` | Base button shape shared by all button variants |
| `.cds-btn-primary` | Brass-glass gradient button, for the main action |
| `.cds-btn-ghost` | Outline button that fills to oxblood on hover |
| `.cds-btn-danger` | Solid hot-red button, for destructive actions |
| `.cds-btn-icon` | 28px square icon button for one inline SVG (close, add, edit, menu) |
| `.cds-panel` | Floating white surface with a hairline rule border, for sidebars/filters |
| `.cds-table` | Data table: sticky ink-on-paper-2 headers, zebra rows, hairline dividers |
| `.cds-num` | Right-aligned, tabular-numeral table cell for numeric columns |
| `.cds-field` | Wrapper around a labeled form control, sets bottom margin |
| `.cds-label` | Standalone brass (`--gold-deep`) uppercase field label (used outside `.cds-field`) |
| `.cds-input` | Text input styled to the white surface field treatment with a brass focus ring |
| `.cds-select` | Select dropdown styled to match `.cds-input` |
| `.cds-badge` | Small status indicator: colored dot plus label |
| `.cds-badge-success` | Badge modifier, emerald, for a good/synced state |
| `.cds-badge-error` | Badge modifier, brick red, for a failed/error state |
| `.cds-badge-muted` | Badge modifier, muted italic, for an empty/inactive state |
| `.cds-pill` | Outline filter chip; toggled solid oxblood with `.active` |
| `.cds-eyebrow` | Uppercase, letterspaced, brass (`--gold-deep`) section label |
| `.cds-tabs` | Flex row container for a tab strip |
| `.cds-tab` | Individual tab; current tab marked with `.active` |
| `.active` | Shared state modifier: solid oxblood fill on `.cds-pill`, underline dot on `.cds-tab` |
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
