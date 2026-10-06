// Props: things that stand on the ground and can be walked behind.
// Each one is drawn by the pixel renderer, in the same style as the characters,
// at whatever size the scene asks for.
//
// A prop is a function draw(pen, frame, options). The pen works in the prop's own
// measurements: the origin is where the prop meets the ground, x runs right and
// y runs DOWN (so "up" is negative). One unit is one art pixel at scale 1.
//
// options.palette holds the colors of the era the prop is standing in.

import { Surface, ramp, pack } from "./pix.js";

const SHADOW = { tones: [pack("#00000040"), pack("#00000040"), pack("#00000040"), pack("#00000040")], soft: true, flat: 1 };

/** Draws in a prop's own measurements, scaled and (if asked) tilted onto a pixel surface. */
export class Pen {
  constructor(box, scale = 1, tilt = 0, sink = 0) {
    const [x0, y0, x1, y1] = box, pad = 4 + Math.ceil(Math.abs(Math.sin(tilt)) * Math.max(x1 - x0, y1 - y0) * scale * 0.6);
    this.k = scale; this.ca = Math.cos(tilt); this.sa = Math.sin(tilt); this.sink = sink * scale;
    const w = Math.ceil((x1 - x0) * scale) + pad * 2, h = Math.ceil((y1 - y0) * scale) + pad * 2;
    this.sf = new Surface(w + (w & 1), h, Math.round(-x0 * scale) + pad, Math.round(-y0 * scale) + pad);
  }
  pt(x, y) { return [this.sf.ox + (x * this.ca - y * this.sa) * this.k, this.sf.oy + (x * this.sa + y * this.ca) * this.k + this.sink]; }
  poly(points, z, material, tone = 1, o) { this.sf.poly(points.map(([x, y]) => this.pt(x, y)), z, material, tone, o); }
  rect(x, y, w, h, z, material, tone = 1, o) { this.poly([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], z, material, tone, o); }
  oval(cx, cy, rx, ry, z, material, tone = 1, o) {
    const pts = [];
    for (let i = 0; i < 20; i++) { const a = (i / 20) * Math.PI * 2; pts.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]); }
    this.poly(pts, z, material, tone, o);
  }
  limb(ax, ay, bx, by, ra, rb, material, o = {}) {
    const A = this.pt(ax, ay), B = this.pt(bx, by), z = o.z || 0;
    this.sf.limb(A[0], A[1], z, B[0], B[1], z, Math.max(0.8, ra * this.k), Math.max(0.8, rb * this.k), material, o);
  }
  ball(cx, cy, rx, ry, material, o = {}) {
    const C = this.pt(cx, cy);
    this.sf.ball(C[0], C[1], o.z || 0, Math.max(0.8, rx * this.k), Math.max(0.8, ry * this.k), Math.max(0.8, Math.min(rx, ry) * this.k), material, o);
  }
  /** A shadow on the ground under the prop, never tilted. */
  shadow(cx, rx, ry) { this.sf.oval(this.sf.ox + cx * this.k, this.sf.oy - 0.5, rx * this.k, Math.max(1.5, ry * this.k), -1e8, SHADOW); }
}

