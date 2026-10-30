"""PAINT-20C: the cedar path's layout.json, measured from the finished picture and the kit's numbers."""

import numpy as np

from edo_cedars_kit import *


def box_of(alpha):
    ys, xs = np.where(alpha > 0.5)
    if not len(ys):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def walk_outline():
    """The steps from the foot of the picture up to the storehouse's front, and round its right side to under the
    window and the pipe: 10 px in from the steps' edges, clear of the house's walls, the kiln and the lean-to."""
    left = [(int(path_x(y) - half_width(y) + 10), y) for y in (600, 560, 520, 488, 462)]
    top = [(334, 452), (326, 438), (420, 436), (500, 434), (556, 430), (606, 436), (640, 448), (640, 462), (604, 470), (560, 466), (520, 462), (496, 458)]
    right = [(int(path_x(y) + half_width(y) - 10), y) for y in (462, 488, 520, 560, 600)]
    return left + top + right


def layout(info, cut):
    fl, fr, br = HOUSE["fl"], HOUSE["fr"], HOUSE["br"]
    gap, wh = HOUSE["floor_gap"], HOUSE["wall_h"]
    dx0, dx1 = HOUSE["door"]
    wx0, wx1, wy0, wy1 = HOUSE["window"]
    stands = {name: {"at": list(p), "grownup_px": round(grownup_px(p[1]), 1)} for name, p in MARKS.items()}
    way = [list(p) for p in ISUKE_WAY]
    stands["isukeWay"] = [{"at": list(p), "grownup_px": round(grownup_px(p[1]), 1)} for p in ISUKE_WAY]
    K = KILN
    Fg = FIGURE
    things = [
        {"id": "cedars", "what": "the cedars: towering trunks in a rhythm of verticals on both sides of the path, their crowns lost above the frame, mist between them",
         "shape": {"poly": [[0, 0], [800, 0], [800, 300], [560, 330], [540, 420], [300, 420], [290, 330], [0, 300]]}, "stand": [404, 520], "face": "N"},
        {"id": "steps", "what": "the worn stone steps climbing the slope, wet, puddles on the treads that ring when the rain hits them",
         "shape": {"poly": [[int(path_x(y) - half_width(y)), y] for y in (598, 540, 490, 450)] + [[int(path_x(y) + half_width(y)), y] for y in (450, 490, 540, 598)]},
         "stand": [410, 540], "face": "N"},
        {"id": "figure", "what": "a small stone figure by the path, worn smooth, a scrap of red cloth tied at its neck (scenery: Big Sister will not touch it; Little Sister says good evening)",
         "shape": {"rect": [Fg["x"] - 14, Fg["base"] - Fg["h"] - 2, 28, Fg["h"] + 6]}, "stand": list(MARKS["figure"]), "face": "W"},
        {"id": "mist", "what": "mist drifting between the trunks and over the slope", "shape": {"poly": [[0, 280], [280, 300], [300, 372], [0, 400]]}, "stand": [380, 500], "face": "W"},
        {"id": "pipe", "what": "a bamboo pipe sticking out of the hillside behind the storehouse (air for the room underneath; a murmur comes out of it)",
         "shape": {"rect": [PIPE["from"][0] - 4, PIPE["to"][1] - 6, PIPE["to"][0] - PIPE["from"][0] + 10, PIPE["from"][1] - PIPE["to"][1] + 12]}, "stand": list(MARKS["pipe"]), "face": "N"},
        {"id": "storehouse", "what": "the charcoal-burner's storehouse: dark boards, a thatched roof heavy with rain, a lean-to of faggots and sacks; the floor on short posts",
         "shape": {"poly": [[fl[0] - 14, fl[1] + 2], [fl[0] - 14, fl[1] - gap - wh - 6], [fl[0] + 36, fl[1] - gap - HOUSE["ridge_h"] - 4], [br[0] - 50, br[1] - gap - HOUSE["ridge_h"] * 0.93 - 6], [br[0] + 14, br[1] - gap - wh * 0.92 - 10], [br[0] + 2, br[1] + 2], [fr[0], fr[1] + 2]]},
         "stand": list(MARKS["door"]), "face": "N"},
        {"id": "door", "what": "the storehouse's front door, outside: planks, a lintel; barred on the inside (nobody answers)",
         "shape": {"poly": [[dx0, 428], [dx1, 427], [dx1, 427 - int(wh * 0.76)], [dx0, 428 - int(wh * 0.76)]]}, "stand": list(MARKS["door"]), "face": "N"},
        {"id": "window", "what": "the small high square window in the storehouse's back (its right end wall, seen from the side): a seven-year-old fits, helped up; lit from inside while the lantern is (window-lit)",
         "shape": {"rect": [wx0 - 2, wy0 - 4, wx1 - wx0 + 4, wy1 - wy0 + 10]}, "stand": list(MARKS["window"]), "face": "N"},
        {"id": "eaves", "what": "the thatch's eaves, dripping", "shape": {"poly": [[fl[0] - 14, fl[1] - gap - wh + 8], [br[0] + 14, br[1] - gap - wh * 0.92 + 4], [br[0] + 14, br[1] - gap - wh * 0.92 - 12], [fl[0] - 14, fl[1] - gap - wh - 8]]},
         "stand": list(MARKS["door"]), "face": "N"},
        {"id": "rain", "what": "the rain: fine straight slanting lines, steady (ENGINE-20's moving thing: fx 'rain')", "shape": {"poly": [[0, 0], [800, 0], [800, 240], [0, 240]]}, "stand": [404, 540], "face": "N"},
        {"id": "light", "what": "a thin line of warm light under the storehouse's floor, between the posts (the cut-out light-on; it goes out and comes back)",
         "shape": {"poly": [[fl[0], fl[1] + 3], [fr[0], fr[1] + 3], [fr[0], fr[1] - gap - 4], [fl[0], fl[1] - gap - 4]]}, "stand": list(MARKS["door"]), "face": "N"},
        {"id": "kiln", "what": "an earth charcoal kiln beside the storehouse, a dome with a low arched mouth, cold", "shape": {"poly": [[K["cx"] - K["rx"] - 2, K["cy"] + 4], [K["cx"] + K["rx"] + 2, K["cy"] + 4], [K["cx"] + K["rx"], K["cy"] - 18], [K["cx"] + 10, K["cy"] - K["ry"] - 8], [K["cx"] - 10, K["cy"] - K["ry"] - 8], [K["cx"] - K["rx"], K["cy"] - 18]]},
         "stand": [566, 452], "face": "E"},
        {"id": "isuke", "what": "Isuke, the constable's man, when he comes up the path (#27; PEOPLE-20 draws him): his place when he talks is marks.door, having come up isukeWay",
         "shape": {"rect": [380, 350, 48, 96]}, "stand": [430, 470], "face": "W", "when": "edo.isukeOnPath"},
    ]
    planes = [
        {"id": "light-on", "file": "light-on.png", "plane": "back", "alt": True, "box": box_of(cut["light-on"][1]),
         "note": "the line of lamplight under the floor: show it while the lamp below is lit (it goes out when they call, and comes back); the backdrop has the dark gap under it"},
        {"id": "window-lit", "file": "window-lit.png", "plane": "back", "alt": True, "box": box_of(cut["window-lit"][1]),
         "note": "the small high window lit from inside (a lantern behind it): show it while the lantern in the storehouse is lit (#25: Big Sister saw it go out); the backdrop has the window dark"},
        {"id": "cedar-l", "file": "cedar-l.png", "base": [[80, 574], [182, 516]], "box": box_of(cut["cedar-l"][1]), "what": "the two near cedars left of the foot of the path"},
        {"id": "cedar-r", "file": "cedar-r.png", "base": [[670, 518], [770, 572]], "box": box_of(cut["cedar-r"][1]), "what": "the two near cedars right of the foot of the path"},
        {"id": "front", "file": "front.png", "plane": "front", "box": box_of(cut["front"][1]), "what": "the two nearest trunks at the picture's edges"},
    ]
    eave_hide = [[fl[0] - 16, fl[1] - gap - wh - 10], [br[0] + 16, br[1] - gap - wh * 0.92 - 14], [br[0] + 16, br[1] + 4], [fl[0] - 16, fl[1] + 4]]
    fx = [
        {"id": "rain", "type": "rain", "what": "fine steady spring rain: straight lines slanting from upper left to lower right, the density of a steady shower, hidden where the eaves cover the walls and the ground under them, and under the lean-to",
         "area": [[0, 0], [800, 0], [800, 600], [0, 600]], "slant": [-8, 1.0], "slant_is": "dx per dy: 8 px left over 100 px down, about 5 degrees off the vertical (the lines run down and a little to the right, the wind from the left)",
         "density": 0.0011, "density_is": "drops on the stage at once per px^2: about 530 lines falling at once over the whole stage", "length": [10, 22], "speed": 520, "color": "#dfe6ec", "opacity": 0.42,
         "behind": [eave_hide, [[LEANTO["x0"] - 8, LEANTO["roof_y"] - 10], [LEANTO["x1"], LEANTO["wall_y"] - 24], [LEANTO["x1"], LEANTO["post_y"]], [LEANTO["x0"] - 8, LEANTO["post_y"] + 4]]],
         "splash": {"on": "steps", "size": 2}, "plane": "front"},
        {"id": "drip-1", "type": "stream", "what": "a drip off the eaves at the house's front-left corner", "path": [[fl[0] - 12, fl[1] - gap - wh + 8], [fl[0] - 12, fl[1] - 2]], "width": 1, "color": "#cfd8e0", "light": "#eef2f4", "opacity": 0.5, "speed": 90, "splash": 2, "base": fl[1]},
        {"id": "drip-2", "type": "stream", "what": "a drip off the eaves over the door", "path": [[dx1 + 10, fl[1] - gap - wh + 6], [dx1 + 10, fl[1] - 1]], "width": 1, "color": "#cfd8e0", "light": "#eef2f4", "opacity": 0.5, "speed": 90, "splash": 2, "base": fl[1]},
        {"id": "drip-3", "type": "stream", "what": "a drip off the end wall's eaves, by the window", "path": [[br[0] + 8, br[1] - gap - wh * 0.92 + 4], [br[0] + 8, br[1] - 1]], "width": 1, "color": "#cfd8e0", "light": "#eef2f4", "opacity": 0.5, "speed": 90, "splash": 2, "base": br[1]},
        {"id": "puddle-1", "type": "ripples", "what": "rain ringing a puddle on a tread", "at": [392, 585], "radius": [1, 14], "flat": 0.3, "every": [0.4, 1.4], "rings": 1, "speed": 16, "color": "#c8d4dc", "opacity": 0.5, "clip": [[372, 585], [412, 585], [412, 591], [372, 591]]},
        {"id": "puddle-2", "type": "ripples", "what": "rain ringing a puddle on a tread", "at": [440, 540], "radius": [1, 10], "flat": 0.3, "every": [0.4, 1.4], "rings": 1, "speed": 14, "color": "#c8d4dc", "opacity": 0.5, "clip": [[425, 540], [455, 540], [455, 545], [425, 545]]},
        {"id": "puddle-3", "type": "ripples", "what": "rain ringing a puddle on a tread", "at": [418, 506], "radius": [1, 8], "flat": 0.3, "every": [0.5, 1.6], "rings": 1, "speed": 12, "color": "#c8d4dc", "opacity": 0.45, "clip": [[407, 506], [429, 506], [429, 510], [407, 510]]},
        {"id": "mist-l", "type": "smoke", "what": "mist drifting between the trunks on the left, slow and wide, from the slope toward the path", "at": [120, 400], "height": 60, "width": [120, 220], "lean": [160, -20], "rise": 2, "rate": 0.5, "gust": 0.2, "color": "#c3cbd3", "opacity": 0.14, "plane": "back"},
        {"id": "mist-r", "type": "smoke", "what": "mist drifting between the trunks on the right", "at": [700, 390], "height": 60, "width": [120, 220], "lean": [-150, -24], "rise": 2, "rate": 0.5, "gust": 0.2, "color": "#c3cbd3", "opacity": 0.14, "plane": "back"},
    ]
    return {
        "id": ID, "horizon": HZ, "full": FULL,
        "light": "dusk in fine spring rain under cedars: little light, all of it cool and soft from the sky above; no sun, no cast shadows, only a soft darkening under things; the line of lamplight under the storehouse's floor the one warm thing",
        "walk": [list(p) for p in walk_outline()],
        "walk_note": "the steps from the foot of the picture (enter, isukeFrom at the bottom edge) up to the storehouse's front, and round its right side to under the window and the pipe; the ground climbs, so people shrink as they go up (the scene's horizon and full: stands give grownup_px at each mark)",
        "blocked": [[[Fg["x"] - 16, Fg["base"] - 6], [Fg["x"] + 16, Fg["base"] - 6], [Fg["x"] + 16, Fg["base"] + 4], [Fg["x"] - 16, Fg["base"] + 4]],
                    [[K["cx"] - K["rx"], K["cy"] - 10], [K["cx"] + K["rx"] + 30, K["cy"] - 10], [K["cx"] + K["rx"] + 30, K["cy"] + 6], [K["cx"] - K["rx"], K["cy"] + 6]],
                    [[LEANTO["x0"] - 4, LEANTO["post_y"] - 14], [LEANTO["x1"], LEANTO["post_y"] - 18], [LEANTO["x1"], LEANTO["post_y"] + 2], [LEANTO["x0"] - 4, LEANTO["post_y"] + 4]]],
        "planes": planes,
        "things": things,
        "marks": {k: list(v) for k, v in MARKS.items()},
        "stands": stands,
        "isukeWay": way,
        "isukeWay_note": "the constable's way up the path in #27, bottom first, ending at marks.door; he starts off the bottom edge at isukeFrom",
        "exits": [{"to": "edo-storehouse", "via": "door", "name": "the storehouse's door (once it is unbarred from inside)", "walkTo": list(MARKS["door"]), "spawn": "door"},
                  {"to": "map", "edge": "S", "name": "back down the path", "walkTo": [400, 598], "spawn": "enter", "band": "rows 560 to 600, x 300 to 520"}],
        "cutouts": {name: box_of(a) for name, (c, a) in cut.items()},
        "fx": fx,
        "fx_note": "Nothing that moves by nature is painted: the rain (ENGINE-20's kind, 'rain': its slant, density and where it is hidden are given), three drips off the eaves (streams), three puddles on the treads that ring when the rain hits them (ripples, each clipped to its puddle), the mist drifting (two wide, slow, faint smokes on the back plane). The painting's own still sheens on four treads stay under the rings.",
        "rain_is": "slant: dx -8 per 100 px down (from upper left; the lines lean right as they fall); density 0.0011 per px^2 (about 530 lines on the stage at once), each 10 to 22 px long, falling 520 px a second; hidden under the eaves (the house's walls and the ground under them) and under the lean-to's roof",
        "sizes": {name: round(grownup_px(p[1]), 1) for name, p in MARKS.items()},
    }
