// Act One: Egypt, about 1920 B.C. (the Bible's own count of years, as Ussher made it: docs/CHARACTERS.md, "How the
// game counts the years"). Every line the four Egypt scenes speak, the hints for the act's beats, and what Dad says
// when he looks at a thing in his pockets.
//   "line.id": ["who", "What they say."]
//
// Speakers: dad; Lot, Abram's nephew, by the river (lot); and the eight Egyptians (scribe, overseer, hauler1,
// hauler2, hauler3, guard, lampboy, goldsmith). These rules hold all through, and briefs/out/check-egypt.mjs holds
// the lines to them:
//   - Dad shortens his words, and the people of the time never do.
//   - Dad never raises his voice: there is not one exclamation mark in his lines.
//   - An Egyptian says only what is true of the time (docs/PUZZLES-egypt.md has the list, and what has been
//     checked). Dad may guess wrong out loud, and is put right.
//   - Dad is a Christian father standing in the Egypt of his Bible. He prays three times, in his own words (the
//     arrival, the dark doorway, the open door) and no more. When he quotes Scripture it is the King James Version,
//     word for word (the check holds each quotation to the checked text in briefs/out/facts-home.json); anything
//     else from the Bible he tells in his own words, with no quotation marks. PASS-17E: and he does not say the
//     reference (the author's rule of 16 October: chapter and verse are said aloud only when natural, which in this
//     game is Big Sister's way, and she is not in this act; everyone else just says the words, and the references
//     live in the documents: docs/PUZZLES-egypt.md, "Historical statements"). Until round seventeen he said each one.
//     No Egyptian speaks of Israel, Joseph or Moses, or of anybody's God, and nobody's belief is anybody's joke.
//   - Years: only the Bible's own count (briefs/DATING.md). From here to the present is "nearly four thousand
//     years"; from here to Rome, "nearly nineteen hundred". Nobody uses the textbook figures, or millions of years.
//   - Abram is in Egypt this week (Genesis 12:10-20), and the man praying under the palm by the river, while his
//     donkey drinks, is his nephew Lot (Genesis 13:1: "and Lot with him"). Lot tells who he is as his own memory, in
//     his own words, and only what Genesis 11:27 to 13:5 tells: never quoted, no reference, nothing of what is still
//     to come to him, and no judgment of anybody, his uncle least of all. He prays; he is the one person of the time
//     who speaks of the LORD. Until Dad has heard him, Dad does not know WHEN he is, and only wonders; after it
//     ("egypt.heardAbram") he knows: what he says at the river, the reeds and the open door follows. Up at the site
//     the scribe has the same week from the Egyptian side, as palace gossip, with no idea whom he is talking about,
//     and Dad hears it knowing more than he does. Nobody meets Abram or Sarai, and nobody passes judgment.
//   - General Feathers, his youngest's stuffed hen, is in his suitcase under the shirts. No puzzle needs her. He
//     talks to her, and shows her to people: five of them answer once each, in character; for the rest, and after
//     that, Dad has a stock reply. Nobody in this Egypt has seen a chicken (they keep geese, ducks and pigeons), and
//     nor has Lot, who keeps flocks and herds.
//
// The lines marked "kept" are the author's own, from the first version of the act. They are the standard the rest
// was written to: leave them word for word. The two marked "changed" are his with a word or two altered, on purpose.
// (docs/PUZZLES-egypt.md says which of the first version's lines were dropped, and why.)
//
// THE CAR'S INSIDE (round thirteen, 13 October: the author's own request of 8 October; briefs/CAR-13.md, briefs/WRITE-13C.md
// and the design in briefs/out/car-interior-design.md. Every line added, moved or changed in this round is marked CAR-13W.)
//   - The driver's window is rolled down, and the window or the wagon gets Dad in: the inside of the wagon is a scene of
//     its own (egypt-car), and the picture is his own view from the driver's seat. Nobody is drawn in it, and every line
//     in it is his. His two looks in at the window (egypt.inside.look, .look2) are said outside, by the river.
//   - No exclamation mark, no Scripture, no prayer and no year: his three prayers are where they were, and none is in the
//     car. "Nothing marked B.C." names no year.
//   - Nothing in the car speaks of light, of mirrors as tools, of the shade, of cold drinks or of sunglasses, and none of
//     those is in the car: they are the later puzzles'. The one line that names a mirror's use, the rearview mirror's
//     "glued" (egypt.car.rearview.glued), is said only once he knows what light does ("egypt.knowsLight"), when the hint
//     itself already says "The car has a mirror it isn't using."
//   - The tender touch is the visor: his youngest's drawing of the five of them, the wagon and the General on the roof,
//     and Dad talking to the three at home. It is a second drawing, which she made for the car: the first hangs on her
//     wall at home (home.drawings.*). The joke is the slushie, which pays off the first minute of the game (intro.3, .4).
//   - The car states no history and no date. It leans only on the game's own story: the slushie and "making good time"
//     (the opening), the other half of the gum (the Son's item.gum.look: the car plants it, Rome pays it), the drawing,
//     the musical taped off the radio and "a little flat" (Mom's, at home and in Nevada), the manuals read to the middle,
//     the two hundred thousand miles (the author's egypt.wagon.look), and the children's ages.
//   - The glovebox holds the map and the ketchup packets and nothing else, so that the author's "Nothing left in there but
//     ketchup packets. I'm saving those." stays true: the manual is in the door pocket now, and the mints are gone. His
//     egypt.wagon.use and egypt.wagon.empty are said inside now, word for word, and egypt.wagon.try, word for word, at the
//     key.
//
// THE DIALOGUE PASS (round seventeen, 16 October: the author's "make the dialogue more realistic, some of the faith-based
// comments seem forced, make the dialogue fun"; S/briefs/PASS-17.md and section 1 of briefs/out/office-hq-design.md).
// PASS-17E: twenty-five lines of this act are new words under their old ids, each marked "PASS-17E" with why; none was
// added or dropped, no clue or hint was lost, and the author's lines marked "kept" are as they were. Fifteen of them are
// faith lines (and one more of Lot's story): no reference is said aloud any more (seven said one), three Bible facts
// tacked on to a look became his own jokes, and Lot tells his story a little more as a man talks than as a book reads.
// docs/PUZZLES-egypt.md, "Round seventeen", has each one, before and after, so that any of them can be put back.
//
// THE SECOND DIALOGUE PASS (round nineteen, 25 October: the author's "Stiff, written-sounding", "Too long", "Jokes fall
// flat"; S/briefs/PASS-19.md). PASS-19E: 283 lines of this act have new words under their old ids, 14 were folded into
// their neighbours and taken out with their uses, and one was added (egypt.got.reed.b); S/work-19-passE/changes.json and
// ready.md have each, before and after, with why. A box is one idea and at most 80 characters, the punch word last and
// nothing after it; no filler openers; one capital word a box, and the goldsmith mishears less often; never more than
// two of Lot's boxes before Dad speaks; the people of the time still never shorten a word, and still no exclamation
// mark. Every clue word is kept, and every line marked "kept" (and the King James words) is exactly as it was.

