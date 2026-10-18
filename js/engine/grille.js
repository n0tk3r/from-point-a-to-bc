// ENGINE-17: grilles. A clickable area of a scene can be a grille in a floor (or a ceiling) over another scene: the air
// ducts run over the Office's rooms, and from each grille the lead in the duct looks down into the room below. The game's
// `g.grilles`; docs/DESIGN.md, section 8, "Looking down through a grille".
//
//   { id: "grille-room", name: "grille", rect: [...], walkTo: [...],                    a hotspot of the scene up here
//     grille: { scene: "office-room", spawn: "vent", when: (g) => ..., no: "line.id", from: [x, y], view: "art/..." } }
//
// Its use is "Look down" (the label line says so): the lead walks to it as to anything, lies down at it (his `peek`
// frames, if he is painted and has them) and the scene below comes up as it is when it is played, its backdrop, cut-outs,
// people living their lives, moving things, scripts and words, but WITHOUT the lead (he is up here), and over it the
// grille's own picture (`view`, or art/scenes/<this scene>/grille-view.png: slats, clear between them; a stand-in drawn
// here until it is painted). Being in the view is being up here: the lead's place, the save, the map and g.where are the
// grille's, `g.here` is this scene, and nothing of the scene below assumes he is in it: its `setup` runs (as whenever it
// is built: g.peeking says it is a view), its `enter` does not (nobody has entered), and its `viewed(g, from)` does, if it
// has one: what it does when somebody looks in (two people talking, heard from the vent).
//
// From above, only the areas of the scene below that say what they do from above are there (`peek`, given per lead as
// everywhere: { look: { ranger: "..." }, use, useWith: { receipt: fn }, verb, drop }); an area with none is not
// clickable from above. A click anywhere else, the "Back up" button in the corner or Escape: back up, on the grille. The
// grille's other verb is the "Drop down" button (when the grille has a `spawn`): if its `when` allows (else its `no`
// line), the lead drops into the scene below, onto that mark, a real g.goto with the scene entered (its `enter` told he
// came from up here); an area below with `peek: { drop: true }` (or a mark's name) does the same from above. The drop
// is a short fall from `from` (a point of the scene below, where the grille is in its picture: by default straight
// above the mark), on his `drop` frames if he has them. And back up: an area of the scene below with
// `climb: { scene, spawn, to, who }` takes him up (his `climb` frames), to that mark of the scene above.

import { listed, picture, url } from "./assets.js";
import { W, H } from "./grid.js";

const told = new Set();
const once = (key, text) => { if (!told.has(key)) { told.add(key); console.warn(text); } };

export class Grilles {
  constructor(game) {
    this.g = game;
    this.view = null;                 // while looking down: { from, scene, spot, grille }
    // The grille's picture lies over the cast (and the light, and the moving things on it), under Show's outlines, the
    // clickable areas and the words: a layer of its own, put just after the cast.
    const cast = game.stage.querySelector("#cast");
    this.el = document.createElement("img");
    this.el.id = "grille"; this.el.className = "layer"; this.el.alt = ""; this.el.draggable = false; this.el.hidden = true;
    if (cast) cast.after(this.el);
    this.standin = null;
  }

  /** A hotspot's grille, if it is one: { scene, spawn, when, no, from, view }; else null. */
  specOf(spot) { const r = spot && spot.grille; return r && typeof r === "object" && typeof r.scene === "string" ? r : null; }
  /** Does an area of the scene below take a lead up (its `climb`), for this lead? The spec, or null. */
  climbOf(spot, who = this.g.store.data.active) {
    const c = spot && spot.climb;
    if (!c || typeof c !== "object" || typeof c.scene !== "string") return null;
    const leads = c.who == null ? null : [].concat(c.who);
    return !leads || leads.includes(who) ? c : null;
  }

  /** Forget a view (the stage is about to be built again, whatever for). */
  clear() { this.view = null; this.el.hidden = true; this.el.removeAttribute("src"); }

