// The game object. It owns the clock, the saved state, sound, the stage and the
// interface, and it is the `g` handed to every scene and cutscene script:
//
//     await g.say("egypt.reeds.look");        speak a line (by ID)
//     const pick = await g.choose([...]);     offer things to say
//     g.give("reed");  g.has("reed");  g.take("reed");
//     g.flag("egypt.penGiven", true);         record a story fact
//     await g.goto("rome-forum", { via: "wormhole" });
//     await g.card("Ancient Egypt", "1250 B.C.");
//     await g.wait(500);  await g.tween(800, (k) => ...);  await g.fade(1);
//     await g.reach();                        the lead reaches out (g.reach(true): bends down)
//     g.team(["mom", "bigsis", "lilsis"]);    who the player can switch between
//     g.closeup(drawing);  g.closeup();       a close look at a screen or a notice, and putting it away
//
// Scripts are ordinary async functions. They read top to bottom like a screenplay.

import { Clock, ease } from "./clock.js";
import { Store, newGame, complete } from "./state.js";
import * as saves from "./save.js";
import { AudioEngine } from "./audio.js";
import { Dialogue } from "./dialogue.js";
import { SceneView, footOf } from "./scene.js";
import { WalkMap, scaleAt } from "./walk.js";
import { UI } from "./ui.js";
import { tunnel } from "./fx.js";
import { openBeats, checkStory, leadsOf, hintFor } from "./story.js";
import * as art from "../art/kit.js";

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const copy = (data) => JSON.parse(JSON.stringify(data));

export class Game {
  constructor(content) {
    Object.assign(this, content);        // sceneIds, loadScene, cutscenes, lines, cast, eras, items, story, sound
    this.scenes = {};                    // scene files already fetched
    this.art = art;
    this.ease = ease;
    this.stage = document.getElementById("stage");
    this.fadeEl = this.stage.querySelector("#fade");
    this.cardEl = this.stage.querySelector("#card");
    this.titleEl = this.stage.querySelector("#title");
    this.fxEl = this.stage.querySelector("#fx");
    this.closeEl = this.stage.querySelector("#closeup");
    this.leads = Object.keys(this.cast).filter((id) => this.cast[id].lead);     // everyone the player can ever control
    this.systemCalm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    this.clock = new Clock();
    this.store = new Store(newGame(this.leads));
    this.settings = saves.loadSettings();
    this.applyCalm();
    this.audio = new AudioEngine(this.settings, content.sound);
    this.view = new SceneView(this.stage);
    this.view.cast.calm = this.calm;
    this.dialogue = new Dialogue(this);
    this.ui = new UI(this);

    this.mode = "boot";      // boot, cutscene, title or play
    this.busy = 0;           // above zero while a script has control
    this.scene = null;
    this.held = null;        // the inventory item in the player's hand
    this.lookMode = false;
    this._fade = 0;
    this._nope = 0;
    this._chats = {};        // how many times each pair has talked, so they do not repeat themselves at once

    this.store.on(() => { this.ui.refresh(); this.view.refreshHotspots(this); });
  }

  get mode() { return this._mode; }
  set mode(value) { this._mode = value; document.body.dataset.mode = value; }   // lets the style sheet react to it

  // =============== start-up ===============
  async boot() {
    this.clock.start();
    this.clock.every((dt) => { if (this.mode === "play") this.store.data.playMs += dt; });
    this.clock.every((dt) => this.view.cast.update(dt));                 // animate and repaint the people and props
    this.bindInput();
    const known = Object.fromEntries(this.sceneIds.map((id) => [id, true]));
    for (const problem of checkStory({ story: this.story, scenes: known, cutscenes: this.cutscenes, lines: this.lines })) console.warn("Story check:", problem);
    try { await document.fonts.load('16px "Koine Road"'); } catch { /* the fallback font will do */ }

    const params = new URLSearchParams(location.search);
    await this.ui.gate(() => this.audio.unlock());

    // Shortcuts for building scenes:  index.html?scene=rome-forum&lead=son
    // Every act before the scene's own counts as played. &flags=a,b makes more story facts true.
    const jump = params.get("scene");
    if (jump && this.sceneIds.includes(jump)) {
      const data = this.freshState(), acts = this.story.acts;
      const at = acts.findIndex((act) => act.beats.some((b) => b.scene === jump));
      for (const act of acts.slice(0, Math.max(0, at))) for (const b of act.beats) data.flags[b.sets] = true;
      for (const fact of (params.get("flags") || "").split(",")) if (fact) data.flags[fact] = true;
      const first = at < 0 ? null : acts[at].beats.find((b) => b.scene === jump);
      const lead = params.get("lead") || (first && leadsOf(this.story, first)[0]);
      if (this.leads.includes(lead)) data.active = lead;
      this.store.reset(data);
      return this.goto(jump, { via: "cut" });
    }
    if (!this.settings.seenIntro || params.has("intro")) {
      await this.cutscene("intro");
      this.setOption("seenIntro", true);
    }
    await this.title();
  }

