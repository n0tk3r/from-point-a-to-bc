// Act Four, the second of its three scenes: inside Grandpa Joe's store, the Last Stop, the same morning (NEVADA-12SB: new
// in round twelve; briefs/SCENES-12B.md). The camera stands just inside the front door and looks along the store: the
// front wall with the window and the door is on the left, the counter is in the middle with the hubcaps over it, Harold
// the cooler is in the far left corner, and the back door stands open on the right, with the hen yard beyond it.
// Grandma Jolene is behind the counter, under a different hat every time they come in.
//
// The three of them come in together from the lot (`party`), and each does what only she can:
//   Mom buys      the last pair of mirror shades off the spinner rack (#10: Big Sister trades them to Ranger on the
//                 porch), and three waters, "because we are going somewhere with no shops". We buy, girls.
//   Little Sister takes four pennies at the take-a-penny dish (it SAYS take a penny), and goes out of the back door to
//                 Jolene's hens (#11, Jolene's Girls): she stands in the row with them, sees that they are guarding,
//                 and tells them, one by one, by name, that they can stand down. Darlene sits; then Charlene; then an
//                 egg, in the dust. Jolene, in the doorway: the run of the store (`nevada.jolene`), and the egg is hers.
//   anyone        may ask Jolene for the sun shade in the window (#12's big shine): not for sale, not the window,
//                 sugar, until somebody has done something about her girls; after #11 it is given (`nevada.shadeGiven`).
// And #12's tries in the store, once the coin door is open: the hubcaps (Grandpa Joe, from the porch: a COLLECTION),
// the space blanket, the chrome polish. Everything else here is for character and nothing else, and each of the three
// has a word for each thing (js/content/lines/nevada.en.js, "THE STORE"; S/work-writer/ids.md part 1, "The store").
//
// Jolene's talk is a dialogue tree (`joleneTree` in js/content/talk/nevada.js), and so is #11 (`hensTree`). The scripts
// a branch needs are handed to the trees as hooks: `giveShade`, `phone`, `out`; and `row`, `sit`, `egg`, `giveEgg`.
//
// Every place below is measured from the finished painting (art/scenes/nevada-store/layout.json is the painter's own
// list), or set by eye against the picture with the people standing in it; where the two differ the comment says why.
//
// Try it: index.html?scene=nevada-store&lead=mom&flags=nevada.arrived
// Later states: &flags=nevada.arrived,nevada.witness,nevada.doorOpen (the tries of #12), nevada.jolene (after #11).

import { joleneTree, hensTree } from "../talk/nevada.js";

const art = "art/scenes/nevada-store/";

const THREE = ["mom", "bigsis", "lilsis"];
const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;
/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];

// ---------- the room, from its camera (layout.json: horizon 158, full 455) ----------
const HORIZON = 158, FULL = 455, MAX_SCALE = 1.17;      // (the floor's front edge is 1.16 by the camera: people there are not held smaller)
/** How big someone is with their feet at row y: as the engine has it (scaleAt in js/engine/walk.js), for a walk of Jolene's own. */
const sizeAt = (y) => Math.min(MAX_SCALE, Math.max(0.26, (y - HORIZON) / (FULL - HORIZON)));

// ---------- Jolene's hat: one a visit, round and round (SCENES-12: the rule everyone who draws her uses) ----------
// 1 a straw cowboy hat, 2 a sun hat with fruit, 3 a tiara, 4 a hard hat, 5 a hen. Today's is on her head and not on its
// peg (the five `hat-<n>` cut-outs on the board over the counter).
const visits = (g) => Number(g.flag("nevada.visits")) || 0;
const hatOf = (g) => ((Math.max(1, visits(g)) - 1) % 5) + 1;
const kindOf = (g) => (hatOf(g) === 1 ? "jolene" : `jolene-${hatOf(g)}`);

/** One of the scene's people as another state of herself, in the same place, facing the same way (as egypt-site.js does it). */
function redraw(g, id, kind) {
  const cast = g.view.cast, old = g.actor(id);
  if (!old || old.kind === kind) return;
  cast.remove(id);
  try { cast.addFigure(id, kind, old.x, old.y, old.scale).face(old.yaw); }
  catch { cast.add(old); }
}

// ---------- where people stand (layout.json: marks and stands) ----------
const JOLENE = [419, 377];             // marks.jolene: behind the counter, standing, facing S (the counter covers her below the waist)
const COUNTER = [385, 424];            // marks.counter: a customer at the counter, facing N (and the penny dish's place)
// Paying: Mom stands at the register's right-hand end, turned to Jolene. (The painter's place, stands.atregister [427, 428],
// is square in front of Jolene's mark, and whoever stands there hides her and the register both.)
// NEVADA-12F: at the counter on Jolene's other side, between the jar of eggs and the penny dish, turned to her (NE). At the
// register's right-hand end, [458, 431], Mom stood in front of the map rack (88% of it behind her); every place along the
// counter hides something, and this one least (an eighth of the jar), with Jolene, the register and the map rack clear.
const PAY = [366, 431];
const STEP = [610, 374];               // marks.step: Little Sister on the back step, in the doorway, facing N, the hens before her
// stands.watchleft, watchright: a grown-up watching from the doorway.
// NEVADA-12F: the right-hand one is in the corner past Jolene's chair, [738, 446]: on the painter's [695, 407] she stood in
// front of the chair (75% of it behind her), and a step to the left of the chair puts her in front of the hens.
const WATCH = { mom: [579, 397], bigsis: [738, 446], lilsis: [738, 446] };
// NEVADA-12F: where Mom steps back to as Jolene comes to the doorway (jolToDoor): a pace straight back from the doorway's
// left-hand side, which Jolene takes, so that Jolene stands just behind her. It was [548, 438], in front of the grill and the
// hot dog roller (88% of the roller behind her); here nothing is more than a tenth behind her.
const ASIDE = [578, 432];
// Jolene answering the pay phone: a step left of the painter's place (stands.atpayphone [679, 401]) and turned to it, so
// that her hand goes up to it, and not to the wall beside it.
const AT_PHONE = [670, 398];
const AT_SHADE = [232, 388];           // stands.atshade: at the sun shade in the window
// Jolene's way out from behind the counter. There is only one: Harold stands against the left end of the counter, and
// the right end, past the grill, has a yard of floor between it and the back wall. Behind the counter she is off the
// floor the family walks on, so she goes there and back in straight lines.
const BEHIND_GRILL = [549, 388];       // behind the grill, at the counter's right end (the counter still covers her below the waist)
const PAST_GRILL = [570, 400];         // out past the end of the counter, on the floor in front of the back door

