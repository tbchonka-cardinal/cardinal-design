# Stripe-craft v4: design

> **Note (v5.0.0, 2026-08-03):** The mechanics here still hold — rings, radii,
> type scale, motion. The chrome color sections are superseded: v5.0.0 replaced
> the oxblood ramp with lapis. Read this spec for craft, not for color.

Date: 2026-07-27
Repo: cardinal-design
Status: approved pending Thatcher's spec review
Source material: Stripe dashboard teardown (Downloads/stripe-dashboard-design-teardown.md)

## 1. Summary

Rebuild cardinal-design to v4.0.0. Keep the heritage identity (parchment canvas,
white surfaces, oxblood chrome, brass accent, Garamond display). Adopt Stripe's
craft mechanics: a layered token architecture, a short type scale with hierarchy
from weight and color, a numeric 4px spacing scale, borders drawn as box-shadow
rings, two-tint layered shadows, 2:1 container-to-control radii, and 150ms motion
limited to background-color and box-shadow. Swap the UI sans from Source Sans 3
to the system stack. This round touches only this repo: tokens.css,
components.css, index.html. Apps bump pins in a later round.

## 2. Decisions made in brainstorming

1. Identity stays; craft changes. Fonts and font hierarchy are in scope.
2. UI sans becomes the system stack. Garamond stays, display only. Source Code
   Pro stays for code.
3. Scope: design system first (this spec), TopLeaseMap/Terminus app round after,
   with its own spec.
4. Color principles adopted: one-accent discipline, feedback tint pairs, tinted
   scrim, formalized neutral ramp. Palette hues stay.
5. Geometry: full Stripe treatment. 6px controls, 12px containers, rings,
   two-tint shadows, 150ms motion.
6. Token structure: primitive ramps plus semantic roles, with every v3 token
   name kept as an alias. No third per-component-state layer.

## 3. Token architecture

tokens.css gets three sections, top to bottom:

1. **Primitives**: ordered ramps with numeric names. Components never reference
   these directly.
2. **Roles**: semantic tokens (`--text`, `--surface`, `--border`, `--accent`,
   `--ring`, `--shadow-sm`...) that map onto primitives. Components reference
   roles.
3. **Compatibility aliases**: every v3 token name, mapped into the new system.
   Some alias values change on purpose (see 9). Consumers keep working on bump.

New in-between values get numbers on the existing ramps, never new ad-hoc names.

## 4. Typography

Faces:

```css
--font-display: 'EB Garamond', Garamond, Georgia, serif;      /* h1/h2 only */
--font-body:    system-ui, -apple-system, 'Segoe UI', Roboto,
                'Helvetica Neue', Arial, sans-serif;
--font-mono:    'Source Code Pro', Consolas, monospace;
```

The Source Sans 3 @import in cardinal.css goes away. EB Garamond and Source
Code Pro imports stay. Numbers keep `font-feature-settings: 'tnum'` in data
contexts. Garamond keeps its `'ss01', 'cv11'` settings on h1/h2.

Scale, line heights on the 4px grid:

| Token | Size / line | Role | Face, weight |
|---|---|---|---|
| `--fs-caption` | 12 / 16 | captions, meta, eyebrows | sans 400; eyebrows 600 + `--ls-eyebrow` tracking |
| `--fs-body` | 14 / 20 | body, data, controls | sans 400; emphasis 600 |
| `--fs-heading` | 16 / 24 | card headings | sans 700 |
| `--fs-section` | 20 / 28 | section titles, h2 | Garamond 600 |
| `--fs-page` | 28 / 36 | page titles, h1 | Garamond 600 |

Each size ships a matching `--lh-*` token. The 10px and 11px sizes retire.
Hierarchy rule, documented in the file header: within a size, differentiate with
weight (400/600/700) and ink tier (`--ink`, `--ink-soft`, `--ink-mute`). A new
size requires editing this spec first.

Not doing: font-metrics variables (cap-height trimming). Wrong scale for us.

## 5. Color

### 5.1 Neutral ramp

Values unchanged, names formalized. Warm neutral ramp `--n-*`:

| Step | Value | v3 name |
|---|---|---|
| `--n-0` | #FFFFFF | --surface |
| `--n-25` | #FAF8F5 | --paper-zebra |
| `--n-50` | #F9F7F2 | --paper |
| `--n-75` | #F2EFE9 | --paper-2 |
| `--n-90` | #EFEBE2 | --rule-soft |
| `--n-100` | #EBE6DC | --paper-3 |
| `--n-150` | #E6E1D8 | --rule |
| `--n-300` | #C8C2B5 | --rule-strong |
| `--n-600` | #706B62 | --ink-mute |
| `--n-800` | #524E48 | --ink-soft |
| `--n-900` | #161514 | --ink |

v4 note: n-600 darkened from #78736A so 12px captions pass 4.5:1 on the canvas (measured 4.43 before, 4.94 after).