  /** The title screen. It rebuilds everything it needs, so it is safe to call from anywhere. */
  async title() {
    this.mode = "title";
    this.scene = null;
    this.dialogue.clear();
    this.closeup();
    this.ui.close();
    this.ui.hud(false);
    this.view.clear();
    this.view.setEra("present");
    await this.view.draw(art.highway(), "Dusk on a desert highway. A family station wagon heads for a swirling time portal, past a road sign where Point B has been crossed out and B.C. painted in.");
    this.view.cast.addThing("wagon", "wagon", 184, 182, 0.72).flag("bounce", true);
    const strip = this.titleEl.querySelector(".strip"), kicker = this.titleEl.querySelector(".kicker");
    strip.style.clipPath = "inset(-20% 100% -20% -5%)";
    kicker.style.opacity = 0;
    this.titleEl.hidden = false;
    this.music("title");
    await this.fade(0, 700);
    // The papyrus unrolls from the left, then the menu arrives.
    await this.tween(900, (k) => { strip.style.clipPath = `inset(-20% ${100 - k * 105}% -20% -5%)`; }, ease.out);
    strip.style.clipPath = "";
    await this.tween(350, (k) => { kicker.style.opacity = k; });
    this.ui.titleMenu();
  }

  /** The state a new game starts from: the story says who leads and what is already true. */
  freshState() {
    const data = newGame(this.leads);
    data.active = this.story.start.lead;
    data.team = [...(this.story.start.team || [])];
    for (const fact of this.story.start.flags || []) data.flags[fact] = true;
    return data;
  }

  async newGame() {
    this.ui.close();
    this.store.reset(this.freshState());
    await this.fade(1, 500);
    await this.goto(this.story.start.scene, { via: "cut" });
  }

  // =============== the script API ===============
  wait(ms) { return this.clock.wait(ms); }
  tween(ms, step, easing) { return this.clock.tween(ms, step, easing); }
  async say(...ids) { for (const id of ids) await this.dialogue.say(id); }
  choose(options) { return this.dialogue.choose(options); }
  flag(name, value) { return this.store.flag(name, value); }
  has(item) { return this.store.has(item); }
  take(item) { if (this.held === item) this.held = null; this.store.take(item); }
  give(item) {
    if (this.store.has(item)) return;
    this.store.give(item);
    this.sfx("pickup");
    if (!this.clock.skipping) this.ui.toast(`You have the ${this.items[item].name}`);
  }
  /** Who is carrying a thing: a lead's id, or null. */
  holder(item) { return this.store.holder(item); }
  /** Say which leads the player can switch between from now on. */
  team(list) { this.store.data.team = list.filter((id) => this.leads.includes(id)); this.store.emit(); }
  music(id) { this.audio.music(id); }
  sfx(id) { if (!this.clock.skipping) this.audio.sfx(id); }
  actor(id) { return this.view.cast.get(id); }
  get lead() { return this.view.cast.get(this.store.data.active); }
  q(selector) { return this.view.q(selector); }
  /** The lead reaches for something: out in front, or (low) down to the ground. */
  reach(low = false) { return this.lead ? this.lead.play(this.clock, low ? "pick" : "reach") : Promise.resolve(); }
  /** For scripts: someone (the lead, unless another is named) walks to a place, round whatever is in the way. */
  async walkTo(x, y, who = null) {
    const actor = who ? this.actor(who) : this.lead, scene = this.scene;
    if (!actor || !actor.walkPath || !scene || !this.map) return;
    await actor.walkPath(this.clock, this.map.path([actor.x, actor.y], [x, y]), (yy) => scaleAt(scene, yy));
    this.rememberPlace(actor.id);
  }
  /** For scripts: walk in a straight line to a place, even one the player could not click on (into a closet, behind a counter). */
  async moveTo(x, y, who = null) {
    const actor = who ? this.actor(who) : this.lead, scene = this.scene;
    if (!actor || !actor.walkPath || !scene) return;
    await actor.walkPath(this.clock, [[x, y]], (yy) => scaleAt(scene, yy));
    this.rememberPlace(actor.id);
  }

