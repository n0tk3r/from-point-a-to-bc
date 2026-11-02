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
//   (PEOPLE-20, round twenty: Japan, 1830, at the end of the file:)
//   outfit, wears   a page that is a lead in other clothes (dressed(): `people[<lead>-<outfit>]`, g.dress(who, name) in a scene)
//   bowDeep    how deep their bow is (the movement `ojigi`: 0.14 a guard's nod, 0.30 polite, 0.62 Jinsuke's)
//   pitch      the whole figure tipped (pose.pitch), for someone lying flat: Little Sister under the cherry
//   sit.seat "kneel"   found sitting on the heels (seiza): Grandmother Sei
//   shoes.foot what shows in a sandal when it is not the sock: white tabi under indigo leg wraps
//   and, in rig.js, pose.smile (a smile a pose asks for: Kihei's rare one)
//   (PEOPLE-21A, round twenty-one: the road west, the ship, Osaka and the boy puppet, in the block PEOPLE_21A near the end:)
//   doll       a puppet: it does not breathe, blink or move its lips (rig.js drawFigure)
//   float      how far the feet hang over the ground, in their own heights, unless a pose says otherwise (pose.raise: 0
//              when a doll's feet stamp); the shadow stays on the ground
//   (PEOPLE-21B, round twenty-one: Akashi, Himeji, Shosha, in the section between its marker lines:)
//   wade       standing in water this deep (in their own heights): what is below the surface is not drawn, ripples round the
//              legs (wadeCut: the Awa pilgrims; Little Sister's outfits `edo-wading`); and, exported, lockHand / LOCK_HANDS /
//              withHand (the three hands of the lock's close-up, for ENGINE-21's g.hand)
//
// The family comes from the present, so their colors never change with the era.
// Each of them owns one color nobody else in the family wears.
//
// docs/CHARACTERS.md says who these people are. To change someone, change the numbers
// and colors here; every view and every animation follows. tools/sprites.html shows the result.

import { ADULT, CHILD, WOMAN, blend, ramp, pack, shifted, add, sub, mul, mix, turn, unit, wear, upOf } from "./rig.js";      // (pack, sub, mul, unit: NEVADA-12P)
import { poses, addMoves, moveKit, lerp } from "./rig.js";              // ROME-13P: the bigger Rome's people, and their own small movements
import { Surface } from "./pix.js";                                       // PEOPLE-21B: the hands of the lock's close-up are drawn flat, by the renderer itself
import { keyId } from "./look.js";                                        // PEOPLE-21B: (and kept for each key they are drawn in)

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
  extras(c) {
    const { ball, limb, hp, wide, deep, d, hy, tw, J, S, parts, pose } = c;      // (PEOPLE-20: c itself, for `spec.outfit` below)
    // her hair: long dark curls from the crown down her back, past her shoulders, and a fall of them over each shoulder
    const fall = [0.078, 0.030], foot = [0.070, 0.024], r0 = wide(fall), r1 = wide(foot);
    limb(hp(0, -0.02, -0.72), add(J.spine(d.shoulderY - 0.175), J.torso([0, 0, -(d.trunkTop[1] + 0.018)])), r0, r1, MOM_HAIR, { part: parts.HAIR, depth: deep(fall) / r0, bias: S * 0.012, fn: (t, a) => (curls(t * 5, a, 2.4) ? MOM_CURL : undefined) });
    for (const sd of [1, -1]) {
      const from = hp(sd * 0.94, -0.18, -0.02), to = add(J.sh, J.torso([sd * 0.072, -0.074, 0.010]));
      limb(from, to, 0.024, 0.020, MOM_HAIR, { part: parts.HAIR, fn: (t, a) => (curls(t * 4, a, 1.4) ? MOM_CURL : undefined) });
      ball(to, [0.022, 0.016, 0.018], MOM_HAIR, { part: parts.HAIR }, tw);      // the ends, curling up
    }
    // pearls: one at each ear, and a string of them at the neck (PEOPLE-20: not over a kimono's collar, where at this size
    // the string read as a white beard: in her Edo clothes the pearls are in her pocket)
    for (const sd of [1, -1]) ball(hp(sd * 1.0, -0.34, -0.06), [0.007, 0.008, 0.007], PEARL, { part: parts.EXTRA }, hy);
    if (!c.spec.outfit) ball(add(J.sh, J.torso([0, -0.016, d.trunkTop[1] * 0.50])), [0.046, 0.034, 0.042], PEARL, {
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
  extras(c) {
    lilHair(c);                                                           // (PEOPLE-20: her hair is its own function, so that her Edo clothes keep it)
    // a star on the bib of her overalls
    const { sf, P, d, th, J, fine, parts } = c;
    if (fine && Math.cos(th) > 0.5) {
      const q = P(add(J.spine(d.shoulderY - 0.150), J.torso([0, 0, d.trunkTop[1] * 0.98]))), x = Math.round(q[0] - 0.5), y = Math.round(q[1] - 0.5), star = SUN.tones[0];
      for (const [i, k] of [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]]) sf.dot(x + i, y + k, star, parts.TORSO);
    }
  },
};
/** Little Sister's hair: a wild mop that falls to just past her shoulders, down her back and in a lock in front of each shoulder, the ends flicking out. */
function lilHair({ ball, limb, hp, wide, deep, d, hy, J, S, parts }) {
  const fall = [0.062, 0.026], foot = [0.070, 0.024], r0 = wide(fall), r1 = wide(foot);
  limb(hp(0, -0.10, -0.66), add(J.spine(d.shoulderY - 0.062), J.torso([0, 0, -(d.trunkTop[1] + 0.014)])), r0, r1, LIL_HAIR, { part: parts.HAIR, depth: deep(fall) / r0, bias: S * 0.012, fn: (t, a) => (Math.sin(a * 7 + t * 9) > 0.86 ? LIL_STRAND : undefined) });
  for (const sd of [1, -1]) {
    const from = hp(sd * 0.92, -0.26, 0.00), to = add(J.sh, J.torso([sd * 0.066, -0.040, 0.014]));
    limb(from, to, 0.020, 0.016, LIL_HAIR, { part: parts.HAIR });
    ball(add(to, J.torso([sd * 0.012, -0.010, 0.004])), [0.022, 0.014, 0.018], LIL_HAIR, { part: parts.HAIR }, hy);      // the ends, flicking out
  }
}

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

// =====================================================================================
// PEOPLE-20 (round twenty): Act Six, "By Your Grace": Japan in the spring of 1830
// =====================================================================================
// Two things are new here. OUTFITS: the family in other clothes (O-Tami's travel kimonos, and the plasterers' white
// head-cloths over them), each a kind of its own named `<lead>-<outfit>` ("mom-edo", "lilsis-edo-crew"), made from the
// lead's own page so that face, build, stance, walk, gestures and prayer stay theirs; a script puts one on with
// g.dress(who, outfit) (js/engine/game.js), it is kept in the save, and the lead is drawn in it wherever a lead is drawn
// (the portraits keep their faces). And THE PEOPLE OF 1830: the fishmonger's house at Yui, the hidden family in the hills
// north of Osaka, and Himeji's gate, with their poses and their small lives. Heights: men about 1.56 m, women 1.46 m, so
// Mom (1.68 m) stands a head over every Japanese woman in the act. Everyone is our own: nobody's likeness.
//   Men: the crown shaved and the hair oiled up into a topknot (`chonmage`); short work jackets, tight work trousers, a
//   twisted towel round the head. Women: the hair in the round chignon of a married woman (`marumage`) or a girl's tied-up
//   knot; a married woman's teeth blackened (face.inside near black: a dark mouth when she talks) and, after a child, no
//   eyebrows (face.brows null). Samurai: two swords at the left hip, always sheathed; hakama (the wide pleated trousers,
//   which the rig draws as a long pleated skirt) and a jacket.
// How a script calls each pose is in docs/DESIGN.md, section 4 ("Japan, 1830: the outfits and the people").

const EDO_SKIN = ramp("#f8dcbe", "#e8bc98", "#bc8662", "#80553c");         // townspeople
const EDO_SUN = ramp("#ecc49c", "#d6a078", "#a87452", "#704a36");          // fishermen and sailors: a lifetime on the water
const EDO_PALE = ramp("#fbe6d0", "#f0ccae", "#c89a7c", "#8a6652");         // indoors: the clerk, the young warden
const EDO_SOOT = ramp("#d8bca4", "#c09a80", "#8e6a52", "#5c4436");         // the charcoal-burner: soot worked into the skin
const EDO_HAIR = ramp("#4c4854", "#2c2932", "#19171e", "#0b0a0e");         // black
const EDO_GREY = ramp("#dcd8d0", "#aca79e", "#7c7770", "#4e4a45");         // the grandmother's
const PATE = new Map([[EDO_SKIN, ramp("#e2c0a2", "#cfa284", "#a97856", "#80553c")], [EDO_SUN, ramp("#d4ac88", "#bc8c68", "#946648", "#704a36")], [EDO_PALE, ramp("#e8ccb4", "#d8b49a", "#b08a70", "#8a6652")], [EDO_SOOT, ramp("#c4a890", "#aa8870", "#7e5e4a", "#5c4436")]]);
const pateOf = (skin) => PATE.get(skin) || PATE.get(EDO_SKIN);             // the shaved crown: the skin a shade darker and bluer, where the hair would be
const AI = ramp("#7488c0", "#4c5c96", "#323f6a", "#1e2646");               // indigo cotton, washed a hundred times
const AI_DEEP = ramp("#5868a0", "#38447e", "#242e58", "#151b36");          // indigo, dark and new
const KAKI = ramp("#cc9470", "#a46e4a", "#784c30", "#4e301e");             // persimmon-dyed cotton: brown
const NEZUMI = ramp("#bcb8b0", "#908c84", "#66625c", "#423f3a");           // mouse grey
const CHA = ramp("#ac8e68", "#826848", "#5c4832", "#3c2e20");              // tea brown
const SUMI = ramp("#5e5c66", "#3c3a42", "#26242b", "#151417");             // ink black: a samurai's jacket
const ASAGI = ramp("#a8c8d4", "#78a0b0", "#527684", "#345058");            // a pale blue-green: the guards' hakama
const TENUGUI = ramp("#ffffff", "#f4f2ea", "#c8c4b8", "#8e8a80");          // white cotton: the head-cloths
const SUGE = ramp("#f0dca4", "#d4b874", "#a0884c", "#6a5a32");             // sedge: the hats
const WARAJI = ramp("#dcc48c", "#b89e60", "#886f3e", "#584a24");           // straw sandals, and a straw raincoat
const BENI = ramp("#ff7c5c", "#e24c30", "#aa3422", "#6e2016");             // vermilion: Kihei's sixtieth-year red
const SHIKKUI = ramp("#ffffff", "#f6f6f2", "#d4d4ce", "#9c9c96");          // lime plaster: white
const EDO_WOOD = ramp("#d8b080", "#b08852", "#7e5e34", "#50391e");         // a ladle, a trowel's handle, a bucket
const EDO_IRON = ramp("#b8bcc4", "#80868e", "#565c64", "#34383e");         // a trowel's blade, the truncheon
const LACQUER = ramp("#3a3238", "#231e22", "#141114", "#080607");          // a sword's scabbard: black lacquer
const SWORD_WRAP = ramp("#f0e8d0", "#d4c8a8", "#a0946e", "#6c6248");       // the hilt's braid
const EDO_BRONZE = ramp("#f6dc98", "#d8ae58", "#a07a34", "#6a4e1e", { shine: true });      // the mirror
const PINK_LIGHT = ramp("#ffc4d8", "#ff8ab0", "#d05080", "#8a3254");       // Little Sister's flashlight, lent
const GLOW = ramp("#ffffff", "#fff6c8", "#ffe070", "#d8a820", { shine: true });
const EGG = ramp("#fff8ea", "#f2e2c8", "#c8b494", "#90805e");
const SWADDLE = ramp("#f8e8c8", "#e8d0a4", "#b89c70", "#7c6646");          // the baby's wrap
const INK_BLACK_MOUTH = "#141016";                                         // blackened teeth: the inside of the mouth, near black
const EDO_EYE = "#1c1410", EDO_IRIS = "#3a2418", EDO_LID = "#3a2418";

// ---- hair ----
/** A man's hair of the time: the crown shaved from the forehead back (the pate shows the scalp), the hair at the sides
    and the back oiled and drawn up to a knot behind the crown. The rig's `where` gives the hair; the pate and the knot
    are drawn in `extras` (chonmageTop). */
const chonmage = (x, y, z) => {
  if (z < -0.30) return y > -0.62 && y < 0.92;                          // the back: up toward the knot
  if (y > 0.40) return false;                                           // the pate: shaved
  if (z > 0.30) return Math.abs(x) > 0.80 && y > -0.16 && y < 0.38;     // the front: the sideburns only
  return y > -0.30;                                                     // the sides
};
/** The top of a topknot head: the shaved pate (the skin a shade darker), and the knot, a short oiled queue lying forward
    along the top of the head from a tie at the back. `small`: a young man's new topknot (Shinnosuke's). */
function chonmageTop(c, o = {}) {
  const { ball, limb, hp, headPt, onHead, d, hy, parts, spec } = c, hr = d.headR, pate = o.pate || pateOf(spec.skin), mat = o.mat || EDO_HAIR, k = o.small ? 0.78 : 1;
  ball(headPt([0, 0.002, 0]), [hr[0] * 1.015, hr[1] * 1.015, hr[2] * 1.015], pate, { part: parts.HEAD, tone: 1, fn: (ux, uy, uz) => { const q = onHead(ux, uy, uz); return q[1] > 0.42 && q[2] > -0.30 && !(q[2] > 0.30 && q[1] < 0.60) ? undefined : null; } }, hy);
  ball(hp(0, 0.74, -0.74), [0.015 * k, 0.014 * k, 0.015 * k], mat, { part: parts.HAIR }, hy);                                     // the tie
  limb(hp(0, 0.86, -0.62), hp(0, 1.04, 0.30 * k), 0.0095 * k, 0.0080 * k, mat, { part: parts.HAIR, squareEnd: true });            // the queue, forward over the pate
}
/** A married woman's hair: smooth from a high forehead, full at the sides, and a round knot on top toward the back. */
const marumage = hairline({ front: 0.58, temple: 0.40, side: -0.20, back: -0.70, brow: 0.50, temples: 1.10 });
const MARUMAGE_PUFFS = [[0, 0.98, -0.30, 0.44, 0.34, 0.46]];
/** A girl's: tied up in a small knot high at the back; a fringe. */
const girlknot = hairline({ front: 0.30, temple: 0.26, side: -0.10, back: -0.60, brow: 0.55, temples: 1.15 });
const GIRLKNOT_PUFFS = [[0, 1.02, -0.34, 0.30, 0.26, 0.30]];
/** A boy's: cropped all round, with the forelock left long over the brow and a small knot behind. */
const boyhair = hairline({ front: 0.44, temple: 0.42, side: 0.02, back: -0.40, brow: 0.50, temples: 1.10 });
const BOY_PUFFS = [[0, 0.70, 0.86, 0.34, 0.22, 0.20], [0, 0.90, -0.60, 0.22, 0.18, 0.22]];
const EDO_MAN_FACE = { eyes: "plain", eye: EDO_EYE, iris: EDO_IRIS, lid: EDO_LID, brows: EDO_HAIR.tones[2], browW: 3, lip: "#9a5648", nose: [0.85, 0.7, 0.85], noseShade: true, mouthW: 0.20, eyeX: 0.40 };
const EDO_WOMAN_FACE = { eyes: "girl", eye: EDO_EYE, iris: EDO_IRIS, lid: EDO_LID, brows: EDO_HAIR.tones[2], brow: { full: [0, 0, 0] }, lip: "#b85a62", lips: "#d07a80", nose: [0.65, 0.6, 0.7], noseShade: true, mouthW: 0.18, eyeX: 0.42,
  big: { eyeW: 0.44, eyeH: 0.44, lashes: 1, arch: 0.22 } };
const EDO_CHILD_FACE = { eyes: "bright", eye: EDO_EYE, iris: EDO_IRIS, lid: EDO_LID, brows: EDO_HAIR.tones[2], browW: 2, blush: "#f2a890", lip: "#b8605a", nose: [0.55, 0.6, 0.7], mouthW: 0.22, eyeX: 0.43, eyeY: -0.06, mouthY: -0.64, smile: 1, jaw: 0.86, chin: 0.56, chinY: -0.52, chinZ: 0.44 };

// ---- clothes ----
/** A kimono's own lines, drawn on the figure's clothes: the two collar bands crossing on the chest (the wearer's left over
    the right, as the living wear it), the sash (obi) round the waist, with its knot behind, and the sleeves (sode) hanging
    below each forearm. The cloth itself is the figure's `top` and `bottom` (a long sleeved top and a narrow long skirt).
      o.mat      the cloth                      o.eri     the collar bands (the cloth a tone darker if not said; the under-robe's white shows as top.under)
      o.obi      the sash (none: no sash)        o.obiUp, o.obiDown   how far above and below the waist it reaches (a woman's is wide: 0.070 and 0.040; a man's narrow, low: 0.018, 0.026)
      o.knot     "big" (a woman's box knot behind), "small" (a man's), or none
      o.sleeve   how far the sleeves hang below the forearm, in heights (0: none; a working sleeve, tied back, is 0)
      o.jacket   true: a short jacket (a happi, a plasterer's or a sailor's): the collar bands run straight down, open, to its hem */
function kimono(c, o) {
  const { J, limb, ball, trunkAt, wide, deep, d, cloth, under, parts, far } = c, mat = o.mat, eri = o.eri || shifted(mat, 1);
  const lie = { [parts.TORSO]: under, [parts.COLLAR]: under, [parts.PELVIS]: under, [parts.SKIRT]: under, [parts.BELT]: under };
  const hem = o.jacket ? d.hipY - 0.040 : d.waistY + 0.016;
  // the collar bands: the right side first, the left over it; each from beside the neck down across the chest
  for (const sd of [1, -1]) {
    const a = trunkAt(d.shoulderY - 0.012, sd * 0.42, 0.006), b = o.jacket ? trunkAt(hem, sd * 0.16, 0.006) : trunkAt(hem, -sd * 0.10, 0.006);
    limb(a, b, 0.0105, 0.0095, eri, { part: parts.COLLAR, over: lie, bias: cloth * 2.2, squareStart: true, squareEnd: true });
  }
  if (o.obi) {
    const up = o.obiUp ?? 0.070, down = o.obiDown ?? 0.040, rw = wide(d.trunkLow) + 0.007, dw = deep(d.trunkLow) + 0.007;
    limb(J.spine(d.waistY + up), J.spine(d.waistY - down), rw, rw + 0.003, o.obi, { part: parts.BELT, depth: dw / rw, bias: cloth * 1.8, squareStart: true, squareEnd: true });
    if (o.knot === "big") ball(add(J.spine(d.waistY + 0.010), J.torso([0, 0, -(d.trunkLow[1] + 0.034)])), [0.046, 0.034, 0.030], o.obi, { part: parts.EXTRA, bias: cloth * 2 }, c.tw);
    else if (o.knot === "small") ball(add(J.spine(d.waistY - down + 0.012), J.torso([0, 0, -(d.trunkLow[1] + 0.022)])), [0.028, 0.016, 0.018], o.obi, { part: parts.EXTRA, bias: cloth * 2 }, c.tw);
  }
  if (o.sleeve) for (const k of ["R", "L"]) {                             // the sleeve: a flat pocket of cloth hanging from the whole forearm
    const A = J[k], len = o.sleeve, e = mix(A.elbow, A.wrist, 0.10), w = mix(A.elbow, A.wrist, 0.92), r = len * 0.5;
    limb([e[0], e[1] - r - 0.004, e[2]], [w[0], w[1] - r - 0.004, w[2]], r, r * 0.92, far(k, mat), { part: parts.SLEEVE[k], depth: 0.24, squareStart: true, squareEnd: true, bias: cloth });
  }
}
/** A sedge hat (sugegasa): a broad shallow cone, about twice the width of the head, set low so that it shades the brow;
    a thin dark cord from its sides down past the jaw (it ties under the chin, where it is not drawn: at this size a cord
    under the chin reads as a beard). `back`: hanging on the back by its cord, a big disc behind the shoulders, the point out.
    o.r: its radius in heights (0.115, a grown woman's; a child's is set by her head: 1.65 of its half width). */
function sugegasa(c, o = {}) {
  const { J, limb, hp, headPt, d, parts, cloth } = c, hr = d.headR, mat = o.mat || SUGE, r = Math.max(o.r ?? 0.115, hr[0] * 1.65);
  if (o.back) {
    const T = (v) => add(J.sh, J.torso(v)), base = T([0, -0.150, -(d.trunkTop[1] + 0.016)]), apex = T([0, -0.140, -(d.trunkTop[1] + 0.064)]);
    limb(apex, base, 0.004, r, mat, { part: parts.EXTRA3, squareEnd: true, bias: cloth });
    for (const sd of [1, -1]) limb(T([sd * (d.shoulderW - 0.012), -0.034, -(d.trunkTop[1] - 0.004)]), T([sd * 0.026, -0.016, d.trunkTop[1] + 0.004]), 0.0022, 0.0022, SUMI, { part: parts.EXTRA3, over: { [parts.TORSO]: c.under, [parts.COLLAR]: c.under }, bias: cloth * 2.5 });
    return;
  }
  const apex = headPt([0, hr[1] * 1.46, 0.012]), brim = headPt([0, hr[1] * 0.70, 0.022]);
  limb(apex, brim, 0.004, r, mat, { part: parts.HAT, squareEnd: true });
  for (const sd of [1, -1]) limb(hp(sd * 0.96, 0.56, 0.12), hp(sd * 0.74, -0.70, 0.30), 0.0022, 0.0022, SUMI, { part: parts.HAT });      // the cord, down past the jaw
}
/** A head-cloth (a tenugui) tied over the hair, knotted behind: the plasterers' white, a workman's. */
const headcloth = (c, mat = TENUGUI, o = {}) => wear.headcloth(c, { mat, brow: 0.42, nape: 0.70, tails: 0.30, ...o });
/** A towel twisted into a rope and tied round the head (hachimaki): a fisherman's, a plasterer's, a sailor's. */
function hachimaki(c, mat = TENUGUI, at = 0.46) { headband(c, mat, at); }
/** The sleeves tied back with a cord (tasuki): a cord from each shoulder across the back to the other hip and over the chest. */
function tasuki(c, mat = KAKI) { strap(c, mat, 1, 0.0045); strap(c, mat, -1, 0.0045); }
/** A short apron (maekake) tied over the front: Kihei's, scaled like fish. */
function apronOf(c, mat, len = 0.30, fishy = false) {
  const { J, limb, trunkAt, d, cloth, under, parts, S } = c;
  const top = trunkAt(d.waistY - 0.006, 0, 0.010), bottom = add(J.spine(d.hipY - len), J.torso([0, 0, d.pelvisR[2] + 0.018]));
  const w = [d.pelvisR[0] * 0.92, 0.004], r = c.wide(w);
  limb(top, bottom, r * 0.96, r, mat, { part: parts.DRAPE, over: { [parts.TORSO]: under, [parts.PELVIS]: under, [parts.SKIRT]: under, [parts.LEG.R]: under, [parts.LEG.L]: under, [parts.BELT]: under }, bias: cloth * 2.4, depth: c.deep(w) / r, squareStart: true, hem: true,
    fn: fishy && S >= 64 ? (t, nx, ny, x, y) => (((x + ((y >> 1) & 1) * 2) % 4 === 0 && (y % 2 === 0)) ? shifted(mat, 1) : undefined) : null });
}
/** Two swords at the left hip, sheathed, thrust through the sash edge up: the long one and the short one. Never drawn. */
function daisho(c) {
  const { J, limb, ball, trunkAt, d, parts, cloth } = c, hip = trunkAt(d.hipY + 0.036, -1.30, 0.012);
  for (const [len, up, out] of [[0.52, 0.045, 0.000], [0.30, 0.028, 0.016]]) {
    const back = [hip[0] - 0.010, hip[1] - 0.030 - up * 0.3, hip[2] - len * 0.80 - out], front = [hip[0] + 0.006, hip[1] + up + 0.070, hip[2] + len * 0.34 + out];
    limb(back, front, 0.0075, 0.0070, LACQUER, { part: parts.EXTRA2, bias: cloth * 1.5 });                   // the scabbard
    const h0 = front, h1 = [front[0] + 0.004, front[1] + 0.055, front[2] + 0.070 * (len > 0.4 ? 1.3 : 0.8)];
    limb(h0, h1, 0.0085, 0.0075, SWORD_WRAP, { part: parts.EXTRA2, bias: cloth * 1.5 });                    // the hilt
    ball(h0, [0.014, 0.014, 0.006], EDO_IRON, { part: parts.EXTRA2 }, 0);                                    // the guard
  }
}
/** A plasterer's spatter: flecks of lime over the front of the clothes, fixed to the cloth. */
function spatter(c, n = 14) {
  const { sf, P, trunkAt, trunkFacing, d, th, parts, fine } = c;
  if (!fine) return;
  for (let i = 0; i < n; i++) {
    const h = cell(i, 7) % 1000 / 1000, round = (cell(i, 3) % 1000 / 1000 - 0.5) * 2.4;
    const facing = trunkFacing(round);
    if (facing[0] * Math.sin(th) + facing[2] * Math.cos(th) < 0.25) continue;
    const q = P(trunkAt(d.hipY + 0.02 + h * (d.shoulderY - d.hipY - 0.06), round, 0.008));
    sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), SHIKKUI.tones[i % 3 ? 0 : 1], parts.TORSO);
  }
}
/** A held thing between two hands, at the middle of the palms: where it is, and the way from one hand to the other. */
const between2 = (J) => ({ at: mix(J.L.palm, J.R.palm, 0.5), across: unit(sub(J.R.palm, J.L.palm)) });
/** The bronze mirror, held up in both hands: a disc the size of a face, its polished front toward whatever the holder faces. */
function mirror(c) {
  const { J, ball, limb, parts, tw } = c, { at } = between2(J);
  ball(add(at, J.torso([0, 0.034, 0.006])), [0.046, 0.046, 0.007], EDO_BRONZE, { part: parts.HELD }, tw);
  limb(add(at, J.torso([0, -0.012, 0.006])), add(at, J.torso([0, -0.052, 0.006])), 0.006, 0.005, EDO_WOOD, { part: parts.HELD });      // its handle, in the hands
}
/** A baby, wrapped, lying across both forearms: a pale bundle and a small dark head at the holder's left. */
function baby(c) {
  const { J, ball, limb, parts, tw } = c, l = mix(J.L.elbow, J.L.wrist, 0.45), r = mix(J.R.elbow, J.R.wrist, 0.55);
  limb(add(l, [0, 0.030, 0.006]), add(r, [0, 0.034, 0.006]), 0.036, 0.028, SWADDLE, { part: parts.HELD, squareStart: true });
  ball(add(l, [0, 0.060, 0.016]), [0.034, 0.032, 0.034], EDO_SKIN, { part: parts.HELD }, tw);
  ball(add(l, [0, 0.072, 0.010]), [0.035, 0.024, 0.035], EDO_HAIR, { part: parts.HELD, fn: (ux, uy) => (uy > -0.25 ? null : undefined) }, tw);
}
/** An egg, held carefully in two cupped hands. */
function egg(c) { const { J, ball, parts } = c, { at } = between2(J); ball(add(at, [0, 0.012, 0.004]), [0.014, 0.018, 0.014], EGG, { part: parts.HELD }); }
/** Little Sister's pink flashlight, lit, in two hands: a short cylinder with a glowing end. */
function flashlight(c) {
  const { J, limb, ball, parts } = c, { at, across } = between2(J), a = add(at, mul(across, -0.045)), b = add(at, mul(across, 0.050));
  limb(add(a, [0, 0.016, 0]), add(b, [0, 0.016, 0]), 0.013, 0.015, PINK_LIGHT, { part: parts.HELD, squareStart: true });
  ball(add(b, [0, 0.016, 0]), [0.016, 0.016, 0.016], GLOW, { part: parts.HELD });
}
/** A pilgrim's wooden ladle, held up in the right hand: a long handle and a cup at the top. */
function ladle(c, up = true) {
  const { J, limb, ball, parts } = c, g = J.R.palm, dir = up ? unit(add(J.R.hDir, [0, 1.2, 0])) : J.R.hDir;
  const foot = add(g, mul(dir, -0.030)), top = add(g, mul(dir, 0.170));
  limb(foot, top, 0.006, 0.006, EDO_WOOD, { part: parts.HELD });
  ball(add(top, mul(dir, 0.016)), [0.022, 0.016, 0.022], EDO_WOOD, { part: parts.HELD, fn: (ux, uy) => (uy < -0.4 ? shifted(EDO_WOOD, 1) : undefined) });
}
/** A plasterer's trowel in the right hand: a flat blade on a short handle. */
function trowel(c, side = "R") {
  const { J, limb, ball, parts } = c, A = J[side], h = A.palm, dir = A.hDir;
  const grip = add(h, mul(dir, 0.010)), neck = add(h, mul(dir, 0.050)), up = unit(add(mul(dir, 0.3), [0, 1, 0]));
  limb(add(h, mul(dir, -0.020)), grip, 0.007, 0.007, EDO_WOOD, { part: parts.HELD });
  limb(grip, neck, 0.004, 0.004, EDO_IRON, { part: parts.HELD });
  ball(add(neck, mul(up, -0.016)), [0.034, 0.005, 0.024], EDO_IRON, { part: parts.HELD }, 0);
}
/** A bucket of lime hanging from a hand, by its handle. */
function bucket(c, side = "R") {
  const { J, limb, ball, parts } = c, h = J[side].palm, top = add(h, [0, -0.018, 0.004]), bottom = add(h, [0, -0.090, 0.004]);
  limb(add(h, [0, 0.004, 0]), top, 0.003, 0.003, EDO_IRON, { part: parts.HELD });
  limb(top, bottom, 0.036, 0.030, EDO_WOOD, { part: parts.HELD, squareStart: true, squareEnd: true, fn: (t) => (t < 0.10 ? SHIKKUI : undefined) });
}
/** A charcoal sack on the shoulder (Jinsuke lifting one): a dark bulging bale. */
function sack(c) {
  const { J, ball, parts, tw } = c, at = add(J.R.shoulder, J.torso([0.016, 0.070, -0.010]));
  ball(at, [0.062, 0.050, 0.082], SUMI, { part: parts.EXTRA, bias: 2 }, tw + 0.3);
}
/** A clerk's register book in the left hand and a brush in the right. */
function registerBook(c) {
  const { J, limb, ball, parts } = c, L = J.L.palm, R = J.R;
  limb(add(L, J.torso([-0.010, 0.000, -0.030])), add(L, J.torso([-0.010, 0.000, 0.046])), 0.030, 0.030, TENUGUI, { part: parts.HELD, depth: 0.22, squareStart: true, squareEnd: true, bias: 1 });
  limb(add(R.palm, mul(R.hDir, -0.016)), add(R.palm, mul(R.hDir, 0.050)), 0.0035, 0.0030, EDO_WOOD, { part: parts.HELD });
  ball(add(R.palm, mul(R.hDir, 0.054)), [0.005, 0.009, 0.005], EDO_HAIR, { part: parts.HELD });
}
/** A short iron truncheon (a jitte without its tassel) tucked in the sash at the left hip: never drawn out. */
function truncheon(c) {
  const { J, limb, trunkAt, d, parts, cloth } = c, hip = trunkAt(d.hipY + 0.030, -1.10, 0.014);
  limb([hip[0], hip[1] - 0.060, hip[2] + 0.010], [hip[0] + 0.004, hip[1] + 0.090, hip[2] + 0.030], 0.0055, 0.0050, EDO_IRON, { part: parts.EXTRA2, bias: cloth * 1.5 });
}
/** A straw raincoat (mino): a shaggy cape of straw from the shoulders to the hips, over everything, dripping. */
function mino(c) {
  const { J, limb, ball, wide, deep, d, tw, under, cloth, parts, S } = c, T = (v) => add(J.sh, J.torso(v));
  const lie = { [parts.TORSO]: under, [parts.BELT]: under, [parts.COLLAR]: under, [parts.ARM.R]: under, [parts.ARM.L]: under, [parts.SLEEVE.R]: under, [parts.SLEEVE.L]: under, [parts.PELVIS]: under, [parts.SKIRT]: under, [parts.EXTRA2]: under };
  const top = [d.shoulderW + 0.030, d.trunkTop[1] + 0.024], low = [d.shoulderW + 0.064, d.trunkTop[1] + 0.060], r0 = wide(top), r1 = wide(low);
  const streaks = S >= 64 ? (t, nx, ny, x) => ((x + (t * 40 | 0)) % 3 === 0 ? shifted(WARAJI, 1) : undefined) : null;
  limb(T([0, -0.006, 0]), T([0, -0.255, -0.010]), r0, r1, WARAJI, { part: parts.DRAPE, over: lie, bias: cloth * 2.4, depth: deep(top) / r0, squareStart: true, hem: true, fn: streaks });
  ball(T([0, 0.000, -0.006]), [r0 * 0.96, 0.022, deep(top) * 0.96], WARAJI, { part: parts.DRAPE, bias: cloth * 2.4, fn: (ux, uy) => (uy > 0.2 && Math.abs(ux) < 0.40 ? null : undefined) }, tw);      // the collar of it, round the neck (open at the throat)
}
/** A big wicker basket on the back, in its straps. */
function backBasket(c) {
  const { J, ball, limb, d, tw, parts, cloth } = c, T = (v) => add(J.sh, J.torso(v)), at = T([0, -0.150, -(d.trunkTop[1] + 0.090)]);
  ball(at, [0.085, 0.120, 0.075], WICKER, { part: parts.EXTRA, fn: (ux, uy, uz, x, y) => ((x + y) % 3 === 0 ? shifted(WICKER, 1) : undefined) }, tw);
  for (const sd of [1, -1]) limb(T([sd * 0.052, 0.012, 0.0]), T([sd * 0.076, -0.120, d.trunkTop[1] * 0.80]), 0.009, 0.009, KAKI, { part: parts.EXTRA, bias: cloth * 2 });
}
/** A net across the knees of a man sitting mending it: a few crossing lines over the lap. */
function netOnLap(c) {
  const { J, sf, P, parts, pose, S } = c;
  if (!pose.seated || S < 52) return;
  const a = P(add(J.L.knee, [0, 0.030, 0.02])), b = P(add(J.R.knee, [0, 0.030, 0.02])), mid = P(add(mix(J.L.knee, J.R.knee, 0.5), [0, 0.070, -0.06]));
  for (let i = 0; i <= 4; i++) { const t = i / 4, x0 = a[0] + (b[0] - a[0]) * t, y0 = a[1] + (b[1] - a[1]) * t; sf.stroke(x0, y0, mid[0] + (x0 - mid[0]) * 0.2, mid[1] - 2 + (y0 - mid[1]) * 0.2, 1, parts.HELD); }
  sf.stroke(a[0], a[1], b[0], b[1], 1, parts.HELD); sf.stroke(a[0], a[1] + 4, b[0], b[1] + 4, 1, parts.HELD);
}
/** A baby in a sling on the back, its head showing over the right shoulder (O-Tami with the baby). */
function babyOnBack(c) {
  const { J, ball, limb, d, tw, parts, cloth } = c, T = (v) => add(J.sh, J.torso(v)), at = T([0.010, -0.110, -(d.trunkTop[1] + 0.052)]);
  ball(at, [0.060, 0.078, 0.046], SWADDLE, { part: parts.EXTRA }, tw);
  ball(T([0.034, 0.012, -(d.trunkTop[1] + 0.030)]), [0.030, 0.030, 0.030], EDO_SKIN, { part: parts.EXTRA }, tw);
  ball(T([0.034, 0.024, -(d.trunkTop[1] + 0.034)]), [0.031, 0.024, 0.031], EDO_HAIR, { part: parts.EXTRA, fn: (ux, uy) => (uy > -0.2 ? null : undefined) }, tw);
  for (const sd of [1, -1]) limb(T([sd * 0.050, 0.010, -0.004]), T([sd * 0.030, -0.150, d.trunkTop[1] * 0.90]), 0.008, 0.008, KAKI, { part: parts.EXTRA, bias: cloth * 2 });
}
/** A folded pile of clothes held out in both hands (O-Tami's kimonos). */
function foldedClothes(c) {
  const { J, limb, parts } = c, { at, across } = between2(J);
  let y = 0.016;
  for (const m of [EMERALD, INDIGO, PINK]) { limb(add(add(at, mul(across, -0.060)), [0, y, 0.01]), add(add(at, mul(across, 0.060)), [0, y, 0.01]), 0.016, 0.016, m, { part: parts.HELD, depth: 2.2, squareStart: true, squareEnd: true }); y += 0.026; }
}
/** A board of sushi held out in both hands: a flat wooden board with a row of pale pieces on it. */
function sushiBoard(c) {
  const { J, limb, ball, parts } = c, { at, across } = between2(J), a = add(add(at, mul(across, -0.075)), [0, 0.010, 0.02]), b = add(add(at, mul(across, 0.075)), [0, 0.010, 0.02]);
  limb(a, b, 0.040, 0.040, EDO_WOOD, { part: parts.HELD, depth: 0.12, squareStart: true, squareEnd: true });
  for (let i = 0; i < 5; i++) ball(add(mix(a, b, 0.14 + i * 0.18), [0, 0.012, 0]), [0.011, 0.008, 0.016], WHITE, { part: parts.HELD, fn: (ux, uy) => (uy < -0.25 ? EDO_SUN : undefined) });
}

const MIRROR_UP = { R: { hand: [0.034, -0.090, 0.150], bend: [0.8, -0.7, -0.3], grip: true, point: [-0.6, 0.6, 0.5] }, L: { hand: [-0.034, -0.090, 0.150], bend: [-0.8, -0.7, -0.3], grip: true, point: [0.6, 0.6, 0.5] } };      // Mom's hands with the mirror up in both hands
// ---- the family's poses for the act: their own holds and cues (on their pages, so that every outfit has them) ----
/** A hold of both hands cupped round the mouth, the head up: a holler (Little Sister's, Tomezō's shout). */
const hollerHold = (o) => {
  const b = o.base, hr = o.d.headR, p = { ...cloneP(b), mouth: 2, breath: 1, lean: (b.lean || 0) - 0.04, head: { nod: nodOf(b) - 0.16 }, held: "holler" };
  for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * (hr[0] + 0.016), o.sp.chinY - 0.006, hr[2] * 0.62], bend: [sd, -0.7, 0.3], curl: 0.6, point: [-sd * 0.3, 0.9, 0.3] });
  return p;
};
/** Both hands cupped together in front at the chest, something small and precious in them (an egg). */
const eggHold = (o) => {
  const b = o.base, sp = o.sp, p = { ...cloneP(b), lean: (b.lean || 0) + 0.04, head: { nod: nodOf(b) + 0.14 }, held: "egg" };
  for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.024, sp.waist + 0.090, sp.belly + 0.120], bend: [sd * 0.9, -0.5, -0.4], curl: 0.9, point: [-sd * 0.5, 0.5, 0.7], thumb: [0, 1, 0] });
  return p;
};
/** Both hands up at the chest holding the mirror, tilting it a little toward the light. */
const mirrorHold = (o) => {
  const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.04 }, held: "mirror" };
  for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { ...MIRROR_UP[s], hand: [sd * 0.034, -0.090 + (o.seated ? -0.03 : 0), 0.150] });
  return p;
};
/** On hands and knees, to go under something low: the back level, the knees and the toes on the ground behind, the hands
    flat on the ground under the shoulders, the head up to see where she is going. */
const crawlHold = (o) => {
  const b = o.base, d = o.d, L = 1.34, len = (d.upperArm + d.foreArm) * 0.90, p = { ...cloneP(b), lean: L, breath: 0, head: { nod: -0.58 }, held: "crawl" };
  for (const [s, sd] of [["R", 1], ["L", -1]]) {
    p[s] = { ...p[s], leg: [0.06, 0.10], knee: 0.06 + Math.PI / 2 - 0.04, foot: Math.PI + 0.30, footYaw: 0.04, hand: [sd * (d.shoulderW + 0.004), -len * Math.cos(L), len * Math.sin(L)], bend: [sd * 0.8, -0.3, -0.5], flat: true, point: [0, -0.3, 0.95], thumb: [-sd, 0, 0] };
  }
  p.rise = -(d.hipY - d.thigh - d.legR[1] - 0.004);
  return p;
};
/** Up at a high window: both hands over the head gripping the sill, one knee up high, the body stretched. */
const climbHold = (o) => {
  const b = o.base, p = { ...cloneP(b), lean: 0.08, breath: 1, head: { nod: -0.30 }, held: "climb" };
  for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { arm: [2.95, 0.18 + (sd > 0 ? 0.06 : 0)], elbow: 0.06, grip: true });
  p.R = { ...p.R, leg: [1.30, 0.20], knee: 1.90, foot: 0.3 };
  p.L = { ...p.L, leg: [0.05, 0.03], knee: 0.02, foot: 0.9 };
  return p;
};
mom.holds = { ...(mom.holds || {}), mirror: mirrorHold };                                     // PEOPLE-20: hold(true, "mirror") in her own clothes or any outfit
mom.cues = { stand: ["tilt"] };
bigsis.cues = { stand: ["count"] };                                                          // PEOPLE-20: counting on her fingers (fidget("count"), holdable)
lilsis.holds = { ...(lilsis.holds || {}), crawl: crawlHold, climb: climbHold, egg: eggHold, holler: hollerHold };      // PEOPLE-20
lilsis.cues = { stand: ["holler"] };
// (the things in their hands during a hold: drawn by the base pages' extras, which every outfit calls first)
const familyHeld = (c) => { const h = c.pose.held; if (h === "mirror") mirror(c); else if (h === "egg") egg(c); };
{ const was = mom.extras; mom.extras = (c) => { was(c); familyHeld(c); }; }
{ const was = lilsis.extras; lilsis.extras = (c) => { was(c); familyHeld(c); }; }

// ---- the family's clothes: outfits ----
const KYAHAN = AI;                                                        // leg wraps: indigo cotton
const MOM_OBI = ramp("#2a7a5c", "#1c5a44", "#133f30", "#0c2a20");         // Mom's obi: a darker green than her emerald
const BIG_OBI = ramp("#4a4a8c", "#333468", "#232448", "#15162e");          // Big Sister's: a deeper indigo
const LIL_OBI = ramp("#ffd6e2", "#f0a8c0", "#c07a90", "#844c60");          // Little Sister's sash: a pale pink
const TRAVEL = { socks: { mat: KYAHAN, from: 0.06, thick: 0.006 }, shoes: { kind: "sandals", mat: WARAJI, foot: WHITE, sole: shifted(WARAJI, 1) } };      // leg wraps from under the knee, white tabi, straw sandals
/** The outfits, by name: what each does to a lead's page (`how(spec)` gives the changed settings), and what it adds to the
    drawing (`gear(c, spec)`). Every outfit keeps the lead's face, build, stance, walk, gestures, prayer and kneeling. */
const OUTFITS = {
  edo: {
    name: "in Edo travel clothes",
    mom: { top: { mat: EMERALD, sleeves: 2, ease: 0.006, open: 0.012, under: WHITE }, bottom: { kind: "skirt", mat: EMERALD, len: 1.68, flare: 1.04, wrap: [0.55, -0.30], folds: [[0.9, 0.3, 1.6]] }, ...TRAVEL, span: 1.15 },
    bigsis: { top: { mat: INDIGO, sleeves: 2, ease: 0.006, open: 0.012, under: WHITE }, bottom: { kind: "skirt", mat: INDIGO, len: 1.35, flare: 1.04, wrap: [0.55, -0.30] }, ...TRAVEL, socks: { mat: ASAGI, from: 0.06, thick: 0.006 }, span: 1.15 },        // too short for her: it ends at mid-calf, and her leg wraps (pale, not her indigo) show below it
    lilsis: { top: { mat: PINK, sleeves: 2, ease: 0.006, open: 0.010, under: WHITE }, bottom: { kind: "skirt", mat: PINK, len: 1.70, flare: 1.08, wrap: [0.55, -0.30] }, shoes: lilsis.shoes, socks: undefined, span: 1.15 },      // her own yellow boots
    gear(c, who, o = {}) {
      const { pose } = c;
      if (who === "mom") { mom.extras({ ...c, pose: { ...pose, bare: "bag" } }); kimono(c, { mat: EMERALD, obi: MOM_OBI, knot: "big", sleeve: 0.075 }); if (!o.cloth) headcloth(c, TENUGUI, { tails: 0 }); }
      else if (who === "bigsis") { bigsis.extras(c); kimono(c, { mat: INDIGO, obi: BIG_OBI, knot: "big", sleeve: 0.070 }); }
      else { lilHair(c); kimono(c, { mat: PINK, obi: LIL_OBI, obiUp: 0.040, obiDown: 0.028, knot: "small", sleeve: 0.050 }); }
      if (o.cloth) headcloth(c, TENUGUI);                                 // (edo-crew: the plasterer's head-cloth, over the hair, and no hat)
      else if (who !== "lilsis" || o.hat !== "none") sugegasa(c, { back: o.hat === "back", r: who === "lilsis" ? 0.10 : 0.115 });
      if (who !== "mom") familyHeld(c);                                   // (what is in the hands during a hold: the egg, the mirror; Mom's own extras draw hers)
    },
  },
};
/** A lead's page in an outfit: `people[<lead>-<name>]`. `o`: the outfit's state (hat worn or on the back; the crew's cloth; what is in the hands). */
function dressed(who, name, o = {}) {
  const base = { mom, bigsis, lilsis }[who], fit = OUTFITS.edo, label = o.label || fit.name;
  const spec = { ...base, ...fit[who], name: `${base.name}, ${label}`, outfit: name, wears: who, extras(c) { fit.gear(c, who, o); if (o.extra) o.extra(c); } };
  if (o.hold) { spec.hold = o.hold; spec.rest = undefined; spec.gestures = o.gestures || [0, 0, 20, 0]; }
  if (o.fidgets) spec.fidgets = o.fidgets;
  if (o.span) spec.span = o.span;
  return spec;
}
// Mom's hands with the baby: cradled across her front, the left arm under its head; and with the mirror up in both hands.
const CRADLE = { R: { hand: [0.040, -0.170, 0.150], bend: [0.9, -0.6, -0.4], curl: 0.8, point: [-0.7, 0.2, 0.7] }, L: { hand: [-0.070, -0.160, 0.140], bend: [-0.9, -0.6, -0.4], curl: 0.8, point: [0.7, 0.3, 0.65] } };
export const momEdo = dressed("mom", "edo"), momEdoHatback = dressed("mom", "edo-hatback", { hat: "back", label: "in Edo travel clothes, the hat on her back" });
export const momEdoCrew = dressed("mom", "edo-crew", { cloth: true, label: "in Edo clothes and the plasterers' head-cloth" });
export const momEdoBaby = dressed("mom", "edo-baby", { hat: "back", label: "in Edo clothes, with O-Tami's baby in her arms", hold: CRADLE, extra: baby, fidgets: { only: true, stand: ["rockbaby"] }, span: 1.25 });
export const momEdoMirror = dressed("mom", "edo-mirror", { hat: "back", label: "in Edo clothes, the bronze mirror held up", hold: MIRROR_UP, extra: mirror, fidgets: { only: true, stand: ["tilt", "look"] }, span: 1.2 });
export const momEdoCrewMirror = dressed("mom", "edo-crew-mirror", { cloth: true, label: "in the crew's head-cloth, the bronze mirror held up", hold: MIRROR_UP, extra: mirror, fidgets: { only: true, stand: ["tilt", "look"] }, span: 1.2 });
export const bigsisEdo = dressed("bigsis", "edo"), bigsisEdoHatback = dressed("bigsis", "edo-hatback", { hat: "back", label: "in Edo travel clothes, the hat on her back" });
export const bigsisEdoCrew = dressed("bigsis", "edo-crew", { cloth: true, label: "in Edo clothes and the plasterers' head-cloth" });
export const lilsisEdo = dressed("lilsis", "edo"), lilsisEdoHatback = dressed("lilsis", "edo-hatback", { hat: "back", label: "in Edo travel clothes, the hat on her back" });
export const lilsisEdoCrew = dressed("lilsis", "edo-crew", { cloth: true, label: "in Edo clothes and the plasterers' head-cloth" });
/** Little Sister flat on her back on the ground (under the double cherry, the petals landing on her face): the whole figure
    tipped flat (spec.pitch: rig.js, headed), her arms a little out, her eyes open. Her head lies away from the way she faces
    (facing E she lies with her head to the west); her words are put low (crown). A kind, not a hold: lying, she is twice as
    wide as standing, and a hold would be cut off at the picture's edge. In her own clothes and in Edo clothes. */
const LYING = { pitch: -1.52, span: 2.3, tall: 0.6, shadow: 0.001, crown: -0.44, stance: undefined, lean: 0, nod: -0.10, gestures: [0, 0, 8, 0], fidgets: { only: true, stand: ["look"] },
  hold: { R: { arm: [0.12, 0.50], elbow: 0.12, flat: true }, L: { arm: [-0.06, 0.50], elbow: 0.12, flat: true } } };
export const lilsisLying = { ...lilsis, ...LYING, name: "Little Sister, lying on her back", holds: undefined, cues: undefined };
export const lilsisEdoLying = { ...lilsisEdoHatback, ...LYING, name: "Little Sister, in Edo clothes, lying on her back", holds: undefined, cues: undefined };
/** The outfits a lead can be dressed in (g.dress): by lead, the names, each the kind `people[<lead>-<name>]`. */
export const OUTFIT_NAMES = { mom: ["edo", "edo-hatback", "edo-crew", "edo-baby", "edo-mirror", "edo-crew-mirror"], bigsis: ["edo", "edo-hatback", "edo-crew"], lilsis: ["edo", "edo-hatback", "edo-crew", "edo-lying"] };

// ---- the people of 1830 ----
const EDO_MAN = { ...ADULT, headR: [0.056, 0.066, 0.063], shoulderW: 0.098 };
const EDO_WOMAN = { ...WOMAN, headR: [0.056, 0.066, 0.063] };
const H = (cm) => cm / 181;                                               // a height in cm as the rig has it (the family's scale: Dad at 1.0 is about 181 cm)
const workman = (skin, o = {}) => ({
  dim: { ...EDO_MAN, ...(o.dim || {}) }, skin, hair: { mat: EDO_HAIR, bulk: [1.06, 1.0, 1.06], where: chonmage },
  face: { ...EDO_MAN_FACE, ...(o.face || {}) },
  top: { mat: o.jacket || AI, sleeves: 2, ease: 0.006, hem: 0.085, open: 0.040, under: skin, cuffs: undefined },      // a short jacket to mid-thigh, open at the neck
  bottom: { kind: "trousers", mat: o.trousers || AI_DEEP, ease: 0.004 },                                       // tight work trousers (momohiki)
  shoes: { kind: "sandals", mat: WARAJI, sole: shifted(WARAJI, 1) },
  gestures: [0, 1, 0, 8], pace: 150,
});
/** A kimono-wearing townsperson's clothes (a long robe, an obi): the figure's own top and bottom, and the lines kimono() draws. */
const robe = (mat, len = 1.92, o = {}) => ({ top: { mat, sleeves: 2, ease: 0.006, open: o.open ?? 0.034, under: o.under || WHITE }, bottom: { kind: "skirt", mat, len, flare: o.flare ?? 1.03, wrap: [0.55, -0.30], under: mat } });
const WOMAN_EDO = (skin, mat, o = {}) => ({
  dim: { ...EDO_WOMAN, ...(o.dim || {}) }, skin, hair: { mat: EDO_HAIR, bulk: [1.14, 1.04, 1.12], where: marumage, puffs: MARUMAGE_PUFFS },
  face: { ...EDO_WOMAN_FACE, inside: INK_BLACK_MOUTH, ...(o.face || {}) },
  ...robe(mat, o.len ?? 1.80, { open: 0.030 }),
  socks: undefined, shoes: { kind: "sandals", mat: WARAJI, foot: skin, sole: shifted(WARAJI, 1) },
  gestures: o.gestures || [0, 8, 0, 9], pace: o.pace ?? 150,
});
const bowOf = (deep) => ({ bowDeep: deep });

// Kihei, the fishmonger, sixty this tiger year: stocky, big forearms, a towel round his head, work clothes and a scaled
// apron, and over them the red sleeveless vest and the red hood his wife made him wear all year. Few words, big hands.
const KIHEI_VEST = BENI;
function kiheiGear(c) {
  const { J, limb, ball, trunkAt, wide, deep, d, tw, under, cloth, parts, pose, headPt, onHead, hy } = c, T = (v) => add(J.sh, J.torso(v));
  chonmageTop(c);
  // the hood: a soft red cap over the crown and down round the back of the head and the neck
  const hr = d.headR;
  ball(headPt([0, 0.006, -0.004]), [hr[0] * 1.16, hr[1] * 1.12, hr[2] * 1.16], BENI, { part: parts.HAT, fn: (ux, uy, uz) => { const q = onHead(ux, uy, uz); return q[1] > 0.12 || (q[2] < -0.20 && q[1] > -0.70) ? undefined : null; } }, hy);
  apronOf(c, NEZUMI, 0.34, true);
  // the sleeveless vest: a short padded body over the jacket, open down the front, its edges bound
  const lie = { [parts.TORSO]: under, [parts.COLLAR]: under, [parts.BELT]: under, [parts.DRAPE]: under };
  const top = [d.trunkTop[0] + 0.012, d.trunkTop[1] + 0.014], low = [d.trunkLow[0] + 0.018, d.trunkLow[1] + 0.016], r0 = wide(top), r1 = wide(low);
  limb(T([0, -0.030, 0]), J.spine(d.waistY - 0.020), r0, r1, KIHEI_VEST, { part: parts.DRAPE, over: lie, bias: cloth * 2.2, depth: deep(top) / r0, squareStart: true, squareEnd: true,
    fn: (t, nx) => { const round = c.roundAt(nx, c.tw * 0.6); return Math.abs(round) < 0.16 ? null : Math.abs(round) < 0.26 ? shifted(KIHEI_VEST, 1) : undefined; } });      // open down the front, a darker binding at the edges
  if (pose.held === "board") sushiBoard(c);
  void tw; void trunkAt;
}
const KIHEI_PRESS = { R: { hand: [0.050, -0.330, 0.190], bend: [0.9, -0.3, -0.5], flat: true, point: [-0.2, -0.2, 0.95], thumb: [0, 0, 1] }, L: { hand: [-0.050, -0.330, 0.190], bend: [-0.9, -0.3, -0.5], flat: true, point: [0.2, -0.2, 0.95], thumb: [0, 0, 1] } };
const kiheiHolds = {
  /** at his board: cutting: the left hand holding the fish down, the right with the knife, the head down to the work */
  cut: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.22, head: { nod: nodOf(b) + 0.26 }, held: "cut" };
    withArm(p, "L", { hand: [-0.070, -0.300, 0.200], bend: [-0.9, -0.3, -0.5], flat: true, point: [0.2, -0.3, 0.9] });
    withArm(p, "R", { hand: [0.050, -0.290, 0.190], bend: [0.9, -0.3, -0.5], grip: true, point: [-0.9, -0.2, 0.3] }); return p; },
  /** pressing the sushi box: both hands flat on the lid in front of him, his weight on it, the elbows locked */
  press: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.34, breath: 1, head: { nod: nodOf(b) + 0.16 }, held: "press" }; withArm(p, "R", KIHEI_PRESS.R); withArm(p, "L", KIHEI_PRESS.L); return p; },
  /** holding out a board of sushi in both hands, with a small bow of the head */
  board: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) + 0.12 }, held: "board" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.090, -0.220, 0.210], bend: [sd * 0.9, -0.5, -0.4], curl: 0.7, point: [-sd * 0.3, 0.2, 0.9], thumb: [0, 1, 0] }); return p; },
  /** his rare smile: nothing moves but his face */
  smile: (o) => ({ ...cloneP(o.base), smile: 2, head: { nod: nodOf(o.base) + 0.02 }, held: "smile" }),
};
export const kihei = {
  ...workman(EDO_SUN, { dim: { shoulderW: 0.108, trunkTop: [0.114, 0.076], trunkLow: [0.108, 0.080], bellyFwd: 0.010, armR: [0.036, 0.032, 0.022], handR: 0.026, legR: [0.054, 0.035, 0.024] }, jacket: NEZUMI, trousers: AI_DEEP,
    face: { eyes: "heavy", lines: 2, jaw: 0.94, chin: 0.66, brow: { full: [1, 0, 0] } } }),
  name: "Kihei, the fishmonger", height: H(156),
  stance: "folded", lean: 0.03,
  walk: { swing: 0.40, arm: 0.22, elbow: 0.30, lean: 0.05, lift: 0.9 }, pace: 135,
  gestures: [0, 8, 0, 20],                                              // few words: a nod, an open hand, a nod aside
  fidgets: { stand: ["apron", "fold"], not: ["sleeve"] }, holds: kiheiHolds, cues: { stand: ["turnout", "ojigi", "fold"] }, ...bowOf(0.28),
  extras(c) { hachimaki(c, TENUGUI, 0.40); kiheiGear(c); },
};
// O-Tami, his wife: small, quick, teeth blackened and no eyebrows (the baby); sleeves tied back with a cord; a dark apron.
const tamiHolds = {
  clothes: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.10 }, held: "clothes" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.080, -0.210, 0.200], bend: [sd * 0.9, -0.5, -0.4], flat: true, point: [-sd * 0.2, 0.1, 0.95], thumb: [0, 1, 0] }); return p; },
  /** pulling someone in by the sleeve: her right arm out to her right, gripping, her body turned that way, a quick look over her shoulder */
  pull: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, twist: 0.30, head: { nod: nodOf(b), turn: 0.70 }, held: "pull" };
    withArm(p, "R", { hand: [0.200, -0.190, 0.050], bend: [1, -0.3, -0.6], grip: true, point: [1, -0.2, 0.2] }); return p; },
};
export const tami = {
  ...WOMAN_EDO(EDO_SKIN, KAKI, { face: { brows: null, blush: "#eea090", smile: 1 }, len: 1.70, gestures: [0, 9, 1, 8], pace: 165, dim: { shoulderW: 0.080 } }),
  name: "O-Tami, the fishmonger's wife", height: H(146),
  stance: "akimbo", walk: { swing: 0.42, arm: 0.34, elbow: 0.40, lean: 0.06, lift: 1.1, sway: 0.014 },
  fidgets: { stand: ["laugh", "shift", "look", "tasuki"], not: ["sleeve", "scratch"] }, holds: tamiHolds, cues: { stand: ["laugh", "ojigi"] }, ...bowOf(0.30),
  extras(c) { kimono(c, { mat: KAKI, obi: AI_DEEP, knot: "big", sleeve: 0 }); tasuki(c, TENUGUI); apronOf(c, AI, 0.42); if (c.pose.held === "clothes") foldedClothes(c); },
};
export const tamiBaby = { ...tami, name: "O-Tami, with the baby on her back", span: 1.15, fidgets: { stand: ["shift", "look", "jog"], not: ["sleeve", "scratch"] }, extras(c) { tami.extras(c); babyOnBack(c); } };
// Sankichi, their grandson, nine: a boy's short kimono over bare legs, a forelock; he can read.
const sankichiHolds = {
  /** reading the notice board: his right hand up on it, a finger along the lines, his head up and to it */
  read: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.02, head: { nod: nodOf(b) - 0.22 }, held: "read" };
    withArm(p, "R", { hand: [0.060, 0.060, 0.190], bend: [0.8, -0.3, -0.5], finger: true, point: [0.3, 0.2, 0.93] }); return p; },
  /** staring at Little Sister's boots: bent right over, his hands on his knees, his head down */
  stare: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.50, head: { nod: nodOf(b) + 0.30 }, held: "stare" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * (o.d.hipW + 0.026), -(o.d.shoulderY - o.d.hipY) - 0.120, 0.150], bend: [sd * 0.6, -0.3, -0.6], curl: 0.6 }); return p; },
};
export const sankichi = {
  name: "Sankichi, the fishmonger's grandson", height: H(125),
  dim: { ...CHILD, headR: [0.068, 0.079, 0.075] }, skin: EDO_SKIN,
  hair: { mat: EDO_HAIR, bulk: [1.08, 1.04, 1.08], where: boyhair, puffs: BOY_PUFFS, ears: true },
  face: { ...EDO_CHILD_FACE },
  top: { mat: ASAGI, sleeves: 2, ease: 0.006, open: 0.030, under: WHITE }, bottom: { kind: "skirt", mat: ASAGI, len: 1.10, flare: 1.08, wrap: [0.55, -0.30], under: ASAGI },      // a boy's kimono to the knee
  shoes: { kind: "sandals", mat: WARAJI, foot: EDO_SKIN, sole: shifted(WARAJI, 1) },
  stance: "behind", walk: { swing: 0.50, arm: 0.50, elbow: 0.30, lean: 0.08, lift: 1.3, bob: 0.03 }, pace: 175,
  gestures: [0, 10, 0, 11, 4],                                          // he asks and points, in Little Sister's rhythm
  fidgets: { stand: ["shift", "look", "scratch", "hop"] }, holds: sankichiHolds, cues: { stand: ["point", "trace", "hop"] },
  extras(c) { kimono(c, { mat: ASAGI, obi: CHA, obiUp: 0.028, obiDown: 0.024, knot: "small", sleeve: 0.040 }); },
};
// Tokuzō, the headman's clerk: thin, neat, very short-sighted; a brush in one hand, the register book in the other.
const tokuzoHolds = {
  /** peering close at someone: leaning right in from the hips, the head forward, the eyes screwed up (his always are) */
  peerclose: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.30, head: { nod: nodOf(b) - 0.26 }, held: "peerclose" }; return p; },
  /** writing in his book, the brush going, the book held up close to his face */
  writing: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.30 }, held: "writing" };
    withArm(p, "L", { hand: [-0.030, -0.110, 0.150], bend: [-0.9, -0.6, -0.3], flat: true, point: [0.2, 0.3, 0.93], thumb: [1, 0, 0] });
    withArm(p, "R", { hand: [0.010, -0.080, 0.170], bend: [0.9, -0.5, -0.3], grip: true, point: [-0.3, -0.8, 0.5] }); return p; },
};
const TOKUZO_HANDS = { L: { hand: [-0.060, -0.200, 0.120], bend: [-0.9, -0.6, -0.3], flat: true, point: [0.2, 0.3, 0.93], thumb: [1, 0, 0] }, R: { hand: [0.070, -0.250, 0.090], bend: [0.8, -0.5, -0.4], grip: true, point: [-0.3, -0.6, 0.7] } };
export const tokuzo = {
  ...workman(EDO_PALE, { dim: { shoulderW: 0.090, trunkTop: [0.094, 0.060], trunkLow: [0.080, 0.058], armR: [0.027, 0.023, 0.016] }, face: { eyes: "squint", lines: 1, jaw: 0.84, chin: 0.52 } }),
  ...robe(NEZUMI, 1.90, { open: 0.030 }), name: "Tokuzō, the headman's clerk", height: H(157),
  hold: TOKUZO_HANDS, gestures: [0, 0, 20, 0], lean: 0.06,
  walk: { swing: 0.36, arm: 0.10, elbow: 0.60, lean: 0.08, lift: 0.9, bob: 0.02 }, pace: 125,
  fidgets: { only: true, stand: ["shift", "look", "squint"] }, holds: tokuzoHolds, cues: { stand: ["ojigi", "squint"] }, ...bowOf(0.34),
  extras(c) { chonmageTop(c); kimono(c, { mat: NEZUMI, obi: SUMI, obiUp: 0.018, obiDown: 0.026, knot: "small", sleeve: 0.060 }); registerBook(c); },
};
// Gonroku, the captain: weathered, broad, a sailor's short jacket and a towel round his head; he speaks in weather.
export const gonroku = {
  ...workman(EDO_SUN, { dim: { shoulderW: 0.110, trunkTop: [0.116, 0.078], trunkLow: [0.104, 0.074], armR: [0.034, 0.030, 0.021] }, jacket: AI_DEEP, trousers: CHA, face: { eyes: "deep", lines: 2, jaw: 0.96, chin: 0.68, short: { mat: shifted(EDO_SUN, 2), stubble: shifted(EDO_SUN, 2), from: 0.3 } } }),
  name: "Gonroku, the captain", height: H(158),
  stance: "folded", lean: -0.01, walk: { swing: 0.42, arm: 0.26, elbow: 0.30, lean: 0.03, lift: 0.9, sway: 0.020 }, pace: 130,
  gestures: [12, 2, 12, 15, 11],                                         // arms folded; a shrug; waving it away; a finger up (the weather)
  fidgets: { stand: ["fold", "look", "headshake", "grumble"], not: ["sleeve", "neck"] }, cues: { stand: ["headshake", "grumble", "fold"] },
  extras(c) { hachimaki(c, AI, 0.44); chonmageTop(c); kimono(c, { mat: AI_DEEP, obi: CHA, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0, jacket: true }); },
};
// O-Masa, his wife and Kihei's sister: sturdy, decided, teeth blackened; the one person Gonroku obeys.
export const masa = {
  ...WOMAN_EDO(EDO_SUN, AI, { face: { brow: { full: [0, 0, 1] }, lines: 1 }, len: 1.66, gestures: [0, 3, 10, 0], pace: 160, dim: { shoulderW: 0.090, trunkTop: [0.094, 0.066], trunkLow: [0.082, 0.062] } }),
  name: "O-Masa, the captain's wife", height: H(150),
  stance: "akimbo", lean: 0.02, walk: { swing: 0.46, arm: 0.40, elbow: 0.20, lean: 0.09, lift: 1.1 },
  fidgets: { stand: ["shift", "look", "hips2"], not: ["sleeve", "scratch"] }, cues: { stand: ["point", "march"] },
  extras(c) { kimono(c, { mat: AI, obi: KAKI, knot: "big", sleeve: 0 }); tasuki(c, TENUGUI); wear.headcloth(c, { mat: TENUGUI, brow: 0.48, nape: 0.72, tails: 0.2 }); },
};
// Grandmother Sei: small, bent a little, grey hair, a dark plain kimono, no eyebrows, teeth blackened. Found kneeling
// (seiza: `sit.seat` "kneel"), on the mats of the room under the storehouse; she keeps the prayers and the calendar.
const seiHolds = {
  mirror: (o) => mirrorHold(o),
  /** opening the altar's doors: both hands out in front, apart, at the height of the doors' handles */
  doors: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) - 0.08 }, held: "doors" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.120, -0.090, 0.200], bend: [sd * 0.8, -0.6, -0.3], curl: 0.6, point: [sd * 0.2, 0.1, 0.95] }); return p; },
};
export const sei = {
  ...WOMAN_EDO(EDO_SKIN, SUMI, { face: { brows: null, lines: 2, eyes: "heavy", jaw: 0.78, chin: 0.50 }, len: 1.92, gestures: [0, 5, 0, 8], pace: 95, dim: { shoulderW: 0.078, trunkTop: [0.084, 0.064], trunkLow: [0.078, 0.062] } }),
  name: "Grandmother Sei", height: H(140),
  hair: { mat: EDO_GREY, bulk: [1.10, 1.02, 1.08], where: marumage, puffs: [[0, 0.96, -0.36, 0.36, 0.28, 0.38]] },
  seated: "ground", sit: { seat: "kneel", lean: 0.10, nod: 0.08 }, riseMs: 1900, shadow: 0.20, span: 1.12,
  stance: "clasped", lean: 0.14, nod: 0.06, walk: { swing: 0.28, arm: 0.10, elbow: 0.30, lean: 0.14, lift: 0.7 },
  pray: { fold: true, high: 0.62, bow: 0.40, lean: 0.06 },             // kneeling, the hands folded together before her breast, the head well down
  fidgets: { only: true, sit: ["shift", "slownod", "beads"], stand: ["shift", "look"] }, holds: seiHolds, cues: { sit: ["slownod", "tilt"], stand: ["slownod", "tilt", "ojigi"] }, ...bowOf(0.30),
  stood: { pray: { high: 0.55, bow: 0.40 } },
  extras(c) { kimono(c, { mat: SUMI, obi: NEZUMI, obiUp: 0.060, obiDown: 0.034, knot: "big", sleeve: 0.070 }); if (c.pose.held === "mirror") mirror(c); },
};
// Jinsuke, her son, the charcoal-burner: soot in his skin and on his face, work clothes; careful, steady; he kneels and bows deep.
const jinsukeHolds = {
  /** his arms out at his sides in front of his daughter, the palms back, planted */
  shield: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.02, breath: 1, head: { nod: nodOf(b) + 0.02 }, held: "shield" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) { withArm(p, s, { arm: [0.30, 0.95], elbow: 0.10, flat: true, point: [sd * 0.9, -0.3, -0.2], thumb: [0, 0, -1] }); p[s] = { ...p[s], leg: [0.02, 0.18], knee: 0.06 }; } return p; },
  /** a sack lifted onto his right shoulder, both hands steadying it, the knees a little bent under the weight */
  sack: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.04, breath: 1, head: { nod: nodOf(b) + 0.06, turn: -0.20 }, held: "sack" };
    withArm(p, "R", { hand: [0.120, 0.040, 0.040], bend: [1, -0.2, -0.3], curl: 0.8, point: [-0.3, 1, 0.2] }); withArm(p, "L", { hand: [0.040, 0.030, 0.090], bend: [-0.6, -0.4, 0.1], curl: 0.8, point: [0.6, 0.8, 0.2] });
    for (const s of ["R", "L"]) p[s] = { ...p[s], leg: [0.08, 0.06], knee: 0.22 }; return p; },
};
export const jinsuke = {
  ...workman(EDO_SOOT, { dim: { shoulderW: 0.102, armR: [0.032, 0.028, 0.020] }, jacket: CHA, trousers: SUMI, face: { lines: 1, freckles: true, freckle: "#4a4038", jaw: 0.90, chin: 0.60 } }),
  name: "Jinsuke, the charcoal-burner", height: H(157),
  stance: "clasped", lean: 0.04, walk: { swing: 0.40, arm: 0.22, elbow: 0.30, lean: 0.06, lift: 0.9 }, pace: 135,
  gestures: [0, 8, 0, 5], kneel: { lean: 0.06, backLean: 0.02 },
  fidgets: { stand: ["shift", "look", "wipehands"], not: ["sleeve"] }, holds: jinsukeHolds, cues: { stand: ["ojigi", "wipehands"] }, ...bowOf(0.62),
  extras(c) { hachimaki(c, NEZUMI, 0.42); chonmageTop(c); kimono(c, { mat: CHA, obi: NEZUMI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0, jacket: true }); if (c.pose.held === "sack") sack(c); },
};
// O-Rin, his daughter, eight: a plain girl's kimono, her hair tied up; she has never prayed above a whisper.
const orinHolds = {
  /** peeking: turned half away, looking back over her shoulder, a hand up by her cheek */
  peek: (o) => { const b = o.base, p = { ...cloneP(b), twist: -0.30, lean: (b.lean || 0) + 0.04, head: { nod: nodOf(b) + 0.04, turn: 0.75 }, held: "peek" };
    withArm(p, "R", { hand: [0.040, o.sp.chinY - 0.010, o.d.headR[2] + 0.030], bend: [1, -0.6, 0.1], curl: 0.9, point: [-0.3, 0.9, 0.2] }); return p; },
};
export const orin = {
  name: "O-Rin, the charcoal-burner's daughter", height: H(118),
  dim: { ...CHILD, headR: [0.070, 0.081, 0.077], shoulderW: 0.086 }, skin: EDO_SKIN,
  hair: { mat: EDO_HAIR, bulk: [1.10, 1.06, 1.10], where: girlknot, puffs: GIRLKNOT_PUFFS, ears: true },
  face: { ...EDO_CHILD_FACE, eyes: "big", smile: 0.5, blush: "#f0a898" },
  top: { mat: KAKI, sleeves: 2, ease: 0.006, open: 0.024, under: WHITE }, bottom: { kind: "skirt", mat: KAKI, len: 1.78, flare: 1.06, wrap: [0.55, -0.30], under: KAKI },
  shoes: { kind: "sandals", mat: WARAJI, foot: EDO_SKIN, sole: shifted(WARAJI, 1) },
  stance: "clasped", lean: 0.03, walk: { swing: 0.48, arm: 0.40, elbow: 0.30, lean: 0.06, lift: 1.2, bob: 0.02 }, pace: 185,
  gestures: [0, 5, 0, 13], pray: { high: 0.70, bow: 0.30 },
  fidgets: { stand: ["shift", "look", "whisper"], not: ["sleeve", "scratch"] }, holds: orinHolds, cues: { stand: ["whisper", "laugh", "giggle"] },
  extras(c) { kimono(c, { mat: KAKI, obi: ASAGI, obiUp: 0.036, obiDown: 0.026, knot: "big", sleeve: 0.045 }); },
};
// Isuke, the constable's man: a townsman's clothes under a straw raincoat, a sedge hat dripping, the short iron truncheon
// (no tassel) in his sash: never drawn. Wet, hungry, sleepy, polite.
export const isuke = {
  ...workman(EDO_SKIN, { dim: { shoulderW: 0.098 }, jacket: NEZUMI, trousers: AI, face: { eyes: "heavy", jaw: 0.90, chin: 0.58 } }),
  name: "Isuke, the constable's man", height: H(156), span: 1.3,
  stance: "clasped", lean: 0.05, walk: { swing: 0.38, arm: 0.14, elbow: 0.40, lean: 0.10, lift: 0.9 }, pace: 125,
  gestures: [0, 8, 0, 16, 2],                                           // an open hand; wiping his brow (the rain); a shrug
  fidgets: { only: true, stand: ["shiver", "yawn", "look", "shift"] }, holds: { egg: eggHold, writing: tokuzoHolds.writing }, cues: { stand: ["shiver", "yawn", "ojigi", "jot"] }, ...bowOf(0.26),
  extras(c) { chonmageTop(c); kimono(c, { mat: NEZUMI, obi: SUMI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.030, jacket: true }); truncheon(c); mino(c); sugegasa(c, { r: 0.118 }); if (c.pose.held === "egg") egg(c); if (c.pose.held === "writing") registerBook(c); },
};
// Tomezō, the plaster foreman: spattered white head to foot, a towel round his head, a plasterer's jacket, a trowel in his
// hand; cheerful, loud, three hands short. `tomezo` on the ground; `tomezo-ladder` up the ladder (standOn), his left arm through a rung.
const TOMEZO_TROWEL = { R: { hand: [0.090, -0.250, 0.100], bend: [0.7, -0.8, -0.4], grip: true, point: [0.2, -0.3, 0.9] } };
const tomezoHolds = {
  holler: hollerHold,
  /** waving the trowel over his head at nobody */
  wavetrowel: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.04, breath: 1, mouth: 2, head: { nod: nodOf(b) - 0.20 }, held: "wavetrowel" };
    withArm(p, "R", { arm: [2.70, 0.40], elbow: 0.30, grip: true, point: [0.3, 0.9, 0.2] }); return p; },
};
export const tomezo = {
  ...workman(EDO_SUN, { dim: { shoulderW: 0.104, armR: [0.033, 0.029, 0.020] }, jacket: AI, trousers: AI_DEEP, face: { lines: 1, smile: 1, jaw: 0.92, chin: 0.62, brow: { full: [0, -1, -1] } } }),
  name: "Tomezō, the plaster foreman", height: H(159),
  hold: TOMEZO_TROWEL, gestures: [0, 4, 9, 18, 11], lean: 0.02,          // loud: both arms up, hands going, hands wide, a finger up
  walk: { swing: 0.44, arm: 0.30, elbow: 0.30, lean: 0.06, lift: 1.0, bob: 0.02 }, pace: 150,
  fidgets: { stand: ["shift", "look", "laugh", "wipebrow"], not: ["sleeve", "scratch"] }, holds: tomezoHolds, cues: { stand: ["laugh", "wipebrow"] },
  extras(c) { hachimaki(c, TENUGUI, 0.42); chonmageTop(c); kimono(c, { mat: AI, obi: KAKI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0, jacket: true }); spatter(c, 16); trowel(c, "R"); },
};
export const LADDER_RUNG = 137 * CM;                                      // how high Tomezō's feet are on his ladder: PAINT-20D's ladder has eleven rungs 25 cm apart and he
                                                                          // stands on rung 6, 1.37 m up (S/work-20-paintD/ready.md, layout.json `ladder`); his place is the ground under his feet
export const tomezoLadder = {
  ...tomezo, name: "Tomezō, up his ladder", standOn: LADDER_RUNG, span: 1.2, tall: 1.25 + LADDER_RUNG / 0.86,      // (tall: room in the picture for what he stands on, in his own heights)
  hold: { ...TOMEZO_TROWEL, L: { hand: [-0.070, 0.090, 0.150], bend: [-0.8, -0.3, -0.4], grip: true, point: [-0.3, 0.9, 0.3] } },      // the left arm hooked up through a rung
  gestures: [0, 0, 14, 0, 11], fidgets: { only: true, stand: ["look", "laugh", "wavetrowelmove"] }, cues: { stand: ["laugh", "wavetrowelmove"] },
};
// The gate guards: samurai, two swords each, hakama and a jacket, the topknot; one tall and one short. Stiff; they count.
const samurai = (skin, height, name, o = {}) => ({
  name, height, dim: { ...EDO_MAN, ...(o.dim || {}) }, skin, hair: { mat: EDO_HAIR, bulk: [1.06, 1.0, 1.06], where: chonmage },
  face: { ...EDO_MAN_FACE, ...(o.face || {}) },
  top: { mat: o.jacket || SUMI, sleeves: 2, ease: 0.008, open: 0.036, under: WHITE, hem: 0.11 },                  // the jacket (haori), open, to mid-thigh
  bottom: { kind: "skirt", mat: o.hakama || ASAGI, len: 1.88, flare: 1.30, pleats: 7, under: o.hakama || ASAGI },   // hakama: wide and pleated, to the ankle
  socks: { mat: WHITE, from: 0.88, thick: 0.004 }, shoes: { kind: "sandals", mat: WARAJI, foot: WHITE, sole: shifted(WARAJI, 1) },
  stance: o.stance || "behind", lean: 0, walk: { swing: 0.40, arm: 0.12, elbow: 0.20, lean: 0.02, lift: 0.9 }, pace: 140,
  gestures: o.gestures || [0, 17, 0, 10], span: 1.2,
  fidgets: { only: true, stand: ["shift", "look", "tally2"] }, cues: { stand: ["tally2", "ojigi"] }, bowDeep: 0.14,
  extras(c) { chonmageTop(c, { small: !!o.young }); kimono(c, { mat: o.jacket || SUMI, obi: NEZUMI, obiUp: 0.014, obiDown: 0.022, knot: "small", sleeve: 0.080, jacket: true }); daisho(c); if (o.extra) o.extra(c); },
});
export const guard1 = samurai(EDO_SKIN, H(162), "the gate guard (the tall one)", { dim: { shoulderW: 0.104 }, face: { jaw: 0.94, chin: 0.64 } });
export const guard2 = samurai(EDO_SUN, H(150), "the gate guard (the short one)", { dim: { shoulderW: 0.100, trunkTop: [0.110, 0.072] }, face: { eyes: "heavy", jaw: 0.96, chin: 0.68 }, hakama: NEZUMI });
// Shinnosuke, the keep's young warden: nineteen, slight, his topknot new, two swords; he makes up poems when frightened.
// `shinnosuke` on his feet (at the foot of the stairs, at the top of them); `shinnosuke-floor` sat down on the floor.
const shinnosukeHolds = {
  /** holding the pink flashlight in both hands in front of him, lit, like something holy */
  light: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.02, head: { nod: nodOf(b) + 0.14 }, held: "light" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.040, -0.150 + (o.seated ? -0.04 : 0), 0.170], bend: [sd * 0.9, -0.5, -0.4], curl: 0.9, point: [-sd * 0.3, 0.3, 0.9], thumb: [0, 1, 0] }); return p; },
  /** SCENES-20C: the bronze mirror held up in both hands, as Mom holds it (#30's end: she puts it in his hands in the west
      window, and he keeps its light on the hum while the three of them walk in) */
  mirror: (o) => mirrorHold(o),
};
const shinnosukeBase = samurai(EDO_PALE, H(158), "Shinnosuke, the keep's young warden", { dim: { shoulderW: 0.090, trunkTop: [0.094, 0.062], trunkLow: [0.078, 0.058], armR: [0.027, 0.023, 0.016] },
  face: { eyes: "wide", jaw: 0.84, chin: 0.50, brow: { full: [0, -1, -1] }, browUp: 3 }, young: true, stance: "clasped", gestures: [0, 17, 5, 0, 6] });
export const shinnosuke = {
  ...shinnosukeBase, lean: 0.04, kneel: { lean: 0.10, backLean: 0.02 },
  fidgets: { only: true, stand: ["tremble", "look", "count", "shift"] }, holds: shinnosukeHolds, cues: { stand: ["tremble", "count", "ojigi"] }, bowDeep: 0.40,
  extras(c) { shinnosukeBase.extras(c); if (c.pose.held === "light") flashlight(c); else if (c.pose.held === "mirror") mirror(c); },      // (SCENES-20C: and the mirror)
};
export const shinnosukeFloor = {
  ...shinnosuke, name: "Shinnosuke, sat down on the floor", seated: "ground", sit: { seat: "floor", lean: -0.20 }, shadow: 0.22, span: 1.3,
  fidgets: { only: true, sit: ["look", "shift"], stand: ["tremble", "look", "count", "shift"] }, cues: { sit: ["count"], stand: ["tremble", "count", "ojigi"] },
};
// The villagers of Yui: an old man mending a net on the sand, and a woman with a basket on her back.
export const netmender = {
  ...workman(EDO_SUN, { jacket: KAKI, trousers: AI, face: { eyes: "heavy", lines: 2, jaw: 0.90, chin: 0.56, short: { mat: EDO_GREY, stubble: EDO_GREY, from: 0.2 } } }),
  name: "the net-mender", height: H(152), hair: { mat: EDO_GREY, bulk: [1.04, 1.0, 1.04], where: chonmage },
  seated: "ground", sit: { lean: 0.12, nod: 0.10 }, riseMs: 1600, shadow: 0.20,
  rest: { R: { hand: [0.040, -0.300, 0.180], bend: [0.9, -0.4, -0.4], grip: true, point: [-0.6, 0.3, 0.7] }, L: { hand: [-0.060, -0.290, 0.170], bend: [-0.9, -0.4, -0.4], grip: true, point: [0.6, 0.2, 0.7] } },
  gestures: [0, 8, 0, 20], fidgets: { only: true, sit: ["mend", "mend", "look", "shift"], stand: ["look", "shift", "back"] }, cues: { sit: ["mend"] }, stood: { rest: undefined },
  extras(c) { hachimaki(c, AI, 0.40); chonmageTop(c, { mat: EDO_GREY, pate: pateOf(EDO_SUN) }); kimono(c, { mat: KAKI, obi: NEZUMI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0, jacket: true }); netOnLap(c); },
};
export const basketwoman = {
  ...WOMAN_EDO(EDO_SUN, AI, { face: { brow: { full: [0, 0, 0] } }, len: 1.60, gestures: [0, 9, 0, 4], pace: 140, dim: { shoulderW: 0.088 } }),
  name: "a village woman, with a basket on her back", height: H(147), span: 1.25, lean: 0.10,
  stance: "straps", walk: { swing: 0.40, arm: 0.10, elbow: 0.60, lean: 0.12, lift: 0.9 },
  fidgets: { stand: ["shift", "look"], not: ["sleeve", "scratch", "neck"] }, holds: { gasp: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.08, breath: 1, mouth: 2, head: { nod: nodOf(b) - 0.10 }, held: "gasp" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.030, o.sp.chinY - 0.030, o.d.headR[2] + 0.040], bend: [sd, -0.6, 0.1], flat: true, point: [-sd * 0.3, 0.9, 0.3] }); return p; } },
  extras(c) { kimono(c, { mat: AI, obi: KAKI, knot: "big", sleeve: 0 }); tasuki(c, TENUGUI); wear.headcloth(c, { mat: TENUGUI, brow: 0.48, nape: 0.72, tails: 0.2 }); if (!c.spec.dropped) backBasket(c); },
};
export const basketwomanDropped = { ...basketwoman, name: "the village woman, the basket dropped", dropped: true, span: 1.1, lean: 0.02, stance: "clasped", hold: undefined,
  fidgets: { stand: ["shift", "look"], not: ["sleeve", "scratch", "neck"] } };
// The pilgrims of Himeji, setting out for Ise: travel clothes, sedge hats, a wooden ladle held up (the pilgrim's badge, held out for alms).
const pilgrim = (skin, height, mat, name, o = {}) => ({
  ...workman(skin, { jacket: mat, trousers: o.trousers || AI_DEEP, face: o.face || {} }), name, height,
  ...robe(mat, 1.60), ...TRAVEL,
  hold: { R: { hand: [0.090, -0.150, 0.130], bend: [0.7, -0.8, -0.3], grip: true, point: [0, 1, 0.2] } },
  gestures: [0, 0, 20, 0], walk: { swing: 0.44, arm: 0.20, elbow: 0.30, lean: 0.07, lift: 1.0 }, pace: 145, span: 1.2,
  fidgets: { only: true, stand: ["shift", "look"] }, holds: { ladleout: (p) => { const b = p.base, q = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.08 }, held: "ladleout" }; withArm(q, "R", { hand: [0.080, -0.180, 0.230], bend: [0.6, -0.8, -0.2], grip: true, point: [0.1, 0.3, 0.95] }); return q; } },
  extras(c) { chonmageTop(c); kimono(c, { mat, obi: o.obi || CHA, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.050 }); sugegasa(c, { r: 0.112 }); ladle(c, c.pose.held !== "ladleout"); },
});
export const pilgrim1 = pilgrim(EDO_SKIN, H(157), KAKI, "a pilgrim for Ise");
export const pilgrim2 = pilgrim(EDO_SUN, H(154), NEZUMI, "a pilgrim for Ise (the second)", { obi: AI_DEEP, face: { lines: 1 } });
export const pilgrim3 = pilgrim(EDO_PALE, H(150), ASAGI, "a pilgrim for Ise (the third)", { trousers: CHA, face: { eyes: "bright" } });
// Tomezō's crew: white head-cloths, spattered clothes; a bucket, a trowel at a wall, the mixing pole.
const plasterer = (skin, height, name, o = {}) => ({
  ...workman(skin, { jacket: o.jacket || AI, trousers: AI_DEEP, face: o.face || {} }), name, height,
  hold: o.hold, gestures: [0, 8, 0, 9], span: 1.2,
  fidgets: { only: true, stand: ["shift", "look", ...(o.fidgets || [])] }, holds: { trowelwall: (p) => { const b = p.base, q = { ...cloneP(b), lean: (b.lean || 0) - 0.02, head: { nod: nodOf(b) - 0.20 }, held: "trowelwall" }; withArm(q, "R", { hand: [0.080, 0.060, 0.190], bend: [0.8, -0.3, -0.5], grip: true, point: [0.2, 0.9, 0.3] }); return q; },
    mix: (p) => { const b = p.base, q = { ...cloneP(b), lean: (b.lean || 0) + 0.24, head: { nod: nodOf(b) + 0.16 }, held: "mix" }; withArm(q, "R", { hand: [0.060, -0.200, 0.200], bend: [0.9, -0.4, -0.4], grip: true, point: [-0.4, -0.6, 0.7] }); withArm(q, "L", { hand: [-0.020, -0.120, 0.170], bend: [-0.9, -0.5, -0.3], grip: true, point: [0.2, -0.8, 0.5] }); return q; } },
  cues: { stand: ["trowelling", "mixing"] },
  extras(c) { headcloth(c, TENUGUI); kimono(c, { mat: o.jacket || AI, obi: KAKI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0, jacket: true }); spatter(c, 12); const h = c.pose.held; if (o.bucket && h !== "trowelwall" && h !== "mix") bucket(c, "R"); if (h === "trowelwall" || o.trowel) trowel(c, "R"); if (h === "mix") mixPole(c); },
});
/** The pole a plasterer mixes lime with, in both hands, its foot in the tub. */
function mixPole(c) { const { J, limb, parts } = c, top = add(J.L.palm, [0, 0.040, 0]), foot = add(J.R.palm, [0.02, -0.220, 0.06]); limb(top, foot, 0.006, 0.007, EDO_WOOD, { part: parts.HELD }); }
export const plasterer1 = plasterer(EDO_SUN, H(156), "a plasterer (with a bucket)", { bucket: true, hold: { R: { hand: [0.100, -0.330, 0.020], bend: [0.6, -0.9, -0.3], grip: true, point: [0, -1, 0.1] } }, face: { jaw: 0.92 } });
export const plasterer2 = plasterer(EDO_SKIN, H(154), "a plasterer (with a trowel)", { trowel: true, jacket: NEZUMI, hold: { R: { hand: [0.080, -0.240, 0.110], bend: [0.7, -0.8, -0.4], grip: true, point: [0.2, -0.3, 0.9] } }, fidgets: ["trowelling"], face: { eyes: "heavy" } });

// ---- their own small movements (figure.fidget(name); each page's `fidgets` says which are theirs for their life, `cues` what a script plays) ----
addMoves({
  /** a bow from the hips, Japanese: the back straight, the hands flat on the thighs, the eyes down (spec.bowDeep: how far: 0.14 a guard's nod, 0.30 polite, 0.62 Jinsuke's deep one) (holdable) */
  ojigi: { ms: 2200, hold: 0.5, make(o) {
    const b = o.base, deep = o.spec.bowDeep ?? 0.30, p = { ...cloneP(b), lean: (b.lean || 0) + deep, head: { nod: nodOf(b) + deep * 0.5 } };
    for (const s of free(o)) { const sd = s === "R" ? 1 : -1; withArm(p, s, { hand: [sd * (o.d.hipW + 0.030), -(o.d.shoulderY - o.d.hipY) - 0.030, 0.090], bend: [sd * 0.7, -0.3, -0.6], flat: true, point: [0, -0.9, 0.4] }); }
    return [[0, b], [0.30, p], [0.72, p], [1, b]];
  } },
  /** Kihei: turns the sushi box out: both hands take the box in front of him, lift it, turn it over and set it down */
  turnout: { ms: 2600, make(o) {
    const b = o.base, at = (y, z, lean, nod, pt) => { const p = { ...cloneP(b), lean: (b.lean || 0) + lean, head: { nod: nodOf(b) + nod } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.080, y, z], bend: [sd * 0.9, -0.4, -0.4], grip: true, point: pt(sd) }); return p; };
    const down = at(-0.300, 0.200, 0.26, 0.20, (sd) => [-sd * 0.5, -0.5, 0.7]), up = at(-0.180, 0.200, 0.10, 0.16, (sd) => [-sd * 0.5, 0.2, 0.8]), over = at(-0.190, 0.210, 0.12, 0.18, (sd) => [-sd * 0.4, -0.8, 0.4]);
    return [[0, b], [0.20, down], [0.38, up], [0.54, over], [0.72, down], [1, b]];
  } },
  /** Kihei: wipes his big hands on his apron */
  apron: { ms: 2000, make(o) {
    const b = o.base, at = (dy) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.12 } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.040, -(o.d.shoulderY - o.d.hipY) + 0.020 + dy, o.sp.belly + 0.070], bend: [sd * 0.9, -0.4, -0.3], flat: true, point: [0, -0.8, 0.5] }); return p; };
    const a1 = at(0), a2 = at(-0.040);
    return [[0, b], [0.24, a1], [0.40, a2], [0.56, a1], [0.72, a2], [1, b]];
  } },
  /** O-Tami, O-Rin: a laugh behind the hand, the head back a little, then the hand over the mouth (holdable) */
  laugh: { ms: 2400, hold: 0.5, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1, hr = o.d.headR;
    if (o.held(s)) return [[0, b], [1, b]];
    const up = withArm({ ...cloneP(b), mouth: 2, breath: 1, lean: (b.lean || 0) - 0.06, head: { nod: nodOf(b) - 0.22, turn: sd * 0.08 } }, s, { hand: [sd * 0.030, o.sp.chinY - 0.020, hr[2] + 0.050], bend: [sd, -0.6, 0.1], flat: true, point: [-sd * 0.3, 0.9, 0.3] });
    const over = withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.04, head: { nod: nodOf(b) + 0.12, turn: -sd * 0.06 } }, s, { hand: [sd * 0.010, o.sp.chinY - 0.010, hr[2] + 0.046], bend: [sd, -0.6, 0.1], flat: true, point: [-sd * 0.6, 0.5, 0.5] });
    return [[0, b], [0.22, up], [0.46, up], [0.62, over], [0.84, over], [1, b]];
  } },
  /** O-Rin: a giggle she cannot help, both hands over her mouth, her shoulders going */
  giggle: { ms: 2000, make(o) {
    const b = o.base, hr = o.d.headR, at = (br, nod) => { const p = { ...cloneP(b), breath: br, mouth: 1, blink: br > 0.5, head: { nod: nodOf(b) + nod } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.014, o.sp.chinY - 0.010, hr[2] + 0.046], bend: [sd, -0.6, 0.1], flat: true, point: [-sd * 0.6, 0.5, 0.5] }); return p; };
    const g1 = at(1, 0.10), g2 = at(0.2, 0.16);
    return [[0, b], [0.20, g1], [0.32, g2], [0.44, g1], [0.56, g2], [0.68, g1], [1, b]];
  } },
  /** O-Rin: whispers behind her hand, leaning toward whoever is beside her (holdable) */
  whisper: { ms: 2600, hold: 0.5, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1, hr = o.d.headR;
    if (o.held(s)) return [[0, b], [1, b]];
    const p = withArm({ ...cloneP(b), mouth: 1, lean: (b.lean || 0) + 0.06, twist: -sd * 0.16, head: { nod: nodOf(b) + 0.06, turn: -sd * 0.40 } }, s, { hand: [sd * (hr[0] + 0.004), o.sp.chinY + 0.004, hr[2] * 0.62], bend: [sd, -0.7, 0.3], flat: true, point: [-sd * 0.3, 0.9, 0.3], thumb: [0, 0, 1] });
    return [[0, b], [0.26, p], [0.76, p], [1, b]];
  } },
  /** O-Tami: tightens the cord that holds her sleeves back, with a tug at her shoulder */
  tasuki: { ms: 1800, make(o) {
    const b = o.base, at = (dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.08, turn: -0.20 } }, "R", { hand: [-0.040, -0.030 + dy, 0.060], bend: [1, -0.6, -0.1], grip: true, point: [-0.8, 0.4, 0.2] });
    return [[0, b], [0.30, at(0)], [0.44, at(0.024)], [0.58, at(0)], [1, b]];
  } },
  /** O-Tami with the baby: a little jog from the knees, side to side, that never settles it */
  jog: { ms: 2400, make(o) {
    const b = o.base, at = (sw, k) => ({ ...cloneP(b), sway: sw, rise: -k, R: { ...b.R, knee: (b.R.knee || 0) + k * 6 }, L: { ...b.L, knee: (b.L.knee || 0) + k * 6 }, head: { nod: nodOf(b) + 0.02, turn: sw * 6 } });
    return [[0, b], [0.16, at(0.012, 0.010)], [0.33, at(-0.012, 0.002)], [0.50, at(0.012, 0.010)], [0.66, at(-0.012, 0.002)], [0.83, at(0.010, 0.008)], [1, b]];
  } },
  /** Sankichi: a hop from foot to foot, as a boy waits who cannot wait */
  hop: { ms: 1600, make(o) {
    const b = o.base, at = (sd) => ({ ...cloneP(b), sway: sd * 0.020, rise: 0.010, R: { ...b.R, leg: [0.10, 0.04], knee: sd > 0 ? 0.6 : 0.1 }, L: { ...b.L, leg: [0.10, 0.04], knee: sd > 0 ? 0.1 : 0.6 }, head: { nod: nodOf(b) - 0.04 } });
    return [[0, b], [0.25, at(1)], [0.50, b], [0.75, at(-1)], [1, b]];
  } },
  /** Sankichi: a finger along the lines of the board, right to left and down (holdable) */
  trace: { ms: 3000, hold: 0.5, make(o) {
    const b = o.base, at = (dx, dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) - 0.20, turn: dx * 2 } }, "R", { hand: [0.070 + dx, 0.060 + dy, 0.190], bend: [0.8, -0.3, -0.5], finger: true, point: [0.3, 0.2, 0.93] });
    return [[0, b], [0.16, at(0.020, 0)], [0.40, at(-0.030, -0.010)], [0.52, at(0.020, -0.050)], [0.78, at(-0.030, -0.060)], [1, b]];
  } },
  /** Tokuzō: squints closer at whatever is in front of him, leaning in from the hips, and back (holdable) */
  squint: { ms: 2400, hold: 0.5, make(o) {
    const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.28, head: { nod: nodOf(b) - 0.24, turn: 0.06 } };
    return [[0, b], [0.30, p], [0.74, p], [1, b]];
  } },
  /** Tokuzō, Isuke: a note in the book, the brush going, the head down to it */
  jot: { ms: 2400, make(o) {
    const b = o.base, at = (dx) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.28 } };
      withArm(p, "L", { hand: [-0.030, -0.110, 0.150], bend: [-0.9, -0.6, -0.3], flat: true, point: [0.2, 0.3, 0.93], thumb: [1, 0, 0] });
      return withArm(p, "R", { hand: [0.010 + dx, -0.085, 0.172], bend: [0.9, -0.5, -0.3], grip: true, point: [-0.3, -0.8, 0.5] }); };
    return [[0, b], [0.20, at(0)], [0.34, at(-0.016)], [0.48, at(0.004)], [0.62, at(-0.014)], [0.76, at(0.006)], [1, b]];
  } },
  /** Gonroku: a slow shake of the head, no */
  headshake: { ms: 2600, make(o) {
    const b = o.base, at = (t) => ({ ...cloneP(b), head: { nod: nodOf(b) + 0.04, turn: t } });
    return [[0, b], [0.20, at(0.30)], [0.42, at(-0.30)], [0.64, at(0.24)], [0.82, at(-0.16)], [1, b]];
  } },
  /** Gonroku: grumbles at the sky, one hand up and open to it, and lets it fall */
  grumble: { ms: 2600, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    const up = withArm({ ...cloneP(b), mouth: 1, head: { nod: nodOf(b) - 0.18, turn: sd * 0.10 } }, s, { hand: [sd * 0.140, 0.020, 0.120], bend: [sd, -0.6, -0.2], flat: true, point: [sd * 0.3, 0.8, 0.5], thumb: [sd, 0, 0] });
    const down = withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.06 } }, s, { arm: [0.10, 0.20], elbow: 0.20, flat: true });
    return [[0, b], [0.26, up], [0.50, up], [0.68, down], [1, b]];
  } },
  /** O-Masa: her hands go to her hips, and she stands so, a look round */
  hips2: { ms: 3000, hold: 0.4, make(o) {
    const b = o.base, p = cloneP(b); moveKit.STANCES.akimbo(p, o.sp); p.lean = (b.lean || 0) - 0.02; p.head = { nod: nodOf(b) - 0.04, turn: 0.26 };
    const q = cloneP(p); q.head = { nod: nodOf(b) - 0.02, turn: -0.16 };
    return [[0, b], [0.24, p], [0.56, q], [0.80, q], [1, b]];
  } },
  /** O-Masa: two marching steps on the spot, the arms going, the chin up (for a march down the beach, walk her: this is the look of it) */
  march: { ms: 1800, make(o) {
    const b = o.base, at = (s) => { const p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) - 0.06 } }; const sd = s === "R" ? 1 : -1; p[s] = { ...p[s], leg: [0.40, 0.04], knee: 0.90 }; withArm(p, s === "R" ? "L" : "R", { arm: [0.70, 0.12], elbow: 0.6, grip: true }); withArm(p, s, { arm: [-0.40, 0.12], elbow: 0.3, grip: true }); void sd; return p; };
    return [[0, b], [0.25, at("R")], [0.50, b], [0.75, at("L")], [1, b]];
  } },
  /** Grandmother Sei: a slow nod, yes, the eyes shut a moment */
  slownod: { ms: 2800, make(o) {
    const b = o.base, at = (n, bl) => ({ ...cloneP(b), blink: bl, head: { nod: nodOf(b) + n } });
    return [[0, b], [0.30, at(0.22, true)], [0.52, at(0.22, true)], [0.78, at(0.04, false)], [1, b]];
  } },
  /** Grandmother Sei, kneeling: her fingers move over something small in her lap, her head bowed */
  beads: { ms: 3000, make(o) {
    const b = o.base, at = (dx) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.20 } }; withArm(p, "L", { hand: [-0.030, -0.300, 0.150], bend: [-0.9, -0.4, -0.5], curl: 0.8 }); return withArm(p, "R", { hand: [0.010 + dx, -0.290, 0.156], bend: [0.9, -0.4, -0.5], finger: true, point: [-0.6, -0.6, 0.4] }); };
    return [[0, b], [0.20, at(0)], [0.36, at(-0.014)], [0.52, at(0.004)], [0.68, at(-0.012)], [1, b]];
  } },
  /** the mirror, held up: tilted a little this way and that toward the light (Mom in `mom-edo-mirror`, Sei in her hold) (holdable) */
  tilt: { ms: 3200, hold: 0.5, make(o) {
    const b = o.base, held = b.held || (o.spec.outfit && /mirror/.test(o.spec.outfit) ? "mirror" : null);
    if (!held && !(o.spec.hold && o.spec.hold.R && o.spec.hold.L) && !(o.spec.holds && o.spec.holds.mirror)) return [[0, b], [1, b]];
    const at = (dy, turn) => { const p = { ...cloneP(b), held: "mirror", head: { nod: nodOf(b) + 0.06, turn } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.034, -0.090 + (o.seated ? -0.03 : 0) + sd * dy, 0.150 + dy * 0.5], bend: [sd * 0.8, -0.7, -0.3], grip: true, point: [-sd * 0.6, 0.6, 0.5] }); return p; };
    const base = { ...cloneP(b), held: "mirror" };
    return [[0, base], [0.22, at(0.016, 0.10)], [0.46, at(-0.016, -0.08)], [0.70, at(0.012, 0.06)], [1, base]];
  } },
  /** Mom with the baby (`mom-edo-baby`): rocks her, a slow sway from the hips, the head bent to her */
  rockbaby: { ms: 3600, make(o) {
    const b = o.base, at = (sw) => ({ ...cloneP(b), sway: sw, hipTwist: sw * 2, twist: -sw * 2, head: { nod: nodOf(b) + 0.16, turn: -0.20 + sw * 3 } });
    return [[0, b], [0.25, at(0.018)], [0.50, b], [0.75, at(-0.018)], [1, b]];
  } },
  /** Jinsuke: wipes the soot off his hands, one on the other */
  wipehands: { ms: 2000, make(o) {
    const b = o.base, at = (dx) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.14 } }; withArm(p, "L", { hand: [-0.020, -0.230, 0.160], bend: [-0.9, -0.5, -0.4], flat: true, point: [0.9, 0.1, 0.3], thumb: [0, 1, 0] }); return withArm(p, "R", { hand: [0.010 + dx, -0.215, 0.165], bend: [0.9, -0.5, -0.4], curl: 0.7, point: [-0.9, 0.1, 0.3] }); };
    return [[0, b], [0.22, at(0.020)], [0.38, at(-0.020)], [0.54, at(0.020)], [0.70, at(-0.020)], [1, b]];
  } },
  /** Isuke: shivers, wet through: the shoulders up, the arms in, a shudder */
  shiver: { ms: 1800, make(o) {
    const b = o.base, at = (sw) => { const p = { ...cloneP(b), breath: 1, sway: sw, lean: (b.lean || 0) + 0.04, blink: true, head: { nod: nodOf(b) + 0.10, turn: sw * 4 } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [-sd * 0.010, -0.120, o.sp.chest + 0.030], bend: [sd, -0.6, 0.1], curl: 0.9 }); return p; };
    return [[0, b], [0.20, at(0.006)], [0.32, at(-0.006)], [0.44, at(0.006)], [0.56, at(-0.006)], [0.68, at(0.004)], [1, b]];
  } },
  /** Shinnosuke: trembles: a fine shake, the hands clasped tight, the knees not quite steady */
  tremble: { ms: 2200, make(o) {
    const b = o.base, at = (sw, k) => { const p = { ...cloneP(b), sway: sw, breath: 1, blink: k > 0, head: { nod: nodOf(b) + 0.06, turn: sw * 3 } }; for (const [s, sd] of [["R", 1], ["L", -1]]) { withArm(p, s, { hand: [sd * 0.014, -0.160, o.sp.belly + 0.080], bend: [sd * 0.8, -0.5, -0.4], grip: true }); p[s] = { ...p[s], knee: (b[s].knee || 0) + 0.06 + k * 0.04 }; } return p; };
    return [[0, b], [0.14, at(0.005, 0)], [0.26, at(-0.005, 1)], [0.38, at(0.005, 0)], [0.50, at(-0.005, 0)], [0.62, at(0.004, 1)], [0.74, at(-0.004, 0)], [1, b]];
  } },
  /** the gate guards: counting people off with a finger, one, two, three, the head going with it */
  tally2: { ms: 2600, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1;
    if (o.held(s)) return [[0, b], [1, b]];
    const at = (turn, dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.06, turn } }, s, { arm: [0.80 + dy, 0.20 + turn * 0.3], elbow: 0.50, finger: true });
    return [[0, b], [0.18, at(0.30, 0)], [0.34, at(0.30, -0.08)], [0.46, at(0.06, 0)], [0.60, at(0.06, -0.08)], [0.72, at(-0.20, 0)], [0.86, at(-0.20, -0.08)], [1, b]];
  } },
  /** Tomezō: a big laugh, the head back, a hand to his belly */
  wipebrow: { ms: 2000, make(o) {
    const b = o.base, s = freeOf(o), sd = s === "R" ? 1 : -1, hr = o.d.headR;
    if (o.held(s)) return [[0, b], [1, b]];
    const at = (dx) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.06 } }, s, { hand: [sd * (0.012 + dx), o.sp.headY + hr[1] * 0.42, hr[2] + 0.030], bend: [sd, -0.3, 0.3], curl: 0.7, point: [-sd, 0.2, 0] });
    return [[0, b], [0.30, at(0)], [0.46, at(0.020)], [0.62, at(0)], [1, b]];
  } },
  /** Tomezō, up the ladder: the trowel waved over his head, twice (his life up there) */
  wavetrowelmove: { ms: 2200, make(o) {
    const b = o.base, at = (a) => withArm({ ...cloneP(b), mouth: 2, head: { nod: nodOf(b) - 0.16, turn: a } }, "R", { arm: [2.60, 0.40 + a], elbow: 0.30, grip: true, point: [0.3, 0.9, 0.2] });
    return [[0, b], [0.20, at(0.16)], [0.36, at(-0.16)], [0.52, at(0.16)], [0.68, at(-0.16)], [1, b]];
  } },
  /** the net-mender, sitting: his hands work along the net across his knees */
  mend: { ms: 2800, make(o) {
    const b = o.base, at = (dx) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.22 } }; withArm(p, "L", { hand: [-0.060 + dx, -0.290, 0.170], bend: [-0.9, -0.4, -0.4], grip: true, point: [0.6, 0.2, 0.7] }); return withArm(p, "R", { hand: [0.040 - dx, -0.300 + Math.abs(dx), 0.180], bend: [0.9, -0.4, -0.4], grip: true, point: [-0.6, 0.3, 0.7] }); };
    return [[0, b], [0.18, at(0.020)], [0.34, at(-0.016)], [0.50, at(0.020)], [0.66, at(-0.016)], [0.82, at(0.010)], [1, b]];
  } },
  /** a plasterer: the trowel goes up and across the wall in front of him, twice (holdable) */
  trowelling: { ms: 2800, hold: 0.5, make(o) {
    const b = o.base, at = (dx, dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) - 0.18 + dy } }, "R", { hand: [0.060 + dx, 0.060 + dy, 0.190], bend: [0.8, -0.3, -0.5], grip: true, point: [0.2, 0.9, 0.3] });
    return [[0, b], [0.16, at(-0.030, -0.060)], [0.34, at(0.040, 0.030)], [0.50, at(-0.030, -0.040)], [0.68, at(0.040, 0.040)], [1, b]];
  } },
  /** a plasterer: mixes the lime, both hands on the pole, round and round */
  mixing: { ms: 3000, make(o) {
    const b = o.base, at = (dx, dz) => { const p = { ...cloneP(b), lean: (b.lean || 0) + 0.24, head: { nod: nodOf(b) + 0.16 } }; withArm(p, "R", { hand: [0.060 + dx, -0.200, 0.200 + dz], bend: [0.9, -0.4, -0.4], grip: true, point: [-0.4, -0.6, 0.7] }); return withArm(p, "L", { hand: [-0.020 + dx, -0.120, 0.170 + dz], bend: [-0.9, -0.5, -0.3], grip: true, point: [0.2, -0.8, 0.5] }); };
    return [[0, b], [0.16, at(0.030, 0)], [0.32, at(0, 0.030)], [0.48, at(-0.030, 0)], [0.64, at(0, -0.030)], [0.80, at(0.030, 0)], [1, b]];
  } },
  /** everyone's: a holler, both hands cupped to the mouth (Little Sister's cue; the hold is `holler`) */
  holler: { ms: 2400, hold: 0.5, make(o) { const p = hollerHold(o); return [[0, o.base], [0.24, p], [0.76, p], [1, o.base]]; } },
});

// =====================================================================================
// PEOPLE-21A (round twenty-one): Act Six made bigger: the people of the Satta Pass, the ship and Osaka; the boy puppet
// =====================================================================================
// The road west (S/briefs/out/edo2-design.md, section 6): at the foot of the pass, O-Kuni's teahouse, the two palanquin
// bearers, the Toyama medicine peddler with his willow trunks, the basket-hatted flute monk and the relay courier; at the
// top, the woodcutter who never looks at Fuji, the widow with a pass and her old manservant; on the ship, the navigator,
// the bosun, the purser, the boy cook and two sailors (the master is round twenty's Gonroku); in Osaka, the rice dealer's
// wife and her husband, the freeloader, the town magistrate's dōshin and his thief-taker, the two broadsheet sellers, the
// printer, the chief puppeteer, the chanter, the shamisen player and four pilgrims in the alms line; and the boy puppet,
// a carved doll of about 0.9 m, worked by three. Heights from ROUND-21.md: men about 1.56 m, women 1.46 m, Kōta (12)
// 1.38 m, the ladle boy 1.10 m, the doll 0.9 m. Everyone is our own: nobody's likeness. All of it is inside one block
// (PEOPLE_21A, below), so that no name here meets another section's; the table at the end takes `...PEOPLE_21A`.
// Facts for clothes and hair: round twenty's (facts-edo item 26, facts-edo-2 items 5, 12, 13) and this round's
// (facts-21a item 3: bearers, couriers, the Toyama peddlers' willow trunks, the komusō's basket hat; item 6: the crew;
// facts-21b items 2, 3, 6: pilgrims' ladles, the puppet theatre, the magistrate's men and their jitte). What the files do
// not say is invented, and docs/DESIGN.md section 4 and PEOPLE-21A's ready.md say which.
// How a script calls each pose is in docs/DESIGN.md, section 4 ("Japan, 1830: the road west").
const PEOPLE_21A = (() => {
  // ---- materials ----
  const SHIRO = TENUGUI;                                                  // white cotton: loincloths, under-collars
  const KOGECHA = ramp("#9a7a5c", "#74583e", "#523c28", "#34261a");        // a dark brown: the purser's, the freeloader's
  const UGUISU = ramp("#b4b47c", "#8e8e56", "#686838", "#444424");         // a dull olive: the bearers', the woodcutter's jacket
  const FUJINEZU = ramp("#b8aac0", "#94849c", "#6c5e74", "#463c4c");       // a greyed wisteria: the widow's travel kimono
  const KACHI = ramp("#6c7aa0", "#46527a", "#2e3858", "#1c223a");          // a dark navy: the courier's, the sailors'
  const SABI = ramp("#a8b49c", "#7e8c72", "#5a664e", "#3a4232");           // a grey green: the chanter's and the shamisen player's formal vests
  const TOBI = ramp("#c88c74", "#a4644c", "#784430", "#4e2a1e");           // a red brown: the thief-taker's jacket
  const SHIBA = ramp("#c0a47a", "#967a50", "#6c5634", "#46381e");          // brushwood: dead branches, grey-brown
  const SHIBA_DARK = shifted(SHIBA, 1);
  const TENGAI_REED = ramp("#e4cc90", "#c4a462", "#92743c", "#5e4a24");    // the komusō's basket hat: woven reed
  const TAKE = ramp("#ece0a0", "#ccb86c", "#98843e", "#625424");           // bamboo: the flute, a ladle's handle
  const FUROSHIKI = ramp("#78ac8c", "#4a8466", "#326048", "#1e3e2e");      // the peddler's wrapping cloth: a deep green
  const FURO_KNOT = shifted(FUROSHIKI, 1);
  const YANAGI = ramp("#f2e2b4", "#d8c48a", "#a8925c", "#706038");         // willow trunks: pale, plaited
  const WASHI = ramp("#fffbf0", "#f2eada", "#cfc4a8", "#9a8e72");          // paper
  const BEROAI = ramp("#86b0ff", "#3e72dc", "#2648a4", "#152a68");         // Berlin blue: the new ink
  const TSUGE = ramp("#f6dc94", "#deba62", "#aa8a3a", "#6e5822");          // boxwood: a comb
  const HINOKI = ramp("#f6e8c8", "#e6cea0", "#b69c6e", "#7c6848");         // pale wood: a rice paddle, a pot lid, a baren's rim
  const LID_KNOB = shifted(HINOKI, 2);
  const UCHIWA = ramp("#f4ecd8", "#e2d4b4", "#b4a484", "#7c7058");          // a round paper fan
  const SHITAN = ramp("#946448", "#6c4630", "#4a2e1e", "#2c1a10");         // dark wood: the shamisen's neck, the abacus
  const NEKO = ramp("#fffcf4", "#f4eee0", "#d4cab4", "#a09680");           // the shamisen's skin: white
  const SHU = ramp("#ff8a70", "#e85a40", "#b23e2c", "#76261a");            // vermilion: a label, the dōshin's tassel
  const MOLE = "#5a3a2c";                                                 // O-Shige's mole, by her right eye
  const OLD_SKIN = ramp("#f2d2b4", "#e0b28e", "#b0805e", "#76523a");        // a face grown old indoors (the widow, the chanter)
  const BIG_SKIN = EDO_SUN;
  // the doll: a carved and painted head, hands and feet (white, as a puppet's are), black lacquered hair, a boy's clothes
  const DOLL_SKIN = ramp("#fffaf0", "#f6ead6", "#d8c2a2", "#a28a68");
  const DOLL_HAIR = ramp("#4c4856", "#25222c", "#15131a", "#08070a", { shine: true });
  const DOLL_KIMONO = ramp("#f4987a", "#dc5a40", "#a83c2c", "#6e241a");    // a bright madder red: a boy in a play, seen from the back of the house
  const DOLL_OBI = ramp("#5e8a6c", "#3c6a4e", "#284a36", "#182e22");
  const DOLL_EYE = "#120c0a";
  const KESA = ramp("#e8c88a", "#c8a058", "#987434", "#64481e");                            // the komusō's surplice: a dull gold
  const BEADS = ramp("#3a3030", "#241c1c", "#161010", "#0a0606");                           // abacus beads
  const IVORY = ramp("#fff6dc", "#eedcae", "#bca67a", "#86744c");                           // a plectrum
  const SAZAE = ramp("#c8a088", "#9c7058", "#6c4a3a", "#442c22");                           // a turban shell
  const SAZAE_LIP = ramp("#f4e2c8", "#dcc2a0", "#a88c6a", "#705a42");                       // its lip
  const TOYAMA_INK = ramp("#8aa0e0", "#5a72c0", "#3c5090", "#24345e");                      // a cheap print's blue
  const OILPAPER = ramp("#e8d4a4", "#ccb47c", "#9c8452", "#685834");                        // a pass in oiled paper
  const COPPER = ramp("#d8b070", "#b08848", "#7c5e2c", "#4e3a18");                          // a one-mon coin
  const SUMI_INK = ramp("#6c6c74", "#46464e", "#2c2c32", "#18181c");                        // printed black
  const BAREN_PAD = ramp("#c8a874", "#a8884e", "#7c6232", "#50401e");                       // a baren's pad
  const SUGE_OLD = shifted(SUGE, 1);                                                        // an old sedge hat

  // ---- small helpers ----
  const T = (c, v) => add(c.J.sh, c.J.torso(v));                            // a point in the torso's space (from the middle of the shoulders)
  const back = (c) => c.d.trunkTop[1];
  /** A thin line of cloth, a cord or a stick between two points. */
  const rod = (c, a, b, r, mat, part = c.parts.HELD, o = {}) => c.limb(a, b, r, r * (o.taper ?? 1), mat, { part, ...o });
  /** A box (a trunk, a letter box, a lacquered box) standing upright at `at` (a point), [half width, half height, half
      depth] in heights, turned with the body: square at top and bottom, its sides narrowing as it turns away, `fn` its
      cloth or its bands (t from its foot to its top). */
  const boxAt = (c, at, half, mat, part, fn = null) => {
    const r = c.wide([half[0], half[2]]), up = c.J.torso([0, 1, 0]);
    c.limb(add(at, mul(up, -half[1])), add(at, mul(up, half[1])), r, r, mat, { part, depth: c.deep([half[0], half[2]]) / r, squareStart: true, squareEnd: true, fn });
  };
  /** Short tight work breeches to above the knee, under a short jacket (a bearer's, a runner's, a sailor's): dark cotton.
      (Their loincloths would be truer, and read at this size as white underwear: the breeches are the game's choice.) */
  const BREECHES = (mat = AI_DEEP) => ({ kind: "shorts", mat, len: 0.78 });
  /** Bare legs below the breeches, and straw sandals. */
  const BARELEGS = (skin, mat) => ({ bottom: BREECHES(mat), socks: undefined, shoes: { kind: "sandals", mat: WARAJI, foot: skin, sole: shifted(WARAJI, 1) } });
  /** Leg wraps over white tabi in straw sandals (a traveller's: round twenty's TRAVEL), in a colour of one's own. */
  const wraps = (mat = KYAHAN) => ({ socks: { mat, from: 0.06, thick: 0.006 }, shoes: { kind: "sandals", mat: WARAJI, foot: WHITE, sole: shifted(WARAJI, 1) } });
  const BARE = { socks: undefined, shoes: { kind: "bare" } };

  /** A sedge hat with a pilgrims' group's mark painted on its front (facts-edo item 26: a hat marked with the group's sign):
      a dark ring and a stroke, our own sign. */
  function markedHat(c, o = {}) {
    sugegasa(c, o);
    if (o.back || !c.fine) return;
    const { sf, P, hp, th, hy } = c, ang = th + hy;
    if (Math.cos(ang) < 0.35) return;                                   // (the front of the hat, seen from the front)
    const q = P(hp(0, 1.04, 0.62)), x = Math.round(q[0] - 0.5), y = Math.round(q[1] - 0.5), ink = SUMI.tones[2];
    for (const [i, k] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) sf.dot(x + i, y + k, ink, c.parts.HAT);
  }

  /** The komusō's basket hat (tengai): a deep cylinder of woven reed over the whole head, down to the shoulders, a little
      wider at the bottom, its top domed; the weave a lattice of darker strands. Nothing of the face shows. */
  function tengai(c) {
    const { limb, ball, hp, headPt, d, hy, parts, fine } = c, hr = d.headR;
    const weave = fine ? (t, nx, ny, x, y) => ((x + y) % 4 === 0 || (x - y + 64) % 4 === 0 ? shifted(TENGAI_REED, 1) : undefined) : null;
    const top = headPt([0, hr[1] * 1.30, -0.004]), low = headPt([0, -hr[1] * 1.55, 0.004]);
    limb(top, low, hr[0] * 1.42, hr[0] * 1.62, TENGAI_REED, { part: parts.HAT, squareEnd: true, depth: 1.05, fn: weave });
    ball(top, [hr[0] * 1.42, hr[1] * 0.42, hr[2] * 1.42], TENGAI_REED, { part: parts.HAT, fn: weave ? (ux, uy, uz, x, y) => weave(0, 0, 0, x, y) : null }, hy);
    void hp;
  }
  /** A bamboo flute (shakuhachi) held in both hands, its top end under the hat at the mouth, its foot down and forward. */
  function shakuhachi(c, playing = true) {
    const { J, hp, parts } = c;
    if (playing) {
      const top = hp(0, -0.72, 1.18), foot = add(mix(J.R.palm, J.L.palm, 0.5), J.torso([0, -0.130, 0.090]));
      rod(c, top, foot, 0.0105, TAKE, parts.HELD, { taper: 1.25 });
      for (const t of [0.30, 0.62]) { const n = mix(top, foot, t); c.ball(n, [0.012, 0.006, 0.012], shifted(TAKE, 1), { part: parts.HELD }); }      // the nodes
    } else {                                                            // carried: down in the right hand, along the leg
      const g = J.R.palm, dir = unit(add(J.R.hDir, [0, -0.2, 0]));
      rod(c, add(g, mul(dir, -0.10)), add(g, mul(dir, 0.20)), 0.0105, TAKE, parts.HELD, { taper: 1.2 });
    }
  }
  /** The komusō's small surplice (rakusu) on the chest from a band round the neck, and the box hung at his chest. */
  function rakusu(c) {
    const { J, limb, d, cloth, under, parts } = c;
    const lie = { [parts.TORSO]: under, [parts.COLLAR]: under };
    limb(T(c, [0, -0.090, back(c) + 0.004]), T(c, [0, -0.150, back(c) + 0.010]), 0.040, 0.044, KESA, { part: parts.DRAPE, over: lie, bias: cloth * 2.4, depth: 0.18, squareStart: true, squareEnd: true });
    for (const sd of [1, -1]) limb(T(c, [sd * 0.030, 0.006, back(c) * 0.5]), T(c, [sd * 0.036, -0.090, back(c) + 0.004]), 0.0035, 0.0035, SUMI, { part: parts.DRAPE, over: lie, bias: cloth * 2.4 });
    void J; void d;
  }

  /** The relay courier's letter box on its pole, on his right shoulder: the pole lies on the shoulder and rises toward the
      front, his right hand on it before the shoulder, the box (black lacquer, a vermilion label) hung from its front end. */
  const COURIER_POLE = [[0.092, 0.020, -0.200], [0.092, 0.110, 0.360]];
  function letterbox(c) {
    const { parts } = c, rear = T(c, COURIER_POLE[0]), front = T(c, COURIER_POLE[1]);
    rod(c, rear, front, 0.0065, TAKE, parts.EXTRA);
    rod(c, add(front, c.J.torso([0, -0.004, -0.010])), add(front, c.J.torso([0, -0.030, -0.010])), 0.003, ROPE, parts.EXTRA2);
    boxAt(c, add(front, c.J.torso([0, -0.070, -0.010])), [0.042, 0.040, 0.052], LACQUER, parts.EXTRA2, (t) => (Math.abs(t - 0.5) < 0.12 ? SHU : undefined));
  }

  /** A woodcutter's load: a tall bundle of brushwood tied with two ropes on a frame on his back, standing up past his head,
      the ends of the sticks spreading out at the top; the frame's foot and its shoulder ropes. */
  function brushwood(c) {
    const { limb, d, parts, cloth, fine } = c, b = back(c), z = -(b + 0.075);
    const sticks = fine ? (t, nx) => (Math.abs(t - 0.30) < 0.035 || Math.abs(t - 0.72) < 0.035 ? ROPE : (Math.floor((nx + 1) * 5) % 2 ? SHIBA_DARK : undefined)) : null;
    const r = c.wide([0.070, 0.055]);
    limb(T(c, [0, -0.250, z]), T(c, [0, 0.260, z - 0.012]), r, r * 1.10, SHIBA, { part: parts.EXTRA, depth: c.deep([0.070, 0.055]) / r, squareStart: true, squareEnd: true, fn: sticks });
    for (const [dx, up, spread] of [[-0.050, 0.34, -0.050], [-0.020, 0.36, -0.016], [0.010, 0.37, 0.010], [0.040, 0.35, 0.040], [0.062, 0.32, 0.070], [-0.064, 0.31, -0.074]])
      limb(T(c, [dx * 0.8, 0.240, z - 0.012]), T(c, [dx + spread, up, z - 0.016]), 0.0045, 0.0030, SHIBA_DARK, { part: parts.EXTRA });
    limb(T(c, [-0.080, -0.250, z + 0.030]), T(c, [0.080, -0.250, z + 0.030]), 0.010, 0.010, EDO_WOOD, { part: parts.EXTRA, squareStart: true, squareEnd: true });      // the frame's foot
    for (const sd of [1, -1]) limb(T(c, [sd * 0.050, 0.012, 0.0]), T(c, [sd * 0.070, -0.110, d.trunkTop[1] * 0.85]), 0.008, 0.008, ROPE, { part: parts.EXTRA, bias: cloth * 2 });
  }
  /** O-Shige's box carried on a pole on the shoulder (Kyūzō's): the pole over his right shoulder, his right hand on its
      front end before him, the black lacquered box hanging from its back end behind him. */
  const KYUZO_POLE = [[0.092, 0.000, -0.400], [0.092, 0.050, 0.100]];
  function poleBox(c) {
    const { parts } = c, rear = T(c, KYUZO_POLE[0]), front = T(c, KYUZO_POLE[1]);
    rod(c, rear, front, 0.0065, EDO_WOOD, parts.EXTRA);
    rod(c, add(rear, c.J.torso([0, -0.004, 0.020])), add(rear, c.J.torso([0, -0.040, 0.020])), 0.003, ROPE, parts.EXTRA2);
    boxAt(c, add(rear, c.J.torso([0, -0.095, 0.020])), [0.062, 0.055, 0.050], LACQUER, parts.EXTRA2, (t) => (Math.abs(t - 0.78) < 0.06 ? EDO_IRON : undefined));
  }
  /** The Toyama peddler's load: the willow trunks, five tiers, wrapped in a big green cloth and carried on the back (the top
      tier's pale willow showing), the cloth's ends knotted over the chest (facts-21a item 3: the five-tier trunk, the
      ledger and the purse on top). */
  function trunks(c) {
    const { J, ball, limb, d, tw, parts, cloth } = c, b = back(c), half = [0.100, 0.165, 0.072];
    boxAt(c, T(c, [0, -0.095, -(b + half[2] + 0.004)]), half, FUROSHIKI, parts.EXTRA, c.fine ? (t) => (t > 0.83 ? YANAGI : (t * 5) % 1 < 0.10 ? shifted(FUROSHIKI, 1) : undefined) : null);
    for (const sd of [1, -1]) limb(T(c, [sd * 0.060, 0.012, -0.006]), T(c, [-sd * 0.030, -0.090, d.trunkTop[1] + 0.010]), 0.010, 0.012, FUROSHIKI, { part: parts.DRAPE, over: { [parts.TORSO]: c.under, [parts.COLLAR]: c.under }, bias: cloth * 2.2 });
    ball(T(c, [0, -0.096, d.trunkTop[1] + 0.016]), [0.020, 0.016, 0.014], FURO_KNOT, { part: parts.DRAPE, bias: cloth * 2.4 }, tw);      // the knot
    void J;
  }
  /** A peddler's ledger (or anyone's book) open in both hands in front of the chest. */
  function openBook(c, mat = WASHI) {
    const { J, limb, parts } = c, { at, across } = between2(J), a = add(at, mul(across, -0.050)), b2 = add(at, mul(across, 0.050));
    limb(add(a, [0, 0.016, 0.010]), add(b2, [0, 0.016, 0.010]), 0.030, 0.030, mat, { part: parts.HELD, depth: 0.10, squareStart: true, squareEnd: true, fn: (t) => (Math.abs(t - 0.5) < 0.04 ? shifted(mat, 2) : undefined) });
  }
  /** A small woodblock print held out in the right hand (a sheet: a coloured figure on it). */
  function heldSheet(c, side = "R", mat = WASHI, picture = KAKI) {
    const { J, limb, parts } = c, g = J[side].palm, up = unit(add(J[side].hDir, [0, 0.9, 0]));
    limb(add(g, mul(up, 0.000)), add(g, mul(up, 0.090)), 0.030, 0.030, mat, { part: parts.HELD, depth: 0.08, squareStart: true, squareEnd: true, fn: picture ? (t, nx) => (t > 0.3 && t < 0.8 && Math.abs(nx) < 0.4 ? picture : undefined) : null });
  }
  /** An abacus: a dark wooden frame with rows of beads, held in the left hand. */
  function abacus(c, side = "L") {
    const { J, limb, parts } = c, g = J[side].palm, across = side === "L" ? J.torso([1, 0, 0]) : J.torso([-1, 0, 0]);
    const a = add(g, mul(across, -0.010)), b2 = add(g, mul(across, 0.150));
    limb(a, b2, 0.030, 0.030, SHITAN, { part: parts.HELD, depth: 0.18, squareStart: true, squareEnd: true, fn: (t, nx) => (Math.abs(nx) < 0.75 && ((t * 12) | 0) % 2 === 0 ? BEADS : undefined) });
  }
  /** A round wooden pot lid with a knob, in the hands (Kōta lifting it to look): its near edge lifted, so that it tilts
      toward him and shows its face from the side as well as from the front. */
  function potLid(c) {
    const { J, limb, parts } = c, { at } = between2(J), mid = add(at, J.torso([0, 0.010, 0.050])), n = J.torso([0, 0.62, -0.78]);
    limb(add(mid, mul(n, -0.008)), add(mid, mul(n, 0.008)), 0.068, 0.068, HINOKI, { part: parts.HELD, squareStart: true, squareEnd: true });
    limb(add(mid, mul(n, 0.008)), add(mid, mul(n, 0.024)), 0.013, 0.011, LID_KNOB, { part: parts.HELD, squareEnd: true });
  }
  /** A rice paddle (shamoji) in the right hand: a flat pale oval blade on a short handle. */
  function paddle(c, side = "R", out = 0.10) {
    const { J, limb, ball, parts } = c, g = J[side].palm, dir = J[side].hDir;
    limb(add(g, mul(dir, -0.012)), add(g, mul(dir, out * 0.55)), 0.006, 0.007, HINOKI, { part: parts.HELD });
    ball(add(g, mul(dir, out)), [0.024, 0.030, 0.008], HINOKI, { part: parts.HELD });
  }
  /** A boxwood comb: a small half-moon, held in two hands before the chest (or worn: see natsuComb). */
  function heldComb(c) {
    const { J, ball, parts, tw } = c, { at } = between2(J);
    ball(add(at, J.torso([0, 0.018, 0.012])), [0.030, 0.016, 0.006], TSUGE, { part: parts.HELD, fn: (ux, uy) => (uy > 0.15 ? null : uy > -0.25 ? undefined : shifted(TSUGE, 1)) }, tw);
  }
  /** A rice ball (bale-shaped, white) in the right hand. */
  function riceBall(c, side = "R") {
    const { J, ball, parts } = c, g = add(J[side].palm, mul(J[side].hDir, 0.012));
    ball(add(g, [0, 0.016, 0]), [0.020, 0.016, 0.026], WHITE, { part: parts.HELD });
  }
  /** A cotton towel (tenugui) in the hand, hanging (the thief-taker's, for his eyes). */
  function towel(c, side = "R", hang = 0.10) {
    const { J, limb, parts } = c, g = J[side].palm;
    limb(add(g, [0, 0.004, 0.004]), add(g, [0, -hang, 0.010]), 0.020, 0.024, SHIRO, { part: parts.HELD, squareStart: true, squareEnd: true, depth: 0.20, fn: (t) => (t > 0.86 ? AI : undefined) });
  }
  /** A towel over the shoulder (left), hanging down the chest and the back. */
  function shoulderTowel(c, mat = SHIRO) {
    const { limb, parts, cloth, under } = c, lie = { [parts.TORSO]: under, [parts.COLLAR]: under };
    limb(T(c, [-0.066, 0.016, 0.0]), T(c, [-0.060, -0.140, back(c) + 0.010]), 0.016, 0.018, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.4, squareEnd: true, depth: 0.25 });
    limb(T(c, [-0.066, 0.016, -0.004]), T(c, [-0.056, -0.120, -(back(c) + 0.010)]), 0.016, 0.018, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.4, squareEnd: true, depth: 0.25 });
  }
  /** A jitte tucked in the sash (round twenty's truncheon), and for the dōshin one with its red tassel (facts-edo-2
      item 13: "the red-tasselled jitte belongs to the dōshin"). Never drawn out. */
  function tasselJitte(c) {
    truncheon(c);
    const { trunkAt, d, limb, ball, parts, cloth } = c, hip = trunkAt(d.hipY + 0.030, -1.10, 0.014), top = [hip[0] + 0.004, hip[1] + 0.090, hip[2] + 0.030];
    limb(top, [top[0], top[1] - 0.050, top[2] + 0.006], 0.004, 0.007, SHU, { part: parts.EXTRA2, bias: cloth * 1.6 });
    ball([top[0], top[1] - 0.054, top[2] + 0.006], [0.008, 0.010, 0.008], SHU, { part: parts.EXTRA2, bias: cloth * 1.6 });
  }
  /** A deep woven hat (the broadsheet sellers'): a deep dome down over the eyes, the mouth showing under its rim. */
  function deepHat(c, mat = SUGE) {
    const { ball, limb, headPt, d, hy, parts, fine } = c, hr = d.headR;
    const weave = fine ? (ux, uy, uz, x, y) => ((x * 2 + y) % 5 === 0 ? shifted(mat, 1) : undefined) : null;
    ball(headPt([0, hr[1] * 0.36, 0.004]), [hr[0] * 1.42, hr[1] * 1.18, hr[2] * 1.40], mat, { part: parts.HAT, fn: (ux, uy, uz, x, y) => { const q = c.onHead(ux, uy, uz); return q[1] < -0.70 ? null : weave ? weave(ux, uy, uz, x, y) : undefined; } }, hy);
    limb(headPt([0, -hr[1] * 0.28, 0.006]), headPt([0, -hr[1] * 0.44, 0.006]), hr[0] * 1.46, hr[0] * 1.50, shifted(mat, 1), { part: parts.HAT, squareStart: true, squareEnd: true, depth: 1 });      // the rim, low over the nose
  }
  /** A sheaf of broadsheets under the left arm, and (talk or chant) one held up in the right hand. */
  function sheaf(c) {
    const { J, limb, parts } = c, at = add(J.L.elbow, J.torso([0.010, -0.010, 0.040]));
    limb(add(at, J.torso([0, 0, -0.060])), add(at, J.torso([0, 0, 0.060])), 0.034, 0.034, WASHI, { part: parts.EXTRA2, depth: 0.22, squareStart: true, squareEnd: true, fn: (t) => (((t * 9) | 0) % 3 === 0 ? shifted(WASHI, 1) : undefined) });
  }
  /** A formal vest with stiff wide shoulders (kataginu) over the kimono, for the chanter and the shamisen player. */
  function kataginu(c, mat) {
    const { J, limb, ball, d, tw, cloth, under, parts } = c, lie = { [parts.TORSO]: under, [parts.COLLAR]: under, [parts.BELT]: under };
    const r0 = c.wide([d.trunkTop[0] + 0.010, d.trunkTop[1] + 0.012]);
    limb(T(c, [0, -0.020, 0]), J.spine(d.waistY - 0.010), r0, r0 * 0.86, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.2, depth: (d.trunkTop[1] + 0.012) / r0, squareStart: true, squareEnd: true,
      fn: (t, nx) => { const round = c.roundAt(nx, tw * 0.6); return Math.abs(round) < 0.20 ? null : undefined; } });      // open down the front (the kimono's collar shows)
    for (const sd of [1, -1]) ball(T(c, [sd * (d.shoulderW + 0.016), 0.012, 0]), [0.066, 0.011, 0.036], mat, { part: parts.DRAPE, bias: cloth * 2.4 }, tw);      // the stiff wings over the shoulders
  }
  /** The shamisen, played kneeling: its square body on the right thigh, the long neck up and across to the left hand,
      the plectrum (bachi) in the right. */
  function shamisenOf(c) {
    const { J, ball, limb, parts, tw } = c, body = add(J.R.knee, [0, 0.080, -0.020]);
    ball(add(mix(J.hipC, J.R.knee, 0.55), [0.010, 0.070, 0.050]), [0.054, 0.054, 0.020], SHITAN, { part: parts.HELD, fn: (ux, uy) => (Math.abs(ux) < 0.78 && Math.abs(uy) < 0.78 ? NEKO : undefined) }, tw + 0.2);
    const base = add(mix(J.hipC, J.R.knee, 0.55), [0.010, 0.090, 0.050]), head = add(J.L.palm, J.torso([-0.010, 0.060, 0.000]));
    limb(base, head, 0.007, 0.006, SHITAN, { part: parts.HELD });
    limb(head, add(head, J.torso([-0.010, 0.040, -0.010])), 0.009, 0.008, SHITAN, { part: parts.HELD });          // the pegbox
    const g = J.R.palm;
    limb(add(g, mul(J.R.hDir, -0.004)), add(g, mul(J.R.hDir, 0.050)), 0.006, 0.016, IVORY, { part: parts.HELD });   // the plectrum
    void body;
  }

  // =================================================================================
  // At the foot of the pass: Nishikurasawa
  // =================================================================================
  // O-Kuni, about forty-five, the teahouse woman: brisk and loud; grills turban shells in their own shells and sells them
  // with a cry. A working kimono in indigo with the sleeves tied back, a persimmon apron, a white head-cloth; long cooking
  // chopsticks in her right hand. Married (teeth blackened); no child is named, so she keeps her brows.
  const CHOPS = { R: { hand: [0.070, -0.230, 0.120], bend: [0.7, -0.8, -0.3], grip: true, point: [0.1, -0.5, 0.86] } };
  function chopsticks(c) {
    const { J, parts } = c, g = J.R.palm, dir = J.R.hDir;
    for (const dx of [-0.004, 0.004]) rod(c, add(g, J.torso([dx, 0.010, 0])), add(add(g, mul(dir, 0.200)), J.torso([dx * 2, 0, 0])), 0.0028, EDO_WOOD, parts.HELD);
  }
  const kuniHolds = {
    /** holding out a grilled shell on the flat of her left hand, the chopsticks still in her right: "for the climb" */
    offer: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.10 }, held: "offer" };
      withArm(p, "L", { hand: [-0.040, -0.150, 0.230], bend: [-0.8, -0.6, -0.3], flat: true, point: [0.3, 0.1, 0.95], thumb: [0, 1, 0] }); return p; },
    /** her cry: her left hand up beside her mouth, her head up, calling the shells to the road */
    cry: (o) => { const b = o.base, hr = o.d.headR, p = { ...cloneP(b), mouth: 2, breath: 1, lean: (b.lean || 0) - 0.04, head: { nod: nodOf(b) - 0.16, turn: -0.20 }, held: "cry" };
      withArm(p, "L", { hand: [-(hr[0] + 0.016), o.sp.chinY - 0.006, hr[2] * 0.62], bend: [-1, -0.7, 0.3], curl: 0.6, point: [0.3, 0.9, 0.3] }); return p; },
  };
  const kuni = {
    ...WOMAN_EDO(EDO_SUN, AI, { face: { lines: 1, smile: 1, mouthW: 0.20, brow: { full: [0, -1, 0] } }, len: 1.62, gestures: [0, 1, 9, 11], pace: 165, dim: { shoulderW: 0.088, trunkTop: [0.094, 0.066], trunkLow: [0.082, 0.062] } }),
    name: "O-Kuni, the teahouse woman", height: H(146),
    stance: "hip", hold: CHOPS, lean: 0.03, walk: { swing: 0.44, arm: 0.36, elbow: 0.30, lean: 0.07, lift: 1.1, sway: 0.016 },
    fidgets: { stand: ["shift", "look", "turnshells", "fanfire"], not: ["sleeve", "scratch", "neck"] }, holds: kuniHolds, cues: { stand: ["turnshells", "fanfire", "ojigi"] }, ...bowOf(0.24),
    extras(c) { kimono(c, { mat: AI, obi: CHA, knot: "big", sleeve: 0 }); tasuki(c, BENI); apronOf(c, KAKI, 0.40); headcloth(c, SHIRO, { tails: 0.12, brow: 0.46 }); chopsticks(c);
      if (c.pose.fidget === "fanfire") { const { J, ball, limb, parts, tw } = c, g = J.L.palm, dir = J.L.hDir; limb(add(g, mul(dir, -0.010)), add(g, mul(dir, 0.040)), 0.004, 0.004, TAKE, { part: parts.HELD }); ball(add(g, mul(dir, 0.075)), [0.036, 0.036, 0.004], UCHIWA, { part: parts.HELD }, tw + 0.4); }
      if (c.pose.held === "offer") { const { J, ball, parts } = c; ball(add(J.L.palm, [0, 0.018, 0]), [0.024, 0.020, 0.024], SAZAE, { part: parts.HELD, fn: (ux, uy) => (uy < -0.2 ? SAZAE_LIP : undefined) }); } },
  };

  // The palanquin bearers (kumosuke: facts-21a item 3): a short jacket over a loincloth, bare legs, a towel twisted round the
  // head; found squatting by their palanquin. Sakuji is small and all mouth; Tora is huge and gentle.
  const SQUAT = { seat: 0.060, knees: 0.20, feet: -0.30, lean: 0.30, nod: -0.10 };      // down on his heels, the knees up
  const bearer = (skin, height, name, o = {}) => ({
    ...workman(skin, { dim: o.dim, jacket: o.jacket || UGUISU, face: o.face }), ...BARELEGS(skin, o.breeches || AI_DEEP), name, height,
    seated: "chair", sit: { ...SQUAT, ...(o.sit || {}) }, riseMs: 900, shadow: 0.20, span: 1.25,
    rest: { R: { hand: [0.080, -0.300, 0.300], bend: [0.6, -0.2, -0.7], curl: 0.6, point: [0, -0.8, 0.5] }, L: { hand: [-0.080, -0.300, 0.300], bend: [-0.6, -0.2, -0.7], curl: 0.6, point: [0, -0.8, 0.5] } },      // the forearms on the knees, the hands hanging
    stood: { rest: undefined },
    walk: { swing: 0.46, arm: 0.36, elbow: 0.30, lean: 0.07, lift: 1.1, bob: 0.02 }, pace: o.pace || 150,
    extras(c) { hachimaki(c, o.band || SHIRO, 0.44); chonmageTop(c); kimono(c, { mat: o.jacket || UGUISU, obi: o.obi || CHA, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0, jacket: true }); },
  });
  const sakuji = {
    ...bearer(EDO_SUN, H(150), "Sakuji, the palanquin bearer (small, all mouth)", { jacket: UGUISU, face: { eyes: "bright", smile: 1, mouthW: 0.24, jaw: 0.86, chin: 0.52, brow: { full: [-1, 0, 1] }, short: { mat: shifted(EDO_SUN, 2), stubble: shifted(EDO_SUN, 2), from: 0.35 } }, dim: { shoulderW: 0.096, armR: [0.030, 0.026, 0.019] }, pace: 165 }),
    gestures: [1, 2, 11, 10, 14],                                       // all mouth: a point, a shrug, a finger up, pointing, a fist
    fidgets: { only: true, sit: ["shift", "look", "jab", "farerub"], stand: ["shift", "look", "jab", "farerub"] },
    holds: { /** "How much have you got?": his hand out, palm up, the fingers rubbing */ fare: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) - 0.04, turn: 0.10 }, held: "fare" };
      withArm(p, "R", { hand: [0.070, o.seated ? -0.150 : -0.200, 0.230], bend: [0.8, -0.6, -0.3], curl: 0.5, point: [0, 0.2, 0.95], thumb: [1, 0, 0] }); return p; } },
    cues: { sit: ["jab", "farerub"], stand: ["jab", "farerub"] },
    stood: { fidgets: { only: true, stand: ["shift", "look", "jab", "farerub"] } },
  };
  const tora = {
    ...bearer(EDO_SUN, H(172), "Tora, the palanquin bearer (huge and gentle)", { jacket: KAKI, obi: AI_DEEP, band: AI, face: { eyes: "heavy", smile: 1, jaw: 1.00, chin: 0.74, brow: { full: [1, 0, 0] } },
      dim: { shoulderW: 0.112, trunkTop: [0.118, 0.080], trunkLow: [0.112, 0.084], bellyFwd: 0.014, armR: [0.036, 0.031, 0.022], handR: 0.026, legR: [0.056, 0.036, 0.024] }, pace: 130 }),
    gestures: [0, 2, 0, 8],                                             // slow: a nod, a shrug, an open hand
    fidgets: { only: true, sit: ["shift", "look", "scratchhead"], stand: ["shift", "look", "scratchhead"] },
    holds: { /** "We'd carry the little one for nothing.": a big open hand toward the palanquin, gently */ carry: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.04, head: { nod: nodOf(b) + 0.06, turn: 0.30 }, held: "carry" };
      withArm(p, "R", { hand: [0.180, o.seated ? -0.120 : -0.180, 0.150], bend: [1, -0.4, -0.3], flat: true, point: [0.7, -0.1, 0.7], thumb: [0, 1, 0] }); return p; } },
    cues: { sit: ["scratchhead"], stand: ["scratchhead"] },
  };

  // Sōshichi, the medicine peddler from Toyama, two months into his round: exact, polite, a man of lists. A plain dark
  // merchant's kimono hitched up for the road, indigo leg wraps, his five-tier willow trunks wrapped in a green cloth on his
  // back (`soshichi`); set down and unpacked (`soshichi-free`: the painter's trunks stand beside him).
  const soshichiHolds = {
    /** his ledger open in both hands, reading it close: every household on his round */
    ledger: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.24 }, held: "ledger" };
      for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.050, -0.140, 0.170], bend: [sd * 0.9, -0.6, -0.3], flat: true, point: [-sd * 0.2, 0.4, 0.9], thumb: [0, 1, 0] }); return p; },
    /** a print held out to a child: "For the child of the house. That's the custom." */
    print: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.12, head: { nod: nodOf(b) + 0.16 }, held: "print" };
      withArm(p, "R", { hand: [0.050, -0.200, 0.240], bend: [0.8, -0.6, -0.3], grip: true, point: [0, 0.3, 0.95] }); return p; },
  };
  const soshichiBase = {
    ...workman(EDO_SKIN, { dim: { shoulderW: 0.096, trunkTop: [0.100, 0.064], trunkLow: [0.088, 0.062] }, face: { eyes: "plain", jaw: 0.86, chin: 0.54, mouthW: 0.18, brow: { full: [0, 0, -1] } } }),
    ...robe(CHA, 1.55, { open: 0.030 }), ...wraps(AI), name: "Sōshichi, the medicine peddler", height: H(157),
    stance: "clasped", lean: 0.04, walk: { swing: 0.44, arm: 0.24, elbow: 0.30, lean: 0.07, lift: 1.0 }, pace: 145,
    gestures: [0, 17, 8, 0, 11],                                        // he counts on his fingers; an open hand; a finger up
    fidgets: { stand: ["shift", "look", "count"], not: ["sleeve", "scratch"] }, holds: soshichiHolds, cues: { stand: ["count", "ojigi"] }, ...bowOf(0.32),
  };
  const soshichiGear = (c) => { chonmageTop(c); kimono(c, { mat: CHA, obi: AI_DEEP, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.050 }); const h = c.pose.held; if (h === "ledger") openBook(c); if (h === "print") heldSheet(c, "R", WASHI, TOYAMA_INK); };
  const soshichi = { ...soshichiBase, span: 1.2, lean: 0.10, stance: "straps", walk: { swing: 0.42, arm: 0.14, elbow: 0.60, lean: 0.12, lift: 0.95 }, extras(c) { soshichiGear(c); trunks(c); } };
  const soshichiFree = { ...soshichiBase, name: "Sōshichi, his trunks set down", extras(c) { soshichiGear(c); } };

  // The komusō: a flute monk of the Fuke sect (facts-21a item 3): the deep basket hat over the whole head, a black robe, a
  // small surplice on the chest, white leg wraps, straw sandals (his clogs left out: he is walking the highway), and the
  // bamboo flute. Never seen, never speaks. `komuso` walking, the flute in his hand; `komuso-play` playing it.
  const komusoBase = {
    ...workman(EDO_SKIN, { dim: { shoulderW: 0.098 } }), ...robe(SUMI, 1.86, { open: 0.024 }), ...wraps(SHIRO),
    name: "the komusō, a flute monk", height: H(160), crown: 0.06, span: 1.15,
    stance: "clasped", lean: 0.0, walk: { swing: 0.40, arm: 0.10, elbow: 0.30, lean: 0.03, lift: 0.9 }, pace: 120,
    gestures: [0, 0, 0, 0], ...bowOf(0.20),
  };
  const FLUTE_DOWN = { R: { hand: [0.080, -0.300, 0.050], bend: [0.6, -0.8, -0.4], grip: true, point: [0.1, -0.9, 0.4] } };
  const FLUTE_UP = { R: { hand: [0.006, -0.150, 0.150], bend: [0.9, -0.6, -0.3], curl: 1.0, point: [-0.3, 0.8, 0.5] }, L: { hand: [-0.004, -0.060, 0.140], bend: [-0.9, -0.6, -0.3], curl: 1.0, point: [0.3, 0.8, 0.5] } };
  const komuso = { ...komusoBase, hold: FLUTE_DOWN, fidgets: { only: true, stand: ["shift", "look"] },
    extras(c) { kimono(c, { mat: SUMI, obi: NEZUMI, obiUp: 0.018, obiDown: 0.026, knot: "small", sleeve: 0.070 }); rakusu(c); tengai(c); shakuhachi(c, false); } };
  const komusoPlay = { ...komusoBase, name: "the komusō, playing", hold: FLUTE_UP, fidgets: { only: true, stand: ["fluteplay", "fluteplay", "shift"] }, cues: { stand: ["fluteplay"] },
    extras(c) { kimono(c, { mat: SUMI, obi: NEZUMI, obiUp: 0.018, obiDown: 0.026, knot: "small", sleeve: 0.070 }); rakusu(c); tengai(c); shakuhachi(c, true); } };

  // The relay courier (tsugi-bikyaku: facts-21a item 3): a short jacket, a loincloth, bare legs, a towel round the head, the
  // letter box on a pole on his right shoulder; he runs (his walk is a run: pace 330).
  const courier = {
    ...workman(EDO_SUN, { dim: { shoulderW: 0.100, legR: [0.052, 0.033, 0.022] }, jacket: KACHI, face: { eyes: "plain", jaw: 0.88, chin: 0.56, mouthW: 0.22 } }), ...BARELEGS(EDO_SUN, AI_DEEP),
    name: "the relay courier", height: H(158), span: 1.6, tall: 1.3,
    hold: { R: { hand: [0.092, 0.040, 0.120], bend: [0.9, -0.6, -0.1], grip: true, point: [0, 0.16, 0.99] } },      // on the pole, before the shoulder
    stance: "clasped", walk: { swing: 0.64, arm: 0.70, elbow: 1.20, pump: 0.30, lean: 0.16, lift: 1.6, bob: 0.04 }, pace: 330,
    gestures: [0, 1, 0, 20], fidgets: { only: true, stand: ["shift", "look", "pant"] }, cues: { stand: ["pant"] },
    extras(c) { hachimaki(c, SHIRO, 0.46); chonmageTop(c); kimono(c, { mat: KACHI, obi: CHA, obiUp: 0.014, obiDown: 0.022, knot: "small", sleeve: 0, jacket: true }); letterbox(c); },
  };

  // =================================================================================
  // At the top of the pass
  // =================================================================================
  // Mosuke, an old woodcutter of Yui: grey, stubbled, bent under a load of brushwood on a frame on his back; his load pole
  // (a long staff) in his right hand. He has walked this road every day of his life and never looks at Fuji.
  const mosuke = {
    ...workman(EDO_SUN, { dim: { shoulderW: 0.096 }, jacket: UGUISU, trousers: CHA, face: { eyes: "heavy", lines: 2, jaw: 0.90, chin: 0.56, short: { mat: EDO_GREY, stubble: EDO_GREY, from: 0.2 } } }), ...wraps(CHA),
    name: "Mosuke, the woodcutter", height: H(152), hair: { mat: EDO_GREY, bulk: [1.04, 1.0, 1.04], where: chonmage }, span: 1.3, tall: 1.32,
    stance: "straps", lean: 0.14, nod: 0.06, walk: { swing: 0.34, arm: 0.16, elbow: 0.50, lean: 0.16, lift: 0.8 }, pace: 105,
    hold: { R: { hand: [0.120, -0.200, 0.120], bend: [0.6, -0.8, -0.3], grip: true, point: [0, 1, 0.1] } },
    gestures: [0, 20, 0, 15],                                            // a nod; a nod aside (down the road); waving it away
    fidgets: { only: true, stand: ["shift", "hitchload", "wipebrow"] }, cues: { stand: ["hitchload"] }, ...bowOf(0.20),
    holds: { /** his pole held up and out at arm's length (to lift something off a high place), or lent */ pole: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.04, head: { nod: nodOf(b) - 0.20 }, held: "pole" };
      withArm(p, "R", { hand: [0.140, -0.020, 0.250], bend: [0.6, -0.8, -0.2], grip: true, point: [0, 0.4, 0.9] }); return p; } },
    extras(c) { hachimaki(c, SHIRO, 0.42); chonmageTop(c, { mat: EDO_GREY, pate: pateOf(EDO_SUN) }); kimono(c, { mat: UGUISU, obi: ROPE, obiUp: 0.014, obiDown: 0.022, knot: "small", sleeve: 0, jacket: true }); brushwood(c);
      if (c.pose.held === "pole") { const { J } = c, g = J.R.palm, dir = unit(add(J.R.hDir, [0, 0.4, 0])); rod(c, add(g, mul(dir, -0.25)), add(g, mul(dir, 0.55)), 0.0075, EDO_WOOD); }
      else wear.staff(c, "R", { mat: EDO_WOOD, top: 1.08, r: 0.0075 }); },
  };

  // O-Shige, about fifty, a merchant's widow from the west, going east to Edo to see a new grandson, with a pass: sharp,
  // funny, tired. Travel clothes (a greyed wisteria kimono hitched up, leg wraps, a sedge hat), teeth blackened, no brows
  // (she has children), and the mole by her right eye that her pass describes. `shige` on her feet (the hat on);
  // `shige-stone` sat down on her stone (the hat on her back), getting up with sit(false).
  const shigeMole = (c) => {
    const { sf, P, hp, th, hy, fine } = c, ang = th + hy;
    if (!fine || Math.sin(ang) < -0.45 || Math.cos(ang) < -0.2) return;  // (her right cheek, seen from in front or her right)
    const q = P(hp(0.56, -0.12, 0.84));
    sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), pack(MOLE), c.parts.HEAD);
  };
  const shigeHolds = {
    /** her pass held to her chest in both hands, given back: she goes white, then pink */
    pass: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.14 }, held: "pass", breath: 1 };
      for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.016, -0.110, o.sp.chest + 0.040 + (o.seated ? 0.02 : 0)], bend: [sd, -0.6, 0.1], curl: 0.8, point: [-sd * 0.6, 0.6, 0.3] }); return p; },
    /** fanning herself with a folding fan: the climb */
    fan: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) - 0.08, turn: 0.10 }, held: "fan" };
      withArm(p, "R", { hand: [0.050, o.sp.chinY - 0.040, 0.130], bend: [0.9, -0.6, -0.2], grip: true, point: [-0.2, 0.9, 0.3] }); return p; },
  };
  function foldingFan(c, side = "R") {
    const { J, ball, parts, tw } = c, g = add(J[side].palm, mul(J[side].hDir, 0.040));
    ball(g, [0.042, 0.034, 0.004], WASHI, { part: parts.HELD, fn: (ux, uy) => (uy > 0.2 ? null : (Math.atan2(ux, uy + 1) * 6 | 0) % 2 ? shifted(WASHI, 1) : undefined) }, tw + 0.6);
  }
  const shigeBase = {
    ...WOMAN_EDO(OLD_SKIN, FUJINEZU, { face: { brows: null, lines: 2, eyes: "heavy", jaw: 0.80, chin: 0.50, mouthW: 0.20 }, len: 1.50, gestures: [0, 3, 2, 15, 8], pace: 130, dim: { shoulderW: 0.084, trunkTop: [0.090, 0.066], trunkLow: [0.084, 0.064] } }),
    ...wraps(NEZUMI), name: "O-Shige, the widow with a pass", height: H(146),
    stance: "clasped", lean: 0.05, walk: { swing: 0.36, arm: 0.20, elbow: 0.30, lean: 0.10, lift: 0.9, sway: 0.012 },
    fidgets: { stand: ["shift", "look", "puff"], sit: ["shift", "look", "knees", "fanself"], not: ["sleeve", "scratch"] }, holds: shigeHolds, cues: { stand: ["puff", "ojigi"], sit: ["fanself"] }, ...bowOf(0.26),
  };
  const shigeGear = (c, hat) => { kimono(c, { mat: FUJINEZU, obi: CHA, knot: "big", sleeve: 0.060 }); sugegasa(c, { back: hat === "back", r: 0.112 }); shigeMole(c); if (c.pose.held === "pass") { const { J, ball, parts } = c; ball(add(mix(J.R.palm, J.L.palm, 0.5), J.torso([0, 0.010, 0.012])), [0.026, 0.018, 0.006], OILPAPER, { part: parts.HELD }, c.tw); } if (c.pose.held === "fan" || c.pose.fidget === "fanself") foldingFan(c); };
  const shige = { ...shigeBase, extras(c) { shigeGear(c, "on"); } };
  const shigeStone = { ...shigeBase, name: "O-Shige, sitting on a stone", seated: "chair", sit: { seat: 0.24, lean: 0.06, knees: 0.12, nod: 0.02 }, riseMs: 1500, shadow: 0.20, stood: { fidgets: shigeBase.fidgets }, extras(c) { shigeGear(c, "back"); } };

  // Kyūzō, her old manservant, her box on a pole on his shoulder: grey, a servant's short indigo coat, leg wraps; he drops
  // things. `kyuzo` with her pass (a folded paper in oiled paper) tucked in his sash; `kyuzo-nopass` after the gust.
  const kyuzoBase = {
    ...workman(EDO_SKIN, { dim: { shoulderW: 0.094 }, jacket: AI, trousers: AI_DEEP, face: { eyes: "wide", lines: 2, jaw: 0.84, chin: 0.52, brow: { full: [0, -1, -1] }, browUp: 3, short: { mat: EDO_GREY, stubble: EDO_GREY, from: 0.4 } } }), ...wraps(AI),
    name: "Kyūzō, the widow's manservant", height: H(150), hair: { mat: EDO_GREY, bulk: [1.04, 1.0, 1.04], where: chonmage }, span: 1.45,
    hold: { R: { hand: [0.092, 0.030, 0.060], bend: [0.9, -0.6, -0.1], grip: true, point: [0, 0.10, 0.99] } },      // on the pole's front end
    stance: "clasped", lean: 0.08, walk: { swing: 0.36, arm: 0.20, elbow: 0.40, lean: 0.10, lift: 0.9, bob: 0.02 }, pace: 120,
    gestures: [0, 5, 0, 2], fidgets: { only: true, stand: ["shift", "look", "patsash"] }, cues: { stand: ["patsash", "ojigi"] }, ...bowOf(0.40),
    holds: { /** startled, his free hand flung up: something has blown away */ drop: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.06, breath: 1, mouth: 2, head: { nod: nodOf(b) - 0.20, turn: 0.30 }, held: "drop" };
      withArm(p, "L", { arm: [2.2, 0.50], elbow: 0.40, flat: true }); return p; } },
  };
  const kyuzoGear = (c, pass) => {
    chonmageTop(c, { mat: EDO_GREY, pate: pateOf(EDO_SKIN) }); kimono(c, { mat: AI, obi: NEZUMI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0, jacket: true }); poleBox(c);
    if (pass) { const { trunkAt, d, ball, parts } = c; ball(trunkAt(d.waistY - 0.004, 0.55, 0.016), [0.014, 0.020, 0.006], OILPAPER, { part: parts.EXTRA2, bias: c.cloth * 2 }, c.tw + 0.5); }
  };
  const kyuzo = { ...kyuzoBase, extras(c) { kyuzoGear(c, true); } };
  const kyuzoNopass = { ...kyuzoBase, name: "Kyūzō, the pass blown out of his sash", extras(c) { kyuzoGear(c, false); } };

  // =================================================================================
  // On the ship (Gonroku, the master, is round twenty's)
  // =================================================================================
  // The sailors' clothes (facts-21a item 6 names the ranks; their clothes are not in the sources): a short jacket, a
  // loincloth or tight trousers, a twisted towel round the head, bare feet on the deck.
  // Kanbei, the navigator (omote), about seventy: his eyes bad in the glare (he squints), a voice like a slow door, proud
  // of the ship's clock.
  const kanbeiHolds = {
    /** bent over the compass box at his waist, a hand flat over his brow against the glare */
    peer: (o) => { const b = o.base, hr = o.d.headR, p = { ...cloneP(b), lean: (b.lean || 0) + 0.36, head: { nod: nodOf(b) + 0.08 }, held: "peer" };
      withArm(p, "R", { hand: [0.030, o.sp.headY + hr[1] * 0.40 - 0.020, hr[2] + 0.040], bend: [1, -0.3, 0.3], flat: true, point: [-0.8, 0.1, 0.6], thumb: [0, -1, 0] });
      withArm(p, "L", { hand: [-0.060, -0.240, 0.200], bend: [-0.8, -0.4, -0.4], flat: true, point: [0.2, -0.4, 0.9] }); return p; },
    /** calling the heading to the helm: his hand beside his mouth, his head turned back over his shoulder */
    call: (o) => { const b = o.base, hr = o.d.headR, p = { ...cloneP(b), mouth: 2, breath: 1, twist: 0.20, head: { nod: nodOf(b) - 0.10, turn: 0.75 }, held: "call" };
      withArm(p, "R", { hand: [hr[0] + 0.016, o.sp.chinY - 0.006, hr[2] * 0.62], bend: [1, -0.7, 0.3], curl: 0.6, point: [-0.3, 0.9, 0.3] }); return p; },
  };
  const kanbei = {
    ...workman(EDO_SUN, { dim: { shoulderW: 0.094, trunkTop: [0.098, 0.064] }, jacket: NEZUMI, trousers: AI, face: { eyes: "squint", lines: 2, jaw: 0.86, chin: 0.54, brow: { full: [1, 1, 0] }, short: { mat: EDO_GREY, stubble: EDO_GREY, from: 0.3 } } }), ...BARE,
    name: "Kanbei, the navigator", height: H(154), hair: { mat: EDO_GREY, bulk: [1.03, 1.0, 1.03], where: chonmage },
    stance: "behind", lean: 0.10, nod: 0.04, walk: { swing: 0.34, arm: 0.14, elbow: 0.40, lean: 0.12, lift: 0.8 }, pace: 100,
    gestures: [0, 11, 0, 20],                                            // slow: a nod, a finger up, a nod aside (toward the helm)
    fidgets: { only: true, stand: ["shift", "squint", "rubeyes"] }, holds: kanbeiHolds, cues: { stand: ["rubeyes", "squint"] }, ...bowOf(0.24),
    extras(c) { hachimaki(c, SHIRO, 0.44); chonmageTop(c, { mat: EDO_GREY, pate: pateOf(EDO_SUN) }); kimono(c, { mat: NEZUMI, obi: CHA, obiUp: 0.014, obiDown: 0.022, knot: "small", sleeve: 0, jacket: true }); },
  };
  // Denzō, the bosun (oyaji): huge, loud, kind, superstitious about everything; his jacket open over a broad chest, a
  // loincloth, bare legs and feet. He knows every sea word and everything sealed in the mast.
  const denzo = {
    ...workman(BIG_SKIN, { dim: { shoulderW: 0.114, trunkTop: [0.120, 0.082], trunkLow: [0.110, 0.084], bellyFwd: 0.012, armR: [0.038, 0.033, 0.023], handR: 0.027, legR: [0.058, 0.037, 0.025] }, jacket: KAKI,
      face: { eyes: "wide", jaw: 1.00, chin: 0.72, mouthW: 0.24, brow: { full: [1, 0, -1] }, short: { mat: shifted(EDO_SUN, 2), stubble: shifted(EDO_SUN, 2), from: 0.25 } } }), ...BARELEGS(BIG_SKIN, CHA), ...BARE,
    name: "Denzō, the bosun", height: H(168), top: { mat: KAKI, sleeves: 2, ease: 0.008, hem: 0.085, open: 0.090, under: BIG_SKIN },
    stance: "akimbo", lean: -0.01, walk: { swing: 0.46, arm: 0.36, elbow: 0.30, lean: 0.04, lift: 1.0, sway: 0.020 }, pace: 140,
    gestures: [4, 18, 1, 14, 0],                                         // loud: both arms up, hands wide, a point, a fist
    fidgets: { only: true, stand: ["shift", "look", "knockwood", "skyward"] }, cues: { stand: ["knockwood", "skyward"] }, ...bowOf(0.20),
    holds: {
      /** his hand flat on the mast in front of him: not that word, not at sea */ mast: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) - 0.06, turn: -0.10 }, held: "mast" };
        withArm(p, "R", { hand: [0.060, 0.020, 0.260], bend: [0.8, -0.6, -0.3], flat: true, point: [0, 0.5, 0.86], thumb: [-1, 0, 0] }); return p; },
      /** counting off what the lady was given, on his fingers */ tally: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.08 }, held: "tally" };
        withArm(p, "L", { hand: [-0.030, o.sp.waist + 0.050, o.sp.belly + 0.080], bend: [-1, -0.5, -0.2], flat: true });
        withArm(p, "R", { hand: [0.012, o.sp.waist + 0.074, o.sp.belly + 0.090], bend: [1, -0.4, -0.2], finger: true, point: [-0.6, -0.6, 0.2] }); return p; },
    },
    extras(c) { hachimaki(c, AI, 0.46); chonmageTop(c); kimono(c, { mat: KAKI, obi: AI_DEEP, obiUp: 0.014, obiDown: 0.022, knot: "small", sleeve: 0, jacket: true }); },
  };
  // Seijirō, the purser (makanai): neat, a plain kimono hitched to the knee, an abacus; found sitting on a bale, counting.
  const seijiro = {
    ...workman(EDO_PALE, { dim: { shoulderW: 0.090, trunkTop: [0.094, 0.062], trunkLow: [0.084, 0.060] }, face: { eyes: "plain", jaw: 0.84, chin: 0.52, mouthW: 0.18, brow: { full: [0, 0, 0] } } }),
    ...robe(KOGECHA, 1.15, { open: 0.026 }), ...BARE, name: "Seijirō, the purser", height: H(154),
    seated: "chair", sit: { seat: 0.27, lean: 0.10, knees: 0.10, nod: 0.12 }, riseMs: 900, shadow: 0.20,
    hold: { L: { hand: [-0.020, -0.200, 0.170], bend: [-0.9, -0.5, -0.4], grip: true, point: [0.9, 0.2, 0.3], thumb: [0, 1, 0] } },
    stance: "clasped", walk: { swing: 0.40, arm: 0.20, elbow: 0.40, lean: 0.05, lift: 0.9 }, pace: 135,
    gestures: [0, 17, 0, 11], fidgets: { only: true, sit: ["shift", "look", "clickbeads"], stand: ["shift", "look", "clickbeads"] }, cues: { sit: ["clickbeads"], stand: ["clickbeads", "ojigi"] }, ...bowOf(0.30),
    holds: { /** pointing at a cask with his free hand, counting it: one */ point: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) - 0.02, turn: 0.30 }, held: "point" };
      withArm(p, "R", { arm: [1.10, 0.30], elbow: 0.20, finger: true }); return p; } },
    extras(c) { chonmageTop(c); kimono(c, { mat: KOGECHA, obi: AI_DEEP, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.040 }); abacus(c, "L"); },
  };
  // Kōta, the ship's boy and cook (kashiki), twelve, on his first voyage: O-Masa's nephew from Yui, homesick; a boy's hair
  // (the forelock, a small knot), a short kimono to the knee with the sleeves tied back, a towel round the head, bare feet.
  const kotaHolds = {
    /** lifting the pot's lid to look (he keeps doing it): both hands on the lid, bent over the pot at his waist */
    lid: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.30, head: { nod: nodOf(b) + 0.18 }, held: "lid" };
      for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.060, -0.250, 0.220], bend: [sd * 0.9, -0.6, -0.3], curl: 0.7, point: [-sd * 0.6, -0.3, 0.7], thumb: [0, 1, 0] }); return p; },
    /** waiting, the hardest thing: hands clenched at his sides, staring at the pot */
    wait: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.12, breath: 1, head: { nod: nodOf(b) + 0.22 }, held: "wait" };
      for (const s of ["R", "L"]) withArm(p, s, { arm: [-0.10, 0.06], elbow: 0.20, grip: true }); return p; },
    /** his one-mon coin held out on his palm */
    coin: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.08, head: { nod: nodOf(b) + 0.14 }, held: "coin" };
      withArm(p, "R", { hand: [0.040, -0.170, 0.220], bend: [0.8, -0.6, -0.3], flat: true, point: [-0.2, 0.1, 0.95], thumb: [0, 1, 0] }); return p; },
  };
  const KOTA_STRIPE = { mat: ramp("#8a9ccc", "#5e70a8", "#40507c", "#283450"), at: Array.from({ length: 12 }, (_, i) => -Math.PI + (i + 0.5) * (2 * Math.PI / 12)), half: 0.06 };
  const kota = {
    name: "Kōta, the ship's boy", height: H(138),
    dim: { ...blend(CHILD, ADULT, 0.45), headR: [0.062, 0.073, 0.070] }, skin: EDO_SUN,
    hair: { mat: EDO_HAIR, bulk: [1.08, 1.04, 1.08], where: boyhair, puffs: BOY_PUFFS, ears: true },
    face: { ...EDO_CHILD_FACE, eyes: "bright", smile: 0.5, brow: { full: [0, 1, 1] } },
    top: { mat: AI, sleeves: 2, ease: 0.006, open: 0.030, under: WHITE, stripe: KOTA_STRIPE }, bottom: { kind: "skirt", mat: AI, len: 1.05, flare: 1.06, wrap: [0.55, -0.30], under: AI, stripe: KOTA_STRIPE }, ...BARE,
    stance: "clasped", lean: 0.03, walk: { swing: 0.48, arm: 0.40, elbow: 0.30, lean: 0.08, lift: 1.2, bob: 0.03 }, pace: 175,
    gestures: [0, 10, 0, 4, 11],                                         // he copies Little Sister's rhythm: a point, both hands up, a finger up
    fidgets: { only: true, stand: ["shift", "look", "peeklid", "stirpot"] }, holds: kotaHolds, cues: { stand: ["peeklid", "stirpot", "laughout", "ojigi"] }, ...bowOf(0.34),
    extras(c) { hachimaki(c, SHIRO, 0.44); kimono(c, { mat: AI, obi: CHA, obiUp: 0.026, obiDown: 0.024, knot: "small", sleeve: 0 }); tasuki(c, SHIRO);
      const h = c.pose.held, f = c.pose.fidget, u = c.pose.fu || 0;
      if (h === "lid" || (f === "peeklid" && u > 0.22 && u < 0.78)) potLid(c);
      if (f === "stirpot") paddle(c, "R", 0.12);
      if (h === "coin") { const { J, ball, parts } = c; ball(add(J.R.palm, [0, 0.012, 0]), [0.012, 0.004, 0.012], COPPER, { part: parts.HELD, fn: (ux, uy, uz, x, y) => (Math.abs(ux) < 0.3 && Math.abs(uz) < 0.3 ? shifted(SHITAN, 2) : undefined) }); } },
  };
  // The two sailors (kako) at the windlass: a short jacket, a loincloth, bare legs and feet, a towel round the head; they lean
  // on the windlass bars (`bar`) and heave on them (`heave`). One voice between them.
  const BAR = (o, deep = 0) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.34 + deep, head: { nod: nodOf(b) - 0.20 - deep * 0.3 }, held: "bar" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.090, -0.040, 0.250], bend: [sd * 0.7, -0.6, -0.3], grip: true, point: [-sd, 0, 0.1] });
    p.R = { ...p.R, leg: [-0.30 - deep, 0.04], knee: 0.10 }; p.L = { ...p.L, leg: [0.22, 0.04], knee: 0.30 + deep }; return p; };
  const sailor = (skin, height, name, o = {}) => ({
    ...workman(skin, { dim: o.dim, jacket: o.jacket || KACHI, face: o.face }), ...BARELEGS(skin, o.breeches || AI_DEEP), ...BARE, name, height,
    stance: o.stance || "folded", lean: 0.02, walk: { swing: 0.46, arm: 0.34, elbow: 0.30, lean: 0.05, lift: 1.0, sway: 0.016 }, pace: 150,
    gestures: [0, 2, 0, 9], fidgets: { only: true, stand: ["shift", "look", "wipebrow"] }, holds: { bar: (k) => BAR(k) }, cues: { stand: ["heave", "wipebrow"] }, ...bowOf(0.20),
    extras(c) { hachimaki(c, o.band || SHIRO, 0.45); chonmageTop(c); kimono(c, { mat: o.jacket || KACHI, obi: o.obi || CHA, obiUp: 0.014, obiDown: 0.022, knot: "small", sleeve: 0, jacket: true }); if (o.towel) shoulderTowel(c); },
  });
  const kako1 = sailor(EDO_SUN, H(158), "a sailor at the windlass", { jacket: KACHI, face: { eyes: "plain", jaw: 0.92, chin: 0.60, short: { mat: shifted(EDO_SUN, 2), stubble: shifted(EDO_SUN, 2), from: 0.3 } } });
  const kako2 = sailor(BIG_SKIN, H(155), "a sailor at the windlass (the second)", { jacket: AI, band: KAKI, towel: true, breeches: CHA, obi: NEZUMI, stance: "akimbo", face: { eyes: "bright", smile: 1, jaw: 0.86, chin: 0.56 }, dim: { shoulderW: 0.104 } });

  // =================================================================================
  // Osaka
  // =================================================================================
  // O-Natsu, about forty, the mistress of a rice dealer's house on the Dōjima shore: warm, quick, managing. A good brown
  // striped kimono, the sleeves tied back for the alms pot, an indigo apron, her boxwood comb in her hair (`natsu`; given
  // away: `natsu-nocomb`). Married (teeth blackened); her runaway apprentice is the only boy she speaks of, so her brows stay.
  const NATSU_STRIPE = { mat: shifted(CHA, 1), at: Array.from({ length: 16 }, (_, i) => -Math.PI + (i + 0.5) * (2 * Math.PI / 16)), half: 0.07 };
  const natsuComb = (c) => { const { ball, hp, parts, hy } = c; ball(hp(0, 0.80, 0.30), [0.026, 0.012, 0.010], TSUGE, { part: parts.HAT, fn: (ux, uy) => (uy > 0.25 ? null : undefined) }, hy); };
  const natsuHolds = {
    /** the rice paddle held out on its own, to Mom: in a house the paddle is more than a spoon */
    paddle: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) + 0.06 }, held: "paddle" };
      withArm(p, "R", { hand: [0.060, -0.140, 0.250], bend: [0.8, -0.6, -0.3], grip: true, point: [0, 0.5, 0.86] }); return p; },
    /** at the crossroads: the comb held up in both hands before her, her head bowed, asking the road god */
    comb: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.30 }, held: "comb", blink: true };
      for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.020, -0.090, o.sp.chest + 0.050], bend: [sd, -0.6, 0.1], curl: 0.8, point: [-sd * 0.6, 0.6, 0.3] }); return p; },
  };
  const natsuBase = {
    ...WOMAN_EDO(EDO_SKIN, CHA, { face: { smile: 1, lines: 1, mouthW: 0.20, brow: { full: [0, -1, 0] } }, len: 1.74, gestures: [0, 9, 8, 1, 11], pace: 170, dim: { shoulderW: 0.086 } }),
    top: { mat: CHA, sleeves: 2, ease: 0.006, open: 0.030, under: WHITE, stripe: NATSU_STRIPE }, bottom: { kind: "skirt", mat: CHA, len: 1.74, flare: 1.03, wrap: [0.55, -0.30], under: CHA, stripe: NATSU_STRIPE },
    name: "O-Natsu, the rice dealer's wife", height: H(146),
    stance: "clasped", lean: 0.03, walk: { swing: 0.44, arm: 0.34, elbow: 0.40, lean: 0.07, lift: 1.1, sway: 0.014 },
    fidgets: { stand: ["shift", "look", "serve", "tasuki"], not: ["sleeve", "scratch"] }, holds: natsuHolds, cues: { stand: ["serve", "laugh", "ojigi"] }, ...bowOf(0.30),
  };
  const natsuGear = (c, comb) => { kimono(c, { mat: CHA, obi: AI_DEEP, knot: "big", sleeve: 0 }); tasuki(c, SHU); apronOf(c, AI, 0.30); const h = c.pose.held, f = c.pose.fidget;
    if (comb && h !== "comb") natsuComb(c); if (h === "comb") heldComb(c); if (h === "paddle" || f === "serve") paddle(c, "R", 0.10); };
  const natsu = { ...natsuBase, extras(c) { natsuGear(c, true); } };
  const natsuNocomb = { ...natsuBase, name: "O-Natsu, her comb given away", extras(c) { natsuGear(c, false); } };

  // Rihei, her husband, a rice dealer: in the market after the close, shouting prices with his hands up, splashed by the
  // water men every day of his life. A dark kimono and a brown jacket.
  const rihei = {
    ...workman(EDO_SKIN, { dim: { shoulderW: 0.098, bellyFwd: 0.010 }, face: { eyes: "wide", mouthW: 0.24, jaw: 0.90, chin: 0.58, brow: { full: [-1, 0, 1] } } }), ...robe(AI_DEEP, 1.80, { open: 0.030 }),
    top: { mat: CHA, sleeves: 2, ease: 0.008, open: 0.040, under: AI_DEEP, hem: 0.10 },
    name: "Rihei, the rice dealer", height: H(156), span: 1.2,
    stance: "clasped", lean: 0.02, walk: { swing: 0.42, arm: 0.30, elbow: 0.30, lean: 0.06, lift: 1.0 }, pace: 160,
    gestures: [4, 1, 14, 11, 18], fidgets: { only: true, stand: ["shift", "bidding", "shakewet"] }, cues: { stand: ["bidding", "shakewet"] }, ...bowOf(0.26),
    holds: { /** bidding: both hands up, the fingers making the price, his mouth open */ bid: (o) => { const b = o.base, p = { ...cloneP(b), mouth: 2, breath: 1, lean: (b.lean || 0) - 0.04, head: { nod: nodOf(b) - 0.14 }, held: "bid" };
      withArm(p, "R", { arm: [2.40, 0.40], elbow: 0.50, finger: true }); withArm(p, "L", { arm: [1.10, 0.40], elbow: 0.90, flat: true }); return p; } },
    extras(c) { chonmageTop(c); kimono(c, { mat: CHA, obi: AI_DEEP, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.060, jacket: true }); },
  };
  // Kyūhachi, the freeloader: lives on alms, sleeps at one alms lodge after another; thin, stubbled, a patched brown travel
  // kimono hitched up, leg wraps, a battered sedge hat, and the ladle he lives by.
  const kyuhachi = {
    ...workman(EDO_SUN, { dim: { shoulderW: 0.090, trunkTop: [0.092, 0.060], trunkLow: [0.078, 0.056], armR: [0.026, 0.022, 0.016] }, face: { eyes: "heavy", smile: 1, jaw: 0.84, chin: 0.50, short: { mat: shifted(EDO_SUN, 2), stubble: shifted(EDO_SUN, 2), from: 0.2 } } }),
    ...robe(KOGECHA, 1.50, { open: 0.030 }), ...wraps(CHA), name: "Kyūhachi, the freeloader", height: H(155), span: 1.2,
    hold: { R: { hand: [0.090, -0.150, 0.130], bend: [0.7, -0.8, -0.3], grip: true, point: [0, 1, 0.2] } },
    stance: "clasped", lean: 0.06, walk: { swing: 0.40, arm: 0.20, elbow: 0.30, lean: 0.08, lift: 0.9, bob: 0.02 }, pace: 140,
    gestures: [0, 0, 20, 2], fidgets: { only: true, stand: ["shift", "look", "scratch"] }, cues: { stand: ["ojigi"] }, ...bowOf(0.30),
    holds: {
      /** his ladle held out for alms, again */ ladleout: (o) => { const b = o.base, q = { ...cloneP(b), lean: (b.lean || 0) + 0.08, head: { nod: nodOf(b) + 0.08 }, held: "ladleout" }; withArm(q, "R", { hand: [0.080, -0.180, 0.230], bend: [0.6, -0.8, -0.2], grip: true, point: [0.1, 0.3, 0.95] }); return q; },
      /** offering to lend it, for a share: the ladle held out sideways, handle first, a grin */ lend: (o) => { const b = o.base, q = { ...cloneP(b), smile: 2, lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.02, turn: 0.10 }, held: "lend" }; withArm(q, "R", { hand: [0.120, -0.150, 0.200], bend: [0.7, -0.7, -0.2], grip: true, point: [-0.6, 0, 0.8] }); return q; },
    },
    extras(c) { chonmageTop(c); kimono(c, { mat: KOGECHA, obi: ROPE, obiUp: 0.014, obiDown: 0.022, knot: "small", sleeve: 0.040 }); sugegasa(c, { r: 0.108, mat: SUGE_OLD }); ladle(c, c.pose.held !== "ladleout" && c.pose.held !== "lend"); },
  };
  // Kurata, a dōshin of the town magistrate's office (facts-21b item 6): dry, tired, unimpressed by everything, sick of
  // strange stories; not cruel, not stupid. A black jacket over a grey striped kimono, no hakama, the two swords at his left
  // hip (always sheathed), the jitte with its red tassel in his sash, white tabi. (How a dōshin dressed is not in the
  // sources: the look is the game's, and says so.)
  const kurata = {
    ...samurai(EDO_SKIN, H(160), "Kurata, the dōshin", { dim: { shoulderW: 0.100 }, face: { eyes: "heavy", lines: 1, jaw: 0.90, chin: 0.56, mouthW: 0.18, brow: { full: [0, 0, 1] } }, stance: "behind", gestures: [0, 15, 0, 2, 20] }),
    ...robe(NEZUMI, 1.86, { open: 0.030 }), top: { mat: SUMI, sleeves: 2, ease: 0.008, open: 0.036, under: NEZUMI, hem: 0.12 },
    bottom: { kind: "skirt", mat: NEZUMI, len: 1.86, flare: 1.03, wrap: [0.55, -0.30], under: NEZUMI, stripe: { mat: shifted(NEZUMI, 1), at: Array.from({ length: 20 }, (_, i) => -Math.PI + (i + 0.5) * (2 * Math.PI / 20)), half: 0.045 } },
    lean: 0.03, walk: { swing: 0.40, arm: 0.10, elbow: 0.20, lean: 0.04, lift: 0.9 }, pace: 125,
    fidgets: { only: true, stand: ["shift", "look", "wearysigh"] }, cues: { stand: ["wearysigh", "ojigi"] }, bowDeep: 0.14,
    holds: { /** a rice ball in his right hand, looked at; "There'll be a notice about all this." */ riceball: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.22 }, held: "riceball" };
      withArm(p, "R", { hand: [0.040, -0.150, 0.180], bend: [0.8, -0.6, -0.3], curl: 0.6, point: [-0.3, 0.3, 0.9], thumb: [0, 1, 0] }); return p; } },
    extras(c) { chonmageTop(c); kimono(c, { mat: SUMI, obi: NEZUMI, obiUp: 0.014, obiDown: 0.022, knot: "small", sleeve: 0.080, jacket: true }); daisho(c); tasselJitte(c); if (c.pose.held === "riceball") riceBall(c); },
  };
  // Tatsu, his thief-taker (okappiki: facts-edo-2 item 13): a townsman, the tasselless jitte in his sash (never drawn out);
  // nosy, sentimental; follows "three tall women in hats"; weeps at puppet plays, into his towel. A red-brown short jacket
  // over a kimono hitched up, grey leg wraps, a towel over his shoulder. `tatsu-seated`: cross-legged in the audience.
  const tatsuHolds = {
    /** peering hard, leaning in from the hips, the eyes screwed up */
    peer: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + (o.seated ? 0.16 : 0.26), head: { nod: nodOf(b) - 0.22, turn: 0.06 }, held: "peer", squeeze: false }; return p; },
    /** his towel held out to Mom, kindly */
    towel: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.10, turn: -0.20 }, held: "towel" };
      withArm(p, "R", { hand: [-0.020, o.seated ? -0.150 : -0.180, 0.240], bend: [0.8, -0.6, -0.3], grip: true, point: [-0.5, 0.0, 0.85] }); return p; },
    /** weeping into his towel, his head down */
    weep: (o) => { const b = o.base, hr = o.d.headR, p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, breath: 1, blink: true, head: { nod: nodOf(b) + 0.30 }, held: "weep" };
      withArm(p, "R", { hand: [0.020, o.sp.headY - hr[1] * 0.10, hr[2] + 0.040], bend: [1, -0.6, 0.2], grip: true, point: [-0.6, 0.6, 0.4] }); return p; },
  };
  const tatsuBase = {
    ...workman(EDO_SKIN, { dim: { shoulderW: 0.096 }, jacket: TOBI, trousers: NEZUMI, face: { eyes: "bright", jaw: 0.88, chin: 0.56, mouthW: 0.20, brow: { full: [0, -1, -1] } } }), ...wraps(NEZUMI),
    name: "Tatsu, the thief-taker", height: H(155),
    stance: "clasped", lean: 0.05, walk: { swing: 0.42, arm: 0.24, elbow: 0.40, lean: 0.10, lift: 1.0 }, pace: 150,
    gestures: [0, 5, 10, 0, 16], holds: tatsuHolds, ...bowOf(0.26),
  };
  const tatsuGear = (c) => { chonmageTop(c); kimono(c, { mat: TOBI, obi: NEZUMI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.040, jacket: true }); truncheon(c); const h = c.pose.held, f = c.pose.fidget;
    if (h === "towel" || h === "weep" || f === "dabeyes") towel(c, "R", 0.08); else shoulderTowel(c, SHIRO); };
  const tatsu = { ...tatsuBase, fidgets: { only: true, stand: ["shift", "look", "craneneck"] }, cues: { stand: ["craneneck", "dabeyes", "ojigi"] }, extras: tatsuGear };
  const tatsuSeated = { ...tatsuBase, name: "Tatsu, sitting in the audience", seated: "ground", sit: { lean: 0.08, nod: -0.04 }, shadow: 0.22, span: 1.3,
    fidgets: { only: true, sit: ["shift", "look", "dabeyes"], stand: ["shift", "look", "craneneck"] }, cues: { sit: ["dabeyes"] }, extras: tatsuGear };

  // The broadsheet sellers (yomiuri: facts-21d item 6): two men in deep woven hats (a costume, not a claim that they hid),
  // plain kimonos hitched up, leg wraps; a sheaf under the left arm, one sheet held up to chant from, in turn.
  const YOMIURI_SHEET = { R: { hand: [0.100, 0.020, 0.170], bend: [0.7, -0.7, -0.3], grip: true, point: [0.1, 0.8, 0.5] } };
  const yomiuri = (skin, height, name, mat, o = {}) => ({
    ...workman(skin, { dim: o.dim, face: o.face }), ...robe(mat, 1.50, { open: 0.030 }), ...wraps(o.wraps || AI), name, height, span: 1.25, crown: 0.02,
    hold: { L: { hand: [-0.030, -0.180, 0.020], bend: [-0.6, -0.8, -0.3], grip: true, point: [0.3, -0.5, 0.8] } },
    stance: "clasped", lean: 0.03, walk: { swing: 0.46, arm: 0.30, elbow: 0.40, lean: 0.08, lift: 1.1 }, pace: 165,
    gestures: [1, 11, 0, 9], fidgets: { only: true, stand: ["shift", "look", "wavesheet"] }, cues: { stand: ["wavesheet"] },
    holds: { /** chanting: the sheet held up in the right hand, the head up */ chant: (k) => { const b = k.base, p = { ...cloneP(b), mouth: 2, breath: 1, head: { nod: nodOf(b) - 0.12 }, held: "chant" }; withArm(p, "R", YOMIURI_SHEET.R); return p; } },
    extras(c) { chonmageTop(c); kimono(c, { mat, obi: o.obi || CHA, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.040 }); sheaf(c); deepHat(c, o.hat || SUGE);
      if (c.pose.held === "chant" || c.pose.fidget === "wavesheet" || (c.pose.gesture && c.pose.gesture !== 0)) heldSheet(c, "R", WASHI, SUMI_INK); },
  });
  const yomiuri1 = yomiuri(EDO_SKIN, H(157), "a broadsheet seller", AI, { face: { eyes: "plain", jaw: 0.88, chin: 0.56, mouthW: 0.24 } });
  const yomiuri2 = yomiuri(EDO_SUN, H(153), "a broadsheet seller (the second)", KAKI, { obi: AI_DEEP, wraps: NEZUMI, hat: SUGE_OLD, face: { eyes: "plain", jaw: 0.92, chin: 0.60, mouthW: 0.22 } });

  // Senzō, a printer in a publisher's shop on Shinsaibashi-suji: inky, cheerful, proud of the new blue. Sleeves tied back,
  // an apron, a towel round his head, Berlin blue on his fingers and a smudge of it on his cheek; found kneeling at his low
  // printing bench (getting up with sit(false)).
  const senzoInk = (c) => {
    const { sf, P, hp, J, th, hy, fine } = c;
    if (!fine) return;
    const blue = BEROAI.tones[1];
    for (const k of ["R", "L"]) { const q = P(J[k].tip); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), blue, c.parts.HAND[k]); }
    if (Math.cos(th + hy) > 0.3) { const q = P(hp(-0.50, -0.30, 0.86)); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), blue, c.parts.HEAD); }
  };
  const senzoHolds = {
    /** rubbing the back of the paper with the round pad (baren), bent over the bench */
    rub: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.34, head: { nod: nodOf(b) + 0.18 }, held: "rub" };
      withArm(p, "R", { hand: [0.040, -0.330, 0.260], bend: [0.8, -0.4, -0.4], flat: true, point: [0, -0.6, 0.8], thumb: [0, 1, 0] });
      withArm(p, "L", { hand: [-0.080, -0.330, 0.230], bend: [-0.8, -0.4, -0.4], flat: true, point: [0.2, -0.6, 0.8] }); return p; },
    /** a print held up in both hands to the light, admiring the blue */
    show: (o) => { const b = o.base, p = { ...cloneP(b), smile: 2, lean: (b.lean || 0) - 0.04, head: { nod: nodOf(b) - 0.12 }, held: "show" };
      for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.070, -0.020, 0.200], bend: [sd * 0.8, -0.6, -0.3], grip: true, point: [0, 0.8, 0.5] }); return p; },
    /** reading the broadsheet aloud, held in both hands before him */
    read: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.20 }, held: "read" };
      for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.060, -0.140, 0.190], bend: [sd * 0.9, -0.6, -0.3], grip: true, point: [0, 0.6, 0.8] }); return p; },
  };
  function baren(c) { const { J, ball, parts, tw } = c, g = add(J.R.palm, [0, -0.010, 0]); ball(g, [0.032, 0.010, 0.032], HINOKI, { part: parts.HELD, fn: (ux, uy) => (uy > 0 && Math.hypot(ux, 0) < 0.6 ? BAREN_PAD : undefined) }, tw); }
  function printBoth(c, sheet = WASHI, picture = BEROAI) {
    const { J, limb, parts } = c, a = add(J.L.palm, [0, 0.040, 0]), b2 = add(J.R.palm, [0, 0.040, 0]);
    limb(a, b2, 0.050, 0.050, sheet, { part: parts.HELD, depth: 0.06, squareStart: true, squareEnd: true, fn: (t, nx) => (t > 0.25 && t < 0.75 && Math.abs(nx) < 0.6 ? picture : undefined) });
  }
  const senzo = {
    ...workman(EDO_SKIN, { dim: { shoulderW: 0.098 }, jacket: AI, trousers: AI_DEEP, face: { eyes: "bright", smile: 1, jaw: 0.88, chin: 0.58, mouthW: 0.22, brow: { full: [0, -1, -1] } } }),
    name: "Senzō, the printer", height: H(156),
    seated: "ground", sit: { seat: "kneel", lean: 0.10, nod: 0.12 }, riseMs: 1300, shadow: 0.20, span: 1.2,
    stance: "clasped", walk: { swing: 0.44, arm: 0.30, elbow: 0.30, lean: 0.06, lift: 1.0 }, pace: 155,
    gestures: [4, 11, 9, 0, 18], fidgets: { only: true, sit: ["shift", "look", "rubbing"], stand: ["shift", "look"] }, holds: senzoHolds, cues: { sit: ["rubbing"], stand: ["ojigi"] }, ...bowOf(0.30),
    extras(c) { hachimaki(c, SHIRO, 0.44); chonmageTop(c); kimono(c, { mat: AI, obi: KAKI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0, jacket: true }); tasuki(c, SHIRO); apronOf(c, NEZUMI, 0.36); senzoInk(c);
      const h = c.pose.held, f = c.pose.fidget; if (h === "rub" || f === "rubbing") baren(c); if (h === "show") printBoth(c); if (h === "read") printBoth(c, WASHI, SUMI_INK); },
  };

  // The pilgrims in O-Natsu's line (facts-21b item 2: every pilgrim carried a ladle; facts-edo item 26: a hat marked with
  // the group's sign): an Awa family, the mother with a baby on her back; an old woman from Kii; a boy with a ladle bigger
  // than his face. One voice between them.
  const pilgrimHolds = { ladleout: (o) => { const b = o.base, q = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.08 }, held: "ladleout" }; withArm(q, "R", { hand: [0.080, -0.180, 0.230], bend: [0.6, -0.8, -0.2], grip: true, point: [0.1, 0.3, 0.95] }); return q; } };
  const LADLE_UP = { R: { hand: [0.090, -0.150, 0.130], bend: [0.7, -0.8, -0.3], grip: true, point: [0, 1, 0.2] } };
  const awafather = {
    ...workman(EDO_SUN, { dim: { shoulderW: 0.100 }, face: { eyes: "plain", jaw: 0.90, chin: 0.58, smile: 0.5 } }), ...robe(ASAGI, 1.56, { open: 0.030 }), ...wraps(AI),
    name: "a pilgrim from Awa", height: H(156), span: 1.2, hold: LADLE_UP,
    stance: "clasped", gestures: [0, 0, 20, 8], walk: { swing: 0.44, arm: 0.20, elbow: 0.30, lean: 0.07, lift: 1.0 }, pace: 145,
    fidgets: { only: true, stand: ["shift", "look"] }, holds: pilgrimHolds, cues: { stand: ["ojigi"] }, ...bowOf(0.30),
    extras(c) { chonmageTop(c); kimono(c, { mat: ASAGI, obi: CHA, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.050 }); markedHat(c, { r: 0.112 }); ladle(c, c.pose.held !== "ladleout"); },
  };
  const awamother = {
    ...WOMAN_EDO(EDO_SUN, AI, { face: { brows: null, smile: 0.5 }, len: 1.52, gestures: [0, 8, 0, 9], pace: 140, dim: { shoulderW: 0.084 } }), ...wraps(NEZUMI),
    name: "a pilgrim from Awa, with a baby on her back", height: H(145), span: 1.2, hold: LADLE_UP,
    stance: "clasped", walk: { swing: 0.40, arm: 0.20, elbow: 0.30, lean: 0.08, lift: 0.9, sway: 0.014 },
    fidgets: { only: true, stand: ["shift", "look", "jog"] }, holds: pilgrimHolds, cues: { stand: ["jog", "ojigi"] }, ...bowOf(0.30),
    extras(c) { kimono(c, { mat: AI, obi: KAKI, knot: "big", sleeve: 0.040 }); babyOnBack(c); markedHat(c, { r: 0.108 }); ladle(c, c.pose.held !== "ladleout"); },
  };
  const oldpilgrim = {
    ...WOMAN_EDO(OLD_SKIN, NEZUMI, { face: { brows: null, lines: 2, eyes: "heavy", jaw: 0.78, chin: 0.50 }, len: 1.56, gestures: [0, 5, 0, 8], pace: 100, dim: { shoulderW: 0.080, trunkTop: [0.086, 0.066], trunkLow: [0.080, 0.064] } }), ...wraps(SHIRO),
    name: "an old pilgrim from Kii", height: H(140), hair: { mat: EDO_GREY, bulk: [1.10, 1.02, 1.08], where: marumage, puffs: [[0, 0.96, -0.36, 0.36, 0.28, 0.38]] }, span: 1.25, hold: LADLE_UP,
    stance: "clasped", lean: 0.14, nod: 0.06, walk: { swing: 0.30, arm: 0.12, elbow: 0.30, lean: 0.16, lift: 0.7 },
    fidgets: { only: true, stand: ["shift", "look", "slownod"] }, holds: pilgrimHolds, cues: { stand: ["slownod", "ojigi"] }, ...bowOf(0.34),
    extras(c) { kimono(c, { mat: NEZUMI, obi: SUMI, knot: "big", sleeve: 0.050 }); markedHat(c, { r: 0.106 }); ladle(c, c.pose.held !== "ladleout"); },
  };
  /** The ladle boy's ladle: the cup bigger than his face. */
  function bigLadle(c, up = true) {
    const { J, limb, ball, parts } = c, g = J.R.palm, dir = up ? unit(add(J.R.hDir, [0, 1.2, 0])) : J.R.hDir;
    limb(add(g, mul(dir, -0.040)), add(g, mul(dir, 0.200)), 0.008, 0.008, TAKE, { part: parts.HELD });
    ball(add(g, mul(dir, 0.250)), [0.070, 0.052, 0.070], EDO_WOOD, { part: parts.HELD, fn: (ux, uy) => (uy < -0.4 ? shifted(EDO_WOOD, 1) : undefined) });
  }
  const ladleboy = {
    name: "a pilgrim boy with a big ladle", height: H(110),
    dim: { ...CHILD, headR: [0.072, 0.084, 0.080] }, skin: EDO_SUN,
    hair: { mat: EDO_HAIR, bulk: [1.08, 1.04, 1.08], where: boyhair, puffs: BOY_PUFFS, ears: true },
    face: { ...EDO_CHILD_FACE, eyes: "big", smile: 1 },
    top: { mat: KAKI, sleeves: 2, ease: 0.006, open: 0.030, under: WHITE }, bottom: { kind: "skirt", mat: KAKI, len: 1.10, flare: 1.08, wrap: [0.55, -0.30], under: KAKI },
    shoes: { kind: "sandals", mat: WARAJI, foot: EDO_SUN, sole: shifted(WARAJI, 1) }, span: 1.3, tall: 1.35,
    hold: { R: { hand: [0.080, -0.110, 0.140], bend: [0.7, -0.8, -0.3], grip: true, point: [0, 1, 0.2] } },
    stance: "clasped", walk: { swing: 0.50, arm: 0.40, elbow: 0.30, lean: 0.08, lift: 1.3, bob: 0.03 }, pace: 175,
    gestures: [0, 4, 0, 10], fidgets: { only: true, stand: ["shift", "look", "hop"] }, holds: { ladleout: (o) => { const b = o.base, q = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) - 0.04 }, held: "ladleout" }; withArm(q, "R", { hand: [0.070, -0.120, 0.230], bend: [0.6, -0.8, -0.2], grip: true, point: [0.1, 0.3, 0.95] }); return q; } },
    cues: { stand: ["hop"] },
    extras(c) { kimono(c, { mat: KAKI, obi: AI, obiUp: 0.028, obiDown: 0.024, knot: "small", sleeve: 0.040 }); sugegasa(c, { back: true, r: 0.10 }); bigLadle(c, c.pose.held !== "ladleout"); },
  };

  // =================================================================================
  // The Inari theatre: the chief puppeteer, the chanter, the shamisen player, and the boy puppet
  // =================================================================================
  // Three operators to a puppet (since 1734: facts-21b item 3). The doll stands on the boards over the stage rail
  // (PUPPET_RAIL: the rail's top over the operators' floor, to be set from PAINT-21D's layout), held by Jūbei from behind
  // (his left hand in its back at the head's grip, his right hand at its right hand), its left hand worked by the left-hand
  // operator and its feet by the feet operator, the two in black (the girls, in PEOPLE-21B's `edo-kurogo`). The three
  // operators stand where TROUPE says, from the doll's place, all facing the way it faces; every operator's holds (`doll`,
  // `dollear`, `dollrun`, `dollkneel`) put their hands where the doll's are in its own `ear`, `run` and `kneel`.
  const DOLL_M = 0.90;                                                    // the doll's height, in metres
  const PUPPET_RAIL = 86 * CM;                                            // the boards it stands on, over its operators' floor (as a seat's height: OFFICE-17P's standOn): the stage rail's top, 86 cm (PAINT-21D's theatre)
  const DOLL_FLOAT = 0.030;                                               // its feet off the boards (in its own heights: 2.7 cm) except when they stamp
  /** Where each operator stands, from the doll's place, in metres: [to the doll's right, forward]. */
  const TROUPE = { jubei: [0.00, -0.30], bigsis: [-0.36, -0.12], lilsis: [-0.18, -0.22] };
  const metresOf = (spec) => spec.height * 1.81;                           // (the rig's scale: 1 is Dad, 181 cm)

  // The boy puppet (`boypuppet`): a doll of about 0.9 m in a boy's clothes of the time (a short red kimono, a green sash,
  // straw sandals), its head, hands and feet carved and painted white, its hair black lacquer, its eyes painted on (they
  // never blink); a little stiff, a little floating (its feet just off the boards except when they stamp). It neither
  // breathes nor moves its lips (spec.doll: rig.js). Holds: `ear` (the left hand raised to the ear: hearing his mother),
  // `run` (a running stride, held), `kneel` (on its knees, the left hand down to the boards); the movement `dollrun` (a run
  // on the spot, the feet stamping); `stand` is the doll as it is (hold(false)). `boypuppet-stand`: the same doll on its
  // stand backstage, held at the same height, so that the operators' holds serve at rehearsal too.
  const DOLL_DIM = { ...CHILD, headR: [0.074, 0.084, 0.080], neckR: 0.82, armR: [0.024, 0.020, 0.015], legR: [0.040, 0.027, 0.018], trunkTop: [0.094, 0.062], trunkLow: [0.086, 0.064] };
  const dollHolds = {
    /** the boy hears his mother calling: the head lifts and turns to her, the left hand cupped behind the left ear */
    ear: (o) => { const b = o.base, hr = o.d.headR, p = { ...cloneP(b), raise: DOLL_FLOAT, lean: -0.04, head: { nod: -0.12, turn: 0.36 }, held: "ear" };
      withArm(p, "L", { hand: [-(hr[0] + 0.024), o.sp.headY - 0.060, -0.004], bend: [-1, -0.6, 0.3], flat: true, point: [0, 1, 0.25], thumb: [0, 0, 1] });
      withArm(p, "R", { arm: [0.20, 0.30], elbow: 0.30, flat: true });
      p.R = { ...p.R, leg: [-0.10, 0.06], knee: 0.06 }; p.L = { ...p.L, leg: [0.12, 0.06], knee: 0.10 }; return p; },
    /** he runs home: a long stride, held, the knees high, the arms going, off the boards */
    run: (o) => dollStride(o.base, 1, 1),
    /** he kneels at her door: down on his knees on the boards, the left hand on the boards before him, the head bowed */
    kneel: (o) => { const p = cloneP(poses.kneel(boypuppetBase, "stand", "back", 1)); delete p.ground;
      const k = { ...p, raise: 0, lean: 0.30, head: { nod: 0.30 }, held: "kneel" };
      withArm(k, "L", { hand: [-0.050, -(o.d.shoulderY - 0.02), 0.200], bend: [-0.7, -0.4, -0.5], flat: true, point: [0.1, -0.3, 0.95], thumb: [1, 0, 0] });
      return groundKneel(k); },
  };
  /** A stride of the doll's run: `side` 1 the right leg forward (-1 the left), `air` how far off the boards (1: the most). */
  function dollStride(b, side, air) {
    const R = side > 0 ? "R" : "L", L = side > 0 ? "L" : "R", p = { ...cloneP(b), raise: DOLL_FLOAT + 0.045 * air, lean: 0.14, head: { nod: -0.04, turn: 0 }, held: "run" };
    p[R] = { ...p[R], leg: [0.62, 0.04], knee: 0.95, foot: 0.30 }; p[L] = { ...p[L], leg: [-0.48, 0.04], knee: 1.05, foot: -0.30 };
    withArm(p, R, { arm: [-0.50, 0.12], elbow: 1.10, grip: true }); withArm(p, L, { arm: [0.50, 0.12], elbow: 1.50, grip: true });      // (the forward arm bent up: a child running, not pointing)
    return p;
  }
  /** The doll's feet down on the boards together, in the run (a stamp). */
  function dollStamp(b, side) {
    const R = side > 0 ? "R" : "L", L = side > 0 ? "L" : "R", p = { ...cloneP(b), raise: 0, lean: 0.10, head: { nod: 0.02 }, held: "run" };
    p[R] = { ...p[R], leg: [0.18, 0.06], knee: 0.30 }; p[L] = { ...p[L], leg: [-0.10, 0.06], knee: 0.24 };
    withArm(p, R, { arm: [-0.30, 0.12], elbow: 1.00, grip: true }); withArm(p, L, { arm: [0.50, 0.12], elbow: 1.10, grip: true });
    return p;
  }
  /** A kneeling pose on the ground: whatever is lowest (a knee, a shin, a foot) at the boards (as the rig's kneelPose finds it). */
  function groundKneel(p) {
    const J = moveKit.skeleton(DOLL_DIM, { ...p, ground: 0, raise: 0 });
    let low = Infinity;
    for (const k of ["R", "L"]) { const L = J[k]; low = Math.min(low, L.heel[1], L.ball[1], L.toe[1], L.knee[1] - DOLL_DIM.legR[1], L.ankle[1] - DOLL_DIM.legR[2]); }
    return { ...p, ground: low };
  }
  const DOLL_REST = { R: { arm: [0.16, 0.12], elbow: 0.22, curl: 0.7 }, L: { arm: [0.16, 0.12], elbow: 0.22, curl: 0.7 } };
  const boypuppetBase = {
    name: "the boy puppet", height: H(90), dim: DOLL_DIM, skin: DOLL_SKIN, doll: true, float: DOLL_FLOAT,
    hair: { mat: DOLL_HAIR, bulk: [1.10, 1.06, 1.10], where: boyhair, puffs: BOY_PUFFS, ears: true },
    face: { eyes: { at: 0, full: ["=="], thin: ["="] }, lid: DOLL_EYE, eye: DOLL_EYE, iris: DOLL_EYE, brows: DOLL_HAIR.tones[2], browW: 2, brow: { full: [0, 0] }, lip: "#c83c34", lips: null, mouthW: 0.14, nose: [0.55, 0.55, 0.6], eyeX: 0.42, eyeY: -0.04, mouthY: -0.64, jaw: 0.84, chin: 0.56, chinY: -0.54, chinZ: 0.44, blush: "#f2b4a0" },
    top: { mat: DOLL_KIMONO, sleeves: 2, ease: 0.008, open: 0.034, under: WHITE }, bottom: { kind: "skirt", mat: DOLL_KIMONO, len: 0.98, flare: 1.10, wrap: [0.55, -0.30], under: DOLL_KIMONO },
    shoes: { kind: "sandals", mat: WARAJI, foot: DOLL_SKIN, sole: shifted(WARAJI, 1) },
    rest: DOLL_REST, stance: undefined, lean: 0.0, kneel: { lean: 0.06, backLean: 0.04 },
    walk: { swing: 0.30, arm: 0.24, elbow: 0.20, lean: 0.02, lift: 0.7, bob: 0, wag: 0, twist: 0.04, sway: 0.004 }, pace: 120,
    gestures: [0, 0, 0, 0], fidgets: { only: true, stand: [] }, holds: dollHolds, cues: { stand: ["dollrun"] }, span: 1.3, tall: 2.2, shadow: 0.14,
    extras(c) { kimono(c, { mat: DOLL_KIMONO, obi: DOLL_OBI, obiUp: 0.034, obiDown: 0.026, knot: "small", sleeve: 0.045 }); if (c.spec.onStand) puppetStand(c); },
  };
  /** The doll's stand backstage: a post from a cross-foot on the floor up behind it to a short bar at its shoulders. */
  function puppetStand(c) {
    const { J, limb, d, parts } = c, lift = (c.spec.standOn || 0) / c.spec.height + (c.pose.raise ?? c.spec.float ?? 0), b = back(c);
    const floor = (y) => [J.hipC[0], y - lift, J.hipC[2] - b - 0.030];
    limb(floor(0.004), T(c, [0, -0.010, -(b + 0.030)]), 0.010, 0.009, EDO_WOOD, { part: parts.EXTRA3, squareStart: true });
    limb(T(c, [-0.090, -0.010, -(b + 0.030)]), T(c, [0.090, -0.010, -(b + 0.030)]), 0.009, 0.009, EDO_WOOD, { part: parts.EXTRA3, squareStart: true, squareEnd: true });
    limb([J.hipC[0] - 0.12, 0.010 - lift, J.hipC[2] - b - 0.030], [J.hipC[0] + 0.12, 0.010 - lift, J.hipC[2] - b - 0.030], 0.012, 0.012, EDO_WOOD, { part: parts.EXTRA3, squareStart: true, squareEnd: true });
    void d;
  }
  const boypuppet = { ...boypuppetBase, standOn: PUPPET_RAIL };
  const boypuppetStand = { ...boypuppetBase, name: "the boy puppet, on its stand backstage", standOn: PUPPET_RAIL, onStand: true, tall: 2.2, holds: dollHolds, cues: { stand: ["dollrun"] } };

  /** The doll's points for a pose of it (its back at the head's grip, its hands, its heels), in metres from its place on
      the operators' floor: [right, up, forward]. */
  function dollPointsOf(pose) {
    const spec = boypuppet, raise = spec.standOn / spec.height + (pose.raise ?? spec.float);
    const J = moveKit.skeleton(spec.dim, { ...pose, raise }), m = metresOf(spec), M = (v) => mul(v, m), d = spec.dim;
    const grip = add(J.spine(d.shoulderY - 0.040), J.torso([0, 0, -d.trunkTop[1] * 0.80]));
    return { back: M(grip), handR: M(J.R.palm), handL: M(J.L.palm), heelR: M(mix(J.R.heel, J.R.ankle, 0.5)), heelL: M(mix(J.L.heel, J.L.ankle, 0.5)), head: M(J.head) };
  }
  /** The doll's pose by name: null (standing), "ear", "run", "kneel"; and the moments of its run on the spot ("strideR",
      "stampR", "strideL", "stampL"). */
  const dollPose = (name) => {
    const b = poses.stand(boypuppet, 0);
    if (!name) return b;
    if (name === "strideR" || name === "strideL") return dollStride(b, name === "strideR" ? 1 : -1, 1);
    if (name === "stampR" || name === "stampL") return dollStamp(b, name === "stampR" ? 1 : -1);
    return poses.reach(boypuppet, 1, name);
  };
  const DOLL_POINTS = new Map();
  const dollPoints = (name) => { const key = name || "stand"; if (!DOLL_POINTS.has(key)) DOLL_POINTS.set(key, dollPointsOf(dollPose(name))); return DOLL_POINTS.get(key); };
  /** A hand placed at a point of the doll (in metres from the doll's place), for an operator standing at `at` (TROUPE):
      the point in the operator's own figure space, then in the torso's space of pose `p`. */
  function toDoll(o, p, at, point) {
    const m = metresOf(o.spec), fig = [(point[0] - at[0]) / m, point[1] / m - (o.spec.float || 0), (point[2] - at[1]) / m];      // (lifted by a float, as Jubei on his stage clogs)
    return moveKit.torsoOf(moveKit.skeleton(o.d, p))(fig);
  }
  // The three operators: where each stands (TROUPE), how they stand for each of the doll's poses (`body`: lean, knees, head;
  // what is not said is as they rest), and which of the doll's points each hand is at.
  const CROUCH = (b, k = 1) => ({ lean: 0.30 + 0.10 * k, head: { nod: -0.10 }, R: { ...b.R, leg: [1.10, 0.20], knee: 2.05, foot: 0.25, footYaw: 0.30 }, L: { ...b.L, leg: [0.70, 0.16], knee: 1.85, foot: 0.40, footYaw: 0.20 } });
  const legsOf = (b, q) => ({ R: { ...b.R, ...((q && q.R) || {}) }, L: { ...b.L, ...((q && q.L) || {}) } });
  const ROLES = {
    // Jūbei: his left hand in the doll's back, his right at its right hand; he leans over it, more as it runs and kneels.
    jubei: { at: TROUPE.jubei,
      body: (b, n) => { const q = { stand: { lean: 0.08, head: { nod: 0.24 } }, ear: { lean: 0.08, head: { nod: 0.16, turn: 0.20 } },
        run: { lean: 0.16, head: { nod: 0.24 }, R: { leg: [0.10, 0.06], knee: 0.20 }, L: { leg: [-0.04, 0.06], knee: 0.16 } },
        kneel: { lean: 0.30, head: { nod: 0.30 }, R: { leg: [0.40, 0.08], knee: 0.80 }, L: { leg: [0.30, 0.08], knee: 0.70 } } }[n]; return { ...q, ...legsOf(b, q) }; },
      hands: [["L", "back", { bend: [-0.8, -0.6, -0.4], grip: true, point: [0.4, 0.6, 0.6] }], ["R", "handR", { bend: [0.8, -0.6, -0.4], grip: true, point: [-0.2, -0.2, 0.95] }]] },
    // The left-hand operator (Big Sister): her right hand at the doll's left hand; she follows it up to its ear, and down.
    bigsis: { at: TROUPE.bigsis,
      body: (b, n) => { const q = { stand: { lean: 0.06, head: { nod: 0.20, turn: 0.30 } }, ear: { lean: 0.04, head: { nod: 0.04, turn: 0.36 } }, run: { lean: 0.12, head: { nod: 0.20, turn: 0.30 } },
        kneel: { lean: 0.40, head: { nod: 0.36, turn: 0.20 }, R: { leg: [0.30, 0.08], knee: 0.60 }, L: { leg: [0.20, 0.08], knee: 0.50 } } }[n]; return { ...q, ...legsOf(b, q) }; },
      hands: [["R", "handL", { bend: [0.8, -0.6, -0.4], grip: true, point: [0.2, 0.2, 0.95] }]] },
    // The feet operator (Little Sister): crouched low behind the doll, a hand at each of its heels.
    lilsis: { at: TROUPE.lilsis, rises: true, body: (b, n) => CROUCH(b, n === "kneel" ? 1.4 : 1),
      hands: [["R", "heelR", { bend: [0.8, -0.5, -0.4], grip: true, point: [0, 0.2, 0.95] }], ["L", "heelL", { bend: [-0.8, -0.5, -0.4], grip: true, point: [0, 0.2, 0.95] }]] },
  };
  /** Who someone is to the doll: the doll itself, the left-hand or the feet operator (any page of Big Sister's or Little
      Sister's), or (anyone else) the main operator. */
  const roleOf = (spec) => (spec.doll ? "doll" : spec === bigsis || spec.wears === "bigsis" ? "bigsis" : spec === lilsis || spec.wears === "lilsis" ? "lilsis" : "jubei");
  /** An operator's pose for one pose of the doll (`name`, as dollPose), standing as `bodyAs` says; bent lower, a step at
      a time (a deeper lean, the knees more bent), until every hand can reach its point; each hand placed so that its palm,
      not its wrist, is at the point. */
  function operatorPose(o, name, bodyAs) {
    const role = ROLES[roleOf(o.spec)], b = o.base, pts = dollPoints(name), d = o.d, reach = d.upperArm + d.foreArm - 0.012;
    let p;
    for (const dip of role.rises ? [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2] : [0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2]) {
      const body = role.body(b, bodyAs), up = role.rises ? -1 : 1;           // (the feet operator reaches up by rising out of her crouch; the others reach down by bending lower)
      p = { ...cloneP(b), ...body, lean: Math.max(0, (body.lean ?? b.lean ?? 0) + 0.40 * dip * (role.rises ? -0.5 : 1)) };
      for (const s of ["R", "L"]) { const q = p[s] || {}; p[s] = { ...q, leg: [Math.max(0, ((q.leg && q.leg[0]) || 0) + 0.50 * dip * up), (q.leg && q.leg[1]) ?? 0.06], knee: Math.max(0.02, (q.knee || 0) + 1.00 * dip * up) }; }
      let ok = true;
      for (const [side, where, how] of role.hands) {
        const want = toDoll(o, p, role.at, pts[where]), dir = unit(how.point || [0, -1, 0]), palm = d.handR * 3.4 * 0.5;
        const hand = sub(want, mul(dir, palm)), sl = [side === "R" ? d.shoulderW : -d.shoulderW, -(d.shoulderDrop ?? 0.046), 0];
        if (Math.hypot(hand[0] - sl[0], hand[1] - sl[1], hand[2] - sl[2]) > reach && (role.rises ? hand[1] > sl[1] : hand[1] < sl[1])) ok = false;      // (bending lower helps only a point below the shoulder; rising, only one above it)
        withArm(p, side, { ...how, hand });
      }
      if (ok) break;
    }
    return p;
  }
  const POSES = [null, "ear", "run", "kneel"];
  const holdName = (n) => "doll" + (n || "");
  /** The holds that work the doll, for whoever holds them (Jūbei, Big Sister, Little Sister): `doll` (it stands), `dollear`,
      `dollrun`, `dollkneel`. */
  const OPERATOR_HOLDS = Object.fromEntries(POSES.map((n) => [holdName(n), (o) => ({ ...operatorPose(o, n, n || "stand"), held: holdName(n) })]));
  /** Give a page of Big Sister or Little Sister the holds that work the doll (whatever they wear: the girls are in black,
      PEOPLE-21B's edo-kurogo, when they do it). Called on every page in the people table (below the table). */
  function giveDollHolds(s) {
    const who = roleOf(s);
    if ((who !== "bigsis" && who !== "lilsis") || s.pitch) return;     // (not lying down)
    s.holds = { ...(s.holds || {}), ...OPERATOR_HOLDS };
    s.cues = { ...(s.cues || {}), stand: [...new Set([...((s.cues && s.cues.stand) || []), "dollrun"])] };
  }

  // Jūbei, the chief puppeteer of the troupe at the Inari theatre: stern, precise, kind under it; the one operator whose
  // face shows. Black kimono and black hakama, a white under-collar; found standing, arms folded. (The look of an 1830
  // puppeteer is not in the sources: the game's.)
  const jubei = {
    ...samurai(EDO_SKIN, H(158), "Jūbei, the chief puppeteer", { dim: { shoulderW: 0.098 }, jacket: SUMI, hakama: SUMI, stance: "folded", gestures: [0, 1, 11, 10, 0],
      face: { eyes: "deep", lines: 2, jaw: 0.90, chin: 0.58, mouthW: 0.18, brow: { full: [1, 0, -1] } } }),
    hair: { mat: EDO_HAIR, bulk: [1.06, 1.0, 1.06], where: chonmage }, top: { mat: SUMI, sleeves: 2, ease: 0.008, open: 0.040, under: WHITE },
    lean: 0.02, walk: { swing: 0.40, arm: 0.14, elbow: 0.30, lean: 0.03, lift: 0.9 }, pace: 135,
    fidgets: { only: true, stand: ["shift", "look", "fold"] }, cues: { stand: ["fold", "ojigi", "dollrun"] }, bowDeep: 0.30,
    holds: { ...OPERATOR_HOLDS,
      /** "Not yet.": a finger to his lips, a hiss */ hiss: (o) => { const b = o.base, hr = o.d.headR, p = { ...cloneP(b), lean: (b.lean || 0) + 0.04, head: { nod: nodOf(b) + 0.04, turn: 0.30 }, held: "hiss" };
        withArm(p, "R", { hand: [0.010, o.sp.chinY + 0.004, hr[2] + 0.030], bend: [1, -0.6, 0.2], finger: true, point: [0, 0.9, 0.3] }); return p; },
      /** "Watch his head, not me.": pointing at the doll's head in front of him */ teach: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.14, turn: -0.20 }, held: "teach" };
        withArm(p, "R", { arm: [0.85, 0.10], elbow: 0.40, finger: true }); return p; },
    },
    extras(c) { chonmageTop(c); kimono(c, { mat: SUMI, obi: SUMI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.060 }); },
  };
  /** Tall stage clogs under each foot (Jūbei's for the show, `jubei-stage`): blocks of black wood the height of his float,
      going with his feet. (Stage clogs for the main operator are the game's choice: the sources do not give them.) */
  function stageClogs(c) {
    const { J, limb, d, parts, spec } = c, h = spec.float || 0;
    for (const k of ["R", "L"]) {
      const L = J[k], mid = mix(L.heel, L.ball, 0.45), sole = Math.min(L.heel[1], L.ball[1]) - d.ankleH * 0.25, r = c.wide([d.footR * 1.25, d.foot * 0.48]);
      limb([mid[0], sole, mid[2]], [mid[0], sole - h, mid[2]], r, r, LACQUER, { part: parts.FOOT[k], depth: c.deep([d.footR * 1.25, d.foot * 0.48]) / r, squareStart: true, squareEnd: true });
    }
  }
  const JUBEI_GETA = 0.15;                                                // his clogs' height, in his own heights (24 cm)
  const jubeiStage = { ...jubei, name: "Jūbei, on his stage clogs", float: JUBEI_GETA, tall: 1.35, pace: 110, walk: { ...jubei.walk, swing: 0.30, lift: 0.7 },
    extras(c) { jubei.extras(c); stageClogs(c); } };
  // The chanter (tayū) and the shamisen player: seen, not heard as words (the chanter's cues are lines of the game's own);
  // kneeling on their dais, in formal vests with stiff shoulders over their kimonos (the look is the game's).
  const chanter = {
    ...workman(OLD_SKIN, { dim: { shoulderW: 0.100, bellyFwd: 0.012 }, face: { eyes: "heavy", lines: 2, jaw: 0.94, chin: 0.62, mouthW: 0.24, brow: { full: [1, 1, 0] } } }), ...robe(NEZUMI, 1.90, { open: 0.030 }),
    name: "the chanter", height: H(156), span: 1.3,
    seated: "ground", sit: { seat: "kneel", lean: 0.06, nod: 0.02 }, riseMs: 1500, shadow: 0.22,
    gestures: [9, 4, 18, 1], fidgets: { only: true, sit: ["shift", "chanting", "chanting"], stand: ["shift", "look"] }, cues: { sit: ["chanting", "turnpage"] },
    holds: { /** chanting, the voice full out: leaning forward, the mouth wide, a hand gripping his knee */ chant: (o) => { const b = o.base, p = { ...cloneP(b), mouth: 2, breath: 1, lean: (b.lean || 0) + 0.14, head: { nod: nodOf(b) - 0.06 }, held: "chant" };
      withArm(p, "R", { hand: [0.070, -0.280, 0.230], bend: [0.8, -0.4, -0.4], grip: true }); return p; } },
    extras(c) { chonmageTop(c); kimono(c, { mat: NEZUMI, obi: SUMI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.060 }); kataginu(c, SABI); },
  };
  const SHAMISEN_HANDS = { R: { hand: [0.070, -0.240, 0.140], bend: [0.8, -0.5, -0.4], grip: true, point: [-0.4, -0.5, 0.7] }, L: { hand: [-0.120, -0.090, 0.130], bend: [-0.8, -0.6, -0.3], curl: 0.9, point: [0.3, 0.6, 0.7] } };
  const shamisen = {
    ...workman(EDO_PALE, { dim: { shoulderW: 0.096 }, face: { eyes: "plain", lines: 1, jaw: 0.86, chin: 0.54, mouthW: 0.18 } }), ...robe(NEZUMI, 1.90, { open: 0.030 }),
    name: "the shamisen player", height: H(155), span: 1.35,
    seated: "ground", sit: { seat: "kneel", lean: 0.04, nod: 0.10 }, riseMs: 1500, shadow: 0.22, hold: SHAMISEN_HANDS,
    gestures: [0, 0, 0, 0], fidgets: { only: true, sit: ["pluck", "pluck", "shift"], stand: ["shift", "look"] }, cues: { sit: ["pluck"] },
    extras(c) { chonmageTop(c); kimono(c, { mat: NEZUMI, obi: SUMI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.060 }); kataginu(c, SABI); if (c.pose.seated) shamisenOf(c); },
  };

  // ---- their own small movements (figure.fidget(name)) ----
  addMoves({
    /** O-Kuni: turns the shells on the grill in front of her with her chopsticks, bent to it, twice */
    turnshells: { ms: 2600, make(o) {
      const b = o.base, at = (dx, dy) => withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.22, head: { nod: nodOf(b) + 0.22 } }, "R", { hand: [0.050 + dx, -0.300 + dy, 0.220], bend: [0.8, -0.6, -0.3], grip: true, point: [0, -0.7, 0.7] });
      return [[0, b], [0.20, at(0, 0)], [0.34, at(-0.030, 0.020)], [0.48, at(0.010, 0)], [0.62, at(-0.030, 0.020)], [0.78, at(0, 0)], [1, b]];
    } },
    /** O-Kuni: fans the coals with a round fan in her left hand, quick */
    fanfire: { ms: 2200, make(o) {
      const b = o.base, at = (dy) => withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.16, head: { nod: nodOf(b) + 0.20, turn: -0.10 } }, "L", { hand: [-0.060, -0.250 + dy, 0.200], bend: [-0.8, -0.6, -0.3], flat: true, point: [0.2, -0.3, 0.9] });
      return [[0, b], [0.18, at(0)], [0.30, at(0.040)], [0.42, at(0)], [0.54, at(0.040)], [0.66, at(0)], [0.78, at(0.040)], [1, b]];
    } },
    /** Sakuji: jabs a finger at his partner as he talks, the mouth going */
    jab: { ms: 2000, make(o) {
      const b = o.base, at = (k) => withArm({ ...cloneP(b), mouth: k ? 2 : 1, head: { nod: nodOf(b) - 0.06, turn: -0.40 } }, "R", { arm: [0.90 + k * 0.10, -0.40], elbow: 0.40 - k * 0.20, finger: true });
      return [[0, b], [0.20, at(0)], [0.32, at(1)], [0.44, at(0)], [0.56, at(1)], [0.68, at(0)], [1, b]];
    } },
    /** Sakuji: rubs his hands together: a fare in the offing */
    farerub: { ms: 1800, make(o) {
      const b = o.base, at = (dx) => { const p = { ...cloneP(b), smile: 2, head: { nod: nodOf(b) + 0.04 } }; withArm(p, "R", { hand: [0.010 + dx, -0.190, 0.200], bend: [0.9, -0.5, -0.3], flat: true, point: [-0.9, 0.1, 0.3] }); return withArm(p, "L", { hand: [-0.010 + dx, -0.200, 0.190], bend: [-0.9, -0.5, -0.3], flat: true, point: [0.9, 0.1, 0.3] }); };
      return [[0, b], [0.24, at(0.012)], [0.40, at(-0.012)], [0.56, at(0.012)], [0.72, at(-0.012)], [1, b]];
    } },
    /** Tora: scratches the back of his big head, sheepish */
    scratchhead: { ms: 2200, make(o) {
      const b = o.base, hr = o.d.headR, at = (dy) => withArm({ ...cloneP(b), smile: 1, head: { nod: nodOf(b) + 0.12, turn: -0.10 } }, "R", { hand: [0.030, o.sp.headY + hr[1] * 0.50 + dy, -hr[2] * 0.40], bend: [1, 0.4, 0.1], curl: 0.7, point: [-0.5, 0.6, -0.4] });
      return [[0, b], [0.26, at(0)], [0.40, at(0.016)], [0.54, at(0)], [0.68, at(0.016)], [1, b]];
    } },
    /** the komusō, playing: a slow sway with the phrase, the basket dipping and rising */
    fluteplay: { ms: 3600, make(o) {
      const b = o.base, at = (n, sw) => ({ ...cloneP(b), sway: sw, head: { nod: nodOf(b) + n, turn: sw * 4 }, lean: (b.lean || 0) + n * 0.2 });
      return [[0, b], [0.25, at(0.10, 0.006)], [0.50, at(-0.04, -0.004)], [0.75, at(0.08, 0.004)], [1, b]];
    } },
    /** the courier, stopped a moment: bent forward, catching his breath */
    pant: { ms: 2400, make(o) {
      const b = o.base, at = (br) => ({ ...withArm({ ...cloneP(b), breath: br, mouth: 1, lean: (b.lean || 0) + 0.24, head: { nod: nodOf(b) - 0.14 } }, "L", { hand: [-(o.d.hipW + 0.020), -(o.d.shoulderY - o.d.hipY) - 0.100, 0.150], bend: [-0.6, -0.3, -0.6], flat: true }) });
      return [[0, b], [0.20, at(1)], [0.34, at(0)], [0.48, at(1)], [0.62, at(0)], [0.76, at(1)], [1, b]];
    } },
    /** Mosuke: hitches the load up on his back, a shrug and a bounce from the knees */
    hitchload: { ms: 1700, make(o) {
      const b = o.base, p = { ...cloneP(b), breath: 1, rise: -0.012, lean: (b.lean || 0) + 0.06, R: { ...b.R, knee: (b.R.knee || 0) + 0.24 }, L: { ...b.L, knee: (b.L.knee || 0) + 0.24 }, head: { nod: nodOf(b) + 0.06 } };
      const q = { ...cloneP(b), breath: 1, rise: 0.006, lean: (b.lean || 0) - 0.02 };
      return [[0, b], [0.30, p], [0.55, q], [1, b]];
    } },
    /** O-Shige: catching her breath after the climb, a hand on her chest */
    puff: { ms: 2600, make(o) {
      const b = o.base, at = (br) => withArm({ ...cloneP(b), breath: br, mouth: 1, lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) - 0.10 } }, "R", { hand: [-0.020, -0.080, o.sp.chest + 0.030], bend: [1, -0.6, 0], flat: true });
      return [[0, b], [0.20, at(1)], [0.36, at(0)], [0.52, at(1)], [0.68, at(0)], [1, b]];
    } },
    /** O-Shige, sitting: fans herself with her folding fan */
    fanself: { ms: 2400, make(o) {
      const b = o.base, at = (dx) => withArm({ ...cloneP(b), head: { nod: nodOf(b) - 0.08, turn: 0.10 } }, "R", { hand: [0.050 + dx, o.sp.chinY - 0.040, 0.130], bend: [0.9, -0.6, -0.2], grip: true, point: [-0.2, 0.9, 0.3] });
      return [[0, b], [0.16, at(0.020)], [0.30, at(-0.020)], [0.44, at(0.020)], [0.58, at(-0.020)], [0.72, at(0.020)], [1, b]];
    } },
    /** Kyūzō: pats his sash, looking for something he is sure he had */
    patsash: { ms: 2400, make(o) {
      const b = o.base, at = (dy, turn) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.24, turn } }, "L", { hand: [-0.030, -(o.d.shoulderY - o.d.waistY) - 0.010 + dy, o.sp.belly + 0.030], bend: [-1, -0.4, -0.2], flat: true });
      return [[0, b], [0.24, at(0, 0.10)], [0.40, at(-0.030, -0.10)], [0.56, at(0, 0.10)], [0.72, at(-0.020, -0.10)], [1, b]];
    } },
    /** Kanbei: rubs his tired eyes with a thumb and finger */
    rubeyes: { ms: 2200, make(o) {
      const b = o.base, hr = o.d.headR, at = (dx) => withArm({ ...cloneP(b), blink: true, head: { nod: nodOf(b) + 0.14 } }, "R", { hand: [0.006 + dx, o.sp.headY - hr[1] * 0.10, hr[2] + 0.034], bend: [1, -0.6, 0.2], curl: 0.8, point: [-0.6, 0.6, 0.4] });
      return [[0, b], [0.26, at(0.008)], [0.42, at(-0.008)], [0.58, at(0.008)], [0.74, at(-0.008)], [1, b]];
    } },
    /** Denzō: knocks twice on the wood beside him (he would rather be safe) */
    knockwood: { ms: 1800, make(o) {
      const b = o.base, at = (dz) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.04, turn: 0.50 } }, "R", { hand: [0.200, -0.100, 0.120 + dz], bend: [1, -0.5, -0.3], grip: true, point: [0.8, 0, 0.6] });
      return [[0, b], [0.26, at(0)], [0.36, at(0.030)], [0.46, at(0)], [0.56, at(0.030)], [1, b]];
    } },
    /** Denzō: looks up at the sail, a long uneasy look: has she chirped? */
    skyward: { ms: 2800, make(o) {
      const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.06, head: { nod: nodOf(b) - 0.40, turn: 0.10 } }, q = { ...cloneP(b), lean: (b.lean || 0) - 0.06, head: { nod: nodOf(b) - 0.36, turn: -0.20 } };
      return [[0, b], [0.24, p], [0.54, q], [0.80, q], [1, b]];
    } },
    /** Seijirō: flicks beads on his abacus, the head down to it */
    clickbeads: { ms: 2400, make(o) {
      const b = o.base, at = (dx) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.22 } }, "R", { hand: [0.010 + dx, -0.180, 0.190], bend: [0.9, -0.5, -0.3], finger: true, point: [-0.6, -0.4, 0.6] });
      return [[0, b], [0.18, at(0)], [0.30, at(0.020)], [0.42, at(-0.010)], [0.54, at(0.024)], [0.66, at(0)], [1, b]];
    } },
    /** Kōta: lifts the pot's lid to look (he cannot help it), and puts it back */
    peeklid: { ms: 2600, make(o) {
      const b = o.base, at = (dy, n) => { const p = { ...cloneP(b), lean: (b.lean || 0) + 0.30, head: { nod: nodOf(b) + n } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.060, -0.250 + dy, 0.220], bend: [sd * 0.9, -0.6, -0.3], curl: 0.7, point: [-sd * 0.6, -0.3, 0.7], thumb: [0, 1, 0] }); return p; };
      return [[0, b], [0.22, at(-0.030, 0.24)], [0.36, at(0.030, 0.30)], [0.64, at(0.030, 0.30)], [0.78, at(-0.030, 0.24)], [1, b]];
    } },
    /** Kōta: stirs (a paddle in a pot in front of him), round and round */
    stirpot: { ms: 2600, make(o) {
      const b = o.base, at = (dx, dz) => withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.24, head: { nod: nodOf(b) + 0.24 } }, "R", { hand: [0.040 + dx, -0.200, 0.220 + dz], bend: [0.9, -0.5, -0.3], grip: true, point: [-0.2, -0.8, 0.5] });
      return [[0, b], [0.16, at(0.030, 0)], [0.32, at(0, 0.030)], [0.48, at(-0.030, 0)], [0.64, at(0, -0.030)], [0.80, at(0.030, 0)], [1, b]];
    } },
    /** Kōta: a laugh out loud at last, the head back, the shoulders going */
    laughout: { ms: 2200, hold: 0.5, make(o) {
      const b = o.base, at = (br, n) => ({ ...cloneP(b), smile: 2, mouth: 2, breath: br, lean: (b.lean || 0) - 0.06, head: { nod: nodOf(b) - n } });
      return [[0, b], [0.20, at(1, 0.20)], [0.34, at(0, 0.14)], [0.48, at(1, 0.20)], [0.62, at(0, 0.14)], [1, b]];
    } },
    /** a sailor at the windlass: heaves on the bar, twice (holdable: leaning into it) */
    heave: { ms: 2600, hold: 0.30, make(o) {
      const p = BAR(o, 0), q = BAR(o, 0.14);
      return [[0, o.base], [0.18, p], [0.32, q], [0.48, p], [0.64, q], [0.80, p], [1, o.base]];
    } },
    /** O-Natsu: serves: the paddle down into the pot, a scoop, up and over */
    serve: { ms: 2400, make(o) {
      const b = o.base, at = (dy, dz, n) => withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.20, head: { nod: nodOf(b) + n } }, "R", { hand: [0.060, -0.260 + dy, 0.220 + dz], bend: [0.8, -0.5, -0.4], grip: true, point: [0, -0.7, 0.7] });
      return [[0, b], [0.22, at(-0.030, 0, 0.26)], [0.40, at(0.010, 0.020, 0.22)], [0.58, at(0.050, 0.060, 0.12)], [0.76, at(0.030, 0.060, 0.10)], [1, b]];
    } },
    /** Rihei: bidding: the hands up and down, the fingers changing, the head going */
    bidding: { ms: 2400, make(o) {
      const b = o.base, at = (k, t) => { const p = { ...cloneP(b), mouth: 2, breath: 1, head: { nod: nodOf(b) - 0.12, turn: t } }; withArm(p, "R", { arm: [2.2 + k * 0.3, 0.40], elbow: 0.50, finger: k > 0, flat: k <= 0 }); return withArm(p, "L", { arm: [1.0 + k * 0.4, 0.40], elbow: 0.90, flat: true }); };
      return [[0, b], [0.20, at(0, 0.20)], [0.38, at(1, -0.10)], [0.56, at(0, 0.10)], [0.74, at(1, -0.20)], [1, b]];
    } },
    /** Rihei: shakes the water off, splashed again */
    shakewet: { ms: 1800, make(o) {
      const b = o.base, at = (sw) => { const p = { ...cloneP(b), sway: sw, blink: true, breath: 1, head: { nod: nodOf(b) + 0.06, turn: sw * 12 } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { arm: [0.30, 0.50], elbow: 0.60, flat: true }); return p; };
      return [[0, b], [0.18, at(0.012)], [0.30, at(-0.012)], [0.42, at(0.012)], [0.54, at(-0.012)], [0.66, at(0.008)], [1, b]];
    } },
    /** Kurata: a tired sigh: the shoulders up and down, the head drops */
    wearysigh: { ms: 2400, make(o) {
      const b = o.base, up = { ...cloneP(b), breath: 1, head: { nod: nodOf(b) - 0.08 } }, down = { ...cloneP(b), breath: 0, blink: true, lean: (b.lean || 0) + 0.04, head: { nod: nodOf(b) + 0.20 } };
      return [[0, b], [0.30, up], [0.56, down], [0.80, down], [1, b]];
    } },
    /** Tatsu: cranes his neck, looking over the crowd for three tall women in hats */
    craneneck: { ms: 2600, make(o) {
      const b = o.base, at = (t) => ({ ...cloneP(b), rise: 0.008, lean: (b.lean || 0) - 0.02, head: { nod: nodOf(b) - 0.16, turn: t }, R: { ...b.R, foot: -0.40 }, L: { ...b.L, foot: -0.40 } });
      return [[0, b], [0.22, at(0.40)], [0.46, at(0.40)], [0.64, at(-0.30)], [0.84, at(-0.30)], [1, b]];
    } },
    /** Tatsu: wipes his eyes with his towel (a sad play; any sad play) */
    dabeyes: { ms: 2400, make(o) {
      const b = o.base, hr = o.d.headR, at = (dx) => withArm({ ...cloneP(b), blink: true, breath: 1, head: { nod: nodOf(b) + 0.24 } }, "R", { hand: [0.020 + dx, o.sp.headY - hr[1] * 0.10, hr[2] + 0.040], bend: [1, -0.6, 0.2], grip: true, point: [-0.6, 0.6, 0.4] });
      return [[0, b], [0.26, at(0.010)], [0.42, at(-0.010)], [0.58, at(0.010)], [0.74, at(-0.010)], [1, b]];
    } },
    /** a broadsheet seller: waves the sheet up over the heads of the crowd */
    wavesheet: { ms: 2000, make(o) {
      const b = o.base, at = (k) => withArm({ ...cloneP(b), mouth: 2, head: { nod: nodOf(b) - 0.14 } }, "R", { arm: [2.40 + k * 0.30, 0.30 - k * 0.10], elbow: 0.30, grip: true, point: [0, 1, 0.2] });
      return [[0, b], [0.20, at(0)], [0.36, at(1)], [0.52, at(0)], [0.68, at(1)], [1, b]];
    } },
    /** Senzō: rubs the paper with the round pad, round and round, bent to the bench */
    rubbing: { ms: 2800, make(o) {
      const b = o.base, at = (dx, dz) => withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.30, head: { nod: nodOf(b) + 0.20 } }, "R", { hand: [0.040 + dx, -0.320, 0.250 + dz], bend: [0.8, -0.4, -0.4], flat: true, point: [0, -0.6, 0.8], thumb: [0, 1, 0] });
      return [[0, b], [0.16, at(0.030, 0)], [0.32, at(0, 0.030)], [0.48, at(-0.030, 0)], [0.64, at(0, -0.030)], [0.80, at(0.030, 0)], [1, b]];
    } },
    /** the chanter: a phrase chanted out, the head going with it, the mouth wide and closing */
    chanting: { ms: 2800, make(o) {
      const b = o.base, at = (m, n, l) => ({ ...cloneP(b), mouth: m, breath: m ? 1 : 0, lean: (b.lean || 0) + l, head: { nod: nodOf(b) + n } });
      return [[0, b], [0.16, at(2, -0.10, 0.08)], [0.36, at(1, 0.06, 0.12)], [0.56, at(2, -0.06, 0.10)], [0.76, at(1, 0.10, 0.04)], [1, b]];
    } },
    /** the chanter: turns a page of the book on his lectern */
    turnpage: { ms: 1800, make(o) {
      const b = o.base, at = (dx) => withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.12, head: { nod: nodOf(b) + 0.20 } }, "R", { hand: [0.060 + dx, -0.200, 0.260], bend: [0.8, -0.5, -0.4], curl: 0.5, point: [-0.6, -0.4, 0.6] });
      return [[0, b], [0.30, at(0.040)], [0.62, at(-0.050)], [1, b]];
    } },
    /** the shamisen player: two strokes of the plectrum */
    pluck: { ms: 1600, make(o) {
      const b = o.base, R = b.R, at = (dy) => ({ ...cloneP(b), head: { nod: nodOf(b) + 0.04 }, R: { ...R, hand: add(R.hand || [0.070, -0.240, 0.140], [0, dy, 0]) } });
      return [[0, b], [0.18, at(0.050)], [0.32, at(-0.020)], [0.52, at(0.050)], [0.68, at(-0.020)], [1, b]];
    } },
    /** the boy puppet runs on the spot (a stride, a stamp, the other stride, a stamp, twice; off the boards between the
        stamps), and the same movement on each of its three operators keeps them with it, in step: Jūbei's hands go with its
        back and its right hand, the left-hand operator's with its left hand, and the feet operator's with its heels, her
        body dipping at each stamp (she is the sound of it). Play it on all four at once; let their holds go first. */
    dollrun: { ms: 2400, hold: 0.10, make(o) {
      const T8 = [0.10, 0.22, 0.34, 0.46, 0.58, 0.70, 0.82, 0.92], NAMES = ["strideR", "stampR", "strideL", "stampL", "strideR", "stampR", "strideL", "stampL"];
      if (o.spec.doll) {
        const b0 = { ...cloneP(o.base), raise: DOLL_FLOAT };
        return [[0, b0], ...T8.map((t, i) => [t, { ...dollPose(NAMES[i]), held: "run" }]), [1, b0]];
      }
      const key = (n) => { const p = operatorPose(o, n, "run"); if (roleOf(o.spec) === "lilsis" && n.startsWith("stamp")) { p.rise = -0.012; p.head = { nod: -0.02 }; } return p; };
      return [[0, o.base], ...T8.map((t, i) => [t, key(NAMES[i])]), [1, o.base]];
    } },
  });

  return {
    kinds: {
      kuni, sakuji, tora, soshichi, "soshichi-free": soshichiFree, komuso, "komuso-play": komusoPlay, courier,
      mosuke, shige, "shige-stone": shigeStone, kyuzo, "kyuzo-nopass": kyuzoNopass,
      kanbei, denzo, seijiro, kota, kako1, kako2,
      natsu, "natsu-nocomb": natsuNocomb, rihei, kyuhachi, kurata, tatsu, "tatsu-seated": tatsuSeated, yomiuri1, yomiuri2, senzo,
      jubei, "jubei-stage": jubeiStage, chanter, shamisen, awafather, awamother, oldpilgrim, ladleboy,
      boypuppet, "boypuppet-stand": boypuppetStand,
    },
    // (not people: the doll's geometry, for the engine and the scenes; and the girls' holds, given below the table)
    TROUPE, PUPPET_RAIL, DOLL_FLOAT, DOLL_M, dollPoints, giveDollHolds,
  };
})();

// ===================================================================================== PEOPLE-21B (begin)
// PEOPLE-21B (round twenty-one): Act Six made bigger. The people of the Akashi shore, of Himeji town and of the women's
// hall at the foot of Mount Shosha; the girls' black robes and hoods (the outfit `edo-kurogo`, for the puppet show); the
// family's holds for the act's new things (the paddle, the rice balls, the comb, the pin, the coin, the ladle, the crab,
// the lantern, the broadsheet, the slips); Little Sister wading (her boots in the water: `edo-wading`); the octopus and the
// crab, as held things. Everyone is our own: nobody's likeness. How a script calls each pose is in docs/DESIGN.md, section
// 4 ("Act Six made bigger: the people of Akashi, Himeji and Shosha").
//   Real sizes: a thing held is drawn at its own size in metres (M: metres to the holder's own heights), so that the same
//   lantern is bigger in Little Sister's hand than in Mom's.

/** Metres, in the holder's own heights (the rig's scale: Dad at 1.0 is about 181 cm). */
const M = (c, metres) => metres / ((c.spec.height || 1) * 1.81);

// ---- materials ----
const KUROGO = ramp("#50505e", "#2c2c36", "#1c1c24", "#0e0e14");          // the puppeteers' black: cotton, a little blue in it
const KUROGO_VEIL = ramp("#5a5a6c", "#3a3a46", "#282832", "#16161c");     // the gauze over the face: a shade lighter than the hood
const OCTO = ramp("#e8a494", "#c06c5c", "#8c463e", "#5a2a26");            // a live octopus: a mottled red-brown
const OCTO_PALE = ramp("#f6d0c2", "#e0a090", "#b06e62", "#74443c");       // (its suckers and its mottle)
const CRAB_SHELL = ramp("#f49464", "#d05c34", "#983c22", "#622414");      // a small shore crab
const SHAMOJI = ramp("#f8e6bc", "#e2c690", "#b29664", "#78663e");         // a rice paddle: pale wood, scrubbed
const RICE = ramp("#ffffff", "#f8f6ee", "#d6d2c2", "#a09c8c");            // rice
const TAKUAN = ramp("#fff4a6", "#f2d662", "#c4a63a", "#84701e");          // pickled radish: yellow
const BAMBOO_LEAF = ramp("#b8d080", "#8aa852", "#607a34", "#3c501e");     // the leaf a rice ball sits on
const TSUGE = ramp("#fae4a8", "#e2c47e", "#b2924e", "#78622e");           // boxwood: a comb
const KANZASHI = ramp("#fff2c4", "#e6c470", "#b08c3c", "#705820", { shine: true });      // O-Tami's hairpin: brass
const MON = ramp("#ecbc94", "#c48a58", "#905e34", "#5c3a1c");             // a one-mon coin: copper
const CHOCHIN = ramp("#fffcea", "#ffeaa8", "#ecbc68", "#ac7c3a", { shine: true });       // a paper lantern, lit
const BAMBOO = ramp("#e8de98", "#c2b466", "#90843c", "#605820");          // a banner's pole, a brush's handle
const JUZU = ramp("#b47c54", "#865430", "#5c381c", "#38200e");            // prayer beads: dark wood
const KOROMO = ramp("#7a7682", "#504c58", "#36333c", "#201e24");          // a novice's robe: grey-black
const CLAPPER = ramp("#f2dcae", "#d6b884", "#a68a58", "#6e5a36");         // the night man's clappers: hard pale wood
const PRINT_PAPER = ramp("#fff6dc", "#f2e2b8", "#c8b48a", "#8c7a58");    // a cheap print's paper, from behind (its colours are on the other side)
const RIPPLE = { tones: [pack("#f4faffa0"), pack("#f4faffa0"), pack("#f4faffa0"), pack("#f4faffa0")], soft: true, flat: 1 };      // a ring on the water round a wader: light, see-through
// clothes
const MOEGI = ramp("#dee6a0", "#b2be6c", "#828e46", "#565e2a");           // O-Fusa's kimono: a young yellow-green
const AKA = ramp("#ffa092", "#e45c50", "#aa3c36", "#702220");             // O-Kiku's best: red
const KIN = ramp("#fff2b6", "#f2ca64", "#ba9032", "#7c5e1a");             // her obi: gold
const KAMENOZOKI = ramp("#eef4f4", "#cadadf", "#94a8b0", "#60747a");      // O-Tane's cotton: the palest indigo, striped
const BUDO = ramp("#c2b2c2", "#947f96", "#6c5c6e", "#463c48");            // O-Shizu's: a grey plum
const WAKATAKE = ramp("#d6e8b6", "#a8c480", "#7a9456", "#4e6234");        // a pupil's: young bamboo
const FUJI = ramp("#dcd0ec", "#aa9aca", "#7c6e9e", "#50466a");            // the girl's: wisteria
const SEIJI = ramp("#c8e4da", "#90c2b2", "#609484", "#3c6256");           // the young wife's: celadon
const KURI = ramp("#ccA48a", "#a2765a", "#764f39", "#4a3121");            // O-Sato's sister-in-law's: chestnut
const EDO_WHITE_HAIR = ramp("#f2f0ea", "#cfcbc2", "#9e9a92", "#6c6964");   // O-Ume's: white
const AWA_MARK = BENI;                                                     // the Awa group's sign, on their hats and their banner: a red disc (the game's own)
const STRIPES = Array.from({ length: 20 }, (_, i) => -Math.PI + (i + 0.5) * (2 * Math.PI / 20));      // O-Tane's stripes, round the body

// ---- small helpers ----
/** The point a little way along a hand, out from the palm the way it points (k in metres). */
const alongHand = (c, s, k) => add(c.J[s].palm, mul(c.J[s].hDir, M(c, k)));
/** On the top of an open hand, where a thing laid in it rests. */
const onPalm = (c, s, up = 0.022) => add(c.J[s].palm, [0, M(c, up), 0]);
/** Between finger and thumb. */
const pinch = (c, s) => mix(c.J[s].tip, c.J[s].thumb1, 0.5);
/** The torso's own right, and forward, as directions in the figure's space. */
const rightOf = (c) => c.J.torso([1, 0, 0]), fwdOf = (c) => c.J.torso([0, 0, 1]);
/** A flat thing (cloth, paper) between corners in the figure's space, filled in one tone at its middle's depth: it turns
    with the figure as a flat thing does (edge-on from the side), which a limb drawn across it would not. */
function panel(c, pts, mat, o = {}) {
  if (c.seatOnly) return;
  const q = pts.map(c.P), z = q.reduce((t, v) => t + v[2], 0) / q.length + (o.bias || 0);
  let area = 0;
  for (let i = 0; i < q.length; i++) { const a = q[i], b = q[(i + 1) % q.length]; area += a[0] * b[1] - b[0] * a[1]; }
  if (Math.abs(area) / 2 < 1.5 * Math.hypot(q[0][0] - q[3][0], q[0][1] - q[3][1])) {      // edge-on: a line down its middle
    const a = mix(pts[0], pts[1], 0.5), b = mix(pts[2], pts[3], 0.5), A = c.P(a), B = c.P(b);
    c.sf.limb(A[0], A[1], z, B[0], B[1], z, 0.6, 0.6, mat, { part: o.part ?? c.parts.HELD });
    return;
  }
  c.sf.poly(q.map((v) => [v[0], v[1]]), z, mat, o.tone ?? 1, { part: o.part ?? c.parts.HELD, fn: o.fn });
}

// ---- things held: each drawn at its own size ----
/** A rice paddle (shamoji) in a hand, along the way the hand points: a short handle and a round flat blade. */
function paddleIn(c, s = "R") {
  const { limb, parts } = c, k = M(c, 1);
  limb(alongHand(c, s, -0.035), alongHand(c, s, 0.075), 0.009 * k, 0.011 * k, SHAMOJI, { part: parts.HELD });
  limb(alongHand(c, s, 0.090), alongHand(c, s, 0.135), 0.030 * k, 0.040 * k, SHAMOJI, { part: parts.HELD, fn: (t, nx) => (nx > 0.55 ? shifted(SHAMOJI, 1) : undefined) });
}
/** A rice ball, bale-shaped, lying across: o.pickle, a slice of yellow radish beside it; o.leaf, the leaf it sits on. */
function riceballAt(c, at, o = {}) {
  const { limb, ball, parts, tw } = c, k = M(c, 1), x = rightOf(c);
  if (o.leaf) ball(add(at, [0, -0.020 * k, 0]), [0.062 * k, 0.007 * k, 0.040 * k], BAMBOO_LEAF, { part: parts.HELD }, tw);
  limb(add(at, mul(x, -0.022 * k)), add(at, mul(x, 0.022 * k)), 0.024 * k, 0.024 * k, RICE, { part: parts.HELD });
  if (o.pickle) ball(add(add(at, mul(x, 0.050 * k)), [0, -0.010 * k, 0.004 * k]), [0.016 * k, 0.010 * k, 0.006 * k], TAKUAN, { part: parts.HELD }, tw);
}
/** A slice of pickled radish between finger and thumb. */
function pickleAt(c, at) { c.ball(at, [M(c, 0.017), M(c, 0.017), M(c, 0.005)], TAKUAN, { part: c.parts.HELD }, c.tw); }
/** A boxwood comb held up across, between the hands (or in one): a flat oblong with a rounded back, the teeth below. */
function combAt(c, mid, o = {}) {
  const { limb, parts } = c, k = M(c, 1), x = o.across || rightOf(c), half = 0.045 * k, r = 0.019 * k, mat = o.mat || TSUGE;
  limb(add(mid, mul(x, -half)), add(mid, mul(x, half)), r, r, mat, { part: parts.HELD, depth: 0.2, squareStart: true, squareEnd: true,
    fn: (t, nx, ny, px) => (ny < -0.62 && (t < 0.10 || t > 0.90) ? null : ny > 0.18 ? (c.S >= 120 && (px & 1) ? null : shifted(mat, 1)) : undefined) });
}
/** O-Tami's hairpin: a thin brass pin with a ball near its head and an ear-pick at the end, along a hand. */
function pinIn(c, s = "R") {
  const { limb, ball, parts } = c, k = M(c, 1);
  limb(alongHand(c, s, -0.020), alongHand(c, s, 0.120), 0.0026 * k, 0.0022 * k, KANZASHI, { part: parts.HELD });
  ball(alongHand(c, s, 0.098), [0.0065 * k, 0.0065 * k, 0.0065 * k], KANZASHI, { part: parts.HELD });
  ball(alongHand(c, s, 0.126), [0.0050 * k, 0.0035 * k, 0.0050 * k], KANZASHI, { part: parts.HELD });
}
/** A one-mon coin, copper, with its square hole (it shows when the coin is big enough to have a middle). */
function coinAt(c, at, mat = MON) {
  const k = M(c, 1), r = Math.max(0.0125 * k, 1.6 / c.S);
  c.ball(at, [r, r, 0.004 * k], mat, { part: c.parts.HELD, fn: (ux, uy) => (r * c.S >= 3 && Math.abs(ux) < 0.30 && Math.abs(uy) < 0.30 ? null : undefined) });
}
/** A small crab, seen from in front: a broad shell, two claws up, legs to the sides. `at` is its shell. */
function crabAt(c, at) {
  const { ball, limb, parts, tw } = c, k = M(c, 1), x = rightOf(c), r = Math.max(0.026 * k, 2.2 / c.S);
  ball(at, [r, r * 0.62, r * 0.80], CRAB_SHELL, { part: parts.HELD }, tw);
  for (const sd of [1, -1]) {
    const shoulder = add(at, mul(x, sd * r * 0.80)), claw = add(add(at, mul(x, sd * r * 1.35)), [0, r * 0.95, r * 0.20]);
    limb(shoulder, claw, r * 0.20, r * 0.30, CRAB_SHELL, { part: parts.HELD });
    ball(claw, [r * 0.34, r * 0.40, r * 0.30], CRAB_SHELL, { part: parts.HELD }, tw);
    for (const dy of [0.10, -0.20, -0.50]) limb(add(at, add(mul(x, sd * r * 0.70), [0, r * dy, 0])), add(at, add(mul(x, sd * r * 1.70), [0, r * (dy - 0.55), 0])), r * 0.12, r * 0.09, CRAB_SHELL, { part: parts.HELD });
  }
}
/** A small octopus. `at` is the bottom of its body (the mantle sits on it). o.hang: held up by the body, its arms hanging
    down; otherwise its arms reach out and down all round (over a ladle's rim, round a crab). */
function octoAt(c, at, o = {}) {
  const { ball, limb, parts, tw } = c, k = M(c, 1), x = rightOf(c), f = fwdOf(c), r = Math.max((o.big ? 0.040 : 0.032) * k, 2.4 / c.S);
  const body = add(at, [0, r * 1.05, 0]);
  ball(body, [r, r * 1.28, r], OCTO, { part: parts.HELD, fn: (ux, uy, uz, px, py) => (c.S >= 100 && (px * 7 + py * 3) % 11 === 0 ? OCTO_PALE : undefined) }, tw);
  if (o.hang) {
    for (const [sd, sw] of [[-1, 0.9], [-0.35, 0.3], [0.35, -0.3], [1, -0.8]]) {
      const base = add(at, add(mul(x, sd * r * 0.55), mul(f, r * 0.2))), mid = add(base, add(mul(x, sd * r * 0.35), [0, -r * 2.2, 0])), tip = add(mid, add(mul(x, sw * r * 0.7), [0, -r * 2.0, 0]));
      limb(base, mid, r * 0.26, r * 0.20, OCTO, { part: parts.HELD }); limb(mid, tip, r * 0.20, r * 0.10, OCTO, { part: parts.HELD });
    }
  } else {
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * 2 * Math.PI + 0.3, dir = add(mul(x, Math.cos(a)), mul(f, Math.sin(a) * 0.8));
      const base = add(at, mul(dir, r * 0.55)), mid = add(base, add(mul(dir, r * 1.05), [0, r * 0.25, 0])), tip = add(mid, add(mul(dir, r * 0.55), [0, -r * 1.10, 0]));
      limb(base, mid, r * 0.26, r * 0.20, OCTO, { part: parts.HELD }); limb(mid, tip, r * 0.20, r * 0.10, OCTO, { part: parts.HELD });
    }
  }
  if (c.S >= 70) for (const sd of [1, -1]) ball(add(add(body, mul(x, sd * r * 0.42)), add(mul(f, r * 0.82), [0, -r * 0.45, 0])), [r * 0.16, r * 0.16, r * 0.10], LACQUER, { part: parts.HELD, bias: 0.5 });      // its eyes
}
/** A pilgrim's wooden ladle in a hand: o.dir, the way its handle goes from the hand (along the hand if not said; o.up, up
    and out, as pilgrims hold theirs); the cup at the far end, open to the sky; o.octo, the octopus in it. */
function ladleHeld(c, s, o = {}) {
  const { limb, ball, parts, tw, J } = c, k = M(c, 1), A = J[s], dir = o.dir || (o.up ? unit(add(A.hDir, [0, 1.3, 0])) : A.hDir);
  const foot = add(A.palm, mul(dir, -0.060 * k)), top = add(A.palm, mul(dir, 0.240 * k)), cup = add(top, [0, -0.004 * k, 0]);
  limb(foot, top, 0.0075 * k, 0.0075 * k, EDO_WOOD, { part: parts.HELD });
  ball(cup, [0.044 * k, 0.030 * k, 0.044 * k], EDO_WOOD, { part: parts.HELD, fn: (ux, uy) => (uy < -0.30 ? shifted(EDO_WOOD, 2) : undefined) }, tw);      // the cup: its dark inside shows over the rim
  if (o.octo) octoAt(c, add(cup, [0, 0.006 * k, 0]));
  return cup;
}
/** A paper lantern, lit, hanging from a short stick held in a hand. */
function lanternIn(c, s = "R") {
  const { limb, ball, parts, tw } = c, k = M(c, 1), tip = alongHand(c, s, 0.200);
  limb(alongHand(c, s, -0.030), tip, 0.0060 * k, 0.0050 * k, EDO_WOOD, { part: parts.HELD });
  const top = add(tip, [0, -0.035 * k, 0]), mid = add(top, [0, -0.115 * k, 0]);
  limb(tip, top, 0.0022 * k, 0.0022 * k, SUMI, { part: parts.HELD });
  ball(add(top, [0, -0.006 * k, 0]), [0.052 * k, 0.012 * k, 0.052 * k], SUMI, { part: parts.HELD }, tw);
  ball(mid, [0.074 * k, 0.106 * k, 0.074 * k], CHOCHIN, { part: parts.HELD, fn: (ux, uy, uz, px, py) => (c.S >= 90 && Math.abs(uy) < 0.86 && ((py + 1) % 4 === 0) ? shifted(CHOCHIN, 1) : undefined) }, tw);
  ball(add(mid, [0, -0.108 * k, 0]), [0.052 * k, 0.012 * k, 0.052 * k], SUMI, { part: parts.HELD }, tw);
}
/** A sheet of paper held up between the hands (the broadsheet; a scrap of practice paper; a name slip held across).
    o.w, o.h: its size in metres; o.out: its printed face is away from the holder (held out to be read); o.print: a picture
    and columns of writing on that face (the broadsheet's: a rabbit on waves, and its story), seen when that face is toward us. */
function sheetAt(c, mid, o = {}) {
  const { parts, P, sf, th } = c, k = M(c, 1), x = rightOf(c), w = (o.w ?? 0.30) * k, h = (o.h ?? 0.22) * k;
  const corner = (u, v) => add(add(mid, mul(x, u * w / 2)), [0, v * h / 2, 0]);
  panel(c, [corner(-1, 1), corner(1, 1), corner(1, -1), corner(-1, -1)], o.mat || PAPER, { bias: 1.5 });
  const f = fwdOf(c), toward = f[0] * Math.sin(th) + f[2] * Math.cos(th), shows = o.out ? toward > 0.15 : toward < -0.15;
  if (!o.print || !shows || c.S < 70) return;
  const at = (u, v) => P(add(add(mid, mul(x, u * w / 2)), [0, v * h / 2, 0]));
  for (const u of [0.55, 0.30, 0.05, -0.20]) { const p0 = at(u, 0.70), p1 = at(u, -0.75); sf.stroke(p0[0], p0[1], p1[0], p1[1], 2, parts.HELD); }      // columns of writing
  const r0 = at(-0.80, 0.45), r1 = at(-0.45, 0.10), w0 = at(-0.92, -0.35), w1 = at(-0.35, -0.55);
  sf.stroke(r0[0], r0[1], r1[0], r1[1], 2, parts.HELD); sf.stroke(w0[0], w0[1], (w0[0] + w1[0]) / 2, w0[1] - 1, 2, parts.HELD); sf.stroke((w0[0] + w1[0]) / 2, w0[1] - 1, w1[0], w1[1], 2, parts.HELD);      // the rabbit, and its waves
}
/** A name slip held upright: a narrow strip of paper with a line of writing down it. */
function slipAt(c, mid, o = {}) {
  const { limb, parts, P, sf } = c, k = M(c, 1), h = (o.h ?? 0.22) * k, w = 0.032 * k;
  const lo = add(mid, [0, -h / 2, 0]), hi = add(mid, [0, h / 2, 0]);
  limb(lo, hi, w, w, PAPER, { part: parts.HELD, depth: 0.10, squareStart: true, squareEnd: true, bias: 1.5 });
  if (c.S >= 90) { const a = P(add(mid, [0, h * 0.36, 0])), b = P(add(mid, [0, -h * 0.30, 0])); sf.stroke(a[0], a[1], b[0], b[1], 2, parts.HELD); }
}
/** A writing brush in a hand, its black tip out along the hand. */
function brushIn(c, s = "R") {
  const { limb, ball, parts } = c, k = M(c, 1);
  limb(alongHand(c, s, -0.040), alongHand(c, s, 0.110), 0.0040 * k, 0.0035 * k, BAMBOO, { part: parts.HELD });
  ball(alongHand(c, s, 0.122), [0.0055 * k, 0.0100 * k, 0.0055 * k], EDO_HAIR, { part: parts.HELD });
}
/** The night man's clappers: a block of hard wood in each hand. */
function clappersIn(c, sides = ["R", "L"]) {
  const { limb, parts } = c, k = M(c, 1);
  for (const s of sides) limb(alongHand(c, s, -0.030), alongHand(c, s, 0.200), 0.017 * k, 0.017 * k, CLAPPER, { part: parts.HELD, squareStart: true, squareEnd: true });
}
/** A string of prayer beads hanging from a hand. */
function beadsIn(c, s = "L") {
  const { ball, parts } = c, k = M(c, 1), x = rightOf(c), at = add(c.J[s].palm, [0, -0.010 * k, 0]), n = 12;
  for (let i = 0; i < n; i++) { const a = (i / n) * 2 * Math.PI, p = add(add(at, mul(x, Math.sin(a) * 0.028 * k)), [0, -0.050 * k + Math.cos(a) * 0.050 * k, 0.008 * k]); ball(p, [0.0062 * k, 0.0062 * k, 0.0062 * k], JUZU, { part: parts.HELD }); }
  if (c.S >= 90) ball(add(at, [0, -0.112 * k, 0.008 * k]), [0.006 * k, 0.014 * k, 0.006 * k], TENUGUI, { part: parts.HELD });      // its tassel
}
/** O-Kiku's writing box, wrapped in a cloth knotted on top, held to her chest. */
function bundleAt(c, at) {
  const { ball, limb, parts, tw } = c, k = M(c, 1), x = rightOf(c);
  limb(add(at, mul(x, -0.075 * k)), add(at, mul(x, 0.075 * k)), 0.040 * k, 0.040 * k, ASAGI, { part: parts.HELD, depth: 1.4, squareStart: true, squareEnd: true });
  for (const sd of [1, -1]) ball(add(add(at, mul(x, sd * 0.018 * k)), [0, 0.046 * k, 0]), [0.016 * k, 0.012 * k, 0.012 * k], ASAGI, { part: parts.HELD }, tw);      // the knot's two ears
}
/** The rod a puppet's left-hand operator works its arm with: a short dark stick from the hand, a toggle at its end. */
function rodIn(c, s = "R") {
  const { limb, ball, parts } = c, k = M(c, 1), end = alongHand(c, s, 0.230);
  limb(alongHand(c, s, -0.030), end, 0.0060 * k, 0.0050 * k, LACQUER, { part: parts.HELD });
  ball(end, [0.012 * k, 0.008 * k, 0.012 * k], LACQUER, { part: parts.HELD });
}
/** The Awa group's hat: a sedge hat with the group's red sign on its front (seen when the face is toward us). */
function awaHat(c, o = {}) {
  sugegasa(c, o);
  if (o.back) return;
  const { ball, headPt, d, parts, th, hy } = c, hr = d.headR;
  if (Math.cos(th + hy) < 0.35) return;
  ball(headPt([0, hr[1] * 0.98, hr[2] * 1.05]), [0.011, 0.009, 0.004], AWA_MARK, { part: parts.HAT, bias: c.S * 0.25 });
}
/** The group's banner on its bamboo pole, held upright in the left hand: a strip of white cloth hanging from a short
    crossbar at the top, beside the pole, with the group's red sign and a column of writing (the game's own). */
function bannerOn(c, o = {}) {
  const { limb, ball, parts, P, sf } = c, k = M(c, 1), { head } = wear.staff(c, "L", { mat: BAMBOO, top: o.top ?? 1.50, r: 0.0085 });
  const out = unit(add(c.J.torso([-1, 0, 0]), [0, 0, -0.25])), w = 0.26 * k, len = 0.92 * k;
  const a = add(head, [0, -0.040 * k, 0]), b = add(a, mul(out, w));
  limb(a, add(b, mul(out, 0.02 * k)), 0.0055 * k, 0.0055 * k, BAMBOO, { part: parts.HELD });       // the crossbar
  const drop = [0, -len - 0.010 * k, 0], ma = add(a, [0, -len / 2 - 0.010 * k, 0]), mb = add(b, [0, -len / 2 - 0.010 * k, 0]);
  panel(c, [add(a, [0, -0.010 * k, 0]), add(b, [0, -0.010 * k, 0]), add(b, drop), add(a, drop)], TENUGUI, { bias: -0.5 });      // the cloth, hanging (it turns with him: edge-on from the side)
  const sign = mix(ma, mb, 0.5), up = add(sign, [0, len * 0.30, 0]);
  ball(up, [w * 0.30, w * 0.30, 0.004], AWA_MARK, { part: parts.HELD, bias: 1 });
  if (c.S >= 70) for (let i = 0; i < 4; i++) { const q0 = P(add(sign, [0, len * (0.06 - i * 0.12), 0])), q1 = P(add(sign, [0, len * (-0.02 - i * 0.12), 0])); sf.stroke(q0[0], q0[1], q1[0], q1[1], 2, parts.HELD); }
}
/** A wooden pail of rope coiled in a fisherman's lap, the line he mends running from hand to hand (sitting). */
function lineOnLap(c) {
  const { J, limb, ball, parts, pose, tw } = c, k = M(c, 1);
  if (!pose.seated) return;
  const lap = add(mix(J.L.knee, J.R.knee, 0.5), [0, 0.020 * k, -0.06 * k]);
  ball(lap, [0.080 * k, 0.020 * k, 0.060 * k], ROPE, { part: parts.HELD, fn: (ux, uy) => (Math.hypot(ux, uy * 0.5) < 0.40 ? shifted(ROPE, 2) : undefined) }, tw);       // the coil
  limb(J.L.palm, J.R.palm, 0.0028 * k, 0.0028 * k, ROPE, { part: parts.HELD });
}

// ---- the water: someone wading ----
/** The water round someone standing in it: whatever of them is below the surface is not seen (the painted water shows),
    and a light ring of ripples lies on the water round their legs. h: the water's depth where they stand, in their own
    heights (what is drawn last in `extras`: call it at the very end). How high a pixel is comes from its own depth, so the
    water line runs round the legs as the surface does, lower across the near side. */
function wadeCut(c, h, o = {}) {
  if (c.seatOnly) return;
  const { sf, S, J, P } = c, TILT = 0.22, { w, m, z, p, t } = sf, H = sf.h, oy = sf.oy;
  for (let i = 0; i < w * H; i++) {
    if (!m[i]) continue;
    const y = (i / w) | 0;
    if ((oy - (y + 0.5) + z[i] * TILT) / S < h) { m[i] = 0; z[i] = -1e9; p[i] = 0; }
  }
  const ring = sf.mat(RIPPLE), rx = o.ring ?? 0.075, C = [J.hipC[0], h, J.hipC[2]];
  for (const [r, every] of [[rx, 1], [rx * 1.45, 3]]) {
    const n = Math.max(24, Math.ceil(2 * Math.PI * r * S * 1.6));
    for (let j = 0; j < n; j++) {
      if (j % every) continue;
      const a = (j / n) * 2 * Math.PI, q = P([C[0] + Math.cos(a) * r, h, C[2] + Math.sin(a) * r * 0.85]);
      const x = Math.round(q[0] - 0.5), y = Math.round(q[1] - 0.5);
      if (x < 0 || y < 0 || x >= w || y >= H) continue;
      const i = y * w + x;
      if (m[i] && q[2] <= z[i]) continue;                               // behind a leg
      m[i] = ring; z[i] = q[2]; p[i] = 0; t[i] = 1;
    }
  }
}

// ---- hair ----
/** A small girl's bob (okappa): a fringe, and the hair cut straight round at the jaw. */
const okappa = hairline({ front: 0.32, temple: 0.18, side: -0.52, back: -0.60, brow: 0.55, temples: 1.15 });
/** An old woman's: thin on top, drawn back to a small knot. */
const OLD_KNOT = [[0, 0.88, -0.48, 0.30, 0.24, 0.30]];
/** A novice's head: shaved all over (the scalp a shade darker and bluer, where the hair would be). */
const shavenHead = (x, y, z) => y > (z > 0.25 ? 0.50 : 0.12);

// ---- the girls in black: the outfit `edo-kurogo` (the puppet show, #31) ----
/** The hood the people who work a puppet's left hand and feet wear: black, over the whole head, and a flap of black gauze
    from the brow down over the face to the chest (the face is not seen: in black you are not there), a fall of it behind
    over the nape. (The face's eyes and mouth are placed only where the head is the part on top: under the hood, nowhere.) */
function kurogoHood(c) {
  const { ball, limb, hp, headPt, d, hy, parts, J, P } = c, hr = d.headR, chest = d.trunkTop[1];
  ball(headPt([0, 0.010, -0.004]), [hr[0] * 1.22, hr[1] * 1.16, hr[2] * 1.22], KUROGO, { part: parts.HAT }, hy);
  ball(headPt([0, -hr[1] * 0.40, hr[2] * 0.10]), [hr[0] * 1.04, hr[1] * 0.98, hr[2] * 1.12], KUROGO, { part: parts.HAT }, hy);      // (and well over the face and jaw: nothing of it shows, whichever way the head is bent)
  limb(add(J.spine(d.shoulderY - 0.030), J.torso([0, 0, 0])), add(J.head, [0, -hr[1] * 0.60, 0]), 0.048, 0.050, KUROGO, { part: parts.HAT });      // round the neck
  // the flap in front and the fall behind, each a flat panel (edge-on from the side, its whole width from in front)
  const T = (x, y, z) => add(J.sh, J.torso([x, y, z])), w = hr[0];
  panel(c, [hp(-0.92, 0.60, 1.32), hp(0.92, 0.60, 1.32), T(w * 1.05, -0.050, chest + 0.026), T(-w * 1.05, -0.050, chest + 0.026)], KUROGO_VEIL, { part: parts.HAT, bias: 1.5 });
  panel(c, [hp(-1.02, 0.20, -1.06), hp(1.02, 0.20, -1.06), T(w * 1.25, -0.050, -(chest + 0.014)), T(-w * 1.25, -0.050, -(chest + 0.014))], KUROGO, { part: parts.HAT });
  void P; void limb;
}
const KUROGO_ROBE = { top: { mat: KUROGO, sleeves: 2, ease: 0.008, open: 0.010, under: KUROGO } };
const OUTFIT_KUROGO = {
  name: "in the puppeteers' black robe and hood",
  bigsis: { ...KUROGO_ROBE, bottom: { kind: "skirt", mat: KUROGO, len: 1.86, flare: 1.06, wrap: [0.55, -0.30], under: KUROGO }, socks: undefined, shoes: { kind: "sandals", mat: WARAJI, foot: KUROGO, sole: shifted(WARAJI, 1) }, span: 1.2, hair: {} },
  lilsis: { ...KUROGO_ROBE, bottom: { kind: "skirt", mat: KUROGO, len: 1.56, flare: 1.08, wrap: [0.55, -0.30], under: KUROGO }, shoes: lilsis.shoes, socks: undefined, span: 1.2, hair: {} },      // her yellow boots, under it
  gear(c, who) {
    kimono(c, { mat: KUROGO, obi: SUMI, obiUp: 0.040, obiDown: 0.026, knot: "small", sleeve: who === "lilsis" ? 0.045 : 0.060 });
    kurogoHood(c);
    const h = c.pose.held;
    if (who === "bigsis" && h && h.startsWith("doll")) { if (c.pose.rod) rodIn(c, "R"); }       // (the rod with these poses: with poses that put her palm at the doll's hand, none)
    else familyHeld21(c);                                                // (their other holds: what is in the hands)
  },
};
/** A lead's page in another outfit than O-Tami's (dressed() is for hers): `people[<lead>-<name>]`. */
function dressedIn(who, name, fit, o = {}) {
  const base = { mom, bigsis, lilsis }[who];
  const spec = { ...base, ...fit[who], name: `${base.name}, ${o.label || fit.name}`, outfit: name, wears: who, extras(c) { fit.gear(c, who, o); if (o.extra) o.extra(c); } };
  if (o.holds) spec.holds = o.holds;
  if (o.cues) spec.cues = o.cues;
  if (o.face) spec.face = { ...base.face, ...o.face };
  return spec;
}

// ---- the family's holds for the act's new things (on their own pages, so that every outfit has them) ----
const reachTo = (p, s, hand, more = {}) => withArm(p, s, { hand, ...more });
const fam = {
  /** the paddle held up in front of her in her right hand, the left hand under it: given the kitchen (O-Natsu's, O-Tane's) */
  paddle: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.04, head: { nod: nodOf(b) + 0.14 }, held: "paddle" };
    reachTo(p, "R", [0.040, -0.070, 0.170], { bend: [0.8, -0.6, -0.3], grip: true, point: [-0.1, 0.9, 0.4] });
    reachTo(p, "L", [-0.010, -0.150, 0.160], { bend: [-0.9, -0.5, -0.3], flat: true, point: [0.7, 0.1, 0.7], thumb: [0, 1, 0] }); return p; },
  /** serving: leaning over the pot, the paddle down into it, the left hand on its rim */
  serve: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.24, head: { nod: nodOf(b) + 0.20 }, held: "serve" };
    reachTo(p, "R", [0.060, -0.250, 0.230], { bend: [0.8, -0.4, -0.5], grip: true, point: [-0.2, -0.8, 0.5] });
    reachTo(p, "L", [-0.090, -0.250, 0.210], { bend: [-0.8, -0.4, -0.5], flat: true, point: [0.3, -0.5, 0.8] }); return p; },
  /** shaping a rice ball with salted hands: both hands cupped together round it in front, the head bent to it */
  shape: (o) => { const b = o.base, sp = o.sp, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.18 }, held: "shape" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) reachTo(p, s, [sd * 0.026, sp.waist + 0.090, sp.belly + 0.110], { bend: [sd * 0.9, -0.5, -0.4], curl: 0.85, point: [-sd * 0.8, 0.3, 0.5] }); return p; },
  /** a rice ball held out on her open right hand (to O-Ume; to whoever she gives one) */
  riceball: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.08 }, held: "riceball" };
    reachTo(p, "R", [0.060, -0.110, 0.230], { bend: [0.8, -0.7, -0.2], flat: true, point: [-0.1, 0.0, 1], thumb: [1, 0, 0] }); return p; },
  /** the comb held up in both hands, looked at */
  comb: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.12 }, held: "comb" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) reachTo(p, s, [sd * 0.050, -0.070, 0.170], { bend: [sd * 0.8, -0.7, -0.3], curl: 0.75, point: [-sd * 0.6, 0.5, 0.6] }); return p; },
  /** the hairpin held up in her right hand, looked at ("It's an ear-pick.") */
  pin: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) - 0.04, turn: 0.10 }, held: "pin" };
    reachTo(p, "R", [0.050, 0.000, 0.160], { bend: [0.8, -0.7, -0.2], curl: 0.9, point: [-0.2, 0.95, 0.2] }); return p; },
  /** the coin held up between finger and thumb at her eye, looked through (its square hole) */
  coin: (o) => { const b = o.base, sp = o.sp, hr = o.d.headR, p = { ...cloneP(b), head: { nod: nodOf(b) - 0.06, turn: 0.06 }, held: "coin" };
    reachTo(p, "R", [0.032, sp.headY + hr[1] * 0.10 - 0.030, hr[2] + 0.060], { bend: [0.9, -0.7, -0.1], curl: 0.9, point: [-0.2, 1, 0.2], thumb: [0, 0, 1] }); return p; },
  /** a coin held out between finger and thumb, to give (a penny for a coin, the coin back to O-Ume) */
  coinout: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.06 }, held: "coinout" };
    reachTo(p, "R", [0.070, -0.060, 0.250], { bend: [0.8, -0.6, -0.2], curl: 0.9, point: [0, 0.6, 0.8], thumb: [0, 1, 0] }); return p; },
  /** the crab held out at arm's length, between finger and thumb */
  crab: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.02, head: { nod: nodOf(b) + 0.04 }, held: "crab" };
    reachTo(p, "R", [0.090, -0.030, 0.290], { bend: [0.7, -0.6, -0.3], curl: 0.9, point: [0, 0.5, 0.9], thumb: [0, 1, 0] }); return p; },
  /** the paper lantern, lit, hanging from its stick in her right hand */
  lantern: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.06 }, held: "lantern" };
    reachTo(p, "R", [0.110, -0.160, 0.150], { bend: [0.6, -0.8, -0.2], grip: true, point: [0.2, 0.55, 0.8] }); return p; },
  /** a slip held up in both hands at her chest (O-Fusa's, to leave at the hall) */
  slip: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.10 }, held: "slip" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) reachTo(p, s, [sd * 0.020, -0.120, 0.140], { bend: [sd * 0.9, -0.6, -0.3], curl: 0.8, point: [-sd * 0.3, 0.9, 0.3] }); return p; },
  /** two slips held out in both hands, a little bow: given to O-Ume ("I promised I'd bring these to you.") */
  slips: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) + 0.10 }, held: "slips" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) reachTo(p, s, [sd * 0.040, -0.110, 0.220], { bend: [sd * 0.8, -0.6, -0.3], curl: 0.8, point: [-sd * 0.2, 0.9, 0.4] }); return p; },
  /** the broadsheet held open in both hands, read */
  sheet: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.16 }, held: "sheet" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) reachTo(p, s, [sd * 0.085, -0.120, 0.160], { bend: [sd * 0.8, -0.6, -0.3], curl: 0.7, point: [sd * 0.2, 0.9, 0.3] }); return p; },
  /** the broadsheet held out at arm's length, its picture toward whoever she shows it to */
  showsheet: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.04, head: { nod: nodOf(b) + 0.04 }, held: "showsheet" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) reachTo(p, s, [sd * 0.090, -0.060, 0.260], { bend: [sd * 0.7, -0.6, -0.3], curl: 0.7, point: [sd * 0.2, 0.9, 0.3] }); return p; },
  /** the ladle given back: held out in both hands, its cup up */
  ladle: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.06 }, held: "ladle" };
    reachTo(p, "R", [0.050, -0.100, 0.200], { bend: [0.8, -0.6, -0.3], grip: true, point: [-0.1, 0.9, 0.4] });
    reachTo(p, "L", [0.010, -0.170, 0.180], { bend: [-0.8, -0.6, -0.3], grip: true, point: [-0.1, 0.9, 0.4] }); return p; },
  /** the ladle held out at arm's length in both hands, the octopus in it: leaning away from her passenger */
  ladleocto: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.08, head: { nod: nodOf(b) + 0.10 }, held: "ladleocto" };
    reachTo(p, "R", [0.040, -0.110, 0.270], { bend: [0.7, -0.6, -0.3], grip: true, point: [0, 0.35, 0.95] });
    reachTo(p, "L", [0.000, -0.140, 0.230], { bend: [-0.7, -0.6, -0.3], grip: true, point: [0, 0.35, 0.95] }); return p; },
  /** the ladle (the octopus in it) in her left hand, the crab held out to it in her right */
  ladlecrab: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.02, head: { nod: nodOf(b) + 0.12, turn: -0.10 }, held: "ladlecrab" };
    reachTo(p, "L", [-0.070, -0.120, 0.230], { bend: [-0.7, -0.6, -0.3], grip: true, point: [0.35, 0.30, 0.90] });
    reachTo(p, "R", [0.050, -0.020, 0.270], { bend: [0.7, -0.6, -0.3], curl: 0.9, point: [-0.5, 0.2, 0.8], thumb: [0, 1, 0] }); return p; },
  /** a slice of pickle held out (one each: the alms line) */
  pickle: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.08, head: { nod: nodOf(b) + 0.06 }, held: "pickle" };
    reachTo(p, "R", [0.060, -0.080, 0.240], { bend: [0.8, -0.6, -0.2], curl: 0.9, point: [0, 0.4, 0.9], thumb: [0, 1, 0] }); return p; },
  /** her left hand out low to her side, holding someone's (O-Kiku's) */
  hand: (o) => { const b = o.base, sp = o.sp, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.02, turn: -0.16 }, held: "hand" };
    reachTo(p, "L", [-(sp.side + 0.090), sp.hip + 0.040, 0.050], { bend: [-0.6, -0.2, -0.8], curl: 0.8, point: [-0.5, -0.5, 0.7] }); return p; },
  /** a monkey, for Kota (#27: "the armpits, the noise"): a hand scratching the top of her head, the other under her arm,
      the knees bent out, the mouth open */
  monkey: (o) => { const b = o.base, sp = o.sp, hr = o.d.headR, p = { ...cloneP(b), mouth: 2, breath: 1, lean: (b.lean || 0) + 0.06, sway: 0.008, head: { nod: nodOf(b) - 0.04, turn: 0.18 }, held: "monkey" };
    withArm(p, "R", { hand: [0.020, sp.headY + hr[1] * 0.55, 0.010], bend: [1, 0.2, 0.3], curl: 0.8, point: [-0.4, 0.2, 0.3] });
    withArm(p, "L", { hand: [-(o.d.shoulderW + 0.010), -0.075, 0.020], bend: [-0.6, 0.6, -0.2], curl: 0.9, point: [0.5, 0.4, 0.2] });
    for (const [s, sd] of [["R", 1], ["L", -1]]) p[s] = { ...p[s], leg: [0.16, 0.22], knee: 0.40 };
    return p; },
  /** a small print held up in both hands, looked at (the peddler's, and the printer's spoiled blue one) */
  print: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.14 }, held: "print" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) reachTo(p, s, [sd * 0.060, -0.090, 0.150], { bend: [sd * 0.8, -0.6, -0.3], curl: 0.7, point: [sd * 0.2, 0.9, 0.3] }); return p; },
  /** the pink flashlight, lit, held out in both hands and pointed up at something (the hum on the wall) */
  shine: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.04, head: { nod: nodOf(b) - 0.16 }, held: "shine" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) reachTo(p, s, [sd * 0.024, -0.050, 0.220], { bend: [sd * 0.9, -0.5, -0.4], curl: 0.9, point: [-sd * 0.2, 0.55, 0.8], thumb: [0, 1, 0] }); return p; },
};
/** Mom, sat back on her heels on the mats (the audience: seiza), crying into Tatsu's towel, held to her eyes in both hands */
const weepHold = (o) => {
  const p = poses.kneel(o.spec, "stand", "back", 1), hr = o.d.headR, sp = o.sp;
  p.head = { nod: (p.head ? p.head.nod : 0) + 0.12 }; p.held = "weep"; p.blink = true;
  for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.026, sp.chinY + 0.010, hr[2] + 0.040], bend: [sd, -0.6, 0.1], curl: 0.7, point: [-sd * 0.3, 0.9, 0.3] });
  return p;
};
/** Mom on her knees at the wall, her right arm up and in to the small door, a rice ball on her palm (#38) */
const feedHold = (o) => {
  const p = poses.kneel(o.spec, "stand", "up", 1);
  p.head = { nod: -0.14 }; p.held = "feed";
  withArm(p, "R", { hand: [0.050, 0.030, 0.300], bend: [0.8, -0.7, -0.2], flat: true, point: [0, 0.2, 1], thumb: [1, 0, 0] });
  return p;
};
Object.assign(mom.holds, { paddle: fam.paddle, serve: fam.serve, shape: fam.shape, riceball: fam.riceball, comb: fam.comb, coin: fam.coinout, crab: fam.crab, lantern: fam.lantern, slips: fam.slips, weep: weepHold, feed: feedHold });
const BIGSIS_HOLDS = { shape: fam.shape, comb: fam.comb, pin: fam.pin, sheet: fam.sheet, showsheet: fam.showsheet, lantern: fam.lantern, riceball: fam.riceball };
bigsis.holds = { ...(bigsis.holds || {}), ...BIGSIS_HOLDS };
for (const page of [bigsisEdo, bigsisEdoHatback, bigsisEdoCrew]) page.holds = bigsis.holds;      // (they were made before she had holds of her own)
Object.assign(lilsis.holds, { pin: fam.pin, coin: fam.coin, coinout: fam.coinout, ladle: fam.ladle, ladleocto: fam.ladleocto, crab: fam.crab, ladlecrab: fam.ladlecrab, pickle: fam.pickle, slip: fam.slip, lantern: fam.lantern, hand: fam.hand, shine: fam.shine, riceball: fam.riceball, monkey: fam.monkey, print: fam.print });
/** What is in the hands during one of these holds (each lead's pages draw it, in every outfit). */
function familyHeld21(c) {
  const h = c.pose.held, J = c.J;
  if (!h) return;
  if (h === "paddle" || h === "serve") paddleIn(c, "R");
  else if (h === "shape") riceballAt(c, add(between2(J).at, [0, M(c, 0.006), 0]));
  else if (h === "riceball") riceballAt(c, onPalm(c, "R"), { pickle: true });
  else if (h === "feed") riceballAt(c, onPalm(c, "R"));
  else if (h === "comb") combAt(c, add(between2(J).at, [0, M(c, 0.030), 0]));
  else if (h === "pin") pinIn(c, "R");
  else if (h === "coin" || h === "coinout" || h === "coinup") coinAt(c, pinch(c, "R"));
  else if (h === "crab") crabAt(c, add(pinch(c, "R"), [0, M(c, 0.012), 0]));
  else if (h === "lantern") lanternIn(c, "R");
  else if (h === "slip") slipAt(c, add(between2(J).at, [0, M(c, 0.070), 0]));
  else if (h === "slips") { const { at, across } = between2(J); for (const sd of [1, -1]) slipAt(c, add(add(at, mul(across, sd * M(c, 0.022))), [0, M(c, 0.080), 0])); }
  else if (h === "sheet" || h === "showsheet") sheetAt(c, add(between2(J).at, [0, M(c, 0.050), 0]), { out: h === "showsheet", print: true });
  else if (h === "print") sheetAt(c, add(between2(J).at, [0, M(c, 0.050), 0]), { w: 0.17, h: 0.23, mat: PRINT_PAPER });
  else if (h === "ladle") ladleHeld(c, "R", { dir: unit(add(J.R.hDir, [0, 0.4, 0])) });
  else if (h === "ladleocto") ladleHeld(c, "R", { octo: true });
  else if (h === "ladlecrab") { ladleHeld(c, "L", { octo: true }); crabAt(c, add(pinch(c, "R"), [0, M(c, 0.010), 0])); }
  else if (h === "pickle") pickleAt(c, pinch(c, "R"));
  else if (h === "shine") flashlight(c);
  else if (h === "weep") { const { at } = between2(J); c.ball(add(at, [0, M(c, 0.020), M(c, 0.020)]), [M(c, 0.060), M(c, 0.045), M(c, 0.030)], TENUGUI, { part: c.parts.HELD }, c.tw); }
}
{ const was = mom.extras; mom.extras = (c) => { was(c); familyHeld21(c); }; }
{ const was = lilsis.extras; lilsis.extras = (c) => { was(c); familyHeld21(c); }; }
// O-Tami's outfits: what is in Big Sister's and Little Sister's hands (Mom's own extras draw hers), and Big Sister's hair,
// put up with O-Tami's pin (#22: "she will not let a girl go on the road with her hair down"). BIGSIS_HAIR_UP false gives
// her round twenty's long hair back in every outfit.
const BIGSIS_HAIR_UP = true;
{ const was = OUTFITS.edo.gear; OUTFITS.edo.gear = (c, who, o = {}) => { if (who === "bigsis" && BIGSIS_HAIR_UP) bigsisEdoGear(c, o); else was(c, who, o); if (who !== "mom") familyHeld21(c); }; }
/** Big Sister in O-Tami's clothes, her hair put up: round twenty's gear for her (the kimono, the hat) with her long hair
    gathered into a knot at the back of her head, O-Tami's pin through it, and her headband. */
function bigsisEdoGear(c, o) {
  const { ball, limb, hp, headPt, onHead, d, hy, parts } = c, hr = d.headR;
  ball(headPt([0, 0.004, 0]), [hr[0] * 1.13, hr[1] * 1.14, hr[2] * 1.13], INDIGO, { part: parts.HAT, fn: (ux, uy, uz) => { const q = onHead(ux, uy, uz); return q[1] > 0.05 && Math.abs(q[2] - 0.28) < 0.12 ? undefined : null; } }, hy);      // her headband (as her own page draws it)
  ball(hp(0, 0.08, -1.00), [hr[0] * 0.52, hr[1] * 0.46, hr[2] * 0.40], BIG_HAIR, { part: parts.HAIR }, hy);                                                   // the knot
  limb(hp(-0.72, 0.18, -1.02), hp(0.78, 0.10, -1.04), 0.0030, 0.0026, KANZASHI, { part: parts.HAIR, bias: c.S * 0.04 });                                      // the pin through it
  ball(hp(0.82, 0.10, -1.04), [0.0055, 0.0055, 0.0055], KANZASHI, { part: parts.HAIR, bias: c.S * 0.04 }, hy);
  kimono(c, { mat: INDIGO, obi: BIG_OBI, knot: "big", sleeve: 0.070 });
  if (o.cloth) headcloth(c, TENUGUI);
  else sugegasa(c, { back: o.hat === "back", r: 0.115 });
}

// ---- the family's new outfits ----
// the girls in black for the puppet show (#31). The doll walks along the top of the stage rail, and its three operators
// stand behind the rail (their legs hidden by it): Jubei at its head and right hand, Big Sister at its left hand (her right
// hand on the rod that works its arm), Little Sister at its feet (her hands at its heels; she stamps for its steps). Their
// holds here have PEOPLE-21A's names for the doll's moments, so that one name moves all three: `doll` (it stands), `dollear`
// (its hand to its ear: cue 1), `dollrun` (it runs: cue 2; Little Sister's other foot is `dollstamp`, so that a scene can
// alternate them), `dollkneel` (it kneels at the door: cue 3). The rest of their holds are their own pages' (inherited).
/** Where the doll's feet are above the floor the operators stand on, in metres: PAINT-21D's theatre has one floor, the
    rail 86 cm high along the stage's front, and the doll walking on its top (PUPPET_FEET_Y, 88 cm: tools/paint/
    edo_theatre_model.py). The operators' hands are put at the doll's hand and heels as it stands there. */
const OPERATOR_RAIL = 0.88;
/** A height above the floor (metres) as a hand's height in the torso's space (from the middle of the shoulders), for someone leaning `lean`. */
const handAt = (o, metres, lean = 0) => { const h = (o.spec.height || 1) * 1.81, d = o.d; return (metres / h - d.hipY) / Math.cos(lean) - (d.shoulderY - d.hipY); };
const leftHandOp = (name, above, o, more = {}) => {
  const b = o.base, lean = more.lean ?? 0.10, p = { ...cloneP(b), lean, head: { nod: nodOf(b) + (more.nod ?? 0.14), turn: -0.26 }, held: name, rod: true };
  if (more.knee) for (const s of ["R", "L"]) p[s] = { ...p[s], leg: [more.knee * 0.45, 0.06], knee: more.knee };
  reachTo(p, "R", [0.120, handAt(o, OPERATOR_RAIL + above, lean) + (more.knee ? 0.06 : 0), more.fwd ?? 0.170], { bend: [0.5, -0.6, -0.4], grip: true, point: [0.80, more.up ?? 0.10, 0.50] });
  reachTo(p, "L", [-0.040, handAt(o, OPERATOR_RAIL + above + 0.10, lean), 0.120], { bend: [-0.8, -0.5, -0.3], curl: 0.8 });
  return p;
};
const OP = {
  /** at the doll's left hand as it stands: her right hand out to her right at its height, on the rod */
  doll: (o) => leftHandOp("doll", 0.42, o),
  /** its hand up to its ear (cue 1: "The boy hears his mother calling") */
  dollear: (o) => leftHandOp("dollear", 0.76, o, { up: 0.45, nod: 0.04 }),
  /** it runs (cue 2): the hand swung forward */
  dollrun: (o) => leftHandOp("dollrun", 0.45, o, { fwd: 0.250, up: 0.20 }),
  /** it kneels at the door (cue 3): the hand to the ground, she bends down with it */
  dollkneel: (o) => leftHandOp("dollkneel", 0.06, o, { lean: 0.40, knee: 0.60, up: -0.30, nod: 0.22 }),
};
const feetOp = (name, o, more = {}) => {
  const b = o.base, lean = more.lean ?? 0.16, p = { ...cloneP(b), lean, breath: 0.4, head: { nod: nodOf(b) + 0.20 }, held: name };
  for (const [s, sd] of [["R", 1], ["L", -1]]) {
    const up = more.up === s;
    p[s] = { ...p[s], leg: up ? [0.95, 0.06] : [more.knee ? more.knee * 0.45 : 0.04, 0.06], knee: up ? 1.25 : more.knee || 0.06, foot: up ? 0.20 : 0 };
    withArm(p, s, { hand: [sd * 0.045, handAt(o, OPERATOR_RAIL + 0.03, lean) + (more.knee ? 0.05 : 0), 0.200], bend: [sd * 0.6, -0.4, -0.5], grip: true, point: [0, -0.5, 0.85] });
  }
  return p;
};
const OP_FEET = {
  /** at the doll's heels as it stands: both hands out low in front, on them */
  doll: (o) => feetOp("doll", o), dollear: (o) => feetOp("dollear", o),
  /** it runs: her right foot up to stamp (and `dollstamp`, her left): a scene alternates them, with the stamp's sound */
  dollrun: (o) => feetOp("dollrun", o, { up: "R" }), dollstamp: (o) => feetOp("dollstamp", o, { up: "L" }),
  /** it kneels: its feet folded under it on the rail, her hands with them, leaning in */
  dollkneel: (o) => feetOp("dollkneel", o, { lean: 0.24 }),
};
const HOODED = { ears: false, nose: [0.2, -1.5, 0.3] };                // (under the hood: no ears, and the nose kept inside it)
// (their holds: their own pages' and the show's, as plain entries, so that a page made from this one by spreading its holds
// keeps them all: PEOPLE-21A gives every page of the girls its own `doll*` holds, after the people table)
export const bigsisEdoKurogo = dressedIn("bigsis", "edo-kurogo", OUTFIT_KUROGO, { holds: { ...bigsis.holds, ...OP }, cues: {}, face: HOODED });
export const lilsisEdoKurogo = dressedIn("lilsis", "edo-kurogo", OUTFIT_KUROGO, { holds: { ...lilsis.holds, ...OP_FEET }, cues: {}, face: HOODED });
// Little Sister wading (#35): O-Tami's clothes with the kimono hitched up into the sash, as travellers did, her yellow
// boots in the water to above the ankle (the water 8.5 cm deep: well below the tops of her rain boots), a ring of ripples
// round them. `edo-wading` (the hat on), `edo-hatback-wading` (the hat on her back). A scene dresses her so at the water's
// edge (`shallows`) and back at the same place coming out.
const LIL_WADE = 0.070;                                                    // the water's depth where she wades, in her own heights (8.5 cm)
const hitched = (spec, len) => ({ ...spec, bottom: { ...spec.bottom, len } });
export const lilsisEdoWading = hitched(dressed("lilsis", "edo-wading", { label: "in Edo clothes, wading, the kimono hitched up", extra: (c) => wadeCut(c, LIL_WADE) }), 1.04);
export const lilsisEdoHatbackWading = hitched(dressed("lilsis", "edo-hatback-wading", { hat: "back", label: "in Edo clothes, wading, the hat on her back", extra: (c) => wadeCut(c, LIL_WADE) }), 1.04);
// Little Sister and O-Kiku going into the writing school hand in hand (#36): her left hand out to her side, held, as she
// walks (O-Kiku's kind `kiku-hand` holds out her right; walk them side by side, O-Kiku on Little Sister's left)
const HAND_OUT = { L: { hand: [-0.110, -0.300, 0.050], bend: [-0.6, -0.2, -0.8], curl: 0.8, point: [-0.5, -0.5, 0.7] } };
export const lilsisEdoHand = { ...dressed("lilsis", "edo-hand", { label: "in Edo clothes, holding someone's hand" }), hold: HAND_OUT };
export const lilsisEdoHatbackHand = { ...dressed("lilsis", "edo-hatback-hand", { hat: "back", label: "in Edo clothes, holding someone's hand, the hat on her back" }), hold: HAND_OUT };
OUTFIT_NAMES.bigsis.push("edo-kurogo");
OUTFIT_NAMES.lilsis.push("edo-kurogo", "edo-wading", "edo-hatback-wading", "edo-hand", "edo-hatback-hand");

// ---- the people ----
const EDO_CHILD = { ...CHILD, headR: [0.068, 0.079, 0.075] };
// ------------------------------------------------------------------ the Akashi shore
// O-Fusa, nine, from a writing school in Tokushima, come across with her group's boat: brave, bossy, in tears (her ladle
// went into the sea as they waded ashore). The group's hat with its red sign. `fusa` in tears; `fusa-ladle` with it back.
const fusaHolds = {
  /** crying, both fists to her eyes, the head down */
  cry: (o) => { const b = o.base, sp = o.sp, hr = o.d.headR, p = { ...cloneP(b), breath: 1, lean: (b.lean || 0) + 0.06, blink: true, head: { nod: nodOf(b) + 0.14 }, held: "cry" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.026, sp.chinY + hr[1] * 0.90, hr[2] + 0.024], bend: [sd, -0.6, 0.1], grip: true, point: [-sd * 0.3, 0.9, 0.3] }); return p; },
  slip: (o) => fam.slip(o),
};
const fusaBase = {
  name: "O-Fusa, a pilgrim from Awa", height: H(125),
  dim: { ...EDO_CHILD, shoulderW: 0.088 }, skin: EDO_SUN,
  hair: { mat: EDO_HAIR, bulk: [1.10, 1.06, 1.10], where: girlknot, puffs: GIRLKNOT_PUFFS, ears: true },
  face: { ...EDO_CHILD_FACE, eyes: "big", blush: "#f0a090", smile: 0 },
  top: { mat: MOEGI, sleeves: 2, ease: 0.006, open: 0.026, under: WHITE }, bottom: { kind: "skirt", mat: MOEGI, len: 1.40, flare: 1.06, wrap: [0.55, -0.30], under: MOEGI },
  shoes: { kind: "sandals", mat: WARAJI, foot: EDO_SUN, sole: shifted(WARAJI, 1) },
  walk: { swing: 0.48, arm: 0.44, elbow: 0.30, lean: 0.08, lift: 1.2, bob: 0.02 }, pace: 175,
  gestures: [0, 10, 0, 17, 4],                                          // bossy: pointing; counting on her fingers; both hands up
};
const fusaGear = (c) => { kimono(c, { mat: MOEGI, obi: AKA, obiUp: 0.034, obiDown: 0.026, knot: "big", sleeve: 0.045 }); awaHat(c, { r: 0.100 }); if (c.pose.held === "slip") slipAt(c, add(between2(c.J).at, [0, M(c, 0.070), 0])); };
export const fusa = {
  ...fusaBase, stance: "clasped", lean: 0.06, nod: 0.12,                // the head down: in tears
  fidgets: { only: true, stand: ["sniffle", "sniffle", "look", "shift"] }, holds: fusaHolds, cues: { stand: ["sniffle"] },
  extras(c) { fusaGear(c); },
};
export const fusaLadle = {
  ...fusaBase, name: "O-Fusa, with her ladle back", stance: "akimbo", face: { ...fusaBase.face, smile: 1 }, span: 1.2,
  hold: { R: { hand: [0.080, -0.140, 0.120], bend: [0.7, -0.8, -0.3], grip: true, point: [0, 1, 0.2] } },
  fidgets: { only: true, stand: ["hop", "look", "shift"] }, holds: fusaHolds, cues: { stand: ["hop"] },
  extras(c) { fusaGear(c); ladleHeld(c, "R", { up: true }); },
};
// Her group's leader: a man of Awa, travel clothes, the group's hat, the banner on its pole in his left hand; counting heads.
export const leader = {
  ...workman(EDO_SUN, { jacket: AI_DEEP, trousers: AI, face: { eyes: "heavy", lines: 1, jaw: 0.92, chin: 0.62 } }),
  ...robe(AI_DEEP, 1.50), ...TRAVEL,
  name: "the leader of O-Fusa's group", height: H(158), tall: 1.62, span: 1.5,
  hold: { L: { hand: [-0.075, -0.080, 0.090], bend: [-0.7, -0.6, -0.2], grip: true, point: [0, 1, 0.1] } },      // the banner's pole
  lean: 0.02, walk: { swing: 0.42, arm: 0.24, elbow: 0.30, lean: 0.05, lift: 1.0 }, pace: 145,
  gestures: [0, 17, 11, 10],                                            // counting heads; a finger up; pointing
  fidgets: { only: true, stand: ["tally2", "look", "shift"] }, cues: { stand: ["tally2", "ojigi"] }, ...bowOf(0.30),
  extras(c) { chonmageTop(c); kimono(c, { mat: AI_DEEP, obi: CHA, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.050 }); awaHat(c, { r: 0.112 }); bannerOn(c); },
};
// Old Heita, the octopus fisherman: few words, all of them about octopus. Sun-dark, grey, a short indigo jacket, a white
// loincloth, bare legs and bare feet on the sand. Found sitting cross-legged on the sand mending a line (`mend`); on his
// feet, the octopus held up in his fist ("with great satisfaction").
const heitaHolds = {
  /** the octopus held up high in his right fist, its arms hanging, a smile */
  octopus: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.04, smile: 2, head: { nod: nodOf(b) - 0.14, turn: 0.20 }, held: "octopus" };
    withArm(p, "R", { hand: [0.190, 0.150, 0.110], bend: [0.8, -0.5, -0.2], grip: true, point: [0.2, 1, 0.1] }); return p; },
  /** the octopus wrapped round the crab, held out in both hands (taken off the child's hands) */
  octocrab: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, smile: 2, head: { nod: nodOf(b) + 0.12 }, held: "octocrab" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.030, -0.130, 0.200], bend: [sd * 0.8, -0.6, -0.3], curl: 0.8, point: [-sd * 0.5, 0.4, 0.7], thumb: [0, 1, 0] }); return p; },
};
export const heita = {
  ...workman(EDO_SUN, { jacket: AI, trousers: AI, face: { eyes: "heavy", lines: 2, jaw: 0.90, chin: 0.56, short: { mat: EDO_GREY, stubble: EDO_GREY, from: 0.2 } } }),
  name: "Heita, the octopus fisherman", height: H(152),
  hair: { mat: EDO_GREY, bulk: [1.04, 1.0, 1.04], where: chonmage },
  top: { mat: AI, sleeves: 1.45, ease: 0.006, hem: 0.050, open: 0.060, under: EDO_SUN, cuff: 0.016 },     // a short work jacket, the sleeves to the forearm, open on the chest
  bottom: { kind: "shorts", mat: TENUGUI, len: 0.10, ease: 0.004 },                                    // a loincloth: only its edge shows under the jacket
  shoes: { kind: "bare" },
  seated: "ground", sit: { lean: 0.14, nod: 0.14 }, riseMs: 1600, shadow: 0.20,
  rest: { R: { hand: [0.040, -0.300, 0.180], bend: [0.9, -0.4, -0.4], grip: true, point: [-0.6, 0.3, 0.7] }, L: { hand: [-0.060, -0.290, 0.170], bend: [-0.9, -0.4, -0.4], grip: true, point: [0.6, 0.2, 0.7] } },
  gestures: [0, 8, 0, 20], walk: { swing: 0.36, arm: 0.26, elbow: 0.30, lean: 0.08, lift: 0.8 }, pace: 120,
  fidgets: { only: true, sit: ["mend", "mend", "look", "shift"], stand: ["look", "shift", "back"] }, holds: heitaHolds, cues: { sit: ["mend"], stand: ["ojigi"] },
  stood: { rest: undefined }, ...bowOf(0.24),
  extras(c) {
    hachimaki(c, TENUGUI, 0.40); chonmageTop(c, { mat: EDO_GREY, pate: pateOf(EDO_SUN) });
    kimono(c, { mat: AI, obi: NEZUMI, obiUp: 0.016, obiDown: 0.022, knot: "small", sleeve: 0, jacket: true });
    lineOnLap(c);
    const h = c.pose.held;
    if (h === "octopus") octoAt(c, add(c.J.R.palm, [0, -M(c, 0.030), 0]), { hang: true, big: true });
    else if (h === "octocrab") { const at = between2(c.J).at; crabAt(c, add(at, [0, M(c, 0.030), 0])); octoAt(c, add(at, [0, M(c, 0.020), 0])); }
  },
};
export const heitaStanding = { ...upOf(heita), name: "Heita, on his feet" };
// O-Sato and her sister-in-law: Harima women slipping away east to Ise, with their ladles, a towel over the hair; they
// stop on the road behind the pines to give the news from Shosha. They walk east.
const harimaWoman = (skin, mat, height, name, o = {}) => ({
  ...WOMAN_EDO(skin, mat, { face: o.face, len: 1.60, gestures: o.gestures || [0, 8, 9, 20], pace: 150, dim: o.dim }), name, height, span: 1.2,
  hold: { R: { hand: [0.085, -0.150, 0.120], bend: [0.7, -0.8, -0.3], grip: true, point: [0, 1, 0.2] } },      // the ladle held up
  walk: { swing: 0.44, arm: 0.30, elbow: 0.30, lean: 0.07, lift: 1.0, sway: 0.012 },
  fidgets: { stand: ["laugh", "look", "shift", "whisper"], not: ["sleeve", "scratch"] }, cues: { stand: ["laugh", "whisper", "ojigi"] }, ...bowOf(0.28),
  holds: { ladleout: (p) => { const b = p.base, q = { ...cloneP(b), lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.08 }, held: "ladleout" }; withArm(q, "R", { hand: [0.080, -0.180, 0.230], bend: [0.6, -0.8, -0.2], grip: true, point: [0.1, 0.3, 0.95] }); return q; } },
  extras(c) { kimono(c, { mat, obi: o.obi || AI_DEEP, knot: "big", sleeve: 0.050 }); headcloth(c, o.cloth || TENUGUI, { tails: 0.16, brow: 0.46 }); ladleHeld(c, "R", { up: c.pose.held !== "ladleout" }); },
});
export const sato = harimaWoman(EDO_SUN, NEZUMI, H(147), "O-Sato, a Harima woman going to Ise", { face: { brows: null, lines: 1, smile: 1 } });
export const satosister = harimaWoman(EDO_SKIN, KURI, H(145), "O-Sato's sister-in-law", { face: { eyes: "girl", smile: 1, blush: "#eea090" }, cloth: ASAGI, obi: CHA, gestures: [0, 9, 0, 4] });
// Two of the Awa pilgrims, wading ashore from their boat with their ladles held up, kimonos hitched to the knee, the
// group's hats: the water at mid-shin (`awapilgrim1`, `awapilgrim2`); and the same on the sand (`-ashore`).
const awaWader = (skin, height, mat, name, o = {}) => {
  const base = o.woman ? WOMAN_EDO(skin, mat, { face: o.face || {}, len: 0.98, gestures: [0, 8, 0, 9], pace: 120 }) : { ...workman(skin, { jacket: mat, trousers: AI, face: o.face || {} }), ...robe(mat, 0.98) };
  return {
    ...base, name, height, span: 1.3, bottom: { ...base.bottom, len: 0.98 }, shoes: { kind: "bare" }, socks: undefined,
    hold: { R: { hand: [0.090, 0.020, 0.100], bend: [0.7, -0.8, -0.3], grip: true, point: [0, 1, 0.2] }, L: { arm: [0.10, 0.62], elbow: 0.40, flat: true } },      // the ladle held up high, the other arm out for balance
    lean: 0.06, walk: { swing: 0.30, arm: 0.10, elbow: 0.30, lean: 0.10, lift: 1.4 }, pace: 95,
    gestures: [0, 8, 0, 9], fidgets: { only: true, stand: ["look", "shift"] }, cues: { stand: ["ojigi"] }, ...bowOf(0.26),
    extras(c) {
      if (!o.woman) chonmageTop(c);
      kimono(c, { mat, obi: o.obi || CHA, obiUp: o.woman ? 0.050 : 0.016, obiDown: o.woman ? 0.034 : 0.024, knot: o.woman ? "big" : "small", sleeve: 0.040 });
      if (o.woman) headcloth(c, TENUGUI, { tails: 0.12, brow: 0.48 });
      awaHat(c, { r: 0.112 }); ladleHeld(c, "R", { up: true });
      if (c.spec.wade) wadeCut(c, c.spec.wade, { ring: 0.085 });
    },
  };
};
export const awapilgrim1 = { ...awaWader(EDO_SUN, H(155), NEZUMI, "a pilgrim from Awa, wading ashore", { face: { lines: 1, jaw: 0.92 } }), wade: 0.20 };
export const awapilgrim2 = { ...awaWader(EDO_SUN, H(145), KAKI, "a pilgrim from Awa (a woman), wading ashore", { woman: true, face: { brows: null }, obi: AI_DEEP }), wade: 0.20 };
export const awapilgrim1Ashore = { ...awapilgrim1, name: "a pilgrim from Awa, ashore", wade: 0, hold: { R: awapilgrim1.hold.R }, walk: { swing: 0.42, arm: 0.20, elbow: 0.30, lean: 0.07, lift: 1.0 }, pace: 140 };
export const awapilgrim2Ashore = { ...awapilgrim2, name: "a pilgrim from Awa (a woman), ashore", wade: 0, hold: { R: awapilgrim2.hold.R }, walk: { swing: 0.42, arm: 0.20, elbow: 0.30, lean: 0.07, lift: 1.0 }, pace: 140 };

// ------------------------------------------------------------------ Himeji town (Watamachi)
// O-Tane, a cotton weaver's wife: practical, proud, worried about her daughter's first day; a striped cotton kimono of the
// town's own cloth, the sleeves tied back, an apron; teeth blackened, no brows (O-Kiku). She hands Mom her paddle.
const taneHolds = {
  /** the paddle held out to Mom in both hands, a little bow: her kitchen, for an hour */
  paddle: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.12, head: { nod: nodOf(b) + 0.10 }, held: "paddle" };
    withArm(p, "R", { hand: [0.040, -0.120, 0.220], bend: [0.8, -0.6, -0.3], grip: true, point: [0, 0.3, 0.95] });
    withArm(p, "L", { hand: [0.000, -0.150, 0.200], bend: [-0.8, -0.6, -0.3], flat: true, point: [0.6, 0.1, 0.8], thumb: [0, 1, 0] }); return p; },
};
const taneTop = (b) => ({ ...b.top, stripe: { mat: AI, at: STRIPES, half: 0.050 } }), taneBottom = (b) => ({ ...b.bottom, stripe: { mat: AI, at: STRIPES, half: 0.042 } });
const taneBase = WOMAN_EDO(EDO_SKIN, KAMENOZOKI, { face: { brows: null, lines: 1 }, len: 1.74, gestures: [0, 10, 17, 8], pace: 165, dim: { shoulderW: 0.084 } });
export const tane = {
  ...taneBase, top: taneTop(taneBase), bottom: taneBottom(taneBase),
  name: "O-Tane, a weaver's wife", height: H(148),
  stance: "clasped", lean: 0.03, walk: { swing: 0.44, arm: 0.30, elbow: 0.40, lean: 0.06, lift: 1.1, sway: 0.012 },
  fidgets: { stand: ["fret", "look", "shift"], not: ["sleeve", "scratch"] }, holds: taneHolds, cues: { stand: ["fret", "ojigi"] }, ...bowOf(0.30),
  extras(c) { kimono(c, { mat: KAMENOZOKI, eri: AI, obi: AI_DEEP, knot: "big", sleeve: 0 }); tasuki(c, TENUGUI); apronOf(c, KAKI, 0.36); if (c.pose.held === "paddle") paddleIn(c, "R"); },
};
// O-Kiku, seven: her best clothes for her first day at the writing school (red, flowered, a gold obi with a big bow), her
// writing box wrapped in a cloth held tight to her chest, and she will not go in. She says nothing till the end.
const KIKU_DIM = { ...CHILD, headR: [0.074, 0.085, 0.080], shoulderW: 0.084, legR: [0.048, 0.034, 0.024] };
const KIKU_BUNDLE = { R: { hand: [0.040, -0.120, 0.120], bend: [0.9, -0.5, -0.3], curl: 0.8, point: [-0.8, 0.2, 0.5] }, L: { hand: [-0.040, -0.110, 0.120], bend: [-0.9, -0.5, -0.3], curl: 0.8, point: [0.8, 0.2, 0.5] } };
function kikuGear(c, o = {}) {
  const { ball, hp, d, hy, parts } = c;
  kimono(c, { mat: AKA, obi: KIN, obiUp: 0.040, obiDown: 0.028, knot: "big", sleeve: 0.070 });
  flowered(c, 40, [TENUGUI, KIN, MOEGI]);
  ball(hp(0.62, 0.78, 0.10), [d.headR[0] * 0.28, d.headR[1] * 0.20, d.headR[2] * 0.22], BENI, { part: parts.HAT }, hy);      // a red tie in her hair
  if (o.bundle !== false && c.pose.held !== "smile") bundleAt(c, add(between2(c.J).at, [0, M(c, 0.010), M(c, -0.012)]));
}
/** Small flowers on a best kimono: dots of two or three colours fixed to the cloth, on the body and the skirt, where the cloth faces us. */
function flowered(c, n, mats) {
  const { sf, P, trunkAt, trunkFacing, d, th, ht, parts, fine, skirtAt } = c;
  if (!fine) return;
  for (let i = 0; i < n; i++) {
    const h = cell(i, 11) % 1000 / 1000, round = (cell(i, 5) % 1000 / 1000 - 0.5) * 2 * Math.PI, col = mats[i % mats.length].tones[1];
    if (i % 2 === 0) {
      const f = trunkFacing(round); if (f[0] * Math.sin(th) + f[2] * Math.cos(th) < 0.25) continue;
      const q = P(trunkAt(d.waistY - 0.02 + h * (d.shoulderY - d.waistY - 0.08), round, 0.010)); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), col, parts.TORSO);
    } else if (skirtAt) {
      const f = turn([Math.sin(round), 0, Math.cos(round)], ht); if (f[0] * Math.sin(th) + f[2] * Math.cos(th) < 0.25) continue;
      const q = P(skirtAt(0.15 + h * (c.spec.bottom.len - 0.30), round, 0.006)); sf.dot(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), col, parts.SKIRT);
    }
  }
}
const kikuBase = {
  name: "O-Kiku, O-Tane's daughter", height: H(115),
  dim: KIKU_DIM, skin: EDO_PALE,
  hair: { mat: EDO_HAIR, bulk: [1.12, 1.06, 1.12], where: okappa, ears: false },
  face: { ...EDO_CHILD_FACE, eyes: "big", smile: 0, blush: "#f2a0a0" },
  top: { mat: AKA, sleeves: 2, ease: 0.006, open: 0.022, under: WHITE }, bottom: { kind: "skirt", mat: AKA, len: 1.80, flare: 1.08, wrap: [0.55, -0.30], under: AKA },
  socks: undefined, shoes: { kind: "sandals", mat: WARAJI, foot: WHITE, sole: shifted(WARAJI, 1) },          // white tabi: her best
  walk: { swing: 0.40, arm: 0.10, elbow: 0.40, lean: 0.06, lift: 1.0, bob: 0.02 }, pace: 150,
  gestures: [0, 0, 5, 0],                                               // she says nothing: a nod; a hand to her heart
};
const kikuHolds = {
  /** she smiles, at last ("...Mother."), the bundle tucked under her arm */
  smile: (o) => ({ ...cloneP(o.base), smile: 2, head: { nod: nodOf(o.base) - 0.12 }, held: "smile" }),
};
export const kiku = {
  ...kikuBase, hold: KIKU_BUNDLE, lean: 0.03, nod: 0.16,                // her head down: she will not go in
  fidgets: { only: true, stand: ["scuff", "look", "shift"] }, holds: kikuHolds, cues: { stand: ["scuff"] },
  extras(c) { kikuGear(c); },
};
export const kikuHand = {
  ...kikuBase, name: "O-Kiku, holding someone's hand", nod: 0.06, pace: 145,       // (Little Sister's pace: they walk together, 0.30 m apart, O-Kiku on her left: their hands meet)
  hold: { L: KIKU_BUNDLE.L, R: { hand: [0.110, -0.290, 0.050], bend: [0.6, -0.2, -0.8], curl: 0.8, point: [0.5, -0.5, 0.7] } },      // her right hand out to her side, held
  fidgets: { only: true, stand: ["look", "shift"] }, holds: kikuHolds,
  extras(c) { kikuGear(c, { bundle: false }); bundleAt(c, add(c.J.L.palm, [M(c, 0.04), M(c, 0.010), 0])); },
};
// O-Shizu, the writing teacher: a woman of about forty, calm, amused, reads everything; a quiet plum-grey kimono, a black
// obi; teeth blackened (married); found kneeling at the school (seiza), a brush in her hand. She draws the family the way.
const shizuHolds = {
  /** the scrap of practice paper with the way drawn on it, held out in both hands (kneeling or standing) */
  paper: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.08, head: { nod: nodOf(b) + 0.08 }, held: "paper" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.060, -0.120 - (o.seated ? 0.04 : 0), 0.220], bend: [sd * 0.8, -0.6, -0.3], curl: 0.7, point: [sd * 0.2, 0.9, 0.3] }); return p; },
  /** writing at a low desk in front of her, the left hand flat on the paper */
  writing: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.20, head: { nod: nodOf(b) + 0.26 }, held: "writing" };
    withArm(p, "R", { hand: [0.040, -0.300, 0.230], bend: [0.8, -0.5, -0.4], grip: true, point: [-0.2, -0.8, 0.5] });
    withArm(p, "L", { hand: [-0.070, -0.320, 0.210], bend: [-0.8, -0.4, -0.4], flat: true, point: [0.3, -0.2, 0.9] }); return p; },
};
export const shizu = {
  ...WOMAN_EDO(EDO_PALE, BUDO, { face: { lines: 1, smile: 0.5, brow: { full: [0, -1, 0] } }, len: 1.90, gestures: [0, 8, 6, 20], pace: 140 }),
  name: "O-Shizu, the writing teacher", height: H(149),
  seated: "ground", sit: { seat: "kneel", lean: 0.06, nod: 0.06 }, riseMs: 1700, shadow: 0.20, span: 1.12,
  stance: "clasped", lean: 0.02,
  rest: { R: { hand: [0.050, -0.300, 0.150], bend: [0.9, -0.4, -0.5], grip: true, point: [-0.6, -0.2, 0.7] } },      // the brush in her hand, resting on her knee
  fidgets: { only: true, sit: ["brushwork", "slownod", "look"], stand: ["look", "shift"] }, holds: shizuHolds, cues: { sit: ["brushwork", "slownod"], stand: ["ojigi", "slownod"] }, ...bowOf(0.32),
  stood: { rest: undefined },
  extras(c) { kimono(c, { mat: BUDO, obi: SUMI, knot: "big", sleeve: 0.070 }); const h = c.pose.held; if (h === "paper") sheetAt(c, add(between2(c.J).at, [0, M(c, 0.050), 0]), { w: 0.20, h: 0.14, out: true }); else brushIn(c, "R"); },
};
// The pupils: girls of eight and nine, kneeling at their low desks (the desks are painted), writing; and whispering.
const PUPIL_DESK = { R: { hand: [0.040, -0.280, 0.230], bend: [0.8, -0.5, -0.4], grip: true, point: [-0.2, -0.8, 0.5] }, L: { hand: [-0.070, -0.300, 0.210], bend: [-0.8, -0.4, -0.4], flat: true, point: [0.3, -0.2, 0.9] } };
const pupil = (mat, height, name, o = {}) => ({
  name, height, dim: { ...EDO_CHILD, shoulderW: 0.086 }, skin: o.skin || EDO_SKIN,
  hair: { mat: EDO_HAIR, bulk: [1.10, 1.06, 1.10], where: girlknot, puffs: GIRLKNOT_PUFFS, ears: true },
  face: { ...EDO_CHILD_FACE, ...(o.face || {}) },
  top: { mat, sleeves: 2, ease: 0.006, open: 0.024, under: WHITE }, bottom: { kind: "skirt", mat, len: 1.78, flare: 1.06, wrap: [0.55, -0.30], under: mat },
  shoes: { kind: "bare" },
  seated: "ground", sit: { seat: "kneel", lean: 0.16, nod: 0.20 }, riseMs: 1200, shadow: 0.18, span: 1.15,
  rest: PUPIL_DESK, stance: "clasped", gestures: [0, 13, 0, 9], pace: 175,
  fidgets: { only: true, sit: ["brushwork", "brushwork", "look", "whisper"], stand: ["look", "shift"] }, cues: { sit: ["brushwork", "whisper", "giggle"] },
  stood: { rest: undefined },
  extras(c) { kimono(c, { mat, obi: o.obi || CHA, obiUp: 0.034, obiDown: 0.026, knot: "big", sleeve: 0.050 }); brushIn(c, "R"); },
});
export const pupil1 = pupil(ASAGI, H(128), "a pupil at the writing school", { obi: AKA });
export const pupil2 = pupil(WAKATAKE, H(122), "a pupil at the writing school (the younger)", { obi: KAKI, face: { eyes: "bright", smile: 1 } });
// Old Tōbei, the ward's night man: sells straw sandals and cheap sweets from his hut by the gate; by day on his stool
// (drawn with him), dozing; at night on his rounds with his clappers, calling the fire (`tobei-night`: the lantern at his sash).
const tobeiHolds = {
  /** a sweet held out between finger and thumb ("for the walk") */
  sweet: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.06, smile: 1, head: { nod: nodOf(b) + 0.08 }, held: "sweet" };
    withArm(p, "R", { hand: [0.070, -0.100 - (o.seated ? 0.05 : 0), 0.240], bend: [0.8, -0.6, -0.2], curl: 0.9, point: [0, 0.4, 0.9], thumb: [0, 1, 0] }); return p; },
  /** the clappers up in front of him, about to strike (both hands) */
  clap: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) - 0.04 }, mouth: 2, held: "clap" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.040, -0.080, 0.190], bend: [sd * 0.8, -0.6, -0.3], grip: true, point: [-sd * 0.1, 0.95, 0.2] }); return p; },
};
const tobeiBase = {
  ...workman(EDO_SKIN, { jacket: CHA, trousers: NEZUMI, face: { eyes: "heavy", lines: 2, jaw: 0.86, chin: 0.52, short: { mat: EDO_GREY, stubble: EDO_GREY, from: 0.3 } } }),
  name: "Tōbei, the ward's night man", height: H(150),
  hair: { mat: EDO_GREY, bulk: [1.04, 1.0, 1.04], where: chonmage },
  gestures: [0, 8, 11, 2], walk: { swing: 0.34, arm: 0.18, elbow: 0.40, lean: 0.10, lift: 0.8 }, pace: 115, ...bowOf(0.26),
};
const tobeiGear = (c) => { chonmageTop(c, { mat: EDO_GREY, pate: pateOf(EDO_SKIN) }); kimono(c, { mat: CHA, obi: NEZUMI, obiUp: 0.016, obiDown: 0.024, knot: "small", sleeve: 0.030, jacket: true }); };
export const tobei = {
  ...tobeiBase,
  seated: "chair", sit: { seat: 40 * CM, drawn: true, lean: 0.10, nod: 0.06 }, riseMs: 1300, shadow: 0.20,
  rest: { R: { hand: [0.050, -0.300, 0.180], bend: [0.9, -0.4, -0.4], curl: 0.6 }, L: { hand: [-0.050, -0.300, 0.170], bend: [-0.9, -0.4, -0.4], curl: 0.6 } },
  fidgets: { only: true, sit: ["doze", "look", "shift", "doze"], stand: ["look", "shift", "back"] }, holds: tobeiHolds, cues: { sit: ["doze", "clack"], stand: ["clack", "ojigi"] },
  stood: { rest: undefined },
  extras(c) {
    wear.stool(c, { mat: EDO_WOOD, r: 0.075 });
    tobeiGear(c);
    const h = c.pose.held;
    if (h === "sweet") ball21(c, pinch(c, "R"), 0.010, TAKUAN);
    else if (h === "clap" || c.pose.fidget === "clack") clappersIn(c);
  },
};
export const tobeiNight = {
  ...tobeiBase, name: "Tōbei, on his rounds at night", span: 1.3,
  hold: { R: { hand: [0.040, -0.110, 0.160], bend: [0.8, -0.6, -0.3], grip: true, point: [-0.1, 0.95, 0.2] }, L: { hand: [-0.040, -0.110, 0.160], bend: [-0.8, -0.6, -0.3], grip: true, point: [0.1, 0.95, 0.2] } },      // the clappers, ready
  fidgets: { only: true, stand: ["clack", "look", "clack"] }, holds: tobeiHolds, cues: { stand: ["clack"] },
  extras(c) {
    tobeiGear(c); clappersIn(c);
    const k = M(c, 1), hip = c.trunkAt(c.d.hipY + 0.020, -0.80, 0.010);                // the lantern, hung from his sash at the left hip
    c.limb(hip, add(hip, [0, -0.050 * k, 0.040 * k]), 0.0022 * k, 0.0022 * k, SUMI, { part: c.parts.EXTRA });
    c.ball(add(hip, [0, -0.140 * k, 0.050 * k]), [0.060 * k, 0.090 * k, 0.060 * k], CHOCHIN, { part: c.parts.EXTRA }, c.tw);
  },
};
/** A small round thing (a sweet) at a point. */
function ball21(c, at, r, mat) { c.ball(at, [M(c, r), M(c, r), M(c, r)], mat, { part: c.parts.HELD }); }

// ------------------------------------------------------------------ the foot of Mount Shosha: the women's hall
// O-Ume, about seventy, the hall's keeper (dōmori), the shipwright's widow: small, bent, dry, funny; a tea-brown kimono and
// a grey apron, white hair in a small knot, teeth blackened, no brows. `ume` on her feet; `ume-kneel` kneeling by the door
// in the hall (seiza). She leaves the voice a rice ball on a leaf every evening; she lends a lantern; she pastes up slips.
const umeHolds = {
  /** a rice ball on its leaf, held out in both hands (to the step; to the voice) */
  riceball: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) + 0.10 }, held: "riceball" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.030, -0.140 - (o.seated ? 0.04 : 0), 0.200], bend: [sd * 0.8, -0.6, -0.3], flat: true, point: [-sd * 0.3, 0.1, 0.95], thumb: [-sd, 0, 0] }); return p; },
  /** the lantern, lit, held out on its stick: lent ("Mind the fire") */
  lantern: (o) => fam.lantern(o),
  /** pasting a slip up on a post: the right hand up and flat against it, the head up */
  paste: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) - 0.06, head: { nod: nodOf(b) - 0.22 }, held: "paste" };
    withArm(p, "R", { hand: [0.040, 0.100, 0.200], bend: [0.8, -0.5, -0.3], flat: true, point: [0, 0.9, 0.3], thumb: [-1, 0, 0] }); return p; },
  /** laughing and crying at once, both hands to her face ("That's him. That's his joke.") */
  laughcry: (o) => { const b = o.base, sp = o.sp, hr = o.d.headR, p = { ...cloneP(b), mouth: 2, breath: 1, blink: true, lean: (b.lean || 0) - 0.04, head: { nod: nodOf(b) - 0.10 }, held: "laughcry" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * (hr[0] + 0.006), sp.chinY + 0.030, hr[2] * 0.70], bend: [sd, -0.6, 0.1], flat: true, point: [-sd * 0.3, 0.9, 0.3] }); return p; },
  /** two slips taken in both hands */
  slips: (o) => fam.slips(o),
};
const umeBase = {
  ...WOMAN_EDO(EDO_SKIN, CHA, { face: { brows: null, lines: 2, eyes: "heavy", jaw: 0.78, chin: 0.46, smile: 0.5 }, len: 1.90, gestures: [0, 8, 2, 20], pace: 100, dim: { shoulderW: 0.076, trunkTop: [0.082, 0.064], trunkLow: [0.078, 0.064] } }),
  name: "O-Ume, the hall's keeper", height: H(136),
  hair: { mat: EDO_WHITE_HAIR, bulk: [1.05, 1.0, 1.05], where: marumage, puffs: OLD_KNOT },
  holds: umeHolds, ...bowOf(0.28), span: 1.15,
};
const umeGear = (c) => {
  kimono(c, { mat: CHA, obi: NEZUMI, obiUp: 0.060, obiDown: 0.034, knot: "big", sleeve: 0.060 }); apronOf(c, NEZUMI, 0.40);
  const h = c.pose.held;
  if (h === "riceball") riceballAt(c, add(between2(c.J).at, [0, M(c, 0.020), 0]), { leaf: true, pickle: false });
  else if (h === "lantern") lanternIn(c, "R");
  else if (h === "paste") slipAt(c, add(c.J.R.palm, [0, M(c, 0.050), M(c, 0.016)]));
  else if (h === "slips") { const { at, across } = between2(c.J); for (const sd of [1, -1]) slipAt(c, add(add(at, mul(across, sd * M(c, 0.022))), [0, M(c, 0.080), 0])); }
};
export const ume = {
  ...umeBase, stance: "clasped", lean: 0.18, nod: 0.04,                  // bent with her years
  walk: { swing: 0.26, arm: 0.10, elbow: 0.30, lean: 0.18, lift: 0.6 },
  fidgets: { only: true, stand: ["rubhands", "slownod", "look", "shift"] }, cues: { stand: ["slownod", "rubhands", "ojigi"] },
  extras(c) { umeGear(c); },
};
export const umeKneel = {
  ...umeBase, name: "O-Ume, kneeling by the door", lean: 0.10,
  seated: "ground", sit: { seat: "kneel", lean: 0.12, nod: 0.08 }, riseMs: 2000, shadow: 0.20, stance: "clasped",
  walk: ume.walk, fidgets: { only: true, sit: ["slownod", "rubhands", "look"], stand: ["rubhands", "slownod", "look"] }, cues: { sit: ["slownod", "rubhands"], stand: ["slownod", "ojigi"] },
  stood: { lean: 0.18 },
  extras(c) { umeGear(c); },
};
// Ryōkai, fifteen, a novice from the mountain: earnest, frightened, ashamed. A grey-black robe over white, white tabi, his
// head shaved, prayer beads in his left hand. Found sitting on the step by the stone (the step is painted); on his feet at
// once when anyone makes for the path (`sit(false)`); `ryokai-standing` (at the lattice, outside the hall).
const ryokaiHolds = {
  /** "Women may not climb.": standing in the way, both open hands low and out, palms down, a little bowed: sorry, but no */
  bar: (o) => { const b = o.base, sp = o.sp, p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) + 0.08 }, held: "bar" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * (sp.side + 0.080), sp.waist - 0.010, 0.120], bend: [sd * 0.8, -0.4, -0.4], flat: true, point: [sd * 0.5, -0.2, 0.85], thumb: [0, 0, 1] }); return p; },
  /** his face at the lattice: both hands up on it, leaning in close */
  peer: (o) => { const b = o.base, p = { ...cloneP(b), lean: (b.lean || 0) + 0.14, head: { nod: nodOf(b) - 0.04 }, held: "peer" };
    for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.080, 0.050, 0.180], bend: [sd * 0.8, -0.5, -0.3], flat: true, point: [0, 0.9, 0.3], thumb: [0, 0, 1] }); return p; },
};
export const ryokai = {
  name: "Ryōkai, a novice of the mountain", height: H(150),
  dim: { ...EDO_MAN, shoulderW: 0.090, trunkTop: [0.094, 0.060], trunkLow: [0.080, 0.058], armR: [0.026, 0.022, 0.016], headR: [0.057, 0.067, 0.064] }, skin: EDO_PALE,
  hair: { mat: pateOf(EDO_PALE), bulk: 1, where: shavenHead },
  face: { ...EDO_MAN_FACE, eyes: "wide", jaw: 0.82, chin: 0.50, brow: { full: [0, -1, -1] }, browUp: 3 },
  top: { mat: KOROMO, sleeves: 2, ease: 0.010, open: 0.030, under: WHITE }, bottom: { kind: "skirt", mat: KOROMO, len: 1.86, flare: 1.10, wrap: [0.55, -0.30], under: KOROMO },
  socks: { mat: WHITE, from: 0.86, thick: 0.004 }, shoes: { kind: "sandals", mat: WARAJI, foot: WHITE, sole: shifted(WARAJI, 1) },
  seated: "chair", sit: { seat: "step", solid: true, lean: 0.08, nod: 0.08 }, riseMs: 700, shadow: 0.18, span: 1.15,
  rest: { L: { hand: [-0.040, -0.290, 0.150], bend: [-0.9, -0.4, -0.5], curl: 0.8 } },
  stance: "clasped", lean: 0.03, walk: { swing: 0.40, arm: 0.14, elbow: 0.40, lean: 0.05, lift: 1.0 }, pace: 150,
  gestures: [0, 5, 2, 8], pray: { fold: true, high: 0.52, bow: 0.32 },
  fidgets: { only: true, sit: ["beads", "look", "shift", "beads"], stand: ["look", "shift"] }, holds: ryokaiHolds, cues: { sit: ["beads"], stand: ["ojigi"] }, ...bowOf(0.42),
  stood: { rest: undefined },
  extras(c) { kimono(c, { mat: KOROMO, eri: WHITE, obi: shifted(KOROMO, 1), obiUp: 0.016, obiDown: 0.022, knot: "small", sleeve: 0.095 }); if (!c.pose.held) beadsIn(c, "L"); },
};
export const ryokaiStanding = { ...upOf(ryokai), name: "Ryōkai, on his feet" };
// The women waiting on the bench to leave their slips: Grandmother Tome (thirty tries with her best comb), a young wife
// with her baby on her back, a girl of eleven with her grandmother's slip.
const tomeHolds = {
  /** her best comb held up in front of her, glared at ("It looked at me.") */
  comb: (o) => { const b = o.base, p = { ...cloneP(b), head: { nod: nodOf(b) + 0.06 }, held: "comb" };
    withArm(p, "R", { hand: [0.050, -0.060 - (o.seated ? 0.05 : 0), 0.200], bend: [0.8, -0.7, -0.3], curl: 0.8, point: [-0.6, 0.5, 0.6] }); return p; },
  /** her slip held in both hands in her lap (or at her chest, standing) */
  slip: (o) => fam.slip(o),
};
/** The waiting women's bench by the hall (PAINT-21E's): its seat's height, as the Office's seats are given (CM). */
export const BENCH_SEAT = 42 * CM;
const TOME_COMB = ramp("#c88a4e", "#9c5a28", "#6c3a14", "#40200a");       // her best comb: dark, like tortoiseshell (it is boxwood, lacquered)
export const tome = {
  ...WOMAN_EDO(EDO_SKIN, AI_DEEP, { face: { brows: null, lines: 2, eyes: "deep", jaw: 0.80, chin: 0.48 }, len: 1.86, gestures: [0, 8, 15, 2], pace: 110, dim: { shoulderW: 0.078 } }),
  name: "Grandmother Tome", height: H(138),
  hair: { mat: EDO_GREY, bulk: [1.06, 1.0, 1.06], where: marumage, puffs: OLD_KNOT },
  seated: "chair", sit: { seat: BENCH_SEAT, lean: 0.10, nod: 0.04 }, riseMs: 1500, shadow: 0.18,
  rest: { R: { hand: [0.050, -0.270, 0.170], bend: [0.9, -0.4, -0.4], curl: 0.8, point: [-0.6, 0.2, 0.7] } },      // her comb in her hand, on her knee
  stance: "clasped", lean: 0.10, walk: { swing: 0.28, arm: 0.10, elbow: 0.30, lean: 0.12, lift: 0.7 },
  fidgets: { only: true, sit: ["combup", "shift", "look", "slownod"], stand: ["look", "shift"] }, holds: tomeHolds, cues: { sit: ["combup", "slownod"], stand: ["ojigi"] }, ...bowOf(0.30),
  stood: { rest: undefined },
  extras(c) {
    kimono(c, { mat: AI_DEEP, obi: NEZUMI, obiUp: 0.060, obiDown: 0.034, knot: "big", sleeve: 0.060 });
    if (c.pose.held === "slip") slipAt(c, add(between2(c.J).at, [0, M(c, 0.070), 0]));
    else combAt(c, add(c.J.R.palm, [0, M(c, 0.022), 0]), { mat: TOME_COMB });
  },
};
export const wife = {
  ...WOMAN_EDO(EDO_SKIN, SEIJI, { face: { brows: null, smile: 0.5, blush: "#eea6a0" }, len: 1.80, gestures: [0, 9, 0, 5], pace: 150, dim: { shoulderW: 0.082 } }),
  name: "a young wife, with her baby on her back", height: H(146), span: 1.15,
  seated: "chair", sit: { seat: BENCH_SEAT, lean: 0.06 }, riseMs: 1100, shadow: 0.18,
  stance: "clasped", walk: { swing: 0.42, arm: 0.26, elbow: 0.40, lean: 0.06, lift: 1.0, sway: 0.012 },
  fidgets: { only: true, sit: ["shift", "look"], stand: ["jog", "shift", "look"] }, cues: { stand: ["jog", "ojigi"] }, ...bowOf(0.28),
  extras(c) { kimono(c, { mat: SEIJI, obi: AI_DEEP, knot: "big", sleeve: 0.060 }); babyOnBack(c); },
};
const GIRL_DIM = { ...blend(CHILD, WOMAN, 0.30), headR: [0.062, 0.072, 0.068] };
export const girl = {
  name: "a girl, with her grandmother's slip", height: H(140),
  dim: GIRL_DIM, skin: EDO_SKIN,
  hair: { mat: EDO_HAIR, bulk: [1.10, 1.05, 1.10], where: girlknot, puffs: [[0, 1.00, -0.40, 0.36, 0.30, 0.34]], ears: true },
  face: { ...EDO_CHILD_FACE, eyes: "girl", mouthY: -0.66, jaw: 0.84, chin: 0.52, smile: 0.5 },
  top: { mat: FUJI, sleeves: 2, ease: 0.006, open: 0.024, under: WHITE }, bottom: { kind: "skirt", mat: FUJI, len: 1.80, flare: 1.06, wrap: [0.55, -0.30], under: FUJI },
  shoes: { kind: "sandals", mat: WARAJI, foot: EDO_SKIN, sole: shifted(WARAJI, 1) },
  hold: { R: { hand: [0.020, -0.120, 0.140], bend: [0.9, -0.6, -0.3], curl: 0.8, point: [-0.3, 0.9, 0.3] }, L: { hand: [-0.020, -0.120, 0.140], bend: [-0.9, -0.6, -0.3], curl: 0.8, point: [0.3, 0.9, 0.3] } },      // the slip, in both hands
  stance: "clasped", lean: 0.02, walk: { swing: 0.44, arm: 0.08, elbow: 0.40, lean: 0.06, lift: 1.1 }, pace: 160,
  gestures: [0, 0, 20, 0], fidgets: { only: true, stand: ["look", "shift", "hop"] }, cues: { stand: ["ojigi"] }, ...bowOf(0.30),
  extras(c) { kimono(c, { mat: FUJI, obi: AKA, obiUp: 0.040, obiDown: 0.028, knot: "big", sleeve: 0.065 }); slipAt(c, add(between2(c.J).at, [0, M(c, 0.070), 0])); },
};

// ---- their own small movements (figure.fidget(name); each page's `fidgets` says which are theirs, `cues` what a script plays) ----
addMoves({
  /** O-Fusa: crying: both fists to her eyes, rubbing, the shoulders going */
  sniffle: { ms: 2600, make(o) {
    const b = o.base, sp = o.sp, hr = o.d.headR, at = (dx, br) => { const p = { ...cloneP(b), breath: br, blink: true, lean: (b.lean || 0) + 0.06, head: { nod: nodOf(b) + 0.12 } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * (0.026 + dx), sp.chinY + hr[1] * 0.90, hr[2] + 0.024], bend: [sd, -0.6, 0.1], grip: true, point: [-sd * 0.3, 0.9, 0.3] }); return p; };
    return [[0, b], [0.18, at(0, 1)], [0.32, at(0.006, 0.2)], [0.46, at(0, 1)], [0.60, at(0.006, 0.2)], [0.76, at(0, 0.8)], [1, b]];
  } },
  /** O-Tane: wringing her hands at her waist, a glance toward the school */
  fret: { ms: 2600, make(o) {
    const b = o.base, sp = o.sp, at = (dx, turn) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.04, turn } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.012 + dx, sp.waist + 0.010, sp.belly + 0.050], bend: [sd * 0.5, -0.2, -0.8], curl: 0.9 }); return p; };
    return [[0, b], [0.20, at(0.010, 0.30)], [0.36, at(-0.010, 0.34)], [0.52, at(0.010, 0.30)], [0.70, at(-0.006, -0.10)], [1, b]];
  } },
  /** O-Kiku: a toe scuffs the ground, a sway, the head lower */
  scuff: { ms: 2400, make(o) {
    const b = o.base, at = (k) => { const p = { ...cloneP(b), sway: -0.006 * k, head: { nod: nodOf(b) + 0.08 * k, turn: 0.10 * k } }; p.R = { ...p.R, leg: [0.12 * k, 0.06], knee: 0.20 * k, foot: 0.25 * k }; return p; };
    return [[0, b], [0.24, at(1)], [0.40, at(0.4)], [0.56, at(1)], [0.80, at(0.2)], [1, b]];
  } },
  /** the writing school: the brush goes in small strokes on the paper on the desk in front, the head down to it (kneeling) */
  brushwork: { ms: 2800, make(o) {
    const b = o.base, at = (dx, dy) => { const p = { ...cloneP(b), lean: (b.lean || 0) + 0.08, head: { nod: nodOf(b) + 0.10 } }; return withArm(p, "R", { hand: [0.040 + dx, -0.280 + dy, 0.240], bend: [0.8, -0.5, -0.4], grip: true, point: [-0.2, -0.8, 0.5] }); };
    return [[0, b], [0.16, at(0, 0)], [0.30, at(-0.010, -0.012)], [0.44, at(0.004, 0.004)], [0.58, at(-0.008, -0.014)], [0.74, at(0.002, 0)], [1, b]];
  } },
  /** Tōbei: nods off on his stool, the head sinking slowly, and jerks awake */
  doze: { ms: 3600, make(o) {
    const b = o.base, at = (n, bl) => ({ ...cloneP(b), blink: bl, breath: 0.2, lean: (b.lean || 0) + n * 0.3, head: { nod: nodOf(b) + n } });
    return [[0, b], [0.40, at(0.30, true)], [0.70, at(0.36, true)], [0.76, at(-0.06, false)], [0.86, at(0.02, false)], [1, b]];
  } },
  /** Tōbei: strikes the clappers together, twice (hi no yōjin): both hands come in and part */
  clack: { ms: 1600, make(o) {
    const b = o.base, at = (gap, mouth) => { const p = { ...cloneP(b), mouth, head: { nod: nodOf(b) - 0.06 } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * gap, -0.080, 0.190], bend: [sd * 0.8, -0.6, -0.3], grip: true, point: [-sd * 0.1, 0.95, 0.2] }); return p; };
    const apart = at(0.070, 0), shut = at(0.022, 2);
    return [[0, b], [0.20, apart], [0.32, shut], [0.46, apart], [0.58, shut], [0.76, apart], [1, b]];
  } },
  /** Grandmother Tome: brings her best comb up in front of her face and glares at it, and puts it down again */
  combup: { ms: 2600, make(o) {
    const b = o.base, at = (dy, turn) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.04, turn } }, "R", { hand: [0.050, -0.060 + dy - (o.seated ? 0.05 : 0), 0.200], bend: [0.8, -0.7, -0.3], curl: 0.8, point: [-0.6, 0.5, 0.6] });
    return [[0, b], [0.26, at(0, 0.04)], [0.50, at(0.010, -0.06)], [0.74, at(0, 0.04)], [1, b]];
  } },
  /** O-Ume: rubs her hands together, slowly */
  rubhands: { ms: 2200, make(o) {
    const b = o.base, sp = o.sp, at = (dz) => { const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.06 } }; for (const [s, sd] of [["R", 1], ["L", -1]]) withArm(p, s, { hand: [sd * 0.010, sp.waist + 0.030, sp.belly + 0.070 + sd * dz], bend: [sd * 0.8, -0.4, -0.4], flat: true, point: [-sd * 0.4, 0.6, 0.6] }); return p; };
    return [[0, b], [0.20, at(0.012)], [0.36, at(-0.012)], [0.52, at(0.012)], [0.68, at(-0.012)], [1, b]];
  } },
});

// ---- the lock's close-up: three hands at once (#37) ----
// `edo-lock` is the lock on the hall's doors seen close, nobody standing in it. While a part of the lock is held, the hand
// that holds it is drawn at the painter's hand point (ENGINE-21's g.hand(id, point, spec), with LOCK_HANDS[...] as the spec):
// Little Sister's small hand with O-Tami's pin in the rabbit's ear (`handEar`), Mom's turning the coin on the square post
// (`handPost`), Big Sister's pressing the comb's teeth into the slits along its back (`handComb`). Each is a forearm in its
// kimono sleeve coming in from outside the picture, and the hand seen from where we stand (its back), with the thing it holds,
// drawn flat by the renderer in the people's own way (two tones, the light from the upper left, a line round each part) at
// half the size it shows and doubled in hard pixels, so that it is the same stuff as the people. Its anchor (ox, oy) is the
// working point: the pin's tip in the ear, the coin's middle on the post, the middle of the comb's teeth at the slits.
//   scale 1: 6.5 stage pixels to the centimetre (Mom's hand, 18 cm, is 117 pixels long): set it from PAINT-21E's lock.
//   from: where the arm comes in from, in degrees round from straight up out of the bottom edge (0 from below, 90 from the
//   right, -90 from the left, 180 from above): each arm from where its owner stands.
const HAND_PX_PER_CM = 6.5;
const HAND_PARTS = { SLEEVE: 1, CUFF: 2, ARM: 3, PALM: 4, FINGER: 5, THUMB: 6, THING: 7 };
const handKept = new Map();
/** One hand of the lock's three: who ("lilsis", "mom", "bigsis"), and o: { scale, from, turned (Mom's coin turned a
    quarter), coin (false: the coin is the painting's, not drawn with her hand), px (2: drawn at half and doubled), reach
    (how far the sleeve goes, in cm) }. Gives { canvas, ox, oy } (the anchor in the canvas). In a browser only. */
export function lockHand(who, o = {}) {
  const scale = o.scale ?? 1, from = o.from ?? { lilsis: -30, mom: 25, bigsis: 155 }[who] ?? 0, px = o.px ?? 2, reach = o.reach ?? 60;
  const key = `${who}|${scale}|${from}|${o.turned ? 1 : 0}|${o.coin === false ? 0 : 1}|${px}|${reach}|${keyId()}`;
  if (handKept.has(key)) return handKept.get(key);
  const k = (HAND_PX_PER_CM * scale) / px, P = HAND_PARTS;
  const turn = ((-from + (who === "mom" && o.turned ? 40 : 0)) * Math.PI) / 180, cs = Math.cos(turn), sn = Math.sin(turn);
  const shapes = [];                                        // [kind, points in cm, radii in cm, z, material, part, opts]
  const L = (a, b, ra, rb, z, mat, part, opt = {}) => shapes.push(["limb", a, b, ra, rb, z, mat, part, opt]);
  const B = (c, rx, ry, z, mat, part, opt = {}) => shapes.push(["ball", c, rx, ry, z, mat, part, opt]);
  const sleeve = { lilsis: PINK, mom: EMERALD, bigsis: INDIGO }[who] || EMERALD;
  const arm = (wristY, rW, rArm) => {                       // the forearm from the wrist down out of the picture, in its sleeve
    L([0, wristY], [0, wristY + 5], rW, rArm, 2, SKIN, P.ARM);
    L([0, wristY + 3.4], [0, wristY + 4.8], rArm + 0.25, rArm + 0.35, 3, WHITE, P.CUFF, { squareStart: true, squareEnd: true });     // the under-sleeve's white at the cuff
    L([0, wristY + 4.4], [0, wristY + reach], rArm + 0.9, rArm + 3.4, 1, sleeve, P.SLEEVE, { squareStart: true });
  };
  if (who === "lilsis") {                                   // a girl of seven: the hand 12.5 cm; the pin pinched between thumb and first finger, its tip in the ear
    L([0, 0], [0.15, 10.5], 0.24, 0.24, 9, KANZASHI, P.THING);
    B([0.18, 9.4], 0.55, 0.55, 9, KANZASHI, P.THING);
    L([0.6, 15.6], [0.2, 9.4], 2.6, 3.0, 4, SKIN, P.PALM);                                   // the palm (the back of the hand)
    L([-0.6, 9.4], [-0.1, 6.0], 0.62, 0.55, 6, SKIN, P.FINGER);                              // the first finger, up along the pin
    for (const [x, y] of [[0.9, 9.6], [2.0, 10.0], [2.9, 10.7]]) L([x, y], [x + 0.1, y - 1.5], 0.66, 0.62, 5, SKIN, P.FINGER);      // the other three, curled under (from behind: short)
    L([-2.6, 13.2], [-1.6, 8.6], 0.85, 0.70, 7, SKIN, P.THUMB); L([-1.6, 8.6], [-0.55, 6.5], 0.70, 0.58, 7, SKIN, P.THUMB);       // the thumb, pinching
    arm(16.4, 2.2, 2.5);
  } else if (who === "mom") {                               // a woman's hand, 18 cm, the thumb and first finger on the coin's rim, turning it
    if (o.coin !== false) B([0, 0], 1.25, 1.25, 8, MON, P.THING, { hole: true });
    L([1.2, 23.0], [1.4, 9.6], 3.4, 4.1, 4, SKIN, P.PALM);
    L([0.2, 9.0], [1.3, 1.6], 0.86, 0.78, 6, SKIN, P.FINGER); L([1.3, 1.6], [1.25, -0.45], 0.78, 0.72, 6, SKIN, P.FINGER);       // the first finger, its tip on the coin's right
    L([1.8, 9.2], [2.9, 2.6], 0.88, 0.78, 5, SKIN, P.FINGER);                                 // the second, beside it
    for (const [x, y] of [[3.3, 9.9], [4.4, 10.8]]) L([x, y], [x + 0.2, y - 2.1], 0.86, 0.80, 5, SKIN, P.FINGER);      // the last two, curled under (from behind: short)
    L([-3.0, 15.0], [-2.7, 7.6], 1.20, 1.00, 7, SKIN, P.THUMB); L([-2.7, 7.6], [-1.45, 0.55], 1.00, 0.82, 7, SKIN, P.THUMB);     // the thumb, its tip on the coin's left
    arm(22.2, 2.9, 3.2);
  } else {                                                  // a girl of thirteen, 16.5 cm: her fingers along the comb's back, pressing its teeth in
    L([-4.4, 0.05], [4.4, 0.05], 0.85, 0.85, 4, TSUGE, P.THING, { squareStart: true, squareEnd: true, teeth: true });      // the teeth, into the slits
    L([-4.5, 1.9], [4.5, 1.9], 1.35, 1.35, 4, TSUGE, P.THING, { squareStart: true, squareEnd: true });                    // its back
    L([0.4, 18.0], [0.2, 7.4], 3.2, 3.8, 6, SKIN, P.PALM);
    for (const [x, len] of [[-2.0, 4.4], [-0.6, 5.0], [0.8, 4.8], [2.1, 3.9]]) L([x, 7.2], [x * 1.12, 7.2 - len + 0.2], 0.80, 0.70, 8, SKIN, P.FINGER);      // four fingers down onto the comb's back
    L([-3.4, 12.4], [-4.0, 4.8], 1.05, 0.88, 9, SKIN, P.THUMB); L([-4.0, 4.8], [-4.2, 2.2], 0.88, 0.76, 9, SKIN, P.THUMB);       // the thumb, on the comb's end
    arm(17.0, 2.6, 2.9);
  }
  // where everything is in the picture (rotated about the anchor), and how big the picture must be
  const at = ([x, y]) => [(x * cs - y * sn) * k, (x * sn + y * cs) * k];
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  const grow = (q, r) => { x0 = Math.min(x0, q[0] - r); y0 = Math.min(y0, q[1] - r); x1 = Math.max(x1, q[0] + r); y1 = Math.max(y1, q[1] + r); };
  for (const sh of shapes) { if (sh[0] === "limb") { grow(at(sh[1]), sh[3] * k); grow(at(sh[2]), sh[4] * k); } else grow(at(sh[1]), Math.max(sh[2], sh[3]) * k); }
  const pad = 4, W = Math.ceil(x1 - x0) + pad * 2, H = Math.ceil(y1 - y0) + pad * 2, ax = Math.round(-x0 + pad), ay = Math.round(-y0 + pad);
  const sf = new Surface(W, H, ax, ay);
  for (const sh of shapes) {
    if (sh[0] === "limb") {
      const [, a, b, ra, rb, z, mat, part, opt] = sh, A = at(a), Bq = at(b);
      const teeth = opt.teeth ? (t, nx, ny, x) => ((x & 1) ? shifted(mat, 1) : undefined) : null;
      sf.limb(ax + A[0], ay + A[1], z * 6, ax + Bq[0], ay + Bq[1], z * 6, Math.max(0.8, ra * k), Math.max(0.8, rb * k), mat, { part, squareStart: opt.squareStart, squareEnd: opt.squareEnd, fn: teeth, depth: 0.6 });
    } else {
      const [, c, rx, ry, z, mat, part, opt] = sh, C = at(c), r = Math.max(0.8, rx * k);
      sf.ball(ax + C[0], ay + C[1], z * 6, r, Math.max(0.8, ry * k), r * 0.4, mat, { part, fn: opt.hole ? (ux, uy) => (Math.abs(ux) < 0.28 && Math.abs(uy) < 0.28 ? shifted(mat, 3) : undefined) : null });
    }
  }
  sf.finish({ reach: 3, rim: true, outline: true, cast: (a, b) => (a > b && a !== P.SLEEVE ? 2 : 0) });
  const canvas = document.createElement("canvas");
  canvas.width = W * px; canvas.height = H * px;
  const g = canvas.getContext("2d"), small = document.createElement("canvas");
  small.width = W; small.height = H;
  small.getContext("2d").putImageData(new ImageData(new Uint8ClampedArray(sf.out.buffer), W, H), 0, 0);
  g.imageSmoothingEnabled = false; g.drawImage(small, 0, 0, W * px, H * px);
  const pic = { canvas, ox: ax * px, oy: ay * px };
  handKept.set(key, pic);
  return pic;
}
/** The specs for g.hand (ENGINE-21): `g.hand("lilsis", "handEar", LOCK_HANDS.lilsis)`, "mom" at `handPost` (and
    `mom-turned` once the coin has clicked round), "bigsis" at `handComb`. Each `draw(scale)` takes the hand's `scale` as
    g.hand gives it; set `from` (and the scale) from the painter's lock with withHand(LOCK_HANDS.mom, { from: 40 }). */
export const LOCK_HANDS = {
  lilsis: { from: -30, draw(scale) { return lockHand("lilsis", { scale, from: this.from, coin: this.coin }); } },
  mom: { from: 25, draw(scale) { return lockHand("mom", { scale, from: this.from, coin: this.coin }); } },
  "mom-turned": { from: 25, draw(scale) { return lockHand("mom", { scale, from: this.from, turned: true, coin: this.coin }); } },
  bigsis: { from: 155, draw(scale) { return lockHand("bigsis", { scale, from: this.from }); } },
};
/** A hand's spec with other settings (from, coin: false). */
export const withHand = (spec, o) => ({ ...spec, ...o, draw: spec.draw });

/** The kinds this section adds to the people table (spread into it below). */
const PEOPLE_21B = {
  "bigsis-edo-kurogo": bigsisEdoKurogo, "lilsis-edo-kurogo": lilsisEdoKurogo,
  "lilsis-edo-wading": lilsisEdoWading, "lilsis-edo-hatback-wading": lilsisEdoHatbackWading, "lilsis-edo-hand": lilsisEdoHand, "lilsis-edo-hatback-hand": lilsisEdoHatbackHand,
  fusa, "fusa-ladle": fusaLadle, leader, heita, "heita-standing": heitaStanding, sato, satosister,
  awapilgrim1, awapilgrim2, "awapilgrim1-ashore": awapilgrim1Ashore, "awapilgrim2-ashore": awapilgrim2Ashore,
  tane, kiku, "kiku-hand": kikuHand, shizu, pupil1, pupil2, tobei, "tobei-night": tobeiNight,
  ume, "ume-kneel": umeKneel, ryokai, "ryokai-standing": ryokaiStanding, tome, wife, girl,
};
// ===================================================================================== PEOPLE-21B (end)

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
  // PEOPLE-20: Japan, 1830. The family's outfits (g.dress(who, name) puts `people[<lead>-<name>]` on), and the people of the act
  "mom-edo": momEdo, "mom-edo-hatback": momEdoHatback, "mom-edo-crew": momEdoCrew, "mom-edo-baby": momEdoBaby, "mom-edo-mirror": momEdoMirror, "mom-edo-crew-mirror": momEdoCrewMirror,
  "bigsis-edo": bigsisEdo, "bigsis-edo-hatback": bigsisEdoHatback, "bigsis-edo-crew": bigsisEdoCrew,
  "lilsis-edo": lilsisEdo, "lilsis-edo-hatback": lilsisEdoHatback, "lilsis-edo-crew": lilsisEdoCrew, "lilsis-edo-lying": lilsisEdoLying, "lilsis-lying": lilsisLying,
  kihei, tami, "tami-baby": tamiBaby, sankichi, tokuzo, gonroku, masa, sei, jinsuke, orin, isuke, tomezo, "tomezo-ladder": tomezoLadder,
  guard1, guard2, shinnosuke, "shinnosuke-floor": shinnosukeFloor, netmender, basketwoman, "basketwoman-dropped": basketwomanDropped,
  pilgrim1, pilgrim2, pilgrim3, plasterer1, plasterer2,
  // PEOPLE-21A: Act Six made bigger (round twenty-one): the people of the Satta Pass, the ship and Osaka, and the boy puppet
  ...PEOPLE_21A.kinds,
  ...PEOPLE_21B,                                                         // PEOPLE-21B: Akashi, Himeji, Shosha; the girls' black robes; Little Sister wading
};
// PEOPLE-21A: the holds that work the boy puppet (`doll`, `dollear`, `dollrun`, `dollkneel`, and the movement `dollrun`), on
// every page of Big Sister's and Little Sister's, whatever section made it (PEOPLE-21B's edo-kurogo among them): here, below
// the table, so that the order of the sections above does not matter.
for (const s of Object.values(people)) PEOPLE_21A.giveDollHolds(s);
/** PEOPLE-21A: the boy puppet's geometry, for the engine and the theatre's scene: where its three operators stand from its
    place (TROUPE, metres: [to its right, forward], all facing the way it faces), how high the boards are that it stands on
    over their floor (PUPPET_RAIL, as a seat's height), how far its feet float (DOLL_FLOAT, in its own heights), its height in
    metres (DOLL_M), and its points for a pose (dollPoints(name): its back, hands and heels, in metres from its place). */
export const PUPPET = { TROUPE: PEOPLE_21A.TROUPE, PUPPET_RAIL: PEOPLE_21A.PUPPET_RAIL, DOLL_FLOAT: PEOPLE_21A.DOLL_FLOAT, DOLL_M: PEOPLE_21A.DOLL_M, dollPoints: PEOPLE_21A.dollPoints };
