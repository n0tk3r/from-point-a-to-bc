// Entry point: gather the content, hand it to the engine, start.
// The engine (js/engine) knows nothing about this particular story.
// The story (js/content) knows nothing about how the engine works inside.

import { Game } from "./engine/game.js";
import { cast, eras, items } from "./content/world.js";
import { lines } from "./content/lines.en.js";
import { story } from "./content/story.js";
import { sound } from "./content/sound.js";
import { sceneIds, loadScene } from "./content/scenes/index.js";
import { maps } from "./content/maps.js";                    // MAP-15: the maps, and the places and ways on them
import intro from "./content/cutscenes/intro.js";
import title from "./content/cutscenes/title.js";
import backup from "./content/cutscenes/backup.js";        // NEVADA-12SC: the cut-scene "Backup", which closes Act Four
import officeArrive from "./content/cutscenes/office-arrive.js";      // SCENES-17: "A Very Small Building With A Very Long Name"
import officeDown from "./content/cutscenes/office-down.js";          // SCENES-17: "Going Down", the end of the demo

const cutscenes = { intro, title, backup, "office-arrive": officeArrive, "office-down": officeDown };      // "title" is not played: it dresses the stage behind the title screen (NEVADA-12SC: backup; SCENES-17: the Office's two)

const game = new Game({ sceneIds, loadScene, cutscenes, cast, eras, items, lines, story, sound, maps });      // (MAP-15: maps)
window.game = game;      // for the browser console while building the game
game.boot();
