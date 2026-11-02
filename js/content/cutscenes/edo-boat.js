// Cut-scene: "The Kyoto Boat" (SCENES-21B: new in round twenty-one, in place of MERGE-21's stub; the beat edo.boat, needs
// edo.troupeTaken and edo.sheetRead, sets edo.boated; the design, briefs/out/edo2-design.md, "Cut-Scene: The Kyoto Boat";
// every line is WRITE-21A's, js/content/lines/edo-c.en.js, its order talk/edo-c.js BOAT). It is played in the Inari theatre
// (edo-theatre.js jubeiTalk) once Jūbei has taken the three of them on as the troupe's carriers and Senzō has read them the
// broadsheet: morning, up the river, round Osaka, and north into the hills.
//
//   the card    "The Kyoto Boat"
//   Hachikenya  morning at the landing: the thirty-koku passenger boat, twenty-eight passengers pressed together, four
//               boatmen, the troupe's boxes, the three of them among the boxes (BOAT .1 to .3)
//   upriver     against the current, the boat hauled by a gang of men on the bank on a long rope (.4, .5: "Like a KITE.")
//   Hirakata    the food boats alongside with their call ("Won't ya stuff some rice?"), counting the bowls (.6 to .9: the voice
//               `foodboat`, world.js's)
//   the ferry   off at Hirakata; the ferry across to the Takatsuki side; goodbye to the troupe (.10 to .14)
//   the map    the portraits up the river path to Hirakata (its picture comes in at the river's turn: the stop named in the
//               first part, PAINT-21F's), then by the road north to the hills (ENGINE-21's journey in two parts: "haul", then
//               "sandals")
//   the rain    the road north at dusk, the first drops, a path up into the hills for shelter (.15 to .17)
//   the card    "The hills"; edo.boated; and round twenty's cedar path (edo-cedars, `enter`), the hats on for the rain.
// Skipped, the same: edo.boated, the hats on, the cedar path.
// Nobody painted the river: its moments are drawn here, as pictures over the stage (g.closeup), as round twenty's voyage
// draws the ship by night (cutscenes/edo-sail.js): flat masses, banded skies, a Prussian-blue line, the three of them as
// small shapes in their borrowed colours (Mom green, Big Sister indigo, Little Sister pink).

import { BOAT } from "../talk/edo-c.js";
import { THREE, cardWords } from "../scenes/edo-yui.js";

