#!/usr/bin/env python3
"""Render the 1200x630 Open Graph card for sylvesterlimited.tech.

Palette is taken from the site tokens so the card and the page agree.
Re-run after any copy change:  python3 make_og.py
Needs Pillow (pip install pillow). Fonts are looked up from a list of
candidates so this runs on macOS and Linux alike.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630

VOID = (5, 5, 10)            # --void
INK = (243, 243, 248)        # --ink
MUTED = (156, 156, 178)      # --muted
DIM = (98, 98, 122)          # --dim
ACCENT = (168, 85, 247)      # --accent   hsl(270 80% 65%)
ICE = (125, 211, 252)        # --ice      hsl(196 92% 74%)
LINE = (255, 255, 255, 26)   # --line

SANS_CANDIDATES = [
    # Space Grotesk is the site face; fall back to any decent grotesk.
    "/usr/share/fonts/truetype/spacegrotesk/SpaceGrotesk-SemiBold.ttf",
    os.path.expanduser("~/Library/Fonts/SpaceGrotesk-SemiBold.ttf"),
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
MONO_CANDIDATES = [
    "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf",
    os.path.expanduser("~/Library/Fonts/JetBrainsMono-Regular.ttf"),
    "/System/Library/Fonts/SFNSMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
]


def font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


card = Image.new("RGB", (W, H), VOID)

# Two faint pools of light, far apart, so the ground stays matte black.
glow = Image.new("RGB", (W, H), VOID)
gd = ImageDraw.Draw(glow)
gd.ellipse([720, -80, 1380, 520], fill=(46, 22, 96))
gd.ellipse([-260, 380, 380, 900], fill=(14, 40, 62))
glow = glow.filter(ImageFilter.GaussianBlur(160))
card = Image.blend(card, glow, 0.55)

# --- The crystal: a seeded shard cluster, drawn as translucent facets. ---
random.seed(1013)
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(layer)
cx, cy = 935, 300


def shard(cx, cy, length, width, angle):
    a = math.radians(angle)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    tip = (cx + dx * length, cy + dy * length)
    base = (cx - dx * length * 0.55, cy - dy * length * 0.55)
    l = (cx + nx * width, cy + ny * width)
    r = (cx - nx * width, cy - ny * width)
    return [tip, l, base, r]


shards = []
for i in range(7):
    ang = random.uniform(0, 360)
    ln = random.uniform(90, 175)
    wd = random.uniform(56, 100)
    off = random.uniform(0, 40)
    ox = cx + math.cos(math.radians(ang + 90)) * off
    oy = cy + math.sin(math.radians(ang + 90)) * off
    shards.append(shard(ox, oy, ln, wd, ang))

for poly in shards:
    t = random.random()
    base = tuple(int(ACCENT[k] * (1 - t) + ICE[k] * t) for k in range(3))
    # body: dark glass
    ld.polygon(poly, fill=tuple(int(c * 0.30) for c in base) + (215,))
    # one lit facet per shard
    ld.polygon([poly[0], poly[1], poly[2]], fill=base + (74,))
for poly in shards:
    t = random.random()
    edge = tuple(int(ACCENT[k] * (1 - t) + ICE[k] * t) for k in range(3)) + (120,)
    ld.line(poly + [poly[0]], fill=edge, width=2)
    # one internal ridge per shard
    ld.line([poly[0], poly[2]], fill=edge[:3] + (70,), width=1)

# soft bloom under the edges
bloom = layer.filter(ImageFilter.GaussianBlur(14))
card = Image.alpha_composite(card.convert("RGBA"), bloom)
card = Image.alpha_composite(card, layer)

d = ImageDraw.Draw(card)

# Hairline frame, echoing the page's 1px borders.
d.rectangle([40, 40, W - 41, H - 41], outline=(30, 30, 44), width=1)

mono_s = font(MONO_CANDIDATES, 17)
mono_xs = font(MONO_CANDIDATES, 15)
sans_xl = font(SANS_CANDIDATES, 74)
sans_m = font(SANS_CANDIDATES, 24)

# Corner instrumentation.
d.text((72, 66), "SYLVESTER LIMITED", font=mono_s, fill=MUTED)
loc = "DAR ES SALAAM · 06°47′S 39°12′E"
lw = d.textlength(loc, font=mono_s)
d.text((W - 72 - lw, 66), loc, font=mono_s, fill=DIM)

# Headline.
y = 205
d.text((72, y), "We build software", font=sans_xl, fill=INK)
d.text((72, y + 84), "for East Africa", font=sans_xl, fill=INK)
# gradient line, rendered through a mask
line = "and run it ourselves."
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).text((72, y + 168), line, font=sans_xl, fill=255)
grad = Image.new("RGB", (W, H), ACCENT)
gp = grad.load()
for x in range(W):
    t = min(1.0, max(0.0, (x - 72) / 720))
    col = tuple(int(ACCENT[k] * (1 - t) + ICE[k] * t) for k in range(3))
    for yy in range(y + 150, y + 260):
        gp[x, yy] = col
card.paste(grad, (0, 0), mask)

d = ImageDraw.Draw(card)
d.text((72, 500), "Web platforms · Mobile applications · AI agent systems", font=sans_m, fill=MUTED)
d.text((72, 546), "EVERY CLAIM OPENS IN A NEW TAB", font=mono_xs, fill=DIM)

# Accent pip + status readout, bottom right.
pip = "● 5 PRODUCTS · 15+ SERVICES · SELF-HOSTED"
pw = d.textlength(pip, font=mono_xs)
d.text((W - 72 - pw, 546), pip, font=mono_xs, fill=ACCENT)

card.convert("RGB").save("og.png", optimize=True)
print("wrote og.png")
