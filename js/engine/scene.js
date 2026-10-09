// What is on the stage. Four layers, back to front, all 800x600 (grid.js):
//
//   backdrop   the scene's painted picture, pixel for pixel
//   live       light that must stay smooth and can move by itself: wormholes, beams,
//              glows. Drawings, not pixels, so a script can find a part and animate it.
//   cast       people, painted cut-outs and props, sorted by depth every frame (cast.js)
//   hot        invisible shapes the player can click
//
// The painting and the cut-outs are files (assets.js). Time travel is drawn by code
// on purpose: its light stays smooth, so a wormhole never looks like part of the
// world it has opened in.
//
// A painted backdrop is shown as the picture itself (an <img> the view puts on the
// stage). A canvas would look the same and cost more: a browser hands every canvas on
// the page to its compositor again for each frame in which anything at all has changed,
// and the backdrop is the one layer that never does. Measured on a slow machine, that
// was a third of the cost of a frame in which somebody walks.
//
// A scene with no painting yet is drawn the old way: markup from the art kit is
// turned into pixels once, when the scene opens, on the backdrop canvas. The kit's own
// scene drawings were made on a 320x200 grid, so they are shown in a band across the
// middle of the stage.

import { Cast, picturesOf } from "./cast.js";
import { picture, url } from "./assets.js";
import { fxPictures } from "./effects.js";
import { W, H, OLD, fit } from "./grid.js";
import * as art from "../art/kit.js";

const SVG = "http://www.w3.org/2000/svg";
const SHAPE = new Set(["x", "y", "width", "height", "cx", "cy", "r", "points"]);      // the attributes that say an area's shape

