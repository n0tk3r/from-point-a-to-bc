// Act Five, continued: Interview Room C, the Comfortable Room (SCENES-17: new in round seventeen; briefs/SCENES-17.md, and
// the design, briefs/out/office-hq-design.md, section 4). INTERVIEW ROOM C. THIS ROOM HAS BEEN RATED COMFORTABLE. A table
// and three chairs, a fourth in the corner under the ceiling vent, a plastic plant, a water cooler, a wall clock, a
// thermostat (72), a long one-way mirror, an intercom (DISPATCH. PRESS TO TALK.), a poster (PECULIAR? REPORT IT.), and a
// door locked "for your comfort".
//
// GRANDPA JOE plays here (Ranger looks down into it from the duct, and once the suits have gone may drop into it):
//   #17 The Comfortable Room   the interview (interviewTree, js/content/talk/office.js) with Dale and Merle across the
//                              table; from his chair he can look at anything, and the suits answer whatever he tries. Once
//                              the fans are off (#16) the room warms, 72, 77, 81 (office-common.js: the heat): Merle mops,
//                              Dale loosens his tie, the plastic plant droops; at 81, asked about the heat (in the talk or
//                              at the thermostat) or how comfortable he is, Regulation 9: they suspend the interview, gather
//                              up the questionnaire, lock the door and go (office.alone). He prays, short, and looks up.
//   #18 The Bearer             he stands on the spare chair under the vent (office.onChair: he does everything from up
//                              there, and steps down to walk); with Ranger at the grille they talk (ventTree), and the
//                              receipt goes up through the slats (or he hands it up himself). The receipt's journey ends in
//                              Property & Effects (office-property.js), and then the key in the door: Opal with the banjo
//                              (opalTree), "Forty-one statements of nothing, Joe Hollis."
//   #19 Wendell's Pie          the intercom (intercomTree): on Jed's behalf, and the hook `burger` cuts away to the break
//                              room, where Jed is up so fast the ice pack is still in the air. Things handed down to him:
//                              the pie tin, the peanuts, and the test schedule, which he reads on his chair.
//   #20 A Soundproof Room      the pie tin used on the banjo (with anything here: the engine has no thing used on a thing
//                              in the pockets): a new head, one string, and the Last Stop Rag through every vent; the door,
//                              Dale and Merle, Wendell with his fingers in his ears (ragTree), and, with the schedule read,
//                              B-7: "Going Down" (js/content/cutscenes/office-down.js).
// RANGER, from above (the grille ROOM C, office-ducts.js), sees the room as it is and every thing answers him (`peek`);
// with the suits gone he calls Joe up onto the chair, hands things down to him, and drops in onto the chair's seat (a floor
// of its own): then he hops down, washes up in a paper cone, presses the intercom, and climbs back up the way he came.
//
// Every place is the painter's own measurement of the finished picture (art/scenes/office-room/layout.json, PAINT-17C's
// ready.md), or was set by eye against the picture with the people in it; where the two differ the comment says why.
//
// Try it: index.html?scene=office-room&lead=grandpajoe&flags=office.arrived
// Later:  &flags=office.arrived,office.acOff (the heat: 81 at once, with no time of #16 to work from), office.alone

import { STOCK, ANNOUNCE, BUILDING, WORDS, who, is, heard, heat, keepHeat, chatter, swap, shades, rangerAt, joeHears, onChair, think, thought, cutAway } from "./office-common.js";
import { interviewTree, ventTree, opalTree, intercomTree, ragTree, ventTalk, nowAndThen, SUSPEND } from "../talk/office.js";
import { scaleAt } from "../../engine/walk.js";
import { icePackAt } from "../../art/people.js";

const art = "art/scenes/office-room/";

// ---------- the room, from its camera (layout.json: horizon 295, full 446) ----------
// maxScale 1.25: the floor's front edge (row 479) is 1.22 by the camera, and the spare chair's front (atchair) 1.19.
const FLOOR = [[133, 451], [456, 413], [472, 419], [500, 416], [553, 435], [528, 439], [565, 453], [590, 448], [631, 463], [603, 471], [595, 479], [424, 479], [301, 479], [190, 479], [80, 479], [84, 470], [130, 464]];
// The spare chair's seat, under the vent: Ranger's floor in here (he lands on it, and climbs back from it), at the floor's
// size under it and sorted just in front of the chair (layout.json marks.vent: scale 1.078, base 467).
const SEAT_AREA = [[92, 409], [108, 409], [108, 415], [92, 415]];
const SEAT = [100, 412], SEAT_SCALE = 1.078, CHAIR_BASE = 467;

// ---------- where people are (layout.json marks and stands) ----------
const JOE = [344, 454];                // at the table on his chair, facing E (the floor under his hips: behind the table's row 458)
const AT_JOE = [361, 469];             // on his feet in front of it (stands.atjoe)
const CHAIR = [96, 458];               // Grandpa Joe standing on the spare chair: the floor under its seat (PEOPLE-17: the rig lifts him the seat's height)
const AT_CHAIR = [113, 474];           // in front of the spare chair (stands.atchair): he gets up onto it from here
const VENT = [106, 201];               // the grille's middle, where the eyes are, and where a thing handed down comes from
const DALE = [439, 431], MERLE = [469, 446];
const DOOR = [186, 452], HALL = [183, 428], OPAL = [208, 460];
const MEET_OPAL = [292, 470];          // Grandpa Joe, a step from Opal at her mark, turned to her
const AT_DOOR = { suit1: [205, 458], suit2: [240, 464], suit3: [183, 430] };      // the Rag: Dale and Merle in the doorway, Wendell behind them in the hall
const INTERCOM_WORDS = [290, 300];     // Houston on the intercom: her words come out of its grille
const VENT_WORDS = [215, 185];         // anyone not on the stage (Ranger at the grille): by the vent

// ---------- what the room is doing now that is not saved (the scene's own, made again whenever it is built) ----------
const room = { heat: 0, playing: false, lit: false };

// ---------- who is where ----------
const alone = (g) => is(g, "office.alone");
const carries = (g, id, item) => ((g.store.data.inventory || {})[id] || []).includes(item);
const ranger = (g) => g.actor("ranger");
const joe = (g) => g.actor("grandpajoe");
const eyes = (g) => rangerAt(g, "over-room");            // Ranger at the grille over the room: two eyes in a mask in the vent
const onSeat = (g) => { const r = ranger(g), f = r ? g.floorOf(r) : null; return !!f && f.name === "seat"; };
const sizeAt = (y) => Math.min(1.25, Math.max(0.1, (y - 295) / (446 - 295)));

