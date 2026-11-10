// SCENES-20B (round twenty): what the three scenes of the hills north of Osaka share (edo-cedars.js, edo-storehouse.js,
// edo-chapel.js), and the card "Three days later" (cutscenes/edo-walk.js). Not a scene (it is in no list of scenes): a
// module they import, as the Office's rooms import office-common.js. The act's own shared pieces are MERGE-20's
// edo-common.js: the stock replies (STOCK_DRESSED: in the hills the borrowed clothes are always on) and LEG_START.hills.
// The design is briefs/out/edo-design.md, #25 to #27; the lines are WRITE-20B's (lines/edo-b.en.js, talk/edo-b.js).
//
//   the times     dusk (#25, until they go down the ladder: edo.hidden), the evening (#26, until edo.trusted), the night
//                 (the trees of the three of them, until O-Rin's warning: edo.watch), the morning (#27: the constable on
//                 the path), and after he has gone (edo.constableGone: the sun on the ladder, the mirror, the walk)
//   who goes      the three of them together (each scene's `party`), but in the morning: then the two girls go together
//                 and Mom goes alone, since she must stay below and they must answer the door
//   the hats      on outdoors (`edo`), hanging on the back indoors (`edo-hatback`): PEOPLE-20's outfits (g.dress)
//   #27           the three things (the sacks over the mat, the pink light off, Mom below: the facts acts/edo.js stages its
//                 hint by), what is still wrong (Jinsuke's NOT_READY), and the constable's climb up the path: a step for
//                 each thing done, and the knock when all three are (a count of beats, not a timer)
//   the path      a look at the cedar path for a moment while the lead stays where he is (the constable climbing, and
//                 going away down it with the egg), the lead's own scene built again after it
//   pockets       a thing into (or out of) the pockets of a lead who is not the one being played
//   the visit     the constable at the storehouse's door (talk/edo-b.js isukeTree, with the hooks that stage it), his
//                 steps up the path as the room is made ready, his knock, and after he has gone, down to the mirror

import { is } from "./edo-common.js";
import { isukeTree, NOT_READY } from "../talk/edo-b.js";
import { scaleAt } from "../../engine/walk.js";
import { keyScene } from "../../art/look.js";
import { forget } from "../../engine/cast.js";

export const THREE = ["mom", "bigsis", "lilsis"];
export const GIRLS = ["bigsis", "lilsis"];
export const who = (g) => g.store.data.active;
/** Has this line been said yet? (The engine counts every line it says.) */
export const heard = (g, id) => !!g.store.data.seenLines[id];
/** A look or a use with a line of each of the three's own (`<id>.mom`, `<id>.bigsis`, `<id>.lilsis`). */
export const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
/** The one being played says her own line of that id (`<id>.<who>`). */
export const own = (id) => (g) => g.say(`${id}.${who(g)}`);

// ---------- the times ----------
export const dusk = (g) => !is(g, "edo.hidden");
export const evening = (g) => is(g, "edo.hidden") && !is(g, "edo.trusted");
export const night = (g) => is(g, "edo.trusted") && !is(g, "edo.watch");
export const morning = (g) => is(g, "edo.watch") && !is(g, "edo.constableGone");
export const sunUp = (g) => is(g, "edo.constableGone");
/** It rains on the hills from the evening they come until the constable has gone down the path with the egg. */
export const raining = (g) => !is(g, "edo.constableGone");

// ---------- who goes where with whom ----------
/** The party of a scene of the hills: the three of them, but in the morning the girls (Mom stays below, and goes alone). */
export const partyOf = (g) => (morning(g) ? GIRLS : THREE);
/** The scene a lead is in (the save's, or the stage's), or null. */
export const sceneOf = (g, id) => { const w = g.where(id); return w ? w.scene : null; };
/** #27: Mom is below with Grandmother Sei (the fact the hint and the constable's knock read), kept up to date as she goes
    up and down: set while the constable is on his way, left as it was after. */
export function keepBelow(g) {
  if (!morning(g)) return;
  const below = sceneOf(g, "mom") === "edo-chapel";
  if (!!g.flag("edo.momBelow") !== below) g.flag("edo.momBelow", below);
}

