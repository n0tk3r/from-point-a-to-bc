// Prints what a scene file says about its picture, as JSON, for the painter's checks (tools/paint/depth_check.py):
// the horizon and the full row, the walk outline(s), the marks, every clickable area's shape and standing place, and
// the painted cut-outs with their planes and base lines. Reads js/content/scenes/<id>.js as the game does; plays nothing.
//
//   node tools/paint/scene_dump.mjs edo-cedars            (from the top of the repository)
//
// An area or a walk outline that is a function of the game is asked with a stand-in game in which every fact is false.
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const id = process.argv[2];
if (!id) { console.error("usage: node tools/paint/scene_dump.mjs <scene id>"); process.exit(2); }
const mod = await import(pathToFileURL(join(root, "js", "content", "scenes", `${id}.js`)));
const scene = mod.default;

// a game in which nothing has happened yet: every question answers false, null or nothing
const quiet = new Proxy(function () {}, {
  get: (t, k) => (k === Symbol.toPrimitive ? () => 0 : k === "then" ? undefined : quiet),
  apply: () => false,
});
const game = new Proxy({}, {
  get: (t, k) => {
    if (k === "flag" || k === "is" || k === "has" || k === "fact") return () => false;
    if (k === "lead" || k === "scene") return null;
    if (k === "store") return { data: { flags: {}, active: "mom", team: [], inventory: {} } };
    return quiet;
  },
});
const val = (v) => { try { return typeof v === "function" ? v(game) : v; } catch { return null; } };
const pts = (p) => (Array.isArray(p) ? p : null);

const walkRaw = val(scene.walk);
const floors = [];
const addFloor = (f, i) => {
  if (!f) return;
  if (Array.isArray(f) && Array.isArray(f[0]) && typeof f[0][0] === "number") floors.push({ name: String(i), area: f });
  else if (f.area) floors.push({ name: f.name ?? String(i), area: f.area, scale: f.scale ?? null, horizon: f.horizon ?? null, full: f.full ?? null });
  else if (f.x && f.y) floors.push({ name: f.name ?? String(i), area: [[f.x[0], f.y[0]], [f.x[1], f.y[0]], [f.x[1], f.y[1]], [f.x[0], f.y[1]]] });
};
if (Array.isArray(walkRaw) && walkRaw.length && (Array.isArray(walkRaw[0]) ? Array.isArray(walkRaw[0][0]) : true)) walkRaw.forEach(addFloor);
else if (walkRaw && walkRaw.areas) walkRaw.areas.forEach(addFloor);
else addFloor(walkRaw, 0);

const shape = (a) => {
  if (a.poly) return pts(val(a.poly));
  if (a.rect) { const [x, y, w, h] = val(a.rect); return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; }
  return null;
};
const areas = [];
for (const a of val(scene.hotspots) || []) {
  if (!a || !a.id) continue;
  areas.push({ id: a.id, name: typeof a.name === "string" ? a.name : null, shape: shape(a), walkTo: pts(val(a.walkTo)), actor: a.actor ?? null, conditional: typeof a.when === "function" });
}
const planes = (val(scene.planes) || []).map((p) => ({ id: p.id, src: p.src, plane: p.plane ?? "floor", base: p.base ?? null, conditional: typeof p.when === "function" }));
const marks = {};
for (const [k, v] of Object.entries(val(scene.spawn) || {})) if (Array.isArray(v)) marks[k] = v;
const actors = (val(scene.actors) || []).filter((a) => a && Array.isArray(a.at)).map((a) => ({ id: a.id, at: a.at, scale: a.scale ?? null }));

console.log(JSON.stringify({
  id: scene.id, era: scene.era ?? null, horizon: scene.horizon ?? 260, full: scene.full ?? 590, minScale: scene.minScale ?? 0.26, maxScale: scene.maxScale ?? 1.12,
  picture: scene.picture ?? null, floors, blocked: val(scene.blocked) || [], marks, areas, planes, actors,
}));
