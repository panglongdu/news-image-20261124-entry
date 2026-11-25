#!/usr/bin/env python3
"""v2 front page: 24 Nov 2026 world news as a rich magazine cover.

Deep-navy broadsheet with an amber/red accent system: a dominant lead
story with a drawn sea-battle panel, a band of big-number stats, two
columns of tagged stories and a ticker strip along the bottom.
Rendered with Pillow at 1024x1024.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
NAVY = (9, 13, 25)
PANEL = (17, 23, 40)
PANEL2 = (22, 30, 52)
INK = (245, 239, 227)
MUTE = (168, 176, 192)
AMBER = (245, 176, 65)
RED = (228, 62, 47)
TEAL = (74, 192, 202)
BLUE = (102, 144, 232)
GREEN = (122, 202, 122)
WHITE = (255, 255, 255)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

canvas = Image.new("RGB", (SIZE, SIZE), NAVY)
pen = ImageDraw.Draw(canvas, "RGBA")


def typeface(path, px):
    return ImageFont.truetype(path, px)


def lines_for(text, face, width):
    """Greedy word-wrap using real glyph widths."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if pen.textlength(trial, font=face) <= width:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(x, y, text, face, width, colour, leading):
    for ln in lines_for(text, face, width):
        pen.text((x, y), ln, font=face, fill=colour)
        y += leading
    return y


def chip(x, y, label, colour, txt=WHITE, px=19):
    face = typeface(FB, px)
    w = pen.textlength(label, font=face) + 22
    pen.rectangle([x, y, x + w, y + px + 12], fill=colour)
    pen.text((x + 11, y + 5), label, font=face, fill=txt)
    return w


# ---------------------------------------------------------------- masthead
pen.rectangle([0, 0, SIZE, 104], fill=(5, 7, 14))
pen.text((40, 16), "THE WORLD IN ONE DAY", font=typeface(FS, 50), fill=INK)
pen.text((42, 76), "Tuesday, 24 November 2026  -  the whole day, on one page",
         font=typeface(FR, 20), fill=MUTE)
pen.rectangle([872, 14, 984, 90], outline=AMBER, width=3)
pen.text((892, 20), "24", font=typeface(FB, 36), fill=AMBER)
pen.text((886, 60), "NOV", font=typeface(FB, 19), fill=INK)
pen.rectangle([0, 108, SIZE, 112], fill=AMBER)

# ---------------------------------------------------------------- lead story
LX, LY, LW = 40, 132, 548
chip(LX, LY, "LEAD STORY", RED)
head_face = typeface(FB, 44)
hy = para(LX, LY + 48,
          "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
          head_face, LW, INK, 52)
para(LX, hy + 8,
     "Sea drones strike at Benghazi, carrying the war far beyond "
     "Europe. Strikes near Kyiv kill at least 14.",
     typeface(FR, 23), LW, MUTE, 30)
pen.rectangle([LX, hy + 106, LX + 120, hy + 110], fill=RED)
pen.text((LX, hy + 122), "ONE WAR, TWO FRONTS: BENGHAZI AND KYIV",
         font=typeface(FB, 16), fill=AMBER)

# lead visual panel: night sea, warship silhouette, incoming sea drones
VX, VY, VW, VH = 616, 132, 368, 252
pen.rectangle([VX, VY, VX + VW, VY + VH], fill=PANEL2)
pen.line([600, VY, 600, VY + VH], fill=(52, 62, 90), width=2)
for sx, sy, sr in ((30, 34, 2), (86, 58, 1), (140, 26, 2), (196, 52, 1),
                   (238, 30, 2), (120, 84, 1), (64, 96, 1), (330, 44, 2)):
    pen.ellipse([VX + sx - sr, VY + sy - sr, VX + sx + sr, VY + sy + sr],
                fill=(200, 210, 235))
pen.arc([VX + 296, VY + 16, VX + 340, VY + 60], 60, 300, fill=AMBER, width=4)
pen.arc([VX + 306, VY + 14, VX + 344, VY + 58], 60, 300, fill=AMBER, width=3)
for i in range(9):  # sea bands
    yy = VY + 118 + i * 13
    pen.line([VX + 8, yy, VX + VW - 8, yy], fill=(38, 62, 104), width=2)
for sx in range(VX + 26, VX + VW - 70, 44):  # wave crests
    for row, off in ((146, 0), (186, 22), (226, 8)):
        pen.arc([sx + off, VY + row, sx + off + 26, VY + row + 12],
                180, 360, fill=(90, 140, 200), width=2)
