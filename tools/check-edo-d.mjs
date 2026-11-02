// WRITE-21B: the check of Act Six's road on from the hills (js/content/lines/edo-d.en.js, js/content/talk/edo-d.js) and of the
// history pass's edits in edo-a.en.js and edo-b.en.js. Run from the game folder: `node tools/check-edo-d.mjs`. Quiet when all
// is well (one summary line); otherwise each problem on its own line, and the exit code is 1.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const url = (p) => "file://" + join(root, p);
const problems = [];
const bad = (msg) => problems.push(msg);

const { lines: D } = await import(url("js/content/lines/edo-d.en.js"));
const { lines: A } = await import(url("js/content/lines/edo-a.en.js"));
const { lines: B } = await import(url("js/content/lines/edo-b.en.js"));
const { lines: ALL } = await import(url("js/content/lines.en.js"));
const { cast } = await import(url("js/content/world.js"));
const T = await import(url("js/content/talk/edo-d.js"));
const LEADS = ["mom", "bigsis", "lilsis"];

// ---- 1. every id once in the source, and with my prefixes ----
const src = readFileSync(join(root, "js/content/lines/edo-d.en.js"), "utf8");
const keys = [...src.matchAll(/^\s*"([^"]+)":\s*\[/gm)].map((m) => m[1]);
const seen = new Map();
for (const k of keys) seen.set(k, (seen.get(k) || 0) + 1);
for (const [k, n] of seen) if (n > 1) bad(`id written ${n} times in edo-d.en.js: ${k}`);
const MINE = /^(edo\.(walk\.stop|akashi|walk2|town|shosha|lock|hall|night)\.|edo\.step\.0$|edo\.map\.far\.(yui|osaka|hills|akashi|himeji)\.[1-5]$|edo\.map\.shosha\.|item\.(ladle|crab|fusaslip|lastpenny|riceball)\.|hint\.edo\.(ladle|supper|hall|son)\.)/;
for (const k of Object.keys(D)) if (!MINE.test(k)) bad(`not one of WRITE-21B's prefixes: ${k}`);
for (const k of Object.keys(D)) if (A[k] || B[k]) bad(`also in a round-twenty file: ${k}`);

// ---- 2. every speaker a person (world.js, or PEOPLE-21B's kinds, which MERGE adds) ----
const PEOPLE21B = ["fusa", "leader", "heita", "sato", "satosister", "awapilgrim1", "awapilgrim2", "tane", "kiku", "shizu", "pupil1",
  "pupil2", "tobei", "ume", "ryokai", "tome", "wife", "girl"];
const speakers = new Set();
for (const [id, entry] of Object.entries(D)) {
  if (!Array.isArray(entry) || entry.length !== 2 || typeof entry[1] !== "string") { bad(`not ["who", "text"]: ${id}`); continue; }
  const [who] = entry;
  speakers.add(who);
  if (!cast[who] && !PEOPLE21B.includes(who)) bad(`speaker "${who}" is not a person: ${id}`);
}
const notYet = [...speakers].filter((w) => !cast[w]).sort();

// ---- 3. boxes: 80 characters (Scripture aside), one word in capitals, one exclamation mark ----
const SCRIPTURE = { "Psalm 61:1-2": ["edo.shosha.psalm.1", "edo.shosha.psalm.2", "edo.shosha.psalm.3"], "Isaiah 49:15": ["edo.hall.sunset.1", "edo.hall.sunset.2", "edo.hall.sunset.3"] };
const scriptureIds = new Set(Object.values(SCRIPTURE).flat());
const CAPS_OK = new Set(["I", "A", "O", "LORD"]);
for (const [id, [who, text]] of Object.entries(D)) {
  if (text.length > 80 && !scriptureIds.has(id)) bad(`over 80 (${text.length}): ${id}`);
  const caps = (text.match(/\b[A-Z]{2,}\b/g) || []).filter((w) => !CAPS_OK.has(w));
  if (caps.length > 1) bad(`more than one word in capitals (${caps.join(", ")}): ${id}`);
  if ((text.match(/!/g) || []).length > 1) bad(`more than one exclamation mark: ${id}`);
  if (/^(Well|So|Okay|Oh|Hmm),/.test(text)) bad(`opens with a filler word: ${id}`);
}
// the round-twenty edits too: lengths
for (const [file, L] of [["edo-a", A], ["edo-b", B]]) {
  const s = readFileSync(join(root, `js/content/lines/${file}.en.js`), "utf8");
  for (const m of s.matchAll(/^\s*"([^"]+)":.*\/\/ WRITE-21B:/gm)) { const t = L[m[1]] && L[m[1]][1]; if (!t) bad(`edited id missing: ${m[1]}`); else if (t.length > 80) bad(`edited line over 80: ${m[1]}`); }
}

