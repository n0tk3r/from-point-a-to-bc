// The intro movie. It is not a video file: it is a script that moves the same art
// the game uses, so it stays small, matches the game's look exactly, has subtitles,
// and can be paused and skipped.
//
// A cutscene is one async function. Each `await` is a beat of the storyboard.
// When the player skips, the engine runs the same function with every wait cut to
// nothing, so the scene always ends in the same place.
//
// Storyboard (ROAD-18M: round eighteen, driving):
//   1. Studio card on black.
//   2. Dusk, driving. The movie fades in with the camera right behind the wagon (only the luggage on its roof in the
//      picture) and the world already going by. The wagon draws ahead to the chase distance and over into its lane, and
//      from then on the camera follows it: the road comes at us under it, poles and brush sweep past, the mesas and the
//      sun stay put. The Son and Dad talk as they drive.
//   3. The sun opens into a portal while they drive; its glow runs down the moving road.
//   4. The sign, POINT B, 40, comes up far ahead, and the camera eases to a stop with the world exactly the painting's.
//      The wagon does not stop: it drives on alone, smaller and smaller, and disappears into the hole.
//   5. A breath. The sign changes its mind: the rings run over the board and POINT B comes out POINT B.C. A breath to read it.
//   6. White flash. The time tunnel. Years fly past.
//   7. White flash. The title screen takes over (see Game.title): the wagon cruising toward the open hole, no sign.
//
// The road is driven down (art/scenes/highway/, the engine's `drive` seen straight ahead). highway.js puts it on the
// stage, with the parts of it that change.

import { highway, lane, VANISH, NEAR, REST, FAR, CHASE, SPEED, zAt } from "./highway.js";

const YEARS = ["1969 A.D.", "1492 A.D.", "476 A.D.", "44 B.C.", "1921 B.C."];
const BRAKE = 60;                       // ROAD-18M: metres the camera takes to stop in (eased out over 2 * BRAKE / SPEED seconds, 4.8 s: no jolt)
const AHEAD = 260;                      // ROAD-18M: at least this far ahead the sign is when it comes up (a speck at the end of the road)
const POLES = 40;                       // ROAD-18M: the camera stops on a multiple of this (the poles' spacing): they stand where the painting has them

export default async function intro(g) {
  const { ease } = g;

  // ---- 1. studio card ----
  g.view.clear();
  g.titleEl.hidden = true;
  g.view.setEra("present");
  await g.fade(1, 0);
  g.music("road");
  await g.wait(400);
  await g.card("n0tk3r presents", "", { plain: true, ms: 1700 });

  // ---- 2. dusk, driving ----
  const road = highway(g, "A desert highway at dusk. A family station wagon drives toward the setting sun.");
  const fx = road.fx;
  road.hole(0);                         // the sun is still the sun,
  road.bend(0);                         // and the sign still says POINT B
  road.bc(0);
  // The wagon is right in front of us, astride the middle of the road, and the world already going by. It draws ahead to
  // the chase distance and over into its lane; from then on the camera follows it.
  const middle = VANISH[0], side = lane(REST);
  road.drive(NEAR, 1, middle);
  road.cruise(SPEED);
  const [stopping] = await Promise.all([road.stopping(), road.ready]);

  await g.fade(0, 900);
  await g.tween(2600, (k) => road.drive(NEAR + (REST - NEAR) * k, 1, middle + (side - middle) * k), ease.out);
  await g.say("intro.1", "intro.2");

  // ---- 3. the sky opens where the sun should be, while they drive ----
  g.sfx("portal");
  await g.tween(1500, (k) => road.hole(k), ease.out);
  await g.say("intro.3", "intro.4");

  // ---- 4. the sign comes up far ahead; the camera eases to a stop, and the wagon drives on into the hole ----
  // Where the camera will stop: a multiple of 40 m at least AHEAD on, so that the poles stand where the painting has them.
  // The world it stops in is set out now, while that stretch of road is still a speck (nothing near enough to be seen changes).
  const STOP = Math.ceil(((fx ? fx.s : 0) + AHEAD) / POLES) * POLES;
  road.stopAt(STOP, stopping);
  while (fx && fx.s < STOP - BRAKE && !g.clock.skipping) await g.wait(20);
  const from = fx ? fx.s : STOP, ms = ((2 * (STOP - from)) / SPEED) * 1000;
  let wagon = from + CHASE;                                           // where the wagon is along the road: it keeps its speed
  await g.tween(ms, (u) => {
    // ease out: the camera leaves its speed at once and stops gently, on STOP exactly; carried with its speed at each moment
    // (set({ s, speed }): between two frames of the tween it goes on at that speed, so that the hand-over has no hitch)
    const s = STOP - (STOP - from) * (1 - u) * (1 - u), speed = u < 1 ? (SPEED * (1 - u)) : 0;
    if (fx) fx.set({ s, speed });
    wagon = from + CHASE + (SPEED * u * ms) / 1000;
    road.at(wagon - s);
  }, ease.linear);
  // the world has stopped; the wagon goes on, smaller and smaller, into the hole (fading as it goes in)
  road.bounce(false);
  const z0 = wagon - STOP, z1 = zAt(FAR), go = ((z1 - z0) / SPEED) * 1000;
  await g.tween(Math.max(0, go), (u) => road.at(z0 + (z1 - z0) * u, 1 - Math.pow(Math.max(0, (u - 0.55) / 0.45), 3)), ease.linear);
  road.drive(FAR, 0);

  // ---- 5. a breath; then the sign changes its mind: the rings run over it, and the letters come through changed ----
  await g.wait(700);
  g.sfx("portal");
  await g.tween(500, (k) => road.bend(k), ease.out);
  await g.tween(650, (k) => road.bc(k));
  road.bc(1);
  await g.tween(750, (k) => road.bend(1 - k), ease.in);
  await g.wait(1200);                   // a breath to read it
  g.sfx("flash");
  await g.fade(1, 300, "#fff");

  // ---- 6. the tunnel ----
  g.view.clear();
  g.view.setEra("tunnel");
  g.startTunnel(YEARS);
  g.music("tunnel");
  await g.fade(0, 300, "#fff");
  await g.wait(1100);
  await g.say("intro.5", "intro.6");
  await g.wait(1000);
  g.sfx("flash");
  await g.fade(1, 300, "#fff");
  g.stopTunnel();
  // ---- 7. whoever played the intro shows the title next ----
}
