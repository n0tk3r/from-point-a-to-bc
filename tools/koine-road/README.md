# Koine Road

The display typeface for From Point A to B.C.: Latin letters written the way a scribe wrote Greek on papyrus around A.D. 200. The models are Papyrus 46 and Papyrus 52.

## Rebuild the font

```
python3 -m pip install fonttools shapely numpy brotli
python3 build.py
```

This writes `fonts/KoineRoad-Regular.woff2` and `fonts/KoineRoad-Regular.ttf` at the top of the repo. The game loads the `.woff2`. The `.ttf` is for installing on a computer so other programs can use the font. Open `fonts/specimen.html` afterwards to check the result.

The build is deterministic. The same skeletons always produce the same outlines.

## Change a letter

Each letter in `glyphs.py` is a list of pen strokes. Each stroke is a list of points along the centre of the stroke. The grid has 1000 units per em and the baseline is at 0. Capitals are about 636 units tall, the x-height is about 480, ascenders reach about 690 and descenders about -230.

- `(x, y)` is a point the pen passes through. The path between points is smoothed.
- `(x, y, "c")` is a sharp corner.
- A dict as the first item of a stroke changes the pen for that stroke. `BAR` makes a bar that runs dry towards its end.
- `stem(x)` makes a vertical with a small flag at the head and a hooked foot. `stem(x, top=XT)` is a short stem and `stem(x, top=ASC)` is an ascender.
- `arc(...)` makes part of an ellipse, for the round letters.
- `opts=LC` on a glyph uses the finer lowercase pen.

Settings that affect every letter are at the top of `build.py`: the pen width, how much ink pools at the ends of strokes, the kerning pairs, and how many times each letter is written (`NVAR`). `penlib.py` is the pen itself: it turns a centre line into an inked outline, fills the corners where strokes meet, and roughens the edge.

## What comes from the papyri

- A is shaped like alpha, with a pointed loop.
- E and C are the rounded forms scribes used.
- M is the rounded mu.
- P is shaped like rho and drops below the line.
- W is shaped like omega.
- O is written small.
- Stems start with a small flag and end in a hook, and the ink pools where the pen lands.

F, G, J, L, Q, R, S, U and V are not in the Greek alphabet, so they are drawn with the same pen.

## What is new

The papyri have capitals only, so the lowercase is new. It is written with the same pen, held a little finer. Where a Greek letter looks like ours it lends its shape: a from alpha, e from the rounded epsilon and w from omega. The d leans back, as it does in early Latin book hands.

Two things happen as you type:

- Each letter is written three slightly different ways, and the font cycles through them so repeated letters don't look stamped.
- The small O is right for text in capitals. When a capital O starts a word in lowercase, as in "Oh", the font swaps in a full-height O so it still reads as a capital.

Both are part of the font's `calt` feature, which browsers apply by default.
