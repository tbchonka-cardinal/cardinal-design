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
    ("paper on gold btn mid", "#faf3da", "#a08420", 3.0),
]

failed = False
for name, fg, bg, floor in PAIRS:
    r = ratio(fg, bg)
    ok = "PASS" if r >= floor else "FAIL"
    failed = failed or r < floor
    print(f"{ok}  {name}: {r:.2f} (floor {floor})")
raise SystemExit(1 if failed else 0)
