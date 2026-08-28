# Card Grammar v6.1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move TopLeaseMap's `src/cards.css` card grammar into cardinal-design as `cds-` classes (tag v6.1.0), then cut both TopLeaseMap apps over and delete the file.

**Architecture:** Faithful port per the spec's name map (`docs/superpowers/specs/2026-08-28-card-grammar-v6-1-design.md`). Two classes merge into existing upstream names; four Minerva-only classes move to `title.css` unchanged; five dead classes are deleted. Terminus consumes by vendoring a new `src/cardinal-cards.css`; Minerva bumps its CDN pin v5.0.0 → v6.1.0.

**Tech Stack:** Plain CSS, git tags, jsDelivr CDN, `node --test`.

## Global Constraints

- Tokens do not change: every var the grammar uses exists in tokens.css v6.0.0. If a var seems missing during the port, STOP — do not add tokens.
- The tag must be pushed before any consumer pins it (cardinal-design hard rule).
- Recipes port unchanged. No redesigns, no value "improvements".
- State classes stay unprefixed: `.active`, `.is-missing`, `.saving`/`.saved`/`.error`, `--open` modifier.
- TopLeaseMap repos: never `supabase db push`; this plan touches no data.
- Both apps must look pixel-identical after cutover except where the spec names a merge (header/body paddings — preserved by app override blocks below).

**Source of truth for recipes:** TopLeaseMap `src/cards.css` at commit `62dd19d` (578 lines). The name map is the spec's table.

---

### Task 1: Port the grammar into components.css (cardinal-design)

**Files:**
- Modify: `C:\Users\ThatcherChonka\CardinalCore\cardinal-design\components.css` (Card section, lines 15–56)
- Modify: `C:\Users\ThatcherChonka\CardinalCore\cardinal-design\cardinal.css` (version header + example pin URL)

**Interfaces:**
- Produces: the full `.cds-card-*` / `.cds-fact-*` / `.cds-ct-*` / `.cds-hero-*` class set per the spec name map, all inside the `/* ===== Card ===== */` section so Task 4 can vendor that one contiguous section.

- [ ] **Step 1:** In `components.css`, update the file header `Version: v6.0.0` → `Version: v6.1.0` and extend the Card section comment: the card grammar (fact rows, card tables, tab bars, panels, notes, hero editables) arrived from TopLeaseMap `cards.css` in v6.1.0.
- [ ] **Step 2:** Merge deltas into the two existing classes, keeping their current recipes as the base:
  - `.cds-card-header`: no property changes (apps override paddings locally).
  - `.cds-card-body`: add `flex: 1; min-height: 0;` (from `.card-content-body`; inert outside flex parents).
- [ ] **Step 3:** Append, INSIDE the Card section (before `/* ===== Buttons ===== */`), every remaining living block from `src/cards.css` renamed per the spec map, comments carried over, recipes verbatim: `cds-card-header-actions`, `cds-card-action-btn`, `cds-card-id-pill`, `cds-card-identity-name`, `cds-card-tab-bar` (+`--underline`), `cds-card-tab`, `cds-card-panel`, `cds-card-panel-title`, `cds-card-notes`, `cds-card-notes-edit`, `cds-card-notes-status` (+`.saving`/`.saved`/`.error`), `cds-card-note` (was `wc-note`), `cds-fact-row` (+`--solo`/`--3`/`--5`), `cds-fact-cell`, `cds-fact-label`, `cds-fact-value`, `cds-fact-status-box`, `cds-card-table`, `cds-card-lv-table`, `cds-ct-row`, `cds-ct-head`, `cds-ct-cell`, `cds-ct-num`, `cds-ct-link`, `cds-ct-section`, `cds-ct-section-row`. Compound selectors rename BOTH halves (e.g. `.card-tab-bar--underline .card-tab` → `.cds-card-tab-bar--underline .cds-card-tab`; `.fact-cell.is-missing .fact-label` → `.cds-fact-cell.is-missing .cds-fact-label`; the `.ct-cell.is-missing` half of that group; `.ct-row:nth-child(odd):not(.ct-head):not(.ct-section-row)` → all three; `.card-lv-table .ct-row` → both).
  - Do NOT port: `card-hero-grid`, `hero-stat`, `hero-label`, `card-section-divider`, `card-section-header` (dead); `card-type-label`, `card-main-title`, `hero-sep`, `card-footer`, `hero-value` + every `.hero-value.hero-editable*` compound (Minerva-local, Task 4 Step 7); `hero-dropdown-panel`/`-option`/`-check`/`-done`, `hero-number-input` (Terminus-local, Task 4 Step 7). `fact-cell--identity` has no CSS rule anywhere; it is a hook class only, do not invent a rule.
