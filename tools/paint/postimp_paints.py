"""The game's paint box and its keys: the colours every scene is mixed from (see postimp_key.py, and "The paints" in
docs/DESIGN.md).

The paints are the 23 of 1888 that the Post-Impressionist style study chose (the box below, in its order: the order
matters to the last digit, as the nearest-paint pull adds them up in it). The places use 21 of them; the interface's
two (canvas ground, time cyan) are never mixed into a place.

A key says, for a scene's era and hour:
  light    the paints a lit warm or neutral surface is pulled toward, as a ramp over lightness
  shadow   the paints a shadow is pulled toward, by hue family (warm/neutral, green, blue, red), as ramps over lightness
  pair     the complementary pair of the place and hour (warm paint, cool paint): the axis of the broken colour
  weight   how much each paint counts when a colour is moved toward its nearest paints (the key's own paints count more)
  ...and a few numbers that set how far each part goes at strength 100 (see postimp_look.py). The game uses 50.

Everything is in OKLab (see postimp_oklab.py). A paint is used at any lightness the way a painter uses it: darker by
adding a dark (its chroma falls with its lightness), lighter by adding lead white (it moves toward the white).

SCENE_KEY (at the bottom) says which key each scene uses: a new scene is added there (and ERA_KEY is what the game
falls back on for a scene that is not in it yet).
"""

import numpy as np

from postimp_oklab import F32, hex_to_lab

STRENGTH = 50                    # the game's strength: 0 is the painting as painted, 100 the paints at their clearest

# name, hex, group (lights, warm middles, cool middles, darks, skins, the interface), and what each is for
BOX = [
    ("lead-white", "#f6eed8", "lights"),            # The warm white of the tube: clouds, sunlit marble, a toga, the brightest stroke in a picture. Ne
    ("naples-yellow", "#f4d88e", "lights"),         # Sunlit stone and pale sand; the light side of anything warm; skin in full sun.
    ("chrome-yellow", "#f2b42e", "lights"),         # The sun's own colour and the lamp's: Dad's shirt, a lit window, the halo round a light.
    ("cerulean", "#7fb8de", "lights"),              # The sky low down, light on water, the cool light side of white things.
    ("yellow-ochre", "#d8963a", "warm"),          # Sand and stone in half light, wood, bread, rope: the middle of the warm world.
    ("chrome-orange", "#e9772b", "warm"),         # Where warm light turns: the edge of a lit form, lamp glow on a wall, a sunset, terracotta.
    ("vermilion", "#d63f2a", "warm"),             # The loudest red: the Son's cap, the temple's paint, the front door, a rug. Small amounts, set ag
    ("geranium-lake", "#c9375e", "warm"),         # Crimson-pink: Little Sister, flowers, a sunset's last band, the red of a shadow on a warm face.
    ("cobalt-blue", "#2f63b8", "cool"),           # The sky, the Son's hoodie, the shadow side of a blue thing; the main cool of a day picture.
    ("ultramarine", "#2e3a93", "cool"),           # Deep sky overhead, night, the deepest part of a shadow before it goes to the line; Big Sister's 
    ("cobalt-violet", "#8e5ea8", "cool"),         # Shadow laid on warm ground and warm stone: the complement of the sunlit yellow beside it.
    ("lilac", "#b8a2d8", "cool"),                 # Shadow in a light key (white stone in shade, haze, far hills), and the cool accent in a warm fie
    ("emerald-green", "#2fa673", "cool"),         # Leaves in light, Mom's dress, water's green; set against vermilion it sings.
    ("viridian", "#1e7461", "cool"),              # Leaf shadow, deep water, the green shadow on a face or a red wall.
    ("veronese-green", "#9ac77f", "cool"),        # Pale greens: grass in sun, haze over far fields, the cool light on skin.
    ("prussian-blue", "#1a2846", "darks"),         # The contour line round things and people, and the darkest dark in any picture.
    ("deep-violet", "#3b2452", "darks"),           # The darkest shadows that are not lines: a doorway, under a table, the night inside.
    ("burnt-sienna", "#8c3b20", "darks"),          # The warm line and the warm dark: hair, a contour on the lit side of a form, wood in shade.
    ("flesh-light", "#f2c6a0", "skins"),           # Light skin in light (the family, the senator).
    ("flesh-shadow", "#c98a5e", "skins"),          # Light skin turning from the light; its shadow is struck with veronese green or lilac, never grey
    ("flesh-deep", "#9a5a36", "skins"),            # Sun-browned and brown skin (the people of Egypt, Lot); shadow struck with cobalt violet.
    ("canvas-ground", "#e9dfc8", "ui"),         # The primed canvas: the ground of the buttons, the inventory bar, the label line.
    ("time-cyan", "#39e6e0", "ui"),             # Time itself: doors in time, the tunnel, and whatever in the interface is active. The one colour 
]
PAINTS = {name: {"hex": hx, "group": group, "lab": hex_to_lab(hx)} for name, hx, group in BOX}
WHITE = PAINTS["lead-white"]["lab"]
# the paints a place may be mixed from: everything in the box but the interface's two (canvas ground, time cyan)
SCENE_PAINTS = [n for n, p in PAINTS.items() if p["group"] != "ui"]


