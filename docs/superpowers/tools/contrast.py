"""WCAG contrast ratios for the Cardinal v6 palette, light layer and
.cds-dark scope. Run: python contrast.py

Both layers are covered the same way: every text role against every
ground it can sit on, the accent as text and as a focus ring, the
feedback pairs on their own tint and on the card surface. A palette
change ships only if this exits 0.
"""

def lum(hexcolor):
    r, g, b = (int(hexcolor.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4))
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def ratio(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

PAIRS = [
    # ---------- light layer (:root) ----------
    # ink tiers on the surfaces they sit on
    ("ink on white",                 "#161514", "#FFFFFF", 4.5),
    ("ink on canvas",                "#161514", "#F9F7F2", 4.5),
    ("ink on raised (n-75)",         "#161514", "#F2EFE9", 4.5),
    ("ink-soft on white",            "#524E48", "#FFFFFF", 4.5),
    ("ink-soft on canvas",           "#524E48", "#F9F7F2", 4.5),
    ("ink-mute captions on white",   "#706B62", "#FFFFFF", 4.5),
    ("ink-mute captions on canvas",  "#706B62", "#F9F7F2", 4.5),
    ("ink-mute captions on raised",  "#706B62", "#F2EFE9", 4.5),
    # brass accent
    ("gold-deep text on white",      "#846931", "#FFFFFF", 4.5),
    ("gold-deep text on canvas",     "#846931", "#F9F7F2", 4.5),
    ("gold-deep text on raised (n-75)", "#846931", "#F2EFE9", 4.5),
    ("gold-deep on gold-subtle",     "#846931", "#F6F1E5", 4.5),
    ("focus ring on white",          "#846931", "#FFFFFF", 3.0),
    ("ink text on brass btn",        "#161514", "#B8934A", 4.5),
    ("ink text on brass hover",      "#161514", "#C9A45C", 4.5),
    # chrome and danger
    ("paper on lapis",               "#F9F7F2", "#1E4585", 4.5),
    ("header text (n-50) on lapis-500", "#F9F7F2", "#1E4585", 4.5),
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

# ---------- dark layer (.cds-dark, v6.0.0) ----------
# The dark grounds, lightest-first names as they read in tokens.css.
D_GROUND = "#1A1714"   # --dk-900  --bg
D_PANEL  = "#25211D"   # --dk-800  --bg-surface
D_ZEBRA  = "#2E2924"   # --dk-750  --paper-zebra
D_RAISED = "#37312B"   # --dk-700  --bg-raised
D_TINT   = "#413A33"   # --dk-600  --paper-3

DARK_PAIRS = [
    # ink tiers on every dark ground
    ("dark: text on ground",           "#F5F1EA", D_GROUND, 4.5),
    ("dark: text on panel",            "#F5F1EA", D_PANEL,  4.5),
    ("dark: text on zebra",            "#F5F1EA", D_ZEBRA,  4.5),
    ("dark: text on raised",           "#F5F1EA", D_RAISED, 4.5),
    ("dark: text on deep tint",        "#F5F1EA", D_TINT,   4.5),
    ("dark: text-soft on ground",      "#D6CFC4", D_GROUND, 4.5),
    ("dark: text-soft on panel",       "#D6CFC4", D_PANEL,  4.5),
    ("dark: text-soft on raised",      "#D6CFC4", D_RAISED, 4.5),
    ("dark: mute captions on ground",  "#AEA69A", D_GROUND, 4.5),
    ("dark: mute captions on panel",   "#AEA69A", D_PANEL,  4.5),
    ("dark: mute captions on zebra",   "#AEA69A", D_ZEBRA,  4.5),
    ("dark: mute captions on raised",  "#AEA69A", D_RAISED, 4.5),
    ("dark: mute captions on tint",    "#AEA69A", D_TINT,   4.5),
    # brass: the accent carries over, text tier lifts to brass-300
    ("dark: gold-deep text on ground", "#D9BC7E", D_GROUND, 4.5),
    ("dark: gold-deep text on panel",  "#D9BC7E", D_PANEL,  4.5),
    ("dark: gold-deep text on raised", "#D9BC7E", D_RAISED, 4.5),
    ("dark: gold-deep on gold-subtle", "#D9BC7E", "#33291B", 4.5),
    ("dark: focus ring on panel",      "#D9BC7E", D_PANEL,  3.0),
    ("dark: focus ring on raised",     "#D9BC7E", D_RAISED, 3.0),
    ("dark: brass hairline on panel",  "#B8934A", D_PANEL,  3.0),
    ("dark: ink text on brass btn",    "#161514", "#B8934A", 4.5),
    ("dark: ink text on brass hover",  "#161514", "#C9A45C", 4.5),
    # lapis: the chrome carries over, text tier lifts to lapis-200
    ("dark: link hover on ground",     "#A8C4EA", D_GROUND, 4.5),
    ("dark: link hover on panel",      "#A8C4EA", D_PANEL,  4.5),
    ("dark: link hover on raised",     "#A8C4EA", D_RAISED, 4.5),
    ("dark: text on lapis band",       "#F5F1EA", "#1E4585", 4.5),
    # feedback: text on its own dark tint, and on the panel
    ("dark: success text on tint",     "#9FD9B8", "#1C2E24", 4.5),
    ("dark: success text on panel",    "#9FD9B8", D_PANEL,  4.5),
    ("dark: danger text on tint",      "#F0A9A0", "#331E1C", 4.5),
    ("dark: danger text on panel",     "#F0A9A0", D_PANEL,  4.5),
    ("dark: warning text on tint",     "#E5BE72", "#33291A", 4.5),
    ("dark: warning text on panel",    "#E5BE72", D_PANEL,  4.5),
    ("dark: info text on tint",        "#A8C4EA", "#1E2836", 4.5),
    ("dark: info text on panel",       "#A8C4EA", D_PANEL,  4.5),
    ("dark: white on brick (btn)",     "#FFFFFF", "#c0392b", 4.5),
    # jewel data colors as dots and chart series: non-text floor
    ("dark: ink-blue on panel",        "#6E9BD6", D_PANEL,  3.0),
    ("dark: moss on panel",            "#6FB894", D_PANEL,  3.0),
    ("dark: data-amber on panel",      "#D9A544", D_PANEL,  3.0),
    ("dark: data-crimson on panel",    "#E0857A", D_PANEL,  3.0),
]

failed = False
for name, fg, bg, floor in PAIRS + DARK_PAIRS:
    r = ratio(fg, bg)
    ok = "PASS" if r >= floor else "FAIL"
    failed = failed or r < floor
    print(f"{ok}  {name}: {r:.2f} (floor {floor})")
raise SystemExit(1 if failed else 0)
