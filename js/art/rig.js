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
// Directions are angles: 0 faces the viewer, 90 faces screen right, 180 faces
// away, 270 faces screen left.
//
// Measurements are fractions of the character's own height.

import { Surface, ramp, pack, shifted } from "./pix.js";

const DEG = Math.PI / 180;

/** Art pixels tall for a full-height adult at scale 1. The stage is 640x400 art pixels. */
export const BASE = 128;

// ---------- small vector helpers (x: the character's right, y: up, z: forward) ----------
const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
const mix = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
const unit = (v) => { const n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / n, v[1] / n, v[2] / n]; };
/** Turn about the upright axis. A positive angle swings "forward" toward the character's right. */
const turn = (v, a) => { const c = Math.cos(a), s = Math.sin(a); return [v[0] * c + v[2] * s, v[1], -v[0] * s + v[2] * c]; };
/** Which way a limb points: hanging straight down, swung forward by `pitch`, and out to its own side by `roll`. */
const dirOf = (pitch, roll, side) => [side * Math.sin(roll), -Math.cos(roll) * Math.cos(pitch), Math.cos(roll) * Math.sin(pitch)];
const lerp = (a, b, t) => a + (b - a) * t;
const clamp1 = (v) => Math.max(-1, Math.min(1, v));

// ---------- proportions ----------
export const ADULT = {
  headR: [0.062, 0.077, 0.070],            // half width, half height, half depth
  neckY: 0.836, shoulderY: 0.802, waistY: 0.590, hipY: 0.485,
  shoulderW: 0.102, shoulderDrop: 0.046, hipW: 0.056,     // the arm hangs from a point this far out from the spine and this far below the shoulder line
  trunkTop: [0.112, 0.074], trunkLow: [0.104, 0.078], bellyFwd: 0,   // [half width, half depth] at the chest and at the waist; bellyFwd carries the waist forward.
                                                                     // An optional trunkHem gives the size at the bottom edge of the shirt.
  pelvisR: [0.104, 0.066, 0.080],
  upperArm: 0.166, foreArm: 0.150, armR: [0.035, 0.030, 0.022], handR: 0.028,      // armR: at the shoulder, the elbow and the wrist
  thigh: 0.228, shin: 0.216, legR: [0.056, 0.042, 0.031], ankleH: 0.041, foot: 0.112, footR: 0.024,
};

export const CHILD = {
  headR: [0.080, 0.094, 0.086],
  neckY: 0.790, shoulderY: 0.758, waistY: 0.565, hipY: 0.470,
  shoulderW: 0.100, shoulderDrop: 0.042, hipW: 0.056,
  trunkTop: [0.110, 0.078], trunkLow: [0.106, 0.082], bellyFwd: 0,
  pelvisR: [0.104, 0.064, 0.080],
  upperArm: 0.152, foreArm: 0.136, armR: [0.033, 0.029, 0.023], handR: 0.027,
  thigh: 0.220, shin: 0.208, legR: [0.054, 0.042, 0.032], ankleH: 0.042, foot: 0.122, footR: 0.026,
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
  headR: [0.064, 0.078, 0.071],
  shoulderW: 0.086, shoulderDrop: 0.044, hipW: 0.054,
  trunkTop: [0.096, 0.068], trunkLow: [0.079, 0.060],
  pelvisR: [0.100, 0.064, 0.078],
  armR: [0.029, 0.025, 0.019], handR: 0.024,
  legR: [0.052, 0.038, 0.026], foot: 0.100, footR: 0.021,
};

// part numbers, used for the thin shadows where one part overlaps another
const HEAD = 1, HAIR = 2, TORSO = 3, PELVIS = 4, ARM = { R: 5, L: 6 }, LEG = { R: 7, L: 8 }, FOOT = { R: 9, L: 10 }, EXTRA = 11, HAT = 12, NECK = 13;
const SHORTS = { R: 14, L: 15 }, SLEEVE = { R: 16, L: 17 };          // cloth that ends part-way down a limb, so its hem can cast a line
const EXTRA2 = 18;                                                    // a second carried thing, so that it shows against the first
const SKIRT = 19, EXTRA3 = 20;
/** Part numbers, for code that looks at a finished figure (the head-and-shoulders portraits, for one). */
export const PARTS = { HEAD, HAIR, HAT, NECK, TORSO };

