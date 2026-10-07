// The highway at dusk: the stage of the opening movie (intro.js) and of the title screen (title.js).
//
// It is one painting and a few parts that change, all in art/scenes/highway/ (the painter's own numbers are in
// layout.json there, and the numbers below are those):
//
//   back.png              the road, the sky and the sign that says POINT B. The backdrop.
//   sun.png               the sun's disc, half sunk at the end of the road
//   sign-strike.png       a slash of red paint through POINT B        }  the road sign
//   sign-bc.png           "B.C." painted underneath it                }  changing its mind
//   wagon-rear-0, -1      the family wagon from behind: two pictures, for the bounce of the road
//
// and two things that are light, and so are drawn live and never painted: the hole in time, which opens where the
// sun's disc was, and the glow it throws down the road.
//
// highway(g, words) puts all of it on the stage and hands back the few things a script does with it:
//
//     const road = highway(g, "A desert highway at dusk.");
//     road.hole(0);  road.strike(0);  road.bc(0);  road.drive(NEAR);      the start of the movie
//     await road.ready;                                                   every picture is here: fade in now
//     await g.tween(1500, (k) => road.hole(k));                           the sun opens into the hole
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
const HOLE = 64;                        // its radius when it is open
const EDIT = [596, 300, 156, 32];       // the part of the sign the red slash crosses: the painter's own box for it (600, 306, 147 by 19) and a little over.
                                        // (The painter's note: "drawn left to right". So it is uncovered from the left.)

/**
 * Set the stage. `words` describes the picture for someone who cannot see it.
 * Returns { ready, wagon, drive(row, opacity), bounce(on), hole(k), strike(k), bc(k) }.
 */
export function highway(g, words) {
  const { art } = g, [vx, vy] = VANISH;
  // LIGHT AND PAINT THAT CHANGE, on the live layer, back to front. The sun and the two edits to the sign are painted
  // pictures, but they are put here and not among the cut-outs for two reasons: cut-outs lie over the live layer, and
  // the hole has to open over the sun; and a cut-out cannot be shown a part at a time, as the slash of paint must be.
  const painted = (id, file, more = "") => `<image id="${id}" href="${g.assets.url(ART + file)}" width="800" height="600" style="image-rendering:pixelated"${more}/>`;
  const live = `<defs>
      <clipPath id="strike-so-far"><rect id="strike-edge" x="${EDIT[0]}" y="${EDIT[1]}" width="0" height="${EDIT[3]}"/></clipPath>
      <radialGradient id="hole-deep"><stop offset="0" stop-color="#22104a" stop-opacity="0.4"/><stop offset="0.5" stop-color="#22104a" stop-opacity="0.82"/><stop offset="0.9" stop-color="#22104a" stop-opacity="0.74"/><stop offset="1" stop-color="#22104a" stop-opacity="0"/></radialGradient>
    </defs>
    <polygon id="road-glow-shape" fill="url(#road-glow)" points="${vx - 2},${vy + 1} ${vx + 2},${vy + 1} 710,600 90,600" opacity="0" shape-rendering="geometricPrecision"/>
    ${painted("sun", "sun.png")}
    <g id="hole-grows" style="transform-origin:${vx}px ${vy}px">
      <g id="hole-dark" shape-rendering="geometricPrecision"><circle cx="${vx}" cy="${vy - HOLE}" r="${HOLE}" fill="url(#hole-deep)"/></g>
      ${art.portal(vx, vy - HOLE, HOLE, "portal")}
    </g>
    ${painted("sign-strike", "sign-strike.png", ` clip-path="url(#strike-so-far)"`)}
    ${painted("sign-bc", "sign-bc.png")}`;
  const drawn = g.view.draw("", words, { picture: ART + "back.png", live, grid: [800, 600] });

  const wagon = g.view.cast.addPicture("wagon", { frames: [ART + "wagon-rear-0.png", ART + "wagon-rear-1.png"], fps: 4, foot: FOOT });
  const part = (id) => g.q("#" + id);
  const road = {
    wagon,
    /** Resolves when every picture is here and the backdrop is painted. */
    ready: Promise.all([drawn, g.view.cast.load(), ...["sun.png", "sign-strike.png", "sign-bc.png"].map((file) => g.assets.picture(ART + file))]),
    /** Put the wagon on the road with its back wheels on a row of the picture, the right size for that row.
        It keeps to its lane, unless it is said how far across the picture it is. */
    drive(row, opacity = 1, x = lane(row)) { wagon.place(x, row, (row - vy) / FULL).fade(opacity); },
    /** The bounce of the road, on or off. */
    bounce(on) { wagon.flag("still", !on); },
    /** The sun opens into the hole: 0 is the sun, whole; 1 is the hole, open, and its glow on the road. It grows out of the middle of the disc. */
    hole(k) {
      part("sun").style.opacity = 1 - k;
      part("portal").style.opacity = k;
      part("hole-dark").style.opacity = k;
      part("hole-grows").style.transform = `scale(${Math.max(k, 0.01)})`;
      part("road-glow-shape").setAttribute("opacity", k);
    },
    /** The slash through POINT B: how much of it has been painted, from the left. */
    strike(k) { part("strike-edge").setAttribute("width", EDIT[2] * k); },
    /** "B.C." under it: how far it has come up. */
    bc(k) { part("sign-bc").style.opacity = k; },
  };
  road.drive(REST);
  return road;
}
