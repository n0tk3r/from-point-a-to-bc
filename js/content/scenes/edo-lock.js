// Act Six, the fifth leg: the shipwright's lock on the women's hall's doors, seen close (SCENES-21C: new in round twenty-one, in
// place of ENGINE-21's stub; briefs/SCENES-21.md, and the design, briefs/out/edo2-design.md, "THE SHIPWRIGHT'S LOCK" and #37).
// A close-up (ENGINE-21: `closeup`): nobody drawn, nobody walking; the portraits switch at once, and whoever is played is the
// one whose hand acts. A block of dark wood bound with iron, carved as a rabbit running over three waves: its long ear laid
// back with a tiny hole in it, black with forty years of dust; the middle wave a hair loose; a line carved along its back; the
// bolt through the hasp's staple; slips on the stiles and the doors' lattice behind.
//
// Opened from the lock at the foot of Mount Shosha (edo-shosha.js, `lockUse`: the first time Grandmother Tome, from the bench,
// and edo.lockSeen). "Step back" (the corner button, Esc) goes back there, everyone where they stood.
//
//   #37 (5) three tricks, one after another, each held while the next is done (the lines: WRITE-21B's lockLines and lockState,
//           talk/edo-d.js, from the most particular id to the most general)
//     the ear     O-Tami's pin (`kanzashi`) on the ear: the first try by anyone cleans the hole (edo.earClean; the ear's
//                 `clean` state); only Little Sister's fingers push it home: the middle wave slides aside, the square post
//                 shows (edo.earHeld: her hand drawn at `handEar`, holding)
//     the post    Kōta's coin (`mon`) on the post while it shows: only Mom's wrist turns it (the coin on it, then turned): the
//                 line along the rabbit's back opens into slits (edo.postHeld: her hand at `handPost`)
//     the slits   O-Natsu's comb, by Big Sister's steady hand (her hand at `handComb`): the springs close, it chirps (the
//                 Funadama's sound), the bolt comes out; O-Ume, outside: "That's his joke." Then back out to the hall's doors,
//                 which open (edo-shosha.js `openDoors`: edo.hallOpen)
//   each part has its person, and each of them is carrying the wrong thing: the hand-round by the portraits (a thing held,
//   a click on another's portrait), with the giver's line when it goes to its right one (edo-shosha.js `handRound`). Out of
//   order, or one person trying two parts: her line, and nothing changes. A held part's thing given away, or stepping back,
//   lets everything go (LOCK.letgo, by whoever does it; the held facts are `momentary`: never saved, a reload finds it shut).
//   Big Sister's note on any part: the list against the riddle (SHOSHA.list, edo.listRead), once the riddle is known.
//   The hidden post's own lines (edo.lock.post.<who>, .use.<who>) have no area to be asked from while the wave covers it: a
//   coin tried on the middle wave then says the post's line ("The wave's in the way.").
//
// Every place is the painter's measurement (art/scenes/edo-lock/layout.json, PAINT-21E's ready.md: 22 px to the centimetre);
// the hands are PEOPLE-21B's (LOCK_HANDS), scaled to the lock (22 / 6.5) and turned so each arm comes in from its owner's side.
//
// Try it: index.html?scene=edo-shosha&lead=mom&flags=edo.supperMade,edo.riddle,edo.oumeMet, then use the lock

import { LOCK_HANDS, withHand } from "../../art/people.js";
import { THREE, who, is, each, takeAny, carries } from "./edo-west.js";
import { LOCK, SHOSHA, SHOSHA_MAP, lockLines, lockState } from "../talk/edo-d.js";
import { openDoors, handRound } from "./edo-shosha.js";
import { GIVE_SILENT } from "./edo-west.js";

const art = "art/scenes/edo-lock/";

