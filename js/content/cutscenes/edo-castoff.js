// Cut-scene: "Casting Off", the ship at first light (SCENES-21A: new in round twenty-one, in place of MERGE-21's stub; the beat
// edo.castoff, which needs edo.west and edo.when and sets edo.aboard; the design, briefs/out/edo2-design.md, "Cut-Scene:
// Casting Off"; the lines are WRITE-21A's CASTOFF, talk/edo-c.js, and round twenty's box, edo.sail.box.1, .2). It is played
// by the village after round twenty's goodbyes, which it says at first light in the street (edo-village.js `depart`).
//
//   the card    "Casting Off"
//   the beach   O-Masa at the ship's boat, beside the tender at the water's edge: her nephew cooks on that ship, Kōta,
//               twelve: "Be kind about the rice." (the plant of #27). On the village's own stage, its people where the goodbyes
//               left them.
//   the boat    the ship's boat rows them out to Gonroku's ship at anchor, Yui behind them, Fuji pink at first light (a
//               picture over the stage, as round twenty's night at sea is: nobody painted it): "Wave to Yui, girls."
//   aboard      the windlass, the yard going up the mast a heave at a time ("Heave." "And heave."), the great sail falling
//               open and filling ("It's BREATHING."; Denzō: "Woven, not sewn."); the purser counts them as cargo;
//               Gonroku's terms again, in weather
//   the night   the first night at sea, the box of sushi eaten at the rail (round twenty's lines: "At night" is true here;
//               the sushibox is taken from whoever carries it), round twenty's picture of the ship by night
//   the card    "Four days later"; edo.aboard; the hats on; the map: the portraits out along the sea path to the ship's
//               place at sea (g.journey("edo", "yui", "sea")); the deck (edo-deck.js), on the mark `deck`
// Skipped, the same: the facts, the box gone, the clothes, the deck.

import { THREE, cardWords, walkOf, look } from "../scenes/edo-yui.js";
import { nightAtSea } from "./edo-sail.js";

/** A seeded random number (the pictures are the same every time). */
const seeded = (s) => () => { s = (s * 16807) % 2147483647; return s / 2147483647; };

/** The dawn sky and sea of Suruga Bay, 800 x 600 (both pictures): banded sky, Fuji pink at first light, the sea in rows. */
function dawn(rnd, { fuji = true, shore = true } = {}) {
  let s = `<defs><linearGradient id="s21a-dawn" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="300"><stop offset="0" stop-color="#22306a"/><stop offset="0.45" stop-color="#55578f"/><stop offset="0.78" stop-color="#b98aa2"/><stop offset="1" stop-color="#f3caa2"/></linearGradient>`;
  s += `<linearGradient id="s21a-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a78aa"/><stop offset="1" stop-color="#1e2c5e"/></linearGradient></defs>`;
  s += `<rect width="800" height="600" fill="url(#s21a-dawn)"/>`;
  for (const [y, h, o] of [[96, 22, 0.05], [150, 26, 0.07], [206, 30, 0.09], [252, 26, 0.12]]) s += `<rect y="${y}" width="800" height="${h}" fill="#f6dcae" opacity="${o}"/>`;      // the sky in soft bands, as the prints band it
  if (fuji) {                                                                                                  // Fuji, far off to the north-east, catching the first light
    s += `<path d="M150 300 L300 150 Q314 140 328 150 L470 300 Z" fill="#7c84ae"/>`;
    s += `<path d="M262 188 L300 150 Q314 140 328 150 L366 188 L346 196 L330 186 L314 200 L298 188 L280 198 Z" fill="#f6d2cc"/>`;
  }
  s += `<rect y="300" width="800" height="300" fill="url(#s21a-sea)"/>`;
  for (let i = 0; i < 70; i++) { const y = 304 + rnd() * 290, x = rnd() * 800, w = 8 + rnd() * (10 + (y - 300) / 6); s += `<rect x="${x.toFixed(0)}" y="${y.toFixed(0)}" width="${w.toFixed(0)}" height="1.5" fill="#f6dcae" opacity="${(0.25 + rnd() * 0.35).toFixed(2)}"/>`; }
  if (shore) {                                                                                                 // Yui's shore, low, the roofs along it
    s += `<path d="M0 300 L0 286 C60 280 120 276 190 284 C220 288 250 296 280 300 Z" fill="#3a3f5e"/>`;
    for (let x = 12; x < 240; x += 18 + rnd() * 10) s += `<path d="M${x.toFixed(0)} ${(292 - (x < 160 ? 6 : 2)).toFixed(0)} l7 -6 l7 6 z" fill="#2a2e46"/>`;
    s += `<rect y="298" width="290" height="3" fill="#f2e2c0" opacity="0.6"/>`;
  }
  return s;
}