# warship silhouette (right side of panel)
ship = [(VX + 196, VY + 126), (VX + 344, VY + 126), (VX + 326, VY + 150),
        (VX + 214, VY + 150)]
pen.polygon(ship, fill=(6, 8, 16))
pen.rectangle([VX + 244, VY + 100, VX + 300, VY + 126], fill=(6, 8, 16))
pen.rectangle([VX + 262, VY + 78, VX + 282, VY + 100], fill=(6, 8, 16))
pen.line([VX + 306, VY + 126, VX + 306, VY + 68], fill=(6, 8, 16), width=4)
pen.line([VX + 306, VY + 68, VX + 330, VY + 80], fill=(6, 8, 16), width=3)
# two sea drones (left) with dashed wakes aimed at the ship
for dy in (100, 146):
    pen.polygon([(VX + 42, VY + dy), (VX + 84, VY + dy + 9),
                 (VX + 42, VY + dy + 18)], fill=RED)
    for t in range(6):
        x0 = VX + 92 + t * 16
        pen.line([x0, VY + dy + 9, x0 + 8, VY + dy + 9],
                 fill=(240, 120, 100), width=2)
pen.text((VX + 18, VY + 12), "BENGHAZI - LIBYA", font=typeface(FB, 19),
         fill=AMBER)
# big toll figure under the panel
pen.text((VX, VY + VH + 12), "500,000", font=typeface(FB, 54), fill=RED)
pen.text((VX + 2, VY + VH + 74), "leaked Russian death toll",
         font=typeface(FR, 19), fill=MUTE)

# ---------------------------------------------------------------- stat band
SY = 492
pen.rectangle([40, SY, 984, SY + 92], fill=PANEL)
stats = [("14+", "killed near Kyiv", RED),
         ("$34B", "Huang fortune jump", AMBER),
         ("258", "Democrat House seats", TEAL),
         ("3", "tankers ablaze, Hormuz", BLUE)]
for i, (num, label, colour) in enumerate(stats):
    cx = 64 + i * 238
    if i:
        pen.line([cx - 22, SY + 16, cx - 22, SY + 80], fill=(52, 62, 90),
                 width=2)
    pen.text((cx, SY + 10), num, font=typeface(FB, 40), fill=colour)
    pen.text((cx, SY + 60), label, font=typeface(FR, 17), fill=MUTE)

# ---------------------------------------------------------------- story columns
def story(x, y, w, tag, colour, headline, body):
    chip(x, y, tag, colour, px=14)
    yy = para(x, y + 28, headline, typeface(FB, 21), w, INK, 25)
    yy = para(x, yy + 2, body, typeface(FR, 17), w, MUTE, 21)
    return yy + 10


COLW = 452
y = 608
y = story(40, y, COLW, "MIDDLE EAST", TEAL,
          "TANKERS BURN IN HORMUZ STRAIT",
          "Iran says three tankers hit sea mines in Hormuz.")
y = story(40, y, COLW, "SPACE", BLUE,
          "NATO EYES SPACE DEFENCE",
          "Allies answer reports of a nuclear satellite plan.")
y = story(40, y, COLW, "ASIA", GREEN,
          "SEOUL SCRAMBLES JETS",
          "Russian warplanes enter the South Korean air zone.")

y = 608
y = story(532, y, COLW, "UNITED STATES", AMBER,
          "DEMOCRATS TAKE THE HOUSE",
          "A historic midterm majority of at least 258 seats.")
y = story(532, y, COLW, "SPACE TRAVEL", BLUE,
          "TIANGONG OPENS ITS DOORS",
          "China invites foreign astronauts to its station.")
y = story(532, y, COLW, "CULTURE - HEALTH", RED,
          "ACROPOLIS REOPENS; WHO IN CUBA",
          "Athens' museum returns; WHO chief visits Havana.")

# ---------------------------------------------------------------- ticker
TY = 902
pen.rectangle([0, TY, SIZE, SIZE], fill=(30, 10, 10))
pen.rectangle([0, TY, SIZE, TY + 4], fill=RED)
pen.text((40, TY + 12), "ALSO TODAY", font=typeface(FB, 18), fill=AMBER)
ticks = ["UN chief: agree global AI risk rules within a year",
         "UN food agency: wars threaten aid for 7.3 million more people",
         "Storms threaten Thanksgiving travel across the United States"]
ty = TY + 38
for t in ticks:
    pen.text((40, ty), "-  " + t, font=typeface(FR, 19), fill=INK)
    ty += 26

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
canvas.save(out)
print("saved", out, os.path.getsize(out))
