// Dialogue. Every spoken line has an ID, and scripts only ever mention IDs:
//
//     await g.say("egypt.river.look");
//
// The words and the speaker live in js/content/lines.en.js. That gives three things:
//   - the whole script is one file, easy to edit and to hand to voice actors;
//   - a recording for a line is just a sound file named after its ID, so voices
//     can be added later, a few lines at a time, without touching any script;
//   - another language is another lines file.
//
// When a recording exists the line stays up until the voice finishes. When it does
// not, the line stays up for a time based on its length. A click moves on either way.

export class Dialogue {
  constructor(game) {
    this.g = game;
    this.el = game.stage.querySelector("#dialogue");
    this.active = false;       // a line is on screen
    this.choosing = false;     // a list of choices is on screen
    this._next = false;
    this._shownAt = 0;
  }

  /** The player clicked or pressed a key: move to the next line. */
  advance() {
    if (this.active && performance.now() - this._shownAt > 180) this._next = true;
  }

  async say(id) {
    const g = this.g;
    const entry = g.lines[id];
    if (!entry) { console.warn("Missing line:", id); return; }
    const [who, text] = entry;
    g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;
    if (g.clock.skipping) return;

    const person = g.cast[who] || {};
    const actor = g.view.actors.get(who);
    const voiced = g.settings.voices ? g.audio.voice(id) : null;
    const showText = g.settings.subtitles || !voiced;

    let p = null;
    {
      p = document.createElement("p");
      p.className = "say";
      p.hidden = !showText;
      p.style.color = person.color || "#fff";
      p.textContent = text;
      // Above the speaker's head when they are on stage, otherwise top centre.
      const x = actor ? Math.min(Math.max(actor.x, 84), 236) : 160;
      const y = actor ? Math.max(actor.y - actor.h * actor.scale - 4, 30) : 62;
      p.style.left = `${(x / 320) * 100}%`;
      p.style.top = `${(y / 200) * 100}%`;
      this.el.appendChild(p);
    }

    this.active = true; this._next = false; this._shownAt = performance.now();
    let left = Math.max(1500, 900 + text.length * 58) / (g.settings.textSpeed || 1);
    let speaking = !!voiced;
    // When the recording ends, move on. If it would not play, show the words for their usual time instead.
    if (voiced) voiced.then((played) => { speaking = false; if (played) left = 280; else p.hidden = false; });

    await new Promise((resolve) => {
      let t = 0;
      const stop = g.clock.every((dt) => {
        t += dt;
        if (!speaking) left -= dt;
        if (actor) actor.flag("talk", Math.floor(t / 130) % 2 === 0);
        if (left <= 0 || this._next || g.clock.skipping) { stop(); resolve(); }
      });
    });

    g.audio.stopVoice();
    if (actor) actor.flag("talk", false);
    if (p) p.remove();
    this.active = false;
    if (!g.clock.skipping) await g.clock.wait(90);       // a short beat between lines
  }

  /** Show a list of things to say. Resolves with the id of the one picked.
      options: [{ id, line, when }], where `line` is a line ID. */
  choose(options) {
    const g = this.g;
    const open = options.filter((o) => !o.when || o.when(g));
    if (g.clock.skipping || open.length === 0) return Promise.resolve(open.length ? open[open.length - 1].id : null);
    return new Promise((resolve) => {
      const list = document.createElement("ul");
      list.className = "choices";
      for (const o of open) {
        const li = document.createElement("li"), b = document.createElement("button");
        b.type = "button";
        b.textContent = g.lines[o.line] ? g.lines[o.line][1] : o.line;
        b.addEventListener("click", (event) => {
          event.stopPropagation();
          list.remove(); this.choosing = false; g.ui.refresh();
          resolve(o.id);
        });
        li.appendChild(b); list.appendChild(li);
      }
      this.el.appendChild(list);
      this.choosing = true; g.ui.refresh();
      list.querySelector("button").focus({ preventScroll: true });
    });
  }

  clear() { this.el.innerHTML = ""; this.active = false; this.choosing = false; }
}