  /** A close look at something small: a screen, a notice, a note. Pass a drawing on the 320x200 grid to show it,
      and nothing to put it away. People carry on talking underneath it. */
  closeup(markup = null, label = "") {
    const el = this.closeEl;
    if (!el) return;
    // (the layer is an SVG element, which has no `hidden` property of its own: the attribute is what counts)
    if (!markup || this.clock.skipping) { el.setAttribute("hidden", ""); el.innerHTML = ""; return; }
    el.innerHTML = `<rect class="veil" width="320" height="200"/>${markup}`;
    el.setAttribute("aria-label", label);
    el.removeAttribute("hidden");
  }
  /** Is a close-up showing? */
  get near() { return !!this.closeEl && !this.closeEl.hasAttribute("hidden"); }

  /** Wait for a click or a key (or for `max` milliseconds, whichever comes first). */
  tap(max = 60000) {
    if (this.clock.skipping) return Promise.resolve();
    this._tapped = false;
    return new Promise((resolve) => {
      let left = max;
      const stop = this.clock.every((dt) => {
        left -= dt;
        if (left <= 0 || this._tapped || this.clock.skipping) { stop(); resolve(); }
      });
    });
  }

  /** Fade the picture out (to = 1) or in (to = 0). */
  async fade(to, ms = 400, color = "#000") {
    const el = this.fadeEl, from = this._fade;
    if (this.calm) color = "#000";                 // no white flashes for players who asked for less motion
    el.style.background = color;
    this._fade = to;
    await this.clock.tween(ms, (k) => { el.style.opacity = from + (to - from) * k; }, ease.linear);
  }

  /** A title card: an era name on a strip of papyrus, or plain words on the picture. */
  async card(title, sub = "", { ms = 2400, plain = false } = {}) {
    if (this.clock.skipping) return;
    const el = this.cardEl;
    const words = `<h2>${esc(title)}</h2>`;
    el.className = "layer" + (plain ? " plain" : "");
    el.innerHTML = (plain ? words : `<div class="strip"><div class="papyrus">${words}</div></div>`) + (sub ? `<p>${esc(sub)}</p>` : "");
    void el.offsetWidth;
    el.classList.add("show");
    this._cardNext = false;                      // a click or a key moves on early
    await new Promise((resolve) => {
      let left = ms;
      const stop = this.clock.every((dt) => {
        left -= dt;
        if (left <= 0 || this._cardNext || this.clock.skipping) { stop(); resolve(); }
      });
    });
    el.classList.remove("show");
    await this.wait(380);
    el.innerHTML = "";
  }

  /** Play a cutscene. The player can skip it; skipping runs the same script
      instantly, so the game always ends up in the same state. */
  async cutscene(id) {
    const script = this.cutscenes[id];
    if (!script) throw new Error(`No cutscene called "${id}"`);
    const before = this.mode;
    this.mode = "cutscene";
    this.busy++;
    this.ui.close();
    this.ui.hud(false);
    this.ui.showSkip(true);
    try {
      await script(this);
    } catch (err) {
      console.error(`Cutscene "${id}" stopped:`, err);
    } finally {
      this.clock.skipping = false;
      if (this.stopFx) { this.stopFx(); this.stopFx = null; }
      this.dialogue.clear();
      this.closeup();
      this.cardEl.classList.remove("show");
      this.cardEl.innerHTML = "";
      this.ui.showSkip(false);
      this.busy--;
      this.mode = before;
    }
  }

  skip() {
    if (this.mode !== "cutscene" || this.clock.skipping) return;
    this.clock.skipping = true;
    this.audio.stopVoice();
  }

  /** Start the time tunnel on the canvas. stopTunnel() ends it. */
  startTunnel(dates = []) {
    if (this.clock.skipping) return;
    this.stopTunnel();
    this.stopFx = tunnel(this.fxEl, this.clock, { dates, calm: this.calm });
  }
  stopTunnel() { if (this.stopFx) { this.stopFx(); this.stopFx = null; } }