- [ ] **Step 4:** In `cardinal.css`, bump `Version: v6.0.0` → `v6.1.0` and the example URL `@v6.0.0` → `@v6.1.0`. tokens.css is untouched.
- [ ] **Step 5:** Sanity check: `python docs/superpowers/tools/contrast.py` from the cardinal-design root. Expected: exit 0 (no palette change).

### Task 2: Showcase and README (cardinal-design)

**Files:**
- Modify: `C:\Users\ThatcherChonka\CardinalCore\cardinal-design\index.html`
- Modify: `C:\Users\ThatcherChonka\CardinalCore\cardinal-design\README.md`

- [ ] **Step 1:** Add one showcase section "Card grammar (v6.1.0)" to `index.html`, following the page's existing section markup pattern: a demo card composing `cds-card` > `cds-card-header` (with `cds-card-header-actions` + two `cds-card-action-btn`), a `cds-fact-row` with `cds-fact-cell`/`cds-fact-label`/`cds-fact-value` (+ one `is-missing` cell and one `cds-fact-status-box`), a `cds-card-tab-bar--underline` with three `cds-card-tab` (one `.active`), a `cds-card-body` holding a `cds-card-table` with `cds-ct-head`/`cds-ct-row`/`cds-ct-cell`/`cds-ct-num` rows and one `cds-ct-section`, a `cds-card-panel` with `cds-card-panel-title` + `cds-card-notes`, a `cds-card-notes-status saved` badge, and a `cds-card-note`. Show it once light and once wrapped in `.cds-dark`.
- [ ] **Step 2:** Add the new classes to README.md's class reference, one line each, same format as existing entries.
- [ ] **Step 3:** Open `index.html` in the browser and eyeball both showcase cards (light and dark scope).

### Task 3: Commit, tag, push (cardinal-design)

- [ ] **Step 1:** `git add -A; git commit -m "v6.1.0: card grammar ported from TopLeaseMap cards.css"`
- [ ] **Step 2:** `git tag v6.1.0; git push; git push origin v6.1.0`
- [ ] **Step 3:** Verify the CDN serves it before touching consumers: fetch `https://cdn.jsdelivr.net/gh/tbchonka-cardinal/cardinal-design@v6.1.0/components.css` and confirm it contains `cds-fact-row`. jsDelivr can lag a minute on a fresh tag; retry, don't fork.

### Task 4: Vendor + rename cutover (TopLeaseMap, one commit)

**Files:**
- Create: `src/cardinal-cards.css` (vendored Card section)
- Modify: `src/main.js:2`, `title.html:8-9`, `ledger-lab.html:6`
- Modify (renames): `src/cardkit.js`, `src/leasecard.js`, `src/wellcard.js`, `src/clustercard.js`, `src/cardhtml.js` (comments), `src/style.css`, `src/app-template.js`, `src/title/title.css`, `src/title/table.css`, `src/title/views/docdetail.js`, `src/title/views/docspanel.js`, `src/title/views/partiespanel.js`, `src/title/views/partycard.js`, `src/title/views/inlinefield.js`, `tests/cardkit.test.mjs`, `tests/leasecard.test.mjs`, `tests/wellcard.test.mjs`, `tests/clustercard.test.mjs`
- Delete: `src/cards.css`

**Interfaces:**
- Consumes: tag v6.1.0 live on the CDN (Task 3).
- Produces: both apps running on the `cds-` names; `cards.css` gone.

