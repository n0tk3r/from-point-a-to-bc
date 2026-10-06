// PLACEHOLDER SCENE: the middle of Nevada, where the phone was last seen.
//
// Two chains and a gate, and again each of the three does what only she can:
//   Mom gets the witness to talk, by asking nicely and knowing her husband's car   (chain A)
//   ...and hands the coin he gives her to Big Sister, who can tell what it is       (chain A)
//   Little Sister asks the man in gray so many questions that he steps aside        (chain B)
//   ...and Big Sister reads the notice he was standing in front of                  (chain B)
// The coin is the one the Son threw through the door in Rome: what goes into a hole in
// one year comes out of one in another.
//
// Try it: index.html?scene=nevada-roadside

const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;

/** Once Big Sister has both the coin and the notice, she puts them together. Said once. */
async function connect(g) {
  if (g.flag("nevada.coinRead") && g.flag("nevada.notice") && !g.flag("nevada.connected")) {
    await g.say("nevada.connect");
    g.flag("nevada.connected", true);
  }
}

// ---------- chain A: the witness ----------
async function talkToOldTimer(g) {
  const me = who(g);
  if (me !== "mom") {
    const after = g.flag("nevada.witness") ? ".after" : "";
    const n = after ? (me === "bigsis" ? 3 : 2) : me === "bigsis" ? 4 : 3;
    return g.say(...Array.from({ length: n }, (_, i) => `nevada.old${after}.${me}.${i + 1}`));
  }
  if (!g.flag("nevada.witness")) {
    if (!g.flag("nevada.metOldTimer")) {
      await g.say("nevada.old.mom.1", "nevada.old.mom.2", "nevada.old.mom.3", "nevada.old.mom.4", "nevada.old.mom.5", "nevada.old.mom.6", "nevada.old.mom.7");
      g.flag("nevada.metOldTimer", true);
    } else await g.say("nevada.old.again");
    for (;;) {                                   // he wants to know she is who she says she is
      const pick = await g.choose([
        { id: "sedan", line: "nevada.car.sedan" },
        { id: "wagon", line: "nevada.car.wagon" },
        { id: "black", line: "nevada.car.black" },
      ]);
      await g.say(`nevada.car.${pick}`);
      if (pick === "wagon") break;
      await g.say(`nevada.car.no.${pick}`);
    }
    await g.say("nevada.old.saw.1", "nevada.old.saw.2", "nevada.old.saw.3", "nevada.old.saw.4", "nevada.old.saw.5");
    await g.reach();
    g.give("coin");
    g.flag("nevada.witness", true);
    return g.say("nevada.old.saw.6");
  }
  for (;;) {
    const pick = await g.choose([
      { id: "fence", line: "nevada.ask.fence" },
      { id: "areas", line: "nevada.ask.areas" },
      { id: "bye", line: "nevada.ask.bye" },
    ]);
    await g.say(`nevada.ask.${pick}`, `nevada.ans.${pick}`);
    if (pick === "bye") return;
  }
}

async function readCoin(g) {
  await g.say("nevada.coin.read.1", "nevada.coin.read.2", "nevada.coin.read.3", "nevada.coin.read.4");
  g.flag("nevada.coinRead", true);
  await connect(g);
}

// ---------- chain B: the man in gray, and what he is standing in front of ----------
async function talkToAgent(g) {
  const me = who(g);
  if (g.flag("nevada.distracted")) return me === "lilsis" ? g.say("nevada.agent.again.1", "nevada.agent.again.2") : g.say("nevada.agent.busy");
  if (me !== "lilsis") return g.say(...[1, 2, 3, 4].map((n) => `nevada.agent.${me}.${n}`));
  await g.say("nevada.agent.lil.1", "nevada.agent.lil.2", "nevada.agent.lil.3", "nevada.agent.lil.4", "nevada.agent.lil.5", "nevada.agent.lil.6");
  // He retreats along the fence with a hand to his ear. She goes with him.
  const agent = g.actor("agent");
  agent.face("E");
  await Promise.all([g.moveTo(300, 146, "agent"), g.walkTo(284, 150)]);
  agent.face("E");
  g.lead.face("E");
  g.flag("nevada.distracted", true);
  await g.say("nevada.agent.lil.7", "nevada.agent.lil.8");
}

