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
//   (NEVADA-12P, round twelve:)
//   crown      how far a hat or a hairdo rises over the head, in heights, so that words are put over it (tallOf in rig.js)
//   hatAt, pencilAt   for the `hat` and `pencil` movements: how high the brim, or the pencil, is, in half-heights of the head
//   banjoPot   for `strum`: where the banjo's head is, in the space of the shoulders (as hands are placed)
//   sit.seat "floor": sat on the ground with the legs out in front, leaning back on both hands
//   pray.fold  someone sitting folds the hands together, as standing, instead of lifting them open
//   hold.loose a prayer may take this hand (the thing held then hangs from the folded hands: Grandpa Joe's banjo)
//   face.shadesTilt   dark glasses knocked crooked: the left lens a pixel lower (1) or higher (-1)
//   top.check  a check woven down long sleeves too: { mat, every, band, stripe } (with top.stripe and top.bands: a plaid)
//   (ROME-13P, round thirteen:)
//   holds      their own holds, kept through whatever is said: { name(o) { return a pose } } (figure.hold(true, "bless"))
//   sit.clutch the hand that holds what they carry to their chest as they hop down from a seat higher than their knees
//   stance "prayer"   their way of standing is their own prayer (`pray`): Eleazar at his window
//   top.bare   "R" or "L": a tunic fastened on one shoulder only, that shoulder bare (Felix's)
//   and, in rig.js, wear.toga's `scant` and `hang` (a toga too small, or very large) and wear.mantle's `tassels` and `thread`
//   Their own small movements are added to the rig's with addMoves (after the Rome people, below).
//   (OFFICE-17P, round seventeen:)
//   standOn    standing on something this high (a chair's seat, given as a seat's height is): drawn that much above their
//              place, which is the ground under it; their shadow is on it, under their feet
//   nod        how someone on their feet holds their head, added to every standing pose's own (less than 0: looking up)
//   restMouth  a mouth a little open when nothing else says how it is (a man asleep)
//   cues       the small movements a script plays on them, besides those of their life: { sit: [...], stand: [...] }
//              (the sprites page shows them; any movement the rig knows can be played on anyone)
//   sit.up     how far in front of the seat they stand once up, in their heights (0: at a table, they push the chair back)
//   sit.turn   the head turned on its own, sitting (Floyd's, lolled against the couch)
//   hold[k].stroke, .strokes   a held hand that goes there and back in time as they walk or talk (strumming)
//   and, in rig.js, the gestures 22 (a stamp brought down onto the other palm) and 23 (a look over the glasses)
//
// The family comes from the present, so their colors never change with the era.
// Each of them owns one color nobody else in the family wears.
//
// docs/CHARACTERS.md says who these people are. To change someone, change the numbers
// and colors here; every view and every animation follows. tools/sprites.html shows the result.

import { ADULT, CHILD, WOMAN, blend, ramp, pack, shifted, add, sub, mul, mix, turn, unit, wear, upOf } from "./rig.js";      // (pack, sub, mul, unit: NEVADA-12P)
import { poses, addMoves, moveKit, lerp } from "./rig.js";              // ROME-13P: the bigger Rome's people, and their own small movements

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

// ---------- Dad: vacation shirt, shorts, socks and sandals; his hair slicked back to the side, green eyes, a five o'clock shadow ----------
const DAD_HAIR = ramp("#a87a4c", "#70482a", "#4d301a", "#2f1d10", { shine: true });      // (combed back with something in it: it catches the light)
const STUBBLE = ramp("#e8c3a2", "#d6a583", "#b2785a", "#7c4a37");          // a five o'clock shadow: the skin a shade darker, low on the face
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
          short: { mat: STUBBLE, stubble: STUBBLE, dense: true, from: 0, belowNose: 0.18, lip: 0.55, chin: 1.1, side: 1.1, under: 1.1 }, lip: "#b06a58", noseShade: true,      // a five o'clock shadow from under the nose down over the jaw and chin, the upper lip clean: no beard, no moustache
          jaw: 0.92, chin: 0.62, chinY: -0.56, chinZ: 0.44, mouthY: -0.68, nose: 1.1, eyeX: 0.43, ear: 1.2, earOut: 1.03, big: { eyeW: 0.46, eyeH: 0.44 } },
  top: { mat: ramp("#ffe582", "#f4c043", "#cf9226", "#8f5d18"), sleeves: 0.62, hem: true, open: true, collar: true, pattern: FLOWERS },
  bottom: { kind: "shorts", mat: ramp("#a9b381", "#7f8d5c", "#59663f", "#39442b"), len: 0.72 },
  socks: { mat: WHITE, from: 0.52, stripes: [ramp("#f08a70", "#d2452f", "#a12f22", "#6e1f19"), ramp("#7fb2e6", "#3f79c2", "#2b5590", "#1b3760")] },
  shoes: { kind: "sandals", mat: ramp("#a8744a", "#7d5030", "#553521", "#332015"), sole: ramp("#6b4a30", "#4d3320", "#332015", "#1f130c") },
  gestures: [0, 1, 0, 3],                               // a nod; a small point; a nod; a hand on the hip (round twelve: half his lines are said with a nod alone)
  pray: { high: -0.40, bow: 0.34 },                     // his big hands folded low in front of him, his head well down
};

// ---------- the Son: blonde hair that sticks up, blue eyes, blue hoodie, backpack. Zany: he bounces, and his hands never stop. ----------
const SON_HAIR = ramp("#fbe7a0", "#e9c867", "#bf9640", "#83611f");          // blonde
const RED = ramp("#ff7a62", "#de4a33", "#a93224", "#72201a");          // the stripe on his sneakers
const PACK = ramp("#b39bf5", "#8463d8", "#5f44a8", "#3d2b72");
const HOODIE = ramp("#93dcf2", "#4fc0e2", "#2e90b6", "#1f6483");
export const son = {
  name: "Son", height: 0.74,
  dim: CHILD,
  skin: SKIN,
  hair: { mat: SON_HAIR, bulk: [1.08, 1.06, 1.08], where: hairline({ front: 0.44, temple: 0.32, side: 0.08, back: -0.44, brow: 0.50, temples: 1.15 }),      // a blonde mop, never combed: it sticks up in tufts all over the top
          puffs: [[0.00, 0.98, 0.34, 0.17, 0.34, 0.16], [-0.44, 0.92, 0.24, 0.15, 0.30, 0.15], [0.46, 0.90, 0.18, 0.15, 0.30, 0.15], [-0.20, 0.96, -0.26, 0.15, 0.32, 0.15],
                  [0.26, 0.94, -0.30, 0.15, 0.30, 0.15], [-0.68, 0.70, -0.06, 0.14, 0.26, 0.14], [0.70, 0.68, 0.02, 0.14, 0.26, 0.14], [0.02, 0.78, -0.72, 0.16, 0.30, 0.16]] },
  face: { eyes: { at: 0, full: ["#h", "ii"], thin: ["#", "i"] }, iris: "#4a8ad0", eye: "#1c3358", brows: SON_HAIR.tones[2], brow: { full: [0, -1, -1] }, blush: "#f3a68c",
          lip: "#a5523f", eyeX: 0.43, eyeY: -0.06, mouthY: -0.64, ear: 1.15, earOut: 1.03, jaw: 0.84, chin: 0.56, chinY: -0.54, chinZ: 0.44, nose: [0.65, 0.65, 0.75], smile: 1, mouthW: 0.26,
          big: { eyeW: 0.48, eyeH: 0.52, arch: 0.30, browUp: 0.70 } },
  top: { mat: HOODIE, sleeves: 2, hem: true },
  bottom: { kind: "shorts", mat: ramp("#5a668f", "#3c4563", "#293049", "#1a1f31"), len: 0.80 },
  socks: { mat: WHITE, from: 0.72 },
  shoes: { kind: "sneakers", mat: ramp("#ffffff", "#f1efe6", "#c4c0b2", "#8f8b80"), stripe: RED, sole: ramp("#d9d5c8", "#b5b1a4", "#8a867c", "#5f5c55") },
  stance: "straps",                                     // thumbs hooked in the straps of his pack
  walk: { swing: 0.50, arm: 0.58, elbow: 0.95, pump: 0.30, lean: 0.10, lift: 1.3, bob: 0.05, wag: 0.10, sway: 0.020 },   // a bounce, fists pumping, head going from side to side
  gestures: [0, 1, 0, 9],                               // a nod (thumbs in his straps); a small point; a nod; his hands turning in front of him (round twelve: no shrug, nothing over his head)
  pray: { high: 0.30, bow: 0.34 },                      // hands folded at his middle and his head down, for once standing still (his hair stays up)
  extras({ ball, limb, wide, deep, d, tw, J, parts }) {
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
  hair: { mat: MOM_HAIR, bulk: [1.14, 1.02, 1.12], lift: [0, -0.002, 0], where: hairline({ front: 0.52, temple: 0.28, side: -0.40, back: -1.0, sweep: 0.22, brow: 0.45, temples: 1.10 }), ears: false,      // (close to the head on top, full at the sides: no dome)
          texture: (x, y, z) => curl(x, y, z, 7) ? MOM_CURL : undefined },     // curls all over, falling past her shoulders (and see `extras`)
  face: { eyes: { at: 1, full: ["==.", "#i="], thin: ["=.", "#="] }, iris: "#8a5a2c", eye: "#2e1b0e", lid: "#2c1a10", brows: MOM_HAIR.tones[2], brow: { full: [0, -1, -1, 0] }, browW: 4, blush: "#f0a08a",
          lip: "#b8475c", lips: "#d4707e", eyeX: 0.43, nose: [0.65, 0.65, 0.75], noseShade: true, jaw: 0.80, chin: 0.52, chinY: -0.58, chinZ: 0.44, mouthY: -0.68, mouthW: 0.20, smile: 1,
          big: { eyeW: 0.46, eyeH: 0.46, lashes: 1, arch: 0.28 } },
  top: { mat: EMERALD, sleeves: 0.42, belt: shifted(EMERALD, 2), open: 0.034 },
  bottom: { kind: "skirt", mat: EMERALD, len: 1.05, flare: 1.20, folds: [[-0.55, 0.15], [0.60, 0.3], [0.15, 0.55]] },
  shoes: { kind: "pumps", mat: ramp("#fffaf0", "#efe2c8", "#c3b596", "#8e8168"), sole: ramp("#c9b99a", "#a39375", "#7a6d55", "#52483a") },
  stance: "clasped",
  walk: { swing: 0.40, arm: 0.20, lean: 0.02, twist: 0.09, sway: 0.016 },     // short steps, quiet arms, a little sway
  gestures: [0, 5, 8, 0],                               // a nod, a hand to the heart, an open hand
  pray: { high: 0.42, bow: 0.28 },                      // her hands folded at her breast
  pace: 150,
  // LETTER-17: she kneels (figure.kneel() in a script: the rig's kneelPose): at the little door in Act Four, the night she
  // hears her son, and nowhere else. Leaning in a little, upright; and sat back on her heels when she understands.
  kneel: { lean: 0.10, backLean: 0.02 },
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
    // LETTER-17: unless she has set it down (figure.bare = "bag": the roadside draws it on the gravel, js/art/props.js `handbag`)
    if (pose.bare === "bag") return;
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
  gestures: [0, 6, 0, 8],                               // a nod (holding her elbow); a hand to her chin; a nod; an open hand, low (round twelve: no finger in the air, no pointing: it read as a smart aleck)
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

// ---------- Little Sister, 7: pink overalls, yellow boots, short wild blonde hair to just past her shoulders. Small but mighty: fists on hips, and she stomps. ----------
const LIL_HAIR = ramp("#e8bb78", "#c08d4c", "#8d6230", "#5c3d1b");
const LIL_STRAND = shifted(LIL_HAIR, 1);
const PINK = ramp("#ff9db4", "#f0607f", "#bd3f5e", "#802a41");
const SUN = ramp("#fff0a0", "#ffd23f", "#d59a1f", "#93640f");
const SMALL = { ...CHILD, headR: [0.078, 0.088, 0.084], neckY: 0.790, shoulderY: 0.760, waistY: 0.565, hipY: 0.462, thigh: 0.214, shin: 0.204, legR: [0.050, 0.036, 0.026], armR: [0.029, 0.025, 0.019], neckR: 0.92 };
export const lilsis = {
  name: "Little Sister", height: 0.67,
  dim: SMALL,
  skin: SKIN,
  hair: { mat: LIL_HAIR, bulk: [1.14, 1.08, 1.12], where: hairline({ front: 0.26, temple: 0.14, side: -0.70, back: -1.1, brow: 0.55, temples: 1.15 }), ears: true,          // a soft fringe (less forehead), and a wild mop round the rest of her head, over the ears
          texture: (x, y, z) => (y < 0.5 && Math.sin(x * 11 + z * 7 + y * 5) > 0.84 ? LIL_STRAND : undefined),                    // strands going their own way
          puffs: [[-0.98, 0.14, -0.20, 0.22, 0.18, 0.20], [1.00, 0.06, -0.14, 0.20, 0.18, 0.20], [-0.92, -0.46, -0.30, 0.24, 0.16, 0.20], [0.96, -0.54, -0.26, 0.24, 0.16, 0.20],
                  [-0.30, 1.00, -0.20, 0.16, 0.20, 0.16], [0.42, 0.98, 0.10, 0.14, 0.20, 0.14], [0.06, 0.94, -0.60, 0.18, 0.22, 0.18], [-0.60, 0.80, 0.40, 0.14, 0.18, 0.14]] },
  face: { eyes: { at: 0, full: ["#h=", "ii"], thin: ["#", "i"] }, iris: "#6a9ee0", eye: "#2c4f8a", lid: "#5a3a20", brows: LIL_HAIR.tones[2], brow: { full: [0, 0] }, browW: 2, blush: "#f59a8e",
          freckles: true, freckle: "#e0a07c", lip: "#c2605a", eyeX: 0.43, eyeY: -0.10, mouthY: -0.62, ear: 1.15, earOut: 1.03, jaw: 0.86, chin: 0.58, chinY: -0.49, chinZ: 0.44, nose: [0.55, 0.6, 0.7], smile: 1, mouthW: 0.22,
          big: { eyeW: 0.44, eyeH: 0.56, lashes: 1, arch: 0.30, browUp: 0.75 } },      // (her portrait: eyes no bigger than anyone's, a lash, brows up)
  top: { mat: WHITE, sleeves: 0.5 },
  bottom: { kind: "shorts", mat: PINK, len: 0.62, rise: 0.085, bib: { top: 0.078, half: 0.60, strap: 0.26 } },     // overalls: a high waist, a bib and two straps
  shoes: { kind: "boots", mat: SUN, sole: shifted(SUN, 2), shaft: 0.52 },     // rain boots
  stance: "akimbo",
  walk: { swing: 0.50, arm: 0.72, elbow: 0.12, lean: 0.09, lift: 1.25, bob: 0.03 },     // a stomp: straight arms, like a small soldier
  gestures: [0, 4, 0, 10],                              // a nod (fists on her hips); both hands up, "ta-da"; a nod; pointing ahead (round twelve: her muscles are for the walk and the talk of it, not every line)
  pray: { high: 0.97, bow: 0.15, tight: true },         // with all her might: hands clasped tight under her chin, eyes squeezed shut
  pace: 145,
  extras({ sf, P, ball, limb, hp, wide, deep, d, hy, th, J, S, fine, parts }) {
    // her hair: a wild mop that falls to just past her shoulders, down her back and in a lock in front of each shoulder, the ends flicking out
    const fall = [0.062, 0.026], foot = [0.070, 0.024], r0 = wide(fall), r1 = wide(foot);
    limb(hp(0, -0.10, -0.66), add(J.spine(d.shoulderY - 0.062), J.torso([0, 0, -(d.trunkTop[1] + 0.014)])), r0, r1, LIL_HAIR, { part: parts.HAIR, depth: deep(fall) / r0, bias: S * 0.012, fn: (t, a) => (Math.sin(a * 7 + t * 9) > 0.86 ? LIL_STRAND : undefined) });
    for (const sd of [1, -1]) {
      const from = hp(sd * 0.92, -0.26, 0.00), to = add(J.sh, J.torso([sd * 0.066, -0.040, 0.014]));
      limb(from, to, 0.020, 0.016, LIL_HAIR, { part: parts.HAIR });
      ball(add(to, J.torso([sd * 0.012, -0.010, 0.004])), [0.022, 0.014, 0.018], LIL_HAIR, { part: parts.HAIR }, hy);      // the ends, flicking out
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

// ---------- the masons on the cradles: two men far up the faces, on planks slung on ropes, polishing the casing ----------
// (Round twelve: the planks had a water jar painted on each, which read as a man sitting still; now a man stands on
// each, facing the stone, and rubs it smooth now and then. Drawn small: `scale` in egypt-site.js.)
const masonBase = {
  name: "Mason", height: 1.0, stance: "hip", hold: undefined, extras: undefined, walk: { swing: 0.44, arm: 0.36, lean: 0.05 },
  fidgets: { only: true, stand: ["polish"] },           // the rubbing stone goes back and forth over the casing
  gestures: [0, 8, 0, 1],
};
export const mason1 = { ...hauler1, ...masonBase, skin: TAN, hair: { mat: shaved(TAN), bulk: 1, where: cropped } };
export const mason2 = { ...hauler3, ...masonBase, skin: DARK };

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
    wear.toga(c, { mat: WOOL });                        // ROME-13P (decision 12): plain white, as a senator's was; the broad stripe of his rank is on his tunic
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
    const lo = loosened(pose);                                          // OFFICE-17P: the knot pulled down a finger's width (`loosen`), then put back
    limb(add(J.sh, J.torso([0, 0.004 - 0.016 * lo, front * (0.50 + 0.10 * lo)])), add(J.sh, J.torso([0, -0.112, front * 1.00])), 0.008, 0.012, TIE, { part: parts.EXTRA, bias: 4 });
    if (lo > 0.4) limb(add(J.sh, J.torso([0, 0.006, front * 0.52])), add(J.sh, J.torso([0, -0.006, front * 0.60])), 0.0065, 0.0045, WHITE, { part: parts.EXTRA, bias: 4.4 });     // (OFFICE-17P: the collar open above it)
  },
};

// =====================================================================================
// NEVADA-12P (round twelve): Grandpa Joe, Grandma Jolene and her hats, the backup, and Jed's collar
// =====================================================================================
// Who they are: briefs/out/nevada-expansion-design.md ("Characters"). All of them people of our own: nobody's likeness,
// no film's costume, no brand.

/** One centimetre in the rig's measure, for seats: a grown person 1.0 high is 1.75 m (the stage's own scale: a stretch
    limousine 6.3 m long is 575 pixels where a grown man is 160). A seat is as high for whoever sits on it. */
const CM = 1 / 175;
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const smooth01 = (k) => { const t = Math.max(0, Math.min(1, k)); return t * t * (3 - 2 * t); };
/** One pixel of ink at a point on (or just over) the figure, where something is drawn and nothing nearer stands in front of
    it: a chain on a neck, a flower on a blouse. (A pixel stamped with no depth would show through from the far side.) */
function inkAt(cx, p, ink, tol = 0.012) {
  const { P, sf, S } = cx, q = P(p), x = Math.round(q[0] - 0.5), y = Math.round(q[1] - 0.5);
  if (x < 0 || y < 0 || x >= sf.w || y >= sf.h || q[2] < sf.z[y * sf.w + x] - tol * S) return;
  sf.dot(x, y, ink, null);
}
/** A thread through the points given (a loose string, hanging in the air or over a coat): a line one pixel wide, drawn as a
    shape so that whatever is in front of it hides it. (Its part throws no shadow: a string is too thin to.) */
const STRING = ramp("#f8f4ea", "#eee8da", "#dcd6c6", "#c4beae");
function thread(cx, pts, mat = STRING) {
  const o = { part: cx.parts.FOOT.R, fn: (t, nx, ny) => (nx * nx + ny * ny > 0.36 ? null : undefined) };
  for (let i = 0; i + 1 < pts.length; i++) cx.limb(pts[i], pts[i + 1], 0.0001, 0.0001, mat, o);
}

// ---------- Grandpa Joe: came west in 1974 and never got round to leaving; forty years on this porch ----------
// Bib overalls over a red plaid shirt, a straw hat with a dent in the crown where the coin came down on it, a full white
// beard, white hair, boots; faded blue eyes. Slow, and the kinder he is the slower he goes. He is found sitting in his
// rocking chair (drawn with him: it stays where it is when he gets up) with the banjo across his knees; on his feet he
// carries it in his right hand by the neck, the head down, and hooks his other thumb in the strap of his overalls.
const JOE_PLAID = ramp("#ff8c74", "#dc4632", "#a32e22", "#6a1c16");      // his shirt: red,
const JOE_CHECK = ramp("#a83c30", "#6c2420", "#4a1714", "#2e0e0c");      // checked with dark red: coarse, so that it reads small
const OVERALLS = ramp("#a6c2ea", "#6a8fc4", "#4b6a98", "#30476a");       // denim, washed a few hundred times
const BRASS = ramp("#fff3b8", "#e6c46c", "#ad8d3c", "#725a22", { shine: true });
const HATBAND = ramp("#97603e", "#6a3f26", "#4a2b19", "#2c190e");
const DENT = ramp("#c9a95c", "#9c7e3c", "#76602c", "#4e3f1c");           // the shadow in the dent
const ROCKER = ramp("#eab474", "#c4863f", "#8f5c29", "#5e3a17");         // the rocking chair: honey-colored wood
const CUSHION = ramp("#f8de8e", "#e0b44c", "#aa842e", "#72581b");        // a cushion Jolene made: mustard calico
const BANJO_HEAD = ramp("#ffffff", "#f5f2e8", "#d4cebd", "#9c9684");
const CHROME = ramp("#ffffff", "#d0d5de", "#9097a3", "#565c67", { shine: true });
const NECK_WOOD = ramp("#b47e4e", "#805232", "#5a3720", "#382214");
const SPLINTER = ramp("#f4dcb0", "#dcb880", "#a8864e", "#705830");
const INK_STRING_HEAD = pack("#aaa79d"), INK_STRING_NECK = pack("#f0e6d0"), INK_PEG = pack("#fffaf0"), INK_GLINT = pack("#ffffff"), INK_BRIDGE = pack("#4a2c18");

/** The height of his rocking chair's seat, and of the limousine's long seat (PAINT-12C confirms the painted seat: set
    LIMO_SEAT from S/work-paintC/ready.md). In the rig's measure: see CM. */
export const ROCKER_SEAT = 42 * CM;
export const LIMO_SEAT = 42 * CM;

/** A ring (a banjo's rim, a hoop) as short tubes round a circle: `c` the middle, `a` and `b` two unit vectors across it. */
function ring(cx, c, a, b, r, tube, mat, o, n = 20, from = 0, to = 2 * Math.PI) {
  const at = (t) => add(c, add(mul(a, Math.cos(t) * r), mul(b, Math.sin(t) * r)));
  for (let i = 0; i < n; i++) cx.limb(at(from + ((to - from) * i) / n), at(from + ((to - from) * (i + 1)) / n), tube, tube, mat, o);
  return at;
}

/**
 * Grandpa Joe's banjo: a round pot (a white head in a chrome rim, the back of it chrome, which catches the sun), a long
 * dark neck with its headstock and pegs, and the strings as a line of light. `b`: { c: the middle of the pot, u: up the
 * neck, n: the way the head faces }, in the figure's own space. All of it is HELD.
 */
function banjo(cx, b, state = "whole") {
  const { limb, sf, P, parts, S, th, seatOnly } = cx;
  if (seatOnly) return;
  // (OFFICE-17P: `state`, what is left of it: "whole"; "broken", its head broken through, the rim, the neck and the strings,
  //  slack, as Jed's head left it; "pie", mended with a pie tin, a bright tin head with a crimped rim. And b.k, its size
  //  against the one who holds it, as their heights go: Opal is smaller than Grandpa Joe, and the banjo is not.)
  const K = b.k || 1, R = 0.085 * K, u = unit(b.u), n0 = unit(b.n), n = unit(sub(n0, mul(u, dot3(n0, u)))), w = cross(u, n), c = b.c, held = { part: parts.HELD };
  const facing = dot3(n, [Math.sin(th), 0.22, Math.cos(th)]) > 0;
  // the rim, round the middle of the pot's depth
  const mid = along(c, n, -0.010 * K), rimAt = ring(cx, mid, w, u, R, 0.0125 * K, CHROME, held, 22);
  // the head (or, from behind, the back), flat, at the face it is on
  const face = along(c, n, (facing ? 0.004 : -0.024) * K), pts = [];
  for (let i = 0; i < 22; i++) { const t = (2 * Math.PI * i) / 22; pts.push(P(add(face, add(mul(w, Math.cos(t) * R * 0.93), mul(u, Math.sin(t) * R * 0.93))))); }
  const ctr = P(face), rpx = R * S;
  const lit = (x, y) => (x + 0.5 - ctr[0]) * 0.60 + (y + 0.5 - ctr[1]) * 0.80;          // (how far toward the shade side a pixel is: the light is from the upper left)
  const fn = !facing ? (x, y) => (lit(x, y) > rpx * 0.30 ? 2 : (x + 0.5 - ctr[0]) ** 2 + (y + 0.5 - ctr[1]) ** 2 < (rpx * 0.45) ** 2 ? 2 : undefined)
    : state === "broken" ? brokenHead(ctr, rpx, lit)
    : state === "pie" ? tinHead(ctr, rpx, lit)
    : (x, y) => (lit(x, y) > rpx * 0.52 ? 2 : undefined);
  sf.poly(pts.map((q) => [q[0], q[1]]), ctr[2], !facing ? CHROME : state === "broken" ? POT_INSIDE : state === "pie" ? TIN : BANJO_HEAD, 1, { part: parts.HELD, fn });
  // the neck and the headstock, angled back a little, and its pegs
  const neck0 = along(c, u, R * 0.90), neck1 = along(c, u, R + 0.370 * K), hs = add(along(neck1, u, 0.052 * K), mul(n, -0.012 * K));
  limb(neck0, neck1, 0.0105 * K, 0.0085 * K, NECK_WOOD, held);
  limb(neck1, hs, 0.0135 * K, 0.0125 * K, NECK_WOOD, { ...held, squareEnd: true });
  const dotAt = (p, ink) => { const q = P(p); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), ink, parts.HELD); };
  if (S >= 84) for (const k of [0.014, 0.036]) for (const sd of [1, -1]) dotAt(add(along(neck1, u, k * K), mul(w, sd * 0.018 * K)), INK_PEG);
  if (S >= 84) dotAt(add(along(c, u, R + 0.11 * K), mul(w, 0.012 * K)), INK_PEG);                // the fifth string's peg, part way up the neck
  if (facing && state === "broken") {
    // (OFFICE-17P) no head, so no bridge: the strings hang slack from the tailpiece across the hole and up the neck,
    // sagging away from it, each its own way
    const from = along(along(c, u, -R * 0.78), n, 0.008 * K), to = along(along(neck1, u, -0.004 * K), n, 0.010 * K);
    for (const [side, sag, out] of [[-0.012, -0.010, 0.006], [0.0, 0.006, 0.010], [0.012, 0.014, 0.004]]) {
      const pts = [];
      for (let i = 0; i <= 10; i++) { const t = i / 10, s = Math.sin(Math.PI * Math.min(1, t * 1.6)) * (t < 0.62 ? 1 : 0.7); pts.push(add(mix(add(from, mul(w, side * K)), add(to, mul(w, side * 0.4 * K)), t), add(mul(w, sag * s * K), add(mul(n, out * s * K), [0, -0.012 * s * K, 0])))); }
      thread(cx, pts, SLACK_STRING);
    }
    limb(along(c, u, -R * 0.98), add(along(c, u, -R * 0.66), mul(n, 0.010 * K)), 0.006 * K, 0.005 * K, CHROME, held);       // the tailpiece
  } else if (facing) {
    // the strings: a line of light from the tailpiece over the head and up the neck; a bridge across them
    const from = P(along(along(c, u, -R * 0.78), n, 0.008 * K)), to = P(along(along(neck1, u, -0.004 * K), n, 0.010 * K)), j = P(along(c, u, R * 0.95));
    const steps = Math.ceil(Math.hypot(to[0] - from[0], to[1] - from[1]));
    for (let i = 0; i <= steps; i++) {
      const t = i / Math.max(1, steps), x = from[0] + (to[0] - from[0]) * t, y = from[1] + (to[1] - from[1]) * t;
      const onHead = (x - from[0]) * (j[0] - from[0]) + (y - from[1]) * (j[1] - from[1]) < (j[0] - from[0]) ** 2 + (j[1] - from[1]) ** 2;
      sf.dot(Math.round(x - 0.5), Math.round(y - 0.5), onHead ? (state === "pie" ? INK_STRING_TIN : INK_STRING_HEAD) : INK_STRING_NECK, parts.HELD);      // (OFFICE-17P: darker over the bright tin, so they show)
    }
    if (S >= 84) for (const k of [-0.016, 0, 0.016]) dotAt(add(along(along(c, u, -R * 0.32), n, 0.008 * K), mul(w, k * K)), INK_BRIDGE);
    limb(along(c, u, -R * 0.98), add(along(c, u, -R * 0.66), mul(n, 0.010 * K)), 0.006 * K, 0.005 * K, CHROME, held);       // the tailpiece
  }
  // the chrome catching the sun: a glint on the rim, on its side toward the light
  let best = null;
  for (let i = 0; i < 22; i++) { const q = P(rimAt((2 * Math.PI * i) / 22)); if (!best || q[0] + q[1] * 1.3 < best[0] + best[1] * 1.3) best = q; }
  if (best) { sf.dot(Math.round(best[0] + 0.5), Math.round(best[1] + 0.5), INK_GLINT, parts.HELD); if (S >= 120) sf.dot(Math.round(best[0] + 1.5), Math.round(best[1] + 0.5), INK_GLINT, parts.HELD); }
}

/** What is left of the banjo once it has come down on Jed: the neck and the headstock, the broken end splintered, a few
    strings trailing from it. `top` is the headstock end, `dir` the way the neck runs from it. */
function brokenBanjo(cx, top, dir) {
  const { limb, sf, P, parts, S, seatOnly } = cx;
  if (seatOnly) return;
  const d = unit(dir), side = unit(cross(d, [0, 1, 0.0001])), held = { part: parts.HELD }, end = along(top, d, 0.300);
  limb(top, along(top, d, -0.052), 0.0135, 0.0125, NECK_WOOD, { ...held, squareEnd: true });     // the headstock
  limb(top, end, 0.0090, 0.0105, NECK_WOOD, held);
  // the break: splinters of pale wood
  for (const [k, s2, len] of [[0, 0.010, 0.030], [0.6, -0.012, 0.022], [-0.5, 0.004, 0.040]]) limb(along(end, side, s2 * 0.6), add(along(end, d, len), mul(side, s2 + k * 0.006)), 0.0040, 0.0016, SPLINTER, held);
  // the strings, trailing loose from the end and curling
  for (const [s2, len, wob] of [[-0.006, 0.150, 0.9], [0.002, 0.110, 1.3], [0.008, 0.170, 0.7]]) {
    const pts = [];
    for (let i = 0; i <= 8; i++) { const t = i / 8; pts.push(add(along(along(end, side, s2 + 0.012 * Math.sin(t * 7 * wob)), d, 0.010 * t), [0, -len * t, 0.020 * Math.sin(t * 5 * wob)])); }
    thread(cx, pts);
  }
  if (S >= 84) for (const k of [0.014, 0.036]) for (const sd of [1, -1]) { const q = P(add(along(top, d, -k), mul(side, sd * 0.018))); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), INK_PEG, parts.HELD); }
}

