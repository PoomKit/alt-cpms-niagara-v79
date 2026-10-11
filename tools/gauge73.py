"""Dial face for the kW/ton gauge (V7.3 item 9): dark face, ASHRAE colour bands, scale labels, band names.
The live needle / ticks are drawn by the kitPx:AnalogMeter widget laid exactly over this image (same square, same
startAngle 225 / arcAngle 270 / min 0.4 / max 1.4) - the widget's own scale labels are off (it prints integers only).
usage: python3 gauge73.py out.png size"""
import sys, math
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
BANDS = [(0.40, 0.75, (30, 132, 73)), (0.75, 0.90, (125, 206, 160)), (0.90, 1.00, (244, 208, 63)), (1.00, 1.40, (231, 76, 60))]
VMIN, VMAX, START, ARC = 0.4, 1.4, 225.0, 270.0


def ang(v):
    return START - (v - VMIN) / (VMAX - VMIN) * ARC       # degrees, math convention (CCW from +x), clockwise sweep


def face(path, S, ss=4):
    N = S * ss; R = N / 2; c = (R, R)
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(40):                                                    # bezel (metal gradient)
        r = R - k * ss * 0.12
        g = int(70 + 60 * math.cos(k / 40 * math.pi))
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=(g, g + 4, g + 10, 255))
    rf = R * 0.94
    for k in range(60):                                                    # face (radial dark gradient)
        r = rf * (1 - k / 60)
        v = int(14 + 16 * (k / 60))
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=(v, v + 5, v + 11, 255))
    r1, r2 = R * 0.90, R * 0.74                                            # colour band ring
    for lo, hi, col in BANDS:
        a0, a1 = ang(hi), ang(lo)                                          # PIL arcs: clockwise from +x, degrees, y down
        d.pieslice([c[0] - r1, c[1] - r1, c[0] + r1, c[1] + r1], -a1, -a0, fill=col + (255,))
    d.ellipse([c[0] - r2, c[1] - r2, c[0] + r2, c[1] + r2], fill=(22, 27, 34, 255))
    for k in range(30):                                                    # inner face gradient again
        r = r2 * (1 - k / 30)
        v = int(18 + 14 * (k / 30))
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=(v, v + 5, v + 11, 255))
    # gap at the bottom (outside the 270 deg sweep) -> face colour
    d.pieslice([c[0] - r1 - 2, c[1] - r1 - 2, c[0] + r1 + 2, c[1] + r1 + 2], 45, 135, fill=(26, 31, 38, 255))
    f = ImageFont.truetype(FONTB, int(S * 0.052) * ss)
    for i in range(11):
        v = VMIN + i * 0.1; a = math.radians(ang(v)); rr = R * 0.60
        x, y = c[0] + math.cos(a) * rr, c[1] - math.sin(a) * rr
        t = f'{v:.1f}'; w = d.textlength(t, font=f)
        d.text((x - w / 2, y - f.size * 0.6), t, font=f, fill=(205, 214, 222, 255))
    f2 = ImageFont.truetype(FONTB, int(S * 0.06) * ss)
    t = 'kW/RT'; w = d.textlength(t, font=f2); d.text((c[0] - w / 2, c[1] + R * 0.26), t, font=f2, fill=(143, 211, 255, 255))
    d.ellipse([c[0] - R * 0.07, c[1] - R * 0.07, c[0] + R * 0.07, c[1] + R * 0.07], fill=(60, 66, 74, 255), outline=(150, 160, 170, 255), width=ss * 2)
    im = im.resize((S, S), Image.LANCZOS)
    im.save(path)


if __name__ == '__main__':
    face(sys.argv[1], int(sys.argv[2]))
