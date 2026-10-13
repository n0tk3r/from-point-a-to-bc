// Across the Tiber: every place to stand and every mark in out/rome-tiber/layout.json, checked on the engine's own
// walk map (js/engine/walk.js of the game copy beside this folder), as the act's check script does it: each must be
// on the walkable ground, clear of blocked ground by the engine's margin (12 px sideways, 5 up and down), reachable
// from the way in (fromBridge), and in the left half of the picture above row 545 (the inventory bar).
//
//   node rome_tiber_walk.mjs [path/to/layout.json] [path/to/game]
import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const here = new URL(".", import.meta.url).pathname;
const layoutPath = process.argv[2] || join(here, "out", "rome-tiber", "layout.json");
// the game: given, or the one this folder is in (tools/paint), or a copy beside the painter's working folder
const game = process.argv[3] || [resolve(here, "..", ".."), resolve(here, "..", "game")].find((g) => existsSync(join(g, "js", "engine", "walk.js")));
const { WalkMap, scaleAt } = await import(pathToFileURL(join(game, "js", "engine", "walk.js")).href);
const L = JSON.parse(readFileSync(layoutPath, "utf8"));
const scene = { walk: { area: L.walk }, horizon: L.horizon, full: L.full };
const blocked = [...L.blocked, ...L.planes.filter((p) => p.solid).map((p) => p.solid)];
const map = new WalkMap(scene, blocked);
let problems = 0, checked = 0;
const say = (s) => console.log(s);
const bad = (s) => { problems++; say("PROBLEM " + s); };
const start = L.marks.fromBridge;
if (!map.ok(start[0], start[1])) bad(`fromBridge ${start} is not on the walk map`);

function check(what, p, { reach = true, bar = true } = {}) {
  checked++;
  const [x, y] = p;
  if (!map.ok(x, y)) return bad(`${what} at ${x},${y}: nobody can stand there (off the floor or within the margin of blocked ground)`);
  if (bar && x < 400 && y > 545) bad(`${what} at ${x},${y}: under the inventory bar (left half, below row 545)`);
  if (reach) {
    const route = map.path(start, [x, y]), end = route[route.length - 1];
    if (Math.hypot(end[0] - x, end[1] - y) > 6) bad(`${what} at ${x},${y}: no way to it from fromBridge (the route ends at ${end.map((v) => v.toFixed(0))})`);
  }
}

for (const t of L.things) check(`thing ${t.id} (stand)`, t.stand);
const m = L.marks;
for (const name of ["fromBridge", "default", "mariam_talk", "petosiris", "door", "wait"]) check(`mark ${name}`, m[name]);
check("mark toBridge", m.toBridge, { bar: false });
check("mark felix", m.felix.at);
m.felix_spots.forEach((p, i) => check(`mark felix_spots[${i}]`, p));
check("mark pray_eleazar", m.pray_eleazar);
check("mark pray_son", m.pray_son);
check("mark bless (Eleazar)", m.bless);
// the blessing: the boy faces him a step in front, further right on the screen, on the same row
{
  const [bx, by] = m.bless, h = 0.96 * 160 * scaleAt(scene, by);
  check(`the boy at the blessing (BLESS_STEP 0.30 of ${h.toFixed(1)} px to the right)`, [bx + 0.30 * h, by]);
}
for (const e of L.exits) { check(`exit ${e.to} walkTo`, e.walkTo, { bar: false }); check(`exit ${e.to} arrive`, e.arrive); }
const baseAt = (base, x) => {                                   // as cast.js reads a base: a row, or a slanted line held at its ends
  if (typeof base === "number") return base;
  const [[x1, y1], [x2, y2]] = base;
  return y1 + (y2 - y1) * (x2 === x1 ? 0.5 : Math.min(1, Math.max(0, (x - x1) / (x2 - x1))));
};
// Mariam and the hens are in the yard: not on the walk map, and behind the fence's two cut-outs (their bases are rows: the
// near run's below everyone in the yard; the corner's below everyone who can come in front of it on the screen, left of
// x 632, where the side fence ends at the house wall: rome_tiber_order.py checks it pixel by pixel)
const near = L.planes.find((p) => p.id === "fence").base, corner = L.planes.find((p) => p.id === "fence-corner").base;
for (const [what, p] of [["mariam", m.mariam.at], ...m.mariam_spots.map((q, i) => [`mariam_spots[${i}]`, q]), ["hens row start", m.hens[0]], ["hens row end", m.hens[1]],
  ...L.fx.filter((f) => String(f.id).startsWith("hen-")).flatMap((f) => f.perch.map((q, i) => [`${f.id} perch end ${i}`, q]))]) {
  checked++;
  if (!(p[1] < baseAt(near, p[0]))) bad(`${what} at ${p}: not behind the fence (its base is at row ${baseAt(near, p[0])})`);
  if (p[0] < 632 && !(p[1] < baseAt(corner, p[0]))) bad(`${what} at ${p}: not behind the fence's corner (its base is at row ${baseAt(corner, p[0])})`);
  if (map.ok(p[0], p[1])) bad(`${what} at ${p}: on the walk map (the yard should be off it)`);
}
// Felix and Petosiris in front of the barge (below its base)
const barge = L.planes.find((p) => p.id === "barge").base;
for (const [what, p] of [["felix", m.felix.at], ...m.felix_spots.map((q, i) => [`felix_spots[${i}]`, q]), ["petosiris", m.petosiris]]) {
  checked++;
  if (!(p[1] >= baseAt(barge, p[0]))) bad(`${what} at ${p}: not in front of the barge (its base is at row ${baseAt(barge, p[0]).toFixed(1)} there)`);
}
// the bottom band of the way out: floor somewhere in rows 548 to 600 that no thing covers
{
  let free = 0;
  for (let x = 400; x < 800; x += 4) for (let y = 552; y < 600; y += 4) if (map.ok(x, y)) free++;
  checked++;
  if (!free) bad("no floor in the bottom band right of the middle");
}
say(`${checked} checks, ${problems} problem${problems === 1 ? "" : "s"}`);
process.exit(problems ? 1 : 0);
