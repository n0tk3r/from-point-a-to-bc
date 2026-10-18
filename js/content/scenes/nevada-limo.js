// Act Five, its one scene (NEVADA-12SC: new in round twelve): the back of a gray limousine, driving, the desert going by.
// Grandpa Joe and Ranger play, and the player switches between them with the portraits (keys 1 and 2).
//
// The first part of the game played by somebody who is not family, and the first part played by a raccoon. What each can
// do is the puzzle (briefs/out/nevada-expansion-design.md, "Act Five opens"):
//   GRANDPA JOE can talk to anybody, and has his hands tied: belted to the long seat, he never walks here (`still`, below:
//     a click on the floor does nothing for him, and he does everything from where he sits). Later, his hands free.
//   RANGER cannot talk ("...", and Grandpa Joe says what he means) and has paws: he walks the carpet, nibbles, reaches,
//     carries small things, and reads with his paws.
//
//   the opening ("Meanwhile, in a limousine")   the seatbelt over the ropes; the divider down and up; Ranger comes up
//                                               from under the facing seat in his mirror shades
//   #14 Ranger's Ropes      the divider comes down every so often (a suit looks back), and a raccoon chewing a prisoner
//                           loose is the kind of thing the clipboard has a line for: Ranger at the ropes is caught
//                           ("Sir, is the raccoon... chewing?" "He's groomin' me, son. It's affection."), and the
//                           divider stays down longer. Talk does not put it up ("Sir, we are required to maintain
//                           visual."); singing does: Grandpa Joe hums the Last Stop Rag, his own tune, and the divider
//                           goes up and stays up while he hums. Then, as Ranger, one strand a nibble; between strands the
//                           singing stops, the divider comes down once more (Ranger sits on his work: "Groomin'."), and
//                           Grandpa Joe must sing again. Four strands, and the bow last: hands. The seatbelt stays on.
//                           Divider down: a raccoon doing nothing. Divider up: furious.
//   #15 Jed's Lunch         on the facing seat, across the car: the paper bag (the pickle is Ranger's), the clipboard,
//                           a juice box. With his hands free Grandpa Joe reads the clipboard and eats the cheeseburger
//                           (Ranger fetches them across the car for him: Grandpa Joe is belted in), the map goes into
//                           his bib pocket, a receipt for the banjo comes back through the divider, and the limousine
//                           slows at the gate of the Office Of Peculiar Sectors: the card, and the end of the demo.
//
// Every line is in js/content/lines/limo.en.js; the suits through the divider are dividerTree (js/content/talk/nevada.js).
// Every place is the painter's own measurement of the finished picture (art/scenes/nevada-limo/layout.json; PAINT-12C's
// ready.md), or was set by eye against the picture with the two of them in it; where the two differ the comment says why.
//
// Try it: index.html?scene=nevada-limo&lead=grandpajoe   (&flags=limo.arrived to skip the opening; limo.loose for #15)

import { dividerTree } from "../talk/nevada.js";
import { scaleAt } from "../../engine/walk.js";

const art = "art/scenes/nevada-limo/";
const DRIVE_CAM = { vanish: [424, 220], focal: 345, eye: 1.83 };          // DRIVE-16M: the scene's camera (layout.json `vanishing`, `view.focal`); the eye 1.83 m above the road
// DRIVE-16F: the things' shadows, laid on the ground by the engine (the sheet has none): the painter's sun, low on the car's
// right and a little behind (a metre of height throws its shadow 0.36 m ahead and 1.95 m to the car's left: out across the
// desert on the left, in toward the road on the right; tools/paint/nevada_limo_drive_kit.py), multiplying the ground by
// the painter's colour for a morning shadow on the sand, as strong as the roadside's standing things' (nevada_roadside.py:
// SHADE at 0.62)
const DRIVE_SUN = { sun: [0.36, 1.95], shade: "#6664ac", shade_k: 0.62 };
const DOTS = "limo.ranger.dots";
const who = (g) => g.store.data.active;
const loose = (g) => !!g.flag("limo.loose");
const strands = (g) => Number(g.flag("limo.strands")) || 0;

// ---------- where the two of them are ----------
const JOE = [318, 327];                // the mark `joe`: the ground under his hips, under the long seat's cushion; facing E, across the car
const JOE_SCALE = 0.791;               // the size the painter drew him at there (the row's own is 0.793)
const RANGER = [422, 354];             // the mark `ranger`: on the carpet, near us, facing Joe (W)
// Ranger's places on the carpet in front of each thing (the painter's `stands`), and the cushion beside the bow.
const AT = { ropes: [344, 340], joe: [354, 330], belt: [332, 359], phone: [376, 329], ashtray: [460, 330], divider: [419, 329],
  bag: [504, 364], juice: [514, 378], clipboard: [507, 380], fridge: [498, 381], windowL: [335, 352], windowR: [502, 353] };
// Up on the long seat's cushion, beside the bow, to nibble: drawn at the painter's scale with his feet there, and sorted as
// if he stood on the carpet under him (`floor`), so that he is in front of the ropes and of Grandpa Joe.
const PERCH = { at: [309, 307], scale: 0.901, floor: 342 };

