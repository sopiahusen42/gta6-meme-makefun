#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: Vice City sunset, make.fun ghost in a deck
chair, GTA VI installing at 99%, 13-years-vs-13-minutes caption.

Vector scene drawn with Pillow; the official make.fun press mark
(mark-1024.png) is composited in as the lounging ghost. Square 1024x1024 PNG.

Usage: python3 meme_gen.py [mark.png] [out.png]
Font: fonts/ArchivoBlack-Regular.ttf if present, else DejaVuSans-Bold.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
MARK = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "press", "mark-1024.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "meme.png")

HORIZON = 580          # sky meets ocean
SHORE = 720            # ocean meets sand


def font(size):
    for path in (
        os.path.join(HERE, "fonts", "ArchivoBlack-Regular.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise SystemExit("no font found")


def fit_font(text, max_w, start, minimum=30):
    """Largest font size (<= start) whose rendered text fits max_w."""
    size = start
    while size > minimum:
        f = font(size)
        if f.getlength(text) <= max_w:
            return f
        size -= 2
    return font(minimum)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def v_gradient(draw, y0, y1, stops):
    """Vertical gradient between (pos, color) stops, pos in 0..1."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0 - 1))
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                draw.line([(0, y), (W, y)], fill=lerp(c0, c1, (t - p0) / (p1 - p0)))
                break


def caption(img, text, cy, max_w=950, start=96, fill=(255, 255, 255)):
    f = fit_font(text, max_w, start)
    d = ImageDraw.Draw(img)
    w = d.textlength(text, font=f)
    x = (W - w) / 2
    d.text((x, cy), text, font=f, fill=fill,
           stroke_width=max(4, f.size // 12), stroke_fill=(10, 5, 20))
    return f.size


# ---------------------------------------------------------------- sky
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
v_gradient(d, 0, HORIZON, [
    (0.00, (24, 10, 58)),
    (0.35, (88, 24, 110)),
    (0.65, (214, 51, 132)),
    (0.88, (255, 107, 53)),
    (1.00, (255, 179, 71)),
])

# stars in the upper sky
for sx, sy, r in [(90, 60, 2), (210, 120, 2), (330, 50, 3), (560, 90, 2),
                  (700, 40, 2), (820, 110, 3), (950, 70, 2), (470, 150, 2),
                  (150, 200, 2), (900, 190, 2)]:
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 240, 255))

# ---------------------------------------------------------------- synthwave sun
sun_cx, sun_cy, sun_r = 430, 505, 168
sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sun)
for y in range(sun_cy - sun_r, sun_cy + sun_r):
    t = (y - (sun_cy - sun_r)) / (2 * sun_r)
    col = lerp((255, 211, 25), (255, 41, 117), t) + (255,)
    half = math.sqrt(max(0.0, sun_r ** 2 - (y - sun_cy) ** 2))
    sd.line([(sun_cx - half, y), (sun_cx + half, y)], fill=col)
# horizontal slice gaps in the lower half (classic retro sun)
gap_y = sun_cy + 8
gap_h = 4
while gap_y < sun_cy + sun_r:
    sd.rectangle([sun_cx - sun_r, gap_y, sun_cx + sun_r, gap_y + gap_h], fill=(0, 0, 0, 0))
    gap_y += gap_h + 14
    gap_h += 3
# soft glow behind the sun
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse(
    [sun_cx - sun_r - 40, sun_cy - sun_r - 40, sun_cx + sun_r + 40, sun_cy + sun_r + 40],
    fill=(255, 120, 90, 90))
glow = glow.filter(ImageFilter.GaussianBlur(30))
img = Image.alpha_composite(img.convert("RGBA"), glow)
img = Image.alpha_composite(img, sun)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- art-deco hotel strip
DECO = (30, 16, 56)
NEON_PINK = (255, 45, 149)
NEON_CYAN = (0, 229, 255)


def hotel(x0, x1, top, neon, deco_top=False):
    d.rectangle([x0, top, x1, HORIZON + 2], fill=DECO)
    if deco_top:  # stepped art-deco crown
        step = (x1 - x0) // 6
        d.rectangle([x0 + step, top - 18, x1 - step, top], fill=DECO)
        d.rectangle([x0 + 2 * step, top - 34, x1 - 2 * step, top - 18], fill=DECO)
        d.line([(x0 + 2 * step, top - 34), (x1 - 2 * step, top - 34)], fill=neon, width=3)
    d.line([(x0, top), (x1, top)], fill=neon, width=3)
    d.line([(x0, top), (x0, HORIZON)], fill=neon, width=2)
    d.line([(x1, top), (x1, HORIZON)], fill=neon, width=2)
    # lit windows
    for wy in range(top + 16, HORIZON - 10, 22):
        for wx in range(x0 + 10, x1 - 8, 20):
            d.rectangle([wx, wy, wx + 8, wy + 10], fill=(255, 214, 120))


hotel(-10, 90, 500, NEON_PINK)
hotel(95, 205, 452, NEON_CYAN, deco_top=True)
hotel(210, 300, 512, NEON_PINK)
hotel(305, 380, 535, NEON_CYAN)

# rooftop neon sign: make.fun (second recognition anchor, worked into the scene)
sign_f = font(40)
sign_text = "make.fun"
sw = d.textlength(sign_text, font=sign_f)
sx0, sy0 = 235 - sw / 2 - 14, 386
sign_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sgd = ImageDraw.Draw(sign_glow)
sgd.rectangle([sx0, sy0, sx0 + sw + 28, sy0 + 58], outline=NEON_CYAN + (255,), width=3)
sgd.text((sx0 + 14, sy0 + 6), sign_text, font=sign_f, fill=NEON_CYAN + (255,))
# posts holding the sign to the roofs below (left hotel top 452, right hotel top 512)
sgd.line([(sx0 + 20, sy0 + 58), (sx0 + 20, 452)], fill=NEON_CYAN + (255,), width=3)
sgd.line([(sx0 + sw + 8, sy0 + 58), (sx0 + sw + 8, 512)], fill=NEON_CYAN + (255,), width=3)
img = Image.alpha_composite(img, sign_glow.filter(ImageFilter.GaussianBlur(6)))
img = Image.alpha_composite(img, sign_glow)
d = ImageDraw.Draw(img)

# vertical pink neon "VICE" on the first hotel
vice_f = font(26)
for i, ch in enumerate("VICE"):
    d.text((32, 512 + i * 30), ch, font=vice_f, fill=NEON_PINK,
           stroke_width=1, stroke_fill=(120, 10, 70))

# ---------------------------------------------------------------- ocean
v_gradient(d, HORIZON, SHORE, [
    (0.00, (64, 26, 96)),
    (0.50, (43, 22, 84)),
    (1.00, (26, 16, 62)),
])
# sun reflection: shimmering dashes under the sun
for i, y in enumerate(range(HORIZON + 6, SHORE - 4, 10)):
    t = (y - HORIZON) / (SHORE - HORIZON)
    half = 26 + 60 * t
    col = lerp((255, 170, 90), (255, 60, 130), t)
    for k in range(3):
        cx = sun_cx + (k - 1) * half * 0.8
        seg = half * (0.55 - 0.12 * k)
        d.line([(cx - seg, y), (cx + seg, y)], fill=col, width=3)
# faint horizon line
d.line([(0, HORIZON), (W, HORIZON)], fill=(255, 190, 120), width=2)

# ---------------------------------------------------------------- beach
v_gradient(d, SHORE, H, [
    (0.00, (232, 168, 124)),
    (0.55, (205, 128, 96)),
    (1.00, (168, 94, 80)),
])
# wet-sand shine line along the shore
d.line([(0, SHORE), (W, SHORE)], fill=(255, 214, 170), width=3)


# ---------------------------------------------------------------- palm silhouettes
PALM = (20, 10, 38)


def palm(base_x, base_y, top_x, top_y, lean, scale=1.0):
    # curved trunk as a tapered polygon
    pts_l, pts_r = [], []
    n = 24
    for i in range(n + 1):
        t = i / n
        x = base_x + (top_x - base_x) * t + lean * math.sin(t * math.pi) * 30
        y = base_y + (top_y - base_y) * t
        wdt = (14 - 8 * t) * scale
        pts_l.append((x - wdt, y))
        pts_r.append((x + wdt, y))
    d.polygon(pts_l + pts_r[::-1], fill=PALM)
    # fronds: curved tapered leaves
    tx, ty = top_x + lean * 0, top_y
    for ang in (-160, -125, -90, -55, -20, 15, 45):
        a = math.radians(ang)
        L = 150 * scale
        ex, ey = tx + L * math.cos(a), ty + L * math.sin(a) * 0.62 + 34 * scale
        mx, my = tx + L * 0.55 * math.cos(a), ty + L * 0.55 * math.sin(a) * 0.62 - 26 * scale
        leaf = []
        for i in range(13):
            t = i / 12
            bx = (1 - t) ** 2 * tx + 2 * (1 - t) * t * mx + t ** 2 * ex
            by = (1 - t) ** 2 * ty + 2 * (1 - t) * t * my + t ** 2 * ey
            wdt = 13 * scale * math.sin(t * math.pi)
            leaf.append((bx, by - wdt))
        for i in range(12, -1, -1):
            t = i / 12
            bx = (1 - t) ** 2 * tx + 2 * (1 - t) * t * mx + t ** 2 * ex
            by = (1 - t) ** 2 * ty + 2 * (1 - t) * t * my + t ** 2 * ey
            wdt = 13 * scale * math.sin(t * math.pi)
            leaf.append((bx, by + wdt))
        d.polygon(leaf, fill=PALM)
    d.ellipse([tx - 10 * scale, ty - 8 * scale, tx + 10 * scale, ty + 10 * scale], fill=PALM)


palm(48, 940, 96, 250, lean=1.0, scale=1.05)
palm(985, 930, 950, 215, lean=-0.8, scale=1.15)

# ---------------------------------------------------------------- deck chair + ghost
# ground shadow
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(shadow).ellipse([470, 820, 930, 880], fill=(40, 15, 30, 110))
img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(10)))
d = ImageDraw.Draw(img)

WOOD = (92, 48, 30)
WOOD_HI = (124, 66, 40)
# chair axis: front-low F to back-high B (side view, facing left)
F = (520, 845)
B = (880, 400)


def rail(p0, p1, wdt, col):
    d.line([p0, p1], fill=col, width=wdt)


# crossing legs (X frame)
rail((560, 858), (800, 620), 14, WOOD)
rail((860, 858), (620, 600), 14, WOOD)
rail((560, 858), (800, 620), 5, WOOD_HI)
# long frame rails the fabric hangs on
rail((F[0] - 14, F[1] + 6), (B[0] + 10, B[1] - 8), 13, WOOD)
rail((F[0] + 60, F[1] + 16), (B[0] + 74, B[1] + 4), 13, WOOD)

# striped sling fabric between the rails (cyan/white beach stripes)
fabric = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(fabric)
ax, ay = B[0] - F[0], B[1] - F[1]
ln = math.hypot(ax, ay)
ux, uy = ax / ln, ay / ln          # along the chair
px, py = -uy, ux                    # perpendicular
fw = 66                             # half-width of the sling
poly = [
    (F[0] + px * fw, F[1] + py * fw),
    (B[0] + px * fw, B[1] + py * fw),
    (B[0] - px * fw, B[1] - py * fw),
    (F[0] - px * fw, F[1] - py * fw),
]
fd.polygon(poly, fill=(240, 248, 255, 255))
# stripes across the sling
nstripes = 9
for i in range(nstripes):
    if i % 2 == 0:
        continue
    t0, t1 = i / nstripes, (i + 1) / nstripes
    q = [
        (F[0] + ax * t0 + px * fw, F[1] + ay * t0 + py * fw),
        (F[0] + ax * t1 + px * fw, F[1] + ay * t1 + py * fw),
        (F[0] + ax * t1 - px * fw, F[1] + ay * t1 - py * fw),
        (F[0] + ax * t0 - px * fw, F[1] + ay * t0 - py * fw),
    ]
    fd.polygon(q, fill=(0, 190, 220, 255))
img = Image.alpha_composite(img, fabric)
d = ImageDraw.Draw(img)

# warm rim glow so the mark sits in the scene light, not on top of it
rim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(rim).ellipse([440, 330, 940, 830], fill=(255, 140, 80, 70))
img = Image.alpha_composite(img, rim.filter(ImageFilter.GaussianBlur(40)))

# the official make.fun mark, lounging in the chair (large: ~450 px across)
mark = Image.open(MARK).convert("RGBA")
mark = mark.crop(mark.getchannel("A").getbbox())
MD = 450
mark = mark.resize((MD, MD), Image.LANCZOS)
mx, my = 690 - MD // 2, 575 - MD // 2
img = Image.alpha_composite(img, Image.new("RGBA", (W, H), (0, 0, 0, 0)))
img.paste(mark, (mx, my), mark)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- retro TV: GTA VI installing
tv_x0, tv_y0, tv_x1, tv_y1 = 100, 608, 420, 836
d.rounded_rectangle([tv_x0, tv_y0, tv_x1, tv_y1], radius=22, fill=(34, 22, 44),
                    outline=NEON_PINK, width=4)
# antenna
d.line([(200, tv_y0), (150, tv_y0 - 52)], fill=(34, 22, 44), width=6)
d.line([(280, tv_y0), (330, tv_y0 - 58)], fill=(34, 22, 44), width=6)
d.ellipse([144, tv_y0 - 60, 158, tv_y0 - 46], fill=NEON_PINK)
d.ellipse([324, tv_y0 - 66, 338, tv_y0 - 52], fill=NEON_CYAN)
# screen
scr = [tv_x0 + 22, tv_y0 + 22, tv_x1 - 66, tv_y1 - 46]
d.rounded_rectangle(scr, radius=12, fill=(12, 10, 40), outline=(90, 70, 140), width=3)
# screen content
gf = font(46)
gt = "GTA VI"
gw = d.textlength(gt, font=gf)
d.text(((scr[0] + scr[2]) / 2 - gw / 2, scr[1] + 12), gt, font=gf, fill=(255, 211, 25))
inf = font(24)
it = "INSTALLING... 99%"
iw = d.textlength(it, font=inf)
d.text(((scr[0] + scr[2]) / 2 - iw / 2, scr[1] + 76), it, font=inf, fill=(235, 235, 255))
# progress bar, nearly full
bx0, bx1 = scr[0] + 18, scr[2] - 18
by0 = scr[1] + 118
d.rounded_rectangle([bx0, by0, bx1, by0 + 20], radius=8, outline=(160, 160, 200), width=2)
d.rounded_rectangle([bx0 + 3, by0 + 3, bx0 + 3 + (bx1 - bx0 - 6) * 0.99, by0 + 17],
                    radius=6, fill=NEON_CYAN)
# knobs on the right panel
for ky in (tv_y0 + 46, tv_y0 + 96):
    d.ellipse([tv_x1 - 52, ky, tv_x1 - 24, ky + 28], fill=(70, 50, 90), outline=NEON_CYAN, width=2)
d.rectangle([tv_x1 - 50, tv_y0 + 140, tv_x1 - 26, tv_y0 + 176], fill=(70, 50, 90))
# little feet
d.rectangle([tv_x0 + 24, tv_y1, tv_x0 + 52, tv_y1 + 12], fill=(34, 22, 44))
d.rectangle([tv_x1 - 52, tv_y1, tv_x1 - 24, tv_y1 + 12], fill=(34, 22, 44))

# ---------------------------------------------------------------- captions
img = img.convert("RGB")
caption(img, "13 YEARS OF WAITING", 30, start=96)
caption(img, "MY make.fun AGENT GOT PAID", 876, start=68)
caption(img, "IN 13 MINUTES", 936, start=80)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size)
