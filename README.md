# noelbennettz.github.io

Source of <https://noelbennettz.github.io/>, an index of the open-source
projects and their sites:

- [Hy2droid](https://noelbennettz.github.io/Hy2droid/) — Hysteria 2 for Android
- [AmneziaWG Web UI](https://noelbennettz.github.io/amneziawg-ui/) — self-hosted Docker panel
- [iMail](https://noelbennettz.github.io/imail/) — mail for your own domains
- [Flow Notes](https://noelbennettz.github.io/flownotes/) — self-hosted Markdown notes

Every page is here: the index at `docs/`, and the four project sites under
`docs/Hy2droid/`, `docs/amneziawg-ui/`, `docs/imail/` and `docs/flownotes/`, each served at the
`https://noelbennettz.github.io/<project>/` path above. The project
repositories no longer carry a `docs/` directory of their own — this repository
is the only place the pages live, so a change to a project page is a change
here.

The site is plain HTML/CSS — English and Traditional Chinese, each page linking
to the other — with no build step, deployed to GitHub Pages by
`.github/workflows/pages.yml`. `docs/sitemap.xml` lists all ten pages and
`docs/robots.txt` points crawlers at it.

The five pages share one design contract. `docs/m3.css` holds the Material 3
roles (colour, shape, motion, type) and the shared top-bar controls, buttons
and `.visually-hidden`; `docs/theme.js` boots the theme before the first paint.
Each page seeds the roles in its own `style.css` and keeps its own fonts and one
signature element, which is why the sites look related without looking the
same. Run `python3 scripts/check-contrast.py` after changing a colour.

Before a pull request, run `python3 scripts/check-links.py`,
`python3 scripts/gen-sitemap.py --check` and
`python3 scripts/check-contrast.py`. The deploy stamps CSS/JS references
with the commit SHA; `checks.yml` runs the same checks in CI and asserts that
the project repositories' Pages sites stay disabled. See
[CONTRIBUTING.md](CONTRIBUTING.md). A 404 page lists the four project sites.

