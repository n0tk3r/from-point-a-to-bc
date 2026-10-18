// Act Five, continued: the Office, stage one, "Processing" (SCENES-17: new in round seventeen; the design is
// briefs/out/office-hq-design.md, sections 3 and 4; the lines are js/content/lines/office.en.js, the talks
// js/content/talk/office.js, the scenes js/content/scenes/office-*.js and the two cut-scenes in js/content/cutscenes/).
//
// The limousine stops at the Office Of Peculiar Sectors, a very small building with a very long name, and the two of them
// are split up at once: GRANDPA JOE is locked in Interview Room C (the Comfortable Room) with Dale, Merle and a
// questionnaire forty-seven pages long; RANGER is outside, then in the air ducts. Each is played on his own, and the player
// switches between them through the Office's map. Neither can finish without the other: Ranger has the run of the
// building and no words; Grandpa Joe has words, a chair, an intercom and his pockets, and cannot leave the room. They meet
// at the vent.
//
//   the arrival (cut-scene)          A Very Small Building With A Very Long Name
//   #16 Not On The Form (A, Ranger)  the trash can, the drainpipe, the roof, four wing nuts, the fan switch: into the ducts;
//                                    the building's air off, and the Comfortable Room starts to warm
//   #17 The Comfortable Room (B, Joe) the interview; at 81, Regulation 9: he is alone
//   #18 The Bearer (both)            the receipt up through the vent, down through a grille to Opal; the banjo comes back
//   #19 Wendell's Pie (both)         Jed's cheeseburger on Jed's behalf; the pie, the clean tin, the test schedule
//   #20 A Soundproof Room (Joe)      the pie-tin banjo, the Rag through every vent, the suits, and B-7
//   Going Down (cut-scene)           the card LAMPLIGHTER, "to be continued": the end of the demo
//
// A beat carries a hint for each of the two. Ranger's are thoughts (pictures), with Grandpa Joe's reading of them where he
// can hear him (office-common.js joeHears). The long puzzles give a hint for the stage they have got to: such a hint is a
// function of the game, listing every line it can give (`lines`) for the story's check (js/engine/story.js hintLines).

import { is, joeHears, heat } from "../scenes/office-common.js";

const BOTH = ["ranger", "grandpajoe"];        // (Ranger first: he is the one played as the stage opens)
const has = (g, who, item) => ((g.store.data.inventory || {})[who] || []).includes(item);
const where = (g) => (typeof g.where === "function" ? g.where("ranger") : null) || {};
/** A hint that follows how far a puzzle has got: fn(g) gives a line or a list of lines; `lines` lists them all. */
const staged = (lines, fn) => Object.assign(fn, { lines });
/** Ranger's thought, and Joe's reading where Joe can hear him. */
const heard = (g, id, reading) => (reading && joeHears(g) ? [id, reading] : id);

