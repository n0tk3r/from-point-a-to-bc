// Act One: inside the wagon, by the Nile (CAR-13S: new in round thirteen; briefs/CAR-13.md, and the design,
// briefs/out/car-interior-design.md). Egypt, about 1920 B.C. Dad plays.
//
// The author, 8 October: getting the map out of the glovebox through the window was not intuitive. The window should be
// rolled down to show the inside of the car, and a click on the inside should take Dad to a scene "where he can click
// around the inside of the car and open the glove compartment to find the map". This is that scene. He gets here from
// the river (egypt-crash.js) by the rolled-down window ("Get into driver's seat") or by the wagon ("Get in wagon").
//
// WHAT THE PLAYER SEES is the inside of the wagon through Dad's own eyes, from the driver's seat, looking ahead and a
// little to the right, so that the whole dashboard is in the picture, from the wheel to the glovebox. DAD IS NOT DRAWN
// (`unseen`, below; docs/DESIGN.md, section 8, "A scene seen through the lead's own eyes"): the car is the subject, and a
// man in the driver's seat would cover the wheel, the key and half the dash. He is on the stage all the same, undrawn, on
// the mark at the bottom middle, so that everything that reaches for him works (what is saved among it); he walks nowhere
// and turns to nothing, and his words are written where the words of somebody not drawn go: at the top of the picture, in
// the middle (their bottom edge on row 150), over the sky, the far bank and the river in the windshield, which the painter
// kept dark enough for his yellow to read (layout.json, "words"). The dashboard runs level across the picture, and the
// world outside is what is tilted: the wagon is nose-down, so the windshield is full of the mound of sand in front of the
// nose, the back of the red hood sloping into it and a strip of river and sky above. Afternoon, as by the river: the sun
// low and ahead, out of the picture, its glare in the top right corner of the glass and a shaft of it across the Son's seat.
//
// Every part of the car is a thing to click: fifteen, none of which sends him anywhere. THE PUZZLE IS THE GLOVEBOX, seen
// whole with nothing in front of it: "Open", and the door drops open on its bottom hinge with a clunk, and there is the
// road map, on a drift of ketchup packets; a beat to see it, the author's line, and the map is his (the beat egypt.map,
// its fact egypt.hasMap, as it always was). The door stays open, on the packets alone, and the author's other line is
// true. The KEY is where the wagon's old "Start" went: the starter grinds and gives up, and the author's line about the
// transmission. The SUN VISOR, pulled down, has his youngest's drawing of the five of them (the tender touch); the
// SLUSHIE in its holder is the Son's, and the first minute of the game (the joke). Each sound plays out before he speaks.
// Nothing here is a wrong try that costs anything: the key, the horn and the rearview mirror are the puzzle's red
// herrings inside, as the hood and the door mirror are outside.
//
// What moves by nature (the painter's marks, layout.json "fx", drawn by the engine): the light on the strip of river and
// the steam off the hood, both outside the glass and kept inside it (`clip`); the air freshener turning on its string
// from the mirror's stem; dust drifting up in the sun over the Son's seat.
//
// The way out is the driver's door ("Open door") or the bottom of the picture, anywhere along it that no thing covers
// ("Go out of the wagon"): the latch, and he is standing at his door by the river (its mark fromCar), facing out. Nothing
// is said, going in again or out. The door is never seen open.
//
// Every number below is the painter's (art/scenes/egypt-car/layout.json; briefs: S/work-car-paint/ready.md, section 3).
//
// Try it: index.html?scene=egypt-car&lead=dad&flags=egypt.arrived
// Later states: &flags=egypt.arrived,egypt.knowsLight   (the rearview mirror's second line: he knows what light does now)
//               &flags=egypt.arrived,egypt.hasMap       (a game saved before round thirteen, with the map: the glovebox is
//                                                        shut until he opens it, and then empty)

const art = "art/scenes/egypt-car/";

