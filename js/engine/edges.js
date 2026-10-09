// Ways out at the edges of the picture.
//
// The old adventure games let the player walk off the edge of the screen. A scene names the ways out across the edges
// of its picture:
//
//     edges: {
//       N: { to: "egypt-site", spawn: "fromCrash", name: "up the track" },     the top of the picture
//       S: { to: "egypt-crash", spawn: "fromSite" },                            the bottom
//       W: { ... },  E: { ... },                                                left, right
//     },
//
//   to, spawn   the scene, and the named way in at the other end: what g.goto(to, { spawn }) is given
//   name        what the label line says after "Go": "Go up the track". With none, "Go to" and the other scene's name
//               ("Go to the great gallery").
//   walkTo      [x, y], where the lead walks before leaving. With none: the floor nearest the click, pushed as far
//               toward that edge as the floor goes (WalkMap.toward).
//   when(g)     the way is there only while this is true. While it is false its band is plain floor.
//   use(g)      a script to run instead of g.goto(to, { spawn }): a way out that is also a gate, or that needs a line first.
//
// Along each named edge lies a band (BANDS). Over the floor in a band the pointer becomes an arrow pointing out of the
// picture and the label line says where the way leads; a click there walks the lead to the edge, and leaves. A clickable
// area in a band, and a companion standing in one, are clicked as usual: they always win. In Show each way out is drawn
// as an arrow at the middle of its edge (outline.js). The engine's side of all this is in game.js (leave, edgeAt).
//
// Every number is a pixel of the 800x600 picture (grid.js).

import { W, H } from "./grid.js";

/** How deep the band along each edge is: the top 60 pixels of the picture, the bottom 52, the left 44 and the right 44. */
export const BANDS = { N: 60, S: 52, W: 44, E: 44 };
export const SIDES = ["N", "S", "W", "E"];

/** How far a point is from each edge. */
const GAP = { N: (x, y) => y, S: (x, y) => H - y, W: (x) => x, E: (x) => W - x };

/** Is this way out there now? */
export const open = (way, g) => !!way && (!way.when || !!way.when(g));

/** The side ("N", "S", "W" or "E") of the way out whose band holds this point, or null. Only ways that are there now
    count. Where two bands meet (a corner), the point belongs to the edge it is nearer. */
export function edgeAt(scene, g, x, y) {
  const edges = scene && scene.edges;
  if (!edges) return null;
  let best = null, near = Infinity;
  for (const side of SIDES) {
    const d = GAP[side](x, y);
    if (d >= 0 && d < BANDS[side] && d < near && open(edges[side], g)) { best = side; near = d; }
  }
  return best;
}

/** A scene's name as it reads after "Go to": "The great gallery" becomes "the great gallery". A name that begins with
    somebody's name keeps its capital ("Little Sister's room", "Dad's study"). */
export function afterTo(name) {
  const [first = "", second = ""] = String(name || "").split(/\s+/);
  if (/^(The|A|An)$/.test(first)) return first.toLowerCase() + name.slice(first.length);
  if (/'s$/.test(first) || /^[A-Z]/.test(second)) return name;
  return name.charAt(0).toLowerCase() + name.slice(1);
}

/** What the label line says over a way out: "Go up the track", or "Go to the great gallery". `there` is the other scene's name. */
export function edgeLabel(way, there) {
  if (way.name) return "Go " + way.name;
  return there ? "Go to " + afterTo(there) : "Go on";
}

/** Look for mistakes in the scenes' ways out. `scenes` is { id: scene } for every scene. Returns plain sentences. */
export function checkEdges(scenes) {
  const problems = [];
  for (const [id, scene] of Object.entries(scenes)) {
    if (!scene || !scene.edges) continue;
    for (const [side, way] of Object.entries(scene.edges)) {
      const where = `Scene "${id}", edge ${side}`;
      if (!SIDES.includes(side)) { problems.push(`${where}: the edges are N (the top), S (the bottom), W (the left) and E (the right).`); continue; }
      if (!way || typeof way !== "object") { problems.push(`${where}: a way out is { to, spawn }.`); continue; }
      if (!way.to && !way.use) problems.push(`${where} goes nowhere: give it \`to\` (and \`spawn\`), or a \`use\` script.`);
      if (way.to && !scenes[way.to]) problems.push(`${where} goes to "${way.to}", which is not in js/content/scenes/index.js.`);
      else if (way.to && way.spawn && !((scenes[way.to].spawn || {})[way.spawn])) problems.push(`${where} comes in at "${way.spawn}", which scene "${way.to}" has no spawn mark for.`);
      if (way.walkTo && !(Array.isArray(way.walkTo) && way.walkTo.length === 2 && way.walkTo.every(Number.isFinite))) problems.push(`${where}: walkTo is [x, y].`);
      if (/^go\b/i.test(way.name || "")) problems.push(`${where}: the label puts "Go" before the name itself, so the name is "${way.name.replace(/^go\s*/i, "")}".`);
    }
  }
  return problems;
}
