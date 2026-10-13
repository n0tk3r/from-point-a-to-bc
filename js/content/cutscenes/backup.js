// The cut-scene "Backup" (NEVADA-12SC: new in round twelve). It closes Act Four and opens Act Five: the author's own scene,
// staged (briefs/out/nevada-expansion-design.md, "Cut-Scene: Backup"; every line is in js/content/lines/nevada.en.js,
// nevada.backup.*, said in the order of that file).
//
// The family has gone through the door; the door stands open in Grandpa Joe's light; the lot is quiet. Then:
//   1. Jed, along the fence with his back to all of it since #7, turns round, sees the door and walks up to it:
//      "Houston, we have a problem...they figured it out. I need a cheeseburger and backup... immediately."
//   2. Grandpa Joe lets the sun shade down (he is himself again, on his feet, the banjo in his hand), and the door folds
//      shut, from the outside in, to nothing. Jed makes for the road; Grandpa Joe steps into his way: "You ain't goin'
//      nowhere flat foot!" The banjo goes up, and comes down: one twang, every string at once, and Jed sits down in the
//      dust with the banjo's hoop round his neck like a collar. Nobody is hurt. "...I would still like the cheeseburger."
//   3. Dust on the road: a gray limousine comes in along the lot from the left, as long as the porch, and stops in front
//      of it. Four doors at once: four men in gray step out in a row, one of them with a paper bag. "Who ordered a cheese
//      burger? Jed? JED?" They see Jed, and Grandpa Joe with what is left of the banjo; they consult a clipboard.
//   4. "Sir. We are going to need you to come with us." "Mind the hat." He walks over to them himself (nobody is pushed
//      or pulled), and the four of them stand round him in a row while they tie him up, saying sorry; when they step
//      back he is tied, with a bow. "Lifting on three, sir." Two of them carry him to the car between them like a sofa,
//      his hat on and his boots off the ground, and in he goes. The banjo is evidence: there will be a receipt.
//   5. Jolene comes out onto the porch in the hat of the hour, and they have their way of talking. Ranger comes out from
//      behind the car at a run and is in through the last door as it shuts ("Is that a raccoon?" "I can neither confirm
//      nor deny the raccoon."). Jed is helped up and put in the front; lunch rides in the back, by regulation.
//   6. The limousine turns, and out of the window: "Jolene! Feed the hens! And don't sell my rocks!" "I'll sell every one
//      of 'em, Joe!" It goes out the way it came. Out back, the five hens turn round, all together, and watch it go, and
//      turn back to the fence (a look through the store's back door, drawn close: see hensWatch). Jolene, alone on the
//      porch, to nobody: "Well. I'd better change my hat." The card: "Meanwhile, in a limousine."
//   7. Then the play goes to the new team, Grandpa Joe and Ranger (Act Five), and to the limousine.
//
// How it stays silly (the design's own list): nobody is pushed, pulled or shouted at; the suits say sir and sorry; the
// rope has a bow; Jed's injury is a banjo collar and a wish for lunch; Grandpa Joe is cheerful from the first word to the
// last and so is Jolene; Ranger chooses to go; the hens watch.
//
// Where it is played from: the roadside's own script calls it at the end of #13 (g.cutscene("backup")), and the roadside's
// enter() calls it for a game saved between "nevada.left" and "nevada.backup". So it begins by dressing the stage as #13
// leaves it, from the facts, whatever is on it (`ready`): the family not to be seen, Grandpa Joe holding the sun shade
// at the coin-holder's place with the cut-out showing, his rocking chair empty on the porch, Ranger beside it, Jed along
// the fence, and the door open wide (the scene's own door(g, size, ms): briefs/SCENES-12.md).
// Skipped, it runs the same script with every wait cut to nothing (DESIGN.md, section 5) and lands in the same place:
// every fact set, the new team, the limousine.
//
// Every place below is a pixel of the roadside's picture (art/scenes/nevada-roadside/layout.json, and the limousine's own
// numbers there under "limo"), or was set by eye against the picture with the people standing in it.

