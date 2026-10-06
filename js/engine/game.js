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
//
// Scripts are ordinary async functions. They read top to bottom like a screenplay.

import { Clock, ease } from "./clock.js";
import { Store, newGame } from "./state.js";
import * as saves from "./save.js";
import { AudioEngine } from "./audio.js";
import { Dialogue } from "./dialogue.js";
import { SceneView, clampToWalk, scaleAt } from "./scene.js";
import { UI } from "./ui.js";
import { tunnel } from "./fx.js";
import { openBeats, checkStory } from "./story.js";
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
    this.systemCalm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    this.clock = new Clock();
    this.store = new Store();
    this.settings = saves.loadSettings();
    this.applyCalm();
    this.audio = new AudioEngine(this.settings, content.sound);
    this.view = new SceneView(this.stage);
    this.dialogue = new Dialogue(this);
    this.ui = new UI(this);

    this.mode = "boot";      // boot, cutscene, title or play
    this.busy = 0;           // above zero while a script has control
    this.scene = null;
    this.held = null;        // the inventory item in the player's hand
    this.lookMode = false;
    this._fade = 0;
    this._nope = 0;

    this.store.on(() => { this.ui.refresh(); this.view.refreshHotspots(this); });
  }

  get mode() { return this._mode; }
  set mode(value) { this._mode = value; document.body.dataset.mode = value; }   // lets the style sheet react to it

  // =============== start-up ===============
  async boot() {
    this.clock.start();
    this.clock.every((dt) => { if (this.mode === "play") this.store.data.playMs += dt; });
    this.bindInput();
    const known = Object.fromEntries(this.sceneIds.map((id) => [id, true]));
    for (const problem of checkStory({ story: this.story, scenes: known, cutscenes: this.cutscenes, lines: this.lines })) console.warn("Story check:", problem);
    try { await document.fonts.load('16px "Koine Road"'); } catch { /* the fallback font will do */ }

    const params = new URLSearchParams(location.search);
    await this.ui.gate(() => this.audio.unlock());

    // Shortcut for building scenes: index.html?scene=rome-forum&lead=son
    const jump = params.get("scene");
    if (jump && this.sceneIds.includes(jump)) {
      this.store.reset(this.freshState());
      if (this.cast[params.get("lead")]) this.store.data.active = params.get("lead");
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
    this.ui.close();
    this.ui.hud(false);
    this.view.clear();
    this.view.setEra("present");
    this.view.draw(art.frame(art.highway(), "Dusk on a desert highway. A family station wagon heads for a swirling time portal, past a road sign where Point B has been crossed out and B.C. painted in."));
    this.view.addActor("wagon", "wagon", 184, 182).flag("bounce", true);
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
    const data = newGame();
    data.active = this.story.start.lead;
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
  music(id) { this.audio.music(id); }
  sfx(id) { if (!this.clock.skipping) this.audio.sfx(id); }
  actor(id) { return this.view.actors.get(id); }
  get lead() { return this.view.actors.get(this.store.data.active); }
  q(selector) { return this.view.q(selector); }

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
      this.enterScene(scene, at || (scene.spawn && (scene.spawn[spawn] || scene.spawn.default)));
      await this.fade(0, via === "wormhole" ? 700 : 400, via === "wormhole" ? "#fff" : "#000");
      if (!from || from.era !== scene.era) {
        const era = this.eras[scene.era];
        await this.card(era.name, era.date);
      }
      if (scene.enter) await scene.enter(this, from ? from.id : null);
    } finally {
      this.busy--;
      this.ui.refresh();
    }
    this.autosave();
  }

  /** Build a scene on the stage from the saved state. No story happens here. */
  enterScene(scene, pos) {
    const d = this.store.data;
    this.dialogue.clear();
    this.held = null;
    this.lookMode = false;
    this.view.clear();
    this.scene = scene;
    this.mode = "play";
    this.titleEl.hidden = true;
    this.view.setEra(scene.era);
    this.view.draw(art.frame(scene.draw ? scene.draw(art, this) : art.sketch(scene), scene.name));   // no drawing yet? sketch it
    for (const a of scene.actors || []) {
      if (a.when && !a.when(this)) continue;
      this.view.addActor(a.id, a.sprite, a.at[0], a.at[1], a.scale ?? scaleAt(scene, a.at[1])).face(a.face || 1);
    }
    const [x, y] = pos || [160, scene.walk.y[1]];
    this.view.addActor(d.active, this.cast[d.active].sprite, x, y, scaleAt(scene, y));
    this.view.setHotspots(scene.hotspots || []);
    d.scene = scene.id;
    d.where[d.active] = { scene: scene.id, x, y };
    if (scene.setup) scene.setup(this);          // match the drawing to the story facts
    this.view.refreshHotspots(this);
    this.music(scene.music || this.eras[scene.era].music);
    this.ui.hud(true);
    this.ui.refresh();
    for (const next of scene.exits || []) this.getScene(next).catch(() => {});   // warm up the places you can go from here
  }

  /** Run a piece of script with the controls locked. */
  async run(script) {
    this.busy++;
    this.ui.refresh();
    try { await script(); }
    catch (err) { console.error("Script stopped:", err); }
    finally { this.busy--; this.ui.refresh(); }
  }

  /** An action can be a line ID, a list of line IDs, { dad: ..., son: ... } or a function. */
  async act(action) {
    if (action == null) return false;
    if (typeof action === "function") { await action(this); return true; }
    if (typeof action === "string") { await this.say(action); return true; }
    if (Array.isArray(action)) { await this.say(...action); return true; }
    return this.act(action[this.store.data.active] ?? action.any);
  }

  /** A stock reply for things nobody wrote a line for. */
  fallback(kind) {
    const list = this.story.fallbacks[kind][this.store.data.active];
    return list[this._nope++ % list.length];
  }

  async interact(spot, verb = "use") {
    if (this.busy || this.mode !== "play") return;
    await this.run(async () => {
      const lead = this.lead, scene = this.scene;
      if (spot.walkTo) {
        const [x, y] = clampToWalk(scene.walk, ...spot.walkTo);
        await lead.walkTo(this.clock, x, y, (yy) => scaleAt(scene, yy));
      }
      const cx = spot.rect ? spot.rect[0] + spot.rect[2] / 2 : spot.circle ? spot.circle[0] : spot.poly[0][0];
      lead.face(spot.face || (cx < lead.x ? -1 : 1));
      this.rememberPlace();
      const item = this.held;
      if (item) {
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
    const [tx, ty] = clampToWalk(scene.walk, x, y);
    lead.walkTo(this.clock, tx, ty, (yy) => scaleAt(scene, yy)).then(() => this.rememberPlace());
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
    const who = this.store.data.active;
    const beat = openBeats(this.story, this.store.data.flags).find((b) => b.hint && (b.lead === who || b.lead === "both"));
    await this.run(() => this.say(beat ? beat.hint : this.fallback("hint")));
  }

  /** Change which lead the player controls. Each lead keeps their own place and pockets. */
  async switchLead(to) {
    const d = this.store.data;
    if (this.busy || d.active === to || !this.cast[to]) return;
    this.rememberPlace();
    const place = d.where[to];
    if (!place || !place.scene) return;
    d.active = to;
    await this.goto(place.scene, { at: place.x != null ? [place.x, place.y] : null });
  }

  // =============== saving ===============
  rememberPlace() {
    const d = this.store.data, a = this.lead;
    if (a && this.scene) d.where[d.active] = { scene: this.scene.id, x: Math.round(a.x), y: Math.round(a.y) };
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
    const data = copy(body.data);
    if (!this.sceneIds.includes(data.scene)) { this.ui.toast("That save is from a part of the game this version does not have.", 4200); return; }
    this.ui.close();
    this.busy++;
    try {
      const loading = this.getScene(data.scene);
      await this.fade(1, 300);
      const scene = await loading;
      this.store.reset(data);
      const place = data.where[data.active] || {};
      this.enterScene(scene, place.x != null ? [place.x, place.y] : null);
      await this.fade(0, 400);
      this.ui.toast("Game loaded");
      if (scene.enter) await scene.enter(this, null);   // finish an arrival the save interrupted
    } finally {
      this.busy--;
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
      } else if (this.dialogue.choosing && key >= "1" && key <= "9") {
        const option = this.stage.querySelectorAll(".choices button")[Number(key) - 1];
        if (option) option.click();
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