// ---------- the pictures (800 x 600 each) ----------
const INK = "#24305c";
let seed = 1;
const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
const f = (n) => n.toFixed(1);
/** A banded sky, top to bottom. */
const sky = (bands, h = 300) => bands.map((c, i) => `<rect y="${f((i * h) / bands.length)}" width="800" height="${f(h / bands.length + 1)}" fill="${c}"/>`).join("");
/** Water in bands, with a few light strokes on it. */
function water(y0, y1, bands, lights = 30, color = "#e8eef0") {
  let s = bands.map((c, i) => `<rect y="${f(y0 + ((y1 - y0) * i) / bands.length)}" width="800" height="${f((y1 - y0) / bands.length + 1)}" fill="${c}"/>`).join("");
  for (let i = 0; i < lights; i++) { const y = y0 + 4 + rnd() * (y1 - y0 - 8), w = 8 + rnd() * 26; s += `<rect x="${f(rnd() * 800)}" y="${f(y)}" width="${f(w)}" height="1.4" fill="${color}" opacity="0.55"/>`; }
  return s;
}
/** A person, small, as a flat shape: a robe, a head, a hat (a sedge hat, a towel, or none). */
function person(x, y, k, coat, { hat = "none", lean = 0, arms = null } = {}) {
  let p = `<g transform="translate(${f(x)} ${f(y)}) scale(${f(k)}) skewX(${lean})">`;
  p += `<path d="M-8 -50 L8 -50 L11 0 L-11 0 Z" fill="${coat}" stroke="${INK}" stroke-width="1"/><circle cx="0" cy="-57" r="6.5" fill="#d9b38c" stroke="${INK}" stroke-width="0.8"/>`;
  if (hat === "sedge") p += `<path d="M-14 -58 L0 -70 L14 -58 Z" fill="#c8b070" stroke="${INK}" stroke-width="0.8"/>`;
  else if (hat === "towel") p += `<rect x="-6.5" y="-64" width="13" height="4" fill="#e8e2d2"/>`;
  else if (hat === "knot") p += `<rect x="-2" y="-67" width="4" height="5" fill="#1c1a20"/>`;
  if (arms) p += `<path d="M-7 -44 L${arms[0]} ${arms[1]}" stroke="${coat}" stroke-width="5" stroke-linecap="round"/>`;
  return p + `</g>`;
}
/** The three of them in O-Tami's kimonos, a little apart (`at`, the middle one's feet). */
function three(x, y, k, hat = "sedge") {
  return person(x - 22 * k, y, k * 1.08, "#2e8a5a", { hat }) + person(x, y + 2 * k, k, "#3e4e9a", { hat }) + person(x + 20 * k, y + 4 * k, k * 0.76, "#d86a96", { hat });
}
/** The thirty-koku boat: long and low, a mat roof over its middle, packed with heads; `boxes` the troupe's (wicker, at its stern). */
function boat(x, y, len, k = 1, { boxes = true, roofed = true, poles = true } = {}) {
  let s = `<g transform="translate(${f(x)} ${f(y)}) scale(${f(k)})">`;
  s += `<path d="M0 0 L${len} 0 L${len - 34} 22 L26 22 Z" fill="#6a4a2c" stroke="${INK}" stroke-width="1.5"/>`;
  s += `<rect x="18" y="-4" width="${len - 40}" height="5" fill="#8a6a42"/>`;
  // the passengers, pressed together: a row of heads and shoulders
  for (let i = 0; i < 26; i++) {
    const hx = 40 + ((len - 110) * i) / 25 + rnd() * 4, c = ["#5a6f8f", "#7d6a52", "#4f6a5a", "#8a5a4a", "#6a6a7a", "#9a8a6a"][i % 6];
    s += `<path d="M${f(hx - 7)} 0 L${f(hx + 7)} 0 L${f(hx + 5)} -12 L${f(hx - 5)} -12 Z" fill="${c}"/><circle cx="${f(hx)}" cy="-16" r="4.5" fill="#d9b38c"/>`;
  }
  if (roofed) s += `<path d="M${f(len * 0.28)} -24 L${f(len * 0.70)} -24 L${f(len * 0.72)} -18 L${f(len * 0.26)} -18 Z" fill="#b8a070" stroke="${INK}" stroke-width="1"/>`
    + `<rect x="${f(len * 0.29)}" y="-18" width="3" height="18" fill="#5a4026"/><rect x="${f(len * 0.68)}" y="-18" width="3" height="18" fill="#5a4026"/>`;
  if (boxes) for (let i = 0; i < 4; i++) s += `<rect x="${f(len - 92 + i * 15)}" y="${-12 - (i % 2) * 9}" width="16" height="10" fill="#c49a5a" stroke="${INK}" stroke-width="0.8"/>`;
  if (poles) for (const [px, d] of [[10, -1], [len - 12, 1]]) s += `<line x1="${px}" y1="-30" x2="${px + d * 26}" y2="30" stroke="#3a2a18" stroke-width="2.5"/>`;
  return s + `</g>`;
}