/** His straw hat: a wide brim, a crown with a dark band, and the dent in the crown where the coin came down on it (on
    top, toward the front, on his right). */
function joeHat(cx) {
  const { ball, hp, onHead, hy, d, parts, S } = cx, hr = d.headR;
  ball(hp(0, 0.60, 0.05), [0.126, 0.012, 0.124], STRAW, { part: parts.HAT, fn: (ux, uy) => (ux * ux + uy * uy > 0.80 ? shifted(STRAW, 1) : undefined) }, hy);      // the brim, its edge a shade darker
  // the crown: tall enough to read, a dark band round its foot, and on his right the dent: the top knocked in (a notch out
  // of its outline as we see it) and the shadow inside it
  const deep = S >= 120 ? 0.34 : 0.40;
  ball(hp(0, 1.02, -0.02), [hr[0] * 0.98, hr[1] * 0.74, hr[2] * 0.96], STRAW, { part: parts.HAT, fn: (ux, uy, uz) => {
    const o = onHead(ux, uy, uz), right = o[0] > 0.04 && o[0] < 0.98;
    if (right && uy < -1 + deep && Math.abs(o[2]) < 0.88) return null;
    if (right && uy < -1 + deep + 0.30 && Math.abs(o[2]) < 0.95) return DENT;
    return uy > 0.42 ? HATBAND : undefined;
  } }, hy);
}

// Where the banjo is when he sits: across his knees, the pot on his right thigh, the neck over to his left; given in the
// space of his shoulders (as hands are), so it leans with him and his hands rest on it.
const JOE_LAP = { c: [0.060, -0.214, 0.172], u: [-0.92, 0.30, 0.20], n: [0.10, 0.36, 0.93] };
const JOE_REST = {
  R: { hand: [0.106, -0.170, 0.214], bend: [1, -0.6, -0.4], curl: 0.5, point: [-0.55, -0.45, 0.70] },       // his right hand over the head, where it strums
  L: { hand: [-0.176, -0.130, 0.208], bend: [-1, -0.7, -0.2], curl: 1.0, point: [0.30, 0.10, 0.95] },       // his left round the neck
};
const JOE_CARRY = { hand: [0.162, -0.296, 0.040], bend: [0.6, -1, -0.5], grip: true, loose: true };        // on his feet: the banjo by the neck, at his side
/** Where the banjo is now: on his lap, in his right hand, between the two while he gets up or sits down, or hanging from
    his folded hands while he prays standing. */
function joeBanjo(cx) {
  const { J, pose } = cx, T = (v) => add(J.sh, J.torso(v)), D = (v) => J.torso(v);
  const lap = { c: T(JOE_LAP.c), u: D(JOE_LAP.u), n: D(JOE_LAP.n) };
  const hand = (g) => { const u = D([0.10, 1, 0.12]); return { c: along(g, unit(u), -0.215), u, n: D([0.82, 0, 0.57]) }; };
  if (pose.seated && !(pose.rising > 0)) return banjo(cx, lap);
  if ((pose.praying || 0) > 0.5 && !pose.seated) return banjo(cx, hand(mix(J.R.palm, J.L.palm, 0.5)));
  const up = hand(J.R.palm);
  if (!(pose.rising > 0)) return banjo(cx, up);
  const e = smooth01((pose.rising - 0.20) / 0.70);                                            // (as the hand travels: risePose)
  return banjo(cx, { c: mix(lap.c, up.c, e), u: mix(lap.u, up.u, e), n: mix(lap.n, up.n, e) });
}

/** The rocking chair, drawn with him (sit.drawn): a seat and its cushion, a back of turned spindles under a broad top rail,
    two arms, four legs and two long curved rockers, the curve touching the ground under his hips. */
function rockingChair(cx) {
  const { J, limb, ball, parts, pose } = cx;
  if (!pose.seated || pose.noSeat) return;
  const hip = J.hipC, sy = J.seatY, at = (x, y, z) => [hip[0] + x, y, hip[2] + z], F = { part: parts.EXTRA3 };
  const arc = (z) => 0.78 - Math.sqrt(0.78 * 0.78 - z * z), rk = 0.012, X = 0.122;
  const back = (h) => -0.112 - h * 0.17;                               // the back leans back as it rises: where it is, h above the seat
  for (const sd of [1, -1]) {
    const zs = [-0.34, -0.26, -0.17, -0.08, 0.01, 0.10, 0.18, 0.25];
    for (let i = 0; i + 1 < zs.length; i++) limb(at(sd * X, arc(zs[i]) + rk, zs[i]), at(sd * X, arc(zs[i + 1]) + rk, zs[i + 1]), rk, rk, ROCKER, F);      // a rocker
    limb(at(sd * 0.114, sy - 0.020, 0.122), at(sd * X, arc(0.124) + rk * 1.6, 0.124), 0.0105, 0.0105, ROCKER, F);           // a front leg
    limb(at(sd * 0.114, sy - 0.020, -0.100), at(sd * X, arc(-0.124) + rk * 1.6, -0.124), 0.0105, 0.0105, ROCKER, F);        // a back leg
    limb(at(sd * 0.118, sy - 0.024, back(0)), at(sd * 0.128, sy + 0.500, back(0.50)), 0.0125, 0.0115, ROCKER, F);          // an upright of the back
    limb(at(sd * 0.120, sy - 0.010, 0.128), at(sd * 0.126, sy + 0.150, 0.132), 0.0100, 0.0100, ROCKER, F);                 // the post under the arm
    limb(at(sd * 0.124, sy + 0.165, back(0.165) + 0.010), at(sd * 0.130, sy + 0.158, 0.160), 0.0125, 0.0135, ROCKER, F);   // the arm
  }
  // the back: a broad top rail, a low rail, and five turned spindles between them, each with a bead turned in it
  limb(at(0.128, sy + 0.478, back(0.478)), at(0, sy + 0.500, back(0.500)), 0.0175, 0.0175, ROCKER, F);
  limb(at(0, sy + 0.500, back(0.500)), at(-0.128, sy + 0.478, back(0.478)), 0.0175, 0.0175, ROCKER, F);
  limb(at(0.118, sy + 0.090, back(0.090)), at(-0.118, sy + 0.090, back(0.090)), 0.0090, 0.0090, ROCKER, F);
  for (const x of [-0.078, -0.039, 0, 0.039, 0.078]) {
    limb(at(x, sy + 0.090, back(0.090)), at(x, sy + 0.470, back(0.470)), 0.0058, 0.0058, ROCKER, F);
    ball(at(x, sy + 0.26, back(0.26)), [0.0095, 0.012, 0.0095], ROCKER, F);
  }
  // the seat, and the cushion on it
  ball(at(0, sy - 0.020, 0.012), [0.132, 0.011, 0.136], ROCKER, F);
  ball(at(0, sy - 0.004, 0.010), [0.120, 0.016, 0.124], CUSHION, { part: parts.EXTRA2, fn: (ux, uy) => ((Math.floor((ux + 1) * 5) + Math.floor((uy + 1) * 2)) % 2 ? shifted(CUSHION, 1) : undefined) });
}

/** His rope (grandpajoe-tied): white twine with a red thread twisted in, regulation issue. */
const TWINE = ramp("#ffffff", "#f3f0e8", "#ccc6b6", "#908a7a");
const TWINE_RED = ramp("#ff8c80", "#e23a2c", "#aa281e", "#701812");
const twined = (t, nx, ny, x, y) => ((x + y) % 4 === 0 ? TWINE_RED : undefined);
/** The rope, as the suits tie it: his wrists bound together in front of him, a turn round his chest over the overalls and
    his arms, finished with a bow at the front. */
function ropes(cx) {
  const { J, limb, ball, d, parts, S, cloth, seatOnly } = cx;
  if (seatOnly) return;
  const T = (v) => add(J.sh, J.torso(v)), rope = { part: parts.EXTRA, bias: cloth * 2.4, fn: twined };
  // round the chest, over the arms: high enough to lie over the bib, wide enough to take in the upper arms
  const y = -0.082, hw = d.shoulderW + d.armR[0] + 0.016, hd = d.trunkTop[1] + d.bellyFwd * 0.3 + 0.018, rr = 0.0068;
  const pt = (a) => T([Math.sin(a) * hw, y, Math.cos(a) * hd]);
  for (let i = 0; i < 18; i++) limb(pt((2 * Math.PI * i) / 18), pt((2 * Math.PI * (i + 1)) / 18), rr, rr, TWINE, rope);
  // the bow, at the front
  const knot = T([0, y, hd + 0.004]), bow = { ...rope, bias: cloth * 3.2 };
  for (const sd of [1, -1]) {
    ball(T([sd * 0.024, y + 0.010, hd + 0.006]), [0.020, 0.013, 0.010], TWINE, { ...bow, fn: (ux, uy, uz, x, yy) => (S >= 110 && ux * ux * 0.9 + uy * uy < 0.16 ? null : twined(0, 0, 0, x, yy)) });
    limb(knot, T([sd * 0.016, y - 0.056, hd + 0.010]), 0.0060, 0.0050, TWINE, bow);           // the two ends, hanging
  }
  ball(knot, [0.010, 0.010, 0.010], TWINE, bow);
  // the wrists: bound together, a few turns, and the end left hanging
  const a = J.R.wrist, b = J.L.wrist, m = mix(a, b, 0.5);
  limb(a, b, d.armR[2] + 0.010, d.armR[2] + 0.010, TWINE, { ...rope, part: parts.HELD });
  for (const k of [-0.012, 0.012]) limb(add(a, [0, k, 0]), add(b, [0, k, 0]), 0.0055, 0.0055, TWINE, { ...rope, part: parts.HELD, bias: cloth * 3 });
  limb(m, add(m, [0.006, -0.060, 0.016]), 0.0055, 0.0045, TWINE, { ...rope, part: parts.HELD });
}

/** The seatbelt in the limousine: a gray band from his left shoulder down across him to his right hip, and its buckle
    ("Regulations."). Over the ropes, when there are ropes. */
const BELT_GRAY = ramp("#b8bcc4", "#8a8f99", "#636873", "#43474f");
function seatbelt(cx) {
  const { J, limb, d, parts, trunkAt, cloth, seatOnly, pose } = cx;
  if (seatOnly || !pose.seated) return;                                // (on his feet, it is unbuckled)
  const T = (v) => add(J.sh, J.torso(v)), from = T([-d.shoulderW + 0.010, 0.020, -0.012]), over = T([-d.shoulderW * 0.70, 0.004, d.trunkTop[1] * 0.70]);
  const to = trunkAt(d.waistY - 0.050, 1.05, 0.020), o = { part: parts.EXTRA2, bias: cloth * 4, depth: 0.35 };
  limb(from, over, 0.012, 0.013, BELT_GRAY, o);
  limb(over, to, 0.013, 0.013, BELT_GRAY, o);
  limb(add(to, J.torso([-0.010, 0.010, 0.006])), add(to, J.torso([0.014, -0.014, 0.008])), 0.012, 0.012, CHROME, { ...o, bias: cloth * 5, squareStart: true, squareEnd: true });      // the buckle
}

const JOE_FACE = { beard: SNOW, beardLen: 0.12, beardW: 0.74, beardZ: 0.52, beardFrom: [-0.40, 0.34], moustache: SNOW, moustacheW: 0.38, moustacheZ: 1.0,
  brows: SNOW.tones[2], browW: 3, eyes: "plain", eye: "#2a1a12", iris: "#86a6c4", lid: "#6a4a3a", noseShade: true, nose: [1.1, 1.15, 1.25], blush: "#e88d78", lines: 1, ear: 1.15, jaw: 0.90, chin: 0.56, smile: 1, mouthW: 0.24 };      // faded blue eyes; a full white beard and a moustache over it
const JOE_STAND = { swing: 0.32, arm: 0.20, lean: 0.07, lift: 0.85, bob: 0.010 };       // slow: the old-timer's walk, slower
/** Grandpa Joe's body, whatever he is doing: everything but what is in his hands. */
const joeBase = {
  name: "Grandpa Joe", height: 0.97, crown: 0.045,                     // (crown: the hat, for his words over it)
  dim: { ...ADULT, trunkTop: [0.110, 0.076], trunkLow: [0.110, 0.094], bellyFwd: 0.014, neckR: 1.04 },
  skin: SKIN_WEATHERED,
  hair: { mat: SNOW, bulk: 1.09, where: hairline({ front: 1.3, temple: 1.1, side: 0.06, back: -0.58 }) },      // white, round the sides and the back, under the hat
  face: JOE_FACE,
  top: { mat: JOE_PLAID, sleeves: 2, stripe: { mat: JOE_CHECK, at: [0.62, -0.62, 1.35, -1.35, Math.PI, Math.PI - 0.70, Math.PI + 0.70], half: 0.075 },
         bands: [[0.035, 0.052, JOE_CHECK], [0.100, 0.117, JOE_CHECK], [0.165, 0.182, JOE_CHECK], [0.230, 0.247, JOE_CHECK], [0.295, 0.312, JOE_CHECK]],
         check: { mat: JOE_CHECK, every: 0.062, band: 0.016, stripe: 0.22 } },          // a plaid: lines down it and across it, and down and across the sleeves
  bottom: { kind: "trousers", mat: OVERALLS, rise: 0.105, bib: { top: 0.092, half: 0.56, strap: 0.20, back: 0.60 } },      // bib overalls
  shoes: { kind: "boots", mat: ramp("#a2724a", "#76492b", "#50301b", "#301c10"), sole: ramp("#4d301a", "#372212", "#24160c", "#150d07") },
  stance: "straps",                                                     // a thumb hooked in the strap of his overalls
  walk: JOE_STAND, pace: 100,
  gestures: [0, 8, 0, 1, 5],                                            // a nod; one open hand, low; a nod; a point; a hand to his heart (small, all of them)
  fidgets: { stand: ["back"] },                                         // a hand to the small of his back
  pray: { high: -0.30, bow: 0.34 },                                     // on his feet: hands folded low, his head bowed, his hat on
};
/** The parts of him that go everywhere he goes: the hat, and two brass buttons on the bib. */
function joeGear(cx) {
  const { sf, P, J, d, parts, fine, th, trunkFacing } = cx;
  joeHat(cx);
  if (fine) for (const sd of [1, -1]) {
    const f = trunkFacing(sd * 0.40);
    if (f[0] * Math.sin(th) + f[2] * Math.cos(th) < 0.3) continue;
    const q = P(add(J.sh, J.torso([sd * 0.052, -0.098, d.trunkTop[1] + 0.006])));
    sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), BRASS.tones[1], parts.TORSO);
  }
}
/** Him standing, as he is when he gets up out of the rocking chair: the banjo by the neck in his right hand. */
const joeOnFeet = { hold: { R: JOE_CARRY }, rest: undefined, walk: JOE_STAND, pace: 100, span: 1.12, shadow: 0.18, pray: { high: -0.30, bow: 0.34 } };
export const grandpajoe = {
  ...joeBase,
  seated: "chair", sit: { seat: ROCKER_SEAT, lean: -0.13, knees: 0.16, feet: 0.12, drawn: true }, shadow: 0.27, span: 1.30, seatShadow: 0.21,      // he leans back in it a little
  rest: JOE_REST, banjoPot: JOE_LAP.c,                                  // (banjoPot: where his right hand strums: `strum` in rig.js)
  riseMs: 1350,                                                         // (slowly: forty years in that chair)
  stood: joeOnFeet,
  fidgets: { stand: ["back"], sit: ["hat", "rock", "strum"], not: ["knees"] },      // sitting: a touch to his hat, a slow rock, and a strum (figure.fidget("strum", { hold: true }) while he plays)
  pray: { fold: true, high: -0.22, out: 0.10, bow: 0.36 },              // sitting: his hat on, his head bowed, his hands folded on the banjo
  extras(c) { rockingChair(c); joeGear(c); joeBanjo(c); },
};

// ---------- NEVADA-12SA: Grandpa Joe on his feet, playing (the roadside's #12, the banjo's half-answer) ----------
// "I'll stand where you tell me and play what you like": he stands at the glass in the low sun and plays. Standing, he
// otherwise carries the banjo by the neck, and `strum` moves the hand that holds it; so, for playing on his feet, the
// banjo is held across him as it lies on his knees (JOE_LAP, in the space of his shoulders), his hands where they rest on
// it sitting (JOE_REST), and `strum` is his one small movement. The scene swaps him into this state at the glass and out
// of it again before he walks back to his chair (js/content/scenes/nevada-roadside.js).
export const grandpajoePlay = {
  ...joeBase, name: "Grandpa Joe, playing", span: 1.12, shadow: 0.18,
  rest: JOE_REST, banjoPot: JOE_LAP.c,
  fidgets: { only: true, stand: ["strum"] },
  extras(c) {
    joeGear(c);
    const { J } = c, T = (v) => add(J.sh, J.torso(v)), D = (v) => J.torso(v);
    banjo(c, { c: T(JOE_LAP.c), u: D(JOE_LAP.u), n: D(JOE_LAP.n) });
  },
};

// ---------- Grandpa Joe holding the sun shade up to the sun (PAINT-12A paints it: shade-held.png) ----------
/** Where his hands hold the sun shade (grandpajoe-shade), in the rig's own measure: the wrist, in the space of his shoulders
    (x to his right, y up, z ahead, from the middle of his shoulders), as guardShade.hold has them. Set from
    S/work-paintA/ready.md (the painter's `shade_hands`, in picture pixels, for him standing at [572, 560] facing E, drawn
    140 pixels tall: R [598, 482], the panel's near lower corner; L [602, 437], its near upper corner). If those points
    change, S/work-people/shade-hands.mjs works the numbers out again and checks them; S/work-people/ready.md gives the
    rule by hand. (SCENES-12 sets them.) */
export const SHADE_HANDS = { R: [0.030, -0.249, 0.155], L: [-0.010, 0.032, 0.198] };
// As the guard with the shade: his hands are where the painted panel's corners are when he stands at [572, 560] facing E
// (SHADE_HANDS, above), and nothing moves them. He talks with his head; the banjo leans on the rocking chair meanwhile.
export const grandpajoeShade = {
  ...joeBase, name: "Grandpa Joe, holding the shade", span: 1.2,
  hold: {
    R: { hand: SHADE_HANDS.R, bend: [0.55, -1, -0.35], grip: true, still: true },
    L: { hand: SHADE_HANDS.L, bend: [-0.55, -1, -0.35], grip: true, still: true },
  },
  gestures: [0, 2, 0, 4],                                               // a nod, a shake of the head and a lift of the shoulders, a nod, his head up: the arms never move
  fidgets: { only: true, stand: ["look"] },
  extras(c) { joeGear(c); },
};

// ---------- Grandpa Joe with what is left of the banjo: the neck in his right hand, strings trailing, no head ----------
const JOE_SWUNG = { hand: [0.150, -0.235, 0.110], bend: [0.5, -1, -0.5], grip: true };
export const grandpajoeBroken = {
  ...joeBase, name: "Grandpa Joe, with the broken banjo", span: 1.15,
  hold: { R: JOE_SWUNG },
  extras(c) {
    joeGear(c);
    const { J } = c, top = add(J.R.palm, J.torso([0.006, 0.034, -0.012]));
    brokenBanjo(c, top, J.torso([0.32, -0.78, 0.54]));
  },
};

// ---------- Grandpa Joe, tied up by the backup: cheerful about it ----------
const JOE_TIED = {
  R: { hand: [0.020, -0.214, 0.140], bend: [0.80, -1, -0.20], grip: true, still: true },
  L: { hand: [-0.020, -0.214, 0.140], bend: [-0.80, -1, -0.20], grip: true, still: true },
};
const joeTiedLife = {
  hold: JOE_TIED,
  gestures: [0, 2, 16, 4],                                              // his head and his shoulders: his hands stay where they are tied
  fidgets: { only: true, stand: ["shift", "look"] },
  walk: { swing: 0.29, arm: 0.0, lean: 0.05, lift: 0.80, bob: 0.010 }, pace: 90,       // slowly: it is hard to hurry tied up, and he is not trying
};
export const grandpajoeTied = {
  ...joeBase, ...joeTiedLife, name: "Grandpa Joe, tied up",
  extras(c) { joeGear(c); ropes(c); },
};

// ---------- the same, in the limousine: found sitting on the long seat (painted), the ropes, and a seatbelt over them ----------
export const grandpajoeSeatTied = {
  ...joeBase, ...joeTiedLife, name: "Grandpa Joe, tied up in the limousine",
  seated: "chair", sit: { seat: LIMO_SEAT, lean: -0.06, knees: 0.12 }, shadow: 0.24, span: 1.2,
  hold: {
    R: { hand: [0.022, -0.236, 0.190], bend: [0.80, -1, -0.30], grip: true, still: true },
    L: { hand: [-0.022, -0.236, 0.190], bend: [-0.80, -1, -0.30], grip: true, still: true },
  },
  fidgets: { only: true, sit: ["shift", "look"], stand: ["shift", "look"] },
  stood: { hold: JOE_TIED, span: 1.12, shadow: 0.18 },
  extras(c) { joeGear(c); ropes(c); seatbelt(c); },
};
// ---------- and loose: Ranger has had the ropes; the seatbelt stays on ("Regulations.") ----------
export const grandpajoeSeatLoose = {
  ...joeBase, name: "Grandpa Joe, in the limousine",
  seated: "chair", sit: { seat: LIMO_SEAT, lean: -0.06, knees: 0.12 }, shadow: 0.24, span: 1.2,
  fidgets: { stand: ["back"], sit: ["hat"] },
  pray: { fold: true, high: 0.0, out: 0.05, bow: 0.36 },                // sitting: his hands folded in his lap, his head bowed
  stood: { span: 1.1, shadow: 0.18, pray: { high: -0.30, bow: 0.34 } },
  extras(c) { joeGear(c); seatbelt(c); },
};

