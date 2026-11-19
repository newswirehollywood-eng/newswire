#!/usr/bin/env python3
"""Freda Payne / Motown for Veterans social cards (Nov 19, 2026).
Builds: cropped burgundy-gown photo (text removed), 1200x630 share image,
1080x1350 Instagram cards per brand, 1080x1080 reel cover cards per brand.
Photos: Courtesy of Freda Payne / PR STARPOWER. Run: python3 tools/cards/freda_motown_cards.py"""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(R, "docs", "img")
SRC = os.path.join(D, "freda-payne-2026")
B = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
BRANDS = {
    "nwh": ("NEWSWIRE HOLLYWOOD", (10, 0, 3), (209, 0, 46), (184, 134, 11), "newswirehollywood.com"),
    "hna": ("HOLLYWOOD NEWS ACCESS", (12, 8, 17), (255, 46, 136), (255, 194, 51), "hollywoodnewsaccess.com"),
    "gna": ("GOSPEL NEWS ACCESS", (10, 10, 12), (240, 180, 41), (240, 180, 41), "gospelnewsaccess.com"),
    "prs": ("PR STARPOWER", (21, 16, 26), (232, 112, 141), (217, 168, 87), "prstarpower.com"),
}
KICK = {"nwh": "JAN. 8 · TEMPE, ARIZ.", "hna": "JAN. 8 · TEMPE, ARIZ.",
        "gna": "SINGING FOR THOSE WHO SERVED", "prs": "CLIENT NEWS · JAN. 8, 2027"}

def f(p, s): return ImageFont.truetype(p, s)

# 1. Burgundy gown: crop to the photo only (drop the other outlet's text and top strip).
g = Image.open(os.path.join(SRC, "freda-payne-burgundy-gown-graphic.jpg")).convert("RGB")
g.crop((0, 95, 540, 770)).save(os.path.join(SRC, "freda-payne-burgundy-gown.jpg"), quality=92)

pink = Image.open(os.path.join(SRC, "freda-payne-pink-gown.jpg")).convert("RGB")
port = Image.open(os.path.join(SRC, "freda-payne-portrait-white.jpg")).convert("RGB")

def text(d, xy, s, font, fill, spacing=10):
    d.multiline_text(xy, s, font=font, fill=fill, spacing=spacing)

# 2. Share image 1200x630: portrait left, text right.
for k, (name, bg, acc, rule, site) in BRANDS.items():
    im = Image.new("RGB", (1200, 630), bg)
    im.paste(ImageOps.fit(port, (473, 630), centering=(0.5, 0.3)), (0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((530, 70, 640, 80), fill=acc)
    text(d, (530, 105), "FREDA PAYNE", f(B, 64), (255, 255, 255))
    text(d, (530, 185), "Motown for Veterans\nBenefit Concert", f(B, 44), (242, 233, 218))
    text(d, (530, 310), "Friday, Jan. 8, 2027 · 7 p.m.\nMullett Arena, Tempe, Ariz.", f(M, 30), rule)
    text(d, (530, 420), "With the Former Ladies of the Supremes,\nGlenn Leonard's Temptations Revue\nand Jr. Walker's All-Star Band", f(M, 24), (200, 196, 190), 8)
    d.text((530, 565), name, font=f(B, 24), fill=acc)
    im.save(os.path.join(D, "freda-motown-veterans-share-%s.jpg" % k), quality=90)

# 3. Instagram cards 1080x1350: pink gown photo, band at bottom.
for k, (name, bg, acc, rule, site) in BRANDS.items():
    im = Image.new("RGB", (1080, 1350), bg)
    im.paste(ImageOps.fit(pink, (1080, 900), centering=(0.55, 0.22)), (0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 900, 1080, 908), fill=acc)
    d.text((64, 940), KICK[k], font=f(B, 30), fill=rule)
    text(d, (64, 990), "FREDA PAYNE SINGS\nFOR VETERANS", f(B, 64), (255, 255, 255), 6)
    d.text((64, 1150), "Mullett Arena · Tempe · Tickets on Ticketmaster", font=f(M, 30), fill=(220, 214, 205))
    d.text((64, 1270), name, font=f(B, 28), fill=acc)
    w = d.textlength(site, font=f(M, 26)); d.text((1080 - 64 - w, 1272), site, font=f(M, 26), fill=(180, 174, 166))
    d.text((64, 1222), "Photo courtesy of Freda Payne / PR STARPOWER", font=f(M, 20), fill=(140, 134, 126))
    im.save(os.path.join(D, "freda-motown-veterans-ig-%s.jpg" % k), quality=90)

# 4. Reel cover cards 1080x1080.
for k, (name, bg, acc, rule, site) in BRANDS.items():
    im = Image.new("RGB", (1080, 1080), bg)
    im.paste(ImageOps.fit(pink, (1080, 760), centering=(0.55, 0.2)), (0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 760, 1080, 768), fill=acc)
    text(d, (60, 800), "FREDA PAYNE\nSINGS FOR VETERANS", f(B, 70), (255, 255, 255), 6)
    d.text((60, 985), "JAN. 8, 2027 · MULLETT ARENA, TEMPE", font=f(B, 32), fill=rule)
    im.save(os.path.join(D, "freda-motown-veterans-reel-card-%s.jpg" % k), quality=90)
print("ok")
