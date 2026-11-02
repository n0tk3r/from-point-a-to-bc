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
        "frames": ["wagon-rear-*", "sun", "sky", "drive-*", "light-*"],     # (the sun's soft disc: keyed colour by colour, its edge kept) ROAD-18P: sky, drive-*, light-*: the drive straight ahead (its backdrop, strips of ground, sheet of things, light)
    },
    "egypt-crash": {
        "folder": "egypt1",                                         # (the painter's working name for it, in out/)
        "planes": ["palm-3", "palm-2", "palm-1", "donkey", "wagon", "mirror", "front"],
        "alt": {"suitcase-open": [], "trunk-open": [], "cooler-open": []},
        "states": {"trunk-open": ["trunk-open-1", "trunk-open-2"]},   # the trunk without the flashlight, then without the shade too
        "union": {"palms": ["palm-3", "palm-2", "palm-1"]},
        "frames": ["steam-*"],                                      # (the kites over the river are egypt-site's frames)
    },
    # CAR-13P: inside the wagon (egypt_car.py). Nobody is drawn; with the story at its start the glovebox is shut, the
    # visor up and the freshener on its string; the glovebox dropped open with the map in it replaces the shut one (and
    # emptied, without the map, is a state of it: the same painting with less in it), the visor pulled down the one up.
    "egypt-car": {"planes": ["glovebox-shut", "visor-up", "freshener"], "alt": {"glovebox-map": ["glovebox-shut"], "visor-down": ["visor-up"]},
                  "states": {"glovebox-map": ["glovebox-empty"]}, "union": {}, "frames": []},
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
    # ROME-13R1: the Forum (rome_forum.py): back to front, as the scene lays them; the awning is its own cut-out so that it
    # can stir (a sway), the hoarding is two (cut at its gateway, each with its own base), and the crane's great wheel
    # turns in painted frames
    "rome-forum": {
        "planes": ["statue-3", "statue-2", "statue-1", "castor", "puteal", "table", "awning", "hoarding", "hoarding-near", "basin", "front-base"],
        "alt": {},
        "union": {},
        "frames": ["crane-*"],
    },
    "rome-capitol": {                                               # ROME-13R2: the Capitol (rome_capitol.py): back to front, as the scene lists them
        "planes": ["altar", "chariot", "world", "parapet", "hut", "pen", "tablets"],
        "alt": {},
        "union": {},
        "frames": ["goose-*"],                                      # ROME-13R2: the sacred geese (goose-<n>, goose-grey-<n>)
    },
    "rome-tiber": {                                                 # ROME-13R3: across the Tiber (rome_tiber.py); the hens are frames
        "planes": ["well", "window-wall", "washing", "barge", "curb", "fence-corner", "fence", "landing-edge"],
        "alt": {},
        "union": {},
        "frames": ["hen-*"],
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
                                                                    # OFFICE-17A: his climb, drop, peek and pull sets (round seventeen) are frames by the same pattern
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
        "frames": ["desert-strip", "drive-*"],                     # DRIVE-16P: and the world outside for the `drive` kind (nevada_limo_drive.py)
    },
    # OFFICE-17A: outside the Office's field headquarters (office_lot.py). Back to front as the scene lays them with nobody
    # there: on the unit (on the roof) the grille and its four wing nuts (each its own, to come off one by one) and the
    # switch's lever; the door; the awning; the can by the wall; the flagpole; the limousine; the front plane. The other
    # states replace them: the grille off (and its nuts with it), the lever down, the door open, the can tipped over or
    # under the pipe, the limousine with its door open. The fan turning and the pennant stirring are frames.
    "office-lot": {
        "planes": ["grille", "nut-1", "nut-2", "nut-3", "nut-4", "switch", "door", "awning", "trash", "flagpole", "limo", "front"],
        "alt": {"grille-off": ["grille", "nut-1", "nut-2", "nut-3", "nut-4"], "switch-off": ["switch"], "door-open": ["door"],
                "trash-tipped": ["trash"], "trash-pipe": ["trash"], "limo-door-open": ["limo"]},
        "union": {},
        "frames": ["fan-*", "pennant-*"],
    },
    # OFFICE-17B: the air ducts over the Office's ground floor, a cut-away (office_ducts.py). Nothing stands in front of
    # the duct (the cut is the front), so there is no cut-out on the stage. The B-7 fan's blades are small cropped frames
    # (fan-0 .. fan-3 turning, fan-stopped still: one box and foot); the grille's view (what Ranger sees looking down
    # through a grille, an RGBA laid by the engine over the room it draws under it) is keyed colour by colour as a frame,
    # its soft alpha kept.
    "office-ducts": {
        "planes": [],
        "alt": {},
        "union": {},
        "frames": ["fan-*", "grille-view"],
    },
    # OFFICE-17C: the Comfortable Room (office_room.py). With nobody on stage: the plain grille, the thermostat at 72, the
    # intercom dark, the door shut in its frame, the corner chair, the table with the questionnaire on it, the plastic plant
    # upright, the wastebasket and the box near us. Each other state replaces its first one: Ranger's eyes at the grille, 77
    # and 81, the button lit, the door open, the plant drooping. The clock's second hand and the cooler's bubble are frames.
    "office-room": {
        "planes": ["vent", "thermostat-72", "intercom", "door", "doorframe", "chair-corner", "table", "questionnaire", "plant", "front"],
        "alt": {"vent-eyes": ["vent"], "thermostat-77": ["thermostat-72"], "thermostat-81": ["thermostat-72"], "intercom-lit": ["intercom"],
                "door-open": ["door"], "plant-droop": ["plant"]},
        "union": {},
        "frames": ["second-*", "bubble-*"],
    },
    # OFFICE-17C: Property & Effects (office_property.py). With nobody on stage: the plain grille, the door shut, the far wall
    # round Opal's window and the door (her counter and what is on it, the window's frame, the casing, the sign), the banjo in
    # its bay, the cart and the boxes near us. Ranger's eyes replace the plain grille, the open door the shut one; the receipt
    # on the counter lies over everything (until then it is not shown).
    "office-property": {
        "planes": ["vent", "door", "wall", "banjo", "front"],
        "alt": {"vent-eyes": ["vent"], "door-open": ["door"], "receipt": []},
        "union": {},
        "frames": [],
    },
    # OFFICE-17D: the Office's break room (office_breakroom.py). With nobody on stage: the grille over the fridge plain, the
    # door shut, the schedule on the board, Wendell's pie whole, the snack machine full, Jed's chair, the near table. The
    # grille with Ranger's eyes in it replaces the plain one; the door standing open replaces the shut one; the pie eaten
    # (the empty tin and the bottle cap) and the pie gone (the card fallen flat, the cap left on it) each replace the whole
    # pie; the peanuts in the tray replace the full machine, and the tray empty again is a state of that (the same painting
    # with less in it). The clock's second hand is frames.
    # PAINT-20B: Kihei's fish shop at Yui (edo_fishshop.py). Back to front with nobody on stage: the noren and the drying
    # fish (sways, at the back), the three tubs, the sushi-box stand with the box empty on it, the hearth, the baby's
    # basket, the front plane; the box filled and pressed, and turned out and cut, replace the empty one; the cat's frames.
    "edo-fishshop": {
        "planes": ["noren", "driedfish", "tub-1", "tub-2", "tub-3", "stand", "sushibox-empty", "hearth", "basket", "front"],
        "alt": {"sushibox-filled": ["sushibox-empty"], "sushibox-cut": ["sushibox-empty"]},
        "union": {},
        "frames": ["cat-*"],
    },
    "office-breakroom": {
        "planes": ["vent", "door", "schedule", "pie", "vending", "chair", "front"],
        "alt": {"vent-eyes": ["vent"], "door-open": ["door"], "pie-eaten": ["pie"], "pie-gone": ["pie"], "vending-peanuts": ["vending"]},
        "states": {"vending-peanuts": ["vending-taken"]},
        "union": {},
        "frames": ["clock-*"],
    },
    # PAINT-20A: Yui on Suruga Bay (edo_village.py). Back to front as the scene lays them with nobody there: Gonroku's
    # freighter at anchor (it bobs), the net racks, his tender at the water's edge (it bobs), the notice-board place,
    # Kihei's noren in the open front (it sways), the big boat on its props, the hen yard's fence, the front plane. No
    # other states. The hens are frames (edo_village_hens.py).
    "edo-village": {
        "planes": ["ship", "racks", "tender", "board", "noren", "boat", "fence", "front"],
        "alt": {},
        "union": {},
        "frames": ["hen-*"],
    },
    # PAINT-20C: the cedar path in rain (edo_cedars.py). With nobody on stage: the two near cedars on each side of the
    # path's foot (each with a slanted base), the two nearest trunks at the picture's edges (the front plane). The line
    # of lamplight under the storehouse's floor lies over the backdrop while the lamp below is lit.
    "edo-cedars": {
        "planes": ["cedar-l", "cedar-r", "front"],
        "alt": {"light-on": [], "window-lit": []},                  # (window-lit: the high window lit from inside, while the lantern is)
        "union": {},
        "frames": [],
    },
    # PAINT-20C: inside the storehouse (edo_storehouse.py). With nobody on stage: the lantern unlit, the sacks under the
    # window, the door shut with the bar across it, the trapdoor under the mat. Each other state replaces its first:
    # the lantern lit, the sacks heaped over the mat, the door open, the bar lifted, the mat pulled aside, the trapdoor
    # open; the floorgaps' light lies over the backdrop (under the mat) while the room below is lit.
    "edo-storehouse": {
        "planes": ["lantern", "sacks", "door", "bar", "trapdoor", "mat"],
        "alt": {"lantern-lit": ["lantern"], "sacks-heaped": ["sacks"], "door-open": ["door"], "bar-up": ["bar"], "mat-aside": ["mat"],
                "trapdoor-open": ["trapdoor", "mat"], "floorgaps-on": ["mat"]},
        "union": {},
        "frames": [],
    },
    # PAINT-20D: the castle approach at Himeji (edo_castle.py). Back to front as the scene lays them with nobody there: the
    # ladder (behind everybody), the gate (its opening clear), the scaffold, the tub, the three buckets of lime (each hidden
    # as the crew carries it: no second state), the cherry (the trunk and all its boughs: the front of the picture). The
    # herons and the egrets are frames.
    "edo-castle": {
        "planes": ["ladder", "gate", "scaffold", "tub", "bucket-1", "bucket-2", "bucket-3", "cherry"],
        "alt": {},
        "union": {},
        "frames": ["heron-*", "egret-*"],
    },
    # PAINT-20E: inside Himeji's keep, a lower floor (edo_keep.py). Back to front with nobody there: the weapon racks on
    # the right wall, the steep stairs with their rail, the great pillar, the plasterers' tubs and lime, the front plane.
    # The three beams of sun through the gun ports are LIGHT, not in the backdrop: each is a light picture (RGBA, soft
    # alpha) for the live layer, keyed colour by colour as a frame.
    "edo-keep": {
        "planes": ["racks", "stairs", "pillar", "tubs", "front"],
        "alt": {},
        "union": {},
        "frames": ["beam-*"],
    },
    # PAINT-20E: the keep's top floor at sunset (edo_keeptop.py). With nobody there and the story at its start: the
    # stairwell's rail, the stored chests, the old lantern, the three shutters seen (north, east, west) shut; the room is
    # near dark. The west shutters open replace the shut ones. The LIT ROOM is a state: `lit` is a second backdrop (the
    # whole stage) laid over everything when the west shutters are open, with the sun flooding in, and each cut-out has
    # its `-lit` twin for that state (the same painting in the sunset light). The north and east shutters open (dark, and
    # lit) replace their shut ones.
    "edo-keeptop": {
        "planes": ["rail", "chests", "lantern", "northshutter", "eastshutter", "westshutter", "front"],
        "alt": {"westshutter-open": ["westshutter"], "northshutter-open": ["northshutter"], "eastshutter-open": ["eastshutter"],
                "lit": [], "rail-lit": ["rail"], "chests-lit": ["chests"], "lantern-lit": ["lantern"], "front-lit": ["front"],
                "northshutter-lit": ["northshutter"], "eastshutter-lit": ["eastshutter"], "westshutter-open-lit": ["westshutter"],
                "northshutter-open-lit": ["northshutter"], "eastshutter-open-lit": ["eastshutter"]},
        "union": {},
        "frames": ["heron-fly-*"],                                  # the herons going past the west bay: three small flight frames
    },
    # PAINT-21A: Nishikurasawa at the foot of the Satta Pass (edo_kurasawa.py). Back to front as the scene lays them with
    # nobody there: Fuji's cap of cloud (on; hidden once it has lifted at the top of the pass), the bearers' palanquin, the
    # noren over the teahouse's door (it sways), Soshichi's trunks set down, O-Kuni's grill, the front plane. No other states.
    "edo-kurasawa": {
        "planes": ["cloud", "kago", "noren", "trunks", "grill", "front"],
        "alt": {},
        "union": {},
        "frames": [],
    },
    # PAINT-21A: the top of the Satta Pass (edo_satta.py). Back to front with nobody there: Fuji's cap of cloud (on; the
    # scene fades it out when it lifts), the bent pine (it sways), the front plane. The folded pass on the Jizo's hat is an
    # alt that lies over the picture while it is there (from the gust to when it is lifted off).
    "edo-satta": {
        "planes": ["cloud", "pine", "front"],
        "alt": {"pass": []},
        "union": {},
        "frames": [],
    },
    # PAINT-21F: inside the women's hall at sunset (edo_hall.py). With nobody on stage: the west wall with the lattice (its
    # gaps clear: Ryōkai's face shows in them from outside), the women's writing desk near us (the front plane). The DUSK
    # state (after the sun has gone) is a second backdrop over the whole stage, with the planes' -dusk twins. The light (the
    # bars on the east wall and the floor, the shafts in the air) is NOT in the backdrop: three RGBA light pictures for the
    # live layer, keyed colour by colour as frames, moved by the scene as the sun goes down (layout.json `bars`).
    "edo-hall": {
        "planes": ["lattice", "front"],
        "alt": {"dusk": [], "lattice-dusk": ["lattice"], "front-dusk": ["front"]},
        "union": {},
        "frames": ["bars-*"],
    },
    # PAINT-20F: the room under the storehouse (edo_chapel.py). With nobody on stage: the trapdoor shut, the wall props, the
    # closet altar shut, the mirror on its stand, the lamps alight, the ladder, the centre prop near us. The other states replace
    # them: the trapdoor open on the dark storehouse, and open on the morning (with the sun on the mats, on the back plane); the
    # altar open (the Kannon, the calendar, the bowl); the lamps cold; the ladder in the morning sun.
    "edo-chapel": {
        "planes": ["trapdoor-shut", "props", "altar-shut", "mirror", "lamps", "ladder", "front"],
        "alt": {"trapdoor-lamp": ["trapdoor-shut"], "trapdoor-day": ["trapdoor-shut"], "altar-open": ["altar-shut"],
                "lamps-out": ["lamps"], "ladder-day": ["ladder"]},
        "union": {},
        "frames": [],
    },
    # PAINT-21B: the ship by day (edo_deck.py). Back to front as the scene lays them with nobody there: the swell layer
    # (the far sea and the cape: it rocks on the swell), the sail (it breathes), the rigging, the mast, the windlass, the
    # tiller and the rudder's head, the compass box (shut), Kota's rice pot (the lid on), the front plane. The compass box
    # propped open replaces the shut one; the pot with its lid lifted, and the pot boiling, each replace the quiet one.
    # The floating cask is frames.
    "edo-deck": {
        "planes": ["swell", "sail", "rigging", "mast", "windlass", "tiller", "compass-shut", "pot", "front"],
        "alt": {"compass-open": ["compass-shut"], "pot-lifted": ["pot"], "pot-steam": ["pot"]},
        "union": {},
        "frames": ["cask-*"],
    },
    # PAINT-21B: the ship's clock (edo_compass.py), a close-up from above with nobody in it. The needle (still) and
    # Kanbei's thumb lie over the card and the box; the needle a hair to the left and a hair to the right replace the still
    # one (its tremble: three positions in turn).
    "edo-compass": {
        "planes": ["needle", "thumb"],
        "alt": {"needle-l": ["needle"], "needle-r": ["needle"]},
        "union": {},
        "frames": [],
    },
    # PAINT-21C: Osaka, the Dojima shore (edo_dojima.py). Back to front with nobody there: the lighter moored at the steps
    # (it bobs), the dealers and the water men at the right, O-Natsu's noren (it sways), and her stall: the sandals' heap,
    # the hearth and pot, the table with the tub, the tray of rice balls (full), the kettle; the front plane. The tray
    # emptying and empty replace the full one; the smaller heap of sandals the full one. The lighters on the river, the
    # price runner and the water men's splash are frames.
    "edo-dojima": {
        "planes": ["lighter", "market", "noren", "sandals", "pot", "stall", "tray", "kettle", "front"],
        "alt": {"tray-half": ["tray"], "tray-empty": ["tray"], "sandals-few": ["sandals"]},
        "union": {},
        "frames": ["lighter-near", "lighter-far", "runner-*", "splash-*"],
    },
    # PAINT-21C: Osaka, the merchant street at a crossroads (edo_street.py). Back to front with nobody there: the two lines
    # of prints across the print shop's open front (they flutter), the three noren (they sway), the printing bench and the
    # sheet on its stand (blank), the medicine shop's standing signboard, the road god, the water-seller. The sheet
    # printed ghost-blurred, and printed clean, replace the blank one (#30).
    "edo-street": {
        "planes": ["prints-1", "prints-2", "noren-kelp", "noren-med", "noren-comb", "bench", "print", "sign", "roadgod", "watervendor"],
        "alt": {"print-ghost": ["print"], "print-clean": ["print"]},
        "union": {},
        "frames": [],
    },
    # PAINT-21D: the Inari puppet theatre (edo_theatre.py). With nobody there and the stage empty: the black robes on their
    # peg (behind everybody), the rail along the stage's front, the lamp, the boy puppet on his stand, the masking curtain,
    # the set's gate and house front, the troupe's boxes at the front. The show is a layer over the backdrop (`show`: the
    # stage in the roof hatch's day, the audience turned to the stage), with the set's two cut-outs lit (their -show twins
    # replace them). The daylight's shafts in the air are light pictures for the live layer (frames, keyed colour by colour).
    "edo-theatre": {
        "planes": ["robes", "stagerail", "lamp", "boypuppet", "curtain", "gate", "housefront", "front"],
        "alt": {"show": [], "gate-show": ["gate"], "housefront-show": ["housefront"]},
        "union": {},
        "frames": ["shaft-*"],
    },
    # PAINT-21D: the Akashi shore (edo_akashi.py). Back to front with nobody there: the floats of the pots' lines and the
    # ladle afloat (both bob), the Awa boat coming in (it bobs; beached, its other state replaces it), Heita's boat and his
    # tub, the octopus pots, the rocks, the two shore pines (they sway), the grass at the front. The boat's approach is a
    # frame (boat-1).
    "edo-akashi": {
        "planes": ["floats", "ladle", "pilgrimboat", "heitaboat", "tub", "pots", "rocks", "pine-l", "pine-r", "front"],
        "alt": {"pilgrimboat-beached": ["pilgrimboat"]},
        "union": {},
        "frames": ["boat-*"],
    },
}


