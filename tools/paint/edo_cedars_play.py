#!/usr/bin/env python3
"""PAINT-23: the cedar path PLAYED, in the game itself (Playwright), after its picture and every number of its scene file
were made again (DEPTH.md, RECOMPOSE). Serve the game first (`python3 -m http.server 8774 --bind 127.0.0.1` from the top
of the repository), then:

    python3 edo_cedars_play.py [--port 8774] [--out out/edo-cedars-play]

What it does, as Mom from the mark `enter` (the three of them in their travel clothes, as the story has them here):
  walk      to every area's standing place, every mark, every arriving place, LIFT, and the constable's way: she must
            arrive (game.walkTo, then where she stands); and every one of those places a grown-up's size by the row
  door      a knock (a line), then a call: the line of light under the floor goes out, and comes back
  pipe      she listens: the fact edo.pipeHeard
  behind    she stands behind each of the two cedars and in front of it: drawn behind, drawn in front (a picture of each)
and as Little Sister:
  window    Mom comes to her place beside the wall and lifts her: she goes up the wall to the sill, and through (the game
            is then in the storehouse)
It prints PASS or what failed, whatever the page's console said, and leaves pictures to look at."""

import asyncio
import json
import os
import sys

from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REST = "window.game && game.scene && game.mode === 'play' && !game.busy && !(game.dialogue && game.dialogue.active)"
FLAGS = "edo.arrived,edo.when,edo.clothes,edo.dressed,edo.fed,edo.west,edo.sailed,edo.boated"
ENTER = """() => { const d = game.store.data; for (const id of ['mom','bigsis','lilsis']) { game.dress(id, 'edo'); if (id !== d.active) delete d.where[id]; }
                  return game.goto('edo-cedars', { via: 'cut', spawn: 'enter', card: false }); }"""