import { scaleAt } from "../../engine/walk.js";
import { Seat } from "../../engine/cast.js";
import { people } from "../../art/people.js";

const ROAD = "art/scenes/nevada-roadside/";
const STORE = "art/scenes/nevada-store/";
const FAMILY = ["mom", "bigsis", "lilsis"];
const SUITS = ["suit1", "suit2", "suit3", "suit4"];

// ---------- where everybody is ----------
const HOLD = [572, 560];               // Grandpa Joe, holding the sun shade up (the coin-holder's place, facing E: the contract)
const ROCKER = [388, 498];             // his rocking chair on the porch (drawn with him; left there while he is up)
const PORCH = [352, 512];              // Ranger, on the ground beside the chair (the contract)
const FENCE = [752, 468];              // Jed, a few yards along the fence, where #7 left him
const BY_DOOR = [[748, 482], [740, 497]];       // Jed, walking up to the door in time (two steps, a stop, two more): at its far side, clear of the shade
const ROADWARD = [[734, 522], [714, 560], [640, 570]];      // Jed, making for the road: round the far end of the glass, along its front
const BLOCK = [600, 568];              // where Grandpa Joe steps into his way (he goes along the front of the glass: nobody stands on it)
const SAT = [640, 570];                // where the banjo sits Jed down, in the dust (clear of the sagebrush in the corner)
// The limousine (PAINT-12A): two side frames, its foot the middle of the ground under its near side; at its stop, foot
// [345, 530] at 0.8 of its size, the body from x 108 to x 571 (its back end behind Mom's car, its base above hers).
const LIMO = { side: [ROAD + "limo-side-0.png", ROAD + "limo-side-1.png"], front: [ROAD + "limo-front-0.png", ROAD + "limo-front-1.png"],
  sideFoot: [438, 155], frontFoot: [294, 145] };
const STOP = [345, 530];
const sizeAt = (row) => (row - 290) / 300;                                           // the painter's rule: 1 on row 590
const LANE = [[139.4, 294.3], [129.1, 298.5], [111.7, 305.6], [84.5, 316.6]];         // the far road toward us (layout.json limo.front.lane), as far as it is clear of the sign's pole
const DOORS = [255, 307, 388, 439];    // the middles of its four doors on this side, at the stop, back to front
const OUT = 552;                       // the row the four of them step out to, in front of the car
const IN = 527;                        // a step behind the car's base: whoever stands there has got in
const INSIDE = 485;                    // Grandpa Joe, once in, as far as his words go: along the car, so that what he says is not across Jolene's face on the porch behind it
const TIE = [512, 566];                // where Grandpa Joe walks over to, to be tied up (in front of the car's front doors)
const LIFT = 7;                        // how far his boots are off the ground while two of them carry him
const JOLENE = [262, 452];             // Jolene on the porch, at the store's door (behind the limousine: she shows from the waist up)

// ---------- small things the script does again and again ----------
/** Someone becomes another figure from js/art/people.js (the same person at another moment), keeping his id, and his
    place and facing unless others are given. Made if he is not on the stage at all. */
function swap(g, id, kind, at = null, face = null) {
  const cast = g.view.cast, old = cast.get(id);
  const [x, y] = at || (old ? [old.x, old.y] : [400, 560]);
  const yaw = face ?? (old ? old.yaw : "S");
  if (old && old.kind === kind && !at && face == null) return old;
  const hid = old ? old.hidden : false, op = old ? old.opacity : 1;
  if (old && old.up && old.up.sprite) old.up.sprite = null;          // (a chair he got up out of stays where he left it: cast.remove would take it with him)
  if (old) cast.remove(id);
  const f = cast.addFigure(id, kind, x, y, scaleAt(g.scene, y)).face(yaw);
  f.hidden = hid; f.opacity = op;
  return f;
}
/** Walk someone through a list of points in a straight line from one to the next (a cut-scene's own way about, not the
    walk map's: behind the car, round the glass). `hurry`: at a run (Ranger scampers). */
