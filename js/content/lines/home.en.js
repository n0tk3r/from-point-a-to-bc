// Act Three: home, that evening. Mom, Big Sister and Little Sister, in five rooms of the house.
//   "line.id": ["who", "What they say."]
// docs/CHARACTERS.md says how each of them talks, and how the family's faith is written. Three rules from it:
//   every fact Big Sister or Mom states is true (the tables are in that file);
//   Scripture in quotation marks is the King James Version, exact and brief; its reference is in that file's table,
//   and is said aloud only where it is natural: by Big Sister, who footnotes everything (PASS-17H: the author's rule
//   of 16 October; Mom and Little Sister no longer read a reference aloud);
//   no hymn, song, poem or play is quoted: a hymn may be named.
// PASS-17H: the dialogue pass of round seventeen. Mom talks to her daughters as their mother (contractions, no "shall",
// fewer "darling"s); "A matter of record" is a gag three times in the act (home.sign.mom.2, home.timeline.2,
// home.talk.landing.bigsis.mom.2b); every changed line is marked, and work-17-passH/changes.json has each before and after.
// A line in quotation marks is somebody's recorded voice (Dad's voicemail and his message, the Son's door alarm)
// or something read out.
//
// Lines kept word for word from the first version of the act have their old ids. Where a thing has moved, its
// lines went with it: `home.pc.*` and `home.note.*` are now said in the study, `home.books.*` at Big Sister's
// bookcase upstairs (Mom's bookcase in the living room is `home.shelf.*`), and `home.photo.*` at the photographs
// on the stair wall.