  /** The short trip between two eras. */
  async wormhole(ms = 1600) {
    this.sfx("portal");
    await this.fade(1, 260, "#fff");
    if (this.clock.skipping) return;
    this.ui.hud(false);
    this.startTunnel();
    this.music("tunnel");
    await this.fade(0, 220, "#fff");
    await this.wait(ms);
    await this.fade(1, 260, "#fff");
    this.stopTunnel();
  }

  // =============== scenes ===============
  /** Fetch a scene file the first time it is needed, then keep it. */
  async getScene(id) {
    if (!this.sceneIds.includes(id)) throw new Error(`No scene called "${id}". Add it to js/content/scenes/index.js.`);
    if (!this.scenes[id]) this.scenes[id] = this.loadScene(id);      // keep the promise, so two askers share one fetch
    return this.scenes[id];
  }

  /** Go to a scene. via: "fade" (default), "wormhole" or "cut". */
  async goto(id, { via = "fade", spawn = "default", at = null } = {}) {
    const from = this.scene;
    this.busy++;
    try {
      const loading = this.getScene(id);         // fetch during the fade, not after it
      loading.catch(() => {});
      if (via === "wormhole") await this.wormhole();
      else if (via === "fade") await this.fade(1, 300);
      else { this._fade = 1; this.fadeEl.style.opacity = 1; }
      let scene;
      try { scene = await loading; }
      catch (err) {                                // the file would not load: come back to where we were
        console.error(err);
        this.stopTunnel();
        delete this.scenes[id];
        if (from) this.music(from.music || this.eras[from.era].music);
        await this.fade(0, 300);
        this.ui.hud(this.mode === "play");
        this.ui.toast("That part of the game would not load. Check your connection and try again.", 4500);
        return;
      }
      const marks = scene.spawn || {};         // a named way in, then this lead's own mark, then the usual one
      await this.enterScene(scene, at || (spawn !== "default" && marks[spawn]) || marks[this.store.data.active] || marks.default);
      await this.fade(0, via === "wormhole" ? 700 : 400, via === "wormhole" ? "#fff" : "#000");
      if (!from || from.era !== scene.era) {
        const era = this.eras[scene.era];
        await this.card(era.name, era.date);
      }
      if (scene.enter) await scene.enter(this, from ? from.id : null);
    } finally {
      this.busy--;
      this.settle();
      this.ui.refresh();
    }
    this.autosave();
  }

  /** Build a scene on the stage from the saved state. No story happens here. */
  async enterScene(scene, pos) {
    const d = this.store.data, cast = this.view.cast;
    this.dialogue.clear();
    this.closeup();
    this.held = null;
    this.lookMode = false;
    this.view.clear();
    this.scene = scene;
    this.mode = "play";
    this.titleEl.hidden = true;
    this.view.setEra(scene.era);
    // a painted picture, a drawing made with the kit, or both; with neither, the scene is sketched as labelled boxes
    const drawn = this.view.draw(scene.draw ? scene.draw(art, this) : scene.picture ? "" : art.sketch(scene), scene.name, scene.picture);

    // Props and people who are not the lead. Each can block the ground it stands on.
    const blocked = [...(scene.blocked || [])];
    for (const p of scene.props || []) {
      if (p.when && !p.when(this)) continue;
      const thing = cast.addThing(p.id, p.kind, p.at[0], p.at[1], p.scale ?? 1, p.options);
      thing.plane = p.plane || "floor";
      thing.base = p.base || null;
      if (p.solid) blocked.push(p.solid);
    }
    for (const a of scene.actors || []) {
      if (a.when && !a.when(this)) continue;
      const s = a.scale ?? scaleAt(scene, a.at[1]);
      cast.addFigure(a.id, a.kind || a.id, a.at[0], a.at[1], s).face(a.face ?? "S");
      if (a.solid !== false) blocked.push(a.solid || [[a.at[0] - 13 * s, a.at[1] - 5], [a.at[0] + 13 * s, a.at[1] - 5], [a.at[0] + 13 * s, a.at[1] + 3], [a.at[0] - 13 * s, a.at[1] + 3]]);
    }
    this.map = new WalkMap(scene, blocked);                 // where the lead may stand, and how to get around things

    const want = pos || (scene.spawn && scene.spawn.default) || [160, 190];
    const [x, y] = this.map.nearest(want[0], want[1]);
    const was = d.where[d.active], facing = was && was.scene === scene.id && was.face != null && pos ? was.face : scene.facing || "S";
    cast.addFigure(d.active, this.cast[d.active].sprite, x, y, scaleAt(scene, y)).face(facing);
    d.scene = scene.id;
    d.where[d.active] = { scene: scene.id, x: Math.round(x), y: Math.round(y), face: this.lead.yaw };

    // A scene can name a party: leads who are here together. They arrive with whoever is leading,
    // each on their own mark, and the player can switch between them.
    const party = (scene.party || []).filter((id) => this.leads.includes(id));
    if (party.includes(d.active)) {
      party.forEach((id, n) => {
        if (!d.team.includes(id)) d.team.push(id);
        const at = d.where[id];
        if (id === d.active || (at && at.scene === scene.id)) return;
        const mark = (scene.spawn && scene.spawn[id]) || [x + 22 * (n + 1), y];
        d.where[id] = { scene: scene.id, x: mark[0], y: mark[1] };
      });
    }
    // Anyone else on the team who is standing in this scene is on stage too.
    for (const id of d.team) {
      const at = d.where[id];
      if (id === d.active || !at || at.scene !== scene.id) continue;
      const [mx, my] = this.map.nearest(at.x ?? x, at.y ?? y);
      cast.addFigure(id, this.cast[id].sprite, mx, my, scaleAt(scene, my)).face(at.face ?? (scene.facing || "S"));
    }
    if (scene.setup) scene.setup(this);          // match the drawing to the story facts
    this.rebuildSpots();
    this.music(scene.music || this.eras[scene.era].music);
    this.ui.hud(true);
    this.ui.refresh();
    for (const next of scene.exits || []) this.getScene(next).catch(() => {});   // warm up the places you can go from here
    await drawn;
  }

