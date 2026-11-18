#!/usr/bin/env python3
"""Draw the 18 Nov 2026 world-news front page, 1024x1024, deterministic.
No network, no randomness. Run from this directory: it writes entry.png
beside this script. Fonts: DejaVu (system)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

W, H = 1024, 1024
NAVY = (15, 42, 74)
RED = (178, 34, 34)
INK = (20, 20, 20)
GREY = (90, 90, 90)
LIGHT = (242, 244, 247)

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

def wrap(draw, text, fnt, max_w):
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

def para(x, y, text, fnt, max_w, leading, color=INK):
    lines = wrap(d, text, fnt, max_w)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y

# Header
d.rectangle([0, 0, W, 148], fill=NAVY)
d.text((32, 22), "THE WORLD IN ONE DAY", font=F_SERIF_B(58), fill="white")
d.text((32, 100), "WEDNESDAY 18 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE IMAGE", font=F_SANS_B(21), fill=(255, 210, 90))

# Lead story
y = 168
d.rectangle([32, y, 42, y + 8], fill=RED)
d.text((56, y - 6), "LEAD  —  THE GULF", font=F_SANS_B(20), fill=RED)
y += 34
d.text((32, y), "IRAN STRIKES BACK IN", font=F_SERIF_B(40), fill=INK)
y += 48
d.text((32, y), "THE GULF", font=F_SERIF_B(40), fill=INK)
y += 56
y = para(32, y, "Iran hit US bases in Kuwait and Bahrain early today, after American jets struck a missile site on Qeshm Island. Tehran said it targeted the Ali Al Salem base, which hosts US forces. The Strait of Hormuz stayed open but on edge.", F_SANS(22), 960, 28)
d.line([32, y + 12, 992, y + 12], fill=(200, 200, 200), width=2)

# Grid: 2 columns x 3 rows (6 stories)
stories = [
    ("UKRAINE", (178, 34, 34), "KERCH BRIDGE SPAN FALLS",
     "A second day of Ukrainian drone and missile strikes partly collapsed the bridge to Crimea. A road span fell into the strait and traffic halted."),
    ("ASIA", (15, 90, 140), "XI AND PUTIN MEET BEFORE TRUMP SUMMIT",
     "China and Russia's leaders opened talks in Shenzhen ahead of Thursday's three-way summit with Donald Trump."),
    ("US POLITICS", (120, 70, 140), "DEMOCRATS TAKE THE SENATE",
     "Mary Peltola beat Dan Sullivan in Alaska, giving Democrats a 56-44 majority in the incoming Senate."),
    ("HEALTH", (0, 120, 90), "EBOLA IN CONGO MORE THAN DOUBLES",
     "The outbreak passed 11,000 cases and 5,400 deaths in three months. Three in four infected children under five die, health officials said."),
    ("HEALTH", (0, 120, 90), "US LOSES MEASLES-FREE STATUS",
     "After 26 years, the US lost measles elimination status, with more than 5,400 cases and 10 deaths this year."),
    ("TECH", (140, 40, 90), "NVIDIA REVENUE DOUBLES",
     "Third-quarter revenue doubled. Its former chief faces Congress over alleged chip smuggling, and the US moved to block China's remote access to AI chips."),
]
grid_top = y + 28
cell_w, cell_h = 480, 160
for i, (tag, color, head, body) in enumerate(stories):
    col, row = i % 2, i // 2
    x = 32 + col * 480
    yy = grid_top + row * cell_h
    if col == 1:
        x = 512
    d.rectangle([x, yy, x + 6, yy + 18], fill=color)
    d.text((x + 16, yy - 2), tag, font=F_SANS_B(17), fill=color)
    yy2 = yy + 24
    for ln in wrap(d, head, F_SERIF_B(23), cell_w - 16):
        d.text((x, yy2), ln, font=F_SERIF_B(23), fill=INK)
        yy2 += 28
    para(x, yy2 + 2, body, F_SANS(18), cell_w - 16, 24)

# Bottom strip
strip_y = grid_top + 3 * cell_h + 8
d.rectangle([0, strip_y, W, strip_y + 64], fill=LIGHT)
d.text((32, strip_y + 8), "ALSO ON 18 NOVEMBER", font=F_SANS_B(18), fill=NAVY)
para(32, strip_y + 32, "Russian military plane crashes in Siberia, 19 dead  •  Category 5 Cyclone Xavier hits the Northern Cook Islands  •  COP31 talks deadlocked in Antalya  •  Gaza cold kills in tents  •  GTA VI unlocks at midnight, New Zealand first", F_SANS(16), 960, 20)

# Footer
d.text((32, 992), "Sources: Reuters  •  AP  •  UN  •  NPR      Events of 18 November 2026, in any time zone", font=F_SANS(16), fill=GREY)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(OUT, os.path.getsize(OUT), img.size)
