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

import { W, H } from "./grid.js";
import { portrait } from "./cast.js";       // LETTERBOX-11: the portrait beside a voice through a door

export class Dialogue {
  constructor(game) {
    this.g = game;
    this.el = game.stage.querySelector("#dialogue");
    this.active = false;       // a line is on screen
    this.choosing = false;     // a list of choices is on screen
    this._next = false;
    this._shownAt = 0;
    this.faces = {};           // LETTERBOX-11: portraits for voices through a door, drawn once for each size ("sprite|pixels")
  }

  /** The player clicked or pressed a key: move to the next line. */
  advance() {
    if (this.active && performance.now() - this._shownAt > 180) this._next = true;
  }

  /** LETTERBOX-11: a portrait of a lead who is at the other end of a door in time, for beside their words: the interface's
      own (cast.js portrait, never in the scene's paints), drawn for the pixels it is shown at, and kept. */
  face(who) {
    const g = this.g, person = g.cast[who] || {}, img = document.createElement("img");
    const dpr = window.devicePixelRatio || 1, css = Math.max(24, Math.round(g.stage.getBoundingClientRect().width * 0.07)), px = Math.round(css * dpr);
    const key = person.sprite + "|" + px;
    if (!(key in this.faces)) { const face = person.sprite ? portrait(person.sprite, px) : null; this.faces[key] = face ? face.toDataURL() : ""; }
    if (this.faces[key]) img.src = this.faces[key];
    img.alt = person.name || who; img.draggable = false; img.className = "face";
    img.style.width = img.style.height = css + "px";
    return img;
  }

  async say(id, { through = null } = {}) {
    const g = this.g;
    const entry = g.lines[id];
    if (!entry) { console.warn("Missing line:", id); return; }
    const [who, text] = entry;
    g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;
    if (g.clock.skipping) return;

    // LETTERBOX-11: a line through a door comes from someone in another century: their portrait stands beside the words,
    // in their colour, top centre as for anyone not on the stage, and nobody here moves their mouth for it.
    const person = g.cast[through || who] || {};
    const actor = through ? null : g.view.cast.get(who);
    let seed = 0;
    for (let i = 0; i < id.length; i++) seed = (seed * 31 + id.charCodeAt(i)) >>> 0;       // which gesture goes with this line
    const voiced = g.settings.voices ? g.audio.voice(id) : null;
    const showText = g.settings.subtitles || !voiced;

    let p = null, fit = () => {};
    {
      p = document.createElement("p");
      p.className = "say";
      p.hidden = !showText;
      p.style.color = person.color || "#fff";
      if (through) { p.classList.add("through"); p.append(this.face(through), Object.assign(document.createElement("span"), { textContent: text })); }      // LETTERBOX-11
      else p.textContent = text;
      // Above the speaker's head when they are on stage, otherwise top center.
      // While a close-up is showing, along the bottom, clear of whatever is being looked at.
      // (x, y) is where the middle of the bottom edge of the words goes, in picture pixels.
      const near = g.near;
      const x = near ? W / 2 : actor ? Math.min(Math.max(actor.x, 210), W - 210) : W / 2;
      let top = actor ? actor.y - actor.h * actor.scale : 0;
      if (actor && !near) {
        // Someone taller standing close by, level with the speaker or nearer: lift the words clear of that head too,
        // so a small speaker's words are not written across a tall listener's face. (Not more than 90 pixels: the
        // words must still belong to the speaker.)
        for (const other of g.view.cast.items.values()) {
          if (other === actor || !other.h || other.hidden || !(other.opacity > 0)) continue;
          const head = other.y - other.h * other.scale;
          if (Math.abs(other.x - x) < 150 && other.y > actor.y - 60 && head < top) top = Math.max(head, top - 90, actor.y - actor.h * actor.scale - 90);
        }
      }
      const y = near ? H - 12 : actor ? Math.max(top - 10, 60) : 150;
      if (near) p.classList.add("under");
      p.style.left = `${(x / W) * 100}%`;
      p.style.top = `${(y / H) * 100}%`;
      this.el.appendChild(p);
      // A long line above someone standing high in the picture would run off the top: bring it down until it all shows.
      fit = () => {
        const over = this.el.getBoundingClientRect().top + 4 - p.getBoundingClientRect().top;
        if (!p.hidden && over > 0) p.style.top = `calc(${(y / H) * 100}% + ${over}px)`;
      };
      fit();
    }

    this.active = true; this._next = false; this._shownAt = performance.now();
    let left = Math.max(1500, 900 + text.length * 58) / (g.settings.textSpeed || 1);
    let speaking = !!voiced;
    // When the recording ends, move on. If it would not play, show the words for their usual time instead.
    if (voiced) voiced.then((played) => { speaking = false; if (played) left = 280; else { p.hidden = false; fit(); } });

    if (actor && actor.talk) actor.talk(true, seed);       // mouth and hands
    await new Promise((resolve) => {
      const stop = g.clock.every((dt) => {
        if (!speaking) left -= dt;
        if (left <= 0 || this._next || g.clock.skipping) { stop(); resolve(); }
      });
    });

    g.audio.stopVoice();
    if (actor && actor.talk) actor.talk(false);
    if (p) p.remove();
    this.active = false;
    if (!g.clock.skipping) await g.clock.wait(90);       // a short beat between lines
  }

