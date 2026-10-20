// The highway at dusk: the stage of the opening movie (intro.js) and of the title screen (title.js), driven down
// (ROAD-18M: round eighteen; before it the camera stood still on one painting and the wagon was drawn smaller up the road).
//
// The camera is behind the wagon, a chase camera, at the painting's own place and height (tools/paint/highway.py, CAM: the
// horizon on row 330, the vanishing point (400, 330) in the middle of the sun, focal 800, the eye 2.70 m above the middle
// of the road). The road and the desert go by under it and beside it, drawn by the engine's `drive` seen straight ahead
// (effects.js, side: "ahead"), from the painter's pictures in art/scenes/highway/ (tools/paint/highway_drive.py paints
// them all from the painting's own code, and its first lines say everything about them):
//
//   sky.png               the painting with nothing standing in it: the sky, the clouds, the mesas, the far plain. The
//                         backdrop, still: too far to move
//   drive-road.png        the road from straight above, 48 px a metre, a 64 m loop; where the camera stops (a multiple
//                         of 64 m) its cracks, patches and dashes are the painting's own
//   drive-desert-l, -r    the desert either side, 6 to 30 m out, 24 px a metre, the same loop; the brush field lies in it
//                         (round dark clumps seen from above, gold on their sunward side, in the painting's drifts)
//   drive-far-l, -r       the plain and the brush field on from 30 to 150 m out, 8 px a metre, the same loop
//   drive-things.png/json the upright things, seen from behind against the low sun: the pole (its six wires hang from its
//                         insulators), reflector posts, fence posts, sagebrush near, middling and far, tufts, stones,
//                         Joshua trees, the tumbleweed; the sign, POINT B and POINT B.C.; and the painting's own things cut
//                         out of it (stop-*, the windpump), each at the size it is where the camera stops
//   drive-stop.json       where those stand when the camera stops: the painting's world, set out on the road
//   light-shade, -glow    the painting's light that stays on the screen while the ground goes by (the dust on fire at the
//                         horizon, the long shine down the road, the corners going deeper), laid over the ground
//   sun.png               the sun's disc, half sunk at the end of the road (on the live layer, as before)
//   sign-bc.png, back.png the sign's second board and the still painting: round seventeen's, kept (nothing shows them now:
//                         the drive's `sign-bc` is that board, and the stop is the painting, set out as pieces)
//   wagon-rear-0, -1      the family wagon from behind: two pictures, for the bounce of the road
//
// The hole in time is the engine's `portal`, rising out of the sun as it opens; it reads the moving road into the paint
// it bends (`under: { fx: "road" }`), and its glow down the road is a light of the drive's (id "hole": the drive covers
// the live layer below the horizon). The sign is a set piece of the drive's, and its own rings read the drive and bring
// the sign through as it will be (`{ fx: "road", piece: "sign", sprite: "sign-bc" }`, an alpha bc() turns from 0 to 1).
//
// highway(g, words) puts all of it on the stage and hands back the few things a script does with it:
//
//     const road = highway(g, "A desert highway at dusk.");
//     road.cruise(SPEED);  road.drive(REST);               the camera behind the wagon, following it at 25 m a second
//     await road.ready;                                    every picture is here and the road's tables are made: fade in
//     await g.tween(1500, (k) => road.hole(k));            the sun opens into the hole
//     road.stopAt(STOP, await road.stopping());            the world the camera will stop in (see intro.js)
//     road.at(z)                                           the wagon z metres ahead of the camera (it climbs the road)
//     await g.tween(500, (k) => road.bend(k));             rings over the sign...
//     await g.tween(600, (k) => road.bc(k));               ...and POINT B comes out POINT B.C.
//
// Each takes a number from 0 to 1 (or a place), so a tween can run it and a skipped movie lands on the same picture.

const ART = "art/scenes/highway/";

// ---------- the road ----------
export const VANISH = [400, 330];       // where the road ends, and the middle of the sun's disc
export const EYE = 2.7, FOCAL = 800;    // ROAD-18M: the painting's camera (the eye's height in metres; the focal length in pixels)
const LANE = (550 - 400) / (600 - 330); // the wagon keeps to the right-hand lane, whose middle runs from the vanishing point down to (550, 600)
/** How far across the picture the middle of that lane is, on a given row. */
export const lane = (row) => VANISH[0] + (row - VANISH[1]) * LANE;
const FULL = 518.4;                     // the painter's rule for its size: (row of its back wheels - 330) / 518.4 of the size it is painted
const FOOT = [251, 419];                // the point of the wagon's picture that is on the road: the middle of the back axle

