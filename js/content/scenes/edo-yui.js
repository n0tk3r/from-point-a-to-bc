// What Act Six's first leg shares (SCENES-20A: new in round twenty): Yui on Suruga Bay, its two scenes (edo-village.js,
// edo-fishshop.js) and its two cut-scenes (cutscenes/edo-arrive.js, cutscenes/edo-sail.js). Not a scene (it is in no list of
// scenes): a module they import, as the Office's scenes import office-common.js. (What the whole act shares is MERGE-20's
// edo-common.js: the stock replies, LEG_START.)
//
//   the three             Mom, Big Sister and Little Sister, a party in both scenes; who is being played
//   their clothes         O-Tami's travel kimonos once edo.clothes (#22): the hat on outdoors (`edo`), on the back indoors
//                         (`edo-hatback`); `dressFor(g, place)` puts the right one on each, as a scene is built
//   two more pages        made here at run time from PEOPLE-20's own (js/art/people.js is not changed, and its test still
//                         counts its 39 kinds): Mom in her own clothes with O-Tami's baby in her arms (`mom-baby`: the lullaby
//                         comes before the kimonos, and PEOPLE-20's `edo-baby` is the kimono), and each of the three sitting
//                         on the step of the raised room (`<outfit>-step`, 45 cm: PAINT-20B's seats) for Kihei's table (#23)
//   #21                   the sum: when the red, the coins and the blue are all in, Big Sister works the year out aloud, and
//                         the act's card carries her words (`whenSolved`)
//   the card              "Act Six: By Your Grace" (the arrival), and after #21 with Big Sister's line under it
//   talk                  what the three say to each other in Yui (WRITE-20A's edo.talk.*), for both scenes' `talk`
//   people                swap (one of the people of 1830 as another state of themselves, under the same id), walking and
//                         turning helpers

import { people, momEdoBaby } from "../../art/people.js";
import { ramp, add, mix, standOffset } from "../../art/rig.js";
import { scaleAt } from "../../engine/walk.js";
import { is } from "./edo-common.js";

export const THREE = ["mom", "bigsis", "lilsis"];
export const who = (g) => g.store.data.active;
export { is };
/** Has this line been said yet? (The engine counts every line it says.) */
export const heard = (g, id) => !!g.store.data.seenLines[id];
/** One line for each of the three: `<id>.mom`, `<id>.bigsis`, `<id>.lilsis`. */
export const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
/** The line of the one being played: `<id>.<who>`. */
export const mine = (g, id) => `${id}.${who(g)}`;
/** A thing's look and use, for each of the three: `<base>.<thing>.<who>` and `<base>.<thing>.use.<who>`. */
export const lookUse = (base, thing) => ({ look: each(`${base}.${thing}`), use: each(`${base}.${thing}.use`) });
/** A line's words, for a card (and the line counted as seen, as a card's lines are). */
export function cardWords(g, id, or = "") {
  if (!g.lines[id]) return or;
  if (!g.clock.skipping) g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;
  return g.lines[id][1];
}

// ---------- their clothes ----------
/** The three in O-Tami's clothes, as the place wants them: outdoors the hat on (`edo`), indoors on the back (`edo-hatback`).
    Before #22 they are in their own clothes (and the yellow boots stay, in every outfit). A held moment's own outfit
    (`baby`, a seated page) is left alone: the scene that put it on takes it off. */
export function dressFor(g, place) {
  if (!is(g, "edo.clothes")) return;
  const want = place === "indoors" ? "edo-hatback" : "edo";
  for (const id of THREE) {
    const now = g.dressOf(id);
    if (now !== want && (now === null || now === "edo" || now === "edo-hatback")) g.dress(id, want);
  }
}

