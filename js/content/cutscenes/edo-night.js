// Cut-scene: "Mind The Fire", the walk back from the women's hall to Himeji in the dark, and "The next day" (SCENES-21C: new in
// round twenty-one, in place of MERGE-21's stub; the beat edo.night; the design, briefs/out/edo2-design.md, "Cut-Scene: Mind The
// Fire"; the lines are WRITE-21B's NIGHT, js/content/talk/edo-d.js). Played by the women's hall (edo-hall.js) once the Son has
// said "Hold hands." and the sun has gone (edo.holdHands):
//   the title     "Mind The Fire"
//   the lantern   outside the hall, the last of the red light going: O-Ume comes out with a lit paper lantern and lends it to
//                 Mom ("A lantern is a patient thing."); Mom carries it (her hold `lantern`). The scene is Shosha's own, with the
//                 dusk drawn over it (a veil in front of everybody, a pool of light round the lantern)
//   the fields    drawn here, as round twenty drew the night at sea: the dark fields and their water, the frogs (the loop), the
//                 castle a pale shape on its hill, and three small figures with a lantern on the path back
//   the gate      Himeji's own painting (Watamachi, edo-town) by night: the shutters, the kitchen door and the ward gate shut
//                 (PAINT-21E's night states), a deep blue over it, the lanterns' light; old Tōbei on his rounds with his clappers
//                 ("Hi no yōjin!"); he sees O-Ume's lantern, strikes a signal, and it is answered from far off; the gate opens,
//                 gate to gate ("We're being POSTED.")
//   O-Tane's door the light of her door; "In. Quietly."
//   the dark      inside, the lantern out: "He ATE it." "He did." "Tomorrow we hold hands."
//   the card      "The next day"; edo.nightDone; the castle approach in the late afternoon (edo-castle, `enter`)
// The people of the fields and the gate are shapes against the night (the lanterns' light on them), as the night at sea's were.
// Skipped, the same in an instant: the fact, the clothes, the castle.

import { NIGHT } from "../talk/edo-d.js";
import { nightTint } from "../scenes/edo-west.js";

const FAMILY = ["mom", "bigsis", "lilsis"];
const TOWN = "art/scenes/edo-town/";

// ---------- shapes in the dark ----------
/** A person as a shape against the night: feet at (x, y), `h` tall; a sedge hat (the family on the road), and a lantern. */
function figure(x, y, h, { hat = false, w = 0.3, fill = "#07080f", rim = null } = {}) {
  const r = h * 0.075, top = y - h, sh = y - h * 0.8, hw = (w * h) / 2;
  let s = `<path d="M${(x - hw).toFixed(1)} ${y} L${(x - hw * 0.62).toFixed(1)} ${sh.toFixed(1)} Q${x} ${(sh - h * 0.05).toFixed(1)} ${(x + hw * 0.62).toFixed(1)} ${sh.toFixed(1)} L${(x + hw).toFixed(1)} ${y} Z" fill="${fill}"/>`;
  s += `<circle cx="${x}" cy="${(top + r * 1.1).toFixed(1)}" r="${r.toFixed(1)}" fill="${fill}"/>`;
  if (hat) s += `<ellipse cx="${x}" cy="${(top + r * 0.7).toFixed(1)}" rx="${(r * 2.5).toFixed(1)}" ry="${(r * 0.75).toFixed(1)}" fill="${fill}"/>`;
  if (rim) s += `<path d="M${(x + hw * 0.62).toFixed(1)} ${sh.toFixed(1)} L${(x + hw).toFixed(1)} ${y}" stroke="${rim}" stroke-width="1.2" opacity="0.6"/>`;
  return s;
}
/** A paper lantern on a stick, lit: a warm pool round it. */
function lantern(x, y, r = 34, id = "") {
  return `<g${id ? ` id="${id}"` : ""}><circle cx="${x}" cy="${y}" r="${r}" fill="url(#mtf-glow)" style="mix-blend-mode:screen"/>`
    + `<ellipse cx="${x}" cy="${y}" rx="${(r * 0.12).toFixed(1)}" ry="${(r * 0.17).toFixed(1)}" fill="#ffe0a0"/></g>`;
}
const DEFS = `<defs><radialGradient id="mtf-glow"><stop offset="0" stop-color="#ffd890" stop-opacity="0.95"/><stop offset="0.3" stop-color="#ffaa48" stop-opacity="0.42"/>`
  + `<stop offset="1" stop-color="#ff9a30" stop-opacity="0"/></radialGradient></defs>`;
