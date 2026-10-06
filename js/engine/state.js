// Game state: the one object a save file stores. Nothing else needs saving, because
// every scene rebuilds itself from this state when it is entered.
// Keep it plain data (no functions, no DOM), so it can be written as JSON.

export const SAVE_VERSION = 1;

export function newGame() {
  return {
    v: SAVE_VERSION,
    startedAt: new Date().toISOString(),
    playMs: 0,
    act: 1,
    scene: null,              // id of the scene the active character is in
    active: "dad",            // which lead the player controls: "dad" or "son"
    where: { dad: null, son: null },   // each lead's scene and position, for when they are apart
    inventory: { dad: [], son: [] },
    flags: {},                // story facts: flags["egypt.metScribe"] = true
    seenLines: {},            // dialogue already heard, so repeats can be shortened
  };
}

export class Store {
  constructor() {
    this.data = newGame();
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
}
