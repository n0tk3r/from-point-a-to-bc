// The cast, as the rig sees them: proportions, colors, clothes, hair, a face, and the
// settings that carry personality:
//
//   stance     how they stand when nothing is happening ("clasped", "akimbo", "behind", "elbow", "folded", "straps", "hip", "carry", "belly")
//   walk       how they move: { swing, arm, elbow, lean, lift, bob, wag }
//   gestures   what their hands do when they talk (numbers from talkPose in rig.js)
//   hold       an arm that is always busy with something: { R: { hand: [...], grip: true } }
//   seated     for someone who is found sitting: "ground" (cross-legged) or "chair" (anything raised).
//              The engine knows only those two, and puts a speaker's words above a head at about that height.
//   sit        what exactly they sit on and how: { seat: "chair", "bench", "stool", "step" or a height, lean, knees,
//              solid: true when the seat is a block painted in the scene (a step, a kerb): the shadow is then under the feet }
//   rest       where an arm lies when a pose leaves it alone: { L: { hand: [...] } }
//   pace       how fast they walk, in picture pixels a second at full size
//   pray       how they stand to pray: { high: how high the folded hands are (0 the belt, 1 under the chin), bow, tight }
//              (someone found sitting prays sitting, hands lifted and open: { high, out, apart, bow }: see sitPrayPose in rig.js)
//   stood      for someone found sitting: what changes when they stand up (what they hold and how, how they walk)
//   sit.drawn  their seat is drawn with them (a stool, a lawn chair): it stays where it is when they get up
//   riseMs     how long getting up takes them, in ms, if not the usual
//   fidgets    their own small movements, besides everyone's: { stand: [...], sit: [...] } (`only: true`: theirs and no others)
//
// The family comes from the present, so their colors never change with the era.
// Each of them owns one color nobody else in the family wears.
//
// docs/CHARACTERS.md says who these people are. To change someone, change the numbers
// and colors here; every view and every animation follows. tools/sprites.html shows the result.

import { ADULT, CHILD, WOMAN, blend, ramp, shifted, add, mix, turn, wear, upOf } from "./rig.js";

// Skin: the plain color, the shade, and a deeper line. (The first tone is kept for things that shine.)
const SKIN = ramp("#fbdcc0", "#f0bc9a", "#c98664", "#8c5440");
const WHITE = ramp("#ffffff", "#f0eee6", "#bfbcae", "#858275");

/**
 * Where hair grows on the head. Each number says how far down it comes: 1 is the crown, 0 the level
 * of the ears, -1 under the chin.
 *   front   at the middle of the forehead        temple  at the corners of the forehead
 *   side    over the ears                        back    at the nape
 *   sweep   brings it lower on the character's right, for a fringe combed to one side
 *   recede  lifts it at the corners of the forehead, as on a man whose hair is going
 *   burn    how far a sideburn comes down in front of each ear
 *   crown   a bald patch on top: its size (0 for none)
 *   top     for a bald head with a fringe: the height above which nothing grows
 *   temples the hairline as a face shows it: level across the middle of the forehead (out to `brow` radians from the
 *           middle, measured round the head), then down round the corners of the forehead (`temple` at the corner)
 *           to the level over the ears (`side`), which it reaches `temples` radians round. Seen from in front, the
 *           hair then frames the forehead and comes down the temples to the ears, as hair does, instead of sitting
 *           on top of it. (Without it, the hairline is set by how far forward a point is, which from in front leaves
 *           the whole width of the forehead bare up to the corners.)
 */
const ease = (t) => t * t * (3 - 2 * t);
const hairline = ({ front = 0.60, temple = 0.45, side = 0.10, back = -0.50, sweep = 0, recede = 0, burn = 0, crown = 0, top = 9, brow = 0.50, temples = 0 } = {}) => (x, y, z) => {
  if (top < 9 && (z > 0.34 || y > top + 0.25 * Math.max(0, -z))) return false;      // a bald head: only a fringe is left, round the sides and the back
  let h;
  if (temples > 0 && z > 0) {
    const a = Math.abs(Math.atan2(x, z)), am = (brow + temples) / 2;             // round the head from the middle of the forehead: 0 there, π/2 over the ears
    h = a <= brow ? front : a < am ? front + (temple - front) * ease((a - brow) / (am - brow)) : a < temples ? temple + (side - temple) * ease((a - am) / (temples - am)) : side;
  } else h = z > 0.3 ? front + (temple - front) * (1 - (z - 0.3) / 0.7) : z > 0 ? temple + (side - temple) * (1 - z / 0.3) : side + (back - side) * -z;
  if (z > 0) h -= sweep * Math.max(0, x);
  if (recede && z > 0.35) { const k = 1 - Math.min(1, Math.abs(Math.abs(x) - 0.50) / 0.28); if (k > 0) h += recede * k; }
  if (burn && z > 0.02 && z < 0.42 && Math.abs(x) > 0.80) h -= burn * (1 - Math.abs(z - 0.22) / 0.20);
  if (crown && y > 1 - crown && Math.hypot(x, z + 0.1) < crown * 1.5) return false;
  return y > h;
};

/** Curly hair: little rings of shade all over it, fixed to the head so they turn and nod with it. `n`: about how many
    rings fit round the head. (Head directions as `where` has them.) */
const curl = (x, y, z, n) => {
  if (y > 0.62) return false;                                           // (smooth on the crown, where it is combed)
  const a = Math.atan2(x, z) * n / Math.PI, b = (y + 1) * n * 0.9, i = Math.floor(a), j = Math.floor(b), u = a - i - 0.5, v = b - j - 0.5 + ((i & 1) ? 0.5 : 0) % 1;
  const r = Math.hypot(u, v - Math.round(v));
  return r > 0.28 && r < 0.46 && v - Math.round(v) > -0.1;
};

const FLOWERS = [
  ramp("#ff9a7d", "#ee5b40", "#bb3c2a", "#7e2619"),      // coral petals
  ramp("#ffffff", "#fff4d8", "#dccaa0", "#a08f68"),      // cream petals
  ramp("#62d2bf", "#2f9c8f", "#1f6f66", "#134843"),      // leaves
];

// ---------- Dad: vacation shirt, shorts, socks and sandals; his hair slicked back to the side, green eyes, stubble, a short beard ----------
const DAD_HAIR = ramp("#a87a4c", "#70482a", "#4d301a", "#2f1d10", { shine: true });      // (combed back with something in it: it catches the light)
const DAD_BEARD = ramp("#8a6040", "#6a4428", "#4d301a", "#2f1d10");
const STUBBLE = ramp("#e6c2a2", "#d8b08e", "#b08268", "#7a5440");          // a day or two's growth over the skin
const DAD_PART = ramp("#70482a", "#4d301a", "#352113", "#2f1d10");
export const dad = {
  name: "Dad", height: 1.0,
  dim: { ...ADULT, headR: [0.056, 0.066, 0.063], shoulderW: 0.104, trunkTop: [0.108, 0.070], trunkLow: [0.106, 0.080], bellyFwd: 0.016,
         hipY: 0.490, thigh: 0.234, shin: 0.222, legR: [0.053, 0.034, 0.023], armR: [0.032, 0.026, 0.019], handR: 0.024 },
  skin: SKIN,
  hair: { mat: DAD_HAIR, bulk: [1.05, 1.10, 1.07], where: hairline({ front: 0.56, temple: 0.36, side: 0.16, back: -0.46, recede: 0.08, burn: 0.34, temples: 1.15 }),
          puffs: [[0.14, 0.80, 0.04, 0.80, 0.30, 0.84]],                     // combed back from the forehead and over to his left: high in front, smooth behind
          texture: (x, y, z) => (Math.abs(x + 0.40) < 0.06 && y > 0.40 && z > -0.30 ? DAD_PART : undefined) },      // the parting, on his right
  face: { eyes: { at: 1, full: ["--", "#i"], thin: ["-", "#"] }, iris: "#5f9140", eye: "#203018", lid: "#4a3020", brows: DAD_HAIR.tones[2], brow: { full: [0, 0, 0] },
          short: { mat: DAD_BEARD, stubble: STUBBLE, from: 0.55, chin: 0.90, side: 0.40 }, lip: "#b06a58", noseShade: true,      // stubble, and a short beard along the jaw and over the chin: no moustache
          jaw: 0.92, chin: 0.54, nose: 1.1, eyeX: 0.43, ear: 1.2, earOut: 1.03, big: { eyeW: 0.46, eyeH: 0.44 } },
  top: { mat: ramp("#ffe582", "#f4c043", "#cf9226", "#8f5d18"), sleeves: 0.62, hem: true, open: true, collar: true, pattern: FLOWERS },
  bottom: { kind: "shorts", mat: ramp("#a9b381", "#7f8d5c", "#59663f", "#39442b"), len: 0.72 },
  socks: { mat: WHITE, from: 0.52, stripes: [ramp("#f08a70", "#d2452f", "#a12f22", "#6e1f19"), ramp("#7fb2e6", "#3f79c2", "#2b5590", "#1b3760")] },
  shoes: { kind: "sandals", mat: ramp("#a8744a", "#7d5030", "#553521", "#332015"), sole: ramp("#6b4a30", "#4d3320", "#332015", "#1f130c") },
  gestures: [0, 1, 2, 3],                               // a nod, a point, a shrug, a hand on the hip
  pray: { high: -0.40, bow: 0.34 },                     // his big hands folded low in front of him, his head well down
};

// ---------- the Son: blonde, blue eyes, red cap, blue hoodie, backpack. Zany: he bounces, and his hands never stop. ----------
const SON_HAIR = ramp("#fbe7a0", "#e9c867", "#bf9640", "#83611f");          // blonde
const CAP = ramp("#ff7a62", "#de4a33", "#a93224", "#72201a");
const PACK = ramp("#b39bf5", "#8463d8", "#5f44a8", "#3d2b72");
const HOODIE = ramp("#93dcf2", "#4fc0e2", "#2e90b6", "#1f6483");
export const son = {
  name: "Son", height: 0.74,
  dim: CHILD,
  skin: SKIN,
  hair: { mat: SON_HAIR, bulk: 1.05, where: hairline({ front: 0.12, temple: 0.08, side: 0.0, back: -0.44, temples: 1.15 }) },      // a blonde mop: a fringe shows under the peak of his cap
  face: { eyes: { at: 0, full: ["#h", "ii"], thin: ["#", "i"] }, iris: "#4a8ad0", eye: "#1c3358", brows: SON_HAIR.tones[2], brow: { full: [0, -1, -1] }, blush: "#f3a68c",
          lip: "#a5523f", eyeX: 0.43, eyeY: -0.06, mouthY: -0.70, ear: 1.15, earOut: 1.03, jaw: 0.84, chin: 0.46, chinY: -0.80, nose: [0.65, 0.65, 0.75], smile: 1, mouthW: 0.26,
          big: { eyeW: 0.48, eyeH: 0.52, arch: 0.30, browUp: 0.70 } },
  top: { mat: HOODIE, sleeves: 2, hem: true },
  bottom: { kind: "shorts", mat: ramp("#5a668f", "#3c4563", "#293049", "#1a1f31"), len: 0.80 },
  socks: { mat: WHITE, from: 0.72 },
  shoes: { kind: "sneakers", mat: ramp("#ffffff", "#f1efe6", "#c4c0b2", "#8f8b80"), stripe: CAP, sole: ramp("#d9d5c8", "#b5b1a4", "#8a867c", "#5f5c55") },
  stance: "straps",                                     // thumbs hooked in the straps of his pack
  walk: { swing: 0.50, arm: 0.58, elbow: 0.95, pump: 0.30, lean: 0.10, lift: 1.3, bob: 0.05, wag: 0.10, sway: 0.020 },   // a bounce, fists pumping, head going from side to side
  gestures: [1, 4, 9, 2],                               // a point, both arms up, both hands waving, a shrug
  pray: { high: 0.06, bow: 0.32, out: 0.012 },          // his cap off and held in both hands in front of him (see below), for once standing still
  extras({ ball, limb, onHead, headPt, hp, wide, deep, d, hy, tw, J, parts, pose }) {
    const hr = d.headR;
    if ((pose.praying || 0) > 0.5) {
      // he has taken his cap off to pray: it hangs from his folded hands, crown outward
      const at = add(mix(J.R.palm, J.L.palm, 0.5), J.torso([0, -0.028, 0.012]));
      ball(at, [0.050, 0.030, 0.026], CAP, { part: parts.HELD }, tw);
      ball(add(at, J.torso([0, -0.036, 0.006])), [0.038, 0.013, 0.018], shifted(CAP, 1), { part: parts.HELD }, tw);       // its peak, hanging down
    } else {
    // cap: a dome over the top of the head and a peak out in front
    ball(headPt([0, 0.006, 0]), [hr[0] * 1.12, hr[1] * 1.10, hr[2] * 1.12], CAP, { part: parts.HAT, fn: (ux, uy, uz) => { const o = onHead(ux, uy, uz); return o[1] > (o[2] > 0 ? 0.30 - 0.10 * o[2] : 0.30 + 0.15 * o[2]) ? undefined : null; } }, hy);
    ball(hp(0, 0.52, 1.44), [0.056, 0.010, 0.046], shifted(CAP, 1), { part: parts.HAT }, hy);
    }
    // hood bunched behind the neck
    ball(add(J.neck, J.torso([0, -0.022, -0.052])), [0.064, 0.040, 0.042], shifted(HOODIE, 1), { part: parts.TORSO }, tw);
    // the pack: a soft upright block against his back, with a pocket on it. [half width, half depth], like the trunk.
    const body = [0.072, 0.040], pocket = [0.050, 0.020], r = wide(body), rp = wide(pocket), back = d.trunkTop[1] + 0.036;
    const onBack = (h, out) => add(J.spine(d.shoulderY - h), J.torso([0, 0, -(back + out)]));
    limb(onBack(0.050, 0), onBack(0.190, 0), r * 0.94, r, PACK, { part: parts.EXTRA, depth: deep(body) / r });
    limb(onBack(0.130, 0.034), onBack(0.186, 0.034), rp, rp, shifted(PACK, 1), { part: parts.EXTRA2, depth: deep(pocket) / rp });
    for (const sd of [1, -1]) limb(add(J.sh, J.torso([sd * 0.060, 0.012, 0.0])), add(J.spine(d.shoulderY - 0.17), J.torso([sd * 0.074, 0, d.trunkTop[1] * 0.80])), 0.011, 0.011, PACK, { part: parts.EXTRA, bias: 4 });
  },
};

