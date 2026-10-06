// The art kit. Every drawing in the game is put together from these parts, on one
// 320x200 grid, with flat fills and hard edges. That shared kit is what keeps
// different time periods looking like one game.
//
// Colour rules (see css/tokens.css and docs/DESIGN.md):
//   ERA parts use classes (s1..s8, far, near, g1..g3, line, light, feat, feat2), so the
//     same drawing code takes on each period's palette.
//   TIME parts (portals, the tunnel) use the neon classes and never change.
//   TRAVELLERS (Dad, Son, the wagon, the road sign) carry fixed colours from the
//     present, so they always look like visitors.

export const HORIZON = 118;

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

/** Wrap scene parts in the standard frame. */
export function frame(inner, title = "") {
  return `<svg viewBox="0 0 320 200" preserveAspectRatio="xMidYMid slice" shape-rendering="crispEdges" role="img">
    ${title ? `<title>${title}</title>` : ""}${defs}${inner}</svg>`;
}

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
  return `<g class="stars">${out}</g>`;
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

/** A wormhole. The same four rings everywhere, in every era: this is the game's signature shape. */
export function portal(cx = 160, cy = 92, r = 27, id = "portal") {
  const k = r / 27;
  const ring = (cls, radius, width, dash) =>
    `<circle class="ring ${cls}" cx="${cx}" cy="${cy}" r="${radius * k}" fill="none" stroke-width="${width * k}" stroke-dasharray="${dash.map((d) => d * k).join(" ")}"/>`;
  return `<g id="${id}" class="portal" shape-rendering="geometricPrecision" style="transform-origin:${cx}px ${cy}px">
    <circle class="glow" cx="${cx}" cy="${cy}" r="${38 * k}" fill="url(#portal-glow)"/>
    ${ring("r1 t-cyan", 27, 2.5, [12, 7])}${ring("r2 t-magenta", 21, 2.5, [8, 6])}
    ${ring("r3 t-violet", 15, 2, [6, 5])}${ring("r4 t-white", 9, 1.5, [4, 3])}
    <circle class="t-core" cx="${cx}" cy="${cy}" r="${4 * k}"/>
  </g>`;
}

/** A stand-in for a scene that has not been drawn yet: sky, ground, and every
    clickable area as a labelled box. Leave `draw` out of a scene file to get this,
    and the scene is playable the moment its puzzle is written. */
export function sketch(scene) {
  const label = (x, y, words, cls) =>
    `<text class="${cls}" x="${x}" y="${y}" text-anchor="middle" font-family="Trebuchet MS, Verdana, sans-serif" font-weight="700" font-size="6" shape-rendering="geometricPrecision">${words}</text>`;
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
      `<rect class="stroke-line" x="${x + 0.5}" y="${y + 0.5}" width="${w - 1}" height="${hh - 1}" fill="none" stroke-width="1" stroke-dasharray="3 2"/>` +
      label(x + w / 2, y + hh / 2 + 2, h.name, "light");
  }).join("");
  return sky() + ground(1) + boxes + label(302, 197, "SKETCH", "line");
}

// ---------- the present: a desert highway ----------
export const mesas = `
  <polygon class="far" points="0,118 0,106 14,106 18,102 44,102 50,108 66,108 72,118"/>
  <polygon class="near" points="0,118 0,111 30,111 34,109 52,109 58,114 80,114 86,118"/>
  <polygon class="far" points="236,118 242,108 256,108 260,101 290,101 296,107 320,107 320,118"/>
  <polygon class="near" points="222,118 228,113 250,113 254,110 284,110 290,113 320,113 320,118"/>`;

export const road = `
  <polygon class="feat" points="159,118 161,118 236,200 84,200"/>
  <polygon id="road-glow-shape" fill="url(#road-glow)" points="159,118 161,118 236,200 84,200"/>
  <line class="stroke-feat2" x1="159" y1="118" x2="84" y2="200" stroke-width="1"/>
  <line class="stroke-feat2" x1="161" y1="118" x2="236" y2="200" stroke-width="1"/>
  <g fill="#f2c14e">
    <rect x="160" y="121" width="1" height="2"/><rect x="160" y="126" width="1" height="3"/>
    <rect x="159" y="133" width="2" height="4"/><rect x="159" y="142" width="2" height="6"/>
    <rect x="158" y="155" width="3" height="8"/><rect x="158" y="172" width="3" height="11"/>
    <rect x="158" y="192" width="4" height="8"/>
  </g>`;