// ---------- Grandma Jolene: his wife, fifty-one years; certain, cheerful, wrong about every fact and right about every person ----------
// Tall and thin; a tower of gray hair with a yellow pencil through it; cat-eye glasses on a chain; a yellow cardigan with a
// hen brooch over a flowered blouse; an apron with a pocket; flat shoes. And a different hat each time the store is
// entered: `jolene` (a straw cowboy hat), `jolene-2` (a wide sun hat with fruit on it), `jolene-3` (a tiara), `jolene-4`
// (a yellow hard hat), `jolene-5` (a hen). The same woman under each.
const SILVER = ramp("#eceef2", "#c4c8d0", "#989ca8", "#686c78");
const SILVER_COIL = shifted(SILVER, 1);
const CARDIGAN = ramp("#ffec9a", "#f2c642", "#c6951e", "#86630f");
const BLOUSE = ramp("#ffffff", "#f6f2fa", "#cfc8dc", "#968ea8");
const SKIRT_PLUM = ramp("#b886a8", "#8c5c80", "#66405c", "#43283c");
const APRON = ramp("#e4f2ff", "#b4d4f0", "#88a8cc", "#5c7a9c");
const PENCIL = ramp("#fff2a0", "#ffd23f", "#d09a1c", "#8f6410");
const ERASER = ramp("#ffc4cc", "#f08a9a", "#c0606e", "#8a3e4a");
const JOLENE_SKIN = ramp("#fbe0cc", "#efc2a6", "#c8927a", "#8c5e4c");
const INK_FRAME = pack("#17808a"), INK_LENS = pack("#ffffff"), INK_CHAIN = pack("#f0d27a"), INK_HEN = pack("#ffffff"), INK_COMB = pack("#e4302a"), INK_BEAK = pack("#ffc02a"), INK_BLOSSOM = pack("#f0708c"), INK_FORGET = pack("#6a9ee8");
// The tower: from the crown of her head up and a little back, in her head's own half-sizes; and its top, where a hat goes.
const TOWER = { y0: 0.70, z0: -0.22, y1: 2.10, z1: -0.40, r0: 0.86, r1: 0.70 };
/** The top of her tower of hair, where the hat sits, and how to place a thing on it (turned and nodded with her head). */
function towerTop(cx) {
  const { headPt, d, hy } = cx, hr = d.headR, top = headPt([0, hr[1] * TOWER.y1 + hr[0] * TOWER.r1 * 0.92, hr[2] * TOWER.z1]);
  return { top, at: (v) => add(top, turn(v, hy)) };
}
/** Everything about her but the hat. */
function joleneBody(cx) {
  const { limb, hp, headPt, J, P, sf, d, S, th, hy, parts, fine, coarse, trunkAt, trunkFacing, skirtAt, cloth, under, pose, seatOnly } = cx, hr = d.headR;
  // the tower of gray hair, coiled
  limb(hp(0, TOWER.y0, TOWER.z0), hp(0, TOWER.y1, TOWER.z1), hr[0] * TOWER.r0, hr[0] * TOWER.r1, SILVER, { part: parts.HAIR,
    fn: (t, nx) => (((t * 4.2 + nx * 0.55 + 4) % 1) < 0.24 ? SILVER_COIL : undefined) });
  // the pencil, through it: the eraser end out on her right, where her hand pushes it back in
  const pm = (x, y, z) => headPt([x, hr[1] * (TOWER.y0 + (TOWER.y1 - TOWER.y0) * 0.55) + y, hr[2] * (TOWER.z0 + (TOWER.z1 - TOWER.z0) * 0.55) + z]);
  const pa = pm(0.078, -0.010, 0.020), pb = pm(-0.074, 0.018, -0.022);
  limb(pa, pb, 0.0052, 0.0052, PENCIL, { part: parts.HAT });
  limb(pa, along(pa, unit(sub(pa, pb)), 0.010), 0.0052, 0.0050, ERASER, { part: parts.HAT, squareEnd: true });
  limb(pb, along(pb, unit(sub(pb, pa)), 0.012), 0.0050, 0.0012, ramp("#f8e8c8", "#e8d0a0", "#b89c70", "#806a48"), { part: parts.HAT });
  if (seatOnly) return;
  // cat-eye glasses: a frame over each eye with a wing at the outer corner, placed where the rig puts the eyes
  const eyeX = cx.spec.face.eyeX ?? 0.36, eyeY = cx.spec.face.eyeY ?? 0.06, headPx = 2 * hr[0] * S, full = headPx >= 13.3, fineFace = headPx >= 10.0;
  const look = (v) => { const w = turn(v, hy); return w[0] * Math.sin(th) + w[2] * Math.cos(th); }, sideways = Math.sin(th + hy);
  const mid = P(hp(0, eyeY, 0.80))[0];
  for (const sd of [1, -1]) {
    const vis = look([sd * 0.25, 0, 0.97]);
    if (vis < 0.20) continue;
    const q = P(hp(sd * eyeX, eyeY, 0.80)), w = full && vis > 0.70 ? 2 : 1, right = Math.abs(sideways) > 0.86 ? sideways < 0 : q[0] > mid;
    const ex = right ? Math.round(q[0] - w / 2) : Math.round(q[0] + w / 2) - 1, ey = Math.round(q[1] - 0.5), out = right ? 1 : -1, put = (i, j, ink = INK_FRAME) => sf.dot(ex + out * i, ey + j, ink, parts.HEAD);
    if (full) {
      // a frame all round the eye, the upper outer corner swept up into a point, and a glint on the lens
      for (let i = -1; i <= w; i++) { put(i, -2); put(i, 1); }
      put(-1, -1); put(-1, 0); put(w, 0); put(w + 1, -2); put(w + 1, -3); put(w, -1);
      if (out < 0) put(0, -1, INK_LENS);
    } else {
      // small: the top of the frame over the eye, its wing, and its outer side
      for (let i = -1; i <= w; i++) put(i, -1);
      put(w + 1, -2);
      if (fineFace) put(w, 0);
    }
  }
  // the chain: hanging from the arms of the glasses at her temples, down past her jaw, and in a loop over her chest
  if (fine) {
    const ends = [1, -1].map((sd) => hp(sd * 1.00, eyeY - 0.02, 0.18)), low = add(J.sh, J.torso([0, -0.104, d.trunkTop[1] + 0.012]));
    for (const [n, e] of ends.entries()) {
      const sd = n === 0 ? 1 : -1, c1 = add(J.sh, J.torso([sd * 0.074, -0.020, d.trunkTop[1] * 0.80]));
      for (let i = 0; i <= 24; i++) {
        const t = i / 24;
        inkAt(cx, mix(mix(e, c1, t), mix(c1, low, t), t), INK_CHAIN);
      }
    }
  }
  // the hen brooch on her cardigan, over her heart
  const bf = trunkFacing(-0.46);
  if (!coarse && bf[0] * Math.sin(th) + bf[2] * Math.cos(th) > 0.25) {
    const q = P(trunkAt(d.shoulderY - 0.086, -0.46, 0.004)), x = Math.round(q[0] - 0.5), y = Math.round(q[1] - 0.5);
    sf.dot(x, y, INK_HEN, parts.TORSO); sf.dot(x, y - 1, INK_COMB, parts.TORSO);
    if (fine) { sf.dot(x + 1, y, INK_HEN, parts.TORSO); sf.dot(x, y + 1, INK_HEN, parts.TORSO); sf.dot(x + 1, y + 1, INK_HEN, parts.TORSO); sf.dot(x + (Math.sin(th) > 0 ? 2 : -1), y, INK_BEAK, parts.TORSO); }
  }
  // the blouse's flowers, in the opening of the cardigan
  if (fine) for (const [k, ink] of [[0.40, INK_BLOSSOM], [0.70, INK_FORGET], [0.92, INK_BLOSSOM]]) inkAt(cx, add(mix(add(J.sh, J.torso([0, 0.006, d.trunkTop[1] * 0.40])), add(J.sh, J.torso([0, -0.074, d.trunkTop[1] * 0.98])), k), J.torso([0, 0, 0.004])), ink, 0.03);
  // the apron's pocket
  if (skirtAt && !pose.seated) limb(skirtAt(0.20, 0.34, 0.006), skirtAt(0.44, 0.34, 0.006), 0.030, 0.030, shifted(APRON, 1), { part: parts.DRAPE, squareStart: true, squareEnd: true, depth: 0.3, bias: cloth, over: { [parts.SKIRT]: under } });
}
// ---- her hats: each one sits on the top of the tower ----
const COWBOY_STRAW = ramp("#fff4c4", "#f0d88e", "#c4a85c", "#86703a");
const TURQ_BAND = ramp("#9ee8e0", "#3fb4aa", "#2a807a", "#1a5450");
/** 1. A straw cowboy hat: the brim turned up at the sides, a crown pinched along the top, a turquoise band. */
function hatCowboy(cx) {
  const { ball, limb, hy, parts, S } = cx, { at } = towerTop(cx), H = { part: parts.HAT };
  ball(at([0, 0.004, 0.006]), [0.098, 0.010, 0.088], COWBOY_STRAW, H, hy);
  for (const sd of [1, -1]) limb(at([sd * 0.080, 0.008, 0.002]), at([sd * 0.100, 0.034, -0.002]), 0.0145, 0.0080, COWBOY_STRAW, H);      // the brim, curling up
  // the crown: tall, pinched along the top from front to back (a dip in the middle of its outline, and the crease's shadow), a band round its foot
  ball(at([0, 0.040, -0.004]), [0.046, 0.044, 0.052], COWBOY_STRAW, { ...H, bias: S * 0.05, fn: (ux, uy) => {
    const pinch = Math.abs(ux) < (S >= 120 ? 0.16 : 0.24);
    if (pinch && uy < -0.62) return null;
    if (pinch && uy < -0.30) return shifted(COWBOY_STRAW, 2);
    return uy > 0.50 ? TURQ_BAND : undefined;
  } }, hy);
}
const SUNHAT = ramp("#ffffff", "#fbf3e2", "#d6c8a8", "#9c8e70");
const RIBBON = ramp("#c4f0a8", "#78c860", "#4e9440", "#30602a");
/** 2. A wide sun hat with fruit on it: cherries, an orange, a lemon, a bunch of grapes, and a leaf. */
function hatFruit(cx) {
  const { ball, limb, hy, parts, S } = cx, { at } = towerTop(cx), H = { part: parts.HAT };
  ball(at([0, 0.002, 0.006]), [0.138, 0.020, 0.126], SUNHAT, { ...H, fn: (ux, uy) => (ux * ux + uy * uy > 0.80 ? shifted(SUNHAT, 1) : undefined) }, hy);      // the brim, wide (seen a little from above)
  ball(at([0, 0.034, -0.004]), [0.054, 0.038, 0.054], SUNHAT, { ...H, bias: S * 0.06, fn: (ux, uy) => (uy > 0.36 ? RIBBON : undefined) }, hy);
  const fruit = { part: parts.HAT, bias: S * 0.08 };
  ball(at([-0.044, 0.030, 0.034]), [0.022, 0.010, 0.014], RIBBON, fruit, hy);                                                // the leaf
  ball(at([0.036, 0.026, 0.040]), [0.0135, 0.0135, 0.0135], ramp("#ffc48a", "#ff8a1c", "#c8600e", "#8a3e06"), fruit);       // an orange
  ball(at([0.004, 0.022, 0.050]), [0.0130, 0.0100, 0.0105], ramp("#fffaa8", "#ffe63a", "#d0b414", "#8a760a"), fruit);       // a lemon
  for (const [x, z] of [[-0.024, 0.044], [-0.012, 0.050]]) ball(at([x, 0.018, z]), [0.0090, 0.0090, 0.0090], ramp("#ff8c8c", "#e8202a", "#a8141c", "#6e0c12"), fruit);      // cherries
  limb(at([-0.024, 0.026, 0.044]), at([-0.016, 0.044, 0.040]), 0.0025, 0.0025, RIBBON, fruit);
  for (const [x, y, z] of [[0.060, 0.024, 0.020], [0.068, 0.018, 0.010], [0.060, 0.012, 0.016], [0.070, 0.028, 0.002]]) ball(at([x, y, z]), [0.0075, 0.0075, 0.0075], ramp("#d8a8ff", "#9a52d8", "#6c3498", "#442062"), fruit);      // grapes
}
const TIARA = ramp("#ffffff", "#e8e0f0", "#a8a0b8", "#6c6478", { shine: true });
/** 3. A tiara: small, and glinting (the glints move as she breathes). */
function hatTiara(cx) {
  const { limb, ball, hp, sf, P, parts, pose, S, fine } = cx, H = { part: parts.HAT, bias: 1 };
  const on = (x, y) => hp(x, TOWER.y0 + 0.40 + y, TOWER.z0 + 1.02 - Math.abs(x) * 0.55);       // on the front of the tower, low
  const xs = [-0.82, -0.40, 0, 0.40, 0.82];
  for (let i = 0; i + 1 < xs.length; i++) limb(on(xs[i], -0.04 * Math.abs(xs[i])), on(xs[i + 1], -0.04 * Math.abs(xs[i + 1])), 0.0050, 0.0050, TIARA, H);
  for (const [x, hgt] of [[-0.52, 0.30], [0, 0.48], [0.52, 0.30]]) limb(on(x, 0), on(x, hgt), 0.0055, 0.0030, TIARA, H);         // its three points
  ball(on(0, 0.16), [0.0085, 0.0085, 0.0060], ramp("#a0d0ff", "#3a7ce8", "#2652a8", "#16306a", { shine: true }), { ...H, bias: 2 });      // a jewel
  if (!cx.seatOnly && S >= 52) {
    const k = Math.floor(((pose.breath || 0) * 2.99 + (pose.mouth || 0)) % 3), [x, hgt] = [[-0.52, 0.30], [0, 0.48], [0.52, 0.30]][k], q = P(on(x, hgt));
    sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), INK_GLINT, parts.HAT);
    if (fine) { sf.dot(Math.round(q[0] - 1.5), Math.round(q[1] - 0.5), INK_GLINT, parts.HAT); sf.dot(Math.round(q[0] + 0.5), Math.round(q[1] - 0.5), INK_GLINT, parts.HAT); }
  }
}
const HARDHAT = ramp("#fff6a0", "#ffd21e", "#d4a00c", "#8c6806", { shine: true });
/** 4. A yellow hard hat, a peak in front and a ridge along the top. */
function hatHard(cx) {
  const { ball, limb, hy, parts, S } = cx, { at } = towerTop(cx), H = { part: parts.HAT };
  ball(at([0, 0.006, 0.024]), [0.078, 0.012, 0.096], HARDHAT, { ...H, fn: (ux, uy) => (uy > 0.15 ? shifted(HARDHAT, 1) : undefined) }, hy);       // the brim, its peak out in front
  ball(at([0, 0.014, 0.000]), [0.068, 0.058, 0.074], HARDHAT, { ...H, bias: S * 0.04, fn: (ux, uy) => (uy > 0.12 ? null : undefined) }, hy);   // the dome
  limb(at([0, 0.066, 0.052]), at([0, 0.070, -0.054]), 0.0100, 0.0100, shifted(HARDHAT, -1), { ...H, bias: S * 0.06 });                     // the ridge
}
const HEN = ramp("#ffd8a0", "#f0a85a", "#c07832", "#80501c");            // a buff hen, plump as a cushion
const HEN_TAIL = ramp("#e0a868", "#a8682e", "#784818", "#4c2c0c");
const COMB = ramp("#ff8a7c", "#e8302a", "#a81c18", "#6e100e");
/** 5. A hen: a plump hen sitting on the top of the tower as if it were her nest, comb, wattle, beak, tail and all. When
    Jolene talks the hen pecks; when Jolene blinks, so does the hen. */
function hatHen(cx) {
  const { ball, limb, hy, parts, P, sf, pose, S, th, seatOnly } = cx, { at } = towerTop(cx), H = { part: parts.HAT };
  const peck = (pose.mouth || 0) === 2 ? 1 : 0;
  ball(at([0, 0.044, -0.006]), [0.066, 0.046, 0.082], HEN, H, hy);                                        // her body
  for (const sd of [1, -1]) ball(at([sd * 0.050, 0.048, -0.014]), [0.020, 0.028, 0.054], shifted(HEN, 1), { ...H, bias: 1 }, hy);      // the wings, folded
  for (const [x, a] of [[-0.016, 0.10], [0, 0.02], [0.016, -0.08]]) limb(at([x, 0.060, -0.066]), at([x + a * 0.10, 0.118, -0.098]), 0.0150, 0.0075, HEN_TAIL, H);      // her tail, up
  const head = at([0, 0.104 - 0.012 * peck, 0.060 + 0.010 * peck]);
  limb(at([0, 0.070, 0.040]), head, 0.022, 0.020, HEN, H);                                                // her neck
  ball(head, [0.024, 0.026, 0.026], HEN, H, hy);
  for (const [z, y, r] of [[0.024, 0.026, 0.0085], [0.010, 0.030, 0.0095], [-0.006, 0.026, 0.0085]]) ball(add(head, turn([0, y, z], hy)), [r * 0.8, r, r], COMB, { ...H, bias: 1 });      // the comb
  limb(add(head, turn([0, -0.002, 0.020], hy)), add(head, turn([0, -0.008 - 0.004 * peck, 0.042], hy)), 0.0072, 0.0020, ramp("#fff0a0", "#ffc21e", "#c8900c", "#805c06"), { ...H, bias: 2 });      // the beak
  ball(add(head, turn([0, -0.022, 0.018], hy)), [0.0060, 0.0090, 0.0060], COMB, { ...H, bias: 1 });      // the wattle
  if (!seatOnly && S >= 52) for (const sd of [1, -1]) {
    const e = turn([sd * 0.80, 0.25, 0.55], hy);
    if (e[0] * Math.sin(th) + e[2] * Math.cos(th) < 0.15) continue;
    const q = P(add(head, turn([sd * 0.018, 0.006, 0.010], hy)));
    sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), pose.blink ? HEN.tones[2] : pack("#1a1210"), parts.HAT);
  }
}
const joleneOf = (n, hat, crown, hatAt) => ({
  name: "Grandma Jolene", height: 1.02, crown, tall: 1.42, span: 1.10, hatAt, pencilAt: TOWER.y0 + (TOWER.y1 - TOWER.y0) * 0.55,
  dim: { ...WOMAN, headR: [0.052, 0.063, 0.060], shoulderW: 0.080, trunkTop: [0.082, 0.056], trunkLow: [0.064, 0.050], pelvisR: [0.084, 0.056, 0.066],
         armR: [0.022, 0.019, 0.0135], handR: 0.018, legR: [0.042, 0.026, 0.017], footR: 0.017, bust: [0.000, 0.024], neckR: 0.84 },
  skin: JOLENE_SKIN,
  hair: { mat: SILVER, bulk: [1.07, 1.05, 1.07], where: hairline({ front: 0.54, temple: 0.36, side: 0.02, back: -0.36, brow: 0.45, temples: 1.10 }) },      // all of it swept up into the tower
  face: { eyes: "girl", eye: "#2a2030", iris: "#6a7a5a", lid: "#4a3040", brows: SILVER.tones[2], browUp: 4, blush: "#f09a8a", lip: "#c04a5a", lips: "#d86a78", lines: 1,
          nose: [1.0, 1.0, 1.05], noseShade: true, jaw: 0.82, chin: 0.48, chinY: -0.84, smile: 1, mouthW: 0.24, big: { eyeW: 0.44, eyeH: 0.44, lashes: 1, arch: 0.30 } },
  top: { mat: CARDIGAN, sleeves: 2, hem: 0.020, open: 0.072, under: BLOUSE, band: BLOUSE, cuffs: shifted(CARDIGAN, 1) },         // the cardigan over the blouse, and the blouse's round collar
  bottom: { kind: "skirt", mat: SKIRT_PLUM, len: 1.42, flare: 1.10, folds: [[-0.75, 0.2], [0.80, 0.25], [2.6, 0.2]] },
  apron: { mat: APRON, half: 0.86, len: 1.30 },
  shoes: { kind: "pumps", mat: ramp("#ff9a8a", "#d8483a", "#9a2e26", "#621c18"), sole: ramp("#7a3a2e", "#5a281e", "#3e1a14", "#240e0a") },      // flat shoes, red
  stance: "hip",                                                        // a fist on her hip
  walk: { swing: 0.46, arm: 0.34, lean: 0.05, sway: 0.016, twist: 0.10, bob: 0.010 }, pace: 178,          // brisk
  gestures: [0, 11, 9, 5],                                              // a nod; a finger in the air; her hands going; a hand to her heart: small and quick
  fidgets: { stand: ["pencil", "hat"] },                                // she pushes the pencil back into her hair; she sets her hat straight
  pray: { high: 0.50, bow: 0.26 },
  extras(c) { joleneBody(c); hat(c); },
  hatNo: n,
});
// (crown: how far the hat rises over the top of her head, for her words; hatAt: the height of its brim, in half-heights of
//  her head, for her hand when she sets it straight)
export const jolene = joleneOf(1, hatCowboy, 0.176, 3.35);
export const jolene2 = joleneOf(2, hatFruit, 0.166, 3.30);
export const jolene3 = joleneOf(3, hatTiara, 0.096, 2.50);
export const jolene4 = joleneOf(4, hatHard, 0.186, 3.30);
export const jolene5 = joleneOf(5, hatHen, 0.248, 3.40);

// ---------- the backup: four men in gray, the man in gray's spec four times over ----------
// Each a hair different in height and build, the hair a little different; all of them in black sunglasses, with an earpiece
// (a pale coil behind the right ear, a dot in it); the same walk, so that they walk in step; hands behind their backs. One
// has a clipboard, one a tape measure on his belt, one a juice box, and one the paper bag with the cheeseburger in it.
const EARPIECE = ramp("#fffdf2", "#ebe6d6", "#c0baa6", "#8a8676");
const SUIT_WALK = { swing: 0.42, arm: 0.26, lean: 0.03 };
/** The earpiece: a pale coil from behind the right ear down into the collar, and the bud in the ear. */
function earpiece(cx) {
  const { ball, hp, J, hy, parts } = cx;
  ball(hp(1.03, -0.10, -0.04), [0.0070, 0.0075, 0.0070], EARPIECE, { part: parts.EAR, bias: 2 }, hy);
  const from = hp(0.95, -0.32, -0.34), to = add(J.sh, J.torso([0.044, 0.016, -0.036])), pts = [from];
  for (let i = 1; i <= 7; i++) pts.push(add(mix(from, to, i / 7), J.torso([(i % 2 ? 0.006 : -0.004), 0, (i % 2 ? -0.004 : 0.004)])));
  thread(cx, pts, EARPIECE);
}
const CLIPBOARD = ramp("#d8a874", "#b07c48", "#80562e", "#54381c"), PAPER = ramp("#ffffff", "#f6f4ee", "#d0ccc0", "#9a968a");
const suitOf = (o) => ({
  ...agent, name: "Man in Gray", stance: "behind", walk: SUIT_WALK, gestures: [0, 8, 0, 10],
  ...o,
  face: { shades: "#15161c", ...(o.face || {}) },
  extras(c) { agent.extras(c); earpiece(c); if (o.gear) o.gear(c); hankie(c); },      // (OFFICE-17P: hankie, while one of them mops his brow)
});
export const suit1 = suitOf({
  height: 0.97,
  dim: { ...ADULT, shoulderW: 0.098, trunkTop: [0.108, 0.072], trunkLow: [0.096, 0.076] },
  hair: { mat: ramp("#bcb8b4", "#928e8a", "#6a6664", "#484644"), where: hairline({ front: 0.72, temple: 0.64, side: 0.24, back: -0.42, recede: 0.16 }) },      // going gray, and going
  face: { mouthW: 0.16, nose: [1.0, 1.05, 1.1] },
  hold: { L: { hand: [-0.060, -0.196, 0.120], bend: [-1, -0.5, -0.4], grip: true } },          // the clipboard
  fidgets: { stand: ["watch", "tie"] },
  gear(c) {
    const { limb, J, wide, deep, parts, sf, P, fine } = c, g = J.L.palm, w = [0.066, 0.006], r = wide(w), b0 = add(g, [0.022, -0.020, 0.016]), b1 = add(g, [0.034, 0.150, 0.004]);
    limb(b0, b1, r, r, CLIPBOARD, { part: parts.HELD, depth: deep(w) / r, squareStart: true, squareEnd: true });
    const p0 = add(mix(b0, b1, 0.05), [0, 0, 0.004]), p1 = add(mix(b0, b1, 0.86), [0, 0, 0.004]), rp = wide([0.056, 0.004]);
    limb(p0, p1, rp, rp, PAPER, { part: parts.HELD, depth: deep([0.056, 0.004]) / rp, squareStart: true, squareEnd: true, bias: 1 });
    limb(add(mix(b0, b1, 0.90), [-0.020, 0, 0.006]), add(mix(b0, b1, 0.90), [0.020, 0, 0.006]), 0.0085, 0.0085, CHROME, { part: parts.HELD, bias: 2 });      // the clip
    if (fine) for (const k of [0.30, 0.45, 0.60]) { const q = P(add(mix(b0, b1, k), [0, 0, 0.008])); sf.dot(Math.round(q[0] - 1.5), Math.round(q[1] - 0.5), pack("#9aa0b0"), parts.HELD); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), pack("#9aa0b0"), parts.HELD); }
  },
});
export const suit2 = suitOf({
  height: 1.0,
  dim: { ...ADULT, shoulderW: 0.108, trunkTop: [0.120, 0.078], trunkLow: [0.104, 0.080] },
  skin: ramp("#dcae86", "#bf8c60", "#8f6040", "#603e28"),
  hair: { mat: ramp("#8e6a4c", "#664830", "#46321f", "#2c1e12"), where: hairline({ front: 0.58, temple: 0.46, side: 0.20, back: -0.44, sweep: 0.12 }),
          texture: (x, y, z) => (Math.abs(x + 0.36) < 0.05 && y > 0.40 && z > -0.30 ? ramp("#46321f", "#2c1e12", "#2c1e12", "#2c1e12") : undefined) },      // parted on the side
  face: { nose: [0.95, 1.0, 1.2], jaw: 0.96, chin: 0.60 },
  fidgets: { stand: ["watch", "tie"] },
  gear(c) {                                                             // the tape measure, clipped at his right hip
    const { limb, ball, trunkAt, d, parts, cloth, sf, P, fine } = c, at = trunkAt(d.hipY - 0.030, 1.30, 0.018), o = { part: parts.EXTRA, bias: cloth * 3 };
    limb(add(at, [0, 0.020, 0]), add(at, [0, -0.020, 0]), 0.022, 0.022, ramp("#fff2a0", "#ffd21e", "#c89a0c", "#806006"), { ...o, squareStart: true, squareEnd: true, depth: 0.8 });
    ball(add(at, [0, -0.002, 0]), [0.008, 0.008, 0.024], ramp("#5a5a60", "#2c2c32", "#1a1a1e", "#0c0c0e"), { ...o, bias: cloth * 3.5 });
    if (fine) { const q = P(add(at, [0, 0.022, 0])); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), pack("#e8eaf0"), parts.EXTRA); }
  },
});
export const suit3 = suitOf({
  height: 1.02,
  dim: { ...ADULT, shoulderW: 0.102, trunkTop: [0.110, 0.072], trunkLow: [0.094, 0.070], neckR: 0.96 },
  skin: ramp("#f2cca6", "#dcaa80", "#ad7a56", "#744e36"),
  hair: { mat: ramp("#5c514c", "#3e3632", "#2a2420", "#181412"), bulk: 1, where: hairline({ front: 0.70, temple: 0.60, side: 0.26, back: -0.34 }) },      // cropped close
  face: { smile: 0, mouthW: 0.18, jaw: 0.86, chin: 0.48 },
  hold: { R: { hand: [0.110, -0.232, 0.120], bend: [0.6, -1, -0.4], grip: true } },           // the juice box
  fidgets: { stand: ["watch"] },
  gear(c) {
    const { limb, J, parts, sf, P, fine } = c, g = J.R.palm, box = ramp("#d8f6a0", "#8ccf3e", "#5e9a24", "#3a6414");
    limb(add(g, [0, -0.020, 0.004]), add(g, [0, 0.044, 0.004]), 0.020, 0.020, box, { part: parts.HELD, squareStart: true, squareEnd: true, depth: 0.7 });
    limb(add(g, [0.006, 0.044, 0.000]), add(g, [0.010, 0.074, -0.004]), 0.0030, 0.0030, ramp("#ffffff", "#f4f0f0", "#d0caca", "#9a9494"), { part: parts.HELD });      // the straw
    if (fine) { const q = P(add(g, [0, 0.012, 0.024])); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), pack("#e8302a"), parts.HELD); }      // an apple on it
  },
});
export const suit4 = suitOf({
  height: 0.99,
  dim: { ...ADULT, shoulderW: 0.104, trunkTop: [0.118, 0.080], trunkLow: [0.112, 0.090], bellyFwd: 0.012 },
  skin: ramp("#ffd6c0", "#f4b49a", "#c88068", "#8c5444"),
  hair: { mat: ramp("#ecd296", "#c8a462", "#98783a", "#664e22"), where: hairline({ front: 0.56, temple: 0.46, side: 0.22, back: -0.42 }), puffs: [[0.12, 0.88, 0.42, 0.44, 0.24, 0.36]] },      // sandy, a little wave in front
  face: { smile: 1, mouthW: 0.22, nose: [0.9, 0.95, 1.0], jaw: 0.94, chin: 0.58 },
  hold: { R: { hand: [0.150, -0.330, 0.040], bend: [0.4, -1, -0.5], grip: true } },          // the paper bag
  fidgets: { stand: ["watch"] },
  gear(c) {
    const { limb, J, parts, sf, P, fine } = c, g = J.R.palm, kraft = ramp("#ecc890", "#c89a5e", "#987040", "#664a28");
    limb(add(g, [0, 0.008, 0]), add(g, [0, -0.034, 0]), 0.024, 0.026, kraft, { part: parts.HELD, squareStart: true, depth: 0.25 });                   // the top of it, rolled down, in his fist
    limb(add(g, [0, -0.030, 0]), add(g, [0, -0.130, 0]), 0.042, 0.044, kraft, { part: parts.HELD, squareStart: true, squareEnd: true, depth: 0.62 });
    if (fine) { const q = P(add(g, [-0.010, -0.090, 0.040])); for (const [i, j] of [[0, 0], [1, 0], [0, 1]]) sf.dot(Math.round(q[0] - 0.5) + i, Math.round(q[1] - 0.5) + j, pack("#b08250"), parts.HELD); }      // a spot of grease
  },
});

// ---------- Jed, after the banjo: the hoop round his neck like a collar, his sunglasses crooked, dust on his knees ----------
// Found sitting in the dust where the banjo sat him down: his legs out in front of him, leaning back on his hands (sit.seat
// "floor", in rig.js). `stood`: on his feet again, the hoop still on.
const HOOP_WOOD = ramp("#f0c890", "#d09a5c", "#a06a34", "#68421c");
function hoop(cx) {
  const { J, limb, parts, cloth, seatOnly } = cx;
  if (seatOnly) return;
  const ctr = add(J.sh, J.torso([0, -0.004, 0.006])), tilt = 0.32, ax = J.torso([1, 0, 0]), az = J.torso([0, -Math.sin(tilt), Math.cos(tilt)]), R = 0.090;
  const o = { part: parts.COLLAR, bias: cloth * 2 };
  const at = ring(cx, ctr, az, ax, R, 0.0120, HOOP_WOOD, o, 22);
  ring(cx, add(ctr, [0, 0.008, 0]), az, ax, R + 0.006, 0.0060, CHROME, { ...o, bias: cloth * 2.6 }, 22);           // the chrome round its top edge
  // the drum head's broken edge, in tatters, round the inside
  for (let i = 0; i < 16; i++) {
    const a = (2 * Math.PI * i) / 16 + 0.17, len = 0.010 + 0.014 * (((i * 7) % 5) / 4), p = at(a), q = add(ctr, mul(sub(p, ctr), (R - 0.012 - len) / R));
    limb(add(mix(p, ctr, 0.10), [0, 0.006, 0]), add(q, [0, 0.004, 0]), 0.0058, 0.0025, BANJO_HEAD, { ...o, bias: cloth * 2.2 });
  }
  // two strings hanging from it, down his front
  for (const [a, len, sw] of [[0.30, 0.150, 1], [-0.42, 0.110, -1]]) {
    const top = at(a), pts = [];
    for (let i = 0; i <= 6; i++) { const t = i / 6; pts.push(add(top, [0.010 * sw * Math.sin(t * 4), -len * t, 0.012 + 0.006 * t])); }
    thread(cx, pts);
  }
}
/** Dust on the knees of his trousers: a lighter patch on each. */
function dusty(cx) {
  const { J, sf, P, parts, S, th, seatOnly } = cx;
  if (seatOnly || S < 52) return;
  for (const k of ["R", "L"]) {
    const L = J[k], front = mul(L.calfBack, -1), kn = add(mix(L.knee, L.ankle, 0.06), mul(front, 0.030));
    if (front[0] * Math.sin(th) + front[2] * Math.cos(th) < -0.2) continue;
    const q = P(kn), x = Math.round(q[0] - 0.5), y = Math.round(q[1] - 0.5);
    for (const [i, j] of S >= 110 ? [[-1, 0], [0, 0], [1, 0], [0, 1], [-1, -1], [0, -1], [1, 1]] : [[0, 0], [1, 0], [0, 1]]) sf.mark(x + i, y + j, -1, parts.LEG[k]);
  }
}
export const agentCollar = {
  ...agent, name: "Man in Gray, with the banjo's hoop",
  seated: "ground", sit: { seat: "floor", nod: -0.03 }, shadow: 0.28, span: 1.40, under: 0.04,       // sat down in the dust
  face: { ...agent.face, shadesTilt: 1 },                                                                   // his sunglasses knocked crooked
  riseMs: 1500,
  stood: { span: 1.05, under: 0, shadow: 0.18 },
  fidgets: { stand: ["watch", "tie"], sit: [] },
  extras(c) { agent.extras(c); hoop(c); dusty(c); },
};