/** Grandpa Joe as he is by the story: at the table while they question him; on the spare chair; or on his feet, with what he
    carries (the banjo broken, or mended with the pie tin) in his hands. */
function joeKind(g) {
  if (!alone(g)) return "grandpajoe-table";
  if (onChair(g)) return "grandpajoe-chair";
  if (carries(g, "grandpajoe", "banjo-pie")) return "grandpajoe-banjo-pie";
  if (carries(g, "grandpajoe", "banjo-broken")) return "grandpajoe-banjo-broken";
  return "grandpajoe-room";
}
/** Put him where and as the story has him (whatever figure the stage made for him: it makes the rocking chair's). */
function placeJoe(g, at = null) {
  if (!joe(g)) return null;
  const kind = joeKind(g);
  let f;
  if (kind === "grandpajoe-table") f = swap(g, "grandpajoe", kind, JOE, "E", sizeAt(JOE[1]));
  else if (kind === "grandpajoe-chair") { f = swap(g, "grandpajoe", kind, CHAIR, "S", sizeAt(CHAIR[1])); f.base = CHAIR_BASE; return f; }
  else { const j = joe(g); f = swap(g, "grandpajoe", kind, at || [j.x, j.y], at ? "SE" : null, sizeAt((at || [j.x, j.y])[1])); }
  f.base = null;
  return f;
}
/** Dale and Merle sweat once the room is warm (PEOPLE-17's -hot kinds: their life mops, and loosens the tie). */
function suitsHot(g) {
  const hot = heat(g) >= 77;
  for (const id of ["suit1", "suit2"]) {
    const a = g.actor(id);
    if (a && !a.up && !a.walking && a.kind !== `${id}-${hot ? "hot" : "table"}` && /-(table|hot)$/.test(a.kind)) swap(g, id, `${id}-${hot ? "hot" : "table"}`);
  }
}

// ---------- the door ----------
async function door(g, open) {
  const shut = g.plane("door"), wide = g.plane("door-open");
  if (open) g.sfx("unlock");
  if (shut) shut.show(!open);
  if (wide) wide.show(!!open);
  if (!open) g.sfx("latch");
  await g.wait(200);
}
/** Someone of the Office goes out through the door: across the floor round the table to it, out into the hall, and gone. */
async function goOut(g, id, delay = 0) {
  const a = g.actor(id);
  if (!a) return;
  if (delay) await g.wait(delay);
  const map = g.groundFor(id);
  await a.walkPath(g.clock, map.path([a.x, a.y], DOOR), (y) => sizeAt(y));
  await Promise.all([a.walkPath(g.clock, [HALL], (y) => sizeAt(y)), g.tween(400, (k) => a.fade(1 - k))]);
  g.view.cast.remove(id);
}
/** Someone comes in from the hall to a place in the room (straight in through the doorway). */
async function comeIn(g, id, kind, to, face = "W") {
  const a = g.view.cast.addFigure(id, kind, HALL[0], HALL[1], sizeAt(HALL[1])).face("S");
  a.fade(0);
  await g.view.cast.load();
  await Promise.all([a.walkPath(g.clock, [DOOR, to], (y) => sizeAt(y)), g.tween(350, (k) => a.fade(k))]);
  a.face(face);
  return a;
}

// ---------- #17: the interview ----------
/** The hook `mop`: Merle mops his forehead; Dale loosens his tie a finger's width, and puts it back. */
async function mop(g) {
  const m = g.actor("suit2"), d = g.actor("suit1");
  if (m && m.fidget) m.fidget("mop");
  if (d && d.fidget) d.fidget("loosen");
  await g.wait(300);
}
/** The hook `suspend` (#17's end, after Regulation 9 has been read: the tree, or the thermostat, says SUSPEND and sets
    office.alone): they gather the questionnaire, get up, apologize their way out and lock the door. Grandpa Joe alone. */
async function suspend(g) {
  const q = g.plane("questionnaire");
  if (q) q.show(false);                                                        // (gathered up)
  await Promise.all(["suit1", "suit2"].map((id) => { const a = g.actor(id); return a && a.sit ? a.sit(false) : null; }));
  await door(g, true);
  await Promise.all([goOut(g, "suit1"), goOut(g, "suit2", 500)]);
  await door(g, false);                                                        // locked, for his comfort
  await g.wait(700);
  const j = joe(g);
  await g.say("office.room.alone.1");
  if (j && j.pray) j.pray(true);                                               // a short prayer of his own
  await g.say("office.room.alone.2", "office.room.alone.3");
  if (j && j.pray) j.pray(false);
  await g.wait(400);
  // up out of his chair where he sat, a step forward; and he looks up at the vent
  if (j && j.sit) await j.sit(false);
  const up = placeJoe(g, AT_JOE);
  if (up) { up.look(VENT[0], VENT[1] + 120); }
  await g.view.cast.load();
  g.rememberPlace("grandpajoe");
}
const INTERVIEW = interviewTree({ suspend, mop });
async function interview(g) {
  const j = joe(g);
  if (j && !alone(g)) j.face("E");
  await g.talk(INTERVIEW);
}

// ---------- Grandpa Joe and the spare chair ----------
/** Up onto the spare chair under the vent (alone): he does everything from up there, and steps down to walk. */
async function upOnChair(g) {
  if (onSeat(g)) return g.say(g.fallback("nope"));                             // (Ranger is sitting on it)
  if (!heard(g, "office.room.corner.use.grandpajoe")) await g.say("office.room.corner.use.grandpajoe");
  g.flag("office.onChair", true);
  placeJoe(g);
  await g.view.cast.load();
  g.rememberPlace("grandpajoe");
}
/** Down off it again, in front of it. */
async function stepDown(g) {
  if (!onChair(g)) return;
  g.flag("office.onChair", false);
  placeJoe(g, AT_CHAIR);
  await g.view.cast.load();
  g.rememberPlace("grandpajoe");
}
/** Grandpa Joe at the spare chair: with the suits there, "please remain in your chair"; alone, up onto it (or down off it). */
async function cornerUse(g) {
  if (!alone(g)) return g.say("office.room.corner.use.suits");
  if (onChair(g)) return stepDown(g);
  await g.walkTo(AT_CHAIR[0], AT_CHAIR[1]);
  if (g.lead) g.lead.face("NW");
  return upOnChair(g);
}
/** A use of Grandpa Joe's that wants him on the floor: down off the chair first, and over to it. */
const low = (fn, to = null, face = null) => async (g) => {
  if (who(g) === "grandpajoe" && onChair(g)) {
    await stepDown(g);
    if (to) { await g.walkTo(to[0], to[1]); if (face && g.lead) g.lead.face(face); }
  }
  return fn(g);
};

