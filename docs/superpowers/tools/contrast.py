"""WCAG contrast ratios for the Cardinal v4 palette. Run: python contrast.py"""

def lum(hexcolor):
    r, g, b = (int(hexcolor.lstrip('#')[i:i+2], 16) / 255 for i in (0, 2, 4))
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def ratio(fg, bg):
    l1, l2 = sorted((lum(fg), lum(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

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
    ("gold ring on white (nontext)", "#9F7A30", "#FFFFFF", 3.0),
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

failed = False
for name, fg, bg, floor in PAIRS:
    r = ratio(fg, bg)
    ok = "PASS" if r >= floor else "FAIL"
    failed = failed or r < floor
    print(f"{ok}  {name}: {r:.2f} (floor {floor})")
raise SystemExit(1 if failed else 0)
