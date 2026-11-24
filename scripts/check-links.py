#!/usr/bin/env python3
"""Fail on broken local links and missing local images in docs/.

Only local references are checked: http(s), mailto, data, javascript and pure
fragments are external or in-page. A link to a directory resolves to its
index.html.
"""
import html
import os
import re
import sys
import urllib.parse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs")
ROOT = os.path.normpath(ROOT)
REF = re.compile(r'(?:href|src)="([^"]+)"', re.IGNORECASE)

def resolve(page, ref):
    ref = html.unescape(ref).strip()
    if not ref or ref.startswith(("#", "//")):
        return None
    parsed = urllib.parse.urlsplit(ref)
    if parsed.scheme or parsed.netloc:
        return None
    path = urllib.parse.unquote(parsed.path)
    if not path:
        return None
    if path.startswith("/"):
        target = os.path.normpath(os.path.join(ROOT, path.lstrip("/")))
    else:
        target = os.path.normpath(os.path.join(os.path.dirname(page), path))
    if os.path.isdir(target):
        target = os.path.join(target, "index.html")
    return target

def main():
    problems = []
    pages = 0
    for base, _, files in os.walk(ROOT):
        for name in files:
            if not name.endswith(".html"):
                continue
            page = os.path.join(base, name)
            pages += 1
            try:
                text = open(page, encoding="utf-8").read()
            except OSError as exc:
                problems.append(f"{page}: {exc}")
                continue
            for match in REF.finditer(text):
                target = resolve(page, match.group(1))
                if target and not os.path.exists(target):
                    rel = os.path.relpath(page, ROOT)
                    problems.append(f"{rel}: missing {match.group(1)!r}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(
            f"{len(problems)} broken local reference(s) in {pages} page(s)",
            file=sys.stderr,
        )
        return 1
    print(f"links ok ({pages} pages)", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