def paint_at(name, L):
    """The ab of a paint brought to lightness L (arrays): lighter with lead white, darker with a dark (ab scales with L)."""
    lab = PAINTS[name]["lab"] if isinstance(name, str) else np.asarray(name, F32)
    Lp, ap, bp = float(lab[0]), float(lab[1]), float(lab[2])
    L = np.asarray(L, F32)
    t_up = np.clip((L - Lp) / max(1e-3, WHITE[0] - Lp), 0, 1)          # share of white mixed in
    k_dn = np.clip(L / Lp, 0, 1)                                         # share of the paint left when darkened
    a = np.where(L > Lp, ap + (WHITE[1] - ap) * t_up, ap * k_dn)
    b = np.where(L > Lp, bp + (WHITE[2] - bp) * t_up, bp * k_dn)
    return a.astype(F32), b.astype(F32)


def ramp_at(names, L):
    """A ramp of paints over lightness: each paint at its own lightness, interpolated between them in ab;
    above the lightest, that paint with white; below the darkest, that paint darkened."""
    labs = sorted([PAINTS[n]["lab"] if isinstance(n, str) else np.asarray(n, F32) for n in names], key=lambda v: float(v[0]))
    L = np.asarray(L, F32)
    if len(labs) == 1:
        return paint_at(labs[0], L)
    a = np.zeros_like(L)
    b = np.zeros_like(L)
    Ls = [float(v[0]) for v in labs]
    lo_a, lo_b = paint_at(labs[0], L)
    hi_a, hi_b = paint_at(labs[-1], L)
    a = np.where(L <= Ls[0], lo_a, np.where(L >= Ls[-1], hi_a, 0)).astype(F32)
    b = np.where(L <= Ls[0], lo_b, np.where(L >= Ls[-1], hi_b, 0)).astype(F32)
    for v0, v1 in zip(labs[:-1], labs[1:]):
        m = (L >= v0[0]) & (L < v1[0]) & (L > Ls[0])
        t = np.clip((L - v0[0]) / max(1e-4, v1[0] - v0[0]), 0, 1)
        a = np.where(m, v0[1] + (v1[1] - v0[1]) * t, a)
        b = np.where(m, v0[2] + (v1[2] - v0[2]) * t, b)
    return a.astype(F32), b.astype(F32)


def mix(a, b, t):
    """Two paints mixed (as an OKLab colour), t of the second."""
    A = PAINTS[a]["lab"] if isinstance(a, str) else np.asarray(a, F32)
    B = PAINTS[b]["lab"] if isinstance(b, str) else np.asarray(b, F32)
    return (A + (B - A) * t).astype(F32)