// ---------- the hats: on outdoors, on the back indoors ----------
export function hats(g, on) {
  for (const id of THREE) {
    const now = g.dressOf(id), want = on ? "edo" : "edo-hatback";
    if ((now === "edo" || now === "edo-hatback") && now !== want) g.dress(id, want);
  }
}

// ---------- #27: the three things, and what Jinsuke says while one is not done ----------
export const ready = (g) => is(g, "edo.sacksHid") && is(g, "edo.pinkOff") && is(g, "edo.momBelow");
/** What is still wrong, in Jinsuke's order (talk/edo-b.js NOT_READY): the mat and the sacks, the pink, Mom; null: nothing. */
export const wrong = (g) => (!is(g, "edo.sacksHid") ? "mat" : !is(g, "edo.pinkOff") ? "pink" : !is(g, "edo.momBelow") ? "mom" : null);
/** How many of the two things done up here are done (the sacks, the pink light): the constable climbs a step for each. */
export const done = (g) => (is(g, "edo.sacksHid") ? 1 : 0) + (is(g, "edo.pinkOff") ? 1 : 0);

// ---------- the constable's way up the cedar path (the painter's isukeWay, bottom first; the last point is the door; PAINT-23: measured
// again from the path's new picture, art/scenes/edo-cedars/layout.json) ----------
export const ISUKE_WAY = [[232, 598], [252, 580], [282, 561], [330, 544], [386, 529], [420, 512], [412, 499]];
/** Where on his way he is by the story: at the foot when O-Rin sees him, a step up for each thing done, at the door once
    he has knocked. */
export const isukeAt = (g) => (is(g, "edo.isukeAtDoor") ? 6 : [1, 3, 4][done(g)]);

// ---------- how the last way in was taken (not saved: a script sets it just before its goto, the scene gone to reads it) ----------
/** `by`: "window" (Little Sister through the storehouse's back window, onto the sacks), "pile" (through the trapdoor
    with the sacks shifted off it and put back, #27), "pink" / "pinkPile" (Little Sister down to her flashlight, from the
    pink floorboards up there: over the open trapdoor, or through the sacks), "sun" (down to the mirror, after the
    constable has gone), or null. */
export const passing = { by: null };

// ---------- #27: her flashlight, left on below on the mats (edo-chapel.js), its light up between the boards ----------
/** On, and shining up between the floorboards: left on the mats for O-Rin when they slept (edo.lightLeft), until Little Sister
    turns it off (edo.pinkOff), and never once he has gone. */
export const pinkOn = (g) => is(g, "edo.lightLeft") && !is(g, "edo.pinkOff") && !is(g, "edo.constableGone");

// ---------- shapes ----------
/** Is the point inside the polygon? */
export function inPoly(poly, x, y) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[j];
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}
/** Anyone on the stage standing where something has just been put down (a heap of sacks) steps off it, to their place in
    `places` (by id), or a step in front of it. */
export function clearOf(g, poly, places = {}) {
  for (const f of g.view.cast.items.values()) {
    if (!f || !f.walkPath || !Number.isFinite(f.x) || !inPoly(poly, f.x, f.y)) continue;
    const to = places[f.id] || [f.x, Math.max(...poly.map((p) => p[1])) + 14];
    f.place(to[0], to[1], g.sizeAt(to[0], to[1]));
    g.rememberPlace(f.id);
  }
}

// ---------- a thing into or out of another lead's pockets ----------
export function giveTo(g, to, item) {
  if (who(g) === to) return g.give(item);
  const inv = g.store.data.inventory;
  inv[to] = inv[to] || [];
  if (inv[to].includes(item)) return;
  inv[to].push(item);
  g.sfx("pickup");
  if (!g.clock.skipping) g.ui.toast(`${g.cast[to].name} has ${g.the(item)}`);
  g.store.emit();
}
export function takeFrom(g, from, item) {
  const inv = g.store.data.inventory[from] || [], i = inv.indexOf(item);
  if (i < 0) return false;
  if (who(g) === from) { g.take(item); return true; }
  inv.splice(i, 1);
  g.store.emit();
  return true;
}
export const carries = (g, id, item) => ((g.store.data.inventory || {})[id] || []).includes(item);