  /** The grille's picture over the view: its own (painted), or the stand-in drawn by code until it is. */
  async cover(view) {
    const src = await this.source(view.grille.view || `art/scenes/${view.from.id}/grille-view.png`);
    if (this.view !== view) return;
    this.el.src = src;
    try { await this.el.decode(); } catch { /* shown as it comes */ }
    if (this.view === view) this.el.hidden = false;
  }
  /** The address of a grille's picture: the painted one, once it is among the page's files; else the stand-in, said once. */
  async source(path) {
    if (listed(path)) { const img = await picture(path); if (img) return url(path); }
    once("standin|" + path, `The grille's picture ${path} is not painted yet: a stand-in drawn by the engine is shown.`);
    return this.standin || (this.standin = drawStandin());
  }
  /** For a cut-scene, which dresses the stage itself: a grille's picture over whatever is on the stage, as if seen from up in
      the duct (`of`: the id of the scene whose grille it is, for its art/scenes/<id>/grille-view.png, or a picture's path;
      the stand-in until it is painted), until over(null) or the stage is emptied (g.view.clear). Not while looking down
      through a grille (the view has its own). True if it is up (or taken away, for null). */
  async over(of) {
    if (!of) { if (!this.view) { this.el.hidden = true; this.el.removeAttribute("src"); } return !this.view; }
    if (this.view) { console.warn("g.grilleOver: the lead is looking down through a grille, which has its picture already."); return false; }
    const src = await this.source(String(of).includes("/") ? String(of) : `art/scenes/${of}/grille-view.png`);
    if (this.view) return false;
    this.el.src = src;
    try { await this.el.decode(); } catch { /* shown as it comes */ }
    this.el.hidden = false;
    return true;
  }

  /** Look down through a grille: `spot` is the hotspot (the lead has walked to it), or its id, from a script. */
  async look(spot) {
    const g = this.g, from = g.here;
    if (typeof spot === "string") spot = ((from && from.hotspots) || []).find((h) => h.id === spot) || null;
    const gr = this.specOf(spot);
    if (!gr || !from) { console.warn(`g.lookDown: ${spot ? `"${spot.id}" is not a grille` : "no such grille here"}, so nothing happens.`); return false; }
    let scene;
    try { scene = await g.getScene(gr.scene); }
    catch (err) { console.warn(`The grille "${spot.id}" looks down into "${gr.scene}", which would not load:`, err); return false; }
    const lead = g.lead;
    if (lead && lead.play && !g.clock.skipping && lead.sheet) {        // a painted lead lies down at the grille: his `peek` frames
      if (lead.walking && lead._stop) lead._stop();
      await lead.play(g.clock, "peek", { ms: 420 });
    }
    g.rememberPlace();
    await g.fade(1, 200);
    const view = { from, scene, spot, grille: gr };
    await g.enterScene(scene, null, "default", { peek: view });
    await g.fade(0, 260);
    if (scene.viewed && this.view === view) {
      try { await scene.viewed(g, from.id); } catch (err) { console.error(`Scene "${scene.id}": viewed stopped:`, err); }
    }
    return true;
  }

  /** Back up from a view, onto the grille: the scene up here built again (its `setup`, not its `enter`: nobody left it). */
  async back() {
    const g = this.g, view = this.view;
    if (!view) return false;
    const d = g.store.data, at = d.where[d.active];
    await g.fade(1, 200);
    await g.enterScene(view.from, at && at.scene === view.from.id && at.x != null ? [at.x, at.y] : null);
    await g.fade(0, 240);
    if (view.grille.back) { try { await view.grille.back(g); } catch (err) { console.error("A grille's `back` stopped:", err); } }
    return true;
  }

  /** May the lead drop in through the grille now? Its `when` (none: yes, if it has a `spawn`). */
  may(view = this.view) {
    if (!view || !view.grille.spawn) return false;
    const w = view.grille.when;
    return w === undefined || w === true || (typeof w === "function" && !!w(this.g));
  }

  /** Drop into the scene below, onto its mark `mark` (none: the grille's `spawn`): if the grille's `when` allows, a real
      g.goto, the scene entered (its `enter` told he came from up here, after the fall). Else the grille's `no` line (none:
      the lead's stock "nope"), and nothing happens. True if he went. */
  async drop(mark = null) {
    const g = this.g, view = this.view;
    if (!view) { console.warn("g.dropIn: nobody is looking down through a grille, so nothing happens."); return false; }
    const gr = view.grille, to = mark || gr.spawn;
    if (!to) { console.warn(`g.dropIn: the grille onto "${view.scene.id}" has no spawn, so nobody drops in by it.`); return false; }
    if (!this.may(view)) { if (!(await g.act(gr.no))) await g.say(g.fallback("nope")); return false; }
    if (!(view.scene.spawn || {})[to]) console.warn(`g.dropIn: "${view.scene.id}" has no mark "${to}": the lead lands on its usual mark.`);
    await g.fade(1, 160);
    await g.goto(view.scene.id, { via: "cut", spawn: to, came: view.from.id, card: false, fall: gr.from || true });
    return !!g.scene && g.scene.id === view.scene.id;
  }

