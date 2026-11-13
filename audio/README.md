# Sound files

Nothing has to be in this folder for the game to run. A scene with no recording plays its
synthesized theme (the patterns in `js/content/sound.js`), and dialogue shows as text.

## Music (MUSIC-24)

```
music-src/                  your masters: kept out of git (it is in .gitignore). Keep them backed up.
  egypt.wav                 a WAV (or FLAC or AIFF) from any music program, named after the track
  egypt.txt                 where it loops, and anything else about it
audio/music/                made by the tool, committed, served with the game
  egypt.webm                Opus, 96 kbps: what most browsers play
  egypt.m4a                 AAC, 128 kbps: for browsers that cannot decode the Opus copy (older iPhones and Macs)
js/content/music-files.js   made by the tool: the list the game reads. Never edit it by hand.
```

### 1. Export the track

- Write the intro (if there is one) and the loop. Export from the very start to **a few seconds past the
  loop's end**: those seconds are the reverb ringing out, and the tool folds them back onto the loop's
  start, so the seam sounds like the music going round rather than a cut.
- WAV, 44.1 or 48 kHz, 16- or 24-bit. Leave about 1 dB of headroom and do not squash it loud: the tool
  sets every track to the same loudness.
- Loops of one to three minutes. While a track plays it is held decoded, about 22 MB a minute. An
  ambient bed can be mono.

### 2. Name it

- The file's name is the track's name: lowercase letters, digits and hyphens (`egypt.wav`, `edo-sea.wav`).
- Named after a theme the game already plays, it replaces that theme everywhere: `title`, `road`,
  `tunnel`, `egypt`, `rome`, `tiber`, `home`, `retreat`, `nevada`, `rag`, `office`, `rag-tin`, `edo`,
  `edo-sea`, `edo-city`, `edo-shosha`, `edo-keep`, `edo-hidden`, `edo-theatre`. The music page
  (`tools/music.html`) shows which scenes play which.
- Any other name plays in the scenes its text file lists under `scenes:`.

### 3. Say where it loops: the text file

```
title:  Desert Dawn
by:     Ilya
bpm:    84
meter:  4            # beats in a bar
intro:  4 bars       # the part that plays once; or how long it is (0:11.43); or none
loop:   32 bars      # how long the part that repeats is; or a length (1:31.43)
volume: 0.9          # 1 is the house loudness; lower for a quiet theme
fade:   1.5          # seconds of cross-fade in and out (1.2 if not given)
scenes: egypt-crash, egypt-site     # only for a name that is not a theme's
```

- Or give the loop as times in the file: `loop start: 0:11.43` and `loop end: 1:42.86`.
- `downbeat: 0:00.35` if the first bar does not begin at the very start (bars are counted from it).
- `loop: none`: the piece plays once (a short cue, a cut-scene's music).
- `stream: yes`: a long piece is streamed instead of held in memory; it then loops whole, or plays once.
- `quality: high`: 128 kbps Opus and 160 kbps AAC, for dense orchestral pieces.
- `#` starts a note to yourself.
- With no text file, or nothing about the loop in it, the loop stored in the file itself is used: a WAV's
  own loop, or `LOOPSTART` and `LOOPLENGTH` tags in an Ogg file, counted in samples (as RPG Maker's
  engines use them). With neither, the whole file loops.
- A scene whose story decides its music (the limousine's Rag, Big Sister's sound machine, the pie-tin
  banjo in the Comfortable Room) keeps deciding. Replace the themes it plays (`rag`, `retreat`,
  `rag-tin`) by name instead.

### 4. Run the tool

```
python3 tools/music/add_music.py              every new or changed track in music-src/
python3 tools/music/add_music.py egypt        just that one
python3 tools/music/add_music.py --all        every track, changed or not
python3 tools/music/add_music.py --list       what the game has now
python3 tools/music/add_music.py --remove egypt
```

It needs Python 3 and ffmpeg (Linux: `sudo apt install ffmpeg`; Mac: `brew install ffmpeg`). For each
track it works out the loop to the sample, folds the tail back, sets the loudness (-18 LUFS, peaks under
-1 dB; nothing is compressed), makes the two copies, checks they decode to the right length, and writes
the list. It prints what it did and which scenes will play the track, and says plainly when something
needs putting right. A track whose master is not on this computer keeps its files and its entry as they are.

### 5. Listen, then commit

- Run `python3 tools/serve.py` and open http://localhost:8000/tools/music.html.
  - **Play** each track.
  - **Hear the seam** plays the last five seconds of the loop going round into its start.
  - **Check every copy** decodes both copies in that browser. Open the page once in Safari and Firefox too.
  - The page also lists every scene with the music it plays.
- Then commit `audio/music/`, `js/content/music-files.js` and the stamped pages (`python3 tools/stamp.py`).
  The masters stay in `music-src/`.

### How the game plays it

`js/engine/audio.js`:

- **Fetching:** a scene's recording is fetched when the scene is near (with the pictures of the places
  next door), then decoded. The browser takes the Opus copy, or the AAC copy if it cannot decode the Opus one.
- **The loop:** the intro plays once and the loop goes round to the sample (the Web Audio API's own loop points).
- **Changing tracks:** the same track carries on from room to room. A different one cross-fades, and the
  track before it plays on until the new one is ready.
- **Volume:** recorded music plays at `recordedLevel` in `sound.js` (0.45, which sits beside the
  synthesized themes and the effects), times the track's own `volume`, under the music slider.
- **Fallback:** a recording that cannot be had falls back to the theme's synthesized pattern.

## Effects and voices

```
audio/sfx/<effect>.mp3             short effects (still all synthesized: js/content/sound.js `sfx`)
audio/voice/en/<line id>.mp3       one file per spoken line, named after its ID
                                   for example: audio/voice/en/egypt.river.look.mp3
```

To make a line spoken, add the recording here and add the line's ID to the `voices` list in
`js/content/sound.js`. Trim silence from the start of voice lines so speech begins the moment the words
appear.
