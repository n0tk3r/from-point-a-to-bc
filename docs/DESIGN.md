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
| People | Drawn by a jointed figure from a page of settings, not stored as pictures (an animal is painted frame by frame instead) | One description gives all eight directions, every animation and every size. See section 4. |
| Depth | People, props and cut-outs are painted back to front by where they touch the ground (only things whose pictures overlap are ordered against each other, so that a base on a slant never puts anybody on the wrong side of it), and people shrink toward the horizon | The lead walks behind the car, in front of it and round it, with no hand-made mask. See section 3. |
| Movement | One game clock drives anything that matters to the game. CSS runs only the glow of time travel and a few ambient loops. | Each tool does the job it is best at. See section 1. |
| Intro movie | A script that moves the game's own art. Not a video file. | A few KB of script and six pictures instead of tens of MB, identical in style to the game, skippable, subtitled. |
| Saves | Autosave and three slots in the browser, plus a save file the player can download and load anywhere | Browser storage can be wiped. A file is the player's own. |
| Sound | Web Audio with separate volume for music, effects and voices | Standard, works everywhere, lets music duck under speech. |
| Dialogue | Every line has an ID. Text now, a sound file with the same name later. | Voices can be added one line at a time without touching any script. |
| Story | Acts and beats listed as data, with a checker and a storyboard page that also draws each act's places as a map of their ways | Parallel puzzle chains inside an act, one gate at the end of it. |
| Leads | Seven people the player can control: the five of the family, and in Act Five Grandpa Joe and Ranger the raccoon. Apart, each has scenes of their own. Together, the player switches between them with their portraits. | A father and son lost in different centuries, a mother and two daughters working as a team, and an old man and his raccoon as a team of two. See section 8. |
| Look | One way of painting, one figure and one light for every person, one typeface, and time travel in neon | Each era changes what is painted, never the rules. See section 9. |
| Updates | Every code file, style file and picture is fetched by an address that changes when the file changes, and a game in progress keeps what it has fetched | A push can never leave a browser running old files next to new ones, or put a new painting behind an old script. See "Publishing a new version" in section 10. |