  /** Run a piece of script with the controls locked. */
  async run(script) {
    this.busy++;
    this.ui.refresh();
    try { await script(); }
    catch (err) { console.error("Script stopped:", err); }
    finally { this.busy--; this.closeup(); this.settle(); this.ui.refresh(); }
  }

  /** An action can be a line ID, a list of line IDs, a function, or one of those for each lead:
      { dad: ..., son: ..., any: ... } (`any` is for whoever is not named). */
  async act(action) {
    if (action == null) return false;
    if (typeof action === "function") { await action(this); return true; }
    if (typeof action === "string") { await this.say(action); return true; }
    if (Array.isArray(action)) { await this.say(...action); return true; }
    return this.act(action[this.store.data.active] ?? action.any);
  }

  /** A stock reply for things nobody wrote a line for. */
  fallback(kind) {
    const table = this.story.fallbacks[kind] || {}, list = table[this.store.data.active] || table.any || [];
    return list.length ? list[this._nope++ % list.length] : null;
  }

  // =============== companions ===============
  /** The clickable areas: the scene's own, and one over each companion standing here. */
  rebuildSpots() {
    const scene = this.scene, d = this.store.data;
    if (!scene) return;
    const spots = [...(scene.hotspots || [])];
    for (const id of d.team) {
      const a = id === d.active ? null : this.actor(id);
      if (!a) continue;
      const w = 20 * a.scale, h = a.h * a.scale;
      spots.push({ id: "mate." + id, name: this.cast[id].name, verb: "Talk to", mate: id, rect: [a.x - w / 2, a.y - h, w, h] });
    }
    this.view.setHotspots(spots);
    this.view.refreshHotspots(this);
    this.ui.hover(null);
  }

  /** After a script has moved people about: note where everyone on the team is standing, and move their clickable areas. */
  settle() {
    if (!this.scene || this.mode !== "play") return;
    for (const id of this.store.data.team) this.rememberPlace(id);
    this.rebuildSpots();
  }

  /** A place to stand that no companion is already standing on: the place asked for, or a step to one side of it. */
  clearOf(at) {
    if (!at) return at;
    const d = this.store.data, others = d.team.filter((id) => id !== d.active).map((id) => this.actor(id)).filter(Boolean);
    const taken = (x, y) => others.some((a) => Math.abs(a.x - x) < 15 && Math.abs(a.y - y) < 6);
    for (const dx of [0, 17, -17, 34, -34]) {
      const x = at[0] + dx, y = at[1] + (dx ? 2 : 0);
      if (!taken(x, y) && (dx === 0 || this.map.ok(x, y))) return [x, y];
    }
    return at;
  }