/** The three of them in a row, Mom with the lantern (her right hand), facing the way they go: feet at (x, y). */
function family(x, y, k = 1, id = "mtf-family") {
  let s = `<g id="${id}">`;
  s += figure(x - 30 * k, y - 4 * k, 77 * k, { hat: true, w: 0.29 });          // Big Sister
  s += figure(x + 26 * k, y + 2 * k, 59 * k, { hat: true, w: 0.33 });          // Little Sister
  s += figure(x, y, 82 * k, { hat: true, w: 0.29 });                           // Mom
  s += lantern(x + 14 * k, y - 44 * k, 40 * k);
  return s + "</g>";
}

/** The fields at night, 800 x 600: stars; the castle a pale shape on its hill; the flooded fields catching the starlight; the
    path back to the town; and the three of them on it with O-Ume's lantern (`x`: where they are along it). */
function fields() {
  let seed = 7;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  let s = DEFS + `<defs><linearGradient id="mtf-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03050f"/><stop offset="1" stop-color="#14204a"/></linearGradient>`
    + `<linearGradient id="mtf-field" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1630"/><stop offset="1" stop-color="#05070e"/></linearGradient></defs>`;
  s += `<rect width="800" height="600" fill="url(#mtf-sky)"/>`;
  for (let i = 0; i < 90; i++) {
    const x = rnd() * 800, y = rnd() * 260, r = 0.5 + rnd() * 1.1, tw = rnd() < 0.3;
    s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r.toFixed(2)}" fill="#e6eaff" opacity="${(0.35 + rnd() * 0.5).toFixed(2)}">${tw ? `<animate attributeName="opacity" values="0.9;0.2;0.9" dur="${(2 + rnd() * 3).toFixed(1)}s" repeatCount="indefinite"/>` : ""}</circle>`;
  }
  // the hills far off, and on one of them the castle: a pale shape, roof on roof
  s += `<path d="M0 300 Q120 278 240 292 Q380 270 520 284 Q620 262 700 276 Q760 268 800 280 L800 320 L0 320 Z" fill="#0b1226"/>`;
  s += `<path d="M560 286 Q620 250 690 284 Z" fill="#0d152c"/>`;
  s += `<g fill="#9aa4c4" opacity="0.5"><rect x="611" y="238" width="18" height="30"/><path d="M604 240 L636 240 L620 228 Z"/><rect x="614" y="218" width="12" height="12"/>`
    + `<path d="M608 220 L632 220 L620 210 Z"/><rect x="616" y="204" width="8" height="8"/><path d="M612 206 L628 206 L620 198 Z"/><rect x="600" y="266" width="40" height="10"/></g>`;
  // the fields, flooded for planting: dark, with the stars in them, in long low terraces
  s += `<rect y="316" width="800" height="284" fill="url(#mtf-field)"/>`;
  for (let i = 0; i < 8; i++) { const y = 330 + i * 34 + i * i * 2.2; s += `<path d="M0 ${y} Q400 ${y - 6} 800 ${y + 2}" stroke="#1b2848" stroke-width="${(1.2 + i * 0.5).toFixed(1)}" fill="none"/>`; }
  for (let i = 0; i < 60; i++) { const x = rnd() * 800, y = 330 + rnd() * 260; s += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${(1 + rnd() * 3).toFixed(1)}" height="1" fill="#c8d0f0" opacity="${(0.15 + rnd() * 0.3).toFixed(2)}"/>`; }
  // the path back, between the fields, from the mountain's foot (right) toward the town (left)
  s += `<path d="M820 452 Q600 470 420 486 Q240 500 -20 520" stroke="#2a2e3c" stroke-width="16" fill="none"/>`;
  s += `<path d="M820 452 Q600 470 420 486 Q240 500 -20 520" stroke="#3a3e4e" stroke-width="2" fill="none" opacity="0.6"/>`;
  return s;
}
/** Himeji by night: Watamachi's own painting under the night (layout of PAINT-21E's town: its shut states laid over it), the gate
    shut (or open), O-Tane's door lit or not, Tōbei on his rounds by his hut, with his clappers and his lantern; and `who`: the
    family's group (drawn by the script that moves it). */
