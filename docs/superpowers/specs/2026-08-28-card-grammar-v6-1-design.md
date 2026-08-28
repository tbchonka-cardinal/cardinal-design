# Card grammar v6.1.0 — design

Status: shipped 2026-08-28 (v6.1.0)

## What this is

TopLeaseMap's `src/cards.css` (the shared Terminus/Minerva card grammar)
moves into `components.css` under the `cds-` prefix. The app file
dissolves: shared grammar comes here, app bindings stay in each app's
own CSS, dead classes die. This closes the TopLeaseMap NEXT.md item
"push the card grammar upstream."

## Decisions

1. **Faithful port.** Every living class ports with its recipe
   unchanged, renamed under the `cds-` prefix. No redesigns ride
   along. Every var the grammar uses already exists in tokens v6.0.0
   (the v3 alias layer), so tokens.css does not change.
2. **Two merges, no new twins.** `components.css` already has
   `.cds-card-header` and `.cds-card-body`, generalized from an older
   Terminus. The ported near-twins (`card-header-bar`,
   `card-content-body`) merge INTO those names. The existing upstream
   recipes win; each app overrides locally where its computed look
   differed (the 48px right header padding that clears the absolute
   close X, the body's `flex: 1; min-height: 0` sizing and exact
   paddings). `card-footer` does NOT merge into `.cds-card-footer` —
   they differ in layout (block vs flex-end) and `card-footer` is
   Minerva-only in production, so it goes app-local under decision 4.
   Everything else is a new class, so the release is additive:
   **v6.1.0**.
3. **Dead classes are deleted, not ported:** `card-hero-grid`,
   `hero-stat`, `hero-label`, `card-section-divider`,
   `card-section-header`. Zero production references.
4. **Minerva-only classes go app-local, not upstream:**
   `card-type-label`, `card-main-title`, `hero-sep`, `card-footer`
   move verbatim into `title.css`, names unchanged. Only Minerva
   emits them (Terminus tests assert `card-footer`'s absence).
5. **The hero/editable/dropdown machinery does not come upstream.**
   Every editable recipe is the compound `.hero-value.hero-editable`,
   and the Prism rebuild (2026-08-25) moved Terminus onto
   `fact-value hero-editable` — so in Terminus those recipes match
   nothing and `hero-editable` is a bare JS hook. Actual ownership:
   `hero-value` and its compounds are Minerva-only (docdetail,
   inlinefield, `table.css`) and move to `title.css`; the
   `hero-dropdown-*` panel machinery and `hero-number-input` are
   lease-card-only and move to `style.css`. Names unchanged
   everywhere. The two `[data-field="acreage"]` compound rules are
   dead on both sides (Terminus has the data-field but no
   `hero-value`; Minerva has `hero-value` but no acreage field) and
   are deleted.
6. **State classes stay unprefixed:** `.active`, `.is-missing`,
   `.saving`/`.saved`/`.error` on the notes status, `--open` on the
   editable. Same convention as `.cds-pill.active`.
7. **`.cds-tabs` (dot style) is untouched.** The card tab grammar is
   a different design and arrives as `.cds-card-tab-bar` /
   `.cds-card-tab` with the `--underline` modifier.

## Name map

| cards.css | components.css v6.1.0 |
|---|---|
| `card-header-bar` | `cds-card-header` (merge into existing) |
| `card-content-body` | `cds-card-body` (merge into existing) |
| `card-header-actions` | `cds-card-header-actions` |
| `card-action-btn` | `cds-card-action-btn` |
| `card-id-pill` | `cds-card-id-pill` |
| `card-identity-name` | `cds-card-identity-name` |
| `card-tab-bar`, `--underline`, `card-tab` | `cds-card-tab-bar`, `--underline`, `cds-card-tab` |
| `card-panel`, `card-panel-title` | `cds-card-panel`, `cds-card-panel-title` |
| `card-notes`, `card-notes-edit`, `card-notes-status` | `cds-card-notes`, `cds-card-notes-edit`, `cds-card-notes-status` |
| `wc-note` | `cds-card-note` |
| `card-fact-row` (+`--solo`/`--3`/`--5`) | `cds-fact-row` (+ same modifiers) |
| `fact-cell` (+`--identity`), `fact-label`, `fact-value`, `fact-status-box` | `cds-fact-cell` (+`--identity`), `cds-fact-label`, `cds-fact-value`, `cds-fact-status-box` |
| `card-table`, `card-lv-table` | `cds-card-table`, `cds-card-lv-table` |
| `ct-row`, `ct-head`, `ct-cell`, `ct-num`, `ct-link`, `ct-section`, `ct-section-row` | `cds-ct-row`, `cds-ct-head`, `cds-ct-cell`, `cds-ct-num`, `cds-ct-link`, `cds-ct-section`, `cds-ct-section-row` |
| `card-type-label`, `card-main-title`, `hero-sep`, `card-footer`, `hero-value` (+ its `.hero-editable` compounds) | none — move to Minerva `title.css` verbatim |
| `hero-dropdown-panel`/`-option`/`-check`/`-done`, `hero-number-input` | none — move to Terminus `style.css` verbatim |
| `card-hero-grid`, `hero-stat`, `hero-label`, `card-section-divider`, `card-section-header`, the two `[data-field="acreage"]` rules | none — deleted |

## Consumers

Both TopLeaseMap pins move in the same pass, ending the deliberate
v5/v6 divergence:

- **Minerva** (`title.html`, `ledger-lab.html`): CDN pin `@v5.0.0` →
  `@v6.1.0`, drop the `/src/cards.css` link. The v5→v6 light-layer
  delta is three token aliasing tweaks plus the additive dark scope,
  so light-mode Minerva barely moves.
- **Terminus**: stays CDN-free. It vendors the card sections of
  components.css as `src/cardinal-cards.css` (same pattern as
  `src/cardinal-tokens.css`, which stays at v6.0.0 — tokens did not
  change). The map's `#lease-card` container adopts `.cds-card` and
  drops the duplicated surface props, keeping position, size,
  animation, and its stronger shadow as app bindings.

LeaseIndex and CharlieBot pins are untouched; additive release.
