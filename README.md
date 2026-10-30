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
v7.0.0 takes its cue from the Claude Code app (Thatcher, 2026-10-29): four type
sizes (`--type-meta` 11, `--type-label` 12, `--type-body` 13, `--type-title` 15),
and inside a `.cds-card-shell` a group is a small muted heading over hairline
rows, never a band or a zebra; a value reads as right-aligned text whose edit
box shows on hover or focus; a status is a dot and a word. The v4 `--fs-*`
sizes stay until no consumer reads them.
v7.1.0 gives tabs two kinds: underline tabs switch a view or section, and
fill tabs pick one of a few in place.
v7.2.0 makes a status a dot and a word (`.cds-status`), with mid-tone
`--status-*` dot colors that stay apart at 6px.

Live showcase: open `index.html` in this repo, or view it hosted once GitHub Pages
is turned on. It renders every token and every `cds-` component with copy-paste
snippets.

## Consumption

Link the whole system (font + tokens + components):

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tbchonka-cardinal/cardinal-design@v7.2.0/cardinal.css">
```

Token-only alternative, for an app that wants the color/spacing/type variables but
keeps its own component CSS:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tbchonka-cardinal/cardinal-design@v7.2.0/tokens.css">
```

Or vendor `tokens.css` into the consuming app's own repo (copy the file in,
comment the version it was pinned at) so the app stays self-contained offline and
in local dev, and pull a fresh copy by hand when you want to bump.

## Versioning policy

- Pin every consumer to a git tag (`@v7.2.0`), never `@main`. jsDelivr caches tags
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

The card grammar (fact rows, card tables, tab bars, panels, notes) arrived
from TopLeaseMap's `cards.css` in v6.1.0, added inside `components.css`'s
existing Card section rather than as a separate file. The card shell
(v6.3.0) joined the end of the same section. That whole section — from
`.cds-card` through the shell's `.cds-card-chart` — is the vendoring unit: an app
that copies rather than links `components.css` copies that one contiguous
block and re-copies it whole on the next tag bump.

## Class reference

