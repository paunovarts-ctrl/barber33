# Barber 33

Public site for **Barber 33**, a walk-in barbershop in Poreč, Croatia.

One file, no build step, no framework. `index.html` is the whole site.

Because the shop takes no bookings, the page is built around the three things
someone standing in the street actually wants: whether the door is open, what
a cut costs, and which way to walk.

## Before it goes live

The phone, the address and the opening hours are in. What is left:

1. **The Instagram handle**, in the `SHOP` object at the foot of
   `index.html`. It is the only empty field; while it stays empty the site
   drops that row rather than linking somewhere wrong.
2. **Sunday.** The hours came from a listing that was cut off after
   Saturday, so Sunday is set closed on an assumption and nothing else.
3. **The prices and durations** in the Cjenik section, which are still the
   plausible-guess ones.
4. **The quiet-times note** beside the hours, and *Hrvatski i engleski* in
   the Što radimo cards. Both are claims about the shop that the shop has
   not confirmed.

`SHOP` is the only place the phone and address are written; every call
button, every maps link and the contact block read from it. The JSON-LD
block in `<head>` carries the same facts for Google's local results, so
keep the two in step.

The phone is stored international (`+385 52 829 587`) rather than as the
local `052 829 587`. Both dial from a Croatian phone, but only the
international form dials from the German or Italian handset half of Poreč
is holding in August.

## Photos

- `assets/hero-*.jpg` is the room, one photograph at three widths.
- `assets/work-*.jpg` are the four cuts in the gallery, each at two widths,
  cropped to a uniform 3:4 so the row is never ragged.

To swap any of them, drop the new picture in and re-run the resizer used to
make them (three widths for the hero, two for a gallery tile). Keep the
gallery at 3:4.

## The logo

`assets/logo.svg` is the shop's mark, top hat, spectacles and scissor-blade
moustache, traced to vector. The page defines it once as an inline
`<symbol>` and uses it twice, in the header and on the loading screen.

It is inline rather than an `<img>` on purpose: an SVG loaded through `<img>`
is an isolated document that cannot see this page's CSS, so `currentColor`
would resolve to black instead of the cream those two places want. Inlined,
the mark takes its colour from whatever it sits in.

`assets/logo-mark.png` is the same shape as a white-on-transparent bitmap,
and is the master the icons are built from. It exists because the supplied
artwork had no alpha channel: its "transparency" was a checkerboard baked
into the pixels, so the mark was keyed out by luminance, which the
histogram made unambiguous.

## The rule grid

The page is held together by hairlines rather than by boxes, the way Wine
Corner is. Two rules run its full height at the container's edges, carried by
the header, the hero, every section, the ticker and the footer, so they are
one unbroken pair rather than a motif repeated per block. A third crosses the
top of each section, and a fourth sits under each section heading. What used
to be cards are now cells of that grid: no fill, no border, no corner radius,
just the rules between them.

Two things make it hold:

- **`--gut`** is the single gutter. The container's rules sit at its outer
  edge and every ruled row pulls back out by exactly that much, so a divider
  always lands *on* a container rule instead of near it. Change the one value
  and the grid stays square.
- **`--rule` is redefined per field.** The same hairline cannot serve a
  near-black section, the green band and the bright ticker, so each sets its
  own and everything inside inherits it.

Below the phone breakpoint the side rules go entirely and the dividers turn
from vertical to horizontal. Drawn hard against a phone's screen edge they
read as a border around the page rather than as a grid holding it together.

## How it behaves

- **Croatian is the page**, English lives in `data-en` attributes beside it.
  A phone not set to Croatian gets English on its first visit, and whatever
  anyone picks with the EN/HR button wins from then on.
- **The open/closed badge** reads the hours table and Poreč's clock, not the
  visitor's, because in August a good share of the people reading this are on a
  phone still set to Munich. Closed is never just "closed": it says when the
  door opens again.
- **The call bar** on a phone keeps the number and the directions within
  thumb reach the whole way down the page.
- **The loading screen** covers the moment before the hero photograph has
  decoded, and lifts as soon as it is ready. A failsafe timer lifts it
  regardless, and `<noscript>` removes it entirely, so a slow photograph can
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

Static, with nothing to build. Vercel serves the repository root as-is;
`vercel.json` only sets cache and security headers.