/** How many times a line has been spoken. (The engine counts every line it says.) */
const count = (g, id) => g.store.data.seenLines[id] || 0;
/** A thing worth looking at twice: the first line, then the second, turn about. */
const twice = (first, second) => (g) => g.say(count(g, first) <= count(g, second) ? first : second);

/** The windshield's glass, exactly (layout.json "glass": 250 corners, not a pixel of the car inside it; the rearview
    mirror is cut out of it). What moves outside the car is kept inside it: the steam off the hood, and the light on the river. */
const GLASS = [
  [77.12, 70.12], [77.12, 74.88], [76.12, 75.12], [76.12, 80.88], [75.12, 81.12], [75.12, 90.88], [74.12, 91.12], [74.12, 98.88], [73.12, 99.12], [73.12, 104.88],
  [72.12, 105.12], [72.12, 111.88], [71.12, 112.12], [71.12, 118.88], [70.12, 119.12], [70.12, 124.88], [69.12, 125.12], [69.12, 130.88], [68.12, 131.12], [68.12, 137.88],
  [67.12, 138.12], [67.12, 144.88], [66.12, 145.12], [66.12, 151.88], [65.12, 152.12], [65.12, 159.88], [64.12, 160.12], [64.12, 168.88], [63.12, 169.12], [63.12, 175.88],
  [62.12, 176.12], [62.12, 181.88], [61.12, 182.12], [61.12, 186.88], [60.12, 187.12], [60.12, 192.88], [59.12, 193.12], [59.12, 199.88], [58.12, 200.12], [58.12, 206.88],
  [57.12, 207.12], [57.12, 216.88], [56.12, 217.12], [55.12, 230.88], [54.12, 231.12], [54.12, 236.88], [53.12, 237.12], [53.12, 243.88], [52.12, 244.12], [52.12, 247.88],
  [51.12, 248.12], [51.12, 254.88], [50.12, 255.12], [50.12, 260.88], [49.12, 261.12], [49.12, 265.88], [86.88, 265.88], [87.12, 266.88], [88.12, 267.12], [88.12, 288.88],
  [97.88, 288.88], [101.12, 284.88], [102.88, 284.88], [103.12, 283.88], [129.88, 283.88], [130.12, 284.88], [131.88, 284.88], [132.12, 283.88], [251.88, 283.88], [252.12, 282.88],
  [258.88, 282.88], [259.12, 283.88], [335.88, 283.88], [336.12, 282.88], [345.88, 282.88], [346.12, 283.88], [373.88, 283.88], [375.12, 285.88], [376.88, 285.88], [378.12, 287.88],
  [379.88, 287.88], [380.12, 288.88], [389.88, 288.88], [390.12, 287.88], [452.88, 287.88], [453.12, 288.88], [460.88, 288.88], [461.12, 287.88], [478.88, 287.88], [479.12, 288.88],
  [512.88, 288.88], [513.12, 287.88], [534.88, 287.88], [535.12, 284.88], [538.88, 284.88], [539.12, 288.88], [571.88, 288.88], [572.12, 287.88], [583.88, 287.88], [584.12, 288.88],
  [634.88, 288.88], [634.88, 288.12], [633.12, 288.12], [632.88, 287.12], [630.12, 287.12], [629.88, 286.12], [624.12, 286.12], [623.88, 285.12], [621.12, 285.12], [620.88, 284.12],
  [616.88, 283.88], [616.88, 267.12], [626.88, 266.88], [627.12, 265.88], [656.88, 265.88], [657.12, 266.88], [666.88, 267.88], [667.12, 268.88], [670.88, 268.88], [671.12, 269.88],
  [675.88, 269.88], [676.12, 270.88], [680.88, 270.88], [681.12, 271.88], [685.88, 271.88], [686.12, 272.88], [691.88, 272.88], [692.12, 273.88], [696.88, 273.88], [697.12, 274.88],
  [700.88, 274.88], [701.12, 275.88], [704.88, 275.88], [705.12, 276.88], [708.88, 276.88], [709.12, 277.88], [713.88, 277.88], [714.12, 278.88], [720.88, 278.88], [721.12, 279.88],
  [730.88, 280.88], [731.12, 281.88], [734.88, 281.88], [735.12, 282.88], [738.88, 282.88], [739.12, 283.88], [744.88, 283.88], [745.12, 284.88], [749.88, 284.88], [749.88, 267.12],
  [750.88, 266.88], [750.88, 247.12], [751.88, 246.88], [751.88, 223.12], [752.88, 222.88], [752.88, 203.12], [753.88, 202.88], [753.88, 187.12], [754.88, 186.88], [754.88, 168.12],
  [755.88, 167.88], [755.88, 148.12], [756.88, 147.88], [756.88, 128.12], [757.88, 127.88], [757.88, 108.12], [758.88, 107.88], [758.88, 87.12], [759.88, 86.88], [759.88, 84.12],
  [758.88, 83.88], [758.88, 83.12], [759.88, 82.88], [759.88, 68.12], [753.12, 68.12], [752.88, 69.12], [711.12, 69.12], [710.88, 68.12], [708.12, 68.12], [707.88, 69.12],
  [667.12, 69.12], [666.88, 68.12], [621.12, 68.12], [620.88, 69.12], [619.12, 69.12], [618.88, 68.12], [531.12, 68.12], [530.88, 69.12], [495.12, 69.12], [494.88, 68.12],
  [488.12, 68.12], [487.88, 69.12], [445.12, 69.12], [444.88, 68.12], [425.12, 68.12], [425.12, 68.88], [424.12, 69.12], [425.12, 70.88], [455.88, 70.88], [456.12, 71.88],
  [467.88, 71.88], [468.12, 72.88], [469.88, 72.88], [470.12, 73.88], [472.12, 75.12], [472.12, 76.88], [473.12, 77.12], [473.12, 95.88], [472.12, 96.12], [472.12, 97.88],
  [471.12, 98.12], [467.88, 102.12], [464.12, 102.12], [463.88, 103.12], [380.12, 103.12], [379.88, 102.12], [378.12, 102.12], [377.88, 101.12], [373.88, 97.88], [373.88, 84.12],
  [372.88, 83.88], [372.88, 82.12], [373.88, 81.88], [373.88, 78.12], [374.88, 77.88], [374.88, 75.12], [375.88, 74.88], [378.12, 71.88], [379.88, 71.88], [380.12, 70.88],
  [416.88, 70.88], [416.88, 69.12], [407.12, 69.12], [406.88, 68.12], [386.12, 68.12], [385.88, 69.12], [328.12, 69.12], [327.88, 68.12], [261.12, 68.12], [260.88, 69.12],
  [206.12, 69.12], [205.88, 68.12], [193.12, 68.12], [192.88, 69.12], [127.12, 69.12], [126.88, 68.12], [87.12, 68.12], [86.88, 69.12], [78.12, 69.12], [78.12, 69.88]
];

