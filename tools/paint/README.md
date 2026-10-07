# The painter

Every background in the game, every cut-out that stands in one, and every inventory picture is painted by the
Python scripts in this folder. Nothing here runs in the browser: the scripts write PNG files, and the PNG files
are what the game shows (`art/scenes/<scene>/`, `art/items/`).

They need Python 3 with `numpy` and `Pillow`, and nothing else.

```
cd tools/paint
python3 rome_street.py fast     # a quick look: skips the brush pass (about 15 seconds)
python3 rome_street.py          # the full passes (a minute or two): writes out/rome-street/
python3 install.py rome-street  # copies out/rome-street/ into art/scenes/rome-street/
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

## People are not painted in

The game draws them (`js/art/`). A grown-up is 160 pixels tall with feet on the scene's row `full`, and smaller
toward `horizon` in proportion. `persp.Camera(horizon, full)` is a camera that matches those two numbers, in
centimetres, so furniture, doors and steps come out the right size for the people who will stand beside them.

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
| `install.py` | copies a painted scene into `art/` |

One script to a scene (some with helper files named after it: `_kit`, `_things`, `_props`, `_check`, `_look`):

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
| `home_living_room.py` | the living room at night | `art/scenes/home-living-room/` |
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