// ---------- the divider ----------
// A smoked window between the back and the front (PAINT-12C: divider-up.png, divider-down.png, the same pixels). Up, the
// glass; down, the backs of two heads with earpieces, two pairs of dark shades in the mirror, the road. It SLIDES: the
// down picture lies on the light layer, and over it the glass, cut to the opening (`#div-slot`), slides down into the seat
// back. (The light layer is under everybody; nothing is ever in front of the divider but people, who are.) Not saved: the
// scene puts it where the facts say (`setup`), and the scene's own clock moves it (see `tick`).
const SLIDE = 60;                      // how far the glass goes down: the opening is 57 pixels high
const UP_MS = 9000, DOWN_MS = 4500;    // the look-backs, before anybody sings: up this long, down that long
const CAUGHT_MS = 9000;                // and after a raccoon is caught chewing: the divider stays down longer
let div = null;                        // this scene's divider as it is now: { k (0 up, 1 down), left (ms till it moves), moving, build }
let builds = 0;

/** The divider to up (false) or down (true), sliding, over ms. */
async function slide(g, down, ms = 650) {
  if (!div) return;
  const from = div.k, to = down ? 1 : 0;
  div.moving = true;
  if (from !== to) g.sfx("panel");
  await g.tween(Math.abs(to - from) * ms, (t) => setDivider(g, from + (to - from) * t), g.ease.inOut);
  setDivider(g, to);
  div.moving = false;
}
function setDivider(g, k) {
  if (div) div.k = k;
  const glass = g.q("#div-glass");
  if (glass) glass.setAttribute("transform", `translate(0 ${Math.round(SLIDE * k)})`);
}
const isDown = () => !!div && div.k > 0.5;
/** Where the divider rests by the facts: up while he sings, and once he is loose; down between strands until he sings again. */
const restsDown = (g) => !loose(g) && !g.flag("limo.singing") && strands(g) > 0;

/** The scene's own clock (made in `setup`, and let go when another scene is built): the look-backs, before anybody sings;
    and the notes of the Last Stop Rag over Grandpa Joe's head while he hums it. Nothing moves while a script has
    control, a menu is up, or anybody is talking: a script does its own sliding. */
function tick(g, me, dt) {
  const n = g.q("#notes");
  if (n) {
    const on = !!g.flag("limo.singing") && g.mode === "play", calm = g.calm;
    n.setAttribute("opacity", on ? 1 : 0);
    if (on && !calm) {
      me.t = (me.t + dt) % 2400;
      [...n.children].forEach((note, i) => {
        const t = ((me.t / 2400) + i / 3) % 1;
        note.setAttribute("transform", `translate(${334 + 10 * i + 6 * Math.sin(t * 6.3 + i)} ${226 - 46 * t})`);
        note.setAttribute("opacity", Math.min(1, 4 * t) * (1 - t));
      });
    }
  }
  if (!div || g.mode !== "play" || g.busy || div.moving || g.dialogue.active || g.dialogue.choosing) return;
  if (!g.flag("limo.arrived") || loose(g) || g.flag("limo.singing") || strands(g) > 0) return;      // (only the look-backs, before any strand)
  div.left -= dt;
  if (div.left > 0) return;
  div.left = isDown() ? UP_MS : DOWN_MS;
  slide(g, !isDown());
}

// ---------- Grandpa Joe ----------
/** Grandpa Joe as he is by the facts: tied, or loose; seated on the long seat at his mark either way (the engine puts a
    lead where he can stand, and as his cast entry draws him: the rocking chair's Grandpa Joe). */
function seatJoe(g) {
  const cast = g.view.cast, old = cast.get("grandpajoe"), kind = loose(g) ? "grandpajoe-seat-loose" : "grandpajoe-seat-tied";
  if (old && old.kind === kind && old.x === JOE[0] && old.y === JOE[1]) return old;
  const was = old ? { hidden: old.hidden, opacity: old.opacity } : null;
  if (old) cast.remove("grandpajoe");
  const f = cast.addFigure("grandpajoe", kind, JOE[0], JOE[1], JOE_SCALE).face("E");
  if (was) { f.hidden = was.hidden; f.opacity = was.opacity; }
  return f;
}

/** As Grandpa Joe, at the divider: he raps on the glass if it is up (a suit looks back: "Sir?"), and talks. The suits
    answer in regulations and do not put it up for talk; the Last Stop Rag puts it up (the tree's hook `sing`). */
async function atDivider(g) {
  if (!isDown()) { g.sfx("thunk"); await g.wait(150); await slide(g, true); }
  await g.talk(DIVIDER);
  if (!g.flag("limo.singing") && !restsDown(g) && div) div.left = DOWN_MS;           // (it goes up again in its own time)
}
/** The tree's hook: he has started humming. The divider goes up, and stays up while he hums; the Rag plays under him. */
async function sing(g) {
  g.flag("limo.singing", true);
  g.music(g.musicOf(g.scene));
  await slide(g, false);
}
const DIVIDER = dividerTree({ sing });
/** The singing stops (a strand is done, or the ropes are off). */
function hush(g) {
  if (!g.flag("limo.singing")) return;
  g.flag("limo.singing", false);
  g.music(g.musicOf(g.scene));
}

