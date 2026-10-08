# From Point A to B.C.: how the game is built

This is the design of the game's engine and its look. It answers ten questions:

1. [What kinds of animation can a browser game use, and which do we use?](#1-animation)
2. [What is on the screen, and how are the pictures made?](#2-the-stage)
3. [How does a flat picture get its depth, and how do people walk about in it?](#3-depth-and-walking)
4. [How are the people drawn?](#4-the-people)
5. [How do intro movies work, and how do they lead into the title?](#5-intro-movies-and-cutscenes)
6. [How do saved games work?](#6-saved-games)
7. [How do music, sound and dialogue work, and how do we get to full voices?](#7-sound-music-and-dialogue)
8. [How is the story kept guided without being a straight line?](#8-story-guided-but-not-a-straight-line)
9. [How does one look hold across every time period?](#9-one-look-across-every-era)
10. [How do I add a scene, a picture, a character, a line, an era?](#10-how-to-add-things)

It ends with [the tools](#11-the-tools), [what is finished and what is not](#12-what-is-built-and-what-is-not),
[the controls](#13-controls) and [the decisions that are yours to make](#14-decisions-waiting-for-you).

Everything described here is working code in this repository.

Companion documents: [CHARACTERS.md](CHARACTERS.md) says who the people are and how each of
them talks. [PUZZLES-egypt.md](PUZZLES-egypt.md), [PUZZLES-rome.md](PUZZLES-rome.md) and
[PUZZLES-the-present.md](PUZZLES-the-present.md) map the acts puzzle by puzzle.

## The short version

| Question | Decision | Why |
| --- | --- | --- |
| Engine | Plain JavaScript modules, no framework, no build step | GitHub Pages serves the files as they are. Nothing to install, nothing to break. |
| Picture | One painted picture, 800 pixels wide and 600 high, scaled to fit any screen | Room for a hand-painted background in the manner of the classic adventures. Every position in the game is a pixel of that picture, so a number in a scene file can be measured straight off the painting. |
| Scenery | A painted backdrop for each scene, with painted cut-outs for whatever people walk behind or the story changes | A background can be as rich as a painter can make it and costs the game nothing while it is on screen. |
| Light | Time travel, beams and glows are drawn by code, never painted | They have to move, grow and stay smooth, and a wormhole should not look like part of the world it has opened in. |
| People | Drawn by a jointed figure from a page of settings, not stored as pictures | One description gives all eight directions, every animation and every size. See section 4. |
| Depth | People, props and cut-outs are painted back to front by where they touch the ground, and people shrink toward the horizon | The lead walks behind the car, in front of it and round it, with no hand-made mask. See section 3. |
| Movement | One game clock drives anything that matters to the game. CSS runs only the glow of time travel and a few ambient loops. | Each tool does the job it is best at. See section 1. |
| Intro movie | A script that moves the game's own art. Not a video file. | A few KB of script and six pictures instead of tens of MB, identical in style to the game, skippable, subtitled. |
| Saves | Autosave and three slots in the browser, plus a save file the player can download and load anywhere | Browser storage can be wiped. A file is the player's own. |
| Sound | Web Audio with separate volume for music, effects and voices | Standard, works everywhere, lets music duck under speech. |
| Dialogue | Every line has an ID. Text now, a sound file with the same name later. | Voices can be added one line at a time without touching any script. |
| Story | Acts and beats listed as data, with a checker and a storyboard page | Parallel puzzle chains inside an act, one gate at the end of it. |
| Leads | Five people the player can control. Apart, each has scenes of their own. Together, the player switches between them with their portraits. | A father and son lost in different centuries, and a mother and two daughters working as a team. See section 8. |
| Look | One way of painting, one figure and one light for every person, one typeface, and time travel in neon | Each era changes what is painted, never the rules. See section 9. |
| Updates | Every code file, style file and picture is fetched by an address that changes when the file changes, and a game in progress keeps what it has fetched | A push can never leave a browser running old files next to new ones, or put a new painting behind an old script. See "Publishing a new version" in section 10. |

Size today: 51 code and style files, about 750 KB (about 230 KB when the server compresses
it); 83 pictures, 3.4 MB in all; and a 49 KB font. Nothing else is downloaded.

## Where things are

```
index.html              the page: one stage, a stack of layers
css/tokens.css          colors and type: the time colors, the era palettes
css/game.css            layout and interface
js/main.js              gathers the content and starts the engine
js/engine/              the engine. Knows nothing about this story.
  grid.js                 the size of the picture (800x600), and how an old 320x200 drawing is fitted into it
  assets.js               pictures: fetched once by a stamped address, then held for the whole session
  clock.js                the game clock: wait, tween, pause, skip
  state.js                the data a save file holds
  save.js                 slots, export to a file, import from a file, upgrades from older versions
  audio.js                music, effects, voices
  dialogue.js             spoken lines and choices
  scene.js                the stage: backdrop, live light, clickable areas
  cast.js                 people, painted cut-outs and props: depth order, animation, the store of finished pictures
  walk.js                 where the lead can stand, routes round obstacles, size by distance
  fx.js                   canvas effects (the time tunnel)
  story.js                reads the story data: open beats, checks
  ui.js                   heads-up display and menus
  game.js                 ties it together; the `g` that scripts use
js/art/                 everything that is drawn by code
  kit.js                  the portal, the sketch of an unpainted scene, close-ups, and the old 320x200 drawings
  pix.js                  the pixel renderer: solid shapes in, pixel art out
  rig.js                  the jointed figure: poses, eight directions, the walk, stances, gestures, sitting
  people.js               the cast as the rig sees them: proportions, clothes, colors, and how each one stands, walks and talks
  props.js                things drawn by code that stand on the ground (kept for scenes that are not painted yet)
js/content/             the game itself. Knows nothing about the engine's insides.
  world.js                cast, eras, items
  lines.en.js             gathers the spoken lines
  lines/*.en.js             the lines, one file to an act: common, egypt, rome, home, nevada
  story.js                where a game starts, stock replies, and the list of acts
  acts/*.js                 the acts and their beats, one file to an act: prologue, egypt, rome, home, nevada
  sound.js                music, effects and the list of recorded lines
  cutscenes/highway.js    the painted highway at dusk, and the parts of it that change
  cutscenes/intro.js      the intro movie
  cutscenes/title.js      what is behind the title screen
  scenes/index.js         the list of scenes
  scenes/*.js             one file per scene, all fetched while the start-up panel shows
  scenes/engine-proof.js    the worked example of a painted scene: the pattern to copy
  scenes/sketch-example.js  a scene with no painting yet, to show storyboarding
art/scenes/<scene id>/  a scene's pictures: back.png, its cut-outs, and layout.json (the painter's measurements)
art/scenes/highway/     the pictures of the intro and the title
art/items/              the pictures of things that can be carried
fonts/                  Koine Road, the game's typeface
tools/storyboard.html   the story, drawn out, straight from the data, with every scene as the game builds it
tools/sprites.html      every character and prop, moving, in every direction
tools/serve.py          runs the game on your computer, always with the files as they are now
tools/stamp.py          gives every file an address that changes when the file does (run before a commit)
tools/hooks/pre-commit  optional: runs stamp.py by itself at every commit
tools/paint/            the scripts that paint the pictures (their own guide is the README there)
tools/koine-road/       the scripts that build the typeface
docs/                   this file, the character bible, and a puzzle document for each part of the story
```

To run it on your computer: `python3 tools/serve.py` in this folder, then open
`http://localhost:8000`. Opening `index.html` by double-clicking will not work,
because browsers only load module files from a web address. The page says so if you try.

---

## 1. Animation

### What a browser game can use

| Technique | What it is | Good at | Weak at |
| --- | --- | --- | --- |
| CSS transitions and keyframes | You describe the motion; the browser runs it | Loops and decoration. Changes to `transform` and `opacity` can run on the graphics card without redrawing the page. | You cannot easily pause it at a saved moment, skip it, or have it wait for a click. |
| Web Animations API | The same engine as CSS, driven from JavaScript, with `pause()`, `finish()`, `currentTime` and `playbackRate` | One-off effects you need to control | Still a separate timeline per animation; many of them get hard to keep in step. |
| `requestAnimationFrame` loop | Your code runs once per screen refresh and moves things itself | Anything the game logic depends on: walking, cutscene timing, dialogue timing | You write the motion yourself. |
| SVG | Vector drawings in the page, styled by CSS | Light and glows, sharpness at any size, clickable shapes | Hundreds of moving parts at once. |
| Picture files | A painting, or a part of one with a clear background | Scenery of any richness, at no cost while it is on screen | Each is a download, and it cannot change except by swapping it for another. |
| Sprite sheets | A strip of frames, stepped through with `steps()` or by a clock | Hand-drawn character animation | Each sheet is an image to download, and every direction, action and size is more drawing. |
| Sprites drawn by code | A figure described as shapes and joints, turned into pixels when needed | Many directions, actions and sizes from one description | No artist's hand on each frame. |
| Canvas 2D | A bitmap you repaint | Many things that overlap and change order: a cast of people among furniture, particles, tunnels | Nothing in it is clickable or readable by a screen reader, and the browser handles the whole of it again on every frame in which the page changes. |
| WebGL (PixiJS, Phaser, Three.js) | The graphics card, directly | Thousands of sprites, shaders, 3D | A large library and a build step, for power a point-and-click does not need. |
| Video files | A recorded movie | Live action, pre-rendered 3D | Tens of megabytes, cannot match the game's state, fixed size, harder to subtitle. |

### What this game does

The rule is: **who needs to know about the motion decides the tool.**

- **If the game depends on it, the game clock runs it.** `js/engine/clock.js` is a
  single `requestAnimationFrame` loop. Walking, cutscene beats, line timing, fades
  and the tunnel all ask this one clock for `wait(ms)` or `tween(ms, step)`. Because
  there is one clock, pausing the game pauses all of it, and skipping a cutscene is
  one switch (see section 5).
- **Scenery is a painted picture, shown as it is.** The backdrop is the picture file
  itself, in a picture element. Nothing that happens afterwards touches it.
- **People, painted cut-outs and props share one canvas above the scenery.** On a frame
  where nothing on it has changed, nothing is painted. When something has (a step, a
  blink, a lid that opens), only the patch it touched is wiped and painted again.
  Sections 3 and 4 explain how those pictures are made and put in order.
- **Light is drawn live, and CSS animates it.** The spinning rings of a portal, the
  glow it throws on a road, a beam of sunlight. These are smooth drawings on a layer of
  their own, and they only ever animate `transform` and `opacity`, the two properties
  browsers can animate without redrawing the picture.
- **A second canvas is used for one effect:** the time tunnel (`js/engine/fx.js`),
  where rings, streaks and flying dates all change every frame.
- **No WebGL and no game framework.** If a later scene needs a storm of particles,
  that scene can add a canvas effect the same way the tunnel does.

Players who ask their system for less motion (`prefers-reduced-motion`), or tick
**Less motion and no flashes** in Options, get still decoration, people who stand
quite still, cut-outs that hold their first picture, plain fades in place of white
flashes, and a slow tunnel.

### Keeping it fast

- **Scenes are small, separate files.** Each scene is its own file of a few KB. All
  of them are fetched while the start-up panel is showing, so that a game in progress
  never asks the server for code and can never be handed a scene from a newer version
  than the one it is running. When there are hundreds of scenes, fetch them an act at a
  time: `Game.start` in `js/engine/game.js` is the place.
- **A scene's pictures are here before it is shown.** Entering a scene fetches its
  backdrop and every picture its cut-outs can show, and only then fades in, so nothing
  pops in late. The pictures of the scenes that can be walked to from it (`exits`) are
  made ready ahead of time.
- **The whole game is fetched quietly behind the title.** Once the title is up, the
  engine goes through every scene's pictures, one at a time and only when the page has a
  moment to spare, and holds the files in memory (`Game.gather`, `assets.js`). It starts
  with the inventory pictures, the scene the autosave is in and the scene a new game
  opens on. Nothing waits for it and it decodes nothing, so neither the start nor play
  feels it. After a few seconds a session holds everything and asks the server for no
  more pictures.
- **Music and voices stream.** Nothing is downloaded until it is about to play.
- **A picture of a person is drawn once and kept.** One pose, one direction, one size:
  drawn the first time it is needed and kept in a store shared by everyone on stage,
  trimmed to the part with paint on it. The store has a budget of about 64 MB and drops
  whatever has gone longest unused. Cut-outs are trimmed and kept the same way.
- **Someone walking is drawn at a ladder of sizes.** Standing still, a person is drawn
  at exactly the size they are. Walking toward the horizon, that would mean a new
  picture at almost every step. So a walker's pictures are drawn at sizes 12% apart, and
  the nearest is stretched or squeezed, by 6% at most and with its pixels kept hard, to
  the size wanted. A walk cycle is then drawn once for a whole band of the floor and
  found again every time anyone crosses it. The old adventure games sized their people
  the same way.
- **A budget per scene**, to keep older machines smooth: about 20 things animating at
  once on the live layer, and only `transform` and `opacity` in any CSS animation.
  The backdrop can be as detailed as you like. Hold **H** in the game to check a scene's
  clickable areas.

**What a frame costs.** Measured in Chromium with the processor slowed four times over,
as a stand-in for an old laptop, while the lead walks across the three busiest scenes
and then from the farthest ground to the nearest. The figure is the main thread's work
for one frame; at 60 frames a second there are 16.7 ms to spend.

| Scene | Window | Walking across | Frames dropped | Walking into the picture | Frames dropped | Standing |
| --- | --- | --- | --- | --- | --- | --- |
| The street in Rome | 800x600 | 11.7, now 7.6 ms | 2, now 0 | 12.1, now 8.8 ms | 5, now 0 | 3.6, now 2.5 ms |
| | 1440x1080 | 11.7, now 6.9 | 3, now 0 | 12.8, now 8.0 | 2, now 1 | 3.5, now 2.3 |
| The living room | 800x600 | 13.9, now 9.7 | 6, now 4 | 14.4, now 9.0 | 1, now 1 | 3.8, now 3.5 |
| | 1440x1080 | 13.9, now 8.8 | 7, now 2 | 13.9, now 8.3 | 5, now 1 | 4.3, now 3.0 |
| Where the wagon came down | 800x600 | 16.4, now 7.9 | 17, now 1 | 13.4, now 8.0 | 4, now 0 | 4.4, now 3.6 |
| | 1440x1080 | 13.1, now 6.5 | 5, now 0 | 13.1, now 7.6 | 3, now 2 | 4.8, now 3.3 |

The first figure of each pair is the engine as it was before the three changes described
below; "frames dropped" is how many of about 350 frames, in six seconds of walking, took
more than twice their time. The figures move by about a millisecond from one run to the
next. The size of the window makes no difference, and nor does the choice between hard
and smooth pixels.

Three things were changed to get there. The backdrop used to be a canvas, and a browser
hands every canvas on the page to its compositor again on each frame in which anything
changes: showing the painting as a picture element took a third off a walking frame.
The cast layer used to be wiped and painted whole on every step: it now repaints only
the patch that changed. And a walker used to need a new picture at almost every step
into the picture: the ladder of sizes ended that.

What is left is the drawing of a new picture of a person the first time it is needed.
On the test machine that takes 1.4 ms for Little Sister, 1.7 for the Son, 3.3 for Mom
and 7.5 for Dad, and four times that on the slowed one, which on top of the rest of a
frame's work is more than a frame's time for the two grown-ups. So the first walk in a
new direction on a slow machine can stutter for a step or two, and the second does not. A third of that time is the renderer's last
pass over the picture (`finish` in `pix.js`).

---

## 2. The stage

### One size

The stage is one picture, **800 pixels wide and 600 high**. Everything on it is on that
grid: the painted backdrop, the cut-outs, the people, the light, the clickable areas.
Every position in the game is a pixel of the picture: where someone stands, where a
clickable area is, where the ground can be walked on, where a thing meets the floor. A
number in a scene file can be read straight off the painting in any paint program, and
the painter and the engine work from the same numbers. `js/engine/grid.js` holds the two
numbers, `W` and `H`.

One older grid survives. The first drawings in the kit (the close-ups of the computer
screen and of a notice, and the scenery the game had before it was painted) were made on
a 320x200 grid. The engine shows such a drawing in the band that fits it, 800 wide and
500 high, in the middle of the stage (`fit` in `grid.js`). Nothing new should be drawn
on that grid.

### The layers

The picture is a stack of layers, back to front:

| Layer | What is on it | How it is made |
| --- | --- | --- |
| Backdrop | The scene's painting: everything that is far away or flat on the ground | A picture file, shown as it is |
| Live | Light: wormholes, the glow they throw, beams, anything that must stay smooth or move by itself | Smooth drawings in picture pixels, animated by CSS or by a script |
| Cast | People, painted cut-outs and props | Pixels, sorted by depth and repainted where something has changed |
| Tunnel | The time tunnel | A canvas effect, only during travel |
| Clickable areas | Invisible shapes | Real buttons, so a keyboard or a screen reader can reach them |
| Close-up | A screen, a notice or a note, shown large over a dimmed scene | A smooth drawing, put up and taken down by a script |
| Words and menus | Speech, pockets, cards, menus | Ordinary page text |

The live layer is **under** the cast. A beam of light or a door in time is covered by
anyone, and any cut-out, standing in front of it.

### How it is fitted to the window

The stage keeps its 4:3 shape and is as large as the window allows. The pictures are
then scaled, and how they are scaled depends on how far:

- **By less than two, smoothly.** This is most windows on an ordinary screen: 1.8 times
  on a 1920x1080 monitor, about 1.4 in a smaller window. With hard pixels at such a size
  some picture pixels come out one screen pixel wide and some two. Thin lines turn into
  dashes, an eye is twice as big in one place as in the next, the speckle of the paint
  turns harsh, and a walker's features swim as he moves.
- **By two or more, with hard pixels.** This is a large or a sharp screen. Each picture
  pixel is a clean block, and smoothing at that size is simply a blur.

The painting, the people, a painted part that a cutscene puts on the live layer and the
tunnel always get the same treatment, so they always match one another. The rule is one
class on the stage, set by the scene view when the stage changes size (`CRISP_FROM` in
`js/engine/scene.js`, and "crisp" in `css/game.css`).

### A painted scene

A scene's pictures are in `art/scenes/<scene id>/`:

| File | What it is |
| --- | --- |
| `back.png` | The backdrop, 800x600: the scene complete, as it would look with everything that can move or change taken away |
| a cut-out, such as `wagon.png` | A part people walk behind, or a part the story changes. Also 800x600, clear except for the thing itself, so it needs no placing: it is laid over the backdrop at (0, 0). |
| a small cropped picture, such as `steam-0.png` | A thing that moves or is scaled by the game. It says which point of it stands on the ground. |
| `layout.json` | The painter's own measurements of the finished picture: the walk outline, what is blocked, each cut-out and its base, the shape and standing place of every thing, exits, marks for people. The game does not read this file. The numbers in the scene file are taken from it. |

Section 3 says how cut-outs are sorted with the people, and section 10 gives the scene
file in full.

A picture is named by its path from the top of the site, whichever page asks for it:
`"art/scenes/egypt-crash/back.png"`.

**People are never painted in.** The game draws them, so a painting leaves them out, and
its doors, tables and steps are sized for people 160 pixels tall at the row the scene
calls `full`.

**Light is never painted in either.** A glow, a beam or a door in time is drawn live by
the scene (`live` in the scene file), so that it can appear, move and fade.

**A scene with no painting yet is sketched.** Leave `picture` out of a scene file and
the engine draws sky, ground and a labelled box for each clickable thing, in the era's
colors. A scene whose painting will not load is sketched too, with a warning in the
console, and can still be played.

### How the pictures are painted

The pictures are made by scripts, not drawn by hand: one Python script for each scene,
using only numpy and Pillow, with a small shared library (brushes, skies, land, plants,
buildings, perspective, lettering). They are in `tools/paint/`, and the painter's own
guide is the README there. The aim is the hand-painted
background of the adventure games of the early 1990s, in compositions that are entirely
our own.

A picture is made in four passes:

1. **Under.** Everything broad and soft is blocked in: sky, the big planes of wall and
   floor, large forms with their light and shadow. No small things.
2. **Strokes.** The whole of it is repainted with visible brush marks.
3. **Details.** Every hard thing is stated again crisply over the brushwork (the edges
   of buildings, furniture, steps, door frames), and then the small crisp things are
   added: joints in stone, planks, leaves, handles, cracks, lettering, highlights. This
   is the pass that makes it an illustration and not a filter, and most of the work.
4. **Finish.** A grain, then a limited palette with a fine speckle: 128 to 160 colors
   for a backdrop, 32 to 96 for a cut-out. The speckle is one pixel fine on purpose.

What makes one look right, in the painter's own list:

- Light has a direction and a temperature: sunlit planes are warm, shaded planes are
  cool, and everything that stands on the ground throws a shadow the right way.
- Three big tones: a clear dark mass, a middle and a light, arranged to lead the eye.
- Depth by color: far things are paler, bluer and lower in contrast.
- Crisp where it is built, soft where it is air.
- No smooth computer gradients, no perfectly straight ruled edges, no repeated identical
  shapes. Skies are painted clouds, never bands.
- Detail that tells the story of the place, with the floor where people walk kept clear.
- Things the player can click are unmistakable at a glance, with room in front of them
  for a person to stand.

Rules for cut-outs: hard edges with no half-clear pixels; the backdrop painted complete
underneath each one, including the shadow the thing leaves behind; a separate cut-out,
aligned to the pixel, for each state of a thing that changes.

The inventory pictures (`art/items/`, 64x64) are painted the same way.

---

## 3. Depth and walking

A flat picture reads as a deep one when three things hold. The engine does all three
from two facts about each thing on stage: **where it touches the ground**, and **what
patch of ground it takes up**.

### 1. Nearer things cover farther things

Higher on the screen is farther away. On every frame the cast is sorted by where each
thing meets the ground and painted back to front.

- **A person or a prop** meets the ground at the point it stands on.
- **A painted cut-out** says where it meets the ground with its `base`:

| `base` | Meaning |
| --- | --- |
| a number, such as `400` | A row of the picture. People whose feet are above that row are behind the cut-out; below it, in front. |
| a line, `[[x1, y1], [x2, y2]]` | For a thing that meets the ground on a slant: a car seen from a corner, a wall running into the distance, a row of palms along a bank. People are behind or in front according to which side of the line their feet are on. |
| nothing, with `plane: "front"` | In front of everybody, always: a pillar at the edge of the screen, an overhanging branch |
| nothing, with `plane: "back"`, or nothing at all | Behind everybody, always: a rug, a thing on a far wall that the story changes |

So when the lead's feet are higher than the car's wheels he is painted first and the car
covers him. When they are lower he is painted last and covers the car. Feet exactly on a
base count as in front. Cut-outs with the same base are painted in the order the scene
lists them, the later over the earlier.

### 2. Nobody walks through anything

The scene's `walk.area` is the outline of the ground people can stand on. Inside it:

- `blocked` lists outlines where something painted into the backdrop stands;
- a cut-out or a prop can give a `solid` outline, the patch of ground it takes up. A
  cut-out blocks its patch only while it is shown;
- people who are not leads block a small patch at their feet (the lead's own companions
  do not: she can walk past them).

From these the engine builds a map of where the lead may stand, pixel by pixel, keeping
him a little clear of each blocked patch. When the player clicks, it finds a route round
whatever is in the way. A click on a place nobody can stand (inside the car, in the
river, in the sky) sends the lead to the nearest place he can. The map is made again
when the story shows or hides a cut-out that is solid.

### 3. Farther things are smaller

A scene has a `horizon`, the row of the picture the ground runs back to, and a `full`
row, where a person is drawn full size (an adult is 160 pixels tall there). In between,
size falls in a straight line with height on screen, which is what perspective does to
people standing on flat ground:

```
size = (feet - horizon) / (full - horizon)
```

The painter works from the same two numbers, so doors and wagons come out the right size
for the people. The rooms of the house go further: each is painted through one camera
whose numbers are the scene's own `horizon` and `full` (the two of them fix how high it
stands), and floor, walls, furniture, light and shadows all go through it, so a person the
engine draws stands in the room at the right size wherever they are on its floor. How a
room is painted that way is in [tools/paint/README.md](../tools/paint/README.md), "Painting
a room".

Steps shorten with size, so the walk still matches the ground. Walking into the picture
also covers more ground than walking across it: one pixel up the screen counts as 2.2
pixels sideways, both for speed and for choosing the shortest route.

Cut-outs and props do not resize themselves. They stay where they are put.

### The settings, with their defaults

| Setting | Default | Meaning |
| --- | --- | --- |
| `horizon` | 260 | The row where the ground meets the sky |
| `full` | 590 | The row where a person is full size |
| `minScale`, `maxScale` | 0.26, 1.12 | Limits, so that nobody vanishes or fills the screen. A scene with steps or a far doorway often sets `minScale` to hold people at the size that fits it. |
| `walk.area` | the lower half of the picture | The outline of the walkable ground, as a list of points |
| `blocked` | none | Outlines inside it where something stands |
| `planes[].base`, `planes[].plane` | none, `"floor"` | See the table above |
| `planes[].solid`, `props[].solid` | none | The outline of the ground a thing takes up |
| `actors[].solid` | a small box at their feet | `false` lets the lead walk through them |

`tools/storyboard.html` draws each scene with its walkable ground, its blocked patches,
its clickable areas and the base line of each cut-out.

---

## 4. The people

### How a person is drawn

People are not stored as pictures. Each is a **jointed figure** with a page of settings,
and every picture of them is worked out from it.

```
people.js    who they are: proportions, skin, hair, a face, clothes, colors
   |
rig.js       a pose (how each joint is bent)  ->  where each joint is  ->  turned to face one of eight directions
   |
pix.js       solid shapes  ->  pixel art
```

The last step gives the look: the hand-pixelled figure of the early 1990s at a larger
size. `pix.js` works from a short list of rules:

- Hard edges. Nothing is smoothed.
- Flat areas of color. A form is its plain color, and the side turned from the light is
  one darker tone, with a clean edge between the two. Nothing is modelled round.
- One light, from the upper left, on every person in every scene and every era.
- A dark line round the figure, so it reads against any backdrop.
- A shadow under the chin and under each hem, a drawn line where cloth folds, and a
  small careful face.

A full-size adult is 160 pixels tall. The pixels are worked out at the size that is
asked for, so a person standing anywhere in a scene's depth is crisp. (Someone walking
borrows the nearest of a ladder of sizes: see "Keeping it fast" in section 1.)

An **animation is a pose that changes with time:**

| Animation | How it is made |
| --- | --- |
| Walk | 12 pictures to a cycle of two steps, in 8 directions. The foot on the ground moves back at the speed the body moves forward, so feet do not slide. The cycle is driven by ground covered, not by time, so it stays in step at every size. |
| At rest | Slow breathing, and a blink every few seconds |
| Talking | A gesture and three mouth shapes. There are twenty gestures and each person uses a few of them (see below). The line decides which, so a line always plays the same way. |
| Reaching | Out at chest height, or bending down to the ground. Anyone in a skirt dips at the knee and bows a little, and does not bend double. |
| Praying | The head bowed, the eyes shut, the hands folded in front, eased into over about a quarter of a second and held, through whatever is said, until a script lets it go. Each of the family prays in their own way (`pray`, below). |
| Sitting | Cross-legged on the ground, or on a seat: a chair, a bench, a stool, a step. Someone who is found sitting breathes, blinks and talks sitting down, with the same gestures of their own that they would use standing. |

This is the method of one of the games this one looks up to, with a puppet in place of an
actor. For King's Quest VI, Sierra filmed costumed actors, brought the video into the
computer, and had animators touch up each frame to sit well on the painted
backgrounds. A puppet costs nothing to shoot again: change Dad's shirt, his height or
his stride in `people.js` and every picture of him follows.

What it does not give is an artist's hand on each frame. If a character later deserves
hand-drawn frames, the cast layer does not care where a picture comes from. It asks for
"this animation, this frame, this direction, this size" and paints what it is given.

`tools/sprites.html` shows every person in every direction, moving, with the single
pictures underneath.

### Who is in the cast

Twenty-four people, all in `js/art/people.js`:

| Where | Who |
| --- | --- |
| The family | `dad`, `son`, `mom`, `bigsis`, `lilsis` |
| Egypt | `scribe` (sits cross-legged on the ground), `carrier`, `overseer` (a staff in his right hand), `hauler1`, `hauler2`, `hauler3`, `guard` (the tallest, a long staff upright), `lampboy` (sits on a bench; can stand and walk), `goldsmith` (sits on his stool) |
| Rome | `keeper`, `washer`, `urchin` (sits on the kerb), `soothsayer` (sits on a step, with a staff), `senator`, `doorkeeper`, `clerk` (sits at his table), `dateseller` (a basket of dates on his hip) |
| Nevada | `oldtimer` (in a lawn chair that is drawn with him), `agent` |

Two more figures are the same two men after the story has changed them:
`goldsmith-shades` (the goldsmith with the sunglasses on) and `guard-shade` (the guard
holding the windshield shade up, his staff laid on the sand). A scene swaps one for the
other in place, under the same id, so the man keeps his name and the color of his words.

### Making someone themselves

Colors and clothes say who a person is when they stand still. These settings in
`people.js` say it when they move, and they are worth as much care:

| Setting | What it is | In the cast |
| --- | --- | --- |
| `stance` | How they stand when nothing is happening: hands `"clasped"`, `"akimbo"`, `"behind"` the back, holding one `"elbow"`, arms `"folded"`, thumbs in their `"straps"`, a fist on a `"hip"`, something to `"carry"`, hands on a `"belly"` | Mom's hands are clasped. Little Sister's fists are on her hips. Big Sister holds one elbow. The man in gray keeps his hands where you cannot see them. |
| `walk` | How they move: length of stride, how far the arms swing and how bent they are, lean, how high the knees come, what the head does | The Son bounces with his fists pumping. Mom takes short steps and her arms hardly move. Little Sister stomps with straight arms. |
| `pace` | How fast they walk, in picture pixels a second at full size (155 unless it says otherwise) | The water carrier plods at 110. The street boy darts at 190. |
| `gestures` | What their hands do when they talk, as a short list of numbers | Dad nods, makes a point, shrugs, puts a hand on his hip. The Son throws both arms up. The clerk wipes his brow and counts on his fingers. |
| `hold` | An arm that is always busy with something | The overseer's staff, the youngest hauler's loaf |
| `pray` | How they stand to pray: how high the folded hands are, how far the head bows, and whether the hands are clasped tight and the eyes squeezed shut | Dad folds his big hands low in front of him, his head well down. The Son takes his cap off and holds it in both hands. Mom folds her hands at her breast, and her handbag slides down to the crook of her elbow. Big Sister prays exactly as she was taught, hands together at her breast. Little Sister prays with all her might: hands clasped tight under her chin, eyes squeezed shut. |
| `seated`, `sit` | For someone who is found sitting: `"ground"` or `"chair"`, and what exactly they sit on (a chair, a bench, a stool, a step, or a height) | The scribe, the lamp boy, the goldsmith, the street boy, the soothsayer, the clerk, the old-timer |
| `rest` | Where an arm lies when a pose leaves it alone | The scribe's pen hand |

The twenty gestures: a nod, one hand making a point, a shrug, a hand on the hip, both
arms up, a hand to the heart, a hand to the chin, showing off muscles, an open hand,
both hands waving, pointing straight ahead, a finger in the air, arms folded, a hand
cupped to the ear, a shaken fist, waving something away, wiping the brow, counting on
the fingers, both hands spread wide, and a thumb over the shoulder. Scripts never name a
gesture: a line picks one from the speaker's own list.

The engine never asks the rig for "a walk". It asks for *this person's* walk, through
`poses` in `rig.js`, so nobody on stage moves like anybody else. The rig also knows
skirts and kilts, a round collar, overalls with a bib and straps, wigs, beards, dark
glasses, and things to carry.

Three things a scene writer needs to know:

- **Where a seated person is put.** Their place in the scene (`at`) is the ground under
  their hips, and the seat itself is painted into the picture, or drawn with them.
- **Words sit just above the head.** The rig says how tall each person is as they are
  found, sitting or standing (`tallOf` in `rig.js`), and a speaker's words are put ten
  pixels above that, for a seated scribe far away and a standing father close by alike.
  (A staff that rises above its owner's head is not counted.)
- **A person's place does not move with them.** Anyone can be walked by a script, but the
  patch of ground they block stays where the scene first put them, so give anyone who
  walks `solid: false`.

[CHARACTERS.md](CHARACTERS.md) is where these choices come from.

---

## 5. Intro movies and cutscenes

A cutscene is **one async function**, kept in `js/content/cutscenes/`. Each `await` is
one beat of the storyboard, so the file reads like a shot list:

```js
await g.card("n0tk3r presents", "", { plain: true, ms: 1700 });
const road = highway(g, "A desert highway at dusk.");
await road.ready;                                            // every picture is here
await g.fade(0, 900);
await g.tween(1500, (k) => road.hole(k), ease.out);          // the sun opens into the hole in time
await g.say("intro.3", "intro.4");
```

### Why not a video file

- **Size.** The intro is a script of a few KB and six pictures, which the title uses
  too. A 40-second video is tens of megabytes.
- **One look.** It uses the same painting, the same wagon and the same light as the
  game, so there is no jump in style between the movie and the title.
- **It can be skipped properly, paused, subtitled and translated.**

A video can still be used for a single shot if one is ever wanted: put a `<video>`
on the stage inside a cutscene function and `await` its `ended` event.

### How skipping works

When the player presses Skip (or Esc), the engine sets `clock.skipping = true`.
Every `wait`, `tween` and `say` then finishes at once. The same function runs to
its end in a few milliseconds and leaves the stage exactly as it would have been.
Nobody has to write a second "skipped" version of each scene, and the two can never
disagree.

### The opening

```
click to begin  ->  studio card  ->  the road at dusk  ->  the sun opens into a portal
->  the road sign changes its mind  ->  the wagon drives in, white flash
->  the time tunnel, years flying past  ->  white flash
->  the title: the papyrus strip unrolls, the menu arrives
```

- The **first click** is needed anyway: browsers keep sound off until the player
  does something. So the game opens on a "Click to begin" screen, and that click
  both starts the movie and unlocks audio.
- The intro plays in full the first time. After that the game opens on the title,
  and the menu has **Watch the intro**. (`index.html?intro` forces it.)
- **The movie and the title are the same stage.** `cutscenes/highway.js` puts the painted
  highway up (`art/scenes/highway/`) with the few parts of it that change, and hands back
  what a script does with them: `road.hole(k)` opens the sun into the hole in time,
  `road.strike(k)` and `road.bc(k)` repaint the sign, `road.drive(row)` puts the wagon
  on the road at the right size for that row. Each takes a number from 0 to 1, so a tween
  can run it and a skipped movie lands on the same picture. `intro.js` runs them in
  order. `title.js` sets them all to their ends: the engine calls the cutscene named
  `title` to dress the stage behind the title screen, waits for it, and puts the game's
  name and the menu over it.
- The wagon is a painted sprite that a cutscene moves about
  (`g.view.cast.addPicture`, in the table at the end of section 10). The sun and the two
  changes to the sign are painted too, but lie on the live layer, because the hole has
  to open over them. The hole and its glow are light, and are drawn.

---

## 6. Saved games

### What is saved

One small object (`js/engine/state.js`): the act, the scene, which lead the player
controls, which leads they can switch between (the team), where each lead is standing
(in picture pixels) and which way they face, each lead's pockets, and the list of story
facts ("flags"). Nothing else. Every scene rebuilds itself from those facts: its
cut-outs read them to decide whether they show and in which state, and its `setup`
function does anything that is left. That is why a save is a few hundred bytes.

### Three ways to save

| | Where it lives | When |
| --- | --- | --- |
| Autosave | This browser | On entering a scene, after each action, and when the tab is hidden |
| Slots 1 to 3 | This browser | When the player picks **Save game** |
| Save file | The player's computer | **Save to a file...** |

Browser storage belongs to one browser on one device and can be cleared. The
**save file** is the player's own copy: a small `.json` file named like
`point-a-to-bc-save-2026-10-06-0021.json`.

- **Saving to a file.** Chrome and Edge show a real Save dialog. Firefox and Safari
  do not have that feature, so there the file goes to the downloads folder.
- **Loading from a file.** **Load game > Load from a file...**, or drop the file
  anywhere on the game. It works on the live site from any device, so a game started
  on a laptop can be finished on a phone.

### What keeps saves safe

Each save is wrapped in an envelope:

```json
{ "magic": "from-point-a-to-bc", "v": 3, "savedAt": "...", "meta": { "era": "...", "lead": "Dad" },
  "data": { ... }, "check": "9f3a1c07" }
```

- `magic` rejects files that are not from this game.
- `check` is a checksum of the data. A damaged or hand-edited file is refused with a
  plain message. (It catches accidents. It is not a lock against cheating.)
- `v` is the save version, now **3**. When the game changes shape, add an upgrade step
  to `migrations` in `save.js` and old saves keep working. There are two:
  - **1 to 2.** Version 1 knew only Dad and the Son. Such a save gets a team, and places
    and pockets for the rest of the family.
  - **2 to 3.** The stage became one 800x600 picture. Where people stood in an older save
    is on a grid that no longer exists, so it is forgotten: each lead keeps their scene
    and their pockets, and appears on that scene's own mark for them.
- A save can name things this version does not have. A lead left in a scene that is gone
  is nowhere until the story puts them somewhere, and cannot be switched to. A carried
  thing that is gone is left out of the pockets. A save whose own scene is gone is turned
  away in words, and the game carries on.
- Volume and subtitle settings are stored apart from saves, so loading a save from
  a friend never changes your volume.

---

## 7. Sound, music and dialogue

### The mixer

```
master -- music   (each track fades in and out on its own)
       |- effects
       '- voices   (while a voice plays, the music drops to about a third)
```

Each has its own slider in Options.

### Music

Each era has a theme, named in `js/content/world.js` and described in
`js/content/sound.js`. Changing scene cross-fades to the new era's theme. A scene can
name a theme of its own with `music`, or give a function of the game that names one, so
that the story can change it. Big Sister's attic plays its own quiet track until the
batteries are taken out of her sound machine, and the house's after that:

```js
music: (g) => (g.flag("home.retreatQuiet") ? "home" : "retreat"),
```

The engine asks again each time the scene is entered (`g.musicOf(scene)`). A script that
has just changed the story asks at once: `g.music(g.musicOf(g.scene))`.

Until music is written, each theme is a **short pattern played by a built-in
synthesizer**, so the game already has a different sound for the title, the road,
Egypt, Rome, home in the evening, Big Sister's attic, the Nevada desert and the tunnel.
To use a real recording, add one line:

```js
egypt: { src: "audio/music/egypt.{ext}", volume: 0.8 },
```

Long tracks are **streamed**, so a five-minute piece starts at once and is never
held whole in memory. Short effects are generated or kept in memory.

**File types.** Export each track as MP3, which every browser plays. Opus is smaller
at the same quality; if you add it, list it first in `formats` and the engine picks
whichever the player's browser can play.

A later step for an adventure soundtrack: split a theme into layers (a bed, a melody,
a tension layer) and fade layers in and out as the story moves. The mixer already
gives each track its own volume, so this is an addition, not a rewrite.

### Dialogue, and the road to full voices

Scripts never contain words. They contain **line IDs**:

```js
await g.say("egypt.river.look");
```

The words are kept one file to an act, in `js/content/lines/`: `egypt.en.js`,
`rome.en.js`, `home.en.js` and `nevada.en.js`, and `common.en.js` for the lines that
belong to no one act (the opening movie, what the family say when they look at one
another or hand something over, and the stock replies for things nobody wrote a line
for). So an act can be written, read aloud and recorded as a piece.

```js
"egypt.river.look": ["dad", "Either that's the Nile or a very committed car wash."],
```

`js/content/lines.en.js` gathers the five files into the one list the engine uses, and
warns in the console if the same ID is written twice.

That one decision is what makes a "talkie" version cheap later:

1. **Record** a line and save it as `audio/voice/en/egypt.river.look.mp3`.
2. **Add** its ID to the `voices` list in `sound.js`.

That is all. The engine plays the recording, keeps the words on screen until the
voice finishes, moves the speaker's mouth and hands, and turns the music down underneath.
Lines without a recording keep showing as timed text, so voices can arrive a scene
at a time. Options has **Show the words on screen** and **Play recorded voices**.

The same files are the voice actors' script (the storyboard page exports them as one
spreadsheet, a row per line, grouped by character), and a translation is a copy of the
files with the same IDs.

On screen, each character speaks in their own color, just above their own head, in the
manner of classic adventure games. While a close-up is showing, the words run along the
bottom of the stage, clear of what is being looked at.

---

## 8. Story: guided, but not a straight line

The shape, taken from how classic adventure games were planned (see the notes on
the puzzle-document method in the project):

```
Act:   opening cutscene
         |
   +-----+------+
 chain A      chain B        two or three things to work on, in any order
   +-----+------+
         |
       the gate               needs every chain
         |
   closing cutscene  ->  next act
```

- **Inside an act the player chooses the order**, so being stuck on one puzzle
  never stops the game.
- **The gate needs everything**, so every player reaches the same closing scene, and
  the story keeps its arc like a film or a book.
- **Acts are the spine.** Each should end on a turn in the family's story, not only on a
  solved puzzle.

### The story is data

Each act is a file in `js/content/acts/` (`prologue.js`, `egypt.js`, `rome.js`,
`home.js`, `nevada.js`) that lists its beats. `js/content/story.js` puts the acts in
order and holds what belongs to no single act: where a new game starts, the stock
replies, and what the leads say about one another. A beat says what it needs and what
it sets:

```js
{ id: "egypt.pass", kind: "puzzle", chain: "A", title: "Give the scribe the map to write on: he writes a pass",
  lead: "dad", scene: "egypt-site", needs: ["egypt.hasMap", "egypt.penGiven"], sets: "egypt.hasPass",
  hint: "hint.egypt.mark" },
```

From that list the game gets three things for free:

- **Hints.** The Hint button finds a beat that is open right now and has the lead
  say its hint line. In a team a beat carries a hint for each lead: the one whose job
  it is says what to try, and the others say whose job it is ("that is one for your
  sister"), so asking for help as the wrong person still points the right way.
- **A check.** At every start the engine walks the story as a player would and
  warns in the console if a beat can never be reached or names a scene that does
  not exist.
- **A storyboard.** `tools/storyboard.html` draws every act, chain and scene from
  the same data. Plan there, and the plan cannot drift from the game.

Today there are a prologue and four acts: Egypt (four scenes), Rome (three), home (five,
the rooms of the house), and the Nevada desert. The puzzle documents in `docs/` say what
happens in each.

### Storyboarding before the art exists

A scene file does not need a painting. Leave out `picture` and the engine **sketches**
the scene: sky, ground, and a labelled box for each clickable thing, in the era's
colors. So the order of work can be:

1. Write the beats in the act's file and look at them on the storyboard page.
2. Write each scene as boxes and lines (see `scenes/sketch-example.js`), and play
   the whole act through. Fix the puzzles and the pacing while changes are cheap.
3. Paint the scenes that survived. The painter measures the finished picture
   (`layout.json`), and the numbers in the scene file are changed to match. If a picture
   and a script disagree about where something is, the picture wins.

### Five leads, apart and together

Dad, the Son, Mom, Big Sister and Little Sister can each be played. Every lead has a
place and pockets of their own; `state.active` says who the player is, and `state.team`
lists who they can switch to at this point in the story. A script sets it:
`g.team(["mom", "bigsis", "lilsis"])`. Each member of the team has a portrait at the
top left of the screen.

**Apart.** Dad and the Son are in different centuries. Switching to the other one
travels to wherever he is. The story can also cut between leads by itself, as it does
at the end of each act. A strong fit for this premise: something sent through a door
in one era turns up in another, so people who are apart can still help each other.
(The coin the Son throws into the door in Rome falls out of the sky in Nevada.)

**Together.** Mom and the girls go through the house as one. Each of its five scenes (the
living room, the landing, Dad's study, Little Sister's room and Big Sister's attic) says so
with `party: ["mom", "bigsis", "lilsis"]`: when the one being played takes the stairs, a
door or the attic ladder, the other two come too and arrive beside her, each on a place of
her own, and switching between them is instant because nobody has to go anywhere. ("A
scene for several leads" in section 10 shows how a scene says where each of them arrives.)
In a party:

- **Each can do what the others cannot.** A clickable thing can answer each lead
  differently: `use: { lilsis: intoCloset, mom: "home.closet.use.mom", bigsis: "home.closet.use.bigsis" }`.
  That is the whole mechanism behind "only Little Sister fits" and "he will only talk
  to Mom", and the refusals are where the jokes are.
- **They talk.** Click a companion to talk to her. The scene supplies the exchanges
  (`talk`), and what has not been heard yet comes first.
- **They hand things over.** Hold something and click a companion, or her portrait, to
  give it to her. The scene can react (`given`): Big Sister, handed her father's note,
  reads what it means.
- **Each has her own pockets, and the screen says whose.** The inventory along the
  bottom is always there, with a tag: "Mom's handbag", or "Mom's handbag: empty". (What
  each lead's pockets are called is `keeps` in `world.js`.) A portrait carries a small
  number when that person is holding something, and pointing at it says what.
- **They stay where they are left.** Within a scene, companions do not follow the lead
  about. When the lead walks up to something, she stands beside a companion who is
  already there, not on top of her.

The two halves of the family meeting in one scene needs nothing new: put all five in a
`party`.

---

## 9. One look across every era

The risk in a time-travel game is a different art style per period. The answer here
is that **an era changes what is painted, and nothing about how.**

### What stays the same in every era

1. **The grid.** One 800x600 picture, and every painting, person and cut-out on it at
   the same size of pixel.
2. **The way a scene is painted.** The same four passes, the same brushes, the same
   speckled finish, the same rules of light and depth (section 2), whether it is a tomb
   or a living room.
3. **The people.** One figure, one way of shading it, one light from the upper left,
   for a pharaoh's scribe and a man from the government alike (section 4).
4. **Darkness is a color.** Shadows are a darker, cooler tone of the thing itself, never
   pure black.
5. **The type.** Koine Road for titles, cards and buttons; a plain bold sans for speech.
6. **The cards.** Every era opens with its name on a torn strip of papyrus.

### Three groups of color that never mix

| Group | Colors | Used for | Changes? |
| --- | --- | --- | --- |
| **Time** | neon cyan, magenta, violet, white core | Portals, the tunnel, anything time travel has touched, highlights in the interface | Never |
| **Travellers** | Dad's yellow shirt, the Son's blue hoodie and red cap, Mom's emerald dress, Big Sister's indigo cardigan, Little Sister's pink overalls and yellow boots, the red wagon | The people and things from the present | Never |
| **Era** | The warm stone and sand of Egypt, the brick and blue shadow of a Roman street, lamplight and wallpaper at home, the dust of Nevada | The world of each period | Per era |

Because of this, in any screenshot from any era you can tell at a glance what
belongs to the period, who the visitors are, and where time is leaking through.

Each member of the family owns one color that nobody else in the family wears, and
their words on screen are a pale tint of it. Everyone else who speaks has a tint that
nobody else in the game uses (`cast` in `world.js`).

### How futuristic and ancient blend

They are kept apart on purpose, and the contrast is the style:

- **The world is painted, warm and matte.** Earth, stone, water, linen, wood.
- **Time travel is the only thing that glows, and the only thing drawn smooth.** Neon
  rings, soft light, dashed lines. A wormhole never looks like part of the world it
  has opened in, because it is not made of the same stuff: it is drawn by code on the
  live layer and never painted. Wherever the two meet, the neon lights the scene: the
  road turns cyan under the portal.
- **Doors in time are invisible until the puzzle that opens them is solved.** Before
  that there is nothing to see: only what people say about a hum.
- **The interface is ancient, with neon for "active".** Menus, buttons, cards and
  the title are ink on papyrus, in Koine Road. The selected item or tool turns cyan.
- **One signature shape.** A wormhole is always the same four dashed rings, turning
  in opposite directions, in every era and in the browser tab icon (`portal` in `kit.js`).
- **A possible motif to grow:** let the eras leak into each other as the story goes
  on. A Roman column with a neon crack. A hieroglyph that is a road sign.

### The era palettes

`css/tokens.css` still gives each era a palette of seventeen slots (eight sky bands, two
silhouettes, three grounds, a dark, a light, two features), and the stage carries
`data-era="egypt"`. The paintings do not use it. It colors what is still drawn by code:
the sketch of a scene that has not been painted, props, and the storyboard page, which
shows all the palettes side by side.

---

## 10. How to add things

**A line.** Add it to the act's file in `js/content/lines/`. Say it with `g.say("its.id")`.

**A scene.** Copy `js/content/scenes/engine-proof.js`, which is the worked example of a
painted scene, change it, and add its id to the list in `js/content/scenes/index.js`.
Every number is a pixel of the picture. Here is that file with its comments taken out,
and a few lines added (marked) to show the forms it does not use:

```js
const art = "art/scenes/egypt-crash/";

export default {
  id: "engine-proof", era: "egypt", name: "Where the wagon came down",

  horizon: 262, full: 590, minScale: 0.3,       // depth: the row the ground runs back to, the row where a person is full size
  walk: { area: [[352, 300], [640, 300], [780, 326], [780, 596], [60, 596], [150, 470], [240, 384], [312, 322]] },   // the ground people can stand on
  blocked: [ [[296, 438], [357, 438], [384, 457], [296, 455]] ],        // (added) patches of it where something painted into the backdrop stands
  spawn: { default: [420, 572] },               // where the lead arrives. A lead's own id names a mark of their own.
  facing: "S",                                  // (added) which way the lead faces on arriving. This is the usual way.
  exits: ["egypt-site"],                        // (added) scenes that can be walked to from here: their pictures are made ready ahead of time

  picture: art + "back.png",                    // the backdrop
  planes: [                                     // painted cut-outs, sorted with the people
    { id: "palms", src: art + "palms.png", base: [[187, 407], [298, 321]] },     // a base line: they stand in a row along the bank
    { id: "wagon", src: art + "wagon.png", base: [[490, 541], [790, 537]],
      solid: [[470, 528], [790, 522], [796, 548], [470, 556]] },                 // the ground it takes up
    { id: "papyrus", src: art + "front.png", plane: "front" },                   // always in front
    { id: "trunk", src: art + "trunk-open.png", base: 541, when: (g) => g.flag("egypt.trunkOpen") },   // (added) there only while the story says so
  ],
  live(art, g) { return art.portal(500, 300, 40, "door"); },                     // (added) light, drawn and not painted

  actors: [{ id: "carrier", kind: "carrier", at: [260, 451], face: "SE" }],      // (added) people who are not the lead
  hotspots: [
    { id: "pyramids", name: "pyramids", rect: [432, 78, 368, 172], look: "egypt.pyramids.look" },       // a box: x, y, width, height. (A circle is [x, y, radius].)
    { id: "wagon", name: "wagon", verb: "Search",                                // (the verb is added: what the pointer says it will do)
      poly: [[462, 492], [560, 470], [600, 420], [650, 388], [750, 394], [790, 440], [790, 520], [740, 544], [462, 520]],
      walkTo: [600, 574], face: "N",            // where the lead goes to do it, and which way he then faces
      look: "egypt.wagon.look",                 // a line ID,
      use: async (g) => { ... },                // (added) or a function,
      useWith: { reed: async (g) => { ... } },  // (added) or a reaction to a carried thing
      when: (g) => !g.flag("egypt.towed") },    // (added) there only while this holds
  ],
  setup(g) { /* (added) anything the picture still needs to match the story facts */ },
  async enter(g, from) {                        // what happens on arrival. It must be safe to run twice, so it checks its own fact.
    if (g.flag("proof.arrived")) return;
    await g.say("egypt.arrive.1");
    g.flag("proof.arrived", true);
  },
};
```

Directions are compass points on the screen: `"N"` is away from the player, `"S"`
toward, `"E"` screen right, and the four in between.

To jump straight to a scene while building it: `index.html?scene=rome-street&lead=son`.
Every act before that scene's own counts as played, so hints work. Add
`&flags=rome.arrived,rome.sawStreet` to start with more of the story done. Hold **H** in
the game to see every clickable area. The storyboard page draws each scene with its
walkable ground, its blocked patches and its base lines, and has a **Play from here**
link under every scene.

**A painted cut-out** is an entry in the scene's `planes`. What it can say:

| Field | Meaning |
| --- | --- |
| `id` | Its name. Cut-outs, props and people share one set of names in a scene; a clash is pointed out in the console. |
| `src` | One picture |
| `states`, `state` | Several pictures, one shown at a time. `states` is `{ name: picture }`. `state` is a name, or a test of the story that gives one: `state: (g) => (g.flag("home.online") ? "login" : "offline")`. With no `state`, the first listed shows. A name with no picture shows nothing. |
| `frames`, `fps` | Several pictures shown in turn, on the game clock (steam, a flame) |
| `when` | A test of the story. The cut-out is there only while it passes. |
| `base`, `plane` | Where it sorts among the people (section 3) |
| `solid` | The outline of the ground it takes up, blocked while it shows |
| `at`, `foot`, `scale` | For a small cropped picture: the point `foot` of the picture is put at `at` on the stage, at `scale`. Without them a cut-out is the size of the stage and is laid over it at (0, 0). |

`when` and `state` are read again every time a story fact changes, and when a script
ends. So a scene never dresses its own picture: a script records a fact, and the picture
follows. They are first read before anyone is on stage, so they should ask about facts
(`g.flag`, `g.has`), not about where somebody is.

A script can also take hold of one: `g.plane("trunk").show(true)`, `.set("login")`,
`.fade(0.5)`, `.place(x, y, scale)`. What a script sets by hand holds until the scene is
built again.

**Light.** A wormhole, a beam, a glow: return it from the scene's `live(art, g)`, as
drawing markup in picture pixels. `art.portal(x, y, radius, id)` is the door in time.
Give a part an `id` and a script finds it with `g.q("#door")`, to fade, move or scale it.
The live layer is under the cast.

**A scene for several leads.** `js/content/scenes/home-living-room.js` is the one to
copy. On top of the above it has:

```js
party: ["mom", "bigsis", "lilsis"],                         // they are here together
spawn: { default: [...], mom: [...], bigsis: [...], lilsis: [...],       // a mark each, for when the act opens here
         fromLanding: [...] },                              // a way in: where the lead arrives, down the stairs
arrive: { fromLanding: [[...], [...]] },                    // where the other two arrive by it: in the order of `party`, the lead left out
hotspots: [
  { id: "stairs", name: "the stairs", verb: "Go up", poly: [...], walkTo: [...],
    use: (g) => g.goto("home-landing", { spawn: "fromStairs" }) },        // the way out names the way in at the other end
  { id: "closet", name: "closet under the stairs", rect: [...], walkTo: [...],
    look: { mom: "home.closet.look.mom", bigsis: "home.closet.look.bigsis", lilsis: "home.closet.look.lilsis" },
    use: { lilsis: intoCloset, mom: "home.closet.use.mom", bigsis: "home.closet.use.bigsis" } },   // one answer for each lead; `any` is for whoever is not named
],
talk: { mom: { bigsis: [["line.a", "line.b"], { when: (g) => g.has("coin"), say: ["line.c", "line.d"] }] } },   // what Mom and Big Sister say when Mom clicks her
async given(g, item, to, from) { /* something was handed over */ },
```

All five scenes of the house are built this way. A way in is a name. The scene that is
left gives it (`g.goto("home-landing", { spawn: "fromStairs" })`), and the scene that is
entered puts the lead on its `spawn` mark of that name and the two who are not leading on
its `arrive` places of that name. Without an `arrive` for the way they came, each of them
goes to her own mark in `spawn`, or beside the lead. One who is already standing in the
scene (after a saved game is loaded, say) stays where she is. So the landing has a way in
for each way onto it (the stairs, the attic ladder, each room that opens off it), and each
of the other four scenes has one way in from the landing.

**A painting.** Write the scene file first and play it as a sketch. Then paint it
(section 2, and the guide in `tools/paint/`), put the pictures in
`art/scenes/<scene id>/`, name them in the scene file, and take the numbers from the
painter's `layout.json`. Run `python3 tools/stamp.py` (see "Publishing a new version").

**A character.** Write down who they are first ([CHARACTERS.md](CHARACTERS.md) has the
pattern). Then copy the nearest entry in `js/art/people.js` and change the proportions,
clothes and colors, and give them a `stance`, a `walk` and a list of `gestures` of
their own (section 4). Give them an entry in `cast` in `world.js` with
`sprite: "that-name"` and a color for their words, and put them in a scene's `actors`
with `kind: "that-name"`. Add `lead: true` in `cast` if the player can control them: they
then get a place, pockets and a portrait. Open `tools/sprites.html` to see them from
every side, moving. Anything the standard figure does not have (a hat, a backpack, a
staff) goes in the entry's `extras` function.

**A thing to carry.** Add it to `items` in `world.js` with a name, a `look` line and an
`icon`. An icon whose name ends in `.png` is a painted picture in `art/items/` (64x64);
any other name is one of the small drawn icons in `kit.js`. A thing a script names that
is not in the list does not stop the game: it is shown by its id, with a note in the
console.

**A close-up.** For something too small to read in the scene (a screen, a notice), draw
it large and show it from a script: `g.closeup(g.art.notice(), "The notice on the fence")`.
People go on talking under it, with their words along the bottom, and it is put away
when the script ends. The kit's close-ups (`monitor`, `screens`, `notice`) are drawn on
the old 320x200 grid, which is what `g.closeup` expects; for a drawing made in picture
pixels say so: `g.closeup(markup, label, { grid: [800, 600] })`.

**A prop drawn by code.** The scenes are painted, and what stands in them is a cut-out.
`js/art/props.js` is still there for a scene that has no painting yet: add an entry with
a `draw` function, and list it in the scene's `props` with a place (`at`), a `scale`,
and if wanted a `solid`, a `plane`, a `base` and a `when`.

**An era.** Add an entry in `eras` in `world.js`, a theme in `sound.js`, and a palette
block in `css/tokens.css` (for its sketches).

**A cutscene.** Add a function in `js/content/cutscenes/` and list it in `main.js`.
Play it with `await g.cutscene("its-name")`.

**A beat of story.** Add it to the act's file in `js/content/acts/`, and have the script
call `g.flag("the.fact", true)` when the player does it. Open `tools/storyboard.html` to
see it in place and to see any warnings.

### Publishing a new version

GitHub Pages lets a browser keep each file for ten minutes. The game is some fifty code
files and more than eighty pictures, so without care a browser can end up running new
files beside old ones. It happened on 2026-10-06: for some minutes after a push, the
title came up and New game went to a black screen. One sequence reproduces that exactly
with the two versions involved: the earlier version's page is on screen when the later
one goes live; New game asks the server for one scene file, is given the new one, and
the old engine cannot run it. Four things now prevent that.

1. **Every file has an address that changes when the file does.**
   `python3 tools/stamp.py` works out a fingerprint of each file in `js/`, `css/` and
   `art/` and writes them into `index.html` (and the two tool pages):
   - an import map, which is the browser's own table for "when a module asks for this
     file, fetch that address": `./js/engine/game.js` becomes `./js/engine/game.js?v=3f2a…`;
   - the same kind of address on each style sheet;
   - a list of the pictures with their fingerprints, from which `js/engine/assets.js`
     makes each picture's address the same way.

   No game file changes for this: modules go on importing `./state.js`, and scenes go on
   naming `art/scenes/egypt-crash/back.png`. A copy of an old file that a browser kept is
   never used by a new page, because the new page asks for a different address. After an
   update only the files that changed are downloaded again.
2. **The page checks that it is the newest.** `index.html` carries `data-build`, a
   fingerprint of everything, a picture included. Before it starts the game, the page
   asks the server for itself afresh. If the server's copy has a different `data-build`,
   the browser was showing a page it had kept, and it reloads once to get the new one.
3. **A game in progress asks the server for no more code.** Every scene file is fetched
   before "Click to begin". A tab left open while a new version goes live carries on
   with the version it has, whole. Reloading the page gets the new one.
4. **A game in progress keeps its pictures.** A picture is fetched once in a session and
   the file is then held in memory until the page is closed. Whatever shows it after
   that (the backdrop, the cast, an inventory button, a painted part on the live layer)
   is given the held copy and never asks the server again. And the whole game's pictures
   are fetched behind the title, within seconds of its coming up (section 1). So a
   version published in the middle of somebody's game cannot hand them a new painting to
   go with their old script. (For those first seconds it still could: a static server
   answers an old address with the new file.)

**What you do.** After changing anything in `js/`, `css/` or `art/`, run
`python3 tools/stamp.py`, then commit and push. Or turn on the commit hook once (the two
commands are at the top of `tools/hooks/pre-commit`) and git runs it at every commit.
`python3 tools/stamp.py --check` says whether the pages are up to date and changes
nothing. `tools/serve.py` stamps whenever you open the game locally, and tells the
browser to keep no copies at all, so what you see locally is always the files as they
are now: reload the page to see a picture you have just repainted. If a commit does go
out unstamped, nothing breaks that did not break before: for ten minutes a browser may
use a copy it kept of a file that has changed.

**If something goes wrong anyway, the game says so in words.** If it cannot start, the
start-up panel says "The game could not start", gives the reason, and offers Reload. If
a scene breaks while it is being built, or a save will not open, the game goes back to
the title screen with a note. A picture that will not load is named in the console; a
scene whose painting is missing is sketched; a cut-out that is missing is simply not
there. A script that stops half-way through a fade does not leave the picture black.

**Not covered yet.** Sound files are not stamped, because there are none; when there
are, add them to `tools/stamp.py`. A browser too old for import maps (before 2023) still
loads the game, by the plain addresses, with the old risk.

### What scripts can do

| Call | Does |
| --- | --- |
| `await g.say("id", "id2")` | Speaks lines in order |
| `await g.choose([{ id, line }])` | Offers things to say; gives back the chosen `id` |
| `g.flag("name")`, `g.flag("name", true)` | Reads or records a story fact. Recording one makes the cut-outs and the clickable areas read their tests again. |
| `g.give("item")`, `g.take("item")`, `g.has("item")` | Pockets of the current lead |
| `g.holder("item")`, `g.item("item")` | Which lead is carrying a thing, or `null`; and the thing's own entry in `items` |
| `await g.goto("scene", { via: "wormhole" })` | Changes scene by fade, cut or time tunnel. `{ spawn: "name" }` arrives on that mark of the scene's `spawn`, and the rest of a `party` on its `arrive` places of that name ("A scene for several leads", above). |
| `await g.card("Ancient Egypt", "about 1920 B.C.")` | Shows a title card. (Egypt is about 1920 B.C. because the game counts the years before Christ from the Bible's own genealogies, as Archbishop Ussher counted them: see "How the game counts the years" in [CHARACTERS.md](CHARACTERS.md#how-the-game-counts-the-years).) |
| `await g.cutscene("intro")` | Plays a skippable cutscene |
| `await g.wait(ms)`, `await g.tween(ms, (k) => ...)`, `await g.fade(1)` | Timing, motion, fades |
| `g.music("egypt")`, `g.sfx("portal")` | Sound. `g.musicOf(g.scene)` is the track the scene plays now: its `music`, which may depend on the story, or its era's. |
| `await g.walkTo(x, y)`, `await g.walkTo(x, y, "scribe")` | Walks the lead, or someone else, to a place, round whatever is in the way |
| `await g.moveTo(x, y)`, `await g.moveTo(x, y, "agent")` | Walks in a straight line to a place the player could not click on (into a closet) |
| `await g.reach()`, `await g.reach(true)` | The lead reaches out, or bends down to the ground |
| `g.lead.hold()`, `g.lead.hold(false)` | Someone keeps an arm held out while people talk (holding a thing up), until told to let it drop |
| `g.actor("mom").pray()`, `g.actor("mom").pray(false)` | Someone stands in prayer, in their own way (section 4), through whatever is said, until told to stop. It is for someone standing still: end it before they walk. |
| `g.assets.url(path)`, `g.assets.picture(path)` | For a script that puts a painted picture on the live layer: its stamped address, and a promise that it has arrived |
| `g.actor("scribe").face("W")`, `g.lead.look(x, y)` | Turns someone to a compass point, or toward a place |
| `g.plane("trunk")` | One of the scene's cut-outs, or `null`: `.show(true)`, `.set("open")`, `.fade(0.5)`, `.place(x, y, scale)` |
| `g.actor("scribe")`, `g.lead`, `g.q("#door")` | Reach people, and the parts of the live layer |
| `g.team(["mom", "bigsis", "lilsis"])` | Says which leads the player can switch between from now on |
| `await g.switchLead("son")` | Changes who the player controls (they must be on the team) |
| `g.closeup(drawing, label)`, `g.closeup()` | Shows a close look at something, and puts it away |
| `await g.tap()` | Waits for a click or a key |
| `g.startTunnel(dates)`, `g.stopTunnel()`, `await g.wormhole()` | The time tunnel, and the short trip between two eras |

For cutscenes, which dress the stage themselves:

| Call | Does |
| --- | --- |
| `g.view.clear()`, `g.view.setEra("present")` | Empties the stage; sets the era |
| `await g.view.draw("", words, { picture, live, grid: [800, 600] })` | Puts up a painted backdrop and its light. `words` describes the picture for someone who cannot see it. |
| `g.view.cast.addPicture(id, { src }, x, y, scale)` | A painted sprite to move about: `{ src }` or `{ frames, fps }`, with `foot: [x, y]`, the point of the picture that is put at (x, y). It has `.place(x, y, scale)`, `.fade(opacity)` and `.flag("still", true)`. Shown smaller than it was painted, it is drawn smoothly. |
| `await g.view.cast.load()` | Waits until every picture on the stage has arrived. Do this before fading in. |

---

## 11. The tools

| Tool | What it is for |
| --- | --- |
| `python3 tools/serve.py` | Runs the game on your computer at `http://localhost:8000` (`8080` for another port, `--lan` to let a phone on your network open it). It tells the browser to keep no copies, and stamps the pages again whenever a file has changed. |
| `python3 tools/stamp.py` | Gives every code file, style file and picture an address that changes when the file does ("Publishing a new version" in section 10). `--check` changes nothing and says whether a page is out of date. |
| `tools/hooks/pre-commit` | Runs `stamp.py` at every commit, once turned on (two commands, at the top of the file) |
| `tools/storyboard.html` | The story from the game's own files: acts, chains and beats; the title and every scene as the game builds it, with clickable areas, walkable ground, blocked patches and the base line of each cut-out; the era palettes; the script by character, with a button that exports it as a spreadsheet. It says so at the top if the story has a beat that cannot be reached. |
| `tools/sprites.html` | Everyone in the game, from the settings in `people.js`: every direction, the walk, every gesture, reaching and sitting, at the sizes they appear in a scene, against a choice of grounds |
| `tools/paint/` | The scripts that paint the pictures, one for each scene, with their shared library and the painter's guide. `python3 install.py <scene>` copies a painted scene into `art/`. |
| `tools/koine-road/` | The scripts that build the typeface from pen strokes (it has a README of its own) |

Useful addresses while building:

- `index.html?scene=egypt-site&lead=dad&flags=egypt.sawSite` jumps straight to a scene.
- `index.html?scene=engine-proof` is the worked example of a painted scene.
- `index.html?intro` plays the intro again.

In the browser's console, `game` is the game object that scripts are handed as `g`.

**The engine's test** drives a real browser through the engine and fails on any console
error: the painted stage and its layers, depth read off the screen pixel by pixel,
walking and routes, every form of cut-out, live light, close-ups, the inventory, old
saves, every scene in the list, how the cast layer repaints, how people are sized,
seated people talking, words over heads, the fetching of every picture behind the title
(and that nothing is asked of the server afterwards), hard and smooth pixels, the
interface at two sizes and in three other window shapes, the storyboard page, the intro
and the stamping tools: 192 checks, in about three minutes. It takes screenshots, which
have to be looked at: a picture that is wrong throws no error. Three more scripts
measure what a frame costs (the table in section 1), take the pictures that the choice
between hard and smooth pixels was made from, and take pictures of seated people
talking and of words over heads in the real scenes. These scripts are not in the repository yet: they were written
beside the game, and their paths have to be changed before they can be run from here.

---

## 12. What is built and what is not

**Built, and meant to stay:** the engine, the 800x600 painted stage with its cut-outs
and live light, the depth system, the save format, the sound system, the line-ID
dialogue system, the story-as-data structure, the pixel renderer and the figure, the
interface, the Koine Road typeface, the stamping of files.

**Painted:** the highway of the intro and the title, and thirteen scenes: four in Egypt,
three in Rome, the five rooms of the house and the Nevada roadside. Twenty-four things to
carry.

**Drawn:** twenty-four people.

**Written:** a prologue and four acts. Act One (Egypt) and Act Two (Rome) have puzzle
documents; the two acts in the present are a first draft, as their puzzle document says.
None of it has been signed off by the author yet: Acts One and Two were rewritten in
October 2026 from his brief, and are waiting to be played.

**Placeholder:** the music, which is synthesized. There are no recorded voices yet.

**Not built yet:**

- Light on people that changes with the scene. Every person is lit from the upper left
  in their own colors, by lamplight and at noon alike, whatever the light in the painting.
- More acting. There is no turning between directions (he snaps round), no running,
  climbing or carrying, no sitting down or getting up as an action, and faces cannot yet
  show a feeling.
- Other people walking about by themselves. Anyone can be walked by a script, and the
  patch of ground they block follows them when the script ends; nobody wanders unasked.
- Companions who follow the lead about a scene. In a party the others come along from one
  scene to the next, but inside a scene they stay where they were left.
- Close-ups the player can click inside. A close-up is a picture to read, not a
  small scene of its own.
- Scrolling scenes wider than the screen.
- Touch polish: larger targets and a bigger inventory on phones.
- Layered music, ambient sound loops, per-scene reverb.
- Translations (the line files are ready for them) and a caption option for sounds.
- Saving in the middle of a conversation. Esc pauses at any time, but Save and Load
  wait until the current moment has played out.
- Painted close-ups. The computer screen and the notice are still the kit's drawings.

**How the engine was tested.** By the test described in section 11, in Chromium, at
800x600 and 1440x1080 and in three window shapes that are not 4:3. Depth was tested by
reading pixels off the screen: with the lead's feet above a cut-out's base the cut-out's
pixels cover his, and below it his cover the cut-out's, at each trunk of a row of palms
and at both ends of a car that stands on a slant; his route to the far side of the car
goes round it, and every place he is seen on the way is ground he may stand on; clicks
in the river and at the water's edge end on the bank. A cast layer repainted in patches
was compared with one painted whole on every frame of a walk in three scenes, and never
differed by a pixel. Saves from both older versions were loaded. Seated people were
watched talking, and the words over six heads were measured: ten pixels above each,
seated or standing, small or full size. And with the title up and the pictures gathered,
the server was made to refuse every picture: the game was continued, and a scene never
yet shown was entered, with every painting, cut-out and inventory picture in place.

**How the acts were tested.** Each act has two checks of its own. One is a script that
plays the act in the real game by real mouse clicks on the real clickable areas (walk,
look, use, a carried thing on a target, a choice of what to say, the Hint button),
more than one way round where the puzzles allow it, and fails on any error in the
browser's console: Egypt in 349 clicks (the three reflectors in two orders), Rome in 268
(its three chains in two orders), the living room in 191 (each of the three trying every
job), Nevada in 209 (a different one of them flashing the coin each time), and the
opening movie and the title watched at two sizes. The other reads the act's files
against one another and against the painters' measurements: every line a scene uses
exists and every line written is used, every beat's fact is set by some script, every
thing given is in the list of things, every place someone is sent to stand can be walked
to, and every number that differs from the painter's `layout.json` is a difference
somebody meant, with its reason. Like the engine's test, these scripts were written
beside the game and are not in the repository yet.

It has not yet been played by a person on a real phone, or in Firefox or Safari. Two
things deserve a look there. Hard pixels at two times and over rely on the browser's
`image-rendering: pixelated`. And the sketch of an unpainted scene is made by handing the
browser a drawing and asking for pixels back; if a browser refuses, the game falls back
to showing the drawing itself.

---

## 13. Controls

| Do this | With a mouse | On a touch screen | On a keyboard |
| --- | --- | --- | --- |
| Walk | Click the ground | Tap the ground | |
| Hurry a walk | Double-click | Double-tap | |
| Use, talk, pick up | Click the thing | Tap the thing | Tab to it, Enter |
| Look | Right-click, or **Look** then click | Press and hold, or **Look** then tap | Tab to it, L |
| Use a carried thing | Click it, then click the target | Tap it, then tap the target | |
| Play as someone else | Click their portrait | Tap their portrait | 1, 2, 3 |
| Talk to a companion | Click them | Tap them | Tab to them, Enter |
| Give a companion something | Click the thing, then click them or their portrait | Tap the thing, then tap them or their portrait | |
| Next line | Click | Tap | Space or Enter |
| Pick a reply | Click it | Tap it | Number keys |
| Skip a cutscene | **Skip** | **Skip** | Esc |
| Menu | **Menu** | **Menu** | Esc |
| Show what can be clicked | **Show** | **Show** | Hold H |
| Move past a title card | Click | Tap | Space or Enter |

---

## 14. Decisions waiting for you

The game makes choices so that it runs. These are yours to keep or change:

1. **How the pictures are scaled.** Smoothly when a picture pixel covers less than two
   screen pixels, with hard pixels from two up (section 2). Hard pixels at every size,
   or none, is one number: `CRISP_FROM` in `js/engine/scene.js`.
2. **How people are sized while they walk.** From a ladder of sizes, stretched to fit,
   and at their exact size when they stop (section 1). It is what keeps a slow machine
   smooth; a sharp eye may see a walker's outline thicken or thin by a pixel as he goes.
3. **How strong the perspective is,** scene by scene. It is the painter's `horizon` and
   `full`, and the scene's `minScale`.
4. **In-engine cutscenes** instead of video.
5. **Five leads:** free switching, alternating chapters, or a mix. At present the story
   decides when to cut from one half of the family to the other, and Mom and the girls
   can be switched between at any time.
6. **Passing things between eras through wormholes** as a core puzzle idea.
7. **Verbs:** one main action plus Look. Classic games had a verb list; a third
   verb such as Talk could be added.
8. **Hints:** a Hint button that has the lead think aloud. Keep it, limit it, or
   drop it.
9. **Voices:** from the start or later. The engine handles either.
10. **Who the leads are.** [CHARACTERS.md](CHARACTERS.md) describes all five. Nobody has
    a name yet: on screen they are Dad, Son, Mom, Big Sister and Little Sister.
11. **Where the present-day chapter goes.** It plays after Rome. It could open the game
    instead, or be cut in between the scenes in the past.
12. **The puzzles.** The three puzzle documents lay them out so they are easy to change.
13. **Big Sister's facts.** Every fact she states has to be true. The list, and which
    of them have been checked against a source, is at the end of CHARACTERS.md.

---

## Sources

- web.dev, [Why are some animations slow?](https://web.dev/articles/animations-overview):
  `transform` and `opacity` can be animated without layout or paint.
- MDN, [Animation (Web Animations API)](https://developer.mozilla.org/en-US/docs/Web/API/Animation):
  script control of animations: pause, finish, `currentTime`, `playbackRate`.
- MDN, [image-rendering](https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering):
  how a browser scales a picture: smoothly, or with hard pixels.
- Chrome for Developers, [Web Audio, Autoplay Policy and Games](https://developer.chrome.com/blog/web-audio-autoplay):
  an audio context starts suspended until the player interacts.
- MDN, [Web Audio API best practices](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices):
  stream long tracks from a media element, start audio from a user gesture, schedule
  changes on the audio clock.
- web.dev, [How to save a file](https://web.dev/patterns/files/save-a-file):
  the Save dialog in Chrome and Edge, and the download-link fallback elsewhere.
- King's Quest Omnipedia, [KQ6 development](https://kingsquest.fandom.com/wiki/KQ6_development):
  the game's character actions were made by capturing live actors on video, then
  touching up each frame on the computer to fit the hand-painted backgrounds.
