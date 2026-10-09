// The character rig. A person is a small jointed figure: head, torso, two arms,
// two legs. A pose says how each joint is bent. The rig works out where the joints
// are, turns the figure to face one of eight directions, and hands the shapes to the
// pixel renderer (pix.js).
//
// One description of a character therefore gives every view of them and every
// frame of every animation, and a new character is a page of settings, not a
// sheet of drawings. Several classic adventure games filmed actors and worked from
// the video; this is the same idea with a puppet in place of the actor.
//
// The look is the hand-pixelled figure of the early 1990s at a larger size: realistic
// proportions, flat areas of color, one darker tone on the side away from the light,
// a shadow under the chin and under each hem, a drawn line where cloth folds, and a
// small careful face. Nothing is modelled round.
//
// Directions are angles: 0 faces the viewer, 90 faces screen right, 180 faces
// away, 270 faces screen left.
//
// Measurements are fractions of the character's own height.

import { Surface, ramp, pack, shifted } from "./pix.js";

const DEG = Math.PI / 180;

/** Art pixels tall for a full-height adult at scale 1. The stage is 800x600 art pixels. */
export const BASE = 160;

// ---------- small vector helpers (x: the character's right, y: up, z: forward) ----------
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
const mix = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const unit = (v) => { const n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / n, v[1] / n, v[2] / n]; };
/** Turn about the upright axis. A positive angle swings "forward" toward the character's right. */
const turn = (v, a) => { const c = Math.cos(a), s = Math.sin(a); return [v[0] * c + v[2] * s, v[1], -v[0] * s + v[2] * c]; };
/** Which way a limb points: hanging straight down, swung forward by `pitch`, and out to its own side by `roll`. */
const dirOf = (pitch, roll, side) => [side * Math.sin(roll), -Math.cos(roll) * Math.cos(pitch), Math.cos(roll) * Math.sin(pitch)];
const lerp = (a, b, t) => a + (b - a) * t;
const clamp1 = (v) => Math.max(-1, Math.min(1, v));
const wrap = (a) => Math.atan2(Math.sin(a), Math.cos(a));

// ---------- proportions ----------
// A grown man is a little over seven heads tall, with legs half his height: the proportions of a
// figure drawing, not of a toy. Limbs taper: thick where the muscle is, fine at the wrist and ankle.
export const ADULT = {
  headR: [0.054, 0.0645, 0.061],           // the skull: half width, half height, half depth. The jaw hangs a little below it.
  neckY: 0.848, shoulderY: 0.815, waistY: 0.600, hipY: 0.498,
  shoulderW: 0.100, shoulderDrop: 0.044, hipW: 0.052,     // the arm hangs from a point this far out from the spine and this far below the shoulder line
  trunkTop: [0.104, 0.066], trunkLow: [0.090, 0.066], bellyFwd: 0,   // [half width, half depth] at the chest and at the waist; bellyFwd carries the waist forward.
                                                                     // An optional trunkHem gives the size at the bottom edge of the shirt.
  pelvisR: [0.094, 0.062, 0.072],
  upperArm: 0.172, foreArm: 0.150, armR: [0.029, 0.024, 0.017], handR: 0.022,      // armR: at the shoulder, the elbow and the wrist
  thigh: 0.240, shin: 0.226, legR: [0.050, 0.031, 0.021], ankleH: 0.038, foot: 0.106, footR: 0.021,      // legR: at the hip, the knee and the ankle
};

// A child of nine or ten is about six heads tall: a bigger head for the body, shorter legs, softer limbs.
export const CHILD = {
  headR: [0.067, 0.078, 0.074],
  neckY: 0.812, shoulderY: 0.780, waistY: 0.580, hipY: 0.480,
  shoulderW: 0.092, shoulderDrop: 0.040, hipW: 0.050,
  trunkTop: [0.100, 0.068], trunkLow: [0.092, 0.070], bellyFwd: 0,
  pelvisR: [0.094, 0.060, 0.072],
  upperArm: 0.158, foreArm: 0.138, armR: [0.027, 0.023, 0.017], handR: 0.022,
  thigh: 0.228, shin: 0.214, legR: [0.047, 0.032, 0.022], ankleH: 0.040, foot: 0.112, footR: 0.022,
};

/** A set of proportions part-way between two others: blend(CHILD, ADULT, 0.6) is a young teenager. */
export function blend(a, b, t) {
  const out = {};
  for (const key of Object.keys(a)) out[key] = Array.isArray(a[key]) ? a[key].map((v, i) => lerp(v, b[key][i], t)) : lerp(a[key], b[key], t);
  return out;
}

/** A grown woman: narrower shoulders and waist, slimmer limbs, smaller hands and feet. */
export const WOMAN = {
  ...ADULT,
  headR: [0.054, 0.0645, 0.061],
  shoulderW: 0.084, shoulderDrop: 0.042, hipW: 0.052,
  trunkTop: [0.088, 0.062], trunkLow: [0.070, 0.054],
  pelvisR: [0.094, 0.060, 0.072],
  armR: [0.024, 0.020, 0.0145], handR: 0.019,
  legR: [0.047, 0.029, 0.018], foot: 0.094, footR: 0.018,
};

// part numbers, used for the thin shadows where one part overlaps another
const HEAD = 1, HAIR = 2, TORSO = 3, PELVIS = 4, ARM = { R: 5, L: 6 }, LEG = { R: 7, L: 8 }, FOOT = { R: 9, L: 10 }, EXTRA = 11, HAT = 12, NECK = 13;
const SHORTS = { R: 14, L: 15 }, SLEEVE = { R: 16, L: 17 };          // cloth that ends part-way down a limb, so its hem can cast a line
const EXTRA2 = 18;                                                    // a second carried thing, so that it shows against the first
const SKIRT = 19, EXTRA3 = 20;
const NOSE = 21, EAR = 22, HAND = { R: 23, L: 24 }, DRAPE = 25, DRAPE2 = 26, BELT = 27, COLLAR = 28, HELD = 29;
/** Part numbers, for code that looks at a finished figure (the head-and-shoulders portraits, for one). */
export const PARTS = { HEAD, HAIR, HAT, NECK, TORSO };

const SHADOW = { tones: [pack("#00000040"), pack("#00000040"), pack("#00000040"), pack("#00000040")], soft: true, flat: 1 };

// ---------- from a pose to joint positions ----------
function skeleton(d, p) {
  const lean = p.lean || 0, tw = p.twist || 0, ht = p.hipTwist || 0, br = p.breath || 0;
  const up = [0, Math.cos(lean), Math.sin(lean)], fw = [0, -Math.sin(lean), Math.cos(lean)];
  // torso space (right, up, forward) to character space: leaning from the hips, shoulders turned about the spine
  const torso = (v) => {
    const r = v[0] * Math.cos(tw) + v[2] * Math.sin(tw), f = -v[0] * Math.sin(tw) + v[2] * Math.cos(tw);
    return [r, v[1] * up[1] + f * fw[1], v[1] * up[2] + f * fw[2]];
  };
  const hipC = [p.sway || 0, d.hipY + (p.rise || 0), p.shift || 0];
  const spine = (h) => add(hipC, torso([0, h - d.hipY, 0]));
  const J = { hipC, sh: spine(d.shoulderY + 0.006 * br), neck: spine(d.neckY + 0.006 * br), torso, lean, twist: tw, hipTwist: ht };
  const hn = (p.head && p.head.nod) || 0, nod = lean * 0.7 + hn;
  J.head = add(J.neck, add(mul([0, Math.cos(nod), Math.sin(nod)], 0.010 + d.headR[1]), torso([0, 0, 0.005])));
  J.headYaw = tw * 0.4 + ((p.head && p.head.turn) || 0);
  J.headPitch = hn + lean * 0.35;                                       // the face tips with the nod; a leaning body keeps its head a little more level

  for (const [key, s] of [["R", 1], ["L", -1]]) {
    const q = p[key] || {};
    const arm = q.arm || [0.03, 0.10], leg = q.leg || [0, 0.03];
    const sLoc = [s * d.shoulderW, -(d.shoulderDrop ?? 0.046), 0];
    const shoulder = add(J.sh, torso(sLoc));
    let elbow, wrist, uDir, fDir, eLoc, wLoc;                           // (eLoc, wLoc: the elbow and the wrist in the torso's own space)
    if (q.hand) {
      // A place for the hand, measured in torso space from the middle of the shoulders. The elbow goes
      // wherever it must (out, down and back, unless `bend` says otherwise), so the same pose fits any build.
      const t = sub(q.hand, sLoc), a = d.upperArm, b = d.foreArm;
      const far = Math.hypot(t[0], t[1], t[2]), len = Math.min(a + b - 0.002, Math.max(Math.abs(a - b) + 0.002, far));
      const dir = far > 1e-6 ? mul(t, 1 / far) : [0, -1, 0];
      const along = (a * a - b * b + len * len) / (2 * len), out = Math.sqrt(Math.max(0, a * a - along * along));
      const hint = q.bend || [s * 0.55, -0.45, -0.70];
      const side = unit(sub(hint, mul(dir, dot3(hint, dir))));
      eLoc = add(sLoc, add(mul(dir, along), mul(side, out))); wLoc = add(sLoc, mul(dir, len));
      elbow = add(J.sh, torso(eLoc)); wrist = add(J.sh, torso(wLoc));
      uDir = unit(sub(elbow, shoulder)); fDir = unit(sub(wrist, elbow));
    } else {
      uDir = torso(dirOf(arm[0], arm[1], s));
      elbow = add(shoulder, mul(uDir, d.upperArm));
      fDir = q.fore ? unit(torso(q.fore)) : torso(dirOf(arm[0] + (q.elbow ?? 0.12), arm[1] * 0.5 - (q.tuck || 0), s));
      wrist = add(elbow, mul(fDir, d.foreArm));
      eLoc = add(sLoc, mul(dirOf(arm[0], arm[1], s), d.upperArm));
      wLoc = add(eLoc, mul(q.fore ? unit(q.fore) : dirOf(arm[0] + (q.elbow ?? 0.12), arm[1] * 0.5 - (q.tuck || 0), s), d.foreArm));
    }
    // The hand: a palm, then fingers that curl a little the way the elbow bends. A grip is a fist.
    const hDir = q.point ? unit(torso(q.point)) : fDir, hl = d.handR * 3.4;
    let bendDir = sub(fDir, mul(uDir, dot3(fDir, uDir)));
    bendDir = Math.hypot(bendDir[0], bendDir[1], bendDir[2]) > 0.2 ? unit(bendDir) : torso([-s * 0.5, 0, 0.86]);
    bendDir = unit(sub(bendDir, mul(hDir, dot3(bendDir, hDir))));
    const fist = q.grip || q.finger;                                    // (a pointing hand is a fist with one finger out of it)
    const curl = fist ? 1.45 : q.flat ? 0.05 : (q.curl ?? 0.42);
    const fingers = unit(add(mul(hDir, Math.cos(curl)), mul(bendDir, Math.sin(curl))));
    const palm = add(wrist, mul(hDir, hl * 0.50)), tip = add(palm, mul(fingers, hl * (fist ? 0.26 : 0.50)));
    // the thumb lies along the forward (or upper) edge of the hand, or wherever `thumb` says (an open hand held palm up has it outward)
    let edge = torso(q.thumb || (Math.abs(hDir[2]) > 0.75 ? [0, 1, 0] : [0, 0, 1]));
    edge = unit(sub(edge, mul(hDir, dot3(edge, hDir))));
    const thumb0 = add(wrist, add(mul(hDir, hl * 0.20), mul(edge, d.handR * 0.62)));
    const thumb1 = add(thumb0, mul(unit(add(mul(hDir, 0.80), mul(edge, 0.60))), hl * (q.grip ? 0.20 : 0.30)));

    const hip = add(hipC, turn([s * d.hipW, 0, 0], ht));
    const tDir = turn(dirOf(leg[0], leg[1], s), ht);
    const knee = add(hip, mul(tDir, d.thigh));
    const sDir = q.shin ? unit(turn(q.shin, ht)) : turn(dirOf(leg[0] - (q.knee ?? 0.02), leg[1], s), ht);
    const ankle = add(knee, mul(sDir, d.shin));
    // The foot, measured along its sole: the back of the heel, the ball, the tip of the toes.
    // When the heel comes up the toes stay flat on the ground, as they do.
    const fp = q.foot || 0, fy = ht + s * (q.footYaw ?? 0.24), tp = Math.max(fp, -0.12);
    const along = turn([0, Math.sin(fp), Math.cos(fp)], fy), nrm = turn([0, Math.cos(fp), -Math.sin(fp)], fy);
    const heel = add(ankle, add(mul(nrm, -d.ankleH), mul(along, -0.27 * d.foot)));
    const ballOf = add(heel, mul(along, 0.72 * d.foot));
    const toeDir = turn([0, Math.sin(tp), Math.cos(tp)], fy), toe = add(ballOf, mul(toeDir, 0.28 * d.foot));
    J[key] = { shoulder, elbow, wrist, palm, tip, thumb0, thumb1, uDir, fDir, hDir, hip, knee, ankle, heel, ball: ballOf, toe, along, nrm, toeDir, footYaw: fy, footPitch: fp, calfBack: turn([0, 0, -1], fy), sLoc, eLoc, wLoc };
  }

  // Stand the figure on the ground: whatever is lowest touches y = 0.
  let low = Infinity;
  for (const k of ["R", "L"]) low = Math.min(low, J[k].heel[1], J[k].ball[1], J[k].toe[1]);
  if (p.seated) low = Math.min(low, hipC[1] - d.pelvisR[1] - (p.seat || 0));
  if (p.ground != null) low = p.ground;                                  // a pose may say where the ground is itself
  const lower = new Set();
  const drop = (v) => { if (Array.isArray(v) && v.length === 3 && !lower.has(v)) { lower.add(v); v[1] -= low; } };
  for (const k of ["hipC", "sh", "neck", "head"]) drop(J[k]);
  for (const k of ["R", "L"]) for (const name of ["shoulder", "elbow", "wrist", "palm", "tip", "thumb0", "thumb1", "hip", "knee", "ankle", "heel", "ball", "toe"]) drop(J[k][name]);
  J.spine = spine;                                                     // a point on the spine at a given height (hipC has been moved, so this follows)
  J.seatY = hipC[1] - d.pelvisR[1] * 0.62;                             // the height of whatever is being sat on
  return J;
}

// ---------- shirt patterns ----------
const hash = (a, b) => { let h = (a * 374761393 + b * 668265263) | 0; h = (h ^ (h >>> 13)) * 1274126177; return ((h ^ (h >>> 16)) >>> 0); };

/** Scattered flowers. `around` is the distance round the body and `high` the height, both in body heights. */
function flowers(around, high, colors) {
  const cell = 0.052, u = around / cell, v = high / cell;
  const iu = Math.floor(u), iv = Math.floor(v), h = hash(iu, iv);
  if (h % 100 > 62) return undefined;
  const fx = 0.28 + ((h >>> 8) % 100) / 220, fy = 0.28 + ((h >>> 16) % 100) / 220;
  const dx = u - iu - fx, dy = v - iv - fy, d2 = dx * dx + dy * dy;
  if (d2 < 0.035) return colors[(h >>> 4) % 2];
  if (d2 < 0.085 && ((h >>> 2) & 1) && dx * dy > 0) return colors[2];
  return undefined;
}

// ---------- eyes ----------
// Each kind of eye is a few rows of pixels, written from the corner nearest the nose outward. The row
// marked by `at` is the one the eye itself is on.  # the dark of the eye (the pupil, in the iris's own darkest
// colour)   i the iris   o the white   h the light in the eye   = the lid, or the lashes, drawn as a dark line
// - a shadow under the brow or under the eye   . nothing.
// `full` is the eye seen from in front; `thin` is the far eye of a three-quarter view, or an eye in profile.
// (face.iris gives the iris its colour; with none, `i` is drawn as the dark of the eye.)
const FACE_FULL = 13.3, FACE_MID = 10.0;      // head widths in pixels at which the full face, and the middle one, are drawn
const EYES = {
  plain:  { at: 0, full: ["#i"], thin: ["#"] },                          // most grown men: small, the pupil toward the nose
  lash:   { at: 1, full: ["===", "#i."], thin: ["==", "#."] },           // a dark upper lid, swept outward
  big:    { at: 0, full: ["##", "ii"], thin: ["#", "i"] },               // a child's eyes: two pixels tall
  bright: { at: 0, full: ["#h", "ii"], thin: ["#", "i"] },               // a child's eyes with the light in them
  wide:   { at: 0, full: ["o#o"], thin: ["#o"] },                        // startled, or sharp
  heavy:  { at: 1, full: ["===", "#i.", "--."], thin: ["==", "#.", "-."] },   // heavy lids and a bag under each eye: bored, or tired
  girl:   { at: 1, full: ["==.", "#i="], thin: ["=.", "#="] },           // a young woman's: a soft lid, and a lash at the outer corner
  kohl:   { at: 0, full: ["o#="], thin: ["#="] },                        // lined with black paint, the line drawn out toward the temple
  squint: { at: 0, full: ["=#="], thin: ["=="] },                        // screwed up against the sun, or against bad eyesight
  shut:   { at: 0, full: ["=="], thin: ["="] },
  tight:  { at: 0, full: ["==-"], thin: ["=-"] },                        // squeezed shut, as a child shuts them: a crease at the corner
  deep:   { at: 1, full: ["---", "#i."], thin: ["--", "#."] },           // set deep under the brow
};

// ---------- a face's colours ----------
/** Two packed colours mixed: t = 0 is a, 1 is b. */
const mixPacked = (a, b, t) => { let o = 0; for (const sh of [0, 8, 16]) o |= Math.round(((a >>> sh) & 255) * (1 - t) + ((b >>> sh) & 255) * t) << sh; return ((255 << 24) | o) >>> 0; };
const INKS = new WeakMap();
/** The colours a face is drawn in, packed, worked out once for each face: the dark of the eye (face.eye), the iris
    (face.iris; with none, the dark), the white, the light in an eye, the lid line (face.lid), the lid's own shadow (the
    skin's shade), the brows, a blush (face.blush), freckles (face.freckle), the lips (face.lip, face.lips), dark glasses. */
function inksOf(face, skin) {
  let k = INKS.get(face);
  if (k && k.skin === skin) return k;
  const dark = pack(face.eye || "#2a1a12"), iris = face.iris ? pack(face.iris) : dark, white = pack(face.white || "#f6efe4");
  const glint = pack(face.glintEye || "#fffdf6"), line = pack(face.lid || "#5a3424"), lidShade = skin.tones[2];
  const brow = face.brows == null ? 0 : typeof face.brows === "string" ? pack(face.brows) : face.brows;
  const lip = pack(face.lip || "#8a4636"), lips = face.lips ? pack(face.lips) : 0;
  k = {
    skin, dark, iris, white, glint, line, lidShade, brow, small: dark,
    blush: face.blush ? pack(face.blush) : 0, freckle: face.freckle ? pack(face.freckle) : lidShade,
    lip, lips, inside: pack(face.inside || "#3a1612"),
    whiteShade: mixPacked(white, lidShade, 0.35), iris2: mixPacked(iris, white, 0.45), teeth: pack("#f6f0e6"), lipUp: lips ? mixPacked(lip, lips, 0.5) : lip,      // (for the faces of portraits)
    blushSoft: face.blush ? mixPacked(pack(face.blush), skin.tones[1], 0.45) : 0,
    shades: face.shades ? pack(face.shades) : 0,
    of: (ch) => (ch === "#" ? dark : ch === "i" ? iris : ch === "o" ? white : ch === "h" ? glint : ch === "=" ? line : ch === "-" ? lidShade : 0),
  };
  INKS.set(face, k);
  return k;
}

