// Show: an outline round each thing the player can click.
//
// The Show button, or holding H, puts the class "reveal" on the clickable layer (#hot); a script can do the same with
// g.reveal(true). While that class is there, this layer (a canvas of its own, just under #hot) shows an outline round
// each thing the player can click: a crisp light line with a soft glow outside it, in the time-cyan, following the
// thing's own shape. Nothing is filled. The shape it follows:
//
//   - for an area that names something on the stage (`plane: "<id>"`; with no `plane`, a cut-out, person or prop with
//     the area's own id): that thing's silhouette, the edge of its picture as it is drawn right now (its state or
//     frame, where it stands), but only as much of it as lies inside the area grown by a few pixels;
//   - for a companion (the mate.* areas the game adds): the person's own figure, as drawn at that moment;
//   - for any other area, and for one whose thing is not showing: the area's own poly, rect or circle.
//
// Each way out at an edge of the picture (edges.js) gets an arrow at the middle of its edge. Areas whose `when` is false
// are left out. The area that has keyboard focus (Tab) gets the same outline, by itself, while Show is off.
//
// It is drawn once when Show is turned on, and again only if what it shows has changed while it is on (another scene, an
// area coming or going, a cut-out's state, a companion's place). While Show is off the layer is hidden: it costs nothing.

import { W, H } from "./grid.js";
import { SIDES, open } from "./edges.js";

const RING = 2;            // the line is this many pixels wide, just outside the thing
const GROW = 4;            // a thing's own picture is outlined only inside its area, grown by this many pixels
const GLOW = 7;            // how far the glow reaches out from the line (a canvas shadow blur)
const PAD = RING + GROW + GLOW + 3;          // room round an area for all of that
const LINE = [218, 253, 255];                // the line itself: the time-cyan, lit almost to white
// every step from a pixel to the pixels within RING of it
const DISC = [];
for (let dy = -RING; dy <= RING; dy++) for (let dx = -RING; dx <= RING; dx++) if ((dx || dy) && dx * dx + dy * dy <= RING * RING + 0.5) DISC.push([dx, dy]);

/** The box round an area: [left, top, right, bottom]. */
function boxOf(spot) {
  if (spot.rect) { const [x, y, w, h] = spot.rect; return [x, y, x + w, y + h]; }
  if (spot.circle) { const [x, y, r] = spot.circle; return [x - r, y - r, x + r, y + r]; }
  const xs = spot.poly.map((p) => p[0]), ys = spot.poly.map((p) => p[1]);
  return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
}

/** The area's own shape, as a path on the picture. */
function pathOf(spot) {
  const p = new Path2D();
  if (spot.rect) p.rect(...spot.rect);
  else if (spot.circle) p.arc(spot.circle[0], spot.circle[1], spot.circle[2], 0, Math.PI * 2);
  else { spot.poly.forEach(([x, y], i) => (i ? p.lineTo(x, y) : p.moveTo(x, y))); p.closePath(); }
  return p;
}

/**
 * Where the cast layer paints a thing right now, worked out the way the cast does it (cast.js, Cast.update):
 * { pic, x, y, w, h }, or null if it shows nothing.
 */
function placed(s, cast) {
  if (!s || s.hidden || !(s.opacity > 0) || !s.picture) return null;
  const pic = s.picture(cast.palette, cast.calm);
  if (!pic || !pic.canvas) return null;
  const sized = pic.w != null, soft = sized && !pic.hard;
  const x = soft ? Math.round((s.x - pic.ox) * 8) / 8 : sized ? Math.round(s.x - pic.ox) : Math.round(s.x) - Math.round(pic.ox);
  const y = soft ? Math.round((s.y - pic.oy) * 8) / 8 : sized ? Math.round(s.y - pic.oy) : Math.round(s.y) - Math.round(pic.oy);
  const w = soft ? Math.round(pic.w * 8) / 8 : sized ? pic.w : pic.canvas.width, h = soft ? Math.round(pic.h * 8) / 8 : sized ? pic.h : pic.canvas.height;
  return { pic, x, y, w, h };
}

export class Outlines {
  constructor(game) {
    this.g = game;
    const hot = game.view.hotEl;
    const c = (this.canvas = document.createElement("canvas"));
    c.width = W; c.height = H;
    c.id = "outlines";
    c.className = "layer";
    c.hidden = true;
    c.setAttribute("aria-hidden", "true");
    hot.before(c);                                   // over the people and the light, under the clickable areas, the words and the fades
    this.ctx = c.getContext("2d");
    this.scratch = document.createElement("canvas").getContext("2d", { willReadFrequently: true });
    this.work = document.createElement("canvas").getContext("2d");
    this.on = false;
    this.focused = null;                             // the area with keyboard focus, outlined by itself while Show is off
    this.key = "";                                   // what is drawn now, in a few characters
    this.drawn = [];                                 // and in full: { id, by: "picture" | "shape", box } for each area outlined, then { edge } for each arrow
    // However Show is turned on or off (the button, the H key, a script), the layer follows the class on #hot.
    new MutationObserver(() => this.changed()).observe(hot, { attributes: true, attributeFilter: ["class"] });
  }

