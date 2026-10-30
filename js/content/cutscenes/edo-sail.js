// Cut-scene: "The Uttermost Parts", the voyage (SCENES-20A, in place of MERGE-20's stub; the beat edo.sail; the design,
// briefs/out/edo-design.md, "Cut-Scene: The Uttermost Parts"; the lines are WRITE-20A's, edo.card.sail*, edo.sail.*). It is
// played by the village after the goodbyes (#24's gate: edo.west, with the year worked out), from edo-village.js `depart`.
//
//   the card    "The Uttermost Parts"
//   the rail    Gonroku's ship at night under its one great sail, the sea dark and enormous, the coast a line of low lights,
//               a moon on the water. First the box, eaten at the rail (edo.sail.box.1, .2: the sushibox is taken from whoever
//               carries it); then Big Sister asleep on a coil of rope, Little Sister asleep on Big Sister, and Mom at the stern
//               rail, saying it to the sea, quietly: Psalm 139:9-10, King James, in two lines (edo.sail.1, .2); Big Sister,
//               not asleep, gives the reference (the only one of them who says one aloud); "Go to sleep, darling."
//               Nobody painted a ship: the night is drawn here, as a picture over the stage (g.closeup), the three in it as
//               shapes against the moonlit sea, the deck riding the swell.
//   the card    "Twelve days later" / "Osaka"; edo.sailed (the map shows Osaka); the map: the portraits along the coast by the
//               sea path, through Osaka to the hills (g.journey, the ship's timbers creaking)
//   Osaka       briefly, in a picture over the stage as the night is (the river mouth, the quay, the crowds with ladles going
//               east, the constable's man who looks twice, the three going west) and its lines (edo.sail.osaka.*), Gonroku's
//               advice (north, into the hills)
//   the hills   g.goto("edo-cedars", { spawn: "enter" }) in the dark of the map (no era card: the same time): the second leg.
// Skipped, the same: the box gone, edo.sailed, the cedar path.

import { THREE, cardWords } from "../scenes/edo-yui.js";

/** The ship by night, 800 x 600: the sky and its stars, the moon and its road on the water, the coast's low lights, the
    great sail, the stern rail and the deck (rocking slowly on the swell), a lantern; and the three, dark against the
    moonlit sea. `asleep`: the girls asleep on the coil of rope (else sitting on it, the box between them). */