function townNight(g, { gate = "shut", door = false } = {}) {
  const url = (f) => (g && g.assets && g.assets.url ? g.assets.url(TOWN + f) : new URL("../../../" + TOWN + f, import.meta.url).href);
  const img = (f, id = "") => `<image${id ? ` id="${id}"` : ""} href="${url(f)}" x="0" y="0" width="800" height="600" style="image-rendering:pixelated"/>`;
  let s = DEFS;
  for (const f of ["noren-cotton.png", "noren.png", "desks.png", "shutters-shut.png", "kitchendoor.png", "saltjar.png", "plumjar.png", "cloth.png", "ricepot.png", "pickletub.png", "well.png", "bucket-down.png"]) s += img(f);
  // the family, behind the ward gate at first (the gate is drawn over them), then out into the street
  s += family(757, 452, 0.56, "mtf-family");
  s += img(gate === "shut" ? "gate-shut.png" : "gate.png", "mtf-gate");
  // the night over all of it; the light of O-Tane's door, when she opens it; Tōbei with his clappers and his lantern
  s += nightTint("mtf-night", [], { wash: 0.78 });
  s += `<rect id="mtf-door" x="515" y="360" width="46" height="92" fill="#ffc36e" opacity="${door ? 0.55 : 0}" style="mix-blend-mode:screen"/>`;
  s += `<g id="mtf-tobei">${figure(706, 470, 76, { w: 0.34 })}<rect x="691" y="414" width="3" height="16" fill="#07080f" transform="rotate(-20 692 420)"/>`
    + `<rect x="719" y="414" width="3" height="16" fill="#07080f" transform="rotate(20 720 420)"/>${lantern(712, 440, 30)}</g>`;
  s += `<g id="mtf-lantern" style="mix-blend-mode:screen">${lantern(765, 425, 44)}</g>`;
  return s;
}

// ---------- the scene ----------
/** A veil of dusk in front of everybody on a real stage (a drawing of the scene's on the cast's front plane, as a hand is:
    g.hand), with a pool of lantern light cut into it round `at`. */
function veil(alpha = 0.55, at = null, r = 70) {
  const c = document.createElement("canvas");
  c.width = 800; c.height = 600;
  const x = c.getContext("2d");
  x.fillStyle = `rgba(10, 14, 38, ${alpha})`;
  x.fillRect(0, 0, 800, 600);
  if (at) {
    x.globalCompositeOperation = "destination-out";
    const grad = x.createRadialGradient(at[0], at[1], 0, at[0], at[1], r);
    grad.addColorStop(0, "rgba(0,0,0,0.9)"); grad.addColorStop(1, "rgba(0,0,0,0)");
    x.fillStyle = grad; x.fillRect(at[0] - r, at[1] - r, r * 2, r * 2);
    x.globalCompositeOperation = "lighter";
    const warm = x.createRadialGradient(at[0], at[1], 0, at[0], at[1], r * 0.8);
    warm.addColorStop(0, "rgba(255, 196, 110, 0.35)"); warm.addColorStop(1, "rgba(255, 160, 60, 0)");
    x.fillStyle = warm; x.fillRect(at[0] - r, at[1] - r, r * 2, r * 2);
  }
  return { canvas: c, ox: 0, oy: 0 };
}

