# The painter

Every background in the game, every cut-out that stands in one, and every inventory picture is painted by the
Python scripts in this folder. Nothing here runs in the browser: the scripts write PNG files, and the PNG files
are what the game shows (`art/scenes/<scene>/`, `art/items/`).

They need Python 3 with `numpy` and `Pillow`, and nothing else. The exceptions: `people_on.py` (and the scripts
that call it) needs the game running and Playwright (see "Painting a room"), and the paints (`postimp_key.py`, which
`install.py` runs) need OpenCV as well (`pip install opencv-python-headless`): see "The paints".

```
cd tools/paint
python3 rome_street.py fast     # a quick look: skips the brush pass (about 15 seconds)
python3 rome_street.py          # the full passes (a minute or two): writes out/rome-street/
python3 install.py rome-street  # keys out/rome-street/ in the game's paints and copies it into art/scenes/rome-street/
python3 ../stamp.py             # then stamp the pages, as after any change (see docs/DESIGN.md)
```

`out/` is scratch space and is not kept in the repository.

## The look

Hand-painted backgrounds in the manner of the adventure games of the early 1990s: 800x600, a limited palette, a
little speckle where neighbouring colors meet, as a scanned painting has. All of it is original. Other people's
pictures are looked at for technique and light only, never copied, and none are kept in this repository.

What makes a picture read as painted and not as computer graphics:

- **Light has a direction and a temperature.** Sunlit planes are warm, shaded planes are cool, and everything that
  stands on the ground throws a shadow the right way. Indoors, each lamp makes a warm pool and the corners fall
  away into cool dark. Each script states its light at the top and keeps to it.
- **Three big tones.** A clear dark mass, a middle and a light, arranged to lead the eye to what matters.
- **Depth by color.** Far things are paler, bluer and lower in contrast; near things are deeper and warmer.
- **Crisp where it is built, soft where it is air.** Sky, haze, water and sand may be soft. Anything made has hard
  edges and joints, drawn after the brush pass.
- **No smooth gradients, no ruled edges, no identical repeats.** Edges wobble; every repeated thing varies.
- **Skies are painted:** clouds with lit tops and shaded bases. Never bands, never a plain gradient.
- **Detail that tells the story of the place,** while the floor where people walk stays clear.

## How a picture is made

Pictures are float arrays (height, width, 3), values 0 to 1. Each scene script works in four passes:

1. **under()** blocks in everything broad and soft: sky, big planes of wall and floor, large forms and their light.
2. **strokes()** (`brush.py`) repaints that with visible brush marks, largest brush first.
3. **details()** restates every hard thing crisply over the brushwork, then adds the small crisp things: joints,
   planks, leaves, handles, lettering, highlights, stones on the ground. Most of the work is here.
4. **finish()** adds pigment grain and reduces the picture to a limited palette with speckle: an 8-bit PNG.

## The paints

Every scene is mixed from one box of paints in a key for its era and hour (the look chosen on 9 October:
docs/DESIGN.md, "The paints"). A scene's script paints it as before, into `out/`; `install.py` then keys it on the
way into `art/`, at the game's strength, 50: the picture is kept exactly (every shape, edge and detail), and its colours
are moved toward the box (shadows a colour instead of grey or brown, lights warmed, a few short marks laid along the
forms). Every cut-out keeps its exact edge, the frames of things that move keep their shapes, and a scene's files
share one palette of 255 colours.

- `postimp_paints.py`: the 23 paints, the six keys and every number, and `SCENE_KEY`, the table of which scene uses
  which key (one table: the game reads it from `js/art/look-data.js`).
- `postimp_plans.py`: each scene's plan: which of its files are cut-outs (in the scene file's order), other states,
  unions and frames. Every picture file of a scene must be in its plan, so nothing goes in unkeyed by mistake. A
  further state of a cut-out that is the same painting with less in it (the open trunk as Dad empties it: `states`)
  is keyed like the cut-out but kept out of the palette's sample, so that adding one changes no other file.
- `postimp_key.py`: keys a scene (`install.py` calls it); `--js` writes `js/art/look-data.js` for the game's people
  and moving things (after adding a scene or changing a key); `--check` checks every scene's pictures against
  `postimp_keyed.json`, which notes what each installed file was keyed from.
- `postimp_look.py` (the keying itself) and `postimp_oklab.py` (colour arithmetic).

A new scene, or a repainted one:

```
python3 rome_forum.py              # paints out/rome-forum/, as ever
#   give it a plan in postimp_plans.py, and its key in postimp_paints.SCENE_KEY
#   (outdoors: its era's key; a room lit by lamps: "lamp-interior")
python3 install.py rome-forum      # keys it at 50 and installs it
python3 postimp_key.py --js        # (a new scene or key) the game's copy of the table
python3 postimp_key.py --check     # every scene keyed, the table current
python3 ../stamp.py
```

Never key a picture twice: `install.py` always starts from the painting in `out/`, and `--check` says if a file in
`art/` was changed after it was keyed. (`python3 install.py --raw <scene>` installs a painting without the paints, to
compare; never leave it so.) The paintings as they were before the paints are in the repository's history (before 9
October). The pictures in the game were keyed with numpy 2.5.3, Pillow 12.3.0 and OpenCV 5.0.0; another version of
OpenCV may differ in a few pixels.

