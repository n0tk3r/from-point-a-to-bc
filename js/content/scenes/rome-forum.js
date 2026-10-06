// PLACEHOLDER SCENE: the Son's side of the story. It shows that the same drawing
// kit takes on another era's palette, that each lead has their own pockets, and
// that the player can switch between the two.

async function tossCoin(g) {
  await g.say("rome.hole.coin");
  await g.reach();
  g.take("coin");                              // it comes out of the sky in Nevada, about two thousand years later
  g.sfx("portal");
  await g.wait(900);
  await g.say("rome.hole.coin2");
  g.flag("rome.tossed", true);
  await g.wait(400);
  await backHome(g);
}

/** Act break: leave the Son in Rome and pick the story up with the rest of the family, in the present. */
async function backHome(g) {
  const d = g.store.data;
  g.rememberPlace();
  d.act = 3;
  d.active = "mom";
  g.team(["mom", "bigsis", "lilsis"]);         // from here the player switches between these three
  await g.fade(1, 700);
  await g.card("Meanwhile", "about two thousand years later", { plain: true });
  await g.goto("home-living-room", { via: "cut" });
}

export default {
  id: "rome-forum",
  era: "rome",
  name: "A quiet corner of the Forum",
  walk: { area: [[8, 146], [312, 146], [312, 196], [8, 196]] },      // the whole square, back to the temple steps
  spawn: { default: [120, 182] },
  exits: ["home-living-room"],

  draw(art) {
    return art.sky() + art.temple() + art.ground(14) + art.portal(292, 144, 10, "hole");
  },

  // The fountain stands in the square: walk behind it and it hides the lead's legs.
  props: [
    { id: "fountain", kind: "fountain", at: [232, 170], solid: [[200, 161], [264, 161], [267, 172], [197, 172]] },
  ],

  hotspots: [
    { id: "temple", name: "temple", rect: [56, 48, 128, 70], look: "rome.temple.look" },
    {
      id: "fountain", name: "fountain", verb: "Reach into", rect: [198, 128, 68, 44], walkTo: [232, 180], face: "N", look: "rome.fountain.look",
      use: async (g) => {
        if (g.flag("rome.hasCoin")) return g.say("rome.fountain.again");
        await g.reach();
        await g.say("rome.fountain.take");
        g.give("coin");
        g.flag("rome.hasCoin", true);
      },
    },
    {
      id: "hole", name: "humming door", verb: "Go through", circle: [292, 144, 16], walkTo: [276, 172], face: "E",
      look: "rome.hole.look", use: "rome.hole.use", useWith: { coin: tossCoin },
    },
  ],

  async enter(g) {
    if (g.flag("rome.tossed") && !g.flag("home.arrived")) return backHome(g);     // a save from just after the coin went through
    if (g.flag("rome.arrived")) return;
    await g.wait(400);
    await g.say("rome.arrive.1", "rome.arrive.2", "rome.arrive.3");
    g.flag("rome.arrived", true);
    g.team(["dad", "son"]);
    g.ui.toast("Dad and the Son: switch with the portraits", 4200);
  },
};
