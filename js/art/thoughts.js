// ENGINE-17: thought pictures. A lead who cannot talk thinks in pictures: a line may carry a third element, a picture name
// or a list of one to three (["ranger", "...", "pie"], ["ranger", "...", ["piepan", "plus", "banjo"]]), and when it is said
// the speaker gets a thought bubble over his head instead of the words: a white cloud with a dark outline, a thin rim in
// his own colour and two or three small puffs trailing down toward his head, and in it the pictures side by side
// (js/engine/dialogue.js says it; docs/DESIGN.md, section 7, "Thought pictures").
//
// Every picture is pixel art drawn by code, 24 x 24, in the game's pixel style as the people and the inventory's small
// drawn things are: hard edges, flat colour, one darker tone on the side turned from the light (the light from the upper
// left, as on every person), a dark line round the thing so it reads on any ground, a highlight or two. The colours are a
// few of the interface's own (css/tokens.css: ink, cream, white, the papyrus, the time cyan and violet, the family's red,
// yellow and blue) and of the kit's drawn icons (js/art/kit.js: the reed's olive, the coin's silver), each with one darker
// tone: never the scenes' paints (js/art/look.js), since a bubble belongs to the interface, as the portraits do.
//
// The names are fixed (briefs: OFFICE-17.md). A name not in the set is said in the console, once, and shows `question`.
// Nothing here knows who thinks what: that is the lines' (js/content/lines/*.en.js) and the scenes'.

export const SIZE = 24;                       // a picture's side, in picture pixels
export const THOUGHTS = ["question", "idea", "heart", "no", "plus", "arrow", "up", "down", "joe", "pie", "piepan", "banjo",
  "banjo-broken", "receipt", "bottlecap", "key", "door", "hole", "fan", "hot", "sun", "zzz", "eye", "shiny", "music", "clock",
  "paper", "cheeseburger", "pickle", "water", "suit", "opal", "trash", "wingnut", "lamp", "peanuts", "switch", "chair", "hand"];

// ---------------------------------------------------------------- the palette (the interface's own colours)
const C = {
  ink: "#1f130a", white: "#ffffff", cream: "#f6e3b8", papyrus: "#d6ae62", papyrusHi: "#e2be72", papyrusLo: "#c5964a",
  cyan: "#5ef2ff", violet: "#b58cff", red: "#c85a43", pink: "#ff9ec4", yellow: "#ffd34d", note: "#ffe36b", noteLo: "#d9b83c",
  blue: "#7fe3ff", olive: "#7a8a3c", oliveLo: "#4d5a22", silver: "#d4d8de", silverHi: "#f4f6f8", silverLo: "#8e949c",
};
const hex = (c) => [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)];
const mix = (a, b, k) => { const x = hex(a), y = hex(b); return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * k).toString(16).padStart(2, "0")).join(""); };
/** The darker tone of a colour: the side turned from the light (toward the ink, as the rig's shade is a darker tone of the thing itself). */
const dark = (c, k = 0.32) => mix(c, C.ink, k);
const brown = mix(C.papyrusLo, C.ink, 0.45);          // wood in shade, a patty: the papyrus gone dark
const steel = mix(C.silverLo, C.ink, 0.35);           // the darkest metal (a hub, a hinge)
export const PALETTE = { ...C, brown, steel };

