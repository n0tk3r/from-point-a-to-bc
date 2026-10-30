// What the three scenes of Himeji share (SCENES-20C: new in round twenty; briefs/SCENES-20.md, and the design,
// briefs/out/edo-design.md, puzzles #28 to #30). Not a scene (it is in no list of scenes): a module edo-castle.js,
// edo-keep.js, edo-keeptop.js and the cut-scene edo-step.js import, as the Office's scenes import office-common.js. What the
// act's legs share is MERGE-20's (edo-common.js); this is the third leg's own.
//
//   who, heard, each      the lead being played; has a line been said; a look or a use for each of the three
//   holderOf, moveItem    who carries a thing (any lead); a thing moved from whoever has it into a lead's pockets
//   chatter               what a place says by itself now and then (the Office's way: office-common.js chatter)
//   swap                  someone becomes another figure of people.js, keeping his id (the man on the ladder, down)
//   dressAll              the three in the clothes the story has them in at Himeji (hats outdoors; the crew's head-cloth)
//   walkBack              someone walked backwards, facing the way they were, along points (Mom with the mirror)
//   TALK                  what the three say to one another at Himeji (WRITE-20A's companion lines that fit any place)

import { scaleAt } from "../../engine/walk.js";

export const THREE = ["mom", "bigsis", "lilsis"];
export const who = (g) => g.store.data.active;
export const is = (g, fact) => !!g.flag(fact);
/** Has this line been said yet? (The engine counts every line it says.) */
export const heard = (g, id) => !!g.store.data.seenLines[id];
/** A look or a use, one line for each of the three: `${base}.mom` and so on. */
export const each = (base) => ({ mom: `${base}.mom`, bigsis: `${base}.bigsis`, lilsis: `${base}.lilsis` });

/** Who of the three carries a thing (or null). */
export const holderOf = (g, item) => {
  const inv = g.store.data.inventory || {};
  for (const id of THREE) if ((inv[id] || []).includes(item)) return id;
  return null;
};
/** A thing moved into a lead's pockets from whoever has it (nothing said; the picture of the pockets follows the store).
    True if it is there now. */
export function moveItem(g, item, to) {
  const inv = g.store.data.inventory || {}, from = holderOf(g, item);
  if (from === to) return true;
  if (!from || !inv[to]) return false;
  inv[from].splice(inv[from].indexOf(item), 1);
  if (!inv[to].includes(item)) inv[to].push(item);
  g.store.emit();
  return true;
}

// ---------- the player has the controls and nothing is going on ----------
export function idle(g) {
  const lead = g.lead;
  return g.mode === "play" && !!g.scene && !g.busy && !g.dialogue.active && !g.dialogue.choosing && !g.near && !g.ui.open &&
    !(g.atlas && g.atlas.open) && !(lead && lead.walking) && !g.view.hotEl.classList.contains("reveal");
}

/**
 * A place's own talk, a little at a time (as office-common.js does it): every so often, while the player has the controls
 * and nothing is going on, one entry of `list` (a line id, a list of them, or { when, say }), the ones not heard yet first.
 * It holds the controls while it is said, as any script does. Off while the people's own lives are off (`?still`, the tests).
 * A scene makes one, calls reset() in its `setup` and tick(g, dt) in its `tick`; now(g) says the next one at once (tests).
 */
export function chatter(list, { first = [14, 22], every = [36, 56], when = () => true } = {}) {
  const st = { left: 0, n: 0, k: 0 };
  const span = ([a, b]) => (a + (b - a) * [0.5, 0.15, 0.85, 0.35, 0.65][st.k++ % 5]) * 1000;
  const open = (g) => list.filter((e) => !e.when || e.when(g));
  const lines = (e) => [].concat(e.say || e);
  const unheard = (g) => open(g).find((e) => !heard(g, lines(e)[0]));
  const say = (g, e) => (e ? g.run(() => g.say(...lines(e)), { settle: false }) : Promise.resolve());
  return {
    list,
    reset() { st.left = span(first); },
    tick(g, dt) {
      if (!g.life || !g.life.enabled || !when(g) || !idle(g)) return;
      if ((st.left -= dt) > 0) return;
      st.left = span(every);
      const all = open(g);
      if (all.length) say(g, unheard(g) || all[st.n++ % all.length]);
    },
    /** For tests: the next entry, said now. */
    now(g) { const all = open(g); return say(g, unheard(g) || all[st.n++ % Math.max(1, all.length)]); },
  };
}

