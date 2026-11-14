// Act Five, continued: the Office, stage one, "Processing" (WRITE-17: new in round seventeen; briefs/OFFICE-17.md,
// briefs/WRITE-17.md, and the design, briefs/out/office-hq-design.md, sections 3 and 4).
//   "line.id": ["who", "What they say."]
//   "line.id": ["ranger", "...", "pie"]                          a line that carries a thought picture
//   "line.id": ["ranger", "...", ["piepan", "plus", "banjo"]]     or two or three of them, read left to right
//
// GRANDPA JOE ("grandpajoe") is locked in Interview Room C, the Comfortable Room, with Dale and Merle and a questionnaire
// forty-seven pages long; RANGER ("ranger") is outside, then in the air ducts. They are played apart, and meet at the vent
// over the room. Ranger never speaks: his line is "...", and the bubble over his head is what he thinks, one picture for a
// plain reaction, two or three for an idea (the names are fixed in briefs/OFFICE-17.md and drawn by js/art/thoughts.js:
// question idea heart no plus arrow up down joe pie piepan banjo banjo-broken receipt bottlecap key door hole fan hot sun zzz
// eye shiny music clock paper cheeseburger pickle water suit opal trash wingnut lamp peanuts switch chair hand). Where
// Grandpa Joe can hear him (in the room, or at the grille over it with the suits gone) Joe says what he means: a look of
// Ranger's is office.<scene>.<thing>.ranger, and Joe's reading of it office.<scene>.<thing>.ranger.joe. Away from Joe the
// picture is all there is. Scene-shorts: lot, duct, room, prop (Property & Effects), break (the break room).
//
// The men in gray are one gray voice, sir and sorry and regulations, each with one thing of his own: DALE ("suit1") reads,
// MERLE ("suit2") writes it down in capitals and apologizes, WENDELL ("suit3") is on the front door and it is his birthday,
// FLOYD ("suit4") is asleep on his regulation rest. JED ("agent") is in the break room with an ice pack and the banjo's
// hoop. OPAL ("opal") of Property & Effects is precise and fond. HOUSTON ("houston") is on the building's speakers
// (office.pa.*, said with g.pa) and the intercom: brisk, and fond of nobody but Jed. She calls him Mr. Grandpa, because
// that is what Merle wrote in the box.
//
// Grandpa Joe never lies, not even to the Office: every answer he gives is true, and the suits write down the wrong thing
// all by themselves. His surname, Hollis, is said once, by Opal (office.opal.6). No real song is sung, named or quoted:
// the Last Stop Rag is his own, and it is played, never sung. Nothing frightening: the suits say sir and sorry, the room is
// locked "for your comfort", the ducts are safe (the fans are off before Ranger goes in). The writer's notes for the scenes
// (S/work-17-write/ids.md) say when every line is said, and which hooks and facts the talks (js/content/talk/office.js) use.