// ---------- the hens, through the back door (layout.json: hens) ----------
// Five small cut-outs, painted at the size they show there and never scaled, each laid with her foot point on her
// place and sorted by her row like a person: behind the door's frame, and behind anyone on the step. They stand with
// their backs to us, facing the fence, guarding: now and then one turns her head a little (`guard-b`). After #11 Darlene
// and Charlene sit; the other three keep guarding, and peck now and then. While the fact `nevada.hensWatch` is true
// (the cut-scene "Backup" may cut here to show it) all five have turned round to watch the limousine go.
const HENS = [
  { n: 1, name: "Darlene", at: [650, 341] },
  { n: 2, name: "Charlene", at: [625, 337] },
  { n: 3, name: "Marlene", at: [636, 334] },
  { n: 4, name: "Arlene", at: [661, 337] },
  { n: 5, name: "Doreen", at: [671, 340] },            // the small one
];
const HEN_FOOT = [16, 27];
const EGG = { at: [647, 342], foot: [4, 5] };         // in the dust, where Darlene sits (painted a little bigger than life, so that it reads)
// What the hens are doing now that the story's facts do not say: during #11 (a turn of the head toward her when she says
// a name, sitting down, getting up to lay), and their small movements on the game clock (`henLife`, below). None of it
// is saved: #11 is one script from first word to last, and `setup` clears it whenever the scene is built.
const hen = { pose: {}, sat: new Set(), twitch: {}, egg: false, clock: null, jolene: null };
function henState(g, n) {
  if (g.flag("nevada.hensWatch")) return "turn";
  if (hen.pose[n]) return hen.pose[n];
  if (hen.sat.has(n) || (n <= 2 && g.flag("nevada.jolene"))) return "sit";
  return hen.twitch[n] || "guard-a";
}
/** The hens and the egg read the story again (they are cut-outs: their `state` and `when` say what they show). */
const henRedo = (g) => { for (const c of g.view.cast.cutouts()) if (/^hen-|^egg$/.test(c.id)) c.refresh(g); };

/** The hens' small movements: every few seconds one of those still on guard turns her head a little and back; after
    #11 the three on guard also peck at the dust now and then. On the game clock, so they stop with the menu. */
function henLife(g) {
  if (hen.clock) hen.clock();
  const scene = g.scene, clock = g.clock;
  let next = clock.now + 2500, back = 0, busy = 0, step = 0;
  const pick = (k) => Math.floor(((Math.sin((clock.now + k) * 12.9898) * 43758.5453) % 1 + 1) % 1 * 1000);    // (a number from the time: enough for a hen)
  hen.clock = clock.every((dt, now) => {
    if (g.scene !== scene) { hen.clock(); hen.clock = null; return; }
    if (busy && now >= back) {
      hen.twitch[busy] = step > 0 ? hen.twitch[busy] : null;
      if (step > 0) { hen.twitch[busy] = hen.twitch[busy] === "peck" ? "guard-a" : "peck"; step--; back = now + 260; }
      else { busy = 0; next = now + 1800 + pick(7) * 3.6; }
      henRedo(g);
      return;
    }
    if (busy || now < next || !g.life.enabled || g.flag("nevada.hensWatch")) return;
    const free = HENS.map((h) => h.n).filter((n) => henState(g, n) === "guard-a" && !hen.pose[n]);
    if (!free.length) { next = now + 3000; return; }
    busy = free[pick(3) % free.length];
    const peck = !!g.flag("nevada.jolene") && pick(5) % 3 > 0;
    hen.twitch[busy] = peck ? "peck" : "guard-b";
    step = peck ? (pick(9) % 2) * 2 : 0;                  // a peck, or two
    back = now + (peck ? 280 : 650 + pick(11) * 0.5);
    henRedo(g);
  });
}

// ---------- Jolene goes somewhere: her errands from behind the counter ----------
/** Walk Jolene along a list of points, in straight lines. */
async function jolMove(g, points) {
  const j = g.actor("jolene");
  if (!j) return;
  await j.walkPath(g.clock, points, sizeAt);
}
/** Is she behind the counter (between its back edge, from [299, 380] to [555, 398], and the back wall)? */
const behind = (j) => j.x > 295 && j.x < 560 && j.y < 380 + ((j.x - 299) * 18) / 256 + 2;
/** Out from behind the counter and across the floor to a place, round whatever is in the way (the family included). */
async function jolOut(g, to) {
  const j = g.actor("jolene");
  if (!j) return;
  if (behind(j)) await jolMove(g, [BEHIND_GRILL, PAST_GRILL]);
  const map = g.groundFor("jolene");
  await jolMove(g, map.path([j.x, j.y], to));
}
/** Back behind the counter to her mark, the way she came: across the floor to the end of the counter, and behind it. */
async function jolHome(g) {
  const j = g.actor("jolene");
  if (!j) return;
  if (Math.abs(j.x - JOLENE[0]) <= 2 && Math.abs(j.y - JOLENE[1]) <= 2) return j.face("S");
  if (!behind(j)) {
    const map = g.groundFor("jolene");
    await jolMove(g, map.path([j.x, j.y], PAST_GRILL));
    await jolMove(g, [PAST_GRILL, BEHIND_GRILL]);
  }
  await jolMove(g, [JOLENE]);
  j.face("S");
}
/** Jolene says something to whoever is being played: she turns to them first (and stays turned to them, as a shopkeeper
    does, until her own life or a script turns her again). */
async function jolSay(g, ...ids) {
  const j = g.actor("jolene"), me = g.lead;
  if (!j) return;
  if (me) j.look(me.x, me.y);
  await g.say(...ids);
}

// ---------- the front door, and Bernice the bell over it ----------
async function goOut(g) {
  g.sfx("beep");                                             // Bernice
  // (MAP-15: they are not inside any more, so the next time they come in is a new visit: `leaving`, below, which runs
  // however they leave, by the door or by the map)
  await g.goto("nevada-roadside", { spawn: "fromStore" });
}

