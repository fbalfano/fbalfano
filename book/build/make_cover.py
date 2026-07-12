#!/usr/bin/env python3
"""Build a KDP print-ready wraparound cover for 6x9, 196 pages, white paper.
If cover/author-photo.jpg exists it is placed in the About-the-Author block."""
import os
from PIL import Image, ImageDraw, ImageFont

DPI = 300
BLEED = 0.125
TRIM_W, TRIM_H = 6.0, 9.0
PAGES = 196
SPINE_IN = PAGES * 0.002252           # white paper
W_IN = 2*BLEED + 2*TRIM_W + SPINE_IN
H_IN = 2*BLEED + TRIM_H
W, H = round(W_IN*DPI), round(H_IN*DPI)

BG = (10, 12, 18)
WHITE = (232, 232, 230)
RED = (186, 48, 38)
GREY = (155, 163, 175)
RULE = (90, 30, 26)

FS  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FNB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def f(path, pts): return ImageFont.truetype(path, pts)

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

# ---- FRONT COVER (right) ----
front = Image.open("cover/how-not-to-get-away-with-murder-cover.jpg").convert("RGB")
fw, fh = round(TRIM_W*DPI), round(TRIM_H*DPI)
front = front.resize((fw, fh), Image.LANCZOS)
front_x = round((2*BLEED + TRIM_W + SPINE_IN)*DPI)
canvas.paste(front, (front_x, round(BLEED*DPI)))

# ---- SPINE ----
spine_px = round(SPINE_IN*DPI)
spine_left = round((BLEED + TRIM_W)*DPI)
spine_cx = spine_left + spine_px//2
strip = Image.new("RGB", (2300, spine_px), BG)
sd = ImageDraw.Draw(strip)
sd.text((60, spine_px/2), "HOW NOT TO GET AWAY WITH MURDER", font=f(FNB, 44), fill=WHITE, anchor="lm")
sd.text((2300-60, spine_px/2), "FRANK ALFANO", font=f(FNB, 40), fill=GREY, anchor="rm")
strip = strip.rotate(270, expand=True)
canvas.paste(strip, (spine_cx - strip.width//2, (H - strip.height)//2))

# ---- BACK COVER (left) ----
x0 = round((BLEED + 0.45)*DPI)
maxw = round(TRIM_W*DPI) - round(0.9*DPI)
y = round((BLEED + 0.42)*DPI)

def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

# Tagline
tag_font = f(FSB, 58)
draw.text((x0, y), "The smoking gun is rarely a gun.", font=tag_font, fill=RED); y += 96

body = f(FS, 40); LH = 56
for p in [
 "Almost no one is caught the way the movies promise. What catches a killer, nearly every time, is smaller and quieter: the one thing he forgot he left behind.",
 "Forty-three true cases from Canadian and American courts, each undone by a single thread of evidence, and each anchored to a real court decision you can look up yourself.",
]:
    for ln in wrap(p, body, maxw):
        draw.text((x0, y), ln, font=body, fill=WHITE); y += LH
    y += 22

# "Inside" bullets
head = f(FSB, 42)
draw.text((x0, y), "Inside you'll meet:", font=head, fill=WHITE); y += 66
bullet_font = f(FS, 38); BLH = 52
for b in [
 "The man who handed police the hairs that convicted him, because they asked nicely",
 "A wife reported dead, contradicted by the Fitbit on her own wrist",
 "A phone that photographed the inside of a pocket on the way to a murder",
 "A bullet that cleared the man everyone saw firing, and found the shooter no one was watching",
 "The stagers, the stings, the junk science, and the innocent it took decades to free",
]:
    lines = wrap(b, bullet_font, maxw - 70)
    draw.text((x0+8, y), "•", font=bullet_font, fill=RED)
    for i, ln in enumerate(lines):
        draw.text((x0+70, y), ln, font=bullet_font, fill=WHITE); y += BLH
    y += 8
y += 14

close = f(FSB, 46)
draw.text((x0, y), "Every case is real. ", font=close, fill=WHITE)
wpx = draw.textlength("Every case is real. ", font=close)
draw.text((x0+wpx, y), "Everything remembers now.", font=close, fill=RED)
y += 88

# ---- About the author block (bottom-left; barcode zone stays clear bottom-right) ----
rule_y = y
draw.line([(x0, rule_y), (x0+maxw, rule_y)], fill=RULE, width=4); y += 40

photo_path = "cover/author-photo.jpg"
bio_x = x0
bio_w = maxw
PH = round(1.55*DPI)  # photo height ~1.55in
if os.path.exists(photo_path):
    ph = Image.open(photo_path).convert("RGB")
    ratio = PH / ph.height
    pw = round(ph.width * ratio)
    ph = ph.resize((pw, PH), Image.LANCZOS)
    canvas.paste(ph, (x0, y))
    bio_x = x0 + pw + 46
    bio_w = maxw - pw - 46

bio_head = f(FNB, 38)
draw.text((bio_x, y+6), "FRANK ALFANO, LL.B., LL.M.", font=bio_head, fill=WHITE)
by = y + 66
bio_font = f(FS, 34); BIOLH = 47
bio = ("Frank Alfano writes about the law the way it actually works: on the record, "
       "one case at a time. He built this book the way a lawyer builds a case, every "
       "chapter anchored to a court decision you can verify yourself.")
# keep bio text clear of the barcode zone (bottom-right ~2.4in x 1.4in)
barcode_top = H - round((BLEED + 1.45)*DPI)
for ln in wrap(bio, bio_font, bio_w):
    draw.text((bio_x, by), ln, font=bio_font, fill=GREY); by += BIOLH
draw.text((bio_x, by+10), "frankalfano.ca", font=f(FNB, 34), fill=RED)

canvas.save("build/cover-wrap-6x9-196pp-WHITE.pdf", "PDF", resolution=DPI)
prev = canvas.copy(); prev.thumbnail((1200, 1200))
prev.save("build/cover-wrap-thumb.png", "PNG")
print(f"{W}x{H}px = {W/DPI:.3f} x {H/DPI:.3f} in | spine {SPINE_IN:.3f} in | photo: {os.path.exists(photo_path)}")
