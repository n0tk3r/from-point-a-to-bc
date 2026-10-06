# From Point A to B.C.: how the game is built

This is the design of the game's engine and its look. It answers seven questions:

1. [What kinds of animation can a browser game use, and which do we use?](#1-animation)
2. [How do intro movies work, and how do they lead into the title?](#2-intro-movies-and-cutscenes)
3. [How do saved games work?](#3-saved-games)
4. [How do music, sound and dialogue work, and how do we get to full voices?](#4-sound-music-and-dialogue)
5. [How is the story kept guided without being a straight line?](#5-story-guided-but-not-a-straight-line)
6. [How does one look hold across every time period?](#6-one-look-across-every-era)
7. [How do I add a scene, a line, an era?](#7-how-to-add-things)

Everything described here is working code in this repository. The story in it is a
placeholder: three short acts written to exercise each part. See
[what is real and what is placeholder](#8-what-is-real-and-what-is-placeholder).

## The short version

| Question | Decision | Why |
| --- | --- | --- |
| Engine | Plain JavaScript modules, no framework, no build step | GitHub Pages serves the files as they are. Nothing to install, nothing to break. |
| Picture | A 320x200 grid drawn in SVG, scaled to fit any screen | Sharp at every size, tiny files, and colours can be swapped per era with CSS. |
| Movement | One game clock drives anything that matters to the game. CSS runs the decoration. Canvas is used only for the time tunnel. | Each tool does the job it is best at. See section 1. |
| Intro movie | A script that moves the game's own art. Not a video file. | About 3 KB instead of tens of MB, identical in style to the game, skippable, subtitled. |
| Saves | Autosave and three slots in the browser, plus a save file the player can download and load anywhere | Browser storage can be wiped. A file is the player's own. |
| Sound | Web Audio with separate volume for music, effects and voices | Standard, works everywhere, lets music duck under speech. |
| Dialogue | Every line has an ID. Text now, a sound file with the same name later. | Voices can be added one line at a time without touching any script. |
| Story | Acts and beats listed as data, with a checker and a storyboard page | Parallel puzzle chains inside an act, one gate at the end of it. |
| Look | Two colour layers that never mix, one drawing kit, one typeface | Each era changes the palette, never the rules. |

Size today: the whole game is 24 files, about 135 KB of code (43 KB when the server
compresses it) plus a 49 KB font. In a test browser it held 60 frames per second.

## Where things are

```
index.html              the page: one stage, a stack of layers
css/tokens.css          colours and type: the time layer, the era palettes
css/game.css            layout and interface
js/main.js              gathers the content and starts the engine
js/engine/              the engine. Knows nothing about this story.
  clock.js                the game clock: wait, tween, pause, skip
  state.js                the data a save file holds
  save.js                 slots, export to a file, import from a file
  audio.js                music, effects, voices
  dialogue.js             spoken lines and choices
  scene.js                background, actors, clickable areas
  fx.js                   canvas effects (the time tunnel)
  story.js                reads the story data: open beats, checks
  ui.js                   heads-up display and menus
  game.js                 ties it together; the `g` that scripts use
js/art/kit.js           the drawing kit: skies, ground, portal, sprites
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
| SVG | Vector drawings in the page, styled by CSS | Flat-colour art, recolouring by era, sharpness at any size, clickable shapes | Hundreds of moving parts at once. |
| Sprite sheets | A strip of frames, stepped through with `steps()` or by a clock | Hand-drawn character animation | Each sheet is an image to download. |
| Canvas 2D | A bitmap you repaint every frame | Hundreds of short-lived shapes: particles, tunnels, weather | Nothing in it is clickable or readable by a screen reader. |
| WebGL (PixiJS, Phaser, Three.js) | The graphics card, directly | Thousands of sprites, shaders, 3D | A large library and a build step, for power a point-and-click does not need. |
| Video files | A recorded movie | Live action, pre-rendered 3D | Tens of megabytes, cannot match the game's state, fixed size, harder to subtitle. |

### What this game does

The rule is: **who needs to know about the motion decides the tool.**

- **If the game depends on it, the game clock runs it.** `js/engine/clock.js` is a
  single `requestAnimationFrame` loop. Walking, cutscene beats, line timing, fades
  and the tunnel all ask this one clock for `wait(ms)` or `tween(ms, step)`. Because
  there is one clock, pausing the game pauses all of it, and skipping a cutscene is
  one switch (see section 2).
- **If it is decoration, CSS runs it.** Twinkling stars, the spinning rings of a
  portal, swaying reeds, ripples. These only ever animate `transform` and `opacity`,
  the two properties browsers can animate without redrawing the picture.
- **Actors are separate elements moved with `transform`.** The background is drawn
  once per scene and left alone. Dad, the Son and the wagon sit above it and slide
  around, so moving them never repaints the scenery.
- **Canvas is used for one thing:** the time tunnel (`js/engine/fx.js`), where rings,
  streaks and flying dates all change every frame.
- **No WebGL and no game framework.** If a later scene needs a storm of particles,
  that scene can add a canvas effect the same way the tunnel does.

Players who ask their system for less motion (`prefers-reduced-motion`), or tick
**Less motion and no flashes** in Options, get still decoration, plain fades in
place of white flashes, and a slow tunnel.

### Keeping it fast as the game grows

- **Scenes load when needed.** Each scene is its own file, fetched the first time
  the player goes there. A scene can name its `exits`, and those are fetched in the
  background, so walking through a door never waits. The game starts just as fast
  with two hundred scenes as with two.
- **Music and voices stream.** Nothing is downloaded until it is about to play.
- **A budget per scene**, to keep older phones smooth: about 300 shapes in the
  background, about 20 things animating at once, and only `transform` and `opacity`
  in any CSS animation. Hold **H** in the game to check a scene's clickable areas.
- **Pictures, when they come.** Painted backgrounds can replace the drawn ones
  scene by scene: an `<image>` inside the same SVG frame, exported at 1280x800 as
  WebP or AVIF. Hotspots, actors, palettes and saves do not change.

---

## 2. Intro movies and cutscenes

A cutscene is **one async function**, kept in `js/content/cutscenes/`. Each `await` is
one beat of the storyboard, so the file reads like a shot list:

```js
await g.card("n0tk3r presents", "", { plain: true });
await g.fade(0, 900);
await g.tween(2600, (k) => wagon.place(160 + 24 * k, 250 - 68 * k, 2.8 - 1.8 * k));
await g.say("intro.1", "intro.2");
```

### Why not a video file

- **Size.** The intro script is about 3 KB. A 40-second video is tens of megabytes.
- **One look.** It uses the same drawings and palette as the game, so there is no
  jump in style between the movie and the title.
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

## 3. Saved games

### What is saved

One small object (`js/engine/state.js`): the act, the scene, which lead the player
controls, where each lead is standing, each lead's pockets, and the list of story
facts ("flags"). Nothing else. Every scene can rebuild itself from those facts
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
{ "magic": "from-point-a-to-bc", "v": 1, "savedAt": "...", "meta": { "era": "...", "lead": "Dad" },
  "data": { ... }, "check": "9f3a1c07" }
```

- `magic` rejects files that are not from this game.
- `check` is a checksum of the data. A damaged or hand-edited file is refused with a
  plain message. (It catches accidents. It is not a lock against cheating.)
- `v` is the save version. When the game changes shape, add an upgrade step to
  `migrations` in `save.js` and old saves keep working.
- Volume and subtitle settings are stored apart from saves, so loading a save from
  a friend never changes your volume.

---

## 4. Sound, music and dialogue

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
synthesizer**, so the game already has a different sound for the road, Egypt, Rome
and the tunnel. To use a real recording, add one line:

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
voice finishes, moves the speaker's mouth, and turns the music down underneath.
Lines without a recording keep showing as timed text, so voices can arrive a scene
at a time. Options has **Show the words on screen** and **Play recorded voices**.

The same file is the voice actors' script (the storyboard page exports it as a
spreadsheet, one row per line, grouped by character), and a translation is a copy of
the file with the same IDs.

On screen, each character speaks in their own colour, above their own head, in the
manner of classic adventure games.

---

## 5. Story: guided, but not a straight line

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
  say its hint line.
- **A check.** At every start the engine walks the story as a player would and
  warns in the console if a beat can never be reached or names a scene that does
  not exist.
- **A storyboard.** `tools/storyboard.html` draws every act, chain and scene from
  the same data. Plan there, and the plan cannot drift from the game.

### Storyboarding before the art exists

A scene file does not need a drawing. Leave out `draw` and the engine **sketches**
the scene: sky, ground, and a labelled box for each clickable thing, in the era's
colours. So the order of work can be:

1. Write the beats in `story.js` and look at them on the storyboard page.
2. Write each scene as boxes and lines (see `scenes/sketch-example.js`), and play
   the whole act through. Fix the puzzles and the pacing while changes are cheap.
3. Draw the scenes that survived.

### Two leads

Dad and the Son each have their own place and their own pockets. The state holds
both; `state.active` says who the player is. The engine supports both designs:
alternate chapters (the story decides when to cut, as at the end of the demo's Act
One) or free switching (the **Play as** button, as in the demo's Act Two). A
strong fit for this premise: something sent through a door in one era turns up in
another, so the two can help each other across time before they meet.

---

## 6. One look across every era

The risk in a time-travel game is a different art style per period. The answer here
is that **eras change the palette and the props, and nothing else.**

### Three groups of colour that never mix

| Group | Colours | Used for | Changes? |
| --- | --- | --- | --- |
| **Time** | neon cyan, magenta, violet, white core | Portals, the tunnel, anything time travel has touched, highlights in the interface | Never |
| **Travellers** | Dad's yellow shirt, the Son's blue hoodie and red cap, the red wagon, the green road sign | The people and things from the present | Never |
| **Era** | 8 sky bands, 2 silhouette tones, 3 ground tones, a dark tone, a light tone, 2 feature colours | The world of each period | Per era, same slots |

Because of this, in any screenshot from any era you can tell at a glance what
belongs to the period (era colours), who the visitors are (traveller colours) and
where time is leaking through (neon).

### How futuristic and ancient blend

They are kept apart on purpose, and the contrast is the style:

- **The ancient world is warm, matte and flat.** Earth, stone, water, linen. No
  glow, no gradients.
- **Time travel is the only thing that glows.** Neon rings, soft light, dashed
  lines. Wherever the two meet, the neon lights the scene: the road turns cyan
  under the portal, and a door in the air is the brightest thing on a riverbank.
- **The interface is ancient, with neon for "active".** Menus, buttons, cards and
  the title are ink on papyrus, in Koine Road. The selected item or tool turns cyan.
- **One signature shape.** A wormhole is always the same four dashed rings, turning
  in opposite directions, in every era and in the browser tab icon.
- **A possible motif to grow:** let the eras leak into each other as the story goes
  on. A Roman column with a neon crack. A hieroglyph that is a road sign.

### What stays the same in every era

1. **The grid:** 320x200, hard edges, flat fills, no outlines.
2. **The composition:** eight sky bands down to a horizon near 118, two layers of
   silhouette, three bands of ground.
3. **The drawing kit:** every scene is assembled from `js/art/kit.js`.
4. **Darkness is a colour:** shadows use the era's darkest tone, never pure black.
5. **The type:** Koine Road for titles, cards and buttons; a plain bold sans for
   speech.
6. **The cards:** every era opens with its name on a torn strip of papyrus.

### How it is enforced in the code

Art never names a colour for the world. It names a **slot**:

```js
art.sky() + art.pyramids + art.ground() + art.river()     // uses classes s1..s8, far, near, g1..g3, feat
```

`css/tokens.css` gives each era the same slots with different values, and the stage
carries `data-era="egypt"`. The same drawing code produces a dusk highway, a dawn on
the Nile or a noon in Rome. Adding an era is one block of sixteen colours. The
storyboard page shows all palettes side by side so a new one can be judged against
the rest.

---

## 7. How to add things

**A line.** Add it to `js/content/lines.en.js`. Say it with `g.say("its.id")`.

**A scene.** Copy `js/content/scenes/egypt-riverbank.js`, change it, and add its id
to the list in `js/content/scenes/index.js`. A scene is:

```js
export default {
  id: "egypt-riverbank", era: "egypt", name: "A riverbank at dawn",
  walk: { x: [50, 300], y: [166, 192] },      // where the lead can walk
  scale: [0.9, 1.15],                           // size at the back and front of that box
  spawn: { default: [200, 184] },
  exits: ["rome-forum"],                        // scenes to fetch ahead of time
  draw(art) { return art.sky() + art.pyramids + art.ground(8) + art.river(); },
  actors: [{ id: "scribe", sprite: "scribe", at: [150, 170] }],
  setup(g) { /* make the drawing match the story facts */ },
  hotspots: [
    { id: "river", name: "river", rect: [0, 118, 120, 60], walkTo: [98, 172],
      look: "egypt.river.look",                 // a line ID,
      use: async (g) => { ... },                // or a function,
      useWith: { reed: async (g) => { ... } } },  // or a reaction to a carried item
  ],
  async enter(g) { /* what happens on arrival; must be safe to run twice */ },
};
```

To jump straight to a scene while building it: `index.html?scene=rome-forum&lead=son`.
Hold **H** in the game to see every clickable area.

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
| `await g.goto("scene", { via: "wormhole" })` | Changes scene by fade, cut or time tunnel |
| `await g.card("Ancient Egypt", "1250 B.C.")` | Shows a title card |
| `await g.cutscene("intro")` | Plays a skippable cutscene |
| `await g.wait(ms)`, `await g.tween(ms, (k) => ...)`, `await g.fade(1)` | Timing, motion, fades |
| `g.music("egypt")`, `g.sfx("portal")` | Sound |
| `g.actor("scribe")`, `g.lead`, `g.q("#hole")` | Reach people and parts of the drawing |
| `await g.switchLead("son")` | Changes who the player controls |

---

## 8. What is real and what is placeholder

**Real, and meant to stay:** the engine, the save format, the sound system, the
line-ID dialogue system, the story-as-data structure, the colour system, the
drawing kit, the interface, the Koine Road typeface.

**Placeholder, written only to prove the engine:** every scene, puzzle, joke,
character detail, era and date in `js/content/`, the sprites for Dad, the Son and
the scribe, and the synthesized music. Replace these as the character bibles and the
real puzzle document are written.

**Not built yet:**

- Walking around obstacles. Leads walk in a straight line inside a box. Scenes with
  things to walk around will need walk-polygons and path-finding.
- Hand-drawn character animation. Sprites have two walk frames and a talking mouth.
- Scrolling scenes wider than the screen, and close-up views of objects.
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
left the voice alone. The browser console stayed clean throughout. It has not yet
been played by a person on a real phone, or in Firefox or Safari.

### Controls

| Do this | With a mouse | On a touch screen | On a keyboard |
| --- | --- | --- | --- |
| Walk | Click the ground | Tap the ground | |
| Use, talk, pick up | Click the thing | Tap the thing | Tab to it, Enter |
| Look | Right-click, or **Look** then click | Press and hold, or **Look** then tap | Tab to it, L |
| Use a carried thing | Click it, then click the target | Tap it, then tap the target | |
| Next line | Click | Tap | Space or Enter |
| Pick a reply | Click it | Tap it | Number keys |
| Skip a cutscene | **Skip** | **Skip** | Esc |
| Menu | **Menu** | **Menu** | Esc |
| Show what can be clicked | **Show** | **Show** | Hold H |
| Move past a title card | Click | Tap | Space or Enter |

### Decisions waiting for you

The scaffold makes choices so that it runs. These are yours to keep or change:

1. **The look.** A 320x200 flat-colour grid drawn in code. It is consistent and
   tiny, but it is one option. Painted backgrounds or larger pixel art would slot
   into the same engine.
2. **In-engine cutscenes** instead of video.
3. **Two leads:** free switching, alternating chapters, or a mix.
4. **Passing things between eras through wormholes** as a core puzzle idea.
5. **Verbs:** one main action plus Look. Classic games had a verb list; a third
   verb such as Talk could be added.
6. **Hints:** a Hint button that has the lead think aloud. Keep it, limit it, or
   drop it.
7. **Voices:** from the start or later. The engine handles either.

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