// ---------- Mom: an emerald dress, pearls, long dark brown curls. Classy: she stands with her hands clasped and never hurries. ----------
const MOM_HAIR = ramp("#86563a", "#5a3520", "#3d2314", "#24140b");          // dark brown
const MOM_CURL = shifted(MOM_HAIR, 1);
/** Curls on a fall of hair: rings of shade fixed to it. u: down the fall (in curls), a: across it (-1 to 1), n: curls across. */
const curls = (u, a, n) => { const v = (a + 1) * n * 0.5 + (Math.floor(u) % 2) * 0.5, du = u - Math.floor(u) - 0.5, dv = v - Math.floor(v) - 0.5, r = Math.hypot(du, dv * 1.1); return r > 0.26 && r < 0.46 && du > -0.15; };
const EMERALD = ramp("#63d3a4", "#2aa27a", "#1b7459", "#104a3a");
const PEARL = ramp("#ffffff", "#f6efe2", "#d2c8b4", "#9c937f");
const LEATHER = ramp("#d9a877", "#b07a4a", "#7e5430", "#50341d");
export const mom = {
  name: "Mom", height: 0.93,
  dim: { ...WOMAN, bust: [0.002, 0.030], neckR: 0.84 },
  skin: SKIN,
  hair: { mat: MOM_HAIR, bulk: [1.16, 1.12, 1.14], where: hairline({ front: 0.52, temple: 0.28, side: -0.40, back: -1.0, sweep: 0.22, brow: 0.45, temples: 1.10 }), ears: false,
          texture: (x, y, z) => curl(x, y, z, 7) ? MOM_CURL : undefined },     // curls all over, falling past her shoulders (and see `extras`)
  face: { eyes: { at: 1, full: ["==.", "#i="], thin: ["=.", "#="] }, iris: "#8a5a2c", eye: "#2e1b0e", lid: "#2c1a10", brows: MOM_HAIR.tones[2], brow: { full: [0, -1, -1, 0] }, browW: 4, blush: "#f0a08a",
          lip: "#b8475c", lips: "#d4707e", eyeX: 0.43, nose: [0.65, 0.65, 0.75], noseShade: true, jaw: 0.80, chin: 0.40, chinY: -0.80, mouthW: 0.20, smile: 1,
          big: { eyeW: 0.46, eyeH: 0.46, lashes: 1, arch: 0.28 } },
  top: { mat: EMERALD, sleeves: 0.42, belt: shifted(EMERALD, 2), open: 0.034 },
  bottom: { kind: "skirt", mat: EMERALD, len: 1.05, flare: 1.20, folds: [[-0.55, 0.15], [0.60, 0.3], [0.15, 0.55]] },
  shoes: { kind: "pumps", mat: ramp("#fffaf0", "#efe2c8", "#c3b596", "#8e8168"), sole: ramp("#c9b99a", "#a39375", "#7a6d55", "#52483a") },
  stance: "clasped",
  walk: { swing: 0.40, arm: 0.20, lean: 0.02, twist: 0.09, sway: 0.016 },     // short steps, quiet arms, a little sway
  gestures: [0, 5, 8, 0],                               // a nod, a hand to the heart, an open hand
  pray: { high: 0.42, bow: 0.28 },                      // her hands folded at her breast
  pace: 150,
  extras({ ball, limb, hp, wide, deep, d, hy, tw, J, S, parts, pose }) {
    // her hair: long dark curls from the crown down her back, past her shoulders, and a fall of them over each shoulder
    const fall = [0.078, 0.030], foot = [0.070, 0.024], r0 = wide(fall), r1 = wide(foot);
    limb(hp(0, -0.02, -0.72), add(J.spine(d.shoulderY - 0.175), J.torso([0, 0, -(d.trunkTop[1] + 0.018)])), r0, r1, MOM_HAIR, { part: parts.HAIR, depth: deep(fall) / r0, bias: S * 0.012, fn: (t, a) => (curls(t * 5, a, 2.4) ? MOM_CURL : undefined) });
    for (const sd of [1, -1]) {
      const from = hp(sd * 0.94, -0.18, -0.02), to = add(J.sh, J.torso([sd * 0.072, -0.074, 0.010]));
      limb(from, to, 0.024, 0.020, MOM_HAIR, { part: parts.HAIR, fn: (t, a) => (curls(t * 4, a, 1.4) ? MOM_CURL : undefined) });
      ball(to, [0.022, 0.016, 0.018], MOM_HAIR, { part: parts.HAIR }, tw);      // the ends, curling up
    }
    // pearls: one at each ear, and a string of them at the neck
    for (const sd of [1, -1]) ball(hp(sd * 1.0, -0.34, -0.06), [0.007, 0.008, 0.007], PEARL, { part: parts.EXTRA }, hy);
    ball(add(J.sh, J.torso([0, -0.016, d.trunkTop[1] * 0.50])), [0.046, 0.034, 0.042], PEARL, {
      part: parts.EXTRA, bias: S * 0.03, fn: (ux, uy) => { const q = ux * ux * 0.8 + (uy + 1.05) ** 2; return q > 0.92 && q < 1.50 ? undefined : null; },
    }, tw);
    // a handbag, hanging from her left forearm: it swings clear of her skirt
    // (when she lifts her hands to pray it slides down to the crook of her elbow)
    const w = mix(J.L.elbow, J.L.wrist, 0.60 - 0.46 * (pose.praying || 0)), off = [w[0] - J.hipC[0], 0, w[2] - J.hipC[2]], far = Math.hypot(off[0], off[2]) || 1, clear = Math.max(1, (d.pelvisR[0] + 0.046) / far);
    const bag = [J.hipC[0] + off[0] * clear, w[1] - 0.084, J.hipC[2] + off[2] * clear];
    limb(add(w, [0, -0.004, 0]), add(bag, [0, 0.030, 0]), 0.006, 0.006, shifted(LEATHER, 1), { part: parts.EXTRA2 });
    ball(bag, [0.040, 0.034, 0.018], LEATHER, { part: parts.EXTRA2, fn: (ux, uy) => (uy < -0.55 ? shifted(LEATHER, 1) : undefined) }, tw);
  },
};

// ---------- Big Sister, 13: cardigan, pleated skirt, long flowing hair under a headband (no bangs). The reader: she stands holding one elbow, thinking. ----------
const BIG_HAIR = ramp("#8a583a", "#5e3824", "#3f2416", "#25150c");
const BIG_PART = shifted(BIG_HAIR, 1);
const INDIGO = ramp("#99a0f2", "#666cd6", "#474aa6", "#2e2f72");
const GRAY = ramp("#a9acba", "#7f8394", "#5b5e6e", "#3c3e4b");
export const bigsis = {
  name: "Big Sister", height: 0.87,
  dim: { ...blend(CHILD, WOMAN, 0.62), legR: [0.046, 0.030, 0.020], neckR: 0.82 },
  skin: SKIN,
  hair: { mat: BIG_HAIR, bulk: [1.08, 1.09, 1.08], where: hairline({ front: 0.58, temple: 0.34, side: -0.60, back: -1.2, brow: 0.45, temples: 1.10 }),          // no fringe: back off her face under the headband
          texture: (x, y, z) => (Math.abs(x) < 0.05 && y > 0.55 && z > 0.10 ? BIG_PART : undefined) },                                   // parted in the middle
  face: { eyes: { at: 1, full: ["==", "#i="], thin: ["=", "#"] }, iris: "#8a7038", eye: "#2c2410", lid: "#3a2416", brows: BIG_HAIR.tones[1], brow: { full: [0, 0, 0] }, blush: "#f2aa92",
          lip: "#b55f52", eyeX: 0.43, eyeY: 0.0, mouthY: -0.70, jaw: 0.80, chin: 0.40, chinY: -0.78, nose: [0.7, 0.65, 0.75], noseShade: true, mouthW: 0.18, smile: 0.5,
          big: { eyeW: 0.46, eyeH: 0.48, lashes: 1, arch: 0.20, browUp: 0.75 } },
  top: { mat: INDIGO, sleeves: 2, hem: true, band: WHITE, cuffs: WHITE, buttons: "#c9ccf7" },
  bottom: { kind: "skirt", mat: GRAY, len: 0.82, flare: 1.16, pleats: 9 },
  socks: { mat: WHITE, from: 0.10 },
  shoes: { kind: "shoes", mat: ramp("#8f5a3c", "#693e27", "#47291a", "#2a180f"), sole: ramp("#4a2e1f", "#332015", "#22150e", "#140c08") },
  stance: "elbow",
  walk: { swing: 0.43, arm: 0.30, lean: 0.04 },
  gestures: [0, 11, 6, 10],                             // a nod, a finger in the air, a hand to her chin, pointing ahead
  pray: { high: 0.46, bow: 0.31 },                      // exactly as she was taught: hands together at her breast, head bowed
  extras({ ball, limb, onHead, headPt, hp, wide, deep, d, hy, J, S, parts }) {
    const hr = d.headR;
    // long hair: down the back, and a lock in front of each shoulder
    const fall = [0.056, 0.022], foot = [0.044, 0.016], r0 = wide(fall), r1 = wide(foot);          // a curtain of hair: broad from behind, thin from the side
    limb(hp(0, -0.10, -0.66), add(J.spine(d.shoulderY - 0.150), J.torso([0, 0, -(d.trunkTop[1] + 0.016)])), r0, r1, BIG_HAIR, { part: parts.HAIR, depth: deep(fall) / r0, bias: S * 0.012 });
    for (const sd of [1, -1]) limb(hp(sd * 0.90, -0.30, 0.05), add(J.sh, J.torso([sd * 0.062, -0.050, 0.018])), 0.017, 0.012, BIG_HAIR, { part: parts.HAIR });
    // a headband
    ball(headPt([0, 0.004, 0]), [hr[0] * 1.13, hr[1] * 1.14, hr[2] * 1.13], INDIGO, { part: parts.HAT, fn: (ux, uy, uz) => { const o = onHead(ux, uy, uz); return o[1] > 0.05 && Math.abs(o[2] - 0.28) < 0.12 ? undefined : null; } }, hy);      // (just behind her hairline)
  },
};