function walk(g, id, points, { hurry = false } = {}) {
  const a = g.actor(id);
  if (!a || !points.length) return Promise.resolve();
  if (hurry) a.hurry = true;
  return a.walkPath(g.clock, points, (y) => scaleAt(g.scene, y));
}
/** Several people set off at once, their legs in step (one phase for all, as the backup walk: PEOPLE-12's note). */
function inStep(g, moves) {
  for (const [id] of moves) { const a = g.actor(id); if (a) a.phase = 0; }
  return Promise.all(moves.map(([id, points]) => walk(g, id, points)));
}
const face = (g, id, dir) => { const a = g.actor(id); if (a) a.face(dir); };
const look = (g, id, at) => { const a = g.actor(id), b = Array.isArray(at) ? null : g.actor(at); if (a) a.look(...(b ? [b.x, b.y] : at)); };
/** Getting in: a step back from the side of the car to behind its base, and gone (the car covers him; his head would
    show over the roof, so he is let go of as he goes). */
async function getIn(g, id) {
  const a = g.actor(id);
  if (!a) return;
  await Promise.all([walk(g, id, [[a.x, IN]]), g.tween(260, (k) => a.fade(1 - k))]);
  a.hidden = true;
}
/** Jolene's hat by the hour: the store's visits (the contract: the same rule as the store's). */
function jolenesKind(g) {
  const hat = ((Math.max(1, Number(g.flag("nevada.visits")) || 1) - 1) % 5) + 1;
  return hat === 1 ? "jolene" : "jolene-" + hat;
}
/** A little dust, kicked up at a place on the ground: a few soft puffs on the light layer (under the people: dust lies
    at their feet), spreading and fading. Nothing is drawn while the scene is being skipped. */
function dust(g, [x, y], k = 1, ms = 700) {
  const live = g.view.liveEl;
  if (!live || g.clock.skipping) return Promise.resolve();
  const SVG = "http://www.w3.org/2000/svg", puff = document.createElementNS(SVG, "g"), motes = [];
  puff.setAttribute("fill", "#e9d2a6");
  for (let n = 0; n < 7; n++) motes.push(puff.appendChild(document.createElementNS(SVG, "circle")));
  live.appendChild(puff);
  return g.tween(ms, (t) => {
    puff.setAttribute("opacity", 0.75 * (1 - t) * (1 - t));
    motes.forEach((m, n) => {
      const a = Math.PI * (0.05 + 0.9 * (n / 6)), r = (6 + 26 * t) * k;
      m.setAttribute("cx", x + Math.cos(a) * r * 1.4); m.setAttribute("cy", y - Math.sin(a) * r * 0.45 - 3 * k);
      m.setAttribute("r", (3 + 6 * t) * k);
    });
  }, g.ease.out).then(() => puff.remove());
}

/** A trail of dust behind something on the move (the limousine on the far road): a puff where it is now and then, each
    one growing, drifting back up the road and fading by itself, on the light layer (under the car). trail.at(x, y, k)
    says where the thing is and how big; trail.stop() lets the last puffs fade. Nothing while the scene is being skipped,
    or for less motion. */
function trail(g, every = 130, life = 1700) {
  const live = g.view.liveEl, SVG = "http://www.w3.org/2000/svg", puffs = [];
  let at = null, since = every, done = false, stop = null;
  const group = live && !g.clock.skipping && !g.calm ? live.appendChild(document.createElementNS(SVG, "g")) : null;
  if (group) {
    group.setAttribute("fill", "#ead6ad");
    stop = g.clock.every((dt) => {
      since += dt;
      if (!done && at && since >= every) { since = 0; puffs.push({ c: group.appendChild(document.createElementNS(SVG, "circle")), x: at[0], y: at[1], k: at[2], t: 0 }); }
      for (const p of [...puffs]) {
        p.t += dt;
        const u = p.t / life;
        if (u >= 1) { p.c.remove(); puffs.splice(puffs.indexOf(p), 1); continue; }
        p.c.setAttribute("cx", p.x + 110 * p.k * u); p.c.setAttribute("cy", p.y - 24 * p.k - 70 * p.k * u);
        p.c.setAttribute("r", p.k * (46 + 120 * u)); p.c.setAttribute("opacity", 0.75 * (1 - u) * (1 - u));
      }
      if (done && !puffs.length) { stop(); group.remove(); }
    });
  }
  return { at(x, y, k) { at = [x, y, k]; }, stop() { done = true; } };
}