// ---------- two more pages: Mom with the baby in her own clothes; the three sitting on the step ----------
const SWADDLE = ramp("#f8e8c8", "#e8d0a4", "#b89c70", "#7c6646");             // the baby's wrap (PEOPLE-20's own tones)
const BABY_SKIN = ramp("#f8dcbe", "#e8bc98", "#bc8662", "#80553c");
const BABY_HAIR = ramp("#4c4854", "#2c2932", "#19171e", "#0b0a0e");
/** A baby, wrapped, lying across both forearms (PEOPLE-20's `baby`, js/art/people.js, drawn the same way). */
function babyInArms(c) {
  const { J, ball, limb, parts, tw } = c, l = mix(J.L.elbow, J.L.wrist, 0.45), r = mix(J.R.elbow, J.R.wrist, 0.55);
  limb(add(l, [0, 0.030, 0.006]), add(r, [0, 0.034, 0.006]), 0.036, 0.028, SWADDLE, { part: parts.HELD, squareStart: true });
  ball(add(l, [0, 0.060, 0.016]), [0.034, 0.032, 0.034], BABY_SKIN, { part: parts.HELD }, tw);
  ball(add(l, [0, 0.072, 0.010]), [0.035, 0.024, 0.035], BABY_HAIR, { part: parts.HELD, fn: (ux, uy) => (uy > -0.25 ? null : undefined) }, tw);
}
/** The step of the raised room in Kihei's shop: 45 cm (PAINT-20B's seats: 0.257 of the rig's 175 cm). */
export const STEP_SEAT = 0.257;
/** The outfits made here (g.dress names): Mom's `baby`, and each lead sitting on the step in whatever she wore. */
export const OWN_OUTFITS = { mom: ["baby", "step", "edo-step", "edo-hatback-step"], bigsis: ["step", "edo-step", "edo-hatback-step"], lilsis: ["step", "edo-step", "edo-hatback-step"] };
function addPages() {
  const mom = people.mom;
  if (mom && !people["mom-baby"]) {
    people["mom-baby"] = { ...mom, name: "Mom, with O-Tami's baby in her arms", outfit: "baby", wears: "mom", hold: momEdoBaby.hold, rest: undefined,
      gestures: [0, 0, 20, 0], fidgets: { only: true, stand: ["rockbaby"] }, span: 1.25,
      extras(c) { mom.extras({ ...c, pose: { ...c.pose, bare: "bag" } }); babyInArms(c); } };      // (her handbag: set down, as in her Edo clothes)
  }
  for (const id of THREE) for (const now of [null, "edo", "edo-hatback"]) {
    const kind = `${id}-${now ? `${now}-step` : "step"}`, base = people[now ? `${id}-${now}` : id];
    if (base && !people[kind]) people[kind] = { ...base, name: `${base.name}, sitting on the step`, outfit: now ? `${now}-step` : "step", seated: "chair",
      sit: { seat: STEP_SEAT, lean: 0.06, knees: 0.10, feet: 0.06 }, shadow: 0.22, span: 1.25, riseMs: id === "lilsis" ? 700 : 950 };
  }
}
addPages();
/** The outfit a lead wears sitting on the step, from whatever she wears now (g.dress names: `step`, `edo-step`, `edo-hatback-step`). */
export function stepOutfit(g, id) {
  const now = g.dressOf(id);
  return now ? `${now.replace(/-step$/, "")}-step` : "step";
}
/** A moment's own outfit (the baby in Mom's arms; sitting on the step) that a save caught: back to what she wore before it. */
export function undoMoment(g) {
  for (const id of THREE) {
    const now = g.dressOf(id);
    if (now === "baby") g.dress(id, null);
    else if (now && now.endsWith("step")) g.dress(id, now === "step" ? null : now.replace(/-step$/, ""));
  }
}
/** Sit a lead down on the step at `seat` (the ground under her hips), facing `face`: she walks to where she will stand up
    from, and sits back onto the step. */
export async function sitOnStep(g, id, seat, face = "W") {
  const f = g.actor(id);
  if (!f) return;
  const name = stepOutfit(g, id), spec = people[`${g.cast[id].sprite}-${name}`], yaw = { W: 270, E: 90, S: 0, N: 180 }[face] ?? 270;
  const size = Math.max(10, Math.round((160 * spec.height * scaleAt(g.scene, seat[1])) / 2) * 2), [dx, dy] = standOffset(spec, yaw, size);
  await g.walkTo(seat[0] + dx, seat[1] + dy, id);
  f.face(face);
  f.place(seat[0], seat[1], scaleAt(g.scene, seat[1]));
  g.dress(id, name);
  f.face(face);
  f.sit(false, true);                                                           // (standing where she walked to: then down onto the step)
  await f.sit(true);
}
/** Up off the step, and in her own outfit again (where she stood up). */
export async function standFromStep(g, id) {
  const f = g.actor(id);
  if (!f || !(g.dressOf(id) || "").endsWith("step")) return;
  await f.sit(false);
  const [x, y] = [f.x, f.y], yaw = f.yaw;
  const was = g.dressOf(id) === "step" ? null : g.dressOf(id).replace(/-step$/, "");
  g.dress(id, was);
  f.place(x, y, scaleAt(g.scene, y));
  f.face(yaw);
  g.rememberPlace(id);
}

// ---------- the people of 1830 ----------
/** Someone becomes another figure of js/art/people.js (the same person at another moment: O-Tami without the baby on her
    back, the village woman without her basket), keeping the id, the place and the facing (as office-common.js swap). */
export function swap(g, id, kind, at = null, face = null) {
  const cast = g.view.cast, old = cast.get(id);
  const [x, y] = at || (old ? [old.x, old.y] : [400, 500]);
  const yaw = face ?? (old ? old.yaw : "S");
  if (old && old.kind === kind && !at && face == null) return old;
  const hid = old ? old.hidden : false, op = old ? old.opacity : 1, base = old ? old.base : null;
  if (old && old._stop) old._stop();
  if (old) cast.remove(id);
  const f = cast.addFigure(id, kind, x, y, g.scene ? scaleAt(g.scene, y) : 1).face(yaw);
  f.hidden = hid; f.opacity = op; f.base = base;
  return f;
}
/** Someone of the scene walks a set path (in straight lines), at the depth's size. */
export function walkOf(g, id, points, hurry = false) {
  const a = g.actor(id);
  if (!a || !points.length) return Promise.resolve();
  if (hurry) a.hurry = true;
  return a.walkPath(g.clock, points, (y) => scaleAt(g.scene, y));
}
/** Turn someone to a point (or to someone, by id). */
export function look(g, id, at) {
  const a = g.actor(id), b = typeof at === "string" ? g.actor(at) : null;
  if (a && (b || Array.isArray(at))) a.look(...(b ? [b.x, b.y] : at));
}