export function nightAtSea(asleep = false) {
  let seed = 11;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  const ink = "#090b16", rim = "#7f8cc0";
  let s = `<defs><linearGradient id="s20a-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b22"/><stop offset="1" stop-color="#1c2a55"/></linearGradient>`;
  s += `<linearGradient id="s20a-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16244c"/><stop offset="1" stop-color="#060a1c"/></linearGradient>`;
  s += `<radialGradient id="s20a-moon"><stop offset="0" stop-color="#fff8e0" stop-opacity="0.55"/><stop offset="1" stop-color="#fff8e0" stop-opacity="0"/></radialGradient>`;
  s += `<radialGradient id="s20a-lamp"><stop offset="0" stop-color="#ffc870" stop-opacity="0.6"/><stop offset="1" stop-color="#ffc870" stop-opacity="0"/></radialGradient></defs>`;
  s += `<rect width="800" height="600" fill="url(#s20a-sky)"/>`;
  for (let i = 0; i < 70; i++) {                                                    // the stars, a few of them twinkling
    const x = rnd() * 800, y = rnd() * 300, r = 0.6 + rnd() * 1.1, tw = rnd() < 0.3;
    s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${r.toFixed(2)}" fill="#e8ecff" opacity="${(0.4 + rnd() * 0.5).toFixed(2)}">${tw ? `<animate attributeName="opacity" values="0.9;0.25;0.9" dur="${(2 + rnd() * 3).toFixed(1)}s" repeatCount="indefinite"/>` : ""}</circle>`;
  }
  s += `<circle cx="640" cy="104" r="70" fill="url(#s20a-moon)"/><circle cx="640" cy="104" r="22" fill="#f6f0d8"/>`;
  s += `<rect y="318" width="800" height="282" fill="url(#s20a-sea)"/>`;
  // the coast, far off: a low dark line of hills, and the low lights of the villages along it
  s += `<path d="M0 322 L60 314 L130 318 L190 309 L260 316 L330 311 L400 319 L470 314 L540 320 L600 322 L600 326 L0 326 Z" fill="#0b1124"/>`;
  for (let i = 0; i < 16; i++) { const x = 12 + rnd() * 570, y = 318 + rnd() * 5; s += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="1.1" fill="#ffcf7a" opacity="${(0.5 + rnd() * 0.4).toFixed(2)}"/>`; }
  // the moon's road on the water, and the swell
  for (let i = 0; i < 26; i++) {
    const y = 330 + i * 5.2 + rnd() * 2, w = 6 + i * 1.6 + rnd() * 10, x = 640 + (rnd() - 0.5) * (14 + i * 4);
    s += `<rect x="${(x - w / 2).toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="1.6" fill="#f2ecd2" opacity="0.6"><animate attributeName="opacity" values="0.7;0.15;0.7" dur="${(1.4 + rnd() * 2).toFixed(1)}s" begin="${(rnd() * 2).toFixed(1)}s" repeatCount="indefinite"/></rect>`;
  }
  for (let i = 0; i < 40; i++) { const y = 334 + rnd() * 250, x = rnd() * 800, w = 10 + rnd() * 30; s += `<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="1.2" fill="#3a4c86" opacity="0.5"/>`; }
  // the ship, rocking: the great sail and its mast, the stern rail, the deck, the coil of rope, the lantern, the three
  s += `<g><animateTransform attributeName="transform" type="rotate" values="-0.8 400 640; 0.8 400 640; -0.8 400 640" dur="8s" repeatCount="indefinite"/>`;
  s += `<rect x="248" y="0" width="12" height="470" fill="#1a1410"/>`;                                            // the mast
  s += `<path d="M120 26 L392 34 L384 360 L132 352 Z" fill="#5c6280"/><path d="M120 26 L392 34 L384 360 L132 352 Z" fill="#c4c8d8" opacity="0.28"/>`;      // the great sail, moonlit cloth
  for (let i = 1; i < 8; i++) { const x0 = 120 + i * 34, x1 = 132 + i * 31.5; s += `<line x1="${x0}" y1="${26 + i}" x2="${x1}" y2="${352 + i}" stroke="#0e1222" stroke-width="2" opacity="0.5"/>`; }
  s += `<line x1="116" y1="24" x2="398" y2="34" stroke="#1a1410" stroke-width="6"/>`;                             // its yard
  s += `<path d="M0 470 L800 470 L800 600 L0 600 Z" fill="#1d140e"/>`;                                            // the deck
  for (let i = 0; i < 6; i++) s += `<line x1="0" y1="${488 + i * 20}" x2="800" y2="${484 + i * 21}" stroke="#2c2016" stroke-width="2"/>`;
  s += `<rect x="0" y="424" width="800" height="9" fill="#2a1d12"/><rect x="0" y="424" width="800" height="2" fill="${rim}" opacity="0.35"/>`;      // the stern rail
  for (let x = 20; x < 800; x += 70) s += `<rect x="${x}" y="430" width="8" height="42" fill="#22170f"/>`;
  s += `<circle cx="712" cy="392" r="60" fill="url(#s20a-lamp)"><animate attributeName="opacity" values="1;0.75;0.95;0.8;1" dur="2.6s" repeatCount="indefinite"/></circle>`;      // the lantern at the stern
  s += `<rect x="704" y="380" width="16" height="22" rx="4" fill="#ffd590" opacity="0.9"/><line x1="712" y1="366" x2="712" y2="380" stroke="#22170f" stroke-width="2"/>`;
  // the coil of rope on the deck, at the left
  s += `<ellipse cx="250" cy="548" rx="86" ry="24" fill="#2e2418"/>`;
  for (let i = 0; i < 4; i++) s += `<ellipse cx="250" cy="${546 - i * 4}" rx="${80 - i * 12}" ry="${21 - i * 3}" fill="none" stroke="#4a3a26" stroke-width="3"/>`;
  // Mom at the stern rail, her back to us, looking out at the sea (her sedge hat on, her sleeves hanging)
  s += `<g fill="${ink}" stroke="${rim}" stroke-width="1.2" stroke-opacity="0.45">`;
  s += `<path d="M577 404 L623 404 L631 556 L569 556 Z"/><path d="M566 410 L580 408 L582 470 L564 472 Z"/><path d="M620 408 L634 410 L636 472 L618 470 Z"/>`;
  s += `<circle cx="600" cy="390" r="14"/><path d="M558 384 L600 360 L642 384 Q600 392 558 384 Z"/></g>`;
  if (!asleep) {
    // the girls on the coil, sitting, the box between them: Big Sister (taller), Little Sister (her hat on her back)
    s += `<g fill="${ink}" stroke="${rim}" stroke-width="1.2" stroke-opacity="0.45">`;
    s += `<path d="M196 446 L232 446 L240 536 L190 536 Z"/><circle cx="214" cy="433" r="12"/><path d="M180 428 L214 410 L248 428 Q214 435 180 428 Z"/>`;
    s += `<path d="M286 482 L312 482 L318 538 L282 538 Z"/><circle cx="299" cy="471" r="10"/><path d="M290 466 L314 474 L310 486 L286 480 Z"/>`;
    s += `<rect x="248" y="500" width="30" height="16" rx="3"/></g>`;
  } else {
    // asleep: Big Sister on her back along the coil, her head on the rope; Little Sister curled on her, asleep too
    s += `<g fill="${ink}" stroke="${rim}" stroke-width="1.2" stroke-opacity="0.45">`;
    s += `<path d="M176 528 Q230 512 330 526 L334 544 Q240 548 178 546 Z"/><circle cx="172" cy="520" r="12"/>`;
    s += `<path d="M228 512 Q262 496 300 506 L302 520 Q262 524 230 524 Z"/><circle cx="222" cy="504" r="10"/></g>`;
  }
  s += `</g>`;
  return s;
}