## People are not painted in

The game draws them (`js/art/`). A grown-up is 160 pixels tall with feet on the scene's row `full`, and smaller
toward `horizon` in proportion. `persp.Camera(horizon, full)` is a camera that matches those two numbers, in
centimetres, so furniture, doors and steps come out the right size for the people who will stand beside them.
The rooms of the house go further: each is painted whole through one camera of this kind, which can stand
anywhere in the room and turn (`room.View`: see "Painting a room", below).

## Cut-outs

The game sorts painted cut-outs with the people (see "planes" in docs/DESIGN.md). A cut-out is a PNG the size of
the whole picture, clear except for the thing, with hard edges, so it needs no placing.

- Anything a person can stand behind is a cut-out with a baseline: the row (or slanted line) where it meets the floor.
- Anything at the very front that people always pass behind is a cut-out on the front plane.
- Anything that changes with the story is its own cut-out for each state, pixel-aligned with the backdrop.
- The backdrop is painted complete under every cut-out.
- Light (a door in time, a beam, a glow) is never painted. The game draws light live.

A thing the game moves or scales (the wagon in the opening) is cropped to its own box, with its foot point given.

## layout.json

Each scene script also writes `layout.json`: the numbers measured from the finished picture that the scene file
needs (depth, the walk outline, blocked ground, each cut-out's baseline, the shape and standing place of every
thing, exits, marks for people). The scene file in `js/content/scenes/` is the authority once the scene is wired;
where it differs from `layout.json` on purpose, the act's puzzle document says why.

<!-- MAP-15D -->
## Maps

The map screen (docs/DESIGN.md, section 8, "The map, and the Timer") shows one map for each place the story goes, each
the kind of map its own time would make (section 9, "The maps"). A map is painted like a scene, by a script of its own
with this kit and in the four passes, but it belongs to the interface, as the inventory pictures do: every colour is
mixed from the paint box by name (`postimp_paints.PAINTS[name]["hex"]`, with `brush.rgb` and `lerp`), and it is never
keyed. What is painted is what the map screen shows.

- **The pictures.** Each is 800x600, the whole stage, which the map screen lies over. The sheet lies within x 32 to 768
  and y 128 to 572; rows 0 to 127 (the band: the time, the small dial, the maps' names, Close) and 572 to 599 (the label
  line) are clear in every file. Each is an 8-bit palette with one clear colour and hard edges (`brush.save`, its alpha a
  mask), and one palette serves all of a map's files (`brush.palette_of` over the sheet with every place and way laid on
  it, then `to_palette` for each file), so that a place's paper is the sheet's exactly. A map's files come to 1.5 MB at
  most.
- **The files**, in `out/map-<map>/`, installed into `art/maps/<map>/`: `back.png`, the sheet and the lie of the land
  that anyone would know before setting foot there (a river, a hill, the walls of the house, the highway), never a place
  or a way; `place-<id>.png` for each place and `path-<a>-<b>.png` for each way (a and b in the order of
  `js/content/maps.js`), clear but for that thing's drawing; and `layout.json`.
- **`layout.json`**, measured from the finished pictures by the map's `_layout` script: `sheet`, the material's box;
  `label`, how the engine writes the place names in Koine Road (`color`, `halo` or null, `upper`, `spacing` in em, `size`
  13 to 18); for each place its `picture`, its `shape` (at most 24 points round its drawing: what is clicked), its `pin`
  (where the portraits stand, a row of discs 36 across and 4 apart centred on it: room for two on Egypt's and Rome's maps,
  three on the house's and Nevada's) and its `label`, the middle of the name's baseline, with `label_max` (the name's box:
  that wide, 20 above the baseline, 5 below); for each way its `picture` and its `via`, a line along its drawing from a's
  pin to b's, which the portrait walks. The engine draws a place not visited yet at 0.28 opacity: see that it reads as
  "not yet" at that, and is plainly gone at 0. A map with no `layout.json`, or one the page does not list yet, is drawn
  by the engine as a sketch.

The five, each with its `_kit`, `_layout` and `_check` beside it (their rows in "The files" say more): <!-- OFFICE-17B: five with the Office's -->

- `map_egypt.py`: Egypt, a scribe's sketch on papyrus with a reed pen (black ink, red, thin washes).
- `map_rome.py`: Rome, a wax tablet in its wooden frame, the plan scratched with a stylus.
- `map_home.py`: the house, Dad's pencil floor plan on squared paper.
- `map_nevada.py`: Nevada, Grandpa Joe's fold-out road map, printed in a few flat inks.
- `map_office.py`: the Office, a blueprint of its ground floor, white lines on the print's blue (round seventeen). <!-- OFFICE-17B -->

```
python3 map_rome.py fast         # a quick look: no brush pass
python3 map_rome.py              # the full passes: out/map-rome/ and its layout.json, then its check (the house's: run it)
python3 map_rome_check.py        # the checks again, and the four pictures to look at
python3 install.py map-rome      # copies out/map-rome/ into art/maps/rome/, as painted
python3 ../stamp.py              # until the page lists a map's files, the engine draws its sketch
```