// ---------- the family wagon, seen from behind ----------
const RED = ramp("#ee8a72", "#cc5c45", "#9f402f", "#6c2b21");
const WOOD = ramp("#c2925a", "#93653a", "#6d4727", "#462d19");
const GLASS = ramp("#6470a0", "#2f3860", "#1b2142", "#0e1226");
const CHROME = ramp("#f6f8fa", "#c4cad1", "#8b929a", "#565c64");
const RUBBER = ramp("#44404b", "#26232b", "#16141a", "#0c0b0e");
const LAMP = ramp("#ffd9c8", "#ff5f47", "#c62c21", "#7c1913");
const CREAM = ramp("#ffffff", "#f1ebdc", "#bfb8a4", "#878170");
const COOLER = ramp("#8cc4ee", "#4f86c6", "#35609a", "#223f68");
const OAK = ramp("#c99a64", "#9c6d3f", "#70492a", "#472d19");
const EBONY = ramp("#6f5a52", "#44332e", "#2b1f1c", "#170f0d");
const BRASS = ramp("#ffeeb0", "#e0b550", "#a8802e", "#6e531c");
const CASE = ramp("#55525f", "#34323c", "#211f27", "#121116");
const DARKSCREEN = ramp("#8795ab", "#2a3445", "#1b2330", "#11161f");
const BLUESCREEN = ramp("#cfe3ff", "#2f5f8f", "#20405f", "#16283d");
const PAPERMAP = ramp("#ffffff", "#ece4c8", "#b9aa8a", "#7a6f55");
const STICKY = ramp("#fff6a8", "#ffe36b", "#f2c94a", "#6b5a1c");
const CLOTH = ramp("#ffffff", "#f3efe4", "#cfc8b6", "#9a937f");
const SHADE = ramp("#fff6cf", "#ffe08a", "#e0b550", "#a8802e");
const CUSHION = ramp("#d86a6a", "#a94040", "#7a2b2b", "#4f1b1b");
const CORD = ramp("#b4bf8c", "#8a9866", "#647046", "#414a2e");
const PEAS = ramp("#b9dd8a", "#86b85a", "#5c8a3a", "#3a5c24");
const TEAL = ramp("#8fd3c3", "#4aa594", "#2f786c", "#1c4d46");
const FADED = ramp("#f2a79a", "#d9796c", "#a8564c", "#703730");
const LEMON = ramp("#fff9c4", "#f6e27a", "#d1b94e", "#958230");
const ROCK = ramp("#cfc6b8", "#a39988", "#766d5f", "#4c463c");
const REDROCK = ramp("#e0a487", "#b8755a", "#87503c", "#573226");
const QUARTZ = ramp("#ffffff", "#e9e4f2", "#b9b0cc", "#857c9c");
const RUST = ramp("#e58a66", "#b9563c", "#863a28", "#562418");

function wagonBody(pen, lift = 0, aboard = true) {
  const b = -lift;                                                    // the body rides on its springs; the wheels do not
  // wheels and exhaust
  pen.rect(-47, -14, 16, 14, 1, RUBBER, 1); pen.rect(31, -14, 16, 14, 1, RUBBER, 1);
  pen.rect(-45, -12, 3, 10, 1.1, RUBBER, 0); pen.rect(33, -12, 3, 10, 1.1, RUBBER, 0);
  pen.rect(-36, -13 + b, 8, 3, 1.5, CHROME, 2);
  // tailgate
  pen.poly([[-50, -43 + b], [50, -43 + b], [52, -15 + b], [-52, -15 + b]], 2, RED, 1);
  pen.rect(-50, -43 + b, 100, 3, 2.1, RED, 0);                       // the top edge catches the light
  pen.poly([[36, -40 + b], [50, -40 + b], [52, -15 + b], [38, -15 + b]], 2.1, RED, 2);   // the right side falls into shade
  pen.rect(-51, -32 + b, 102, 6, 2.2, WOOD, 1);                      // the wood trim of a proper family wagon
  pen.rect(-51, -32 + b, 102, 1, 2.3, WOOD, 0); pen.rect(-51, -27 + b, 102, 1, 2.3, WOOD, 3);
  pen.rect(-49, -41 + b, 12, 8, 2.4, LAMP, 1); pen.rect(-49, -41 + b, 12, 2, 2.5, LAMP, 0); pen.rect(-49, -34 + b, 12, 1, 2.5, LAMP, 2);
  pen.rect(37, -41 + b, 12, 8, 2.4, LAMP, 1); pen.rect(37, -41 + b, 12, 2, 2.5, LAMP, 0); pen.rect(37, -34 + b, 12, 1, 2.5, LAMP, 2);
  pen.rect(-7, -38 + b, 14, 2, 2.4, CHROME, 1);                      // handle
  pen.rect(-12, -25 + b, 24, 8, 2.4, CREAM, 1); pen.rect(-12, -25 + b, 24, 1, 2.5, CREAM, 0);
  for (const x of [-9, -5, -1, 4, 8]) pen.rect(x, -23 + b, 2, 4, 2.6, RUBBER, 1);          // the number plate, unreadable at this distance
  // bumper
  pen.rect(-54, -18 + b, 108, 6, 3, CHROME, 1); pen.rect(-54, -18 + b, 108, 2, 3.1, CHROME, 0); pen.rect(-54, -13 + b, 108, 1, 3.1, CHROME, 3);
  // cabin and rear window
  pen.poly([[-47, -43 + b], [-40, -76 + b], [40, -76 + b], [47, -43 + b]], 2, RED, 1);
  pen.poly([[-47, -43 + b], [-40, -76 + b], [-36, -76 + b], [-43, -43 + b]], 2.1, RED, 0);
  pen.poly([[43, -43 + b], [36, -76 + b], [40, -76 + b], [47, -43 + b]], 2.1, RED, 2);
  pen.poly([[-41, -47 + b], [-36, -72 + b], [36, -72 + b], [41, -47 + b]], 2.2, GLASS, 1);
  pen.poly([[-33, -47 + b], [-24, -72 + b], [-14, -72 + b], [-23, -47 + b]], 2.3, GLASS, 0);   // a reflection across the glass
  pen.rect(-30, -56 + b, 22, 9, 2.4, GLASS, 3); pen.rect(8, -56 + b, 22, 9, 2.4, GLASS, 3);    // seat backs
  if (aboard) {
    pen.oval(-19, -60 + b, 7, 8, 2.5, GLASS, 3); pen.oval(18, -57 + b, 6, 6.5, 2.5, GLASS, 3); // Dad at the wheel, the Son beside him
    pen.rect(18, -65 + b, 9, 2, 2.5, GLASS, 3);                                                // the peak of a cap
  }
  // roof, rack and the holiday luggage
  pen.rect(-41, -79 + b, 82, 4, 2.2, RED, 0); pen.rect(-41, -76 + b, 82, 1, 2.3, RED, 2);
  pen.rect(-38, -82 + b, 76, 2, 2.3, CHROME, 2); pen.rect(-36, -84 + b, 2, 3, 2.3, CHROME, 1); pen.rect(34, -84 + b, 2, 3, 2.3, CHROME, 1);
  pen.rect(-31, -96 + b, 27, 14, 2.4, WOOD, 1); pen.rect(-31, -96 + b, 27, 2, 2.5, WOOD, 0); pen.rect(-31, -84 + b, 27, 2, 2.5, WOOD, 2);
  pen.rect(-25, -96 + b, 2, 14, 2.6, WOOD, 3); pen.rect(-12, -96 + b, 2, 14, 2.6, WOOD, 3); pen.rect(-21, -98 + b, 7, 2, 2.6, WOOD, 3);
  pen.rect(1, -92 + b, 25, 10, 2.4, COOLER, 1); pen.rect(1, -92 + b, 25, 2, 2.5, COOLER, 0); pen.rect(20, -90 + b, 6, 8, 2.5, COOLER, 2);
  pen.rect(0, -95 + b, 27, 4, 2.6, CREAM, 0); pen.rect(0, -92 + b, 27, 1, 2.7, CREAM, 2);
}