// ---------- the vent: the two of them, and things up and down through the slats ----------
/** The hook `receiptUp` (ventTree), and the receipt used on the vent: he reaches up and pushes it through the slats. */
async function passUp(g, item) {
  const j = joe(g);
  if (j && j.hold) j.hold(false);
  const passing = j && j.fidget ? j.fidget("passup") : null;                   // (the receipt in his hand until 0.52 of it: his hand is through the slats)
  await g.wait(1144);
  g.pass(item, "ranger");
  if (passing) await passing;
}
const VENT_TREE = ventTree({ receiptUp: (g) => passUp(g, "receipt") });
/** Grandpa Joe at the vent: from the floor he cannot reach it; on the chair, with Ranger at the grille, they talk; with
    nobody up there, the duct. */
async function ventUse(g) {
  if (!onChair(g)) return g.say("office.room.vent.use.grandpajoe");
  if (!eyes(g)) return g.say(heard(g, "office.room.vent.empty.1") ? "office.room.vent.empty.2" : "office.room.vent.empty.1");
  const j = joe(g);
  if (j && j.hold) j.hold(true, "reach");
  try { await g.talk(VENT_TREE); } finally { if (j && j.hold) j.hold(false); }
}
/** Something used on the vent by Grandpa Joe: handed up to Ranger, or not (a banjo will not go through the slats). */
async function handUp(g, item) {
  if (!onChair(g)) return g.say("office.room.vent.use.grandpajoe");
  if (!eyes(g)) return g.say(heard(g, "office.room.vent.empty.1") ? "office.room.vent.empty.2" : "office.room.vent.empty.1");
  if (item === "receipt") {
    await g.say("office.vent.receipt.up");
    await passUp(g, "receipt");
    g.flag("office.receiptUp", true);
    return g.say("office.vent.receipt.got");
  }
  if (item === "peanuts") { await g.say("office.vent.up.peanuts"); return passUp(g, "peanuts"); }
  const no = { sectormap: "office.vent.up.sectormap", "banjo-broken": "office.vent.up.banjo", "banjo-pie": "office.vent.up.banjo", pietin: "office.vent.up.pietin", schedule: "office.vent.up.schedule" };
  return g.say(no[item] || g.fallback("nope"));
}
/** Ranger at the grille, the suits gone, Grandpa Joe at the table: Ranger calls him (he hears), and up onto the chair he gets. */
async function callJoe(g) {
  await g.say("office.vent.call.ranger", "office.vent.call.joe");
  const j = joe(g);
  if (j) {
    const map = g.groundFor("grandpajoe");
    await j.walkPath(g.clock, map.path([j.x, j.y], AT_CHAIR), (y) => sizeAt(y));
  }
  g.flag("office.onChair", true);
  placeJoe(g);
  await g.view.cast.load();
  g.rememberPlace("grandpajoe");
}
/** A thing used on the vent: Grandpa Joe on the chair hands it up (or not); on the floor, the banjo and the pie tin are for
    playing and mending as anywhere; Ranger (in the room) keeps what he has. */
function ventWith(g, item) {
  if (who(g) !== "grandpajoe") return g.say(g.fallback("nope"));
  if (!onChair(g) && JOE_WITH[item]) return JOE_WITH[item](g);
  return handUp(g, item);
}
/** Ranger, from above, at Grandpa Joe: with the suits there, a look up and "Not now"; alone at the table, he calls him up;
    on the chair, a word between them (ventTalk). */
async function fromAbove(g) {
  if (!alone(g)) return g.say("office.room.vent.eyes.suits.grandpajoe");
  if (!onChair(g)) return callJoe(g);
  return g.chat("grandpajoe");
}
/** A thing handed down through the grille by Ranger (from above: on Grandpa Joe or anything near the vent; or on the
    grille itself, from the duct: office-ducts.js looks down first, then calls this). The pie tin, the peanuts and the
    schedule go to Joe; the bottle cap and the receipt do not (his best, for trading; Opal's). With the suits there, no. */
async function handDown(g, item) {
  if (!alone(g)) return g.say("office.duct.drop.suits.ranger");
  if (item === "receipt") return g.say("office.vent.down.receipt.ranger", "office.vent.down.receipt.joe");
  if (item === "bottlecap") return g.say("office.vent.down.bottlecap.ranger", "office.vent.down.bottlecap.joe");
  if (!["pietin", "peanuts", "schedule"].includes(item)) return g.say(g.fallback("nope"));
  const j = joe(g);
  if (onChair(g) && j) {                                                       // into his hands, through the slats
    const taking = j.fidget ? j.fidget(item === "pietin" ? "taketin" : "takepaper") : null;
    await g.wait(1196);
    g.pass(item, "grandpajoe");
    if (taking) await taking;
  } else {                                                                     // it falls onto the spare chair's seat
    g.pass(item, "grandpajoe");
    await g.arrive(item, VENT, { to: SEAT, ms: 700 });
    await g.say("office.vent.down.table");
  }
  if (item === "pietin") return g.say("office.vent.down.pietin.1", "office.vent.down.pietin.ranger", "office.vent.down.pietin.joe");
  if (item === "peanuts") return g.say("office.vent.down.peanuts");
  // the schedule: he reads it, on his chair under the vent (#19's end: the stage's revelation)
  if (j && j.hold && onChair(g)) j.hold(true, "read");
  await g.say("office.schedule.read.1", "office.schedule.read.2", "office.schedule.read.3", "office.schedule.read.4", "office.schedule.read.5",
    "office.schedule.read.6", "office.schedule.read.7", "office.schedule.read.ranger", "office.schedule.read.8", "office.schedule.read.9");
  if (j && j.hold) j.hold(false);
  g.flag("office.schedule", true);
}

