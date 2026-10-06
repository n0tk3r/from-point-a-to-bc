// A scene is one file. It says how the place is drawn, where people can walk,
// what stands on the ground, what can be clicked, and what happens when it is.
//
// PLACEHOLDER SCENE, written to prove the engine: two short puzzle chains (a pen
// for the scribe, a sheet for him to draw on) that meet at one gate (the door).

async function talkToScribe(g) {
  if (!g.flag("egypt.metScribe")) {
    await g.say("egypt.scribe.hello", "egypt.scribe.hello2");
    g.flag("egypt.metScribe", true);
  }
  for (;;) {
    const pick = await g.choose([
      { id: "boy", line: "egypt.ask.boy" },
      { id: "door", line: "egypt.ask.door" },
      { id: "bye", line: "egypt.ask.bye" },
    ]);
    if (pick === "boy") await g.say("egypt.ask.boy", "egypt.ans.boy", "egypt.ans.boy2");
    else if (pick === "door") await g.say("egypt.ask.door", "egypt.ans.door");
    else return g.say("egypt.ask.bye", "egypt.ans.bye");
  }
}

async function giveReed(g) {
  await g.say("egypt.give.reed");
  await g.reach();
  g.take("reed");
  await g.say("egypt.got.reed", "egypt.need.sheet");
  g.flag("egypt.metScribe", true);
  g.flag("egypt.penGiven", true);
}

async function giveMap(g) {
  await g.say("egypt.give.map");
  if (!g.flag("egypt.penGiven")) return g.say("egypt.got.map.nopen");
  await g.reach();
  g.take("map");
  await g.say("egypt.got.map", "egypt.door.steady");
  g.flag("egypt.mapMarked", true);
  // The door stops flickering and opens wide.
  const hole = g.q("#hole");
  hole.classList.remove("flicker");
  g.sfx("portal");
  await g.tween(900, (k) => { hole.style.transform = `scale(${1 + 1.3 * k})`; }, g.ease.out);
}

async function useDoor(g) {
  if (!g.flag("egypt.mapMarked")) return g.say("egypt.hole.small");
  if (g.flag("egypt.ready")) return g.say("egypt.hole.wait");
  await g.say("egypt.hole.go");
  g.flag("egypt.ready", true);
  // Act break: leave Dad at the door and pick the story up with the Son.
  const d = g.store.data;
  g.rememberPlace();
  d.act = 2;
  d.active = "son";
  await g.fade(1, 500);
  await g.card("Meanwhile", "about twelve hundred years later", { plain: true });
  await g.goto("rome-forum", { via: "wormhole" });
}

export default {
  id: "egypt-riverbank",
  era: "egypt",
  name: "A riverbank at dawn",

  // DEPTH. The horizon is the line the ground runs back to. A figure is full size
  // with its feet at `full`, and shrinks toward the horizon. (These are the defaults.)
  horizon: 118, full: 190,

  // Where the lead can walk: the sand, from far back near the pyramids to the front
  // of the screen, with the edge following the riverbank.
  walk: { area: [[104, 138], [312, 138], [312, 196], [8, 196], [8, 190], [48, 176], [84, 154]] },
  spawn: { default: [200, 184] },
  exits: ["rome-forum"],                       // scenes to fetch ahead of time

  // The backdrop: everything that is far away or flat on the ground.
  draw(art) {
    return art.sky() +
      `<circle class="light" cx="150" cy="112" r="11"/>` +
      art.pyramids + art.ground(8) + art.river() +
      art.portal(34, 148, 9, "hole");
  },

  // Props stand on the ground. The lead is drawn behind one when his feet are
  // higher on the screen than the prop's own `at` point, and in front when lower.
  // `solid` is the patch of ground the prop takes up: nobody can walk through it.
  props: [
    { id: "reeds", kind: "reeds", at: [82, 168], scale: 0.9 },
    { id: "wagon", kind: "wagonStuck", at: [254, 176], scale: 1.12, solid: [[220, 164], [288, 164], [292, 179], [216, 179]] },
  ],

  // People who are here but are not the lead. They block the ground they sit on.
  actors: [{ id: "scribe", kind: "scribe", at: [150, 170], face: "E" }],

  // Make the drawing match the story facts. Runs on arrival and after loading a save.
  setup(g) {
    const hole = g.q("#hole"), open = !!g.flag("egypt.mapMarked");
    hole.style.transform = `scale(${open ? 2.3 : 1})`;
    hole.classList.toggle("flicker", !open);
  },

  hotspots: [
    { id: "pyramids", name: "pyramids", rect: [186, 82, 110, 36], look: "egypt.pyramids.look" },
    { id: "river", name: "river", poly: [[0, 118], [128, 118], [104, 134], [76, 152], [40, 172], [0, 186]], walkTo: [98, 174], face: "W", look: "egypt.river.look" },
    {
      id: "reeds", name: "reeds", verb: "Pick", rect: [62, 136, 42, 33], walkTo: [110, 172], face: "W", look: "egypt.reeds.look",
      use: async (g) => {
        if (g.flag("egypt.hasReed")) return g.say("egypt.reeds.again");
        await g.reach();
        await g.say("egypt.reeds.take");
        g.give("reed");
        g.flag("egypt.hasReed", true);
      },
    },
    {
      id: "wagon", name: "wagon", verb: "Search", rect: [222, 122, 64, 56], walkTo: [254, 186], face: "N", look: "egypt.wagon.look",
      use: async (g) => {
        if (g.flag("egypt.hasMap")) return g.say("egypt.wagon.empty");
        await g.reach();
        await g.say("egypt.wagon.use");
        g.give("map");
        g.flag("egypt.hasMap", true);
      },
    },
    {
      id: "scribe", name: "scribe", verb: "Talk to", rect: [133, 140, 34, 32], walkTo: [186, 174], face: "W",
      look: "egypt.scribe.look", use: talkToScribe, useWith: { reed: giveReed, map: giveMap },
    },
    {
      id: "hole", name: "humming door", verb: "Go through", circle: [34, 148, 17], walkTo: [62, 174], face: "W",
      look: (g) => g.say(g.flag("egypt.mapMarked") ? "egypt.hole.big" : "egypt.hole.look"),
      use: useDoor,
    },
  ],

  // Runs when the lead arrives. It must be safe to run twice, so it checks its own fact.
  async enter(g) {
    if (g.flag("egypt.arrived")) return;
    await g.wait(500);
    await g.say("egypt.arrive.1", "egypt.arrive.2", "egypt.arrive.3");
    g.flag("egypt.arrived", true);
  },
};
