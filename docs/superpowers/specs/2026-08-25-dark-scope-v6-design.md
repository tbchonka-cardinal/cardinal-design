# Dark scope v6: design

Date: 2026-08-25
Repo: cardinal-design
Version: v6.0.0 ("Dark scope")
Status: built, contrast-gated, not tagged
Decided by: Thatcher, 2026-08-24 (`Resources/2026-08-24-competitive-capability-map.md`,
"Decided 2026-08-24: we go dark") and the amendment in
`TopLeaseMap/docs/superpowers/specs/2026-08-25-terminus-lease-card-design.md`
Value reference: `Resources/enverus-prism-ui-research/01-global-chrome-and-theme.md`
and `02-well-card-anatomy.md`

## 1. Summary

Dark ships as a scope class, `.cds-dark`, in `tokens.css`. Put it on any element
and every color role beneath it rewires onto a new warm dark ramp. Nothing that
is not color moves: same spacing, same radii, same 1px ring weight, same five
type sizes, same 150ms motion. A component looks like itself in either theme.

This is deliberately not a `prefers-color-scheme` media query and not a second
stylesheet. Terminus needs one dark card floating on a light map before it needs
a dark app, and a scope class does both from one definition.

## 2. The open question, resolved

The capability map left one question for this spec: do brass and lapis carry into
dark, or does dark get its own accent. **They carry.** Prism is dark gray with one
green accent; keeping brass and lapis is the difference between our own product
and a clone of theirs.

What "carry" means, precisely, because a hue cannot survive a ground swap
untouched:

- Where brass or lapis is a **fill, a band, or a hairline**, the value stands. A
  brass button, a brass card-header rule, a lapis masthead: all already read
  bright against a near-black ground. `--accent` stays `--brass-500`,
  `--ring-accent` stays `--brass-500`, `--imperial` stays `--lapis-500`, and both
  gradients are untouched.
- Where brass or lapis is **text**, the scope swaps in the light end of the ramp.
  `--gold-deep` and `--accent-text` go from `#846931` to `#D9BC7E`; the link hover
  goes from `#1E4585` to a new `--lapis-200` at `#A8C4EA`. Hue identity holds:
  brass-300 is the same brass ramp, and lapis-200 sits at hue 214 against
  lapis-500's 216.
- The two alpha tints (`--gold-wash` row hover, `--gold-tint` focus glow and
  selection) lift to the light brass at higher alpha. A fixed alpha over a dark
  ground is a different color, not a dimmer one.

## 3. The dark ramp

Warm, not cool. Prism's `#1B1B1B` page / `#282828` panel / `#393939` zebra set the
**value** steps we aim at; the hue stays warm (R > G > B) because the identity is
parchment. Steps are even in L\*, one per elevation level, so the system's
"one step per level" rule reads the same in the dark.

| Token | Value | L\* | Role it fills |
|---|---|---|---|
| `--dk-0` | `#F5F1EA` | 95.3 | `--text`, `--ink` |
| `--dk-100` | `#D6CFC4` | 83.4 | `--text-soft`, `--ink-soft` |
| `--dk-300` | `#AEA69A` | 68.5 | `--text-mute`, `--ink-mute` |
| `--dk-450` | `#5A5147` | 35.0 | `--border-strong`, `--rule-strong`, `--ring-strong` |
| `--dk-500` | `#4A4239` | 28.5 | `--border`, `--ring` |
| `--dk-600` | `#413A33` | 24.9 | `--paper-3`, `--rule` |
| `--dk-700` | `#37312B` | 20.8 | `--bg-raised`, `--paper-2`, `--rule-soft` |
| `--dk-750` | `#2E2924` | 17.0 | `--paper-zebra` |
| `--dk-800` | `#25211D` | 13.0 | `--bg-surface`, `--surface` (the panel) |
| `--dk-900` | `#1A1714` | 8.0 | `--bg`, `--paper` (the ground) |

The numbers keep the light ramp's meaning: bigger is darker, 0 is lightest. What
differs is the distribution. The light ramp crowds the light end (surfaces near
white, one dark ink); this one crowds the dark end (surfaces near black, one light
ink). Elevation walks 900 → 800 → 750 → 700, about 4 L\* a step, so a zebra row
sits nearer the panel than a header band does, exactly as `--n-25` and `--n-75` do
on white.

New accent slots, both in the primitive layer:

| Token | Value | Why |
|---|---|---|
| `--brass-900` | `#33291B` | the dark end of the brass ramp; becomes `--gold-subtle` |
| `--lapis-200` | `#A8C4EA` | lapis as text on a dark ground; becomes `--link-hover` and `--imperial-bright` |

Feedback pairs swap ends: a light chip on a dark card reads as a flare, so the
tint goes deep and the text goes light. `#9FD9B8` on `#1C2E24` (success),
`#F0A9A0` on `#331E1C` (danger), `#E5BE72` on `#33291A` (warning), `#A8C4EA` on
`#1E2836` (info). Brick keeps its value; white on it still passes. The four jewel
data colors lift to clear 3:1 on the panel as dots and chart series.

Elevation keeps the exact shadow geometry of the light layer and changes only the
color: black at 44% and 30% instead of the two warm tints, which are invisible on
a dark ground. The alpha is up because the first consumer is a dark card floating
on a light map and it needs a real shadow. The paper grain inverts to light
specks at 3%.

## 4. The scope mechanism

```css
.cds-dark {
  background-color: var(--bg);
  color: var(--text);
  color-scheme: dark;
  --bg: var(--dk-900);
  /* ...every other role and alias... */
}
```

Three things about that rule are load-bearing.

`color: var(--text)` is not decoration. Inherited `color` is a computed value, not
a var reference, so a dark card dropped into a light page would otherwise keep the
light page's near-black ink and render invisible.

`background-color: var(--bg)` covers a bare wrapper, and a component still wins
over it: `.cds-dark` and `.cds-card` have equal specificity, and `components.css`
loads after `tokens.css`, so an element carrying both paints `--bg-surface`. That
is the wanted order.

`color-scheme: dark` hands native scrollbars, spinners and date pickers to the
dark side.

## 5. What had to change in components.css

The scope can only reach color that goes through a role or an alias. Three
declarations reached past them into a neutral primitive, and each one would have
left a light artifact on a dark surface. All three swaps are value-identical in
the light theme:

| Rule | Was | Now |
|---|---|---|
| `.cds-pill.active` 2px ring | `--n-900` | `--text` |
| `.cds-switch-slider` off track | `--n-100` | `--paper-3` |
| `.cds-input:focus` glow | `--brass-tint` | `--gold-tint` |

`::selection` in `tokens.css` moved from `--brass-tint` to `--gold-tint` for the
same reason. The primitives left in `components.css` are theme-neutral on purpose:
`--n-900` ink on a brass fill, `--n-0` white on brick, and the brass ramp itself.

One new role, `--link-hover`, defaults to `--imperial`. The base `a:hover` rule now
reads it, which is what lets the dark scope lighten a link without moving the
masthead band. It also settles a contradiction the file carried: the craft note
said lapis is not a text color while `a:hover` used it as one. Now there is one
sanctioned lapis text use and it has a name.

## 6. Contrast gate

`docs/superpowers/tools/contrast.py` covers the dark layer the same way it covers
the light one: every text role against every ground it can sit on, the accent as
text and as a focus ring, the feedback pairs on their own tint and on the panel,
the jewel colors at the 3:1 non-text floor. 65 pairs, all pass, exit 0.

Tightest margins, worth knowing before anyone nudges a value:

| Pair | Ratio | Floor |
|---|---|---|
| muted captions on the deep tint | 4.64 | 4.5 |
| muted captions on the raised band | 5.33 | 4.5 |
| brass text on the raised band | 6.99 | 4.5 |

`--dk-300` was set at `#AEA69A` rather than a darker `#A29A8E` for exactly the
first row: the darker value read 4.02 on `--paper-3` and failed. The light layer's
own gate stops at the raised band and never tested that pair; the dark section
tests one ground further out.

## 7. Consumers

Nothing auto-follows. `tokens.css` needs re-copying whole into each vendoring app,
not patching: the primitive layer gained the `--dk-*` ramp plus `--brass-900` and
`--lapis-200`, the role layer gained `--link-hover`, `a:hover` and `::selection`
changed, and the `.cds-dark` block is new at the bottom. Then put `cds-dark` on
whatever should go dark.

TopLeaseMap goes first, on `#lease-card`, per the lease-card amendment. It already
paints its own card background, so the scope only has to supply the roles. App-wide
dark is a later pass, and it will surface any app CSS still holding a raw hex.

## 8. Not in this round

No `prefers-color-scheme` hook and no theme toggle. Both are app decisions, and a
scope class is the primitive they would be built on. No dark map style, no dark
variants of the app icons, no per-component dark overrides.