// ---------- Ranger in the room ----------
/** Off the chair's seat, down to the floor (a hop). */
async function hopDown(g) {
  if (!onSeat(g)) return;
  await g.climbTo(AT_CHAIR, { path: [[110, 440]], set: "drop", face: "E" });
}
/** Up from the floor onto the chair's seat (not while Grandpa Joe is standing on it). */
async function toSeat(g) {
  if (onSeat(g)) return true;
  if (onChair(g)) { await g.say(g.fallback("nope")); return false; }
  await g.walkTo(AT_CHAIR[0], AT_CHAIR[1]);
  await g.climbTo("vent", { path: [[110, 440]], set: "climb", base: CHAIR_BASE, face: "W" });
  return true;
}
/** Up onto the seat, and up through the grille into the duct, the way he came (Joe sees him off). */
async function upAndOut(g) {
  if (!(await toSeat(g))) return;
  if (joe(g)) await g.say("office.room.climb.grandpajoe");
  await g.climbUp({ scene: "office-ducts", spawn: "over-room", to: VENT });
}
/** Ranger presses the intercom: Houston answers anyway. */
async function rangerIntercom(g) {
  const r = ranger(g);
  if (r) { await r.sit(true); await r.play(g.clock, "reach"); }
  g.sfx("buzz");
  lit(g, true);
  WORDS.at = INTERCOM_WORDS;
  try { await g.say("office.room.intercom.press.1", "office.room.intercom.press.2", "office.room.intercom.press.3"); }
  finally { WORDS.at = null; lit(g, false); }
  if (joe(g)) await g.say("office.room.intercom.press.4");
  if (r) await r.sit(false);
}
function lit(g, on) {
  room.lit = !!on;
  const a = g.plane("intercom"), b = g.plane("intercom-lit");
  if (a) a.show(!on);
  if (b) b.show(!!on);
}

// ---------- #19: the intercom ----------
async function press(g) {
  const j = joe(g);
  if (j) { j.face("N"); if (j.hold) j.hold(true, "intercom"); }
  g.sfx("buzz");
  lit(g, true);
  WORDS.at = INTERCOM_WORDS;
}
async function release(g) {
  const j = joe(g);
  if (j && j.hold) j.hold(false);
  lit(g, false);
  WORDS.at = null;
}
/** The hook `burger`: Jed's cheeseburger on every speaker in the building, and in the break room Jed is up so fast the ice
    pack is still in the air (a look at the break room for a moment: office-common.js cutAway); "...Thank you, Houston." */
async function burger(g) {
  WORDS.at = null;
  await g.pa("office.pa.burger");
  const there = await g.getScene("office-breakroom");
  await cutAway(g, "office-breakroom", [
    { id: "suit4", kind: "suit4-asleep", at: [84, 412], face: "E" },
    { id: "agent", kind: "agent-ice", at: [514, 394], face: "W" },
  ], async (g) => {
    g.think("suit4", "zzz", { loop: true });
    const jed = g.actor("agent");
    await g.wait(700);
    if (jed) {
      const [dx, dy] = icePackAt(jed.yaw, jed.sizeNow()), seat = [jed.x, jed.y];
      const pack = g.view.cast.addThing("icepack", "icepack", seat[0] + dx, seat[1] + dy, jed.scale);
      pack.base = seat[1] + 2;
      const up = jed.sit(false);                                               // up so fast the pack is still in the air
      g.wait(700).then(() => g.tween(320, (k) => pack.place(seat[0] + dx, seat[1] + dy - k * k * (dy + 0.262 * jed.sizeNow() * 0.98), jed.scale)))
        .then(() => { pack.options = { state: "down" }; });
      await up;
    }
    await g.say("office.jed.go.1");
    const dooro = g.plane("door-open"), shut = g.plane("door");
    if (dooro) dooro.show(true);
    if (shut) shut.show(false);
    if (jed) jed.walkPath(g.clock, [[640, 392], [715, 380]], (y) => scaleAt(there, y));
    await g.say("office.jed.go.2", "office.jed.go.3");
    await g.wait(500);
  });
  WORDS.at = INTERCOM_WORDS;
}
const INTERCOM = intercomTree({ press, release, burger });
async function intercom(g) {
  if (!alone(g)) return g.say("office.room.intercom.use.suits");
  try { await g.talk(INTERCOM); } finally { await release(g); }
}

// ---------- #18's end: Opal at the door with the banjo ----------
/** The key in the door, and Opal with the banjo in her arms (PEOPLE-17's opal-banjo); then the talk, with the scene's hooks. */
const OPAL_TREE = opalTree({
  sign: async (g) => {
    const o = g.actor("opal");
    await g.reach();                                                           // he signs her slip
    if (o && o.fidget) o.fidget("thunk");
    await g.wait(550);
    g.sfx("stamp");                                                            // THUNK
    await g.wait(500);
  },
  banjo: async (g) => {
    g.give("banjo-broken");
    placeJoe(g);                                                               // the banjo in his hands
    const o = g.actor("opal");
    if (o) swap(g, "opal", "opal-standing");
    await g.view.cast.load();
  },
  leave: async (g) => {
    const o = g.actor("opal");
    if (o) await o.walkPath(g.clock, [DOOR], (y) => sizeAt(y));
  },
  gone: async (g) => {
    const o = g.actor("opal");
    if (o) { await Promise.all([o.walkPath(g.clock, [HALL], (y) => sizeAt(y)), g.tween(400, (k) => o.fade(1 - k))]); g.view.cast.remove("opal"); }
    await door(g, false);                                                      // (gently)
  },
});
async function opalVisit(g) {
  if (onChair(g)) await stepDown(g);
  await g.wait(500);
  await door(g, true);                                                         // the key in the door
  const o = await comeIn(g, "opal", "opal-banjo", OPAL, "E");
  const j = joe(g);
  if (j) { await g.walkTo(MEET_OPAL[0], MEET_OPAL[1]); j.look(o.x, o.y); }
  await g.say("office.room.opal.grandpajoe");
  if (eyes(g)) await g.say("office.room.opal.ranger");                         // two eyes in the vent
  await g.talk(OPAL_TREE);
  if (g.actor("opal")) { g.view.cast.remove("opal"); await door(g, false); }   // (however the talk ended, she has gone)
}

