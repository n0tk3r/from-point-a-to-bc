// Sound: music, effects and voices, each on its own volume slider.
//
//   master ── music ── (each track fades in and out on its own gain)
//          ├─ sfx
//          └─ voice     while a voice plays, the music is turned down ("ducking")
//
// Browsers keep sound off until the player clicks or presses a key, so unlock()
// must be called from that first click.
//
// Until real recordings exist, every track is a short synthesized placeholder
// described in js/content/sound.js. Give a track a `src` there and the engine
// streams that file instead. Nothing else in the game has to change.
//
// MUSIC-24: recorded music. A track with a recording (sound.files, the list js/content/music-files.js that
// tools/music/add_music.py makes from the masters in music-src/; audio/README.md) is fetched, decoded and played with the
// Web Audio API's own loop: its intro once, then round and round between its loop points, to the sample. The browser takes
// the first copy it can decode (`musicFormats`: Opus in WebM, then AAC), and a track it cannot have at all falls back to
// its synthesized pattern, if it has one. While a recording loads, the track before it goes on; then the two cross-fade.

const NOTE = (midi) => 440 * Math.pow(2, (midi - 69) / 12);

export class AudioEngine {
  constructor(settings, sound) {
    this.settings = settings;
    this.sound = sound;          // { music: {...}, sfx: {...}, voices: Set, voicePath, formats } (MUSIC-24: files, sceneMusic, musicFormats, recordedLevel)
    this.ctx = null;
    this.current = null;         // { id, gain, stop } (MUSIC-24: the track asked for; it may still be loading)
    this.live = [];              // MUSIC-24: every track that is sounding (the current one, and those fading out)
    this.bytes = new Map();      // MUSIC-24: recordings fetched, "<id>.<format>" -> Promise of the file's bytes (a few, newest last)
    this.decoded = new Map();    // MUSIC-24: recordings decoded, id -> Promise of { buffer, format, shift } (two kept, besides those sounding)
    this.badFormats = new Set(); // MUSIC-24: copies this browser turned out not to decode (it is asked for the next one from then on)
    this.voiceEl = null;
    this.wanted = null;          // music asked for before sound was unlocked
  }

  get ready() { return !!this.ctx && this.ctx.state === "running"; }

  unlock() {
    if (!this.ctx) {
      const Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return;          // very old browser: the game simply stays silent
      this.ctx = new Ctx();
      const bus = () => this.ctx.createGain();
      this.master = bus(); this.musicBus = bus(); this.sfxBus = bus(); this.voiceBus = bus(); this.duck = bus();
      this.duck.connect(this.musicBus);
      for (const b of [this.musicBus, this.sfxBus, this.voiceBus]) b.connect(this.master);
      this.master.connect(this.ctx.destination);
      this.applyVolumes();
      this.ext = this.pickFormat();
    }
    if (this.ctx.state === "suspended") this.ctx.resume();
    if (this.wanted) { const id = this.wanted; this.wanted = null; this.music(id); }
  }

  /** Stop all sound while the tab is hidden, and carry on when it comes back. */
  hush(on) {
    if (!this.ctx) return;
    if (on) this.ctx.suspend(); else this.ctx.resume();
    if (on) this.stopVoice();
  }

  /** The first file type this browser can play, from the list in sound.js. */
  pickFormat() {
    const probe = document.createElement("audio");
    const types = { opus: 'audio/ogg; codecs="opus"', ogg: 'audio/ogg; codecs="vorbis"', m4a: 'audio/mp4; codecs="mp4a.40.2"', mp3: "audio/mpeg" };
    return (this.sound.formats || ["mp3"]).find((ext) => probe.canPlayType(types[ext] || "")) || "mp3";
  }