// ---------- a look at the cedar path, while the lead stays where she is ----------
/**
 * The cedar path for a moment (the constable climbing it, or going away down it): its painting and cut-outs as the facts
 * have them, its moving things (the rain, the drips, the mist), the constable put on it where `isuke` says ({ at, face,
 * kind, hold }), `play(g, isuke)` played, and then the lead's own scene built again where she stood (its `setup` runs
 * again; not its `enter`: nobody has gone anywhere). As the Office's cutAway (office-common.js), with the path's moving
 * things and its paints (keyed: the path and the storehouse share edo-rain; the room underground is edo-lamp).
 */
export async function toPath(g, play, isuke = null) {
  const d = g.store.data, here = g.scene, place = d.where[d.active];
  const there = await g.getScene("edo-cedars");
  g.rememberPlace();
  await g.fade(1, 260);
  g.dialogue.clear();
  g.view.clear();
  if (keyScene(there.id, there.era)) forget();
  await g.view.show(there, g);
  g.effects.drop(g.scene);
  for (const spec of (typeof there.fx === "function" ? there.fx(g) : there.fx) || []) g.effects.add(spec);
  let man = null;
  if (isuke) {
    const [x, y] = isuke.at;
    man = g.view.cast.addFigure("isuke", isuke.kind || "isuke", x, y, scaleAt(there, y)).face(isuke.face || "N");
    if (isuke.hold) man.hold(true, isuke.hold);
  }
  await g.view.cast.load();
  await g.fade(0, 260);
  try { await play(g, man, there); }
  finally {
    await g.fade(1, 260);
    if (keyScene(here.id, here.era)) forget();
    await g.enterScene(here, place && place.x != null ? [place.x, place.y] : null);
    await g.fade(0, 300);
  }
}
/** A person walks along points of the path, at the path's own sizes (for a script of toPath). */
export const walkOn = (g, f, there, points) => (f ? f.walkPath(g.clock, points, (y) => scaleAt(there, y)) : Promise.resolve());

// ---------- the other two, where they stand ----------
/** Each companion's own area (the engine's box round her figure: no shape of its own), listed FIRST among a scene's areas, so
    that the things of these small rooms lie over her: a companion standing in front of the altar, the mirror's stand or the
    door's bar does not take its clicks (NEVADA-12SC's `mate` areas). Not the one being played. */
export const MATES = [["mom", "Mom"], ["bigsis", "Big Sister"], ["lilsis", "Little Sister"]].map(([id, name]) =>
  ({ id: `mate-${id}`, mate: id, name, verb: "Talk to", when: (g) => who(g) !== id }));

// ---------- what the three say to each other in the hills (the scenes' `talk`) ----------
// WRITE-20B wrote none for the hills: these are WRITE-20A's companion talks of the act that hold anywhere in Japan
// (lines/edo-a.en.js), with the one about telling the truth to a man who asks kept for the morning the constable comes.
export const TALK = {
  mom: {
    bigsis: [
      { when: (g) => morning(g), say: ["edo.talk.mom.bigsis.lie.a", "edo.talk.mom.bigsis.lie.b", "edo.talk.mom.bigsis.lie.c"] },
      ["edo.talk.mom.bigsis.read.a", "edo.talk.mom.bigsis.read.b", "edo.talk.mom.bigsis.read.c"],
    ],
    lilsis: [["edo.talk.mom.lilsis.boots.a", "edo.talk.mom.lilsis.boots.b"]],
  },
  bigsis: {
    mom: [["edo.talk.bigsis.mom.tall.a", "edo.talk.bigsis.mom.tall.b"]],
    lilsis: [["edo.talk.bigsis.lilsis.hens.a", "edo.talk.bigsis.lilsis.hens.b"]],
  },
  lilsis: {
    mom: [["edo.talk.lilsis.mom.son.a", "edo.talk.lilsis.mom.son.b"], ["edo.talk.lilsis.mom.grace.a", "edo.talk.lilsis.mom.grace.b"]],
    bigsis: [["edo.talk.lilsis.bigsis.word.a", "edo.talk.lilsis.bigsis.word.b", "edo.talk.lilsis.bigsis.word.c"]],
  },
};