// ---------- in and out ----------
/** Out of the wagon, by the door or by the bottom of the picture: the latch, and he is standing at his door by the river
    (egypt-crash's mark fromCar, on the sand at the driver's door), facing out (S: the river gives no facing, so whoever
    comes in from another scene faces S). Nothing is said. */
async function getOut(g) {
  g.sfx("latch");
  await g.goto("egypt-crash", { spawn: "fromCar" });
}

// ---------- the glovebox: the puzzle (#1, The Road Map) ----------
/** Opened: the clunk, and the door drops open (egypt.gloveOpen: the cut-out shows it hanging on its hinge, the road map
    on the ketchup packets), a beat to see it, the author's line, and the map is his (egypt.hasMap: the map leaves the
    picture). The door stays open. Searched again: the author's other line. A game saved before round thirteen that has
    the map already finds the glovebox shut, and opens it on the packets alone. (No reach: nobody would see it.) */
async function openGlovebox(g) {
  if (!g.flag("egypt.gloveOpen")) {
    g.sfx("clunk");
    g.flag("egypt.gloveOpen", true);
    await g.wait(700);
  }
  if (g.flag("egypt.hasMap")) return g.say("egypt.wagon.empty");
  await g.say("egypt.wagon.use");
  g.give("map");
  g.flag("egypt.hasMap", true);
}
/** Looked at, shut or open: the map is in there until it is in his pockets, and then only the packets are. (So that an
    old save with the map in his pockets never hears "The map's in there".) */
