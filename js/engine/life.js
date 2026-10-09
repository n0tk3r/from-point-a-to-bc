// The people's own lives.
//
// Everyone in a scene who is not one of the family (the scene's `actors`) lives a little while the player is busy
// elsewhere. Every few seconds one of them does something small where they are: shifts their weight, looks about,
// rubs the back of their neck (each person's own movements: `figure.fidgets` and `figure.fidget(name)`, drawn by the
// rig). And now and then, if their scene says how, something bigger: whoever sits stands up, walks a few steps to a
// place of their own, stretches or looks at something there, walks back and sits down again; whoever stands strolls
// a little way off and comes back.
//
// A scene says how each person lives, in their entry under `actors`:
//
//   { id: "scribe", kind: "scribe", at: [150, 448], face: "E",
//     life: {
//       fidget: true,                         small movements where they are, every few seconds (the default, for everyone).
//                                             false: none; [4, 9]: every 4 to 9 seconds
//       every: [18, 40],                      seconds between bigger moments, picked at random in the range
//       spots: [[178, 462, "E"], [120, 470, "S"]],     where they may go, and which way they face there
//       stay: [3, 8],                         seconds they stay there, doing a fidget or two
//       stand: true,                          someone seated stands up first, and sits down again on coming back
//       when: (g) => !g.flag("egypt.writing"),         only while the story allows (and only while their own `when` holds)
//       still: false,                         true: fidgets only, never leaves the mark (a guard at a door)
//     } },
//
// With no `life` a person fidgets now and then, a little at a time, and never leaves their mark.
//
// What the engine sees to, so that a scene never has to:
//   - It all runs on the game clock, so it stops with the menu. Nothing starts while a script has control, while anyone
//     is talking or choosing what to say, in a cutscene, during a close look at something, or while Show is on.
//   - One person in a scene is away at a time, and nobody goes anywhere in the first 6 to 10 seconds after a scene opens.
//   - A place is picked only if the way there and back keeps 60 pixels or more from the family; whoever is away turns
//     for home if one of the family comes within 60 pixels of the way they still have to go.
//   - Nobody is talked to away from home. When anything starts a script (a click on a person, a thing used on them or
//     given to them, a look), whoever is away, or up from their seat, walks briskly home and sits down while the lead
//     walks over, and the script starts once both are done (after about two seconds at most, they are simply put
//     there). Scripts can go on assuming that everyone is on their mark. A script can ask for it as well:
//     `await g.settle()` (everyone) or `await g.settle("scribe")`.
//   - Their clickable area (the one with their id, or one that says `actor: "<id>"`) goes with them while they are away:
//     a box round the figure, outlined by the figure itself in Show. Back on their mark, the scene's own shape applies.
//   - Their place on the ground is kept for them while they are away; where they stand still meanwhile is blocked.
//   - Nothing is saved. A game loaded, or a scene entered, has everyone on their mark.
//   - `index.html?still`, or game.life.enabled = false, turns all of it off (for tests). With the "less motion" option
//     the small movements stay and the walks stop.
//
// The person who draws people gives a figure `sit(false)` (stand up from the seat) and `sit(true)` (sit down again),
// `seated` (which of the two they are in now), `fidget(name)` and `fidgets` (the names that suit them). A figure that
// has none of these yet is handled as well as it can be: someone seated stays seated and only fidgets, and a fidget is
// a glance to one side and back.

import { scaleAt } from "./walk.js";

const OPEN = [6, 10];            // seconds after a scene opens before anyone goes anywhere
const GAP = [3, 7];              // seconds after one person is home before the next may go
const FIRST = 0.35;              // the first bigger moment comes this far into a person's `every`
const CLEAR = 60;                // pixels between the family and anyone's way there and back
const EASY = 0.8, BRISK = 1.75;  // walking pace, against the person's own: a stroll, and a brisk walk home
const CAP = 2000;                // milliseconds a script waits for everyone to be home before they are put there
const ALONE = [7, 15];           // seconds between fidgets for someone whose scene says nothing of their life
const LIVELY = [4, 10];          // and for someone whose scene gives them one
const GLANCE = [0.8, 1.6];       // seconds a glance aside lasts (the stand-in fidget, for a figure that has none of its own)
const SIT_MS = 1100;             // how long standing up or sitting down takes, for a figure that does not say