// =====================================================================================
// NEVADA-12SC (round twelve, the cut-scene "Backup": js/content/cutscenes/backup.js): Grandpa Joe at three more moments,
// and two of the backup carrying him. Each is someone above at another moment of the story, as `lot-standing` is Lot.
// =====================================================================================
/** Grandpa Joe on his feet with no rocking chair: the man who has just let the sun shade down, the banjo by the neck in
    his right hand (what Figure.sit(false) makes of him, put in his place by a scene). */
export const grandpajoeStanding = { ...upOf(grandpajoe), name: "Grandpa Joe, standing" };
/** The banjo up over his head, by the neck, the pot high and the strings to the sky: the moment before it comes down on
    Jed (and, a moment later, `grandpajoe-broken`). His other thumb stays in his strap: he is not in a hurry even now. */
const JOE_RAISED = { hand: [0.120, 0.300, 0.120], bend: [1, 0.2, -0.6], grip: true };
export const grandpajoeSwing = {
  ...grandpajoeStanding, name: "Grandpa Joe, the banjo raised", hold: { R: JOE_RAISED }, tall: 1.55, span: 1.2,
  fidgets: { only: true, stand: [] },
  extras(c) {
    joeGear(c);
    const { J } = c, u = J.torso([0.18, -1, 0.30]);                     // up the neck: down from the pot, through his hand
    banjo(c, { c: along(J.R.palm, unit(u), -0.215), u, n: J.torso([0.82, 0, 0.57]) });
  },
};
/** Tied up, and lifted off his feet by two of the backup ("Lifting on three, sir"): carried to the limousine with his hat
    on and his boots off the ground. The same man as `grandpajoe-tied`, with no shadow of his own (he is in the air: the
    scene draws him a few pixels above where his feet would be, between the two who carry him). */
export const grandpajoeCarried = { ...grandpajoeTied, name: "Grandpa Joe, tied up and carried", shadow: 0, fidgets: { only: true, stand: [] } };
/** Two of the backup carrying him between them: both hands out in front at the height of his elbows, holding on (politely). */
const CARRY = {
  R: { hand: [0.070, -0.150, 0.230], bend: [0.7, -1, -0.2], grip: true },
  L: { hand: [-0.070, -0.150, 0.230], bend: [-0.7, -1, -0.2], grip: true },
};
export const suit2Carry = { ...suit2, name: "Man in Gray, carrying", hold: CARRY, fidgets: { only: true, stand: [] } };
export const suit3Carry = { ...suit3, name: "Man in Gray, carrying (with the juice box)", hold: CARRY, fidgets: { only: true, stand: [] } };

// =====================================================================================
// ROME-13P (round thirteen): the bigger Rome's seven people, and their other states
// =====================================================================================
// Who they are: briefs/out/rome2-design.md (3.3; and 6.1 for Eleazar). All of them people of our own: nobody's likeness,
// no film's costume. Dressed as 44 B.C. dressed (the design's 7.7): a man's tunic belted at the knee; a citizen's toga plain
// white, a senator's mark the broad purple stripe down his tunic; a woman's tunic long, and a mantle over her head out of
// doors; Romans clean-shaven, Greeks, Jews and Gauls often bearded. Each one's own small movements are written after them
// (addMoves: rig.js), and their holds (`holds`, kept through whatever is said: figure.hold(true, "bless") in a scene).
const { cloneP, withArm, nodOf, free, skeleton, torsoOf } = moveKit;

/** The seats the Rome scenes paint, in the rig's measure (CM), set from the painters' reports as LIMO_SEAT was. A seated
    person's place (`at`) is the ground under their hips, and the top of the seat is this far above it. */
export const CAPITOL_BASE_SEAT = 120 * CM;     // Titus's statue base on the Capitol (PAINT-13R2's marks.titus_seat.cm)
export const TIBER_BENCH_SEAT = 45 * CM;       // the bench by the house of prayer (PAINT-13R3's marks.bench_seat.cm)
/** The blessing: Eleazar facing E, the boy facing him (W) on the same row, the boy's feet this many of Eleazar's drawn
    heights in front of Eleazar's (to the right on the screen). Eleazar's `bless` hold lays his right hand on the crown of
    the boy's head there, bowed (the boy in his own prayer, as at the date seller's blessing). */
export const BLESS_STEP = 0.30;

/** A point of a seated person's lap in the space of their shoulders (as hands are placed): `along` from the hips toward
    the knees, `up` above the thighs. For resting their hands on what lies in it. */
function lapAt(spec, along = 0.5, up = 0.04) {
  const J = skeleton(spec.dim, poses.sit({ ...spec, rest: undefined, hold: undefined }, 0));
  return torsoOf(J)(lapOf(J, along, up));
}
/** The same point of a drawn figure's lap (its joints J), for drawing what lies there. */
const lapOf = (J, along = 0.5, up = 0.04) => add(mix(J.hipC, mix(J.R.knee, J.L.knee, 0.5), along), [0, up, 0]);
/** A direction given in a figure's own space, turned into the space of its shoulders (torsoOf turns points). */
const dirIn = (toT, J, v) => toT(add(J.sh, v));
const held = (cx) => ({ part: cx.parts.HELD });

// ---------- the Gaul: Gaius Iulius Litumarus of Nemausus, made a senator by the dictator, lost in the Forum ----------
// About forty-five; big, broad and proud; fair-red hair combed back and worn longer than a Roman's, a long drooping
// moustache and a shaven chin (a Gaulish nobleman's fashion), fair skin the Italian sun has reddened, a gold ring round his
// right wrist; a senator's tunic with the broad stripe, and a senator's shoes. `gaul` wears the Roman senator's best
// toga, taken by mistake: far too short for him, stopping above his knees, its folds skimpy and pulled tight. `gaul-own`,
// after the swap, is the same man in his own new toga, very large, falling properly. Both plain white. He stands, and
// walks, like a man walking on ice: upright, short careful steps, his arms kept still.
const GAUL_SKIN = ramp("#ffdcc8", "#f6b8a0", "#d0846a", "#934e3e");
const GAUL_HAIR = ramp("#f7be7a", "#dd8c47", "#ad5d29", "#723b17");
const GAUL_TACHE = ramp("#cf7c3c", "#a95c28", "#7e401c", "#552810");     // his moustache: a shade deeper than his hair, so that it reads on his face
const gaulBase = {
  name: "Gaulish Senator", height: 1.08, lean: -0.03,
  dim: { ...ADULT, headR: [0.056, 0.066, 0.064], shoulderW: 0.112, trunkTop: [0.120, 0.078], trunkLow: [0.104, 0.080], bellyFwd: 0.008, pelvisR: [0.100, 0.064, 0.078],
         armR: [0.034, 0.029, 0.020], legR: [0.055, 0.036, 0.024], handR: 0.024, neckR: 1.12 },
  skin: GAUL_SKIN,
  hair: { mat: GAUL_HAIR, bulk: [1.09, 1.08, 1.12], where: hairline({ front: 0.66, temple: 0.50, side: -0.34, back: -1.05, brow: 0.50, temples: 1.12 }),
          puffs: [[0, -0.66, -0.70, 0.86, 0.44, 0.46]],                 // down to his collar behind
          texture: (x, y, z) => (y > 0.20 && z > -0.5 && Math.abs(Math.sin(x * 9.4)) < 0.17 ? shifted(GAUL_HAIR, 1) : undefined) },      // combed straight back: the comb's lines
  face: { eyes: "plain", eye: "#202838", iris: "#6f8fae", brows: GAUL_HAIR.tones[2], browW: 4, lines: 1, nose: [1.1, 1.15, 1.1], noseShade: true, jaw: 0.96, chin: 0.62, chinZ: 0.50, lip: "#b0604e", mouthW: 0.22, ear: 1.05 },
  top: { mat: UNDYED_PALE, sleeves: 0.46, stripe: { mat: PURPLE, at: [0], half: 0.17 } },       // a senator's tunic, the broad stripe down it, as the senator's
  shoes: { kind: "shoes", mat: RED_LEATHER, sole: shifted(RED_LEATHER, 2) },                       // and a senator's shoes, as his
  hold: { L: { hand: [-0.104, -0.214, 0.090], bend: [-0.6, -0.5, -0.6], curl: 0.9 } },           // his left arm carries the folds
  hand: "R",
  walk: { swing: 0.30, arm: 0.14, elbow: 0.20, lean: -0.02, lift: 0.75, twist: 0.04, sway: 0.008 },
  pace: 132,
  gestures: [0, 8, 11, 2],                              // a nod; an open hand; a finger raised (every word chosen); a shrug
};
/** His moustache, long, drooping past the corners of his mouth; and the gold ring round his right wrist. */
function gaulGear(c) {
  const { limb, hp, J, d, parts, spec } = c, my = spec.face.mouthY ?? -0.74;
  for (const sd of [1, -1]) {
    const a = hp(sd * 0.04, my + 0.22, 1.00), b = hp(sd * 0.28, my + 0.08, 0.92), e = hp(sd * 0.34, my - 0.42, 0.78);
    limb(a, b, 0.0064, 0.0060, GAUL_TACHE, { part: parts.HAIR });
    limb(b, e, 0.0060, 0.0040, GAUL_TACHE, { part: parts.HAIR });
  }
  limb(mix(J.R.elbow, J.R.wrist, 0.84), mix(J.R.elbow, J.R.wrist, 0.97), d.armR[2] + 0.0055, d.armR[2] + 0.0050, GOLD, { part: parts.EXTRA2, squareStart: true, squareEnd: true });
}
export const gaul = {
  ...gaulBase,
  bottom: { kind: "skirt", mat: WOOL, len: 0.94, flare: 1.03, folds: [[-0.9, 0.3, 0.94, 0.12], [0.55, 0.45, 0.94, -0.12], [0.05, 0.6, 0.94]] },      // the toga's wrap: it stops short of his knees
  fidgets: { stand: ["tug", "crane", "fold", "ask"] },  // tugs it down; looks up at the crane; folds his arms; asks the air, and shrugs
  extras(c) { wear.toga(c, { mat: WOOL, scant: 0.62, hang: 0.18 }); gaulGear(c); },
};
export const gaulOwn = {
  ...gaulBase, name: "Gaulish Senator, in his own toga",
  bottom: { kind: "skirt", mat: WOOL, len: 1.88, flare: 1.12, folds: [[-1.0, 0.3, 1.88, 0.1], [0.55, 0.5, 1.88, -0.1], [0.05, 0.9, 1.88, 0.05], [-0.45, 0.2, 1.4], [1.25, 0.3, 1.88], [2.5, 0.2], [-2.4, 0.4], [3.0, 0.6]] },
  fidgets: { stand: ["crane", "fold", "ask"] },
  extras(c) { wear.toga(c, { mat: WOOL, scant: 1.16, hang: -0.06 }); gaulGear(c); },
};

// ---------- Phyllis: Fannia Phyllis, a Greek freedwoman and a widow, who sells garlands at the foot of Castor's temple ----------
// About fifty-five; small, quick, sun-browned; grey hair under a dark mantle drawn over her head; a long tunic to the ankles;
// sandals. She is found sitting on a low stool that is drawn with her (it stays where it is when she gets up, as the
// goldsmith's does), among her baskets (painted). `phyllis` has the little clay lamp, wrapped in a cloth, in her lap: her
// present for her son. `phyllis-free` has given it away, and has a half-made garland in her hands. On her feet she hangs a
// garland on her pole, shoos a pigeon, calls to the square, and sits again. Fast and warm; soft about her son.
const BROWNED = ramp("#eab48c", "#d2946a", "#a36846", "#6b4430");
const PALLA = ramp("#80687a", "#5a4654", "#3e3039", "#271d24");          // her mantle: dark wool
const ROSE_WOOL = ramp("#ecb4a2", "#cc8a78", "#9e6052", "#6c3e34");      // her tunic: a red long since faded
const VIOLET = ramp("#dab2f8", "#a46ede", "#7648ae", "#4c2c74");
const MYRTLE = ramp("#a2d07c", "#68a04c", "#467034", "#2c4a22");
const LAMP_CLOTH = ramp("#fffaf0", "#f0e6cf", "#c8ba9a", "#90846a");
const COIN = ramp("#ffffff", "#dde1e8", "#a0a6b0", "#666b74");
/** A mantle worn over the head, as a woman wore hers out of doors: round the body as a mantle is, and drawn up over the back
    of her head, a little clear of the brow, falling to the shoulders at each side. */
function palla(c, mat) {
  const { ball, limb, onHead, headPt, hp, J, d, hy, parts } = c, hr = d.headR, T = (x, y, z) => add(J.sh, J.torso([x, y, z]));
  wear.mantle(c, { mat, len: 0.46, front: 0.22 });
  ball(headPt([0, 0.006, -0.006]), [hr[0] * 1.20, hr[1] * 1.15, hr[2] * 1.18], mat, { part: parts.HAT, fn: (ux, uy, uz) => { const q = onHead(ux, uy, uz); return q[2] < 0.20 + 0.42 * Math.max(0, q[1]) ? undefined : null; } }, hy);
  for (const sd of [1, -1]) limb(hp(sd * 1.04, -0.30, 0.02), T(sd * (d.shoulderW - 0.012), 0.012, 0.006), 0.030, 0.038, mat, { part: parts.HAT });
  limb(hp(0, -0.45, -0.82), T(0, -0.060, -(d.trunkTop[1] + 0.012)), 0.054, 0.062, mat, { part: parts.HAT });
}
/** The little clay lamp in its cloth: the cloth wrapped up round it, the lamp's top and nozzle showing out of it (or, `open`,
    the cloth turned back under it): `at` its middle, `fw` the way its nozzle points. */
function clayLamp(cx, at, fw, open = false) {
  const { ball, limb } = cx, o = held(cx), f = unit([fw[0], 0, fw[2]]);
  if (!open) ball(add(at, [0, -0.004, 0]), [0.048, 0.024, 0.040], LAMP_CLOTH, { ...o, fn: (ux, uy) => (uy < -0.25 ? null : undefined) });     // the cloth, wrapped up round it
  else ball(add(at, [0, -0.012, 0]), [0.046, 0.008, 0.040], LAMP_CLOTH, o);                                                                 // the cloth, turned back
  ball(add(at, [0, open ? 0 : 0.008, 0]), [0.032, 0.017, 0.029], CLAY, o);                                                                   // the lamp: round and low
  limb(add(at, mul(f, 0.018)), add(add(at, mul(f, 0.048)), [0, open ? 0.004 : 0.011, 0]), 0.0110, 0.0090, CLAY, o);                        // its nozzle
  ball(add(at, [0, open ? 0.015 : 0.023, 0]), [0.0095, 0.0042, 0.0095], shifted(CLAY, 2), o);                                              // the hole in its top, dark
  if (open) limb(add(at, mul(f, -0.020)), add(add(at, mul(f, -0.030)), [0, 0.010, 0]), 0.0048, 0.0042, shifted(CLAY, 1), o);             // and the little handle
}
/** A garland between two points: myrtle threaded with violets, hanging in a curve (`sag`: how far it dips; `out`: how far
    it comes forward as it dips, in the figure's own space, so that one lying across a lap shows over the knees). */
function garland(cx, a, b, sag = 0.030, n = 9, out = 0) {
  const { ball } = cx, o = held(cx), fw = cx.J.torso([0, 0, 1]);
  for (let i = 0; i <= n; i++) {
    const k = 4 * (i / n) * (1 - i / n), t = i / n, p = add(add(mix(a, b, t), [0, -sag * k, 0]), mul(fw, out * k)), flower = i % 3 === 1;
    ball(p, flower ? [0.0110, 0.0110, 0.0110] : [0.0140, 0.0112, 0.0140], flower ? VIOLET : MYRTLE, o);
  }
}
const phyllisBody = {
  name: "Garland Seller", height: 0.88, seated: "chair", shadow: 0.20, span: 1.25,
  dim: { ...WOMAN, headR: [0.055, 0.066, 0.063], shoulderW: 0.082, trunkTop: [0.086, 0.060], trunkLow: [0.072, 0.056], pelvisR: [0.094, 0.060, 0.072], armR: [0.024, 0.020, 0.0145], handR: 0.019, legR: [0.045, 0.029, 0.018], bust: [0.002, 0.026], neckR: 0.86 },
  skin: BROWNED,
  hair: { mat: GREY_HAIR, bulk: 1.04, where: hairline({ front: 0.58, temple: 0.44, side: 0.0, back: -0.50, brow: 0.45, temples: 1.10 }), texture: (x, y, z) => (Math.abs(x) < 0.05 && y > 0.50 && z > 0.10 ? shifted(GREY_HAIR, 1) : undefined) },
  face: { eyes: "girl", eye: "#2a1a12", iris: BROWN_EYES, lid: "#3a2218", brows: GREY_HAIR.tones[2], blush: "#d98a6c", lip: "#9a4a40", lines: 1, nose: [1.0, 0.95, 1.0], noseShade: true, jaw: 0.84, chin: 0.46, chinY: -0.82, smile: 1, mouthW: 0.22 },
  top: { mat: ROSE_WOOL, sleeves: 0.80, cuff: 0.012, belt: shifted(ROSE_WOOL, 2), blouse: 0.012 },
  bottom: { kind: "skirt", mat: ROSE_WOOL, len: 1.92, flare: 1.10, folds: [[-0.8, 0.3, 1.92, 0.06], [0.7, 0.4, 1.92, -0.06], [0.1, 0.8, 1.92], [2.5, 0.3], [-2.5, 0.3]] },
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  sit: { seat: "stool", lean: 0.12, knees: 0.12, drawn: true },        // a low stool, drawn with her: it stays where it is when she gets up
  riseMs: 900,
  walk: { swing: 0.44, arm: 0.36, lean: 0.06, sway: 0.014, twist: 0.08 }, pace: 172,      // small quick steps
  gestures: [8, 9, 5, 0],                               // an open hand (her patter); her hands going; a hand to her heart (her son); a nod
  pray: { high: 0.50, bow: 0.28 },
};
const PH_LAP = lapAt(phyllisBody, 0.72, 0.086);
const PH_REST = {                                       // her hands round what is in her lap
  R: { hand: add(PH_LAP, [0.054, -0.012, -0.016]), bend: [1, -0.4, -0.4], curl: 0.8, point: [-0.7, -0.1, 0.7] },
  L: { hand: add(PH_LAP, [-0.054, -0.012, -0.016]), bend: [-1, -0.4, -0.4], curl: 0.8, point: [0.7, -0.1, 0.7] },
};
/** Her stool and her mantle; and what she has in her hands or her lap, by what she is doing: `lap` "lamp" or "garland". */
function phyllisGear(c, lap) {
  const { J, pose, seatOnly } = c;
  wear.stool(c, { mat: WOOD, r: 0.062 });
  palla(c, PALLA);
  if (seatOnly) return;
  const sitting = pose.seated && !(pose.rising > 0), f = pose.fidget, u = pose.fu || 0, mid = mix(J.R.palm, J.L.palm, 0.5), fw = J.torso([0, 0, 1]);
  if (sitting && f === "offer" && u > 0.18 && lap === "lamp") return clayLamp(c, add(mid, [0, 0.016, 0]), fw, true);                         // unwrapped, and held out
  if (sitting && (f === "weave" && u > 0.10 && u < 0.90)) garland(c, J.L.palm, J.R.palm, 0.034, 7);
  if (sitting && f === "count" && u > 0.16 && u < 0.86) for (const [x, z] of [[-0.006, 0.006], [0.008, -0.004], [0.000, -0.012]]) c.ball(add(J.L.palm, J.torso([x, 0.010, z])), [0.0062, 0.0030, 0.0062], COIN, held(c));
  if (f === "sniff" && u > 0.22 && u < 0.80) { const s = J.R; c.limb(s.tip, add(s.tip, [0, -0.026, 0]), 0.0022, 0.0022, MYRTLE, held(c)); c.ball(add(s.tip, [0, 0.006, 0]), [0.0090, 0.0080, 0.0090], VIOLET, held(c)); }
  if (f === "hang" && u > 0.12 && u < 0.88) return garland(c, J.L.palm, J.R.palm, 0.050, 9);
  if (lap === "lamp") {
    if (sitting) clayLamp(c, lapOf(J, 0.72, 0.086), fw);
    else clayLamp(c, add(J.L.palm, [0, -0.010, 0.006]), fw);         // on her feet: held against her in her left hand
  } else if (!(f === "weave" && sitting)) {
    if (sitting) garland(c, add(J.L.palm, J.torso([-0.020, 0.006, 0.004])), add(J.R.palm, J.torso([0.020, 0.006, 0.004])), 0.020, 11, 0.050);      // across her knees, in her hands
    else garland(c, J.L.palm, add(J.L.palm, [0, -0.090, 0.020]), 0.010, 6);      // on her feet: hanging from her left hand
  }
}
export const phyllis = {
  ...phyllisBody, rest: PH_REST,
  stood: { hold: { L: { hand: [-0.050, -0.190, 0.098], bend: [-1, -0.5, -0.4], curl: 1.0 } }, rest: undefined },     // on her feet: the lamp held against her
  fidgets: { sit: ["weave", "sniff", "count", "peer"], stand: ["hang", "shoo", "call", "peer"] },
  extras(c) { phyllisGear(c, "lamp"); },
};
export const phyllisFree = {
  ...phyllisBody, name: "Garland Seller, the lamp given", rest: PH_REST,
  stood: { rest: undefined },
  fidgets: { sit: ["weave", "sniff", "count", "peer"], stand: ["hang", "shoo", "call", "peer"] },
  extras(c) { phyllisGear(c, "garland"); },
};

// ---------- Titus: the keeper's boy, about eleven, born free, found up on a statue's base on the Capitol ----------
// Skinny, dark curls, a big grin, a tunic too big for him (it was his father's), sandals, and round his neck a small
// leather amulet on a cord (the freeborn boy's charm, the poor boy's kind). `titus` is found sitting on top of a statue's
// base among the kings (painted, not drawn with him: CAPITOL_BASE_SEAT), his legs hanging down its front, the soothsayer's
// breakfast knotted in a cloth in his lap; on his feet he has it in his hand. Getting down is a hop (figure.sit(false):
// about 400 ms, onto his feet on the ground in front of the base). `titus-free` is him on his feet with nothing in his
// hands, ready to run home. He talks like his father, without stopping for breath; boasting, then honest.
const OCHRE_THIN = ramp("#f8dcaa", "#e4bb82", "#b48c56", "#7a5c36");     // his tunic: his father's colour, washed thin
const CHECK = ramp("#ffffff", "#f1efe8", "#c8c6bd", "#8c8a84");           // the cloth the breakfast is knotted in, as its picture has it (art/items/breakfast.png):
const CHECK_LINE = ramp("#b2cbf4", "#7898d6", "#5470a8", "#344a72");      // white, checked with blue
const CORD = ramp("#7c5a3c", "#5a3e28", "#3e2a1a", "#28180e");
const titusBase = {
  name: "Keeper's Boy", height: 0.78,
  dim: { ...blend(CHILD, ADULT, 0.30), trunkTop: [0.084, 0.056], trunkLow: [0.074, 0.054], pelvisR: [0.080, 0.054, 0.062], armR: [0.021, 0.018, 0.0135], legR: [0.037, 0.026, 0.018], handR: 0.021, neckR: 0.80 },
  skin: OLIVE,
  hair: { mat: DARK_HAIR, bulk: [1.12, 1.12, 1.12], where: hairline({ front: 0.42, temple: 0.28, side: -0.12, back: -0.52, brow: 0.50, temples: 1.12 }),
          texture: (x, y, z) => (curl(x, y, z, 8) ? shifted(DARK_HAIR, 1) : undefined),
          puffs: [[0.30, 0.86, 0.36, 0.30, 0.24, 0.28], [-0.34, 0.84, 0.30, 0.30, 0.24, 0.28], [0, 0.96, -0.10, 0.36, 0.22, 0.40], [0.66, 0.50, 0.10, 0.24, 0.30, 0.30], [-0.66, 0.50, 0.10, 0.24, 0.30, 0.30], [0, 0.40, -0.80, 0.50, 0.40, 0.30]] },      // dark curls, all over
  face: { eyes: "bright", eye: "#2a1a12", iris: BROWN_EYES, brows: DARK_HAIR.tones[2], blush: "#e89a7a", noseShade: true, eyeY: -0.04, mouthY: -0.70, jaw: 0.82, chin: 0.44, chinY: -0.80, nose: [0.7, 0.75, 0.85], lip: "#9a4a3c", smile: 1, mouthW: 0.32, ear: 1.20 },      // a big grin, and ears that stick out
  top: { mat: OCHRE_THIN, sleeves: 0.74, cuff: 0.020, belt: shifted(ROPE, 1), beltLow: 0.020, blouse: 0.026 },       // too big: the sleeves to his elbows, a roll of it over the belt
  bottom: { kind: "skirt", mat: OCHRE_THIN, len: 1.22, flare: 1.18, folds: [[-0.8, 0.2], [0.85, 0.3], [0.1, 0.5]] },  // and too long: below his knees
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  gestures: [9, 1, 18, 4],                              // his hands going; making a point; "everybody"; "ta-da" (boasting)
};
/** The amulet: a small leather pouch on a cord round his neck, on his chest. */
function amulet(c) {
  const { J, ball, d, parts, seatOnly } = c;
  if (seatOnly) return;
  const T = (x, y, z) => add(J.sh, J.torso([x, y, z])), at = T(0, -0.074, d.trunkTop[1] + 0.012);
  thread(c, [T(0.030, 0.016, 0.014), T(0.020, -0.034, d.trunkTop[1] * 0.80), at], CORD);
  thread(c, [T(-0.030, 0.016, 0.014), T(-0.020, -0.034, d.trunkTop[1] * 0.80), at], CORD);
  ball(at, [0.0115, 0.0130, 0.0080], HIDE, { part: parts.EXTRA, bias: 2 });
}
/** The breakfast, knotted in its checked cloth: in his lap on the base, at his chest while he hops down or draws his feet
    up, and by its knot in his left hand on his feet. Peeking, he has the knot open, and there is the loaf. */