  applyVolumes() {
    if (!this.ctx) return;
    const s = this.settings, t = this.ctx.currentTime;
    this.musicBus.gain.setTargetAtTime(s.music, t, 0.05);
    this.sfxBus.gain.setTargetAtTime(s.sfx, t, 0.05);
    this.voiceBus.gain.setTargetAtTime(s.voice, t, 0.05);
  }

  // ---------- music ----------
  /** MUSIC-24: whether a track of that name exists (a recording, or a synthesized pattern). */
  has(id) { return !!this.recording(id) || !!(id && this.sound.music && this.sound.music[id]); }
  /** MUSIC-24: a track's recording (its entry in js/content/music-files.js), or null. */
  recording(id) { return (id && this.sound.files && this.sound.files[id]) || null; }

  /** Cross-fade to a track. Asking for the track that is already playing does nothing.
      MUSIC-24: `fade` defaults to the recording's own (else 1.2 s). A recording is fetched and decoded first, and the track
      that was playing goes on until it is ready (so a scene's music never drops out while its file loads); if it cannot be
      had, its synthesized pattern plays instead, or nothing. `at` (seconds into the recording): start there, even if it is
      the track playing (the music page's "hear the seam"). */
  music(id, fade = null, at = null) {
    if (!this.ctx) { this.wanted = id; return; }
    if (this.current && this.current.id === id && at == null) return;
    const rec = this.recording(id), track = id ? this.sound.music[id] : null;
    const cur = { id, gain: null, stop: null, fade: fade ?? (rec && rec.fade) ?? 1.2 };
    if (!rec && !track) { this.current = null; this.release(cur.fade); return; }      // silence (or a name no track has)
    this.current = cur;
    const gain = cur.gain = this.ctx.createGain();
    gain.gain.value = 0;
    gain.connect(this.duck);
    const begin = (stop, when = this.ctx.currentTime, recorded = false) => {           // it sounds: it comes up, every other track goes down
      cur.stop = stop;
      const level = recorded ? (this.sound.recordedLevel ?? 1) * (rec.volume ?? 1) : (track.volume ?? 1);
      gain.gain.setValueAtTime(0, when);
      gain.gain.linearRampToValueAtTime(level, when + cur.fade);
      this.release(cur.fade, when);
      this.live.push(cur);
    };
    const instead = () => {                                                            // no recording to be had: the pattern, or nothing
      if (this.current !== cur || cur.stop) return;
      if (track) begin(track.src ? this.playFile(track, gain) : this.playPattern(track, gain));
      else { gain.disconnect(); this.current = null; this.release(cur.fade); }
    };
    if (rec && !rec.stream) {
      const late = setTimeout(() => { console.warn(`Music "${id}": its recording is taking long to load.`); instead(); }, 12000);
      this.decodeMusic(id).then((d) => {
        clearTimeout(late);
        if (this.current !== cur || cur.stop) { if (!cur.stop) gain.disconnect(); return; }     // (something else was asked for meanwhile)
        const when = this.ctx.currentTime + 0.05;
        begin(this.playRecording(rec, d, gain, when, at ?? 0, cur), when, true);
      }).catch((err) => { clearTimeout(late); console.warn(`Music "${id}" would not play from its recording:`, err && err.message); instead(); });
      return;
    }
    if (rec) {                                                                         // a long piece, streamed (`stream: yes`): it loops whole, or plays once
      const format = this.musicFormats().find((f) => rec.files[f]);
      if (!format) { instead(); return; }
      begin(this.playFile({ src: this.musicUrl(rec.files[format]), loop: !!rec.loop }, gain), this.ctx.currentTime, true);
      return;
    }
    begin(track.src ? this.playFile(track, gain) : this.playPattern(track, gain));
  }

  /** MUSIC-24: fade out every track that is sounding, over `fade` seconds from `when` (now), and stop it after. */
  release(fade = 1.2, when = null) {
    const t = when ?? this.ctx.currentTime;
    for (const old of this.live.splice(0)) {
      old.gain.gain.cancelScheduledValues(t);
      old.gain.gain.setValueAtTime(old.gain.gain.value, t);
      old.gain.gain.linearRampToValueAtTime(0, t + fade);
      setTimeout(() => old.stop(), Math.max(0, t - this.ctx.currentTime + fade) * 1000 + 100);
    }
  }

