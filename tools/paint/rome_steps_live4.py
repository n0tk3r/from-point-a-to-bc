#!/usr/bin/env python3
"""Round four, to look at: a Rome scene in the game with the painter's marks put on the stage live (as
briefs/out/fx-4-ready.md says): the new cut-outs from layout.json "cutouts" (the laundry's pieces replace the plane
"laundry"), then every "fx" mark. Screenshots at moments of the effects' time, and what the engine said.

    python3 rome_steps_live4.py rome-steps|rome-street|rome-temple [ms,ms,...]   -> out/<scene>-4-live-<ms>.png"""

import asyncio
import json
import os
import sys

from playwright.async_api import async_playwright

BASE = os.environ.get("GAME_URL", "http://localhost:8765/")
scene = sys.argv[1] if len(sys.argv) > 1 else "rome-steps"
moments = [int(v) for v in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2000, 6000]
HERE = os.path.dirname(os.path.abspath(__file__))

SETUP = """async (scene) => {
  const art = `art/scenes/${scene}/`;
  const L = await (await fetch(art + "layout.json", { cache: "no-store" })).json();
  const cast = game.view.cast, said = [];
  for (const c of L.cutouts || []) {
    if (c.id.startsWith("laundry-") && cast.items.has("laundry")) cast.remove("laundry");
    const spec = { ...c };
    if (c.file) spec.src = art + c.file;
    if (c.frames) spec.frames = c.frames.map((f) => art + f);
    cast.addCutout(c.id, spec);
  }
  await cast.load();
  for (const m of L.fx || []) { try { game.effects.add(m); } catch (e) { said.push(`${m.id}: ${e.message}`); } }
  return { fx: (L.fx || []).length, cutouts: (L.cutouts || []).length, said };
}"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": 800, "height": 600})
        await ctx.add_init_script("try { localStorage.setItem('pabc.settings', JSON.stringify({ seenIntro: true })); } catch (e) {}")
        page = await ctx.new_page()
        notes = []
        page.on("console", lambda m: notes.append(f"{m.type}: {m.text}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: notes.append(f"pageerror: {e}"))
        flags = {"rome-temple": "rome.arrived,rome.inside", "rome-street": "rome.arrived,rome.sawStreet,rome.knowsBC"}.get(scene, "rome.arrived")
        await page.goto(BASE + f"index.html?scene={scene}&lead=son&still&flags={flags}")
        await page.wait_for_selector("#begin:not([disabled])", timeout=30000)
        await page.click("#begin")
        await page.wait_for_function("window.game && game.mode === 'play' && game.scene && !game.busy", timeout=30000)
        await page.wait_for_timeout(400)
        print(json.dumps(await page.evaluate(SETUP, scene)))
        await page.wait_for_timeout(300)
        for ms in moments:
            st = await page.evaluate(f"(() => {{ game.effects.hold(true); game.effects.seek({ms}); const c = game.view.cast; c.ctx.clearRect(0, 0, 800, 600); c.last = ''; c.shots = []; c.update(0); return game.effects.list.map((e) => [e.id, e.shown, e.drawn]); }})()")
            print(ms, json.dumps(st))
            await page.screenshot(path=os.path.join(HERE, "out", f"{scene}-4-live-{ms}.png"))
        print("\n".join(notes[:40]) or "no console errors or warnings")
        await b.close()

asyncio.run(main())