function breakfast(c) {
  const { J, pose, ball, seatOnly } = c;
  if (seatOnly) return;
  const sitting = pose.seated && !(pose.rising > 0), f = pose.fidget, u = pose.fu || 0, chest = sitting && f === "feet" && u > 0.06 && u < 0.88;
  const at = sitting && !chest ? lapOf(J, 0.42, 0.040) : chest || pose.rising > 0 ? add(J.L.palm, J.torso([0.010, 0.000, 0.016])) : add(J.L.palm, [0, -0.038, 0]);
  const peek = f === "peek" && u > 0.30 && u < 0.80;
  ball(at, [0.040, 0.030, 0.034], CHECK, { ...held(c), fn: (ux, uy) => (Math.abs(((ux * 2.6 + 9) % 1) - 0.5) < 0.13 || Math.abs(((uy * 2.6 + 9) % 1) - 0.5) < 0.13 ? CHECK_LINE : undefined) });
  if (peek) ball(add(at, [0, 0.022, 0]), [0.026, 0.012, 0.024], BREAD, held(c));                                           // the loaf, under the opened knot
  else for (const sd of [1, -1]) ball(add(at, J.torso([sd * 0.010, 0.028, 0])), [0.010, 0.010, 0.009], CHECK, held(c));      // the knot's two ears
}
export const titus = {
  ...titusBase, seated: "chair", tall: 1.5, shadow: 0.0001, span: 1.15,          // (tall: room in his picture for the base he sits on top of; no shadow of his own up there)
  sit: { seat: CAPITOL_BASE_SEAT, lean: 0.05, knees: 0.10, feet: 0.06, clutch: "L" },     // his legs hanging down the base's front; hopping down, he clutches the bundle (rig.js hopPose)
  rest: { L: { hand: add(lapAt({ ...titusBase, seated: "chair", sit: { seat: CAPITOL_BASE_SEAT, lean: 0.05, knees: 0.10, feet: 0.06 } }, 0.42, 0.040), [-0.034, 0.008, -0.030]), bend: [-1, -0.4, -0.4], curl: 0.8, point: [0.6, -0.3, 0.7] } },
  riseMs: 420,
  stood: { hand: "L", rest: undefined, shadow: 0.17, walk: { swing: 0.54, arm: 0.60, lean: 0.10, lift: 1.25, bob: 0.04 }, pace: 200 },     // on his feet: the bundle by its knot in his left hand (the one he holds out)
  fidgets: { only: true, sit: ["wave", "peek", "statue"], stand: ["shift", "look"] },     // on the base, his own only: he waves at the boy, peeks into the cloth, is a statue
  extras(c) { amulet(c); breakfast(c); },
};
export const titusFree = {
  ...titusBase, name: "Keeper's Boy, empty-handed", shadow: 0.17,
  walk: { swing: 0.56, arm: 0.66, elbow: 0.40, pump: 0.30, lean: 0.12, lift: 1.30, bob: 0.05 }, pace: 215,      // ready to run home
  fidgets: { stand: [] },
  extras(c) { amulet(c); },
};

// ---------- the goose-keeper: Titus Rubrius Anser, about sixty, who holds the Republic's contract to feed Juno's geese ----------
// Heavy, slow, a leather apron over his tunic, a basket of grain on his hip, a long stick in his other hand, big hands.
// Among the geese he carries the stick held flat and low, never raised. Mournful and devoted, and full of the story of the
// Gauls, which he tells to anyone. His hands are busy (the basket, the stick): he talks with his head.
const ANSER_SKIN = ramp("#f2be98", "#da9c74", "#aa6e4e", "#724634");
const GOOSE_WOOL = ramp("#ccb89e", "#ab967c", "#7c6a56", "#524636");     // a brown work tunic
const GRAIN = ramp("#fcecb4", "#e8cd82", "#b89c52", "#7c682e");
/** The basket of grain on his left hip: wide and shallow, woven, heaped with grain; shaken, a little of it jumps. */
function grainBasket(c, r0 = 0.084) {
  const { ball, J, pose } = c, g = J.L.palm, axis = [J.hipC[0], g[1], J.hipC[2]], inward = norm([axis[0] - g[0], 0, axis[2] - g[2]]);
  const at = [g[0] + inward[0] * r0 * 0.94, g[1] - 0.022, g[2] + inward[2] * r0 * 0.94];
  ball(add(at, [0, 0.020, 0]), [r0 * 0.90, 0.020, r0 * 0.90], GRAIN, { ...held(c), fn: (ux, uy) => (cell(Math.floor(ux * 7 + 40), Math.floor(uy * 4 + 40)) % 5 === 0 ? shifted(GRAIN, 1) : undefined) });
  ball(at, [r0, 0.034, r0], WICKER, { ...held(c), fn: (ux, uy) => (uy < -0.12 ? null : uy < 0.12 ? undefined : Math.floor((uy + 1) * 5.0) % 2 ? shifted(WICKER, 1) : undefined) });
  if (pose.fidget === "shake" && pose.fu > 0.10 && pose.fu < 0.80) {
    const k = Math.floor(pose.fu * 10);
    for (let i = 0; i < 4; i++) ball(add(at, [(((i * 37 + k * 13) % 9) - 4) * 0.012, 0.050 + ((i + k) % 3) * 0.018, ((i * 23 + k * 7) % 7 - 3) * 0.010]), [0.0060, 0.0060, 0.0060], GRAIN, held(c));
  }
}
/** His stick: planted at his side; walking among the geese, held flat and low, pointing ahead of him. */
function gooseStick(c) {
  const { J, limb, pose, parts } = c;
  if (!pose.gait) return wear.staff(c, "R", { mat: STAFF, top: 1.12, r: 0.0072 });
  const g = J.R.palm, dir = unit(J.torso([-0.30, -0.04, 0.95]));
  limb(along(g, dir, -0.30), along(g, dir, 0.86), 0.0080, 0.0064, STAFF, { part: parts.HELD });
}
export const anser = {
  name: "Goose-Keeper", height: 1.0, lean: 0.04,
  dim: { ...ADULT, headR: [0.058, 0.066, 0.064], shoulderW: 0.108, trunkTop: [0.116, 0.078], trunkLow: [0.116, 0.088], bellyFwd: 0.018, paunch: [0.108, 0.060, 0.078, 0.020],
         pelvisR: [0.104, 0.064, 0.080], armR: [0.036, 0.031, 0.022], legR: [0.056, 0.036, 0.024], handR: 0.027, neckR: 1.16, thigh: 0.232, shin: 0.218 },
  skin: ANSER_SKIN,
  hair: { mat: GREY_HAIR, bulk: 1.05, where: hairline({ front: 0.64, temple: 0.40, side: 0.06, back: -0.44, recede: 0.20 }) },      // grey, and going at the temples
  face: { eyes: "heavy", eye: "#2a1a12", iris: BROWN_EYES, lid: "#5a3a2a", brows: GREY_HAIR.tones[2], browW: 4, browTilt: -1, jowl: 0.84, jaw: 0.96, chin: 0.60, nose: [1.25, 1.3, 1.45], noseShade: true, lip: "#8a4a3a", smile: -1, mouthW: 0.22, lines: 2, ear: 1.2 },      // mournful: heavy lids, a long face, a big nose
  top: { mat: GOOSE_WOOL, sleeves: 0.44, cuff: 0.014, belt: shifted(HIDE, 1) },
  bottom: { kind: "skirt", mat: GOOSE_WOOL, len: 0.98, flare: 1.08, folds: [[-0.9, 0.2], [1.0, 0.3], [2.4, 0.2], [-2.3, 0.35]] },
  apron: { mat: HIDE, half: 0.90, len: 0.94, bib: 0.11 },               // a leather apron, up over his chest
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  hold: { L: { hand: [-0.202, -0.236, 0.136], bend: [-1, -0.3, -0.75], grip: true }, R: { hand: [0.208, -0.190, 0.110], bend: [0.25, -1, -0.45], grip: true } },     // the basket on his hip; the stick
  walk: { swing: 0.34, arm: 0.16, lean: 0.06, sway: 0.026, twist: 0.06, lift: 0.80 },
  pace: 105,
  gestures: [0, 2, 0, 16],                              // with his hands full: a nod, a shrug of the shoulders, a nod, his head down
  fidgets: { only: true, stand: ["shift", "look", "shake", "stick", "tally", "sigh"] },     // shakes the basket; leans on his stick; counts his geese; sighs
  extras(c) { grainBasket(c); gooseStick(c); },
};

// ---------- Eleazar: the devout Jew of Rome, about sixty-five, the date seller's father-in-law ----------
// Born in Jerusalem; a grown man there when Pompey took it, carried to Rome a captive, long since freed. Lean, a little
// stooped, a full white beard, grey hair, dark deep-set eyes, weathered hands; a long tunic of undyed wool to the calf, and
// over it a mantle with a tassel at each of its four corners, each tassel with a thread of blue (Numbers 15:38: the rig's
// mantle, `tassels` and `thread`); sandals. (The small leather cases of the commandments, only probable for this date, are
// left off.) He calls the boy "child", and never hurries.
// - `eleazar-window`: standing at his upper window, head bare, at his morning prayer, facing the river (W): his way of
//   standing is his prayer (stance "prayer": his hands folded at his breast, so that they show over the sill; his head
//   bowed; his eyes shut), and his one small movement is `lift` (his head lifted a while, his lips moving, then bowed again)
//   and `murmur` (his lips moving): his life plays them. Drawn at the window's own scale (PAINT-13R3's marks.window).
// - `eleazar`: found sitting on the bench before the house of prayer (painted: TIBER_BENCH_SEAT), his scroll open in his
//   hands. On his feet (`stood`) he has it rolled in his left hand, which a prayer takes (hold.loose); his prayer standing,
//   hands folded low and his head bowed; and the hold `bless`: his right hand laid on the crown of the boy standing facing
//   him at BLESS_STEP, the boy's head bowed.
const ELEAZAR_SKIN = ramp("#ecc49e", "#d0a078", "#a07050", "#6a4634");    // weathered
const ELEAZAR_MANTLE = ramp("#8c7a6a", "#645444", "#46392e", "#2b231c");  // his mantle: dark brown wool
const TASSEL = ramp("#fffdf6", "#f4ecdc", "#d0c6ae", "#9a907a");         // its tassels: white wool,
const TEKHELET = ramp("#a4beff", "#3462e2", "#2446a8", "#16296c");       // a thread of blue in each
const PARCHMENT = ramp("#fcf2d8", "#ecdcb2", "#c4ae82", "#8c7856");      // his scroll
const WRIT = ramp("#a08c70", "#7c6a54", "#5a4c3c", "#3c3228");           // and the lines of its writing
const ELEAZAR_FACE = { eyes: "deep", eye: "#1a120c", iris: "#3c2a1e", brows: GRIZZLE.tones[2], browW: 4, beard: SNOW, beardLen: 0.30, beardW: 0.72, beardZ: 0.42, beardFrom: [-0.42, 0.24],
  moustache: SNOW, moustacheW: 0.34, moustacheZ: 1.0, lip: "#8a4e40", lines: 2, nose: [1.15, 1.2, 1.05], noseShade: true, jaw: 0.84, chin: 0.48, ear: 1.15 };
const eleazarBody = {
  name: "Old Man", height: 0.96, lean: 0.07,
  dim: { ...ADULT, headR: [0.055, 0.066, 0.063], shoulderW: 0.094, trunkTop: [0.096, 0.064], trunkLow: [0.084, 0.064], pelvisR: [0.088, 0.058, 0.068], armR: [0.025, 0.022, 0.016], legR: [0.044, 0.029, 0.020], handR: 0.023, neckR: 0.88 },
  build: "old",
  skin: ELEAZAR_SKIN,
  hair: { mat: GREY_HAIR, bulk: 1.06, where: hairline({ front: 0.70, temple: 0.50, side: -0.22, back: -0.70, recede: 0.10, burn: 0.50 }) },
  face: ELEAZAR_FACE,
  top: { mat: UNDYED, sleeves: 0.88, cuff: 0.012, belt: shifted(ROPE, 1) },
  bottom: { kind: "skirt", mat: UNDYED, len: 1.56, flare: 1.06, folds: [[-0.85, 0.3, 1.56, 0.08], [0.50, 0.5, 1.56, -0.08], [-0.15, 0.9, 1.56], [2.6, 0.3], [-2.5, 0.4]] },
  shoes: { kind: "sandals", mat: HIDE, sole: shifted(HIDE, 1) },
  walk: { swing: 0.32, arm: 0.18, lean: 0.06, lift: 0.85, bob: 0.008 },
  pace: 100,
  gestures: [0, 8, 5, 0],                               // few and slow: a nod; an open hand, low; a hand to his heart; a nod
  pray: { high: -0.25, bow: 0.36 },                     // standing: his hands folded low, his head bowed
};
const eleazarMantle = (c) => wear.mantle(c, { mat: ELEAZAR_MANTLE, len: 0.42, front: 0.24, tassels: TASSEL, thread: TEKHELET });
/** His scroll: open between his hands as he reads (two rolls, and the sheet between them with its lines of writing), or
    rolled up, in one hand on his feet, or in his folded hands at prayer. */
function scroll(c) {
  const { J, pose, limb, ball, seatOnly, wide } = c;
  if (seatOnly) return;
  const o = held(c), up = unit(J.torso([0, 1, 0.30])), sitting = pose.seated && !(pose.rising > 0);
  const roll = (at, len = 0.080) => { limb(along(at, up, -len / 2), along(at, up, len / 2), 0.0118, 0.0118, PARCHMENT, { ...o, squareStart: true, squareEnd: true }); for (const k of [-1, 1]) ball(along(at, up, k * (len / 2 + 0.004)), [0.0060, 0.0050, 0.0060], WOOD, o); };
  const apart = Math.hypot(J.R.palm[0] - J.L.palm[0], J.R.palm[1] - J.L.palm[1], J.R.palm[2] - J.L.palm[2]);
  if (sitting && apart < 0.20 && pose.fidget !== "beard") {
    const a = add(J.R.palm, J.torso([-0.010, 0.012, 0.006])), b = add(J.L.palm, J.torso([0.010, 0.012, 0.006])), w = [0.038, 0.002], r = wide(w);
    limb(a, b, 0.036, 0.036, PARCHMENT, { ...o, depth: 0.10, squareStart: true, squareEnd: true, fn: (t, nx, ny) => (t > 0.12 && t < 0.88 && Math.abs(ny) < 0.62 && Math.floor(t * 9) % 2 === 0 ? WRIT : undefined) });
    void r;
    roll(a); roll(b);
    return;
  }
  const g = (pose.praying || 0) > 0.5 && !sitting ? mix(J.R.palm, J.L.palm, 0.5) : J.L.palm;
  roll(add(g, J.torso([0, 0.006, 0.010])), 0.090);
}
export const eleazarWindow = {
  ...eleazarBody, name: "Old Man, at his window", stance: "prayer",
  pray: { high: 0.74, bow: 0.30, out: -0.012 },         // at the window: his hands folded at his breast (they show over the sill), his head bowed
  face: { ...ELEAZAR_FACE, eyes: "shut" },
  gestures: [0],
  fidgets: { only: true, stand: ["lift", "murmur"] },   // his life: his head lifted a while, his lips moving; and bowed again
  extras(c) { eleazarMantle(c); },
};
const ELEAZAR_SIT = { seat: TIBER_BENCH_SEAT, lean: 0.10, knees: 0.08, solid: true };
const EL_LAP = lapAt({ ...eleazarBody, seated: "chair", sit: ELEAZAR_SIT }, 0.52, 0.090);
export const eleazar = {
  ...eleazarBody, seated: "chair", shadow: 0.22, span: 1.2,
  sit: ELEAZAR_SIT,                                     // the bench by the house of prayer, as it is painted
  rest: { R: { hand: add(EL_LAP, [0.040, 0.010, -0.026]), bend: [1, -0.4, -0.4], grip: true, point: [-0.5, 0.2, 0.8] }, L: { hand: add(EL_LAP, [-0.040, 0.010, -0.026]), bend: [-1, -0.4, -0.4], grip: true, point: [0.5, 0.2, 0.8] } },      // his scroll open between his hands
  pray: { fold: true, high: 0.0, out: 0.06, bow: 0.36 },                     // sitting: his hands folded on the scroll in his lap
  riseMs: 1250,
  stood: { hold: { L: { hand: [-0.140, -0.300, 0.060], bend: [-0.4, -1, -0.4], grip: true, loose: true } }, rest: undefined, span: 1.1, shadow: 0.18, pray: { high: -0.25, bow: 0.36 },
           holds: { bless: (o) => blessPose(o) } },     // on his feet: the scroll rolled in his left hand (which a prayer takes); and the blessing
  fidgets: { sit: ["unroll", "read", "beard", "still"], stand: ["beard"], not: ["knees", "scratch"] },     // unrolls his scroll a little; reads, a finger following; strokes his beard; is still
  extras(c) { eleazarMantle(c); scroll(c); },
};

// ---------- Mariam: Eleazar's granddaughter, about eight, born in Rome, in the hen yard ----------
// Small and quick, dark hair in a plait (brought over her shoulder, so that it shows), a long plain tunic, bare feet, a dish
// of grain on her hip. Certain about everything, especially hens; bossy, fond, quick to laugh. Her own girl: not Little
// Sister's double (dark, olive, plaited, barefoot, in a long tunic, a dish on her hip).
const MARIAM_SKIN = ramp("#f0c8a2", "#d8a67e", "#a8765a", "#704c38");
const MARIAM_HAIR = ramp("#5c463a", "#3a2a22", "#271c16", "#150e0b");
const SAGE = ramp("#d8e6c4", "#b2c69c", "#849872", "#5a6a4c");           // her tunic: plain, a pale green
const MARIAM_DIM = { ...CHILD, headR: [0.075, 0.085, 0.081], neckY: 0.794, shoulderY: 0.764, waistY: 0.568, hipY: 0.466, shoulderW: 0.086, trunkTop: [0.090, 0.060], trunkLow: [0.080, 0.058],
  pelvisR: [0.088, 0.058, 0.068], thigh: 0.216, shin: 0.206, legR: [0.044, 0.030, 0.021], armR: [0.024, 0.020, 0.015], handR: 0.020, neckR: 0.86 };
/** Her plait, brought forward over her right shoulder: the braid's plies, a red tie near the end, and the tuft below it. */
function plait(c) {
  const { J, hp, limb, ball, d, parts } = c, T = (x, y, z) => add(J.sh, J.torso([x, y, z]));
  const pts = [hp(0.42, -0.30, -0.72), T(0.058, 0.020, -0.008), T(0.056, -0.040, d.trunkTop[1] * 0.86), T(0.050, -0.110, d.trunkTop[1] + 0.010)];
  const ply = shifted(MARIAM_HAIR, 1);
  for (let i = 0; i + 1 < pts.length; i++) limb(pts[i], pts[i + 1], 0.0150 - i * 0.0012, 0.0140 - i * 0.0012, MARIAM_HAIR, { part: parts.HAIR, bias: 2, fn: (t) => (Math.floor((i + t) * 4) % 2 ? ply : undefined) });
  const end = pts[pts.length - 1];
  ball(end, [0.0110, 0.0080, 0.0100], MADDER, { part: parts.HAIR, bias: 3 });
  ball(add(end, [0, -0.018, 0.002]), [0.0115, 0.0140, 0.0100], MARIAM_HAIR, { part: parts.HAIR, bias: 2 });
}
/** The dish of grain on her left hip: shallow clay, heaped; scattering, a little flies from her hand. */
function grainDish(c) {
  const { ball, J, pose } = c, g = J.L.palm, axis = [J.hipC[0], g[1], J.hipC[2]], inward = norm([axis[0] - g[0], 0, axis[2] - g[2]]), r0 = 0.066;
  const at = [g[0] + inward[0] * r0 * 0.90, g[1] - 0.016, g[2] + inward[2] * r0 * 0.90];
  ball(add(at, [0, 0.016, 0]), [r0 * 0.84, 0.016, r0 * 0.84], GRAIN, { ...held(c), fn: (ux, uy) => (cell(Math.floor(ux * 6 + 40), Math.floor(uy * 4 + 40)) % 5 === 0 ? shifted(GRAIN, 1) : undefined) });
  ball(at, [r0, 0.022, r0], CLAY, { ...held(c), fn: (ux, uy) => (uy < -0.10 ? null : undefined) });
  if (pose.fidget === "scatter" && pose.fu > 0.42 && pose.fu < 0.74) {
    const h = J.R.tip;
    for (let i = 0; i < 5; i++) ball(add(h, J.torso([((i * 3) % 5 - 2) * 0.014, -0.010 - (i % 3) * 0.016, 0.020 + i * 0.012])), [0.0055, 0.0055, 0.0055], GRAIN, held(c));
  }
}
export const mariam = {
  name: "Girl", height: 0.69,
  dim: MARIAM_DIM,
  skin: MARIAM_SKIN,
  hair: { mat: MARIAM_HAIR, bulk: [1.06, 1.05, 1.08], where: hairline({ front: 0.50, temple: 0.36, side: -0.24, back: -0.72, brow: 0.50, temples: 1.12 }),
          texture: (x, y, z) => (Math.abs(x) < 0.05 && y > 0.45 && z > 0.05 ? shifted(MARIAM_HAIR, 1) : undefined) },     // parted in the middle and drawn back smooth into the plait
  face: { eyes: "bright", eye: "#2a1a12", iris: BROWN_EYES, brows: MARIAM_HAIR.tones[2], blush: "#ec9a80", lip: "#b05a4c", eyeX: 0.43, eyeY: -0.08, mouthY: -0.64, jaw: 0.84, chin: 0.54, chinY: -0.52, chinZ: 0.44, nose: [0.6, 0.62, 0.72], smile: 1, mouthW: 0.22, ear: 1.1 },
  top: { mat: SAGE, sleeves: 0.58, cuff: 0.012 },
  bottom: { kind: "skirt", mat: SAGE, len: 1.78, flare: 1.14, folds: [[-0.7, 0.2], [0.75, 0.3], [0.1, 0.6], [2.6, 0.2]] },
  shoes: { kind: "bare" },
  hold: { L: { hand: [-0.150, -0.214, 0.112], bend: [-1, -0.3, -0.75], grip: true } },          // her left arm round the dish on her hip
  hand: "R",
  walk: { swing: 0.50, arm: 0.56, lean: 0.07, lift: 1.20, bob: 0.03 },
  pace: 168,
  gestures: [10, 11, 0, 8],                             // pointing (at a hen); a finger in the air (she is certain); a nod; an open hand
  pray: { high: 0.80, bow: 0.22 },
  fidgets: { stand: ["scatter", "hips", "hens", "crouch"] },     // scatters grain nobody eats; her hand on her hip; counts the hens; crouches to look one in the eye
  holds: { crouch: (o) => crouchPose(o) },              // (crouched through whatever is said: figure.hold(true, "crouch"))
  extras(c) { plait(c); grainDish(c); },
};

// ---------- Felix: Gaius Fannius Felix, Phyllis's son, about twenty-six, a boatman, his name down for Corinth ----------
// Strong, sunburnt, short hair, a short work tunic tied at one shoulder (the right shoulder and arm bare), bare legs, bare
// feet, a coil of rope over his right shoulder. `felix` carries a bale on his left shoulder, steadied with his left hand (he
// works between the landing and the barge); `felix-free` has set it down, his hands free to talk and to take the lamp.
// Cheerful, impatient, soft about his mother, full of Corinth.
const SUNBURNT = ramp("#f4ba94", "#dc946e", "#ac684c", "#724234");
const FELIX_HAIR = ramp("#7c5c46", "#54392a", "#37261b", "#21160f");
const EXOMIS = ramp("#e8d8ba", "#cab692", "#9a8664", "#6a5a40");         // his work tunic: undyed, and well worn
const BALE = ramp("#f0deb6", "#d6bc8a", "#a48c5e", "#6e5e3e");
/** The knot on his left shoulder, where his work tunic is tied (the tunic itself is his `top`, with the rig's `bare`). */
function shoulderKnot(c) {
  const { J, ball, d, cloth, parts } = c;
  ball(add(J.sh, J.torso([-(d.shoulderW - 0.020), 0.020, 0.018])), [0.013, 0.012, 0.012], shifted(EXOMIS, 1), { part: parts.DRAPE, bias: cloth * 2 });
}
/** A coil of rope hung on his right shoulder, down to his hip at that side (as the hauler's on his left). */
function ropeCoil(c) {
  const { J, limb, d, cloth, under, parts } = c, T = (x, y, z) => add(J.sh, J.torso([x, y, z])), back = d.trunkTop[1];
  const lie = { [parts.TORSO]: under, [parts.SKIRT]: under, [parts.BELT]: under, [parts.ARM.R]: under };
  for (const [dx, r, m] of [[0, 0.011, ROPE], [-0.013, 0.009, shifted(ROPE, 1)], [0.012, 0.009, shifted(ROPE, 1)]]) {
    const loop = [T(0.080 + dx, 0.024, 0), T(0.066 + dx, -0.040, back * 0.80), T(0.060 + dx, -0.150, back + 0.014), T(0.070 + dx, -0.250, back * 0.60), T(0.084 + dx, -0.290, 0),
                  T(0.070 + dx, -0.250, -back * 0.60), T(0.060 + dx, -0.150, -(back + 0.014)), T(0.066 + dx, -0.040, -back * 0.80), T(0.080 + dx, 0.024, 0)];
    for (let i = 0; i + 1 < loop.length; i++) limb(loop[i], loop[i + 1], r, r, m, { part: parts.EXTRA, over: lie, bias: cloth * 2 });
  }
}
/** The bale on his left shoulder: a long bundle wrapped in sacking and corded round, lying fore and aft. */
function bale(c) {
  const { J, ball, own, tw } = c, at = add(J.L.shoulder, J.torso([0.004, 0.086, -0.034]));
  ball(at, [0.078, 0.066, 0.150], BALE, { ...held(c), fn: (ux, uy, uz) => { const z = own(ux, uy, uz, tw + 0.40)[2]; return Math.abs(z) < 0.09 || Math.abs(Math.abs(z) - 0.58) < 0.08 ? shifted(ROPE, 1) : undefined; } }, tw + 0.40);      // (turned a little across him)
}
const felixBase = {
  name: "Boatman", height: 1.03,
  dim: { ...ADULT, shoulderW: 0.110, trunkTop: [0.114, 0.072], trunkLow: [0.088, 0.064], pelvisR: [0.092, 0.062, 0.072], armR: [0.035, 0.029, 0.020], legR: [0.054, 0.035, 0.023], handR: 0.024, neckR: 1.10 },
  build: "strong",
  skin: SUNBURNT,
  hair: { mat: FELIX_HAIR, bulk: 1.03, where: hairline({ front: 0.66, temple: 0.56, side: 0.20, back: -0.36 }) },       // cut short
  face: { eyes: "plain", eye: "#2a1a12", iris: BROWN_EYES, brows: FELIX_HAIR.tones[2], blush: "#e48a6a", jaw: 0.94, chin: 0.56, nose: [1.0, 1.05, 1.0], noseShade: true, lip: "#9a4a3c", smile: 1, mouthW: 0.24 },
  top: { mat: EXOMIS, sleeves: 0, bare: "R", belt: shifted(ROPE, 1) },         // tied on the left shoulder: the right shoulder and arm bare
  bottom: { kind: "skirt", mat: EXOMIS, len: 0.62, flare: 1.08, folds: [[-0.7, 0.2], [0.8, 0.3], [0.1, 0.5]] },
  shoes: { kind: "bare" },
  walk: { swing: 0.48, arm: 0.44, lean: 0.06, bob: 0.02 },
  pace: 175,
  gestures: [8, 9, 1, 19],                              // an open hand; his hands going (Corinth!); making a point; a thumb over his shoulder, at the barge
  fidgets: { stand: ["roll", "whistle", "peer"] },      // rolls his shoulders; whistles (no tune is heard); shades his eyes toward the bridge
};
export const felix = {
  ...felixBase,
  hold: { L: { hand: [-0.176, 0.050, 0.030], bend: [-1, -0.5, 0.0], curl: 0.8, point: [0.55, 0.55, 0.30] } },       // his hand up over its side, steadying it
  extras(c) { shoulderKnot(c); ropeCoil(c); bale(c); },
};
export const felixFree = {
  ...felixBase, name: "Boatman, the bale set down", stance: "hip",
  extras(c) { shoulderKnot(c); ropeCoil(c); },
};

// ---------- their holds ----------
/** Eleazar's blessing: his right hand laid flat on the crown of the boy standing facing him at BLESS_STEP, the boy's head
    bowed in his own prayer; leaning a little toward him, looking down at him. The wrist is in the space of his shoulders
    (as SHADE_HANDS is), solved with the rig by tools/bless-hand.mjs in S/work-rome-people, which draws the Son there. */
export const BLESS_HAND = { hand: [0.020, 0.018, 0.182], point: [0.10, -0.30, 0.95], bend: [0.7, -0.6, -0.3] };      // (for the boy upright, [0.020, 0.022, 0.217])
function blessPose(o) {
  const b = o.base, p = withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.05, head: { nod: nodOf(b) + 0.16 } }, "R", { hand: BLESS_HAND.hand, bend: BLESS_HAND.bend, flat: true, point: BLESS_HAND.point, thumb: [-0.6, 0.2, 0.5] });
  return p;
}
/** Mariam crouched down, to look a hen in the eye: her knees right down, her free hand on her knee, her head up and forward. */
function crouchPose(o) {
  const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.32, lap: true, head: { nod: nodOf(b) - 0.18 } };
  for (const s of ["R", "L"]) p[s] = { ...p[s], leg: [1.32, 0.24], knee: 2.30, foot: 0, footYaw: 0.30 };
  if (!o.held("R")) withArm(p, "R", { hand: [0.084, -0.330, 0.196], bend: [1, -0.3, -0.4], curl: 0.6 });
  return p;
}

