# Stripe-craft v4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild cardinal-design to v4.0.0: heritage identity, Stripe mechanics (layered tokens, short type scale, system UI sans, rings, two-tint shadows, 2:1 radii, 150ms motion, feedback tint pairs).

**Architecture:** tokens.css becomes three layers (primitive ramps, semantic roles, v3 compatibility aliases). components.css sweeps every `cds-` class onto the roles and gains three new components. index.html shows all of it. contrast.py is the palette's test harness and runs first.

**Tech Stack:** Plain CSS custom properties, no build step. Python 3 for contrast.py. Git tag `v4.0.0` for release. Spec: `docs/superpowers/specs/2026-07-27-stripe-craft-v4-design.md`.

## Global Constraints

- Repo: `C:\Users\ThatcherChonka\CardinalCore\cardinal-design`. All paths below are relative to it. All commits go to this repo (`main`). Do not push; do not tag until Task 6's user gate passes.
- Version string is `v4.0.0` in every file header, the README pins, and both index.html locations.
- components.css contains no raw hex/rgb values; every value is a `var()`. (Exception already in file: the splash inline SVG template colors live in index.html, not components.css.)
- Every v3 token name must remain defined in tokens.css (the compatibility alias layer). The check in Task 2 Step 3 enumerates them.
- No JS beyond the existing `.active` toggling contract. No new dependencies.
- Motion discipline: interactive elements transition `background-color` and `box-shadow` only. The switch knob `transform` is the one sanctioned exception.
- Two palette adjustments are pre-baked and must survive: `--n-600` darkens to `#706B62` (caption contrast on canvas) and warning text is `#8A5A00` (contrast on its tint). Primary buttons use ink text on brass (paper text fails contrast; this closes the open NEXT.md primary-button question).
- Docs prose: plain short words, active voice, no em-dashes.

---

### Task 1: Palette lock via contrast.py

The contrast harness is the test for every color decision. It runs before tokens.css changes, because it tests hex values, not CSS. Expected: the full v4 pair list passes, proving the two pre-baked adjustments and the ink-on-brass button decision.

**Files:**
- Modify: `docs/superpowers/tools/contrast.py` (replace PAIRS and docstring; keep `lum` and `ratio` as they are)
- Modify: `docs/superpowers/specs/2026-07-27-stripe-craft-v4-design.md` (record outcomes)

**Interfaces:**
- Produces: the locked v4 hex values every later task uses verbatim:
  `--n-600: #706B62`, warning text `#8A5A00`, feedback tints `#E7F0E9 / #FBE9E5 / #FBF3DC / #E8EEF6`, primary-button text = ink `#161514`.

- [ ] **Step 1: Rewrite contrast.py pairs**

Replace the docstring and the whole `PAIRS` list (keep `lum` and `ratio` unchanged):

```python
"""WCAG contrast ratios for the Cardinal v4 palette. Run: python contrast.py"""
```

```python
PAIRS = [
    # ink tiers on the surfaces they sit on
    ("ink on white",                 "#161514", "#FFFFFF", 4.5),
    ("ink on canvas",                "#161514", "#F9F7F2", 4.5),
    ("ink on raised (n-75)",         "#161514", "#F2EFE9", 4.5),
    ("ink-soft on white",            "#524E48", "#FFFFFF", 4.5),
    ("ink-soft on canvas",           "#524E48", "#F9F7F2", 4.5),
    ("ink-mute captions on white",   "#706B62", "#FFFFFF", 4.5),
    ("ink-mute captions on canvas",  "#706B62", "#F9F7F2", 4.5),
    # brass accent
    ("gold-deep text on white",      "#8A6D33", "#FFFFFF", 4.5),
    ("gold-deep text on canvas",     "#8A6D33", "#F9F7F2", 4.5),
    ("gold ring on white (nontext)", "#B8934A", "#FFFFFF", 3.0),
    ("ink text on brass btn",        "#161514", "#B8934A", 4.5),
    ("ink text on brass hover",      "#161514", "#C9A45C", 4.5),
    # chrome and danger
    ("paper on imperial",            "#F9F7F2", "#4A1017", 4.5),
    ("white on brick (danger btn)",  "#FFFFFF", "#c0392b", 4.5),
    # feedback: text on its own tint
    ("success text on tint",         "#1B4D3E", "#E7F0E9", 4.5),
    ("danger text on tint",          "#8B1E1E", "#FBE9E5", 4.5),
    ("warning text on tint",         "#8A5A00", "#FBF3DC", 4.5),
    ("info text on tint",            "#1B365D", "#E8EEF6", 4.5),
    # feedback: text on white (badges on cards)
    ("success text on white",        "#1B4D3E", "#FFFFFF", 4.5),
    ("danger text on white",         "#8B1E1E", "#FFFFFF", 4.5),
    ("warning text on white",        "#8A5A00", "#FFFFFF", 4.5),
    ("info text on white",           "#1B365D", "#FFFFFF", 4.5),
]
```

- [ ] **Step 2: Run it**

Run: `python docs/superpowers/tools/contrast.py`
Expected: every line PASS, exit code 0. If any line fails, darken that foreground hex in 8-16 unit steps per channel until it passes, then carry the adjusted hex into the spec edit below and into Task 2.

- [ ] **Step 3: Record outcomes in the spec**