// ---------- the hands (layout.json hands; PEOPLE-21B's LOCK_HANDS) ----------
const HANDS = { handEar: [409, 226], handPost: [433, 373], handComb: [500, 256] };
const SCALE = 22 / 6.5;                                      // the lock's 22 px to the cm, against the hands' 6.5
// where each arm comes in from, in degrees round from straight up out of the bottom edge (PEOPLE-21B's `from`), worked out from
// the painter's wrists: Little Sister's from the upper left (228, 40), Mom's from below (470, 600), Big Sister's from the
// upper right (660, 40)
const FROM = { lilsis: -136, mom: 9, bigsis: 144 };
const SPEC = {
  lilsis: withHand(LOCK_HANDS.lilsis, { from: FROM.lilsis, scale: SCALE }),
  mom: withHand(LOCK_HANDS.mom, { from: FROM.mom, scale: SCALE, coin: false }),
  momTurned: withHand(LOCK_HANDS["mom-turned"], { from: FROM.mom, scale: SCALE, coin: false }),
  bigsis: withHand(LOCK_HANDS.bigsis, { from: FROM.bigsis, scale: SCALE }),
};

// ---------- what is held now (the facts are `momentary`; the moments in between are the scene's own) ----------
const room = { coin: false, comb: false, opening: false };
const ear = (g) => is(g, "edo.earHeld");
const post = (g) => is(g, "edo.postHeld");
/** The hands that are holding, put back from the facts (nothing of a hand is saved). */
function hands(g) {
  if (ear(g)) g.hand("lilsis", "handEar", SPEC.lilsis); else g.hand("lilsis", null);
  if (post(g)) g.hand("mom", "handPost", SPEC.momTurned); else if (room.coin) g.hand("mom", "handPost", SPEC.mom); else g.hand("mom", null);
  if (room.comb) g.hand("bigsis", "handComb", SPEC.bigsis); else g.hand("bigsis", null);
}
/** Everything springs back: the comb, the coin, the pin; the wave slides home. */
function letGo(g) {
  room.coin = false; room.comb = false;
  g.flag("edo.postHeld", false);
  g.flag("edo.earHeld", false);
  hands(g);
}

// ---------- looks and uses ----------
const lookOf = (thing) => (g) => { const st = lockState(g, thing); return g.say(`edo.lock.${thing}${st ? "." + st : ""}.${who(g)}`); };
/** The lines for a use, or the act's stock "nope". */
async function say(g, ids) { if (ids && ids.length) await g.say(...ids); else await g.say(g.fallback("nope")); }
const PRINTS = { toyamaprint: "print", blueprint: "print" };
/** A part of the lock used with nothing in hand. */
const useOf = (thing) => async (g) => {
  const me = who(g);
  if (thing === "rabbit" && me === "mom") return g.say(...LOCK.rabbitMom);
  return say(g, lockLines(g, g.lines, thing, me));
};
/** A part of the lock with a thing used on it: the three tricks, the list, or the thing's line. */
const withOf = (thing) => async (g, item) => {
  const me = who(g), it = PRINTS[item] || item;
  // the note: the list against the riddle (once there is a riddle to hold it against)
  if (it === "note") {
    if (me === "bigsis" && !is(g, "edo.riddle")) return g.say(g.fallback("nope"));
    const ids = lockLines(g, g.lines, thing, me, "note");
    await say(g, ids);
    if (me === "bigsis" && !is(g, "edo.listRead")) { await g.say(...SHOSHA.list); g.flag("edo.listRead", true); }
    return;
  }
  // the pin in the ear: cleaned by anyone; pushed home only by Little Sister
  if (it === "kanzashi" && (thing === "ear" || thing === "earhole")) {
    const ids = lockLines(g, g.lines, thing, me, "kanzashi");
    if (!is(g, "edo.earClean")) {
      await g.say(ids[0]);
      g.flag("edo.earClean", true);
      g.sfx("click");
      if (me !== "lilsis") return g.say(ids[1]);
      await g.say(ids[1]);
      return holdEar(g);
    }
    await g.say(ids[0]);
    if (me === "lilsis" && !ear(g)) return holdEar(g);
    return;
  }
  // the coin on the post, while it shows: Mom's wrist turns it
  if (it === "mon" && thing === "post" && ear(g) && !post(g) && me === "mom") {
    const ids = lockLines(g, g.lines, "post", "mom", "mon");
    room.coin = true; hands(g);
    g.sfx("click");
    await g.say(ids[0]);
    g.flag("edo.postHeld", true);
    room.coin = false; hands(g);
    g.sfx("click");
    return g.say(ids[1]);
  }
  // a coin on the middle wave while it covers the post: the post's own line
  if (it === "mon" && thing === "wave" && !ear(g)) return say(g, lockLines(g, g.lines, "post", me, "mon"));
  // the comb into the slits, by Big Sister's steady hand: it opens
  if (it === "comb" && thing === "back" && post(g) && me === "bigsis") return openIt(g);
  return say(g, lockLines(g, g.lines, thing, me, it));
};
async function holdEar(g) {
  g.flag("edo.earHeld", true);
  hands(g);
  g.sfx("click");
}

