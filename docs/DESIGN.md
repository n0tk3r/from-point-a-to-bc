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
| Light | Beams and glows are drawn by code, never painted; a door in time is the painting itself, bending | Light has to move, grow and stay smooth. A door in time is a ripple in the paint, as if a stone had been dropped in the picture: the author's choice, round ten (section 2, "The door in time"). |
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

Size today: 57 code and style files, about 1 MB (about 350 KB when the server compresses
it); 106 pictures, 4.7 MB in all; and a 49 KB font. Nothing else is downloaded.

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
  life.js                 the scene's people living their own lives: small movements, and a walk now and then
  edges.js                ways out at the edges of the picture: the bands, what the label says, a check of every scene's
  outline.js              Show: an outline round each thing that can be clicked
  fx.js                   canvas effects (the time tunnel)
  effects.js              things that move by nature: smoke, flames and embers, water, birds, cloth that stirs
  story.js                reads the story data: open beats, checks
  ui.js                   heads-up display and menus
  game.js                 ties it together; the `g` that scripts use
js/art/                 everything that is drawn by code
  kit.js                  the neon rings (the tab icon, the title, the tunnel), the sketch of an unpainted scene, close-ups, and the old 320x200 drawings
  pix.js                  the pixel renderer: solid shapes in, pixel art out
  rig.js                  the jointed figure: poses, eight directions, the walk, stances, gestures, sitting
  people.js               the cast as the rig sees them: proportions, clothes, colors, and how each one stands, walks and talks
  props.js                things drawn by code that stand on the ground (kept for scenes that are not painted yet)
  look.js                 the paints: the people and the moving things in the key of the scene on stage (section 9)
  look-data.js            the paint box, the six keys and which scene uses which (written by tools/paint/postimp_key.py)
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
- **Light is drawn live, and CSS animates it.** The glow a door in time throws on a
  road, a beam of sunlight, the spot of sun off a coin. These are smooth drawings on a
  layer of their own, and they only ever animate `transform` and `opacity`, the two
  properties browsers can animate without redrawing the picture. (The door itself is
  not light: it is the paint, bending, drawn among the moving things: section 2.)
- **A second canvas is used for one effect:** the time tunnel (`js/engine/fx.js`),
  where rings, streaks and flying dates all change every frame.
- **No WebGL and no game framework.** If a later scene needs a storm of particles,
  that scene can add a canvas effect the same way the tunnel does.

Players who ask their system for less motion (`prefers-reduced-motion`), or tick
**Less motion and no flashes** in Options, get still decoration, people who stand
quite still, cut-outs that hold their first picture, plain fades in place of white
flashes, a slow tunnel, and smoke, flames, water and birds that move gently, at half
speed or less (no bird flaps up: they walk off instead).

### Keeping it fast

- **Scenes are small, separate files.** Each scene is its own file of a few KB. All
  of them are fetched while the start-up panel is showing, so that a game in progress
  never asks the server for code and can never be handed a scene from a newer version
  than the one it is running. When there are hundreds of scenes, fetch them an act at a
  time: `Game.start` in `js/engine/game.js` is the place.
- **A scene's pictures are here before it is shown.** Entering a scene fetches its
  backdrop and every picture its cut-outs can show, and only then fades in, so nothing
  pops in late. The pictures of the scenes that can be walked to from it (`exits`, and
  wherever its ways out at the edges lead) are made ready ahead of time.
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
  clickable areas: each gets an outline.
- **The things that move by nature take turns.** Each changes its picture only as often
  as its motion needs (a bird thirty times a second, smoke twenty, a flame fifteen, a
  swaying cut-out six, light on water five), and in any one frame only four of them may
  change: the cast then repaints a few small patches and never the whole layer (section 2,
  "Things that move by nature").
- **Show costs nothing until it is asked for.** Its outlines are worked out once, when it
  is turned on (some 30 to 50 ms in the busiest scenes on the test machine), and again only
  if what it shows changes while it is on. While it is off its layer is hidden and nothing
  is drawn.

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
| Live | Light: the glow a door throws, beams, the spot of sun off a coin, anything that must stay smooth or move by itself | Smooth drawings in picture pixels, animated by CSS or by a script |
| Cast | People, painted cut-outs and props, the things that move by nature (smoke, flames, water, birds), and the doors in time | Pixels, sorted by depth and repainted where something has changed |
| Tunnel | The time tunnel | A canvas effect, only during travel |
| Outlines | Show: an outline round each thing that can be clicked, and an arrow at each way out at an edge | A canvas, drawn once when Show is turned on, hidden while it is off (section 10, "What Show shows") |
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

The painting, the people, a painted part that a cutscene puts on the live layer, the
tunnel and the outlines of Show always get the same treatment, so they always match one
another. The rule is one class on the stage, set by the scene view when the stage
changes size (`CRISP_FROM` in `js/engine/scene.js`, and "crisp" in `css/game.css`).

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

**Nothing that moves by nature is painted still.** Smoke, a flame, running water, rings
on a pool, birds, washing in the wind: the painter leaves it out of the picture and marks
where it goes, and the engine draws it moving (below, "Things that move by nature").

**A scene with no painting yet is sketched.** Leave `picture` out of a scene file and
the engine draws sky, ground and a labelled box for each clickable thing, in the era's
colors. A scene whose painting will not load is sketched too, with a warning in the
console, and can still be played.

### Things that move by nature

The author, after playing Rome: "any statically drawn thing that naturally moves can break the illusion of the reality
we're trying to create." So nothing that moves by itself in the world is painted still: smoke, fire, running water,
rings on water, light on water, birds, washing and banners in the wind. The painter leaves such a thing out of the
picture (or takes it out, leaving what was behind it and every other pixel as it was) and marks where it goes, in the
scene's `layout.json` under `"fx"`. The scene lists the same marks under `fx`, and `js/engine/effects.js` draws them,
moving, on the cast layer among the people:

```js
fx: [
  { id: "altar-smoke", type: "smoke", at: [286, 429], base: [[244, 518], [338, 509]], height: 196, width: [2, 15], lean: [-30, -196], opacity: 0.45 },
  { id: "pigeons", type: "birds", count: 5, area: [[430, 466], [796, 438], [796, 586], [258, 586]],
    frames: { foot: [23, 40], sizeAt: 590, stand: ["pigeon-1.png", "pigeon-3.png"], peck: ["pigeon-4.png", "pigeon-5.png"],
      walk: ["pigeon-6.png", "pigeon-7.png", "pigeon-8.png", "pigeon-9.png"], fly: ["pigeon-13.png", "pigeon-14.png", "pigeon-15.png"] } },
  { id: "laundry-1", type: "sway", plane: "laundry-1", anchor: "top", amount: 1 },
],
```

The marks go into the scene file as they are: the field names are the same in both places, and a mark's notes
(`what`, `note`) and words where a number goes ("wind": "from the left") are simply passed over. The kinds:

| Kind | What it draws | Its own fields, with their defaults |
| --- | --- | --- |
| `smoke` | Soft puffs that rise from a point, rise straight for a little, then bend away with the air, waver, widen and fade. Gusts give the column soft bends. | `at` (where it leaves the fire); `height` (110 px); `width` (at the top, or `[at the start, at the top]`: `[top × 0.18, 36]`); `lean` (where the top ends up, `[dx, dy]`, or dx) or `wind` (6 px a second sideways); `rise` (height / 6 px a second); `rate` (3 puffs a second); `gust` (0.35); `color` (`#d9d5cd`); `opacity` (0.32) |
| `flame` | A tongue of flame with a white heart and a soft glow round it, flickering: ducking, stretching, its tip wandering | `at` (the foot of the flame, at the wick); `size` (12 px tall); `width` (size × 0.42); `color`, `edge`, `core` (its middle, outside and heart); `glow` (size × 2.2 px; 0: none), `glowColor`, `glowOpacity` (0.22); `flicker` (0.5, from 0 to 1); `lean`; `lull` (0; up to 1: it dies down to nothing now and then, as charcoal's tongues do) |
| `embers` | A bed of coals that glow and fade each in its own time, a soft light over the bed that swells (over a big bed, in one part and then another), and now and then a spark | `at` and `size` (`[half its width, half its depth]`: `[10, 3.5]`), or `bed` (its shape); `count` (from the size); `color`, `cool`; `glow`, `glowColor`, `glowOpacity` (0.2); `breath` (2.4 s); `sparks` (0.25 a second); `blobs` |
| `ripples` | Rings that spread and fade on still water, with a light edge and a darker trough just inside it | `at`; `radius` (where a ring has gone, or `[where it starts, where it has gone]`: `[1, 16]`); `flat` (0.32, its height over its width); `every` (a number of seconds: steadily; `[low, high]`: now and then; `[1.5, 4]`); `rings` (2 from each drop); `speed` (13 px a second); `color`, `trough`; `opacity` (0.6) |
| `stream` | Water running along a path, light running down it, and a splash where it lands: foam, rings and drops | `path` (from the spout's mouth to where it lands, smoothed); `width` (3, or `[at the mouth, at the end]`); `color`, `light`; `opacity` (0.55); `speed` (55 px a second); `splash` (5 px; 0: none) |
| `shimmer` | A few glints of light that come, drift and go on a water surface, kept inside its shape: very quiet | `poly` (or `area`, or `rect`); `holes` (shapes kept clear: a boat, reeds); `count` (the water's area / 1100); `size` (6 px at the near edge, shorter farther off); `flow` (`[4, 0]` px a second); `life` (1.8 s); `color`; `opacity` (0.45) |
| `birds`, flyers | Small birds crossing the sky now and then along `lanes`, or wheeling round a `circle` (kites): beating their wings in bursts and gliding between, banking at the ends of a circle | `lanes` (lines across the sky, beginning and ending off the picture) or `circle` (`{ at, r: [rx, ry] }`); `every` (`[6, 14]` s between crossings); `group` (`[1, 3]` birds); `count` (2, wheeling); `speed` (70 crossing, 14 wheeling); `size` (7 px across, drawn); `scale` (or `[low, high]`: each bird its own size); `frames` (`glide`, `flap`, `bank`, `middle`, `mirror`); without frames, small dark silhouettes drawn by the engine |
| `birds`, a flock | Birds on the ground (`area`) or along a ledge (`perch`) that stand, look about, peck, walk a few steps and turn; go up when somebody comes near and land again a little way off, the ones beside them going too; with nowhere clear to land, fly off and come back later | `area` (or `poly`, `rect`) or `perch`; `count` (5); `frames` (below), or birds drawn by the engine: `look` (`pigeon`, `dove`, `sparrow`) and `size` (26 px long where a person is 160 tall); `depth` (smaller farther off: on an area); `moves` (`{ stand: 2, look: 2, peck: 4, walk: 3, turn: 1, away: 0 }`; `away`: one flies off by itself and comes back); `shy` (150 px at full size, about a metre and a half; half that from someone standing still; 0: never startled); `fly`, `turn` (false: never); `back` (`[8, 20]` s away); `treads` (`[y, ...]`) or `tread` (px): birds on steps keep to the treads and hop from one to the next; `walk` (12), `flight` (95) |
| `sway` | A cut-out of the scene (washing on a line, a banner, a palm's crown) stirring in the air from a fixed edge, with a ripple running along it | `plane` (the cut-out's id); `anchor` (`"top"`: it hangs; `"bottom"`: it is rooted; `"left"`, `"right"`: it flies from a pole at that side; or a line); `at` (the foot row, the pin row or the pole's column); `amount` (2.5 px at the far edge); `period` (3.4 s); `wave`; `lean` (0.3 of the amount, with the wind) |
| `portal` | The door in time: a ripple in the paint. See "The door in time", below | `at` (its middle, wide open); `r` (half its height, wide open); `wide` (1: a round hole; the chamber's doorway 0.48); `keep` (the bare wall it is in, `[x0, x1]`); `rise`; `under`; `light`; `open` (0); `strength` (0.45); `bend` (0.6); `rate` (1.5); `size` (1.11); `pale` |

Every kind also takes: `id` (its name, for scripts and tests; on the stage it is `fx:<id>`); `base` or `plane`, its
depth among the people exactly as for a cut-out (section 3: a row, a line, `"front"`, `"back"`); `when` (on the stage
only while the story says so, read again whenever the story changes); `scale` (every size and speed of it, times this);
`opacity`, `color`; `clip` (a shape it is kept inside: rings that must not run onto the sand); `behind` (shapes where it
passes behind something painted nearer, and is not drawn, or only at `behindOpacity`: smoke rising behind a pyramid);
`seed`. A smoke, a flame, embers or a stream sits by default at the row of its own point, so give the `base` of the thing
it belongs to (an altar's smoke has the altar's base: a man behind the altar is behind its smoke); water on the ground
and birds in the sky lie behind everybody; birds on the ground sort by their own feet, each one, like people. A sway is
its cut-out: the cut-out keeps its depth, its states and everything a script does to it.

**Painted frames for birds.** One picture a frame, clear background, every frame of a bird on the same size of canvas
with its feet at the same point: `frames: { foot: [x, y], face: "E", sizeAt: 590, stand: [...], look: [...], peck:
[...], walk: [...], turn: [...], takeoff: [...], fly: [...], glide: [...], land: [...], shadow: "..." }`. Only `stand`
is needed; a missing list falls back sensibly (no `walk`: the bird hops; no `fly`: it never flies). The engine turns
the frames round for a bird facing the other way (not the `shadow`, which lies under a bird on the ground and goes when
it takes off: the sun does not move). `sizeAt` is the row at which they are the right size: they grow and shrink from
there with the depth, as people do (`scale: "depth"` means the row `full`); without it they are drawn as painted, times
`scale`. File names are in the scene's own folder unless `dir` says otherwise; with `set: "pigeon-dark"`, a number `n`
stands for `pigeon-dark-n.png`. The frames are fetched with the scene's other pictures (ahead of time, and in the
quiet fetching behind the title), and a scene does not show until they are here.

**On the game clock.** Each moving thing keeps its own time, which goes on with the game clock: at its speed, and not
at all while the game is paused. What it shows at a moment is worked out from its seed and that time alone (the puffs
of a smoke, the glints on water, when the birds cross), so a scene opened twice looks the same at the same moment of its
time. The only exception is a flock that somebody has startled, since what it does then depends on where people walked.
For less motion, each one's time runs at half speed or less, it changes its picture less often, flames flicker less,
flyers glide, and a flock never flies: a startled bird walks off instead.

**Cheap.** Each kind changes its picture only as often as its motion needs: a bird thirty times a second, smoke, rings
and a stream twenty, a flame fifteen, embers ten, a sway six, light on water five. In any one frame only four of them
may change (`game.effects.budget`): the ones that have waited longest go first, and a bird on the move before them all,
so the others wait a frame or two, which nobody sees. The cast then repaints a few small patches, never the whole layer
(it does that when more than six things change at once: `Cast.update`). Each picture is cut to the box the thing can
reach; a group of birds crossing together is one picture. A swaying cut-out is repainted whole each time it moves, so
keep sways to the things that need them. The engine's own scene, with twelve moving things (two of them big sways) and
some 120 puffs, glints, coals and birds on the stage, has the cast layer repaint about 3 million pixels a second, all in
patches (with none of them, 0.2 million). Measured as in section 1 ("What a frame costs"), with the processor slowed four
times over: a frame's main-thread work while the lead walks across it goes from 3.5 to 6.2 ms, and while he stands from
0.8 to 6.0 ms, every frame still on time. A scene with a few moving things costs a fraction of that.

**Never clickable, never outlined.** They are on the cast layer, which takes no clicks: a click on smoke is a click on
whatever is under it, the floor or a clickable area. None of them is a clickable area, and their ids on the stage begin
`fx:`, which no area names, so Show never outlines them. A scene that wants the player to click the pigeons gives them
an area of its own, and its script can startle them: `g.effects.get("pigeons").scare([x, y])`.

**Trying marks out.** In the game, in the browser's console, a painter can put every mark of the scene on the stage
before any scene file has them:
`(await (await fetch("art/scenes/" + game.scene.id + "/layout.json")).json()).fx.forEach((m) => game.effects.add(m))`.
A mark the engine cannot use says so in the console, by its id. `game.effects.hold(true)` stops their time,
`game.effects.seek(5000)` shows them five seconds in, `game.effects.stats()` counts what is moving, and `?nofx` in the
page address (or `game.effects.enabled = false`) takes them all away. The engine's own scene shows every kind:
`index.html?scene=engine-proof&lead=dad&flags=proof.fx`.

### The door in time

The author, 9 October: "Rather than a solid object or rays let's see if we can make it look like a ripple or distortion
of the paint. The time portal really needs to look good." A design study showed six such looks live on the real
backdrops (pond rings, a slow vortex, wet paint flowing, a glass lens, heat haze, the paint thinning to light), and he
chose **pond rings**, with the settings that are now the kind's defaults. So since round ten a door in time is not a
drawn thing laid over the painting (the neon rings stay the game's mark: in the browser tab icon, on the gate you
click to begin, and rushing past in the time tunnel; `kit.portal` still draws them, and no scene uses it now): it
is the painting itself, bending. The `portal` kind reads the paint in the box
the door can reach, once the scene is up (the backdrop; any cut-out that lies under the door, named in `under`; and,
with `light: true`, the light the scene draws over the wall, so that the sunbeam that opens the chamber door is bent
with the wall and not hidden by it), and writes it back displaced thirty times a second: rings travel out from the
door's middle and the paint bends along each one, a crest catching the lamplight a shade lighter and a trough a shade
darker, as wet paint does; the rings fade with distance, their strength and phase wander round the circle and across
the wall from seeded tables (so it is paint, not geometry), and the heart holds a soft light of the paint's own colour
(`pale`, never keyed). A coin-sized door gets a brighter heart and a wet rim, so it shows on a dark floor and on bright
sand alike; a coin door is also given more `strength` (0.8) than the walk-in door, or it would not be seen. Where the
rings do not reach nothing is drawn, so the door sits in the picture at its depth (`base`): whoever walks up to it is
drawn over it. `keep` fences the bend into the bare wall the chamber door stands in, so the king's furniture beside it
stays straight.

A door opens and shuts by `open`, 0 to 1: `g.effects.get("door").open(k)`, tweened by the scene's script (1.6 s in
the chamber; 0.9 s for a coin door). As it opens the radius grows fast and the bending follows, so a small disturbance
shows at once; shut is the same backwards, and at 0 nothing is drawn. The options a moment may need ride with it and
hold until given again: `{ wide }` (the chamber door opens round and is squeezed to a doorway as it grows), `{ at,
scale }` (the flashlight opens a plate-sized round hole off to one side: `at` an offset from the door's middle, `scale`
0.11 of its size), `{ flicker }` (with the batteries). The coin's wink in Rome is `scale` over 600 ms. `refresh()`
reads the paint again when the light over it has changed (the beam has come on). On the highway `rise: true` lets
the hole's middle rise out of the sun's disc as it opens, and `under: [{ src: "...sun.png" }]` reads the sun into the
paint it bends; the sun stays where it is, part of the picture the hole is in.

What it costs: the chamber door is about 30,000 pixels a picture (one read of the paint, blended from four pixels,
per pixel), 1.5 to 3 ms here and perhaps three times that on a slow laptop, thirty times a second while it is open;
the coin doors are under 0.2 ms; making a door (its tables) is about 30 ms, once, as the scene is built. For less
motion the clock runs at half speed, the bend is 0.6 as big, and it is drawn fifteen times a second: never stopped
dead, as the author asked. The study, with the six looks and the author's settings, is kept as a private page
(`claude.ai/artifact/WCRWEAbF2DfeouYApqQewm`).

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

Then the paints: a scene's pictures are mixed from the game's one box of paints in its key, on their way into
`art/` (section 9, "The paints"). The inventory pictures belong to the interface and are not.

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
  do not: she can walk past them), and someone away on a walk of their own has their
  place kept for them (section 4, "Their own lives").

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
| Praying | The head bowed, the eyes shut, the hands folded in front, eased into over about a quarter of a second and held, through whatever is said, until a script lets it go. Each of the family prays in their own way (`pray`, below). Someone sitting prays sitting down: Lot, on the sand by the river, lifts his open hands in front of him, palms up, his head bowed. |
| Shading the eyes | A flinch back, the head turned a little away, the eyes screwed shut and a hand laid flat over the brow, up in about a seventh of a second and held until a script lets it go (`shade`). Anyone standing can do it: Dad does it when the car's door mirror throws the sun in his eyes. |
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

Twenty-four people in the story, all in `js/art/people.js` (which also keeps `carrier`, the water carrier of the
first drafts, whose place by the river Lot has taken):

| Where | Who |
| --- | --- |
| The family | `dad`, `son`, `mom`, `bigsis`, `lilsis` |
| Egypt | `lot` (Abram's nephew: sits cross-legged on the sand and prays), `scribe` (sits cross-legged on the ground), `overseer` (a staff in his right hand), `hauler1`, `hauler2`, `hauler3`, `mason1`, `mason2` (far up the pyramid's faces on the painter's hanging planks, drawn small, rubbing the stone now and then), `guard` (the tallest, a long staff upright), `lampboy` (sits on a bench; can stand and walk), `goldsmith` (sits on his stool) |
| Rome | `keeper`, `washer`, `urchin` (sits on the kerb), `soothsayer` (sits on a step, with a staff), `senator`, `doorkeeper`, `clerk` (sits at his table), `dateseller` (a basket of dates on his hip) |
| Nevada | `oldtimer` (in a lawn chair that is drawn with him), `agent` |

Three more figures are the same men in another state: `goldsmith-shades` (the goldsmith
with the sunglasses on), `guard-shade` (the guard holding the windshield shade up, his
staff laid on the sand) and `lot-standing` (Lot on his feet, his staff in his hand). A
scene swaps one for the other in place, under the same id, so the man keeps his name and
the color of his words.

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
| `pray` | How they stand to pray: how high the folded hands are, how far the head bows, and whether the hands are clasped tight and the eyes squeezed shut | Dad folds his big hands low in front of him, his head well down. The Son folds his hands at his middle and bows his head; his hair stays up. Mom folds her hands at her breast, and her handbag slides down to the crook of her elbow. Big Sister prays exactly as she was taught, hands together at her breast. Little Sister prays with all her might: hands clasped tight under her chin, eyes squeezed shut. |
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
- **A person's place goes with them.** On their mark they block their `solid` (or a small
  patch at their feet); walked somewhere else by a script, a patch at their feet there.
  `solid: false` lets the lead walk through them. (On a walk of their own, below, their
  place is kept for them.)

[CHARACTERS.md](CHARACTERS.md) is where these choices come from.

### Their own lives

Nobody in a painted scene should stand like a statue: in a picture that is otherwise alive, a person who never moves
breaks the illusion as surely as painted smoke does. So everyone in a scene who is not one of the family (the scene's
`actors`) lives a little by themselves while the player is busy elsewhere (`js/engine/life.js`):

- **Small movements**, every few seconds, where they are: shifting their weight, looking about, a hand to the back of
  the neck, a stretch, and the movements that are theirs alone. The rig draws them (`figure.fidgets` lists a person's
  own, `figure.fidget(name)` plays one); the engine chooses when, and which, never the same one twice running.
- **A bigger moment** now and then, for a person whose scene says where they may go: whoever sits stands up, walks a
  few steps to one of their places, stretches or looks at something there for a few seconds, walks back and sits down
  again; whoever stands strolls a little way off and comes back.

A scene says how each person lives, in their entry under `actors`:

```js
actors: [
  { id: "scribe", kind: "scribe", at: [150, 448], face: "E",
    life: {
      fidget: true,                      // small movements in place (the default, for everyone)
      every: [18, 40],                   // seconds between bigger moments, picked at random in the range
      spots: [[178, 462, "E"], [120, 470, "S"]],     // where they may go (where their feet go), and which way they face there
      stay: [3, 8],                      // seconds they stay there, doing a small movement or two
      stand: true,                       // someone seated stands up first, and sits down again on coming back
      when: (g) => !g.flag("egypt.writing"),         // only while the story allows
      still: false,                      // true: small movements only; never leaves the mark (a guard at a door)
    } },
],
```

| Setting | Default | Meaning |
| --- | --- | --- |
| no `life` at all | | Small movements now and then, every 7 to 15 seconds; never leaves the mark |
| `fidget` | `true`: every 4 to 10 seconds | `false`: none at all; `[4, 9]`: every 4 to 9 seconds |
| `every` | `[18, 40]` | Seconds between bigger moments. The first comes about a third of the way into it. |
| `spots` | none | Where they may go: `[x, y, facing]`, the facing optional. A spot is on the floor (the scene's `walk`), clear of blocked ground, and the way there goes round things by the walk map at an easy stroll. Someone whose own mark is off the floor the family walks on (a keeper behind his counter, a clerk behind his table) walks in a straight line between the mark and the spot, so give them spots on their own ground. A few steps reads best: 40 to 120 pixels from the mark. With no spots, they never leave the mark. |
| `stay` | `[3, 8]` | Seconds they stay at the spot |
| `stand` | `true` | `false`: someone seated never gets up |
| `when` | always | A test of the story: nothing happens while it is false |
| `still` | `false` | `true`: small movements only |

What the engine sees to, so that a scene never has to:

- **The game clock.** All of it stops with the menu. Nothing starts while a script has control, while anyone is
  talking or a choice is on the screen, in a cutscene, during a close look at something, or while Show is on; whoever
  is walking when one of those begins stands still until it is over.
- **One at a time.** Only one person in a scene is away at a time, and the next waits a few seconds after the last is
  home. Nobody goes anywhere in the first 6 to 10 seconds after a scene opens.
- **The story first.** A person whose own `when` or whose `life.when` is false is left alone, and so is anyone who is
  talking, praying, holding something out or being walked by a script. Only someone who is on their mark goes
  anywhere: a person a script has left somewhere else stays there.
- **The family is kept clear.** A spot is picked only if the way there and back passes 60 pixels or more from every
  member of the family on the stage. Whoever is away turns for home if one of the family comes within 60 pixels of
  the way they still have to go, and on their walks they go round the family, never through.
- **Nobody is talked to away from home.** Whatever starts a script (a click on someone, a carried thing used on them or
  given to them, a look) first sends everyone who is away, or up from their seat, home at a brisk walk, to sit down
  again, while the lead walks over to the place the scene gives for the conversation. The script starts when both are
  there, and never waits more than about two seconds: after that they are simply put on their marks. So every script
  can go on assuming that everyone is on their mark, as it always has. A script can ask for it too:
  `await g.settle()` brings everyone home, `await g.settle("scribe")` one person. (A hint, or a look at a thing in the
  pockets, only has the lead speak: nobody is sent home for that, and anyone walking simply waits.)
- **Their clickable area goes with them.** The area with the person's id, or one that says `actor: "<id>"`, follows
  them while they are away (or up from their seat): a box round the figure as it is drawn at that moment, which Show
  outlines by the figure itself. Back on the mark, the scene's own shape applies again.
- **The ground.** While someone is away their place is kept for them, so the lead cannot stand in it, and where they
  stand still is blocked. While they walk, they block nothing.
- **Saves.** Nothing of it is saved. A game loaded, or a scene entered, has everyone on their mark.
- **Less motion.** With that option on, the small movements stay and the walks stop.
- **Tests.** `index.html?still` (or `game.life.enabled = false`) turns all of it off, and the act tests open the game
  that way, since they click on people where the scene puts them. `game.life.where()` says who is where and what they
  are doing, `game.life.force("scribe")` starts someone's bigger moment at once, and `await game.life.idle()` waits
  until everyone is home. The engine's own test (part `life`) watches the two people of the proof scene, who are there
  with the fact `proof.life`.

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
  `road.bend(k)` runs the hole's rings over the sign and `road.bc(k)` changes what it says
  (POINT B comes out POINT B.C. while the paint is bent: round twelve; until then a red
  slash and dripping letters, which read as blood), `road.drive(row)` puts the wagon
  on the road at the right size for that row. Each takes a number from 0 to 1, so a tween
  can run it and a skipped movie lands on the same picture. `intro.js` runs them in
  order. `title.js` sets them all to their ends: the engine calls the cutscene named
  `title` to dress the stage behind the title screen, waits for it, and puts the game's
  name and the menu over it.
- The wagon is a painted sprite that a cutscene moves about
  (`g.view.cast.addPicture`, in the table at the end of section 10). The sun and the
  sign's second board are painted too, but lie on the live layer, because each is paint
  that a portal bends (it reads them in: `under`). The hole and its glow are light, and
  are drawn.

---

## 6. Saved games

### What is saved

One small object (`js/engine/state.js`): the act, the scene, which lead the player
controls, which leads they can switch between (the team), where each lead is standing
(in picture pixels) and which way they face, each lead's pockets, the list of story
facts ("flags"), the tunnel: things put into a door in time and not yet taken out
of another (section 8, "The letterbox"; a save with no `tunnel` field is from before
it, and the field being absent means empty), and what has been asked in dialogue trees,
and how many times (`asked`, section 7, "Dialogue trees"; absent in an older save, which
means nothing yet). Nothing else. Every scene rebuilds itself from those facts: its
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

### Testing: parts

**Temporary, for the testers; it will be taken out.** The pause menu ends with a row
marked "Testing: for testers; will be removed": the part of the story the game is at, with
**Previous part** and **Next part** under it. The keys **[** and **]** do the same during
play (not in a menu, and not while typing in a field). A part is a beat of the story
(`js/content/acts/*.js`), in story order, the opening of each act included, so a tester can
go straight to any puzzle, or back to the one before, instead of playing through everything
again. Next goes to the part after the furthest one done; Previous goes to the one before
it, so pressing it once undoes the last puzzle, and pressing it again goes back one more.
At either end the button is greyed, and its tooltip says why.

Going to a part loads a saved game, exactly as **Load game** does: the same checks, the
same way into the scene, and a note at the top naming the part ("Act One · Take the road
map from the glovebox"). Those saved games are `js/content/checkpoints.js`: for each beat,
the game as it stood the first moment the player had control after that beat was done, with
everything in the pockets, every fact, and everyone where they stood. They are not written
by hand. They are captured from the scripted playthroughs (the act tests described in
section 12), which play each act in the real game by real clicks: a hook in each script
keeps a copy of the game's own autosave whenever a beat's fact has just come true, and
`python3 scratchpad/checkpoints/build.py` runs the four plays, gathers what they captured,
writes the file in story order, and loads every checkpoint to see that it opens. It takes
about half an hour, because the plays are slow by design, and it has to be run again
whenever an act's beats, scenes or scripts change, or the parts will be yesterday's game.

Three things follow from where the saved games come from. An act's gate and the next act's
opening are one moment (the player first has control again after the hand-over), so they
are one and the same saved game, and the buttons treat them as one part, named for the
opening. The plays do the puzzles of an act in their own order, so a part can have a later
puzzle of the act done already (Dad has the copper mirror before the shade is up); the row
names the part that was jumped to until a puzzle is done or undone, and then the furthest
one done. And the last part is the end of the demo: the door open where the tracks stop,
and the family at it, as the game stood when the ending went to the title screen.

To take it out: the block marked TESTING-9 in `js/engine/game.js` (and the import at its
top and one line in `bindInput`), `testingRow` and its three lines in `js/engine/ui.js`,
the `.testing` rule in `css/game.css`, and the data file.

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

### Dialogue trees

The author, 10 October: the dialogue branches in the LucasArts games "are all enjoyable with funny and cute quips back
and forth", and they are part of the puzzle: they give clues, they change things, and they are where the jokes are. A
flat menu in a loop (`g.choose` four times over) cannot fork, forget, or remember. A tree can. The engine has it as
`await g.talk(tree)` (marked `TALK-11` in the code), with nothing of any one conversation in it: a tree is plain data
that a scene file holds, and every word in it is a line id as everywhere else.

```js
const JOE = {
  id: "joe",                                                   // what the memory is kept under (below)
  start: "open",                                               // the node to begin at, or a function of the game giving one
  nodes: {
    open: {
      say: ["nevada.joe.look.up"],                             // said on arriving at the node, exactly as g.say says them
      options: [
        { id: "morning", line: "nevada.joe.opt.morning", then: "liked" },                            // -> another node
        { id: "lemonade", line: "nevada.joe.opt.lemonade", say: ["nevada.joe.lemonade.1"], then: "asking" },
        { id: "raccoon", line: "nevada.joe.opt.raccoon", set: "joe.liked", then: "raccoon" },        // sets a fact, too
        { id: "vegas", line: "nevada.joe.opt.vegas", then: "vegas", do: (g) => g.sfx("portal") },    // a script, too
      ],
    },
    asking: {
      options: [
        { id: "car", line: "nevada.joe.opt.car", when: (g) => g.flag("joe.liked"), then: (g) => witness(g) },   // a script as the reply
        { id: "gas", line: "nevada.joe.opt.gas", say: { 1: ["nevada.joe.gas.1"], 2: ["nevada.joe.gas.2"], more: ["nevada.joe.gas.3"] } },   // the nth asking
        { id: "hens", line: "nevada.joe.opt.hens", once: true, say: ["nevada.joe.hens.1", "nevada.joe.hens.2"], set: "nevada.hensTold" },
        { id: "bye", line: "nevada.ask.bye", say: ["nevada.joe.bye"], then: "exit" },
      ],
    },
  },
};
// in the scene:   use: (g) => g.talk(JOE)
```

**A node** has `say` (line ids, said in order on arriving, by whoever each line belongs to), `options`, and `then`
(where to go after its lines, for a node that is only a speech: a greeting that leads to the questions). A node with
nothing to show ends the talk after its lines. Three names are the engine's: `exit` ends the talk, `back` is the node
this one was reached from, and `root` is the start node (`start` is asked again, so a start that reads the story gives
today's answer: the greeting the first time, the questions after).

**An option** is one thing the player can say:

| Field | Meaning |
| --- | --- |
| `id` | Its name, unique in the tree: what the memory is kept under |
| `line` | The line id the player picks: its words are the menu button, and it is said when picked, by whoever the line belongs to (the lead) |
| `when` | A test of the game: the option is offered only while it passes. Read again every time the menu is shown, so an option can come and go with the story |
| `once` | `true`: gone for good once it has been picked (the memory remembers across saves). Off by default |
| `say` | The reply: a list of line ids, said after the pick. Or an object keyed by how many times this option has been picked, `1`, `2`, `3`..., with `more` for every time after the last given, so a question asked twice gets a different answer |
| `set` | A story fact, or a list of them, made true (`g.flag`) |
| `do` | A script, `(g) => ...`, run after the lines and awaited: anything a script can do (walk somebody, hand something over, open a door) |
| `then` | Where to go next: a node id, `"exit"`, `"back"`, `"root"`, or a function of the game giving one of those, or nothing. Nothing means stay: the same menu again |

An option with no `say`, no `do` and no `then` just stays. The menu is the same `choose` menu as before, with its
number keys (1 to 9), and two things more: **Escape** picks the way out, when the node has one (an option whose `then`
is `"exit"`), and otherwise does nothing; and the menu **remembers**. An option picked before is written lighter (not
greyed out: it can still be picked, unless it is `once`), and one never picked carries a small round mark in the time
colour after its words, the completist's tick, as the classic games did it (`.choices .asked` and `.choices .new`).

**The memory.** The game keeps every pick: `asked["joe/car"] = 2` in the save, under the tree's `id` and the option's
(`g.talk(tree, { id })` names a tree that has none; with no id at all, under the scene's id and the node's:
`"nevada-roadside/open/car"`). A script reads it with `g.asked("joe/car")`, which is how an option can wait for another
to have been picked: `when: (g) => g.asked("joe/raccoon") > 0`. `seenLines` goes on counting every line as before; the
nth-asking replies come from `asked`, which counts the pick and not the words. A save from before trees has no `asked`,
which means nothing yet, and the save version stays 3. The Hint button and the beats are not touched: the beats are the
story's, a tree is a scene's.

**Skipping.** While a cutscene is being skipped a tree ends at once and safely: at a node, the way out is picked first
(an option whose `then` is `"exit"`), else the last option, and the talk ends after that one node, so a tree with no way
out cannot loop. The picked option's lines still count as seen, its facts are set and its script runs, so the game ends
up in the same state. A menu that is already up when skipping starts gives way the same way.

**Through the door.** `g.talk(tree, { through: "son" })` is the same tree held through a letterbox (section 8, "The
letterbox"): every menu is shown as the words of the lead who is off the stage, the picked line goes through the door
(`g.through`), and so does any reply line that belongs to that lead; everyone else's lines are said as they are. One
tree serves a talk face to face and the same talk through a door.

**The proof.** `index.html?scene=engine-proof&lead=dad&flags=proof.talk`: an old water carrier on the sand by the
river, with a tree (`CARRIER` in `engine-proof.js`) that uses every piece: a start that reads the story, four ways in,
a fork two deep (the river, then the fish), his name once and only once, the jars answered differently each time, an
option that appears only after another was picked, a `do` that walks him to the water and back, `back`, `root`, and a
goodbye that is a line. The engine test's `talk` part plays all of it, by key and by Escape, through a door, skipped,
saved and loaded.

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
travels to wherever he is (by the short tunnel, when the two scenes are in different
eras). The story can also cut between leads by itself, as it does
at the end of each act. A strong fit for this premise: something sent through a door
in one era turns up in another, so people who are apart can still help each other.
(The coin the Son throws into the door in Rome falls out of the sky in Nevada.) The
engine has this as the letterbox, below.

**Together.** Mom and the girls go through the house as one. Each of its five scenes
(the living room, the landing, Dad's study, Little Sister's room and Big Sister's attic)
says so with `party: ["mom", "bigsis", "lilsis"]`: when the one being played takes the
stairs, a door or the attic ladder, or walks off the edge of the picture, the other two
come too and arrive beside her, each on a place of her own, and switching between them
is instant because nobody has to go anywhere. ("A scene for several leads" in section 10
shows how a scene says where each of them arrives.)
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

### The letterbox

The author, 10 October: the family is split three ways in three times, and "they are able to communicate through the
portals and pass items through because the portals are small." Later each of them steps through a wide door and lands
somewhere new, and "they have to communicate with each other to figure out where and when." So a door in time that is
too small to step through is a letterbox: a thing goes in at one end and comes out at the other, centuries away, and
voices carry through it. The engine has this generically (marked `LETTERBOX-11` in the code), with nothing of any one
puzzle in it: which door takes which thing, and every word said, belong to the scenes.

**The tunnel.** A thing put into a door waits in the tunnel until the lead it is for takes it out of a door of theirs.
The save body keeps the list: `tunnel: [{ item, from, to, at }]`, the thing, who sent it, who it is for (lead ids), and
the play time it went in. A save from before the letterbox has no such field, and the field being absent means empty:
`complete()` in `state.js` gives it an empty list, and the save version stays 3 (the note at the top of `save.js`).

**The four calls.** A scene's door does the sending and the receiving with them; the engine keeps the list, marks the
portrait and draws the arrival.

- `g.send(item, { to })`: the active lead puts a thing they are carrying into the door for another lead. It leaves their
  pockets, goes on the tunnel list, the HUD refreshes, the game autosaves; true if it went. A thing they are not carrying,
  or a `to` that is not another lead, gives a console warning and nothing happens. A door's `useWith` calls it, with the
  scene's own lines: the engine does not decide what fits through.
- `g.waiting(who = the active lead)`: the tunnel entries for that lead, oldest first.
- `g.receive(item)`: takes the named entry (or, with no name, the oldest waiting for the active lead) out of the tunnel
  into their pockets (`g.give`), and returns it; null if nothing of the kind waits for them.
- `await g.arrive(item, [x, y])`: the thing drawn arriving: its inventory picture pops out of the point (the door) in a
  small arc, over the shoulder of whoever stands at the door, and lands with a puff at the lead's feet, on the side away
  from the door (`{ to: [x, y] }` says where instead), then is taken off the stage; about 600 ms, and it resolves when
  done. In the air it is behind whoever stands in front of the door, on the ground in front of them, as the luggage on
  the wagon's roof is unpacked. A thing with a drawn icon and no painted picture makes only the puff.

The door's script does the moment: on entering a scene with a door, or on using an open door, it asks `g.waiting()`,
and for each entry plays `g.arrive`, says its line, and calls `g.receive()`.

**The mark.** When something waits for a lead who is on the team, their portrait in the team bar carries a small round
mark in the time colour at its top left (`data-post` on the portrait's button; the interface's own colours, never the
scene's paints), and pointing at the portrait says what waits: "Play as Son. Something has come through for Son: the
pack of gum". The mark goes when the thing is received. The active lead's own portrait shows it too: something waits for
them, and the scene's door will give it.

**Voices through the door.** `await g.through(who, "line.id")` is a line from a lead who is not on the stage, at the
other end of a letterbox: shown top centre, as a line with no speaker on stage is, with that person's portrait beside
the words (the interface's `portrait`, drawn for the pixels it is shown at, never keyed) in that person's colour, and
with the `through` style (`.say.through`: lighter and leaning, as from a little way off; no echo gimmicks). It counts
the line as seen, waits and is skippable like `say`. A `choose` works the same way: `g.choose(options, { through: who })`
shows the menu as that person's words, their portrait and name at its head and the options in their colour (the options
are what the lead off stage may say). The lead on stage speaks ordinary `g.say` lines over their own head, so the player
sees one person on stage talking to a portrait of the other, which is the whole picture of a letterbox.

**Switching across the centuries.** Switching to a lead who is in another scene travels there, as before; when the two
scenes are in different eras (`scene.era`) the trip is the short tunnel (`g.goto(..., { via: "wormhole" })`), and within
one era it is a fade, as it always was. Their place and facing are kept. A lead can be switched to only if they are on
the team; the scenes decide the team.

**The proof.** `index.html?scene=engine-proof&lead=dad&flags=proof.letterbox`: Dad on the sand with a pack of gum, the
Son in the market street sketch in Rome, a small door in the air. The gum goes in the door for the Son, the mark
appears, switching to him is the tunnel, and coming back as him the door gives it up. The door with nothing in hand is a
word through it, with a choose through the door. The engine test's `letterbox` part plays all of it.

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
| **Travellers** | Dad's yellow shirt, the Son's blue hoodie, Mom's emerald dress, Big Sister's indigo cardigan, Little Sister's pink overalls and yellow boots, the red wagon | The people and things from the present | Never (each era's light falls on them: "The paints") |
| **Era** | The warm stone and sand of Egypt, the brick and blue shadow of a Roman street, lamplight and wallpaper at home, the dust of Nevada | The world of each period | Per era |

Because of this, in any screenshot from any era you can tell at a glance what
belongs to the period, who the visitors are, and where time is leaking through.

Each member of the family owns one color that nobody else in the family wears, and
their words on screen are a pale tint of it. Everyone else who speaks has a tint that
nobody else in the game uses (`cast` in `world.js`).

### How futuristic and ancient blend

They are kept apart on purpose, and the contrast is the style:

- **The world is painted, warm and matte.** Earth, stone, water, linen, wood.
- **A door in time is the world, bending.** Since round ten it is not a drawn thing
  over the painting but the painting itself, rippling as if a stone had been dropped
  in it (section 2, "The door in time"): the paint stays paint, wet and lit. What still
  glows, drawn smooth on the live layer, is the light it throws: the glow down the road,
  the spot of sun off a coin, the beam that opens the chamber.
- **Doors in time are invisible until the puzzle that opens them is solved.** Before
  that there is nothing to see: only what people say about a hum.
- **The interface is ancient, with neon for "active".** Menus, buttons, cards and
  the title are ink on papyrus, in Koine Road. The selected item or tool turns cyan.
- **One signature shape, kept small.** The dashed rings turning in opposite directions
  remain the game's mark: in the browser tab icon, on the gate you click to begin, and
  rushing past in the time tunnel between eras. The doors themselves no longer wear them.
- **A possible motif to grow:** let the eras leak into each other as the story goes
  on. A Roman column with a neon crack. A hieroglyph that is a road sign.

### The era palettes

`css/tokens.css` still gives each era a palette of seventeen slots (eight sky bands, two
silhouettes, three grounds, a dark, a light, two features), and the stage carries
`data-era="egypt"`. The paintings do not use it. It colors what is still drawn by code:
the sketch of a scene that has not been painted, props, and the storyboard page, which
shows all the palettes side by side.

### The paints

Chosen on 9 October: **every picture in the game is mixed from one box of paints, the Post-Impressionists' 23 of 1888,
in a key for its era and hour, at strength 50.** The paintings are kept exactly as they were painted (every shape, edge
and detail, the depth, the light's direction), and their colours are moved toward the box:

- **Shadows become a colour.** A shadow takes its key's shadow paints at its own lightness (lilac, cobalt violet, deep
  violet on warm ground and stone; viridian on greens; ultramarine on blues), instead of grey or brown. A thing that is
  only dark in its own colour (bronze, wood, a red wall) leans toward its own darker paint and stays itself.
- **Lights warm** toward the key's light (naples yellow and lead white in Rome's sun, chrome yellow at noon, lamplight
  indoors). A pale wall keeps its own colour; the light only warms it.
- **Every colour moves part of the way toward its nearest paints**, a little purer, as paint is purer than a print.
  There is no black: the darkest darks lean to prussian blue and deep violet.
- **A little of the painters' touch:** sparse short marks laid along the forms, each a little lighter and warmer or
  darker and cooler (broken colour). Fine detail and lettering are left alone.

The six keys (numbers in `tools/paint/postimp_paints.py`; the game reads them from `js/art/look-data.js`):

| Key | Scenes | The pair | Light | Shadow |
| --- | --- | --- | --- | --- |
| Egypt at noon | egypt-crash, egypt-site | chrome yellow / cobalt blue | naples and chrome yellow, through orange | lilac, cobalt violet, deep violet |
| Rome in the morning | rome-steps, rome-street | naples yellow / cobalt violet | lead white, naples yellow | lilac, cobalt violet, toward ultramarine |
| The house at night | home-living-room, home-landing, home-study, home-lilsis-room, home-bigsis-room | lamplight / ultramarine | naples and chrome yellow, chrome orange | ultramarine, deep violet; viridian on greens |
| Lamplit rooms | egypt-gallery, egypt-chamber, rome-temple | chrome orange / ultramarine | chrome yellow, chrome orange (the lamps are lights, not lit walls) | ultramarine, deep violet |
| Nevada in the morning | nevada-roadside | chrome orange / cobalt blue | lead white, naples and chrome yellow | lilac, cobalt violet |
| The highway at dusk | highway (the title screen and the opening movie) | chrome orange / ultramarine | chrome yellow to orange and geranium | cobalt violet, deep violet |

**Strength 50.** The keys run from 0 (the painting as painted) to 100 (the paints at their clearest); the game uses 50
everywhere (`STRENGTH` in `postimp_paints.py`, `strength` in `look-data.js`): every scene still reads as the painting
it was, with coloured shadows, warmer light and one box of paints shared by the places and the people.

**Where it happens.**

- **The pictures** are keyed once, when they are installed: `tools/paint/install.py` runs `postimp_key.py` on the
  painting in `out/`, so every file in `art/scenes/` is keyed already. The scene is keyed as the game composes it (back
  and cut-outs together, so they read the same light); every cut-out keeps its exact edge; the frames of things that
  move are keyed colour by colour, their shapes untouched; a scene's files share one palette of 255 colours.
  `postimp_keyed.json` notes what each file was keyed from, and `python3 tools/paint/postimp_key.py --check` checks
  every scene.
- **The people** are drawn by the rig in today's pixel art, and `js/art/look.js` keys their colours for the scene on
  the stage: `game.js` names the scene as it builds it (`keyScene`), `pix.js` asks for each material's four tones
  (`tonesOf`: the light ones toward the key's light, the shade ones toward its coloured shadow) and for each exact
  pixel (`pixelOf`), and the shadow on the ground under each person becomes the key's shadow colour instead of a grey.
  Shapes, faces and motion are the rig's own. Pictures kept from a scene in another key are let go (`forget` in
  `cast.js`). **The team portraits are the interface's and are never keyed** (`portrait()` in `cast.js` draws each
  one inside `withoutKey`, at the size the interface asks for, and keeps it).
- **The moving things** (`effects.js`): the colours a scene gives its smoke, flames, embers, water and drawn birds, or
  the engine's own defaults for them, go through the same key (`keyHex`) as each is put on the stage; their painted
  frames are keyed with the pictures.
- **Never keyed:** time (the tunnel, and the pale light at the heart of a door in time: its colour belongs to no
  place; the paint a door bends is keyed already, being the picture), and the interface (the buttons, the label line,
  the inventory and its pictures, the title strip, the cards).

**A new scene, or a repainted one** (the four new places in Rome, say):

1. Paint it with its script, into `tools/paint/out/<scene>/`, as ever.
2. Give it a plan in `tools/paint/postimp_plans.py` (its cut-outs in the scene file's order, the cut-outs of other
   states, its frames), and a key in `postimp_paints.SCENE_KEY`: a place out of doors takes its era's key (the Forum,
   the Capitol, across the Tiber: "rome-morning"); a room lit by lamps takes "lamp-interior".
3. `python3 tools/paint/install.py <scene>` keys it at 50 and installs it.
4. `python3 tools/paint/postimp_key.py --js` (when the table or a key changed), then `--check`, then `tools/stamp.py`.

A scene missing from the table is drawn with its era's key (`ERA_KEY`) until it is added. A new era gets a key of its
own in `postimp_paints.KEYS`: copy the nearest, choose its complementary pair, its light and shadow paints by
lightness, and add it to `GROUND_SHADOW` and `ERA_KEY`. Never key a picture twice: `install.py` always starts from the
painting in `out/` (the paintings as they were before the paints are in the repository's history).

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
  edges: {                                      // ways out at the edges of the picture (below)
    N: { to: "sketch-example", name: "up the track", walkTo: [496, 302] },
    E: { to: "sketch-example" },
    W: { to: "sketch-example", name: "across the river", when: (g) => !!g.flag("proof.ferry"),
      use: async (g) => { await g.say("egypt.river.look"); await g.goto("sketch-example"); } },
  },

  picture: art + "back.png",                    // the backdrop
  planes: [                                     // painted cut-outs, sorted with the people
    { id: "palms", src: art + "palms.png", base: [[187, 407], [298, 321]] },     // a base line: they stand in a row along the bank
    { id: "wagon", src: art + "wagon.png", base: [[490, 541], [790, 537]],
      solid: [[470, 528], [790, 522], [796, 548], [470, 556]] },                 // the ground it takes up
    { id: "papyrus", src: art + "front.png", plane: "front" },                   // always in front
    { id: "trunk", src: art + "trunk-open.png", base: 541, when: (g) => g.flag("egypt.trunkOpen") },   // (added) there only while the story says so
  ],
  live(art, g) { return `<polygon id="beam" .../>`; },                           // (added) light, drawn and not painted
  fx: [                                         // (added) things that move by nature, drawn moving (section 2, "Things that move by nature")
    { id: "door", type: "portal", at: [500, 300], r: 40, base: 342 },                                             // a door in time: the paint bending; a script opens it, g.effects.get("door").open(1)
    { id: "fire-smoke", type: "smoke", at: [468, 422], base: 430, height: 130, width: [6, 46], wind: 7 },          // its base: a man behind the fire is behind its smoke
    { id: "doves", type: "birds", look: "dove", count: 6, area: [[268, 372], [318, 334], [372, 338], [392, 372], [330, 402], [282, 400]] },
    { id: "palms-sway", type: "sway", plane: "palms", anchor: "bottom", amount: 1.4 },                            // a cut-out stirring from its feet
  ],

  actors: [{ id: "lot", kind: "lot", at: [404, 432], face: "E",                 // (added) people who are not the lead (Lot sits: his kind says so)
    life: { every: [18, 40], spots: [[446, 470, "E"]], stay: [3, 8] } }],       // (added) what they do by themselves now and then (section 4, "Their own lives")
  hotspots: [
    { id: "pyramids", name: "pyramids", rect: [432, 78, 368, 172], look: "egypt.pyramids.look" },       // a box: x, y, width, height. (A circle is [x, y, radius].)
    { id: "wagon", name: "wagon", verb: "Search",                                // (the verb is added: what the pointer says it will do)
      plane: "wagon",                           // (added) Show outlines the wagon's own silhouette (here it would anyway: a cut-out has this id)
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
the game to see an outline round every clickable thing, and an arrow at every way out at
an edge. The storyboard page draws each scene with its
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

**Light.** A beam, a glow, a spot of sun: return it from the scene's `live(art, g)`, as
drawing markup in picture pixels. Give a part an `id` and a script finds it with
`g.q("#beam")`, to fade, move or scale it. The live layer is under the cast. A door in time
is not light: it is a `portal` among the scene's `fx` (section 2, "The door in time"), and
a script opens it with `g.effects.get("door").open(k)`.

**A way out at the edge of the picture.** As in the old adventure games, the player can
walk off the edge of the screen. A scene lists the ways out across the edges of its picture
under `edges`, by side: `N` is the top of the picture, `S` the bottom, `W` the left, `E` the
right (`js/engine/edges.js`):

| Field | Meaning |
| --- | --- |
| `to`, `spawn` | The scene, and the named way in at the other end: what `g.goto(to, { spawn })` is given, as for a door. Without `spawn` the lead arrives on the other scene's usual mark. |
| `name` | What the label line says: `"Go "` and the name ("Go up the track"). Without one, `"Go to "` and the other scene's own name, with "The", "A" or "An" made small ("Go to the great gallery"); a name that begins with somebody's name keeps its capital ("Go to Little Sister's room"). When the other scene's name does not read well after "Go to", give `name`. |
| `walkTo` | Where the lead walks before leaving. Without it: the floor nearest the click, pushed as far toward that edge as the floor goes (for the top and the bottom, in the column of the click; for the sides, along the row of the floor nearest the click). A way that is one particular path (a track, a stair) should say where it starts. |
| `when` | A test of the story. The way is there only while it passes; until then its band is plain floor. |
| `use` | A script to run instead of the plain `g.goto`, with the controls held as for any script: a way out that is also a gate, or that needs a line first. |

Along each edge that has a way out lies a band: the top 60 pixels of the picture, the
bottom 52, the left 44, the right 44. Where two bands meet, a point belongs to the nearer
edge. Over the floor in a band the pointer becomes an arrow pointing out of the picture
that way, drawn for the game (`edge-n`, `edge-s`, `edge-w` and `edge-e` in
`css/game.css`), and the label line says where the way leads. A click there walks the lead
toward that edge, and when he is there the scene changes, the party coming along as
through any door. It is an ordinary walk, not a script: a click anywhere else on the way
sends him there instead, and nobody leaves; a double click hurries him; on a touch screen a
tap does the same. Anything that can be clicked in a band wins over it: a clickable area, a
companion standing there, a button of the interface. With a thing in hand a band is floor
like any other (a click puts the thing away), and in look mode a click there only ends look
mode: nobody leaves by looking. The doors, stairs and tracks a scene already has as
clickable areas go on working beside its edges, and they are what a keyboard reaches.

At every start the engine checks every scene's ways out and warns in the console
("Edge check: ...") about a way to a scene that does not exist, a `spawn` the other scene
has no mark for, a side that is not one of the four, a way with neither `to` nor `use`, or a
`name` that begins with "Go" (the label puts that in itself).

**What Show shows.** The **Show** button (for a moment), holding **H**, or `g.reveal(true)`
in a script puts the class `reveal` on the clickable layer, and a layer of its own shows an
outline round each thing that can be clicked: a crisp light line, two pixels wide, just
outside the thing, with a soft time-cyan glow outward, and nothing filled
(`js/engine/outline.js`). Which outline:

- An area that names something on the stage follows that thing's own silhouette, as it is
  drawn at that moment (its state, its frame, where it stands), as much of it as lies inside
  the area grown by four pixels. It names it with `plane: "<id>"`; with no `plane`, a cut-out,
  a person or a prop with the area's own id is taken. So the wagon is outlined as a wagon,
  and the man by the river as the man himself, not as boxes.
- A companion is outlined by her own figure.
- Any other area by its own `poly`, `rect` or `circle`, so a shape should hug its thing to
  within a few pixels. An area whose thing is not showing falls back to its own shape.
- An area whose `when` fails is left out. Each way out at an edge gets a soft arrow at the
  middle of its edge.

It is drawn once when Show is turned on, and again only if what it shows changes while it
is on: another scene, an area coming or going, a cut-out's state, a companion's place. The
area that has keyboard focus (Tab) gets the same outline, by itself.

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
(section 2, and the guide in `tools/paint/`), install the pictures into
`art/scenes/<scene id>/` with `tools/paint/install.py`, which keys them in the game's paints
(section 9, "The paints"), name them in the scene file, and take the numbers from the
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
console. The engine puts "the" before a thing's name when it makes a sentence of it ("You
have the reed", "Mom has the reed", "Put the reed away"), except for a proper name: give
the thing `proper: true` and it is "You have General Feathers". A name that begins with a
capital counts as proper by itself ("You have Dad's pencil"); `proper: false` puts "the"
back.

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

GitHub Pages lets a browser keep each file for ten minutes. The game is some sixty code
files and more than a hundred pictures, so without care a browser can end up running new
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
| `await g.through("son", "id")` | A line from a lead who is not on the stage, at the other end of a small door in time: top centre, with their portrait beside the words, in the `through` style (section 8, "The letterbox"). Counted, timed and skippable as `say` is. |
| `await g.choose([{ id, line }], { through: "son" })` | The same menu as that person's words: their portrait at its head, the options in their colour |
| `await g.talk(tree)`, `await g.talk(tree, { through: "son" })` | A dialogue tree (section 7, "Dialogue trees"): nodes with lines and options, options with `when`, `once`, a reply (or one for each asking), `set`, `do`, `then` (a node, `"exit"`, `"back"`, `"root"`); remembered in the save, number keys and Escape, ends safely when skipped. Through a door, the same tree as that person's words. Resolves when the talk is over |
| `g.asked("joe/car")` | How many times that option of that tree has been picked (0 if never): for a `when` that waits on another question |
| `g.send("gum", { to: "son" })` | The active lead puts a thing they carry into a door in time for another lead: out of their pockets, into the tunnel (the save keeps it), the mark on that lead's portrait; true if it went. A thing they do not carry, or a `to` that is not another lead: a console warning, nothing happens. The scene's door calls it from its `useWith`, with its own lines: the engine never decides what fits. |
| `g.waiting()`, `g.waiting("son")` | What waits in the tunnel for the active lead, or for another: `[{ item, from, to, at }]`, oldest first |
| `g.receive()`, `g.receive("gum")` | The active lead takes the oldest thing waiting for them, or the named one, out of the tunnel into their pockets; gives back the entry, or null |
| `await g.arrive("gum", [x, y])` | The thing drawn arriving: its inventory picture pops out of the point in a small arc and lands with a puff at the lead's feet (`{ to: [x, y] }` elsewhere), then is taken off the stage; about 600 ms. The scene then says its line and calls `g.receive()`. |
| `g.flag("name")`, `g.flag("name", true)` | Reads or records a story fact. Recording one makes the cut-outs and the clickable areas read their tests again. |
| `g.give("item")`, `g.take("item")`, `g.has("item")` | Pockets of the current lead |
| `g.holder("item")`, `g.item("item")`, `g.the("item")` | Which lead is carrying a thing, or `null`; the thing's own entry in `items`; and its name as it goes into a sentence ("the reed", "General Feathers") |
| `await g.goto("scene", { via: "wormhole" })` | Changes scene by fade, cut or time tunnel. `{ spawn: "name" }` arrives on that mark of the scene's `spawn`, and the rest of a `party` on its `arrive` places of that name ("A scene for several leads", above). |
| `g.leave("N")` | Leaves by the scene's way out at that edge, as a click in the middle of its band does: the lead walks there, and on. `g.edgeAt(x, y)` says which way out a place of the picture lies in the band of (`"N"`, `"S"`, `"W"`, `"E"` or `null`), and `g.leaving` which one the lead is on his way out by. |
| `g.reveal(true)`, `g.reveal(false)`, `g.reveal(true, 2400)` | Show: turns the outlines on until told otherwise, off, or on for a while (as the button does). `g.outlines.drawn` lists what was outlined, and how. |
| `await g.card("Ancient Egypt", "about 1920 B.C.")` | Shows a title card. (Egypt is about 1920 B.C. because the game counts the years before Christ from the Bible's own genealogies, as Archbishop Ussher counted them: see "How the game counts the years" in [CHARACTERS.md](CHARACTERS.md#how-the-game-counts-the-years).) |
| `await g.cutscene("intro")` | Plays a skippable cutscene |
| `await g.wait(ms)`, `await g.tween(ms, (k) => ...)`, `await g.fade(1)` | Timing, motion, fades |
| `g.music("egypt")`, `g.sfx("portal")` | Sound. `g.musicOf(g.scene)` is the track the scene plays now: its `music`, which may depend on the story, or its era's. |
| `g.effects.get("altar-smoke").show(false)`, `.show(true)`, `.auto()` | One of the scene's moving things (`fx`) taken away, or shown, whatever its `when` says; `auto()` hands it back to its `when` (section 2, "Things that move by nature"). |
| `g.effects.get("pigeons").scare([x, y])`, `.scare()` | The birds of a flock near that place go up (all of them, with no place), as if somebody had rushed at them, and keep clear of it for a moment: a "Chase". |
| `g.effects.add({ type: "flame", at: [x, y], size: 10 })` | Puts another moving thing on the stage, until the scene changes (a fire the story lights). |
| `await g.settle()`, `await g.settle("scribe")` | Brings everyone of the scene's people who is away on a walk of their own home (or one of them), briskly, sitting down if they sit (section 4, "Their own lives"). Every script already gets this before it starts. |
| `await g.walkTo(x, y)`, `await g.walkTo(x, y, "scribe")` | Walks the lead, or someone else, to a place, round whatever is in the way |
| `await g.moveTo(x, y)`, `await g.moveTo(x, y, "agent")` | Walks in a straight line to a place the player could not click on (into a closet) |
| `await g.reach()`, `await g.reach(true)` | The lead reaches out, or bends down to the ground |
| `g.lead.hold()`, `g.lead.hold(false)` | Someone keeps an arm held out while people talk (holding a thing up), until told to let it drop |
| `g.actor("mom").pray()`, `g.actor("mom").pray(false)` | Someone prays, in their own way (section 4), through whatever is said, until told to stop: standing still, or sitting where they sit. End it before they walk. |
| `g.lead.shade()`, `g.lead.shade(false)` | Someone standing shades their eyes from a glare (section 4) until told to stop |
| `g.assets.url(path)`, `g.assets.picture(path)` | For a script that puts a painted picture on the live layer: its stamped address, and a promise that it has arrived |
| `g.actor("scribe").face("W")`, `g.lead.look(x, y)` | Turns someone to a compass point, or toward a place |
| `g.plane("trunk")` | One of the scene's cut-outs, or `null`: `.show(true)`, `.set("open")`, `.fade(0.5)`, `.place(x, y, scale)` |
| `g.actor("scribe")`, `g.lead`, `g.q("#beam")`, `g.effects.get("door")` | Reach people, the parts of the live layer, and the moving things (a door in time among them: `.open(k)`) |
| `g.team(["mom", "bigsis", "lilsis"])` | Says which leads the player can switch between from now on |
| `await g.switchLead("son")` | Changes who the player controls (they must be on the team). One who is in another scene is travelled to: by the short tunnel when the two scenes are in different eras, by a fade within one. |
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
| `tools/paint/` | The scripts that paint the pictures, one for each scene, with their shared library and the painter's guide. `python3 install.py <scene>` keys a painted scene in the game's paints and copies it into `art/` (section 9, "The paints"). |
| `tools/koine-road/` | The scripts that build the typeface from pen strokes (it has a README of its own) |

Useful addresses while building:

- `index.html?scene=egypt-site&lead=dad&flags=egypt.sawSite` jumps straight to a scene.
- `index.html?scene=engine-proof` is the worked example of a painted scene.
- `index.html?intro` plays the intro again.

In the browser's console, `game` is the game object that scripts are handed as `g`.

**The engine's test** drives a real browser through the engine and fails on any console
error: the painted stage and its layers, depth read off the screen pixel by pixel,
walking and routes, every form of cut-out, live light, close-ups, the inventory, old
saves, every scene in the list (and that each of its ways out at the edges can be
clicked and walked to), how the cast layer repaints, how people are sized, seated people
talking, words over heads, the ways out at the edges of the picture, the outlines of
Show, the names of things with and without "the", the fetching of every picture behind
the title (and that nothing is asked of the server afterwards), hard and smooth pixels,
the interface at two sizes and in three other window shapes, the storyboard page, the
intro and the stamping tools: some 250 checks, in about four minutes. It takes screenshots, which
have to be looked at: a picture that is wrong throws no error. Three more scripts
measure what a frame costs (the table in section 1), take the pictures that the choice
between hard and smooth pixels was made from, and take pictures of seated people
talking and of words over heads in the real scenes. These scripts are not in the repository yet: they were written
beside the game, and their paths have to be changed before they can be run from here.

---

## 12. What is built and what is not

**Built, and meant to stay:** the engine, the 800x600 painted stage with its cut-outs
and live light, the depth system, the things that move by nature (smoke, flames, water,
birds, cloth), the save format, the sound system, the line-ID
dialogue system, the story-as-data structure, the pixel renderer and the figure, the
interface, the Koine Road typeface, the stamping of files, and the letterbox (things
and voices through a small door in time, between leads who are centuries apart: section
8). No act's scene uses the letterbox yet: that is for the story to decide.

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
- The moving things in the acts' own scenes. The engine draws them (section 2, "Things that move by nature") and the
  painters have taken them out of the pictures and marked them in each scene's `layout.json`; the scene files list them
  under `fx` next round. Not built: a startled bird landing in another flock's place (the gutter, say), and sound for
  any of them (a fountain's splash, the crackle of a brazier).
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
seated or standing, small or full size. The ways out at the edges were tried with a real
mouse and a real tap: the arrow and the label in each band and in a corner, an area and a
companion in a band winning over it, a way that is not there yet, a click that changes its
mind on the way, look mode, a thing in hand, a double click, and the party arriving
together on the other side. Show's outlines were read off the screen: nothing inside any
area is filled, and every pixel of the line round the wagon, and round a companion, lies
within three pixels of their own paint. And with the title up and the pictures gathered,
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
| Leave by the edge of the picture | Click near that edge, where the pointer turns into an arrow pointing out | Tap near that edge | Tab to the door or the path, Enter (where the way out is also a thing to click) |
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
| Show what can be clicked (an outline round each thing, an arrow at each way out) | **Show** | **Show** | Hold H |
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
8. **How near an edge a click leaves the scene.** The bands are the top 60 pixels of the
   picture, the bottom 52 and 44 at each side (`BANDS` in `js/engine/edges.js`), and
   anything clickable in a band wins over it. Wider bands are easier to hit and take more
   of the floor away from plain walking.
9. **Hints:** a Hint button that has the lead think aloud. Keep it, limit it, or
   drop it.
10. **Voices:** from the start or later. The engine handles either.
11. **Who the leads are.** [CHARACTERS.md](CHARACTERS.md) describes all five. Nobody has
    a name yet: on screen they are Dad, Son, Mom, Big Sister and Little Sister.
12. **Where the present-day chapter goes.** It plays after Rome. It could open the game
    instead, or be cut in between the scenes in the past.
13. **The puzzles.** The three puzzle documents lay them out so they are easy to change.
14. **Big Sister's facts.** Every fact she states has to be true. The list, and which
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
