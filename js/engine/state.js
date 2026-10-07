// Game state: the one object a save file stores. Nothing else needs saving, because
// every scene rebuilds itself from this state when it is entered.
// Keep it plain data (no functions, no DOM), so it can be written as JSON.

export const SAVE_VERSION = 3;

/** A new game. `leads` are the ids of everyone the player can ever control (cast entries marked lead: true). */
export function newGame(leads = ["dad", "son"]) {
  return complete({
    v: SAVE_VERSION,
    startedAt: new Date().toISOString(),
    playMs: 0,
    act: 1,
    scene: null,              // id of the scene the active character is in
    active: leads[0],         // which lead the player controls
    team: [],                 // the leads the player can switch between right now
    where: {},                // each lead's scene and position: { scene, x, y, face }, x and y in picture pixels (800x600)
    inventory: {},            // each lead's pockets
    flags: {},                // story facts: flags["egypt.metScribe"] = true
    seenLines: {},            // dialogue already heard, so repeats can be shortened
  }, leads);
}

/** Give a state a place and pockets for every lead. A save made before someone joined the cast has neither for them. */
export function complete(data, leads) {
  data.where = data.where || {};
  data.inventory = data.inventory || {};
  for (const id of leads) {
    if (!(id in data.where)) data.where[id] = null;
    if (!Array.isArray(data.inventory[id])) data.inventory[id] = [];
  }
  data.team = (Array.isArray(data.team) ? data.team : []).filter((id) => leads.includes(id));
  data.flags = data.flags || {};
  data.seenLines = data.seenLines || {};
  return data;
}

export class Store {
  constructor(data = newGame()) {
    this.data = data;
    this.listeners = new Set();
  }

  reset(data = newGame()) { this.data = data; this.emit(); }
  on(fn) { this.listeners.add(fn); return () => this.listeners.delete(fn); }
  emit() { for (const fn of this.listeners) fn(this.data); }

  flag(name, value) {
    if (value === undefined) return this.data.flags[name];
    this.data.flags[name] = value;
    this.emit();
    return value;
  }

  get items() { return this.data.inventory[this.data.active]; }
  has(item) { return this.items.includes(item); }
  give(item) { if (!this.has(item)) { this.items.push(item); this.emit(); } }
  take(item) {
    const i = this.items.indexOf(item);
    if (i >= 0) { this.items.splice(i, 1); this.emit(); }
  }
  /** Hand a thing from the active lead's pockets to another lead's. */
  pass(item, to) {
    const i = this.items.indexOf(item), pockets = this.data.inventory[to];
    if (i < 0 || !pockets) return false;
    this.items.splice(i, 1);
    if (!pockets.includes(item)) pockets.push(item);
    this.emit();
    return true;
  }
  /** Who is carrying a thing, or null. */
  holder(item) {
    for (const [who, pockets] of Object.entries(this.data.inventory)) if (pockets.includes(item)) return who;
    return null;
  }
}
