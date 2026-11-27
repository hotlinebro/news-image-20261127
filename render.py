#!/usr/bin/env python3
"""Render the news-image-20261127 entry: one newspaper-style image summing up
Friday 27 November 2026's world news. Pure PIL, deterministic output.

Six stories, all first reported on 27 November 2026 (verified against news
sources the morning of the build):
  1. UK net migration falls to its lowest since 1997 (ex-pandemic) - NYT/ONS
  2. Israel kills 10 in Gaza; Hamas weighs its response - Reuters
  3. Diesel tanker capsizes off Ibiza, one dead, oil spill - BBC
  4. Gukesh vs Sindarov draw marathon Game 3, World Chess Championship
  5. Thanksgiving storm leaves 500,000+ without power in the US
  6. Ebola epidemic in Congo passes 12,000 cases
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PAPER = (246, 241, 231)
NAVY = (18, 40, 75)
GOLD = (201, 162, 39)
INK = (24, 24, 24)
MUTED = (84, 84, 84)
CARD = (255, 255, 255)
BORDER = (206, 198, 178)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- art panels
def art_uk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(223, 233, 242))
    # Big Ben silhouette, left
    d.rectangle([x + 28, y + 34, x + 58, y + h], fill=(27, 79, 114))
    d.polygon([(x + 24, y + 34), (x + 62, y + 34), (x + 43, y + 8)], fill=(27, 79, 114))
    d.ellipse([x + 33, y + 44, x + 53, y + 64], fill=(246, 241, 231))
    d.rectangle([x + 42, y + 44, x + 44, y + 64], fill=(27, 79, 114))
    d.rectangle([x + 33, y + 53, x + 53, y + 55], fill=(27, 79, 114))
    # descending bars, right
    base = y + h - 18
    vals = [86, 66, 46, 28]
    bx = x + 150
    for i, v in enumerate(vals):
        d.rectangle([bx + i * 78, base - v, bx + i * 78 + 56, base], fill=(31, 97, 141))
    # red down arrow over the bars
    d.line([x + 150, base - 92, x + 440, base - 20], fill=(192, 57, 43), width=7)
    d.polygon([(x + 440, base - 20), (x + 416, base - 26), (x + 428, base - 2)],
              fill=(192, 57, 43))


def art_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 63, 58))
    # white dove
    d.ellipse([x + 150, y + 34, x + 320, y + 82], fill=(255, 255, 255))
    d.ellipse([x + 300, y + 18, x + 336, y + 54], fill=(255, 255, 255))
    d.polygon([(x + 336, y + 30), (x + 358, y + 38), (x + 336, y + 44)], fill=(201, 162, 39))
    d.ellipse([x + 318, y + 28, x + 326, y + 36], fill=(18, 63, 58))
    d.polygon([(x + 170, y + 44), (x + 260, y + 20), (x + 280, y + 48)],
              fill=(226, 232, 232))
    d.polygon([(x + 150, y + 66), (x + 120, y + 92), (x + 168, y + 80)], fill=(255, 255, 255))
    # olive branch
    d.line([x + 330, y + 96, x + 440, y + 78], fill=(88, 150, 80), width=4)
    for lx, ly in [(350, 92), (375, 87), (400, 82), (425, 78)]:
        d.ellipse([x + lx, y + ly - 6, x + lx + 22, y + ly + 6], fill=(88, 150, 80))
    # small candle of remembrance, left
    d.rectangle([x + 52, y + 62, x + 72, y + h - 14], fill=(246, 241, 231))
    d.polygon([(x + 62, y + 62), (x + 56, y + 46), (x + 68, y + 46)], fill=(243, 180, 60))


def art_ibiza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + 58], fill=(188, 216, 232))
    d.rectangle([x, y + 58, x + w, y + h], fill=(26, 82, 118))
    # waves
    for wy in (y + 66, y + 84, y + 102):
        for wx in range(x + 6, x + w - 20, 44):
            d.arc([wx, wy, wx + 40, wy + 16], 180, 360, fill=(255, 255, 255), width=3)
    # tilted tanker
    d.polygon([(x + 120, y + 44), (x + 380, y + 22), (x + 392, y + 52),
               (x + 150, y + 74)], fill=(44, 62, 80))
    d.rectangle([x + 250, y + 12, x + 290, y + 33], fill=(192, 57, 43))
    d.rectangle([x + 300, y + 18, x + 330, y + 30], fill=(44, 62, 80))
    # black oil slick
    d.ellipse([x + 300, y + 78, x + 470, y + 108], fill=(12, 12, 12))
    d.ellipse([x + 180, y + 92, x + 300, y + 112], fill=(12, 12, 12))
    d.ellipse([x + 60, y + 88, x + 150, y + 104], fill=(12, 12, 12))


def art_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 224, 200))
    # 4x4 board, left
    bs = 26
    bx, by = x + 24, y + 6
    for r in range(4):
        for c in range(4):
            col = (240, 217, 181) if (r + c) % 2 == 0 else (181, 136, 99)
            d.rectangle([bx + c * bs, by + r * bs, bx + (c + 1) * bs, by + (r + 1) * bs],
                        fill=col)
    # white king on a light square
    kx, ky = bx + 1 * bs + 13, by + 1 * bs + 13
    d.ellipse([kx - 11, ky - 11, kx + 11, ky + 11], fill=(255, 255, 255),
              outline=(120, 120, 120), width=2)
    d.line([kx - 6, ky, kx + 6, ky], fill=(120, 120, 120), width=3)
    d.line([kx, ky - 6, kx, ky + 6], fill=(120, 120, 120), width=3)
    # black queen on a dark square
    qx, qy = bx + 2 * bs + 13, by + 2 * bs + 13
    d.polygon([(qx - 11, qy + 10), (qx - 11, qy - 4), (qx - 5, qy + 2),
               (qx, qy - 8), (qx + 5, qy + 2), (qx + 11, qy - 4), (qx + 11, qy + 10)],
              fill=(30, 30, 30))
    d.ellipse([qx - 11, qy + 6, qx + 11, qy + 14], fill=(30, 30, 30))
    # score on the right: big and short so it never clips the panel edge
    d.text((x + 168, y + 24), "1\u00bd \u2013 1\u00bd",
           font=font(BOLD, 40), fill=(24, 24, 24))
    d.text((x + 168, y + 72), "GAME 3  \u00b7  DRAW",
           font=font(REG, 22), fill=(84, 84, 84))


def art_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(44, 62, 80))
    # storm cloud
    for cx, cy, r in [(120, 46, 34), (170, 34, 42), (230, 48, 36), (280, 58, 26)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(26, 37, 48))
    d.rectangle([x + 90, y + 48, x + 310, y + 78], fill=(26, 37, 48))
    # lightning bolt
    d.polygon([(x + 210, y + 70), (x + 178, y + 108), (x + 198, y + 108),
               (x + 182, y + h - 6), (x + 222, y + 96), (x + 202, y + 96)],
              fill=(243, 180, 60))
    # rain
    for rx in range(x + 330, x + w - 10, 26):
        d.line([rx, y + 20, rx - 12, y + 52], fill=(150, 180, 205), width=3)
        d.line([rx, y + 66, rx - 12, y + 98], fill=(150, 180, 205), width=3)
    # dark house, bottom left
    d.rectangle([x + 24, y + 78, x + 84, y + h - 8], fill=(18, 28, 38))
    d.polygon([(x + 18, y + 78), (x + 90, y + 78), (x + 54, y + 58)], fill=(18, 28, 38))
    d.rectangle([x + 36, y + 88, x + 48, y + 100], fill=(10, 10, 10))
    d.rectangle([x + 60, y + 88, x + 72, y + 100], fill=(10, 10, 10))


def art_ebola(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(249, 231, 159))
    # simplified Africa outline: wide north coast, west bulge, horn on the
    # east, tapering south. Drawn tall so the continent reads at a glance.
    africa = [(86, 6), (126, 2), (160, 12), (186, 26), (172, 44), (158, 58),
              (146, 84), (136, 106), (124, 110), (114, 88), (96, 68),
              (72, 56), (58, 34), (62, 14)]
    pts = [(x + px, y + py) for px, py in africa]
    d.polygon(pts, fill=(214, 164, 90), outline=(125, 102, 8), width=2)
    # Congo highlighted as a small red dot near the continent's middle
    d.ellipse([x + 108, y + 48, x + 126, y + 66], fill=(192, 57, 43))
    # red cross badge
    d.ellipse([x + 380, y + 22, x + 452, y + 94], fill=(255, 255, 255),
              outline=(192, 57, 43), width=4)
    d.rectangle([x + 408, y + 36, x + 424, y + 80], fill=(192, 57, 43))
    d.rectangle([x + 394, y + 50, x + 438, y + 66], fill=(192, 57, 43))
    # case dots on the map
    for dx, dy in [(100, 22), (150, 34), (132, 72)]:
        d.ellipse([x + dx - 5, y + dy - 5, x + dx + 5, y + dy + 5], fill=(192, 57, 43))


ARTS = {
    "uk": art_uk,
    "gaza": art_gaza,
    "ibiza": art_ibiza,
    "chess": art_chess,
    "storm": art_storm,
    "ebola": art_ebola,
}

PANELS = [
    ("uk", "UNITED KINGDOM \u00b7 MIGRATION", (27, 79, 114),
     "Net migration falls to lowest since 1997",
     "Arrivals minus departures hit a near 30-year low, pandemic years aside."),
    ("gaza", "GAZA \u00b7 CONFLICT", (146, 43, 33),
     "Israel kills 10 in Gaza; Hamas weighs reply",
     "Strike toll reported as Hamas considers its response to the deaths."),
    ("ibiza", "SPAIN \u00b7 ENVIRONMENT", (17, 122, 101),
     "Tanker capsizes off Ibiza; one dead",
     "Diesel carrier with up to 7,000 tonnes aboard sinks; Spain races to stop the spill."),
    ("chess", "WORLD CHESS \u00b7 SPORT", (91, 44, 111),
     "Gukesh, Sindarov draw marathon Game 3",
     "World Championship match still level after three games."),
    ("storm", "UNITED STATES \u00b7 WEATHER", (46, 64, 83),
     "Thanksgiving storm leaves 500,000+ in the dark",
     "Flights cancelled and homes without power as a major storm hits the holiday."),
    ("ebola", "CONGO \u00b7 HEALTH", (125, 102, 8),
     "Ebola outbreak in Congo passes 12,000 cases",
     "Epidemic grows as unrest forces responders to leave some areas."),
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    draw_center(d, W // 2, 16, "THE WORLD IN ONE DAY", font(BOLD, 30), (201, 162, 39))
    draw_center(d, W // 2, 58, "FRIDAY 27 NOVEMBER 2026", font(BOLD, 62), (255, 255, 255))

    # grid: 2 cols x 3 rows
    pw, ph, gap, mx = 496, 276, 16, 16
    top = 170
    for i, (key, kicker, color, headline, caption) in enumerate(PANELS):
        px = mx + (i % 2) * (pw + gap)
        py = top + (i // 2) * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=CARD, outline=BORDER, width=2)
        d.rectangle([px, py, px + pw, py + 34], fill=color)
        d.text((px + 12, py + 5), kicker, font=font(BOLD, 21), fill=(255, 255, 255))
        ARTS[key](d, px + 2, py + 36, pw - 4, 110)
        # headline, up to 2 lines
        hl = wrap(d, headline, font(BOLD, 29), pw - 24)
        hy = py + 152
        for line in hl[:2]:
            d.text((px + 12, hy), line, font=font(BOLD, 29), fill=INK)
            hy += 35
        # caption, up to 2 lines
        cap = wrap(d, caption, font(REG, 19), pw - 24)
        cy = py + 152 + 35 * min(2, len(hl)) + 4
        for line in cap[:2]:
            d.text((px + 12, cy), line, font=font(REG, 19), fill=MUTED)
            cy += 24

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
