// The interface: the heads-up display during play, and the menus.
// All of it is ordinary HTML buttons on papyrus, so it works with a mouse, a finger,
// the keyboard and a screen reader, and it looks the same in every era.

import * as saves from "./save.js";
import { icon } from "../art/kit.js";
import { portrait } from "./cast.js";

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const minutes = (ms) => { const m = Math.round((ms || 0) / 60000); return m < 1 ? "under a minute" : m === 1 ? "1 minute" : `${m} minutes`; };
const when = (iso) => { try { return new Date(iso).toLocaleString(undefined, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }); } catch { return ""; } };

export class UI {
  constructor(game) {
    const g = (this.g = game);
    const q = (s) => g.stage.querySelector(s);
    this.hudEl = q("#hud"); this.menuEl = q("#menu"); this.skipEl = q("#skip");
    this.toastEl = q("#toast"); this.gateEl = q("#gate");
    this.open = null;
    this.hovered = null;
    this.over = null;          // the team portrait the pointer is on
    this.faces = {};           // portraits, drawn once

    this.hudEl.innerHTML = `
      <p class="place" id="place"></p>
      <div class="team" id="team" role="group" aria-label="Who you are playing"></div>
      <div class="tools" id="tools">
        <button class="tool" id="t-look" type="button" aria-pressed="false" title="Look at something. Right-click does the same.">Look</button>
        <button class="tool" id="t-show" type="button" title="Show what can be clicked. Holding H does the same.">Show</button>
        <button class="tool" id="t-hint" type="button" title="Ask for a hint">Hint</button>
        <button class="tool" id="t-menu" type="button" title="Menu (Esc)">Menu</button>
      </div>
      <p class="label" id="label"></p>
      <div class="inv" id="inv" aria-label="Inventory"></div>`;
    this.placeEl = q("#place"); this.toolsEl = q("#tools"); this.labelEl = q("#label"); this.invEl = q("#inv");
    this.teamEl = q("#team"); this.lookEl = q("#t-look");

    this.lookEl.addEventListener("click", () => { g.lookMode = !g.lookMode; this.refresh(); });
    q("#t-hint").addEventListener("click", () => g.hint());
    q("#t-show").addEventListener("click", () => {
      const hot = g.view.hotEl;
      hot.classList.add("reveal");
      clearTimeout(this._reveal);
      this._reveal = setTimeout(() => hot.classList.remove("reveal"), 2400);
    });
    q("#t-menu").addEventListener("click", () => this.pauseMenu());
    // The team: a portrait for each lead the player can switch to.
    const faceOf = (event) => { const b = event.target.closest ? event.target.closest("[data-lead]") : null; return b ? b.dataset.lead : null; };
    const point = (event) => { this.over = faceOf(event); this.label(); };
    const leave = () => { this.over = null; this.label(); };
    this.teamEl.addEventListener("click", (event) => { const to = faceOf(event); if (to) { if (event.detail && document.activeElement && document.activeElement.blur) document.activeElement.blur(); g.switchLead(to); } });
    this.teamEl.addEventListener("pointerover", point);
    this.teamEl.addEventListener("focusin", point);
    this.teamEl.addEventListener("pointerleave", leave);
    this.teamEl.addEventListener("focusout", leave);
    this.invEl.addEventListener("click", (event) => {
      const b = event.target.closest("[data-item]");
      if (b) g.useItem(b.dataset.item);
    });
    this.skipEl.addEventListener("click", () => g.skip());
    this.menuEl.addEventListener("click", (event) => this.onClick(event));
    this.menuEl.addEventListener("input", (event) => this.onInput(event));

    this.fileInput = Object.assign(document.createElement("input"), { type: "file", accept: ".json,application/json", hidden: true });
    document.body.appendChild(this.fileInput);
    this.fileInput.addEventListener("change", () => {
      const file = this.fileInput.files[0];
      this.fileInput.value = "";
      if (file) g.loadFile(file);
    });
  }

