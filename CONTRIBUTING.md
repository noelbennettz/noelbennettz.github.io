# Contributing to the site

This repository is the only place the pages live. The project repositories
(`Hy2droid`, `amneziawg-ui`, `imail`) no longer have a `docs/` directory or a
Pages workflow; their former URLs are served from this repository:

- `/Hy2droid/`
- `/amneziawg-ui/`
- `/imail/`

Do not copy a project site back into its own repository. A page change is a pull
request here.

## Before opening a pull request

```sh
python3 scripts/check-links.py          # local href/src references
python3 scripts/gen-sitemap.py --check  # sitemap matches the files
python3 scripts/check-contrast.py       # colour roles meet WCAG AA
```

## Design system

All four sites share `docs/m3.css`: Material 3 roles for colour, shape, state
layers, motion and type, plus the top-bar control and the button components.
Each page links it before its own `style.css` and seeds the colour roles there,
once for light and once for dark. Page CSS is unlayered and therefore wins over
the shared layers; components are unlayered so that a page's `a { color: … }`
cannot repaint a filled button.

When changing a page's look, keep the rule of one system and four looks: pick
shape steps from the shared scale instead of writing a new radius, use the
shared state-layer opacities, and keep at most one element that is unmistakably
that page's own (iMail's postage stamp and offset shadows, Hy2droid's hairline
readouts, the AmneziaWG browser frame). Then run `check-contrast.py`, which
reads the seeds straight out of each `style.css` and fails on a pair below
4.5:1 for text or 3:1 for a control edge.

`docs/theme.js` boots `data-theme` before the first paint and drives every
`.theme-toggle`; the `theme` key in localStorage is shared by all four sites,
so switching on one page switches the rest.

If a page is added, run `python3 scripts/gen-sitemap.py` and commit the updated
`docs/sitemap.xml`. Every page has an English and a Traditional Chinese version
(`index.html` and `zh.html`, or the project equivalent), and each links to the
other.

`pages.yml` deploys a copy of `docs/` with CSS/JS references stamped with the
commit SHA, so a stylesheet change cannot hide behind the GitHub Pages cache.
`checks.yml` runs the link and sitemap checks on every pull request; the Pages
state job asserts that the three project repositories still have Pages disabled
(otherwise they would shadow the central copies).

The 404 page (`docs/404.html`) lists the three project sites for old links that
no longer resolve.