// ---- 4. words the act never says; Scripture exactly ----
const NEVER = [/itadakimasu/i, /gochis/i, /white heron/i, /kawaraban/i, /bunraku/i, /thursday|monday|tuesday|wednesday|friday|saturday|sunday/i,
  /m[oō]kari/i, /kitchen of the realm/i, /tsumoto/i, /takoyaki/i, /kitsune udon/i, /okonomiyaki/i, /battera/i, /nigiri/i, /tenp[oō]zan/i,
  /ropeway/i, /bell of compassion/i, /chanchanko/i, /hakone/i, /nori/i, /seaweed/i, /leather/i, /crucif/i, /ghost/i];
for (const [id, [, text]] of Object.entries(D)) for (const re of NEVER) if (re.test(text)) bad(`says what the act never says (${re}): ${id}`);
const KJV = {
  "Psalm 61:1-2": "Hear my cry, O God; attend unto my prayer. From the end of the earth will I cry unto thee, when my heart is overwhelmed: lead me to the rock that is higher than I.",
  "Isaiah 49:15": "Can a woman forget her sucking child, that she should not have compassion on the son of her womb? yea, they may forget, yet will I not forget thee.",
};
for (const [ref, ids] of Object.entries(SCRIPTURE)) {
  const joined = ids.map((i) => (D[i] ? D[i][1] : "")).join(" ");
  if (joined !== `'${KJV[ref]}'`) bad(`${ref} is not the King James text exactly: ${joined}`);
  for (const i of ids) if (!D[i] || D[i][0] !== "mom") bad(`${ref}: ${i} is not Mom's`);
}
if (!D["edo.shosha.psalm.4"] || D["edo.shosha.psalm.4"][1] !== "Psalm 61." || D["edo.shosha.psalm.4"][0] !== "bigsis") bad("Big Sister's \"Psalm 61.\" is not right");
if (!D["edo.hall.sunset.4"] || D["edo.hall.sunset.4"][1] !== "Isaiah 49:15." || D["edo.hall.sunset.4"][0] !== "bigsis") bad("Big Sister's \"Isaiah 49:15.\" is not right");
const SCRIPTY = /\b(thee|thou|thy|thine|unto|saith|hath|LORD|yea)\b/;
for (const [id, [who, text]] of Object.entries(D)) {
  if (scriptureIds.has(id)) continue;
  if (SCRIPTY.test(text)) bad(`looks like Scripture but is not one of the round's verses: ${id}`);
  if (/\b(Psalm|Isaiah|Jeremiah|Luke|Matthew|John|Genesis)\s+\d/.test(text) && who !== "bigsis") bad(`a reference said by someone not Big Sister: ${id}`);
}

// ---- 5. the trees: every id they name is a line ----
const known = (id) => !!ALL[id];
const walk = (v, where) => {
  if (v == null) return;
  if (typeof v === "string") { if (/^(edo|hint)\./.test(v) && !known(v)) bad(`${where} names a line that is not there: ${v}`); return; }
  if (Array.isArray(v)) { v.forEach((x) => walk(x, where)); return; }
  if (typeof v === "object") for (const x of Object.values(v)) walk(x, where);
};
const g0 = { store: { data: { active: "mom", inventory: {} } }, flag: () => false, has: () => false, asked: () => 0, lines: ALL };
for (const [name, make] of Object.entries(T.trees)) {
  const tree = make({});
  if (!tree || !tree.nodes) { bad(`${name} is not a tree`); continue; }
  for (const [nid, node] of Object.entries(tree.nodes)) {
    walk(node.say, `${name}/${nid}`);
    for (const o of node.options || []) { walk(o.line, `${name}/${nid}/${o.id}`); walk(o.say, `${name}/${nid}/${o.id}`); if (!o.line) bad(`${name}/${nid}/${o.id} has no line`); }
  }
}
for (const list of ["WALK", "WALK2", "NIGHT", "STEP", "AKASHI", "TOWN", "COOK", "SHOSHA", "HALL", "LOCK", "SON", "FAR", "SHOSHA_MAP"]) walk(T[list], list);
// byLead groups expand to all three
for (const [list, k] of [["AKASHI", "east"], ["AKASHI", "west"], ["TOWN", "north"], ["LOCK", "letgo"]]) for (const lead of LEADS) if (!known(T[list][k][lead])) bad(`${list}.${k}.${lead} is not a line`);

