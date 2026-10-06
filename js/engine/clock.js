// The game clock. One requestAnimationFrame loop drives everything that must be
// pausable, skippable or saved: cutscene timing, dialogue timing, actor movement.
// Ambient loops that do not affect the game (twinkling stars, a spinning portal)
// are left to CSS, which the browser can run without touching this loop.

export const ease = {
  linear: (k) => k,
  in: (k) => k * k,
  out: (k) => 1 - (1 - k) * (1 - k),
  inOut: (k) => (k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2),
};

export class Clock {
  constructor() {
    this.now = 0;          // game time in ms; stops while paused
    this.scale = 1;        // 2 = fast-forward
    this.paused = false;
    this.skipping = false; // while true, every wait and tween finishes at once
    this.tasks = new Set();
    this.frameMs = 16.7;   // smoothed frame time, for the performance readout
    this._last = null;
  }

  start() {
    const frame = (t) => {
      if (this._last === null) this._last = t;
      const real = Math.min(t - this._last, 100); // a hidden tab must not cause a huge jump
      this._last = t;
      this.frameMs += (real - this.frameMs) * 0.05;
      if (!this.paused) {
        const dt = real * this.scale;
        this.now += dt;
        for (const task of [...this.tasks]) task(dt, this.now);
      }
      requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  }

  /** Run fn(dt, now) every frame. Returns a function that stops it. */
  every(fn) {
    this.tasks.add(fn);
    return () => this.tasks.delete(fn);
  }

  /** Resolve after ms of game time, or at once when skipping. */
  wait(ms) {
    if (this.skipping || ms <= 0) return Promise.resolve();
    return new Promise((resolve) => {
      let left = ms;
      const stop = this.every((dt) => {
        left -= dt;
        if (left <= 0 || this.skipping) { stop(); resolve(); }
      });
    });
  }

  /** Call step(k) with k easing from 0 to 1 over ms. Skipping jumps to k = 1. */
  tween(ms, step, easing = ease.inOut) {
    if (this.skipping || ms <= 0) { step(1); return Promise.resolve(); }
    return new Promise((resolve) => {
      let t = 0;
      const stop = this.every((dt) => {
        t += dt;
        const k = this.skipping ? 1 : Math.min(t / ms, 1);
        step(easing(k));
        if (k >= 1) { stop(); resolve(); }
      });
    });
  }
}