// ---------- their own small movements (figure.fidget(name); each person's `fidgets` says which are theirs for their life) ----------
// Each is a few key poses made from the person's resting pose, at points from 0 to 1 of its time, the first and the last
// the resting pose itself, as the rig's own are (FIDGETS in rig.js: `ms`, `hold` for one that can be held, `make(o)`).
/** The free hand: the one a movement uses (the other may be carrying something). */
const freeOf = (o) => (o.held(o.H) ? o.O : o.H);
/** Where a hand lies flat across the brow, shading the eyes (as shadePose finds it), for a pose `p` whose head is turned as it will be. */
function browHand(o, p, s) {
  const sd = s === "R" ? 1 : -1, J = skeleton(o.d, p), hr = o.d.headR, cpi = Math.cos(J.headPitch), spi = Math.sin(J.headPitch);
  const headDir = (v) => turn([v[0], v[1] * cpi - v[2] * spi, v[1] * spi + v[2] * cpi], J.headYaw), toT = torsoOf(J);
  return { hand: toT(add(J.head, headDir([sd * hr[0] * 1.02, hr[1] * 0.66, hr[2] * 0.78]))), bend: [sd, -0.25, 0.35], flat: true, point: dirIn(toT, J, headDir([-sd * 0.80, 0.02, 0.60])), thumb: dirIn(toT, J, headDir([0, -1, 0])) };
}
addMoves({
  // ---- the Gaul ----
  /** the Gaul (`gaul`): tugs the short toga down at his thigh with his free hand, twice, looking down at it */
  tug: { ms: 1900, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    if (o.held(s)) return [[0, b], [1, b]];
    const at = (dy) => withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.10, sway: sd * 0.010, head: { nod: nodOf(b) + 0.24, turn: sd * 0.10 } }, s, { hand: [sd * (o.d.shoulderW + 0.012), o.sp.hip - 0.020 + dy, 0.052], bend: [sd, -0.2, -0.3], grip: true });
    const t1 = at(0), t2 = at(-0.030);
    return [[0, b], [0.22, t1], [0.38, t2], [0.54, t1], [0.70, t2], [1, b]];
  } },
  /** the Gaul: looks up at the crane (or anything tall) a long while, his mouth a little open (holdable) */
  crane: { ms: 2600, hold: 0.5, make(o) {
    const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.03, mouth: 1, head: { nod: nodOf(b) - 0.34, turn: 0.18 } };
    return [[0, b], [0.28, p], [0.78, p], [1, b]];
  } },
  /** the Gaul: asks the air a question, his free hand open and lifted to it, and shrugs */
  ask: { ms: 2800, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1, sp = o.sp;
    if (o.held(s)) return [[0, b], [1, b]];
    const asking = (m, up) => withArm({ ...cloneP(b), mouth: m, head: { nod: nodOf(b) - 0.16, turn: sd * 0.20 } }, s, { hand: [sd * 0.150, -0.120 + up, sp.chest + 0.120], bend: [sd, -0.6, -0.3], flat: true, point: [sd * 0.4, 0.5, 0.75], thumb: [sd, 0, 0] });
    const shrug = { ...cloneP(b), breath: 1, head: { nod: nodOf(b) - 0.02, turn: -sd * 0.12 } };
    for (const k of free(o)) withArm(shrug, k, { arm: [0.12, 0.24], elbow: 1.0, flat: true });
    return [[0, b], [0.22, asking(1, 0)], [0.40, asking(2, 0.025)], [0.58, shrug], [0.80, shrug], [1, b]];
  } },
  /** the Gaul: bows, deep and formal, from the hips, his free hand to his heart (holdable) */
  bow: { ms: 2400, hold: 0.5, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1, p = { ...cloneP(b), lean: (b.lean || 0) + 0.46, head: { nod: nodOf(b) + 0.22 } };
    if (!o.held(s)) withArm(p, s, { hand: [-sd * 0.030, -0.085, o.sp.chest + 0.030], bend: [sd, -0.6, 0], flat: true });
    return [[0, b], [0.34, p], [0.70, p], [1, b]];
  } },
  /** the Gaul: points ahead with his free arm, at what he is facing (the hole where the House was), his head with it (holdable) */
  point: { ms: 2200, hold: 0.5, make(o) {
    const b = o.base, s = freeOf(o);
    if (o.held(s)) return [[0, b], [1, b]];
    const p = withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.03, head: { nod: nodOf(b) + 0.02 } }, s, { arm: [1.05, 0.12], elbow: 0.22, finger: true });
    return [[0, b], [0.30, p], [0.76, p], [1, b]];
  } },
  // ---- Phyllis (and Felix: `peer` is his too) ----
  /** Phyllis, sitting: works a stem into the garland in her hands, her head bent to it */
  weave: { ms: 2600, make(o) {
    const b = o.base, sp = o.sp, at = (dx) => {
      const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.20, turn: -0.06 } };
      withArm(p, "L", { hand: [-0.050, -0.190, sp.chest + 0.110], bend: [-1, -0.5, -0.3], curl: 0.8 });
      return withArm(p, "R", { hand: [0.030 + dx, -0.175, sp.chest + 0.130], bend: [1, -0.5, -0.3], grip: true, point: [-0.7, 0.2, 0.5] });
    };
    const w1 = at(0.030), w2 = at(-0.006);
    return [[0, b], [0.20, w1], [0.36, w2], [0.52, w1], [0.68, w2], [1, b]];
  } },
  /** Phyllis: a violet to her nose, her eyes shut */
  sniff: { ms: 2200, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1, hr = o.d.headR;
    const p = withArm({ ...cloneP(b), blink: true, head: { nod: nodOf(b) + 0.06, turn: sd * 0.06 } }, s, { hand: [sd * 0.016, o.sp.chinY - 0.016, hr[2] + 0.052], bend: [sd, -0.6, 0.1], grip: true, point: [-sd * 0.3, 0.8, 0.5] });
    return [[0, b], [0.30, p], [0.70, p], [1, b]];
  } },
  /** Phyllis: counts the coins in her palm, a finger going over them */
  count: { ms: 2600, make(o) {
    const b = o.base, sp = o.sp, at = (dx) => {
      const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.22 } };
      withArm(p, "L", { hand: [-0.020, sp.waist + 0.040, sp.belly + 0.110], bend: [-1, -0.5, -0.2], flat: true, thumb: [-1, 0, 0], point: [0.3, -0.1, 0.95] });
      return withArm(p, "R", { hand: [0.024 + dx, sp.waist + 0.070, sp.belly + 0.120], bend: [1, -0.4, -0.2], finger: true, point: [-0.5, -0.6, 0.4] });
    };
    return [[0, b], [0.20, at(0)], [0.36, at(-0.014)], [0.52, at(-0.028)], [0.68, at(-0.014)], [1, b]];
  } },
  /** Phyllis, and Felix: a hand flat to the brow, looking a long way off across the square or up the river (holdable) */
  peer: { ms: 2800, hold: 0.5, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    if (o.held(s)) return [[0, b], [1, b]];
    const p = { ...cloneP(b), head: { nod: nodOf(b) - 0.08, turn: sd * 0.26 } };
    withArm(p, s, browHand(o, p, s));
    return [[0, b], [0.26, p], [0.78, p], [1, b]];
  } },
  /** Phyllis, sitting: unwraps the lamp from her lap and holds it out in both hands (holdable: until the boy takes it) */
  offer: { ms: 1500, hold: 0.62, make(o) {
    const b = o.base, sp = o.sp, p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) + 0.06 } };
    withArm(p, "R", { hand: [0.034, -0.150, sp.chest + 0.215], bend: [1, -0.5, -0.4], curl: 0.6, point: [-0.5, 0.1, 0.85] });
    withArm(p, "L", { hand: [-0.034, -0.150, sp.chest + 0.215], bend: [-1, -0.5, -0.4], curl: 0.6, point: [0.5, 0.1, 0.85] });
    return [[0, b], [0.40, p], [0.90, p], [1, b]];
  } },
  /** Phyllis, on her feet: hangs a garland on her pole, her hands up (one that holds something keeps it) */
  hang: { ms: 2400, make(o) {
    const b = o.base, sp = o.sp, up = (dy) => {
      const p = { ...cloneP(b), breath: 1, lean: (b.lean || 0) - 0.04, head: { nod: nodOf(b) - 0.22 } };
      for (const s of free(o)) { const sd = s === "R" ? 1 : -1; withArm(p, s, { hand: [sd * 0.060, sp.headY + 0.040 + dy, 0.140], bend: [sd, -0.3, -0.4], grip: true }); }
      return p;
    };
    return [[0, b], [0.30, up(0)], [0.50, up(-0.020)], [0.66, up(0)], [1, b]];
  } },
  /** Phyllis, on her feet: shoos a pigeon off her baskets with the back of her free hand, twice */
  shoo: { ms: 1600, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    if (o.held(s)) return [[0, b], [1, b]];
    const at = (a) => withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) + 0.16, turn: sd * 0.20 } }, s, { arm: [0.60, 0.30], fore: [sd * (0.20 + a), -0.40, 0.85], flat: true });
    return [[0, b], [0.20, at(0.30)], [0.36, at(-0.10)], [0.52, at(0.30)], [0.68, at(-0.10)], [1, b]];
  } },
  /** Phyllis, on her feet: calls to the square, her free hand by her mouth (holdable) */
  call: { ms: 2200, hold: 0.5, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1, hr = o.d.headR;
    if (o.held(s)) return [[0, b], [1, b]];
    const p = withArm({ ...cloneP(b), mouth: 2, breath: 1, head: { nod: nodOf(b) - 0.12, turn: -sd * 0.18 } }, s, { hand: [sd * (hr[0] + 0.012), o.sp.chinY - 0.004, hr[2] * 0.60], bend: [sd, -0.7, 0.3], flat: true, point: [0, 1, 0.3] });
    return [[0, b], [0.26, p], [0.76, p], [1, b]];
  } },
  // ---- Titus, on his base ----
  /** Titus: waves at the boy, his whole arm going */
  wave: { ms: 1800, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    const at = (w) => withArm({ ...cloneP(b), mouth: 1, head: { nod: nodOf(b) - 0.04, turn: sd * 0.06 } }, s, { arm: [1.70, 0.55], elbow: 0, tuck: 0, fore: [sd * (0.20 + w), 0.96, 0.10], flat: true });
    const w1 = at(0.30), w2 = at(-0.25);
    return [[0, b], [0.20, w1], [0.35, w2], [0.50, w1], [0.65, w2], [0.80, w1], [1, b]];
  } },
  /** Titus: peeks into the cloth in his lap, lifting its knot (and there is the loaf) */
  peek: { ms: 2400, make(o) {
    const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.24, head: { nod: nodOf(b) + 0.30 } }, J = skeleton(o.d, p), toT = torsoOf(J), lap = lapOf(J, 0.42, 0.040);
    const at = (dy) => { const q = cloneP(p); withArm(q, "R", { hand: toT(add(lap, [0.006, 0.050 + dy, -0.006])), bend: [1, -0.3, -0.4], grip: true }); return withArm(q, "L", { hand: toT(add(lap, [-0.036, 0.006, -0.024])), bend: [-1, -0.4, -0.4], curl: 0.8 }); };
    return [[0, b], [0.28, at(0)], [0.46, at(0.024)], [0.66, at(0.024)], [1, b]];
  } },
  /** Titus: pretends to be a statue, an arm raised as the kings' statues raise theirs, chin up, quite still (holdable) */
  statue: { ms: 4200, hold: 0.5, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    const p = withArm({ ...cloneP(b), breath: 1, lean: (b.lean || 0) - 0.06, head: { nod: nodOf(b) - 0.14, turn: sd * 0.20 } }, s, { arm: [1.55, 0.32], elbow: 0.25, flat: true, point: [sd * 0.15, 0.55, 0.85], thumb: [0, 1, 0] });
    return [[0, b], [0.16, p], [0.84, p], [1, b]];
  } },
  /** Titus: draws his feet up out of reach, as if a goose had looked at him, the bundle clutched to him; and lets them down
      again (a scene calls it: the hook `feet`) */
  feet: { ms: 1700, hold: 0.40, make(o) {
    const b = o.base, sp = o.sp;
    const legs = (pitch, shin, lean, nod) => {
      const p = { ...cloneP(b), lean: (b.lean || 0) + lean, mouth: 1, head: { nod: nodOf(b) + nod } };
      for (const s of ["R", "L"]) { const sd = s === "R" ? 1 : -1; p[s] = { ...p[s], leg: [pitch, 0.14], shin: [sd * 0.06, shin[0], shin[1]] }; }
      withArm(p, "L", { hand: [-0.012, -0.150, sp.chest + 0.060], bend: [-0.55, -0.60, -0.25], grip: true });
      return withArm(p, "R", { hand: [0.030, -0.215, sp.chest + 0.120], bend: [1, -0.5, -0.3], curl: 0.8 });
    };
    const mid = legs(1.75, [-0.92, -0.38], -0.02, 0.14), up = legs(2.15, [-0.66, -0.75], -0.06, 0.18);
    return [[0, b], [0.08, mid], [0.16, up], [0.64, up], [0.80, mid], [1, b]];
  } },
  // ---- the goose-keeper ----
  /** the goose-keeper: shakes the basket on his hip, three quick shakes, and a little grain jumps */
  shake: { ms: 1500, make(o) {
    const b = o.base, s = o.held("L") ? "L" : o.O, q = b[s];
    if (!q || !q.hand) return [[0, b], [1, b]];
    const at = (dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.10, turn: -0.22 } }, s, { ...q, hand: add(q.hand, [0.006, dy, 0.012]) });
    const u = at(0.034), d0 = at(-0.004);
    return [[0, b], [0.14, u], [0.26, d0], [0.38, u], [0.50, d0], [0.62, u], [0.74, d0], [1, b]];
  } },
  /** the goose-keeper: leans his weight on his stick, his head down (holdable) */
  stick: { ms: 3400, hold: 0.5, make(o) {
    const b = o.base, q = b.R || {}, p = withArm({ ...cloneP(b), sway: 0.018, hipTwist: -0.05, lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.12, turn: -0.10 } }, "R", { ...q, hand: [0.150, -0.070, 0.120], bend: [0.6, -1, -0.3] });
    p.L = { ...p.L, leg: [0.14, 0.06], knee: 0.26 };
    return [[0, b], [0.30, p], [0.76, p], [1, b]];
  } },
  /** the goose-keeper: counts his geese, his head going from one to the next, his lips moving, a finger off the stick at each */
  tally: { ms: 3200, make(o) {
    const b = o.base, step = (turn, m, fing) => { const p = { ...cloneP(b), mouth: m, head: { nod: nodOf(b) + 0.10, turn } }; if (b.R && b.R.hand) p.R = { ...p.R, finger: fing, grip: !fing }; return p; };
    return [[0, b], [0.14, step(0.50, 1, true)], [0.28, step(0.50, 0, false)], [0.42, step(0.22, 1, true)], [0.56, step(0.22, 0, false)], [0.70, step(-0.06, 1, true)], [0.84, step(-0.06, 0, false)], [1, b]];
  } },
  /** the goose-keeper: a long sigh: the shoulders up, and down further than they started */
  sigh: { ms: 2600, make(o) {
    const b = o.base, inn = { ...cloneP(b), breath: 1, lean: (b.lean || 0) - 0.03, head: { nod: nodOf(b) - 0.10 } }, out = { ...cloneP(b), breath: 0, lean: (b.lean || 0) + 0.06, mouth: 1, head: { nod: nodOf(b) + 0.18 } };
    return [[0, b], [0.34, inn], [0.50, inn], [0.76, out], [1, b]];
  } },
  // ---- Eleazar ----
  /** Eleazar at his window: lifts his head a while, his lips moving, and bows it again */
  lift: { ms: 3000, make(o) {
    const b = o.base, up = (m) => ({ ...cloneP(b), mouth: m, head: { nod: nodOf(b) - 0.42 } });
    return [[0, b], [0.24, up(1)], [0.40, up(0)], [0.56, up(2)], [0.72, up(1)], [1, b]];
  } },
  /** Eleazar at his window: his head still bowed, his lips moving (no words are heard) */
  murmur: { ms: 2400, make(o) {
    const b = o.base, m = (k) => ({ ...cloneP(b), mouth: k, head: { nod: nodOf(b) + 0.03 } });
    return [[0, b], [0.16, m(1)], [0.32, m(0)], [0.48, m(1)], [0.64, m(2)], [0.80, m(1)], [1, b]];
  } },
  /** Eleazar on his bench: unrolls his scroll a little, his hands drawing apart, and bends to it */
  unroll: { ms: 3000, make(o) {
    const b = o.base, lap = lapOf(o.J, 0.52, 0.090), toT = o.toTorso;
    const at = (w, nod) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + nod } }; withArm(p, "R", { ...b.R, hand: toT(add(lap, [w, 0.010, -0.026])) }); return withArm(p, "L", { ...b.L, hand: toT(add(lap, [-w, 0.010, -0.026])) }); };
    return [[0, b], [0.34, at(0.072, 0.16)], [0.70, at(0.072, 0.22)], [1, b]];
  } },
  /** Eleazar on his bench: reads, a finger of his right hand following the lines down the sheet, his head following it */
  read: { ms: 3200, make(o) {
    const b = o.base, lap = lapOf(o.J, 0.52, 0.090), toT = o.toTorso;
    const at = (dy, turn) => { const p = { ...cloneP(b), mouth: 0, head: { nod: nodOf(b) + 0.20 + dy * 1.5, turn } }; return withArm(p, "R", { ...b.R, hand: toT(add(lap, [0.026, 0.020 + dy, -0.018])), grip: false, finger: true, point: [-0.6, -0.5, 0.6] }); };
    return [[0, b], [0.18, at(0.010, 0.06)], [0.38, at(-0.006, 0.02)], [0.58, at(-0.020, -0.02)], [0.78, at(-0.032, -0.05)], [1, b]];
  } },
  /** Eleazar on his bench: rests his hands on the scroll in his lap and is still a while, his eyes closed (holdable) */
  still: { ms: 4000, hold: 0.5, make(o) {
    const b = o.base, p = { ...cloneP(b), breath: 0.2, blink: true, lean: (b.lean || 0) + 0.02, head: { nod: nodOf(b) + 0.16 } };
    for (const s of ["R", "L"]) if (p[s].hand) p[s] = { ...p[s], hand: add(p[s].hand, [0, -0.018, -0.010]), curl: 0.5, grip: false };
    return [[0, b], [0.24, p], [0.80, p], [1, b]];
  } },
  // ---- Mariam ----
  /** Mariam: takes a pinch of grain from the dish on her hip and throws it to the hens, who will not eat it */
  scatter: { ms: 1900, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    if (o.held(s)) return [[0, b], [1, b]];
    const dip = withArm({ ...cloneP(b), twist: -sd * 0.10, head: { nod: nodOf(b) + 0.16, turn: -sd * 0.20 } }, s, { hand: [-sd * 0.080, -0.215, 0.100], bend: [sd, -0.5, -0.3], grip: true });
    const fling = (a) => withArm({ ...cloneP(b), twist: sd * 0.08, lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.14 } }, s, { arm: [0.95 + a, 0.25], elbow: 0.15, flat: true, point: [sd * 0.3, -0.3, 0.9] });
    return [[0, b], [0.24, dip], [0.44, fling(0)], [0.60, fling(0.15)], [1, b]];
  } },
  /** Mariam: her free fist on her hip, her chin up: certain (holdable) */
  hips: { ms: 2600, hold: 0.5, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    if (o.held(s)) return [[0, b], [1, b]];
    const p = withArm({ ...cloneP(b), lean: (b.lean || 0) - 0.03, head: { nod: nodOf(b) - 0.08, turn: sd * 0.12 } }, s, { hand: [sd * (o.sp.side + 0.012), o.sp.hip + 0.085, 0.012], bend: [sd, 0, -0.55], grip: true });
    return [[0, b], [0.24, p], [0.78, p], [1, b]];
  } },
  /** Mariam: counts the hens, pointing at each in turn, her lips moving */
  hens: { ms: 3200, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    if (o.held(s)) return [[0, b], [1, b]];
    const at = (x, m) => withArm({ ...cloneP(b), mouth: m, head: { nod: nodOf(b) + 0.10, turn: x * 0.6 } }, s, { arm: [0.75, 0.10], elbow: 0.20, fore: [x, -0.30, 0.90], finger: true });
    return [[0, b], [0.16, at(sd * 0.40, 1)], [0.32, at(sd * 0.20, 0)], [0.48, at(0, 1)], [0.64, at(-sd * 0.20, 0)], [0.80, at(-sd * 0.36, 1)], [1, b]];
  } },
  /** Mariam: crouches to look a hen in the eye, a while, and up again (holdable; figure.hold(true, "crouch") keeps her down through what is said) */
  crouch: { ms: 2600, hold: 0.5, make(o) {
    const b = o.base, c = crouchPose(o);
    return [[0, b], [0.30, c], [0.72, c], [1, b]];
  } },
  // ---- Felix ----
  /** Felix: whistles to himself (his lips only: no tune is heard), his head keeping time */
  whistle: { ms: 2400, make(o) {
    const b = o.base, at = (k) => ({ ...cloneP(b), mouth: 1, head: { nod: nodOf(b) - 0.06 + k, turn: 0.10 } });
    return [[0, b], [0.16, at(0.05)], [0.30, at(-0.03)], [0.44, at(0.05)], [0.58, at(-0.03)], [0.72, at(0.05)], [1, b]];
  } },
});

// =====================================================================================
// OFFICE-17P (round seventeen): Opal of Property & Effects, and the poses the Office's stage one needs
// =====================================================================================
// Who they are and what they do: briefs/out/office-hq-design.md (sections 3 and 4: #16 to #20 and the two cut-scenes).
// Opal is a person of our own: nobody's likeness. Everyone else here is someone the game has already (the backup, Jed,
// Grandpa Joe) at another moment: a scene swaps one for the other under the same id, as `guard-shade` is the guard.
//
// How a script calls each pose (docs/DESIGN.md section 4, "The Office's people"):
//   - a state is a kind of its own, swapped in under the same id (a scene's `redraw`, as backup.js swaps Grandpa Joe for
//     `grandpajoe-broken`): Opal with the banjo, Wendell with his button or his fingers in his ears, Grandpa Joe on the chair;
//   - a movement is a small movement, `g.actor(id).fidget("thunk")` (ends by itself; at once if they talk or walk);
//   - a pose kept through whatever is said is one of their holds, `g.actor(id).hold(true, "up")`, until `hold(false)`
//     (ease it in with a tween on `act.k`, as rome-tiber.js eases the blessing; held, the lips move when they talk);
//   - getting up from the table, the couch or the stool is `figure.sit(false)`, as for anyone found sitting.

/** The seats the Office's rooms paint, in the rig's measure (CM): the top of the seat over the floor under the sitter's
    hips. These are the usual heights; when the painters' reports are in (S/work-17-paintC and S/work-17-paintD:
    ready.md and layout.json), set each from theirs, as LIMO_SEAT was set from PAINT-12C's. */
export const OFFICE_CHAIR_SEAT = 46 * CM;      // the Comfortable Room's chairs: Dale, Merle and Grandpa Joe at the table, and the corner chair he stands on
export const OFFICE_TABLE_TOP = 74 * CM;       // its table: where their hands lie
export const OPAL_STOOL_SEAT = 66 * CM;        // Opal's stool at her window, a counter stool: her feet hang (she hops down) (SCENES-17: 66 cm, as PAINT-17C painted it)
export const COUCH_SEAT = 45.9 * CM;           // the break room's couch, sunk under Floyd (SCENES-17: 45.9 cm, as PAINT-17D painted its cushions)
export const BREAK_CHAIR_SEAT = 45.9 * CM;     // the break room's plastic chair, Jed's (SCENES-17: 45.9 cm, as PAINT-17D painted it)
/** How far in front of the hips of someone seated at the table its near edge is, in their own heights (for the painter
    and the scene: put a seated suit or Grandpa Joe that far behind the edge, and his hands lie on the top). */
export const TABLE_EDGE = 0.13;

// ---------- things they carry, and small things they wear ----------
const POT_INSIDE = ramp("#a07c5a", "#6c5038", "#4a3626", "#2c2018");      // the inside of the banjo's pot, where its head was
const TIN = ramp("#ffffff", "#e6eaf0", "#b2b9c4", "#767d88", { shine: true });       // a pie tin, washed: it shines
const SLACK_STRING = ramp("#e8e4da", "#d6d0c2", "#b8b2a2", "#9a9484");
const INK_STRING_TIN = pack("#8a8f98");
/** The broken head of the banjo: the dark inside of the pot, the wood of the rim inside it, and tatters of the old head
    round the edge where they caught. (A poly's fn: the pixel, and how far from the middle it is.) */
function brokenHead(ctr, rpx, lit) {
  return (x, y) => {
    const dx = x + 0.5 - ctr[0], dy = y + 0.5 - ctr[1], q = Math.hypot(dx, dy) / Math.max(1, rpx), a = Math.atan2(dy, dx);
    const tatter = 0.70 + 0.16 * Math.abs(Math.sin(a * 3.5 + 0.7)) + 0.08 * Math.sin(a * 9.0);
    if (q > tatter && Math.sin(a * 5.0 + 1.1) > -0.35) return BANJO_HEAD;                // the old head, torn: white jags round the edge
    if (q > 0.80) return lit(x, y) > rpx * 0.20 ? 2 : 1;                                  // the wood of the rim, inside
    return lit(x, y) < -rpx * 0.45 ? 1 : 2;                                               // the hole: dark, a little light at the far side
  };
}
/** The pie tin for a head: bright tin, its crimped rim all round (light and dark in turn), and a shine across it. */
function tinHead(ctr, rpx, lit) {
  return (x, y) => {
    const dx = x + 0.5 - ctr[0], dy = y + 0.5 - ctr[1], q = Math.hypot(dx, dy) / Math.max(1, rpx), a = Math.atan2(dy, dx);
    if (q > 0.80) return Math.floor(((a + Math.PI) / (2 * Math.PI)) * 18) % 2 ? 0 : 2;   // the crimps
    if (q > 0.72) return 2;                                                                // the step down into the tin
    const shine = (dx - dy) / Math.max(1, rpx);
    if (Math.abs(shine + 0.18) < 0.13) return 0;                                           // a shine across it
    return lit(x, y) > rpx * 0.40 ? 2 : 1;
  };
}

/** A man in gray mopping his brow (`mop`): the handkerchief in the hand that does it, white, a corner hanging. */
const HANKIE = ramp("#ffffff", "#f4f6f8", "#c8ccd2", "#8c9098");
function hankie(cx) {
  const { pose, J, ball, limb, parts, seatOnly } = cx;
  if (seatOnly || pose.fidget !== "mop" || !(pose.fu > 0.10 && pose.fu < 0.90)) return;
  const s = pose.mopHand || "L", g = J[s].palm;
  ball(add(g, J.torso([0, 0.006, 0.004])), [0.020, 0.016, 0.014], HANKIE, { part: parts.HELD, bias: 1 });
  limb(add(g, J.torso([0, -0.004, 0.004])), add(g, J.torso([s === "R" ? 0.010 : -0.010, -0.040, 0.010])), 0.012, 0.006, HANKIE, { part: parts.HELD });
}
/** How far the tie is loosened at this moment of `loosen` (0 to 1): down, a while, and back up. */
function loosened(pose) {
  if (!pose || pose.fidget !== "loosen") return 0;
  const u = pose.fu || 0;
  return u < 0.22 ? 0 : u < 0.34 ? (u - 0.22) / 0.12 : u < 0.62 ? 1 : u < 0.76 ? 1 - (u - 0.62) / 0.14 : 0;
}
/** Sweat on the brow, in the heat: a bead at each temple that shows. */
const INK_SWEAT = pack("#e6f6ff");
function sweat(cx) {
  const { hp, seatOnly } = cx;
  if (seatOnly || cx.S < 84) return;
  for (const [x, y] of [[0.62, 0.52], [-0.58, 0.46], [0.30, 0.66]]) inkAt(cx, hp(x, y, Math.sqrt(Math.max(0, 1 - x * x - y * y * 0.6)) * 0.98), INK_SWEAT, 0.02);
}