const SHADOW = { tones: [pack("#00000048"), pack("#00000048"), pack("#00000048"), pack("#00000048")], soft: true, flat: 1 };

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
  const nod = lean + ((p.head && p.head.nod) || 0);
  J.head = add(J.neck, mul([0, Math.cos(nod), Math.sin(nod)], 0.010 + d.headR[1]));
  J.headYaw = tw * 0.4 + ((p.head && p.head.turn) || 0);

  for (const [key, s] of [["R", 1], ["L", -1]]) {
    const q = p[key] || {};
    const arm = q.arm || [0.03, 0.10], leg = q.leg || [0, 0.03];
    const shoulder = add(J.sh, torso([s * d.shoulderW, -(d.shoulderDrop ?? 0.046), 0]));
    const uDir = torso(dirOf(arm[0], arm[1], s));
    const elbow = add(shoulder, mul(uDir, d.upperArm));
    const fDir = q.fore ? unit(torso(q.fore)) : torso(dirOf(arm[0] + (q.elbow ?? 0.12), arm[1] * 0.5 - (q.tuck || 0), s));
    const wrist = add(elbow, mul(fDir, d.foreArm));
    const tip = add(wrist, mul(fDir, d.handR * 1.5));

    const hip = add(hipC, turn([s * d.hipW, 0, 0], ht));
    const tDir = turn(dirOf(leg[0], leg[1], s), ht);
    const knee = add(hip, mul(tDir, d.thigh));
    const sDir = q.shin ? unit(turn(q.shin, ht)) : turn(dirOf(leg[0] - (q.knee ?? 0.02), leg[1], s), ht);
    const ankle = add(knee, mul(sDir, d.shin));
    const fp = q.foot || 0, fy = ht + s * (q.footYaw ?? 0.16);
    const footDir = turn([0, Math.sin(fp), Math.cos(fp)], fy);
    const heel = add(ankle, add([0, -d.ankleH * 0.48, 0], mul(footDir, -0.020)));
    const toe = add(heel, mul(footDir, d.foot));
    J[key] = { shoulder, elbow, wrist, tip, hip, knee, ankle, heel, toe };
  }

  // Stand the figure on the ground: whatever is lowest touches y = 0.
  let low = Infinity;
  for (const k of ["R", "L"]) low = Math.min(low, J[k].heel[1] - d.footR, J[k].toe[1] - d.footR * 0.8);
  if (p.seated) low = Math.min(low, hipC[1] - d.pelvisR[1]);
  const drop = (v) => { v[1] -= low; };
  for (const k of ["hipC", "sh", "neck", "head"]) drop(J[k]);
  for (const k of ["R", "L"]) for (const j of Object.values(J[k])) drop(j);
  J.spine = spine;                                                     // a point on the spine at a given height (hipC has been moved, so this follows)
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

/**
 * Draw a character.
 * spec: who they are (see people.js). pose: how they are standing. yawDeg: the way they face.
 * size: their height in art pixels.
 * Returns a Surface whose anchor (ox, oy) is the point on the ground between the feet.
 */
