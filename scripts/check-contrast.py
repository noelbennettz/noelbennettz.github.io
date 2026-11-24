#!/usr/bin/env python3
"""Check WCAG contrast for every colour pair the pages actually use.

Each page seeds the M3 roles in its own style.css, once per scheme. The checker
reads those declarations (no browser, no build step) and fails when a role that
carries text falls under 4.5:1, or a role used only for borders falls under
3:1. Entry-scoped primaries on the index are checked against the list surface
they sit on.

    python3 scripts/check-contrast.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.normpath(os.path.join(HERE, "..", "docs"))
ROLE = re.compile(r"--md-sys-color-([a-z-]+)\s*:\s*#([0-9a-fA-F]{3,8})\s*;")
BLOCK = re.compile(r"([^{}]*)\{([^{}]*)\}")
SITES = [
    ("index", "."),
    ("Hy2droid", "Hy2droid"),
    ("amneziawg-ui", "amneziawg-ui"),
    ("imail", "imail"),
]

# Pairs that carry text, and the surfaces they can land on.
TEXT_PAIRS = [
    ("on-surface", ["surface", "surface-container-low", "surface-container",
                    "surface-container-high"]),
    ("on-surface-variant", ["surface", "surface-container-low", "surface-container",
                            "surface-container-high"]),
    ("on-primary", ["primary"]),
    ("on-primary-container", ["primary-container"]),
    ("primary", ["surface", "surface-container-low", "surface-container"]),
    ("tertiary", ["surface", "surface-container"]),
    ("error", ["surface"]),
]
BORDER_PAIRS = [
    # A control's own edge must be visible (WCAG 1.4.11, 3:1).
    ("outline", ["surface"], 3.0),
    # Dividers are decorative; this floor only catches a divider that has
    # collapsed into its background by accident.
    ("outline-variant", ["surface"], 1.2),
]

def parse_hex(value):
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))

def luminance(rgb):
    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = luminance(parse_hex(a)), luminance(parse_hex(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def read_palettes(path):
    text = open(path, encoding="utf-8").read()
    base = "light"
    palettes = {"light": {}, "dark": {}}
    entries = {"light": [], "dark": []}
    for selector, body in BLOCK.findall(text):
        if "--md-sys-color-" not in body:
            continue
        scheme = None
        if '[data-theme="dark"]' in selector:
            scheme = "dark"
        elif '[data-theme="light"]' in selector:
            scheme = "light"
        elif ":root" in selector:
            declared = re.search(r"color-scheme\s*:\s*(light|dark)", body)
            base = declared.group(1) if declared else base
            scheme = base
        else:
            continue
        roles = dict((name, value) for name, value in ROLE.findall(body))
        if not roles:
            continue
        if ".entry" in selector:
            if "primary" in roles:
                entries[scheme].append((selector.strip(), roles["primary"]))
            continue
        palettes[scheme].update(roles)
    return palettes, entries

def main():
    problems = []
    checked = 0
    for name, folder in SITES:
        path = os.path.join(DOCS, folder, "style.css")
        palettes, entries = read_palettes(path)
        for scheme in ("light", "dark"):
            roles = palettes[scheme]
            if not roles:
                problems.append(f"{name} [{scheme}]: no roles declared")
                continue
            for fg, backgrounds in TEXT_PAIRS:
                if fg not in roles:
                    continue
                for bg in backgrounds:
                    if bg not in roles:
                        continue
                    ratio = contrast(roles[fg], roles[bg])
                    checked += 1
                    if ratio < 4.5:
                        problems.append(
                            f"{name} [{scheme}]: {fg} on {bg} = {ratio:.2f}:1 "
                            f"({roles[fg]} on {roles[bg]}), needs 4.5"
                        )
            for fg, backgrounds, minimum in BORDER_PAIRS:
                if fg not in roles:
                    continue
                for bg in backgrounds:
                    if bg not in roles:
                        continue
                    ratio = contrast(roles[fg], roles[bg])
                    checked += 1
                    if ratio < minimum:
                        problems.append(
                            f"{name} [{scheme}]: {fg} on {bg} = {ratio:.2f}:1 "
                            f"({roles[fg]} on {roles[bg]}), needs {minimum}"
                        )
            surface = roles.get("surface-container-low") or roles.get("surface")
            if surface:
                for selector, primary in entries[scheme]:
                    ratio = contrast(primary, surface)
                    checked += 1
                    if ratio < 4.5:
                        problems.append(
                            f"{name} [{scheme}]: {selector} primary = {ratio:.2f}:1 "
                            f"on surface-container-low, needs 4.5"
                        )
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(
            f"{len(problems)} contrast problem(s) in {checked} pairs",
            file=sys.stderr,
        )
        return 1
    print(f"contrast ok ({checked} pairs)", file=sys.stderr)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