// ---------- the stage as #13 leaves it ----------
/** Dress the stage from the facts, whatever is on it: the family gone through, Grandpa Joe holding the sun shade with the
    cut-out showing, his chair on the porch, Ranger beside it in his shades, Jed along the fence, the door open wide. */
async function ready(g) {
  const cast = g.view.cast;
  for (const id of FAMILY) { const a = g.actor(id); if (a) { a.hidden = true; a.fade(0); } }
  // His rocking chair stays on the porch while he is up (Figure.sit leaves it there as "<id>.seat"); if nobody left it
  // there, it is put there now, as it stands when he sits in it.
  if (![...cast.items.values()].some((s) => s instanceof Seat && s.kind === "grandpajoe")) {
    const k = scaleAt(g.scene, ROCKER[1]);
    cast.add(new Seat("grandpajoe.seat", "grandpajoe", people.grandpajoe, 45, Math.max(10, Math.round((160 * people.grandpajoe.height * k) / 2) * 2)).place(ROCKER[0], ROCKER[1], k));
  }
  swap(g, "grandpajoe", "grandpajoe-shade", HOLD, "E");
  const shade = g.plane("shade-held") || cast.addPicture("shade-held", { src: ROAD + "shade-held.png", base: 561 });
  shade.show(true);
  let r = g.actor("ranger");
  if (!r) { r = cast.addFigure("ranger", "ranger", PORCH[0], PORCH[1], scaleAt(g.scene, PORCH[1])).face("SE"); r.sit(true, true); }
  if (r.variant) r.variant("shades");                                  // (he has traded for them by now: #10)
  if (!g.actor("agent")) cast.addFigure("agent", "agent", FENCE[0], FENCE[1], scaleAt(g.scene, FENCE[1])).face("E");
  if (typeof g.scene.door === "function") await g.scene.door(g, "wide");
  await cast.load();
}

// ---------- the limousine ----------
/** It comes down the far road toward us, small (the nose-on frames), and turns off it; then along the front of the lot
    from the left edge (the side frames, its wheels turning), slowing to its stop in front of the porch. */
async function driveIn(g) {
  const cast = g.view.cast;
  const front = cast.addPicture("limo-front", { frames: LIMO.front, fps: 8, foot: LIMO.frontFoot }, LANE[0][0], LANE[0][1], sizeAt(LANE[0][1]));
  const side = cast.addPicture("limo", { frames: LIMO.side, fps: 8, foot: LIMO.sideFoot }, -260, STOP[1], sizeAt(STOP[1]));
  side.show(false);
  await cast.load();
  const along = (k) => {                                               // a point k of the way down the far road, and its size
    const n = LANE.length - 1, i = Math.min(n - 1, Math.floor(k * n)), t = k * n - i, [a, b] = [LANE[i], LANE[i + 1]];
    const x = a[0] + (b[0] - a[0]) * t, y = a[1] + (b[1] - a[1]) * t;
    return [x, y, sizeAt(y)];
  };
  const dusty = trail(g);                                               // dust on the road
  await g.tween(3400, (k) => { const [x, y, s] = along(k); front.place(x, y, s); dusty.at(x, y, s); }, g.ease.in);
  dusty.stop();
  await g.tween(240, (k) => front.fade(1 - k));                       // (off the road, behind the sign: out of sight)
  front.show(false);
  await g.wait(500);
  side.show(true);
  await g.tween(3400, (k) => side.place(-260 + (STOP[0] + 260) * k, STOP[1], sizeAt(STOP[1])), g.ease.out);
  side.flag("still", true);                                            // (stopped: its wheels too)
  await dust(g, [STOP[0] + 150, STOP[1] + 2], 1.4, 900);          // (at its front wheels: the back ones are behind Mom's car)
  return side;
}