async function readNotice(g) {
  const me = who(g);
  if (!g.flag("nevada.distracted")) return g.say(`nevada.notice.blocked.${me}`);
  g.closeup(g.art.notice(), "The notice on the fence");
  if (me === "mom") return g.say("nevada.notice.mom.1", "nevada.notice.mom.2");
  if (me === "lilsis") return g.say("nevada.notice.lilsis");
  if (g.flag("nevada.notice")) return g.say("nevada.notice.again");
  await g.say("nevada.notice.big.1", "nevada.notice.big.2", "nevada.notice.big.3");
  g.flag("nevada.notice", true);
  g.closeup();
  await connect(g);
}

// ---------- the gate: where the tracks stop ----------
async function atTheTracks(g) {
  if (!(g.flag("nevada.coinRead") && g.flag("nevada.notice"))) return g.say(`nevada.tracks.early.${who(g)}`);
  await connect(g);
  // all three come and stand at the edge of the glass
  await Promise.all([g.walkTo(206, 180, "mom"), g.walkTo(224, 188, "bigsis"), g.walkTo(190, 190, "lilsis")]);
  for (const id of ["mom", "bigsis", "lilsis"]) { const a = g.actor(id); if (a) a.look(250, 172); }
  // the air over the glass opens a little way, as if it had been waiting for somebody to work it out
  const shimmer = g.q("#shimmer"), rings = g.q("#shimmer-rings");
  g.sfx("portal");
  if (shimmer && rings) await g.tween(1400, (k) => { shimmer.setAttribute("opacity", 0.42 + 0.55 * k); rings.style.transform = `scale(${1 + 1.5 * k})`; }, g.ease.out);
  await g.say("nevada.gate.1", "nevada.gate.2", "nevada.gate.3", "nevada.gate.4", "nevada.gate.5", "nevada.gate.6", "nevada.gate.7");
  g.flag("demo.done", true);
  await g.wait(500);
  await g.fade(1, 900);
  await g.card("To be continued", "End of the demo", { plain: true, ms: 3200 });
  await g.title();
}

