// The drawing kit: everything the game draws by code that is not a person or a prop.
//
// Scenes are painted pictures now (800x600 files: see js/engine/scene.js). What is
// still drawn here, and in which units:
//
//   IN PICTURE PIXELS (800x600)
//     portal()    the wormhole, for a scene's live(): the light of time travel is never
//                 painted, so that it can glow, spin and grow
//     sketch()    a stand-in backdrop for a scene that has no painting yet
//   ON THE OLD 320x200 GRID
//     the first scene backdrops (highway, the riverbank, the forum, the living room, the
//     desert stop) and their parts. The engine shows these in a band across the middle
//     of the stage (grid.js, `fit`). They go when their scenes are painted.
//     the close-ups (monitor, screens, notice), which g.closeup() fits the same way
//   12x12
//     the drawn inventory icons
//
// People and props are not here: they are drawn by js/art/rig.js and js/art/props.js.
//
// Color rules (see css/tokens.css and docs/DESIGN.md):
//   ERA parts use classes (s1..s8, far, near, g1..g3, line, light, feat, feat2), so the
//     same drawing code takes on each period's palette.
//   TIME parts (portals, the tunnel) use the neon classes and never change.
//
// LIVE parts. In a kit drawing that is turned into pixels, anything wrapped in
// class="live" is left as a smooth drawing on top: wormholes and their glow, and the few
// things that move by themselves (twinkling stars, ripples). Scripts can find live parts
// by id and animate them. (Everything a scene's live() returns is live already.)

import { W, H } from "../engine/grid.js";

export const HORIZON = 118;            // on the old 320x200 grid

/** Small repeatable random numbers, so a scene looks the same on every visit. */
export function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const rect = (cls, x, y, w, h, more = "") => `<rect class="${cls}" x="${x}" y="${y}" width="${w}" height="${h}"${more}/>`;

export const defs = `<defs>
  <radialGradient id="portal-glow">
    <stop offset="0" stop-color="#fff" stop-opacity="0.95"/><stop offset="0.22" stop-color="#c9f8ff" stop-opacity="0.6"/>
    <stop offset="0.6" stop-color="#5ef2ff" stop-opacity="0.16"/><stop offset="1" stop-color="#5ef2ff" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="road-glow" cx="0.5" cy="0" r="0.85">
    <stop offset="0" stop-color="#7ff5ff" stop-opacity="0.45"/><stop offset="1" stop-color="#7ff5ff" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="tail-glow">
    <stop offset="0" stop-color="#ff4b3a" stop-opacity="0.7"/><stop offset="1" stop-color="#ff4b3a" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="above-horizon"><rect width="320" height="118"/></clipPath>
  <pattern id="mesh" width="3" height="3" patternUnits="userSpaceOnUse">
    <path d="M0,3 L3,0 M0,0 L3,3" stroke="#6b6866" stroke-width="0.35" fill="none"/>
  </pattern>
</defs>`;

/** Eight flat bands from the top of the sky down to the horizon. */
export function sky(bands = [31, 22, 17, 14, 11, 9, 7, 7]) {
  let y = 0;
  return bands.map((h, i) => { const r = rect(`s${i + 1}`, 0, y, 320, h); y += h; return r; }).join("");
}

export function stars(seed = 7, count = 30, maxY = 62) {
  const r = rng(seed);
  let out = "";
  for (let i = 0; i < count; i++) {
    const tw = r() < 0.35 ? ` tw${["", " d1", " d2"][Math.floor(r() * 3)]}` : "";
    out += rect(`light${tw}`, Math.floor(r() * 318) + 1, Math.floor(r() * maxY) + 3, r() < 0.08 ? 2 : 1, 1);
  }
  return `<g class="stars live">${out}</g>`;
}

/** Three ground bands below the horizon, with a few pebbles. */
export function ground(seed = 3, top = HORIZON) {
  const r = rng(seed);
  let pebbles = "";
  for (let i = 0; i < 14; i++) {
    const x = Math.floor(r() * 300) + 8, y = top + 6 + Math.floor(r() * (194 - top - 6));
    if (x > 90 && x < 232 && y > top + 20) continue;       // keep the middle clear for the action
    pebbles += rect("g2", x, y, 2 + Math.floor(r() * 3), 1 + Math.floor(r() * 2));
  }
  return rect("g3", 0, top, 320, 200 - top) + rect("g1", 0, top, 320, 6) + rect("g2", 0, top + 6, 320, 10) + pebbles;
}