In `docs/superpowers/specs/2026-07-27-stripe-craft-v4-design.md`:
1. §5.1 table: change `--n-600` row value to `#706B62`, and append to the section: "v4 note: n-600 darkened from #78736A so 12px captions pass 4.5:1 on the canvas (measured 4.43 before, ~4.97 after)."
2. §5.3 table: warning row text becomes `#8A5A00 (new step below data-amber; #A36A00 measured 4.11:1 on its tint)`.
3. §9 alias table: add rows `--ink-mute | #78736A | #706B62 | caption contrast on canvas` and `.cds-btn-primary text | --paper | --ink | paper on brass measured ~2.6:1; closes the NEXT.md open question`.
4. §10 `.cds-btn` bullet: append "Primary text is ink on brass, per §9."

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/tools/contrast.py docs/superpowers/specs/2026-07-27-stripe-craft-v4-design.md
git commit -m "test: v4 palette contrast harness; lock adjusted values"
```

---

### Task 2: tokens.css v4 and cardinal.css font swap

**Files:**
- Modify: `tokens.css` (full replacement below)
- Modify: `cardinal.css` (full replacement below)

**Interfaces:**
- Produces: every token name Task 3-5 references: `--n-0..900`, `--brass-300/400/500/700`, `--brass-wash/tint/subtle`, `--oxblood-400/500/700`, `--success-text/-bg`, `--danger-text/-bg`, `--warning-text/-bg`, `--info-text/-bg`, `--fs-caption/body/heading/section/page` + matching `--lh-*`, `--s-25..800`, `--r-sm/control/container/full`, `--ring`, `--ring-strong`, `--shadow-sm/md/lg/brass`, `--dur`, `--dur-long`, `--ease/enter/exit`, `--scrim`, plus all v3 aliases.

- [ ] **Step 1: Replace tokens.css with this exact content**

```css
/* ============================================================
   Cardinal Design System — tokens.css
   Version: v4.0.0 ("Stripe-craft")
   Spec:    docs/superpowers/specs/2026-07-27-stripe-craft-v4-design.md
   Philosophy: heritage parchment identity, Stripe mechanics. Warm
     off-white canvas, crisp white surfaces, oxblood chrome, brass
     accent, Garamond display over a system UI sans. Three layers
     below: primitives (ordered ramps, numeric names), roles (what
     components consume), and v3 compatibility aliases. Components
     never reference a primitive directly.
   Craft rules (edit the spec before breaking one):
     - Type: five sizes (12/14/16/20/28), line heights on the 4px
       grid. Inside a size, hierarchy comes from weight (400/600/700)
       and ink tier, never a new size.
     - Space: 8 inside compact controls, 12 between related items,
       16 between fields, 24 between regions, 32 between sections,
       48 page bottom.
     - Radii: 6px controls inside 12px containers (2:1); 4px small
       bits; 9999em pills. Square icon tiles use border-radius: 20%.
     - Separators: box-shadow rings, not borders. Exceptions: table
       row dividers, card-header underline, dashed empty states.
     - Motion: interactive elements transition background-color and
       box-shadow only, at 150ms. The switch knob slide is the one
       sanctioned transform.
     - Brass is the only actionable color. Oxblood is chrome.
   ============================================================ */