Brass and oxblood get small ramps the same way (`--brass-*`, `--oxblood-*`)
covering the existing five brass values and two oxblood values.

### 5.2 One-accent discipline

Brass is the only color that means actionable: links, primary buttons, focus,
selection, active states. Oxblood is chrome only: nav bars, card headers, brand
marks. It is no longer an interaction color. Component consequences:

- `.cds-btn-ghost` no longer fills to oxblood on hover. New treatment: white
  surface, ring darkens to `--n-300`, shadow lifts sm to md.
- `.cds-pill.active` no longer fills solid oxblood. New treatment: 2px ink ring
  on white (Stripe filter-chip pattern).

The gold-text rule stays: brass text on light surfaces uses `--gold-deep`.

Focus indicators (the `:focus-visible` outline and input focus rings) use the darker `--brass-700` step (#846931): an indicator needs 3:1 on white and brass-500 measures ~2.8:1.

### 5.3 Feedback pairs

Each status color gains a background tint. The pair is valid only if the text
color passes 4.5:1 on its own tint, checked with docs/superpowers/tools/contrast.py.
Candidate values, to be validated and adjusted during implementation:

| Status | Text | Tint (candidate) |
|---|---|---|
| success | #1B4D3E (moss) | #E7F0E9 |
| error | #8B1E1E (data-crimson; brick #c0392b stays for danger buttons) | #FBE9E5 |
| warning | #8A5A00 (new step below data-amber; #A36A00 measured 4.11:1 on its tint) | #FBF3DC |
| info | #1B365D (ink-blue) | #E8EEF6 |

Tints appear only in feedback contexts: badges, banners, form validation.

### 5.4 Scrim

`--scrim: rgba(82, 78, 72, 0.55)` (from `--n-800`), replacing any black
backdrop. Modals and drawers dim to warm gray, and the parchment reads through.

## 6. Spacing

Numeric 4px-grid scale, `100` = 8px:

```
--s-25: 2px   --s-50: 4px   --s-75: 6px   --s-100: 8px   --s-150: 12px
--s-200: 16px --s-300: 24px --s-400: 32px --s-600: 48px  --s-800: 64px
```

Usage rule in the file header: 8 inside compact controls, 12 between related
items, 16 between fields, 24 between regions, 32 between sections, 48 page
bottom. Old `--s-1..--s-7` alias onto the new steps at unchanged values.

## 7. Geometry and elevation

### 7.1 Radii

2:1 nesting system:

```
--r-sm: 4px          /* badges, small bits */
--r-control: 6px     /* buttons, inputs, selects, pills, tabs */
--r-container: 12px  /* cards, panels, popovers, modals */
--r-full: 9999em     /* toolbar pills only */
```

Square icon tiles use `border-radius: 20%` so the shape holds at any size.
This is the most visible change of the round: cards soften from 6px to 12px.

### 7.2 Rings

Hairline borders on cards, panels, inputs, chips, and buttons convert to
box-shadow rings:

```
--ring:        0 0 0 1px var(--n-150);
--ring-strong: 0 0 0 1px var(--n-300);
```

Rings take no layout space, so hover and focus can thicken or recolor them with
zero reflow, and they compose with drop shadows in one property. Real `border`
survives only where rings cannot work: table row dividers and the dashed
empty-state.

### 7.3 Shadows

Two-tint pairs: a tight near-black contact shadow plus a wide warm ambient
shadow from the ink family. Opacity fixed, offsets grow geometrically.

```
--shadow-sm: 0 1px 1px rgba(22,21,20,0.12), 0 2px 5px  rgba(82,78,72,0.08);
--shadow-md: 0 3px 6px rgba(22,21,20,0.12), 0 7px 14px rgba(82,78,72,0.08);
--shadow-lg: 0 5px 15px rgba(22,21,20,0.12), 0 15px 35px rgba(82,78,72,0.08);
--shadow-brass: 0 2px 5px rgba(90,68,28,0.32);  /* primary button only */
```

sm = resting cards, md = dropdowns and hover lift, lg = modals and floating
panels. The v3 names (--shadow-sm/--shadow-page/--shadow-pop) alias to
sm/md/lg.

## 8. Motion

```
--dur:       150ms;
--dur-long:  300ms;   /* drawers, modals */
--ease:       cubic-bezier(0, .09, .4, 1);   /* persistent elements */
--ease-enter: cubic-bezier(0, 0, .4, 1);
--ease-exit:  cubic-bezier(.4, 0, 1, 1);
```

Discipline, documented in the file: interactive elements transition only
`background-color` and `box-shadow`, at `--dur` with `--ease`. No transform,
width, or color animation. Prefer elevation change over background change for
hover where the ring and shadow can carry it. Old `--dur` 180ms and the old
single ease update in place.

## 9. Alias table (intentional value changes)

| v3 token | v3 value | v4 value | Why |
|---|---|---|---|
| `--fs-body`, `--fs-data` | 13px | 14px | Stripe body size; better reading at equal density cost |
| `--fs-meta` | 11px | 12px | scale merge |
| `--fs-eyebrow` | 10px | 12px | scale merge; tracking keeps the eyebrow look |
| `--fs-display` | 15px | 16px | maps to heading |
| `--fs-title` | 20px | 20px (section) | unchanged value, new role name |
| `--radius-xs` | 0 | 4px | sharp corners retire |
| `--radius-sm` | 2px | 4px | scale merge |
| `--radius-md` | 4px | 6px | control radius |
| `--radius-lg` | 6px | 12px | container radius |
| `--dur` | 180ms | 150ms | Stripe timing |
| `--ease` | cubic-bezier(.2,.4,.2,1) | cubic-bezier(0,.09,.4,1) | Stripe standard curve |
| `--shadow-page` | single shadow | `--shadow-md` pair | two-tint rebuild |
| `--shadow-pop` | single shadow | `--shadow-lg` pair | two-tint rebuild |
| `--font-body` | Source Sans 3 stack | system stack | webfont retired |
| `--ink-mute` | #78736A | #706B62 | caption contrast on canvas |
| `.cds-btn-primary text` | --paper | --ink | paper on brass measured ~2.6:1; closes the NEXT.md open question |
| `--focus` | `--gold` (#B8934A) | `--brass-700` (#846931) | focus indicator needs 3:1 on white; brass-500 measures ~2.8:1 |
| `--shadow-sm` | single shadow | two-tint pair | ~3x more visible at rest; announce to vendoring apps |
| `--gold-deep` / `--brass-700` | #8A6D33 | #846931 | 4.5:1 on tinted surfaces (n-75 measured 4.24 before) |
| body line-height, h1/h2 sizes | 1.5 unitless; h1/h2 unsized | 1.4286 unitless; h1 28px, h2 20px | scale enforcement; announce to vendoring apps |

All other aliases keep their v3 values.

## 10. Components

Sweep of existing `cds-` classes onto the new tokens:

- `.cds-card`: 12px radius, `--ring`, `--shadow-sm`. Header band keeps the
  oxblood gradient (chrome). The body band uses `--n-75` only in the
  three-band pattern (10, `.cds-card-footer`); plain cards stay white.
- `.cds-btn`: 6px radius, ring-based borders, `--shadow-brass` on primary,
  heights stay 32/28. Primary text is ink on brass, per §9.
- `.cds-btn-ghost`: white, `--ring`, hover = `--ring-strong` + `--shadow-md`.
- `.cds-pill.active`: 2px ink ring on white.
- `.cds-input`, `.cds-select`: 6px radius, ring instead of border, focus
  ring uses `--focus` (brass-700).
- `.cds-badge`: feedback pairs from 5.3.
- `.cds-table`, `.cds-switch`, `.cds-tabs`: token sweep, no structural change.

Three new components:

- `.cds-card-footer`: completes the three-band card. Oxblood header, `--n-75`
  body, white footer with right-aligned actions, footer inherits the bottom
  radii. Save bars attach to the card being edited, not the page.
- `.cds-empty`: 1px dashed `--n-300` border, 12px radius, centered `--ink-mute`
  message.
- `.cds-banner`: neutral notice on `--n-50` with a hairline ring,
  message 14px, optional text-link action right, dismiss far right. Status
  variants use the feedback pairs.
- Badges and banners carry no leading dot or icon (owner call at the 2026-07-27 visual gate).

## 11. Showcase and verification

- index.html renders every new token and component with copy-paste snippets,
  including the three new components and the feedback pairs.
- contrast.py validates: each feedback text on its tint, `--gold-deep` on
  `--n-0`/`--n-50`, each ink tier on each paper step it will sit on. Special
  check: `--n-600` (#706B62) as 12px caption text on white; if it fails 4.5:1,
  darken the caption use or the token, and record the choice here. `--n-600`
  (#706B62) passes.
- Browser pass on the showcase (Thatcher verifies visually).
- Tag v4.0.0 only after both pass.

## 12. Rollout (round 2, separate spec)

After the tag: TopLeaseMap re-vendors tokens.css and sweeps `bb-*`/`sb-*`/
`ppq-*`; Minerva and Janus bump CDN pins; CharlieBot pins whenever next touched.
App-level Stripe patterns ride with the TopLeaseMap round: progressive
disclosure (three-band edit cards, right rail for secondary content), page
organization, solid-fill icon audit at 12/16/20. That round gets its own
brainstorm against real screens. Nothing in this spec blocks on it.

## 13. Non-goals

Dark theme. JS behaviors. Build step or npm. Font-metrics variables.
Per-component state tokens. Stripe's palette or typefaces. App changes of any
kind in this round.