// ---------------------------------------------------------------- a small pixel canvas, for drawing the pictures
class Pix {
  constructor(w = SIZE, h = SIZE) { this.w = w; this.h = h; this.c = new Array(w * h).fill(null); }
  in(x, y) { return x >= 0 && y >= 0 && x < this.w && y < this.h; }
  get(x, y) { return this.in(x, y) ? this.c[y * this.w + x] : null; }
  set(x, y, col) { x = Math.round(x); y = Math.round(y); if (this.in(x, y)) this.c[y * this.w + x] = col; return this; }
  /** Every pixel whose middle passes the test gets the colour (null: cleared). */
  each(test, col) { for (let y = 0; y < this.h; y++) for (let x = 0; x < this.w; x++) if (test(x + 0.5, y + 0.5, x, y)) this.c[y * this.w + x] = col; return this; }
  rect(x, y, w, h, col) { return this.each((px, py) => px > x && px < x + w && py > y && py < y + h, col); }
  disc(cx, cy, r, col) { return this.each((px, py) => (px - cx) ** 2 + (py - cy) ** 2 <= r * r, col); }
  ell(cx, cy, rx, ry, col, turn = 0) {
    const c = Math.cos(turn), s = Math.sin(turn);
    return this.each((px, py) => { const dx = px - cx, dy = py - cy, u = dx * c + dy * s, v = -dx * s + dy * c; return (u / rx) ** 2 + (v / ry) ** 2 <= 1; }, col);
  }
  ring(cx, cy, r, w, col) { return this.each((px, py) => { const d = Math.hypot(px - cx, py - cy); return d <= r && d > r - w; }, col); }
  /** A line `t` pixels thick from (x0, y0) to (x1, y1). */
  line(x0, y0, x1, y1, col, t = 1) {
    const dx = x1 - x0, dy = y1 - y0, L = dx * dx + dy * dy || 1;
    return this.each((px, py) => { const k = Math.max(0, Math.min(1, ((px - x0) * dx + (py - y0) * dy) / L)); return Math.hypot(px - x0 - k * dx, py - y0 - k * dy) <= t / 2; }, col);
  }
  poly(pts, col) {
    return this.each((px, py) => {
      let inside = false;
      for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
        const [xi, yi] = pts[i], [xj, yj] = pts[j];
        if ((yi > py) !== (yj > py) && px < xi + ((py - yi) / (yj - yi)) * (xj - xi)) inside = !inside;
      }
      return inside;
    }, col);
  }
  /** Rows of characters, each standing for a colour (a space or a dot for none), put down with their top left at (x, y). */
  grid(rows, keys, x = 0, y = 0) {
    rows.forEach((row, j) => [...row].forEach((ch, i) => { if (keys[ch]) this.set(x + i, y + j, keys[ch]); }));
    return this;
  }
  /** Recolour the pixels that already have colour and pass the test: the side turned from the light, a highlight. */
  tone(test, col, only = null) {
    for (let y = 0; y < this.h; y++) for (let x = 0; x < this.w; x++) {
      const v = this.c[y * this.w + x];
      if (v && (!only || [].concat(only).includes(v)) && test(x + 0.5, y + 0.5, x, y)) this.c[y * this.w + x] = col;
    }
    return this;
  }
  /** The dark line round the thing: every clear pixel beside one with colour (side by side, not corner to corner). */
  outline(col = C.ink) {
    const add = [];
    for (let y = 0; y < this.h; y++) for (let x = 0; x < this.w; x++) {
      if (this.get(x, y)) continue;
      if (this.get(x - 1, y) || this.get(x + 1, y) || this.get(x, y - 1) || this.get(x, y + 1)) add.push([x, y]);
    }
    for (const [x, y] of add) this.set(x, y, col);
    return this;
  }
  canvas() {
    const cv = document.createElement("canvas");
    cv.width = this.w; cv.height = this.h;
    const ctx = cv.getContext("2d"), img = ctx.createImageData(this.w, this.h);
    this.c.forEach((v, i) => { if (!v) return; const [r, g, b] = hex(v); img.data.set([r, g, b, 255], i * 4); });
    ctx.putImageData(img, 0, 0);
    return cv;
  }
}

// ---------------------------------------------------------------- the pictures
// Each draws on a fresh 24 x 24 Pix. The light is from the upper left: the side away from it takes the darker tone.
const lowerRight = (cx, cy, k = 0) => (x, y) => (x - cx) + (y - cy) > k;
const I = { "#": C.ink };                          // the key for a glyph drawn in ink