  /** MUSIC-24: the copies this browser can play, in the order sound.js prefers them (`musicFormats`), less any it failed to decode. */
  musicFormats() {
    if (!this._musicFormats) {
      const probe = document.createElement("audio");
      const types = { webm: 'audio/webm; codecs="opus"', ogg: 'audio/ogg; codecs="opus"', m4a: 'audio/mp4; codecs="mp4a.40.2"', mp3: "audio/mpeg" };
      this._musicFormats = (this.sound.musicFormats || ["webm", "m4a"]).filter((f) => !types[f] || probe.canPlayType(types[f]) !== "");
    }
    return this._musicFormats.filter((f) => !this.badFormats.has(f));
  }
  /** MUSIC-24: a recording's address, from the top of the site (the list names them so), whichever page the game runs in. */
  musicUrl(path) { return new URL(`../../${path}`, import.meta.url).href; }

  /** MUSIC-24: a recording's bytes, fetched once (and kept: a few hundred KB a minute). */
  fetchMusic(id, format) {
    const key = `${id}.${format}`;
    let got = this.bytes.get(key);
    if (got) { this.bytes.delete(key); this.bytes.set(key, got); return got; }     // (the newest last)
    const rec = this.recording(id);
    got = fetch(this.musicUrl(rec.files[format])).then((r) => {
      if (!r.ok) throw Object.assign(new Error(`${rec.files[format]}: ${r.status}`), { fetching: true });
      return r.arrayBuffer();
    }, (err) => { throw Object.assign(err, { fetching: true }); });
    this.bytes.set(key, got);
    got.catch(() => { if (this.bytes.get(key) === got) this.bytes.delete(key); });
    while (this.bytes.size > 8) this.bytes.delete(this.bytes.keys().next().value);
    return got;
  }

  /** MUSIC-24: fetch a scene's recording ahead (the bytes only: decoded, a minute is some 22 MB), for a place next door. */
  prefetch(id) {
    const rec = this.recording(id);
    if (!rec || rec.stream) return;
    const format = this.musicFormats().find((f) => rec.files[f]);
    if (format) this.fetchMusic(id, format).catch(() => {});
  }

  /** MUSIC-24: a recording decoded: { buffer, format, shift }. The first copy this browser decodes is used; a copy it cannot
      decode is not asked for again. `shift`: where the sound first rises above -50 dBFS, against where the list says it does
      (`onset`, measured by the tool): a browser that leaves a codec's start-up silence in has the music start a little later
      (by 2 to 60 ms), and the loop points move with it. (Earlier is a codec's pre-echo, and is left alone.) */
  decodeMusic(id) {
    const had = this.decoded.get(id);
    if (had) { this.decoded.delete(id); this.decoded.set(id, had); return had; }
    const rec = this.recording(id);
    const job = (async () => {
      let why = null;
      for (const format of this.musicFormats()) {
        if (!rec.files[format]) continue;
        try {
          const bytes = await this.fetchMusic(id, format);
          const buffer = await this.ctx.decodeAudioData(bytes.slice(0));            // (a copy: decoding takes the bytes it is given)
          const late = this.onsetOf(buffer, (rec.onset || 0) + 0.1) - (rec.onset || 0);
          return { buffer, format, shift: late > 0.002 && late < 0.06 ? late : 0 };
        } catch (err) {
          why = err;
          if (!(err && err.fetching)) this.badFormats.add(format);                   // (it fetched, and would not decode)
        }
      }
      throw why || new Error("no copy this browser can play");
    })();
    this.decoded.set(id, job);
    job.catch(() => { if (this.decoded.get(id) === job) this.decoded.delete(id); });
    for (const key of [...this.decoded.keys()]) {                                    // two kept, besides those sounding
      if (this.decoded.size <= 2) break;
      if (key !== id && !this.live.some((c) => c.id === key) && !(this.current && this.current.id === key)) this.decoded.delete(key);
    }
    return job;
  }

