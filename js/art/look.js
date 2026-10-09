// The game's paints: every scene is mixed from one box of paints, the Post-Impressionists' of 1888, in a key for its
// era and hour (docs/DESIGN.md, "The paints"). The painted pictures come keyed already (tools/paint/postimp_key.py, at
// strength 50); this file keys what the game draws itself, in the same key at the same strength:
//
//   - the people (pix.js asks tonesOf for a material's four tones, pixelOf for an exact pixel): the light tones toward
//     the key's light (warmer under lamps), the shade tones toward its coloured shadow, every colour a little toward its
//     nearest paints; the shadow on the ground under them becomes the key's shadow colour instead of a grey. Shapes,
//     faces and motion are the rig's own; only colours change. The team's portraits are drawn without the key (withoutKey):
//     they belong to the interface.
//   - the moving things (effects.js asks keyHex for each colour a scene gives its smoke, flames, embers, water and drawn
//     birds). The time portal is never keyed: time's colour belongs to no place.
//
// game.js says which scene is on the stage (keyScene). Which key a scene uses, and every number of every key, are in
// look-data.js, written by tools/paint/postimp_key.py --js from tools/paint/postimp_paints.py: the same arithmetic as
// postimp_look.py (key_colour, for one colour at a time with no picture round it).

import { LOOK_DATA as D } from "./look-data.js";

// ---------------------------------------------------------------- colour arithmetic (OKLab)
const lin = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const gam = (c) => (c <= 0.0031308 ? c * 12.92 : 1.055 * c ** (1 / 2.4) - 0.055);
function rgbToLab(r, g, b) {
  r = lin(r); g = lin(g); b = lin(b);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s, 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s, 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s];
}
function labToLin(L, a, b) {
  const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3, m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3, s = (L - 0.0894841775 * a - 1.291485548 * b) ** 3;
  return [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s, -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s];
}
const inside = (c) => c.every((v) => v >= -1e-4 && v <= 1 + 1e-4);
/** OKLab -> sRGB 0..1, brought into the gamut by giving up chroma (lightness and hue kept), as oklab.gamut does. */
function labToRgb(L, a, b) {
  L = Math.min(1, Math.max(0, L));
  let c = labToLin(L, a, b);
  if (!inside(c)) {
    let lo = 0, hi = 1;
    for (let i = 0; i < 14; i++) { const mid = (lo + hi) / 2; if (inside(labToLin(L, a * mid, b * mid))) lo = mid; else hi = mid; }
    c = labToLin(L, a * lo, b * lo);
  }
  return c.map((v) => gam(Math.min(1, Math.max(0, v))));
}

const ss = (e0, e1, x) => { const t = Math.min(1, Math.max(0, (x - e0) / (e1 - e0))); return t * t * (3 - 2 * t); };
const RAD = Math.PI / 180;

function paintAt(p, L) {
  const [Lp, ap, bp] = p, W = D.white;
  if (L > Lp) { const t = Math.min(1, Math.max(0, (L - Lp) / Math.max(1e-3, W[0] - Lp))); return [ap + (W[1] - ap) * t, bp + (W[2] - bp) * t]; }
  const k = Math.min(1, Math.max(0, L / Lp));
  return [ap * k, bp * k];
}
function rampAt(r, L) {
  if (r.length === 1) return paintAt(r[0], L);
  if (L <= r[0][0]) return paintAt(r[0], L);
  if (L >= r[r.length - 1][0]) return paintAt(r[r.length - 1], L);
  for (let i = 0; i + 1 < r.length; i++) {
    const v0 = r[i], v1 = r[i + 1];
    if (L >= v0[0] && L < v1[0]) { const t = Math.min(1, Math.max(0, (L - v0[0]) / Math.max(1e-4, v1[0] - v0[0]))); return [v0[1] + (v1[1] - v0[1]) * t, v0[2] + (v1[2] - v0[2]) * t]; }
  }
  return paintAt(r[r.length - 1], L);
}
function families(L, a, b) {
  const h = Math.atan2(b, a) / RAD, C = Math.hypot(a, b);
  const bump = (c, half) => { const d = ((h - c + 180) % 360 + 360) % 360 - 180; return Math.max(0, Math.cos(Math.min(1, Math.max(-1, d / half)) * Math.PI / 2)) ** 2; };
  const warm = bump(75, 62) + bump(-40, 42), red = bump(22, 34), green = bump(158, 52), blue = bump(-112, 62);
  const tot = warm + red + green + blue + 1e-6, gate = ss(0.012, 0.05, C);
  return { warm: (warm / tot) * gate + (1 - gate), red: (red / tot) * gate, green: (green / tot) * gate, blue: (blue / tot) * gate };
}
function toward(a, b, ta, tb, w, cap, own0 = 0.025, own1 = 0.075) {
  const ca = a + w * (ta - a), cb = b + w * (tb - b), C = Math.hypot(a, b), h0 = Math.atan2(b, a), h1 = Math.atan2(cb, ca);
  let dh = ((h1 - h0 + Math.PI) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI) - Math.PI;
  dh = Math.min(cap, Math.max(-cap, dh));
  const C1 = Math.hypot(ca, cb), pa = C1 * Math.cos(h0 + dh), pb = C1 * Math.sin(h0 + dh), k = ss(own0, own1, C);
  return [ca + k * (pa - ca), cb + k * (pb - cb)];
}

