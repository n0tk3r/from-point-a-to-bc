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
    // NEVADA-12SC: the Last Stop Rag, Grandpa Joe's own tune, hummed (no words) under his breath in the limousine
    // (js/content/scenes/nevada-limo.js, while "limo.singing"). The notes are the phrase his banjo plays on the porch (the
    // sfx "banjo", NEVADA-12SA: B D G E D B C E D B A G over G, D, C, D, a note every fifth of a second), so it is the
    // same tune, round and round. The game's own, not any real song's.
    rag: {
      bpm: 150, root: 55, scale: [0, 2, 4, 5, 7, 9, 11], wave: "triangle", hold: 1.2, volume: 0.7,
      lead: [2, 4, 7, 5, 4, 2, 3, 5, 4, 2, 1, 0],
      bass: [7, null, null, 11, null, null, 10, null, null, 11, null, null],
    },
    // ROME-13S3: across the Tiber (js/content/scenes/rome-tiber.js), the act's own quiet: Rome's mode (D dorian, as `rome`),
    // one soft voice, slow, and more rests than notes, like water going by under a bridge. The game's own tune, written for
    // it: not any real song or hymn. (It drops while the old man talks with the boy, and the river is heard instead.)
    tiber: {
      bpm: 60, root: 50, scale: [0, 2, 3, 5, 7, 9, 10], wave: "sine", hold: 3.2, volume: 0.55,
      lead: [4, null, null, 3, null, null, 2, null, 3, null, null, null, null, null, null, null, 2, null, null, 1, null, null, 0, null, 1, null, null, null, null, null, null, null,
        0, null, null, 2, null, null, 4, null, 5, null, null, 4, null, null, null, null, 3, null, null, 2, null, null, 1, null, 0, null, null, null, null, null, null, null],
      bass: [7, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 11, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null,
        10, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 11, null, null, null, null, null, null, null, 7, null, null, null, null, null, null, null],
    },
    // ENGINE-17: the Office's own tune, for its five scenes: the polite music a building plays to people who are waiting, a
    // little flat (`detune`: its tune a fifth of a semitone low, as a tape that has been played too often), quiet under talk.
    // A soft electric-piano voice falls by steps down a plain F major sequence (A C E D C, then G Bb D C Bb, and round),
    // over a bass that walks F, C, Bb, F, G, D, C, F. Written for the game: not any real song.
    office: {
      bpm: 84, root: 53, scale: [0, 2, 4, 5, 7, 9, 11], wave: "sine", hold: 2.1, volume: 0.42, detune: -20,
      lead: [2, null, 4, null, 6, null, 5, 4, null, null, 2, null, 3, null, null, null, 1, null, 3, null, 5, null, 4, 3, null, null, 1, null, 2, null, null, null],
      bass: [7, null, null, null, 4, null, null, null, 3, null, null, null, 0, null, null, null, 1, null, null, null, 5, null, null, null, 4, null, null, null, 7, null, null, null],
    },
    // ENGINE-17: the Last Stop Rag (`rag`, above: the same notes) on the pie-tin banjo: a tin head is bright and hard, so a
    // square wave, each note short and plucked, a little louder than his humming. Grandpa Joe's own tune, never sung.
    "rag-tin": {
      bpm: 150, root: 55, scale: [0, 2, 4, 5, 7, 9, 11], wave: "square", hold: 0.55, volume: 0.5,
      lead: [2, 4, 7, 5, 4, 2, 3, 5, 4, 2, 1, 0],
      bass: [7, null, null, 11, null, null, 10, null, null, 11, null, null],
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
    // A foam dart leaving a toy blaster: a short breath of air that drops in pitch, and the soft pop of the spring.
    thwip: { noise: [5200, 1400], len: 0.09, q: 2.6, notes: [[88, 0, 0.018], [81, 0.016, 0.028], [74, 0.04, 0.035]], level: 0.075, wave: "triangle" },
    latch: { noise: [900, 280], len: 0.1, q: 2, notes: [[47, 0, 0.05]], level: 0.09 },                                   // a door pulled shut again
    wind: { noise: [700, 2400], len: 1.4, q: 7, notes: [[74, 0.05, 0.02], [74, 0.25, 0.02], [74, 0.45, 0.02], [74, 0.65, 0.02], [74, 0.85, 0.02], [74, 1.05, 0.02], [74, 1.25, 0.02]], level: 0.06 },   // a pencil turning the hub of a cassette
    machine: { notes: [[45, 0, 0.05], [83, 0.22, 0.45]], level: 0.07, wave: "sine" },                                    // an answering machine: the clack of its play button, and its beep
    hiss: { noise: [5200, 2800], len: 1.4, q: 0.5, level: 0.08 },                                                        // tape, with nothing more on it
    dial: { notes: [[82, 0, 0.02], [82, 0.09, 0.02], [82, 0.18, 0.02], [82, 0.27, 0.02], [82, 0.36, 0.02], [82, 0.45, 0.02], [78, 0.56, 0.03]], level: 0.05 },   // a combination dial
    clunk: { noise: [520, 110], len: 0.2, q: 2, notes: [[36, 0, 0.18], [43, 0.02, 0.1]], level: 0.16, wave: "sine" },    // a cash box letting go

    // ---- the Last Stop, Act Four (NEVADA-12SA) ----
    // A phrase of the Last Stop Rag on Grandpa Joe's banjo: plucked notes over a bass on the beat. The tune is the game's own
    // (it is not any real song). One phrase lasts one pass of his strum (2.4 seconds: `strum` in js/art/rig.js), so the
    // roadside plays it once a pass while he plays.
    banjo: { notes: [[55, 0, 0.5], [71, 0, 0.2], [74, 0.2, 0.2], [79, 0.4, 0.28], [62, 0.6, 0.45], [76, 0.6, 0.2], [74, 0.8, 0.2], [71, 1.0, 0.28],
      [60, 1.2, 0.5], [72, 1.2, 0.2], [76, 1.4, 0.2], [74, 1.6, 0.28], [62, 1.8, 0.45], [71, 1.8, 0.2], [69, 2.0, 0.2], [67, 2.2, 0.4]], level: 0.07, wave: "triangle" },

    // ---- NEVADA-12SC: the cut-scene "Backup" ----
    // Grandpa Joe's banjo coming down over Jed's head: one twang, every string at once (the five of a banjo tuned to G),
    // and the thump of the head going through. Nobody is hurt: it is a banjo.
    twang: { noise: [900, 180], len: 0.16, q: 1.6, notes: [[67, 0, 0.8], [50, 0, 0.95], [55, 0, 0.9], [59, 0, 0.85], [62, 0, 0.8]], level: 0.045, wave: "sawtooth" },

    // ---- CAR-13E: inside the wagon, Act One (the car also has latch, clunk, hiss and click, above) ----
    // The wagon's horn: two square-wave notes a major third apart (E and G sharp), dying away over half a second, not loud. A
    // touch sour is in character. (At 0.08 it was as loud as the hiss, the loudest of the car's sounds: 0.06 puts it between
    // the hiss and the clunk.)
    horn: { notes: [[64, 0, 0.5], [68, 0, 0.5]], level: 0.06, wave: "square" },
    // The starter, grinding and giving up: a low sweep of noise with four short pulses under it, about a second. (Quieter
    // than the clunk and louder than the latch: as it was designed.)
    starter: { noise: [180, 700], len: 0.9, q: 2, notes: [[38, 0, 0.08], [38, 0.16, 0.08], [38, 0.32, 0.08], [38, 0.48, 0.08]], level: 0.12, wave: "sawtooth" },

    // ---- ROME-13S2: Juno's geese, on the Capitol (js/content/scenes/rome-capitol.js) ----
    honk: { notes: [[62, 0, 0.09], [60, 0.1, 0.12]], level: 0.07, wave: "square" },                                       // one goose: two short nasal notes
    // The flock running for their pen after the stomp: a flurry of honks over the beat of wings. Nobody is hurt.
    geese: { noise: [3000, 900], len: 0.9, q: 1.5, notes: [[62, 0, 0.08], [60, 0.09, 0.1], [65, 0.22, 0.08], [63, 0.31, 0.1], [61, 0.45, 0.08], [59, 0.54, 0.12], [64, 0.7, 0.08], [62, 0.79, 0.12]], level: 0.08, wave: "square" },
    goosehiss: { noise: [4200, 2600], len: 0.5, q: 0.7, level: 0.05 },                                                     // a goose's hiss, short: every neck out at once

    // ---- ROME-13S3: across the Tiber ----
    // The river, as the music drops for the old man's talk: a soft rush of water, a few seconds, and gone.
    river: { noise: [500, 900], len: 3, q: 0.8, level: 0.025 },

    // ---- MAP-15: the map, and the Timer (js/engine/atlas.js) ----
    notch: { noise: [2600, 1500], len: 0.035, q: 3, notes: [[88, 0, 0.016]], level: 0.03 },           // the dial clicking into a notch: short and dry, quieter than `dial` (the vault's)
    ding: { notes: [[93, 0, 1.1], [100, 0, 0.45], [105, 0, 0.18]], level: 0.026, wave: "sine" },      // the dial arriving at its time: a small bell, once (softer than `pickup` and `found`)
    rustle: { noise: [1800, 5200], len: 0.3, q: 0.9, level: 0.06 },                                     // the map opened, or put away: paper

    // ---- ENGINE-17: the Office (stage one), every one made by code, the game's own. (The game had a `thunk`, the piano's
    // dead note and the limousine's divider, and a `twang`, the banjo over Jed's head in "Backup": both kept as they were.
    // So the rubber date stamp is `stamp`, and the pie-tin banjo's string is `twang-tin`.) A note may slide: [note, start,
    // length, the note it slides to] (audio.js). ----
    // A steel trash can tipped over onto gravel: the crunch of the gravel, the clang of the can (notes that are not in tune
    // with one another, as struck metal is not), and the lid rattling after.
    clang: { noise: [2600, 700], len: 0.55, q: 0.9, notes: [[83, 0, 0.42], [90, 0.005, 0.36], [94, 0.01, 0.3], [79, 0.17, 0.3], [86, 0.18, 0.24], [88, 0.31, 0.14], [84, 0.4, 0.12]], level: 0.055, wave: "triangle" },
    // A wing nut turned: a short squeal of metal on metal, rising, twice.
    squeak: { noise: [5200, 6400], len: 0.24, q: 6, notes: [[88, 0, 0.09, 91], [89, 0.12, 0.1, 93]], level: 0.028, wave: "triangle" },
    // A big fan running down: the rush of its air falling away over a few seconds, and the hum of its motor sliding down under it.
    fanstop: { noise: [900, 70], len: 2.6, q: 1.1, notes: [[45, 0, 2.5, 28], [57, 0, 2.2, 40]], level: 0.06, wave: "sawtooth" },
    // A rubber date stamp coming down on a counter: THUNK. A dull, solid knock and the counter's thump under it.
    stamp: { noise: [420, 140], len: 0.12, q: 1.5, notes: [[40, 0, 0.13], [33, 0.012, 0.11]], level: 0.16, wave: "sine" },
    // An intercom's press-to-talk: the click of the button, and its buzz while it is held.
    buzz: { noise: [3200, 2800], len: 0.05, q: 2, notes: [[47, 0.01, 0.34], [59, 0.01, 0.34]], level: 0.03, wave: "square" },
    // The building's speakers clearing their throat: two soft notes, down a fourth, before every line on them (g.pa).
    pa: { notes: [[79, 0, 0.7], [74, 0.38, 1.0]], level: 0.04, wave: "sine" },
    // A raccoon and a pie: one short, happy slurp.
    slurp: { noise: [700, 2600], len: 0.32, q: 3, notes: [[60, 0, 0.24, 72]], level: 0.05, wave: "sine" },
    // One string of a banjo with a pie tin for a head: a hard, bright, loud pluck (the old `twang` is every string, and dull).
    "twang-tin": { noise: [6000, 2500], len: 0.05, q: 1, notes: [[74, 0, 0.9], [86, 0, 0.5], [93, 0, 0.25]], level: 0.07, wave: "square" },
  },
};