// ---------- a face at portrait size ----------
// A team portrait is drawn with several times the pixels of a figure in a scene, and its face is drawn feature by
// feature at that size, pixel by pixel, from the same face settings (people.js `face`, and `face.big` for what only
// shows at that size): the eyes with their lids, whites, iris, pupil and the light in them, lashes for women and girls,
// brows, the shadow under the nose, the lips, a blush, freckles. Hard pixels and the face's own few colours, as the
// small faces are: nothing is blended.
//   f: { sf, scr, see, face, ink, skin, eyeX, eyeY, mouthY, headPx, pose, sideways, noseTip, part }
function bigFace(f) {
  const { sf, scr, see, face, ink, eyeX, eyeY, mouthY, headPx, pose, sideways, noseTip, part } = f, big = face.big || {};
  const u = headPx / 2;                                                 // pixels in half the width of the head
  const put = (x, y, col) => { if (col) sf.dot(x, y, col, part); };
  const lash = ink.line, lidShade = ink.lidShade, deep = f.skin.tones[3];
  const eyeW = (big.eyeW ?? 0.40) * u, eyeH = eyeW * (big.eyeH ?? 0.46), irisR = eyeH * (big.iris ?? 0.62);
  const lashes = big.lashes ?? 0, lidT = Math.max(1, Math.round(eyeH * (big.lid ?? 0.16)));
  const tiny = u < 16;                                                  // (a portrait of about 60 pixels or less: room for an eye, its lid and a brow, and no more)
  for (const sd of [1, -1]) {
    const vis = see([sd * 0.25, 0, 0.97]);
    if (vis < 0.2) continue;
    const c = scr(sd * eyeX, eyeY, 0.80), w = eyeW * Math.min(1, 0.35 + vis * 0.65), h = eyeH;
    const out = c[0] >= f.mid ? 1 : -1;                                 // the side away from the nose, as seen
    const top = (q) => -Math.sqrt(Math.max(0, 1 - q * q)) * (1 + 0.10 * q * out),   // the upper lid: a little higher toward the outer corner
      bot = (q) => Math.sqrt(Math.max(0, 1 - q * q)) * 0.72;
    const x0 = Math.floor(c[0] - w / 2) - 3, x1 = Math.ceil(c[0] + w / 2) + 3, y0 = Math.floor(c[1] - h / 2) - 4, y1 = Math.ceil(c[1] + h / 2) + 2;
    const inside = (x, y) => { const q = (x + 0.5 - c[0]) / (w / 2), v = (y + 0.5 - c[1]) / (h / 2); return Math.abs(q) <= 1 && v >= top(q) && v <= bot(q); };
    if (pose.blink) {                                                    // shut: the line of the lashes, curving down
      for (let x = x0; x <= x1; x++) { const q = (x + 0.5 - c[0]) / (w / 2); if (Math.abs(q) > 1.02) continue; put(x, Math.round(c[1] + h * 0.10 + h * 0.18 * (1 - q * q) - 0.5), lash); }
      continue;
    }
    if (tiny) {
      // A small portrait's eye, pixel by pixel: the lid over it, the white at the corners, the iris in the middle with its
      // pupil toward the nose (so that the two meet the viewer's), and for women and girls a lash at the outer corner.
      const ew = Math.max(3, Math.round(w)), eh = h < 2.6 ? 2 : 3, irisW = ew <= 3 ? 1 : ew - 2, i0 = Math.floor((ew - irisW) / 2);
      const xIn = out > 0 ? Math.round(c[0] - ew / 2) : Math.round(c[0] + ew / 2) - 1, yT = Math.round(c[1] - eh / 2);
      const at = (i, j, col) => put(xIn + out * i, yT + j, col);
      const pupil = i0 + Math.floor((irisW - 1) / 2);
      for (let i = 0; i < ew; i++) {
        const corner = i === 0 || i === ew - 1;
        if (!corner || (lashes && i === ew - 1)) at(i, -1, lash);         // the lid, over the iris (and out to the outer corner, where there are lashes)
        for (let j = 0; j < eh; j++) {
          if (corner && j === eh - 1) continue;                           // (the lower corners are skin: the eye is almond-shaped)
          const iris = i >= i0 && i < i0 + irisW;
          at(i, j, !iris ? ink.white : j === 0 && i === pupil ? ink.dark : ink.iris);
        }
      }
      if (irisW >= 3) { const g = out > 0 ? pupil - 1 : pupil + 1; if (g >= i0 && g < i0 + irisW) at(g, 0, ink.glint); }      // the light in it, on the side toward the light
      if (lashes) at(ew, -1, lash);
    } else {
      // the iris looks at the viewer: in the middle of the eye, a little up under the lid
      const ix = c[0] + (big.gaze ?? 0) * out * w * 0.10, iy = c[1] + h * 0.06;
      const small = h < 3.4;                                                // (a small eye has no room for the lid's shadow: an iris and its pupil)
      for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
        if (!inside(x, y)) continue;
        const d = Math.hypot(x + 0.5 - ix, (y + 0.5 - iy) * 1.05);
        const underLid = !small && (!inside(x, y - lidT) || !inside(x, y - 1));
        if (!small && d <= irisR * 0.46) put(x, y, ink.dark);              // the pupil
        else if (d <= irisR) put(x, y, underLid ? ink.dark : ink.iris);    // the iris, darker under the lid
        else put(x, y, underLid ? ink.whiteShade : ink.white);            // the white, in the lid's shadow at the top
      }
      if (small) put(Math.round(ix - 0.5), Math.round(iy - 0.5), ink.dark);
      // the light in the eye, toward the light (up and to the left as we see it)
      const gx = Math.round(ix - irisR * 0.42 - 0.5), gy = Math.round(iy - irisR * 0.42 - 0.5);
      if (inside(gx, gy)) { put(gx, gy, ink.glint); if (irisR >= 3.2) put(gx + 1, gy, ink.glint); }
      if (irisR >= 3.6 && inside(gx + 2, gy + 2)) put(Math.round(ix + irisR * 0.30), Math.round(iy + irisR * 0.30), ink.iris2);   // a second, smaller light below
      // the upper lid: a dark line along the top of the eye, thicker toward the outer corner for women and girls
      for (let x = x0; x <= x1; x++) {
        let yTop = null;
        for (let y = y0; y <= y1; y++) if (inside(x, y)) { yTop = y; break; }
        if (yTop === null) continue;
        const q = (x + 0.5 - c[0]) / (w / 2) * out;                        // -1 at the inner corner, 1 at the outer
        put(x, yTop - 1, lash);
        if (lashes && q > 0.1) put(x, yTop - 2, lash);
        if (big.crease !== false && u >= 24) put(x, yTop - 2 - (lashes && q > 0.1 ? 1 : 0) - Math.max(1, Math.round(h * 0.18)), q > -0.6 && q < 0.8 ? lidShade : 0);      // the crease of the lid
        // the lower lid: a soft line under the outer part of the eye
        let yBot = null;
        for (let y = y1; y >= y0; y--) if (inside(x, y)) { yBot = y; break; }
        if (yBot !== null && q > -0.2 && q < 0.95) put(x, yBot + 1, lidShade);
      }
      // lashes at the outer corner, swept up and out
      if (lashes) {
        const ex = Math.round(c[0] + out * w / 2 - 0.5), ey = Math.round(c[1] - h * 0.30 - 0.5);
        put(ex, ey, lash); put(ex + out, ey - 1, lash);
        if (lashes > 1) { put(ex + out, ey, lash); put(ex + 2 * out, ey - 2, lash); }
      }
    }
    // the brow: an arch over the eye, a pixel or two thick, the colour of the hair
    if (ink.brow) {
      const arch = big.arch ?? 0.20, lift = (big.browUp ?? 0.55) * h + (pose.browsUp || 0) + (tiny ? 2 : 0), thick = tiny ? 1 : Math.max(1, Math.round(u * (big.browT ?? 0.07)));
      const bx0 = c[0] - out * w * 0.55, bx1 = c[0] + out * w * 0.62;
      const n = Math.round(Math.abs(bx1 - bx0));
      for (let i = 0; i <= n; i++) {
        const t = i / Math.max(1, n), x = Math.round(bx0 + (bx1 - bx0) * t - 0.5);
        const base = Math.min(c[1] - h * 0.55 - lift, c[1] - h / 2 - 2 - (lashes && !tiny ? 2 : 1));      // (and always a row of skin clear of the lid and the lashes)
        const y = base - arch * h * Math.sin(Math.PI * Math.min(1, t * 1.15)) + (big.browTilt ?? 0) * h * (t - 0.5);
        const tk = t > 0.85 ? Math.max(1, thick - 1) : thick;
        for (let k = 0; k < tk; k++) put(x, Math.round(y - 0.5) + k, ink.brow);
      }
    }
    // a blush on the cheek, under the outer part of the eye
    if (ink.blush && vis > 0.55) {
      const bc = scr(sd * (eyeX + 0.10), eyeY - 0.46, 0.80), rx = u * (big.blushR ?? 0.12), ry = rx * 0.55;
      for (let y = Math.floor(bc[1] - ry); y <= Math.ceil(bc[1] + ry); y++) for (let x = Math.floor(bc[0] - rx); x <= Math.ceil(bc[0] + rx); x++) {
        const r = ((x + 0.5 - bc[0]) / rx) ** 2 + ((y + 0.5 - bc[1]) / ry) ** 2;
        if (r <= 1) put(x, y, r < 0.35 ? ink.blush : ink.blushSoft);
      }
    }
  }
  // freckles: a few across the nose and the cheeks
  if (face.freckles) for (const [x, y] of [[-0.30, -0.30], [-0.18, -0.36], [0.20, -0.33], [0.32, -0.28], [-0.44, -0.40], [0.44, -0.40]]) {
    if (see([x, 0, 0.95]) < 0.3) continue;
    const q = scr(x, eyeY + y, 0.92);
    put(Math.round(q[0] - 0.5), Math.round(q[1] - 0.5), ink.freckle);
  }
  // the nose: the shadow under its tip, and the nostrils
  if (see([0, 0, 1]) > 0.35) {
    const q = noseTip, w = Math.max(2, Math.round(u * 0.20)), x = Math.round(q[0] - 0.5), y = Math.round(q[1] - 0.5) + Math.max(1, Math.round(u * 0.04));
    for (let i = -Math.floor(w / 2); i <= Math.ceil(w / 2); i++) put(x + i, y, lidShade);
    if (u >= 9) { put(x - Math.ceil(w / 2), y - 1, deep); put(x + Math.ceil(w / 2), y - 1, deep); }
  }
  // the mouth: the line between the lips, lifted at the corners for a smile, and the lower lip under it
  if (face.mouth !== false && see([0, 0, 1]) > 0.10) {
    const mq = scr(0, mouthY, 0.95), mw = Math.max(2, (face.mouthW ?? 0.22) * u * 2 * (big.mouthW ?? 1.0)), smile = (face.smile || 0) * (big.smile ?? 1) * Math.max(1, u * 0.06), open = pose.mouth || 0;
    const xa = Math.round(mq[0] - mw / 2), xb = Math.round(mq[0] + mw / 2) - 1, yc = Math.round(mq[1] - 0.5);
    const lipDark = ink.lip, lipLow = ink.lips || ink.lip;
    for (let x = xa; x <= xb; x++) {
      const t = (x + 0.5 - mq[0]) / (mw / 2), lift = Math.round(smile * t * t);
      if (open) { for (let k = 0; k < open + 1; k++) put(x, yc + k - lift, Math.abs(t) > 0.85 ? lipDark : ink.inside); if (open > 1 && Math.abs(t) < 0.5) put(x, yc - lift, ink.teeth); }
      else put(x, yc - lift, lipDark);
      // the lower lip: a little narrower, in the lip's lighter colour, and a shadow under it (on a small face, only the lip)
      if (Math.abs(t) < 0.70) {
        const yl = yc - lift + (open ? open + 1 : 1);
        if (ink.lips) put(x, yl, lipLow);
        if (Math.abs(t) < 0.45 && u >= 14) put(x, yl + (ink.lips ? 1 : 0), lidShade);
      }
    }
    if (ink.lips && !open && u >= 14) for (let x = xa + 1; x <= xb - 1; x++) { const t = (x + 0.5 - mq[0]) / (mw / 2); if (Math.abs(t) < 0.55) put(x, yc - Math.round(smile * t * t) - 1, ink.lipUp); }   // the upper lip
  }
}


/**
 * Draw a character.
 * spec: who they are (see people.js). pose: how they are standing. yawDeg: the way they face.
 * size: their height in art pixels.
 * Returns a Surface whose anchor (ox, oy) is the point on the ground between the feet.
 * opt.seat: draw only the seat that is drawn with this person (a stool, a lawn chair) and its shadow: see drawSeat.
 * opt.window: [x, y, w, h], draw only that part of the picture, measured from the anchor (x right, y down): a portrait.
 * opt.portrait: the face is drawn feature by feature at whatever size the head is (bigFace), not in the small patterns.
 */
