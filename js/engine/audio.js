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

const NOTE = (midi) => 440 * Math.pow(2, (midi - 69) / 12);

export class AudioEngine {
  constructor(settings, sound) {
    this.settings = settings;
    this.sound = sound;          // { music: {...}, sfx: {...}, voices: Set, voicePath, formats }
    this.ctx = null;
    this.current = null;         // { id, gain, stop }
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
  /** Cross-fade to a track. Asking for the track that is already playing does nothing. */
  music(id, fade = 1.2) {
    if (!this.ctx) { this.wanted = id; return; }
    if (this.current && this.current.id === id) return;
    const t = this.ctx.currentTime;
    if (this.current) {
      const old = this.current;
      old.gain.gain.cancelScheduledValues(t);
      old.gain.gain.setValueAtTime(old.gain.gain.value, t);
      old.gain.gain.linearRampToValueAtTime(0, t + fade);
      setTimeout(() => old.stop(), fade * 1000 + 100);
    }
    this.current = null;
    const track = id && this.sound.music[id];
    if (!track) return;
    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(track.volume ?? 1, t + fade);
    gain.connect(this.duck);
    const stop = track.src ? this.playFile(track, gain) : this.playPattern(track, gain);
    this.current = { id, gain, stop };
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
      even when the page is busy drawing. */
  playPattern(track, out) {
    const ctx = this.ctx;
    const stepLen = 60 / track.bpm / (track.div || 2);
    let step = 0, next = ctx.currentTime + 0.06;
    const voice = (midi, when, len, wave, level) => {
      const osc = ctx.createOscillator(), env = ctx.createGain();
      osc.type = wave; osc.frequency.value = NOTE(midi);
      env.gain.setValueAtTime(0, when);
      env.gain.linearRampToValueAtTime(level, when + 0.012);
      env.gain.exponentialRampToValueAtTime(0.0008, when + len);
      osc.connect(env).connect(out);
      osc.start(when); osc.stop(when + len + 0.03);
    };
    const pitch = (degree, octave) => {
      const n = track.scale.length, d = ((degree % n) + n) % n;
      return track.root + 12 * (octave + Math.floor(degree / n)) + track.scale[d];
    };
    const timer = setInterval(() => {
      while (next < ctx.currentTime + 0.14) {
        const i = step % track.lead.length;
        if (track.lead[i] != null) voice(pitch(track.lead[i], 1), next, stepLen * (track.hold || 1.7), track.wave || "triangle", 0.12);
        const b = track.bass[step % track.bass.length];
        if (b != null) voice(pitch(b, -1), next, stepLen * 3.4, track.bassWave || "sine", 0.17);
        step++; next += stepLen;
      }
    }, 30);
    return () => { clearInterval(timer); out.disconnect(); };
  }

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
    for (const [midi, at, len] of fx.notes || []) {  // a few notes: clicks and pick-ups
      const osc = ctx.createOscillator(), env = ctx.createGain();
      osc.type = fx.wave || "square"; osc.frequency.value = NOTE(midi);
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
