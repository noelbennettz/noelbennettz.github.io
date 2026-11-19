#!/usr/bin/env python3
"""Generate docs/sitemap.xml from the HTML files under docs/.

The root index and zh.html are listed first, then every project page. The
result is deterministic, so CI can regenerate it and fail on a diff.
"""
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs"))
BASE = "https://noelbennettz.github.io"
PREFERRED = ["index.html", "zh.html"]


def urls():
    found = []
    for base, _, files in os.walk(ROOT):
        for name in files:
            if not name.endswith(".html") or name == "404.html":
                continue
            rel = os.path.relpath(os.path.join(base, name), ROOT).replace(os.sep, "/")
            if rel == "index.html":
                path = "/"
            elif rel.endswith("/index.html"):
                path = "/" + rel[: -len("index.html")]
            else:
                path = "/" + rel
            found.append(path)

    def key(path):
        if path == "/":
            return (0, path)
        if path == "/zh.html":
            return (1, path)
        return (2, path)

    return sorted(set(found), key=key)


def main():
    check = "--check" in sys.argv
    body = "".join(f"  <url><loc>{BASE}{path}</loc></url>\n" for path in urls())
    text = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}"
        "</urlset>\n"
    )
    path = os.path.join(ROOT, "sitemap.xml")
    if check:
        try:
            current = open(path, encoding="utf-8").read()
        except OSError:
            current = ""
        if current != text:
            print("docs/sitemap.xml is stale; run scripts/gen-sitemap.py", file=sys.stderr)
            return 1
        print("sitemap ok", file=sys.stderr)
        return 0
    open(path, "w", encoding="utf-8").write(text)
    print(f"wrote {path} ({len(urls())} URLs)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