export function drawFigure(spec, pose, yawDeg, size, opt = null) {
  const d = spec.dim, S = size;
  const only = opt && opt.seat ? new Set(spec.seatParts || [EXTRA3, EXTRA2]) : null;      // (the parts a seat is drawn as)
  // (spec.span and spec.tall make room for someone wide or tall with what they carry; spec.under, for something lying
  //  on the ground nearer to us than their feet, which is drawn below them)
  const below = Math.ceil(S * (spec.under || 0));
  const W = (Math.ceil(S * (spec.span || 1.05)) + 14) & ~1, H = Math.ceil(S * (spec.tall || 1.2)) + 12 + below;
  const win = opt && opt.window, ox = win ? -win[0] : W / 2, oy = win ? -win[1] : H - 6 - below;
  const sf = new Surface(win ? win[2] : W, win ? win[3] : H, ox, oy);
  const th = yawDeg * DEG, c = Math.cos(th), s = Math.sin(th), TILT = 0.22;
  // character space to picture space. The camera looks slightly down, so nearer things sit lower.
  const P = (v) => { const dp = (v[0] * s + v[2] * c) * S; return [ox + (-v[0] * c + v[2] * s) * S, oy - v[1] * S + dp * TILT, dp]; };
  const R = (r) => Math.max(0.85, r * S);
  const J = skeleton(d, pose);
  const fine = S >= 84, coarse = S < 52;

  const limb = (a, b, ra, rb, mat, o) => {
    if (only && !only.has(o && o.part)) return;
    const A = P(a), B = P(b);
    // hem (far end) and cuff (near end): the cloth stops in a straight edge, unless the limb points so nearly at the viewer that its end is what shows
    if (o && (o.hem || o.cuff)) { const long = Math.hypot(B[0] - A[0], B[1] - A[1]), min = o.hemMin ?? 1.4; o = { ...o, squareEnd: !!o.hem && long > R(rb) * min, squareStart: !!o.cuff && long > R(ra) * min }; }
    sf.limb(A[0], A[1], A[2], B[0], B[1], B[2], R(ra), R(rb), mat, o);
  };
  // r3 = [half width, half height, half depth] in the part's own frame, which is turned by `psi` from the body
  const ball = (ctr, r3, mat, o = {}, psi = 0) => {
    if (only && !only.has(o.part)) return;
    const C = P(ctr), a = th + psi, ca = Math.cos(a), sa = Math.sin(a);
    sf.ball(C[0], C[1], C[2], R(Math.hypot(r3[0] * ca, r3[2] * sa)), R(r3[1]), R(Math.hypot(r3[0] * sa, r3[2] * ca)), mat, o);
  };
  // From a point on a ball as seen (ux right, uy down, uz toward the viewer) back to the part's own directions.
  const own = (ux, uy, uz, psi) => { const a = th + psi, ca = Math.cos(a), sa = Math.sin(a); return [-ux * ca + uz * sa, -uy, ux * sa + uz * ca]; };
  // A shape that is wider than it is deep, [half width, half depth], looks narrower or wider as the figure turns.
  const widthAt = (r2, turned) => Math.hypot(r2[0] * Math.cos(th + turned), r2[1] * Math.sin(th + turned));
  const depthAt = (r2, turned) => Math.hypot(r2[0] * Math.sin(th + turned), r2[1] * Math.cos(th + turned));
  // How far round a body a point is, from how far across the shape it is seen: 0 is the middle of the front,
  // a quarter turn is the character's own right side. Patterns and folds use it, so that they turn with the body.
  const roundAt = (across, turned) => { const u = clamp1(across), o = own(u, 0, Math.sqrt(1 - u * u), turned); return Math.atan2(o[0], o[2]); };
  /** A line drawn on the cloth between two points in space, seen only where that part is on top. `facing` (optional)
      is the way that bit of cloth faces: the line is left out when it is on the far side of the figure. */
  const fold = (a, b, part, facing = null, by = 1) => {
    if (only && !only.has(part)) return;
    if (facing && facing[0] * s + facing[2] * c < 0.12) return;
    const A = P(a), B = P(b);
    sf.stroke(A[0], A[1], B[0], B[1], by, part);
  };

  // The arm and the leg on the far side of the body are drawn a tone down, as a draughtsman would:
  // it sets them behind the near ones without any modelling.
  const gapR = P(J.R.hip)[2] - P(J.L.hip)[2], farK = Math.abs(gapR) > S * 0.03 ? (gapR < 0 ? "R" : "L") : null;
  const dimmed = new Map();
  const far = (k, mat) => {
    if (k !== farK || !mat) return mat;
    if (!dimmed.has(mat)) dimmed.set(mat, { ...mat, lift: -2 });
    return dimmed.get(mat);
  };

  const skin = spec.skin, top = spec.top || {}, bottom = spec.bottom || {}, socks = spec.socks, shoes = spec.shoes || {};
  const hair = spec.hair || {}, face = spec.face || {}, apron = spec.apron || null;
  const breath = pose.breath || 0;
  const tw = J.twist, ht = J.hipTwist, topMat = top.mat || skin, psi = tw * 0.6;
  const cloth = S * 0.014;                                              // cloth sits just outside whatever it covers
  const under = S * 0.07;                                               // how far a body may bulge under loose cloth and still be covered by it

  // ----- shadow on the ground -----
  // (Someone sitting on a solid thing that the scene has painted, a step or a kerb or a stone bench, has no ground
  //  under the seat to throw a shadow on: theirs lies under their feet. `sit.solid` says so.)
  if (only) sf.oval(ox, oy - 0.5, S * (spec.seatShadow ?? 0.11), Math.max(1.5, S * 0.026), -1e8, SHADOW);     // (a seat by itself: its own shadow)
  else if (pose.seated && spec.sit && spec.sit.solid) {
    const f = P(mix(J.R.ball, J.L.ball, 0.5)), wide = Math.abs(P(J.R.ball)[0] - P(J.L.ball)[0]) / 2;
    sf.oval(f[0], f[1] + 0.5, wide + S * 0.075, Math.max(1.5, S * 0.026), -1e8, SHADOW);
  } else sf.oval(ox, oy - 0.5, S * (spec.shadow || 0.18), Math.max(1.5, S * 0.032), -1e8, SHADOW);

  // ----- legs -----
  const trousers = bottom.kind === "trousers";
  for (const k of ["R", "L"]) {
    const L = J[k], part = LEG[k];
    const legMat = far(k, trousers ? bottom.mat : spec.tights || skin);
    const [rT, rK, rA] = d.legR, rC = d.calf ?? rK * 1.04;
    if (trousers) {
      const ease = bottom.ease ?? 0.007;                                // cloth: wider than the leg inside it, and straighter
      limb(L.hip, L.knee, rT + ease * 0.4, rK + ease, legMat, { part });
      limb(L.knee, add(L.ankle, [0, -0.004, 0]), rK + ease, rA + ease * 1.7, legMat, { part, hem: true });
    } else {
      const calf = add(mix(L.knee, L.ankle, 0.30), mul(L.calfBack, 0.011));     // the calf swells behind the shin
      limb(L.hip, L.knee, rT, rK, legMat, { part });
      limb(L.knee, calf, rK, rC, legMat, { part });
      limb(calf, L.ankle, rC, rA, legMat, { part });
      // a bare knee is drawn: a short line under the kneecap, where the leg faces us
      const front = mul(L.calfBack, -1);
      if (fine && !spec.tights && front[0] * s + front[2] * c > 0.35) {
        const below = mix(L.knee, L.ankle, 0.10), side = turn([1, 0, 0], L.footYaw);
        fold(add(add(below, mul(front, rK * 0.9)), mul(side, -rK * 0.34)), add(add(below, mul(front, rK * 0.9)), mul(side, rK * 0.20)), part);
      }
    }
    if (bottom.kind === "shorts") {
      const len = bottom.len ?? 0.7;
      limb(L.hip, mix(L.hip, L.knee, len), rT + 0.012, lerp(rT, rK, len) + 0.016, far(k, bottom.mat), { part: SHORTS[k], hem: true });
    }
    const sockThick = socks ? (socks.thick ?? 0.004) : 0;
    if (socks) {
      // a sock follows the leg's own line, calf and all
      const from = socks.from ?? 0.55, stripes = socks.stripes, sm = far(k, socks.mat);
      const calfAt = add(mix(L.knee, L.ankle, 0.30), mul(L.calfBack, trousers ? 0 : 0.011));
      const top = from < 0.30 ? mix(L.knee, calfAt, from / 0.30) : mix(calfAt, L.ankle, (from - 0.30) / 0.70);
      const rTop = (from < 0.30 ? lerp(rK, rC, from / 0.30) : lerp(rC, rA, (from - 0.30) / 0.70)) + sockThick;
      const band = stripes && fine ? (t) => (t > 0.10 && t < 0.24 ? stripes[0] : t > 0.34 && t < 0.48 ? stripes[1] : undefined) : null;
      if (from < 0.30) { limb(top, calfAt, rTop, rC + sockThick, sm, { part, cuff: true }); limb(calfAt, L.ankle, rC + sockThick, rA + sockThick + 0.001, sm, { part }); }
      else limb(top, L.ankle, rTop, rA + sockThick + 0.001, sm, { part, cuff: true, fn: band });
    }
    // ----- feet: a heel, a sloping instep and a broad front, flat on the sole -----
    const fpart = FOOT[k], kind = shoes.kind || "shoes", pumps = kind === "pumps", bareFoot = kind === "bare" || kind === "sandals";
    const footMat = far(k, kind === "bare" ? skin : kind === "sandals" ? (socks ? socks.mat : skin) : shoes.mat);
    const fr = d.footR, lift = (pt, hgt) => add(pt, mul(L.nrm, hgt));
    const rH = fr * 0.90, rB = fr * (bareFoot ? 0.64 : 0.72), rTip = fr * (bareFoot ? 0.54 : 0.60);
    const heelC = lift(add(L.heel, mul(L.along, rH)), rH), ballC = lift(L.ball, rB), toeC = lift(add(L.toe, mul(L.toeDir, -rTip)), rTip);
    if (shoes.sole) {
      const sink = -0.006;
      limb(add(heelC, mul(L.nrm, sink)), add(ballC, mul(L.nrm, sink)), rH, rB, shoes.sole, { part: fpart, bias: -0.8 });
      limb(add(ballC, mul(L.nrm, sink)), add(toeC, mul(L.nrm, sink)), rB, rTip, shoes.sole, { part: fpart, bias: -0.8 });
    }
    const strap = kind === "sandals" ? shoes.mat : null;
    limb(heelC, ballC, rH, rB, footMat, {
      part: fpart, flatten: 1.3,
      fn: strap ? (t) => (t > 0.62 && t < 0.86 ? strap : undefined)                                 // the strap over the instep
        : pumps ? (t) => (t > 0.30 && t < 0.80 ? legMat : undefined)                                // a court shoe: the top of the foot shows
        : shoes.stripe && fine ? (t) => (t > 0.42 && t < 0.60 ? shoes.stripe : undefined) : null,
    });
    limb(ballC, toeC, rB, rTip, footMat, { part: fpart, flatten: 1.3 });
    ball(lift(mix(L.ball, L.toe, 0.10), rB * 1.0), [fr * (bareFoot ? 1.30 : 1.36), rB * 1.0, fr * 1.7], footMat, { part: fpart, flatten: 1.3 }, L.footYaw);     // the front of the foot is broad
    const instep = pumps || strap ? legMat : footMat;
    limb(L.ankle, lift(mix(L.heel, L.ball, 0.72), rB * 0.95), rA + sockThick, rB * 0.80, pumps ? legMat : strap ? far(k, socks ? socks.mat : skin) : instep, { part: fpart });
    limb(L.ankle, mix(L.ankle, heelC, 0.85), rA + sockThick, rH * 0.95, pumps ? legMat : footMat, { part: fpart });
    if (strap && fine) limb(add(L.ankle, mul(L.nrm, -0.004)), add(L.ankle, mul(L.nrm, -0.010)), rA + sockThick + 0.003, rA + sockThick + 0.004, strap, { part: fpart, squareStart: true, squareEnd: true });   // and one round the ankle
    if (shoes.shaft) limb(mix(L.knee, L.ankle, 1 - shoes.shaft), L.ankle, lerp(rC, rA, 1 - shoes.shaft) + 0.008, rA + 0.009, footMat, { part: fpart, cuff: true });     // a boot comes up the shin
  }

  // ----- pelvis, and a skirt if there is one -----
  const wraps = bottom.kind === "skirt" || bottom.kind === "kilt";
  // (sitting, whatever is sat on presses it flat underneath)
  const seatCut = pose.seated ? 0.62 + 0.012 / d.pelvisR[1] : 9;
  ball(add(J.hipC, [0, 0.012, 0]), d.pelvisR, wraps ? bottom.under || bottom.mat : bottom.mat || skin, { part: PELVIS, fn: pose.seated ? (ux, uy) => (uy > seatCut ? null : undefined) : null }, ht);
  if (bottom.rise) {                                                    // a high waist: the cloth comes up over the stomach, and the shirt is tucked into it
    const rw = widthAt(d.trunkLow, psi) + 0.007;
    limb(J.spine(d.hipY + bottom.rise), J.spine(d.hipY + 0.026), rw, rw, bottom.mat, { part: PELVIS, depth: depthAt(d.trunkLow, psi) / rw, bias: S * 0.022, squareStart: true, squareEnd: true });
  }
  // An apron is a panel of other cloth over the front of whatever is worn: it is drawn as part of the
  // cloth it lies on, so it hangs and swings exactly as that does.
  const apronOn = (round, low) => apron && !coarse && Math.abs(round) < (apron.half ?? 1.0) && low <= (apron.len ?? 1.0) ? apron.mat : undefined;
  let skirtAt = null;                                                   // for clothes that hang over the skirt: a point on it, given how far down and how far round
  if (wraps) {
    const len = bottom.len ?? 0.9;                                      // 1 is the knee, 2 the ankle
    const down = (L, u) => (u <= 1 ? mix(L.hip, L.knee, u) : mix(L.knee, L.ankle, Math.min(1, u - 1)));
    const legAt = (u) => (u <= 1 ? lerp(d.legR[0], d.legR[1], u) : lerp(d.legR[1], d.legR[2], Math.min(1, u - 1)));
    const flare = bottom.flare ?? 1.25, slung = bottom.low ?? (bottom.kind === "kilt" ? 0.030 : 0);      // a kilt is tied below the waist, on the hips
    const hip2 = [d.pelvisR[0] + 0.008, d.pelvisR[2] + 0.006], sk = slung / Math.max(0.01, d.waistY - d.hipY);
    const waist2 = [lerp(d.trunkLow[0], hip2[0], sk * 0.8), lerp(d.trunkLow[1], hip2[1], sk * 0.8)];
    const top = { at: add(J.spine(d.waistY - 0.004 - slung), J.torso([0, 0, (d.bellyFwd || 0) * 0.6])), r2: waist2, turned: psi, u: -0.45 }, seat = { at: add(J.hipC, [0, 0.004, 0]), r2: hip2, turned: ht, u: 0 };
    const loose = { [PELVIS]: under, [LEG.R]: under, [LEG.L]: under, [SHORTS.R]: under, [SHORTS.L]: under };
    const cone = (A, B, o) => { const ra = widthAt(A.r2, A.turned), rb = widthAt(B.r2, B.turned); limb(A.at, B.at, ra, rb, bottom.mat, { part: SKIRT, depth: (depthAt(A.r2, A.turned) + depthAt(B.r2, B.turned)) / (ra + rb), over: loose, bias: S * 0.006, ...o }); };
    // bands of color woven across the cloth: [from, to, material], measured down the legs as `len` is (sitBands, if given,
    // are the ones that show sitting down: a band that runs round the shins makes no sense over crossed legs)
    const bandAt = bottom.bands ? (u) => { for (const [a, b, m] of bottom.bands) if (u >= a && u < b) return m; return undefined; } : null;
    if (pose.seated || pose.lap) {
      // Sitting, a skirt lies along the thighs and is stretched between them: a lap. An apron covers it.
      // (`lap`: someone getting up, whose thighs are still far from upright.)
      const lap = apron ? apron.mat : bottom.mat, ease = 0.013, end = Math.min(1, len);
      const sitBand = bottom.sitBands ? (u) => { for (const [a, b, m] of bottom.sitBands) if (u >= a && u < b) return m; return undefined; } : bandAt;
      const woven = sitBand && !apron ? (u0, u1) => (t) => sitBand(lerp(u0, u1, t)) : () => null;
      cone(top, seat, { squareEnd: true, fn: woven(top.u, 0) });
      for (const k of ["R", "L"]) {
        const L = J[k];
        limb(L.hip, down(L, end), legAt(0) + ease, legAt(end) + ease, lap, { part: SKIRT, hem: len <= 1, fn: woven(0, end) });
        if (len > 1) limb(L.knee, down(L, len), legAt(1) + ease, legAt(len) + ease, lap, { part: SKIRT, hem: true, fn: woven(1, len) });
      }
      // Seen from in front, a long robe would be one flat sheet from waist to feet. A draughtsman shows the knees:
      // the lap lies flat and light, a line runs from knee to knee where the cloth turns over them, and below
      // that it hangs in shade between the two shins, which stand a little forward of it.
      const kr = P(J.R.knee), kl = P(J.L.knee), toward = (kr[2] + kl[2]) / 2 - P(J.hipC)[2];        // how far the knees come toward us
      const kneesOut = len > 1.05 && toward > S * 0.08;
      for (let u = 0.2; u < len + 0.07; u += 0.14) {                    // the cloth between the legs, all the way down
        const at = Math.min(u, len), hangs = kneesOut && at > 1.04, r = legAt(at) + ease * 0.7, m = (sitBand && !apron && sitBand(at)) || lap;
        limb(down(J.R, at), down(J.L, at), r, r, m, hangs ? { part: SKIRT, tone: 2, depth: 0.35 } : { part: SKIRT, tone: 1 });
      }
      if (kneesOut && !coarse && !only) {
        const drop = R(legAt(1) + ease) * 0.55, sag = Math.abs(kr[0] - kl[0]) * 0.10, mx = (kr[0] + kl[0]) / 2, my = (kr[1] + kl[1]) / 2 + drop + sag;
        sf.stroke(kr[0], kr[1] + drop, mx, my, 1, SKIRT); sf.stroke(mx, my, kl[0], kl[1] + drop, 1, SKIRT);
      }
      if (len > 1.15 && !(pose.rising > 0)) for (const k of ["R", "L"]) {     // a long robe also falls from under the thighs to its hem: from the side it is one fall of cloth, not two trouser legs (not while getting up)
        const L = J[k], hemY = down(L, len)[1];
        for (const u of [0.20, 0.40, 0.60, 0.80, 1.0]) { const a = down(L, u), r = (legAt(u) + ease) * 0.86; if (a[1] - hemY > 0.03) limb(a, [a[0], hemY, a[2]], r, r, bottom.mat, { part: SKIRT, tone: 1, hem: true }); }
      }
    } else {
      // Standing, a skirt is one cone round both legs, from the waist over the hips to the hem. The hem follows
      // the legs: when they stride apart it widens, and when the knees bend it swings forward with them.
      // The cloth at a given distance down the legs is an oval big enough to hold both of them however they stand.
      const ringAt = (u) => {
        const pR = down(J.R, u), pL = down(J.L, u), apart = turn([pR[0] - pL[0], 0, pR[2] - pL[2]], -ht), legR2 = legAt(u) + 0.015;
        const k = 1 + (flare - 1) * Math.min(1, u / len);
        return { at: mix(pR, pL, 0.5), r2: [Math.max(hip2[0] * k, Math.abs(apart[0]) / 2 + legR2), Math.max(hip2[1] * k, Math.abs(apart[2]) / 2 + legR2)], turned: ht, u };
      };
      const rings = [top, seat];
      if (len > 1.3) rings.push(ringAt(1));
      rings.push(ringAt(len));
      const pleats = bottom.pleats && !coarse ? shifted(bottom.mat, 1) : null;
      const stripe = bottom.stripe && !coarse ? bottom.stripe : null;
      for (let i = 0; i + 1 < rings.length; i++) {
        const A = rings[i], B = rings[i + 1], last = i === rings.length - 2;
        const fn = pleats || stripe || apron || bandAt ? (t, nx) => {
          const round = roundAt(nx, ht), low = lerp(A.u, B.u, t);
          const ap = apronOn(round, low);
          if (ap) return ap;
          if (stripe) for (const at of stripe.at) if (Math.abs(wrap(round - at)) < stripe.half) return stripe.mat;
          const band = bandAt && bandAt(low);
          if (band) return band;
          return pleats && Math.floor((Math.asin(clamp1(nx)) / Math.PI + 0.5) * bottom.pleats + 0.5) % 2 ? pleats : undefined;
        } : null;
        cone(A, B, { squareEnd: i > 0, fn });                           // each length ends in a straight edge (the next one's rounded top fills the join), and the last is the hem
      }
      skirtAt = (u, round, out = 0) => {
        let i = 0; while (i + 2 < rings.length && rings[i + 1].u < u) i++;
        const A = rings[i], B = rings[i + 1], t = Math.max(0, Math.min(1, (u - A.u) / (B.u - A.u || 1)));
        const at = mix(A.at, B.at, t), r2 = [lerp(A.r2[0], B.r2[0], t) + out, lerp(A.r2[1], B.r2[1], t) + out];
        return add(at, turn([Math.sin(round) * r2[0], 0, Math.cos(round) * r2[1]], ht));
      };
      // folds: lines drawn down the cloth, each fixed to its own place round the body
      if (bottom.folds && fine) for (const f of bottom.folds) {
        const [round, from = 0.25, to = len, slant = 0] = Array.isArray(f) ? f : [f];
        const facing = turn([Math.sin(round), 0, Math.cos(round)], ht);
        const steps = to > 1.2 && from < 1 ? [from, 1, to] : [from, to];
        for (let i = 0; i + 1 < steps.length; i++) fold(skirtAt(steps[i], round + slant * (steps[i] - from)), skirtAt(steps[i + 1], round + slant * (steps[i + 1] - from)), SKIRT, facing);
      }
      // a wrapped kilt: the edge of the cloth runs down the front from one hip toward the other knee
      if (bottom.wrap && fine) {
        const [r0, r1] = Array.isArray(bottom.wrap) ? bottom.wrap : [0.60, -0.25];
        for (let i = 0; i < 4; i++) { const u0 = -0.3 + ((len + 0.3) * i) / 4, u1 = -0.3 + ((len + 0.3) * (i + 1)) / 4, a0 = lerp(r0, r1, (i / 4) ** 0.7), a1 = lerp(r0, r1, ((i + 1) / 4) ** 0.7); fold(skirtAt(u0, a0), skirtAt(u1, a1), SKIRT, turn([Math.sin(a0), 0, Math.cos(a0)], ht)); }
      }
    }
    if (bottom.sash) {                                                  // a band tied round the top of it
      const ra = widthAt(top.r2, top.turned) + 0.005;
      limb(add(top.at, [0, 0.008, 0]), add(top.at, [0, -0.014, 0]), ra, ra + 0.002, bottom.sash, { part: BELT, depth: depthAt(top.r2, top.turned) / ra, bias: cloth * 1.8, squareStart: true, squareEnd: true });
    }
  }

  // ----- trunk -----
  // The trunk is wider than it is deep, so how wide it looks depends on the way the figure is turned.
  const wide = (r2) => widthAt(r2, psi), deep = (r2) => depthAt(r2, psi);
  // Chest to waist, then waist to hem: two lengths, so that a stomach can stick out at the waist and tuck back in below.
  const lowR = d.trunkHem || [d.trunkLow[0] * 0.97, d.trunkLow[1] * 0.90];
  const rT = wide(d.trunkTop) + 0.003 * breath, rW = wide(d.trunkLow), rB = wide(lowR);
  const hemY = top.hem ? d.hipY - (top.hem === true ? 0.042 : top.hem) : d.hipY + 0.05;
  const chestY = d.shoulderY - rT * 0.80;
  const tTop = J.spine(chestY);
  const tMid = add(J.spine(d.waistY), J.torso([0, 0, d.bellyFwd || 0]));
  const tLow = add(J.spine(hemY), J.torso([0, 0, (d.bellyFwd || 0) * 0.55]));
  /** A point on the surface of the trunk: `high` up the spine, `round` the body (0 is the middle of the front), `out` from the cloth. */
  const trunkAt = (high, round, out = 0) => {
    const t = high >= d.waistY ? (high - d.waistY) / (chestY - d.waistY) : (high - d.waistY) / (d.waistY - hemY);
    const r2 = t >= 0 ? [lerp(d.trunkLow[0], d.trunkTop[0], Math.min(1, t)), lerp(d.trunkLow[1], d.trunkTop[1], Math.min(1, t))] : [lerp(d.trunkLow[0], lowR[0], Math.min(1, -t)), lerp(d.trunkLow[1], lowR[1], Math.min(1, -t))];
    const fwd = (d.bellyFwd || 0) * (t >= 0 ? 1 - Math.min(1, t) : 1 + 0.45 * Math.max(-1, t));
    return add(J.spine(high), J.torso([Math.sin(round) * (r2[0] + out), 0, Math.cos(round) * (r2[1] + out) + fwd]));
  };
  const trunkFacing = (round) => turn(J.torso([Math.sin(round), 0, Math.cos(round)]), 0);
  // a patterned shirt: the pattern is fixed to the cloth, so it turns with the body
  const printed = top.pattern && !coarse;
  const around = (nx) => roundAt(nx, psi) * 0.115;
  const TA = P(tTop), TB = P(tLow), tdx = TB[0] - TA[0], tdy = TB[1] - TA[1], tl2 = tdx * tdx + tdy * tdy || 1, ra = R(rT), rb = R(rB);
  const high = (y) => (TA[1] - y) / S;                                 // height measured down the cloth itself, so the print moves with the body
  const across = (x, y) => {                                           // how far across the trunk a pixel is, also out on the shoulders, which are not part of the trunk's own shape
    let k = ((x + 0.5 - TA[0]) * tdx + (y + 0.5 - TA[1]) * tdy) / tl2; k = k < 0 ? 0 : k > 1 ? 1 : k;
    return (x + 0.5 - TA[0] - tdx * k) / (ra + (rb - ra) * k);
  };
  // overalls: a bib on the chest and a strap over each shoulder, drawn on the shirt so that they turn with the body
  const bib = bottom.bib && !coarse ? bottom.bib : null;
  const bibAt = bib ? (u, y) => {
    const a = Math.abs(roundAt(u, psi));                                                     // how far round the body from the middle of the chest
    const below = rT * 0.80 - high(y), half = bib.half ?? 0.62, strap = bib.strap ?? 0.30;   // how far below the shoulder line
    if (a < half) return below > (bib.top ?? 0.07) || a > half - strap ? bottom.mat : undefined;
    const back = Math.PI - a, low = bib.back ?? 0.62;
    return back < low && back > low - strap ? bottom.mat : undefined;                        // a strap down each side of the back
  } : null;
  const stripe = top.stripe && !coarse ? top.stripe : null;             // stripes down the cloth, each at its own place round the body
  const tBands = top.bands || null;                                     // bands woven across it: [from, to, material], measured down from the line of the shoulders
  const bibTop = apron && apron.bib ? d.shoulderY - apron.bib : null;   // an apron with a bib comes up the chest
  const dressed = printed || bib || stripe || bibTop != null || !!tBands;
  const clothAt = dressed ? (u, x, y) => {
    if (u < -1 || u > 1) return undefined;                              // plain cloth out past the trunk's own width
    const round = roundAt(u, psi);
    if (bibTop != null && !coarse && Math.abs(round) < (apron.half ?? 1.0) * 0.72 && TA[1] + (chestY - bibTop) * S < y) return apron.mat;
    if (stripe) for (const at of stripe.at) if (Math.abs(wrap(round - at)) < stripe.half) return stripe.mat;
    if (bib) { const m = bibAt(u, y); if (m) return m; }
    if (tBands) { const below = rT * 0.80 - high(y); for (const [a, b, m] of tBands) if (below >= a && below < b) return m; }
    return printed ? flowers(round * 0.115, high(y), top.pattern) : undefined;
  } : null;
  const onCloth = clothAt ? (t, nx, ny, x, y) => clothAt(clamp1(nx), x, y) : null;
  const offTrunk = clothAt ? (t, nx, ny, x, y) => clothAt(across(x, y), x, y) : null;
  // an untucked shirt hangs over the hips, even where they stick out further than the chest does
  const loose = top.hem && !pose.seated ? { [PELVIS]: under, [SHORTS.R]: under, [SHORTS.L]: under, [LEG.R]: under, [LEG.L]: under, [SKIRT]: under } : null;
  const dT = deep(d.trunkTop), dW = deep(d.trunkLow), dB = deep(lowR);
  const cover = top.mat ? cloth : 0;                                    // (bare skin is not cloth: whatever is tied round the waist lies over it)
  limb(tTop, tMid, rT, rW, topMat, { part: TORSO, depth: (dT + dW) / (rT + rW), bias: cover, fn: onCloth });
  limb(tMid, tLow, rW, rB, topMat, { part: TORSO, depth: (dW + dB) / (rW + rB), bias: cover, squareEnd: !!top.hem || !!bottom.rise, over: loose, fn: onCloth });   // an untucked shirt ends in a straight hem
  if (d.paunch) {                                                       // a real stomach: it hangs out over whatever is tied round the waist
    const [pw, ph, pd, py = 0] = d.paunch;
    ball(add(J.spine(d.waistY + py), J.torso([0, 0, (d.bellyFwd || 0) + d.trunkLow[1] - pd * 0.72])), [pw, ph, pd], topMat, { part: TORSO, bias: cloth, fn: onCloth && ((ux, uy, uz, x, y) => offTrunk(0, 0, 0, x, y)) }, psi);
  }
  if (d.bust) {                                                         // [how far out, how big, how far below the shoulders]
    const [out, big, low = 0.118] = d.bust;
    for (const sd of [1, -1]) ball(add(J.spine(d.shoulderY - low), J.torso([sd * d.trunkTop[0] * 0.44, 0, d.trunkTop[1] - big * 0.55 + out])), [big * 1.05, big, big], topMat, { part: TORSO, bias: cloth, fn: onCloth && ((ux, uy, uz, x, y) => offTrunk(0, 0, 0, x, y)) }, psi);
  }
  if (top.blouse) {                                                     // cloth pulled up through a belt hangs over it in a soft roll
    const r = rW + top.blouse;
    limb(add(tMid, J.torso([0, 0.060, 0])), add(tMid, J.torso([0, 0.022, 0])), lerp(rW, rT, 0.26) + top.blouse * 0.3, r, topMat, { part: TORSO, depth: dW / rW, bias: cloth, fn: onCloth, squareEnd: true });
  }
  if (top.belt) { const low = top.beltLow || 0; limb(add(tMid, J.torso([0, 0.012 - low, 0])), add(tMid, J.torso([0, -0.012 - low, 0])), rW + 0.004, rW + 0.004, top.belt, { part: BELT, depth: dW / rW, bias: cloth * 1.6, squareEnd: true, squareStart: true }); }
  // shoulders: one slope from the side of the neck out over the top of each arm
  const capR = d.armR[0] + (top.mat ? 0.008 : 0.003);
  for (const k of ["R", "L"]) {
    const sd = k === "R" ? 1 : -1;
    limb(add(J.sh, J.torso([sd * 0.034, 0.002, -0.004])), add(J[k].shoulder, J.torso([-sd * 0.008, capR - 0.022, 0])), 0.020, 0.022, topMat, { part: TORSO, bias: cover, fn: offTrunk });
    ball(J[k].shoulder, [capR, capR, capR], topMat, { part: TORSO, bias: cover, fn: offTrunk && ((ux, uy, uz, x, y) => offTrunk(0, 0, 0, x, y)) });
  }
  // Cloth is drawn too: a fold from each armpit toward the waist, and small gathers where a belt pulls it in.
  if (top.mat && fine && top.folds !== false && !printed) {
    for (const sd of [1, -1]) fold(trunkAt(d.shoulderY - 0.110, sd * 1.05, 0.004), trunkAt(d.waistY + 0.040, sd * 0.62, 0.004), TORSO, trunkFacing(sd * 0.85));
    if (top.belt) { const low = top.beltLow || 0; for (const round of [-0.5, 0.25, 0.75, 2.5, -2.6]) { fold(trunkAt(d.waistY - low + 0.040, round, 0.006), trunkAt(d.waistY - low + 0.016, round * 1.04, 0.006), TORSO, trunkFacing(round)); } }
  }
  // a bare chest is drawn, not left blank: the line under each breast muscle, the middle of the stomach, the navel
  if (!top.mat && fine && !spec.plain) {
    const build = spec.build || "lean", front = trunkFacing(0);
    for (const sd of [1, -1]) {
      const lowC = d.shoulderY - (build === "fat" ? 0.128 : 0.112);
      fold(trunkAt(lowC + 0.004, sd * 0.16), trunkAt(lowC - 0.004, sd * 0.52), TORSO, trunkFacing(sd * 0.34));
      fold(trunkAt(lowC - 0.004, sd * 0.52), trunkAt(lowC + 0.010, sd * 0.86), TORSO, trunkFacing(sd * 0.70));
      if (build === "old") for (const dy of [0.036, 0.058]) fold(trunkAt(lowC - dy, sd * 0.46), trunkAt(lowC - dy - 0.008, sd * 0.86), TORSO, trunkFacing(sd * 0.66));       // ribs
    }
    if (build === "strong") fold(trunkAt(d.shoulderY - 0.140, 0), trunkAt(d.waistY + 0.022, 0), TORSO, front);
    const nav = P(trunkAt(d.waistY - (d.paunch ? 0.012 : -0.004), 0, d.paunch ? d.paunch[2] * 0.3 : 0));
    if (front[0] * s + front[2] * c > 0.5 && !only) sf.mark(nav[0] - 0.5, nav[1] - 0.5, 1, TORSO);
  }
  // neck, and what shows at the collar
  const neckR = d.neckR ?? 1;
  limb(add(J.spine(d.shoulderY - 0.012), J.torso([0, 0, -0.004])), add(J.head, [0, -d.headR[1] * 0.55, -0.014]), 0.033 * neckR, 0.031 * neckR, skin, { part: NECK });
  if (top.mat && top.open) {
    const front = d.trunkTop[1];                         // the open neck: a narrow strip of chest, lying on the chest's own curve
    limb(add(J.sh, J.torso([0, 0.012, front * 0.34])), add(J.sh, J.torso([0, -(top.open === true ? 0.046 : top.open), front * 0.95])), 0.021, 0.008, top.under || skin, { part: NECK, bias: cloth * 1.5 });
  }
  if (top.mat && top.band) {                             // a round collar: a band lying at the base of the neck, with two rounded points in front
    ball(add(J.sh, J.torso([0, -0.012, d.trunkTop[1] * 0.44])), [0.052, 0.026, 0.044], top.band, {
      part: COLLAR, bias: cloth * 1.5,
      fn: (ux, uy) => (ux * ux * 0.8 + (uy + 1.05) ** 2 < 0.62 || (Math.abs(ux) < 0.09 && uy > 0.05) ? null : undefined),
    }, tw);
  }
  if (top.mat && top.collar) {
    const cm = top.collar === true ? shifted(top.mat, -1) : top.collar, front = d.trunkTop[1];
    for (const sd of [1, -1]) limb(add(J.sh, J.torso([sd * 0.026, 0.012, front * 0.30])), add(J.sh, J.torso([sd * 0.052, -0.016, front * 0.74])), 0.012, 0.008, cm, { part: COLLAR, bias: cloth * 1.5 });
  }
  if (top.buttons && fine && !only) {                     // a row of buttons down the front
    const facing = trunkFacing(0);
    if (facing[0] * s + facing[2] * c > 0.35) for (let hgt = d.shoulderY - 0.075; hgt > hemY + 0.02; hgt -= 0.046) { const q = P(trunkAt(hgt, 0)); sf.dot(q[0] - 0.5, q[1] - 0.5, top.buttons.tones ? top.buttons.tones[1] : pack(top.buttons), TORSO); }
  }

  // ----- arms -----
  const sleeves = top.mat ? (top.sleeves ?? 0.6) : 0, longSleeves = sleeves >= 2;
  for (const k of ["R", "L"]) {
    const A = J[k], part = ARM[k], q = pose[k] || {};
    // (an arm that reaches across in front of the body is no longer the far arm: its forearm and hand are in full light)
    const across = k === farK && P(A.wrist)[2] > P(J.spine(d.waistY))[2] + S * 0.03;
    const armMat = far(k, longSleeves ? top.mat : skin), foreMat = across ? (longSleeves ? top.mat : skin) : armMat;
    const [r0, r1, r2] = d.armR, ease = longSleeves ? (top.ease ?? 0.004) : 0;
    const swell = mix(A.elbow, A.wrist, 0.28);                          // the forearm is thickest just below the elbow
    if (longSleeves) {
      limb(A.shoulder, A.elbow, r0 + ease * 0.5, r1 + ease, armMat, { part });
      limb(A.elbow, swell, r1 + ease, r1 * 1.10 + ease, foreMat, { part });
      limb(swell, A.wrist, r1 * 1.10 + ease, r2 + ease * 1.6, foreMat, { part, hem: true });
    } else {
      // A bare arm is not a tube: it narrows to the elbow, swells again just below it and is narrowest at the
      // wrist. Bent, the elbow comes to a point on the outside of the bend.
      // (One length from shoulder to elbow: two lengths end to end show their joint as a band across the arm
      // whenever the arm points toward us or away.)
      const rE = r1 * 0.92, rW = r2 * 0.88;
      limb(A.shoulder, A.elbow, r0, rE, armMat, { part });
      limb(A.elbow, swell, rE, r1 * 1.10, foreMat, { part });
      limb(swell, A.wrist, r1 * 1.10, rW, foreMat, { part });
      const out = sub(A.uDir, A.fDir), bent = Math.hypot(out[0], out[1], out[2]);
      if (bent > 0.5) ball(add(A.elbow, mul(out, (r1 * 0.34 * Math.min(1, bent / 1.4)) / bent)), [rE, rE, rE], bent > 1 ? armMat : foreMat, { part });
    }
    if (longSleeves && top.cuffs && !coarse) limb(mix(A.elbow, A.wrist, 0.90), mix(A.elbow, A.wrist, 1.03), r2 + ease * 1.6 + 0.002, r2 + ease * 1.6 + 0.002, across ? top.cuffs : far(k, top.cuffs), { part: SLEEVE[k], squareStart: true, squareEnd: true });     // a shirt cuff showing at the wrist
    if (sleeves > 0 && !longSleeves) {
      // a short sleeve: its own print, fixed to the sleeve so that it swings with the arm
      const len = d.upperArm * sleeves, seed = k === "R" ? 0.31 : 0.67;
      const end = sleeves <= 1 ? mix(A.shoulder, A.elbow, sleeves) : mix(A.elbow, A.wrist, sleeves - 1);
      if (sleeves > 1) limb(A.shoulder, A.elbow, r0 + 0.005, r1 + 0.008, far(k, top.mat), { part: SLEEVE[k] });
      limb(sleeves > 1 ? A.elbow : A.shoulder, end, sleeves > 1 ? r1 + 0.008 : r0 + 0.005, (sleeves > 1 ? lerp(r1, r2, sleeves - 1) : lerp(r0, r1, sleeves)) + (top.cuff ?? 0.010), far(k, top.mat), {
        part: SLEEVE[k], hem: true,
        fn: printed ? (t, nx) => (t <= 0 ? undefined : flowers(seed + Math.asin(clamp1(nx)) * 0.045, t * len, top.pattern))
          : top.trim ? (t) => (t > 1 - (top.trimW ?? 0.30) ? far(k, top.trim) : undefined) : null,
      });
    }
    // the hand
    const hm = across ? skin : far(k, skin), hpart = HAND[k], hr = d.handR;
    limb(A.wrist, A.palm, hr * (longSleeves ? 0.80 : 0.70), hr * 0.98, hm, { part: hpart });     // (a bare wrist is narrower than the hand)
    limb(A.palm, A.tip, hr * 0.94, hr * (q.grip || q.finger ? 0.86 : 0.56), hm, { part: hpart });
    if (!coarse && !q.finger) limb(A.thumb0, A.thumb1, hr * 0.42, hr * 0.32, hm, { part: hpart });
    if (q.finger) limb(add(A.palm, mul(A.hDir, 0.004)), add(A.palm, mul(A.hDir, 0.046)), 0.0078, 0.0058, hm, { part: hpart });   // a pointing finger, out of the fist
  }

  // ----- head -----
  const hy = J.headYaw, hr = d.headR, hc = J.head;
  const cpi = Math.cos(J.headPitch), spi = Math.sin(J.headPitch);
  const tipped = (v) => [v[0], v[1] * cpi - v[2] * spi, v[1] * spi + v[2] * cpi];           // the head's own nod
  const headPt = (v) => add(hc, turn(tipped(v), hy));                 // a point given in the head's own frame
  const hp = (x, y, z) => headPt([x * hr[0], y * hr[1], z * hr[2]]);  // the same, in fractions of the skull's half-sizes
  // from a point on the head as seen, back to the head's own directions: hairlines, hats and hoods turn and nod with it
  const onHead = (ux, uy, uz) => { const o = own(ux, uy, uz, hy); return [o[0], o[1] * cpi + o[2] * spi, -o[1] * spi + o[2] * cpi]; };
  const hairAt = hair.where || (() => false);
  const eyeY = face.eyeY ?? 0.06, eyeX = face.eyeX ?? 0.36, mouthY = face.mouthY ?? -0.74;
  const scalp = hair.mat && !hair.wig ? hair.mat : null;
  // The head is built of several shapes and shaded as one: flat, with a band of shade inside its outline on the side away from the light.
  ball(hc, hr, skin, { part: HEAD, tone: 1, fn: scalp ? (ux, uy, uz) => { const o = onHead(ux, uy, uz); return hairAt(o[0], o[1], o[2]) ? scalp : undefined; } : null }, hy);
  // the jaw: from the cheeks down and forward to the chin. A beard is the same shape in another color, starting lower.
  const jaw = face.jaw ?? 0.88, chin = face.chin ?? 0.50, chinY = face.chinY ?? -0.84, chinZ = face.chinZ ?? 0.54;
  // A short beard (face.short: { mat, stubble, from, chin }): on the jaw itself, along its lower edge and over the chin, with
  // stubble above it; never on the upper lip. `from` and `chin` are how far down the jaw (0 at the cheekbones, 1 at the
  // chin) the stubble and the beard over the chin begin.
  const sb = face.short, fwd = Math.sin(th + J.headYaw);
  const [noseLen, noseOut, noseTip] = Array.isArray(face.nose) ? face.nose : [1, face.nose ?? 1, face.nose ?? 1];
  const noseEnd = hp(0, eyeY - 0.04 - 0.34 * noseLen, 0.97 + 0.20 * noseOut);
  // The upper lip, as seen: between the nose and the mouth, as wide as the mouth. A short beard keeps clear of it (no moustache).
  const lipBox = sb && !sb.moustache ? (() => { const mw = (face.mouthW ?? 0.22) * 1.25, a = P(hp(-mw, mouthY, 0.90)), b = P(hp(mw, mouthY, 0.90)), m = P(hp(0, mouthY, 0.95)), n = P(noseEnd); return [Math.min(a[0], b[0]) - 1, Math.max(a[0], b[0]) + 1, n[1] - 1, m[1] + 1]; })() : null;
  const stubbly = (x, y) => (S < 200 || (sb.dense ? (x + y) % 3 !== 0 : (x + y) % 2 === 0) ? sb.stubble : undefined);       // (on a portrait's big face, stubble is a stipple over the skin: every other pixel, or two in three when it is `dense`)
  const shortBeard = sb ? (t, nx, ny, x, y) => {
    if (lipBox && x + 0.5 > lipBox[0] && x + 0.5 < lipBox[1] && y + 0.5 > lipBox[2] && y + 0.5 < lipBox[3]) return undefined;          // the upper lip and the mouth: clean
    if (Math.abs(fwd) > 0.35 && nx * fwd > 0.30 && t < (sb.chin ?? 0.86)) return t > (sb.lip ?? 0.6) ? stubbly(x, y) : undefined;      // the front of a turned face: lips and upper lip stay clear
    if (t > (sb.chin ?? 0.86) || ny > (sb.under ?? 0.30) || (Math.abs(nx) > 0.74 && t > (sb.side ?? 0.30))) return sb.mat;      // (under: how far round to the underside of the jaw the beard proper begins)
    return t > (sb.from ?? 0.45) ? stubbly(x, y) : undefined;
  } : null;
  limb(hp(0, -0.22, 0.24), hp(0, chinY, chinZ), hr[0] * jaw, hr[0] * chin, face.shadow || skin, { part: HEAD, tone: 1, fn: shortBeard || (face.shadow && face.shadowFrom ? (t) => (t < face.shadowFrom ? skin : undefined) : null) });     // (shadowFrom: how far down the jaw the stubble starts)
  if (face.shadow) limb(hp(0, -0.20, 0.22), hp(0, -0.34, 0.30), hr[0] * (jaw + 0.01), hr[0] * (jaw - 0.02), skin, { part: HEAD, tone: 1 });      // an unshaven jaw: the cheeks above it are clean
  if (face.beard) {
    const long = face.beardLen ?? 0;
    const [by, bz] = face.beardFrom || [-0.50, 0.30];                  // (where it starts on the cheeks: farther back, and the lips show above it in profile)
    const stub = face.beardStubble, stubTo = face.beardStubbleTo ?? 0.3;  // (a short beard: stubble where it starts, the beard itself below)
    limb(hp(0, by, bz), hp(0, chinY - 0.04 - long, face.beardZ ?? chinZ + 0.02), hr[0] * (jaw - 0.06), hr[0] * (face.beardW ?? chin + 0.06), face.beard, {
      part: HAIR,                                                       // (a beard going grey: it is lighter over the chin)
      fn: stub ? (t) => (t <= 0.001 ? null : t < stubTo ? stub : undefined)
        : face.beardGrey && fine ? (t, across) => (t > 0.56 && Math.abs(across) < 0.52 ? face.beardGrey : undefined) : null,
      squareEnd: !!face.beardSquare,                                    // (trimmed square across the bottom; beardW: how broad it is there, beardZ: how far forward)
    });
  }
  if (face.jowl) ball(hp(0, -0.90, 0.26), [hr[0] * face.jowl, hr[1] * 0.26, hr[2] * 0.52], skin, { part: HEAD, tone: 1 }, hy);       // a second chin
  // the nose: a wedge from between the eyes down and out to its tip
  limb(hp(0, eyeY - 0.02, 0.90), noseEnd, 0.0045, 0.0082 * noseTip, skin, { part: NOSE });
  // ears, unless the hair hangs over them
  if (face.ears !== false) for (const sd of [1, -1]) if (!hairAt(sd * 0.99, -0.10, -0.08) || hair.ears) ball(hp(sd * (face.earOut ?? 0.98), eyeY - 0.20, -0.08), [0.009, 0.019, 0.012].map((v) => v * (face.ear ?? 1)), skin, { part: EAR }, hy);      // (face.ear: how big; face.earOut: how far out from the middle of the head, in half-widths: an ear that stands clear of the hair)
  if (hair.mat) {
    const g = hair.bulk ?? 1.07, g3 = Array.isArray(g) ? g : [g, g, g], up3 = hair.lift || [0, 0.003, 0];
    if (g3[0] !== 1 || hair.wig) ball(headPt(up3), [hr[0] * g3[0], hr[1] * g3[1], hr[2] * g3[2]], hair.mat, {
      part: HAIR,
      fn: (ux, uy, uz, x, y) => { const o = onHead(ux, uy, uz); return !hairAt(o[0], o[1], o[2]) ? null : hair.texture ? hair.texture(o[0], o[1], o[2], x, y) : undefined; },
    }, hy);
    // Thick hair, or a wig, stands out from the head: what shows between it and the cheek is the far side of it, seen from inside.
    if (g3[0] >= 1.14 || hair.wig) ball(headPt(up3), [hr[0] * g3[0], hr[1] * g3[1], hr[2] * g3[2]], shifted(hair.mat, 1), {
      part: HAIR, bias: -R(hr[2] * g3[2]) * 1.25,
      fn: (ux, uy, uz) => { const o = onHead(ux, uy, -uz); return hairAt(o[0], o[1], o[2]) ? undefined : null; },
    }, hy);
    for (const q of hair.puffs || []) ball(hp(q[0], q[1], q[2]), [hr[0] * q[3], hr[1] * q[4], hr[2] * q[5]], q[6] || hair.mat, { part: HAIR }, hy);
  }
  if (face.wrap) {
    // Modern wrap-around sunglasses: one dark band across both eyes with a notch over the nose, and an arm back to each ear.
    const half = face.wrapH ?? 0.19, mid = eyeY + 0.03;
    ball(headPt([0, 0, 0.003]), [hr[0] * 1.05, hr[1] * 1.04, hr[2] * 1.06], face.wrap, {
      part: HAT, fn: (ux, uy, uz) => {
        const q = onHead(ux, uy, uz), y = q[1] - mid;
        if (q[2] < -0.12) return null;                                  // nothing behind the ears
        if (q[2] < 0.34) return Math.abs(y - 0.03) < 0.055 ? undefined : null;       // the arm
        return y < half && y > -(Math.abs(q[0]) < 0.13 ? half * 0.30 : half) ? undefined : null;
      },
    }, hy);
  }
  const wrapMid = eyeY + 0.03;
  if (face.moustache) for (const sd of [1, -1]) limb(hp(0, mouthY + 0.20, face.moustacheZ ?? 1.02), hp(sd * (face.moustacheW ?? 0.33), mouthY + 0.10, 0.86), 0.0058, 0.0044, face.moustache, { part: HAIR });

  // hats, hair that hangs, packs, bags and whatever else this character wears or carries
  const ctx = {
    sf, J, P, R, limb, ball, own, onHead, headPt, hp, wide, deep, widthAt, depthAt, roundAt, fold, trunkAt, trunkFacing, skirtAt, far, d, S, th, hy, tw, ht, fine, coarse, pose, spec, skin, cloth, under, farSide: farK,
    parts: { HEAD, HAIR, TORSO, PELVIS, SKIRT, EXTRA, EXTRA2, EXTRA3, HAT, NECK, ARM, HAND, LEG, FOOT, SLEEVE, DRAPE, DRAPE2, BELT, COLLAR, HELD, NOSE, EAR },
  };
  if (spec.extras) spec.extras(ctx);
  if (only) {                                                           // a seat by itself: nothing more to draw
    const held = Math.max(1, Math.round(S * 0.020));
    return sf.finish({ reach: held, rim: fine && spec.rim !== false, outline: fine && spec.outline !== false, inset: () => 0, seams: () => false,
      cast: (a, b) => (a === EXTRA2 || a === EXTRA3) && a !== b ? held : 0 });
  }

  // ----- face, placed pixel by pixel -----
  // How much of a face there is room for depends on how many pixels wide the head is (a child's head is
  // bigger than a grown-up's of the same height). Full: the eye patterns above, brows, cheeks, lines. Middle:
  // every eye is drawn the narrow way and the mouth is short. Small: a dot for each eye.
  const headPx = 2 * hr[0] * S, faceFull = headPx >= FACE_FULL, faceFine = headPx >= FACE_MID;
  const ang = th + hy, sideways = Math.sin(ang), frontOn = Math.abs(sideways) < 0.12 && Math.cos(ang) > 0;
  const see = (v) => { const w = turn(tipped(v), hy); return w[0] * s + w[2] * c; };          // how much a head direction faces the viewer
  const scr = (x, y, z) => P(hp(x, y, z));
  const mid = scr(0, eyeY, 0.80)[0];                                    // the middle of the face, as seen
  const mirror = (x) => Math.round(2 * mid) - 1 - x;
  const ink = inksOf(face, skin);                                       // the face's own colours (inksOf, below)
  const shade = ink.shades, big = !!(opt && opt.portrait);
  if (big) bigFace({ sf, scr, see: (v) => see(unit(v)), face, ink, skin, eyeX, eyeY, mouthY, headPx, pose, sideways, mid, noseTip: P(noseEnd), part: HEAD });
  const eyes = [];
  for (const sd of big ? [] : [1, -1]) {
    const vis = see(unit([sd * 0.25, 0, 0.97]));
    if (vis < 0.20) continue;
    const q = scr(sd * eyeX, eyeY, 0.80), w = faceFull && vis > 0.70 ? 2 : 1;
    const right = Math.abs(sideways) > 0.86 ? sideways < 0 : q[0] > mid;                    // which way is "away from the nose", as seen
    eyes.push({ x: right ? Math.round(q[0] - w / 2) : Math.round(q[0] + w / 2) - 1, y: Math.round(q[1] - 0.5), out: right ? 1 : -1, w, vis });
  }
  if (frontOn && eyes.length === 2) { eyes[1].x = mirror(eyes[0].x); eyes[1].y = eyes[0].y; }   // seen straight on, a face is the same on both sides
  for (const e of eyes) {
    const put = (i, j, color) => sf.dot(e.x + e.out * i, e.y + j, color, HEAD);
    if (shade) {                                                                          // dark glasses: a lens over each eye
      if (faceFull) for (let i = -1; i <= e.w; i++) for (let j = -1; j <= 0; j++) put(i, j, shade);
      else if (faceFine) for (let i = -1; i <= 1; i++) for (let j = -1; j <= 0; j++) { if (i >= 0 || j < 0) put(i, j, shade); }
      else { put(0, 0, shade); put(1, 0, shade); }
      continue;
    }
    if (!faceFine) { put(0, 0, pose.blink ? ink.lidShade : ink.small); continue; }
    const kind = pose.blink ? EYES[pose.squeeze ? "tight" : "shut"] : typeof face.eyes === "object" ? face.eyes : EYES[face.eyes || "plain"] || EYES.plain, rows = e.w === 2 ? kind.full : kind.thin;      // (face.eyes: a kind of eye from the table, or a person's own)
    rows.forEach((row, j) => { for (let i = 0; i < row.length; i++) { const col = ink.of(row[i]); if (col) put(i, j - kind.at, col); } });
    if (ink.brow && (faceFull || !kind.at)) {                                             // (on a middle-sized face a lid line does for the brow as well)
      const up = (face.browUp ?? 2) + (kind.at ? 1 : 0), n = e.w === 2 ? (face.browW ?? 3) : 2, squeezed = pose.blink && pose.squeeze;
      const shape = faceFull && face.brow ? (e.w === 2 ? face.brow.full : face.brow.thin) || null : null;    // their own brows: a rise or fall for each pixel, from the nose outward
      const tilt = faceFull ? (squeezed ? 1 : face.browTilt || 0) : 0;                     // (eyes squeezed shut pull the brows down toward the nose)
      if (shape && !squeezed) shape.forEach((dy, i) => { if (dy !== null) put(i - (shape.length > 3 ? 1 : 0), -up + dy, ink.brow); });
      else for (let i = 0; i < n; i++) put(i - (n > 3 ? 1 : 0), -up + (tilt > 0 && i === 0 ? 1 : tilt < 0 && i === n - 1 ? 1 : 0), ink.brow);
    }
    if (faceFull && e.w === 2) {
      if (ink.blush) for (const [i, j] of face.cheek || [[1, 2]]) put(i, j, ink.blush);     // a little colour in the cheek
      if (face.freckles) { put(0, 3, ink.freckle); put(2, 4, ink.freckle); }
    }
  }
  if (face.wrap && face.glint !== false && S >= 52) {
    // one small glint on the dark glasses, at the upper corner (toward the light) of whichever lens is farthest left as we see it
    let best = null;
    for (const sd of [1, -1]) { if (see(unit([sd * 0.45, 0, 0.89])) < 0.30) continue; const q = scr(sd * 0.46, wrapMid + 0.07, 0.90); if (!best || q[0] < best[0]) best = q; }
    if (best) { const gx = Math.round(best[0] - 0.5), gy = Math.round(best[1] - 0.5), glint = pack(face.glint || "#c4cdea"); sf.dot(gx, gy, glint, HAT); if (faceFull) sf.dot(gx - 1, gy, glint, HAT); }
  }
  // seen from the side, glasses show the arm that runs back to the ear
  if (shade && eyes.length === 1 && faceFine) for (let i = 2; i <= 5; i++) sf.dot(eyes[0].x + eyes[0].out * i, eyes[0].y - 1, shade, HEAD);
  // the nose: the shadow under its tip, on the side away from the light (face.noseShade)
  if (face.noseShade && faceFull && see([0, 0, 1]) > 0.35 && !shade && !big) {
    const q = P(noseEnd), x = Math.round(q[0] - 0.5) + (sideways > 0.3 ? 0 : 1), y = Math.round(q[1] - 0.5) + 1;
    sf.dot(x, y, ink.lidShade, HEAD);
  }
  // the mouth: a line from corner to corner when shut; open shapes for talking
  if (face.mouth !== false && !coarse && see([0, 0, 1]) > 0.10 && !big) {
    const mw = face.mouthW ?? 0.22, mz = 0.95;
    const pts = [scr(-mw, mouthY, mz - 0.12), scr(0, mouthY, mz + (Math.abs(sideways) > 0.6 ? 0.06 : 0)), scr(mw, mouthY, mz - 0.12)].filter((q, i) => i === 1 || see(unit([(i - 1) * 0.5, 0, 0.87])) > 0.25);
    let x0 = Infinity, x1 = -Infinity;
    for (const q of pts) { x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); }
    const mq = scr(0, mouthY, mz), y = Math.round(mq[1] - 0.5), open = pose.mouth || 0;
    let a = Math.round(x0), b = Math.max(a, Math.round(x1) - 1);
    if (!faceFine) { a = b = Math.round(mq[0] - 0.5); }
    else if (frontOn) { const half = Math.max(1, Math.round((x1 - x0) / 2)); a = Math.round(mid) - half; b = Math.round(mid) + half - 1; }
    const lip = ink.lip, inside = ink.inside, smile = face.smile || 0;
    const dot = (x, y, col) => { sf.dot(x, y, col, HEAD); if (face.beard) sf.dot(x, y, col, HAIR); };      // (on the skin, or on a beard)
    const hidden = face.beard && !open && !face.mouthShows;             // (a long beard hides a shut mouth; a trimmed one does not)
    if (!hidden) for (let x = a; x <= b; x++) {
      const end = faceFine && b - a >= 2 && (x === a || x === b) && Math.abs(sideways) < 0.6;
      if (open === 0) dot(x, y - (end ? smile : 0), lip);
      else if (!end || open > 1) { dot(x, y, inside); if (open > 1) dot(x, y + 1, x === a || x === b ? lip : inside); }
      else dot(x, y, lip);
    }
    if (ink.lips && faceFull && open === 0 && !hidden) for (let x = a + (b - a >= 2 ? 1 : 0); x <= b - (b - a >= 2 ? 1 : 0); x++) dot(x, y + 1, ink.lips);       // a painted lower lip
  }
  // the lines of an older face: from the nose to the corners of the mouth, across the forehead, under the eyes
  if (face.lines && faceFull && !big) {
    const n = face.lines;
    for (const sd of [1, -1]) {
      if (see(unit([sd * 0.5, 0, 0.87])) < 0.35) continue;
      const a = scr(sd * 0.26, eyeY - 0.50, 0.93), b = scr(sd * 0.38, mouthY + 0.10, 0.86);
      sf.stroke(a[0], a[1], b[0], b[1], 1, HEAD);
      if (n > 1) { const e0 = scr(sd * 0.22, eyeY - 0.20, 0.84), e1 = scr(sd * 0.52, eyeY - 0.16, 0.80); sf.stroke(e0[0], e0[1], e1[0], e1[1], 1, HEAD); }
    }
    if (n > 1 && see([0, 0, 1]) > 0.3 && !hairAt(0, 0.50, 0.86)) { const a = scr(-0.34, eyeY + 0.52, 0.84), b = scr(0.34, eyeY + 0.52, 0.84); sf.stroke(a[0], a[1], b[0], b[1], 1, HEAD); }
  }
  // Lines the eye expects: between the two legs, between an arm and the body it hangs against,
  // and a thin shadow under the edge of a sleeve, a pair of shorts, a skirt or an untucked shirt.
  const armR = (q) => q === ARM.R || q === SLEEVE.R, armL = (q) => q === ARM.L || q === SLEEVE.L;
  const legR = (q) => q === LEG.R || q === SHORTS.R, legL = (q) => q === LEG.L || q === SHORTS.L;
  const ofHead = (q) => q === HEAD || q === HAIR || q === NOSE || q === EAR || q === HAT;
  const ofArm = (q) => armR(q) || armL(q) || q === HAND.R || q === HAND.L;
  // an arm shows a line against the body only below the armpit: over the top of the shoulder the two are one shape
  const pitR = P(J.R.shoulder)[1] + R(capR) * 0.7, pitL = P(J.L.shoulder)[1] + R(capR) * 0.7;
  const beside = (q, other, y) => other === TORSO && ((armR(q) && y > pitR) || (armL(q) && y > pitL));
  const px = (k) => Math.max(1, Math.round(S * k));
  const reach = { chin: px(0.034), brim: px(spec.brim ?? 0.014), arm: px(0.022), hem: px(0.016), held: px(0.020) };
  // Where the hands and the top of the head are in the finished picture, measured from the anchor (x right, y down):
  // for a scene that lays a painted thing over a hand, and for tools.
  const spot = (v) => { const q = P(v); return [Math.round((q[0] - ox) * 10) / 10, Math.round((q[1] - oy) * 10) / 10]; };
  sf.spots = { handR: spot(J.R.palm), handL: spot(J.L.palm), head: spot(add(J.head, [0, hr[1], 0])) };
  if (big) {
    // A portrait's face is shaded as one form: a band of shade inside the outline of the head on the side away from the
    // light, but no line where the chin stands in front of the skull (at this size that line would cross the face).
    const { w: sw, h: sh, m: sm, t: st, p: spart } = sf, band = Math.max(1, Math.min(2, Math.round(S * 0.0055))), faceParts = new Set([HEAD, NOSE, EAR]);
    for (let y = 0; y < sh; y++) for (let x = 0; x < sw; x++) {
      const i = y * sw + x;
      if (!sm[i] || spart[i] !== HEAD || st[i] !== 1) continue;
      for (let j = 1; j <= band; j++) {
        const qx = x + Math.round(j * 0.30), qy = y + Math.round(j * 0.95), q = qy * sw + qx;
        if (qx >= sw || qy >= sh || !sm[q] || !faceParts.has(spart[q])) { st[i] = 2; break; }
      }
    }
  }
  return sf.finish({
    reach: Math.max(reach.chin, reach.brim, reach.arm, reach.hem, reach.held),
    rim: fine && spec.rim !== false, outline: fine && spec.outline !== false,     // at full size every form has a line of its own darker color round it; small, it would only be mud
    inset: (q) => (q === HEAD && !big ? [1, 0.30, 0.95] : 0),       // (a portrait's face has its own band, above)      // a face is shaded under the jaw, and kept clear across the cheek, where the far eye is (wider on a portrait's big head)
    seams: (a, b, below, x, y) =>
      (a === SHORTS.R && b === LEG.R) || (a === SHORTS.L && b === LEG.L) || (a === SLEEVE.R && b === ARM.R) || (a === SLEEVE.L && b === ARM.L) ||
      (a === SKIRT && (b === LEG.R || b === LEG.L)) || (a === BELT || b === BELT) || (a === COLLAR && b === TORSO) ||
      (longSleeves && ((a === ARM.R && b === HAND.R) || (a === ARM.L && b === HAND.L) || (b === ARM.R && a === HAND.R) || (b === ARM.L && a === HAND.L))) ||
      (a === EAR && b === HEAD) || (below && !top.mat && a === TORSO && b === SKIRT) ||
      (below ? !!loose && a === TORSO && (b === PELVIS || b === SKIRT || legR(b) || legL(b))
        : (legR(a) && legL(b)) || (legL(a) && legR(b)) || beside(a, b, y) || beside(b, a, y)),
    // Shadows one part throws on another, in pixels.
    cast: (a, b) => {
      if (ofHead(a)) return ofHead(b) ? ((a === HAT || a === HAIR) && b === HEAD ? reach.brim : 0) : b === NECK || b === TORSO || b === COLLAR || b === DRAPE || ofArm(b) ? reach.chin : 0;
      if (ofHead(b) || b === NECK) return a === HAT ? reach.brim : 0;
      if (ofArm(a)) return ofArm(b) ? 1 : reach.arm;
      if (a === TORSO || a === BELT || a === COLLAR) return ofArm(b) ? 1 : reach.hem;
      if (a === SKIRT || a === SHORTS.R || a === SHORTS.L || a === PELVIS) return reach.hem;
      if (a === EXTRA || a === EXTRA2 || a === EXTRA3 || a === HELD || a === DRAPE || a === DRAPE2) return reach.held;
      if (a === LEG.R || a === LEG.L) return b === LEG.R || b === LEG.L ? reach.hem : 0;
      return 0;
    },
  });
}