/** Hachikenya, morning: the landing, an inn's roofs and a lantern on a post; the boat along the stone steps, boarding. */
function hachikenya() {
  seed = 3;
  let s = sky(["#f4ecd6", "#ecdcb8", "#c8d4dc", "#9cb4cc", "#7c9cc0"].reverse(), 250);
  s += `<path d="M0 238 L120 226 L240 232 L380 220 L520 230 L660 222 L800 232 L800 252 L0 252 Z" fill="#8a96a8"/>`;      // the far bank, the town in haze
  for (let x = 10; x < 800; x += 40 + rnd() * 30) s += `<rect x="${f(x)}" y="${f(226 + rnd() * 10)}" width="${f(26 + rnd() * 20)}" height="18" fill="#a4a8b4"/>`;
  s += water(250, 600, ["#6f93a8", "#5f849c", "#4e7590", "#43677f", "#3a5e76", "#335670"], 56);
  // the landing at the left: stone steps, a timber stage over the water, the inn's roofs, a lantern on a post
  s += `<path d="M0 300 L190 300 L230 470 L0 470 Z" fill="#9a8e78" stroke="${INK}" stroke-width="1.5"/>`;
  for (let i = 0; i < 7; i++) s += `<line x1="0" y1="${310 + i * 22}" x2="${f(192 + i * 6)}" y2="${310 + i * 22}" stroke="#7a705c" stroke-width="2"/>`;
  s += `<path d="M-10 300 L60 210 L190 210 L240 300 Z" fill="#4a5068" stroke="${INK}" stroke-width="1.5"/><rect x="10" y="236" width="170" height="64" fill="#e6dcc4" stroke="${INK}" stroke-width="1"/>`;
  s += `<rect x="40" y="250" width="24" height="50" fill="#3a3a52"/><rect x="100" y="246" width="56" height="20" fill="#c4b494"/>`;
  s += `<rect x="226" y="196" width="4" height="110" fill="#3a2a18"/><rect x="216" y="196" width="24" height="30" rx="6" fill="#e8c070" stroke="${INK}" stroke-width="1"/>`;
  // the boat along the landing, boarding: the troupe's boxes going in, the three among them; Jūbei in black at the stern
  s += boat(230, 392, 520, 1);
  s += three(612, 392, 0.62, "sedge");
  s += person(694, 392, 0.66, "#1c1c24", { hat: "knot" });
  // the morning sun low over the far bank
  s += `<circle cx="660" cy="130" r="26" fill="#fff4cc" opacity="0.9"/>`;
  // the landing's timber stage in front, out over the water, its posts in it
  s += `<path d="M0 500 L560 528 L560 548 L0 522 Z" fill="#8a6a42" stroke="${INK}" stroke-width="1.5"/>`;
  for (let x = 30; x < 560; x += 60) s += `<rect x="${x}" y="${f(518 + x * 0.05)}" width="7" height="80" fill="#5a4026" stroke="${INK}" stroke-width="0.8"/>`;
  for (let i = 0; i < 9; i++) s += `<line x1="${i * 62}" y1="${f(500 + i * 3.1)}" x2="${i * 62}" y2="${f(522 + i * 3.1)}" stroke="#6a4e30" stroke-width="1.5"/>`;
  return s;
}
/** Upriver, against the current: the boat on its long rope, hauled by a gang of men on the bank, leaning into it. */
function hauled() {
  seed = 5;
  let s = sky(["#7fa0c8", "#9cb6d2", "#c4d4e0", "#e8e4d0"], 230);
  s += `<path d="M0 214 L90 196 L180 206 L300 186 L420 204 L560 190 L680 206 L800 196 L800 236 L0 236 Z" fill="#7e9a8a"/>`;      // low hills, far
  s += `<rect y="232" width="800" height="22" fill="#a8b886"/>`;                                                               // the far bank's fields
  s += water(252, 420, ["#6a8ea2", "#5c8298", "#4f768c"], 34);
  for (let i = 0; i < 18; i++) s += `<line x1="${f(20 + rnd() * 760)}" y1="252" x2="${f(20 + rnd() * 760)}" y2="${f(242 + rnd() * 6)}" stroke="#7a8a5a" stroke-width="1.5"/>`;      // reeds
  // the near bank, the towpath, and the gang on it
  s += `<path d="M0 420 L800 404 L800 600 L0 600 Z" fill="#b8a578"/><path d="M0 420 L800 404 L800 414 L0 432 Z" fill="#9a8a5e"/>`;
  s += boat(120, 330, 300, 0.8, { poles: false });
  s += `<line x1="318" y1="324" x2="318" y2="262" stroke="#3a2a18" stroke-width="3"/>`;                                       // the short towing mast, forward, the rope runs from
  s += `<path d="M318 266 Q 520 330 772 440" fill="none" stroke="#5a4a32" stroke-width="2"/>`;                                   // the long rope to the gang on the bank
  for (let i = 0; i < 11; i++) s += person(470 + i * 30, 448 + i * 3.4, 0.8, ["#6a5a44", "#4f5a6a", "#7a6448"][i % 3], { hat: "towel", lean: -16, arms: [10, -60] });
  s += three(210, 316, 0.42, "sedge");
  return s;
}
/** Hirakata: the boat brought in at the landing, and the food boats alongside: a man standing with bowls held up, a pot
    steaming, another counting on his fingers. */