/** It turns (the nose-on frame, a moment, and then the side frames the other way round: Cutout's "mirror") and goes out
    the way it came, off the left edge. Grandpa Joe, inside, goes with it (his words are over the car). */
async function driveOut(g, side, joe, during) {
  const cast = g.view.cast, front = cast.get("limo-front");
  const row = STOP[1], k = sizeAt(row);
  // The turn: from the side, to facing us, to the other side.
  side.flag("still", false);
  await g.tween(380, (t) => side.place(STOP[0] + 14 * t, row, k), g.ease.inOut);
  side.show(false);
  if (front) { front.show(true); front.fade(1); front.place(STOP[0] + 14, row + 2, k); }
  await g.wait(260);
  if (front) front.show(false);
  side.flag("mirror", true).show(true);
  side.place(STOP[0] + 14, row, k);
  if (joe) joe.place(STOP[0] + 14 + INSIDE - STOP[0], IN, scaleAt(g.scene, IN));
  const lines = during ? during() : Promise.resolve();
  await g.wait(400);
  await g.tween(3000, (t) => {
    const x = STOP[0] + 14 - (STOP[0] + 14 + 300) * t;
    side.place(x, row, k);
    if (joe) joe.place(x + INSIDE - STOP[0], IN, scaleAt(g.scene, IN));
  }, g.ease.in);
  side.show(false);
  await lines;
}

// ---------- out back: the hens, through the store's back door ----------
// The store's own pictures (PAINT-12B: art/scenes/nevada-store/), drawn close on the close-up layer over the lot for a
// moment, two and a half times their size, the back door in the middle: the five hens in the doorway turn round, all together, and look
// the way the limousine has gone; then turn back to the fence. (Through the doorway the hens are a finger high at the
// store's own size, too small to see turn: so the look is drawn close, and nobody has to go anywhere. The store is as
// the family left it: Jolene out on the porch, her hat of the hour off its peg.) Their places and foot points are the
// painter's (hens.json); after #11 Darlene (1) and Charlene (2) are sitting and the other three still guarding.
const HENS = [[650, 341], [625, 337], [636, 334], [661, 337], [671, 340]];      // hens.json: Darlene, Charlene, Marlene, Arlene, Doreen
const HEN_FOOT = [16, 27];
const henFile = (n, state) => `${STORE}hen-${n}-${state}.png`;
const before = (n) => (n <= 2 ? "sit" : "guard-a");
async function hensWatch(g) {
  if (g.clock.skipping) return;
  const hat = ((Math.max(1, Number(g.flag("nevada.visits")) || 1) - 1) % 5) + 1;
  const flat = ["back.png", ...[1, 2, 3, 4, 5].filter((n) => n !== hat).map((n) => `hat-${n}.png`), "counter.png"];
  const files = [...flat.map((f) => STORE + f), STORE + "roller-0.png", STORE + "doorframe.png", STORE + "rockbins.png",
    ...HENS.flatMap((_, i) => [henFile(i + 1, before(i + 1)), henFile(i + 1, "turn")])];
  await Promise.all(files.map((f) => g.assets.picture(f)));
  const img = (file, x = 0, y = 0, w = 800, h = 600, id = "") => `<image${id ? ` id="${id}"` : ""} href="${g.assets.url(file)}" x="${x}" y="${y}" width="${w}" height="${h}" style="image-rendering:pixelated"/>`;
  const hens = HENS.map(([x, y], i) => img(henFile(i + 1, before(i + 1)), x - HEN_FOOT[0], y - HEN_FOOT[1], 32, 30, `hen-${i + 1}`)).join("");
  const markup = `<rect width="800" height="600" fill="#000"/><g transform="scale(2.5) translate(-470 -198)">${flat.map((f) => img(STORE + f)).join("")}${img(STORE + "roller-0.png", 525, 324, 26, 11)}${hens}${img(STORE + "doorframe.png")}${img(STORE + "rockbins.png")}</g>`;
  g.closeup(markup, "Out back of the store: five hens in the doorway", { grid: [800, 600] });
  const set = (state) => HENS.forEach((_, i) => {
    const el = g.closeEl.querySelector(`#hen-${i + 1}`);
    if (el) { el.setAttribute("href", g.assets.url(henFile(i + 1, state === "turn" ? "turn" : before(i + 1)))); el.setAttribute("data-state", state); }     // (data-state: for the tests, which cannot read a picture's state from its address)
  });
  await g.wait(700);
  set("turn");                                                         // all together: round, to look
  await g.wait(1900);
  set("back");                                                         // and back to the fence
  await g.wait(800);
  g.closeup();
}

