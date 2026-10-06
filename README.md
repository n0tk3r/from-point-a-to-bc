# From Point A to B.C.

Dad's shortcut sends a father and son tumbling through history, and the rest of the family sets out to fetch them. A point-and-click adventure you can play in your browser.

**Play it:** https://n0tk3r.github.io/from-point-a-to-bc/

## Status

Early development. What is here now:

- **The engine**: scenes, walking, clickable areas, inventory, dialogue with choices, cutscenes that can be skipped, close-ups, hints.
- **Five playable leads**: Dad and the Son, lost in different centuries, and Mom, Big Sister and Little Sister, who work as a team in one scene. You switch between them with their portraits. Each can do something the others cannot, and they talk to each other and hand things over.
- **Pixel-art characters drawn by code**: each is a jointed figure that walks in eight directions, talks with its hands, reaches and bends, and each stands, walks and gestures in a way of their own. There are no picture files.
- **Depth**: people walk behind things and in front of them, round obstacles, and get smaller as they walk away.
- **An intro movie** that runs into the title screen.
- **Saved games**: autosave, three slots, and a save file you can download and load on any device.
- **Sound**: music, effects and voices on separate sliders. The music is synthesized placeholder until real tracks are written. Dialogue is ready for recorded voices.
- **A short demo story**: a prologue and four small acts (Egypt, Rome, home in the present, the Nevada desert). It is placeholder, written to exercise the engine.

Read [docs/DESIGN.md](docs/DESIGN.md) for how it all works and why, [docs/CHARACTERS.md](docs/CHARACTERS.md) for who the family are and how each of them talks, and [docs/PUZZLES-the-present.md](docs/PUZZLES-the-present.md) for the present-day chapter laid out puzzle by puzzle. Open [tools/storyboard.html](tools/storyboard.html) to see the story and every scene laid out, and [tools/sprites.html](tools/sprites.html) to see every character moving.

## Running locally

The game is plain HTML, CSS and JavaScript modules. There is no build step.

```
python3 -m http.server
```

Then open `http://localhost:8000`. Opening `index.html` by double-clicking will not work, because browsers only load module files from a web address.

Useful addresses while building:

- `http://localhost:8000/?intro` plays the intro again.
- `http://localhost:8000/?scene=rome-forum&lead=son` jumps straight to a scene.
- `http://localhost:8000/?scene=home-living-room` starts the present-day chapter, and `?scene=nevada-roadside` its second half.
- `http://localhost:8000/tools/storyboard.html` shows the storyboard.
- `http://localhost:8000/tools/sprites.html` shows every character and prop, in every direction, moving.

In the game: click to walk, use and talk. Right-click (or press and hold on a touch screen) looks at things. Click a portrait at the top left (or press **1**, **2**, **3**) to play as someone else. Click one of the others to talk to her; pick something up from your pockets and click her to hand it over. **Esc** opens the menu or skips a cutscene. Hold **H** to see everything you can click.

## Layout

```
index.html        the page
css/              colors (tokens.css) and layout (game.css)
js/engine/        the engine: clock, saves, sound, dialogue, scenes, depth and walking, menus
js/art/           everything that draws: backdrops (kit.js), the pixel renderer (pix.js),
                  the jointed figure (rig.js), the cast (people.js), props (props.js)
js/content/       the game: cast, lines, story, sound list, cutscenes, scenes (one file each)
fonts/            Koine Road, the game's typeface
tools/            the storyboard page, the sprite viewer and the typeface's source
docs/             how it is built (DESIGN.md), who the family are (CHARACTERS.md),
                  and the present-day chapter as a puzzle document (PUZZLES-the-present.md)
```

## Type

The title is set in Koine Road, a display face made for this game. Its capitals follow the handwriting of Greek papyri from the second and third centuries, and its lowercase is written with the same pen. The font files are in `fonts/`, and `fonts/specimen.html` is a page for trying the font out. The font is built from pen strokes by the scripts in `tools/koine-road/`.

## Copyright

© 2026 n0tk3r. All rights reserved. The code, story, art and music in this repository are not licensed for reuse.