const DRAW = {
  question(p) {
    p.grid([
      "....######....",
      "...########...",
      "..###....###..",
      "..###....###..",
      "..........###.",
      ".........###..",
      "........###...",
      ".......###....",
      "......###.....",
      "......###.....",
      "..............",
      "......###.....",
      "......###.....",
    ].map((r) => r.replace(/\./g, " ")), I, 5, 4);
  },
  idea(p) {
    p.disc(12, 9.5, 6.4, C.note).poly([[7.6, 12], [16.4, 12], [14.6, 16.5], [9.4, 16.5]], C.note);
    p.tone(lowerRight(12, 9.5, 2.5), C.noteLo, C.note);
    p.rect(8.6, 16.4, 6.8, 1.4, C.silver).rect(8.6, 17.6, 6.8, 1.2, C.silverLo).rect(8.6, 18.6, 6.8, 1.2, C.silver).rect(9.8, 19.6, 4.4, 1.6, steel);
    p.set(9, 6, C.white).set(9, 7, C.white).set(10, 5, C.white).set(9, 8, C.white);
    p.line(11, 13, 11, 16, C.noteLo).line(13, 13, 13, 16, C.noteLo);
    p.outline();
    for (const [x, y] of [[2, 9], [3, 3], [12, 0], [20, 3], [21, 9]]) p.set(x, y, C.noteLo);     // the light it gives: a short ray each way
    p.set(1, 9, C.noteLo).set(22, 9, C.noteLo).set(2, 2, C.noteLo).set(21, 2, C.noteLo);
  },
  heart(p) {
    p.disc(8, 9, 5.2, C.red).disc(16, 9, 5.2, C.red).poly([[3, 10.5], [21, 10.5], [12, 20.5]], C.red);
    p.tone(lowerRight(12, 10, 3.5), dark(C.red), C.red);
    p.set(6, 6, C.pink).set(7, 6, C.pink).set(5, 7, C.pink).set(5, 8, C.pink).set(6, 7, C.white);
    p.outline();
  },
  no(p) {
    p.ring(12, 12, 10, 3, C.red).line(5.8, 5.8, 18.2, 18.2, C.red, 3.2);
    p.tone((x, y) => x + y > 26, dark(C.red), C.red);
    p.outline();
  },
  plus(p) { p.rect(4, 10, 16, 4, C.ink).rect(10, 4, 4, 16, C.ink); },
  arrow(p) { p.rect(3, 10, 11, 4, C.ink).poly([[12.5, 4.5], [21, 12], [12.5, 19.5]], C.ink); },
  up(p) { p.rect(10, 10, 4, 11, C.ink).poly([[4.5, 11.5], [12, 3], [19.5, 11.5]], C.ink); },
  down(p) { p.rect(10, 3, 4, 11, C.ink).poly([[4.5, 12.5], [12, 21], [19.5, 12.5]], C.ink); },
  joe(p) {                                         // a straw hat with a dent in the crown
    p.ell(12, 16.5, 11, 3.6, C.papyrus);                                              // the brim
    p.poly([[6, 15.5], [6.6, 7], [9, 5], [12, 7.4], [15, 5], [17.4, 7], [18, 15.5]], C.papyrusHi);   // the crown, pinched at the top
    p.rect(6, 12.2, 12, 2.4, C.red);                                                  // the band
    p.tone((x, y) => x > 13.5 && y < 15.5, C.papyrus, C.papyrusHi);
    p.tone((x, y) => x > 13.5, dark(C.red), C.red);
    p.tone((x, y) => y > 17.2, C.papyrusLo, C.papyrus);                               // the brim's underside
    for (const [x, y] of [[8, 8], [10, 10], [8, 11], [15, 9], [16, 11], [4, 17], [19, 16], [12, 18]]) p.set(x, y, C.papyrusLo);     // the straw's weave
    p.set(12, 7, C.papyrusLo).set(12, 8, C.papyrusLo);                                // the dent
    p.outline();
  },
  pie(p) {
    p.poly([[3, 13.5], [21, 13.5], [19, 19.5], [5, 19.5]], C.silver);                // the tin
    p.tone((x) => x > 15, C.silverLo, C.silver);
    p.ell(12, 12.5, 9.6, 5.2, C.papyrusHi);                                          // the crust, domed
    p.tone(lowerRight(12, 12, 2), C.papyrus, C.papyrusHi);
    for (let x = 4; x <= 20; x += 2) p.set(x, 15.2 + (x % 4 === 0 ? 0 : 0.6), C.papyrusLo);     // the crimped edge
    p.line(8, 9.5, 11, 15, C.papyrusLo).line(12, 8, 15, 15, C.papyrusLo).line(9, 14, 15.5, 9.2, C.papyrusLo);     // the lattice
    p.set(8, 10, C.cream).set(9, 9, C.cream).set(7, 11, C.cream);
    p.outline();
  },
  piepan(p) {
    p.ell(12, 13, 10.6, 6.2, C.silver);
    p.ell(12, 13.6, 7.6, 4, C.silverLo);
    p.ell(12.6, 14.2, 6.4, 3, dark(C.silverLo, 0.2));
    p.tone((x, y) => y < 9.5 && x < 13, C.silverHi, C.silver);
    for (let a = 0; a < Math.PI * 2; a += Math.PI / 9) p.set(12 + Math.cos(a) * 9.7, 13 + Math.sin(a) * 5.4, C.silverHi);     // the crimped rim
    p.set(7, 12, C.silverHi).set(8, 11, C.silverHi);
    p.outline();
  },
  banjo(p) { banjo(p, true); },
  "banjo-broken": (p) => banjo(p, false),
  receipt(p) {
    const teeth = [[6, 19], [7, 20.5], [8, 19], [9, 20.5], [10, 19], [11, 20.5], [12, 19], [13, 20.5], [14, 19], [15, 20.5], [16, 19], [17, 20.5], [18, 19]];
    p.poly([[6, 2.5], [18, 2.5], ...teeth.reverse()], C.white);
    p.tone((x) => x > 15.5, C.cream, C.white);
    p.rect(7.6, 4.6, 8.8, 1.2, C.ink);                                               // RECEIVED
    for (const [y, w] of [[7.6, 8], [9.6, 6], [11.6, 7.4], [13.6, 5]]) p.rect(7.6, y, w, 0.9, C.silverLo);
    p.rect(12.4, 15.4, 4, 1.4, C.ink);                                               // the total
    p.disc(9.4, 16, 1.7, C.red);                                                     // a stamp
    p.outline();
  },
  bottlecap(p) {                                   // the best one there is: a crimped red cap with a gold star
    for (let k = 0; k < 18; k++) { const a = (k * Math.PI) / 9; p.disc(12 + Math.cos(a) * 8.4, 12 + Math.sin(a) * 8.4, 1.7, C.red); }   // the crimp
    p.disc(12, 12, 8.6, C.red);
    p.tone(lowerRight(12, 12, 4.6), dark(C.red), C.red);
    p.ring(12, 12, 6.4, 1, dark(C.red, 0.2));
    p.disc(12, 12, 5.4, mix(C.red, C.pink, 0.35));
    const star = []; for (let k = 0; k < 10; k++) { const a = -Math.PI / 2 + (k * Math.PI) / 5, r = k % 2 ? 1.9 : 4.4; star.push([12 + Math.cos(a) * r, 12.3 + Math.sin(a) * r]); }
    p.poly(star, C.yellow).tone(lowerRight(12, 12.3, 1.5), C.noteLo, C.yellow);
    p.set(6, 7, C.pink).set(7, 6, C.pink).set(6, 8, C.white);
    p.outline();
  },
  key(p) {
    p.disc(7.4, 12, 5, C.note);
    p.rect(11, 10.6, 10.4, 2.8, C.note).rect(15.4, 13, 2, 3.4, C.note).rect(18.6, 13, 2.2, 4.6, C.note);
    p.tone((x, y) => y > 12.2, C.noteLo, C.note);
    p.disc(6.8, 11.6, 1.9, null);                                                   // the hole in the bow
    p.set(5, 9, C.white).set(6, 8, C.white);
    p.outline();
  },
  door(p) {
    p.rect(5.5, 1.5, 13, 21, C.papyrusLo);
    p.tone((x) => x > 15, brown, C.papyrusLo);
    p.rect(7.5, 3.5, 9, 7, dark(C.papyrusLo, 0.18)).rect(7.5, 12.5, 9, 7.5, dark(C.papyrusLo, 0.18));      // the panels
    p.rect(8.5, 4.5, 1, 5, C.papyrus).rect(8.5, 13.5, 1, 5.5, C.papyrus);
    p.disc(15.5, 12, 1.4, C.note).set(15, 11, C.white);
    p.outline();
  },
  hole(p) {                                        // a door in time: rings of the time colours round a white heart
    p.disc(12, 12, 10.8, C.ink);
    p.ring(12, 12, 10.8, 2.2, C.cyan).ring(12, 12, 7.8, 1.8, C.violet).ring(12, 12, 5.2, 1.8, C.cyan).disc(12, 12, 2.4, C.white);
    p.set(9, 3, C.white).set(4, 9, C.white);
    p.outline();
  },
  fan(p) {
    for (const a of [-Math.PI / 2, Math.PI / 6, (5 * Math.PI) / 6]) {
      const cx = 12 + Math.cos(a) * 5.6, cy = 12.4 + Math.sin(a) * 5.6;
      p.ell(cx, cy, 5.6, 3.3, C.silver, a + 0.35);
    }
    p.tone(lowerRight(12, 12.4, 1), C.silverLo, C.silver);
    p.disc(12, 12.4, 3, steel).set(11, 11, C.silverLo);
    p.outline();
  },
  hot(p) {                                         // a thermometer, red to the top
    p.rect(9.6, 1.6, 4.8, 16, C.white).disc(12, 19, 4.2, C.white);
    p.disc(12, 19, 3, C.red).rect(11, 3.2, 2, 15, C.red);
    p.tone((x) => x > 12.4, dark(C.red), C.red);
    p.tone((x) => x > 13.4, C.cream, C.white);
    p.set(10.6, 18, C.pink);
    p.outline();
    for (const y of [4, 7, 10, 13]) p.set(16, y, C.ink).set(17, y, C.ink);          // the marks up its side
  },
  sun(p) {
    for (let k = 0; k < 8; k++) {
      const a = (k * Math.PI) / 4, c = Math.cos(a), s = Math.sin(a);
      p.line(12 + c * 7.4, 12 + s * 7.4, 12 + c * 10.4, 12 + s * 10.4, C.noteLo, k % 2 ? 2 : 2.6);
    }
    p.disc(12, 12, 6.2, C.yellow);
    p.tone(lowerRight(12, 12, 3), C.noteLo, C.yellow);
    p.set(9, 8, C.white).set(8, 9, C.white).set(10, 8, C.note).set(8, 10, C.note);
    p.outline();
  },
  zzz(p) {
    const Z = (x, y, s, t) => { p.rect(x, y, s, t, C.ink).rect(x, y + s - t, s, t, C.ink).line(x + s - t / 2, y + t, x + t / 2, y + s - t, C.ink, t + 0.2); };
    Z(2, 12, 9, 2.2); Z(11, 6, 7, 2); Z(17.4, 1.6, 5, 1.6);
  },
  eye(p) {
    p.poly([[1.5, 12], [6, 7], [12, 5.4], [18, 7], [22.5, 12], [18, 16.8], [12, 18.6], [6, 16.8]], C.white);
    p.disc(12, 12, 5, C.olive).tone(lowerRight(12, 12, 1.5), C.oliveLo, C.olive);
    p.disc(12, 12, 2.3, C.ink).set(10, 10, C.white).set(11, 10, C.white).set(10, 11, C.white);
    p.outline();
    p.line(4, 8.6, 12, 4.6, C.ink, 1.4).line(12, 4.6, 20, 8.6, C.ink, 1.4);           // the upper lid, heavier
  },
  shiny(p) {
    p.poly([[12, 1.5], [14, 10], [22.5, 12], [14, 14], [12, 22.5], [10, 14], [1.5, 12], [10, 10]], C.note);
    p.poly([[12, 5.5], [13, 11], [18.5, 12], [13, 13], [12, 18.5], [11, 13], [5.5, 12], [11, 11]], C.white);
    p.outline();
    p.set(19, 4, C.noteLo).set(18, 5, C.note).set(20, 5, C.note).set(19, 6, C.noteLo).set(19, 5, C.white);   // a small one beside it
  },
  music(p) {
    p.ell(6.8, 18, 3.6, 2.6, C.ink, -0.35).ell(16.8, 16, 3.6, 2.6, C.ink, -0.35);
    p.rect(9.2, 4.6, 1.8, 13.4, C.ink).rect(19.2, 2.6, 1.8, 13.4, C.ink);
    p.poly([[9.2, 4.6], [21, 2], [21, 5.4], [9.2, 8]], C.ink);
  },
  clock(p) {                                       // a wall clock, at a quarter to six (the minute the sky opened)
    p.disc(12, 12, 10.6, C.silver).tone(lowerRight(12, 12, 4), C.silverLo, C.silver);
    p.disc(12, 12, 8.4, C.cream);
    for (let k = 0; k < 12; k++) { const a = (k * Math.PI) / 6; p.set(12 + Math.sin(a) * 7.2 - 0.5, 12 - Math.cos(a) * 7.2 - 0.5, k % 3 ? C.papyrusLo : C.ink); }
    p.line(12, 12, 12.5, 17, C.ink, 1.6);                                            // the hour hand, a little short of six
    p.line(12, 12, 5.6, 10.6, C.ink, 1.1);                                           // the minute hand, at forty-seven
    p.disc(12, 12, 1.2, C.red);
    p.outline();
  },
  paper(p) {
    p.poly([[5, 2], [15, 2], [19, 6], [19, 22], [5, 22]], C.white);
    p.poly([[15, 2], [15, 6], [19, 6]], C.cream).set(15, 6, C.papyrusHi);             // the corner folded over
    p.tone((x) => x > 16, C.cream, C.white);
    p.rect(7, 4, 6.4, 1.6, C.ink);
    for (const [y, w] of [[8, 10], [10.4, 9], [12.8, 10], [15.2, 7], [17.6, 9.4]]) p.rect(7, y, w, 1, C.silverLo);
    p.outline();
  },
  cheeseburger(p) {
    p.ell(12, 11.4, 9.4, 6.4, C.papyrusHi).each((x, y) => y > 11.4, null);          // the top of the bun (the lower half of the oval cleared)
    p.tone(lowerRight(12, 9, 3.2), C.papyrus, C.papyrusHi);
    for (const [x, y] of [[8, 7], [12, 6], [15, 8], [10, 9], [17, 6]]) p.set(x, y, C.cream);     // its seeds
    p.rect(2.4, 11.2, 19.2, 2.2, C.olive).tone((x) => x > 17, C.oliveLo, C.olive);   // the lettuce
    p.rect(3, 14.4, 18, 2.6, brown);                                                  // the patty
    p.poly([[3, 13.2], [21, 13.2], [18.6, 16.6], [16, 14], [12.6, 17], [10.2, 14], [7, 16.4], [3, 14]], C.yellow);   // the cheese, dripping
    p.rect(3.5, 17, 17, 4, C.papyrusLo).tone((x) => x > 16, brown, C.papyrusLo);    // the bottom of the bun
    p.outline();
  },
  pickle(p) {
    p.ell(12, 12, 10.2, 4.8, C.olive, -0.62);
    p.tone((x, y) => (x - 12) * 0.58 + (y - 12) * 0.81 > 1.4, C.oliveLo, C.olive);
    for (const [x, y] of [[8, 13], [11, 10], [14, 9], [16, 7], [9, 16], [13, 14], [17, 11]]) p.set(x, y, mix(C.olive, C.note, 0.45));    // its bumps
    p.set(6, 14, C.cream).set(7, 13, mix(C.olive, C.white, 0.5));
    p.outline();
  },
  water(p) {
    p.disc(12, 15, 6.6, C.blue).poly([[6.4, 13], [12, 2], [17.6, 13]], C.blue);
    p.tone(lowerRight(12, 15, 2.4), dark(C.blue, 0.3), C.blue);
    p.set(9, 13, C.white).set(9, 14, C.white).set(10, 12, C.white).set(9, 15, C.white).set(11, 9, C.white);
    p.outline();
  },
  suit(p) {                                        // a face in black sunglasses, and a gray suit's collar
    p.poly([[3, 23], [5, 19.6], [19, 19.6], [21, 23]], C.silverLo).poly([[10, 19.6], [14, 19.6], [12, 23]], C.white).rect(11.2, 20.6, 1.6, 2.4, C.ink);
    p.ell(12, 11.4, 6.2, 7.6, C.cream).tone((x) => x > 14.6, C.papyrusHi, C.cream);
    p.ell(12, 5.6, 6.4, 3, steel).rect(5.6, 5.6, 12.8, 1.8, steel);                  // the hair, short
    p.rect(5.4, 9.4, 13.2, 1.4, C.ink).rect(6, 9.6, 5, 3.4, C.ink).rect(13, 9.6, 5, 3.4, C.ink);     // the sunglasses
    p.set(7, 10, C.white).set(14, 10, C.white);
    p.rect(10, 15.6, 4, 1, dark(C.papyrusHi, 0.3));                                  // a straight mouth, on duty
    p.outline();
  },
  opal(p) {                                        // half-moon reading glasses, on a beaded chain
    const glass = mix(C.blue, C.white, 0.72), gold = C.noteLo;
    for (let k = 0; k <= 18; k++) {                                                  // the chain, hanging in a long loop below them
      const t = k / 18, x = 3.4 + 17.2 * t, y = 12.6 + Math.sin(Math.PI * t) * 8.8;
      p.set(x, y, k % 3 === 1 ? C.violet : gold);
    }
    const half = (cx) => (x, y) => y >= 8 && (x - cx) ** 2 / 25 + (y - 8) ** 2 / 20 <= 1;
    p.each(half(7.2), C.ink).each(half(16.8), C.ink);                                // the rims: half-moons, flat along the top
    p.each((x, y) => y >= 9 && (x - 7.2) ** 2 / 12.5 + (y - 8.6) ** 2 / 10 <= 1, glass);
    p.each((x, y) => y >= 9 && (x - 16.8) ** 2 / 12.5 + (y - 8.6) ** 2 / 10 <= 1, glass);
    p.set(5.6, 9.6, C.white).set(15.2, 9.6, C.white);
    p.rect(10.6, 7.6, 2.8, 1.4, C.ink);                                               // the bridge
    p.line(1.6, 8.6, 2.6, 12, gold, 1.2).line(22.4, 8.6, 21.4, 12, gold, 1.2);        // the ends of the chain at the temples
  },
  trash(p) {                                       // a steel can with a lid
    p.poly([[6, 9], [18, 9], [17, 21.6], [7, 21.6]], C.silver);
    for (const x of [9.4, 12, 14.6]) p.line(x, 10.4, x - (x - 12) * 0.1, 20.4, C.silverLo, 1);   // its ridges
    p.tone((x) => x > 15, C.silverLo, C.silver);
    p.ell(12, 8, 8, 2.4, C.silverHi).tone((x) => x > 15.4, C.silver, C.silverHi);   // the lid
    p.rect(9, 3.6, 6, 1.6, C.silverLo).rect(9, 3.6, 1.6, 4, C.silverLo).rect(13.4, 3.6, 1.6, 4, C.silverLo);    // its handle
    p.set(8, 7, C.white).set(7, 12, C.silverHi).set(7, 13, C.silverHi).set(7, 14, C.silverHi);
    p.outline();
  },
  wingnut(p) {
    p.poly([[9.4, 11], [3, 3.6], [2.6, 7.6], [8, 15]], C.silver).poly([[14.6, 11], [21, 3.6], [21.4, 7.6], [16, 15]], C.silver);   // the wings
    p.disc(12, 15, 5, C.silver);
    p.tone(lowerRight(12, 13, 2), C.silverLo, C.silver);
    p.disc(12, 15, 2, steel).set(11, 14, C.silverLo);
    p.set(4, 5, C.silverHi).set(4, 6, C.silverHi).set(9, 12, C.silverHi);
    p.outline();
  },
  lamp(p) {                                        // a great lamp of lighthouse rings, throwing its light both ways
    const beam = mix(C.note, C.white, 0.55);
    p.poly([[8.6, 8.6], [0.6, 4], [0.6, 15.4], [8.6, 12.8]], beam).poly([[15.4, 8.6], [23.4, 4], [23.4, 15.4], [15.4, 12.8]], beam);
    p.rect(7.6, 6.6, 8.8, 9, C.note);
    for (const y of [8, 10.4, 12.8]) p.rect(7.6, y, 8.8, 1, C.noteLo);              // the rings of the lens
    p.rect(9, 7.4, 1.4, 7.4, C.white);
    p.poly([[7, 6.8], [12, 3.2], [17, 6.8]], steel);                                  // its cap
    p.rect(8.4, 15.6, 7.2, 2.2, C.silverLo).rect(6.6, 17.8, 10.8, 3.4, C.silver).tone((x) => x > 14, C.silverLo, C.silver);
    p.outline();
    p.each((x, y) => (x < 2 || x > 22) && y > 3 && y < 16, null);                    // (the beams run on out of the picture: no line at their ends)
  },
  peanuts(p) {                                     // a small packet, crimped top and bottom, a peanut on its label
    p.poly([[5, 3.6], [19, 3.6], [19.6, 20.4], [4.4, 20.4]], C.red);
    p.tone((x) => x > 15.6, dark(C.red), C.red);
    for (let x = 5; x <= 19; x += 2) { p.set(x, 2.6, C.red); p.set(x, 21.4, C.red); }
    p.rect(5, 8.4, 14.4, 7.2, C.yellow).tone((x) => x > 15.6, C.noteLo, C.yellow);
    p.ell(12, 12, 4.4, 2.2, C.papyrusLo, -0.2).disc(10, 12.4, 1.4, C.papyrus).disc(14, 11.6, 1.4, C.papyrus);
    p.set(7, 5, C.pink).set(7, 6, C.pink);
    p.outline();
  },
  switch(p) {                                      // a lever in a gray box
    p.rect(4.6, 9.6, 14.8, 12, C.silver).tone((x, y) => x > 16 || y > 19, C.silverLo, C.silver);
    p.rect(10.6, 12, 2.8, 6.6, steel);                                               // its slot
    p.line(12, 15, 17.6, 4.6, C.silverLo, 2.2);                                       // the lever
    p.disc(17.8, 4.4, 2.6, C.red).set(17, 3, C.pink);
    p.rect(6, 11, 3, 3, C.note);                                                      // the sticker
    p.outline();
  },
  chair(p) {
    p.rect(6, 1.6, 3, 12, C.papyrusLo).rect(6, 1.6, 11, 2.8, C.papyrusLo);           // the back
    p.poly([[5, 12.6], [18.6, 12.6], [19.6, 15.4], [6, 15.4]], C.papyrus);           // the seat
    p.rect(6, 15, 2.2, 7.4, brown).rect(17, 15, 2.2, 7.4, brown).rect(9.4, 15, 1.6, 5.4, dark(brown, 0.2)).rect(14.4, 15, 1.6, 5.4, dark(brown, 0.2));
    p.tone((x, y) => y > 14.4 && y < 15.6, C.papyrusLo, C.papyrus);
    p.set(7, 3, C.papyrus).set(7, 4, C.papyrus);
    p.outline();
  },
  hand(p) {                                        // a small paw, open: a raccoon's long fingers
    const fur = mix(C.silverLo, C.ink, 0.25), pad = mix(C.cream, C.pink, 0.3);
    for (const a of [-2.35, -1.95, -1.57, -1.19, -0.79]) p.line(12 + Math.cos(a) * 3.6, 15 + Math.sin(a) * 3.6, 12 + Math.cos(a) * 10.4, 15 + Math.sin(a) * 10.4, fur, 2.6);
    p.ell(12, 15.6, 6.2, 5, fur);
    p.tone(lowerRight(12, 14, 4), dark(fur, 0.25), fur);
    p.ell(12, 16.6, 3.4, 2.4, pad);
    for (const a of [-2.35, -1.95, -1.57, -1.19, -0.79]) p.set(12 + Math.cos(a) * 9.4, 15 + Math.sin(a) * 9.4, pad);
    p.outline();
  },
};
/** The banjo, whole, or with its head gone (the round frame with nothing in it, and the neck). */
function banjo(p, whole) {
  p.line(11, 13, 20.6, 3.4, C.papyrusLo, 3.4);                                       // the neck
  p.poly([[18.6, 1], [23, 1], [23, 5.4], [20.4, 5]], brown);                           // its head, with the pegs
  p.disc(8, 16, 7.4, C.papyrusLo);                                                    // the rim
  if (whole) { p.disc(8, 16, 5.4, C.cream); p.tone(lowerRight(8, 16, 2), C.papyrusHi, C.cream); p.rect(6.6, 17, 3.4, 1.4, brown); }   // the head, and its bridge
  else p.disc(8, 16, 5.4, null);
  p.tone(lowerRight(8, 16, 4.4), brown, C.papyrusLo);
  p.outline();
  if (whole) { p.line(8.4, 17, 20, 4, C.silverLo, 1); }                              // the strings
  else {                                                                                // the strings, slack, hanging down through the frame
    p.line(14, 9.6, 10.4, 15, C.silverLo, 1).line(10.4, 15, 11.6, 20.4, C.silverLo, 1);
    p.set(4, 12, C.cream).set(5, 11, C.cream).set(11, 21, C.cream);                    // shreds of the old head at the rim
  }
  p.set(21, 2, C.silver).set(22, 4, C.silver).set(19, 2, C.silver);
}