// ---------- buying: Mom pays (decision 9). We buy, girls. We do not borrow. ----------
/** The register rings: for Jolene, and nobody else. */
async function ring(g) {
  const j = g.actor("jolene");
  if (j) { j.face("S"); await j.play(g.clock, "reach"); }
  g.sfx("beep");
  await g.wait(350);
}
async function buyShades(g) {
  await g.say("nevada.buy.shades.mom");
  await g.reach();
  const pair = g.plane("mirror-shades");
  if (pair) pair.show(false);                                // off the hook and into her hand
  await g.walkTo(PAY[0], PAY[1]);
  g.lead.face("NE");                                         // NEVADA-12F: to Jolene (PAY is on her other side now)
  await jolSay(g, "nevada.buy.shades.jolene");
  await g.reach();                                           // she pays: three dollars and ninety-nine cents
  await ring(g);
  await g.say("nevada.buy.ring");
  g.give("mirrorshades");
  g.flag("nevada.shadesBought", true);
}
async function buyWaters(g) {
  await g.reach();                                           // three bottles off the shelf
  await g.walkTo(PAY[0], PAY[1]);
  g.lead.face("NE");                                         // NEVADA-12F: to Jolene
  await g.say("nevada.buy.waters.mom");
  await jolSay(g, "nevada.buy.waters.jolene");
  await g.reach();
  await ring(g);
  g.give("waters");
  g.flag("nevada.waters", true);
}

// ---------- the spinner rack: one pair of mirror shades left ----------
const spinnerLook = (g) => g.say(`nevada.store.${g.flag("nevada.shadesBought") ? "spinner2" : "spinner"}.${who(g)}`);
async function useSpinner(g) {
  const me = who(g);
  if (g.flag("nevada.shadesBought")) return spinnerLook(g);
  if (me === "mom") return buyShades(g);
  return g.say(`nevada.store.spinner.use.${me}`);            // Big Sister has no money; Little Sister knows who buys things
}

// ---------- the survival shelf: Mom buys three waters; and #12's try, the space blanket ----------
/** #12 is open: the coin door is the size of a coin, and they are looking for something that shines like a car. */
const seeking = (g) => !!g.flag("nevada.doorOpen") && !g.flag("nevada.wideOpen");
async function blanket(g) {
  await g.say("nevada.shade.blanket.bigsis", "nevada.shade.blanket.mom");
}
async function useSurvival(g) {
  const me = who(g);
  if (me === "mom" && !g.flag("nevada.waters")) return buyWaters(g);
  if (seeking(g) && !heard(g, "nevada.shade.blanket.mom")) return blanket(g);
  if (me === "mom") return g.say("nevada.buy.again.mom");
  return g.say(`nevada.store.survival.${me}`);
}

// ---------- the auto shelf: the family squeegee; and #12's try, the chrome polish from 1987 ----------
async function useAuto(g) {
  if (seeking(g) && !heard(g, "nevada.shade.polish.mom")) return g.say("nevada.shade.polish.bigsis", "nevada.shade.polish.mom");
  return lookAt("nevada.store.auto", "nevada.jolene.squeegee")(g);
}

// ---------- the hubcap wall: #12's try. Grandpa Joe says no from the porch, through the window ----------
async function useHubcaps(g) {
  if (!seeking(g) || heard(g, "nevada.shade.hubcaps.bigsis")) return lookAt("nevada.store.hubcaps", "nevada.jolene.hubcaps")(g);
  await g.say(who(g) === "mom" ? "nevada.shade.hubcaps.joe" : "nevada.shade.hubcaps.joe.girls");    // (he is on the porch: his words come in through the window)
  await jolSay(g, "nevada.jolene.hubcaps");
  await g.say("nevada.shade.hubcaps.bigsis");                // one hubcap's worth of shine: nobody tries it twice
}

// ---------- the take-a-penny dish (#10's wrong try): four pennies, and Ranger does not want copper ----------
async function takePennies(g) {
  if (g.flag("nevada.pennies")) return g.say("nevada.store.pennydish.again");
  await g.reach();
  await g.say("nevada.store.pennydish.lilsis.1");
  const big = g.actor("bigsis"), lil = g.lead;
  if (big) big.look(lil.x, lil.y);
  await g.say("nevada.store.pennydish.bigsis.2", "nevada.store.pennydish.lilsis.2");
  for (let n = 0; n < 3; n++) { const hand = g.reach(); await g.wait(260); g.sfx("key"); await hand; }   // one at a time: A LOT of times
  await g.say("nevada.store.pennydish.lilsis.3");
  g.give("penny");                                           // one for luck (it goes through the coin door to her brother)
  g.give("pennies");                                         // and three she will not give to anybody
  g.flag("nevada.pennies", true);
}

// ---------- the register: it rings for Jolene and for nobody else ----------
async function useRegister(g) {
  const me = who(g);
  if (me === "lilsis") {                                     // she presses ALL the buttons
    const hand = g.reach();
    for (let n = 0; n < 4; n++) { await g.wait(150); g.sfx("key"); }
    await hand;
  }
  await g.say(`nevada.store.register.use.${me}`);
  await jolSay(g, "nevada.jolene.register");
}

// ---------- looks, and Jolene's word ----------
/** A look of each of the three's own (`<id>.<who>`), and Jolene's word on the thing, the first time anybody looks:
    she does not say the same thing twice. */
const lookAt = (id, ...hers) => async (g) => {
  await g.say(`${id}.${who(g)}`);
  if (hers.length && !heard(g, hers[0]) && g.actor("jolene")) await jolSay(g, ...hers);
};
/** The hat rack: today's hats, and a gap where the hat she has on lives. Little Sister notices every time (a word for
    each hat); Big Sister refuses to, and then does not mention it; Mom sees a plan. Jolene has a word for the plan. */
