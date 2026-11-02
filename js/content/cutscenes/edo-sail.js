// Cut-scene: "The Uttermost Parts", the voyage (SCENES-20A, in place of MERGE-20's stub; the beat edo.sail; the design,
// briefs/out/edo-design.md, "Cut-Scene: The Uttermost Parts"; the lines are WRITE-20A's, edo.card.sail*, edo.sail.*).
// SCENES-21A (round twenty-one: briefs/out/edo2-design.md, "Cut-Scene: The Uttermost Parts (as built, edited)"; WRITE-21A's
// SAIL_EDIT, talk/edo-c.js): it is played on the deck now (edo-deck.js, edo-sea.js `uttermost`), when #26 and #27 are both
// done; the box of sushi is eaten on the first night, in Casting Off; after the night the card is WRITE-21A's "Eight days
// later" (the deck is the fifth day of twelve); and the quick Osaka passage (round twenty's osakaQuay picture and
// edo.sail.osaka.1, .2) is the river mouth, the lighter, Gonroku's goodbye at the Dōjima steps and the landing.
//
//   the card    "The Uttermost Parts"
//   the rail    the ship at night under its one great sail, the sea dark and enormous, the coast a line of low lights, a moon
//               on the water; Big Sister asleep on a coil of rope, Little Sister asleep on Big Sister, and Mom at the stern
//               rail, saying it to the sea, quietly: Psalm 139:9-10, King James, in two lines (edo.sail.1, .2); Big Sister,
//               not asleep, gives the reference (the only one of them who says one aloud); "Go to sleep, darling."
//               Nobody painted a ship by night: the night is drawn here, as a picture over the stage (g.closeup).
//   the card    "Eight days later" / "Osaka" (edo.card.sail.later, edo.card.osaka); edo.sailed; the map: the portraits along
//               the sea path from the ship's place at sea to Osaka (g.journey("edo", "sea", "osaka"), the timbers creaking)
//   the mouth   masts crowding the two river mouths, the city beyond, and on its skyline a castle with walls and turrets and
//               no top (Gonroku: "Burned before my grandfather."); the lighter alongside: the ship stays at the mouth;
//               Kōta's goodbye and Denzō's
//   the steps   up the river in the lighter to the Dōjima steps; Gonroku's goodbye (round twenty's edo.sail.osaka.3, .3b, .4,
//               then "And don't tell anybody anything true." "That's the only kind I've got."; .5 as the lighter goes)
//   Osaka       g.goto("edo-dojima", { spawn: "landing" }) in the dark (no era card: the same time): the second leg. The
//               Dōjima shore says its own first words there (WRITE-21A's LANDING: the scene's, SCENES-21B).
// Skipped, the same: edo.sailed, the hats on, the Dōjima shore at `landing`.

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

/** SCENES-21A: the river mouth, eight days later: ships at anchor off the mouths of the two rivers, masts crowding them like
    reeds; the low city beyond, white storehouses, roofs; on the skyline a long line of castle walls and corner turrets, and
    no keep; Gonroku's ship anchored near, the lighter alongside her (`lighter`: the three in it, Kōta waving from the rail). */