/** The comb home: the springs close; it chirps; the bolt comes out; O-Ume's laugh from outside. Then back out, and the doors. */
async function openIt(g) {
  const ids = lockLines(g, g.lines, "back", "bigsis", "comb");
  room.comb = true; hands(g);
  await g.say(ids[0]);
  await g.say(LOCK.open[0]);
  g.sfx("chirp");
  await g.wait(700);
  room.opening = true;
  const bolt = g.plane("bolt");
  if (bolt) bolt.set("out");
  g.sfx("click");
  await g.say(LOCK.open[1], LOCK.open[2]);
  await g.say(LOCK.open[3]);
  await g.wait(300);
  room.comb = false;
  for (const id of THREE) g.hand(id, null);
  try { await g.stepBack(); } finally { room.opening = false; }
  await openDoors(g);
}

// ---------- the hand-round, and things given away while held ----------
async function given(g, item, to, from) {
  if ((item === "kanzashi" && from === "lilsis" && ear(g)) || (item === "mon" && from === "mom" && post(g))) {
    await g.say(LOCK.letgo[from]);
    letGo(g);
  }
  await handRound(g, item, to, from);
}

// ---------- the scene ----------
const part = (id, name, shape, more = {}) => ({ id, name, ...shape, look: lookOf(id), use: useOf(id), useWith: WITH(id), ...more });
/** Every carried thing on a part: its handler (the engine calls useWith[item]). */
const ITEMS = ["kanzashi", "mon", "comb", "note", "coin", "lastpenny", "twopennies", "lilflash", "carkey", "pencil", "sheet", "mirror", "trowel", "riceball",
  "natsuslip", "fusaslip", "toyamaprint", "blueprint"];
const WITH = (id) => Object.fromEntries(ITEMS.map((item) => [item, (g) => withOf(id)(g, item)]));
const poly = (p) => ({ poly: p });
const rect = (r) => ({ rect: r });