  /** The area with keyboard focus (or null): outlined by itself while Show is off. */
  focus(spot) { this.focused = spot || null; this.changed(); }

  /** Something may have changed. Draw again if what the layer should show is different now; otherwise do nothing. */
  changed() {
    const g = this.g;
    this.on = g.view.hotEl.classList.contains("reveal");
    if (!this.on && !this.focused) { if (this.key) this.clear(); return; }                 // (the usual case: off, and nothing to do)
    const play = g.mode === "play" && !!g.scene;
    const spots = !play ? [] : (this.on ? g.view.spots : [this.focused]).filter((s) => s && g.view.spots.includes(s) && (!s.when || s.when(g)));
    const edges = play && this.on ? SIDES.filter((side) => g.scene.edges && open(g.scene.edges[side], g)) : [];
    let key = (play ? g.scene.id : "-") + "|" + edges.join("");
    for (const s of spots) {
      const t = this.thingOf(s);
      key += `|${g.view.spots.indexOf(s)}` + (t ? `:${t.id},${t.hidden ? 0 : 1},${t.state ?? ""},${Math.round(t.x)},${Math.round(t.y)},${t.scale}` : "");
    }
    if (key === this.key) return;
    this.key = key;
    this.paint(spots, edges);
  }

  clear() {
    this.key = "";
    this.drawn = [];
    this.ctx.clearRect(0, 0, W, H);
    this.canvas.hidden = true;
  }