// ---------- #20: the pie tin on the banjo, and the Rag ----------
/** The pie tin and the broken banjo (one used on the other is the engine's thing used on a thing in the room): a new head,
    bracket by bracket; one string, the loudest sound the building has made; and then he plays. */
async function mend(g) {
  if (!(g.has("banjo-broken") && g.has("pietin"))) return g.say(g.has("pietin") ? "item.pietin.grandpajoe" : g.fallback("nope"));
  if (onChair(g)) await stepDown(g);
  await g.say("office.mend.1");
  await g.reach();
  for (let k = 0; k < 3; k++) { g.sfx("click"); await g.wait(260); }
  await g.say("office.mend.2");
  g.take("pietin"); g.take("banjo-broken"); g.give("banjo-pie");
  g.flag("office.mended", true);
  placeJoe(g);
  await g.view.cast.load();
  await g.say("office.mend.3");
  g.sfx("twang-tin");
  await g.wait(1100);
  await g.say("office.mend.4");
  await rag(g);
}
/** The broken banjo, played: one dull clunk. */
async function clunk(g) {
  if (onChair(g)) await stepDown(g);
  swap(g, "grandpajoe", "grandpajoe-play-broken");
  await g.view.cast.load();
  await g.wait(300);
  g.sfx("clunk");
  await g.wait(500);
  await g.say("office.mend.clunk");
  placeJoe(g);
}
/** The hooks of the Rag at the door (ragTree). */
const RAG_TREE = ragTree({
  louder: async (g) => { for (let k = 0; k < 2; k++) { g.sfx("twang-tin"); await g.wait(320); } },
  stop: async (g) => {
    room.playing = false;
    g.music(g.musicOf(g.scene));
    placeJoe(g);
    await Promise.all([goOut(g, "suit1"), goOut(g, "suit2", 300), goOut(g, "suit3", 100)]);
    await door(g, false);
  },
  down: async (g) => { await g.cutscene("office-down"); },
});
/** He plays the pie-tin banjo: the Last Stop Rag through every vent on every floor (the fans are off, and sheet metal carries
    a tune like a trumpet). Houston; then the door: Dale and Merle, and Wendell behind them with his fingers in his ears. */
async function rag(g) {
  if (!g.has("banjo-pie")) return clunk(g);
  if (onChair(g)) await stepDown(g);
  const again = heard(g, "office.pa.music");
  swap(g, "grandpajoe", "grandpajoe-play-pie");
  await g.view.cast.load();
  room.playing = true;
  g.music("rag-tin");
  await g.wait(1200);
  await g.pa("office.pa.music");
  if (again) await g.pa("office.pa.music.2");
  await g.wait(600);
  await door(g, true);
  const j = joe(g);
  await Promise.all([comeIn(g, "suit1", "suit1", AT_DOOR.suit1, "E"), g.wait(350).then(() => comeIn(g, "suit2", "suit2", AT_DOOR.suit2, "E"))]);
  const w = g.view.cast.addFigure("suit3", "suit3-ears", AT_DOOR.suit3[0], AT_DOOR.suit3[1], sizeAt(AT_DOOR.suit3[1])).face("S");
  await g.view.cast.load();
  if (j) j.look(AT_DOOR.suit1[0], AT_DOOR.suit1[1]);
  if (!heard(g, "office.room.wendell.grandpajoe")) await g.say("office.room.wendell.grandpajoe");
  await g.talk(RAG_TREE);
  if (is(g, "office.done")) { await g.title(); return; }                     // Going Down has played: the end of the demo
  if (room.playing || g.actor("suit1")) {                                      // (however else the talk ended: he stops, they go)
    room.playing = false;
    g.music(g.musicOf(g.scene));
    placeJoe(g);
    for (const id of ["suit1", "suit2", "suit3"]) g.view.cast.remove(id);
    await door(g, false);
  }
  if (w) w.hidden = true;
}
/** Every room thing takes the banjo (to play it, broken or mended) and the pie tin (to mend it) in Grandpa Joe's hands. */
const JOE_WITH = { "banjo-pie": (g) => rag(g), "banjo-broken": (g) => clunk(g), pietin: (g) => mend(g) };

// ---------- the looks and uses that change with the story ----------
/** A look of Ranger's here, as a peek (from above) and in the room: his thought, and Joe's reading where Joe can hear him. */
const rlook = (id, reading = id + ".joe") => thought(id, reading);
/** One of the room's areas, for both of them: Grandpa Joe's look and use (with the suits there, and alone), Ranger's look
    (in the room and from above) and use (in the room), and what the two of them can use on it. */
function spot(id, name, shape, walkTo, face, { joeLook = null, joeUse = null, rLook = null, rUse = null, useWith = {}, peekWith = null, drop = false, above = true, when = null, more = {} } = {}) {
  const look = {}, use = {};
  if (joeLook) look.grandpajoe = joeLook;
  if (rLook) look.ranger = rLook;
  if (joeUse) use.grandpajoe = joeUse;
  if (rUse) use.ranger = rUse;
  if (joeUse || rUse) use.any = (g) => g.say(g.fallback("nope"));                // (whoever has no use of it here: a stock reply, never silence)
  const withAll = { ...JOE_WITH, ...useWith };
  const uw = Object.fromEntries(Object.entries(withAll).map(([item, fn]) => [item, (g) => (who(g) === "grandpajoe" || !JOE_WITH[item] || useWith[item] ? g.act(fn) : g.say(g.fallback("nope")))]));
  const peek = rLook && above ? { look: { ranger: rLook }, ...(peekWith ? { useWith: peekWith } : {}), ...(drop ? { drop: true } : {}) } : null;
  return { id, name, ...shape, walkTo, face, look, ...(joeUse || rUse ? { use } : {}), useWith: uw, ...(peek ? { peek } : {}), ...(when ? { when } : {}), ...more };
}
const DOWN = Object.fromEntries(["pietin", "peanuts", "schedule", "bottlecap", "receipt"].map((item) => [item, (g) => handDown(g, item)]));
const byHeat = (cool, warm, hot) => (g) => g.say(heat(g) >= 81 ? hot : heat(g) >= 77 ? warm : cool);
const suitsOr = (withSuits, aloneLine) => (g) => (alone(g) ? g.act(aloneLine) : g.act(withSuits));