// ---------------------------------------------------------------- the pictures, made once and kept
const made = new Map();
const told = new Set();
/** A thought picture by name: a canvas 24 x 24, made the first time and kept. Null for a name not in the set. */
export function thoughtPicture(name) {
  if (!DRAW[name]) return null;
  if (!made.has(name)) { const p = new Pix(); DRAW[name](p); made.set(name, p.canvas()); }
  return made.get(name);
}
const urls = new Map();
/** The same, as an address a page can show (for a picture beside the words: a choice, the map's label line). */
export function thoughtURL(name) {
  const known = DRAW[name] ? name : "question";
  if (!urls.has(known)) urls.set(known, thoughtPicture(known).toDataURL());
  return urls.get(known);
}
/** What a line's third element names, as a list of known names: one to three of them. A name not in the set is said in the
    console, once, and stands as `question`; more than three are cut to three (also said); none at all is `question`. */
export function picturesOf(spec, where = "") {
  const list = (Array.isArray(spec) ? spec : spec == null ? [] : [spec]).map((n) => String(n));
  const out = list.slice(0, 3).map((n) => {
    if (DRAW[n]) return n;
    const key = n + "|" + where;
    if (!told.has(key)) { told.add(key); console.warn(`No thought picture called "${n}"${where ? ` (${where})` : ""}: the bubble shows a question mark. The names are in js/art/thoughts.js.`); }
    return "question";
  });
  if (list.length > 3 && !told.has("3|" + where)) { told.add("3|" + where); console.warn(`A thought has ${list.length} pictures${where ? ` (${where})` : ""}: a bubble holds three, and the rest are left out.`); }
  return out.length ? out : ["question"];
}

