// The cast, as the rig sees them: proportions, colors, clothes, hair, and the
// three settings that carry personality:
//
//   stance     how they stand when nothing is happening ("clasped", "akimbo", "book", "behind")
//   walk       how they move: { swing, arm, elbow, lean, lift, bob, wag, hold }
//   gestures   what their hands do when they talk (numbers from talkPose in rig.js)
//
// The family comes from the present, so their colors never change with the era.
// Each of them owns one color nobody else in the family wears.
//
// PLACEHOLDER DESIGNS until the author signs them off. docs/CHARACTERS.md says who
// these people are. To change someone, change the numbers and colors here; every
// view and every animation follows. tools/sprites.html shows the result.

import { ADULT, CHILD, WOMAN, CARRY, blend, ramp, shifted, add } from "./rig.js";

const SKIN = ramp("#f9d6ae", "#e8b083", "#c2825a", "#87533c");
const SKIN_BROWN = ramp("#d39a66", "#b0733f", "#84502a", "#55301a");
const SKIN_WEATHERED = ramp("#f0c49a", "#d99f72", "#ad744c", "#774a32");
const WHITE = ramp("#ffffff", "#ecebe2", "#bdb9ac", "#8a867c");

/**
 * Where hair grows on the head. Each number says how far down it comes at the forehead, the temples,
 * the sides and the back: 1 is the crown, 0 the level of the ears, -1 under the chin.
 * `sweep` brings it lower on the character's right, for a fringe combed to one side.
 */
const hairline = (front, temple, side, back, sweep = 0) => (x, y, z) => {
  const h = z > 0.3 ? front + (temple - front) * (1 - (z - 0.3) / 0.7) : z > 0 ? temple + (side - temple) * (1 - z / 0.3) : side + (back - side) * -z;
  return y > h - (z > 0 ? sweep * Math.max(0, x) : 0);
};

const FLOWERS = [
  ramp("#ff9a7d", "#ee5b40", "#bb3c2a", "#7e2619"),      // coral petals
  ramp("#ffffff", "#fff4d8", "#dccaa0", "#a08f68"),      // cream petals
  ramp("#62d2bf", "#2f9c8f", "#1f6f66", "#134843"),      // leaves
];

// ---------- Dad: vacation shirt, shorts, socks and sandals ----------
const DAD_HAIR = ramp("#9a6a40", "#70482a", "#4d301a", "#2f1d10");
export const dad = {
  name: "Dad", height: 1.0,
  dim: { ...ADULT, headR: [0.066, 0.079, 0.073], shoulderW: 0.106, trunkTop: [0.118, 0.080], trunkLow: [0.122, 0.104], bellyFwd: 0.026,
         hipY: 0.475, thigh: 0.222, shin: 0.212, legR: [0.060, 0.045, 0.033], armR: [0.038, 0.032, 0.024], handR: 0.030 },
  skin: SKIN,
  hair: { mat: DAD_HAIR, where: (x, y, z) => y > (z > 0 ? 0.42 + 0.26 * z : 0.42 + 0.92 * z) - 0.12 * Math.abs(x), top: [-0.006, 0.74, 0.16, 0.86, 0.36, 0.86] },
  face: { brows: DAD_HAIR.tones[2], moustache: DAD_HAIR, eye: "#2a1a12", mouthLat: -0.66 },
  top: { mat: ramp("#ffe582", "#f4c043", "#d19328", "#93601a"), sleeves: 0.62, hem: true, open: true, collar: true, pattern: FLOWERS },
  bottom: { kind: "shorts", mat: ramp("#a9b381", "#7f8d5c", "#59663f", "#39442b"), len: 0.72 },
  socks: { mat: WHITE, from: 0.52, stripes: [ramp("#f08a70", "#d2452f", "#a12f22", "#6e1f19"), ramp("#7fb2e6", "#3f79c2", "#2b5590", "#1b3760")] },
  shoes: { kind: "sandals", mat: ramp("#a8744a", "#7d5030", "#553521", "#332015"), sole: ramp("#6b4a30", "#4d3320", "#332015", "#1f130c") },
  gestures: [0, 1, 2, 3],                               // a nod, a point, a shrug, a hand on the hip
};

