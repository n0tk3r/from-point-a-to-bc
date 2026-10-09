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
  unions and frames. Every picture file of a scene must be in its plan, so nothing goes in unkeyed by mistake.
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
| `egypt1.py`, `wagon.py`, `egypt1_donkey.py`, `egypt1_steam.py` | where the wagon came down: backdrop, palms, the wagon and its states, the donkey, steam | `art/scenes/egypt-crash/` |
| `egypt_site.py` | the foot of the pyramid | `art/scenes/egypt-site/` |
| `egypt_gallery.py` | the great gallery | `art/scenes/egypt-gallery/` |
| `egypt_chamber.py` | the burial chamber | `art/scenes/egypt-chamber/` |
| `rome_street.py` | the street to the Forum | `art/scenes/rome-street/` |
| `rome_steps.py` | the steps of the temple | `art/scenes/rome-steps/` |
| `rome_temple.py` | inside the temple | `art/scenes/rome-temple/` |
| `home_living_room.py` | the living room at night, two storeys high, with the stairs up to the landing | `art/scenes/home-living-room/` |
| `home_landing.py` | the landing upstairs, seen from out over the living room | `art/scenes/home-landing/` |
| `home_study.py` | Dad's study under the roof | `art/scenes/home-study/` |
| `home_lilsis_room.py` | Little Sister's room under the roof | `art/scenes/home-lilsis-room/` |
| `home_bigsis_room.py` | Big Sister's room in the attic, the Retreat | `art/scenes/home-bigsis-room/` |
| `nevada_roadside.py` | the last stop in Nevada | `art/scenes/nevada-roadside/` |
| `items.py` | the inventory pictures | `art/items/` |

## Two things to know before changing anything

- **The painting is seeded.** Running a script again gives the same picture, pixel for pixel. Changing a library
  file changes every picture painted with it, a little, the next time each is run. Change the library only when you
  mean to repaint, and look at every scene afterwards.
- **`brush.Sheet` and half-transparent strokes.** A half-transparent stroke laid over an earlier one on the same
  `Sheet` replaces it instead of glazing over it, which can leave thin spots in a cut-out. Several scene kits carry
  a small subclass that layers properly (`Paper` in `highway_kit.py`, for one). Use that for cut-outs, or paint
  solids and glazes on separate sheets.