# ------------------------------------------------------------------ the six keys
# light / shadow ramps list paints (or mixes) from light to dark; postimp_look.py interpolates them by lightness.
KEYS = {
    "rome-morning": {
        "title": "Rome in the morning",
        "pair": ("naples-yellow", "cobalt-violet"),
        "light": ["lead-white", "naples-yellow"],   # stone in sun: naples yellow and lead white (darker: naples yellow darkened)
        "shadow": {
            # cobalt violet and lilac, leaning to cobalt and ultramarine as they deepen (today's Rome shadows are blue-grey)
            "warm": ["lilac", mix("lilac", "cobalt-violet", 0.4), mix("cobalt-violet", "cobalt-blue", 0.3), mix("cobalt-violet", "ultramarine", 0.55),
                     mix("deep-violet", "ultramarine", 0.4), "prussian-blue"],
            "green": ["veronese-green", mix("emerald-green", "viridian", 0.5), "viridian", mix("viridian", "prussian-blue", 0.5)],
            "blue": ["cerulean", "cobalt-blue", "ultramarine", "prussian-blue"],
            "red": [mix("vermilion", "geranium-lake", 0.5), "burnt-sienna", mix("burnt-sienna", "deep-violet", 0.5), "deep-violet"],
        },
        "sky": ["lead-white", "cerulean", mix("cerulean", "cobalt-blue", 0.5), "cobalt-blue"],
        "weight": {"naples-yellow": 2.2, "lead-white": 1.6, "cobalt-violet": 2.2, "lilac": 1.8, "ultramarine": 1.2, "cerulean": 1.4,
                   "cobalt-blue": 1.3, "chrome-orange": 1.2, "yellow-ochre": 1.2, "vermilion": 1.3, "viridian": 1.3, "emerald-green": 1.1,
                   "veronese-green": 1.1, "deep-violet": 1.0, "burnt-sienna": 1.0},
        "warm_light": 0.48,      # how far a lit warm/neutral surface goes toward the light ramp at strength 100
        "shade": 0.64,           # how far a shadow goes toward its shadow ramp
        "turn": 60,              # the most a coloured thing's hue is turned toward its shadow paint (degrees, at 100)
        "snap": 0.48,            # how far every colour goes toward its nearest paints
        "chroma": 0.3,          # extra chroma at 100 (a share of today's), as paint is purer than a print
        "shade_lo": 0.20, "shade_hi": 0.44,   # lightness below which a surface is in shadow, fully / not at all
        "lift": 0.06,            # the darkest darks lifted toward prussian blue (there is no black)
        "sky_pull": 0.25,        # open sky toward the key's sky paints
        "cast": 0.55,            # how much a dark region on lit ground counts as a cast shadow (today's Rome shadows are cool already)
        "light_chroma": 0.85,    # today's sunlit stone is a strong beige: it too goes toward naples yellow
        "turn_orange": 0.20,     # where light turns into shadow it goes through orange
        "density": 0.016, "mark_len": 3, "film": 0.55, "stroke_value": 0.06, "stroke_colour": 0.045,   # the touch at 100
    },
    "egypt-noon": {
        "title": "Egypt at noon",
        "pair": ("chrome-yellow", "cobalt-blue"),
        "light": ["lead-white", "naples-yellow", mix("naples-yellow", "chrome-yellow", 0.5), "chrome-yellow", mix("chrome-yellow", "chrome-orange", 0.5)],
        "shadow": {
            "warm": ["lilac", mix("lilac", "cobalt-violet", 0.5), "cobalt-violet", mix("cobalt-violet", "ultramarine", 0.45), "deep-violet", "prussian-blue"],
            "green": ["veronese-green", "emerald-green", "viridian", mix("viridian", "prussian-blue", 0.5)],
            "blue": ["cerulean", "cobalt-blue", "ultramarine", "prussian-blue"],
            "red": [mix("vermilion", "chrome-orange", 0.4), "burnt-sienna", mix("burnt-sienna", "deep-violet", 0.5), "deep-violet"],
        },
        "sky": ["lead-white", "cerulean", mix("cerulean", "cobalt-blue", 0.55), "cobalt-blue"],
        "weight": {"chrome-yellow": 2.0, "naples-yellow": 1.8, "cobalt-blue": 2.0, "cobalt-violet": 1.8, "lilac": 1.4, "lead-white": 1.4,
                   "cerulean": 1.5, "yellow-ochre": 1.4, "chrome-orange": 1.3, "emerald-green": 1.4, "viridian": 1.3, "veronese-green": 1.1,
                   "vermilion": 1.1, "ultramarine": 1.1, "burnt-sienna": 1.0},
        "warm_light": 0.5,
        "shade": 0.7,
        "turn": 75,
        "snap": 0.5,
        "chroma": 0.34,
        "shade_lo": 0.22, "shade_hi": 0.44,
        "lift": 0.05,
        "sky_pull": 0.25,
        "cast": 1.0,             # today's Egypt shadows are warm browns: here the cast shadows are what turns violet
        "turn_orange": 0.22,
        "density": 0.016, "mark_len": 3, "film": 0.55, "stroke_value": 0.056, "stroke_colour": 0.045,
    },
    "home-night": {
        "title": "The house at night",
        "pair": ("chrome-yellow", "ultramarine"),
        "light": ["naples-yellow", mix("naples-yellow", "chrome-yellow", 0.6), "chrome-yellow", mix("chrome-yellow", "chrome-orange", 0.55), "chrome-orange"],
        "shadow": {
            "warm": [mix("cobalt-violet", "ultramarine", 0.5), "ultramarine", mix("ultramarine", "deep-violet", 0.5), mix("deep-violet", "prussian-blue", 0.5), "prussian-blue"],
            "green": [mix("viridian", "emerald-green", 0.4), "viridian", mix("viridian", "prussian-blue", 0.45), mix("viridian", "prussian-blue", 0.75)],
            "blue": ["cobalt-blue", "ultramarine", mix("ultramarine", "prussian-blue", 0.5), "prussian-blue"],
            "red": ["vermilion", "burnt-sienna", mix("burnt-sienna", "deep-violet", 0.55), "deep-violet"],
        },
        "sky": ["cobalt-blue", "ultramarine", "prussian-blue"],
        "weight": {"chrome-yellow": 2.0, "chrome-orange": 1.8, "ultramarine": 2.0, "deep-violet": 1.6, "viridian": 1.8, "emerald-green": 1.3,
                   "vermilion": 1.4, "geranium-lake": 1.1, "burnt-sienna": 1.5, "yellow-ochre": 1.5, "naples-yellow": 1.2, "prussian-blue": 1.2,
                   "cobalt-violet": 1.0},
        "warm_light": 0.5,
        "shade": 0.66,
        "turn": 55,
        "snap": 0.48,
        "chroma": 0.32,
        "shade_lo": 0.10, "shade_hi": 0.27,
        "lit_lo": 0.30, "lit_hi": 0.55,
        "lift": 0.07,
        "sky_pull": 0.25,
        "cast": 0.45,
        "cool": 0.35,            # today's house is painted in blue-greys: a cool colour here is mostly paint, not shadow
        "env_cap": 0.60,         # the lamps and the lit kitchen are lights, not lit surfaces
        "turn_orange": 0.15,
        "density": 0.016, "mark_len": 3, "film": 0.5, "stroke_value": 0.05, "stroke_colour": 0.04,
    },
    # ---- added for the whole game ----
    "lamp-interior": {
        "title": "Lamplit rooms (the gallery, the chamber, the treasury)",
        "pair": ("chrome-orange", "ultramarine"),
        "light": ["naples-yellow", mix("naples-yellow", "chrome-yellow", 0.6), "chrome-yellow", mix("chrome-yellow", "chrome-orange", 0.55), "chrome-orange"],
        "shadow": {
            "warm": [mix("cobalt-violet", "ultramarine", 0.5), "ultramarine", mix("ultramarine", "deep-violet", 0.5), mix("deep-violet", "prussian-blue", 0.5), "prussian-blue"],
            "green": [mix("viridian", "emerald-green", 0.4), "viridian", mix("viridian", "prussian-blue", 0.45), mix("viridian", "prussian-blue", 0.75)],
            "blue": ["cobalt-blue", "ultramarine", mix("ultramarine", "prussian-blue", 0.5), "prussian-blue"],
            "red": ["vermilion", "burnt-sienna", mix("burnt-sienna", "deep-violet", 0.55), "deep-violet"],
        },
        "sky": ["lead-white", "cerulean", "cobalt-blue", "ultramarine"],     # (a shaft of daylight, a lit doorway)
        "weight": {"chrome-orange": 1.8, "chrome-yellow": 1.6, "yellow-ochre": 1.6, "burnt-sienna": 1.6, "ultramarine": 1.8, "deep-violet": 1.6,
                   "prussian-blue": 1.2, "naples-yellow": 1.2, "vermilion": 1.3, "viridian": 1.2, "geranium-lake": 1.1, "cobalt-violet": 1.1},
        "warm_light": 0.48,
        "shade": 0.62,
        "turn": 55,
        "snap": 0.46,
        "chroma": 0.30,
        "shade_lo": 0.10, "shade_hi": 0.28,
        "lit_lo": 0.32, "lit_hi": 0.58,
        "lift": 0.07,
        "sky_pull": 0.25,
        "cast": 0.45,
        "cool": 0.55,            # the dark stone of the gallery is blue-grey in today's picture: a shadow, mostly
        "env_cap": 0.60,         # the lamps are lights, not lit surfaces
        "turn_orange": 0.15,
        "density": 0.016, "mark_len": 3, "film": 0.50, "stroke_value": 0.050, "stroke_colour": 0.040,
    },
    "nevada-morning": {
        "title": "Nevada in the morning",
        "pair": ("chrome-orange", "cobalt-blue"),
        "light": ["lead-white", "naples-yellow", mix("naples-yellow", "chrome-yellow", 0.5), mix("chrome-yellow", "chrome-orange", 0.5)],
        "shadow": {
            "warm": ["lilac", mix("lilac", "cobalt-violet", 0.5), "cobalt-violet", mix("cobalt-violet", "ultramarine", 0.5), "deep-violet", "prussian-blue"],
            "green": ["veronese-green", mix("veronese-green", "viridian", 0.5), "viridian", mix("viridian", "prussian-blue", 0.5)],
            "blue": ["cerulean", "cobalt-blue", "ultramarine", "prussian-blue"],
            "red": [mix("vermilion", "chrome-orange", 0.4), "burnt-sienna", mix("burnt-sienna", "deep-violet", 0.5), "deep-violet"],
        },
        "sky": ["lead-white", "cerulean", mix("cerulean", "cobalt-blue", 0.55), "cobalt-blue"],
        "weight": {"chrome-orange": 1.8, "cobalt-blue": 1.8, "chrome-yellow": 1.5, "naples-yellow": 1.5, "yellow-ochre": 1.5, "cerulean": 1.5,
                   "cobalt-violet": 1.6, "lilac": 1.4, "veronese-green": 1.3, "lead-white": 1.3, "ultramarine": 1.1, "burnt-sienna": 1.0, "vermilion": 1.0},
        "warm_light": 0.48,
        "shade": 0.66,
        "turn": 70,
        "snap": 0.48,
        "chroma": 0.30,
        "shade_lo": 0.22, "shade_hi": 0.44,
        "lift": 0.05,
        "sky_pull": 0.25,
        "cast": 0.9,
        "light_chroma": 0.7,
        "turn_orange": 0.22,
        "density": 0.016, "mark_len": 3, "film": 0.55, "stroke_value": 0.056, "stroke_colour": 0.045,
    },
    "highway-dusk": {
        "title": "The highway at dusk",
        "pair": ("chrome-orange", "ultramarine"),
        "light": ["naples-yellow", "chrome-yellow", mix("chrome-yellow", "chrome-orange", 0.5), "chrome-orange", mix("chrome-orange", "geranium-lake", 0.4)],
        "shadow": {
            "warm": [mix("lilac", "cobalt-violet", 0.5), "cobalt-violet", mix("cobalt-violet", "ultramarine", 0.5), "deep-violet", "prussian-blue"],
            "green": [mix("veronese-green", "viridian", 0.5), "viridian", mix("viridian", "prussian-blue", 0.5), "prussian-blue"],
            "blue": ["cobalt-blue", "ultramarine", mix("ultramarine", "prussian-blue", 0.5), "prussian-blue"],
            "red": ["geranium-lake", mix("geranium-lake", "cobalt-violet", 0.5), "deep-violet", "prussian-blue"],
        },
        "sky": ["lilac", "cobalt-violet", "ultramarine", "deep-violet"],
        "weight": {"chrome-orange": 1.9, "ultramarine": 1.8, "chrome-yellow": 1.5, "geranium-lake": 1.4, "cobalt-violet": 1.6, "deep-violet": 1.5,
                   "lilac": 1.2, "vermilion": 1.2, "veronese-green": 1.1, "prussian-blue": 1.2},
        "warm_light": 0.45,
        "shade": 0.60,
        "turn": 60,
        "snap": 0.45,
        "chroma": 0.24,          # today's dusk is already strong colour: less to add
        "shade_lo": 0.15, "shade_hi": 0.34,
        "lit_lo": 0.45, "lit_hi": 0.70,
        "lift": 0.06,
        "sky_pull": 0.20,
        "cast": 0.6,
        "turn_orange": 0.15,
        "density": 0.016, "mark_len": 3, "film": 0.50, "stroke_value": 0.050, "stroke_colour": 0.040,
    },
}

