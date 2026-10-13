"""Every scene's plan for the paints (postimp_key.py): which of its picture files are what.

A scene is keyed as the game shows it, so that a cut-out and what is round it read the same light and are mixed from the
same paints. The plan says how the game lays its files together:

  planes   the cut-outs shown with nobody on stage, back to front (front-plane things last), as the scene file's
           `planes` give them in their first state
  alt      a cut-out of another state of the story (an open lid, the open piano, a mirror once it is set), and which
           first-state cut-outs it replaces when it shows (most simply lie over the picture)
  states   further states of an alt (the open trunk as the story empties it): each keyed from the picture in that state
           as the alt is, with the alt's replacements, but left out of the palette's sample: it is the same painting
           with less in it, so its colours are the alt's, and adding one leaves the scene's other files as they were
  union    a file that is other cut-outs put together (made as their union, from the same painting)
  frames   small pictures of things that move (birds, the cat, steam, the kites, the wagon from behind): keyed colour by
           colour, their shapes untouched (file name patterns)

Every picture file of a scene must be in its plan (postimp_key.py stops at one that is not), so that nothing is
installed unkeyed by mistake. A new scene, or a new cut-out, gets its line here, and its key in postimp_paints.SCENE_KEY.
"""

import os

import numpy as np
from PIL import Image

from postimp_oklab import F32

PLANS = {
    "highway": {                                                    # the title's stage: the sign has changed its mind (round twelve: the board saying POINT B.C.)
        "planes": ["sign-bc"],
        "alt": {},
        "union": {},
        "frames": ["wagon-rear-*", "sun"],                         # (the sun's soft disc: keyed colour by colour, its edge kept)
    },
    "egypt-crash": {
        "folder": "egypt1",                                         # (the painter's working name for it, in out/)
        "planes": ["palm-3", "palm-2", "palm-1", "donkey", "wagon", "mirror", "front"],
        "alt": {"suitcase-open": [], "trunk-open": [], "cooler-open": []},
        "states": {"trunk-open": ["trunk-open-1", "trunk-open-2"]},   # the trunk without the flashlight, then without the shade too
        "union": {"palms": ["palm-3", "palm-2", "palm-1"]},
        "frames": ["steam-*"],                                      # (the kites over the river are egypt-site's frames)
    },
    "egypt-site": {
        "planes": ["awning", "sledge", "streamers", "front"],
        "alt": {"shade": []},                                       # the windshield shade, once the guard holds it
        "union": {},
        "frames": ["kite-*"],
    },
    "egypt-gallery": {
        "planes": ["front"],
        "alt": {"mirror-top": [], "mirror-foot": []},              # the mirrors, once they are set
        "union": {},
        "frames": [],
    },
    "egypt-chamber": {
        "planes": ["bench", "mirror", "front"],                     # the copper mirror on the bench, until it is traded
        "alt": {},
        "union": {},
        "frames": [],
    },
    "rome-street": {
        "planes": ["awning", "fountain", "laundry-lines"] + [f"laundry-{i}" for i in range(1, 13)] + ["tunic", "front"],
        "alt": {},
        "union": {"laundry": ["laundry-lines"] + [f"laundry-{i}" for i in range(1, 13)]},
        "frames": ["cat-*", "pigeon-*", "sparrow-*", "swallow-*"],
    },
    "rome-steps": {
        "planes": ["columns", "altar", "tripod", "stone", "cage-front", "front-base", "laurel"],
        "alt": {},
        "union": {"front": ["front-base", "laurel"]},
        "frames": ["hen-*", "pigeon-*", "swallow-*"],
    },
    "rome-temple": {
        "planes": ["table", "front"],
        "alt": {},
        "union": {},
        "frames": [],
    },
    "home-living-room": {
        "planes": ["piano", "armchair", "pencil", "table"],
        "alt": {"piano-open": ["piano"]},                           # the open piano replaces the shut one
        "union": {},
        "frames": [],
    },
    "home-landing": {
        "planes": ["ladder", "rail"],
        "alt": {"study-open": []},                                  # the study door standing open
        "union": {},
        "frames": [],
    },
    "home-study": {
        "planes": ["desk", "screen-offline", "note", "tape-out", "front"],
        "alt": {"screen-login": ["screen-offline"], "screen-map": ["screen-offline"], "vault-open": []},
        "union": {},
        "frames": [],
    },
    "home-lilsis-room": {
        "planes": ["fort", "flashlight", "teaparty", "front", "mobile"],
        "alt": {},
        "union": {},
        "frames": [],
    },
    "home-bigsis-room": {
        "planes": ["desk", "front"],
        "alt": {},
        "union": {},
        "frames": [],
    },
    "nevada-roadside": {
        "planes": ["pump", "stand", "car", "front"],
        "alt": {"shade-held": []},                                  # NEVADA-12A: the sun shade, once Grandpa Joe holds it up
        "union": {},
        "frames": ["bird-*", "limo-*", "ranger-*-[0-9]"],           # NEVADA-12A: the limousine (PAINT-12A) and Ranger's frames (PAINT-12C; his portraits are the interface's, in art/portraits)
    },
    "nevada-store": {                                               # NEVADA-12B: the store's inside (nevada_store.py)
        # back to front: the five hats on their pegs (the scene hides today's), the back door's frame (the hens and Little
        # Sister on the step are behind it), Harold, the counter, the spinner, the rock bins; the front plane last
        "planes": ["hat-1", "hat-2", "hat-3", "hat-4", "hat-5", "doorframe", "cooler", "counter", "spinner", "rockbins", "front"],
        "alt": {"window-shade": [], "mirror-shades": []},           # the sun shade (until it is given), the last mirror shades (until bought)
        "union": {},
        "frames": ["hen-*", "egg-dust", "roller-*", "tv-*"],       # the hens and the egg, the roller turning, the TV's snow
    },
    # NEVADA-12C: inside the limousine, driving (Act Five opens here). With nobody on stage the divider is up and our own
    # seat is the foreground; everything that changes or goes is an alt: the divider slid down (it replaces the glass),
    # the ropes (four strands; three, two and one are states of it, the same painting with less of the bow in it), and
    # the bag, the clipboard and the juice box (each goes when taken). The desert strip behind the windows is a frame.
    "nevada-limo": {
        "planes": ["divider-up", "front"],
        "alt": {"divider-down": ["divider-up"], "ropes-4": [], "bag": [], "clipboard": [], "juice": []},
        "states": {"ropes-4": ["ropes-3", "ropes-2", "ropes-1"]},
        "union": {},
        "frames": ["desert-strip"],
    },
}


def path(folder, name):
    return os.path.join(folder, name + ".png")


def load_rgba(p):
    return np.asarray(Image.open(p).convert("RGBA"), F32) / 255.0


def load_rgb(p):
    return np.asarray(Image.open(p).convert("RGB"), F32) / 255.0


def over(dst, rgba):
    a = (rgba[..., 3:4] >= 0.5).astype(F32)                               # the game's cut-outs are hard-edged
    return dst * (1 - a) + rgba[..., :3] * a


def picture(folder, plan, extra=None, without=()):
    """The scene's back with its first-state cut-outs laid on it (+ `extra` cut-outs laid over, `without` left out)."""
    img = load_rgb(path(folder, "back"))
    for name in plan["planes"]:
        if name in without:
            continue
        img = over(img, load_rgba(path(folder, name)))
    for name in extra or ():
        img = over(img, load_rgba(path(folder, name)))
    return img


def alpha(folder, name):
    return load_rgba(path(folder, name))[..., 3] >= 0.5
