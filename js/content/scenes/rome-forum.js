// PLACEHOLDER SCENE: the Son's side of the story. It shows that the same drawing
// kit takes on another era's palette, that each lead has their own pockets, and
// that the player can switch between the two.

async function tossCoin(g) {
  await g.say("rome.hole.coin");
  g.take("coin");
  g.sfx("portal");
  await g.wait(900);
  await g.say("rome.hole.coin2");
  g.flag("demo.done", true);
  await g.wait(400);
  await g.fade(1, 700);
  await g.card("To be continued", "End of the demo", { plain: true, ms: 3000 });
  await g.title();
}

export default {
  id: "rome-forum",
  era: "rome",
  name: "A quiet corner of the Forum",
  walk: { x: [20, 300], y: [170, 192] },
  scale: [0.95, 1.2],
  spawn: { default: [120, 182] },

  draw(art) {
    return art.sky() + art.temple() + art.ground(14) + art.fountain + art.portal(292, 148, 10, "hole");
  },

  hotspots: [
    { id: "temple", name: "temple", rect: [56, 48, 128, 70], look: "rome.temple.look" },
    {
      id: "fountain", name: "fountain", verb: "Reach into", rect: [204, 134, 56, 34], walkTo: [194, 180], look: "rome.fountain.look",
      use: async (g) => {
        if (g.flag("rome.hasCoin")) return g.say("rome.fountain.again");
        await g.say("rome.fountain.take");
        g.give("coin");
        g.flag("rome.hasCoin", true);
      },
    },
    {
      id: "hole", name: "humming door", verb: "Go through", circle: [292, 148, 16], walkTo: [270, 178],
      look: "rome.hole.look", use: "rome.hole.use", useWith: { coin: tossCoin },
    },
  ],

  async enter(g) {
    if (g.flag("rome.arrived")) return;
    await g.wait(400);
    await g.say("rome.arrive.1", "rome.arrive.2");
    g.flag("rome.arrived", true);
    g.flag("leads.switch", true);
    g.ui.toast("You can now switch between Dad and Son");
  },
};