# PAINT-21E: Himeji town, Watamachi on the highway at midday (edo_town.py). Back to front as the scene lays them with nobody
# there: the two noren (sways, at the back), the school's desks, the school's front (its shutters propped open), the kitchen
# door, the salt jar, the plum jar and the cloth on the shelf, the rice pot, the pickle tub, the well, its bucket (up), the
# ward gate (open by day). The other states replace their first: the school shut up (for the night), the kitchen door open,
# the bucket down in the well, the cloth knotted round the rice balls, the gate shut (for the night).
PLANS["edo-town"] = {
    "planes": ["noren-cotton", "noren", "desks", "shutters", "kitchendoor", "saltjar", "plumjar", "cloth", "ricepot", "pickletub", "well", "bucket", "gate"],
    "alt": {"shutters-shut": ["shutters"], "kitchendoor-open": ["kitchendoor"], "bucket-down": ["bucket"], "cloth-bundle": ["cloth"], "gate-shut": ["gate"]},
    "union": {},
    "frames": [],
}


# PAINT-21E: the foot of Mount Shosha, the women's hall (edo_shosha.py), in two lights. With nobody there and the story at
# its start (the gold afternoon): the hall's doors shut, the lock on the hasp, O-Ume's rice ball on the step, the stone at
# the path's foot, the bench, the near pine (the front plane: it sways). The doors half open and open replace the shut
# ones; the lock opened replaces the shut one. SUNSET is a second backdrop: `sunset` covers the whole stage (the scene
# fades it in over back.png, under everybody), and every cut-out has its `-sunset` twin in that light, replacing its
# first state as the light changes.
PLANS["edo-shosha"] = {
    "planes": ["doors", "lock", "stepball", "stone", "bench", "pine"],
    "alt": {"doors-half": ["doors"], "doors-open": ["doors"], "lock-open": ["lock"],
            "sunset": [], "doors-sunset": ["doors"], "doors-half-sunset": ["doors"], "doors-open-sunset": ["doors"],
            "lock-sunset": ["lock"], "lock-open-sunset": ["lock"], "stepball-sunset": ["stepball"], "stone-sunset": ["stone"],
            "bench-sunset": ["bench"], "pine-sunset": ["pine"]},
    "union": {},
    "frames": [],
}


# PAINT-21E: the shipwright's lock, a close-up (edo_lock.py). With the story at its start: the middle wave in place, the
# ear with its hole dusty, the bolt through the staple (all on the back plane: nobody stands in a close-up). The others
# replace their first or lie over the picture: the ear's hole clean, the wave slid aside (the post in its recess is the
# backdrop's), the coin on the post, the post and coin turned, the slits open along the rabbit's back, the bolt drawn.
PLANS["edo-lock"] = {
    "planes": ["wave", "ear", "bolt"],
    "alt": {"ear-clean": ["ear"], "wave-slid": ["wave"], "post-coin": [], "post-turned": [], "back-open": [], "bolt-out": ["bolt"]},
    "union": {},
    "frames": [],
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
