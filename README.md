# noelbennettz.github.io

Source of <https://noelbennettz.github.io/>, an index of the open-source
projects and their sites:

- [Hy2droid](https://noelbennettz.github.io/Hy2droid/) — Hysteria 2 for Android
- [AmneziaWG Web UI](https://noelbennettz.github.io/amneziawg-ui/) — self-hosted Docker panel
- [iMail](https://noelbennettz.github.io/imail/) — mail for your own domains

Every page is here: the index at `docs/`, and the three project sites under
`docs/Hy2droid/`, `docs/amneziawg-ui/` and `docs/imail/`, each served at the
`https://noelbennettz.github.io/<project>/` path above. The project
repositories no longer carry a `docs/` directory of their own — this repository
is the only place the pages live, so a change to a project page is a change
here.

The site is plain HTML/CSS — English and Traditional Chinese, each page linking
to the other — with no build step, deployed to GitHub Pages by
`.github/workflows/pages.yml`. `docs/sitemap.xml` lists all eight pages and
`docs/robots.txt` points crawlers at it.

Before a pull request, run `python3 scripts/check-links.py` and
`python3 scripts/gen-sitemap.py --check`. The deploy stamps CSS/JS references
with the commit SHA; `checks.yml` runs the same checks in CI and asserts that
the project repositories' Pages sites stay disabled. See
[CONTRIBUTING.md](CONTRIBUTING.md). A 404 page lists the three project sites.