export function drawFigure(spec, pose, yawDeg, size) {
  const d = spec.dim, S = size;
  const W = (Math.ceil(S * (spec.span || 1.05)) + 14) & ~1, H = Math.ceil(S * (spec.tall || 1.2)) + 12;
  const ox = W / 2, oy = H - 6;
  const sf = new Surface(W, H, ox, oy);
  const th = yawDeg * DEG, c = Math.cos(th), s = Math.sin(th), TILT = 0.22;
  // character space to picture space. The camera looks slightly down, so nearer things sit lower.
  const P = (v) => { const dp = (v[0] * s + v[2] * c) * S; return [ox + (-v[0] * c + v[2] * s) * S, oy - v[1] * S + dp * TILT, dp]; };
  const R = (r) => Math.max(0.85, r * S);
  const J = skeleton(d, pose);
  const fine = S >= 84, coarse = S < 52;

  const limb = (a, b, ra, rb, mat, o) => {
    const A = P(a), B = P(b);
    // hem (far end) and cuff (near end): the cloth stops in a straight edge, unless the limb points so nearly at the viewer that its end is what shows
    if (o && (o.hem || o.cuff)) { const long = Math.hypot(B[0] - A[0], B[1] - A[1]), min = o.hemMin ?? 1.4; o = { ...o, squareEnd: !!o.hem && long > R(rb) * min, squareStart: !!o.cuff && long > R(ra) * min }; }
    sf.limb(A[0], A[1], A[2], B[0], B[1], B[2], R(ra), R(rb), mat, o);
  };
  // r3 = [half width, half height, half depth] in the part's own frame, which is turned by `psi` from the body
  const ball = (ctr, r3, mat, o = {}, psi = 0) => {
    const C = P(ctr), a = th + psi, ca = Math.cos(a), sa = Math.sin(a);
    sf.ball(C[0], C[1], C[2], R(Math.hypot(r3[0] * ca, r3[2] * sa)), R(r3[1]), R(Math.hypot(r3[0] * sa, r3[2] * ca)), mat, o);
  };
  // From a point on a ball as seen (ux right, uy down, uz toward the viewer) back to the part's own directions.
  const own = (ux, uy, uz, psi) => { const a = th + psi, ca = Math.cos(a), sa = Math.sin(a); return [-ux * ca + uz * sa, -uy, ux * sa + uz * ca]; };
  // A shape that is wider than it is deep, [half width, half depth], looks narrower or wider as the figure turns.
  const widthAt = (r2, turned) => Math.hypot(r2[0] * Math.cos(th + turned), r2[1] * Math.sin(th + turned));
  const depthAt = (r2, turned) => Math.hypot(r2[0] * Math.sin(th + turned), r2[1] * Math.cos(th + turned));

  const skin = spec.skin, top = spec.top || {}, bottom = spec.bottom || {}, socks = spec.socks, shoes = spec.shoes || {};
  const hair = spec.hair || {}, face = spec.face || {};
  const breath = pose.breath || 0;

  // ----- shadow on the ground -----
  sf.oval(ox, oy - 0.5, S * (spec.shadow || 0.19), Math.max(1.5, S * 0.034), -1e8, SHADOW);

  // ----- legs -----
  for (const k of ["R", "L"]) {
    const L = J[k], part = LEG[k];
    const longLegs = bottom.kind === "trousers";
    const legMat = longLegs ? bottom.mat : spec.tights || skin;
    limb(L.hip, L.knee, d.legR[0], d.legR[1], legMat, { part });
    limb(L.knee, L.ankle, d.legR[1], d.legR[2], legMat, { part });
    if (bottom.kind === "shorts") {
      const len = bottom.len ?? 0.7;
      limb(L.hip, mix(L.hip, L.knee, len), d.legR[0] + 0.012, lerp(d.legR[0], d.legR[1], len) + 0.014, bottom.mat, { part: SHORTS[k], hem: true });
    } else if (bottom.kind === "kilt") {
      const len = bottom.len ?? 0.92;
      limb(L.hip, mix(L.hip, L.knee, len), d.legR[0] + 0.010, lerp(d.legR[0], d.legR[1], len) + 0.012, bottom.mat, { part: PELVIS });
    }
    if (socks) {
      const from = socks.from ?? 0.55, stripes = socks.stripes, thick = socks.thick ?? 0.004;
      limb(mix(L.knee, L.ankle, from), L.ankle, lerp(d.legR[1], d.legR[2], from) + thick, d.legR[2] + thick + 0.001, socks.mat, {
        part, cuff: true, fn: stripes && fine ? (t) => (t > 0.10 && t < 0.24 ? stripes[0] : t > 0.34 && t < 0.48 ? stripes[1] : undefined) : null,
      });
    }
    // feet
    const fpart = FOOT[k], pumps = shoes.kind === "pumps";
    const footMat = shoes.kind === "bare" ? skin : shoes.kind === "sandals" ? (socks ? socks.mat : skin) : shoes.mat;
    if (shoes.sole) limb(add(L.heel, [0, -0.008, 0]), add(L.toe, [0, -0.008, 0]), d.footR * 0.92, d.footR * 0.74, shoes.sole, { part: fpart, bias: -0.8 });
    limb(L.heel, L.toe, d.footR, d.footR * 0.78, footMat, {
      part: fpart, flatten: 1.3,
      fn: shoes.kind === "sandals" ? (t) => ((t > 0.30 && t < 0.56) || t < 0.08 ? shoes.mat : undefined)
        : pumps ? (t) => (t > 0.26 && t < 0.60 ? legMat : undefined)                                   // a court shoe: the top of the foot shows
        : shoes.stripe && fine ? (t) => (t > 0.38 && t < 0.52 ? shoes.stripe : undefined) : null,
    });
    limb(L.ankle, mix(L.ankle, L.heel, 0.8), d.legR[2] + (socks ? (socks.thick ?? 0.004) : 0), d.footR * 0.9, pumps ? legMat : footMat, { part: fpart });
  }

  // ----- pelvis, and a skirt if there is one -----
  const tw = J.twist, topMat = top.mat || skin, psi = tw * 0.6;
  ball(add(J.hipC, [0, 0.012, 0]), d.pelvisR, bottom.kind === "skirt" ? bottom.under || bottom.mat : bottom.mat || skin, { part: PELVIS }, J.hipTwist);
  if (bottom.kind === "kilt") ball(add(J.hipC, [0, -0.012, 0.045]), [d.pelvisR[0] * 1.12, 0.05, 0.10], bottom.mat, { part: PELVIS }, J.hipTwist);
  const under = S * 0.07;                                               // how far a body may bulge under loose cloth and still be covered by it
  if (bottom.rise) {                                                    // a high waist: the cloth comes up over the stomach, and the shirt is tucked into it
    const rw = widthAt(d.trunkLow, psi) + 0.007;
    limb(J.spine(d.hipY + bottom.rise), J.spine(d.hipY + 0.026), rw, rw, bottom.mat, { part: PELVIS, depth: depthAt(d.trunkLow, psi) / rw, bias: S * 0.022, squareStart: true, squareEnd: true });
  }
  if (bottom.kind === "skirt") {
    // A skirt is one cone round both legs, from the waist over the hips to the hem. The hem follows the
    // legs: when they stride apart it widens, and when the knees bend it swings forward with them.
    const len = bottom.len ?? 0.9;                                      // 1 is the knee
    const down = (L) => (len <= 1 ? mix(L.hip, L.knee, len) : mix(L.knee, L.ankle, ((len - 1) * d.thigh) / d.shin));
    const pR = down(J.R), pL = down(J.L);
    const apart = turn([pR[0] - pL[0], 0, pR[2] - pL[2]], -J.hipTwist);                      // sideways, and fore and aft
    const flare = bottom.flare ?? 1.25, ht = J.hipTwist;
    const waist2 = d.trunkLow, hip2 = [d.pelvisR[0] + 0.008, d.pelvisR[2] + 0.006];
    const legR2 = lerp(d.legR[0], d.legR[1], Math.min(1, len)) + 0.016;
    const hem2 = [Math.max(hip2[0] * flare, Math.abs(apart[0]) / 2 + legR2), Math.max(hip2[1] * flare, Math.abs(apart[2]) / 2 + legR2)];
    const a0 = J.spine(d.waistY - 0.004), a1 = add(J.hipC, [0, 0.004, 0]), a2 = mix(pR, pL, 0.5);
    const r0 = widthAt(waist2, psi), r1 = widthAt(hip2, ht), r2 = widthAt(hem2, ht);
    const loose = { [PELVIS]: under, [LEG.R]: under, [LEG.L]: under };
    const pleats = bottom.pleats && !coarse ? shifted(bottom.mat, 1) : null;
    const fold = pleats ? (t, nx) => (Math.floor((Math.asin(clamp1(nx)) / Math.PI + 0.5) * bottom.pleats + 0.5) % 2 ? pleats : undefined) : null;
    limb(a0, a1, r0, r1, bottom.mat, { part: SKIRT, depth: (depthAt(waist2, psi) + depthAt(hip2, ht)) / (r0 + r1), over: loose, bias: S * 0.006 });
    limb(a1, a2, r1, r2, bottom.mat, { part: SKIRT, depth: (depthAt(hip2, ht) + depthAt(hem2, ht)) / (r1 + r2), over: loose, bias: S * 0.006, hem: true, hemMin: 0.35, fn: fold });   // a wide hem stays a straight edge
  }

  // The trunk is wider than it is deep, so how wide it looks depends on the way the figure is turned.
  const wide = (r2) => widthAt(r2, psi), deep = (r2) => depthAt(r2, psi);
  // Chest to waist, then waist to hem: two lengths, so that a stomach can stick out at the waist and tuck back in below.
  const lowR = d.trunkHem || [d.trunkLow[0] * 0.97, d.trunkLow[1] * 0.90];
  const rT = wide(d.trunkTop) + 0.003 * breath, rW = wide(d.trunkLow), rB = wide(lowR);
  const hemY = top.hem ? d.hipY - 0.042 : d.hipY + 0.05;
  const tTop = J.spine(d.shoulderY - rT * 0.80);
  const tMid = add(J.spine(d.waistY), J.torso([0, 0, d.bellyFwd || 0]));
  const tLow = add(J.spine(hemY), J.torso([0, 0, (d.bellyFwd || 0) * 0.55]));
  // a patterned shirt: the pattern is fixed to the cloth, so it turns with the body
  const printed = top.pattern && !coarse;
  const around = (nx) => { const u = clamp1(nx), o = own(u, 0, Math.sqrt(1 - u * u), psi); return Math.atan2(o[0], o[2]) * 0.115; };
  const TA = P(tTop), TB = P(tLow), tdx = TB[0] - TA[0], tdy = TB[1] - TA[1], tl2 = tdx * tdx + tdy * tdy || 1, ra = R(rT), rb = R(rB);
  const high = (y) => (TA[1] - y) / S;                                 // height measured down the cloth itself, so the print moves with the body
  const onTrunk = printed ? (t, nx, ny, x, y) => flowers(around(nx), high(y), top.pattern) : null;
  // the same print carried out onto the shoulders, which are not part of the trunk's own shape
  const print = printed ? (t, nx, ny, x, y) => {
    let k = ((x + 0.5 - TA[0]) * tdx + (y + 0.5 - TA[1]) * tdy) / tl2; k = k < 0 ? 0 : k > 1 ? 1 : k;
    const u = (x + 0.5 - TA[0] - tdx * k) / (ra + (rb - ra) * k);
    return u < -1 || u > 1 ? undefined : flowers(around(u), high(y), top.pattern);         // plain cloth out past the trunk's own width
  } : null;
  // overalls: a bib on the chest and a strap over each shoulder, drawn on the shirt so that they turn with the body
  const bib = bottom.bib && !coarse ? bottom.bib : null;
  const bibAt = bib ? (u, y) => {
    const o = own(u, 0, Math.sqrt(1 - u * u), psi), a = Math.abs(Math.atan2(o[0], o[2]));    // how far round the body from the middle of the chest
    const below = rT * 0.80 - high(y), half = bib.half ?? 0.62, strap = bib.strap ?? 0.30;   // how far below the shoulder line
    if (a < half) return below > (bib.top ?? 0.07) || a > half - strap ? bottom.mat : undefined;
    const back = Math.PI - a, low = bib.back ?? 0.62;
    return back < low && back > low - strap ? bottom.mat : undefined;                        // a strap down each side of the back
  } : null;
  const onBib = bib ? (t, nx, ny, x, y) => bibAt(clamp1(nx), y) : null;
  const bibOut = bib ? (t, nx, ny, x, y) => {
    let k = ((x + 0.5 - TA[0]) * tdx + (y + 0.5 - TA[1]) * tdy) / tl2; k = k < 0 ? 0 : k > 1 ? 1 : k;
    const u = (x + 0.5 - TA[0] - tdx * k) / (ra + (rb - ra) * k);
    return u < -1 || u > 1 ? undefined : bibAt(u, y);
  } : null;
  const onCloth = onTrunk || onBib, offTrunk = print || bibOut;
  const cloth = S * 0.014;                                              // cloth sits just outside whatever it covers
  // an untucked shirt hangs over the hips, even where they stick out further than the chest does
  const loose = top.hem && !pose.seated ? { [PELVIS]: under, [SHORTS.R]: under, [SHORTS.L]: under, [LEG.R]: under, [LEG.L]: under, [SKIRT]: under } : null;
  const dT = deep(d.trunkTop), dW = deep(d.trunkLow), dB = deep(lowR);
  limb(tTop, tMid, rT, rW, topMat, { part: TORSO, depth: (dT + dW) / (rT + rW), bias: cloth, fn: onCloth });
  limb(tMid, tLow, rW, rB, topMat, { part: TORSO, depth: (dW + dB) / (rW + rB), bias: cloth, squareEnd: !!top.hem || !!bottom.rise, over: loose, fn: onCloth });   // an untucked shirt ends in a straight hem
  if (top.belt) limb(add(tMid, J.torso([0, 0.012, 0])), add(tMid, J.torso([0, -0.012, 0])), rW + 0.004, rW + 0.004, top.belt, { part: TORSO, depth: dW / rW, bias: cloth * 1.6, squareEnd: true, squareStart: true });
  // shoulders: one slope from the side of the neck out over the top of each arm
  const capR = d.armR[0] + (top.mat ? 0.008 : 0.003);
  for (const k of ["R", "L"]) {
    const sd = k === "R" ? 1 : -1;
    limb(add(J.sh, J.torso([sd * 0.034, 0.002, -0.004])), add(J[k].shoulder, J.torso([-sd * 0.008, capR - 0.022, 0])), 0.020, 0.022, topMat, { part: TORSO, bias: cloth, fn: offTrunk });
    ball(J[k].shoulder, [capR, capR, capR], topMat, { part: TORSO, bias: cloth, fn: offTrunk && ((ux, uy, uz, x, y) => offTrunk(0, 0, 0, x, y)) });
  }
  // neck, and what shows at the collar
  limb(J.spine(d.shoulderY - 0.012), add(J.head, [0, -d.headR[1] * 0.55, 0.004]), 0.031 * (d.neckR ?? 1), 0.029 * (d.neckR ?? 1), skin, { part: NECK });
  if (top.mat && top.open) {
    const front = d.trunkTop[1];                         // the open neck: a narrow strip of chest, lying on the chest's own curve
    limb(add(J.sh, J.torso([0, 0.012, front * 0.34])), add(J.sh, J.torso([0, -0.046, front * 0.95])), 0.021, 0.008, top.under || skin, { part: NECK, bias: cloth * 1.5 });
  }
  if (top.mat && top.band) {                             // a round collar: a band lying at the base of the neck, with two rounded points in front
    ball(add(J.sh, J.torso([0, -0.014, d.trunkTop[1] * 0.44])), [0.060, 0.032, 0.048], top.band, {
      part: NECK, bias: cloth * 1.5,
      fn: (ux, uy) => (ux * ux * 0.8 + (uy + 1.05) ** 2 < 0.62 || (Math.abs(ux) < 0.09 && uy > 0.05) ? null : undefined),
    }, tw);
  }
  if (top.mat && top.collar) {
    const cm = top.collar === true ? shifted(top.mat, -1) : top.collar, front = d.trunkTop[1];
    for (const sd of [1, -1]) limb(add(J.sh, J.torso([sd * 0.027, 0.014, front * 0.26])), add(J.sh, J.torso([sd * 0.058, -0.022, front * 0.74])), 0.014, 0.010, cm, { part: TORSO, bias: cloth * 1.5 });
  }

  // ----- arms -----
  for (const k of ["R", "L"]) {
    const A = J[k], part = ARM[k];
    const sleeves = top.mat ? (top.sleeves ?? 0.6) : 0, long = sleeves >= 2;
    const armMat = long ? top.mat : skin;
    limb(A.shoulder, A.elbow, d.armR[0], d.armR[1], armMat, { part });
    limb(A.elbow, A.wrist, d.armR[1] + (long ? 0.004 : 0), d.armR[2] + (long ? 0.006 : 0), armMat, { part });
    if (sleeves > 0 && !long) {
      // a short sleeve: its own print, fixed to the sleeve so that it swings with the arm
      const len = d.upperArm * sleeves, seed = k === "R" ? 0.31 : 0.67;
      limb(A.shoulder, mix(A.shoulder, A.elbow, sleeves), d.armR[0] + 0.005, lerp(d.armR[0], d.armR[1], sleeves) + 0.010, top.mat, {
        part: SLEEVE[k], hem: true,
        fn: printed ? (t, nx) => (t <= 0 ? undefined : flowers(seed + Math.asin(clamp1(nx)) * 0.045, t * len, top.pattern)) : null,
      });
    }
    limb(A.wrist, A.tip, d.handR, d.handR * 0.8, skin, { part });
    if (pose[k] && pose[k].finger) limb(A.tip, add(A.tip, mul(unit([A.tip[0] - A.wrist[0], A.tip[1] - A.wrist[1], A.tip[2] - A.wrist[2]]), 0.034)), 0.0085, 0.0065, skin, { part });   // a pointing finger
  }

  // ----- head -----
  const hy = J.headYaw, hr = d.headR, hc = J.head;
  const headPt = (v) => add(hc, turn(v, hy));                 // a point given in the head's own frame
  const hairAt = hair.where || (() => false);
  ball(hc, hr, skin, { part: HEAD, fn: (ux, uy, uz) => { const o = own(ux, uy, uz, hy); return hairAt(o[0], o[1], o[2]) ? hair.mat : undefined; } }, hy);
  ball(headPt([0, -hr[1] * 0.50, hr[2] * 0.10]), [hr[0] * 0.78, hr[1] * 0.50, hr[2] * 0.78], face.beard || skin, { part: face.beard ? HAIR : HEAD }, hy);     // jaw, or the beard that covers it
  if (hair.mat) {
    const grow = hair.bulk ?? 1.07;
    ball(add(hc, [0, 0.003, 0]), [hr[0] * grow, hr[1] * grow, hr[2] * grow], hair.mat, { part: HAIR, fn: (ux, uy, uz) => { const o = own(ux, uy, uz, hy); return hairAt(o[0], o[1], o[2]) ? undefined : null; } }, hy);
  }
  if (hair.mat && hair.top) ball(headPt([hair.top[0], hr[1] * hair.top[1], hr[2] * hair.top[2]]), [hr[0] * hair.top[3], hr[1] * hair.top[4], hr[2] * hair.top[5]], hair.mat, { part: HAIR }, hy);
  for (const sd of [1, -1]) ball(headPt([sd * hr[0] * 0.97, -0.006, -0.004]), [0.012, 0.02, 0.014], skin, { part: HEAD }, hy);   // ears
  ball(headPt([0, -0.008, hr[2] * 1.0]), [0.015, 0.018, 0.020].map((v) => v * (face.nose ?? 1)), skin, { part: HEAD }, hy);       // nose
  if (face.moustache) limb(headPt([-0.021, -0.034, hr[2] * 0.93]), headPt([0.021, -0.034, hr[2] * 0.93]), 0.0105, 0.0105, face.moustache, { part: HAIR });

  // hats, hair that hangs, packs, bags and whatever else this character wears or carries
  if (spec.extras) spec.extras({ sf, J, P, R, limb, ball, own, headPt, wide, deep, widthAt, depthAt, d, S, th, hy, tw, fine, coarse, pose, parts: { HEAD, HAIR, TORSO, EXTRA, EXTRA2, EXTRA3, HAT, NECK, ARM } });

  // ----- face, placed pixel by pixel -----
  const seen = (v) => { const w = turn(v, hy); return w[0] * s + w[2] * c; };          // how much a head direction faces the viewer
  const facePt = (lon, lat) => { const e = [Math.sin(lon) * Math.cos(lat), Math.sin(lat), Math.cos(lon) * Math.cos(lat)]; return { e, at: P(headPt([e[0] * hr[0], e[1] * hr[1], e[2] * hr[2]])) }; };
  const eyeDark = pack(face.eye || "#2a1a12"), eyeWhite = pack("#fff8ee"), lidTone = skin.tones[2];
  const frame = face.glasses ? pack(face.glasses) : 0, shade = face.shades ? pack(face.shades) : 0;
  const center = P(hc)[0];
  let eyesSeen = 0, lastEye = null;
  for (const sd of [1, -1]) {
    const { e, at } = facePt(sd * (face.eyeLon ?? 0.46), face.eyeLat ?? 0.10), vis = seen(e);
    if (vis < 0.40) continue;
    const x = Math.round(at[0] - 0.5), y = Math.round(at[1] - 0.5);
    const inward = at[0] < center ? 1 : -1;                                               // toward the nose, as seen
    eyesSeen++; lastEye = { x, y, inward };
    if (shade) {                                                                          // dark glasses: a lens over each eye
      if (fine) for (let i = -1; i <= 2; i++) for (let j = -1; j <= 0; j++) sf.dot(x + inward * i, y + j, shade, HEAD);
      else { sf.dot(x, y, shade, HEAD); sf.dot(x + inward, y, shade, HEAD); }
      continue;
    }
    if (pose.blink) { sf.dot(x, y, lidTone, HEAD); if (fine) sf.dot(x + inward, y, lidTone, HEAD); }
    else if (fine) {
      sf.dot(x, y, eyeWhite, HEAD); sf.dot(x + inward, y, eyeDark, HEAD);
      if (face.big) { sf.dot(x, y + 1, eyeWhite, HEAD); sf.dot(x + inward, y + 1, eyeDark, HEAD); }       // a child's eyes: two pixels tall
      else if (face.lashes) { sf.dot(x, y - 1, eyeDark, HEAD); sf.dot(x + inward, y - 1, eyeDark, HEAD); sf.dot(x - inward, y - 1, eyeDark, HEAD); }   // a dark upper lid, swept outward
      else if (S >= 110) { sf.dot(x, y - 1, lidTone, HEAD); sf.dot(x + inward, y - 1, lidTone, HEAD); }
    } else sf.dot(x, y, eyeDark, HEAD);
    if (face.brows && fine) {
      const by = y - (S >= 110 ? 3 : 2);
      for (const i of [-1, 0, 1]) sf.dot(x + i, by, face.brows, HEAD);
    }
    if (frame && fine) {                                                                  // glasses: a thin frame round each eye
      const tall = face.big ? 2 : 1, x0 = Math.min(x, x + inward) - 1, x1 = Math.max(x, x + inward) + 1;
      for (let i = x0; i <= x1; i++) { sf.dot(i, y - 1, frame, HEAD); sf.dot(i, y + tall, frame, HEAD); }
      for (let j = 0; j < tall; j++) { sf.dot(x0, y + j, frame, HEAD); sf.dot(x1, y + j, frame, HEAD); }
      sf.dot(inward > 0 ? x1 + 1 : x0 - 1, y, frame, HEAD);                               // toward the bridge of the nose
    } else if (frame && !coarse) { sf.dot(x - inward, y, frame, HEAD); sf.dot(x + inward * 2, y, frame, HEAD); }
    if (face.freckles && fine) { sf.dot(x - inward, y + 3, lidTone, HEAD); sf.dot(x + inward, y + 4, lidTone, HEAD); }
  }
  // seen from the side, glasses show the arm that runs back to the ear
  if ((frame || shade) && eyesSeen === 1 && fine && lastEye) for (let i = 2; i <= 5; i++) sf.dot(lastEye.x - lastEye.inward * i, lastEye.y - (shade ? 1 : 0), frame || shade, HEAD);
  // mouth: a line when shut; open shapes for talking
  if (face.mouth !== false && !coarse) {
    const { e, at } = facePt(0, face.mouthLat ?? -0.50), vis = seen(e);
    if (vis > 0.18) {
      const half = vis > 0.75 ? (fine ? 1 : 0) : 0, x = Math.round(at[0] - 0.5), y = Math.round(at[1] - 0.5), open = pose.mouth || 0;
      const lip = pack(face.lip || "#7a3a2c"), inside = pack("#3a1612"), on = face.beard ? HAIR : HEAD;
      if (open === 0) { if (!face.moustache && !face.beard) for (let i = -half; i <= half; i++) sf.dot(x + i, y, lip, on); }
      else {
        for (let i = -half; i <= half; i++) { sf.dot(x + i, y, inside, on); if (open > 1) sf.dot(x + i, y + 1, inside, on); }
        if (open > 1 && fine) sf.dot(x, y + 1, lip, on);
      }
    }
  }
  // Lines the eye expects: between the two legs, between an arm and the body it hangs against,
  // and a thin shadow under the edge of a sleeve, a pair of shorts, a skirt or an untucked shirt.
  const armR = (q) => q === ARM.R || q === SLEEVE.R, armL = (q) => q === ARM.L || q === SLEEVE.L;
  const legR = (q) => q === LEG.R || q === SHORTS.R, legL = (q) => q === LEG.L || q === SHORTS.L;
  // an arm shows a line against the body only below the armpit: over the top of the shoulder the two are one shape
  const pitR = P(J.R.shoulder)[1] + R(capR) * 0.7, pitL = P(J.L.shoulder)[1] + R(capR) * 0.7;
  const beside = (q, other, y) => other === TORSO && ((armR(q) && y > pitR) || (armL(q) && y > pitL));
  return sf.finish({
    seams: (a, b, below, x, y) =>
      (a === SHORTS.R && b === LEG.R) || (a === SHORTS.L && b === LEG.L) || (a === SLEEVE.R && b === ARM.R) || (a === SLEEVE.L && b === ARM.L) ||
      (a === SKIRT && (b === LEG.R || b === LEG.L)) ||
      (below ? !!loose && a === TORSO && (b === PELVIS || b === SKIRT || legR(b) || legL(b))
        : (legR(a) && legL(b)) || (legL(a) && legR(b)) || beside(a, b, y) || beside(b, a, y)),
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
    R: { leg: [r.pitch, 0.02], knee: r.knee, foot: r.foot, arm: [-arm * Math.cos(a), 0.07], elbow: bend + pump * (0.5 - 0.5 * Math.cos(a)) },
    L: { leg: [l.pitch, 0.02], knee: l.knee, foot: l.foot, arm: [arm * Math.cos(a), 0.07], elbow: bend + pump * (0.5 + 0.5 * Math.cos(a)) },
  };
  for (const k of ["R", "L"]) if (o.hold && o.hold[k]) p[k] = { ...p[k], ...o.hold[k] };
  return p;
}

/** Arm poses for carrying something. A walk can keep one going: walk: { hold: { L: CARRY.book } }. */
export const CARRY = { book: { arm: [0.30, 0.05], fore: [0.80, 0.22, 0.56] } };

// Ways of standing. Each changes the arms of the plain standing pose.
const STANCES = {
  /** hands lightly clasped in front of the waist */
  clasped(p) { for (const [k, sd] of [["R", 1], ["L", -1]]) p[k] = { ...p[k], arm: [0.20, 0.06], fore: [-sd * 0.62, -0.60, 0.50] }; },
  /** fists on hips */
  akimbo(p) { for (const k of ["R", "L"]) p[k] = { ...p[k], arm: [-0.25, 0.55], elbow: 1.55, tuck: 0.9 }; },
  /** a book held against the chest: the left forearm lies across it */
  book(p) { p.L = { ...p.L, ...CARRY.book }; },
  /** hands behind the back */
  behind(p) { for (const [k, sd] of [["R", 1], ["L", -1]]) p[k] = { ...p[k], arm: [-0.26, 0.05], fore: [-sd * 0.70, -0.48, -0.53] }; },
};

/** Standing still. f counts slow breaths: eight steps to one breath. o.stance picks a way of standing. */
export function standPose(f = 0, o = {}) {
  const br = 0.5 - 0.5 * Math.cos((2 * Math.PI * f) / 8);
  const p = {
    breath: br, lean: o.lean ?? 0.02,
    R: { arm: [0.05, 0.10], elbow: 0.18, leg: [0.0, 0.04], knee: 0.03 },
    L: { arm: [-0.02, 0.10], elbow: 0.14, leg: [0.0, 0.04], knee: 0.03 },
  };
  if (o.stance && STANCES[o.stance]) STANCES[o.stance](p);
  return p;
}

/**
 * Talking with the hands. g picks the gesture, f counts frames within it.
 *   0 a nod            1 one hand up, making a point    2 both palms up: a shrug     3 a hand on the hip
 *   4 both arms up     5 a hand to the heart            6 pushing glasses up         7 showing off muscles
 *   8 an open hand     9 both hands waving              10 pointing straight ahead   11 a finger in the air
 */
export function talkPose(f = 0, g = 0, o = {}) {
  const wob = Math.sin((2 * Math.PI * f) / 6), p = standPose(f, o);
  const both = (make) => { p.R = { ...p.R, ...make(1) }; p.L = { ...p.L, ...make(-1) }; };
  const free = (side) => { const q = { ...p[side] }; delete q.fore; delete q.tuck; return q; };       // an arm let go of whatever the stance had it doing
  if (g === 1) {                    // one hand up, making a point
    p.R = { ...free("R"), arm: [0.42, 0.16], elbow: 1.75 + 0.18 * wob };
    p.head = { nod: 0.03 * wob };
  } else if (g === 2) {             // both palms up: a shrug
    p.R = { ...free("R"), arm: [0.22, 0.34], elbow: 1.25 + 0.10 * wob };
    p.L = { ...free("L"), arm: [0.22, 0.34], elbow: 1.25 + 0.10 * wob };
    p.breath = 1;
    p.head = { nod: -0.04, turn: 0.10 * wob };
  } else if (g === 3) {             // hand on hip
    p.L = { ...free("L"), arm: [-0.25, 0.55], elbow: 1.55, tuck: 0.9 };
    p.head = { nod: 0.02 * wob, turn: 0.06 * wob };
  } else if (g === 4) {             // both arms up
    p.R = { ...free("R"), arm: [2.55 + 0.10 * wob, 0.38], elbow: 0.25 };
    p.L = { ...free("L"), arm: [2.55 - 0.10 * wob, 0.38], elbow: 0.25 };
    p.breath = 1;
    p.head = { nod: -0.10 };
  } else if (g === 5) {             // a hand to the heart
    p.R = { ...free("R"), arm: [0.25, 0.10], fore: [-0.74, 0.61 + 0.03 * wob, 0.29] };
    p.head = { nod: 0.04 + 0.02 * wob, turn: 0.05 * wob };
  } else if (g === 6) {             // pushing glasses up
    p.R = { ...free("R"), arm: [1.80, 0.30], fore: [-0.53, 0.76 + 0.04 * wob, -0.38], finger: true };
    p.head = { nod: 0.05 };
  } else if (g === 7) {             // showing off muscles
    both((sd) => ({ arm: [0.05, 1.35], elbow: 0, tuck: 0, fore: [sd * (0.18 + 0.06 * wob), 0.96, 0.12] }));
    p.breath = 1;
  } else if (g === 8) {             // an open hand, held out
    p.R = { ...free("R"), arm: [0.16, 0.14], fore: [0.50, -0.10 + 0.06 * wob, 0.86] };
    p.head = { nod: 0.02, turn: -0.08 };
  } else if (g === 9) {             // both hands waving
    both((sd) => ({ arm: [0.55, 0.75], elbow: 0, tuck: 0, fore: [sd * (0.45 + 0.30 * wob * sd), 0.85, 0.25] }));
    p.head = { nod: -0.04, turn: 0.12 * wob };
  } else if (g === 10) {            // pointing straight ahead
    p.R = { ...free("R"), arm: [1.38 + 0.05 * wob, 0.08], elbow: 0.08, finger: true };
    p.lean = 0.07;
  } else if (g === 11) {            // a finger in the air: "fun fact"
    p.R = { ...free("R"), arm: [0.35, 0.80], fore: [-0.10 + 0.05 * wob, 0.98, 0.14], finger: true };
    p.head = { nod: -0.03, turn: 0.04 * wob };
  } else p.head = { nod: 0.035 * wob };
  return p;
}

/** Reaching for something. k goes 0 to 1. low: bend down for it; otherwise reach out at chest height. */
export function reachPose(k, low = false, o = {}) {
  const p = standPose(0, o), carrying = o.stance === "book";       // an arm that is carrying something stays where it is
  if (low && o.soft) {             // in a skirt: a dip at the knees and a small bow, not a deep bend
    const legs = { leg: [0.24 * k, 0.04], knee: 0.46 * k };
    p.lean = 0.40 * k;
    p.R = { arm: [0.78 * k + 0.05, 0.08], elbow: 0.14, ...legs };
    p.L = carrying ? { ...p.L, ...legs } : { arm: [0.12 * k, 0.14], elbow: 0.3 * k + 0.14, ...legs };
    p.head = { nod: -0.16 * k };
  } else if (low) {
    p.lean = 0.62 * k;
    p.R = { arm: [1.05 * k + 0.05, 0.08], elbow: 0.18, leg: [0.42 * k, 0.04], knee: 0.80 * k };
    p.L = carrying ? { ...p.L, leg: [0.42 * k, 0.04], knee: 0.80 * k } : { arm: [0.25 * k, 0.16], elbow: 0.5 * k + 0.14, leg: [0.42 * k, 0.04], knee: 0.80 * k };
    p.head = { nod: -0.25 * k };
  } else {
    p.lean = 0.14 * k;
    const base = { ...p.R }; delete base.fore; delete base.tuck;
    p.R = { ...base, arm: [1.32 * k + 0.05, 0.06], elbow: 0.18 + 0.1 * k };
    p.head = { nod: 0.04 * k };
  }
  return p;
}

/** Sitting: cross-legged on the ground, or (o.chair) on a seat with the feet on the floor. */
export function sitPose(f = 0, o = {}) {
  const br = 0.5 - 0.5 * Math.cos((2 * Math.PI * f) / 8), g = o.gesture || 0, wob = Math.sin((2 * Math.PI * f) / 6);
  if (o.chair) {
    const side = (raised) => ({
      leg: [1.46, 0.10], knee: 1.46, foot: 0, footYaw: 0.10,
      arm: raised ? [0.55, 0.20] : [0.42, 0.10], elbow: raised ? 1.85 + 0.15 * wob : 0.85,            // a hand resting on each knee
    });
    return { seated: true, breath: br, lean: -0.12, R: side(g === 1), L: side(false), head: { nod: 0.10 + (g ? 0.03 * wob : 0) } };
  }
  const side = (sd, raised) => ({
    leg: [1.42, 0.86], shin: [-sd * 0.9, -0.12, -0.36], footYaw: -1.35, foot: 0,
    arm: raised ? [0.50, 0.22] : [0.22, 0.12],
    ...(raised ? { elbow: 1.95 + 0.15 * wob } : { fore: [-sd * 0.42, -0.34, 0.84] }),      // hands come together over the lap
  });
  return { seated: true, breath: br, lean: 0.05, R: side(1, g === 1), L: side(-1, false), head: { nod: g ? 0.03 * wob : 0 } };
}

// ---------- each character's own way of doing these ----------
const DEFAULT_GESTURES = [0, 1, 2, 3];
/** Standing, walking, talking, reaching and sitting the way one particular character does them. */
export const poses = {
  stand: (spec, f) => standPose(f, { stance: spec.stance }),
  walk: (spec, ph) => walkPose(ph, spec.walk),
  /** `seed` is any whole number; the same seed always gives this character the same gesture. */
  gesture: (spec, seed) => { const list = spec.gestures || DEFAULT_GESTURES; return list[seed % list.length]; },
  talk: (spec, f, g) => talkPose(f, g, { stance: spec.stance }),
  reach: (spec, k, low) => reachPose(k, low, { stance: spec.stance, soft: !!spec.bottom && spec.bottom.kind === "skirt" }),
  sit: (spec, f, o = {}) => sitPose(f, { ...o, chair: spec.seated === "chair" }),
};

export { ramp, pack, shifted, add, mul, mix, turn, lerp };