function foodboats() {
  seed = 9;
  let s = sky(["#86a6cc", "#a6bdd6", "#d4dcdc", "#f0e4c4"], 240);
  s += `<path d="M0 230 L130 214 L300 222 L470 206 L640 220 L800 210 L800 246 L0 246 Z" fill="#8a9c88"/>`;
  // Hirakata's bank: inn roofs along the water, a landing of planks
  for (let x = 0; x < 800; x += 92) s += `<path d="M${x - 8} 252 L${x + 14} 230 L${x + 78} 230 L${x + 100} 252 Z" fill="#4a5068" stroke="${INK}" stroke-width="1"/><rect x="${x}" y="252" width="92" height="26" fill="#e6dcc4" stroke="${INK}" stroke-width="0.8"/>`;
  s += water(278, 600, ["#6f93a8", "#628aa0", "#567e96", "#4a728a", "#406680"], 50);
  s += boat(160, 420, 520, 1);
  s += three(560, 420, 0.6, "sedge");
  // two food boats alongside, nearer, low: bowls held up, a pot with its steam
  for (const [x, y] of [[220, 520], [470, 540]]) {
    s += `<path d="M${x} ${y} L${x + 170} ${y} L${x + 150} ${y + 18} L${x + 14} ${y + 18} Z" fill="#5a3e24" stroke="${INK}" stroke-width="1.2"/>`;
    s += `<ellipse cx="${x + 120}" cy="${y - 10}" rx="16" ry="12" fill="#3a3430" stroke="${INK}" stroke-width="1"/>`;
    for (let i = 0; i < 3; i++) s += `<path d="M${x + 112 + i * 6} ${y - 24} q -6 -12 0 -24" fill="none" stroke="#eef0f0" stroke-width="2" opacity="0.6"/>`;
    s += person(x + 50, y, 0.9, "#6a5440", { hat: "towel", arms: [16, -78] });
    s += `<ellipse cx="${x + 66}" cy="${y - 80}" rx="9" ry="4" fill="#d8c8a0" stroke="${INK}" stroke-width="0.8"/><ellipse cx="${x + 64}" cy="${y - 86}" rx="9" ry="4" fill="#d8c8a0" stroke="${INK}" stroke-width="0.8"/>`;
  }
  return s;
}
/** Off at Hirakata: the ferry across to the Takatsuki side, the three of them in it with the ferryman; the passenger boat
    going on upriver with the troupe, Jūbei in black at its stern. */
function ferry() {
  seed = 13;
  let s = sky(["#8aa6c8", "#a8bcd2", "#cfd4d0", "#e8dcbc"], 250);
  s += `<path d="M0 238 L160 222 L320 234 L470 214 L620 228 L800 218 L800 256 L0 256 Z" fill="#7e9480"/>`;
  s += water(254, 520, ["#6c90a6", "#5f869c", "#527a90", "#486f86"], 40);
  s += boat(470, 300, 300, 0.62, { poles: true });
  s += person(640, 296, 0.46, "#1c1c24", { hat: "knot", arms: [-14, -54] });                                                    // Jūbei, at the stern, a hand up
  // the ferry, nearer, crossing to the left: the ferryman with his pole, the three of them
  s += `<path d="M150 430 L410 430 L390 452 L170 452 Z" fill="#6a4a2c" stroke="${INK}" stroke-width="1.5"/>`;
  s += person(380, 430, 0.8, "#5a5040", { hat: "towel" }) + `<line x1="392" y1="356" x2="430" y2="470" stroke="#3a2a18" stroke-width="3"/>`;
  s += three(250, 430, 0.8, "sedge");
  // the near bank, the Takatsuki side, with a path going off north
  s += `<path d="M0 520 L800 500 L800 600 L0 600 Z" fill="#a89a70"/><path d="M60 600 Q 140 540 210 516" fill="none" stroke="#c8b888" stroke-width="16"/>`;
  return s;
}
/** The road north at dusk, the first rain: fields, the hills dark ahead, a path going up into the trees, the three of them on
    the road with their hats on, small. The rain falls as the prints draw it: fine straight lines, all one slant. */
function rainRoad() {
  seed = 17;
  let s = sky(["#2c3450", "#3c4660", "#525a70", "#6a6a78", "#86808a"], 300);
  s += `<path d="M0 300 L110 236 L210 270 L330 206 L460 262 L560 214 L690 258 L800 226 L800 330 L0 330 Z" fill="#26302e"/>`;      // the hills, dark
  s += `<path d="M0 330 L800 316 L800 600 L0 600 Z" fill="#4c5638"/>`;
  for (let i = 0; i < 9; i++) s += `<path d="M0 ${f(352 + i * 30)} L800 ${f(340 + i * 31)}" stroke="#5c6644" stroke-width="2"/>`;      // the field's rows
  s += `<path d="M380 600 Q 420 450 520 360 Q 560 326 600 300" fill="none" stroke="#8a826a" stroke-width="22" stroke-linecap="round"/>`;      // the road, and the path going up
  s += `<path d="M560 330 Q 600 290 640 270" fill="none" stroke="#6a6450" stroke-width="10"/>`;
  s += three(470, 470, 0.9, "sedge");
  // the rain: fine slanting lines over everything (an animation: it falls)
  let r = `<g opacity="0.55"><animateTransform attributeName="transform" type="translate" values="0 -40; 6 0" dur="0.5s" repeatCount="indefinite"/>`;
  for (let i = 0; i < 160; i++) { const x = rnd() * 840 - 20, y = rnd() * 640 - 40, l = 10 + rnd() * 12; r += `<line x1="${f(x)}" y1="${f(y)}" x2="${f(x + l * 0.12)}" y2="${f(y + l)}" stroke="#d6dee8" stroke-width="1"/>`; }
  return s + r + `</g>`;
}