export function riverMouth(lighter = false) {
  let seed = 53;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  let s = `<defs><linearGradient id="s21a-mouth-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a5a96"/><stop offset="0.7" stop-color="#9fb2cc"/><stop offset="1" stop-color="#e8dcc0"/></linearGradient>`;
  s += `<linearGradient id="s21a-mouth-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a7096"/><stop offset="1" stop-color="#2a3a62"/></linearGradient></defs>`;
  s += `<rect width="800" height="600" fill="url(#s21a-mouth-sky)"/>`;
  for (const [y, h, o] of [[70, 20, 0.06], [130, 24, 0.08], [188, 26, 0.1]]) s += `<rect y="${y}" width="800" height="${h}" fill="#e8dcc0" opacity="${o}"/>`;      // the sky in soft bands
  // the castle on its rise above the city: long stone walls, white plaster, four corner turrets roofed in grey, and no top
  s += `<path d="M330 262 C380 236 430 226 520 224 C610 222 660 232 720 262 Z" fill="#7d8aa0"/>`;
  s += `<path d="M400 238 L640 238 L652 252 L388 252 Z" fill="#9aa3b4"/><rect x="404" y="222" width="232" height="18" fill="#eeeef0"/><rect x="404" y="220" width="232" height="4" fill="#4e5670"/>`;
  for (const x of [398, 478, 560, 626]) s += `<rect x="${x}" y="196" width="22" height="28" fill="#f4f4f6"/><rect x="${x + 7}" y="206" width="8" height="6" fill="#4e5670"/><path d="M${x - 6} 200 L${x + 11} 186 L${x + 28} 200 Z" fill="#4e5670"/><path d="M${x - 5} 212 L${x + 11} 203 L${x + 27} 212 Z" fill="#4e5670"/>`;
  // the city, low and wide; white storehouses among the roofs
  for (let x = -20; x < 820; x += 30 + rnd() * 26) { const w = 26 + rnd() * 24, h = 10 + rnd() * 10, kura = rnd() < 0.25, top = 268 - h - (kura ? 6 : 0);
    s += `<rect x="${x.toFixed(0)}" y="${top.toFixed(0)}" width="${w.toFixed(0)}" height="${(272 - top).toFixed(0)}" fill="${kura ? "#efe9da" : "#9a9488"}"/><path d="M${(x - 3).toFixed(0)} ${top.toFixed(0)} L${(x + w * 0.2).toFixed(0)} ${(top - 7).toFixed(0)} L${(x + w * 0.8).toFixed(0)} ${(top - 7).toFixed(0)} L${(x + w + 3).toFixed(0)} ${top.toFixed(0)} Z" fill="#4a5068"/>`; }
  s += `<rect y="270" width="800" height="330" fill="url(#s21a-mouth-sea)"/>`;
  for (let i = 0; i < 50; i++) s += `<rect x="${(rnd() * 800).toFixed(0)}" y="${(276 + rnd() * 320).toFixed(0)}" width="${(10 + rnd() * 30).toFixed(0)}" height="1.6" fill="#c8d4e6" opacity="0.5"/>`;
  // masts: hundreds of them, standing in the river mouths like reeds
  for (let i = 0; i < 70; i++) { const x = 20 + rnd() * 760, base = 274 + rnd() * 26, h = 40 + rnd() * 70;
    s += `<rect x="${x.toFixed(0)}" y="${(base - h).toFixed(0)}" width="2" height="${h.toFixed(0)}" fill="#3a2e24" opacity="${(0.55 + rnd() * 0.4).toFixed(2)}"/><path d="M${(x - 9).toFixed(0)} ${(base + 2).toFixed(0)} L${(x + 11).toFixed(0)} ${(base + 2).toFixed(0)} L${(x + 7).toFixed(0)} ${(base + 7).toFixed(0)} L${(x - 5).toFixed(0)} ${(base + 7).toFixed(0)} Z" fill="#3a2e24" opacity="0.8"/>`; }
  // Gonroku's ship, anchored near: hull, mast, the sail furled on its yard
  s += `<path d="M90 420 L470 420 L440 470 L120 470 Z" fill="#2c2116"/><rect x="268" y="150" width="9" height="272" fill="#2c2116"/><rect x="170" y="390" width="200" height="12" rx="6" fill="#d8ccb4"/>`;
  s += `<rect x="100" y="408" width="360" height="8" fill="#5a4030"/>`;
  // Kōta at the rail, waving
  s += `<g transform="translate(330 408)"><path d="M-7 -36 L7 -36 L9 0 L-9 0 Z" fill="#3e4e8a"/><circle cx="0" cy="-42" r="6" fill="#d9b38c"/><rect x="-6" y="-49" width="12" height="4" fill="#e8e2d2"/><line x1="6" y1="-34" x2="16" y2="-52" stroke="#3e4e8a" stroke-width="3" stroke-linecap="round"/></g>`;
  if (lighter) {                                                                                              // the lighter alongside: a long flat boat, a man poling, the three among bales
    s += `<path d="M300 500 L700 492 L684 530 L316 536 Z" fill="#4a3624"/><path d="M300 500 L700 492" stroke="#7a5a3a" stroke-width="3"/>`;
    for (const x of [420, 460, 500]) s += `<rect x="${x}" y="486" width="34" height="18" rx="5" fill="#c8b070"/>`;
    s += `<g transform="translate(650 498)"><path d="M-9 -44 L9 -44 L11 0 L-11 0 Z" fill="#4a5a7a"/><circle cx="0" cy="-51" r="6" fill="#c89a72"/></g><line x1="640" y1="448" x2="610" y2="560" stroke="#7a5a3a" stroke-width="3"/>`;
    const fig = (x, y, k, coat, boots = false) => `<g transform="translate(${x} ${y}) scale(${k})"><path d="M-10 -52 L10 -52 L12 0 L-12 0 Z" fill="${coat}"/><circle cx="0" cy="-60" r="7" fill="#d9b38c"/><path d="M-16 -60 L0 -73 L16 -60 Z" fill="#c8b070"/>${boots ? `<rect x="-8" y="-4" width="6" height="5" fill="#f2c230"/><rect x="2" y="-4" width="6" height="5" fill="#f2c230"/>` : ""}</g>`;
    s += fig(344, 500, 0.95, "#2e8a5a") + fig(372, 498, 0.9, "#3e4e9a") + fig(396, 500, 0.7, "#d86a96", true);
    s += `<g transform="translate(560 496)"><path d="M-10 -52 L10 -52 L12 0 L-12 0 Z" fill="#2e3c5a"/><circle cx="0" cy="-60" r="7" fill="#c89a72"/><rect x="-7" y="-68" width="14" height="5" fill="#e8e2d2"/></g>`;      // Gonroku, going up with them
  }
  return s;
}

