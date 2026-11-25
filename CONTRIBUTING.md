# Contributing to the site

This repository is the only place the pages live. The project repositories
(`Hy2droid`, `amneziawg-ui`, `imail`, `flownotes`) no longer serve Pages sites of their
own; their former URLs are served from this repository:

- `/Hy2droid/`
- `/amneziawg-ui/`
- `/imail/`
- `/flownotes/`

Do not copy a project site back into its own repository. A page change is a pull
request here.

## Before opening a pull request

```sh
python3 scripts/check-links.py          # local href/src references
python3 scripts/gen-sitemap.py --check  # sitemap matches the files
python3 scripts/check-contrast.py       # colour roles meet WCAG AA
python3 -m py_compile scripts/*.py
shfmt -i 2 -d scripts/*.sh && shellcheck scripts/*.sh
```

## Design system

All five sites share `docs/m3.css`: Material 3 roles for colour, shape, motion
and type, plus the top-bar controls (`.theme-toggle`, `.nav .lang`), the button
components and `.visually-hidden`. Each page links it before its own
`style.css` and seeds the colour roles there, once for light and once for dark.
Page CSS is unlayered and therefore wins over the shared layers; components are
unlayered so that a page's `a { color: … }` cannot repaint a filled button.

The token list is kept to what a component actually reads: shape steps, motion
durations and easings, type sizes, and the colour roles `primary`,
`on-primary`, `surface`, `surface-container-low` / `-container` /
`-high`, `on-surface`, `on-surface-variant`, `outline`, `outline-variant`
(plus `tertiary` where a page uses it). Add a role only together with the
component that consumes it — an unused token is dead code like any other.

When changing a page's look, keep the rule of one system and five looks: pick
shape steps from the shared scale instead of writing a new radius, use the
8% hover / 12% pressed state convention, and keep at most one element that is
unmistakably that page's own (iMail's postage stamp and offset shadows,
Hy2droid's hairline readouts, the AmneziaWG browser frame, Flow Notes’ editor sheet). Then run
`check-contrast.py`, which reads the seeds straight out of each `style.css` and
fails on a pair below 4.5:1 for text or 3:1 for a control edge.

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
state job asserts that the four project repositories still have Pages disabled
(otherwise they would shadow the central copies).

The 404 page (`docs/404.html`) lists the four project sites for old links that
no longer resolve.
