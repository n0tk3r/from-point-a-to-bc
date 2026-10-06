// Entry point: gather the content, hand it to the engine, start.
// The engine (js/engine) knows nothing about this particular story.
// The story (js/content) knows nothing about how the engine works inside.

import { Game } from "./engine/game.js";
import { cast, eras, items } from "./content/world.js";
import { lines } from "./content/lines.en.js";
import { story } from "./content/story.js";
import { sound } from "./content/sound.js";
import { sceneIds, loadScene } from "./content/scenes/index.js";
import intro from "./content/cutscenes/intro.js";

const cutscenes = { intro };

const game = new Game({ sceneIds, loadScene, cutscenes, cast, eras, items, lines, story, sound });
window.game = game;      // for the browser console while building the game
game.boot();