async function hatsLook(g) {
  const me = who(g);
  if (me === "bigsis") return g.say(heard(g, "nevada.store.hats.bigsis") ? "nevada.store.hats.bigsis.2" : "nevada.store.hats.bigsis");
  await g.say(me === "lilsis" ? `nevada.store.hats.lilsis.${hatOf(g)}` : "nevada.store.hats.mom");
  if (!heard(g, "nevada.jolene.hats") && g.actor("jolene")) await jolSay(g, "nevada.jolene.hats");
}
/** The pickled eggs. Little Sister asks the one question, once; Jolene answers it; and that is all the questions. */
async function eggsLook(g) {
  const me = who(g);
  if (me !== "lilsis") return g.say(`nevada.store.eggs.${me}`);
  if (heard(g, "nevada.jolene.eggs.lilsis")) return g.say("nevada.store.eggs.lilsis.2");
  await g.say("nevada.store.eggs.lilsis");
  await jolSay(g, "nevada.jolene.eggs.lilsis");
  await g.say("nevada.store.eggs.lilsis.2");
}
/** Jolene's chair, and the very small sweater on it. Each of the girls asks who it is for, once. */
async function chairLook(g) {
  const me = who(g);
  if (me === "mom") return g.say("nevada.store.chair.mom");
  if (heard(g, `nevada.store.chair.${me}`)) return g.say(`nevada.store.chair.${me}.2`);
  await g.say(`nevada.store.chair.${me}`);
  await jolSay(g, "nevada.jolene.chair");
  await g.say(`nevada.store.chair.${me}.2`);
}
/** The front door. Little Sister rings the bell, more than once. Jolene has named it. */
async function doorLook(g) {
  if (who(g) === "lilsis") { g.sfx("beep"); await g.wait(250); }
  await lookAt("nevada.store.door", "nevada.jolene.bell")(g);
}
/** The window, and once the shade is given, the empty window. */
const windowLook = (g) => g.say(`nevada.store.${g.flag("nevada.shadeGiven") ? "window2" : "window"}.${who(g)}`);
/** The back door: the hens in a row, and Mom sees what they are looking at. After #11: two sitting, three on guard. */
async function backdoorLook(g) {
  const me = who(g);
  if (g.flag("nevada.jolene")) return g.say(`nevada.store.backdoor2.${me}`);
  if (me === "mom") return g.say("nevada.store.backdoor.mom", "nevada.store.backdoor.mom.2");
  return g.say(`nevada.store.backdoor.${me}`);
}

// ---------- the sun shade in the window: DISPLAY ONLY, until somebody does something about her girls ----------
const ASK = { mom: ["nevada.jolene.opt.window.mom", "windowMom"], bigsis: ["nevada.jolene.opt.window.big", "windowBig"], lilsis: ["nevada.jolene.opt.window.lil", "windowLil"] };
/** Asked for at the window itself: the same question as in her talk (the tree's `windowAsk` and `windowGive`), with the
    same answers, and counted with it (the tree's memory of that question, `jolene/windowMom` and so on), so that asking
    here or across the counter goes on from where it got to. Not for sale: a store with an empty window is a shed;
    anything but the window; do somethin' about my girls. After #11 she gives it. */
async function askShade(g) {
  if (g.flag("nevada.shadeGiven")) return windowLook(g);
  const [line, option] = ASK[who(g)], asked = g.store.data.asked || (g.store.data.asked = {}), key = `jolene/${option}`;
  await g.say(line);
  if (g.flag("nevada.jolene")) {
    await jolSay(g, "nevada.jolene.window.give");
    g.flag("nevada.shadeGiven", true);
    return giveShade(g);
  }
  const n = (asked[key] = (asked[key] || 0) + 1);
  await jolSay(g, n === 1 ? "nevada.jolene.window.1" : n === 2 ? "nevada.jolene.window.2" : "nevada.jolene.window.3");
}
/** The hook `giveShade`: she comes out from behind the counter, lifts the sun shade out of her window and puts it in the
    hands of whoever asked. (The fact is set already, and the window is empty by the story: the shade is there by hand
    until she lifts it out.) Then Mom has the line about the one their father bought. */
async function giveShade(g) {
  const shade = g.plane("window-shade"), me = g.lead, j = g.actor("jolene");
  if (shade) shade.show(true);
  if (!j || !me) { if (shade) shade.show(false); g.give("storeshade"); return; }
  // The one who asked goes to meet her at the window.
  const meet = [AT_SHADE[0] + 52, AT_SHADE[1] + 22];
  await Promise.all([jolOut(g, AT_SHADE), g.walkTo(meet[0], meet[1])]);
  j.face("W");
  me.look(j.x, j.y);
  await j.play(g.clock, "reach");                            // up into the window, and out it comes
  if (shade) shade.show(false);
  j.look(me.x, me.y);
  await g.wait(200);
  await g.reach();
  g.give("storeshade");
  await Promise.all([jolHome(g), g.say("nevada.shade.mom.1", "nevada.shade.bigsis.1", "nevada.shade.mom.2")]);
}

// ---------- the pay phone: dead since the eighties, and she answers it ----------
/** She goes to the pay phone, takes the receiver off its hook, answers it, and hangs it up: "Keeps it hopeful." (The tree
    says her two lines and then calls the hook `phone`; the scene hands it a tree whose phone answers say them here,
    at the phone, in the same order: see JOLENE_TREE below.) */
async function answerPhone(g) {
  const j = g.actor("jolene");
  if (!j) return;
  await jolOut(g, AT_PHONE);
  j.face("NE");
  await j.play(g.clock, "reach");
  j.hold(true);                                              // the receiver at her ear
  await g.say("nevada.jolene.phone.1");
  j.hold(false);
  await g.wait(250);
  await g.say("nevada.jolene.phone.2");
  await jolHome(g);
}

// ---------- #11, Jolene's Girls: Little Sister on the back step, the hens before her ----------
/** Little Sister goes out of the back door onto the step; the first time, the other two come to the doorway to watch,
    and Jolene calls the hens' names after her (she gave them to her at the door). */