  /** MUSIC-24: the time of the first sample of a decoded recording above -50 dBFS (in any channel), looking no further than `upTo` seconds. */
  onsetOf(buffer, upTo) {
    const n = Math.min(buffer.length, Math.ceil(upTo * buffer.sampleRate));
    let first = n;
    for (let c = 0; c < buffer.numberOfChannels; c++) {
      const d = buffer.getChannelData(c);
      for (let i = 0; i < first; i++) if (d[i] >= 0.00316 || d[i] <= -0.00316) { first = i; break; }
    }
    return first / buffer.sampleRate;
  }

  /** MUSIC-24: a decoded recording, from `at` seconds into it: its intro once, then its loop for ever (or once through, with no loop). */
  playRecording(rec, d, out, when, at = 0, cur = null) {
    const src = this.ctx.createBufferSource();
    src.buffer = d.buffer;
    const loop = rec.loop || null;
    let from = Math.max(0, at);
    if (loop) {
      src.loop = true; src.loopStart = loop[0] + d.shift; src.loopEnd = loop[1] + d.shift;
      if (from >= loop[1]) from = loop[0] + ((from - loop[0]) % (loop[1] - loop[0]));
    }
    src.connect(out);
    src.start(when, from + d.shift);
    if (cur) cur.clock = { started: when, from, loop };
    return () => { try { src.stop(); } catch { /* stopped */ } src.disconnect(); out.disconnect(); };
  }

  /** MUSIC-24: how far into its recording the track playing is, in seconds (null for a synthesized track, or none). */
  position() {
    const c = this.current;
    if (!c || !c.clock || !this.ctx) return null;
    const { started, from, loop } = c.clock;
    let p = from + Math.max(0, this.ctx.currentTime - started);
    if (loop && p >= loop[1]) p = loop[0] + ((p - loop[0]) % (loop[1] - loop[0]));
    return p;
  }

  /** A recorded track: streamed, so a long file starts at once and is never held whole in memory. */
  playFile(track, out) {
    const el = new Audio(track.src.replace("{ext}", this.ext));
    el.loop = track.loop !== false;
    el.crossOrigin = "anonymous";
    const node = this.ctx.createMediaElementSource(el);
    node.connect(out);
    el.play().catch((err) => console.warn("Music did not start:", track.src, err.message));
    return () => { el.pause(); node.disconnect(); out.disconnect(); };
  }

