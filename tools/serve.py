#!/usr/bin/env python3
"""Run the game on this computer.

    python3 tools/serve.py            then open http://localhost:8000
    python3 tools/serve.py 8080       another port
    python3 tools/serve.py --lan      let other devices on your network open it (a phone, say)

It differs from "python3 -m http.server" in two ways, both so that what you see is
always the files as they are right now:

  - it tells the browser to keep no copies, so an old file is never reused;
  - it re-stamps the pages (see tools/stamp.py) whenever a code file, a style file or
    a picture has changed, so the page you test is the page you will push. (It looks
    each time a page is opened: reload the page to see a picture you have just repainted.)
"""

import functools
import http.server
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stamp  # noqa: E402  (tools/stamp.py)

ROOT = stamp.ROOT


def restamp():
    try:
        changed = stamp.stamp()
        if changed:
            print("  re-stamped " + ", ".join(changed) + " (code, styles or pictures changed)")
    except (Exception, SystemExit) as err:      # never let a stamping mishap take the server down
        print(f"  could not stamp the pages: {err}")


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0].split("#")[0]
        if path.endswith("/") or path.endswith(".html"):
            restamp()
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, pattern, *args):      # one quiet line for a page, nothing for its thirty files
        if args and isinstance(args[0], str) and (" / " in args[0] or ".html" in args[0]):
            super().log_message(pattern, *args)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    port = int(args[0]) if args else 8000
    host = "0.0.0.0" if "--lan" in sys.argv[1:] else "127.0.0.1"
    restamp()
    server = http.server.ThreadingHTTPServer((host, port), functools.partial(Handler, directory=ROOT))
    print(f"From Point A to B.C. is at http://localhost:{port}   (Ctrl+C to stop)")
    if host == "0.0.0.0":
        print("Other devices on your network can open it at this computer's address, same port.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