// =====================================================================================
// Poses and animation
// =====================================================================================

/** A smooth hump of the given width centered on c, on a clock that wraps at 1. */
const hump = (x, c, w) => { const dlt = Math.abs((((x - c + 0.5) % 1) + 1) % 1 - 0.5); return dlt < w / 2 ? Math.cos((Math.PI * dlt) / w) ** 2 : 0; };

/** How far a character travels in one full walk cycle, in their own heights. */
export const strideOf = (spec, swing = (spec.walk && spec.walk.swing) ?? 0.46) => 4 * (spec.dim.thigh + spec.dim.shin) * Math.sin(swing);

/**
 * One moment of a walk. ph runs from 0 to 1 over two steps; 0 is the right heel landing.
 * The style makes it somebody's own walk: swing (length of stride), arm (how far the arms swing),
 * elbow (how bent they are), pump (how much more they bend on the way forward), lean, lift (how high the knees come), bob and wag (the head),
 * and hold: { L: {...} }, which keeps an arm in a fixed pose for carrying something.
 */
export function walkPose(ph, o = {}) {
  const A = o.swing ?? 0.46, s0 = Math.sin(A), lift = o.lift ?? 1;
  const leg = (f) => {
    f = ((f % 1) + 1) % 1;
    // on the ground the foot moves back at a steady rate, so it does not slide; in the air it eases forward
    const pitch = f < 0.5 ? Math.asin(s0 * (1 - 4 * f)) : -A + 2 * A * (1 - (1 - (f - 0.5) * 2) ** 2.1);
    const knee = 0.05 + 0.12 * hump(f, 0.10, 0.24) + 0.80 * lift * hump(f, 0.65, 0.40);
    const foot = 0.30 * hump(f, 0.0, 0.16) - 0.80 * hump(f, 0.56, 0.2) - 0.25 * hump(f, 0.74, 0.2) + 0.2 * hump(f, 0.94, 0.12);
    return { pitch, knee, foot };
  };
  const r = leg(ph), l = leg(ph + 0.5), a = 2 * Math.PI * ph, arm = o.arm ?? 0.42, bend = o.elbow ?? 0.22, pump = 0.32 + (o.pump || 0);
  const p = {
    lean: o.lean ?? 0.06, twist: (o.twist ?? 0.13) * Math.cos(a), hipTwist: -0.07 * Math.cos(a), sway: (o.sway ?? 0.012) * Math.sin(a),
    head: { nod: -0.03 + (o.bob || 0) * Math.cos(2 * a), turn: (o.wag || 0) * Math.sin(a) },
    R: { leg: [r.pitch, 0.02], knee: r.knee, foot: r.foot, footYaw: 0.10, arm: [-arm * Math.cos(a), 0.07], elbow: bend + pump * (0.5 - 0.5 * Math.cos(a)) },
    L: { leg: [l.pitch, 0.02], knee: l.knee, foot: l.foot, footYaw: 0.10, arm: [arm * Math.cos(a), 0.07], elbow: bend + pump * (0.5 + 0.5 * Math.cos(a)) },
  };
  for (const k of ["R", "L"]) if (o.hold && o.hold[k]) p[k] = { ...p[k], ...o.hold[k] };
  p.gait = { phase: ((ph % 1) + 1) % 1 };                              // for things that are carried: where in the step this is
  return p;
}