/** A wormhole. The same four rings everywhere, in every era: this is the game's signature shape.
    (cx, cy) is its middle and r the radius of the outer ring, in whatever units it is drawn into: picture pixels
    in a scene's live(), the old grid inside an old drawing. Ring widths, dashes and the glow all grow with r,
    and the glow reaches out to 1.4 r. A script scales it about its own middle: g.q("#portal").style.transform = "scale(2)". */
export function portal(cx = 400, cy = 230, r = 68, id = "portal") {
  const k = r / 27;
  const ring = (cls, radius, width, dash) =>
    `<circle class="ring ${cls}" cx="${cx}" cy="${cy}" r="${radius * k}" fill="none" stroke-width="${width * k}" stroke-dasharray="${dash.map((d) => d * k).join(" ")}"/>`;
  return `<g id="${id}" class="portal live" shape-rendering="geometricPrecision" style="transform-origin:${cx}px ${cy}px">
    <circle class="glow" cx="${cx}" cy="${cy}" r="${38 * k}" fill="url(#portal-glow)"/>
    ${ring("r1 t-cyan", 27, 2.5, [12, 7])}${ring("r2 t-magenta", 21, 2.5, [8, 6])}
    ${ring("r3 t-violet", 15, 2, [6, 5])}${ring("r4 t-white", 9, 1.5, [4, 3])}
    <circle class="t-core" cx="${cx}" cy="${cy}" r="${4 * k}"/>
  </g>`;
}

/** A stand-in for a scene that has not been painted yet: sky, ground, and every
    clickable area as a labelled box, in the era's colors. Leave `picture` and `draw` out
    of a scene file to get this, and the scene is playable the moment its puzzle is written.
    Drawn in picture pixels (800x600), like the scene file's own numbers. */
export function sketch(scene) {
  const top = Math.max(60, Math.min(H - 120, scene.horizon ?? 260));       // where the sky meets the ground
  const plain = (words) => String(words).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
  const label = (x, y, words, cls) =>
    `<text class="${cls}" x="${x}" y="${y}" text-anchor="middle" font-family="Trebuchet MS, Verdana, sans-serif" font-weight="700" font-size="15" shape-rendering="geometricPrecision">${plain(words)}</text>`;
  let out = "", y = 0;
  [31, 22, 17, 14, 11, 9, 7, 7].forEach((part, i) => {                       // eight bands of sky, deeper toward the top
    const next = i === 7 ? top : Math.round(y + (part / 118) * top);
    out += rect(`s${i + 1}`, 0, y, W, next - y);
    y = next;
  });
  out += rect("g3", 0, top, W, H - top) + rect("g1", 0, top, W, 15) + rect("g2", 0, top + 15, W, 25);
  const boxes = (scene.hotspots || []).map((h) => {
    let x, y, w, hh;
    if (h.rect) [x, y, w, hh] = h.rect;
    else if (h.circle) [x, y, w, hh] = [h.circle[0] - h.circle[2], h.circle[1] - h.circle[2], h.circle[2] * 2, h.circle[2] * 2];
    else {
      const xs = h.poly.map((p) => p[0]), ys = h.poly.map((p) => p[1]);
      [x, y] = [Math.min(...xs), Math.min(...ys)];
      [w, hh] = [Math.max(...xs) - x, Math.max(...ys) - y];
    }
    return `<rect class="near" x="${x}" y="${y}" width="${w}" height="${hh}" opacity="0.6"/>` +
      `<rect class="stroke-line" x="${x + 1}" y="${y + 1}" width="${w - 2}" height="${hh - 2}" fill="none" stroke-width="2" stroke-dasharray="8 5"/>` +
      label(x + w / 2, y + hh / 2 + 5, h.name, "light");
  }).join("");
  return out + boxes + label(W - 45, H - 8, "SKETCH", "line");
}

// ---------- the present: a desert highway ----------
export const mesas = `
  <polygon class="far" points="0,118 0,106 14,106 18,102 44,102 50,108 66,108 72,118"/>
  <polygon class="near" points="0,118 0,111 30,111 34,109 52,109 58,114 80,114 86,118"/>
  <polygon class="far" points="236,118 242,108 256,108 260,101 290,101 296,107 320,107 320,118"/>
  <polygon class="near" points="222,118 228,113 250,113 254,110 284,110 290,113 320,113 320,118"/>`;

export const road = `
  <polygon class="feat" points="159,118 161,118 236,200 84,200"/>
  <polygon id="road-glow-shape" class="live" fill="url(#road-glow)" points="159,118 161,118 236,200 84,200"/>
  <line class="stroke-feat2" x1="159" y1="118" x2="84" y2="200" stroke-width="1"/>
  <line class="stroke-feat2" x1="161" y1="118" x2="236" y2="200" stroke-width="1"/>
  <g fill="#f2c14e">
    <rect x="160" y="121" width="1" height="2"/><rect x="160" y="126" width="1" height="3"/>
    <rect x="159" y="133" width="2" height="4"/><rect x="159" y="142" width="2" height="6"/>
    <rect x="158" y="155" width="3" height="8"/><rect x="158" y="172" width="3" height="11"/>
    <rect x="158" y="192" width="4" height="8"/>
  </g>`;