/** Grandpa Joe's look at the vent: blowing, still, or with two eyes in it. */
const ventLook = (g) => g.say(eyes(g) ? (alone(g) ? "office.room.vent.eyes.grandpajoe" : "office.room.vent.eyes.suits.grandpajoe")
  : is(g, "office.acOff") ? "office.room.vent.off.grandpajoe" : "office.room.vent.grandpajoe");
/** The thermostat, used: with the suits there it is the interview's lever; alone, the dial does nothing. */
async function thermostat(g) {
  if (alone(g)) return g.say("office.room.thermostat.use.grandpajoe");
  const h = heat(g);
  if (h < 77) return g.say("office.room.thermostat.72.grandpajoe", "office.room.thermostat.72.suits");
  if (h < 81) {
    await g.say("office.room.thermostat.77.grandpajoe", "office.room.thermostat.77.suits.1");
    await mop(g);
    return g.say("office.room.thermostat.77.suits.2", "office.room.thermostat.77.suits.3");
  }
  await g.say("office.room.thermostat.81.grandpajoe", ...SUSPEND);
  g.flag("office.alone", true);
  await suspend(g);
}
const thermoLook = byHeat("office.room.thermostat.72.grandpajoe", "office.room.thermostat.77.grandpajoe", "office.room.thermostat.81.grandpajoe");

// ---------- now and then ----------
// From above, the interview as Ranger hears it through the slats (the questionnaire repeats itself: that is the joke); in
// the room, once it is warm, Merle mopping. Off while the people's own lives are off (the tests' ?still).
const CHAT_VIEW = chatter(nowAndThen["office-room"], { first: [6, 9], every: [16, 26], when: (g) => !!g.peeking && !alone(g) });
const CHAT_ROOM = chatter([{ when: (g) => !alone(g) && heat(g) >= 77, say: ["office.room.merle.mop", "office.room.dale.tie"] }],
  { first: [24, 34], every: [50, 80], when: (g) => !g.peeking && who(g) === "grandpajoe" });