export const lines = {
  // ---------- Cut-scene: A Very Small Building With A Very Long Name (js/content/cutscenes/office-arrive.js) ----------
  "office.arrive.card": ["narrator", "A Very Small Building With A Very Long Name"],
  // the limousine stops in the lot; the four suits get out in a row
  // STAGE-19O: "office.arrive.1" ("We have arrived, sir.") and "office.arrive.2" ("Sorry about the drive, sir.") are gone,
  // lines and use: the arrival enters late, on the four of them standing in a row
  // two of them bring Grandpa Joe out of the back, upright, hat on
  "office.arrive.3": ["suit1", "Sir, you will now be processed."],
  "office.arrive.4": ["grandpajoe", "You might could ask nicely first, son."],
  // Jed comes round from the front, the banjo's hoop round his neck and what is left of the banjo in his hands; he goes in ahead
  "office.arrive.5": ["agent", "Evidence."],
  "office.arrive.6": ["grandpajoe", "Careful with her, son. She's had a day."],
  "office.arrive.7": ["agent", "We have all had a day, sir."],
  // across the gravel to the door, between the suits: the sign on the gate, and the rooftop unit
  "office.arrive.8": ["grandpajoe", "'Please do not look directly at the building.' Only thing out here to look at."],   // FINAL-19: REVIEW-19's patch
  "office.arrive.9": ["suit1", "Please look at the gravel, sir."],
  "office.arrive.10": ["grandpajoe", "That's a powerful lot of air conditioner for a building the size of a garage."],
  "office.arrive.11": ["suit2", "Sorry, sir. We are not permitted to discuss the air."],
  // he wipes his boots on the mat (WIPE)
  "office.arrive.12": ["suit3", "Thank you for wiping your feet, sir."],
  "office.arrive.13": ["grandpajoe", "Sign asked nice."],
  // at the door he looks back at the limousine's open door, and says, not loud:
  "office.arrive.14": ["grandpajoe", "Ranger. You know what to do."],
  "office.arrive.15": ["suit3", "Sir, was that addressed to the raccoon?"],
  "office.arrive.16": ["grandpajoe", "What raccoon, son?"],
  "office.arrive.17": ["suit1", "The raccoon is not on the form."],                       // Dale checks the clipboard
  "office.arrive.18": ["grandpajoe", "Then officially, there ain't one."],
  // the door shuts on all of them but Wendell, who turns round, by regulation, to face the gate
  "office.arrive.19": ["suit3", "It is my birthday."],
  // a moment; Ranger comes out from under the limousine's seat in his mirror shades, drops to the gravel and sits up
  "office.arrive.ranger.1": ["ranger", "...", "joe"],
  // STAGE-19O: "office.arrive.ranger.2" (the question mark) is gone, line and use: two thoughts, not three of the same picture
  "office.arrive.ranger.3": ["ranger", "Ranger looks at the door Grandpa Joe went in by, and at the man in gray standing in front of it.", ["door", "plus", "suit"]],

  // ---------- #16 Not On The Form: the lot (office-lot). Ranger, alone: his thoughts are all there is. ----------
  // the front door, steel and beige, and Wendell on it, facing the gate
  "office.lot.door.ranger": ["ranger", "A gray door with a keypad beside it and a man in gray in front of it. Ranger wonders how a raccoon gets through.", ["door", "question"]],
  "office.lot.door.use.1": ["suit3", "Sir. Er. Raccoon. You are not authorized."],                  // he shoos, politely, with his clipboard
  "office.lot.door.use.2": ["suit3", "Shoo, please."],
  "office.lot.door.use.ranger": ["ranger", "Ranger backs off a few steps. That is plainly not the way in.", "no"],
  "office.lot.door.again.1": ["suit3", "Raccoon. You are still not authorized."],                    // the second time, and after
  "office.lot.door.again.2": ["suit3", "Raccoon, please. I am on the door."],
  "office.lot.door.again.ranger": ["ranger", "Asked nicely, Ranger goes. He likes manners in a man.", "heart"],                                         // asked nicely, he goes: he likes manners
  // the mat by the door: WIPE
  "office.lot.mat.ranger": ["ranger", "A doormat with one word on it. Ranger can't read it, but he knows what a mat is for.", ["hand", "question"]],
  "office.lot.mat.use.ranger": ["ranger", "Ranger wipes his feet on the mat, all four of them, carefully.", ["hand", "shiny"]],                                  // he wipes his feet, all four, carefully
  "office.lot.mat.use.1": ["suit3", "Thank you for wiping your feet, sir. Raccoon."],
  // the keypad beside the door
  "office.lot.keypad.ranger": ["ranger", "A keypad beside the door, with a button for every number. Ranger's hands itch to press them.", ["hand", "question"]],
  "office.lot.keypad.use.1": ["suit3", "That is not the code."],                                      // he presses every button; it beeps every time
  "office.lot.keypad.use.2": ["suit3", "That is also not the code."],
  "office.lot.keypad.use.3": ["suit3", "Raccoon. That is the code for the vending machine."],
  "office.lot.keypad.use.ranger": ["ranger", "Ranger presses every button on the keypad. Each one beeps, and the door stays shut.", "question"],
  // the long sign over the door: OFFICE OF PECULIAR SECTORS, and so on, and PLEASE WIPE YOUR FEET
  "office.lot.sign.ranger": ["ranger", "The sign over the door has a very long name on it. Ranger reads pictures, and there isn't one.", ["question", "question", "question"]],                 // a very long name, and he reads pictures
  "office.lot.sign.use.ranger": ["ranger", "The sign is bolted high on the wall, well out of a raccoon's reach.", ["hand", "no"]],
  // the trash can: standing by the wall; tipped over on the gravel; standing under the drainpipe
  "office.lot.trash.ranger": ["ranger", "A trash can stands by the wall, its lid chained on. Ranger has never met a trash can he didn't like.", ["trash", "heart"]],
  "office.lot.trash.tipped.ranger": ["ranger", "The trash can lies on its side on the gravel. A can on its side will roll wherever Ranger pushes it.", ["trash", "arrow"]],
  "office.lot.trash.under.ranger": ["ranger", "The can stands under the end of the drainpipe now. Up the can, then up the pipe.", ["trash", "plus", "up"]],
  // he tips it: a clang; Wendell turns round, sees a raccoon in a trash can, writes it down, and turns back to the gate
  "office.lot.trash.wendell.1": ["suit3", "One raccoon. In trash."],
  "office.lot.trash.wendell.2": ["suit3", "Noted."],
  "office.lot.trash.noted.ranger": ["ranger", "Wendell has written Ranger down. He is on a form at last, and he is delighted.", ["paper", "heart"]],                            // he is on a form at last
  "office.lot.trash.report": ["suit3", "Houston, it is Wendell."],       // into his earpiece; then office.pa.raccoon
  "office.lot.trash.roll.ranger": ["ranger", "Ranger puts his shoulder to the can and rolls it along the wall, toward the drainpipe.", ["trash", "arrow", "up"]],                        // he rolls it along to the foot of the drainpipe
  "office.lot.trash.stand.ranger": ["ranger", "Ranger stands the can up under the end of the drainpipe. It makes a fine step.", "idea"],                                         // and stands it up there
  "office.lot.trash.lid.ranger": ["ranger", "Ranger tries the lid of the trash can. It is chained to the can, by regulation.", ["hand", "no"]],                                   // the lid, chained to the can: REGULATION
  "office.lot.trash.with.bottlecap.ranger": ["ranger", "Ranger will not put his best bottle cap in a trash can. It is for trading.", ["bottlecap", "no"]],                   // not in the trash: it is his best
  // the drainpipe down the near corner, ending three feet above the gravel
  "office.lot.pipe.ranger": ["ranger", "A drainpipe runs up the corner of the building to the roof. It stops three feet short of the ground.", ["up", "question"]],
  "office.lot.pipe.use.ranger": ["ranger", "Ranger stretches up for the end of the drainpipe. It is just out of reach.", ["up", "no"]],                                      // he stretches up: just out of reach
  "office.lot.pipe.again.ranger": ["ranger", "Ranger stretches up again, on the tips of his toes. He needs something to stand on.", ["hand", "up", "no"]],
  "office.lot.pipe.climb.ranger": ["ranger", "With the can under it, the pipe is easy. Ranger goes up the can, and then up the pipe.", ["up", "heart"]],                                 // the can under it: up the can, up the pipe
  // the gray limousine, parked along the side, its back door left open
  "office.lot.limo.ranger": ["ranger", "The gray limousine, where Ranger last had a pickle. He thinks of it fondly.", ["pickle", "heart"]],
  "office.lot.limo.use.ranger": ["ranger", "Ranger hops up onto the hood of the limousine. The roof of the building is still much too far.", "no"],                                              // he hops up on the hood: the roof is too far
  "office.lot.limo.door.ranger": ["ranger", "The limousine's back door stands open. Ranger isn't getting back in, not without Grandpa Joe.", ["joe", "no"]],                                    // back in? Not without Joe
  // the rooftop unit, the size of a minivan, humming (seen from the gravel, and up close on the roof)
  "office.lot.unit.ranger": ["ranger", "On the roof sits an air conditioner the size of a minivan, with a fan turning behind a grille.", ["fan", "up"]],
  "office.lot.unit.use.ranger": ["ranger", "The big unit is up on the roof, and Ranger is down on the gravel. He needs a way up.", ["up", "question"]],
  "office.lot.unit.roof.ranger": ["ranger", "The rooftop unit hums and blows. Behind the grille on its side, Ranger can see a big fan turning.", ["fan", "eye"]],
  "office.lot.unit.off.ranger": ["ranger", "The rooftop unit has gone quiet, and the big fan behind it stands still.", ["fan", "zzz"]],                                    // once the fans are off
  // the intake grille, held on by four wing nuts; behind it the fan
  "office.lot.grille.ranger": ["ranger", "A grille on the side of the unit, held on by four wing nuts. Raccoons have hands for exactly this.", ["wingnut", "hand"]],                                 // raccoons have hands
  "office.lot.wingnuts.ranger": ["ranger", "A shiny wing nut, one of four that hold the grille on. Ranger could turn it with his fingers.", ["wingnut", "shiny"]],
  "office.lot.grille.done.ranger": ["ranger", "The fourth wing nut comes off, and the grille comes away from the unit.", ["wingnut", "heart"]],                           // the fourth one turned: the grille comes off
  "office.lot.grille.off.ranger": ["ranger", "The grille is off, but the fan behind it is still turning. Nobody is going in past that.", ["fan", "no"]],                                   // off, and the fan turning behind it
  "office.lot.grille.use.ranger": ["ranger", "Ranger leans back from the turning fan. It will have to stop before he goes in.", ["fan", "no"]],                                   // in, while it turns: he leans back from it
  "office.lot.grille.open.ranger": ["ranger", "The grille is off and the fan has stopped. The opening is a way in, just the size of a raccoon.", ["door", "heart"]],                              // off, and the fan stopped: a way in
  "office.lot.fan.ranger": ["ranger", "The big fan turns behind the opening, fast enough to blur. Ranger keeps his distance.", ["fan", "no"]],
  "office.lot.fan.still.ranger": ["ranger", "The big fan stands still. There is room for a raccoon to slip between its blades.", ["fan", "zzz"]],
  // the maintenance switch: a fan with a line through it, and TURN OFF BEFORE SERVICING. THIS MEANS YOU, WENDELL.
  "office.lot.switch.ranger": ["ranger", "A switch on the unit, with a sticker: a picture of a fan with a line through it. Ranger can read that.", ["switch", "fan", "no"]],                             // he reads the sticker's picture
  "office.lot.switch.use.ranger": ["ranger", "Ranger looks at the picture on the sticker, and then at the fan, and pulls the switch down.", ["fan", "arrow", "no"]],                          // he looks at the picture, at the fan, and pulls
  "office.lot.switch.off.ranger": ["ranger", "The switch is down and the fans are off. Ranger is pleased with it.", ["switch", "heart"]],
  "office.lot.switch.back.ranger": ["ranger", "Ranger leaves the switch down. The fans stay off.", ["fan", "no"]],                                  // push it back up? No: the fans stay off
  "office.lot.in.ranger": ["ranger", "Ranger slips in between the still blades of the fan, to find Grandpa Joe.", ["joe", "heart"]],                                        // in at the intake, to find Joe
  // the flagpole, and its pennant, O.O.P.S.
  "office.lot.flag.ranger": ["ranger", "A flagpole, with a small gray pennant at the top. Ranger wonders what is up there.", ["up", "question"]],
  "office.lot.flag.use.ranger": ["ranger", "The flagpole is too smooth to climb, even for a raccoon.", ["hand", "no"]],                                    // too smooth to climb
  // the sign on the gate: PLEASE DO NOT LOOK DIRECTLY AT THE BUILDING (no pictures on it, so he does)
  "office.lot.fencesign.ranger": ["ranger", "A sign on the gate asks visitors not to look directly at the building. Ranger can't read it, so he looks.", "question"],
  "office.lot.fencesign.use.ranger": ["ranger", "Ranger turns from the sign and looks directly at the building. It has one door.", ["eye", "door"]],
  // the gate, standing open, and the desert past it
  "office.lot.gate.ranger": ["ranger", "The gate stands open on the road back out into the sun.", ["arrow", "sun"]],
  "office.lot.gate.use.ranger": ["ranger", "Ranger sits back down on the gravel. He isn't leaving, not without Grandpa Joe.", ["joe", "no"]],                                     // not without Joe: he sits back down
  "office.lot.desert.ranger": ["ranger", "Desert in every direction, warm and wide in the afternoon sun. Ranger likes it out there.", ["sun", "heart"]],
  "office.lot.desert.use.ranger": ["ranger", "The desert will keep. Ranger isn't going anywhere without Grandpa Joe.", ["joe", "no"]],
  "office.lot.window.ranger": ["ranger", "A small window, high in the wall, with frosted glass. Ranger can't see a thing through it.", ["eye", "no"]],                                       // the small high window: frosted
  "office.lot.window.use.ranger": ["ranger", "The window is far too high in the wall for Ranger to reach.", ["hand", "no"]],                                   // too high
  // Wendell, on the door, with a round button on his lapel
  "office.lot.wendell.ranger": ["ranger", "A man in a gray suit, on the door. There is a shiny round button on his lapel.", ["suit", "plus", "shiny"]],
  "office.lot.wendell.use.1": ["suit3", "Raccoon. Please do not approach the door."],
  "office.lot.wendell.with.bottlecap.1": ["suit3", "That is a very nice bottle cap, sir. Raccoon."],
  "office.lot.wendell.with.bottlecap.2": ["suit3", "But this is my birthday button. It is not for trade."],
  "office.lot.wendell.with.bottlecap.ranger": ["ranger", "Ranger keeps his best bottle cap, then. He admires the button all the same.", ["bottlecap", "heart"]],              // he keeps his best, then
  "office.lot.wendell.idle.1": ["suit3", "I face the gate, by regulation. Even on my birthday."],        // now and then, to the gate
  "office.lot.wendell.idle.2": ["suit3", "Houston, it is Wendell. Nothing to report."],
  "office.lot.wendell.air": ["suit3", "Houston, I am on the door. It is my birthday."],               // into his earpiece, after office.pa.air.2

  // ---------- the ducts (office-ducts): Ranger alone, but for the grille over the Comfortable Room ----------
  "office.duct.in.ranger": ["ranger", "Ranger is inside, in a long sheet-metal duct. Grandpa Joe is somewhere underneath it.", ["joe", "question"]],                                    // just in at the intake, the first time
  "office.duct.intake.ranger": ["ranger", "Daylight comes in at the intake. That is the way back up to the roof.", ["sun", "up"]],                                      // the way back up to the roof
  "office.duct.intakefan.ranger": ["ranger", "The back of the intake fan. Its blades are still, and will stay that way.", ["fan", "zzz"]],                                  // the intake fan's back: still
  // the four grilles: what comes up through each before he looks; and the first look down
  "office.duct.room.ranger": ["ranger", "A grille in the floor of the duct. Under it, somebody is asking questions, and a voice Ranger knows is answering.", ["joe", "question"]],                                  // ROOM C: a voice he knows, under the questions
  "office.duct.room.found.ranger": ["ranger", "The grille over the Comfortable Room. Grandpa Joe is right down there.", ["joe", "heart"]],                               // once he has seen Joe down there
  "office.duct.room.ranger.joe": ["grandpajoe", "I hear you up there, partner."],                     // Joe's reading, when he is alone
  "office.duct.room.first.ranger": ["ranger", "Down through the slats, Ranger sees a dented straw hat. He has found Grandpa Joe.", "heart"],
  "office.duct.prop.ranger": ["ranger", "A grille in the floor of the duct. Something down there is catching the light.", ["shiny", "question"]],                                // PROP & EFF
  "office.duct.prop.first.ranger": ["ranger", "Shelves to the ceiling, and every one of them full of things. Ranger has never seen so much to look at.", ["shiny", "shiny", "shiny"]],
  "office.duct.break.ranger": ["ranger", "A grille in the floor of the duct. Ranger can smell pie through it.", ["pie", "question"]],                                 // BREAK: he can smell it
  "office.duct.break.first.ranger": ["ranger", "A whole pie sits on the counter down there. Ranger's heart is lost at once.", ["pie", "heart"]],
  "office.duct.hall.ranger": ["ranger", "A grille over the hall. Ranger wonders which doors are down there.", ["door", "question"]],                                 // HALL
  "office.duct.hall.first.ranger": ["ranger", "Down in the hall there is an elevator door. The arrow over it points down.", ["door", "down"]],                               // the elevator, its arrow pointing down
  "office.duct.hall.use.ranger": ["ranger", "Ranger watches the hall for a while. Nothing happens in it.", ["eye", "zzz"]],                                   // if the hall has no view: nothing doing
  // dropping in, and not
  "office.duct.drop.no.ranger": ["ranger", "Ranger stays where he is. Somebody down there would see him drop.", ["eye", "no"]],                                     // somebody would see
  "office.duct.drop.suits.ranger": ["ranger", "Not with the two men in suits in the room. Ranger waits up in the duct.", ["suit", "no"]],                                 // over the room, with Dale and Merle in it
  "office.duct.drop.hall.ranger": ["ranger", "It is a long way down to the floor of the hall, with nothing to land on.", ["down", "no"]],                                  // over the hall: nothing to land on
  // the B-7 shaft at the right end, and the big fan across it, stopped
  "office.duct.shaft.ranger": ["ranger", "The shaft at the far end of the duct drops away out of sight. Ranger wonders how far down it goes.", ["down", "question"]],
  "office.duct.shaft.use.ranger": ["ranger", "Ranger looks down the shaft and stays put. He isn't going down there without Grandpa Joe.", ["joe", "no"]],                                   // go down? Not without Joe
  "office.duct.fan.ranger": ["ranger", "A big fan sits across the top of the shaft, its blades standing still.", ["fan", "zzz"]],
  "office.duct.fan.use.ranger": ["ranger", "Ranger pushes one blade of the big fan. It turns a little way, and stops.", ["fan", "hand"]],                                   // he pushes a blade: it turns a little, and stops
  "office.duct.stencil.ranger": ["ranger", "Letters stenciled on the shaft: 'B-7 exhaust. Soundproofed. Authorized air only.' Ranger can't read a word of it.", "question"],                                        // B-7 EXHAUST. SOUNDPROOFED. AUTHORIZED AIR ONLY.
  "office.duct.stencil.use.ranger": ["ranger", "Ranger runs a paw over the stenciled letters. They don't tell him anything more.", ["hand", "question"]],
  // the ceiling's hidden world, round the duct
  "office.duct.pipe.ranger": ["ranger", "A water pipe runs along the duct, with a valve on it. Ranger can hear water moving inside.", ["water", "question"]],
  "office.duct.pipe.use.ranger": ["ranger", "Ranger lays his cheek against the cool pipe. In a warm duct, that is very good.", ["hot", "water", "heart"]],                        // he lays his cheek on the cool pipe
  "office.duct.wires.ranger": ["ranger", "A bundle of wires runs along the wall of the duct. Ranger doesn't care for the look of them.", "no"],
  "office.duct.wires.use.ranger": ["ranger", "Ranger does not touch the wires. He is a careful raccoon.", ["hand", "no"]],                                  // he does not touch them
  "office.duct.insulation.ranger": ["ranger", "Pink insulation, as soft as a bed. Ranger would dearly like a nap on it.", ["heart", "zzz"]],                               // pink, and soft as a bed
  "office.duct.insulation.use.ranger": ["ranger", "Ranger pats the insulation and takes his hand away. It is itchy.", ["hand", "no"]],                             // itchy
  "office.duct.cup.ranger": ["ranger", "A coffee cup, forgotten on a ceiling tile. Ranger wonders whether there is anything in it.", ["water", "question"]],                                 // a coffee cup, forgotten on a tile
  "office.duct.cup.use.ranger": ["ranger", "Ranger looks into the cup. Whatever was in it dried up long ago.", ["eye", "no"]],                                     // he looks in
  "office.duct.pencil.ranger": ["ranger", "A pencil, left behind in the duct. Ranger wonders what it is for.", ["hand", "question"]],
  "office.duct.pencil.use.ranger": ["ranger", "The pencil isn't shiny, so Ranger isn't interested.", ["shiny", "no"]],                                // not shiny: not interested
  "office.duct.wrapper.ranger": ["ranger", "A sandwich wrapper, flattened in the dust. Ranger hopes there was a cheeseburger in it.", ["cheeseburger", "question"]],                      // a sandwich wrapper, from about 1983
  "office.duct.wrapper.use.ranger": ["ranger", "Ranger sniffs the wrapper. It is far too old, by about forty years.", ["clock", "clock", "no"]],                      // he sniffs it: far too old
  "office.duct.light.ranger": ["ranger", "A light fitting glows up through the ceiling tiles, with a caged bulb beside it.", ["sun", "question"]],                                 // a light fitting, glowing up through the tiles
  "office.duct.light.use.ranger": ["ranger", "Ranger holds a paw near the light and takes it away again. It is hot.", ["hot", "no"]],
  "office.duct.tiles.ranger": ["ranger", "The backs of the ceiling tiles, beside the duct. They are not for standing on.", ["down", "no"]],                                      // the backs of the ceiling tiles: not to stand on
  "office.duct.rivets.ranger": ["ranger", "A row of rivets along the wall of the duct, every one of them shiny. Ranger approves.", ["shiny", "heart"]],
  "office.duct.rivets.use.ranger": ["ranger", "Ranger tries a rivet. It is in for good.", ["hand", "no"]],

  // ---------- #17 The Comfortable Room (office-room): INTERVIEW ROOM C. THIS ROOM HAS BEEN RATED COMFORTABLE. ----------
  // Grandpa Joe's looks (he can always look; with the suits there he does it from his chair); Ranger's, from the grille
  // over the room or in it; and Joe's reading of Ranger's, which needs Joe alone
  "office.room.door.grandpajoe": ["narrator", "The door of the Comfortable Room, locked for Grandpa Joe's comfort. He has never been so comforted in his life."],
  "office.room.door.use.suits": ["suit1", "Sir, the door is locked for your comfort."],
  "office.room.door.use.joe": ["grandpajoe", "I'm feelin' better already, son."],
  "office.room.door.use.grandpajoe": ["narrator", "Grandpa Joe tries the handle. It is locked, and still comforting him."],                                   // alone
  "office.room.door.ranger": ["ranger", "...", ["door", "key"]],
  "office.room.door.ranger.joe": ["grandpajoe", "He says it wants a key. Opal's got every key in the building, partner."],
  "office.room.sign.grandpajoe": ["narrator", "A sign on the wall: 'This room has been rated comfortable.' Grandpa Joe wonders who by."],
  "office.room.sign.hot.grandpajoe": ["narrator", "'This room has been rated comfortable.' Grandpa Joe thinks somebody ought to come and rate it again."],
  "office.room.sign.ranger": ["ranger", "A sign on the wall, all words. Ranger can't make anything of it.", "question"],
  "office.room.sign.ranger.joe": ["grandpajoe", "It says comfortable, partner. Don't believe everything you can't read."],
  "office.room.table.grandpajoe": ["narrator", "A gray table, with two men in suits on one side and one old man on the other. That seems fair to Grandpa Joe."],
  "office.room.table.alone.grandpajoe": ["narrator", "The table, empty now. It looked bigger with Dale and Merle behind it."],
  "office.room.table.ranger": ["ranger", "...", ["paper", "zzz"]],
  "office.room.table.ranger.joe": ["grandpajoe", "He says that's a table for paperwork. He's against it."],
  "office.room.table.use.grandpajoe": ["narrator", "Grandpa Joe keeps his hands on the table, where folks can see them. It's only manners."],
  "office.room.questionnaire.grandpajoe": ["narrator", "The questionnaire, forty-seven pages thick. At this rate Jolene will have to mail Grandpa Joe his Christmas."],
  "office.room.questionnaire.use": ["suit1", "Please do not touch the questionnaire, sir. It is in order."],
  "office.room.questionnaire.ranger": ["ranger", "Paper, and more paper under it, and more under that. Ranger has never seen so much paper.", ["paper", "paper", "paper"]],
  // the chairs: his own; Dale's and Merle's across the table; the spare in the corner, under the vent
  "office.room.chair.grandpajoe": ["narrator", "Grandpa Joe's chair. It has a regulation seat and a regulation squeak."],
  "office.room.chair.use.grandpajoe": ["narrator", "Grandpa Joe sits back down for a spell, and gets right up again. It's too hot for sitting."],                // alone, once it is hot
  "office.room.chairs.grandpajoe": ["narrator", "Dale's chair and Merle's, both still warm. Then again, everything in this room is still warm."],   // alone
  "office.room.chairs.ranger": ["ranger", "...", ["chair", "zzz"]],
  "office.room.chairs.ranger.joe": ["grandpajoe", "He says I ought to sit down, I've had a day. So have you, partner."],
  "office.room.corner.grandpajoe": ["narrator", "A spare chair stands in the corner, right under the vent in the ceiling."],
  "office.room.corner.use.suits": ["suit1", "Please remain in your chair, sir. That one is the spare."],
  "office.room.corner.use.grandpajoe": ["narrator", "Grandpa Joe climbs onto the spare chair, slowly. He hasn't stood on a chair since Jolene saw a mouse."],    // alone: up he goes
  "office.room.corner.ranger": ["ranger", "...", ["chair", "up"]],
  "office.room.corner.ranger.joe": ["grandpajoe", "He says that's the way up. Only way there is, partner."],
  // the vent in the ceiling over the spare chair: plain, or with two eyes in a mask behind the slats
  "office.room.vent.grandpajoe": ["narrator", "A vent in the ceiling, over the spare chair, blowing cool air. The Office does look after a fellow."],    // before #16
  "office.room.vent.off.grandpajoe": ["narrator", "The vent in the ceiling, over the spare chair. There isn't a breath of air coming out of it now."],             // after #16
  "office.room.vent.eyes.grandpajoe": ["narrator", "Two eyes in a black mask look down through the vent. Grandpa Joe would know them anywhere."],                          // the suits gone
  "office.room.vent.eyes.suits.grandpajoe": ["narrator", "Two eyes shine in the vent. Grandpa Joe gives his head the smallest shake: not now, not with company."],                                   // the suits there (not loud)
  "office.room.vent.use.grandpajoe": ["narrator", "Grandpa Joe can't reach the vent from the floor. He'd want something to stand on."],                       // from the floor
  "office.room.vent.empty.1": ["grandpajoe", "Ranger? No, just me and the duct."],                                                       // on the chair, nobody up there
  "office.room.vent.empty.2": ["grandpajoe", "Ranger? Still just the duct, and it don't say much either."],
  "office.room.vent.ranger": ["ranger", "...", ["up", "heart"]],                                                                              // from in the room
  "office.room.vent.ranger.joe": ["grandpajoe", "He says that's his way home now. Up there."],
  // the long mirror on the back wall (one-way)
  "office.room.mirror.grandpajoe": ["narrator", "A long mirror fills most of one wall. Somebody behind it is eating chips, and not quietly."],
  "office.room.mirror.use.grandpajoe": ["grandpajoe", "Afternoon. Go on and finish your chips, son, I won't tell."],
  "office.room.mirror.use.suits": ["suit1", "Sir, that is a mirror."],                                                                        // after his line, while they are there
  "office.room.mirror.use.joe": ["grandpajoe", "Course it is, son."],
  "office.room.mirror.ranger": ["ranger", "...", ["eye", "heart"]],
  "office.room.mirror.ranger.joe": ["grandpajoe", "He says there's a handsome raccoon in that mirror. Can't argue with him."],
  // the plastic plant: upright, and drooping (it cannot, and it does)
  "office.room.plant.grandpajoe": ["narrator", "A plastic plant in a pot, standing up very straight. Somebody dusts it."],
  "office.room.plant.droop.grandpajoe": ["narrator", "The plant is plastic, and it is wilting. Grandpa Joe didn't know they could."],
  "office.room.plant.use.grandpajoe": ["narrator", "Grandpa Joe would water it, but with a plastic plant that would only be for show."],
  "office.room.plant.droop.use.grandpajoe": ["grandpajoe", "Hang in there, little feller."],
  "office.room.plant.ranger": ["ranger", "...", ["water", "question"]],
  "office.room.plant.ranger.joe": ["grandpajoe", "He wants to know should he water it. It's plastic, partner."],
  // the water cooler, and its paper cones
  "office.room.cooler.grandpajoe": ["narrator", "A water cooler, with a stack of paper cones beside it. Government water."],
  "office.room.cooler.hot.grandpajoe": ["narrator", "The water in the cooler is still cold. It is the only thing in the room that is."],
  "office.room.cooler.use.grandpajoe": ["narrator", "Grandpa Joe drinks a paper cone of government water. It tastes like a form."],
  "office.room.cooler.use.suits": ["suit2", "Help yourself, sir. Sorry."],
  "office.room.cooler.ranger": ["ranger", "...", ["water", "heart"]],
  "office.room.cooler.ranger.joe": ["grandpajoe", "He says that's the best thing in the room. He ain't wrong."],
  "office.room.cooler.use.ranger": ["ranger", "...", ["hand", "water", "heart"]],                                                           // in the room: he washes up in a cone
  "office.room.cooler.use.ranger.joe": ["grandpajoe", "He's washin' up. Government water's good for something."],
  "office.room.cones.grandpajoe": ["narrator", "Paper cones, pointed at the bottom so they can't be set down. Grandpa Joe reckons that's on purpose."],
  "office.room.cones.ranger": ["ranger", "...", ["hand", "question"]],
  "office.room.cones.ranger.joe": ["grandpajoe", "He says they fall over. That's so a fella holds on to his, partner."],
  // the wall clock
  "office.room.clock.grandpajoe": ["narrator", "A wall clock, ticking louder than any clock Grandpa Joe ever heard. Every tick is another page."],
  "office.room.clock.late.grandpajoe": ["narrator", "The clock is still going, and Grandpa Joe has until five."],                                                // once he has read the schedule
  "office.room.clock.ranger": ["ranger", "...", ["clock", "question"]],
  "office.room.clock.ranger.joe": ["grandpajoe", "He wants to know what time it is. Time we were gone, partner."],
  "office.room.clock.use.grandpajoe": ["narrator", "Grandpa Joe can't make it go any faster. Clocks don't take requests."],
  // the thermostat by the door: 72, 77, 81
  "office.room.thermostat.72.grandpajoe": ["narrator", "The thermostat on the wall reads seventy-two degrees, which figures."],
  "office.room.thermostat.72.suits": ["suit1", "It is always seventy-two, sir. It is the Comfortable Room."],                                // while they are there
  "office.room.thermostat.77.grandpajoe": ["narrator", "The thermostat reads seventy-seven now, and it is climbing."],
  "office.room.thermostat.77.suits.1": ["suit1", "Within regulations, sir. Comfortable is seventy to eighty."],
  "office.room.thermostat.77.suits.2": ["suit2", "It is going up, Dale."],
  "office.room.thermostat.77.suits.3": ["suit1", "Then we will read faster, Merle."],
  "office.room.thermostat.81.grandpajoe": ["narrator", "The thermostat reads eighty-one. Whatever the sign says, that is not comfortable."],                                         // with them there: SUSPEND follows
  "office.room.thermostat.use.grandpajoe": ["narrator", "Grandpa Joe turns the dial, and nothing happens. It is only there for comfort."],                         // alone: he turns it
  "office.room.thermostat.ranger": ["ranger", "...", ["hot", "question"]],
  "office.room.thermostat.ranger.joe": ["grandpajoe", "He says it's hot in here. That's your doin', partner, and I thank you."],
  "office.room.thermostat.use.ranger": ["ranger", "Ranger turns the dial on the thermostat. Nothing happens at all.", ["hand", "no"]],                                                                    // in the room: the dial
  "office.room.thermostat.use.ranger.joe": ["grandpajoe", "That dial don't do a thing, partner. It's just for comfort."],
  // the intercom by the door: DISPATCH. PRESS TO TALK. (Alone, it is intercomTree.)
  "office.room.intercom.grandpajoe": ["narrator", "An intercom on the wall, labeled 'Dispatch. Press to talk.' That will be Houston."],
  "office.room.intercom.use.suits": ["suit1", "Sir, please do not touch the intercom."],
  "office.room.intercom.ranger": ["ranger", "A box on the wall with one button. Ranger's hand goes toward it by itself.", ["hand", "switch"]],
  "office.room.intercom.ranger.joe": ["grandpajoe", "That's Houston's button, partner. She don't take calls from raccoons."],
  "office.room.intercom.press.1": ["houston", "Dispatch."],                                                                                   // Ranger in the room presses it anyway
  "office.room.intercom.press.2": ["ranger", "Ranger breathes hopefully into the intercom. He is thinking of a cheeseburger.", ["cheeseburger", "question"]],
  "office.room.intercom.press.3": ["houston", "Mr. Grandpa, is there a raccoon on my intercom?"],
  "office.room.intercom.press.4": ["grandpajoe", "Ma'am, I wouldn't want to say what ain't on the form."],
  // the poster: PECULIAR? REPORT IT., a fence with a hole in the sky behind it
  "office.room.poster.grandpajoe": ["narrator", "A poster: 'Peculiar? Report it.' It shows a fence and a hole in the sky. They got the fence right."],
  "office.room.poster.ranger": ["ranger", "...", ["hole", "eye"]],
  "office.room.poster.ranger.joe": ["grandpajoe", "He says he's seen one of those holes. So have I, partner, and we ain't reportin' it."],
  "office.room.poster.use.grandpajoe": ["narrator", "Grandpa Joe has been not reporting things for forty years. He won't start for a poster."],
  // Dale and Merle, across the table (a word with either of them is interviewTree)
  "office.room.dale.grandpajoe": ["narrator", "That is Dale, in a gray suit and dark glasses. Dale reads the questions."],
  "office.room.merle.grandpajoe": ["narrator", "That is Merle. Merle writes every answer down, and he is sorry about it."],
  "office.room.merle.hot.grandpajoe": ["narrator", "Merle mops his forehead. He is sweating right through his apologies."],
  "office.room.dale.hot.grandpajoe": ["narrator", "Dale has loosened his tie and is reading more slowly. The heat has got into the regulations."],
  "office.room.opal.grandpajoe": ["narrator", "Opal, of Property and Effects. She has worn the same glasses on the same chain since 1971."],                // her visit
  "office.room.opal.ranger": ["ranger", "It is the lady with the glasses on a chain. Ranger likes her.", ["opal", "heart"]],
  "office.room.wendell.grandpajoe": ["narrator", "A man in gray with a birthday button on his lapel and a finger in each ear. That will be Wendell."],  // at the door, #20
  "office.room.dale.ranger": ["ranger", "A man in a gray suit, reading aloud from a great many sheets of paper.", ["suit", "paper"]],
  "office.room.merle.ranger": ["ranger", "A man in a gray suit, writing fast. His hand never stops moving.", ["suit", "hand"]],
  "office.room.suits.with.receipt": ["suit1", "That is your receipt, sir. Please keep it."],                       // the receipt given to Dale or Merle
  "office.room.suits.with.sectormap.grandpajoe": ["narrator", "Grandpa Joe keeps the map in his bib pocket. That one is going home with him."],                          // the map: he will not hand it over
  "office.room.joe.ranger": ["ranger", "Grandpa Joe, seen from above: mostly a straw hat with a dent in it. Ranger is very glad to see it.", ["joe", "heart"]],                                                                              // Grandpa Joe, seen from above
  // the room warming (#16 done): Merle mops his forehead; Dale loosens his tie a finger's width, and puts it back
  "office.room.merle.mop": ["suit2", "Sorry. I am perspiring, sir."],
  "office.room.dale.tie": ["suit1", "Regulations."],
  // the suits gone (#17's end): Grandpa Joe alone, and then he looks up at the vent
  "office.room.alone.1": ["grandpajoe", "Well."],
  "office.room.alone.2": ["grandpajoe", "Lord, You know where that family is, and I don't. You look after 'em."],
  "office.room.alone.3": ["grandpajoe", "And that raccoon of mine, wherever he's got to."],
  // Ranger drops into the room (alone), and climbs back out by the spare chair
  "office.room.drop.grandpajoe": ["grandpajoe", "Look who dropped in."],
  "office.room.climb.grandpajoe": ["grandpajoe", "Up you go, partner. Mind the... well. You ain't got a hat."],
  // the two of them, in the room together (the scene's talk; Ranger's word with Joe is office.vent.r.*)
  "office.room.talk.joe.1a": ["grandpajoe", "You come in through the roof, partner? With your little hands?"],
  "office.room.talk.joe.1b": ["ranger", "...", ["up", "hand", "heart"]],
  "office.room.talk.joe.1c": ["grandpajoe", "He says it weren't nothin'. Partner, it was plenty."],
  "office.room.talk.joe.2a": ["grandpajoe", "Smell that? That's government carpet."],
  "office.room.talk.joe.2b": ["ranger", "...", "no"],
  "office.room.talk.joe.2c": ["grandpajoe", "He says he'd rather not."],

  // ---------- the interview (interviewTree, js/content/talk/office.js): Dale reads, Merle writes, nobody finishes ----------
  "office.iv.open.1": ["suit1", "Thank you for coming in, sir."],
  "office.iv.open.2": ["grandpajoe", "Didn't have a lot of say in it, son."],
  "office.iv.open.3": ["suit2", "Sorry about that, sir."],
  "office.iv.open.4": ["suit1", "This is the questionnaire, sir. It is forty-seven pages."],
  "office.iv.open.5": ["suit2", "Sorry about that too, sir."],
  "office.iv.again.1": ["suit1", "Shall we continue, sir?"],                                       // back at the table after a minute
  "office.iv.again.2": ["suit2", "Sorry, sir."],
  "office.iv.sorry": ["suit2", "Sorry, sir."],                                                          // Merle, before the question
  "office.iv.sorry.2": ["suit2", "Sorry in advance, sir."],
  "office.iv.sorry.3": ["suit2", "This one has a box, sir. Sorry."],
  "office.iv.sorry.4": ["suit2", "This one is a little personal, sir. Sorry."],
  // page one, question one: the name (he never says it is Grandpa; they write it down anyway)
  "office.iv.q1": ["suit1", "Page one. Question one. Name?"],
  "office.iv.opt.joe": ["grandpajoe", "Joe."],
  "office.iv.q1.last": ["suit1", "Last name?"],
  "office.iv.opt.drove": ["grandpajoe", "You drove two hours to fetch me, son, and you ain't got my name?"],
  "office.iv.q1.drove.1": ["suit1", "We have your name, sir. We are required to ask it."],
  "office.iv.q1.drove.2": ["suit2", "Sorry, sir."],
  "office.iv.opt.folks": ["grandpajoe", "Folks just call me Grandpa."],
  "office.iv.q1.folks": ["suit2", "G... R... A... N... D..."],
  "office.iv.opt.sign": ["grandpajoe", "It's on the sign out front of my store, son."],
  "office.iv.q1.sign.1": ["suit2", "The sign says 'Grandpa Joe's'."],
  "office.iv.q1.sign.2": ["suit1", "Then it is Grandpa, sir."],
  "office.iv.opt.sooner": ["grandpajoe", "I'd sooner not say, son."],
  "office.iv.q1.sooner.1": ["suit1", "Sir, I have to put something in the box."],
  "office.iv.q1.sooner.2": ["suit2", "I will put Grandpa, since it is on the sign. Sorry, sir."],
  "office.iv.q1.record": ["suit2", "NAME: JOE. LAST NAME: GRANDPA."],
  "office.iv.q1.jolene": ["grandpajoe", "Jolene's gonna love that."],
  // occupation
  "office.iv.q2": ["suit1", "Occupation?"],
  "office.iv.opt.lemonade": ["grandpajoe", "Lemonade."],
  "office.iv.q2.lemonade.1": ["suit2", "Lemonade."],
  "office.iv.q2.lemonade.2": ["suit1", "Sir, lemonade is a beverage."],
  "office.iv.q2.lemonade.3": ["grandpajoe", "It's a dollar, son."],
  "office.iv.opt.rocks": ["grandpajoe", "Rocks."],
  "office.iv.q2.rocks.1": ["suit1", "Sir, are you a rock?"],
  "office.iv.q2.rocks.2": ["grandpajoe", "I sell 'em, son. Some days I feel like one."],
  "office.iv.opt.road": ["grandpajoe", "Watchin' the road. Forty years."],
  "office.iv.q2.road": ["suit2", "Forty... years. Noted."],
  // yesterday at 1747: the clue (somebody wrote down the very minute)
  "office.iv.q3.sorry": ["suit2", "Sorry about this one, sir."],
  "office.iv.q3": ["suit1", "On 30 October, at 1747 hours, did you observe a sector?"],
  "office.iv.opt.wagon": ["grandpajoe", "I observed a station wagon."],
  "office.iv.q3.wagon.1": ["suit2", "One... station... wagon."],
  "office.iv.q3.wagon.2": ["suit1", "Sir, what color was the station wagon?"],
  "office.iv.q3.wagon.3": ["grandpajoe", "Red, son. Wood on the sides."],
  "office.iv.q3.wagon.4": ["suit2", "Sorry, sir. There is no box for wood."],
  "office.iv.opt.sector": ["grandpajoe", "What's a sector?"],
  "office.iv.q3.sector.1": ["suit1", "We are not permitted to say, sir."],
  "office.iv.q3.sector.2": ["grandpajoe", "Then I can't rightly say if I seen one."],
  "office.iv.q3.sector.3": ["suit2", "He has a point, Dale."],
  "office.iv.q3.sector.4": ["suit1", "Write 'no answer', Merle."],
  "office.iv.opt.opal": ["grandpajoe", "Told this office nothin' forty-one times, son. Ask Opal."],
  "office.iv.q3.opal.1": ["suit1", "Sir, Property & Effects does not take statements."],
  "office.iv.q3.opal.2": ["suit2", "She files them."],
  "office.iv.q3.opal.3": ["suit1", "She does file them."],
  "office.iv.opt.minute": ["grandpajoe", "Seventeen forty-seven. That's an awful particular minute, son."],
  "office.iv.q3.minute.1": ["suit1", "It is the minute on the form, sir."],
  "office.iv.q3.minute.2": ["grandpajoe", "Who wrote it down so exact?"],
  "office.iv.q3.minute.3": ["suit2", "Sorry, sir. We are not permitted to say who writes the form."],
  // page two: the raccoon (who is not on the form, except on this one)
  "office.iv.q4.page": ["suit1", "Page two."],
  "office.iv.q4": ["suit1", "Describe the raccoon."],
  "office.iv.opt.what": ["grandpajoe", "What raccoon?"],
  "office.iv.q4.what.1": ["suit1", "The raccoon is not on the form, sir."],
  "office.iv.q4.what.2": ["suit2", "It is on this form. Page two, question one."],
  "office.iv.q4.what.3": ["suit1", "Describe the raccoon, sir."],
  "office.iv.opt.handsome": ["grandpajoe", "Handsome."],
  "office.iv.q4.handsome.1": ["suit1", "Sir, can you be more specific?"],
  "office.iv.q4.handsome.2": ["grandpajoe", "Very handsome."],
  "office.iv.q4.handsome.3": ["suit2", "Very... handsome."],
  "office.iv.opt.likeme": ["grandpajoe", "He's a lot like me, only he don't talk and he's better lookin'."],
  "office.iv.q4.likeme": ["suit2", "Better... looking."],
  // the green page: Lamplighter (the clue: there is one, and they do not know what it is either)
  "office.iv.q5.turn": ["suit1", "Next page."],
  "office.iv.q5": ["suit1", "Have you had any contact with Lamplighter?"],
  "office.iv.opt.withwhat": ["grandpajoe", "With what?"],
  "office.iv.opt.pleasure": ["grandpajoe", "Don't believe I've had the pleasure, son."],
  "office.iv.opt.lamp": ["grandpajoe", "That some kind of a lamp?"],
  "office.iv.q5.lamp": ["suit1", "I cannot say if it is a lamp. ...Strike that, sir."],
  "office.iv.q5.strike": ["suit1", "Strike that, sir."],
  "office.iv.q5.green.1": ["suit2", "You read the green page."],
  "office.iv.q5.green.2": ["suit1", "I read the green page."],
  "office.iv.q5.green.3": ["suit2", "We are not supposed to read the green page."],
  "office.iv.opt.greenpage": ["grandpajoe", "What's on that green page, fellas?"],
  "office.iv.green.1": ["suit2", "We do not know, sir. We are not supposed to read it."],
  "office.iv.green.2": ["suit1", "It is the only page that is green, sir."],
  // the banjo, and the receipt
  "office.iv.q6": ["suit1", "Did you strike an officer of this Office with a banjo?"],
  "office.iv.opt.once": ["grandpajoe", "Once."],
  "office.iv.q6.once.1": ["suit2", "Once."],
  "office.iv.q6.once.2": ["suit1", "Thank you for your honesty, sir."],
  "office.iv.opt.sorry": ["grandpajoe", "I did, son. And I'd tell him I'm sorry, if he's about."],
  "office.iv.q6.sorry.1": ["suit2", "He is in the break room, sir. With an ice pack."],
  "office.iv.q6.sorry.2": ["suit1", "He is keeping the hoop on, sir. It is evidence."],
  "office.iv.opt.going": ["grandpajoe", "He was about to go someplace, son. I said he wasn't."],
  "office.iv.q6.going": ["suit1", "Noted, sir."],
  "office.iv.q6.receipt.1": ["suit2", "Sorry about the banjo, sir."],
  "office.iv.q6.receipt.2": ["suit1", "Your banjo is entered in Property & Effects, sir. You have your receipt."],
  "office.iv.q6.receipt.3": ["grandpajoe", "I do."],
  // and on, and on (never finished): a question, two true answers, and round again after the fifth
  "office.iv.m1": ["suit1", "Next question. Have you ever been, or are you now, a sector?"],
  "office.iv.opt.m1.a": ["grandpajoe", "Not as I know of, son."],
  "office.iv.m1.a": ["suit2", "Not... as he... knows of."],
  "office.iv.opt.m1.b": ["grandpajoe", "You tell me what one is, and I'll tell you."],
  "office.iv.m1.b.1": ["suit1", "We are not permitted to say, sir."],
  "office.iv.m1.b.2": ["grandpajoe", "Then we're stuck, son."],
  "office.iv.m2": ["suit1", "Next question. Have you ever looked directly at the building?"],
  "office.iv.opt.m2.a": ["grandpajoe", "Your sign told me not to. So I did."],
  "office.iv.m2.a": ["suit2", "Sorry, sir. That is a yes."],
  "office.iv.opt.m2.b": ["grandpajoe", "I looked. It's beige."],
  "office.iv.m2.b": ["suit2", "Beige."],
  "office.iv.m3": ["suit1", "Next question. Please describe the sky, using the box provided."],
  "office.iv.opt.m3.a": ["grandpajoe", "Blue, mostly."],
  "office.iv.m3.a": ["suit2", "Blue... mostly."],
  "office.iv.opt.m3.b": ["grandpajoe", "Big. Ain't you boys been outside?"],
  "office.iv.m3.b": ["suit1", "Not during an interview, sir. Regulations."],
  "office.iv.m4": ["suit1", "Is there anything you would like to add? Please do not add anything."],
  "office.iv.opt.m4.a": ["grandpajoe", "No, son."],
  "office.iv.m4.a": ["suit1", "Thank you, sir."],
  "office.iv.opt.m4.b": ["grandpajoe", "Well, now that you mention it..."],
  "office.iv.m4.b": ["suit1", "Sir. Please do not add anything."],
  "office.iv.m5": ["suit1", "Next question. On a scale of one to five, how comfortable are you?"],
  "office.iv.opt.m5.cool": ["grandpajoe", "Four, son. Five if the door opened."],                                // at 72
  "office.iv.opt.m5.warm": ["grandpajoe", "Ask me again when it cools off."],                                 // warming
  "office.iv.opt.m5.hot": ["grandpajoe", "One, son. And that's bein' neighborly."],                           // at 81: the second way to the lever
  "office.iv.m5.a": ["suit2", "Noted, sir."],
  "office.iv.m5.next.1": ["suit2", "Sorry, sir. That was the end of page two."],
  "office.iv.m5.next.2": ["suit1", "Page two, continued."],
  "office.iv.m5.hot.1": ["suit2", "That is a one, Dale."],
  "office.iv.m5.hot.2": ["suit1", "There is a regulation for a one."],
  // what he can say at any question
  "office.iv.opt.leave": ["grandpajoe", "I believe I'll be gettin' on home now, fellas."],
  "office.iv.leave.1": ["suit1", "Sir, you have not completed the questionnaire."],
  "office.iv.leave.2": ["grandpajoe", "How far are we?"],
  "office.iv.leave.3": ["suit2", "Page two, sir."],
  "office.iv.leave.again.1": ["suit1", "Sir, you have still not completed the questionnaire."],
  "office.iv.leave.again.2": ["suit2", "Still page two. Sorry, sir."],
  "office.iv.opt.warm": ["grandpajoe", "Gettin' warm in here, fellas."],                                       // warming: replies office.room.thermostat.77.suits.*
  "office.iv.warm.again": ["suit1", "Still within regulations, sir. Just."],
  "office.iv.opt.hot": ["grandpajoe", "Hot in here, fellas. Ain't there a regulation?"],                       // at 81: the lever
  "office.iv.opt.pause": ["grandpajoe", "Give me a minute, fellas."],
  "office.iv.pause": ["suit1", "Take all the time you need, sir. We have forty-five pages."],
  // SUSPEND (#17's end): Dale takes out the book of regulations; then they gather up the questionnaire, and go
  "office.suspend.1": ["suit1", "Regulation 9. 'The Comfortable Room shall be comfortable.'"],
  "office.suspend.2": ["suit2", "It is not comfortable, Dale."],
  "office.suspend.3": ["suit1", "Then the interview is suspended, pending a Form 30."],
  "office.suspend.4": ["suit2", "We will be back, sir. A Form 30 is very long."],
  "office.suspend.5": ["suit1", "The door will be locked for your comfort, sir."],

  // ---------- the vent: Grandpa Joe on the spare chair, Ranger at the grille over him (ventTree) ----------
  "office.vent.meet.1": ["grandpajoe", "Took your time, partner."],
  "office.vent.meet.ranger": ["ranger", "...", ["fan", "no"]],
  "office.vent.meet.joe": ["grandpajoe", "He says he turned the fans off. So that's why I'm cookin', you little wonder."],
  "office.vent.opt.banjo": ["grandpajoe", "Partner, I want my banjo back."],
  "office.vent.banjo.1": ["grandpajoe", "With a banjo and the Rag, partner, I could empty this whole building."],
  "office.vent.banjo.ranger": ["ranger", "...", ["banjo", "door", "no"]],
  "office.vent.banjo.joe": ["grandpajoe", "He says a banjo won't come through there. No, sir, but a receipt will."],
  "office.vent.opt.receipt": ["grandpajoe", "Take this to Opal for me, partner."],
  "office.vent.receipt.1": ["grandpajoe", "Property and Effects. A window with a bell, and a lady with glasses on a chain."],
  "office.vent.receipt.ranger": ["ranger", "...", ["opal", "question"]],
  "office.vent.receipt.joe": ["grandpajoe", "That's her, that's Opal. You give her this, and she'll know what to do."],
  "office.vent.receipt.known.ranger": ["ranger", "...", ["opal", "idea"]],                                      // he has looked down into Property already
  "office.vent.receipt.known.joe": ["grandpajoe", "You seen her already? 'Course you have."],
  "office.vent.receipt.up": ["grandpajoe", "Up she goes."],                                                     // he pushes it up through the slats (the hook)
  "office.vent.receipt.got": ["ranger", "...", ["receipt", "heart"]],
  "office.vent.opt.seenbanjo": ["grandpajoe", "Seen my banjo anywhere, partner?"],
  "office.vent.seenbanjo.ranger": ["ranger", "...", ["banjo", "paper"]],
  "office.vent.seenbanjo.joe": ["grandpajoe", "On a shelf, with a tag on it? Then she's in Property and Effects, with Opal."],
  "office.vent.opt.eat": ["grandpajoe", "Find anything to eat down that duct?"],
  "office.vent.eat.ranger": ["ranger", "...", ["pie", "heart"]],
  "office.vent.eat.joe": ["grandpajoe", "He says there's a pie. He says it ain't his. He says that's a technicality."],
  "office.vent.jed.ranger": ["ranger", "...", ["suit", "eye", "pie"]],
  "office.vent.jed.joe.1": ["grandpajoe", "And a fella with a hoop round his neck, watchin' it like it owes him money."],
  "office.vent.jed.joe.2": ["grandpajoe", "That's Jed. That boy's wanted a cheeseburger since five this mornin'."],
  "office.vent.opt.head": ["grandpajoe", "This banjo wants a new head, partner."],
  "office.vent.head.1": ["grandpajoe", "Somethin' round and tin, stretched tight. A pie plate would do, if a man had a pie."],
  "office.vent.head.known.ranger": ["ranger", "...", ["pie", "idea"]],
  "office.vent.head.known.joe": ["grandpajoe", "He says he knows where there's a pie. 'Course he does."],
  "office.vent.head.look.ranger": ["ranger", "...", ["pie", "question"]],
  "office.vent.head.look.joe": ["grandpajoe", "He says he'll go sniff one out. If anybody can, partner."],
  "office.vent.opt.jed": ["grandpajoe", "How do we get Jed off that pie?"],
  "office.vent.jedplan.ranger": ["ranger", "...", ["suit", "cheeseburger"]],
  "office.vent.jedplan.joe.1": ["grandpajoe", "He says the only thing Jed wants more than that pie is a cheeseburger."],
  "office.vent.jedplan.joe.2": ["grandpajoe", "Then leave Jed to me, partner. I'm gonna ask nicely."],
  "office.vent.opt.trade": ["grandpajoe", "What did you pay for that pie, partner?"],
  "office.vent.trade.ranger": ["ranger", "...", ["bottlecap", "heart"]],
  "office.vent.trade.joe": ["grandpajoe", "His best bottle cap. That's better than a fair trade, partner."],
  "office.vent.opt.down": ["grandpajoe", "We got to get down to B-7 by five, partner."],
  "office.vent.down.ranger": ["ranger", "...", ["fan", "down"]],
  "office.vent.down.joe.1": ["grandpajoe", "He says the big fan at the end of the duct goes down. And it's stopped."],
  "office.vent.down.joe.2": ["grandpajoe", "You go your way, partner, and I'll go mine. See you at the bottom."],
  "office.vent.opt.promise": ["grandpajoe", "That lady's countin' on us, partner."],
  "office.vent.promise.ranger": ["ranger", "...", "heart"],
  "office.vent.promise.joe": ["grandpajoe", "I know. Porch light on, however long it takes, so let's get to it."],
  "office.vent.opt.jolene": ["grandpajoe", "Reckon Jolene's changed her hat yet?"],
  "office.vent.jolene.ranger": ["ranger", "...", ["clock", "joe"]],
  "office.vent.jolene.joe": ["grandpajoe", "He says about three hats ago. He's probably right."],
  "office.vent.jolene.2.ranger": ["ranger", "...", ["joe", "plus", "joe"]],
  "office.vent.jolene.2.joe": ["grandpajoe", "He says another one since I asked. That's Jolene."],
  "office.vent.opt.bye": ["grandpajoe", "Go on, partner. I'll be right here."],
  "office.vent.bye.ranger": ["ranger", "...", ["joe", "heart"]],
  // Ranger at the grille, and Joe alone at the table: Ranger thinks, and Joe can hear him
  "office.vent.call.ranger": ["ranger", "Ranger scratches at the grille. He wants Grandpa Joe up on the spare chair, where they can talk.", ["joe", "chair", "up"]],
  "office.vent.call.joe": ["grandpajoe", "Comin', partner. Let me get up on that chair."],
  // Ranger's word with Joe (from the grille, Joe on the chair; or in the room together): his thought, and Joe's answer
  "office.vent.r.1": ["ranger", "...", ["joe", "heart"]],
  "office.vent.r.1.joe": ["grandpajoe", "Missed you too, partner."],
  "office.vent.r.2": ["ranger", "...", ["hot", "question"]],
  "office.vent.r.2.joe": ["grandpajoe", "Hot as a skillet, partner, and it ran those two boys right out. That was you."],
  "office.vent.r.3": ["ranger", "...", ["cheeseburger", "question"]],
  "office.vent.r.3.joe": ["grandpajoe", "No cheeseburger, partner. I ate the last one, and Jed gets the next."],
  "office.vent.r.4": ["ranger", "...", ["banjo-broken", "question"]],
  "office.vent.r.4.joe": ["grandpajoe", "Jed's head went clean through her. She wants a new head, is all."],
  "office.vent.r.5": ["ranger", "...", ["clock", "question"]],
  "office.vent.r.5.joe": ["grandpajoe", "Five o'clock, partner. We got till five."],
  // handing things up and down through the slats: a receipt fits, a pie tin fits, a banjo does not
  "office.vent.up.sectormap": ["grandpajoe", "Not the map, partner. That map's comin' home with us."],
  "office.vent.up.banjo": ["grandpajoe", "She won't go through there, partner. That's the whole trouble."],                 // the banjo, broken or mended
  "office.vent.up.pietin": ["grandpajoe", "I'll be needin' that one, partner."],
  "office.vent.up.schedule": ["grandpajoe", "I'll hang on to this. Most important paper in the building."],
  "office.vent.up.peanuts": ["grandpajoe", "You keep them, partner. You're the planner."],
  "office.vent.down.pietin.1": ["grandpajoe", "Washed and shinin'."],
  "office.vent.down.pietin.ranger": ["ranger", "Ranger pictures the pie tin on the broken banjo, where the head used to be.", ["piepan", "plus", "banjo"]],
  "office.vent.down.pietin.joe": ["grandpajoe", "Round, and tin, and just the size. Great minds, partner."],
  "office.vent.down.peanuts": ["grandpajoe", "Peanuts. He's a planner."],
  "office.vent.down.bottlecap.ranger": ["ranger", "Ranger holds his best bottle cap over the slats, and thinks better of it. That one he keeps.", ["bottlecap", "heart", "no"]],                                // he will not hand down his best
  "office.vent.down.bottlecap.joe": ["grandpajoe", "He says that's his best one. He'd trade it, for the right thing."],
  "office.vent.down.receipt.ranger": ["ranger", "Ranger holds the receipt over the slats and waits. He isn't sure it is meant for Grandpa Joe.", ["receipt", "question"]],
  "office.vent.down.receipt.joe": ["grandpajoe", "That ain't for me, partner. That's for Opal."],
  "office.vent.down.table": ["grandpajoe", "That's twice this week somethin's fell out of the sky on me."],                // a thing lands on the table

  // ---------- the schedule, handed down (#19's end): Grandpa Joe reads it, on his chair under the vent ----------
  "office.schedule.read.1": ["grandpajoe", "What's this, partner? 'LAMPLIGHTER. TEST SCHEDULE.'"],
  "office.schedule.read.2": ["grandpajoe", "'30 OCT, 1747 HRS: SECTOR 1921. One civilian vehicle, unconfirmed. See Form 7.'"],
  "office.schedule.read.3": ["grandpajoe", "'31 OCT, 1700 HRS: SECTOR 44. B-7. Please do not look directly at the sector.'"],
  "office.schedule.read.4": ["grandpajoe", "Seventeen forty-seven. That's when the sky opened over my road."],
  "office.schedule.read.5": ["grandpajoe", "I can confirm the vehicle. Red, with wood on the sides."],
  "office.schedule.read.6": ["grandpajoe", "Every hole in my desert, partner. They're makin' 'em."],
  "office.schedule.read.7": ["grandpajoe", "Today. Five o'clock."],
  "office.schedule.read.ranger": ["ranger", "...", ["hole", "question"]],
  "office.schedule.read.8": ["grandpajoe", "Sector 44. That's the boy's year; Miss said so."],
  "office.schedule.read.9": ["grandpajoe", "B-7. So that's what all the air is for: this little building goes a long way down."],

  // ---------- #18 The Bearer: Property & Effects (office-property). Ranger, from the grille, or on the top shelf ----------
  "office.prop.opal.ranger": ["ranger", "A small lady in a lavender cardigan sits at her window, knitting, with her back to the shelves.", "opal"],                                                         // at her window, her back to the shelves
  "office.prop.opal.idle.1": ["opal", "Knit two. Purl two."],                                                   // her own life, now and then
  "office.prop.opal.idle.2": ["opal", "Received."],                                                          // THUNK
  "office.prop.opal.idle.3": ["opal", "Fifty-five years at this window, and nobody has ever come for the gnome."],
  "office.prop.opal.idle.4": ["opal", "This window closes at seventeen hundred. Not one minute after."],
  "office.prop.opal.sees": ["opal", "You are not on the form, dear. Mind the gnome."],                       // she turns, and there he is on her shelves
  // the receipt: he lets it go through the slats, and it flutters down onto her counter
  "office.prop.receipt.drop.ranger": ["ranger", "Ranger pushes the receipt through the slats, and it flutters down toward the lady at the window.", ["receipt", "arrow", "opal"]],
  "office.prop.receipt.1": ["opal", "Claim number 3117. One banjo, damaged. One raccoon, unconfirmed."],
  "office.prop.receipt.2": ["opal", "Confirmed."],                                                           // she looks up: two eyes in a mask; THUNK
  "office.prop.receipt.3": ["opal", "Regulation 4. Property is returned to its owner on presentation of the receipt."],
  "office.prop.receipt.4": ["opal", "It does not say who presents it."],
  "office.prop.receipt.5": ["opal", "Thank you, raccoon."],                                                     // the banjo off the shelf, her keys, and out
  "office.prop.receipt.ranger": ["ranger", "The lady has stamped the receipt and thanked him. Ranger likes her very much.", ["opal", "heart"]],
  // the shelves, floor to ceiling, and everything on them tagged and dated
  "office.prop.shelves.ranger": ["ranger", "Shelves from the floor to the ceiling, full of tagged and dated things. Ranger loves every one of them.", ["shiny", "shiny", "heart"]],
  "office.prop.tagged.use.ranger": ["ranger", "It has a tag on it, so it belongs to somebody. Ranger leaves it where it is.", ["paper", "no"]],                                          // any tagged thing: it has a tag, it is somebody's
  "office.prop.sandal.ranger": ["ranger", "A leather sandal with a tag that says 1951. The sandal itself smells much, much older.", ["clock", "clock", "clock"]],                                  // a Roman sandal, tagged 1951
  "office.prop.lamp.ranger": ["ranger", "A small clay oil lamp. Clay doesn't shine, so Ranger moves on.", ["shiny", "no"]],                                                // a clay oil lamp: clay does not shine
  "office.prop.cup.ranger": ["ranger", "A dented tin cup with a tag on its handle. Ranger wonders who last drank from it.", ["water", "question"]],                                          // a tin cup
  "office.prop.horseshoe.ranger": ["ranger", "A horseshoe, worn bright along one edge. Ranger thinks it very fine.", ["shiny", "heart"]],
  "office.prop.hat.ranger": ["ranger", "A cowboy hat, bleached white by the sun. It is somebody's hat, but not Grandpa Joe's.", ["joe", "no"]],                                                  // a cowboy hat, bleached white: not Joe's
  "office.prop.feather.ranger": ["ranger", "A long white goose feather. Ranger would like to hold it for a while.", ["hand", "heart"]],                                          // a goose feather
  "office.prop.tape.ranger": ["ranger", "A cassette tape with a tag on it. Ranger wonders what music is inside.", ["music", "question"]],                                          // a cassette tape
  "office.prop.gnome.ranger": ["ranger", "A garden gnome with a tag round its neck. Nobody knows why it is here, and Ranger can't explain it either.", ["question", "question", "question"]],                          // a garden gnome: nobody knows
  "office.prop.boxes.ranger": ["ranger", "Boxes of forms, a box for every ten years. Ranger has found where the paper goes.", ["paper", "paper", "paper"]],                                  // FORM 7 (1971-1979), and so on
  "office.prop.boxes.use.ranger": ["ranger", "Ranger lifts a lid and finds forms. He nearly falls asleep on the spot.", "zzz"],
  "office.prop.banjo.ranger": ["ranger", "On the lowest shelf, with a tag on it: Grandpa Joe's banjo. Ranger would know it anywhere.", ["banjo", "joe", "heart"]],                                   // the low shelf, tag No. 3117: Joe's
  "office.prop.banjo.use.ranger": ["ranger", "Ranger gets both arms round the banjo and heaves. He can't lift it.", ["banjo", "up", "no"]],                                     // he cannot lift it
  "office.prop.banjo.use2.ranger": ["ranger", "Even if Ranger could lift the banjo, it would never fit through the grille and into the duct.", ["banjo", "door", "no"]],                                  // and it would not fit in the duct anyway
  "office.prop.window.ranger": ["ranger", "A sliding window that opens onto the hall. The lady keeps her seat right beside it.", ["door", "question"]],                                         // her sliding window onto the hall
  "office.prop.window.use.ranger": ["ranger", "The window is the lady's, and Ranger can't get to it from the shelf.", ["hand", "no"]],
  "office.prop.bell.ranger": ["ranger", "A little bell on the far side of the glass, for people in the hall to ring.", ["hand", "question"]],                                           // RING FOR SERVICE, on the hall side of the glass
  "office.prop.bell.use.ranger": ["ranger", "The bell is on the hall side of the glass, and Ranger can't reach it.", ["hand", "no"]],                                             // he cannot reach it
  "office.prop.stamp.ranger": ["ranger", "A date stamp and an ink pad on the counter. Ranger would love to try it, just once.", ["hand", "heart"]],                                             // her date stamp and ink pad
  "office.prop.stamp.use.ranger": ["ranger", "The stamp is the lady's, and Ranger doesn't take what belongs to somebody.", ["opal", "no"]],                                            // it is Opal's
  "office.prop.knitting.ranger": ["ranger", "A basket of gray wool, and a long gray scarf growing out of it. It looks soft enough to sleep in.", ["heart", "zzz"]],                                           // a basket, and a long gray scarf out of it
  "office.prop.knitting.use.ranger": ["ranger", "The knitting is the lady's. Ranger leaves it alone.", ["opal", "no"]],
  "office.prop.sign.ranger": ["ranger", "A sign over the window, all words and one number. It says the window closes at 1700.", ["clock", "question"]],                                          // THIS WINDOW CLOSES AT 1700
  "office.prop.door.ranger": ["ranger", "The door out to the hall. It is shut, and it is not a raccoon's way out.", ["door", "no"]],
  "office.prop.vent.ranger": ["ranger", "The grille in the ceiling, over the top shelf. That is the way back up.", "up"],                                                           // from the shelf: the way back up
  "office.prop.counter.ranger": ["ranger", "The lady's counter, with her papers squared on it. Ranger wonders what she does with them all.", ["paper", "question"]],
  "office.prop.receipt.lying.ranger": ["ranger", "The receipt lies on the lady's counter, right where she will see it.", ["receipt", "heart"]],                                  // the receipt, on her counter
  "office.prop.stool.ranger": ["ranger", "A tall stool at the window, with the lady sitting on it.", "chair"],
  "office.prop.with.ranger": ["ranger", "Ranger keeps hold of it. That isn't what the lady at the window is waiting for.", "no"],                                                           // anything but the receipt, from the grille

  // ---------- Opal's visit to the Comfortable Room (opalTree): the key in the door, and Opal with the banjo ----------
  "office.opal.1": ["opal", "Afternoon, Joe."],
  "office.opal.2": ["grandpajoe", "Opal."],
  "office.opal.3": ["opal", "A raccoon brought me your receipt."],
  "office.opal.4": ["grandpajoe", "He's good like that."],
  "office.opal.5": ["opal", "Sign here."],                                                                       // he signs (the hook sign: THUNK)
  "office.opal.6": ["opal", "Forty-one statements of nothing, Joe Hollis."],                                     // over her glasses: the one time
  "office.opal.7": ["grandpajoe", "I'm a man of few observations."],
  "office.opal.8": ["opal", "It's warm in here."],
  "office.opal.9": ["grandpajoe", "It's the Comfortable Room."],
  "office.opal.10": ["opal", "One banjo, damaged. Returned to its owner."],                                      // the hook banjo: into his hands
  "office.opal.11": ["grandpajoe", "Well. Look at you, old girl."],                                                // to the banjo
  "office.opal.vent": ["opal", "And good afternoon to you too, up there."],                                   // Ranger's eyes in the room's vent
  "office.opal.opt.damage": ["grandpajoe", "What did they do to her, Opal?"],
  "office.opal.damage.1": ["opal", "Jed's head went through her, Joe. It's in the report."],
  "office.opal.damage.2": ["opal", "Rim: sound. Neck: sound. Strings: sound. Head: gone."],
  "office.opal.opt.jed": ["grandpajoe", "How's Jed, ma'am?"],
  "office.opal.jed.1": ["opal", "In the break room, with an ice pack and the hoop still on."],
  "office.opal.jed.2": ["opal", "Mostly he would like a cheeseburger."],
  "office.opal.opt.sandal": ["grandpajoe", "Still got that Roman sandal, Opal?"],
  "office.opal.sandal.1": ["opal", "Since 1951. The Director brought it in himself, and he has never come back for it."],
  "office.opal.sandal.2": ["grandpajoe", "Maybe he don't want it back."],
  "office.opal.sandal.3": ["opal", "Everybody wants something back, Joe. That's what my window is for."],
  "office.opal.opt.lamp": ["grandpajoe", "Opal, what's Lamplighter?"],
  "office.opal.lamp.1": ["opal", "That's a green-page word, Joe."],
  "office.opal.lamp.2": ["opal", "I file the green pages, Joe. Reading is a different department."],
  "office.opal.opt.door": ["grandpajoe", "Couldn't leave that door open behind you, could you, ma'am?"],
  "office.opal.door.1": ["opal", "Regulations, Joe."],
  "office.opal.door.2": ["grandpajoe", "I figured."],
  "office.opal.door.3": ["opal", "But I'll lock it gently."],
  "office.opal.opt.thanks": ["grandpajoe", "Thank you kindly, Opal."],
  "office.opal.thanks": ["opal", "Regulation 4, Joe. Thank the raccoon."],
  "office.opal.lock": ["opal", "Regulations, Joe."],                                                             // from the door, as she locks it

  // ---------- #19 Wendell's Pie: the break room (office-breakroom). Ranger, from the grille, or on the fridge and counter ----------
  "office.break.fridge.ranger": ["ranger", "A fridge with a notice taped to its door. Ranger wonders what is inside.", ["eye", "question"]],                                         // LABEL YOUR LUNCH. MGMT.
  "office.break.fridge.use.ranger": ["ranger", "Ranger tugs at the fridge door. It will not open for him.", ["hand", "no"]],                                          // he tugs the door: it will not come
  "office.break.fridgesign.ranger": ["ranger", "A notice on the fridge: 'Label your lunch. Mgmt.' Ranger can't read it, and has no lunch to label.", "question"],
  "office.break.magnets.ranger": ["ranger", "Bright little magnets all over the fridge door. Ranger thinks they are lovely.", ["shiny", "heart"]],
  "office.break.magnets.use.ranger": ["ranger", "Ranger tries to pick a magnet off the door. It sticks.", ["hand", "no"]],                                         // they stick
  "office.break.menu.ranger": ["ranger", "A takeout menu, with a picture of a cheeseburger on it. Ranger gazes at it.", ["cheeseburger", "heart"]],                                     // a takeout menu
  "office.break.menu.use.ranger": ["ranger", "Ranger sniffs the menu. A picture of a cheeseburger is not a cheeseburger.", ["cheeseburger", "no"]],                         // a picture of one is not one
  "office.break.forks.ranger": ["ranger", "A box of plastic forks on top of the fridge. Ranger has never needed one.", ["hand", "question"]],                                         // a box of plastic forks, on the fridge
  "office.break.forks.use.ranger": ["ranger", "Ranger eats with his hands, and leaves the forks in their box.", "no"],
  "office.break.plant.ranger": ["ranger", "A dusty plant in a pot, on top of the fridge. Ranger wonders when it last had a drink.", ["water", "question"]],                                        // a dusty plant, on the fridge
  "office.break.plant.use.ranger": ["ranger", "Ranger has no water to give the plant, and the plant has given up asking.", ["water", "no"]],
  "office.break.vent.ranger": ["ranger", "The grille in the ceiling, over the fridge. That is the way back up into the duct.", "up"],
  "office.break.counter.ranger": ["ranger", "The counter, with a whole pie on it, and a card standing in front of the pie.", ["pie", "heart"]],
  "office.break.counter.after.ranger": ["ranger", "An empty pie tin on the counter. Ranger wonders what a round tin might be good for.", ["piepan", "question"]],                               // the pie eaten
  "office.break.sink.ranger": ["ranger", "A sink, with a tap that runs. Ranger is very fond of a sink.", ["water", "heart"]],
  "office.break.sink.use.ranger": ["ranger", "Ranger runs the tap and washes his hands, back and front.", ["hand", "water", "heart"]],                                // he washes his paws
  "office.break.rack.ranger": ["ranger", "A dish rack beside the sink, with a few clean spoons shining in it.", "shiny"],                                                       // the dish rack
  "office.break.coffee.ranger": ["ranger", "A coffee maker, its pot steaming. Ranger keeps well away from it.", ["hot", "no"]],                                               // the coffee maker, its pot steaming
  "office.break.cups.ranger": ["ranger", "A stack of paper cups by the coffee maker. Ranger wonders whether any has water in it.", ["water", "question"]],
  "office.break.cups.use.ranger": ["ranger", "Ranger looks into the top cup. It is empty.", ["water", "no"]],                               // empty
  "office.break.microwave.ranger": ["ranger", "A microwave oven, with a little door on the front. Ranger wonders what is behind it.", ["door", "question"]],
  "office.break.microwave.use.ranger": ["ranger", "Ranger pulls at the microwave's door. It does not open, and there is nothing inside anyway.", ["hand", "no"]],
  "office.break.pie.ranger": ["ranger", "Wendell's birthday pie, whole, on the counter. Ranger has never wanted anything so much.", ["pie", "heart"]],
  "office.break.card.ranger": ["ranger", "A card stands by the pie: 'Happy birthday Wendell. Do not eat. (Regulations)'. Ranger can't read.", ["paper", "question"]],                                         // HAPPY BIRTHDAY WENDELL. DO NOT EAT. (REGULATIONS)
  "office.break.card.use.ranger": ["ranger", "Ranger turns the card over. It is only paper, and paper is not pie.", ["paper", "no"]],
  "office.break.card.after.ranger": ["ranger", "Ranger's best bottle cap lies on Wendell's card. It was a fair trade, properly made.", ["bottlecap", "heart"]],                                  // his bottle cap on it, for Wendell
  "office.break.board.ranger": ["ranger", "A corkboard covered in sheets of paper. One sheet has a picture at the top.", ["paper", "paper", "paper"]],                                  // the corkboard
  "office.break.board.use.ranger": ["ranger", "The other sheets on the board are no use to Ranger. They are all words.", ["paper", "no"]],                             // the other sheets: not his
  "office.break.form7.ranger": ["ranger", "A notice pinned to the board: 'Form 7 is not optional.' It is all words, and Ranger yawns.", ["paper", "zzz"]],                                             // FORM 7 IS NOT OPTIONAL
  "office.break.found.ranger": ["ranger", "A notice: 'Found: one Roman sandal (1951). See Opal.' Ranger wonders what it says.", ["paper", "question"]],                                        // FOUND: ONE ROMAN SANDAL (1951). SEE OPAL
  "office.break.bowling.ranger": ["ranger", "A list of names under a drawing of a bowling pin. Ranger doesn't know the game.", "question"],                                                 // the bowling league
  "office.break.schedule.ranger": ["ranger", "A sheet with a lamp printed at the top, and rows of times under it. Grandpa Joe would want to see this.", ["lamp", "clock", "joe"]],                                  // LAMPLIGHTER. TEST SCHEDULE: a lamp on top, and times
  "office.break.couch.ranger": ["ranger", "A couch with a knitted blanket over the back. It looks very comfortable.", ["zzz", "heart"]],                                             // the couch, and its afghan
  "office.break.couch.use.ranger": ["ranger", "There is a man in gray asleep on the couch already, and Ranger won't wake him.", ["suit", "zzz", "no"]],                       // Floyd is on it
  "office.break.floyd.ranger": ["ranger", "A man in a gray suit, asleep sitting up on the couch, still in his sunglasses.", ["suit", "zzz"]],
  "office.break.floyd.use.1": ["suit4", "Regulation twenty-two, sir..."],                                       // Ranger tries to wake him: he does not
  "office.break.floyd.use.ranger": ["ranger", "The man on the couch sleeps on. Ranger lets him.", "zzz"],
  "office.break.chair.ranger": ["ranger", "A plastic chair, empty now. The man with the hoop round his neck has gone after his lunch.", "chair"],                                                      // the plastic chair, Jed gone
  "office.break.jed.ranger": ["ranger", "Jed, with an ice pack on his head and a banjo hoop round his neck. He never takes his eyes off the pie.", ["suit", "eye", "pie"]],                                         // Jed, ice pack on his head, watching the pie
  "office.break.vending.ranger": ["ranger", "A vending machine, empty but for one row of peanuts. Ranger's hopes rise.", ["peanuts", "heart"]],
  "office.break.vending.use.ranger": ["ranger", "Ranger presses every button on the machine. One packet of peanuts falls, and he saves it for later.", ["peanuts", "clock"]],                                   // every button; one packet falls: for later
  "office.break.vending.again.ranger": ["ranger", "Ranger presses every button again. Nothing more comes out.", "no"],                                                 // nothing more comes
  "office.break.buttons.ranger": ["ranger", "A row of buttons on the vending machine. Ranger wonders what each one does.", ["hand", "question"]],
  "office.break.tray.ranger": ["ranger", "The tray at the bottom of the vending machine, where the peanuts fall.", "peanuts"],
  "office.break.clock.ranger": ["ranger", "A clock on the break-room wall, ticking toward five.", "clock"],
  "office.break.speaker.ranger": ["ranger", "A speaker up in the corner of the ceiling. A lady's voice comes out of it now and then.", "question"],
  "office.break.speaker.use.ranger": ["ranger", "The speaker is up in the corner of the ceiling, where Ranger can't reach it.", ["hand", "no"]],                           // up in the ceiling corner
  "office.break.door.ranger": ["ranger", "The break-room door, out to the hall. It is not Ranger's way out.", ["door", "no"]],
  // Jed, in his chair with the ice pack and the hoop, facing the counter; heard from the grille
  "office.jed.idle.1": ["agent", "I am not going to eat the pie."],
  "office.jed.idle.2": ["agent", "It says do not eat. It says it in capitals."],
  "office.jed.idle.3": ["agent", "Floyd. Floyd. Are you awake?"],                                                // Floyd answers in his sleep
  "office.jed.idle.4": ["agent", "Houston, it's Jed. Is there any word on the cheeseburger?"],
  "office.jed.idle.5": ["houston", "Jed, you have asked me that nine times."],                                   // in his earpiece
  "office.jed.idle.6": ["agent", "Ten, now."],
  "office.jed.idle.7": ["agent", "The hoop is evidence, Floyd. I am not permitted to remove it."],
  // Ranger drops in while Jed is there
  "office.jed.ranger.1": ["agent", "Raccoon. In the break room."],
  "office.jed.ranger.2": ["agent", "Do you have a cheeseburger?"],
  "office.jed.ranger.3": ["ranger", "...", ["cheeseburger", "no"]],
  "office.jed.ranger.4": ["agent", "No. Shoo, please."],                                                         // and back up he goes
  // office.pa.burger on the speakers: Jed is up so fast the ice pack is still in the air
  "office.jed.go.1": ["agent", "Thank you, Houston."],
  "office.jed.go.2": ["agent", "Floyd. My cheeseburger, Floyd."],
  "office.jed.go.3": ["suit4", "Lunch rides in the back, sir..."],
  // Floyd, on his regulation rest (twenty minutes, Regulation 22), asleep sitting up in his sunglasses, and talking
  "office.floyd.1": ["suit4", "Regulation twenty-two, sir..."],
  "office.floyd.2": ["suit4", "Twenty minutes, sir... a regulation rest..."],
  "office.floyd.3": ["suit4", "Neither confirm... nor deny... the raccoon..."],
  "office.floyd.4": ["suit4", "Lifting on three, sir... one... two..."],
  // the pie: Jed gone, Ranger drops onto the fridge, then the counter
  "office.pie.fridge.ranger": ["ranger", "From the top of the fridge Ranger can see the whole pie, and nobody watching it.", ["pie", "heart"]],
  "office.pie.nibble": ["ranger", "Ranger takes one small nibble of the pie, only to be sure.", "pie"],
  "office.pie.eat": ["ranger", "Then Ranger eats the pie, the whole of it.", ["pie", "heart"]],                                                         // the whole pie
  "office.pie.full": ["ranger", "Ranger leans back, full to the ears and entirely content.", ["heart", "zzz"]],                                                     // a pause; a satisfied lean back
  "office.pie.trade": ["ranger", "Ranger sets his best bottle cap in the middle of the empty tin. He doesn't steal. He trades.", ["bottlecap", "arrow", "piepan"]],                                       // his best bottle cap, in the tin: a trade
  "office.pie.sticky": ["ranger", "Ranger picks up the empty pie tin. It is sticky, and wants washing.", ["piepan", "water"]],                                                   // the tin is sticky
  "office.pie.card": ["ranger", "Taking the tin, Ranger leaves his bottle cap on Wendell's card, where Wendell will find it.", ["bottlecap", "arrow", "paper"]],                                         // taking the tin, he leaves the cap on Wendell's card
  "office.pie.wash": ["ranger", "Ranger washes the pie tin at the sink until it comes up shining.", ["piepan", "shiny"]],                                                     // the wash, at the sink: it comes up shining
  "office.pie.schedule": ["ranger", "Ranger takes the sheet with the lamp on it down off the corkboard. It is for Grandpa Joe.", ["lamp", "clock", "joe"]],                                            // off the corkboard: for Joe

  // ---------- the intercom (intercomTree): DISPATCH. PRESS TO TALK. Houston; and Grandpa Joe, who never lies ----------
  "office.intercom.press": ["houston", "Dispatch."],
  "office.intercom.opt.joe": ["grandpajoe", "Houston, this is Joe."],
  "office.intercom.joe.1": ["houston", "Mr. Grandpa, please return to your chair."],
  "office.intercom.joe.2": ["houston", "Mr. Grandpa. Chair."],
  "office.intercom.joe.3": ["houston", "Mr. Grandpa, I have a building to run."],
  "office.intercom.opt.name": ["grandpajoe", "Ma'am, it's just Joe."],
  "office.intercom.name.1": ["houston", "You are on the form as Grandpa, Mr. Grandpa."],
  "office.intercom.name.2": ["grandpajoe", "Folks do call me that."],
  "office.intercom.opt.out": ["grandpajoe", "Could somebody let me out, ma'am?"],
  "office.intercom.out": ["houston", "You have not completed the questionnaire, Mr. Grandpa."],
  "office.intercom.opt.air": ["grandpajoe", "Ma'am, it's a mite warm in here."],
  "office.intercom.air.1": ["houston", "The air is off, Mr. Grandpa. Maintenance has been informed."],
  "office.intercom.air.2": ["houston", "Maintenance is Wendell. Wendell is on the door, and it is his birthday."],
  "office.intercom.opt.burger": ["grandpajoe", "Ma'am, could I get a cheeseburger?"],
  "office.intercom.burger.1": ["houston", "Mr. Grandpa, you are not Jed."],
  "office.intercom.burger.2": ["houston", "You are still not Jed, Mr. Grandpa."],
  "office.intercom.opt.behalf": ["grandpajoe", "Ma'am, I'm callin' on behalf of Jed. Jed would still like the cheeseburger."],
  "office.intercom.behalf.1": ["houston", "On behalf of Jed."],
  "office.intercom.behalf.2": ["houston", "Oh, for heaven's sake."],
  // the hook burger: office.pa.burger on every speaker, and Jed up and gone
  "office.intercom.behalf.3": ["houston", "He has waited since five this morning. Thank you for asking, Mr. Grandpa."],
  "office.intercom.behalf.4": ["grandpajoe", "Any time, ma'am."],
  "office.intercom.opt.howjed": ["grandpajoe", "How's Jed doin' with his cheeseburger?"],
  "office.intercom.howjed": ["houston", "Eaten, Mr. Grandpa, in four bites. I timed it."],
  "office.intercom.opt.lamp": ["grandpajoe", "What's Lamplighter, ma'am?"],
  "office.intercom.lamp": ["houston", "That is a green-page word, Mr. Grandpa. Please do not say it on my intercom."],
  "office.intercom.opt.b7": ["grandpajoe", "Ma'am, what's down on B-7?"],
  "office.intercom.b7.1": ["houston", "You are not authorized to ask about B-7, Mr. Grandpa."],
  "office.intercom.b7.2": ["grandpajoe", "Can I ask about B-6?"],
  "office.intercom.b7.3": ["houston", "No."],
  "office.intercom.opt.bye": ["grandpajoe", "Thank you kindly, ma'am."],
  "office.intercom.bye": ["houston", "Dispatch out."],

  // ---------- #20 A Soundproof Room: the pie tin on the banjo, and the Last Stop Rag through every vent ----------
  "office.mend.1": ["grandpajoe", "Hold still, old girl. Here's your new head."],
  "office.mend.2": ["grandpajoe", "One bracket. Two. Three... Snug."],                             // tightened, bracket by bracket
  "office.mend.3": ["grandpajoe", "Let's hear you, then."],                                                      // one string: the loudest sound the building has made
  "office.mend.4": ["grandpajoe", "Oh, my. She's louder than she ever was."],
  "office.mend.clunk": ["grandpajoe", "That ain't music. That's furniture."],                                    // the broken banjo, played: one dull clunk
  // the door: Dale and Merle, and Wendell behind them (ragTree); he plays on through all of it
  "office.rag.door.1": ["suit1", "Sir. Please."],
  "office.rag.door.2": ["suit2", "Sir, it is in the ducts. It is on every floor."],
  "office.rag.door.3": ["suit1", "B-3 has called twice, sir."],
  "office.rag.opt.medical": ["grandpajoe", "Can't stop, son. Medical condition."],
  "office.rag.medical.1": ["suit1", "Sir, there is no medical condition in your file."],
  "office.rag.medical.2": ["grandpajoe", "At my age, son, I am a medical condition."],
  "office.rag.medical.3": ["suit2", "I will add it to the file. Sorry, sir."],
  "office.rag.medical.again": ["suit2", "It is in your file now. Sorry, sir."],
  "office.rag.opt.twice": ["grandpajoe", "This here's the Last Stop Rag. You fellas want to hear it twice?"],
  "office.rag.twice.1": ["suit2", "No, sir. Sorry."],
  "office.rag.twice.2": ["suit1", "Once was very nice, sir."],
  "office.rag.twice.3": ["suit3", "Sir, please. It is my birthday."],
  "office.rag.opt.home": ["grandpajoe", "I'd sure like to go on home, fellas."],
  "office.rag.home": ["suit1", "Sir, you have not completed the questionnaire."],
  "office.rag.opt.lamp": ["grandpajoe", "Lamplighter."],                                                          // once he has read the schedule
  "office.rag.lamp.1": ["suit1", "Where did you hear that word, sir?"],
  "office.rag.lamp.2": ["grandpajoe", "A raccoon brought it to me, son."],
  "office.rag.lamp.3": ["suit2", "Sorry, sir. That is a green-page word, and it is on B-7."],
  "office.rag.lamp.4": ["suit1", "Merle!"],
  "office.rag.lamp.5": ["suit2", "Sorry, Dale."],
  "office.rag.opt.somewhere": ["grandpajoe", "You got somewhere I can play where I won't bother nobody?"],         // once he has read the schedule
  "office.rag.lever.1": ["suit1", "Sir, the only soundproof room in the building is B-7."],
  "office.rag.lever.2": ["suit2", "We are not authorized to take civilians to B-7, sir."],
  "office.rag.lever.3": ["suit3", "Dale, it is my BIRTHDAY."],                                                    // after he plays louder (the hook)
  "office.rag.lever.4": ["suit1", "Sir, we are now authorized."],
  "office.rag.opt.stop": ["grandpajoe", "Well. Since you asked nice."],                                        // he stops: he is a gentleman
  "office.rag.stop.1": ["suit1", "Thank you, sir."],
  "office.rag.stop.2": ["suit2", "It is a very nice song, sir. Sorry."],
  "office.rag.stop.3": ["suit1", "For your comfort, sir."],                                                      // and they lock the door again

  // ---------- Cut-scene: Going Down (js/content/cutscenes/office-down.js): the hall, seen through the grille ----------
  "office.down.card": ["narrator", "Going Down"],
  // Grandpa Joe walking between Dale and Merle, hat on, playing; Wendell behind with his fingers in his ears
  "office.down.1": ["grandpajoe", "You boys ever been down to B-7?"],
  "office.down.2": ["suit1", "No, sir. We have never been authorized."],
  "office.down.3": ["grandpajoe", "Well. Now you are."],
  "office.down.4": ["suit3", "It is still my birthday, Dale."],
  "office.down.5": ["suit1", "Noted, Wendell."],
  // the elevator, and its own polite little tune
  "office.down.6": ["grandpajoe", "Turn that off, son. I brought my own."],
  "office.down.7": ["grandpajoe", "Mind the--"],
  "office.down.8": ["suit2", "Minding the hat, sir."],
  // the doors close on the Rag; at the grille over the hall, Ranger; then at the B-7 shaft, the big fan stopped
  "office.down.ranger.1": ["ranger", "...", ["joe", "down"]],
  "office.down.ranger.2": ["ranger", "...", ["down", "joe", "heart"]],
  "office.down.ranger.3": ["ranger", "...!"],                                                                     // a look at us, in his mirror shades, and he goes
  // the card that ends the stage and the demo
  "office.card.1": ["narrator", "LAMPLIGHTER"],
  "office.card.2": ["narrator", "to be continued"],

  // ---------- Houston, on the building's speakers (await g.pa("office.pa.<id>")) ----------
  "office.pa.arrive": ["houston", "Attention all personnel. One civilian has arrived. Please make him comfortable."],
  "office.pa.pie": ["houston", "Attention all personnel. It is Wendell's birthday. There is a pie in the break room. Do not eat the pie."],
  "office.pa.raccoon": ["houston", "Attention all personnel. One raccoon has been noted. In trash. It is not on the form. Carry on."],
  "office.pa.air.1": ["houston", "Attention all personnel. The air is off. Will maintenance please see to it."],
  "office.pa.air.2": ["houston", "Wendell, you are maintenance."],
  "office.pa.air.3": ["houston", "Then the air will have to wait."],                                              // after Wendell's answer, in the lot
  "office.pa.comfort": ["houston", "Reminder. Interview Room C has been rated comfortable."],
  "office.pa.burger": ["houston", "Jed. Your cheeseburger is at the front desk."],
  "office.pa.peanuts": ["houston", "The vending machine on the ground floor is out of everything but peanuts."],
  "office.pa.peanuts.2": ["houston", "The vending machine on the ground floor is now out of peanuts."],             // once Ranger has his
  "office.pa.music": ["houston", "Attention all personnel. There is... music. On the ground floor."],
  "office.pa.music.2": ["houston", "B-3 would like the music to stop. So would B-4. So would I."],
  "office.pa.down": ["houston", "Attention all personnel. The music is going down to B-7. Thank you for your patience."],
  "office.pa.test": ["houston", "Lamplighter test at seventeen hundred hours. Sector 44. Please do not look directly at the sector."],
  // the building's life, now and then
  "office.pa.fairweather": ["houston", "Dr. Fairweather to B-7, please."],
  "office.pa.limo": ["houston", "Will the owner of a gray limousine please stop leaving the door open."],
  "office.pa.plant": ["houston", "The Director's plant needs watering."],
  "office.pa.form7": ["houston", "Reminder. Form 7 is not optional."],

  // ---------- hints: a beat's hint for each of the two (ids.md says which stage of a puzzle each is for) ----------
  // #16 office.inside (Ranger's)
  "hint.office.inside.ranger": ["ranger", "Ranger needs a way up to the roof. The trash can would make a step, if it stood under the drainpipe.", ["trash", "plus", "up"]],
  "hint.office.inside.ranger.2": ["ranger", "The grille on the side of the big unit is held by four wing nuts. Ranger has the hands to turn them.", ["wingnut", "hand"]],                                          // on the roof, the grille on
  "hint.office.inside.ranger.3": ["ranger", "The fan must stop before Ranger can go in. The switch beside it has a fan with a line through it.", ["switch", "fan", "no"]],                                      // the grille off, the fan turning
  "hint.office.inside.grandpajoe": ["grandpajoe", "Nothin' I can do from this chair. Getting into places is Ranger's end of it."],
  // #17 office.room (Grandpa Joe's)
  "hint.office.room.grandpajoe": ["grandpajoe", "Seventy-two degrees and forty-seven pages. Those boys could go all week, unless it warmed up."],
  "hint.office.room.grandpajoe.2": ["grandpajoe", "Those boys don't like it warm. I saw 'em sweat in that limousine."],          // the room warming
  "hint.office.room.grandpajoe.3": ["grandpajoe", "Eighty-one. If there's a regulation for that, now's when I ask about it."],     // at 81
  "hint.office.room.ranger": ["ranger", "Grandpa Joe is shut in with two men who can't stand the heat. With the air off, the room will warm up.", ["joe", "hot"]],
  // #18 office.bearer (both)
  "hint.office.bearer.grandpajoe": ["grandpajoe", "Opal'll honor a receipt for one banjo. I just can't walk it down the hall."],
  "hint.office.bearer.grandpajoe.2": ["grandpajoe", "Ranger's got the receipt, and Opal's got the banjo. Rest of it's up to him."],
  "hint.office.bearer.ranger": ["ranger", "Ranger ought to find Grandpa Joe. The first grille along the duct looks down into his room.", ["joe", "down"]],                                                // he has not been to Joe's grille
  "hint.office.bearer.ranger.2": ["ranger", "The receipt goes to the lady with the glasses on a chain. Ranger can drop it through the grille over her counter.", ["receipt", "arrow", "opal"]],                                 // he has the receipt
  "hint.office.bearer.ranger.2.joe": ["grandpajoe", "He says the receipt goes to Opal. That's right, partner: glasses on a chain."],
  // #19 office.pie (both)
  "hint.office.pie.grandpajoe": ["grandpajoe", "A pie tin would mend her. If there's a pie in this building, Ranger's the one to sniff it out."],
  "hint.office.pie.grandpajoe.2": ["grandpajoe", "Jed won't leave that pie for anything but a cheeseburger. Houston sends those, and she's on that intercom."],
  "hint.office.pie.grandpajoe.3": ["grandpajoe", "Jed's gone after his lunch. That pie's Ranger's business now."],
  "hint.office.pie.grandpajoe.4": ["grandpajoe", "I'd bet that break room's got more in it than pie. Ranger's got the eyes for it."],
  "hint.office.pie.ranger": ["ranger", "The man with the hoop will leave the pie only for a cheeseburger. Ranger should tell Grandpa Joe at the vent.", ["suit", "cheeseburger", "joe"]],                                   // Jed at the pie
  "hint.office.pie.ranger.2": ["ranger", "The pie is unguarded, and under the pie is a tin. Grandpa Joe needs a round tin for his banjo.", ["pie", "piepan", "joe"]],                                         // Jed gone
  "hint.office.pie.ranger.3": ["ranger", "The pie tin is on the counter, sticky. Ranger should take it and wash it at the sink.", ["piepan", "water"]],                                              // the tin sticky
  "hint.office.pie.ranger.4": ["ranger", "One sheet on the corkboard has a lamp at the top. Ranger should take it and hand it down to Grandpa Joe.", ["lamp", "arrow", "joe"]],                                         // the tin clean; the schedule still on the board
  // #20 office.rag (Grandpa Joe's)
  "hint.office.rag.grandpajoe": ["grandpajoe", "A broken banjo and a clean pie tin. Jolene would call that a banjo waitin' to happen."],
  "hint.office.rag.grandpajoe.2": ["grandpajoe", "I could play 'em out of this room. Don't know where I'm playin' to yet."],
  "hint.office.rag.grandpajoe.3": ["grandpajoe", "Those boys will do anything to stop the Rag. Even take a man where he wants to go."],
  "hint.office.rag.ranger": ["ranger", "...", ["joe", "music"]],
  "hint.office.rag.ranger.joe": ["grandpajoe", "He says play it, Joe. I aim to, partner."],

  // ---------- the things carried in this stage (js/content/world.js items; pictures art/items/<id>.png) ----------
  "item.banjo-broken.grandpajoe": ["narrator", "Grandpa Joe's banjo. Jed's head went clean through it, and all it wants now is a new head."],
  "item.pietin.grandpajoe": ["narrator", "A pie tin, washed and shining. Grandpa Joe has a feeling this was Wendell's birthday."],
  "item.pietin.ranger": ["ranger", "...", ["piepan", "plus", "banjo"]],
  "item.pietin.ranger.joe": ["grandpajoe", "He says it'd make a fine banjo head. I was thinkin' the same."],
  "item.banjo-pie.grandpajoe": ["narrator", "A banjo with a pie tin for a head. Jolene will never let Grandpa Joe hear the end of it."],
  "item.schedule.grandpajoe": ["narrator", "The Lamplighter test schedule. Yesterday at five forty-seven, Sector 1921. Today at five, Sector 44, down on B-7."],
  "item.schedule.ranger": ["ranger", "...", ["lamp", "clock", "joe"]],
  "item.schedule.ranger.joe": ["grandpajoe", "He says it's got a lamp on top, and times, and it's for me. Right three times."],
  "item.bottlecap.ranger": ["ranger", "...", ["bottlecap", "shiny", "heart"]],
  "item.bottlecap.ranger.joe": ["grandpajoe", "That's his best bottle cap. He's had it longer than he's had me."],
  "item.peanuts.ranger": ["ranger", "...", ["peanuts", "clock"]],
  "item.peanuts.ranger.joe": ["grandpajoe", "He says those are for later."],
  "item.peanuts.grandpajoe": ["narrator", "A packet of peanuts, from a machine Grandpa Joe has never seen. Ranger is a planner."],
  "office.item.receipt.ranger": ["ranger", "Grandpa Joe's receipt for one banjo. It goes to Opal, the lady with the glasses on a chain.", ["receipt", "arrow", "opal"]],                                   // in his stash, in the Office

  // ---------- the stock replies in the Office, for story.fallbacks, story.see and story.give (ids.md) ----------
  "office.nope.grandpajoe.1": ["narrator", "That isn't on the form, and Grandpa Joe lets it be."],
  "office.nope.grandpajoe.2": ["narrator", "Grandpa Joe would try it, but he expects there's a regulation against it."],
  "office.nope.grandpajoe.3": ["narrator", "Nothing doing. Grandpa Joe takes the news comfortably."],
  "office.look.grandpajoe.1": ["narrator", "It is government issue, gray, and most likely rated comfortable."],
  "office.hint.none.grandpajoe": ["grandpajoe", "I ain't got a notion. And they asked me two pages of questions to make sure."],
  "office.give.grandpajoe.1": ["grandpajoe", "Here, partner. Mind the corners."],
  "office.see.grandpajoe.ranger": ["narrator", "Ranger, in his mirror shades. He got in where only the air goes."],
  "office.nope.ranger.1": ["ranger", "Ranger thinks it over and decides against it.", "no"],
  "office.nope.ranger.2": ["ranger", "Ranger turns it over in his mind and can't see what it would do.", "question"],
  "office.nope.ranger.3": ["ranger", "Ranger tries it with both hands, and nothing comes of it.", ["hand", "no"]],
  "office.look.ranger.1": ["ranger", "Ranger gives it a good look. There is nothing in it for a raccoon.", ["eye", "zzz"]],
  "office.hint.none.ranger": ["ranger", "Ranger can't think what to do next. He wonders what Grandpa Joe would do.", ["joe", "question"]],
  "office.give.ranger.1": ["ranger", "Ranger holds it out flat on both hands, the proper way to offer a thing.", ["hand", "heart"]],
  "office.see.ranger.grandpajoe": ["ranger", "Grandpa Joe, straw hat and all. He is Ranger's, mostly, and Ranger is glad of him.", ["joe", "heart"]],
  // the Office's map: who may travel where (a lead's refusal, as the map's refusals are said)
  "office.map.locked.grandpajoe": ["grandpajoe", "I'd go, but I'm locked in. For my comfort."],
  "office.map.rooms.ranger": ["ranger", "Ranger doesn't go into rooms by their doors. His way is the duct, and the grille over each one.", ["door", "no"]],                                                     // a room: not by its door
  "office.map.b7.grandpajoe": ["grandpajoe", "B-7. RESTRICTED. Ain't nobody invited me."],
  "office.map.b7.ranger": ["ranger", "B-7 is a long way down, and Ranger isn't going down there on his own.", ["down", "no"]],
  // ---- TALK-24 (10 November: dialogue trees with topics, every act): the topics a talk's questions are gathered under ----
  "office.iv.topic.aside": ["grandpajoe", "Before I answer that, fellas..."],
  "office.iv.back": ["grandpajoe", "Go on, son. Ask your question."],
  "office.vent.topic.banjo": ["grandpajoe", "Partner, about my banjo."],
  "office.vent.topic.food": ["grandpajoe", "Partner, about somethin' to eat."],
  "office.vent.topic.partners": ["grandpajoe", "Partner, let's just talk a minute."],
  "office.opal.topic.office": ["grandpajoe", "While you're here, Opal. Couple of questions."],
  "office.intercom.topic.more": ["grandpajoe", "Ma'am, while I got you..."],
  "office.rag.topic.tell": ["grandpajoe", "Let me tell you boys somethin'."],
};