Size today (round fifteen): 76 code and style files, about 2.9 MB (about 790 KB when the
server compresses it; the testers' saved games, `checkpoints.js`, are about 0.7 MB of that,
and compress to under 30 KB); 652 pictures, 11.5 MB in all (76 of them the engine's own, for
its proof scene, 12 the game's emblem, and 35 the four maps); a 49 KB font; and a few small
files of measurements (the maps' `layout.json`, the painted figures' sidecars). Nothing else
is downloaded. <!-- MAP-15D: it was, at round thirteen, 74 files, about 2.8 MB (760 KB
compressed), and 614 pictures, 9.5 MB -->

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
  cast.js                 people (drawn by the rig, or painted frame by frame), painted cut-outs and props: depth order, animation, the store of finished pictures
  walk.js                 where the lead can stand, routes round obstacles, size by distance
  life.js                 the scene's people living their own lives: small movements, and a walk now and then
  edges.js                ways out at the edges of the picture: the bands, what the label says, a check of every scene's
  outline.js              Show: an outline round each thing that can be clicked
  fx.js                   canvas effects (the time tunnel)
  effects.js              things that move by nature: smoke, flames and embers, water, birds, cloth that stirs, the country going by a car's windows
  story.js                reads the story data: open beats, checks
  ui.js                   heads-up display and menus
  atlas.js                the map screen and the Timer: travel on the map, switching through it, the maps' check (MAP-15)
  game.js                 ties it together; the `g` that scripts use
js/art/                 everything that is drawn by code
  kit.js                  the neon rings (the title, the tunnel; the tab icon is the emblem since EMBLEM-13), the sketch of an unpainted scene, close-ups, and the old 320x200 drawings
  pix.js                  the pixel renderer: solid shapes in, pixel art out
  rig.js                  the jointed figure: poses, eight directions, the walk, stances, gestures, sitting
  people.js               the cast as the rig sees them: proportions, clothes, colors, and how each one stands, walks and talks
  painted.js              the people who are painted frame by frame and not drawn by the rig (Ranger, and the proof's critter), and where each one's sidecar is
  props.js                things drawn by code that stand on the ground (kept for scenes that are not painted yet)
  look.js                 the paints: the people and the moving things in the key of the scene on stage (section 9)
  look-data.js            the paint box, the six keys and which scene uses which (written by tools/paint/postimp_key.py)
js/content/             the game itself. Knows nothing about the engine's insides.
  world.js                cast, eras, items
  lines.en.js             gathers the spoken lines
  lines/*.en.js             the lines, one file to an act: common, egypt, rome, home, nevada (with the cut-scene "Backup"), limo
  talk/nevada.js          the talks of Act Four and Act Five, as dialogue trees: Grandpa Joe, Grandma Jolene, Ranger, the hens, the letterbox, the divider
  talk/rome.js            the talks of the bigger Rome's seven (Act Two, since round thirteen), as dialogue trees: the Gaul, Phyllis, Titus, the goose-keeper, Eleazar, Mariam, Felix
  story.js                where a game starts, stock replies, and the list of acts
  acts/*.js                 the acts and their beats, one file to an act: prologue, egypt, rome, home, nevada, limo
  checkpoints.js          the testers' saved games, one for each beat (section 6, "Testing: parts"): written by a script, not by hand
  sound.js                music, effects and the list of recorded lines
  maps.js                 the maps: each time's places and the ways between them, the marks they arrive on, a sketch of each (MAP-15)
  cutscenes/highway.js    the painted highway at dusk, and the parts of it that change
  cutscenes/intro.js      the intro movie
  cutscenes/title.js      what is behind the title screen
  cutscenes/backup.js     the cut-scene "Backup", on the Nevada roadside: it closes Act Four and hands the game to Act Five
  scenes/index.js         the list of scenes, act by act (since round thirteen Act One has five, the inside of the wagon among them, and Act Two six)
  scenes/*.js             one file per scene, all fetched while the start-up panel shows
  scenes/engine-proof.js    the worked example of a painted scene: the pattern to copy
  scenes/sketch-example.js  a scene with no painting yet, to show storyboarding
art/scenes/<scene id>/  a scene's pictures: back.png, its cut-outs, and layout.json (the painter's measurements); the
                        frames and sidecar of anyone painted frame by frame who belongs there (Ranger's, in nevada-roadside/);
                        and the frames of its birds (the pigeons on the steps, the geese on the Capitol, the hens across the Tiber)
art/scenes/highway/     the pictures of the intro and the title
art/items/              the pictures of things that can be carried
art/portraits/          the painted portraits of the painted people (Ranger, with and without his mirror shades): never keyed
art/proof/              the engine's own pictures for its proof scene: a small painted creature, a strip of country, a window, and
                        since round thirteen a flock of geese (their frames) with their pen, a boat, and a house front with a room
                        behind its upper window; since round sixteen, in art/proof/drive/, the world outside a car's side windows
                        for the `drive` (a car's side, a sky, two grounds of squares and stripes, ranges of plain triangles,
                        posts, poles and a marker: tools/paint/proof_drive.py) <!-- DRIVE-16E -->
art/emblem/             the game's emblem, the Timer (EMBLEM-13): the begin screen's sky, turning bow, top and still, and the
                        tab and home-screen icons: interface pictures, never keyed; since round fifteen the same three pieces at
                        1024, for the large dial of the switch across the centuries (MAP-15D)
art/maps/<map>/         a map's pictures (MAP-15): the sheet, a picture for each place and each way, and layout.json (the
                        painters' measurements, which the engine reads): interface pictures, never keyed
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
  one switch (see section 5). <!-- MAP-15D --> The one exception is the map screen, which
  pauses the game while it is up, as the menu does: its dials, the portraits walking on it
  and its fades run on a small timer of its own (section 8, "The map, and the Timer").
- **Scenery is a painted picture, shown as it is.** The backdrop is the picture file
  itself, in a picture element. Nothing that happens afterwards touches it.
- **People, painted cut-outs and props share one canvas above the scenery.** On a frame
  where nothing on it has changed, nothing is painted. When something has (a step, a
  blink, a lid that opens), only the patch it touched is wiped and painted again. (A patch
  that touches a picture shown at another size than it was drawn, somebody walking, is
  grown to hold all of that picture: painted through a clip that cuts it, the browser can
  take its pixels a column differently, and the patch would no longer match the rest of
  him. Round thirteen, `Cast.update`.) Sections 3 and 4 explain how those pictures are
  made and put in order.
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
speed or less (no bird flaps up: they walk off instead). <!-- MAP-15D --> On the map
nothing moves: the dials show their notch at once, and a portrait is where it is going.

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
| `birds`, a flock | Birds on the ground (`area`) or along a ledge (`perch`) that stand, look about, peck, walk a few steps and turn; go up when somebody comes near and land again a little way off, the ones beside them going too; with nowhere clear to land, fly off and come back later. A script can send the flock running to another place on the ground (`herd`), and give every bird one pose at once (`pose`): "A flock that is sent somewhere", below <!-- ROME-13E --> | `area` (or `poly`, `rect`) or `perch`; `count` (5); `frames` (below), or birds drawn by the engine: `look` (`pigeon`, `dove`, `sparrow`) and `size` (26 px long where a person is 160 tall); `depth` (smaller farther off: on an area); `moves` (`{ stand: 2, look: 2, peck: 4, walk: 3, turn: 1, away: 0 }`; `away`: one flies off by itself and comes back); `shy` (150 px at full size, about a metre and a half; half that from someone standing still; 0: never startled); `fly`, `turn` (false: never); `back` (`[8, 20]` s away); `treads` (`[y, ...]`) or `tread` (px): birds on steps keep to the treads and hop from one to the next; `walk` (12), `flight` (95) |
| `sway` | A cut-out of the scene (washing on a line, a banner, a palm's crown) stirring in the air from a fixed edge, with a ripple running along it | `plane` (the cut-out's id); `anchor` (`"top"`: it hangs; `"bottom"`: it is rooted; `"left"`, `"right"`: it flies from a pole at that side; or a line); `at` (the foot row, the pin row or the pole's column); `amount` (2.5 px at the far edge); `period` (3.4 s); `wave`; `lean` (0.3 of the amount, with the wind) |
| `bob` | A cut-out of the scene (a boat, a barge at its mooring) riding the water: it rises and falls on the swell, as two slow waves added together so that it never ticks like a clock, and with a `tilt` it rocks as well, about the middle of its base line. It is drawn on whole pixels from its own picture (a turned copy for each quarter of a degree it rocks, made once and kept), only its place changing, a few times a second at most; its base (who is in front of it and who behind), its clickable area, its `solid` ground and anything a script does to it are as they were. One that also sways does both: it rises and falls as it stirs, without rocking. For less motion half the amount (a bob of one pixel is then still) at half the pace <!-- ROME-13E --> | `plane` (the cut-out's id); `amount` (1 px up and down); `period` (5 s); `tilt` (0 degrees: none) |
| `strip` | The country going by the windows of a car on the move: one long painting, painted to run on from its right edge into its left, scrolling past behind the windows and drawn only inside them, with hard edges, over the backdrop. In the proof the car is a cut-out with its windows cut clear, laid over it; in the limousine (`nevada-limo`) the windows are the backdrop's own, and two strips went by, outward on each side, until round sixteen: two drives now (below) <!-- DRIVE-16M --> | `src` (the picture, in the scene's folder unless its name begins `art/`); `windows` (the glass of each window, the shapes it shows through; or `clip`; with neither, the whole width of the stage); `row` (the row of the stage its bottom edge is on: needed); `speed` (0 px a second; more than 0, the world goes by to the left, as from a car driving right; `set({ speed })` from a script, and it goes on from where it is); `loop` (true: drawn twice where the seam is in a window; false: it goes by once); `offset` (0: the column of the picture at the stage's left edge when it begins); `fps` (20) |
| `drive` | The world outside a car's side windows as a pinhole camera that is moving forward sees it, drawn from the scene's own camera: the ground in perspective, panoramas standing at their distances, upright things beside the road growing and sweeping past, wires; each side of the road its own place. See "The world going by a car's side windows", below <!-- DRIVE-16E --> And each thing's shadow laid on the ground in perspective, from the sun the scene gives <!-- DRIVE-16F --> | `side` (`"L"`, `"R"`); `windows` (or `clip`); `vanish`, `focal`, `eye` (1.6 m); `speed` (0 m a second; `set({ speed })`); `start` (0 m); `sky`; `bands` (`[{ src, distance, ppm }]`); `ground` (`{ src, from, ppm }`); `things` (`{ src, rows }`); `haze` (`#d9dde6`), `haze_far` (4000 m); `streak` (0.6); `slices` (2); `wire` (`#2f2a26`); `phase` (0 on the left, 0.5 on the right); `fps` (30); `sun` (`[forward, left]`; none: no shadows), `shade` (`#6664ac`), `shade_k` (0.6) <!-- DRIVE-16F --> |
| `portal` | The door in time: a ripple in the paint. See "The door in time", below | `at` (its middle, wide open); `r` (half its height, wide open); `wide` (1: a round hole; the chamber's doorway 0.48); `keep` (the bare wall it is in, `[x0, x1]`); `rise`; `under`; `light`; `open` (0); `strength` (0.45); `bend` (0.6); `rate` (1.5); `size` (1.11); `pale` |

Every kind also takes: `id` (its name, for scripts and tests; on the stage it is `fx:<id>`); `base` or `plane`, its
depth among the people exactly as for a cut-out (section 3: a row, a line, `"front"`, `"back"`); `when` (on the stage
only while the story says so, read again whenever the story changes); `scale` (every size and speed of it, times this);
`opacity`, `color`; `clip` (a shape it is kept inside: rings that must not run onto the sand); `behind` (shapes where it
passes behind something painted nearer, and is not drawn, or only at `behindOpacity`: smoke rising behind a pyramid);
`seed`. A smoke, a flame, embers or a stream sits by default at the row of its own point, so give the `base` of the thing
it belongs to (an altar's smoke has the altar's base: a man behind the altar is behind its smoke); water on the ground,
birds in the sky and a strip lie behind everybody; birds on the ground sort by their own feet, each one, like people. A sway is
its cut-out: the cut-out keeps its depth, its states and everything a script does to it.

**Painted frames for birds.** One picture a frame, clear background, every frame of a bird on the same size of canvas
with its feet at the same point: `frames: { foot: [x, y], face: "E", sizeAt: 590, stand: [...], look: [...], peck:
[...], walk: [...], turn: [...], takeoff: [...], fly: [...], glide: [...], land: [...], run: [...], flap: [...], shadow: "..." }`.
Only `stand` is needed; a missing list falls back sensibly (no `walk`: the bird hops; no `fly`: it never flies; no `run`, for
a flock that is herded: it runs on its `walk` frames; no `flap`, wings up where it stands: its `look`). <!-- ROME-13E: run, flap --> The engine turns
the frames round for a bird facing the other way (not the `shadow`, which lies under a bird on the ground and goes when
it takes off: the sun does not move). `sizeAt` is the row at which they are the right size: they grow and shrink from
there with the depth, as people do (`scale: "depth"` means the row `full`); without it they are drawn as painted, times
`scale`. File names are in the scene's own folder unless `dir` says otherwise; with `set: "pigeon-dark"`, a number `n`
stands for `pigeon-dark-n.png`. The frames are fetched with the scene's other pictures (ahead of time, and in the
quiet fetching behind the title), and a scene does not show until they are here.

<!-- ROME-13E -->
**A flock that is sent somewhere.** A script can herd a flock into another place on the ground, as the boy's stomp sends
the Capitol's geese into their pen: `await g.effects.get("geese").herd(PEN, { from: [x, y], via: [x, y] })`. `PEN` (a
shape on the ground: a poly, a rect or a circle) is the flock's area from then on, where the birds stand, look, peck and
walk as they did in the old one, with their own `shy`, `fly`, `turn` and `moves`. Each bird is given a place of its own
in it, the places spread out (no two nearer than about a bird's length, where there is room). The bird nearest `from`
(where the boy stomped) sets off first, each of the others a tenth of a second after the one before: it flaps where it
stands, facing the way it will run (its `flap` frames, a third of a second), then runs to its place on its `run` frames,
twelve a second, by `via` first if one is given (a point, or a list of points: the gap in the pen's fence, so that nobody
runs through the fence), at `pace` pixels a second at full size (110: a man is 160 tall there), smaller and slower farther
off, as a person walks. The first to set off goes deepest in, and a running bird faces the way it runs, whatever its
`turn`. Nothing startles a bird that is being herded, and one that is up and away is simply put at its place. The promise
resolves when the last of them is there: at once, every bird at its place, while a cut-scene is being skipped and when the
flock is not on the stage (`?nofx`, its `when` false). For less motion they do not flap, and walk there briskly (their
`walk` frames, at twice the flock's `walk`: a goose's waddle is about 30). Like a startled flock, a herded one is not worked
out from its time alone: where the birds end up depends on when and from where they were sent.
`pose(name, seconds)` gives every bird on the ground one pose at once, for about that long (each a little more or less),
and then they carry on as they were, from where they were: `pose("look", 1.2)` is the geese stretching their necks out low
and hissing at whoever moved. It resolves when they have all carried on, and at once while skipping or off the stage. With
no frames for it, `flap` shows `look`, and any other name `stand`. A flock on a perch cannot be herded: the console says so,
once, and the promise resolves.

Nothing of a herd is saved. A scene whose flock has been sent somewhere gives the flock its place from a fact as the scene
is built: its `fx` is then a function of the game, `fx: (g) => [ ..., { id: "geese", type: "birds", area: g.flag("rome.geeseGone")
? PEN : BASE, ... } ]`. The engine asks the function as the scene is entered; to fetch the scene's pictures ahead it asks it
again of a stand-in that knows nothing yet (every fact false, nothing carried), and if that throws it fetches nothing ahead
(the scene still waits for its frames as it is entered). `seek(ms)` after a herd shows the birds in their new area. The
proof: `index.html?scene=engine-proof&lead=dad&flags=proof.herd`, six geese of the engine's own round a spot on the sand,
and a little pen with a gap in its front: shoo them, and Dad stomps, and they are herded through the gap (the fact
`proof.herded`: entered again, they are in the pen at once); ask them nicely into the pen, and they hiss. The engine test's
`herd` part plays all of it.

**On the game clock.** Each moving thing keeps its own time, which goes on with the game clock: at its speed, and not
at all while the game is paused. What it shows at a moment is worked out from its seed and that time alone (the puffs
of a smoke, the glints on water, when the birds cross), so a scene opened twice looks the same at the same moment of its
time. The only exception is a flock that somebody has startled, since what it does then depends on where people walked.
For less motion, each one's time runs at half speed or less, it changes its picture less often, flames flicker less,
flyers glide, and a flock never flies: a startled bird walks off instead.

**Cheap.** Each kind changes its picture only as often as its motion needs: a bird thirty times a second, smoke, rings,
a stream and a strip twenty, a flame fifteen, embers ten, a sway six, light on water five. In any one frame only four of them
may change (`game.effects.budget`): the ones that have waited longest go first, and a bird on the move before them all,
so the others wait a frame or two, which nobody sees. The cast then repaints a few small patches, never the whole layer
(it does that when more than six things change at once: `Cast.update`). Each picture is cut to the box the thing can
reach; a group of birds crossing together is one picture. A swaying cut-out is repainted whole each time it moves, so
keep sways to the things that need them. The engine's own scene, with twelve moving things (two of them big sways) and
some 120 puffs, glints, coals and birds on the stage, has the cast layer repaint about 3 million pixels a second, all in
patches (with none of them, 0.2 million). Measured as in section 1 ("What a frame costs"), with the processor slowed four
times over: a frame's main-thread work while the lead walks across it goes from 3.5 to 6.2 ms, and while he stands from
0.8 to 6.0 ms, every frame still on time. A scene with a few moving things costs a fraction of that. A strip is a
picture for each window, cut to the window's box, drawn again only when it has gone by a whole pixel (a parked one costs
nothing): the proof's two windows, 79 by 45 pixels each, going by at 40 pixels a second, are some 140,000 pixels a
second, at 0.04 ms a picture; slowed four times over, a frame of the proof scene goes from 1.6 to 3.1 ms while the lead
stands, and from 3.3 to about 4 ms while he walks. A drive works every pixel of its panes out afresh, thirty times a second
while it moves: the limousine's four panes are about 7 ms a moment (<!-- DRIVE-16M --> with the painter's pictures), one side's on a frame and the other's on the next (its
own section, below <!-- DRIVE-16F: it is below again, moved after these paragraphs -->). <!-- DRIVE-16E -->

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
`index.html?scene=engine-proof&lead=dad&flags=proof.fx`; and a strip, behind the two windows of a cut-out laid over the
sand, with `flags=proof.strip` (`g.effects.get("desert").set({ speed: 0 })` parks it). A boat riding the water by the bank
is `flags=proof.bob` (the papyrus in the corner is cleared away while it is there), and a flock herded into a pen
`flags=proof.herd`. <!-- ROME-13E --> The world going by a car's side windows is `flags=proof.drive`
(`g.effects.get("drive-l").set({ speed: 0 })` parks one side). <!-- DRIVE-16E -->

<!-- DRIVE-16E --> <!-- DRIVE-16F: this section moved here, after the paragraphs about every moving thing ("On the game clock" to "Trying marks out"), which had come after it -->
### The world going by a car's side windows

The author, 15 October, of the limousine's windows: "the outside needs to go past not look like mirrors". A strip
(above) is one flat painting pulled past the glass: drawn behind both sides' windows at one speed, the same picture on
both sides, it moved apart from the middle like a mirror, and nothing had depth. Seen from a seat in the back of a car
driving into the picture, the world outside the side windows comes toward us: everything comes out of the far end of the
windows small and slow, near the vanishing point, and grows and speeds up as it comes nearer, sweeping out past the near
edge of the near pane; the mountains hardly move, the desert in the middle distance drifts, the ground and the posts
beside the road rush by; lines along the road (a fence, the road's edge, wires) run to the vanishing point; and the two
sides are different places. That is one thing, the view through a pinhole camera that is moving forward, and `drive`
draws it that way: a small renderer, run from the scene's own camera, of a world the painter paints.

**The camera** is the scene's, level: `vanish` is the point the line of travel runs to (its row is the horizon), `focal`
its focal length in pixels, `eye` how high the eye is above the road in metres (the limousine's: `[424, 220]`, 345 and
1.83, its floor taken as 35 cm above the road). A point X metres out to the side of the line of travel, z metres ahead and
Y metres up is on the stage at `x = vanish x - focal * X / z` (on the left; `+` on the right) and `y = vanish y + focal *
(eye - Y) / z`, and as the car goes s metres forward every z is s smaller. Each pane (as a strip's windows: a picture of
its own, cut to its shape with hard edges, a pixel in it when its middle is) is drawn far to near:

- **the sky**, a picture the stage's size, as it is (still), wherever the pane shows sky;
- **the ground** beside the road, seen from straight above: each pixel below the horizon shows the patch of ground it
  sees (`z = focal * eye / (y - horizon)`, `X = |x - vanish x| * z / focal`), read from the ground's picture at
  `(z + s) * ppm` along the road (looping end to end) and `(X - from) * ppm` across it; beyond its last row, the colour of
  its last rows; fading into the haze with distance (`haze`, half covered at `haze_far` metres);
- **the bands**, panoramas seen from the side, far to near, each a wall `distance` metres out: the stage's column at `u =
  |x - vanish x|` looks at it `z = focal * distance / u` ahead and shows its column `(z + s) * ppm` (looping), standing on
  its foot (`y = horizon + eye * u / distance`) at `u / (distance * ppm)` of its own size. A band hides the ground beyond
  it; the ground nearer than it lies below its foot, and none of it is drawn over;
- **the things**, upright beside the road (posts, poles, bushes, a sign), far to near, each at its place and its size
  there, from a sheet of pictures painted from the side; and wires from each to the next of its row, one pixel, dark
  (`wire`), fainter far off, sagging in the middle. A thing nearer than 1.5 m ahead, or smaller than a pixel, is not drawn.
  Given a `sun`, every thing's shadow is laid on the ground first, and the things stand on their shadows ("The things'
  shadows", below). <!-- DRIVE-16F -->

**No shimmer.** A picture drawn smaller than its own size is never one pixel picked from many. The ground's pictures and
the bands' are summed once, as they arrive (sums of their pixels along the road, from which the average of any stretch is
a few steps), and each pixel of a pane is the average of the very patch of the picture it sees: for a band, the stretch its
column looks at and the rows its pixel covers; for the ground, the slanting strip between the lines of sight at the pixel's
edges (the farther along the road, the farther across it), taken in up to `slices` slices along the road, each averaged
over its stretch and then across over the stretch its pixel sees there. Each is a copy of the picture made smaller for that
pixel alone, averaged. A thing drawn smaller than its own size is drawn from a copy of itself halved, and halved again (each
pixel the average of four, made once). Drawn larger, a picture's pixels stay hard, as the game's are (a pixel that straddles
two of them takes a share of each). **Speed reads as speed**: a row of ground that goes by faster than it is long (its
picture's travel, times `streak`, more than its own patch) is averaged along the road over that much, so the near ground
streaks along its motion; a slower row is drawn as it would be parked; for less motion, nothing streaks.

**Its time** is the strip's: where it is (s, metres gone) is worked out from its time alone and the speeds since each
`set()`, so a scene opened twice shows the same picture at the same moment. `speed` is metres a second, read and set by a
script (`g.effects.get("desert-l").set({ speed: 0 })`: it goes on from where it is; tweened, the car slows to a stop, as the
limousine's ending does), and a parked drive draws nothing new. For less motion its time runs at half speed, and nothing
streaks. Each pane's picture is drawn again thirty times a second while it moves (`fps`), the right side's half way between
the left side's (`phase`), so that a frame of the game draws one side's panes and the next frame the other's.

<!-- DRIVE-16M: the limousine's right side as merged (js/content/scenes/nevada-limo.js; the left side is its own, beside it) -->
```js
{ id: "desert-r", type: "drive", side: "R",              // "L" or "R": the side of the line of travel its world is on
  windows: [ ...the side's panes, as polys... ],          // where it is seen, as a strip's windows (layout.json `windows`)
  vanish: [424, 220], focal: 345, eye: 1.83,              // the camera (the scene's)
  speed: 16,                                              // metres a second (a calm 36 mph: a post can be seen going by)
  sky: "drive-sky.png",                                   // the sky, drawn still: the stage's size
  bands: [                                                // far to near, each looping along the road
    { src: "drive-far-r.png", distance: 3000, ppm: 0.14 },        // `distance` metres out; `ppm` its pixels a metre
    { src: "drive-mid-r.png", distance: 850, ppm: 0.5 } ],
  ground: { src: "drive-ground-r.png", from: 6, ppm: 16 },        // columns along the road (looping), rows outward from `from` m
  things: { src: "drive-things.png", rows: [                      // its sheet's JSON beside it (drive-things.json), or `sheet`
    { sprite: ["post-r", "post-r", "tpost-r"], every: 4.6, at: 9.5, wires: [1.25, 0.95, 0.65] },  // the fence: a list to pick from
    { sprite: "pole-r", every: 55, at: 70, wires: [8.6, 8.1] },   // one every 55 m, 70 m out, wired pole to pole at those heights
    { sprite: "sign-range-r", every: [600, 1300], at: [7, 8] },   // [min, max]: placed from the seed
    { sprite: ["sage-1-r", "sage-2-r", "sage-3-r", "sage-2-r", "rabbitbrush-r", "creosote-r"], every: [3, 16], at: [10.4, 24] },
    { sprite: ["sage-1-r", "sage-2-r", "sage-3-r", "creosote-r"], every: [3, 14], at: [24, 70] },
    { sprite: ["joshua-r", "joshua-2-r"], every: [80, 240], at: [17, 90] },
    { sprite: "rock-r", every: [60, 180], at: [11, 45] },
    { sprite: "sign-services-r", every: 9000, at: 7.4, offset: 300 } ] },   // one, about 18 s in: `offset` puts it there
  haze: "#b6bee0", haze_far: 3000, wire: "#2c2a32",       // the air's colour and the wires' (through the scene's key); half hazed at 3 km
  sun: [0.36, 1.95], shade: "#6664ac", shade_k: 0.62,     // DRIVE-16F: the things' shadows: a metre of height throws one 0.36 m ahead
                                                          //   and 1.95 m to the car's left; the ground under it multiplied by `shade`
  seed: 7,
}
```

**The pictures** (in the scene's folder unless a name begins `art/`; 8-bit, keyed as the scene's frames): the sky, the
stage's size (only its rows down to the horizon and a little below are seen); each band wide and short, clear above its
ridges, its bottom row the ground at its foot, looping end to end, in the haze of its distance (a far one pale and blue);
the ground, 1024 x 512 at 16 pixels a metre (64 m of road, looping; 32 m outward from `from`), a map seen from straight
above with nothing standing up in it; and the sheet of things, each painted from the side at 24 pixels a metre in its box,
its foot on the ground at the middle of its bottom row, with its JSON: `{ "ppm": 24, "sprites": { "<name>": { "box": [x,
y, w, h], "foot": [fx, fy], "height": <metres> } } }` (`foot` in the box, or on the sheet: whichever lies in the box).
<!-- DRIVE-16F --> A sheet of things is painted **without shadows**, each box only as wide as the thing itself: the shadows
are the engine's (below).

**The things' rows.** Each row is placed from the seed, the same every time: a thing in each cell of `every` metres along
the road (with `[min, max]`, each moved by up to a quarter of the range either way, so that from one to the next is within
it), `at` metres out (or anywhere in `[min, max]`), its picture `sprite` (or one picked from a list); `offset` is where the
first stands (from the seed if not given). The road never repeats unless a row says `loop` (metres): to keep upright posts
on footings painted in the ground, give it the ground's length (64 m) and an `every` that divides it. `wires` are heights
in metres, from each thing to the next, sagging `sag` metres in the middle (1.5% of the span).

<!-- DRIVE-16F -->
**The things' shadows** are the engine's. A shadow painted along the bottom rows of a thing's picture stands up with the
picture: near the car it was a brown bar in the air beside each post, and was left alone in the pane once its post had gone
(decision 92). So a sheet of things has none, and with `sun: [forward, left]` (metres of shadow for a metre of a thing's
height, ahead along the line of travel and to the car's left; the car's left is outward on the left side and toward the road
on the right) the engine lays every thing's shadow on the ground, all of them before any thing, the things then far to
near over them. A shadow runs from the thing's foot along the sun, as long as the light makes it, and is as wide at each
point as the thing is at the height that throws it: the solid pixels of each row of its picture counted, so a post's or a
pole's is a thin band (with the crossarm across it near its end), a bush's a rounded blob narrowing toward its tip, an open
bush's thinner than its span, a sign's its posts and then its board. Its middle line is worked out on the ground in metres
and put on the stage with the camera, as the ground is, and its width by the camera's rates of change there. A pane's
shadows are one shape (where two overlap, the ground is shaded once), laid over the ground multiplied by `shade` (through
the scene's key) at `shade_k`, its edges a pixel soft as any filled shape's, and cut to the pane with everything else. The
ground is seen very aslant from a car's seat: a fence post's shadow 10 m away is about half a pixel thick, and as a shade
spread over two rows of the streaking ground it could not be seen. So no shadow is drawn thinner, across the way it runs,
than 10 cm would be seen face on at its distance, up to a pixel and a half: near the car (within some 23 m in the
limousine) a pixel and a half at least, as a wire is never thinner than a pixel; farther off less, as the things themselves
grow smaller, so that a far telephone pole's long shadow is a faint line. A thing gone out past the edge of a pane takes its shadow
with it, unless the shadow itself still lies in the pane, on the ground. A drive without `sun` draws no shadows. The
limousine's two sides have the painter's sun, `[0.36, 1.95]` (low on the car's right and a little behind:
`tools/paint/nevada_limo_drive_kit.py`), so the shadows run out across the desert on the left and in toward the road on the
right; `shade` is the painter's colour for a morning shadow on the sand (`#6664ac`, the roadside's and the ground pictures'),
at the roadside's strength for its standing things' shadows (0.62).

**What a side window sees.** The panes look out between about 20 and 50 degrees from straight ahead. In the limousine the
nearest ground any pane shows is about 7.4 m out on the left and 6.8 m on the right (the bottom edge of a pane is a line
along the road), and the top of the glass, 18 cm above the eye, sees no higher than `1.83 + 0.107 * X` metres at X out (on
the right; `0.099` on the left): a pole 14 m out shows only its lowest 3.3 m going by, and wires 8.6 m up are in view only
from about 63 m out.

<!-- DRIVE-16M -->
**In the limousine** each side is its own country, painted for it (PAINT-16, `tools/paint/nevada_limo_drive.py`; every
upright thing twice, `-l` and `-r`, lit for its side: the sun low on the car's right and a little behind, as the roadside's
light). On the left, across the oncoming lane (its white edge line 8 m out rushing by along the bottom of the panes, then
its gravel shoulder), the open desert runs to the long ranges across the valley (6000 m out, at 0.07 pixels a metre), with
a ranch in the middle distance (850 m out: it comes into the far pane about half a minute in and leaves the near pane at
about two and a half minutes); beside the road, white reflector posts every 38 to 70 m, a mile marker every mile, the backs
of the oncoming lane's signs every 600 to 1300 m, brush, rocks and now and then a Joshua tree. On the right, straight onto
the desert: a wire fence 9.5 m out, its posts rushing past below the eye (about three a second), the telephone line 70 m
out with its poles and sagging wires along the top of the panes (nearer, the glass would show only their feet), low hills
3000 m out (painted at 0.14 pixels a metre, so that they are never drawn larger than painted) and, in the middle distance,
buttes and a far line of power poles; an OPEN RANGE sign every 600 to 1300 m, one NEXT SERVICES sign about 18 seconds in,
brush, rocks and Joshua trees. So something goes by in each near pane every few seconds (on the left a reflector post every
three or four, the brush between; on the right the fence all the time), and a sign about every half minute on one side or
the other. `start` and `streak` are the engine's (0 and 0.6). The pictures come to some 770 KB, the limousine's folder to
1.4 MB (section 14).

**Cost.** Each picture's sums are made once a session, while the scene is being entered (the limousine's, some 21 MB
for its two grounds, four bands and sky, in about 90 to 140 ms for the left side and 30 to 90 for the right, which shares
the sky and the sheet). On the test machine a moment's four panes in the limousine (some 51,000 pixels) take about 6.5 to
8 ms, at most about 4 ms in any one frame; with the processor slowed four times over, 11 to 15 ms for a side's panes.
(Measured with the painter's pictures, at the merge; the engine's stand-ins had taken about 60 and 30 ms, and 6 ms.)
<!-- DRIVE-16M --> `cost` on a drive keeps what its pictures took. <!-- DRIVE-16F --> The things' shadows add about 0.3 ms to
a moment's four panes (their outlines and the fill); the engine test's whole quick run measured the limousine at 6 to 7 ms
a moment with them, and 11 to 16 ms for a side's panes slowed four times over (that last varies from run to run).

**The proof**: `index.html?scene=engine-proof&lead=dad&flags=proof.drive`. A car's side of the engine's own seen from the
back seat (`art/proof/drive/car.png`, a cut-out behind everybody: a grey band with a window cut clear on each side of the
vanishing point, a small cross on the vanishing point between them; the palms and the papyrus are cleared away while it is
there) and, through its windows, two drives from the proof's camera (`[400, 226]`, 320, 1.6 m) and its own plain pictures
(tools/paint/proof_drive.py): grounds of two-metre squares with stripes along the road 6, 10, 16 and 24 m out (they run to
the cross) and bands across it every 16 m, ranges of plain triangles 3000 and 400 m out (the far ones hardly move, the near
ones drift), red posts with wires and brown poles on the left, a magenta marker and a yellow board on the right, each on
its shadow (the limousine's sun: out across the ground on the left, in toward the road on the right). <!-- DRIVE-16F --> The engine
test's part `drive` reads the geometry back from the pixels.

### The door in time

The author, 9 October: "Rather than a solid object or rays let's see if we can make it look like a ripple or distortion
of the paint. The time portal really needs to look good." A design study showed six such looks live on the real
backdrops (pond rings, a slow vortex, wet paint flowing, a glass lens, heat haze, the paint thinning to light), and he
chose **pond rings**, with the settings that are now the kind's defaults. So since round ten a door in time is not a
drawn thing laid over the painting (the neon rings still rush past in the time tunnel, and `kit.portal` still draws
them, though no scene uses it now; since EMBLEM-13 the game's mark, on the gate and in the browser tab, is the Timer
emblem of section 9): it
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
<!-- MAP-15D --> Nor are the maps (since round fifteen): four sheets painted by the same passes with the same kit, each
the kind of map its own time would make, their colours mixed from the box by name (section 9, "The maps").

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

Only two things that overlap on the screen are compared, because only they can cover each
other: a person and a cut-out by the side of its base line the person's feet are on, two
people by their feet, two cut-outs by their bases where their pictures overlap. The cast is
painted in an order that keeps every one of those answers (`Cast.sorted` in
`js/engine/cast.js`). This matters once a base slants. With the Son behind a fence near its
near end and Dad in front of it at its far end, higher up the picture, Dad is also behind
the Son by their feet, and the three answers go round in a circle: a plain sort had to
break one, and could paint the Son over the fence. But Dad and the Son do not overlap, so
they are never compared, and nothing goes round. Overlap is judged by the boxes the pictures
fill; where answers still go round, the engine looks closer and lets go of any pair whose
paint does not in fact meet. A true circle needs three things whose paint all overlaps, such
as two people who overlap on either side of a steep base line; then the one that breaks the
fewest answers goes out of turn, the same one on every frame. With no slanted base on the
floor this is the plain sort it always was, and thirty things with slanted bases take about
twenty microseconds a frame. (`SORT-13`)

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

<!-- ROME-13E -->
**Someone above the floor.** A person at an upper window, on a roof or on a balcony stands on a floor that is not the
scene's ground, so the row his feet are on does not say how big he is. He is one of the scene's people with a `scale` of
his own, standing behind a cut-out of the wall he is in, its opening cut clear (the painter paints what is behind him, a
dark room, into the backdrop):

```js
{ id: "watcher", kind: "dateseller", at: [373, 307], scale: 0.5, face: "W", solid: false, life: { fidget: false }, when: (g) => !g.flag("x.down") },
```

`at` is the point under his feet on that floor: above the wall's base, so he is drawn behind the wall and shows only
through the opening. `scale` is the size of a man standing there; a man a step back from a window is a little smaller than
one at the foot of its wall, and the painter measures it, with the sill at his waist. `solid: false`, since his feet are
on no ground of ours. His area is the opening, with `actor` naming him (`{ id: "atwindow", actor: "watcher", poly: OPENING,
... }`): a click on the wall below the sill is a click on the wall (list the wall's own area before his: where two areas
overlap, the one listed later is on top), and Show outlines his own figure inside the opening, grown by four pixels, and
nowhere else. His words go over his head as anyone's do, at his scale. Nothing turns him while he prays: the engine turns
only a companion toward the lead, his life is still, and the life of the scene's people never moves anyone who is
praying. A save rebuilds him there. To bring him down, a script lets his prayer go, turns him from the window and fades
him out, puts him in his doorway at the size of that row (`scaleAt` in `js/engine/walk.js`), shows him, sets the fact,
and walks him to a spot of his. The scene has two entries under `actors` with the same id and opposite `when`s (at the
window, and on the ground), and two areas likewise, so that whenever it is built he is wherever the story says; only the
entry the story has now takes up any ground (until round thirteen the other one also claimed a patch at the feet of the
one on the stage: under the window, on the sand behind the house). The proof:
`index.html?scene=engine-proof&lead=dad&flags=proof.window`, a plastered house front with a man at its upper window,
praying; knock at his door and he comes down (`proof.windowDown`). The engine test's `window` part checks all of it.

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
| Sitting | Cross-legged on the ground, or on a seat: a chair, a bench, a stool, a step. Someone who is found sitting breathes, blinks and talks sitting down, with the same gestures of their own that they would use standing. Someone found sitting up high, their feet clear of the floor (Titus, on a statue's base on the Capitol), gets down with a hop, landing a step in front of the seat, and anything they carry is clutched to their chest on the way. |

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

**Painted frame by frame: an animal.** The rig draws people, and an animal is not one. Ranger, the raccoon who is a lead
in Act Five, is painted frame by frame, as the birds and the donkey are, and to the engine he is a person in every other
way: he walks, is clicked on, has words over his head (his "..."), a life of his own, a place, pockets and a portrait,
and the player can switch to him. `js/art/painted.js` lists the kinds that are painted and where each one's sidecar is;
`cast.addFigure` makes a `PaintedFigure` (in `cast.js`) for those and a `Figure` for everyone else, so a scene puts him
in its `actors` or its `party`, and a script on the team (`g.team`), like anyone. His pictures are one picture a frame, on a clear background,
every frame on one canvas with his feet at one point and every frame facing east, in the folder of the scene he belongs
to, painted at the size he shows where a person is 160 pixels tall. The sidecar beside them says what is there:

```
art/scenes/nevada-roadside/ranger.json
{ "id": "ranger", "face": "E", "foot": [68, 56], "tall": { "stand": 34, "sit": 49 }, "stride": { "walk": 32, "run": 70 }, "pace": 100,
  "frames": { "stand": [...], "sit": [...], "walk": [...], "run": [...], "nibble": [...], "wash": [...], "reach": [...], "look": [...],
              "walkN": [...], "walkS": [...] },
  "fps": { "stand": 1.5, "sit": 1.5, "walk": 8, "run": 10, "nibble": 6, "wash": 5, "reach": 2, "look": 1, "walkN": 8, "walkS": 8 },
  "fidgets": ["look", "wash"], "portrait": "art/portraits/ranger-face.png",
  "variants": { "shades": { "prefix": "ranger-shades-", "portrait": "art/portraits/ranger-shades-face.png" } } }
```

| Field | What it is |
| --- | --- |
| `foot` | The point on the ground under him, in every frame's pixels |
| `tall` | Ground to the top of his head at full size, on all fours (`stand`) and sitting up (`sit`), for his words. A set may have a height of its own (`"nibble": 44`); without one, the sets drawn sitting up (`sit`, `nibble`, `wash`, `reach`, `look`, and any the sidecar lists in `sitUp`) take `sit`, and the rest `stand`. One number does for both. |
| `stride`, `pace` | The ground one walk cycle covers at full size (or `{ "walk": 44, "run": 96 }`: a scamper covers twice a walk's if not said), and how fast he walks, in pixels a second at full size (120). His walk goes by the ground covered, as a person's does, so his feet do not slide. |
| `frames` | The sets, each a list of files, in the sidecar's folder unless a name begins `art/`. Only `stand` is needed: a set that is not there is shown by another (`walk` and `sit` by `stand`, `run` by `walk`, the sets drawn sitting up by `sit`). `walkN` and `walkS` (from behind and from the front), if painted, are his walk to the north and to the south. |
| `fps` | Pictures a second for each set when it is not a walk: `stand` and `sit` 1.5, `run` 10, any other 4 if not said |
| `fidgets` | The sets that are his small movements, for his life (`look` and `wash` if not said) |
| `portrait` | His face, 64 by 64, for the team bar and for words through a door: drawn as it is (never keyed), with hard pixels at a whole multiple of its size where that nearly fills the square, and at the size asked where it does not |
| `variants` | Him in another state, every set and the face: `prefix` stands in for the frames' own (the id and a hyphen, or the sidecar's `prefix`) in every file name, and `portrait` is the face in that state; `frames` can give a set pictures of its own. `figure.variant("shades")` puts it on and `variant(null)` takes it off. It is not saved: the scene puts it on from a fact, in `setup` and at the moment it happens. |
| `sitMs` | How long sitting up or settling back takes (300 ms) |

What he cannot do, having no joints: gesture (while he talks his `stand` or `sit` pictures go on as they were), move his
mouth, pray or shade his eyes (asked to, nothing happens and nothing breaks), or be seen from eight ways. He is painted
from two: east is the frames, west their mirror, and the other six ways are the nearer of the two (facing straight
toward us or away he stays the way round he was, and walks with `walkN` and `walkS` if they are painted). Nor has he a
stance or a walk of his own from a page of settings: whatever he does is a set that was painted. He is sized by the
depth as a person is, from the size he was painted at: with hard pixels, in steps of two, and never more than a quarter
bigger. A script plays a set by name: `await g.lead.play(g.clock, "nibble", { ms: 1800 })` runs for that long, or with
no `ms` until `stop()`; `g.reach()` is his `reach` out and back, `hold()` holds it out; a hurried walk is a scamper
(`run`).

The sidecars and the portraits are read as the game starts, so a portrait is there when the team bar first draws it;
the frames come with the pictures of the scene he is in, which does not show until they are here. A sidecar must be
among the page's files: once it is painted, run `tools/stamp.py`. Until then the engine does not ask for it (so the
browser reports no missing file), he is not drawn, and the console says why, once. `tools/sprites.html` shows him too,
from his sets. The proof: `index.html?scene=engine-proof&lead=dad&flags=proof.painted` has a small creature of the
engine's own (`art/proof/critter.json`) sitting up on the sand, living, looked at and talked to (Dad says what he
means), joining Dad as a team of two, put in his shades by a pair of sunglasses and nibbling at the cooler; the engine
test's `painted` part plays all of it.

### Who is in the cast

Thirty-eight people in the story, all in `js/art/people.js` (which also keeps two whom no scene uses now: `carrier`, the
water carrier of the first drafts, whose place by the river Lot has taken, and `oldtimer`, the old man of the Last Stop
in his lawn chair, whose place Grandpa Joe has taken):

| Where | Who |
| --- | --- |
| The family | `dad`, `son`, `mom`, `bigsis`, `lilsis` |
| Egypt | `lot` (Abram's nephew: sits cross-legged on the sand and prays), `scribe` (sits cross-legged on the ground), `overseer` (a staff in his right hand), `hauler1`, `hauler2`, `hauler3`, `mason1`, `mason2` (far up the pyramid's faces on the painter's hanging planks, drawn small, rubbing the stone now and then), `guard` (the tallest, a long staff upright), `lampboy` (sits on a bench; can stand and walk), `goldsmith` (sits on his stool) |
| Rome | `keeper`, `washer`, `urchin` (sits on the kerb), `soothsayer` (sits on a step, with a staff), `senator`, `doorkeeper`, `clerk` (sits at his table), `dateseller` (a basket of dates on his hip); and since round thirteen `gaul` (the Gaulish senator, in the Roman senator's toga, far too short), `phyllis` (on a low stool that is drawn with her, the lamp in her lap), `titus` (high on a statue's base, the breakfast in his lap: he gets down with a hop), `anser` (the goose-keeper: a basket of grain on his hip and a long stick), `eleazar` (on his bench with his scroll; he stands to pray, and lays his hand on the boy's head to bless him), `mariam` (a dish of grain on her hip), `felix` (a bale on his shoulder) |
| Nevada | `agent` (Jed, the man in gray), `grandpajoe` (in his rocking chair, which is drawn with him, the banjo across his knees), `jolene` (under her straw cowboy hat), `suit1`, `suit2`, `suit3`, `suit4` (the backup, with a clipboard, a tape measure, a juice box and a paper bag) |

Twenty-four more figures are the same people in another state: `goldsmith-shades` (the goldsmith
with the sunglasses on), `guard-shade` (the guard holding the windshield shade up, his
staff laid on the sand) and `lot-standing` (Lot on his feet, his staff in his hand); Grandpa
Joe holding up the sun shade (`grandpajoe-shade`), playing on his feet (`grandpajoe-play`),
standing with the banjo by its neck (`grandpajoe-standing`), with it raised over his head
(`grandpajoe-swing`), with what is left of it (`grandpajoe-broken`), tied (`grandpajoe-tied`),
carried (`grandpajoe-carried`), and on the limousine's seat in the ropes and the seatbelt, and
then loose (`grandpajoe-seat-tied`, `grandpajoe-seat-loose`); Jolene under her other four hats
(`jolene-2` to `jolene-5`); Jed in the dust with the banjo's hoop round his neck
(`agent-collar`); two of the backup carrying Grandpa Joe (`suit2-carry`, `suit3-carry`); and,
since round thirteen, the Gaul in his own toga, very large (`gaul-own`), Phyllis with the lamp
given and a half-made garland in her hands (`phyllis-free`), Titus on his feet with nothing in
his hands (`titus-free`), Eleazar at his upper window, his way of standing his prayer
(`eleazar-window`), and Felix with his bale set down (`felix-free`). A scene swaps one for the
other in place, under the same id, so the person keeps their name and the color of their words.

Grandma Jolene's five hens are not people: each is a cut-out of the store's painting, with a
picture for each thing she does (on guard, two ways; turning; sitting; pecking). Nor are the
birds of Rome: the soothsayer's chickens, the Capitol's geese and Mariam's five hens across the
Tiber are moving things of their scenes, painted frame by frame (section 2).

The painted ones are in `js/art/painted.js`, not in `people.js`: `ranger`, the raccoon (his frames are painted with the
Nevada roadside), and `critter`, the engine's own, for its proof scene.

### Making someone themselves

Colors and clothes say who a person is when they stand still. These settings in
`people.js` say it when they move, and they are worth as much care:

| Setting | What it is | In the cast |
| --- | --- | --- |
| `stance` | How they stand when nothing is happening: hands `"clasped"`, `"akimbo"`, `"behind"` the back, holding one `"elbow"`, arms `"folded"`, thumbs in their `"straps"`, a fist on a `"hip"`, something to `"carry"`, hands on a `"belly"`, or `"prayer"`: their way of standing is their prayer, and their small movements are made from it | Mom's hands are clasped. Little Sister's fists are on her hips. Big Sister holds one elbow. The man in gray keeps his hands where you cannot see them. Eleazar, at his upper window across the Tiber, stands at his prayer (round thirteen). |
| `walk` | How they move: length of stride, how far the arms swing and how bent they are, lean, how high the knees come, what the head does | The Son bounces with his fists pumping. Mom takes short steps and her arms hardly move. Little Sister stomps with straight arms. |
| `pace` | How fast they walk, in picture pixels a second at full size (155 unless it says otherwise) | The water carrier plods at 110. The street boy darts at 190. |
| `gestures` | What their hands do when they talk, as a short list of numbers | Dad nods, makes a point, shrugs, puts a hand on his hip. The Son throws both arms up. The clerk wipes his brow and counts on his fingers. |
| `hold` | An arm that is always busy with something; and holds a person has of their own, which a script names and keeps through whatever is said (`figure.hold(true, "bless")`) | The overseer's staff, the youngest hauler's loaf, the goose-keeper's stick; Eleazar's hand laid on the boy's head (`bless`) |
| `pray` | How they stand to pray: how high the folded hands are, how far the head bows, and whether the hands are clasped tight and the eyes squeezed shut | Dad folds his big hands low in front of him, his head well down. The Son folds his hands at his middle and bows his head; his hair stays up. Mom folds her hands at her breast, and her handbag slides down to the crook of her elbow. Big Sister prays exactly as she was taught, hands together at her breast. Little Sister prays with all her might: hands clasped tight under her chin, eyes squeezed shut. |
| `seated`, `sit` | For someone who is found sitting: `"ground"` or `"chair"`, and what exactly they sit on (a chair, a bench, a stool, a step, a height, or the `"floor"`: legs out, leaning back on the hands) | The scribe, the lamp boy, the goldsmith, the street boy, the soothsayer, the clerk, Grandpa Joe (in his rocking chair, and on the limousine's seat), and Jed in the dust (`"floor"`); since round thirteen Phyllis (on a low stool drawn with her, which stays where it is when she gets up), Titus (on a statue's base, high: he hops down) and Eleazar (on his bench) |
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
glasses, and things to carry; and since round thirteen a tunic tied on one shoulder (Felix),
a toga too small or very large (the Gaul's two), and a mantle with a tassel at each corner,
each with its thread of blue (Eleazar's). A person's own small movements can be written
beside them in `people.js` (`addMoves`), as the Rome people's are.

Three things a scene writer needs to know:

- **Where a seated person is put.** Their place in the scene (`at`) is the ground under
  their hips, and the seat itself is painted into the picture, or drawn with them.
- **Words sit just above the head.** The rig says how tall each person is as they are
  found, sitting or standing (`tallOf` in `rig.js`), and a speaker's words are put ten
  pixels above that, for a seated scribe far away and a standing father close by alike.
  (A staff that rises above its owner's head is not counted.) When a taller head stands
  level with the speaker or nearer us, the words go up over it too, by up to 90 pixels.
  Someone standing farther back whose face is just where everybody's words would go
  (Grandma Jolene behind her counter) can be marked with the sprite flag `clear`
  (`g.actor("jolene").flag("clear", true)`): words are then lifted over her head
  wherever she is under them, by up to 110 pixels.
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

A painted figure ("Painted frame by frame", above) lives the same way. His small movements are the sets his sidecar
names as `fidgets`, and he is found sitting up only if his entry says `sit: true` (`{ id: "ranger", kind: "ranger", at:
[...], sit: true, life: { ... } }`): then he settles back on all fours to go to a spot, and sits up again on coming home.

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
means nothing yet), and the scenes the player has entered, in order (`visited`, which the map
reads: section 8, "The map, and the Timer"). <!-- MAP-15 --> Nothing else. Every scene rebuilds itself from those facts: its
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
- A save from before the map has no `visited` (every one made before round fifteen). It is <!-- MAP-15T: it said "(every one
  made before round fifteen, and the testers' saved games)": they carry the list since they were made again, 14 October -->
  given one as it is loaded (`visitedOf` in `game.js`): the scenes of every beat of every act whose gate is done, the
  scenes of the beats done in the act under way, and the scenes where the team stands. The `?scene=` shortcut does the
  same. A save with a list keeps it (`complete()` in `state.js` keeps a list and leaves anything else for the game to
  fill), and the save version stays 3. <!-- MAP-15 -->
- A save can also lack a lead this version has: one who joined the cast after it was made
  (Grandpa Joe and Ranger, in Act Five). `complete()` in `state.js` gives such a lead no
  place (nowhere, until the story puts him somewhere) and empty pockets, and the save
  version stays 3.
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
same way into the scene, and a note at the top naming the part ("Act One · Get into the
wagon and take the road map from the glovebox"). Those saved games are `js/content/checkpoints.js`: for each beat,
the game as it stood the first moment the player had control after that beat was done, with
everything in the pockets, every fact, and everyone where they stood. They are not written
by hand. They are captured from the scripted playthroughs (the act tests described in
section 12), which play each act in the real game by real clicks: a hook in each script
keeps a copy of the game's own autosave whenever a beat's fact has just come true, and
`python3 scratchpad/checkpoints/build.py` runs the plays, gathers what they captured,
writes the file in story order, and loads every checkpoint to see that it opens. It takes
about half an hour, because the plays are slow by design, and it has to be run again
whenever an act's beats, scenes or scripts change, or the parts will be yesterday's game.

**Today they are.** The file was last made on 14 October, at the end of round fifteen, from
the game with the map merged: 58 saved games, one for each beat of the story, and every one
loaded again to see that it opens. Act One's are captured from its play with the inside of
the wagon (the road map's part opens inside the wagon), and Act Two's sixteen from its play
of the act as it is now. Each carries the scenes its play had entered (`visited`, which the
map reads). And Dad and the Son stand where the story left them: the plays of the later acts
begin from the `?scene=` shortcut, which knows nothing of them, so the script gives every
saved game after Act One's gate Dad's place at his door, as the Egypt play left him, and every
one after Act Two's the Son's in the treasury, as the Rome play left him (43 and 27 saved
games), and packs those again with the game's own `pack`, so that each checksum is the game's.
<!-- MAP-15T: it said the file was last made on 13 October, at the end of round thirteen, from
the game with both of the round's builds merged, and Act Two's sixteen from "its new play" -->

Three things follow from where the saved games come from. An act's gate and the next act's
opening are one moment (the player first has control again after the hand-over), so they
are one and the same saved game, and the buttons treat them as one part, named for the
opening. The plays do the puzzles of an act in their own order, so a part can have a later
puzzle of the act done already (Dad has the copper mirror before the shade is up); the row
names the part that was jumped to until a puzzle is done or undone, and then the furthest
one done. And the last part is the end of the demo, as the game stood when the ending went
to the title screen (in the file as it is, Act Five's gate: the back of the limousine, at
the gate of the Office Of Peculiar Sectors).

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
Egypt, Rome, home in the evening, Big Sister's attic, the Nevada desert and the tunnel,
and the Last Stop Rag that Grandpa Joe hums in the limousine (`rag`: the limousine names it
with `music` while he sings; its notes are the phrase his banjo plays on the porch), and,
since round thirteen, the quiet across the Tiber (`tiber`: Rome's mode, slower and softer,
named by that scene with `music`; it stops while the old man talks with the boy, from his
greeting to his "Go in peace", so that the river is heard, very softly, and comes back after).
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
`rome.en.js`, `home.en.js`, `nevada.en.js` (Act Four, and the cut-scene "Backup") and
`limo.en.js` (Act Five), and `common.en.js` for the lines that belong to no one act (the
opening movie, what the family say when they look at one another or hand something over,
and the stock replies for things nobody wrote a line for). So an act can be written, read
aloud and recorded as a piece.

```js
"egypt.river.look": ["dad", "Either that's the Nile or a very committed car wash."],
```

`js/content/lines.en.js` gathers the six files into the one list the engine uses, and
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
that a scene file holds, and every word in it is a line id as everywhere else. In outline (a sketch: its line ids
are made up for the example; the game's own trees are at the end of this section):

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

**The game's own.** The talks of Act Four and Act Five are trees, in `js/content/talk/nevada.js`: Grandpa Joe
(`joeTree`), Grandma Jolene (`joleneTree`), Ranger (`rangerTree`: he says "...", and Grandpa Joe says what he means),
the hens (`hensTree`), the Son through the coin door (`letterboxTree`, held with `{ through: "son" }`) and the
limousine's divider (`dividerTree`). Each is a function of the scripts its scene hands in, the moments a branch needs
staged (`joeTree({ lemonade, witness, coinTold, play, banjo, banjoDone, hold })`); a script that is not handed in is
passed over, and the talk still says every line and sets every fact. The head of the file says what each must do.
Since round thirteen the talks of the bigger Rome's seven are trees too, in `js/content/talk/rome.js`, made the same
way: the Gaul (`gaulTree`, in the Forum), Phyllis (`phyllisTree`), Titus and the goose-keeper on the Capitol
(`titusTree`, `anserTree`: the goose-keeper's hook `stomp` is the solution of Juno's Geese), and across the Tiber
Eleazar (`eleazarTree`, every hook of it staging: the prayer side by side, the hand on the boy's head), Mariam
(`mariamTree`) and Felix (`felixTree`). The act's old conversations (the doorkeeper, the senator, the keeper and the
rest) are still the flat menus they were, with the few options round thirteen needed added: rewriting them as trees
waits for the author's review of the puzzles.

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
`home.js`, `nevada.js`, `limo.js`) that lists its beats. `js/content/story.js` puts the acts in
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

<!-- ROME-13E -->
**The map.** The storyboard draws each act's places as a map, from the scenes' own data, so that anyone can see how an
act's places join: each place a small picture of its backdrop, laid out by its ways out at the edges of the picture (what
a scene's bottom edge leads to is drawn below it, its top edge above it, its left and right edges to either side). The
first place laid out stays put, and a place whose cell is taken goes on to the next free one that way, its line bent round
anything in between; but a place laid out because its own edge leads to one already placed goes first to a free cell
beside the one it asked for, so that its line stays short (since the round's third phase, TESTS-13R: before, Act One's
map put the wagon's inside a whole place above the pyramid's foot, with one long curve down to the river). A place reached only by a door or a thing to click (in `exits`, with no edge between the two) is drawn
beside, its line dashed and labelled with what the label line says over the thing, when its script names the place. Each
way out at an edge is a line with its own label (`edgeLabel`: "Go into the Forum"), and a diamond if it is there only some
of the time (`when`); a way to another act's place is an arrow off the map, with that place's name. Under each map is a
table of every way: where from, which edge (or a door), where to, the `spawn` mark it arrives at, and its label. A scene
that will not load, or a way to a scene that is not there, is said in red, and the rest of the page is drawn. Change a
scene's `edges` and the map follows.

Today there are a prologue and five acts: Egypt (five scenes: the river where the wagon came
down, the inside of the wagon, the foot of the pyramid, the great gallery and the burial
chamber), Rome (six: the steps of Saturn's temple, the street, the treasury, and since round
thirteen the Forum, the Capitol and across the Tiber), home (five, the rooms of the house),
the Nevada desert (two: the roadside and the store; the cut-scene "Backup" is played on the
roadside), and Act Five, of which only the opening is built (one scene, the back of a
limousine), whose last card is the end of the demo. The puzzle documents in `docs/` say what
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

### Seven leads, apart and together

Dad, the Son, Mom, Big Sister and Little Sister can each be played, and in Act Five
Grandpa Joe and Ranger, his raccoon (below, "A party is any leads"). Every lead has a
place and pockets of their own; `state.active` says who the player is, and `state.team`
lists who they can switch to at this point in the story. A script sets it: `g.team(["mom",
"bigsis", "lilsis"])`. Each member of the team has a portrait at the top left of the
screen.

**Apart.** Dad and the Son are in different centuries. Switching to the other one
goes to wherever he is through his map, and across the centuries the Timer turns first
(below, "The map, and the Timer"). <!-- MAP-15 --> The story can also cut between leads by itself, as it does
at the end of each act. A strong fit for this premise: something sent through a door
in one era turns up in another, so people who are apart can still help each other.
(The coin the Son throws into the door in Rome falls out of the sky in Nevada.) The
engine has this as the letterbox, below.

**Together.** Mom and the girls go through the house as one. Each of its five scenes (the
living room, the landing, Dad's study, Little Sister's room and Big Sister's attic) says
so with `party: ["mom", "bigsis", "lilsis"]`: when the one being played takes the stairs,
a door or the attic ladder, or walks off the edge of the picture, the other two come too
and arrive beside her, each on a place of her own, and switching between them is instant
because nobody has to go anywhere. So do the Nevada roadside and the store, which the
three go in and out of together (the store's `party` is a function of the game, which
names nobody once the family has gone through the door). ("A scene for several leads" in
section 10 shows how a scene says where each of them arrives.) In a party:

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

**A party is any leads.** Nothing in the engine knows who the leads are, or that a party is the family, or three: a
party is whichever leads (`lead: true` in `cast`) the scene names, two or more, and everything above works for them.
Grandpa Joe and Ranger are a party of two in the limousine (`party: ["grandpajoe", "ranger"]`), each with his own
pockets ("Grandpa Joe's bib pocket", "Ranger's stash"), handing things over and talking to each other, keys 1 and 2 for
the two portraits. A scene's `party` can also be a function of the game, for a scene that is shared only after
something has happened (the proof's: `party: (g) => (g.flag("proof.party") ? ["dad", "critter"] : null)`); a beat's
`lead` is any list of leads (`lead: ["grandpajoe", "ranger"]`); and a hint for one of them can be a list of lines, said
in turn, so that a lead who cannot talk says "..." and the one with him says what he means (the proof's: `hint: { dad:
"proof.hint.party.dad", critter: ["proof.critter.dots", "proof.hint.party.critter.dad"] }`). The stock replies (`story.fallbacks`), what a lead says looking at a companion (`story.see`) and
handing a thing over (`story.give`) are found by the id of the lead who is playing, so a new lead needs entries of his
own there (or a stock reply under `any`): without one he says nothing, and for a stock reply the console says so, once.
The proof: `index.html?scene=engine-proof&lead=dad&flags=proof.party`:
Dad and the critter arriving together by a way in, each on a mark, switching, handing, talking, a hint for each and a
beat for both (`proof.cooler`); the engine test's `party2` part plays it.

**A lead who stays in his seat** (NEVADA-12SC). Grandpa Joe rides the whole of Act Five belted to the limousine's long
seat. A scene says so with `still: ["grandpajoe"]` (or a function of the game and a lead's id, `still: (g, who) => ...`):
for a lead it names, a click on the floor does nothing, a way out at an edge does not take him, and he does everything
from where he sits: an area is looked at, used, or has a thing used on it without his walking to its `walkTo` or
turning to it, and a word with his companion is had across the car. Nor does he turn round in his seat when his
companion comes over to talk to him. What is out of his reach is the scene's to decide (in the limousine, Ranger fetches
it for him). Scripts can ask: `g.stays()` for the one being played, `g.stays("ranger")` for anyone.

**A scene seen through the lead's own eyes** (CAR-13E). The inside of the wagon is what Dad sees from the driver's seat,
and he is not in the picture: a man in the seat would cover the wheel and half the dash, and the rig has no man that size
with his legs under a dashboard. A scene says so with `unseen: true` (or a function of the game, read as the scene is
entered, as `party` is). The lead is on the stage there as anywhere, on the scene's mark, for everything that reaches for
him (his place and facing, `g.reach()`, `g.lead.look()`, the place a save keeps), but as he is put there, before the
scene's `setup`, he is faded to nothing: the cast does not draw a thing at opacity 0, and nothing in the engine sets it
back, so a game saved there loads with him undrawn. Anyone else of the team standing in the scene is undrawn too, and has
no box round his figure: a companion whom the picture shows is given an area of the scene's own (`mate:`, below). He walks
to nothing and turns to nothing, as a lead in his seat does: `g.stays()` is true for every lead there, a click on the floor
does nothing, and an area is looked at, used, or has a thing used on it from where he is. Unlike a lead in his seat, he
leaves by the edges: a click in the band of a way out takes him out at once, by the way's `use` or by `g.goto(to, { spawn
})`, with the label and the arrow over the band as anywhere (nobody is seen walking, so there is no walk to wait for). His
words, and anyone's who is not drawn there (hidden, or faded to nothing), are placed as for someone off the stage: at the
top middle, their bottom on row 150, or where the scene's `wordsAt` says (`[x, y]`, the middle of the words' bottom edge:
for a picture whose top middle the words would not read over). The x of `wordsAt` is kept 210 pixels from either side, as
a speaker's is, and a long line there is brought down until it all shows, as at the top middle; a close-up still puts the
words along the bottom. Everything else is as anywhere: hints, things carried and used, Show (the areas and the arrows,
never the lead), the menu, saving and loading, the team bar and the portraits. Elsewhere, someone a script puts out of
sight still speaks from where he is, as those scripts mean: Little Sister from inside the closet under the stairs, Grandpa
Joe from inside the limousine in the cut-scene "Backup". (A figure the cast does not draw is not moved on by it either: a
script that waits on what only his drawing moves on, a small movement, or getting up from a seat other than at once, waits
for ever. His walks, `g.reach()` and a painted figure's `play` run on the game clock, as anywhere.) The proof:
`index.html?scene=engine-proof&lead=dad&flags=proof.unseen` (with `proof.party` as well, the two of them, neither drawn);
the engine test's `unseen` part plays it, gives it a `wordsAt`, and plays the two sounds the car added, `horn` and `starter`.

**A companion's own area** (NEVADA-12SC). A companion standing in a scene gets a box round his figure to be clicked
(section 10, "What Show shows": it is outlined by his figure). Where that box would lie over other things (Grandpa Joe on
the long seat, with the bow of his ropes, the seatbelt and the divider beside him), the scene can give him an area of
its own: one of its `hotspots` with `mate: "<id>"`, while its `when` holds, is his in place of the box (its shape, and its
place among the scene's areas). A click on it is a word with him, a right click a look at him, a thing used on it is
handed to him, all as on the box. The engine test's `limo12` part proves both on the proof scene.

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
other end of a letterbox: shown top centre, as a line with no speaker on stage is (CAR-13E: in a scene seen through the
lead's own eyes a speaker who is not drawn counts as one not on the stage, and a scene's `wordsAt` moves the place, for
these lines too: above, "A scene seen through the lead's own eyes"), with that person's portrait beside
the words (the interface's `portrait`, drawn for the pixels it is shown at, never keyed) in that person's colour, and
with the `through` style (`.say.through`: lighter and leaning, as from a little way off; no echo gimmicks). It counts
the line as seen, waits and is skippable like `say`. A `choose` works the same way: `g.choose(options, { through: who })`
shows the menu as that person's words, their portrait and name at its head and the options in their colour (the options
are what the lead off stage may say). The lead on stage speaks ordinary `g.say` lines over their own head, so the player
sees one person on stage talking to a portrait of the other, which is the whole picture of a letterbox.

**Switching across the centuries.** Switching to a lead who is in another scene goes there, and their place and facing
are kept. Since round fifteen it goes through their map, and when the two scenes are in different eras (`scene.era`) the
Timer turns first (below, "The map, and the Timer"). <!-- MAP-15 --> The old way is still there for scripts
(`g.switchLead(to, { map: false })`): the short tunnel across the eras (`g.goto(..., { via: "wormhole" })`), and within one
era a fade. A lead can be switched to only if they are on the team; the scenes decide the team.

**The proof.** `index.html?scene=engine-proof&lead=dad&flags=proof.letterbox`: Dad on the sand with a pack of gum, the
Son in the market street sketch in Rome, a small door in the air. The gum goes in the door for the Son, the mark
appears, switching to him is the Timer and his map (MAP-15; before, the tunnel), and coming back as him the door gives it
up. The door with nothing in hand is a word through it, with a choose through the door. The engine test's `letterbox` part
plays all of it.

**In the game.** Act Four's coin door is the first letterbox in the story. From #9 until #12 the little door over the
glass is a thing to click, "Talk into": a talk with the Son, in Rome, held through it
(`g.talk(letterboxTree(...), { through: "son" })`, `js/content/scenes/nevada-roadside.js`); and Little Sister's lucky
penny goes into it for him (`g.send("penny", { to: "son" })`, or, when the penny is in one of the others' pockets,
straight onto the tunnel list from there). It waits in the tunnel for the Rome end of the door, which is not built yet.

<!-- MAP-15 -->
### The map, and the Timer

The author, 14 October, on what "the map" in his notes meant: "maybe if we switch back and forth between players it can use
the dial we created and load a map with a map button". Of the ways put to him he chose three things: switching to someone
in another century is the Timer (the game's emblem, section 9) turning notch by notch from one time to the other, and then
that time's map with them on it, a click on them dropping into their scene; the Map button shows the places of the time
the lead is in, the visited ones drawn in, everyone of the family where they stand, and travel back to any place already
visited; and each time has its own kind of map (a papyrus sketch for Egypt, a wax-tablet plan for Rome, a pencil floor plan
of the house, a fold-out road map of Nevada). The engine has this as the map screen (`js/engine/atlas.js`, the game's
`g.atlas`, marked `MAP-15` in the code); the maps themselves are data (`js/content/maps.js`); the pictures are the
painters' (`art/maps/<map>/`). The tunnel stays for falling through doors in the story, and the story's own cuts between
leads (the ends of the acts) keep their own transitions.

**What the player sees.** The **Map** button, in the row of tools after Show, or the key **M**, opens the map of the place
the lead is in. It is a screen of its own over the scene (a layer, `#atlas`, over the HUD and under the fade, the cards and
the menu, built of ordinary buttons and pictures as the HUD is, and scaled with the stage). At the top (rows 0 to 127): the
time and its date at the left, in the game's face ("Rome", "44 B.C."); the small dial in the middle, the Timer at that
time's notch; at the right a chip for each map the player knows (one of its places visited, or someone standing on it), in
the dial's order, A first, the one shown pressed; and Close, which lies exactly over the HUD's Map button (measured as the
map comes up), so that a second click where the map was opened puts it away again, as a toggle does, with the chips a row
lower, under it. <!-- MAP-15M --> In the middle (the sheet, x 32 to 768, y 128 to 572), the map.
At the bottom (rows 572 to 599), the label line: what the pointer or the keyboard's focus is on, and what a click there does.
M again, Esc or Close puts it away. While it is up the world stops, as under the menu: the game clock is paused and the game
is busy, so nothing in the scene moves, the tools, the pockets and the team bar are put away, nothing is saved, the testers'
`[` and `]` do nothing and the pause menu does not open. The map's own motion (the dials, a portrait walking, its fades)
runs on a timer of its own (`tween` in `atlas.js`, on the browser's frames, since the clock is stopped), and a click or a
key hurries a turning dial, the Timer or a walk to its end; the short fades as the map comes up, goes away or gives way to
the dark take no clicks and no keys, a fifth to a third of a second each. <!-- MAP-15D -->
A rustle of paper (`rustle`) as it opens and as it is put away. (The map's three sounds are in
`sound.js`: `notch`, short and dry, quieter than the vault's `dial`; `ding`, a small bell, softer than `pickup`; and `rustle`.)

**Places and ways.** A map is a sheet of places joined by ways, in one time. A place is one scene or several (the wagon's
inside is part of "By the river"); the map of a scene is the one with a place that lists it, and a scene on no map has no
Map button. A place the player has been to (any of its scenes in the save's `visited`, or one of the team standing in it)
is drawn in, with its name; a place not visited yet that a way joins to one that has been is drawn faint (its picture at
0.28), with no name ("Somewhere you haven't been yet"); any other is not shown. A way between two visited places is drawn,
between a visited place and a faint one faint, and otherwise not shown. The names are the engine's, written in Koine Road
over the painting in the map's own style (`label` in its layout: colour, a halo or none, capitals or not, spacing, size),
each at its place's anchor; a name wider than its box is drawn narrower to fit.

**The portraits.** Every lead whose place (`where` in the save) is on a map has a portrait there, at their <!-- MAP-15D -->
place's pin: a row of discs centred on the pin, 4 pixels apart, the team first (in the team's order) and then anyone else.
The team's are buttons 36 pixels across ("Play as Mom"; "Mom, playing now" for the one being played, who has a ring in
their colour); anyone else's are 28, faded, and not buttons ("Dad is here. Not playable just now."). A lead who is not on
the team is left out where he is one of his scene's own people (its `actors`): Ranger and Grandpa Joe at the Last Stop in
Act Four are part of the place, not leads left there, and the pins have room for three. The portraits are drawn as the
team bar's are (`portrait()`, for the pixels they are shown at, never keyed).

**Travel.** On the lead's own map, a click on a place they have been to, other than their own, sends them there. The route
is the fewest ways through visited places only (with none, the place is not a way to go). Their portrait (and their
party's, standing with them) walks along the ways drawn on the map (each way's `via`, turned round where it is walked from
its far end), at about 220 pixels a second and never more than 2.5 seconds for the whole trip, a soft click (`notch`) at
each place passed through; then the map fades out to the stage's own fade, is put away, and the game goes to the place's
first scene: `g.goto(id, { via: "map", spawn, came })`, arriving on the mark of the last way (as the scenes' own ways out
name it) as if they had walked in from the place before it (that place's first scene is what the scene's `enter` is told
they came from). The party comes along by the scene's own `party` and `arrive`, keyed by that mark, and the game saves, as
after any way out. A script can do the same: `await g.travel("forum")`, true when the new scene is up, or false at once
with nothing done (and the console says why) when it may not be. `g.mapOf("rome-forum")` is the map and the place a
scene is on.

**Leaving, and travel.** Two fields a scene can have. `leaving(g, to)` runs whenever the lead leaves the scene for
another, by any way (an edge, a door, the map), before anything changes; not when the player switches to a lead in another
scene, not when a script has handed the controls to a lead who is not in it (as the end of an act does), and not on loading
a save. Across the Tiber, the old man has finished his prayer as the boy goes (`rome.eleazarDown`, once `rome.sawTiber`), and
leaving the store they are not inside any more (`nevada.inStore` false, so the next time in is a new visit): both were done by
a way's script, and are done by `leaving` now, so that they happen on the map's travel too; the ways still do the rest (the
bell, the walk, the goto). `travel` says whether the lead may leave the scene by the map: `false` never, or a function of
the game. The limousine never (Grandpa Joe is belted in, and it has no way out); a scene whose act has ended, whatever a
save catches it in: the burial chamber once `egypt.ready`, the treasury once `rome.tossed`, the living room once
`home.left`, the Last Stop and the store once `nevada.left`. A refusal is a plain line on the map, "Not from here.", and
nothing is said.

**Switching through the map.** To a lead in the same scene, the controls change hands at once, as always. To a lead in
another scene (a click on their portrait in the team bar, or their number key), their map opens with their portrait
breathing; a click on it, or Enter, drops into their scene, where they stand (`g.dropInto`: the old lead's place
remembered and their walk stopped, nothing held, and `g.goto(their scene, { via: "map", at: their place, switching:
true })`: no tunnel, no era card, since the map has said where and when, and no `leaving`, since nobody leaves); Esc goes
back, and nothing has changed. <!-- MAP-15D --> A click on a portrait of the
team on any map is the same switch, and while the map is up the number keys do what a click on that portrait does.
`g.switchLead(to, { map: false })`, or a lead whose scene is on no map, keeps the old way: a fade within one time, the short
tunnel across the centuries.

**The Timer.** When the other lead's scene is in another time, the switch begins with the Timer: the emblem's three pieces
(the sky, the bow that turns and the top, laid as the begin screen lays them; at 1024 pixels once the page lists all three,
else the 512s the begin screen gives a sharp screen; the 1024s were made in round fifteen: section 9, "The Timer at 1024"
<!-- MAP-15D -->), 440 pixels across in the middle of the dark, come in from a little smaller with
a fade (0.25 s), and the bow turns from the active lead's time to theirs, notch by notch: each a snap of 0.12 s into the
notch, a tenth of a notch past it, a settle of 0.06 s back and a hold of 0.08 s, with a click (`notch`) as it lands, and a
small bell (`ding`) at the end. Then the dial shrinks and rises into the small dial's place at the top of their map (0.4 s)
as the map fades in under it. A click or a key hurries it to its end. Each time's notch is `dial` in `eras` (`world.js`):
A, today, is 0 (the present, home and Nevada), B.C., the furthest back the game goes, is 8 (Egypt, about 1920 B.C.), and Rome
is 4; the bow is at `rotate(48deg)` at A and 12 degrees less at each notch, about the point 50% across and 58.59375% down,
as on the begin screen. Two times on one notch (home and Nevada) have no turn: a fade to the map. On the map, the chips, a
click on the small dial (the next map) and the Left and Right keys turn the small dial the same way, notch by notch from the
shown map's time to the chosen one's, a click at each and the bell at the end (two maps on one notch: one click, no turn),
and the sheet changes with a short cross-fade.

**Less motion.** With less motion (the system's or the game's own), nothing on the map moves: a dial is shown at its notch
at once (with the bell), a portrait is where it is going at once, the one being switched to has a steady thick ring instead
of a breathing one, and one screen gives way to the next by a fade.

**The pictures.** A map's pictures are in `art/maps/<map>/`: `back.png`, the sheet on clear ground (its material, and the
lie of the land anyone would know before setting foot there, never a place or a way); `place-<id>.png` for each place and
`path-<a>-<b>.png` for each way, clear but for that thing's own drawing; and `layout.json`, the painters' measurements: the
`sheet`'s box, the names' `label` style, and for each place its `picture`, its `shape` (what is clicked), its `pin` (where
the portraits stand) and its `label` anchor with `label_max`, and for each way its `picture` and its `via`, a line along
its drawing from one pin to the other. Each is 800x600, laid over the whole stage, as painted and never keyed: the map is
the interface's, as the inventory pictures are. They are fetched with the rest of the game's pictures behind the title,
quietly and last (`gather`): a map's `layout.json` only when it is among the page's files (its stamp), so that a map not
painted yet asks the server for nothing, and then its pictures. A map with no `layout.json`, or one that will not load or
does not fit the map (the console says so, once), is drawn as a sketch from the pins in `maps.js`, as a scene with no
painting is sketched: the interface's own papyrus, a box at each place's pin with its name inside, the ways dashed in ink,
and the same three states. <!-- MAP-15D --> The four maps of the story are painted (section 9, "The maps"); the proof's two
are sketches.

**At every start** the engine checks the maps against the scenes and the eras, beside the edge check ("Map check: ..."): a
place's scene that is not in `index.js`, on two maps or listed twice; a way whose places are not on its map; a way's mark
that its scene has no spawn for (a mark that is a function of the game is asked which mark it gives); a map whose time is
not in `eras` or has no notch; and any scene of the list that is on no map.

**The proof.** The engine's proof scene and the sketch of a market street are on two maps of their own, drawn as sketches
(`proof-sand`, in Egypt, and `proof-street`, in Rome). With the letterbox proof (Dad on the sand, the Son in the street),
`index.html?scene=engine-proof&lead=dad&flags=proof.letterbox,proof.arrived` and then 2: the Timer turns from B.C. to the
middle notch, four notches, then the street's map opens with the Son breathing, and a click on him drops into his scene.

<!-- MAP-15D -->
**In the game.** No act has the team in two times at once yet: Dad and the Son are apart in Acts One and Two, but each
plays his act alone, and the family, then Grandpa Joe and Ranger, are together. So in the story the Map button works in
every act, travel and the maps of the other times are there, and the small dial turns as the player turns from one map to
another; but the switch across the centuries, the Timer turning and then the other's map, is seen only in the proof. It
will first be seen in the story with Round One's step (Act Six in `briefs/out/story-redesign.md`: Dad and the Son at their
doors). In a game played through, Dad stays where Act One leaves him, at his door in the burial chamber, and the Son where
Act Two leaves him, in the treasury, and their maps show them there, smaller and faded, from then on. The testers' saved
games are each captured from a play of one act, which knows nothing of the leads left behind before it, so the script that
makes them gives those after Act One's gate Dad's place at his door and those after Act Two's the Son's in the treasury, as
the plays that passed the acts on left them: their maps show them there too. <!-- MAP-15T: it said that from the second
part of Act Two on Dad had no place in them, nor the Son from the second part of Act Three, and that on those the Egypt
and Rome maps showed nobody: so they were until round fifteen's testers made them again -->
Within one time, switching to someone
in another scene is the map with them breathing (a fade, no turn), then the drop: in the house, a sister in another room,
when one is.

**The test.** The engine test's part `map` (in its quick run) checks all of this, reading every position from the maps'
data and the maps' layouts (`g.atlas.layout(id)`: the painters' `layout.json`, or the sketch's), so that it passes on the
paintings as on the sketches: the button and M, the world stopped and nothing saved while the map is up; the four maps on
the act's checkpoints (what is drawn, faint and absent, the names and their style, the places to click, the portraits at
their pins, the band); travel two ways off (the mark, the scene `enter` is told, the walk along the ways, the party, the
save, `leaving` by the map and by the bridge, the store's visits); the refusals; the chips, the dial's clicks and its
angles; the letterbox proof's switch (the Timer's four notches and the bell, Esc, the drop with no tunnel and no card, a
click and a key hurrying it); the number keys; the keyboard alone; less motion; the save's `visited` and the shortcut's; a
painted map from throw-away stand-in pictures, and a broken `layout.json` drawn as the sketch; and the three sounds (each
heard; the click quieter than the vault's dial; the bell and the paper no louder than `pickup`). It takes screenshots of each
map open, of the Timer, and of the stand-in (`shots/map-*.png`), which have to be looked at.

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
- **One signature shape, kept small.** The game's mark is the Timer (EMBLEM-13, the author's
  pick of 13 October), a sunset bow drawn as a 1950s kitchen-timer dial that reads from A
  through notches to B.C.: on the gate you click to begin it turns from A to B.C. and back,
  notch by notch (holding still for less motion), its still is the browser tab icon
  (`art/emblem/`, `css/game.css`), and the dashed rings turning in opposite directions
  still rush past in the time tunnel between eras. The doors themselves no longer wear them.
  <!-- MAP-15D --> Since round fifteen the Timer is also the small dial of the map screen, and the large one that turns
  from one time's notch to another's when the player switches across the centuries (section 8, "The map, and the
  Timer"; below, "The Timer at 1024").
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
| Egypt at noon | egypt-crash, egypt-car (the inside of the wagon: the same sun through its glass), egypt-site | chrome yellow / cobalt blue | naples and chrome yellow, through orange | lilac, cobalt violet, deep violet |
| Rome in the morning | rome-steps, rome-street, rome-forum, rome-capitol, rome-tiber | naples yellow / cobalt violet | lead white, naples yellow | lilac, cobalt violet, toward ultramarine |
| The house at night | home-living-room, home-landing, home-study, home-lilsis-room, home-bigsis-room | lamplight / ultramarine | naples and chrome yellow, chrome orange | ultramarine, deep violet; viridian on greens |
| Lamplit rooms | egypt-gallery, egypt-chamber, rome-temple | chrome orange / ultramarine | chrome yellow, chrome orange (the lamps are lights, not lit walls) | ultramarine, deep violet |
| Nevada in the morning | nevada-roadside, nevada-store, nevada-limo | chrome orange / cobalt blue | lead white, naples and chrome yellow | lilac, cobalt violet |
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

**A new scene, or a repainted one** (as the bigger Rome's three new places, and the inside of the wagon, were in round
thirteen):

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

A scene repainted only in part (round thirteen: the river's wagon, its driver's window rolled down) should keep the
palette it was keyed with, so that only the pixels painted again change. `install.py --keep-palette` does not quite do
that today: it reads the palette back from the installed picture, where it is rounded to whole numbers, and some
thousands of pixels nobody touched fall to the next paint (17,000 of the river's, with nothing repainted). The painter
of the car's inside installed the river with the exact palette instead, by a script kept beside the game and not in it;
keeping the exact palette in the ledger, `postimp_keyed.json`, would mend the tool.

<!-- MAP-15D -->
### The maps

The author's choice of 14 October: **each time its own kind of map.** A map is a thing of its world, made the way people
there made such things, so each of the four is a different object, and the rule above still holds: what changes is what is
painted (the material, and the hand that drew on it), never how. Each is what somebody in the story would have had to hand:
a scribe's papyrus where the pyramid is being finished, a writing tablet such as a Roman boy did his lessons on, Dad's own
plan of his house, and a road map from the rack on Grandpa Joe's counter ("A road map of Nevada. It stops here too.").
All four are painted by scripts with the scene painters' kit, in the four passes (the brush at sizes 7, 4 and 2, kept calm
enough to read names on), every colour mixed from the box of paints by name; and they are the interface's pictures, like
the inventory's, never keyed: what is painted is what the map screen shows. Nothing on them is copied from any real map,
papyrus, tablet or plan, and none of them names a year B.C. or a real company.

| Map | What it is | Its names (drawn by the engine) |
| --- | --- | --- |
| Egypt | A scribe's sketch on papyrus, two sheets joined, the edges frayed and browned, an old fold, two stains, three pen trials in the margin. The land as a scribe draws it, side-on: the Nile along the bottom (zigzag water, fish, lotus), the edge of the desert, three small pyramids far off, and the pyramid itself in section, as seen from the river, with the great gallery and the burial chamber drawn inside it. Black ink for the places, red for the ways (the track up from the river with the boy's small prints, dots up the stair and the ramp), and a few thin washes: the river's blue-green, the palms' green, the red wagon (all four wheels in a row), the king's gold. Lot's donkey drinks by the wagon. | Dark ink-brown, not in capitals, with a halo of the papyrus's palest straw |
| Rome | A writing tablet: a raised frame of plain wood round a panel of dark beeswax, the plan scratched into the wax with a stylus, each scratch pale where it reaches the wood, its walls lit and shaded by a light from the upper left; old writing rubbed out under it, none of it legible. Saturn's steps in the middle (the temple's front), the street to the left, the treasury behind the temple's doors, the Forum's long square below, the Capitol up its hill to the right, and across the Tiber at the lower left, beyond the river's bend and over the stone bridge. No lettering, nothing in Latin. | Capitals in the scratch's pale, spaced, with a halo of the dark wax |
| The house | Dad's pencil plan on squared paper (a square is two feet), folded into a pocket, creased, a corner turned over, an eraser smudge or two: the ground floor on the left, upstairs on the right with the attic above it, each titled and underlined; the walls, doors and stairs on the sheet, each room that is a place in plan with its things, the rooms that are not places left empty. Dad's arrow "up" runs from the foot of the stairs to the landing. | Pencil grey, not in capitals, with a faint halo of the paper |
| Nevada | Grandpa Joe's own fold-out road map, opened flat: thin paper gone yellow, creased into panels and worn at the folds, printed in a few flat inks a little out of register. The highway in red through LAST GAS and "37 MI." on to the east edge, TO NOTHING; ranges, dry lakes, a cover panel ("Compliments of GRANDPA JOE'S LAST STOP"), a legend, and a detail panel ("DETAIL · 37 MILES PAST LAST GAS", "NOT TO SCALE") in which the Last Stop's lot is in plan, with the store drawn inside the shack's walls and the hens out back; the No Gas sign marks the Last Stop on the highway. Once Act Five has begun, a small printed gray limousine on the road beyond it. | Printed blue-black capitals, spaced, knocked out of the paper |

**The pictures** (`tools/paint/README.md`, "Maps", has them whole; section 8 says how the engine reads them). Each is 800x600,
a palette with one clear colour and hard edges, one palette for all of a map's files (208 colours for Egypt and the house,
200 for Rome and Nevada), the sheet within x 32 to 768 and y 128 to 572 so that the band at the top and the label line stay
clear, and no more than 1.5 MB to a map (the four are 0.25 to 0.31 MB). `back.png` is the sheet and the lie of the land,
never a place or a way; each place and each way is a picture of its own, laid over it; `layout.json`, measured from the
finished pictures by each map's own script, gives the sheet's box, the names' style, and for each place what is clicked,
where the portraits stand and where its name goes. The rows of portraits were laid out for two on the maps of Egypt and
Rome, where one person plays the act, and three on the house's and Nevada's. A place not visited yet, next to one that has
been, is drawn at 0.28: each painter looked at theirs so, and it reads as "not yet"; and a place not shown at all is
plainly gone, since nothing of a place is in the sheet.

**The Timer at 1024.** The switch across the centuries shows the emblem 440 pixels across, which a sharp screen draws with
880 of its own, and the begin screen's pieces are 512 at most. So the three pieces (the sky, the bow that turns, the top)
were drawn again at 1024 (DIAL-15), not enlarged: the same drawing sampled twice as finely, every length kept in the 512
drawing's own pixels. Its circles keep their exact centres, its edges along whole rows stay on the same rows, the letters
and the notches are drawn at twice the size, and the grain is the same field drawn finer; brought down to 512, each piece
matches the begin screen's but for where a hard edge falls on a pixel, and each stop still sits under the index.
They are made by DIAL-15's copies of the emblem's scripts (`logo4.py`, `logo5.py` and `brush.py`, every change marked),
kept beside the game in the scratch folder (`scratchpad/work-map-dial/emblem/make1024.py`) and not in the repository; the
same copies make the three 512 pieces again, pixel for pixel (the script that put the pieces together in round thirteen,
`make_emblem.py`, is gone). The three come to 873 KB, fetched quietly behind the title with everything else, and the engine
lays them only once the page lists all three (`tools/stamp.py`). Where the dial itself is drawn 1,600 or more device pixels
across (a large window on a sharp screen), the 1024 is enlarged in its turn, and the rim's edges show faint steps
(section 14, decision 86).

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
  unseen: true,                                 // (CAR-13E; seldom) the picture is the lead's own view: he is on the stage, never drawn, walks nowhere, leaves by an edge at once (section 8)
  wordsAt: [400, 120],                          // (CAR-13E; seldom) where the words of anyone off the stage go, in place of the top middle (section 8)
  travel: (g) => !g.flag("egypt.ready"),        // (MAP-15; seldom) may the lead leave by the map now? false: never (section 8, "The map, and the Timer")
  leaving(g, to) { /* ... */ },                 // (MAP-15; seldom) what happens as the lead leaves for another scene, by any way: an edge, a door, the map
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
party: ["mom", "bigsis", "lilsis"],                         // they are here together (any leads; or a function of the game)
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
still: ["grandpajoe"],          // (NEVADA-12SC; seldom) leads who never walk here, but do everything from where they are (section 8)
// (NEVADA-12SC; seldom) a companion's own area, in place of the box round his figure: { id, name, mate: "grandpajoe", poly, when } in hotspots
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
staff) goes in the entry's `extras` function. An animal is painted frame by frame instead
(section 4, "Painted frame by frame"): its frames and sidecar go in its scene's folder, a
line in `js/art/painted.js` names the sidecar, and the `cast` entry is the same.

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
block in `css/tokens.css` (for its sketches). Give it its notch on the Timer, `dial` (MAP-15):
the stop its years put it at, rounded, A being today (0) and B.C. the furthest back the game
goes (8: Egypt, about 1920 B.C., some 3,945 years back): 8 x (years back) / 3,945. Rome, 44 B.C.,
is 2,069 years back (there is no year nought: the count PUZZLES-rome.md makes for the act's last
card), 4.2: the middle notch. <!-- MAP-15D: the years counted as the game counts them; js/content/world.js's comment says 2,070 and 3,947 --> A time with no notch (the tunnel) is on no map.