/** The road sign. The edit (strike-through and "B.C.") is a live part, so a cutscene can reveal it. */
export const sign = `
  <rect x="247" y="166" width="2" height="18" fill="#7d8288"/><rect x="281" y="166" width="2" height="18" fill="#7d8288"/>
  <rect x="236" y="142" width="58" height="26" fill="#1e7b4b"/>
  <rect x="238.5" y="144.5" width="53" height="21" fill="none" stroke="#eaf5ee" stroke-width="1"/>
  <text x="265" y="153.5" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="8" fill="#eaf5ee" textLength="40" lengthAdjust="spacingAndGlyphs">POINT B</text>
  <g id="sign-edit" class="live" shape-rendering="geometricPrecision">
    <line id="sign-strike" x1="242" y1="151.5" x2="288" y2="149.5" stroke="#ff4a3d" stroke-width="1.6" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0"/>
    <g id="sign-bc">
      <text x="256" y="164" text-anchor="middle" font-family="'Koine Road', Arial, Helvetica, sans-serif" font-size="10.5" fill="#ffd23f">B.C.</text>
      <polygon fill="#ffd23f" points="272,159 281,159 281,156 287,160.5 281,165 281,162 272,162"/>
    </g>
  </g>`;

/** The dusk highway used by the intro and the title screen. The sun and the portal sit behind the horizon. */
export function highway({ sun = false } = {}) {
  return sky() + stars(11, 30) + mesas + ground(3) + road + sign +
    `<g class="live" clip-path="url(#above-horizon)">` +
    (sun ? `<circle id="sun" class="s8" cx="160" cy="104" r="15" shape-rendering="geometricPrecision"/>` : "") +
    portal(160, 92, 27) + `</g>`;
}

// ---------- ancient Egypt: a riverbank at dawn ----------
export const pyramids = `
  <polygon class="far" points="186,118 222,82 258,118"/><polygon class="near" points="222,82 258,118 232,118"/>
  <polygon class="far" points="244,118 270,92 296,118"/><polygon class="near" points="270,92 296,118 278,118"/>`;

export function river() {
  let still = "", moving = "";
  const r = rng(21);
  for (let i = 0; i < 12; i++) {
    const y = 122 + Math.floor(r() * 50), x = Math.floor(r() * 70 * (1 - (y - 122) / 110)) + 4, w = 3 + Math.floor(r() * 5);
    if (r() < 0.5) moving += rect("feat2 ripple", x, y, w, 1); else still += rect("feat2", x, y, w, 1);
  }
  return `<polygon class="feat" points="0,118 128,118 104,134 76,152 40,172 0,186"/>${still}<g class="live">${moving}</g>`;
}

// ---------- Rome: a forum at noon ----------
export function temple() {
  let columns = "";
  for (let i = 0; i < 6; i++) {
    const x = 70 + i * 20;
    columns += rect("light", x, 72, 6, 38) + rect("g2", x + 4, 72, 2, 38) + rect("g1", x - 1, 70, 8, 2) + rect("g1", x - 1, 108, 8, 2);
    if (i === 1 || i === 4) columns += rect("feat", x, 78, 6, 16) + rect("feat2", x, 94, 6, 2);
  }
  return `<polygon class="far" points="0,118 30,100 70,106 110,96 190,104 250,94 320,110 320,118"/>
    ${rect("near", 64, 74, 112, 36)}
    <polygon class="g1" points="58,70 120,48 182,70"/><polygon class="g2" points="72,68 120,53 168,68"/>
    ${rect("g3", 58, 68, 124, 3)}${columns}${rect("g2", 56, 110, 128, 4)}${rect("g1", 50, 114, 140, 4)}`;
}

// ---------- home: the living room, in the evening ----------
const BOOKS = ["#b5483a", "#3f6f8f", "#d9a441", "#5b7d4b", "#7b4f8f", "#c9c2ae", "#2f3a5c", "#a8552c", "#3f8c7c"];
const FAMILY = [["#f4c043", 7], ["#2aa27a", 6.5], ["#666cd6", 6], ["#4fc0e2", 5], ["#f0607f", 4.5]];      // Dad, Mom, Big Sister, the Son, Little Sister