const lookAtGlovebox = (g) => g.say(g.flag("egypt.hasMap") ? "egypt.wagon.empty" : "egypt.glovebox.look");

// ---------- the rest of the car ----------
/** The visor comes down (the click of it), and stays down, his youngest's drawing showing: a moment to see it, and the
    two lines, once. Down, a click looks at it. */
async function pullVisor(g) {
  g.sfx("click");
  g.flag("egypt.visorDown", true);
  await g.wait(450);
  await g.say("egypt.car.visor.down.1", "egypt.car.visor.down.2");
}

/** The rearview mirror: all sky, and once he knows what light does, the mirror he wants is the one on the door. */
const adjustMirror = (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.car.rearview.glued" : "egypt.car.rearview.use");

/** The horn, once: the sound, and then what he says. After that he does not honk again (no sound), and says why. */
async function honk(g) {
  if (count(g, "egypt.car.horn.use")) return g.say("egypt.car.horn.again");
  g.sfx("horn");
  await g.wait(650);
  await g.say("egypt.car.horn.use");
}

/** The key: the starter grinds and gives up (about a second), and the wagon's old line, moved in here with it. */
async function turnKey(g) {
  g.sfx("starter");
  await g.wait(1050);
  await g.say("egypt.wagon.try");
}

/** The radio: static, the whole of it (a second and more), and then what he makes of it. */
async function playRadio(g) {
  g.sfx("hiss");
  await g.wait(1300);
  await g.say("egypt.car.radio.use");
}

/** The gear lever: the click of it, and it stays in Park. */
async function shift(g) {
  g.sfx("click");
  await g.wait(300);
  await g.say("egypt.car.gears.use");
}

/** A thing that is two clickable shapes, because a fact changes its shape and its verb (the visor down, the glovebox
    open), as the river's luggage is (`lidded` in egypt-crash.js). One shows at a time: `before` until the fact is true,
    `after` from then on. */
const twoWays = (spot, fact, before, after) => [
  { ...spot, ...before, when: (g) => !g.flag(fact) },
  { ...spot, ...after, when: (g) => !!g.flag(fact) },
];

export default {
  id: "egypt-car",
  era: "egypt",
  name: "Inside the wagon",

  // Seen through Dad's own eyes: he is on the stage but never drawn, stays where he is, speaks from the top middle, and
  // leaves by the bottom edge at once (the engine: CAR-13E).
  unseen: true,

  // The painter's camera (layout.json: horizon 181 and full 282, room.View's). Nobody is drawn: they size nothing seen.
  horizon: 181, full: 282,

  // Nobody walks: the mark at the bottom middle, under no clickable thing, and a small patch round it (the engine wants
  // somewhere to put him).
  walk: { area: [[410, 580], [450, 580], [450, 598], [410, 598]] },
  blocked: [],
  spawn: { default: [430, 590] },
  exits: ["egypt-crash"],
  // The bottom of the picture is the way out (its band, rows 548 to 600; the bench's bare middle is where the arrow is):
  // a click there takes him out at once. (Its walkTo is his own mark: nobody walks.)
  edges: {
    S: { to: "egypt-crash", spawn: "fromCar", name: "out of the wagon", walkTo: [430, 590], use: getOut },
  },

  picture: art + "back.png",

  // The painted cut-outs, pixel for pixel over the backdrop (which shows the glovebox open with only the packets in it,
  // no driver's visor and no air freshener). Nobody stands in this picture, so their depth only orders them and what
  // moves: the glovebox and the visor at the bottom of the picture, the air freshener in front of everything.
  planes: [
    // the glovebox door: shut; dropped open on the road map; dropped open on the ketchup packets alone. Once open, it stays open.
    { id: "glovebox", states: { shut: art + "glovebox-shut.png", map: art + "glovebox-map.png", empty: art + "glovebox-empty.png" },
      state: (g) => (!g.flag("egypt.gloveOpen") ? "shut" : g.flag("egypt.hasMap") ? "empty" : "map"), base: 600 },
    // the driver's sun visor: up against the headliner; down, the drawing and the registration card on its back. It stays down.
    { id: "visor", states: { up: art + "visor-up.png", down: art + "visor-down.png" }, state: (g) => (g.flag("egypt.visorDown") ? "down" : "up"), base: 600 },
    // the little cardboard wagon on its string from the mirror's stem, a cut-out of its own so that it can turn and swing
    { id: "freshener", src: art + "freshener.png", plane: "front" },
  ],

  // THINGS THAT MOVE BY NATURE: the painter's marks as they are (layout.json "fx"), in the painter's order.
  fx: [
    // the light moving on the strip of river above the mound, very small and quiet: behind every cut-out, kept in the glass
    { id: "river", type: "shimmer", poly: [[85, 122], [744, 122], [744, 158], [520, 156], [400, 166], [262, 154], [120, 168], [60, 180], [73, 186]],
      count: 14, size: 3, flow: [3, 0], life: 1.6, color: "#fff6e2", opacity: 0.3, plane: "back", clip: GLASS },
    // steam off the radiator, from the hood's left side where it runs under the sand, up across the shaded mound, leaning a
    // little to the right: outside the glass (behind every cut-out: the visor, down, hangs in front of it) and kept in it
    { id: "steam", type: "smoke", at: [300, 242], height: 122, width: [4, 30], lean: [34, -122], rise: 22, rate: 3, gust: 0.4, color: "#f6f4ee", opacity: 0.4, plane: "back", clip: GLASS },
    // the air freshener swinging a little in the air from the open window, pinned at the string's knot under the mirror
    { id: "freshener", type: "sway", plane: "freshener", anchor: "top", at: [433, 106], amount: 1.2, period: 3.5 },
    // dust drifting up in the shaft of sun across the Son's cushion (in front: kept off the glovebox's dropped door)
    { id: "dust", type: "shimmer", poly: [[548, 516], [742, 512], [746, 598], [552, 598]], count: 12, size: 1.5, flow: [2, -4], life: 3, color: "#fff2d8", opacity: 0.5, plane: "front" },
  ],

  // The shapes are the painter's (layout.json "things"), traced round each thing as painted. None has a walkTo: nobody
  // walks. In the master brief's order: an area lower in this list lies over the ones above it where they touch, so the
  // nearer and the smaller thing wins (the visor, the mirror and the air freshener over the glass; the gauges, the horn,
  // the gear lever, the key and the radio over the wheel). The wheel and the Son's seat stop at row 548, the top of the
  // bottom band, so that the way out can be clicked along it; only the door, the manual in its pocket and the key's ring
  // reach into the band. The three cut-outs name their planes, so that Show outlines their own silhouettes.
  hotspots: [
    // the glass, and the sand, the hood, the river and the sky seen through it
    {
      id: "windshield", name: "windshield", verb: "Wipe",
      poly: [[77, 70], [74, 98], [65, 152], [63, 175], [59, 193], [57, 216], [49, 265], [86, 265], [88, 267], [88, 288], [97, 288], [103, 283], [131, 284], [252, 282], [373, 283], [380, 288], [512, 288], [534, 287], [535, 284], [538, 284], [539, 288], [634, 288], [616, 283], [616, 267], [627, 265], [656, 265], [696, 273], [709, 277], [749, 284], [759, 68], [424, 69], [455, 70], [469, 72], [473, 77], [473, 95], [467, 102], [463, 103], [378, 102], [373, 97], [372, 82], [374, 75], [380, 70], [416, 70], [406, 68], [87, 68]],
      look: twice("egypt.car.windshield.look", "egypt.car.windshield.look2"), use: "egypt.car.windshield.use",
    },
    // the driver's sun visor: up, "Pull down"; down (it stays down), "Look at", its shape the visor hanging over the glass
    ...twoWays({ id: "visor", name: "sun visor", plane: "visor" }, "egypt.visorDown",
      { verb: "Pull down", look: "egypt.car.visor.look", use: pullVisor,
        poly: [[28, 29], [29, 36], [33, 40], [70, 66], [72, 66], [77, 61], [79, 62], [78, 66], [292, 66], [295, 63], [302, 63], [301, 59], [296, 58], [306, 37], [305, 25], [29, 25]] },
      { verb: "Look at", look: "egypt.car.visor.look2", use: "egypt.car.visor.look2",
        poly: [[65, 62], [70, 65], [70, 75], [62, 160], [295, 160], [292, 65], [301, 64], [302, 60], [300, 59], [79, 59], [75, 81], [74, 98], [71, 107], [71, 76], [73, 60], [68, 59]] }),
    {
      id: "rearview", name: "rearview mirror", verb: "Adjust",
      poly: [[472, 95], [471, 97], [467, 101], [463, 102], [380, 102], [378, 101], [374, 97], [373, 83], [373, 82], [374, 78], [375, 75], [378, 72], [380, 71], [417, 56], [420, 55], [424, 55], [467, 72], [469, 73], [471, 75], [472, 77]],
      look: "egypt.car.rearview.look", use: adjustMirror,
    },
    // the air freshener, its string and the card: looked at only (with no use, a click looks)
    {
      id: "freshener", name: "air freshener", plane: "freshener",
      poly: [[449, 144], [443, 148], [422, 148], [417, 146], [416, 145], [416, 139], [432, 106], [433, 105], [447, 133], [449, 138]],
      look: "egypt.car.freshener.look",
    },
    // his door down the left edge: the open window, the lock knob, the armrest's end, the crank, the pocket. "Open": out.
    {
      id: "door", name: "door", verb: "Open",
      poly: [[0, 59], [0, 599], [61, 599], [65, 590], [55, 577], [29, 576], [25, 541], [26, 522], [17, 510], [18, 506], [16, 504], [0, 503], [0, 421], [18, 402], [18, 371], [15, 369], [15, 363], [1, 361], [1, 307], [6, 304], [29, 303], [29, 292], [36, 288], [87, 287], [86, 266], [39, 265], [67, 80], [68, 65], [59, 59]],
      look: "egypt.car.door.look", use: getOut,
    },
    // the owner's manual, standing in the door pocket (it lies over the door)
    {
      id: "manual", name: "owner's manual", verb: "Read",
      poly: [[17, 510], [0, 535], [0, 591], [8, 590], [26, 556], [26, 522]],
      look: "egypt.car.manual.look", use: "egypt.car.manual.use",
    },
    // the Son's half of the bench, at the bottom right (stopping at row 548): wrappers, a sock, and the gum under it
    {
      id: "seat", name: "passenger seat", verb: "Look under",
      poly: [[799, 513], [681, 513], [679, 511], [673, 511], [671, 509], [662, 511], [662, 513], [595, 514], [571, 519], [555, 525], [539, 535], [528, 547], [799, 547]],
      look: "egypt.car.seat.look", use: "egypt.car.seat.use",
      useWith: { chicken: "egypt.car.seat.chicken" },
    },
    // THE GLOVEBOX: shut, "Open"; open (it stays open), "Search", its shape the compartment and the dropped door
    ...twoWays({ id: "glovebox", name: "glovebox", plane: "glovebox", look: lookAtGlovebox, use: openGlovebox, useWith: { map: "egypt.car.glovebox.map" } }, "egypt.gloveOpen",
      { verb: "Open", poly: [[555, 378], [553, 437], [556, 445], [565, 452], [748, 453], [758, 449], [764, 439], [764, 381], [760, 373], [748, 365], [561, 365], [565, 368], [561, 370]] },
      { verb: "Search", poly: [[556, 376], [554, 382], [553, 431], [556, 439], [560, 443], [560, 448], [556, 452], [554, 452], [614, 489], [618, 493], [619, 500], [783, 501], [783, 461], [760, 452], [751, 451], [747, 447], [747, 443], [753, 432], [753, 383], [750, 375], [744, 370], [739, 368], [653, 367], [569, 368], [561, 371]] }),
    // the Son's slushie in its clip-on holder on the right-hand vent, straw to holder
    {
      id: "cupholder", name: "slushie", verb: "Pick up",
      poly: [[551, 342], [550, 419], [544, 444], [541, 447], [537, 448], [529, 448], [522, 447], [518, 446], [513, 444], [507, 441], [501, 435], [495, 408], [484, 356], [484, 351], [495, 329], [500, 321], [535, 285], [538, 285], [551, 337]],
      look: "egypt.car.slushie.look", use: "egypt.car.slushie.use",
      useWith: { rootbeer: "egypt.car.slushie.rootbeer" },
    },
    // the steering wheel's rim and the column (stopping at row 548); the things below lie over it
    {
      id: "wheel", name: "steering wheel", verb: "Turn",
      poly: [[29, 491], [26, 528], [27, 547], [444, 547], [445, 528], [442, 491], [433, 450], [421, 418], [409, 394], [399, 378], [373, 346], [340, 318], [327, 310], [297, 296], [262, 287], [232, 285], [209, 287], [186, 292], [164, 300], [144, 310], [131, 318], [106, 338], [83, 363], [62, 394], [50, 418], [39, 447]],
      look: "egypt.car.wheel.look", use: "egypt.car.wheel.use",
    },
    {
      id: "radio", name: "radio", verb: "Turn on",
      poly: [[493, 416], [372, 416], [371, 415], [370, 403], [370, 375], [397, 373], [489, 373], [491, 375], [493, 384]],
      look: "egypt.car.radio.look", use: playRadio,
    },
    {
      id: "gauges", name: "gauges", verb: "Tap",
      poly: [[387, 418], [372, 417], [370, 415], [369, 373], [362, 364], [349, 352], [121, 352], [103, 371], [88, 392], [88, 414], [93, 422], [100, 425], [375, 425], [383, 422]],
      look: "egypt.car.gauges.look", use: "egypt.car.gauges.use",
    },
    // the horn pad, plain
    {
      id: "horn", name: "horn", verb: "Honk",
      poly: [[296, 519], [295, 529], [294, 532], [292, 537], [290, 541], [287, 545], [285, 547], [186, 547], [184, 545], [180, 540], [179, 538], [176, 531], [175, 525], [175, 514], [176, 480], [177, 465], [178, 459], [179, 456], [183, 448], [190, 440], [198, 436], [201, 435], [206, 434], [264, 434], [270, 435], [273, 436], [281, 440], [287, 447], [289, 450], [292, 456], [294, 467], [295, 480], [296, 514]],
      look: "egypt.car.horn.look", use: honk,
    },
    {
      id: "gears", name: "gear lever", verb: "Shift",
      poly: [[436, 428], [435, 430], [433, 433], [432, 434], [430, 435], [294, 463], [293, 461], [292, 455], [292, 453], [418, 406], [424, 406], [430, 409], [433, 412], [436, 418]],
      look: "egypt.car.gears.look", use: shift,
    },
    // the car's key alone in the ignition, its plain ring and fob hanging into the band (to row 584)
    {
      id: "key", name: "car key", verb: "Turn",
      poly: [[362, 584], [350, 584], [346, 583], [313, 503], [313, 502], [318, 501], [338, 501], [345, 502], [346, 504], [353, 524], [361, 548], [362, 575]],
      look: "egypt.car.key.look", use: turnKey,
    },
  ],

  // Runs when he gets in. The first time only: a moment in the seat, and his word on it (egypt.sawCar). It must be safe to
  // run twice (loading a save runs it again), so it checks its own fact.
  async enter(g) {
    if (g.flag("egypt.sawCar")) return;
    await g.wait(450);
    await g.say("egypt.car.arrive");
    g.flag("egypt.sawCar", true);
  },
};