// The pictures are 800 pixels wide and the stage is whatever the window allows. When each picture pixel covers at
// least this many screen pixels, the pictures are shown with hard pixels; below it they are smoothed, because hard
// pixels of uneven widths look worse than soft ones. The style sheet does the work (css/game.css, "crisp") and says
// more about why. To have hard pixels at every size, make this 0; to have none, Infinity.
export const CRISP_FROM = 2;

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
    this.backdrop = stage.querySelector(".backdrop");       // a canvas: a backdrop that is drawn by code is shown here (and a painted one is copied here, for anything that wants its pixels)
    this.painting = document.createElement("img");          // a painted backdrop is shown here, and the canvas is put away
    this.painting.className = "painting";
    this.painting.alt = "";
    this.painting.draggable = false;
    this.painting.style.display = "none";
    this.backdrop.before(this.painting);
    this.liveEl = stage.querySelector(".live");
    this.hotEl = stage.querySelector(".hot");
    this.cast = new Cast(stage.querySelector(".cast"));
    this.actors = this.cast.items;          // everyone on stage, by id
    this.spots = [];
    this.drawing = 0;
    this.palette = paletteOf(stage);
    this.cast.palette = this.palette;
    // Hard pixels or smooth: measured now, and again whenever the stage changes size. (A stage 1599.98 screen pixels wide is twice 800.)
    const measure = () => stage.classList.toggle("crisp", (stage.getBoundingClientRect().width * (window.devicePixelRatio || 1)) / W >= CRISP_FROM - 0.02);
    measure();
    if (window.ResizeObserver) new ResizeObserver(measure).observe(stage);
    window.addEventListener("resize", measure);
  }

  setEra(era) {
    this.stage.dataset.era = era;
    this.palette = paletteOf(this.stage);
    this.cast.palette = this.palette;
  }

  /**
   * Put a scene on the stage: its painted backdrop (or, with none, its kit drawing or a sketch), its light,
   * and its painted cut-outs. `g` is what the scene's own functions are handed (the game).
   * The light and the cut-outs are in place at once, so scripts can find them. The promise resolves when
   * every picture the scene can show has arrived and the backdrop is painted: wait for it before fading
   * in, and nothing pops in late.
   */
  show(scene, g) {
    const kit = scene.draw ? scene.draw(art, g) : scene.picture ? "" : art.sketch(scene);
    const drawn = this.draw(kit, scene.name, { picture: scene.picture, live: scene.live ? scene.live(art, g) : "", grid: scene.draw ? OLD : [W, H],
      instead: () => art.sketch(scene) });
    for (const plane of scene.planes || []) this.cast.addCutout(plane.id, plane);
    this.cast.refresh(g);
    return Promise.all([drawn, this.cast.load()]);
  }

  /** Ask for a scene's pictures ahead of time, without showing anything: for the scenes that can be walked to from
      the one on stage, so that going there does not mean waiting for them. */
  warm(scene) {
    for (const path of picturesIn(scene)) picture(path);
  }

  /**
   * Paint the backdrop and set out the live layer.
   *   inner     markup from the art kit, turned into pixels. Parts marked class="live" stay as drawings.
   *   picture   a painted backdrop: the path of an 800x600 picture, put down first, with no scaling
   *   live      markup in 800x600 units, all of it for the live layer
   *   grid      the grid `inner` was drawn on. The kit's old scene drawings are 320x200 (the default),
   *             and are shown in the band that fits; a sketch is drawn on the stage's own 800x600.
   *   instead   a function giving markup in 800x600 units to use if the picture will not load and there is
   *             no `inner`: a scene whose painting is missing is sketched, and can still be played.
   * The live parts are in place at once; the promise resolves when the pixels are too.
   */
  async draw(inner = "", title = "", { picture: file = null, live = "", grid = OLD, instead = null } = {}) {
    const turn = ++this.drawing;
    const pixels = (markup, on) => {                       // kit markup as a drawing ready to be turned into pixels
      const svg = document.createElementNS(SVG, "svg");
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
      svg.setAttribute("width", W); svg.setAttribute("height", H);
      svg.setAttribute("shape-rendering", "crispEdges");
      svg.innerHTML = `<style>${this.palette.css}</style>${art.defs}${fit(markup, on)}`;
      return svg;
    };
    const holder = pixels(inner, grid);
    // The live layer: first the live parts of the kit drawing, on the same grid as the rest of it, then the scene's own light.
    this.liveEl.innerHTML = `${art.defs}${fit("", grid)}${live}`;
    const band = holder.lastElementChild, liveBand = this.liveEl.querySelector("svg");
    for (const node of holder.querySelectorAll(".live")) if (!node.parentNode.closest(".live")) liveBand.appendChild(node);
    this.liveEl.setAttribute("aria-label", title);

    const load = (svg) => new Promise((done) => {
      const img = new Image();
      img.onload = () => done(img); img.onerror = () => done(img);
      img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(new XMLSerializer().serializeToString(svg));
    });
    let [image, painted] = await Promise.all([
      inner ? load(holder) : null,
      file ? picture(file) : null,                           // (a picture that will not load has already been reported, by name)
    ]);
    let on = grid;                                         // the grid of whatever `image` is a drawing of
    if (file && !painted && !inner && instead) { image = await load(pixels(instead(), [W, H])); on = [W, H]; }
    if (turn !== this.drawing) return;                     // a newer drawing has taken this one's place
    const ctx = this.backdrop.getContext("2d");
    ctx.clearRect(0, 0, W, H);
    ctx.imageSmoothingEnabled = false;
    if (painted) ctx.drawImage(painted, 0, 0);
    const whole = painted && painted.naturalWidth === W && painted.naturalHeight === H;
    if (painted && !whole) console.warn(`The picture ${file} is ${painted.naturalWidth}x${painted.naturalHeight}. A backdrop should be ${W}x${H}: it is put down as it is, with no scaling.`);
    if (image && image.naturalWidth) {
      ctx.drawImage(image, 0, 0, W, H);
      // A drawing on the old grid leaves a strip above and below it. Fill each with the drawing's own edge,
      // so the sky carries on up and the ground carries on down. (A stop-gap, until every scene is painted.)
      const y = Math.round((H - (on[1] * W) / on[0]) / 2);
      if (y > 0 && !painted) { ctx.drawImage(this.backdrop, 0, y, W, 1, 0, 0, W, y); ctx.drawImage(this.backdrop, 0, H - y - 1, W, 1, 0, H - y, W, y); }
    } else if (image) {                                    // a browser that will not turn a drawing into pixels still gets the drawing, under its live parts
      const first = liveBand.firstChild;
      for (const node of [...band.childNodes]) liveBand.insertBefore(node, first);
    }
    // Which of the two is shown. A painting with nothing drawn over it is shown as the picture itself (see the top
    // of this file); anything else stays on the canvas, as painted just now.
    let plain = !!whole && !image;
    if (plain) {
      const el = this.painting, address = url(file);       // (the copy held for this session: see assets.js)
      if (el.getAttribute("src") !== address) el.src = address;
      try { await el.decode(); } catch { plain = false; }  // ready to paint before it is shown, so nothing pops in
      if (turn !== this.drawing) return;
    }
    this.present(plain);
  }

  /** Show the painting (true) or the canvas (false), never both. */
  present(painting) {
    const el = this.painting;
    if (!painting) el.removeAttribute("src");
    el.style.display = painting ? "" : "none";
    this.backdrop.style.display = painting ? "none" : "";
  }

  /** Find a live part of the drawing, for a script to move or fade. */
  q(selector) { return this.liveEl.querySelector(selector); }

  clear() {
    this.drawing++;
    this.backdrop.getContext("2d").clearRect(0, 0, W, H);
    this.present(false);
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
    this.hotEl.innerHTML = `<rect class="floor" width="${W}" height="${H}"/>` + spots.map(shape).join("");
  }

  /** One area's shape has changed (someone has walked off with theirs, or come back: life.js). Its element is given the
      new shape where it is, keeping everything else about it (and keyboard focus, if it had it). */
  reshape(i) {
    const old = this.hotEl.querySelector(`.spot[data-i="${i}"]`), h = this.spots[i];
    if (!old || !h) return;
    const tag = h.rect ? "rect" : h.circle ? "circle" : "polygon";
    let el = old;
    if (old.tagName.toLowerCase() !== tag) {
      el = document.createElementNS(SVG, tag);
      for (const { name, value } of [...old.attributes]) if (!SHAPE.has(name)) el.setAttribute(name, value);
      const focused = document.activeElement === old;
      old.replaceWith(el);
      if (focused) el.focus({ preventScroll: true });
    }
    const set = (o) => { for (const [k, v] of Object.entries(o)) el.setAttribute(k, v); };
    if (h.rect) set({ x: h.rect[0], y: h.rect[1], width: h.rect[2], height: h.rect[3] });
    else if (h.circle) set({ cx: h.circle[0], cy: h.circle[1], r: h.circle[2] });
    else set({ points: h.poly.map((p) => p.join(",")).join(" ") });
  }

  /** Hide the areas whose `when` test fails right now. */
  refreshHotspots(game) {
    this.hotEl.querySelectorAll(".spot").forEach((el) => {
      const h = this.spots[el.dataset.i];
      el.style.display = !h.when || h.when(game) ? "" : "none";
    });
  }

  /** The story has changed: the clickable areas and the painted cut-outs read their `when` and `state` again. */
  refresh(game) {
    this.refreshHotspots(game);
    this.cast.refresh(game);
  }

  /** Turn a pointer event into a place on the picture. */
  toPicture(event) {
    const box = this.stage.getBoundingClientRect();
    return [((event.clientX - box.left) / box.width) * W, ((event.clientY - box.top) / box.height) * H];
  }
}

/** Every picture file a scene can show: its backdrop, and each cut-out's picture, states and frames. */
export const picturesIn = (scene) => [scene.picture, ...(scene.planes || []).flatMap(picturesOf), ...fxPictures(scene)].filter(Boolean);      // (fxPictures: the painted frames of its birds)

/** Where a clickable area meets the ground: the middle of its bottom edge. The lead turns to face this. */
export function footOf(spot) {
  if (spot.rect) return [spot.rect[0] + spot.rect[2] / 2, spot.rect[1] + spot.rect[3]];
  if (spot.circle) return [spot.circle[0], spot.circle[1] + spot.circle[2]];
  let x = 0, y = -Infinity;
  for (const p of spot.poly) { x += p[0] / spot.poly.length; y = Math.max(y, p[1]); }
  return [x, y];
}