async function toStep(g) {
  const lil = g.lead, first = !g.flag("nevada.jolene");
  // (after #11 the other two stay where they are, unless one of them is standing on the step herself)
  const others = THREE.filter((id) => id !== "lilsis").map((id) => g.actor(id)).filter((a) => a && (first || Math.hypot(a.x - STEP[0], a.y - STEP[1]) < 30));
  await Promise.all([g.walkTo(STEP[0], STEP[1]), ...others.map((a) => g.walkTo(WATCH[a.id][0], WATCH[a.id][1], a.id).then(() => a.look(STEP[0], STEP[1] - 20)))]);
  lil.face("N");
  if (!heard(g, "nevada.jolene.names") && g.actor("jolene")) {
    g.actor("jolene").look(STEP[0], STEP[1]);
    await g.say("nevada.jolene.names");
  }
}
const henShow = async (g, n, pose, ms) => { hen.pose[n] = pose; henRedo(g); await g.wait(ms); };
/** Jolene comes to the doorway to see: out from behind the counter at its end, and as she comes out Mom steps back a
    pace to make room for her (NEVADA-12F: straight back, to ASIDE: it is the doorway's left-hand side that Jolene takes). */
async function jolToDoor(g) {
  const mom = g.actor("mom"), j = g.actor("jolene");
  if (!j) return;
  await jolMove(g, [BEHIND_GRILL]);
  const aside = mom && Math.hypot(mom.x - WATCH.mom[0], mom.y - WATCH.mom[1]) < 20 ? g.walkTo(ASIDE[0], ASIDE[1], "mom").then(() => mom.look(STEP[0], STEP[1] - 20)) : null;      // NEVADA-12F: ASIDE (was [548, 438])
  await jolOut(g, WATCH.mom);
  j.look(STEP[0] + 20, STEP[1] - 30);
  await aside;
}
const HENS_TREE = hensTree({
  // she stands in the row with them (the row is the step), and looks where they look: the fence, the Hummy Place
  row: async (g) => { g.lead.face("N"); await g.wait(600); },
  // a hen hears her name, looks round at her, and sits down: still facing the fence, but standing down
  sit: async (g, n) => {
    if (n === 1 && !hen.jolene) hen.jolene = jolToDoor(g);        // (Jolene sees her girls sit, and comes to look)
    await henShow(g, n, "turn", 700);
    hen.pose[n] = null; hen.sat.add(n); henRedo(g);
    await g.wait(450);
  },
  // Darlene gets up, and there is an egg in the dust; she looks round at it, and sits down again behind it
  egg: async (g) => {
    if (hen.jolene) await hen.jolene;
    hen.sat.delete(1);
    await henShow(g, 1, "guard-a", 450);
    hen.egg = true; henRedo(g); g.sfx("found");
    await henShow(g, 1, "turn", 700);
    hen.pose[1] = null; hen.sat.add(1); henRedo(g);
    await g.wait(300);
  },
  // the egg is hers to carry: she hops down into the yard for it, and back up onto the step
  giveEgg: async (g) => {
    const lil = g.lead, up = [STEP[0], STEP[1]];
    await g.moveTo(628, 349);
    lil.face("E");
    await g.reach(true);
    hen.egg = false; henRedo(g);
    g.give("egg");
    await g.moveTo(up[0], up[1]);
    lil.face("S");
  },
});
/** Out to the hens, and #11 (or, after it, a word with them). Then Jolene goes back behind her counter. */
async function hens(g) {
  hen.jolene = null;
  await toStep(g);
  await g.talk(HENS_TREE);
  if (hen.jolene) { await hen.jolene; hen.jolene = null; await jolHome(g); }
}
async function useBackdoor(g) {
  const me = who(g);
  if (me === "lilsis") return hens(g);
  return g.say(`nevada.hens.door.${me}`);                    // the other two will not go out: they observe from the doorway
}

// ---------- Jolene: her talk ----------
/** The tree, with the scene's hooks. The hook `out` sends Little Sister out to the hens; the talk with Jolene then ends,
    and the hens' begins (so the two talks are one after the other, not one inside the other). */
let toHens = false;
const JOLENE_TREE = (() => {
  const tree = joleneTree({ giveShade, phone: answerPhone, out: async () => { toHens = true; } });
  // Her answer to the pay phone is said at the phone, with the receiver at her ear: the tree has her two lines and then
  // the hook, so here the lines go into the hook (answerPhone says them, in the same order, once).
  const PHONE = ["nevada.jolene.phone.1", "nevada.jolene.phone.2"];
  for (const node of Object.values(tree.nodes)) for (const o of node.options || [])
    if (Array.isArray(o.say) && o.say.join() === PHONE.join() && o.do === answerPhone) delete o.say;
  return tree;
})();
async function talkToJolene(g) {
  const j = g.actor("jolene");
  if (!j) return;
  j.look(g.lead.x, g.lead.y);
  toHens = false;
  await g.talk(JOLENE_TREE);
  j.face("S");
  if (toHens) { toHens = false; await hens(g); }
}

// ---------- handing things about ----------
/** Little Sister will not give up the egg ("It's WARM. It's MINE to keep warm.") or the three pennies: what she hands
    over comes straight back. (The lucky penny she may hand to anybody.) */
async function given(g, item, to, from) {
  if (from !== "lilsis" || (item !== "egg" && item !== "pennies")) return;
  const pockets = g.store.data.inventory, i = pockets[to].indexOf(item);
  if (i >= 0) { pockets[to].splice(i, 1); if (!pockets.lilsis.includes(item)) pockets.lilsis.push(item); g.store.emit(); }
  if (!g.clock.skipping) g.ui.toast(`Little Sister keeps ${g.the(item)}`);
  await g.say(item === "egg" ? "nevada.egg.keep" : "nevada.pennies.keep");
}

// The cut-outs' bases and solids (layout.json `planes`).
const COUNTER_BASE = [[281, 396], [556, 417]];
const SPINNER_BASE = [[182, 425], [218, 428]];

