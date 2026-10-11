// What is behind the title screen: the highway at dusk as the opening movie leaves it. The hole in time is open
// at the end of the road, the sign has changed its mind, and the wagon is on its way, bouncing gently.
// The engine calls this to dress the stage, waits for it, and then puts the game's name and the menu over it (Game.title).
//
// The road is a painting (art/scenes/highway/). highway.js puts it on the stage, with the parts of it that change.

import { highway, REST } from "./highway.js";

export default async function title(g) {
  const road = highway(g, "Dusk on a desert highway. A family station wagon heads for a swirling time portal, past a road sign that now reads POINT B.C.");
  road.hole(1);
  road.bend(0);
  road.bc(1);                           // the sign has changed its mind
  road.drive(REST);
  await road.ready;
}