/** The ship's boat rowing out: two sailors at the oars, the three of them in its stern in O-Tami's kimonos and hats (the
    smallest in pink, her yellow boots showing), Gonroku's ship at anchor ahead, Yui behind. */
export function boatOut() {
  const rnd = seeded(31);
  let s = dawn(rnd);
  // the ship at anchor, off to the right: hull, one mast, the yard down, the sail furled on it
  s += `<path d="M520 318 L760 318 L740 344 L540 344 Z" fill="#2a2018"/><rect x="636" y="196" width="6" height="124" fill="#2a2018"/><rect x="586" y="300" width="106" height="9" rx="4" fill="#d8ccb4"/><rect x="586" y="300" width="106" height="9" rx="4" fill="none" stroke="#2a2018" stroke-width="1"/>`;
  s += `<line x1="752" y1="330" x2="790" y2="372" stroke="#2a2018" stroke-width="1.5"/>`;                 // its anchor rope
  // the ship's boat, near, rowing toward it, its wake behind
  s += `<path d="M118 470 C200 476 300 478 380 470 L364 500 C290 508 196 506 132 498 Z" fill="#4a3624"/><path d="M118 470 C200 476 300 478 380 470" fill="none" stroke="#7a5a3a" stroke-width="3"/>`;
  for (let i = 0; i < 9; i++) s += `<rect x="${(40 + i * 10 + rnd() * 6).toFixed(0)}" y="${(486 + rnd() * 18).toFixed(0)}" width="${(16 + rnd() * 20).toFixed(0)}" height="1.6" fill="#f6dcae" opacity="0.55"/>`;
  const figure = (x, y, k, coat, hat, boots = false) => {
    let p = `<g transform="translate(${x} ${y}) scale(${k})"><path d="M-10 -52 L10 -52 L12 0 L-12 0 Z" fill="${coat}"/><circle cx="0" cy="-60" r="7" fill="#d9b38c"/>`;
    if (hat) p += `<path d="M-16 -60 L0 -73 L16 -60 Z" fill="#c8b070"/>`;
    if (boots) p += `<rect x="-8" y="-4" width="6" height="5" fill="#f2c230"/><rect x="2" y="-4" width="6" height="5" fill="#f2c230"/>`;
    return p + `</g>`;
  };
  // two sailors at the oars, amidships, leaning back; the oars in the water
  for (const [x, lean] of [[214, -8], [262, -6]]) {
    s += `<g transform="translate(${x} 476) rotate(${lean})"><path d="M-9 -40 L9 -40 L11 0 L-11 0 Z" fill="#3a4a6a"/><circle cx="0" cy="-47" r="6" fill="#c89a72"/><rect x="-7" y="-55" width="14" height="4" fill="#e8e2d2"/></g>`;
    s += `<line x1="${x + 10}" y1="452" x2="${x + 60}" y2="508" stroke="#7a5a3a" stroke-width="3"/>`;
  }
  // the three in the stern (at the right end, facing the ship): Mom in green, Big Sister in indigo, Little Sister in pink
  s += figure(312, 474, 0.95, "#2e8a5a", true) + figure(338, 476, 0.9, "#3e4e9a", true) + figure(358, 478, 0.68, "#d86a96", true, true);
  // Little Sister's arm up: waving back to Yui
  s += `<line x1="352" y1="452" x2="338" y2="436" stroke="#d86a96" stroke-width="4" stroke-linecap="round"/>`;
  return s;
}

/** Aboard at anchor, first light: the mast, the yard part way up it (k, 0 down to 1 up), the sail furled on it, or fallen open
    and filling (open); the windlass and its two sailors; Denzō by the mast; the three of them at the stern rail. */
