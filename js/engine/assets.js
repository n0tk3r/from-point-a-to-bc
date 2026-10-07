// Painted pictures: backdrops, cut-outs, inventory icons.
//
// A picture is named by its path from the top of the site ("art/scenes/egypt-crash/back.png"),
// whichever page asks for it. Like the code and the style sheets, every picture has an address
// that changes when the file does: tools/stamp.py writes each one's fingerprint into the page,
// and the fetch uses it. So a browser never shows a picture it kept from an older version next
// to code from a newer one. A picture that is not in the page's list still loads, by its plain address.
//
// A picture is fetched ONCE in a session, and the file is then held here, in memory, until the
// page is closed. Whatever shows it after that (the backdrop, the cast, an inventory button, a
// drawing in the live layer) is given the held copy and never asks the server again. That is what
// lets the game fetch everything quietly behind the title (game.js, gather) and then play on from
// what it holds: a version published half-way through somebody's game cannot hand them a new
// picture to go with their old code. All the game's pictures together are a few megabytes.

let stamps = {};
try { stamps = JSON.parse(document.getElementById("art-stamps").textContent) || {}; } catch { /* a page that has not been stamped */ }

/** Where a file is on the server, given its path from the top of the site. Works from index.html and from the pages in tools/. */
function onServer(path) {
  const address = new URL("../../" + path, import.meta.url);     // this file is two folders down from the top
  if (stamps[path]) address.searchParams.set("v", stamps[path]);
  return address.href;
}

const fetching = new Map();   // path -> a promise of the held copy's address
const held = new Map();       // path -> that address, once the file is here
const asked = new Map();      // path -> a promise of the picture
const have = new Map();       // path -> the picture, once it is ready to paint

/**
 * The address to give a picture element (<img src>, <image href>): of the copy held for this session once
 * the file has arrived, and of the file on the server until then. Ask each time it is needed; do not keep the answer.
 */
export function url(path) { return held.get(path) || onServer(path); }

/**
 * Fetch a file, once, and hold it for the rest of the session. Resolves with the held copy's address.
 * Nothing is decoded: this is the cheap way to have a picture here before it is wanted.
 * `quiet` marks a fetch nobody is waiting for, so the browser lets everything else go first.
 * It never rejects: a file that will not come resolves with null, and is asked for again the next time something wants it.
 */
export function hold(path, { quiet = false } = {}) {
  let wait = fetching.get(path);
  if (wait) return wait;
  wait = fetch(onServer(path), quiet ? { priority: "low" } : {})
    .then((reply) => { if (!reply.ok) throw new Error(`${reply.status}`); return reply.blob(); })
    .then((file) => { const address = URL.createObjectURL(file); held.set(path, address); return address; })
    .catch(() => { fetching.delete(path); return null; });
  fetching.set(path, wait);
  return wait;
}

/** Is this file held already? */
export const holding = (path) => held.has(path);

/**
 * A picture, ready to paint: fetched (or taken from what is held), decoded, and kept. Resolves with the image.
 * It never rejects: a picture that will not load resolves with null, with a warning in the console,
 * and is asked for again the next time something wants it.
 */
export function picture(path) {
  let wait = asked.get(path);
  if (wait) return wait;
  wait = hold(path).then((address) => new Promise((done) => {
    const no = () => {
      asked.delete(path);
      if (address) { fetching.delete(path); held.delete(path); URL.revokeObjectURL(address); }     // it came, but it is not a picture
      console.warn(`A picture would not load: ${path}`);
      done(null);
    };
    if (!address) return no();
    const img = new Image();
    const ok = () => { have.set(path, img); done(img); };
    img.src = address;
    if (img.decode) img.decode().then(ok, no);
    else { img.onload = ok; img.onerror = no; }
  }));
  asked.set(path, wait);
  return wait;
}

/** A picture that has already arrived, or null. For code that paints every frame and cannot wait. */
export const got = (path) => have.get(path) || null;