A new map needs its entry in `install.py` (`"map-<map>": "maps/<map>"` in `PLACES`, and `"map-<map>"` in `SCENES`).
What a map's `_check` holds: exactly the places and ways of `js/content/maps.js`, every file there, 800x600, a palette
with a clear colour; the clear rows, the sheet's box, the size; each shape at most 24 points, on the sheet, holding at
least 90 per cent of its drawing's painted pixels, no two overlapping; each pin row on the sheet, no two within 8 pixels;
each name's box on the sheet, clear of every pin row, every other name, every other place's drawing and every way, and the
name fitting it (Koine Road at the label's size and spacing, as Pillow measures it); each `via` from a's pin to b's,
within 6 pixels of its drawing. Some hold more (no two drawings overlapping, in Rome's and the house's; how plainly each
place shows at 0.28, in Nevada's). Each writes, into `out/map-<map>-check/`, `all.png` (everything, the names in the
label's style, grey discs at the pins), `none.png` (the sheet alone), `first.png` (the act's first place visited, its
neighbours faint) and `layout.png` (`all.png` with every shape, pin row, name box and via drawn over it). Look at all four.

## Painting a room

The five scenes of the house (`home-living-room`, `home-landing`, `home-study`, `home-lilsis-room`,
`home-bigsis-room`) are interiors. An interior is painted through one camera, with `room.py` and three small tools
beside it.

### Why one camera

A room looks flat when its parts are drawn from different places: the back wall face-on across the whole picture,
the ceiling seen from below, the floor seen from high above, the furniture in a projection of its own. Then nothing
runs to a vanishing point and nothing recedes. The first painting of the living room was made like that, and looked
flat. So each room is seen through one camera, and everything in the picture goes through it: floor, walls,
ceiling, stairs, every piece of furniture, every shadow and every pool of light.

The camera is worked out from the scene's own `horizon` and `full`, the two numbers the game sizes people by. A
grown-up, 175 cm, is 160 pixels tall with feet on the row `full` and nothing at the row `horizon`; that fixes how
high the lens is above the floor: (`full` - `horizon`) x 175 / 160 cm, about 3.3 m in the living room and 3.5 m in
the rooms under the roof. The people the game draws then stand in the painted room at the right size anywhere on
its floor, with nothing to adjust.

### `room.View`

A room is measured in centimetres: X across, left to right along the back wall; Y up from the floor; Z out from the
back wall toward us (the back wall is Z = 0). A door is about 205 high and 85 wide, a table 76, a chair seat 46, a
kitchen counter 90, a step 18 high and 25 deep, a ceiling 270; a grown-up is 175, the seven-year-old 118.

```python
from room import View
v = View(horizon=150, full=455, cam=(620, 1150), yaw=-18, focal=680)    # the living room's camera
```

`cam` is where the camera stands on the floor plan (X, Z). `yaw` turns it, in degrees, positive to the right: at 0
it looks square at the back wall and the side walls run to one vanishing point; 20 to 35 is a corner view, with
two. `focal` is the lens in pixels: larger is narrower and flatter. The height of the lens is not chosen: it
follows from `horizon` and `full`.

| Call | Gives |
| --- | --- |
| `v.pt(X, Y, Z)` | the point of the picture that shows a place in the room |
| `v.person(X, Z)` | where the feet of a grown-up standing there are in the picture, and how tall they are in pixels (a third number gives another height, in cm) |
| `v.poly(points)`, `v.line(p, q)` | a polygon or an edge in the room as picture points, cut off where it passes behind the lens |
| `v.box(X0, X1, Y0, Y1, Z0, Z1)` | the faces of a box that the camera can see, the farthest first, each with its name and its normal (for lighting) |
| `v.stairs(...)` | a flight of stairs, as one box for each step |
| `v.floor_xz(shape)` | for every pixel, the place on the floor it shows (X, Z, and a mask of where the floor is seen); with `Y=`, the same for any level plane, such as a ceiling |
| `v.plane_uv(shape, axis, at)` | the same for an upright wall: `"Z"` for a wall that faces us (u is X), `"X"` for a side wall (u is Z); v is the height |
| `v.depth_map(shape)` | how far away the floor is at every pixel, for haze and for light that fades |
| `v.vanishing()`, `v.floor_at(x, y)` | where lines running back and lines running across meet; the place on the floor under a point of the picture |

### The model

Each room has a model, `<scene>_model.py`: a short file of measurements, read by the room's script and by the two
skeleton tools below. It defines:

- `ID`, the scene id, and `VIEW`, the camera (the arguments of `View`);
- `ROOM`: `X=(left, right)`, `Z=(back, front)` and `H`, the height of the walls;
- `SLABS` and `BOXES`, each `(id, X0, X1, Y0, Y1, Z0, Z1)`: floors, galleries and built-in blocks; the furniture;
- `FLATS`, each `(id, wall, u0, u1, v0, v1)`: flat things on a wall, such as doors, frames and windows;
- `STAIRS`, `POLYS` and `FLOORS`: stairs; other flat parts of the shell, such as a slope of the roof; floors at
  other levels;
- `MARKS`, `{name: (X, Z)}`, where people stand, and `WALK`, the outline of the floor they may stand on.

The full list is at the top of `room_plan.py`. A model can carry more for its own script: the living room's lists
its lamps, and the Retreat's gives the height of its sloping ceiling at any depth (`roof(Z)`).

**The camera numbers in `VIEW` belong to the scene file.** `horizon` and `full` are the scene's own, and every
place in the scene file (the walk outline, the stand places, the base lines) was measured through the whole
camera. Change any of them, `cam`, `yaw` and `focal` included, and everything in the picture moves: the scene file
must then be measured again. The shell (walls, stairs, landing, roof) is fixed with them. The furniture is the
painter's: move it, add to it, split a box into the real pieces of a chair, and then change the model to match what
is painted, so that the skeleton, the picture and `layout.json` agree.

### The skeleton

Draw the room through its camera before painting anything:

```
mkdir -p out
python3 room_plan.py home_study_model out/home-study-plan.png         # the skeleton
python3 room_layout.py home_study_model out/home-study-model.json     # its numbers, in picture pixels
```

`room_plan.py` draws the model as flat-shaded boxes, with stand-in people on the marks at the size the game will
draw them (the children at their own heights), the walk outline, and the rows `horizon` and `full`. If the skeleton
does not look like a deep room with people of the right size in it, no painting will mend it: change the model and
look again. `room_layout.py` writes the marks, the walk outline and the box of every thing in picture pixels:
provisional numbers, for a scene file that is written while the room is being painted. The `layout.json` measured
from the finished picture replaces them. (Give `room_layout.py` an output path: the folder it writes to by default,
`plans/`, is not in the repository.)

### The game's people in the picture: `people_on.py`

```
python3 people_on.py <picture.png> <horizon> <full> "<who>|<x>|<y>[|<yaw>];..." <out.png> [front.png ...]
```

`people_on.py` stands the game's own figures on any picture, at exactly the size the game will draw them there.
`who` is a person's id (`mom`, `bigsis`, `lilsis`, `dad`, `son`, ...), `x` and `y` are where their feet are, and
`yaw` is which way they face (0 toward us, the default; 180 away; 90 and 270 sideways). Pictures named after
`out.png` are laid over the people, as front-plane cut-outs are. Stand people at the back of the finished room, in
the middle and at the front, and look: this is the test that matters. It draws the figures with the game's own
code, so it needs the game running on port 8765 (`python3 tools/serve.py 8765`, from the top of the repository)
and Playwright with its Chromium (`pip install playwright`, then `playwright install chromium`). The rooms'
`_people.py` scripts, and the living room's `home_living_room_check.py`, stand the family at the room's own marks
and stand places; the full runs of the study and of the Retreat end by doing so.

### Painting through the camera

1. **Surfaces, pixel by pixel.** `floor_xz` and `plane_uv` give the place in the room that every pixel shows.
   Paint each surface in its own measurements: floorboards 12 cm wide running back, with a butt joint every metre
   or two; a rug as a rectangle on the floor; wallpaper stripes every 9 cm; a chair rail at 95; skirting 12 high;
   rafters every 60. Every line then runs to its vanishing point by itself, exactly. A sloping plane such as a roof
   is done the same way: meet each pixel's ray with the plane, as `plane_uv` does for an upright wall (the study's
   and the Retreat's kits do this).
2. **Things, as boxes.** Build every piece of furniture from `box` and `poly`: a table is a top and four legs, an
   armchair a seat, a back, two arms and a cushion, a bookcase a carcase with shelves and books. Round the corners
   and wobble the edges afterwards, in the details pass. Nothing is drawn flat, face-on or from another height, not
   even a small thing: that is what made the first living room look wrong.
3. **Light with a place in the room.** Each lamp has a place (X, Y, Z) and lights every surface from there:
   brightness falls with distance and with the angle at which the light strikes (every pixel of a surface has its
   X, Y and Z, and every face its normal). A lamp's pool on the floor then comes out as a true ellipse, a wall glows
   near a lamp and falls away from it, and the far corners go cool and dark. Lamplight is warm; what no lamp reaches
   is blue-violet. Moonlight through a window is pale blue and lies on the floor as the window's own shape,
   slanted: project the window's corners along the moon's direction onto the floor, and paint that polygon.
4. **Shadows with a place in the room.** Everything that stands on the floor throws a shadow away from the nearest
   lamp: project the corners of its top along the line from the lamp onto the floor, through `poly`, and darken
   there, softly at the edge and most where the shadow meets the thing. Add contact shadows under legs and along the
   skirting. People will stand on this floor, and on a floor without shadows they float.
5. **Depth by tone as well as by line.** The far end of a room is a little cooler, paler in its lights and closer
   in value; the near corners hold the deepest, warmest darks in the picture. At every depth something overlaps
   something else: a newel post across the landing, a lamp across a wall, a chair in front of a table.
6. Then the passes of "How a picture is made": the brush pass at interior sizes (`sizes=(9, 5, 2)`, `keep` 0.30 to
   0.40), the details, the finish.

### The foreground

The camera stands high so that the floor people walk on is broad. People may walk down to about 50 rows below
`full` and no lower, or they would be giants, so the bottom of the picture is foreground: things that stand near us
and are cut off by its bottom edge (the back of an armchair, the end of a table, a heap of luggage, a door frame),
painted darker and warmer than the middle of the room, as front-plane cut-outs that people pass behind. Never leave
bare floor along the bottom edge. A good foreground is half of what makes a room look deep.

### Cut-outs and `layout.json` in a room

All of "Cut-outs" and "layout.json" above holds, and:

- A thing people can walk behind has as its `base` the line where its front meets the floor. Through a turned camera
  that line is slanted: give it as `[[x1, y1], [x2, y2]]`, taken from `v.pt(X, 0, Z)` of the two front corners of
  its footprint. People whose feet are above the line are drawn behind the thing.
- The ground a thing takes up (its `solid`, or its outline in `blocked`) is `v.poly` of its footprint.
- Lettering that must be read (a notice, a sampler) is at least 7 pixels high, and is laid on its wall through
  `plane_uv` so that it lies in the wall's perspective.
- A room's `layout.json` also carries `view`, the model's `VIEW`. Its `walk` keeps at least 14 pixels clear of the
  walls, and of the front edge where people would be more than about 200 pixels tall. Its `marks` give a place for
  each of the three for every way into the room, a comfortable step apart and none in front of another's face.

## The files

The library, shared by every scene:

| File | What it holds |
| --- | --- |
| `brush.py` | color, noise, soft shapes, `Sheet` (many small strokes laid at once), light and shadow, the brush pass, grain, the palette |
| `sky.py` | the open sky, cumulus clouds lit and shaded, wisps |
| `land.py` | ground in perspective, sand, water, haze, shadows (including the true shadow of a cut-out), rocks, cliffs |
| `flora.py` | palms, reeds, papyrus, scrub |
| `build.py` | pyramid faces in courses, ramps, blocks, huts, boats |
| `solid.py` | `Draft`: a solid thing drawn in its own measurements (the wagon) |
| `persp.py` | `Camera`: true perspective tied to the game's depth numbers; paved floors |
| `letter.py` | lettering for signs and inscriptions, with the game's own Koine Road font or Pillow's plain face |
| `comp.py` | lays a scene's finished pictures together to look at |
| `install.py` | keys a painted scene in the game's paints and copies it into `art/` |
| `postimp_key.py`, `postimp_plans.py`, `postimp_paints.py`, `postimp_look.py`, `postimp_oklab.py` | the paints: see "The paints" |
| `postimp_keyed.json` | what each installed picture was keyed from, and what it became (`postimp_key.py --check`) |

For the rooms of the house (see "Painting a room"):

| File | What it holds |
| --- | --- |
| `room.py` | `View`: one camera for a whole room, worked out from the scene's `horizon` and `full` |
| `room_plan.py` | draws a room's model through its camera as a skeleton, with stand-in people at the game's sizes |
| `room_layout.py` | a room's marks, walk outline and things from its model, in picture pixels: provisional numbers for a scene file |
| `people_on.py` | stands the game's own figures on any picture, at the size the game draws them there (needs the game running, and Playwright) |

One script to a scene, some with helper files named after it: `_kit` (the scene's own tools), `_things`, `_props`,
`_check` (checks on the finished pictures: most draw `layout.json` over them), `_look`. A room also has `_model`
(its measurements), and can have `_layout` (writes `layout.json`) and `_people` (the game's figures standing in
the finished room).

| Script | Paints | Into |
| --- | --- | --- |
| `highway.py` | the highway at dusk, the sun, the sign's two changes, the wagon from behind | `art/scenes/highway/` |
| `highway_drive.py` (with `_kit`: the camera, the strips, the loop's and the stop's numbers; `_world`: the painting's world in metres, read out of `highway.py`'s own code, and its things drawn again one at a time; `_sky`: the backdrop and the light; `_ground`: the road and the desert from above; `_things`: the sheet; `_check`: the checks, and the chase view drawn as the engine draws it, cruising, stopped beside `back.png`, and the title's) | the highway at dusk to be driven down, for the engine's `drive` seen straight ahead (ROAD-18), all of it by `highway.py`'s own code: `sky.png` (the backdrop: the sky, the mesas and the far plain, nothing standing); `drive-road.png` (the road and its shoulders from straight above, 48 px a metre, 64 m long, end to end, the painting's own cracks, patches and dashes where the camera stops) and `drive-desert-l/-r.png` (6 to 30 m out, 24 px a metre) and `drive-far-l/-r.png` (30 to 150 m out, 8 px a metre), the brush field lying in them as round dark clumps with their gold tops and their own shade, seen from straight above, in the painting's drifts (PAINT-18B); `drive-things.png` and `.json` (the pole, the reflector post, fence posts, sagebrush near and far, grass, stones, Joshua trees, the tumbleweed, the jackrabbit, a bird, the two signs at the painting's own size at 17.3 m, and every thing of the painting cut out of it, the strip of tire, the bottle and the hubcap among them); `drive-stop.json` (where they stand when the camera stops: 820); `light-shade.png` and `light-glow.png` (the painting's light and colours by distance, still on the stage: multiply, then screen). Keyed as the scene's frames (`python3 install.py --keep-palette highway`; it keys `back.png` and `sign-bc.png` again too, a few pixels apart on another OpenCV: put those two back as they were, and their lines in `postimp_keyed.json`), the scene's other files byte for byte as they were <!-- ROAD-18P --> | `art/scenes/highway/` |
| `egypt1.py`, `wagon.py`, `egypt1_donkey.py`, `egypt1_steam.py` | where the wagon came down: backdrop, palms, the wagon and its states (the driver's window rolled down, the inside of the car seen through it: round thirteen <!-- CAR-13P -->), the donkey, steam | `art/scenes/egypt-crash/` |
| `egypt_car.py` | inside the wagon, from the driver's seat, one afternoon, through one camera (nobody drawn): the glovebox shut, open with the map and empty, the visor up and down, the air freshener; the sand, the river and the sky through the glass (`egypt_car_world.py`); its model, kit, things, painted props, layout and check in `egypt_car_*.py` <!-- CAR-13P --> | `art/scenes/egypt-car/` |
| `egypt_site.py` | the foot of the pyramid | `art/scenes/egypt-site/` |
| `egypt_gallery.py` | the great gallery | `art/scenes/egypt-gallery/` |
| `egypt_chamber.py` | the burial chamber | `art/scenes/egypt-chamber/` |
| `rome_street.py` | the street to the Forum | `art/scenes/rome-street/` |
| `rome_steps.py` | the steps of the temple | `art/scenes/rome-steps/` |
| `rome_temple.py` | inside the temple | `art/scenes/rome-temple/` |
| `rome_forum.py` (with `rome_forum_model.py`, `_kit`, `_far`, `_things`, `_layout`, `_frames`, `_check`, `_people`, `_mock`) | the Forum from its east end: the temple of Castor's corner, Juturna's basin, the Puteal, the moneychanger's table and its awning, the hoarding of the senate house's site, statues on their columns, the crane's wheel in frames <!-- ROME-13R1 --> | `art/scenes/rome-forum/` |
| `rome_capitol.py`, `rome_capitol_temple.py`, `rome_capitol_things.py`, `rome_capitol_geese.py` | the Capitol: the precinct before the temple of Jupiter, its cut-outs, and the sacred geese's frames (`_kit` the measurements, `_layout` writes `layout.json`, `_check` and `_walk.mjs` check it, `_plan` the blocks, `_people` the game's people in it) <!-- ROME-13R2 --> | `art/scenes/rome-capitol/` |
| `rome_tiber.py` | across the Tiber: the right bank below the stone bridge, the barge, Eleazar's house and window, the house of prayer and its bench, the hen yard; with `rome_tiber_model.py` (the place measured), `rome_tiber_kit.py`, `rome_tiber_things.py`, `rome_tiber_hens.py` (the hens' frames), `rome_tiber_layout.py` (layout.json), `rome_tiber_plan.py` (the skeleton), `rome_tiber_check.py`, `rome_tiber_walk.mjs` and `rome_tiber_order.py` (the check picture, the engine's walk map, the engine's back-to-front order with the boy anywhere), `rome_tiber_people.py` (the game's people stood in it, the man at the window at his own scale) <!-- ROME-13R3 --> | `art/scenes/rome-tiber/` |
| `home_living_room.py` | the living room at night, two storeys high, with the stairs up to the landing | `art/scenes/home-living-room/` |
| `home_landing.py` | the landing upstairs, seen from out over the living room | `art/scenes/home-landing/` |
| `home_study.py` | Dad's study under the roof | `art/scenes/home-study/` |
| `home_lilsis_room.py` | Little Sister's room under the roof | `art/scenes/home-lilsis-room/` |
| `home_bigsis_room.py` | Big Sister's room in the attic, the Retreat | `art/scenes/home-bigsis-room/` |
| `nevada_roadside.py`, `nevada_roadside_held.py`, `nevada_roadside_limo.py` | the last stop in Nevada; the sun shade held up (an alt); the limousine's frames, side on and nose on <!-- NEVADA-12A --> | `art/scenes/nevada-roadside/` |
| `nevada_ranger.py` | Ranger, Grandpa Joe's raccoon: his painted frames, plain and in the mirror shades, and `ranger.json` (installed with the roadside, keyed as its frames); his two portraits (into `out/portraits/`, installed as painted). Round seventeen added four sets after the others, so that none of theirs changed: `climb` (4), `drop` (2), `peek` (2), `pull` (2) <!-- OFFICE-17A --> | `art/scenes/nevada-roadside/`, `art/portraits/` |
| `nevada_store.py` | the store inside, one morning, through one camera: its cut-outs, the roller and the TV, the hens in the yard (`nevada_store_hens.py`) | `art/scenes/nevada-store/` <!-- NEVADA-12B --> |
| `nevada_limo.py` | inside the limousine, driving: the divider up and down, the ropes as they come undone, the bag, the clipboard and the juice box, the window panes; and the desert going by behind them (`nevada_limo_strip.py`) | `art/scenes/nevada-limo/` |
| `nevada_limo_drive.py` (with `_kit`: the camera and the road's numbers, the light, the smoked glass, the tools for pictures that repeat end to end; `_sky`, `_bands`, `_ground`, `_things`: the pictures; `_check`: the checks, and the pictures seen through the four panes with the contract's formulas at two moments) | the world outside the limousine's windows for the engine's `drive` kind (DRIVE-16): the sky (`drive-sky.png`); each side's far ranges and middle distance, side on (`drive-far-l/-r.png`, `drive-mid-l/-r.png`); each side's ground from straight above, 16 px a metre (`drive-ground-l/-r.png`); the upright things beside the road on one sheet, 24 px a metre, each in two lights (`drive-things.png` and `.json`). Keyed as the scene's frames <!-- DRIVE-16P --> The things are painted without their shadows, each box only as wide as the thing: the engine lays the shadows on the ground (`drive`'s `sun`) <!-- DRIVE-16F --> | `art/scenes/nevada-limo/` |
| `office_lot.py` (with `_kit`: the camera, the sun and where everything is, in cm; `_things`: the things drawn through the camera; `_limo`: the gray limousine parked, the roadside's drawing in this light, its rear door shut and open; `_out`: the full run's files and the pictures to look at; `_layout`: `layout.json`; `_check`: the checks, the check pictures, and `people`, the game's figures standing in it) | outside the Office's field headquarters, early afternoon: the building and its sign, the rooftop unit, the drainpipe, the fence and its open gate; the cut-outs and their states (the grille on and off, its four wing nuts, the switch on and off, the door shut and open, the awning, the trash can standing, tipped over and under the pipe, the flagpole, the limousine with its door shut and open, the front plane), the fan turning and the pennant stirring in frames; two floors to walk, the gravel and the roof <!-- OFFICE-17A --> | `art/scenes/office-lot/` |
| `office_room.py` (with `office_room_model.py`, the room measured; `office_room_kit.py`, the Office's own kit, which Property & Effects shares: light panels and their tubes, carpet tiles, painted block, the suspended ceiling, the grille and Ranger's eyes behind it, the stacking chair, the four passes; `_things`; `_cuts`, the full run; `_layout`; `office_people.py`, the game's people and Ranger's frames stood in either room, sorted with its cut-outs; `office_check.py`, the checks of both rooms) | Interview Room C, the Comfortable Room, under the tubes, through one camera: the grille over the corner chair (plain; two eyes behind it), the thermostat at 72, 77 and 81, the intercom dark and lit, the door shut and open, the table (whole under the questionnaire) and the questionnaire, the plastic plant upright and drooping; the clock's second hand and the cooler's bubble in frames; the one-way mirror shows the room rendered through it <!-- OFFICE-17C --> | `art/scenes/office-room/` |
| `office_property.py` (with `_model`, `_things`, `_cuts`, `_layout`) | Property & Effects, from among the shelves: every thing tagged, the banjo in its bay (No. 3117), Opal's window onto the lit hall, her counter, stool and knitting, the door shut and open, the far wall round them as a cut-out, the grille (plain; two eyes behind it), the receipt on the counter <!-- OFFICE-17C --> | `art/scenes/office-property/` |
| `office_breakroom.py` (with `_model`: the room measured, the camera; `_kit`: the stage of rays, the lamps, the lettering laid through the camera; `_things`: the shell, the tubes, the grille, the door and the hall; `_props`: the furniture and everything on it; `_cuts`: the full run, the cut-outs, their states and the clock's frames; `_layout`: `layout.json`, measured from the picture; `_check`: the checks and the check picture; `_people`: the game's people and Ranger's frames stood in the installed room) | the Office's break room under its fluorescent tubes, through one camera: the fridge with the grille over it, the counter with Wendell's pie (whole, eaten with a bottle cap in the tin, gone), the corkboard and the test schedule, the snack machine (the peanuts in its tray), the couch, Jed's chair, the door (shut, open), the clock's second hand in frames, the near tables <!-- OFFICE-17D --> | `art/scenes/office-breakroom/` |
| `items.py` | the inventory pictures | `art/items/` |
| `proof_critter.py` | the engine's own painted creature, its strip and its window, for the proof scene (drawn as they are, never keyed) | `art/proof/` |
| `proof_drive.py` | the engine's own pictures for its `drive` (the world going by a car's side windows), for the proof scene: a car's side with a window each side of the vanishing point, a sky, a ground of squares and stripes for each side, ranges of plain triangles, posts, poles and a marker on a sheet with its JSON (drawn as they are, never keyed) <!-- DRIVE-16E --> | `art/proof/drive/` |
| `map_egypt.py` (with `map_egypt_kit.py`: the measurements, the paints, the papyrus and the reed pen; `_things`: the drawings; `_layout`: `layout.json`, measured from the pictures; `_check`: the checks and the four check pictures) | the map of Egypt for the map screen: a scribe's sketch on papyrus, the sheet with the lie of the land (`back.png`), each place and each way its own picture; installed as painted, never keyed (`python3 install.py map-egypt`) <!-- MAP-15E --> | `art/maps/egypt/` |
| `map_rome.py` (with `map_rome_kit.py` the tablet's measures, paints and stylus, `_sheet` the tablet, `_places` the plan, `_layout` writes `layout.json` from the pictures, `_check` checks it and draws its four check pictures) | the map of Rome for the map screen: a wax tablet in its wooden frame, the Tiber's bend and the Capitol's hill scratched in (`back.png`), the six places and the five ways each its own picture, the plan scratched with a stylus; installed as painted, never keyed <!-- MAP-15R --> | `art/maps/rome/` |
| `map_home.py` (with `map_home_house.py`, the house measured from the five rooms' models; `_kit`, the squared paper and the pencil; `_things`, what is drawn; `_layout`, which measures `layout.json`; `_check`) | the map of the house: Dad's pencil floor plan on squared paper (ground floor, upstairs, the attic), its places and ways (as painted, never keyed) <!-- MAP-15H --> | `art/maps/home/` |
| `map_nevada.py` (with `map_nevada_kit.py`: the sheet's measures, its inks mixed from the paint box, the plates, the paper and its folds, the ranges' hachures; `_layout`: `layout.json`, measured from the pictures; `_check`: the checks and the four check pictures) | the map of Nevada for the map screen: Grandpa Joe's own fold-out road map from his counter's rack, opened flat (`back.png`: the creased, yellowed sheet, the main map with the highway TO NOTHING, the cover panel, the legend and the empty detail panel), the Last Stop, the store and the road each its own picture, printed on it; installed as painted, never keyed (`python3 install.py map-nevada`) <!-- MAP-15N --> | `art/maps/nevada/` |
| `office_ducts.py` (with `office_ducts_model.py`: the measurements and the camera; `_kit`: a ray for every pixel, lit from where each light is; `_things`: everything in the ceiling space, built in centimetres; `_layout`: `layout.json`, measured (`python3 office_ducts.py layout` measures it again from the geometry alone); `_grille`: the grille's view; `_check`: the checks, and Ranger at every mark, the grille's view over three rooms; `office_letters.py`: the Office's single-stroke capitals, as stencils here and as drafting on the map) | the air ducts over the Office's ground floor as a cut-away, like an architect's section, through one camera (Ranger on the duct's floor at scale 1.0): a sheet-metal tube cut open along its near side, its walls cut as a section is drawn (the cut sheet bright on the tube's inside, a thin hatched core; the intake run at the left and the B-7 shaft at the right cut the same way), its inside 3.5 times Ranger's height and the brightest thing in the picture, four grilles in its floor (ROOM C, PROP & EFF, BREAK, HALL) with the rooms' light in bars up its back wall; the intake run (daylight from the rooftop unit, the intake fan still); round it the ceiling space, dim but readable (the joists and the deck cut at the top, pink insulation lying on the duct and on the tiles, the water pipe, a jacketed hot-water line, the bundled wires, a conduit, the sprinkler main, the tiles' backs with a coffee cup, a pencil, a wrapper, the light fittings cut with their tubes alight and their light falling into the rooms under the tiles' cut line); the B-7 shaft, a clean tube going down past its fan, rungs down its back wall; the B-7 fan's frames (`fan-0` .. `fan-3` turning, `fan-stopped`); `grille-view.png`, the slats Ranger sees through, laid by the engine over a room <!-- OFFICE-17B; OFFICE-17B2: painted again as a section --> | `art/scenes/office-ducts/` |
| `map_office.py` (with `map_office_kit.py`: the draughtsman's pen, the print, the paper, the rubber stamp; `_things`: the plan, in pixels; `_layout`: `layout.json`, measured from the pictures; `_check`: the checks and five check pictures) | the map of the Office for the map screen: a blueprint, sheet 1 of 8 (`back.png`: the folded print, its border, the title block, the scale bar and north arrow, the general notes, the ground floor's walls, doors and room numbers), the lot, the ducts (dotted, with their four grilles), the three rooms and B-7 (the shaft and the elevator, stamped B-7 · RESTRICTED) each its own picture, and the way from the lot up to the ducts; installed as painted, never keyed (`python3 install.py map-office`) <!-- OFFICE-17B --> | `art/maps/office/` |

## Two things to know before changing anything

- **The painting is seeded.** Running a script again gives the same picture, pixel for pixel. Changing a library
  file changes every picture painted with it, a little, the next time each is run. Change the library only when you
  mean to repaint, and look at every scene afterwards.
- **`brush.Sheet` and half-transparent strokes.** A half-transparent stroke laid over an earlier one on the same
  `Sheet` replaces it instead of glazing over it, which can leave thin spots in a cut-out. Several scene kits carry
  a small subclass that layers properly (`Paper` in `highway_kit.py`, for one). Use that for cut-outs, or paint
  solids and glazes on separate sheets.