  /** A place to stand for a word with a companion: beside them, on the side the lead is coming from. */
  beside(mate) {
    const lead = this.lead, reach = 22 * mate.scale;
    if (Math.abs(lead.x - mate.x) <= reach + 6 && Math.abs(lead.y - mate.y) <= 5) return null;      // near enough already
    return [mate.x + (lead.x <= mate.x ? -reach : reach), mate.y + 1];
  }

  /** A few words with a companion. The scene supplies them, as talk: { mom: { bigsis: [exchange, ...] } },
      where an exchange is a list of line IDs or { when(g), say: [...] }. What has not been heard comes first. */
  async chat(to) {
    const who = this.store.data.active, key = `${this.scene.id}|${who}|${to}`;
    const from = (table) => (table && table[who] && table[who][to]) || null;
    let list = from(this.scene.talk) || from(this.story.talk) || [];
    if (typeof list === "function") list = list(this);
    list = list.filter((e) => !e.when || e.when(this));
    if (!list.length) { const line = this.fallback("look"); if (line) await this.say(line); return; }
    const heard = (e) => { const first = [].concat(e.say || e)[0]; return typeof first !== "string" || this.store.data.seenLines[first]; };
    const n = (this._chats[key] = (this._chats[key] || 0) + 1);
    const pick = list.find((e) => !heard(e)) || list[(n - 1) % list.length];
    await this.act(pick.say || pick);
  }

  /** The lead gives something they are carrying to a companion. A scene can react with given(g, item, to, from). */
  async handOver(item, to) {
    const from = this.store.data.active, lines = (this.story.give && this.story.give[from]) || [];
    if (lines.length) await this.say(lines[this._nope++ % lines.length]);
    await this.reach();
    if (!this.store.pass(item, to)) return;
    this.sfx("pickup");
    if (!this.clock.skipping) this.ui.toast(`${this.cast[to].name} has the ${this.items[item].name}`);
    if (this.scene.given) await this.scene.given(this, item, to, from);
  }

  async interact(spot, verb = "use") {
    if (this.busy || this.mode !== "play") return;
    await this.run(async () => {
      const lead = this.lead, scene = this.scene, mate = spot.mate ? this.actor(spot.mate) : null;
      const stand = mate ? this.beside(mate) : this.clearOf(spot.walkTo);
      if (stand) await lead.walkPath(this.clock, this.map.path([lead.x, lead.y], stand), (yy) => scaleAt(scene, yy));
      if (spot.face) lead.face(spot.face); else lead.look(...footOf(spot));       // turn to the thing
      this.rememberPlace();
      const item = this.held;
      if (mate) {                                                                  // a companion: talk, look, or hand something over
        mate.look(lead.x, lead.y);
        if (item) { this.held = null; this.ui.refresh(); await this.handOver(item, spot.mate); }
        else if (verb === "look") { const see = this.story.see && this.story.see[this.store.data.active]; await this.say((see && see[spot.mate]) || this.fallback("look")); }
        else await this.chat(spot.mate);
      } else if (item) {
        this.held = null;
        this.ui.refresh();
        if (!(await this.act(spot.useWith && spot.useWith[item]))) await this.say(this.fallback("nope"));
      } else if (verb === "look" || !spot.use) {
        if (!(await this.act(spot.look))) await this.say(this.fallback("look"));
      } else {
        await this.act(spot.use);
      }
    });
    this.autosave();
  }

  walk(x, y) {
    const lead = this.lead, scene = this.scene;
    if (!lead || !scene || this.busy) return;
    lead.walkPath(this.clock, this.map.path([lead.x, lead.y], [x, y]), (yy) => scaleAt(scene, yy)).then(() => this.rememberPlace());
  }

  async useItem(item) {
    if (this.busy) return;
    if (this.lookMode) {
      this.lookMode = false;
      return this.run(() => this.act(this.items[item].look));
    }
    this.held = this.held === item ? null : item;
    this.ui.refresh();
  }

  async hint() {
    if (this.busy || this.mode !== "play") return;
    const d = this.store.data, who = d.active;
    // A beat can carry one hint, spoken by whoever does it, or one for each lead: the doer's says
    // what to try, and the others' say whose job it is. The lead's own jobs come first.
    const open = openBeats(this.story, d.flags).filter((b) => hintFor(this.story, b, who));
    const beat = open.find((b) => leadsOf(this.story, b).includes(who)) || open[0];
    const line = beat ? hintFor(this.story, beat, who) : this.fallback("hint");
    if (line) await this.run(() => this.say(line));
  }