// ---------- Little Sister, 7: pink overalls, yellow boots, pigtails. Small but mighty: fists on hips, and she stomps. ----------
const LIL_HAIR = ramp("#e8bb78", "#c08d4c", "#8d6230", "#5c3d1b");
const PINK = ramp("#ff9db4", "#f0607f", "#bd3f5e", "#802a41");
const SUN = ramp("#fff0a0", "#ffd23f", "#d59a1f", "#93640f");
const SMALL = { ...CHILD, headR: [0.078, 0.088, 0.084], neckY: 0.790, shoulderY: 0.760, waistY: 0.565, hipY: 0.462, thigh: 0.214, shin: 0.204, legR: [0.050, 0.036, 0.026], armR: [0.029, 0.025, 0.019], neckR: 0.92 };
export const lilsis = {
  name: "Little Sister", height: 0.67,
  dim: SMALL,
  skin: SKIN,
  hair: { mat: LIL_HAIR, bulk: 1.07, where: hairline({ front: 0.26, temple: 0.16, side: -0.06, back: -0.58, brow: 0.55, temples: 1.15 }) },          // a soft fringe: less forehead
  face: { eyes: { at: 0, full: ["#h=", "ii"], thin: ["#", "i"] }, iris: "#6a9ee0", eye: "#2c4f8a", lid: "#5a3a20", brows: LIL_HAIR.tones[2], brow: { full: [0, 0] }, browW: 2, blush: "#f59a8e",
          freckles: true, freckle: "#e0a07c", lip: "#c2605a", eyeX: 0.43, eyeY: -0.10, mouthY: -0.68, ear: 1.15, earOut: 1.03, jaw: 0.86, chin: 0.48, chinY: -0.76, nose: [0.55, 0.6, 0.7], smile: 1, mouthW: 0.22,
          big: { eyeW: 0.50, eyeH: 0.54, lashes: 1, arch: 0.30, browUp: 0.75 } },      // (her portrait: rounder eyes, a lash, brows up)
  top: { mat: WHITE, sleeves: 0.5 },
  bottom: { kind: "shorts", mat: PINK, len: 0.62, rise: 0.085, bib: { top: 0.078, half: 0.60, strap: 0.26 } },     // overalls: a high waist, a bib and two straps
  shoes: { kind: "boots", mat: SUN, sole: shifted(SUN, 2), shaft: 0.52 },     // rain boots
  stance: "akimbo",
  walk: { swing: 0.50, arm: 0.72, elbow: 0.12, lean: 0.09, lift: 1.25, bob: 0.03 },     // a stomp: straight arms, like a small soldier
  gestures: [0, 4, 7, 10],                              // a nod, both arms up, showing her muscles, pointing ahead
  pray: { high: 0.97, bow: 0.15, tight: true },         // with all her might: hands clasped tight under her chin, eyes squeezed shut
  pace: 145,
  extras({ sf, P, ball, limb, hp, d, hy, th, J, fine, parts }) {
    // pigtails: each starts at a yellow band high on the side of her head, puffs out, and hangs to a point beside her cheek
    for (const sd of [1, -1]) {
      const root = hp(sd * 0.90, 0.50, -0.12), off = (out, up, back = 0) => add(root, turn([sd * out, up, -back], hy));
      limb(off(0.016, -0.004), off(0.046, -0.034, 0.004), 0.018, 0.028, LIL_HAIR, { part: parts.HAIR });
      limb(off(0.046, -0.034, 0.004), off(0.052, -0.112, 0.014), 0.028, 0.010, LIL_HAIR, { part: parts.HAIR });
      ball(off(0.014, 0.004), [0.024, 0.026, 0.024], SUN, { part: parts.HAT }, hy);
    }
    // a star on the bib of her overalls
    if (fine && Math.cos(th) > 0.5) {
      const c = P(add(J.spine(d.shoulderY - 0.150), J.torso([0, 0, d.trunkTop[1] * 0.98]))), x = Math.round(c[0] - 0.5), y = Math.round(c[1] - 0.5), star = SUN.tones[0];
      for (const [i, k] of [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]]) sf.dot(x + i, y + k, star, parts.TORSO);
    }
  },
};

// =====================================================================================
// Egypt, about 2560 B.C.
// =====================================================================================
// Working men wear a short kilt of white linen and little else. Officials wear a longer one and a broad
// collar of beads, and paint a black line round their eyes. Heads are shaved, cropped close, or wear a
// short round wig.
const TAN = ramp("#ecb896", "#d19270", "#a16646", "#6c402a");            // skin that keeps indoors
const BROWN = ramp("#d59f6e", "#bb7c4d", "#8b5331", "#5b331d");          // skin
const DARK = ramp("#bd8858", "#9c6139", "#704125", "#482715");           // skin after a lifetime in the sun
const LINEN = ramp("#fffdf4", "#f5efde", "#cfc3a4", "#9a8c6c");
const WORN = ramp("#f6eeda", "#e4d8ba", "#bbab87", "#86795c");           // linen that has been worked in
const BLACK = ramp("#50506a", "#2b2a38", "#191822", "#0c0b12");          // hair, and wigs
const TURQ = ramp("#93d6d2", "#3f9aa3", "#2b6f7a", "#1b4750");
const GOLD = ramp("#ffeeb0", "#f0c35a", "#b98a2e", "#7a5a1c");
const LAPIS = ramp("#8fa8f0", "#4a66c8", "#30438e", "#1e2a5c");
const WOOD = ramp("#c99a66", "#a37443", "#77512c", "#4d331b");
const ROPE = ramp("#e4cc94", "#bf9e5e", "#8a6c36", "#5a4520");
const HIDE = ramp("#b98a5e", "#8f6238", "#664424", "#422b16");           // leather
const CLAY = ramp("#e6a878", "#c57d4d", "#915833", "#5f3921");
const PAPYRUS = ramp("#f6e2a8", "#e3c47e", "#b59653", "#7d6433");
const BREAD = ramp("#eac27e", "#c48e4a", "#96662e", "#684418");
const BROWN_EYES = "#6a4428";                                              // (the iris of a dark brown eye: in Egypt, in Rome and with Lot)
/** Hair shaved to the skin: only a shadow of it, a little darker than the scalp. */
const SHAVED = new Map([
  [TAN, ramp("#d19270", "#bc8262", "#935c40", "#6c402a")],
  [BROWN, ramp("#bb7c4d", "#a56c42", "#7d4a2c", "#5b331d")],
  [DARK, ramp("#9c6139", "#86522f", "#653a21", "#482715")],
]);
const shaved = (skin) => SHAVED.get(skin);
const cropped = hairline({ front: 0.70, temple: 0.60, side: 0.26, back: -0.34 });
/** A strap worn across the body, from one shoulder to the opposite hip, front and back. */
function strap({ J, limb, trunkAt, d, under, cloth, parts }, mat, from = 1, r = 0.008) {
  const lie = { [parts.TORSO]: under };
  for (const face of [1, -1]) {
    const a = add(J.sh, J.torso([from * 0.066, 0.010, face * 0.020])), b = trunkAt(d.waistY - 0.010, face > 0 ? -from * 1.25 : Math.PI + from * 1.25, 0.004);
    limb(a, b, r, r, mat, { part: parts.EXTRA, over: lie, bias: cloth * 2 });
  }
}
/** A plain band round the head, tied behind. */
function headband({ ball, limb, onHead, headPt, hp, d, hy, parts }, mat, at = 0.50) {
  const hr = d.headR;
  ball(headPt([0, 0.004, 0]), [hr[0] * 1.11, hr[1] * 1.11, hr[2] * 1.11], mat, { part: parts.HAT, fn: (ux, uy, uz) => { const q = onHead(ux, uy, uz), y = q[1] - (q[2] < 0 ? 0.14 * q[2] : 0); return Math.abs(y - at) < 0.11 ? undefined : null; } }, hy);
  for (const sd of [1, -1]) limb(hp(sd * 0.08, at - 0.18, -1.02), hp(sd * 0.22, at - 0.62, -1.10), 0.008, 0.005, mat, { part: parts.HAT });
}

const CAKE_BLACK = ramp("#3a3640", "#221f27", "#15131a", "#0c0b10"), CAKE_RED = ramp("#d0604a", "#a8402e", "#7a2c20", "#531c14");
// ---------- the scribe of the building site: cross-legged, a sheet across his knees. Fussy, and proud of his lists. ----------
export const scribe = {
  name: "Scribe", height: 0.98, seated: "ground", shadow: 0.25, span: 1.15,
  dim: { ...ADULT, shoulderW: 0.094, trunkTop: [0.100, 0.066], trunkLow: [0.098, 0.076], bellyFwd: 0.010, armR: [0.027, 0.023, 0.016], neckR: 0.92 },
  build: "soft",
  skin: TAN,
  hair: { mat: shaved(TAN), bulk: 1, where: cropped },
  face: { eyes: "kohl", eye: "#14121c", lid: "#14121c", white: "#f0e4cc", brows: "#2b2a38", browUp: 3, lip: "#7a4530", nose: [1.0, 1.0, 0.9], noseShade: true, jaw: 0.86, chin: 0.46, mouthW: 0.15 },
  top: {},
  bottom: { kind: "kilt", mat: LINEN, len: 0.92, flare: 1.05, sash: shifted(LINEN, 1) },
  shoes: { kind: "bare" },
  rest: { R: { hand: [0.034, -0.215, 0.180], bend: [1, -0.4, -0.5], grip: true }, L: { hand: [-0.074, -0.232, 0.150], bend: [-1, -0.4, -0.5], flat: true } },      // a pen in one hand, the other steadying the sheet
  stood: { hold: { L: { hand: [-0.052, -0.168, 0.098], bend: [-1, -0.5, -0.4], grip: true } }, rest: { R: { hand: [0.122, -0.300, 0.070], bend: [0.6, -0.6, -0.5], grip: true } } },     // on his feet: the sheet held against him, the pen in his other hand
  gestures: [11, 17, 1],                                // a finger in the air, counting off, making a point
  fidgets: { sit: ["pen"] },                            // he trims his pen
  extras(c) {
    const { ball, limb, hp, wide, deep, J, pose, parts } = c;
    wear.collar(c, { rows: [LAPIS, GOLD, TURQ], wide: 0.070, deep: 0.034, drop: 0.024 });
    // spare pens behind his ear
    limb(hp(1.02, 0.10, -0.30), hp(1.06, 0.34, 0.50), 0.004, 0.004, PAPYRUS, { part: parts.HAT });
    if (pose.fidget === "pen" && pose.fu > 0.16 && pose.fu < 0.84) limb(J.L.palm, add(J.L.palm, [0.026, 0.010, 0.014]), 0.0042, 0.0026, IRON, { part: parts.HELD });     // the little knife
    if (!pose.seated) {
      // on his feet: the sheet held upright against him in his left hand, the palette along its foot, and the pen
      const g = J.L.palm, w = [0.070, 0.010], r = wide(w);
      limb(add(g, [0.020, -0.012, 0.012]), add(g, [0.030, 0.085, 0.004]), r, r, PAPYRUS, { part: parts.EXTRA, depth: deep(w) / r, squareStart: true, squareEnd: true });
      limb(add(g, [-0.016, -0.016, 0.020]), add(g, [0.074, -0.016, 0.020]), 0.0100, 0.0100, WOOD, { part: parts.EXTRA2, squareStart: true, squareEnd: true });
      limb(J.R.palm, add(J.R.palm, [0.010, -0.046, 0.012]), 0.0045, 0.003, WOOD, { part: parts.HELD });
      return;
    }
    // the sheet across his knees, the palette with its two cakes of ink, and the pen
    const lap = add(mix(J.R.knee, J.L.knee, 0.5), [0, 0.060, -0.070]), w = [0.086, 0.012], r = wide(w);
    limb(add(lap, [0, 0.030, -0.044]), add(lap, [0, -0.004, 0.060]), r, r, PAPYRUS, { part: parts.EXTRA, depth: deep(w) / r, squareStart: true, squareEnd: true });
    // (the palette: a narrow slip of wood lying across his shins in front of the sheet, a cake of black ink and a cake of red in it)
    limb(add(lap, [-0.066, -0.014, 0.092]), add(lap, [0.040, -0.010, 0.100]), 0.0115, 0.0115, WOOD, { part: parts.EXTRA2, squareStart: true, squareEnd: true,
      fn: (t, nx) => (Math.abs(nx) > 0.62 ? undefined : t > 0.14 && t < 0.30 ? CAKE_BLACK : t > 0.40 && t < 0.56 ? CAKE_RED : undefined) });
    limb(J.R.palm, add(J.R.palm, [0.010, -0.046, 0.012]), 0.0045, 0.003, WOOD, { part: parts.HELD });
  },
};

