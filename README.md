# From Point A to B.C.

Dad's shortcut sends a father and son tumbling through history. A point-and-click adventure you can play in your browser.

**Play it:** https://n0tk3r.github.io/from-point-a-to-bc/

## Status

Early development. What is here now:

- **The engine**: scenes, walking, clickable areas, inventory, dialogue with choices, cutscenes that can be skipped, two playable leads, hints.
- **An intro movie** that runs into the title screen.
- **Saved games**: autosave, three slots, and a save file you can download and load on any device.
- **Sound**: music, effects and voices on separate sliders. The music is synthesized placeholder until real tracks are written. Dialogue is ready for recorded voices.
- **A short demo story** in three small acts. It is placeholder, written to exercise the engine.

Read [docs/DESIGN.md](docs/DESIGN.md) for how it all works and why. Open [tools/storyboard.html](tools/storyboard.html) to see the story and every scene laid out.

## Running locally

The game is plain HTML, CSS and JavaScript modules. There is no build step.

```
python3 -m http.server
```

Then open `http://localhost:8000`. Opening `index.html` by double-clicking will not work, because browsers only load module files from a web address.

Useful addresses while building:

- `http://localhost:8000/?intro` plays the intro again.
- `http://localhost:8000/?scene=rome-forum&lead=son` jumps straight to a scene.
- `http://localhost:8000/tools/storyboard.html` shows the storyboard.

In the game: click to walk, use and talk. Right-click (or press and hold on a touch screen) looks at things. **Esc** opens the menu or skips a cutscene. Hold **H** to see everything you can click.

## Layout

```
index.html        the page
css/              colours (tokens.css) and layout (game.css)
js/engine/        the engine: clock, saves, sound, dialogue, scenes, menus
js/art/kit.js     the drawing kit every scene is built from
js/content/       the game: cast, lines, story, sound list, cutscenes, scenes (one file each)
fonts/            Koine Road, the game's typeface
tools/            the storyboard page and the typeface's source
docs/DESIGN.md    how it is built
```

## Type

The title is set in Koine Road, a display face made for this game. Its capitals follow the handwriting of Greek papyri from the second and third centuries, and its lowercase is written with the same pen. The font files are in `fonts/`, and `fonts/specimen.html` is a page for trying the font out. The font is built from pen strokes by the scripts in `tools/koine-road/`.

## Copyright

© 2026 n0tk3r. All rights reserved. The code, story, art and music in this repository are not licensed for reuse.
