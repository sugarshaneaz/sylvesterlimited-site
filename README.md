# sylvesterlimited.tech

The Sylvester Limited company site. One static page, no build step, no framework.

```
index.html    the whole site
og.png        1200x630 link-preview card
make_og.py    regenerates og.png (python3 make_og.py)
favicon.svg   wordmark
```

## Editing

Open `index.html` and edit it. There is nothing to compile. Pushing to `main`
deploys to production automatically via Vercel.

If you change the headline or the project list, regenerate the link-preview
card so the two agree:

```sh
python3 make_og.py
```

## House rule

Every claim on the page links to something a reader can open — a live product
or a public repository. If a new claim can't be linked, it doesn't go on the
page.

Colours are the original site's tokens, defined once at the top of
`index.html`: ground `hsl(252 20% 6%)`, accent `hsl(270 80% 65%)`.