/** The key, for one colour (OKLab), with its light read as given (point_maps). s = strength 0..1. */
function keyLab(L, a, b, K, s, litIn = null, laidIn = null) {
  // point_maps
  const C = Math.hypot(a, b), h = Math.atan2(b, a) / RAD;
  const coolness = Math.max(0, Math.cos(Math.min(1, Math.max(-1, (((h + 55 + 180) % 360 + 360) % 360 - 180) / 70)) * 90 * RAD));
  const cool = coolness * ss(0.010, 0.025, C) * (1 - ss(0.06, 0.09, C)) * ss(0.80, 0.55, L);
  const dark = ss(K.shade_hi, K.shade_lo, L), cast = laidIn == null ? 0 : laidIn;
  const shade = Math.min(1, Math.max(0, Math.max(dark, cast, cool)));
  const lit = (litIn == null ? ss(K.lit_lo, K.lit_hi, L) : litIn) * (1 - shade), turnM = 0;
  const fam = families(L, a, b);
  // key_colour
  const grey = 1 - ss(0.03, 0.10, C);
  const laid = Math.max(cast, cool), own = dark * (1 - laid);
  let sa = 0, sb = 0;
  for (const f of ["warm", "red", "green", "blue"]) {
    let [ta, tb] = rampAt(K.shadow[f], L);
    if (f === "warm") { const [da, db] = rampAt(K.shadow.red, L), q = (own / Math.max(own + laid, 1e-4)) * (1 - grey); ta += q * (da - ta); tb += q * (db - tb); }
    sa += fam[f] * ta; sb += fam[f] * tb;
  }
  const prot = (laid * (0.70 + 0.30 * grey) + own * (0.35 + 0.65 * grey)) / Math.max(laid + own, 1e-4);
  const wSh = s * K.shade * shade * prot, cap = K.turn * RAD * s * ((laid + 0.5 * own) / Math.max(laid + own, 1e-4));
  [a, b] = toward(a, b, sa, sb, wSh, cap);
  const [law, lbw] = rampAt(K.light, L), [lag, lbg] = rampAt(K.lightGreen, L), [lab_, lbb] = rampAt(K.sky, L), fw = fam.warm + fam.red;
  const la = fw * law + fam.green * lag + fam.blue * lab_, lb = fw * lbw + fam.green * lbg + fam.blue * lbb;
  const greyL = 1 - ss(0.015, 0.05, C);
  const wLi = s * K.warm_light * lit * (K.light_chroma + (1 - K.light_chroma) * greyL) * (0.45 + 0.55 * fw);
  const Cb = Math.hypot(a, b);
  [a, b] = toward(a, b, la, lb, wLi, 35 * RAD * s, 0.010, 0.035);
  { const Cn = Math.hypot(a, b), lim = Cb + s * K.light_add; if (Cn > lim) { const f = lim / Math.max(Cn, 1e-6); a *= f; b *= f; } }
  const [oa, ob] = paintAt(K.turnPaint, L);
  [a, b] = toward(a, b, oa, ob, s * K.turn_orange * turnM * fw, 30 * RAD * s);
  let na = 0, nb = 0, den = 0;
  const sig2 = 2 * 0.032 ** 2;
  for (const [name, p] of Object.entries(D.paints)) {
    const [pa, pb] = paintAt(p, L), d2 = (a - pa) ** 2 + (b - pb) ** 2 + (0.16 * (L - p[0])) ** 2, w = K.weight[name] * Math.exp(-d2 / sig2);
    na += w * pa; nb += w * pb; den += w;
  }
  let ta = (na + 0.12 * a) / (den + 0.12), tb = (nb + 0.12 * b) / (den + 0.12);
  const Cs = Math.hypot(a, b), Ct = Math.hypot(ta, tb), Cl = Math.min(Math.max(Ct, 0.85 * Cs), (1 + 0.35 * s) * Cs + 0.010);
  ta = (ta * Cl) / Math.max(Ct, 1e-6); tb = (tb * Cl) / Math.max(Ct, 1e-6);
  [a, b] = toward(a, b, ta, tb, s * K.snap * ss(0.008, 0.03, Cs), 25 * RAD * s);
  const C1 = Math.hypot(a, b), gain = 1 + s * K.chroma * (1 - ss(0.08, 0.16, C1)) * ss(0.01, 0.04, C1) * (1 - 0.6 * ss(0.70, 0.92, L));
  a *= gain; b *= gain;
  const dk = ss(0.30, 0.08, L), [pa, pb] = paintAt(D.prussian, L), [va, vb] = paintAt(D.deepViolet, L), kd = s * 0.45 * dk * grey;
  a += kd * (0.5 * (pa + va) - a); b += kd * (0.5 * (pb + vb) - b);
  return [L + s * K.lift * dk * Math.max(0, 0.30 - L), a, b];
}

