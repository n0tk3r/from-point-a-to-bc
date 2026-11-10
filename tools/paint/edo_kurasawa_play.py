#!/usr/bin/env python3
"""PAINT-23: Nishikurasawa PLAYED, in the game itself (Playwright), after its picture and every number of its scene file
were made again (DEPTH.md, RECOMPOSE). Serve the game first (`python3 -m http.server 8773 --bind 127.0.0.1` from the top
of the repository), then:

    python3 edo_kurasawa_play.py [--port 8773] [--out out/edo-kurasawa-play]

What it does, as Mom, the three of them in O-Tami's clothes:
  arrive    from Yui: the road west at the west end of Yui's street (edo-village): the game is in Nishikurasawa, the one
            played on `arrive_mom`, the other two on their arriving places (arrive.yui)
  walk      to every area's standing place, every mark, every arriving place, FROM_TOP, AT_GRILL and the print's place: she
            must arrive (game.walkTo, then where she stands), at a grown-up's size by the row; the people's own marks
            (O-Kuni's, behind her grill, and the rest) are walked to and reported, not required
  talk      O-Kuni (the shell for the climb: the three come round her grill, edo.shellShared), the bearers (Sakuji, then
            Tora), Soshichi, each to the end; the komuso: his look and both his uses (the idea, then his line)
  courier   the relay courier stopped on his way at the grill, the palanquin and the trunks: drawn in front of the grill
            and the palanquin, behind the trunks, and behind both front planes (a picture of each)
  looks     every area a look
  up/down   up by the right edge (edo-satta) and down by its left edge: back on `climb`, the other two on FROM_TOP; up by
            the cliff road's use and by the road's, down each time; out by the left edge to Yui (edo-village, `fromWest`)
and as Little Sister:
  sit       the bearers: she sits in the palanquin (on KAGO_SEAT, behind its front) and gets out again
  print     Soshichi: she comes to him for the print (on its place) and has it (toyamaprint, edo.printGiven)
It prints PASS or what failed, whatever the page's console said, and leaves pictures to look at."""

import asyncio
import json
import os
import sys

from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REST = "window.game && game.scene && game.mode === 'play' && !game.busy && !(game.dialogue && game.dialogue.active) && !(game.dialogue && game.dialogue.choosing)"
FLAGS = "edo.arrived,edo.clothes,edo.dressed,edo.hensWest"
NPC = {"kuni", "bearers", "tora", "peddler", "komuso"}                  # the people's own marks (they stand on them)
USE = "(a) => { const s = game.view.spots.find((h) => h.id === a[0]); if (!s) return false; game.interact(s, a[1]); return true; }"
PICK = """(line) => {
  const bs = [...document.querySelectorAll('ul.choices button')];
  if (!bs.length) return 'none';
  let b = null;
  if (line) { const t = (game.lines[line] || [])[1]; b = bs.find((x) => x.textContent.trim() === String(t).trim()); }
  else b = bs.find((x) => x.classList.contains('exit')) || bs[bs.length - 1];
  if (!b) return 'missing: ' + bs.map((x) => x.textContent.trim()).join(' | ');
  b.click(); return 'ok'; }"""
ADVANCE = "() => { try { if (game.dialogue && game.dialogue.active) game.dialogue.advance(); } catch (e) {} }"
WHERE = "(id) => { const f = game.actor(id); return f ? [f.x, f.y, f.scale] : null; }"


async def open_game(pw, port, lead, said, scene="edo-village"):
    b = await pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    ctx = await b.new_context(viewport={"width": 800, "height": 600})
    await ctx.add_init_script("try { localStorage.setItem('pabc.settings', JSON.stringify({ seenIntro: true })); } catch (e) {}")
    page = await ctx.new_page()
    page.on("console", lambda m: said.append(f"console {m.type}: {m.text[:240]}") if m.type in ("error", "warning") else None)
    page.on("pageerror", lambda e: said.append(f"page error: {str(e)[:240]}"))
    await page.goto(f"http://127.0.0.1:{port}/index.html?scene={scene}&lead={lead}&flags={FLAGS}")
    try:
        await page.wait_for_selector("#begin:not([disabled])", timeout=60000)
        await page.click("#begin")
    except Exception:
        pass
    await page.wait_for_function(REST, timeout=90000)
    await page.mouse.move(797, 598)
    return b, page