export const lines = {
  // =====================================================================================================
  // THE OPENING (the living room)
  // =====================================================================================================
  "home.arrive.vm1": ["dad", "You've reached Dad. I can't come to the phone, so I'm either driving or lost."],
  "home.arrive.vm2": ["dad", "And I'm never lost, so I must be driving. Leave a message."],
  "home.arrive.1": ["mom", "Voicemail again. That's nine times, and I'd meant to stop worrying at eight."],
  "home.arrive.2": ["lilsis", "Daddy's not lost. Daddy's EARLY."],
  "home.arrive.2b": ["bigsis", "That's not what early means."],
  "home.arrive.3": ["bigsis", "They left at noon for a four-hour drive, and it's nine forty. That's not a shortcut. It's an expedition."],   // PASS-19H1: shorter; punch last (her figures are the joke)
  "home.arrive.4": ["mom", "Dinner was at six. I set five places, and I am not clearing two of them away."],
  "home.arrive.pray.1": ["mom", "First things first, girls. Come here, both of you."],
  "home.arrive.pray.2": ["mom", "Father, You know where they are tonight, and I do not. Keep them."],
  "home.arrive.pray.3": ["mom", "And bring us to them, wherever that turns out to be. In Jesus' name."],
  "home.arrive.pray.4": ["lilsis", "And please make Daddy ask for directions. Just ONE time. Amen."],
  "home.arrive.pray.5": ["mom", "Amen."],
  "home.arrive.5": ["bigsis", "Dad's phone tells the family computer where it is. The computer's up in his study."],   // PASS-19H1: shorter
  "home.arrive.6": ["lilsis", "Then the computer knows where Daddy is. Somebody should go and ask it."],   // PASS-19H1: emphasis (one exclamation)
  "home.arrive.6b": ["bigsis", "It can't tell us. The internet's been down ever since Dad 'improved' the wiring."],   // PASS-19H1: shorter; punch last
  "home.pc.router": ["mom", "The router's in the closet under the stairs. Your father keeps the internet next to the vacuum."],
  "home.arrive.7": ["mom", "Places, girls. That phone was last seen somewhere, and we're going to find out where."],   // PASS-19H1: spoken; shorter

  // =====================================================================================================
  // THE LIVING ROOM
  // =====================================================================================================
  "home.upstairs.mom": ["narrator", "The landing upstairs, with the bedrooms and Dad's study. The study is the locked one; he says the lock keeps the surprises in."],   // PASS-19H1: shorter
  "home.upstairs.bigsis": ["narrator", "The landing upstairs. Four rooms open off it, and Big Sister would like it noted that exactly one of them is tidy."],   // PASS-19H1: shorter; punch last; one idea
  "home.upstairs.lilsis": ["narrator", "The landing upstairs. Little Sister's fort is up there, under a sign that says 'No Big Sisters' and means it."],   // PASS-19H1: shorter; emphasis; one idea

  "home.window.mom": ["narrator", "The stair window looks out on an empty street. Mom has checked it for headlights eleven times, and this makes twelve."],
  "home.window.bigsis": ["narrator", "The street outside is dark and still. Big Sister decides it is the wrong kind of quiet, and saves the phrase for her novel."],   // PASS-19H1: her whole words; shorter
  "home.window.lilsis": ["narrator", "No car in the street yet. Little Sister has been on car watch since dinner, and has hardly blinked."],   // PASS-19H1: shorter; punch last
  "home.photo.mom": ["narrator", "Family photographs, with the lake trip at the top. Dad took a shortcut that day, and they saw a great deal of lake."],   // PASS-19H1: shorter; one idea
  "home.photo.bigsis": ["narrator", "Family photographs. For the one at the lake, Dad set the timer and ran. He is the blur."],   // PASS-19H1: shorter; one idea
  "home.photo.lilsis": ["narrator", "Family photographs. Little Sister was six at the lake, and is now a whole number bigger."],   // PASS-19H1: emphasis; shorter; one idea
  "home.stairs.mom": ["narrator", "The stairs up to the landing and the bedrooms. Nobody is going up to bed tonight, Mom least of all."],   // PASS-19H1: spoken
  "home.stairs.bigsis": ["narrator", "Sixteen steps up to the landing. Big Sister counted them in fours, for calm, and it didn't help."],   // PASS-19H1: shorter; her whole words; one idea
  "home.stairs.lilsis": ["narrator", "The stairs up to bed. Little Sister is not tired, has never been tired, and would like to know what time it is."],

  // ---- chain B: the closet under the stairs
  "home.closet.look.mom": ["narrator", "The closet under the stairs, where the router lives. Its door opens four inches and not a whisker more."],
  "home.closet.look.bigsis": ["narrator", "The closet door sticks at four inches. Big Sister is wider than four inches; she has shoulders."],
  "home.closet.look.lilsis": ["narrator", "A tiny red light glows at the back of the closet. That is the internet, and Little Sister is surprised how small it is."],
  "home.closet.use.mom": ["narrator", "The gap is four inches wide, and Mom is not. Squeezing into closets is a job for the seven-year-old of the family."],
  "home.closet.use.bigsis": ["narrator", "Big Sister looks into the dark gap and declines. It is narrow, it has spiders, and her little sister is the one who fits."],
  "home.closet.go.1": ["lilsis", "I FIT!"],
  "home.closet.dark.1": ["lilsis", "It's so dark in here. I can't find the plug, but my nose found the vacuum."],
  "home.closet.dark.2": ["lilsis", "I need my pink flashlight. It's up in my fort, and I'm the only one who goes in there."],
  "home.closet.dark.3": ["mom", "Then up you go for it. That fort admits exactly one person."],
  "home.closet.needflash": ["lilsis", "I'm not scared. I'm brave-scared, and brave-scared people bring a flashlight."],
  "home.closet.lent": ["lilsis", "I need my flashlight back first, please. Going in the closet is my job."],
  "home.closet.dead": ["lilsis", "A dead flashlight is just a pink stick. It needs batteries before I go in."],
  "home.closet.go.2": ["lilsis", "Hi, vacuum. Hi, spiders. There's a plug down here that isn't plugged into anything at all."],
  "home.closet.go.3": ["mom", "Into the wall, darling. It's the socket with the surprised face."],
  "home.closet.go.4": ["lilsis", "The red light went green! I fixed the internet, so I'm a engineer."],
  "home.closet.go.5": ["bigsis", "An engineer."],
  "home.closet.go.6": ["lilsis", "That's what I said."],
  "home.closet.again": ["narrator", "The router's little light is a steady green. Little Sister fixed it, and green means she's good at it."],
  "home.closet.done.mom": ["narrator", "One small green light at the back of the closet. Mom has never been so glad to see one."],
  "home.closet.done.bigsis": ["narrator", "The router's light is green. Big Sister expects to hear about it from her sister every day for a week."],
  "home.closet.key.mom": ["narrator", "The closet has no lock for the key to fit. Nothing in there has ever wanted to get out."],   // PASS-17H: Mom's formality; one darling fewer
  "home.closet.key.bigsis": ["narrator", "The closet doesn't lock, it only sticks. Dad maintains that this is a feature."],
  "home.closet.key.lilsis": ["narrator", "There's no keyhole. It's just a door that is bad at being a door."],

  // ---- Mom's bookcase, the kitchen, the Preamble, the clock
  "home.shelf.mom": ["narrator", "Mom's bookcase: the Adams letters, Washington, Franklin, the hymnal, and more plays than one shelf ought to hold."],
  "home.shelf.mom2": ["mom", "In March 1776 Abigail Adams wrote to John, 'Remember the Ladies.' I do like her."],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.shelf.bigsis": ["narrator", "Mom's bookcase, mostly the Founders. She reads them the way other people read thrillers, and has been known to gasp."],
  "home.shelf.lilsis": ["narrator", "Mom's books. Little Sister has checked every one of them for pictures, and found a single man in a wig."],
  "home.kitchen.mom": ["narrator", "The kitchen light is on. Mom always leaves it for whoever is last home, and tonight it's on for two."],   // PASS-19H1: shorter
  "home.kitchen.bigsis": ["narrator", "The kitchen, where Mom has made four pots of tea since six o'clock. Even the kettle has started to look worried."],   // PASS-19H1: shorter; punch last; one idea
  "home.kitchen.lilsis": ["narrator", "The kitchen. Little Sister's hen guards the snacks in there, and to her it is always a little bit snack time."],   // PASS-19H1: shorter; emphasis
  "home.frame.mom": ["narrator", "'We the People', framed: the Constitution, signed in Philadelphia on 17 September 1787. It still gives Mom goosebumps."],   // PASS-19H1: shorter (the fact's figures stay)
  "home.frame.bigsis": ["narrator", "The opening of the Constitution, framed. Mom recites the Preamble every Fourth of July, with gestures."],   // PASS-19H1: shorter; punch last; one idea
  "home.frame.lilsis": ["narrator", "'We the People', in a frame. The letters start out giant and curly, and then they get tired."],   // PASS-19H1: emphasis; punch last
  "home.clock.mom": ["narrator", "The clock says nine forty. That makes them five hours and forty minutes late, and Mom has stopped rounding."],   // PASS-19H1: shorter; one idea
  "home.clock.bigsis": ["narrator", "The living-room clock. Mom says it ticks flat. Big Sister has listened hard, and can't hear it."],   // PASS-19H1: one idea
  "home.clock.lilsis": ["narrator", "The clock. It is three fingers past Little Sister's bedtime, and she would rather nobody mentioned it."],   // PASS-19H1: shorter; emphasis

  // ---- chain A: the piano, and the key that is in it
  "home.piano.look.mom": ["narrator", "Mom's piano. Big Sister plays it better than she does now, which was always the plan."],   // PASS-19H1: shorter; punch last; one idea
  "home.piano.look.bigsis": ["narrator", "The family piano. Bartolomeo Cristofori built the first one, in Florence, around 1700."],   // PASS-19H1: shorter; 'Fun fact' rationed (the fact's figures stay)
  "home.piano.look.bigsis2": ["bigsis", "They called it a harpsichord with soft and loud. I'd have called it a miracle."],   // PASS-19H1: shorter
  "home.piano.look.lilsis": ["narrator", "The piano. Little Sister has made up one whole song on it, and it is short and loud."],   // PASS-19H1: emphasis; shorter; one idea
  "home.piano.key.mom": ["narrator", "The study key is somewhere inside Mom's piano. Knowing that has not brought it an inch closer to her."],   // PASS-19H1: shorter
  "home.piano.key.bigsis": ["narrator", "The key is lying under the A above middle C. Big Sister can hear exactly where, and wishes she couldn't."],   // PASS-19H1: shorter; one idea
  "home.piano.key.lilsis": ["narrator", "There's a key inside the piano, and Little Sister fits under everything. She'd like everybody to stand back."],   // PASS-19H1: emphasis; shorter
  "home.piano.use.mom": ["mom", "'A Mighty Fortress Is Our God.' One verse of Luther's hymn, quietly, for courage."],   // PASS-17H: shorter; the hymn's author without the label
  "home.piano.use.mom2": ["mom", "'God is our refuge and strength, a very present help in trouble.' Very present."],   // PASS-19H1: shorter; faith natural (the quotation stays)
  "home.piano.use.mom3": ["mom", "Once more, then. It's a hymn that doesn't mind being needed."],   // PASS-17H: Mom's formality
  "home.piano.use.bigsis": ["narrator", "Big Sister plays something slow, in a minor key. Under the circumstances, it seems right."],
  "home.piano.use.bigsis2": ["narrator", "Big Sister plays it again. The loud one Dad likes is being saved for when he's home, and then she'll play it twice."],
  "home.piano.use.lilsis": ["narrator", "Little Sister plays her song, which is one note long and very loud. It is called 'Plonk'."],
  "home.thunk.bigsis.1": ["bigsis", "The A above middle C just went 'thunk'. This piano doesn't go 'thunk'."],   // PASS-19H1: shorter; one idea
  "home.thunk.bigsis.2": ["bigsis", "Something's lying on the hammers. Something small, and metal."],
  "home.thunk.mom.react": ["mom", "In my piano. Somebody put it there, and I know which somebody."],   // PASS-19H1: shorter; punch last
  "home.thunk.mom.1": ["mom", "One dead note, the A above middle C. That isn't the piano, and it certainly isn't me."],   // PASS-19H1: one idea
  "home.thunk.mom.2": ["mom", "Somebody's dropped something into my piano, and he's going to hear about it."],   // PASS-19H1: shorter; one idea
  "home.thunk.bigsis.react": ["bigsis", "It's small and metal, by the sound. I can tell you which hammer it's on."],   // PASS-19H1: shorter; one idea
  "home.key.mom.1": ["mom", "With the lid up I can see it. It's a door key, lying on the hammers as if it lived there."],   // PASS-19H1: one idea
  "home.key.mom.2": ["mom", "And I can't reach it. My arms are a civilized length."],
  "home.key.mom.2.b": ["lilsis", "My arms aren't civilized at all."],   // PASS-19H1: new; a turn: three boxes by one speaker broken
  "home.key.mom.3": ["mom", "The panel down by the pedals lifts off. That's your cue."],   // PASS-19H1: shorter
  "home.key.bigsis.1": ["bigsis", "It's under the A above middle C. I can hear exactly where."],   // PASS-19H1: shorter; one idea
  "home.key.bigsis.2": ["bigsis", "But I'm not putting my arm inside a piano. I'm halfway through a sonata."],   // PASS-19H1: shorter; punch last
  "home.key.get.1": ["lilsis", "There's a little wall down here, and it comes off."],   // PASS-19H1: emphasis; shorter
  "home.key.get.2": ["lilsis", "It's all dusty in here. There's a marble, and a penny, and a key!"],
  "home.key.get.3": ["mom", "The study key, tagged 'TRIP HQ'. He hid it, and then he labeled it. That's your father."],   // PASS-19H1: shorter; punch last; one idea
  "home.key.get.4": ["bigsis", "And not one string knocked out of tune. That's pure luck, and I'll take it."],   // PASS-19H1: shorter (one 'For the record' an act scene)
  "home.key.get.5": ["lilsis", "I'm keeping the marble."],
  "home.piano.keyback.mom": ["narrator", "The key has spent quite long enough in Mom's piano. It stays out."],
  "home.piano.keyback.bigsis": ["narrator", "Putting the key back in the piano would be historically accurate, and no use to anyone."],   // PASS-19H1: shorter
  "home.piano.keyback.lilsis": ["narrator", "Little Sister has only just got that key out of the piano. It is not going back in."],   // PASS-19H1: shorter; emphasis

  // ---- the gate: the front door, and the sampler over it
  "home.door.look.mom": ["narrator", "The front door. Its bell rings a quarter-tone flat, like Dad when he sings, and Mom is fond of both."],   // PASS-19H1: shorter (its words stay); one idea
  "home.door.look.bigsis": ["narrator", "The front door. Two coats are missing from the hooks beside it. Big Sister notices hooks."],   // PASS-19H1: shorter; one idea
  "home.door.look.lilsis": ["narrator", "The front door. Little Sister is watching it and the window at the same time, one eye each."],   // PASS-19H1: emphasis
  "home.door.early.mom": ["narrator", "Mom won't open that door until they know where they're going. Somebody in this family has to know."],   // PASS-19H1: spoken
  "home.door.early.bigsis": ["narrator", "They have no destination yet. A journey without one, Big Sister points out, is just Dad."],   // PASS-19H1: her whole words; shorter
  "home.door.early.lilsis": ["narrator", "Little Sister has been ready to go since dinner. Nobody knows yet which way Dad went."],   // PASS-19H1: shorter; emphasis
  "home.door.message.mom": ["narrator", "Not yet. There is a message on Dad's answering machine, and Mom wants to hear it before they go anywhere."],   // PASS-19H1: shorter
  "home.door.message.bigsis": ["narrator", "There is one new message on Dad's machine in the study. Big Sister isn't leaving the house with it still blinking."],   // PASS-19H1: shorter; concrete
  "home.door.message.lilsis": ["narrator", "The blinking machine in the study has a message on it. Little Sister is nearly sure it's from Dad."],   // PASS-19H1: emphasis
  "home.door.nokey.mom": ["narrator", "They know where to go, and they have heard his message. What they haven't got is a car key."],   // PASS-19H1: shorter
  "home.door.nokey.bigsis": ["narrator", "A destination and a message, but no car key. Two out of three, Big Sister notes, does not start a car."],   // PASS-19H1: shorter
  "home.door.nokey.lilsis": ["narrator", "There is no car key yet. Little Sister offers to push the car instead, being mighty."],   // PASS-19H1: emphasis; shorter
  "home.door.keys.1": ["mom", "My car keys left this morning, in your father's pocket."],   // PASS-19H1: shorter; one idea
  "home.door.keys.2": ["bigsis", "There's a spare in the 'family vault', in his study. He was very proud of the name."],   // PASS-19H1: shorter
  "home.door.keys.3": ["lilsis", "It's a box with a clicky wheel. Mommy knows all the clicks."],   // PASS-19H1: shorter; emphasis
  "home.door.psalm.1": ["mom", "One moment, girls. Nobody in this family leaves the house without the psalm."],   // PASS-19H1: shorter
  "home.door.psalm.2": ["bigsis", "Psalm 121, verse 8. She always does this part."],   // PASS-17H: the reference is Big Sister's to say; a beat for her sister
  "home.door.psalm.3": ["lilsis", "'The LORD shall preserve thy going out and thy coming in from this time forth, and even for evermore.'"],
  "home.door.psalm.4": ["mom", "Amen. Going out, and coming in. All five of us."],
  "home.leave.1": ["mom", "Coats, girls. We're going to Nevada."],
  "home.leave.2": ["bigsis", "I'll bring the atlas, a book, and a second book in case the first one ends."],   // PASS-19H1: her whole words; shorter; three, the best last
  "home.leave.3": ["lilsis", "I'll get my boots. Oh, I'm already wearing my boots."],   // PASS-19H1: emphasis (one exclamation)
  "home.leave.4": ["mom", "We are going to be perfectly polite, and completely impossible to get rid of."],
  "home.door.studykey.mom": ["narrator", "That is the study key. The front door is waiting for a car key, and a car to go with it."],   // PASS-19H1: shorter
  "home.door.studykey.bigsis": ["narrator", "The study key opens Dad's study, upstairs. It does nothing at all for the front door."],   // PASS-19H1: shorter; one idea
  "home.door.studykey.lilsis": ["narrator", "The key doesn't fit the front door. Dad's key is for Dad's door."],   // PASS-19H1: emphasis
  "home.sampler.mom": ["mom", "'...as for me and my house, we will serve the LORD.' We hung it before we hung the curtains."],   // PASS-19H1: shorter (the quotation stays)
  "home.sampler.bigsis": ["narrator", "The sampler over the front door. Big Sister measured every letter of it when she was nine, on a rainy day."],   // PASS-19H1: shorter; one idea
  "home.sampler.lilsis": ["narrator", "The sampler over the front door. Mom let Little Sister put in one stitch, and it is the wobbly one."],   // PASS-19H1: shorter; emphasis; one idea
  "home.coats.mom": ["narrator", "The coat hooks, two of them empty. Dad wore his other hat today, and Mom has opinions about the other hat."],   // PASS-19H1: spoken; shorter
  "home.coats.bigsis": ["narrator", "The coat hooks. Big Sister's coat is hung up by its loop, and she wishes that to be clear."],   // PASS-19H1: shorter; one idea
  "home.coats.lilsis": ["narrator", "The coat hooks. Dad's big coat went on the trip, with Dad in it."],   // PASS-19H1: emphasis; shorter

  // ---- Dad's armchair, his crossword and his pencil; the dinner table and the Bible
  "home.chair.mom": ["narrator", "Dad's armchair. It has kept his shape, and tonight Mom rather likes that."],   // PASS-19H1: spoken; shorter
  "home.chair.bigsis": ["narrator", "Dad's armchair, with his reading lamp beside it. Big Sister notes that nobody has sat in it all evening."],   // PASS-19H1: her whole words; shorter
  "home.chair.lilsis": ["narrator", "Dad's chair. Anyone who sits in it has to say 'well, well, well', the way he does."],
  "home.crossword.mom": ["narrator", "Dad's crossword, half done. It can wait up for him tonight, like the rest of the family."],   // PASS-19H1: shorter
  "home.crossword.bigsis": ["narrator", "Dad's crossword. Seven across is wrong, and written in pencil. He uses ink when he's sure, so he knew."],   // PASS-19H1: shorter; punch last
  "home.crossword.lilsis": ["narrator", "Dad's crossword. Little Sister does the three-letter ones for him, always with 'hen'. It's right more often than anyone expects."],   // PASS-19H1: shorter
  "home.pencil.look.mom": ["narrator", "Dad's pencil, on his crossword. It is the one pencil in the house that is always exactly where it should be."],   // PASS-19H1: shorter
  "home.pencil.look.bigsis": ["narrator", "An ordinary wooden pencil with a great many tooth marks. Dad thinks with his teeth."],   // PASS-19H1: shorter
  "home.pencil.look.lilsis": ["narrator", "Dad's pencil. He bites it when he thinks, so it is a very thought-about pencil."],   // PASS-19H1: emphasis
  "home.pencil.take.mom": ["narrator", "Mom borrows the pencil. Dad is welcome to come home and ask for it back."],   // PASS-19H1: shorter; punch last
  "home.pencil.take.bigsis": ["narrator", "Big Sister takes the pencil. She'll return it sharpened, and he will never notice."],   // PASS-19H1: shorter; one idea
  "home.pencil.take.lilsis": ["narrator", "Little Sister takes Dad's pencil. The tooth marks on it are not hers, mostly."],   // PASS-19H1: shorter; emphasis
  "home.table.mom": ["narrator", "The table, set for five. Pot roast was at six o'clock sharp, and it is no longer sharp."],
  "home.table.bigsis": ["narrator", "The table is set for five, and the house is not. Big Sister keeps the sentence for her novel."],
  "home.table.lilsis": ["narrator", "Five places, and two plates gone cold. Little Sister wonders about Dad's potatoes, since he isn't using them."],
  "home.bible.mom": ["mom", "'My help cometh from the LORD, which made heaven and earth.' He read us that this morning."],   // PASS-19H1: shorter (the quotation stays); FINAL-19: the lead's line
  "home.bible.bigsis": ["bigsis", "Psalm 121, where Dad left it. 'I will lift up mine eyes unto the hills, from whence cometh my help.'"],   // PASS-19H1: shorter (the quotation stays); FINAL-19: the lead's line
  "home.bible.lilsis": ["lilsis", "'The LORD is my shepherd; I shall not want.' ...I do want Daddy, though."],   // PASS-19H1: shorter; faith natural (the quotation stays)

  // ---- what they say to each other in the living room
  "home.talk.mom.bigsis.key.a": ["mom", "You can hear which note it's under. Couldn't you just reach in and fish it out?"],   // PASS-17H: Mom's formality; one darling fewer
  "home.talk.mom.bigsis.key.b": ["bigsis", "It's a piano, Mom, not a mailbox. You want the one of us who fits under things."],   // PASS-19H1: shorter
  "home.talk.batt.mom.bigsis.a": ["mom", "Your sister's flashlight needs batteries, and I suspect you know where some are."],
  "home.talk.batt.mom.bigsis.b": ["bigsis", "I know where every battery in this house is. That's what hurts."],
  "home.talk.batt.lilsis.bigsis.a": ["lilsis", "Your music box has batteries in it. I've seen them, so don't pretend."],
  "home.talk.batt.lilsis.bigsis.b": ["bigsis", "It's a sound machine, not a music box. And yes. I'd hoped nobody would mention it."],
  "home.talk.batt.mom.lilsis.a": ["mom", "Batteries in one place, a flashlight in another. I think they should be introduced, don't you?"],
  "home.talk.batt.mom.lilsis.b": ["lilsis", "Give them to me. I've got two hands and a pocket, and that's three places to put things."],
  "home.talk.mom.bigsis.1a": ["mom", "You've gone very quiet. With you, that usually means the wheels are turning."],
  "home.talk.mom.bigsis.1b": ["bigsis", "I'm thinking. It only looks quiet from the outside; inside, it's very loud."],
  "home.talk.mom.bigsis.2a": ["mom", "Whatever's happened to them, we'll handle it the way we handle everything in this house."],   // PASS-19H1: shorter
  "home.talk.mom.bigsis.2b": ["bigsis", "With a list?"],
  "home.talk.mom.bigsis.2c": ["mom", "With a list."],
  "home.talk.mom.lilsis.dark.a": ["mom", "Your flashlight's up in your fort. Will you run and get it? Mind the stairs."],   // PASS-19H1: shorter
  "home.talk.mom.lilsis.dark.b": ["lilsis", "I'm already going. And there's nothing secret in my fort, so nobody look."],   // PASS-19H1: shorter; emphasis; punch last
  "home.talk.mom.lilsis.1a": ["mom", "Are you frightened? You can tell me if you are."],
  "home.talk.mom.lilsis.1b": ["lilsis", "No! Are you?"],
  "home.talk.mom.lilsis.1c": ["mom", "Not while I have you to look after me."],
  "home.talk.mom.lilsis.2a": ["lilsis", "Mommy, why did Daddy take a shortcut? Doesn't he know the regular way?"],
  "home.talk.mom.lilsis.2b": ["mom", "He knows it perfectly well. The long way around has just never once been his idea."],
  "home.talk.bigsis.mom.1a": ["bigsis", "Mom, statistically they're fine. I've run the numbers several times."],
  "home.talk.bigsis.mom.1b": ["mom", "Thank you, darling. And unstatistically?"],
  "home.talk.bigsis.mom.1c": ["bigsis", "Also fine. Probably."],
  "home.talk.bigsis.mom.2a": ["bigsis", "I've started a new chapter. For now it's called 'The Night They Didn't Come Home'."],   // PASS-19H1: her whole words; shorter
  "home.talk.bigsis.mom.2b": ["mom", "Then give it a happy ending. Your father will insist on reading it."],
  "home.talk.bigsis.lilsis.key.a": ["bigsis", "The panel by the pedals lifts off, and you're the only one of us who fits under there."],   // PASS-19H1: shorter
  "home.talk.bigsis.lilsis.key.b": ["lilsis", "I know. That's where I keep my marble."],   // PASS-19H1: shorter
  "home.talk.bigsis.lilsis.1a": ["bigsis", "Please don't touch anything while I'm thinking. It interrupts the thinking."],   // PASS-19H1: her whole words
  "home.talk.bigsis.lilsis.1b": ["lilsis", "I'm not touching. I'm holding."],
  "home.talk.bigsis.lilsis.2a": ["lilsis", "Why do you know so many years?"],
  "home.talk.bigsis.lilsis.2b": ["bigsis", "Somebody in this family has to. Years don't remember themselves."],   // PASS-19H1: her whole words
  "home.talk.lilsis.mom.1a": ["lilsis", "Mommy, I can help. I'm small but I'm MIGHTY, so point me at something."],
  "home.talk.lilsis.mom.1b": ["mom", "You're the mightiest person I know, my love. Just aim it carefully."],
  "home.talk.lilsis.mom.2a": ["lilsis", "Can I stay up?"],
  "home.talk.lilsis.mom.2b": ["mom", "Tonight, yes."],
  "home.talk.lilsis.mom.2c": ["lilsis", "Now I'm worried."],
  "home.talk.lilsis.mom.3a": ["lilsis", "Mommy, sit down for a minute. I'll do the worrying, I'm really good at it."],   // PASS-19H1: shorter
  "home.talk.lilsis.mom.3b": ["mom", "Five minutes, my love. Then I'll want my worrying back."],   // PASS-17H: Mom's formality ('shall')
  "home.talk.lilsis.bigsis.1a": ["lilsis", "Read me a fact."],
  "home.talk.lilsis.bigsis.1b": ["bigsis", "It's 'tell me a fact'."],   // PASS-19H1: her whole words
  "home.talk.lilsis.bigsis.1c": ["lilsis", "Tell me a read."],
  "home.talk.lilsis.bigsis.2a": ["lilsis", "My tooth is loose. Look at it, it wiggles."],
  "home.talk.lilsis.bigsis.2b": ["bigsis", "I've seen the tooth. Everyone on this street has seen the tooth."],

  // =====================================================================================================
  // THE LANDING
  // =====================================================================================================
  "home.landing.first.1": ["bigsis", "That's Dad's study, the door with the notice on it. It's always locked."],   // PASS-19H1: shorter
  "home.landing.first.2": ["mom", "With your father, there's always a notice."],
  "home.landing.first.3": ["lilsis", "My brother's door says 'No Girls Allowed'. We'll see about that."],   // PASS-19H1: emphasis (a sign read out)

  "home.landing.window.mom": ["narrator", "The moon, in the stair window. The same moon is over them, wherever they are, and Mom finds that unexpectedly useful."],   // PASS-19H1: shorter
  "home.landing.window.bigsis": ["narrator", "A bright moon in the stair window. Bright enough to read by, if a person's mother were to allow it."],   // PASS-19H1: shorter; one idea
  "home.landing.window.lilsis": ["narrator", "The moon in the window. It always follows the family car, so Little Sister reasons it is following Dad right now."],   // PASS-19H1: emphasis; shorter; one idea
  "home.ladder.mom": ["narrator", "The ladder to the attic. Big Sister asked for the attic, and Mom said yes before she had thought about the ladder."],   // PASS-19H1: shorter; punch last
  "home.ladder.bigsis": ["narrator", "The ladder up to the Retreat, Big Sister's attic. Visitors are admitted strictly by appointment."],   // PASS-19H1: shorter; punch last; one idea
  "home.ladder.lilsis": ["narrator", "The ladder to the attic, with a card that says 'The Retreat'. Little Sister's visiting hours up there are short."],   // PASS-19H1: shorter; emphasis; one idea
  "home.landing.photos.mom": ["narrator", "Photographs on the landing, the wedding among them. Dad was forty minutes late to it, and would not ask the way."],   // PASS-19H1: shorter
  "home.landing.photos.bigsis": ["narrator", "Photographs on the landing. Big Sister was a serious baby; in one of them she is frowning at a rattle."],   // PASS-19H1: shorter; one idea
  "home.landing.photos.lilsis": ["narrator", "Photographs. Little Sister with no teeth, then with all her teeth. Soon there will be one with a tooth fewer."],   // PASS-19H1: shorter; emphasis; three, the best last
  "home.hamper.mom": ["narrator", "The laundry hamper. It was empty at noon and is full again, and Mom can only admire the industry."],   // PASS-19H1: shorter; punch last
  "home.hamper.bigsis": ["narrator", "The laundry hamper. Big Sister has no comment to make on the hamper."],
  "home.hamper.lilsis": ["narrator", "The laundry hamper, where the flock goes to be promoted. Corporal Speckle is next in line."],   // PASS-19H1: emphasis; shorter
  "home.lildoor.mom": ["narrator", "Little Sister's door: 'Beware of Chickens'. She asked Mom how to spell 'beware', and Mom didn't ask why."],   // PASS-19H1: explanation cut
  "home.lildoor.bigsis": ["narrator", "Little Sister's door, with stickers, a crayon hen and a warning. Big Sister can confirm that the warning is accurate."],   // PASS-19H1: shorter
  "home.lildoor.lilsis": ["narrator", "Little Sister's own door. She did the letters, the hen and every one of the stickers herself."],   // PASS-19H1: emphasis; shorter
  "home.halltable.mom": ["narrator", "A bowl of keys on the hall table. Every key the family owns is in it, except the two Mom wants tonight."],   // PASS-19H1: shorter
  "home.halltable.bigsis": ["narrator", "The key bowl on the hall table. Three keys nobody can name, and no study key. Big Sister has already looked."],   // PASS-19H1: shorter; one idea
  "home.halltable.lilsis": ["narrator", "The key bowl. Little Sister is not allowed to play pirates with it anymore."],   // PASS-19H1: emphasis; one idea
  "home.halltable.use.mom": ["narrator", "Mom goes through the bowl a third time. The study key is still not in it."],   // PASS-19H1: one idea
  "home.halltable.use.bigsis": ["narrator", "Big Sister sorts through the bowl. Nothing is labeled 'study', which, coming from Dad, is itself a clue."],   // PASS-19H1: shorter; one idea
  "home.halltable.use.lilsis": ["narrator", "Little Sister jingles every key in the bowl. None of them is the study key, but she is helping."],
  "home.countdown.mom": ["narrator", "The countdown to the trip, with a day crossed off at every breakfast. Today's square is the little car."],   // PASS-19H1: shorter
  "home.countdown.bigsis": ["narrator", "The countdown to the trip. Dad crossed off today before it happened, and Big Sister let it stand."],   // PASS-19H1: shorter
  "home.countdown.lilsis": ["narrator", "The countdown chart. The red car at the end is today, and Little Sister is sure Dad is still coming."],   // PASS-19H1: emphasis; shorter
  "home.landing.stairs.mom": ["narrator", "The stairs down to the living room. Mom has carried all three children up them asleep, when they were a great deal lighter."],   // PASS-19H1: shorter
  "home.landing.stairs.bigsis": ["narrator", "The same sixteen steps, going down. Big Sister checked on the way up."],   // PASS-19H1: shorter; one idea
  "home.landing.stairs.lilsis": ["narrator", "The stairs down. Little Sister can do them two at a time, and Mom has asked her not to."],   // PASS-19H1: emphasis; shorter; one idea
  "home.rail.mom": ["narrator", "From up here the living room looks like a lit set, waiting. Two of the cast are late for their entrance."],   // PASS-19H1: shorter
  "home.rail.bigsis": ["narrator", "The living room below, with two empty chairs at the table. To Big Sister it looks like a sentence missing two words."],   // PASS-19H1: shorter
  "home.rail.lilsis": ["narrator", "From the rail Little Sister can see the piano, the rug and the front door. The door is still shut."],   // PASS-19H1: emphasis; shorter; one idea

  // ---- the Son's door: NO GIRLS ALLOWED, and booby-trapped. Mom does not try it tonight. The first time a sister opens
  // it, his toy alarm (.alarm.1; Little Sister does the password, .2 and .3), a volley of foam darts, the author's line
  // for Big Sister (.trap.bigsis, word for word), Little Sister's say, and Mom's "not tonight" (.alarm.4 to her, .trap.mom
  // to her sister). The second time, the one dart he kept back (.dart). After that nobody tries (.again); and the darts
  // stay on the runner (.after, looking at the door).
  "home.son.look.mom": ["narrator", "The Son's door: 'No Girls Allowed'. He spelled it right this year, and Mom was so proud she nearly obeyed."],   // PASS-19H1: shorter; punch last
  "home.son.look.bigsis": ["narrator", "The Son's door, covered in notices. One of the smaller ones is addressed to Big Sister personally."],   // PASS-19H1: shorter
  "home.son.look.lilsis": ["narrator", "The sign says 'No Girls Allowed'. Little Sister does not count as a girl here, in her view. She is a sister."],   // PASS-19H1: explanation cut; punch last
  "home.son.use.mom": ["mom", "He'd let me in; I'm his mother. But not tonight."],   // PASS-19H1: shorter
  "home.son.use.bigsis": ["bigsis", "I won't guess; it'll be something about snacks. I'll just open the door."],   // PASS-19H1: shorter; one idea
  "home.son.alarm.1": ["son", "'Halt! This is Operation No Girls. What's the password?'"],
  "home.son.alarm.2": ["lilsis", "'The password is: I still want a dog.' I've watched him do it."],   // PASS-19H1: shorter; explanation cut
  "home.son.alarm.3": ["son", "'Password correct. Ten out of ten. You may enter, me.'"],
  "home.son.trap.bigsis": ["bigsis", "I don't want to go in there. The rug is probably booby-trapped."],
  "home.son.trap.lilsis": ["lilsis", "It said 'correct', and then it shot me. It was a good trap, though."],   // PASS-19H1: emphasis; shorter; punch last
  "home.son.trap.lilsis.2": ["lilsis", "He got you. I'm making a sign that says 'No Brothers', except on Saturdays."],   // PASS-19H1: second joke cut; emphasis; punch last
  "home.son.trap.mom": ["mom", "Not tonight, darling. I am not ready to look at that room with nobody in it."],
  "home.son.alarm.4": ["mom", "Not tonight, sweetheart. I am not ready to look at that room with nobody in it."],
  "home.son.alarm.5": ["lilsis", "I'll shut it. He'd want me to shut it."],   // PASS-19H1: filler cut
  "home.son.again": ["narrator", "Mom said not tonight, so the door stays shut. Little Sister is getting good at waiting."],   // PASS-19H1: shorter; one idea
  "home.son.dart.lilsis": ["narrator", "One last dart pops out of the gap. He saved one for his little sister, which she considers less a trap than plain rude."],   // PASS-19H1: emphasis; shorter
  "home.son.dart.bigsis": ["narrator", "One last dart, kept in reserve. Big Sister respects that, and is still not going in."],   // PASS-19H1: one idea
  "home.son.again.bigsis": ["narrator", "Big Sister stands by what she said about the rug. The door stays shut."],
  "home.son.after.mom": ["narrator", "Foam darts lie all over the rug outside the Son's door. Mom is leaving them where they fell; he'll want to count them."],   // PASS-19H1: shorter
  "home.son.after.bigsis": ["narrator", "The Son's door, and his darts on the rug. He will want a full report, and Big Sister intends to call it adequate."],   // PASS-19H1: shorter
  "home.son.after.lilsis": ["narrator", "The Son's darts are all over the rug. Little Sister has declared them evidence, and nobody is to touch them."],   // PASS-19H1: emphasis; one idea
  "home.son.key.mom": ["narrator", "The study key isn't for this door. The Son's door has never had a lock, only opinions."],   // PASS-19H1: shorter; one idea
  "home.son.key.bigsis": ["narrator", "The Son's door has no keyhole. It has a toy alarm and a great deal of confidence."],   // PASS-19H1: shorter
  "home.son.key.lilsis": ["narrator", "No keyhole. The Son's door has a password, which is a key that gets said out loud."],   // PASS-19H1: emphasis
  "home.bag.mom": ["narrator", "The Son's school bag, hanging on its peg. It has never once been there on a school morning."],   // PASS-19H1: shorter
  "home.bag.bigsis": ["narrator", "The Son's school bag. There is a sandwich in it from before the holidays, and Big Sister will not be the one to find it."],   // PASS-19H1: shorter
  "home.bag.lilsis": ["narrator", "The Son's school bag. Little Sister is guarding it, and nobody is to touch it, not even her."],   // PASS-19H1: emphasis; shorter; one idea; FINAL-19: REVIEW-19's patch

  // ---- chain A: Dad's notice, and the study door
  "home.sign.lilsis": ["lilsis", "'Lost your key? It is with the other eighty-eight.' Eighty-eight doors? Somebody big should read this."],   // PASS-19H1: emphasis; shorter; punch last
  "home.sign.bigsis.1": ["bigsis", "'Lost your key? It is with the other eighty-eight.' Eighty-eight what?"],   // PASS-19H1: shorter
  "home.sign.bigsis.2": ["bigsis", "Keys. A piano has eighty-eight keys. The study key is in our piano."],   // PASS-19H1: shorter; 'Fun fact' rationed
  "home.sign.mom.react": ["mom", "He has hidden a key in MY piano. Of all the places in this house."],
  "home.sign.mom.1": ["mom", "'Lost your key? It is with the other eighty-eight.' Oh, my love."],   // PASS-19H1: shorter
  "home.sign.mom.2": ["mom", "A matter of record: a full-size piano has eighty-eight keys. He means my piano."],   // PASS-19H1: shorter; punch last
  "home.sign.bigsis.react": ["bigsis", "Eighty-eight. I was half a second behind you, Mom. Half."],
  "home.sign.thunk.mom": ["narrator", "'The other eighty-eight' are the keys of a piano. So that was the thunk in Mom's piano: his study key."],   // PASS-19H1: shorter
  "home.sign.thunk.bigsis": ["narrator", "'The other eighty-eight' are the keys of a piano. So the study key is what went 'thunk' under the A."],   // PASS-19H1: shorter; punch last
  "home.sign.again.mom": ["narrator", "'Authorized personnel only.' By that, Dad means himself and the boy."],   // PASS-19H1: shorter; one idea
  "home.sign.again.bigsis": ["narrator", "Dad's notice: block capitals and a riddle. For Dad, that is a formal document."],   // PASS-19H1: shorter
  "home.study.look.mom": ["narrator", "The door to Dad's study. It is the one door he locks, and the one they need."],   // PASS-17H: Mom's formality
  "home.study.look.bigsis": ["narrator", "Dad's study: one lock, one notice and no key, in that order."],
  "home.study.look.lilsis": ["narrator", "Dad's room, which is for planning. Little Sister understands planning to be maps and snacks."],
  "home.study.open.mom": ["narrator", "The study door stands open. Mom half expects to find him in there, saying 'well, well, well'."],
  "home.study.open.bigsis": ["narrator", "Trip Headquarters is open. Big Sister counts herself as authorized personnel now."],
  "home.study.open.lilsis": ["narrator", "Dad's study is open. Little Sister has promised not to touch anything, and plans to touch everything."],
  "home.study.locked.mom": ["narrator", "Locked, naturally. Dad has left a notice on the door instead of a key, which is very like him."],   // PASS-17H: Mom's formality
  "home.study.locked.bigsis": ["narrator", "Locked. The notice on the door says where the key is; it just doesn't say it in plain English."],
  "home.study.locked.lilsis": ["narrator", "Locked. Little Sister knocks for Dad to open up, and then remembers he isn't in there."],
  "home.study.theirs.mom.bigsis": ["mom", "Your big sister has the key. Let her do the honors."],
  "home.study.theirs.mom.lilsis": ["mom", "Your little sister has the key. She fetched it, so she turns it."],   // PASS-17H: Mom's formality ('shall')
  "home.study.theirs.bigsis.mom": ["bigsis", "Mom has the key. Technically, she outranks the Management."],
  "home.study.theirs.bigsis.lilsis": ["bigsis", "My sister has the key. I expect she'll sleep with it."],
  "home.study.theirs.lilsis.mom": ["lilsis", "Mommy's got the key! Mommy, do the door."],
  "home.study.theirs.lilsis.bigsis": ["lilsis", "She's got the key, and she's being slow on purpose."],
  "home.study.unlock.mom": ["narrator", "The key turns. 'Authorized personnel only': Mom authorized herself on their wedding day."],
  "home.study.unlock.bigsis": ["narrator", "The key turns. Trip Headquarters is under new management."],
  "home.study.unlock.lilsis": ["narrator", "The key turns. Little Sister has opened Dad's door with the key from the piano."],

  // ---- what they say to each other on the landing
  "home.talk.landing.mom.bigsis.sign.a": ["mom", "Your father's left us a riddle on that notice. You're better at his riddles than I am."],   // PASS-17H: one darling fewer
  "home.talk.landing.mom.bigsis.sign.b": ["bigsis", "There's a number in it, and with Dad a number is never decoration. I'd like to read it again."],   // PASS-19H1: shorter
  "home.talk.landing.mom.bigsis.1a": ["mom", "As a schoolboy, George Washington copied out 110 Rules of Civility."],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.talk.landing.mom.bigsis.1b": ["bigsis", "Is one of them 'Do not hide keys in your wife's piano'?"],
  "home.talk.landing.mom.bigsis.1c": ["mom", "It's implied. Throughout."],   // PASS-17H: Mom's formality
  "home.talk.landing.mom.bigsis.2a": ["mom", "You take after me. It's the nicest thing I can say about either of us."],   // PASS-19H1: shorter; one idea
  "home.talk.landing.mom.bigsis.2b": ["bigsis", "I take after you with footnotes."],
  "home.talk.landing.mom.lilsis.1a": ["lilsis", "Mommy, is my brother scared? Because I'm not."],   // PASS-19H1: shorter
  "home.talk.landing.mom.lilsis.1b": ["mom", "Your brother has never been scared of anything. That's the part that scares me."],   // PASS-19H1: shorter
  "home.talk.landing.mom.lilsis.2a": ["mom", "Hold the rail on the stairs, please."],
  "home.talk.landing.mom.lilsis.2b": ["lilsis", "I AM holding it."],
  "home.talk.landing.mom.lilsis.2c": ["mom", "With a hand."],
  "home.talk.landing.bigsis.mom.1a": ["bigsis", "Mom, when they're back, I intend to be extremely calm about it."],
  "home.talk.landing.bigsis.mom.1b": ["mom", "So do I. We'll be calm together, at some volume."],   // PASS-19H1: shorter; filler cut
  "home.talk.landing.bigsis.mom.2a": ["bigsis", "John Adams and Thomas Jefferson died on the same day: the fourth of July, 1826."],   // PASS-19H1: shorter; 'Fun fact' rationed
  "home.talk.landing.bigsis.mom.2b": ["mom", "Fifty years to the day after the Declaration. A matter of record."],   // PASS-19H1: shorter; punch last
  "home.talk.landing.bigsis.mom.2b.b": ["mom", "And I told you that one."],   // PASS-19H1: new; punch own box
  "home.talk.landing.bigsis.lilsis.1a": ["bigsis", "Don't slide down the banister."],
  "home.talk.landing.bigsis.lilsis.1b": ["lilsis", "I wasn't going to. Now I'm thinking about it."],
  "home.talk.landing.bigsis.lilsis.2a": ["lilsis", "Do you know his password?"],
  "home.talk.landing.bigsis.lilsis.2b": ["bigsis", "I've never asked. A person is entitled to one noisy secret."],   // PASS-19H1: shorter; punch last; one idea
  "home.talk.landing.lilsis.mom.1a": ["lilsis", "Mommy, can I say my bedtime prayer if it isn't bedtime?"],
  "home.talk.landing.lilsis.mom.1b": ["mom", "Any time, my love. He isn't listening for the clock. He's listening for you."],   // PASS-19H1: shorter
  "home.talk.landing.lilsis.mom.2a": ["lilsis", "When Daddy's home, can we have the same dinner? I saved him my potato."],   // PASS-19H1: shorter; emphasis
  "home.talk.landing.lilsis.mom.2b": ["mom", "A fresh one, I think. That one has done its duty."],
  "home.talk.landing.lilsis.bigsis.1a": ["lilsis", "Why doesn't your ladder have stickers?"],
  "home.talk.landing.lilsis.bigsis.1b": ["bigsis", "It has one card. That isn't boring, it's restrained."],   // PASS-19H1: shorter; one idea
  "home.talk.landing.lilsis.bigsis.2a": ["lilsis", "Are you writing this down for your book?"],
  "home.talk.landing.lilsis.bigsis.2b": ["bigsis", "Every word."],
  "home.talk.landing.lilsis.bigsis.2c": ["lilsis", "Write that I was brave."],

  // =====================================================================================================
  // DAD'S STUDY
  // =====================================================================================================
  "home.study.first.1": ["mom", "Trip Headquarters. He hasn't let me dust in here since March."],   // PASS-17H: Mom's formality
  "home.study.first.2": ["bigsis", "That box on the shelves is the 'family vault'. You'll notice it has a label."],
  "home.study.first.3": ["lilsis", "Something's blinking, over there on the drawer thing."],

  // ---- chain C: the family computer, and the note on it
  "home.pc.look.mom": ["narrator", "The family computer. It is nine years old, and it sighs when it is switched on."],
  "home.pc.look.bigsis": ["narrator", "The family computer, which runs the family map. It also runs, technically."],
  "home.pc.look.lilsis": ["narrator", "The family computer. It has a game on it where a cat eats numbers."],
  "home.pc.offline.mom": ["narrator", "The screen says 'No internet'. It worked perfectly well until Dad improved the wiring."],
  "home.pc.offline.bigsis": ["bigsis", "No internet. In October 1969, what became the internet tried to send 'login'. It crashed at 'lo'."],
  "home.pc.offline.bigsis2": ["bigsis", "So this is traditional."],
  "home.pc.offline.lilsis": ["narrator", "The computer says there is no internet. Little Sister doesn't think computers are allowed to say no, and means to tell Mom."],
  "home.pc.login.mom": ["narrator", "The computer wants a password of four numbers. 'Forgot it? Ask Dad,' it says, and Mom would dearly love to."],
  "home.pc.login.bigsis": ["narrator", "Four digits make ten thousand possible passwords. Dad will have written his down somewhere; he always does."],
  "home.pc.login.lilsis": ["narrator", "Little Sister types one, two, three, four. The computer says no again."],
  "home.pc.type.mom": ["narrator", "Mom types the year in: one, nine, two, eight."],
  "home.pc.type.bigsis": ["narrator", "Big Sister types one, nine, two, eight, with all ten fingers."],
  "home.pc.type.lilsis": ["narrator", "Little Sister types one, nine, two, eight, with one finger."],
  "home.pc.question.mom": ["narrator", "The computer has one more question: 'What did you promise on your wedding day?' Mom sighs. He would."],
  "home.pc.question.bigsis": ["narrator", "The computer asks, 'What did you promise on your wedding day?' Big Sister wasn't invited. This one is Mom's."],
  "home.pc.question.lilsis": ["narrator", "The computer is asking about a wedding. Little Sister wasn't born yet, so this one is for Mom."],
  "home.pc.pick.love": ["mom", "To love, honor and cherish."],
  "home.pc.pick.scenic": ["mom", "To always take the scenic route."],
  "home.pc.pick.directions": ["mom", "To never ask for directions."],
  "home.pc.wrong.love": ["mom", "No? We both said that one. I'd hoped he was listening."],
  "home.pc.wrong.scenic": ["mom", "No. That wasn't a promise. That was a warning."],
  "home.pc.right": ["mom", "He promised never to ask for directions. It's the one promise he's always kept."],
  "home.pc.map.1": ["mom", "'Last seen 5:47 p.m. Thirty-seven miles past Last Gas.' That's the middle of Nevada."],
  "home.pc.map.2": ["bigsis", "That's not on the way home. That's not on the way to anywhere."],
  "home.pc.map.six": ["bigsis", "5:47, and his message was at 5:41. Six minutes later, his phone stops."],
  "home.pc.map.3": ["lilsis", "Is Nevada past the mailbox?"],
  "home.pc.map.4": ["mom", "A little past the mailbox, darling. Shoes on. We leave tonight."],
  "home.pc.done.mom": ["narrator", "The map shows one dot in the middle of nothing, thirty-seven miles past Last Gas. Mom has looked at it quite long enough."],
  "home.pc.done.bigsis": ["narrator", "Thirty-seven miles past Last Gas, last seen at 5:47 p.m. Big Sister has it memorized, and couldn't have stopped herself."],
  "home.pc.done.lilsis": ["narrator", "The dot on the map is Dad. Little Sister says hi to the dot."],
  "home.pc.pencil.lilsis": ["narrator", "Little Sister pokes the screen with Dad's pencil. It leaves a small gray dot that wasn't there before."],

  "home.note.look.mom": ["narrator", "A yellow note on the monitor, in Dad's hand: 'Password: the year of the best thing since.' Since what, he doesn't say."],
  "home.note.look.lilsis": ["narrator", "A yellow note stuck on the monitor. It says 'Password', and then more words, with Dad's loopy Ys."],
  "home.note.take.mom": ["narrator", "Mom takes the note off the monitor. Tonight it is the nearest thing to Dad in the house."],
  "home.note.take.lilsis": ["narrator", "Little Sister takes the note and calls it hers. Then she corrects herself: it is evidence."],
  "home.note.solve.1": ["bigsis", "'The year of the best thing since.' Since sliced bread."],
  "home.note.solve.1.b": ["mom", "He said that about the toaster."],
  "home.note.solve.2": ["bigsis", "Sliced bread was first sold on the seventh of July, 1928, in Chillicothe, Missouri."],
  "home.note.solve.3": ["bigsis", "So the password is 1928. Dad, that's so... actually, that's quite good."],

  // ---- chain D: the answering machine, its tape, and Dad's last message
  "home.machine.look.mom": ["narrator", "Dad's answering machine, blinking, with a loop of tape hanging out of it. The tape is meant to be on the inside."],   // PASS-17H: Mom's formality
  "home.machine.look.bigsis": ["narrator", "The answering machine says 'one new message'. A loop of tape hangs out of it like a tongue."],
  "home.machine.look.lilsis": ["narrator", "The answering machine, with its tape hanging out. Little Sister fixed it last week. It was working before she fixed it."],
  "home.machine.ready.mom": ["narrator", "The tape is wound, and the light blinks: one new message. Mom wants to hear it, and doesn't."],   // PASS-17H: the speech that is really an essay
  "home.machine.ready.bigsis": ["narrator", "One new message, and the tape back where it belongs. The button marked 'Play' is the large one."],
  "home.machine.ready.lilsis": ["narrator", "The answering machine has an answer in it now. Little Sister recommends pressing the big button."],
  "home.machine.flash": ["narrator", "Little Sister shines her flashlight into the machine's little window. Two tape reels look back at her like eyes."],
  "home.tape.need.mom": ["narrator", "The tape has to be wound back in. Mom needs a pencil for that: an ordinary wooden one, with some heft to it."],
  "home.tape.need.bigsis": ["narrator", "A pencil in the hub would wind the tape back in. Big Sister's pencils are too slim. Dad's is not."],
  "home.tape.need.lilsis": ["narrator", "The tape needs winding back in with a pencil. Little Sister is not allowed to fix this machine again; Mom said so."],
  "home.tape.where": ["mom", "The only pencil anybody can ever find in this house is the one on his crossword."],   // PASS-17H: Mom's formality
  "home.tape.has.mom": ["mom", "I have his pencil. Stand aside, girls. This is my department."],
  "home.tape.has.bigsis": ["bigsis", "I have Dad's pencil. Mom should do the winding, though. She knows which way it turns."],
  "home.tape.has.lilsis": ["lilsis", "Daddy's pencil is in my pocket, and Mommy needs it. I'll hand it over in a minute."],
  "home.tape.notme.bigsis": ["narrator", "Big Sister has the pencil, but that tape has Dad's voice on it. Mom should be the one to wind it."],
  "home.tape.notme.lilsis": ["narrator", "Little Sister has the pencil, but she fixed this machine last time. The winding is Mom's job."],
  "home.tape.wind.1": ["mom", "I taped whole musicals off the radio on these. Pencil in the hub, and gently."],
  "home.tape.wind.2": ["mom", "There. Every inch of it home again, and not one crease. It only takes patience."],
  "home.tape.wind.3": ["bigsis", "So the knack is going slower than you want to. Noted."],
  "home.tape.wind.4": ["lilsis", "It's still blinking. Can I press it? I'm asking really fast."],
  "home.msg.1": ["dad", "'Hi, honey. It's 5:41 and we're making great time. I found a shortcut.'"],
  "home.msg.2": ["dad", "'Thirty-seven miles past the last gas station, and not one other car.'"],
  "home.msg.2.b": ["son", "'Hi, Mom! Dad, that sign up there looks funny.'"],
  "home.msg.3": ["dad", "'Huh. That is funny.'"],
  "home.msg.4": ["dad", "'That sign just changed its--'"],
  "home.msg.after.lilsis": ["lilsis", "Changed its what? Daddy? Changed its what?"],
  "home.msg.after.bigsis": ["bigsis", "That's the last anybody heard, at 5:41 p.m. I'm writing down the minute."],
  "home.msg.after.bigsis.six": ["bigsis", "5:41 on the tape. 5:47 on the map. Whatever happened took six minutes."],
  "home.msg.after.mom": ["mom", "No need to play it twice. He sounded happy, and very pleased with his shortcut. Let's hold on to that."],
  "home.msg.again.mom": ["narrator", "Once was enough. Mom has every word of the message by heart, down to the 'Huh'."],
  "home.msg.again.bigsis": ["narrator", "The message was left at 5:41 p.m. Big Sister has it memorized, including the hiss at the end."],
  "home.msg.again.lilsis": ["narrator", "The sign changed its what? Little Sister means to ask Dad first thing, before the hug. All right, after the hug."],

  // ---- chain E: the family vault
  "home.vault.read.mom": ["narrator", "'The year We the People got it in writing. Your mother will know. She brings it up.' Mom does not bring it up. Not often."],
  "home.vault.read.bigsis": ["narrator", "'Combination: the year We the People got it in writing.' The label says Mom will know, and Big Sister agrees."],
  "home.vault.read.lilsis": ["narrator", "The label says 'Your mother will know.' Little Sister shouts for Mom: the box says she knows."],
  "home.vault.pick.1776": ["mom", "Seventeen seventy-six."],
  "home.vault.pick.1787": ["mom", "Seventeen eighty-seven."],
  "home.vault.pick.1789": ["mom", "Seventeen eighty-nine."],
  "home.vault.pick.later": ["mom", "Let me think about that a moment longer."],
  "home.vault.wrong.1776": ["mom", "No. 1776 is the Declaration, on the Fourth of July. 'We the People' came later."],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.vault.wrong.1789": ["mom", "No. 1789 is the new government, and General Washington's oath. That's too late."],
  "home.vault.right.1": ["mom", "1787, signed in Philadelphia in September. He does listen. Just not at the time."],
  "home.vault.right.2": ["mom", "My spare car key, two packets of ketchup, and a card: 'Knew you'd know. The Management.'"],
  "home.vault.right.3": ["bigsis", "He keeps ketchup in a vault."],
  "home.vault.right.4": ["lilsis", "Is that the treasure? Daddy wouldn't lock up ketchup unless it was treasure. Can I have it?"],
  "home.vault.right.5": ["mom", "The ketchup stays. I've never asked what he's saving it for, and I'm not starting tonight."],   // PASS-17H: Mom's formality
  "home.vault.done.mom": ["narrator", "The family vault stands open, empty but for Dad's card and his condiments."],   // PASS-17H: Mom's formality
  "home.vault.done.bigsis": ["narrator", "A vault, opened by the Constitution of the United States. Big Sister will be footnoting that."],
  "home.vault.done.lilsis": ["narrator", "The treasure box is open, and Dad's treasure turns out to be ketchup. Little Sister is not even surprised."],
  "home.vault.key.mom": ["narrator", "The vault has no keyhole, only a dial. Dad does like a dial; it lets him be mysterious on a budget."],   // PASS-17H: one darling fewer
  "home.vault.key.bigsis": ["narrator", "A combination lock, and no keyhole. Dad doesn't cheat at his own riddles: the answer will be in the clue on the label."],
  "home.vault.key.lilsis": ["narrator", "There is no hole for a key, just a little wheel that clicks when it turns."],

  // ---- the rest of the study
  "home.wallmap.mom": ["narrator", "Dad's wall map, with the whole route in red wool. One yellow piece strikes off across nothing at all."],
  "home.wallmap.bigsis": ["narrator", "A yellow string on the map follows a road that simply stops. Yellow is the color of caution, and Dad chose it himself."],
  "home.wallmap.lilsis": ["narrator", "The wall map. The red string is Dad driving, and the yellow one is Dad being clever."],
  "home.wallmap.pencil.mom": ["narrator", "Mom won't draw on his map. She will, however, be having a word with him about that yellow string."],   // PASS-17H: Mom's formality ('shall')
  "home.wallmap.pencil.bigsis": ["narrator", "Big Sister isn't going to correct Dad's map. She is going to correct Dad, in person."],
  "home.wallmap.pencil.lilsis": ["narrator", "Little Sister draws a tiny car on the string, with the General in the back window, keeping an eye out."],
  "home.corkboard.mom": ["narrator", "The Son's plan for the trip, pinned to the corkboard. Step one is 'snacks'. So are steps two through five."],
  "home.corkboard.bigsis": ["narrator", "The Son's snack schedule. Every snack is rated out of ten, in advance, before he has tasted a single one."],
  "home.corkboard.lilsis": ["narrator", "The Son's drawing of the trip. He made the luggage taller than the car, and that part is true."],
  "home.shelves.mom": ["narrator", "Dad's shelves, with his manuals. Every one of them has been read precisely as far as the middle."],
  "home.shelves.bigsis": ["narrator", "Jars of screws on Dad's shelves. One is labeled 'Misc'. So are all the others."],
  "home.shelves.lilsis": ["narrator", "Dad's shelves. One of the jars has googly eyes in it, and Little Sister is not saying whose."],
  "home.globe.mom": ["narrator", "Dad's globe. 'Anywhere but the interstate,' he likes to say, and Mom wishes she had taken him at his word."],
  "home.globe.bigsis": ["narrator", "A globe says where a place is. Tonight, to Big Sister, 'where' feels like only half the question."],   // PASS-17H: truer; it plants 'when' without saying it
  "home.globe.lilsis": ["narrator", "The globe opens in the middle. Dad says it is not an egg. Little Sister says it is so an egg."],
  "home.globe.use.mom": ["narrator", "Mom doesn't spin it. Tonight there is only one small corner of the world she cares about."],   // PASS-17H: Mom's formality ('shall')
  "home.globe.use.bigsis": ["narrator", "Big Sister spins the globe. It stops on Nevada every single time; Dad has leaned on it, and not by accident."],
  "home.globe.use.lilsis": ["narrator", "Little Sister spins the globe and stops it with her finger. By her reckoning, Dad is in the ocean."],
  "home.study.window.mom": ["narrator", "The driveway, and the oil spot where the wagon sleeps. Mom will take that up with him too, once he's home."],   // PASS-17H: Mom's formality ('shall')
  "home.study.window.bigsis": ["narrator", "The study window shows the whole street. Big Sister has looked, and it hasn't helped."],
  "home.study.window.lilsis": ["narrator", "The swings look sad in the dark. Little Sister has plans for tomorrow: Dad is going to push her very high."],
  "home.banner.mom": ["narrator", "The trip banner. Dad lettered the word 'Trip', and the Son did the rest, one color a letter."],
  "home.banner.bigsis": ["narrator", "The banner. Dad ruled his letters in pencil and the Son did his freehand. The Son's is the better half."],
  "home.banner.lilsis": ["narrator", "The banner. Little Sister held the tape, and nobody put her name on it. She is adding it later, in pink."],
  "home.plane.mom": ["narrator", "A model biplane, built by Dad and the Son together. It took every clothespin Mom owns."],   // PASS-17H: American: clothespin
  "home.plane.bigsis": ["narrator", "The model biplane hangs by a thread. The thread was Big Sister's condition for sharing a roof with it."],
  "home.plane.lilsis": ["narrator", "The model plane goes round if someone blows on it. Little Sister isn't allowed to blow. She blows a little."],
  "home.boxes.mom": ["narrator", "The things that didn't fit in the car: the tent, the cooler, and the box of maps. He left the maps."],   // PASS-17H: Mom's formality
  "home.boxes.bigsis": ["narrator", "One of the boxes says 'Maps', in Dad's capitals. He walked straight past it."],
  "home.boxes.lilsis": ["narrator", "Boxes left behind, and not one juice box among them. Little Sister and Dad are going to have a talk."],
  "home.study.door.mom": ["narrator", "The study door. Mom is leaving it open; next time he would only hide the key somewhere worse than her piano."],   // PASS-17H: Mom's formality
  "home.study.door.bigsis": ["narrator", "The door back to the landing. Big Sister isn't finished in here, and may never be."],
  "home.study.door.lilsis": ["narrator", "The door they opened with the key Little Sister got out of the piano. She would like the piano part remembered."],

  // ---- what they say to each other in the study
  "home.talk.study.mom.bigsis.note.a": ["mom", "Your father's left us a riddle about a year. Years have always been your department."],
  "home.talk.study.mom.bigsis.note.b": ["bigsis", "Then may I have it, please? I think better with the paper in my hands."],
  "home.talk.study.mom.bigsis.1a": ["mom", "Bach wrote 'S.D.G.' at the end of many of his scores. 'To God alone the glory.'"],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.talk.study.mom.bigsis.1b": ["bigsis", "Dad writes 'The Management' at the end of his."],
  "home.talk.study.mom.bigsis.2a": ["mom", "Your father planned this trip for a month, up here, with your brother at his elbow."],
  "home.talk.study.mom.bigsis.2b": ["bigsis", "And then he took a shortcut."],
  "home.talk.study.mom.bigsis.2c": ["mom", "And then he took a shortcut."],
  "home.talk.study.mom.lilsis.1a": ["mom", "Hands, please."],
  "home.talk.study.mom.lilsis.1b": ["lilsis", "They're in my pockets. Mostly."],
  "home.talk.study.mom.lilsis.2a": ["lilsis", "Mommy, what's a headquarters?"],
  "home.talk.study.mom.lilsis.2b": ["mom", "It's where the plans get made. The mistakes get made on the road."],   // PASS-17H: Mom's formality
  "home.talk.study.bigsis.mom.vault.a": ["bigsis", "Mom, 'the year We the People got it in writing' is your territory. Which year?"],
  "home.talk.study.bigsis.mom.vault.b": ["mom", "The one in the frame on our living-room wall. Leave the dial to me; I know it in my sleep."],   // PASS-17H: Mom's formality ('shall'); one darling fewer
  "home.talk.study.bigsis.mom.dot.a": ["bigsis", "Mother, what if we drive all the way to the dot, and they aren't there?"],
  "home.talk.study.bigsis.mom.dot.b": ["mom", "Then we keep looking. You don't stop the show for a missing cast member. You go and fetch him."],
  "home.talk.study.bigsis.mom.1a": ["bigsis", "Dad calls this computer 'the mainframe'. It isn't a mainframe."],
  "home.talk.study.bigsis.mom.1b": ["mom", "He calls the car 'she', and himself 'the Management'. He has a gift for names."],
  "home.talk.study.bigsis.mom.2a": ["bigsis", "If he'd just written down the route, like a reasonable person..."],
  "home.talk.study.bigsis.mom.2b": ["mom", "Then it wouldn't have been a shortcut. It would have been a plan."],   // PASS-17H: Mom's formality
  "home.talk.study.bigsis.lilsis.1a": ["bigsis", "Don't spin the globe, don't open the jars, and don't fix anything."],
  "home.talk.study.bigsis.lilsis.1b": ["lilsis", "Those are all the good ones."],
  "home.talk.study.bigsis.lilsis.2a": ["lilsis", "What's a mainframe?"],
  "home.talk.study.bigsis.lilsis.2b": ["bigsis", "It's what Dad calls a nine-year-old computer. He means it fondly."],
  "home.talk.study.lilsis.mom.tape.a": ["lilsis", "Mommy, I only fixed the tape machine a little."],
  "home.talk.study.lilsis.mom.tape.b": ["mom", "I can mend it. All I need is one ordinary pencil and a moment's quiet. Mostly the quiet."],
  "home.talk.study.lilsis.mom.1a": ["lilsis", "Is Daddy in trouble?"],
  "home.talk.study.lilsis.mom.1b": ["mom", "A little, my love. He has to come home first. The trouble will keep."],   // PASS-17H: Mom's formality
  "home.talk.study.lilsis.mom.2a": ["lilsis", "Mommy, why does Daddy have so many jars?"],
  "home.talk.study.lilsis.mom.2b": ["mom", "Because he has so many screws. Which is because he has so many jars."],   // PASS-17H: funnier: the answer goes round in a circle; one darling fewer
  "home.talk.study.lilsis.bigsis.1a": ["lilsis", "My tooth's so loose. I told it to wait till Daddy's home, so he can see it come out."],
  "home.talk.study.lilsis.bigsis.1b": ["bigsis", "You're negotiating with a tooth. I wouldn't bet against you."],
  "home.talk.study.lilsis.bigsis.2a": ["lilsis", "If the computer's broken, I can fix it. I fixed the tape machine."],
  "home.talk.study.lilsis.bigsis.2b": ["bigsis", "That's exactly why I'm standing between you and the computer."],

  // =====================================================================================================
  // LITTLE SISTER'S ROOM (it was the girls' room until Big Sister's thirteenth birthday). A kingdom of chickens.
  // =====================================================================================================
  "home.lilroom.first.1": ["lilsis", "Rule one: don't step on the rug. The rug is an egg."],
  "home.lilroom.first.2": ["bigsis", "I used to live in here. It has since been annexed by poultry."],

  "home.lilroom.window.mom": ["narrator", "The window, and the maple outside. Little Sister used to think the maple held up the moon, and Mom never corrected her."],
  "home.lilroom.window.bigsis": ["narrator", "A paper rooster in the window is in charge of the weather. Big Sister has been told his name, twice."],
  "home.lilroom.window.lilsis": ["narrator", "The maple taps on the glass to say hi. Little Sister always says hi back, so that it doesn't feel silly."],
  "home.drawings.mom": ["narrator", "Little Sister's drawings of the family. She drew Dad the biggest of anyone, and he was more pleased than a grown man should be."],   // PASS-19H1: shorter
  "home.drawings.bigsis": ["narrator", "In the drawings the hen has a long and elegant neck, and Big Sister has none at all. She has raised it with the artist."],   // PASS-19H1: shorter; one idea
  "home.drawings.lilsis": ["narrator", "Little Sister's drawings. That is General Feathers on the roof, on lookout, keeping an eye on Dad."],   // PASS-19H1: emphasis; shorter

  // ---- the chickens. Every one has a name and a rank or a job; "Chickens KNOW." is said here for the first time
  "home.chart.mom": ["narrator", "A chart headed 'My Chickens'. The General has a star by her name, and the Admiral is being terribly gracious about it."],   // PASS-19H1: shorter
  "home.chart.bigsis": ["narrator", "The chart of chickens, with every name and rank. Big Sister knows them all; she is quizzed at breakfast, without warning."],   // PASS-19H1: shorter
  "home.chart.lilsis": ["narrator", "The chart of ranks. A chicken goes up one every time it goes through the wash. That is the rule."],   // PASS-19H1: emphasis; shorter
  "home.flock.mom": ["narrator", "The flock, heaped on the beanbag. Mom has washed every one of them at least once, and knows most of their names."],
  "home.flock.bigsis": ["narrator", "The flock: Admiral Doodle on top, then Corporal Speckle, then Private Peep. Big Sister knows every one of them."],
  "home.flock.bigsis.b": ["bigsis", "Against my will."],
  "home.flock.lilsis": ["narrator", "The flock sits very still tonight. Even Admiral Doodle, who is in charge of mornings, has nothing to say."],
  "home.flock.lilsis2": ["lilsis", "They know something's up. They knew before I did. Chickens KNOW."],
  "home.teaparty.mom": ["narrator", "A tea party round a spotted teapot. Mom came to tea last week, and was told afterwards that her manners would do."],   // PASS-19H1: shorter; punch last
  "home.teaparty.bigsis": ["narrator", "The tea party. The tea is water, and the water is from Tuesday. Big Sister regrets checking."],   // PASS-19H1: shorter
  "home.teaparty.lilsis": ["narrator", "The tea party. Nobody drinks until the General gets back. That isn't a rule, it's manners."],   // PASS-19H1: emphasis; shorter; one idea
  "home.coop.mom": ["narrator", "The hen house was a dollhouse once. The dolls were asked to leave, and Mom is told it was amicable."],
  "home.coop.bigsis": ["narrator", "The hen house. Big Sister wired its lights herself, on the understanding that it was for dolls. She was misled."],
  "home.coop.lilsis": ["narrator", "The hen house. Everybody in it is home; Little Sister has checked twice."],
  "home.coop.flash": ["narrator", "Little Sister shines her flashlight into the hen house. Not one hen blinks. They are brave hens."],
  // (Matthew 23:37. Those nine words, and no more of the verse, are quoted.)
  "home.nest.mom": ["mom", "'...even as a hen gathereth her chickens under her wings'..."],   // PASS-17H: reference aloud; the Bible fact tacked on
  "home.nest.mom2": ["mom", "Tonight I know just how the hen feels."],
  "home.nest.bigsis": ["narrator", "A stuffed hen in a cardboard nest, sitting on plastic eggs since March. Big Sister admires her patience, if not her judgment."],
  "home.nest.lilsis": ["narrator", "Henrietta, on the eggs. They are plastic, Little Sister explains, so hatching takes extra long."],

  // ---- her bed, and the place kept on the pillow for General Feathers, who went on the trip in Daddy's suitcase
  "home.lilbed.mom": ["narrator", "Little Sister's bed. It has been jumped on, recently and with conviction."],
  "home.lilbed.bigsis": ["narrator", "Hens on top of the bed, non-hens ranked below. The non-hens were not consulted."],   // PASS-19H1: shorter; one idea
  "home.lilbed.lilsis": ["narrator", "Little Sister's bed, which is for the officers, and for jumping."],   // PASS-19H1: shorter; punch last
  "home.pillow.mom": ["narrator", "A place kept on the pillow, marked 'Reserved'. Mom found the first draft of the General's orders; it said 'Do what she says' twice."],
  "home.pillow.bigsis": ["narrator", "A place on the pillow marked 'Reserved', for a hen with a medal. She outranks Big Sister."],
  "home.pillow.lilsis": ["narrator", "The General's place on the pillow. General Feathers went on the trip in Dad's suitcase, to keep an eye on him."],
  "home.pillow.lilsis2": ["lilsis", "I'm not worried about the General. Daddy's the one who needs supervising."],
  "home.lamp.mom": ["narrator", "The rooster lamp. Little Sister won't sleep without it, and neither, Mom suspects, would the rooster."],   // PASS-19H1: shorter; one idea
  "home.lamp.bigsis": ["narrator", "The rooster lamp. Little Sister stood at the shop window for a week, saying nothing, until it was hers. Big Sister was impressed."],   // PASS-19H1: shorter
  "home.lamp.lilsis": ["narrator", "The rooster lamp stays up all night so that Little Sister doesn't have to. He never even goes to bed."],   // PASS-19H1: emphasis; shorter

  // ---- chain B: the blanket fort, and the flashlight in it, which is dead
  "home.fort.look.mom": ["narrator", "A fort made of every blanket Little Sister owns, with a sign of very firm views. Her pink flashlight is just inside."],   // PASS-17H: American: drying rack
  "home.fort.look.bigsis": ["narrator", "The blanket fort. Its sign says 'No Big Sisters', and there is only one of those in the house."],
  "home.fort.look.lilsis": ["narrator", "Little Sister's fort. It holds her flashlight and a secret, and she isn't telling the secret."],
  "home.fort.empty.mom": ["narrator", "The blanket fort. It is better built than Dad's shelves, and Mom hasn't told either builder."],   // PASS-17H: Mom's formality
  "home.fort.empty.bigsis": ["narrator", "The fort and its sign. Big Sister has never once tried to go in, which is what makes it hurtful."],
  "home.fort.empty.lilsis": ["narrator", "The fort. The secret is still in there. It is a cookie."],
  "home.fort.use.mom": ["narrator", "Mom doesn't go into a lady's fort uninvited; she taught Little Sister that herself. Whatever is in there is hers to fetch."],   // PASS-17H: Mom's formality ('One does not')
  "home.fort.use.bigsis": ["narrator", "Big Sister respects a posted boundary, and wouldn't fit in any case. Only Little Sister goes in there."],
  "home.flashlight.mom": ["narrator", "A pink flashlight, just inside the fort. It is Little Sister's to fetch: her fort, her rule, and a good one."],   // PASS-19H1: shorter
  "home.flashlight.bigsis": ["narrator", "The flashlight lies inside the sign's jurisdiction. Big Sister won't reach past it, not even for a flashlight."],   // PASS-19H1: shorter
  "home.flashlight.lilsis": ["narrator", "Little Sister's pink flashlight. It lives in her fort, for the dark, which is when a flashlight is needed."],   // PASS-19H1: emphasis; shorter; one idea
  "home.fort.take.dark": ["lilsis", "My flashlight! Now the closet can't be dark at me. Hey, why won't it click on?"],
  "home.fort.take.early": ["lilsis", "My flashlight, in case of dark. Hey, why won't it click on?"],
  "home.fort.take.2": ["lilsis", "It's dead. I read to the flock all night, and they wanted the whole book."],
  "home.fort.take.3": ["mom", "Then it needs batteries. I haven't seen that size in this house since Easter."],   // PASS-17H: Mom's formality
  "home.fort.take.4": ["bigsis", "There are four, in my sound machine. Let it be noted that I said so."],
  "home.fort.again": ["narrator", "Little Sister goes into her fort and comes out again. The cookie is all right."],
  "home.fort.putback.mom": ["narrator", "Not yet. Little Sister is going to want that flashlight for the closet under the stairs."],
  "home.fort.putback.bigsis": ["narrator", "Big Sister may not go near that fort. She will hold the flashlight until its owner takes it."],
  "home.fort.putback.lilsis": ["narrator", "Little Sister isn't putting it back. They need it tonight. It can go home afterwards."],
  "home.lilroom.door.mom": ["narrator", "The door to the landing. Mom would usually turn the lights off on the way out. Tonight she leaves them on."],
  "home.lilroom.door.bigsis": ["narrator", "The door to the landing. There is a hen on this side of it as well. Of course there is."],
  "home.lilroom.door.lilsis": ["narrator", "There is a hen on the door, so that the door knows whose door it is."],

  // ---- what they say to each other in Little Sister's room
  "home.talk.lilroom.mom.bigsis.1a": ["mom", "How's the novel?"],   // PASS-17H: Mom's formality
  "home.talk.lilroom.mom.bigsis.1b": ["bigsis", "It acquired a plot this evening. I didn't ask for one."],
  "home.talk.lilroom.mom.bigsis.2a": ["mom", "You shared this room with her once. Do you ever miss it?"],
  "home.talk.lilroom.mom.bigsis.2b": ["bigsis", "I miss the window. I don't miss being counted at bedtime with the flock."],
  "home.talk.lilroom.mom.lilsis.flash.a": ["mom", "Your flashlight's in your fort, and nobody goes in that fort but you."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.mom.lilsis.flash.b": ["lilsis", "I know, I made the rule. I'm already getting it."],
  "home.talk.lilroom.mom.lilsis.1a": ["mom", "Did you say your verse tonight?"],
  "home.talk.lilroom.mom.lilsis.1b": ["lilsis", "Twice. Once for me and once for my brother, because he forgets."],
  "home.talk.lilroom.mom.lilsis.2a": ["lilsis", "Mommy, can Daddy sleep in my fort when he's back?"],
  "home.talk.lilroom.mom.lilsis.2b": ["mom", "He'd be honored, my love. He won't fit, and he'll try anyway."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.bigsis.mom.1a": ["bigsis", "Mom, did you ever want to be on a real stage? A big one, with a curtain?"],
  "home.talk.lilroom.bigsis.mom.1b": ["mom", "I'm on one every day. And nobody ever knows their lines."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.bigsis.mom.2a": ["bigsis", "I've decided what the next chapter's called. 'Places, Girls.'"],
  "home.talk.lilroom.bigsis.mom.2b": ["mom", "I expect a credit."],   // PASS-17H: Mom's formality ('I should like'); funnier
  "home.talk.lilroom.bigsis.lilsis.1a": ["bigsis", "Which one is Corporal Speckle? I've forgotten."],
  "home.talk.lilroom.bigsis.lilsis.1b": ["lilsis", "You have not, you're being nice. It's the speckly one."],
  "home.talk.lilroom.bigsis.lilsis.2a": ["lilsis", "When I'm thirteen, do I get an attic?"],
  "home.talk.lilroom.bigsis.lilsis.2b": ["bigsis", "When you're thirteen I'll be nineteen, and you can have mine."],
  "home.talk.lilroom.bigsis.lilsis.2c": ["lilsis", "I don't want yours. Yours has no chickens."],
  "home.talk.lilroom.lilsis.mom.1a": ["lilsis", "Mommy, look. I made my bed!"],
  "home.talk.lilroom.lilsis.mom.1b": ["mom", "You made a bed, my love. Out of every blanket we own."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.lilsis.mom.2a": ["lilsis", "Is it still today?"],
  "home.talk.lilroom.lilsis.mom.2b": ["mom", "It's still today. It's been today for a very long time."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.lilsis.bigsis.1a": ["lilsis", "Do you want to hold a chicken? It helps."],
  "home.talk.lilroom.lilsis.bigsis.1b": ["bigsis", "The speckled one. Briefly. For morale."],
  "home.talk.lilroom.lilsis.bigsis.2a": ["lilsis", "Is your book about us?"],
  "home.talk.lilroom.lilsis.bigsis.2b": ["bigsis", "It's about a family of five. Any resemblance is entirely the point."],

  // =====================================================================================================
  // THE RETREAT: Big Sister's attic. Soft light, one sound, three rules. (Up here Little Sister whispers at full volume.)
  // =====================================================================================================
  "home.retreat.first.1": ["lilsis", "Boots off. One... two. Everybody see me doing the rule."],
  "home.retreat.first.2": ["bigsis", "Rule two is voices down. You're whispering at full volume."],
  "home.retreat.first.3": ["lilsis", "THIS IS MY WHISPER."],
  "home.retreat.first.4": ["mom", "Darling, it's a set. It's a very good set. Let's all try to deserve it."],

  // ---- the rules, on their easel by the hatch (the close-up shows them, and what is written under the third in crayon)
  "home.rules.mom": ["narrator", "The rules of the Retreat: shoes off, voices down, no chickens. The third is already under appeal. The girls have founded a republic."],   // PASS-19H1: shorter
  "home.rules.bigsis": ["narrator", "Three rules, composed for a reader of seven: shoes off, voices down, no chickens. The crayon underneath is not Big Sister's."],   // PASS-19H1: shorter
  "home.rules.lilsis": ["narrator", "Rule three is 'No Chickens'. Little Sister found it unfair, and has lodged what she calls 'a appeal', in crayon."],   // PASS-19H1: emphasis; shorter; one idea

  // ---- Big Sister's timeline: where the game says how it counts the years, and what B.C. and A.D. mean.
  // Every year before Christ is the Bible's count, as Archbishop Ussher counted it (docs/CHARACTERS.md has the table).
  // The first time any of them looks along it, the three read it between them: .1 to .6, then .bigsis, .bigsis2, .mom, .lilsis.
  "home.timeline.1": ["bigsis", "I used Archbishop Ussher's dates. He counted from the Bible's own genealogies."],
  "home.timeline.2": ["mom", "A matter of record: the Archbishop's book, 1650. Now he's in felt pen."],
  "home.timeline.3": ["bigsis", "It starts on the left: 4004 B.C., the Creation. And here's the Flood, 2348 B.C."],
  "home.timeline.4": ["lilsis", "There's not much paper before Abram. I thought the beginning was the longest bit."],
  "home.timeline.5": ["bigsis", "It's as long as it was. 1921 B.C.: Abram leaves Haran, and goes down into Egypt."],
  "home.timeline.6": ["bigsis", "1491 B.C.: the Exodus. 44 B.C.: the Ides of March. That one's Rome's, but it's on my wall."],
  "home.timeline.bigsis": ["bigsis", "At the red mark the years turn round. Before it they're B.C., 'before Christ'."],
  "home.timeline.bigsis2": ["bigsis", "After it they count up: A.D., Anno Domini, Latin for 'in the year of the Lord'."],
  "home.timeline.mom": ["mom", "Every year on that wall is counted from His birth. I've always loved that."],   // PASS-17H: a faith line said as a mother says it
  "home.timeline.lilsis": ["lilsis", "I'm on it, right at the end, in pencil. Everybody else gets pen."],
  "home.timeline.bigsis3": ["bigsis", "A monk named Dionysius worked out that count in 525, from the birth of Jesus."],
  "home.timeline.bigsis4": ["bigsis", "Cristofori's piano. The Constitution. Sliced bread. And, in pencil, my sister."],
  "home.timeline.again.mom": ["narrator", "Big Sister's timeline: from the Creation to her little sister, on a single strip. Mom would hate to have ruled it."],   // PASS-17H: Mom's formality ('I should not like')
  "home.timeline.again.lilsis": ["narrator", "The timeline. Little Sister is at the end of it, in pencil. When she does something big, she will have to go in pen."],
  "home.timeline.pencil.mom": ["narrator", "The timeline is Big Sister's, and she does her own footnotes. Mom leaves it alone."],   // PASS-17H: Mom's formality ('One does not'); funnier
  "home.timeline.pencil.bigsis": ["narrator", "Tonight goes on the timeline when Big Sister knows what tonight was. And not in Dad's chewed pencil."],
  "home.timeline.pencil.lilsis": ["narrator", "Little Sister drew a hen on the timeline once, by the Flood. It is still there, very small. One hen is enough."],

  // ---- chain B: the sound machine, and the only batteries of that size in the house
  "home.sound.look.mom": ["narrator", "Big Sister's sound machine, playing one slow tune in D major. A sensible choice: D major never panics."],   // PASS-17H: the speech that is really an essay; funnier
  "home.sound.look.bigsis": ["narrator", "The sound machine, playing its slow tune. It is the only thing in the house that is calm on purpose."],
  "home.sound.look.lilsis": ["narrator", "The music box runs on batteries. Little Sister says so in a whisper, since this is the Retreat."],
  "home.sound.use.mom": ["narrator", "It is Big Sister's room and her machine. Mom wouldn't dream of touching it without her say-so."],   // PASS-17H: Mom's formality ('One does not'); one darling fewer
  "home.sound.use.bigsis": ["narrator", "Big Sister leaves it playing. Tonight it is the calmest thing in the house, and nobody has given her a reason to stop it."],
  "home.sound.use.lilsis": ["narrator", "Little Sister isn't allowed to touch anything up here. There is a treaty, and she signed it."],
  "home.sound.take.mom": ["narrator", "The batteries aren't Mom's to take. Big Sister has to be the one to give them."],   // PASS-17H: Mom's formality
  "home.sound.take.lilsis": ["narrator", "The batteries are in there, and Little Sister can't touch the machine. Her sister will have to take them out."],
  "home.sound.give.1": ["bigsis", "The only batteries that size in this whole house are in here. I knew this moment was coming."],
  "home.sound.give.2": ["bigsis", "Very well. The Retreat goes dark so that the internet may live."],
  "home.sound.give.3": ["lilsis", "It stopped. Now the water's going tick, tick, tick."],
  "home.sound.give.4": ["bigsis", "I'll be hearing that all night. I intend to mention this again."],
  "home.sound.give.5": ["mom", "You will, darling. And each time, I'll say thank you and mean it."],   // PASS-17H: Mom's formality ('shall')
  "home.sound.quiet.mom": ["narrator", "The sound machine is silent. Big Sister gave up her music for her sister, and has only mentioned it twice."],   // PASS-17H: Mom's formality
  "home.sound.quiet.bigsis": ["narrator", "With the machine off, only the fountain is left. It sounds exactly like a clock, which Big Sister had been managing not to notice."],
  "home.sound.quiet.lilsis": ["narrator", "The music box is quiet. Big Sister took the batteries out for her, so Little Sister is drawing her a chicken."],
  "home.sound.putback.mom": ["narrator", "The batteries don't go back in. They have an appointment with a pink flashlight."],
  "home.sound.putback.bigsis": ["narrator", "A sacrifice stays made. The batteries go in her sister's flashlight, not back in the machine."],
  "home.sound.putback.lilsis": ["narrator", "The batteries go in Little Sister's flashlight now. That is the whole point of them."],
  "home.soundtable.mom": ["narrator", "Music at one end of the table and water at the other. It is very well blocked, and Big Sister gets that from Mom."],   // PASS-19H1: shorter
  "home.soundtable.bigsis": ["narrator", "The machine and the fountain stand exactly a hand's width apart. Big Sister measured. It matters, though she couldn't say why."],   // PASS-19H1: shorter; one idea
  "home.soundtable.lilsis": ["narrator", "The sound table. Little Sister would put a chicken between the music and the water. Her sister says no."],   // PASS-19H1: emphasis; shorter; one idea
  "home.fountain.mom": ["narrator", "A little tabletop fountain, and not one drop on the floor. She is her mother's daughter."],   // PASS-19H1: shorter
  "home.fountain.bigsis": ["narrator", "The fountain is meant to sound like a brook. Tonight, to Big Sister, it sounds like a clock."],   // PASS-19H1: shorter
  "home.fountain.lilsis": ["narrator", "The fountain never stops running. It makes Little Sister need to... never mind."],   // PASS-19H1: emphasis; second joke cut

  // ---- the rest of the Retreat
  "home.skylight.mom": ["narrator", "The skylight. Big Sister thinks under the stars; at her age, Mom had to go outside to do it."],   // PASS-19H1: shorter
  "home.skylight.bigsis": ["narrator", "The skylight, and the little lights along the rafters. Big Sister has counted the lights in fours, twice. They are all still there."],   // PASS-19H1: shorter
  "home.skylight.lilsis": ["narrator", "The skylight over the bed. It has the same moon as Little Sister's window. She asked."],   // PASS-19H1: emphasis; shorter; one idea
  "home.retreat.window.mom": ["narrator", "The round window. From the road it makes the house look as if it has one eye open, and tonight it really has."],
  "home.retreat.window.bigsis": ["narrator", "The round window looks down the road. Big Sister has not been watching the road. Much."],
  "home.retreat.window.lilsis": ["narrator", "A round window, like a boat's. Little Sister concludes that her sister's room is a boat and her own is a farm."],
  "home.plants.mom": ["narrator", "Every plant alive and thriving, in an attic. Mom can't keep parsley."],   // PASS-19H1: shorter
  "home.plants.bigsis": ["narrator", "Big Sister's plants. Not one of them is worried about anything, and she envies them a little."],   // PASS-19H1: shorter
  "home.plants.lilsis": ["narrator", "The plants. There are no animals in her sister's jungle, though Little Sister did offer her a chicken."],   // PASS-19H1: shorter; one idea
  "home.towels.mom": ["narrator", "A robe on its hook, and a stack of rolled towels. Mom didn't own a robe until she was married."],   // PASS-19H1: shorter
  "home.towels.bigsis": ["narrator", "Rolled towels. A folded towel is a towel; a rolled towel, in Big Sister's view, is a decision."],   // PASS-19H1: shorter
  "home.towels.lilsis": ["narrator", "The rolled towels look like cinnamon buns. Little Sister can report that they are not."],   // PASS-19H1: emphasis; one idea
  "home.saltlamp.mom": ["narrator", "A salt lamp, giving the light of one tired candle. Big Sister won't hear a word against it."],   // PASS-19H1: shorter
  "home.saltlamp.bigsis": ["narrator", "The salt lamp is said to be calming. Big Sister has written down her doubts."],   // PASS-19H1: shorter; one idea
  "home.saltlamp.lilsis": ["narrator", "The orange rock is made of salt. Little Sister is not allowed to lick the lamp."],   // PASS-19H1: emphasis; shorter
  "home.books.mom": ["narrator", "Big Sister's books. She has read every one. Several were Mom's first, and Mom has given up hope of getting them back."],   // PASS-19H1: shorter; one idea
  "home.books.bigsis": ["narrator", "The books run from red to violet, but that is not the system. The system is in Big Sister's head, and it stays there."],   // PASS-19H1: shorter; one idea
  "home.books.lilsis": ["narrator", "The bookcase. The duck book is in the yellow part, and the duck has no words."],   // PASS-19H1: emphasis; shorter
  "home.desk.mom": ["narrator", "Big Sister's desk, and her novel. Mom has been asked not to read it, in writing."],   // PASS-17H: Mom's formality
  "home.desk.bigsis": ["narrator", "Her novel, open at chapter nine, and a jar of pencils, all slim and all exactly the same length."],
  "home.desk.lilsis": ["narrator", "The desk, and the pencil jar. Little Sister touched one pencil one time, and her sister knew."],
  "home.desk.pencil.mom": ["narrator", "That is Dad's pencil. Big Sister's are a matched set, and his would not match."],   // PASS-17H: Mom's formality; one darling fewer
  "home.desk.pencil.bigsis": ["narrator", "Dad's chewed pencil does not go in Big Sister's jar. Her jar has standards."],
  "home.desk.pencil.lilsis": ["narrator", "Little Sister drops Dad's pencil in the jar, then fishes it out again. Now her sister will have to count them all."],
  "home.bedbig.mom": ["narrator", "Big Sister's bed, made with hospital corners. Mom didn't teach her those, and isn't sure anybody did."],   // PASS-19H1: shorter; one idea
  "home.bedbig.bigsis": ["narrator", "Her bed, with hospital corners. Big Sister learned them from a book. It was a book about hospitals."],   // PASS-19H1: shorter; the 'second book' joke is the leaving's; one idea
  "home.bedbig.lilsis": ["narrator", "Her sister's bed, which Little Sister calls the tent. She isn't allowed in it, and has been in it nine times."],   // PASS-19H1: emphasis; shorter
  "home.mat.mom": ["narrator", "An exercise mat. Big Sister stretches on it at dawn, in silence; the floorboards tell Mom."],   // PASS-19H1: shorter
  "home.mat.bigsis": ["narrator", "The exercise mat. In for four, out for four. Tonight Big Sister loses count at three."],   // PASS-19H1: shorter
  "home.mat.lilsis": ["narrator", "The exercise mat. Little Sister does three somersaults on it in her head, and one not in her head."],   // PASS-19H1: emphasis; shorter
  "home.hatch.mom": ["narrator", "The hatch, and the ladder down to the landing. Everything is steeper going down, as Mom reminds the girls."],   // PASS-19H1: shorter; punch last; one idea
  "home.hatch.bigsis": ["narrator", "The hatch down to the landing. Shoes go back on at the bottom, and outdoor voices may resume."],   // PASS-19H1: shorter
  "home.hatch.lilsis": ["narrator", "The hole with the ladder in it. Little Sister goes down it backwards, like a bear."],   // PASS-19H1: emphasis; shorter

  // ---- what they say to each other in the Retreat
  "home.talk.retreat.mom.bigsis.key.a": ["mom", "That's D major, isn't it?"],
  "home.talk.retreat.mom.bigsis.key.b": ["bigsis", "D major. You always know, and it's extremely annoying."],
  "home.talk.retreat.mom.bigsis.1a": ["mom", "You put the Constitution on your timeline. In ink."],   // PASS-17H: Mom's formality
  "home.talk.retreat.mom.bigsis.1b": ["bigsis", "You stood behind me until I did, Mother."],
  "home.talk.retreat.mom.bigsis.2a": ["mom", "It's a lovely room. You made every inch of it yourself, and it shows."],   // PASS-17H: Mom's formality
  "home.talk.retreat.mom.bigsis.2b": ["bigsis", "On pocket money. I'd like that in the program."],
  "home.talk.retreat.mom.lilsis.1a": ["mom", "Indoor voice, please."],
  "home.talk.retreat.mom.lilsis.1b": ["lilsis", "This is my indoor voice. It's for indoors in a BARN."],
  "home.talk.retreat.mom.lilsis.2a": ["lilsis", "Can the General come up here? She's not a chicken, she's a general."],
  "home.talk.retreat.mom.lilsis.2b": ["mom", "That's for the court of appeal. I only supplied the spelling."],   // PASS-17H: Mom's formality
  "home.talk.retreat.bigsis.mom.1a": ["bigsis", "It's calm up here, and I'm not. It's inconsiderate of the room."],
  "home.talk.retreat.bigsis.mom.1b": ["mom", "The set is never nervous. Only the cast."],   // PASS-17H: Mom's formality
  "home.talk.retreat.bigsis.mom.2a": ["bigsis", "I counted the lights again, in fours. It came out even."],
  "home.talk.retreat.bigsis.mom.2b": ["mom", "And did it help?"],
  "home.talk.retreat.bigsis.mom.2c": ["bigsis", "No. But it came out even."],
  "home.talk.retreat.bigsis.lilsis.1a": ["bigsis", "Visiting hours end when the big hand reaches the twelve."],
  "home.talk.retreat.bigsis.lilsis.1b": ["lilsis", "Which twelve? There's one every hour, so I'll have the last one."],
  "home.talk.retreat.bigsis.lilsis.2a": ["bigsis", "You may stay if you can be silent for one whole minute."],
  "home.talk.retreat.bigsis.lilsis.2b": ["lilsis", "Okay... Is it a minute? Now? I was silent in between."],
  "home.talk.retreat.lilsis.mom.1a": ["lilsis", "Mommy, why can't chickens come up here?"],
  "home.talk.retreat.lilsis.mom.1b": ["mom", "It's your sister's room. She has three rules. You have eleven."],   // PASS-17H: Mom's formality; one darling fewer
  "home.talk.retreat.lilsis.mom.2a": ["lilsis", "It smells like a flower shop up here. And a bit like a library."],
  "home.talk.retreat.lilsis.mom.2b": ["mom", "That's your sister. Precisely."],   // PASS-17H: Mom's formality
  "home.talk.retreat.lilsis.bigsis.1a": ["lilsis", "Can I come up when it isn't visiting hours? Just my toe?"],
  "home.talk.retreat.lilsis.bigsis.1b": ["bigsis", "One toe. And I'll know which one."],
  "home.talk.retreat.lilsis.bigsis.2a": ["lilsis", "Are you scared?"],
  "home.talk.retreat.lilsis.bigsis.2b": ["bigsis", "No. A little. Don't tell the room."],
  "home.talk.retreat.lilsis.bigsis.2c": ["lilsis", "I'll hold your hand, then. Not for me. For the room."],

  // =====================================================================================================
  // IN ANY ROOM
  // =====================================================================================================
  // ---- what the one who is handed something says
  "home.give.studykey.mom": ["mom", "Thank you. I'll do the honors."],   // PASS-17H: Mom's formality ('shall')
  "home.give.studykey.bigsis": ["bigsis", "Trip Headquarters. I accept the responsibility, and the tag."],   // PASS-19H1: shorter; one idea
  "home.give.studykey.lilsis": ["lilsis", "The key! I'm the key person now, and I'm in charge of the door."],   // PASS-19H1: emphasis; one idea
  "home.give.lilflash.mom": ["mom", "I'll keep it safe for you. You'll want it for the closet under the stairs."],   // PASS-19H1: shorter
  "home.give.lilflash.bigsis": ["bigsis", "It's pink and slightly sticky, and I'm holding it under protest."],   // PASS-19H1: shorter
  "home.give.lilflash.lilsis": ["lilsis", "Hi, flashlight. You like me best."],   // PASS-19H1: emphasis; shorter; one idea
  "home.give.batteries.mom": ["mom", "I'll hold them like a borrowed prop: carefully, and not for long. They belong in her flashlight."],   // PASS-19H1: shorter
  "home.give.batteries.bigsis": ["bigsis", "They're not going back in the machine, so please don't ask. They go in her flashlight."],   // PASS-19H1: shorter
  "home.give.batteries.lilsis": ["lilsis", "Somebody else has my flashlight. These two need to meet."],   // PASS-19H1: emphasis; shorter
  // ---- batteries and flashlight in one pair of hands: whoever that is puts them in
  "home.flash.load.mom": ["narrator", "Mom slides the batteries in, and there is a small pink spotlight. Little Sister will want it back at once."],   // PASS-19H1: shorter; one idea
  "home.flash.load.bigsis": ["narrator", "Big Sister loads the batteries, and the flashlight lights. The Retreat did not go dark for nothing."],   // PASS-19H1: shorter
  "home.flash.load.lilsis": ["narrator", "Little Sister clicks the batteries in, and the flashlight shines. Now she can see in the closet under the stairs."],   // PASS-19H1: emphasis; shorter
  // ---- her flashlight, shined at something while there is nothing in it
  "home.flash.dead": ["narrator", "Little Sister clicks the switch, and nothing happens. The flashlight needs batteries."],
  "home.give.pencil.mom": ["mom", "Your father's pencil, thoroughly chewed. That'll do nicely."],   // PASS-19H1: shorter
  "home.give.pencil.bigsis": ["bigsis", "I know what Dad's pencil fits, but not how to do it. Mom does."],   // PASS-19H1: shorter; one idea
  "home.give.pencil.lilsis": ["lilsis", "I'll just hold Daddy's pencil and not fix anything. Probably."],   // PASS-19H1: emphasis; one idea
  "home.give.carkey.mom": ["mom", "Thank you. I am, after all, the only one with a license."],   // PASS-19H1: shorter
  "home.give.carkey.bigsis": ["bigsis", "I'm thirteen and holding the car key. I'm not driving yet."],   // PASS-19H1: shorter; one idea
  "home.give.carkey.lilsis": ["lilsis", "I call the front seat. I called it. It's called."],   // PASS-19H1: emphasis

  // ---- carried things
  "item.note.mom": ["narrator", "Dad's note: 'The year of the best thing since.' Big Sister knows the year of everything."],   // PASS-19H1: shorter; one idea
  "item.note.bigsis": ["narrator", "Dad's note. Sliced bread, 1928. Big Sister is keeping it as a primary source."],
  "item.note.lilsis": ["narrator", "A note that is all words. It wants somebody who reads books with no pictures, such as Big Sister."],
  "item.studykey.mom": ["narrator", "The study key, tag and all. It smells faintly of piano."],   // PASS-19H1: shorter; one idea
  "item.studykey.bigsis": ["narrator", "One brass key, formerly of the piano. Technically, it was the eighty-ninth."],   // PASS-19H1: shorter
  "item.studykey.lilsis": ["narrator", "The study key. Little Sister got it out of the piano herself, with her own arm."],   // PASS-19H1: emphasis; one idea
  "item.lilflash.mom": ["narrator", "Little Sister's flashlight: pink, chunky and much loved. It is hers to carry into the dark."],   // PASS-19H1: shorter
  "item.lilflash.bigsis": ["narrator", "The pink flashlight. Its button is sticky, and Big Sister is not going to ask."],   // PASS-19H1: shorter; one idea
  "item.lilflash.lilsis": ["narrator", "Little Sister's flashlight. It only works when its batteries work."],   // PASS-19H1: emphasis; shorter
  "item.batteries.mom": ["narrator", "Four batteries from the sound machine. They are wanted in a pink flashlight, and after that they would like to go home."],   // PASS-19H1: shorter
  "item.batteries.bigsis": ["narrator", "Four double-As for her sister's flashlight. The Retreat is silent, and Big Sister is fine."],   // PASS-19H1: shorter; one idea
  "item.batteries.lilsis": ["narrator", "The batteries go in her flashlight, and the flashlight goes in the closet. That is the whole plan."],   // PASS-19H1: emphasis; shorter; one idea
  "item.pencil.mom": ["narrator", "Dad's pencil. Mom has wound a great many cassettes with a pencil like this one, musicals mostly."],   // PASS-19H1: shorter
  "item.pencil.bigsis": ["narrator", "Dad's pencil. A cassette can be wound with one, Big Sister knows. Doing it is another matter."],   // PASS-19H1: 'Fun fact' rationed; shorter
  "item.pencil.lilsis": ["narrator", "Dad's pencil. It is bitten at the end, which, Little Sister explains, is where the thinking goes in."],   // PASS-19H1: shorter; one idea
  "item.carkey.mom": ["narrator", "Mom's spare car key. After two years in a cash box with the ketchup, it has earned a drive."],   // PASS-19H1: shorter
  "item.carkey.bigsis": ["narrator", "Mom's spare car key, liberated by the Constitution."],   // PASS-19H1: shorter; punch last
  "item.carkey.lilsis": ["narrator", "The car key. Mom does the driving, and Little Sister does the beep."],   // PASS-19H1: emphasis; shorter; one idea

  // =====================================================================================================
  // HINTS: one from each of them for every puzzle. The one whose job it is says what to try; the others say whose job it is.
  // =====================================================================================================
  "hint.home.riddle.mom": ["mom", "Your father's locked his study and taped a notice to the door. Let's go up and read it."],
  "hint.home.riddle.bigsis": ["bigsis", "The study's locked, and Dad left a notice on its door upstairs. It reads like a riddle, so it is one."],
  "hint.home.riddle.lilsis": ["lilsis", "Daddy's door upstairs has a sign with so many words on it. Words are my sister's favorite."],
  "hint.home.key.lilsis": ["lilsis", "The key's inside the piano, behind the little wall by the pedals. My arm fits in there."],   // PASS-19H1: shorter (its words stay); one idea
  "hint.home.key.mom": ["mom", "The key's inside my piano, and my arms won't reach it. It wants someone small and brave."],   // PASS-19H1: shorter (its words stay); one idea
  "hint.home.key.bigsis": ["bigsis", "The key's lying on the piano's hammers. My arm isn't going in there. My sister fits, and knows it."],   // PASS-19H1: shorter (its words stay); one idea
  "hint.home.study.mom": ["mom", "We have the key to his study now. Whoever's holding it should try the door upstairs."],
  "hint.home.study.bigsis": ["bigsis", "One of us has the study key. The study door is upstairs, at the end of the landing."],
  "hint.home.study.lilsis": ["lilsis", "We got the key! Whoever's got it, put it in Daddy's door upstairs."],
  "hint.home.batteries.lilsis": ["lilsis", "The closet's too dark. I need my flashlight from my fort, and if it's dead, my sister's music box has batteries."],
  "hint.home.batteries.bigsis": ["bigsis", "A dead flashlight is no use. The only batteries that size are in my sound machine, in the Retreat."],
  "hint.home.batteries.mom": ["mom", "A dead flashlight needs batteries, and your sister's sound machine has them. She'll have to take them out."],
  "hint.home.router.lilsis": ["lilsis", "My flashlight works now. The internet's in the closet under the stairs, and I fit."],
  "hint.home.router.mom": ["mom", "The router's in the closet under the stairs. Her flashlight works now, so that's her cue."],   // PASS-17H: Mom's formality
  "hint.home.router.bigsis": ["bigsis", "The flashlight works, and I paid for it in music. The router's in the closet under the stairs. That's hers."],
  "hint.home.note.bigsis": ["bigsis", "Dad always writes his passwords down, never plainly. There's a yellow note on the monitor I should read."],
  "hint.home.note.mom": ["mom", "Your father left a note on the monitor, a riddle about a year. That's your sister's department."],   // PASS-17H: Mom's formality
  "hint.home.note.lilsis": ["lilsis", "There's a yellow sticky on Daddy's computer. It's all words, so it's for my sister."],
  "hint.home.login.mom": ["mom", "We have the internet back, and the password. I'll sit down at your father's computer myself."],   // PASS-17H: Mom's formality
  "hint.home.login.bigsis": ["bigsis", "The router's on and the password is 1928. Then the computer asks about Mom's wedding, so it's hers."],
  "hint.home.login.lilsis": ["lilsis", "I fixed the internet, and my sister did the number. Now Mommy does the typing."],
  "hint.home.tape.mom": ["mom", "The answering machine has spilled its tape. I can wind it back in with your father's crossword pencil."],
  "hint.home.tape.bigsis": ["bigsis", "The tape needs winding back in with Dad's crossword pencil. Mom has the knack. I only have the theory."],
  "hint.home.tape.lilsis": ["lilsis", "The tape fell out of the tape machine. Not my fault this time. Mommy needs a pencil to wind it."],
  "hint.home.message.mom": ["mom", "The tape is wound, and there's one new message on your father's machine. Let's hear it."],   // PASS-17H: Mom's formality
  "hint.home.message.bigsis": ["bigsis", "The tape's back in its cassette, and there's one new message on Dad's machine. We should play it."],
  "hint.home.message.lilsis": ["lilsis", "The tape's fixed, and I didn't even do it. Press 'Play' on the blinky machine."],
  "hint.home.vault.mom": ["mom", "Your father's vault wants the 'We the People' year. It's framed on our living-room wall."],   // PASS-17H: Mom's formality
  "hint.home.vault.bigsis": ["bigsis", "Dad's 'family vault' has the spare car key in it. The combination is a year Mom knows by heart."],
  "hint.home.vault.lilsis": ["lilsis", "Daddy's vault box has a clicky wheel. Mommy knows the 'We the People' number."],
  "hint.home.leave.mom": ["mom", "We know where that phone was last seen, girls. All that's left is the front door."],
  "hint.home.leave.bigsis": ["bigsis", "We have a location, a message and a car key. The next step is the front door."],
  "hint.home.leave.lilsis": ["lilsis", "We found the dot, so let's go. The front door's right there."],   // PASS-19H1: emphasis; one idea
};