/** The five pictures, by name (for a look at them: tools, tests). */
export const PICTURES = { hachikenya, hauled, foodboats, ferry, rainRoad };

// ---------- the cut-scene ----------
const say = (g, ...ids) => g.say(...ids);
const L = (id) => BOAT[BOAT.indexOf(id)];                          // (the sequence's own ids, in its order)

export default async function boatRun(g) {
  g.dialogue.clear();
  g.caption(null);
  for (const id of g.view.cast.items.keys()) { const a = g.actor(id); if (a && a.fade) a.fade(0); }      // (the theatre's people off the stage under the pictures)
  await g.fade(1, 800);
  g.stopLoop();
  g.music("edo");
  await g.card(cardWords(g, L("edo.card.boat.title"), "The Kyoto Boat"), "", { plain: true, ms: 2600 });
  // Hachikenya, in the morning: into the boat, among the boxes
  g.closeup(hachikenya(), "Morning at the Hachikenya landing: the long passenger boat packed with people, the troupe's boxes, and the three of them among the boxes", { grid: [800, 600] });
  await g.fade(0, 800);
  g.sfx("creak");
  await g.wait(600);
  await say(g, BOAT[1], BOAT[2], BOAT[3]);
  await g.wait(400);
  // upriver, against the current, hauled from the bank
  await g.fade(1, 600);
  g.closeup(hauled(), "Upriver: the boat on a long rope, hauled against the current by a gang of men leaning into it on the bank", { grid: [800, 600] });
  await g.fade(0, 700);
  g.sfx("haul");
  await g.wait(700);
  await say(g, BOAT[4], BOAT[5]);
  await g.wait(400);
  // Hirakata: the food boats alongside, and their call; the bowls counted
  await g.fade(1, 600);
  g.closeup(foodboats(), "Hirakata: two food boats come alongside, a man holding bowls up, a pot steaming", { grid: [800, 600] });
  await g.fade(0, 700);
  await g.wait(400);
  await say(g, BOAT[6], BOAT[7], BOAT[8], BOAT[9]);
  await g.wait(300);
  // off at Hirakata, the ferry to the Takatsuki side; goodbye to the troupe
  await g.fade(1, 600);
  g.closeup(ferry(), "The ferry across to the Takatsuki side, the three of them in it; the troupe's boat going on upriver, Jūbei at its stern", { grid: [800, 600] });
  await g.fade(0, 700);
  g.sfx("creak");
  await g.wait(400);
  await say(g, BOAT[10], BOAT[11], BOAT[12], BOAT[13], BOAT[14]);
  await g.wait(500);
  // the map: up the river path to Hirakata (its picture at the river's turn), then the road north to the hills
  await g.fade(1, 600);
  g.closeup();
  g.flag("edo.boated", true);
  for (const id of THREE) if (g.dressOf(id) !== "edo") g.dress(id, "edo");          // (out on the road: the hats on, and the girls out of the theatre's black)
  await g.journey("edo", "osaka", "hills", { segments: [{ to: "hirakata", sound: "haul", stops: ["hirakata"] }, { to: "hills", sound: "sandals" }] });
  // the road north at dusk, and the rain
  g.closeup(rainRoad(), "The road north at dusk, the first rain falling; the hills dark ahead and a path going up into the trees", { grid: [800, 600] });
  g.loop("rain", { level: 0.6 });
  await g.fade(0, 900);
  await g.wait(500);
  await say(g, BOAT[15], BOAT[16], BOAT[17]);
  await g.wait(600);
  await g.fade(1, 800);
  g.closeup();
  await g.card(cardWords(g, L("edo.card.boat.hills"), "The hills"), "", { plain: true, ms: 2400 });
  // the skippable part ends here: whatever was skipped, the hills are reached the same way
  g.flag("edo.boated", true);
  for (const id of THREE) if (g.dressOf(id) !== "edo") g.dress(id, "edo");
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.goto("edo-cedars", { via: "cut", spawn: "enter", card: false });
}