// ---------- the Son: red cap, blue hoodie, backpack. Zany: he bounces, and his hands never stop. ----------
const SON_HAIR = ramp("#66492f", "#43301f", "#2c1e13", "#190f09");
const CAP = ramp("#ff7a62", "#de4a33", "#a93224", "#72201a");
const PACK = ramp("#b39bf5", "#8463d8", "#5f44a8", "#3d2b72");
export const son = {
  name: "Son", height: 0.74,
  dim: CHILD,
  skin: SKIN,
  hair: { mat: SON_HAIR, where: (x, y, z) => y > (z > 0 ? 0.30 + 0.34 * z : 0.20 + 0.75 * z) - 0.10 * Math.abs(x) },
  face: { big: true, eye: "#2a1a12", lip: "#a5523f", mouthLat: -0.60, eyeLat: -0.02, eyeLon: 0.48 },
  top: { mat: ramp("#93dcf2", "#4fc0e2", "#2e90b6", "#1f6483"), sleeves: 2, hem: true },
  bottom: { kind: "shorts", mat: ramp("#5a668f", "#3c4563", "#293049", "#1a1f31"), len: 0.80 },
  socks: { mat: WHITE, from: 0.72 },
  shoes: { kind: "sneakers", mat: ramp("#ffffff", "#f1efe6", "#c4c0b2", "#8f8b80"), stripe: CAP, sole: ramp("#d9d5c8", "#b5b1a4", "#8a867c", "#5f5c55") },
  walk: { swing: 0.50, arm: 0.70, elbow: 0.55, pump: 0.60, lean: 0.10, lift: 1.3, bob: 0.05, wag: 0.10, sway: 0.020 },   // a bounce, fists pumping, head going from side to side
  gestures: [1, 4, 9, 2],                               // a point, both arms up, both hands waving, a shrug
  extras({ ball, limb, own, headPt, wide, deep, d, hy, tw, J, parts }) {
    const hr = d.headR, hc = J.head;
    // cap: a dome over the top of the head and a peak out in front
    ball(add(hc, [0, 0.006, 0]), [hr[0] * 1.12, hr[1] * 1.10, hr[2] * 1.12], CAP, { part: parts.HAT, fn: (ux, uy, uz) => { const o = own(ux, uy, uz, hy); return o[1] > 0.40 - 0.06 * o[2] ? undefined : null; } }, hy);
    ball(headPt([0, hr[1] * 0.58, hr[2] * 0.98 + 0.030]), [0.058, 0.011, 0.050], shifted(CAP, 1), { part: parts.HAT }, hy);
    // hood bunched behind the neck, and the backpack with its straps
    ball(add(J.neck, J.torso([0, -0.022, -0.052])), [0.064, 0.040, 0.042], shifted(son.top.mat, 1), { part: parts.TORSO }, tw);
    // the pack: a soft upright block against his back, with a pocket on it. [half width, half depth], like the trunk.
    const body = [0.072, 0.040], pocket = [0.050, 0.020], r = wide(body), rp = wide(pocket), back = d.trunkTop[1] + 0.036;
    const onBack = (h, out) => add(J.spine(d.shoulderY - h), J.torso([0, 0, -(back + out)]));
    limb(onBack(0.050, 0), onBack(0.190, 0), r * 0.94, r, PACK, { part: parts.EXTRA, depth: deep(body) / r });
    limb(onBack(0.130, 0.034), onBack(0.186, 0.034), rp, rp, shifted(PACK, 1), { part: parts.EXTRA2, depth: deep(pocket) / rp });
    for (const sd of [1, -1]) limb(add(J.sh, J.torso([sd * 0.060, 0.012, 0.0])), add(J.spine(d.shoulderY - 0.17), J.torso([sd * 0.074, 0, d.trunkTop[1] * 0.80])), 0.011, 0.011, PACK, { part: parts.EXTRA, bias: 4 });
  },
};

