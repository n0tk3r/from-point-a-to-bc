#!/usr/bin/env python3
"""Stamp the pages with the fingerprint of every code file, style file and picture.

Why: GitHub Pages lets a browser keep each file for ten minutes. The game is some
thirty code files and many more pictures, so for ten minutes after a push a browser
could run new files next to old ones it had kept, and the game would break in odd ways
(or show last week's painting behind this week's people).

What this does: it works out a short fingerprint of each file in js/, css/ and art/ and
writes into each page

  - an "import map" that gives every code file the address  file.js?v=<fingerprint>
  - the same kind of address on each style sheet link
  - a list of the pictures and their fingerprints (<script id="art-stamps">), from which
    js/engine/assets.js makes each picture's address the same way
  - data-build="..." on the <html> tag, which changes whenever anything changes,
    a picture included

A file's address now changes exactly when the file does, so a browser's kept copy
of an old file is never used for a new page. No game code has to change for this:
modules go on importing "./state.js" and the browser looks the real address up, and
scenes go on naming "art/scenes/egypt-crash/back.png".

Run it after changing anything in js/, css/ or art/, before you commit:

    python3 tools/stamp.py           writes the pages
    python3 tools/stamp.py --check   changes nothing; says if a page is out of date

tools/serve.py runs it for you whenever you open the game locally.
"""

import hashlib
import json
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The pages that load game files.
PAGES = ["index.html", "tools/storyboard.html", "tools/sprites.html"]

OPEN = "<!-- files: written by tools/stamp.py. Each address changes when its file changes, so a browser cannot mix old files with new. -->"
CLOSE = "<!-- /files -->"


def fingerprint(data):
    return hashlib.sha256(data).hexdigest()[:10]


# What counts as a picture under art/. (.json is for numbers that travel with a picture.)
ART = (".png", ".jpg", ".webp", ".json")


def files_under(folder, ending):
    """Every file under a folder whose name ends in `ending` (one ending, or several)."""
    found = []
    for here, _, names in os.walk(os.path.join(ROOT, folder)):
        for name in names:
            if name.lower().endswith(ending):
                found.append(os.path.relpath(os.path.join(here, name), ROOT).replace(os.sep, "/"))
    return sorted(found)


def fingerprints():
    """{ "js/engine/game.js": "3f2a…", "css/game.css": "…", "art/scenes/egypt-crash/back.png": "…" }
    for every code file, style file and picture."""
    prints = {}
    for path in files_under("js", ".js") + files_under("css", ".css") + files_under("art", ART):
        try:
            with open(os.path.join(ROOT, path), "rb") as f:
                prints[path] = fingerprint(f.read())
        except OSError:              # it was there a moment ago: someone is moving files about. The next run will see it.
            pass
    return prints


def bare(page):
    """The page with every stamp taken off, so two stampings of the same page compare equal."""
    page = re.sub(r'(<html\b[^>]*?)\s+data-build="[^"]*"', r"\1", page, count=1)
    page = re.sub(r'(<link\b[^>]*\bhref="[^"?]+\.css)\?v=[0-9a-f]+(")', r"\1\2", page)
    page = re.sub(re.escape(OPEN) + r".*?" + re.escape(CLOSE) + r"\n?", "", page, flags=re.S)
    return page


def stamped(page, name, prints):
    """The page with fresh stamps. `name` is where the page lives, e.g. "tools/storyboard.html"."""
    folder = os.path.dirname(name)
    up = "../" * (folder.count("/") + 1) if folder else "./"          # how this page reaches the top of the site
    page = bare(page)
    build = fingerprint(("\n".join(f"{p} {h}" for p, h in sorted(prints.items())) + "\n" + page).encode("utf-8"))

    def link(match):
        href = match.group(2)
        path = os.path.normpath(os.path.join(folder, href)).replace(os.sep, "/")
        return f"{match.group(1)}{href}?v={prints[path]}{match.group(3)}" if path in prints else match.group(0)

    page = re.sub(r'(<link\b[^>]*\bhref=")([^"?]+\.css)(")', link, page)
    imports = {f"{up}{path}": f"{up}{path}?v={h}" for path, h in sorted(prints.items()) if path.endswith(".js")}
    # Pictures are named from the top of the site on every page, so this list is the same in each of them.
    art = {path: h for path, h in sorted(prints.items()) if path.startswith("art/")}
    listing = json.dumps(art, indent=2).replace("<", "\\u003c")         # (no file name can close the script element early)
    block = (f'{OPEN}\n<script type="importmap">\n{json.dumps({"imports": imports}, indent=2)}\n</script>\n'
             f'<script type="application/json" id="art-stamps">\n{listing}\n</script>\n{CLOSE}\n')
    if "</head>" not in page:
        raise SystemExit(f"{name} has no </head> to put the list of files before.")
    page = page.replace("</head>", block + "</head>", 1)
    page, n = re.subn(r"<html\b([^>]*)>", lambda m: f'<html{m.group(1)} data-build="{build}">', page, count=1)
    if n != 1:
        raise SystemExit(f"{name} has no <html> tag to stamp.")
    return page


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def replace(path, text):
    """Put new text in a file in one step, so nothing ever reads half a page."""
    handle, temp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".stamp-")
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.chmod(temp, os.stat(path).st_mode & 0o7777)
        os.replace(temp, path)
    except BaseException:
        if os.path.exists(temp):
            os.remove(temp)
        raise


def stamp(write=True):
    """Stamp every page. Returns the names of the pages that were (or would be) changed."""
    prints = fingerprints()
    changed = []
    for name in PAGES:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            continue
        for _ in range(5):
            before = read(path)
            after = stamped(before, name, prints)
            if after == before:
                break
            if not write:
                changed.append(name)
                break
            if read(path) != before:         # someone saved the page while it was being stamped: stamp what they saved
                continue
            replace(path, after)
            changed.append(name)
            break
    return changed


if __name__ == "__main__":
    check = "--check" in sys.argv[1:]
    changed = stamp(write=not check)
    if check:
        if changed:
            print("Out of date: " + ", ".join(changed) + ". Run: python3 tools/stamp.py")
            sys.exit(1)
        print("Every page is up to date.")
    else:
        print("Stamped: " + ", ".join(changed) if changed else "Nothing to do: every page is already up to date.")