/** The road sign. The edit (strike-through and "B.C.") is a separate group so a cutscene can reveal it. */
export const sign = `
  <rect x="247" y="166" width="2" height="18" fill="#7d8288"/><rect x="281" y="166" width="2" height="18" fill="#7d8288"/>
  <rect x="236" y="142" width="58" height="26" rx="2" fill="#1e7b4b"/>
  <rect x="238" y="144" width="54" height="22" rx="1.5" fill="none" stroke="#eaf5ee" stroke-width="1"/>
  <g shape-rendering="geometricPrecision">
    <text x="265" y="153.5" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="8" fill="#eaf5ee" textLength="40" lengthAdjust="spacingAndGlyphs">POINT B</text>
    <g id="sign-edit">
      <line id="sign-strike" x1="242" y1="151.5" x2="288" y2="149.5" stroke="#ff4a3d" stroke-width="1.6" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0"/>
      <g id="sign-bc">
        <text x="256" y="164" text-anchor="middle" font-family="'Koine Road', Arial, Helvetica, sans-serif" font-size="10.5" fill="#ffd23f">B.C.</text>
        <polygon fill="#ffd23f" points="272,159 281,159 281,156 287,160.5 281,165 281,162 272,162"/>
      </g>
    </g>
  </g>`;

/** The dusk highway used by the intro and the title screen. */
export function highway({ sun = false } = {}) {
  return sky() + stars(11, 30) +
    (sun ? `<circle id="sun" class="s8" cx="160" cy="104" r="15" shape-rendering="geometricPrecision"/>` : "") +
    portal(160, 92, 27) + mesas + ground(3) + road + sign;
}

// ---------- ancient Egypt: a riverbank at dawn ----------
export const pyramids = `
  <polygon class="far" points="186,118 222,82 258,118"/><polygon class="near" points="222,82 258,118 232,118"/>
  <polygon class="far" points="244,118 270,92 296,118"/><polygon class="near" points="270,92 296,118 278,118"/>`;

export function river() {
  let ripples = "";
  const r = rng(21);
  for (let i = 0; i < 12; i++) {
    const y = 122 + Math.floor(r() * 50), x = Math.floor(r() * 70 * (1 - (y - 122) / 110)) + 4;
    ripples += rect(`feat2${r() < 0.5 ? " ripple" : ""}`, x, y, 3 + Math.floor(r() * 5), 1);
  }
  return `<polygon class="feat" points="0,118 128,118 104,134 76,152 40,172 0,186"/>${ripples}`;
}

