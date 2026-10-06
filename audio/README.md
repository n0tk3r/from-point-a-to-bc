# Sound files

Nothing has to be in this folder for the game to run. Until recordings exist, the
engine plays synthesized placeholder music and shows dialogue as text.

```
audio/music/<track>.mp3            one file per theme, named in js/content/sound.js
audio/sfx/<effect>.mp3             short effects
audio/voice/en/<line id>.mp3       one file per spoken line, named after its ID
                                   for example: audio/voice/en/egypt.river.look.mp3
```

To switch a theme from the synthesizer to a recording, give it a `src` in
`js/content/sound.js`. To make a line spoken, add the recording here and add the
line's ID to the `voices` list in the same file.

MP3 plays in every browser, so the game asks for `.mp3` only. Opus files are
smaller: if you export every track and line as `.opus` too, set `formats` to
`["opus", "mp3"]` in `js/content/sound.js` and each browser takes the one it can play.

Keep long music as files of a few megabytes at most (128 kbps MP3 is plenty for
this style), and trim silence from the start of voice lines so speech begins the
moment the words appear.