// ---------- Opal: Property & Effects, at her window since 1971 ----------
// Small and round-shouldered, about 1.55 m; short silver curls; half-moon reading glasses on a beaded chain; a lavender
// cardigan over a white blouse with a round collar, a gray skirt, stockings, sensible brown shoes; a rubber thimble on her
// right thumb (a dot of pink). She moves briskly in small steps, looks at people over her glasses, and is never without
// her date stamp or her knitting: on her stool, her hands are knitting the long gray scarf (in the regulation color) that
// trails into her basket; on her feet, the stamp is in her right hand and her keys hang at her left hip.
const OPAL_SKIN = ramp("#fde6d6", "#f2cab2", "#cc9a86", "#906454");
const OPAL_SILVER = ramp("#ffffff", "#e3e6ed", "#b3b8c3", "#7f848e");     // silver: brighter than Grandma Jolene's, a little blue
const OPAL_CURL = shifted(OPAL_SILVER, 1);
const LAVENDER = ramp("#ecdff8", "#c4abe2", "#9178b6", "#605084");
const OPAL_BLOUSE = ramp("#ffffff", "#f6f4f2", "#d0ccc6", "#9a948c");
const OPAL_SKIRT = ramp("#c2c2c8", "#96969c", "#6e6e75", "#4a4a50");
const OPAL_HOSE = ramp("#f6dece", "#e4c2ac", "#b48e7a", "#7c5e50");
const OPAL_SHOES = ramp("#a07e6a", "#705442", "#4c382c", "#2e2219");
const STAMP_KNOB = ramp("#f4cc8c", "#d29e5a", "#a06e36", "#68461e");
const STAMP_BLOCK = ramp("#8a8290", "#544c5c", "#383240", "#201c26");
const NEEDLE = ramp("#ffffff", "#e6edf4", "#b2bdc8", "#78838f", { shine: true });
const SCARF = ramp("#c9cbce", "#9fa1a6", "#76797e", "#515358");          // the regulation gray
const RECEIPT_PAPER = ramp("#fffdf6", "#f4efe0", "#cfc7b2", "#958c76");
const INK_HALFMOON = pack("#c9a24c"), INK_BEAD_A = pack("#faf4ff"), INK_BEAD_B = pack("#c79ad8"), INK_THIMBLE = pack("#f28aa6");
const KEY_METAL = ramp("#ffffff", "#d8dde4", "#a2a9b4", "#666d78", { shine: true });
/** Short silver curls: little rings of shade all over, the crown too. */
const opalCurls = (x, y, z) => {
  const n = 7, a = Math.atan2(x, z) * n / Math.PI, b = (y + 1) * n * 1.1, i = Math.floor(a), j = Math.floor(b);
  const u = a - i - 0.5, v = b - j - 0.5 + ((i & 1) ? 0.5 : 0) % 1, r = Math.hypot(u, v - Math.round(v));
  return r > 0.26 && r < 0.44 && v - Math.round(v) > -0.12;
};
const OPAL_DIM = { ...WOMAN, headR: [0.057, 0.068, 0.064], shoulderW: 0.080, shoulderDrop: 0.052, trunkTop: [0.090, 0.068], trunkLow: [0.084, 0.066], bellyFwd: 0.010,
  pelvisR: [0.098, 0.064, 0.076], armR: [0.024, 0.021, 0.015], handR: 0.019, legR: [0.046, 0.030, 0.019], footR: 0.018, bust: [0.004, 0.030], neckR: 0.84 };
const OPAL_FACE = { eyes: "girl", eye: "#2a2230", iris: "#7d90ac", lid: "#5a4048", brows: OPAL_SILVER.tones[2], browUp: 2, blush: "#f29a9a", lip: "#c25a72", lips: "#dc8094", lines: 2,
  nose: [0.9, 0.9, 1.0], noseShade: true, jaw: 0.84, chin: 0.50, chinY: -0.84, smile: 1, mouthW: 0.20, ear: 1.0, big: { eyeW: 0.42, eyeH: 0.42, lashes: 1, arch: 0.28 } };
const opalBase = {
  name: "Opal", height: 0.886, lean: 0.035,                            // 1.55 m; round-shouldered, a little forward
  dim: OPAL_DIM,
  skin: OPAL_SKIN,
  hair: { mat: OPAL_SILVER, bulk: [1.17, 1.12, 1.17], lift: [0, 0.004, 0], ears: false,
          where: hairline({ front: 0.50, temple: 0.34, side: -0.14, back: -0.46, brow: 0.46, temples: 1.10 }),
          texture: (x, y, z) => (opalCurls(x, y, z) ? OPAL_CURL : undefined),
          puffs: [[0, 0.78, 0.16, 0.86, 0.36, 0.82]] },                  // set short in curls, a little high on top
  face: OPAL_FACE,
  top: { mat: LAVENDER, sleeves: 2, hem: 0.034, open: 0.050, under: OPAL_BLOUSE, band: OPAL_BLOUSE, cuffs: shifted(LAVENDER, 1), buttons: "#f6eefc" },      // the cardigan over the blouse, its round collar out over it
  bottom: { kind: "skirt", mat: OPAL_SKIRT, len: 1.30, flare: 1.10, folds: [[-0.7, 0.25], [0.75, 0.3], [0.05, 0.55], [2.6, 0.3], [-2.5, 0.3]] },
  tights: OPAL_HOSE,
  shoes: { kind: "shoes", mat: OPAL_SHOES, sole: shifted(OPAL_SHOES, 2) },
  stance: "clasped",                                                    // her hands together at her waist, the stamp in them
  walk: { swing: 0.30, arm: 0.22, elbow: 0.32, lean: 0.07, lift: 0.85, bob: 0.014, sway: 0.010, twist: 0.08 }, pace: 150,     // brisk, in small steps
  gestures: [23, 0, 22, 8],                                             // over her glasses; a nod; THUNK, the stamp onto her other palm; an open hand
  pray: { high: 0.45, bow: 0.28 },
  portrait: { head: 0.54, y: 0.44 },
};
/** Opal's half-moon reading glasses, low on her nose: a straight gold rim along the middle of each eye and the half-round
    lens under it, placed where the rig puts the eyes (as Grandma Jolene's are); a pixel lower when she looks over them
    (pose.over). And the beaded chain, from the arms of the glasses down behind her ears and round the back of her neck. */
function halfMoons(cx) {
  const { hp, P, sf, J, d, S, th, hy, parts, pose, spec, fine } = cx, hr = d.headR;
  const eyeX = spec.face.eyeX ?? 0.36, eyeY = spec.face.eyeY ?? 0.06, headPx = 2 * hr[0] * S, full = headPx >= 13.3, fineFace = headPx >= 10.0;
  const look = (v) => { const w = turn(v, hy); return w[0] * Math.sin(th) + w[2] * Math.cos(th); }, sideways = Math.sin(th + hy);
  const mid = P(hp(0, eyeY, 0.80))[0], low = pose.over ? 1 : 0, inner = [];
  for (const sd of [1, -1]) {
    const vis = look([sd * 0.25, 0, 0.97]);
    if (vis < 0.20) continue;
    const q = P(hp(sd * eyeX, eyeY, 0.80)), w = full && vis > 0.70 ? 2 : 1, right = Math.abs(sideways) > 0.86 ? sideways < 0 : q[0] > mid;
    const ex = right ? Math.round(q[0] - w / 2) : Math.round(q[0] + w / 2) - 1, ey = Math.round(q[1] - 0.5) + 1 + low, out = right ? 1 : -1;
    const put = (i, j) => sf.dot(ex + out * i, ey + j, INK_HALFMOON, parts.HEAD);
    if (!fineFace) { put(0, 0); continue; }
    for (let i = -1; i <= w; i++) put(i, 0);                            // the straight top of the rim, across the middle of the eye
    if (full) { for (let i = 0; i < w; i++) put(i, 1); put(-1, 1); put(w, 1); }      // and the half-round under it
    else put(0, 1);
    inner.push(ex - out, ey);
  }
  if (inner.length === 4 && Math.abs(inner[1] - inner[3]) <= 1) { const [x0, y0, x1] = inner, a = Math.min(x0, x1), b = Math.max(x0, x1); for (let x = a + 1; x < b; x++) sf.dot(x, y0, INK_HALFMOON, parts.HEAD); }      // the bridge, over the nose
  if (!fine) return;
  // the chain: beads, pale and lavender in turn, from each temple behind the ear and round the back of the neck
  const nape = add(J.spine(d.neckY - 0.010), J.torso([0, 0, -(d.trunkTop[1] * 0.62)]));
  for (const sd of [1, -1]) {
    const a = hp(sd * 1.00, eyeY - 0.04, 0.10), b = hp(sd * 0.98, -0.62, -0.36), c2 = add(J.sh, J.torso([sd * 0.052, 0.010, -(d.trunkTop[1] * 0.40)]));
    for (let i = 0; i <= 20; i++) {
      const t = i / 20, p = t < 0.45 ? mix(a, b, t / 0.45) : t < 0.78 ? mix(b, c2, (t - 0.45) / 0.33) : mix(c2, nape, (t - 0.78) / 0.22);
      inkAt(cx, p, i % 2 ? INK_BEAD_B : INK_BEAD_A, 0.016);
    }
  }
}
/** Her date stamp, in her right hand: a turned wooden knob in her fist and the inked block under it, on the side the hand points. */
function dateStamp(cx) {
  const { J, limb, ball, parts } = cx, A = J.R, d = A.hDir, held = { part: parts.HELD };
  ball(add(A.palm, mul(d, -0.004)), [0.0115, 0.0115, 0.0115], STAMP_KNOB, held);
  limb(add(A.palm, mul(d, 0.010)), add(A.palm, mul(d, 0.034)), 0.0062, 0.0058, STAMP_KNOB, held);
  limb(add(A.palm, mul(d, 0.034)), add(A.palm, mul(d, 0.050)), 0.0150, 0.0150, STAMP_BLOCK, { ...held, squareStart: true, squareEnd: true, depth: 0.6 });
}
/** The knitting: in her hands while she knits (two needles, their tips crossing in front, their ends out past her hands,
    and the scarf hanging from them into her lap and down off her knees toward the basket by the stool), or, while her
    hands are busy with anything else, laid in her lap. */
const KNITTING = new Set(["knit", "purl", "look", "shift"]);
function knitting(cx) {
  const { J, limb, ball, parts, pose } = cx, held = { part: parts.HELD }, T = (v) => J.torso(v);
  const rows = (t, nx, ny, x, y) => ((x + 2 * y) % 3 === 0 ? shifted(SCARF, 1) : undefined);
  const kneeMid = mix(J.R.knee, J.L.knee, 0.5), lap = lapOf(J, 0.62, 0.030);
  const inHands = (!pose.gesture || pose.gesture === 23) && !pose.held && (!pose.fidget || KNITTING.has(pose.fidget));      // (a nod, or a look over her glasses, leaves her hands at it)
  if (inHands) {
    const R = J.R.palm, L = J.L.palm, mid = mix(R, L, 0.5);
    for (const [g, sd] of [[R, 1], [L, -1]]) {
      // (long ones, the ends rising out past her elbows: from behind, as she sits at her window, they are what shows)
      const tip = add(mid, T([-sd * 0.020, 0.004, 0.036])), dir = unit(add(unit(sub(g, tip)), T([sd * 0.10, 0.62, -0.30]))), butt = along(g, dir, 0.165);
      limb(tip, butt, 0.0030, 0.0030, NEEDLE, held);
      ball(butt, [0.0055, 0.0055, 0.0055], NEEDLE, held);
    }
    const top = add(mid, T([0, 0.016, 0.026]));
    limb(top, lap, 0.026, 0.030, SCARF, { ...held, fn: rows });
    limb(lap, add(kneeMid, [0, -0.13, 0.03]), 0.030, 0.028, SCARF, { ...held, fn: rows });
  } else {
    const a = add(lap, T([0.060, 0.012, -0.010])), b = add(lap, T([-0.060, 0.016, 0.020]));
    limb(add(lap, T([0, 0.004, 0])), add(kneeMid, [0, -0.13, 0.03]), 0.030, 0.028, SCARF, { ...held, fn: rows });
    limb(a, b, 0.0030, 0.0030, NEEDLE, held);
    limb(add(a, T([0, 0, 0.030])), add(b, T([0, 0, -0.030])), 0.0030, 0.0030, NEEDLE, held);
  }
}
/** A small slip of paper (the receipt) in her hand or hands, as her hold says (pose.slip: "R", "L" or "both"). */
function slip(cx) {
  const { J, limb, parts, pose, wide, deep } = cx, s = pose.slip;
  if (!s) return;
  const held = { part: parts.HELD };
  if (s === "both") {
    const a = add(J.L.palm, J.torso([0.008, 0.016, 0.006])), b = add(J.R.palm, J.torso([-0.008, 0.016, 0.006])), w = [0.030, 0.0015], r = wide(w);
    limb(a, b, r, r, RECEIPT_PAPER, { ...held, depth: deep(w) / Math.max(1e-4, r), squareStart: true, squareEnd: true, bias: 1 });
    return;
  }
  const A = J[s], at = s === "L" && pose.flatL ? add(A.palm, J.torso([0, 0.012, 0])) : A.palm, w = [0.026, 0.0015], r = wide(w);
  limb(add(at, J.torso([0, 0.004, -0.020])), add(at, J.torso([0, 0.004, 0.026])), r, r, RECEIPT_PAPER, { ...held, depth: deep(w) / Math.max(1e-4, r), squareStart: true, squareEnd: true, bias: 1 });
}
/** Everything of Opal's but what is in her arms: the glasses and the chain, the thimble, the stamp, the knitting, the keys. */
function opalGear(cx) {
  const { J, pose, seatOnly, trunkAt, limb, ball, d, parts, cloth, S } = cx;
  if (seatOnly) return;
  halfMoons(cx);
  inkAt(cx, J.R.thumb1, INK_THIMBLE, 0.014);                            // the rubber thimble on her right thumb
  const sitting = pose.seated && !(pose.rising > 0), stamping = (pose.fidget === "thunk" && pose.fu > 0.08 && pose.fu < 0.92) || pose.gesture === 22;
  if (sitting && !cx.spec.armsFull) knitting(cx);
  if ((!pose.seated || stamping) && !cx.spec.armsFull) dateStamp(cx);
  if (!pose.seated && S >= 52) {                                        // her keys, on a ring at her left hip
    const at = trunkAt(d.hipY + 0.030, -1.28, 0.010), o = { part: parts.EXTRA, bias: cloth * 2 };
    ball(at, [0.0080, 0.0080, 0.0040], KEY_METAL, o);
    for (const [dx, len] of [[-0.006, 0.034], [0.004, 0.028], [0.010, 0.022]]) limb(add(at, [dx * 0.5, -0.004, 0]), add(at, [dx, -len, 0.004]), 0.0040, 0.0034, KEY_METAL, o);
  }
  slip(cx);
}
// Where her hands are while she knits, on her stool: together in front of her, low, her elbows out.
const OPAL_KNIT = {
  R: { hand: [0.042, -0.150, 0.150], bend: [1, -0.4, -0.5], grip: true, point: [-0.55, 0.30, 0.75] },
  L: { hand: [-0.042, -0.146, 0.146], bend: [-1, -0.4, -0.5], grip: true, point: [0.55, 0.30, 0.75] },
};
/** Opal's own holds (figure.hold(true, name)), each made from how she is (on her stool, or on her feet). */
const opalHolds = {
  /** turned on her stool to look up (at the vent): her head back, looking up over her glasses, the receipt in her right
      hand in her lap. (The scene turns her the way the vent is first: she is on a stool that turns.) */
  up: (o) => {
    const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.06, twist: -0.22, head: { nod: nodOf(b) - 0.50, turn: -0.42 }, slip: "R", held: "up", over: 1 };      // (her shoulders round to her left, her head up over that shoulder)
    withArm(p, "R", { hand: [0.050, -0.200, 0.120], bend: [1, -0.4, -0.5], curl: 0.6, point: [-0.3, -0.3, 0.9] });
    withArm(p, "L", { hand: [-0.050, -0.206, 0.112], bend: [-1, -0.4, -0.5], curl: 0.7, point: [0.4, -0.3, 0.85] });
    return p;
  },
  /** reading a slip (the receipt) close, in both hands, her chin down, through her half-moons */
  read: (o) => {
    const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.16 }, slip: "both", held: "read" };
    withArm(p, "R", { hand: [0.032, -0.104, 0.170], bend: [1, -0.6, -0.4], curl: 0.8, point: [-0.6, 0.5, 0.6] });
    withArm(p, "L", { hand: [-0.032, -0.104, 0.170], bend: [-1, -0.6, -0.4], curl: 0.8, point: [0.6, 0.5, 0.6] });
    return p;
  },
  /** looking at someone over her glasses: the chin down, the glasses a little lower (sitting or standing) */
  over: (o) => ({ ...cloneP(o.base), head: { nod: nodOf(o.base) + 0.14 }, over: 1, held: o.seated ? null : "over" }),
  /** on her feet, holding out the slip for signing on her left palm, the stamp ready in her right */
  form: (o) => {
    const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.04, head: { nod: nodOf(b) + 0.08 }, slip: "L", flatL: true, held: "form" };
    withArm(p, "L", { hand: [-0.040, -0.172, 0.215], bend: [-1, -0.5, -0.4], flat: true, thumb: [0, 0, 1], point: [0.30, 0.0, 0.95] });
    withArm(p, "R", { hand: [0.060, -0.200, 0.110], bend: [1, -0.5, -0.5], grip: true, point: [-0.2, -0.9, 0.3] });
    return p;
  },
};
/** Opal, found on her stool at her window (the stool is painted: OPAL_STOOL_SEAT), knitting, her back to the shelves; her
    life is her knitting. On her feet (`stood`, and `opal-standing`): the stamp in her hands, her keys at her hip. */
export const opal = {
  ...opalBase,
  seated: "chair", sit: { seat: OPAL_STOOL_SEAT, lean: 0.10, knees: 0.08, feet: 0.02 }, shadow: 0.20, span: 1.20,
  top: { ...opalBase.top, hem: undefined },                            // (sitting, her cardigan rides up over the skirt's band: no hem below it)
  rest: OPAL_KNIT,
  riseMs: 560,                                                          // down off the stool briskly: a little hop (rig.js hopPose)
  fidgets: { only: true, sit: ["knit", "purl", "yarn", "look"], stand: ["look", "shift", "tidy"] },      // (two of her four are the needles going: give her `life: { fidget: [2.6, 3.4] }` and she knits nearly all the time)
  holds: opalHolds, cues: { sit: ["thunk"], stand: ["thunk"] },      // (cues: what a script plays on her, besides her life: the THUNK)
  stood: { rest: undefined, holds: opalHolds, top: opalBase.top, span: 1.10, shadow: 0.17 },
  extras(c) { opalGear(c); },
};
export const opalStanding = { ...upOf(opal), name: "Opal, standing" };
// ---------- Opal with the banjo (damaged), in both arms in front of her: from the shelf to Grandpa Joe ----------
const OPAL_ARMS = {
  R: { hand: [0.064, -0.270, 0.150], bend: [0.9, -0.6, -0.4], curl: 0.8, point: [-0.6, 0.1, 0.8] },      // under the pot
  L: { hand: [-0.096, -0.150, 0.150], bend: [-0.9, -0.5, -0.4], curl: 0.9, point: [0.6, 0.3, 0.75] },     // round the neck where it leaves the pot
};
export const opalBanjo = {
  ...opalStanding, name: "Opal, with the banjo", span: 1.25, armsFull: true,
  hold: OPAL_ARMS, gestures: [23, 0, 23, 0],                            // her arms are full: over her glasses, a nod
  fidgets: { only: true, stand: ["look"] }, holds: { over: opalHolds.over }, cues: undefined,
  extras(c) {
    opalGear(c);
    const { J } = c, T = (v) => add(J.sh, J.torso(v)), D = (v) => J.torso(v);
    banjo(c, { c: T([0.010, -0.228, 0.152]), u: D([-0.78, 0.60, 0.12]), n: D([0.10, 0.20, 0.97]), k: 0.97 / 0.886 }, "broken");
  },
};

// ---------- the backup at the Office ----------
// Dale (suit1) and Merle (suit2), seated at the table in the Comfortable Room, side-on (the chairs and the table are
// painted: OFFICE_CHAIR_SEAT, OFFICE_TABLE_TOP, TABLE_EDGE). Dale reads the questionnaire, forty-seven pages and a green
// one, held up in both hands; Merle writes the answers in capitals in his own copy, flat on the table, the pen going.
// In the heat (`suit1-hot`, `suit2-hot`) they sweat, Merle mops his brow (`mop`) and Dale loosens his tie a finger's
// width and puts it back (`loosen`). They get up where they sit (they push their chairs back) and walk out with the papers.
const QPAPER = ramp("#ffffff", "#f3f3f0", "#cbcbc4", "#93938a");
const QGREEN = ramp("#e0f8c8", "#a8d88c", "#76aa5c", "#4c723a");          // the green page
/** A point on the table top in front of someone seated at it, in the space of their shoulders (as hands are placed). */
function onTable(spec, x, fwd, up = 0.014) {
  const J = skeleton(spec.dim, poses.sit({ ...spec, rest: undefined, hold: undefined }, 0));
  return torsoOf(J)([x, OFFICE_TABLE_TOP / (spec.height || 1) + up, J.hipC[2] + fwd]);
}
/** The questionnaire, held up between Dale's hands, its pages toward him: thick, stapled, the green page sticking out of
    it; on his feet, in his left hand at his side. */
function questionnaire(cx) {
  const { J, limb, parts, wide, deep, pose, seatOnly, sf, P, fine } = cx;
  if (seatOnly) return;
  const held = { part: parts.HELD }, sitting = pose.seated && !(pose.rising > 0), oneHand = !sitting || pose.fidget === "loosen" || pose.fidget === "mop";
  // sitting: its foot on the table's edge between his hands, its top leaning away from him as a book is read; on his feet,
  // upright in his left hand at his side
  const mid = oneHand ? J.L.palm : mix(J.R.palm, J.L.palm, 0.5), up = sitting ? unit(J.torso([0, 0.80, 0.60])) : unit(J.torso([0, 1, 0.10]));
  // (turned a little toward his left, so that side-on, as he sits at the table, it is seen at a slant and not edge-on)
  const TURN = -0.75, w = [0.056, 0.012], r = cx.widthAt(w, cx.tw * 0.6 + TURN), a = add(mid, mul(up, -0.010)), b = add(mid, mul(up, 0.140));
  const leaves = fine ? (t, nx, ny, x, y) => ((x + y) % 2 === 0 && Math.abs(nx) > 0.70 ? shifted(QPAPER, 1) : undefined) : null;      // (the edges of its pages)
  limb(a, b, r, r, QPAPER, { ...held, depth: cx.depthAt(w, cx.tw * 0.6 + TURN) / Math.max(1e-4, r), squareStart: true, squareEnd: true, fn: leaves });
  const across = turn([1, 0, 0], cx.tw * 0.6 + TURN);                   // (its width, turned so)
  limb(add(mix(a, b, 0.80), mul(across, 0.052)), add(mix(a, b, 0.94), mul(across, 0.064)), 0.010, 0.010, QGREEN, { ...held, bias: -0.5 });      // the green page, sticking out at the side
  if (fine) for (const k of [0.30, 0.48, 0.66]) { const q = P(add(mix(a, b, k), J.torso([0, 0, -0.014]))); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), pack("#a8a8b0"), parts.HELD); }      // lines of print
  if (pose.fidget === "page" && pose.fu > 0.25 && pose.fu < 0.70) limb(b, J.L.palm, 0.020, 0.016, QPAPER, { ...held, bias: 1 });       // a page, turning over
}
/** Merle's copy, flat on the table between his hands, and his pen in his right fist, its point on the page. */
function answerSheet(cx) {
  const { J, limb, parts, wide, deep, pose, seatOnly } = cx;
  if (seatOnly) return;
  const held = { part: parts.HELD };
  if (pose.seated && !(pose.rising > 0)) {
    // flat on the table top, where it lies whatever his hands do
    const top = OFFICE_TABLE_TOP / (cx.spec.height || 1) + 0.003, h = J.hipC, near = [h[0] + 0.004, top, h[2] + TABLE_EDGE + 0.030], far = [h[0] + 0.004, top, h[2] + TABLE_EDGE + 0.150], w = [0.062, 0.003], r = wide(w);
    limb(near, far, r, r, QPAPER, { ...held, depth: deep(w) / Math.max(1e-4, r), squareStart: true, squareEnd: true });
  } else {
    const g = J.L.palm, w = [0.050, 0.006], r = wide(w);
    limb(add(g, J.torso([0, -0.010, 0.004])), add(g, J.torso([0, 0.110, 0.012])), r, r, QPAPER, { ...held, depth: deep(w) / Math.max(1e-4, r), squareStart: true, squareEnd: true });
  }
  const g = J.R.palm, dn = unit(J.R.hDir);
  limb(add(g, mul(dn, -0.020)), add(g, mul(dn, 0.034)), 0.0040, 0.0030, ramp("#4c4a58", "#2c2a36", "#1c1a24", "#0e0d14"), held);      // the pen
}
const DALE_DESK = { seated: "chair", sit: { seat: OFFICE_CHAIR_SEAT, lean: 0.06, knees: 0.08, feet: 0.08, up: 0 }, shadow: 0.22, span: 1.15, riseMs: 900 };
const daleBody = { ...suit1, ...DALE_DESK, name: "Man in Gray (Dale), at the table", hold: undefined, rest: undefined };
const DALE_HOLD = { R: { hand: onTable(daleBody, 0.058, TABLE_EDGE + 0.020, 0.036), bend: [1, -0.5, -0.4], grip: true, point: [-0.6, 0.5, 0.6] },
                    L: { hand: onTable(daleBody, -0.058, TABLE_EDGE + 0.020, 0.036), bend: [-1, -0.5, -0.4], grip: true, point: [0.6, 0.5, 0.6] } };
const daleOf = (hot) => ({
  ...daleBody, name: hot ? "Man in Gray (Dale), at the table, in the heat" : daleBody.name,
  hold: DALE_HOLD, gestures: [0, 2, 0, 16],                             // the questionnaire in both hands: he talks with his head
  fidgets: { only: true, sit: hot ? ["page", "loosen", "page"] : ["page", "look"], stand: ["watch", "tie"] }, cues: { sit: ["loosen", "page"], stand: ["loosen", "mop"] },
  stood: { hold: { L: { hand: [-0.060, -0.196, 0.120], bend: [-1, -0.5, -0.4], grip: true } }, span: 1.05, shadow: 0.18 },      // on his feet: the papers in his left hand, as his clipboard was
  extras(c) { agent.extras(c); earpiece(c); questionnaire(c); hankie(c); if (hot) sweat(c); },
});
export const suit1Table = daleOf(false), suit1Hot = daleOf(true);
const merleBody = { ...suit2, ...DALE_DESK, name: "Man in Gray (Merle), at the table", hold: undefined, rest: undefined };
const MERLE_PEN = { hand: onTable(merleBody, 0.030, TABLE_EDGE + 0.090, 0.050), bend: [1, -0.5, -0.4], grip: true, point: [-0.3, -0.6, 0.7] };
const merleOf = (hot) => ({
  ...merleBody, name: hot ? "Man in Gray (Merle), at the table, in the heat" : merleBody.name,
  hold: { R: MERLE_PEN }, hand: "L",
  rest: { L: { hand: onTable(merleBody, -0.050, TABLE_EDGE + 0.080, 0.026), bend: [-1, -0.5, -0.4], flat: true, point: [0.4, -0.3, 0.85] } },
  gestures: [5, 0, 2, 0],                                               // a hand to his heart (sorry), a nod, a shrug: he apologizes for every question
  fidgets: { only: true, sit: hot ? ["write", "mop", "write"] : ["write", "look", "write"], stand: ["watch", "tie"] }, cues: { sit: ["mop"], stand: ["mop"] },
  stood: { hold: { L: { hand: [-0.060, -0.196, 0.120], bend: [-1, -0.5, -0.4], grip: true } }, rest: undefined, hand: "R", span: 1.05, shadow: 0.18 },
  extras(c) { agent.extras(c); earpiece(c); answerSheet(c); hankie(c); if (hot) sweat(c); },
});
export const suit2Table = merleOf(false), suit2Hot = merleOf(true);

