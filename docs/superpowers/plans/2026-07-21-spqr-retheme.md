# SPQR Retheme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Retheme cardinal-design to SPQR flag colors: light gold paper, imperial red chrome, hot red errors, gradients on the primary button and card headers only.

**Architecture:** Pure CSS token and component edits in the cardinal-design repo. One structural change (a new `--imperial` token family separates dark surfaces from text ink); everything else is value swaps. No class renames, no JS, no build step.

**Tech Stack:** Plain CSS custom properties, static `index.html` showcase, git tag versioning. No test framework exists; verification is a contrast-ratio script plus visual checks of the showcase in the browser.

**Spec:** `docs/superpowers/specs/2026-07-21-spqr-retheme-design.md`

## Global Constraints

- Repo: `C:\Users\ThatcherChonka\CardinalCore\cardinal-design` (its own git repo; commit there).
- No class or token renames. New tokens only: `--imperial`, `--imperial-bright`, `--grad-gold`, `--grad-imperial`.
- Body text keeps `--ink: #1a1814` everywhere. Never set text to a red.
- Gradients appear in exactly two components: `.cds-btn-primary` and `.cds-card-header`.
- Contrast floors: 4.5:1 for body-size text, 3:1 for the bold 10-11px uppercase labels (they render bolder than their point size suggests; treat 3:1 as the hard floor, prefer more).
- All hex values below are approved starting points; if the visual pass or contrast script fails a pair, darken the foreground (never lighten the paper) and re-check.
- Do NOT tag `v2.0.0` until the user has visually approved the showcase (Task 5 pauses for that).

---

### Task 1: Retheme `tokens.css`

**Files:**
- Modify: `tokens.css`
- Create: `docs/superpowers/tools/contrast.py` (checked in; reused at every future palette change)

**Interfaces:**
- Produces: tokens `--imperial`, `--imperial-bright`, `--grad-gold`, `--grad-imperial`, plus re-valued `--paper*`, `--rule*`, `--gold*`, `--brick*`, `--focus`, `--rule-on-ink`. Task 2 consumes these exact names.

- [ ] **Step 1: Write the contrast checker**

Create `docs/superpowers/tools/contrast.py`:

```python
"""WCAG contrast ratios for the SPQR palette. Run: python contrast.py"""

def lum(hexcolor):
    r, g, b = (int(hexcolor.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4))
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def ratio(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

PAIRS = [
    ("ink on paper",          "#1a1814", "#faf3da", 4.5),
    ("ink on paper-2",        "#1a1814", "#f3e8c4", 4.5),
    ("ink on paper-3",        "#1a1814", "#ead9a8", 4.5),
    ("ink-soft on paper",     "#4a443c", "#faf3da", 4.5),
    ("gold labels on paper",  "#a87b1c", "#faf3da", 3.0),
    ("gold labels on paper-2","#a87b1c", "#f3e8c4", 3.0),
    ("paper on imperial",     "#faf3da", "#6e1414", 4.5),
    ("paper on brick (danger)","#faf3da", "#c0392b", 4.5),
    ("paper on gold btn mid", "#faf3da", "#b09227", 3.0),
]

failed = False
for name, fg, bg, floor in PAIRS:
    r = ratio(fg, bg)
    ok = "PASS" if r >= floor else "FAIL"
    failed = failed or r < floor
    print(f"{ok}  {name}: {r:.2f} (floor {floor})")
raise SystemExit(1 if failed else 0)
```

- [ ] **Step 2: Run it, confirm the palette passes before touching CSS**

Run: `python docs/superpowers/tools/contrast.py`
Expected: every line `PASS` and exit code 0. Approximate ratios: ink on paper ~15.7, gold on paper ~3.4, paper on imperial ~10.7, paper on brick ~4.9. If any FAIL, darken that foreground hex until it passes and carry the adjusted hex into Step 3.

- [ ] **Step 3: Edit `tokens.css` values**

In the header comment block (lines 2-9), change `Version: v1.0.0` to `Version: v2.0.0` and the Philosophy line to:

```
   Philosophy: an aged-ledger look in SPQR colors — light gold paper, dark
               ink text, imperial red chrome, gold hairline rules, and
               Garamond set small and letterspaced.
```

Replace the Paper surfaces block:

```css
  /* Paper surfaces */
  --paper:     #faf3da;
  --paper-2:   #f3e8c4;
  --paper-3:   #ead9a8;
  --rule:      #cbb271;
  --rule-soft: #dcc98f;
```

Ink block: unchanged.

Replace the Accents block (keep `--ink-blue`, `--moss` as-is; `--brick` moves here from its old value):

