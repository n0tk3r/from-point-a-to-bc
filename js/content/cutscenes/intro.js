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

const YEARS = ["1969 A.D.", "1492 A.D.", "476 A.D.", "44 B.C.", "1250 B.C.", "2560 B.C."];

export default async function intro(g) {
  const { art, ease } = g;

  // ---- 1. studio card ----
  g.view.clear();
  g.titleEl.hidden = true;
  g.view.setEra("present");
  await g.fade(1, 0);
  g.music("road");
  await g.wait(400);
  await g.card("n0tk3r presents", "", { plain: true, ms: 1700 });

  // ---- 2. the road at dusk ----
  g.view.draw(art.frame(art.highway({ sun: true }), "A desert highway at dusk."));
  const portal = g.q("#portal"), sun = g.q("#sun"), roadGlow = g.q("#road-glow-shape");
  const strike = g.q("#sign-strike"), bc = g.q("#sign-bc");
  portal.style.opacity = 0;
  portal.style.transform = "scale(0.01)";
  roadGlow.style.opacity = 0;
  strike.style.strokeDashoffset = 1;
  bc.style.opacity = 0;
  const wagon = g.view.addActor("wagon", "wagon", 160, 250, 2.8).flag("bounce", true);

  await g.fade(0, 900);
  await g.tween(2600, (k) => wagon.place(160 + 24 * k, 250 - 68 * k, 2.8 - 1.8 * k), ease.out);
  await g.say("intro.1", "intro.2");

  // ---- 3. the sky opens where the sun should be ----
  g.sfx("portal");
  await g.tween(1500, (k) => {
    portal.style.opacity = k;
    portal.style.transform = `scale(${Math.max(k, 0.01)})`;
    sun.style.opacity = 1 - k;
    roadGlow.style.opacity = k;
  }, ease.out);
  await g.say("intro.3", "intro.4");

  // ---- 4. the sign changes its mind ----
  g.sfx("paint");
  await g.tween(450, (k) => { strike.style.strokeDashoffset = 1 - k; });
  await g.tween(350, (k) => { bc.style.opacity = k; });
  await g.wait(800);

  // ---- 5. into the portal ----
  wagon.flag("bounce", false);
  await g.tween(1500, (k) => wagon.place(184 - 24 * k, 182 - 66 * k, 1 - 0.95 * k).fade(1 - k * k * k), ease.in);
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