// ---------- where things are on a body, for placing hands ----------
// Hands are placed by naming a spot: measured in the torso's own space from the middle of the shoulders
// (x toward the character's right, y up, z forward). These give the usual spots for any build.
const spots = (d) => {
  const hip = -(d.shoulderY - d.hipY), waist = -(d.shoulderY - d.waistY), chest = d.trunkTop[1], belly = d.trunkLow[1] + (d.bellyFwd || 0) + (d.paunch ? d.paunch[2] * 0.4 : 0);
  const headY = d.neckY - d.shoulderY + 0.010 + d.headR[1];
  return { hip, waist, chest, belly, headY, chinY: headY - d.headR[1] * 1.12, side: d.pelvisR[0], back: d.trunkLow[1] };
};

// Ways of standing. Each changes the arms of the plain standing pose. `sp` is spots(d).
const STANCES = {
  /** hands lightly clasped in front of the waist */
  clasped(p, sp) { for (const [k, sd] of [["R", 1], ["L", -1]]) p[k] = { ...p[k], hand: [sd * 0.016, sp.waist - 0.006, sp.belly + 0.036], bend: [sd * 0.45, -0.1, -0.9], curl: 0.9 }; },
  /** fists on hips */
  akimbo(p, sp) { for (const [k, sd] of [["R", 1], ["L", -1]]) p[k] = { ...p[k], hand: [sd * (sp.side + 0.012), sp.hip + 0.085, 0.012], bend: [sd, 0, -0.55], grip: true }; },
  /** hands behind the back */
  behind(p, sp) { for (const [k, sd] of [["R", 1], ["L", -1]]) p[k] = { ...p[k], hand: [sd * 0.020, sp.hip + 0.060, -(sp.back + 0.022)], bend: [sd * 0.5, -0.5, -0.7] }; },
  /** one hand holding the other elbow: a reader's way of standing, a little shy */
  elbow(p, sp, d) {
    p.R = { ...p.R, arm: [0.04, 0.05], elbow: 0.10 };
    p.L = { ...p.L, hand: [d.shoulderW - 0.004, -(d.shoulderDrop + d.upperArm * 0.86), sp.belly * 0.60 + 0.034], bend: [-0.6, -0.7, -0.3], curl: 1.1 };
  },
  /** arms folded across the chest */
  folded(p, sp, d) {
    p.R = { ...p.R, hand: [-0.058, sp.waist + 0.085, sp.chest + 0.034], bend: [1, -0.5, 0.1], curl: 0.8 };
    p.L = { ...p.L, hand: [0.050, sp.waist + 0.062, sp.chest + 0.022], bend: [-1, -0.5, 0.1], curl: 0.8 };
  },
  /** thumbs hooked in the straps of a backpack */
  straps(p, sp, d) { for (const [k, sd] of [["R", 1], ["L", -1]]) p[k] = { ...p[k], hand: [sd * 0.062, -0.085, sp.chest + 0.022], bend: [sd * 0.25, -1, -0.3], grip: true }; },
  /** one fist on a hip, the other arm hanging */
  hip(p, sp) { p.L = { ...p.L, hand: [-(sp.side + 0.012), sp.hip + 0.085, 0.012], bend: [-1, 0, -0.55], grip: true }; },
  /** one hand held up at the chest with something in it (a scroll, a ladle), the other arm as it was */
  carry(p, sp, d) { p.R = { ...p.R, hand: [d.shoulderW * 0.72, sp.waist + 0.080, sp.belly + 0.072], bend: [0.55, -0.8, -0.3], grip: true }; },
  /** worn out from standing a long time: the knees soft, one foot a little forward, the head sunk (the arms are left as they are) */
  weary(p) {
    p.R = { ...p.R, leg: [0.16, 0.05], knee: 0.32 };
    p.L = { ...p.L, leg: [-0.02, 0.05], knee: 0.16 };
    p.head = { nod: 0.11 };
  },
  /** at ease, the weight on the left leg: the right knee loose, that foot a little forward and turned out (the arms are left as they are) */
  easy(p) {
    p.L = { ...p.L, leg: [-0.02, 0.0], knee: 0.0 };
    p.R = { ...p.R, leg: [0.17, 0.10], knee: 0.30, footYaw: 0.62 };
    p.sway = -0.010;
    p.lean = (p.lean || 0) - 0.03;
  },
  /** both hands resting on a stomach */
  belly(p, sp) { for (const [k, sd] of [["R", 1], ["L", -1]]) p[k] = { ...p[k], hand: [sd * 0.040, sp.waist + 0.020, sp.belly + 0.026], bend: [sd, -0.3, -0.3], curl: 0.8 }; },
};

/** Standing still. f counts slow breaths: eight steps to one breath. o.stance picks a way of standing; o.dim is the build. */
export function standPose(f = 0, o = {}) {
  const br = 0.5 - 0.5 * Math.cos((2 * Math.PI * f) / 8);
  const p = {
    breath: br, lean: o.lean ?? 0.02,
    R: { arm: [0.05, 0.10], elbow: 0.18, leg: [0.0, 0.04], knee: 0.03 },
    L: { arm: [-0.02, 0.10], elbow: 0.14, leg: [0.0, 0.04], knee: 0.03 },
  };
  if (o.stance && STANCES[o.stance]) STANCES[o.stance](p, spots(o.dim || ADULT), o.dim || ADULT);
  return p;
}

/**
 * Talking with the hands. g picks the gesture, f counts frames within it.
 *   0 a nod            1 one hand up, making a point    2 both palms up: a shrug     3 a hand on the hip
 *   4 both arms up     5 a hand to the heart            6 a hand to the chin         7 showing off muscles
 *   8 an open hand     9 both hands waving              10 pointing straight ahead   11 a finger in the air
 *   12 arms folded     13 a hand cupped to the ear      14 a shaken fist             15 waving something away
 *   16 wiping the brow 17 counting on the fingers       18 both hands spread wide    19 a thumb over the shoulder
 *   20 a nod aside, toward something off to that side (the river, the road), the open hand following it
 *   21 a hand raised in blessing, open, the palm toward the listener
 * o.hand ("R" or "L") is the hand that makes one-handed gestures: the other may be holding something.
 */
export function talkPose(f = 0, g = 0, o = {}) {
  const wob = Math.sin((2 * Math.PI * f) / 6), p = standPose(f, o), d = o.dim || ADULT, sp = spots(d);
  const H = o.hand === "L" ? "L" : "R", sd = H === "R" ? 1 : -1, O = H === "R" ? "L" : "R";
  const both = (make) => { p.R = { ...legs("R"), ...make(1) }; p.L = { ...legs("L"), ...make(-1) }; };
  const legs = (side) => { const q = { ...p[side] }; for (const k of ["arm", "elbow", "fore", "tuck", "hand", "bend", "grip", "curl", "finger", "point", "flat", "thumb"]) delete q[k]; return q; };   // an arm let go of whatever the stance had it doing
  const free = (side) => ({ ...legs(side), arm: side === "R" ? [0.05, 0.10] : [-0.02, 0.10], elbow: 0.16 });
  if (g === 1) {                    // one hand up, making a point
    p[H] = { ...legs(H), arm: [0.42, 0.16], elbow: 1.75 + 0.18 * wob };
    p.head = { nod: 0.03 * wob };
  } else if (g === 2) {             // both palms up: a shrug
    both(() => ({ arm: [0.22, 0.34], elbow: 1.25 + 0.10 * wob, flat: true }));
    p.breath = 1;
    p.head = { nod: -0.04, turn: 0.10 * wob };
  } else if (g === 3) {             // hand on hip
    p[O] = { ...legs(O), hand: [-sd * (sp.side + 0.012), sp.hip + 0.085, 0.012], bend: [-sd, 0, -0.55], grip: true };
    p.head = { nod: 0.02 * wob, turn: 0.06 * wob };
  } else if (g === 4) {             // both arms up
    p.R = { ...legs("R"), arm: [2.55 + 0.10 * wob, 0.38], elbow: 0.25, flat: true };
    p.L = { ...legs("L"), arm: [2.55 - 0.10 * wob, 0.38], elbow: 0.25, flat: true };
    p.breath = 1;
    p.head = { nod: -0.10 };
  } else if (g === 5) {             // a hand to the heart
    p[H] = { ...legs(H), hand: [-sd * 0.030, -0.085 + 0.004 * wob, sp.chest + 0.030], bend: [sd, -0.6, 0], flat: true };
    p.head = { nod: 0.04 + 0.02 * wob, turn: 0.05 * wob };
  } else if (g === 6) {             // a hand to the chin, the other holding its elbow: thinking
    p[H] = { ...legs(H), hand: [sd * 0.022, sp.chinY - 0.012, sp.chest + 0.040 + 0.004 * wob], bend: [sd * 0.5, -1, 0.1], curl: 0.9 };
    p[O] = { ...legs(O), hand: [sd * (d.shoulderW - 0.030), sp.waist + 0.030, sp.belly * 0.5 + 0.040], bend: [-sd * 0.7, -0.5, -0.4], curl: 1.0 };
    p.head = { nod: 0.05 + 0.015 * wob, turn: sd * 0.05 };
  } else if (g === 7) {             // showing off muscles
    both((k) => ({ arm: [0.05, 1.35], elbow: 0, tuck: 0, fore: [k * (0.18 + 0.06 * wob), 0.96, 0.12], grip: true }));
    p.breath = 1;
  } else if (g === 8) {             // an open hand, held out
    p[H] = { ...legs(H), arm: [0.16, 0.14], fore: [sd * 0.50, -0.10 + 0.06 * wob, 0.86], flat: true };
    p.head = { nod: 0.02, turn: -sd * 0.08 };
  } else if (g === 9) {             // both hands waving
    both((k) => ({ arm: [0.55, 0.75], elbow: 0, tuck: 0, fore: [k * (0.45 + 0.30 * wob * k), 0.85, 0.25], flat: true }));
    p.head = { nod: -0.04, turn: 0.12 * wob };
  } else if (g === 10) {            // pointing straight ahead
    p[H] = { ...legs(H), arm: [1.16 + 0.05 * wob, 0.10], elbow: 0.34, finger: true };
    p.lean = 0.07;
  } else if (g === 11) {            // a finger in the air: "fun fact"
    p[H] = { ...legs(H), arm: [0.35, 0.80], fore: [sd * (-0.10 + 0.05 * wob), 0.98, 0.14], finger: true };
    p.head = { nod: -0.03, turn: 0.04 * wob };
  } else if (g === 12) {            // arms folded: not impressed
    STANCES.folded(p, sp, d);
    p.head = { nod: -0.02 + 0.02 * wob, turn: 0.05 * wob };
    p.lean = -0.01;
  } else if (g === 13) {            // a hand cupped behind the ear: "what?"
    p[H] = { ...legs(H), hand: [sd * (d.headR[0] + 0.026), sp.headY - 0.070, 0.006 + 0.004 * wob], bend: [sd, -0.7, 0.3], flat: true, point: [0, 1, 0.25] };
    p.head = { nod: 0.04, turn: -sd * 0.22 };
    p.lean = 0.07;
  } else if (g === 14) {            // a shaken fist
    p[H] = { ...legs(H), arm: [0.70, 0.30], fore: [sd * -0.10, 0.92 + 0.05 * wob, 0.36], grip: true };
    p.head = { nod: -0.03, turn: 0.05 * wob };
    p.lean = 0.05;
  } else if (g === 15) {            // waving something away
    p[H] = { ...legs(H), arm: [0.34, 0.22], fore: [sd * (0.55 + 0.35 * wob), 0.20, 0.72], flat: true };
    p.head = { nod: 0.0, turn: -sd * 0.16 };
  } else if (g === 16) {            // wiping the brow with the back of a hand
    p[H] = { ...legs(H), hand: [sd * (0.012 + 0.016 * wob), sp.headY + d.headR[1] * 0.42, d.headR[2] + 0.030], bend: [sd, -0.3, 0.3], curl: 0.7, point: [-sd, 0.2, 0] };
    p.head = { nod: 0.06 };
  } else if (g === 17) {            // counting on the fingers: one hand held flat, the other ticking things off on it
    p[O] = { ...legs(O), hand: [-sd * 0.030, sp.waist + 0.050, sp.belly + 0.070], bend: [-sd, -0.5, -0.2], flat: true };
    p[H] = { ...legs(H), hand: [sd * 0.012, sp.waist + 0.074 + 0.012 * wob, sp.belly + 0.080], bend: [sd, -0.4, -0.2], finger: true, point: [-sd * 0.6, -0.6, 0.2] };
    p.head = { nod: 0.10 };
  } else if (g === 18) {            // both hands spread wide: "all of it", "everybody"
    both((k) => ({ arm: [0.25, 0.80], fore: [k * (0.86 + 0.06 * wob), 0.30, 0.40], flat: true }));
    p.breath = 1;
    p.head = { nod: -0.05, turn: 0.10 * wob };
  } else if (g === 19) {            // a thumb jerked back over the shoulder: "up there", "that way"
    p[H] = { ...legs(H), hand: [sd * (d.shoulderW + 0.004), -0.004 + 0.008 * wob, 0.060], bend: [sd * 0.35, -1, 0.35], grip: true, point: [0, 0.6, -0.8] };
    p.head = { nod: 0.0, turn: sd * 0.14 };
  } else if (g === 20) {            // a nod aside, toward something off to that side: the head turns and dips, the open hand follows low
    p[H] = { ...legs(H), arm: [0.28, 0.42], fore: [sd * 0.80, -0.22 + 0.04 * wob, 0.55], flat: true, thumb: [0, 1, 0] };
    p.head = { nod: 0.10 + 0.05 * Math.max(0, wob), turn: sd * 0.62 };
  } else if (g === 21) {            // a hand raised in blessing: the forearm upright, the hand open, its palm toward the listener
    p[H] = { ...legs(H), arm: [0.95 + 0.04 * wob, 0.80], fore: [sd * 0.08, 0.99, 0.06], flat: true, point: [0, 1, 0.04], thumb: [-sd, 0, 0] };
    p.head = { nod: 0.03 + 0.015 * wob };
  } else p.head = { nod: 0.035 * wob };
  void free;
  p.gesture = g;                                                      // (for whatever a character carries that belongs to one gesture)
  return p;
}

/** Reaching for something. k goes 0 to 1. low: bend down for it; otherwise reach out at chest height. o.hand is the hand that does it. */
export function reachPose(k, low = false, o = {}) {
  const p = standPose(0, o), H = o.hand === "L" ? "L" : "R", O = H === "R" ? "L" : "R";
  const held = (side) => o.keep && o.keep[side];                    // an arm that is carrying something stays where it is
  if (low && o.soft) {             // in a skirt: a dip at the knees and a small bow, not a deep bend
    const legs = { leg: [0.24 * k, 0.04], knee: 0.46 * k };
    p.lean = 0.40 * k;
    p[H] = { arm: [0.78 * k + 0.05, 0.08], elbow: 0.14, ...legs };
    p[O] = held(O) ? { ...p[O], ...legs } : { arm: [0.12 * k, 0.14], elbow: 0.3 * k + 0.14, ...legs };
    p.head = { nod: -0.16 * k };
  } else if (low) {
    p.lean = 0.62 * k;
    p[H] = { arm: [1.05 * k + 0.05, 0.08], elbow: 0.18, leg: [0.42 * k, 0.04], knee: 0.80 * k };
    p[O] = held(O) ? { ...p[O], leg: [0.42 * k, 0.04], knee: 0.80 * k } : { arm: [0.25 * k, 0.16], elbow: 0.5 * k + 0.14, leg: [0.42 * k, 0.04], knee: 0.80 * k };
    p.head = { nod: -0.25 * k };
  } else {
    p.lean = 0.14 * k;
    p[H] = { leg: p[H].leg, knee: p[H].knee, arm: [1.32 * k + 0.05, 0.06], elbow: 0.18 + 0.1 * k };
    p.head = { nod: 0.04 * k };
    p.reaching = k;                                                   // (for whatever a character holds out when their hand goes out: a date, say)
  }
  return p;
}