  /** The first screen. Its click is also what lets the browser play sound, so
      `onGesture` runs inside the click itself: Safari only accepts that. */
  gate(onGesture = () => {}) {
    return new Promise((resolve) => {
      const button = this.gateEl.querySelector("#begin");
      button.disabled = false;
      button.textContent = window.matchMedia("(pointer: coarse)").matches ? "Tap to begin" : "Click to begin";
      const go = () => { onGesture(); document.removeEventListener("keydown", onKey); this.gateEl.hidden = true; resolve(); };
      const onKey = (event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); go(); } };
      button.addEventListener("click", go, { once: true });
      document.addEventListener("keydown", onKey);
      button.focus({ preventScroll: true });
    });
  }

  // ---------- heads-up display ----------
  hud(on) { this.hudEl.hidden = !on; }
  showSkip(on) { this.skipEl.hidden = !on; }
  hover(spot) { this.hovered = spot; this.label(); }

  /** The leads the player can switch between right now, in order. */
  team() {
    const d = this.g.store.data;
    return d.team.filter((id) => d.where[id] && d.where[id].scene);
  }

  label() {
    const g = this.g;
    let text = "";
    if (g.mode === "play" && !g.busy) {
      const spot = this.hovered, name = spot ? spot.name : "";
      if (this.over) text = this.over === g.store.data.active ? `${g.cast[this.over].name} (playing now)` : `Play as ${g.cast[this.over].name}`;
      else if (g.held) text = spot && spot.mate ? `Give ${g.items[g.held].name} to ${name}` : `Use ${g.items[g.held].name} with ${name || "…"}`;
      else if (g.lookMode) text = `Look at ${name || "…"}`;
      else if (spot) text = `${spot.verb || (spot.use ? "Use" : "Look at")} ${name}`;
    }
    this.labelEl.textContent = text;
  }

  refresh() {
    const g = this.g, d = g.store.data;
    const free = g.mode === "play" && !g.busy && !g.dialogue.choosing;
    this.toolsEl.hidden = !free;
    this.invEl.hidden = !free;
    this.placeEl.textContent = g.scene && g.mode === "play" ? g.scene.name : "";
    this.lookEl.setAttribute("aria-pressed", String(g.lookMode));
    const team = this.team();
    this.teamEl.hidden = !free || team.length < 2;
    const now = team.join() + "|" + d.active;
    if (now !== this._team) {                       // rebuilt only when it changes, so a portrait under the pointer stays put
      this._team = now;
      this.teamEl.innerHTML = team.map((id, n) => {
        const name = esc(g.cast[id].name), on = id === d.active;
        if (!this.faces[id]) { const face = portrait(g.cast[id].sprite); this.faces[id] = face ? face.toDataURL() : ""; }
        return `<button class="tool face" type="button" data-lead="${esc(id)}" aria-pressed="${on}" style="--who:${esc(g.cast[id].color)}"` +
          ` aria-label="${on ? `${name}, playing now` : `Play as ${name}`}" title="${on ? `${name} (playing now)` : `Play as ${name} (key ${n + 1})`}">` +
          `<img src="${this.faces[id]}" alt="" draggable="false"></button>`;
      }).join("");
    }
    this.invEl.innerHTML = d.inventory[d.active].map((id) =>
      `<button class="tool item" type="button" data-item="${esc(id)}" aria-pressed="${g.held === id}">${icon(g.items[id].icon)}<span>${esc(g.items[id].name)}</span></button>`).join("");
    this.label();
  }

  toast(text, ms = 2600) {
    clearTimeout(this._toast);
    this.toastEl.textContent = text;
    this.toastEl.classList.add("show");
    this._toast = setTimeout(() => this.toastEl.classList.remove("show"), ms);
  }

  // ---------- menus ----------
  show(name, html, overTitle = false) {
    this.open = name;
    this.menuEl.className = "layer" + (overTitle ? " title-mode" : "");
    this.menuEl.innerHTML = html;
    this.menuEl.hidden = false;
    const pause = this.g.mode === "play";
    this.g.clock.paused = pause;                     // the world stops while a menu is up
    this.g.stage.classList.toggle("paused", pause);
    const first = this.menuEl.querySelector("button:not(:disabled)");
    if (first) first.focus({ preventScroll: true });
  }

  close() {
    this.open = null;
    this.menuEl.hidden = true;
    this.menuEl.innerHTML = "";
    this.g.clock.paused = false;
    this.g.stage.classList.remove("paused");
  }

  /** Esc or a Back button: one step up. */
  back() {
    if (this.g.mode === "title") return this.open === "title" ? null : this.titleMenu();
    if (this.open === "pause" || !this.open) return this.close();
    this.pauseMenu();
  }

  titleMenu() {
    const auto = saves.readSlot("auto");
    this.show("title", `<nav class="title-menu" aria-label="Main menu">
      ${auto ? `<button class="chip" type="button" data-act="continue" title="${esc((auto.meta || {}).era)}, as ${esc((auto.meta || {}).lead)}">Continue</button>` : ""}
      <button class="chip" type="button" data-act="new">New game</button>
      <button class="chip" type="button" data-act="load">Load game</button>
      <button class="chip" type="button" data-act="options">Options</button>
      <button class="chip" type="button" data-act="intro">Watch the intro</button>
    </nav>`, true);
  }

  /** Starting over replaces the autosave, so ask first. */
  confirmNew() {
    this.show("confirm", `<div class="panel" role="dialog" aria-label="Start a new game"><h2>Start over?</h2>
      <p>A new game replaces the autosave. Saves in slots 1 to 3 and save files are not touched.</p>
      <div class="foot"><button class="row" type="button" data-act="new-yes"><b>Start a new game</b></button>
      <button class="row" type="button" data-act="back"><b>Back</b></button></div></div>`);
  }

  /** Esc pauses at any moment. While a scene is playing out (someone is talking, the
      lead is walking somewhere) saving and loading wait, so a save can never catch
      the story half-way through a sentence. */
  pauseMenu() {
    if (this.g.mode !== "play") return;
    const off = this.g.busy ? " disabled" : "";
    this.show("pause", `<div class="panel" role="dialog" aria-label="Paused"><h2>Paused</h2><div class="rows">
      <button class="row" type="button" data-act="resume"><b>Back to the game</b></button>
      <button class="row" type="button" data-act="save"${off}><b>Save game</b></button>
      <button class="row" type="button" data-act="load"${off}><b>Load game</b></button>
      <button class="row" type="button" data-act="options"><b>Options</b></button>
      <button class="row" type="button" data-act="quit"${off}><b>Quit to the title screen</b></button>
    </div>${off ? "<p>Saving and loading are back as soon as this moment has played out.</p>" : ""}</div>`);
  }

  slotRow({ slot, save }, act) {
    const name = slot === "auto" ? "Autosave" : `Slot ${slot}`;
    const m = save ? save.meta || {} : null;
    const info = m ? `${esc(m.era)} &middot; ${esc(m.lead)}<br>${esc(when(save.savedAt))} &middot; ${esc(minutes(m.playMs))} played` : "Empty";
    return `<button class="row" type="button" data-act="${act}" data-slot="${slot}"${!save && act === "load-slot" ? " disabled" : ""}><b>${name}</b><small>${info}</small></button>`;
  }

  saveMenu() {
    const rows = saves.listSlots().filter((s) => s.slot !== "auto").map((s) => this.slotRow(s, "save-slot")).join("");
    this.show("save", `<div class="panel" role="dialog" aria-label="Save game"><h2>Save game</h2>
      <div class="rows">${rows}</div>
      <p>Slots are kept by this browser. A save file is yours to keep: load it on any computer or phone to carry on from the same spot.</p>
      <div class="foot"><button class="row" type="button" data-act="save-file"><b>Save to a file&hellip;</b></button>
      <button class="row" type="button" data-act="back"><b>Back</b></button></div></div>`);
  }

  loadMenu() {
    const rows = saves.listSlots().map((s) => this.slotRow(s, "load-slot")).join("");
    this.show("load", `<div class="panel" role="dialog" aria-label="Load game"><h2>Load game</h2>
      <div class="rows">${rows}</div>
      <p>You can also drop a save file anywhere on the game.</p>
      <div class="foot"><button class="row" type="button" data-act="load-file"><b>Load from a file&hellip;</b></button>
      <button class="row" type="button" data-act="back"><b>Back</b></button></div></div>`, this.g.mode === "title" ? false : false);
  }

  optionsMenu() {
    const s = this.g.settings;
    const slider = (key, label) => `<label>${label}<input type="range" min="0" max="1" step="0.05" value="${s[key]}" data-opt="${key}"></label>`;
    const check = (key, label) => `<label>${label}<input type="checkbox" data-opt="${key}"${s[key] ? " checked" : ""}></label>`;
    this.show("options", `<div class="panel" role="dialog" aria-label="Options"><h2>Options</h2>
      ${slider("music", "Music")}${slider("sfx", "Sound effects")}${slider("voice", "Voices")}
      ${check("subtitles", "Show the words on screen")}${check("voices", "Play recorded voices when there are any")}
      ${check("calm", "Less motion and no flashes")}
      <label>Text speed<select data-opt="textSpeed">
        ${[[0.6, "Slow"], [1, "Normal"], [1.6, "Fast"]].map(([v, n]) => `<option value="${v}"${Number(s.textSpeed) === v ? " selected" : ""}>${n}</option>`).join("")}
      </select></label>
      <p>Hold H during play to show everything you can click.</p>
      <div class="foot"><button class="row" type="button" data-act="back"><b>Back</b></button></div></div>`);
  }

  onInput(event) {
    const el = event.target.closest("[data-opt]");
    if (!el) return;
    const value = el.type === "checkbox" ? el.checked : Number(el.value);
    this.g.setOption(el.dataset.opt, value);
  }

  async onClick(event) {
    const b = event.target.closest("[data-act]");
    if (!b) return;
    const g = this.g, slot = b.dataset.slot;
    switch (b.dataset.act) {
      case "new": return saves.readSlot("auto") ? this.confirmNew() : g.newGame();
      case "new-yes": return g.newGame();
      case "continue": return g.load(saves.readSlot("auto"));
      case "intro": this.close(); await g.cutscene("intro"); return g.title();
      case "resume": return this.close();
      case "save": return this.saveMenu();
      case "load": return this.loadMenu();
      case "options": return this.optionsMenu();
      case "back": return this.back();
      case "quit": this.close(); await g.fade(1, 400); return g.title();
      case "save-slot": if (g.saveSlot(slot)) this.saveMenu(); return;
      case "save-file": return g.saveFile();
      case "load-slot": { const body = saves.readSlot(slot); if (body) return g.load(body); return; }
      case "load-file": return this.fileInput.click();
    }
  }
}
