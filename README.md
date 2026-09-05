# sylvesterlimited.tech

The Sylvester Limited company site. One static page, no build step, no framework.

```
index.html    the whole site — markup, styles, and both scripts
og.png        1200x630 link-preview card
make_og.py    regenerates og.png (python3 make_og.py, needs Pillow)
favicon.svg   faceted shard mark
robots.txt    / sitemap.xml
```

## How the page is put together

The page is a single descent. A fixed WebGL stage sits behind the document
and the camera moves down it as you scroll. Every crystal in the scene is
anchored to an element in the markup (`data-shard="…"`): at layout time the
script reads where that element sits in the document and places the crystal
at the matching depth, so the scene and the copy cannot drift apart. Resize,
font load and the reveal animations all trigger a re-measure.

There are two scripts, on purpose:

- **Baseline** (`<script>` near the end of the body) — loader, clock, reveals,
  text scramble, tallies, section rail, cursor, ambient sound, footer particle
  field. No dependencies. If everything else fails, this still runs.
- **The Void** (`<script type="module">`) — the three.js scene. It loads from
  a CDN via an import map, reports progress into the loader, and on any error
  flags `no-webgl` on `<html>` and steps aside. The CSS `.ambient` layer takes
  over as a flat background.

Everything else is progressive enhancement: the copy renders and reads
without JavaScript, `prefers-reduced-motion` stops every autonomous
animation, and sound is off until a visitor asks for it.

## Editing

Open `index.html` and edit it. There is nothing to compile. Pushing to `main`
deploys to production automatically via Vercel.

To preview locally, serve the folder (`python3 -m http.server`) rather than
opening the file directly — the module import map needs an origin.

If you change the headline or the project list, regenerate the link-preview
card so the two agree:

```sh
python3 make_og.py
```

`make_og.py` looks for Space Grotesk / JetBrains Mono on the machine and
falls back to whatever grotesk and mono it can find, so it runs on macOS and
Linux alike.

### Adding a project

Copy one of the `<article class="entry">` blocks in `#work`. Alternate
`class="entry"` and `class="entry flip"` so the empty column alternates
sides. Give its `.void-slot` a new `data-shard` key and add a matching row
to `PLAN` in the module script — a seed, a cell count, a scale, and which
side (`x`) it should sit on. Same seed, same crystal, every load.

## House rule

Every claim on the page links to something a reader can open — a live product
or a public repository. If a new claim can't be linked, it doesn't go on the
page.

## Colour

Tokens are defined once at the top of `index.html`. The accent
`hsl(270 80% 65%)` is carried over from the original site; the ground moved
from `hsl(252 20% 6%)` to a matte `#05050a` so refracted light off the
crystals is the only real colour on the page, and an ice tone
`hsl(196 92% 74%)` was added for the chromatic split they throw.