export default {
  id: "edo-lock",
  era: "edo",
  name: "The shipwright's lock",
  music: "edo-shosha",
  closeup: { back: "edo-shosha", spawn: "lock" },      // where Step back goes when nothing else says (a save loaded in it)
  party: THREE,
  picture: art + "back.png",
  hands: HANDS,
  momentary: ["edo.earHeld", "edo.postHeld"],          // ENGINE-21: the held states: never saved, let go as the scene is left or built
  stock: GIVE_SILENT,
  travel: SHOSHA_MAP.stay,
  given,

  // CUT-OUTS (the painter's moving parts and alts, all on the back plane): the ear (dusty, clean), the middle wave (in place,
  // slid aside), the coin on the square post (on it; turned), the slits along the back, the bolt (in, out).
  planes: [
    { id: "ear", plane: "back", states: { dusty: art + "ear.png", clean: art + "ear-clean.png" }, state: (g) => (is(g, "edo.earClean") ? "clean" : "dusty") },
    { id: "wave", plane: "back", states: { in: art + "wave.png", slid: art + "wave-slid.png" }, state: (g) => (ear(g) ? "slid" : "in") },
    { id: "post", plane: "back", states: { coin: art + "post-coin.png", turned: art + "post-turned.png" }, state: (g) => (post(g) ? "turned" : "coin"),
      when: (g) => post(g) || room.coin },
    { id: "back", plane: "back", src: art + "back-open.png", when: post },
    { id: "bolt", plane: "back", states: { in: art + "bolt.png", out: art + "bolt-out.png" }, state: (g) => (is(g, "edo.hallOpen") || room.opening ? "out" : "in") },
    { id: "near", src: art + "near.png", plane: "front" },
  ],
  // THINGS THAT MOVE BY NATURE: a few motes of dust in the low sun across the lock (layout.json fx)
  fx: [{ id: "dust", type: "shimmer", rect: [180, 140, 520, 320], count: 8, size: 2, flow: [3, -1], life: 3.0, color: "#fff2cc", opacity: 0.35 }],

  // Back to front: a later area lies over an earlier one (layout.json things).
  hotspots: [
    part("lattice", "lattice", poly([[0, 0], [84, 0], [84, 600], [0, 600]])),
    { ...part("lattice", "lattice", poly([[690, 0], [800, 0], [800, 600], [690, 600]])), id: "lattice2" },
    ...[[[96, 16], [146, 16], [146, 176], [96, 176]], [[606, 16], [662, 16], [662, 176], [606, 176]], [[90, 426], [144, 426], [144, 584], [90, 584]], [[634, 446], [684, 446], [684, 594], [634, 594]]]
      .map((p, n) => ({ id: n ? `slips${n + 1}` : "slips", name: "name slips", poly: p, look: each("edo.shosha.slips"), use: each("edo.shosha.slips.use") })),
    part("hasp", "hasp", poly([[98, 220], [168, 216], [172, 398], [102, 402]])),
    part("rabbit", "rabbit", poly([[255, 275], [285, 253], [327, 251], [393, 244], [464, 248], [519, 260], [552, 260], [536, 277], [591, 313], [585, 326], [525, 299], [446, 306], [356, 299], [283, 326], [252, 321], [305, 295], [261, 286]])),
    part("waves", "three waves", poly([[226, 326], [635, 326], [635, 407], [226, 407]])),
    part("back", "rabbit's back", poly([[459, 238], [541, 238], [541, 271], [459, 271]])),
    { ...part("wave", "middle wave", poly([[361, 348], [385, 331], [405, 324], [430, 327], [455, 343], [474, 362], [499, 388], [507, 412], [357, 413], [353, 410], [354, 385], [357, 359]])), when: (g) => !ear(g) },
    { ...part("wave", "middle wave", poly([[436, 359], [442, 347], [464, 331], [486, 323], [509, 327], [533, 343], [550, 359], [578, 388], [586, 408], [586, 412], [436, 413], [431, 410]])), when: ear },
    { ...part("post", "square post", rect([402, 343, 60, 60])), when: ear },
    part("ear", "rabbit's ear", poly([[305, 254], [327, 229], [362, 216], [406, 210], [449, 214], [469, 222], [472, 226], [471, 230], [458, 238], [325, 267], [323, 266], [310, 259]])),
    part("earhole", "hole in the ear", rect([394, 214, 28, 24])),
    part("bolt", "bolt", poly([[211, 293], [211, 319], [105, 328], [103, 328], [78, 321], [73, 312], [73, 302], [79, 292], [103, 280], [105, 280]])),
  ],

  // The hands that are holding, from the facts (none after a reload: the held states are never saved).
  setup(g) {
    room.coin = false; room.comb = false;
    hands(g);
  },
  /** Stepping back (the corner button, Esc), with a part held: everything springs back. */
  async leaving(g) {
    if (room.opening) return;
    if (ear(g) || post(g)) { await g.say(LOCK.letgo[who(g)]); letGo(g); }
  },
};

// (the names a test or a tool may want)
export { HANDS, SCALE, FROM, SPEC };
