// The game object. It owns the clock, the saved state, sound, the stage and the
// interface, and it is the `g` handed to every scene and cutscene script:
//
//     await g.say("egypt.reeds.look");        speak a line (by ID)
//     const pick = await g.choose([...]);     offer things to say
//     g.give("reed");  g.has("reed");  g.take("reed");
//     g.flag("egypt.penGiven", true);         record a story fact
//     await g.goto("rome-steps", { via: "wormhole" });
//     await g.card("Ancient Egypt", "about 1920 B.C.");
//     await g.wait(500);  await g.tween(800, (k) => ...);  await g.fade(1);
//     await g.reach();                        the lead reaches out (g.reach(true): bends down)
//     g.team(["mom", "bigsis", "lilsis"]);    who the player can switch between
//     g.closeup(drawing);  g.closeup();       a close look at a screen or a notice, and putting it away
//     g.plane("trunk").show(false);           a painted cut-out of the scene: show, set(state), fade, place
//
// Scripts are ordinary async functions. They read top to bottom like a screenplay.
// Every position is a pixel on the 800x600 picture (grid.js).

import { Clock, ease } from "./clock.js";
import { Store, newGame, complete } from "./state.js";
import * as saves from "./save.js";
import { AudioEngine } from "./audio.js";
import { Dialogue } from "./dialogue.js";
import { SceneView, footOf, picturesIn } from "./scene.js";
import { Cutout } from "./cast.js";
import * as castKit from "./cast.js";               // (castKit.forget: the paints, below)
import { keyScene } from "../art/look.js";
import { WalkMap, scaleAt } from "./walk.js";
import { W, H, OLD, fit } from "./grid.js";
import { hold, url, picture } from "./assets.js";
import { UI, iconPath } from "./ui.js";
import { tunnel } from "./fx.js";
import { openBeats, checkStory, leadsOf, hintFor } from "./story.js";
import { BANDS, edgeAt, edgeLabel, open, checkEdges } from "./edges.js";
import { Outlines } from "./outline.js";
import { Life } from "./life.js";
import { Effects } from "./effects.js";
import * as art from "../art/kit.js";

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const copy = (data) => JSON.parse(JSON.stringify(data));

export class Game {
  constructor(content) {
    Object.assign(this, content);        // sceneIds, loadScene, cutscenes, lines, cast, eras, items, story, sound
    this.scenes = {};                    // scene files already fetched
    this.art = art;
    this.assets = { url, picture };      // for a script that puts a painted picture on the live layer: g.assets.url("art/..."), g.assets.picture("art/...")
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
    this.outlines = new Outlines(this);   // what Show draws (outline.js)
    this.life = new Life(this);           // the scene's people living their own lives: small movements, and a walk now and then (life.js)
    this.effects = new Effects(this);     // the things in a scene that move by nature: smoke, flames, water, birds, cloth (effects.js)
    this.names = {};                      // each scene's name, by its id, once its file is in (for the label over a way out)

    this.mode = "boot";      // boot, cutscene, title or play
    this.busy = 0;           // above zero while a script has control
    this.scene = null;
    this.held = null;        // the inventory item in the player's hand
    this.lookMode = false;
    this._fade = 0;
    this._nope = 0;
    this._chats = {};        // how many times each pair has talked, so they do not repeat themselves at once

    this.store.on(() => { this.ui.refresh(); this.follow(); });
  }

  get mode() { return this._mode; }
  set mode(value) { this._mode = value; document.body.dataset.mode = value; if (this.outlines) this.outlines.changed(); }   // lets the style sheet react to it (and Show draws only in play)

  // =============== start-up ===============
  async boot() {
    try { await this.start(); }
    catch (err) { console.error("The game stopped while starting:", err); this.ui.fatal("The game could not start. Press Reload."); }
  }