// ---------- #14: Ranger's Ropes ----------
/** Ranger up onto the cushion beside the bow (a hop from his place on the carpet), or down again. */
async function perch(g, up) {
  const r = g.actor("ranger");
  if (!r) return;
  const from = [r.x, r.y, r.scale], to = up ? [...PERCH.at, PERCH.scale] : [...AT.ropes, scaleAt(g.scene, AT.ropes[1])];
  r.sit(false, true);
  if (up) r.base = PERCH.floor;
  await g.tween(340, (t) => r.place(from[0] + (to[0] - from[0]) * t, from[1] + (to[1] - from[1]) * t - 16 * Math.sin(Math.PI * t), from[2] + (to[2] - from[2]) * t), g.ease.inOut);
  r.place(to[0], to[1], to[2]);
  if (!up) r.base = null;
  r.face("W");
  r.sit(true, true);
  g.rememberPlace("ranger");
}
/** A good chew at the ropes, sitting up on the cushion: the nibble frames, for so long. */
const nibble = (g, ms) => { const r = g.actor("ranger"); return r ? r.play(g.clock, "nibble", { ms }) : Promise.resolve(); };
/** Caught: a raccoon chewing a prisoner loose, with a man in dark shades looking back at him. He stops, and sits, and is
    a raccoon doing nothing; Grandpa Joe explains; and the divider stays down longer. Nothing is lost. */
async function caught(g) {
  const r = g.actor("ranger");
  if (r) r.stop();
  await g.say("limo.ropes.chewing", "limo.ropes.grooming");
  await g.wait(300);
  if (div) div.left = CAUGHT_MS;
  await perch(g, false);
}
/** As Ranger, the ropes. */
async function ropes(g) {
  if (loose(g)) return g.say(DOTS, "limo.ropes.ranger2.joe");                       // (he is keeping the bow: it is his now)
  await perch(g, true);
  if (isDown()) {                                                                   // a suit is looking back: caught at once
    await nibble(g, 900);
    return caught(g);
  }
  if (!g.flag("limo.singing")) {                                                    // up, but nobody is keeping them busy: a suit looks back mid-chew
    const chewing = nibble(g, 3000);
    await g.wait(800);
    await slide(g, true, 450);
    await Promise.race([chewing, g.wait(250)]);
    return caught(g);
  }
  // The divider is up and staying up: furious. One strand.
  await g.say("limo.ropes.nibble");
  await nibble(g, 2200);
  const n = strands(g) + 1;
  g.flag("limo.strands", n);
  await g.say(`limo.ropes.strand.${n}`);
  if (n < 4) {
    // Between strands the singing stops, and the divider comes down once more: Ranger sits on his work.
    hush(g);
    const r = g.actor("ranger");
    if (r) r.sit(true, true);
    await slide(g, true);
    await g.say("limo.ropes.groomin");
    await g.wait(400);
    return perch(g, false);                                                          // (and gets down, innocently: it stays down till he sings again)
  }
  // Four strands; and the bow, last: a trade like any other. He reads it with his paws, and it comes undone.
  const r = g.actor("ranger");
  if (r) await r.play(g.clock, "wash", { ms: 1600 });
  hush(g);
  g.flag("limo.loose", true);
  seatJoe(g);
  await g.say("limo.ropes.bow");
  await g.wait(500);
  await g.say("limo.ropes.regs");                                                   // (the seatbelt stays on)
  await perch(g, false);
}

// ---------- #15: Jed's Lunch ----------
/** Ranger fetches a thing from the facing seat across the car to Grandpa Joe (who is belted in): over to it, his paws on
    it (the cut-out goes), and back to the long seat, where he holds it up to him. Grandpa Joe is the one being played. */
async function fetch(g, thing, { pickle = false } = {}) {
  const r = g.actor("ranger");
  if (!r) return;
  r.sit(false, true);
  r.hurry = true;
  await g.walkTo(AT[thing][0], AT[thing][1], "ranger");
  r.face("E");
  if (pickle && !g.flag("limo.pickle")) {                                           // into the bag before anyone can speak: the pickle is his
    await r.play(g.clock, "nibble", { ms: 1400 });
    g.flag("limo.pickle", true);
    await g.say("limo.lunch.pickle");
  }
  await r.play(g.clock, "reach");
  g.flag(`limo.${thing}Taken`, true);                                               // (its cut-out goes)
  r.hurry = true;
  await g.walkTo(AT.joe[0], AT.joe[1], "ranger");
  r.face("W");
  await r.play(g.clock, "reach");                                                   // held up to him
}

