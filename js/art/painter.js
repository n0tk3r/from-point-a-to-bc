// A worker that paints people (paint.js), away from the game's own thread.
//
// Painting one picture of a person takes some milliseconds: on a slow machine, ten to thirty at twice the stage's
// size. That is too long to do in the middle of a frame, so when people are painted (?people=painted) the cast
// (js/engine/cast.js) asks this worker for each picture it does not have yet, goes on showing the nearest picture it
// does have, and uses the new one the moment it arrives. The worker draws with the game's own rig and people, so the
// pictures are exactly those the game would paint itself.
//
// A message is one picture: { id, kind, up, seat, pose, yaw, size, k, keyId }:
//   kind   the person (js/art/people.js)       up     true: someone found sitting, on their feet (rig.js upOf)
//   seat   true: only the seat drawn with them (rig.js drawSeat)
//   pose   the pose, as the rig's `poses` give it    yaw, size, k   as drawFigure takes them (size in painted pixels)
//   keyId  the colour key it is wanted in (paint.js colourKey.id; "" for none)
// or a portrait: { id, kind, portrait: n } (rig.js portraitOf: n pixels square, never in a colour key: it belongs to
// the interface), answered { id, blob } (a PNG) or { id, w, h, data }.
// The answer: { id, w, h, ox, oy, bitmap } (the picture cut down to its paint; ox, oy the point between the feet), or
// { id, stale: true } when this worker is in another colour key than the one asked for, or { id, error }.
//
// A message { import: url, call, args } loads a module here as well (and then calls its export `call` with `args`): a
// colour key (paint.js setColourKey) that a study sets in the game's own thread is set in this one by loading its
// module here too (cast.js keyPainter). The answer: { id: null, keyed } (the colour key this worker now paints in).

import { drawFigure, drawSeat, upOf, portraitOf } from "./rig.js";
import { people } from "./people.js";
import { colourKey, unkeyed } from "./paint.js";

/** The picture cut down to the part with paint on it. */
function crop(sf) {
  const { w, h, out } = sf;
  let x0 = w, x1 = -1, y0 = h, y1 = -1;
  for (let y = 0, i = 0; y < h; y++) for (let x = 0; x < w; x++, i++) {
    if (!(out[i] >>> 24)) continue;
    if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
  }
  if (x1 < 0) return { w: 1, h: 1, ox: sf.ox, oy: sf.oy, data: new Uint8ClampedArray(4) };
  const cw = x1 - x0 + 1, ch = y1 - y0 + 1, data = new Uint8ClampedArray(cw * ch * 4), src = new Uint8ClampedArray(out.buffer, out.byteOffset, out.byteLength);
  for (let y = 0; y < ch; y++) data.set(src.subarray(((y0 + y) * w + x0) * 4, ((y0 + y) * w + x1 + 1) * 4), y * cw * 4);
  return { w: cw, h: ch, ox: sf.ox - x0, oy: sf.oy - y0, data };
}

// Messages are taken strictly one after another (a module being loaded is waited for before the next picture), so a
// picture asked for after a colour key is never painted before the key is set.
let turn = Promise.resolve();
self.onmessage = (event) => {
  const job = event.data;
  turn = turn.then(() => handle(job)).catch((err) => self.postMessage({ id: (job && job.id) ?? null, error: String((err && err.message) || err) }));     // (one failure never stops the rest)
};

async function handle(job) {
  if (job && job.import) {
    try {
      const mod = await import(job.import);
      if (job.call) await mod[job.call](...(job.args || []));
      self.postMessage({ id: null, keyed: colourKey.id });
    } catch (err) {
      self.postMessage({ id: null, keyed: colourKey.id, error: "The painter could not load " + job.import + ": " + err });
    }
    return;
  }
  try {
    const base = people[job.kind];
    if (!base) throw new Error(`no person called "${job.kind}"`);
    if (job.portrait) {                                                  // a portrait: the whole square, as a PNG if this browser can make one here
      const sf = unkeyed(() => portraitOf(base, job.portrait)), data = new Uint8ClampedArray(sf.out.buffer, sf.out.byteOffset, sf.out.byteLength).slice();
      if (typeof OffscreenCanvas === "function") {
        try {
          const oc = new OffscreenCanvas(sf.w, sf.h);
          oc.getContext("2d").putImageData(new ImageData(data, sf.w, sf.h), 0, 0);
          self.postMessage({ id: job.id, blob: await oc.convertToBlob({ type: "image/png" }) });
          return;
        } catch { /* (then as pixels) */ }
      }
      self.postMessage({ id: job.id, w: sf.w, h: sf.h, data }, [data.buffer]);
      return;
    }
    if ((job.keyId || "") !== colourKey.id) { self.postMessage({ id: job.id, stale: true }); return; }
    const spec = job.up ? upOf(base) : base;
    const sf = job.seat ? drawSeat(spec, job.yaw, job.size, { k: job.k }) : drawFigure(spec, job.pose, job.yaw, job.size, { paint: { k: job.k } });
    const c = crop(sf);
    let bitmap = null;
    try { if (typeof createImageBitmap === "function") bitmap = await createImageBitmap(new ImageData(c.data, c.w, c.h)); } catch { bitmap = null; }
    if (bitmap) self.postMessage({ id: job.id, w: c.w, h: c.h, ox: c.ox, oy: c.oy, bitmap }, [bitmap]);
    else self.postMessage({ id: job.id, w: c.w, h: c.h, ox: c.ox, oy: c.oy, data: c.data }, [c.data.buffer]);
  } catch (err) {
    self.postMessage({ id: job.id, error: String((err && err.message) || err) });
  }
}