export default {
  id: "nevada-roadside",
  era: "nevada",
  name: "The last stop before nothing",

  // Out of doors, but seen from a little above: people shrink gently as they walk away.
  horizon: 60, full: 190,
  walk: { area: [[8, 130], [312, 130], [312, 196], [8, 196]] },

  party: ["mom", "bigsis", "lilsis"],
  spawn: { default: [200, 184], mom: [200, 184], bigsis: [226, 192], lilsis: [174, 176] },

  draw(art) { return art.desertStop(); },

  props: [
    { id: "pump", kind: "pump", at: [100, 131], scale: 0.72, solid: [[92, 127], [108, 127], [108, 133], [92, 133]] },
    { id: "stand", kind: "stand", at: [168, 146], scale: 0.75, solid: [[148, 140], [188, 140], [188, 148], [148, 148]] },
    // Mom's car has come in from the left, and most of it is still off the edge of the picture.
    { id: "car", kind: "car", at: [16, 192], scale: 1.7, solid: [[0, 180], [84, 180], [88, 196], [0, 196]] },
  ],

  actors: [
    { id: "oldtimer", kind: "oldtimer", at: [131, 144], face: "SE" },
    { id: "agent", kind: "agent", at: [259, 133], face: "S", when: (g) => !g.flag("nevada.distracted") },
    { id: "agent", kind: "agent", at: [300, 146], face: "E", when: (g) => !!g.flag("nevada.distracted") },
  ],

  hotspots: [
    { id: "shack", name: "shack", rect: [10, 64, 80, 58], walkTo: [50, 132], face: "N", look: each("nevada.shack") },
    { id: "fence", name: "fence", rect: [186, 80, 56, 42], walkTo: [214, 132], face: "N", look: each("nevada.fence") },
    { id: "notice", name: "notice", verb: "Read", rect: [242, 90, 34, 25], walkTo: [252, 138], face: "N", look: readNotice, use: readNotice },
    { id: "pump", name: "gas pump", rect: [90, 90, 20, 42], walkTo: [100, 137], face: "N", look: each("nevada.pump") },
    { id: "stand", name: "lemonade stand", rect: [148, 110, 42, 38], walkTo: [170, 153], face: "N", look: each("nevada.stand") },
    {
      id: "oldtimer", name: "old-timer", verb: "Talk to", rect: [118, 108, 26, 38], walkTo: [140, 156], face: "NW",
      look: each("nevada.old.look"), use: talkToOldTimer, useWith: { coin: "nevada.old.coin" },
    },
    {
      id: "agent", name: "man in gray", verb: "Talk to", rect: [252, 95, 14, 39], walkTo: [246, 138], face: "NE", when: (g) => !g.flag("nevada.distracted"),
      look: each("nevada.agent.look"), use: talkToAgent,
    },
    {
      id: "agent2", name: "man in gray", verb: "Talk to", rect: [292, 102, 16, 45], walkTo: [282, 151], face: "E", when: (g) => !!g.flag("nevada.distracted"),
      look: each("nevada.agent.look"), use: talkToAgent,
    },
    { id: "car", name: "Mom's car", rect: [0, 142, 82, 50], walkTo: [96, 190], face: "W", look: each("nevada.car.look") },
    {
      id: "tracks", name: "where the tracks stop", verb: "Go to", rect: [222, 140, 58, 40], walkTo: [208, 182], face: "E",
      look: each("nevada.tracks.look"), use: atTheTracks,
    },
  ],

  // Handing the coin over. Big Sister is the one who knows what it is.
  async given(g, item, to) {
    if (item !== "coin") return;
    if (to === "bigsis" && !g.flag("nevada.coinRead")) await readCoin(g);
    else if (to === "lilsis") await g.say("nevada.coin.lilsis");
    else if (to === "mom") await g.say("nevada.coin.mom");
  },

  talk: {
    mom: {
      bigsis: [
        { when: (g) => g.has("coin") && !g.flag("nevada.coinRead"), say: ["nevada.talk.mom.bigsis.coin.a", "nevada.talk.mom.bigsis.coin.b"] },
        ["nevada.talk.mom.bigsis.1a", "nevada.talk.mom.bigsis.1b"],
        ["nevada.talk.mom.bigsis.2a", "nevada.talk.mom.bigsis.2b", "nevada.talk.mom.bigsis.2c"],
      ],
      lilsis: [
        { when: (g) => !g.flag("nevada.distracted"), say: ["nevada.talk.mom.lilsis.gray.a", "nevada.talk.mom.lilsis.gray.b"] },
        ["nevada.talk.mom.lilsis.1a", "nevada.talk.mom.lilsis.1b"],
        ["nevada.talk.mom.lilsis.2a", "nevada.talk.mom.lilsis.2b"],
      ],
    },
    bigsis: {
      mom: [["nevada.talk.bigsis.mom.1a", "nevada.talk.bigsis.mom.1b"], ["nevada.talk.bigsis.mom.2a", "nevada.talk.bigsis.mom.2b", "nevada.talk.bigsis.mom.2c"]],
      lilsis: [
        { when: (g) => !g.flag("nevada.distracted"), say: ["nevada.talk.bigsis.lilsis.gray.a", "nevada.talk.bigsis.lilsis.gray.b"] },
        ["nevada.talk.bigsis.lilsis.1a", "nevada.talk.bigsis.lilsis.1b", "nevada.talk.bigsis.lilsis.1c", "nevada.talk.bigsis.lilsis.1d"],
        ["nevada.talk.bigsis.lilsis.2a", "nevada.talk.bigsis.lilsis.2b"],
      ],
    },
    lilsis: {
      mom: [["nevada.talk.lilsis.mom.1a", "nevada.talk.lilsis.mom.1b"], ["nevada.talk.lilsis.mom.2a", "nevada.talk.lilsis.mom.2b", "nevada.talk.lilsis.mom.2c"]],
      bigsis: [["nevada.talk.lilsis.bigsis.1a", "nevada.talk.lilsis.bigsis.1b", "nevada.talk.lilsis.bigsis.1c"], ["nevada.talk.lilsis.bigsis.2a", "nevada.talk.lilsis.bigsis.2b", "nevada.talk.lilsis.bigsis.2c"]],
    },
  },

  async enter(g) {
    if (g.flag("nevada.arrived")) return;
    await g.wait(500);
    await g.say("nevada.arrive.1", "nevada.arrive.2", "nevada.arrive.3", "nevada.arrive.4");
    g.flag("nevada.arrived", true);
  },
};