/**
 * Standing in prayer: the head bowed, the eyes shut, the hands folded together in front. It is a still pose.
 * o.dim is the build, o.lean the person's own way of standing. o.pray says how this person prays:
 *   high   how high the folded hands are: 0 at the belt, 0.5 at the breastbone, 1 under the chin (0.45 if not given)
 *   bow    how far the head is bowed (0.30)
 *   tight  true: elbows in, hands clasped hard, eyes squeezed shut, as a small child prays
 *   out    how much farther out in front of the body the hands are than usual
 */
export function prayPose(o = {}) {
  const d = o.dim || ADULT, sp = spots(d), how = o.pray || {}, high = how.high ?? 0.45, up = Math.max(0, high), low = Math.max(0, -high);
  const p = standPose(0, { dim: d, lean: (o.lean ?? 0.02) + (how.lean ?? 0.03) });
  // Where the two wrists are. (Hands folded lower than the belt: the arms hang nearly straight, a little forward, round the stomach.)
  const y = lerp(sp.waist + 0.016, sp.chinY - 0.040, high), z = lerp(sp.belly + 0.030, sp.chest + 0.030, up) + (how.out || 0);
  const apart = how.tight ? 0.022 : 0.030;
  for (const [k, sd] of [["R", 1], ["L", -1]]) {
    p[k] = {
      leg: p[k].leg, knee: p[k].knee, hand: [sd * apart, y, z], grip: true,
      bend: [sd * (how.tight ? 0.22 : lerp(0.70, 0.40, up) + 0.6 * low), -1, lerp(-0.55, -0.10, up) + 1.1 * low],
      point: [-sd * 0.80, lerp(-0.10, 0.62, up) - 1.4 * low, 0.16],
    };
  }
  p.breath = 0;
  p.head = { nod: how.bow ?? 0.30 };
  p.blink = true;
  if (how.tight) p.squeeze = true;
  p.praying = 1;
  return p;
}

/**
 * Dazzled: a sudden glare in the eyes (the low sun off a mirror). The body pulls back from it, the head turns a little
 * away and drops, the eyes are screwed shut, and one hand comes up flat to the brow to shade them; the other lifts a
 * little, half startled. A still pose. o: dim, lean, stance, and hand ("R" or "L"): the hand that shades.
 */
export function shadePose(o = {}) {
  const d = o.dim || ADULT, H = o.hand === "L" ? "L" : "R", sd = H === "R" ? 1 : -1, O = H === "R" ? "L" : "R";
  const p = standPose(0, { stance: o.stance, dim: d, lean: (o.lean ?? 0.02) - 0.07 });
  const keep = (q) => ({ leg: q.leg, knee: q.knee });
  p.twist = -sd * 0.12;
  p.breath = 1;                                                       // (the shoulders come up)
  p.head = { nod: 0.13, turn: -sd * 0.40 };                           // away from the shading hand, and down
  p[O] = { ...keep(p[O]), arm: [0.14, 0.20], elbow: 0.50 };
  // Where the brow is, with the head turned and bowed so: the hand lies flat over the eyes like the peak of a cap, from
  // the near temple across and a little forward, and the elbow stands out to the side, below it.
  const J = skeleton(d, p), hr = d.headR, cpi = Math.cos(J.headPitch), spi = Math.sin(J.headPitch);
  const headDir = (v) => turn([v[0], v[1] * cpi - v[2] * spi, v[1] * spi + v[2] * cpi], J.headYaw);
  const cL = Math.cos(J.lean), sL = Math.sin(J.lean), cT = Math.cos(J.twist), sT = Math.sin(J.twist);
  const toTorso = (w) => { const v1 = w[1] * cL + w[2] * sL, f = -w[1] * sL + w[2] * cL; return [w[0] * cT - f * sT, v1, w[0] * sT + f * cT]; };     // (torso() turned back)
  const wrist = toTorso(sub(add(J.head, headDir([sd * hr[0] * 1.02, hr[1] * 0.64, hr[2] * 0.80])), J.sh));
  p[H] = { ...keep(p[H]), hand: wrist, bend: [sd, -0.25, 0.35], flat: true, point: toTorso(headDir([-sd * 0.80, 0.02, 0.60])), thumb: toTorso(headDir([0, -1, 0])) };
  p.blink = true;
  p.squeeze = true;
  p.shading = 1;
  return p;
}

/** Part of the way from one pose to another, for easing into a pose and out of it: e runs from 0 (the first) to 1
    (the second). A hand travels from where it was to where it will be and the elbow follows; the rest goes in step. */
function between(d, a, b, e) {
  const A = skeleton(d, a), B = skeleton(d, b), num = (x, y) => lerp(x || 0, y || 0, e), late = e >= 0.5, p = { ...(late ? b : a) };
  for (const name of ["lean", "twist", "hipTwist", "sway", "rise", "shift", "breath"]) if (a[name] != null || b[name] != null) p[name] = num(a[name], b[name]);
  p.head = { nod: num(a.head && a.head.nod, b.head && b.head.nod), turn: num(a.head && a.head.turn, b.head && b.head.turn) };
  for (const k of ["R", "L"]) {
    const qa = a[k] || {}, qb = b[k] || {}, q = { ...(late ? qb : qa) };
    for (const name of ["arm", "elbow", "fore", "tuck"]) delete q[name];
    const w = mix(A[k].wLoc, B[k].wLoc, e);
    q.hand = [w[0], w[1], w[2] + 0.034 * Math.sin(Math.PI * e)];        // (a little forward on the way, so that a hand coming up from the side goes round the body and not through it)
    q.bend = sub(mix(A[k].eLoc, B[k].eLoc, e), A[k].sLoc);
    const la = qa.leg || [0, 0.03], lb = qb.leg || [0, 0.03];
    q.leg = [lerp(la[0], lb[0], e), lerp(la[1], lb[1], e)];
    q.knee = lerp(qa.knee ?? 0.02, qb.knee ?? 0.02, e);
    p[k] = q;
  }
  return p;
}

/** Heights of things to sit on, as fractions of a grown person's height: a step is a step whoever sits on it. */
const SEATS = { chair: 0.262, bench: 0.294, stool: 0.150, step: 0.105 };
const ARM_KEYS = ["arm", "elbow", "fore", "tuck", "hand", "bend", "grip", "curl", "finger", "point", "flat", "thumb"];

/**
 * Sitting. o.seat says on what:
 *   "ground"  cross-legged on the ground (the default)
 *   "chair"   on a seat of ordinary height, feet on the floor
 *   "bench"   on something a little higher: a child's feet hang
 *   "stool"   on something low, knees high and apart
 *   "step"    on a kerb or a step, feet on the ground below it, knees drawn up
 *   or a number: the height of the seat, as a fraction of a grown person's height.
 * o.gesture: 0 at rest; 1 talking, with this person's own main gesture (o.main); any other number is that
 * gesture from talkPose, made sitting down. o.dim is the build and o.height the sitter's height (1 for an adult).
 * o.lean, o.knees (how far apart) and o.feet (how far out in front) adjust the way of sitting; o.nod tips the head
 * (less than 0: looking up, as someone on the ground does at whoever stands talking to them).
 * The figure's anchor is the point on the ground under the hips.
 */
export function sitPose(f = 0, o = {}) {
  const br = 0.5 - 0.5 * Math.cos((2 * Math.PI * f) / 8), g = o.gesture || 0;
  const d = o.dim || ADULT, sp = spots(d);
  const seat = o.chair ? "chair" : o.seat || "ground";
  let p;
  if (seat !== "ground") {
    // The hips are at the height of the seat and the feet flat on the floor in front: the knees go where they must.
    const h = (typeof seat === "number" ? seat : SEATS[seat] ?? SEATS.chair) / (o.height || 1), low = h < 0.21, lowest = h < 0.15;
    const hipH = h + d.pelvisR[1] * 0.62, tilt = o.feet ?? (lowest ? 0.30 : low ? 0.14 : 0.05);          // how far the feet are set out in front of the knees
    const drop = hipH - d.ankleH - d.shin * Math.cos(tilt);                                             // how far the knee is below the hip (negative: above it)
    const pitch = Math.max(Math.acos(clamp1(drop / d.thigh)), 1.34);                                    // on a high seat the thighs stay level and the feet hang
    const roll = o.knees ?? (lowest ? 0.16 : low ? 0.34 : 0.10);
    const side = (sd) => ({
      leg: [pitch, roll], shin: [sd * Math.sin(roll) * 0.25, -Math.cos(tilt), Math.sin(tilt)], foot: 0, footYaw: low && !lowest ? 0.36 : 0.14,
      hand: [sd * (d.hipW + Math.sin(roll) * d.thigh * 0.80), sp.hip - Math.cos(pitch) * d.thigh * 0.80 + 0.042, Math.sin(pitch) * d.thigh * 0.80 + 0.012], bend: [sd, -0.3, -0.6], curl: 0.6,     // a hand resting on each knee
    });
    p = { seated: true, ground: d.hipY - d.pelvisR[1] * 0.62 - h, breath: br, lean: o.lean ?? (low ? 0.10 : -0.08), R: side(1), L: side(-1), head: { nod: o.nod ?? (low ? -0.02 : 0.06) } };
  } else {
    const side = (sd) => ({
      leg: [1.42, 0.86], shin: [-sd * 0.9, -0.12, -0.36], footYaw: -1.35, foot: 0,
      hand: [sd * 0.060, sp.hip + 0.070, sp.belly + 0.100], bend: [sd, -0.4, -0.5], curl: 0.7,         // hands come together over the lap
    });
    p = { seated: true, breath: br, lean: o.lean ?? 0.05, R: side(1), L: side(-1), head: { nod: o.nod ?? 0 } };
  }
  if (g) {
    // The gesture's arms on the sitting body: any arm the gesture does not use stays where it was resting.
    const which = g === 1 ? (o.main ?? 1) : g, opt = { dim: d, hand: o.hand }, t = talkPose(f, which, opt), still = standPose(f, opt);
    for (const k of ["R", "L"]) {
      if (ARM_KEYS.every((name) => JSON.stringify(t[k][name]) === JSON.stringify(still[k][name]))) continue;
      const q = { ...p[k] };
      for (const name of ARM_KEYS) { delete q[name]; if (t[k][name] !== undefined) q[name] = t[k][name]; }
      p[k] = q;
    }
    if (t.head) p.head = { nod: (p.head.nod || 0) + (t.head.nod || 0), turn: t.head.turn || 0 };
    if (which === 0) p.head = { nod: (p.head.nod || 0) + 0.035 * Math.sin((2 * Math.PI * f) / 6) };
  }
  return p;
}

/**
 * Sitting in prayer: the hands lifted a little in front, open, palms up; the head bowed and the eyes shut. It is this
 * person's own way of sitting (o: as for sitPose) with the arms and the head changed. o.pray says how:
 *   high   how high the hands are: 0 just over the lap, 1 level with the chin (0.70 if not given)
 *   out    how far in front of the chest (0.08)        apart   how far apart (0.050)        bow   how far the head is bowed (0.32)
 */
export function sitPrayPose(o = {}) {
  const d = o.dim || ADULT, sp = spots(d), how = o.pray || {}, high = how.high ?? 0.70;
  const p = sitPose(0, { ...o, gesture: 0 });
  const y = lerp(sp.waist - 0.010, sp.chinY - 0.030, high), z = sp.chest + (how.out ?? 0.08), x = how.apart ?? 0.050;
  for (const [k, sd] of [["R", 1], ["L", -1]]) {
    const q = { ...p[k] };
    for (const name of ARM_KEYS) delete q[name];
    p[k] = { ...q, hand: [sd * x, y, z], bend: [sd * 0.6, -1, -0.1], flat: true, point: [sd * 0.40, 0.75, 0.55], thumb: [sd, 0, 0] };
  }
  p.breath = 0;
  p.lean = (p.lean || 0) + (how.lean ?? 0.04);
  p.head = { nod: how.bow ?? 0.32 };
  p.blink = true;
  p.praying = 1;
  return p;
}

// ---------- each character's own way of doing these ----------
const DEFAULT_GESTURES = [0, 1, 2, 3];
/** An arm that is holding something keeps hold of it whatever else the body is doing. */
const holding = (spec, p) => {
  if (spec.hold) for (const k of ["R", "L"]) if (spec.hold[k]) {
    const q = { ...p[k] }, h = spec.hold[k];
    for (const name of ARM_KEYS) delete q[name];
    p[k] = { ...q, ...h };
    // `still: true`: the thing held is fixed in the picture (painted there by the scene), so the hand must not ride
    // up and down as the chest breathes: the shoulders move and the hand stays.
    if (h.still && h.hand) p[k].hand = [h.hand[0], h.hand[1] - 0.006 * (p.breath || 0), h.hand[2]];
  }
  return p;
};
/** Arms that a pose leaves alone go to this character's own resting places (spec.rest), if there are any. `plain` is the same pose with no gesture in it. */
const resting = (spec, p, plain) => {
  if (spec.rest) for (const k of ["R", "L"]) {
    if (!spec.rest[k] || (plain && !ARM_KEYS.every((name) => JSON.stringify(p[k][name]) === JSON.stringify(plain[k][name])))) continue;
    const q = { ...p[k] };
    for (const name of ARM_KEYS) delete q[name];
    p[k] = { ...q, ...spec.rest[k] };
  }
  return p;
};
const freeHand = (spec) => (spec.hold && spec.hold.R && !spec.hold.L ? "L" : spec.hand || "R");
const seatOf = (spec) => (spec.seated === true ? "ground" : spec.seated || "chair");
const mainGesture = (spec) => (spec.gestures || DEFAULT_GESTURES).find((g) => g !== 0) ?? 1;
/** Standing, walking, talking, reaching and sitting the way one particular character does them. */
export const poses = {
  stand: (spec, f) => holding(spec, resting(spec, standPose(f, { stance: spec.stance, dim: spec.dim, lean: spec.lean }))),
  walk: (spec, ph) => holding(spec, walkPose(ph, spec.walk)),
  /** `seed` is any whole number; the same seed always gives this character the same gesture. */
  gesture: (spec, seed) => { const list = spec.gestures || DEFAULT_GESTURES; return list[seed % list.length]; },
  talk: (spec, f, g) => { const o = { stance: spec.stance, dim: spec.dim, lean: spec.lean, hand: freeHand(spec) }; return holding(spec, resting(spec, talkPose(f, g, o), standPose(f, o))); },
  /** (A figure in the game is in prayer when its "act" is one called "pray", counted from 2 to 3 so that it is never
      taken for a reach: see Figure.pray in js/engine/cast.js.) */
  /** (A figure in the game is shading its eyes when its "act" is one called "shade", counted from 4 to 5: see Figure.shade.) */
  reach: (spec, k, low) => low === "pray" ? poses.pray(spec, k >= 2 ? k - 2 : k) : low === "shade" ? poses.shade(spec, k >= 4 ? k - 4 : k) : holding(spec, reachPose(k, low, { stance: spec.stance, dim: spec.dim, soft: !!spec.bottom && (spec.bottom.kind === "skirt" || spec.bottom.kind === "kilt"), hand: freeHand(spec), keep: spec.hold })),
  /** In prayer, the way this character prays (spec.pray: see prayPose, and sitPrayPose for someone found sitting).
      k eases from standing, or sitting, (0) into the pose (1). */
  pray: (spec, k = 1) => {
    const seated = !!spec.seated;
    const full = holding(spec, seated ? sitPrayPose({ ...sitHow(spec), pray: spec.pray }) : prayPose({ dim: spec.dim, lean: spec.lean, pray: spec.pray }));
    if (k >= 1) return full;
    const from = seated ? poses.sit(spec, 0) : poses.stand(spec, 0);
    if (!(k > 0)) return from;
    const e = k * k * (3 - 2 * k), p = holding(spec, between(spec.dim, from, full, e));
    p.blink = e > 0.5; p.squeeze = !!full.squeeze && e > 0.5; p.praying = e;
    return p;
  },
  /** Dazzled, a hand flat to the brow (see shadePose): for someone standing. k comes up from standing (0) to the pose (1), quickly. */
  shade: (spec, k = 1) => {
    const o = { stance: spec.stance, dim: spec.dim, lean: spec.lean, hand: freeHand(spec) };
    const full = holding(spec, resting(spec, shadePose(o), standPose(0, o)));
    if (k >= 1) return full;
    const from = poses.stand(spec, 0);
    if (!(k > 0)) return from;
    const e = 1 - (1 - k) * (1 - k), p = holding(spec, between(spec.dim, from, full, e));
    p.blink = p.squeeze = e > 0.35; p.shading = e;
    return p;
  },
  /** o.gesture: 0 at rest; 1 talking, with this character's own main gesture; another number is that gesture. o.seat overrides what they sit on. */
  sit: (spec, f, o = {}) => {
    const how = sitHow(spec, o);
    return holding(spec, resting(spec, sitPose(f, how), sitPose(f, { ...how, gesture: 0 })));
  },
};
/** How this character sits: their own `sit` settings, with whatever `o` changes. */
function sitHow(spec, o = {}) {
  return { ...(spec.sit || {}), ...o, dim: spec.dim, height: spec.height, seat: o.seat || (spec.sit && spec.sit.seat) || seatOf(spec), main: o.main ?? mainGesture(spec), hand: freeHand(spec) };
}

// =====================================================================================
// Getting up and sitting down, and the small things people do where they are
// =====================================================================================
// Someone found sitting can stand up and sit down again (Figure.sit in js/engine/cast.js), and everyone has a few small
// movements of their own (Figure.fidget). The rig draws every moment of them; the engine plays them on the game clock.

const VIEW_TILT = 0.22;                                                 // (as in drawFigure: how far down the picture a step toward us goes)
const smooth = (k) => k * k * (3 - 2 * k);
const span = (k, a, b) => (k <= a ? 0 : k >= b ? 1 : (k - a) / (b - a));
const cloneP = (p) => ({ ...p, R: { ...(p.R || {}) }, L: { ...(p.L || {}) }, head: { ...(p.head || {}) } });
/** A pose with one arm changed: the leg on that side as it was, the arm as `q` says. */
const withArm = (p, side, q) => { const o = { ...p[side] }; for (const name of ARM_KEYS) delete o[name]; p[side] = { ...o, ...q }; return p; };
/** From a point in a figure's own space back to its torso's space (measured from the middle of the shoulders), for a skeleton J. */
const torsoOf = (J) => {
  const cL = Math.cos(J.lean), sL = Math.sin(J.lean), cT = Math.cos(J.twist), sT = Math.sin(J.twist);
  return (w) => { const v = sub(w, J.sh), v1 = v[1] * cL + v[2] * sL, f = -v[1] * sL + v[2] * cL; return [v[0] * cT - f * sT, v1, v[0] * sT + f * cT]; };
};
/** How someone is when nothing is happening: sitting if they are found sitting, else standing. */
const restOf = (spec) => (spec.seated ? poses.sit(spec, 0) : poses.stand(spec, 0));

/** The same person on their feet: someone found sitting, standing, with their own `stood` settings (what they hold, and how). */
const UPS = new WeakMap();
export function upOf(spec) {
  if (!spec || !spec.seated) return spec;
  let up = UPS.get(spec);
  if (!up) { up = { ...spec, ...(spec.stood || {}), seated: false, sit: undefined }; UPS.set(spec, up); }
  return up;
}

/** How someone found sitting gets up: `forward`, how far in front of their seat they stand once up (in their own heights;
    nothing for someone on the ground, who gets up where they sat), and `ms`, how long it takes (spec.riseMs if given). */
const RISES = new WeakMap();
export function riseOf(spec) {
  let r = RISES.get(spec);
  if (r) return r;
  const how = sitHow(spec), ground = how.seat === "ground";
  const J0 = skeleton(spec.dim, poses.sit(spec, 0));
  const feet = (J0.R.ankle[2] + J0.L.ankle[2]) / 2 - J0.hipC[2];
  r = { ground, feet, forward: ground ? 0 : Math.max(0, feet * 0.55), ms: spec.riseMs ?? (ground ? 1250 : spec.height < 0.85 ? 760 : 1000) };
  RISES.set(spec, r);
  return r;
}

/** Where someone stands once up, from the point they sat on: [right, down] in picture pixels, for a figure `size` pixels tall facing `yawDeg`. */
export function standOffset(spec, yawDeg, size) {
  const f = riseOf(spec).forward * size, th = yawDeg * DEG;
  return [f * Math.sin(th), f * Math.cos(th) * VIEW_TILT];
}

/** The seat that is drawn with someone (the goldsmith's stool, the old-timer's lawn chair), by itself, where they sat:
    for while they are up. Anchored as their seated picture is, at the point under the seat. */
export function drawSeat(spec, yawDeg, size) {
  return drawFigure(spec, poses.sit(spec, 0), yawDeg, size, { seat: true });
}

/** A leg reaching from its hip to a place for its ankle (in the figure's own space, unturned), the knee bending toward
    `hint`: the `leg` angles and `shin` direction that skeleton() takes, and where the knee is. */
function legTo(d, s, hip, ankle, hint) {
  const a = d.thigh, b = d.shin, v = sub(ankle, hip), far = Math.hypot(v[0], v[1], v[2]);
  const L = Math.min(a + b - 0.001, Math.max(Math.abs(a - b) + 0.001, far)), dir = far > 1e-6 ? mul(v, 1 / far) : [0, -1, 0];
  const along = (a * a - b * b + L * L) / (2 * L), out = Math.sqrt(Math.max(0, a * a - along * along));
  const side = unit(sub(hint, mul(dir, dot3(hint, dir))));
  const knee = add(hip, add(mul(dir, along), mul(side, out))), end = add(hip, mul(dir, L));
  const t = unit(sub(knee, hip));
  return { leg: [Math.atan2(t[2], -t[1]), Math.asin(clamp1(s * t[0]))], shin: unit(sub(end, knee)), knee };
}

/**
 * Getting up from the seat: k runs from 0 (sitting, as they always sit) to 1 (standing, as they always stand); played
 * backwards it is sitting down. The picture is anchored where their feet will be once they are up (standOffset says
 * where that is from the seat), and the seat is not in it: a seat drawn with them is drawn apart (drawSeat) and stays put.
 * From a chair, a stool or a step: the feet come back, the weight comes forward over them, the hands go to the knees,
 * and the legs push the body up as it straightens. From the ground: lean forward, hands to the knees, the legs come out
 * of the cross and under the body, and up. `inPlace`: the same where the seat is (no step forward: someone who walked
 * back to their seat and sits down on it).
 */
