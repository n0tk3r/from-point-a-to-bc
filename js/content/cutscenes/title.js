// What is behind the title screen: the highway at dusk, driven down (ROAD-18M: round eighteen; before it, the still
// painting as the movie left it). The hole in time is open at the end of the road, the sign has been passed (it is no
// longer in the picture: the game's name above still makes the joke), and the camera is behind the wagon at the chase
// distance, cruising toward the hole with the road and the desert streaming past, bouncing gently, on and on with no seam
// (the road loops every 64 m; the things beside it are worked out from a seed and never repeat).
// The engine calls this to dress the stage, waits for it, and then puts the game's name and the menu over it (Game.title).
//
// The road is driven down (art/scenes/highway/). highway.js puts it on the stage, with the parts of it that change.

import { highway, REST, SPEED } from "./highway.js";

export default async function title(g) {
  const road = highway(g, "Dusk on a desert highway. A family station wagon cruises toward a swirling time portal at the end of the road.");
  road.hole(1);
  road.bend(0);
  road.drive(REST);
  road.cruise(SPEED);
  await road.ready;
}