// ---------- the list ----------
export const props = {
  /** The wagon on the road. frame 1 is the body bouncing on its springs. */
  wagon: {
    frames: 2, fps: 4,
    draw(scale, frame) {
      const pen = new Pen([-58, -102, 58, 6], scale);
      pen.shadow(0, 56, 5);
      wagonBody(pen, frame ? 1 / Math.max(scale, 0.5) : 0);
      return pen.sf.finish();
    },
  },

  /** The wagon after its landing: nose-down in the sand, with a drift across the wheels. */
  wagonStuck: {
    frames: 1,
    draw(scale, frame, o) {
      const pen = new Pen([-62, -106, 62, 8], scale, -0.11, 7);
      wagonBody(pen, 0, false);                                       // nobody is in it now
      const sand = sandOf(o.palette), flat = new Pen([-62, -106, 62, 8], scale);
      flat.sf = pen.sf;                                               // the sand lies level, whatever the car is doing
      flat.shadow(4, 60, 5);
      flat.poly([[-60, 4], [-50, -9], [-28, -15], [-4, -12], [22, -17], [44, -10], [60, 4]], 5, sand, 1);
      flat.poly([[-50, -9], [-28, -15], [-4, -12], [22, -17], [30, -14], [-4, -9], [-30, -11]], 5.1, sand, 0);
      flat.poly([[-60, 4], [60, 4], [50, -2], [10, 0], [-40, -1]], 5.1, sand, 2);
      return pen.sf.clipBelow(pen.sf.oy + 4 * scale).finish();
    },
  },

  /** A stone fountain: a round basin, a pillar, a bowl, and water falling from it. */
  fountain: {
    frames: 4, fps: 5,
    draw(scale, frame, o) {
      const STONE = ramp("#fffdf6", "#e7ddc8", "#bcae92", "#887c64"), WATER = ramp("#e6f6fb", "#8fc8e6", "#4f93c9", "#2f6fb0");
      const pen = new Pen([-66, -84, 66, 6], scale);
      pen.shadow(2, 66, 6);
      // basin: a low drum, lit from the left
      pen.oval(0, -4, 60, 8, 1, STONE, 2);
      pen.rect(-60, -24, 120, 20, 1.1, STONE, 1);
      pen.rect(-60, -24, 22, 20, 1.2, STONE, 0); pen.rect(30, -24, 30, 20, 1.2, STONE, 2); pen.rect(50, -24, 10, 20, 1.3, STONE, 3);
      pen.oval(0, -24, 62, 9, 2, STONE, 0);                            // the rim
      pen.oval(0, -24, 55, 6.5, 2.1, WATER, 2);
      pen.oval(-6, -25, 44, 4.5, 2.2, WATER, 1);
      for (let i = 0; i < 5; i++) { const x = -38 + ((i * 19 + frame * 7) % 78); pen.rect(x, -25 + (i % 2), 5, 1, 2.3, WATER, 0); }
      // pillar and bowl
      pen.limb(0, -26, 0, -62, 6, 5, STONE, { z: 3 });
      pen.oval(0, -66, 24, 5, 4, STONE, 2); pen.oval(0, -69, 25, 5, 4.1, STONE, 0); pen.oval(0, -69, 20, 3.4, 4.2, WATER, 1);
      // water falling in four thin streams, flickering
      for (const [x, sway] of [[-21, 0], [-9, 1], [9, 2], [21, 3]]) {
        for (let y = -66; y < -26; y += 3) if ((y + frame + sway) % 4) pen.rect(x + (((y >> 1) + frame + sway) % 2 ? 0 : 0.5), y, 1.5, 2.4, 3.5, WATER, (y + frame) % 3 ? 0 : 1);
      }
      return pen.sf.finish();
    },
  },

  /** Reeds at the water's edge, moving a little in the wind. */
  reeds: {
    frames: 4, fps: 2.5,
    draw(scale, frame) {
      const STALK = ramp("#c6d17a", "#93a34d", "#657334", "#3f4a22"), HEAD = ramp("#b58a55", "#8a6238", "#634425", "#3f2a17");
      const pen = new Pen([-46, -70, 46, 5], scale);
      const lean = [0, 0.6, 1.2, 0.6][frame];
      for (let i = 0; i < 13; i++) {
        const x = -36 + i * 6 + ((i * 7) % 5), h = 36 + ((i * 13) % 26), bend = (((i * 5) % 7) - 3) * 1.3 + lean * (1 + (i % 3) * 0.5);
        const z = (i * 37) % 9;
        pen.limb(x, 0, x + bend, -h, 1.5, 0.9, STALK, { z });
        if (i % 3 !== 1) pen.limb(x + bend, -h + 1, x + bend * 1.18, -h - 9, 2.2, 1.4, HEAD, { z: z + 0.5 });
        else pen.limb(x + bend * 0.5, -h * 0.55, x + bend * 0.5 + 7, -h * 0.55 - 8, 1.1, 0.8, STALK, { z });      // a leaf
      }
      return pen.sf.finish();
    },
  },

  // ---------- home ----------
  /** The family computer on its desk. options.state: "offline", "login" or "map", with ".note" added while the sticky note is on the screen. */
  desk: {
    frames: 1,
    draw(scale, frame, o) {
      const state = String(o.state || "offline"), pen = new Pen([-52, -96, 52, 6], scale);
      pen.shadow(0, 50, 4);
      pen.rect(-46, -52, 92, 52, 0.5, OAK, 3);                               // the dark under the desk
      pen.rect(-46, -52, 30, 52, 1, OAK, 1); pen.rect(40, -52, 6, 52, 1, OAK, 2);
      for (const y of [-46, -31, -16]) { pen.rect(-43, y, 24, 12, 1.1, OAK, 0); pen.rect(-33, y + 5, 4, 2, 1.2, BRASS, 1); }
      pen.rect(-50, -57, 100, 6, 2, OAK, 0); pen.rect(-50, -52, 100, 1, 2.1, OAK, 2);
      // the monitor, its keyboard, a mug
      pen.rect(-5, -64, 10, 7, 3, CASE, 2); pen.rect(-14, -59, 28, 2, 3, CASE, 1);
      pen.rect(-28, -94, 56, 32, 3, CASE, 1); pen.rect(-28, -94, 56, 1, 3.1, CASE, 0);
      const glass = state.startsWith("map") ? PAPERMAP : state.startsWith("login") ? BLUESCREEN : DARKSCREEN;
      pen.rect(-25, -91, 50, 26, 3.2, glass, 1);
      if (state.startsWith("map")) { pen.rect(-25, -74, 22, 2, 3.3, PAPERMAP, 2); pen.rect(-4, -78, 12, 2, 3.3, PAPERMAP, 2); pen.rect(8, -82, 4, 4, 3.4, LAMP, 1); pen.rect(4, -76, 18, 7, 3.3, CREAM, 0); }
      else if (state.startsWith("login")) { pen.rect(-25, -91, 50, 4, 3.3, BLUESCREEN, 3); pen.rect(-12, -80, 24, 6, 3.3, CREAM, 0); pen.rect(-16, -71, 32, 1, 3.3, BLUESCREEN, 0); }
      else { pen.rect(-25, -91, 50, 4, 3.3, DARKSCREEN, 2); pen.rect(-3, -82, 6, 6, 3.3, DARKSCREEN, 0); pen.rect(-8, -73, 16, 1, 3.3, DARKSCREEN, 0); }
      if (state.endsWith(".note")) { pen.rect(18, -93, 9, 9, 3.6, STICKY, 1); pen.rect(18, -93, 9, 2, 3.7, STICKY, 2); pen.rect(20, -89, 5, 1, 3.7, STICKY, 3); }
      pen.rect(-20, -60, 40, 3, 3.4, CREAM, 2); pen.rect(-20, -60, 40, 1, 3.5, CREAM, 0);
      pen.rect(34, -65, 7, 8, 3.4, LAMP, 1); pen.rect(41, -63, 2, 4, 3.4, LAMP, 2);
      return pen.sf.finish();
    },
  },

  /** An upright piano, well looked after, with its stool. */
  piano: {
    frames: 1,
    draw(scale) {
      const pen = new Pen([-66, -118, 66, 6], scale);
      pen.shadow(0, 62, 4);
      pen.rect(-58, -96, 116, 96, 1, EBONY, 1); pen.rect(-58, -96, 10, 96, 1.1, EBONY, 0); pen.rect(44, -96, 14, 96, 1.1, EBONY, 2);
      pen.rect(-60, -100, 120, 5, 2, EBONY, 0); pen.rect(-60, -96, 120, 1, 2.1, EBONY, 3);
      pen.rect(-50, -90, 100, 28, 1.5, EBONY, 2); pen.rect(-50, -90, 100, 1, 1.6, EBONY, 3);          // the panel behind the music
      pen.rect(-26, -70, 52, 3, 2.4, EBONY, 0);                                                         // music desk
      pen.rect(-20, -88, 18, 18, 2.5, CREAM, 0); pen.rect(1, -88, 18, 18, 2.5, CREAM, 1);
      for (const y of [-84, -80, -76]) { pen.rect(-18, y, 14, 1, 2.6, RUBBER, 0); pen.rect(3, y, 14, 1, 2.6, RUBBER, 0); }
      pen.rect(-60, -60, 120, 7, 3, EBONY, 0); pen.rect(-60, -54, 120, 2, 3.1, EBONY, 3);             // the key bed
      pen.rect(-54, -59, 108, 5, 3.2, CREAM, 0); pen.rect(-54, -55, 108, 1, 3.3, CREAM, 2);
      for (let x = -54; x < 54; x += 4) pen.rect(x, -59, 0.6, 5, 3.3, CREAM, 2);
      for (let i = 0, x = -52; x < 52; x += 4, i++) if (i % 7 !== 2 && i % 7 !== 6) pen.rect(x + 1.2, -59, 2.2, 3, 3.4, RUBBER, 2);
      pen.rect(-58, -52, 7, 52, 3, EBONY, 0); pen.rect(51, -52, 7, 52, 3, EBONY, 2);                  // legs
      pen.rect(-50, -48, 100, 40, 1.5, EBONY, 2); pen.rect(-50, -48, 100, 1, 1.6, EBONY, 3);
      for (const x of [-9, -2, 5]) pen.rect(x, -5, 5, 2, 3, BRASS, 1);                               // pedals
      // a metronome and a small lamp on the lid
      pen.poly([[-44, -100], [-34, -100], [-37, -114], [-41, -114]], 2.5, OAK, 1); pen.rect(-39.6, -112, 1.2, 10, 2.6, BRASS, 0);
      pen.rect(34, -103, 10, 3, 2.5, BRASS, 2); pen.rect(38, -110, 2, 8, 2.5, BRASS, 1); pen.poly([[31, -110], [47, -110], [44, -117], [34, -117]], 2.6, SHADE, 0);
      // the stool
      pen.rect(-17, -36, 34, 6, 6, CUSHION, 1); pen.rect(-17, -36, 34, 2, 6.1, CUSHION, 0); pen.rect(-17, -31, 34, 1, 6.1, CUSHION, 3);
      pen.rect(-14, -30, 4, 30, 5.5, EBONY, 1); pen.rect(10, -30, 4, 30, 5.5, EBONY, 2); pen.rect(-12, -14, 24, 2, 5.4, EBONY, 2);
      return pen.sf.finish();
    },
  },

  /** The dining table, set for five. Two of the chairs have nobody coming to them. */
  table: {
    frames: 1,
    draw(scale) {
      const pen = new Pen([-90, -84, 90, 6], scale);
      pen.shadow(0, 84, 5);
      const chair = (x, z, tone) => { pen.rect(x - 11, -80, 22, 34, z, OAK, tone); pen.rect(x - 8, -76, 16, 4, z + 0.1, OAK, 3); pen.rect(x - 8, -68, 16, 4, z + 0.1, OAK, 3); pen.rect(x - 8, -60, 16, 4, z + 0.1, OAK, 3); };
      for (const x of [-52, 0, 52]) chair(x, 1, 2);                                                  // the far side
      pen.rect(-74, -42, 7, 42, 2, OAK, 2); pen.rect(67, -42, 7, 42, 2, OAK, 3);
      pen.rect(-82, -52, 164, 5, 3, CLOTH, 0); pen.rect(-82, -47, 164, 9, 3, CLOTH, 1); pen.rect(-82, -39, 164, 1, 3.1, CLOTH, 3);
      for (let x = -80; x < 80; x += 8) pen.rect(x, -40, 4, 2, 3.2, CLOTH, 1);                       // a scalloped edge
      // five places, a covered dish and a jug
      for (const x of [-62, -32, 32, 62, 0]) {
        if (x === 0) { pen.oval(0, -55, 15, 3, 4, CHROME, 1); pen.ball(0, -59, 12, 7, CHROME, { z: 4.2 }); pen.rect(-2, -68, 4, 3, 4.3, CHROME, 0); continue; }
        pen.oval(x, -54, 9, 2.4, 4, CREAM, 0); pen.oval(x, -54.4, 6, 1.5, 4.1, CREAM, 1);
        pen.oval(x - 1, -55, 3.4, 1.3, 4.2, x < 0 ? PEAS : OAK, 1); pen.oval(x + 2.5, -54.6, 2.2, 1, 4.2, LAMP, 1);
        pen.rect(x + 11, -60, 3, 6, 4.1, GLASS, 0);
      }
      pen.rect(-20, -66, 6, 12, 4.4, COOLER, 0); pen.rect(-14, -63, 2, 5, 4.4, COOLER, 1);
      // the near side: two chairs pulled out, waiting
      for (const x of [-42, 44]) {
        pen.rect(x - 12, -74, 24, 36, 6, OAK, 1); pen.rect(x - 12, -74, 24, 2, 6.1, OAK, 0);
        for (const y of [-69, -60, -51]) pen.rect(x - 9, y, 18, 5, 6.1, OAK, 3);
        pen.rect(x - 13, -38, 26, 5, 6.2, OAK, 0); pen.rect(x - 12, -33, 4, 33, 6, OAK, 2); pen.rect(x + 8, -33, 4, 33, 6, OAK, 3);
      }
      return pen.sf.finish();
    },
  },

  /** Dad's armchair, and the lamp he reads by. It has his shape. */
  armchair: {
    frames: 1,
    draw(scale) {
      const pen = new Pen([-46, -128, 64, 6], scale);
      pen.shadow(4, 52, 5);
      pen.rect(49, -112, 2, 112, 0.5, BRASS, 2); pen.oval(50, -2, 9, 2.5, 0.6, BRASS, 2);
      pen.poly([[38, -110], [62, -110], [57, -126], [43, -126]], 0.7, SHADE, 0); pen.poly([[52, -110], [62, -110], [57, -126], [51, -126]], 0.8, SHADE, 1);
      pen.oval(0, -78, 30, 9, 1, CORD, 1); pen.rect(-30, -78, 60, 52, 1, CORD, 1); pen.rect(-30, -78, 12, 52, 1.1, CORD, 0); pen.rect(18, -78, 12, 52, 1.1, CORD, 2);
      for (const x of [-12, 0, 12]) pen.rect(x, -80, 1, 46, 1.2, CORD, 2);                           // corduroy
      pen.rect(-24, -38, 48, 14, 2, CORD, 0); pen.oval(0, -33, 15, 4, 2.1, CORD, 2);                  // the seat, with a dent in it
      pen.rect(-32, -26, 64, 20, 2, CORD, 2); pen.rect(-32, -26, 64, 2, 2.1, CORD, 1);
      pen.rect(-40, -50, 14, 44, 3, CORD, 0); pen.oval(-33, -50, 7, 4, 3.1, CORD, 0); pen.rect(-40, -50, 3, 44, 3.2, CORD, 1);
      pen.rect(26, -50, 14, 44, 3, CORD, 2); pen.oval(33, -50, 7, 4, 3.1, CORD, 1);
      pen.rect(-36, -6, 6, 6, 2, OAK, 2); pen.rect(30, -6, 6, 6, 2, OAK, 3);
      pen.rect(-39, -56, 13, 3, 3.4, CREAM, 0); pen.rect(-37, -55, 9, 1, 3.5, RUBBER, 0);            // the crossword, folded on the arm
      return pen.sf.finish();
    },
  },

  // ---------- Nevada ----------
  /** Mom's car: small, tidy, and parked straight. */
  car: {
    frames: 1,
    draw(scale) {
      const pen = new Pen([-76, -64, 76, 6], scale);
      pen.shadow(0, 70, 5);
      pen.poly([[-48, -34], [-34, -58], [24, -58], [46, -34]], 2, TEAL, 1); pen.poly([[-34, -58], [24, -58], [26, -56], [-33, -56]], 2.1, TEAL, 0);
      pen.poly([[-41, -35], [-31, -54], [-5, -54], [-5, -35]], 2.2, GLASS, 1); pen.poly([[0, -35], [0, -54], [22, -54], [39, -35]], 2.2, GLASS, 1);
      pen.poly([[-36, -35], [-29, -52], [-22, -52], [-29, -35]], 2.3, GLASS, 0); pen.poly([[5, -35], [5, -52], [11, -52], [11, -35]], 2.3, GLASS, 0);
      pen.poly([[-70, -12], [-70, -30], [-62, -35], [60, -35], [70, -28], [72, -12]], 2, TEAL, 1);
      pen.poly([[-70, -30], [-62, -35], [60, -35], [70, -28], [70, -26], [60, -32], [-62, -32], [-70, -27]], 2.1, TEAL, 0);
      pen.rect(-70, -18, 142, 7, 2.1, TEAL, 2); pen.rect(-70, -12, 142, 2, 2.2, TEAL, 3);
      pen.rect(-3, -34, 1, 22, 2.3, TEAL, 3); pen.rect(-46, -34, 1, 20, 2.3, TEAL, 3); pen.rect(-12, -29, 6, 2, 2.4, CHROME, 0); pen.rect(30, -29, 6, 2, 2.4, CHROME, 0);
      pen.rect(-74, -16, 7, 5, 2.5, CHROME, 1); pen.rect(67, -16, 8, 5, 2.5, CHROME, 1);
      pen.rect(64, -29, 6, 5, 2.4, SHADE, 0); pen.rect(-70, -29, 4, 6, 2.4, LAMP, 1);
      for (const x of [-42, 42]) { pen.oval(x, -13, 14, 13, 2.6, TEAL, 3); pen.oval(x, -10, 11, 10, 3, RUBBER, 1); pen.oval(x, -10, 5, 5, 3.1, CHROME, 1); pen.oval(x - 1, -11, 2, 2, 3.2, CHROME, 0); }
      return pen.sf.finish();
    },
  },

  /** The old-timer's stand: lemonade, rocks, a painted board, and an umbrella that has seen every summer since. */
  stand: {
    frames: 1,
    draw(scale) {
      const pen = new Pen([-112, -150, 52, 6], scale);
      pen.shadow(-10, 56, 4);
      // the umbrella
      pen.rect(-51, -132, 2.5, 132, 0.5, CHROME, 2);
      const rim = [[-108, -112], [-80, -118], [-50, -120], [-20, -118], [8, -112]], top = [-50, -146];
      for (let i = 0; i + 1 < rim.length; i++) pen.poly([top, rim[i], rim[i + 1]], 1 + i * 0.01, i % 2 ? CREAM : FADED, i < 2 ? 0 : 1);
      for (let i = 0; i + 1 < rim.length; i++) pen.poly([rim[i], rim[i + 1], [rim[i + 1][0], rim[i + 1][1] + 5], [rim[i][0], rim[i][1] + 5]], 1.2, i % 2 ? CREAM : FADED, 2);
      // the table
      pen.limb(-36, -34, -22, 0, 1.4, 1.4, CHROME, { z: 1.5 }); pen.limb(-22, -34, -36, 0, 1.4, 1.4, CHROME, { z: 1.4 });
      pen.limb(24, -34, 38, 0, 1.4, 1.4, CHROME, { z: 1.5 }); pen.limb(38, -34, 24, 0, 1.4, 1.4, CHROME, { z: 1.4 });
      pen.rect(-42, -39, 86, 5, 2, OAK, 0); pen.rect(-42, -35, 86, 1, 2.1, OAK, 3);
      // lemonade, cups, rocks
      pen.rect(-34, -58, 14, 19, 3, LEMON, 1); pen.rect(-34, -58, 14, 4, 3.1, CREAM, 1); pen.rect(-32, -52, 3, 9, 3.1, LEMON, 0); pen.rect(-20, -54, 3, 9, 3, CREAM, 2);
      pen.rect(-14, -48, 7, 9, 3, CREAM, 0); pen.rect(-14, -45, 7, 2, 3.1, LAMP, 1); pen.rect(-6, -46, 6, 7, 3, CREAM, 1);
      pen.ball(12, -43, 7, 5, ROCK, { z: 3 }); pen.ball(25, -44, 8, 6, REDROCK, { z: 3.1 }); pen.ball(37, -42, 5, 4, ROCK, { z: 3 }); pen.ball(19, -41, 3, 2.4, QUARTZ, { z: 3.3 });
      // the board: three lines of paint
      pen.rect(-30, -30, 62, 24, 4, CREAM, 1); pen.rect(-30, -30, 62, 1, 4.1, CREAM, 0); pen.rect(-30, -7, 62, 1, 4.1, CREAM, 3);
      pen.rect(-24, -26, 34, 3, 4.2, LAMP, 2); pen.rect(14, -26, 10, 3, 4.2, LAMP, 2);
      pen.rect(-24, -19, 22, 3, 4.2, RUBBER, 0); pen.rect(2, -19, 10, 3, 4.2, RUBBER, 0);
      pen.rect(-24, -12, 28, 3, 4.2, RUBBER, 0); pen.rect(8, -12, 18, 3, 4.2, LAMP, 2);
      return pen.sf.finish();
    },
  },

  /** A gas pump from before the road was moved. Nothing has come out of it for years. */
  pump: {
    frames: 1,
    draw(scale) {
      const pen = new Pen([-22, -112, 26, 6], scale);
      pen.shadow(0, 18, 3);
      pen.rect(-14, -6, 28, 6, 1, CHROME, 3);
      pen.rect(-12, -76, 24, 70, 1, RUST, 1); pen.rect(-12, -76, 5, 70, 1.1, RUST, 0); pen.rect(6, -76, 6, 70, 1.1, RUST, 2);
      pen.rect(-8, -68, 16, 16, 1.2, CREAM, 1); pen.rect(-6, -64, 12, 1, 1.3, RUBBER, 0); pen.rect(-6, -60, 12, 1, 1.3, RUBBER, 0); pen.rect(-6, -56, 8, 1, 1.3, RUBBER, 0);
      pen.rect(-9, -42, 18, 2, 1.2, RUST, 3); pen.rect(-4, -84, 8, 8, 1, CHROME, 2);
      pen.ball(0, -95, 11, 11, CREAM, { z: 2 }); pen.rect(-7, -97, 14, 4, 2.4, LAMP, 2);
      pen.limb(12, -58, 20, -40, 1.6, 1.6, RUBBER, { z: 1.5 }); pen.limb(20, -40, 16, -14, 1.6, 1.6, RUBBER, { z: 1.5 }); pen.rect(12, -18, 6, 8, 1.6, CHROME, 1);
      return pen.sf.finish();
    },
  },
};

/** The ground of the current era as a material, so drifts and mounds match the scene. */
function sandOf(palette) {
  const p = palette || {};
  return ramp(p.g1 || "#dbb46b", p.g2 || "#c79b55", p.g3 || "#a97f42", p.line || "#3b2616");
}
