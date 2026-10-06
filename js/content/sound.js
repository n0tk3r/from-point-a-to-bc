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
  },
};
