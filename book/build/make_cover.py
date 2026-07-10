#!/usr/bin/env python3
"""Build a KDP print-ready wraparound cover for 6x9, 196 pages, white paper."""
from PIL import Image, ImageDraw, ImageFont

DPI = 300
BLEED = 0.125
TRIM_W, TRIM_H = 6.0, 9.0
PAGES = 196
SPINE_IN = PAGES * 0.002252           # white paper
W_IN = 2*BLEED + 2*TRIM_W + SPINE_IN  # 12.6914
H_IN = 2*BLEED + TRIM_H               # 9.25
W, H = round(W_IN*DPI), round(H_IN*DPI)

BG = (10, 12, 18)
WHITE = (232, 232, 230)
RED = (176, 40, 31)
GREY = (150, 158, 170)

FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FNB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def f(path, pts): return ImageFont.truetype(path, pts)

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

# ---- FRONT COVER (right), placed at trim; bleed filled by dark bg ----
front = Image.open("cover/how-not-to-get-away-with-murder-cover.jpg").convert("RGB")
fw, fh = round(TRIM_W*DPI), round(TRIM_H*DPI)          # 1800 x 2700
front = front.resize((fw, fh), Image.LANCZOS)
front_x = round((2*BLEED + TRIM_W + SPINE_IN)*DPI)     # spine right edge
front_y = round(BLEED*DPI)
canvas.paste(front, (front_x, front_y))

# ---- SPINE (center) ----
spine_px = round(SPINE_IN*DPI)
spine_left = round((BLEED + TRIM_W)*DPI)
spine_cx = spine_left + spine_px//2
strip = Image.new("RGB", (2300, spine_px), BG)
sd = ImageDraw.Draw(strip)
spine_font = f(FNB, 44)
auth_font = f(FNB, 40)
title = "HOW NOT TO GET AWAY WITH MURDER"
author = "FRANK ALFANO"
tb = sd.textbbox((0,0), title, font=spine_font)
ab = sd.textbbox((0,0), author, font=auth_font)
sd.text((60, spine_px/2), title, font=spine_font, fill=WHITE, anchor="lm")
sd.text((2300-60, spine_px/2), author, font=auth_font, fill=GREY, anchor="rm")
strip = strip.rotate(270, expand=True)
canvas.paste(strip, (spine_cx - strip.width//2, (H - strip.height)//2))

# ---- BACK COVER (left) ----
back_left = round(BLEED*DPI)
mx = back_left + round(0.5*DPI)                 # inside margin
maxw = round(TRIM_W*DPI) - round(1.0*DPI)       # usable text width
x0 = mx
y = round((BLEED + 0.55)*DPI)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

# Tagline
tag_font = f(FSB, 50)
for ln in wrap("The smoking gun is rarely a gun.", tag_font, maxw):
    draw.text((x0, y), ln, font=tag_font, fill=RED); y += 66
y += 34

body_font = f(FS, 39)
paras = [
 "Almost no one is caught the way the movies promise. What catches a killer, nearly every time, is smaller and quieter: the one thing he forgot he left behind.",
 "A cell tower that puts a phone on a lonely road. A Fitbit still counting a woman's steps after her husband swears she was already dead. A search for “what happens when you die,” typed minutes after a murder.",
 "Forty-three true cases from Canadian and American courts, each undone by a single thread of evidence, and each anchored to a real court decision you can look up yourself.",
]
for p in paras:
    for ln in wrap(p, body_font, maxw):
        draw.text((x0, y), ln, font=body_font, fill=WHITE); y += 54
    y += 26

y += 10
close_font = f(FSB, 44)
draw.text((x0, y), "Every case is real.", font=close_font, fill=WHITE); y += 60
draw.text((x0, y), "Everything remembers now.", font=close_font, fill=RED)

# (Bottom-right of back cover left clear for the KDP barcode.)

canvas.save("build/cover-wrap-6x9-196pp-WHITE.pdf", "PDF", resolution=DPI)
canvas.save("build/cover-wrap-preview.png", "PNG")
prev = canvas.copy(); prev.thumbnail((1100, 1100))
prev.save("build/cover-wrap-thumb.png", "PNG")
print(f"Canvas {W}x{H}px = {W/DPI:.3f} x {H/DPI:.3f} in  |  spine {SPINE_IN:.3f} in ({spine_px}px)")