:root {
  /* ---------- Layer 1: primitives ---------- */

  /* Warm neutral ramp. New in-between values get numbers, not names. */
  --n-0:   #FFFFFF;
  --n-25:  #FAF8F5;
  --n-50:  #F9F7F2;
  --n-75:  #F2EFE9;
  --n-90:  #EFEBE2;
  --n-100: #EBE6DC;
  --n-150: #E6E1D8;
  --n-300: #C8C2B5;
  --n-600: #706B62;  /* darkened from #78736A: 4.5:1 captions on canvas */
  --n-800: #524E48;
  --n-900: #161514;

  /* Brass ramp (the accent). Brass TEXT on light surfaces uses 700. */
  --brass-300: #D9BC7E;
  --brass-400: #C9A45C;
  --brass-500: #B8934A;
  --brass-700: #8A6D33;
  --brass-wash:   rgba(184, 147, 74, 0.08);
  --brass-tint:   rgba(184, 147, 74, 0.16);
  --brass-subtle: #F6F1E5;

  /* Oxblood ramp (the chrome). Surfaces only; text on them is --n-50. */
  --oxblood-400: #5E1620;
  --oxblood-500: #4A1017;
  --oxblood-700: #38090F;

  /* Feedback pairs. Text passes 4.5:1 on its own tint and on white
     (docs/superpowers/tools/contrast.py). Tints appear only in
     feedback contexts: badges, banners, form validation. */
  --success-text: #1B4D3E;  --success-bg: #E7F0E9;
  --danger-text:  #8B1E1E;  --danger-bg:  #FBE9E5;
  --warning-text: #8A5A00;  --warning-bg: #FBF3DC;
  --info-text:    #1B365D;  --info-bg:    #E8EEF6;

  /* Hot action red (danger buttons; must not blend into oxblood) */
  --brick:        #c0392b;
  --brick-bright: #d64a3b;

  /* Jewel data colors (charts, status dots) */
  --ink-blue:     #1B365D;
  --moss:         #1B4D3E;
  --data-amber:   #A36A00;
  --data-crimson: #8B1E1E;

  /* Paper texture — 1% noise SVG. Canvas only; surfaces are crisp. */
  --paper-noise: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.1 0 0 0 0 0.09 0 0 0 0 0.08 0 0 0 0.045 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");

  /* ---------- Layer 2: roles ---------- */

  /* Fonts. UI and data ride the system stack (Segoe UI on Windows);
     Garamond is display only (h1/h2); mono for code. The Garamond and
     Source Code Pro imports live in cardinal.css. */
  --font-display: 'EB Garamond', Garamond, Georgia, serif;
  --font-body:    system-ui, -apple-system, 'Segoe UI', Roboto,
                  'Helvetica Neue', Arial, sans-serif;
  --font-mono:    'Source Code Pro', Consolas, monospace;

  /* Type scale, line heights locked to the 4px grid */
  --fs-caption: 12px;  --lh-caption: 16px;
  --fs-body:    14px;  --lh-body:    20px;
  --fs-heading: 16px;  --lh-heading: 24px;
  --fs-section: 20px;  --lh-section: 28px;
  --fs-page:    28px;  --lh-page:    36px;
  --ls-eyebrow: 0.12em;

  /* Spacing: 4px grid, 100 = 8px */
  --s-25: 2px;   --s-50: 4px;   --s-75: 6px;   --s-100: 8px;
  --s-150: 12px; --s-200: 16px; --s-300: 24px; --s-400: 32px;
  --s-600: 48px; --s-800: 64px;

  /* Control sizing — one height so rows line up */
  --control-h: 32px;
  --control-h-sm: 28px;

  /* Radii: 2:1 container-to-control */
  --r-sm: 4px;
  --r-control: 6px;
  --r-container: 12px;
  --r-full: 9999em;

  /* Rings: hairline borders drawn as box-shadow. Zero layout space,
     animate and recolor freely, compose with drop shadows. */
  --ring:        0 0 0 1px var(--n-150);
  --ring-strong: 0 0 0 1px var(--n-300);

  /* Elevation: two-tint pairs. Tight near-black contact shadow plus
     wide warm ambient (from n-800). Fixed opacity, geometric offsets. */
  --shadow-sm: 0 1px 1px rgba(22,21,20,0.12), 0 2px 5px rgba(82,78,72,0.08);
  --shadow-md: 0 3px 6px rgba(22,21,20,0.12), 0 7px 14px rgba(82,78,72,0.08);
  --shadow-lg: 0 5px 15px rgba(22,21,20,0.12), 0 15px 35px rgba(82,78,72,0.08);
  --shadow-brass: 0 2px 5px rgba(90,68,28,0.32);  /* primary button only */

  /* Motion */
  --dur:      150ms;
  --dur-long: 300ms;  /* drawers, modals, splash fades */
  --ease:       cubic-bezier(0, 0.09, 0.4, 1);
  --ease-enter: cubic-bezier(0, 0, 0.4, 1);
  --ease-exit:  cubic-bezier(0.4, 0, 1, 1);

  /* Scrim: warm gray from the ink family, never black */
  --scrim: rgba(82, 78, 72, 0.55);

  --focus: var(--brass-500);

  /* Glass — the only two sanctioned gradients (spec 2026-07-21) */
  --grad-gold:     linear-gradient(180deg, var(--brass-400) 0%, var(--brass-500) 100%);
  --grad-imperial: linear-gradient(180deg, var(--oxblood-400) 0%, var(--oxblood-700) 100%);

  /* Hairline divider on dark oxblood headers */
  --rule-on-ink: rgba(247, 245, 240, 0.18);

  /* Plain-English roles */
  --bg:            var(--n-50);
  --bg-surface:    var(--n-0);
  --bg-raised:     var(--n-75);
  --text:          var(--n-900);
  --text-soft:     var(--n-800);
  --text-mute:     var(--n-600);
  --accent:        var(--brass-500);
  --accent-text:   var(--brass-700);
  --border:        var(--n-150);
  --border-strong: var(--n-300);

  /* ---------- Layer 3: v3 compatibility aliases ----------
     Every v3 token name survives. Rows marked (changed) moved on
     purpose; see spec §9. */
  --paper:       var(--n-50);
  --paper-2:     var(--n-75);
  --paper-3:     var(--n-100);
  --surface:     var(--n-0);
  --paper-zebra: var(--n-25);
  --rule:        var(--n-150);
  --rule-soft:   var(--n-90);
  --rule-strong: var(--n-300);
  --ink:         var(--n-900);
  --ink-soft:    var(--n-800);
  --ink-mute:    var(--n-600);          /* (changed) #78736A -> #706B62 */
  --gold:        var(--brass-500);
  --gold-bright: var(--brass-400);
  --gold-soft:   var(--brass-300);
  --gold-deep:   var(--brass-700);
  --gold-wash:   var(--brass-wash);
  --gold-tint:   var(--brass-tint);
  --gold-subtle: var(--brass-subtle);
  --imperial:        var(--oxblood-500);
  --imperial-bright: var(--oxblood-400);
  --fs-eyebrow: var(--fs-caption);      /* (changed) 10px -> 12px */
  --fs-meta:    var(--fs-caption);      /* (changed) 11px -> 12px */
  --fs-data:    var(--fs-body);         /* (changed) 13px -> 14px */
  --fs-display: var(--fs-heading);      /* (changed) 15px -> 16px */
  --fs-title:   var(--fs-section);      /* 20px, role renamed */
  --s-1: var(--s-50);
  --s-2: var(--s-100);
  --s-3: var(--s-150);
  --s-4: var(--s-200);
  --s-5: var(--s-300);
  --s-6: var(--s-400);
  --s-7: var(--s-600);
  --radius-xs: var(--r-sm);             /* (changed) 0 -> 4px */
  --radius-sm: var(--r-sm);             /* (changed) 2px -> 4px */
  --radius-md: var(--r-control);        /* (changed) 4px -> 6px */
  --radius-lg: var(--r-container);      /* (changed) 6px -> 12px */
  --shadow-page: var(--shadow-md);
  --shadow-pop:  var(--shadow-lg);
}

/* ============================================================
   Base element styles
   ============================================================ */
* { box-sizing: border-box; }

body {
  margin: 0;
  background-color: var(--bg);
  background-image: var(--paper-noise);
  color: var(--text);
  font-family: var(--font-body);
  font-size: var(--fs-body);
  line-height: var(--lh-body);
}

/* Display serif for page/brand headers only. Garamond stylistic sets
   (small-cap alternates + old-style figures) apply here only. */
h1, h2 {
  font-family: var(--font-display);
  font-weight: 600;
  font-feature-settings: 'ss01', 'cv11';
}
h1 { font-size: var(--fs-page);    line-height: var(--lh-page); }
h2 { font-size: var(--fs-section); line-height: var(--lh-section); }

