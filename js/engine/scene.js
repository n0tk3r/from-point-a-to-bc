// What is on the stage. Four layers, back to front:
//
//   backdrop   the scene's drawing, turned into pixels once on a 640x400 grid
//   live       the few parts that glow or move by themselves (wormholes, twinkling
//              stars, ripples), kept as smooth drawings on top of the pixels
//   cast       people and props, sorted by depth every frame (cast.js)
//   hot        invisible shapes the player can click
//
// Putting the backdrop and the cast on the same 640x400 grid is what makes the
// picture read as one piece of pixel art. Time travel is the exception on
// purpose: its light stays smooth, so a wormhole never looks like part of the
// world it has opened in.

import { Cast } from "./cast.js";
import { defs } from "../art/kit.js";

const SVG = "http://www.w3.org/2000/svg";
export const ART_W = 640, ART_H = 400;

// class name in the drawings -> color slot in css/tokens.css
const FILLS = { s1: "sky-1", s2: "sky-2", s3: "sky-3", s4: "sky-4", s5: "sky-5", s6: "sky-6", s7: "sky-7", s8: "sky-8",
  far: "far", near: "near", g1: "ground-1", g2: "ground-2", g3: "ground-3", line: "line", light: "light", feat: "feature", feat2: "feature-2",
  "t-core": "time-core", "f-cyan": "time-cyan", "f-magenta": "time-magenta" };
const STROKES = { "stroke-line": "line", "stroke-feat2": "feature-2", "t-cyan": "time-cyan", "t-magenta": "time-magenta", "t-violet": "time-violet", "t-white": "time-core" };

/** The current era's colors, read from the style sheet, as plain values a drawing can carry with it. */
export function paletteOf(el) {
  const style = getComputedStyle(el), read = (slot) => style.getPropertyValue("--" + slot).trim() || "#888";
  let css = "";
  for (const [cls, slot] of Object.entries(FILLS)) css += `.${cls}{fill:${read(slot)}}`;
  for (const [cls, slot] of Object.entries(STROKES)) css += `.${cls}{stroke:${read(slot)}}`;
  return { key: el.dataset.era || "", css, g1: read("ground-1"), g2: read("ground-2"), g3: read("ground-3"), line: read("line"), light: read("light"),
    far: read("far"), near: read("near"), feat: read("feature"), feat2: read("feature-2"), sky: [1, 2, 3, 4, 5, 6, 7, 8].map((i) => read("sky-" + i)) };
}

export class SceneView {
  constructor(stage) {
    this.stage = stage;
    this.backdrop = stage.querySelector(".backdrop");
    this.liveEl = stage.querySelector(".live");
    this.hotEl = stage.querySelector(".hot");
    this.cast = new Cast(stage.querySelector(".cast"));
    this.actors = this.cast.items;          // everyone on stage, by id
    this.spots = [];
    this.drawing = 0;
    this.palette = paletteOf(stage);
    this.cast.palette = this.palette;
  }

  setEra(era) {
    this.stage.dataset.era = era;
    this.palette = paletteOf(this.stage);
    this.cast.palette = this.palette;
  }

  /**
   * Show a scene drawing. `inner` is markup from the art kit (js/art/kit.js).
   * Parts marked class="live" stay as drawings; everything else becomes pixels.
   * `picture` is the address of a painted backdrop (a 640x400 image), if the scene has one:
   * it goes down first and anything drawn by the kit is laid over it.
   * The live parts are in place at once; the promise resolves when the pixels are too.
   */
  async draw(inner, title = "", picture = null) {
    const turn = ++this.drawing;
    const holder = document.createElementNS(SVG, "svg");
    holder.setAttribute("viewBox", "0 0 320 200");
    holder.setAttribute("width", ART_W); holder.setAttribute("height", ART_H);
    holder.setAttribute("shape-rendering", "crispEdges");
    holder.innerHTML = `<style>${this.palette.css}</style>${defs}${inner}`;
    const live = [...holder.querySelectorAll(".live")].filter((node) => !node.parentNode.closest(".live"));
    this.liveEl.innerHTML = defs;
    for (const node of live) this.liveEl.appendChild(node);
    this.liveEl.setAttribute("aria-label", title);

    const load = (src) => new Promise((done) => { const img = new Image(); img.onload = () => done(img); img.onerror = () => done(img); img.src = src; });
    const [image, painted] = await Promise.all([
      load("data:image/svg+xml;charset=utf-8," + encodeURIComponent(new XMLSerializer().serializeToString(holder))),
      picture ? load(picture) : null,
    ]);
    if (turn !== this.drawing) return;                     // a newer drawing has taken this one's place
    const ctx = this.backdrop.getContext("2d");
    ctx.clearRect(0, 0, ART_W, ART_H);
    ctx.imageSmoothingEnabled = false;                     // a painting at another size is scaled in whole pixels, never blurred
    if (painted && painted.naturalWidth) ctx.drawImage(painted, 0, 0, ART_W, ART_H);
    else if (picture) console.warn(`The picture for this scene did not load: ${picture}`);
    if (image.naturalWidth) ctx.drawImage(image, 0, 0, ART_W, ART_H);
    else {                                                 // a browser that will not turn a drawing into pixels still gets the drawing
      for (const node of [...holder.childNodes]) if (node.nodeName !== "style" && node.nodeName !== "defs") this.liveEl.insertBefore(node, this.liveEl.children[1] || null);
    }
  }

  /** Find a live part of the drawing, for a script to move or fade. */
  q(selector) { return this.liveEl.querySelector(selector); }

  clear() {
    this.drawing++;
    this.backdrop.getContext("2d").clearRect(0, 0, ART_W, ART_H);
    this.liveEl.innerHTML = "";
    this.cast.clear();
    this.hotEl.innerHTML = "";
    this.spots = [];
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

/** Where a clickable area meets the ground: the middle of its bottom edge. The lead turns to face this. */
export function footOf(spot) {
  if (spot.rect) return [spot.rect[0] + spot.rect[2] / 2, spot.rect[1] + spot.rect[3]];
  if (spot.circle) return [spot.circle[0], spot.circle[1] + spot.circle[2]];
  let x = 0, y = -Infinity;
  for (const p of spot.poly) { x += p[0] / spot.poly.length; y = Math.max(y, p[1]); }
  return [x, y];
}