export function aboard(k = 0, open = false) {
  const rnd = seeded(47);
  let s = dawn(rnd, { fuji: true, shore: true });
  // the deck and the bulwark, the ship's own planks
  s += `<path d="M0 430 L800 430 L800 600 L0 600 Z" fill="#6a4a2c"/>`;
  for (let i = 0; i < 7; i++) s += `<line x1="0" y1="${448 + i * 22}" x2="800" y2="${446 + i * 23}" stroke="#4a3220" stroke-width="2"/>`;
  s += `<rect y="400" width="800" height="32" fill="#7a5634"/><rect y="400" width="800" height="4" fill="#c8a070"/>`;
  // the mast, iron-ringed
  s += `<rect x="388" y="0" width="22" height="440" fill="#8a6a44"/>`;
  for (let y = 30; y < 430; y += 34) s += `<rect x="386" y="${y}" width="26" height="4" fill="#2e3a5e"/>`;
  const yy = Math.round(380 - k * 330);
  if (open) {                                                                                                  // the great sail, fallen open and filling: woven cotton in bolts
    s += `<path d="M150 ${yy + 6} L650 ${yy + 6} C668 ${yy + 140} 664 ${yy + 250} 640 ${yy + 330} L160 ${yy + 330} C136 ${yy + 250} 132 ${yy + 140} 150 ${yy + 6} Z" fill="#f2eee2"/>`;
    for (let i = 1; i < 14; i++) { const x = 150 + i * 500 / 14; s += `<path d="M${x.toFixed(0)} ${yy + 8} C${(x + (x - 400) * 0.06).toFixed(0)} ${yy + 160} ${(x + (x - 400) * 0.05).toFixed(0)} ${yy + 250} ${(x + (x - 400) * 0.03).toFixed(0)} ${yy + 328}" fill="none" stroke="#c8c0aa" stroke-width="1.5"/>`; }
    s += `<path d="M150 ${yy + 6} L650 ${yy + 6} C668 ${yy + 140} 664 ${yy + 250} 640 ${yy + 330} L160 ${yy + 330} C136 ${yy + 250} 132 ${yy + 140} 150 ${yy + 6} Z" fill="none" stroke="#2e3a5e" stroke-width="2"/>`;
  }
  s += `<rect x="140" y="${yy}" width="520" height="10" rx="4" fill="#5a3e24"/>`;                             // the yard
  if (!open) s += `<rect x="156" y="${yy + 8}" width="488" height="14" rx="7" fill="#e2dccb"/><rect x="156" y="${yy + 8}" width="488" height="14" rx="7" fill="none" stroke="#2e3a5e" stroke-width="1.5"/>`;      // the sail furled on it
  s += `<line x1="399" y1="${yy}" x2="640" y2="470" stroke="#3a2a1a" stroke-width="2"/>`;                    // the halyard down to the windlass
  // the windlass, at the right, its drum and bars, and two sailors heaving on it
  s += `<rect x="610" y="452" width="110" height="34" rx="6" fill="#5a3e24"/><rect x="618" y="458" width="94" height="22" rx="10" fill="#8a6a44"/>`;
  const heave = Math.round(k * 40) % 2 ? 6 : -6;
  for (const [x, lean] of [[628, heave], [706, -heave]]) {
    s += `<g transform="translate(${x} 486) rotate(${lean})"><path d="M-10 -54 L10 -54 L12 0 L-12 0 Z" fill="#3a4a6a"/><circle cx="0" cy="-62" r="7" fill="#c89a72"/><rect x="-7" y="-71" width="14" height="5" fill="#e8e2d2"/></g>`;
    s += `<line x1="${x}" y1="${458 + lean}" x2="${x + (x < 660 ? 22 : -22)}" y2="470" stroke="#5a3e24" stroke-width="4"/>`;
  }
  // Denzō, huge, by the mast; the purser on a bale at the left with his abacus
  s += `<g transform="translate(446 520)"><path d="M-14 -76 L14 -76 L17 0 L-17 0 Z" fill="#7a5634"/><circle cx="0" cy="-86" r="10" fill="#c89a72"/><rect x="-10" y="-97" width="20" height="6" fill="#e8e2d2"/></g>`;
  s += `<rect x="88" y="488" width="64" height="34" rx="4" fill="#c8b070"/><g transform="translate(120 492)"><path d="M-10 -46 L10 -46 L12 0 L-12 0 Z" fill="#5a4a3a"/><circle cx="0" cy="-54" r="7" fill="#c89a72"/><rect x="-14" y="-24" width="20" height="9" fill="#2a2018"/></g>`;
  // the three at the stern rail, at the left, looking up at the sail
  const figure = (x, y, sc, coat, boots = false) => `<g transform="translate(${x} ${y}) scale(${sc})"><path d="M-12 -62 L12 -62 L14 0 L-14 0 Z" fill="${coat}"/><circle cx="0" cy="-71" r="8" fill="#d9b38c"/><path d="M-18 -70 L0 -84 L18 -70 Z" fill="#c8b070"/>${boots ? `<rect x="-9" y="-5" width="7" height="6" fill="#f2c230"/><rect x="2" y="-5" width="7" height="6" fill="#f2c230"/>` : ""}</g>`;
  s += figure(212, 560, 1.15, "#2e8a5a") + figure(256, 566, 1.08, "#3e4e9a") + figure(290, 572, 0.82, "#d86a96", true);
  return s;
}

