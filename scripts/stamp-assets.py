#!/usr/bin/env python3
"""Copy docs/ to a deploy directory and stamp CSS/JS with the commit SHA.

GitHub Pages serves files with long-lived caching. A query string that changes
with the deployed commit makes sure a stylesheet change is picked up without
changing every page by hand.
"""
import os
import re
import shutil
import sys

src, dst, version = sys.argv[1], sys.argv[2], sys.argv[3]
assets = re.compile(r'((?:href|src)=")([^"?#]+\.(?:css|js))(")', re.IGNORECASE)

if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)

for base, _, files in os.walk(dst):
    for name in files:
        if not name.endswith(".html"):
            continue
        path = os.path.join(base, name)
        text = open(path, encoding="utf-8").read()
        stamped = assets.sub(lambda m: f"{m.group(1)}{m.group(2)}?v={version}{m.group(3)}", text)
        if stamped != text:
            open(path, "w", encoding="utf-8").write(stamped)
print(f"stamped assets in {dst} with {version}", file=sys.stderr)