// ---------- Mom: an emerald dress, pearls, her hair up. Classy: she stands with her hands clasped and never hurries. ----------
const MOM_HAIR = ramp("#c47a48", "#96502c", "#683319", "#40200f");
const EMERALD = ramp("#63d3a4", "#2aa27a", "#1b7459", "#104a3a");
const PEARL = ramp("#ffffff", "#f6efe2", "#d2c8b4", "#9c937f");
const LEATHER = ramp("#d9a877", "#b07a4a", "#7e5430", "#50341d");
export const mom = {
  name: "Mom", height: 0.93,
  dim: WOMAN,
  skin: SKIN,
  hair: { mat: MOM_HAIR, bulk: 1.09, where: hairline(0.60, 0.42, 0.02, -0.62, 0.22) },
  face: { lashes: true, brows: MOM_HAIR.tones[1], eye: "#33210f", lip: "#c4566f", mouthLat: -0.54, eyeLat: 0.08, nose: 0.85 },
  top: { mat: EMERALD, sleeves: 0.42, belt: shifted(EMERALD, 2), open: true },
  bottom: { kind: "skirt", mat: EMERALD, len: 1.02, flare: 1.20 },
  shoes: { kind: "pumps", mat: ramp("#fffaf0", "#efe2c8", "#c3b596", "#8e8168"), sole: ramp("#c9b99a", "#a39375", "#7a6d55", "#52483a") },
  stance: "clasped",
  walk: { swing: 0.40, arm: 0.20, lean: 0.02, twist: 0.09, sway: 0.016 },     // short steps, quiet arms, a little sway
  gestures: [0, 5, 8, 0],                               // a nod, a hand to the heart, an open hand
  pace: 60,
  extras({ ball, limb, headPt, d, hy, tw, J, S, parts }) {
    const hr = d.headR;
    // her hair is pinned up in a knot at the back of the crown
    ball(headPt([0, hr[1] * 0.90, -hr[2] * 0.52]), [0.036, 0.031, 0.034], MOM_HAIR, { part: parts.HAIR }, hy);
    // pearls: one at each ear, and a string of them at the neck
    for (const sd of [1, -1]) ball(headPt([sd * hr[0] * 1.0, -0.031, -0.002]), [0.008, 0.009, 0.008], PEARL, { part: parts.EXTRA }, hy);
    ball(add(J.sh, J.torso([0, -0.016, d.trunkTop[1] * 0.50])), [0.046, 0.034, 0.042], PEARL, {
      part: parts.EXTRA, bias: S * 0.03, fn: (ux, uy) => { const q = ux * ux * 0.8 + (uy + 1.05) ** 2; return q > 0.92 && q < 1.50 ? undefined : null; },
    }, tw);
    // a handbag, hanging from her left hand
    const w = J.L.wrist;
    limb(add(w, [0, -0.004, 0]), add(w, [0, -0.046, 0]), 0.006, 0.006, shifted(LEATHER, 1), { part: parts.EXTRA2 });
    ball(add(w, [0, -0.078, 0]), [0.040, 0.034, 0.017], LEATHER, { part: parts.EXTRA2, fn: (ux, uy) => (uy < -0.55 ? shifted(LEATHER, 1) : undefined) }, tw);
  },
};