/** The sushibox goes from whoever has it (eaten on the first night, the whole box). */
function eatBox(g) {
  const who = g.holder ? g.holder("sushibox") : null;
  if (!who) return;
  const pockets = g.store.data.inventory[who], i = pockets.indexOf("sushibox");
  if (i >= 0) { pockets.splice(i, 1); g.store.emit(); }
}

// O-Masa and the three at the ship's boat (the tender at the water's edge in Yui's picture)
const AT_BOAT = { mom: [244, 436], bigsis: [214, 444], lilsis: [272, 442], masa: [306, 430] };

export default async function castoff(g) {
  g.dialogue.clear();
  // ---- the card ----
  await g.fade(1, 800);
  await g.card(cardWords(g, "edo.card.castoff.title", "Casting Off"), "", { plain: true, ms: 2400 });
  // ---- the beach: O-Masa at the ship's boat (on the village's own stage) ----
  for (const id of ["kihei", "tami", "sankichi"]) { const f = g.actor(id); if (f) f.fade(0); }      // (gone back in; the street empty at first light)
  await g.fade(0, 700);
  await Promise.all([...THREE.map((id) => g.walkTo(AT_BOAT[id][0], AT_BOAT[id][1], id)), walkOf(g, "masa", [AT_BOAT.masa])]);
  for (const id of THREE) look(g, id, AT_BOAT.masa);
  look(g, "masa", "mom");
  await g.say("edo.castoff.masa.1", "edo.castoff.masa.2", "edo.castoff.masa.3");
  await g.wait(400);
  // ---- the ship's boat rows them out ----
  await g.fade(1, 700);
  g.closeup(boatOut(), "The ship's boat rowing the three of them out to Gonroku's ship at anchor, Yui behind, Fuji pink at first light", { grid: [800, 600] });
  g.sfx("creak");
  await g.fade(0, 800);
  await g.wait(600);
  await g.say("edo.castoff.boat.1", "edo.castoff.boat.2", "edo.castoff.boat.3");
  await g.wait(500);
  // ---- aboard: the windlass, the yard going up a heave at a time, the sail ----
  await g.fade(1, 600);
  const deck = (k, open, words) => g.closeup(aboard(k, open), words, { grid: [800, 600] });
  deck(0, false, "Aboard at anchor: two sailors at the windlass, the yard down on the deck with the sail furled on it");
  await g.fade(0, 700);
  await g.wait(400);
  const up = async (k) => { g.sfx("windlass"); deck(k, false, "The yard going up the mast a heave at a time"); await g.wait(500); };
  await g.say("edo.castoff.heave.1"); await up(0.25);
  await g.say("edo.castoff.heave.2"); await up(0.45);
  await g.say("edo.castoff.heave.1"); await up(0.7);
  await g.say("edo.castoff.heave.2"); await up(0.9);
  await g.say("edo.castoff.heave.3");
  await up(1);
  g.sfx("sail");
  deck(1, true, "The great sail fallen open on its yard, filling with the wind");
  await g.wait(800);
  await g.say("edo.castoff.sail.1", "edo.castoff.sail.2", "edo.castoff.sail.3", "edo.castoff.sail.4");
  await g.say("edo.castoff.count.1", "edo.castoff.count.2", "edo.castoff.count.3");
  await g.say("edo.castoff.gonroku");
  await g.wait(500);
  // ---- the first night: the box, eaten at the rail ----
  await g.fade(1, 900);
  g.closeup(nightAtSea(false), "Gonroku's ship at night: the sea, the coast's lights, the great sail; the three of them at the stern rail", { grid: [800, 600] });
  g.sfx("creak");
  await g.fade(0, 900);
  await g.wait(700);
  await g.say("edo.sail.box.1", "edo.sail.box.2");
  eatBox(g);
  await g.wait(600);
  // ---- "Four days later": the map, out along the sea path, and the deck ----
  await g.fade(1, 900);
  g.closeup();
  await g.card(cardWords(g, "edo.card.castoff.later", "Four days later"), "", { plain: true, ms: 2600 });
  g.flag("edo.aboard", true);
  for (const id of THREE) if (g.dressOf(id) !== "edo") g.dress(id, "edo");            // (on deck in the sun: the hats on)
  await g.journey("edo", "yui", "sea", { sound: "creak" });
  // the skippable part ends here: whatever was skipped, the deck is reached the same way
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.goto("edo-deck", { via: "map", spawn: "deck", card: false });
}