export const REST = 548;                // "on its way": back wheels on row 548, which puts it at (521, 548), 0.42 of its painted size
export const NEAR = 935;                // close behind it, as the movie opens: so near that only the luggage on its roof is in the picture
export const FAR = 343;                 // almost at the end of the road: a speck, in the mouth of the hole
/** ROAD-18M: the row of the stage that the road z metres ahead of the camera is on, and the other way about. */
export const rowAt = (z) => VANISH[1] + (FOCAL * EYE) / z;
export const zAt = (row) => (FOCAL * EYE) / (row - VANISH[1]);
export const CHASE = zAt(REST);         // ROAD-18M: 9.91 m, the chase distance (the wagon's back wheels on row 548)
export const SPEED = 25;                // ROAD-18M: metres a second (55 mph): a pole goes by in a second and a half
export const SIGN_Z = 17.3;             // ROAD-18M: the sign, when the camera has stopped: the painting's picture
const SIGN_X = 5.96;                    // ROAD-18M: the sign's foot across the road (midway between its posts)

// ---------- the hole in time ----------
const HOLE = 64;                        // its radius when it is open (its middle rises out of the sun by as much)
// ---------- the sign ----------
const BOARD = [599, 287, 752, 377];     // the painter's board (layout.json: sign.board), x0 y0 x1 y1
const B_AT = [733, 316];                // the middle of the B of POINT B: the rings that change the sign spread from here
const SIGN_R = 44;                      // their radius, drawn 2.4 times as wide as high: the whole board, and the paint beside it, is in their reach

// ROAD-18M: the drive. The rows are the painter's (its preview, highway_drive_check.py ROWS) thinned to some 500 things a
// picture: the poles every 40 m with their six wires at the painting's insulators ([across, up] from the foot) and running
// on through the stop (gap: false; the stop is a multiple of 40, so they stand where the painting has them); the reflector
// posts every 18 m; the far fences every 5 m with their two wires (the painting's 5.2 m would never come round to the stop:
// 5 m does, and its posts are within a metre or two of the painting's); the brush near, middling and far, its stones and
// tufts folded in; now and then a Joshua tree or a tumbleweed. The haze is a colour (the painter's, keyed) and with the
// painting's two lights the road reads as the painting's. The glow the hole throws down the road is the light "hole".
const ROAD = {
  id: "road", type: "drive", side: "ahead", vanish: VANISH, focal: FOCAL, eye: EYE, speed: 0,
  // (ROAD-18M, PAINT-18B: five grounds, the brush field painted into the four deserts; the far strips only with these near ones)
  grounds: [{ src: ART + "drive-far-l.png", from: -150, to: -30, ppm: 8 },
    { src: ART + "drive-desert-l.png", from: -30, to: -6, ppm: 24 }, { src: ART + "drive-road.png", from: -6, to: 6, ppm: 48 },
    { src: ART + "drive-desert-r.png", from: 6, to: 30, ppm: 24 }, { src: ART + "drive-far-r.png", from: 30, to: 150, ppm: 8 }],
  things: { src: ART + "drive-things.png", rows: [
    { sprite: "pole", every: 40, at: -7.5, offset: 18, gap: false, far: 520, wire_alpha: 0.9,
      wires: [[-1.04, 8.24], [-0.58, 8.24], [0.58, 8.24], [1.04, 8.24], [-0.8, 7.46], [0.8, 7.46]] },
    { sprite: "post", every: 18, at: 3.52, offset: 12.4, far: 220 }, { sprite: "post", every: 18, at: -3.52, offset: 21.4, far: 220 },
    { sprite: ["fence-1", "fence-2"], every: 10, at: [-14.6, 14.6], offset: 3.4, gap: false, far: 220, wire_alpha: 0.35, wires: [1.09, 0.65] },
    { sprite: ["sage-1", "sage-2", "sage-3", "sage-4", "sage-5", "sage-6", "tuft-1", "tuft-2", "stone-1", "stone-3"], every: [1.4, 4.4], at: [3.4, 12], both: true, far: 200 },
    { sprite: ["sage-1-mid", "sage-2-mid", "sage-3-mid", "sage-4-mid", "tuft-1", "stone-2"], every: [2, 6], at: [12, 30], both: true, far: 240 },
    { sprite: ["sage-1-far", "sage-2-far", "sage-3-far", "sage-4-far"], every: [3, 8], at: [30, 90], both: true, far: 240 },
    { sprite: ["joshua-1", "joshua-2"], every: [140, 320], at: [14, 70], both: true, far: 700 },
    { sprite: "tumbleweed", every: [150, 400], at: [3.6, 14], both: true, far: 300 } ] },
  sun: [-5.5, 0], shade: "#5c4a86", shade_k: 0.55,
  haze: "#febb85", haze_far: 120, far: 1500, things_far: 1500,
  light: [{ id: "shade", src: ART + "light-shade.png", blend: "multiply" }, { id: "glow", src: ART + "light-glow.png", blend: "screen" },
    { id: "hole", poly: [[VANISH[0] - 2, VANISH[1] + 1], [VANISH[0] + 2, VANISH[1] + 1], [710, 600], [90, 600]], radial: { at: [400, 331], r: [527, 228.65] },
      stops: [[0, "#7ff5ff", 0.45], [1, "#7ff5ff", 0]], opacity: 0 }],
  seed: 21,
};