```css
  /* Accents */
  --gold:        #a87b1c;
  --gold-soft:   #d6b562;
  --gold-bright: #c1922a;
  --gold-wash:   rgba(168, 123, 28, 0.08);
  --gold-tint:   rgba(168, 123, 28, 0.16);

  /* Imperial chrome — solid dark surfaces (nav bars, card headers, active
     pills, icons). Surfaces only; text stays --ink. */
  --imperial:        #6e1414;
  --imperial-bright: #8a1a1a;

  --ink-blue: #234e70;
  --moss:     #486b32;
  --brick:    #c0392b;   /* hot warning red — deep red is furniture, this is a warning */

  --focus: #a87b1c;
```

After the Shadows block, add:

```css
  /* Glass — the only two sanctioned gradients (spec 2026-07-21) */
  --grad-gold:     linear-gradient(180deg, #d9ad33 0%, var(--gold) 100%);
  --grad-imperial: linear-gradient(180deg, var(--imperial-bright) 0%, #5a0f0f 100%);
```

In the component-layer additions at the bottom, retune the two values and their comments:

```css
  /* Hairline divider for dark (imperial) card headers: a translucent tint of
     the new paper so the rule reads warm on the red header. */
  --rule-on-ink: rgba(250, 243, 218, 0.18);
  /* Danger-button hover, parallel to --gold-bright. */
  --brick-bright: #d64a3b;
```

Aliases block: unchanged (they point at vars).

- [ ] **Step 4: Verify the file parses and shows the palette**

Open `index.html` in the browser (swatch hex *labels* will be stale until Task 3; the rendered colors themselves come from the vars and must show gold paper). Confirm the page background is light gold, no unstyled flash, no console errors.

- [ ] **Step 5: Commit**

```bash
git add tokens.css docs/superpowers/tools/contrast.py
git commit -m "feat: SPQR token palette — gold paper, imperial chrome, hot brick"
```

---

### Task 2: Repoint dark surfaces and add glass in `components.css`

**Files:**
- Modify: `components.css`

**Interfaces:**
- Consumes: `--imperial`, `--imperial-bright`, `--grad-gold`, `--grad-imperial`, `--gold`, `--gold-bright` from Task 1.

- [ ] **Step 1: Bump version comment**

In the header block, `Version: v1.0.0` → `Version: v2.0.0`.

- [ ] **Step 2: Card header — imperial gradient with gold hairline**

Replace the `background` and `border-bottom` lines of `.cds-card-header` (currently `background: var(--ink);` and `border-bottom: 1px solid var(--rule-on-ink);`):

```css
.cds-card-header {
  display: flex;
  align-items: center;
  gap: var(--s-2);
  padding: var(--s-3) var(--s-4) 10px;
  background-color: var(--imperial);   /* fallback if gradients unsupported */
  background-image: var(--grad-imperial);
  color: var(--paper);
  border-bottom: 1px solid var(--gold);
  font-family: var(--font-body);
  font-size: var(--fs-meta);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: var(--ls-eyebrow);
}
```

- [ ] **Step 3: Primary button — gold glass**

Replace `.cds-btn-primary` and its hover:

```css
/* primary — gold glass: flag-gold gradient with an inset top highlight */
.cds-btn-primary {
  border-color: var(--gold);
  background-color: var(--gold);       /* fallback */
  background-image: var(--grad-gold);
  box-shadow: inset 0 1px 0 rgba(255, 240, 190, 0.4);
  color: var(--paper);
}
.cds-btn-primary:hover:not(:disabled) {
  border-color: var(--gold-bright);
  background-color: var(--gold-bright);
  background-image: linear-gradient(180deg, #e3bb45 0%, var(--gold-bright) 100%);
  color: var(--paper);
}
```

- [ ] **Step 4: Ghost hover and active pill — ink to imperial**

`.cds-btn-ghost:hover:not(:disabled)`:

```css
.cds-btn-ghost:hover:not(:disabled) {
  background: var(--imperial);
  border-color: var(--imperial);
  color: var(--paper);
}
```

(Note: the resting ghost border and `.cds-btn` base border stay `--ink`; they are hairlines, not solid surfaces.)

`.cds-pill.active`:

```css
.cds-pill.active {
  border-color: var(--imperial);
  background: var(--imperial);
  color: var(--paper);
}
```

Leave `.cds-pill:hover` as-is (it is not a solid dark surface). Leave `.cds-btn-danger` untouched: the Task 1 token change already makes it hot red.

- [ ] **Step 5: Verify in the browser**

Open `index.html`. Check: card header is deep red with a faint top-light gradient and a gold hairline under it; primary button has a gold sheen and brightens on hover; ghost button fills deep red on hover; active pill is deep red; danger button is clearly hotter/brighter than the header red when seen side by side; switch, tabs, table, badges all still legible. Screenshot for the record.

- [ ] **Step 6: Commit**

```bash
git add components.css
git commit -m "feat: imperial dark surfaces + gold-glass primary button"
```

---

### Task 3: Update the showcase `index.html`

**Files:**
- Modify: `index.html` (swatch grid ~lines 193-211, misc token list ~line 244)

