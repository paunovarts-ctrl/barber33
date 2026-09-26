"""Barber 33 brand assets, built from the shop's own mark.

assets/logo-mark.png is the master: the logo keyed out of the supplied
artwork (whose transparency was a checkerboard baked into the pixels, not an
alpha channel) and stored white-on-transparent so it can be tinted to
anything. assets/logo.svg is the same shape traced to vector, and is what
the page itself uses.

Everything below is derived. Change a colour here and re-run rather than
re-exporting by hand:

    pip install Pillow && python3 tools/make-brand.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.join(HERE, '..')
ICONS  = os.path.join(ROOT, 'icons')
ASSETS = os.path.join(ROOT, 'assets')

# the same values as the CSS custom properties in index.html
INK   = (10, 11, 12)
GREEN = (18, 48, 42)
CREAM = (246, 242, 234)
BRASS = (200, 160, 70)

MASTER = Image.open(os.path.join(ASSETS, 'logo-mark.png'))   # white on transparent
SS = 4                                                       # supersample factor


def tinted(height, rgb):
    """The mark at a given height, in one flat colour, keeping its alpha."""
    w = round(MASTER.width * height / MASTER.height)
    a = MASTER.resize((w, height), Image.LANCZOS).getchannel('A')
    return Image.merge('RGBA', tuple(Image.new('L', a.size, c) for c in rgb) + (a,))


def icon(size, bleed=False, share=0.74):
    """One app icon: the mark, centred, on the shop's green.

    bleed fills the whole square, because iOS applies its own corner mask and a
    rounded icon inside that mask reads as a shrunken sticker.
    """
    W = size * SS
    img = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if bleed:
        d.rectangle([0, 0, W, W], fill=GREEN + (255,))
    else:
        d.rounded_rectangle([0, 0, W - 1, W - 1], radius=int(W * 0.215), fill=GREEN + (255,))

    mark = tinted(int(W * share), CREAM)
    img.paste(mark, ((W - mark.width) // 2, (W - mark.height) // 2), mark)
    return img.resize((size, size), Image.LANCZOS)


for name, size, kw in [('icon-512.png', 512, {}),
                       ('icon-192.png', 192, {}),
                       ('apple-touch-icon.png', 180, dict(bleed=True)),
                       # the scissor tails vanish below about 48px, so the
                       # small sizes give the mark more of the square
                       ('favicon-32.png', 32, dict(share=0.86)),
                       ('favicon-16.png', 16, dict(share=0.92))]:
    icon(size, **kw).save(os.path.join(ICONS, name), optimize=True)
    print('wrote icons/' + name)


# ---- share card -------------------------------------------------------------
# What WhatsApp, Messenger and Facebook show when someone sends the shop to a
# friend. For a walk-in barbershop that link IS the marketing, so it carries
# the name, the town and the one thing that matters: no appointment needed.
W, H = 1200, 630

# A warm off-centre glow, computed small and scaled up: concentric ellipses
# left visible rings, this ramps smoothly for nothing.
gw, gh = 60, 32
grad = Image.new('RGB', (gw, gh))
gp = grad.load()
for gy in range(gh):
    for gx in range(gw):
        dx, dy = (gx - gw * 0.68) / (gw * 0.60), (gy - gh * 0.46) / (gh * 0.86)
        f = max(0.0, 1.0 - (dx * dx + dy * dy)) ** 1.6
        gp[gx, gy] = (int(INK[0] + 26 * f), int(INK[1] + 40 * f), int(INK[2] + 34 * f))
card = grad.resize((W, H), Image.BICUBIC)
cd = ImageDraw.Draw(card)

mark = tinted(430, CREAM)
card.paste(mark, (846, (H - mark.height) // 2), mark)

B = lambda p: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', p)
R = lambda p: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', p)

X = 96
cd.rectangle([X, 172, X + 84, 179], fill=(192, 57, 46))
cd.text((X, 300), 'BARBER', font=B(108), fill=CREAM, anchor='ls')
# "33" and the town share a baseline; the town is placed off the measured
# width of the numerals so the two can never collide.
f33 = B(108)
cd.text((X, 424), '33', font=f33, fill=BRASS, anchor='ls')
cd.text((X + cd.textlength('33', font=f33) + 34, 424), 'POREČ',
        font=B(44), fill=CREAM, anchor='ls')
cd.text((X, 505), 'Walk-in barbershop, bez naručivanja',
        font=R(34), fill=(163, 155, 145), anchor='ls')

card.save(os.path.join(ASSETS, 'share-card.jpg'),
          quality=88, optimize=True, progressive=True)
print('wrote assets/share-card.jpg')