// ---------- the cut-scene ----------
export default async function backup(g) {
  const d = g.store.data;
  await g.settle();
  await ready(g);
  const jed = () => g.actor("agent"), joe = () => g.actor("grandpajoe"), ranger = g.actor("ranger");
  if (g.fadeEl && Number(g.fadeEl.style.opacity || 0) > 0.5) await g.fade(0, 500);
  await g.wait(900);                                                   // the lot is quiet; the door stands open in his light

  // ---- 1. Jed turns round, sees the door, and walks up to it, slowly
  face(g, "agent", "W");
  await g.wait(700);
  await walk(g, "agent", [BY_DOOR[0]]);
  await g.wait(450);
  await walk(g, "agent", [BY_DOOR[1]]);
  face(g, "agent", "W");
  await g.wait(400);
  await g.say("nevada.backup.jed.1");

  // ---- 2. The shade comes down, and the door folds shut; the banjo
  const shade = g.plane("shade-held");
  if (shade) shade.show(false);
  swap(g, "grandpajoe", "grandpajoe-standing");                         // himself again, the banjo in his hand
  g.sfx("portal");
  if (typeof g.scene.door === "function") await g.scene.door(g, "shut", 900);
  look(g, "agent", "grandpajoe");                                      // Jed turns to him
  await g.wait(600);
  // Jed makes for the road; Grandpa Joe steps into his way. (Ranger, on the porch, sits up to see.)
  if (ranger && ranger.play) ranger.play(g.clock, "look", { ms: 2400 });
  await Promise.all([walk(g, "agent", ROADWARD), g.wait(500).then(() => walk(g, "grandpajoe", [BLOCK]))]);
  face(g, "agent", "W"); face(g, "grandpajoe", "E");
  await g.wait(300);
  await g.say("nevada.backup.joe.1");
  swap(g, "grandpajoe", "grandpajoe-swing");                            // up it goes
  await g.wait(520);
  g.sfx("twang");                                                      // and down: one twang, every string at once
  swap(g, "grandpajoe", "grandpajoe-broken");
  swap(g, "agent", "agent-collar", SAT, "S");                          // and Jed sits down in the dust, the hoop round his neck
  await dust(g, [SAT[0], SAT[1] + 2], 1.1);
  await g.wait(700);
  await g.say("nevada.backup.jed.2");
  await g.wait(500);

  // ---- 3. Dust on the road: the limousine
  const limo = await driveIn(g);
  await g.wait(500);
  g.sfx("latch");                                                      // four doors at once
  SUITS.forEach((id, i) => { g.view.cast.addFigure(id, id, DOORS[3 - i], IN - 3, scaleAt(g.scene, IN - 3)).face("S"); });
  await g.view.cast.load();
  await inStep(g, SUITS.map((id, i) => [id, [[DOORS[3 - i], OUT]]]));
  SUITS.forEach((id) => face(g, id, "S"));
  await g.wait(500);
  await g.say("nevada.backup.suit.1");
  face(g, "suit1", "SW"); await g.wait(350); face(g, "suit1", "SE"); await g.wait(350);
  for (const id of SUITS) look(g, id, SAT);                           // there he is
  await g.wait(900);
  // a pause, in which four men consult a clipboard (it is suit1's)
  for (const id of ["suit2", "suit3", "suit4"]) look(g, id, "suit1");
  face(g, "suit1", "SW");
  await g.wait(1400);
  for (const id of SUITS) look(g, id, "grandpajoe");
  await g.wait(400);

  // ---- 4. Come with us. Mind the hat.
  await g.say("nevada.backup.suit.2");
  face(g, "grandpajoe", "W");
  await g.say("nevada.backup.joe.2");
  await walk(g, "grandpajoe", [TIE]);                                  // he goes over to them himself
  // NEVADA-12F: still what is left of the banjo in his hand (it was `grandpajoe-standing`, which carries the whole banjo,
  // and showed it whole again from "Mind the hat." until he was tied); it goes when he is tied (`grandpajoe-tied`), as evidence
  swap(g, "grandpajoe", "grandpajoe-broken", null, "S");
  await g.say("nevada.backup.suit.3");
  // The four of them round him in a row, their backs to us, while they tie him up: it takes four of them, and saying sorry.
  const wall = [[TIE[0] - 46, TIE[1] + 12], [TIE[0] - 16, TIE[1] + 14], [TIE[0] + 14, TIE[1] + 14], [TIE[0] + 44, TIE[1] + 12]];
  await inStep(g, SUITS.map((id, i) => [id, [wall[i]]]));
  SUITS.forEach((id) => face(g, id, "N"));
  await g.say("nevada.backup.suit.4");
  swap(g, "grandpajoe", "grandpajoe-tied");
  await g.say("nevada.backup.suit.5", "nevada.backup.joe.3");
  // they step back: tied, with a bow
  await inStep(g, [["suit1", [[TIE[0] - 70, TIE[1] - 4]]], ["suit4", [[TIE[0] + 74, TIE[1] - 4]]], ["suit2", [[TIE[0] - 30, TIE[1]]]], ["suit3", [[TIE[0] + 32, TIE[1]]]]]);
  face(g, "suit1", "E"); face(g, "suit4", "W");
  face(g, "suit2", "W"); swap(g, "suit3", "suit3-carry", null, "W");      // (the one behind has his hands out to carry him; the one in front, his behind him)
  await g.say("nevada.backup.suit.6");
  // up he comes, between them
  swap(g, "grandpajoe", "grandpajoe-carried", [TIE[0], TIE[1] - LIFT], "W");
  await g.wait(250);

  // ---- the carry, to the back door, and in
  const carried = joe(), back = DOORS[1];
  const follow = () => { const a = g.actor("suit2"), b = g.actor("suit3"); if (a && b && carried) carried.place((a.x + b.x) / 2, (a.y + b.y) / 2 - LIFT, scaleAt(g.scene, (a.y + b.y) / 2)); };
  const stop = g.clock.every(follow);
  const carrying = inStep(g, [["suit2", [[back - 30, TIE[1]]]], ["suit3", [[back + 32, TIE[1]]]]]);
  await g.wait(500);
  await g.say("nevada.backup.joe.4");
  look(g, "suit1", "grandpajoe");
  await g.say("nevada.backup.suit.7");
  await carrying;
  follow(); stop();
  // in at the back door: he goes in, his hat last
  await Promise.all([g.tween(500, (k) => carried.place(back, TIE[1] - LIFT - (TIE[1] - IN) * k, scaleAt(g.scene, TIE[1] - (TIE[1] - IN) * k))), g.tween(500, (k) => carried.fade(1 - k * k))]);
  carried.hidden = true;
  swap(g, "suit3", "suit3", null, "S"); face(g, "suit2", "S");
  carried.place(INSIDE, IN, scaleAt(g.scene, IN));                     // (where his words come from now: the car, along from Jolene on the porch behind it)

  // ---- 5. Jolene, on the porch
  const jo = swap(g, "jolene", jolenesKind(g), [JOLENE[0], JOLENE[1] - 6], "S");
  jo.fade(0);
  await g.view.cast.load();
  await Promise.all([g.tween(400, (k) => jo.fade(k)), walk(g, "jolene", [JOLENE])]);
  face(g, "jolene", "SE");
  await g.say("nevada.backup.jolene.1", "nevada.backup.joe.5", "nevada.backup.jolene.2", "nevada.backup.joe.6");
  // Ranger: out from behind the car at a run, across the lot, and in at the last door as it shuts
  if (ranger) {
    ranger.sit(false, true);
    ranger.place(STOP[0] + 196, IN - 10, scaleAt(g.scene, IN - 10));          // (behind the car, coming from the porch)
    await walk(g, "ranger", [[STOP[0] + 248, 540], [STOP[0] + 218, OUT + 4], [back + 4, OUT + 4]], { hurry: true });
    await walk(g, "ranger", [[back, IN + 1]], { hurry: true });
    ranger.hidden = true;
  }
  g.sfx("latch");
  look(g, "suit3", [back, OUT + 8]);                                   // a suit looks down
  await g.say("nevada.backup.suit.8");
  look(g, "suit4", "suit3");
  await g.say("nevada.backup.suit.9");

  // ---- Jed, helped up, and put in the front; the lunch in the back
  await inStep(g, [["suit1", [[SAT[0] - 34, SAT[1] - 2]]], ["suit4", [[SAT[0] + 34, SAT[1] - 6]]]]);
  look(g, "suit1", "agent"); look(g, "suit4", "agent");
  const up = jed();
  if (up && up.sit) await up.sit(false);                               // up he gets, through a squat, the hoop still on
  look(g, "agent", "suit4");
  await g.say("nevada.backup.jed.3");
  await g.say("nevada.backup.suit.10");
  look(g, "agent", "suit1");
  await g.say("nevada.backup.jed.4");
  const front = DOORS[3];
  await Promise.all([walk(g, "agent", [[front, OUT]]), walk(g, "suit1", [[front + 30, OUT + 4]]), walk(g, "suit4", [[DOORS[2], OUT + 2]])]);
  await getIn(g, "agent");
  g.sfx("latch");
  await Promise.all([getIn(g, "suit4"), walk(g, "suit2", [[DOORS[0], OUT]]).then(() => getIn(g, "suit2")), walk(g, "suit3", [[back, OUT]]).then(() => getIn(g, "suit3"))]);
  await walk(g, "suit1", [[front, OUT]]);
  await getIn(g, "suit1");
  g.sfx("latch");
  await g.wait(600);

  // ---- 6. It turns, and goes out the way it came. Out of the window:
  await driveOut(g, limo, carried, async () => {
    await g.say("nevada.backup.joe.7");
    face(g, "jolene", "SW");
    await g.say("nevada.backup.jolene.3");
  });
  await g.wait(700);
  // Out back, the hens turn round to watch it go.
  await hensWatch(g);
  // Jolene, alone on the porch.
  face(g, "jolene", "S");
  await g.wait(700);
  await g.say("nevada.backup.jolene.4");
  face(g, "jolene", "N");
  await Promise.all([walk(g, "jolene", [[JOLENE[0], JOLENE[1] - 6]]), g.tween(500, (k) => jo.fade(1 - k))]);
  await g.wait(600);
  await g.fade(1, 900);
  await g.card(g.lines["nevada.backup.card"] ? g.lines["nevada.backup.card"][1] : "Meanwhile, in a limousine.", "", { plain: true, ms: 2600 });

  // ---- 7. The play goes to the new team, in the limousine (as an act hands over: backHome in rome-temple.js)
  g.flag("nevada.backup", true);
  for (const id of FAMILY) d.where[id] = null;                         // (through the door: in no scene of this game's, until the story says)
  d.act = 5;
  d.active = "grandpajoe";
  g.team(["grandpajoe", "ranger"]);
  // The skippable part ends here: whatever was skipped, the limousine's opening plays as itself (its own beat).
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.goto("nevada-limo", { via: "cut" });
}