**Interfaces:**
- Consumes: token names from Task 1. Display-only changes.

- [ ] **Step 1: Update stale hex labels**

The swatch tiles render from `var()` (already correct); only the `sc-swatch-hex` text labels are stale. Update each to match Task 1:

| Swatch | New label text |
|---|---|
| `--paper` | `#faf3da` |
| `--paper-2` | `#f3e8c4` |
| `--paper-3` | `#ead9a8` |
| `--rule` | `#cbb271` |
| `--rule-soft` | `#dcc98f` |
| `--gold` | `#a87b1c` |
| `--gold-soft` | `#d6b562` |
| `--gold-bright` | `#c1922a` |
| `--gold-wash` | `rgba(168,123,28,.08)` |
| `--gold-tint` | `rgba(168,123,28,.16)` |
| `--brick` | `#c0392b` |
| `--brick-bright` | `#d64a3b` |
| `--rule-on-ink` | `rgba(250,243,218,.18) on imperial` |

Also change the `--rule-on-ink` tile's demo background from `background-color: var(--ink)` to `background-color: var(--imperial)`.

- [ ] **Step 2: Add the new swatches**

Insert after the `--gold-tint` swatch (line ~206), matching the existing one-line format:

```html
<div class="sc-swatch"><div class="sc-swatch-color" style="background: var(--imperial);"></div><div class="sc-swatch-meta"><span class="sc-swatch-name">--imperial</span><span class="sc-swatch-hex" style="color: var(--paper-3);">#6e1414</span></div></div>
<div class="sc-swatch"><div class="sc-swatch-color" style="background: var(--imperial-bright);"></div><div class="sc-swatch-meta"><span class="sc-swatch-name">--imperial-bright</span><span class="sc-swatch-hex" style="color: var(--paper-3);">#8a1a1a</span></div></div>
```

And add gradient tiles right after those two (the gradient renders in the tile because `background:` accepts an image):

```html
<div class="sc-swatch"><div class="sc-swatch-color" style="background: var(--grad-gold);"></div><div class="sc-swatch-meta"><span class="sc-swatch-name">--grad-gold</span><span class="sc-swatch-hex">#d9ad33 → --gold</span></div></div>
<div class="sc-swatch"><div class="sc-swatch-color" style="background: var(--grad-imperial);"></div><div class="sc-swatch-meta"><span class="sc-swatch-name">--grad-imperial</span><span class="sc-swatch-hex" style="color: var(--paper-3);">--imperial-bright → #5a0f0f</span></div></div>
```

- [ ] **Step 3: Verify in the browser**

Open `index.html`. Every swatch label matches its rendered color; the four new tiles render (two solid reds, two gradients). Skim the whole page once more for anything still visually black that should be red.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "docs: showcase swatches for SPQR palette and gradients"
```

---

### Task 4: Update `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Edit the descriptions**

Line 4 intro: change `warm paper, dark ink, gold hairline rules, EB Garamond set small` to `light gold paper, dark ink text, imperial red chrome, gold hairline rules, EB Garamond set small`.

Consumption snippets: change both pinned URLs from `@v1.0.0` to `@v2.0.0`.

Class-reference rows that name the old colors:

| Class | New description |
|---|---|
| `.cds-card-header` | Imperial red gradient header bar for a card, uppercase meta text |
| `.cds-btn-primary` | Gold-glass gradient button, for the main action |
| `.cds-btn-ghost` | Outline button that fills to imperial red on hover |
| `.cds-btn-danger` | Solid hot-red button, for destructive actions |
| `.cds-pill` | Outline filter chip; toggled solid imperial red with `.active` |
| `.active` | Shared state modifier: solid imperial fill on `.cds-pill`, underline dot on `.cds-tab` |

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: README wording for SPQR v2 palette"
```

---

### Task 5: Visual sign-off, then tag v2.0.0

**Files:** none (verification and release only)

- [ ] **Step 1: Full showcase pass with screenshots**

Open `index.html` in the browser at desktop width. Screenshot the swatch grid and the component sections. Re-run `python docs/superpowers/tools/contrast.py` one last time (guards against any hex adjusted mid-task); expected all PASS.

- [ ] **Step 2: STOP — user visual approval**

Show the user the screenshots and wait for explicit approval. Do not tag without it. If the user wants tuning, adjust the hex in `tokens.css`, re-run the contrast script, update the matching labels in `index.html`, commit as `fix: tune <token> after visual review`, and return to Step 1.

- [ ] **Step 3: Tag and push**

```bash
git tag v2.0.0
git push origin main --tags
```

- [ ] **Step 4: Report**

Confirm to the user: tag pushed, jsDelivr URL for v2.0.0, and the reminder that no consumer moves until its pin is bumped deliberately. TopLeaseMap's vendored-token refresh and its own `--ink → --imperial` dark-surface repoint are the next piece of work, planned in the TopLeaseMap repo.