// ---------- #21: the sum ----------
/** Big Sister's sum, once all three clues are in (the red: O-Tami; the coins: the money box; the blue: the print): she works
    the year out aloud (WRITE-20A's edo.when.solve.1 to .6, whoever is being played), and the act's card comes up with her
    line under it (edo.card.title, edo.card.when): the where-and-when the arrival kept back. True if it was solved now. */
export async function whenSolved(g) {
  if (is(g, "edo.when") || !is(g, "edo.clue.red") || !is(g, "edo.clue.coins") || !is(g, "edo.clue.blue")) return false;
  const big = g.actor("bigsis");
  if (big && big.fidget) big.fidget("count", { hold: true });                     // counting the sixties on her fingers
  await g.say("edo.when.solve.1", "edo.when.solve.2");
  if (big && big.fidget) big.fidget(null);
  await g.say("edo.when.solve.3", "edo.when.solve.4", "edo.when.solve.5", "edo.when.solve.6");
  g.flag("edo.when", true);
  await actCard(g, true);
  return true;
}
/** The act's card: "Act Six: By Your Grace", and (once #21 is solved) Big Sister's line under it. */
export async function actCard(g, when = false) {
  const title = cardWords(g, "edo.card.title", "Act Six: By Your Grace"), sub = when ? cardWords(g, "edo.card.when", "Spring, 1830.") : "";
  await g.card(title, sub, { plain: true, ms: when ? 4200 : 3000 });
}
/** Dad's pencil used on the sticky note (or the note on the pencil), by whoever holds both: the sum written down (not needed). */
export async function sum(g) {
  if (!is(g, "edo.when")) return g.say(who(g) === "bigsis" ? "edo.when.sum.early" : g.fallback("nope"));
  await g.reach();
  await g.say(mine(g, "edo.when.sum"));
}
export const COMBINE = { "pencil+note": sum };

// ---------- what the three say to each other in Yui (WRITE-20A's ids.md, "Companions") ----------
export const TALK = {
  mom: {
    bigsis: [
      { when: (g) => is(g, "edo.clothes") && !is(g, "edo.dressed"), say: ["edo.talk.mom.bigsis.lie.a", "edo.talk.mom.bigsis.lie.b", "edo.talk.mom.bigsis.lie.c"] },
      ["edo.talk.mom.bigsis.read.a", "edo.talk.mom.bigsis.read.b", "edo.talk.mom.bigsis.read.c"],
    ],
    lilsis: [["edo.talk.mom.lilsis.boots.a", "edo.talk.mom.lilsis.boots.b"]],
  },
  bigsis: {
    mom: [["edo.talk.bigsis.mom.tall.a", "edo.talk.bigsis.mom.tall.b"]],
    lilsis: [{ when: (g) => is(g, "edo.hensWest"), say: ["edo.talk.bigsis.lilsis.hens.a", "edo.talk.bigsis.lilsis.hens.b"] }],
  },
  lilsis: {
    mom: [
      { when: (g) => is(g, "edo.fed"), say: ["edo.talk.lilsis.mom.grace.a", "edo.talk.lilsis.mom.grace.b"] },
      ["edo.talk.lilsis.mom.son.a", "edo.talk.lilsis.mom.son.b"],
    ],
    bigsis: [{ when: (g) => is(g, "edo.arigato"), say: ["edo.talk.lilsis.bigsis.word.a", "edo.talk.lilsis.bigsis.word.b", "edo.talk.lilsis.bigsis.word.c"] }],
  },
};

/** Both scenes' `given`: Little Sister keeps her egg (it is for later: a constable on a path in the rain, #27) and her
    three pennies (Kihei's, #23): what she hands to Mom or Big Sister comes straight back, as in Nevada. */
export async function keepHers(g, item, to, from) {
  if (from !== "lilsis" || (item !== "egg" && item !== "pennies")) return;
  const pockets = g.store.data.inventory, i = pockets[to].indexOf(item);
  if (i >= 0) { pockets[to].splice(i, 1); if (!pockets.lilsis.includes(item)) pockets.lilsis.push(item); g.store.emit(); }
  if (!g.clock.skipping) g.ui.toast(`Little Sister keeps ${g.the(item)}`);
  await g.say(item === "egg" ? "nevada.egg.keep" : "nevada.pennies.keep");
}

/** Anything handed to one of the people of Yui who has no use for it: their own polite no (edo.give.no.<person>). */
export const giveNo = (person, items = ["coin", "pennies", "penny", "egg", "lilflash", "carkey", "pencil", "note", "sushibox", "studykey", "batteries", "waters", "mirrorshades", "storeshade"]) =>
  Object.fromEntries(items.map((item) => [item, `edo.give.no.${person}`]));
