# Depth: the three planes (round twenty-three)

The author, 9 November: "You have to redo the scenes and make the perspectives not look so amateur and flat. Study the
Broken Sword scenes and how they have dimension (foreground objects, middle ground and background objects add dimension
to the scenes). Also make the Japanese scenes look a little more watercolored."

This file is the art direction for that repaint, and it goes before the README where they differ. Read the README's
"The look", "How a picture is made", "Cut-outs" and (for a room) "Painting a room" as well: all of it still holds.

**What was studied, and what is taken.** The backgrounds of the hand-drawn adventure games of the middle 1990s were laid
out by people trained on animated films, and a film layout is staged in depth: something near the lens, the action in
the middle, the world going away behind. We take how a picture is staged. Nothing is copied: no place, building,
object, arrangement or figure of anybody else's. Every place in this game is its own, and stays so.

## Why our pictures look flat (measured: `python3 depth_check.py <scene>`)

1. **Nothing is near us.** In most scenes the front plane covers under 5 per cent of the picture, and in many, nothing.
2. **The camera stands high and far off.** The eye is 3.2 to 4.9 m above the ground; at half the standing places a
   grown-up is under 90 px tall; the ground is half the picture, like a stage seen from the gallery.
3. **The main building faces us square,** or stands small and whole inside the frame with sky all round it: a toy.
4. **The ground is one tone** from far to near, with few shadows on it.
5. **Behind the middle ground there is one far thing** (a mountain, a hill) and not layer behind layer.
6. **Things stand side by side with gaps between,** like a diagram. Little overlaps anything.

## The three planes

Every picture is staged in three planes, and each has its own tone. Squint at the finished picture: three masses.

### Near: the front plane (12 to 25 per cent of the picture)

Things within a few metres of the lens, between us and the play. This is the plane we did not have.

- **Large, and cut off by the frame.** Never a whole thing: a trunk up one side and its bough across the top; the
  corner of an eave and its post; a column and a slice of its entablature; jars and baskets heaped along the bottom; a
  boat's prow; a cart's wheel; a lantern; cloth hanging; reeds. It runs off **at least two edges** of the frame, and
  never leaves bare ground along the whole bottom edge.
- **A clear dark mass by day:** in shade, the richest and warmest darks of the picture, lit only along the edge that
  faces the light (a rim). In a dark room it is the near dark shape against the lit room, or one near thing in the lamp.
- **Outline before inside.** An interesting silhouette (gaps to see through, a broken edge), little detail within.
- **Through the scene's own camera, at its true size.** A thing nearer than the `full` row is larger than life (z less
  than 0 in `persp.Camera`; a place nearer the lens in `room.View`): a post 20 cm thick, 2 m from the lens, is a
  hand's breadth of the picture wide. Its lines run to the same vanishing points as everything else.
- **It frames the play and never hides it.** No clickable thing, standing place or mark behind it (`depth_check.py`
  lists what is hidden). Keep it out of the middle of the picture; the corners and edges are its place.