export default {
  id: "office-room",
  era: "nevada",
  name: "The Comfortable Room",
  building: BUILDING,
  music: (g) => (room.playing ? "rag-tin" : "office"),

  horizon: 295, full: 446, maxScale: 1.25,
  walk: [
    { name: "floor", area: FLOOR, away: { ranger: (g) => hopDown(g) } },
    { name: "seat", area: SEAT_AREA, scale: SEAT_SCALE, base: CHAIR_BASE,
      away: { ranger: (g) => toSeat(g), grandpajoe: "office.room.vent.use.grandpajoe" } },
  ],
  // Grandpa Joe's chair, Dale's, Merle's (their footprints), and the lamp's foot
  blocked: [[[315, 450], [358, 445], [374, 457], [328, 464]], [[412, 429], [446, 424], [466, 434], [431, 439]], [[439, 443], [476, 438], [501, 450], [462, 456]],
    [[488, 412], [490, 414], [485, 415], [477, 415], [470, 414], [468, 412], [473, 410], [481, 410]]],

  spawn: { default: AT_JOE, joe: JOE, vent: SEAT, chair: CHAIR, atchair: AT_CHAIR, atjoe: AT_JOE,
    dale: DALE, merle: MERLE, door: DOOR, opal: OPAL, intercom: [295, 438], thermostat: [260, 443] },
  facing: "E",
  // Grandpa Joe never walks while they question him (he does everything from his chair), nor while he stands on the spare chair
  still: (g, id) => id === "grandpajoe" && (!alone(g) || onChair(g)),
  exits: ["office-ducts"],
  stock: STOCK,
  announce: ANNOUNCE,
  get wordsAt() { return WORDS.at || VENT_WORDS; },
  talk: ventTalk,                                          // the two of them in the room together (Ranger dropped in)
  handDown,                                                // (office-ducts.js: a thing used on the grille is handed down here)
  // Ranger in the room hands Grandpa Joe something himself: the same as down through the slats (the schedule is read)
  async given(g, item, to) {
    if (to !== "grandpajoe") return;
    if (item === "pietin") await g.say("office.vent.down.pietin.1", "office.vent.down.pietin.ranger", "office.vent.down.pietin.joe");
    else if (item === "peanuts") await g.say("office.vent.down.peanuts");
    else if (item === "schedule") {
      await g.say("office.schedule.read.1", "office.schedule.read.2", "office.schedule.read.3", "office.schedule.read.4", "office.schedule.read.5",
        "office.schedule.read.6", "office.schedule.read.7", "office.schedule.read.ranger", "office.schedule.read.8", "office.schedule.read.9");
      g.flag("office.schedule", true);
    }
  },

  tick(g, dt) {
    keepHeat(g);
    const h = heat(g);
    if (h !== room.heat) { room.heat = h; suitsHot(g); }
    CHAT_VIEW.tick(g, dt);
    CHAT_ROOM.tick(g, dt);
  },

  picture: art + "back.png",
  planes: [
    { id: "vent", src: art + "vent.png", plane: "back", when: (g) => !eyes(g) },
    { id: "vent-eyes", src: art + "vent-eyes.png", plane: "back", when: eyes },
    { id: "thermostat-72", src: art + "thermostat-72.png", plane: "back", when: (g) => heat(g) < 73 },
    { id: "thermostat-77", src: art + "thermostat-77.png", plane: "back", when: (g) => heat(g) >= 73 && heat(g) < 80 },
    { id: "thermostat-81", src: art + "thermostat-81.png", plane: "back", when: (g) => heat(g) >= 80 },
    { id: "intercom", src: art + "intercom.png", plane: "back" },
    { id: "intercom-lit", src: art + "intercom-lit.png", plane: "back", when: () => room.lit },
    { id: "second", frames: Array.from({ length: 60 }, (_, n) => art + `second-${String(n).padStart(2, "0")}.png`), fps: 1, at: [184, 243], foot: [12, 22], plane: "back" },
    { id: "bubble", frames: [...[0, 1, 2, 3, 4, 5].map((n) => art + `bubble-${n}.png`), ...Array(24).fill(art + "bubble-none.png")], fps: 6, at: [566, 350], foot: [2, 24], plane: "back" },
    { id: "door", src: art + "door.png", base: [[104, 450], [266, 431]] },
    { id: "door-open", src: art + "door-open.png", base: [[104, 450], [266, 431]], when: () => false },
    { id: "doorframe", src: art + "doorframe.png", base: [[104, 450], [266, 431]] },
    { id: "chair-corner", src: art + "chair-corner.png", base: [[64, 469], [121, 462]], solid: [[71, 454], [126, 448], [122, 462], [62, 469]] },
    { id: "table", src: art + "table.png", base: 458, solid: [[345, 435], [409, 427], [467, 459], [391, 471]] },
    { id: "questionnaire", src: art + "questionnaire.png", base: 458, when: (g) => !alone(g) },
    { id: "plant", src: art + "plant.png", base: [[647, 484], [677, 482]], when: (g) => heat(g) < 81,
      solid: [[668, 472], [680, 479], [674, 484], [655, 485], [633, 480], [624, 473], [630, 468], [648, 468]] },
    { id: "plant-droop", src: art + "plant-droop.png", base: [[647, 484], [677, 482]], when: (g) => heat(g) >= 81,
      solid: [[668, 472], [680, 479], [674, 484], [655, 485], [633, 480], [624, 473], [630, 468], [648, 468]] },
    { id: "front", src: art + "front.png", plane: "front" },
  ],

  // Dale and Merle across the table, side-on (PEOPLE-17's -table kinds; -hot once it is warm: their life mops and loosens)
  actors: [
    { id: "suit1", kind: "suit1-table", at: DALE, face: "W", when: (g) => !alone(g), life: { fidget: [4, 9] } },
    { id: "suit2", kind: "suit2-table", at: MERLE, face: "W", when: (g) => !alone(g), life: { fidget: [4, 9] } },
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    // standing on the spare chair, he steps down to walk anywhere
    { id: "floor", name: "the floor", verb: "Step down to", poly: FLOOR, when: (g) => onChair(g) && who(g) === "grandpajoe", use: { grandpajoe: stepDown } },
    spot("mirror", "mirror", { poly: [[362, 266], [366, 266], [450, 268], [487, 269], [488, 350], [487, 351], [377, 357], [362, 357]] }, [438, 420], "N", {
      joeLook: "office.room.mirror.grandpajoe", rLook: rlook("office.room.mirror.ranger"),
      joeUse: low(suitsOr(["office.room.mirror.use.grandpajoe", "office.room.mirror.use.suits", "office.room.mirror.use.joe"], "office.room.mirror.use.grandpajoe"), [438, 420], "N") }),
    spot("poster", "poster", { rect: [312, 280, 45, 69] }, [346, 432], "N", {
      joeLook: "office.room.poster.grandpajoe", joeUse: low((g) => g.say("office.room.poster.use.grandpajoe"), [346, 432], "N"), rLook: rlook("office.room.poster.ranger") }),
    spot("sign", "sign", { rect: [234, 254, 72, 63] }, [280, 442], "N", {
      joeLook: (g) => g.say(heat(g) >= 77 ? "office.room.sign.hot.grandpajoe" : "office.room.sign.grandpajoe"), rLook: rlook("office.room.sign.ranger") }),
    spot("clock", "clock", { rect: [168, 217, 33, 30] }, [186, 458], "N", {
      joeLook: (g) => g.say(is(g, "office.schedule") ? "office.room.clock.late.grandpajoe" : "office.room.clock.grandpajoe"),
      joeUse: (g) => g.say("office.room.clock.use.grandpajoe"), rLook: rlook("office.room.clock.ranger") }),
    spot("door", "door", { poly: [[132, 252], [162, 252], [194, 253], [226, 254], [232, 255], [231, 437], [134, 448], [133, 448]] }, DOOR, "N", {
      joeLook: "office.room.door.grandpajoe", rLook: rlook("office.room.door.ranger"),
      joeUse: low(suitsOr(["office.room.door.use.suits", "office.room.door.use.joe"], "office.room.door.use.grandpajoe"), DOOR, "N") }),
    spot("thermostat", "thermostat", { rect: [237, 317, 33, 26] }, [260, 443], "N", {
      joeLook: thermoLook, joeUse: low(thermostat, [260, 443], "N"), rLook: rlook("office.room.thermostat.ranger"),
      rUse: (g) => g.say("office.room.thermostat.use.ranger", "office.room.thermostat.use.ranger.joe") }),
    spot("intercom", "intercom", { rect: [273, 318, 28, 38] }, [295, 438], "N", {
      joeLook: "office.room.intercom.grandpajoe", joeUse: low(intercom, [295, 438], "N"), rLook: rlook("office.room.intercom.ranger"), rUse: rangerIntercom,
      more: { verb: "Press" } }),
    spot("cooler", "water cooler", { poly: [[541, 351], [553, 318], [557, 315], [569, 314], [578, 318], [590, 353], [589, 445], [568, 449], [564, 449], [543, 441]] }, [556, 454], "E", {
      joeLook: (g) => g.say(heat(g) >= 77 ? "office.room.cooler.hot.grandpajoe" : "office.room.cooler.grandpajoe"), rLook: rlook("office.room.cooler.ranger"),
      joeUse: low(suitsOr(["office.room.cooler.use.grandpajoe", "office.room.cooler.use.suits"], "office.room.cooler.use.grandpajoe"), [556, 454], "E"),
      rUse: async (g) => { const r = ranger(g); if (r) { await r.sit(true); await r.play(g.clock, "wash", { ms: 1600 }); } await g.say("office.room.cooler.use.ranger", "office.room.cooler.use.ranger.joe"); if (r) await r.sit(false); } }),
    spot("cones", "paper cones", { rect: [567, 335, 12, 57] }, [556, 454], "E", {
      joeLook: "office.room.cones.grandpajoe", rLook: rlook("office.room.cones.ranger") }),
    spot("plant", "plastic plant", { poly: [[619, 316], [627, 309], [646, 303], [663, 306], [676, 313], [684, 324], [677, 447], [671, 480], [646, 482], [632, 475], [626, 441], [613, 331]] }, [590, 470], "E", {
      joeLook: (g) => g.say(heat(g) >= 81 ? "office.room.plant.droop.grandpajoe" : "office.room.plant.grandpajoe"), rLook: rlook("office.room.plant.ranger"),
      joeUse: low((g) => g.say(heat(g) >= 81 ? "office.room.plant.droop.use.grandpajoe" : "office.room.plant.use.grandpajoe"), [590, 470], "E") }),
    // the chairs across the table, once Dale and Merle have gone from them
    spot("chair-dale", "Dale's chair", { poly: [[414, 415], [415, 401], [448, 356], [452, 356], [466, 359], [468, 362], [464, 434], [432, 439], [431, 439], [414, 430]] }, [449, 427], "W", {
      joeLook: "office.room.chairs.grandpajoe", rLook: rlook("office.room.chairs.ranger"), when: alone }),
    spot("chair-merle", "Merle's chair", { poly: [[442, 402], [478, 363], [483, 363], [489, 364], [502, 367], [502, 375], [497, 450], [464, 456], [463, 456], [442, 445]] }, [521, 458], "W", {
      joeLook: "office.room.chairs.grandpajoe", rLook: rlook("office.room.chairs.ranger"), when: alone }),
    spot("chair-joe", "his chair", { poly: [[313, 369], [316, 369], [326, 374], [371, 411], [371, 458], [331, 464], [330, 464], [318, 452], [313, 372]] }, [361, 469], "N", {
      joeLook: "office.room.chair.grandpajoe", rLook: rlook("office.room.chairs.ranger"),
      joeUse: (g) => (alone(g) && heat(g) >= 81 ? g.say("office.room.chair.use.grandpajoe") : g.say(g.fallback("nope"))) }),
    spot("table", "table", { poly: [[346, 370], [370, 368], [382, 368], [423, 370], [461, 381], [466, 384], [466, 388], [461, 458], [460, 459], [397, 469], [393, 469], [350, 436]] }, [361, 475], "N", {
      joeLook: (g) => g.say(alone(g) ? "office.room.table.alone.grandpajoe" : "office.room.table.grandpajoe"), rLook: rlook("office.room.table.ranger"),
      joeUse: (g) => g.say("office.room.table.use.grandpajoe"), peekWith: DOWN }),
    spot("questionnaire", "questionnaire", { rect: [379, 361, 46, 19] }, [351, 449], "N", {
      joeLook: "office.room.questionnaire.grandpajoe", joeUse: (g) => g.say("office.room.questionnaire.use"), rLook: rlook("office.room.questionnaire.ranger", null),
      when: (g) => !alone(g) }),
    // the spare chair in the corner, under the vent: his way up to it; Ranger's way down from it and back up
    spot("chair-corner", "spare chair", { poly: [[70, 370], [96, 368], [112, 368], [117, 372], [118, 375], [122, 412], [122, 460], [121, 461], [72, 469], [71, 469]] }, null, null, {
      joeLook: "office.room.corner.grandpajoe", rLook: rlook("office.room.corner.ranger"), rUse: upAndOut, drop: true, peekWith: DOWN,
      joeUse: cornerUse, more: { verb: "Climb on" } }),
    spot("vent", "vent", { poly: [[68, 192], [139, 197], [144, 198], [146, 209], [138, 213], [78, 209], [68, 204], [57, 193]] }, null, null, {
      joeLook: ventLook, joeUse: ventUse, rLook: rlook("office.room.vent.ranger"), rUse: upAndOut, above: false, peekWith: DOWN,
      useWith: Object.fromEntries(["receipt", "peanuts", "sectormap", "banjo-broken", "banjo-pie", "pietin", "schedule"].map((item) => [item, (g) => ventWith(g, item)])) }),
    // Dale and Merle, across the table (a word with either is the interview)
    spot("suit1", "Dale", { rect: [421, 318, 34, 112] }, null, null, {
      joeLook: (g) => g.say(heat(g) >= 77 ? "office.room.dale.hot.grandpajoe" : "office.room.dale.grandpajoe"), joeUse: interview, rLook: rlook("office.room.dale.ranger", null),
      useWith: { receipt: "office.room.suits.with.receipt", sectormap: "office.room.suits.with.sectormap.grandpajoe" }, when: (g) => !alone(g), more: { verb: "Talk to" } }),
    spot("suit2", "Merle", { rect: [451, 322, 40, 122] }, null, null, {
      joeLook: (g) => g.say(heat(g) >= 77 ? "office.room.merle.hot.grandpajoe" : "office.room.merle.grandpajoe"), joeUse: interview, rLook: rlook("office.room.merle.ranger", null),
      useWith: { receipt: "office.room.suits.with.receipt", sectormap: "office.room.suits.with.sectormap.grandpajoe" }, when: (g) => !alone(g), more: { verb: "Talk to" } }),
    // Grandpa Joe, from above (Ranger at the grille): the box round his figure
    { id: "joe-above", name: "Grandpa Joe", mate: "grandpajoe", when: (g) => !!g.peeking,
      peek: { look: { ranger: "office.room.joe.ranger" }, use: { ranger: fromAbove }, useWith: DOWN, verb: "Call to" } },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and as the room is built to be looked into.
  setup(g) {
    keepHeat(g);
    room.heat = heat(g); room.playing = false; room.lit = false;
    WORDS.at = null;
    CHAT_VIEW.reset(); CHAT_ROOM.reset();
    placeJoe(g);
    suitsHot(g);
    shades(g);
  },

  // What happens as somebody comes in: Ranger dropping onto the chair's seat (Joe sees him); Grandpa Joe, with Opal on her
  // way with his banjo (the receipt's journey: office-property.js), the key in the door. Nothing else starts by itself.
  async enter(g, from) {
    if (who(g) === "ranger" && from === "office-ducts" && joe(g)) { await g.say("office.room.drop.grandpajoe"); return; }
    if (who(g) === "grandpajoe" && is(g, "office.receiptGiven") && !is(g, "office.banjoBack")) await opalVisit(g);
  },

  // Ranger looks down through the grille (office-ducts.js): the first time, there is Joe; and the first time after the
  // suits have gone, Joe hears him, and gets up on the chair.
  async viewed(g) {
    if (!is(g, "office.sawRoom")) { g.flag("office.sawRoom", true); await g.say("office.duct.room.first.ranger"); }
    if (alone(g) && !onChair(g) && !is(g, "office.called") && joe(g)) { g.flag("office.called", true); await callJoe(g); }
  },
};
