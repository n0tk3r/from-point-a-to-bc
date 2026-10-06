# From Point A to B.C.: how the game is built

This is the design of the game's engine and its look. It answers eight questions:

1. [What kinds of animation can a browser game use, and which do we use?](#1-animation)
2. [How are the characters drawn, and how does a flat picture get its depth?](#2-characters-and-depth)
3. [How do intro movies work, and how do they lead into the title?](#3-intro-movies-and-cutscenes)
4. [How do saved games work?](#4-saved-games)
5. [How do music, sound and dialogue work, and how do we get to full voices?](#5-sound-music-and-dialogue)
6. [How is the story kept guided without being a straight line?](#6-story-guided-but-not-a-straight-line)
7. [How does one look hold across every time period?](#7-one-look-across-every-era)
8. [How do I add a scene, a character, a line, an era?](#8-how-to-add-things)

It ends with [the controls](#10-controls) and [the decisions that are yours to make](#11-decisions-waiting-for-you).

Everything described here is working code in this repository. The story in it is a
placeholder: a prologue and four short acts written to exercise each part. See
[what is real and what is placeholder](#9-what-is-real-and-what-is-placeholder).

Two companion documents: [CHARACTERS.md](CHARACTERS.md) says who the five members of
the family are and how each of them talks, and [PUZZLES-the-present.md](PUZZLES-the-present.md)
maps the present-day chapter puzzle by puzzle.

## The short version

| Question | Decision | Why |
| --- | --- | --- |
| Engine | Plain JavaScript modules, no framework, no build step | GitHub Pages serves the files as they are. Nothing to install, nothing to break. |
| Picture | Pixel art on a 640x400 grid, scaled to fit any screen | Four times the pixels of the classic 320x200 adventure screen, so people have faces and clothes have patterns. Still no picture files to download. |
| Characters | Drawn by a jointed figure from a page of settings, not stored as pictures | One description gives all eight directions, every animation and every size. See section 2. |
| Depth | People and props are painted back to front by where they touch the ground, and shrink toward the horizon | The lead walks behind the car, in front of it and round it, with no hand-made mask per scene. See section 2. |
| Movement | One game clock drives anything that matters to the game. CSS runs only the glow of time travel and a few ambient loops. | Each tool does the job it is best at. See section 1. |
| Intro movie | A script that moves the game's own art. Not a video file. | About 3 KB instead of tens of MB, identical in style to the game, skippable, subtitled. |
| Saves | Autosave and three slots in the browser, plus a save file the player can download and load anywhere | Browser storage can be wiped. A file is the player's own. |
| Sound | Web Audio with separate volume for music, effects and voices | Standard, works everywhere, lets music duck under speech. |
| Dialogue | Every line has an ID. Text now, a sound file with the same name later. | Voices can be added one line at a time without touching any script. |
| Story | Acts and beats listed as data, with a checker and a storyboard page | Parallel puzzle chains inside an act, one gate at the end of it. |
| Leads | Five people the player can control. Apart, each has a scene of their own. Together, the player switches between them with their portraits. | A father and son lost in different centuries, and a mother and two daughters working as a team. See section 6. |
| Look | Three groups of color that never mix, one light, one drawing kit, one typeface | Each era changes the palette, never the rules. |

Size today: the whole game is 32 files, about 350 KB of code (120 KB when the server
compresses it) plus a 49 KB font. There are no picture files at all: every character,
prop and backdrop is drawn by code when it is needed. In a test browser it held 60
frames per second, and a full-size character took between one and two thousandths of a
second to draw.

## Where things are

```
index.html              the page: one stage, a stack of layers
css/tokens.css          colors and type: the time layer, the era palettes
css/game.css            layout and interface
js/main.js              gathers the content and starts the engine
js/engine/              the engine. Knows nothing about this story.
  clock.js                the game clock: wait, tween, pause, skip
  state.js                the data a save file holds
  save.js                 slots, export to a file, import from a file
  audio.js                music, effects, voices
  dialogue.js             spoken lines and choices
  scene.js                the stage: backdrop, glow layer, clickable areas
  cast.js                 people and props: depth order, animation, the store of finished pictures
  walk.js                 where the lead can stand, routes round obstacles, size by distance
  fx.js                   canvas effects (the time tunnel)
  story.js                reads the story data: open beats, checks
  ui.js                   heads-up display and menus
  game.js                 ties it together; the `g` that scripts use
js/art/                 everything that draws
  kit.js                  backdrops (skies, ground, river, temple, a living room, a desert lot), the portal, close-ups, item icons
  pix.js                  the pixel renderer: solid shapes in, pixel art out
  rig.js                  the jointed figure: poses, eight directions, the walk, stances and gestures
  people.js               the cast as the rig sees them: proportions, clothes, colors, and how each one stands, walks and talks
  props.js                things that stand on the ground: wagon, fountain, reeds, furniture, a car, a lemonade stand
js/content/             the game itself. Knows nothing about the engine's insides.
  world.js                cast, eras, items
  lines.en.js             every spoken line
  story.js                acts and beats (the storyboard)
  sound.js                music, effects and the list of recorded lines
  cutscenes/intro.js      the intro movie
  scenes/index.js         the list of scenes
  scenes/*.js             one file per scene, fetched when the player first gets there
  scenes/sketch-example.js  a scene with no art yet, to show storyboarding
tools/storyboard.html   the story, drawn out, straight from the data
tools/sprites.html      every character and prop, moving, in every direction
docs/DESIGN.md          this file
docs/CHARACTERS.md      the character bible: who the family are and how they talk
docs/PUZZLES-the-present.md   the present-day chapter as a puzzle document
```

To run it on your computer: `python3 -m http.server` in this folder, then open
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
| SVG | Vector drawings in the page, styled by CSS | Flat-color art, recoloring by era, sharpness at any size, clickable shapes | Hundreds of moving parts at once. |
| Sprite sheets | A strip of frames, stepped through with `steps()` or by a clock | Hand-drawn character animation | Each sheet is an image to download, and every direction, action and size is more drawing. |
| Sprites drawn by code | A figure described as shapes and joints, turned into pixels when needed | Many directions, actions and sizes from one description | No artist's hand on each frame. |
| Canvas 2D | A bitmap you repaint every frame | Hundreds of short-lived shapes: particles, tunnels, weather | Nothing in it is clickable or readable by a screen reader. |
| WebGL (PixiJS, Phaser, Three.js) | The graphics card, directly | Thousands of sprites, shaders, 3D | A large library and a build step, for power a point-and-click does not need. |
| Video files | A recorded movie | Live action, pre-rendered 3D | Tens of megabytes, cannot match the game's state, fixed size, harder to subtitle. |

### What this game does

The rule is: **who needs to know about the motion decides the tool.**

- **If the game depends on it, the game clock runs it.** `js/engine/clock.js` is a
  single `requestAnimationFrame` loop. Walking, cutscene beats, line timing, fades
  and the tunnel all ask this one clock for `wait(ms)` or `tween(ms, step)`. Because
  there is one clock, pausing the game pauses all of it, and skipping a cutscene is
  one switch (see section 3).
- **Scenery is painted once.** When a scene opens, its drawing is turned into pixels
  on a canvas and then left alone. Nothing that happens afterwards repaints it.
- **People and props share one canvas above the scenery.** It is repainted only on a
  frame where something on it has changed: a step, a blink, a ripple in the fountain.
  Section 2 explains how those pictures are made and put in order.
- **CSS runs the glow of time travel and a few ambient loops.** The spinning rings of
  a portal, the road it lights, twinkling stars, ripples on the river. These are
  smooth drawings on a layer of their own, and they only ever animate `transform`
  and `opacity`, the two properties browsers can animate without redrawing the picture.
- **A second canvas is used for one effect:** the time tunnel (`js/engine/fx.js`),
  where rings, streaks and flying dates all change every frame.
- **No WebGL and no game framework.** If a later scene needs a storm of particles,
  that scene can add a canvas effect the same way the tunnel does.

Players who ask their system for less motion (`prefers-reduced-motion`), or tick
**Less motion and no flashes** in Options, get still decoration, people who stand
quite still, plain fades in place of white flashes, and a slow tunnel.

### Keeping it fast as the game grows

- **Scenes load when needed.** Each scene is its own file, fetched the first time
  the player goes there. A scene can name its `exits`, and those are fetched in the
  background, so walking through a door never waits. The game starts just as fast
  with two hundred scenes as with two.
- **Music and voices stream.** Nothing is downloaded until it is about to play.
- **Pictures are drawn once and kept.** A character picture (one pose, one direction,
  one size) is drawn the first time it is needed and kept in a store shared by
  everyone on stage. The store has a fixed budget of about 12 MB and drops whatever
  has gone longest unused.
- **A budget per scene**, to keep older phones smooth: about 20 things animating at
  once on the glow layer, and only `transform` and `opacity` in any CSS animation.
  The backdrop can be as detailed as you like, because it is a single picture once
  the scene has opened. Hold **H** in the game to check a scene's clickable areas.
- **Painted backdrops, when they come.** A scene can name a picture file
  (`picture: "art/scenes/egypt-riverbank.png"`, 640x400 pixels). It is laid down first
  and anything the scene draws with the kit goes over it, so a painted riverbank can
  still have the kit's wormhole glowing on it. Hotspots, walkable ground, props and
  saves do not change.

---

## 2. Characters and depth

### The stage

The picture is a stack of layers, back to front:

| Layer | What is on it | How it is made |
| --- | --- | --- |
| Backdrop | Sky, land, buildings: whatever is far away or flat on the ground | Pixels, painted once when the scene opens |
| Glow | Wormholes, the light they throw, stars, ripples | Smooth drawings, animated by CSS |
| Cast | People and props | Pixels, repainted back to front whenever something moves |
| Tunnel | The time tunnel | A canvas effect, only during travel |
| Clickable areas | Invisible shapes | Real buttons, so a keyboard or a screen reader can reach them |
| Close-up | A screen, a notice or a note, shown large over a dimmed scene | A smooth drawing, put up and taken down by a script |
| Words and menus | Speech, pockets, cards, menus | Ordinary page text |

Two grids are in use, and it helps to know which is which:

- **Positions are on a 320x200 grid.** Where someone stands, where a clickable area
  is, where the ground can be walked on. These are the numbers in a scene file.
- **Art is on a 640x400 grid:** two art pixels to each unit of position. The backdrop
  and the cast share it, which is what makes the picture read as one piece of pixel art.

Most adventure games of the early 1990s had a 320x200 screen. This is four times as
many pixels: a full-size adult here is about 128 pixels tall, and on that screen the
same figure would have 64.

### How a character is drawn

Characters are not stored as pictures. Each is a **jointed figure** with a page of
settings, and every picture of them is worked out from it.

```
people.js    who they are: proportions, skin, hair, clothes, colors
   |
rig.js       a pose (how each joint is bent)  ->  where each joint is  ->  turned to face one of eight directions
   |
pix.js       solid shapes  ->  pixel art
```

The last step gives the look. `pix.js` works the way a pixel artist does, from a short
list of rules:

- Hard edges. Nothing is smoothed.
- Four tones per material, never a gradient.
- One light, from the upper left, in every scene and every era.
- A dark line down the shadow side of a figure and a softer one down the lit side, so
  it reads against any backdrop.
- A thin shadow wherever one part overlaps another: under the hem of a shirt, between
  the legs, where an arm hangs against the body.

The pixels are worked out at the size that is asked for, so a character can stand
anywhere in a scene's depth and still be crisp. Shrinking a finished picture would
smear it.

An **animation is a pose that changes with time:**

| Animation | How it is made |
| --- | --- |
| Walk | 12 pictures to a cycle of two steps, in 8 directions. The foot on the ground moves back at the speed the body moves forward, so feet do not slide. The cycle is driven by ground covered, not by time, so it stays in step at every size. |
| At rest | Slow breathing, and a blink every few seconds |
| Talking | A gesture and three mouth shapes. There are twelve gestures and each character uses a few of them (see below). The line decides which, so a line always plays the same way. |
| Reaching | Out at chest height, or bending down to the ground. Anyone in a skirt dips at the knee and bows a little, and does not bend double. |
| Sitting | Cross-legged on the ground, or on a chair, each with a talking gesture of its own |

This is the method of one of the games this one looks up to, with a puppet in place of an
actor. For King's Quest VI, Sierra filmed costumed actors, brought the video into the
computer, and had animators touch up each frame to sit well on the painted
backgrounds. A puppet costs nothing to shoot again: change Dad's shirt, his height or
his stride in `people.js` and every picture of him follows.

What it does not give is an artist's hand on each frame. Faces are a few pixels, hands
are mittens, and cloth does not fold. If a character later deserves hand-drawn frames,
the cast layer does not care where a picture comes from. It asks for "this animation,
this frame, this direction, this size" and paints what it is given.

`tools/sprites.html` shows every character in every direction, moving, with the
single pictures underneath.

### Making someone themselves

Colors and clothes say who a character is when they stand still. Three more settings
in `people.js` say it when they move, and they are worth as much care:

| Setting | What it is | In the cast |
| --- | --- | --- |
| `stance` | How they stand when nothing is happening: `"clasped"` hands, `"akimbo"`, a `"book"` held to the chest, hands `"behind"` the back | Mom's hands are clasped. Little Sister's fists are on her hips. Big Sister never puts her book down. The man in gray keeps his hands where you cannot see them. |
| `walk` | How they move: length of stride, how far the arms swing and how bent they are, lean, how high the knees come, what the head does | The Son bounces with his fists pumping. Mom takes short steps and her arms hardly move. Little Sister stomps with straight arms. |
| `gestures` | What their hands do when they talk, as a short list of numbers | Dad shrugs. The Son throws both arms up. Mom puts a hand to her heart. Big Sister raises a finger ("fun fact") or pushes her glasses up. Little Sister shows her muscles. |

The twelve gestures: a nod, one hand making a point, a shrug, a hand on the hip, both
arms up, a hand to the heart, pushing glasses up, showing off muscles, an open hand,
both hands waving, pointing straight ahead, and a finger in the air.

The engine never asks the rig for "a walk". It asks for *this character's* walk, through
`poses` in `rig.js`, so nobody on stage moves like anybody else. The rig also knows
skirts (one cone round both legs, with a hem that follows the stride), a round collar,
overalls with a bib and straps, glasses, dark glasses and a beard.

[CHARACTERS.md](CHARACTERS.md) is where these choices come from.

### Depth

A flat picture reads as a deep one when three things hold. The engine does all three
from two facts about each thing on stage: **where it touches the ground**, and **what
patch of ground it takes up**.

**1. Nearer things cover farther things.** Every person and prop has a ground point:
the feet of a figure, the `at` of a prop. Higher on the screen is farther away. On
every frame the cast is sorted by that point and painted back to front. When the
lead's feet are higher than the car's wheels he is painted first and the car covers
him. When they are lower he is painted last and covers the car.

Three planes handle the cases that sorting cannot decide:

| Plane | Painted | Use it for |
| --- | --- | --- |
| `"back"` | First, always | A rug, a mark on the floor |
| `"floor"` | In order of ground point (the default) | Nearly everything |
| `"front"` | Last, always | A pillar at the edge of the screen, an overhanging branch |

A long thing that meets the ground on a slant, such as a wall running into the
distance, can give a `base` line (two points) in place of a single ground point. The
lead is then behind or in front according to which side of the line his feet are on.

**2. Nobody walks through anything.** A prop can give a `solid` outline: the patch of
ground it stands on. People who are not leads block a small patch of their own (the
lead's own companions do not: she can walk past them). The
scene's `walk.area` is the outline of the ground itself. From these the engine builds
a map of where the lead may stand. When the player clicks, it finds a route round
whatever is in the way. A click on a place nobody can stand (inside the car, in the
river, in the sky) sends the lead to the nearest place he can.

**3. Farther things are smaller.** A scene has a `horizon`, the height on screen
where the ground runs out, and a `full` line, where a person is drawn full size. In
between, size falls in a straight line with height on screen, which is what
perspective does to people standing on flat ground:

```
size = (feet - horizon) / (full - horizon)
```

Steps shorten with size, so the walk still matches the ground. Walking into the
picture also covers more ground than walking across it: one unit up the screen counts
as 2.2 units sideways, both for speed and for choosing the shortest route.

Props do not resize themselves. A prop stays where it is put, so its `scale` is set
once to suit that spot.

The settings, with their defaults:

| Setting | Default | Meaning |
| --- | --- | --- |
| `horizon` | 118 | Height on screen where the ground meets the sky |
| `full` | 190 | Height on screen where a person is full size |
| `minScale`, `maxScale` | 0.26, 1.12 | Limits, so that nobody vanishes or fills the screen |
| `walk.area` | | The outline of the walkable ground, as a list of points |
| `props[].solid` | none | The outline of the ground a prop takes up |
| `props[].plane`, `props[].base` | `"floor"`, none | See the table above |
| `actors[].solid` | a small box at their feet | `false` lets the lead walk through them |

For a gentler perspective, as in a view from higher up, move the `horizon` up the
screen (a smaller number, such as 60). People then shrink less as they walk away.

`tools/storyboard.html` draws each scene with its walkable ground, its footprints and
its clickable areas outlined.

---

## 3. Intro movies and cutscenes

A cutscene is **one async function**, kept in `js/content/cutscenes/`. Each `await` is
one beat of the storyboard, so the file reads like a shot list:

```js
await g.card("n0tk3r presents", "", { plain: true });
await g.fade(0, 900);
await g.tween(2600, (k) => wagon.place(160 + 24 * k, 262 - 80 * k, 2.0 - 1.28 * k));
await g.say("intro.1", "intro.2");
```

### Why not a video file

- **Size.** The intro script is about 3 KB. A 40-second video is tens of megabytes.
- **One look.** It uses the same drawings, the same wagon and the same palette as
  the game, so there is no jump in style between the movie and the title.
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
->  the road sign rewrites itself  ->  the wagon drives in, white flash
->  the time tunnel, years flying past  ->  white flash
->  the title: the papyrus strip unrolls, the menu arrives
```

- The **first click** is needed anyway: browsers keep sound off until the player
  does something. So the game opens on a "Click to begin" screen, and that click
  both starts the movie and unlocks audio.
- The intro plays in full the first time. After that the game opens on the title,
  and the menu has **Watch the intro**. (`index.html?intro` forces it.)
- The last frame of the movie and the first frame of the title are the same picture,
  so the title simply settles into place.

---

## 4. Saved games

### What is saved

One small object (`js/engine/state.js`): the act, the scene, which lead the player
controls, which leads they can switch between (the team), where each lead is standing
and which way they face, each lead's pockets, and the list of story facts ("flags"). Nothing else. Every scene can rebuild itself from those facts
(its `setup` function does that), which is why a save is a few hundred bytes.

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
{ "magic": "from-point-a-to-bc", "v": 2, "savedAt": "...", "meta": { "era": "...", "lead": "Dad" },
  "data": { ... }, "check": "9f3a1c07" }
```

- `magic` rejects files that are not from this game.
- `check` is a checksum of the data. A damaged or hand-edited file is refused with a
  plain message. (It catches accidents. It is not a lock against cheating.)
- `v` is the save version. When the game changes shape, add an upgrade step to
  `migrations` in `save.js` and old saves keep working. There is one already: version 1
  knew only Dad and the Son. A version 1 save loads, gets places and pockets for the
  rest of the family, and carries on into the new chapter.
- Volume and subtitle settings are stored apart from saves, so loading a save from
  a friend never changes your volume.

---

## 5. Sound, music and dialogue

### The mixer

```
master -- music   (each track fades in and out on its own)
       |- effects
       '- voices   (while a voice plays, the music drops to about a third)
```

Each has its own slider in Options.

### Music

Each era has a theme, named in `js/content/world.js` and described in
`js/content/sound.js`. Changing scene cross-fades to the new era's theme.

Until music is written, each theme is a **short pattern played by a built-in
synthesizer**, so the game already has a different sound for the road, Egypt, Rome,
home in the evening, the Nevada desert and the tunnel. To use a real recording, add one line:

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

The words live in `js/content/lines.en.js`:

```js
"egypt.river.look": ["dad", "Either that's the Nile or a very committed car wash."],
```

That one decision is what makes a "talkie" version cheap later:

1. **Record** a line and save it as `audio/voice/en/egypt.river.look.mp3`.
2. **Add** its ID to the `voices` list in `sound.js`.

That is all. The engine plays the recording, keeps the words on screen until the
voice finishes, moves the speaker's mouth and hands, and turns the music down underneath.
Lines without a recording keep showing as timed text, so voices can arrive a scene
at a time. Options has **Show the words on screen** and **Play recorded voices**.

The same file is the voice actors' script (the storyboard page exports it as a
spreadsheet, one row per line, grouped by character), and a translation is a copy of
the file with the same IDs.

On screen, each character speaks in their own color, above their own head, in the
manner of classic adventure games.

---

## 6. Story: guided, but not a straight line

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
- **Acts are the spine.** Each should end on a turn in the father-and-son story, not
  only on a solved puzzle.

### The story is data

`js/content/story.js` lists each act and its beats. A beat says what it needs and
what it sets:

```js
{ id: "egypt.mark", kind: "puzzle", chain: "B", title: "Have the scribe mark the door's path on the map",
  lead: "dad", scene: "egypt-riverbank", needs: ["egypt.hasMap", "egypt.penGiven"], sets: "egypt.mapMarked",
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

### Storyboarding before the art exists

A scene file does not need a drawing. Leave out `draw` and the engine **sketches**
the scene: sky, ground, and a labelled box for each clickable thing, in the era's
colors. So the order of work can be:

1. Write the beats in `story.js` and look at them on the storyboard page.
2. Write each scene as boxes and lines (see `scenes/sketch-example.js`), and play
   the whole act through. Fix the puzzles and the pacing while changes are cheap.
3. Draw the scenes that survived.

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

**Together.** Mom and the girls share a scene. A scene says so with
`party: ["mom", "bigsis", "lilsis"]`: they arrive together, each on a mark of her own,
and switching is instant because nobody has to go anywhere. In a party:

- **Each can do what the others cannot.** A clickable thing can answer each lead
  differently: `use: { lilsis: intoCloset, mom: "home.closet.use.mom", bigsis: "home.closet.use.bigsis" }`.
  That is the whole mechanism behind "only Little Sister fits" and "he will only talk
  to Mom", and the refusals are where the jokes are.
- **They talk.** Click a companion to talk to her. The scene supplies the exchanges
  (`talk`), and what has not been heard yet comes first.
- **They hand things over.** Hold something and click a companion to give it to her.
  The scene can react (`given`): Big Sister, handed her father's note, reads what it means.
- **They stay where they are left.** Companions do not follow the lead about. When
  the lead walks up to something, she stands beside a companion who is already there,
  not on top of her.

The two halves of the family meeting in one scene needs nothing new: put all five in a
`party`.

---

## 7. One look across every era

The risk in a time-travel game is a different art style per period. The answer here
is that **eras change the palette and the props, and nothing else.**

### Three groups of color that never mix

| Group | Colors | Used for | Changes? |
| --- | --- | --- | --- |
| **Time** | neon cyan, magenta, violet, white core | Portals, the tunnel, anything time travel has touched, highlights in the interface | Never |
| **Travellers** | Dad's yellow shirt, the Son's blue hoodie and red cap, Mom's emerald dress, Big Sister's indigo cardigan, Little Sister's pink overalls and yellow boots, the red wagon, the green road sign | The people and things from the present | Never |
| **Era** | 8 sky bands, 2 silhouette tones, 3 ground tones, a dark tone, a light tone, 2 feature colors | The world of each period | Per era, same slots |

Because of this, in any screenshot from any era you can tell at a glance what
belongs to the period (era colors), who the visitors are (traveller colors) and
where time is leaking through (neon).

Each member of the family owns one color that nobody else in the family wears, and
their words on screen are a pale tint of it. The travellers carry their colors with
them, in `js/art/people.js` and `js/art/props.js`. A prop can also pick up the era it is standing in: the sand heaped
round the stuck wagon is the riverbank's own.

### How futuristic and ancient blend

They are kept apart on purpose, and the contrast is the style:

- **The ancient world is warm, matte and made of pixels.** Earth, stone, water,
  linen. No glow, no gradients.
- **Time travel is the only thing that glows, and the only thing drawn smooth.** Neon
  rings, soft light, dashed lines. A wormhole never looks like part of the world it
  has opened in, because it is not made of the same stuff. Wherever the two meet, the
  neon lights the scene: the road turns cyan under the portal, and a door in the air
  is the brightest thing on a riverbank.
- **The interface is ancient, with neon for "active".** Menus, buttons, cards and
  the title are ink on papyrus, in Koine Road. The selected item or tool turns cyan.
- **One signature shape.** A wormhole is always the same four dashed rings, turning
  in opposite directions, in every era and in the browser tab icon.
- **A possible motif to grow:** let the eras leak into each other as the story goes
  on. A Roman column with a neon crack. A hieroglyph that is a road sign.

### What stays the same in every era

1. **The grid:** 640x400 art pixels, hard edges, nothing smoothed.
2. **The light:** from the upper left, in four tones per material, on every person
   and prop in every era.
3. **The composition:** eight sky bands down to a horizon near 118, two layers of
   silhouette, three bands of ground. Indoors the same slots are a room: the "sky" is
   the night outside the window, the wallpaper and the woodwork, the silhouettes are
   furniture, and the ground is floorboards.
4. **The drawing kit:** every backdrop is assembled from `js/art/kit.js`, every person
   from `js/art/rig.js`, every prop with the same renderer.
5. **Darkness is a color:** shadows are a darker tone of the thing itself, never
   pure black.
6. **The type:** Koine Road for titles, cards and buttons; a plain bold sans for
   speech.
7. **The cards:** every era opens with its name on a torn strip of papyrus.

### How it is enforced in the code

Art never names a color for the world. It names a **slot**:

```js
art.sky() + art.pyramids + art.ground() + art.river()     // uses classes s1..s8, far, near, g1..g3, feat
```

`css/tokens.css` gives each era the same slots with different values, and the stage
carries `data-era="egypt"`. The same drawing code produces a dusk highway, a dawn on
the Nile or a noon in Rome. Adding an era is one block of seventeen colors. The
storyboard page shows all palettes side by side so a new one can be judged against
the rest.

---

## 8. How to add things

**A line.** Add it to `js/content/lines.en.js`. Say it with `g.say("its.id")`.

**A scene.** Copy `js/content/scenes/egypt-riverbank.js`, change it, and add its id
to the list in `js/content/scenes/index.js`. A scene is:

```js
export default {
  id: "egypt-riverbank", era: "egypt", name: "A riverbank at dawn",
  horizon: 118, full: 190,                      // depth: where the ground runs out, and where a person is full size
  walk: { area: [[104, 138], [312, 138], [312, 196], [8, 196], [8, 190], [48, 176], [84, 154]] },   // the outline of the walkable ground
  spawn: { default: [200, 184] },
  exits: ["rome-forum"],                        // scenes to fetch ahead of time
  draw(art) { return art.sky() + art.pyramids + art.ground(8) + art.river(); },   // the backdrop
  props: [                                      // things standing on the ground
    { id: "wagon", kind: "wagonStuck", at: [254, 176], scale: 1.12,
      solid: [[220, 164], [288, 164], [292, 179], [216, 179]] },                  // the patch of ground it takes up
  ],
  actors: [{ id: "scribe", kind: "scribe", at: [150, 170], face: "E" }],          // people who are not the lead
  setup(g) { /* make the drawing match the story facts */ },
  hotspots: [
    { id: "wagon", name: "wagon", verb: "Search", rect: [222, 122, 64, 56],
      walkTo: [254, 186], face: "N",            // where the lead goes to do it, and which way he then faces
      look: "egypt.wagon.look",                 // a line ID,
      use: async (g) => { ... },                // or a function,
      useWith: { reed: async (g) => { ... } } },  // or a reaction to a carried item
  ],
  async enter(g) { /* what happens on arrival; must be safe to run twice */ },
};
```

All the numbers are positions on the 320x200 grid. Directions are compass points on
the screen: `"N"` is away from the player, `"S"` toward, `"E"` screen right, and the
four in between.

To jump straight to a scene while building it: `index.html?scene=rome-forum&lead=son`.
Every act before that scene's own counts as played, so hints work. Add
`&flags=home.online,home.knowsYear` to start with more of the story done. Hold **H** in
the game to see every clickable area. The storyboard page outlines each scene's
walkable ground and footprints, and has a **Play from here** link under every scene.

**A scene for several leads.** `js/content/scenes/home-living-room.js` is the one to
copy. On top of the above it has:

```js
party: ["mom", "bigsis", "lilsis"],                         // they are here together
spawn: { default: [150, 162], mom: [134, 160], bigsis: [196, 150], lilsis: [84, 140] },   // a mark each
hotspots: [
  { id: "closet", name: "closet under the stairs", rect: [288, 92, 26, 30], walkTo: [282, 129],
    look: { mom: "home.closet.look.mom", bigsis: "home.closet.look.bigsis", lilsis: "home.closet.look.lilsis" },
    use: { lilsis: intoCloset, mom: "home.closet.use.mom", bigsis: "home.closet.use.bigsis" } },   // one answer for each lead; `any` is for whoever is not named
],
talk: { mom: { bigsis: [["line.a", "line.b"], { when: (g) => g.has("coin"), say: ["line.c", "line.d"] }] } },   // what Mom and Big Sister say when Mom clicks her
async given(g, item, to, from) { /* something was handed over */ },
```

**A character.** Write down who they are first ([CHARACTERS.md](CHARACTERS.md) has the
pattern). Then copy the nearest entry in `js/art/people.js` and change the proportions,
clothes and colors, and give them a `stance`, a `walk` and a list of `gestures` of
their own (section 2). Give them `sprite: "that-name"` in `cast` in `world.js`, or put
them in a scene's `actors` with `kind: "that-name"`. Add `lead: true` in `cast` if the
player can control them: they then get a place, pockets and a portrait. Open
`tools/sprites.html` to see them from every side, moving. Anything the standard figure
does not have (a hat, a backpack, a handbag, pigtails) goes in the entry's `extras`
function.

**A prop.** Add an entry to `js/art/props.js` with a `draw` function that builds the
thing from panels, limbs and balls, the way the wagon and the fountain are built. Then
list it in a scene's `props`. A prop with several `frames` animates by itself. A prop
that changes with the story takes a `state` in its `options` (the computer screen in
the living room is `"offline"`, `"login"` or `"map"`); the scene's `setup` sets it.

**A close-up.** For something too small to read in the scene (a screen, a notice), draw
it large on the 320x200 grid and show it from a script: `g.closeup(g.art.notice())`.
People go on talking under it, and it is put away when the script ends. The drawings
are in `kit.js` (`monitor`, `screens`, `notice`).

**A painted backdrop.** Save it as a 640x400 PNG and name it in the scene:
`picture: "art/scenes/egypt-riverbank.png"`. Keep `draw` for anything that should
still come from the kit, such as a wormhole, or leave `draw` out.

**An item.** Add it to `items` in `world.js` and draw a 12x12 icon in `kit.js`.

**An era.** Add a palette block to `css/tokens.css`, an entry in `eras` in
`world.js`, and a theme in `sound.js`.

**A cutscene.** Add a function in `js/content/cutscenes/` and list it in `main.js`.
Play it with `await g.cutscene("its-name")`.

**A beat of story.** Add it to `js/content/story.js`, and have the script call
`g.flag("the.fact", true)` when the player does it. Open `tools/storyboard.html` to
see it in place and to see any warnings.

### What scripts can do

| Call | Does |
| --- | --- |
| `await g.say("id", "id2")` | Speaks lines in order |
| `await g.choose([{ id, line }])` | Offers things to say; gives back the chosen `id` |
| `g.flag("name")`, `g.flag("name", true)` | Reads or records a story fact |
| `g.give("item")`, `g.take("item")`, `g.has("item")` | Pockets of the current lead |
| `g.holder("item")` | Which lead is carrying a thing, or `null` |
| `await g.goto("scene", { via: "wormhole" })` | Changes scene by fade, cut or time tunnel |
| `await g.card("Ancient Egypt", "1250 B.C.")` | Shows a title card |
| `await g.cutscene("intro")` | Plays a skippable cutscene |
| `await g.wait(ms)`, `await g.tween(ms, (k) => ...)`, `await g.fade(1)` | Timing, motion, fades |
| `g.music("egypt")`, `g.sfx("portal")` | Sound |
| `await g.walkTo(x, y)`, `await g.walkTo(x, y, "scribe")` | Walks the lead, or someone else, to a place, round whatever is in the way |
| `await g.moveTo(x, y)`, `await g.moveTo(x, y, "agent")` | Walks in a straight line to a place the player could not click on (into a closet) |
| `await g.reach()`, `await g.reach(true)` | The lead reaches out, or bends down to the ground |
| `g.actor("scribe").face("W")`, `g.lead.look(x, y)` | Turns someone to a compass point, or toward a place |
| `g.actor("scribe")`, `g.lead`, `g.q("#hole")` | Reach people, props and the glowing parts of the drawing |
| `g.team(["mom", "bigsis", "lilsis"])` | Says which leads the player can switch between from now on |
| `await g.switchLead("son")` | Changes who the player controls (they must be on the team) |
| `g.closeup(drawing)`, `g.closeup()` | Shows a close look at something, and puts it away |
| `await g.tap()` | Waits for a click or a key |

---

## 9. What is real and what is placeholder

**Real, and meant to stay:** the engine, the save format, the sound system, the
line-ID dialogue system, the story-as-data structure, the color system, the pixel
renderer and the figure, the depth system, the interface, the Koine Road typeface.

**Placeholder, written only to prove the engine:** every scene, puzzle, joke, era and
date in `js/content/`; the designs of everyone in `js/art/people.js`; the backdrops,
which are still flat shapes and bands of color; and the synthesized music. The five
members of the family and their traits are the author's. The details hung on them in
[CHARACTERS.md](CHARACTERS.md), and every puzzle in the present-day chapter, are a
first draft to keep, change or throw out.

**Not built yet:**

- Painted backdrops. The characters and props are shaded pixel art; the scenery
  behind them is not yet. The engine takes a painted picture per scene (section 1).
- Hiding the lead behind part of the backdrop. Only props can cover him. A rock or a
  doorway he should pass behind has to be a prop, or a cut-out piece on the `"front"` plane.
- Light that changes with the scene. Every character is lit the same way in their own
  colors, at dusk and at noon alike.
- More acting. There is no turning between directions (he snaps round), no running,
  climbing, carrying or sitting down, and faces cannot yet show a feeling.
- Other people walking about. Anyone can be walked by a script, but their patch of
  blocked ground does not follow them, so give walkers `solid: false`.
- Companions who follow the lead. In a party the others stay where they were left.
- Close-ups the player can click inside. A close-up is a picture to read, not a
  small scene of its own.
- Scrolling scenes wider than the screen.
- Touch polish: larger targets and a bigger inventory on phones.
- Layered music, ambient sound loops, per-scene reverb.
- Translations (the line files are ready for them) and a caption option for sounds.
- Saving in the middle of a conversation. Esc pauses at any time, but Save and Load
  wait until the current moment has played out.

**How it was tested.** A script drove a real browser (Chromium) through the whole demo: the
intro played and skipped (early and late) to the same title state; New Game, all
puzzles, the dialogue tree, both leads, the act break and the wormhole; saving to a
slot, exporting a file, loading it back, and refusing an edited file; reload and
Continue; and four screen sizes from a phone held upright to a 2560-pixel monitor. The
voice path was tested with a test tone standing in for a recording: the line waited
for the sound, the music dropped under it and came back, and turning the words off
left the voice alone. The browser console stayed clean throughout.

Depth was tested the same way, by reading pixels off the screen: the lead is painted
before the car when he stands behind it, and the car's pixels cover his; he is painted
after it when he stands in front; his route to the far side goes round the car; clicks
inside the car, on the scribe, in the river and in the sky all end on legal ground; his
size follows the rule at five depths; and a save made in an impossible spot loads to
the nearest possible one. Every full-size picture of every character was also looked
at by eye (eight directions, each walk, each gesture), with a sample of the smaller sizes.

The present-day chapter was tested the same way: a script played the whole game from
New Game through Egypt, Rome, the living room and Nevada to the end, switching leads
with the portraits and the number keys, handing things from one lead to another, and
asking each lead for a hint at each stage; it saved part-way through to a slot and a
file and loaded back, and loaded a save made by the previous version of the game and
carried it on into the new chapter. The interface was photographed at four screen
sizes. The new characters were looked at in every direction, walking, talking and
reaching, at full size.

A second script went looking for every line in the game. It played each scene from
several starting points, as every lead and in more than one order, and read each line
off the screen as it was spoken. 394 of the 405 lines in the script file were heard
that way, each of them word for word as written. The other eleven are stock replies
that no scene can reach yet: what each lead says when a thing has nothing written for
it (five lines), what four of them say when there is no hint to give, and what Dad and
the Son say on handing each other something. A third check read the scripts against
the line file: no script names a line that is not there, and no line is left unnamed.

It has not yet been played by a person on a real phone, or in Firefox or Safari. One
step deserves a look there: the backdrop is made by handing the browser a drawing and
asking for pixels back. If a browser refuses, the game falls back to showing the
drawing itself, which is smooth instead of pixelled.

---

## 10. Controls

| Do this | With a mouse | On a touch screen | On a keyboard |
| --- | --- | --- | --- |
| Walk | Click the ground | Tap the ground | |
| Use, talk, pick up | Click the thing | Tap the thing | Tab to it, Enter |
| Look | Right-click, or **Look** then click | Press and hold, or **Look** then tap | Tab to it, L |
| Use a carried thing | Click it, then click the target | Tap it, then tap the target | |
| Play as someone else | Click their portrait | Tap their portrait | 1, 2, 3 |
| Talk to a companion | Click them | Tap them | Tab to them, Enter |
| Give a companion something | Click the thing, then click them | Tap the thing, then tap them | |
| Next line | Click | Tap | Space or Enter |
| Pick a reply | Click it | Tap it | Number keys |
| Skip a cutscene | **Skip** | **Skip** | Esc |
| Menu | **Menu** | **Menu** | Esc |
| Show what can be clicked | **Show** | **Show** | Hold H |
| Move past a title card | Click | Tap | Space or Enter |

---

## 11. Decisions waiting for you

The scaffold makes choices so that it runs. These are yours to keep or change:

1. **The look.** Pixel art at 640x400, with characters shaded in four tones and
   drawn from a jointed figure. The alternative is hand-drawn sprite sheets, which
   look more hand-made and cost a drawing for every frame, direction and size. The
   backdrops are still flat placeholders; painting them is the largest step left
   toward the look of the classic games.
   **How strong the perspective is** is part of this: at present the lead shrinks to
   under a third of his size at the far edge of the sand. Section 2 says how to soften it.
2. **In-engine cutscenes** instead of video.
3. **Five leads:** free switching, alternating chapters, or a mix. At present Dad and
   the Son can be switched between once the Son has landed, and Mom and the girls can
   be switched between at any time, but the story decides when to cut from one half of
   the family to the other.
4. **Passing things between eras through wormholes** as a core puzzle idea.
5. **Verbs:** one main action plus Look. Classic games had a verb list; a third
   verb such as Talk could be added.
6. **Hints:** a Hint button that has the lead think aloud. Keep it, limit it, or
   drop it.
7. **Voices:** from the start or later. The engine handles either.
8. **Who the leads are.** [CHARACTERS.md](CHARACTERS.md) is a first draft of all five,
   built on your descriptions. Nobody has a name yet: on screen they are Dad, Son, Mom,
   Big Sister and Little Sister.
9. **Where the present-day chapter goes.** It plays after Rome, as "Meanwhile, about two
   thousand years later". It could open the game instead, or be cut in between the
   scenes in the past.
10. **The present-day puzzles.** The router in the closet, the password, the wedding
    question, the witness, the man in gray and the notice are all a first draft.
    [PUZZLES-the-present.md](PUZZLES-the-present.md) lays them out so they are easy to change.
11. **Big Sister's facts.** Every fact she states has to be true. The list, and which
    of them have been checked against a source, is at the end of CHARACTERS.md.

---

## Sources

- web.dev, [Why are some animations slow?](https://web.dev/articles/animations-overview):
  `transform` and `opacity` can be animated without layout or paint.
- MDN, [Animation (Web Animations API)](https://developer.mozilla.org/en-US/docs/Web/API/Animation):
  script control of animations: pause, finish, `currentTime`, `playbackRate`.
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
