#!/usr/bin/env python3
"""Meme v2 for gta6-meme-x-01: launch-day sick day in Leonida.

The make.fun ghost (official press mark) sits up in bed in a Vice City
bedroom, phone to its ear, calling in sick: "BOSS, I CAN'T COME IN.
LEONIDA NEEDS ME." A neon make.fun sign on the wall is the second anchor;
the bottom tag sells the pitch: the agent covers the shift and gets paid.

Vector scene drawn with Pillow; square 1024x1024 PNG.
Usage: python3 meme_gen2.py [mark.png] [out.png]
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
MARK = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "press", "mark-1024.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "meme2.png")

NEON_PINK = (255, 45, 149)
NEON_CYAN = (0, 229, 255)
INK = (16, 8, 28)


def font(size):
    for path in (
        os.path.join(HERE, "fonts", "ArchivoBlack-Regular.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit("no font found")


def fit_font(text, max_w, start, minimum=24):
    size = start
    while size > minimum:
        f = font(size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return font(minimum)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def v_gradient(d, x0, x1, y0, y1, stops):
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0 - 1))
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                d.line([(x0, y), (x1, y)], fill=lerp(c0, c1, (t - p0) / (p1 - p0)))
                break


def caption(img, text, cy, max_w=950, start=96, fill=(255, 255, 255)):
    f = fit_font(text, max_w, start)
    d = ImageDraw.Draw(img)
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, cy), text, font=f, fill=fill,
           stroke_width=max(4, f.size // 12), stroke_fill=INK)
    return f.size


# ---------------------------------------------------------------- bedroom wall + floor
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
v_gradient(d, 0, W, 0, 760, [
    (0.00, (26, 12, 48)),
    (0.60, (44, 20, 74)),
    (1.00, (58, 26, 92)),
])
# floor
v_gradient(d, 0, W, 760, H, [
    (0.00, (36, 18, 58)),
    (1.00, (24, 12, 42)),
])
d.line([(0, 760), (W, 760)], fill=(90, 44, 120), width=3)
# faint wall stripes (art-deco wallpaper)
for x in range(40, W, 96):
    d.line([(x, 110), (x, 758)], fill=(52, 24, 84), width=2)

# ---------------------------------------------------------------- window: neon palm sunrise
wx0, wy0, wx1, wy1 = 62, 150, 402, 562
# view inside the window
v_gradient(d, wx0 + 10, wx1 - 10, wy0 + 10, wy1 - 10, [
    (0.00, (40, 16, 80)),
    (0.45, (178, 44, 118)),
    (0.78, (255, 107, 53)),
    (1.00, (255, 190, 90)),
])
# rising sun
scx, scy, sr = 232, 470, 78
for y in range(scy - sr, min(scy + sr, wy1 - 10)):
    t = (y - (scy - sr)) / (2 * sr)
    half = math.sqrt(max(0.0, sr ** 2 - (y - scy) ** 2))
    d.line([(scx - half, y), (scx + half, y)], fill=lerp((255, 224, 60), (255, 60, 120), t))
# skyline silhouette in the window
for bx0, bx1, btop in [(80, 130, 470), (136, 176, 440), (286, 330, 458), (334, 386, 486)]:
    d.rectangle([bx0, btop, bx1, wy1 - 10], fill=(30, 14, 52))
    for wy in range(btop + 10, wy1 - 18, 16):
        for wxx in range(bx0 + 6, bx1 - 6, 12):
            d.rectangle([wxx, wy, wxx + 4, wy + 6], fill=(255, 214, 120))
# palm silhouette in the window
PALM = (22, 10, 40)
d.polygon([(150, wy1 - 10), (162, wy1 - 10), (176, 330), (166, 330)], fill=PALM)
for ang in (-165, -120, -75, -30, 10):
    a = math.radians(ang)
    tx, ty = 171, 330
    L = 74
    ex, ey = tx + L * math.cos(a), ty + L * math.sin(a) * 0.6 + 16
    mx, my = tx + L * 0.55 * math.cos(a), ty + L * 0.55 * math.sin(a) * 0.6 - 14
    leaf = []
    for i in range(11):
        t = i / 10
        bx = (1 - t) ** 2 * tx + 2 * (1 - t) * t * mx + t ** 2 * ex
        by = (1 - t) ** 2 * ty + 2 * (1 - t) * t * my + t ** 2 * ey
        leaf.append((bx, by - 7 * math.sin(t * math.pi)))
    for i in range(10, -1, -1):
        t = i / 10
        bx = (1 - t) ** 2 * tx + 2 * (1 - t) * t * mx + t ** 2 * ex
        by = (1 - t) ** 2 * ty + 2 * (1 - t) * t * my + t ** 2 * ey
        leaf.append((bx, by + 7 * math.sin(t * math.pi)))
    d.polygon(leaf, fill=PALM)
# window frame + cross bars
d.rectangle([wx0, wy0, wx1, wy1], outline=(120, 70, 150), width=10)
d.line([(232, wy0), (232, wy1)], fill=(120, 70, 150), width=8)
d.line([(wx0, 356), (wx1, 356)], fill=(120, 70, 150), width=8)
# sunrise glow spilling into the room
spill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(spill).rectangle([wx0 - 20, wy0 - 20, wx1 + 60, wy1 + 60], fill=(255, 120, 90, 46))
img = Image.alpha_composite(img.convert("RGBA"), spill.filter(ImageFilter.GaussianBlur(36)))
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- neon wall sign: make.fun
sign_f = font(54)
sign_text = "make.fun"
sw = d.textlength(sign_text, font=sign_f)
sx, sy = 700 - sw / 2, 168
neon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
nd = ImageDraw.Draw(neon)
nd.text((sx, sy), sign_text, font=sign_f, fill=NEON_PINK + (255,))
nd.line([(sx - 16, sy + 70), (sx + sw + 16, sy + 70)], fill=NEON_PINK + (255,), width=3)
img = Image.alpha_composite(img, neon.filter(ImageFilter.GaussianBlur(9)))
img = Image.alpha_composite(img, neon)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- speech bubble (the joke)
bub = [452, 268, 1000, 458]
d.rounded_rectangle(bub, radius=30, fill=(255, 255, 255), outline=INK, width=6)
# tail pointing down-left toward the ghost
d.polygon([(560, 452), (620, 452), (540, 528)], fill=(255, 255, 255), outline=INK)
d.line([(562, 452), (618, 452)], fill=(255, 255, 255), width=8)  # seamless join
bf1 = fit_font("BOSS, I CAN'T COME IN.", 500, 46)
bf2 = fit_font("LEONIDA NEEDS ME.", 500, 46)
d.text((478, 292), "BOSS, I CAN'T COME IN.", font=bf1, fill=INK)
d.text((478, 360), "LEONIDA NEEDS ME.", font=bf2, fill=(160, 16, 88))

# ---------------------------------------------------------------- bed + ghost
# headboard (right side)
d.rounded_rectangle([930, 470, 1024, 900], radius=18, fill=(96, 44, 70), outline=(140, 70, 100), width=4)
for yy in range(510, 860, 60):
    d.line([(946, yy), (1010, yy)], fill=(140, 70, 100), width=3)
# mattress base
d.rounded_rectangle([430, 800, 1024, 912], radius=16, fill=(232, 226, 240), outline=(150, 140, 170), width=3)
# pillow behind the ghost
d.rounded_rectangle([470, 640, 660, 760], radius=26, fill=(250, 246, 255), outline=(170, 160, 190), width=3)

# warm lamp glow so the mark sits in the room light
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([430, 420, 950, 900], fill=(255, 150, 110, 56))
img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(42)))

# the official make.fun mark: the ghost sitting up in bed (~410 px across)
mark = Image.open(MARK).convert("RGBA")
mark = mark.crop(mark.getchannel("A").getbbox())
MD = 410
mark = mark.resize((MD, MD), Image.LANCZOS)
mx, my = 705 - MD // 2, 655 - MD // 2
img.paste(mark, (mx, my), mark)
d = ImageDraw.Draw(img)

# blanket over the lower part of the disc (ghost is IN the bed)
blanket = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(blanket)
bd.polygon([(432, 780), (520, 748), (640, 768), (760, 744), (880, 770),
            (1024, 752), (1024, 908), (432, 908)], fill=(214, 40, 120, 255))
# folds
for fx in (540, 680, 820, 950):
    bd.line([(fx, 770), (fx - 14, 906)], fill=(170, 26, 96, 255), width=5)
bd.line([(432, 780), (520, 748), (640, 768), (760, 744), (880, 770), (1024, 752)],
        fill=(255, 120, 180, 255), width=5)
img = Image.alpha_composite(img, blanket)
d = ImageDraw.Draw(img)

# phone in the ghost's hand, mid-call: a round white hand (ghost style)
# grips the phone at the ghost's right side, screen glowing green
phone = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(phone)
pd.rounded_rectangle([836, 640, 890, 736], radius=12, fill=INK + (255,), outline=(200, 200, 220, 255), width=3)
pd.rounded_rectangle([844, 652, 882, 724], radius=6, fill=(60, 220, 130, 255))
pd.ellipse([854, 670, 872, 688], fill=(255, 255, 255, 255))
pd.line([(856, 702), (870, 702)], fill=(255, 255, 255, 255), width=3)
# the hand: white circle, thick black outline, overlapping phone and ghost body
pd.ellipse([816, 688, 862, 734], fill=(255, 255, 255, 255), outline=INK + (255,), width=6)
img = Image.alpha_composite(img, phone.filter(ImageFilter.GaussianBlur(3)))
img = Image.alpha_composite(img, phone)
d = ImageDraw.Draw(img)
# call waves from the phone's top-right corner
for r in (14, 24, 34):
    d.arc([892 - r, 648 - r, 892 + r, 648 + r], start=-55, end=55, fill=NEON_CYAN, width=3)

# ---------------------------------------------------------------- TV on a dresser: GTA VI
d.rectangle([60, 700, 392, 760], fill=(70, 34, 60))          # dresser top
d.rectangle([76, 760, 376, 900], fill=(54, 26, 48))          # dresser body
d.line([(76, 810), (376, 810)], fill=(90, 44, 80), width=3)
d.ellipse([200, 830, 252, 856], fill=(90, 44, 80))           # drawer knob
tv = [96, 560, 356, 704]
d.rounded_rectangle(tv, radius=16, fill=(28, 18, 40), outline=NEON_CYAN, width=4)
scr = [114, 578, 338, 686]
d.rounded_rectangle(scr, radius=10, fill=(10, 8, 34), outline=(80, 64, 130), width=3)
gf = font(52)
gt = "GTA VI"
gw = d.textlength(gt, font=gf)
d.text(((scr[0] + scr[2]) / 2 - gw / 2, 592), gt, font=gf, fill=(255, 211, 25))
pf = font(22)
pt = "READY TO PLAY"
pw = d.textlength(pt, font=pf)
d.text(((scr[0] + scr[2]) / 2 - pw / 2, 652), pt, font=pf, fill=NEON_CYAN)
# TV glow on the wall
tvglow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(tvglow).rectangle([76, 540, 376, 724], fill=(0, 200, 255, 40))
img = Image.alpha_composite(img, tvglow.filter(ImageFilter.GaussianBlur(26)))
d = ImageDraw.Draw(img)
# game controller on the blanket
cx, cy = 560, 850
d.rounded_rectangle([cx - 46, cy - 16, cx + 46, cy + 18], radius=16, fill=INK)
d.ellipse([cx - 58, cy - 8, cx - 26, cy + 24], fill=INK)
d.ellipse([cx + 26, cy - 8, cx + 58, cy + 24], fill=INK)
d.line([(cx - 40, cy + 2), (cx - 24, cy + 2)], fill=(200, 200, 220), width=3)
d.line([(cx - 32, cy - 6), (cx - 32, cy + 10)], fill=(200, 200, 220), width=3)
d.ellipse([cx + 28, cy - 2, cx + 36, cy + 6], fill=NEON_PINK)
d.ellipse([cx + 38, cy + 6, cx + 46, cy + 14], fill=NEON_CYAN)

# ---------------------------------------------------------------- captions
img = img.convert("RGB")
caption(img, "CALLING IN SICK FOR GTA 6", 24, start=92)
caption(img, "my make.fun agent covers my shift - and gets paid", 944, max_w=980, start=48)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size)