/** sRGB 0..1 through a key (by name) at strength 0..100. lit / laid as point_maps takes them (null: read from the colour).
    `people`: with the people's own numbers (a firmer pull to the paints, a more decided coloured shade). */
export function keyRgb(rgb, keyName, strength, lit = null, laid = null, people = false) {
  let K = D.keys[keyName];
  const s = strength / 100;
  if (!K || s <= 0) return rgb;
  if (people) K = { ...K, ...K.people };
  const [L, a, b] = rgbToLab(rgb[0], rgb[1], rgb[2]);
  const out = keyLab(L, a, b, K, s, lit, laid);
  return labToRgb(out[0], out[1], out[2]);
}

// ---------------------------------------------------------------- the key of the scene on stage
let current = null;          // { name, strength, id } of the key in use, or null

/** Say which scene is on the stage (its id and era). Answers true when the key changed: the people's pictures kept from
    before are then in the wrong colours (game.js has the cast forget them). */
export function keyScene(sceneId, era = null) {
  const name = D.scenes[sceneId] || (era && D.eras[era]) || null, strength = D.strength;
  const id = name && strength > 0 ? `${name}@${strength}` : null;
  if ((current && current.id) === id) return false;
  current = id ? { name, strength, id } : null;
  return true;
}
/** The key in use, as a short string ("" for none). */
export const keyId = () => (current ? current.id : "");

// A person's four tones: what each is, to the key. The light tone and the plain colour are lit (the plain one less);
// the shade tone and the deep one are shadow laid on the form, so they take the key's coloured shadow.
const TONE = [[1.0, 0], [0.55, 0], [null, 0.7], [null, 1.0]];
const unpack = (n) => [(n & 255) / 255, ((n >>> 8) & 255) / 255, ((n >>> 16) & 255) / 255, n >>> 24];
const pack = (r, g, b, a) => ((a << 24) | (Math.round(b * 255) << 16) | (Math.round(g * 255) << 8) | Math.round(r * 255)) >>> 0;
const memo = new Map();
function keyPacked(n, tone) {
  if (!current) return n;
  const k = `${current.id}|${n}|${tone}`;
  let v = memo.get(k);
  if (v !== undefined) return v;
  const [r, g, b, a] = unpack(n);
  if (a === 0) v = n;
  else {
    const [lit, laid] = TONE[tone] || TONE[1];
    const out = keyRgb([r, g, b], current.name, current.strength, lit, laid, true);
    v = pack(out[0], out[1], out[2], a);
  }
  memo.set(k, v);
  return v;
}

// The shadow on the ground: today a see-through black. In the look, the key's own shadow colour (a little more of it,
// so it darkens the ground as much as the black did).
function groundShadow(n) {
  const [, , , a] = unpack(n), K = D.keys[current.name], s = current.strength / 100;
  const [sa, sb] = rampAt(K.shadow.warm, K.groundL), rgb = labToRgb(K.groundL, sa, sb);
  return pack(rgb[0] * s, rgb[1] * s, rgb[2] * s, Math.min(255, Math.round(a * (1 + D.groundAlphaGain * s))));
}

const tonesKept = new WeakMap();
/** A material's four tones in the key of the scene on stage (kept per material and key). */
export function tonesOf(material) {
  if (!current) return material.tones;
  let hit = tonesKept.get(material);
  if (hit && hit.id === current.id) return hit.tones;
  const t = material.tones;
  const tones = material.soft && (t[0] >>> 24) < 255 && (t[0] & 0xffffff) === 0 ? t.map(groundShadow) : t.map((n, i) => keyPacked(n, i));
  tonesKept.set(material, { id: current.id, tones });
  return tones;
}
/** One exact pixel (an eye, a button) in the key: as a plain colour. */
export const pixelOf = (n) => keyPacked(n, 1);

/** A CSS colour ("#rrggbb") from a scene's moving things, in the key (a light colour stays light). */
export function keyHex(hex) {
  if (!current || typeof hex !== "string" || !/^#[0-9a-f]{6}$/i.test(hex)) return hex;
  const n = parseInt(hex.slice(1), 16), out = keyRgb([(n >> 16) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255], current.name, current.strength);
  return "#" + out.map((v) => Math.round(v * 255).toString(16).padStart(2, "0")).join("");
}

/** Draw something with no key (the interface: the team's portraits). */
export function withoutKey(fn) {
  const was = current;
  current = null;
  try { return fn(); } finally { current = was; }
}