// ---------- #27: the constable's visit (talk/edo-b.js isukeTree), staged in the storehouse ----------
// PAINT-20C's storehouse: marks.isuke (where he stands and talks), the door's opening (where he comes in from the rain),
// and, set by eye against the picture with the people in it, where Jinsuke keeps the door before he comes and where he
// stands while he is in (between the guest and the girls), O-Rin's place by the lantern, and the place in front of him
// where Little Sister holds out the egg.
export const STORE = { door: [526, 464], doorway: [556, 456], isuke: [505, 471], jinsuke: [490, 462], guard: [452, 474], orin: [330, 470], egg: [476, 484],
  bigsis: [392, 488], lilsis: [424, 478] };
const storeScale = (g, y) => (g.scene ? scaleAt(g.scene, y) : 1);

/** Jinsuke opens the door (the bar is up already: he lifts nothing, he swings it in), and the constable's man comes in out
    of the rain to his place, dripping; Jinsuke steps between him and the girls, who turn to him. */
async function letIn(g) {
  const j = g.actor("jinsuke");
  if (j) { await g.walkTo(538, 466, "jinsuke"); j.face("E"); await j.play(g.clock, "reach"); }
  g.sfx("shutter");
  g.flag("edo.isukeIn", true);                                                 // (the door open: door-open; he is in)
  g.view.cast.remove("isuke");
  const man = g.view.cast.addFigure("isuke", "isuke", STORE.doorway[0], STORE.doorway[1], storeScale(g, STORE.doorway[1])).face("W");
  man.fade(0);
  await g.view.cast.load();
  await Promise.all([man.walkPath(g.clock, [STORE.isuke], (y) => storeScale(g, y)), g.tween(450, (k) => man.fade(k))]);
  man.face("W");
  // Jinsuke between him and the girls; the girls a step back, side by side, where he can see them both
  await Promise.all([j ? g.walkTo(STORE.guard[0], STORE.guard[1], "jinsuke") : null,
    ...GIRLS.map((id) => (g.actor(id) ? g.walkTo(STORE[id][0], STORE[id][1], id) : null))]);
  if (j) j.face("E");
  for (const id of GIRLS) { const a = g.actor(id); if (a) a.look(man.x, man.y); }
}
/** Little Sister holds out the egg in both hands, carefully, and he takes it in both of his. */
async function giveEgg(g) {
  const lil = g.actor("lilsis"), man = g.actor("isuke");
  if (lil && who(g) === "lilsis") await g.walkTo(STORE.egg[0], STORE.egg[1]);
  if (lil && man) lil.look(man.x, man.y);
  if (lil) lil.hold(true, "egg");
  await g.wait(1000);
  if (man) man.hold(true, "egg");
  if (lil) lil.hold(false);
  takeFrom(g, "lilsis", "egg");
  await g.wait(300);
}
/** No egg (it is in nobody's pockets): the rest of Kihei's sushi, in its box, held out the same way. */
async function giveSushi(g) {
  const lil = g.actor("lilsis"), man = g.actor("isuke");
  if (lil && who(g) === "lilsis") await g.walkTo(STORE.egg[0], STORE.egg[1]);
  if (lil && man) lil.look(man.x, man.y);
  if (who(g) === "lilsis") await g.reach();
  takeFrom(g, "lilsis", "sushibox");
  await g.wait(300);
}
/** He goes: out of the door with the egg in both hands, the door shut behind him; and down the cedar path in the rain. */
async function goes(g) {
  const man = g.actor("isuke"), egg = !!g.flag("edo.eggGiven");
  if (man) {
    await Promise.all([man.walkPath(g.clock, [STORE.doorway], (y) => storeScale(g, y)), g.wait(500).then(() => g.tween(450, (k) => man.fade(1 - k)))]);
    g.view.cast.remove("isuke");
  }
  g.flag("edo.isukeIn", false);
  g.sfx("shutter");
  await g.wait(400);
  await toPath(g, async (g, him, there) => {
    await g.wait(300);
    await walkOn(g, him, there, [ISUKE_WAY[4], ISUKE_WAY[2]]);
    await g.wait(500);
  }, { at: ISUKE_WAY[6], face: "S", hold: egg ? "egg" : null });
}
const RAW = isukeTree({ letIn, giveEgg, giveSushi, goes });
/** The constable's talk: the tree as WRITE-20B wrote it, but started where his visit has got to (a talk the girls leave
    while he stands there goes on from his questions, not from his knock): Mom, below, never answers him (momNo). */