- [ ] **Step 1:** Create `src/cardinal-cards.css`: the entire `/* ===== Card ===== */` section of components.css v6.1.0, verbatim, under a header comment matching `src/cardinal-tokens.css`'s style ("Vendored from cardinal-design v6.1.0 (components.css Card section). Re-copy on tag bump, never edit here.").
- [ ] **Step 2:** `src/main.js:2` — replace `import './cards.css';` with `import './cardinal-cards.css';` (comment: vendored card grammar, cardinal-design v6.1.0).
- [ ] **Step 3:** `title.html` — bump line 8 pin `@v5.0.0` → `@v6.1.0`; delete line 9 (`<link rel="stylesheet" href="/src/cards.css" />`). `ledger-lab.html` — bump pin `@v5.0.0` → `@v6.1.0`.
- [ ] **Step 4:** Apply the spec name map as literal find-and-replace across the rename files, LONGEST NAME FIRST within each family (`card-tab-bar--underline` before `card-tab-bar` before `card-tab`; `card-fact-row--solo/--3/--5` before `card-fact-row`; `fact-cell--identity` and `fact-cell--stack` before `fact-cell`; `ct-section-row` before `ct-section`; `card-notes-edit`/`card-notes-status` before `card-notes`). Renames: `card-header-bar`→`cds-card-header`, `card-content-body`→`cds-card-body`, `card-fact-row*`→`cds-fact-row*`, `wc-note`→`cds-card-note`, `ct-*`→`cds-ct-*`, everything else per the map. Do NOT rename (names live on unchanged): the entire hero family (`hero-value`, `hero-editable`, `hero-editable--open`, `hero-dropdown-*`, `hero-number-input`, `hero-sep`), `card-type-label`, `card-main-title`, `card-footer`, and the neighbors `.card-tab-content`, `.wc-api-link`, `.wc-lease-link`, `.dd-extract-row` (`ct-row` appears as a substring of `dd-extract-row` — use word-boundary-safe replacement).
  Known hazard sites to hand-check after the sweep:
  - `src/cardkit.js:76-79` — the fact-row modifier is built from separate literals (`' card-fact-row--solo'` etc. plus `` `card-fact-row${mod}` ``); all four literals must change.
  - `src/cardkit.js:24` — `` `fact-cell${...}` `` template plus the caller-supplied `cellClass` values `fact-cell--identity` (cardkit.js:83, leasecard.js:58) and `fact-cell--stack` (tests only).
  - `src/leasecard.js:197-198` — class names inside template-literal SELECTORS (`` `textarea.card-notes-edit[data-airtable-id=...]` ``, `` `.card-notes-status[...]` `` if present).
  - `src/leasecard.js:205` — `` `card-notes-status${cls ? ' ' + cls : ''}` `` (state suffixes `saving`/`saved`/`error` stay bare).
  - `src/style.css:792/795/798` — `.lease-wells-table .ct-row` etc. compound selectors.
  - `src/style.css:804` — `.fact-cell--identity .lease-name-edit`.
  - `src/title/views/inlinefield.js` — emits `card-notes-status` and `card-notes-edit` (rename) alongside `hero-value`/`hero-editable` (keep).
- [ ] **Step 5:** App binding blocks preserving current geometry where the merged upstream recipes differ. In `src/style.css`, next to the `#lease-card` block:

```css
/* Bindings for the upstream card grammar (cardinal-design v6.1.0).
   The pinned card keeps its 48px right header clearance for the
   absolute close X, and the body keeps its pre-port paddings. */
#lease-card .cds-card-header { padding: 9px 48px 8px 18px; }
#lease-card .cds-card-body { padding: 14px 18px 10px; }
```

  In `src/title/title.css`, next to the existing header-bar binding (~line 1707):

```css
/* Pre-v6.1 cards.css geometry, kept as Minerva bindings after the
   upstream merge (cardinal-design v6.1.0). */
.cds-card-header { padding: 9px 48px 8px 18px; }
.cds-card-body { padding: 14px 18px 10px; }
```