// ---------- Big Sister, 13: cardigan, pleated skirt, glasses, long hair, and always a book. ----------
const BIG_HAIR = ramp("#7c4d33", "#573220", "#3b2115", "#23130b");
const INDIGO = ramp("#99a0f2", "#666cd6", "#474aa6", "#2e2f72");
const GRAY = ramp("#a9acba", "#7f8394", "#5b5e6e", "#3c3e4b");
const BOOK = ramp("#e58a66", "#c05a3c", "#8b3b27", "#5a2519");
const PAGES = ramp("#fffdf2", "#f3ead0", "#cfc4a4", "#998e70");
const LABEL = ramp("#ffe9a8", "#f2cd6b", "#c39a3c", "#856724");
export const bigsis = {
  name: "Big Sister", height: 0.87,
  dim: { ...blend(CHILD, WOMAN, 0.62), legR: [0.050, 0.038, 0.027] },
  skin: SKIN,
  hair: { mat: BIG_HAIR, bulk: 1.09, where: hairline(0.34, 0.28, -0.50, -0.98) },
  face: { glasses: "#2b2f55", eye: "#2a1a12", lip: "#b55f52", mouthLat: -0.58, eyeLat: 0.02, eyeLon: 0.47 },
  top: { mat: INDIGO, sleeves: 2, hem: true, band: WHITE },
  bottom: { kind: "skirt", mat: GRAY, len: 0.82, flare: 1.16, pleats: 9 },
  socks: { mat: WHITE, from: 0.10 },
  shoes: { kind: "shoes", mat: ramp("#8f5a3c", "#693e27", "#47291a", "#2a180f"), sole: ramp("#4a2e1f", "#332015", "#22150e", "#140c08") },
  stance: "book",
  walk: { swing: 0.43, arm: 0.30, lean: 0.04, hold: { L: CARRY.book } },     // one arm swings; the other has the book
  gestures: [0, 11, 6, 10],                             // a nod, a finger in the air, pushing her glasses up, pointing ahead
  extras({ ball, limb, own, headPt, wide, deep, d, hy, J, S, parts }) {
    const hr = d.headR, hc = J.head;
    // long hair: down the back, and a lock in front of each shoulder
    limb(headPt([0, -hr[1] * 0.10, -hr[2] * 0.62]), add(J.spine(d.shoulderY - 0.150), J.torso([0, 0, -(d.trunkTop[1] + 0.022)])), 0.056, 0.044, BIG_HAIR, { part: parts.HAIR, depth: 0.5, bias: S * 0.02 });
    for (const sd of [1, -1]) limb(headPt([sd * hr[0] * 0.90, -hr[1] * 0.30, hr[2] * 0.05]), add(J.sh, J.torso([sd * 0.062, -0.050, 0.018])), 0.017, 0.012, BIG_HAIR, { part: parts.HAIR });
    // a headband
    ball(add(hc, [0, 0.004, 0]), [hr[0] * 1.13, hr[1] * 1.13, hr[2] * 1.13], INDIGO, { part: parts.HAT, fn: (ux, uy, uz) => { const o = own(ux, uy, uz, hy); return o[1] > 0.05 && Math.abs(o[2] - 0.12) < 0.13 ? undefined : null; } }, hy);
    // the book, flat against her chest, with her left forearm across it
    const size = [0.050, 0.013], r = wide(size), low = d.shoulderY - d.shoulderDrop - d.upperArm - 0.018;
    const onChest = (h) => add(J.spine(h), J.torso([-0.020, 0, d.trunkLow[1] + 0.008]));
    limb(onChest(low), onChest(low + 0.150), r, r, BOOK, {
      part: parts.EXTRA, depth: deep(size) / r, flatten: 2.4, squareStart: true, squareEnd: true,
      fn: (t, across) => (across > 0.60 ? PAGES : t > 0.60 && t < 0.80 && Math.abs(across) < 0.42 ? LABEL : undefined),      // the pages, and a label on the cover
    });
  },
};