/** SCENES-21A: the Dōjima steps from the river: the stone steps up from the water, a rice dealer's house front and white
    warehouses above, the lighter at the foot of the steps with Gonroku in it; the three on the steps, going up. */
export function dojimaSteps() {
  let seed = 61;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  let s = `<defs><linearGradient id="s21a-steps-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a5e9e"/><stop offset="1" stop-color="#e2d6b8"/></linearGradient></defs>`;
  s += `<rect width="800" height="600" fill="url(#s21a-steps-sky)"/>`;
  // the shore street above: the house fronts and the white storehouses, roofs
  for (let x = -10; x < 820; x += 120 + rnd() * 40) { const w = 110 + rnd() * 30, kura = rnd() < 0.5;
    s += `<rect x="${x.toFixed(0)}" y="150" width="${w.toFixed(0)}" height="130" fill="${kura ? "#efe9da" : "#7a3e2a"}"/>`;
    s += `<path d="M${(x - 12).toFixed(0)} 156 L${(x + 10).toFixed(0)} 116 L${(x + w - 10).toFixed(0)} 116 L${(x + w + 12).toFixed(0)} 156 Z" fill="#4e5670"/>`;      // a tiled roof, overhanging
    for (let r = 124; r < 154; r += 7) s += `<line x1="${(x - 6).toFixed(0)}" y1="${r}" x2="${(x + w + 6).toFixed(0)}" y2="${r}" stroke="#3a4058" stroke-width="1"/>`;
    if (!kura) { s += `<rect x="${(x + 16).toFixed(0)}" y="196" width="${(w - 32).toFixed(0)}" height="50" fill="#2a2e46"/>`;      // a dealer's open front, its noren
      for (let n = 0; n < 4; n++) s += `<rect x="${(x + 18 + n * (w - 36) / 4).toFixed(0)}" y="196" width="${((w - 40) / 4).toFixed(0)}" height="20" fill="#3a5a8a"/>`; }
    else s += `<rect x="${(x + w / 2 - 12).toFixed(0)}" y="200" width="24" height="44" fill="#2a2e46"/><rect x="${(x + 10).toFixed(0)}" y="252" width="${(w - 20).toFixed(0)}" height="6" fill="#8a8274"/>`; }
  s += `<rect y="280" width="800" height="40" fill="#d8c494"/>`;                                            // the shore street, sand
  // the stone steps down to the water
  for (let i = 0; i < 8; i++) s += `<rect x="${260 - i * 6}" y="${318 + i * 18}" width="${280 + i * 12}" height="18" fill="${i % 2 ? "#b8ab92" : "#c8bca2"}"/><rect x="${260 - i * 6}" y="${318 + i * 18}" width="${280 + i * 12}" height="2" fill="#8a7e68"/>`;
  s += `<rect y="462" width="800" height="138" fill="#4a6a7e"/>`;                                           // the river
  for (let i = 0; i < 40; i++) s += `<rect x="${(rnd() * 800).toFixed(0)}" y="${(468 + rnd() * 128).toFixed(0)}" width="${(10 + rnd() * 30).toFixed(0)}" height="1.6" fill="#b8ccd8" opacity="0.6"/>`;
  // the lighter at the foot of the steps, Gonroku standing in it, the boatman with his pole
  s += `<path d="M180 486 L640 480 L622 520 L196 526 Z" fill="#4a3624"/><path d="M180 486 L640 480" stroke="#7a5a3a" stroke-width="3"/>`;
  s += `<g transform="translate(420 490)"><path d="M-11 -56 L11 -56 L13 0 L-13 0 Z" fill="#2e3c5a"/><circle cx="0" cy="-64" r="8" fill="#c89a72"/><rect x="-8" y="-73" width="16" height="5" fill="#e8e2d2"/></g>`;
  s += `<g transform="translate(590 488)"><path d="M-9 -44 L9 -44 L11 0 L-11 0 Z" fill="#4a5a7a"/><circle cx="0" cy="-51" r="6" fill="#c89a72"/></g><line x1="584" y1="436" x2="560" y2="560" stroke="#7a5a3a" stroke-width="3"/>`;
  // the three on the steps, going up, turned back to him
  const fig = (x, y, k, coat, boots = false) => `<g transform="translate(${x} ${y}) scale(${k})"><path d="M-12 -62 L12 -62 L14 0 L-14 0 Z" fill="${coat}"/><circle cx="0" cy="-71" r="8" fill="#d9b38c"/><path d="M-18 -70 L0 -84 L18 -70 Z" fill="#c8b070"/>${boots ? `<rect x="-9" y="-5" width="7" height="6" fill="#f2c230"/><rect x="2" y="-5" width="7" height="6" fill="#f2c230"/>` : ""}</g>`;
  s += fig(352, 426, 1.0, "#2e8a5a") + fig(392, 408, 0.95, "#3e4e9a") + fig(428, 394, 0.74, "#d86a96", true);
  return s;
}