export const act = {
  id: 6, title: "Act Five, continued: Processing", era: "nevada", gate: "office.done",
  summary: "The limousine stops at the Office Of Peculiar Sectors: a very small building with a very long name, a flagpole, a gravel lot, and on the roof an air conditioner much too big for it. The four suits bring Grandpa Joe in upright, hat on (\"Ranger. You know what to do.\"); the raccoon is not on the form. Grandpa Joe is locked in the Comfortable Room with Dale, Merle and a questionnaire forty-seven pages long; Ranger, outside, tips over a trash can (a raccoon in trash: noted), climbs the drainpipe, turns four wing nuts, pulls the fan switch, and goes in at the intake. The building's air is off, and the Comfortable Room warms until Regulation 9 suspends the interview. At the vent the two of them meet: the receipt goes up through the slats and down through another grille to Opal of Property & Effects, who returns the banjo, damaged. Grandpa Joe calls Houston on Jed's behalf, and Jed's cheeseburger is at the front desk at last; Ranger eats Wendell's birthday pie, leaves his best bottle cap, washes the tin, and brings it and the Lamplighter test schedule down to Joe. They are making the holes in the desert, and the next is today at five, on Sector 44, the boy's year, on B-7. A pie-tin banjo and the Last Stop Rag through every vent, and the suits will take him anywhere he can play without bothering anybody: there is one soundproof room. Going down.",
  beats: [
    { id: "office.arrive", kind: "cutscene", title: "A Very Small Building With A Very Long Name", lead: BOTH, scene: "office-lot", needs: ["limo.done"], sets: "office.arrived" },
    { id: "office.inside", kind: "puzzle", chain: "A", title: "Not On The Form: a trash can, a drainpipe, four wing nuts and the fan switch, into the ducts", lead: "ranger", scene: "office-lot",
      needs: ["office.arrived"], sets: "office.inside",
      hint: {
        grandpajoe: "hint.office.inside.grandpajoe",
        ranger: staged(["hint.office.inside.ranger", "hint.office.inside.ranger.2", "hint.office.inside.ranger.3", "office.lot.grille.open.ranger"], (g) => {
          if (is(g, "office.grilleOff")) return is(g, "office.acOff") ? "office.lot.grille.open.ranger" : "hint.office.inside.ranger.3";
          const w = where(g);
          return w.scene === "office-lot" && w.y != null && w.y < 300 ? "hint.office.inside.ranger.2" : "hint.office.inside.ranger";
        }),
      } },
    { id: "office.room", kind: "puzzle", chain: "B", title: "The Comfortable Room: the interview, until it is too warm to be comfortable", lead: "grandpajoe", scene: "office-room",
      needs: ["office.arrived"], sets: "office.alone",
      hint: {
        grandpajoe: staged(["hint.office.room.grandpajoe", "hint.office.room.grandpajoe.2", "hint.office.room.grandpajoe.3"],
          (g) => (heat(g) >= 81 ? "hint.office.room.grandpajoe.3" : heat(g) >= 77 ? "hint.office.room.grandpajoe.2" : "hint.office.room.grandpajoe")),
        ranger: "hint.office.room.ranger",
      } },
    { id: "office.bearer", kind: "puzzle", chain: "A", title: "The Bearer: the receipt up through the vent and down to Opal; the banjo comes back", lead: BOTH, scene: "office-property",
      needs: ["office.inside", "office.alone"], sets: "office.banjoBack",
      hint: {
        grandpajoe: staged(["hint.office.bearer.grandpajoe", "hint.office.bearer.grandpajoe.2"],
          (g) => (is(g, "office.receiptUp") ? "hint.office.bearer.grandpajoe.2" : "hint.office.bearer.grandpajoe")),
        ranger: staged(["hint.office.bearer.ranger", "hint.office.bearer.ranger.2", "hint.office.bearer.ranger.2.joe"],
          (g) => (has(g, "ranger", "receipt") ? heard(g, "hint.office.bearer.ranger.2", "hint.office.bearer.ranger.2.joe") : "hint.office.bearer.ranger")),
      } },
    { id: "office.pie", kind: "puzzle", chain: "A", title: "Wendell's Pie: Jed's cheeseburger, a clean pie tin, and the test schedule", lead: BOTH, scene: "office-breakroom",
      needs: ["office.banjoBack"], sets: "office.schedule",
      hint: {
        grandpajoe: staged(["hint.office.pie.grandpajoe", "hint.office.pie.grandpajoe.2", "hint.office.pie.grandpajoe.3", "hint.office.pie.grandpajoe.4", "hint.office.rag.grandpajoe.2"], (g) => {
          if (is(g, "office.mended")) return "hint.office.rag.grandpajoe.2";                    // (mended, and nowhere yet to play to)
          if (is(g, "office.tinClean") || has(g, "grandpajoe", "pietin")) return "hint.office.pie.grandpajoe.4";
          if (is(g, "office.jedGone")) return "hint.office.pie.grandpajoe.3";
          if (is(g, "office.jedTold")) return "hint.office.pie.grandpajoe.2";
          return "hint.office.pie.grandpajoe";
        }),
        ranger: staged(["hint.office.pie.ranger", "hint.office.pie.ranger.2", "hint.office.pie.ranger.3", "hint.office.pie.ranger.4"], (g) => {
          if (is(g, "office.tinClean")) return "hint.office.pie.ranger.4";
          if (is(g, "office.pieEaten")) return "hint.office.pie.ranger.3";
          if (is(g, "office.jedGone")) return "hint.office.pie.ranger.2";
          return "hint.office.pie.ranger";
        }),
      } },
    { id: "office.rag", kind: "puzzle", chain: "A", title: "A Soundproof Room: the pie-tin banjo, the Rag, and B-7", lead: "grandpajoe", scene: "office-room",
      needs: ["office.schedule"], sets: "office.down",
      hint: {
        grandpajoe: staged(["hint.office.rag.grandpajoe", "hint.office.rag.grandpajoe.3"],
          (g) => (is(g, "office.mended") ? "hint.office.rag.grandpajoe.3" : "hint.office.rag.grandpajoe")),
        ranger: staged(["hint.office.rag.ranger", "hint.office.rag.ranger.joe"], (g) => heard(g, "hint.office.rag.ranger", "hint.office.rag.ranger.joe")),
      } },
    { id: "office.end", kind: "gate", title: "Going Down (the end of the demo)", lead: BOTH, scene: "office-ducts", needs: ["office.down"], sets: "office.done" },
  ],
};