// ---------- Little Sister, 7: pink overalls, yellow boots, pigtails. Small but mighty: fists on hips, and she stomps. ----------
const LIL_HAIR = ramp("#e0b06c", "#b98646", "#875d2c", "#573a19");
const PINK = ramp("#ff9db4", "#f0607f", "#bd3f5e", "#802a41");
const SUN = ramp("#fff0a0", "#ffd23f", "#d59a1f", "#93640f");
const SMALL = { ...CHILD, headR: [0.086, 0.100, 0.092], neckY: 0.776, shoulderY: 0.746, waistY: 0.555, hipY: 0.452, thigh: 0.208, shin: 0.198, legR: [0.056, 0.044, 0.034] };
export const lilsis = {
  name: "Little Sister", height: 0.67,
  dim: SMALL,
  skin: SKIN,
  hair: { mat: LIL_HAIR, bulk: 1.08, where: hairline(0.40, 0.34, -0.06, -0.58) },
  face: { big: true, freckles: true, eye: "#2a1a12", lip: "#c2605a", mouthLat: -0.60, eyeLat: -0.04, eyeLon: 0.50 },
  top: { mat: WHITE, sleeves: 0.5 },
  bottom: { kind: "shorts", mat: PINK, len: 0.62, rise: 0.085, bib: { top: 0.078, half: 0.60, strap: 0.26 } },     // overalls: a high waist, a bib and two straps
  socks: { mat: SUN, from: 0.40, thick: 0.013 },        // rain boots
  shoes: { kind: "boots", mat: SUN, sole: shifted(SUN, 2) },
  stance: "akimbo",
  walk: { swing: 0.50, arm: 0.72, elbow: 0.12, lean: 0.09, lift: 1.25, bob: 0.03 },     // a stomp: straight arms, like a small soldier
  gestures: [0, 4, 7, 10],                              // a nod, both arms up, showing her muscles, pointing ahead
  pace: 58,
  extras({ sf, P, ball, limb, headPt, d, hy, th, J, fine, parts }) {
    const hr = d.headR;
    // pigtails: each starts at a yellow band high on the side of her head, puffs out, and hangs to a point beside her cheek
    for (const sd of [1, -1]) {
      const at = (out, up, back = 0) => headPt([sd * (hr[0] * 0.90 + out), hr[1] * 0.50 + up, -hr[2] * 0.12 - back]);
      limb(at(0.016, -0.004), at(0.046, -0.034, 0.004), 0.018, 0.028, LIL_HAIR, { part: parts.HAIR });
      limb(at(0.046, -0.034, 0.004), at(0.052, -0.112, 0.014), 0.028, 0.010, LIL_HAIR, { part: parts.HAIR });
      ball(at(0.014, 0.004), [0.024, 0.026, 0.024], SUN, { part: parts.HAT }, hy);
    }
    // a star on the bib of her overalls
    if (fine && Math.cos(th) > 0.5) {
      const c = P(add(J.spine(d.shoulderY - 0.150), J.torso([0, 0, d.trunkTop[1] * 0.98]))), x = Math.round(c[0] - 0.5), y = Math.round(c[1] - 0.5), star = SUN.tones[0];
      for (const [i, k] of [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]]) sf.dot(x + i, y + k, star, parts.TORSO);
    }
  },
};