**A map** (MAP-15). Give it an entry in `js/content/maps.js`: its time (`era`), the word on its
chip (`name`), its folder of pictures (`art`), its places (each one's scenes, the first the one
travel goes to, and the `label` the engine writes on the map; `go` for the words after "Go" on
the label line, when "Go to" and the name would not read well), its ways (`a`, `b`, and for each
end the mark of that end's scene where a lead arrives along it, as the scenes' own ways out name
them, or a function of the game that says it), and a pin for each place in its `sketch`, laid
out as the ways run. It is drawn as a sketch until its pictures and `layout.json` are in
`art/maps/<map>/` (section 8, "The map, and the Timer"); run `python3 tools/stamp.py` so the page
lists them. <!-- MAP-15D --> The pictures are painted as the painter's guide says (`tools/paint/README.md`,
"Maps": a script of the map's own, with its `_layout` and its `_check`), and installed as painted by
`python3 tools/paint/install.py map-<map>` (its line in `install.py`'s `PLACES`: `"map-<map>": "maps/<map>"`).
A new place on an old map: its scenes, label, ways and pin, and the painters' picture
of it. At every start the engine checks the maps against the scenes and the eras, and says in the
console what does not fit ("Map check: ...").

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
| `await g.through("son", "id")` | A line from a lead who is not on the stage, at the other end of a small door in time: top centre, with their portrait beside the words, in the `through` style (section 8, "The letterbox"). Counted, timed and skippable as `say` is. (CAR-13E: top centre is where any line with no speaker on the stage goes, and in a scene seen through the lead's own eyes a speaker who is not drawn counts as one not on the stage; a scene's `wordsAt` moves the place: section 8, "A scene seen through the lead's own eyes".) |
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
| `await g.goto("scene", { via: "wormhole" })` | Changes scene by fade, cut or time tunnel. `{ spawn: "name" }` arrives on that mark of the scene's `spawn`, and the rest of a `party` on its `arrive` places of that name ("A scene for several leads", above). (MAP-15) `{ via: "map" }` after the map has faded out to the dark: no fade out and no era card; `{ came: "id" }`: the scene its `enter` is told the lead came from. The scene left runs its `leaving` first. |
| `g.leave("N")` | Leaves by the scene's way out at that edge, as a click in the middle of its band does: the lead walks there, and on. `g.edgeAt(x, y)` says which way out a place of the picture lies in the band of (`"N"`, `"S"`, `"W"`, `"E"` or `null`), and `g.leaving` which one the lead is on his way out by. |
| `g.reveal(true)`, `g.reveal(false)`, `g.reveal(true, 2400)` | Show: turns the outlines on until told otherwise, off, or on for a while (as the button does). `g.outlines.drawn` lists what was outlined, and how. |
| `await g.card("Ancient Egypt", "about 1920 B.C.")` | Shows a title card. (Egypt is about 1920 B.C. because the game counts the years before Christ from the Bible's own genealogies, as Archbishop Ussher counted them: see "How the game counts the years" in [CHARACTERS.md](CHARACTERS.md#how-the-game-counts-the-years).) |
| `await g.cutscene("intro")` | Plays a skippable cutscene |
| `await g.wait(ms)`, `await g.tween(ms, (k) => ...)`, `await g.fade(1)` | Timing, motion, fades |
| `g.music("egypt")`, `g.sfx("portal")` | Sound. `g.musicOf(g.scene)` is the track the scene plays now: its `music`, which may depend on the story, or its era's. |
| `g.effects.get("altar-smoke").show(false)`, `.show(true)`, `.auto()` | One of the scene's moving things (`fx`) taken away, or shown, whatever its `when` says; `auto()` hands it back to its `when` (section 2, "Things that move by nature"). |
| `g.effects.get("pigeons").scare([x, y])`, `.scare()` | The birds of a flock near that place go up (all of them, with no place), as if somebody had rushed at them, and keep clear of it for a moment: a "Chase". |
| `g.effects.add({ type: "flame", at: [x, y], size: 10 })` | Puts another moving thing on the stage, until the scene changes (a fire the story lights). |
| `g.effects.get("desert").set({ speed: 0 })` | A strip goes on at another speed from where it is (0: parked). Tweened, the car slows to a stop: `await g.tween(3000, (k) => g.effects.get("desert").set({ speed: 160 * (1 - k) }))`. |
| `g.effects.get("desert-l").set({ speed: 0 })`, `.speed` | A drive likewise, in metres a second (section 2, "The world going by a car's side windows"). <!-- DRIVE-16E --> |
| `await g.settle()`, `await g.settle("scribe")` | Brings everyone of the scene's people who is away on a walk of their own home (or one of them), briskly, sitting down if they sit (section 4, "Their own lives"). Every script already gets this before it starts. |
| `await g.walkTo(x, y)`, `await g.walkTo(x, y, "scribe")` | Walks the lead, or someone else, to a place, round whatever is in the way |
| `await g.moveTo(x, y)`, `await g.moveTo(x, y, "agent")` | Walks in a straight line to a place the player could not click on (into a closet) |
| `await g.reach()`, `await g.reach(true)` | The lead reaches out, or bends down to the ground |
| `g.lead.hold()`, `g.lead.hold(false)` | Someone keeps an arm held out while people talk (holding a thing up), until told to let it drop |
| `g.actor("mom").pray()`, `g.actor("mom").pray(false)` | Someone prays, in their own way (section 4), through whatever is said, until told to stop: standing still, or sitting where they sit. End it before they walk. |
| `g.lead.shade()`, `g.lead.shade(false)` | Someone standing shades their eyes from a glare (section 4) until told to stop |
| `await g.actor("ranger").play(g.clock, "nibble", { ms: 1800 })`, `.stop()` | Someone painted frame by frame plays one of his sets by name (section 4, "Painted frame by frame"): for `ms`, or until stopped; resolves when it ends. Praying and shading the eyes do nothing for him. |
| `g.actor("ranger").variant("shades")`, `.variant(null)`, `.variant()` | Someone painted frame by frame in another state his sidecar has (every set, and his portrait), back as he was, or which one he is in. Not saved: the scene puts it on from a fact in `setup`. |
| `g.assets.url(path)`, `g.assets.picture(path)` | For a script that puts a painted picture on the live layer: its stamped address, and a promise that it has arrived |
| `g.actor("scribe").face("W")`, `g.lead.look(x, y)` | Turns someone to a compass point, or toward a place |
| `g.plane("trunk")` | One of the scene's cut-outs, or `null`: `.show(true)`, `.set("open")`, `.fade(0.5)`, `.place(x, y, scale)` |
| `g.actor("scribe")`, `g.lead`, `g.q("#beam")`, `g.effects.get("door")` | Reach people, the parts of the live layer, and the moving things (a door in time among them: `.open(k)`) |
| `g.team(["mom", "bigsis", "lilsis"])` | Says which leads the player can switch between from now on |
| `await g.switchLead("son")` | Changes who the player controls (they must be on the team). One who is in another scene is switched to through their map, the Timer first when the two scenes are in different eras (section 8, "The map, and the Timer"); `g.switchLead("son", { map: false })` keeps the old way: the short tunnel across the eras, a fade within one. <!-- MAP-15 --> |
| `await g.travel("forum")`, `g.mapOf("rome-forum")`, `g.atlas.show()` | (MAP-15) The lead travels to a place of their own map as a click on it does (true when the new scene is up; false, and nothing done, when they may not go); the map and the place a scene is on (`{ id, map, place }`, or null); the map screen comes up, as the Map button brings it (section 8, "The map, and the Timer"). |
| `g.closeup(drawing, label)`, `g.closeup()` | Shows a close look at something, and puts it away |
| `await g.tap()` | Waits for a click or a key |
| `g.startTunnel(dates)`, `g.stopTunnel()`, `await g.wormhole()` | The time tunnel, and the short trip between two eras |

For cutscenes, which dress the stage themselves:

| Call | Does |
| --- | --- |
| `g.view.clear()`, `g.view.setEra("present")` | Empties the stage; sets the era |
| `await g.view.draw("", words, { picture, live, grid: [800, 600] })` | Puts up a painted backdrop and its light. `words` describes the picture for someone who cannot see it. |
| `g.view.cast.addPicture(id, { src }, x, y, scale)` | A painted sprite to move about: `{ src }` or `{ frames, fps }`, with `foot: [x, y]`, the point of the picture that is put at (x, y). It has `.place(x, y, scale)`, `.fade(opacity)` and `.flag("still", true)`, and (NEVADA-12SC) `.flag("mirror", true)`, which draws it turned left for right about its foot point: a car that came in nose first goes out the way it came. Shown smaller than it was painted, it is drawn smoothly. |
| `await g.view.cast.load()` | Waits until every picture on the stage has arrived. Do this before fading in. |

---

## 11. The tools

| Tool | What it is for |
| --- | --- |
| `python3 tools/serve.py` | Runs the game on your computer at `http://localhost:8000` (`8080` for another port, `--lan` to let a phone on your network open it). It tells the browser to keep no copies, and stamps the pages again whenever a file has changed. |
| `python3 tools/stamp.py` | Gives every code file, style file and picture an address that changes when the file does ("Publishing a new version" in section 10). `--check` changes nothing and says whether a page is out of date. |
| `tools/hooks/pre-commit` | Runs `stamp.py` at every commit, once turned on (two commands, at the top of the file) |
| `tools/storyboard.html` | The story from the game's own files: acts, chains and beats; a map of each act's places joined by their ways, with a table of every way (section 8, "The map") <!-- ROME-13E -->; the title and every scene as the game builds it, with clickable areas, walkable ground, blocked patches and the base line of each cut-out; the era palettes; the script by character, with a button that exports it as a spreadsheet. It says so at the top if the story has a beat that cannot be reached. |
| `tools/sprites.html` | Everyone in the game, from the settings in `people.js`: every direction, the walk, every gesture, reaching and sitting, at the sizes they appear in a scene, against a choice of grounds; and anyone painted frame by frame, from his sidecar: every set moving both ways round, every picture, each variant, the portrait |
| `tools/paint/` | The scripts that paint the pictures, one for each scene, with their shared library and the painter's guide. `python3 install.py <scene>` keys a painted scene in the game's paints and copies it into `art/` (section 9, "The paints"). <!-- MAP-15D --> Since round fifteen, one for each map as well (`map_<map>.py`): `python3 install.py map-<map>` copies a map into `art/maps/<map>/` as painted (section 9, "The maps"). |
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
a lead painted frame by frame, a strip going by behind windows, a party of two who are
not family, a lead who stays in his seat, a companion's own area and a cut-out turned
left for right; since round thirteen a flock herded into a pen and posed, a cut-out riding
the water, a man at an upper window, the depth order where bases slant (and the same stage
put on in the reverse order painting the same pixels), and a scene seen through the lead's
own eyes, with its two new sounds; since round fifteen the map screen, the Timer, travel on the map and
switching through it (the part `map`: section 8, "The map, and the Timer"); <!-- MAP-15 --> since round sixteen the world
going by a car's side windows (the part `drive`: section 2); <!-- DRIVE-16E --> the interface at two sizes and in three other window
shapes, the storyboard page and its maps, the intro and the stamping tools: some 650 checks
in its quick run (655 at the end of round sixteen, 25 of them the part `drive`'s <!-- DRIVE-16E --> <!-- DRIVE-16F: four of them the things' shadows: 651 and 21 at the merge -->; 629 at the end of round fifteen, 116 of them the part `map`'s), in about twelve minutes on the test
machine. <!-- MAP-15D: it was some 510, in eight or nine minutes, before the map --> It takes screenshots, which
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
dialogue system and its dialogue trees, the story-as-data structure, the pixel renderer and
the figure, the interface, the Koine Road typeface, the stamping of files, and the letterbox
(things and voices through a small door in time, between leads who are centuries apart:
section 8), which Act Four's coin door is the first to use. Since round twelve: people
painted frame by frame (an animal who is a lead: section 4), a strip of country going by a
car's windows (section 2), a party of any leads, a lead who stays in his seat and a
companion's own area (section 8), a cut-out turned left for right (section 10, "What scripts
can do"), and words lifted over a face that is in their way (`clear`, section 4). Since round
thirteen: a flock that a script herds into another place, and poses (section 2, "A flock that is
sent somewhere"), a cut-out that rides the water (`bob`, section 2), someone above the floor (a man
at an upper window: section 3), a depth order that holds where bases slant (only things whose
pictures overlap are ordered against each other, and the order is the old one wherever the old
one was right: section 3, "Nearer things cover farther things"), a scene seen through the lead's
own eyes (`unseen` and `wordsAt`, section 8), the storyboard's map of each act's ways (section 8,
"The map"), and the game's emblem on the begin screen and in the browser tab (the Timer, section 9). Since round
sixteen: the world going by a car's side windows, drawn from the scene's camera (`drive`, section 2). <!-- DRIVE-16E -->
Since round fifteen: the map screen, with travel to the places already visited, and switching between
leads through the map, with the Timer turning across the centuries first (section 8, "The map, and the
Timer"). <!-- MAP-15 --> With it, the save's list of the scenes the player has entered (`visited`,
section 6), and each map drawn from its painters' pictures and measurements, or as a sketch until it is
painted. <!-- MAP-15D -->

**Painted:** the highway of the intro and the title, and nineteen scenes: five in Egypt (the
inside of the wagon among them), six in Rome, the five rooms of the house, and in Nevada the
roadside, the store inside and the back of the limousine. Ranger, frame by frame; and the birds
of the Capitol and across the Tiber, the geese and Mariam's hens, frame by frame as the pigeons
are. Thirty-four things to carry. The game's emblem, in nine pictures of the interface's own
(twelve since round fifteen, with the Timer's three pieces at 1024). <!-- MAP-15D --> Since round
fifteen, the four maps of the story, each its own kind of map (section 9, "The maps"): thirty-five
pictures, with their measurements. Since round sixteen, the world outside the limousine's windows for the `drive`:
a sky, each side's far ranges, middle distance and ground, and a sheet of seventeen things beside the road, each in two lights (section 2,
"The world going by a car's side windows"). <!-- DRIVE-16M -->

**Drawn:** thirty-eight people, and twenty-four more states of them (section 4).

**Written:** a prologue and five acts, the fifth only as far as its opening: Egypt, Rome,
home, the Nevada desert, and the limousine of Act Five, whose last card is the end of the
demo. Each part has its puzzle document (the present's has Acts Three and Four and the
opening of Act Five). None of it has been signed off by the author yet: Acts One and Two
were rewritten in October 2026 from his brief, Act Three was remade on 7 October, Act Four
was expanded and Act Five begun on 10 to 12 October, and on 13 October Act Two gained the
bigger Rome's first stage (three places, seven people, three puzzles that each add a step to a
chain he has played, and the heart of the faith thread) and Act One the inside of the wagon;
all of it is waiting to be played.

**Placeholder:** the music, which is synthesized. There are no recorded voices yet.

**Not built yet:**

- Light on people that changes with the scene. Every person is lit from the upper left,
  by lamplight and at noon alike, whatever the light in the painting; only their colors
  follow the scene's paints (section 9).
- More acting. There is no turning between directions (he snaps round), no running for
  the rig's people (Ranger's scamper is painted), no climbing, and faces cannot yet show a
  feeling. Carrying someone is a pose drawn for one moment (two of the backup carrying
  Grandpa Joe), not something anybody can do. The Son cannot sit down: there is no seated
  drawing of him, so across the Tiber he waits for the old man standing.
- Other people going wherever they like. Everyone lives a little by themselves (section 4,
  "Their own lives"), and some walk out and back now and then, but only to the places their
  scene names; nobody wanders unasked.
- Companions who follow the lead about a scene. In a party the others come along from one
  scene to the next, but inside a scene they stay where they were left.
- Close-ups the player can click inside. A close-up is a picture to read, not a
  small scene of its own.
- Scrolling scenes wider than the screen.
- Sound for the things that move by nature (a fountain's splash, the crackle of a brazier), and a startled bird
  landing in another flock's place (the gutter, say). The acts' scenes list their moving things now (section 2).
  (Across the Tiber the river is heard, very softly, but only while the music stops for the old man's talk.)
- Touch polish: larger targets and a bigger inventory on phones.
- Layered music, ambient sound loops, per-scene reverb.
- Translations (the line files are ready for them) and a caption option for sounds.
- Saving in the middle of a conversation. Esc pauses at any time, but Save and Load
  wait until the current moment has played out.
- Painted close-ups. The computer screen, the notice and the office's clipboard are drawn by code.
- The rest of Act Five, and where the family comes out of the door.
- The rest of the bigger Rome: Caesar's house on the Sacred Way and its puzzle, Nine Hundred Senators; the optional
  speakers and the people without lines; Titus at his father's counter; the act's old conversations as trees; the
  Rome end of the letterbox (section 14, and PUZZLES-rome.md, "What comes next").

**Known faults** (round thirteen):

- The storyboard draws Dad, full size, over the bench in the inside of the wagon: it puts
  every scene's leads on their marks, and should leave out the leads of a scene seen through
  the lead's own eyes (one line in `tools/storyboard.html`). The game is not touched by it.
- On the Capitol anyone walking to the goose-keeper, or to the parapet for the view, is
  drawn over the pen's far fence for a moment on the way, since that fence is painted into
  the backdrop (section 14).
- A long line said near the glass can lie across the face of the man in gray, when he
  stands at the far end of the fence (round twelve).
- `tools/paint/install.py --keep-palette` changes pixels nobody repainted (section 9, "The
  paints").

Five faults were mended in the round's third phase (TESTS-13R): two found when the builds
were merged, the storyboard's map of Act One, which laid the inside of the wagon out above
the foot of the pyramid, and a goose's head that showed past an end of the pen's near fence
(section 14, 65 and 72); and three lines that lay across a face, each now set over the
head: a hint said where the boy first stands on the steps (the soothsayer's; section 14,
57), the look at the writing over the snack bar in the street (the keeper's), and the look
at the chest by the treasury's right-hand door (the clerk's).

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
within three pixels of their own paint. A painted lead was read off the screen at two
depths (smaller farther off, in steps of two pixels, turned for the west), by his outline
and by his portrait at 42 pixels; a strip was watched going by, across its seam with no
line, never a pixel outside its windows, parked at speed 0 and at half speed for less
motion. And with the title up and the pictures gathered,
the server was made to refuse every picture: the game was continued, and a scene never
yet shown was entered, with every painting, cut-out and inventory picture in place.
Since round thirteen: geese herded through the gap in a pen and every one inside (watched
in pictures a quarter of a second of game time apart); a boat at the top and the bottom of its bob; a man at an
upper window shown only through it, with the ground under the window free to walk; a
fence and a wall on slanting bases and a post before them, with Dad at 480 places on both sides of them and
every pair whose paint meets judged pixel by pixel against the rule (and the same stage put
on in the reverse order painting the same pixels); every story scene opened in some 4,500
arrangements of its people, painted with the new depth order and the old, and every pair
whose paint meets judged (the new order laid none against the rule; the old, three); and Dad
in a scene seen through his own eyes, not drawn, his words measured at the top middle.
<!-- MAP-15D --> Since round fifteen: the map screen with the world stopped under it (the clock's time,
the lead and two of the proof's people unchanged for a second and a half, nothing saved); the four maps,
as sketches, on two of each act's saved games, what is drawn, faint and absent read against the save;
travel watched on the map (every place the portrait was seen lies on the ways it walked, at 216 to 219
pixels a second, the whole trip never over two and a half seconds) and arriving on the way's mark, the
scene told where the lead came from; the Timer's notches counted by their clicks, and its bow read at
the angle of the stop it ends on; the switch dropping into the other's scene with no tunnel and no card, and Esc going
back with nothing changed; and a painted map drawn from stand-in pictures. Then, once the four
paintings were in (in a throw-away copy, DOCS-15), each was opened in the game on the saved games of its
act: every name inside its box as the browser draws it, the Timer laying its 1024 pieces, and nothing
said in the console. <!-- DRIVE-16E --> Since round sixteen: the world going by a car's side windows read off
the screen in the proof's car: a marker at a known distance out and ahead found where the projection puts it and at its
size there, to half a pixel, near and far; stripes along the road on lines through the vanishing point; a post followed out
of the far end of a window and out at its near edge, always further out, larger and quicker; each band's ridges a second on
where the projection carries them, as its distance says; a band hiding the ground beyond it and not a pixel nearer; no seam
in a ground or a band of one colour with their seams in view; parked, half speed and streaks; the far ground and the bands
from one picture to the next with no shimmer; and the limousine with the painter's pictures (<!-- DRIVE-16M --> the engine's
stand-ins until the merge), its two sides different and going outward, slowed to a stop by its ending's way. <!-- DRIVE-16F -->
Since the round's fix, the things' shadows: a marker's shadow read back from the pixels where the sun puts it on each side
of the road, every column's middle on its line to half a pixel, as thick as the marker is wide, the ground multiplied by the
shade; far off no thinner than the least the engine draws; still on the ground in the pane when its marker has gone past
the edge; none at all without a sun; and the limousine's things on the painter's sun, its sheet painting no shadow.

**How the acts were tested.** Each act has two checks of its own. One is a script that
plays the act in the real game by real mouse clicks on the real clickable areas (walk,
look, use, a carried thing on a target, a choice of what to say, the Hint button), more
than one way round where the puzzles allow it, and fails on any error in the browser's
console: Egypt in 349 clicks (the three reflectors in two orders), Rome in 268 (its
three chains in two orders), the living room in 191 (each of the three trying every
job), the Nevada roadside as it was before round twelve in 209 (a different one of them
flashing the coin each time), and the opening movie and the title watched at two sizes.
The other reads the act's files against one another and against the painters'
measurements: every line a scene uses exists and every line written is used, every
beat's fact is set by some script, every thing given is in the list of things, every
place someone is sent to stand can be walked to, and every number that differs from the
painter's `layout.json` is a difference somebody meant, with its reason. Like the
engine's test, these scripts were written beside the game and are not in the repository
yet.

Round twelve's three parts were each built with a play of its own, and all three were run
again on the merged game: the roadside in 357, 74 and 63 clicks (a different one of the
three holding the coin at the walk through each time), the store in 263 and 12, and the
cut-scene "Backup" and the limousine in 102 (watched, and Act Five the long way round) and
21 (skipped, and the short way). Since then the act's own play and check were rewritten for
the act as it is, and every one of them finds nothing wrong on the game as it is now.

Round thirteen's two builds were tested the same way. The car's inside is in Act One's own
play, which now goes in by the window and by the wagon and out by the door and the bottom
edge, looks at all fifteen things in the car and uses each (371 clicks one way round and 81
the other), and in its check (five scenes, every line of the act said in its dry run). The
bigger Rome's three parts were each built with a play of its own: the Forum and the steps
in 233 clicks, the Capitol and the street in eight ways (the keeper first, the Capitol
first, the old act's saved games, less motion), and across the Tiber and the treasury in
five (107, 32, 26, 27 and 22 clicks; every one of the part's 210 lines said). All of them
find nothing wrong on the game with both builds merged. Act Two's own play and check were
then rewritten for the act as it is (the round's third phase, TESTS-13R): the play goes
four ways round by real clicks (the design's order; the coin first; leaving the Tiber
without waiting, with every wrong try; and the old act's saved games played on), 1011
clicks and 133 pictures, and with the three part plays it says 1084 of the act's 1085 lines
(the one not said is the look at Juno Moneta's temple, which is not painted); the check
reads the six scenes, the seven talks, every way at the edges and the five verses, and
finds nothing wrong. Then every check and play there is ran again on the final game: every
check clean, every play without a problem, and the engine's test passing all 512 of its
checks.

<!-- MAP-15D -->
Round fifteen changed two ways out, across the Tiber the bridge and in the store the front door:
what each did as the lead left is done by the scene's `leaving` now. So the plays of those two
parts were run again on the engine with the map: across the Tiber all 210 of the part's lines
said, and its record of every way and every fact byte for byte what it was; in the store all
246, going out of the front door and in again five times. The house's play (814 clicks) and the
limousine's (all 148 lines) were run again too, every one without a problem; and the four acts'
checks give exactly what they gave before the round (Rome's once its own stand-in for the
engine runs a scene's `leaving` in its `goto`, as the engine does now: one line in
`check-rome.mjs`).

<!-- MAP-15T -->
Then the round's testers took the merged game as a whole. They made the testers' saved games again from the four acts'
plays, each without a problem: every one carries the scenes its play had entered, and Dad and the Son stand where the story
left them (section 6, "Testing: parts"). The engine test's part `map` now checks the rule for a save from before the map on
saves made so (a saved game with its list taken out), and that a save of this version keeps its own. A new play beside the
others, `map-sweep.py`, plays the map through all 58 saved games by real clicks: every place the map offers, there and back,
each from a fresh load (103 places), checking where the lead and the party arrive, the save and the console; the limousine's
refusals; a click on every portrait on every map the player knows; and less motion, with the game's own setting ticked in
Options. It found nothing wrong. Then every check and play there is ran again on the final game, the sweep with them: every
check clean, every play without a problem, the engine's test passing all 630 of its quick checks (688 in the full run), and
the intro's watch and the emblem's check passing.

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
| Play as someone else | Click their portrait (someone in another scene: their map comes up, with the Timer first across the centuries; click them on it) | Tap their portrait | 1, 2, 3 (then Enter, for someone in another scene) |
| Talk to a companion | Click them | Tap them | Tab to them, Enter |
| Give a companion something | Click the thing, then click them or their portrait | Tap the thing, then tap them or their portrait | |
| Next line | Click | Tap | Space or Enter |
| Pick a reply | Click it | Tap it | Number keys |
| Skip a cutscene | **Skip** | **Skip** | Esc |
| Menu | **Menu** | **Menu** | Esc |
| Show what can be clicked (an outline round each thing, an arrow at each way out) | **Show** | **Show** | Hold H |
| See the map, go back to a place already visited, play as someone elsewhere (MAP-15) | **Map**, then click the place or the portrait (a map's name at the top, or the dial, turns to another map) <!-- MAP-15D --> | **Map**, then tap | M; Tab and Enter; Left and Right for the other maps; M or Esc to put it away |
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
5. **The leads:** free switching, alternating chapters, or a mix. At present the story
   decides when to cut from one half of the family to the other, and from the family to
   Grandpa Joe and Ranger; Mom and the girls can be switched between at any time, and so
   can Grandpa Joe and Ranger.
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
11. **Who the leads are.** [CHARACTERS.md](CHARACTERS.md) describes all seven. Nobody in
    the family has a name yet: on screen they are Dad, Son, Mom, Big Sister and Little
    Sister. Grandpa Joe and Ranger are named.
12. **Where the present-day chapter goes.** It plays after Rome. It could open the game
    instead, or be cut in between the scenes in the past.
13. **The puzzles.** The three puzzle documents lay them out so they are easy to change.
14. **Big Sister's facts.** Every fact she states has to be true. The list, and which
    of them have been checked against a source, is at the end of CHARACTERS.md.

**From round twelve** (Nevada expanded, and Act Five begun, 10 to 12 October). Where the
design left something open, or could not be built as written, the builders chose; each is
yours to keep or change, and says what the game does meanwhile. The puzzle document
(PUZZLES-the-present.md) tells each where it happens.

15. **Grandpa Joe's rocking chair** stands on the ground in front of the porch, where the
    lawn chair stood; the design put it up on the porch boards. To move it, the scene changes
    his place and his area; nothing in his drawing changes.
16. **Where Ranger sits.** On the ground beside the chair, as the scene draws him; Mom's look at him
    (`nevada.ranger.look.mom`) now says so ("A raccoon beside the chair..."). If he should ride on the chair's
    arm, as the design had him, the scene moves his place and the line goes back.
17. **Mom's car is painted teal**, so her lines now say "a sensible teal sedan" (`nevada.car.sedan`,
    `nevada.shade.car.mom.1`), and her third guess at Dad's car is "A gray car with dark windows." (the
    gray suits drive a gray limousine). If the car should be silver, it is repainted and the lines go back.
18. **#6 is read at the trade.** Big Sister reads the coin the moment Ranger puts it in her
    hand (#10): a carried thing's look cannot call the scene. So Mom's two lines for a coin
    nobody has read (`nevada.talk.mom.bigsis.coin.*`) and the three hints of the beat
    `nevada.coin` are never heard. For the read to wait for a look, the coin's look in
    `world.js` would have to call the scene.
19. **The banjo's flash** comes off the chrome pegs at the end of its neck (he hides the
    white head himself). Meanwhile, the pegs.
20. **The wide door** is a second door in time over the coin's, drawn over the sun shade he
    holds and bending it with the sand, so that the whole doorway shows; the banjo's door is
    the same, round, at a third of the size.
21. **Where they stand for #9:** the two who are not holding the coin watch from a row
    further back than the design's, because Grandpa Joe sits behind the front row.
22. **Jolene's hat** goes round the five, one a visit, and the visit is counted as the store
    is built, so that her hat is right from the first picture.
23. **The sun shade** is lifted out of the window by Jolene, who comes out from behind the
    counter, and whoever asked comes to meet her. The asker taking it down would be shorter.
24. **The pay phone.** Jolene says her two lines at the phone and reaches toward it: there
    is no pose with the receiver at her ear.
25. **The egg.** Little Sister hops down into the yard for it, and back onto the step: from
    the step it was out of her reach.
26. **Mom's dollar in the dish** on the way out (the design's) has no line, and is not done.
27. **The first look round the store is talky:** Jolene has a word after eleven of the
    things, once each.
28. **The hens in "Backup"** are a close look, drawn from the store's own pictures at two
    and a half times their size, over the lot for three seconds; the cut-scene does not go
    into the store.
29. **The limousine has no pictures with its doors open.** The four suits step out from
    behind it, and get in by stepping behind it. Its plate (O.O.P.S.) is hidden behind Mom's
    car while it stands, and reads backwards as it drives out (it is drawn mirrored). A view
    from behind would show the plate best; none was painted.
30. **The carry:** two of the backup carry Grandpa Joe upright between them, not laid
    across them like a sofa. Jolene has no spatula, and there is no knitting pose.
31. **The four suits share one color** for their words (`#abc8ed`), as the three haulers
    do. Each could have his own.
32. **Grandpa Joe never walks in the limousine,** loose or tied (the seatbelt stays on), so
    Ranger fetches across the car what he wants, and eats the pickle on the way.
33. **The looks at the map and the receipt** are written and not heard in the demo: both
    come into his pocket in #15's last script, which runs on to the card and the title.
34. **Jolene's four facts are new** (a hen has teeth; a raccoon has a pocket; a good hen
    lays one on the hour; the rooster lays on Tuesdays): the design's could each be true by
    accident. So Big Sister's goodbye at the door is about the egg, and not "A hen cannot
    count to five."
35. **Through the coin door the menus are the Son's lines:** the player chooses what he
    says, and the family answer.
36. **Jed's name** is heard once before "Backup", in his earpiece; Jolene calls him "the
    gray fella", and the card on her board that says JED is not read aloud.
37. **Big Sister's "Non, merci. Nein, danke."** is written from knowledge, and not yet
    checked against a source.
38. **Houston** is Houston Pruitt in the design, thirty-one years in dispatch; nobody in the
    game says her surname or her years, and she has one line.
39. **Jolene's spare hat,** on the nail in the porch post (straw, with a blue scarf),
    matches none of her five.

**From round thirteen** (the bigger Rome's first stage, and the inside of the wagon, 13
October). The changes to puzzles you have played are listed plainly in the puzzle documents
(PUZZLES-rome.md, "What changes in the act he has played"; PUZZLES-egypt.md, "Round thirteen":
the one change in Act One, the glovebox inside the wagon, is your own request of 8 October).
Each of these is yours to keep or change, and says what the game does meanwhile. First the
questions the round's plans left open:

40. **The senator moves to Caesar's door** (the design's proposal; held). It would move #2,
    Deliver It, which you have played, to a new place behind a new gate. So the senator stays
    on the temple steps, and with the move wait Caesar's house on the Sacred Way (`rome-house`,
    off the Forum's bottom edge, which is plain floor meanwhile), its porter Anteros, the
    callers, the lictors and the litter, the maid Doris and her whispers, the design's first
    new puzzle, Nine Hundred Senators, and the keeper's knowing the senator's three names. It
    is asked again now that you can play this stage.
41. **The optional speakers.** Seven of the design's fifteen new speakers are built, the ones
    the puzzles and the faith thread need. Diodorus (the Capitol's guide), Paetus the
    moneychanger, Demetrius, Vibius and Petosiris wait, and with the house its porter, Doris
    and the lictor; their places are painted and left clear (the moneychanger's table waits
    under its awning in the Forum), and nothing only they would say is said (the Egyptian
    queen, as gossip, waits with two of them). The people without lines wait too (the
    revellers going to Anna Perenna's feast, the nurse and child, the builders, the tutor and
    his boy, the woman at the well), so the Forum has no passers-by and the Gaul asks the air.
42. **The A.D. chapter** (A.D. 60, played by the Son): the direction is taken for the plan
    (`briefs/out/ad-way-plan.md`); nothing of it is built.
43. **The act's old conversations as trees.** The doorkeeper, the keeper, the washerwoman, the
    senator, Walnut, the soothsayer, the clerk and the date seller still talk in the flat
    menus they had, with the few options this stage needed added. Rewriting them as trees
    waits for your review of the puzzles.
44. **The car's two small additions**, each a picture and a few lines, if you want them once
    you have played it: the driver's door seen swinging open as Dad gets in and out
    (meanwhile the picture fades, and the door is never seen open), and a close-up of Little
    Sister's drawing behind the visor (meanwhile it is painted at the size the visor shows
    it).
45. **A map screen?** Your words of 10 October: "remember to... incorporate the expanded parts
    of the levels into the map as well". The game has no map the player opens. The new places
    join the old by ways at the edges of the pictures (the steps' bottom edge into the Forum,
    their right edge up to the Capitol, the Forum's left edge down the Tuscan street and over
    the river, and each way back), and the storyboard page draws each act's ways as a map,
    from the scenes' own data (section 8, "The map"). Do you want an in-game map screen? It
    would be a new feature, for a round of its own.
    <!-- MAP-15D --> **Answered** on 14 October: by "the map" you meant the scene edges for the
    expanded parts (as round thirteen built them), and you asked for a map screen besides, with
    the dial for switching between leads. Built in round fifteen (section 8, "The map, and the
    Timer"); what its builders chose is 74 to 86, below.

Then what the builders chose, where the design left a choice open or could not be built as
written. **The inside of the wagon:**

46. **Standing at the wagon's door, Dad covers the rolled-down window while he looks in.** He
    stands at the brief's fixed place (642, 563), at his door, and the window is about 40
    pixels wide; the player sees it before he walks up, and again when he steps away. To move
    him (to the left of the window, say) the fixed measurements change: say if you want it.
47. **What the window shows.** At 36 by 27 pixels: daylight from the far windows along its
    top, the bench's back and the headrest, the top of the wheel. The dashboard and the
    windshield's edge that the design wanted there are behind the door's front edge from
    where the river is seen, and two small cheats make the daylight and the wheel read.
48. **The steam through the windshield** reads as a thin, slightly beaded thread of small
    puffs rising off the hood, kept as the painter marked it; a higher rate would make it one
    continuous wisp.
49. **The dust** drifting in the sun over the Son's seat barely shows, as the painter said it
    would. It is kept, being the painter's.
50. **The glovebox checks for the map first**: looked at, it says the map is in there only
    while it is, so an old save that already has the map never hears "The map's in there"
    (it hears "Nothing left in there but ketchup packets. I'm saving those.").
51. **The horn's second honk** says "There's a man sitting quietly out there.", where the
    design said "praying": the act's check holds every line of Dad's that speaks of prayer to
    the family's faith, and nothing in the car is that. If you want "praying", the check takes
    the line and it reads as designed.
52. **The horn** is a little quieter than the design's (0.06 for 0.08), so that it does not
    stand out over the car's other sounds, and it dies away over its half second rather than
    holding the note: a held honk is a one-line change in `sound.js`.
53. **A hidden speaker's words.** In a scene seen through the lead's own eyes anyone not drawn
    speaks from the top middle (or the scene's `wordsAt`); everywhere else a speaker a script
    has hidden still speaks from where he is, because two scenes rely on it (Little Sister in
    the closet, Grandpa Joe inside the limousine in "Backup"). To make the rule general is a
    line in each of those scripts and two in the engine.

**The Forum and the steps:**

54. **A look at the hill or the Forum from the steps walks the boy to that edge first**, and
    he says the look there: each half of the far view is the same way as its edge. For him to
    look from where he stands, the two areas lose their walk, and only a click walks him.
55. **The senator holds up the Gaul's toga with an empty hand**, and holds out an empty hand
    to give it back, because the people's rig has no toga to put in it. A folded toga drawn in
    a hand would mend it.
56. **Phyllis gives her leave with no gesture**: a short pause, and the boy's line (the rig
    has no hand closing over a coin, and no nod for someone seated).
57. **Hints spoken at the steps' arrival mark sat six pixels over the soothsayer's face.** It
    came from the old act's layout. Mended in the round's third phase (TESTS-13R): words said
    there now go over his head.
58. **The Forum's far end is told shorter than it is** (some 60 metres to Saturn's steps, not
    150 or more), so that the boy arriving there is his true size beside his temple; a bigger
    boy there would mean arriving nearer us. And **the senate house's site is brought
    forward**, before the near end of the basilica of Paullus rather than beyond it, so that
    the Gaul is 80 pixels tall and his short toga reads.
59. **The pigeons in the Forum are clicked one by one**, as on the steps: the painter's one
    area for them lay over the middle of the square, where a click meant to walk would have
    chased pigeons.

**The Capitol and the street:**

60. **The goose-keeper stands 21 pixels back from the painter's mark**, at [146, 437]: at the
    mark he stood on the pen's far fence, which is painted into the backdrop. So he does not
    walk out among the geese round the base, and anyone walking to him (or to the parapet
    for the view) crosses that fence for a moment on the way. Cutting the far fence out as a
    picture of its own would mend all of it.
61. **Juno Moneta's temple is not painted** on the Capitol (it would stand behind the
    temple's right side, which runs out of the picture), so the Son's look at it,
    `rome.capitol.moneta.look`, is never said. The goose-keeper still talks of Moneta, and the
    Forum shows her temple on the hill. Painting her, or letting the line go, is yours.
62. **The Capitol as painted**: the temple stands far back across a deep precinct (so that its
    pediment and the chariot on its roof show), the dictator's chariot is to the right of the
    altar, not its left, and the precinct's portico is left out (the parapet is its west side,
    with the view over it).
63. **Speech is now lifted over three faces** (`clear`): Titus's and the goose-keeper's on the
    Capitol, and the date seller's in the street, whose face Walnut's long new tips and the
    wish at the fountain would cross; so words near the date seller sit higher in the street
    than they did.
64. **The geese, Titus and the goose-keeper, as staged.** The geese's verb is "Shoo"; until
    the stomp they mostly stand and look, after it they mostly peck. Titus hops down, walks to
    the boy for the hand-over, and runs out past him at the bottom. He is small up there
    (about 67 pixels): bringing the row of kings forward would make him read better. The
    goose-keeper talks with his head only, his hands full of basket and stick; letting the
    stick go would let him gesture as he tells the tale.
65. **A goose's head poked past an end of the pen's near fence**, as the Capitol was built
    (looking about, standing or pecking: up to 25 pixels past it). The round's third phase
    (TESTS-13R) mended it by drawing the pen's inside in from both ends of the near fence, by
    the most a goose reaches out in front of or behind its feet: no goose shows past the fence
    now, and the six keep to a smaller pen (72 pixels across at the front, where it was 108).

**Across the Tiber and the treasury:**

66. **The Son cannot sit.** There is no seated drawing of him, so he waits for the old man
    standing at the bench's near end, while two lines offer a seat he never takes: his own
    "I'll sit. Sitting is the main part of waiting." and the old man's "Sit, child, if you
    like. The bench is long." A seated drawing of the Son, or a word changed, would mend it.
67. **The window figure prays through his standing pose**, not by being told to pray, so that
    his head still lifts and his lips move now and then at the window (told to pray, he would
    look the same, and stand quite still).
68. **The boy steps aside as the old man comes out** of his door, out of his way to the bench
    (the painter's place for the boy to wait is on it).
69. **Felix is talked to from [144, 466]**, a step east of the painter's places round him, so
    that the bollard does not hide the boy's feet.
70. **The river sound is very soft** at the brief's level, heard only because the music has
    just stopped. If it should be heard plainly, its level goes up.
71. **Sizes.** Mariam is about 70 pixels tall in her yard, not the design's 87, and the old man
    at his window about 90, not 105: the painter's camera sees the yard and the window further
    off than the design reckoned.

**The lines** (where they leave the design, and why): the Gaul's joke is a notice put up, not
writing on the walls (Suetonius says a placard); the Son answers Numbers 6:25 with "Back home
we get all three parts. I know them by HEART.", not the design's "the blessing Pastor says at
the end of church", since he says no Christian word to the old man but "Is that your church?"
(the echo of the date seller's scene is one line to put back, `rome.eleazar.bless.son`);
Felix's Corinth is "a city with a sea on each side"; the boy is "a boy in strange shoes", not
in a cap; with no Egyptian in this stage, the old man's "Greeks. Egyptians. Gauls. Romans."
looks over the river at the city, and Moneta's money is the goose-keeper's; Felix promises the
ninth hour (it is in six lines, if you would rather another); and there are two Tituses, the
keeper's boy and the goose-keeper, who is called Anser but for his full name, said once.

**The rest:**

72. **The storyboard's map of Act One** laid the inside of the wagon out above the foot of the
    pyramid, its two ways to the river one long curve across it, and the label "Go out of the
    wagon" half under the gallery's picture. The round's third phase (TESTS-13R) mended it in
    `tools/storyboard.html` (section 8, "The map"): the wagon's inside now lies left of the
    pyramid's foot, a short straight line from the river, every label clear, and the other
    acts' maps are the same pictures as before. The game is not touched by it.
73. **The emblem keeps turning** while the begin screen is up, A to B.C. and back, notch by
    notch, as you saw it on the review page. It could instead turn once, A to B.C., when Begin
    is pressed, which would hold the begin screen up for about four seconds after the click.

<!-- MAP-15D: the decisions of round fifteen, 74 to 86 -->
**From round fifteen** (the map, and the Timer, 14 October). You chose the switch, the Map button
and each time's own kind of map (section 8, "The map, and the Timer"; section 9, "The maps").
Where that left something open, the builders chose; each is yours to keep or change, and says what
the game does meanwhile. Nothing in the story changed. The one you are most likely to want to see
first is 74; then the four maps themselves, 82 to 85.

74. **The switch across the centuries is seen only in the proof, for now.** No act has the team in
    two times at once yet (Dad and the Son each play their act alone), so in the story the Timer
    turns only as you look from one map to another. To see the switch you chose, Timer and then
    map, open `index.html?scene=engine-proof&lead=dad&flags=proof.letterbox,proof.arrived` and
    press the key 2. It comes into the story with Round One's step (Act Six in
    `briefs/out/story-redesign.md`: Dad and the Son at their doors), and needs nothing more of the
    engine.
75. **After the Timer, a click drops you in**, as you chose: the other's map comes up with their
    portrait breathing, and a click on them (or Enter) drops into their scene; Esc goes back. The
    other way is to drop in by itself after a beat, Esc still able to stop it: a few lines in
    `switchTo` (`js/engine/atlas.js`).
76. **Travel is a shortcut, back and never ahead.** A click on a place already visited takes the
    lead there along the ways, where Act One's design said "There is no map and no shortcut"
    (PUZZLES-egypt.md now says so). A place is there to go to only once it has been walked into,
    so the map passes no gate (the guard, the doorkeeper, the study's key, "Snacks first"). For
    less of it (only to the next place, say, or none in Act One), a rule in `cannot` in
    `atlas.js`; with none at all, the map only shows.
77. **Who is on a map.** Leads not on the team are shown where they stand, smaller and faded, not
    to be clicked ("Dad is here. Not playable just now."). A place where one of the team stands
    counts as visited. Grandpa Joe and Ranger have no portrait at the Last Stop in Act Four, where
    they are its people (and a pin has room for three). To hide the faded ones, or show those two
    in Act Four, is a line in `facesOn` in `atlas.js`.
78. **The place names are the engine's**, written over each painting in Koine Road in the map's
    own style (ink-brown on the papyrus, pale capitals on the wax, pencil grey on the plan, printed
    capitals on the road map), not painted: they come and go with their places and read at any
    size. Painted names would be truer to each hand (a scribe's letters, a stylus's), and would
    need a picture for each name, laid with its place, and the engine's names off for that map.
79. **Old saves show a few places faint.** A save from before the map is given its list of places
    visited from the story's facts (section 6), so a place that is no beat's (Little Sister's room)
    or whose beat is not done yet (the store before the hens, the Capitol before the geese) is faint
    on it until walked into again, even if the player had been there. A game started now counts
    every scene as it is entered; the testers' saved games carry the list, as their plays played it, since
    they were made again on 14 October. <!-- MAP-15T: it said they "will carry the list when next made" -->
80. **The three new sounds were set by measuring, not by ear**: the dial's click (`notch`) quieter
    than the vault's dial, the bell (`ding`) and the paper (`rustle`) no louder than picking a thing
    up. They want listening to; each is a line in `js/content/sound.js`.
81. **The place name at the top of the screen is narrower** (from 26% to 66% of the stage's width,
    to 23% to 59%), to make room for the fifth tool, Map. The longest, "The steps of the temple of
    Saturn", still fits. Wider again would mean smaller tools, or the name on a line of its own
    (`.place` in `css/game.css`).
82. **Egypt's map.** Black ink and red, as designed, and thin washes besides where a scribe's brush
    would lay them (the river, the palms, the red wagon, the king's gold, the lotus), to help a
    child find each place: `pen.wash` in `tools/paint/map_egypt_things.py`, easy to take out. The
    pyramid is drawn side-on, in section, from the river, its gallery steeper than true and its
    chamber larger, so that both read with a portrait on them: the game's layout, not the real
    pyramid's. Two portraits at the gallery at once (rare) put one over the doorway, which is the
    site's; the wagon has all four wheels in a row (the scribe's "neat, a little wrong").
83. **Rome's map.** The Capitol is to the right of Saturn's steps, as the act's ways put it (it is
    the steps' right edge); in Rome it rises behind the temple. The hill's rings run off the
    tablet's edges; across the Tiber is the tightest corner (one portrait, as in Act Two, leaves
    its little square readable; two cover it); the frame's honey wood is the brightest thing at the
    edge of the dark screen (`WOOD` and `WOOD_LIGHT` in `map_rome_kit.py` tone it down); and the
    names are 15 pixels, since at 16 "Saturn's steps" would reach the hill's rings.
84. **The house's map.** It is turned half round, as plans usually are (the street at the bottom),
    so each room faces the other way from its picture (the living room's stairs are on the right
    of its plan); that lets Dad's arrow run straight from the stairs to the landing, and the ladder
    straight up to the attic. The five rooms' models do not fit together as one house, so the
    joins are invented (a passage to Little Sister's door, a lobby inside the study's, the study
    over a covered porch, the Son's room, the ground floor's back rooms), every room at its true
    size. No sofa (the scene has none); two sizes are guesses (the Retreat's length, the Son's room);
    and the rows of portraits are big for these rooms, covering a room's middle when all three are
    in it.
85. **Nevada's map.** Its printed jokes are the act's own; please confirm them: "TO NOTHING", LAST
    GAS printed as a town, "37 MI.", the legend's "No gas", "DETAIL · 37 MILES PAST LAST GAS", "NOT
    TO SCALE"; no real company, publisher or highway number, and no place but NEVADA. The store is
    drawn inside the shack's walls in the detail (not as a plan beside the lot), turned as the
    shack stands, so the shop's door is one short arrow. The limousine's stretch of road is east of
    the Last Stop, toward NOTHING; if it drove back west, the way it came, the stretch moves to the
    other side of the No Gas sign. Mom's car is printed blue-grey (the inks have no green), and
    three portraits in the store cover its front third.
86. **The Timer at its very largest** (DIAL-15). Where the large dial is drawn 1,600 or more device
    pixels across, the 1024 is itself enlarged and the cream rim's edges show faint steps (much
    smaller than the 512's would). Its edges are hard because the drawing is the emblem's own, at
    twice the size; drawing them soft is a small change to the drawing. The scripts that make the
    emblem are kept beside the game (`scratchpad/work-map-dial/emblem/`), not in it; they could go
    into the repository with the painter's.
87. **The sun outside the limousine** is the roadside's morning, a few miles on: low on the car's right and a little
    behind it. So the left windows are bright and warm, their shadows lying away from the road, and the right ones look
    toward the light (shaded faces with bright rims, a paler sky low down), their shadows toward the road. If the limousine
    drives east into the morning, as Nevada's map has it (toward NOTHING), the sun would be ahead: every picture relit, and
    the shadows along the road, which reads less well than across it (`tools/paint/nevada_limo_drive_kit.py`). <!-- DRIVE-16M -->
88. **The telephone line stands far out, with its wires.** The side glass sees no higher than about 1.8 m plus a tenth of
    the distance out, so a line beside the road (14 m) would show only its poles' feet flicking past; with its crossarms and
    sagging wires in view it must stand far out, where the poles are small. It is 70 m out on the right (`every: 55, at:
    70`); the other way is `at: 14`. The camera cannot give both. <!-- DRIVE-16M -->
89. **The ground repeats every 64 m** (four seconds at 36 mph), so it is kept free of anything to remember, and the
    landmarks are the things the engine places, which never repeat. A wash or a cattle guard crossing the road would need
    a longer ground picture (2048 pixels wide is 128 m) or a picture of its own. <!-- DRIVE-16M -->
90. **The far hills on the right are at 0.14 pixels a metre**, where the brief said 0.07: "nearer, lower hills" at 0.07
    would be drawn up to twice their painted size, with blocky pixels. They stand 3000 m out, the left side's ranges 6000;
    the middle distance 850 m (each band is at its own size at the near pane's outer edge). <!-- DRIVE-16M -->
91. **The limousine's folder is now 1.4 MB** (the nine new files 770 KB, the two grounds 600 KB of it; it was 0.65 MB,
    and the next largest scene is the roadside's, 0.55 MB). The old strip (`desert-strip.png`, 210 KB) is no longer shown
    but stays, since the painting kit's limousine scripts read it; taking it out of the game saves that. <!-- DRIVE-16M -->
92. **The things' painted shadows lie as bars near the car.** Each upright thing has its long morning shadow painted along
    its bottom rows, three rows (12 cm) thick in the side view. Far off that is right, but near the car (the fence posts,
    the signs) a shadow on the ground would be foreshortened to a pixel or so, and it shows as a brown bar 3 to 6 pixels
    thick; the shadow of a post just past a pane's near edge lies in the pane by itself. Shadows one row thick on the sheet,
    or the engine squashing a thing's shadow rows by how far below the eye they lie, would mend it. <!-- DRIVE-16M -->
    Mended in the round's fix (FIX-16): the sheet is painted without shadows, and the engine lays each thing's shadow on
    the ground in perspective (the drive's `sun`, section 2, "The things' shadows"); no bar stands in the air, and every
    post and bush stands on its shadow. <!-- DRIVE-16F -->
93. **What stands beside the road is the scene's to choose** (the rows in `nevada-limo.js`): an OPEN RANGE sign every 600
    to 1300 m on the right and the backs of the oncoming lane's signs as often on the left (a sign about every half
    minute, one side or the other); one NEXT SERVICES 112 MI sign about 18 s in (and nine kilometres on); a mile marker
    every mile (its plate says MILE 41 every time); and a Joshua tree on each side every 80 to 240 m, though the roadside
    a few miles back has none. Fewer, more, or none is a number in a row. <!-- DRIVE-16M -->

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