a {
  color: var(--accent-text);
  text-decoration: none;
}
a:hover { color: var(--imperial); text-decoration: underline; }

::selection {
  background: var(--brass-tint);
  color: var(--text);
}

:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}
```

- [ ] **Step 2: Replace cardinal.css with this exact content**

```css
/* ============================================================
   Cardinal Design System — cardinal.css
   Version: v4.0.0
   The one file an app links. Loads the display/code fonts, then
   tokens, then components. UI text uses the system stack: no
   webfont needed for it.

   Usage (pin to a git tag, never @main):
   <link rel="stylesheet"
     href="https://cdn.jsdelivr.net/gh/tbchonka-cardinal/cardinal-design@v4.0.0/cardinal.css">

   Token-only consumers (e.g. TopLeaseMap) link tokens.css the same way.
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Source+Code+Pro:wght@400..600&display=swap');
@import 'tokens.css';
@import 'components.css';
```

- [ ] **Step 3: Verify every v3 token name still resolves**

Run from the repo root (Git Bash):

```bash
for t in paper paper-2 paper-3 surface rule rule-soft rule-strong ink ink-soft ink-mute gold gold-bright gold-soft gold-deep gold-wash gold-tint gold-subtle paper-zebra imperial imperial-bright ink-blue moss brick brick-bright data-amber data-crimson focus s-1 s-2 s-3 s-4 s-5 s-6 s-7 control-h control-h-sm fs-eyebrow fs-meta fs-body fs-data fs-title fs-display ls-eyebrow radius-xs radius-sm radius-md radius-lg shadow-sm shadow-page shadow-pop grad-gold grad-imperial ease dur paper-noise rule-on-ink bg bg-surface bg-raised text text-soft text-mute accent accent-text border border-strong font-display font-body font-mono; do grep -q -- "--$t:" tokens.css || echo "MISSING --$t"; done
```

Expected: no output. Any `MISSING` line means an alias was dropped; add it before continuing.

- [ ] **Step 4: Verify Source Sans 3 is gone**

Run: `grep -ri "source sans" tokens.css cardinal.css components.css`
Expected: no matches.

- [ ] **Step 5: Commit**

```bash
git add tokens.css cardinal.css
git commit -m "feat: v4 layered tokens (ramps + roles + v3 aliases), system UI sans"
```

---

### Task 3: components.css sweep

Apply Stripe mechanics to every existing `cds-` rule. Leave the `.cds-splash` block (lines from the `cds-splash` banner comment to the end of the file) completely untouched. Every change below is a full replacement of the named rule.

**Files:**
- Modify: `components.css`

**Interfaces:**
- Consumes: Task 2 tokens (`--r-control`, `--r-container`, `--ring`, `--ring-strong`, `--shadow-*`, `--fs-caption`, `--lh-caption`, feedback pairs).
- Produces: the swept classes Task 5 renders. No class names change; new badge variants `.cds-badge-warning`, `.cds-badge-info` appear.

- [ ] **Step 1: Update the file header version**

Header comment: `Version: v3.1.0` becomes `Version: v4.0.0`, and add one line to the header block: `Craft: rings not borders; transitions on background-color and box-shadow only (switch knob transform excepted).`

- [ ] **Step 2: Card**

```css
.cds-card {
  background-color: var(--bg-surface);
  border-radius: var(--r-container);
  box-shadow: var(--ring), var(--shadow-sm);
  overflow: hidden;
  color: var(--text);
  font-family: var(--font-body);
  font-size: var(--fs-body);
  line-height: var(--lh-body);
}

.cds-card-header {
  display: flex;
  align-items: center;
  gap: var(--s-100);
  padding: var(--s-150) var(--s-200);
  background-color: var(--oxblood-500);   /* fallback if gradients unsupported */
  background-image: var(--grad-imperial);
  color: var(--n-50);
  border-bottom: 1px solid var(--accent);
  font-family: var(--font-body);
  font-size: var(--fs-caption);
  line-height: var(--lh-caption);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: var(--ls-eyebrow);
}

.cds-card-body {
  padding: var(--s-200) var(--s-200) var(--s-150);
  overflow-y: auto;
  scrollbar-color: var(--border) transparent;
}
.cds-card-body::-webkit-scrollbar { width: 10px; }
.cds-card-body::-webkit-scrollbar-thumb {
  background: var(--border-strong);
  border-radius: var(--r-sm);
  border: 2px solid var(--bg-surface);
}
.cds-card-body::-webkit-scrollbar-track { background: transparent; }
```

- [ ] **Step 3: Buttons**

```css
.cds-btn {
  padding: var(--s-100) var(--s-200);
  font-family: var(--font-body);
  font-size: var(--fs-caption);
  line-height: var(--lh-caption);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border: none;
  border-radius: var(--r-control);
  background: var(--bg-surface);
  color: var(--text);
  box-shadow: var(--ring), var(--shadow-sm);
  cursor: pointer;
  white-space: nowrap;
  transition: background-color var(--dur) var(--ease),
              box-shadow var(--dur) var(--ease);
}
.cds-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* primary — brass glass. Ink text: paper on brass measures ~2.6:1. */
.cds-btn-primary {
  background-color: var(--brass-500);       /* fallback */
  background-image: var(--grad-gold);
  box-shadow: inset 0 1px 0 rgba(255, 240, 190, 0.4), var(--shadow-brass);
  color: var(--n-900);
}
.cds-btn-primary:hover:not(:disabled) {
  background-color: var(--brass-400);
  background-image: linear-gradient(180deg, var(--brass-300) 0%, var(--brass-400) 100%);
  box-shadow: inset 0 1px 0 rgba(255, 240, 190, 0.4), var(--shadow-md);
}

