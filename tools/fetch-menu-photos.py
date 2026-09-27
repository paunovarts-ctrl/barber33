#!/usr/bin/env python3
"""Download the eight menu photographs, fit them to the cells, and switch the
cards on.

    pip install Pillow && python3 tools/fetch-menu-photos.py

Idempotent: it re-downloads only what is missing from tools/.menu-cache/ and
only uncomments a card once. Pass file paths instead of URLs by dropping the
files into that cache directory named <slug>.png or <slug>.jpg first.

The URLs below are OpenArt CDN links for one account's generations. If they
have expired, regenerate and replace them; everything downstream is unchanged.
"""
import pathlib, re, subprocess, sys
from PIL import Image

URLS = {
 "sisanje":        "https://cdn.openart.ai/openart-ai/production/2026-09/create-image/McR5lRTZfGEldEHAz3c7/image_1790540216557_6a450607_1790540217321_31116aa2.png",
 "sisanje-pranje": "https://cdn.openart.ai/openart-ai/production/2026-09/create-image/McR5lRTZfGEldEHAz3c7/image_1790540216188_630f7db4_1790540217177_40732be3.png",
 "fade":           "https://cdn.openart.ai/openart-ai/production/2026-09/create-image/McR5lRTZfGEldEHAz3c7/image_1790540218000_bc52dd82_1790540218678_27c83934.png",
 "sisanje-brada":  "https://cdn.openart.ai/openart-ai/production/2026-09/create-image/McR5lRTZfGEldEHAz3c7/image_1790540219475_8956add1_1790540219917_696234ac.png",
 "brada":          "https://cdn.openart.ai/openart-ai/production/2026-09/create-image/McR5lRTZfGEldEHAz3c7/image_1790540266477_fcd2bed6_1790540266902_6a242a08.png",
 "britva":         "https://cdn.openart.ai/openart-ai/production/2026-09/create-image/McR5lRTZfGEldEHAz3c7/image_1790540269438_c726f3a0_1790540269969_5f6e287b.png",
 "glava":          "https://cdn.openart.ai/openart-ai/production/2026-09/create-image/McR5lRTZfGEldEHAz3c7/image_1790540270593_6559f80e_1790540271228_b300b692.png",
 "djecje":         "https://cdn.openart.ai/openart-ai/production/2026-09/create-image/McR5lRTZfGEldEHAz3c7/image_1790540272007_39d59f2d_1790540272658_d0d5dd79.png",
}

ROOT  = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT/"tools"/".menu-cache"
OUT   = ROOT/"assets"
W, H  = 1200, 800                       # 3:2, ample for the widest cell at 2x


def trim_frame(im, thresh=238, frac=.94):
    """Drop edge rows and columns that are almost entirely near-white.

    The generator sometimes reads "photography" as a physical print and mats
    the picture in white. The test is on a whole row rather than one sample
    because a white towel or a lathered face fills the middle of a row without
    filling the row, and a centre sample calls that a border and eats a sixth
    of the photograph.
    """
    g = im.convert("L"); w, h = g.size; px = g.load()
    xs, ys = range(0, w, 4), range(0, h, 4)
    row = lambda y: sum(px[x, y] >= thresh for x in xs)/len(xs) >= frac
    col = lambda x: sum(px[x, y] >= thresh for y in ys)/len(ys) >= frac
    t = 0
    while t < h//3 and row(t): t += 1
    b = h-1
    while b > 2*h//3 and row(b): b -= 1
    l = 0
    while l < w//3 and col(l): l += 1
    r = w-1
    while r > 2*w//3 and col(r): r -= 1
    return im.crop((l, t, r+1, b+1)), (t, h-1-b, l, w-1-r)


def to_three_two(im):
    tw, th = im.width, round(im.width*H/W)
    if th > im.height:
        th, tw = im.height, round(im.height*W/H)
    x, y = (im.width-tw)//2, (im.height-th)//2
    return im.crop((x, y, x+tw, y+th)).resize((W, H), Image.LANCZOS)


def local(slug):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = CACHE/(slug+ext)
        if p.exists() and p.stat().st_size > 10_000: return p
    return None


def main():
    CACHE.mkdir(parents=True, exist_ok=True)
    missing = []
    for slug, url in URLS.items():
        src = local(slug)
        if src is None:
            dst = CACHE/(slug+".png")
            subprocess.run(["curl", "-sSfL", "--max-time", "120", "-o", str(dst), url])
            src = local(slug)
            if src is None:
                dst.unlink(missing_ok=True); missing.append(slug); continue
        im, insets = trim_frame(Image.open(src).convert("RGB"))
        if any(insets):
            print("  %-14s trimmed print border T%d B%d L%d R%d" % (slug, *insets))
        to_three_two(im).save(OUT/("menu-%s.jpg" % slug), "JPEG",
                              quality=82, optimize=True, progressive=True)
        print("  wrote assets/menu-%s.jpg" % slug)

    if missing:
        sys.exit("\ncould not fetch: %s\n"
                 "Is cdn.openart.ai reachable? Otherwise drop the files into\n"
                 "%s as <slug>.png and run this again." % (", ".join(missing), CACHE))

    html = ROOT/"index.html"; s = html.read_text(); n = 0
    for slug in URLS:
        # (?!-->) at every step keeps the match inside ONE comment. A plain
        # lazy .*? under DOTALL spans from the first card's comment to this
        # card's <img> and deletes every card in between.
        pat = re.compile(r'<!-- PHOTO:(?:(?!-->)[\s\S])*?'
                         r'(<img src="assets/menu-%s\.jpg"(?:(?!-->)[\s\S])*?>)'
                         r'\s*-->' % re.escape(slug))
        s, k = pat.subn(lambda m: m.group(1), s); n += k
    html.write_text(s)
    print("\nswitched on %d of %d cards (already-live cards count 0)" % (n, len(URLS)))


if __name__ == "__main__":
    main()
