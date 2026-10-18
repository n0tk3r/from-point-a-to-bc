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
import { picturesOf, bubble, thoughtURL, speakerIcon } from "../art/thoughts.js";      // ENGINE-17: thought pictures, and the speakers' little loudspeaker

// ENGINE-17: a thought is up for as long as a line of three words ("one two three, and"): 900 + 16 x 58 ms, at the usual speed.
export const THOUGHT_MS = 900 + 16 * 58;
const LIFT = 16;                            // from the top of a thinker's head to the bottom of his cloud: room for the puffs trailing down

export class Dialogue {
  constructor(game) {
    this.g = game;
    this.el = game.stage.querySelector("#dialogue");
    this.active = false;       // a line is on screen
    this.choosing = false;     // a list of choices is on screen
    this._next = false;
    this._shownAt = 0;
    this.faces = {};           // LETTERBOX-11: portraits for voices through a door, drawn once for each size ("sprite|pixels")
    this.loops = new Map();    // ENGINE-17: thoughts kept up over somebody (g.think(who, pictures, { loop: true })): who -> { names, el, hidden, key }
    this._told = new Set();
    game.clock.every(() => this.follow());
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
    const on = g.actor(who), variant = on && typeof on.variant === "function" ? on.variant() : null;      // NEVADA-12E: a painted lead's portrait in the variant he is in, if he is on the stage
    const key = person.sprite + "|" + px + (variant ? "|" + variant : "");
    if (!this.faces[key]) { const face = person.sprite ? portrait(person.sprite, px, variant) : null; if (face) this.faces[key] = face.toDataURL(); }     // (NEVADA-12E: nothing kept until there is a picture)
    if (this.faces[key]) img.src = this.faces[key];
    img.alt = person.name || who; img.draggable = false; img.className = "face";
    img.style.width = img.style.height = css + "px";
    return img;
  }