| Class | What it is |
|---|---|
| `.cds-dark` | Theme scope: rewires every color role beneath it onto the warm dark ramp. Lives in `tokens.css`, so token-only consumers get it |
| `.cds-card` | Elevated white card container: surface background, hairline ring, soft resting shadow |
| `.cds-card-header` | Raised neutral header band for a card, brass hairline beneath |
| `.cds-card-body` | Padded, scrollable card content area; v6.1.0 added `flex: 1; min-height: 0`, inert outside a flex parent, so a pinned card column can let the body take the leftover height |
| `.cds-card-footer` | White action band completing the three-band edit card; tints the body via `:has()` |
| `.cds-card-header-actions` | Header action-button cluster; right padding clears an absolutely-positioned close control |
| `.cds-card-action-btn` | Quiet ghost button inside the header actions cluster |
| `.cds-card-id-pill` | Gold identity pill on the fact-label line: 10px, dark text on gold, 4px below; v6.2.0 moved it off its own 12px size and v6.2.1 made it a 14px block, the same line box as the label, so the identity cell aligns with the fact cells under any inherited line-height |
| `.cds-card-identity-name` | Identity name on the fact-value line: 13px, weight 500, tabular figures; v6.2.0 dropped the 4px top margin and the body-size font |
| `.cds-fact-row` | Header fact row: identity cell plus facts, four-column base shape; `--solo`/`--3`/`--5` size the column count |
| `.cds-fact-cell` | One fact-row cell; `.is-missing` mutes its label and value color |
| `.cds-fact-label` | Small brass (`--gold-deep`) label above a fact value |
| `.cds-fact-value` | Tabular-numeral fact value |
| `.cds-fact-status-box` | Filled color status chip inside a fact cell, tint supplied by the app; no box on `--` |
| `.cds-card-table` | Card-scoped table grammar: header band over zebra rows, no divider lines |
| `.cds-card-lv-table` | Label/value banded table variant: two columns, value right |
| `.cds-ct-row` | One card-table row (its own grid; column template is left to the consumer); odd rows zebra, excluding the head and section rows |
| `.cds-ct-head` | Card-table header row |
| `.cds-ct-cell` | Card-table cell; `.is-missing` mutes its color |
| `.cds-ct-num` | Right-aligned card-table cell for numeric columns |
| `.cds-ct-link` | Link inside a card-table cell: brass at rest, lapis and underlined on hover, like a plain link; v6.4.0 moved it off `--imperial`, which stays dark under `.cds-dark` |
| `.cds-ct-section` | Gold section-header text spanning the full row width |
| `.cds-ct-section-row` | Card-table row wrapping a `.cds-ct-section` label, excluded from zebra striping |
| `.cds-card-tab-bar` | Segmented pill tab bar inside a card |
| `.cds-card-tab-bar--underline` | Tab bar variant: transparent bar, 3px brass underline on the active tab |
| `.cds-card-tab` | Individual card tab; current tab marked with `.active` |
| `.cds-card-panel` | Boxed subsection inside a card body, brass ring and tinted background |
| `.cds-card-panel-title` | Brass eyebrow title for a `.cds-card-panel` |
| `.cds-card-notes` | Read-only note surface |
| `.cds-card-notes-edit` | Editable notes textarea, same surface treatment as `.cds-card-notes` |
| `.cds-card-notes-status` | Save-status label with a leading dot; `.saving`/`.saved`/`.error` color it |
| `.cds-card-note` | Quiet inline note inside a card body (loading, empty, absent states) |
| `.cds-card-shell` | v6.3.0 card shell: the pinned card's column; action bar, identity and tabs stay put while the body scrolls. Markup comes from the app (TopLeaseMap `card-shell.js`); this package ships only the CSS |
| `.cds-card-action-btn.is-primary` | The one brass-filled action in a shell's action bar |
| `.cds-card-identity` | Shell identity zone: `-top` row (id pill and `.cds-card-kind` word), `.cds-card-title` (wraps, never cut off), `.cds-card-facts` (one fact line, key numbers in `<b>`) |
| `.cds-card-chips` | Row of editable status chips: `.cds-card-chip-wrap` (label plus chip) around a `.cds-card-field-box.cds-card-chip` pill |
| `.cds-card-tab-count` | Muted count after a tab label |
| `.cds-card-section` | Marks a section table (gold heading row); `.cds-card-section-aside` holds a right-side count or link |
| `.cds-card-link` | Quiet text button inside a body, e.g. "Full PPQ ›" |
| `.cds-card-tone-pos` / `.cds-card-tone-neg` | Moss / crimson value color for money and status |
| `.cds-card-empty` | One muted line for an empty or loading section |
| `.cds-card-toolbar` | Filter box and buttons above a table; `.cds-card-search` is its filter input |
| `.cds-card-field` | An editable row: its value sits in `.cds-card-field-box`, which in a v7 shell shows only on hover or focus (the arrow cursor holds). Parts: `-text`, `-caret`, `-input` (the open editor), `-msg` (Saving…, error, warning via `data-state`); `.cds-card-field--long` for long text |
| `.cds-card-menu` | Floating select / multi-select menu for a field box: `-option`, `-check`, `-done` |
| `.cds-card-more` | `⋯` disclosure for rare actions; `.cds-card-more-menu` is its list |
| `.cds-card-row-link` | Table row that opens something, with hover and focus fill |
| `.cds-card-chart` | Fixed-height chart slot under a section heading |
| `.cds-card-field-pill` | v7.0.0: a status on a field's text, drawn as a dot in `--field-color` before the word |
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
| `.cds-tabs` | v7.1.0 tab strip: underline tabs that switch a view or section; draws no rule of its own |
| `.cds-tabs--fill` | v7.1.0 fill tabs that pick one of a few in place; the open one sits on `--paper-2` |
| `.cds-tab` | A tab: a muted word, ink at 600 when open (`aria-selected="true"` or `.active`) |
| `.cds-tab-count` | A count after a tab's word, muted, tabular |
| `.active` | Shared state modifier: 2px ink ring on `.cds-pill`, open state on `.cds-tab` |
| `.cds-status` | v7.2.0 status: a 6px dot in `--status` and a word, no box; `-success`, `-info`, `-warning`, `-danger` set the dot, and danger colors the word too |
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