  /** Change which lead the player controls. Each lead keeps their own place and pockets. */
  async switchLead(to) {
    const d = this.store.data;
    if (this.busy || this.mode !== "play" || d.active === to || !d.team.includes(to)) return;
    this.rememberPlace();
    const place = d.where[to];
    if (!place || !place.scene) return;
    if (this.scene && place.scene === this.scene.id && this.actor(to)) {      // standing right here: hand over the controls
      const old = this.lead;
      if (old && old._stop) old._stop();
      this.held = null;
      this.lookMode = false;
      d.active = to;
      this.sfx("switch");
      this.settle();
      this.store.emit();
      this.autosave();
      return;
    }
    d.active = to;
    await this.goto(place.scene, { at: place.x != null ? [place.x, place.y] : null });
  }

  // =============== saving ===============
  /** Note where a lead is standing (the active one, unless another is named). */
  rememberPlace(who = this.store.data.active) {
    const d = this.store.data, a = this.actor(who);
    if (a && this.scene && this.leads.includes(who)) d.where[who] = { scene: this.scene.id, x: Math.round(a.x), y: Math.round(a.y), face: a.yaw };
  }
  snapshot() { this.rememberPlace(); return copy(this.store.data); }
  meta() {
    const era = this.eras[this.scene.era];
    return { scene: this.scene.name, era: `${era.name}${era.date ? ", " + era.date : ""}`, lead: this.cast[this.store.data.active].name, playMs: Math.round(this.store.data.playMs) };
  }
  autosave() {
    if (this.mode === "play" && this.scene && !this.busy) saves.writeSlot("auto", this.snapshot(), this.meta());
  }
  saveSlot(slot) {
    const ok = saves.writeSlot(slot, this.snapshot(), this.meta());
    this.ui.toast(ok ? `Saved in slot ${slot}` : "This browser would not store the save. Use Save to a file.");
    return ok;
  }
  async saveFile() {
    const how = await saves.exportFile(saves.pack(this.snapshot(), this.meta()));
    if (how === "download") this.ui.toast("Save file sent to your downloads");
    if (how === "picker") this.ui.toast("Save file written");
  }
  async loadFile(file) {
    try { await this.load(await saves.importFile(file)); }
    catch (err) { this.ui.toast(err.message, 4200); }
  }

  /** Start playing from a save (a slot or an imported file). */
  async load(body) {
    if (!body) return;
    const data = complete(copy(body.data), this.leads);
    if (!this.leads.includes(data.active) || !this.sceneIds.includes(data.scene)) { this.ui.toast("That save is from a part of the game this version does not have.", 4200); return; }
    this.ui.close();
    this.busy++;
    try {
      const loading = this.getScene(data.scene);
      await this.fade(1, 300);
      const scene = await loading;
      this.store.reset(data);
      const place = data.where[data.active] || {};
      await this.enterScene(scene, place.x != null ? [place.x, place.y] : null);
      await this.fade(0, 400);
      this.ui.toast("Game loaded");
      if (scene.enter) await scene.enter(this, null);   // finish an arrival the save interrupted
    } finally {
      this.busy--;
      this.settle();
      this.ui.refresh();
    }
  }

  setOption(key, value) {
    this.settings[key] = value;
    saves.storeSettings(this.settings);
    this.audio.applyVolumes();
    this.applyCalm();
  }

  /** Less motion: decoration holds still, flashes become fades, the tunnel drifts. */
  applyCalm() {
    this.calm = this.systemCalm || !!this.settings.calm;
    this.stage.classList.toggle("calm", this.calm);
    if (this.view) this.view.cast.calm = this.calm;
  }

