// What is on the stage: the background drawing, the actors, and the clickable areas.
// The background is drawn once per scene and then left alone. Actors are separate
// elements moved with CSS transforms, which the browser can do without redrawing
// the background.

import { sprite, sprites } from "../art/kit.js";

const U = 100 / 320;   // one grid pixel in cqw

export class Actor {
  constructor(id, name, host) {
    this.id = id;
    this.spriteName = name;
    const s = sprites[name];
    this.w = s.w; this.h = s.h;
    this.el = document.createElement("div");
    this.el.className = "actor";
    this.el.dataset.id = id;
    this.el.style.width = `${s.w * U}cqw`;
    this.el.style.height = `${s.h * U}cqw`;
    this.el.innerHTML = sprite(name);
    host.appendChild(this.el);
    this.x = 0; this.y = 0; this.scale = 1; this.dir = 1; this.opacity = 1;
  }

  /** Put the actor's feet at (x, y) on the grid. */
  place(x, y, scale = this.scale) {
    this.x = x; this.y = y; this.scale = scale;
    this.el.style.transform =
      `translate(${(x - this.w / 2) * U}cqw, ${(y - this.h) * U}cqw) scale(${scale * this.dir}, ${scale})`;
    this.el.style.zIndex = Math.round(y);
    return this;
  }
  face(dir) { this.dir = dir < 0 ? -1 : 1; return this.place(this.x, this.y); }
  fade(opacity) { this.opacity = opacity; this.el.style.opacity = opacity; return this; }
  flag(name, on) { this.el.classList.toggle(name, on); return this; }

  /** Walk in a straight line. A new walk replaces the one in progress. */
  walkTo(clock, x, y, scaleAt = () => this.scale, speed = 64) {
    if (this._stop) this._stop();
    const sx = this.x, sy = this.y;
    const dist = Math.hypot(x - sx, (y - sy) * 2);      // going "into" the picture takes longer
    if (clock.skipping || dist < 0.5) { this.place(x, y, scaleAt(y)); return Promise.resolve(); }
    const ms = (dist / speed) * 1000;
    if (Math.abs(x - sx) > 1) this.dir = x < sx ? -1 : 1;
    return new Promise((resolve) => {
      let t = 0;
      const finish = () => { stop(); this._stop = null; this.flag("step", false); resolve(); };
      const stop = clock.every((dt) => {
        t += dt;
        const k = clock.skipping ? 1 : Math.min(t / ms, 1);
        const ny = sy + (y - sy) * k;
        this.place(sx + (x - sx) * k, ny, scaleAt(ny));
        this.flag("step", Math.floor(t / 150) % 2 === 1);
        if (k >= 1) finish();
      });
      this._stop = finish;
    });
  }
}

export class SceneView {
  constructor(stage) {
    this.stage = stage;
    this.sceneEl = stage.querySelector("#scene");
    this.actorsEl = stage.querySelector("#actors");
    this.hotEl = stage.querySelector("#hot");
    this.actors = new Map();
    this.spots = [];
  }

  setEra(era) { this.stage.dataset.era = era; }

  draw(markup) { this.sceneEl.innerHTML = markup; }
  q(selector) { return this.sceneEl.querySelector(selector); }

  clear() {
    this.sceneEl.innerHTML = "";
    this.actorsEl.innerHTML = "";
    this.hotEl.innerHTML = "";
    this.actors.clear();
    this.spots = [];
  }

  addActor(id, spriteName, x, y, scale = 1) {
    const actor = new Actor(id, spriteName, this.actorsEl).place(x, y, scale);
    this.actors.set(id, actor);
    return actor;
  }

  removeActor(id) {
    const a = this.actors.get(id);
    if (a) { a.el.remove(); this.actors.delete(id); }
  }

  /** Build the clickable areas. Each is a real, focusable button for keyboard and screen-reader players. */
  setHotspots(spots) {
    this.spots = spots;
    const shape = (h, i) => {
      const common = `class="spot" data-i="${i}" tabindex="0" role="button" aria-label="${h.name}"`;
      if (h.rect) { const [x, y, w, hh] = h.rect; return `<rect ${common} x="${x}" y="${y}" width="${w}" height="${hh}"/>`; }
      if (h.circle) { const [cx, cy, r] = h.circle; return `<circle ${common} cx="${cx}" cy="${cy}" r="${r}"/>`; }
      return `<polygon ${common} points="${h.poly.map((p) => p.join(",")).join(" ")}"/>`;
    };
    this.hotEl.innerHTML = `<rect class="floor" width="320" height="200"/>` + spots.map(shape).join("");
  }

  /** Hide the areas whose `when` test fails right now. */
  refreshHotspots(game) {
    this.hotEl.querySelectorAll(".spot").forEach((el) => {
      const h = this.spots[el.dataset.i];
      el.style.display = !h.when || h.when(game) ? "" : "none";
    });
  }

  /** Turn a pointer event into grid coordinates. */
  toGrid(event) {
    const box = this.stage.getBoundingClientRect();
    return [((event.clientX - box.left) / box.width) * 320, ((event.clientY - box.top) / box.height) * 200];
  }
}

/** Keep a point inside a scene's walkable box, and work out how big an actor is there. */
export function clampToWalk(walk, x, y) {
  return [Math.min(Math.max(x, walk.x[0]), walk.x[1]), Math.min(Math.max(y, walk.y[0]), walk.y[1])];
}
export function scaleAt(scene, y) {
  const [near, far] = [scene.walk.y[1], scene.walk.y[0]];
  const [small, big] = scene.scale || [1, 1];
  if (near === far) return big;
  return small + (big - small) * ((y - far) / (near - far));
}