export default async function night(g) {
  const L = (id, or) => (g.lines[id] ? g.lines[id][1] : or);
  const seen = (id) => { g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1; };
  const tweenAttr = (sel, attr, from, to, ms, fmt = (v) => v.toFixed(1)) => g.tween(ms, (k) => { const el = g.q(sel); if (el) el.setAttribute(attr, fmt(from + (to - from) * k)); });

  // ---- the title ----
  await g.fade(1, 700);
  g.dialogue.clear();
  g.stopLoop();
  g.ui.hud(false);
  await g.card(L(NIGHT.title, "Mind The Fire"), "", { plain: true, ms: 2200 });
  seen(NIGHT.title);

  // ---- the lantern: outside the hall, O-Ume lends hers ----
  await g.goto("edo-shosha", { spawn: "hall", via: "fade", card: false });
  g.ui.hud(false);
  const mom = g.actor("mom");
  const ume = g.view.cast.get("ume") || g.view.cast.addFigure("ume", "ume", 470, 474, g.sizeAt(470, 474));
  ume.place(470, 474, g.sizeAt(470, 474)); ume.hidden = false; ume.fade(1); ume.face("E");
  await g.view.cast.load();
  if (mom) { mom.look(ume.x, ume.y); ume.look(mom.x, mom.y); }
  const hand = mom ? [mom.x + 10 * mom.scale, mom.y - mom.h * mom.scale * 0.45] : [500, 420];
  g.hand("night", [0, 0], { draw: () => veil(0.5, [ume.x + 8, ume.y - 52], 64), plane: "front" });
  ume.hold(true, "lantern");
  await g.say(NIGHT.lantern[0]);
  ume.hold(false);
  if (mom) mom.hold(true, "lantern");
  g.hand("night", [0, 0], { draw: () => veil(0.5, hand, 70), plane: "front" });
  g.sfx("pickup");
  await g.say(NIGHT.lantern[1], NIGHT.lantern[2]);
  await g.wait(400);

  // ---- the fields ----
  await g.fade(1, 600);
  g.hand("night", null);
  g.view.clear();
  g.effects.drop();
  g.view.setEra("edo");
  await g.view.draw("", "The fields at night: the castle a pale shape on its hill; three small figures with a lantern on the path back.", { picture: null, live: fields() + `<g id="mtf-walk" transform="translate(0 0)">${family(700, 456, 0.62, "mtf-walkers")}</g>`, grid: [800, 600] });
  g.loop("frogs", { level: 1 });
  await g.fade(0, 700);
  const walking = tweenAttr("#mtf-walk", "transform", 0, -420, 9000, (v) => `translate(${v.toFixed(1)} ${(-v * 0.045).toFixed(1)})`);
  await g.wait(600);
  await g.say(...NIGHT.fields);
  await walking;
  await g.fade(1, 700);
  g.stopLoop("frogs");

  // ---- the gate: Himeji by night, Tōbei on his rounds ----
  g.view.clear();
  await g.view.draw("", "Himeji by night: Watamachi's street, the ward gate shut; the night man with his clappers and his lantern; a lantern behind the gate.", { picture: TOWN + "back.png", live: townNight(g), grid: [800, 600] });
  await g.fade(0, 700);
  g.sfx("clappers");
  await g.say(NIGHT.gate[0]);
  await g.wait(500);
  await g.say(NIGHT.gate[1], NIGHT.gate[2]);
  g.sfx("clappers");                                          // the signal, struck
  await g.wait(1300);
  g.sfx("clappers");                                          // and answered, from the next gate
  await g.wait(900);
  const gateEl = g.q("#mtf-gate");
  if (gateEl) gateEl.setAttribute("href", g.assets && g.assets.url ? g.assets.url(TOWN + "gate.png") : TOWN + "gate.png");
  g.sfx("shutter");
  await g.say(NIGHT.passed[0]);
  // out through the gate and along the street to O-Tane's door, the lantern with them
  const out = Promise.all([
    tweenAttr("#mtf-family", "transform", 0, 1, 4200, (k) => `translate(${(-200 * k).toFixed(1)} ${(14 * k).toFixed(1)})`),
    tweenAttr("#mtf-lantern", "transform", 0, 1, 4200, (k) => `translate(${(-200 * k).toFixed(1)} ${(14 * k).toFixed(1)})`),
  ]);
  await g.say(NIGHT.passed[1], NIGHT.passed[2]);
  await g.say(NIGHT.passed[3]);
  await out;

  // ---- O-Tane's door ----
  const door = g.q("#mtf-door");
  if (door) await g.tween(700, (k) => door.setAttribute("opacity", (0.55 * k).toFixed(2)));
  await g.say(...NIGHT.door);
  await g.wait(400);

  // ---- the dark ----
  await g.fade(1, 900);
  g.view.clear();
  await g.fade(0, 0);
  await g.wait(700);
  await g.say(...NIGHT.dark);
  await g.wait(800);

  // ---- the card, the next day, and the castle (after the skippable part: the arrival always plays as itself) ----
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.card(L(NIGHT.card, "The next day"), "", { plain: true, ms: 3200 });
  seen(NIGHT.card);
  for (const id of FAMILY) { const now = g.dressOf(id); if (now !== "edo") g.dress(id, "edo"); }
  g.flag("edo.nightDone", true);
  await g.goto("edo-castle", { spawn: "enter", via: "fade", card: false });
}