/** As Ranger, at the bag: he is into it before anyone can speak. The pickle is gone. */
async function bagRanger(g) {
  if (g.flag("limo.pickle")) return g.say(g.fallback("nope"));
  const r = g.actor("ranger");
  if (r) { r.face("E"); await r.play(g.clock, "nibble", { ms: 1400 }); }
  g.flag("limo.pickle", true);
  await g.say("limo.lunch.pickle");
}

/** The clipboard, close: the office's sheet as Grandpa Joe reads it (lines read.1 to read.3): the notice's own words, a
    map of the desert with three sectors ringed in pen, two numbered and the third under a thumbprint in mustard, and a
    column headed WHAT OPENS THEM, blank all the way down, and Jed's note in the margin. Drawn on the 800x600 picture, in
    its upper part (the words spoken while it is up run along the bottom). Nothing on it names the third sector. */
function clipboard() {
  const t = (x, y, size, text, fill = "#2b2622", o = "") => `<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" text-anchor="middle"${o}>${text}</text>`;
  const ring = (x, y, label) => `<ellipse cx="${x}" cy="${y}" rx="26" ry="19" fill="none" stroke="#24408a" stroke-width="2.4"/>${label ? t(x, y + 6, 17, label, "#24408a") : ""}`;
  const box = (y) => `<rect x="492" y="${y}" width="64" height="30" fill="none" stroke="#2b2622" stroke-width="1.6"/>`;
  return `<g shape-rendering="geometricPrecision" transform="translate(0 18)">
    <rect x="196" y="26" width="408" height="440" rx="10" fill="#9a6a3c"/><rect x="200" y="30" width="400" height="432" rx="8" fill="#b07c48"/>
    <rect x="222" y="54" width="356" height="396" fill="#f6f4ee"/>
    <rect x="352" y="22" width="96" height="40" rx="6" fill="#c9ced6"/><rect x="368" y="14" width="64" height="18" rx="5" fill="#9097a3"/>
    ${t(400, 92, 22, "AREA CLOSED")}${t(400, 116, 15, "ELEVATED RADIATION", "#c8402f")}
    <rect x="240" y="128" width="320" height="1.4" fill="#2b2622"/>
    <path d="M240,330 C280,300 310,250 360,236 M246,214 L280,190 L320,205 L356,182 M376,328 L416,310 L458,326" fill="none" stroke="#7a6a58" stroke-width="2" stroke-linecap="round"/>
    ${ring(282, 266, "44")}${ring(410, 206, "1921")}${ring(392, 352, "")}
    <path d="M376,338 c10,-14 34,-10 38,6 c4,16 -18,26 -32,18 c-12,-6 -14,-14 -6,-24 z" fill="#e8c23a" opacity="0.92"/>
    <path d="M382,344 c6,-6 18,-4 20,4 M380,352 c8,-6 22,-4 26,4" fill="none" stroke="#c99a1a" stroke-width="1.4"/>
    <rect x="478" y="140" width="1" height="176" fill="#cfc9bd"/>
    ${t(524, 152, 10, "WHAT OPENS THEM")}${box(162)}${box(200)}${box(238)}${box(276)}
    ${t(326, 412, 17, "A COIN?? Ask Houston.", "#5a5a66", ' font-style="italic" transform="rotate(-4 326 412)"')}
  </g>`;
}

/** #15: Grandpa Joe, his hands free, wants his lunch and his reading: Ranger fetches the bag (the pickle, if it is still
    there, is his fee) and the clipboard across the car to him. He eats the cheeseburger and reads; he tears the map off
    and folds it small, and Ranger puts it in his bib pocket; the receipt for the banjo comes back through the divider;
    the limousine slows at the gate; the card; the end of the demo. */
async function lunch(g) {
  if (!g.flag("limo.bagTaken")) await fetch(g, "bag", { pickle: true });
  await fetch(g, "clipboard");
  await g.say("limo.lunch.burger");
  g.closeup(clipboard(), "The office's clipboard", { grid: [800, 600] });
  await g.say("limo.lunch.read.1", "limo.lunch.read.2", "limo.lunch.read.3");
  g.closeup();
  await g.say("limo.lunch.read.4", "limo.lunch.read.5");
  // The map, torn off the clipboard and folded small; Ranger puts it in the bib pocket for him.
  const r = g.actor("ranger");
  if (r) await r.play(g.clock, "reach");
  g.give("sectormap");
  await g.say("limo.lunch.trade");
  // And the divider slides down, and a hand passes back a receipt.
  await slide(g, true);
  await g.say("limo.lunch.receipt.1");
  g.sfx("paint");
  await g.arrive("receipt", [421, 252], { to: [346, 322] });
  g.give("receipt");
  await slide(g, false);
  await g.say("limo.lunch.receipt.2", "limo.lunch.receipt.3", DOTS, "limo.lunch.receipt.4");
  g.flag("limo.map", true);
  await ending(g);
}
/** As Grandpa Joe, the juice box (his hands free): Ranger fetches it, and he drinks it. */
async function juice(g) {
  await fetch(g, "juice");
  await g.say("limo.lunch.juice");
}