/** The back wall and the floor. Furniture that can be walked round is in js/art/props.js. */
export function livingRoom() {
  const r = rng(5);
  let out = "";
  // ceiling, wallpaper, panelling
  out += rect("s6", 0, 0, 320, 30) + rect("s8", 0, 28, 320, 3) + rect("s5", 0, 31, 320, 62);
  for (let x = 6; x < 320; x += 12) out += rect("s4", x, 31, 3, 62);
  out += rect("s7", 0, 93, 320, 27) + rect("s8", 0, 93, 320, 2) + rect("s8", 0, 116, 320, 4);
  for (let x = 16; x < 320; x += 30) out += rect("s8", x, 99, 1, 14);
  // floorboards: wider as they come nearer
  out += rect("g2", 0, 120, 320, 80) + rect("g3", 0, 120, 320, 2);
  const rows = [122, 128, 137, 149, 164, 183, 200];
  for (let i = 0; i + 1 < rows.length; i++) {
    out += rect("g3", 0, rows[i + 1], 320, 1);
    for (let k = 0; k < 4; k++) out += rect("g3", Math.floor(r() * 316) + 2, rows[i], 1, rows[i + 1] - rows[i]);
    if (i % 2) out += rect("g1", Math.floor(r() * 200) + 20, rows[i] + 1, 60 + Math.floor(r() * 50), 1);
  }
  // a rug in the middle of the floor
  out += `<polygon class="feat" points="98,142 232,142 250,182 80,182"/><polygon class="feat2" points="105,146 225,146 239,178 91,178"/>
    <polygon class="feat" points="112,150 218,150 229,174 101,174"/><polygon class="light" points="165,154 196,162 165,170 134,162" opacity="0.5"/>`;
  // the front door, and the mat in front of it
  out += rect("s8", 8, 54, 34, 66) + rect("near", 11, 57, 28, 63) + rect("far", 14, 61, 22, 20) + rect("far", 14, 86, 22, 30) +
    rect("light", 35, 84, 2, 3) + rect("s8", 20, 100, 10, 2) + `<polygon class="g3" points="6,122 46,122 50,128 2,128"/>`;
  // the window: night outside, a moon, the house across the road
  out += rect("s8", 58, 44, 60, 3) + rect("s8", 62, 48, 52, 46) + rect("s1", 65, 51, 46, 14) + rect("s2", 65, 65, 46, 13) + rect("s3", 65, 78, 46, 13) +
    `<circle class="light" cx="99" cy="60" r="4.5"/><circle class="s1" cx="101.5" cy="59" r="4"/>` +
    rect("line", 65, 82, 24, 9) + `<polygon class="line" points="65,82 77,75 89,82"/>` + rect("light", 71, 85, 3, 3) +
    `<g class="live">${rect("light tw", 70, 55, 1, 1)}${rect("light tw d1", 84, 62, 1, 1)}${rect("light tw d2", 106, 71, 1, 1)}${rect("light", 77, 68, 1, 1)}</g>` +
    rect("s8", 87, 51, 2, 40) + rect("s8", 65, 70, 46, 2) + rect("s7", 60, 93, 56, 3) +
    `<polygon class="feat2" points="62,47 73,47 70,94 62,94"/><polygon class="feat2" points="103,47 114,47 114,94 106,94"/>`;
  // the bookcase
  out += rect("far", 170, 54, 40, 66) + rect("near", 172, 56, 36, 62);
  for (let shelf = 0; shelf < 5; shelf++) {
    const y = 56 + shelf * 12.4;
    out += rect("far", 172, y + 10.4, 36, 2);
    for (let x = 173; x < 206; ) {
      const w = 2 + Math.floor(r() * 3), h = 6.5 + Math.floor(r() * 4), lean = r() < 0.08;
      if (x + w > 207) break;
      if (!lean) out += `<rect x="${x}" y="${y + 10.4 - h}" width="${w}" height="${h}" fill="${BOOKS[Math.floor(r() * BOOKS.length)]}"/>`;
      x += w + (r() < 0.2 ? 1 : 0);
    }
  }
  // the family, framed, above the piano
  out += rect("s8", 226, 52, 34, 22) + rect("light", 228, 54, 30, 18);
  FAMILY.forEach(([shirt, tall], i) => {
    const x = 231 + i * 5.2;
    out += `<rect x="${x}" y="${70 - tall}" width="3.6" height="${tall}" fill="${shirt}"/><rect x="${x + 0.6}" y="${70 - tall - 2.6}" width="2.4" height="2.6" fill="#e8b083"/>`;
  });
  // the stairs, and the closet under them
  for (let i = 0; i < 9; i++) {
    const x = 262 + i * 7, y = 120 - 7 * (i + 1);
    out += rect("s7", x, y, 320 - x, 7) + rect("s8", x, y, 320 - x, 1) + rect("near", x, y + 1, 1, 6);
    out += rect("s8", x + 3, y - 20, 1, 20);                                  // a baluster on every step
  }
  out += `<polygon class="s8" points="258,91 262,89 320,31 320,35 262,93"/>` + rect("s8", 258, 88, 4, 32) + `<circle class="s7" cx="260" cy="87" r="3"/>`;
  out += rect("far", 290, 94, 22, 26) + rect("near", 294, 97, 16, 21) + rect("line", 290, 94, 4, 26) + rect("light", 307, 107, 2, 2);
  out += `<rect id="router-led" class="live flicker" x="291.2" y="111" width="1.6" height="1.6" fill="#ff4a3d"/>`;
  // the lamp over the middle of the room
  out += rect("line", 160, 0, 1, 12) + `<polygon class="light" points="151,21 170,21 166,12 155,12"/>`;
  return out;
}