- [ ] **Step 6:** `#lease-card` onto `.cds-card`: in `src/app-template.js`, add `cds-card` to the `#lease-card` element's class attribute (keep `hidden` handling intact). In `src/style.css` `#lease-card` block, delete only the props `.cds-card` now supplies with identical values via aliases: `background-color: var(--surface)`, `overflow: hidden`, `font-family: var(--font-body)`, `font-size: var(--fs-body)`, `color: var(--ink)`. KEEP: position/top/right/width/max-height/display/flex-direction/z-index/animation, `border-radius: var(--radius-lg)` and `box-shadow: var(--ring), var(--shadow-pop)` (stronger than the upstream resting shadow), and `line-height: 1.5` unless tokens.css `--lh-body` is exactly 1.5 (check; if equal, delete it too).
- [ ] **Step 7:** Split the app-local blocks out of `src/cards.css`, names unchanged, then delete the file:
  - Into `src/title/title.css`, under one comment ("Minerva-only card classes, moved from the dissolved cards.css (2026-08-28): only Minerva emits these."): `.card-type-label` (+ its `::before` swatch rule), `.card-main-title`, `.hero-sep`, `.card-footer`, `.hero-value`, and the `.hero-value.hero-editable` / `:hover` / `::after` / `--open::after` compounds. Do NOT bring the two `[data-field="acreage"]` rules — they are dead on both sides (note this in the comment).
  - Into `src/style.css`, next to the lease-card editor styles, under one comment ("Lease-card dropdown machinery, moved from the dissolved cards.css (2026-08-28): leasecard.js is the only emitter. hero-editable itself is a bare JS hook in Terminus — the visual recipes are Minerva's."): `.hero-dropdown-panel`, `.hero-dropdown-option` (+`:hover`, `.is-selected`), `.hero-dropdown-check` (+`:hover`), `.hero-dropdown-done` (+`:hover`), `.hero-number-input` (+ its spin-button suppression rules).
- [ ] **Step 8:** `npm test`. Expected: all pass (test files were renamed in Step 4). `npm run build`. Expected: clean build, no unresolved import.
- [ ] **Step 9:** Grep the repo for stragglers: `card-header-bar|card-content-body|card-hero-grid|hero-stat|hero-label|card-section-divider|card-section-header|wc-note|card-tab-bar|card-fact-row|fact-status-box|card-id-pill|hero-dropdown|card-lv-table` across `src/` and `tests/` should return only `src/CLAUDE.md` doc prose (fixed in Task 6) and Minerva's four kept names. `ct-row|ct-cell|ct-head` should return nothing outside `cds-` forms and `.dd-extract-row`.

### Task 5: Browser verification (TopLeaseMap)

- [ ] **Step 1:** `npm run dev`, open Terminus: click a lease (card: header actions, fact row, id pill, underline tabs, wells table, PPQ tab section rows, Notes editor + status badge), a well (tabs, table, `cds-card-note` empty states), a cluster, and one small card (parcel). All dark, all shaped exactly as before.
- [ ] **Step 2:** Exercise the editors: open a Candidate dropdown (hero dropdown panel renders into `document.body` — confirm it still styles), the Acres number input, type in Notes and watch the status badge cycle saving → saved.
- [ ] **Step 3:** Open `/title.html` (Minerva): a document detail card (type label + swatch, main title, hero values, editable ring, footer), the docs panel, parties panel, a party card. Search view for the record rows. Confirm the CDN v6.1.0 load in the network tab and zero 404s.
- [ ] **Step 4:** Screenshot the lease card and one Minerva panel for the ship note.

### Task 6: Docs + ship (TopLeaseMap)

- [ ] **Step 1:** `src/CLAUDE.md`: rewrite the `cards.css` bullet as `cardinal-cards.css` (vendored Card section, v6.1.0, re-copy on tag bump; class names now `cds-*`; Minerva-only quartet lives in `title.css`). Sweep its prose for old class names (`.card-header-bar`, `.well-card-tab-bar` note, etc.).
- [ ] **Step 2:** Root `CLAUDE.md` Design system section: both pins now v6.1.0 — CDN (title.html, ledger-lab.html) and the two vendored files (`src/cardinal-tokens.css` tokens still copied at v6.0.0 values under a v6.1.0-compatible header note — leave its header alone since tokens did not change; `src/cardinal-cards.css` at v6.1.0). State that the v5/v6 divergence is over.
- [ ] **Step 3:** `docs/NEXT.md`: delete the "Push the card grammar upstream" item. `docs/HISTORY.md`: one dated entry.
- [ ] **Step 4:** Commit `feat: adopt cardinal-design v6.1.0 card grammar, dissolve cards.css`, push, confirm Vercel picks it up.
