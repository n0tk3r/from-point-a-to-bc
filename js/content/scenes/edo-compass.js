// Act Six, the first stretch: the ship's clock, a close-up of the compass box from above, noon (SCENES-21A: new in round
// twenty-one, in place of ENGINE-21's stub; the design, briefs/out/edo2-design.md, sections 5 and 7, #26; every line is
// WRITE-21A's, js/content/lines/edo-c.en.js). A close look that is a scene (ENGINE-21: `closeup`): nobody drawn, nobody
// walking, the portraits switchable, whoever is played the one who looks; "Step back" to the deck, everyone where they stood.
// The card's twelve marks are cut anticlockwise (the rat at the bow mark, the boar, the dog, the rooster at the right, the
// monkey, the sheep, the horse at the bottom, the snake, the dragon, the hare at the left, the tiger, the ox), and beside each
// Kōta has drawn its animal in ink, because he cannot read either; the needle trembles on its pin, its tip on the monkey:
// west-south-west. Kanbei's thumb steadies the box at its near edge (his words come from beside the box: he is not drawn).
//
//   #26, step 1   Big Sister's first look at the needle is the working-out (edo.compass.first.1 to .7): the card is backwards
//                 on purpose, so the needle sits on the heading. "That's backwards genius." (edo.compassRead). Mom's and
//                 Little Sister's looks are their own; Big Sister's after it is her plain one.
//   the marks     a look at each animal, for each of the three; a use of any of them steers nothing (the monkey's and the
//                 rooster's have their own words)
// The needle's tremble is the painter's three states (still, left, still, right), stepped here unevenly three or four times a
// second (no engine kind steps a cut-out's states: the painter's fx `needle-tremble`); for less motion it is still.
//
// Every place is the painter's (art/scenes/edo-compass/layout.json, PAINT-21B's ready.md).
//
// Try it: index.html?scene=edo-deck&lead=bigsis&flags=edo.arrived,edo.clothes,edo.dressed,edo.when,edo.west,edo.aboard, then the box

import { STOCK_DRESSED } from "./edo-common.js";
import { THREE, who, is, each } from "./edo-sea.js";

const art = "art/scenes/edo-compass/";

/** What the scene is doing that is not saved: where the needle's tremble is. */
export const clock = { at: 0, step: 0 };
const TREMBLE = ["still", "left", "still", "right"];

/** The needle: Big Sister's first look is the working-out (#26, step 1). */
const needleLook = Object.assign(async (g) => {
  const me = who(g);
  if (me !== "bigsis" || is(g, "edo.compassRead")) return g.say(`edo.compass.needle.${me}`);
  await g.say("edo.compass.first.1", "edo.compass.first.2", "edo.compass.first.3", "edo.compass.first.4", "edo.compass.first.5", "edo.compass.first.6", "edo.compass.first.7");
  g.flag("edo.compassRead", true);
}, { lines: [...THREE.map((w) => `edo.compass.needle.${w}`), ...[1, 2, 3, 4, 5, 6, 7].map((n) => `edo.compass.first.${n}`)] });
const cardLook = Object.assign((g) => g.say(`edo.compass.card.${is(g, "edo.compassRead") ? "read." : ""}${who(g)}`),
  { lines: THREE.flatMap((w) => [`edo.compass.card.${w}`, `edo.compass.card.read.${w}`]) });

/** A mark of the card: its look for each of the three; a use steers nothing (the monkey's and the rooster's their own). */
const mark = (id, poly) => ({ id, name: id === "rat" ? "the rat's mark" : `the ${id}`, poly, look: each(`edo.compass.${id}`),
  use: each(id === "monkey" || id === "rooster" ? `edo.compass.${id}.use` : "edo.compass.mark.use") });

function tick(g, dt) {
  const n = g.plane("needle");
  if (!n) return;
  if (g.calm) { if (clock.step) { clock.step = 0; n.set("still"); } return; }        // (less motion: the needle still)
  clock.at -= dt;
  if (clock.at > 0) return;
  clock.step = (clock.step + 1) % TREMBLE.length;
  n.set(TREMBLE[clock.step]);
  clock.at = (TREMBLE[clock.step] === "still" ? 170 : 110) + Math.random() * 190;      // (three or four a second, unevenly)
}