export default async function sail(g) {
  g.dialogue.clear();
  // the people of the deck, and the three, off the stage under the night (their lines are said from off it)
  for (const id of [...THREE, "gonroku", "kanbei", "denzo", "seijiro", "kota", "kako1", "kako2"]) { const f = g.actor(id); if (f) f.fade(0); }      // SCENES-21A: the deck's people (was the village's)
  await g.fade(1, 900);
  await g.card(cardWords(g, "edo.card.sail.title", "The Uttermost Parts"), "", { plain: true, ms: 2600 });
  // the ship at night: the girls asleep on the rope; Mom at the stern rail, to the sea, quietly (SCENES-21A: the box was eaten
  // on the first night, in Casting Off)
  g.closeup(nightAtSea(true), "Gonroku's ship at night: Big Sister and Little Sister asleep on a coil of rope; Mom at the stern rail", { grid: [800, 600] });
  g.sfx("creak");
  await g.fade(0, 900);
  await g.wait(1600);
  await g.say("edo.sail.1", "edo.sail.2");
  await g.wait(1200);
  await g.say("edo.sail.4");
  await g.wait(500);
  await g.say("edo.sail.5", "edo.sail.6", "edo.sail.7");
  await g.wait(1400);
  // eight days later: Osaka (SCENES-21A: WRITE-21A's card; the night is the fifth day's)
  await g.fade(1, 1000);
  g.closeup();
  await g.card(cardWords(g, "edo.card.sail.later", "Eight days later"), cardWords(g, "edo.card.osaka", "Osaka"), { plain: true, ms: 3000 });
  g.flag("edo.sailed", true);
  for (const id of THREE) if (g.dressOf(id) !== "edo") g.dress(id, "edo");          // (on the road from here: the hats on)
  await g.journey("edo", "sea", "osaka", { sound: "creak" });                       // SCENES-21A: from the ship's place at sea (was yui to the hills by Osaka)
  // SCENES-21A: the river mouth; the castle with no top; the lighter alongside
  g.closeup(riverMouth(false), "Osaka from the sea: masts crowding the river mouths, the city beyond, a castle on the skyline with walls and turrets and no top", { grid: [800, 600] });
  await g.fade(0, 800);
  await g.wait(600);
  await g.say("edo.sail.mouth.1", "edo.sail.mouth.2", "edo.sail.mouth.3", "edo.sail.mouth.4");
  await g.wait(400);
  g.closeup(riverMouth(true), "The lighter alongside Gonroku's ship at the river mouth: the three of them in it among the bales, Gonroku with them, Kōta waving from the rail", { grid: [800, 600] });
  g.sfx("creak");
  await g.wait(500);
  await g.say("edo.sail.lighter.1", "edo.sail.lighter.2", "edo.sail.lighter.3", "edo.sail.lighter.4");
  await g.wait(500);
  // SCENES-21A: up the river to the Dōjima steps; Gonroku's goodbye
  await g.fade(1, 700);
  g.closeup(dojimaSteps(), "The Dōjima steps from the river: the lighter at their foot with Gonroku in it, the three of them going up, the rice dealers' houses above", { grid: [800, 600] });
  await g.fade(0, 700);
  await g.wait(500);
  await g.say("edo.sail.osaka.3", "edo.sail.osaka.3b", "edo.sail.osaka.4", "edo.sail.bye.1", "edo.sail.bye.2", "edo.sail.osaka.5");
  await g.wait(500);
  await g.fade(1, 700);
  g.closeup();
  // the skippable part ends here: whatever was skipped, the Dōjima shore is reached the same way
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.goto("edo-dojima", { via: "cut", spawn: "landing", card: false });      // SCENES-21A: was edo-cedars, enter
}
