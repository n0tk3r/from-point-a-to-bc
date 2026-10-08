// The sound list: every piece of music, every effect and every recorded line.
//
// MUSIC. Each era has a theme. Right now each theme is a short pattern that the
// engine plays on a synthesizer, so the game has sound before any music is written.
// To use a real recording, add a `src` to the track:
//
//     egypt: { src: "audio/music/egypt.{ext}", volume: 0.8 },
//
// {ext} becomes the first type in `formats` that the player's browser can play.
// MP3 plays everywhere, so that is the only type listed. Opus files are smaller: if
// you export EVERY track and voice line as .opus as well, change this to
// ["opus", "mp3"]. A listed type with a missing file is a silent track.
//
// VOICES. To make a line "talkie", record it, save it as
// audio/voice/en/<line id>.mp3 (for example audio/voice/en/egypt.river.look.mp3)
// and add the line ID to `voices` below. Lines without a recording keep showing as text.

export const sound = {
  formats: ["mp3"],
  voicePath: "audio/voice/en/",
  voices: new Set([
    // "intro.1", "intro.2", ...
  ]),

  // Pattern tracks: `scale` is semitones above `root` (a MIDI note number).
  // `lead` and `bass` list scale steps, one per beat division; null is a rest.
  music: {
    title: {
      bpm: 104, root: 57, scale: [0, 2, 4, 7, 9],
      lead: [0, null, 2, 4, null, 2, 4, null, 5, null, 4, 2, null, 0, null, null, 2, null, 4, 5, null, 4, 5, null, 7, null, 5, 4, null, 2, null, null],
      bass: [0, null, null, null, 0, null, null, null, 3, null, null, null, 3, null, null, null, 4, null, null, null, 4, null, null, null, 3, null, null, null, 3, null, 2, null],
    },
    road: {
      bpm: 92, root: 57, scale: [0, 2, 4, 7, 9],
      lead: [0, null, null, 2, null, 4, null, null, 3, null, 2, null, 0, null, null, null],
      bass: [0, null, null, null, 0, null, 3, null, 4, null, null, null, 3, null, null, null],
    },
    egypt: {
      bpm: 84, root: 50, scale: [0, 1, 4, 5, 7, 8, 10],
      lead: [0, null, 1, 4, null, 1, 0, null, 4, 5, 4, 1, 0, null, null, null, 4, null, 5, 7, null, 5, 4, null, 5, 4, 1, 0, 1, null, 0, null],
      bass: [7, null, null, null, null, null, 7, null, 7, null, null, null, null, null, 11, null],   // 7 = the octave: low notes vanish on small speakers
    },
    rome: {
      bpm: 100, root: 50, scale: [0, 2, 3, 5, 7, 9, 10],
      lead: [0, null, 0, 4, null, 4, null, 3, 4, null, 5, null, 4, null, 2, null, 0, null, 0, 4, null, 4, null, 5, 7, null, 5, 4, 2, null, 0, null],
      bass: [7, null, 11, null, 7, null, 11, null, 10, null, 7, null, 10, null, 7, null],
    },
    // home in the evening: a slow tune in three, in a minor key, waiting for a car in the drive
    home: {
      bpm: 84, root: 57, scale: [0, 2, 3, 5, 7, 8, 10], wave: "sine", hold: 2.3, volume: 0.85,
      lead: [4, null, 2, 4, null, 5, 4, null, 2, 0, null, null, 2, null, 0, 2, null, 4, 3, null, 1, 0, null, null],
      bass: [7, null, null, null, null, null, 10, null, null, null, null, null, 11, null, null, null, null, null, 7, null, null, 11, null, null],
    },
    // the Retreat, Big Sister's attic: one soft voice, very slow, in D major (five notes of it), and more silence than sound.
    // (It comes out of her sound machine, so it stops when the batteries are taken out: scenes/home-bigsis-room.js.)
    retreat: {
      bpm: 48, root: 50, scale: [0, 2, 4, 7, 9], wave: "sine", hold: 3.6, volume: 0.55,
      lead: [0, null, null, null, null, null, null, null, 2, null, null, null, null, null, null, null, 4, null, null, null, null, null, null, null, 3, null, null, null, null, null, null, null, 1, null, null, null, null, null, null, null, 3, null, null, null, null, null, null, null, 2, null, null, null, null, null, null, null, 0, null, null, null, null, null, null, null],
      bass: [5, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 8, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    },
    // the desert in the morning: wide open, not much in it
    nevada: {
      bpm: 96, root: 52, scale: [0, 2, 4, 7, 9],
      lead: [0, null, null, 2, 4, null, null, null, 4, null, 2, null, 0, null, null, null, 3, null, null, 4, 3, null, 2, null, 0, null, null, null, null, null, null, null],
      bass: [5, null, null, null, 5, null, null, 5, 8, null, null, null, 8, null, null, null],
    },
    tunnel: {
      bpm: 150, root: 57, scale: [0, 2, 4, 6, 8, 10], wave: "square", hold: 0.9, volume: 0.5,
      lead: [0, 2, 4, 5, 4, 2, 0, 2, 1, 3, 5, 6, 5, 3, 1, 3],
      bass: [0, null, null, null, 3, null, null, null],
    },
  },

  // Effects: `notes` are [MIDI note, start, length]; `noise` sweeps a filter from one pitch to another.
  sfx: {
    pickup: { notes: [[72, 0, 0.09], [79, 0.08, 0.16]], level: 0.09 },
    paint: { notes: [[62, 0, 0.07], [69, 0.06, 0.09]], level: 0.07 },
    portal: { noise: [260, 4200], len: 1.2, level: 0.32, notes: [[45, 0, 1.0], [52, 0.2, 0.8]], wave: "sawtooth" },
    flash: { noise: [5200, 300], len: 0.6, level: 0.4 },
    switch: { notes: [[76, 0, 0.05], [83, 0.05, 0.08]], level: 0.05, wave: "triangle" },
    ring: { notes: [[84, 0, 0.11], [88, 0, 0.11], [84, 0.15, 0.11], [88, 0.15, 0.11], [84, 0.30, 0.11], [88, 0.30, 0.11], [84, 0.45, 0.11], [88, 0.45, 0.11]], level: 0.045, wave: "sine" },
    beep: { notes: [[81, 0, 0.55]], level: 0.06, wave: "sine" },
    key: { notes: [[96, 0, 0.03]], level: 0.04 },
    wrong: { notes: [[52, 0, 0.14], [47, 0.14, 0.28]], level: 0.08, wave: "sawtooth" },
    found: { notes: [[72, 0, 0.1], [76, 0.1, 0.1], [79, 0.2, 0.1], [84, 0.3, 0.32]], level: 0.08, wave: "triangle" },
    plug: { notes: [[43, 0, 0.05], [67, 0.07, 0.05]], level: 0.12 },
    // Big Sister at the piano: a phrase in A minor. And Little Sister's song.
    piano: { notes: [[69, 0, 0.55], [72, 0.3, 0.55], [76, 0.6, 0.55], [74, 0.9, 0.5], [72, 1.2, 0.5], [71, 1.5, 0.8], [64, 1.5, 0.9], [69, 2.2, 1.5], [57, 2.2, 1.5], [60, 2.2, 1.5]], level: 0.1, wave: "triangle" },
    plonk: { notes: [[60, 0, 0.35], [61, 0, 0.35], [63, 0, 0.35]], level: 0.08, wave: "triangle" },

    // ---- the house, Act Three ----
    // The same phrase with one note missing: there is a key lying on that hammer. (The scene plays `thunk` where the note should be: 0.9 seconds in.)
    pianodead: { notes: [[69, 0, 0.55], [72, 0.3, 0.55], [76, 0.6, 0.55], [72, 1.2, 0.5], [71, 1.5, 0.8], [64, 1.5, 0.9], [69, 2.2, 1.5], [57, 2.2, 1.5], [60, 2.2, 1.5]], level: 0.1, wave: "triangle" },
    // Mom at the piano: the first phrase of a hymn, in F major. The tune is the game's own, written for it: it is not the tune of any real hymn.
    hymn: { notes: [[65, 0, 0.8], [53, 0, 1.3], [69, 0.6, 0.45], [67, 0.9, 0.45], [72, 1.2, 0.8], [57, 1.2, 1.3], [74, 1.8, 0.8], [70, 2.4, 0.45], [58, 2.4, 0.9], [69, 2.7, 0.45], [67, 3.0, 0.8], [48, 3.0, 0.7], [65, 3.6, 1.6], [53, 3.6, 1.6], [57, 3.6, 1.6], [60, 3.6, 1.6]], level: 0.09, wave: "triangle" },
    // The same, with its fourth note missing (the scene plays `thunk` there: 1.2 seconds in), and broken off where she stops to listen.
    hymndead: { notes: [[65, 0, 0.8], [53, 0, 1.3], [69, 0.6, 0.45], [67, 0.9, 0.45], [57, 1.2, 1.0], [74, 1.8, 0.7]], level: 0.09, wave: "triangle" },
    thunk: { noise: [240, 90], len: 0.13, q: 2, notes: [[36, 0, 0.1]], level: 0.2, wave: "sine" },                       // a hammer landing on something that is not a string
    panel: { notes: [[50, 0, 0.06], [43, 0.1, 0.12]], level: 0.1, wave: "triangle" },                                    // the piano's lower panel, lifted off
    click: { notes: [[92, 0, 0.02]], level: 0.05 },                                                                      // a flashlight's rubbery button
    deadclick: { notes: [[58, 0, 0.025]], level: 0.04, wave: "triangle" },                                                // the same button, with nothing behind it
    hush: { notes: [[74, 0, 0.5], [69, 0.16, 0.6], [62, 0.34, 1.1]], level: 0.045, wave: "sine" },                          // a sound machine winding down as its batteries come out
    unlock: { noise: [1900, 500], len: 0.16, q: 3, notes: [[86, 0, 0.03], [52, 0.13, 0.09]], level: 0.1 },                // a key turned in a door
    alarm: { notes: [[91, 0, 0.09], [86, 0.1, 0.09], [91, 0.2, 0.09], [86, 0.3, 0.09], [91, 0.4, 0.14]], level: 0.045 }, // a toy door alarm, pleased with itself
    latch: { noise: [900, 280], len: 0.1, q: 2, notes: [[47, 0, 0.05]], level: 0.09 },                                   // a door pulled shut again
    wind: { noise: [700, 2400], len: 1.4, q: 7, notes: [[74, 0.05, 0.02], [74, 0.25, 0.02], [74, 0.45, 0.02], [74, 0.65, 0.02], [74, 0.85, 0.02], [74, 1.05, 0.02], [74, 1.25, 0.02]], level: 0.06 },   // a pencil turning the hub of a cassette
    machine: { notes: [[45, 0, 0.05], [83, 0.22, 0.45]], level: 0.07, wave: "sine" },                                    // an answering machine: the clack of its play button, and its beep
    hiss: { noise: [5200, 2800], len: 1.4, q: 0.5, level: 0.08 },                                                        // tape, with nothing more on it
    dial: { notes: [[82, 0, 0.02], [82, 0.09, 0.02], [82, 0.18, 0.02], [82, 0.27, 0.02], [82, 0.36, 0.02], [82, 0.45, 0.02], [78, 0.56, 0.03]], level: 0.05 },   // a combination dial
    clunk: { noise: [520, 110], len: 0.2, q: 2, notes: [[36, 0, 0.18], [43, 0.02, 0.1]], level: 0.16, wave: "sine" },    // a cash box letting go
  },
};