  // =============== input ===============
  bindInput() {
    const hot = this.view.hotEl;
    const spotOf = (event) => {
      const el = event.target.closest ? event.target.closest(".spot") : null;
      return el ? this.view.spots[el.dataset.i] : null;
    };

    // A click while someone is talking moves to the next line, whatever was clicked.
    this.stage.addEventListener("click", (event) => {
      this._tapped = true;
      if (this.cardEl.classList.contains("show")) this._cardNext = true;
      if (this.dialogue.active && !event.target.closest("button")) {
        this.dialogue.advance();
        event.stopPropagation();
      }
    }, true);

    // Touch screens have no right-click: press and hold looks at a thing.
    let hold = null, held = false;
    const letGo = () => clearTimeout(hold);
    hot.addEventListener("pointerdown", (event) => {
      const spot = spotOf(event);
      held = false;
      if (!spot || event.pointerType === "mouse") return;
      hold = setTimeout(() => { held = true; this.interact(spot, "look"); }, 550);
    });
    hot.addEventListener("pointerup", letGo);
    hot.addEventListener("pointercancel", letGo);
    hot.addEventListener("pointerleave", letGo);

    hot.addEventListener("click", (event) => {
      if (held) { held = false; return; }             // that press was a look, not a tap
      // A mouse click leaves keyboard focus on the thing clicked. Drop it, or pressing
      // Space to hurry a line along would click the same thing again.
      if (event.detail && document.activeElement && document.activeElement.blur) document.activeElement.blur();
      if (this.mode !== "play" || this.busy) return;
      const spot = spotOf(event);
      const verb = this.lookMode ? "look" : "use";
      this.lookMode = false;
      if (spot) this.interact(spot, verb);
      else if (this.held) { this.held = null; this.ui.refresh(); }
      else { this.ui.refresh(); this.walk(...this.view.toGrid(event)); }
    });
    hot.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      const spot = spotOf(event);
      if (spot) this.interact(spot, "look");
      else if (this.held) { this.held = null; this.ui.refresh(); }
    });
    hot.addEventListener("pointerover", (event) => this.ui.hover(spotOf(event)));
    hot.addEventListener("pointerleave", () => this.ui.hover(null));
    hot.addEventListener("focusin", (event) => this.ui.hover(spotOf(event)));
    hot.addEventListener("focusout", () => this.ui.hover(null));
    hot.addEventListener("keydown", (event) => {
      const spot = spotOf(event);
      if (!spot) return;
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); this.interact(spot, "use"); }
      else if (event.key.toLowerCase() === "l") this.interact(spot, "look");
    });

    document.addEventListener("keydown", (event) => {
      const key = event.key;
      // Keys typed into a slider or a tick box belong to it. Esc still closes the menu.
      if (key !== "Escape" && event.target.closest && event.target.closest("input, select, textarea")) return;
      if (key === "Escape") {
        if (this.mode === "cutscene") this.skip();
        else if (this.ui.open) this.ui.back();
        else this.ui.pauseMenu();
      } else if ((key === " " || key === "Enter") && this.cardEl.classList.contains("show")) {
        event.preventDefault();
        this._cardNext = true;
      } else if ((key === " " || key === "Enter" || key === ".") && this.dialogue.active) {
        event.preventDefault();
        this.dialogue.advance();
      } else if ((key === " " || key === "Enter") && this.near) {
        event.preventDefault();
        this._tapped = true;
      } else if (this.dialogue.choosing && key >= "1" && key <= "9") {
        const option = this.stage.querySelectorAll(".choices button")[Number(key) - 1];
        if (option) option.click();
      } else if (key >= "1" && key <= "9" && this.mode === "play" && !this.ui.open) {      // 1, 2, 3: play as that member of the team
        const to = this.ui.team()[Number(key) - 1];
        if (to) this.switchLead(to);
      } else if (key.toLowerCase() === "h") {
        hot.classList.add("reveal");
      }
    });
    document.addEventListener("keyup", (event) => { if (event.key.toLowerCase() === "h") hot.classList.remove("reveal"); });

    // If a browser put the sound to sleep, the next click or key wakes it.
    const wake = () => { if (this.mode !== "boot" && !document.hidden) this.audio.unlock(); };
    document.addEventListener("pointerdown", wake, { passive: true });
    document.addEventListener("keydown", wake);

    // Dropping a save file anywhere on the game loads it.
    this.stage.addEventListener("dragover", (event) => event.preventDefault());
    this.stage.addEventListener("drop", (event) => {
      event.preventDefault();
      const file = event.dataTransfer && event.dataTransfer.files[0];
      if (file && this.mode !== "cutscene" && this.mode !== "boot") this.loadFile(file);
    });

    // Switching to another tab saves the game and silences it. Coming back picks up the tune.
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) this.autosave();
      this.audio.hush(document.hidden);
    });
  }
}
