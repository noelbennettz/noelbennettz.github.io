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
```

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