/** Osaka, twelve days later, briefly (not a scene: a picture over the stage, as the night is): the river mouth in the late
    afternoon, warehouses and roofs beyond, boats; on the quay a crowd going east, ladles held up (pilgrims for Ise), and
    three taller travellers in hats going the other way, west, the smallest in pink; at the left a constable's man in a
    belt, turned to look at them; Gonroku's ship tied up at the right. */
export function osakaQuay() {
  let seed = 23;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  let s = `<defs><linearGradient id="s20a-osaka-sky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="270"><stop offset="0" stop-color="#5a6a8e"/><stop offset="0.62" stop-color="#a3a2b0"/><stop offset="1" stop-color="#e8cf9c"/></linearGradient></defs>`;
  s += `<rect width="800" height="600" fill="url(#s20a-osaka-sky)"/>`;
  // the hills far beyond the town in the morning haze, and gulls over the river mouth
  s += `<path d="M0 238 C90 214 150 206 230 220 C300 232 350 204 430 198 C520 192 590 222 660 214 C720 208 770 196 800 200 L800 270 L0 270 Z" fill="#7d84a0" opacity="0.5"/>`;
  for (const [x, y, k] of [[180, 122, 1], [214, 140, 0.8], [520, 98, 0.9], [548, 112, 0.7], [610, 150, 0.6]]) {
    s += `<path d="M${x - 9 * k} ${y} Q${x - 4 * k} ${y - 5 * k} ${x} ${y} Q${x + 4 * k} ${y - 5 * k} ${x + 9 * k} ${y}" fill="none" stroke="#3a3f52" stroke-width="1.6" stroke-linecap="round"/>`;
  }
  // the town beyond the river: two rows of houses on the far bank (the far row hazier), white storehouses among them
  for (const [base, k, wall, roof, haze] of [[262, 0.7, "#8a8a96", "#4a5068", 0.55], [282, 1, "#a09884", "#3a3f52", 1]]) {
    for (let x = -30; x < 830; x += (44 + rnd() * 26) * k) {
      const w = (36 + rnd() * 24) * k, h = (16 + rnd() * 10) * k, kura = rnd() < 0.2, top = base - h - (kura ? 8 * k : 0);
      s += `<g opacity="${haze}"><rect x="${x.toFixed(0)}" y="${top.toFixed(0)}" width="${w.toFixed(0)}" height="${(base - top).toFixed(0)}" fill="${kura ? "#ebe5d6" : wall}"/>`;
      s += `<path d="M${(x - 4 * k).toFixed(0)} ${top.toFixed(0)} L${(x + w * 0.2).toFixed(0)} ${(top - 9 * k).toFixed(0)} L${(x + w * 0.8).toFixed(0)} ${(top - 9 * k).toFixed(0)} L${(x + w + 4 * k).toFixed(0)} ${top.toFixed(0)} Z" fill="${roof}"/></g>`;
    }
  }
  s += `<rect y="282" width="800" height="6" fill="#6e6a62"/>`;                        // the far bank's stones
  // the river, and boats on it
  s += `<rect y="286" width="800" height="120" fill="#3a5078"/>`;
  for (let i = 0; i < 30; i++) s += `<rect x="${(rnd() * 800).toFixed(0)}" y="${(292 + rnd() * 108).toFixed(0)}" width="${(10 + rnd() * 30).toFixed(0)}" height="1.6" fill="#9cb0d0" opacity="0.6"/>`;
  for (const [x, y, w] of [[90, 318, 60], [260, 352, 74], [430, 330, 52]]) s += `<path d="M${x} ${y} L${x + w} ${y} L${x + w - 8} ${y + 9} L${x + 8} ${y + 9} Z" fill="#2a2018"/><rect x="${x + w / 2 - 1}" y="${y - 30}" width="2" height="30" fill="#2a2018"/>`;
  // Gonroku's ship, tied up at the right
  s += `<path d="M560 372 L780 372 L760 402 L580 402 Z" fill="#2c2116"/><rect x="664" y="250" width="6" height="122" fill="#2c2116"/><path d="M600 262 L740 266 L736 352 L604 348 Z" fill="#cfcabb" opacity="0.85"/>`;
  // the quay
  s += `<rect y="406" width="800" height="194" fill="#8a8170"/><rect y="406" width="800" height="8" fill="#6e6656"/>`;
  for (let i = 0; i < 12; i++) s += `<rect x="${i * 70 + (i % 2) * 20}" y="${430 + (i % 3) * 50}" width="60" height="2" fill="#7a725f"/>`;
  // the crowd going east with their ladles up
  const person = (x, y, k, coat, hat, ladle, faceL = false) => {
    let p = `<g transform="translate(${x.toFixed(0)} ${y.toFixed(0)}) scale(${k.toFixed(2)})">`;
    p += `<path d="M-9 -58 L9 -58 L12 0 L-12 0 Z" fill="${coat}"/><circle cx="0" cy="-66" r="7" fill="#d9b38c"/>`;
    p += hat ? `<path d="M-15 -66 L0 -78 L15 -66 Z" fill="#c8b070"/>` : `<rect x="-6" y="-76" width="12" height="6" fill="#2a2420"/>`;
    if (ladle) p += `<rect x="${faceL ? -16 : 12}" y="-92" width="2" height="40" fill="#7a5a32"/><ellipse cx="${faceL ? -15 : 13}" cy="-93" rx="5" ry="3" fill="#a07a42"/>`;
    return p + `</g>`;
  };
  const coats = ["#5a6f8f", "#7d6a52", "#4f6a5a", "#8a5a4a", "#6a6a7a", "#9a8a6a"];
  for (let i = 0; i < 26; i++) { const y = 440 + rnd() * 120; s += person(30 + rnd() * 740, y, 0.7 + (y - 440) / 300, coats[i % coats.length], rnd() < 0.7, rnd() < 0.8); }
  // the three of them, going west, taller than everybody, in their hats; the smallest in pink
  s += person(486, 548, 1.30, "#2e8a5a", true, false) + person(452, 556, 1.22, "#3e4e9a", true, false) + person(424, 566, 0.92, "#d86a96", true, false);
  // a constable's man in a belt, at the left, turned to look at them twice
  s += `<g transform="translate(92 560) scale(1.25)"><path d="M-10 -58 L10 -58 L12 0 L-12 0 Z" fill="#3a3a44"/><rect x="-11" y="-30" width="22" height="4" fill="#b08a3a"/><rect x="8" y="-34" width="3" height="26" fill="#5a4a3a"/><circle cx="2" cy="-66" r="7" fill="#d9b38c"/><rect x="-5" y="-76" width="12" height="6" fill="#2a2420"/></g>`;
  // Gonroku, by his ship
  s += `<g transform="translate(624 520) scale(1.15)"><path d="M-10 -58 L10 -58 L12 0 L-12 0 Z" fill="#2e3c5a"/><circle cx="0" cy="-66" r="7" fill="#c89a72"/><rect x="-7" y="-74" width="14" height="5" fill="#e8e2d2"/></g>`;
  return s;
}