/** The gate: the limousine slows (the desert going by slows with it: both drives, tweened to nothing: DRIVE-16M), a gate, a very small
    building with a very long name on it; the card; "limo.done"; and (SCENES-17) the arrival at the Office, which goes on
    from here (js/content/cutscenes/office-arrive.js): the demo now ends at the end of the Office's stage one. On the
    way, the two of them have the last word, about the map. */
async function ending(g) {
  await g.say("limo.talk.joe.ranger.4a", DOTS, "limo.talk.joe.ranger.4c");
  const strips = ["desert-l", "desert-r"].map((id) => g.effects.get(id)).filter(Boolean), from = strips.map((s) => s.speed);
  const slowing = g.tween(3600, (k) => strips.forEach((s, i) => s.set({ speed: from[i] * (1 - k) })), g.ease.out);
  await g.wait(600);
  await g.say("limo.lunch.slowing");
  await slowing;
  await g.wait(600);
  await g.fade(1, 900);
  const L = (id, or) => (g.lines[id] ? g.lines[id][1] : or);
  await g.card(L("limo.card.1", "THE OFFICE OF PECULIAR SECTORS"), L("limo.card.2", "Desert Field Headquarters, the same afternoon"), { plain: true, ms: 3800 });
  g.flag("limo.done", true);
  await g.cutscene("office-arrive");                                              // SCENES-17: on to the Office (the demo's end is "Going Down" now)
}

// ---------- the opening: "Meanwhile, in a limousine" (the beat limo.arrive) ----------
async function opening(g) {
  const r = g.actor("ranger");
  await g.wait(900);
  await g.say("limo.open.1");
  await g.wait(300);
  await slide(g, true);
  await g.say("limo.open.2", "limo.open.3", "limo.open.4");
  await slide(g, false);
  await g.wait(500);
  // Ranger comes up from under the facing seat (at its near end, by the little fridge), in his mirror shades.
  if (r) {
    r.place(AT.fridge[0], AT.fridge[1] + 10, scaleAt(g.scene, AT.fridge[1]));
    r.face("W");
    r.hidden = false;
    r.sit(true, true);
    await g.tween(420, (k) => { r.fade(k); r.place(AT.fridge[0], AT.fridge[1] + 10 - 10 * k, scaleAt(g.scene, AT.fridge[1])); });
    await g.wait(300);
  }
  await g.say("limo.open.5", "limo.open.6");
  if (r) {
    r.sit(false, true);
    await g.walkTo(RANGER[0], RANGER[1], "ranger");
    r.face("W");
    r.sit(true, true);
    await g.wait(250);
  }
  // LETTER-17: and with the divider up, where the suits cannot hear, quietly: the first thing he says to Ranger. The
  // promise he made Mom at the wide door ("Porch light on. However long it takes.": nevada.through.joe.6).
  await g.say("limo.promise", DOTS, "limo.promise.joe");
  await g.say(DOTS);                                                               // he looks at the ropes
  if (r) await r.play(g.clock, "look", { ms: 900 });
  g.flag("limo.arrived", true);
  if (div) div.left = UP_MS;
  g.ui.toast("Play as Grandpa Joe or Ranger: use the portraits", 5200);
}

// ---------- the things in the back: what each of them sees, and does ----------
/** A look: Grandpa Joe's own words; Ranger's "..." and what Grandpa Joe says he means. */
const looks = (thing, ranger = `limo.${thing}.ranger.joe`) => ({ grandpajoe: `limo.${thing}.joe`, ranger: [`limo.${thing}.ranger`, ranger] });
const HANDS = "limo.ropes.joe";                                                    // "I'd need hands for that, and mine are busy bein' tied."