// ---------- the water carrier by the river: old, wiry, sun-dark, and in no hurry at all ----------
const GRIZZLE = ramp("#f4f2ea", "#d9d6cc", "#aaa69a", "#77736a");
export const carrier = {
  name: "Water Carrier", height: 0.93, lean: 0.07,
  dim: { ...ADULT, shoulderW: 0.092, trunkTop: [0.094, 0.060], trunkLow: [0.082, 0.060], pelvisR: [0.086, 0.058, 0.066], armR: [0.024, 0.021, 0.016], legR: [0.043, 0.029, 0.020], neckR: 0.88 },
  build: "old",
  skin: DARK,
  hair: { mat: GRIZZLE, bulk: 1.03, where: hairline({ front: 0.80, temple: 0.60, side: 0.10, back: -0.40 }) },
  face: { eyes: "squint", eye: "#1c120c", lid: "#3a2014", brows: GRIZZLE.tones[2], browW: 2, shadow: ramp("#c4a080", "#a68468", "#7a5c46", "#4d382a"), shadowFrom: 0.45, lines: 1, nose: [1.1, 1.15, 1.1], noseShade: true, jaw: 0.82, chin: 0.44, lip: "#4f2a1a", ear: 1.15, mouthW: 0.20 },
  top: {},
  bottom: { kind: "kilt", mat: WORN, len: 0.62, flare: 1.02, sash: shifted(WORN, 1), wrap: true },
  shoes: { kind: "bare" },
  stance: "behind",
  walk: { swing: 0.34, arm: 0.20, lean: 0.10, lift: 0.8, bob: 0.01 },
  pace: 110,
  gestures: [0, 8, 19, 2],                              // a slow nod, an open hand, a thumb over the shoulder, a shrug
  extras(c) {
    const { ball, J, d, tw, parts } = c;
    wear.headcloth(c, { mat: WORN, brow: 0.52, tails: 0.46, bulk: 1.07, fold: true });
    // a water-skin slung on his back
    strap(c, HIDE, 1);
    ball(add(J.sh, J.torso([-0.030, -0.215, -(d.trunkTop[1] + 0.040)])), [0.058, 0.074, 0.044], HIDE, { part: parts.EXTRA2 }, tw);
    ball(add(J.sh, J.torso([-0.020, -0.130, -(d.trunkTop[1] + 0.036)])), [0.020, 0.024, 0.020], shifted(HIDE, 1), { part: parts.EXTRA2 }, tw);
  },
};

// ---------- Lot, Abram's nephew (Genesis 11:27 to 13:5): a herdsman of a rich household from Haran and Canaan ----------
// About forty, strong and weathered; grave, courteous, plain-spoken. He is the first person Dad meets, and he is plainly
// not an Egyptian: black hair to the neck bound with a plain band of red wool, a full black beard cut square, a long
// tunic of wool woven in bands of madder red, ochre and indigo on the undyed cloth, a leather belt, a fringed mantle of
// indigo over his left shoulder, sandals. He is found sitting cross-legged on the sand in the shade, at his prayers:
// his hands lifted a little in front of him, open, his head bowed (`pray`); his shepherd's staff lies on the sand at his
// side. When someone talks to him he looks up (`sit.nod`) and talks with his hands: an open hand, a hand to his chest,
// a nod toward the river, a hand raised in blessing. `lot-standing`, below, is the same man on his feet.
const WEATHER = ramp("#e4ac82", "#c78a5c", "#97603c", "#623c24");         // skin: sun and wind, a lifetime with flocks
const RAVEN = ramp("#4e4548", "#2d2629", "#1c1719", "#0f0b0d");           // his hair: black
const RAVEN_BEARD = ramp("#584d50", "#362e31", "#231d1f", "#130f10");     // his beard, a shade lighter, as beards are
const FLEECE = ramp("#f2e4c4", "#dccaa2", "#ae9a76", "#7a684c");          // undyed wool
const MADDER_WOOL = ramp("#e27a6c", "#be4b40", "#8c2f2b", "#5c1c1b");     // dyed with madder root
const OCHRE_WOOL = ramp("#f4c87a", "#daa24a", "#a8742c", "#704c1c");
const INDIGO_WOOL = ramp("#6f7bb0", "#46528a", "#2f3864", "#1d2240");
const STAFF = ramp("#b8915e", "#8e6a3e", "#664a28", "#433018");           // a herdsman's staff, dark with handling
const LOT_TAKES = 0.40;                                                   // getting up, he takes his staff up off the sand here (see `stood`)
export const lot = {
  name: "Lot", height: 1.02, seated: "ground", shadow: 0.27, span: 1.16, under: 0.10,
  dim: { ...ADULT, headR: [0.056, 0.066, 0.063], shoulderW: 0.106, trunkTop: [0.110, 0.072], trunkLow: [0.098, 0.074], bellyFwd: 0.006, pelvisR: [0.098, 0.064, 0.076],
         armR: [0.032, 0.027, 0.019], legR: [0.053, 0.034, 0.022], handR: 0.024, neckR: 1.10 },
  build: "strong",
  skin: WEATHER,
  hair: { mat: RAVEN, bulk: 1.08, where: hairline({ front: 0.64, temple: 0.48, side: -0.40, back: -0.95, burn: 0.62 }), puffs: [[0, -0.50, -0.56, 0.88, 0.52, 0.54]] },      // thick, to the neck
  face: { eyes: "deep", eye: "#1c120c", iris: BROWN_EYES, noseShade: true, brows: RAVEN.tones[1], browW: 4, beard: RAVEN_BEARD, beardLen: 0.17, beardSquare: true, beardW: 0.70, beardZ: 0.50, beardFrom: [-0.46, 0.10], moustache: RAVEN_BEARD, moustacheW: 0.30, moustacheZ: 0.95, mouthShows: true,
          lip: "#7a3e32", lines: 1, nose: [1.1, 1.15, 1.05], jaw: 0.92, chin: 0.56, chinZ: 0.46, mouthW: 0.20 },
  top: { mat: FLEECE, sleeves: 0.86, cuff: 0.010, trim: MADDER_WOOL, belt: shifted(HIDE, 1),
         bands: [[0.050, 0.088, MADDER_WOOL], [0.088, 0.100, INDIGO_WOOL], [0.150, 0.180, OCHRE_WOOL]] },
  bottom: { kind: "skirt", mat: FLEECE, len: 1.70, flare: 1.08,
            bands: [[0.20, 0.36, MADDER_WOOL], [0.36, 0.42, INDIGO_WOOL], [0.75, 0.88, OCHRE_WOOL], [1.20, 1.36, MADDER_WOOL], [1.36, 1.42, INDIGO_WOOL], [1.56, 9, OCHRE_WOOL]],
            sitBands: [[0.74, 0.90, OCHRE_WOOL], [1.50, 1.58, MADDER_WOOL], [1.58, 9, OCHRE_WOOL]],
            folds: [[-0.85, 0.3, 1.70, 0.08], [0.50, 0.5, 1.70, -0.08], [-0.15, 0.9, 1.70], [2.6, 0.3], [-2.5, 0.4]] },
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  hand: "R",
  sit: { nod: -0.06 },                                  // (sitting, he looks up at whoever stands talking to him)
  pray: { high: 0.85, out: 0.075, apart: 0.085, bow: 0.40 },      // his hands lifted a little in front of him, open, palms up; his head bowed
  gestures: [8, 5, 20, 21],                             // an open hand, a hand to his chest, a nod toward the river, a hand raised in blessing
  walk: { swing: 0.40, arm: 0.26, lean: 0.03 },
  pace: 130,
  stood: { span: 1.12, under: 0.10, hold: { L: { hand: [-0.178, -0.198, 0.122], bend: [-1, -0.3, -0.6], grip: true } }, pray: { high: 0.45, bow: 0.30 },      // on his feet: his staff in his left hand (and room below him for it on the sand, as he gets up)
           takeUp: LOT_TAKES },                         // getting up, his left hand goes down at his side, takes up the staff there, and he climbs up it
  extras(c) { lotGear(c); },
};
/** Lot's band, mantle and staff. Sitting, the staff lies on the sand at his side, nearer us than he is, and stays where it
    lies whichever way he turns to talk; standing, he has it in his left hand. */
function lotGear(c) {
  const { ball, onHead, headPt, d, hy, limb, pose, th, parts } = c, hr = d.headR;
  // a plain band of red wool round his head, tied behind under the hair
  ball(headPt([0, 0.004, 0]), [hr[0] * 1.11, hr[1] * 1.11, hr[2] * 1.11], MADDER_WOOL, { part: parts.HAT, fn: (ux, uy, uz) => { const q = onHead(ux, uy, uz), y = q[1] - (q[2] < 0 ? 0.14 * q[2] : 0); return Math.abs(y - 0.56) < 0.11 ? undefined : null; } }, hy);
  wear.mantle(c, { mat: INDIGO_WOOL, fringe: shifted(INDIGO_WOOL, -1), len: 0.38, front: 0.24 });
  if (!pose.seated && !(pose.rising < LOT_TAKES)) { wear.staff(c, "L", { mat: STAFF, top: 1.06, r: 0.0085, crook: true }); return; }      // (getting up, he takes it up on the way: `takeUp`)
  const cs = Math.cos(th), sn = Math.sin(th), on = (X, D, y = 0.0095) => [-X * cs + D * sn, y, X * sn + D * cs];     // (X: across the picture, D: toward us)
  limb(on(-0.36, 0.265), on(0.30, 0.265), 0.0105, 0.0098, STAFF, { part: parts.HELD });
  const crook = [on(0.30, 0.265), on(0.335, 0.269), on(0.360, 0.255), on(0.368, 0.231), on(0.356, 0.211), on(0.336, 0.211)];
  for (let i = 0; i + 1 < crook.length; i++) limb(crook[i], crook[i + 1], 0.0094, 0.0090, STAFF, { part: parts.HELD });
}
// ---------- the same man on his feet (a scene puts this in his place when he stands up) ----------
export const lotStanding = { ...upOf(lot), name: "Lot, standing", under: 0 };       // (what Figure.sit(false) makes of him: see `stood`)

// ---------- the overseer of works: a big stomach, a staff of office, and twenty years behind him that were on time ----------
export const overseer = {
  name: "Overseer", height: 1.0, lean: -0.02,
  dim: { ...ADULT, headR: [0.057, 0.066, 0.063], shoulderW: 0.106, trunkTop: [0.116, 0.078], trunkLow: [0.116, 0.088], bellyFwd: 0.020, paunch: [0.116, 0.080, 0.086, -0.012],
         pelvisR: [0.108, 0.064, 0.082], armR: [0.034, 0.029, 0.020], legR: [0.056, 0.036, 0.024], handR: 0.024, neckR: 1.12 },
  build: "fat",
  skin: BROWN,
  hair: { mat: BLACK, wig: true, bulk: [1.26, 1.15, 1.20], lift: [0, 0.006, -0.006], where: (x, y, z) => y > (z > 0.36 ? 0.38 : -0.50),
          texture: (ox, oy, oz, x, y) => ((y & 1) === 0 && ((x + ((y >> 1) & 1) * 2) & 3) === 0 ? shifted(BLACK, -1) : undefined) },      // a short round wig, in rows of curls
  face: { eyes: "kohl", eye: "#14121c", lid: "#14121c", white: "#f0e4cc", brows: "#191822", browTilt: 1, browW: 4, jowl: 0.92, jaw: 0.96, chin: 0.60, nose: [1.0, 1.1, 1.3], noseShade: true, lip: "#6a3420", mouthW: 0.26, smile: -1, ears: false },
  top: {},
  bottom: { kind: "kilt", mat: LINEN, len: 1.50, flare: 1.10, sash: shifted(LINEN, 1), folds: [[-0.9, 0.2], [0.85, 0.35], [-0.45, 0.6]] },
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  hold: { R: { hand: [0.205, -0.190, 0.100], bend: [0.25, -1, -0.45], grip: true } },
  stance: "hip",
  walk: { swing: 0.34, arm: 0.22, lean: 0.0, sway: 0.022, twist: 0.08 },
  pace: 135,
  gestures: [14, 10, 15, 16, 3],                        // a shaken fist, pointing, waving it all away, wiping his brow, a hand on his hip
  fidgets: { stand: ["tap"] },                          // he taps his staff on the ground
  extras(c) {
    const { limb, skirtAt, J, d, cloth, under, parts } = c;
    wear.collar(c, { rows: [TURQ, GOLD, LAPIS, GOLD] });
    for (const k of ["R", "L"]) limb(mix(J[k].shoulder, J[k].elbow, 0.40), mix(J[k].shoulder, J[k].elbow, 0.52), d.armR[0] + 0.003, d.armR[0] + 0.002, GOLD, { part: parts.EXTRA2, squareStart: true, squareEnd: true });     // an armlet on each arm
    wear.staff(c, "R", { mat: WOOD, top: 0.90, r: 0.0085, knob: GOLD });
    // the stiff front of his kilt: a starched panel that stands out from the waist to the knee
    if (skirtAt) limb(skirtAt(-0.30, 0.0, 0.008), skirtAt(0.98, 0.0, 0.040), 0.010, 0.064, shifted(LINEN, -1), { part: parts.DRAPE, depth: 0.3, squareEnd: true, bias: cloth, over: { [parts.SKIRT]: under } });
  },
};