// ---------- Nevada: the last stop before nothing ----------
/** A dirt lot in the desert: a shack that sells rocks and lemonade, a government fence, and tracks that stop. */
export function desertStop() {
  const text = (x, y, size, words, fill, more = "") => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="${size}" fill="${fill}"${more}>${words}</text>`;
  let out = sky() + `<circle class="light" cx="206" cy="38" r="9" shape-rendering="geometricPrecision"/>` + mesas +
    `<polygon class="far" points="96,118 104,112 130,112 136,105 164,105 172,112 200,112 206,118"/>` + ground(23);
  // scrub
  const r = rng(31);
  for (let i = 0; i < 12; i++) {
    const x = Math.floor(r() * 300) + 8, y = 122 + Math.floor(r() * 72);
    if (x > 60 && x < 270 && y > 128 && y < 190) continue;                  // keep the lot clear
    out += `<rect x="${x}" y="${y}" width="5" height="2" fill="#8a9a78"/><rect x="${x + 1}" y="${y - 1}" width="3" height="1" fill="#a3b08f"/>`;
  }
  // the fence, and what is behind it
  out += `<rect x="232" y="100" width="46" height="18" fill="#b9b6ad"/><rect x="232" y="100" width="46" height="2" fill="#d8d5cb"/><rect x="238" y="106" width="6" height="12" fill="#6b6866"/>
    <rect x="286" y="96" width="20" height="22" fill="#a7a49b"/><rect x="302" y="62" width="1" height="34" fill="#6b6866"/>
    <rect class="live tw" x="301" y="60" width="3" height="2" fill="#ff4a3d"/>`;
  out += `<rect x="186" y="84" width="134" height="38" fill="url(#mesh)"/><rect x="186" y="84" width="134" height="1" fill="#8f8a86"/><rect x="186" y="121" width="134" height="1" fill="#8f8a86"/>`;
  for (let x = 186; x < 320; x += 22) out += `<rect x="${x}" y="80" width="1.5" height="43" fill="#7b7672"/>`;
  out += `<path d="M186,81 L320,81" stroke="#7b7672" stroke-width="0.5" stroke-dasharray="2 1.5" fill="none"/>`;
  // the notice on the fence
  out += `<rect x="244" y="92" width="30" height="21" fill="#f4efe0"/><rect x="244" y="92" width="30" height="6" fill="#c8402f"/>
    <rect x="247" y="101" width="24" height="1.5" fill="#1f130a"/><rect x="249" y="104.5" width="20" height="1.5" fill="#1f130a"/><rect x="250" y="108" width="18" height="1.2" fill="#c8402f"/>
    <circle cx="246" cy="94" r="0.6" fill="#555"/><circle cx="272" cy="94" r="0.6" fill="#555"/>`;
  // the shack
  out += rect("near", 14, 80, 70, 40) + `<polygon class="feat" points="8,82 50,66 90,82"/><polygon class="feat2" points="8,82 50,66 50,69 12,84"/>`;
  for (let x = 20; x < 84; x += 7) out += rect("far", x, 84, 1, 36);
  out += rect("line", 56, 92, 16, 28) + rect("s2", 24, 94, 20, 14) + rect("light", 26, 96, 5, 3) + rect("far", 22, 92, 24, 2) + rect("far", 22, 108, 24, 2) +
    `<rect x="18" y="71" width="62" height="10" fill="#f4efe0" transform="rotate(-2 49 76)"/>` + text(49, 79, 7, "LAST STOP", "#c8402f", ` transform="rotate(-2 49 76)"`);
  out += `<polygon class="far" points="10,120 88,120 94,124 4,124"/>`;                 // the porch step
  // tracks that come in from the road and stop
  out += `<path d="M120,200 C150,186 190,176 226,170" class="stroke-line" stroke-width="1.2" fill="none" opacity="0.35"/>
    <path d="M150,200 C176,190 206,182 238,175" class="stroke-line" stroke-width="1.2" fill="none" opacity="0.35"/>`;
  // the patch where the sand turned to glass, and the air that has not settled above it
  out += `<ellipse cx="250" cy="170" rx="27" ry="7" fill="#9fd3dc"/><ellipse cx="249" cy="169.5" rx="23" ry="5.2" fill="#d9f0f2"/><polygon points="236,168 252,166 262,170 246,172" fill="#ffffff" opacity="0.7"/>
    <g class="live">${rect("light tw", 232, 169, 1, 1)}${rect("light tw d1", 258, 167, 1, 1)}${rect("light tw d2", 268, 171, 1, 1)}</g>`;
  out += `<g id="shimmer" class="live" opacity="0.42"><g class="flicker">${portal(250, 150, 6, "shimmer-rings")}</g></g>`;
  return out;
}

// ---------- close-ups: a screen or a sign, big enough to read ----------
const words = (x, y, size, what, fill = "#fff", weight = 700, anchor = "middle") =>
  `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" font-weight="${weight}" fill="${fill}">${what}</text>`;

/** The family computer. `inner` is what is on its screen, which runs from (66, 22) to (254, 140). */
export function monitor(inner) {
  return `<g shape-rendering="geometricPrecision">
    <rect x="58" y="14" width="204" height="136" rx="6" fill="#2b2a33"/><rect x="66" y="22" width="188" height="118" fill="#101822"/>
    ${inner}
    <rect x="146" y="150" width="28" height="7" fill="#22212a"/><rect x="124" y="156" width="72" height="5" rx="2" fill="#2b2a33"/><circle cx="160" cy="145" r="1.2" fill="#5ef2ff"/>
  </g>`;
}
const page = (bg, body) => `<rect x="66" y="22" width="188" height="118" fill="${bg}"/><rect x="66" y="22" width="188" height="12" fill="#16283d"/>` +
  `<circle cx="73" cy="27" r="2.8" fill="#ff6b5a"/><polygon points="70.7,28.6 75.3,28.6 73,32.6" fill="#ff6b5a"/><circle cx="73" cy="27" r="1" fill="#16283d"/>` + words(80, 30.5, 6, "FIND MY FAMILY", "#cfe3ff", 700, "start") + body;

export const screens = {
  /** The router is off: nothing to look at. */
  offline: () => page("#1b2330",
    `<rect x="141" y="58" width="14" height="10" rx="2" fill="#5d6b80"/><rect x="144" y="52" width="2" height="6" fill="#5d6b80"/><rect x="150" y="52" width="2" height="6" fill="#5d6b80"/>
     <rect x="165" y="60" width="16" height="6" rx="3" fill="#5d6b80"/><path d="M157,57 l5,12" stroke="#ff6b5a" stroke-width="1.6"/>` +
    words(160, 90, 11, "No internet.") + words(160, 102, 6, "The router is not answering.", "#9fb0c8", 400)),
  /** Signing in. `typed` is how many of the four figures are in; `shake` marks a wrong try. */
  login: (typed = 0, shake = false) => page("#20405f",
    words(160, 62, 10, "Welcome back, Dad") + words(160, 76, 6, "Password", "#cfe3ff", 400) +
    `<rect x="118" y="81" width="84" height="18" rx="2" fill="${shake ? "#ffd9d2" : "#ffffff"}"/>` +
    [0, 1, 2, 3].map((i) => (i < typed ? `<circle cx="${133 + i * 18}" cy="90" r="3.2" fill="#16283d"/>` : `<rect x="${128 + i * 18}" y="94" width="10" height="1.4" fill="#8aa0b8"/>`)).join("") +
    words(160, 114, 6, "Forgot it? Ask Dad.", "#ffe9a8", 400)),
  /** A question only one person in the house can answer. */
  question: () => page("#20405f",
    words(160, 56, 6, "This computer is new to us. One question first.", "#cfe3ff", 400) +
    words(160, 80, 9.5, "What did you promise") + words(160, 93, 9.5, "on your wedding day?") +
    `<rect x="100" y="104" width="120" height="14" rx="2" fill="#ffffff" opacity="0.92"/><rect x="106" y="110" width="1.2" height="6" fill="#16283d" class="tw"/>`),
  /** The map: a great deal of nothing, and one dot. */
  map: () => {
    let grid = "";
    for (let x = 78; x < 254; x += 16) grid += `<rect x="${x}" y="34" width="0.5" height="106" fill="#d3c9a8"/>`;
    for (let y = 46; y < 140; y += 16) grid += `<rect x="66" y="${y}" width="188" height="0.5" fill="#d3c9a8"/>`;
    const hill = (x, y) => `<path d="M${x},${y} l4,-5 l4,5 M${x + 6},${y} l3,-3.5 l3,3.5" stroke="#b9aa8a" stroke-width="0.8" fill="none"/>`;
    return page("#ece4c8", grid +
      `<path d="M66,128 C100,120 120,104 150,96 S176,90 182,88" stroke="#b9aa8a" stroke-width="3" fill="none"/><path d="M66,128 C100,120 120,104 150,96 S176,90 182,88" stroke="#fff8e0" stroke-width="0.8" stroke-dasharray="3 2" fill="none"/>` +
      hill(84, 60) + hill(214, 120) + hill(120, 76) + `<ellipse cx="222" cy="64" rx="15" ry="5" fill="#d9e9ea"/>` +
      `<circle cx="96" cy="122" r="1.6" fill="#7a6f55"/>` + words(100, 132, 5, "LAST GAS", "#7a6f55", 700, "start") + words(222, 66, 5, "DRY LAKE", "#7a8f90") + words(128, 60, 5, "NOT MUCH", "#a59a7c") +
      `<circle class="glow" cx="184" cy="87" r="9" fill="#ff6b5a" opacity="0.28"/><circle cx="184" cy="87" r="3.2" fill="#c8402f"/><circle cx="184" cy="87" r="1.2" fill="#fff"/>` +
      `<rect x="142" y="100" width="108" height="30" rx="2" fill="#ffffff"/><rect x="142" y="100" width="108" height="30" rx="2" fill="none" stroke="#c8402f" stroke-width="0.8"/>` +
      words(148, 110, 6.5, "DAD'S PHONE", "#c8402f", 700, "start") + words(148, 118, 5, "Last seen 5:47 p.m. today", "#3a3326", 400, "start") + words(148, 125.5, 5, "37 miles past Last Gas. No signal since.", "#3a3326", 400, "start") +
      `<rect x="72" y="38" width="34" height="42" rx="2" fill="#ffffff" opacity="0.9"/><polygon points="78,43 100,43 100,66 97,73 78,54" fill="#e2d8b8" stroke="#a59a7c" stroke-width="0.7"/><circle cx="90" cy="56" r="1.6" fill="#c8402f"/>` +
      words(89, 78, 4.6, "NEVADA", "#7a6f55"));
  },
};

/** The notice on the fence, close enough to read. */
export function notice() {
  const blade = (a) => { const p = (deg, rad) => `${96 + Math.cos((deg * Math.PI) / 180) * rad},${88 + Math.sin((deg * Math.PI) / 180) * rad}`; return `<path d="M${p(a - 30, 4)} L${p(a - 30, 12)} A12,12 0 0 1 ${p(a + 30, 12)} L${p(a + 30, 4)} A4,4 0 0 0 ${p(a - 30, 4)} Z" fill="#1f130a"/>`; };
  return `<g shape-rendering="geometricPrecision">
    <rect x="62" y="16" width="196" height="138" rx="3" fill="#8f8a86"/><rect x="65" y="19" width="190" height="132" rx="2" fill="#f4efe0"/>
    <rect x="65" y="19" width="190" height="30" fill="#c8402f"/>${words(160, 41, 19, "AREA CLOSED")}
    ${words(160, 60, 6, "BY ORDER", "#4a2f20")}
    <circle cx="96" cy="88" r="17" fill="#f2c230"/><circle cx="96" cy="88" r="17" fill="none" stroke="#1f130a" stroke-width="1"/><circle cx="96" cy="88" r="2.4" fill="#1f130a"/>${blade(-90)}${blade(30)}${blade(150)}
    ${words(184, 82, 11, "ELEVATED", "#1f130a")}${words(184, 96, 11, "RADIATION LEVELS", "#1f130a")}
    <rect x="76" y="112" width="168" height="0.8" fill="#4a2f20"/>
    ${words(160, 125, 10, "SECTORS 44 AND 1921", "#c8402f")}${words(160, 135, 6, "SEALED UNTIL FURTHER NOTICE", "#1f130a")}
    ${words(160, 146, 4.6, "No entry. No photographs. No questions.", "#4a2f20", 400)}
    <circle cx="70" cy="24" r="1.4" fill="#6b6866"/><circle cx="250" cy="24" r="1.4" fill="#6b6866"/><circle cx="70" cy="146" r="1.4" fill="#6b6866"/><circle cx="250" cy="146" r="1.4" fill="#6b6866"/>
  </g>`;
}

/**
 * A sheet of paper with a few lines of lettering on it, close enough to read: a notice taped to a door, the label
 * on a box. Drawn on the 800x600 picture, so it is shown with g.closeup(art.paper({...}), "label", { grid: [800, 600] }).
 * The sheet keeps to the upper part of the picture, because words spoken during a close-up run along the bottom.
 *   lines   [{ text, size, gap, anchor, fill }]: one line of lettering each. `size` is the letter height in pixels
 *           (30 if not said), `gap` the extra space left under the line, `anchor` "middle" (the usual), "start" or "end".
 *   width   of the sheet (540)        tint   the paper's color        ink   the lettering's
 *   tilt    degrees: a notice somebody put up by hand never hangs quite straight
 *   tape    true: a strip of tape across each top corner
 */
export function paper({ lines = [], width = 540, tint = "#f4efe0", ink = "#2b2622", tilt = 0, tape = true } = {}) {
  const plain = (text) => String(text).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
  const pad = 46, lead = 1.5;
  let tall = pad * 2 - 8;
  for (const l of lines) tall += (l.size || 30) * lead + (l.gap || 0);
  const x0 = (W - width) / 2, y0 = Math.max(18, (H - 96 - tall) / 2);
  let y = y0 + pad, text = "";
  for (const l of lines) {
    const size = l.size || 30, anchor = l.anchor || "middle";
    const x = anchor === "start" ? x0 + pad : anchor === "end" ? x0 + width - pad : W / 2;
    y += size;
    const slant = l.turn ? ` transform="rotate(${l.turn} ${x} ${y})"` : "";      // (a line added by another hand, not quite straight)
    text += `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" font-weight="700" fill="${l.fill || ink}"${slant}>${plain(l.text)}</text>`;
    y += size * (lead - 1) + (l.gap || 0);
  }
  const strip = (x, turn) => `<rect x="${x - 34}" y="${y0 - 10}" width="68" height="24" fill="#e9e2c4" opacity="0.82" transform="rotate(${turn} ${x} ${y0 + 2})"/>`;
  return `<g shape-rendering="geometricPrecision" transform="rotate(${tilt} ${W / 2} ${y0 + tall / 2})">
    <rect x="${x0 + 7}" y="${y0 + 9}" width="${width}" height="${tall}" fill="#07040d" opacity="0.4"/>
    <rect x="${x0}" y="${y0}" width="${width}" height="${tall}" fill="${tint}"/>
    <rect x="${x0}" y="${y0 + tall - 26}" width="${width}" height="26" fill="#000" opacity="0.05"/>
    <path d="M${x0 + 20},${y0 + tall * 0.47} h${width - 40}" stroke="#000" stroke-width="1" opacity="0.07"/>
    ${text}${tape ? strip(x0 + 44, -38) + strip(x0 + width - 44, 38) : ""}
  </g>`;
}

// ---------- inventory icons, 12x12 ----------
export const icons = {
  map: `<rect x="1" y="2" width="10" height="8" fill="#efe9da"/><rect x="4" y="2" width="1" height="8" fill="#b9b2a0"/><rect x="8" y="2" width="1" height="8" fill="#b9b2a0"/><rect x="2" y="5" width="6" height="1" fill="#c85a43"/><rect x="7" y="6" width="3" height="1" fill="#c85a43"/>`,
  reed: `<rect x="5" y="1" width="2" height="10" fill="#7a8a3c"/><rect x="5" y="4" width="2" height="1" fill="#4d5a22"/><rect x="5" y="8" width="2" height="1" fill="#4d5a22"/><rect x="5" y="10" width="2" height="1" fill="#1f130a"/>`,
  coin: `<rect x="3" y="2" width="6" height="8" fill="#d4d8de"/><rect x="2" y="3" width="8" height="6" fill="#d4d8de"/><rect x="3" y="3" width="5" height="1" fill="#f4f6f8"/><rect x="5" y="4" width="2" height="3" fill="#8e949c"/><rect x="4" y="7" width="4" height="1" fill="#8e949c"/>`,
  note: `<rect x="2" y="2" width="8" height="8" fill="#ffe36b"/><rect x="2" y="2" width="8" height="2" fill="#f2c94a"/><rect x="3" y="5" width="6" height="1" fill="#6b5a1c"/><rect x="3" y="7" width="4" height="1" fill="#6b5a1c"/><rect x="8" y="8" width="2" height="2" fill="#d9b83c"/>`,
};
export const icon = (name) => `<svg viewBox="0 0 12 12" shape-rendering="crispEdges" aria-hidden="true">${icons[name] || ""}</svg>`;
