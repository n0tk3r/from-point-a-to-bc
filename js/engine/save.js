// Saving and loading.
// 1. Slots in the browser (localStorage): one autosave and three manual slots.
// 2. A save FILE the player can keep: exported as JSON to their computer and
//    loaded back into the online game from any browser or device.
// Every save carries a version and a checksum, so old or damaged files are
// caught and old versions can be upgraded step by step.

import { SAVE_VERSION } from "./state.js";

const MAGIC = "from-point-a-to-bc";
const SLOT_KEY = "pabc.save.";
const SETTINGS_KEY = "pabc.settings";
export const SLOTS = ["auto", "1", "2", "3"];

export const defaultSettings = {
  music: 0.7, sfx: 0.8, voice: 1.0,
  subtitles: true,       // text on screen; stays on by default even with voices
  voices: true,          // play recorded lines when they exist
  textSpeed: 1,          // 0.6 slow, 1 normal, 1.6 fast
  calm: false,           // less motion and no flashes (also on when the system asks for reduced motion)
  seenIntro: false,      // the intro plays by itself once; after that it is on the title menu
};

// FNV-1a: a small, fast checksum. It catches accidents, not determined cheaters.
function checksum(text) {
  let h = 0x811c9dc5;
  for (let i = 0; i < text.length; i++) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h.toString(16).padStart(8, "0");
}

/** Wrap game state in the envelope that goes to a slot or a file. */
export function pack(data, meta = {}) {
  const body = { magic: MAGIC, v: SAVE_VERSION, savedAt: new Date().toISOString(), meta, data };
  body.check = checksum(JSON.stringify(data));
  return body;
}

// Upgrades from older save versions. migrations[1] turns a version 1 save into version 2.
const migrations = {
  // 1 -> 2. The switch between Dad and the Son became a list, `team`, so that any number of leads
  // can be in play, and the end of the Rome scene stopped being the end of the game.
  // (Places and pockets for the leads who joined later are added when the save is loaded.)
  1: (data) => {
    const flags = data.flags || {};
    data.team = flags["leads.switch"] ? ["dad", "son"] : [];
    if (flags["demo.done"]) { flags["rome.tossed"] = true; delete flags["demo.done"]; }
    return data;
  },
  // 2 -> 3. The stage became one 800x600 painted picture. Places saved before that are on the old 320x200
  // grid and mean nothing on the new pictures, so they are forgotten: each lead keeps their scene, and
  // appears on that scene's own mark for them when it is next built.
  2: (data) => {
    for (const place of Object.values(data.where || {})) if (place) { delete place.x; delete place.y; }
    return data;
  },
};

/** Check an envelope and return it with its data upgraded to the current version. */
export function unpack(body) {
  if (!body || body.magic !== MAGIC) throw new Error("This is not a From Point A to B.C. save file.");
  if (checksum(JSON.stringify(body.data)) !== body.check) throw new Error("This save file is damaged or was edited.");
  if (body.v > SAVE_VERSION) throw new Error("This save is from a newer version of the game.");
  let data = body.data;
  for (let v = body.v; v < SAVE_VERSION; v++) {
    if (!migrations[v]) throw new Error(`No upgrade path from save version ${v}.`);
    data = migrations[v](data);
  }
  data.v = SAVE_VERSION;
  return { ...body, v: SAVE_VERSION, data };
}

// ---- slots ----
export function writeSlot(slot, data, meta) {
  try {
    localStorage.setItem(SLOT_KEY + slot, JSON.stringify(pack(data, meta)));
    return true;
  } catch (err) {       // private windows and full storage both end up here
    console.warn("Could not write save slot", slot, err);
    return false;
  }
}

export function readSlot(slot) {
  try {
    const text = localStorage.getItem(SLOT_KEY + slot);
    return text ? unpack(JSON.parse(text)) : null;
  } catch (err) {
    console.warn("Could not read save slot", slot, err);
    return null;
  }
}

export function listSlots() {
  return SLOTS.map((slot) => ({ slot, save: readSlot(slot) }));
}

// ---- files ----
function fileName(body) {
  const d = new Date(body.savedAt), two = (n) => String(n).padStart(2, "0");
  const stamp = `${d.getFullYear()}-${two(d.getMonth() + 1)}-${two(d.getDate())}-${two(d.getHours())}${two(d.getMinutes())}`;
  return `point-a-to-bc-save-${stamp}.json`;   // the player's local date and time
}

/** Save to the player's computer. Returns "picker", "download" or "cancelled". */
export async function exportFile(body) {
  const text = JSON.stringify(body, null, 2);
  const name = fileName(body);
  if (window.showSaveFilePicker) {          // Chrome and Edge: a real Save dialog
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: name,
        types: [{ description: "From Point A to B.C. save game", accept: { "application/json": [".json"] } }],
      });
      const out = await handle.createWritable();
      await out.write(text);
      await out.close();
      return "picker";
    } catch (err) {
      if (err.name === "AbortError") return "cancelled";
      // anything else: fall through to a plain download
    }
  }
  const url = URL.createObjectURL(new Blob([text], { type: "application/json" }));
  const link = Object.assign(document.createElement("a"), { href: url, download: name });
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  return "download";
}

/** Read a save file the player picked or dropped on the game. */
export async function importFile(file) {
  if (file.size > 2_000_000) throw new Error("That file is too large to be a save game.");
  let body;
  try { body = JSON.parse(await file.text()); }
  catch { throw new Error("That file is not a save game."); }
  return unpack(body);
}

// ---- settings: kept apart from saves, so loading a save never changes the volume ----
export function loadSettings() {
  try { return { ...defaultSettings, ...JSON.parse(localStorage.getItem(SETTINGS_KEY) || "{}") }; }
  catch { return { ...defaultSettings }; }
}

export function storeSettings(settings) {
  try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings)); } catch { /* not fatal */ }
}