// ---------- the hauling gang, "Friends of Khufu", on a break that has lasted since the wall began to hum ----------
const haulerBase = {
  name: "Hauler", top: {}, shoes: { kind: "bare" }, build: "strong",
  fidgets: { stand: ["roll"] },                         // they roll their shoulders
  bottom: { kind: "kilt", mat: WORN, len: 0.60, flare: 1.02, sash: shifted(WORN, 1), wrap: true },
};
// the one who does the talking: tall, easy, a coil of rope over his shoulder
export const hauler1 = {
  ...haulerBase, height: 1.03,
  dim: { ...ADULT, shoulderW: 0.108, trunkTop: [0.112, 0.070], trunkLow: [0.088, 0.064], armR: [0.034, 0.028, 0.019], legR: [0.053, 0.034, 0.023], neckR: 1.08 },
  skin: BROWN,
  hair: { mat: BLACK, bulk: 1.04, where: hairline({ front: 0.64, temple: 0.54, side: 0.20, back: -0.36 }) },
  face: { eyes: "plain", eye: "#14121c", iris: BROWN_EYES, brows: "#191822", jaw: 0.94, chin: 0.56, nose: [1.0, 1.0, 1.1], noseShade: true, lip: "#6a3420", smile: 1, mouthW: 0.26 },
  stance: "hip",
  walk: { swing: 0.46, arm: 0.40, lean: 0.05 },
  gestures: [1, 7, 2, 3],                               // making a point, showing his arms, a shrug, a hand on his hip
  extras(c) {
    const { J, limb, d, cloth, under, parts } = c;
    // the rope: a coil hung on his left shoulder, down to the hip
    const T = (x, y, z) => add(J.sh, J.torso([x, y, z])), back = d.trunkTop[1], lie = { [parts.TORSO]: under, [parts.SKIRT]: under, [parts.BELT]: under, [parts.ARM.L]: under };
    for (const [dx, r, m] of [[0, 0.012, ROPE], [0.014, 0.010, shifted(ROPE, 1)], [-0.012, 0.009, shifted(ROPE, 1)]]) {
      const loop = [T(-0.080 + dx, 0.024, 0), T(-0.066 + dx, -0.040, back * 0.80), T(-0.060 + dx, -0.150, back + 0.014), T(-0.070 + dx, -0.250, back * 0.60), T(-0.084 + dx, -0.290, 0),
                    T(-0.070 + dx, -0.250, -back * 0.60), T(-0.060 + dx, -0.150, -(back + 0.014)), T(-0.066 + dx, -0.040, -back * 0.80), T(-0.080 + dx, 0.024, 0)];
      for (let i = 0; i + 1 < loop.length; i++) limb(loop[i], loop[i + 1], r, r, m, { part: parts.EXTRA, over: lie, bias: cloth * 2 });
    }
  },
};
// the one who agrees: short, thick, arms folded, a man of few words and all of them "yes"
export const hauler2 = {
  ...haulerBase, height: 0.94,
  dim: { ...ADULT, headR: [0.057, 0.064, 0.063], shoulderW: 0.108, trunkTop: [0.118, 0.078], trunkLow: [0.104, 0.076], pelvisR: [0.100, 0.062, 0.078], armR: [0.037, 0.031, 0.021], legR: [0.057, 0.037, 0.025], handR: 0.024, neckR: 1.22, thigh: 0.232, shin: 0.218 },
  skin: DARK,
  hair: { mat: shaved(DARK), bulk: 1, where: cropped },
  face: { eyes: "deep", eye: "#14121c", iris: BROWN_EYES, brows: "#191822", browW: 4, jaw: 1.0, chin: 0.64, nose: [0.9, 1.0, 1.35], noseShade: true, lip: "#4f2a1a", mouthW: 0.22, ear: 1.1 },
  stance: "folded",
  walk: { swing: 0.42, arm: 0.34, lean: 0.06, sway: 0.018 },
  gestures: [0, 12, 19, 0],                             // a nod, arms folded, a thumb over his shoulder
  extras({ limb, J, d, parts }) {
    for (const k of ["R", "L"]) limb(mix(J[k].elbow, J[k].wrist, 0.80), mix(J[k].elbow, J[k].wrist, 0.98), d.armR[2] + 0.005, d.armR[2] + 0.004, WORN, { part: parts.EXTRA2, squareStart: true, squareEnd: true });     // his wrists bound with linen, for the rope
  },
};
// the one who eats: young, long-limbed, a loaf in his hand and his mouth full
export const hauler3 = {
  ...haulerBase, height: 0.99,
  dim: { ...ADULT, shoulderW: 0.098, trunkTop: [0.100, 0.064], trunkLow: [0.080, 0.060], pelvisR: [0.088, 0.060, 0.068], armR: [0.029, 0.024, 0.017], legR: [0.047, 0.031, 0.021], neckR: 0.96 },
  skin: TAN,
  hair: { mat: BLACK, bulk: [1.10, 1.12, 1.10], where: hairline({ front: 0.52, temple: 0.40, side: 0.06, back: -0.44 }), puffs: [[0.34, 0.80, 0.34, 0.50, 0.34, 0.48], [-0.36, 0.78, 0.20, 0.50, 0.36, 0.52], [0, 0.90, -0.30, 0.52, 0.30, 0.56], [0.70, 0.36, -0.10, 0.36, 0.40, 0.50], [-0.70, 0.36, -0.10, 0.36, 0.40, 0.50]],
          texture: (ox, oy, oz, x, y) => (((x + y) & 3) === 0 && (y & 1) === 0 ? shifted(BLACK, -1) : undefined) },     // a mop of curls
  face: { eyes: "wide", eye: "#14121c", brows: "#191822", jaw: 0.84, chin: 0.44, nose: [0.9, 0.9, 0.9], noseShade: true, lip: "#7a4530", mouthW: 0.20, ear: 1.1 },
  hold: { R: { hand: [0.036, -0.012, 0.110], bend: [1, -0.8, 0.1], grip: true } },
  walk: { swing: 0.46, arm: 0.44, lean: 0.05, bob: 0.02 },
  gestures: [0, 8, 2, 0],                               // a nod with his mouth full, an open hand, a shrug
  extras({ ball, J, parts }) {
    ball(add(J.R.palm, [0, 0.014, 0.008]), [0.030, 0.020, 0.028], BREAD, { part: parts.HELD });       // the loaf
  },
};

// ---------- the guard at the foot of the stair: tall, bored, and very hot ----------
export const guard = {
  name: "Guard", height: 1.06,
  dim: { ...ADULT, shoulderW: 0.102, trunkTop: [0.104, 0.066], trunkLow: [0.084, 0.062], armR: [0.030, 0.025, 0.018], legR: [0.049, 0.032, 0.022], neckR: 1.0 },
  build: "lean",
  skin: BROWN,
  hair: { mat: BLACK, bulk: 1.04, where: hairline({ front: 0.60, temple: 0.50, side: 0.14, back: -0.42 }) },
  face: { eyes: "heavy", eye: "#14121c", iris: BROWN_EYES, lid: "#3a2014", brows: "#191822", jaw: 0.88, chin: 0.50, chinY: -0.88, nose: [1.15, 1.0, 1.0], noseShade: true, lip: "#6a3420", mouthW: 0.20, smile: -1 },
  top: {},
  bottom: { kind: "kilt", mat: LINEN, len: 0.70, flare: 1.02, sash: HIDE, wrap: true },
  shoes: { kind: "bare" },
  hold: { R: { hand: [0.200, -0.150, 0.100], bend: [0.25, -1, -0.45], grip: true } },
  walk: { swing: 0.40, arm: 0.24, lean: 0.03 },
  gestures: [0, 15, 16, 0],                             // a nod, waving someone away, wiping his brow
  fidgets: { stand: ["lean"] },                         // he leans on his staff
  extras(c) {
    headband(c, LINEN, 0.50);
    strap(c, HIDE, -1, 0.009);
    wear.staff(c, "R", { mat: WOOD, top: 1.08, r: 0.0075 });
  },
};

// ---------- the same guard, later: holding Dad's windshield shade up to the sun, and regretting it ----------
// The shade is painted (art/scenes/egypt-site/shade.png) and laid over him by the scene. His fists are where
// the two near corners of that panel are when he stands on the sunny spot (330, 520) facing east: the corner
// toward us in his right hand (345, 436 in the picture), the far one, higher, in his left (350, 413). Nothing
// here moves those hands: he breathes, sags at the knees and hangs his head, and talks with his head alone.
// His staff lies on the sand beside him. Turned any other way, or stood anywhere else, his hands miss the shade.
export const guardShade = {
  ...guard,
  name: "Guard, holding the shade", span: 1.34, under: 0.17,       // (room in his picture for the staff on the ground)
  stance: "weary", lean: -0.050,
  hold: {
    R: { hand: [0.118, -0.176, 0.084], bend: [0.55, -1, -0.35], grip: true, still: true },
    L: { hand: [-0.118, -0.073, 0.142], bend: [-0.55, -1, -0.35], grip: true, still: true },
  },
  // With his hands full he talks with his head. It hangs while he is silent; to speak he lifts it and shakes it (2),
  // looks up from under his brows (16), throws it back at the sky (4), or nods (0). The arms of those gestures never happen.
  gestures: [2, 16, 4, 0],
  fidgets: { only: true, stand: ["look"] },             // (his hands are on the shade, where it is painted: only his head moves)
  extras(c) {
    const { limb, parts } = c;
    headband(c, LINEN, 0.50);
    strap(c, HIDE, -1, 0.009);
    if (!c.pose.gait) limb([-0.330, 0.009, -0.400], [-0.110, 0.009, 0.600], 0.0090, 0.0078, WOOD, { part: parts.HELD });       // the staff, laid down on the sand on his left (it stays there if he walks off)
  },
};

const OILJAR = ramp("#f8e9c6", "#e4cc9c", "#b39662", "#7a6239");
// ---------- the boy who fills the lamps: twelve, thin, quick, and the only one who saw it ----------
export const lampboy = {
  name: "Lamp Boy", height: 0.80, seated: "chair", plain: true,          // found sitting on the edge of the stone bench in the gallery, his feet just reaching the floor
  dim: { ...blend(CHILD, ADULT, 0.40), trunkTop: [0.090, 0.058], trunkLow: [0.078, 0.056], pelvisR: [0.084, 0.058, 0.064], armR: [0.022, 0.019, 0.015], legR: [0.040, 0.027, 0.019], neckR: 0.82 },
  skin: BROWN,
  hair: { mat: shaved(BROWN), bulk: 1, where: cropped },
  face: { eyes: "wide", eye: "#14121c", brows: "#191822", browUp: 3, blush: "#d48a62", eyeY: 0.0, mouthY: -0.72, jaw: 0.82, chin: 0.42, chinY: -0.80, nose: [0.7, 0.75, 0.8], noseShade: true, lip: "#7a4530", mouthW: 0.18, ear: 1.15 },
  top: {},
  bottom: { kind: "kilt", mat: WORN, len: 0.60, flare: 1.04, sash: shifted(WORN, 1) },
  shoes: { kind: "bare" },
  hold: { L: { hand: [-0.020, -0.200, 0.100], bend: [-1, -0.6, -0.3], curl: 1.0 } },       // the oil jar, held against him
  hand: "R",
  walk: { swing: 0.50, arm: 0.40, lean: 0.08, lift: 1.15, bob: 0.03 },
  pace: 175,
  gestures: [10, 19, 11, 2],                            // pointing, a thumb over his shoulder, a finger in the air, a shrug
  fidgets: { sit: ["yawn"] },                           // a yawn
  sit: { seat: 0.247, lean: 0.04, knees: 0.06, solid: true },      // the gallery's stone bench as it is painted: 40 pixels above the floor where he sits
  extras({ ball, limb, hp, hy, J, d, parts }) {
    // the side-lock that children wear: one plait from the right temple, curled at its end
    limb(hp(0.96, 0.34, 0.10), hp(1.12, -0.36, 0.06), 0.012, 0.010, BLACK, { part: parts.HAIR });
    limb(hp(1.12, -0.36, 0.06), hp(1.04, -0.92, 0.12), 0.010, 0.008, BLACK, { part: parts.HAIR });
    ball(hp(0.92, -1.02, 0.16), [0.012, 0.012, 0.012], BLACK, { part: parts.HAIR }, hy);
    // a small jar of lamp oil in the crook of his left arm
    const at = add(mix(J.L.wrist, J.L.palm, 0.5), [0.012, 0.030, 0.010]);
    // (pale buff ware: red clay would be lost against his skin)
    ball(at, [0.033, 0.041, 0.033], OILJAR, { part: parts.HELD });
    limb(add(at, [0, 0.034, 0]), add(at, [0, 0.056, 0]), 0.014, 0.019, OILJAR, { part: parts.HELD, squareEnd: true });
    ball(add(at, [0, 0.057, 0]), [0.015, 0.006, 0.015], shifted(HIDE, 2), { part: parts.HELD });        // its mouth, dark with oil
    void d;
  },
};

