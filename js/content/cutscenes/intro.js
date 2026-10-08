// The intro movie. It is not a video file: it is a script that moves the same art
// the game uses, so it stays small, matches the game's look exactly, has subtitles,
// and can be paused and skipped.
//
// A cutscene is one async function. Each `await` is a beat of the storyboard.
// When the player skips, the engine runs the same function with every wait cut to
// nothing, so the scene always ends in the same place.
//
// Storyboard:
//   1. Studio card on black.
//   2. Dusk. The wagon climbs the road toward the setting sun.
//   3. The sun opens into a portal.
//   4. The road sign rewrites itself: POINT B becomes B.C.
//   5. The wagon drives into the portal. White flash.
//   6. The time tunnel. Years fly past.
//   7. White flash. The title screen takes over (see Game.title).
//
// The road is a painting (art/scenes/highway/). highway.js puts it on the stage, with the parts of it that change.

import { highway, lane, VANISH, NEAR, REST, FAR } from "./highway.js";

const YEARS = ["1969 A.D.", "1492 A.D.", "476 A.D.", "44 B.C.", "1921 B.C."];

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

  // ---- 2. the road at dusk ----
  const road = highway(g, "A desert highway at dusk.");
  road.hole(0);                         // the sun is still the sun,
  road.strike(0);                       // and the sign still says POINT B
  road.bc(0);
  // The wagon is right in front of us, astride the middle of an empty road. It pulls over into its lane as it goes.
  const middle = VANISH[0], side = lane(REST);
  road.drive(NEAR, 1, middle);
  await road.ready;

  await g.fade(0, 900);
  await g.tween(2600, (k) => road.drive(NEAR + (REST - NEAR) * k, 1, middle + (side - middle) * k), ease.out);
  await g.say("intro.1", "intro.2");

  // ---- 3. the sky opens where the sun should be ----
  g.sfx("portal");
  await g.tween(1500, (k) => road.hole(k), ease.out);
  await g.say("intro.3", "intro.4");

  // ---- 4. the sign changes its mind ----
  g.sfx("paint");
  await g.tween(450, (k) => road.strike(k));
  await g.tween(350, (k) => road.bc(k));
  await g.wait(800);

  // ---- 5. into the portal ----
  road.bounce(false);
  await g.tween(1500, (k) => road.drive(REST + (FAR - REST) * k, 1 - k * k * k), ease.in);
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