  /** The fall into a scene (goto's `fall`, after the scene has faded in and before its `enter`): from `from` (a point of
      the picture; true: straight above the lead, about a room's height) down onto his mark, as a thing falls (slow, then
      fast), on his `drop` frames (the first while he falls, the second as he lands, crouched) if he has them; a plain
      fall otherwise. In depth he is where he lands all the while (in front of what he lands on). */
  async fall(from) {
    const g = this.g, lead = g.lead;
    if (!lead) return;
    lead.fade(1);                                 // (goto hid him on his mark while the scene faded in)
    if (g.clock.skipping) return;
    const x1 = lead.x, y1 = lead.y, s = lead.scale, base = lead.base;
    const [x0, y0] = Array.isArray(from) ? from : [x1, Math.max(-20, y1 - 150 * s)];
    const h = Math.max(0, y1 - y0), ms = Math.round(240 + Math.sqrt(h) * 18);
    lead.base = base ?? y1;
    if (lead.pose) lead.pose("drop", 0);
    lead.place(x0, y0, s);
    await g.tween(ms, (k) => lead.place(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k * k, s), (k) => k);
    lead.place(x1, y1, s);
    if (lead.pose) { lead.pose("drop", 1); await g.wait(260); lead.pose(null); }
    lead.base = base;
    g.rememberPlace();
  }

  /** Climb out of this scene up into the one above (an area's `climb`: { scene, spawn, to }): from where the lead stands up
      toward `to` (where the opening is in this picture; by default straight up, a room's height), on his `climb` frames
      if he has them, fading as he goes in; then the scene above, on its mark `spawn`, as by any way out (this scene's
      `leaving` runs, the other's `enter` is told he came from here). */
  async climb(c) {
    const g = this.g, lead = g.lead, scene = g.scene;
    if (!lead || !scene) return false;
    const x0 = lead.x, y0 = lead.y, s = lead.scale, [x1, y1] = Array.isArray(c.to) ? c.to : [x0, Math.max(-30, y0 - 160 * s)];
    if (!g.clock.skipping) {
      const len = Math.hypot(x1 - x0, y1 - y0), pace = (lead.spec && lead.spec.pace) || 120, ms = c.ms || Math.max(500, Math.min(2200, (len / (pace * 0.6 * Math.max(s, 0.5))) * 1000));
      if (Math.abs(x1 - x0) > 2) lead.face(x1 > x0 ? "E" : "W");
      lead.base = y0;
      const playing = lead.play && lead.sheet ? lead.play(g.clock, c.set || "climb") : null;
      await g.tween(ms, (k) => { lead.place(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, s); if (k > 0.8) lead.fade(Math.max(0, (1 - k) / 0.2)); }, (k) => k);
      if (lead.stop) lead.stop();
      if (playing) await playing;
    }
    await g.goto(c.scene, { spawn: c.spawn, came: scene.id, card: false });
    return true;
  }
}

/** The stand-in for a grille's picture, until one is painted: four broad slats of a ceiling grille very close and soft,
    across the picture, catching the light of the room on their near edges; clear between them; a soft dark frame round
    the edge, the duct's dark. No more than about a third of the picture covered. An address (a data URL), made once. */
function drawStandin() {
  const c = document.createElement("canvas");
  c.width = W; c.height = H;
  const x = c.getContext("2d");
  const frame = x.createRadialGradient(W / 2, H / 2, H * 0.42, W / 2, H / 2, H * 0.92);
  frame.addColorStop(0, "rgba(10, 12, 16, 0)"); frame.addColorStop(1, "rgba(10, 12, 16, 0.9)");
  x.fillStyle = frame; x.fillRect(0, 0, W, H);
  x.filter = "blur(3px)";
  for (const y of [86, 236, 386, 536]) {
    const g = x.createLinearGradient(0, y - 22, 0, y + 22);
    g.addColorStop(0, "#8b929c"); g.addColorStop(0.18, "#d9dde2"); g.addColorStop(0.4, "#9aa1aa"); g.addColorStop(1, "#4a5058");
    x.fillStyle = g;
    x.fillRect(-10, y - 22, W + 20, 44);
  }
  x.filter = "none";
  return c.toDataURL();
}