// ---------- the goldsmith: very old, very cheerful, and deaf as a post from fifty years of hammering ----------
export const goldsmith = {
  name: "Goldsmith", height: 0.92, seated: "chair", shadow: 0.22, span: 1.15,
  dim: { ...ADULT, headR: [0.056, 0.066, 0.063], shoulderW: 0.090, trunkTop: [0.094, 0.062], trunkLow: [0.086, 0.066], bellyFwd: 0.006, pelvisR: [0.088, 0.058, 0.068], armR: [0.025, 0.023, 0.018], legR: [0.043, 0.030, 0.020], handR: 0.024, neckR: 0.86 },
  build: "old",
  skin: TAN,
  hair: { mat: GRIZZLE, bulk: 1.03, where: hairline({ front: 0.30, temple: 0.24, side: 0.06, back: -0.36, top: 0.40 }) },      // bald, with a fringe of white round the back
  face: { eyes: "squint", eye: "#1c120c", iris: BROWN_EYES, lid: "#4a2a1a", brows: GRIZZLE.tones[2], browUp: 2, lines: 1, nose: [1.1, 1.2, 1.3], noseShade: true, jaw: 0.84, chin: 0.46, lip: "#7a4530", mouthW: 0.30, smile: 1, ear: 1.45 },
  top: {},
  bottom: { kind: "kilt", mat: WORN, len: 0.90, flare: 1.05, sash: shifted(HIDE, 1) },
  apron: { mat: HIDE, half: 0.95, len: 1.0 },           // a leather apron over his knees
  shoes: { kind: "bare" },
  hold: { R: { hand: [0.085, -0.230, 0.150], bend: [1, -0.4, -0.5], grip: true } },       // his little hammer
  gestures: [13, 0, 8, 2],                              // a hand cupped to his ear, a nod, an open hand, a shrug
  sit: { seat: "stool", lean: 0.14, drawn: true },
  stood: { hold: { R: { hand: [0.150, -0.318, 0.060], bend: [0.4, -1, -0.4], grip: true } } },      // on his feet, the hammer at his side
  fidgets: { sit: ["light"] },                          // he holds something small up to the light and turns it
  extras(c) {
    const { limb, ball, J, pose, parts } = c;
    wear.stool(c, { mat: WOOD, r: 0.066 });
    if (pose.fidget === "light" && pose.fu > 0.14 && pose.fu < 0.86) ball(add(J.L.tip, [0, 0.010, 0]), [0.0090, 0.0090, 0.0090], GOLD, { part: parts.HELD });     // a bead of gold, between finger and thumb
    const g = J.R.palm;
    limb(add(g, [0, -0.012, -0.006]), add(g, [0, 0.050, 0.020]), 0.0055, 0.0055, WOOD, { part: parts.HELD });
    limb(add(g, [0, 0.050, 0.004]), add(g, [0, 0.054, 0.040]), 0.011, 0.011, ramp("#d8d2c8", "#a9a296", "#77716a", "#4c4843"), { part: parts.HELD, squareStart: true, squareEnd: true });
  },
};

// ---------- the same goldsmith, after the trade: in Dad's sunglasses, and the whole world the color of good beer ----------
// Everything but his face is the goldsmith's own, so one can be put in the other's place without a jump.
const LENS = ramp("#3a3c4c", "#24252f", "#14151c", "#09090d");
export const goldsmithShades = {
  ...goldsmith,
  name: "Goldsmith, in sunglasses",
  face: { ...goldsmith.face, wrap: LENS, eyes: "plain", lines: 0, mouthW: 0.38, smile: 1 },      // a broader, easier smile, and nothing left to squint at
};

// =====================================================================================
// Rome, 44 B.C.
// =====================================================================================
// Ordinary people wear a belted tunic to the knee, pulled up a little through the belt. A citizen on
// business wears the toga over it. Women wear a long tunic to the feet.
const OLIVE = ramp("#f6d4ae", "#e6b084", "#b67e56", "#7d4f35");           // skin
const RUDDY = ramp("#f4c4a0", "#e0a07a", "#b06e50", "#76402e");           // a red face over a hot stove
const SALLOW = ramp("#f8e0c6", "#ecc6a4", "#be9070", "#84624c");          // a face that never sees the sun
const SWARTHY = ramp("#e0ac80", "#c98c5e", "#9a643e", "#663e26");         // skin that lives out of doors
const WOOL = ramp("#ffffff", "#f8f6f0", "#c4c2bc", "#8c8a86");            // the white of a toga
const OLDWOOL = ramp("#f4eedc", "#e2dac4", "#b8ae94", "#857c66");         // and of one that has seen forty winters
const UNDYED = ramp("#f2e6ca", "#decca6", "#b09c78", "#7c6c50");          // plain wool
const UNDYED_PALE = ramp("#fbf4e0", "#ece2c8", "#beb294", "#887c62");     // a tunic of good wool, not quite white
const PURPLE = ramp("#b870a4", "#8c3f78", "#642656", "#401638");          // the stripe of rank
const OCHRE = ramp("#f4c680", "#dc9e4c", "#a8702c", "#724a1c");
const MADDER = ramp("#e88880", "#c65a54", "#923a36", "#602222");          // a dull red
const WOAD = ramp("#b0c8de", "#84a4c2", "#5a7a96", "#3a5268");            // a dull blue
const MOSS = ramp("#b4bc8e", "#8e9868", "#667046", "#434a2e");
const DUN = ramp("#cdbc9c", "#ae9a7c", "#806f58", "#54483a");             // no color at all
const RED_LEATHER = ramp("#e4745e", "#bc4631", "#882e20", "#5c1e16");
const DARK_HAIR = ramp("#6a5444", "#44342a", "#2c211a", "#18110d");
const GREY_HAIR = ramp("#d0ccc4", "#a8a39a", "#7c7770", "#54504b");
const IRON = ramp("#c8ccd2", "#8e949c", "#62676e", "#3e4248");
const BRONZE = ramp("#f4d890", "#d4a850", "#9c7430", "#684a1c");
const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const norm = (v) => { const n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / n, v[1] / n, v[2] / n]; };
/** The way a thing held in a fist sticks out of the top of it: at right angles to the hand, along the thumb's side. */
const upFromFist = (A) => { const v = [A.thumb1[0] - A.thumb0[0], A.thumb1[1] - A.thumb0[1], A.thumb1[2] - A.thumb0[2]], k = dot3(v, A.hDir); return norm([v[0] - A.hDir[0] * k, v[1] - A.hDir[1] * k, v[2] - A.hDir[2] * k]); };
const along = (p, dir, k) => [p[0] + dir[0] * k, p[1] + dir[1] * k, p[2] + dir[2] * k];

// ---------- the keeper of the snack bar: stout, red in the face, and never once out of breath ----------
export const keeper = {
  name: "Snack-Bar Keeper", height: 0.95,
  dim: { ...ADULT, headR: [0.058, 0.066, 0.064], shoulderW: 0.104, trunkTop: [0.112, 0.076], trunkLow: [0.112, 0.088], bellyFwd: 0.018, paunch: [0.108, 0.062, 0.078, 0.022],
         pelvisR: [0.104, 0.064, 0.080], armR: [0.035, 0.030, 0.021], legR: [0.055, 0.036, 0.024], handR: 0.024, neckR: 1.14, thigh: 0.232, shin: 0.218 },
  skin: RUDDY,
  hair: { mat: DARK_HAIR, bulk: [1.10, 1.06, 1.08], where: hairline({ front: 0.30, temple: 0.26, side: 0.06, back: -0.42, top: 0.50 }) },       // bald on top, curls round the sides
  face: { eyes: "plain", eye: "#2a1a12", iris: BROWN_EYES, brows: DARK_HAIR.tones[2], browW: 4, browUp: 3, blush: "#e2805e", jowl: 0.88, jaw: 0.98, chin: 0.62, nose: [0.95, 1.1, 1.45], noseShade: true, lip: "#8a3e30", smile: 1, mouthW: 0.30 },
  top: { mat: OCHRE, sleeves: 0.46, cuff: 0.014, belt: shifted(HIDE, 1), beltLow: 0.040 },
  stance: "carry",
  bottom: { kind: "skirt", mat: OCHRE, len: 0.98, flare: 1.08, folds: [[-0.95, 0.2], [1.0, 0.3], [2.4, 0.2], [-2.3, 0.35]] },
  apron: { mat: ramp("#fbf6e6", "#eadfc6", "#bdb195", "#8a7f66"), half: 0.90, len: 0.86 },
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  walk: { swing: 0.36, arm: 0.30, sway: 0.024, twist: 0.10, lean: 0.02 },
  pace: 140,
  gestures: [1, 18, 9, 2, 5],                           // a point with the ladle, both hands wide, both hands waving, a shrug, a hand to his heart
  fidgets: { stand: ["wipe"] }, fidgetHand: "L",        // he wipes down his counter with the cloth off his shoulder
  extras({ limb, ball, J, pose, parts }) {
    // the ladle, which is never out of his hand
    const up = upFromFist(J.R), dir = norm([up[0] - J.R.hDir[0] * 0.35, up[1] - J.R.hDir[1] * 0.35, up[2] - J.R.hDir[2] * 0.35]), g = J.R.palm;
    limb(along(g, dir, -0.024), along(g, dir, 0.150), 0.0055, 0.0050, WOOD, { part: parts.HELD });
    ball(along(g, dir, 0.166), [0.022, 0.016, 0.022], BRONZE, { part: parts.HELD });
    // a cloth over his left shoulder (in his hand while he wipes the counter with it)
    if (pose.fidget === "wipe" && pose.fu > 0.12 && pose.fu < 0.88) {
      const g = J.L.palm;
      limb(add(g, [0, -0.012, -0.020]), add(g, [0, -0.012, 0.040]), 0.026, 0.024, WHITE, { part: parts.HELD, squareStart: true, squareEnd: true, depth: 0.3 });
      return;
    }
    limb(add(J.L.shoulder, J.torso([0.014, 0.030, 0.030])), add(J.L.shoulder, J.torso([0.020, -0.090, 0.058])), 0.020, 0.024, WHITE, { part: parts.EXTRA2 });
    limb(add(J.L.shoulder, J.torso([0.014, 0.030, -0.020])), add(J.L.shoulder, J.torso([0.018, -0.060, -0.056])), 0.020, 0.022, WHITE, { part: parts.EXTRA2 });
  },
};

// ---------- the washerwoman: strong arms, her tunic kilted up out of the wet, her hair in a cloth. Brisk, and kind. ----------
export const washer = {
  name: "Washerwoman", height: 0.94,
  dim: { ...WOMAN, shoulderW: 0.092, trunkTop: [0.096, 0.066], trunkLow: [0.084, 0.064], pelvisR: [0.102, 0.062, 0.078], armR: [0.030, 0.026, 0.018], handR: 0.021, legR: [0.050, 0.032, 0.021], bust: [0.004, 0.034], neckR: 0.92 },
  skin: SWARTHY,
  hair: { mat: DARK_HAIR, bulk: 1.05, where: hairline({ front: 0.56, temple: 0.42, side: 0.04, back: -0.40 }) },
  face: { eyes: "girl", eye: "#2a1a12", iris: BROWN_EYES, lid: "#3a2218", brows: DARK_HAIR.tones[2], blush: "#e08a70", lip: "#9a4038", nose: [0.9, 0.85, 0.95], noseShade: true, jaw: 0.86, chin: 0.44, chinY: -0.80, smile: 1, mouthW: 0.24 },
  top: { mat: WOAD, sleeves: 0.40, cuff: 0.016, belt: shifted(ROPE, 1), blouse: 0.020 },
  bottom: { kind: "skirt", mat: WOAD, len: 1.42, flare: 1.14, folds: [[-0.7, 0.1], [0.75, 0.2], [0.1, 0.5], [2.6, 0.2]] },
  shoes: { kind: "bare" },
  stance: "akimbo",
  walk: { swing: 0.48, arm: 0.50, lean: 0.07, sway: 0.016 },
  pace: 185,
  gestures: [3, 15, 8, 1],                              // a hand on her hip, waving it away, an open hand, making a point
  fidgets: { stand: ["wring"] },                        // she wrings out the wet cloth
  extras(c) {
    const { limb, J, pose, parts } = c;
    wear.headcloth(c, { mat: MADDER, brow: 0.56, nape: 0.62, tails: 0.26, bulk: 1.12 });
    if (pose.fidget === "wring" && pose.fu > 0.14 && pose.fu < 0.86) {
      // the cloth twisted between her two fists, its ends hanging
      const a = J.R.palm, b = J.L.palm;
      limb(a, b, 0.016, 0.016, WOOL, { part: parts.HELD });
      limb(add(a, [0.004, -0.008, 0.004]), add(a, [0.012, -0.070, 0.010]), 0.013, 0.016, WOOL, { part: parts.HELD });
      limb(add(b, [-0.004, -0.008, 0.004]), add(b, [-0.010, -0.058, 0.012]), 0.013, 0.015, WOOL, { part: parts.HELD });
      return;
    }
    // a wet cloth over her shoulder
    limb(add(J.R.shoulder, J.torso([-0.014, 0.028, 0.030])), add(J.R.shoulder, J.torso([-0.024, -0.110, 0.056])), 0.020, 0.026, WOOL, { part: parts.EXTRA2 });
    limb(add(J.R.shoulder, J.torso([-0.014, 0.028, -0.020])), add(J.R.shoulder, J.torso([-0.020, -0.070, -0.052])), 0.020, 0.022, WOOL, { part: parts.EXTRA2 });
  },
};