async def open_game(pw, port, lead, said, extra=""):
    b = await pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    ctx = await b.new_context(viewport={"width": 800, "height": 600})
    await ctx.add_init_script("try { localStorage.setItem('pabc.settings', JSON.stringify({ seenIntro: true })); } catch (e) {}")
    page = await ctx.new_page()
    page.on("console", lambda m: said.append(f"console {m.type}: {m.text[:240]}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: said.append(f"page error: {str(e)[:240]}"))
    await page.goto(f"http://127.0.0.1:{port}/index.html?scene=edo-cedars&lead={lead}&flags={FLAGS}{extra}")
    try:
        await page.wait_for_selector("#begin:not([disabled])", timeout=60000)
        await page.click("#begin")
    except Exception:
        pass
    await page.wait_for_function(REST, timeout=90000)
    await page.evaluate(ENTER)
    await page.wait_for_timeout(1500)
    await page.wait_for_function(REST, timeout=90000)
    await page.mouse.move(797, 598)
    return b, page


async def rest(page, ms=60000):
    """Wait for the game to come to rest, hurrying the lines along."""
    for _ in range(int(ms / 150)):
        if await page.evaluate(REST):
            return True
        await page.evaluate("() => { try { if (game.dialogue && game.dialogue.active) game.dialogue.advance(); } catch (e) {} }")
        await page.wait_for_timeout(150)
    return False


async def main(argv):
    port = argv[argv.index("--port") + 1] if "--port" in argv else "8774"
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(HERE, "out", "edo-cedars-play")
    os.makedirs(out, exist_ok=True)
    lay = json.load(open(os.path.join(HERE, "..", "..", "art", "scenes", "edo-cedars", "layout.json")))
    said, bad, notes = [], [], []
    async with async_playwright() as pw:
        # ------------------------------------------------------------ as Mom
        b, page = await open_game(pw, port, "mom", said)
        await page.wait_for_timeout(1800)                                   # (the bell, and the lamp in the window going out)
        await rest(page)
        await page.screenshot(path=os.path.join(out, "enter.png"))
        hz, full = await page.evaluate("() => [game.scene.horizon, game.scene.full]")
        places = await page.evaluate("""() => {
            const s = game.scene, out = [];
            for (const h of s.hotspots) if (h.id && Array.isArray(h.walkTo)) out.push(['area ' + h.id, h.walkTo[0], h.walkTo[1]]);
            for (const [k, v] of Object.entries(s.spawn)) out.push(['mark ' + k, v[0], v[1]]);
            for (const [k, v] of Object.entries(s.arrive)) v.forEach((p, i) => out.push(['arrive ' + k + ' ' + i, p[0], p[1]]));
            return out; }""")
        places.append(["LIFT", lay["lift"][0], lay["lift"][1]])
        for i, p in enumerate(lay["isukeWay"]):
            places.append([f"isukeWay {i}", p[0], p[1]])
        for name, x, y in places:
            got = await page.evaluate(f"async () => {{ await game.walkTo({x}, {y}); return [game.lead.x, game.lead.y, game.lead.scale]; }}")
            off = ((got[0] - x) ** 2 + (got[1] - y) ** 2) ** 0.5
            size = 160 * got[2]
            line = f"  walk {name:24s} ({x:5.1f}, {y:5.1f}) -> ({got[0]:6.1f}, {got[1]:6.1f})  a grown-up {size:5.1f} px"
            if off > 1.5:
                bad.append(f"walk: {name} ({x}, {y}): she stops at ({got[0]:.1f}, {got[1]:.1f}), {off:.1f} px off")
                line += "   OFF"
            print(line)
        # ------------------------------------------------------------ the two cedars people walk behind
        for cid, behind, front in (("cedar-l", (331, 500), (331, 530)), ("cedar-r", (678, 500), None)):       # (no walked ground lies in front of cedar-r)
            base = await page.evaluate(f"() => game.plane('{cid}').base")
            for tag, spot in (("behind", behind), ("front", front)):
                if spot is None:
                    continue
                x, y = spot
                got = await page.evaluate(f"async () => {{ await game.walkTo({x}, {y}); return [game.lead.x, game.lead.y]; }}")
                await page.wait_for_timeout(250)
                (x0, y0), (x1, y1) = base
                yb = y0 + (y1 - y0) * (got[0] - x0) / (x1 - x0) if x1 != x0 else y0
                is_behind = got[1] < yb
                await page.screenshot(path=os.path.join(out, f"{cid}-{tag}.png"))
                print(f"  {cid}: at ({got[0]:.0f}, {got[1]:.0f}) the base line is row {yb:.0f}: she is {'behind' if is_behind else 'in front of'} it (wanted: {tag})")
                if is_behind != (tag == "behind"):
                    bad.append(f"{cid}: at ({got[0]:.0f}, {got[1]:.0f}) she is on the wrong side of its base line")
        # ------------------------------------------------------------ the door: a knock, then a call
        use = "(id) => { const s = game.view.spots.find((h) => h.id === id); if (!s) return false; game.interact(s, 'use'); return true; }"
        shown = "() => !game.plane('light-on').hidden"
        if not await page.evaluate(shown):
            bad.append("door: the line of light under the floor is not showing before the knock")
        ok = await page.evaluate(use, "door")
        await page.wait_for_timeout(400)
        await rest(page)
        at = await page.evaluate("() => [game.lead.x, game.lead.y, game.lead.yaw]")
        print(f"  door: knocked from ({at[0]:.0f}, {at[1]:.0f}), facing {at[2]}; the light is {'on' if await page.evaluate(shown) else 'OUT'}")
        await page.evaluate(use, "door")
        seen_out = False
        for _ in range(120):
            if not await page.evaluate(shown):
                if not seen_out:
                    await page.screenshot(path=os.path.join(out, "door-light-out.png"))
                seen_out = True
            await page.evaluate("() => { try { if (game.dialogue && game.dialogue.active) game.dialogue.advance(); } catch (e) {} }")
            if seen_out and await page.evaluate(shown) and await page.evaluate(REST):
                break
            await page.wait_for_timeout(100)
        back_on = await page.evaluate(shown)
        print(f"  door: called: the light went out: {seen_out}; and came back: {back_on}")
        if not ok or not seen_out or not back_on:
            bad.append(f"door: the call (went out {seen_out}, came back {back_on})")
        await rest(page)
        await page.screenshot(path=os.path.join(out, "door.png"))
        # ------------------------------------------------------------ the pipe
        await page.evaluate(use, "pipe")
        await page.wait_for_timeout(600)
        await page.screenshot(path=os.path.join(out, "pipe.png"))
        await rest(page)
        heard = await page.evaluate("() => !!game.flag('edo.pipeHeard')")
        at = await page.evaluate("() => [game.lead.x, game.lead.y]")
        print(f"  pipe: listened at ({at[0]:.0f}, {at[1]:.0f}); edo.pipeHeard: {heard}")
        if not heard:
            bad.append("pipe: edo.pipeHeard is not set")
        # every area a look, so that a line of each is said without an error
        for hid in await page.evaluate("() => game.view.spots.filter((h) => h.id && !h.mate && !String(h.id).startsWith('mate')).map((h) => h.id)"):
            await page.evaluate("(id) => { const s = game.view.spots.find((h) => h.id === id); game.interact(s, 'look'); }", hid)
            await page.wait_for_timeout(250)
            if not await rest(page, 30000):
                bad.append(f"look {hid}: the game did not come to rest")
        await b.close()
        # ------------------------------------------------------------ as Little Sister: the window
        b, page = await open_game(pw, port, "lilsis", said)
        await page.wait_for_timeout(1800)
        await rest(page)
        await page.evaluate(use, "window")
        track, shot = [], False
        for i in range(400):
            st = await page.evaluate("() => ({ scene: game.scene && game.scene.id, lil: game.lead ? [game.lead.x, game.lead.y, game.lead.scale] : null, mom: game.actor('mom') ? [game.actor('mom').x, game.actor('mom').y] : null, busy: game.busy })")
            track.append(st)
            if st["scene"] != "edo-cedars":
                break
            if st["lil"] and st["lil"][1] < lay["marks"]["window"][1] - 40 and not shot:
                await page.screenshot(path=os.path.join(out, "window-lift.png"))
                shot = True
            await page.evaluate("() => { try { if (game.dialogue && game.dialogue.active) game.dialogue.advance(); } catch (e) {} }")
            await page.wait_for_timeout(60)
        on_path = [t for t in track if t["scene"] == "edo-cedars" and t["lil"]]
        top = min(on_path, key=lambda t: t["lil"][1])
        mom = [t["mom"] for t in on_path if t["mom"]][-1]
        sill, lift, mark = lay["sill"], lay["lift"], lay["marks"]["window"]
        print(f"  window: Little Sister from ({on_path[0]['lil'][0]:.0f}, {on_path[0]['lil'][1]:.0f}) stood at ({mark[0]}, {mark[1]}), went up to ({top['lil'][0]:.0f}, {top['lil'][1]:.0f}) (the sill: {sill}); Mom at ({mom[0]:.0f}, {mom[1]:.0f}) (LIFT: {lift}); then the game is in: {track[-1]['scene']}")
        if abs(top["lil"][0] - sill[0]) > 3 or abs(top["lil"][1] - sill[1]) > 3:
            bad.append(f"window: she went up to ({top['lil'][0]:.0f}, {top['lil'][1]:.0f}), not to the sill {sill}")
        if abs(mom[0] - lift[0]) > 2 or abs(mom[1] - lift[1]) > 2:
            bad.append(f"window: Mom stood at ({mom[0]:.0f}, {mom[1]:.0f}), not at LIFT {lift}")
        if track[-1]["scene"] != "edo-storehouse":
            bad.append(f"window: the game did not go to the storehouse (it is in {track[-1]['scene']})")
        await page.wait_for_timeout(1500)
        await rest(page, 30000)
        await page.screenshot(path=os.path.join(out, "window-through.png"))
        await b.close()
        # ------------------------------------------------------------ the morning: a look out at the path from the storehouse (the constable on it)
        b = await pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        ctx = await b.new_context(viewport={"width": 800, "height": 600})
        await ctx.add_init_script("try { localStorage.setItem('pabc.settings', JSON.stringify({ seenIntro: true })); } catch (e) {}")
        page = await ctx.new_page()
        page.on("console", lambda m: said.append(f"console {m.type}: {m.text[:240]}") if m.type in ("error", "warning") else None)
        page.on("pageerror", lambda e: said.append(f"page error: {str(e)[:240]}"))
        await page.goto(f"http://127.0.0.1:{port}/index.html?scene=edo-storehouse&lead=bigsis&flags={FLAGS},edo.cedarsSeen,edo.pipeHeard,edo.unbarred,edo.matMoved,edo.knocked,edo.hidden,edo.trusted,edo.watch")
        try:
            await page.wait_for_selector("#begin:not([disabled])", timeout=60000)
            await page.click("#begin")
        except Exception:
            pass
        await page.wait_for_function(REST, timeout=90000)
        await page.evaluate("() => { for (const id of ['mom','bigsis','lilsis']) game.dress(id, 'edo-hatback'); }")
        await page.wait_for_timeout(500)
        await rest(page)
        ok = await page.evaluate("() => { const s = game.view.spots.find((h) => h.id === 'door-shut' || h.id === 'door'); if (!s) return false; game.interact(s, 'use'); return true; }")
        man = None
        for _ in range(150):
            man = await page.evaluate("() => { const f = game.view.cast.get('isuke'); return f && game.view.cast.get('cedar-l') ? [f.x, f.y, f.scale] : null; }")
            if man:
                break
            await page.wait_for_timeout(100)
        if man:
            await page.wait_for_timeout(900)
            await page.screenshot(path=os.path.join(out, "isuke-on-path.png"))
            want = lay["isukeWay"][1]
            print(f"  the look out at the path: the constable's man at ({man[0]:.0f}, {man[1]:.0f}), {160 * man[2] * 156 / 175:.0f} px tall (his way's second place: {want})")
            if abs(man[0] - want[0]) > 1 or abs(man[1] - want[1]) > 1:
                bad.append(f"the look out at the path: he stands at ({man[0]:.0f}, {man[1]:.0f}), not at {want}")
        else:
            bad.append("the look out at the path (the storehouse's door, in the morning) did not show him on it")
        await rest(page, 40000)
        back = await page.evaluate("() => game.scene && game.scene.id")
        if back != "edo-storehouse":
            bad.append(f"after the look out at the path the game is in {back}, not back in the storehouse")
        await b.close()
    said = [s for s in said if "favicon" not in s]
    print("console:", "nothing" if not said else "")
    for s in said[:20]:
        print("  " + s)
        bad.append("console: " + s)
    print("PLAY: PASS" if not bad else f"PLAY: {len(bad)} TO MEND")
    for x in bad:
        print("  - " + x)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv[1:])))