export default {
  id: "nevada-store",
  era: "nevada",
  name: "Grandpa Joe's store",
  // MAP-15: as they leave, by the front door or by the map, they are not inside any more: the next time in is a new visit (`setup`)
  leaving(g) { g.flag("nevada.inStore", false); },
  travel: (g) => !g.flag("nevada.left"),                   // MAP-15: not by the map once the act has ended (whatever a save catches it in)

  // DEPTH, from the room's camera (layout.json: `room.View`, the eye 325 cm up, as the house's rooms are painted).
  horizon: HORIZON, full: FULL, maxScale: MAX_SCALE,

  // The floor: in front of the counter and round the room, through the back doorway onto the step (the step is at
  // floor height; the yard is a step down and is not walked on), and to the front door's threshold at the left edge.
  // It keeps 14 px off the walls, and its front edge keeps people under about 190 px.
  walk: { area: [[226, 374], [296, 379], [270, 402], [556, 425], [555, 392], [604, 395], [598, 370], [663, 375], [677, 400], [711, 402], [744, 452], [557, 436], [558, 474], [773, 494], [779, 502], [685, 502], [588, 502], [469, 502], [360, 502], [252, 503], [143, 502], [46, 502], [1, 499], [75, 453], [104, 456]] },
  // The spinner rack's foot, the one thing standing inside the floor. (Harold, the counter, the rock bins and the spinner
  // itself also give their footprints as `solid`, below.)
  blocked: [[[232, 421], [221, 426], [205, 429], [191, 427], [184, 423], [187, 417], [198, 412], [213, 410], [227, 411], [234, 415]]],

  // The three of them come in together from the lot, and go out together (a party). Once they have gone through the
  // door in time (`nevada.left`), only a cut-scene brings the stage here, and nobody comes with it.
  party: (g) => (g.flag("nevada.left") ? null : THREE),
  // Just inside the front door, a step apart, nobody in front of anyone's face (layout.json marks.fromLot): whoever leads
  // on Mom's mark, the other two on the others in turn.
  // NEVADA-12F: the second place (Big Sister's, when Mom leads) is a step to the right of the painter's [318, 471], where
  // whoever came in second stood in front of Ranger's basket under the counter (79% of it behind her).
  spawn: { default: [244, 447], mom: [244, 447], bigsis: [360, 475], lilsis: [142, 460], fromLot: [244, 447] },
  arrive: { fromLot: [[360, 475], [142, 460]] },
  facing: "NE",                                              // looking into the store, at the counter
  exits: ["nevada-roadside"],
  // No ways out across the edges of the picture: the front door is a door in the wall (the area `door`, below).

  picture: art + "back.png",

  // CUT-OUTS, in the painter's order (layout.json `planes`), with the things that move and the hens laid among them.
  planes: [
    // Jolene's hats on their pegs over the counter: today's is on her head and not on its peg.
    ...[1, 2, 3, 4, 5].map((n) => ({ id: `hat-${n}`, src: art + `hat-${n}.png`, plane: "back", when: (g) => hatOf(g) !== n })),
    // the TV's snow: rabbit ears, one channel (it is on top of the survival shelf, against the far wall)
    { id: "tv", frames: [art + "tv-0.png", art + "tv-1.png", art + "tv-2.png"], fps: 6, at: [227, 252], foot: [9, 17], plane: "back" },
    // the sun shade in the far sash of the window, DISPLAY ONLY, until it is given (the window is painted complete under it)
    { id: "window-shade", src: art + "window-shade.png", plane: "back", when: (g) => !g.flag("nevada.shadeGiven") },
    // the hens, out in the yard (each sorted by her own row: behind the door's frame and anyone on the step), and the egg
    ...HENS.map(({ n, at }) => ({
      id: `hen-${n}`, at, foot: HEN_FOOT, state: (g) => henState(g, n),
      states: Object.fromEntries(["guard-a", "guard-b", "turn", "sit", "peck"].map((s) => [s, art + `hen-${n}-${s}.png`])),
    })),
    { id: "egg", src: art + "egg-dust.png", at: EGG.at, foot: EGG.foot, when: () => hen.egg },
    // the back wall round the back door: its casing, the screen door hooked back, Jolene's chair and the pay phone
    { id: "doorframe", src: art + "doorframe.png", base: [[572, 377], [717, 386]] },
    { id: "cooler", src: art + "cooler.png", base: [[241, 370], [298, 374]], solid: [[261, 357], [314, 360], [298, 374], [241, 370]] },       // Harold
    // the counter: the grill and the roller's tray, the register, the jar, the dish, the postcards, the map rack, Ranger's basket
    { id: "counter", src: art + "counter.png", base: COUNTER_BASE, solid: [[299, 380], [555, 398], [556, 417], [336, 400], [325, 413], [275, 409], [288, 397], [281, 396]] },
    // the hot dog roller, turning, empty, for company: on the counter's own base, laid straight after it (sorted by its own
    // row it would go behind the counter and vanish)
    { id: "roller", frames: [art + "roller-0.png", art + "roller-1.png"], fps: 2, at: [538, 335], foot: [13, 11], base: COUNTER_BASE },
    { id: "spinner", src: art + "spinner.png", base: SPINNER_BASE, solid: [[227, 421], [218, 425], [206, 427], [195, 426], [189, 422], [192, 418], [200, 414], [212, 412], [223, 413], [229, 416]] },
    { id: "mirror-shades", src: art + "mirror-shades.png", base: SPINNER_BASE, when: (g) => !g.flag("nevada.shadesBought") },     // the last pair, until it is bought
    { id: "rockbins", src: art + "rockbins.png", base: [[572, 469], [782, 488]], solid: [[570, 442], [760, 458], [782, 488], [572, 469]] },
    { id: "front", src: art + "front.png", plane: "front" },  // the water flats, the crate of empty bottles, the tyres
  ],

  // Grandma Jolene, behind the counter, under the hat of the visit (her kind follows the hat: `setup`). Now and then she
  // goes along to the register and back (her mark is off the floor the family walks on, so in a straight line), and
  // pushes the pencil back into her hair, or sets her hat straight. She is not behind the counter once the family has
  // gone through the door in time: she is out on the porch.
  actors: [
    { id: "jolene", kind: "jolene", at: JOLENE, face: "S", solid: false, when: (g) => !g.flag("nevada.left"),
      life: { every: [22, 44], spots: [[477, 381, "S"]], stay: [4, 9] } },
  ],

  // Make the picture match the story. Runs on arrival and after loading a save.
  // A visit is counted here, as they come in (and not after the picture is up), so that Jolene is under the hat of this
  // visit from the first moment she is seen, and the gap on the board is the right one: `nevada.inStore` says they are
  // inside already (a game saved in here, and loaded), and the scene's `leaving` clears it as they go out (MAP-15M: by the
  // front door or by the map).
  setup(g) {
    hen.pose = {}; hen.sat = new Set(); hen.twitch = {}; hen.egg = false; hen.jolene = null;
    arriving = false;
    if (!g.flag("nevada.left")) {
      if (!g.flag("nevada.inStore")) {
        g.flag("nevada.visits", visits(g) + 1);
        g.flag("nevada.inStore", true);
        arriving = true;
      }
      redraw(g, "jolene", kindOf(g));
      // Her face is just where the words of anybody at the counter would go: the engine lifts their words over her head
      // (the sprite flag `clear`, NEVADA-12SB in js/engine/dialogue.js), as it does for anybody standing nearer.
      const j = g.actor("jolene");
      if (j) j.flag("clear", true);
    }
    henLife(g);
  },

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "hubcaps", name: "hubcap wall", walkTo: [360, 425], face: "N", look: lookAt("nevada.store.hubcaps", "nevada.jolene.hubcaps"), use: useHubcaps,
      poly: [[56, 111], [88, 106], [112, 114], [152, 115], [160, 120], [376, 125], [400, 121], [464, 120], [504, 121], [512, 125], [544, 119], [576, 122], [608, 117], [696, 121], [704, 151], [712, 151], [712, 243], [688, 243], [680, 215], [560, 216], [528, 214], [520, 188], [480, 192], [464, 183], [432, 178], [424, 190], [368, 191], [360, 211], [320, 209], [304, 214], [288, 234], [256, 231], [248, 190], [224, 188], [216, 211], [200, 211], [192, 189], [96, 201], [72, 199], [56, 134]] },
    { id: "fan", name: "ceiling fan", poly: [[314, 94], [317, 79], [389, 48], [395, 48], [484, 82], [484, 83], [398, 147], [396, 147], [314, 95]], walkTo: [457, 468], face: "N", look: lookAt("nevada.store.fan", "nevada.jolene.fan") },
    { id: "window", name: "front window", poly: [[88, 252], [109, 247], [208, 228], [217, 315], [196, 327], [93, 377], [88, 369], [87, 321]], walkTo: [216, 399], face: "W", look: windowLook },
    { id: "backdoor", name: "the back door", verb: "Go out of", poly: [[585, 231], [604, 231], [686, 233], [686, 385], [664, 385], [602, 381], [591, 380], [584, 379]], walkTo: [626, 389], face: "N",
      look: backdoorLook, use: useBackdoor },
    { id: "bulletin", name: "bulletin board", rect: [315, 222, 86, 77], walkTo: [300, 417], face: "N", look: each("nevada.store.board") },
    { id: "hatrack", name: "hat rack", rect: [383, 206, 143, 21], walkTo: [459, 430], face: "N", look: hatsLook },
    // (whoever uses it stands back a step, to watch: the place in front of the phone is Jolene's, when she answers it)
    { id: "payphone", name: "pay phone", rect: [677, 254, 40, 55], walkTo: [640, 424], face: "NE", look: each("nevada.store.phone"), use: answerPhone },
    { id: "cooler", name: "cooler", rect: [240, 236, 75, 138], walkTo: [258, 381], face: "N", look: lookAt("nevada.store.cooler", "nevada.jolene.cooler") },
    { id: "survival", name: "survival shelf", rect: [210, 251, 50, 115], walkTo: [233, 379], face: "N", look: each("nevada.store.survival"), use: useSurvival },
    { id: "tv", name: "television", rect: [213, 202, 41, 55], walkTo: [233, 379], face: "N", look: lookAt("nevada.store.tv", "nevada.jolene.tv") },
    { id: "chair", name: "Jolene's chair", rect: [681, 321, 47, 70], walkTo: [675, 402], face: "E", look: chairLook },
    { id: "counter", name: "counter", poly: [[295, 317], [313, 317], [473, 325], [492, 327], [489, 411], [484, 413], [279, 396], [277, 331]], walkTo: COUNTER, face: "N", look: each("nevada.store.counter") },
    // Grandma Jolene herself: her figure above the counter, as the game draws her at her mark (the register, in front of
    // her, takes the clicks on itself: it is later in this list)
    { id: "jolene", name: "Grandma Jolene", verb: "Talk to", walkTo: COUNTER, face: "N", look: each("nevada.jolene.look"), use: talkToJolene,
      poly: [[403, 226], [435, 226], [438, 248], [431, 251], [432, 285], [446, 291], [446, 323], [397, 321], [397, 291], [407, 285], [407, 251], [400, 248]] },
    { id: "grill", name: "grill", rect: [486, 315, 71, 103], walkTo: [527, 435], face: "N", look: lookAt("nevada.store.grill", "nevada.jolene.grill.1", "nevada.jolene.grill.2") },
    { id: "roller", name: "hot dog roller", rect: [522, 320, 32, 22], walkTo: [538, 436], face: "N", look: lookAt("nevada.store.roller", "nevada.jolene.roller") },
    { id: "register", name: "cash register", rect: [411, 284, 54, 53], walkTo: [427, 428], face: "N", look: each("nevada.store.register"), use: useRegister },
    { id: "eggs", name: "pickled eggs", rect: [323, 285, 25, 43], walkTo: [315, 418], face: "N", look: eggsLook, use: (g) => jolSay(g, "nevada.jolene.eggs") },
    { id: "pennydish", name: "take-a-penny dish", rect: [387, 318, 23, 17], walkTo: COUNTER, face: "N", look: each("nevada.store.pennydish"),
      use: { lilsis: takePennies, mom: "nevada.store.pennydish.mom", bigsis: "nevada.store.pennydish.bigsis" } },
    { id: "postcards", name: "postcards", rect: [299, 274, 20, 51], walkTo: [289, 416], face: "N", look: each("nevada.store.postcards"), use: (g) => jolSay(g, "nevada.jolene.postcards") },
    { id: "maprack", name: "map rack", rect: [433, 343, 48, 55], walkTo: [452, 431], face: "N", look: each("nevada.store.maps") },
    // Ranger's basket, under the counter (where the coin is, until the trade): nobody goes in it but Ranger, and he does not want copper
    { id: "basket", name: "Ranger's basket", rect: [281, 375, 57, 39], walkTo: [307, 424], face: "NW", look: each("nevada.store.basket"), use: (g) => jolSay(g, "nevada.jolene.basket"),
      useWith: { penny: (g) => jolSay(g, "nevada.ranger.copper.jolene"), pennies: (g) => jolSay(g, "nevada.ranger.copper.jolene"), mirrorshades: (g) => jolSay(g, "nevada.jolene.basket") } },
    { id: "autoshelf", name: "auto shelf", rect: [93, 332, 111, 110], walkTo: [166, 429], face: "W", look: lookAt("nevada.store.auto", "nevada.jolene.squeegee"), use: useAuto },
    { id: "spinner", name: "rack of sunglasses", rect: [187, 273, 43, 153], walkTo: [250, 425], face: "W", look: spinnerLook, use: useSpinner },
    { id: "windowshade", name: "the sun shade", verb: "Ask for", plane: "window-shade", rect: [153, 256, 51, 77], walkTo: [232, 388], face: "W", when: (g) => !g.flag("nevada.shadeGiven"),
      look: each("nevada.store.shade"), use: askShade },
    { id: "rockbins", name: "rock bins", poly: [[568, 379], [574, 379], [759, 391], [762, 392], [782, 420], [782, 489], [778, 489], [571, 469], [569, 444], [567, 389]], walkTo: [670, 491], face: "N",
      look: lookAt("nevada.store.rocks", "nevada.jolene.rocks") },
    { id: "door", name: "the door to the lot", verb: "Go out by", poly: [[0, 269], [3, 268], [66, 255], [71, 255], [72, 282], [72, 450], [2, 493], [0, 493]], walkTo: [99, 473], face: "W",
      look: doorLook, use: goOut },
  ],

  given,

  // What they say to each other in here (S/work-writer/ids.md, "What they say to each other"). What has not been heard
  // comes first; the ones that wait for something come first of all.
  talk: {
    mom: {
      bigsis: [
        { when: (g) => g.has("coin") && !g.flag("nevada.coinRead"), say: ["nevada.talk.mom.bigsis.coin.a", "nevada.talk.mom.bigsis.coin.b"] },
        { when: (g) => !!g.flag("nevada.traded"), say: ["nevada.talk.mom.bigsis.trade.a", "nevada.talk.mom.bigsis.trade.b"] },
        { when: (g) => (Number(g.flag("nevada.factsTold")) || 0) >= 1, say: ["nevada.talk.mom.bigsis.jolene.a", "nevada.talk.mom.bigsis.jolene.b", "nevada.talk.mom.bigsis.jolene.c"] },
        ["nevada.talk.mom.bigsis.2a", "nevada.talk.mom.bigsis.2b", "nevada.talk.mom.bigsis.2c"],
      ],
      lilsis: [
        { when: (g) => visits(g) >= 2, say: ["nevada.talk.mom.lilsis.hats.a", "nevada.talk.mom.lilsis.hats.b"] },
        { when: (g) => g.asked("joe/grandpa") > 0, say: ["nevada.talk.mom.lilsis.joe.a", "nevada.talk.mom.lilsis.joe.b"] },
        ["nevada.talk.mom.lilsis.2a", "nevada.talk.mom.lilsis.2b"],
      ],
    },
    bigsis: {
      mom: [
        { when: (g) => !!g.flag("nevada.heardSon"), say: ["nevada.talk.bigsis.mom.son.a", "nevada.talk.bigsis.mom.son.b", "nevada.talk.bigsis.mom.son.c"] },
        ["nevada.talk.bigsis.mom.1a", "nevada.talk.bigsis.mom.1b"],
        ["nevada.talk.bigsis.mom.2a", "nevada.talk.bigsis.mom.2b", "nevada.talk.bigsis.mom.2c"],
      ],
      lilsis: [
        { when: (g) => !!g.flag("nevada.jolene"), say: ["nevada.talk.bigsis.lilsis.egg.a", "nevada.talk.bigsis.lilsis.egg.b"] },
        { when: (g) => !!g.flag("nevada.banjoTried"), say: ["nevada.talk.bigsis.lilsis.banjo.a", "nevada.talk.bigsis.lilsis.banjo.b"] },
        ["nevada.talk.bigsis.lilsis.2a", "nevada.talk.bigsis.lilsis.2b"],
      ],
    },
    lilsis: {
      mom: [
        { when: (g) => !!g.flag("nevada.jolene"), say: ["nevada.talk.lilsis.mom.egg.a", "nevada.talk.lilsis.mom.egg.b", "nevada.talk.lilsis.mom.egg.c"] },
        { when: (g) => !!g.flag("nevada.jolene"), say: ["nevada.talk.lilsis.mom.hens.a", "nevada.talk.lilsis.mom.hens.b", "nevada.talk.lilsis.mom.hens.c"] },
        { when: (g) => !!g.flag("nevada.heardSon"), say: ["nevada.talk.lilsis.mom.son.a", "nevada.talk.lilsis.mom.son.b"] },
        ["nevada.talk.lilsis.mom.2a", "nevada.talk.lilsis.mom.2b", "nevada.talk.lilsis.mom.2c"],
      ],
      bigsis: [
        { when: (g) => !!g.flag("nevada.traded"), say: ["nevada.talk.lilsis.bigsis.trade.a", "nevada.talk.lilsis.bigsis.trade.b", "nevada.talk.lilsis.bigsis.trade.c"] },
        { when: (g) => visits(g) >= 2, say: ["nevada.talk.lilsis.bigsis.hats.a", "nevada.talk.lilsis.bigsis.hats.b", "nevada.talk.lilsis.bigsis.hats.c", "nevada.talk.lilsis.bigsis.hats.d"] },
        ["nevada.talk.lilsis.bigsis.1a", "nevada.talk.lilsis.bigsis.1b", "nevada.talk.lilsis.bigsis.1c"],
      ],
    },
  },

  // Coming in: Bernice rings, and Jolene says hello under the hat of the visit. (Nothing at all once the family has gone
  // through: only the cut-scene brings the stage here then.)
  async enter(g) {
    if (g.flag("nevada.left") || !arriving) return;
    arriving = false;
    g.sfx("beep");                                           // Bernice, the bell over the door
    await g.wait(450);
    await jolSay(g, `nevada.jolene.hello.${hatOf(g)}`);
    const j = g.actor("jolene");
    if (j) j.face("S");
  },
};

/** Set by `setup` when a visit has just been counted: `enter` then says hello. */
let arriving = false;