// ---------- the street boy: ten, ragged, barefoot, sharp as a tack ----------
export const urchin = {
  name: "Street Boy", height: 0.72, seated: "chair", shadow: 0.20,
  dim: { ...CHILD, trunkTop: [0.090, 0.060], trunkLow: [0.080, 0.058], pelvisR: [0.084, 0.056, 0.064], armR: [0.022, 0.019, 0.015], legR: [0.039, 0.028, 0.020], neckR: 0.86 },
  skin: SWARTHY,
  hair: { mat: DARK_HAIR, bulk: [1.10, 1.12, 1.10], where: hairline({ front: 0.42, temple: 0.30, side: -0.12, back: -0.56 }), puffs: [[0.40, 0.84, 0.30, 0.40, 0.26, 0.40], [-0.30, 0.90, 0.0, 0.44, 0.26, 0.44], [0.10, 0.60, 0.86, 0.50, 0.22, 0.30], [-0.80, 0.50, -0.30, 0.30, 0.34, 0.40]] },       // never seen a comb
  face: { eyes: "bright", eye: "#2a1a12", iris: BROWN_EYES, brows: DARK_HAIR.tones[2], blush: "#e09070", noseShade: true, eyeY: -0.06, mouthY: -0.70, jaw: 0.82, chin: 0.44, chinY: -0.80, nose: [0.6, 0.65, 0.75], lip: "#8a4636", smile: 1, mouthW: 0.28, ear: 1.15 },
  top: { mat: DUN, sleeves: 0.28, cuff: 0.016, belt: shifted(ROPE, 2) },
  bottom: { kind: "skirt", mat: DUN, len: 0.72, flare: 1.10 },
  shoes: { kind: "bare" },
  walk: { swing: 0.52, arm: 0.60, lean: 0.10, lift: 1.2, bob: 0.04 },
  pace: 190,
  gestures: [10, 19, 2, 1],                             // pointing, a thumb over his shoulder, a shrug, making a point
  fidgets: { sit: ["scratch"] },                        // he scratches his head
  sit: { seat: "step", lean: 0.16, knees: 0.22, solid: true },      // the kerb
  extras({ sf, P, trunkAt, d, fine, parts }) {
    // a patch on his tunic
    if (fine) { const q = P(trunkAt(d.waistY + 0.060, 0.45)), m = shifted(DUN, 1).tones[1]; for (const [i, j] of [[0, 0], [1, 0], [0, 1], [1, 1], [2, 1], [2, 0]]) sf.dot(q[0] + i, q[1] + j, m, parts.TORSO); }
  },
};

// ---------- the soothsayer: old, gloomy, bad knees, and right about everything ----------
export const soothsayer = {
  name: "Soothsayer", height: 0.96, seated: "chair", shadow: 0.24, span: 1.15,
  dim: { ...ADULT, shoulderW: 0.092, trunkTop: [0.094, 0.062], trunkLow: [0.084, 0.062], pelvisR: [0.088, 0.058, 0.068], armR: [0.024, 0.021, 0.016], legR: [0.043, 0.029, 0.020], neckR: 0.86 },
  skin: OLIVE,
  hair: { mat: GRIZZLE, bulk: 1.04, where: hairline({ front: 0.40, temple: 0.30, side: 0.0, back: -0.50, top: 0.62 }) },
  face: { eyes: "deep", eye: "#2a1a12", iris: BROWN_EYES, brows: GRIZZLE.tones[2], browW: 4, beard: GRIZZLE, beardLen: 0.16, lines: 2, nose: [1.2, 1.25, 1.0], noseShade: true, jaw: 0.80, chin: 0.42, chinY: -0.90, lip: "#7a4636", smile: -1, mouthW: 0.20 },
  top: { mat: UNDYED, sleeves: 0.46 },
  bottom: { kind: "skirt", mat: OLDWOOL, len: 1.82, flare: 1.10, folds: [[-0.9, 0.3, 1.82, 0.1], [0.6, 0.5, 1.82, -0.1], [0.0, 0.8, 1.82], [2.5, 0.2], [-2.4, 0.4]] },
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  hold: { R: { hand: [0.215, -0.150, 0.110], bend: [0.3, -1, -0.3], grip: true } },
  gestures: [11, 2, 0, 16],                             // a finger in the air, a shrug, a nod, a hand across his brow
  fidgets: { sit: ["beard"] },                          // he strokes his beard
  riseMs: 1350,                                         // (his knees)
  stood: { walk: { swing: 0.30, arm: 0.16, lean: 0.10, lift: 0.75 }, pace: 95 },
  sit: { seat: 0.134, lean: 0.20, knees: 0.14, solid: true },      // a step of the temple of Saturn as it is painted (ten pixels high where he sits): his place is the tread below his seat
  extras(c) {
    wear.toga(c, { mat: OLDWOOL, hood: true });
    wear.staff(c, "R", { mat: WOOD, top: 0.86, r: 0.0070, crook: true });
  },
};

// ---------- the senator: late, pompous, and without his clean toga ----------
export const senator = {
  name: "Senator", height: 1.0, lean: -0.02,
  dim: { ...ADULT, headR: [0.057, 0.066, 0.063], trunkTop: [0.110, 0.074], trunkLow: [0.106, 0.082], bellyFwd: 0.014, pelvisR: [0.100, 0.064, 0.078], armR: [0.031, 0.027, 0.019], neckR: 1.06 },
  skin: OLIVE,
  hair: { mat: GREY_HAIR, bulk: 1.05, where: hairline({ front: 0.36, temple: 0.30, side: 0.10, back: -0.42, top: 0.56 }) },       // bald on top
  face: { eyes: "lash", eye: "#2a1a12", iris: BROWN_EYES, lid: "#6a4636", brows: GREY_HAIR.tones[2], browUp: 3, jowl: 0.80, jaw: 0.92, chin: 0.54, nose: [1.2, 1.35, 1.1], noseShade: true, lip: "#8a4a3a", smile: -1, mouthW: 0.18 },
  top: { mat: UNDYED_PALE, sleeves: 0.46, stripe: { mat: PURPLE, at: [0], half: 0.17 } },
  stance: "carry",
  bottom: { kind: "skirt", mat: WOOL, len: 1.76, flare: 1.08, folds: [[-1.0, 0.3, 1.76, 0.1], [0.55, 0.5, 1.76, -0.1], [0.05, 0.9, 1.76, 0.05], [-0.45, 0.2, 1.3], [1.25, 0.3, 1.76], [2.5, 0.2], [-2.4, 0.4], [3.0, 0.6]] },
  shoes: { kind: "shoes", mat: RED_LEATHER, sole: shifted(RED_LEATHER, 2) },
  hold: { L: { hand: [-0.100, -0.210, 0.090], bend: [-0.6, -0.5, -0.6], curl: 0.9 } },       // his left arm carries the folds
  hand: "R",
  walk: { swing: 0.36, arm: 0.34, lean: 0.02, twist: 0.08 },
  pace: 185,
  gestures: [1, 11, 15, 14],                            // a point with the scroll, the scroll in the air, waving it all away, shaking it
  fidgets: { stand: ["toga"] },                         // he settles the folds of his toga over his arm
  extras(c) {
    const { limb, J, parts } = c;
    wear.toga(c, { mat: WOOL, edge: PURPLE });
    // the scroll in his right hand
    const up = upFromFist(J.R), g = J.R.palm;
    limb(along(g, up, -0.040), along(g, up, 0.070), 0.011, 0.011, PAPYRUS, { part: parts.HELD, squareStart: true, squareEnd: true });
    for (const k of [-0.046, 0.076]) limb(along(g, up, k), along(g, up, k + 0.006), 0.006, 0.006, WOOD, { part: parts.HELD });
  },
};

// ---------- the doorkeeper of the temple: burly, and unimpressed by everything since the day he was born ----------
export const doorkeeper = {
  name: "Doorkeeper", height: 1.05,
  dim: { ...ADULT, headR: [0.057, 0.064, 0.063], shoulderW: 0.112, trunkTop: [0.122, 0.078], trunkLow: [0.104, 0.076], pelvisR: [0.100, 0.064, 0.078], armR: [0.037, 0.031, 0.022], legR: [0.057, 0.037, 0.025], handR: 0.025, neckR: 1.25 },
  skin: SWARTHY,
  hair: { mat: DARK_HAIR, bulk: 1.03, where: hairline({ front: 0.64, temple: 0.54, side: 0.22, back: -0.34 }) },
  face: { eyes: "deep", eye: "#1c120c", iris: BROWN_EYES, brows: DARK_HAIR.tones[2], browW: 4, browTilt: 1, shadow: ramp("#c49878", "#ac7c5c", "#825a40", "#56382a"), shadowFrom: 0.45, jaw: 1.02, chin: 0.66, nose: [0.95, 1.0, 1.45], noseShade: true, lip: "#6a3828", mouthW: 0.24, ear: 1.1 },
  top: { mat: MOSS, sleeves: 0.42, cuff: 0.012, belt: HIDE, blouse: 0.006 },
  bottom: { kind: "skirt", mat: MOSS, len: 0.92, flare: 1.08, folds: [[-0.8, 0.2], [0.9, 0.25], [0.2, 0.5]] },
  shoes: { kind: "boots", mat: HIDE, sole: shifted(HIDE, 2), shaft: 0.22 },
  hold: { R: { hand: [0.238, -0.170, 0.100], bend: [0.25, -1, -0.45], grip: true } },
  stance: "hip",
  walk: { swing: 0.40, arm: 0.26, lean: 0.02, sway: 0.020 },
  pace: 140,
  gestures: [0, 15, 19, 10],                            // a nod (barely), waving someone off, a thumb at the doors behind him, pointing the way out
  fidgets: { stand: ["fold"] },                         // he folds his arms
  extras(c) {
    wear.cloak(c, { mat: MADDER, len: 0.40, pin: BRONZE });
    wear.staff(c, "R", { mat: WOOD, top: 1.02, r: 0.0105, knob: IRON });
  },
};

// ---------- the clerk of the treasury: thin, exact, and tired, with ink on his fingers ----------
const CLAVUS = ramp("#c08a80", "#9c5c54", "#723c38", "#4a2424");
const INK = ramp("#4a4660", "#2c2a3c", "#1a1826", "#0c0b14");
export const clerk = {
  name: "Clerk", height: 0.97, seated: "chair", shadow: 0.22, span: 1.15,
  dim: { ...ADULT, shoulderW: 0.088, trunkTop: [0.090, 0.060], trunkLow: [0.080, 0.060], pelvisR: [0.086, 0.058, 0.066], armR: [0.023, 0.020, 0.015], legR: [0.042, 0.028, 0.019], neckR: 0.80, handR: 0.020 },
  skin: SALLOW,
  hair: { mat: DARK_HAIR, bulk: 1.05, where: hairline({ front: 0.48, temple: 0.42, side: 0.12, back: -0.42 }) },       // combed straight forward, as the fashion is
  face: { eyes: "heavy", eye: "#2a1a12", iris: "#6a5a48", lid: "#7a5a48", brows: DARK_HAIR.tones[1], browTilt: -1, nose: [1.1, 1.0, 0.85], noseShade: true, jaw: 0.80, chin: 0.40, chinY: -0.88, lip: "#8a5a4a", mouthW: 0.16 },
  top: { mat: UNDYED, sleeves: 0.48, belt: shifted(HIDE, 1), stripe: { mat: CLAVUS, at: [0.48, -0.48, Math.PI - 0.48, Math.PI + 0.48], half: 0.07 } },      // two narrow stripes, shoulder to hem, as plain people's tunics have
  bottom: { kind: "skirt", mat: UNDYED, len: 1.0, flare: 1.06, stripe: { mat: CLAVUS, at: [0.48, -0.48, Math.PI - 0.48, Math.PI + 0.48], half: 0.07 } },
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  hold: { R: { hand: [0.050, -0.180, 0.225], bend: [1, -0.5, -0.4], grip: true } },        // his pen hand stays on the table
  rest: { L: { hand: [-0.070, -0.196, 0.200], bend: [-1, -0.5, -0.4], flat: true } },
  gestures: [16, 17, 1, 0],                             // a hand across his eyes, counting on his fingers, making a point, a nod
  sit: { lean: 0.12, drawn: true },
  stood: { hold: { R: { hand: [0.132, -0.326, 0.052], bend: [0.4, -1, -0.4], grip: true } }, rest: undefined },     // on his feet: the pen at his side
  fidgets: { sit: ["eyes"] },                           // he rubs his eyes
  extras(c) {
    const { limb, J, d, parts } = c;
    wear.stool(c, { mat: WOOD, r: 0.070 });
    const g = J.R.palm, up = upFromFist(J.R);
    limb(along(g, up, -0.030), along(g, up, 0.046), 0.0040, 0.0030, BRONZE, { part: parts.HELD });       // the pen
    limb(mix(J.R.palm, J.R.tip, 0.55), J.R.tip, d.handR * 0.62, d.handR * 0.56, INK, { part: parts.HELD });      // and the ink
  },
};