export default {
  id: "nevada-limo",
  era: "nevada",
  name: "The back of a limousine",
  travel: false,                                           // MAP-15: nobody leaves by the map: Grandpa Joe is belted in, and the limousine has no way out

  // DEPTH. The painter's camera: a seated eye, the cartoon's roomy car (layout.json "view"). maxScale 1.22, so that Ranger
  // keeps growing to the near edge of the carpet (the engine's default is 1.12).
  horizon: 220, full: 355, maxScale: 1.22,
  // The carpet between the seats, from the bar under the divider to where Ranger is drawn at 1.22. Grandpa Joe is never on it.
  walk: { area: [[345, 326], [495, 329], [532, 385], [304, 381]] },

  party: ["grandpajoe", "ranger"],
  spawn: { default: JOE, grandpajoe: JOE, ranger: RANGER },
  facing: "W",
  // NEVADA-12SC: the leads who never walk here. Grandpa Joe is belted to the long seat, tied or not ("Regulations.").
  still: ["grandpajoe"],
  music: (g) => (g.flag("limo.singing") ? "rag" : null),

  picture: art + "back.png",
  planes: [
    // The divider's two pictures are drawn on the light layer (`live`, below), where the glass can slide; listed here,
    // never shown, so that they are fetched with the scene's other pictures and the game's.
    { id: "divider-pictures", states: { up: art + "divider-up.png", down: art + "divider-down.png" }, plane: "back", when: () => false },
    // The bow and the loose end on the cushion beside him: four strands, then three, two, one; gone when he is loose.
    // Its base is just in front of his ground point: he is behind it, Ranger (sorted by the carpet under him) in front.
    { id: "ropes", states: { 4: art + "ropes-4.png", 3: art + "ropes-3.png", 2: art + "ropes-2.png", 1: art + "ropes-1.png" }, base: 329,
      state: (g) => String(Math.max(1, 4 - strands(g))), when: (g) => !loose(g) },
    // On the facing seat: lunch, paperwork and a beverage. Each goes when it is taken; a figure on the carpet is in front.
    { id: "bag", src: art + "bag.png", base: [[500, 330], [699, 616]], when: (g) => !g.flag("limo.bagTaken") },
    { id: "juice", src: art + "juice.png", base: [[500, 330], [699, 616]], when: (g) => !g.flag("limo.juiceTaken") },
    { id: "clipboard", src: art + "clipboard.png", base: [[500, 330], [699, 616]], when: (g) => !g.flag("limo.clipboardTaken") },
    { id: "front", src: art + "front.png", plane: "front" },                      // the seat we sit on, and its two armrests
  ],

  // THINGS THAT MOVE BY NATURE: the desert going by the windows. DRIVE-16M: the world outside as the scene's own camera sees
  // it from the moving car (two drives, js/engine/effects.js; the pictures PAINT-16's, DRIVE-16P), each side its own country:
  // the left looks across the oncoming lane, its white edge line rushing by under the panes, to the long ranges across the
  // valley and a ranch in the middle distance; the right straight onto the desert, a fence along the road, the telephone
  // line far out with its wires, and nearer, lower hills. Everything comes out of the far end of the windows small and slow
  // and goes out past the near edge large and fast: the ranges hardly move, the middle distance drifts, the fence rushes.
  // Each side has its own pictures (`-l` and `-r`: lit for their side, the sun low on the car's right and a little behind).
  // The ending's script reads and sets their `speed` (metres a second) as it did the strips'.
  fx: [
    { id: "desert-l", type: "drive", side: "L", ...DRIVE_CAM, speed: 16, ...DRIVE_SUN,           // (DRIVE-16F: the things' shadows)
      windows: [[[300.1, 250.4], [242.1, 264.5], [242.1, 201.7], [300.1, 207.5]], [[232.2, 267.0], [0.0, 323.8], [0.0, 177.4], [232.2, 200.7]]],
      sky: "drive-sky.png",
      bands: [{ src: "drive-far-l.png", distance: 6000, ppm: 0.07 }, { src: "drive-mid-l.png", distance: 850, ppm: 0.5 }],
      ground: { src: "drive-ground-l.png", from: 6, ppm: 16 },
      things: { src: "drive-things.png", rows: [
        { sprite: "reflector-l", every: [38, 70], at: [9.9, 10.3] },                 // white posts past the shoulder: one every three or four seconds
        { sprite: "marker-l", every: 1609, at: 10.4, offset: 1200 },               // a mile marker every mile (`offset`: clear of the signs)
        { sprite: ["sign-back-l", "sign-back-2-l"], every: [600, 1300], at: [10.5, 11.5] },   // the oncoming lane's signs, from behind
        { sprite: ["sage-1-l", "sage-2-l", "sage-3-l", "sage-1-l", "rabbitbrush-l", "creosote-l"], every: [3, 16], at: [10.8, 24] },
        { sprite: ["sage-1-l", "sage-2-l", "sage-3-l", "creosote-l"], every: [3, 14], at: [24, 70] },
        { sprite: ["joshua-l", "joshua-2-l"], every: [80, 240], at: [16, 90] },
        { sprite: "rock-l", every: [60, 180], at: [11, 45] }] },
      haze: "#b6bee0", haze_far: 3000, wire: "#2c2a32", seed: 8 },
    { id: "desert-r", type: "drive", side: "R", ...DRIVE_CAM, speed: 16, ...DRIVE_SUN,           // (DRIVE-16F: the things' shadows)
      windows: [[[544.4, 251.9], [604.9, 267.9], [604.9, 200.3], [544.4, 206.9]], [[615.6, 270.8], [800.0, 319.7], [800.0, 179.1], [615.6, 199.1]]],
      sky: "drive-sky.png",
      bands: [{ src: "drive-far-r.png", distance: 3000, ppm: 0.14 }, { src: "drive-mid-r.png", distance: 850, ppm: 0.5 }],
      ground: { src: "drive-ground-r.png", from: 6, ppm: 16 },
      things: { src: "drive-things.png", rows: [
        { sprite: ["post-r", "post-r", "tpost-r"], every: 4.6, at: 9.5, wires: [1.25, 0.95, 0.65] },   // the fence, rushing past below the eye
        { sprite: "pole-r", every: 55, at: 70, wires: [8.6, 8.1] },               // far out, so that its wires show (beside the road: only its feet)
        { sprite: "sign-range-r", every: [600, 1300], at: [7, 8] },
        { sprite: ["sage-1-r", "sage-2-r", "sage-3-r", "sage-2-r", "rabbitbrush-r", "creosote-r"], every: [3, 16], at: [10.4, 24] },
        { sprite: ["sage-1-r", "sage-2-r", "sage-3-r", "creosote-r"], every: [3, 14], at: [24, 70] },
        { sprite: ["joshua-r", "joshua-2-r"], every: [80, 240], at: [17, 90] },
        { sprite: "rock-r", every: [60, 180], at: [11, 45] },
        { sprite: "sign-services-r", every: 9000, at: 7.4, offset: 300 }] },      // one, some 18 s in
      haze: "#b6bee0", haze_far: 3000, wire: "#2c2a32", seed: 7 },
  ],

  // LIGHT AND THE DIVIDER, on the light layer: the divider down, under; over it the glass, cut to the opening, which
  // slides; and the notes of the Last Stop Rag over Grandpa Joe's head while he hums (drawn by the scene's clock).
  live(kit, g) {
    // (the game's stamped address for each picture; for the storyboard, which hands a game of its own with no `assets` and
    // is a page in tools/, the picture's address from the game's own folder)
    const url = (file) => (g && g.assets && g.assets.url ? g.assets.url(art + file) : new URL("../../../" + art + file, import.meta.url).href);
    const pic = (id, file) => `<image id="${id}" href="${url(file)}" width="800" height="600" style="image-rendering:pixelated"/>`;
    const note = (flag) => `<g opacity="0"><ellipse cx="0" cy="0" rx="3.4" ry="2.6" transform="rotate(-20)" fill="#fff4c8"/><rect x="2.4" y="-13" width="1.3" height="13" fill="#fff4c8"/>${flag ? `<path d="M3.6,-13 q5,3 4,9" fill="none" stroke="#fff4c8" stroke-width="1.3"/>` : ""}</g>`;
    return `<defs><clipPath id="div-slot"><rect x="327" y="208" width="189" height="57"/></clipPath></defs>
      ${pic("div-down", "divider-down.png")}
      <g clip-path="url(#div-slot)">${pic("div-glass", "divider-up.png")}</g>
      <g id="notes" opacity="0" shape-rendering="geometricPrecision">${note(true)}${note(false)}${note(true)}</g>`;
  },

  // Back to front: a later area lies over an earlier one. The long seat and the facing seat first (big), Grandpa Joe on the
  // long seat over them (for Ranger: a word with him), the windows, and the small things over all of them.
  hotspots: [
    { id: "seat", name: "long seat", poly: [[145, 574], [345, 321], [345, 292], [301, 252], [0, 331], [145, 474]], walkTo: AT.joe, face: "W", look: looks("seat"), use: looks("seat") },
    { id: "facingseat", name: "facing seat", poly: [[699, 600], [687, 600], [500, 330], [500, 299], [551, 256], [800, 326], [800, 425], [699, 504]], walkTo: AT.bag, face: "E", look: looks("facingseat"), use: looks("facingseat") },
    // Grandpa Joe, for Ranger: his figure on the seat (and not the bow and the belt beside him, which have areas of their own, over this).
    { id: "joe", name: "Grandpa Joe", verb: "Talk to", mate: "grandpajoe", plane: "grandpajoe", poly: [[296, 232], [330, 228], [346, 262], [350, 300], [372, 316], [366, 330], [300, 330], [292, 292]],
      when: (g) => who(g) === "ranger" },
    { id: "window-l", name: "window", rect: [0, 177, 300, 146], walkTo: AT.windowL, face: "W", look: looks("window"), use: looks("window") },
    { id: "window-r", name: "window", rect: [544, 179, 255, 140], walkTo: AT.windowR, face: "E", look: looks("window"), use: looks("window") },
    { id: "fridge", name: "little fridge", verb: "Open", rect: [580, 388, 99, 194], walkTo: AT.fridge, face: "E", look: looks("fridge"),
      use: { grandpajoe: "limo.fridge.joe", ranger: async (g) => { await g.actor("ranger").play(g.clock, "reach"); await g.say("limo.fridge.ranger", "limo.fridge.ranger.joe"); } } },
    { id: "divider", name: "divider", verb: "Talk through", rect: [321, 202, 201, 69], walkTo: AT.divider, face: "N",
      look: { grandpajoe: "limo.divider.joe", ranger: ["limo.divider.ranger", "limo.divider.ranger.look.joe"] },
      use: { grandpajoe: atDivider, ranger: [DOTS, "limo.divider.ranger.joe"] } },
    { id: "phone", name: "car phone", verb: "Pick up", rect: [366, 263, 28, 53], walkTo: AT.phone, face: "N",
      look: { grandpajoe: "limo.phone.joe", ranger: ["limo.phone.ranger", "limo.phone.ranger.look.joe"] },
      use: { grandpajoe: "limo.phone.joe", ranger: async (g) => { await g.actor("ranger").play(g.clock, "reach"); await g.say(DOTS, "limo.phone.ranger.joe"); } } },     // he lifts it off the hook, and it says nothing
    { id: "ashtray", name: "ashtray", rect: [449, 267, 20, 13], walkTo: AT.ashtray, face: "N", look: looks("ashtray"), use: looks("ashtray") },
    { id: "belt", name: "seatbelt", rect: [271, 312, 47, 11], walkTo: AT.belt, face: "W", look: looks("belt"),
      use: { grandpajoe: (g) => g.say(loose(g) ? "limo.ropes.regs" : "limo.belt.joe"), ranger: looks("belt").ranger } },
    // The ropes beside him: four strands and a bow, and after #14 what is left of them (the cut-out goes; the place stays, and
    // the two of them have a word for what Ranger has done to it).
    { id: "ropes", name: "ropes", verb: "Nibble", plane: "ropes", rect: [287, 295, 42, 27], walkTo: AT.ropes, face: "W",
      look: (g) => g.say(...(who(g) === "ranger" ? ["limo.ropes.ranger", loose(g) ? "limo.ropes.ranger2.joe" : "limo.ropes.ranger.joe"] : [loose(g) ? "limo.ropes.look2.joe" : "limo.ropes.look.joe"])),
      use: { grandpajoe: (g) => g.say(loose(g) ? "limo.ropes.look2.joe" : HANDS), ranger: ropes } },
    { id: "bag", name: "paper bag", verb: "Open", plane: "bag", rect: [543, 292, 30, 38], walkTo: AT.bag, face: "E", when: (g) => !g.flag("limo.bagTaken"),
      look: looks("bag"), use: { grandpajoe: (g) => (loose(g) ? lunch(g) : g.say("limo.lunch.bag.early")), ranger: bagRanger } },
    { id: "juice", name: "juice box", plane: "juice", rect: [576, 325, 21, 33], walkTo: AT.juice, face: "E", when: (g) => !g.flag("limo.juiceTaken"),
      look: looks("juice"), use: { grandpajoe: (g) => (loose(g) ? juice(g) : g.say(HANDS)), ranger: looks("juice").ranger } },
    { id: "clipboard", name: "clipboard", verb: "Read", plane: "clipboard", rect: [628, 336, 58, 74], walkTo: AT.clipboard, face: "E", when: (g) => !g.flag("limo.clipboardTaken"),
      look: looks("clipboard"),
      use: { grandpajoe: (g) => (loose(g) ? lunch(g) : g.say(HANDS)),
        ranger: async (g) => { const r = g.actor("ranger"); if (r) await r.play(g.clock, "wash", { ms: 1500 }); await g.say(DOTS, "limo.lunch.clipboard.joe"); } } },     // he reads it with his paws: it is a clipboard
  ],

  // What the two of them say to each other: Grandpa Joe's word, Ranger's "...", and what Grandpa Joe says he means.
  talk: {
    grandpajoe: {
      ranger: [
        ["limo.talk.joe.ranger.1a", DOTS, "limo.talk.joe.ranger.1c"],
        ["limo.talk.joe.ranger.2a", DOTS, "limo.talk.joe.ranger.2c"],
        { when: (g) => loose(g), say: ["limo.talk.joe.ranger.3a", DOTS, "limo.talk.joe.ranger.3c"] },
        { when: (g) => !!g.flag("limo.map"), say: ["limo.talk.joe.ranger.4a", DOTS, "limo.talk.joe.ranger.4c"] },
      ],
    },
    ranger: {
      grandpajoe: [[DOTS, "limo.talk.ranger.joe.1c"], [DOTS, "limo.talk.ranger.joe.2c"],
        // PASS-17N: once he is loose, Ranger mentions the ropes himself, as Grandpa Joe said he would (limo.talk.joe.ranger.3c)
        { when: (g) => loose(g), say: [DOTS, "limo.talk.ranger.joe.3c"] }],
    },
  },

  // Make the picture match the story facts. Runs on arrival and after loading a save.
  setup(g) {
    const build = ++builds, scene = this;
    div = { k: 0, left: UP_MS, moving: false, build, t: 0 };
    setDivider(g, restsDown(g) ? 1 : 0);
    seatJoe(g);
    const r = g.actor("ranger");
    if (r) {
      if (r.variant) r.variant("shades");                                           // he wears them for the rest of the game (#10)
      if (!g.flag("limo.arrived")) { r.hidden = true; r.fade(0); }                  // (under the facing seat, till the opening brings him up)
      else if (r.sit) r.sit(true, true);
    }
    const me = { t: 0 }, stop = g.clock.every((dt) => { if (g.scene !== scene || !div || div.build !== build) return stop(); tick(g, me, dt); });
  },

  async enter(g) {
    await Promise.all(["divider-up.png", "divider-down.png"].map((f) => g.assets.picture(art + f)));
    if (!g.flag("limo.arrived")) await opening(g);
    else if (g.flag("limo.done") && !g.flag("office.arrived")) await g.cutscene("office-arrive");      // SCENES-17: a game saved at the gate goes on to the Office
  },
};
