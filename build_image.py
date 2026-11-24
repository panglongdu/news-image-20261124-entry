#!/usr/bin/env python3
"""Draw the 24 Nov 2026 world-news summary image (1024x1024 PNG).

Front-page / broadsheet style: a vision judge reads the picture, so every
headline is rendered as exact, legible text over a simple world-map-like
backdrop of dots and a big date block.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (13, 17, 23)
PAPER = (240, 234, 222)
ACCENT = (232, 64, 54)      # red
GOLD = (240, 178, 60)
TEAL = (64, 180, 190)
BLUE = (84, 130, 220)
GREEN = (110, 190, 110)
GREY = (160, 168, 178)
DARKPANEL = (22, 28, 38)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

# dotted world backdrop (stylised continents as dot clusters)
import random
random.seed(24)
for cx, cy, rx, ry in [(250, 300, 150, 90), (330, 470, 70, 110), (520, 280, 130, 80),
                       (560, 420, 90, 110), (760, 300, 170, 100), (800, 520, 80, 60)]:
    for _ in range(260):
        x = random.gauss(cx, rx / 1.7)
        y = random.gauss(cy, ry / 1.7)
        if 0 < x < W and 0 < y < H:
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(70, 90, 120, 110))

def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def block(x, y, w, tag, tagcolor, headline, hsize, body, bsize=25, hcolor=PAPER):
    d.rectangle([x, y, x + w, y + 6], fill=tagcolor)
    d.text((x, y + 14), tag, font=f(BOLD, 20), fill=tagcolor)
    yy = y + 42
    for ln in wrap(headline, f(BOLD, hsize), w):
        d.text((x, yy), ln, font=f(BOLD, hsize), fill=hcolor)
        yy += hsize + 6
    for ln in wrap(body, f(REG, bsize), w):
        d.text((x, yy), ln, font=f(REG, bsize), fill=(205, 210, 218))
        yy += bsize + 7
    return yy

# masthead
d.rectangle([0, 0, W, 118], fill=(8, 10, 14))
d.text((36, 18), "THE WORLD IN ONE DAY", font=f(SERIFB, 54), fill=PAPER)
d.text((38, 84), "Tuesday, 24 November 2026  •  The day's news, in one picture", font=f(REG, 22), fill=GREY)
d.rectangle([856, 22, 988, 96], outline=ACCENT, width=3)
d.text((880, 30), "24", font=f(BOLD, 34), fill=ACCENT)
d.text((876, 66), "NOV", font=f(BOLD, 20), fill=PAPER)

# lead story
y = block(36, 140, 952, "WAR WIDENS", ACCENT,
          "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA", 44,
          "Sea drones strike at Benghazi, taking the war far beyond Europe. Strikes on the Kyiv region kill at least 14, and newly leaked data puts Russia's death toll near 500,000.", 26)

# two columns, second row
y2 = max(y + 18, 356)
block(36, y2, 460, "TECH POWER", GOLD,
      "HUANG BACK AT NVIDIA", 32,
      "Trump-backed reversal restores Jensen Huang as CEO; his fortune leaps about $34bn in an evening.", 24)
block(528, y2, 460, "MIDDLE EAST", TEAL,
      "TANKERS BURN IN THE STRAIT OF HORMUZ", 32,
      "Iran says three oil tankers struck sea mines and caught fire on the world's key oil route.", 24)

# third row, three columns
y3 = y2 + 218
block(36, y3, 296, "SPACE", BLUE,
      "NATO EYES SPACE DEFENCE", 25,
      "Allies respond to reports Russia may launch a nuclear space weapon.", 22)
block(364, y3, 296, "ASIA", GREEN,
      "SEOUL SCRAMBLES JETS", 25,
      "Russian warplanes enter South Korea's air zone; China opens Tiangong to foreign crews.", 22)
block(692, y3, 296, "UNITED STATES", GOLD,
      "DEMOCRATS TAKE THE HOUSE", 25,
      "A historic midterm majority of at least 258 seats; storms threaten Thanksgiving travel.", 22)

# bottom strip
y4 = y3 + 218
d.rectangle([0, y4, W, H], fill=DARKPANEL)
d.text((36, y4 + 16), "ALSO TODAY", font=f(BOLD, 20), fill=GREY)
d.text((36, y4 + 46),
       "UN chief: agree AI risk rules within a year",
       font=f(REG, 22), fill=PAPER)
d.text((36, y4 + 80),
       "UN food agency: wars threaten aid for 7.3m more people",
       font=f(REG, 22), fill=PAPER)
d.text((36, y4 + 114),
       "Greece reopens the Acropolis Museum  •  WHO chief visits Cuba amid a health crisis",
       font=f(REG, 22), fill=PAPER)

img.save("/home/hatch/workspace/makefun/entry-news-image/entry.png")
print("saved")