  /** Show a list of things to say. Resolves with the id of the one picked.
      options: [{ id, line, when }], where `line` is a line ID.
      LETTERBOX-11: { through: who } shows the list as the words of a lead who is not on the stage (at the other end of a
      door in time): their portrait at its head, the options in their colour.
      TALK-11: an option may carry `asked` (how many times it has been picked before: 0 marks it new, more marks it asked)
      and `exit: true` (it ends a talk: Esc picks it); { talk: true } marks the list as a tree's. A menu that is up when
      a cutscene starts being skipped is taken as it would be if it were asked for while skipping: the last open option. */
  choose(options, { through = null, talk = false } = {}) {
    const g = this.g;
    const open = options.filter((o) => !o.when || o.when(g));
    if (g.clock.skipping || open.length === 0) return Promise.resolve(open.length ? open[open.length - 1].id : null);
    return new Promise((resolve) => {
      const list = document.createElement("ul");
      list.className = "choices";
      if (talk) list.classList.add("talk");                                             // TALK-11
      if (through) {                                                                    // LETTERBOX-11
        const person = g.cast[through] || {}, head = document.createElement("li");
        head.className = "voice";
        head.append(this.face(through), Object.assign(document.createElement("span"), { textContent: person.name || through }));
        list.classList.add("through");
        list.style.setProperty("--who", person.color || "#fff");
        list.appendChild(head);
      }
      let stop = null;                                                                  // TALK-11: the watch for skipping, below
      const done = (id) => { if (stop) stop(); list.remove(); this.choosing = false; g.ui.refresh(); resolve(id); };
      for (const o of open) {
        const li = document.createElement("li"), b = document.createElement("button");
        b.type = "button";
        b.textContent = g.lines[o.line] ? g.lines[o.line][1] : o.line;
        if (o.asked != null) b.classList.add(o.asked > 0 ? "asked" : "new");          // TALK-11: picked before (lighter), or never (the completist's mark)
        if (o.exit) b.classList.add("exit");                                           // TALK-11
        b.addEventListener("click", (event) => {
          event.stopPropagation();
          if (list.isConnected) done(o.id);
        });
        li.appendChild(b); list.appendChild(li);
      }
      stop = g.clock.every(() => { if (!list.isConnected) stop(); else if (g.clock.skipping) done(open[open.length - 1].id); });     // TALK-11 (a list cleared by other means lets the clock go)
      this.el.appendChild(list);
      this.choosing = true; g.ui.refresh();
      list.querySelector("button").focus({ preventScroll: true });
    });
  }

