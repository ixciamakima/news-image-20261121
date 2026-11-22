"""Render entry.png for news-image-20261121.

Broadsheet front page: masthead + huge date, three lead stories with vector
illustrations, a numbered world map, a markets strip (Friday 20 Nov close,
labelled as such), and a 33-story grid. All 36 stories happened on, or were
first reported on, Saturday 21 November 2026.

Deterministic: fixed data, fixed fonts, no timestamps, no randomness.
Run twice and the bytes must be identical.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (22, 21, 19)
NAVY = (18, 54, 92)
RED = (180, 35, 24)
TEAL = (14, 107, 107)
GOLD = (166, 110, 20)
MUTED = (90, 85, 75)
CARD = (255, 255, 255)
LINE = (180, 172, 155)
MAP_BG = (220, 231, 234)
LAND = (216, 205, 180)
LAND_LINE = (138, 127, 99)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
F_SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")

_font_cache = {}
FIT = {}  # label -> verified font size, filled by fit_check()


def font(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _font_cache:
        path = F_SERIF if serif else (F_BOLD if bold else F_REG)
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


# ---------------------------------------------------------------- data

LEADS = [
    {
        "n": 1, "kicker": "CLIMATE  ·  ANTALYA, TURKEY", "color": TEAL,
        "headline": ["COP31 DEADLOCK", "IN ANTALYA"],
        "detail": [
            "Talks run into overtime with no deal in sight.",
            "Draft drops fossil fuels; EU: \u201cgood deal or no deal\u201d.",
            "Adaptation cash target of $120bn also cut.",
        ],
        "art": "cop",
    },
    {
        "n": 2, "kicker": "MIDDLE EAST  ·  RIYADH", "color": RED,
        "headline": ["3 MISSILES DOWN", "OVER RIYADH"],
        "detail": [
            "3 Houthi missiles downed, 2am.",
            "2nd attack on capital in 3 days.",
            "Coalition hits Hodeidah port.",
        ],
        "art": "riyadh",
    },
    {
        "n": 3, "kicker": "DISASTER  ·  JUN\u00cdN, PERU", "color": (150, 84, 20),
        "headline": ["QUAKE SHAKES", "PERU"],
        "detail": [
            "M6.7 (USGS; GFZ says 6.8).",
            "Deep, 108\u2013129 km; felt in Lima.",
            "No deaths; residents flee homes.",
        ],
        "art": "quake",
    },
]

# n, category, headline (<=32 chars at 16px bold), detail (<=36 chars at 15px)
STORIES = [
    (4, "war", "Kryvyi Rih missile kills 2", "Boy, 7, among 2 dead; ~60 injured"),
    (5, "war", "Kyiv bridges hit; Crimea reply", "Zelenskyy calls it \u2018fair response\u2019"),
    (6, "war", "Missiles crossed into Poland", "Warsaw: missiles \u2018probably\u2019 Russian"),
    (7, "war", "Ship hit by drones off Finland", "Finland: Ukraine likely behind attack"),
    (8, "war", "Israeli fire kills 4 in Gaza", "Aid vehicle hit in Gaza City; 3 dead"),
    (9, "politics", "Shenzhen summit fallout", "Trump hails talks; Zelenskyy objects"),
    (10, "crime", "Cartel boss on FBI list captured", "El Chapo Isidro seized in Sinaloa"),
    (11, "tech", "FBI probes database hack", "Crime database apparently hacked"),
    (12, "politics", "Denmark: Russian \u2018murder plot\u2019", "Defence attach\u00e9 expelled over claim"),
    (13, "markets", "EU\u2013Indonesia sign trade deal", "98.5% of tariffs on EU goods to fall"),
    (14, "politics", "UK\u2013EU sign post-Brexit reset", "Youth scheme among the pacts"),
    (15, "politics", "Nepal PM\u2019s first trip is to India", "Balendra Shah to meet Modi in India"),
    (16, "war", "Salvadoran troops mourn dead", "Soldiers killed in gang fight in Haiti"),
    (17, "war", "Fighting widens in E. Congo", "Conflict spreads in the east"),
    (18, "disaster", "700,000 displaced in Ethiopia", "Displacement crisis grows in south"),
    (19, "politics", "Lissu convicted of sedition", "Tanzania\u2019s Lissu guilty of sedition"),
    (20, "disaster", "Mourners\u2019 boat capsizes", "Funeral-party boat sinks in Bayelsa"),
    (21, "disaster", "Basra power-station fire kills 4", "Blaze at power plant in Basra"),
    (22, "politics", "Bolsonaro hospitalised", "Bolsonaro in hospital, bowel blocked"),
    (23, "politics", "Turkey takes over S\u00f6zc\u00fc TV", "State seizes opposition broadcaster"),
    (24, "crime", "Police jailed over racist beating", "Sentenced for 2020 racist beating"),
    (25, "disaster", "Cyclone Akvan hits Odisha", "Storm crosses coast near Gopalpur"),
    (26, "health", "Toxic alcohol kills 11 in Manipur", "180+ in hospital after toxic liquor"),
    (27, "science", "Mosquitoes cut dengue by 69%", "Wolbachia trial success in Brazil"),
    (28, "crime", "Palisades fire starter convicted", "Man guilty over deadly LA blaze"),
    (29, "tech", "Trump: ban AI centres abroad", "US firms told to build at home"),
    (30, "politics", "Mamdani: close Rikers by 2032", "NYC mayor-elect\u2019s jail-closure plan"),
    (31, "sport", "England 37\u201312 New Zealand", "Record rugby win at Twickenham"),
    (32, "sport", "Ireland 20\u201317 South Africa", "Late win over world champions"),
    (33, "sport", "Alcaraz into ATP Finals final", "Beats Shelton 3\u20136, 6\u20133, 7\u20136 in Turin"),
    (34, "sport", "Harden passes Kobe: 51 points", "51 pts; Cavs beat Pacers 128\u2013119"),
    (35, "sport", "India 159/1 in Wellington Test", "Jaiswal 85; Rahul 52* vs New Zealand"),
    (36, "sport", "Australia edge Wales in Cardiff", "Narrow win in Nations Championship"),
]

CAT_COLOR = {
    "war": RED, "politics": NAVY, "markets": GOLD, "crime": (70, 66, 60),
    "tech": (70, 90, 120), "disaster": (150, 84, 20), "health": (178, 34, 34),
    "science": (96, 60, 140), "sport": (34, 120, 60), "climate": TEAL,
}

# World map: rough continent outlines in (lon, lat). Stylised, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 55), (-55, 47), (-65, 44), (-75, 35), (-80, 26),
     (-85, 20), (-90, 15), (-95, 17), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-158, 58), (-168, 66)],  # N America
    [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-55, -35), (-65, -40), (-70, -50), (-73, -40),
     (-75, -20), (-80, -5), (-80, 10)],  # S America
    [(-10, 36), (0, 36), (10, 38), (20, 40), (28, 36), (30, 42), (28, 45),
     (20, 45), (12, 44), (5, 43), (-2, 44), (-10, 44), (-10, 48), (-5, 50),
     (0, 52), (5, 55), (8, 58), (12, 58), (18, 56), (21, 55), (24, 60),
     (30, 60), (30, 65), (25, 70), (18, 70), (10, 65), (5, 60),
     (-10, 58), (-10, 36)],  # Europe
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (10, -5), (8, 4), (-8, 4),
     (-17, 15)],  # Africa
    [(30, 65), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 67), (178, 65), (170, 60), (160, 55), (150, 45),
     (140, 40), (130, 33), (127, 35), (120, 30), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 10), (75, 8), (70, 20),
     (60, 25), (55, 27), (50, 30), (45, 30), (40, 35), (35, 36), (30, 36),
     (30, 42), (30, 65)],  # Asia
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (136, -12), (132, -11), (126, -14),
     (122, -17), (113, -22)],  # Australia
]

# story number -> (lon, lat, label dx, dy) for the numbered map
MAP_POINTS = [
    (1, 30.7, 36.9, -16, -16),
    (2, 46.7, 24.7, 14, 10),
    (3, -75.9, -11.2, -18, -2),
    (4, 30.5, 50.5, 16, -6),
    (5, 34.5, 31.4, 14, 12),
    (6, -108.0, 25.7, -16, -14),
    (7, 4.4, 50.8, 14, -16),
    (8, 85.0, 19.3, 12, 10),
    (9, -47.9, -15.8, -14, 12),
    (10, -3.2, 51.5, 0, -18),
]

MARKETS_L1 = "MARKETS \u2014 CLOSE FRI 20 NOV  (SAT 21 NOV: MARKETS SHUT)"
MARKETS_L2 = ("Nasdaq 22,618 -5.3% \u00b7 S&P 6,910 -3.7% \u00b7 "
              "Dow 48,147 -1.9% \u00b7 Gold $3,515 -4.6% \u00b7 "
              "Brent $92.57 +0.6% \u00b7 WTI $83.98 +0.9%")

FOOTER = ("Sources: Reuters \u00b7 BBC \u00b7 AP \u00b7 AFP \u00b7 USGS \u00b7 GFZ  \u2014  "
          "All 36 stories happened or were first reported on Saturday 21 November 2026.")


# ---------------------------------------------------------------- fit check

def measure(text, size, bold=False, serif=False):
    return font(size, bold, serif).getlength(text)


def fit_check():
    """Return list of failures; print a line per checked string.
    Records the fitted size of every line in FIT so render() draws each
    line at the size that was verified to fit (never larger)."""
    failures = []
    probe = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(probe)
    del d

    def check(label, text, max_w, size, bold=False, serif=False, minimum=15):
        s = size
        while s > minimum and measure(text, s, bold, serif) > max_w:
            s -= 1
        w = measure(text, s, bold, serif)
        ok = w <= max_w
        FIT[label] = s
        print("FIT %s size=%d w=%.0f max=%d %s :: %s"
              % (label, s, w, max_w, "OK" if ok else "FAIL", text))
        if not ok:
            failures.append(label + ": " + text)
        return s

    check("masthead", "THE WORLD IN ONE DAY", 976, 52, bold=True, serif=True)
    check("date", "SATURDAY 21 NOVEMBER 2026", 976, 38, bold=True)
    check("subline", "36 stories \u00b7 7 regions \u00b7 Every event of Saturday "
          "21 November 2026 \u00b7 Sources: Reuters, BBC, AP, AFP",
          976, 15)
    for lead in LEADS:
        cw = 420 if lead["n"] == 1 else 278
        for i, line in enumerate(lead["headline"]):
            check("lead%d-h%d" % (lead["n"], i), line, cw - 28, 24, bold=True)
        for i, line in enumerate(lead["detail"]):
            check("lead%d-d%d" % (lead["n"], i), line, cw - 28, 15)
    for (n, cat, head, detail) in STORIES:
        check("s%d-h" % n, head, 271, 16, bold=True)
        check("s%d-d" % n, detail, 293, 15)
    check("markets1", MARKETS_L1, 976, 15, bold=True)
    check("markets2", MARKETS_L2, 976, 15)
    check("footer", FOOTER, 976, 13)
    return failures


# ---------------------------------------------------------------- icons

def draw_icon(d, cat, x, y, s=18):
    c = CAT_COLOR[cat]
    if cat == "climate":  # sun
        d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], fill=c)
        for dx, dy in ((8, 0), (8, 16), (0, 8), (16, 8)):
            d.line([x + dx, y + dy, x + dx, y + dy], fill=c, width=2)
    elif cat == "missile":  # rocket triangle + trail
        d.polygon([(x + 9, y + 1), (x + 15, y + 13), (x + 9, y + 10),
                   (x + 3, y + 13)], fill=c)
        d.line([x + 3, y + 15, x + 8, y + 17], fill=c, width=2)
        d.line([x + 9, y + 16, x + 13, y + 17], fill=c, width=2)
    elif cat == "quake":  # seismograph zigzag
        d.line([(x + 1, y + 9), (x + 5, y + 9), (x + 7, y + 3), (x + 10, y + 15),
                (x + 12, y + 6), (x + 15, y + 9), (x + 17, y + 9)],
               fill=c, width=2)
    elif cat == "war":  # crosshair
        d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=c, width=2)
        d.line([x + 9, y + 1, x + 9, y + 5], fill=c, width=2)
        d.line([x + 9, y + 13, x + 9, y + 17], fill=c, width=2)
        d.line([x + 1, y + 9, x + 5, y + 9], fill=c, width=2)
        d.line([x + 13, y + 9, x + 17, y + 9], fill=c, width=2)
    elif cat == "politics":  # flag
        d.line([x + 4, y + 2, x + 4, y + 16], fill=c, width=2)
        d.polygon([(x + 4, y + 2), (x + 15, y + 5), (x + 4, y + 9)], fill=c)
    elif cat == "markets":  # rising bars
        d.rectangle([x + 2, y + 11, x + 5, y + 16], fill=c)
        d.rectangle([x + 7, y + 8, x + 10, y + 16], fill=c)
        d.rectangle([x + 12, y + 4, x + 15, y + 16], fill=c)
    elif cat == "crime":  # star badge
        cx, cy, r = x + 9, y + 9, 8
        pts = []
        for i in range(10):
            ang = -90 + i * 36
            rr = r if i % 2 == 0 else r * 0.45
            import math
            pts.append((cx + rr * math.cos(math.radians(ang)),
                        cy + rr * math.sin(math.radians(ang))))
        d.polygon(pts, fill=c)
    elif cat == "sport":  # ball
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=c, width=2)
        d.arc([x + 2, y + 2, x + s - 2, y + s - 2], 200, 340, fill=c, width=2)
    elif cat == "science":  # flask
        d.polygon([(x + 7, y + 2), (x + 11, y + 2), (x + 11, y + 7),
                   (x + 15, y + 15), (x + 3, y + 15), (x + 7, y + 7)], outline=c,
                  width=2)
        d.line([x + 5, y + 12, x + 13, y + 12], fill=c, width=2)
    elif cat == "health":  # cross
        d.rectangle([x + 7, y + 2, x + 11, y + 16], fill=c)
        d.rectangle([x + 2, y + 7, x + 16, y + 11], fill=c)
    elif cat == "disaster":  # flame
        d.polygon([(x + 9, y + 1), (x + 14, y + 8), (x + 15, y + 13),
                   (x + 9, y + 17), (x + 3, y + 13), (x + 4, y + 8)], fill=c)
    elif cat == "tech":  # chip
        d.rectangle([x + 4, y + 4, x + 14, y + 14], outline=c, width=2)
        d.rectangle([x + 7, y + 7, x + 11, y + 11], fill=c)
        for px in (7, 11):
            d.line([x + px, y + 1, x + px, y + 4], fill=c, width=2)
            d.line([x + px, y + 14, x + px, y + 17], fill=c, width=2)


# ---------------------------------------------------------------- lead art

def draw_lead_art(d, kind, x0, y0, w, h):
    # Art lives in a short band (h ~ 40) below the detail lines; it must
    # never reach above y0.
    if kind == "cop":  # earth + thermometer
        cx, cy, r = x0 + 38, y0 + h // 2, 19
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(158, 205, 214),
                  outline=TEAL, width=2)
        d.arc([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=TEAL, width=2)
        d.line([cx - r, cy, cx + r, cy], fill=TEAL, width=2)
        d.ellipse([cx - 13, cy - 15, cx + 5, cy - 3], fill=(64, 140, 90))
        d.ellipse([cx - 4, cy + 5, cx + 14, cy + 15], fill=(64, 140, 90))
        tx = x0 + w - 128
        d.rectangle([tx, y0 + 2, tx + 12, y0 + h - 10], outline=RED, width=2)
        d.rectangle([tx + 2, y0 + h - 16, tx + 10, y0 + h - 12], fill=RED)
        d.ellipse([tx - 2, y0 + h - 15, tx + 14, y0 + h + 1], fill=RED)
        d.text((tx + 19, y0 + 2), "1.5\u00b0C", font=font(14, bold=True),
               fill=RED)
        d.text((tx + 19, y0 + 19), "LIMIT AT RISK", font=font(12, bold=True),
               fill=INK)
    elif kind == "riyadh":  # skyline + intercept arcs
        base = y0 + h - 2
        heights = [22, 32, 26, 38, 24, 30]
        bw = w // 7
        for i, hh in enumerate(heights):
            bx = x0 + 6 + i * bw
            d.rectangle([bx, base - hh, bx + bw - 6, base], fill=NAVY)
        d.arc([x0 + 8, y0 + 6, x0 + 110, y0 + 40], 200, 340, fill=RED, width=3)
        d.arc([x0 + 80, y0 + 2, x0 + 200, y0 + 36], 200, 340, fill=GOLD,
              width=3)
        for sx, sy in ((x0 + 84, y0 + 12), (x0 + 152, y0 + 10)):
            d.line([sx - 6, sy, sx + 6, sy], fill=RED, width=2)
            d.line([sx, sy - 6, sx, sy + 6], fill=RED, width=2)
    elif kind == "quake":  # mountains + seismograph
        base = y0 + h - 2
        d.polygon([(x0 + 4, base), (x0 + 44, y0 + 4), (x0 + 84, base)],
                  fill=(120, 110, 96))
        d.polygon([(x0 + 60, base), (x0 + 108, y0 + 12), (x0 + 156, base)],
                  fill=(90, 84, 72))
        d.polygon([(x0 + 38, y0 + 10), (x0 + 44, y0 + 4), (x0 + 50, y0 + 10)],
                  fill=(255, 255, 255))
        pts = [(x0 + 168, y0 + 18), (x0 + 180, y0 + 18), (x0 + 184, y0 + 6),
               (x0 + 189, y0 + 32), (x0 + 194, y0 + 12), (x0 + 199, y0 + 24),
               (x0 + 204, y0 + 18), (x0 + 224, y0 + 18)]
        d.line(pts, fill=RED, width=3)


# ---------------------------------------------------------------- render

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # header
    d.text((W // 2, 8), "THE WORLD IN ONE DAY",
           font=font(FIT.get("masthead", 52), bold=True, serif=True),
           fill=NAVY, anchor="ma")
    d.text((W // 2, 66), "SATURDAY 21 NOVEMBER 2026",
           font=font(FIT.get("date", 38), bold=True),
           fill=RED, anchor="ma")
    d.line([24, 112, W - 24, 112], fill=INK, width=2)
    d.text((W // 2, 118), "36 stories \u00b7 7 regions \u00b7 Every event of "
           "Saturday 21 November 2026 \u00b7 Sources: Reuters, BBC, AP, AFP",
           font=font(FIT.get("subline", 15)), fill=MUTED, anchor="ma")

    # lead row
    lead_y, lead_h = 142, 190
    lead_x = [24, 456, 746]
    lead_w = [420, 278, 278]
    for lead, x0, cw in zip(LEADS, lead_x, lead_w):
        d.rectangle([x0, lead_y, x0 + cw, lead_y + lead_h], fill=CARD,
                    outline=LINE, width=1)
        d.rectangle([x0, lead_y, x0 + cw, lead_y + 5], fill=lead["color"])
        d.text((x0 + 14, lead_y + 12), lead["kicker"],
               font=font(13, bold=True), fill=lead["color"])
        hy = lead_y + 32
        for i, line in enumerate(lead["headline"]):
            d.text((x0 + 14, hy), line,
                   font=font(FIT.get("lead%d-h%d" % (lead["n"], i), 24),
                         bold=True), fill=INK)
            hy += 28
        dy = hy + 4
        for i, line in enumerate(lead["detail"]):
            d.text((x0 + 14, dy), line,
                   font=font(FIT.get("lead%d-d%d" % (lead["n"], i), 15)),
                   fill=INK)
            dy += 18
        draw_lead_art(d, lead["art"], x0 + 14, lead_y + 150, cw - 28, 36)

    # map strip
    map_y, map_h = 338, 132
    d.text((24, map_y), "WHERE IT HAPPENED \u2014 10 PLACES ON THE MAP  "
           "(NUMBERS MATCH THE STORIES BELOW)",
           font=font(13, bold=True), fill=NAVY)
    mx0, my0, mw, mh = 24, map_y + 20, W - 48, map_h - 20

    def proj(lon, lat):
        # Strip map: latitudes 75..-55 fill the box; clamp poles out.
        lat = max(-55.0, min(75.0, lat))
        px = mx0 + (lon + 180.0) / 360.0 * mw
        py = my0 + (75.0 - lat) / 130.0 * mh
        return px, py

    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=MAP_BG, outline=LINE)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_LINE)
    for (n, lon, lat, dx, dy) in MAP_POINTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                  outline=(255, 255, 255), width=1)
        cx, cy = px + dx, py + dy
        d.line([px, py, cx, cy], fill=MUTED, width=1)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=NAVY,
                  outline=(255, 255, 255), width=1)
        d.text((cx, cy), str(n), font=font(11, bold=True), fill=(255, 255, 255),
               anchor="mm")

    # markets strip (two lines)
    mk_y, mk_h = 494, 48
    d.rectangle([24, mk_y, W - 24, mk_y + mk_h], fill=NAVY)
    d.text((W // 2, mk_y + 13), MARKETS_L1,
           font=font(FIT.get("markets1", 15), bold=True),
           fill=(255, 255, 255), anchor="mm")
    d.text((W // 2, mk_y + 35), MARKETS_L2, font=font(FIT.get("markets2", 15)),
           fill=(255, 255, 255), anchor="mm")

    # story grid: 3 columns x 11 rows
    grid_y, row_h = 548, 40
    col_x = [24, 353, 682]
    col_w = 317
    for idx, (n, cat, head, detail) in enumerate(STORIES):
        col = idx % 3
        row = idx // 3
        x0 = col_x[col]
        y0 = grid_y + row * row_h
        if row > 0:
            d.line([x0, y0 - 1, x0 + col_w, y0 - 1], fill=(226, 220, 205),
                   width=1)
        # number chip
        d.ellipse([x0, y0 + 2, x0 + 19, y0 + 21], fill=CAT_COLOR[cat])
        d.text((x0 + 10, y0 + 11), str(n), font=font(11, bold=True),
               fill=(255, 255, 255), anchor="mm")
        draw_icon(d, cat, x0 + 23, y0 + 2)
        d.text((x0 + 45, y0 + 1), head,
               font=font(FIT.get("s%d-h" % n, 16), bold=True), fill=INK)
        d.text((x0 + 23, y0 + 21), detail,
               font=font(FIT.get("s%d-d" % n, 15)), fill=(52, 50, 46))

    # footer
    d.line([24, 994, W - 24, 994], fill=INK, width=1)
    d.text((W // 2, 1000), FOOTER, font=font(FIT.get("footer", 13)),
           fill=MUTED, anchor="ma")

    img.save(OUT, format="PNG", optimize=True, compress_level=9)
    print("WROTE %s %dx%d" % (OUT, W, H))


def main():
    failures = fit_check()
    if failures:
        print("FIT FAILURES: %d" % len(failures))
        for f in failures:
            print("  FAIL " + f)
        return 1
    render()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
