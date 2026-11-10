#!/usr/bin/env python3
"""PAINT-23: the foot of Mount Shosha PLAYED, in the game itself (Playwright), after its picture and every number of its
scene file were made again (DEPTH.md, RECOMPOSE). Serve the game first (`python3 -m http.server 8772 --bind 127.0.0.1`
from the top of the repository), then:

    python3 edo_shosha_play.py [--port 8772] [--out out/edo-shosha-play]

What it does, as Mom, arriving by the map from the town at the mark `road` (edo.supperMade, the story's #37):
  arrive    the women on the bench argue, O-Ume settles it (the lines hurried along); a picture
  walk      to every area's standing place, every mark, every arriving place, the place for talking to Ryokai at the
            lattice, the edge's way out: she must arrive (game.walkTo, then where she stands), a grown-up's size by the row
  talk      to Ryokai and to O-Ume (every option asked, then the way out), and to the three women on the bench
  climb     the east path (Ryokai on his feet at his place, then down again), the stone, the bench (the end of it)
  lock      Look closer at the lock from the hall's doors: the close-up edo-lock opens; Step back: she is where she stood
  open      the doors open (the scene's own openDoors, as the close-up calls it): the light goes red, the women go in at the
            doorway, two come out and go home down the road, O-Ume takes the rice ball in, Ryokai goes round to the
            lattice; where each of them ends; a picture
  lattice   talk to Ryokai at the lattice; then in by the open doors (the game is in edo-hall)
  night     the cut-scene Mind The Fire from the hall: back here at the mark `hall`, O-Ume outside with her lantern at her
            new place (edo-night.js); a picture
It prints PASS or what failed, whatever the page's console said, and leaves pictures to look at."""

import asyncio
import json
import os
import sys

from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REST = "window.game && game.scene && game.mode === 'play' && !game.busy && !(game.dialogue && game.dialogue.active)"
FLAGS = "edo.supperMade"
ADVANCE = """() => { try {
    const list = document.querySelector('ul.choices');
    if (list) { const bs = [...list.querySelectorAll('button')]; const b = bs.find((x) => x.classList.contains('new') && !x.classList.contains('exit')) || bs.find((x) => x.classList.contains('exit')) || bs[bs.length - 1]; if (b) b.click(); return 'choice'; }
    if (game.dialogue && game.dialogue.active) { game.dialogue.advance(); return 'line'; }
  } catch (e) {} return null; }"""