// ---------- a scribe of ancient Egypt, sitting with his palette ----------
const WIG = ramp("#44475a", "#26283a", "#171824", "#0b0c14");
const LINEN = ramp("#fffdf4", "#f1e9d6", "#cdc0a5", "#988b71");
const TURQ = ramp("#93d6d2", "#3f9aa3", "#2b6f7a", "#1b4750");
const GOLD = ramp("#ffeeb0", "#f0c35a", "#b98a2e", "#7a5a1c");
const PAPYRUS = ramp("#f1d894", "#dbb46b", "#b08945", "#7a5c2c");
export const scribe = {
  name: "Scribe", height: 1.0, seated: true, shadow: 0.26, span: 1.15,
  dim: { ...ADULT, trunkTop: [0.108, 0.070], trunkLow: [0.094, 0.072] },
  skin: SKIN_BROWN,
  hair: { mat: WIG, bulk: 1.13, where: (x, y, z) => !(z > 0.34 && y < 0.50) },
  face: { brows: WIG.tones[1], eye: "#0b0c16", lip: "#6a3a22", mouthLat: -0.56 },
  top: {},
  bottom: { kind: "kilt", mat: LINEN, len: 0.80 },
  shoes: { kind: "bare" },
  extras({ ball, limb, headPt, d, hy, tw, J, S, parts }) {
    const hr = d.headR;
    // the wig hangs to the shoulders at each side and behind
    for (const sd of [1, -1]) limb(headPt([sd * hr[0] * 0.92, -hr[1] * 0.2, -0.012]), add(J.sh, J.torso([sd * 0.072, 0.004, -0.004])), 0.034, 0.030, WIG, { part: parts.HAIR });
    limb(headPt([0, -hr[1] * 0.2, -hr[2] * 0.75]), add(J.sh, J.torso([0, 0.0, -0.05])), 0.045, 0.040, WIG, { part: parts.HAIR });
    // a broad collar of beads, and the writing palette across his lap
    ball(add(J.sh, J.torso([0, -0.030, d.trunkTop[1] * 0.50])), [0.090, 0.046, 0.048], TURQ, {
      part: parts.EXTRA, bias: S * 0.02,
      fn: (ux, uy) => (ux * ux * 0.8 + (uy + 1.05) ** 2 < 0.62 ? null : ux * ux + uy * uy > 0.66 ? GOLD : undefined),    // a crescent round the neck, edged in gold
    }, tw);
    const lap = [(J.R.wrist[0] + J.L.wrist[0]) / 2, Math.min(J.R.wrist[1], J.L.wrist[1]) - 0.012, (J.R.wrist[2] + J.L.wrist[2]) / 2 + 0.02];
    ball(lap, [0.120, 0.014, 0.070], PAPYRUS, { part: parts.EXTRA });
  },
};