// ---------- people ----------
/** Someone becomes another figure of js/art/people.js (the same person at another moment), keeping his id, and his place and
    facing unless others are given; made if he is not on the stage at all (as office-common.js swaps them). `scale`: his
    size (none: the depth's, at his feet); `base`: the row he sorts at (none: his feet's). */
export function swap(g, id, kind, at = null, face = null, scale = null, base = null) {
  const cast = g.view.cast, old = cast.get(id);
  const [x, y] = at || (old ? [old.x, old.y] : [400, 500]);
  const yaw = face ?? (old ? old.yaw : "S");
  const hid = old ? old.hidden : false, op = old ? old.opacity : 1;
  if (old && old._stop) old._stop();
  if (old) cast.remove(id);
  const s = scale ?? (g.scene ? scaleAt(g.scene, y) : 1);
  const f = cast.addFigure(id, kind, x, y, s).face(yaw);
  f.hidden = hid; f.opacity = op; f.base = base;
  return f;
}

/** The three in the clothes the story has them in here: O-Tami's travel clothes, the hats on (`edo`), out of doors before
    they are crew; the plasterers' white head-cloth (`edo-crew`) from Tomezō's hook on (#28). Mom holding the mirror up
    is the scene's own (keeptop: `edo-crew-mirror`), and so is Little Sister lying under the cherry. */
export function dressAll(g, outfit) {
  for (const id of THREE) if (g.dressOf && g.dressOf(id) !== outfit) g.dress(id, outfit);
}

/**
 * Someone walked backwards along points, still facing the way they face (the rig walks them; the scene moves them: a tween
 * of x, y and the walk's phase, as PEOPLE-20 says of Mom with the mirror). At their own pace, a little slower, as one walks
 * backwards; the size follows the depth. Resolves at the last point (at once while a cut-scene is skipped).
 */
export async function walkBack(g, id, points, { pace = 0.6 } = {}) {
  const f = g.actor(id), scene = g.scene;
  if (!f || !points.length) return;
  const size = (y) => (scene ? scaleAt(scene, y) : f.scale);
  for (const [x1, y1] of points) {
    const x0 = f.x, y0 = f.y, dist = Math.hypot(x1 - x0, (y1 - y0) * 2.2);
    if (dist < 0.5) continue;
    if (g.clock.skipping) { f.place(x1, y1, size(y1)); continue; }
    const speed = (f.spec.pace || 155) * pace * Math.max(f.scale, 0.5), ms = (dist / speed) * 1000, ph0 = f.phase || 0;
    const stride = (f.stride || 60) * f.scale;
    f.walking = true;
    try {
      await g.tween(ms, (k) => { const x = x0 + (x1 - x0) * k, y = y0 + (y1 - y0) * k; f.place(x, y, size(y)); f.phase = (ph0 + (1 - k) * dist / Math.max(1, stride)) % 1; });
    } finally { f.walking = false; f.t = 0; }
    f.place(x1, y1, size(y1));
  }
  g.rememberPlace(id);
}

/** What the three say to one another at Himeji, when one clicks another: WRITE-20A's companion lines that are not about the
    first leg (lines/edo-a.en.js: reading, Mom's height, the boots, the Son, the word). The ones not heard come first. */
export const TALK = {
  mom: {
    bigsis: [["edo.talk.mom.bigsis.read.a", "edo.talk.mom.bigsis.read.b", "edo.talk.mom.bigsis.read.c"]],
    lilsis: [["edo.talk.mom.lilsis.boots.a", "edo.talk.mom.lilsis.boots.b"]],
  },
  bigsis: {
    mom: [["edo.talk.bigsis.mom.tall.a", "edo.talk.bigsis.mom.tall.b"]],
  },
  lilsis: {
    mom: [["edo.talk.lilsis.mom.son.a", "edo.talk.lilsis.mom.son.b"]],
    bigsis: [{ when: (g) => is(g, "edo.arigato"), say: ["edo.talk.lilsis.bigsis.word.a", "edo.talk.lilsis.bigsis.word.b", "edo.talk.lilsis.bigsis.word.c"] }],
  },
};