  async start() {
    this.clock.start();
    this.clock.every((dt) => { if (this.mode === "play") this.store.data.playMs += dt; });
    this.clock.every((dt) => this.view.cast.update(dt));                 // animate and repaint the people and props
    this.bindInput();
    const known = Object.fromEntries(this.sceneIds.map((id) => [id, true]));
    for (const problem of checkStory({ story: this.story, scenes: known, cutscenes: this.cutscenes, lines: this.lines })) console.warn("Story check:", problem);
    try { await document.fonts.load('16px "Koine Road"'); } catch { /* the fallback font will do */ }
    // Fetch every scene file now, while the start-up panel is showing. After this the game asks the
    // server for no more code, so a new version published in the middle of a session cannot get mixed
    // into this one. (A scene that will not load now is tried again when the player gets there.)
    await Promise.all(this.sceneIds.map((id) => this.getScene(id).catch(() => { delete this.scenes[id]; })));
    const loaded = {};
    for (const id of this.sceneIds) if (this.scenes[id]) loaded[id] = await this.scenes[id];
    for (const problem of checkEdges(loaded)) console.warn("Edge check:", problem);
    // No pictures yet. The title fetches its own; the rest are fetched behind it, once it is up (see gather),
    // and a scene that is entered before its turn has come fetches its own first (see enterScene).

    const params = new URLSearchParams(location.search);
    await this.ui.gate(() => this.audio.unlock());

    // Shortcuts for building scenes:  index.html?scene=rome-street&lead=son
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
    // What is behind the title belongs to the story, not to the engine: the cutscene called "title"
    // dresses the stage (js/content/cutscenes/title.js), and returns when its pictures are in.
    if (this.cutscenes.title) await this.cutscenes.title(this);
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
    this.gather();
  }

  /**
   * Fetch every picture in the game, quietly, so that before long this session holds all of it (assets.js) and
   * plays on from what it holds: a version published in the middle of somebody's game cannot then hand them new
   * pictures to go with their old code. It starts once the title is up (or, for a game opened straight into a
   * scene, once that scene is), so it takes nothing from the start. One file at a time, each asked for when the
   * page has a moment to spare, and only fetched, not decoded, so play does not feel it. Nothing waits for it: a
   * scene entered before its turn has come fetches its own pictures first, as it always did.
   * What the player is likeliest to want comes first: the inventory icons, the scene the autosave is in, the scene
   * a new game opens on. Then every scene in order. Calling it again does nothing more; it answers with the same promise.
   */
  gather() {
    if (this.gathering) return this.gathering;
    const spare = () => new Promise((go) => { if (window.requestIdleCallback) requestIdleCallback(() => go(), { timeout: 1500 }); else setTimeout(go, 120); });
    const auto = saves.readSlot("auto");
    const order = new Set([auto && auto.data.scene, this.story.start.scene, ...this.sceneIds].filter((id) => this.sceneIds.includes(id)));
    this.gathering = (async () => {
      const files = Object.values(this.items).map(iconPath).filter(Boolean);
      for (const id of order) {
        try { files.push(...picturesIn(await this.getScene(id))); } catch { /* a scene file that will not load: its pictures are fetched if the player gets there */ }
      }
      for (const path of new Set(files)) { await spare(); await hold(path, { quiet: true }); }
    })();
    return this.gathering;
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
    if (!this.clock.skipping) this.ui.toast(`You have ${this.the(item)}`);
  }
  /** A thing's name as it goes into a sentence: "the reed", but "General Feathers". A name is used as it is when the item
      says `proper: true`, or when the name begins with a capital ("Dad's pencil"); `proper: false` puts "the" back. */
  the(id) {
    const it = this.item(id), name = it.name;
    return (it.proper ?? /^[A-Z]/.test(name)) ? name : "the " + name;
  }
  /** What is known about a thing that can be carried (its entry in `items`). A thing that is not there, through a slip
      in a script or a save from another version, gets its own id for a name and a note in the console, and the game carries on. */
  item(id) {
    if (this.items[id]) return this.items[id];
    this._strays = this._strays || {};
    if (!this._strays[id]) { console.warn(`No item called "${id}" in js/content/world.js.`); this._strays[id] = { name: id }; }
    return this._strays[id];
  }
  /** Who is carrying a thing: a lead's id, or null. */
  holder(item) { return this.store.holder(item); }
  /** Say which leads the player can switch between from now on. */
  team(list) { this.store.data.team = list.filter((id) => this.leads.includes(id)); this.store.emit(); }
  music(id) { this.audio.music(id); }
  /** The track a scene plays: its own `music` (a track id, or a function of the game that returns one, so that the
      story can change it), or else its era's. A script that has just changed the story calls g.music(g.musicOf(g.scene)). */
  musicOf(scene) { const m = typeof scene.music === "function" ? scene.music(this) : scene.music; return m || this.eras[scene.era].music; }
  sfx(id) { if (!this.clock.skipping) this.audio.sfx(id); }
  actor(id) { return this.view.cast.get(id); }
  /** One of the scene's painted cut-outs, by the id it has under `planes`: .show(bool), .set(state), .fade(opacity), .place(x, y, scale).
      What a script shows or sets by hand holds until the scene is built again; left alone, a cut-out follows its `when` and `state`. */
  plane(id) { const s = this.view.cast.get(id); return s instanceof Cutout ? s : null; }
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