// ROAD-18M: the painting's own things where the camera stops are set out on the road as pieces, but not the poles and
// fences (their rows run through the stop, wires and all), and (MERGE-18B) not those the ground carries now or nobody
// could pick out: a piece costs a picture as much whether it is seen or not, and the brake should be as quick as the
// cruise. The brush field is painted into the deserts (PAINT-18B: whole from FIELD, 16 m, out; thin by the road), and
// out there a bush, a stone or a tuft under 16 px is no more than the field's own. So: every piece SEEN_WHOLE (16) pixels
// tall or more where the camera stops; the brush, stones and tufts by the road (inside FIELD) from SEEN_NEAR (10) pixels;
// the painting's few odd things (the windpump, the posts, the birds, the jackrabbit, the tumbleweeds, the tread, the
// hubcap, the bottle) from SEEN (2). Beyond the haze (120 m) only the windpump is kept. 260 of the 757.
const SEEN = 2, SEEN_NEAR = 10, SEEN_WHOLE = 16, FIELD = 16;
/** ROAD-18M: is this piece of the painting's (drive-stop.json) set out where the camera stops? `sp`: its sprite in the
    drive's tables (its pictures and pixels a metre), for its height there in pixels. */
export function keepAtStop(p, sp) {
  if (!sp || !sp.levels || !sp.levels[0]) return true;
  const h = (FOCAL * (sp.levels[0].h / sp.ppm)) / p.z;                                   // (its height in metres, from the sheet)
  if (h >= SEEN_WHOLE) return true;
  if (h < SEEN) return false;
  if (/^stop-(bush|stone|tuft)/.test(p.sprite)) return Math.abs(p.X) < FIELD && h >= SEEN_NEAR;     // (the field's, out from FIELD)
  return true;
}

/**
 * Set the stage. `words` describes the picture for someone who cannot see it.
 * Returns { ready, wagon, fx, stopping(), drive(row, opacity, x), at(z, opacity), bounce(on), cruise(speed), stopAt(STOP, pieces),
 * hole(k), bend(k), bc(k) }.
 */
