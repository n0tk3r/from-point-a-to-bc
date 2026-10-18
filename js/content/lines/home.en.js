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
  "home.arrive.vm1": ["dad", "'You've reached Dad. I can't pick up right now. I'm either driving or lost.'"],
  "home.arrive.vm2": ["dad", "'And I am never lost. So: driving. Leave a message.'"],
  "home.arrive.1": ["mom", "Voicemail. That is the ninth time. I had decided to stop worrying at eight."],
  "home.arrive.2": ["lilsis", "Daddy's not lost. Daddy's EARLY."],
  "home.arrive.2b": ["bigsis", "That is not what early means."],
  "home.arrive.3": ["bigsis", "They left at noon. It is a four-hour drive. It is now nine forty. For the record, that is not a shortcut."],
  "home.arrive.4": ["mom", "Dinner was at six. I set five places, and I am not clearing two of them away."],
  "home.arrive.pray.1": ["mom", "First things first, girls."],
  "home.arrive.pray.2": ["mom", "Father, You know where they are tonight, and I do not. Keep them."],
  "home.arrive.pray.3": ["mom", "And bring us to them. In Jesus' name."],
  "home.arrive.pray.4": ["lilsis", "And please make Daddy ask for directions. Just ONE time. Amen."],
  "home.arrive.pray.5": ["mom", "Amen."],
  "home.arrive.5": ["bigsis", "His phone still tells the family computer where it is. 'The mainframe'. Upstairs, in his study."],
  "home.arrive.6": ["lilsis", "Then the computer KNOWS! Ask the computer!"],
  "home.arrive.6b": ["bigsis", "It cannot answer. The internet has been down since Dad 'improved' the wiring this morning."],
  "home.pc.router": ["mom", "The router lives in the closet under the stairs. Your father keeps the internet next to the vacuum cleaner."],
  "home.arrive.7": ["mom", "Places, girls. We are going to find out where that phone was last seen."],

  // =====================================================================================================
  // THE LIVING ROOM
  // =====================================================================================================
  "home.upstairs.mom": ["mom", "Three doors upstairs. The locked one is your father's study. He says it keeps the surprises in."],
  "home.upstairs.bigsis": ["bigsis", "Upstairs: my brother's room, my sister's room, Dad's study. Above all three, mine. One of the four is tidy."],
  "home.upstairs.lilsis": ["lilsis", "My fort is up there! It has a sign. NO BIG SISTERS. I made the sign AND the rule."],

  "home.window.mom": ["mom", "No headlights. I have looked eleven times. Twelve."],
  "home.window.bigsis": ["bigsis", "'The street,' she wrote, 'was the wrong kind of quiet.' ...That's good. I'm keeping that."],
  "home.window.lilsis": ["lilsis", "I'm watching for the car. I'm the best at watching. I haven't blinked since dinner."],
  "home.photo.mom": ["mom", "The five of us at the lake. Your father took a shortcut that day, too. We saw a great deal of the lake."],
  "home.photo.bigsis": ["bigsis", "Five people, one tripod. Dad set the timer and ran. He is the blur."],
  "home.photo.lilsis": ["lilsis", "That's me at the lake! I was only SIX. Now I'm seven. That's a WHOLE number bigger."],
  "home.stairs.mom": ["mom", "Nobody is going up to bed tonight. Least of all me."],
  "home.stairs.bigsis": ["bigsis", "Sixteen steps. I count in fours when I'm nervous. Sixteen is four fours. It did not help."],
  "home.stairs.lilsis": ["lilsis", "I'm not tired. I'm NEVER tired. ...What time is it?"],

  // ---- chain B: the closet under the stairs
  "home.closet.look.mom": ["mom", "The closet under the stairs. The door stops at my shoulder, and it opens exactly this far."],
  "home.closet.look.bigsis": ["bigsis", "The door opens four inches. I am wider than four inches. I have shoulders."],
  "home.closet.look.lilsis": ["lilsis", "It's dark in there. And there's a tiny light! That's the internet. The internet is TINY."],
  "home.closet.use.mom": ["mom", "A lady does not squeeze into closets, darling. A lady has a seven-year-old."],
  "home.closet.use.bigsis": ["bigsis", "I refuse. There are spiders in there, and I am thirteen. Both of those are final."],
  "home.closet.go.1": ["lilsis", "I FIT!"],
  "home.closet.dark.1": ["lilsis", "It's SO dark. I can't find the plug. I found the vacuum. With my NOSE."],
  "home.closet.dark.2": ["lilsis", "I need my flashlight. MINE. The pink one, from my fort. Come ON, everybody. I know the way!"],
  "home.closet.dark.3": ["mom", "Then we go up and fetch it, sweetheart. Nobody else is allowed in that fort. Your rule."],
  "home.closet.needflash": ["lilsis", "Not without my flashlight! I'm not scared. I'm BRAVE-scared. Brave-scared people bring a flashlight."],
  "home.closet.lent": ["lilsis", "I need my flashlight BACK. Somebody's got it who isn't me. Hand it over, please. I'm the closet person."],
  "home.closet.dead": ["lilsis", "A DEAD flashlight is just a pink stick! It wants batteries. THEN I go in. That's the plan."],
  "home.closet.go.2": ["lilsis", "Flashlight ON! Hi, vacuum. Hi, spiders. And there's a plug that isn't plugged into ANYTHING!"],
  "home.closet.go.3": ["mom", "Into the wall, sweetheart. The socket with two little eyes and a surprised mouth."],
  "home.closet.go.4": ["lilsis", "The red light went GREEN! I fixed the internet! I'm a ENGINEER!"],
  "home.closet.go.5": ["bigsis", "AN engineer."],
  "home.closet.go.6": ["lilsis", "That's what I SAID."],
  "home.closet.again": ["lilsis", "I already fixed it. It's green. Green means I'm good at it."],
  "home.closet.done.mom": ["mom", "A small green light. Clever girl."],
  "home.closet.done.bigsis": ["bigsis", "The light is green. She will be insufferable for a week."],
  "home.closet.key.mom": ["mom", "It doesn't lock. It's never needed to. Nothing in there wants to get out."],   // PASS-17H: Mom's formality; one darling fewer
  "home.closet.key.bigsis": ["bigsis", "The closet does not lock. It only sticks. Dad says that is a feature."],
  "home.closet.key.lilsis": ["lilsis", "No keyhole! It's just a door that's bad at being a door."],

  // ---- Mom's bookcase, the kitchen, the Preamble, the clock
  "home.shelf.mom": ["mom", "My shelves. The Adams letters, General Washington, Dr. Franklin, a great many plays, and the hymnal."],
  "home.shelf.mom2": ["mom", "In March of 1776 Abigail Adams wrote to John, 'Remember the Ladies.' I do like her."],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.shelf.bigsis": ["bigsis", "Mom's books. She reads lives of the Founders the way other people read thrillers. She gasps."],
  "home.shelf.lilsis": ["lilsis", "Mommy's books. No pictures. I checked ALL of them. One has a man in a wig."],
  "home.kitchen.mom": ["mom", "I've left the kitchen light on. I always do, for whoever's last home."],   // PASS-17H: Mom's formality
  "home.kitchen.bigsis": ["bigsis", "Mom has made four pots of tea since six. She says she is not worried. The kettle says otherwise."],
  "home.kitchen.lilsis": ["lilsis", "My best hen is on the fridge! She's guarding the snacks. Is it snack time? It's ALWAYS a little bit snack time."],
  "home.frame.mom": ["mom", "'We the People.' Signed in Philadelphia, the seventeenth of September, 1787. It still gives me goosebumps."],   // PASS-17H: 'A matter of record' as a gag (three in the act), not a habit; warmer
  "home.frame.bigsis": ["bigsis", "The Preamble. Mom can recite all of it. On the Fourth of July she does. With gestures."],
  "home.frame.lilsis": ["lilsis", "It says 'We the People' in GIANT curly letters. Then the letters get tired and go little."],
  "home.clock.mom": ["mom", "Twenty to ten. They're five hours and forty minutes late. I've stopped rounding."],   // PASS-17H: Mom's formality
  "home.clock.bigsis": ["bigsis", "Nine forty. Mom says that clock ticks a little flat. I cannot hear it. I have tried."],
  "home.clock.lilsis": ["lilsis", "The little hand's nearly on the ten. That's THREE fingers past my bedtime. Nobody say anything."],

  // ---- chain A: the piano, and the key that is in it
  "home.piano.look.mom": ["mom", "My piano. I taught your sister to play it. Now she plays it better than I do. That was the plan."],   // PASS-17H: truer to her (proud, not stiff)
  "home.piano.look.bigsis": ["bigsis", "My piano. Fun fact: Bartolomeo Cristofori built the first one, in Florence, around the year 1700."],
  "home.piano.look.bigsis2": ["bigsis", "They called it a harpsichord with soft and loud. I would have called it a miracle."],
  "home.piano.look.lilsis": ["lilsis", "The piano! I know one whole song. I made it up. It's short and LOUD, and it's MINE."],
  "home.piano.key.mom": ["mom", "There is a key in my piano. I've said it out loud now, and it's no better."],   // PASS-17H: the speech that is really an essay (lightly)
  "home.piano.key.bigsis": ["bigsis", "The key is on the hammers, under the A above middle C. I can hear it from here."],
  "home.piano.key.lilsis": ["lilsis", "A key INSIDE the piano? I'll get it! I fit under everything. Everybody stand BACK."],
  "home.piano.use.mom": ["mom", "'A Mighty Fortress Is Our God.' Luther's. One verse, quietly, for courage."],   // PASS-17H: shorter; the hymn's author without the label
  "home.piano.use.mom2": ["mom", "'God is our refuge and strength, a very present help in trouble.' Very present. That's the part I need tonight."],   // PASS-17H: reference aloud; the Bible fact tacked on
  "home.piano.use.mom3": ["mom", "Once more, then. It's a hymn that doesn't mind being needed."],   // PASS-17H: Mom's formality
  "home.piano.use.bigsis": ["bigsis", "Something in a minor key. It felt appropriate."],
  "home.piano.use.bigsis2": ["bigsis", "When Dad is home I will play the loud one he likes. Twice."],
  "home.piano.use.lilsis": ["lilsis", "PLONK. That was my song. It's called 'Plonk'."],
  "home.thunk.bigsis.1": ["bigsis", "That was the A above middle C. It went 'thunk'. This piano does not go 'thunk'."],
  "home.thunk.bigsis.2": ["bigsis", "Something is lying on the hammers. Something small, and metal."],
  "home.thunk.mom.react": ["mom", "On the hammers. In MY piano. Then somebody put it there, and I know which somebody."],
  "home.thunk.mom.1": ["mom", "One dead note. The A above middle C. That's not the piano, and it's certainly not me."],   // PASS-17H: Mom's formality
  "home.thunk.mom.2": ["mom", "Something is lying on the hammers. Somebody has dropped something into MY piano."],
  "home.thunk.bigsis.react": ["bigsis", "Small and metal, by the sound. I can tell you exactly which hammer it is on."],
  "home.key.mom.1": ["mom", "With the lid up I can see it. A door key, on the hammers, with a tag in your father's capitals."],
  "home.key.mom.2": ["mom", "And I cannot reach it. My arms are a civilized length."],
  "home.key.mom.3": ["mom", "The panel down by the pedals lifts off. Under the keyboard, sweetheart: that is your cue."],
  "home.key.bigsis.1": ["bigsis", "Thunk. It is under the A above middle C. I can hear exactly where."],
  "home.key.bigsis.2": ["bigsis", "I am not putting my arm in a piano. I need all ten fingers. I am halfway through a sonata."],
  "home.key.get.1": ["lilsis", "There's a little wall down here by the pedals. It comes OFF!"],
  "home.key.get.2": ["lilsis", "It's all dusty. There's a marble. And a penny. And a KEY!"],
  "home.key.get.3": ["mom", "The study key. With a tag: 'TRIP HQ.' He hid it in a piano, and then he labelled it."],
  "home.key.get.4": ["bigsis", "And not one string out of tune. For the record, that is luck."],
  "home.key.get.5": ["lilsis", "I'm keeping the marble."],
  "home.piano.keyback.mom": ["mom", "It has spent quite long enough in my piano, thank you."],
  "home.piano.keyback.bigsis": ["bigsis", "Putting it back would be historically accurate and of no use whatever."],
  "home.piano.keyback.lilsis": ["lilsis", "It came OUT of there. I'm not putting it back. I only just got it!"],

  // ---- the gate: the front door, and the sampler over it
  "home.door.look.mom": ["mom", "The doorbell is a quarter-tone flat. So is your father, when he sings. I'm fond of them both."],   // PASS-17H: Mom's formality
  "home.door.look.bigsis": ["bigsis", "The front door. Two coats are missing from the hooks. I notice hooks."],
  "home.door.look.lilsis": ["lilsis", "The door Daddy comes in by. I'm watching it AND the window. I have two eyes."],
  "home.door.early.mom": ["mom", "Not until we know where we are going. One of us in this family must."],
  "home.door.early.bigsis": ["bigsis", "We don't have a destination. A journey without a destination is just Dad."],
  "home.door.early.lilsis": ["lilsis", "I'm READY. I've been ready since dinner. ...Which way IS Daddy? Somebody find out which way."],
  "home.door.message.mom": ["mom", "Not yet. There's a message on your father's machine upstairs, and I want to hear it first."],   // PASS-17H: Mom's formality
  "home.door.message.bigsis": ["bigsis", "There is one new message on Dad's machine. One does not leave the house with one new message."],
  "home.door.message.lilsis": ["lilsis", "But the blinky machine has a message! What if it's Daddy? It's probably DADDY."],
  "home.door.nokey.mom": ["mom", "We know where, and we've heard his voice. What we haven't got is a car key."],   // PASS-17H: Mom's formality
  "home.door.nokey.bigsis": ["bigsis", "Destination: yes. Message: yes. Car key: no. Two out of three does not start an engine."],
  "home.door.nokey.lilsis": ["lilsis", "We can't go! We don't have a KEY! ...I could push the car. I'm mighty."],
  "home.door.keys.1": ["mom", "And there's the matter of my car. Your father moved it this morning. My keys left in his pocket."],   // PASS-17H: Mom's formality
  "home.door.keys.2": ["bigsis", "There is a spare. Dad keeps it in the 'family vault'. In his study. He told us so. He was proud."],
  "home.door.keys.3": ["lilsis", "It's a box with a clicky wheel! Mommy will know the clicks. Mommy knows ALL the clicks."],
  "home.door.psalm.1": ["mom", "One moment. In this family nobody starts a journey without the psalm."],
  "home.door.psalm.2": ["bigsis", "Psalm 121, verse 8. She always does this part."],   // PASS-17H: the reference is Big Sister's to say; a beat for her sister
  "home.door.psalm.3": ["lilsis", "'The LORD shall preserve thy going out and thy coming in from this time forth, and even for evermore.'"],
  "home.door.psalm.4": ["mom", "Amen. Going out, and coming in. All five of us."],
  "home.leave.1": ["mom", "Coats, girls. We are going to Nevada."],
  "home.leave.2": ["bigsis", "I'll bring the atlas. And a book. And a second book, in case the first one ends."],
  "home.leave.3": ["lilsis", "I'll bring my boots! I'm already WEARING my boots!"],
  "home.leave.4": ["mom", "We are going to be perfectly polite, and completely impossible to get rid of."],
  "home.door.studykey.mom": ["mom", "That's the study key. This door wants a car at the other end of it."],   // PASS-17H: Mom's formality; one darling fewer
  "home.door.studykey.bigsis": ["bigsis", "Wrong key. This one opens Dad's study. That door opens everything else."],
  "home.door.studykey.lilsis": ["lilsis", "It doesn't fit! Daddy's key is for Daddy's door."],
  "home.sampler.mom": ["mom", "'...as for me and my house, we will serve the LORD.' I stitched it the winter we moved in. Before the curtains."],   // PASS-17H: reference aloud
  "home.sampler.bigsis": ["bigsis", "Mom's needlework. Every letter is the same height. I measured. I was nine, and it was raining."],
  "home.sampler.lilsis": ["lilsis", "Red letters, and a little house, and a heart. Mommy let me do one stitch. It's THAT one. The wobbly one."],
  "home.coats.mom": ["mom", "The hooks. His good hat is still here. He left in the other one. I have opinions about the other one."],
  "home.coats.bigsis": ["bigsis", "Coats. Mine is the one hung up by its loop. I wish to be clear about that."],
  "home.coats.lilsis": ["lilsis", "Coats! Daddy's big one is gone. It went on the trip with Daddy in it."],

  // ---- Dad's armchair, his crossword and his pencil; the dinner table and the Bible
  "home.chair.mom": ["mom", "Your father's chair. It has kept his shape. I find I rather like that tonight."],
  "home.chair.bigsis": ["bigsis", "Dad's chair. His crossword is on the arm. Seven across is wrong. I haven't told him."],
  "home.chair.lilsis": ["lilsis", "Daddy's chair. If you sit in it you have to say 'well, well, well'."],
  "home.crossword.mom": ["mom", "His crossword, half done. He does it in that chair every evening. Tonight it can wait for him."],
  "home.crossword.bigsis": ["bigsis", "Seven across is still wrong. He does them in ink when he is sure. This one is in pencil. He knew."],
  "home.crossword.lilsis": ["lilsis", "Daddy's puzzle. He lets me do the three-letter ones. I always put HEN. It's right more than you'd think."],
  "home.pencil.look.mom": ["mom", "His pencil. The only one in this house that is ever where it should be."],
  "home.pencil.look.bigsis": ["bigsis", "Dad's crossword pencil. Yellow, ordinary, and a great many tooth marks. He thinks with his teeth."],
  "home.pencil.look.lilsis": ["lilsis", "Daddy's pencil! He bites it when he thinks. It's a VERY thought-about pencil."],
  "home.pencil.take.mom": ["mom", "I'm borrowing this, my love. You can have it back when you come home and ask for it."],   // PASS-17H: Mom's formality ('shall')
  "home.pencil.take.bigsis": ["bigsis", "Dad's pencil. I will return it sharpened. He will not notice. He never does."],
  "home.pencil.take.lilsis": ["lilsis", "I've got Daddy's pencil! It has teeth marks. They're not mine. Mostly."],
  "home.table.mom": ["mom", "Pot roast at six o'clock sharp. It is no longer sharp."],
  "home.table.bigsis": ["bigsis", "'The table,' she observed, 'was set for five. The house was not.'"],
  "home.table.lilsis": ["lilsis", "Can I have Daddy's potatoes? He's not using them."],
  "home.bible.mom": ["mom", "'My help cometh from the LORD, which made heaven and earth.' He read us that this morning. I'm holding on to it."],   // PASS-17H: reference aloud
  "home.bible.bigsis": ["bigsis", "Psalm 121, where Dad left it. 'I will lift up mine eyes unto the hills, from whence cometh my help.'"],
  "home.bible.lilsis": ["lilsis", "'The LORD is my shepherd; I shall not want.' I know ALL of it. ...I do want Daddy, though."],   // PASS-17H: reference aloud

  // ---- what they say to each other in the living room
  "home.talk.mom.bigsis.key.a": ["mom", "You can hear which note it's under. Can't you just reach in?"],   // PASS-17H: Mom's formality; one darling fewer
  "home.talk.mom.bigsis.key.b": ["bigsis", "I could. I will not. It is a piano, Mother, not a mailbox. Ask the one who fits under things."],
  "home.talk.batt.mom.bigsis.a": ["mom", "Darling. Your sister's flashlight wants batteries. I believe you know where there are some."],
  "home.talk.batt.mom.bigsis.b": ["bigsis", "I know where ALL the batteries in this house are, Mother. That is what makes it painful."],
  "home.talk.batt.lilsis.bigsis.a": ["lilsis", "Your music box has batteries in it. I've SEEN them. With my EYES. So you know what you have to do."],
  "home.talk.batt.lilsis.bigsis.b": ["bigsis", "It is a sound machine. And yes. It has. I was hoping nobody would say so out loud."],
  "home.talk.batt.mom.lilsis.a": ["mom", "Batteries in one pocket and a flashlight in another, sweetheart. They ought to be introduced."],
  "home.talk.batt.mom.lilsis.b": ["lilsis", "Give them to ME! Or give me the flashlight. Or BOTH. I've got two hands and a pocket."],
  "home.talk.mom.bigsis.1a": ["mom", "You are very quiet, darling."],
  "home.talk.mom.bigsis.1b": ["bigsis", "I am thinking. It only looks like quiet from the outside."],
  "home.talk.mom.bigsis.2a": ["mom", "Whatever has happened, we will deal with it the way we deal with everything."],
  "home.talk.mom.bigsis.2b": ["bigsis", "With a list?"],
  "home.talk.mom.bigsis.2c": ["mom", "With a list."],
  "home.talk.mom.lilsis.dark.a": ["mom", "Your flashlight's in your fort, sweetheart. Want to go up and get it?"],   // PASS-17H: Mom's formality ('shall')
  "home.talk.mom.lilsis.dark.b": ["lilsis", "I'm ALREADY going. And nobody look in my fort. There's nothing in there. There's a LOT in there."],
  "home.talk.mom.lilsis.1a": ["mom", "Are you frightened, sweetheart?"],
  "home.talk.mom.lilsis.1b": ["lilsis", "No! ...Are YOU?"],
  "home.talk.mom.lilsis.1c": ["mom", "Not while I have you to look after me."],
  "home.talk.mom.lilsis.2a": ["lilsis", "Mommy, why did Daddy take a shortcut?"],
  "home.talk.mom.lilsis.2b": ["mom", "Because the long way around has never once been his idea."],
  "home.talk.bigsis.mom.1a": ["bigsis", "Mom. Statistically, they are fine."],
  "home.talk.bigsis.mom.1b": ["mom", "Thank you, darling. And unstatistically?"],
  "home.talk.bigsis.mom.1c": ["bigsis", "...Also fine. Probably."],
  "home.talk.bigsis.mom.2a": ["bigsis", "I've started a new chapter. It is called 'The Night They Didn't Come Home'."],
  "home.talk.bigsis.mom.2b": ["mom", "Do give it a happy ending."],
  "home.talk.bigsis.lilsis.key.a": ["bigsis", "There is a panel by the pedals, under the keyboard. You are the only one of us who fits under there."],
  "home.talk.bigsis.lilsis.key.b": ["lilsis", "I KNOW. I've been under there LOTS. That's where I keep my marble."],
  "home.talk.bigsis.lilsis.1a": ["bigsis", "Don't touch anything while I'm thinking."],
  "home.talk.bigsis.lilsis.1b": ["lilsis", "I'm not touching. I'm HOLDING."],
  "home.talk.bigsis.lilsis.2a": ["lilsis", "Why do you know so many years?"],
  "home.talk.bigsis.lilsis.2b": ["bigsis", "Because somebody has to. Years don't remember themselves."],
  "home.talk.lilsis.mom.1a": ["lilsis", "Mommy, I can help. I'm small but I'm MIGHTY."],
  "home.talk.lilsis.mom.1b": ["mom", "You are the mightiest person I know, my love. Do aim it carefully."],
  "home.talk.lilsis.mom.2a": ["lilsis", "Can I stay up?"],
  "home.talk.lilsis.mom.2b": ["mom", "Tonight, yes."],
  "home.talk.lilsis.mom.2c": ["lilsis", "...Now I'm worried."],
  "home.talk.lilsis.mom.3a": ["lilsis", "Mommy, sit down. You've been standing up since dinner. I'll do the worrying for a while."],
  "home.talk.lilsis.mom.3b": ["mom", "Five minutes, my love. Then I'll want my worrying back."],   // PASS-17H: Mom's formality ('shall')
  "home.talk.lilsis.bigsis.1a": ["lilsis", "Read me a fact."],
  "home.talk.lilsis.bigsis.1b": ["bigsis", "It's 'tell me a fact'."],
  "home.talk.lilsis.bigsis.1c": ["lilsis", "Tell me a READ."],
  "home.talk.lilsis.bigsis.2a": ["lilsis", "My tooth is loose. Look. LOOK."],
  "home.talk.lilsis.bigsis.2b": ["bigsis", "I have seen the tooth. Everyone on this street has seen the tooth."],

  // =====================================================================================================
  // THE LANDING
  // =====================================================================================================
  "home.landing.first.1": ["bigsis", "Dad's study is the door with the notice taped to it. It will be locked. It is always locked."],
  "home.landing.first.2": ["mom", "With your father there is always a notice."],
  "home.landing.first.3": ["lilsis", "And my brother's door says NO GIRLS ALLOWED. We'll SEE about that."],

  "home.landing.window.mom": ["mom", "The moon is over the maple. It's the same moon wherever they are. I find that useful."],   // PASS-17H: Mom's formality
  "home.landing.window.bigsis": ["bigsis", "The moon is nearly full. Bright enough to read by, if one's mother allowed it."],
  "home.landing.window.lilsis": ["lilsis", "The moon follows our car when we drive. So it's following Daddy RIGHT NOW. Good moon."],
  "home.ladder.mom": ["mom", "The attic ladder. She asked for the attic for her thirteenth birthday. I said yes before I'd thought about the ladder."],   // PASS-17H: Mom's formality
  "home.ladder.bigsis": ["bigsis", "The way up to the Retreat. The card says so. It is my room, and I should like that remembered up there."],
  "home.ladder.lilsis": ["lilsis", "The ladder to my sister's room! The card says THE RETREAT. I have visiting hours. They're SHORT."],
  "home.landing.photos.mom": ["mom", "Our wedding photograph. He was forty minutes late for it. He had refused to ask the way."],
  "home.landing.photos.bigsis": ["bigsis", "Baby pictures. I was a serious baby. There is one of me frowning at a rattle."],
  "home.landing.photos.lilsis": ["lilsis", "That's me with NO teeth. And that's me with all my teeth. Soon it's me with one less."],
  "home.hamper.mom": ["mom", "The hamper. It was empty at noon. I don't know how this family does it, but I admire the industry."],   // PASS-17H: Mom's formality
  "home.hamper.bigsis": ["bigsis", "The laundry hamper. I have no comment on the hamper."],
  "home.hamper.lilsis": ["lilsis", "The hamper! That's where the flock goes to get promoted. Corporal Speckle's going in NEXT."],
  "home.lildoor.mom": ["mom", "'BEWARE OF CHICKENS.' She asked me how to spell 'beware'. I didn't ask why. You learn not to."],   // PASS-17H: Mom's formality ('One learns')
  "home.lildoor.bigsis": ["bigsis", "My sister's door. Chicken stickers, a hen in crayon, and a warning. The warning is accurate."],
  "home.lildoor.lilsis": ["lilsis", "MY door! It says BEWARE OF CHICKENS. I did the letters. And the hen. And ALL the stickers."],
  "home.halltable.mom": ["mom", "The key bowl. Every key this family owns, except the two I want tonight."],
  "home.halltable.bigsis": ["bigsis", "The shed, the mailbox, and three keys nobody can identify. Not the study. I have looked."],
  "home.halltable.lilsis": ["lilsis", "The key bowl! I'm not allowed to play pirates with it. Anymore."],
  "home.halltable.use.mom": ["mom", "I've been through this bowl twice. I'm not above a third time. ...No."],   // PASS-17H: Mom's formality
  "home.halltable.use.bigsis": ["bigsis", "Nothing labelled 'study'. Dad labels everything. Its absence is a clue in itself."],
  "home.halltable.use.lilsis": ["lilsis", "Jingle jingle jingle. ...I'm HELPING."],
  "home.countdown.mom": ["mom", "The countdown to the trip. One day crossed off every morning at breakfast, with ceremony. Today is the little car."],
  "home.countdown.bigsis": ["bigsis", "My brother's countdown. He crossed off today before today had happened. I let it stand."],
  "home.countdown.lilsis": ["lilsis", "The trip chart! The red car at the end is TODAY. The car got there. Daddy's still coming."],
  "home.landing.stairs.mom": ["mom", "The stairs. I've carried each of you up them asleep. You were all a great deal lighter."],   // PASS-17H: Mom's formality
  "home.landing.stairs.bigsis": ["bigsis", "Sixteen steps down. It is the same sixteen. I checked on the way up."],
  "home.landing.stairs.lilsis": ["lilsis", "I can do the stairs two at a time! Going DOWN I can do three. Mommy says don't."],
  "home.rail.mom": ["mom", "The living room, from the gallery. A set with the lights left on and nobody on it. Two of the cast are late."],
  "home.rail.bigsis": ["bigsis", "'From the landing,' she wrote, 'the room below looked like a sentence with two words missing.'"],
  "home.rail.lilsis": ["lilsis", "I can see the piano! And the rug! And the door Daddy comes in by. It's still shut. I checked."],

  // ---- the Son's door: NO GIRLS ALLOWED, and booby-trapped. Mom does not try it tonight. The first time a sister opens
  // it, his toy alarm (.alarm.1; Little Sister does the password, .2 and .3), a volley of foam darts, the author's line
  // for Big Sister (.trap.bigsis, word for word), Little Sister's say, and Mom's "not tonight" (.alarm.4 to her, .trap.mom
  // to her sister). The second time, the one dart he kept back (.dart). After that nobody tries (.again); and the darts
  // stay on the runner (.after, looking at the door).
  "home.son.look.mom": ["mom", "'NO GIRLS ALLOWED.' He spelled all three words correctly this year. I was so proud that I very nearly obeyed it."],
  "home.son.look.bigsis": ["bigsis", "My brother's door. 'NO GIRLS ALLOWED', warning tape, and smaller notices. One is addressed to me personally."],
  "home.son.look.lilsis": ["lilsis", "NO GIRLS ALLOWED? I'm not a girl. I'm a SISTER. That's a whole different thing."],
  "home.son.use.mom": ["mom", "'NO GIRLS ALLOWED.' I'm his mother, which he's always counted as a separate thing. ...Not tonight."],   // PASS-17H: Mom's formality
  "home.son.use.bigsis": ["bigsis", "I decline to guess. It will be about snacks, and I have my dignity. I shall simply open the door."],
  "home.son.alarm.1": ["son", "'HALT! This is Operation No Girls. What's the password?'"],
  "home.son.alarm.2": ["lilsis", "'The password is: I still want a dog.' ...That's how he says it. I've watched."],
  "home.son.alarm.3": ["son", "'Password CORRECT. Ten out of ten. You may enter, me.'"],
  "home.son.trap.bigsis": ["bigsis", "I don't want to go in there. The rug is probably booby-trapped."],
  "home.son.trap.lilsis": ["lilsis", "It said CORRECT! You can't say ten out of ten and then SHOOT people! ...It was a GOOD trap, though."],
  "home.son.trap.lilsis.2": ["lilsis", "He GOT you! SEVEN darts! ...Right. I'm making a sign for MY door. NO BROTHERS. Except on Saturdays."],
  "home.son.trap.mom": ["mom", "Not tonight, darling. I am not ready to look at that room with nobody in it."],
  "home.son.alarm.4": ["mom", "Not tonight, sweetheart. I am not ready to look at that room with nobody in it."],
  "home.son.alarm.5": ["lilsis", "...Okay. I'll shut it. He'd want me to shut it."],
  "home.son.again": ["lilsis", "Mommy said not tonight. I can wait. I'm getting good at it."],
  "home.son.dart.lilsis": ["lilsis", "ONE more! He saved one for me! ...That's not a trap anymore. That's just RUDE."],
  "home.son.dart.bigsis": ["bigsis", "One more. He kept one in reserve. I respect that, and I am still not going in."],
  "home.son.again.bigsis": ["bigsis", "No. I stand by what I said about the rug."],
  "home.son.after.mom": ["mom", "His darts, all over my runner. I'm leaving them exactly where they fell. He'll want to count them."],   // PASS-17H: Mom's formality ('shall')
  "home.son.after.bigsis": ["bigsis", "Foam darts all over the runner. He will want a full report. I intend to say it was adequate."],
  "home.son.after.lilsis": ["lilsis", "His darts are ALL over the rug. Nobody pick them up. That's EVIDENCE."],
  "home.son.key.mom": ["mom", "That key is for the study. This door has never had a lock. Only opinions."],   // PASS-17H: one darling fewer
  "home.son.key.bigsis": ["bigsis", "His door has no keyhole. It has a toy alarm and a great deal of confidence."],
  "home.son.key.lilsis": ["lilsis", "It doesn't have a keyhole! It has a PASSWORD. Passwords are keys you say."],
  "home.bag.mom": ["mom", "His school bag, on its peg. Exactly where it can never be found on a school morning."],
  "home.bag.bigsis": ["bigsis", "My brother's bag. There is a sandwich in it from before the holidays. I will not be the one who finds it."],
  "home.bag.lilsis": ["lilsis", "His school bag! I'm guarding it till he's back. Nobody touch it. Not even me."],

  // ---- chain A: Dad's notice, and the study door
  "home.sign.lilsis": ["lilsis", "'LOST YOUR KEY? IT IS WITH THE OTHER EIGHTY-EIGHT.' Eighty-eight keys! Daddy has a LOT of doors."],
  "home.sign.bigsis.1": ["bigsis", "'Lost your key? It is with the other eighty-eight.' Signed, 'The Management'. Eighty-eight of what?"],
  "home.sign.bigsis.2": ["bigsis", "...Keys. Fun fact: a standard piano has eighty-eight keys. Dad has hidden the study key in the piano."],
  "home.sign.mom.react": ["mom", "He has hidden a key in MY piano."],
  "home.sign.mom.1": ["mom", "'Lost your key? It is with the other eighty-eight.' Signed, 'The Management'. Oh, my love."],
  "home.sign.mom.2": ["mom", "A matter of record: a full-size piano has eighty-eight keys. He has hidden a key in MY piano."],
  "home.sign.bigsis.react": ["bigsis", "Eighty-eight. I was half a second behind you, Mother. Half."],
  "home.sign.thunk.mom": ["mom", "'The other eighty-eight.' Piano keys. So that's what he dropped into my piano: his own door key."],   // PASS-17H: Mom's formality
  "home.sign.thunk.bigsis": ["bigsis", "'The other eighty-eight.' Eighty-eight piano keys. So THAT is what is lying on the hammers."],
  "home.sign.again.mom": ["mom", "'Authorized personnel only.' In a family of five. He means himself and the boy."],
  "home.sign.again.bigsis": ["bigsis", "Block capitals, no spelling mistakes, and one riddle. For Dad, that is a formal document."],
  "home.study.look.mom": ["mom", "Your father's study. He locks one door in this house, and tonight it's the one we need."],   // PASS-17H: Mom's formality
  "home.study.look.bigsis": ["bigsis", "Dad's study. One lock, one notice, no key. In that order."],
  "home.study.look.lilsis": ["lilsis", "Daddy's room. It's for 'planning'. I've seen planning. It's maps and snacks."],
  "home.study.open.mom": ["mom", "Open. I half expect him to be sitting in there, saying 'well, well, well'."],
  "home.study.open.bigsis": ["bigsis", "Trip Headquarters is open. For the record, I am authorized personnel now."],
  "home.study.open.lilsis": ["lilsis", "It's OPEN! We're allowed in Daddy's room! Don't touch anything. I'M going to touch everything."],
  "home.study.locked.mom": ["mom", "Locked. Naturally. And he's left us a notice instead of a key."],   // PASS-17H: Mom's formality
  "home.study.locked.bigsis": ["bigsis", "Locked. Dad's notice says where the key is. It simply does not say it in plain English."],
  "home.study.locked.lilsis": ["lilsis", "It's LOCKED. Daddy! Open up! ...He can't hear me. I forgot."],
  "home.study.theirs.mom.bigsis": ["mom", "Your big sister is holding the key, darling. Let her do the honors."],
  "home.study.theirs.mom.lilsis": ["mom", "Your little sister is holding the key. She fetched it, so she gets to turn it."],   // PASS-17H: Mom's formality ('shall')
  "home.study.theirs.bigsis.mom": ["bigsis", "Mom has the key. Technically she outranks the Management."],
  "home.study.theirs.bigsis.lilsis": ["bigsis", "My sister has the key. She has not put it down since. She will be sleeping with it, I expect."],
  "home.study.theirs.lilsis.mom": ["lilsis", "Mommy's got the key! Mommy, do the door! Do the DOOR!"],
  "home.study.theirs.lilsis.bigsis": ["lilsis", "SHE's got the key. She's being slow about it on PURPOSE."],
  "home.study.unlock.mom": ["mom", "There. 'Authorized personnel only.' I authorized myself on our wedding day."],
  "home.study.unlock.bigsis": ["bigsis", "It turns. Trip Headquarters is under new management."],
  "home.study.unlock.lilsis": ["lilsis", "It WENT! I opened Daddy's door! With the key I got out of the PIANO!"],

  // ---- what they say to each other on the landing
  "home.talk.landing.mom.bigsis.sign.a": ["mom", "Your father's notice is a riddle. What do you make of it?"],   // PASS-17H: one darling fewer
  "home.talk.landing.mom.bigsis.sign.b": ["bigsis", "There is a number in it. I should like to read it again. Properly, with my finger."],
  "home.talk.landing.mom.bigsis.1a": ["mom", "As a schoolboy, George Washington copied out 110 Rules of Civility."],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.talk.landing.mom.bigsis.1b": ["bigsis", "Is one of them 'Do not hide keys in your wife's piano'?"],
  "home.talk.landing.mom.bigsis.1c": ["mom", "It's implied, darling. Throughout."],   // PASS-17H: Mom's formality
  "home.talk.landing.mom.bigsis.2a": ["mom", "You take after me, you know. It's the nicest thing I can say about either of us."],   // PASS-17H: Mom's formality
  "home.talk.landing.mom.bigsis.2b": ["bigsis", "I take after you with footnotes."],
  "home.talk.landing.mom.lilsis.1a": ["lilsis", "Mommy, is my brother scared? Because I'm NOT. You can tell him I said."],
  "home.talk.landing.mom.lilsis.1b": ["mom", "Your brother has never been scared of anything in his life. That's the part that scares me."],   // PASS-17H: funnier: a reply that answers back
  "home.talk.landing.mom.lilsis.2a": ["mom", "Hold the rail on the stairs, sweetheart."],
  "home.talk.landing.mom.lilsis.2b": ["lilsis", "I AM holding it."],
  "home.talk.landing.mom.lilsis.2c": ["mom", "With a hand, darling."],
  "home.talk.landing.bigsis.mom.1a": ["bigsis", "Mom. When they are back, I intend to be extremely calm about it."],
  "home.talk.landing.bigsis.mom.1b": ["mom", "Of course you do, darling. So do I. We'll be calm together, at some volume."],   // PASS-17H: Mom's formality ('shall')
  "home.talk.landing.bigsis.mom.2a": ["bigsis", "Fun fact: John Adams and Thomas Jefferson died on the same day. The fourth of July, 1826."],
  "home.talk.landing.bigsis.mom.2b": ["mom", "Fifty years to the day after the Declaration. A matter of record. And I told YOU that one."],
  "home.talk.landing.bigsis.lilsis.1a": ["bigsis", "Do not slide down the banister."],
  "home.talk.landing.bigsis.lilsis.1b": ["lilsis", "I wasn't GOING to. ...Now I'm thinking about it."],
  "home.talk.landing.bigsis.lilsis.2a": ["lilsis", "Do you know his password?"],
  "home.talk.landing.bigsis.lilsis.2b": ["bigsis", "I have never asked. A person is entitled to one secret. He has chosen a noisy one."],
  "home.talk.landing.lilsis.mom.1a": ["lilsis", "Mommy, can I say my bedtime prayer if it isn't bedtime?"],
  "home.talk.landing.lilsis.mom.1b": ["mom", "Any time you like, my love. He isn't listening for the clock. He's listening for you."],   // PASS-17H: a faith line said as a mother says it
  "home.talk.landing.lilsis.mom.2a": ["lilsis", "When Daddy's home, can we have dinner again? The SAME dinner? I'm saving him my potato."],
  "home.talk.landing.lilsis.mom.2b": ["mom", "A fresh one, darling. That one has done its duty."],
  "home.talk.landing.lilsis.bigsis.1a": ["lilsis", "Why doesn't YOUR ladder have stickers?"],
  "home.talk.landing.lilsis.bigsis.1b": ["bigsis", "It has a card. One card. It is not boring. It is restrained."],
  "home.talk.landing.lilsis.bigsis.2a": ["lilsis", "Are you writing this down for your book?"],
  "home.talk.landing.lilsis.bigsis.2b": ["bigsis", "Every word."],
  "home.talk.landing.lilsis.bigsis.2c": ["lilsis", "Write that I was BRAVE."],

  // =====================================================================================================
  // DAD'S STUDY
  // =====================================================================================================
  "home.study.first.1": ["mom", "Trip Headquarters. He hasn't let me dust in here since March."],   // PASS-17H: Mom's formality
  "home.study.first.2": ["bigsis", "The mainframe is on the desk. And that box on the shelves is the 'family vault'. It has a label."],
  "home.study.first.3": ["lilsis", "Something's BLINKING! Over there! On the drawer thing!"],

  // ---- chain C: the family computer, and the note on it
  "home.pc.look.mom": ["mom", "The family computer. Your father calls it 'the mainframe'. It is nine years old and it sighs when you switch it on."],
  "home.pc.look.bigsis": ["bigsis", "Our computer. It runs the family map. It also runs. Technically."],
  "home.pc.look.lilsis": ["lilsis", "The computer! It has a game where a cat eats numbers."],
  "home.pc.offline.mom": ["mom", "'No internet.' I see. It was working perfectly well until your father improved it."],
  "home.pc.offline.bigsis": ["bigsis", "No connection. Fun fact: the first message ever sent on the network that became the internet was 'LO'. They were typing LOGIN, and it crashed. October 1969."],
  "home.pc.offline.bigsis2": ["bigsis", "So this is traditional."],
  "home.pc.offline.lilsis": ["lilsis", "It says NO. Computers aren't allowed to say no. I'm telling Mommy."],
  "home.pc.login.mom": ["mom", "It wants a password. Four numbers. 'Forgot it? Ask Dad.' I would dearly love to."],
  "home.pc.login.bigsis": ["bigsis", "Four digits. Ten thousand possibilities. Dad will have written it down somewhere. He always does."],
  "home.pc.login.lilsis": ["lilsis", "One, two, three, four! ... It said no AGAIN."],
  "home.pc.type.mom": ["mom", "One. Nine. Two. Eight."],
  "home.pc.type.bigsis": ["bigsis", "One, nine, two, eight. I type with all ten fingers. It is not difficult."],
  "home.pc.type.lilsis": ["lilsis", "One! Nine! Two! Eight! I typed it with ONE finger."],
  "home.pc.question.mom": ["mom", "'What did you promise on your wedding day?' Oh, my love. You would."],
  "home.pc.question.bigsis": ["bigsis", "'What did you promise on your wedding day?' I was not invited to the wedding. Mother?"],
  "home.pc.question.lilsis": ["lilsis", "It's asking about a wedding. I wasn't BORN. Mommy!"],
  "home.pc.pick.love": ["mom", "To love, honor and cherish."],
  "home.pc.pick.scenic": ["mom", "To always take the scenic route."],
  "home.pc.pick.directions": ["mom", "To never ask for directions."],
  "home.pc.wrong.love": ["mom", "No? I did say that. I had hoped he was listening."],
  "home.pc.wrong.scenic": ["mom", "No. That was not a promise. That was a warning."],
  "home.pc.right": ["mom", "He promised me he would never ask for directions. It is the one promise he has always kept."],
  "home.pc.map.1": ["mom", "There. 'Dad's phone. Last seen 5:47 p.m. Thirty-seven miles past Last Gas.' In the middle of Nevada."],
  "home.pc.map.2": ["bigsis", "That is not on the way home. That is not on the way to anywhere."],
  "home.pc.map.six": ["bigsis", "5:47. His message was at 5:41. Six minutes after that, his phone stops."],
  "home.pc.map.3": ["lilsis", "Is Nevada past the mailbox?"],
  "home.pc.map.4": ["mom", "A little past the mailbox, darling. Shoes on, both of you. We leave tonight."],
  "home.pc.done.mom": ["mom", "One dot, in the middle of nothing. I have looked at it quite long enough."],
  "home.pc.done.bigsis": ["bigsis", "Thirty-seven miles past Last Gas. I have memorized it. I memorize everything."],
  "home.pc.done.lilsis": ["lilsis", "The dot is Daddy. Hi, dot."],
  "home.pc.pencil.lilsis": ["lilsis", "I poked the screen with Daddy's pencil. Now there's a dot. It's not the right kind of dot."],

  "home.note.look.mom": ["mom", "Your father's handwriting. 'Password: the year of the best thing since.' Since WHAT, my love? He has left off the end."],
  "home.note.look.lilsis": ["lilsis", "It says 'PASS WORD'. And then more words. Daddy does the loopy Ys."],
  "home.note.take.mom": ["mom", "I will hold on to this. It is the nearest thing to your father in the house."],
  "home.note.take.lilsis": ["lilsis", "MINE. I mean: evidence."],
  "home.note.solve.1": ["bigsis", "'Password: the year of the best thing since.' ...Since sliced bread. With Dad, everything is the best thing since sliced bread."],
  "home.note.solve.2": ["bigsis", "Fun fact: sliced bread was first sold on the seventh of July, 1928, in Chillicothe, Missouri."],
  "home.note.solve.3": ["bigsis", "The password is 1928. Dad, that is so... actually, that is quite good."],

  // ---- chain D: the answering machine, its tape, and Dad's last message
  "home.machine.look.mom": ["mom", "Your father's answering machine. It's older than you are, darling. And its tape is on the outside."],   // PASS-17H: Mom's formality
  "home.machine.look.bigsis": ["bigsis", "A machine with a cassette in it. 'One new message.' And a loop of tape hanging out like a tongue."],
  "home.machine.look.lilsis": ["lilsis", "I FIXED that last week! ...It was working before I fixed it."],
  "home.machine.ready.mom": ["mom", "Wound, and blinking. One new message. I want to hear it, and I don't."],   // PASS-17H: the speech that is really an essay
  "home.machine.ready.bigsis": ["bigsis", "The tape is back in. One new message. The button marked PLAY is the large one."],
  "home.machine.ready.lilsis": ["lilsis", "The answer machine's BLINKING! It's got an answer in it! Press the big button! PRESS it!"],
  "home.machine.flash": ["lilsis", "I shined my flashlight in its little window. There's two wheels in there. It has EYES."],
  "home.tape.need.mom": ["mom", "It wants winding back in, and for that I want a pencil. An ordinary wooden one."],
  "home.tape.need.bigsis": ["bigsis", "Fun fact: you can wind a cassette by turning its hub with a pencil. Mine are too slim. Dad's is not."],
  "home.tape.need.lilsis": ["lilsis", "I'm not allowed to fix it again. Mommy said. With her whole-name voice."],
  "home.tape.where": ["mom", "There's exactly one pencil in this house that can ever be found. It's on your father's crossword."],   // PASS-17H: Mom's formality
  "home.tape.has.mom": ["mom", "I have his pencil here. Stand aside, darlings. This is my department."],
  "home.tape.has.bigsis": ["bigsis", "I am holding Dad's pencil. Mom should be. She is the one who knows which way it turns."],
  "home.tape.has.lilsis": ["lilsis", "I've got Daddy's pencil! Mommy needs it. I'll give it to her. In a minute. Okay, NOW."],
  "home.tape.notme.bigsis": ["bigsis", "I know that it fits. I do not know how hard to turn. That tape is his voice. Mom should do this."],
  "home.tape.notme.lilsis": ["lilsis", "I'm not ALLOWED. I fixed it last time. Mommy has to do it. She needs the pencil."],
  "home.tape.wind.1": ["mom", "I recorded entire musicals off the radio with one of these. Pencil in the hub, and gently."],
  "home.tape.wind.2": ["mom", "There. Every inch of it back in, and not one crease."],
  "home.tape.wind.3": ["bigsis", "So that is the knack. Slower than you want to. I am writing it down."],
  "home.tape.wind.4": ["lilsis", "It's still BLINKING. It wants to tell us something! Can I press it? I'm asking really FAST."],
  "home.msg.1": ["dad", "'Hi, honey. It's 5:41 and we are making GREAT time. I found a shortcut.'"],
  "home.msg.2": ["dad", "'Thirty-seven miles past the last gas station and not one other car. The boy says hi.'"],
  "home.msg.3": ["dad", "'He says the road sign up ahead looks funny. ...Huh. That IS funny.'"],
  "home.msg.4": ["dad", "'That sign just changed its--'"],
  "home.msg.after.lilsis": ["lilsis", "Changed its WHAT? Daddy! Changed its WHAT?"],
  "home.msg.after.bigsis": ["bigsis", "5:41 p.m. on the tape. That is the last anybody heard of them. I am writing down the minute."],
  "home.msg.after.bigsis.six": ["bigsis", "5:41 on the tape. His phone was last seen at 5:47. Whatever happened took six minutes."],
  "home.msg.after.mom": ["mom", "I do not need to hear it twice. He sounded happy."],
  "home.msg.again.mom": ["mom", "Once was enough, my love. I have it by heart already."],
  "home.msg.again.bigsis": ["bigsis", "5:41 p.m. I have the whole message memorized. Including the hiss."],
  "home.msg.again.lilsis": ["lilsis", "Changed its WHAT. I'm going to ask him. FIRST thing."],

  // ---- chain E: the family vault
  "home.vault.read.mom": ["mom", "'The year WE THE PEOPLE got it in writing.' ...I do NOT bring it up. Not often."],
  "home.vault.read.bigsis": ["bigsis", "'The year We the People got it in writing.' I can think of three years. Mom will know which."],
  "home.vault.read.lilsis": ["lilsis", "It says 'FAMILY VAULT'. And 'Your mother will know.' MOMMY! The box says you know!"],
  "home.vault.pick.1776": ["mom", "Seventeen seventy-six."],
  "home.vault.pick.1787": ["mom", "Seventeen eighty-seven."],
  "home.vault.pick.1789": ["mom", "Seventeen eighty-nine."],
  "home.vault.pick.later": ["mom", "Let me think about it."],
  "home.vault.wrong.1776": ["mom", "No. 1776 is the Declaration, the Fourth of July. 'We the People' came later."],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.vault.wrong.1789": ["mom", "No. In 1789 the new government began, and General Washington took the oath. It was written by then."],
  "home.vault.right.1": ["mom", "1787. Signed in Philadelphia on the seventeenth of September. He does listen. Just not at the time."],
  "home.vault.right.2": ["mom", "My spare car key. Two ketchup packets. And a card: 'KNEW YOU'D KNOW. - THE MANAGEMENT.'"],
  "home.vault.right.3": ["bigsis", "He keeps ketchup in a vault."],
  "home.vault.right.4": ["lilsis", "Is the ketchup a treasure? Can I have the treasure?"],
  "home.vault.right.5": ["mom", "The ketchup stays, darling. He's saving it. I've never asked what for."],   // PASS-17H: Mom's formality
  "home.vault.done.mom": ["mom", "Empty, but for two ketchup packets and a card. I've left him the ketchup."],   // PASS-17H: Mom's formality
  "home.vault.done.bigsis": ["bigsis", "The family vault, opened by the Constitution. I am going to enjoy footnoting that."],
  "home.vault.done.lilsis": ["lilsis", "The treasure box is open! It's got ketchup. Daddy's treasure is ketchup."],
  "home.vault.key.mom": ["mom", "The vault has a dial, not a keyhole. Your father does like a dial."],   // PASS-17H: one darling fewer
  "home.vault.key.bigsis": ["bigsis", "It is a combination lock. A key would be cheating, and Dad does not cheat at his own riddles."],
  "home.vault.key.lilsis": ["lilsis", "No hole for a key. It's got a wheel with numbers. The numbers go CLICK."],

  // ---- the rest of the study
  "home.wallmap.mom": ["mom", "His route, in red wool. And a shorter piece, in yellow, across a part of the map with nothing on it."],
  "home.wallmap.bigsis": ["bigsis", "The yellow piece cuts the corner on a road the map says ends. Yellow is for caution. He chose it himself."],
  "home.wallmap.lilsis": ["lilsis", "The pin is our house! Hi, house. The red string is Daddy driving. The yellow one is Daddy being clever."],
  "home.wallmap.pencil.mom": ["mom", "I'm not drawing on his map. I will, however, be having a word with him about that yellow string."],   // PASS-17H: Mom's formality ('shall')
  "home.wallmap.pencil.bigsis": ["bigsis", "I am not going to correct Dad's map. I am going to correct Dad. Later. In person."],
  "home.wallmap.pencil.lilsis": ["lilsis", "I drew a tiny car on the string. And a hen in the window. That's the General. Now they're BOTH on the map."],
  "home.corkboard.mom": ["mom", "'Operation Road Trip.' Your brother's plan. Step one is 'snacks'. So are steps two through five."],
  "home.corkboard.bigsis": ["bigsis", "My brother's snack schedule. Hourly. He has rated each snack out of ten, in advance."],
  "home.corkboard.lilsis": ["lilsis", "He drew the wagon! He made the luggage taller than the car. That part's TRUE."],
  "home.shelves.mom": ["mom", "His manuals. Every one of them read exactly as far as the middle."],
  "home.shelves.bigsis": ["bigsis", "Jars of screws, sorted by a system known only to Dad. One jar is labelled 'MISC'. So are the others."],
  "home.shelves.lilsis": ["lilsis", "Jars! That one's got googly eyes in it. I'm not saying whose."],
  "home.globe.mom": ["mom", "The globe. He spins it and says 'anywhere but the interstate'. I should have listened harder."],
  "home.globe.bigsis": ["bigsis", "A globe tells you where. Tonight I have a feeling 'where' is only half the question."],   // PASS-17H: truer; it plants 'when' without saying it
  "home.globe.lilsis": ["lilsis", "The WORLD! It opens in the middle, like an egg. Daddy says it's not an egg. It's SO an egg."],
  "home.globe.use.mom": ["mom", "I'm not spinning it. I know exactly which part of it I care about tonight."],   // PASS-17H: Mom's formality ('shall')
  "home.globe.use.bigsis": ["bigsis", "It stops on Nevada. It always stops on Nevada. Dad has leaned on it."],
  "home.globe.use.lilsis": ["lilsis", "WHEEE. I stopped it with my finger! Daddy's in... the ocean. That can't be right."],
  "home.study.window.mom": ["mom", "The driveway, from above. One oil spot, where the wagon lives. I'll be taking that up with him."],   // PASS-17H: Mom's formality ('shall')
  "home.study.window.bigsis": ["bigsis", "The whole street, from the highest window in the house. I have looked. It has not helped."],
  "home.study.window.lilsis": ["lilsis", "I can see my swing! Swings look sad in the dark. Tomorrow I'm going SO high. Daddy can push."],
  "home.banner.mom": ["mom", "'TRIP HEADQUARTERS.' Your father did TRIP, in blue. Your brother did the rest, one color to a letter."],
  "home.banner.bigsis": ["bigsis", "Dad ruled his four letters in pencil first. My brother did twelve freehand and added a car. His is the better half."],
  "home.banner.lilsis": ["lilsis", "I helped! I held the tape. Nobody put my name on it. I'll do it myself when Daddy's home. In PINK."],
  "home.plane.mom": ["mom", "The biplane. He and your brother built it in February. It took three weekends and every clothespin I own."],   // PASS-17H: American: clothespin
  "home.plane.bigsis": ["bigsis", "My brother's model biplane. It hangs on a thread. The thread was my condition for living under the same roof."],
  "home.plane.lilsis": ["lilsis", "The red airplane! It goes round if you blow. I'm not allowed to blow. I blow a LITTLE."],
  "home.boxes.mom": ["mom", "What wouldn't fit in the car. The tent, the cooler, and the box of maps. He left the maps."],   // PASS-17H: Mom's formality
  "home.boxes.bigsis": ["bigsis", "He left the maps behind. On purpose. The box says 'MAPS' in his own capitals, and he walked straight past it."],
  "home.boxes.lilsis": ["lilsis", "The cooler! ...It's empty. They took ALL the juice boxes. Daddy and I are going to have a TALK."],
  "home.study.door.mom": ["mom", "The landing. I'm leaving this door open behind us. He may hide the next key somewhere else."],   // PASS-17H: Mom's formality
  "home.study.door.bigsis": ["bigsis", "The way out. I am not finished in here. I may never be finished in here."],
  "home.study.door.lilsis": ["lilsis", "That's the door we opened with the key I got. Out of the PIANO."],

  // ---- what they say to each other in the study
  "home.talk.study.mom.bigsis.note.a": ["mom", "This note of your father's is about a year, darling. Years are your department."],
  "home.talk.study.mom.bigsis.note.b": ["bigsis", "Then may I have it? I read better with my hands."],
  "home.talk.study.mom.bigsis.1a": ["mom", "Bach wrote 'S.D.G.' at the end of many of his scores. 'To God alone the glory.'"],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.talk.study.mom.bigsis.1b": ["bigsis", "Dad writes 'THE MANAGEMENT' at the end of his."],
  "home.talk.study.mom.bigsis.2a": ["mom", "Your father planned this trip for a month, up here, with your brother."],
  "home.talk.study.mom.bigsis.2b": ["bigsis", "And then he took a shortcut."],
  "home.talk.study.mom.bigsis.2c": ["mom", "And then he took a shortcut."],
  "home.talk.study.mom.lilsis.1a": ["mom", "Hands, sweetheart."],
  "home.talk.study.mom.lilsis.1b": ["lilsis", "I'm not touching! I'm looking with my hands."],
  "home.talk.study.mom.lilsis.2a": ["lilsis", "Mommy, what's a headquarters?"],
  "home.talk.study.mom.lilsis.2b": ["mom", "It's where the plans get made, darling. The mistakes get made on the road."],   // PASS-17H: Mom's formality
  "home.talk.study.bigsis.mom.vault.a": ["bigsis", "Mother. 'The year We the People got it in writing.' Which year does he mean?"],
  "home.talk.study.bigsis.mom.vault.b": ["mom", "The one that's framed on our living-room wall. I'll do the dial myself."],   // PASS-17H: Mom's formality ('shall'); one darling fewer
  "home.talk.study.bigsis.mom.dot.a": ["bigsis", "Mother. What if they are not at the dot?"],
  "home.talk.study.bigsis.mom.dot.b": ["mom", "We do not stop the show for a missing cast member, darling. We go and fetch him."],
  "home.talk.study.bigsis.mom.1a": ["bigsis", "Dad calls this computer 'the mainframe'."],
  "home.talk.study.bigsis.mom.1b": ["mom", "He calls the car 'she', and himself 'the Management'. He has a gift for names."],
  "home.talk.study.bigsis.mom.2a": ["bigsis", "If he had simply told us the route..."],
  "home.talk.study.bigsis.mom.2b": ["mom", "Then it wouldn't have been a shortcut, darling. It would have been a plan."],   // PASS-17H: Mom's formality
  "home.talk.study.bigsis.lilsis.1a": ["bigsis", "Do not spin the globe. Do not open the jars. Do not fix anything."],
  "home.talk.study.bigsis.lilsis.1b": ["lilsis", "That's ALL the good ones."],
  "home.talk.study.bigsis.lilsis.2a": ["lilsis", "What's a mainframe?"],
  "home.talk.study.bigsis.lilsis.2b": ["bigsis", "It is what Dad calls a computer he has owned for nine years. It is a term of affection."],
  "home.talk.study.lilsis.mom.tape.a": ["lilsis", "Mommy, I only fixed the tape machine a LITTLE."],
  "home.talk.study.lilsis.mom.tape.b": ["mom", "I know, sweetheart. I can mend it. I want one ordinary pencil, and a moment's quiet."],
  "home.talk.study.lilsis.mom.1a": ["lilsis", "Is Daddy in trouble?"],
  "home.talk.study.lilsis.mom.1b": ["mom", "A little, my love. He has to come home first. The trouble will keep."],   // PASS-17H: Mom's formality
  "home.talk.study.lilsis.mom.2a": ["lilsis", "Mommy, why does Daddy have SO many jars?"],
  "home.talk.study.lilsis.mom.2b": ["mom", "Because he has so many screws. And he has so many screws because he has so many jars."],   // PASS-17H: funnier: the answer goes round in a circle; one darling fewer
  "home.talk.study.lilsis.bigsis.1a": ["lilsis", "My tooth's SO loose. But it's not allowed out till Daddy's home. He has to SEE it."],
  "home.talk.study.lilsis.bigsis.1b": ["bigsis", "You are negotiating with a tooth. I would not bet against you."],
  "home.talk.study.lilsis.bigsis.2a": ["lilsis", "If the computer's broken, I can fix it. I fixed the tape machine."],
  "home.talk.study.lilsis.bigsis.2b": ["bigsis", "That is exactly why I am standing between you and the computer."],

  // =====================================================================================================
  // LITTLE SISTER'S ROOM (it was the girls' room until Big Sister's thirteenth birthday). A kingdom of chickens.
  // =====================================================================================================
  "home.lilroom.first.1": ["lilsis", "Welcome to MY room! Rule one: don't step on the rug. The rug is an EGG. Nobody steps on an egg."],
  "home.lilroom.first.2": ["bigsis", "I used to live in here. It has since been annexed by poultry."],

  "home.lilroom.window.mom": ["mom", "The maple, and the moon in it. She used to think the tree was holding it up. I never corrected her."],
  "home.lilroom.window.bigsis": ["bigsis", "Chicken curtains. And over the window, a paper rooster. His job is the weather. I have been told his name. Twice."],
  "home.lilroom.window.lilsis": ["lilsis", "The tree taps on the glass at night. It's saying hi. I say hi back so it knows."],
  "home.drawings.mom": ["mom", "The five of us and the wagon, with a hen on the roof. She drew your father the biggest. He was so pleased."],
  "home.drawings.bigsis": ["bigsis", "Her drawings. Chickens, mostly. In the family one I have no neck, and the hen has. I have raised it with the artist."],
  "home.drawings.lilsis": ["lilsis", "That's all of us and the car! General Feathers is on the roof, on lookout. Keep an eye on Daddy, General!"],

  // ---- the chickens. Every one has a name and a rank or a job; "Chickens KNOW." is said here for the first time
  "home.chart.mom": ["mom", "'MY CHICKENS.' Twelve of them, drawn from life. The General has a star. I'm told the Admiral is cross about it."],   // PASS-17H: Mom's formality
  "home.chart.bigsis": ["bigsis", "Twelve chickens. I know every name, rank and job. I did not set out to. She quizzes me at breakfast."],
  "home.chart.lilsis": ["lilsis", "MY CHICKENS. All twelve! The one with the star is General Feathers. You go up a rank every time you go in the wash."],
  "home.flock.mom": ["mom", "Her flock. Every one of them has been through my washing machine, and has come out with a promotion."],
  "home.flock.bigsis": ["bigsis", "Admiral Doodle on top. Corporal Speckle. Private Peep. Each has a name, a rank and a job. I know them all. Against my will."],
  "home.flock.lilsis": ["lilsis", "That's the flock. Admiral Doodle's the big one on top. He's in charge of mornings. Everybody's very quiet tonight."],
  "home.flock.lilsis2": ["lilsis", "They know something's up. They knew before I did. Chickens KNOW."],
  "home.teaparty.mom": ["mom", "Four chickens at tea, and a spotted teapot. I was invited last week. I was told my manners would do."],
  "home.teaparty.bigsis": ["bigsis", "Four chickens and a spotted teapot. The tea is water. The water is from Tuesday. I checked. I regret checking."],
  "home.teaparty.lilsis": ["lilsis", "It's a tea party! Mrs. Biscuit poured. Nobody's drinking yet. They're waiting for the General. It's MANNERS."],
  "home.coop.mom": ["mom", "It was a dollhouse. The dolls were asked to leave. I understand they are in the toy box, and that it was amicable."],
  "home.coop.bigsis": ["bigsis", "The hen house has electric light. I did the wiring. I was told it was for dolls. I was misled."],
  "home.coop.lilsis": ["lilsis", "Everybody in my hen house is home. I checked. Twice."],
  "home.coop.flash": ["lilsis", "I shined my flashlight in their window. They didn't even blink. They're very brave hens."],
  // (Matthew 23:37. Those nine words, and no more of the verse, are quoted.)
  "home.nest.mom": ["mom", "'...even as a hen gathereth her chickens under her wings'..."],   // PASS-17H: reference aloud; the Bible fact tacked on
  "home.nest.mom2": ["mom", "Tonight I know just how the hen feels."],
  "home.nest.bigsis": ["bigsis", "'NEST.' A cardboard box, straw from the garden, and a hen who has sat on plastic eggs since March. I admire her patience."],
  "home.nest.lilsis": ["lilsis", "That's the NEST. Henrietta's sitting on the eggs. You can't rush eggs. They're plastic, so it takes EXTRA long."],

  // ---- her bed, and the place kept on the pillow for General Feathers, who went on the trip in Daddy's suitcase
  "home.lilbed.mom": ["mom", "A bed that has been jumped on. Recently, and with conviction."],
  "home.lilbed.bigsis": ["bigsis", "Her bed. Hens on the quilt, hens on the bed, and the non-hens ranked below them. The rankings change. There are tears."],
  "home.lilbed.lilsis": ["lilsis", "My bed! The officers sleep there. I sleep in my FORT. The bed is for officers. And jumping."],
  "home.pillow.mom": ["mom", "The General's place, kept. I found the first draft of her note to your father. It said 'DO WHAT SHE SAYS' twice."],
  "home.pillow.bigsis": ["bigsis", "'RESERVED.' For a stuffed hen with one blue eye and a medal. She outranks me. I have seen the chart."],
  "home.pillow.lilsis": ["lilsis", "That's General Feathers' place. RESERVED. She's on the trip, in Daddy's suitcase. To keep an eye on him."],
  "home.pillow.lilsis2": ["lilsis", "I'm not worried about the General. I'm a LITTLE worried about Daddy. That's why I SENT her. He needs supervising."],
  "home.lamp.mom": ["mom", "The rooster lamp. She won't sleep without it. Nor, I suspect, would the rooster."],   // PASS-17H: Mom's formality
  "home.lamp.bigsis": ["bigsis", "A lamp shaped like a rooster. She stood in front of the shop window until it was hers. It took a week."],
  "home.lamp.lilsis": ["lilsis", "My rooster lamp! He stays on ALL night. Roosters are supposed to get up early. He never even goes to BED."],

  // ---- chain B: the blanket fort, and the flashlight in it, which is dead
  "home.fort.look.mom": ["mom", "Two chairs, a drying rack and every blanket she owns. Her flashlight is just inside the door."],   // PASS-17H: American: drying rack
  "home.fort.look.bigsis": ["bigsis", "'NO BIG SISTERS.' There is one big sister in this house. The sign is not a general statement."],
  "home.fort.look.lilsis": ["lilsis", "My FORT. It's got lights and a sign and my flashlight and a secret. I'm not telling the secret."],
  "home.fort.empty.mom": ["mom", "The fort. It's better built than your father's shelves. I haven't told either of them."],   // PASS-17H: Mom's formality
  "home.fort.empty.bigsis": ["bigsis", "'NO BIG SISTERS.' I have never once tried to go in. That is what makes the sign so hurtful."],
  "home.fort.empty.lilsis": ["lilsis", "My fort. I've got my flashlight now. The secret's still in there. It's a cookie."],
  "home.fort.use.mom": ["mom", "Her fort, and her flashlight. You don't go into a lady's fort without an invitation. I taught her that myself."],   // PASS-17H: Mom's formality ('One does not')
  "home.fort.use.bigsis": ["bigsis", "'NO BIG SISTERS.' I respect a posted boundary. Also I would not fit, and she would never let it go."],
  "home.flashlight.mom": ["mom", "Her flashlight, just inside the door of her fort. It's hers to fetch, and nobody else's. Her rule, and a good one."],   // PASS-17H: Mom's formality
  "home.flashlight.bigsis": ["bigsis", "Her flashlight. It is inside the sign's jurisdiction. I am not reaching past that sign."],
  "home.flashlight.lilsis": ["lilsis", "My flashlight! It lives right inside my fort so I can find it in the dark. That's when you NEED one."],
  "home.fort.take.dark": ["lilsis", "MY flashlight! Now the closet can't be dark at me. CLICK. ...Click? CLICK CLICK CLICK."],
  "home.fort.take.early": ["lilsis", "My flashlight! I'm bringing it. You never know when it's going to be dark. CLICK. ...Click?"],
  "home.fort.take.2": ["lilsis", "It's DEAD. I used it all up last night. I was reading to the flock under the blanket. They wanted the WHOLE book."],
  "home.fort.take.3": ["mom", "Then it wants batteries, sweetheart. And I haven't seen one that size in this house since Easter."],   // PASS-17H: Mom's formality
  "home.fort.take.4": ["bigsis", "...There are four. In my sound machine. In the Retreat. I should like it noted that I said so myself."],
  "home.fort.again": ["lilsis", "I went in and came out again. Everything's okay in there. The cookie's okay."],
  "home.fort.putback.mom": ["mom", "Not yet, darling. Your sister will be wanting that."],
  "home.fort.putback.bigsis": ["bigsis", "I am not permitted within arm's reach of that fort. I shall hold the flashlight until relieved."],
  "home.fort.putback.lilsis": ["lilsis", "No! We NEED it. It can go home after."],
  "home.lilroom.door.mom": ["mom", "The landing. Lights off when we go, girls. ...No. Leave them on tonight."],
  "home.lilroom.door.bigsis": ["bigsis", "The way out. There is a hen on this side of the door as well. Of course there is."],
  "home.lilroom.door.lilsis": ["lilsis", "The door! There's a hen on it so the door knows whose door it is."],

  // ---- what they say to each other in Little Sister's room
  "home.talk.lilroom.mom.bigsis.1a": ["mom", "How's the novel, darling?"],   // PASS-17H: Mom's formality
  "home.talk.lilroom.mom.bigsis.1b": ["bigsis", "It has acquired a plot this evening. I did not ask for one."],
  "home.talk.lilroom.mom.bigsis.2a": ["mom", "You shared this room once, darling. Do you miss it?"],
  "home.talk.lilroom.mom.bigsis.2b": ["bigsis", "I miss the window, Mother. I do not miss being counted at bedtime. With the flock. As one of the flock."],
  "home.talk.lilroom.mom.lilsis.flash.a": ["mom", "Your flashlight's in your fort, sweetheart, and only you are allowed in."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.mom.lilsis.flash.b": ["lilsis", "I KNOW. I made the rule. It's a GOOD rule. I'm already getting it. Stand back, everybody."],
  "home.talk.lilroom.mom.lilsis.1a": ["mom", "Did you say your verse tonight, sweetheart?"],
  "home.talk.lilroom.mom.lilsis.1b": ["lilsis", "Twice. Once for me and once for my brother. He forgets."],
  "home.talk.lilroom.mom.lilsis.2a": ["lilsis", "Mommy, can Daddy sleep in my fort when he's back?"],
  "home.talk.lilroom.mom.lilsis.2b": ["mom", "He'd be honored, my love. He also wouldn't fit. He'll try anyway."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.bigsis.mom.1a": ["bigsis", "Mom, did you ever want to be on a real stage? A big one?"],
  "home.talk.lilroom.bigsis.mom.1b": ["mom", "I'm on one every day, darling. I direct, I stage-manage, and nobody ever knows their lines."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.bigsis.mom.2a": ["bigsis", "I have decided what the next chapter is called. 'Places, Girls.'"],
  "home.talk.lilroom.bigsis.mom.2b": ["mom", "I expect a credit."],   // PASS-17H: Mom's formality ('I should like'); funnier
  "home.talk.lilroom.bigsis.lilsis.1a": ["bigsis", "Which one is Corporal Speckle? I have forgotten."],
  "home.talk.lilroom.bigsis.lilsis.1b": ["lilsis", "You have NOT. You never forget ANYTHING. You're being nice. ...It's the speckly one."],
  "home.talk.lilroom.bigsis.lilsis.2a": ["lilsis", "When I'm thirteen, do I get an attic?"],
  "home.talk.lilroom.bigsis.lilsis.2b": ["bigsis", "When you are thirteen I shall be nineteen, and you may have mine."],
  "home.talk.lilroom.bigsis.lilsis.2c": ["lilsis", "...I don't WANT yours. Yours has no chickens."],
  "home.talk.lilroom.lilsis.mom.1a": ["lilsis", "Mommy, look! I made my bed!"],
  "home.talk.lilroom.lilsis.mom.1b": ["mom", "You made A bed, darling. It's on the floor, out of every blanket we own. Well done."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.lilsis.mom.2a": ["lilsis", "Is it still today?"],
  "home.talk.lilroom.lilsis.mom.2b": ["mom", "It's still today, sweetheart. It's been today for a very long time."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.lilsis.bigsis.1a": ["lilsis", "Do you want to hold a chicken? It helps."],
  "home.talk.lilroom.lilsis.bigsis.1b": ["bigsis", "...The speckled one. Briefly. For morale."],
  "home.talk.lilroom.lilsis.bigsis.2a": ["lilsis", "Is your book about us?"],
  "home.talk.lilroom.lilsis.bigsis.2b": ["bigsis", "It is about a family of five. Any resemblance is entirely the point."],

  // =====================================================================================================
  // THE RETREAT: Big Sister's attic. Soft light, one sound, three rules. (Up here Little Sister whispers at full volume.)
  // =====================================================================================================
  "home.retreat.first.1": ["lilsis", "Boots OFF. One. ...Two. I'M DOING THE RULE. Everybody see me doing the rule!"],
  "home.retreat.first.2": ["bigsis", "Rule two is voices down. You are whispering at full volume."],
  "home.retreat.first.3": ["lilsis", "THIS IS MY WHISPER."],
  "home.retreat.first.4": ["mom", "Soft light, one sound, nothing out of place. Darling, it is a set. It is a very good set."],

  // ---- the rules, on their easel by the hatch (the close-up shows them, and what is written under the third in crayon)
  "home.rules.mom": ["mom", "Three rules, darling, and the third already under appeal. You haven't made a room. You've founded a republic."],   // PASS-17H: Mom's formality
  "home.rules.bigsis": ["bigsis", "My rules. I kept them to three, so that a person of seven could remember them. The crayon is not mine."],
  "home.rules.lilsis": ["lilsis", "Rule three is NOT FAIR. So I lodged a appeal. Mommy told me the word. It has a D in it for no reason."],

  // ---- Big Sister's timeline: where the game says how it counts the years, and what B.C. and A.D. mean.
  // Every year before Christ is the Bible's count, as Archbishop Ussher counted it (docs/CHARACTERS.md has the table).
  // The first time any of them looks along it, the three read it between them: .1 to .6, then .bigsis, .bigsis2, .mom, .lilsis.
  "home.timeline.1": ["bigsis", "My timeline. I used Archbishop Ussher's dates. He counted the years from the Bible's own genealogies."],
  "home.timeline.2": ["mom", "A matter of record: the Archbishop's book was published in 1650. And here are his years, on an attic wall, in felt pen."],
  "home.timeline.3": ["bigsis", "It begins at the left: 4004 B.C., the Creation. And here, 2348 B.C.: the Flood."],
  "home.timeline.4": ["lilsis", "There's not much paper before Abram! I thought the beginning would be the LONGEST bit."],
  "home.timeline.5": ["bigsis", "It is as long as it was. Here: 1921 B.C. Abram leaves Haran, and goes down into Egypt."],
  "home.timeline.6": ["bigsis", "1491 B.C.: the Exodus. And 44 B.C.: the Ides of March. That one is Rome's. It is on my wall anyway."],
  "home.timeline.bigsis": ["bigsis", "And at the red mark the years turn round. Before it they count down: B.C., 'before Christ'."],
  "home.timeline.bigsis2": ["bigsis", "After it they count up: A.D. It is Latin. Anno Domini, 'in the year of the Lord'."],
  "home.timeline.mom": ["mom", "Every year on that wall is counted from His birth. I've always loved that."],   // PASS-17H: a faith line said as a mother says it
  "home.timeline.lilsis": ["lilsis", "And I'm ON it! Right at the end. She did me in pencil. Everybody else gets PEN."],
  "home.timeline.bigsis3": ["bigsis", "Fun fact: a monk named Dionysius worked that count out in the year 525. It starts at the birth of Jesus."],
  "home.timeline.bigsis4": ["bigsis", "Cristofori's piano. The Constitution. Sliced bread. And at the far end, in pencil, my sister."],
  "home.timeline.again.mom": ["mom", "From the Creation to your little sister, on one strip of paper. I'd hate to have had to rule that line."],   // PASS-17H: Mom's formality ('I should not like')
  "home.timeline.again.lilsis": ["lilsis", "I'm the last thing on it. In PENCIL. When I do something big she has to do me in pen. That's the deal."],
  "home.timeline.pencil.mom": ["mom", "It's your sister's, darling. She does her own footnotes."],   // PASS-17H: Mom's formality ('One does not'); funnier
  "home.timeline.pencil.bigsis": ["bigsis", "Tonight goes on the timeline when I know what tonight was. Not before. And not in Dad's pencil."],
  "home.timeline.pencil.lilsis": ["lilsis", "I'm not allowed to draw on it. I drew a hen on it once, by the Flood. She's still there. She's SMALL."],

  // ---- chain B: the sound machine, and the only batteries of that size in the house
  "home.sound.look.mom": ["mom", "Her sound machine. One slow tune, in D major. Sensible girl. D major never panics."],   // PASS-17H: the speech that is really an essay; funnier
  "home.sound.look.bigsis": ["bigsis", "My sound machine. One tune, very slow, very soft. It is the only thing in this house that is calm on purpose."],
  "home.sound.look.lilsis": ["lilsis", "THE MUSIC BOX. It runs on batteries. I looked in the back. With my EYES. I'M WHISPERING."],
  "home.sound.use.mom": ["mom", "It's her room and her machine. I wouldn't dream of it."],   // PASS-17H: Mom's formality ('One does not'); one darling fewer
  "home.sound.use.bigsis": ["bigsis", "It stays on. Tonight of all nights. It is the only one of us that is calm."],
  "home.sound.use.lilsis": ["lilsis", "I'm not ALLOWED to touch anything up here. It's a rule. It's ALL the rules. And we signed a treaty."],
  "home.sound.take.mom": ["mom", "The batteries are in there, and they're not mine to take. Not from a daughter. Your sister has to do this herself."],   // PASS-17H: Mom's formality
  "home.sound.take.lilsis": ["lilsis", "The batteries are IN there! I can't touch it: rule AND treaty. So YOU have to. It's your music box. Go on."],
  "home.sound.give.1": ["bigsis", "The only batteries of that size in this house are in here. I have looked in every drawer. Twice."],
  "home.sound.give.2": ["bigsis", "Very well. The Retreat goes dark so that the internet may live."],
  "home.sound.give.3": ["lilsis", "IT STOPPED. ...Now I can hear the water. It's going tick, tick, tick."],
  "home.sound.give.4": ["bigsis", "Thank you. I shall be hearing that all night. I intend to mention this again."],
  "home.sound.give.5": ["mom", "You will, darling. Often. And every time, I'll say thank you and mean it."],   // PASS-17H: Mom's formality ('shall')
  "home.sound.quiet.mom": ["mom", "Silent. She gave up her music for her sister's flashlight, and she's only mentioned it twice. I'm very proud."],   // PASS-17H: Mom's formality
  "home.sound.quiet.bigsis": ["bigsis", "Silent. Now there is only the fountain, and the fountain sounds like a clock. I had been managing not to notice."],
  "home.sound.quiet.lilsis": ["lilsis", "It's quiet now. She took the batteries out FOR ME. I'm going to draw her a chicken. She'll say no. I'll draw it anyway."],
  "home.sound.putback.mom": ["mom", "Not into the machine, darling. They have an appointment with a pink flashlight."],
  "home.sound.putback.bigsis": ["bigsis", "They are not going back in. A sacrifice stays made. They go in my sister's flashlight."],
  "home.sound.putback.lilsis": ["lilsis", "They go in my FLASHLIGHT now. That's the whole point of them. And I can't touch the music box anyway."],
  "home.soundtable.mom": ["mom", "One table, two sounds. Music at one end, water at the other. It's very well blocked."],   // PASS-17H: Mom's formality
  "home.soundtable.bigsis": ["bigsis", "The sound table. The machine and the fountain, a hand's width apart. I measured. It matters."],
  "home.soundtable.lilsis": ["lilsis", "The music table. Music at THIS end, water at THAT end. I'd put a chicken in the middle. She says no."],
  "home.fountain.mom": ["mom", "A fountain, on a table, in an attic. And not one drop on the floor. She's my daughter."],   // PASS-17H: Mom's formality
  "home.fountain.bigsis": ["bigsis", "Water over stones. It is meant to sound like a brook. Tonight it sounds like a clock."],
  "home.fountain.lilsis": ["lilsis", "THE FOUNTAIN. It never stops. It makes me need to... never mind. I'M WHISPERING."],

  // ---- the rest of the Retreat
  "home.skylight.mom": ["mom", "Two skylights. She lies under the stars to think. So did I, at her age. I had to go outside for it."],
  "home.skylight.bigsis": ["bigsis", "A branch in the left one, the moon in the right. I have counted the little lights along the rafters, in fours. Twice."],
  "home.skylight.lilsis": ["lilsis", "You can see the MOON from her bed. I can see it from mine too. It's the same moon. I asked."],
  "home.retreat.window.mom": ["mom", "The round window. From the road, at night, it looks as if the house has one eye open. Tonight it has."],
  "home.retreat.window.bigsis": ["bigsis", "The round window looks down the road. I have not been watching the road. Much."],
  "home.retreat.window.lilsis": ["lilsis", "A ROUND window. Like on a boat. Her room's a boat and my room's a farm."],
  "home.plants.mom": ["mom", "Ferns, ivy, a small palm. Every one of them alive. In an attic. I can't keep parsley."],   // PASS-17H: Mom's formality
  "home.plants.bigsis": ["bigsis", "The ferns, the ivy and the palm. Each has its watering day. Not one of them is worried about anything. I envy them."],
  "home.plants.lilsis": ["lilsis", "Her jungle. There's no animals in it. I OFFERED her a chicken for it."],
  "home.towels.mom": ["mom", "A robe, rolled towels, slippers side by side. She's thirteen. I didn't own a robe until I was married."],   // PASS-17H: Mom's formality
  "home.towels.bigsis": ["bigsis", "Towels, rolled, not folded. A folded towel is a towel. A rolled towel is a decision."],
  "home.towels.lilsis": ["lilsis", "Towel rolls! They look like cinnamon buns. They're NOT. I checked."],
  "home.saltlamp.mom": ["mom", "A lamp made of salt. It gives the light of one tired candle, and she won't hear a word against it."],   // PASS-17H: Mom's formality
  "home.saltlamp.bigsis": ["bigsis", "A salt lamp. It is said to be calming. Tonight I have my doubts, and I have written them down."],
  "home.saltlamp.lilsis": ["lilsis", "The orange rock! It's SALT. I licked it once. It's really salt. I'm not allowed to lick the lamp."],
  "home.books.mom": ["mom", "Your sister's books. She's read every one of them. Several were mine first."],   // PASS-17H: Mom's formality; shorter
  "home.books.bigsis": ["bigsis", "My books. By color: red at one end, violet at the other. It is not a system. It is a view. The system is in my head."],
  "home.books.lilsis": ["lilsis", "It's a RAINBOW of books. The one about the duck is in the yellow. The duck has NO words."],
  "home.desk.mom": ["mom", "Her novel, squared up, and the whole plot on cards above it. I've been asked not to read either. In writing."],   // PASS-17H: Mom's formality
  "home.desk.bigsis": ["bigsis", "My desk. Chapter nine, the plot on cards, and my pencils: the slim kind, all exactly the same length."],
  "home.desk.lilsis": ["lilsis", "Her desk. I touched ONE pencil ONE time and she KNEW."],
  "home.desk.pencil.mom": ["mom", "That's your father's. It doesn't go in with your sister's. Hers are a matched set."],   // PASS-17H: Mom's formality; one darling fewer
  "home.desk.pencil.bigsis": ["bigsis", "That is Dad's pencil. It does not go in my jar. My jar has standards."],
  "home.desk.pencil.lilsis": ["lilsis", "I put Daddy's pencil in her jar and took it out again. Now she has to count them ALL."],
  "home.bedbig.mom": ["mom", "Hospital corners. I didn't teach her that. I'm not sure anybody did."],   // PASS-17H: Mom's formality
  "home.bedbig.bigsis": ["bigsis", "My bed. Made. One book on the pillow, a ribbon at my place, and a second book under it, in case the first one ends."],
  "home.bedbig.lilsis": ["lilsis", "Her bed has a TENT on it. A see-through one. I'm not allowed in it. I've only been in it nine times."],
  "home.mat.mom": ["mom", "The exercise mat. She stretches at dawn, in perfect silence. I only know because the floorboards tell me."],   // PASS-17H: Mom's formality
  "home.mat.bigsis": ["bigsis", "My mat. Ten minutes every morning. In for four, out for four. Tonight I keep losing count at three."],
  "home.mat.lilsis": ["lilsis", "I can do a somersault on it! I'm not allowed. I did three. In my head. ...And one not in my head."],
  "home.hatch.mom": ["mom", "The way down. Mind the ladder, girls. It's steeper going down than it was coming up. Everything is."],   // PASS-17H: Mom's formality
  "home.hatch.bigsis": ["bigsis", "The hatch. Shoes go back on at the bottom. Outdoor voices may be resumed on the landing."],
  "home.hatch.lilsis": ["lilsis", "The ladder hole! I go down it backwards. Like a bear. Bears go down backwards."],

  // ---- what they say to each other in the Retreat
  "home.talk.retreat.mom.bigsis.key.a": ["mom", "D major, darling?"],
  "home.talk.retreat.mom.bigsis.key.b": ["bigsis", "D major. You always know. It is extremely annoying, Mother."],
  "home.talk.retreat.mom.bigsis.1a": ["mom", "You put the Constitution on your timeline. In ink."],   // PASS-17H: Mom's formality
  "home.talk.retreat.mom.bigsis.1b": ["bigsis", "You stood behind me until I did, Mother."],
  "home.talk.retreat.mom.bigsis.2a": ["mom", "It's a lovely room, darling. You made every inch of it yourself."],   // PASS-17H: Mom's formality
  "home.talk.retreat.mom.bigsis.2b": ["bigsis", "On pocket money. I should like that in the program."],
  "home.talk.retreat.mom.lilsis.1a": ["mom", "Indoor voice, sweetheart."],
  "home.talk.retreat.mom.lilsis.1b": ["lilsis", "THIS IS MY INDOOR VOICE. IT'S FOR INDOORS IN A BARN."],
  "home.talk.retreat.mom.lilsis.2a": ["lilsis", "Mommy, can the General come up here when she's home? She's not a chicken. She's a GENERAL."],
  "home.talk.retreat.mom.lilsis.2b": ["mom", "That's for the court of appeal, darling. I only supplied the spelling."],   // PASS-17H: Mom's formality
  "home.talk.retreat.bigsis.mom.1a": ["bigsis", "Mother. It is perfectly calm up here, and I am not. I find that inconsiderate of the room."],
  "home.talk.retreat.bigsis.mom.1b": ["mom", "The set is never nervous, darling. Only the cast. That's what a set is for."],   // PASS-17H: Mom's formality
  "home.talk.retreat.bigsis.mom.2a": ["bigsis", "I counted the lights again. In fours. It came out even."],
  "home.talk.retreat.bigsis.mom.2b": ["mom", "And did it help?"],
  "home.talk.retreat.bigsis.mom.2c": ["bigsis", "No. But it came out even."],
  "home.talk.retreat.bigsis.lilsis.1a": ["bigsis", "Visiting hours end when the big hand reaches the twelve."],
  "home.talk.retreat.bigsis.lilsis.1b": ["lilsis", "WHICH twelve? There's one every hour! I'll have the LAST one."],
  "home.talk.retreat.bigsis.lilsis.2a": ["bigsis", "You may stay if you can be silent for one whole minute."],
  "home.talk.retreat.bigsis.lilsis.2b": ["lilsis", "Okay. ...Is it a minute? ...Now? ...I was silent in BETWEEN."],
  "home.talk.retreat.lilsis.mom.1a": ["lilsis", "Mommy, why can't chickens come up here?"],
  "home.talk.retreat.lilsis.mom.1b": ["mom", "Because it's your sister's room, and she asks so little. Three rules. You have eleven."],   // PASS-17H: Mom's formality; one darling fewer
  "home.talk.retreat.lilsis.mom.2a": ["lilsis", "It smells like a flower shop up here. And a little bit like a library."],
  "home.talk.retreat.lilsis.mom.2b": ["mom", "That's your sister, darling. Precisely."],   // PASS-17H: Mom's formality
  "home.talk.retreat.lilsis.bigsis.1a": ["lilsis", "Can I come up when it isn't visiting hours? Just my toe?"],
  "home.talk.retreat.lilsis.bigsis.1b": ["bigsis", "...One toe. For morale."],
  "home.talk.retreat.lilsis.bigsis.2a": ["lilsis", "Are you scared?"],
  "home.talk.retreat.lilsis.bigsis.2b": ["bigsis", "No. ...A little. Do not tell the room."],
  "home.talk.retreat.lilsis.bigsis.2c": ["lilsis", "I'll hold your hand, then. Not because I'M scared. For the ROOM."],

  // =====================================================================================================
  // IN ANY ROOM
  // =====================================================================================================
  // ---- what the one who is handed something says
  "home.give.studykey.mom": ["mom", "Thank you, darling. I'll do the honors."],   // PASS-17H: Mom's formality ('shall')
  "home.give.studykey.bigsis": ["bigsis", "The key to Trip Headquarters. I accept the responsibility. And the tag."],
  "home.give.studykey.lilsis": ["lilsis", "The KEY! I'm the key person! I'm in CHARGE of the door!"],
  "home.give.lilflash.mom": ["mom", "Your flashlight, sweetheart? I'll keep it safe. You'll want it back for the closet."],   // PASS-17H: Mom's formality
  "home.give.lilflash.bigsis": ["bigsis", "Her flashlight. It is pink and slightly sticky. I am holding it under protest."],
  "home.give.lilflash.lilsis": ["lilsis", "MY flashlight! Hi, flashlight. I'm hugging it. Nobody else hold it. It likes ME best."],
  "home.give.batteries.mom": ["mom", "Your sister's batteries. I'll hold them the way you hold a borrowed prop: carefully, and not for long."],   // PASS-17H: Mom's formality ('shall')
  "home.give.batteries.bigsis": ["bigsis", "My batteries, back in my own hand. They are not going back in the machine. A sacrifice stays made."],
  "home.give.batteries.lilsis": ["lilsis", "The batteries! But I don't have my flashlight. Somebody's got it who isn't me. They need to MEET."],
  // ---- batteries and flashlight in one pair of hands: whoever that is puts them in
  "home.flash.load.mom": ["mom", "In they go, the right way round. ...And it lights. A small pink spotlight. She'll want it back at once."],   // PASS-17H: Mom's formality
  "home.flash.load.bigsis": ["bigsis", "Batteries in. The flat ends go against the springs. ...There. It lights. The Retreat did not go dark for nothing."],
  "home.flash.load.lilsis": ["lilsis", "Batteries IN. Click. ...CLICK! It WORKS! It's pink and it's back! Now the closet can't be dark at me."],
  // ---- her flashlight, shined at something while there is nothing in it
  "home.flash.dead": ["lilsis", "Click. Nothing. It's all used up. I can't shine it at ANYTHING till it gets batteries."],
  "home.give.pencil.mom": ["mom", "Your father's pencil. Yellow, wooden, and thoroughly chewed. That'll do very nicely."],   // PASS-17H: Mom's formality
  "home.give.pencil.bigsis": ["bigsis", "Dad's pencil. I know what it fits. I do not know how to do it."],
  "home.give.pencil.lilsis": ["lilsis", "Daddy's pencil! I'll just HOLD it. I won't fix anything. Probably."],
  "home.give.carkey.mom": ["mom", "Thank you. I am, after all, the only one of us with a license."],
  "home.give.carkey.bigsis": ["bigsis", "The car key. I am thirteen. I am holding it. I am not driving. Yet."],
  "home.give.carkey.lilsis": ["lilsis", "The car key! I call the front seat. I CALLED it. It's called."],

  // ---- carried things
  "item.note.mom": ["mom", "'The year of the best thing since.' Your sister will know. She knows the year of everything."],
  "item.note.bigsis": ["bigsis", "Sliced bread, 1928. I am keeping this. It is a primary source."],
  "item.note.lilsis": ["lilsis", "Words. I'll give it to somebody who reads books with NO pictures."],
  "item.studykey.mom": ["mom", "The study key, on a string, with a tag: 'TRIP HQ.' It smells faintly of piano."],
  "item.studykey.bigsis": ["bigsis", "One brass key, formerly of the piano. Technically it was the eighty-ninth."],
  "item.studykey.lilsis": ["lilsis", "Daddy's key! I got it out of the piano. Me. With my arm."],
  "item.lilflash.mom": ["mom", "Her flashlight. Pink, chunky, and very much loved. It's hers to carry into the dark."],   // PASS-17H: Mom's formality
  "item.lilflash.bigsis": ["bigsis", "My sister's flashlight. The button is sticky. I am not going to ask."],
  "item.lilflash.lilsis": ["lilsis", "My flashlight! It's pink and it's got a big squishy button. It only works when its batteries work."],
  "item.batteries.mom": ["mom", "Your sister's batteries. Four of them. They want a pink flashlight, and after that they want to go home."],
  "item.batteries.bigsis": ["bigsis", "Four double-A batteries, lately the whole sound of the Retreat. They go in my sister's flashlight. I am fine."],
  "item.batteries.lilsis": ["lilsis", "Batteries! They go in my flashlight. Then it works. Then I do the closet. That's the WHOLE plan."],
  "item.pencil.mom": ["mom", "Your father's crossword pencil. I've wound a great many tapes with pencils like this."],   // PASS-17H: Mom's formality
  "item.pencil.bigsis": ["bigsis", "Dad's pencil. Fun fact: you can wind a cassette with one. Knowing it and doing it are different."],
  "item.pencil.lilsis": ["lilsis", "Daddy's pencil. It's all bitey at the end. That's where the thinking goes in."],
  "item.carkey.mom": ["mom", "My spare car key. It's spent two years in a cash box with the ketchup. It's earned a drive."],   // PASS-17H: Mom's formality
  "item.carkey.bigsis": ["bigsis", "The spare key to Mom's car. Liberated by the Constitution. I will be telling this story for years."],
  "item.carkey.lilsis": ["lilsis", "The key for Mommy's car! It makes the car go BEEP. Mommy does the driving. I do the BEEP."],

  // =====================================================================================================
  // HINTS: one from each of them for every puzzle. The one whose job it is says what to try; the others say whose job it is.
  // =====================================================================================================
  "hint.home.riddle.mom": ["mom", "Your father has locked his study and taped a notice to the door. I should read it properly."],
  "hint.home.riddle.bigsis": ["bigsis", "The study is locked, and Dad has left a notice on its door. It reads like a riddle. I like riddles."],
  "hint.home.riddle.lilsis": ["lilsis", "Daddy's door upstairs has a sign with SO many words. My sister likes words. Mommy likes words. I like DOORS."],
  "hint.home.key.lilsis": ["lilsis", "The key's INSIDE the piano, way down. There's a little wall by the pedals. I fit under there. I fit under EVERYTHING."],
  "hint.home.key.mom": ["mom", "The key is down inside my piano, and my arms won't reach. It wants someone small, underneath."],   // PASS-17H: Mom's formality
  "hint.home.key.bigsis": ["bigsis", "The key is on the hammers. I am not putting my arm in a piano. My sister fits under the keyboard."],
  "hint.home.study.mom": ["mom", "We have the key to his study. Whoever is holding it should try that door upstairs."],
  "hint.home.study.bigsis": ["bigsis", "One of us is holding the study key. The study door is upstairs, at the end of the landing."],
  "hint.home.study.lilsis": ["lilsis", "We got the KEY! Whoever's holding it has to put it in Daddy's door upstairs. Chop chop!"],
  "hint.home.batteries.lilsis": ["lilsis", "The closet's too dark! I need my flashlight from my fort. If it's dead, my sister's music box has batteries. Just SAYING."],
  "hint.home.batteries.bigsis": ["bigsis", "Her flashlight is no use dead. The only batteries that size live in my sound machine. After that, the two must meet."],
  "hint.home.batteries.mom": ["mom", "No light, no closet. If her flashlight is dead, the batteries are your sister's to give. Then the two must be put together."],
  "hint.home.router.lilsis": ["lilsis", "My flashlight WORKS! The internet's in the closet under the stairs. I fit. I'm going IN."],
  "hint.home.router.mom": ["mom", "The router is in the closet under the stairs, and she has a flashlight that works. That's her cue."],   // PASS-17H: Mom's formality
  "hint.home.router.bigsis": ["bigsis", "The flashlight works. I paid for that. Now the router: it is in the closet only my sister fits into."],
  "hint.home.note.bigsis": ["bigsis", "Dad always writes his passwords down. There is a yellow note on the monitor. I should read it."],
  "hint.home.note.mom": ["mom", "Your father left a note on the monitor. It's a riddle about a year, and your sister is the one for years."],   // PASS-17H: Mom's formality
  "hint.home.note.lilsis": ["lilsis", "There's a yellow sticky on the computer with words on it. Words are for my sister."],
  "hint.home.login.mom": ["mom", "We have the internet and we have the password. I'll sit down at that computer myself."],   // PASS-17H: Mom's formality
  "hint.home.login.bigsis": ["bigsis", "The router is on and the password is 1928. After that it asks about the wedding. That is Mom's department."],
  "hint.home.login.lilsis": ["lilsis", "I fixed the internet and my sister did the number. Now Mommy has to do the typing."],
  "hint.home.tape.mom": ["mom", "The machine has spilled its tape. I can wind it in with a pencil: your father's, from his crossword."],
  "hint.home.tape.bigsis": ["bigsis", "The tape wants winding back in with a pencil. Dad's is on his crossword. Mom has the knack."],
  "hint.home.tape.lilsis": ["lilsis", "The tape machine's tape fell out. NOT my fault this time. Mommy needs Daddy's pencil, from his puzzle downstairs."],
  "hint.home.message.mom": ["mom", "The tape is wound, and there's one new message on your father's machine. Somebody press play."],   // PASS-17H: Mom's formality
  "hint.home.message.bigsis": ["bigsis", "The tape is back in. There is one new message on Dad's machine. We should play it."],
  "hint.home.message.lilsis": ["lilsis", "The tape's fixed and I didn't even do it! Press PLAY on the blinky machine! The big button!"],
  "hint.home.vault.mom": ["mom", "The vault wants the year 'We the People' got it in writing. That's framed on our living-room wall."],   // PASS-17H: Mom's formality
  "hint.home.vault.bigsis": ["bigsis", "The spare car key is in Dad's 'family vault'. The combination is a year. Mom's kind of year."],
  "hint.home.vault.lilsis": ["lilsis", "Daddy's vault box has a clicky wheel, and Mommy knows the number. It's the 'We the People' year!"],
  "hint.home.leave.mom": ["mom", "We know where that phone was last seen. The front door, girls."],
  "hint.home.leave.bigsis": ["bigsis", "We have a location. The logical next step is the front door."],
  "hint.home.leave.lilsis": ["lilsis", "We found the dot! Let's GO! The door is right THERE!"],
};