export default {
  id: "edo-compass",
  era: "edo",
  name: "The ship's clock",
  music: "edo-sea",
  closeup: { back: "edo-deck", spawn: "compass" },      // where "Step back" goes when nothing remembered it (a save loaded in it)
  party: THREE,
  hands: { thumb: [590, 577] },                       // the tip of Kanbei's thumb (painted: the cut-out `thumb`)
  stock: STOCK_DRESSED,
  tick,

  picture: art + "back.png",
  planes: [
    { id: "needle", plane: "front", states: { still: art + "needle.png", left: art + "needle-l.png", right: art + "needle-r.png" }, state: "still" },
    { id: "thumb", src: art + "thumb.png", plane: "front" },
    { id: "near", src: art + "near.png", plane: "front" },
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "box", name: "compass box", poly: [[152, 84], [648, 84], [688, 598], [112, 598]], ...{ look: each("edo.compass.box"), use: each("edo.compass.box.use") } },
    { id: "lid", name: "lid", poly: [[156, 84], [644, 84], [618, 2], [182, 2]], look: each("edo.compass.lid"), use: each("edo.compass.lid.use") },
    { id: "card", name: "card", poly: [[400, 240], [426, 244], [450, 254], [470, 270], [485, 291], [494, 315], [496, 340], [490, 365], [478, 388], [461, 407], [438, 420], [413, 427], [387, 427], [362, 420], [339, 407], [322, 388], [310, 365], [304, 340], [306, 315], [315, 291], [330, 270], [350, 254], [374, 244]],
      look: cardLook, use: each("edo.compass.card.use") },
    mark("rat", [[372, 228], [386, 226], [400, 225], [414, 226], [428, 228], [450, 145], [434, 142], [417, 140], [400, 139], [383, 140], [366, 142], [350, 145]]),
    mark("boar", [[430, 229], [443, 233], [456, 239], [468, 247], [479, 256], [540, 195], [528, 184], [514, 174], [500, 165], [485, 158], [469, 151], [453, 146]]),
    mark("dog", [[480, 257], [489, 268], [497, 279], [503, 292], [508, 305], [593, 282], [588, 266], [581, 251], [573, 236], [564, 223], [554, 210], [543, 197]]),
    mark("rooster", [[508, 307], [511, 320], [512, 334], [511, 348], [508, 361], [594, 383], [597, 367], [599, 350], [600, 334], [599, 318], [597, 301], [594, 285]]),
    mark("monkey", [[508, 363], [503, 376], [497, 389], [489, 400], [480, 411], [543, 471], [554, 458], [564, 445], [573, 431], [581, 417], [588, 402], [593, 386]]),
    mark("sheep", [[479, 412], [468, 421], [456, 429], [443, 435], [430, 439], [453, 522], [469, 517], [485, 510], [500, 503], [514, 494], [528, 484], [540, 473]]),
    mark("horse", [[428, 440], [414, 442], [400, 443], [386, 442], [372, 440], [350, 523], [366, 526], [383, 528], [400, 529], [417, 528], [434, 526], [450, 523]]),
    mark("snake", [[370, 439], [357, 435], [344, 429], [332, 421], [321, 412], [260, 473], [272, 484], [286, 494], [300, 503], [315, 510], [331, 517], [347, 522]]),
    mark("dragon", [[320, 411], [311, 400], [303, 389], [297, 376], [292, 363], [207, 386], [212, 402], [219, 417], [227, 432], [236, 445], [246, 458], [257, 471]]),
    mark("hare", [[292, 361], [289, 348], [288, 334], [289, 320], [292, 307], [206, 285], [203, 301], [201, 318], [200, 334], [201, 350], [203, 367], [206, 383]]),
    mark("tiger", [[292, 305], [297, 292], [303, 279], [311, 268], [320, 257], [257, 197], [246, 210], [236, 223], [227, 236], [219, 251], [212, 266], [207, 282]]),
    mark("ox", [[321, 256], [332, 247], [344, 239], [357, 233], [370, 229], [347, 146], [331, 151], [315, 158], [300, 165], [286, 174], [272, 184], [260, 195]]),
    { id: "bowmark", name: "bow mark", rect: [384, 113, 32, 26], look: each("edo.compass.bowmark"), use: each("edo.compass.bowmark.use") },
    { id: "needle", name: "needle", poly: [[517, 405], [394, 343], [301, 286], [308, 274], [406, 325], [522, 398]], look: needleLook, use: each("edo.compass.needle.use") },
    { id: "thumb", name: "Kanbei's thumb", rect: [576, 563, 158, 39], look: each("edo.compass.thumb"), use: each("edo.compass.thumb.use") },
  ],

  setup(g) {
    clock.at = 300; clock.step = 0;
    g.loop("sea", { level: 0.6 });
  },
};