/* ghost/secondary — white, ring darkens and shadow lifts on hover */
.cds-btn-ghost {
  background: var(--bg-surface);
  color: var(--text);
  box-shadow: var(--ring), var(--shadow-sm);
}
.cds-btn-ghost:hover:not(:disabled) {
  box-shadow: var(--ring-strong), var(--shadow-md);
}

/* danger — solid hot red, distinct from oxblood chrome */
.cds-btn-danger {
  background: var(--brick);
  color: var(--n-0);
  box-shadow: var(--shadow-sm);
}
.cds-btn-danger:hover:not(:disabled) {
  background: var(--brick-bright);
  box-shadow: var(--shadow-md);
}
```

`.cds-btn-icon`: replace only these declarations, keep the rest of the rule:
`border-radius: var(--radius-sm);` becomes `border-radius: var(--r-control);`
the `transition` becomes `transition: background-color var(--dur) var(--ease), box-shadow var(--dur) var(--ease);`
`.cds-btn-icon:hover:not(:disabled)` keeps `background: var(--paper-3); color: var(--ink);` (aliases resolve; color change is instant now, which is the intent).

- [ ] **Step 4: Panel**

```css
.cds-panel {
  background-color: var(--bg-surface);
  border-radius: var(--r-container);
  box-shadow: var(--ring), var(--shadow-lg);
  color: var(--text);
}
```

- [ ] **Step 5: Table**

Replace the `thead th` and `tbody td` rules only (keep the `.cds-table` base rule, zebra, hover, and `.cds-num` as they are):

```css
.cds-table thead th {
  position: sticky;
  top: 0;
  z-index: 1;
  background-color: var(--bg-raised);
  padding: var(--s-100) var(--s-150);
  font-family: var(--font-body);
  font-size: var(--fs-caption);
  line-height: var(--lh-caption);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: var(--ls-eyebrow);
  color: var(--text);
  text-align: left;
  border-bottom: 1px solid var(--border);   /* row dividers stay borders */
  white-space: nowrap;
}
.cds-table tbody td {
  padding: var(--s-100) var(--s-150);
  border-bottom: 1px solid var(--rule-soft);
  color: var(--text);
}
```

- [ ] **Step 6: Fields**

```css
.cds-field { margin-bottom: var(--s-200); }
.cds-field > label,
.cds-label {
  display: block;
  margin-bottom: var(--s-50);
  font-family: var(--font-body);
  font-size: var(--fs-caption);
  line-height: var(--lh-caption);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: var(--ls-eyebrow);
  color: var(--accent-text);
}

.cds-input,
.cds-select,
.cds-field textarea {
  width: 100%;
  box-sizing: border-box;
  padding: var(--s-75) var(--s-150);
  font-family: var(--font-body);
  font-size: var(--fs-body);
  line-height: var(--lh-body);
  color: var(--text);
  background: var(--bg-surface);
  border: none;
  border-radius: var(--r-control);
  box-shadow: var(--ring-strong);
  transition: box-shadow var(--dur) var(--ease);
}
.cds-field textarea { resize: vertical; }

.cds-input:focus,
.cds-select:focus,
.cds-field textarea:focus {
  outline: none;
  box-shadow: 0 0 0 1px var(--accent), 0 0 0 3px var(--brass-tint);
}
.cds-input:disabled,
.cds-select:disabled,
.cds-field textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

- [ ] **Step 7: Pill (Stripe filter-chip pattern)**

```css
.cds-pill {
  display: inline-block;
  padding: var(--s-25) var(--s-100);
  font-family: var(--font-body);
  font-size: var(--fs-caption);
  line-height: var(--lh-caption);
  font-weight: 600;
  color: var(--text-soft);
  background: var(--bg-surface);
  border: none;
  border-radius: var(--r-control);
  box-shadow: var(--ring);
  cursor: pointer;
  white-space: nowrap;
  transition: background-color var(--dur) var(--ease),
              box-shadow var(--dur) var(--ease);
}
.cds-pill:hover {
  box-shadow: var(--ring-strong), var(--shadow-sm);
}
.cds-pill.active {
  color: var(--text);
  background: var(--bg-surface);
  box-shadow: 0 0 0 2px var(--n-900);
}
```

- [ ] **Step 8: Badge (feedback pairs)**

```css
.cds-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--s-75);
  padding: var(--s-25) var(--s-100);
  border-radius: var(--r-sm);
  font-family: var(--font-body);
  font-size: var(--fs-caption);
  line-height: var(--lh-caption);
  font-weight: 600;
  background: transparent;
  color: var(--text-mute);
}
.cds-badge::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}
.cds-badge-success { color: var(--success-text); background: var(--success-bg); }
.cds-badge-error   { color: var(--danger-text);  background: var(--danger-bg); }
.cds-badge-warning { color: var(--warning-text); background: var(--warning-bg); }
.cds-badge-info    { color: var(--info-text);    background: var(--info-bg); }
.cds-badge-muted   { color: var(--text-mute); background: transparent; font-style: italic; }
```

- [ ] **Step 9: Eyebrow, tabs, stat**

`.cds-eyebrow` and `.cds-stat-label`: change `font-size: var(--fs-eyebrow);` to `font-size: var(--fs-caption); line-height: var(--lh-caption);` in both (aliases would resolve anyway; components use canonical names).

`.cds-tab`: change `font-size: var(--fs-meta);` to `font-size: var(--fs-caption); line-height: var(--lh-caption);` and delete its `transition` line (color changes are instant under the motion rule).

`.cds-stat-value`: change `font-size: 14px; font-weight: 500;` to `font-size: var(--fs-body); line-height: var(--lh-body); font-weight: 600;`.

- [ ] **Step 10: Switch**