async def rest(page, ms=60000):
    """Wait for the game to come to rest, hurrying the lines along (a list of choices is a failure here: talk() picks)."""
    for _ in range(int(ms / 120)):
        if await page.evaluate(REST):
            return True
        if await page.evaluate("() => !!(game.dialogue && game.dialogue.choosing)"):
            await page.evaluate(PICK, None)
        await page.evaluate(ADVANCE)
        await page.wait_for_timeout(120)
    return False


async def talk(page, spot, picks, bad, during=None):
    """Talk to someone (the area's use) and pick these options by their line ids in turn, then the way out. `during`
    (line id -> coroutine) runs when that option has just been picked."""
    picks = list(picks)
    if not await page.evaluate(USE, [spot, "use"]):
        bad.append(f"talk {spot}: no such area")
        return
    for _ in range(1200):
        if await page.evaluate("() => !!(game.dialogue && game.dialogue.choosing)"):
            want = picks.pop(0) if picks else None
            got = await page.evaluate(PICK, want)
            if got != "ok":
                bad.append(f"talk {spot}: the option {want or 'bye'}: {got}")
                await page.evaluate(PICK, None)
            elif during and want in during:
                await during[want]()
        elif await page.evaluate(REST):
            break
        await page.evaluate(ADVANCE)
        await page.wait_for_timeout(90)
    if picks:
        bad.append(f"talk {spot}: not offered: {picks}")
    await rest(page)


async def scene_is(page, sid, ms=60000):
    for _ in range(int(ms / 150)):
        if await page.evaluate("() => game.scene && game.scene.id") == sid and await page.evaluate(REST):
            return True
        if await page.evaluate("() => !!(game.dialogue && game.dialogue.choosing)"):
            await page.evaluate(PICK, None)
        await page.evaluate(ADVANCE)
        await page.wait_for_timeout(150)
    return False


async def out_by(page, side):
    """A real click in that edge's band, where the game says one lands on the floor."""
    pt = await page.evaluate(f"() => game.edgePoint('{side}')")
    if not pt:
        return False
    await page.mouse.click(pt[0], pt[1])
    await page.mouse.move(797, 598)
    return True


def near(a, b, tol=2.0):
    return a is not None and abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol


async def main(argv):
    port = argv[argv.index("--port") + 1] if "--port" in argv else "8773"
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(HERE, "out", "edo-kurasawa-play")
    os.makedirs(out, exist_ok=True)
    lay = json.load(open(os.path.join(HERE, "..", "..", "art", "scenes", "edo-kurasawa", "layout.json")))
    said, bad = [], []
    async with async_playwright() as pw:
        # ============================================================ as Mom, from Yui
        b, page = await open_game(pw, port, "mom", said)
        await rest(page)
        if not await page.evaluate(USE, ["west", "use"]):
            bad.append("arrive: Yui has no road west to use")
        if not await scene_is(page, "edo-kurasawa"):
            bad.append("arrive: the road west from Yui did not come to Nishikurasawa")
        sc = await page.evaluate("() => ({ spawn: game.scene.spawn, arrive: game.scene.arrive, horizon: game.scene.horizon, full: game.scene.full })")
        await page.screenshot(path=os.path.join(out, "arrive.png"))
        mom, big, lil = [await page.evaluate(WHERE, w) for w in ("mom", "bigsis", "lilsis")]
        others = sc["arrive"]["yui"]
        print(f"  arrive from Yui: Mom at ({mom[0]:.0f}, {mom[1]:.0f}) (arrive_mom {sc['spawn']['arrive_mom']}); Big Sister ({big[0]:.0f}, {big[1]:.0f}), Little Sister ({lil[0]:.0f}, {lil[1]:.0f}) (arrive.yui {others})")
        if not near(mom, sc["spawn"]["arrive_mom"]):
            bad.append(f"arrive: Mom is at ({mom[0]:.0f}, {mom[1]:.0f}), not on arrive_mom")
        if not ((near(big, others[0]) and near(lil, others[1])) or (near(big, others[1]) and near(lil, others[0]))):
            bad.append("arrive: the other two are not on their arriving places")
        # ------------------------------------------------------------ every place she can be sent to
        hz, full = sc["horizon"], sc["full"]
        places = await page.evaluate("""() => {
            const s = game.scene, out = [];
            for (const h of s.hotspots) if (h.id && Array.isArray(h.walkTo)) out.push(['area ' + h.id, h.walkTo[0], h.walkTo[1]]);
            for (const [k, v] of Object.entries(s.spawn)) out.push(['mark ' + k, v[0], v[1]]);
            for (const [k, v] of Object.entries(s.arrive)) v.forEach((p, i) => out.push(['arrive ' + k + ' ' + i, p[0], p[1]]));
            return out; }""")
        for k, v in lay["atGrill"].items():
            places.append([f"AT_GRILL {k}", v[0], v[1]])
        places.append(["printWalk", lay["printWalk"][0], lay["printWalk"][1]])
        for name, x, y in places:
            got = await page.evaluate(f"async () => {{ await game.walkTo({x}, {y}); return [game.lead.x, game.lead.y, game.lead.scale]; }}")
            off = ((got[0] - x) ** 2 + (got[1] - y) ** 2) ** 0.5
            size = 160 * got[2]
            want = min(1.12, max(0.26, (got[1] - hz) / (full - hz))) * 160
            npc = name.startswith("mark ") and name[5:] in NPC
            line = f"  walk {name:22s} ({x:5.1f}, {y:5.1f}) -> ({got[0]:6.1f}, {got[1]:6.1f})  a grown-up {size:5.1f} px"
            if off > 1.5:
                line += "   OFF" + (" (somebody's own place: not a place she is sent to)" if npc else "")
                if not npc:
                    bad.append(f"walk: {name} ({x}, {y}): she stops at ({got[0]:.1f}, {got[1]:.1f}), {off:.1f} px off")
            if abs(size - want) > 1.0 and off <= 1.5:
                bad.append(f"walk: {name}: a grown-up is {size:.1f} px there, the row says {want:.1f}")
            print(line)
        # ------------------------------------------------------------ the talks
        seen = {}

        async def at_grill():
            for _ in range(120):
                ps = [await page.evaluate(WHERE, w) for w in ("mom", "bigsis", "lilsis")]
                if all(near(p, lay["atGrill"][w], 1.5) for p, w in zip(ps, ("mom", "bigsis", "lilsis"))):
                    await page.wait_for_timeout(300)
                    await page.screenshot(path=os.path.join(out, "shell-at-grill.png"))
                    seen["grill"] = ps
                    return
                await page.evaluate(ADVANCE)
                await page.wait_for_timeout(100)
        await talk(page, "kuni", ["edo.kuni.opt.morning.mom"], bad, during={"edo.kuni.opt.morning.mom": at_grill})
        shared = await page.evaluate("() => !!game.flag('edo.shellShared')")
        print("  O-Kuni's shell: the three round her grill at " + (", ".join(f"({p[0]:.0f}, {p[1]:.0f})" for p in seen["grill"]) if "grill" in seen else "NOT ALL THERE")
              + f" (AT_GRILL {lay['atGrill']}); edo.shellShared: {shared}")
        if "grill" not in seen:
            bad.append("O-Kuni's shell: the three did not all come to their places round the grill (AT_GRILL)")
        if not shared:
            bad.append("O-Kuni: edo.shellShared is not set after the shell")
        await talk(page, "kuni", ["edo.kuni.opt.west.mom"], bad)
        await talk(page, "sakuji", ["edo.bearers.opt.fare.mom"], bad)
        await talk(page, "tora", ["edo.bearers.opt.tora.mom"], bad)
        await talk(page, "soshichi", ["edo.soshichi.opt.trust.mom"], bad)
        for verb in ("look", "use", "use"):                                    # the komuso: his look; the idea (Big Sister's, Mom's answer); his line
            await page.evaluate(USE, ["komuso", verb])
            await page.wait_for_timeout(300)
            if not await rest(page, 30000):
                bad.append(f"komuso {verb}: the game did not come to rest")
        if not await page.evaluate("() => !!(game.store.data.seenLines || {})['edo.kurasawa.komuso.idea.1']"):
            bad.append("komuso: the idea (edo.kurasawa.komuso.idea.1) was not said")
        print(f"  talks: O-Kuni (shell, west), Sakuji, Tora, Soshichi, the komuso: done; Mom at ({(await page.evaluate(WHERE, 'mom'))[0]:.0f}, {(await page.evaluate(WHERE, 'mom'))[1]:.0f})")
        # ------------------------------------------------------------ the courier, stopped where he passes the cut-outs
        await page.evaluate("async () => { await game.walkTo(140, 560); }")
        for tx, what, front_of, behind in ((282, "grill", ["grill"], []), (566, "palanquin", ["kago"], []), (652, "trunks", [], ["trunks"])):
            pos = await page.evaluate("""(tx) => {
                const E = game.effects, fx = E.get('courier');
                if (!fx) return null;
                E.hold(true); fx.restart(); fx.plan(0);
                const tr = fx.trips[0];
                let best = 0, bd = 1e9;
                for (let s = 0; s <= fx.len; s += 0.5) { const p = fx.along(s); const d = Math.abs(p[0] - tx); if (d < bd) { bd = d; best = s; } }
                const d = tr.back ? fx.len - best : best;
                fx.seek((tr.start + (d / fx.len) * tr.dur) * 1000);
                return [fx.fig.x, fx.fig.y, fx.fig.hidden]; }""", tx)
            await page.wait_for_timeout(250)
            order = await page.evaluate("() => game.view.cast.order().map((s) => s.id)")
            await page.screenshot(path=os.path.join(out, f"courier-{what}.png"))
            if not pos or pos[2] or "fx:courier" not in order:
                bad.append(f"courier at the {what}: not on the stage ({pos})")
                continue
            i = order.index("fx:courier")
            wrong = [c for c in front_of if c in order and order.index(c) > i] + [c for c in behind + ["front", "near"] if c in order and order.index(c) < i]
            area = await page.evaluate("() => { const s = game.view.spots.find((h) => h.id === 'courier'); return s ? (s.rect || null) : null; }")
            print(f"  courier at the {what}: ({pos[0]:.0f}, {pos[1]:.0f}); drawn in front of {front_of or '-'}, behind {behind + ['front', 'near']}: {'yes' if not wrong else 'NO ' + str(wrong)}; his area {area}")
            if wrong:
                bad.append(f"courier at the {what}: on the wrong side of {wrong}")
            if not area:
                bad.append(f"courier at the {what}: his area does not go with him")
        await page.evaluate("() => { const E = game.effects; E.get('courier').restart(); E.hold(false); }")
        # ------------------------------------------------------------ every area a look
        for hid in await page.evaluate("() => game.view.spots.filter((h) => h.id && !h.mate && !String(h.id).startsWith('mate')).map((h) => h.id)"):
            await page.evaluate(USE, [hid, "look"])
            await page.wait_for_timeout(200)
            if not await rest(page, 30000):
                bad.append(f"look {hid}: the game did not come to rest")
        # ------------------------------------------------------------ up to the pass and down, three ways up
        for way in ("edge", "cliffroad", "road"):
            if way == "edge":
                ok = await out_by(page, "E")
            else:
                ok = await page.evaluate(USE, [way, "use"])
            if not ok:
                bad.append(f"up by the {way}: nothing to click")
                continue
            if not await scene_is(page, "edo-satta"):
                bad.append(f"up by the {way}: the game did not come to the top of the pass")
                continue
            await page.screenshot(path=os.path.join(out, f"up-{way}.png"))
            if not await out_by(page, "W"):
                bad.append("down: the top of the pass has no way down at its left edge")
                continue
            if not await scene_is(page, "edo-kurasawa"):
                bad.append(f"down (after the {way}): the game did not come back to Nishikurasawa")
                continue
            await page.wait_for_timeout(400)
            lead = await page.evaluate(WHERE, "mom")
            o1, o2 = await page.evaluate(WHERE, "bigsis"), await page.evaluate(WHERE, "lilsis")
            ft = sc["arrive"]["climb"]
            print(f"  up by the {way} and down: Mom at ({lead[0]:.0f}, {lead[1]:.0f}) (climb {sc['spawn']['climb']}), the other two at ({o1[0]:.0f}, {o1[1]:.0f}), ({o2[0]:.0f}, {o2[1]:.0f}) (FROM_TOP {ft})")
            if not near(lead, sc["spawn"]["climb"]):
                bad.append(f"down (after the {way}): Mom is at ({lead[0]:.0f}, {lead[1]:.0f}), not on `climb`")
            if not ((near(o1, ft[0]) and near(o2, ft[1])) or (near(o1, ft[1]) and near(o2, ft[0]))):
                bad.append(f"down (after the {way}): the other two are not on FROM_TOP")
            await page.screenshot(path=os.path.join(out, f"down-{way}.png"))
        # ------------------------------------------------------------ back to Yui by the left edge
        if not await out_by(page, "W"):
            bad.append("to Yui: no way out at the left edge")
        elif not await scene_is(page, "edo-village"):
            bad.append("to Yui: the left edge did not go back to Yui")
        else:
            at = await page.evaluate(WHERE, "mom")
            print(f"  out by the left edge: in Yui, Mom at ({at[0]:.0f}, {at[1]:.0f})")
            await page.screenshot(path=os.path.join(out, "back-to-yui.png"))
        await b.close()
        # ============================================================ as Little Sister
        b, page = await open_game(pw, port, "lilsis", said)
        await rest(page)
        await page.evaluate("() => game.goto('edo-kurasawa', { spawn: 'yui', card: false })")
        if not await scene_is(page, "edo-kurasawa"):
            bad.append("Little Sister: the game did not come to Nishikurasawa")
        seat = lay["kagoSeat"]
        seen = {}

        async def sitting():
            for _ in range(100):
                p = await page.evaluate(WHERE, "lilsis")
                if near(p, seat, 0.6) and await page.evaluate("() => (game.dressOf('lilsis') || '').endsWith('step')"):
                    await page.wait_for_timeout(500)
                    await page.screenshot(path=os.path.join(out, "lilsis-in-palanquin.png"))
                    seen["sat"] = p
                    return
                await page.evaluate(ADVANCE)
                await page.wait_for_timeout(100)
        await talk(page, "sakuji", ["edo.bearers.opt.sit.lil"], bad, during={"edo.bearers.opt.sit.lil": sitting})
        after = await page.evaluate(WHERE, "lilsis")
        dressed = await page.evaluate("() => game.dressOf('lilsis')")
        print(f"  Little Sister in the palanquin: sat at {seen.get('sat')} (KAGO_SEAT {seat}); after the talk at ({after[0]:.0f}, {after[1]:.0f}) in '{dressed}'")
        if "sat" not in seen:
            bad.append(f"the palanquin: Little Sister did not sit on KAGO_SEAT {seat}")
        if (dressed or "").endswith("step"):
            bad.append("the palanquin: Little Sister did not get up again")
        got = await page.evaluate("async () => { await game.walkTo(484, 495); return [game.lead.x, game.lead.y]; }")
        if not near(got, [484, 495], 1.5):
            bad.append(f"the palanquin: from the seat she cannot walk away (stops at {got})")

        async def printed():
            for _ in range(120):
                p = await page.evaluate(WHERE, "lilsis")
                if near(p, lay["printWalk"], 1.5):
                    await page.wait_for_timeout(300)
                    await page.screenshot(path=os.path.join(out, "lilsis-print.png"))
                    seen["print"] = p
                    return
                await page.evaluate(ADVANCE)
                await page.wait_for_timeout(100)
        await talk(page, "soshichi", ["edo.soshichi.opt.boxes.lil"], bad, during={"edo.soshichi.opt.boxes.lil": printed})
        has = await page.evaluate("() => (game.store.data.inventory.lilsis || []).includes('toyamaprint') && !!game.flag('edo.printGiven')")
        print(f"  the print: Little Sister came to {seen.get('print')} (printWalk {lay['printWalk']}); she has it: {has}")
        if "print" not in seen:
            bad.append(f"the print: Little Sister did not come to its place {lay['printWalk']}")
        if not has:
            bad.append("the print: she does not have toyamaprint (edo.printGiven)")
        await talk(page, "kuni", ["edo.kuni.opt.hiss.lil"], bad)
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