// Wendell (suit3): on the front door, by regulation facing the gate; it is his birthday, and he has a button that says so.
// `suit3-birthday` is the same man with a round yellow button on his lapel; `suit3-ears`, the same, his fingers in his ears
// (the Rag: he walks, stands and talks so), his juice box in his breast pocket.
const BUTTON = ramp("#fff6b0", "#ffd83a", "#d6a816", "#94700a");
function birthdayButton(cx) {
  const { J, ball, d, parts, cloth, seatOnly, sf, P, trunkFacing, th, S } = cx;
  if (seatOnly) return;
  const f = trunkFacing(-0.62), at = add(J.sh, J.torso([-0.054, -0.052, d.trunkTop[1] + 0.006]));
  ball(at, [0.0150, 0.0150, 0.0050], BUTTON, { part: parts.EXTRA, bias: cloth * 3 }, cx.tw);
  if (S >= 84 && f[0] * Math.sin(th) + f[2] * Math.cos(th) > 0.30) { const q = P(add(at, J.torso([0, 0, 0.006]))); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), pack("#e8402e"), parts.EXTRA); }      // a candle on it, red
}
function pocketJuice(cx) {
  const { J, limb, d, parts, cloth, seatOnly } = cx;
  if (seatOnly) return;
  const at = add(J.sh, J.torso([0.054, -0.060, d.trunkTop[1] + 0.006]));
  limb(add(at, [0, -0.012, 0]), add(at, [0, 0.024, 0]), 0.016, 0.016, ramp("#d8f6a0", "#8ccf3e", "#5e9a24", "#3a6414"), { part: parts.EXTRA, bias: cloth * 2, squareStart: true, squareEnd: true, depth: 0.6 });
  limb(add(at, [0.004, 0.024, 0]), add(at, [0.008, 0.050, -0.002]), 0.0030, 0.0030, ramp("#ffffff", "#f4f0f0", "#d0caca", "#9a9494"), { part: parts.EXTRA, bias: cloth * 2 });
}
export const suit3Birthday = { ...suit3, name: "Man in Gray (Wendell), with his birthday button", extras(c) { suit3.extras(c); birthdayButton(c); } };
const EARS = {      // (the wrist below and outside the ear, the finger up into it, the elbow out and down)
  R: { hand: [0.094, 0.026, -0.006], bend: [0.6, -0.8, 0.1], finger: true, point: [-0.50, 0.86, 0.0] },
  L: { hand: [-0.094, 0.026, -0.006], bend: [-0.6, -0.8, 0.1], finger: true, point: [0.50, 0.86, 0.0] },
};
export const suit3Ears = {
  ...suit3Birthday, name: "Man in Gray (Wendell), his fingers in his ears", hold: EARS, span: 1.15,
  gestures: [0, 2, 0, 4],                                               // his hands are at his ears: he talks with his head
  fidgets: { only: true, stand: ["look"] },
  extras(c) { agent.extras(c); earpiece(c); pocketJuice(c); birthdayButton(c); },
};

// Floyd (suit4): on his regulation rest after a transport, asleep sitting up on the break room's couch (painted:
// COUCH_SEAT), slumped, his head back against it, his sunglasses on, his mouth a little open, breathing slowly. He shifts
// now and then (`stir`, his life); a script can wake him for a moment (`wake`), and he goes back. In his sleep he talks
// regulations, with no hands at all. (The cheeseburger's bag is long gone.)
export const suit4Asleep = {
  ...suit4, name: "Man in Gray (Floyd), asleep", hold: undefined,
  seated: "chair", sit: { seat: COUCH_SEAT, lean: -0.22, knees: 0.26, feet: 0.30, nod: -0.22, turn: 0.34 }, shadow: 0.24, span: 1.30,      // (his head lolled to one side against the couch's back)
  rest: { R: { hand: [0.120, -0.300, 0.090], bend: [1, -0.4, -0.3], curl: 0.5, point: [0.1, -0.9, 0.4] }, L: { hand: [-0.020, -0.200, 0.110], bend: [-1, -0.3, -0.4], curl: 0.6, point: [0.6, -0.4, 0.6] } },
  restMouth: 1, gestures: [0],
  fidgets: { only: true, sit: ["stir", "stir"] }, cues: { sit: ["wake"] },
  riseMs: 1400,
  stood: { rest: undefined, restMouth: 0, gestures: [0, 8, 0, 10], fidgets: { stand: ["watch"] }, span: 1.05, shadow: 0.18 },
  extras(c) { agent.extras(c); earpiece(c); hankie(c); },
};

// ---------- Jed in the break room: the hoop still round his neck ("It is evidence."), an ice pack held to the top of his head ----------
// Found sitting on the plastic chair (painted: BREAK_CHAIR_SEAT), facing the counter and the pie. When Houston calls him
// to the front desk he is up so fast the ice pack is still in the air: figure.sit(false) is quick (riseMs), and from the
// moment he starts up the pack is no longer drawn on him. The script puts the `icepack` prop (js/art/props.js) where it
// was (icePackAt, below), lets it hang a moment and tweens it down.
const ICE_HAND = { hand: [0.020, 0.214, 0.012], bend: [0.9, 0.6, -0.1], flat: true, point: [-0.55, -0.10, 0.80], thumb: [0, 0, 1] };
function icePack(cx) {
  const { J, pose, ball, limb, parts, seatOnly } = cx;
  if (seatOnly || !pose.seated || pose.rising > 0) return;
  const at = add(J.R.palm, [0, -0.020, 0]), held = { part: parts.HELD };
  ball(at, [0.046, 0.024, 0.040], ramp("#ecf7ff", "#a9d2f2", "#6f9fcc", "#466a92"), held);
  limb(add(at, J.torso([0.034, 0.008, 0])), add(at, J.torso([0.050, 0.026, 0])), 0.010, 0.009, CHROME, held);     // the cap
}
export const agentIce = {
  ...agentCollar, name: "Man in Gray (Jed), with an ice pack",
  seated: "chair", sit: { seat: BREAK_CHAIR_SEAT, lean: 0.03, knees: 0.12, feet: 0.10, nod: 0.03 }, shadow: 0.22, span: 1.25, under: 0,
  crown: 0.056,                                                         // (his hand and the pack on top of his head: his words go over them)
  hold: { R: ICE_HAND },
  rest: { L: { hand: [-0.110, -0.330, 0.150], bend: [-1, -0.3, -0.4], curl: 0.6, point: [0.3, -0.7, 0.6] } },
  riseMs: 300,                                                          // up so fast the ice pack is still in the air
  gestures: [0, 8, 0, 0],
  fidgets: { only: true, sit: ["look"], stand: ["watch", "tie"] },
  stood: { hold: undefined, rest: undefined, crown: 0, span: 1.05, under: 0, shadow: 0.18, gestures: [0, 8, 0, 10] },
  extras(c) { agent.extras(c); hoop(c); dusty(c); icePack(c); },
};
/** Where the `icepack` prop goes so that it is where the pack was on Jed's head: [right, down] in picture pixels from his
    place (the point on the floor under his hips), for him drawn `size` pixels tall facing `yawDeg`. Put the prop there at
    his scale: cast.addThing("icepack", "icepack", jed.x + dx, jed.y + dy, jed.scale). */
export function icePackAt(yawDeg, size) {
  const J = skeleton(agentIce.dim, poses.sit(agentIce, 0)), p = add(J.R.palm, [0, -0.020 - 0.024, 0]);      // (the bottom of the pack: the prop's foot)
  const th = (yawDeg * Math.PI) / 180, cs = Math.cos(th), sn = Math.sin(th), dp = (p[0] * sn + p[2] * cs) * size;
  return [Math.round((-p[0] * cs + p[2] * sn) * size * 10) / 10, Math.round((-p[1] * size + dp * 0.22) * 10) / 10];
}

// ---------- Grandpa Joe at the Office ----------
// He has no banjo when he comes in (it is in Property & Effects, tag No. 3117). His hat is on throughout.
//   grandpajoe-table   at the table in the Comfortable Room, on its chair (painted: OFFICE_CHAIR_SEAT), side-on, his hands
//                      on the table; up (figure.sit(false)) he stands where he sat (he pushes the chair back)
//   grandpajoe-room    on his feet in the room, his thumbs in his straps; his hold `intercom`
//   grandpajoe-chair   standing on the corner chair (standOn), looking up at the vent; his holds `reach` and `read`; his
//                      movements `passup`, `taketin`, `takepaper`
//   grandpajoe-banjo-broken, grandpajoe-banjo-pie     carrying the banjo by the neck at his side, as it is
//   grandpajoe-play-broken, grandpajoe-play-pie       playing it, standing or walking: his hands stay on it, and the right
//                      strums as he walks and as he talks (`strum` while he stands); `grandpajoe-play` is the banjo whole
const JOE_TABLE_GESTURES = [0, 6, 0, 11, 5];                            // above the table: a nod; a hand to his chin; a finger raised; a hand to his heart
const joeDeskBody = { ...joeBase, name: "Grandpa Joe, at the table", seated: "chair", sit: { seat: OFFICE_CHAIR_SEAT, lean: 0.03, knees: 0.10, feet: 0.10, up: 0 }, shadow: 0.24, span: 1.15 };
const joeIntercom = (o) => {
  const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.15, head: { nod: nodOf(b) + 0.10, turn: 0.22 } };      // leaning in, an ear to the speaker
  withArm(p, "R", { hand: [0.054, -0.044, 0.250], bend: [0.8, -0.7, -0.2], finger: true, point: [-0.15, 0.10, 1] });
  return p;
};
export const grandpajoeTable = {
  ...joeDeskBody,
  rest: { R: { hand: onTable(joeDeskBody, 0.060, TABLE_EDGE + 0.120, 0.022), bend: [1, -0.5, -0.4], flat: true, point: [-0.3, -0.2, 0.9] },
          L: { hand: onTable(joeDeskBody, -0.070, TABLE_EDGE + 0.100, 0.022), bend: [-1, -0.5, -0.4], curl: 0.7, point: [0.4, -0.2, 0.9] } },
  gestures: JOE_TABLE_GESTURES,
  riseMs: 1250,
  fidgets: { sit: ["hat"], stand: ["back"], not: ["knees"] },
  stood: { rest: undefined, gestures: joeBase.gestures, span: 1.10, shadow: 0.18, holds: { intercom: joeIntercom } },
  extras(c) { joeGear(c); },
};
export const grandpajoeRoom = { ...upOf(grandpajoeTable), name: "Grandpa Joe, on his feet in the Comfortable Room" };
/** On the chair: his hands up to the vent, flat, as high as they go (to talk with Ranger through it, or to hand things up
    and take them down). */
const joeReach = (o) => {
  const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.03, breath: 1, head: { nod: nodOf(b) - 0.16 }, held: "reach" };
  for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.074, 0.250, 0.060], bend: [sd * 0.9, -0.2, -0.3], flat: true, point: [-sd * 0.10, 1, 0.10], thumb: [-sd, 0, 0.3] });
  return p;
};
/** On the chair: reading a sheet held up in both hands (the test schedule), his chin down to it. */
const joeRead = (o) => {
  const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.42 }, held: "read", sheet: true };
  for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.052, -0.040, 0.200], bend: [sd, -0.6, -0.4], curl: 0.8, point: [-sd * 0.4, 0.6, 0.7] });
  return p;
};
/** What he has in his hands on the chair: the receipt going up (`passup`), the pie tin or the sheet coming down
    (`taketin`, `takepaper`), the sheet he reads (`read`). */
function chairThings(cx) {
  const { J, pose, limb, ball, parts, wide, deep, seatOnly } = cx;
  if (seatOnly) return;
  const held = { part: parts.HELD }, f = pose.fidget, u = pose.fu || 0, both = mix(J.R.palm, J.L.palm, 0.5);
  const sheet = (at) => { const w = [0.072, 0.0015], r = wide(w); limb(add(at, J.torso([0, -0.040, 0])), add(at, J.torso([0, 0.060, 0.010])), r, r, QPAPER, { ...held, depth: deep(w) / Math.max(1e-4, r), squareStart: true, squareEnd: true, bias: 1 }); };
  if (f === "passup" && u < 0.52) { const g = J.R.palm, w = [0.026, 0.0015], r = wide(w); limb(add(g, J.torso([0, 0.004, -0.012])), add(g, J.torso([0, 0.050, 0.004])), r, r, RECEIPT_PAPER, { ...held, depth: deep(w) / Math.max(1e-4, r), squareStart: true, squareEnd: true, bias: 1 }); }
  if (f === "taketin" && u > 0.46 && u < 0.94) { ball(add(both, J.torso([0, 0.010, 0.016])), [0.068, 0.014, 0.068], TIN, held, cx.tw); ball(add(both, J.torso([0, 0.020, 0.016])), [0.050, 0.006, 0.050], shifted(TIN, 1), { ...held, bias: 1 }, cx.tw); }
  if (f === "takepaper" && u > 0.46 && u < 0.94) sheet(both);
  if (pose.sheet) sheet(both);
}
export const grandpajoeChair = {
  ...joeBase, name: "Grandpa Joe, standing on the chair", standOn: OFFICE_CHAIR_SEAT, nod: -0.34, span: 1.25, shadow: 0.10,
  tall: 1.55,                                                           // (room in his picture for his hands up over his head, on the chair)
  gestures: [0, 8, 0, 1, 5],
  fidgets: { only: true, stand: ["look"] },
  holds: { reach: joeReach, read: joeRead }, cues: { stand: ["passup", "taketin", "takepaper"] },
  extras(c) { joeGear(c); chairThings(c); },
};
// The banjo in his hands at the Office: carried by the neck at his side, as he carries it whole (grandpajoe-standing), or
// held across him to play, as at the glass (grandpajoe-play), with his hands kept on it as he walks and talks.
const JOE_STRUM = { ...JOE_REST.R, stroke: [0.006, -0.046, 0.004], strokes: 2 };     // his right hand over the head, strumming as he walks and talks
const JOE_FRET = JOE_REST.L;
const lapBanjo = (c) => { const { J } = c, T = (v) => add(J.sh, J.torso(v)), D = (v) => J.torso(v); return { c: T(JOE_LAP.c), u: D(JOE_LAP.u), n: D(JOE_LAP.n) }; };
const carriedBanjo = (c) => { const { J } = c, u = J.torso([0.10, 1, 0.12]); return { c: along(J.R.palm, unit(u), -0.215), u, n: J.torso([0.82, 0, 0.57]) }; };
const joePlaying = (state, name) => ({
  ...joeBase, name, span: 1.12, shadow: 0.18,
  rest: JOE_REST, banjoPot: JOE_LAP.c,
  hold: { R: JOE_STRUM, L: JOE_FRET },
  gestures: [0, 0, 2, 0],                                               // playing through it: his head and his shoulders talk
  fidgets: { only: true, stand: ["strum"] },
  extras(c) { joeGear(c); banjo(c, lapBanjo(c), state); },
});
export const grandpajoePlayBroken = joePlaying("broken", "Grandpa Joe, playing the broken banjo");
export const grandpajoePlayPie = joePlaying("pie", "Grandpa Joe, playing the pie-tin banjo");
const joeCarrying = (state, name) => ({ ...joeBase, ...joeOnFeet, name, extras(c) { joeGear(c); banjo(c, carriedBanjo(c), state); } });
export const grandpajoeBanjoBroken = joeCarrying("broken", "Grandpa Joe, with the broken banjo");
export const grandpajoeBanjoPie = joeCarrying("pie", "Grandpa Joe, with the pie-tin banjo");
// (and grandpajoe-play, the banjo whole, walks as these do now: its walk keeps his hands on it, strumming)
grandpajoePlay.walk = { ...JOE_STAND, hold: { R: JOE_STRUM, L: JOE_FRET } };
// Jed in the arrival (office-arrive, "A Very Small Building With A Very Long Name"): on his feet, the hoop round his neck,
// carrying what is left of the banjo by its neck at his side, ahead of everyone into the building ("Evidence."). He talks
// with his free hand; the banjo goes into Property & Effects (tag No. 3117) and he never has it again.
const JED_CARRY = { hand: [0.150, -0.300, 0.040], bend: [0.6, -1, -0.5], grip: true, loose: true };
export const agentCollarBanjo = {
  ...upOf(agentCollar), name: "Man in Gray (Jed), carrying the banjo (damaged)",
  hold: { R: JED_CARRY }, hand: "L", span: 1.12,
  fidgets: { only: true, stand: ["watch"] },                           // (his watch is on his left wrist: the banjo stays still)
  extras(c) { agentCollar.extras(c); banjo(c, { ...carriedBanjo(c), k: 0.97 / 1.0 }, "broken"); },
};

// ---------- their own small movements (figure.fidget(name)) ----------
addMoves({
  /** Opal, on her stool: knitting, the needles going, her elbows working (her life when nobody needs her) */
  knit: { ms: 2800, make(o) {
    const b = o.base, at = (dr, dl, nod) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + nod } }; if (b.R.hand) withArm(p, "R", { ...b.R, hand: add(b.R.hand, dr) }); if (b.L.hand) withArm(p, "L", { ...b.L, hand: add(b.L.hand, dl) }); return p; };
    const k1 = at([-0.014, 0.014, 0.012], [0.004, -0.004, 0.000], 0.05), k2 = at([0.010, -0.006, -0.006], [-0.004, 0.006, 0.006], 0.03);
    return [[0, b], [0.12, k1], [0.26, k2], [0.40, k1], [0.54, k2], [0.68, k1], [0.82, k2], [1, b]];
  } },
  /** Opal, on her stool: the needles going the other way about, the left one working, a stitch slipped across */
  purl: { ms: 2600, make(o) {
    const b = o.base, at = (dr, dl, nod) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + nod } }; if (b.R.hand) withArm(p, "R", { ...b.R, hand: add(b.R.hand, dr) }); if (b.L.hand) withArm(p, "L", { ...b.L, hand: add(b.L.hand, dl) }); return p; };
    const k1 = at([-0.004, 0.004, 0.002], [0.014, 0.012, 0.010], 0.06), k2 = at([0.006, -0.004, -0.002], [-0.008, -0.004, -0.004], 0.04);
    return [[0, b], [0.14, k1], [0.30, k2], [0.46, k1], [0.62, k2], [0.78, k1], [1, b]];
  } },
  /** Opal, on her stool: a tug at the yarn, down to the basket at her left, and back to her knitting */
  yarn: { ms: 2000, make(o) {
    const b = o.base, down = withArm({ ...cloneP(b), twist: -0.10, head: { nod: nodOf(b) + 0.12, turn: -0.20 } }, "L", { hand: [-0.150, -0.300, 0.060], bend: [-1, -0.4, -0.4], grip: true });
    const tug = withArm({ ...cloneP(b), twist: -0.06, head: { nod: nodOf(b) + 0.08, turn: -0.12 } }, "L", { hand: [-0.100, -0.200, 0.100], bend: [-1, -0.5, -0.4], grip: true });
    return [[0, b], [0.30, down], [0.48, tug], [0.62, down], [1, b]];
  } },
  /** Opal: the date stamp brought down, THUNK, onto the slip on her other palm (or on her counter) (a script plays the
      sound `thunk` when it lands: at 0.46 of its time, 550 ms in) */
  thunk: { ms: 1200, make(o) {
    const b = o.base, sp = o.sp, at = (up, nod) => {
      const p = { ...cloneP(b), head: { nod: nodOf(b) + nod } };
      withArm(p, "L", { hand: [-0.020, sp.waist + 0.040, sp.belly + 0.100], bend: [-1, -0.5, -0.3], flat: true, thumb: [0, 0, 1], point: [0.5, -0.1, 0.85] });
      return withArm(p, "R", { hand: [0.012, sp.waist + 0.122 + up, sp.belly + 0.104], bend: [1, -0.4, -0.3], grip: true, point: [-0.2, -1, 0.15] });
    };
    const ready = at(0.050, 0.08), high = at(0.090, 0.06), down = at(0.002, 0.14);
    return [[0, b], [0.18, ready], [0.34, high], [0.46, down], [0.60, down], [0.74, ready], [1, b]];
  } },
  /** Opal, on her feet: she straightens her cardigan, a tug at each front */
  tidy: { ms: 1600, make(o) {
    const b = o.base, sp = o.sp, at = (dy) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.10 } }; withArm(p, "R", { hand: [0.040, sp.waist + 0.010 + dy, sp.belly + 0.030], bend: [1, -0.4, -0.4], grip: true }); return withArm(p, "L", { hand: [-0.040, sp.waist + 0.010 + dy, sp.belly + 0.030], bend: [-1, -0.4, -0.4], grip: true }); };
    return [[0, b], [0.30, at(0)], [0.46, at(-0.022)], [0.62, at(0)], [1, b]];
  } },
  /** the men in gray: a handkerchief to the brow, dabbing it twice, and put away (in the heat); with the free hand (holdable) */
  mop: { ms: 2600, hold: 0.5, make(o) {
    const b = o.base, s = o.held("L") ? (o.held("R") ? "L" : "R") : "L", sd = s === "R" ? 1 : -1, hr = o.d.headR;
    const at = (dx, dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) - 0.08, turn: -sd * 0.06 }, mopHand: s }, s, { hand: [sd * (0.006 + dx), o.sp.headY + hr[1] * 0.42 + dy, hr[2] + 0.040], bend: [sd * 0.7, -0.8, 0.3], curl: 0.8, point: [-sd, 0.15, 0.1] });
    const a1 = at(0.010, 0), a2 = at(-0.012, -0.010);
    return [[0, { ...cloneP(b), mopHand: s }], [0.22, a1], [0.36, a2], [0.50, a1], [0.64, a2], [0.78, a1], [1, { ...cloneP(b), mopHand: s }]];
  } },
  /** Dale: loosens his tie a finger's width, a breath of air, and puts it back (regulations) */
  loosen: { ms: 2600, make(o) {
    const b = o.base, sp = o.sp, s = o.held("R") && !o.held("L") ? "L" : "R", sd = s === "R" ? 1 : -1;
    const at = (dy, nod) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + nod } }, s, { hand: [sd * 0.008, -0.044 + dy, sp.chest + 0.036], bend: [sd, -0.6, -0.1], grip: true, point: [0, 1, 0.3] });
    return [[0, b], [0.20, at(0, -0.06)], [0.34, at(-0.018, -0.10)], [0.50, { ...at(-0.018, -0.14), breath: 1 }], [0.66, at(-0.016, -0.04)], [0.76, at(0.002, -0.06)], [1, b]];
  } },
  /** Dale, at the table: turns a page of the questionnaire, his left hand over the top of it */
  page: { ms: 1800, make(o) {
    const b = o.base, q = b.L, lift = (k) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.04 } }, "L", { ...q, hand: add(q.hand, [0.010 * k, 0.110 * k, 0.020 * k]), curl: 0.6 });
    return [[0, b], [0.24, lift(0.6)], [0.42, lift(1)], [0.62, lift(0.5)], [1, b]];
  } },
  /** Merle, at the table: writes the answer down in capitals, the pen going along the line, his head down to it */
  write: { ms: 2600, make(o) {
    const b = o.base, q = b.R, at = (dx, dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.12 } }, "R", { ...q, hand: add(q.hand, [dx, dy, 0]) });
    return [[0, b], [0.12, at(-0.012, 0.004)], [0.24, at(-0.004, 0)], [0.36, at(0.004, 0.004)], [0.48, at(0.012, 0)], [0.60, at(0.020, 0.004)], [0.74, at(-0.010, 0.002)], [0.86, at(0.000, 0.004)], [1, b]];
  } },
  /** Floyd, asleep on the couch: he shifts a little, his head lolls to the other side and back, his mouth shuts and opens */
  stir: { ms: 3200, make(o) {
    const b = o.base, roll = { ...cloneP(b), twist: 0.10, sway: 0.010, mouth: 0, head: { nod: nodOf(b) + 0.06, turn: 0.32 } }, back = { ...cloneP(b), twist: 0.04, mouth: 2, head: { nod: nodOf(b) - 0.02, turn: 0.18 } };
    return [[0, b], [0.30, roll], [0.55, roll], [0.75, back], [1, b]];
  } },
  /** Floyd: wakes for a moment, his head up, a look round through his sunglasses, and back to sleep (a script's: holdable) */
  wake: { ms: 3400, hold: 0.45, make(o) {
    const b = o.base, up = { ...cloneP(b), lean: (b.lean || 0) + 0.16, mouth: 0, head: { nod: nodOf(b) + 0.28, turn: 0.20 } }, round = { ...cloneP(up), head: { nod: nodOf(b) + 0.26, turn: -0.26 } };
    return [[0, b], [0.22, up], [0.40, round], [0.52, round], [0.66, up], [1, b]];
  } },
  /** Grandpa Joe on the chair: the receipt in his right hand, up through the slats of the vent, and his hand down empty */
  passup: { ms: 2200, make(o) {
    const b = o.base, at = (dy) => withArm({ ...cloneP(b), lean: (b.lean || 0) - 0.03, head: { nod: nodOf(b) - 0.16 } }, "R", { hand: [0.040, 0.250 + dy, 0.046], bend: [0.9, -0.2, -0.3], grip: true, point: [0, 1, 0.1] });
    return [[0, b], [0.30, at(0)], [0.44, at(0.016)], [0.56, at(0.016)], [0.70, at(-0.020)], [1, b]];
  } },
  /** Grandpa Joe on the chair: both hands up to the vent, and down with what Ranger hands through it: the pie tin */
  taketin: { ms: 2600, make(o) { return takeDown(o, 0.05); } },
  /** the same, with a sheet of paper (the test schedule) */
  takepaper: { ms: 2600, make(o) { return takeDown(o, 0.0); } },
});
/** Both hands up to the vent, a moment there, and down together to his chest with what he took. */
function takeDown(o, wide) {
  const b = o.base, both = (y, z, nod, flat) => {
    const p = { ...cloneP(b), lean: (b.lean || 0) - (y > 0.1 ? 0.03 : 0), head: { nod: nodOf(b) + nod } };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * (0.046 + wide), y, z], bend: [sd * 0.9, -0.3, -0.3], ...(flat ? { flat: true, point: [-sd * 0.15, 1, 0.1] } : { curl: 0.8, point: [-sd * 0.5, 0.2, 0.8] }) });
    return p;
  };
  const up = both(0.258, 0.046, -0.16, true), got = both(0.240, 0.050, -0.16, false), chest = both(-0.090, 0.200, 0.30, false);
  return [[0, b], [0.28, up], [0.40, up], [0.48, got], [0.70, chest], [0.90, chest], [1, b]];
}

export const people = {
  dad, son, mom, bigsis, lilsis,
  scribe, carrier, overseer, hauler1, hauler2, hauler3, mason1, mason2, guard, lampboy, goldsmith,
  keeper, washer, urchin, soothsayer, senator, doorkeeper, clerk, dateseller,
  oldtimer, agent,
  lot,
  // the same people at another moment of the story (a scene puts one in the other's place):
  "guard-shade": guardShade, "goldsmith-shades": goldsmithShades, "lot-standing": lotStanding,
  // NEVADA-12P: the Last Stop, round twelve (Grandpa Joe takes the old-timer's place; the old-timer stays for the older tests)
  grandpajoe, jolene, suit1, suit2, suit3, suit4,
  "grandpajoe-shade": grandpajoeShade, "grandpajoe-broken": grandpajoeBroken, "grandpajoe-tied": grandpajoeTied,
  "grandpajoe-seat-tied": grandpajoeSeatTied, "grandpajoe-seat-loose": grandpajoeSeatLoose,
  "jolene-2": jolene2, "jolene-3": jolene3, "jolene-4": jolene4, "jolene-5": jolene5,
  "agent-collar": agentCollar,
  "grandpajoe-play": grandpajoePlay,                                    // NEVADA-12SA: on his feet at the glass, playing
  // NEVADA-12SC: the cut-scene "Backup" (above)
  "grandpajoe-standing": grandpajoeStanding, "grandpajoe-swing": grandpajoeSwing, "grandpajoe-carried": grandpajoeCarried,
  "suit2-carry": suit2Carry, "suit3-carry": suit3Carry,
  // ROME-13P: the bigger Rome, round thirteen; and the same people in another state, which a scene swaps in under the same id
  gaul, phyllis, titus, anser, eleazar, mariam, felix,
  "gaul-own": gaulOwn, "phyllis-free": phyllisFree, "titus-free": titusFree, "eleazar-window": eleazarWindow, "felix-free": felixFree,
  // OFFICE-17P: the Office, round seventeen: Opal; and the people of the Office at their moments (each swapped in under the id it stands for)
  opal, "opal-standing": opalStanding, "opal-banjo": opalBanjo,
  "suit1-table": suit1Table, "suit1-hot": suit1Hot, "suit2-table": suit2Table, "suit2-hot": suit2Hot,
  "suit3-birthday": suit3Birthday, "suit3-ears": suit3Ears, "suit4-asleep": suit4Asleep, "agent-ice": agentIce, "agent-collar-banjo": agentCollarBanjo,
  "grandpajoe-table": grandpajoeTable, "grandpajoe-room": grandpajoeRoom, "grandpajoe-chair": grandpajoeChair,
  "grandpajoe-banjo-broken": grandpajoeBanjoBroken, "grandpajoe-banjo-pie": grandpajoeBanjoPie,
  "grandpajoe-play-broken": grandpajoePlayBroken, "grandpajoe-play-pie": grandpajoePlayPie,
};
