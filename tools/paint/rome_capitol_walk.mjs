// The Capitol's places to stand, on the engine's own walk map (js/engine/walk.js), as briefs/out/check-rome.mjs does it:
//   node rome_capitol_walk.mjs [path/to/layout.json] [path/to/game]
// Every mark and every thing's stand must be on the ground (clear of blocked ground by the engine's margin, 12 px
// sideways and 5 up and down), reachable from the way in (fromSteps), and in the left half of the picture above row
// 545 (the inventory bar). The way out's walkTo must be on the ground in the bottom band.
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
const layoutPath = process.argv[2] || "out/rome-capitol/layout.json";
const game = process.argv[3] || (existsSync("../game/js") ? "../game" : "../..");      // (the painter's folder beside the game, or tools/paint in it)
const L = JSON.parse(readFileSync(layoutPath, "utf8"));
const { WalkMap, scaleAt } = await import(join(process.cwd(), game, "js", "engine", "walk.js"));
const blocked = [...(L.blocked || [])];
for (const p of L.planes || []) {
  const s = p.solid;
  if (!s) continue;
  if (Array.isArray(s[0][0])) blocked.push(...s); else blocked.push(s);
}
const scene = { horizon: L.horizon, full: L.full, minScale: L.minScale, walk: { area: L.walk } };
const map = new WalkMap(scene, blocked);
const problems = [];
const places = [];
for (const [k, v] of Object.entries(L.marks)) if (k !== "pen_gate" && Array.isArray(v) && v.length === 2 && typeof v[0] === "number") places.push([`mark ${k}`, v]);   // (the gate is the geese's way in, not a place to stand)
for (const t of L.things) places.push([`stand of ${t.id}`, t.stand]);
for (const e of L.exits) places.push([`walkTo of the way to ${e.to}`, e.walkTo]);
const from = L.marks.fromSteps;
for (const [what, [x, y]] of places) {
  if (what === "mark titus_run") { if (!map.ok(x, y)) problems.push(`${what} ${x},${y}: off the ground`); continue; }
  if (!map.ok(x, y)) { problems.push(`${what} ${x},${y}: nobody can stand there`); continue; }
  if (x < 400 && y > 545) problems.push(`${what} ${x},${y}: under the inventory bar (left half, below row 545)`);
  const route = map.path(from, [x, y]), end = route[route.length - 1];
  if (Math.hypot(end[0] - x, end[1] - y) > 6) problems.push(`${what} ${x},${y}: no way to it from fromSteps`);
  console.log(`  ok  ${what.padEnd(28)} ${String(x).padStart(3)},${String(y).padStart(3)}  scale ${scaleAt(scene, y).toFixed(2)}`);
}
// the bottom band: open floor somewhere, not covered by a thing to click
const inside = (poly, x, y) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) c = !c; } return c; };
let open = 0;
for (let x = 2; x < 798; x += 4) for (let y = 550; y < 598; y += 4) if (map.ok(x, y) && !L.things.some((t) => inside(t.shape.poly, x, y))) open++;
if (!open) problems.push("the bottom band has no open floor");
console.log(`bottom band: ${open} open points`);
console.log(problems.length ? "PROBLEMS:\n  " + problems.join("\n  ") : "ALL PLACES OK");
process.exit(problems.length ? 1 : 0);
