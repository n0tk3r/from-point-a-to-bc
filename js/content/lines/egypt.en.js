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
  "egypt.arrive.1": ["dad", "Well, that's one expressway I won't be taking again."],                                                              // kept (the author's new first line, 10 October: the first line of play answers the movie's shortcut)
  "egypt.arrive.2": ["dad", "Buddy? Buddy, where are you?"],                                                                                    // kept
  "egypt.arrive.3": ["dad", "He was in his seat a minute ago, or a thousand years from now. I'm still working out the tenses."],   // kept
  "egypt.arrive.4": ["narrator", "Small sneaker prints wander away up the track, as if they owned it."],
  "egypt.arrive.5": ["dad", "He's gone to see the biggest thing in sight. He gets that from me."],
  "egypt.arrive.pray.1": ["dad", "Lord, I took a shortcut. You know that; You were in the car."],
  "egypt.arrive.pray.2": ["dad", "You know where he is. I don't even know when I am. Keep him, please. In Jesus' name, amen."],

  // ---------- the river, the bank, the far end of the track ----------
  "egypt.river.look": ["narrator", "A wide brown river, slow and full. Dad decides it is either the Nile or a very committed car wash."],                                               // kept
  "egypt.river.look2": ["narrator", "There are no hoses and no brushes. Dad is calling it: the Nile."],
  "egypt.river.use": ["narrator", "Dad stays out of the river. These are his good sandals, and also his only sandals."],
  "egypt.river.bible.1": ["dad", "This is the Egypt of my Bible. Abraham, Joseph, Moses: any of them could be round that bend."],
  "egypt.river.bible.4": ["dad", "Or not for a thousand years. I never kept the dates straight. I always skipped to the maps."],
  // (once Lot has told him who he is, he knows: Abram is here, and Joseph and Moses are still to come)
  "egypt.river.after.1": ["dad", "Abram's in Egypt this very week. Joseph and Moses are still a long way down the road."],
  "egypt.river.after.3": ["dad", "I never needed the dates in the margin. I needed his nephew, praying under a palm."],
  "egypt.reeds.look": ["narrator", "A bed of tall reeds at the water's edge. Dad calls them nature's ballpoint."],                                                                         // kept
  "egypt.reeds.take": ["narrator", "Dad cuts one reed and promises to bring it back. He has never once brought a pen back."],                               // kept
  "egypt.reeds.again": ["narrator", "One reed is plenty. Dad isn't opening a stationery shop."],                                                 // kept
  "egypt.reeds.basket.1": ["dad", "Moses' basket. '...and she laid it in the flags by the river's brink.'"],  // PASS-17E: reference aloud
  "egypt.reeds.basket.2": ["dad", "Flags are reeds, so I had to look. No basket. Either I'm early, or I'm late."],
  "egypt.reeds.basket.3": ["dad", "Flags are reeds, so I had to look. No basket yet. I'm early. I'm very early."],                               // (after the news)  PASS-17E: running gag ("I'm early, or I'm late" settled in two words; Little Sister's "Daddy's EARLY" in Act Four)
  "egypt.boat.look": ["narrator", "A boat rides low across the river under a load of white stone. Even the rocks here get a ferry."],
  "egypt.boat.look2": ["narrator", "A whole quarry is crossing the river, one boatload at a time. Dad complains about carrying in the groceries."],
  "egypt.palms.look": ["narrator", "Palm trees along the bank, the only shade for miles. Dad is standing in none of it."],
  "egypt.pyramids.look": ["narrator", "The pyramids stand white and sharp against the sky. They look brand new, as if somebody kept the receipt."],                                                 // kept
  "egypt.pyramids.look2": ["narrator", "They are farther off than they look. Dad learned that about big things while crossing a mall parking lot."],
  "egypt.pyramids.look3": ["narrator", "Dad wonders who else has looked at them from right here. Abraham, maybe. Or maybe not yet."],  // PASS-17E: shorter; a wonder, not a lesson ("my Bible" four times in a minute)
  "egypt.pyramids.look3b": ["narrator", "Abram could have stood right here and looked at those. This week, of all the weeks."],     // (once Lot has told him)
  "egypt.footprints.look": ["narrator", "Small sneaker prints, no two of them in a straight line. That's Dad's boy, all right."],
  "egypt.footprints.use": ["dad", "Up the track, toward the pyramid. Where he goes, I go."],
  "egypt.chicken.footprints": ["narrator", "Dad shows the General the prints. She knows those sneakers: they've stepped on her more than once, and she bears no grudge."],
  "egypt.track.look": ["narrator", "The track runs straight up to the pyramid. Dad found it without asking anybody, and wants that noted."],
  "egypt.block.look": ["narrator", "A stone block on a broken sledge, left where it fell. Somebody here is having a worse day than Dad."],
  "egypt.block.use": ["narrator", "Dad pushes the block. It's the size of a dishwasher, and it feels the same way about moving."],
  "egypt.donkey.look": ["narrator", "A donkey at the water's edge. Low mileage, runs on hay, and has never once needed a jump."],
  "egypt.donkey.look2": ["narrator", "He has been drinking since the wagon landed. Wherever he's going, he won't get there thirsty."],
  "egypt.donkey.use": ["narrator", "The donkey lets Dad scratch his ears. It's the friendliest welcome Dad has had since Nevada."],
  "egypt.donkey.sunglasses": ["narrator", "The donkey gives Dad the look a car salesman gives a man in sunglasses. Dad puts them away."],

  // ---------- the wagon, and what is still in it ----------
  "egypt.wagon.look": ["narrator", "The family wagon, nose down in a dune. Two hundred thousand miles and she still runs. Not right now, but in general."],                      // kept
  "egypt.hood.look": ["narrator", "Steam curls out from under the hood. Dad says she's just thinking it over."],
  "egypt.hood.look2": ["narrator", "The steam hasn't let up. The wagon isn't going anywhere until she has cooled off."],
  "egypt.hood.use": ["narrator", "Dad doesn't open the hood. He and the wagon have an understanding."],
  "egypt.hood.flashlight": ["narrator", "Dad shines the flashlight in through the grille. Sand, and more sand. That's the full report."],
  "egypt.hood.rootbeer": ["narrator", "The wagon doesn't take root beer. Dad is fairly sure."],
  // CAR-13W: the driver's window is rolled down (round thirteen), and through it he looks into the wagon; a click on it,
  // or on the wagon, gets him in (egypt-car, below). Said outside, at the window: before he has the map, and after it.
  "egypt.inside.look": ["narrator", "The driver's window is rolled down. Dad's map is in the glovebox, being wrong in private."],
  "egypt.inside.look2": ["narrator", "The window is down to let the heat out. The heat has other plans."],
  // CAR-13W: the key (egypt.wagon.try) and the glovebox (egypt.glovebox.look, egypt.wagon.use, egypt.wagon.empty) are
  // inside the wagon now, and their lines with them: see egypt-car, below.
  "egypt.mirror.look": ["narrator", "The door mirror. It has shown Dad every wrong turn he ever made, only smaller."],
  // the first time he comes up to the car, the low sun off the door mirror catches him in the eye (once: the mirror's hint)
  "egypt.mirror.dazzle": ["dad", "Ow. That's the sun, right off the door mirror. It's brighter than it appears."],
  "egypt.mirror.take": ["narrator", "One twist and the mirror comes off in Dad's hand. It has been one twist from off since March."],
  "egypt.car.noreason": ["narrator", "Dad doesn't take things off his car without a reason, even a bad one. So far he hasn't got one."],
  "egypt.suitcase.look": ["narrator", "A suitcase strapped to the roof rack. Dad sat on it to get it shut, and it hasn't forgiven him."],
  "egypt.suitcase.open": ["narrator", "The open suitcase, with six loud shirts folded inside. Dad packed for a week of barbecues."],
  "egypt.suitcase.take": ["narrator", "A pair of sunglasses, from on top of six more shirts, every one louder than the one Dad has on."],
  // under the shirts: General Feathers, and a note in crayon (the close-up shows it: egypt-crash.js, NOTE)
  "egypt.suitcase.general.1": ["dad", "And under the shirts, General Feathers. With orders, in crayon."],
  "egypt.suitcase.general.2": ["dad", "My youngest sent her to watch me. She has concerns about my driving."],
  "egypt.suitcase.general.3": ["dad", "Welcome aboard, General. The boy's gone on ahead."],
  "egypt.suitcase.again": ["narrator", "Nothing is left in the suitcase but shirts. So far the week of barbecues has been one pyramid."],
  "egypt.trunk.look": ["narrator", "The trunk on the roof rack holds everything Dad might need, packed under everything he won't."],
  "egypt.trunk.flashlight": ["narrator", "A flashlight. Dad packed it in case of a flat tire, not in case of Egypt."],
  "egypt.trunk.rest": ["narrator", "A lawn chair, jumper cables and the windshield shade are left in the trunk. Dad needs none of them yet."],  // PASS-17E: funnier (and the shade is planted)
  "egypt.trunk.shade": ["narrator", "The windshield shade. After ten years of keeping the sun out, it's time it switched sides."],
  "egypt.trunk.after": ["narrator", "A lawn chair and jumper cables. Much longer in this heat and Dad is getting the chair out."],
  "egypt.trunk.cables": ["narrator", "Jumper cables. The nearest battery is nearly four thousand years up the road."],
  "egypt.trunk.chair": ["narrator", "A lawn chair, for when Dad has earned a sit-down. He hasn't, not while his boy is out there."],
  "egypt.cooler.look": ["narrator", "The cooler holds root beer, ice, and one sandwich Dad isn't ready to talk about."],
  "egypt.cooler.take": ["narrator", "A root beer, still cold. The ice held. Something on this trip had to."],
  "egypt.cooler.have": ["narrator", "Dad already has a root beer in his pocket. One at a time: it's a cooler, not a bar."],
  "egypt.cooler.more": ["narrator", "Dad takes one more. The rest are for the drive home, because he's an optimist."],

  // ---------- Lot, Abram's nephew: under the palm, praying, while his donkey drinks ----------
  // Before he has said who he is he is a stranger on the screen ("herdsman"); after it, "Lot". He tells who he is as
  // his own memory, in his own words, from Genesis 11:27 to 13:5 and nothing beyond it (docs/PUZZLES-egypt.md has
  // each statement and its verse). Dad's understanding lands here, the first time Lot has told it.
  "egypt.lot.look": ["narrator", "A man at his prayers in the shade of a palm. A car fell out of the sky beside him, and he never lost his place."],
  "egypt.lot.look2": ["narrator", "Lot, Abram's nephew, back at his prayers. One of them was for the Son, and Dad won't forget it."],                          // (after he has prayed for the boy)
  "egypt.lot.hello": ["lot", "You came down out of the sky in a red box, with no ox and no donkey to pull it."],
  "egypt.scribe.hello2": ["dad", "It has a hundred and forty horses. They're resting."],                                             // kept (Lot names the ox and the donkey that were not pulling, so that the horses answer him: round twelve)
  "egypt.lot.hello2": ["lot", "Then let them rest. Since the LORD called my uncle, I ask no man how he came here."],   // FINAL-19: REVIEW-19's patch
  "egypt.ask.boy": ["dad", "Have you seen a boy? About this tall, asks a lot of questions?"],                                        // kept
  "egypt.lot.boy.1": ["lot", "A small one in strange sandals went up the track, asking everyone for the 'wy-fy'."],
  "egypt.lot.boy.2": ["lot", "If the Egyptians have such a thing, it is at their Horizon. They keep everything there."],
  "egypt.lot.boy.3": ["dad", "That's my boy. He asks that in every house we walk into. It's how he says hello."],
  "egypt.lot.ask.horizon": ["dad", "This Horizon everybody's so keen on. What is it, exactly?"],
  "egypt.lot.horizon.1": ["lot", "The great white one yonder. It is their king's tomb, and they call it the Horizon of Khufu."],
  "egypt.lot.horizon.2": ["dad", "A pyramid called the Horizon. Finally, a horizon I can actually walk to."],
  "egypt.lot.ask.news": ["dad", "Anything I should know before I go up? This isn't asking for directions."],  // PASS-17E: running gag (he has never asked for directions)
  "egypt.lot.news.1": ["lot", "The men who come down for water say that a wall inside the Horizon has begun to hum."],
  "egypt.lot.news.2": ["lot", "And their scribe's pen has split, so he can write nobody onto his list."],
  "egypt.lot.news.3": ["dad", "A humming wall and a paperwork problem. I've had Mondays like that."],
  "egypt.lot.news.4": ["lot", "Since the hum began, the geese on the bank all stand facing the Horizon."],
  // who he is: his father, his grandfather, the call, the promise, Canaan, the famine (Genesis 11:27-32, 12:1-10, 13:5)
  "egypt.lot.ask.who": ["dad", "Who are you, if you don't mind my asking?"],
  "egypt.lot.who.1": ["lot", "I am Lot, the son of Haran. My father died in Ur of the Chaldees, before his own father did."],
  "egypt.lot.who.2": ["lot", "My grandfather Terah took my uncle Abram, Sarai and me out of Ur. He died at Haran."],
  "egypt.lot.who.3": ["dad", "Ur of the Chaldees. I've only ever seen that on the maps in the back of my Bible."],
  "egypt.lot.who.4": ["lot", "The LORD called my uncle to a land He would show him. He was seventy-five, and he went."],  // PASS-17E: shorter; a man telling it, not reading it out
  "egypt.lot.who.8": ["lot", "He built altars to the LORD in Canaan. Then the famine brought us down into Egypt."],  // PASS-17E: shorter (the act's longest line)
  // and Dad understands, slowly and then all at once: he is standing in Genesis 12 (an aside, looking out over the river)
  "egypt.abram.1": ["dad", "Abram, not Abraham yet, in Egypt, in a famine. I'm standing in Genesis."],  // PASS-17E: reference aloud (the chapter number); the penny dropping, as it drops
  "egypt.abram.3": ["dad", "God promised every family on earth a blessing through him. Mine's included, and I'm counting on it."],  // PASS-17E: reference aloud (the design's own sample); FINAL-19: REVIEW-19's patch
  // this week, told briefly and judging nobody (Genesis 12:14-20)
  "egypt.lot.ask.week": ["dad", "You look like a man waiting for a ride."],
  "egypt.lot.week.1": ["lot", "The king took my uncle's wife into his house, and was good to my uncle for her sake."],
  "egypt.lot.week.4": ["lot", "Then the LORD struck his house with plagues. Today the king's men are sending us out of Egypt."],
  "egypt.lot.week.5": ["dad", "I'd heard something along those lines. From a long way off."],
  "egypt.lot.week.6": ["lot", "Then the story has traveled farther than we have."],
  // parting, the first time after he has told it: two men and two sons, and Lot prays for the boy (his own prayer, not Dad's)
  "egypt.lot.ask.bye": ["dad", "There's a hill to climb, and a boy to ground."],
  "egypt.lot.son.1": ["lot", "My uncle has no son, and yet the LORD has promised to make of him a great nation."],
  "egypt.lot.son.2": ["dad", "A nation promised, and no son yet. I've got the one, and I've mislaid him."],
  "egypt.lot.son.3": ["lot", "Then you are both waiting on a son. Yours, at least, is already walking."],
  "egypt.abram.4": ["dad", "I'd give a lot to go and shake your uncle's hand."],
  "egypt.abram.5": ["dad", "But I've got a boy to find."],
  "egypt.lot.son.4": ["lot", "Then go and find him. But first, let me ask for him."],
  "egypt.lot.prayer": ["lot", "LORD, the God of my father's brother Abram, keep the boy until his father comes."],
  "egypt.lot.amen": ["dad", "Amen."],
  "egypt.lot.thanks": ["dad", "Thank you. I asked Him the same when I landed. It's good to hear another man ask."],
  "egypt.lot.bye": ["lot", "Go in peace. Everything up there has already gone wrong, so you cannot be late."],
  // things offered to him
  "egypt.lot.rootbeer.1": ["dad", "Something cold? It's on the house. Well, on the car."],
  "egypt.lot.rootbeer.2": ["lot", "It hisses. Where I come from, a man leaves a hissing thing alone."],
  "egypt.lot.map.1": ["lot", "Where is the river on this?"],
  "egypt.lot.map.2": ["dad", "There isn't one. It's Nevada."],
  "egypt.lot.map.3": ["lot", "A land with no river. Then I will pray that it has wells."],
  "egypt.lot.chicken": ["lot", "I would not know whether to shear her, milk her, or follow her."],

  // ================= egypt-car: inside the wagon =================
  // CAR-13W: new in round thirteen. Dad's own view from the driver's seat: nobody is drawn here, and every line is his.
  // The ids, the words and when each is said are the design's (briefs/out/car-interior-design.md, section 4).

  // ---------- getting in ----------
  "egypt.car.arrive": ["narrator", "Dad climbs in behind the wheel. It's as hot as a skillet in here, and still the only seat in Egypt that fits him."],                // (the first time only)

  // ---------- the glovebox: the road map (puzzle #1) ----------
  // CAR-13W: new words, and said inside now (the glovebox, shut). It said "The glovebox. Home of the map, the manual, and
  // something that used to be mints." The manual has moved to the door pocket and the mints are gone, so that the
  // author's "Nothing left in there but ketchup packets. I'm saving those." stays true.
  "egypt.glovebox.look": ["narrator", "The glovebox. Dad's map is in there, along with a few things he's saving."],
  // CAR-13W: the author's two, moved here word for word with their ids: said as the glovebox drops open and the map is
  // his, and then whenever he looks in.
  "egypt.wagon.use": ["narrator", "The glovebox drops open on a road map. It covers three states and zero centuries, and Dad takes it anyway."],                                   // kept
  "egypt.wagon.empty": ["narrator", "Nothing is left in the glovebox but ketchup packets. Dad is saving those."],                                      // kept
  "egypt.car.glovebox.map": ["narrator", "The map has never gone back in the way it came out, and Dad isn't starting now."],                           // (the map, tried on it)

  // ---------- the windshield, the rearview mirror, the air freshener ----------
  "egypt.car.windshield.look": ["narrator", "Nothing through the windshield but sand. The wagon parked nose first. Dad has parked worse."],                      // (the two looks, in turn)
  "egypt.car.windshield.look2": ["narrator", "Past the dune there's a river and no traffic. It's the best parking space Dad has ever found."],
  "egypt.car.windshield.use": ["narrator", "Dad wipes the glass. The sand is on the other side, as it always is."],
  "egypt.car.rearview.look": ["narrator", "The rearview mirror shows nothing but sky. The wagon is standing on her nose."],
  "egypt.car.rearview.use": ["narrator", "Dad tips the mirror down and gets sky, tips it up and gets more sky, and leaves it."],                             // (before he knows what light does)
  "egypt.car.rearview.glued": ["narrator", "The rearview mirror is glued to the windshield. The one on the door is the one that comes off."],                     // (after it: "egypt.knowsLight")
  "egypt.car.freshener.look": ["narrator", "An air freshener labeled 'New Car Smell'. The wagon is older than two of Dad's kids, and nobody is fooled."],

  // ---------- the sun visor: his youngest's drawing ----------
  "egypt.car.visor.look": ["narrator", "The sun visor. Dad's youngest tucked something behind it, and for once he isn't driving."],      // (up)
  "egypt.car.visor.down.1": ["narrator", "It's her drawing, in crayon: the five of them, the wagon, and General Feathers on the roof."],                      // (pulled down: once)
  "egypt.car.visor.down.2": ["dad", "She drew me the biggest. Hang on, you three. We're making good time."],
  "egypt.car.visor.look2": ["narrator", "The drawing, and behind it the registration, paid through next spring. Dad will have to explain the gap."],                      // (down)

  // ---------- the wheel, the gauges, the horn, the gear lever, the key ----------
  "egypt.car.wheel.look": ["narrator", "The steering wheel. Dad had both hands on it the whole way, and wants that on the record."],
  "egypt.car.wheel.use": ["narrator", "Dad turns the wheel. The front end is in a dune, and doesn't get the message."],
  "egypt.car.gauges.look": ["narrator", "The odometer reads two hundred thousand and six miles. The last one was a long one."],
  "egypt.car.gauges.use": ["narrator", "Dad taps the gauge. The needle stays in the red, so it isn't the gauge."],
  "egypt.car.horn.look": ["narrator", "The horn. It's a little flat, which Mom says about Dad too."],
  "egypt.car.horn.use": ["narrator", "Dad never raises his voice. That's what the horn is for."],                                             // (the first honk, after the horn)
  // CAR-13W: the design has "There's a man praying out there." Nothing in the car speaks of prayer (the head, above), and
  // the act's check holds every line of Dad's that does to the list of lines written for the faith: so, "sitting quietly".
  "egypt.car.horn.again": ["narrator", "Once is hello and twice is rude. A man is sitting quietly out there, so Dad leaves the horn alone."],                         // (every honk after: no sound)
  "egypt.car.gears.look": ["narrator", "The gear lever: P, R, N, D and L. There's nothing marked B.C. Dad would have noticed."],
  "egypt.car.gears.use": ["narrator", "Dad leaves it in Park. Park has never once let him down."],
  "egypt.car.key.look": ["narrator", "The key is still in the ignition. Car thieves haven't been invented yet."],
  // CAR-13W: moved here word for word, with its id, from the wagon outside (its "Start"): said after the starter.
  "egypt.wagon.try": ["narrator", "Dad turns the key. The wagon makes the noise she makes when he brings up the transmission."],

  // ---------- the radio, the slushie, his seat ----------
  "egypt.car.radio.look": ["narrator", "The tape in the radio is a musical Mom recorded off the air, traffic report and all."],
  "egypt.car.radio.use": ["narrator", "Static, from one end of the dial to the other. It's a quiet century."],                             // (after the hiss)
  "egypt.car.slushie.look": ["narrator", "The Son's slushie, melting in its holder. He said the sky did the slushie thing. Dad said weather, and stands by weather."],
  "egypt.car.slushie.use": ["narrator", "Dad leaves the slushie for the boy. He has never finished one, but he likes to be asked."],
  "egypt.car.slushie.rootbeer": ["narrator", "That cup holder is the Son's. Dad's root beer rides in his shorts."],                                              // (the root beer, tried on it)
  "egypt.car.seat.look": ["narrator", "The passenger seat: six wrappers, one sock and no boy. He travels light and leaves heavy."],
  "egypt.car.seat.use": ["narrator", "Half a pack of gum is stuck under the Son's seat. Dad leaves that problem for later."],              // (the gum is not taken)
  "egypt.car.seat.chicken": ["narrator", "Dad sits the General in the Son's seat. She reports that it's sticky, and she's right."],                            // (General Feathers, tried on it)

  // ---------- the owner's manual, the door ----------
  "egypt.car.manual.look": ["narrator", "The owner's manual, in the door pocket. It's read to the middle, like all of Dad's manuals."],
  "egypt.car.manual.use": ["narrator", "Dad has read the first half. Time travel must be in the second."],
  "egypt.car.door.look": ["narrator", "The driver's door. Out there is Egypt. In here is the one thing in Egypt that Dad understands."],

  // ================= egypt-site: the foot of the pyramid =================

  // ---------- arrival, and the place ----------
  "egypt.site.arrive.1": ["dad", "So that's what they look like before the gift shop."],
  "egypt.site.arrive.2": ["overseer", "Why is nobody pulling? Why is every man on this site standing still?"],
  "egypt.site.arrive.3": ["dad", "And that'll be the manager."],
  "egypt.site.pyramid.look": ["narrator", "The pyramid, cased in smooth white stone all the way up. Somebody has waxed a mountain."],
  "egypt.site.pyramid.look2": ["narrator", "It's still in scaffolding, and nearly done. Dad knows all about 'nearly done'. He owns a deck."],
  "egypt.site.small.look": ["narrator", "Three small pyramids stand around the side of the great one."],
  "egypt.site.entrance.look": ["narrator", "A doorway at the top of the steps, under two great leaning slabs. There is no welcome mat."],
  "egypt.site.entrance.look2": ["narrator", "The way in. A wall is humming somewhere up there, and Dad's son went to say hello to it."],  // PASS-17E: truer (the old line was a puzzle of its own; "It's how he says hello" comes round once more)
  "egypt.site.stair.look": ["narrator", "Steps of mud brick climb the face of the pyramid to the doorway."],
  "egypt.site.desk.look": ["narrator", "The scribe's station under its awning, with the day's wages set out beside it: bread and beer."],
  "egypt.site.desk.look2": ["narrator", "Papyrus, and tallies scratched on bits of broken pot. All the office needs is a dead plant."],
  "egypt.site.sledge.look": ["narrator", "A white block on a wooden sledge. It's the invention of the bad back."],
  "egypt.site.sledge.look2": ["narrator", "The sand ahead of the runners is wet, and raked like a ballfield. The haulers know something Dad doesn't."],
  "egypt.site.sledge.use": ["narrator", "Dad pulls. The sledge doesn't. They agree to see other people."],
  "egypt.site.blocks.look": ["narrator", "Copper chisels, wooden mallets and a plumb line. The stone they cut is squarer than Dad's garage."],
  "egypt.site.blocks.use": ["narrator", "They're another man's chisels. Dad once lent a ladder, and he knows how that ends."],
  // (a second look at the masons' work: the stone itself. Said once.)
  "egypt.site.shells.1": ["dad", "Seashells in the stone, out here in the desert. The Flood covered every hill."],
  "egypt.site.mizraim": ["dad", "Noah's grandson settled Egypt. Technically, everybody here's my cousin."],  // PASS-17E: reference aloud; a Bible fact tacked on, turned into his own joke
  "egypt.site.sunspot.look": ["narrator", "A patch of full sun with nobody standing in it. The men here have more sense."],
  "egypt.site.sunspot.look2": ["narrator", "Full sun, and a clear line from here up to the doorway. If light were a golf ball, this would be the tee."],
  "egypt.site.sunspot.use": ["narrator", "Dad stands in the sun. It's the same sun as at home, with the dial turned all the way up."],
  "egypt.site.track.look": ["narrator", "The track back down to the river, the wagon, and the only cold drinks in Egypt."],
  "egypt.site.rope.look": ["narrator", "A hauling rope as thick as Dad's wrist, dropped where the gang stopped pulling."],
  "egypt.site.scaffold.look": ["narrator", "Scaffolding of poles and rope, four stories up. Dad gets dizzy cleaning the gutters."],
  "egypt.site.masons.look": ["narrator", "A mason on a hanging plank, polishing the white stone. There's nothing under him but Egypt."],
  "egypt.site.yard.look": ["narrator", "Blocks of stone in the yard, each one waiting its turn to go up."],
  "egypt.site.water.look": ["narrator", "Big water jars. Every drop in them was carried up the track from the river."],
  "egypt.site.bricks.look": ["narrator", "Mud bricks drying in rows. Somebody here invented the ice cube tray and never got the credit."],
  "egypt.site.bricks.use.1": ["dad", "Bricks for Pharaoh. I know this one: the Israelites made them."],
  "egypt.site.bricks.use.3": ["dad", "But the pyramid's stone. The Bible's bricks were for 'treasure cities, Pithom and Raamses.'"],  // PASS-17E: reference aloud; a man working it out, not reading it out
  "egypt.site.bricks.use.4": ["dad", "Not one word about building a pyramid. I've had it wrong since Sunday school."],  // PASS-17E: shorter (the point made once)

  // ---------- the scribe: a pen, a sheet, a pass ----------
  "egypt.scribe.look": ["narrator", "The scribe has been staring at a blank sheet for a while. Dad knows writer's block when he sees it."],              // kept
  "egypt.scribe.look2": ["narrator", "The scribe is writing again, fast, like a man catching up on a whole lost morning."],
  "egypt.scribe.meet.1": ["scribe", "Do not tell me your name. Until I have a pen, it is only a noise."],
  "egypt.scribe.meet.2": ["dad", "Pen trouble?"],
  "egypt.scribe.meet.3": ["scribe", "It split at dawn, and since then nothing has happened. Not officially."],
  "egypt.scribe.boy.1": ["scribe", "There is no boy on my list. If he is not on the list, he did not go in. That is what a list is for."],
  "egypt.scribe.boy.2": ["dad", "He's not on a lot of lists. It's never once stopped him going in."],
  "egypt.scribe.ask.list": ["dad", "How does a man get onto that list of yours?"],
  "egypt.scribe.list.nopen": ["scribe", "I write him onto it, with a pen. You see the difficulty."],
  "egypt.scribe.list.nosheet": ["scribe", "I write him a pass, and my last clean sheet is promised to the grain account."],
  "egypt.scribe.list.done": ["scribe", "You are on it already. It is the only thing written anywhere today: short, but tidy."],
  "egypt.ask.bye": ["dad", "I'll let you get back to your sheet."],                                                                  // kept
  "egypt.ans.bye": ["scribe", "It is not going anywhere, and neither am I."],                                                            // kept
  "egypt.give.reed": ["dad", "Here. It's a pen. Some assembly required."],                                                           // kept
  "egypt.got.reed": ["scribe", "A good reed. You have the eye of a scribe and the clothes of a market stall."],                      // kept
  "egypt.got.reed.b": ["dad", "I'll take the first half. The shirt can speak for itself."],   // PASS-19E: new box, said right after egypt.got.reed (a Dad reaction between the scribe's boxes (the run of four broken))
  "egypt.scribe.rush": ["scribe", "A rush is the proper pen, but a man without one cannot be particular."],
  "egypt.scribe.supplier": ["scribe", "You supply reeds, so you go on the list. But my last sheet is for the grain account."],
  "egypt.give.map": ["dad", "Draw on this. It's a map, and it's already wrong, so you can't make it worse."],                               // kept
  "egypt.got.map.nopen": ["scribe", "It is a fine sheet, and I have nothing to mark it with."],                                                // kept
  "egypt.scribe.pass.1": ["scribe", "'One supplier of reeds. Foreign. Loud about the shoulders.' There. Now you exist."],
  "egypt.scribe.pass.2": ["scribe", "Show the guard my side of the sheet. He knows my hand."],
  "egypt.pass.got": ["dad", "A hall pass. Thirty years out of school, and I finally get one."],
  "egypt.scribe.rootbeer": ["scribe", "Beer made of roots? The brewers would never forgive me."],
  "egypt.scribe.shade": ["scribe", "I hold a pen, and nothing else. Ask a man with idle arms; this site is full of them."],
  "egypt.scribe.pass": ["scribe", "I wrote it, so I do not need to read it. That is the whole point of writing."],
  "egypt.scribe.chicken": ["scribe", "There is no sign for that bird. So, officially, she is not here."],

  // ---------- the scribe's news: the same week from the Egyptian side (Genesis 12:10-20, told from outside, as gossip) ----------
  // Offered once Lot has told Dad who he is: Dad hears it knowing more than the scribe does.
  "egypt.scribe.ask.news": ["dad", "Any news? I've been out of touch. Badly out of touch."],
  "egypt.scribe.news.1": ["scribe", "Only grain. The famine has driven the desert herdsmen down to us, and I count every basket they eat."],
  "egypt.scribe.news.2": ["scribe", "One of them is rich, a man named Abram. He brought his sister with him."],
  "egypt.scribe.news.3": ["dad", "Abram. I've met his nephew."],
  "egypt.scribe.news.4": ["scribe", "She is very fair, and she was taken into the Great House."],
  "egypt.scribe.news.5": ["dad", "The Great House. That's what 'Pharaoh' means; I read it in a footnote."],
  "egypt.scribe.news.6": ["scribe", "Sheep, oxen, asses and camels: the king's gifts to him run all through my accounts."],
  "egypt.scribe.news.7": ["scribe", "Then a sickness fell on the Great House, and now they say she is his wife."],
  "egypt.scribe.news.8": ["dad", "And the king's sending him away. Him, his wife and everything he owns."],
  "egypt.scribe.news.9": ["scribe", "Today, with the king's own men. But how do you know that? It is written nowhere at all."],
  "egypt.scribe.news.10": ["dad", "Not yet."],
  "egypt.scribe.news.11": ["dad", "His nephew's down by the river, praying. For my boy, among other things."],

  // ---------- the overseer: the schedule ----------
  "egypt.overseer.look": ["narrator", "A big man with a schedule. The schedule can't be seen, but it can certainly be heard."],
  "egypt.overseer.meet.1": ["overseer", "Nobody dresses like that without a reason. You must be the specialist."],
  "egypt.overseer.meet.2": ["dad", "Close. I'm the generalist nobody sent for."],
  "egypt.overseer.meet.3": ["overseer", "A wall inside has begun to hum. Inspect it and make it stop. Take all the time you need, as long as it is today."],
  "egypt.overseer.boy.1": ["overseer", "A boy? I have a whole gang not working. I cannot watch a boy not working as well."],
  "egypt.overseer.ask.hum": ["dad", "Tell me about this humming wall."],
  "egypt.overseer.hum.1": ["overseer", "It is in the top chamber, and it began at dawn. Not one man will carry a basket past it."],
  "egypt.overseer.hum.2": ["overseer", "I told them a wall cannot hurt them. They told me a wall cannot hum, either."],
  "egypt.overseer.hum.3": ["dad", "They've got you there. I'd have said it was the wind."],  // PASS-17E: running gag (everything he cannot explain is the wind)
  "egypt.overseer.hum.4": ["overseer", "Twenty years I have built this, on time, every day of it. Until a wall began to hum."],
  "egypt.overseer.ask.schedule": ["dad", "How's the schedule holding up?"],
  "egypt.overseer.sched.0a": ["overseer", "The haulers blame the wall and the scribe blames his pen. I blame them all, which saves time."],
  "egypt.overseer.sched.0b": ["overseer", "First get yourself onto the scribe's list. The guard at the stair turns back any man who is not on it."],
  "egypt.overseer.sched.1": ["overseer", "It still hums. Ask the lamp boy: he saw something in there, and he will tell me nothing at all."],
  "egypt.overseer.sched.2": ["overseer", "A little sun in a hand? Then find a little sun. I have only the big one."],
  "egypt.overseer.sched.3": ["overseer", "The sunlight is out here and the wall is in there. I did not plan for them to meet."],
  "egypt.overseer.sched.3b": ["overseer", "Unless you can bend the day around three corners, we are late."],
  "egypt.overseer.sched.3c": ["dad", "We're not late. We're making good time."],
  "egypt.overseer.sched.4": ["overseer", "There is daylight in my pyramid, and it is not on the schedule. Is it helping?"],
  "egypt.overseer.sched.4b": ["dad", "Like a charm."],
  "egypt.overseer.sched.4c": ["overseer", "Then it was always on the schedule."],
  "egypt.overseer.ask.bye": ["dad", "I'll get right on it."],
  "egypt.overseer.bye": ["overseer", "Get on it faster."],
  "egypt.overseer.bark.light": ["overseer", "Does it still hum? No, do not answer me. I can see it in your face from here."],
  "egypt.overseer.bark.guard": ["overseer", "My guard is holding up the sun. Put it on the schedule, under 'strange'."],
  "egypt.overseer.bark.all": ["overseer", "There is daylight in my pyramid, and nobody told me. Nobody tells me anything."],
  "egypt.overseer.map": ["overseer", "A plan? I have had the same plan for twenty years, and it was going well."],
  "egypt.overseer.shade": ["overseer", "I oversee. If I stand there holding that, who oversees me holding it?"],
  "egypt.overseer.mirror": ["overseer", "Who is that tired man? Take it away."],
  "egypt.overseer.rootbeer": ["overseer", "Is it medicine? If it is not medicine, then it cannot help me."],

  // ---------- the haulers: one speaks, one agrees, one eats ----------
  "egypt.haulers.look": ["narrator", "Three haulers resting by their sledge. One talks, one nods and one eats. It's a road crew."],
  "egypt.haulers.meet.1": ["hauler1", "We are the Friends of Khufu, the best gang on the Horizon. We are resting."],
  "egypt.haulers.meet.2": ["hauler2", "We are resting very well."],
  "egypt.haulers.meet.3": ["hauler3", "Mm."],
  "egypt.haulers.boy.1": ["hauler1", "The small one asked to ride the sledge. We said no, and he rode it anyway."],
  "egypt.haulers.boy.2": ["hauler2", "He was no weight at all."],
  "egypt.haulers.boy.3": ["dad", "He's been told about riding things, many times. It has never once helped."],
  "egypt.haulers.ask.break": ["dad", "Long break?"],
  "egypt.haulers.break.1": ["hauler1", "Since the wall began to hum. We do not pull stone toward a noise."],
  "egypt.haulers.break.2": ["hauler2", "Never toward a noise."],
  "egypt.haulers.ask.free": ["dad", "Hang in there, fellas. One day you'll all be free."],
  "egypt.haulers.free.1": ["hauler1", "Free? We are paid. Bread and beer, every day."],
  "egypt.haulers.free.2": ["hauler2", "Every day."],
  "egypt.haulers.free.3": ["hauler3", "Mm-hm."],
  "egypt.haulers.free.4": ["dad", "Bread and beer, every day. I take it back, are you hiring?"],
  "egypt.haulers.ask.sand": ["dad", "Why's the sand wet in front of the sledge?"],
  "egypt.haulers.sand.1": ["hauler1", "Wet the sand in front of the runners, and one man pulls like two."],
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
  "egypt.guard.look": ["narrator", "A tall guard at the foot of the stair, bored and sweating, in a patch of no shade at all."],
  "egypt.guard.look2": ["narrator", "The guard holds the shade up to the sun like a man surrendering. It's working."],
  "egypt.guard.stop": ["guard", "Nobody goes up these stairs who is not on the scribe's list. Nobody at all."],
  "egypt.guard.stop.2": ["dad", "I'm more of a walk-in."],
  "egypt.guard.stop.3": ["guard", "Then walk to the scribe, under the awning. He keeps the list, and I only keep the stair."],
  "egypt.pass.show": ["dad", "One hall pass. Signed, sealed and slightly folded."],
  "egypt.guard.pass.1": ["guard", "The scribe's hand. I know it well, for it looks like geese in a quarrel."],
  "egypt.guard.pass.2": ["guard", "You are on the list, so go up. If it hums at you, do not bring it here."],
  "egypt.site.pray.1": ["dad", "Lord, it's dark in there, and it hums. That's exactly where he'd go."],
  "egypt.site.pray.2": ["dad", "Go in ahead of me. I'll follow, for once. Amen."],
  "egypt.guard.after": ["guard", "You are on the list, and the stair is behind me. I am hot. That is all my news."],
  "egypt.shade.try.1": ["narrator", "Dad holds the shade up in the sun, and a patch of sunlight jumps up the stair into the doorway."],  // PASS-17E: a wrong foot that pays (the next line: "And it stops when I let go.")
  "egypt.shade.try.2": ["narrator", "It drops away the moment Dad lowers his arms. The job wants somebody with steady arms and nothing to do."],
  "egypt.shade.ask": ["dad", "Could you hold this up in the sun? That's the whole job."],
  "egypt.guard.nohold": ["guard", "I guard. I do not hold."],
  "egypt.guard.cold": ["guard", "I would hold it for something cold. But there is nothing cold in Egypt, and so I guard."],
  "egypt.rootbeer.give": ["dad", "Try this. It's cold, and around here that makes it treasure."],
  "egypt.guard.rootbeer": ["guard", "It bites the tongue, like a small and friendly snake."],
  "egypt.guard.owe": ["guard", "I owe you one holding, of anything you like, so long as it is not heavy."],
  "egypt.guard.again": ["guard", "One snake is a friend. Two would be a nest."],
  "egypt.shade.favor": ["dad", "About that holding you owe me."],
  "egypt.guard.take": ["guard", "The shining thing, up in the sun? For how long?"],
  "egypt.shade.notlong": ["dad", "Not long."],
  "egypt.guard.notlong": ["guard", "The overseer says 'not long' too. He has been saying it for twenty years."],
  "egypt.shade.lit": ["narrator", "The sunlight runs up the stair and in at the doorway. Nobody asks it for a pass."],
  "egypt.beam.all": ["dad", "If my mirrors are where I left them, that's going all the way in."],
  "egypt.guard.arms.1": ["guard", "My arms have gone to sleep. They are the only part of me that has."],
  "egypt.guard.arms.2": ["guard", "How long is 'not long' in your country? In days."],
  "egypt.guard.arms.3": ["guard", "When this is over I would like another of the snake water. A big one."],
  "egypt.guard.full": ["guard", "Later. My hands are full of your sun."],
  "egypt.guard.sunglasses": ["guard", "It is darker, but it is no cooler. I have been cheated."],
  "egypt.guard.map": ["guard", "This is not the scribe's hand. It is a great many roads to nowhere I know."],
  "egypt.guard.chicken": ["guard", "She does not move, and she has no arms. I do not see how she is in charge."],
  "egypt.guard.chicken.2": ["dad", "She delegates."],

  // ================= egypt-gallery: inside the pyramid =================

  // ---------- arrival, and the place ----------
  "egypt.gallery.arrive.1": ["dad", "Would you look at that."],
  "egypt.gallery.arrive.2": ["dad", "A hallway four stories high, all uphill, by lamplight. And me in sandals."],
  "egypt.gallery.walls.look": ["narrator", "Each row of stone steps in a little from the one below it. Dad gets nervous hanging a shelf."],
  "egypt.gallery.walls.look2": ["narrator", "The gallery is shaped like the hull of a ship turned upside down, and built out of rock."],
  "egypt.gallery.out.look": ["narrator", "Daylight, at the end of a very low passage. Dad means to watch his head this time."],
  "egypt.gallery.low.look": ["narrator", "A low passage leading off into the dark. No lamps, no hum, and no small footprints."],
  "egypt.gallery.low.use": ["narrator", "Dad calls 'Buddy?' into the passage. It says 'Buddy' back, twice. Nobody is home."],
  "egypt.gallery.low.flashlight": ["narrator", "The flashlight's beam goes a long way into nothing. The batteries don't enjoy the trip."],
  "egypt.gallery.top.look": ["narrator", "A small doorway at the top of the gallery. The lamps give up before the climb does."],
  "egypt.gallery.top.look2": ["narrator", "The way to the chamber, the hum, and the one man in Egypt who can't hear it."],
  "egypt.gallery.slot.look": ["narrator", "Slots are cut into the stone bench at intervals, all the way up the gallery."],
  "egypt.gallery.slot.beam": ["narrator", "The sunbeam lands on plain stone beside the slot and goes no farther. Stone makes a poor mirror."],
  "egypt.gallery.slot.set": ["narrator", "Dad's door mirror, wedged in a pyramid. It has never had a view like this."],
  "egypt.gallery.step.look": ["narrator", "A step at the top of the gallery, flat as a table. It's a good place to stand something."],
  "egypt.gallery.step.set": ["narrator", "The goldsmith's mirror stands on the step, doing the one thing he couldn't bear: shining."],
  "egypt.gallery.marks.look": ["narrator", "Squiggles of red paint on the stone. The builders left themselves a note."],
  "egypt.gallery.marks.look2": ["narrator", "Dad guesses it means 'this way up'. He guesses with great confidence."],
  "egypt.gallery.jars.look": ["narrator", "Jars of lamp oil, lined up along the wall. The lamp boy keeps count of them."],
  "egypt.gallery.jars.use": ["narrator", "Dad doesn't borrow a lamp. The boy counts them, and Dad wouldn't want him to come up one short."],
  "egypt.gallery.ladder.look": ["narrator", "A ladder against the wall. It's the one thing in here Dad already knows how to fall off."],
  "egypt.gallery.rope.look": ["narrator", "A coil of rope. Rope is the answer to everything here: duct tape, with splinters."],
  "egypt.gallery.runner.look": ["narrator", "A sledge runner, worn flat. Whatever it hauled up here wasn't coming back down."],
  "egypt.gallery.chest.look": ["narrator", "A chest left halfway up the gallery. Somebody heard the hum and remembered an appointment."],
  "egypt.gallery.dinner.look": ["narrator", "Bread and beer, left on the bench. That's a whole day's pay. The hum must be serious."],

  // ---------- the lamp boy: the only one who saw ----------
  "egypt.lampboy.look": ["narrator", "A boy with a jar of oil, sitting as far from the top of the gallery as he can get."],
  "egypt.lampboy.meet.1": ["lampboy", "You wear strange sandals. So did the small one."],
  "egypt.lampboy.meet.2": ["dad", "He gets his feet from me."],
  "egypt.lampboy.saw.1": ["lampboy", "I saw him. I am the only one who saw."],
  "egypt.lampboy.saw.ask": ["dad", "Saw what?"],
  "egypt.lampboy.saw.2": ["lampboy", "A small one came up here with a little sun in his hand."],
  "egypt.lampboy.saw.3": ["lampboy", "He pointed it at the wall, and the wall opened like an eye and took him."],
  "egypt.lampboy.saw.4": ["dad", "A little sun in his hand. That's the flashlight off his key ring."],
  "egypt.lampboy.saw.5a": ["dad", "So it opens for a light. I've got a bigger one than his, back in the trunk."],  // PASS-17E: clearer (where the flashlight is)
  "egypt.lampboy.saw.5b": ["dad", "So it opens for a light. I've got a bigger one than his, right here in my pocket."],
  "egypt.lampboy.saw.5c": ["dad", "A light. I found that out the hard way. Those were good batteries."],
  "egypt.ask.door": ["dad", "What is the humming door?"],                                                                            // kept
  "egypt.lampboy.door.1": ["lampboy", "It is not a door. I know every door in the Horizon, because I light them."],
  "egypt.lampboy.door.2": ["lampboy", "This one opened where the masons put nothing."],
  "egypt.lampboy.door.3": ["dad", "That's the kind my family finds. Every time."],
  "egypt.lampboy.ask.lamps": ["dad", "You look after all these lamps yourself?"],
  "egypt.lampboy.lamps.1": ["lampboy", "Every lamp from here to the top. I fill them before they go hungry."],
  "egypt.lampboy.lamps.2": ["lampboy", "But not today. Today the top ones go hungry, because I am not going up there."],
  "egypt.lampboy.lamps.3": ["dad", "Fair enough, I wouldn't either. I'm going to, but I wouldn't."],
  "egypt.lampboy.ask.bye": ["dad", "Keep the lights on."],
  "egypt.lampboy.bye": ["lampboy", "That is all I do."],
  "egypt.lampboy.sun": ["lampboy", "You brought the sun indoors. It needs no oil, and I do not trust it."],
  "egypt.lampboy.flashlight": ["lampboy", "No, keep your sun. I saw what the small one's did."],
  "egypt.lampboy.dead.1": ["dad", "Here, a little sun of your own. It's out of sun."],
  "egypt.lampboy.dead.2": ["lampboy", "It is a lamp, and lamps I understand. I will fill it."],
  "egypt.lampboy.dead.3": ["dad", "Don't do that. Actually, go ahead and see what happens."],
  "egypt.lampboy.rootbeer": ["lampboy", "It is sweet, and it bites. Do not tell the overseer; he would count it."],
  "egypt.lampboy.sunglasses": ["lampboy", "They put out every lamp at once. I work all day to do the opposite."],
  "egypt.lampboy.chicken": ["lampboy", "What does she eat? Everything I look after goes hungry if I let it."],
  "egypt.lampboy.chicken.2": ["dad", "She's stuffed."],

  // ---------- the two mirrors, and the sunbeam as it grows ----------
  "egypt.foot.set": ["narrator", "Dad wedges the door mirror into the slot. It isn't coming out. Nothing he wedges ever does."],
  "egypt.mirror.nothing": ["narrator", "The mirror has nothing to reflect, like some people Dad has worked with. No sunlight is coming in from outside yet."],
  "egypt.foot.lit": ["narrator", "The sunbeam turns off the mirror and runs up the ramp. It stops dead at the top step, one corner short."],
  "egypt.foot.wrong": ["narrator", "The copper mirror won't wedge into a slot. It wants a flat place to stand, like anybody."],
  "egypt.top.early": ["narrator", "A mirror at the top of a dark ramp would only be decoration. Dad can't see a reason for it yet."],
  "egypt.top.set": ["narrator", "Dad stands the copper mirror on the step and tilts it at the little door. The goldsmith kept it well polished."],
  "egypt.top.dark": ["narrator", "For now it reflects the dark beautifully. The daylight hasn't come this far up the gallery."],
  "egypt.top.lit": ["narrator", "The sunbeam strikes the copper and goes in at the little door. Dad had better go and see what it has found."],
  "egypt.top.wrong": ["narrator", "The door mirror won't stand up on a flat step. It was built to hang off a car door."],
  "egypt.gallery.shade": ["narrator", "There's no sun in here to bounce. All the sunlight is outside, standing around by the stairs."],
  "egypt.beam.in": ["narrator", "A sunbeam comes in through the passage, lands on the bench and stops there, waiting for somebody to turn it."],
  "egypt.beam.up": ["narrator", "The sunbeam strikes Dad's mirror and runs up the ramp. It's the first right turn that mirror has ever shown him."],  // PASS-17E: funnier (pays off "It's shown me every wrong turn I ever made")
  "egypt.relay.done": ["narrator", "Passage, ramp, copper mirror, little door. The sunbeam runs the whole relay."],

  // ================= egypt-chamber: the burial chamber =================

  // ---------- arrival, and the place ----------
  "egypt.chamber.arrive.1": ["dad", "That is a great deal of gold."],
  "egypt.chamber.arrive.2": ["dad", "And a hum, low, like a refrigerator in the next room. There is no next room."],
  "egypt.chamber.walls.look": ["narrator", "Bare red granite, without one picture or one word. Dad was promised walls he could read."],
  "egypt.chamber.walls.look2": ["narrator", "There's no curse over the door. Dad looked, and he's a little let down."],
  "egypt.chamber.door.look": ["narrator", "The little door back to the gallery. Dad has met it already, forehead first."],
  "egypt.chamber.treasure.look": ["narrator", "A gold bed, gold chairs, and a chair to be carried around in. The king packs the way Dad does."],
  "egypt.chamber.treasure.look2": ["narrator", "The bed stands on lion's feet. Dad's stands on a phone book. It's the same idea."],
  "egypt.chamber.treasure.use": ["narrator", "Dad doesn't touch it. He can't get a hotel towel past his conscience."],
  "egypt.chamber.sarc.look": ["narrator", "A stone box the size of a bathtub, with no lid on and nobody in it. Good."],
  "egypt.chamber.sarc.look2": ["narrator", "It's as plain as a workbench. A man with a gold bed has picked a very firm mattress."],
  "egypt.chamber.sarc.use": ["narrator", "Dad isn't getting in. That's a one-way bath."],
  "egypt.chamber.lid.look": ["narrator", "The sarcophagus lid, still roped. Nobody is in a hurry for it, least of all the king."],
  "egypt.chamber.bench.look": ["narrator", "The goldsmith's bench, laid out with small hammers and sheets of gold leaf."],
  "egypt.chamber.brazier.look": ["narrator", "A brazier and a basket of charcoal. It's the first grill Dad has seen all day, and there's nothing on it."],
  "egypt.chamber.mirror.look": ["narrator", "A copper hand mirror on the bench, bright enough to shave in. Dad needs a shave."],
  "egypt.chamber.mirror.use": ["dad", "Mind if I borrow that mirror?"],
  "egypt.goldsmith.mirror.no": ["goldsmith", "Sorrow? Yes, that mirror is a sorrow. I check the gold in it, and it checks my face."],

  // ---------- the goldsmith: he mishears everything ----------
  "egypt.goldsmith.look": ["narrator", "A very old man gilding a box, squinting at the gold as if it were a flashlight in his eyes."],
  "egypt.goldsmith.look2": ["narrator", "The goldsmith is wearing Dad's sunglasses and humming. He's the only thing in here that should be."],
  "egypt.goldsmith.meet.1": ["dad", "Hello there."],
  "egypt.goldsmith.meet.2": ["goldsmith", "A chair? Yes, it is a chair. You have good eyes, and I had those once myself."],
  "egypt.goldsmith.meet.3": ["dad", "This is going to be a long conversation."],
  "egypt.goldsmith.boy.1": ["goldsmith", "A toy? I do not make toys, I make furniture for the king."],
  "egypt.goldsmith.boy.2": ["dad", "A boy. B, O, Y."],
  "egypt.goldsmith.boy.3": ["goldsmith", "Ah, him. He stood where you are standing, and then he did not. I thought he had gone home."],
  "egypt.goldsmith.ask.hum": ["dad", "Doesn't the humming bother you?"],
  "egypt.goldsmith.hum.1": ["goldsmith", "What hum?"],
  "egypt.goldsmith.hum.2": ["goldsmith", "I hear my hammer and nothing else. Fifty years of it, and very restful."],
  "egypt.goldsmith.ask.eyes": ["dad", "Are your eyes all right?"],
  "egypt.goldsmith.eyes.1": ["goldsmith", "Fifty years of gold, all of it shining at me. My eyes are sore."],
  "egypt.goldsmith.eyes.2": ["goldsmith", "I am tired of shining things. That mirror is the worst: it shines, and it shows me my face."],
  "egypt.goldsmith.eyes.3": ["dad", "Tired eyes and too much glare. As it happens, I packed a thing for that."],
  "egypt.goldsmith.eyes.after": ["goldsmith", "Night? Yes, I wear the night on my nose now, and nothing shines at me."],
  "egypt.goldsmith.ask.king": ["dad", "All this for one pharaoh?"],
  "egypt.goldsmith.king.1": ["goldsmith", "It is furniture, and all of it is for the king."],
  "egypt.goldsmith.king.2": ["dad", "Right, the king. One of those."],
  "egypt.goldsmith.ask.bye": ["dad", "Good talking to you."],
  "egypt.goldsmith.bye": ["goldsmith", "Walking? You stood there the whole time, for I saw you."],
  "egypt.goldsmith.trade.1": ["dad", "Try these. They turn the whole world down a notch."],
  "egypt.goldsmith.trade.3": ["goldsmith", "That is kind. The whole world has gone the color of good beer."],
  "egypt.goldsmith.trade.4": ["goldsmith", "I never want to see a shining thing again. Take that mirror away with you."],
  "egypt.goldsmith.trade.5": ["dad", "A copper mirror for drugstore sunglasses. I finally came out ahead on a trade."],
  "egypt.goldsmith.trade.early": ["dad", "What would I do with a mirror? That's never stopped me before."],
  "egypt.goldsmith.rootbeer": ["goldsmith", "Beer? No, that is not beer. Somebody has played a trick on beer."],
  "egypt.goldsmith.flashlight": ["goldsmith", "Put it out. I have enough brightness in here already."],
  "egypt.goldsmith.pass": ["goldsmith", "I am on the list. I have been on it for fifty years."],
  "egypt.goldsmith.carmirror": ["goldsmith", "Another mirror? Is this a joke somebody has sent you to play on me?"],
  "egypt.goldsmith.copper": ["goldsmith", "No, no. It is yours now, so let it shine at you."],
  "egypt.goldsmith.chicken": ["goldsmith", "A medal, in paper and ribbon, and it does not shine. I would hire its maker."],

  // ---------- the wall that hums: the flashlight, and the rule ----------
  "egypt.hum.look": ["narrator", "A bare wall and empty air, and a low hum coming from it. Dad says it's probably the wind."],
  "egypt.hum.look2": ["narrator", "It only opens for light. Dad's son has found the one door in history with a dimmer."],
  "egypt.hum.use": ["narrator", "Dad knocks on the air, like a man at a door from the wrong side. Nobody comes."],
  "egypt.hum.use2": ["narrator", "It wants light, and a lot more of it than Dad carries in his pockets."],
  "egypt.hum.mirror": ["narrator", "Dad shows the wall its own reflection. Nothing happens. It isn't vain, and there's no light in here to throw."],
  "egypt.hum.shade": ["narrator", "Shading the wall from the light would be the opposite of the plan."],
  "egypt.chicken.hum": ["narrator", "Dad holds the General up to the hum. Nothing rattles the General."],
  "egypt.flash.1": ["dad", "A little sun, the boy said. Let's try a medium one."],
  "egypt.flash.1b": ["dad", "A dark room and a strange wall. This is what the flashlight's for."],
  "egypt.hole.look": ["narrator", "A hole opens in the air, the size of a dinner plate. Dad is not the size of a dinner plate."],            // kept
  "egypt.hole.small": ["narrator", "It shrinks as Dad comes closer. He has the same effect on waiters."],                             // kept
  "egypt.flash.dies": ["narrator", "The batteries give out, and the hole closes with them. They were meant to last until the motel."],
  "egypt.flash.son": ["dad", "A key-ring light, a hole in the air, and a boy who can't leave things alone."],
  "egypt.flash.rule.1": ["dad", "So that's the trick. Light opens it. A little light makes a little door."],
  "egypt.flash.rule.2": ["dad", "More light, more door. And there's a whole sun going to waste outside."],
  "egypt.flash.dead": ["narrator", "The flashlight is dead. Dad shakes it, which is everything he knows about batteries."],
  "egypt.goldsmith.flash": ["goldsmith", "Did you say something? Never mind, I would not have heard it."],

  // ---------- the gate ----------
  "egypt.gate.1": ["dad", "Here it comes. Around three corners and in, like it pays rent."],
  "egypt.hole.big": ["narrator", "The hole in the air stands as tall as a man, and holds still in the sunlight. Now that is a door."],                                                                                   // kept
  "egypt.gate.gold": ["goldsmith", "Somebody has let the day in. Well, let it look, for I am wearing the night."],
  "egypt.gate.thanks": ["dad", "Thank You, Lord. A shade, a root beer and two mirrors. I know who did the rest."],
  "egypt.gate.psalm.1": ["dad", "'For a thousand years in thy sight are but as yesterday when it is past, and as a watch in the night.'"],
  "egypt.gate.psalm.2": ["dad", "Moses wrote that one. Show-off."],  // PASS-17E: reference aloud (the design's own sample, cut to fit both ways through)
  "egypt.gate.psalm.4": ["dad", "Either way, a thousand years is yesterday to Him. He knows where my boy is."],
  // (the same moment, when he has heard the scribe's news and knows when he is)
  "egypt.gate.psalm.3b": ["dad", "And he isn't even born yet. I've finally worked out the tenses."],  // PASS-17E: shorter (Moses is named in the line before it now)
  "egypt.gate.psalm.4b": ["dad", "A thousand years is yesterday to Him. He knows right where my boy is."],
  "egypt.hole.go": ["dad", "Hold on, buddy. Dad's taking the next shortcut."],                                                       // kept
  "egypt.hole.wait": ["narrator", "Dad waits at the door. He isn't stepping through until he knows where it comes out. He made that mistake once today."],                             // kept

  // ================= General Feathers, shown to people =================
  // Five of them answer once each, in their own way (Lot, the scribe, the guard, the lamp boy, the goldsmith).
  // For everybody else, and for anybody who has met her already, Dad's stock reply.
  "egypt.chicken.show": ["dad", "This is General Feathers. She's in charge."],
  "egypt.chicken.stock": ["narrator", "Nobody here has ever seen a bird like her. The General takes it well."],

  // ================= carried things =================
  "item.map.look": ["narrator", "A road map of three states. It folds eleven ways, and none of them is the way it came."],                                 // kept
  "item.reed.look": ["narrator", "A reed from the riverbank. The pen of the future, nearly four thousand years ago."],                                       // changed: was "three thousand"
  "item.pass.look": ["narrator", "The scribe's pass, written on the back of Nevada: one supplier of reeds, loud about the shoulders."],
  "item.flashlight.look": ["narrator", "A flashlight, with batteries from two vacations ago. Dad's faith in them is about the same age."],
  "item.rootbeer.look": ["narrator", "A root beer, the only cold thing in the country. It rides in the pocket of Dad's shorts."],
  "item.shade.look": ["narrator", "The windshield shade, bright and shiny on one side. Unlike the map, it folds the way it came."],
  "item.carmirror.look": ["narrator", "The wagon's door mirror. Things in it are closer than they appear, and Dad wishes that worked on home."],
  "item.sunglasses.look": ["narrator", "Drugstore sunglasses. Through them everything looks like late afternoon, Dad's best time of day."],
  "item.coppermirror.look": ["narrator", "A hand mirror of polished copper. In it Dad looks like a penny with a beard."],
  "item.chicken.look": ["narrator", "General Feathers, a stuffed hen with one eye and a medal for bravery. Dad does what she says."],

  // ================= hints: one for each puzzle, in Dad's own voice =================
  "hint.egypt.map": ["dad", "I should check what's still in the wagon."],                                                            // kept
  "hint.egypt.reed": ["dad", "The scribe's pen has split, and a pen here is a reed. There might be one growing down by the river."],                          // changed: was "The scribe lost his pen."
  "hint.egypt.pen": ["dad", "There's a reed in my pocket, and a scribe up the hill who needs a pen."],                                                     // kept
  "hint.egypt.mark": ["dad", "The scribe wants something to draw on. A map is mostly drawing."],                                     // kept (now the hint of "egypt.pass")
  "hint.egypt.inside": ["dad", "I'm on the list, and I've got the pass to prove it. The guard at the stairs should see it."],
  "hint.egypt.witness": ["dad", "Somebody inside the pyramid saw what happened to my boy. I'd try the boy who tends the lamps."],
  "hint.egypt.flash": ["dad", "A little sun in his hand: that's a flashlight, and I packed one. I'll shine it on the wall that hums."],   // FINAL-19: REVIEW-19's patch
  "hint.egypt.shade": ["dad", "The windshield shade can throw sun into the doorway, but somebody has to hold it. The guard's thirsty."],   // FINAL-19: REVIEW-19's patch
  "hint.egypt.carmirror": ["dad", "The sunbeam has to turn a corner at the foot of the gallery. The car has a mirror it isn't using."],
  "hint.egypt.trade": ["dad", "The goldsmith has a mirror he's sick of, and eyes too tired for it. I packed sunglasses."],
  "hint.egypt.topmirror": ["dad", "The copper mirror goes on the top step, facing the little door. One more corner, and the light's in."],  // PASS-17E: his own voice (the same clue)
  "hint.egypt.leave": ["dad", "The door's holding still now. Time to go through it."],                                              // kept
};