/** A small random number generator with a seed: the same scene opened twice lives the same life. */
function seeded(text) {
  let h = 2166136261;
  for (let i = 0; i < text.length; i++) h = Math.imul(h ^ text.charCodeAt(i), 16777619);
  return () => {
    h = (h + 0x6d2b79f5) | 0;
    let t = Math.imul(h ^ (h >>> 15), 1 | h);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const within = (rnd, [a, b]) => a + (b - a) * rnd();

/** How far a point is from a path (a list of points walked in turn). */
function away(pt, path) {
  let best = Infinity;
  for (let i = 0; i < path.length; i++) {
    const a = path[i], b = path[Math.min(i + 1, path.length - 1)];
    const dx = b[0] - a[0], dy = b[1] - a[1], len = dx * dx + dy * dy;
    const k = len ? Math.max(0, Math.min(1, ((pt[0] - a[0]) * dx + (pt[1] - a[1]) * dy) / len)) : 0;
    best = Math.min(best, Math.hypot(pt[0] - (a[0] + k * dx), pt[1] - (a[1] + k * dy)));
  }
  return best;
}

/** What a scene's `life` says, with everything it leaves out filled in. */
export function lifeOf(actor) {
  const l = (actor && actor.life) || {};
  const spots = Array.isArray(l.spots) ? l.spots.filter((s) => Array.isArray(s) && s.length >= 2 && isFinite(s[0]) && isFinite(s[1])) : [];
  return {
    fidget: l.fidget === false ? null : Array.isArray(l.fidget) ? l.fidget : actor && actor.life ? LIVELY : ALONE,
    every: Array.isArray(l.every) ? l.every : [18, 40],
    spots,
    stay: Array.isArray(l.stay) ? l.stay : [3, 8],
    stand: l.stand !== false,
    when: typeof l.when === "function" ? l.when : null,
    walks: !l.still && spots.length > 0,
  };
}

export class Life {
  constructor(game) {
    this.g = game;
    let on = true;
    try { on = !new URLSearchParams(location.search).has("still"); } catch { /* (no address to read: on) */ }
    this._on = on;
    this.scene = null;
    this.folk = new Map();        // the scene's people, by id: what is known of each one's life
    this.out = null;              // the one person who is away on a walk of their own, if anyone is
    this.homing = 0;              // how many calls to settle() are waiting for people to get home
    game.clock.every(() => this.tick());
  }

  /** On (the default), or off: `index.html?still`, or game.life.enabled = false. Turned off, anyone away is put home at once. */
  get enabled() { return this._on; }
  set enabled(on) {
    this._on = !!on;
    if (!this._on) for (const p of this.folk.values()) if (p.trip) this.put(p);
    if (!this._on) for (const p of this.folk.values()) this.unglance(p);
  }

  // ---------------------------------------------------------------- a scene opens
  /** A scene has been built: everyone is on their mark. The first small movements come in a few seconds, and the first walk not before 6 to 10. */
  enter(scene) {
    this.drop();
    const now = this.g.clock.now;
    this.scene = scene;
    this.rnd = seeded(scene.id);
    this.nextAt = now + within(this.rnd, OPEN) * 1000;
    for (const a of scene.actors || []) {
      if (this.folk.has(a.id)) continue;                // (one person under two marks, each with its own `when`: one life)
      const p = { id: a.id, rnd: seeded(scene.id + "|" + a.id), trip: null, glance: null, last: null, fidgetAt: 0, dueAt: 0, sits: null, up: null };
      const how = lifeOf(a);
      p.fidgetAt = now + within(p.rnd, [1.5, 6]) * 1000;
      p.dueAt = Math.max(this.nextAt, now + within(p.rnd, how.every) * FIRST * 1000);
      this.folk.set(a.id, p);
    }
  }

  /** The scene has gone (another is coming, or the title): forget it. The figures went with it, so nothing is put back. */
  drop() {
    for (const p of this.folk.values()) if (p.trip) { p.trip.dead = p.trip.gone = true; p.trip.end(); }
    this.folk.clear();
    this.out = null;
    this.scene = null;
  }

  // ---------------------------------------------------------------- what is true now
  /** The entry under `actors` that is this person now: the first with their id whose `when` holds. */
  entry(id) {
    for (const a of (this.scene && this.scene.actors) || []) if (a.id === id && (!a.when || a.when(this.g))) return a;
    return null;
  }

  /** May anything happen now? Not in a script, a cutscene, a conversation, a close look, a menu, or while Show is on. */
  quiet() {
    const g = this.g;
    return this._on && g.mode === "play" && !!g.scene && g.scene === this.scene && !g.busy && !g.dialogue.active && !g.dialogue.choosing &&
      !g.near && !g.ui.open && !g.view.hotEl.classList.contains("reveal");
  }

  /** This person, if they are free to do something of their own: { a, f, how }. Not while the story wants them otherwise. */
  free(p) {
    const g = this.g, a = this.entry(p.id), f = g.actor(p.id);
    if (!a || !f || typeof f.walkPath !== "function" || f.hidden || !(f.opacity > 0) || f.talking || f.act) return null;
    const how = lifeOf(a);
    if (how.when && !how.when(g)) return null;
    return { a, f, how };
  }

  /** Is the figure sitting now? (The figure says, once the people's `sit` is there; until then, whoever is found sitting is.) */
  sitting(f, p = null) {
    if (typeof f.seated === "boolean") return f.seated;
    if (p && p.up != null) return !p.up;                                  // (a figure that does not say: what life last asked of it)
    return !!(f.spec && f.spec.seated);
  }
  /** Can the figure get up from its seat, and sit down again? */
  canStand(f) { return typeof f.sit === "function"; }
  /** On their mark. */
  onMark(a, f) { return Math.abs(f.x - a.at[0]) <= 4 && Math.abs(f.y - a.at[1]) <= 4; }
  /** At home: on their mark, and sitting if they sit there (as they were when the scene opened). */
  home(p, a, f) { return this.onMark(a, f) && (p.sits == null || this.sitting(f, p) === p.sits); }
  /** Away from home on a walk of their own (and so their clickable area goes with them). */
  isAway(id) { const p = this.folk.get(id); return !!(p && p.trip); }
  /** Has this person's area keyboard focus (Tab)? Then nobody walks off with it. */
  focused(id) { const s = this.g.outlines && this.g.outlines.focused; return !!s && (s.actor || s.id) === id; }

  /** How big they are with their feet at y: as everyone else, or in proportion to a size the scene gave them. */
  sizeAt(a, y) { const s = this.g.scene; return a.scale ? (a.scale * scaleAt(s, y)) / scaleAt(s, a.at[1]) : scaleAt(s, y); }

  /** The family on the stage: the lead and anyone else of the team standing here. */
  family() {
    const g = this.g, d = g.store.data, out = [];
    for (const id of new Set([d.active, ...(d.team || [])])) { const f = g.actor(id); if (f && !f.hidden) out.push(f); }
    return out;
  }
  /** Does this way keep clear of all of the family? */
  clear(path) { return this.family().every((f) => away([f.x, f.y], path) >= CLEAR); }

  /** A way from one place to another for one person, on `map` (game.groundFor: the ground less their own place): round
      things, on the floor; or, for someone whose own ground is off the floor the family walks on (behind a counter, a
      table), straight there. Null if there is no way. */
  route(map, from, to) {
    if (!map.ok(from[0], from[1])) return [[to[0], to[1]]];
    let end = [to[0], to[1]];
    if (!map.ok(end[0], end[1])) {                                       // (a place just inside the margin round something: as near as it goes)
      const near = map.nearest(end[0], end[1]);
      if (Math.hypot(near[0] - end[0], near[1] - end[1]) > 8) return [end];
      end = near;
    }
    const r = map.path(from, end), last = r[r.length - 1];
    return Math.hypot(last[0] - end[0], last[1] - end[1]) <= 3 ? r : null;
  }

  // ---------------------------------------------------------------- every frame
  tick() {
    const g = this.g;
    if (!this.scene) return;
    if (g.scene !== this.scene) { this.drop(); return; }   // (gone to the title, which builds no scene)
    this.follow();                                          // a clickable area goes with whoever is away
    if (this.homing) return;                                // everyone is on the way home: settle() is in charge
    const now = g.clock.now, quiet = this.quiet();
    for (const p of this.folk.values()) {
      if (p.sits == null && !p.trip) { const f = g.actor(p.id); if (f && f.spec) p.sits = this.sitting(f); }      // (as the scene opened: sitting, or standing)
      if (p.glance && (!quiet || now >= p.glance.until)) this.unglance(p);
    }
    if (!quiet) { this.halt(); return; }
    if (this.out) this.watch(this.out);
    for (const p of this.folk.values()) {
      if (now < p.fidgetAt || p.trip) continue;
      const it = this.free(p);
      if (!it || it.f.walking) { p.fidgetAt = now + 1200; continue; }
      if (!it.how.fidget) { p.fidgetAt = now + 5000; continue; }
      this.fidget(p, it.f);
      p.fidgetAt = now + within(p.rnd, it.how.fidget) * 1000;
    }
    if (!this.out && !g.calm && now >= this.nextAt) this.wander(now);
  }

  /** Time for someone's bigger moment? The one most overdue goes, if they are free, at home, and there is somewhere clear to go. */
  wander(now) {
    let best = null;
    for (const p of this.folk.values()) {
      if (now < p.dueAt) continue;
      const it = this.free(p);
      if (!it || !it.how.walks || it.f.walking || !this.home(p, it.a, it.f) || this.focused(p.id)) continue;
      if (this.sitting(it.f, p) && (!it.how.stand || !this.canStand(it.f))) continue;      // (someone seated who cannot get up stays put)
      if (!best || p.dueAt < best.p.dueAt) best = { p, ...it };
    }
    if (!best) return;
    const plan = this.plan(best.p, best.a, best.how);
    if (plan) this.go(best.p, plan);
    else best.p.dueAt = now + within(best.p.rnd, [3, 6]) * 1000;           // nowhere clear of the family just now: try again soon
  }

  /** Where this person might go now: one of their spots whose way there and back keeps clear of the family. `n` asks for one in particular. */
  plan(p, a, how, n = null) {
    const list = n != null ? [how.spots[n]].filter(Boolean) : [...how.spots];
    if (n == null) for (let i = list.length - 1; i > 0; i--) { const j = Math.floor(p.rnd() * (i + 1)); [list[i], list[j]] = [list[j], list[i]]; }
    const map = this.g.groundFor(p.id);
    for (const spot of list) {
      const there = this.route(map, a.at, spot);
      if (!there) continue;
      const end = there[there.length - 1], back = this.route(map, end, a.at);
      if (!back) continue;
      if (this.clear([a.at, ...there, ...back])) return { spot, there, back };
    }
    return null;
  }

  // ---------------------------------------------------------------- a bigger moment
  /** Start a person's walk: up, there, a little while there, back, down. */
  go(p, plan) {
    const t = { spot: plan.spot, back: plan.back, goal: "spot", pace: EASY, phase: "up", dead: false, gone: false };
    t.ended = new Promise((done) => { t.end = done; });
    p.trip = t;
    this.out = p;
    this.unglance(p);
    this.trip(p, t)
      .catch((err) => console.warn(`Life: ${p.id}'s walk stopped:`, err))
      .finally(() => this.done(p, t));
    return t;
  }

  async trip(p, t) {
    const g = this.g;
    const a = this.entry(p.id), f0 = g.actor(p.id);
    if (!a || !f0) return;
    const how = lifeOf(a), sits = p.sits ?? this.sitting(f0, p);
    if (sits) { t.phase = "up"; await this.posture(p, t, false); }        // up from the seat
    if (t.dead) return;
    g.remap();                                                            // (their place is kept for them, and they block nothing while they walk)
    if (t.goal === "spot") {
      t.phase = "out";
      const there = await this.walk(p, t, t.spot, () => t.goal === "spot");
      if (there && t.goal === "spot" && !t.dead) {
        t.phase = "there";
        const f = g.actor(p.id);
        if (t.spot[2] != null) f.face(t.spot[2]);
        t.back = this.route(g.groundFor(p.id), [f.x, f.y], a.at) || [a.at];
        g.remap();                                                        // where they stand now is taken
        const stay = within(p.rnd, how.stay) * 1000, from = g.clock.now;
        await this.pause(t, 350);
        let n = 0;
        while (t.goal === "spot" && !t.dead && g.clock.now - from < stay) {
          if (n < 2 && this.quiet() && !f.walking) { this.fidget(p, f); n++; }
          await this.pause(t, Math.min(stay - (g.clock.now - from), n < 2 ? within(p.rnd, [1.6, 3]) * 1000 : 400));
        }
        this.unglance(p);
      }
    }
    if (t.dead) return;
    t.phase = "back";
    g.remap();
    await this.walk(p, t, a.at, () => true);
    if (t.dead) return;
    const f = g.actor(p.id);
    if (f) f.face(a.face ?? "S");
    if (sits) { t.phase = "down"; await this.posture(p, t, true); }
    t.phase = "home";
  }

  /** Walk to a place, again and again if something stops them on the way, for as long as `keep()` says to. True when they are there. */
  async walk(p, t, to, keep) {
    const g = this.g;
    for (let tries = 0; tries < 12; tries++) {
      if (t.dead || !keep()) return false;
      const f = g.actor(p.id), a = this.entry(p.id) || { at: to };
      if (!f) return false;
      if (Math.hypot(f.x - to[0], f.y - to[1]) < 1.5) { f.place(to[0], to[1], this.sizeAt(a, to[1])); return true; }    // (near enough: exactly there)
      await this.until(t, () => t.dead || !keep() || t.pace === BRISK || this.quiet());
      if (t.dead || !keep()) return false;
      const route = this.route(g.groundFor(p.id), [f.x, f.y], to) || [[to[0], to[1]]], end = route[route.length - 1];
      const clock = g.clock;
      const paced = { every: (fn) => clock.every((dt, now) => fn(dt * t.pace, now)), get skipping() { return clock.skipping; } };
      await f.walkPath(paced, route, (y) => this.sizeAt(a, y));
      // There: or as near as the ground lets them (a spot just inside the margin round something). Stopped on the way, again.
      if (!t.dead && keep() && Math.hypot(f.x - end[0], f.y - end[1]) < 1.5 && Math.hypot(end[0] - to[0], end[1] - to[1]) >= 1.5) return true;
    }
    return false;
  }

  /** Stand up (`down` false) or sit down (`down` true), and wait while it plays. */
  async posture(p, t, down) {
    const f = this.g.actor(p.id);
    if (!f || !this.canStand(f) || this.sitting(f, p) === down) return;
    let r;
    try { r = f.sit(down); } catch (err) { console.warn(`Life: ${p.id} could not ${down ? "sit down" : "stand up"}:`, err); return; }
    p.up = !down;
    if (r && typeof r.then === "function") await Promise.race([r, this.until(t, () => t.dead)]);
    else await this.pause(t, f.sitMs ?? SIT_MS, () => !t.dead);            // (the whole movement, whenever the figure starts calling itself seated)
  }

  /** Game time passing (`ms`), cut short when the walk is over or turns for home (or `keep()` stops holding). */
  pause(t, ms, keep = () => !t.dead && t.goal === "spot") {
    if (!(ms > 0)) return Promise.resolve();
    return new Promise((done) => {
      let left = ms;
      const stop = this.g.clock.every((dt) => { left -= dt; if (left <= 0 || !keep()) { stop(); done(); } });
    });
  }

  /** Until a test holds (checked every frame, on the game clock). */
  until(t, test) {
    if (test()) return Promise.resolve();
    return new Promise((done) => { const stop = this.g.clock.every(() => { if (t.dead || test()) { stop(); done(); } }); });
  }

  /** The family is coming near the way they have still to go: home, at an easy pace. */
  watch(p) {
    const t = p.trip, f = this.g.actor(p.id), a = this.entry(p.id);
    if (!t || t.goal !== "spot" || !f || !a) return;
    const left = [[f.x, f.y], ...(t.phase === "there" ? [] : [t.spot]), ...(t.back || [a.at])];
    if (!this.clear(left)) { t.goal = "home"; this.nudge(p); }
  }

  /** Stop the walk under way, so that it can be planned again (for home, or briskly). */
  nudge(p) { const f = this.g.actor(p.id); if (f && f.walking && f._stop) f._stop(); }

  /** Something needs the stage (Show is on, a line is being said): whoever is walking stops where they are until it is over. */
  halt() { const p = this.out; if (p && p.trip && p.trip.pace !== BRISK) this.nudge(p); }

  /** A walk is over: whenever the next may be. */
  done(p, t) {
    t.end();
    if (t.gone || (p.trip && p.trip !== t)) return;                       // (the scene has gone; or this walk was cut short, and a newer one has begun)
    const g = this.g, a = this.entry(p.id), f = g.actor(p.id), cut = p.trip !== t;
    p.trip = null;
    if (this.out === p) this.out = null;
    if (cut) return;                                                      // (put() has seen to the rest)
    if (a && f && (!this.onMark(a, f) || (p.sits != null && this.canStand(f) && this.sitting(f, p) !== p.sits))) this.put(p);     // (a walk that could not finish: home it is)
    this.rest(p);
    g.remap();
    this.follow();
  }

  /** After a walk: the next small movement in a few seconds, the next walk of theirs in `every`, and anyone's in a few seconds more. */
  rest(p) {
    const now = this.g.clock.now, a = this.entry(p.id);
    p.dueAt = now + within(p.rnd, lifeOf(a).every) * 1000;
    p.fidgetAt = now + within(p.rnd, [2.5, 6]) * 1000;
    this.nextAt = Math.max(this.nextAt, now + within(this.rnd, GAP) * 1000);
  }

  /** Put someone home at once: on their mark, facing as the scene says, sitting if they sit. */
  put(p) {
    const g = this.g, t = p.trip, a = this.entry(p.id), f = g.actor(p.id);
    if (t) { t.dead = true; t.end(); p.trip = null; if (this.out === p) this.out = null; this.rest(p); }     // (the walk winds itself up on its next frame: see done)
    if (!a || !f) return;
    if (f._stop) f._stop();
    f.place(a.at[0], a.at[1], this.sizeAt(a, a.at[1])).face(a.face ?? "S");
    if (p.sits != null && this.canStand(f) && this.sitting(f, p) !== p.sits) { try { f.sit(p.sits, true); p.up = !p.sits; } catch { /* (it eases down instead) */ } }
    g.remap();
    this.follow();
  }

  // ---------------------------------------------------------------- nobody is talked to away from home
  /**
   * Everyone who is away (or only `who`: an id, or a list of them) goes home now, briskly, and sits down if they sit.
   * Resolves when they are all there, or after about two seconds of game time, when they are simply put there.
   */
  settle(who = null) {
    const want = who == null ? null : [].concat(who);
    for (const p of this.folk.values()) if (!want || want.includes(p.id)) this.unglance(p);
    const out = [...this.folk.values()].filter((p) => p.trip && (!want || want.includes(p.id)));
    if (!out.length) return Promise.resolve();
    for (const p of out) { p.trip.goal = "home"; p.trip.pace = BRISK; this.nudge(p); }
    this.homing++;
    let stop = null;
    const cap = new Promise((done) => {
      let left = CAP;
      stop = this.g.clock.every((dt) => { left -= dt; if (left <= 0 || this.g.clock.skipping) done(); });
    });
    return Promise.race([Promise.all(out.map((p) => p.trip.ended)), cap]).then(() => {
      stop();
      for (const p of out) if (p.trip && !p.trip.gone) this.put(p);
      this.homing--;
      return Promise.all(out.map((p) => p.trip ? p.trip.ended : null));
    }).then(() => undefined);
  }

  // ---------------------------------------------------------------- small movements
  /** One small movement: one of the person's own, not the one they did last; or, for a figure that has none, a glance aside. */
  fidget(p, f) {
    const list = typeof f.fidgets === "function" ? f.fidgets() : f.fidgets;
    const names = Array.isArray(list) ? list.filter(Boolean) : [];
    if (typeof f.fidget === "function" && names.length) {
      let name = names[Math.floor(p.rnd() * names.length)];
      if (name === p.last && names.length > 1) name = names[(names.indexOf(name) + 1) % names.length];
      p.last = name;
      try { f.fidget(name); } catch (err) { console.warn(`Life: ${p.id} could not ${name}:`, err); }
      return name;
    }
    if (this.sitting(f, p)) return null;                                  // (a glance means turning: someone seated stays as they are)
    const side = p.rnd() < 0.5 ? -45 : 45;
    p.glance = { yaw: f.yaw, to: (((f.yaw + side) % 360) + 360) % 360, until: this.g.clock.now + within(p.rnd, GLANCE) * 1000 };
    f.face(p.glance.to);
    p.last = "glance";
    return "glance";
  }
  /** The glance aside is over: back as they were (unless something else has turned them since). */
  unglance(p) {
    const gl = p.glance, f = this.g.actor(p.id);
    p.glance = null;
    if (gl && f && f.yaw === gl.to && !f.walking) f.face(gl.yaw);
  }

  // ---------------------------------------------------------------- their clickable areas go with them
  /** A box round the figure as it is drawn now, a few pixels outside it: [x, y, w, h]. */
  box(f) {
    const cast = this.g.view.cast, pic = f.picture && f.picture(cast.palette, cast.calm);
    if (!pic || !pic.canvas) return null;
    const w = pic.w ?? pic.canvas.width, h = pic.h ?? pic.canvas.height, x = f.x - pic.ox, y = f.y - pic.oy;
    return [Math.floor(x) - 3, Math.floor(y) - 3, Math.ceil(w) + 6, Math.ceil(h) + 6];
  }

  /** Each person's own area: round them wherever they are while they are away; the scene's own shape when they are home. */
  follow() {
    const g = this.g, spots = g.view.spots;
    for (let i = 0; i < spots.length; i++) {
      const s = spots[i], home = s.home;
      if (!home) continue;                                                // (only people's own areas: see rebuildSpots in game.js)
      const id = s.actor || s.id, f = this.isAway(id) ? g.actor(id) : null, box = f && this.box(f);
      if (box) {
        if (s.rect && s.rect.every((v, k) => v === box[k])) continue;
        s.rect = box; s.poly = undefined; s.circle = undefined;
      } else {
        if (s.rect === home.rect && s.poly === home.poly && s.circle === home.circle) continue;
        s.rect = home.rect; s.poly = home.poly; s.circle = home.circle;
      }
      g.view.reshape(i);
      if (g.outlines && g.outlines.focused === s) g.outlines.changed();       // (an area with keyboard focus keeps its outline round them)
    }
  }

  // ---------------------------------------------------------------- for tests
  /** Who is where: [{ id, x, y, at, home, seated, away, phase, spot }] for each person of the scene on the stage. */
  where() {
    const g = this.g, out = [];
    for (const p of this.folk.values()) {
      const f = g.actor(p.id), a = this.entry(p.id);
      if (!f || !a) continue;
      out.push({ id: p.id, x: f.x, y: f.y, at: a.at, home: this.home(p, a, f), seated: this.sitting(f, p), away: !!p.trip,
        phase: p.trip ? p.trip.phase : null, spot: p.trip ? p.trip.spot : null, fidget: p.last, walks: lifeOf(a).walks });
    }
    return out;
  }
  /** Start someone's bigger moment now (to one spot in particular if `n` is given): their spot, or null if they cannot go
      now (someone else is away, they are not free or not home, or no spot keeps clear of the family). */
  force(id, n = null) {
    const p = this.folk.get(id);
    if (!p || this.out || !this.quiet()) return null;
    const it = this.free(p);
    if (!it || !it.how.spots.length || it.f.walking || !this.home(p, it.a, it.f)) return null;
    if (this.sitting(it.f, p) && (!it.how.stand || !this.canStand(it.f))) return null;
    const plan = this.plan(p, it.a, it.how, n);
    if (!plan) return null;
    this.go(p, plan);
    return plan.spot;
  }
  /** Resolves when nobody is away. */
  idle() { return new Promise((done) => { const stop = this.g.clock.every(() => { if (!this.out && !this.homing) { stop(); done(); } }); }); }
}
