# From Point A to B.C.

Dad's shortcut sends a father and son tumbling through history, and the rest of the family sets out to fetch them. A point-and-click adventure you can play in your browser.

**Play it:** https://n0tk3r.github.io/from-point-a-to-bc/

## Status

In development. What is here now:

- **The engine**: scenes, walking, clickable areas, inventory, dialogue with choices and talks that branch and remember, cutscenes that can be skipped, close-ups, hints, and a small door in time that things and voices can pass through.
- **Painted scenes**: every scene is one painted picture, 800 pixels by 600, with painted cut-outs for the things people walk behind and the things the story changes. The highway of the intro and all nineteen scenes of the story are painted: five in Egypt (the inside of the wagon among them, seen through Dad's own eyes), six in Rome, the five rooms of the house, and in Nevada the roadside, the store and the back of a limousine.
- **Seven playable leads**: Dad and the Son, lost in different centuries; Mom, Big Sister and Little Sister, who work as a team; and, in Act Five, Grandpa Joe and his raccoon, Ranger, a team of two. You switch between them with their portraits. Each can do something the others cannot, and they talk to each other and hand things over.
- **Pixel-art people drawn by code**: each of the thirty-eight is a jointed figure that walks in eight directions, talks with its hands, reaches, bends and sits, and each stands, walks and gestures in a way of their own. There are no picture files of people. Ranger, who is a raccoon, is painted frame by frame.
- **Depth**: people walk behind things and in front of them, round obstacles, and get smaller as they walk away.
- **An intro movie** that runs into the title screen.
- **Saved games**: autosave, three slots, and a save file you can download and load on any device.
- **Sound**: music, effects and voices on separate sliders. The music is synthesized placeholder until real tracks are written. Dialogue is ready for recorded voices.
- **The story so far**: a prologue, four acts, and the opening of a fifth. Each leads into the next, from the intro to the end of the demo:
  - **Prologue: The Shortcut.** The intro movie: Dad takes a shortcut, and the wagon drives into a hole in time.
  - **Act One: Scattered** (Egypt, five scenes). Dad, alone by the Nile, gets into his wagon for the road map in the glovebox, gets into the pyramid, and brings a sunbeam round three corners to open the humming wall.
  - **Act Two: Meanwhile** (Rome, six scenes). The Son, on the Ides of March, 44 B.C., runs errands across the Forum, up the Capitol and over the Tiber to get back into the temple of Saturn, and, with its owner's leave, tosses a silver coin through a door its own size.
  - **Act Three: Five Places Set** (the five rooms of the house). Mom, Big Sister and Little Sister find out where Dad's phone was last seen and what he last said.
  - **Act Four: The Last Stop Before Nothing** (Nevada: the roadside and the store). Grandpa Joe, Grandma Jolene, Ranger the raccoon and five hens; a door the size of a coin, and the Son's voice through it; a door as wide as a windshield, and the walk through. Then the cut-scene "Backup".
  - **Act Five: Everybody's Grandpa**, its opening (the back of a limousine). Grandpa Joe and Ranger, taken by the men in gray. The demo ends at the gate of the Office Of Peculiar Sectors.

Read [docs/DESIGN.md](docs/DESIGN.md) for how it all works and why, and [docs/CHARACTERS.md](docs/CHARACTERS.md) for who the people are and how each of them talks. The acts are laid out puzzle by puzzle in [docs/PUZZLES-egypt.md](docs/PUZZLES-egypt.md), [docs/PUZZLES-rome.md](docs/PUZZLES-rome.md) and [docs/PUZZLES-the-present.md](docs/PUZZLES-the-present.md). Open [tools/storyboard.html](tools/storyboard.html) to see the story, a map of each act's places, and every scene laid out, and [tools/sprites.html](tools/sprites.html) to see every character moving.

## Running locally

The game is plain HTML, CSS and JavaScript modules. There is no build step.

```
python3 tools/serve.py
```

Then open `http://localhost:8000`. Opening `index.html` by double-clicking will not work, because browsers only load module files from a web address. (`python3 -m http.server` works too. `tools/serve.py` differs in telling the browser to keep no copies of files, so you always see them as they are now.)

Useful addresses while building:

- `http://localhost:8000/?intro` plays the intro again.
- `http://localhost:8000/?scene=rome-street&lead=son` jumps straight to a scene. Add `&flags=rome.arrived,rome.sawStreet` to start with more of the story done (`?scene=rome-forum&lead=son&flags=rome.arrived,rome.knowsBC` is the Forum, and `?scene=egypt-car&lead=dad&flags=egypt.arrived` the inside of the wagon).
- `http://localhost:8000/?scene=home-living-room` starts the present-day chapter, `?scene=nevada-roadside` Act Four (`?scene=nevada-store&lead=mom&flags=nevada.arrived` its store), and `?scene=nevada-limo&lead=grandpajoe` the opening of Act Five.
- `http://localhost:8000/?scene=engine-proof` is the worked example of a painted scene.
- `http://localhost:8000/tools/storyboard.html` shows the storyboard.
- `http://localhost:8000/tools/sprites.html` shows every character and prop, in every direction, moving.

In the game: click to walk, use and talk. Right-click (or press and hold on a touch screen) looks at things. What the person you are playing carries is along the bottom left; click a thing there, then click what to use it with. Click a portrait at the top left (or press **1**, **2**, **3**) to play as someone else. Click one of the others to talk to them; to hand them something, click the thing and then click them, or their portrait. **Esc** opens the menu or skips a cutscene. Hold **H** to see everything you can click.

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
js/engine/        the engine: clock, saves, sound, dialogue, pictures, scenes, depth and walking, menus,
                  and the things that move by nature, the doors in time among them (effects.js)
js/art/           everything that is drawn by code: the pixel renderer (pix.js), the jointed
                  figure (rig.js), the cast (people.js), the neon rings, sketches and close-ups
                  (kit.js); and the list of those painted frame by frame instead (painted.js)
js/content/       the game: cast and items (world.js), the lines (one file to an act, in lines/),
                  the story (one file to an act, in acts/), the talks written as dialogue
                  trees (talk/), the sound list, cutscenes, and the scenes (one file each)
art/              the painted pictures: a folder for each scene (scenes/), the things
                  that can be carried (items/), the painted portraits (portraits/), the
                  engine's own pictures for its proof scene (proof/), and the game's emblem,
                  a sunset kitchen-timer dial, for the begin screen and the browser tab (emblem/)
fonts/            Koine Road, the game's typeface
tools/            the storyboard page (the story, a map of each act's ways, every scene),
                  the sprite viewer, the local server (serve.py),
                  the stamping tool (stamp.py), the painter (paint/: the scripts that
                  paint every picture) and the typeface's source
docs/             how it is built (DESIGN.md), who the people are (CHARACTERS.md),
                  and a puzzle document for each part of the story
```

## Type

The title is set in Koine Road, a display face made for this game. Its capitals follow the handwriting of Greek papyri from the second and third centuries, and its lowercase is written with the same pen. The font files are in `fonts/`, and `fonts/specimen.html` is a page for trying the font out. The font is built from pen strokes by the scripts in `tools/koine-road/`.

## Copyright

© 2026 n0tk3r. All rights reserved. The code, story, art and music in this repository are not licensed for reuse.