# The people (the rig's flat four-tone figures) take the scene's key with a few numbers of their own: small and flat,
# they need a firmer pull to the paints and a more decided coloured shade to sit in the painted picture. And the shadow
# on the ground under each (today a see-through black) becomes the key's shadow paint, laid a little thicker, so that
# it tints the ground as the picture's own shadows do instead of greying it.
PEOPLE = {"snap": 0.62, "shade": 0.85, "warm_light": 0.52, "chroma": 0.34, "turn": 40}
GROUND_SHADOW = {"rome-morning": 0.46, "egypt-noon": 0.46, "home-night": 0.30,     # the lightness of the shadow paint
                 "lamp-interior": 0.30, "nevada-morning": 0.46, "highway-dusk": 0.34}
GROUND_ALPHA_GAIN = 0.7                                                            # alpha x (1 + gain * strength)


def people_key(key):
    k = dict(key)
    k.update(PEOPLE)
    return k


# Which key each scene uses (one table: the game reads it from js/art/look-data.js, which postimp_key.py --js writes).
SCENE_KEY = {
    "highway": "highway-dusk",                                                    # the title screen and the opening movie
    "egypt-crash": "egypt-noon", "egypt-site": "egypt-noon",                      # Act One
    "egypt-gallery": "lamp-interior", "egypt-chamber": "lamp-interior",
    "rome-steps": "rome-morning", "rome-street": "rome-morning",                  # Act Two
    "rome-temple": "lamp-interior",
    "home-living-room": "home-night", "home-landing": "home-night", "home-study": "home-night",     # Act Three
    "home-lilsis-room": "home-night", "home-bigsis-room": "home-night",
    "nevada-roadside": "nevada-morning",                                          # Act Four
}
# A scene that is not in the table yet: its era's daylight key (an interior lit by lamps should be put in the table
# with "lamp-interior").
ERA_KEY = {"egypt": "egypt-noon", "rome": "rome-morning", "home": "home-night", "nevada": "nevada-morning"}


def key_for(scene):
    return KEYS[SCENE_KEY[scene]]