export const ISUKE = { ...RAW, start: (g) => (who(g) === "mom" ? "momNo" : is(g, "edo.isukeIn") ? "asked" : "door") };
const BIG = ["sea", "east", "mom", "tall"];
/** A word with the constable (or the door, while he is at it): Little Sister sizes him up first; Big Sister, her answers used
    up, has only her opinion of how it is going. When he has gone, down to the mirror. */
export async function talkToIsuke(g) {
  const me = who(g);
  if (is(g, "edo.isukeIn") && me === "lilsis" && !heard(g, "edo.store.isuke.use.lilsis")) await g.say("edo.store.isuke.use.lilsis");
  if (is(g, "edo.isukeIn") && me === "bigsis") {
    const left = BIG.some((id) => !g.asked(`isuke/${id}`)), some = BIG.some((id) => g.asked(`isuke/${id}`));
    if (!left || (some && !heard(g, "edo.store.isuke.use.bigsis"))) await g.say("edo.store.isuke.use.bigsis");
    if (!left) return;
  }
  await g.talk(ISUKE);
  if (is(g, "edo.constableGone") && !is(g, "edo.mirror")) await afterVisit(g);
}
/** What Jinsuke says while the room is not ready (and while he is in, what each of them says of Jinsuke). */
export const notReady = (g) => g.say(NOT_READY[wrong(g) || "mat"]);

/** A step done up here (the sacks; the pink light): the constable climbs a step nearer (a look out at the path); or, all
    three things done, he is at the door. `stepped`: the step was one of the two (Mom going below is not a climb). */
export async function afterStep(g, stepped = true) {
  keepBelow(g);
  if (!morning(g) || is(g, "edo.isukeAtDoor")) return;
  if (ready(g)) return knockAtDoor(g);
  if (!stepped) return;
  const n = done(g), from = ISUKE_WAY[[1, 3, 4][Math.max(0, n - 1)]], to = ISUKE_WAY[[1, 3, 4][n]];
  await toPath(g, async (g, man, there) => {
    await g.wait(300);
    await walkOn(g, man, there, [to]);
    if (man) { man.face("N"); await man.fidget("yawn"); }
    await g.wait(400);
  }, { at: from, face: "N" });
}
/** All three done: he climbs the last steps and knocks. A girl up in the storehouse answers at once (with Jinsuke: the
    talk); Mom, below, says why she must not (the talk's momNo); a girl below hears it, and must go up. */
export async function knockAtDoor(g) {
  if (is(g, "edo.isukeAtDoor")) return;
  await toPath(g, async (g, man, there) => {
    await walkOn(g, man, there, [ISUKE_WAY[5], ISUKE_WAY[6]]);
    if (man) man.face("NE");                                                    // (PAINT-23: the door is up to his right in the path's new picture; it was straight ahead, "N")
    await g.wait(300);
    g.sfx("knock");
    await g.wait(1100);
  }, { at: ISUKE_WAY[4], face: "N" });
  g.flag("edo.isukeAtDoor", true);
  g.sfx("knock");
  await g.wait(700);
  const me = who(g);
  if (me === "mom" || sceneOf(g, me) === "edo-storehouse") await talkToIsuke(g);
}
/** He has gone: the sun is on the ladder. Jinsuke and O-Rin go down first; the sacks come off the trapdoor; everyone goes
    down to the room, where the grandmother has something for Mom (edo-chapel.js: the mirror, and the walk to Himeji). */
export async function afterVisit(g) {
  await g.fade(1, 500);
  for (const id of ["jinsuke", "orin", "isuke"]) g.view.cast.remove(id);
  passing.by = "sun";
  await g.goto("edo-chapel", { spawn: "ladder", via: "cut", card: false });
}