// ---------- the date seller: a Jew from Judea, about fifty, selling the dates of Jericho in a Roman street. ----------
// Courteous, dry, in no hurry. He stands easily with the weight on one leg and the basket on his hip, and his right hand
// does the talking. A plain long tunic of undyed wool; over it a mantle with dark bands woven near its ends.
const SUNNED = ramp("#f2caa2", "#dcaa7c", "#ac7a52", "#744c32");          // skin that has worked out of doors all its life
const OAT = ramp("#faf0da", "#eadec2", "#bcae90", "#877a60");             // wool as it comes off the sheep
const CAMEL = ramp("#e2c69e", "#c6a478", "#977852", "#665238");           // his mantle: brown wool
const BAND = ramp("#6c6074", "#463e50", "#2e2838", "#1b1722");            // the dark bands woven into it
const PEPPER = ramp("#66564c", "#44372e", "#2d231d", "#19120e");          // his hair: dark
const BEARD = ramp("#7c6e62", "#584a3f", "#3c312a", "#231b17");           // his beard: a shade lighter, as beards are
const SALT = ramp("#b6ada0", "#8f867a", "#686158", "#46403a");            // and both going grey
const WICKER = ramp("#ecd296", "#cca862", "#9a7838", "#685022");
const DATES = ramp("#c08850", "#9a6234", "#6c4020", "#442612");           // dates: brown,
const AMBER = ramp("#f6c868", "#e0a03c", "#ac7220", "#744a12");           // and the amber of the best ones
const LEAF = ramp("#aed078", "#80a84c", "#587a30", "#38501d");
const cell = (a, b) => { let h = (a * 374761393 + b * 668265263) | 0; h = (h ^ (h >>> 13)) * 1274126177; return (h ^ (h >>> 16)) >>> 0; };
export const dateseller = {
  name: "Date Seller", height: 0.98, span: 1.25,
  dim: { ...ADULT, headR: [0.056, 0.066, 0.063], shoulderW: 0.098, trunkTop: [0.104, 0.068], trunkLow: [0.098, 0.074], bellyFwd: 0.010, pelvisR: [0.096, 0.062, 0.074], armR: [0.029, 0.025, 0.018], neckR: 1.0 },
  skin: SUNNED,
  hair: { mat: PEPPER, bulk: 1.06, where: hairline({ front: 0.58, temple: 0.44, side: 0.10, back: -0.46, recede: 0.06 }),
          texture: (x, y, z) => (Math.abs(x) > 0.70 && y < 0.50 && z > -0.02 ? SALT : undefined) },           // grey at the temples
  face: { eyes: "plain", eye: "#2a1a12", iris: BROWN_EYES, noseShade: true, brows: PEPPER.tones[1], beard: BEARD, beardLen: 0.0, beardGrey: SALT, moustache: BEARD, mouthShows: true, lip: "#96564a", smile: 1, mouthW: 0.20, lines: 1, jaw: 0.90, chin: 0.52 },
  top: { mat: OAT, sleeves: 0.84, cuff: 0.012, belt: shifted(ROPE, 1) },
  bottom: { kind: "skirt", mat: OAT, len: 1.62, flare: 1.08, folds: [[-0.85, 0.3, 1.62, 0.08], [0.50, 0.5, 1.62, -0.08], [-0.15, 0.9, 1.62], [2.6, 0.3], [-2.5, 0.4]] },
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  stance: "easy",
  hold: { L: { hand: [-0.196, -0.232, 0.136], bend: [-1, -0.3, -0.75], grip: true } },      // his left arm round the basket on his hip
  hand: "R",
  walk: { swing: 0.36, arm: 0.26, lean: 0.03 },
  pace: 125,
  gestures: [8, 11, 5, 2],                              // an open hand (with a date on it), a finger raised, a hand to his chest, a small shrug
  fidgets: { stand: ["hitch"] },                        // he hitches his basket up on his hip
  extras(c) {
    const { ball, J, tw, pose, parts } = c;
    wear.mantle(c, { mat: CAMEL, band: BAND });
    // The basket on his left hip: wide and shallow, woven, heaped with dates. His hand has its far rim.
    const g = J.L.palm, axis = [J.hipC[0], g[1], J.hipC[2]], inward = norm([axis[0] - g[0], 0, axis[2] - g[2]]), R0 = 0.086;
    const at = [g[0] + inward[0] * R0 * 0.94, g[1] - 0.022, g[2] + inward[2] * R0 * 0.94];
    ball(add(at, [0, 0.022, 0]), [R0 * 0.90, 0.022, R0 * 0.90], DATES, {
      part: parts.HELD,                                 // the heap: brown, darker brown and amber, a date at a time
      fn: (ux, uy) => { const h = cell(Math.floor(ux * 5.5 + 40), Math.floor(uy * 3.0 + 40)) % 9; return h < 3 ? AMBER : h < 5 ? shifted(DATES, 1) : undefined; },
    });
    ball(at, [R0, 0.036, R0], WICKER, {
      part: parts.HELD,                                 // the bowl of it: the rim, then row under row of weaving
      fn: (ux, uy) => (uy < -0.12 ? null : uy < 0.12 ? undefined : Math.floor((uy + 1) * 5.0) % 2 ? shifted(WICKER, 1) : undefined),
    });
    // a few of the best, set out on a leaf on top
    const top = add(at, [inward[0] * 0.010, 0.043, inward[2] * 0.010]);
    ball(top, [0.030, 0.006, 0.018], LEAF, { part: parts.HELD }, tw);
    for (const dx of [-0.012, 0.004, 0.017]) ball(add(top, [dx, 0.007, 0.002]), [0.0085, 0.0065, 0.0085], dx === 0.004 ? DATES : AMBER, { part: parts.HELD });
    // and one held out on his hand: when that is the gesture, and when a script has him reach out or hold his hand out (hold())
    if (pose.gesture === 8 || (pose.reaching || 0) > 0.7) ball(add(mix(J.R.palm, J.R.tip, 0.35), [0, 0.012, 0]), [0.012, 0.0085, 0.012], shifted(DATES, 1), { part: parts.HELD });
  },
};

// =====================================================================================
// Nevada, the present
// =====================================================================================
const SKIN_WEATHERED = ramp("#f4cca6", "#e0a67c", "#b07850", "#774a32");

// ---------- the old-timer at the last stop in Nevada: straw hat, white beard, a lawn chair ----------
const SNOW = ramp("#ffffff", "#ecece6", "#c2c2ba", "#8e8e86");
const DENIM = ramp("#a9c3db", "#7797b6", "#53708e", "#364a61");
const CANVAS = ramp("#c9b48a", "#a48d63", "#7b6845", "#52452d");
const STRAW = ramp("#fff0b8", "#e9cf82", "#b99c52", "#7e6932");
const WEBBING = ramp("#8fe0b0", "#4fb07e", "#357c59", "#22513a");
const TUBE = ramp("#f6f8fa", "#c4cad1", "#8b929a", "#565c64");
const BRACES = ramp("#c9584a", "#a23c32", "#742a24", "#4a1a17");
export const oldtimer = {
  name: "Old-Timer", height: 0.97, seated: "chair", sit: { seat: 0.215, drawn: true }, shadow: 0.25, span: 1.2, seatShadow: 0.17,       // (a lawn chair is a low one)
  stood: { walk: { swing: 0.34, arm: 0.22, lean: 0.06 }, pace: 105 },
  fidgets: { stand: ["back"], sit: ["hat"] },           // standing, a hand to the small of his back; sitting, a touch to his hat
  dim: { ...ADULT, trunkTop: [0.110, 0.076], trunkLow: [0.110, 0.094], bellyFwd: 0.014 },
  skin: SKIN_WEATHERED,
  hair: { mat: SNOW, where: hairline({ front: 1.3, temple: 1.1, side: 0.20, back: -0.50 }) },
  face: { beard: SNOW, brows: SNOW.tones[2], eye: "#2a1a12", iris: "#7f9fbf", noseShade: true },      // (eyes of a faded blue)
  top: { mat: DENIM, sleeves: 2, stripe: { mat: BRACES, at: [0.50, -0.50, Math.PI - 0.42, Math.PI + 0.42], half: 0.085 } },      // suspenders over the work shirt, front and back
  bottom: { kind: "trousers", mat: CANVAS },
  shoes: { kind: "boots", mat: ramp("#9a6b45", "#70482a", "#4d301a", "#2f1d10"), sole: ramp("#4d301a", "#372212", "#24160c", "#150d07") },
  extras({ ball, limb, hp, d, hy, J, parts, widthAt, depthAt, pose, th, S }) {
    const hip = J.hipC, seat = J.seatY - 0.006;
    // a straw hat: a wide brim and a low crown
    ball(hp(0, 0.62, 0.06), [0.118, 0.012, 0.118], STRAW, { part: parts.HAT }, hy);
    ball(hp(0, 0.86, 0), [d.headR[0] * 0.98, d.headR[1] * 0.42, d.headR[2] * 0.98], shifted(STRAW, 1), { part: parts.HAT }, hy);
    if (!pose.seated || pose.noSeat) return;            // (when he gets up it stays where it is: see drawSeat in rig.js)
    // the lawn chair: webbing for the seat and the back, on a frame of bent tube
    const at = (x, y, z) => [hip[0] + x, y, hip[2] + z];
    ball(at(0, seat, 0.075), [0.120, 0.012, 0.140], WEBBING, { part: parts.EXTRA3 });
    const slab = [0.116, 0.010], sw = widthAt(slab, 0);            // the back: a flat panel of straps, square at the top and the bottom
    limb(at(0, seat + 0.040, -0.070), at(0, seat + 0.362, -0.119), sw, sw, WEBBING, { part: parts.EXTRA3, depth: depthAt(slab, 0) / sw, bias: Math.cos(th) < -0.2 ? S * 0.045 : 0, squareStart: true, squareEnd: true, fn: (t) => (Math.floor(t * 7) % 2 ? shifted(WEBBING, 1) : undefined) });
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
  hair: { mat: ramp("#5a5560", "#3a3640", "#25222a", "#151318"), where: hairline({ front: 0.62, temple: 0.50, side: 0.26, back: -0.42 }) },
  face: { shades: "#15161c" },
  top: { mat: SUIT, sleeves: 2, hem: true, open: true, under: WHITE, collar: shifted(SUIT, 1) },
  bottom: { kind: "trousers", mat: shifted(SUIT, 1) },
  shoes: { kind: "shoes", mat: ramp("#4a4650", "#2c2a31", "#1b1a1f", "#0e0d10"), sole: ramp("#2c2a31", "#1b1a1f", "#0e0d10", "#070608") },
  stance: "behind",
  walk: { swing: 0.42, arm: 0.26, lean: 0.03 },
  gestures: [0, 8, 0, 10],                              // mostly nothing; an open hand; a pointing finger
  fidgets: { stand: ["watch", "tie"] },                 // he looks at his watch; he straightens his tie
  extras({ limb, ball, d, J, pose, parts }) {
    const front = d.trunkTop[1];
    if (pose.fidget === "watch" && pose.fu > 0.18 && pose.fu < 0.82) {        // his watch, out from under the cuff
      const at = mix(J.L.wrist, J.L.elbow, 0.10);
      ball(at, [0.0115, 0.0115, 0.0115], ramp("#e8ecf0", "#b8c0c8", "#7c848e", "#4c525a"), { part: parts.HELD });
    }
    limb(add(J.sh, J.torso([0, 0.004, front * 0.50])), add(J.sh, J.torso([0, -0.112, front * 1.00])), 0.008, 0.012, TIE, { part: parts.EXTRA, bias: 4 });
  },
};


export const people = {
  dad, son, mom, bigsis, lilsis,
  scribe, carrier, overseer, hauler1, hauler2, hauler3, guard, lampboy, goldsmith,
  keeper, washer, urchin, soothsayer, senator, doorkeeper, clerk, dateseller,
  oldtimer, agent,
  lot,
  // the same people at another moment of the story (a scene puts one in the other's place):
  "guard-shade": guardShade, "goldsmith-shades": goldsmithShades, "lot-standing": lotStanding,
};
