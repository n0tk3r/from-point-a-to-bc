// The highway at dusk: the stage of the opening movie (intro.js) and of the title screen (title.js).
//
// It is one painting and a few parts that change, all in art/scenes/highway/ (the painter's own numbers are in
// layout.json there, and the numbers below are those):
//
//   back.png              the road, the sky and the sign that says POINT B. The backdrop.
//   sun.png               the sun's disc, half sunk at the end of the road
//   sign-bc.png           the sign's board again, saying POINT B.C.: what the sign says once the hole in time has
//                         had its way with it (round twelve: no red slash, no dripping letters)
//   wagon-rear-0, -1      the family wagon from behind: two pictures, for the bounce of the road
//
// and the glow the hole in time throws down the road, which is light, and so is drawn live and never painted. The hole
// itself is the paint, bending (round ten: the engine's `portal`): rings spread from the sun's middle through the sky
// and the road, and the hole rises out of the sun's disc as it opens. The sign changes its mind the same way: rings
// spread over the board from the B, and while the paint is bent the letters come through changed (the effect reads
// sign-bc.png into the paint it bends, a little more each frame: `under` with an alpha, effects.js).
//
// highway(g, words) puts all of it on the stage and hands back the few things a script does with it:
//
//     const road = highway(g, "A desert highway at dusk.");
//     road.hole(0);  road.bend(0);  road.bc(0);  road.drive(NEAR);        the start of the movie
//     await road.ready;                                                   every picture is here: fade in now
//     await g.tween(1500, (k) => road.hole(k));                           the sun opens into the hole
//     await g.tween(500, (k) => road.bend(k));                            rings over the sign...
//     await g.tween(600, (k) => road.bc(k));                              ...and POINT B comes out POINT B.C.
//     await g.tween(700, (k) => road.bend(1 - k));                        the paint settles
//
// Each takes a number from 0 to 1, so a tween can run it and a skipped movie lands on the same picture.


const ART = "art/scenes/highway/";

// ---------- the road ----------
export const VANISH = [400, 330];       // where the road ends, and the middle of the sun's disc
const LANE = (550 - 400) / (600 - 330); // the wagon keeps to the right-hand lane, whose middle runs from the vanishing point down to (550, 600)
/** How far across the picture the middle of that lane is, on a given row. */
export const lane = (row) => VANISH[0] + (row - VANISH[1]) * LANE;
const FULL = 518.4;                     // the painter's rule for its size: (row of its back wheels - 330) / 518.4 of the size it is painted
const FOOT = [251, 419];                // the point of the wagon's picture that is on the road: the middle of the back axle

export const REST = 548;                // "on its way": back wheels on row 548, which puts it at (521, 548), 0.42 of its painted size
export const NEAR = 935;                // close behind it, as the movie opens: so near that only the luggage on its roof is in the picture
export const FAR = 343;                 // almost at the end of the road: a speck, in the mouth of the hole

// ---------- the hole in time ----------
const HOLE = 64;                        // its radius when it is open (its middle rises out of the sun by as much)
// ---------- the sign ----------
const BOARD = [599, 287, 752, 377];     // the painter's board (layout.json: sign.board), x0 y0 x1 y1
const B_AT = [733, 316];                // the middle of the B of POINT B: the rings that change the sign spread from here
const SIGN_R = 44;                      // their radius, drawn 2.4 times as wide as high: the whole board, and the paint beside it, is in their reach

/**
 * Set the stage. `words` describes the picture for someone who cannot see it.
 * Returns { ready, wagon, drive(row, opacity), bounce(on), hole(k), bend(k), bc(k) }.
 */
export function highway(g, words) {
  const [vx, vy] = VANISH;
  // LIGHT AND PAINT THAT CHANGE, on the live layer, back to front. The sun and the sign's second board are painted
  // pictures, but they are put here and not among the cut-outs: each is part of the paint a portal bends (the hole
  // reads the sun in, the sign's rings read the board in: `under`), and shows here, plain, when its rings are gone.
  const painted = (id, file, more = "") => `<image id="${id}" href="${g.assets.url(ART + file)}" width="800" height="600" style="image-rendering:pixelated"${more}/>`;
  const live = `<polygon id="road-glow-shape" fill="url(#road-glow)" points="${vx - 2},${vy + 1} ${vx + 2},${vy + 1} 710,600 90,600" opacity="0" shape-rendering="geometricPrecision"/>
    ${painted("sun", "sun.png")}
    ${painted("sign-bc", "sign-bc.png", ` style="opacity:0"`)}`;
  const drawn = g.view.draw("", words, { picture: ART + "back.png", live, grid: [800, 600] });

  // The hole in time: the paint bending in rings from the sun's middle, the hole rising out of the sun's disc as it
  // opens (round ten; effects.js, `portal`). On the cast layer at the road's end, so the wagon is drawn over it as it
  // drives in. Shut until hole() opens it. (The stage was cleared for this road: whatever moved on it before goes too.)
  g.effects.drop(g.scene);
  const hole = g.effects.add({ id: "hole", type: "portal", at: [vx, vy], r: HOLE, rise: true, base: vy + 1, pale: "#fff2c8", under: [{ src: ART + "sun.png", x: 0, y: 0 }] });
  // The sign's own rings (round twelve): from the B, across the board and no farther sideways (`keep`), the paint of
  // the second board read in as much as bc() says.
  const board = { src: ART + "sign-bc.png", x: 0, y: 0, alpha: 0 };
  const sign = g.effects.add({ id: "sign", type: "portal", at: B_AT, r: SIGN_R, wide: 2.4, keep: [BOARD[0], BOARD[2]], base: vy + 2, pale: "#fff2c8", strength: 0.8, under: [board] });
  const wagon = g.view.cast.addPicture("wagon", { frames: [ART + "wagon-rear-0.png", ART + "wagon-rear-1.png"], fps: 4, foot: FOOT });
  const part = (id) => g.q("#" + id);
  const road = {
    wagon,
    /** Resolves when every picture is here and the backdrop is painted. */
    ready: Promise.all([drawn, g.view.cast.load(), ...["sun.png", "sign-bc.png"].map((file) => g.assets.picture(ART + file))]),
    /** Put the wagon on the road with its back wheels on a row of the picture, the right size for that row.
        It keeps to its lane, unless it is said how far across the picture it is. */
    drive(row, opacity = 1, x = lane(row)) { wagon.place(x, row, (row - vy) / FULL).fade(opacity); },
    /** The bounce of the road, on or off. */
    bounce(on) { wagon.flag("still", !on); },
    /** The sun opens into the hole: 0 is the sun, whole; 1 is the hole, open, and its glow on the road. It grows out of the middle of the disc. */
    hole(k) {
      if (hole) hole.open(k);
      part("road-glow-shape").setAttribute("opacity", k);
    },
    /** The rings over the sign: 0 is the paint still, 1 the rings at their widest. */
    bend(k) { if (sign) sign.open(k); },
    /** What the sign says: 0 is POINT B, 1 is POINT B.C.; between, the one coming through the other (under the rings, as a rule). */
    bc(k) {
      board.alpha = k;
      if (sign) sign.refresh();
      part("sign-bc").style.opacity = k;
    },
  };
  road.drive(REST);
  return road;
}