async def open_game(pw, port, lead, said, flags=FLAGS):
    b = await pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    ctx = await b.new_context(viewport={"width": 800, "height": 600})
    await ctx.add_init_script("try { localStorage.setItem('pabc.settings', JSON.stringify({ seenIntro: true })); } catch (e) {}")
    page = await ctx.new_page()
    page.on("console", lambda m: said.append(f"console {m.type}: {m.text[:240]}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: said.append(f"page error: {str(e)[:240]}"))
    await page.goto(f"http://127.0.0.1:{port}/index.html?scene=edo-shosha&lead={lead}&flags={flags}")
    try:
        await page.wait_for_selector("#begin:not([disabled])", timeout=60000)
        await page.click("#begin")
    except Exception:
        pass
    await page.wait_for_function("window.game && game.scene && game.mode === 'play'", timeout=90000)
    await page.mouse.move(797, 598)
    return b, page


async def rest(page, ms=60000):
    """Wait for the game to come to rest, hurrying the lines along and taking each new option of a talk, then the way out."""
    for _ in range(int(ms / 150)):
        if await page.evaluate(REST) and not await page.evaluate("() => !!document.querySelector('ul.choices')"):
            return True
        await page.evaluate(ADVANCE)
        await page.wait_for_timeout(150)
    return False


async def use(page, hid, verb="use", nth=0):
    """Use (or look at) the area of that id that is live now (its `when`)."""
    return await page.evaluate("""([id, verb, nth]) => { const s = game.view.spots.filter((h) => h.id === id && (!h.when || h.when(game)))[nth]; if (!s) return false; game.interact(s, verb); return true; }""", [hid, verb, nth])


async def walk_all(page, places, bad, skip_near_people=True):
    """Walk the lead to each place; a place where somebody is standing or sitting (their own place) is left for later.
    -> the places left."""
    left = []
    for name, x, y in places:
        if skip_near_people:
            near = await page.evaluate(f"() => ['ume', 'ryokai', 'tome', 'wife', 'girl'].some((id) => {{ const a = game.actor(id); return a && !a.hidden && Math.abs(a.x - {x}) < 34 && Math.abs(a.y - {y}) < 12; }})")
            if near:
                left.append((name, x, y))
                continue
        got = await page.evaluate(f"async () => {{ await game.walkTo({x}, {y}); return [game.lead.x, game.lead.y, game.lead.scale]; }}")
        off = ((got[0] - x) ** 2 + (got[1] - y) ** 2) ** 0.5
        line = f"  walk {name:22s} ({x:5.1f}, {y:5.1f}) -> ({got[0]:6.1f}, {got[1]:6.1f})  a grown-up {160 * got[2]:5.1f} px"
        if off > 1.5:
            bad.append(f"walk: {name} ({x}, {y}): she stops at ({got[0]:.1f}, {got[1]:.1f}), {off:.1f} px off")
            line += "   OFF"
        print(line)
    return left


async def where(page, who):
    return await page.evaluate(f"() => {{ const a = game.actor('{who}'); return a && !a.hidden ? [a.x, a.y] : null; }}")


async def main(argv):
    port = argv[argv.index("--port") + 1] if "--port" in argv else "8772"
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(HERE, "out", "edo-shosha-play")
    os.makedirs(out, exist_ok=True)
    lay = json.load(open(os.path.join(HERE, "..", "..", "art", "scenes", "edo-shosha", "layout.json")))
    said, bad = [], []
    async with async_playwright() as pw:
        b, page = await open_game(pw, port, "mom", said)
        # ------------------------------------------------------------ arriving: the women argue; O-Ume settles it
        await page.wait_for_timeout(1200)
        await rest(page)
        at = await page.evaluate("() => [game.lead.x, game.lead.y]")
        road = lay["marks"]["road"]
        print(f"  arrived at ({at[0]:.0f}, {at[1]:.0f}) (the mark road: {road})")
        if abs(at[0] - road[0]) > 2 or abs(at[1] - road[1]) > 2:
            bad.append(f"arrive: Mom is at ({at[0]:.0f}, {at[1]:.0f}), not on the mark road {road}")
        await page.screenshot(path=os.path.join(out, "arrive.png"))
        for who in ("ume", "ryokai", "tome", "wife", "girl"):
            p = await where(page, who)
            print(f"  {who:7s} at {p}")
        # ------------------------------------------------------------ every standing place, mark and arriving place
        places = await page.evaluate("""() => {
            const s = game.scene, out = [];
            for (const h of s.hotspots) if (h.id && Array.isArray(h.walkTo)) out.push(['area ' + h.id, h.walkTo[0], h.walkTo[1]]);
            for (const [k, v] of Object.entries(s.spawn)) out.push(['mark ' + k, v[0], v[1]]);
            for (const [k, v] of Object.entries(s.arrive)) v.forEach((p, i) => out.push(['arrive ' + k + ' ' + i, p[0], p[1]]));
            for (const [k, v] of Object.entries(s.edges || {})) if (v.walkTo) out.push(['edge ' + k, v.walkTo[0], v.walkTo[1]]);
            return out; }""")
        places.append(["LATTICE (Ryokai's)", lay["LATTICE"][0], lay["LATTICE"][1]])
        places.append(["lattice talk", lay["latticeTalk"][0], lay["latticeTalk"][1]])
        later = await walk_all(page, places, bad)
        print(f"  (left for when they have gone: {[n for n, x, y in later]})")
        await page.screenshot(path=os.path.join(out, "walked.png"))
        # ------------------------------------------------------------ the talks
        for who in ("ryokai", "ume", "tome", "wife", "girl"):
            ok = await use(page, who)
            await page.wait_for_timeout(300)
            done = await rest(page, 90000)
            at = await page.evaluate("() => [game.lead.x, game.lead.y]")
            print(f"  talk {who:7s} {'done' if ok and done else 'FAILED'} from ({at[0]:.0f}, {at[1]:.0f})")
            if not ok or not done:
                bad.append(f"talk {who}: {'no area' if not ok else 'the game did not come to rest'}")
            if who == "ume":
                await page.screenshot(path=os.path.join(out, "talk-ume.png"))
        # ------------------------------------------------------------ the path (Ryokai on his feet), the stone, the bench
        await use(page, "pathup")
        seen_up = None
        for _ in range(60):
            k = await page.evaluate("() => { const a = game.actor('ryokai'); return a ? [a.kind || a.look || '', a.x, a.y] : null; }")
            if k and "standing" in str(k[0]):
                seen_up = k
                await page.screenshot(path=os.path.join(out, "climb.png"))
                break
            await page.evaluate(ADVANCE)
            await page.wait_for_timeout(120)
        await rest(page)
        print(f"  climb: Ryokai on his feet: {seen_up}")
        if not seen_up:
            bad.append("climb: Ryokai never stood up")
        elif abs(seen_up[1] - lay["marks"]["ryokai"][0]) > 2 and abs(seen_up[2] - lay["marks"]["ryokai"][1]) > 2:
            bad.append(f"climb: Ryokai stood at ({seen_up[1]:.0f}, {seen_up[2]:.0f}), not at his mark")
        for hid in ("stone", "bench", "combs", "mountain", "stepball", "step", "slips", "doors", "lattice", "lantern", "hut", "plain", "castle", "sky", "cherry", "trees", "hall"):
            await use(page, hid, "look")
            await page.wait_for_timeout(200)
            if not await rest(page, 30000):
                bad.append(f"look {hid}: the game did not come to rest")
        await use(page, "bench")
        await rest(page)
        # ------------------------------------------------------------ the lock: the close-up, and back
        await use(page, "lock")
        into = None
        for _ in range(200):
            sid = await page.evaluate("() => game.scene && game.scene.id")
            if sid == "edo-lock":
                into = sid
                break
            await page.evaluate(ADVANCE)
            await page.wait_for_timeout(100)
        await page.wait_for_timeout(800)
        await page.screenshot(path=os.path.join(out, "lock-closeup.png"))
        print(f"  lock: the close-up is {'up' if into else 'NOT up'}")
        if not into:
            bad.append("lock: the close-up edo-lock did not open")
        else:
            await page.evaluate("async () => { await game.stepBack(); }")
            await page.wait_for_timeout(1200)
            await rest(page)
            sid = await page.evaluate("() => game.scene && game.scene.id")
            at = await page.evaluate("() => [game.lead.x, game.lead.y]")
            lk = lay["marks"]["lock"]
            print(f"  lock: stepped back into {sid} at ({at[0]:.0f}, {at[1]:.0f}) (the mark lock: {lk})")
            if sid != "edo-shosha":
                bad.append(f"lock: Step back went to {sid}")
            elif abs(at[0] - lk[0]) > 3 or abs(at[1] - lk[1]) > 3:
                bad.append(f"lock: stepped back to ({at[0]:.0f}, {at[1]:.0f}), not to the mark lock {lk}")
            await page.screenshot(path=os.path.join(out, "lock-back.png"))
        # ------------------------------------------------------------ the doors open (the close-up's openDoors)
        await page.evaluate("() => { game.run(async () => { const m = await import(new URL('js/content/scenes/edo-shosha.js', location.href).href); await m.openDoors(game); }); }")
        track = {}
        shot = False
        for i in range(900):
            st = await page.evaluate("() => { const o = {}; for (const id of ['ume', 'ryokai', 'tome', 'wife', 'girl']) { const a = game.actor(id); o[id] = a ? [Math.round(a.x), Math.round(a.y), !!a.hidden] : null; } o.open = !!game.flag('edo.hallOpen'); o.busy = !!game.busy; return o; }")
            for k_, v in st.items():
                if k_ in ("open", "busy") or v is None:
                    continue
                track.setdefault(k_, []).append(tuple(v))
            if st["open"] and not shot:
                await page.wait_for_timeout(200)
                await page.screenshot(path=os.path.join(out, "doors-open.png"))
                shot = True
            if st["open"] and not st["busy"] and await page.evaluate(REST):
                break
            await page.evaluate(ADVANCE)
            await page.wait_for_timeout(80)
        await rest(page)
        await page.wait_for_timeout(600)
        await page.screenshot(path=os.path.join(out, "open-after.png"))
        ends = {k_: v[-1] for k_, v in track.items()}
        print(f"  open: edo.hallOpen {await page.evaluate('() => !!game.flag(\"edo.hallOpen\")')}; where each ends: {ends}")
        lat = lay["LATTICE"]
        r_end = await where(page, "ryokai")
        if not r_end or abs(r_end[0] - lat[0]) > 3 or abs(r_end[1] - lat[1]) > 3:
            bad.append(f"open: Ryokai ends at {r_end}, not at the lattice {lat}")
        for who in ("tome", "wife", "girl", "ume"):
            if not await page.evaluate(f"() => {{ const a = game.actor('{who}'); return !a || a.hidden; }}"):
                bad.append(f"open: {who} is still on the stage after the doors open")
        door = lay["DOORWAY"]
        for who in ("tome", "ume"):
            pts = [p for p in track.get(who, []) if not p[2]]
            near = [p for p in pts if abs(p[0] - door[0]) <= 3 and abs(p[1] - door[1]) <= 3]
            print(f"  open: {who} reached the doorway {door}: {bool(near)}")
            if not near:
                bad.append(f"open: {who} never reached the doorway {door}")
        # ------------------------------------------------------------ the places that were taken: free now (the women and O-Ume are in or
        # home; Ryokai is at the lattice, so his own place there is his)
        still = await walk_all(page, later, bad)
        for name, x, y in still:
            print(f"  walk {name:22s} ({x}, {y}): Ryokai's own place at the lattice (he stands there now)")
        # ------------------------------------------------------------ Ryokai at the lattice; then in by the open doors
        ok = await use(page, "ryokai")
        await page.wait_for_timeout(300)
        await rest(page, 60000)
        at = await page.evaluate("() => [game.lead.x, game.lead.y]")
        print(f"  talk ryokai at the lattice from ({at[0]:.0f}, {at[1]:.0f}) (the place: {lay['latticeTalk']}): {ok}")
        await page.screenshot(path=os.path.join(out, "lattice-talk.png"))
        await use(page, "doors")
        for _ in range(200):
            if await page.evaluate("() => game.scene && game.scene.id") == "edo-hall":
                break
            await page.evaluate(ADVANCE)
            await page.wait_for_timeout(100)
        sid = await page.evaluate("() => game.scene && game.scene.id")
        print(f"  in by the open doors: the game is in {sid}")
        if sid != "edo-hall":
            bad.append(f"doors: the open doors did not lead into the hall (the game is in {sid})")
        await page.wait_for_timeout(800)
        await rest(page, 60000)
        await b.close()
        # ------------------------------------------------------------ Mind The Fire: back out here, O-Ume with her lantern
        b, page = await open_game(pw, port, "mom", said, flags="edo.supperMade,edo.hallOpen,edo.umeIn,edo.holdHands")
        await page.wait_for_timeout(800)
        await rest(page)
        await page.evaluate("() => { game.run(() => game.cutscene('edo-night')); }")
        got = None
        for _ in range(300):
            st = await page.evaluate("() => { const u = game.view && game.view.cast && game.view.cast.get('ume'); const m = game.actor('mom'); return game.scene && game.scene.id === 'edo-shosha' && u && !u.hidden ? [Math.round(u.x), Math.round(u.y), m ? Math.round(m.x) : null, m ? Math.round(m.y) : null] : null; }")
            if st:
                got = st
                await page.wait_for_timeout(500)
                await page.screenshot(path=os.path.join(out, "night-lantern.png"))
                break
            await page.wait_for_timeout(100)
        nu = lay["nightUme"]
        print(f"  night: O-Ume with her lantern at {got[:2] if got else None} (the place: {nu}); Mom at {got[2:] if got else None} (the mark hall: {lay['marks']['hall']})")
        if not got or abs(got[0] - nu[0]) > 2 or abs(got[1] - nu[1]) > 2:
            bad.append(f"night: O-Ume stands at {got[:2] if got else None}, not at {nu}")
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