  /** A close look at something small: a screen, a notice, a note. Pass a drawing to show it, and nothing to put
      it away. The kit's close-ups are drawn on a 320x200 grid, which is what is expected; for a drawing made at
      another size say so: g.closeup(markup, label, { grid: [800, 600] }). It is shown in the middle of the stage,
      as large as will fit, over a veil that covers the whole scene. People carry on talking underneath it. */
  closeup(markup = null, label = "", { grid = OLD } = {}) {
    const el = this.closeEl;
    if (!el) return;
    // (the layer is an SVG element, which has no `hidden` property of its own: the attribute is what counts)
    if (!markup || this.clock.skipping) { el.setAttribute("hidden", ""); el.innerHTML = ""; return; }
    el.innerHTML = `<rect class="veil" width="${W}" height="${H}"/>${fit(markup, grid)}`;
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
    if (!this.scenes[id]) this.scenes[id] = this.loadScene(id).then((scene) => { this.names[id] = scene.name; return scene; });      // keep the promise, so two askers share one fetch
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
        if (from) this.music(this.musicOf(from));
        await this.fade(0, 300);
        this.ui.hud(this.mode === "play");
        this.ui.toast("That part of the game would not load. Check your connection and try again.", 4500);
        return;
      }
      const marks = scene.spawn || {};         // a named way in, then this lead's own mark, then the usual one
      try {
        await this.enterScene(scene, at || (spawn !== "default" && marks[spawn]) || marks[this.store.data.active] || marks.default, spawn);
      } catch (err) {                              // the scene broke while it was being built: never leave the player looking at black
        this.stopTunnel();
        return await this.trouble(err, `Scene "${id}"`);
      }
      await this.fade(0, via === "wormhole" ? 700 : 400, via === "wormhole" ? "#fff" : "#000");
      if (!from || from.era !== scene.era) {
        const era = this.eras[scene.era];
        await this.card(era.name, era.date);
      }
      if (scene.enter) await scene.enter(this, from ? from.id : null);
    } finally {
      this.busy--;
      this.tidy();
      this.ui.refresh();
    }
    this.autosave();
  }

  /** Build a scene on the stage from the saved state. No story happens here.
      It returns once every picture the scene can show has arrived, so the caller can fade in on a finished stage. */
  async enterScene(scene, pos, way = "default") {
    const d = this.store.data, cast = this.view.cast;
    this.dialogue.clear();
    this.closeup();
    this.held = null;
    this.lookMode = false;
    this._leaving = null;
    this.view.clear();
    // The paints (js/art/look.js): the people and the moving things take this scene's key. The team's portraits are the
    // interface's and are drawn with none (portrait() in cast.js sees to that itself, and keeps each one); pictures of
    // people kept from another key are let go.
    if (keyScene(scene.id, scene.era) && castKit.forget) castKit.forget();
    this.scene = scene;
    this.life.enter(scene);                     // everyone's own life starts again with the scene, on their marks (life.js)
    this.mode = "play";
    this.titleEl.hidden = true;
    this.view.setEra(scene.era);
    // The backdrop, the light that stays smooth, and the painted cut-outs (`planes`), each of which reads the story
    // to see whether it shows and in which state. A scene with no painting gets its kit drawing, or a sketch.
    // Then the things in it that move by nature (`fx`: smoke, flames, water, birds, cloth), each at its depth (effects.js).
    const shown = Promise.all([this.view.show(scene, this), this.effects.enter(scene)]);

    // Props and people who are not the lead. Each can block the ground it stands on.
    const blocked = [...(scene.blocked || [])];
    for (const p of scene.props || []) {
      if (p.when && !p.when(this)) continue;
      const thing = cast.addThing(p.id, p.kind, p.at[0], p.at[1], p.scale ?? 1, p.options);
      thing.plane = p.plane || "floor";
      thing.base = p.base ?? null;
      if (p.solid) blocked.push(p.solid);
    }
    for (const a of scene.actors || []) {
      if (a.when && !a.when(this)) continue;
      const s = a.scale ?? scaleAt(scene, a.at[1]);
      cast.addFigure(a.id, a.kind || a.id, a.at[0], a.at[1], s).face(a.face ?? "S");
    }
    this.blocked = blocked;                     // (remap adds the ground under each cut-out and each person, because those come, go and move with the story)
    this.remap(true);                           // where the lead may stand, and how to get around things

    const marks = scene.spawn || {};            // with no place given: this lead's own mark, then the usual one
    const want = pos || marks[d.active] || marks.default || [W / 2, 560];
    const [x, y] = this.map.nearest(want[0], want[1]);
    const was = d.where[d.active], facing = was && was.scene === scene.id && was.face != null && pos ? was.face : scene.facing || "S";
    cast.addFigure(d.active, this.cast[d.active].sprite, x, y, scaleAt(scene, y)).face(facing);
    d.scene = scene.id;
    d.where[d.active] = { scene: scene.id, x: Math.round(x), y: Math.round(y), face: this.lead.yaw };

    // A scene can name a party: leads who are here together. They arrive with whoever is leading,
    // each on their own mark, and the player can switch between them. When they come in by a named way
    // (g.goto(id, { spawn: "fromStairs" })), the scene can say where the ones who are NOT leading end up:
    //     arrive: { fromStairs: [[x, y], [x, y]] }      (in the order of `party`, the lead left out)
    const markOf = (id, n) => marks[id] || [x + 55 * (n + 1), y];
    const party = (scene.party || []).filter((id) => this.leads.includes(id));
    if (party.includes(d.active)) {
      const beside = (scene.arrive && scene.arrive[way]) || [];
      let nth = 0;
      party.forEach((id, n) => {
        if (!d.team.includes(id)) d.team.push(id);
        const at = d.where[id];
        if (id === d.active || (at && at.scene === scene.id && at.x != null)) return;
        const mark = beside[nth++] || markOf(id, n);
        d.where[id] = { scene: scene.id, x: mark[0], y: mark[1] };
      });
    }
    // Anyone else on the team who is standing in this scene is on stage too.
    // (A save from before the picture changed size knows which scene they are in but not where: they go to their marks.)
    d.team.forEach((id, n) => {
      const at = d.where[id];
      if (id === d.active || !at || at.scene !== scene.id) return;
      const mark = at.x != null ? [at.x, at.y] : markOf(id, n);
      const [mx, my] = this.map.nearest(mark[0], mark[1]);
      cast.addFigure(id, this.cast[id].sprite, mx, my, scaleAt(scene, my)).face(at.face ?? (scene.facing || "S"));
    });
    if (scene.setup) scene.setup(this);          // anything the scene still does by hand to match the story facts
    this.rebuildSpots();
    this.music(this.musicOf(scene));
    this.ui.hud(true);
    this.ui.refresh();
    await shown;
    // Once this scene has everything it needs: fetch the pictures of the scenes that can be reached from it
    // (`exits`, and its ways out at the edges), so that walking on does not mean waiting for them.
    const next = new Set([...(scene.exits || []), ...Object.values(scene.edges || {}).map((way) => way && way.to)].filter((id) => this.sceneIds.includes(id)));
    for (const id of next) this.getScene(id).then((there) => this.view.warm(there)).catch(() => {});
    this.gather();                               // (already under way, unless the game was opened straight into a scene)
  }

  /** Work out where people may stand: the scene's walk outline, less the ground that props, people and painted
      cut-outs take up. A cut-out blocks its `solid` only while it is shown, so this is asked again whenever the
      story changes; the map is built again only when the answer would be different. */
  remap(anyway = false) {
    if (!this.scene) return;
    const { solid, people } = this.ground();
    const key = solid.map((c) => c.id).join("|") + "#" + people.map((p) => p.flat().map(Math.round).join(",")).join("|");
    if (!anyway && key === this._solid) return;
    this._solid = key;
    this.map = new WalkMap(this.scene, [...(this.blocked || []), ...solid.map((c) => c.spec.solid), ...people]);
  }

  /** The ground that things and people take up: the cut-outs that are showing ({ solid }), and the people who are not
      leads ({ people }: outlines). A person blocks their own `solid` while they are on their mark, and a patch under
      their feet wherever a script has walked them to since. One who is away on a walk of their own (life.js) has their
      place kept for them, and blocks a patch where they stand still, but nothing while they walk. `except`: leave out
      that person (for working out their own way about). */
  ground(except = null) {
    const cast = this.view.cast, scene = this.scene;
    const solid = cast.cutouts().filter((c) => c.spec.solid && !c.hidden);
    const patch = (x, y, s) => [[x - 32 * s, y - 12], [x + 32 * s, y - 12], [x + 32 * s, y + 8], [x - 32 * s, y + 8]];
    const people = [];
    for (const a of scene.actors || []) {
      const f = cast.get(a.id);
      if (a.id === except || !f || f.hidden || a.solid === false) continue;
      if (this.life.isAway(a.id)) {
        if (!a.when || a.when(this)) people.push(a.solid || patch(a.at[0], a.at[1], a.scale ?? scaleAt(scene, a.at[1])));
        if (!f.walking) people.push(patch(f.x, f.y, f.scale));
        continue;
      }
      const moved = Math.abs(f.x - a.at[0]) > 4 || Math.abs(f.y - a.at[1]) > 4;
      people.push(a.solid && !moved ? a.solid : patch(f.x, f.y, f.scale));
    }
    return { solid, people };
  }

  /** Where one of the scene's people may walk on a walk of their own (life.js): the ground as the lead has it, less
      their own place and with the family standing in it, so that they go round the family and not through them. */
  groundFor(id) {
    const { solid, people } = this.ground(id), d = this.store.data, family = [];
    for (const who of new Set([d.active, ...(d.team || [])])) {
      const f = this.actor(who);
      if (f && !f.hidden) family.push([[f.x - 20 * f.scale, f.y - 8], [f.x + 20 * f.scale, f.y - 8], [f.x + 20 * f.scale, f.y + 6], [f.x - 20 * f.scale, f.y + 6]]);
    }
    return new WalkMap(this.scene, [...(this.blocked || []), ...solid.map((c) => c.spec.solid), ...people, ...family]);
  }

  /** The story has changed, or a script has ended: the picture follows. Clickable areas and painted cut-outs
      read their `when` and `state` again, and the ground under a cut-out that has come or gone is blocked or freed. */
  follow() {
    this.view.refresh(this);
    this.remap();
    this.outlines.changed();                    // (while Show is on, it draws again if what it shows has changed)
  }

  /** Run a piece of script with the controls locked. First, anyone of the scene's people who is away on a walk of their
      own goes home (life.js), so that every script finds everyone on their mark; `{ settle: false }` for a script that
      only has the lead say something (a hint), during which they simply stand where they are until it is over. */
  async run(script, { settle = true } = {}) {
    this.busy++;
    this.ui.refresh();
    try { if (settle) await this.life.settle(); await script(); }
    catch (err) {
      console.error("Script stopped:", err);
      this.ui.toast("Something went wrong there. If it keeps happening, reload the page.", 5000);
      if (this._fade > 0.5 && this.mode === "play") await this.fade(0, 300);       // it stopped half-way through a fade
    }
    finally { this.busy--; this.closeup(); this.tidy(); this.ui.refresh(); }
  }

  /** Something broke that should not have. Say so on the screen and go back to the title, which rebuilds
      everything. If even that fails, put the start-up panel back with a Reload button. Never a black screen. */
  async trouble(err, what = "The game") {
    console.error(`${what} stopped:`, err);
    try {
      await this.title();
      this.ui.toast("Something went wrong there. Your last save is safe.", 6000);
    } catch (worse) {
      console.error(worse);
      this.ui.fatal("Something went wrong and the game had to stop. Your last save is safe.");
    }
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
  /** The clickable areas: the scene's own, and one over each companion standing here. A person's own area (the one with
      their id, or that says `actor: "<id>"`) is a copy that remembers the scene's shape (`home`), so that it can go with
      them on a walk of their own and come back to that shape when they do (life.js). */
  rebuildSpots() {
    const scene = this.scene, d = this.store.data;
    if (!scene) return;
    const people = new Set((scene.actors || []).map((a) => a.id));
    const spots = (scene.hotspots || []).map((h) => (people.has(h.actor || h.id) ? { ...h, home: h } : h));
    for (const id of d.team) {
      const a = id === d.active ? null : this.actor(id);
      if (!a) continue;
      const w = 50 * a.scale, h = a.h * a.scale;
      spots.push({ id: "mate." + id, name: this.cast[id].name, verb: "Talk to", mate: id, rect: [a.x - w / 2, a.y - h, w, h] });
    }
    this.view.setHotspots(spots);
    this.life.follow();                         // (someone away has theirs round them at once)
    this.follow();
    this.ui.edge = null;                        // (until the pointer moves again)
    this.ui.hover(null);
  }

  /** After a script has moved people about: note where everyone on the team is standing, and move their clickable areas. */
  tidy() {
    if (!this.scene || this.mode !== "play") return;
    for (const id of this.store.data.team) this.rememberPlace(id);
    this.rebuildSpots();
  }

  /** Everyone back on their marks: anyone of the scene's people who is away on a walk of their own (or up from their
      seat) goes home, briskly, and sits down again if they sit (life.js); then, as after any script, the team's places
      are noted and the clickable areas follow. Resolves when they are home (after about two seconds at most, they are
      put there). Every script gets this before it starts; a script can also ask for it: `await g.settle()`, or for one
      person, `await g.settle("scribe")`. */
  settle(who = null) {
    const home = this.life.settle(who);
    this.tidy();
    return home;
  }

  /** A place to stand that no companion is already standing on: the place asked for, or a step to one side of it. */
  clearOf(at) {
    if (!at) return at;
    const d = this.store.data, others = d.team.filter((id) => id !== d.active).map((id) => this.actor(id)).filter(Boolean);
    const taken = (x, y) => others.some((a) => Math.abs(a.x - x) < 38 && Math.abs(a.y - y) < 15);
    for (const dy of [5, 18, -12])
      for (const dx of [0, 42, -42, 84, -84, 126, -126]) {
        const x = at[0] + dx, y = at[1] + (dx ? dy : 0);
        if (!taken(x, y) && (dx === 0 || this.map.ok(x, y))) return [x, y];
      }
    return at;
  }

  /** A place to stand for a word with a companion: beside them, on the side the lead is coming from. */
  beside(mate) {
    const lead = this.lead, reach = 55 * mate.scale;
    if (Math.abs(lead.x - mate.x) <= reach + 15 && Math.abs(lead.y - mate.y) <= 12) return null;    // near enough already
    // the side the lead is coming from, unless someone else is standing there: then the other side, then a step nearer or farther
    const d = this.store.data, others = d.team.filter((id) => id !== d.active && id !== mate.id).map((id) => this.actor(id)).filter(Boolean);
    const free = (x, y) => this.map.ok(x, y) && !others.some((a) => Math.abs(a.x - x) < 38 && Math.abs(a.y - y) < 15);
    const side = lead.x <= mate.x ? -1 : 1;
    for (const k of [1, 1.4, 1.8])                     // (a step farther off, if there is no room close by)
      for (const [sd, dy] of [[side, 2], [-side, 2], [side, 24], [-side, 24], [side, -20], [-side, -20]]) {
        const x = mate.x + sd * reach * k, y = mate.y + dy;
        if (free(x, y)) return [x, y];
      }
    return null;                                       // no room beside them: a word from where the lead stands, never on top of someone
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
    if (!this.clock.skipping) this.ui.toast(`${this.cast[to].name} has ${this.the(item)}`);
    if (this.scene.given) await this.scene.given(this, item, to, from);
  }

  async interact(spot, verb = "use") {
    if (this.busy || this.mode !== "play") return;
    this._leaving = null;                          // (if he was on his way out by an edge, he is not now)
    // A person's own area may have gone with them on a walk of their own (life.js). Nobody is talked to away from home:
    // they go back to their place while the lead walks over to it, as the scene has it, and the script starts once both are there.
    spot = spot.home || spot;
    await this.run(async () => {
      const homing = this.life.settle();
      const lead = this.lead, scene = this.scene, mate = spot.mate ? this.actor(spot.mate) : null;
      const stand = mate ? this.beside(mate) : this.clearOf(spot.walkTo);
      if (stand) await lead.walkPath(this.clock, this.map.path([lead.x, lead.y], stand), (yy) => scaleAt(scene, yy));
      await homing;
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
    }, { settle: false });
    this.autosave();
  }

  walk(x, y) {
    const lead = this.lead, scene = this.scene;
    if (!lead || !scene || this.busy) return;
    this._leaving = null;
    lead.walkPath(this.clock, this.map.path([lead.x, lead.y], [x, y]), (yy) => scaleAt(scene, yy)).then(() => this.rememberPlace());
  }

  // =============== ways out at the edges of the picture (edges.js) ===============
  /** The side ("N", "S", "W", "E") of the way out whose band holds this point of the picture, or null. A clickable area
      there still wins over the band: this answers only for the floor. */
  edgeAt(x, y) { return this.mode === "play" ? edgeAt(this.scene, this, x, y) : null; }
  /** The side the lead is on his way out by (after a click in its band, before the scene changes), or null. */
  get leaving() { return this._leaving ? this._leaving.side : null; }
  /** Is there a way out at this side of the picture now? Its side if there is, or null. */
  edgeOpen(side) { return side && this.scene && this.scene.edges && open(this.scene.edges[side], this) ? side : null; }
  /** What the label line says over that way out: "Go up the track", "Go to the great gallery". */
  edgeLabel(side) {
    const way = this.scene && this.scene.edges && this.scene.edges[side];
    return way ? edgeLabel(way, this.names[way.to]) : "";
  }

  /**
   * Leave by the way out at one side of the picture, as a click at (x, y) in its band does: the lead walks toward that
   * edge (to the way's `walkTo`, or to the floor nearest (x, y) pushed as far toward the edge as it goes), and when he is
   * there, g.goto(to, { spawn }) (or the way's own `use`). It is an ordinary walk, not a script: a click anywhere else
   * on the way sends him there instead, and then nobody leaves. A double click hurries him, as on any walk.
   */
  leave(side, x = W / 2, y = H / 2) {
    const scene = this.scene, lead = this.lead, way = scene && scene.edges && scene.edges[side];
    if (!lead || !way || this.busy || this.mode !== "play" || !open(way, this)) return;
    const target = way.walkTo || this.map.toward(side, x, y) || [lead.x, lead.y];
    const route = this.map.path([lead.x, lead.y], target), end = route[route.length - 1];
    const trip = (this._leaving = { side, end });
    lead.walkPath(this.clock, route, (yy) => scaleAt(scene, yy)).then(async () => {
      this.rememberPlace();
      if (this._leaving !== trip) return;                   // he was sent somewhere else on the way
      this._leaving = null;
      if (this.scene !== scene || this.lead !== lead || this.busy || this.mode !== "play") return;
      if (Math.hypot(lead.x - end[0], lead.y - end[1]) > 1.5) return;
      await this.run(async () => { if (way.use) await way.use(this); else await this.goto(way.to, { spawn: way.spawn }); }, { settle: !!way.use });     // (nobody need go home for a scene that is being left)
      this.autosave();
    });
  }

  /** For test scripts: a point of the picture inside the band of that way out where a real click lands on the floor
      (not on a clickable area, or a button lying over it), nearest the middle of the edge; or null if there is none. */
  edgePoint(side) {
    if (!this.edgeOpen(side)) return null;
    const box = this.stage.getBoundingClientRect(), depth = BANDS[side], across = side === "N" || side === "S";
    const rows = [depth / 2, depth / 4, (depth * 3) / 4, 4, depth - 4];       // how far in from the edge
    for (let k = 0; k <= (across ? W : H) / 2; k += 8) {
      for (const along of k ? [(across ? W : H) / 2 - k, (across ? W : H) / 2 + k] : [(across ? W : H) / 2]) {
        for (const d of rows) {
          const x = across ? along : side === "W" ? d : W - d, y = !across ? along : side === "N" ? d : H - d;
          const el = document.elementFromPoint(box.left + (x / W) * box.width, box.top + (y / H) * box.height);
          if (el && el.classList && el.classList.contains("floor") && this.edgeAt(x, y) === side) return [x, y];
        }
      }
    }
    return null;
  }

  /** Show what can be clicked (the Show button, holding H): reveal(true) until reveal(false), or reveal(true, ms) for a while.
      It is the class "reveal" on #hot that does it: the outlines follow it (outline.js). */
  reveal(on = true, ms = 0) {
    clearTimeout(this._revealing);
    this.view.hotEl.classList.toggle("reveal", !!on);
    if (on && ms) this._revealing = setTimeout(() => this.view.hotEl.classList.remove("reveal"), ms);
    this.outlines.changed();
  }

  async useItem(item) {
    if (this.busy) return;
    if (this.lookMode) {
      this.lookMode = false;
      return this.run(() => this.act(this.item(item).look), { settle: false });      // (only the lead speaks: anyone away stands still till it is said)
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
    if (line) await this.run(() => this.say(line), { settle: false });
  }

  /** Change which lead the player controls. Each lead keeps their own place and pockets. */
  async switchLead(to) {
    const d = this.store.data;
    if (this.busy || this.mode !== "play" || d.active === to || !d.team.includes(to)) return;
    this._leaving = null;
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
      this.tidy();
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
    // Anyone else who was left in a scene this version does not have is nowhere, until the story puts them somewhere.
    // And a thing in somebody's pockets that this version does not have is left behind.
    for (const id of this.leads) {
      if (data.where[id] && !this.sceneIds.includes(data.where[id].scene)) data.where[id] = null;
      const lost = data.inventory[id].filter((item) => !this.items[item]);
      if (lost.length) { console.warn(`This save has things the game does not know (${lost.join(", ")}). They were left out.`); data.inventory[id] = data.inventory[id].filter((item) => this.items[item]); }
    }
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
    } catch (err) {                                     // a save that will not open must not leave a black screen
      await this.trouble(err, "Loading a save");
    } finally {
      this.busy--;
      this.tidy();
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
      const verb = this.lookMode ? "look" : "use", looking = this.lookMode;
      this.lookMode = false;
      if (spot) this.interact(spot, verb);
      else if (this.held) { this.held = null; this.ui.refresh(); }
      else {
        const [x, y] = this.view.toPicture(event), side = this.edgeAt(x, y);
        this.ui.refresh();
        if (side && looking) return;                    // in the band of a way out: nobody leaves by looking
        if (side) this.leave(side, x, y);               // walk off the edge of the picture
        else this.walk(x, y);
      }
    });
    // A double click hurries whoever is walking, so a long way across a scene never has to be sat through.
    hot.addEventListener("dblclick", () => { const lead = this.lead; if (lead && lead.walking) lead.hurry = true; });
    hot.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      const spot = spotOf(event);
      if (spot) this.interact(spot, "look");
      else if (this.held) { this.held = null; this.ui.refresh(); }
    });
    hot.addEventListener("pointerover", (event) => this.ui.hover(spotOf(event)));
    hot.addEventListener("pointerleave", () => { this.ui.edge = null; this.ui.hover(null); });
    // Over the floor in the band of a way out, the pointer is an arrow and the label says where the way leads (ui.js).
    hot.addEventListener("pointermove", (event) => {
      const side = spotOf(event) ? null : this.edgeAt(...this.view.toPicture(event));
      if (side !== this.ui.edge) { this.ui.edge = side; this.ui.label(); }
    });
    // Keyboard focus (Tab) outlines the one area it is on, the way Show outlines them all.
    const visible = (el) => { try { return el.matches(":focus-visible"); } catch { return true; } };
    hot.addEventListener("focusin", (event) => { const spot = spotOf(event); this.ui.hover(spot); this.outlines.focus(spot && visible(event.target) ? spot : null); });
    hot.addEventListener("focusout", () => { this.ui.hover(null); this.outlines.focus(null); });
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
        if (!event.repeat) this.reveal(true);          // held down: Show stays on until it is let go
      }
    });
    document.addEventListener("keyup", (event) => { if (event.key.toLowerCase() === "h") this.reveal(false); });

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