// ---------------------------------------------------------------- the bubble
export const GAP = 4, PAD = 7;                  // between two pictures; round them inside the cloud
/**
 * A thought bubble round some pictures: a white cloud, its puffs round the edge, a dark line round it and a thin rim in the
 * speaker's colour inside the line, and two or three small puffs trailing from it toward where the thinker is
 * (`toward`: [dx, dy] in picture pixels, from the middle of the cloud's bottom edge, the trail leaving the cloud there; or,
 * when dy is below 0, from the middle of its top edge, the trail rising from there, as for the lead up in a duct over the
 * room he looks down into; null: no trail).
 * Gives { canvas, ox, oy, cloud, size }: the canvas, the point of it that is the middle of the cloud's bottom edge (ox, oy),
 * the cloud's box in the canvas, [left, top, right, bottom), and the canvas's size. All in picture pixels: it is shown at
 * the stage's scale.
 */
export function bubble(names, { rim = C.white, toward = null } = {}) {
  const n = names.length, inner = n * SIZE + (n - 1) * GAP, cw = inner + PAD * 2, ch = SIZE + PAD * 2 - 2;
  // the trail: up to three puffs, smaller as they go, from the cloud's edge toward the thinker
  const puffs = [];
  if (toward && Math.hypot(toward[0], toward[1]) > 4) {
    const [tx, ty] = toward, d = Math.hypot(tx, ty), ux = tx / d, uy = ty / d, steps = d > 30 ? [[0.3, 3.4], [0.62, 2.4], [0.9, 1.5]] : [[0.42, 2.8], [0.86, 1.6]];
    const sy = ty < 0 ? -ch : 0;                // where it leaves the cloud: its bottom edge, or its top
    for (const [k, r] of steps) puffs.push([ux * (8 + (d - 8) * k), sy + uy * (8 + (d - 8) * k), r]);
  }
  const reach = puffs.reduce((m, [x, y, r]) => [Math.min(m[0], x - r), Math.max(m[1], x + r), Math.min(m[2], y - r), Math.max(m[3], y + r)], [0, 0, 0, 0]);
  const m = 2;                                  // room for the line round it
  const left = Math.ceil(Math.max(cw / 2, -reach[0])) + m, right = Math.ceil(Math.max(cw / 2, reach[1])) + m;
  const top = Math.ceil(Math.max(ch + 2, -reach[2])) + m, bottom = Math.ceil(Math.max(0, reach[3])) + m;
  const W = left + right, H = top + bottom, ox = left, oy = top;      // (ox, oy): the middle of the cloud's bottom edge
  const p = new Pix(W, H), x0 = ox - cw / 2, y0 = oy - ch, cloud = [Math.floor(x0), Math.floor(y0), Math.ceil(x0 + cw), Math.ceil(oy)];
  // the cloud: a rounded box with puffs all round its edge, so that it reads as a cloud and not a box
  const blobs = [];
  const r = Math.min(8.5, ch / 2);
  const span = cw - r * 1.6, count = Math.max(1, Math.round(span / 11)), step = span / count;
  for (let i = 0; i <= count; i++) { const x = x0 + r * 0.8 + i * step; blobs.push([x, y0 + r * 0.62, r * (i % 2 ? 0.92 : 1)]); }
  for (let i = 0; i < count; i++) { const x = x0 + r * 0.8 + (i + 0.5) * step; blobs.push([x, oy - r * 0.62, r * (i % 2 ? 1 : 0.9)]); }
  blobs.push([x0 + r * 0.55, y0 + ch / 2, r * 0.95], [x0 + cw - r * 0.55, y0 + ch / 2, r * 0.95]);
  const inCloud = (px, py) => (px > x0 + 4 && px < x0 + cw - 4 && py > y0 + 4 && py < oy - 4) || blobs.some(([bx, by, br]) => (px - bx) ** 2 + (py - by) ** 2 <= br * br);
  p.each((px, py) => inCloud(px, py), C.white);
  for (const [dx, dy, pr] of puffs) p.disc(ox + dx, oy + dy, pr, C.white);
  // the rim, in the speaker's colour: the cloud's own edge, a pixel in from the line; then the dark line round it all
  const edge = [];
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    if (!p.get(x, y)) continue;
    const inC = inCloud(x + 0.5, y + 0.5);
    if (inC && (!p.get(x - 1, y) || !p.get(x + 1, y) || !p.get(x, y - 1) || !p.get(x, y + 1))) edge.push([x, y]);
  }
  for (const [x, y] of edge) p.set(x, y, rim);
  p.outline(C.ink);
  const canvas = p.canvas(), ctx = canvas.getContext("2d");
  names.forEach((name, i) => ctx.drawImage(thoughtPicture(name), Math.round(x0 + PAD + i * (SIZE + GAP)), Math.round(y0 + PAD - 1)));
  return { canvas, ox, oy, cloud, size: [W, H] };
}

/** ENGINE-17: the small loudspeaker drawn at the left of a line on a building's speakers (game.js pa), 16 x 16, in the
    speaker's colour for its sound. Kept for each colour. */
const speakers = new Map();
export function speakerIcon(color = C.cream) {
  if (speakers.has(color)) return speakers.get(color);
  const p = new Pix(16, 16);
  p.rect(1.5, 5.5, 4, 5, C.silver).poly([[5, 5.6], [10, 1.6], [10, 14.4], [5, 10.4]], C.silverLo);
  p.tone((x, y) => y > 9, steel, C.silverLo);
  p.outline();
  p.each((x, y) => { const d = Math.hypot(x - 9, y - 8); return x > 11 && ((d > 3.4 && d < 4.6) || (d > 6 && d < 7.2)) && Math.abs(y - 8) < d * 0.8; }, color);
  const c = p.canvas();
  speakers.set(color, c);
  return c;
}
