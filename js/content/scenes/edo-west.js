// What the scenes of Act Six's road west share, from the Akashi shore to the women's hall (SCENES-21C: new in round twenty-one;
// briefs/SCENES-21.md, and the design, briefs/out/edo2-design.md, #35 to #38, "The next day" and "Mind The Fire"). Not a scene
// (it is in no list of scenes): a module edo-akashi.js, edo-town.js, edo-shosha.js, edo-lock.js, edo-hall.js and the cut-scenes
// edo-walk2.js and edo-night.js import, as the Himeji scenes import edo-himeji.js. What the whole act shares is edo-common.js;
// round twenty's Himeji helpers (edo-himeji.js) are used as they are.
//
//   who, is, heard, each   the lead being played; a fact; has a line been said; a look or a use for each of the three
//   inside, near           a point in an outline (a zone of the floor, the shallows); within a few pixels of it
//   pockets                put a thing into a lead's pockets, take it from whoever has it, swap one thing for another
//   dressAll               the three in O-Tami's clothes as the place wants them (the hat on outdoors, on the back indoors);
//                          a held moment's own outfit (wading, hand in hand) is the scene's to put on and take off
//   thing                  a thing of a scene, by its shape, with a look and a use for each of the three
//   GIVE_SILENT            the act's stock replies with no "give" line: the women's hall says its own (the lock's hand-round)
//   nightTint              the dark over a painting, for "Mind The Fire" (drawn on the live layer: the town by night)

import { STOCK_DRESSED } from "./edo-common.js";
import { THREE, who, is, heard, each, holderOf, moveItem, idle, chatter, swap, TALK } from "./edo-himeji.js";

export { THREE, who, is, heard, each, holderOf, moveItem, idle, chatter, swap, TALK };

// ---------- shapes ----------
/** Is a point inside an outline? */
export function inside(poly, x, y) {
  let hit = false;
  for (let i = 0, k = poly.length - 1; i < poly.length; k = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[k];
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) hit = !hit;
  }
  return hit;
}
/** Is a figure (or a point) standing inside an outline, or within `d` pixels of it? */
export function standsIn(poly, f, d = 0) {
  if (!f) return false;
  const x = f.x ?? f[0], y = f.y ?? f[1];
  if (inside(poly, x, y)) return true;
  if (!d) return false;
  for (let i = 0; i < poly.length; i++) {
    const [ax, ay] = poly[i], [bx, by] = poly[(i + 1) % poly.length], L = (bx - ax) ** 2 + (by - ay) ** 2;
    const t = L ? Math.max(0, Math.min(1, ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / L)) : 0;
    if (Math.hypot(ax + t * (bx - ax) - x, ay + t * (by - ay) - y) <= d) return true;
  }
  return false;
}

// ---------- pockets ----------
const inv = (g) => g.store.data.inventory || (g.store.data.inventory = {});
/** A thing into a lead's pockets (any lead, not only the one being played); nothing said. */
export function giveTo(g, lead, item) {
  const p = inv(g)[lead] || (inv(g)[lead] = []);
  if (!p.includes(item)) p.push(item);
  g.store.emit();
}
/** A thing out of whoever's pockets it is in; true if it was there. */
export function takeAny(g, item) {
  const from = holderOf(g, item);
  if (!from) return false;
  const p = inv(g)[from];
  p.splice(p.indexOf(item), 1);
  g.store.emit();
  return true;
}
/** One thing in a lead's pockets becomes another, in its place (three pennies become two; two become one). */
export function swapItem(g, lead, from, to) {
  const p = inv(g)[lead] || [];
  const i = p.indexOf(from);
  if (i >= 0) p[i] = to; else if (!p.includes(to)) p.push(to);
  g.store.emit();
}
/** Does a lead carry a thing? (any lead) */
export const carries = (g, lead, item) => (inv(g)[lead] || []).includes(item);

// ---------- their clothes ----------
const PLAIN = new Set([null, undefined, "edo", "edo-hatback"]);
/** The three in O-Tami's clothes: outdoors the hat on (`edo`), indoors on the back (`edo-hatback`). A held moment's own outfit
    (Little Sister wading, or hand in hand) is left alone unless `all`. */
export function dressAll(g, place = "outdoors", all = false) {
  const want = place === "indoors" ? "edo-hatback" : "edo";
  for (const id of THREE) {
    const now = g.dressOf(id);
    if (now !== want && (all || PLAIN.has(now))) g.dress(id, want);
  }
}

// ---------- the scenes' things ----------
/** A thing of a scene, by its shape, with a look and a use for each of the three: `<short>.<id>.<who>` and `.use.<who>`. */
export const thingOf = (short) => (id, name, shape, walkTo, face, more = {}) =>
  ({ id, name, ...shape, walkTo, face, look: each(`edo.${short}.${id}`), use: each(`edo.${short}.${id}.use`), ...more });
/** Turn two people to each other. */
export function faceEach(g, a, b) {
  const x = typeof a === "string" ? g.actor(a) : a, y = typeof b === "string" ? g.actor(b) : b;
  if (x && y) { x.look(y.x, y.y); y.look(x.x, x.y); }
}
/** Someone holds a thing up while lines are said, then lets it drop (a hold of their own page). */
export async function holding(g, id, hold, fn) {
  const f = g.actor(id);
  if (f) f.hold(true, hold);
  try { return await fn(); } finally { const h = g.actor(id); if (h && h.act && h.act.low === hold) h.hold(false); }
}

// ---------- stock ----------
/** The act's stock replies with no "give" line for the three (an empty list says nothing): the women's hall and its lock say
    their own as a thing changes hands (the hand-round: LOCK.give, in the scene's `given`). */
export const GIVE_SILENT = { ...STOCK_DRESSED, give: { mom: [], bigsis: [], lilsis: [] } };
/** The act's own give line, as the engine would have said it. */
export const stockGive = (lead) => `edo.give.${lead}.1`;

// ---------- the dark ----------
/** A night over a painting, on the live layer (under the people: for a cut-scene that draws no people, or draws them as
    shapes): a deep blue wash, darker at the top; `glows` [[x, y, r, opacity], ...] warm pools of lantern light. */
export function nightTint(id, glows = [], { wash = 0.74 } = {}) {
  let s = `<defs><linearGradient id="${id}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05081a" stop-opacity="${Math.min(1, wash + 0.12)}"/>`;
  s += `<stop offset="1" stop-color="#0c1430" stop-opacity="${wash}"/></linearGradient>`;
  s += `<radialGradient id="${id}-glow"><stop offset="0" stop-color="#ffd27a" stop-opacity="0.85"/><stop offset="0.35" stop-color="#ffb04a" stop-opacity="0.35"/><stop offset="1" stop-color="#ffb04a" stop-opacity="0"/></radialGradient></defs>`;
  s += `<rect width="800" height="600" fill="url(#${id}-sky)"/>`;
  for (const [x, y, r, o = 1] of glows) s += `<circle cx="${x}" cy="${y}" r="${r}" fill="url(#${id}-glow)" opacity="${o}" style="mix-blend-mode:screen"/>`;
  return s;
}
