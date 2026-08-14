#!/usr/bin/env python3
"""Render the 1200x630 Open Graph card for sylvesterlimited.tech.

Palette is taken from the site tokens so the card and the page agree.
Re-run after any copy change:  python3 make_og.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630

GROUND = (14, 12, 18)        # hsl(252 20% 6%)
TEXT = (247, 247, 247)       # hsl(0 0% 97%)
MUTED = (142, 138, 155)      # hsl(255 10% 58%)
DIM = (110, 106, 124)
ACCENT = (168, 85, 247)      # hsl(270 80% 65%)
BORDER = (38, 34, 49)        # hsl(255 15% 16%)

SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"
MONO = "/System/Library/Fonts/SFNSMono.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


card = Image.new("RGB", (W, H), GROUND)

# Ambient purple glow — kept faint on purpose. The page's ground stays
# near-black; a strong wash would read as a gradient poster, not as this site.
glow = Image.new("RGB", (W, H), GROUND)
gd = ImageDraw.Draw(glow)
gd.ellipse([-300, 210, 520, 860], fill=(74, 34, 118))
glow = glow.filter(ImageFilter.GaussianBlur(170))
card = Image.blend(card, glow, 0.42)

d = ImageDraw.Draw(card)

# Hairline frame, echoing the page's 1px borders.
d.rectangle([40, 40, W - 41, H - 41], outline=BORDER, width=1)

x = 96
y = 118

# Eyebrow
d.ellipse([x, y + 7, x + 11, y + 18], fill=ACCENT)
d.text((x + 26, y), "DAR ES SALAAM, TANZANIA", font=font(MONO, 21), fill=MUTED)

# Wordmark
y += 62
d.text((x, y), "Sylvester Limited", font=font(SANS_BOLD, 82), fill=TEXT)

# Thesis line, accent half on its own line
y += 116
d.text((x, y), "Software for East Africa,", font=font(SANS, 46), fill=TEXT)
y += 62
d.text((x, y), "built and run in-house.", font=font(SANS, 46), fill=ACCENT)

# Proof strip
y = H - 132
d.line([x, y, W - 96, y], fill=BORDER, width=1)
d.text(
    (x, y + 30),
    "KAZILAW   ·   DINO IG   ·   CHUMA   ·   SEMA   ·   ROUTINE-ENGINE",
    font=font(MONO, 22),
    fill=DIM,
)

card.save("og.png", "PNG", optimize=True)
print(f"wrote og.png  {card.size[0]}x{card.size[1]}")