  /** A placeholder tune: a 16-step pattern played by two oscillators.
      Notes are scheduled a little ahead on the audio clock, so timing stays tight
      even when the page is busy drawing.
      ENGINE-20: two more voices a track can ask for, for Act Six's tunes (sound.js `edo`): `voice: "pluck"`, a plucked
      string (a triangle with a brighter octave over it that dies at once: the attack of a plectrum; the note then falls
      away fast), and `voice: "flute"`, a breathy flute (a sine that comes in over `attack` seconds, with a little filtered
      breath under it, `breath`); and a second line, `alt` (notes of the scale, as `lead`), in `altVoice` ("flute"), so a
      plucked tune can have a flute answer it. A `lull` of silent steps at the end of the pattern is simply rests. */
  playPattern(track, out) {
    const ctx = this.ctx;
    const stepLen = 60 / track.bpm / (track.div || 2);
    let step = 0, next = ctx.currentTime + 0.06;
    const voice = (midi, when, len, wave, level, cents = 0, kind = null) => {
      const osc = ctx.createOscillator(), env = ctx.createGain();
      osc.type = kind === "flute" ? "sine" : wave; osc.frequency.value = NOTE(midi);
      if (cents) osc.detune.value = cents;           // ENGINE-17: a tune a little flat (`detune`, in cents, on its lead): a building's waiting music
      const attack = kind === "flute" ? Math.max(0.03, track.attack || 0.09) : 0.012;
      env.gain.setValueAtTime(0, when);
      env.gain.linearRampToValueAtTime(level, when + attack);
      if (kind === "pluck") { env.gain.setValueAtTime(level, when + 0.02); env.gain.exponentialRampToValueAtTime(level * 0.25, when + Math.min(len, 0.35)); }      // (the string's quick fall)
      env.gain.exponentialRampToValueAtTime(0.0008, when + len);
      osc.connect(env).connect(out);
      osc.start(when); osc.stop(when + len + 0.03);
      if (kind === "pluck") {                        // the bright attack: the octave above, gone in a tenth of a second
        const o2 = ctx.createOscillator(), e2 = ctx.createGain();
        o2.type = "triangle"; o2.frequency.value = NOTE(midi + 12); if (cents) o2.detune.value = cents;
        e2.gain.setValueAtTime(level * 0.5, when); e2.gain.exponentialRampToValueAtTime(0.0008, when + 0.1);
        o2.connect(e2).connect(out); o2.start(when); o2.stop(when + 0.13);
      }
      if (kind === "flute" && (track.breath ?? 0.35) > 0) {      // the breath: a little noise through a band at the note, under it
        const b = this.breathBuffer(), src = ctx.createBufferSource(), f = ctx.createBiquadFilter(), e3 = ctx.createGain();
        src.buffer = b; src.loop = true; f.type = "bandpass"; f.frequency.value = NOTE(midi) * 2; f.Q.value = 2.5;
        const lv = level * (track.breath ?? 0.35) * 0.6;
        e3.gain.setValueAtTime(0, when); e3.gain.linearRampToValueAtTime(lv, when + attack * 0.8); e3.gain.exponentialRampToValueAtTime(0.0008, when + len);
        src.connect(f).connect(e3).connect(out); src.start(when); src.stop(when + len + 0.03);
      }
    };
    const pitch = (degree, octave) => {
      const n = track.scale.length, d = ((degree % n) + n) % n;
      return track.root + 12 * (octave + Math.floor(degree / n)) + track.scale[d];
    };
    // ENGINE-21: a bed under the tune, going on as long as the track does and fading with it: noise through a filter that drifts
    // between two pitches (`bed: { noise: [low, high], sweep, q, level }`): the crowd under Osaka's tune, the wind under Shosha's
    let bedStop = null;
    if (track.bed && track.bed.noise) {
      const bd = track.bed, src = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain(), t = ctx.currentTime;
      src.buffer = this.breathBuffer(); src.loop = true; f.type = bd.kind || "bandpass"; f.Q.value = bd.q ?? 0.8;
      const [lo, hi] = Array.isArray(bd.noise) ? bd.noise : [bd.noise, bd.noise];
      f.frequency.setValueAtTime((lo + hi) / 2, t);
      const nodes = [src];
      if (hi !== lo) { const lfo = ctx.createOscillator(), depth = ctx.createGain(); lfo.frequency.value = 1 / Math.max(0.5, bd.sweep || 6); depth.gain.value = (hi - lo) / 2; lfo.connect(depth).connect(f.frequency); lfo.start(t); nodes.push(lfo); }
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(bd.level ?? 0.02, t + 1.5);
      src.connect(f).connect(g).connect(out); src.start(t);
      bedStop = () => { for (const n of nodes) { try { n.stop(); } catch { /* stopped */ } } };
    }
    const timer = setInterval(() => {
      while (next < ctx.currentTime + 0.14) {
        const i = step % track.lead.length;
        if (track.lead[i] != null) voice(pitch(track.lead[i], 1), next, stepLen * (track.hold || 1.7), track.wave || "triangle", track.level ?? 0.12, track.detune || 0, track.voice || null);      // (ENGINE-17: detune; ENGINE-20: voice)
        if (track.alt && track.alt[step % track.alt.length] != null) voice(pitch(track.alt[step % track.alt.length], track.altOctave ?? 1), next, stepLen * (track.altHold || track.hold || 1.7), "sine", track.altLevel ?? 0.07, 0, track.altVoice || "flute");      // ENGINE-20: the second line
        const b = track.bass[step % track.bass.length];
        if (b != null) voice(pitch(b, -1), next, stepLen * (track.bassHold || 3.4), track.bassWave || "sine", track.bassLevel ?? 0.17, 0, track.bassVoice || null);      // (ENGINE-21: bassHold, bassVoice)
        step++; next += stepLen;
      }
    }, 30);
    return () => { clearInterval(timer); if (bedStop) bedStop(); out.disconnect(); };
  }
  /** ENGINE-20: a second of noise, made once, for the flute's breath and the loops below. */
  breathBuffer() {
    if (this._breath) return this._breath;
    const ctx = this.ctx, b = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate), d = b.getChannelData(0);
    let last = 0;
    for (let i = 0; i < d.length; i++) { const w = Math.random() * 2 - 1; last = (last + 0.02 * w) / 1.02; d[i] = w * 0.6 + last * 8; }      // (white, with a little brown under it)
    return (this._breath = b);
  }

  // ---------- ENGINE-20: loops of sound (ambience): rain on thatch, waves on a shingle beach, the keep's hum ----------
  /** A loop from sound.js `loops` (noise through a filter, or notes, or both: { noise: [low, high] (a slow sweep between
      them and back, `sweep` seconds; one number: steady), q, notes: [[midi, level]], wave, level }) starts, or goes on if it is
      playing, at `level` times its own (1). Loops are on the effects' bus; each has a gain of its own, so stopLoop fades it out
      over `fade` seconds and loopLevel turns it up or down (the hush). */
  loop(id, { level = 1, fade = 0.6 } = {}) {
    if (!this.ready) return false;
    const spec = this.sound.loops && this.sound.loops[id];
    if (!spec) return false;
    this.loops = this.loops || {};
    const ctx = this.ctx, t = ctx.currentTime, want = (spec.level ?? 0.05) * level;
    let L = this.loops[id], fresh = false;
    if (!L) {
      // LOOPS-24 (the author, 10 November: going in and out of Kihei's shop "sounds like a gunshot because of the loud wave
      // crash"): a new gain reads 1 until the sound thread has run, so the ramp below began from full and fell from there, a
      // burst of the loop at some twenty times its level on every scene with a loop. It starts from silence now.
      const gain = ctx.createGain(); gain.gain.value = 0; gain.gain.setValueAtTime(0, t); gain.connect(this.sfxBus);
      fresh = true;
      const nodes = [];
      if (spec.noise) {
        const src = ctx.createBufferSource(), f = ctx.createBiquadFilter();
        src.buffer = this.breathBuffer(); src.loop = true; f.type = spec.kind || "bandpass"; f.Q.value = spec.q ?? 0.7;
        const lo = Array.isArray(spec.noise) ? spec.noise[0] : spec.noise, hi = Array.isArray(spec.noise) ? spec.noise[1] : spec.noise;
        f.frequency.setValueAtTime(lo, t);
        if (hi !== lo) { const lfo = ctx.createOscillator(), depth = ctx.createGain(); lfo.frequency.value = 1 / Math.max(0.5, spec.sweep || 6); depth.gain.value = (hi - lo) / 2; f.frequency.setValueAtTime((lo + hi) / 2, t); lfo.connect(depth).connect(f.frequency); lfo.start(t); nodes.push(lfo); }
        src.connect(f).connect(gain); src.start(t); nodes.push(src);
      }
      // ENGINE-21: `pulse` (Hz): the notes throb on and off (frogs croaking); `gate` (Hz): and the whole chorus swells and lulls slowly
      let into = gain;
      if (spec.pulse || spec.gate) {
        const pg = ctx.createGain(); pg.gain.value = 0.5; pg.connect(gain); into = pg;
        for (const [rate, depthK] of [[spec.pulse, 0.5], [spec.gate, 0.35]]) {
          if (!rate) continue;
          const lfo = ctx.createOscillator(), depth = ctx.createGain(); lfo.type = "sine"; lfo.frequency.value = rate; depth.gain.value = depthK;
          lfo.connect(depth).connect(pg.gain); lfo.start(t); nodes.push(lfo);
        }
      }
      for (const [midi, lv] of spec.notes || []) {
        const osc = ctx.createOscillator(), e = ctx.createGain();
        osc.type = spec.wave || "sine"; osc.frequency.value = NOTE(midi); e.gain.value = lv ?? 1;
        if (spec.wobble) { const lfo = ctx.createOscillator(), depth = ctx.createGain(); lfo.frequency.value = spec.wobble; depth.gain.value = NOTE(midi) * 0.004; lfo.connect(depth).connect(osc.frequency); lfo.start(t); nodes.push(lfo); }
        osc.connect(e).connect(into); osc.start(t); nodes.push(osc);
      }
      L = this.loops[id] = { gain, nodes, level: want };
    }
    L.level = want; L.stopping = false;
    L.gain.gain.cancelScheduledValues(t); L.gain.gain.setValueAtTime(fresh ? 0 : L.gain.gain.value, t); L.gain.gain.linearRampToValueAtTime(want, t + fade);
    return true;
  }
  /** The loop's loudness, as a share of what it was started at (the hush: 0.7 under a line). */
  loopLevel(id, k = 1) {
    const L = this.loops && this.loops[id];
    if (!L || L.stopping || !this.ctx) return;
    const want = L.level * Math.max(0, k), t = this.ctx.currentTime;
    if (Math.abs(want - L.gain.gain.value) < 1e-4) return;
    L.gain.gain.cancelScheduledValues(t); L.gain.gain.setValueAtTime(L.gain.gain.value, t); L.gain.gain.linearRampToValueAtTime(want, t + 0.25);
  }
  /** Stop a loop (fading it out over `fade` seconds), or every loop (no id): a scene change, the title. */
  stopLoop(id = null, fade = 0.8) {
    if (!this.loops || !this.ctx) return;
    for (const key of id ? [id] : Object.keys(this.loops)) {
      const L = this.loops[key];
      if (!L) continue;
      const t = this.ctx.currentTime;
      L.stopping = true;
      L.gain.gain.cancelScheduledValues(t); L.gain.gain.setValueAtTime(L.gain.gain.value, t); L.gain.gain.linearRampToValueAtTime(0, t + fade);
      delete this.loops[key];
      setTimeout(() => { for (const n of L.nodes) { try { n.stop(); } catch { /* stopped */ } } L.gain.disconnect(); }, fade * 1000 + 100);
    }
  }
  /** Which loops are playing now (for tests). */
  get looping() { return Object.keys(this.loops || {}); }

  // ---------- effects ----------
  sfx(id) {
    if (!this.ready) return;
    const fx = this.sound.sfx[id];
    if (!fx) return;
    const ctx = this.ctx, t = ctx.currentTime;
    if (fx.noise) {                             // a filtered sweep of noise: whooshes and flashes
      const len = fx.len, buffer = ctx.createBuffer(1, Math.ceil(ctx.sampleRate * len), ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
      const src = ctx.createBufferSource(), filter = ctx.createBiquadFilter(), env = ctx.createGain();
      src.buffer = buffer; filter.type = "bandpass"; filter.Q.value = fx.q || 1.2;
      filter.frequency.setValueAtTime(fx.noise[0], t);
      filter.frequency.exponentialRampToValueAtTime(fx.noise[1], t + len);
      env.gain.setValueAtTime(0, t);
      env.gain.linearRampToValueAtTime(fx.level || 0.4, t + len * 0.3);
      env.gain.linearRampToValueAtTime(0, t + len);
      src.connect(filter).connect(env).connect(this.sfxBus);
      src.start(t);
    }
    // ENGINE-21: several short bursts of noise in one sound (`noises`: [[from Hz, to Hz, start, length, level]]): two clacks of
    // wooden clappers, feet stamping on boards, the beats of a laugh
    for (const [f0, f1, at, len, lv] of fx.noises || []) {
      const n = Math.max(1, Math.ceil(ctx.sampleRate * len)), buffer = ctx.createBuffer(1, n, ctx.sampleRate), data = buffer.getChannelData(0);
      for (let i = 0; i < n; i++) data[i] = Math.random() * 2 - 1;
      const src = ctx.createBufferSource(), filter = ctx.createBiquadFilter(), env = ctx.createGain(), t0 = t + at;
      src.buffer = buffer; filter.type = "bandpass"; filter.Q.value = fx.q || 1.2;
      filter.frequency.setValueAtTime(f0, t0); filter.frequency.exponentialRampToValueAtTime(Math.max(20, f1), t0 + len);
      env.gain.setValueAtTime(0, t0); env.gain.linearRampToValueAtTime(lv ?? fx.level ?? 0.2, t0 + Math.min(0.006, len * 0.2)); env.gain.exponentialRampToValueAtTime(0.0008, t0 + len);
      src.connect(filter).connect(env).connect(this.sfxBus);
      src.start(t0);
    }
    for (const [midi, at, len, to] of fx.notes || []) {  // a few notes: clicks and pick-ups
      const osc = ctx.createOscillator(), env = ctx.createGain();
      osc.type = fx.wave || "square"; osc.frequency.value = NOTE(midi);
      if (to != null) { osc.frequency.setValueAtTime(NOTE(midi), t + at); osc.frequency.exponentialRampToValueAtTime(NOTE(to), t + at + len); }    // ENGINE-17: a note that slides to another (a fan running down)
      env.gain.setValueAtTime(fx.level || 0.12, t + at);
      env.gain.exponentialRampToValueAtTime(0.0008, t + at + len);
      osc.connect(env).connect(this.sfxBus);
      osc.start(t + at); osc.stop(t + at + len + 0.02);
    }
  }

  // ---------- voices ----------
  hasVoice(lineId) { return this.ready && this.sound.voices.has(lineId); }

  /** Play the recording for a line. Resolves with true when it has played, or false if
      the file would not play. Returns null when the line has no recording. */
  voice(lineId) {
    if (!this.hasVoice(lineId)) return null;
    this.stopVoice();
    const el = new Audio(`${this.sound.voicePath}${lineId}.${this.ext}`);
    this.voiceEl = el;
    const node = this.ctx.createMediaElementSource(el);
    node.connect(this.voiceBus);
    this.setDuck(true);
    return new Promise((resolve) => {
      let settled = false;
      const done = (ok) => {
        if (settled) return;
        settled = true;
        if (this.voiceEl === el) { this.voiceEl = null; this.setDuck(false); }
        node.disconnect();
        resolve(ok);
      };
      el.addEventListener("ended", () => done(true), { once: true });
      el.addEventListener("pause", () => done(true), { once: true });
      el.addEventListener("error", () => { console.warn("Voice file would not play:", el.src); done(false); }, { once: true });
      el.play().catch(() => done(false));
    });
  }

  stopVoice() { if (this.voiceEl) this.voiceEl.pause(); }

  setDuck(on) {
    if (this.ctx) this.duck.gain.setTargetAtTime(on ? 0.35 : 1, this.ctx.currentTime, 0.12);
  }
}
