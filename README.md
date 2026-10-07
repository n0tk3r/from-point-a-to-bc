# From Point A to B.C.

Dad's shortcut sends a father and son tumbling through history, and the rest of the family sets out to fetch them. A point-and-click adventure you can play in your browser.

**Play it:** https://n0tk3r.github.io/from-point-a-to-bc/

## Status

In development. What is here now:

- **The engine**: scenes, walking, clickable areas, inventory, dialogue with choices, cutscenes that can be skipped, close-ups, hints.
- **Painted scenes**: every scene is one painted picture, 800 pixels by 600, with painted cut-outs for the things people walk behind and the things the story changes. The highway of the intro and nine scenes are painted so far.
- **Five playable leads**: Dad and the Son, lost in different centuries, and Mom, Big Sister and Little Sister, who work as a team. You switch between them with their portraits. Each can do something the others cannot, and they talk to each other and hand things over.
- **Pixel-art people drawn by code**: each of the twenty-three is a jointed figure that walks in eight directions, talks with its hands, reaches, bends and sits, and each stands, walks and gestures in a way of their own. There are no picture files of people.
- **Depth**: people walk behind things and in front of them, round obstacles, and get smaller as they walk away.
- **An intro movie** that runs into the title screen.
- **Saved games**: autosave, three slots, and a save file you can download and load on any device.
- **Sound**: music, effects and voices on separate sliders. The music is synthesized placeholder until real tracks are written. Dialogue is ready for recorded voices.
- **The story so far**: a prologue and four acts (Egypt, Rome, home in the present, the Nevada desert).

Read [docs/DESIGN.md](docs/DESIGN.md) for how it all works and why, and [docs/CHARACTERS.md](docs/CHARACTERS.md) for who the people are and how each of them talks. The acts are laid out puzzle by puzzle in [docs/PUZZLES-egypt.md](docs/PUZZLES-egypt.md), [docs/PUZZLES-rome.md](docs/PUZZLES-rome.md) and [docs/PUZZLES-the-present.md](docs/PUZZLES-the-present.md). Open [tools/storyboard.html](tools/storyboard.html) to see the story and every scene laid out, and [tools/sprites.html](tools/sprites.html) to see every character moving.

## Running locally

The game is plain HTML, CSS and JavaScript modules. There is no build step.

```
python3 tools/serve.py
```

Then open `http://localhost:8000`. Opening `index.html` by double-clicking will not work, because browsers only load module files from a web address. (`python3 -m http.server` works too. `tools/serve.py` differs in telling the browser to keep no copies of files, so you always see them as they are now.)

Useful addresses while building:

- `http://localhost:8000/?intro` plays the intro again.
- `http://localhost:8000/?scene=rome-street&lead=son` jumps straight to a scene. Add `&flags=rome.arrived,rome.sawStreet` to start with more of the story done.
- `http://localhost:8000/?scene=home-living-room` starts the present-day chapter, and `?scene=nevada-roadside` its second half.
- `http://localhost:8000/?scene=engine-proof` is the worked example of a painted scene.
- `http://localhost:8000/tools/storyboard.html` shows the storyboard.
- `http://localhost:8000/tools/sprites.html` shows every character and prop, in every direction, moving.

In the game: click to walk, use and talk. Right-click (or press and hold on a touch screen) looks at things. What the person you are playing carries is along the bottom left; click a thing there, then click what to use it with. Click a portrait at the top left (or press **1**, **2**, **3**) to play as someone else. Click one of the others to talk to her; to hand her something, click the thing and then click her, or her portrait. **Esc** opens the menu or skips a cutscene. Hold **H** to see everything you can click.

## Publishing

After changing anything in `js/`, `css/` or `art/`, stamp the pages, then commit and push:

```
python3 tools/stamp.py
```

The stamp gives every code file, style file and picture an address that changes when the file changes, so a browser can never run old files next to new ones after an update, or show last week's painting behind this week's people. `tools/serve.py` does it for you whenever you open the game locally, and `tools/hooks/pre-commit` can do it at every commit (the two commands to turn it on are at the top of that file). [docs/DESIGN.md](docs/DESIGN.md) explains it under "Publishing a new version".

After a push, GitHub Pages takes a minute or two to put the new version up. Reload the page to get it. A game already open in a tab carries on with the version it has.

## Layout

```
index.html        the page
css/              colors (tokens.css) and layout (game.css)
js/engine/        the engine: clock, saves, sound, dialogue, pictures, scenes, depth and walking, menus
js/art/           everything that is drawn by code: the pixel renderer (pix.js), the jointed
                  figure (rig.js), the cast (people.js), the portal, sketches and close-ups (kit.js)
js/content/       the game: cast and items (world.js), the lines (one file to an act, in lines/),
                  the story (one file to an act, in acts/), the sound list, cutscenes,
                  and the scenes (one file each)
art/              the painted pictures: a folder for each scene (scenes/), and the things
                  that can be carried (items/)
fonts/            Koine Road, the game's typeface
tools/            the storyboard page, the sprite viewer, the local server (serve.py),
                  the stamping tool (stamp.py) and the typeface's source
docs/             how it is built (DESIGN.md), who the people are (CHARACTERS.md),
                  and a puzzle document for each part of the story
```

## Type

The title is set in Koine Road, a display face made for this game. Its capitals follow the handwriting of Greek papyri from the second and third centuries, and its lowercase is written with the same pen. The font files are in `fonts/`, and `fonts/specimen.html` is a page for trying the font out. The font is built from pen strokes by the scripts in `tools/koine-road/`.

## Copyright

© 2026 n0tk3r. All rights reserved. The code, story, art and music in this repository are not licensed for reuse.