  async say(id, { through = null } = {}) {
    const g = this.g;
    const entry = g.lines[id];
    if (!entry) { console.warn("Missing line:", id); return; }
    const [who, text, pictures] = entry;                  // ENGINE-17: a third element is the pictures he thinks
    g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;
    if (g.clock.skipping) return;
    if (pictures != null) return this.thought(who, pictures, { line: id, through });      // ENGINE-17: a bubble, not words
    const looping = through ? null : this.loops.get(who);                                   // ENGINE-17: a thought kept up over him steps aside while he speaks
    if (looping) { looping.hidden++; this.follow(); }

    // LETTERBOX-11: a line through a door comes from someone in another century: their portrait stands beside the words,
    // in their colour, top centre as for anyone not on the stage, and nobody here moves their mouth for it.
    const person = g.cast[through || who] || {};
    const actor = through ? null : g.view.cast.get(who);
    // CAR-13E: in a scene seen through the lead's own eyes (game.js, `unseen`) whoever is not drawn (the lead himself, or anyone
    // hidden or faded to nothing) is placed as one off the stage, not over an invisible head (his mouth and hands may move: nobody
    // sees them). Off the stage is the scene's `wordsAt` ([x, y]: the middle of the words' bottom edge, x kept 210 pixels from
    // either side, as a speaker's is), or the top middle. (Elsewhere someone a script has put out of sight still speaks from
    // where he is, as those scripts mean: Little Sister inside the closet, Grandpa Joe inside the limousine.)
    const seen = actor && (!g.unseen || (!actor.hidden && actor.opacity > 0)) ? actor : null;
    const at = g.scene && g.scene.wordsAt;
    const off = Array.isArray(at) && at.length === 2 && at.every(Number.isFinite) ? [Math.min(Math.max(at[0], 210), W - 210), at[1]] : [W / 2, 150];
    let seed = 0;
    for (let i = 0; i < id.length; i++) seed = (seed * 31 + id.charCodeAt(i)) >>> 0;       // which gesture goes with this line
    const voiced = g.settings.voices ? g.audio.voice(id) : null;
    const showText = g.settings.subtitles || !voiced;

    let p = null, fit = () => {};
    {
      const actor = seen;                                  // CAR-13E: the words go by the speaker as seen (above)
      p = document.createElement("p");
      p.className = "say";
      p.hidden = !showText;
      p.style.color = person.color || "#fff";
      if (through) { p.classList.add("through"); p.append(this.face(through), Object.assign(document.createElement("span"), { textContent: text })); }      // LETTERBOX-11
      else p.textContent = text;
      // Above the speaker's head when they are on stage, otherwise top center (CAR-13E: or the scene's `wordsAt`).
      // While a close-up is showing, along the bottom, clear of whatever is being looked at.
      // (x, y) is where the middle of the bottom edge of the words goes, in picture pixels.
      const near = g.near;
      const x = near ? W / 2 : actor ? Math.min(Math.max(actor.x, 210), W - 210) : off[0];          // (CAR-13E: off, above)
      let top = actor ? actor.y - actor.h * actor.scale : 0;
      if (actor && !near) {
        // Someone taller standing close by, level with the speaker or nearer: lift the words clear of that head too,
        // so a small speaker's words are not written across a tall listener's face. (Not more than 90 pixels: the
        // words must still belong to the speaker.) NEVADA-12SB: or farther back, when the scene asks for it with the
        // sprite flag `clear` (Grandma Jolene behind her counter, whose face is just where the words of everyone at
        // the counter would go); and for her, anywhere under the words, which can be 400 pixels wide (css: .say), and
        // up to 110 pixels over the speaker's head.
        for (const other of g.view.cast.items.values()) {
          if (other === actor || !other.h || other.hidden || !(other.opacity > 0)) continue;
          const head = other.y - other.h * other.scale, clear = !!(other.flags && other.flags.clear), most = clear ? 110 : 90;
          if (Math.abs(other.x - x) < (clear ? 210 : 150) && (other.y > actor.y - 60 || clear) && head < top) top = Math.max(head, top - most, actor.y - actor.h * actor.scale - most);
        }
      }
      const y = near ? H - 12 : actor ? Math.max(top - 10, 60) : off[1];                            // (CAR-13E: off, above)
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
    if (looping) { looping.hidden = Math.max(0, looping.hidden - 1); this.follow(); }      // (ENGINE-17: and back)
    if (!g.clock.skipping) await g.clock.wait(90);       // a short beat between lines
  }

  // ---------------------------------------------------------------- ENGINE-17: thoughts
  /**
   * A thought: a bubble with one to three pictures in it over the thinker's head (js/art/thoughts.js), in place of words.
   * A line with pictures (its third element) is said this way by say(), which counts it as seen; g.think says one with no
   * line. It is timed (as long as a line of three words, or `ms`), and skippable as a line is (a click, a key, a cutscene
   * skipped). With { loop: true } it stays up over him until think(who, null), and steps aside while he says or thinks
   * anything else; it resolves at once. Through a door in time (`through`), it is beside his portrait, as his words would be.
   */
  async thought(who, spec, { ms = null, loop = false, line = null, through = null } = {}) {
    const g = this.g;
    if (spec == null || spec === false) { this.unloop(who); return; }
    const names = picturesOf(spec, line ? `the line "${line}"` : `g.think("${who}")`);
    if (loop) { this.unloop(who); this.loops.set(who, { names, el: null, hidden: 0, key: "" }); this.follow(); return; }
    if (g.clock.skipping) return;
    const looping = this.loops.get(who);
    if (looping) { looping.hidden++; this.follow(); }
    const el = this.bubbleFor(who, names, { through });
    this.active = true; this._next = false; this._shownAt = performance.now();
    let left = (ms ?? THOUGHT_MS) / (g.settings.textSpeed || 1);
    await new Promise((resolve) => {
      const stop = g.clock.every((dt) => {
        left -= dt;
        if (left <= 0 || this._next || g.clock.skipping) { stop(); resolve(); }
      });
    });
    el.remove();
    this.active = false;
    if (looping) { looping.hidden = Math.max(0, looping.hidden - 1); this.follow(); }
    if (!g.clock.skipping) await g.clock.wait(90);       // a short beat, as between lines
  }

  /** Where a thought of `who` goes: { head: [x, y] } over the top of his head when he is drawn on the stage (as his words
      would go), else { off: [x, y], up } where words go for someone off the stage (the scene's `wordsAt`, or the top
      middle), `up` when he is up above the scene on the stage (the lead looking down through a grille). */
  thinkerAt(who) {
    const g = this.g, actor = g.view.cast.get(who);
    if (actor && !actor.hidden && actor.opacity > 0 && actor.h) return { head: [actor.x, actor.y - actor.h * actor.scale] };
    const at = g.scene && g.scene.wordsAt;
    const off = Array.isArray(at) && at.length === 2 && at.every(Number.isFinite) ? [Math.min(Math.max(at[0], 210), W - 210), at[1]] : [W / 2, 150];
    const view = g.peeking, there = g.store.data.where[who];
    return { off, up: !!view && !actor && !!there && there.scene === view.from.id };
  }

  /** The bubble on the stage, in the words' layer: a picture drawn for it (bubble, in thoughts.js), placed in picture pixels
      and shown at the stage's scale, as the cast is (smooth below twice the size, hard pixels from there: css). Gives the element. */
  bubbleFor(who, names, { through = null } = {}) {
    const g = this.g, rim = (g.cast[through || who] || {}).color || "#ffffff";
    if (through) {                                     // through a door: the bubble beside the portrait, where the words would be
      const b = bubble(names, { rim }), p = document.createElement("p");
      p.className = "say through thinking";
      p.style.color = rim;
      const at = g.scene && g.scene.wordsAt;
      p.style.left = `${((Array.isArray(at) ? Math.min(Math.max(at[0], 210), W - 210) : W / 2) / W) * 100}%`;
      p.style.top = `${((Array.isArray(at) ? at[1] : 150) / H) * 100}%`;
      b.canvas.className = "thought";
      b.canvas.style.width = `${(b.size[0] / W) * 100}cqw`;
      p.append(this.face(through), b.canvas);
      this.el.appendChild(p);
      return p;
    }
    const n = names.length, cw = n * 24 + (n - 1) * 4 + 14, ch = 36, where = this.thinkerAt(who);
    let cx, by, toward;
    if (where.head) {
      const [hx, hy] = where.head;
      cx = Math.min(Math.max(hx, cw / 2 + 4), W - cw / 2 - 4);
      by = hy - LIFT;
      if (by - ch < 4) {                               // too near the top: beside the head instead, toward the middle of the stage
        cx = Math.min(Math.max(hx + (hx < W / 2 ? 1 : -1) * (cw / 2 + 18), cw / 2 + 4), W - cw / 2 - 4);
        by = Math.max(ch + 4, hy + 6);
      }
      toward = [hx - cx, hy - 3 - by];
    } else {
      [cx, by] = where.off;
      toward = where.up ? [0, -Math.min(44, Math.max(10, by - ch - 2))] : [0, 22];
    }
    const b = bubble(names, { rim, toward }), c = b.canvas;
    const left = Math.min(Math.max(cx - b.ox, 0), W - b.size[0]), top = Math.min(Math.max(by - b.oy, 0), H - b.size[1]);
    c.className = "thought";
    c.dataset.who = who;
    c.setAttribute("role", "img");
    c.setAttribute("aria-label", `${(g.cast[who] || {}).name || who} thinks: ${names.join(", ")}`);
    c.style.left = `${(left / W) * 100}%`; c.style.top = `${(top / H) * 100}%`; c.style.width = `${(b.size[0] / W) * 100}%`;
    c.dataset.box = [left, top, b.size[0], b.size[1]].map((v) => Math.round(v)).join(",");          // (where it is, in picture pixels: for the tests)
    c.dataset.cloud = [left + b.cloud[0], top + b.cloud[1], left + b.cloud[2], top + b.cloud[3]].map((v) => Math.round(v)).join(",");
    this.el.appendChild(c);
    return c;
  }

  /** Keep each looping thought over its thinker: drawn again where his head has gone, hidden while he says something else
      or is not on the stage. (Every frame; a thought whose thinker stands still is not drawn again.) */
  follow() {
    if (!this.loops.size) return;
    for (const [who, l] of this.loops) {
      const at = this.thinkerAt(who), show = !l.hidden && !!at.head;
      const key = show ? at.head.map(Math.round).join(",") : "";
      if (key === l.key && (!!l.el) === show) continue;
      if (l.el) { l.el.remove(); l.el = null; }
      l.key = key;
      if (show) { l.el = this.bubbleFor(who, l.names); l.el.classList.add("loop"); }
    }
  }
  /** A looping thought ends (g.think(who, null)). */
  unloop(who) { const l = this.loops.get(who); if (l && l.el) l.el.remove(); this.loops.delete(who); }

  // ---------------------------------------------------------------- ENGINE-17: the building's speakers
  /**
   * A line over a building's speakers (g.pa): nobody on the stage says it. A soft chime (`pa`), and it is shown at the top of
   * the stage in a narrow banner, a small loudspeaker drawn at its left, in the speaker's colour; timed, counted and
   * skippable as a line is. It is heard only in a scene that is in a building (`building: "office"`, or a function of the
   * game), in a grille's view too, and, given `building`, only in that one: anywhere else it is not shown, the console says
   * so (once), and it resolves false at once. `ambient`: shown without taking the controls or a click (the building's own
   * life, now and then: the scene's `announce`); one at a time. Resolves true when it has been heard. In a cut-scene, which
   * dresses the stage itself and may be in no scene's building, the `building` it names is where it is.
   */
  async pa(id, { building = null, ambient = false } = {}) {
    const g = this.g, entry = g.lines[id], scene = g.scene;
    if (!entry) { console.warn("Missing line:", id); return false; }
    const here = g.mode === "cutscene" && building ? building : scene ? (typeof scene.building === "function" ? scene.building(g) : scene.building) : null;
    if (!here || (building && building !== here)) {
      const key = id + "|" + (scene ? scene.id : "-");
      if (!this._told.has(key)) { this._told.add(key); console.warn(`g.pa("${id}"): ${scene ? `the scene "${scene.id}" is in ${here ? `the building "${here}"` : "no building"}` : "there is no scene"}${building ? `, not "${building}"` : ""}, so the speakers are not heard here.`); }
      return false;
    }
    if (ambient && this.el.querySelector(".pa")) return false;          // (one at a time)
    const [who, text, pictures] = entry;
    g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;
    if (g.clock.skipping) return true;
    const color = (g.cast[who] || {}).color || "#ffffff";
    g.sfx("pa");
    const p = document.createElement("p"), speaker = speakerIcon(color).cloneNode(), words = document.createElement("span");
    speaker.getContext("2d").drawImage(speakerIcon(color), 0, 0);
    speaker.className = "speaker";
    p.className = "pa" + (ambient ? " ambient" : "");
    p.style.color = color;
    if (pictures != null) for (const n of picturesOf(pictures, `the line "${id}"`)) words.appendChild(Object.assign(document.createElement("img"), { src: thoughtURL(n), alt: n, className: "pic" }));
    else words.textContent = text;
    p.append(speaker, words);
    p.dataset.line = id;
    this.el.appendChild(p);
    if (!ambient) { this.active = true; this._next = false; this._shownAt = performance.now(); }
    let left = (Math.max(1500, 900 + String(text).length * 58) + 400) / (g.settings.textSpeed || 1);       // (and a moment for the chime)
    await new Promise((resolve) => {
      const stop = g.clock.every((dt) => {
        left -= dt;
        if (left <= 0 || (!ambient && this._next) || g.clock.skipping || !p.isConnected) { stop(); resolve(); }
      });
    });
    p.remove();
    if (!ambient) { this.active = false; if (!g.clock.skipping) await g.clock.wait(90); }
    return true;
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
        const pics = g.lines[o.line] && g.lines[o.line][2];                         // ENGINE-17: a thing a lead who cannot talk "says" is the pictures he thinks
        if (pics != null) {
          const names = picturesOf(pics, `the line "${o.line}"`), words = b.textContent.trim();
          b.textContent = "";
          if (words && words !== "...") b.append(words + " ");
          for (const n of names) b.appendChild(Object.assign(document.createElement("img"), { src: thoughtURL(n), alt: "", className: "pic" }));
          b.setAttribute("aria-label", `${words && words !== "..." ? words + ": " : ""}${names.join(", ")}`);
        }
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

  // (ENGINE-17: a thought kept up is drawn again over its thinker, if he is still on the stage: after a cut-scene played over
  // the scene, say. The stage emptied (g.view.clear, as every scene is built) ends them all: forgetLoops.)
  clear() { this.el.innerHTML = ""; this.active = false; this.choosing = false; for (const l of this.loops.values()) { l.el = null; l.key = ""; } this.follow(); }
  /** ENGINE-17: every thought kept up ends (the stage is emptied). */
  forgetLoops() { for (const l of this.loops.values()) if (l.el) l.el.remove(); this.loops.clear(); }
}