export function highway(g, words) {
  const [vx, vy] = VANISH;
  // LIGHT ON THE LIVE LAYER: the sun's disc only (ROAD-18M: the glow down the road is the drive's now, and so is the sign)
  const live = `<image id="sun" href="${g.assets.url(ART + "sun.png")}" width="800" height="600" style="image-rendering:pixelated"/>`;
  const drawn = g.view.draw("", words, { picture: ART + "sky.png", live, grid: [800, 600] });

  // The road (first: the doors in time read what it draws in the same frame). Then the hole in time: the paint bending in
  // rings from the sun's middle, the hole rising out of the sun's disc as it opens (round ten; effects.js, `portal`), the
  // sun and the moving road read into it. On the cast layer at the road's end, so the wagon is drawn over it as it drives
  // in. Shut until hole() opens it. (The stage was cleared for this road: whatever moved on it before goes too.)
  g.effects.drop(g.scene);
  const fx = g.effects.add(ROAD);
  const hole = g.effects.add({ id: "hole", type: "portal", at: [vx, vy], r: HOLE, rise: true, base: vy + 1, pale: "#fff2c8", under: [{ src: ART + "sun.png", x: 0, y: 0 }, { fx: "road" }] });
  // The sign's own rings (round twelve): from the B, across the board and no farther sideways (`keep`), the drive's own
  // sign read in as it will be, POINT B.C., as much as bc() says.
  const board = { fx: "road", piece: "sign", sprite: "sign-bc", alpha: 0 };
  const sign = g.effects.add({ id: "sign", type: "portal", at: B_AT, r: SIGN_R, wide: 2.4, keep: [BOARD[0], BOARD[2]], base: vy + 2, pale: "#fff2c8", strength: 0.8, under: [{ fx: "road" }, board] });
  const wagon = g.view.cast.addPicture("wagon", { frames: [ART + "wagon-rear-0.png", ART + "wagon-rear-1.png"], fps: 4, foot: FOOT });
  const road = {
    wagon, fx,
    /** Resolves when every picture is here, the backdrop is painted and the road's tables are made. */
    ready: Promise.all([drawn, g.view.cast.load(), g.assets.picture(ART + "sun.png"), fx ? fx.ready() : null]),
    /** The painting's own things at the moment the camera stops (drive-stop.json: [{ sprite, X, z, row? }]), fetched when
        asked (the title has no stop). */
    stopping() { return fetch(g.assets.url(ART + "drive-stop.json")).then((r) => r.json()).then((j) => (Array.isArray(j) ? j : [])).catch(() => []); },
    /** Put the wagon on the road with its back wheels on a row of the picture, the right size for that row.
        It keeps to its lane, unless it is said how far across the picture it is. */
    drive(row, opacity = 1, x = lane(row)) { wagon.place(x, row, (row - vy) / FULL).fade(opacity); },
    /** ROAD-18M: the wagon z metres ahead of the camera, in its lane. */
    at(z, opacity = 1) { road.drive(rowAt(z), opacity); },
    /** The bounce of the road, on or off. */
    bounce(on) { wagon.flag("still", !on); },
    /** ROAD-18M: the camera goes on at this speed (metres a second), from where it is. */
    cruise(speed) { if (fx) fx.set({ speed }); },
    /** ROAD-18M: the world the camera stops in, the camera at STOP: the sign 17.3 m ahead, the painting's things where it has
        them (pieces: { sprite, X, z, row? }, z ahead of the stopped camera; those keepAtStop leaves out left out), and
        the rows' own things kept off that stretch (the poles and fences go on: STOP a multiple of 40, they stand where the
        painting has them, near enough). */
    stopAt(STOP, pieces = []) {
      if (!fx) return 0;
      fx.place("sign", { sprite: "sign", X: SIGN_X, s: STOP + SIGN_Z });
      const zs = [SIGN_Z], sprites = (fx.tabs && fx.tabs.sprites) || {};
      let n = 1;
      pieces.forEach((p, i) => {
        if (p.sprite === "sign" || p.row === "pole" || p.row === "fence") return;
        if (!keepAtStop(p, sprites[fx.sideName ? fx.sideName(p.sprite, p.X) : p.sprite])) return;     // (MERGE-18B: see keepAtStop)
        fx.place(`stop-${i}`, { sprite: p.sprite, X: p.X, s: STOP + p.z });
        zs.push(p.z); n++;
      });
      fx.set({ gap: [[STOP - 2, STOP + Math.max(...zs) + 1]] });     // (from just behind the stopped camera to the farthest of them)
      return n;
    },
    /** The sun opens into the hole: 0 is the sun, whole; 1 is the hole, open, and its glow on the road. It grows out of the middle of the disc. */
    hole(k) { if (hole) hole.open(k); if (fx) fx.set({ light: { hole: k } }); },
    /** The rings over the sign: 0 is the paint still, 1 the rings at their widest. */
    bend(k) { if (sign) sign.open(k); },
    /** What the sign says: 0 is POINT B, 1 is POINT B.C.; between, the one coming through the other (under the rings). At 1 the
        drive's sign is POINT B.C. itself: what the rings brought through is what is there when they settle. */
    bc(k) {
      board.alpha = k;
      if (sign) sign.refresh();
      if (fx && fx.pieces && fx.pieces.has("sign")) fx.place("sign", { sprite: k >= 1 ? "sign-bc" : "sign" });
    },
  };
  road.drive(REST);
  return road;
}