Replace only these declarations inside the existing rules (structure and knob transform stay):
- `.cds-switch-slider`: `background: var(--paper-3); border: 1px solid var(--rule);` becomes `background: var(--n-100); border: 1px solid var(--border);` and the transition stays `background var(--dur) var(--ease), border-color var(--dur) var(--ease)`.
- `.cds-switch input:checked + .cds-switch-slider`: `background: var(--gold); border-color: var(--gold);` becomes `background: var(--accent); border-color: var(--accent);`.
- Knob rules keep `transform` (the sanctioned exception) and their current colors via aliases.

- [ ] **Step 11: No raw hex check**

Run: `grep -nE "#[0-9a-fA-F]{3,6}\b" components.css`
Expected: no matches (the primary button's inset highlight is an rgba(), which this pattern ignores; the splash SVG colors live in index.html). If any hex appears, tokenize it.

- [ ] **Step 12: Commit**

```bash
git add components.css
git commit -m "feat: sweep cds- components onto v4 mechanics (rings, radii, motion)"
```

---

### Task 4: New components (card footer, empty state, banner)

**Files:**
- Modify: `components.css` (append before the `.cds-splash` block)

**Interfaces:**
- Consumes: Task 2 tokens.
- Produces: `.cds-card-footer`, `.cds-empty`, `.cds-banner` (+ `.cds-banner-action`, status variants) for Task 5's showcase.

- [ ] **Step 1: Append these rules immediately before the cds-splash banner comment**

```css
/* ===== Card footer (three-band card) ===== */
/* White footer band with right-aligned actions. When a card has a
   footer, the body band tints to bg-raised: the tinted middle band
   marks "things you can change" and binds save/cancel to this card,
   not to the page. */
.cds-card-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: var(--s-100);
  padding: var(--s-150) var(--s-200);
  background: var(--bg-surface);
  border-top: 1px solid var(--border);
  border-radius: 0 0 var(--r-container) var(--r-container);
}
.cds-card:has(.cds-card-footer) .cds-card-body {
  background: var(--bg-raised);
}

/* ===== Empty state ===== */
/* Dashed border says "this container is real but unfilled". */
.cds-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--s-400) var(--s-300);
  border: 1px dashed var(--border-strong);
  border-radius: var(--r-container);
  color: var(--text-mute);
  font-family: var(--font-body);
  font-size: var(--fs-body);
  line-height: var(--lh-body);
}

/* ===== Inline banner ===== */
/* Neutral by default: informs without alarming. Colored tints are
   reserved for real feedback via the status variants. */
.cds-banner {
  display: flex;
  align-items: center;
  gap: var(--s-150);
  padding: var(--s-150) var(--s-200);
  background: var(--bg);
  border-radius: var(--r-control);
  font-family: var(--font-body);
  font-size: var(--fs-body);
  line-height: var(--lh-body);
  color: var(--text);
}
.cds-banner > svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: var(--text-soft);
}
.cds-banner-action {
  margin-left: auto;
  flex-shrink: 0;
  color: var(--accent-text);
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}
.cds-banner-success { background: var(--success-bg); color: var(--success-text); }
.cds-banner-success > svg,
.cds-banner-success .cds-banner-action { color: var(--success-text); }
.cds-banner-error   { background: var(--danger-bg);  color: var(--danger-text); }
.cds-banner-error > svg,
.cds-banner-error .cds-banner-action   { color: var(--danger-text); }
.cds-banner-warning { background: var(--warning-bg); color: var(--warning-text); }
.cds-banner-warning > svg,
.cds-banner-warning .cds-banner-action { color: var(--warning-text); }
.cds-banner-info    { background: var(--info-bg);    color: var(--info-text); }
.cds-banner-info > svg,
.cds-banner-info .cds-banner-action    { color: var(--info-text); }
```

- [ ] **Step 2: Commit**

```bash
git add components.css
git commit -m "feat: add cds-card-footer, cds-empty, cds-banner"
```

---

### Task 5: Showcase update (index.html)

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: everything from Tasks 2-4.

- [ ] **Step 1: Version and philosophy**

- Both version strings (`<span class="sc-version">v3.1.0</span>` in the masthead and `v3.1.0` in `.sc-footer`) become `v4.0.0`.
- The masthead h1 rule in the showcase `<style>` block: `font-size: 32px;` becomes `font-size: var(--fs-page);`.
- Replace the `.sc-philosophy` paragraph text with:

```
A layered heritage-parchment visual language with Stripe-grade mechanics: warm off-white canvas, crisp white surfaces held by hairline rings and two-tint shadows, deep oxblood chrome, and a single brass accent that always means "actionable." Type is Garamond for display over the system UI sans (tabular figures for data), with Source Code Pro reserved for code. Five type sizes, a 4px spacing grid, 6px controls inside 12px containers, and 150ms motion on background and shadow only.
```

- [ ] **Step 2: Color swatches**

Replace the entire `sc-swatch-grid` div content with swatches for the v4 primitives, in this order (same swatch markup pattern as now: `--name` plus hex in the meta; use `style="color: var(--paper-3);"` on the hex line for dark swatches):

1. Neutral ramp: `--n-0` #FFFFFF, `--n-25` #FAF8F5, `--n-50` #F9F7F2 (canvas), `--n-75` #F2EFE9, `--n-90` #EFEBE2, `--n-100` #EBE6DC, `--n-150` #E6E1D8, `--n-300` #C8C2B5, `--n-600` #706B62 (dark), `--n-800` #524E48 (dark), `--n-900` #161514 (dark)
2. Brass: `--brass-300` #D9BC7E, `--brass-400` #C9A45C, `--brass-500` #B8934A (dark hex line), `--brass-700` #8A6D33 (dark; label it `text/links`), `--brass-subtle` #F6F1E5, `--brass-wash` rgba(184,147,74,.08), `--brass-tint` rgba(184,147,74,.16)
3. Oxblood: `--oxblood-400` #5E1620 (dark), `--oxblood-500` #4A1017 (dark), `--oxblood-700` #38090F (dark), `--grad-gold`, `--grad-imperial` (keep the two existing gradient swatches, relabel unchanged)
4. Feedback pairs, shown as text-on-tint: for each of success/danger/warning/info, one swatch whose color block carries the tint background with the text color rendered as a sample word, e.g.:

```html
<div class="sc-swatch"><div class="sc-swatch-color" style="background: var(--success-bg); display:flex; align-items:center; justify-content:center;"><span style="color: var(--success-text); font-weight:600;">Synced</span></div><div class="sc-swatch-meta"><span class="sc-swatch-name">--success-text / -bg</span><span class="sc-swatch-hex">#1B4D3E on #E7F0E9</span></div></div>
```

(same pattern for `--danger-text/-bg` "Failed" #8B1E1E on #FBE9E5, `--warning-text/-bg` "Check" #8A5A00 on #FBF3DC, `--info-text/-bg` "Note" #1B365D on #E8EEF6)
5. Reds and data: `--brick` #c0392b (dark), `--brick-bright` #d64a3b (dark), `--ink-blue`, `--moss`, `--data-amber`, `--data-crimson` (all dark), `--rule-on-ink` (keep existing swatch), and one scrim swatch: `--scrim` rgba(82,78,72,.55) on a patterned background is not needed; a plain block with the rgba background is fine.

- [ ] **Step 3: Spacing rows**

Replace the seven spacing rows with ten, same row markup: `--s-25 · 2px`, `--s-50 · 4px`, `--s-75 · 6px`, `--s-100 · 8px`, `--s-150 · 12px`, `--s-200 · 16px`, `--s-300 · 24px`, `--s-400 · 32px`, `--s-600 · 48px`, `--s-800 · 64px` (bar widths match the px). Add below the rows:

```html
<p class="sc-section-sub" style="margin-top: var(--s-300);">8 inside compact controls · 12 between related items · 16 between fields · 24 between regions · 32 between sections · 48 page bottom. Old --s-1 .. --s-7 alias onto these.</p>
```

- [ ] **Step 4: Type ramp rows**

Replace the six type rows with five:

```html
<div class="sc-type-row"><span class="sc-type-label">--fs-caption 12/16</span><span style="font-size: var(--fs-caption); line-height: var(--lh-caption);">Captions, meta, labels · <span style="text-transform: uppercase; letter-spacing: var(--ls-eyebrow); color: var(--accent-text); font-weight: 600;">Eyebrow</span></span></div>
<div class="sc-type-row"><span class="sc-type-label">--fs-body 14/20</span><span style="font-size: var(--fs-body); line-height: var(--lh-body);">Body, controls, data 1,024.50 · <b style="font-weight:600;">emphasis 600</b></span></div>
<div class="sc-type-row"><span class="sc-type-label">--fs-heading 16/24</span><span style="font-size: var(--fs-heading); line-height: var(--lh-heading); font-weight: 700;">Card heading, sans 700</span></div>
<div class="sc-type-row"><span class="sc-type-label">--fs-section 20/28</span><span style="font-family: var(--font-display); font-size: var(--fs-section); line-height: var(--lh-section); font-weight: 600;">Section Title, Garamond</span></div>
<div class="sc-type-row"><span class="sc-type-label">--fs-page 28/36</span><span style="font-family: var(--font-display); font-size: var(--fs-page); line-height: var(--lh-page); font-weight: 600;">Page Title, Garamond</span></div>
```

Add below the rows:

```html
<p class="sc-section-sub" style="margin-top: var(--s-150);">Five sizes only. Inside a size, hierarchy comes from weight (400/600/700) and ink tier (--text, --text-soft, --text-mute), never a new size.</p>
```

- [ ] **Step 5: Misc list**

Replace the `sc-misc-list` items with:

```html
<div class="sc-misc-item"><b>--r-sm</b> 4px, badges</div>
<div class="sc-misc-item"><b>--r-control</b> 6px, buttons/inputs/pills</div>
<div class="sc-misc-item"><b>--r-container</b> 12px, cards/panels</div>
<div class="sc-misc-item"><b>--r-full</b> 9999em, toolbar pills</div>
<div class="sc-misc-item"><b>--ring</b> hairline via box-shadow</div>
<div class="sc-misc-item"><b>--ring-strong</b> hover/input ring</div>
<div class="sc-misc-item"><b>--shadow-sm</b> resting cards</div>
<div class="sc-misc-item"><b>--shadow-md</b> dropdowns, hover lift</div>
<div class="sc-misc-item"><b>--shadow-lg</b> modals, floating panels</div>
<div class="sc-misc-item"><b>--shadow-brass</b> primary button</div>
<div class="sc-misc-item"><b>--dur / --dur-long</b> 150ms / 300ms</div>
<div class="sc-misc-item"><b>--ease</b> cubic-bezier(0,.09,.4,1)</div>
<div class="sc-misc-item"><b>--scrim</b> rgba(82,78,72,.55), never black</div>
<div class="sc-misc-item"><b>--paper-noise</b> canvas texture only</div>
```

- [ ] **Step 6: New component blocks**

After the existing Card block, insert a three-band card block:

```html
<!-- Three-band card -->
<div class="sc-component-block">
  <p class="sc-component-class"><code>.cds-card-footer</code> — three-band edit card (tinted body binds Save/Cancel to this card)</p>
  <div class="cds-card sc-card-demo">
    <div class="cds-card-header">Payout Settings</div>
    <div class="cds-card-body">
      <div class="cds-field">
        <label>Statement Descriptor</label>
        <input class="cds-input" type="text" value="CARDINAL RES">
      </div>
    </div>
    <div class="cds-card-footer">
      <button class="cds-btn cds-btn-ghost">Cancel</button>
      <button class="cds-btn cds-btn-primary">Save</button>
    </div>
  </div>
  <pre class="sc-snippet"><code>&lt;div class="cds-card"&gt;
  &lt;div class="cds-card-header"&gt;Payout Settings&lt;/div&gt;
  &lt;div class="cds-card-body"&gt;...fields...&lt;/div&gt;
  &lt;div class="cds-card-footer"&gt;
    &lt;button class="cds-btn cds-btn-ghost"&gt;Cancel&lt;/button&gt;
    &lt;button class="cds-btn cds-btn-primary"&gt;Save&lt;/button&gt;
  &lt;/div&gt;
&lt;/div&gt;</code></pre>
</div>
```

Before the Eyebrow block, insert empty-state and banner blocks:

```html
<!-- Empty state -->
<div class="sc-component-block">
  <p class="sc-component-class"><code>.cds-empty</code></p>
  <div class="cds-empty" style="max-width: 420px;">No production records for this lease yet.</div>
  <pre class="sc-snippet"><code>&lt;div class="cds-empty"&gt;No production records for this lease yet.&lt;/div&gt;</code></pre>
</div>

<!-- Banner -->
<div class="sc-component-block">
  <p class="sc-component-class"><code>.cds-banner</code> + <code>-success</code> / <code>-error</code> / <code>-warning</code> / <code>-info</code></p>
  <div style="display: flex; flex-direction: column; gap: var(--s-150); max-width: 560px;">
    <div class="cds-banner">
      <svg viewBox="0 0 16 16" fill="currentColor"><circle cx="8" cy="8" r="7"/></svg>
      Monthly production sync runs tonight at 02:00.
      <span class="cds-banner-action">View schedule</span>
      <button class="cds-btn-icon" aria-label="Dismiss"><svg viewBox="0 0 16 16" fill="currentColor"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="2"/></svg></button>
    </div>
    <div class="cds-banner cds-banner-warning">
      <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 1L15 14H1z"/></svg>
      3 wells report zero volume for 2026-05.
      <span class="cds-banner-action">Review</span>
    </div>
  </div>
  <pre class="sc-snippet"><code>&lt;div class="cds-banner"&gt;
  &lt;svg&gt;...&lt;/svg&gt; Message text
  &lt;span class="cds-banner-action"&gt;Action&lt;/span&gt;
&lt;/div&gt;
&lt;div class="cds-banner cds-banner-warning"&gt;...&lt;/div&gt;</code></pre>
</div>
```

In the Badge block, add the two new variants to the demo row and snippet:
`<span class="cds-badge cds-badge-warning">Zero Volume</span>` and `<span class="cds-badge cds-badge-info">Pending Review</span>`.

- [ ] **Step 7: Render check**

Start the showcase: preview_start with name `cardinal-design-showcase`, open `http://localhost:8931/`. Check: no console errors; cards show 12px corners with rings; pills' active state is a 2px ink ring; primary button shows ink text on brass; the three-band card's body band is tinted; banner and empty state render; type ramp shows Garamond only on the two title rows. Take a screenshot for the record.

- [ ] **Step 8: Commit**

```bash
git add index.html
git commit -m "feat: v4 showcase (ramps, feedback pairs, three-band card, banner, empty)"
```

---

### Task 6: README, final verification, release gate

**Files:**
- Modify: `README.md`
- Modify: `C:\Users\ThatcherChonka\CardinalCore\NEXT.md` (workspace root, outside this repo)

- [ ] **Step 1: README updates**

- Intro paragraph: replace the type-system sentence so the paragraph reads that type is "Garamond for display over the system UI sans (numbers in tabular figures), with Source Code Pro reserved for code", and append: "v4 adds the Stripe-craft mechanics: hairline rings instead of borders, two-tint shadows, a five-size type scale, 6px controls inside 12px containers, and a single-accent rule (brass means actionable; oxblood is chrome)."
- Both jsDelivr pins: `@v3.1.0` becomes `@v4.0.0`.
- Class reference table, add rows:

```markdown
| `.cds-card-footer` | White action band completing the three-band edit card; tints the body via `:has()` |
| `.cds-empty` | Dashed-border empty state with a centered muted message |
| `.cds-banner` | Neutral inline notice; `-success`/`-error`/`-warning`/`-info` variants use the feedback tint pairs |
```

- Badge row: extend to mention `-warning` and `-info` variants.

- [ ] **Step 2: Full verification**

Run: `python docs/superpowers/tools/contrast.py` — Expected: all PASS, exit 0.
Run the Task 2 Step 3 alias loop again — Expected: no output.
Reload `http://localhost:8931/` — Expected: renders clean, no console errors.

- [ ] **Step 3: USER GATE — stop here**

Post a screenshot of the showcase and ask Thatcher to verify in the browser (`http://localhost:8931/`). Call out for explicit approval: 14px body, 12px card corners, ink-on-brass primary buttons, ring-active pills. Do not proceed until approved. If changes are requested, make them, re-run Step 2, and re-ask.

- [ ] **Step 4: Tag and wrap (after approval only)**

```bash
git add README.md
git commit -m "docs: v4 README (pins, craft rules, new components)"
git tag v4.0.0
```

Update workspace `NEXT.md` item 7: append to it that cardinal-design v4.0.0 ("Stripe-craft") is tagged as of today's date, that the ink-on-brass primary button resolves the open primary-button contrast question, and that round 2 (TopLeaseMap vendored-token refresh plus app-level pass: progressive disclosure, organization, icons; then Minerva/Janus pin bumps) is next and needs its own brainstorm. Do not push; pushing happens via the ship skill when Thatcher says so.
