# Barber 33

Public site for **Barber 33**, a walk-in barbershop in Poreč, Croatia.

One file, no build step, no framework — `index.html` is the whole site.

Because the shop takes no bookings, the page is built around the three things
someone standing in the street actually wants: whether the door is open, what
a cut costs, and which way to walk.

## Before it goes live

Two places hold everything the shop still has to confirm. Both are marked
`FILL` in `index.html`:

1. **`SHOP`**, at the top of the script at the bottom of the file — phone,
   street address, Instagram handle. Every call button, every maps link and
   the contact block read from here, so it is the only place to type them.
   A field left empty is handled rather than faked: the call buttons
   disappear instead of offering a dead link, and the contact row keeps
   saying *upiši broj* so nobody ships the site without noticing.
2. **The JSON-LD block** in `<head>` — the same address and phone again, this
   time for Google's local results. Keep it in step with `SHOP`.

Worth a second pair of eyes from the shop as well:

- the prices and durations in the **Cjenik** section
- the **opening hours table** — the open/closed badge at the top of the page
  is computed from its `data-open` / `data-close` attributes, so an hour
  wrong there is wrong in two places
- the quiet-times note beside the hours
- *Hrvatski i engleski* in the **Što radimo** cards

## Photos

- `assets/hero-*.jpg` — the room, one photograph at three widths.
- `assets/work-*.jpg` — the four cuts in the gallery, each at two widths,
  cropped to a uniform 3:4 so the row is never ragged.

To swap any of them, drop the new picture in and re-run the resizer used to
make them (three widths for the hero, two for a gallery tile). Keep the
gallery at 3:4.

## The logo

`assets/logo.svg` is the shop's mark — top hat, spectacles, scissor-blade
moustache — traced to vector. The page defines it once as an inline
`<symbol>` and uses it twice, in the header and on the loading screen.

It is inline rather than an `<img>` on purpose: an SVG loaded through `<img>`
is an isolated document that cannot see this page's CSS, so `currentColor`
would resolve to black instead of the cream those two places want. Inlined,
the mark takes its colour from whatever it sits in.

`assets/logo-mark.png` is the same shape as a white-on-transparent bitmap,
and is the master the icons are built from. It exists because the supplied
artwork had no alpha channel — its "transparency" was a checkerboard baked
into the pixels — so the mark was keyed out by luminance, which the
histogram made unambiguous.

## How it behaves

- **Croatian is the page**, English lives in `data-en` attributes beside it.
  A phone not set to Croatian gets English on its first visit, and whatever
  anyone picks with the EN/HR button wins from then on.
- **The open/closed badge** reads the hours table and Poreč's clock, not the
  visitor's — in August a good share of the people reading this are on a
  phone still set to Munich. Closed is never just "closed": it says when the
  door opens again.
- **The call bar** on a phone keeps the number and the directions within
  thumb reach the whole way down the page.
- **The loading screen** covers the moment before the hero photograph has
  decoded, and lifts as soon as it is ready. A failsafe timer lifts it
  regardless, and `<noscript>` removes it entirely — a slow photograph can
  never leave anyone looking at a covered page.
- **Motion** is gated: every animation stops under
  `prefers-reduced-motion`, every hover effect is behind `(hover: hover)`,
  and the translucent chrome turns solid under
  `prefers-reduced-transparency`.

## Running it locally

```bash
python3 -m http.server 8146
```

Then <http://localhost:8146/>.

## Assets

`icons/` and `assets/share-card.jpg` are generated, not drawn by hand. They
are built from `assets/logo-mark.png` by `tools/make-brand.py`, so a colour
change is a re-run rather than a redraw:

```bash
pip install Pillow && python3 tools/make-brand.py
```

The palette constants at the top of that script are the same values as the
CSS custom properties in `index.html`; change both together.

## Deploying

Static — there is nothing to build. Vercel serves the repository root as-is;
`vercel.json` only sets cache and security headers.