/** The sushibox goes from whoever has it (eaten at the rail, the whole box). */
function eatBox(g) {
  const who = g.holder ? g.holder("sushibox") : null;
  if (!who) return;
  const pockets = g.store.data.inventory[who], i = pockets.indexOf("sushibox");
  if (i >= 0) { pockets.splice(i, 1); g.store.emit(); }
}

export default async function sail(g) {
  g.dialogue.clear();
  // the people of the village, and the three, off the stage under the night (their lines are said from off it)
  for (const id of [...THREE, "gonroku", "kihei", "tami", "sankichi", "masa"]) { const f = g.actor(id); if (f) f.fade(0); }
  await g.fade(1, 900);
  await g.card(cardWords(g, "edo.card.sail.title", "The Uttermost Parts"), "", { plain: true, ms: 2600 });
  // the ship at night: the box, eaten at the rail
  g.closeup(nightAtSea(false), "Gonroku's ship at night: the sea, the coast's lights, the great sail; the three of them at the stern rail", { grid: [800, 600] });
  g.sfx("creak");
  await g.fade(0, 900);
  await g.wait(800);
  await g.say("edo.sail.box.1", "edo.sail.box.2");
  eatBox(g);
  await g.wait(600);
  // later: the girls asleep on the rope; Mom at the stern rail, to the sea, quietly
  await g.fade(1, 700);
  g.closeup(nightAtSea(true), "Gonroku's ship at night: Big Sister and Little Sister asleep on a coil of rope; Mom at the stern rail", { grid: [800, 600] });
  await g.fade(0, 900);
  g.sfx("creak");
  await g.wait(1600);
  await g.say("edo.sail.1", "edo.sail.2");
  await g.wait(1200);
  await g.say("edo.sail.4");
  await g.wait(500);
  await g.say("edo.sail.5", "edo.sail.6", "edo.sail.7");
  await g.wait(1400);
  // twelve days later: Osaka
  await g.fade(1, 1000);
  g.closeup();
  await g.card(cardWords(g, "edo.card.sail", "Twelve days later"), cardWords(g, "edo.card.osaka", "Osaka"), { plain: true, ms: 3000 });
  g.flag("edo.sailed", true);
  for (const id of THREE) if (g.dressOf(id) !== "edo") g.dress(id, "edo");          // (on the road from here: the hats on)
  await g.journey("edo", "yui", "hills", { via: ["osaka"], sound: "creak" });
  // Osaka, briefly: the river mouth, the crowds with ladles going east, a constable's man who looks twice
  g.closeup(osakaQuay(), "Osaka: the river mouth, a crowd with ladles going east, and the three of them going west", { grid: [800, 600] });
  await g.fade(0, 700);
  await g.wait(500);
  await g.say("edo.sail.osaka.1", "edo.sail.osaka.2", "edo.sail.osaka.3", "edo.sail.osaka.3b", "edo.sail.osaka.4", "edo.sail.osaka.5");
  await g.wait(500);
  await g.fade(1, 700);
  g.closeup();
  // the skippable part ends here: whatever was skipped, the hills are reached the same way
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.goto("edo-cedars", { via: "cut", spawn: "enter", card: false });
}