// ---- 6. every hint stage for each of the three, and hintFor's answers ----
for (const [beat, h] of Object.entries(T.HINTS)) for (const st of h.stages) for (const lead of LEADS) if (!D[`hint.edo.${beat}.${lead}${st}`]) bad(`no hint for ${beat} stage "${st || "1"}" for ${lead}`);
const FACTS = ["edo.fusaMet", "edo.waded", "edo.crabClue", "edo.crab", "edo.ladleFree", "edo.ladleBack", "edo.riddle", "edo.kikuIn", "edo.knowWay",
  "edo.kitchenLent", "edo.riceballs", "edo.oumeMet", "edo.lockSeen", "edo.listRead", "edo.earHeld", "edo.postHeld", "edo.sonHeard", "edo.doorWide", "edo.sonFed"];
for (let mask = 0; mask < 2 ** 10; mask++) {             // a spread of states (the first ten facts every way; the rest from the mask's bits again)
  const on = new Set(FACTS.filter((f, i) => (mask >> (i % 10)) & 1));
  for (const lead of LEADS) {
    const g = { store: { data: { active: lead, inventory: { lilsis: ["kanzashi"], mom: ["mon"], bigsis: ["comb"] } } }, flag: (f) => on.has(f) };
    for (const beat of ["ladle", "supper", "hall", "son"]) { const id = T.hintFor(g, beat, lead); if (!D[id]) bad(`hintFor(${beat}, ${lead}) gives a line that is not there: ${id}`); }
  }
}

// ---- 7. every new item a look for each of the three ----
for (const item of ["ladle", "crab", "fusaslip", "lastpenny", "riceball"]) for (const lead of LEADS) if (!D[`item.${item}.${lead}`]) bad(`no look at ${item} for ${lead}`);

// ---- 8. every place behind the family in every leg has a far line ----
const BEHIND = { yui: [2, 3, 4, 5], osaka: [3, 4, 5], hills: [4, 5], akashi: [5] };
for (const [place, legs] of Object.entries(BEHIND)) for (const leg of legs) { const id = T.farLine(place, leg); if (id !== `edo.map.far.${place}.${leg}` || !D[id]) bad(`no far line for ${place} from leg ${leg}`); }
for (const place of ["yui", "osaka", "hills", "himeji"]) if (!known(`edo.map.far.${place}`)) bad(`round twenty's fallback far line is gone: ${place}`);

// ---- 9. every thing in ROUND-21's lists for these scenes: a look and a use for each of the three (people: a look; a use is a tree) ----
const THINGS = {
  akashi: ["strait", "awaji", "castle", "pilgrimboat", "pilgrims", "banner", "ladlething", "pots", "potlines", "heitaboat", "tub", "rocks", "pines", "sand", "road", "shallows", "komuso"],
  town: ["keep", "roofs", "cottonoffice", "noteoffice", "bales", "house", "passage", "well", "bucket", "ricepot", "saltjar", "pickletub", "plumjar", "cloth", "pan", "mortar",
    "school", "desks", "gate", "hut", "hutsandals", "sweets", "clappers", "highway", "kitchendoor", "lane", "storehouse", "komuso"],
  shosha: ["mountain", "pathup", "stone", "trees", "cherry", "hall", "doors", "lock", "slips", "step", "stepball", "lattice", "hut", "lantern", "bench", "combs", "plain", "castle", "sky"],
  lock: ["rabbit", "ear", "earhole", "waves", "wave", "post", "back", "bolt", "hasp", "lattice"],
  hall: ["lattice", "bars", "wall", "hum", "cabinet", "lamp", "incense", "flowers", "slips", "posts", "ceiling", "mats", "doorway", "door", "desk"],
};
const PEOPLE = { akashi: ["fusa", "leader", "heita", "sato", "satosister", "awapilgrim1", "awapilgrim2"], town: ["tane", "kiku", "shizu", "pupil1", "pupil2", "tobei"],
  shosha: ["ume", "ryokai", "tome", "wife", "girl"], hall: ["ume", "ryokai"] };
