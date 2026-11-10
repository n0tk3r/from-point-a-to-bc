#!/usr/bin/env python3
"""A picture of the game itself showing a scene, at rest, with its people in it (round twenty-three).

    python3 game_shot.py "<address after index.html>" out.png [--port 8765] [--walk x,y] [--wait ms]

    python3 game_shot.py "?scene=edo-cedars&lead=mom&flags=edo.arrived,edo.when" out/edo-cedars-game.png

The address is the scene file's own "Try it" line (the part from the question mark on). The game must be running:
`python3 tools/serve.py 8765` from the top of the repository (or `python3 -m http.server 8765` there). With --walk the
lead is sent to a place first (to see people at the back, in the middle and at the front). Needs Playwright with its
Chromium. Prints what the page's console said, if anything: a clean run prints only the file's name.
"""

import asyncio
import sys

from playwright.async_api import async_playwright

REST = "window.game && game.scene && game.mode === 'play' && !game.busy && !(game.dialogue && game.dialogue.active)"


async def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    query, out = argv[0], argv[1]
    port = argv[argv.index("--port") + 1] if "--port" in argv else "8765"
    walk = [float(v) for v in argv[argv.index("--walk") + 1].split(",")] if "--walk" in argv else None
    wait = int(argv[argv.index("--wait") + 1]) if "--wait" in argv else 900
    said = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        ctx = await b.new_context(viewport={"width": 800, "height": 600})
        await ctx.add_init_script("try { localStorage.setItem('pabc.settings', JSON.stringify({ seenIntro: true })); } catch (e) {}")
        page = await ctx.new_page()
        page.on("console", lambda m: said.append(f"console {m.type}: {m.text[:200]}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: said.append(f"page error: {str(e)[:200]}"))
        await page.goto(f"http://127.0.0.1:{port}/index.html{query}")
        try:
            await page.wait_for_selector("#begin:not([disabled])", timeout=60000)
            await page.click("#begin")
        except Exception:
            pass
        await page.wait_for_function(REST, timeout=90000)
        if walk:
            await page.evaluate(f"() => {{ game.walkTo({walk[0]}, {walk[1]}); }}")
            last, still = None, 0
            for _ in range(120):                                  # (the game is at rest while she walks: wait until she stands still)
                await page.wait_for_timeout(250)
                at = await page.evaluate("game.lead ? [Math.round(game.lead.x), Math.round(game.lead.y)] : null")
                still = still + 1 if at == last else 0
                last = at
                if still >= 3:
                    break
            else:
                said.append("the walk did not come to rest")
            print(f"  the lead stands at {last}")
        await page.wait_for_timeout(wait)
        await page.screenshot(path=out)
        await b.close()
    print(out)
    for s in said[:10]:
        print("  " + s)

asyncio.run(main(sys.argv[1:]))