function risePose(spec, k, inPlace = false) {
  const R = riseOf(spec), up = upOf(spec), d = spec.dim, Fs = inPlace ? 0 : R.forward;
  const S0 = poses.sit(spec, 0), S4 = poses.stand(up, 0);
  if (!(k > 0)) return { ...S0, shift: (S0.shift || 0) - Fs, noSeat: true, rising: 0 };
  if (k >= 1) return S4;
  const J0 = skeleton(d, S0), J4 = skeleton(d, S4), ground = R.ground;
  const less = (v) => [v[0], v[1], v[2] - Fs];                          // (from the point under the seat to the point under the feet)
  const L0 = S0.lean || 0, L4 = S4.lean || 0, H0 = J0.hipC[1], H4 = J4.hipC[1];
  const hip0 = less(J0.hipC), hip4 = J4.hipC;
  // the phases, as fractions of the whole: still sitting until `seatK`; the hands on the knees from `onK` to `offK`
  const seatK = ground ? 0.26 : 0.30, offK = ground ? 0.76 : 0.68;
  let hc, lean, seated, ankleOf, hintOf, yawOf;
  if (!ground) {
    if (k < seatK) {
      // still on the seat: the feet come back under the knees, the weight comes forward
      const e = smooth(k / seatK);
      seated = true; hc = hip0; lean = lerp(L0, 0.48, e);
      ankleOf = (s) => { const a0 = less(J0[s].ankle), a4 = J4[s].ankle; return [lerp(a0[0], (a0[0] + a4[0]) / 2, e), lerp(a0[1], a4[1], e), lerp(a0[2], 0, e)]; };
      hintOf = (s) => unit(add(mul(unit(sub(J0[s].knee, J0[s].hip)), 1 - e), mul([s === "R" ? 0.25 : -0.25, 0.1, 1], e)));
      yawOf = (s) => lerp(S0[s].footYaw ?? 0.24, 0.20, e);
    } else {
      // up: the hips go forward over the feet, then up; the body straightens
      const e = (k - seatK) / (1 - seatK), ez = smooth(span(e, 0, 0.55)), ey = smooth(span(e, 0.04, 0.90));
      seated = false;
      hc = [lerp(hip0[0], hip4[0], ey), lerp(H0, H4, ey), lerp(hip0[2], hip4[2], ez)];
      lean = lerp(0.48, L4, smooth(span(e, 0.30, 1))) + 0.07 * Math.sin(Math.PI * span(e, 0, 0.6));
      ankleOf = (s) => { const a0 = less(J0[s].ankle), a4 = J4[s].ankle, m = [(a0[0] + a4[0]) / 2, a4[1], 0]; return mix(m, a4, smooth(e)); };
      hintOf = (s) => [s === "R" ? 0.20 : -0.20, 0.1, 1];
      yawOf = (s) => lerp(0.20, S4[s].footYaw ?? 0.24, e);
    }
  } else {
    const Hsq = Math.max(H0 + 0.05, d.thigh * 0.95 + d.ankleH * 0.6);                   // the height of the hips in a squat
    const sq = (s) => [(s === "R" ? 1 : -1) * (d.hipW + 0.035), J4[s].ankle[1], 0.035];     // the feet, under the body, squatting
    if (k < seatK) {
      // still sitting cross-legged: the weight comes forward, the hands go to the knees
      const e = smooth(k / seatK);
      seated = true; hc = hip0; lean = lerp(L0, 0.40, e);
      ankleOf = (s) => J0[s].ankle; hintOf = (s) => sub(J0[s].knee, J0[s].hip); yawOf = (s) => S0[s].footYaw ?? -1.35;
    } else if (k < 0.55) {
      // the legs come out of the cross and under the body, and the hips come up off the ground into a squat
      const e = smooth(span(k, seatK, 0.55));
      seated = false; hc = [0, lerp(H0, Hsq, e), lerp(hip0[2], -0.045, e)]; lean = lerp(0.40, 0.62, e);
      ankleOf = (s) => mix(J0[s].ankle, sq(s), e);
      hintOf = (s) => unit(add(mul(unit(sub(J0[s].knee, J0[s].hip)), 1 - e), mul([s === "R" ? 0.35 : -0.35, 0.5, 1], e)));
      yawOf = (s) => lerp(S0[s].footYaw ?? -1.35, 0.30, e);
    } else {
      // and up
      const e = smooth(span(k, 0.55, 1));
      seated = false; hc = [lerp(0, hip4[0], e), lerp(Hsq, H4, e), lerp(-0.045, hip4[2], e)]; lean = lerp(0.62, L4, e);
      ankleOf = (s) => mix(sq(s), J4[s].ankle, e);
      hintOf = (s) => [s === "R" ? 0.30 : -0.30, 0.25, 1];
      yawOf = (s) => lerp(0.30, S4[s].footYaw ?? 0.24, e);
    }
  }
  const all = smooth(k);
  const p = {
    seated, noSeat: true, rising: k, breath: 0, lean, twist: 0, hipTwist: 0, sway: hc[0], shift: hc[2],
    head: { nod: lerp((S0.head && S0.head.nod) || 0, (S4.head && S4.head.nod) || 0, all) - 0.35 * (lean - lerp(L0, L4, all)), turn: 0 },
  };
  // the legs, by reaching from the hips to where the feet are
  const knees = {};
  let flat = 0;
  for (const s of ["R", "L"]) {
    const sd = s === "R" ? 1 : -1, hipJ = add(hc, [sd * d.hipW, 0, 0]), leg = legTo(d, sd, hipJ, ankleOf(s), hintOf(s));
    knees[s] = leg.knee;
    flat += leg.leg[0] / 2;
    p[s] = { leg: leg.leg, shin: leg.shin, knee: 0, foot: 0, footYaw: yawOf(s) };
  }
  if (!seated && flat > 0.80 + lean * 0.3) p.lap = true;                // (a skirt lies on thighs that are still nearly level)
  // the arms: what they hold, they hold; a free hand goes to its knee to push, and then to its place standing
  const sh = add(hc, [0, (d.shoulderY - d.hipY) * Math.cos(lean), (d.shoulderY - d.hipY) * Math.sin(lean)]);
  const toT = torsoOf({ lean, twist: 0, sh });
  const onK = 0.04;
  for (const s of ["R", "L"]) {
    const sd = s === "R" ? 1 : -1, a0 = J0[s], a4 = J4[s], held = !!((spec.hold && spec.hold[s]) || (up.hold && up.hold[s]));
    const q0 = S0[s] || {}, q4 = S4[s] || {}, flags = (q) => { const f = {}; for (const n of ["grip", "curl", "finger", "point", "flat", "thumb"]) if (q[n] !== undefined) f[n] = q[n]; return f; };
    let hand, bend, f;
    if (held && up.takeUp != null) {
      // a thing taken up off the ground on the way (Lot's staff, lying beside him: `takeUp` in people.js): the hand goes
      // down to where it will stand, takes it there (from `takeUp` on it is in the hand, planted), and climbs up it
      const T = up.takeUp, wr = J4[s].wrist, low = 0.22, side = [sd * 0.60, 0.10, -0.50];
      if (k < T) { const e = smooth(span(k, 0.06, T)); hand = mix(a0.wLoc, toT([wr[0], low, wr[2]]), e); bend = mix(sub(a0.eLoc, a0.sLoc), side, e); f = e < 0.6 ? flags(q0) : { curl: 0.70 }; }
      else { const e = smooth(span(k, T, 1)); hand = mix(toT([wr[0], lerp(low, wr[1], e), wr[2]]), a4.wLoc, smooth(span(k, 0.85, 1))); bend = mix(side, sub(a4.eLoc, a4.sLoc), e); f = flags(q4); }
    } else if (held) {
      const e = smooth(span(k, 0.20, 0.90));
      hand = mix(a0.wLoc, a4.wLoc, e); bend = sub(mix(a0.eLoc, a4.eLoc, e), a0.sLoc); f = flags(e < 0.5 ? q0 : q4);
    } else {
      const knee = toT(add(knees[s], [0, 0.030, -0.014])), kneeBend = [sd * 0.55, -0.15, -0.55];
      if (k < seatK) { const e = smooth(span(k, onK, seatK)); hand = mix(a0.wLoc, knee, e); bend = mix(sub(a0.eLoc, a0.sLoc), kneeBend, e); f = e < 0.5 ? flags(q0) : { curl: 0.75 }; }
      else if (k < offK) { hand = knee; bend = kneeBend; f = { curl: 0.75 }; }
      else { const e = smooth(span(k, offK, 1)); hand = mix(knee, a4.wLoc, e); bend = mix(kneeBend, sub(a4.eLoc, a4.sLoc), e); f = e < 0.5 ? { curl: 0.75 } : flags(q4); }
    }
    p[s] = { ...p[s], hand, bend, ...f };
  }
  return p;
}

// ---------- small movements ----------
// Each is a few key poses made from the person's own resting pose (standing, or sitting if they are found sitting), at
// points from 0 to 1 of its time, eased one into the next. The first and the last are the resting pose itself, so a
// small movement starts and ends exactly where the person was. `hold`: where a movement that can be held stops, for as
// long as it is held (Figure.fidget(name, { hold: true })).
const STAND_FIDGETS = ["shift", "look", "neck", "stretch"], SIT_FIDGETS = ["shift", "look", "knees", "stretch"];
const free = (o) => ["R", "L"].filter((s) => !o.held(s));
const nodOf = (p) => (p.head && p.head.nod) || 0;
const FIDGETS = {
  /** shifting the weight onto the other leg (sitting: shifting on the seat) */
  shift: { ms: 1900, make(o) {
    const b = o.base;
    if (o.seated) return [[0, b], [0.32, { ...cloneP(b), sway: 0.016, twist: 0.16, lean: (b.lean || 0) + 0.05, head: { nod: nodOf(b) + 0.03, turn: -0.10 } }], [0.66, { ...cloneP(b), sway: -0.010, twist: -0.08, head: { nod: nodOf(b), turn: 0.06 } }], [1, b]];
    const dir = (b.sway || 0) < -0.004 ? -1 : 1, W = dir > 0 ? "L" : "R", F = dir > 0 ? "R" : "L", p = cloneP(b);
    p.sway = -0.022 * dir; p.hipTwist = 0.08 * dir; p.lean = (b.lean || 0) + 0.01;
    p[W] = { ...p[W], leg: [-0.03, 0.04], knee: 0.02 }; p[F] = { ...p[F], leg: [0.18, 0.08], knee: 0.36, footYaw: 0.50 };
    p.head = { nod: nodOf(b) + 0.02, turn: 0.06 * dir };
    return [[0, b], [0.30, p], [0.72, p], [1, b]];
  } },
  /** looking about: a long look one way, then the other and up */
  look: { ms: 2400, make(o) {
    const b = o.base, one = cloneP(b), two = cloneP(b);
    one.head = { nod: nodOf(b) - 0.02, turn: 0.55 }; two.head = { nod: nodOf(b) - 0.15, turn: -0.45 };
    if (!o.seated && !o.still) { one.twist = 0.06; two.twist = -0.05; }
    return [[0, b], [0.18, one], [0.42, one], [0.60, two], [0.84, two], [1, b]];
  } },
  /** a hand to the back of the neck, rubbing it, the head down */
  neck: { ms: 2100, make(o) {
    const b = o.base, s = o.held(o.H) ? o.O : o.H, sd = s === "R" ? 1 : -1, hr = o.d.headR;
    if (o.held(s)) return [[0, b], [1, b]];
    const at = (dx, dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.14, turn: -sd * 0.08 } }, s, { hand: [sd * (0.032 + dx), o.sp.headY - hr[1] * 1.30 + dy, -(hr[2] * 0.70)], bend: [sd, 0.55, 0.15], curl: 0.5 });
    const n1 = at(0, 0), n2 = at(-0.012, 0.010);
    return [[0, b], [0.26, n1], [0.42, n2], [0.58, n1], [0.74, n2], [1, b]];
  } },
  /** a stretch: the free arms up over the head, the body back */
  stretch: { ms: 2200, make(o) {
    const b = o.base, up = (roll, elbow) => { const p = { ...cloneP(b), lean: (b.lean || 0) - (o.seated ? 0.03 : 0.06), breath: 1, head: { nod: nodOf(b) - 0.15 } }; for (const s of free(o)) withArm(p, s, { arm: [2.80, roll], elbow, flat: true }); return p; };
    return [[0, b], [0.38, up(0.32, 0.22)], [0.60, up(0.46, 0.12)], [1, b]];
  } },
  /** sitting: rubbing the knees */
  knees: { ms: 2000, make(o) {
    const b = o.base, rub = (back) => { const p = { ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) + 0.05 } }; for (const s of free(o)) withArm(p, s, { hand: o.toTorso(add(o.J[s].knee, [0, 0.032, -0.012 - back])), bend: [s === "R" ? 0.6 : -0.6, -0.2, -0.5], curl: 0.6 }); return p; };
    const k1 = rub(0), k2 = rub(0.040);
    return [[0, b], [0.24, k1], [0.40, k2], [0.56, k1], [0.72, k2], [1, b]];
  } },
  // ---- each person's own ----
  /** the overseer: taps his staff on the ground, twice */
  tap: { ms: 1700, make(o) {
    const b = o.base, s = o.held("R") ? "R" : "L", q = b[s];
    const up = { ...withArm(cloneP(b), s, { ...q, hand: add(q.hand, [0, 0.060, 0.006]) }), staffLift: 0.060, head: { nod: nodOf(b) + 0.06 } }, down = { ...cloneP(b), staffLift: 0, head: { nod: nodOf(b) + 0.06 } };
    return [[0, b], [0.16, up], [0.30, down], [0.46, up], [0.60, down], [1, b]];
  } },
  /** the guard: leans on his staff, both hands on it */
  lean: { ms: 3600, hold: 0.30, make(o) {
    const b = o.base, p = cloneP(b), sp = o.sp;
    withArm(p, "R", { hand: [0.150, -0.090, 0.120], bend: [0.6, -1, -0.3], grip: true });
    withArm(p, "L", { hand: [0.120, -0.030, 0.128], bend: [-0.4, -1, -0.2], grip: true });
    p.sway = 0.012; p.lean = (b.lean || 0) + 0.06; p.hipTwist = -0.05; p.head = { nod: nodOf(b) + 0.06, turn: -0.12 };
    p.L = { ...p.L, leg: [0.12, 0.06], knee: 0.24 };
    void sp;
    return [[0, b], [0.30, p], [0.76, p], [1, b]];
  } },
  /** the senator: settles the folds of his toga over his left arm */
  toga: { ms: 2300, make(o) {
    const b = o.base, sp = o.sp, lift = withArm(cloneP(b), "L", { hand: [-0.112, -0.165, 0.112], bend: [-0.6, -0.5, -0.6], curl: 0.9 });
    const t1 = withArm(cloneP(lift), "R", { hand: [-0.070, -0.040, sp.chest + 0.040], bend: [1, -0.4, 0.1], curl: 0.8 });
    const t2 = withArm(cloneP(lift), "R", { hand: [-0.095, -0.115, sp.chest + 0.050], bend: [1, -0.5, 0.0], curl: 0.8 });
    t1.head = t2.head = { nod: nodOf(b) + 0.10, turn: -0.18 };
    return [[0, b], [0.28, t1], [0.50, t2], [0.66, t2], [1, b]];
  } },
  /** the date seller: hitches his basket up on his hip */
  hitch: { ms: 1500, make(o) {
    const b = o.base, q = b.L, p = withArm(cloneP(b), "L", { ...q, hand: add(q.hand, [0.014, 0.060, -0.004]) });
    p.sway = -0.022; p.hipTwist = 0.08; p.R = { ...p.R, knee: (p.R.knee || 0) + 0.14 }; p.head = { nod: nodOf(b) + 0.04, turn: 0.10 };
    return [[0, b], [0.30, p], [0.48, p], [1, b]];
  } },
  /** the washerwoman: takes the wet cloth from her shoulder and wrings it out */
  wring: { ms: 2600, make(o) {
    const b = o.base, sp = o.sp, w = (tw) => {
      const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.12 } };
      withArm(p, "R", { hand: [0.030, sp.waist + 0.012, sp.belly + 0.105], bend: [1, -0.6, -0.3], grip: true, point: [-1, tw, 0.3] });
      withArm(p, "L", { hand: [-0.030, sp.waist + 0.002, sp.belly + 0.100], bend: [-1, -0.6, -0.3], grip: true, point: [1, -tw, 0.3] });
      return p;
    };
    const w1 = w(0.35), w2 = w(-0.35);
    return [[0, b], [0.20, w1], [0.38, w2], [0.56, w1], [0.74, w2], [1, b]];
  } },
  /** the snack-bar keeper: wipes down his counter */
  wipe: { ms: 2400, make(o) {
    const b = o.base, sp = o.sp, s = o.spec.fidgetHand || (o.held("R") ? "L" : "R"), sd = s === "R" ? 1 : -1;
    const at = (x) => { const p = withArm({ ...cloneP(b), lean: (b.lean || 0) + 0.10, head: { nod: nodOf(b) + 0.14 } }, s, { hand: [sd * x, sp.waist + 0.035, sp.belly + 0.175], bend: [sd, -0.4, -0.4], flat: true, point: [0, -0.2, 1] }); return p; };
    const w1 = at(0.110), w2 = at(-0.010);
    return [[0, b], [0.18, w1], [0.36, w2], [0.54, w1], [0.72, w2], [1, b]];
  } },
  /** the doorkeeper: folds his arms */
  fold: { ms: 3600, hold: 0.22, make(o) {
    const b = o.base, p = cloneP(b);
    STANCES.folded(p, o.sp, o.d);
    p.lean = (b.lean || 0) - 0.02; p.head = { nod: nodOf(b) - 0.04 };
    return [[0, b], [0.22, p], [0.80, p], [1, b]];
  } },
  /** a hauler: rolls his shoulders */
  roll: { ms: 1900, make(o) {
    const b = o.base, r1 = { ...cloneP(b), breath: 1, twist: 0.14, lean: (b.lean || 0) - 0.04, head: { nod: nodOf(b) - 0.08, turn: -0.10 } }, r2 = { ...cloneP(b), breath: 0.2, twist: -0.14, lean: (b.lean || 0) + 0.05, head: { nod: nodOf(b) + 0.06, turn: 0.10 } };
    return [[0, b], [0.25, r1], [0.50, r2], [0.75, r1], [1, b]];
  } },
  /** the man in gray: looks at his watch */
  watch: { ms: 2200, make(o) {
    const b = o.base, sp = o.sp, p = withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.20, turn: -0.28 } }, "L", { hand: [-0.010, sp.waist + 0.095, sp.chest + 0.105], bend: [-1, -0.6, -0.2], curl: 0.6, point: [1, 0.15, 0.25] });
    return [[0, b], [0.30, p], [0.72, p], [1, b]];
  } },
  /** the man in gray: straightens his tie */
  tie: { ms: 1800, make(o) {
    const b = o.base, sp = o.sp, at = (dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) - 0.07 } }, "R", { hand: [0.008, -0.044 + dy, sp.chest + 0.034], bend: [1, -0.6, -0.1], grip: true, point: [0, 1, 0.3] });
    const t1 = at(0), t2 = at(-0.014);
    return [[0, b], [0.30, t1], [0.45, t2], [0.60, t1], [1, b]];
  } },
  /** the old-timer, standing: rubs the small of his back and arches it */
  back: { ms: 2400, make(o) {
    const b = o.base, sp = o.sp, at = (lean) => { const p = { ...cloneP(b), lean: (b.lean || 0) - lean, head: { nod: nodOf(b) - 0.10 } }; for (const s of free(o)) withArm(p, s, { hand: [(s === "R" ? 1 : -1) * 0.046, sp.waist - 0.030, -(sp.back + 0.032)], bend: [s === "R" ? 0.7 : -0.7, -0.3, -0.7], curl: 0.6 }); return p; };
    const b1 = at(0.08), b2 = at(0.13);
    return [[0, b], [0.30, b1], [0.55, b2], [0.75, b1], [1, b]];
  } },
  /** the scribe: trims his pen with a little knife */
  pen: { ms: 2400, make(o) {
    const b = o.base, sp = o.sp, at = (dx) => {
      const p = { ...cloneP(b), head: { nod: nodOf(b) + 0.18 } };
      withArm(p, "R", { hand: [0.022, -0.108, sp.chest + 0.115], bend: [1, -0.6, -0.2], grip: true, point: [-0.4, 0.8, 0.5] });
      withArm(p, "L", { hand: [-0.020 + dx, -0.118, sp.chest + 0.108], bend: [-1, -0.6, -0.2], grip: true, point: [0.9, 0.1, 0.4] });
      return p;
    };
    const p1 = at(0), p2 = at(0.016);
    return [[0, b], [0.24, p1], [0.38, p2], [0.52, p1], [0.66, p2], [1, b]];
  } },
  /** the goldsmith: holds something small up to the light and turns it */
  light: { ms: 2400, make(o) {
    const b = o.base, sp = o.sp, at = (px) => withArm({ ...cloneP(b), head: { nod: nodOf(b) - 0.08, turn: -0.22 } }, "L", { hand: [-0.040, sp.headY - 0.020, sp.chest + 0.085], bend: [-0.6, -1, -0.1], curl: 0.9, point: [px, 1, 0.35] });
    const l1 = at(0.35), l2 = at(-0.40);
    return [[0, b], [0.28, l1], [0.48, l2], [0.68, l1], [1, b]];
  } },
  /** the lamp boy: a yawn, an arm up, the mouth wide */
  yawn: { ms: 2200, make(o) {
    const b = o.base, p = { ...cloneP(b), breath: 1, blink: true, mouth: 2, head: { nod: nodOf(b) - 0.20 } };
    for (const s of free(o)) withArm(p, s, { arm: [2.60, 0.45], elbow: 0.45, flat: true });
    return [[0, b], [0.34, p], [0.64, p], [1, b]];
  } },
  /** the clerk: rubs his tired eyes */
  eyes: { ms: 2000, make(o) {
    const b = o.base, sp = o.sp, hr = o.d.headR, s = o.held("L") ? "R" : "L", sd = s === "R" ? 1 : -1;
    const at = (dx) => withArm({ ...cloneP(b), blink: true, head: { nod: nodOf(b) + 0.14 } }, s, { hand: [sd * (0.010 + dx), sp.headY - hr[1] * 0.02, hr[2] + 0.030], bend: [sd, -0.3, 0.3], curl: 0.6, point: [-sd, 0.2, 0] });
    const e1 = at(0), e2 = at(0.014);
    return [[0, b], [0.30, e1], [0.45, e2], [0.60, e1], [1, b]];
  } },
  /** the soothsayer: strokes his beard */
  beard: { ms: 2400, make(o) {
    const b = o.base, sp = o.sp, s = o.held("L") ? "R" : "L", sd = s === "R" ? 1 : -1;
    const at = (dy) => withArm({ ...cloneP(b), head: { nod: nodOf(b) - 0.04 } }, s, { hand: [sd * 0.004, sp.chinY - 0.030 + dy, sp.chest + 0.062], bend: [sd, -0.6, 0], curl: 0.8, point: [0, -1, 0.3] });
    const b1 = at(0), b2 = at(-0.034);
    return [[0, b], [0.28, b1], [0.46, b2], [0.62, b1], [0.80, b2], [1, b]];
  } },
  /** the street boy: scratches his head */
  scratch: { ms: 1900, make(o) {
    const b = o.base, sp = o.sp, hr = o.d.headR, s = o.held("R") ? "L" : "R", sd = s === "R" ? 1 : -1;
    const at = (dx) => withArm({ ...cloneP(b), head: { nod: nodOf(b) + 0.10, turn: sd * 0.12 } }, s, { hand: [sd * (0.030 + dx), sp.headY + hr[1] * 0.78, -0.010], bend: [sd, 0.6, 0], curl: 0.9 });
    const s1 = at(0), s2 = at(0.012);
    return [[0, b], [0.28, s1], [0.40, s2], [0.52, s1], [0.64, s2], [1, b]];
  } },
  /** the old-timer, sitting: a hand to the brim of his hat */
  hat: { ms: 2000, make(o) {
    const b = o.base, sp = o.sp, hr = o.d.headR;
    const p = withArm({ ...cloneP(b), head: { nod: nodOf(b) - 0.06 } }, "R", { hand: [0.026, sp.headY + hr[1] * 0.42, hr[2] + 0.048], bend: [1, -0.4, 0.2], curl: 0.6, point: [-0.3, 0.3, 1] });
    return [[0, b], [0.34, p], [0.66, p], [1, b]];
  } },
};