- **It belongs.** Ask what would really stand there, by the lens, in this place and hour, and paint that.
- A front-plane cut-out is a file of its own (`near.png`, or more of the scene's own `front.png`), `plane: "front"` in
  the scene file, last in its `planes`: people always pass behind it.

### Middle: the play

Where people walk and things are clicked: the clearest, best lit, most detailed plane. The light falls here.

- **Shadows lie across the ground.** Everything that stands on it throws one, the same way, through the camera
  (`land.cast` for a cut-out, a projected polygon for a box). And at least one **large shadow from something outside
  the picture** (the building behind us, a tree overhead): its edge leads into the picture and tells where the light
  is. Dappled shade under leaves. People stand on this ground: on a floor without shadows they float.
- **A texture that shrinks with distance.** Joints, ruts, stones, tufts, cracks, puddles, straw: big and few near us,
  small and many far off, at a true density for each square metre (`depth.scatter` gives the places and sizes through
  the camera). The ground deepens in tone toward us and pales toward the horizon. Under 40 per cent of the walkable
  ground may be flat colour.
- **Overlap.** At every depth something stands in front of something else. Group things in clusters with gaps between
  the clusters; never space them out evenly. Six clear overlaps across the play, at least.
- **Lines that lead in.** A path, a kerb, a row of posts, a shadow's edge running from a lower corner into the picture
  toward what matters.
- New things in the middle ground stand where nobody walks (beyond the walk outline, or in a `blocked` patch).

### Far: the background (three layers at least)

- Behind the play, **layer behind layer**: the far side of the square, the roofs beyond it, the hill and its temple, the
  sky. Each layer is paler, plainer and nearer **the colour of the sky at the horizon** than the one in front of it
  (toward the sky's colour, not toward grey), and its edges are softer.
- Each layer **overlaps** the next: skyline against skyline.
- The darkest dark of a far layer is lighter than the middle tones of the play. A dark thing far away jumps forward.
- Clouds grow smaller and flatter toward the horizon. A sky has perspective too.

## Perspective

Scenes are of two kinds this round (the lead says which yours is):

**DEEPEN: the camera and every number of the scene file stay.** The picture gains its three planes round them.

**RECOMPOSE: a new camera,** because the old view was square-on or from too high. Then:

- The eye 2.3 to 3.0 m above the ground (`full` minus `horizon` between 210 and 275), so that the ground is no more
  than about 45 per cent of the picture and a grown-up at the usual standing places is 95 to 150 px tall.
- Outdoors, a view turned 20 to 40 degrees: two vanishing points, no long wall parallel to the picture. A view straight
  down a street or a room has one vanishing point, set off-centre.
- The main building near, and **cut off by the top or the side of the frame**. Something looms.
- Draw the skeleton first (boxes through the camera, stand-in people at the marks: `room_plan.py`, or the scene kit's
  own) and look at it. If the skeleton is not a deep place with people the right size in it, no painting will mend it.
- Then every number of the scene file is measured again (walk, blocked, marks, areas, bases, effects), ids and logic
  untouched.

In both kinds:

- **One camera for everything,** small things and shadows included (README, "Why one camera").
- **True perspective, hand-made lines.** A ridge sags, a post leans, steps are worn: nothing ruled for long. But every
  line still runs to its vanishing point.
- No whole building floating in sky. If the camera cannot move (DEEPEN), put things in front of it and beside it,
  bring boughs and eaves across the sky, and layer the land behind it.

## Light and air

- One key light with a direction (the scene's own: keep its hour). A shadow side on every form; cast shadows on ground
  and walls; warm light bounced up from sunlit ground into the shaded walls; pools of light indoors.
- Decide where the lightest light of the picture is (the door, the thing to be found) and keep the rest quieter.
- Depth by colour: near darks rich and warm, far things toward the sky's colour.

## Japan in watercolour (Act Six only)

"A little more watercolored": the same act, the same drawing, laid in washes on paper and not pressed from a block.

- **Washes for flats.** No area is one even colour: grade every wash (darker toward one side or the ground:
  `watercolor.graded`), and finish every picture with `watercolor.wash` just before the palette: the backdrop with
  `wash`, every cut-out with `wash_cut` over the backdrop **with the same seed**, so the paper is one sheet.
- **Wet in wet for what is far or soft:** sky, clouds, mist, far land, open water, smoke. Give `wash` a `soft` mask of
  them: their edges bleed. Near things stay crisp, wet on dry.
- **The white is the paper.** Snow, plaster in sun, foam, the lightest road: bare paper (`watercolor.PAPER`), with a
  little left unpainted along lit edges. The whole picture a step lighter and more transparent than the print was.
- **Shadows are glazes:** a thin cool wash over the local colour (multiply: `brush.tint`), never a flat block of
  another colour.
- **The key line stays, quieter:** thinner, a little broken, lost altogether on the lit side of things and in the
  distance (far layers have no line at all).
- Lamplit rooms and night: `wash(..., amount=0.6)`, so the darks stay deep.
- It must still read as the same act beside the scenes not yet repainted. A little.

## What stays exactly as it is

- In a DEEPEN scene: every number of the scene file; every existing picture file's name, what it shows and where it
  is (a cut-out's place and base line; a state pixel-aligned with what it replaces; every frame of a moving thing).
- Every clickable thing: still there, still recognisable, in the same place, not hidden.
- Whatever a puzzle needs to be seen (the scene file's header comment and the act's puzzle document say what).
- Lettering that is read. The hour and the light's direction. The history: the scripts' header comments hold the
  research on the place; nothing invented may contradict it. Nothing frightening. Nothing that reads as a cross on a
  Buddhist place.
- The look outside Japan: the game's paints at 50 (`install.py` keys the scene as before).

What may change: the backdrop anywhere outside the clickable things (sky, far land, ground, set dressing where nobody
walks), the drawing and light of buildings and of the cut-outs themselves (same place, same outline at the base, better
form), and new front-plane files.

## How to work

1. Work only in the copy of the game you were given. Never run git.
2. Read this file, the README sections named above, the scene file's header comment, and the scene's painter scripts.
3. **Before:** run the scene's script as it is (it is seeded: it repaints what is installed) and
   `python3 depth_check.py <scene>`; look at `out/<scene>-depth-pair.png`. Keep the picture as it was.
4. **Plan** in `out/<scene>-plan.md` (40 lines at most): what stands near, and why it belongs there; what the middle
   gains (which shadows, what texture, which overlaps); the far layers; where the lightest light is. For RECOMPOSE:
   the camera, and the skeleton looked at before any painting.
5. **Paint** in the scene's own scripts, in the four passes. The machine has two cores and other painters are on it:
   compose with the `fast` run, and make full runs only to judge.
6. **Look, and mend.** After each full run read the picture yourself at full size beside the old one, name its three
   weakest places, and mend them. Three rounds at least. A picture that passes the numbers and still looks flat is not
   finished: the numbers are a floor.
7. **Install:** the new files in the scene file's `planes` and in `postimp_plans.py`; `python3 install.py <scene>`;
   `python3 postimp_key.py --check`; `python3 ../stamp.py`.
8. **Check:** `depth_check.py` says PASS; the scene's own `_check.py`, if it has one, is as clean as it was before;
   the game shows it (the "Try it" address in the scene file's header) with the family standing in it, every clickable
   thing in sight, nobody hidden.
