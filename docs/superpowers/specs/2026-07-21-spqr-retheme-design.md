# SPQR retheme of cardinal-design

Date: 2026-07-21
Status: approved design, pending implementation plan

## Goal

Shift the Cardinal Design System from the current paper/ink/gold "Editorial
Almanac" palette to SPQR flag colors: light golds for paper surfaces, a deep
red for dark chrome, and restrained glassy effects. Text stays near-black.
This is a retheme, not a refactor: token values change, class names and
structure do not.

## Decisions made

1. Body text keeps the current near-black `--ink` (#1a1814). Red and gold
   live in chrome and accents only.
2. Every solid dark surface becomes deep red: top nav bars, card headers,
   active filter pills, ghost button hover fill, icons.
3. Error and danger states move to a hotter, brighter red so they stay
   distinct from the chrome red.
4. Glass effects go in exactly two places: the primary button and the dark
   nav/header bars. Active pills and tabs get none.

## Changes

### 1. New tokens: imperial red for dark surfaces

Today `--ink` does two jobs: text and solid dark surfaces. Add:

- `--imperial: #6e1414` (deep flag red, darkened for contrast; tune visually)
- `--imperial-bright` (hover lift, parallel to `--gold-bright`)

Repoint every dark-surface rule in `components.css` from `--ink` to
`--imperial`: `.cds-card-header`, `.cds-pill.active`, `.cds-btn-ghost:hover`,
and any other solid-ink fill. `--rule-on-ink` gets a matching review since it
was tuned for an ink background; rename or retune it for the red header.
Text rules keep `--ink` untouched.

### 2. Paper surfaces go light gold

Same lightness as today, warmer hue. Starting points, tuned in the showcase:

| Token | Now | Target |
|---|---|---|
| `--paper` | #f7f1e3 | ~#faf3da |
| `--paper-2` | #efe7d3 | ~#f3e8c4 |
| `--paper-3` | #e6dcc2 | ~#ead9a8 |
| `--rule` | #c8b894 | ~#cbb271 |
| `--rule-soft` | #d8caac | ~#dcc98f |

### 3. Accent gold nudges toward the flag

`--gold` #a8772a moves toward ~#b0851f, with `--gold-soft`, `--gold-bright`,
`--gold-wash`, `--gold-tint`, and `--focus` re-derived from it. The gold must
stay dark enough that 10px uppercase gold labels pass WCAG AA (3:1 minimum
for large/bold text, 4.5:1 preferred) on the new paper. The bright flag gold
(~#e9c85d) appears only inside gradients, never as text.

### 4. Errors get hotter

`--brick` #8b2a1f moves to ~#c0392b and `--brick-bright` re-derives from it.
Danger buttons and error badges use the hot red; deep red is furniture, hot
red is a warning.

### 5. Glass gradient tokens

Two new tokens so consuming apps with their own component classes can adopt
the same treatment:

- `--grad-gold`: vertical gradient, bright flag gold at top through `--gold`,
  used by `.cds-btn-primary` along with a 1px inset top highlight.
- `--grad-imperial`: faint vertical gradient on `--imperial`, light to dark,
  used by `.cds-card-header` (and app nav bars) with a gold hairline beneath.

No other component gets a gradient or sheen.

## Files touched

- `tokens.css`: new and changed token values, new gradient tokens.
- `components.css`: dark-surface repoint to `--imperial`, primary button
  gradient, card-header gradient plus gold hairline, danger button hot red.
- `index.html`: showcase renders the new look; no structural changes needed
  unless a new token deserves a swatch row.
- `README.md`: update the one-line palette description and class notes that
  mention ink surfaces.

## Verification

- Open `index.html` in the browser and check every component visually.
- Check contrast on every text/background pair that changed: ink on the new
  papers, gold labels on paper, paper-tinted text on imperial headers, white
  or paper text on the hot red danger button. WCAG AA at rendered sizes.
- Confirm the danger button and error badge read as clearly different from
  the imperial chrome next to each other.

## Rollout

1. Land the changes in cardinal-design, verify the showcase, tag `v2.0.0`
   (the look changed even though token names mostly did not).
2. Bump consumers one at a time, deliberately, per the versioning policy.
   TopLeaseMap first: refresh its vendored `cardinal-tokens.css`. It inherits
   the palette from token names, but its own `bb-*`/`sb-*`/`ppq-*` CSS uses
   `--ink` for dark surfaces and needs the same `--ink` to `--imperial`
   repoint. That work is a follow-up spec'd in the TopLeaseMap repo.

## Non-goals

- No class renames, no new components, no dark theme, no build pipeline.
- No glass anywhere beyond the primary button and dark header bars.
- No change to type scale, spacing, radii, or motion tokens.