/** The small movements that suit someone, as they are now (sitting or standing): everyone's, and their own (spec.fidgets). */
export function fidgetsOf(spec) {
  const own = spec.fidgets || {}, mine = (spec.seated ? own.sit : own.stand) || [];
  const list = own.only ? mine : [...(spec.seated ? SIT_FIDGETS : STAND_FIDGETS), ...mine];
  return list.filter((n, i) => FIDGETS[n] && list.indexOf(n) === i && !(own.not || []).includes(n));
}
/** How long a small movement takes, in ms of game time (0: there is no such movement). */
export const fidgetMs = (spec, name) => (FIDGETS[name] ? FIDGETS[name].ms : 0);
/** Where a small movement that can be held stops while it is held (a fraction of its time), or null. */
export const fidgetHold = (name) => (FIDGETS[name] && FIDGETS[name].hold) || null;

const FKEYS = new WeakMap();
function fidgetKeys(spec, name) {
  let m = FKEYS.get(spec);
  if (!m) FKEYS.set(spec, (m = new Map()));
  let keys = m.get(name);
  if (!keys) {
    const d = spec.dim, base = restOf(spec), H = freeHand(spec), J = skeleton(d, base);
    const o = { spec, d, sp: spots(d), base, seated: !!spec.seated, H, O: H === "R" ? "L" : "R", J, toTorso: torsoOf(J), held: (s) => !!(spec.hold && spec.hold[s]), still: !!(spec.hold && Object.values(spec.hold).some((h) => h && h.still)) };
    keys = FIDGETS[name].make(o);
    m.set(name, keys);
  }
  return keys;
}
/** The step of a small movement to draw at u (0 to 1) when it is shown in `n` steps: a moment it is held for gives one picture. */
export function fidgetStep(spec, name, u, n) {
  if (!FIDGETS[name] || !(u > 0) || !(u < 1)) return u >= 1 ? n : 0;
  const keys = fidgetKeys(spec, name);
  let i = 0;
  while (i + 2 < keys.length && keys[i + 1][0] <= u) i++;
  return keys[i][1] === keys[i + 1][1] ? Math.round(keys[i][0] * n) : Math.round(u * n);
}

Object.assign(poses, {
  /** Getting up from their seat (k 0 to 1), or, backwards, sitting down: see risePose. */
  rise: (spec, k, inPlace = false) => risePose(spec, k, inPlace),
  /** One moment (u from 0 to 1) of one of this person's small movements: see FIDGETS. */
  fidget: (spec, name, u) => {
    const F = FIDGETS[name], base = restOf(spec);
    if (!F || !(u > 0) || !(u < 1)) return base;
    const keys = fidgetKeys(spec, name);
    let i = 0;
    while (i + 2 < keys.length && keys[i + 1][0] <= u) i++;
    const [u0, a] = keys[i], [u1, b] = keys[i + 1], e = smooth(span(u, u0, u1));
    const p = a === b ? cloneP(a) : between(spec.dim, a, b, e);
    if (a.staffLift != null || b.staffLift != null) p.staffLift = lerp(a.staffLift || 0, b.staffLift || 0, e);
    p.fidget = name; p.fu = u;
    return p;
  },
});

/** How tall a character is as they are usually found (standing, or sitting on whatever they sit on), in their own
    heights: 1 for someone standing, about 0.6 for someone cross-legged on the ground. For placing words over a head. */
/**
 * A team portrait: head and shoulders, n pixels square, drawn with that many pixels (not a figure enlarged), facing the
 * viewer, the face feature by feature at that size (bigFace). spec.portrait (optional) frames it: { head: how much of
 * the height the skull takes, y: where the middle of the head sits, from the top }.
 */
export function portraitOf(spec, n = 84, yawDeg = 0) {
  const how = spec.portrait || {}, pose = spec.seated ? poses.sit(spec, 0) : poses.stand(spec, 0);
  const size = ((how.head ?? 0.56) * n) / (spec.dim.headR[1] * 2);
  const [hx, hy] = headPoint(spec, pose, yawDeg, size);
  return drawFigure(spec, pose, yawDeg, size, { window: [Math.round(hx - n / 2), Math.round(hy - n * (how.y ?? 0.42)), n, n], portrait: true });
}

/** Where the middle of someone's head is in a picture drawn by drawFigure (the same spec, pose, way and size), measured
    from the anchor: [x right, y down]. For a portrait, which frames the head. */
export function headPoint(spec, pose, yawDeg, size) {
  const J = skeleton(spec.dim, pose), th = yawDeg * DEG, c = Math.cos(th), s = Math.sin(th), v = J.head;
  const dp = (v[0] * s + v[2] * c) * size;
  return [(-v[0] * c + v[2] * s) * size, -v[1] * size + dp * 0.22];
}

export function tallOf(spec) {
  const J = skeleton(spec.dim, spec.seated ? poses.sit(spec, 0) : poses.stand(spec, 0));
  return J.head[1] + spec.dim.headR[1] * 1.2;
}

// =====================================================================================
// Things to wear and to carry
// =====================================================================================
// Each of these takes the tools a character's `extras` is given (see drawFigure), so a costume is a few
// lines in people.js. Places on the body are given in the torso's own space, measured from the middle
// of the shoulders, as hands are.

/** A staff held upright in one hand, its foot on the ground. o: mat, top (how high it reaches, in heights), r,
    knob (a material: a ball on top), crook (true: a curled top), out and fwd (how far its foot is set from under the hand). */
function staff(c, side, o = {}) {
  const { J, limb, ball, parts } = c, g = J[side].palm, r = o.r ?? 0.0075, raised = c.pose.staffLift || 0, top = (o.top ?? 1.0) + raised;      // (staffLift: lifted off the ground, as when it is tapped)
  // Standing, its foot is on the ground. Walking, it is carried: lifted clear of the ground and tipped a little
  // forward, rising and falling with the steps, so that it never slides along the ground.
  const gait = c.pose.gait, a = gait ? 2 * Math.PI * gait.phase : 0;
  const lift = gait ? 0.030 + 0.010 * Math.cos(2 * a) : 0, back = gait ? 0.034 + 0.014 * Math.sin(a) : 0;
  const foot = [g[0] + (o.out || 0), 0.004 + lift + raised, g[2] + (o.fwd || 0) - back], k = (top - g[1]) / Math.max(0.05, g[1] - foot[1]);
  const head = [g[0] + (g[0] - foot[0]) * k, top, g[2] + (g[2] - foot[2]) * k];
  limb(foot, head, r * 1.1, r * 0.9, o.mat, { part: parts.HELD });
  if (o.knob) ball(head, [r * 2, r * 2, r * 2], o.knob, { part: parts.HELD });
  if (o.crook) {
    const at = (fwd, up) => [head[0], head[1] + up, head[2] + fwd];
    const pts = [at(0, 0), at(0.012, 0.026), at(0.040, 0.030), at(0.058, 0.008), at(0.044, -0.016), at(0.026, -0.006)];
    for (let i = 0; i + 1 < pts.length; i++) limb(pts[i], pts[i + 1], r * 0.9, r * 0.85, o.mat, { part: parts.HELD });
  }
  return { foot, head };
}

/** A broad collar of beads lying on the shoulders and chest. o.rows: materials, from the neck outward (three or four). */
function collar(c, o) {
  const { J, ball, d, tw, S, parts } = c, rows = o.rows;
  ball(add(J.sh, J.torso([0, -(o.drop ?? 0.032), 0])), [o.wide ?? 0.094, o.deep ?? 0.052, d.trunkTop[1] + 0.016], rows[0], {
    part: parts.COLLAR, bias: S * 0.026,
    fn: (ux, uy) => { const q = ux * ux * 0.8 + (uy + 1.05) ** 2; return q < 0.62 ? null : q < 1.15 ? undefined : q < 2.0 ? rows[1] : q < 3.1 || !rows[3] ? rows[2] || rows[0] : rows[3]; },
  }, tw);
}

/** A cloth tied over the hair and knotted at the back of the neck. o: mat, brow (how low on the forehead), nape, tails (how long: 0 for none), knot. */
function headcloth(c, o) {
  const { ball, limb, onHead, headPt, hp, d, hy, parts } = c, hr = d.headR, g = o.bulk ?? 1.10, brow = o.brow ?? 0.50, nape = o.nape ?? 0.80;
  const band = o.fold ? shifted(o.mat, 1) : null;                      // the turned-up edge of it, round the brow
  ball(headPt([0, 0.004, 0]), [hr[0] * g, hr[1] * g, hr[2] * g], o.mat, {
    part: parts.HAT, fn: (ux, uy, uz) => { const q = onHead(ux, uy, uz), edge = q[2] > 0 ? brow - 0.12 * (1 - q[2]) : brow - 0.12 + nape * q[2]; return q[1] > edge ? (band && q[1] < edge + 0.16 ? band : undefined) : null; },
  }, hy);
  const ky = brow - 0.12 - nape + 0.10, kz = -Math.sqrt(Math.max(0.05, 1 - ky * ky)) - 0.06;
  if (o.knot !== false) ball(hp(0, ky, kz), [0.017, 0.015, 0.015], shifted(o.mat, 1), { part: parts.HAT }, hy);
  const tails = o.tails ?? 0.5;
  if (tails) for (const sd of [1, -1]) limb(hp(sd * 0.10, ky - 0.04, kz - 0.02), hp(sd * 0.24, ky - 0.04 - tails, kz - 0.06), 0.009, 0.006, o.mat, { part: parts.HAT });
}

/**
 * The Roman toga: one great length of white wool, over the left shoulder, round the back, under the right
 * arm, across the chest and up over the left shoulder again, so that the right arm is free and the left
 * carries the folds. (The wrap round the legs is the character's own long skirt, in the same cloth.)
 * o: mat, hood (true: pulled up over the head, as a man did who was about a god's business), edge (a border color).
 */
function toga(c, o) {
  const { J, limb, ball, fold, onHead, headPt, hp, trunkAt, trunkFacing, wide, deep, d, S, hy, tw, fine, under, cloth, parts } = c;
  const mat = o.mat, T = (x, y, z) => add(J.sh, J.torso([x, y, z])), chest = d.trunkTop[1], lie = { [parts.TORSO]: under, [parts.BELT]: under, [parts.SKIRT]: under, [parts.PELVIS]: under, [parts.COLLAR]: under };
  const sw = d.shoulderW;
  // the sweep across the chest, from under the right arm up to the left shoulder, and the same across the back
  for (const face of [1, -1]) {
    const a = trunkAt(d.waistY - 0.030, face > 0 ? 1.20 : Math.PI - 1.20, 0.006), m = trunkAt(d.waistY + 0.070, face > 0 ? 0.10 : Math.PI - 0.10, 0.012), b = T(-(sw - 0.016), 0.014, face * 0.022);
    limb(a, m, 0.046, 0.043, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.2, depth: 0.5 });
    limb(m, b, 0.043, 0.034, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.2, depth: 0.5 });
    if (fine) for (const dy of [0.022, 0.002, -0.018]) {
      const facing = trunkFacing(face > 0 ? 0 : Math.PI);
      fold(add(a, [0, dy + 0.016, 0]), add(m, [0, dy, 0]), parts.DRAPE, facing);
      fold(add(m, [0, dy, 0]), add(b, [0, dy - 0.010, 0]), parts.DRAPE, facing);
    }
    if (o.edge) {                                                       // a colored border along the lower edge of the sweep
      const on = { ...lie, [parts.DRAPE]: under };
      limb(add(a, [0, -0.038, 0]), add(m, [0, -0.036, 0]), 0.0055, 0.0055, o.edge, { part: parts.DRAPE, over: on, bias: cloth * 3 });
      limb(add(m, [0, -0.036, 0]), add(b, [0, -0.030, 0]), 0.0055, 0.0055, o.edge, { part: parts.DRAPE, over: on, bias: cloth * 3 });
    }
  }
  // the weight of it on the left shoulder, and round the left arm, which holds the folds up
  ball(add(J.L.shoulder, J.torso([0.010, 0.014, 0])), [0.046, 0.040, 0.052], mat, { part: parts.DRAPE }, tw);
  const A = J.L, r = d.armR;
  limb(A.shoulder, A.elbow, r[0] + 0.016, r[1] + 0.018, mat, { part: parts.DRAPE2 });
  limb(A.elbow, mix(A.elbow, A.wrist, 0.80), r[1] + 0.018, r[2] + 0.018, mat, { part: parts.DRAPE2, hem: true });
  // what hangs from the arm, and the two ends: one down the front from the left shoulder, one down the back
  const hang = mix(A.elbow, A.wrist, 0.45), low = Math.min(J.L.knee[1], J.R.knee[1]) - 0.050;
  limb(add(hang, [0, -0.010, 0]), [hang[0], Math.max(0.10, low + 0.040), hang[2]], 0.032, 0.040, mat, { part: parts.DRAPE2, hem: true, depth: 0.6 });
  for (const face of [1, -1]) {
    const fall = [0.038, 0.020], foot = [0.046, 0.022], r0 = wide(fall), r1 = wide(foot);
    const from = T(-(sw - 0.022), -0.020, face * (chest * 0.80)), to = [from[0] - 0.006, Math.max(0.08, low - (face > 0 ? 0 : 0.050)), from[2] + face * 0.016];
    limb(from, to, r0, r1, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.6, depth: deep(fall) / r0, hem: true });
    if (fine) for (const dx of [0.012, -0.012]) fold(add(from, [dx, -0.030, 0]), add(to, [dx * 1.4, 0.012, 0]), parts.DRAPE, trunkFacing(face > 0 ? -0.5 : Math.PI + 0.5));
    if (o.edge) limb(add(from, [0.026, 0, face * 0.004]), add(to, [0.032, 0, face * 0.004]), 0.006, 0.007, o.edge, { part: parts.DRAPE, over: { ...lie, [parts.DRAPE]: under }, bias: cloth * 3.2 });
  }
  if (o.hood) {
    // drawn up over the back of the head, standing a little clear of the brow, and falling to the shoulders at each side
    const hr = d.headR;
    ball(headPt([0, 0.006, -0.004]), [hr[0] * 1.20, hr[1] * 1.16, hr[2] * 1.18], mat, {
      part: parts.HAT, fn: (ux, uy, uz) => { const q = onHead(ux, uy, uz); return q[2] < 0.30 + 0.45 * Math.max(0, q[1]) ? undefined : null; },
    }, hy);
    for (const sd of [1, -1]) limb(hp(sd * 1.02, -0.30, 0.10), T(sd * (sw - 0.020), 0.010, 0.012), 0.030, 0.034, mat, { part: parts.HAT });
    limb(hp(0, -0.40, -0.80), T(0, -0.050, -(d.trunkTop[1] + 0.010)), 0.052, 0.060, mat, { part: parts.HAT });
  }
}

/** A short cloak pinned on the right shoulder: it hangs down the back and over the left arm. o: mat, len (how far below the shoulders), pin (a material). */
function cloak(c, o) {
  const { J, limb, ball, fold, wide, deep, trunkFacing, d, tw, fine, under, cloth, parts } = c;
  const mat = o.mat, T = (x, y, z) => add(J.sh, J.torso([x, y, z])), len = o.len ?? 0.36, back = d.trunkTop[1], sw = d.shoulderW;
  const lie = { [parts.TORSO]: under, [parts.BELT]: under, [parts.SKIRT]: under, [parts.PELVIS]: under, [parts.ARM.L]: under, [parts.SLEEVE.L]: under };
  const top = [0.108, 0.030], low = [0.120, 0.040], r0 = wide(top), r1 = wide(low);
  limb(T(0, -0.012, -(back * 0.70)), T(0, -len, -(back * 0.90)), r0, r1, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2, depth: deep(top) / r0, hem: true });     // down the back
  limb(T(-(sw - 0.004), 0.004, 0), add(J.L.elbow, J.torso([-0.004, -0.050, 0])), 0.054, 0.060, mat, { part: parts.DRAPE2, hem: true, bias: cloth * 2 });                 // over the left shoulder and arm
  ball(add(J.L.shoulder, J.torso([0.006, 0.010, 0])), [0.052, 0.040, 0.056], mat, { part: parts.DRAPE2, bias: cloth * 2 }, tw);
  // gathered on the right shoulder: a band of it comes over the top of the shoulder from the back to the pin
  limb(T(sw - 0.026, 0.004, back * 0.60), T(sw - 0.034, 0.012, 0), 0.027, 0.030, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2 });
  limb(T(sw - 0.034, 0.012, 0), T(sw - 0.050, -0.004, -(back * 0.74)), 0.030, 0.034, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2 });
  limb(T(sw - 0.030, -0.004, back * 0.62), T(-(sw - 0.030), -0.030, back * 0.80), 0.024, 0.030, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.2, depth: 0.5 });   // its edge across the chest
  if (o.pin) ball(T(sw - 0.034, 0.000, back * 0.66), [0.011, 0.011, 0.011], o.pin, { part: parts.HELD, bias: cloth * 4 });
  if (fine) for (const x of [-0.040, 0.034]) fold(T(x, -0.050, -(back + 0.020)), T(x * 1.2, -len + 0.020, -(back + 0.030)), parts.DRAPE, trunkFacing(Math.PI));
}

/**
 * A mantle: a plain oblong of wool worn over the tunic, as people of the East wore it. It lies over the left
 * shoulder, goes round the back and under the right arm, comes across the front and is thrown back over the left
 * shoulder, so the right arm is free. Smaller and closer than a toga; an end of it hangs in front of the left
 * shoulder and the other behind.
 * o: mat; band (a material: dark bands woven across the cloth near each end, and a line along its edge);
 *    len and front (how far below the shoulders the end behind, and the end in front, hang); fringe (a material: a
 *    fringe of threads on each end).
 */
function mantle(c, o) {
  const { J, limb, ball, fold, trunkAt, trunkFacing, wide, deep, d, tw, fine, under, cloth, parts } = c;
  const mat = o.mat, T = (x, y, z) => add(J.sh, J.torso([x, y, z])), chest = d.trunkTop[1], sw = d.shoulderW;
  const lie = { [parts.TORSO]: under, [parts.BELT]: under, [parts.SKIRT]: under, [parts.PELVIS]: under, [parts.COLLAR]: under };
  // the sweep across the front, from the right hip up to the left shoulder, and the same across the back
  for (const face of [1, -1]) {
    const a = trunkAt(d.waistY - 0.022, face > 0 ? 1.25 : Math.PI - 1.25, 0.004), m = trunkAt(d.waistY + 0.060, face > 0 ? 0.12 : Math.PI - 0.12, 0.010), b = T(-(sw - 0.018), 0.010, face * 0.020);
    limb(a, m, 0.036, 0.034, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.2, depth: 0.5 });
    limb(m, b, 0.034, 0.027, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.2, depth: 0.5 });
    const facing = trunkFacing(face > 0 ? 0 : Math.PI);
    if (fine) { fold(add(a, [0, 0.014, 0]), add(m, [0, 0.006, 0]), parts.DRAPE, facing); fold(add(m, [0, 0.006, 0]), add(b, [0, -0.004, 0]), parts.DRAPE, facing); }
    if (o.band && facing[0] * Math.sin(c.th) + facing[2] * Math.cos(c.th) > 0.30) {       // the dark line woven along its edge: drawn where that side of him is toward us (it is lost in the folds under the right arm)
      const on = { ...lie, [parts.DRAPE]: under }, a2 = mix(a, m, 0.52);
      limb(add(a2, [0, -0.024, 0]), add(m, [0, -0.023, 0]), 0.0048, 0.0048, o.band, { part: parts.DRAPE, over: on, bias: cloth * 3 });
      limb(add(m, [0, -0.023, 0]), add(b, [0, -0.019, 0]), 0.0048, 0.0044, o.band, { part: parts.DRAPE, over: on, bias: cloth * 3 });
    }
  }
  // where it lies on the left shoulder and over the top of that arm
  ball(add(J.L.shoulder, J.torso([0.010, 0.012, 0])), [0.042, 0.034, 0.052], mat, { part: parts.DRAPE }, tw);
  // (and down that side of the body, between the end that hangs in front and the end that hangs behind)
  limb(T(-(sw - 0.016), -0.016, 0), T(-(sw - 0.010), -(d.shoulderY - d.waistY) + 0.012, 0), 0.046, 0.050, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2, depth: 0.62, squareEnd: true });
  limb(J.L.shoulder, mix(J.L.shoulder, J.L.elbow, 0.72), d.armR[0] + 0.013, d.armR[1] + 0.015, mat, { part: parts.DRAPE2, hem: true });
  // its two ends, hanging: each with two dark bands across it near the bottom
  const bands = o.band ? (t) => ((t > 0.74 && t < 0.81) || (t > 0.86 && t < 0.93) ? o.band : undefined) : null;
  for (const face of [1, -1]) {
    const len = face > 0 ? (o.front ?? 0.21) : (o.len ?? 0.40), fall = [0.034, 0.017], foot = [0.040, 0.019], r0 = wide(fall), r1 = wide(foot);
    const from = T(-(sw - 0.022), -0.014, face * (chest * 0.80)), to = [from[0] - 0.004, from[1] - len, from[2] + face * 0.012];
    limb(from, to, r0, r1, mat, { part: parts.DRAPE, over: lie, bias: cloth * 2.6, depth: deep(fall) / r0, hem: true, fn: bands });
    if (fine) fold(add(from, [0.008, -0.030, 0]), add(to, [0.010, len * 0.30, 0]), parts.DRAPE, trunkFacing(face > 0 ? -0.5 : Math.PI + 0.5));
    if (o.fringe) {                                                     // a fringe: the warp threads left long and knotted, hanging from the end
      const by = c.S >= 64 ? 1 : 0, low = [to[0], to[1] - 0.026, to[2]];
      limb(add(to, [0, 0.004, 0]), low, r1, r1 * 0.96, o.fringe, { part: parts.DRAPE, over: lie, bias: cloth * 2.6, depth: deep(foot) / r1, squareStart: true, squareEnd: true,
        fn: (t, nx, ny, x) => (t > 0.25 && (x + by) % 2 ? null : undefined) });
    }
  }
}

/** A low stool under someone sitting. o: mat, r (half its width). */
function stool(c, o = {}) {
  if (!c.pose.seated || c.pose.noSeat) return;                          // (it stays where it is when they get up: see drawSeat)
  const { J, ball, limb, parts } = c, y = J.seatY, hip = J.hipC, r = o.r ?? 0.072;
  ball([hip[0], y - 0.010, hip[2] - 0.010], [r, 0.012, r], o.mat, { part: parts.EXTRA3 });
  for (const [dx, dz] of [[-1, -0.6], [1, -0.6], [0, 1]]) limb([hip[0] + dx * r * 0.6, y - 0.016, hip[2] - 0.010 + dz * r * 0.6], [hip[0] + dx * r * 0.95, 0.004, hip[2] - 0.010 + dz * r * 0.95], 0.008, 0.007, shifted(o.mat, 1), { part: parts.EXTRA3 });
}

/** Clothes and props that several characters share. */
export const wear = { staff, collar, headcloth, toga, cloak, mantle, stool };

export { ramp, pack, shifted, add, sub, mul, mix, turn, unit, lerp };