// uses that are a sequence or a tree instead of a line (ids.md says which)
const USE_IS_SCENE = new Set(["akashi.ladlething.lilsis", "akashi.shallows.lilsis", "hall.door.mom", "town.lane.mom", "town.lane.bigsis", "town.lane.lilsis"]);
for (const [short, things] of Object.entries(THINGS)) for (const thing of things) for (const lead of LEADS) {
  if (!D[`edo.${short}.${thing}.${lead}`]) bad(`no look at ${short}/${thing} by ${lead}`);
  if (!D[`edo.${short}.${thing}.use.${lead}`] && !USE_IS_SCENE.has(`${short}.${thing}.${lead}`)) bad(`no use of ${short}/${thing} by ${lead}`);
}
for (const [short, people] of Object.entries(PEOPLE)) for (const p of people) for (const lead of LEADS) if (!D[`edo.${short}.${p}.${lead}`]) bad(`no look at ${short}/${p} by ${lead}`);

// ---- 10. the lock's table: every part, state, lead and thing gives a line ----
const STATES = { "edo.earClean": [false, true], "edo.earHeld": [false, true], "edo.postHeld": [false, true] };
for (const clean of [false, true]) for (const ear of [false, true]) for (const post of [false, true]) {
  if (post && !ear) continue;
  const on = new Set([clean && "edo.earClean", ear && "edo.earHeld", post && "edo.postHeld"].filter(Boolean));
  const g = { flag: (f) => on.has(f) };
  for (const thing of THINGS.lock) for (const lead of LEADS) for (const item of [null, "kanzashi", "mon", "comb", "lastpenny", "coin", "riceball", "note"]) {
    const ids = T.lockLines(g, ALL, thing, lead, item);
    if (!ids.length) bad(`the lock says nothing: ${thing}${clean ? " (clean)" : ""}${ear ? " (ear held)" : ""}${post ? " (post held)" : ""}, ${lead}, ${item || "nothing"}`);
    for (const id of ids) if (!known(id)) bad(`lockLines gives a missing line: ${id}`);
  }
}
for (const [item, lead] of Object.entries(T.LOCK.rightHands)) if (!known(T.LOCK.give[item])) bad(`no hand-round line for ${item} (to ${lead})`);

// ---- 11. the kitchen: every step after every set of steps gives a line ----
const steps = T.COOK.order;
for (let mask = 0; mask < 2 ** steps.length; mask++) {
  const done = steps.filter((s, i) => (mask >> i) & 1);
  for (const step of [...steps, "plum"]) for (const id of T.cookLines(done, step)) if (!known(id)) bad(`cookLines(${done.join("+") || "-"}, ${step}) gives a missing line: ${id}`);
}

// ---- 12. the Son: his lines are his, and every list of his is in the file ----
for (const [k, list] of Object.entries(T.SON)) for (const id of list) if (!known(id)) bad(`SON.${k} names a missing line: ${id}`);
const sonLines = Object.entries(D).filter(([, [w]]) => w === "son").length;

// ---- 13. Japanese words glossed: tako, hi no yōjin ----
const has = (re) => Object.values(D).some(([, t]) => re.test(t));
if (!has(/Tako\. Octopus\.|Tako is octopus\./)) bad("tako is never glossed");
if (!has(/Hi no yōjin\. Mind the fire\./)) bad("hi no yōjin is never glossed by Tōbei");

// ---- the summary ----
const count = (re) => Object.keys(D).filter((k) => re.test(k)).length;
const hints = count(/^hint\./), treesN = Object.keys(T.trees).length;
if (problems.length) { for (const p of problems) console.log("PROBLEM: " + p); console.log(`${problems.length} problem(s).`); process.exit(1); }
console.log(`check-edo-d: ${Object.keys(D).length} lines (${hints} hints, ${sonLines} of the Son's), ${treesN} trees; quiet.` +
  (notYet.length ? ` Speakers not in world.js yet (PEOPLE-21B's, for MERGE): ${notYet.join(", ")}.` : ""));