export function reeds(x = 70, y = 166, count = 9, seed = 5) {
  const r = rng(seed);
  let out = "";
  for (let i = 0; i < count; i++) {
    const rx = x + i * 4 + Math.floor(r() * 2), h = 14 + Math.floor(r() * 12);
    out += `<g class="sway" style="animation-delay:${(-r() * 3).toFixed(2)}s">${rect("line", rx, y - h, 1, h)}${rect("near", rx - 1, y - h - 3, 3, 4)}</g>`;
  }
  return `<g id="reeds">${out}</g>`;
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

export const fountain = `
  <ellipse cx="232" cy="169" rx="32" ry="2.5" fill="#000" opacity="0.25" shape-rendering="geometricPrecision"/>
  ${rect("g1", 229, 134, 6, 22)}${rect("line", 233, 134, 2, 22, ' opacity="0.25"')}${rect("light", 220, 132, 24, 3)}
  ${rect("s2 ripple", 222, 135, 2, 20)}${rect("s2", 240, 135, 2, 20)}
  ${rect("g1", 204, 156, 56, 12)}${rect("line", 204, 164, 56, 4, ' opacity="0.22"')}${rect("light", 202, 153, 60, 4)}${rect("s2", 206, 154, 52, 2)}
  ${rect("light ripple", 212, 154, 5, 1)}${rect("light", 238, 154, 6, 1)}${rect("light ripple", 226, 155, 3, 1)}`;

// ---------- sprites: small drawings that move ----------
const SKIN = "#e9b98f";
const legs = (xa, xb, y, len, skin, sock, shoe, wide) => {
  const one = (x) => rect("", x, y, 2, len, ` fill="${skin}"`) + (sock ? rect("", x, y + len, 2, 4, ` fill="${sock}"`) : "") +
    rect("", x, y + len + (sock ? 4 : 0), 4, 2, ` fill="${shoe}"`);
  return `<g class="f1">${one(xa)}${one(xb)}</g><g class="f2">${one(xa - wide)}${one(xb + wide)}</g>`;
};
const shadow = (cx, cy, rx) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="1.6" fill="#000" opacity="0.35" shape-rendering="geometricPrecision"/>`;

export const sprites = {
  // Dad: holiday shirt, shorts, socks and sandals. His shirt is his subtitle colour.
  dad: { w: 16, h: 34, svg: `${shadow(8, 33.4, 7)}
    <rect x="5" y="0" width="7" height="3" fill="#5a3b22"/><rect x="5" y="1" width="2" height="4" fill="#5a3b22"/>
    <rect x="6" y="2" width="6" height="6" fill="${SKIN}"/><rect x="10" y="4" width="1" height="1" fill="#1f130a"/>
    <rect x="9" y="6" width="4" height="1" fill="#5a3b22"/><rect class="mouth" x="10" y="7" width="2" height="1" fill="#7a2f22"/>
    <rect x="4" y="8" width="9" height="11" fill="#e8b93a"/><rect x="8" y="8" width="3" height="2" fill="${SKIN}"/>
    <rect x="5" y="11" width="1" height="1" fill="#c9562f"/><rect x="11" y="13" width="1" height="1" fill="#c9562f"/><rect x="5" y="16" width="1" height="1" fill="#c9562f"/><rect x="10" y="17" width="1" height="1" fill="#c9562f"/>
    <rect x="7" y="10" width="3" height="7" fill="#c99a25"/><rect x="7" y="17" width="3" height="2" fill="${SKIN}"/>
    <rect x="4" y="19" width="9" height="5" fill="#6f7f5a"/>
    ${legs(5, 9, 24, 4, SKIN, "#f4f1e6", "#6e4b2e", 2)}` },
  // Son: red cap, blue hoodie, backpack.
  son: { w: 14, h: 26, svg: `${shadow(7, 25.4, 6)}
    <rect x="3" y="0" width="7" height="3" fill="#d2452f"/><rect x="9" y="2" width="3" height="1" fill="#d2452f"/>
    <rect x="4" y="3" width="6" height="5" fill="${SKIN}"/><rect x="3" y="3" width="2" height="3" fill="#3b2a1c"/>
    <rect x="8" y="5" width="1" height="1" fill="#1f130a"/><rect class="mouth" x="8" y="7" width="2" height="1" fill="#7a2f22"/>
    <rect x="3" y="8" width="8" height="8" fill="#49bfe0"/><rect x="1" y="9" width="3" height="6" fill="#7a5ad1"/>
    <rect x="6" y="9" width="2" height="6" fill="#2f9fc2"/><rect x="6" y="15" width="2" height="1" fill="${SKIN}"/>
    <rect x="3" y="16" width="8" height="3" fill="#39415e"/>
    ${legs(4, 8, 19, 5, SKIN, null, "#f4f1e6", 1)}` },
  // A scribe, sitting cross-legged with his palette. Era colours where the cloth is.
  scribe: { w: 22, h: 22, svg: `${shadow(11, 21.4, 10)}
    <rect x="7" y="0" width="8" height="6" fill="#1b1410"/><rect x="8" y="2" width="6" height="5" fill="#b9793f"/>
    <rect x="9" y="4" width="1" height="1" fill="#1b1410"/><rect class="mouth" x="8" y="6" width="2" height="1" fill="#5a2418"/>
    <rect x="7" y="7" width="8" height="7" fill="#b9793f"/><rect class="feat" x="7" y="7" width="8" height="2"/><rect class="s7" x="9" y="8" width="4" height="1"/>
    <rect x="4" y="10" width="4" height="2" fill="#b9793f"/><rect class="g1" x="0" y="11" width="6" height="3"/>
    <rect class="light" x="4" y="14" width="14" height="5"/><rect x="2" y="18" width="18" height="3" fill="#b9793f"/>` },
  // The family wagon, seen from behind.
  wagon: { w: 40, h: 34, svg: `${shadow(20, 33, 22)}<g transform="translate(-164,-149)">
    <rect x="172" y="152" width="24" height="3" fill="#6e4b2e"/><rect x="175" y="150" width="9" height="2" fill="#9a7445"/><rect x="186" y="150" width="6" height="2" fill="#4f6b8a"/>
    <rect x="169" y="155" width="30" height="11" fill="#b8503c"/><rect x="172" y="157" width="24" height="7" fill="#232842"/>
    <rect x="175" y="159" width="5" height="5" fill="#0e1120"/><rect x="187" y="160" width="4" height="4" fill="#0e1120"/><rect x="193" y="158" width="2" height="1" fill="#6b7aa8"/>
    <rect x="166" y="166" width="36" height="10" fill="#c85a43"/><rect x="166" y="170" width="36" height="2" fill="#7d5131"/>
    <rect x="167" y="167" width="4" height="3" fill="#ff3434"/><rect x="197" y="167" width="4" height="3" fill="#ff3434"/>
    <rect x="179" y="172" width="10" height="4" fill="#efe9da"/><rect x="181" y="173" width="6" height="1" fill="#3a3343"/>
    <rect x="165" y="176" width="38" height="2" fill="#a3a8ad"/><rect x="168" y="178" width="6" height="3" fill="#0d0b10"/><rect x="194" y="178" width="6" height="3" fill="#0d0b10"/>
    <g shape-rendering="geometricPrecision"><circle cx="169" cy="168.5" r="6" fill="url(#tail-glow)"/><circle cx="199" cy="168.5" r="6" fill="url(#tail-glow)"/></g></g>` },
};

/** A sprite as stand-alone SVG markup. */
export function sprite(name) {
  const s = sprites[name];
  return `<svg viewBox="0 0 ${s.w} ${s.h}" shape-rendering="crispEdges" aria-hidden="true">${name === "wagon" ? defs : ""}${s.svg}</svg>`;
}

/** A sprite placed inside a scene drawing (for things that never move). */
export function prop(name, x, y, { rotate = 0, scale = 1 } = {}) {
  const s = sprites[name];
  return `<g transform="translate(${x - (s.w * scale) / 2},${y - s.h * scale}) rotate(${rotate} ${(s.w * scale) / 2} ${s.h * scale}) scale(${scale})">${s.svg}</g>`;
}

// ---------- inventory icons, 12x12 ----------
export const icons = {
  map: `<rect x="1" y="2" width="10" height="8" fill="#efe9da"/><rect x="4" y="2" width="1" height="8" fill="#b9b2a0"/><rect x="8" y="2" width="1" height="8" fill="#b9b2a0"/><rect x="2" y="5" width="6" height="1" fill="#c85a43"/><rect x="7" y="6" width="3" height="1" fill="#c85a43"/>`,
  reed: `<rect x="5" y="1" width="2" height="10" fill="#7a8a3c"/><rect x="5" y="4" width="2" height="1" fill="#4d5a22"/><rect x="5" y="8" width="2" height="1" fill="#4d5a22"/><rect x="5" y="10" width="2" height="1" fill="#1f130a"/>`,
  coin: `<rect x="3" y="2" width="6" height="8" fill="#e3b436"/><rect x="2" y="3" width="8" height="6" fill="#e3b436"/><rect x="5" y="4" width="2" height="4" fill="#a87f1c"/>`,
};
export const icon = (name) => `<svg viewBox="0 0 12 12" shape-rendering="crispEdges" aria-hidden="true">${icons[name] || ""}</svg>`;