// ---------- the old-timer at the last stop in Nevada: straw hat, white beard, a lawn chair ----------
const SNOW = ramp("#ffffff", "#ecece6", "#c2c2ba", "#8e8e86");
const DENIM = ramp("#a9c3db", "#7797b6", "#53708e", "#364a61");
const CANVAS = ramp("#c9b48a", "#a48d63", "#7b6845", "#52452d");
const STRAW = ramp("#fff0b8", "#e9cf82", "#b99c52", "#7e6932");
const WEBBING = ramp("#8fe0b0", "#4fb07e", "#357c59", "#22513a");
const TUBE = ramp("#f6f8fa", "#c4cad1", "#8b929a", "#565c64");
export const oldtimer = {
  name: "Old-Timer", height: 0.97, seated: "chair", shadow: 0.25, span: 1.2,
  dim: { ...ADULT, trunkTop: [0.110, 0.076], trunkLow: [0.110, 0.094], bellyFwd: 0.014 },
  skin: SKIN_WEATHERED,
  hair: { mat: SNOW, where: hairline(1.3, 1.1, 0.20, -0.50) },
  face: { beard: SNOW, brows: SNOW.tones[2], eye: "#2a1a12", mouthLat: -0.50 },
  top: { mat: DENIM, sleeves: 2 },
  bottom: { kind: "trousers", mat: CANVAS },
  shoes: { kind: "boots", mat: ramp("#9a6b45", "#70482a", "#4d301a", "#2f1d10"), sole: ramp("#4d301a", "#372212", "#24160c", "#150d07") },
  extras({ ball, limb, headPt, d, hy, J, parts }) {
    const hr = d.headR, hip = J.hipC, seat = hip[1] - d.pelvisR[1] * 0.86;
    // a straw hat: a wide brim and a low crown
    ball(headPt([0, hr[1] * 0.62, 0.004]), [0.118, 0.012, 0.118], STRAW, { part: parts.HAT }, hy);
    ball(headPt([0, hr[1] * 0.86, 0]), [hr[0] * 0.98, hr[1] * 0.42, hr[2] * 0.98], shifted(STRAW, 1), { part: parts.HAT }, hy);
    // suspenders over the work shirt
    for (const sd of [1, -1]) limb(add(J.sh, J.torso([sd * 0.050, 0.010, d.trunkTop[1] * 0.3])), add(J.spine(d.waistY - 0.03), J.torso([sd * 0.062, 0, d.trunkLow[1] * 0.98 + d.bellyFwd])), 0.009, 0.009, shifted(CANVAS, 2), { part: parts.EXTRA, bias: 3 });
    // the lawn chair: webbing for the seat and the back, on a frame of bent tube
    const at = (x, y, z) => [hip[0] + x, y, hip[2] + z];
    ball(at(0, seat, 0.075), [0.120, 0.012, 0.140], WEBBING, { part: parts.EXTRA3 });
    ball(at(0, seat + 0.190, -0.105), [0.120, 0.180, 0.014], WEBBING, { part: parts.EXTRA3, fn: (ux, uy) => (Math.floor((uy + 1) * 4.5) % 2 ? shifted(WEBBING, 1) : undefined) });
    for (const sd of [1, -1]) {
      limb(at(sd * 0.122, seat, 0.200), at(sd * 0.122, 0.008, 0.215), 0.008, 0.008, TUBE, { part: parts.EXTRA2 });      // front leg
      limb(at(sd * 0.122, seat, -0.060), at(sd * 0.122, 0.008, -0.130), 0.008, 0.008, TUBE, { part: parts.EXTRA2 });    // back leg
      limb(at(sd * 0.122, seat + 0.085, -0.100), at(sd * 0.122, seat + 0.085, 0.190), 0.009, 0.009, TUBE, { part: parts.EXTRA2 });   // arm rest
      limb(at(sd * 0.122, seat + 0.085, 0.190), at(sd * 0.122, seat, 0.200), 0.008, 0.008, TUBE, { part: parts.EXTRA2 });
      limb(at(sd * 0.122, seat, -0.060), at(sd * 0.122, seat + 0.370, -0.120), 0.008, 0.008, TUBE, { part: parts.EXTRA2 });      // the back's upright
    }
  },
};

// ---------- the man in gray, who stands in front of things in the desert ----------
const SUIT = ramp("#b4b8c2", "#8b909c", "#666a76", "#44474f");
const TIE = ramp("#6f7686", "#4a5060", "#333846", "#20232d");
export const agent = {
  name: "Man in Gray", height: 1.0,
  dim: { ...ADULT, shoulderW: 0.104, trunkTop: [0.116, 0.076], trunkLow: [0.102, 0.078] },
  skin: SKIN,
  hair: { mat: ramp("#5a5560", "#3a3640", "#25222a", "#151318"), where: hairline(0.62, 0.50, 0.26, -0.42) },
  face: { shades: "#15161c", mouthLat: -0.56 },
  top: { mat: SUIT, sleeves: 2, hem: true, open: true, under: WHITE, collar: shifted(SUIT, 1) },
  bottom: { kind: "trousers", mat: shifted(SUIT, 1) },
  shoes: { kind: "shoes", mat: ramp("#4a4650", "#2c2a31", "#1b1a1f", "#0e0d10"), sole: ramp("#2c2a31", "#1b1a1f", "#0e0d10", "#070608") },
  stance: "behind",
  walk: { swing: 0.42, arm: 0.26, lean: 0.03 },
  gestures: [0, 8, 0, 10],                              // mostly nothing; an open hand; a pointing finger
  extras({ limb, d, J, parts }) {
    const front = d.trunkTop[1];
    limb(add(J.sh, J.torso([0, 0.004, front * 0.50])), add(J.sh, J.torso([0, -0.112, front * 1.00])), 0.008, 0.012, TIE, { part: parts.EXTRA, bias: 4 });
  },
};

export const people = { dad, son, mom, bigsis, lilsis, scribe, oldtimer, agent };