  paint(spots, edges) {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, W, H);
    this.drawn = [];
    const glow = getComputedStyle(this.g.stage).getPropertyValue("--time-cyan").trim() || "#5ef2ff";
    for (const spot of spots) {
      try { this.outline(spot, glow); }
      catch (err) { console.warn(`Show could not outline "${spot.id}":`, err); }
    }
    for (const side of edges) this.arrow(side, glow);
    this.canvas.hidden = !this.drawn.length;
  }

  /** What an area stands for on the stage, if anything: a companion's figure, the thing it names with `plane`, the person
      it names with `actor`, or a thing with its own id. */
  thingOf(spot) {
    const cast = this.g.view.cast;
    if (spot.mate) return cast.get(spot.mate) || null;
    const id = spot.plane || spot.actor || spot.id;
    return (id && id !== this.g.store.data.active && cast.get(id)) || null;
  }

  /** Draw on the scratch canvas (w by h, cleared) and read back where it is solid: a mask, one byte a pixel. */
  mask(w, h, draw, solid = 128) {
    const c = this.scratch, cv = c.canvas;
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; } else c.clearRect(0, 0, w, h);
    c.save();
    draw(c);
    c.restore();
    const px = c.getImageData(0, 0, w, h).data, out = new Uint8Array(w * h);
    for (let i = 0; i < out.length; i++) out[i] = px[i * 4 + 3] >= solid ? 1 : 0;
    return out;
  }

  /** The ring just outside a mask, RING pixels wide, kept to `within` if given. Null if it is empty. */
  ring(mask, w, h, within = null) {
    const out = new Uint8Array(w * h);
    let any = false;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x;
      if (!mask[i]) continue;
      // only the pixels at the edge of the mask can have open ground within RING of them
      if (x > 0 && x < w - 1 && y > 0 && y < h - 1 && mask[i - 1] && mask[i + 1] && mask[i - w] && mask[i + w]) continue;
      for (const [dx, dy] of DISC) {
        const xx = x + dx, yy = y + dy;
        if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue;
        const j = yy * w + xx;
        if (!mask[j] && (!within || within[j])) { out[j] = 1; any = true; }
      }
    }
    return any ? out : null;
  }

  outline(spot, glow) {
    const g = this.g, box = boxOf(spot), shape = pathOf(spot);
    const x0 = Math.max(0, Math.floor(box[0]) - PAD), y0 = Math.max(0, Math.floor(box[1]) - PAD);
    const x1 = Math.min(W, Math.ceil(box[2]) + PAD), y1 = Math.min(H, Math.ceil(box[3]) + PAD), w = x1 - x0, h = y1 - y0;
    if (w <= 0 || h <= 0) return;
    let solid = null, line = null, by = "shape";
    const at = placed(this.thingOf(spot), g.view.cast);
    if (at) {                                        // the thing's own picture, as the cast paints it
      const { pic } = at;
      solid = this.mask(w, h, (c) => {
        if (pic.w == null) c.drawImage(pic.canvas, at.x - x0, at.y - y0);
        else { c.imageSmoothingEnabled = !pic.hard; c.drawImage(pic.canvas, 0, 0, pic.sw, pic.sh, at.x - x0, at.y - y0, at.w, at.h); }
      });
      const area = this.mask(w, h, (c) => { c.translate(-x0, -y0); c.fillStyle = c.strokeStyle = "#000"; c.lineWidth = GROW * 2; c.lineJoin = "round"; c.fill(shape); c.stroke(shape); }, 1);
      line = this.ring(solid, w, h, area);
      if (line) by = "picture";
    }
    if (!line) {                                     // the area's own shape
      solid = this.mask(w, h, (c) => { c.translate(-x0, -y0); c.fillStyle = "#000"; c.fill(shape); });
      line = this.ring(solid, w, h);
    }
    if (!line) return;
    this.stamp(line, solid, x0, y0, w, h, glow);
    this.drawn.push({ id: spot.id, by, box: [x0, y0, x1, y1] });
  }

  /** Put a ring on the layer: first its glow, then the glow taken off whatever lies inside the thing, then the line itself, crisp. */
  stamp(line, solid, x0, y0, w, h, glow) {
    const picture = (bits, [r, gr, b]) => {
      const c = document.createElement("canvas");
      c.width = w; c.height = h;
      const ctx = c.getContext("2d"), img = ctx.createImageData(w, h), d = img.data;
      for (let i = 0; i < bits.length; i++) if (bits[i]) { d[i * 4] = r; d[i * 4 + 1] = gr; d[i * 4 + 2] = b; d[i * 4 + 3] = 255; }
      ctx.putImageData(img, 0, 0);
      return c;
    };
    const ring = picture(line, LINE), inside = picture(solid, [0, 0, 0]);
    const k = this.work, cv = k.canvas;
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; } else k.clearRect(0, 0, w, h);
    k.save();
    k.shadowColor = glow;
    k.shadowBlur = GLOW;
    k.drawImage(ring, 0, 0);
    k.drawImage(ring, 0, 0);                         // (twice: one thin line casts a faint glow)
    k.restore();
    k.globalCompositeOperation = "destination-out";  // no glow over the thing itself: it glows outward only
    k.drawImage(inside, 0, 0);
    k.globalCompositeOperation = "source-over";
    k.drawImage(ring, 0, 0);
    this.ctx.drawImage(cv, x0, y0);
  }

  /** The bottom arrow's place: the middle of the bottom edge, or, when a long row of carried things lies over that,
      just to the right of the row (which grows from the left), so that the arrow is never hidden under it. */
  clearOfInventory(x, y) {
    const inv = this.g.ui && this.g.ui.invEl, stage = this.g.stage;
    if (!inv || inv.hidden || !stage) return x;
    const box = stage.getBoundingClientRect(), r = inv.getBoundingClientRect();
    if (!box.width || !box.height || !r.width || !r.height) return x;
    const left = ((r.left - box.left) / box.width) * W, right = ((r.right - box.left) / box.width) * W, top = ((r.top - box.top) / box.height) * H;
    if (y + 14 < top || x + 16 < left || x - 16 > right) return x;
    return Math.min(W - 30, right + 30);
  }

  /** A soft arrow at the middle of an edge with a way out, pointing out of the picture. */
  arrow(side, glow) {
    // (the top one sits a little lower than the others, clear of the place name the HUD writes at the top of the picture)
    const ctx = this.ctx, [x0, y, turn] = { N: [W / 2, 46, 0], S: [W / 2, H - 20, 2], W: [20, H / 2, 3], E: [W - 20, H / 2, 1] }[side];
    const x = side === "S" ? this.clearOfInventory(x0, y) : x0;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate((turn * Math.PI) / 2);
    const p = new Path2D("M0 -13 L14 1 L5 1 L5 12 L-5 12 L-5 1 L-14 1 Z");        // pointing up; turned for the other edges
    ctx.shadowColor = glow;
    ctx.shadowBlur = 10;
    ctx.fillStyle = `rgba(${LINE.join(",")}, 0.85)`;
    ctx.fill(p);
    ctx.shadowColor = "transparent";
    ctx.strokeStyle = "rgba(20, 11, 43, 0.55)";        // a thin dark edge, so that it reads on a bright sky as well as a dark wall
    ctx.lineWidth = 1.5;
    ctx.lineJoin = "round";
    ctx.stroke(p);
    ctx.restore();
    this.drawn.push({ edge: side });
  }
}