export const lines = {
  // ================= egypt-crash: where the wagon came down =================

  // ---------- arrival ----------
  "egypt.arrive.1": ["dad", "Well. That's one expressway I won't be taking again."],                                                              // kept (the author's new first line, 10 October: the first line of play answers the movie's shortcut)
  "egypt.arrive.2": ["dad", "Buddy? ... Buddy?"],                                                                                    // kept
  "egypt.arrive.3": ["dad", "He was in the passenger seat a minute ago. Or a thousand years from now. I'm still working out the tenses."],   // kept
  "egypt.arrive.4": ["dad", "Sneaker prints. Small ones, wandering up that track as if they owned it."],
  "egypt.arrive.5": ["dad", "Off to see the biggest thing in sight. He gets that from me. I can't even be cross about it."],
  "egypt.arrive.pray.1": ["dad", "Lord. I took a shortcut. You know that. You were in the car."],
  "egypt.arrive.pray.2": ["dad", "You know where he is. I don't know when I am. Keep him. In Jesus' name, amen."],

  // ---------- the river, the bank, the far end of the track ----------
  "egypt.river.look": ["dad", "Either that's the Nile or a very committed car wash."],                                               // kept
  "egypt.river.look2": ["dad", "No hoses, no brushes. I'm calling it: the Nile."],
  "egypt.river.use": ["dad", "Not in these. They're my good sandals. Also my only sandals."],
  "egypt.river.bible.1": ["dad", "The Egypt of my Bible. Abraham, Joseph, Moses: any one of them could be just round that bend."],
  "egypt.river.bible.4": ["dad", "Or not for a thousand years. I never could keep the dates straight. I always skipped to the maps."],
  // (once Lot has told him who he is, he knows: Abram is here, and Joseph and Moses are still to come)
  "egypt.river.after.1": ["dad", "Abram's in Egypt this very week. Joseph and Moses are still a long way down the road."],
  "egypt.river.after.3": ["dad", "Turns out I never needed the dates in the margin. I needed his nephew, praying under a palm."],
  "egypt.reeds.look": ["dad", "Reeds. Nature's ballpoint."],                                                                         // kept
  "egypt.reeds.take": ["dad", "One reed. I'll bring it back. That's a lie. I never bring pens back."],                               // kept
  "egypt.reeds.again": ["dad", "One is plenty. I'm not opening a stationery shop."],                                                 // kept
  "egypt.reeds.basket.1": ["dad", "Moses' basket. '...and she laid it in the flags by the river's brink.'"],  // PASS-17E: reference aloud
  "egypt.reeds.basket.2": ["dad", "Flags are reeds, so naturally I looked. No basket. Either I'm early, or I'm late."],
  "egypt.reeds.basket.3": ["dad", "Flags are reeds, so naturally I looked. No basket. I'm early. I'm very early."],                               // (after the news)  PASS-17E: running gag ("I'm early, or I'm late" settled in two words; Little Sister's "Daddy's EARLY" in Act Four)
  "egypt.boat.look": ["dad", "A boat riding low with white stone, coming across the water. Even the rocks here get a ferry."],
  "egypt.boat.look2": ["dad", "A whole quarry, ferried across a river one boatload at a time. And I complain about carrying in the groceries."],
  "egypt.palms.look": ["dad", "Palm trees: the only shade for miles, and every inch of it exactly where I'm not standing."],
  "egypt.pyramids.look": ["dad", "They look brand new. Somebody kept the receipt."],                                                 // kept
  "egypt.pyramids.look2": ["dad", "It's farther than it looks. Everything is. I learned that crossing a mall parking lot."],
  "egypt.pyramids.look3": ["dad", "I wonder who else has looked at those from right here. Abraham, maybe. Or maybe not yet."],  // PASS-17E: shorter; a wonder, not a lesson ("my Bible" four times in a minute)
  "egypt.pyramids.look3b": ["dad", "Abram could've stood right here and looked at those. This week, of all the weeks."],     // (once Lot has told him)
  "egypt.footprints.look": ["dad", "Small prints, and not two of them in a straight line. That's my boy, all right."],
  "egypt.footprints.use": ["dad", "Up the track, toward the pyramid. Where he goes, I go. It's in the job description."],
  "egypt.chicken.footprints": ["dad", "She knows those sneakers. She's been stepped on by them more than once, and she bears no grudge."],
  "egypt.track.look": ["dad", "Straight up to the pyramid. I didn't ask anybody. I want that noted."],
  "egypt.block.look": ["dad", "A broken sledge. Somebody's having a worse day than me. It helps."],
  "egypt.block.use": ["dad", "It's the size of a dishwasher, and it feels the same about moving."],
  "egypt.donkey.look": ["dad", "A donkey. Low mileage, runs on hay, and has never once needed a jump."],
  "egypt.donkey.look2": ["dad", "He's been drinking since I landed. Wherever he's headed, he won't get there thirsty."],
  "egypt.donkey.use": ["dad", "He let me scratch his ears. Friendliest welcome I've had since Nevada."],
  "egypt.donkey.sunglasses": ["dad", "He gave me the look a car salesman gives a man in sunglasses. I put them away."],

  // ---------- the wagon, and what is still in it ----------
  "egypt.wagon.look": ["dad", "Two hundred thousand miles and she still runs. Not right now. But in general."],                      // kept
  "egypt.hood.look": ["dad", "She's just thinking it over."],
  "egypt.hood.look2": ["dad", "Steam. It's her way of saying 'not now'. The lawnmower says it too, usually on a Saturday."],
  "egypt.hood.use": ["dad", "I don't open the hood. We have an understanding."],
  "egypt.hood.flashlight": ["dad", "Sand. More sand. That's the full report."],
  "egypt.hood.rootbeer": ["dad", "She doesn't take root beer. I'm fairly sure."],
  // CAR-13W: the driver's window is rolled down (round thirteen), and through it he looks into the wagon; a click on it,
  // or on the wagon, gets him in (egypt-car, below). Said outside, at the window: before he has the map, and after it.
  "egypt.inside.look": ["dad", "Window's down. My map's in the glovebox, being wrong in private."],
  "egypt.inside.look2": ["dad", "Window's down to let the heat out. The heat has other plans."],
  // CAR-13W: the key (egypt.wagon.try) and the glovebox (egypt.glovebox.look, egypt.wagon.use, egypt.wagon.empty) are
  // inside the wagon now, and their lines with them: see egypt-car, below.
  "egypt.mirror.look": ["dad", "It's shown me every wrong turn I ever made, only smaller."],
  // the first time he comes up to the car, the low sun off the door mirror catches him in the eye (once: the mirror's hint)
  "egypt.mirror.dazzle": ["dad", "Ow. Sun off the mirror. Objects in mirror are brighter than they appear."],
  "egypt.mirror.take": ["dad", "One twist and it's off. It's been one twist from off since March."],
  "egypt.car.noreason": ["dad", "I don't take my car apart without a reason. Even a bad one."],
  "egypt.suitcase.look": ["dad", "I sat on it to get it shut. It hasn't forgiven me."],
  "egypt.suitcase.open": ["dad", "Six more loud shirts. The store saw me coming."],
  "egypt.suitcase.take": ["dad", "Sunglasses, on six more shirts. Every one louder than this."],
  // under the shirts: General Feathers, and a note in crayon (the close-up shows it: egypt-crash.js, NOTE)
  "egypt.suitcase.general.1": ["dad", "And under the shirts, General Feathers. With orders. In crayon."],
  "egypt.suitcase.general.2": ["dad", "My youngest sent her to watch me. She has concerns about my driving."],
  "egypt.suitcase.general.3": ["dad", "Welcome aboard, General. The boy's gone ahead."],
  "egypt.suitcase.again": ["dad", "Six shirts, for a week of barbecues. I got one pyramid."],
  "egypt.trunk.look": ["dad", "Everything I might need, packed under everything I won't."],
  "egypt.trunk.flashlight": ["dad", "A flashlight, packed in case of a flat. Not in case of Egypt."],
  "egypt.trunk.rest": ["dad", "Lawn chair, jumper cables, windshield shade. Nothing I need. Yet."],  // PASS-17E: funnier (and the shade is planted)
  "egypt.trunk.shade": ["dad", "The windshield shade. Ten years keeping sun out. Time it switched sides."],
  "egypt.trunk.after": ["dad", "Lawn chair, jumper cables. Much longer and I'm getting the chair out."],
  "egypt.trunk.cables": ["dad", "Jumper cables. The nearest battery's nearly four thousand years up the road."],
  "egypt.trunk.chair": ["dad", "A lawn chair. For when I've earned a sit-down, and I haven't. Not while he's out there."],
  "egypt.cooler.look": ["dad", "Root beer, ice, and one sandwich I'm not ready to talk about."],
  "egypt.cooler.take": ["dad", "Still cold. The ice held. Something on this trip had to."],
  "egypt.cooler.have": ["dad", "One at a time. It's a cooler, not a bar."],
  "egypt.cooler.more": ["dad", "One more. The rest are for the drive home. I'm an optimist."],

  // ---------- Lot, Abram's nephew: under the palm, praying, while his donkey drinks ----------
  // Before he has said who he is he is a stranger on the screen ("herdsman"); after it, "Lot". He tells who he is as
  // his own memory, in his own words, from Genesis 11:27 to 13:5 and nothing beyond it (docs/PUZZLES-egypt.md has
  // each statement and its verse). Dad's understanding lands here, the first time Lot has told it.
  "egypt.lot.look": ["dad", "A man at his prayers in the shade. My car fell out of the sky beside him, and he never lost his place."],
  "egypt.lot.look2": ["dad", "Lot, Abram's nephew, back at his prayers. One of them was for my boy. I won't forget that."],                          // (after he has prayed for the boy)
  "egypt.lot.hello": ["lot", "You came down out of the sky in a red box. No ox. No donkey. Nothing."],
  "egypt.scribe.hello2": ["dad", "It has a hundred and forty horses. They're resting."],                                             // kept (Lot names the ox and the donkey that were not pulling, so that the horses answer him: round twelve)
  "egypt.lot.hello2": ["lot", "Let them rest. Since the LORD called my uncle, I ask nobody how they got here."],   // FINAL-19: REVIEW-19's patch
  "egypt.ask.boy": ["dad", "Have you seen a boy? About this tall, asks a lot of questions?"],                                        // kept
  "egypt.lot.boy.1": ["lot", "A small one in strange sandals went up the track, asking for the 'wy-fy'."],
  "egypt.lot.boy.2": ["lot", "If the Egyptians have one, it is at their Horizon. They keep everything there."],
  "egypt.lot.boy.3": ["dad", "That's my boy. He asks that in every house we walk into. It's how he says hello."],
  "egypt.lot.ask.horizon": ["dad", "And this Horizon everybody's so keen on: what is it, exactly?"],
  "egypt.lot.horizon.1": ["lot", "The great white one. Their king's tomb: the Horizon of Khufu."],
  "egypt.lot.horizon.2": ["dad", "A pyramid called the Horizon. Finally, a horizon I can actually walk to."],
  "egypt.lot.ask.news": ["dad", "Anything I should know before I go up? This isn't asking for directions."],  // PASS-17E: running gag (he has never asked for directions)
  "egypt.lot.news.1": ["lot", "Those who come for water say a wall in the Horizon has begun to hum."],
  "egypt.lot.news.2": ["lot", "Their scribe's pen has split. He can write nobody onto his list."],
  "egypt.lot.news.3": ["dad", "A humming wall and a paperwork problem. I've had Mondays like that."],
  "egypt.lot.news.4": ["lot", "Since the hum began, the geese on the bank all face the Horizon."],
  // who he is: his father, his grandfather, the call, the promise, Canaan, the famine (Genesis 11:27-32, 12:1-10, 13:5)
  "egypt.lot.ask.who": ["dad", "Who are you, if you don't mind my asking?"],
  "egypt.lot.who.1": ["lot", "Lot, son of Haran. My father died in Ur of the Chaldees, before his own father."],
  "egypt.lot.who.2": ["lot", "Grandfather Terah took my uncle Abram, Sarai and me out of Ur. He died at Haran."],
  "egypt.lot.who.3": ["dad", "Ur of the Chaldees. I've only ever seen that on the maps in the back of my Bible."],
  "egypt.lot.who.4": ["lot", "The LORD called my uncle to a land He would show him. At seventy-five, he went."],  // PASS-17E: shorter; a man telling it, not reading it out
  "egypt.lot.who.8": ["lot", "He built altars to the LORD in Canaan. Then famine brought us down into Egypt."],  // PASS-17E: shorter (the act's longest line)
  // and Dad understands, slowly and then all at once: he is standing in Genesis 12 (an aside, looking out over the river)
  "egypt.abram.1": ["dad", "Abram, not Abraham yet. Egypt. A famine. ...I'm standing in Genesis."],  // PASS-17E: reference aloud (the chapter number); the penny dropping, as it drops
  "egypt.abram.3": ["dad", "God promised every family on earth a blessing through him. Mine included. I'm counting on it."],  // PASS-17E: reference aloud (the design's own sample); FINAL-19: REVIEW-19's patch
  // this week, told briefly and judging nobody (Genesis 12:14-20)
  "egypt.lot.ask.week": ["dad", "You look like a man waiting for a ride."],
  "egypt.lot.week.1": ["lot", "The king took my uncle's wife into his house, and was good to him for her sake."],
  "egypt.lot.week.4": ["lot", "Then the LORD struck his house with plagues. Today his men send us out of Egypt."],
  "egypt.lot.week.5": ["dad", "I'd heard something along those lines. From a long way off."],
  "egypt.lot.week.6": ["lot", "Then the story has gone farther than we have."],
  // parting, the first time after he has told it: two men and two sons, and Lot prays for the boy (his own prayer, not Dad's)
  "egypt.lot.ask.bye": ["dad", "I've got a hill to climb and a boy to ground."],
  "egypt.lot.son.1": ["lot", "My uncle has no son. And the LORD has promised him a great nation."],
  "egypt.lot.son.2": ["dad", "A nation promised, and not one son yet. I've got the one, and I've gone and mislaid him."],
  "egypt.lot.son.3": ["lot", "Then you are both waiting on a son. Yours is already walking."],
  "egypt.abram.4": ["dad", "I'd give a lot to go and shake your uncle's hand."],
  "egypt.abram.5": ["dad", "But I've got a boy to find."],
  "egypt.lot.son.4": ["lot", "Then go and find him. But first, let me ask for him."],
  "egypt.lot.prayer": ["lot", "LORD, the God of my father's brother Abram, keep the boy until his father comes."],
  "egypt.lot.amen": ["dad", "Amen."],
  "egypt.lot.thanks": ["dad", "Thank you. I asked Him the same when I landed. It's good to hear another man ask it."],
  "egypt.lot.bye": ["lot", "Go in peace. Everything up there has already gone wrong. You cannot be late."],
  // things offered to him
  "egypt.lot.rootbeer.1": ["dad", "Something cold? On the house. Well, on the car."],
  "egypt.lot.rootbeer.2": ["lot", "It hisses. Where I come from, a man leaves a hissing thing alone."],
  "egypt.lot.map.1": ["lot", "Where is the river on this?"],
  "egypt.lot.map.2": ["dad", "There isn't one. It's Nevada."],
  "egypt.lot.map.3": ["lot", "A land with no river. Then I will pray that it has wells."],
  "egypt.lot.chicken": ["lot", "I would not know whether to shear her, milk her, or follow her."],

  // ================= egypt-car: inside the wagon =================
  // CAR-13W: new in round thirteen. Dad's own view from the driver's seat: nobody is drawn here, and every line is his.
  // The ids, the words and when each is said are the design's (briefs/out/car-interior-design.md, section 4).

  // ---------- getting in ----------
  "egypt.car.arrive": ["dad", "Hot as a skillet. Still the only seat in Egypt that fits me."],                // (the first time only)

  // ---------- the glovebox: the road map (puzzle #1) ----------
  // CAR-13W: new words, and said inside now (the glovebox, shut). It said "The glovebox. Home of the map, the manual, and
  // something that used to be mints." The manual has moved to the door pocket and the mints are gone, so that the
  // author's "Nothing left in there but ketchup packets. I'm saving those." stays true.
  "egypt.glovebox.look": ["dad", "The glovebox. The map's in there, with a few things I'm saving."],
  // CAR-13W: the author's two, moved here word for word with their ids: said as the glovebox drops open and the map is
  // his, and then whenever he looks in.
  "egypt.wagon.use": ["dad", "There's a road map in the glovebox. Three states, zero centuries."],                                   // kept
  "egypt.wagon.empty": ["dad", "Nothing left in there but ketchup packets. I'm saving those."],                                      // kept
  "egypt.car.glovebox.map": ["dad", "It's never gone back in the way it came out. Not starting now."],                           // (the map, tried on it)

  // ---------- the windshield, the rearview mirror, the air freshener ----------
  "egypt.car.windshield.look": ["dad", "Sand. She parked nose first. I've parked worse."],                      // (the two looks, in turn)
  "egypt.car.windshield.look2": ["dad", "A river and no traffic. Best parking space I've ever found."],
  "egypt.car.windshield.use": ["dad", "I wiped the glass. The sand's on the other side. It always is."],
  "egypt.car.rearview.look": ["dad", "All sky back there. She's standing on her nose."],
  "egypt.car.rearview.use": ["dad", "Tipped it down. Sky. Tipped it up. More sky. I'm leaving it."],                             // (before he knows what light does)
  "egypt.car.rearview.glued": ["dad", "Glued to the windshield. The door one's the one that comes off."],                     // (after it: "egypt.knowsLight")
  "egypt.car.freshener.look": ["dad", "'New Car Smell.' She's older than two of my kids. Nobody's fooled."],

  // ---------- the sun visor: his youngest's drawing ----------
  "egypt.car.visor.look": ["dad", "My youngest tucked something behind the visor. Not while I'm driving."],      // (up)
  "egypt.car.visor.down.1": ["dad", "Her drawing. The five of us, the wagon, and the General on the roof."],                      // (pulled down: once)
  "egypt.car.visor.down.2": ["dad", "She drew me the biggest. Hang on, you three. We're making good time."],
  "egypt.car.visor.look2": ["dad", "The registration, paid through next spring. I'll explain the gap."],                      // (down)

  // ---------- the wheel, the gauges, the horn, the gear lever, the key ----------
  "egypt.car.wheel.look": ["dad", "Both hands on the wheel, the whole way. On the record."],
  "egypt.car.wheel.use": ["dad", "The front end's in a dune. It didn't get the message."],
  "egypt.car.gauges.look": ["dad", "Two hundred thousand and six miles. The last one was a long one."],
  "egypt.car.gauges.use": ["dad", "Tapped the gauge. Still in the red. So it isn't the gauge."],
  "egypt.car.horn.look": ["dad", "The horn. It's a little flat. My wife says the same about me."],
  "egypt.car.horn.use": ["dad", "I don't raise my voice. That's what the horn is for."],                                             // (the first honk, after the horn)
  // CAR-13W: the design has "There's a man praying out there." Nothing in the car speaks of prayer (the head, above), and
  // the act's check holds every line of Dad's that does to the list of lines written for the faith: so, "sitting quietly".
  "egypt.car.horn.again": ["dad", "Once is hello. Twice is rude. A man's sitting quietly out there."],                         // (every honk after: no sound)
  "egypt.car.gears.look": ["dad", "P, R, N, D and L. Nothing marked B.C. I'd have noticed."],
  "egypt.car.gears.use": ["dad", "It's staying in Park. Park has never once let me down."],
  "egypt.car.key.look": ["dad", "The key's in. Car thieves haven't been invented."],
  // CAR-13W: moved here word for word, with its id, from the wagon outside (its "Start"): said after the starter.
  "egypt.wagon.try": ["dad", "She made the noise she makes when I bring up the transmission."],

  // ---------- the radio, the slushie, his seat ----------
  "egypt.car.radio.look": ["dad", "A musical my wife taped off the radio, traffic report and all."],
  "egypt.car.radio.use": ["dad", "Static, end to end. It's a quiet century."],                             // (after the hiss)
  "egypt.car.slushie.look": ["dad", "He said the sky did the slushie thing. I said weather. I stand by weather."],
  "egypt.car.slushie.use": ["dad", "Leaving it for him. He's never finished one. He likes to be asked."],
  "egypt.car.slushie.rootbeer": ["dad", "That holder's his. Mine rides in my shorts."],                                              // (the root beer, tried on it)
  "egypt.car.seat.look": ["dad", "Six wrappers, one sock, no boy. He travels light and leaves heavy."],
  "egypt.car.seat.use": ["dad", "Half a pack of gum, stuck under his seat. A problem for later."],              // (the gum is not taken)
  "egypt.car.seat.chicken": ["dad", "The General's in his seat. She says it's sticky. She's right."],                            // (General Feathers, tried on it)

  // ---------- the owner's manual, the door ----------
  "egypt.car.manual.look": ["dad", "The owner's manual. Read to the middle, like all my manuals."],
  "egypt.car.manual.use": ["dad", "I've read the first half. Time travel must be in the second."],
  "egypt.car.door.look": ["dad", "Out there, Egypt. In here, the one thing in Egypt I understand."],

  // ================= egypt-site: the foot of the pyramid =================

  // ---------- arrival, and the place ----------
  "egypt.site.arrive.1": ["dad", "That's what they look like before the gift shop."],
  "egypt.site.arrive.2": ["overseer", "Why is nobody pulling? Why is every man on this site STANDING?"],
  "egypt.site.arrive.3": ["dad", "And that'll be the manager."],
  "egypt.site.pyramid.look": ["dad", "Smooth white stone, all the way up. Somebody waxed a mountain."],
  "egypt.site.pyramid.look2": ["dad", "Still in scaffolding. Nearly done. I know 'nearly done'. I own a deck."],
  "egypt.site.small.look": ["dad", "Three small ones around the side. Everybody starts somewhere."],
  "egypt.site.entrance.look": ["dad", "A doorway up the steps, under two leaning slabs. No welcome mat."],
  "egypt.site.entrance.look2": ["dad", "The way in. A wall's humming up there. My son went to say hello."],  // PASS-17E: truer (the old line was a puzzle of its own; "It's how he says hello" comes round once more)
  "egypt.site.stair.look": ["dad", "Mud brick steps to the door. The inspector will have notes."],
  "egypt.site.desk.look": ["dad", "Bread and beer for wages. I've had jobs that paid worse and tasted worse."],
  "egypt.site.desk.look2": ["dad", "Papyrus, and tallies on bits of pot. All it needs is a dead plant."],
  "egypt.site.sledge.look": ["dad", "A white block, a wooden sled. The invention of the bad back."],
  "egypt.site.sledge.look2": ["dad", "Wet sand ahead of the runners, raked like a ballfield before a game. They know something I don't."],
  "egypt.site.sledge.use": ["dad", "I pulled. It didn't. We've agreed to see other people."],
  "egypt.site.blocks.look": ["dad", "Copper chisels, wooden mallets, a plumb line. And it's squarer than my garage."],
  "egypt.site.blocks.use": ["dad", "Another man's chisels? I've lent a ladder. I know how that ends."],
  // (a second look at the masons' work: the stone itself. Said once.)
  "egypt.site.shells.1": ["dad", "Seashells in the stone, in the desert. The Flood covered every hill."],
  "egypt.site.mizraim": ["dad", "Noah's grandson settled Egypt. Technically, everybody here's my cousin."],  // PASS-17E: reference aloud; a Bible fact tacked on, turned into his own joke
  "egypt.site.sunspot.look": ["dad", "Full sun, and nobody standing in it. They have more sense."],
  "egypt.site.sunspot.look2": ["dad", "Full sun, clear line to the door. If light were a golf ball, this is the tee."],
  "egypt.site.sunspot.use": ["dad", "Same sun as at home, with the dial turned all the way up."],
  "egypt.site.track.look": ["dad", "Back to the river, the car, and the only cold drinks in Egypt."],
  "egypt.site.rope.look": ["dad", "Rope thick as my wrist, dropped. I've left a hose out for less."],
  "egypt.site.scaffold.look": ["dad", "Poles and rope, four stories up. I get dizzy cleaning the gutters."],
  "egypt.site.masons.look": ["dad", "Masons on hanging planks. Nothing under them but Egypt."],
  "egypt.site.yard.look": ["dad", "Blocks waiting their turn. The school pickup line, only heavier."],
  "egypt.site.water.look": ["dad", "Water jars, every one carried up from the river. I get winded carrying a cooler to the car."],
  "egypt.site.bricks.look": ["dad", "Mud bricks, drying in rows. Somebody here invented the ice cube tray and never got the credit."],
  "egypt.site.bricks.use.1": ["dad", "Bricks for Pharaoh. I know this one: the Israelites made them."],
  "egypt.site.bricks.use.3": ["dad", "That's stone. The Bible's bricks were for 'treasure cities, Pithom and Raamses.'"],  // PASS-17E: reference aloud; a man working it out, not reading it out
  "egypt.site.bricks.use.4": ["dad", "Not one word about building a pyramid. Wrong since Sunday school."],  // PASS-17E: shorter (the point made once)

  // ---------- the scribe: a pen, a sheet, a pass ----------
  "egypt.scribe.look": ["dad", "He's been staring at a blank sheet for a while. I know writer's block when I see it."],              // kept
  "egypt.scribe.look2": ["dad", "He's writing again, fast, like a man catching up on a whole lost morning."],
  "egypt.scribe.meet.1": ["scribe", "Do not tell me your name. Without a pen it is only a noise."],
  "egypt.scribe.meet.2": ["dad", "Pen trouble?"],
  "egypt.scribe.meet.3": ["scribe", "It split at dawn. Since then nothing has happened. Not officially."],
  "egypt.scribe.boy.1": ["scribe", "There is no boy on my list. If he is not on the list, then he did not go in. That is what a list is for."],
  "egypt.scribe.boy.2": ["dad", "He's not on a lot of lists. It's never once stopped him going in."],
  "egypt.scribe.ask.list": ["dad", "How does a man get onto that list of yours?"],
  "egypt.scribe.list.nopen": ["scribe", "I write him onto it. With a pen. You see the difficulty."],
  "egypt.scribe.list.nosheet": ["scribe", "I write him a pass. My last clean sheet is for the grain account."],
  "egypt.scribe.list.done": ["scribe", "You are on it. The only thing written anywhere today. Short, but tidy."],
  "egypt.ask.bye": ["dad", "I'll let you get back to your sheet."],                                                                  // kept
  "egypt.ans.bye": ["scribe", "It is not going anywhere. Neither am I."],                                                            // kept
  "egypt.give.reed": ["dad", "Here. It's a pen. Some assembly required."],                                                           // kept
  "egypt.got.reed": ["scribe", "A good reed. You have the eye of a scribe and the clothes of a market stall."],                      // kept
  "egypt.got.reed.b": ["dad", "I'll take the first half. The shirt can speak for itself."],   // PASS-19E: new box, said right after egypt.got.reed (a Dad reaction between the scribe's boxes (the run of four broken))
  "egypt.scribe.rush": ["scribe", "A rush is the proper pen. A man without one cannot be particular."],
  "egypt.scribe.supplier": ["scribe", "You supply reeds, so you go on the list. My last sheet is for the grain account."],
  "egypt.give.map": ["dad", "Draw on this. It's a map. It's already wrong, you can't make it worse."],                               // kept
  "egypt.got.map.nopen": ["scribe", "A fine sheet. I have nothing to mark it with."],                                                // kept
  "egypt.scribe.pass.1": ["scribe", "'One supplier of reeds. Foreign. Loud about the shoulders.' Now you exist."],
  "egypt.scribe.pass.2": ["scribe", "Show the guard my side of the sheet. He knows my hand."],
  "egypt.pass.got": ["dad", "A hall pass. Thirty years out of school, and finally."],
  "egypt.scribe.rootbeer": ["scribe", "Beer made of roots? The brewers would never forgive me."],
  "egypt.scribe.shade": ["scribe", "I hold a pen. It is all I hold. Ask a man with idle arms. This site is full of them."],
  "egypt.scribe.pass": ["scribe", "I wrote it. I do not need to read it. That is the point of writing."],
  "egypt.scribe.chicken": ["scribe", "There is no sign for that bird. So, officially, she is not here."],

  // ---------- the scribe's news: the same week from the Egyptian side (Genesis 12:10-20, told from outside, as gossip) ----------
  // Offered once Lot has told Dad who he is: Dad hears it knowing more than the scribe does.
  "egypt.scribe.ask.news": ["dad", "Any news? I've been out of touch. Badly out of touch."],
  "egypt.scribe.news.1": ["scribe", "Only grain. The famine has driven the desert herdsmen down to us, and I count every basket they eat."],
  "egypt.scribe.news.2": ["scribe", "One of them is rich. Abram, by name. He brought his sister."],
  "egypt.scribe.news.3": ["dad", "Abram. I've met his nephew."],
  "egypt.scribe.news.4": ["scribe", "She is very fair. She was taken into the Great House."],
  "egypt.scribe.news.5": ["dad", "The Great House. That's what 'Pharaoh' means. I read that in a footnote."],
  "egypt.scribe.news.6": ["scribe", "Sheep, oxen, asses, camels. The king's gifts, all through my accounts."],
  "egypt.scribe.news.7": ["scribe", "Then a sickness fell on the Great House. Now they say she is his WIFE."],
  "egypt.scribe.news.8": ["dad", "And the king's sending him away. Him, his wife, everything he owns."],
  "egypt.scribe.news.9": ["scribe", "Today, with the king's men. How do you know? It is written nowhere."],
  "egypt.scribe.news.10": ["dad", "Not yet."],
  "egypt.scribe.news.11": ["dad", "His nephew's by the river, praying. For my boy, among other things."],

  // ---------- the overseer: the schedule ----------
  "egypt.overseer.look": ["dad", "A big man with a schedule. I can't see the schedule. I can hear it."],
  "egypt.overseer.meet.1": ["overseer", "Nobody dresses like that for no reason. You must be the specialist."],
  "egypt.overseer.meet.2": ["dad", "Close. I'm the generalist nobody sent for."],
  "egypt.overseer.meet.3": ["overseer", "A wall inside has begun to hum. Inspect it and make it stop. Take all the time you need, so long as it is today."],
  "egypt.overseer.boy.1": ["overseer", "A boy? I have a whole gang not working. I cannot watch a boy not working too."],
  "egypt.overseer.ask.hum": ["dad", "Tell me about this humming wall."],
  "egypt.overseer.hum.1": ["overseer", "In the top chamber, since dawn. Not one man will carry so much as a basket past it."],
  "egypt.overseer.hum.2": ["overseer", "I told them a wall cannot hurt them. They said a wall cannot hum either."],
  "egypt.overseer.hum.3": ["dad", "They've got you there. I'd have said it was the wind."],  // PASS-17E: running gag (everything he cannot explain is the wind)
  "egypt.overseer.hum.4": ["overseer", "Twenty years I have built this. On time, every day of it. Until a wall began to HUM."],
  "egypt.overseer.ask.schedule": ["dad", "How's the schedule holding up?"],
  "egypt.overseer.sched.0a": ["overseer", "The haulers blame the wall, the scribe his pen. I blame them all. It saves time."],
  "egypt.overseer.sched.0b": ["overseer", "First get yourself onto the scribe's list. The guard at the stair turns back any man who is not."],
  "egypt.overseer.sched.1": ["overseer", "It still hums. Ask the lamp boy. He saw something in there, and he tells me nothing at all."],
  "egypt.overseer.sched.2": ["overseer", "A little sun in a hand? Then find a little sun. I have only the big one."],
  "egypt.overseer.sched.3": ["overseer", "The sunlight is out here, the wall in there. I did not plan for them to meet."],
  "egypt.overseer.sched.3b": ["overseer", "Unless you can bend the day around three corners, we are late."],
  "egypt.overseer.sched.3c": ["dad", "We're not late. We're making good time."],
  "egypt.overseer.sched.4": ["overseer", "Daylight in my pyramid. Not on the schedule. Is it helping?"],
  "egypt.overseer.sched.4b": ["dad", "Like a charm."],
  "egypt.overseer.sched.4c": ["overseer", "Then it was always on the schedule."],
  "egypt.overseer.ask.bye": ["dad", "I'll get right on it."],
  "egypt.overseer.bye": ["overseer", "Get on it faster."],
  "egypt.overseer.bark.light": ["overseer", "Does it still hum? No. Do not answer. I can see it in your face."],
  "egypt.overseer.bark.guard": ["overseer", "My guard is holding the sun. Put it on the schedule. Under 'strange'."],
  "egypt.overseer.bark.all": ["overseer", "DAYLIGHT in my pyramid. Nobody told me. Nobody tells me anything."],
  "egypt.overseer.map": ["overseer", "A plan? I have had the same plan for twenty years. It was going well."],
  "egypt.overseer.shade": ["overseer", "I oversee. If I stand there holding that, who oversees me holding it?"],
  "egypt.overseer.mirror": ["overseer", "Who is that tired man? ... Take it away."],
  "egypt.overseer.rootbeer": ["overseer", "Is it medicine? No? Then it cannot help me."],

  // ---------- the haulers: one speaks, one agrees, one eats ----------
  "egypt.haulers.look": ["dad", "One talks, one nods, one eats. It's a road crew."],
  "egypt.haulers.meet.1": ["hauler1", "Friends of Khufu. Best gang on the Horizon. We are resting."],
  "egypt.haulers.meet.2": ["hauler2", "We are resting very well."],
  "egypt.haulers.meet.3": ["hauler3", "Mm."],
  "egypt.haulers.boy.1": ["hauler1", "The small one. He asked to ride the sledge. We said no. He rode it."],
  "egypt.haulers.boy.2": ["hauler2", "He was no weight at all."],
  "egypt.haulers.boy.3": ["dad", "He's been told about riding things. Many times. It has never once helped."],
  "egypt.haulers.ask.break": ["dad", "Long break?"],
  "egypt.haulers.break.1": ["hauler1", "Since the wall began to hum. We do not pull stone toward a noise."],
  "egypt.haulers.break.2": ["hauler2", "Never toward a noise."],
  "egypt.haulers.ask.free": ["dad", "Hang in there, fellas. One day you'll all be free."],
  "egypt.haulers.free.1": ["hauler1", "Free? We are PAID. Bread and beer, every day."],
  "egypt.haulers.free.2": ["hauler2", "Every day."],
  "egypt.haulers.free.3": ["hauler3", "Mm-hm."],
  "egypt.haulers.free.4": ["dad", "Bread and beer, every day. I take it back. Are you hiring?"],
  "egypt.haulers.ask.sand": ["dad", "Why's the sand wet in front of the sledge?"],
  "egypt.haulers.sand.1": ["hauler1", "Wet the sand in front of the runners and one man pulls like two."],
  "egypt.haulers.sand.2": ["dad", "Noted. Next time we move the piano, I'm bringing a bucket."],  // PASS-17E: funnier (Mom's piano, at home)
  "egypt.haulers.ask.bye": ["dad", "Keep up the good work."],
  "egypt.haulers.bye.1": ["hauler1", "We are not doing any."],
  "egypt.haulers.bye.2": ["hauler3", "Mm."],
  "egypt.haulers.rootbeer.1": ["hauler1", "Is there beer in it?"],
  "egypt.haulers.rootbeer.2": ["dad", "No. It's root beer."],
  "egypt.haulers.rootbeer.3": ["hauler1", "Then it is a root. We are not paid in roots."],
  "egypt.haulers.rootbeer.4": ["hauler2", "Never in roots."],
  "egypt.haulers.shade.1": ["hauler1", "We pull. Holding is another trade."],
  "egypt.haulers.shade.2": ["hauler2", "A lesser trade."],

  // ---------- the guard: the stair, and then the shade ----------
  "egypt.guard.look": ["dad", "Tall, bored, sweating. Guarding a staircase from a patch of no shade."],
  "egypt.guard.look2": ["dad", "He's holding my shade up to the sun like he's surrendering. It's working."],
  "egypt.guard.stop": ["guard", "Nobody goes up these stairs who is not on the scribe's list. Nobody."],
  "egypt.guard.stop.2": ["dad", "I'm more of a walk-in."],
  "egypt.guard.stop.3": ["guard", "Then walk to the scribe, under the awning. He keeps the list. I only keep the stair."],
  "egypt.pass.show": ["dad", "One hall pass. Signed, sealed, slightly folded."],
  "egypt.guard.pass.1": ["guard", "The scribe's hand. I know it. It looks like geese in a quarrel."],
  "egypt.guard.pass.2": ["guard", "You are on the list. Go up. If it hums at you, do not bring it here."],
  "egypt.site.pray.1": ["dad", "Lord, it's dark in there, and it hums. That's exactly where he'd go."],
  "egypt.site.pray.2": ["dad", "Go in ahead of me. I'll follow. For once. Amen."],
  "egypt.guard.after": ["guard", "On the list. The stair is behind me. I am hot. That is all my news."],
  "egypt.shade.try.1": ["dad", "Sunlight, straight up into the doorway. Hold your applause."],  // PASS-17E: a wrong foot that pays (the next line: "And it stops when I let go.")
  "egypt.shade.try.2": ["dad", "It stops the moment I let go. I need a volunteer with steady arms and nothing to do."],
  "egypt.shade.ask": ["dad", "Could you hold this up in the sun? That's the whole job."],
  "egypt.guard.nohold": ["guard", "I guard. I do not hold."],
  "egypt.guard.cold": ["guard", "I would hold it for something cold. There is nothing cold. So I guard."],
  "egypt.rootbeer.give": ["dad", "Try this. It's cold. Around here that makes it treasure."],
  "egypt.guard.rootbeer": ["guard", "It bites the tongue. Like a small friendly snake."],
  "egypt.guard.owe": ["guard", "I owe you one holding. Of anything. Not heavy."],
  "egypt.guard.again": ["guard", "One snake is a friend. Two is a nest."],
  "egypt.shade.favor": ["dad", "About that holding you owe me."],
  "egypt.guard.take": ["guard", "The shining thing. In the sun. For how long?"],
  "egypt.shade.notlong": ["dad", "Not long."],
  "egypt.guard.notlong": ["guard", "The overseer says 'not long'. He has said it for twenty years."],
  "egypt.shade.lit": ["dad", "There it goes, up the stairs and in. Nobody asked it for a pass."],
  "egypt.beam.all": ["dad", "If my mirrors are where I left them, that's going all the way in."],
  "egypt.guard.arms.1": ["guard", "My arms have gone to sleep. They are the only part of me that has."],
  "egypt.guard.arms.2": ["guard", "How long is 'not long'? In your country. In days."],
  "egypt.guard.arms.3": ["guard", "When this is over I want another of the snake water. A big one."],
  "egypt.guard.full": ["guard", "Later. My hands are full of your sun."],
  "egypt.guard.sunglasses": ["guard", "It is darker. It is not cooler. I have been cheated."],
  "egypt.guard.map": ["guard", "Not the scribe's hand. A great many roads to nowhere I know."],
  "egypt.guard.chicken": ["guard", "She does not move. She has no arms. I do not see how she is in charge."],
  "egypt.guard.chicken.2": ["dad", "She delegates."],

  // ================= egypt-gallery: inside the pyramid =================

  // ---------- arrival, and the place ----------
  "egypt.gallery.arrive.1": ["dad", "Would you look at that."],
  "egypt.gallery.arrive.2": ["dad", "A hallway four stories high, uphill, by lamplight. And me in sandals."],
  "egypt.gallery.walls.look": ["dad", "Every row of stone steps in from the last. I get nervous hanging a shelf."],
  "egypt.gallery.walls.look2": ["dad", "The hull of a ship, parked upside down. On purpose. Out of rock."],
  "egypt.gallery.out.look": ["dad", "Daylight, down a very low passage. Watch your head. I didn't."],
  "egypt.gallery.low.look": ["dad", "A low passage. No lamps, no hum, no small footprints."],
  "egypt.gallery.low.use": ["dad", "I said 'Buddy?' in there. It said 'Buddy' back, twice. Nobody home."],
  "egypt.gallery.low.flashlight": ["dad", "It goes a long way into nothing. The batteries didn't enjoy it."],
  "egypt.gallery.top.look": ["dad", "A small doorway at the top. The lamps give up before it does."],
  "egypt.gallery.top.look2": ["dad", "The way to the chamber, the hum, and the one man who can't hear it."],
  "egypt.gallery.slot.look": ["dad", "Slots in the bench, all the way up. The builder liked slots."],
  "egypt.gallery.slot.beam": ["dad", "The sunbeam lands on plain stone and goes no farther. Stone makes a poor mirror. I checked."],
  "egypt.gallery.slot.set": ["dad", "My door mirror, wedged in a pyramid. Never had a view like this."],
  "egypt.gallery.step.look": ["dad", "A step at the top, flat as a table. Good place to stand something."],
  "egypt.gallery.step.set": ["dad", "The goldsmith's mirror, doing the one job he couldn't stand."],
  "egypt.gallery.marks.look": ["dad", "Red paint squiggles. The builders left themselves a note."],
  "egypt.gallery.marks.look2": ["dad", "I'd say it means 'this way up'. I guess with great confidence."],
  "egypt.gallery.jars.look": ["dad", "Oil jars. Every job has a supply closet, and a kid who runs it."],
  "egypt.gallery.jars.use": ["dad", "Not borrowing a lamp. The boy counts them. I can tell."],
  "egypt.gallery.ladder.look": ["dad", "A ladder. One thing in here I already know how to fall off."],
  "egypt.gallery.rope.look": ["dad", "Rope. The answer to everything here. Duct tape, with splinters."],
  "egypt.gallery.runner.look": ["dad", "A sled runner, worn flat. Whatever it hauled wasn't coming back down."],
  "egypt.gallery.chest.look": ["dad", "A chest, left halfway up. Somebody heard the hum and had an appointment."],
  "egypt.gallery.dinner.look": ["dad", "Bread and beer left on the bench. A whole day's pay. The hum is serious."],

  // ---------- the lamp boy: the only one who saw ----------
  "egypt.lampboy.look": ["dad", "A boy with a jar of oil, sitting as far from the top as he can."],
  "egypt.lampboy.meet.1": ["lampboy", "You wear strange sandals. So did the small one."],
  "egypt.lampboy.meet.2": ["dad", "He gets his feet from me."],
  "egypt.lampboy.saw.1": ["lampboy", "I saw him. I am the only one who saw."],
  "egypt.lampboy.saw.ask": ["dad", "Saw what?"],
  "egypt.lampboy.saw.2": ["lampboy", "A small one came, with a little sun in his hand."],
  "egypt.lampboy.saw.3": ["lampboy", "He pointed it at the wall and the wall opened like an eye and it took him."],
  "egypt.lampboy.saw.4": ["dad", "A little sun in his hand. That's the flashlight off his key ring."],
  "egypt.lampboy.saw.5a": ["dad", "It opens for a light, then. I've got a bigger one than his. It's in the trunk."],  // PASS-17E: clearer (where the flashlight is)
  "egypt.lampboy.saw.5b": ["dad", "It opens for a light, then. I've got a bigger one than his, right here in my pocket."],
  "egypt.lampboy.saw.5c": ["dad", "A light. I found that out the hard way. Those were good batteries."],
  "egypt.ask.door": ["dad", "What is the humming door?"],                                                                            // kept
  "egypt.lampboy.door.1": ["lampboy", "It is not a door. I know every door in the Horizon. I light them."],
  "egypt.lampboy.door.2": ["lampboy", "This opened where the masons put nothing."],
  "egypt.lampboy.door.3": ["dad", "That's the kind my family finds. Every time."],
  "egypt.lampboy.ask.lamps": ["dad", "You look after all these lamps yourself?"],
  "egypt.lampboy.lamps.1": ["lampboy", "Every lamp from here to the top. I fill them before they go hungry."],
  "egypt.lampboy.lamps.2": ["lampboy", "Not today. Today the top ones go hungry. I am not going up there."],
  "egypt.lampboy.lamps.3": ["dad", "Fair. I wouldn't either. I'm going to. But I wouldn't."],
  "egypt.lampboy.ask.bye": ["dad", "Keep the lights on."],
  "egypt.lampboy.bye": ["lampboy", "That is all I do."],
  "egypt.lampboy.sun": ["lampboy", "You brought the sun indoors. It needs no oil. I do not trust it."],
  "egypt.lampboy.flashlight": ["lampboy", "No. Keep your sun. I saw what the small one's did."],
  "egypt.lampboy.dead.1": ["dad", "Here. A little sun of your own. It's out of sun."],
  "egypt.lampboy.dead.2": ["lampboy", "It is a lamp. Lamps I understand. I will fill it."],
  "egypt.lampboy.dead.3": ["dad", "Don't. ... No, you know what? Go ahead. See what happens."],
  "egypt.lampboy.rootbeer": ["lampboy", "Sweet, and it bites. Do not tell the overseer. He would count it."],
  "egypt.lampboy.sunglasses": ["lampboy", "They put out every lamp at once. I work all day to do the opposite."],
  "egypt.lampboy.chicken": ["lampboy", "What does she eat? Everything I look after goes hungry, if I let it."],
  "egypt.lampboy.chicken.2": ["dad", "She's stuffed."],

  // ---------- the two mirrors, and the sunbeam as it grows ----------
  "egypt.foot.set": ["dad", "Wedged. That's not coming out. Nothing I wedge ever does."],
  "egypt.mirror.nothing": ["dad", "A mirror with nothing to reflect. I've worked with people like that."],
  "egypt.foot.lit": ["dad", "Up the ramp it goes. It stops dead at the top step. One more corner."],
  "egypt.foot.wrong": ["dad", "It won't wedge. It wants a flat place to stand, like the rest of us."],
  "egypt.top.early": ["dad", "A mirror at the top of a dark ramp. I'd only be decorating."],
  "egypt.top.set": ["dad", "Tilted at the little door. He kept it polished, I'll give him that."],
  "egypt.top.dark": ["dad", "It's reflecting the dark beautifully. The daylight hasn't got this far."],
  "egypt.top.lit": ["dad", "And in it goes. I'd better go and see what it's found."],
  "egypt.top.wrong": ["dad", "It won't stand up on its own. It was built to hang off a door."],
  "egypt.gallery.shade": ["dad", "No sun in here to bounce. All the sun's outside, standing around by the stairs."],
  "egypt.beam.in": ["dad", "My sunbeam: in through the passage, onto the bench, and stuck there, waiting for somebody to turn it."],
  "egypt.beam.up": ["dad", "Off my mirror and up the ramp. First right turn it's ever shown me."],  // PASS-17E: funnier (pays off "It's shown me every wrong turn I ever made")
  "egypt.relay.done": ["dad", "Passage, ramp, copper, top. That's the relay."],

  // ================= egypt-chamber: the burial chamber =================

  // ---------- arrival, and the place ----------
  "egypt.chamber.arrive.1": ["dad", "Gold. That is a great deal of gold."],
  "egypt.chamber.arrive.2": ["dad", "And a hum. Low, like a refrigerator in the next room. There is no next room."],
  "egypt.chamber.walls.look": ["dad", "Bare red stone. No picture, not one word. I was promised walls you could read."],
  "egypt.chamber.walls.look2": ["dad", "No curse over the door. I looked. I'm a little let down."],
  "egypt.chamber.door.look": ["dad", "The little door. We've met. I led with my forehead."],
  "egypt.chamber.treasure.look": ["dad", "Gold bed, chairs, a chair to be carried around in. A man after my own suitcase."],
  "egypt.chamber.treasure.look2": ["dad", "The bed has lion's feet. Mine has a phone book. Same idea."],
  "egypt.chamber.treasure.use": ["dad", "Not touching it. I can't get a hotel towel past my conscience."],
  "egypt.chamber.sarc.look": ["dad", "A stone box the size of a bathtub. No lid on, nobody in. Good."],
  "egypt.chamber.sarc.look2": ["dad", "Plain as a workbench. A man with a gold bed picked a very firm mattress."],
  "egypt.chamber.sarc.use": ["dad", "I'm not getting in. That's a one-way bath."],
  "egypt.chamber.lid.look": ["dad", "The lid, still roped. Nobody's in a hurry for it. Least of all the king."],
  "egypt.chamber.bench.look": ["dad", "Hammers, gold leaf. All you need for a chair too good to sit on."],
  "egypt.chamber.brazier.look": ["dad", "First grill I've seen all day, and not a thing on it."],
  "egypt.chamber.mirror.look": ["dad", "A copper hand mirror. Bright enough to shave in. I need a shave."],
  "egypt.chamber.mirror.use": ["dad", "Mind if I borrow that mirror?"],
  "egypt.goldsmith.mirror.no": ["goldsmith", "SORROW? Yes. That mirror. I check the gold in it, and it checks my face."],

  // ---------- the goldsmith: he mishears everything ----------
  "egypt.goldsmith.look": ["dad", "An old man gilding a box, squinting like it's a flashlight."],
  "egypt.goldsmith.look2": ["dad", "He's in my sunglasses, humming. The only thing in here that should be."],
  "egypt.goldsmith.meet.1": ["dad", "Hello there."],
  "egypt.goldsmith.meet.2": ["goldsmith", "A CHAIR? Yes, it is a chair. You have good eyes. I had those once."],
  "egypt.goldsmith.meet.3": ["dad", "This is going to be a long conversation."],
  "egypt.goldsmith.boy.1": ["goldsmith", "A TOY? I do not make toys. I make furniture for the king."],
  "egypt.goldsmith.boy.2": ["dad", "A BOY."],
  "egypt.goldsmith.boy.3": ["goldsmith", "Him. He stood where you stand. Then he did not. I thought he had gone home."],
  "egypt.goldsmith.ask.hum": ["dad", "Doesn't the humming bother you?"],
  "egypt.goldsmith.hum.1": ["goldsmith", "What hum?"],
  "egypt.goldsmith.hum.2": ["goldsmith", "I hear my hammer and nothing else. Fifty years of it. Very restful."],
  "egypt.goldsmith.ask.eyes": ["dad", "Are your eyes all right?"],
  "egypt.goldsmith.eyes.1": ["goldsmith", "Fifty years of gold, all of it shining at me. I have sore eyes."],
  "egypt.goldsmith.eyes.2": ["goldsmith", "I am tired of shining things. That mirror shines AND shows me my face."],
  "egypt.goldsmith.eyes.3": ["dad", "Tired eyes and too much glare. As it happens, I packed a thing for that."],
  "egypt.goldsmith.eyes.after": ["goldsmith", "NIGHT? Yes. I wear the night on my nose now. Nothing shines at me."],
  "egypt.goldsmith.ask.king": ["dad", "All this for one pharaoh?"],
  "egypt.goldsmith.king.1": ["goldsmith", "It is furniture. All of it for the king."],
  "egypt.goldsmith.king.2": ["dad", "The king. Right. One of those."],
  "egypt.goldsmith.ask.bye": ["dad", "Good talking to you."],
  "egypt.goldsmith.bye": ["goldsmith", "WALKING? You stood there the whole time. I saw you."],
  "egypt.goldsmith.trade.1": ["dad", "Try these. They turn the whole world down a notch."],
  "egypt.goldsmith.trade.3": ["goldsmith", "... That is kind. The whole world has gone the color of good beer."],
  "egypt.goldsmith.trade.4": ["goldsmith", "I never want to see a shining thing again. Take that mirror away."],
  "egypt.goldsmith.trade.5": ["dad", "A copper mirror for drugstore sunglasses. I came out ahead on a trade."],
  "egypt.goldsmith.trade.early": ["dad", "What would I do with a mirror? Never stopped me before."],
  "egypt.goldsmith.rootbeer": ["goldsmith", "Beer? ... No. Somebody has played a trick on beer."],
  "egypt.goldsmith.flashlight": ["goldsmith", "Put it OUT. I have enough bright in here."],
  "egypt.goldsmith.pass": ["goldsmith", "I am on the list. I have been on it for fifty years."],
  "egypt.goldsmith.carmirror": ["goldsmith", "ANOTHER mirror? Is this a joke? Who sent you?"],
  "egypt.goldsmith.copper": ["goldsmith", "No. NO. It is yours now. Let it shine at you."],
  "egypt.goldsmith.chicken": ["goldsmith", "A medal. Paper and ribbon. It does not shine. I would hire its maker."],

  // ---------- the wall that hums: the flashlight, and the rule ----------
  "egypt.hum.look": ["dad", "Bare wall, empty air. And a hum. Probably the wind."],
  "egypt.hum.look2": ["dad", "It only opens for light. My son found the one door in history with a dimmer."],
  "egypt.hum.use": ["dad", "I knocked on the air, like a man at a door from the wrong side. Nobody came."],
  "egypt.hum.use2": ["dad", "It wants light. A lot more than I carry in my pockets."],
  "egypt.hum.mirror": ["dad", "I showed the wall its own reflection. Nothing. It's not vain."],
  "egypt.hum.shade": ["dad", "Shading the door from the light is the opposite of the plan."],
  "egypt.chicken.hum": ["dad", "Held her up to the hum. Nothing rattles the General."],
  "egypt.flash.1": ["dad", "A little sun, the boy said. Let's try a medium one."],
  "egypt.flash.1b": ["dad", "Dark room, strange wall. This is what the flashlight's for."],
  "egypt.hole.look": ["dad", "A hole in the air the size of a dinner plate. I am not the size of a dinner plate."],            // kept
  "egypt.hole.small": ["dad", "It shrinks every time I get close. I have the same effect on waiters."],                             // kept
  "egypt.flash.dies": ["dad", "There go the batteries. They were meant to last till the motel."],
  "egypt.flash.son": ["dad", "A key-ring light, a hole in the air, and a boy who can't leave things alone."],
  "egypt.flash.rule.1": ["dad", "That's the trick. Light opens it. A little light, a little door."],
  "egypt.flash.rule.2": ["dad", "More light, more door. And a whole sun going to waste outside."],
  "egypt.flash.dead": ["dad", "Dead. I've shaken it. Shaking is all I know about batteries."],
  "egypt.goldsmith.flash": ["goldsmith", "Did you say something? Never mind. I would not have heard it."],

  // ---------- the gate ----------
  "egypt.gate.1": ["dad", "Here it comes. Around three corners and in, like it pays rent."],
  "egypt.hole.big": ["dad", "Now that's a door."],                                                                                   // kept
  "egypt.gate.gold": ["goldsmith", "Somebody has let the day in. Let it look. I am wearing the night."],
  "egypt.gate.thanks": ["dad", "Thank You, Lord. A shade, a root beer, two mirrors. I know who did the rest."],
  "egypt.gate.psalm.1": ["dad", "'For a thousand years in thy sight are but as yesterday when it is past, and as a watch in the night.'"],
  "egypt.gate.psalm.2": ["dad", "Moses wrote that. Show-off."],  // PASS-17E: reference aloud (the design's own sample, cut to fit both ways through)
  "egypt.gate.psalm.4": ["dad", "Either way, a thousand years is yesterday to Him. He knows where my boy is."],
  // (the same moment, when he has heard the scribe's news and knows when he is)
  "egypt.gate.psalm.3b": ["dad", "And he isn't even born yet. I've got the tenses worked out."],  // PASS-17E: shorter (Moses is named in the line before it now)
  "egypt.gate.psalm.4b": ["dad", "A thousand years is yesterday to Him. He knows right where my boy is."],
  "egypt.hole.go": ["dad", "Hold on, buddy. Dad's taking the next shortcut."],                                                       // kept
  "egypt.hole.wait": ["dad", "Not until I know where it comes out. I've made that mistake once today."],                             // kept

  // ================= General Feathers, shown to people =================
  // Five of them answer once each, in their own way (Lot, the scribe, the guard, the lamp boy, the goldsmith).
  // For everybody else, and for anybody who has met her already, Dad's stock reply.
  "egypt.chicken.show": ["dad", "This is General Feathers. She's in charge."],
  "egypt.chicken.stock": ["dad", "Nobody here's seen a bird like her. She's taking it well."],

  // ================= carried things =================
  "item.map.look": ["dad", "A road map. It folds eleven ways and none of them is the way it came."],                                 // kept
  "item.reed.look": ["dad", "A reed. The pen of the future, nearly four thousand years ago."],                                       // changed: was "three thousand"
  "item.pass.look": ["dad", "Supplier of reeds, on the back of Nevada. Loud about the shoulders."],
  "item.flashlight.look": ["dad", "A flashlight. Batteries from two vacations ago. So is my faith in them."],
  "item.rootbeer.look": ["dad", "Root beer. The only cold thing in the country, and it's in my shorts."],
  "item.shade.look": ["dad", "The windshield shade. Unlike the map, it folds the way it came."],
  "item.carmirror.look": ["dad", "The door mirror. Closer than it appears. I wish that worked on home."],
  "item.sunglasses.look": ["dad", "Sunglasses. Everything looks like late afternoon. My best time of day."],
  "item.coppermirror.look": ["dad", "Polished copper. I look like a penny with a beard."],
  "item.chicken.look": ["dad", "General Feathers. One eye, a medal for bravery. I do what she says."],

  // ================= hints: one for each puzzle, in Dad's own voice =================
  "hint.egypt.map": ["dad", "I should check what's still in the wagon."],                                                            // kept
  "hint.egypt.reed": ["dad", "The scribe's pen has split, and a pen here is a reed. A new one might be growing down by the river."],                          // changed: was "The scribe lost his pen."
  "hint.egypt.pen": ["dad", "I have a reed, and I know a man who needs a pen."],                                                     // kept
  "hint.egypt.mark": ["dad", "The scribe wants something to draw on. A map is mostly drawing."],                                     // kept (now the hint of "egypt.pass")
  "hint.egypt.inside": ["dad", "I'm on the list, with the pass to prove it. The guard at the stairs ought to see it before I go up."],
  "hint.egypt.witness": ["dad", "Somebody inside the pyramid saw what happened to my boy. A witness: the boy who tends the lamps."],
  "hint.egypt.flash": ["dad", "A little sun in his hand: that's a flashlight, and I packed one. Shine it on the wall that hums."],   // FINAL-19: REVIEW-19's patch
  "hint.egypt.shade": ["dad", "The windshield shade can throw sun into the doorway, but somebody has to hold it. The guard's thirsty."],   // FINAL-19: REVIEW-19's patch
  "hint.egypt.carmirror": ["dad", "The sunbeam has to turn a corner at the gallery's foot. The car has a mirror it isn't using."],
  "hint.egypt.trade": ["dad", "The goldsmith has a mirror he's sick of, and eyes too tired for it. I packed sunglasses."],
  "hint.egypt.topmirror": ["dad", "The copper mirror goes on the top step, facing the little door. One more corner, and the light's in."],  // PASS-17E: his own voice (the same clue)
  "hint.egypt.leave": ["dad", "The door is holding still now. Time to go through it."],                                              // kept
};