  /**
   * TALK-11: a dialogue tree, the way the classic adventures do them (docs/DESIGN.md, "Dialogue trees"). The tree is plain
   * data: { id, start, nodes: { name: { say, options, then } } }, an option { id, line, when, once, say, set, do, then }.
   * It is walked from `start` (a node id, or a function of the game giving one) until a node ends it: `exit`, a node with
   * nothing to show, or a cutscene being skipped. The game remembers every pick (`asked` in the save, by `id` of the tree
   * and the option: "joe/car"; with no tree id, by the scene and the node: "nevada-roadside/open/car"): an option picked
   * before shows as asked, one never picked as new, `once` takes an option away for good, and a reply keyed by the number
   * of askings ({ 1: [...], 2: [...], more: [...] }) answers differently each time.
   * { through: who } shows every menu as the words of a lead who is off the stage (LETTERBOX-11) and says the picked
   * line, and any reply of theirs, through the door. Resolves when the talk is over.
   */
  async talk(tree, { through = null, id = null } = {}) {
    const g = this.g, nodes = (tree && tree.nodes) || {}, memory = g.store.data.asked || (g.store.data.asked = {});
    const treeId = id || (tree && tree.id) || null;
    const keyOf = (node, option) => (treeId || `${g.scene ? g.scene.id : "talk"}/${node}`) + "/" + option.id;
    const count = (node, option) => memory[keyOf(node, option)] || 0;
    const resolve = async (to) => (typeof to === "function" ? await to(g) : to);          // a node id, "exit", "back", "root", or nothing: stay
    const root = async () => (await resolve(tree && tree.start)) || Object.keys(nodes)[0];   // (`start` is asked again for "root", so a start that depends on the story gives today's answer)
    // Lines, as g.say says them; in a talk through a door, the words of the one at the other end go through it.
    const speak = async (ids) => { for (const lid of [].concat(ids || [])) { const entry = g.lines[lid]; if (through && entry && entry[0] === through) await g.through(through, lid); else await g.say(lid); } };
    // The reply to the nth asking: a plain list is the same every time; { 1, 2, ..., more } says each in turn, `more` after the last given.
    const replyFor = (say, n) => {
      if (say == null || typeof say === "string" || Array.isArray(say)) return say;
      if (say[n] != null) return say[n];
      const last = Math.max(0, ...Object.keys(say).map(Number).filter((k) => k > 0));
      return n > last ? say.more : null;
    };
    const trail = [await root()];                       // the nodes on the way here, for "back"
    let node = trail[0];
    for (;;) {
      const spec = nodes[node];
      if (!spec) { if (node != null) console.warn(`g.talk: there is no node called "${node}".`); break; }
      await speak(spec.say);                            // on arriving: once, however many picks are made here
      let next = spec.then == null ? null : await resolve(spec.then);
      while (next == null) {                            // the node's choices, again after a pick that stays, until one leads away
        const open = (spec.options || []).filter((o) => (!o.when || o.when(g)) && !(o.once && count(node, o)));
        if (!open.length) { next = "exit"; break; }     // nothing to ask: the talk is over
        let pick = null;
        if (g.clock.skipping) pick = open.find((o) => o.then === "exit") || open[open.length - 1];     // a cutscene being skipped: the way out, else the last
        else {
          const picked = await this.choose(open.map((o) => ({ id: o.id, line: o.line, asked: count(node, o), exit: o.then === "exit" })), { through, talk: true });
          pick = open.find((o) => o.id === picked) || null;
        }
        if (!pick) { next = "exit"; break; }
        const key = keyOf(node, pick), n = (memory[key] = (memory[key] || 0) + 1);
        if (through) await g.through(through, pick.line); else await g.say(pick.line);
        await speak(replyFor(pick.say, n));
        for (const fact of [].concat(pick.set || [])) g.flag(fact, true);
        if (pick.do) await pick.do(g);
        next = pick.then == null ? null : await resolve(pick.then);
        if (g.clock.skipping) { next = "exit"; break; } // while skipping, one node is all a talk gets (its lines, facts and scripts still count)
      }
      if (next === "exit") break;
      if (next === "back") { if (trail.length > 1) trail.pop(); node = trail[trail.length - 1]; continue; }
      if (next === "root") { trail.length = 0; trail.push(await root()); node = trail[0]; continue; }
      if (next !== node) trail.push(next);
      node = next;
    }
  }

  clear() { this.el.innerHTML = ""; this.active = false; this.choosing = false; }
}
