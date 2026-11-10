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
  "home.arrive.1": ["mom", "Voicemail. That's the ninth time. I had quite decided to stop worrying at eight."],
  "home.arrive.2": ["lilsis", "Daddy's not lost. Daddy's EARLY."],
  "home.arrive.2b": ["bigsis", "That is not what early means."],
  "home.arrive.3": ["bigsis", "Noon departure, a four-hour drive, and it is now nine forty. That is not a shortcut. That is an expedition."],   // PASS-19H1: shorter; punch last (her figures are the joke)
  "home.arrive.4": ["mom", "Dinner was at six. I set five places, and two of them can stay exactly where they are."],
  "home.arrive.pray.1": ["mom", "First things first, girls. Come here, both of you."],
  "home.arrive.pray.2": ["mom", "Father, You know where they are tonight, and I do not. Keep them."],
  "home.arrive.pray.3": ["mom", "And bring us to them, wherever that turns out to be. In Jesus' name."],
  "home.arrive.pray.4": ["lilsis", "And please make Daddy ask for directions. Just ONE time. Amen."],
  "home.arrive.pray.5": ["mom", "Amen."],
  "home.arrive.5": ["bigsis", "Dad's phone reports its whereabouts to the family computer. Which is in his study, naturally."],   // PASS-19H1: shorter
  "home.arrive.6": ["lilsis", "Then the computer KNOWS where Daddy is. Somebody go ask it!"],   // PASS-19H1: emphasis (one exclamation)
  "home.arrive.6b": ["bigsis", "It cannot. The internet has been down ever since Dad 'improved' the wiring. His word, not mine."],   // PASS-19H1: shorter; punch last
  "home.pc.router": ["mom", "The router's in the closet under the stairs. Your father files the internet beside the vacuum."],
  "home.arrive.7": ["mom", "Places, girls. That phone was last seen somewhere, and we're going to find out where."],   // PASS-19H1: spoken; shorter

  // =====================================================================================================
  // THE LIVING ROOM
  // =====================================================================================================
  "home.upstairs.mom": ["mom", "Your father's study is the locked one. He claims the lock keeps the surprises in."],   // PASS-19H1: shorter
  "home.upstairs.bigsis": ["bigsis", "Four rooms upstairs, and exactly one of the four is tidy. I leave you to guess whose."],   // PASS-19H1: shorter; punch last; one idea
  "home.upstairs.lilsis": ["lilsis", "My fort's up there. The sign says 'NO BIG SISTERS.' That means her, and that means forever."],   // PASS-19H1: shorter; emphasis; one idea

  "home.window.mom": ["mom", "No headlights yet. I've looked out eleven times, darling. ...Twelve."],
  "home.window.bigsis": ["bigsis", "'The street,' she wrote, 'was the wrong kind of quiet.' I am keeping that."],   // PASS-19H1: her whole words; shorter
  "home.window.lilsis": ["lilsis", "I'm on car watch. I haven't blinked since dinner. My eyeballs are getting crunchy."],   // PASS-19H1: shorter; punch last
  "home.photo.mom": ["mom", "He took a shortcut to the lake. We saw a great deal of lake."],   // PASS-19H1: shorter; one idea
  "home.photo.bigsis": ["bigsis", "Dad set the timer and ran. He is the blur."],   // PASS-19H1: shorter; one idea
  "home.photo.lilsis": ["lilsis", "I was six at the lake. Now I'm a WHOLE number bigger."],   // PASS-19H1: emphasis; shorter; one idea
  "home.stairs.mom": ["mom", "Nobody's going up to bed tonight, girls. Least of all your mother."],   // PASS-19H1: spoken
  "home.stairs.bigsis": ["bigsis", "Sixteen steps. I counted them in fours, for calm. It did not help."],   // PASS-19H1: shorter; her whole words; one idea
  "home.stairs.lilsis": ["lilsis", "I'm not tired. I'm NEVER tired. ...What time is it?"],

  // ---- chain B: the closet under the stairs
  "home.closet.look.mom": ["mom", "The closet under the stairs. The door gives exactly this far, and not a whisker more."],
  "home.closet.look.bigsis": ["bigsis", "The door sticks at four inches. I am wider than four inches. I have shoulders."],
  "home.closet.look.lilsis": ["lilsis", "That tiny light in there is the internet. The internet is TINY."],
  "home.closet.use.mom": ["mom", "A lady does not squeeze into closets, darling. A lady has a seven-year-old."],
  "home.closet.use.bigsis": ["bigsis", "I refuse. There are spiders in there, and I am thirteen. Both are final."],
  "home.closet.go.1": ["lilsis", "I FIT!"],
  "home.closet.dark.1": ["lilsis", "It's so dark. I can't find the plug. I found the vacuum. With my NOSE."],
  "home.closet.dark.2": ["lilsis", "I need my pink flashlight. It's in my fort, and I know the way there. It's MY fort."],
  "home.closet.dark.3": ["mom", "Then up you go for it, sweetheart. That fort admits exactly one person, and it's you."],
  "home.closet.needflash": ["lilsis", "I'm not scared. I'm BRAVE-scared. Brave-scared people bring a flashlight."],
  "home.closet.lent": ["lilsis", "My flashlight, please. I'm the closet person. It's my whole job."],
  "home.closet.dead": ["lilsis", "A dead flashlight is just a pink stick. It needs batteries."],
  "home.closet.go.2": ["lilsis", "Hi, vacuum. Hi, spiders. There's a plug that isn't plugged into ANYTHING."],
  "home.closet.go.3": ["mom", "Into the wall, darling. The socket with the surprised face."],
  "home.closet.go.4": ["lilsis", "The red light went green. I fixed the internet. I'm a ENGINEER!"],
  "home.closet.go.5": ["bigsis", "AN engineer."],
  "home.closet.go.6": ["lilsis", "That's what I SAID."],
  "home.closet.again": ["lilsis", "I already fixed it. The light's green. Green means I'm good at it."],
  "home.closet.done.mom": ["mom", "One small green light. I've never been so glad to see one. Clever girl."],
  "home.closet.done.bigsis": ["bigsis", "The light is green. She will be insufferable for a week."],
  "home.closet.key.mom": ["mom", "It doesn't lock, darling. Nothing in there has ever wanted to get out."],   // PASS-17H: Mom's formality; one darling fewer
  "home.closet.key.bigsis": ["bigsis", "It does not lock. It only sticks. Dad maintains that this is a feature."],
  "home.closet.key.lilsis": ["lilsis", "No keyhole. It's just a door that's bad at being a door."],

  // ---- Mom's bookcase, the kitchen, the Preamble, the clock
  "home.shelf.mom": ["mom", "The Adams letters, Washington, Franklin, more plays than one shelf ought to hold, and the hymnal."],
  "home.shelf.mom2": ["mom", "In March 1776 Abigail Adams wrote to John, 'Remember the Ladies.' I do like her."],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.shelf.bigsis": ["bigsis", "Mom reads the Founders the way people read thrillers. She gasps."],
  "home.shelf.lilsis": ["lilsis", "No pictures. I checked ALL of them. One has a man in a wig."],
  "home.kitchen.mom": ["mom", "I always leave the kitchen light on for whoever's last home. Tonight it's on for two."],   // PASS-19H1: shorter
  "home.kitchen.bigsis": ["bigsis", "Four pots of tea since six o'clock. Even the kettle has started to look worried."],   // PASS-19H1: shorter; punch last; one idea
  "home.kitchen.lilsis": ["lilsis", "My hen guards the snacks. It's always a little bit snack time."],   // PASS-19H1: shorter; emphasis
  "home.frame.mom": ["mom", "'We the People.' Philadelphia, 17 September 1787. It still gives me goosebumps."],   // PASS-19H1: shorter (the fact's figures stay)
  "home.frame.bigsis": ["bigsis", "Mom recites the Preamble every Fourth of July. With gestures."],   // PASS-19H1: shorter; punch last; one idea
  "home.frame.lilsis": ["lilsis", "The letters start giant and curly. Then they get tired."],   // PASS-19H1: emphasis; punch last
  "home.clock.mom": ["mom", "Five hours and forty minutes late. I've stopped rounding."],   // PASS-19H1: shorter; one idea
  "home.clock.bigsis": ["bigsis", "That clock ticks flat, Mom says. I cannot hear it, and I have tried."],   // PASS-19H1: one idea
  "home.clock.lilsis": ["lilsis", "Three fingers past my bedtime. Nobody say anything."],   // PASS-19H1: shorter; emphasis

  // ---- chain A: the piano, and the key that is in it
  "home.piano.look.mom": ["mom", "Your sister plays my piano better than I do now. That was always the plan."],   // PASS-19H1: shorter; punch last; one idea
  "home.piano.look.bigsis": ["bigsis", "Bartolomeo Cristofori built the first one, in Florence, around 1700."],   // PASS-19H1: shorter; 'Fun fact' rationed (the fact's figures stay)
  "home.piano.look.bigsis2": ["bigsis", "They called it a harpsichord with soft and loud. I would say miracle."],   // PASS-19H1: shorter
  "home.piano.look.lilsis": ["lilsis", "I made up one whole song on the piano. It's short and LOUD."],   // PASS-19H1: emphasis; shorter; one idea
  "home.piano.key.mom": ["mom", "There's a key in my piano. Saying so out loud hasn't brought it an inch closer."],   // PASS-19H1: shorter
  "home.piano.key.bigsis": ["bigsis", "It is under the A above middle C. I can hear it from here, and I wish I could not."],   // PASS-19H1: shorter; one idea
  "home.piano.key.lilsis": ["lilsis", "A key in the piano? I fit under everything. Everybody stand BACK."],   // PASS-19H1: emphasis; shorter
  "home.piano.use.mom": ["mom", "'A Mighty Fortress Is Our God.' Luther's. One verse, quietly, for courage."],   // PASS-17H: shorter; the hymn's author without the label
  "home.piano.use.mom2": ["mom", "'God is our refuge and strength, a very present help in trouble.' Very present."],   // PASS-19H1: shorter; faith natural (the quotation stays)
  "home.piano.use.mom3": ["mom", "Once more, then. It's a hymn that doesn't mind being needed."],   // PASS-17H: Mom's formality
  "home.piano.use.bigsis": ["bigsis", "Something in a minor key. Under the circumstances, it felt appropriate."],
  "home.piano.use.bigsis2": ["bigsis", "When Dad is home I will play the loud one he likes. Twice."],
  "home.piano.use.lilsis": ["lilsis", "PLONK. That was my song. It's called 'Plonk'."],
  "home.thunk.bigsis.1": ["bigsis", "The A above middle C went 'thunk'. This piano does not go 'thunk'."],   // PASS-19H1: shorter; one idea
  "home.thunk.bigsis.2": ["bigsis", "Something is lying on the hammers. Something small, and metal."],
  "home.thunk.mom.react": ["mom", "In MY piano. Somebody put it there, and I know which somebody."],   // PASS-19H1: shorter; punch last
  "home.thunk.mom.1": ["mom", "One dead note, the A above middle C. Not the piano, and certainly not me."],   // PASS-19H1: one idea
  "home.thunk.mom.2": ["mom", "Somebody has dropped something into MY piano. Somebody who is going to hear about it."],   // PASS-19H1: shorter; one idea
  "home.thunk.bigsis.react": ["bigsis", "Small and metal, by the sound. I can tell you which hammer."],   // PASS-19H1: shorter; one idea
  "home.key.mom.1": ["mom", "With the lid up I can see it: a door key, resting on the hammers as if it lived there."],   // PASS-19H1: one idea
  "home.key.mom.2": ["mom", "And I cannot reach it. My arms are a civilized length."],
  "home.key.mom.2.b": ["lilsis", "My arms aren't civilized at ALL."],   // PASS-19H1: new; a turn: three boxes by one speaker broken
  "home.key.mom.3": ["mom", "The panel down by the pedals lifts off. That's your cue, sweetheart."],   // PASS-19H1: shorter
  "home.key.bigsis.1": ["bigsis", "It is under the A above middle C. I can hear exactly where."],   // PASS-19H1: shorter; one idea
  "home.key.bigsis.2": ["bigsis", "I am not putting my arm in a piano. I am halfway through a sonata."],   // PASS-19H1: shorter; punch last
  "home.key.get.1": ["lilsis", "There's a little wall down here. It comes OFF."],   // PASS-19H1: emphasis; shorter
  "home.key.get.2": ["lilsis", "It's all dusty in here. There's a marble. And a penny. And a KEY!"],
  "home.key.get.3": ["mom", "The study key, tagged 'TRIP HQ.' He hid it, and then he labeled it. That's your father."],   // PASS-19H1: shorter; punch last; one idea
  "home.key.get.4": ["bigsis", "And not one string knocked out of tune. That is pure luck, and I will take it."],   // PASS-19H1: shorter (one 'For the record' an act scene)
  "home.key.get.5": ["lilsis", "I'm keeping the marble."],
  "home.piano.keyback.mom": ["mom", "It has spent quite long enough in my piano, thank you."],
  "home.piano.keyback.bigsis": ["bigsis", "Putting it back: historically accurate, and of no use whatever."],   // PASS-19H1: shorter
  "home.piano.keyback.lilsis": ["lilsis", "It came OUT of there. I'm not putting it back."],   // PASS-19H1: shorter; emphasis

  // ---- the gate: the front door, and the sampler over it
  "home.door.look.mom": ["mom", "The doorbell sings a quarter-tone flat, like your father. I'm fond of both."],   // PASS-19H1: shorter (its words stay); one idea
  "home.door.look.bigsis": ["bigsis", "Two coats are missing from the hooks. I notice hooks."],   // PASS-19H1: shorter; one idea
  "home.door.look.lilsis": ["lilsis", "I'm watching the door and the window. I have two eyes."],   // PASS-19H1: emphasis
  "home.door.early.mom": ["mom", "Not until we know where we're going. One of us in this family must."],   // PASS-19H1: spoken
  "home.door.early.bigsis": ["bigsis", "We do not have a destination. A journey without one is just Dad."],   // PASS-19H1: her whole words; shorter
  "home.door.early.lilsis": ["lilsis", "I've been ready since dinner. ...Which way IS Daddy?"],   // PASS-19H1: shorter; emphasis
  "home.door.message.mom": ["mom", "Not yet. There's a message on your father's machine, and I want to hear it before we go anywhere."],   // PASS-19H1: shorter
  "home.door.message.bigsis": ["bigsis", "There is one new message on Dad's machine. We are not leaving the house with it blinking."],   // PASS-19H1: shorter; concrete
  "home.door.message.lilsis": ["lilsis", "The blinky machine has a message. It's probably DADDY."],   // PASS-19H1: emphasis
  "home.door.nokey.mom": ["mom", "We know where, and we've heard him. What we haven't got is a car key."],   // PASS-19H1: shorter
  "home.door.nokey.bigsis": ["bigsis", "Destination: yes. Message: yes. Car key: no. Two of three does not start a car."],   // PASS-19H1: shorter
  "home.door.nokey.lilsis": ["lilsis", "We don't have a key. ...I could push the car. I'm mighty."],   // PASS-19H1: emphasis; shorter
  "home.door.keys.1": ["mom", "And my car keys left this morning, in your father's pocket."],   // PASS-19H1: shorter; one idea
  "home.door.keys.2": ["bigsis", "There is a spare in the 'family vault', in his study. He was extremely proud of the name."],   // PASS-19H1: shorter
  "home.door.keys.3": ["lilsis", "It's a box with a clicky wheel. Mommy knows ALL the clicks."],   // PASS-19H1: shorter; emphasis
  "home.door.psalm.1": ["mom", "One moment, girls. Nobody in this family leaves the house without the psalm."],   // PASS-19H1: shorter
  "home.door.psalm.2": ["bigsis", "Psalm 121, verse 8. She always does this part."],   // PASS-17H: the reference is Big Sister's to say; a beat for her sister
  "home.door.psalm.3": ["lilsis", "'The LORD shall preserve thy going out and thy coming in from this time forth, and even for evermore.'"],
  "home.door.psalm.4": ["mom", "Amen. Going out, and coming in. All five of us."],
  "home.leave.1": ["mom", "Coats, girls. We are going to Nevada."],
  "home.leave.2": ["bigsis", "The atlas, a book, and a second book in case the first one ends."],   // PASS-19H1: her whole words; shorter; three, the best last
  "home.leave.3": ["lilsis", "I'll bring my boots. I'm already WEARING my boots!"],   // PASS-19H1: emphasis (one exclamation)
  "home.leave.4": ["mom", "We are going to be perfectly polite, and completely impossible to get rid of."],
  "home.door.studykey.mom": ["mom", "That's the study key. This door wants a car at the other end."],   // PASS-19H1: shorter
  "home.door.studykey.bigsis": ["bigsis", "This one opens Dad's study. That door opens everything else."],   // PASS-19H1: shorter; one idea
  "home.door.studykey.lilsis": ["lilsis", "It doesn't fit. Daddy's key is for Daddy's door."],   // PASS-19H1: emphasis
  "home.sampler.mom": ["mom", "'...as for me and my house, we will serve the LORD.' Hung before the curtains."],   // PASS-19H1: shorter (the quotation stays)
  "home.sampler.bigsis": ["bigsis", "I measured every letter. I was nine, and it was raining."],   // PASS-19H1: shorter; one idea
  "home.sampler.lilsis": ["lilsis", "Mommy let me do one stitch. The wobbly one."],   // PASS-19H1: shorter; emphasis; one idea
  "home.coats.mom": ["mom", "He wore his other hat. I have opinions about the other hat."],   // PASS-19H1: spoken; shorter
  "home.coats.bigsis": ["bigsis", "Mine is hung up by its loop. I wish to be clear about that."],   // PASS-19H1: shorter; one idea
  "home.coats.lilsis": ["lilsis", "Daddy's big coat went on the trip with Daddy in it."],   // PASS-19H1: emphasis; shorter

  // ---- Dad's armchair, his crossword and his pencil; the dinner table and the Bible
  "home.chair.mom": ["mom", "It has kept his shape. I rather like that tonight."],   // PASS-19H1: spoken; shorter
  "home.chair.bigsis": ["bigsis", "Seven across is wrong. I have not told him."],   // PASS-19H1: her whole words; shorter
  "home.chair.lilsis": ["lilsis", "Daddy's chair. If you sit in it you have to say 'well, well, well'."],
  "home.crossword.mom": ["mom", "His crossword, half done. It can wait up for him tonight, like the rest of us."],   // PASS-19H1: shorter
  "home.crossword.bigsis": ["bigsis", "Seven across is wrong, in pencil. He uses ink when he is sure. He knew."],   // PASS-19H1: shorter; punch last
  "home.crossword.lilsis": ["lilsis", "I do the three-letter ones. Always HEN. It's right more than you'd think."],   // PASS-19H1: shorter
  "home.pencil.look.mom": ["mom", "The one pencil in this house that's always exactly where it should be. Your father's."],   // PASS-19H1: shorter
  "home.pencil.look.bigsis": ["bigsis", "A great many tooth marks. He thinks with his teeth."],   // PASS-19H1: shorter
  "home.pencil.look.lilsis": ["lilsis", "He bites it when he thinks. It's a VERY thought-about pencil."],   // PASS-19H1: emphasis
  "home.pencil.take.mom": ["mom", "I'm borrowing this, my love. Come home and ask for it."],   // PASS-19H1: shorter; punch last
  "home.pencil.take.bigsis": ["bigsis", "I will return it sharpened. He will never notice."],   // PASS-19H1: shorter; one idea
  "home.pencil.take.lilsis": ["lilsis", "I've got Daddy's pencil. The teeth marks aren't mine. Mostly."],   // PASS-19H1: shorter; emphasis
  "home.table.mom": ["mom", "Pot roast at six o'clock sharp. It is no longer sharp."],
  "home.table.bigsis": ["bigsis", "'The table,' she observed, 'was set for five. The house was not.'"],
  "home.table.lilsis": ["lilsis", "Can I have Daddy's potatoes? He's not using them."],
  "home.bible.mom": ["mom", "'My help cometh from the LORD, which made heaven and earth.' He read us that this morning."],   // PASS-19H1: shorter (the quotation stays); FINAL-19: the lead's line
  "home.bible.bigsis": ["bigsis", "Psalm 121, where Dad left it. 'I will lift up mine eyes unto the hills, from whence cometh my help.'"],   // PASS-19H1: shorter (the quotation stays); FINAL-19: the lead's line
  "home.bible.lilsis": ["lilsis", "'The LORD is my shepherd; I shall not want.' ...I do want Daddy, though."],   // PASS-19H1: shorter; faith natural (the quotation stays)

  // ---- what they say to each other in the living room
  "home.talk.mom.bigsis.key.a": ["mom", "You can hear exactly which note it's under, darling. Couldn't you just reach in and fish it out?"],   // PASS-17H: Mom's formality; one darling fewer
  "home.talk.mom.bigsis.key.b": ["bigsis", "It is a piano, Mother, not a mailbox. You want the member of this family who fits under things."],   // PASS-19H1: shorter
  "home.talk.batt.mom.bigsis.a": ["mom", "Darling, your sister's flashlight wants batteries, and I suspect you know exactly where some are."],
  "home.talk.batt.mom.bigsis.b": ["bigsis", "I know where every battery in this house is. That is precisely what hurts."],
  "home.talk.batt.lilsis.bigsis.a": ["lilsis", "Your music box has batteries in it. I've SEEN them, so don't pretend."],
  "home.talk.batt.lilsis.bigsis.b": ["bigsis", "It is a sound machine, not a music box. And yes. I had hoped nobody would mention it."],
  "home.talk.batt.mom.lilsis.a": ["mom", "Batteries in one place, a flashlight in another. I think they ought to be introduced, don't you?"],
  "home.talk.batt.mom.lilsis.b": ["lilsis", "Give them to ME. I've got two hands and a pocket. That's three places to put things."],
  "home.talk.mom.bigsis.1a": ["mom", "You've gone very quiet, darling. With you, that generally means the wheels are turning."],
  "home.talk.mom.bigsis.1b": ["bigsis", "I am thinking. From the outside it only looks like quiet. From the inside it is very loud."],
  "home.talk.mom.bigsis.2a": ["mom", "Whatever's happened to them, we'll handle it the way we handle everything else in this house."],   // PASS-19H1: shorter
  "home.talk.mom.bigsis.2b": ["bigsis", "With a list?"],
  "home.talk.mom.bigsis.2c": ["mom", "With a list."],
  "home.talk.mom.lilsis.dark.a": ["mom", "Your flashlight's up in your fort, sweetheart. Will you run and get it? Mind the stairs."],   // PASS-19H1: shorter
  "home.talk.mom.lilsis.dark.b": ["lilsis", "I'm ALREADY going. There's nothing in my fort. ...Except a lot of things. Nobody look."],   // PASS-19H1: shorter; emphasis; punch last
  "home.talk.mom.lilsis.1a": ["mom", "Are you frightened, sweetheart? You can tell me if you are."],
  "home.talk.mom.lilsis.1b": ["lilsis", "No! ...Are YOU?"],
  "home.talk.mom.lilsis.1c": ["mom", "Not while I have you to look after me."],
  "home.talk.mom.lilsis.2a": ["lilsis", "Mommy, why did Daddy take a shortcut? Didn't he know the regular way?"],
  "home.talk.mom.lilsis.2b": ["mom", "He knew it perfectly well, darling. The long way around has just never once been his idea."],
  "home.talk.bigsis.mom.1a": ["bigsis", "Mom. Statistically speaking, they are fine. I have run the numbers several times."],
  "home.talk.bigsis.mom.1b": ["mom", "Thank you, darling. And unstatistically?"],
  "home.talk.bigsis.mom.1c": ["bigsis", "...Also fine. Probably."],
  "home.talk.bigsis.mom.2a": ["bigsis", "I have begun a new chapter. It is called 'The Night They Didn't Come Home'. Provisionally."],   // PASS-19H1: her whole words; shorter
  "home.talk.bigsis.mom.2b": ["mom", "Then do give it a happy ending, darling. Your father will insist on reading it."],
  "home.talk.bigsis.lilsis.key.a": ["bigsis", "There is a panel by the pedals that lifts off, and you are the only one of us who fits under there."],   // PASS-19H1: shorter
  "home.talk.bigsis.lilsis.key.b": ["lilsis", "I KNOW. That's where I keep my marble."],   // PASS-19H1: shorter
  "home.talk.bigsis.lilsis.1a": ["bigsis", "Please do not touch anything while I am thinking. It interrupts the thinking."],   // PASS-19H1: her whole words
  "home.talk.bigsis.lilsis.1b": ["lilsis", "I'm not touching. I'm HOLDING."],
  "home.talk.bigsis.lilsis.2a": ["lilsis", "Why do you know so many years?"],
  "home.talk.bigsis.lilsis.2b": ["bigsis", "Because somebody in this family must. Years do not remember themselves."],   // PASS-19H1: her whole words
  "home.talk.lilsis.mom.1a": ["lilsis", "Mommy, I can help. I'm small, but I'm MIGHTY. Point me at something."],
  "home.talk.lilsis.mom.1b": ["mom", "You're the mightiest person I know, my love. Do aim it carefully."],
  "home.talk.lilsis.mom.2a": ["lilsis", "Can I stay up?"],
  "home.talk.lilsis.mom.2b": ["mom", "Tonight, yes."],
  "home.talk.lilsis.mom.2c": ["lilsis", "...Now I'm worried."],
  "home.talk.lilsis.mom.3a": ["lilsis", "Mommy, sit down for a minute. I'll do the worrying. I'm really good at it."],   // PASS-19H1: shorter
  "home.talk.lilsis.mom.3b": ["mom", "Five minutes, my love. Then I'll want my worrying back."],   // PASS-17H: Mom's formality ('shall')
  "home.talk.lilsis.bigsis.1a": ["lilsis", "Read me a fact."],
  "home.talk.lilsis.bigsis.1b": ["bigsis", "It is 'tell me a fact'."],   // PASS-19H1: her whole words
  "home.talk.lilsis.bigsis.1c": ["lilsis", "Tell me a READ."],
  "home.talk.lilsis.bigsis.2a": ["lilsis", "My tooth is loose. Look. LOOK."],
  "home.talk.lilsis.bigsis.2b": ["bigsis", "I have seen the tooth. Everyone on this street has seen the tooth."],

  // =====================================================================================================
  // THE LANDING
  // =====================================================================================================
  "home.landing.first.1": ["bigsis", "That is Dad's study, with the notice on the door. It is always locked. Always."],   // PASS-19H1: shorter
  "home.landing.first.2": ["mom", "With your father, darling, there's always a notice."],
  "home.landing.first.3": ["lilsis", "My brother's door says 'NO GIRLS ALLOWED.' We'll SEE about that."],   // PASS-19H1: emphasis (a sign read out)

  "home.landing.window.mom": ["mom", "The same moon's over them, wherever they've got to. I find that unexpectedly useful."],   // PASS-19H1: shorter
  "home.landing.window.bigsis": ["bigsis", "A bright moon. Bright enough to read by, if a person's mother were to allow it."],   // PASS-19H1: shorter; one idea
  "home.landing.window.lilsis": ["lilsis", "The moon always follows our car. So it's following Daddy right now. Good moon."],   // PASS-19H1: emphasis; shorter; one idea
  "home.ladder.mom": ["mom", "She asked for the attic. I said yes before I'd thought about the ladder."],   // PASS-19H1: shorter; punch last
  "home.ladder.bigsis": ["bigsis", "The way up to the Retreat. Visitors are admitted strictly by appointment."],   // PASS-19H1: shorter; punch last; one idea
  "home.ladder.lilsis": ["lilsis", "The card says 'THE RETREAT.' My visiting hours are SHORT."],   // PASS-19H1: shorter; emphasis; one idea
  "home.landing.photos.mom": ["mom", "Our wedding. He was forty minutes late to it, and he would not ask the way."],   // PASS-19H1: shorter
  "home.landing.photos.bigsis": ["bigsis", "I was a serious baby. Here I am frowning at a rattle."],   // PASS-19H1: shorter; one idea
  "home.landing.photos.lilsis": ["lilsis", "Me with no teeth. Me with all my teeth. Soon, me with one less."],   // PASS-19H1: shorter; emphasis; three, the best last
  "home.hamper.mom": ["mom", "The hamper was empty at noon. I admire the industry."],   // PASS-19H1: shorter; punch last
  "home.hamper.bigsis": ["bigsis", "The laundry hamper. I have no comment on the hamper."],
  "home.hamper.lilsis": ["lilsis", "The flock gets promoted in the hamper. Corporal Speckle's next."],   // PASS-19H1: emphasis; shorter
  "home.lildoor.mom": ["mom", "'BEWARE OF CHICKENS.' She asked me how to spell 'beware'. I didn't ask why."],   // PASS-19H1: explanation cut
  "home.lildoor.bigsis": ["bigsis", "Stickers, a crayon hen, a warning. The warning is accurate."],   // PASS-19H1: shorter
  "home.lildoor.lilsis": ["lilsis", "My door. I did the letters, the hen, and ALL the stickers."],   // PASS-19H1: emphasis; shorter
  "home.halltable.mom": ["mom", "Every key this family owns, except the two I want tonight."],   // PASS-19H1: shorter
  "home.halltable.bigsis": ["bigsis", "Three keys nobody can name, and no study key. I have looked."],   // PASS-19H1: shorter; one idea
  "home.halltable.lilsis": ["lilsis", "I'm not allowed to play pirates with the key bowl. Anymore."],   // PASS-19H1: emphasis; one idea
  "home.halltable.use.mom": ["mom", "I've been through this bowl twice, and I'm not above a third. ...No."],   // PASS-19H1: one idea
  "home.halltable.use.bigsis": ["bigsis", "Nothing labeled 'study'. Coming from Dad, that is itself a clue."],   // PASS-19H1: shorter; one idea
  "home.halltable.use.lilsis": ["lilsis", "Jingle jingle jingle. ...I'm HELPING."],
  "home.countdown.mom": ["mom", "A day crossed off every breakfast. Today is the little car."],   // PASS-19H1: shorter
  "home.countdown.bigsis": ["bigsis", "He crossed off today before it happened. I let it stand."],   // PASS-19H1: shorter
  "home.countdown.lilsis": ["lilsis", "The red car at the end is today. Daddy's still coming."],   // PASS-19H1: emphasis; shorter
  "home.landing.stairs.mom": ["mom", "I've carried you all up these asleep. You were a great deal lighter."],   // PASS-19H1: shorter
  "home.landing.stairs.bigsis": ["bigsis", "The same sixteen steps down. I checked on the way up."],   // PASS-19H1: shorter; one idea
  "home.landing.stairs.lilsis": ["lilsis", "I can do the stairs two at a time. Mommy says don't."],   // PASS-19H1: emphasis; shorter; one idea
  "home.rail.mom": ["mom", "From up here it looks like a lit set, waiting. Two of the cast are late for their entrance."],   // PASS-19H1: shorter
  "home.rail.bigsis": ["bigsis", "'The room below,' she wrote, 'was a sentence missing two words.'"],   // PASS-19H1: shorter
  "home.rail.lilsis": ["lilsis", "I can see the piano, the rug and Daddy's door. Still shut."],   // PASS-19H1: emphasis; shorter; one idea

  // ---- the Son's door: NO GIRLS ALLOWED, and booby-trapped. Mom does not try it tonight. The first time a sister opens
  // it, his toy alarm (.alarm.1; Little Sister does the password, .2 and .3), a volley of foam darts, the author's line
  // for Big Sister (.trap.bigsis, word for word), Little Sister's say, and Mom's "not tonight" (.alarm.4 to her, .trap.mom
  // to her sister). The second time, the one dart he kept back (.dart). After that nobody tries (.again); and the darts
  // stay on the runner (.after, looking at the door).
  "home.son.look.mom": ["mom", "'NO GIRLS ALLOWED.' Spelled right this year. I was so proud I nearly obeyed."],   // PASS-19H1: shorter; punch last
  "home.son.look.bigsis": ["bigsis", "Smaller notices too. One is addressed to me personally."],   // PASS-19H1: shorter
  "home.son.look.lilsis": ["lilsis", "'NO GIRLS ALLOWED'? I'm not a girl. I'm a SISTER."],   // PASS-19H1: explanation cut; punch last
  "home.son.use.mom": ["mom", "I'm his mother. He counts that as a separate thing. ...Not tonight."],   // PASS-19H1: shorter
  "home.son.use.bigsis": ["bigsis", "I decline to guess: it will be about snacks. I shall simply open it."],   // PASS-19H1: shorter; one idea
  "home.son.alarm.1": ["son", "'HALT! This is Operation No Girls. What's the password?'"],
  "home.son.alarm.2": ["lilsis", "'The password is: I still want a dog.' I've watched him."],   // PASS-19H1: shorter; explanation cut
  "home.son.alarm.3": ["son", "'Password CORRECT. Ten out of ten. You may enter, me.'"],
  "home.son.trap.bigsis": ["bigsis", "I don't want to go in there. The rug is probably booby-trapped."],
  "home.son.trap.lilsis": ["lilsis", "It said 'CORRECT.' Then it SHOT me. ...It was a good trap, though."],   // PASS-19H1: emphasis; shorter; punch last
  "home.son.trap.lilsis.2": ["lilsis", "He got you. ...I'm making a sign. 'NO BROTHERS.' Except on Saturdays."],   // PASS-19H1: second joke cut; emphasis; punch last
  "home.son.trap.mom": ["mom", "Not tonight, darling. I am not ready to look at that room with nobody in it."],
  "home.son.alarm.4": ["mom", "Not tonight, sweetheart. I am not ready to look at that room with nobody in it."],
  "home.son.alarm.5": ["lilsis", "...I'll shut it. He'd want me to shut it."],   // PASS-19H1: filler cut
  "home.son.again": ["lilsis", "Mommy said not tonight. I'm getting good at waiting."],   // PASS-19H1: shorter; one idea
  "home.son.dart.lilsis": ["lilsis", "He saved one for me. That's not a trap. That's just RUDE."],   // PASS-19H1: emphasis; shorter
  "home.son.dart.bigsis": ["bigsis", "He kept one in reserve, and I respect that. I am still not going in."],   // PASS-19H1: one idea
  "home.son.again.bigsis": ["bigsis", "No. I stand by what I said about the rug."],
  "home.son.after.mom": ["mom", "I'm leaving his darts where they fell. He'll want to count them."],   // PASS-19H1: shorter
  "home.son.after.bigsis": ["bigsis", "He will want a full report. I intend to say it was adequate."],   // PASS-19H1: shorter
  "home.son.after.lilsis": ["lilsis", "His darts are all over the rug. Nobody touch the EVIDENCE."],   // PASS-19H1: emphasis; one idea
  "home.son.key.mom": ["mom", "That key's for the study. This door only ever had opinions."],   // PASS-19H1: shorter; one idea
  "home.son.key.bigsis": ["bigsis", "No keyhole. A toy alarm and a great deal of confidence."],   // PASS-19H1: shorter
  "home.son.key.lilsis": ["lilsis", "It has a password. Passwords are keys you say."],   // PASS-19H1: emphasis
  "home.bag.mom": ["mom", "His school bag, hanging on its peg. It's never once been there on a school morning."],   // PASS-19H1: shorter
  "home.bag.bigsis": ["bigsis", "A holiday sandwich is in there. I will not be the one to find it."],   // PASS-19H1: shorter
  "home.bag.lilsis": ["lilsis", "I'm guarding his bag. Nobody touch it. Not even me."],   // PASS-19H1: emphasis; shorter; one idea; FINAL-19: REVIEW-19's patch

  // ---- chain A: Dad's notice, and the study door
  "home.sign.lilsis": ["lilsis", "'LOST YOUR KEY? IT IS WITH THE OTHER EIGHTY-EIGHT.' Daddy has a lot of doors."],   // PASS-19H1: emphasis; shorter; punch last
  "home.sign.bigsis.1": ["bigsis", "'Lost your key? It is with the other eighty-eight.' ...Eighty-eight what?"],   // PASS-19H1: shorter
  "home.sign.bigsis.2": ["bigsis", "...Keys. A standard piano has eighty-eight. The study key is in ours."],   // PASS-19H1: shorter; 'Fun fact' rationed
  "home.sign.mom.react": ["mom", "He has hidden a key in MY piano. Of all the places in this house."],
  "home.sign.mom.1": ["mom", "'Lost your key? It is with the other eighty-eight.' Oh, my love."],   // PASS-19H1: shorter
  "home.sign.mom.2": ["mom", "A matter of record: a full-size piano has eighty-eight keys. MY piano."],   // PASS-19H1: shorter; punch last
  "home.sign.bigsis.react": ["bigsis", "Eighty-eight. I was half a second behind you, Mother. Half."],
  "home.sign.thunk.mom": ["mom", "'The other eighty-eight.' So that was the thunk: his study key."],   // PASS-19H1: shorter
  "home.sign.thunk.bigsis": ["bigsis", "'The other eighty-eight.' So that is what went 'thunk'."],   // PASS-19H1: shorter; punch last
  "home.sign.again.mom": ["mom", "'Authorized personnel only.' He means himself and the boy."],   // PASS-19H1: shorter; one idea
  "home.sign.again.bigsis": ["bigsis", "Block capitals and a riddle. For Dad, a formal document."],   // PASS-19H1: shorter
  "home.study.look.mom": ["mom", "Your father's study. The one door he locks, and the one we need."],   // PASS-17H: Mom's formality
  "home.study.look.bigsis": ["bigsis", "Dad's study. One lock, one notice, no key. In that order."],
  "home.study.look.lilsis": ["lilsis", "Daddy's room. It's for 'planning'. Planning is maps and snacks."],
  "home.study.open.mom": ["mom", "Open. I half expect him in there, saying 'well, well, well'."],
  "home.study.open.bigsis": ["bigsis", "Trip Headquarters is open. I am authorized personnel now."],
  "home.study.open.lilsis": ["lilsis", "It's OPEN! Don't touch anything. I'm going to touch everything."],
  "home.study.locked.mom": ["mom", "Locked, naturally. He's left us a notice instead of a key, which is very like him."],   // PASS-17H: Mom's formality
  "home.study.locked.bigsis": ["bigsis", "Locked. The notice says where the key is. It simply does not say it in English."],
  "home.study.locked.lilsis": ["lilsis", "It's LOCKED. Daddy, open up! ...He can't hear me. I forgot."],
  "home.study.theirs.mom.bigsis": ["mom", "Your big sister has the key, darling. Let her do the honors."],
  "home.study.theirs.mom.lilsis": ["mom", "Your little sister has the key. She fetched it, so she turns it."],   // PASS-17H: Mom's formality ('shall')
  "home.study.theirs.bigsis.mom": ["bigsis", "Mom has the key. Technically she outranks the Management."],
  "home.study.theirs.bigsis.lilsis": ["bigsis", "My sister has the key. She will be sleeping with it."],
  "home.study.theirs.lilsis.mom": ["lilsis", "Mommy's got the key! Mommy, do the DOOR."],
  "home.study.theirs.lilsis.bigsis": ["lilsis", "She's got the key. She's being slow on PURPOSE."],
  "home.study.unlock.mom": ["mom", "There. 'Authorized personnel only.' I authorized myself on our wedding day."],
  "home.study.unlock.bigsis": ["bigsis", "It turns. Trip Headquarters is under new management."],
  "home.study.unlock.lilsis": ["lilsis", "It went! I opened Daddy's door with the PIANO key."],

  // ---- what they say to each other on the landing
  "home.talk.landing.mom.bigsis.sign.a": ["mom", "Your father's left us a riddle on that notice. You're better at his riddles than I am, darling."],   // PASS-17H: one darling fewer
  "home.talk.landing.mom.bigsis.sign.b": ["bigsis", "There is a number in it, and with Dad a number is never decoration. I should like to read it again."],   // PASS-19H1: shorter
  "home.talk.landing.mom.bigsis.1a": ["mom", "As a schoolboy, George Washington copied out 110 Rules of Civility."],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.talk.landing.mom.bigsis.1b": ["bigsis", "Is one of them 'Do not hide keys in your wife's piano'?"],
  "home.talk.landing.mom.bigsis.1c": ["mom", "It's implied, darling. Throughout."],   // PASS-17H: Mom's formality
  "home.talk.landing.mom.bigsis.2a": ["mom", "You take after me. It's the nicest thing I can say about either of us."],   // PASS-19H1: shorter; one idea
  "home.talk.landing.mom.bigsis.2b": ["bigsis", "I take after you with footnotes."],
  "home.talk.landing.mom.lilsis.1a": ["lilsis", "Mommy, is my brother scared? Because I'm NOT."],   // PASS-19H1: shorter
  "home.talk.landing.mom.lilsis.1b": ["mom", "Your brother has never been scared of anything. That's the part that scares me."],   // PASS-19H1: shorter
  "home.talk.landing.mom.lilsis.2a": ["mom", "Hold the rail on the stairs, sweetheart."],
  "home.talk.landing.mom.lilsis.2b": ["lilsis", "I AM holding it."],
  "home.talk.landing.mom.lilsis.2c": ["mom", "With a hand, darling."],
  "home.talk.landing.bigsis.mom.1a": ["bigsis", "Mom. When they are back, I intend to be extremely calm about it."],
  "home.talk.landing.bigsis.mom.1b": ["mom", "I intend the same, darling. We'll be calm together, at some volume."],   // PASS-19H1: shorter; filler cut
  "home.talk.landing.bigsis.mom.2a": ["bigsis", "John Adams and Thomas Jefferson died on the same day. The fourth of July, 1826."],   // PASS-19H1: shorter; 'Fun fact' rationed
  "home.talk.landing.bigsis.mom.2b": ["mom", "Fifty years to the day after the Declaration. A matter of record."],   // PASS-19H1: shorter; punch last
  "home.talk.landing.bigsis.mom.2b.b": ["mom", "And I told YOU that one."],   // PASS-19H1: new; punch own box
  "home.talk.landing.bigsis.lilsis.1a": ["bigsis", "Do not slide down the banister."],
  "home.talk.landing.bigsis.lilsis.1b": ["lilsis", "I wasn't GOING to. ...Now I'm thinking about it."],
  "home.talk.landing.bigsis.lilsis.2a": ["lilsis", "Do you know his password?"],
  "home.talk.landing.bigsis.lilsis.2b": ["bigsis", "I have never asked. A person is entitled to one noisy secret."],   // PASS-19H1: shorter; punch last; one idea
  "home.talk.landing.lilsis.mom.1a": ["lilsis", "Mommy, can I say my bedtime prayer if it isn't bedtime?"],
  "home.talk.landing.lilsis.mom.1b": ["mom", "Any time, my love. He isn't listening for the clock. He's listening for you."],   // PASS-19H1: shorter
  "home.talk.landing.lilsis.mom.2a": ["lilsis", "When Daddy's home, can we have the same dinner? I saved him my potato."],   // PASS-19H1: shorter; emphasis
  "home.talk.landing.lilsis.mom.2b": ["mom", "A fresh one, darling. That one has done its duty."],
  "home.talk.landing.lilsis.bigsis.1a": ["lilsis", "Why doesn't YOUR ladder have stickers?"],
  "home.talk.landing.lilsis.bigsis.1b": ["bigsis", "One card. It is not boring, it is restrained."],   // PASS-19H1: shorter; one idea
  "home.talk.landing.lilsis.bigsis.2a": ["lilsis", "Are you writing this down for your book?"],
  "home.talk.landing.lilsis.bigsis.2b": ["bigsis", "Every word."],
  "home.talk.landing.lilsis.bigsis.2c": ["lilsis", "Write that I was BRAVE."],

  // =====================================================================================================
  // DAD'S STUDY
  // =====================================================================================================
  "home.study.first.1": ["mom", "Trip Headquarters. He hasn't let me dust in here since March."],   // PASS-17H: Mom's formality
  "home.study.first.2": ["bigsis", "That box on the shelves is the 'family vault'. It has, you will notice, a label."],
  "home.study.first.3": ["lilsis", "Something's BLINKING. Over there, on the drawer thing!"],

  // ---- chain C: the family computer, and the note on it
  "home.pc.look.mom": ["mom", "The family computer. Nine years old, and it sighs when you switch it on."],
  "home.pc.look.bigsis": ["bigsis", "It runs the family map. It also runs. Technically."],
  "home.pc.look.lilsis": ["lilsis", "The computer! It has a game where a cat eats numbers."],
  "home.pc.offline.mom": ["mom", "'No internet.' It worked perfectly well until your father improved it."],
  "home.pc.offline.bigsis": ["bigsis", "October 1969: what became the internet tried LOGIN. It crashed at 'LO'."],
  "home.pc.offline.bigsis2": ["bigsis", "So this is traditional."],
  "home.pc.offline.lilsis": ["lilsis", "It says NO. Computers aren't allowed to say no. I'm telling Mommy."],
  "home.pc.login.mom": ["mom", "Four numbers. 'Forgot it? Ask Dad.' I would dearly love to."],
  "home.pc.login.bigsis": ["bigsis", "Four digits: ten thousand possibilities. Dad will have written it down somewhere. He always does."],
  "home.pc.login.lilsis": ["lilsis", "One, two, three, four! ...It said no AGAIN."],
  "home.pc.type.mom": ["mom", "One. Nine. Two. Eight."],
  "home.pc.type.bigsis": ["bigsis", "One, nine, two, eight, with all ten fingers. It is not difficult."],
  "home.pc.type.lilsis": ["lilsis", "One. Nine. Two. Eight. I typed it with ONE finger!"],
  "home.pc.question.mom": ["mom", "'What did you promise on your wedding day?' Oh, my love. You would."],
  "home.pc.question.bigsis": ["bigsis", "'What did you promise on your wedding day?' I was not invited. Mother?"],
  "home.pc.question.lilsis": ["lilsis", "It's asking about a wedding. I wasn't BORN. Mommy!"],
  "home.pc.pick.love": ["mom", "To love, honor and cherish."],
  "home.pc.pick.scenic": ["mom", "To always take the scenic route."],
  "home.pc.pick.directions": ["mom", "To never ask for directions."],
  "home.pc.wrong.love": ["mom", "No? I did say that. I had hoped he was listening."],
  "home.pc.wrong.scenic": ["mom", "No. That was not a promise. That was a warning."],
  "home.pc.right": ["mom", "He promised never to ask for directions. It's the one promise he's always kept."],
  "home.pc.map.1": ["mom", "'Last seen 5:47 p.m. Thirty-seven miles past Last Gas.' In the middle of Nevada."],
  "home.pc.map.2": ["bigsis", "That is not on the way home. That is not on the way to anywhere."],
  "home.pc.map.six": ["bigsis", "5:47. His message was 5:41. Six minutes later, his phone stops."],
  "home.pc.map.3": ["lilsis", "Is Nevada past the mailbox?"],
  "home.pc.map.4": ["mom", "A little past the mailbox, darling. Shoes on. We leave tonight."],
  "home.pc.done.mom": ["mom", "One dot, in the middle of nothing. I've looked at it quite long enough."],
  "home.pc.done.bigsis": ["bigsis", "Thirty-seven miles past Last Gas. I have memorized it. I could not stop myself if I tried."],
  "home.pc.done.lilsis": ["lilsis", "The dot is Daddy. Hi, dot."],
  "home.pc.pencil.lilsis": ["lilsis", "I poked the screen with Daddy's pencil. Now there's a bad dot."],

  "home.note.look.mom": ["mom", "'Password: the year of the best thing since.' Since WHAT, my love?"],
  "home.note.look.lilsis": ["lilsis", "It says 'PASS WORD', and more words. Daddy does the loopy Ys."],
  "home.note.take.mom": ["mom", "I'll keep this. It's the nearest thing to your father in the house."],
  "home.note.take.lilsis": ["lilsis", "MINE. I mean: evidence."],
  "home.note.solve.1": ["bigsis", "'The year of the best thing since.' ...Since sliced bread."],
  "home.note.solve.1.b": ["mom", "He said that about the toaster."],
  "home.note.solve.2": ["bigsis", "Sliced bread: first sold on the seventh of July, 1928, in Chillicothe, Missouri."],
  "home.note.solve.3": ["bigsis", "The password is 1928. Dad, that is so... actually, that is quite good."],

  // ---- chain D: the answering machine, its tape, and Dad's last message
  "home.machine.look.mom": ["mom", "His answering machine. Its tape is meant to be on the inside."],   // PASS-17H: Mom's formality
  "home.machine.look.bigsis": ["bigsis", "'One new message.' And a loop of tape hanging out, like a tongue."],
  "home.machine.look.lilsis": ["lilsis", "I FIXED that last week! ...It was working before I fixed it."],
  "home.machine.ready.mom": ["mom", "Wound, and blinking. One new message. I want to hear it, and I don't."],   // PASS-17H: the speech that is really an essay
  "home.machine.ready.bigsis": ["bigsis", "One new message. The button marked PLAY is the large one."],
  "home.machine.ready.lilsis": ["lilsis", "The answer machine's got an answer in it. Press the BIG button."],
  "home.machine.flash": ["lilsis", "I shined my flashlight in its window. It has EYES."],
  "home.tape.need.mom": ["mom", "I'll need a pencil to wind it back in. An ordinary wooden one, with some heft to it."],
  "home.tape.need.bigsis": ["bigsis", "A pencil in the hub winds a cassette. Mine are too slim. Dad's is not."],
  "home.tape.need.lilsis": ["lilsis", "I'm not allowed to fix it again. Mommy said. With her whole-name voice."],
  "home.tape.where": ["mom", "The only pencil anybody in this house can ever find is the one on his crossword."],   // PASS-17H: Mom's formality
  "home.tape.has.mom": ["mom", "I have his pencil. Stand aside, darlings. This is my department."],
  "home.tape.has.bigsis": ["bigsis", "I have Dad's pencil. Mom should do the winding; she knows which way it turns."],
  "home.tape.has.lilsis": ["lilsis", "I've got Daddy's pencil. Mommy needs it. In a minute. ...Okay, NOW."],
  "home.tape.notme.bigsis": ["bigsis", "That tape has his voice on it. Mom should be the one to do this."],
  "home.tape.notme.lilsis": ["lilsis", "I'm not ALLOWED. I fixed it last time. Mommy has to."],
  "home.tape.wind.1": ["mom", "I taped whole musicals off the radio on these. Pencil in the hub, gently."],
  "home.tape.wind.2": ["mom", "There. Every inch of it home again, and not one crease. Patience, darlings, and a steady pencil."],
  "home.tape.wind.3": ["bigsis", "So the knack is going slower than you want to. Noted, and underlined."],
  "home.tape.wind.4": ["lilsis", "It's still blinking. Can I press it? I'm asking really FAST."],
  "home.msg.1": ["dad", "'Hi, honey. It's 5:41 and we're making GREAT time. I found a shortcut.'"],
  "home.msg.2": ["dad", "'Thirty-seven miles past the last gas station, and not one other car.'"],
  "home.msg.2.b": ["son", "'Hi, Mom! Dad, that sign up there looks funny.'"],
  "home.msg.3": ["dad", "'...Huh. That IS funny.'"],
  "home.msg.4": ["dad", "'That sign just changed its--'"],
  "home.msg.after.lilsis": ["lilsis", "Changed its WHAT? Daddy? Changed its what?"],
  "home.msg.after.bigsis": ["bigsis", "5:41 p.m. The last anybody heard. I am writing down the minute."],
  "home.msg.after.bigsis.six": ["bigsis", "5:41 on the tape. 5:47 on the map. Whatever happened took six minutes."],
  "home.msg.after.mom": ["mom", "No need to play it twice. He sounded happy, and terribly pleased with his shortcut. Let's hold on to that."],
  "home.msg.again.mom": ["mom", "Once was enough, my love. I have every word of it by heart, down to the 'Huh'."],
  "home.msg.again.bigsis": ["bigsis", "5:41 p.m. I have it memorized. Including the hiss."],
  "home.msg.again.lilsis": ["lilsis", "Changed its WHAT. I'm asking him first thing, before the hug. Okay, after the hug."],

  // ---- chain E: the family vault
  "home.vault.read.mom": ["mom", "'The year WE THE PEOPLE got it in writing.' ...I do NOT bring it up. Not often."],
  "home.vault.read.bigsis": ["bigsis", "'The year We the People got it in writing.' Mom will know which."],
  "home.vault.read.lilsis": ["lilsis", "It says 'Your mother will know.' MOMMY! The box says you know."],
  "home.vault.pick.1776": ["mom", "Seventeen seventy-six."],
  "home.vault.pick.1787": ["mom", "Seventeen eighty-seven."],
  "home.vault.pick.1789": ["mom", "Seventeen eighty-nine."],
  "home.vault.pick.later": ["mom", "Let me think about that a moment longer."],
  "home.vault.wrong.1776": ["mom", "No. 1776 is the Declaration, the Fourth of July. 'We the People' came later."],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.vault.wrong.1789": ["mom", "No. 1789 is the new government, and General Washington's oath. Too late."],
  "home.vault.right.1": ["mom", "1787. Signed in Philadelphia in September. He does listen. Just not at the time."],
  "home.vault.right.2": ["mom", "My spare car key, two packets of ketchup, and a card: 'KNEW YOU'D KNOW. - THE MANAGEMENT.'"],
  "home.vault.right.3": ["bigsis", "He keeps ketchup in a vault."],
  "home.vault.right.4": ["lilsis", "Is that the treasure? Daddy wouldn't lock up ketchup unless it was treasure. Can I have it?"],
  "home.vault.right.5": ["mom", "The ketchup stays, darling. I have never once asked what he's saving it for, and I'm not starting tonight."],   // PASS-17H: Mom's formality
  "home.vault.done.mom": ["mom", "Empty, but for his card and his condiments."],   // PASS-17H: Mom's formality
  "home.vault.done.bigsis": ["bigsis", "A vault, opened by the Constitution of the United States. I will be footnoting that."],
  "home.vault.done.lilsis": ["lilsis", "The treasure box is open, and Daddy's treasure is ketchup. I'm not even surprised."],
  "home.vault.key.mom": ["mom", "No keyhole, only a dial. Your father does like a dial. It lets him be mysterious on a budget."],   // PASS-17H: one darling fewer
  "home.vault.key.bigsis": ["bigsis", "A combination lock, and no keyhole. Dad does not cheat at his own riddles: the answer will be in the clue."],
  "home.vault.key.lilsis": ["lilsis", "There's no hole for a key. Just a little wheel that goes CLICK when you turn it."],

  // ---- the rest of the study
  "home.wallmap.mom": ["mom", "His whole route, in red wool. And one yellow piece, striking off across nothing at all."],
  "home.wallmap.bigsis": ["bigsis", "Yellow string, along a road that simply stops. Yellow is the color of caution, and he chose it himself."],
  "home.wallmap.lilsis": ["lilsis", "The red string is Daddy driving. The yellow one is Daddy being clever."],
  "home.wallmap.pencil.mom": ["mom", "Not on his map, darling. I'll be having a word with him about that yellow string."],   // PASS-17H: Mom's formality ('shall')
  "home.wallmap.pencil.bigsis": ["bigsis", "I am not correcting Dad's map. I am correcting Dad. In person."],
  "home.wallmap.pencil.lilsis": ["lilsis", "I drew a tiny car on the string, with the General in the back window. Keeping an eye out."],
  "home.corkboard.mom": ["mom", "Your brother's plan for the trip. Step one is 'snacks'. So, I notice, are steps two through five."],
  "home.corkboard.bigsis": ["bigsis", "My brother's snack schedule, every snack rated out of ten. In advance. Before tasting a single one."],
  "home.corkboard.lilsis": ["lilsis", "He made the luggage taller than the car. That part's TRUE."],
  "home.shelves.mom": ["mom", "His manuals. Every one of them read precisely as far as the middle, and not one page further."],
  "home.shelves.bigsis": ["bigsis", "Jars of screws. One is labeled 'MISC'. So are all the others."],
  "home.shelves.lilsis": ["lilsis", "That jar's got googly eyes in it. I'm not saying whose."],
  "home.globe.mom": ["mom", "'Anywhere but the interstate,' he says. I should have listened."],
  "home.globe.bigsis": ["bigsis", "A globe tells you where. Tonight 'where' feels like half the question."],   // PASS-17H: truer; it plants 'when' without saying it
  "home.globe.lilsis": ["lilsis", "It opens in the middle. Daddy says it's not an egg. It's SO an egg."],
  "home.globe.use.mom": ["mom", "I won't spin it. Tonight there's only one small corner of it I care about."],   // PASS-17H: Mom's formality ('shall')
  "home.globe.use.bigsis": ["bigsis", "It stops on Nevada every single time. Dad has leaned on it, and not by accident."],
  "home.globe.use.lilsis": ["lilsis", "I stopped it with my finger. Daddy's in... the ocean."],
  "home.study.window.mom": ["mom", "Just the oil spot where the wagon sleeps. I'll take that up with him too, once he's home."],   // PASS-17H: Mom's formality ('shall')
  "home.study.window.bigsis": ["bigsis", "The whole street. I have looked. It has not helped."],
  "home.study.window.lilsis": ["lilsis", "Swings look sad in the dark. Tomorrow Daddy's pushing me SO high."],
  "home.banner.mom": ["mom", "Your father did TRIP. Your brother did the rest, one color a letter."],
  "home.banner.bigsis": ["bigsis", "Dad ruled his in pencil. My brother did his freehand. His is the better half."],
  "home.banner.lilsis": ["lilsis", "I held the tape for the banner, and nobody put my name on it. I'm adding it later. In PINK."],
  "home.plane.mom": ["mom", "He and your brother built it. It took every clothespin I own."],   // PASS-17H: American: clothespin
  "home.plane.bigsis": ["bigsis", "It hangs by a thread. The thread was my condition for sharing a roof."],
  "home.plane.lilsis": ["lilsis", "It goes round if you blow. I'm not allowed to blow. I blow a LITTLE."],
  "home.boxes.mom": ["mom", "The tent, the cooler, and the box of maps. He left the maps."],   // PASS-17H: Mom's formality
  "home.boxes.bigsis": ["bigsis", "The box says 'MAPS', in his capitals. He walked straight past it."],
  "home.boxes.lilsis": ["lilsis", "They took every juice box. Daddy and I are having a TALK."],
  "home.study.door.mom": ["mom", "I'm leaving this door open. Next time he'll only hide the key somewhere worse than my piano."],   // PASS-17H: Mom's formality
  "home.study.door.bigsis": ["bigsis", "I am not finished in here. I may never be finished in here."],
  "home.study.door.lilsis": ["lilsis", "The door we opened with the key I got. Out of the PIANO."],

  // ---- what they say to each other in the study
  "home.talk.study.mom.bigsis.note.a": ["mom", "Your father's left us a riddle about a year, darling. Years have always been your department."],
  "home.talk.study.mom.bigsis.note.b": ["bigsis", "Then may I have it, please? I think better with the paper in my hands."],
  "home.talk.study.mom.bigsis.1a": ["mom", "Bach wrote 'S.D.G.' at the end of many of his scores. 'To God alone the glory.'"],   // PASS-17H: 'A matter of record' as a gag, not a habit
  "home.talk.study.mom.bigsis.1b": ["bigsis", "Dad writes 'THE MANAGEMENT' at the end of his."],
  "home.talk.study.mom.bigsis.2a": ["mom", "Your father planned this trip for a month, up here, with your brother at his elbow."],
  "home.talk.study.mom.bigsis.2b": ["bigsis", "And then he took a shortcut."],
  "home.talk.study.mom.bigsis.2c": ["mom", "And then he took a shortcut."],
  "home.talk.study.mom.lilsis.1a": ["mom", "Hands, sweetheart."],
  "home.talk.study.mom.lilsis.1b": ["lilsis", "I'm not touching. I'm looking with my hands."],
  "home.talk.study.mom.lilsis.2a": ["lilsis", "Mommy, what's a headquarters?"],
  "home.talk.study.mom.lilsis.2b": ["mom", "It's where the plans get made, darling. The mistakes get made on the road."],   // PASS-17H: Mom's formality
  "home.talk.study.bigsis.mom.vault.a": ["bigsis", "Mother. 'The year We the People got it in writing.' That is your territory, not mine. Which year?"],
  "home.talk.study.bigsis.mom.vault.b": ["mom", "The one in the frame on our living-room wall. Leave the dial to me, darling. I know that one in my sleep."],   // PASS-17H: Mom's formality ('shall'); one darling fewer
  "home.talk.study.bigsis.mom.dot.a": ["bigsis", "Mother. What if we drive all the way to the dot, and they are not there?"],
  "home.talk.study.bigsis.mom.dot.b": ["mom", "Then we keep looking. You don't stop the show for a missing cast member, darling. You go and fetch him."],
  "home.talk.study.bigsis.mom.1a": ["bigsis", "Dad refers to this computer as 'the mainframe'. It is not a mainframe."],
  "home.talk.study.bigsis.mom.1b": ["mom", "He calls the car 'she', and himself 'the Management'. He has a gift for names."],
  "home.talk.study.bigsis.mom.2a": ["bigsis", "If he had simply written down the route, like a reasonable person..."],
  "home.talk.study.bigsis.mom.2b": ["mom", "Then it wouldn't have been a shortcut, darling. It would have been a plan."],   // PASS-17H: Mom's formality
  "home.talk.study.bigsis.lilsis.1a": ["bigsis", "Do not spin the globe. Do not open the jars. Do not fix anything."],
  "home.talk.study.bigsis.lilsis.1b": ["lilsis", "That's ALL the good ones."],
  "home.talk.study.bigsis.lilsis.2a": ["lilsis", "What's a mainframe?"],
  "home.talk.study.bigsis.lilsis.2b": ["bigsis", "It is what Dad calls a nine-year-old computer. It is a term of affection, and also of denial."],
  "home.talk.study.lilsis.mom.tape.a": ["lilsis", "Mommy, I only fixed the tape machine a LITTLE."],
  "home.talk.study.lilsis.mom.tape.b": ["mom", "I can mend it, sweetheart. All it wants is one ordinary pencil and a moment's quiet. Mostly the quiet."],
  "home.talk.study.lilsis.mom.1a": ["lilsis", "Is Daddy in trouble?"],
  "home.talk.study.lilsis.mom.1b": ["mom", "A little, my love. He has to come home first. The trouble will keep."],   // PASS-17H: Mom's formality
  "home.talk.study.lilsis.mom.2a": ["lilsis", "Mommy, why does Daddy have SO many jars?"],
  "home.talk.study.lilsis.mom.2b": ["mom", "Because he has so many screws. Which is because he has so many jars."],   // PASS-17H: funnier: the answer goes round in a circle; one darling fewer
  "home.talk.study.lilsis.bigsis.1a": ["lilsis", "My tooth's SO loose. I told it to wait till Daddy's home, so he can see it come out."],
  "home.talk.study.lilsis.bigsis.1b": ["bigsis", "You are negotiating with a tooth. I would not bet against you."],
  "home.talk.study.lilsis.bigsis.2a": ["lilsis", "If the computer's broken, I can fix it. I fixed the tape machine."],
  "home.talk.study.lilsis.bigsis.2b": ["bigsis", "That is exactly why I am standing between you and the computer."],

  // =====================================================================================================
  // LITTLE SISTER'S ROOM (it was the girls' room until Big Sister's thirteenth birthday). A kingdom of chickens.
  // =====================================================================================================
  "home.lilroom.first.1": ["lilsis", "Rule one: don't step on the rug. The rug is an EGG."],
  "home.lilroom.first.2": ["bigsis", "I used to live in here. It has since been annexed by poultry."],

  "home.lilroom.window.mom": ["mom", "She thought the maple held up the moon. I never corrected her."],
  "home.lilroom.window.bigsis": ["bigsis", "The paper rooster in the window is in charge of the weather. I have been told his name. Twice."],
  "home.lilroom.window.lilsis": ["lilsis", "The tree taps on the glass to say hi. I always say hi back, so it doesn't feel silly."],
  "home.drawings.mom": ["mom", "She drew your father the biggest of any of us. He was more pleased than a grown man has any right to be."],   // PASS-19H1: shorter
  "home.drawings.bigsis": ["bigsis", "She gave the hen a long and elegant neck, and me none whatsoever. I have raised it with the artist."],   // PASS-19H1: shorter; one idea
  "home.drawings.lilsis": ["lilsis", "That's General Feathers on the roof, on lookout. Keep an eye on Daddy, General!"],   // PASS-19H1: emphasis; shorter

  // ---- the chickens. Every one has a name and a rank or a job; "Chickens KNOW." is said here for the first time
  "home.chart.mom": ["mom", "The General has a star by her name. I gather the Admiral is being terribly gracious about it, which is worse."],   // PASS-19H1: shorter
  "home.chart.bigsis": ["bigsis", "I know every name and every rank. She quizzes me at breakfast, without warning."],   // PASS-19H1: shorter
  "home.chart.lilsis": ["lilsis", "You go up a rank every time you go through the wash. That's the rule. The washing machine knows."],   // PASS-19H1: emphasis; shorter
  "home.flock.mom": ["mom", "Every one of them has been through my washing machine, and every one came out promoted."],
  "home.flock.bigsis": ["bigsis", "Admiral Doodle on top. Corporal Speckle. Private Peep. I know them all."],
  "home.flock.bigsis.b": ["bigsis", "Against my will."],
  "home.flock.lilsis": ["lilsis", "Admiral Doodle does the mornings. Tonight nobody's saying anything. Not even the Admiral."],
  "home.flock.lilsis2": ["lilsis", "They know something's up. They knew before I did. Chickens KNOW."],
  "home.teaparty.mom": ["mom", "I was invited to tea here last week, and told afterwards that my manners would do. I was very relieved."],   // PASS-19H1: shorter; punch last
  "home.teaparty.bigsis": ["bigsis", "The tea is water. The water is from Tuesday. I regret checking."],   // PASS-19H1: shorter
  "home.teaparty.lilsis": ["lilsis", "Nobody's allowed to drink till the General gets back. That's not a rule. It's MANNERS."],   // PASS-19H1: emphasis; shorter; one idea
  "home.coop.mom": ["mom", "It was a dollhouse. The dolls were asked to leave. I'm told it was amicable."],
  "home.coop.bigsis": ["bigsis", "I wired the hen house. I was told it was for dolls. I was misled."],
  "home.coop.lilsis": ["lilsis", "Everybody in my hen house is home. I checked. Twice."],
  "home.coop.flash": ["lilsis", "They didn't even blink at my flashlight. Brave hens."],
  // (Matthew 23:37. Those nine words, and no more of the verse, are quoted.)
  "home.nest.mom": ["mom", "'...even as a hen gathereth her chickens under her wings'..."],   // PASS-17H: reference aloud; the Bible fact tacked on
  "home.nest.mom2": ["mom", "Tonight I know just how the hen feels."],
  "home.nest.bigsis": ["bigsis", "A hen, sitting on plastic eggs since March. I admire her patience, if not her judgment."],
  "home.nest.lilsis": ["lilsis", "Henrietta's on the eggs. They're plastic, so it takes EXTRA long."],

  // ---- her bed, and the place kept on the pillow for General Feathers, who went on the trip in Daddy's suitcase
  "home.lilbed.mom": ["mom", "A bed that has been jumped on. Recently, and with conviction."],
  "home.lilbed.bigsis": ["bigsis", "Hens on top, non-hens ranked below. The non-hens were not consulted."],   // PASS-19H1: shorter; one idea
  "home.lilbed.lilsis": ["lilsis", "My bed is for the officers. And jumping."],   // PASS-19H1: shorter; punch last
  "home.pillow.mom": ["mom", "Her first draft of the note said 'DO WHAT SHE SAYS' twice."],
  "home.pillow.bigsis": ["bigsis", "'RESERVED.' For a hen with a medal. She outranks me."],
  "home.pillow.lilsis": ["lilsis", "General Feathers went in Daddy's suitcase, to keep an eye on him. That's her whole job."],
  "home.pillow.lilsis2": ["lilsis", "I'm not worried about the General. Daddy's the one who needs supervising."],
  "home.lamp.mom": ["mom", "She won't sleep without it. Nor, I suspect, would the rooster."],   // PASS-19H1: shorter; one idea
  "home.lamp.bigsis": ["bigsis", "She stood at the shop window for a week, saying nothing, until it was hers. I have never seen better negotiating."],   // PASS-19H1: shorter
  "home.lamp.lilsis": ["lilsis", "My rooster lamp stays up all night, so I don't have to. He never even goes to BED."],   // PASS-19H1: emphasis; shorter

  // ---- chain B: the blanket fort, and the flashlight in it, which is dead
  "home.fort.look.mom": ["mom", "Every blanket she owns, and a sign with very firm views. Her flashlight's just inside."],   // PASS-17H: American: drying rack
  "home.fort.look.bigsis": ["bigsis", "'NO BIG SISTERS.' There is only one of me."],
  "home.fort.look.lilsis": ["lilsis", "My fort has my flashlight and a secret. I'm not telling the secret."],
  "home.fort.empty.mom": ["mom", "Better built than your father's shelves. I haven't told either one."],   // PASS-17H: Mom's formality
  "home.fort.empty.bigsis": ["bigsis", "I have never once tried to go in. That is what makes it hurtful."],
  "home.fort.empty.lilsis": ["lilsis", "The secret's still in my fort. It's a cookie."],
  "home.fort.use.mom": ["mom", "Nobody goes into a lady's fort uninvited. I taught her that myself."],   // PASS-17H: Mom's formality ('One does not')
  "home.fort.use.bigsis": ["bigsis", "I respect a posted boundary. Also, I would not fit."],
  "home.flashlight.mom": ["mom", "That's hers to fetch, darling. Her fort, her rule, and a good one."],   // PASS-19H1: shorter
  "home.flashlight.bigsis": ["bigsis", "It is inside the sign's jurisdiction, and I am not reaching past it. Not even for a flashlight."],   // PASS-19H1: shorter
  "home.flashlight.lilsis": ["lilsis", "It lives in my fort, for the dark. That's when you NEED one."],   // PASS-19H1: emphasis; shorter; one idea
  "home.fort.take.dark": ["lilsis", "My flashlight! The closet can't be dark at me now. Click. ...Click?"],
  "home.fort.take.early": ["lilsis", "My flashlight, in case of dark. Click. ...Click?"],
  "home.fort.take.2": ["lilsis", "It's DEAD. I read to the flock all night. They wanted the whole book."],
  "home.fort.take.3": ["mom", "Then it wants batteries. I haven't seen that size since Easter."],   // PASS-17H: Mom's formality
  "home.fort.take.4": ["bigsis", "...There are four, in my sound machine. Let it be noted I said so."],
  "home.fort.again": ["lilsis", "I went in and out again. The cookie's okay."],
  "home.fort.putback.mom": ["mom", "Not yet, darling. Your sister will be wanting that."],
  "home.fort.putback.bigsis": ["bigsis", "I may not go near that fort. I shall hold this until relieved."],
  "home.fort.putback.lilsis": ["lilsis", "No! We NEED it. It can go home after."],
  "home.lilroom.door.mom": ["mom", "The landing. Lights off when we go, girls. ...No. Leave them on tonight."],
  "home.lilroom.door.bigsis": ["bigsis", "There is a hen on this side of the door as well. Of course there is."],
  "home.lilroom.door.lilsis": ["lilsis", "There's a hen on the door, so the door knows whose door it is."],

  // ---- what they say to each other in Little Sister's room
  "home.talk.lilroom.mom.bigsis.1a": ["mom", "How's the novel, darling?"],   // PASS-17H: Mom's formality
  "home.talk.lilroom.mom.bigsis.1b": ["bigsis", "It has acquired a plot this evening. I did not ask for one."],
  "home.talk.lilroom.mom.bigsis.2a": ["mom", "You shared this room with her once. Do you ever miss it, darling?"],
  "home.talk.lilroom.mom.bigsis.2b": ["bigsis", "I miss the window. I do not miss being counted at bedtime along with the flock."],
  "home.talk.lilroom.mom.lilsis.flash.a": ["mom", "Your flashlight's in your fort, sweetheart, and nobody goes into that fort but you."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.mom.lilsis.flash.b": ["lilsis", "I KNOW. I made the rule. I'm already getting it."],
  "home.talk.lilroom.mom.lilsis.1a": ["mom", "Did you say your verse tonight, sweetheart?"],
  "home.talk.lilroom.mom.lilsis.1b": ["lilsis", "Twice. Once for me and once for my brother. He forgets."],
  "home.talk.lilroom.mom.lilsis.2a": ["lilsis", "Mommy, can Daddy sleep in my fort when he's back?"],
  "home.talk.lilroom.mom.lilsis.2b": ["mom", "He'd be honored, my love. He also wouldn't fit. He'll try anyway."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.bigsis.mom.1a": ["bigsis", "Mom, did you ever want to be on a real stage? A big one, with a curtain that goes up?"],
  "home.talk.lilroom.bigsis.mom.1b": ["mom", "I'm on one every day, darling. And nobody ever knows their lines."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.bigsis.mom.2a": ["bigsis", "I have decided what the next chapter is called. 'Places, Girls.'"],
  "home.talk.lilroom.bigsis.mom.2b": ["mom", "I expect a credit."],   // PASS-17H: Mom's formality ('I should like'); funnier
  "home.talk.lilroom.bigsis.lilsis.1a": ["bigsis", "Which one is Corporal Speckle? I have forgotten."],
  "home.talk.lilroom.bigsis.lilsis.1b": ["lilsis", "You have NOT. You're being nice. ...It's the speckly one."],
  "home.talk.lilroom.bigsis.lilsis.2a": ["lilsis", "When I'm thirteen, do I get an attic?"],
  "home.talk.lilroom.bigsis.lilsis.2b": ["bigsis", "When you are thirteen I shall be nineteen, and you may have mine."],
  "home.talk.lilroom.bigsis.lilsis.2c": ["lilsis", "...I don't WANT yours. Yours has no chickens."],
  "home.talk.lilroom.lilsis.mom.1a": ["lilsis", "Mommy, look. I made my bed!"],
  "home.talk.lilroom.lilsis.mom.1b": ["mom", "You made A bed, darling. Out of every blanket we own."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.lilsis.mom.2a": ["lilsis", "Is it still today?"],
  "home.talk.lilroom.lilsis.mom.2b": ["mom", "It's still today, sweetheart. It's been today for a very long time."],   // PASS-17H: Mom's formality
  "home.talk.lilroom.lilsis.bigsis.1a": ["lilsis", "Do you want to hold a chicken? It helps."],
  "home.talk.lilroom.lilsis.bigsis.1b": ["bigsis", "...The speckled one. Briefly. For morale."],
  "home.talk.lilroom.lilsis.bigsis.2a": ["lilsis", "Is your book about us?"],
  "home.talk.lilroom.lilsis.bigsis.2b": ["bigsis", "It is about a family of five. Any resemblance is entirely the point."],

  // =====================================================================================================
  // THE RETREAT: Big Sister's attic. Soft light, one sound, three rules. (Up here Little Sister whispers at full volume.)
  // =====================================================================================================
  "home.retreat.first.1": ["lilsis", "Boots off. One. ...Two. Everybody see me doing the RULE."],
  "home.retreat.first.2": ["bigsis", "Rule two is voices down. You are whispering at full volume."],
  "home.retreat.first.3": ["lilsis", "THIS IS MY WHISPER."],
  "home.retreat.first.4": ["mom", "Darling, it's a set. It's a very good set. Let's all try to deserve it."],

  // ---- the rules, on their easel by the hatch (the close-up shows them, and what is written under the third in crayon)
  "home.rules.mom": ["mom", "Three rules, darling, and the third already under appeal. You girls have founded a republic."],   // PASS-19H1: shorter
  "home.rules.bigsis": ["bigsis", "Three rules, composed for a person of seven. The crayon underneath is not mine."],   // PASS-19H1: shorter
  "home.rules.lilsis": ["lilsis", "Rule three is NOT fair, so I lodged a appeal. It has a D for no reason."],   // PASS-19H1: emphasis; shorter; one idea

  // ---- Big Sister's timeline: where the game says how it counts the years, and what B.C. and A.D. mean.
  // Every year before Christ is the Bible's count, as Archbishop Ussher counted it (docs/CHARACTERS.md has the table).
  // The first time any of them looks along it, the three read it between them: .1 to .6, then .bigsis, .bigsis2, .mom, .lilsis.
  "home.timeline.1": ["bigsis", "I used Archbishop Ussher's dates. He counted from the Bible's own genealogies."],
  "home.timeline.2": ["mom", "A matter of record: the Archbishop's book, 1650. Now he's in felt pen."],
  "home.timeline.3": ["bigsis", "It begins at the left: 4004 B.C., the Creation. And here, 2348 B.C.: the Flood."],
  "home.timeline.4": ["lilsis", "Not much paper before Abram. I thought the beginning was the LONGEST bit."],
  "home.timeline.5": ["bigsis", "It is as long as it was. 1921 B.C.: Abram leaves Haran, goes down into Egypt."],
  "home.timeline.6": ["bigsis", "1491 B.C.: the Exodus. 44 B.C.: the Ides of March. Rome's, but on my wall."],
  "home.timeline.bigsis": ["bigsis", "At the red mark the years turn round. Before it: B.C., 'before Christ'."],
  "home.timeline.bigsis2": ["bigsis", "After it they count up: A.D. Anno Domini, Latin for 'in the year of the Lord'."],
  "home.timeline.mom": ["mom", "Every year on that wall is counted from His birth. I've always loved that."],   // PASS-17H: a faith line said as a mother says it
  "home.timeline.lilsis": ["lilsis", "I'm on it! At the end, in pencil. Everybody else gets PEN."],
  "home.timeline.bigsis3": ["bigsis", "A monk named Dionysius worked that count out in 525, from the birth of Jesus."],
  "home.timeline.bigsis4": ["bigsis", "Cristofori's piano. The Constitution. Sliced bread. And, in pencil, my sister."],
  "home.timeline.again.mom": ["mom", "From the Creation to your sister, on one strip. I'd hate to have ruled it."],   // PASS-17H: Mom's formality ('I should not like')
  "home.timeline.again.lilsis": ["lilsis", "I'm in pencil. When I do something big, she has to do me in PEN."],
  "home.timeline.pencil.mom": ["mom", "It's your sister's, darling. She does her own footnotes."],   // PASS-17H: Mom's formality ('One does not'); funnier
  "home.timeline.pencil.bigsis": ["bigsis", "Tonight goes on the timeline when I know what tonight was. And not in Dad's chewed pencil."],
  "home.timeline.pencil.lilsis": ["lilsis", "I drew a hen on it once, by the Flood. She's still there, very SMALL."],

  // ---- chain B: the sound machine, and the only batteries of that size in the house
  "home.sound.look.mom": ["mom", "One slow tune, in D major. Sensible girl. D major never panics."],   // PASS-17H: the speech that is really an essay; funnier
  "home.sound.look.bigsis": ["bigsis", "The only thing in this house that is calm on purpose."],
  "home.sound.look.lilsis": ["lilsis", "The music box runs on batteries. I'm WHISPERING."],
  "home.sound.use.mom": ["mom", "It's her room and her machine. I wouldn't dream of touching it without her say-so."],   // PASS-17H: Mom's formality ('One does not'); one darling fewer
  "home.sound.use.bigsis": ["bigsis", "It stays on. Tonight it is the only one of us that is calm, and nobody has yet given me a reason to stop it."],
  "home.sound.use.lilsis": ["lilsis", "I'm not allowed to touch anything up here. We signed a TREATY."],
  "home.sound.take.mom": ["mom", "They're not mine to take, darling. Your sister has to give them."],   // PASS-17H: Mom's formality
  "home.sound.take.lilsis": ["lilsis", "The batteries are in there. I can't touch it. So YOU have to."],
  "home.sound.give.1": ["bigsis", "The only batteries of that size in this whole house are in here. I knew this moment was coming."],
  "home.sound.give.2": ["bigsis", "Very well. The Retreat goes dark so that the internet may live."],
  "home.sound.give.3": ["lilsis", "It stopped. ...Now the water's going tick, tick, tick."],
  "home.sound.give.4": ["bigsis", "I shall be hearing that all night. I intend to mention this again."],
  "home.sound.give.5": ["mom", "You will, darling. And each time, I'll say thank you and mean it."],   // PASS-17H: Mom's formality ('shall')
  "home.sound.quiet.mom": ["mom", "She gave up her music for her sister. And only mentioned it twice."],   // PASS-17H: Mom's formality
  "home.sound.quiet.bigsis": ["bigsis", "Only the fountain is left now. It sounds exactly like a clock, which I had been managing not to notice."],
  "home.sound.quiet.lilsis": ["lilsis", "She took the batteries out for ME. I'm drawing her a chicken."],
  "home.sound.putback.mom": ["mom", "Darling, they have an appointment with a pink flashlight."],
  "home.sound.putback.bigsis": ["bigsis", "A sacrifice stays made. They go in my sister's flashlight."],
  "home.sound.putback.lilsis": ["lilsis", "They go in my FLASHLIGHT now. That's the whole point of them."],
  "home.soundtable.mom": ["mom", "Music at one end of the table and water at the other. Very well blocked. She gets that from me."],   // PASS-19H1: shorter
  "home.soundtable.bigsis": ["bigsis", "Exactly a hand's width apart. I measured. It matters, although I could not tell you why."],   // PASS-19H1: shorter; one idea
  "home.soundtable.lilsis": ["lilsis", "I'd put a chicken between the music and the water. She says no."],   // PASS-19H1: emphasis; shorter; one idea
  "home.fountain.mom": ["mom", "Not one drop on the floor. She's my daughter."],   // PASS-19H1: shorter
  "home.fountain.bigsis": ["bigsis", "It is meant to sound like a brook. Tonight it sounds like a clock."],   // PASS-19H1: shorter
  "home.fountain.lilsis": ["lilsis", "The fountain never stops. It makes me need to... never mind."],   // PASS-19H1: emphasis; second joke cut

  // ---- the rest of the Retreat
  "home.skylight.mom": ["mom", "She thinks under the stars. At her age, I had to go outside."],   // PASS-19H1: shorter
  "home.skylight.bigsis": ["bigsis", "I have counted the little lights along the rafters in fours. Twice. They are all still there."],   // PASS-19H1: shorter
  "home.skylight.lilsis": ["lilsis", "Her bed has the same moon as mine. I asked."],   // PASS-19H1: emphasis; shorter; one idea
  "home.retreat.window.mom": ["mom", "From the road, the house has one eye open. Tonight it really has."],
  "home.retreat.window.bigsis": ["bigsis", "It looks down the road. I have not been watching the road. Much."],
  "home.retreat.window.lilsis": ["lilsis", "A ROUND window. Her room's a boat and my room's a farm."],
  "home.plants.mom": ["mom", "Every plant alive, in an attic. I can't keep parsley."],   // PASS-19H1: shorter
  "home.plants.bigsis": ["bigsis", "Not one of these plants is worried about anything. I envy them, a little."],   // PASS-19H1: shorter
  "home.plants.lilsis": ["lilsis", "There's no animals in her jungle. I OFFERED her a chicken."],   // PASS-19H1: shorter; one idea
  "home.towels.mom": ["mom", "A robe. I didn't own a robe until I was married."],   // PASS-19H1: shorter
  "home.towels.bigsis": ["bigsis", "A folded towel is a towel. A rolled towel is a decision."],   // PASS-19H1: shorter
  "home.towels.lilsis": ["lilsis", "They look like cinnamon buns. They're NOT."],   // PASS-19H1: emphasis; one idea
  "home.saltlamp.mom": ["mom", "The light of one tired candle. She won't hear a word against it."],   // PASS-19H1: shorter
  "home.saltlamp.bigsis": ["bigsis", "It is said to be calming. I have written down my doubts."],   // PASS-19H1: shorter; one idea
  "home.saltlamp.lilsis": ["lilsis", "The orange rock is salt. I'm not allowed to lick the lamp."],   // PASS-19H1: emphasis; shorter
  "home.books.mom": ["mom", "She has read every one of them. Several were mine first, and I've quite given up hope of getting them back."],   // PASS-19H1: shorter; one idea
  "home.books.bigsis": ["bigsis", "The books go red to violet, but that is not the system. The system is in my head, and it stays there."],   // PASS-19H1: shorter; one idea
  "home.books.lilsis": ["lilsis", "The duck book's in the yellow. The duck has NO words."],   // PASS-19H1: emphasis; shorter
  "home.desk.mom": ["mom", "Her novel. I've been asked not to read it. In writing."],   // PASS-17H: Mom's formality
  "home.desk.bigsis": ["bigsis", "My novel, open at chapter nine. And my pencils: all slim, and all exactly the same length."],
  "home.desk.lilsis": ["lilsis", "I touched one pencil one time, and she KNEW."],
  "home.desk.pencil.mom": ["mom", "That's your father's pencil. Your sister's are a matched set."],   // PASS-17H: Mom's formality; one darling fewer
  "home.desk.pencil.bigsis": ["bigsis", "Dad's pencil does not go in my jar. My jar has standards."],
  "home.desk.pencil.lilsis": ["lilsis", "I put Daddy's pencil in her jar. Now she has to count them ALL."],
  "home.bedbig.mom": ["mom", "I didn't teach her hospital corners. I'm not sure anybody did."],   // PASS-19H1: shorter; one idea
  "home.bedbig.bigsis": ["bigsis", "I learned hospital corners from a book. A book about hospitals."],   // PASS-19H1: shorter; the 'second book' joke is the leaving's; one idea
  "home.bedbig.lilsis": ["lilsis", "I'm not allowed in her tent. I've been in it nine times."],   // PASS-19H1: emphasis; shorter
  "home.mat.mom": ["mom", "She stretches at dawn, in silence. The floorboards tell me."],   // PASS-19H1: shorter
  "home.mat.bigsis": ["bigsis", "In for four, out for four. Tonight I lose count at three."],   // PASS-19H1: shorter
  "home.mat.lilsis": ["lilsis", "I did three somersaults in my head. ...And one not in my head."],   // PASS-19H1: emphasis; shorter
  "home.hatch.mom": ["mom", "Mind the ladder, girls. Everything's steeper going down."],   // PASS-19H1: shorter; punch last; one idea
  "home.hatch.bigsis": ["bigsis", "Shoes on at the bottom. Outdoor voices may resume on the landing."],   // PASS-19H1: shorter
  "home.hatch.lilsis": ["lilsis", "I go down the ladder hole backwards. Like a bear."],   // PASS-19H1: emphasis; shorter

  // ---- what they say to each other in the Retreat
  "home.talk.retreat.mom.bigsis.key.a": ["mom", "D major, darling?"],
  "home.talk.retreat.mom.bigsis.key.b": ["bigsis", "D major. You always know. It is extremely annoying, Mother."],
  "home.talk.retreat.mom.bigsis.1a": ["mom", "You put the Constitution on your timeline. In ink."],   // PASS-17H: Mom's formality
  "home.talk.retreat.mom.bigsis.1b": ["bigsis", "You stood behind me until I did, Mother."],
  "home.talk.retreat.mom.bigsis.2a": ["mom", "It's a lovely room, darling. You made every inch of it yourself, and it shows."],   // PASS-17H: Mom's formality
  "home.talk.retreat.mom.bigsis.2b": ["bigsis", "On pocket money. I should like that in the program."],
  "home.talk.retreat.mom.lilsis.1a": ["mom", "Indoor voice, sweetheart."],
  "home.talk.retreat.mom.lilsis.1b": ["lilsis", "THIS IS MY INDOOR VOICE. IT'S FOR INDOORS IN A BARN."],
  "home.talk.retreat.mom.lilsis.2a": ["lilsis", "Can the General come up here? She's not a chicken. She's a GENERAL."],
  "home.talk.retreat.mom.lilsis.2b": ["mom", "That's for the court of appeal, darling. I only supplied the spelling."],   // PASS-17H: Mom's formality
  "home.talk.retreat.bigsis.mom.1a": ["bigsis", "It is calm up here, and I am not. It is inconsiderate of the room."],
  "home.talk.retreat.bigsis.mom.1b": ["mom", "The set is never nervous, darling. Only the cast."],   // PASS-17H: Mom's formality
  "home.talk.retreat.bigsis.mom.2a": ["bigsis", "I counted the lights again. In fours. It came out even."],
  "home.talk.retreat.bigsis.mom.2b": ["mom", "And did it help?"],
  "home.talk.retreat.bigsis.mom.2c": ["bigsis", "No. But it came out even."],
  "home.talk.retreat.bigsis.lilsis.1a": ["bigsis", "Visiting hours end when the big hand reaches the twelve."],
  "home.talk.retreat.bigsis.lilsis.1b": ["lilsis", "Which twelve? There's one every hour. I'll have the LAST one."],
  "home.talk.retreat.bigsis.lilsis.2a": ["bigsis", "You may stay if you can be silent for one whole minute."],
  "home.talk.retreat.bigsis.lilsis.2b": ["lilsis", "Okay. ...Is it a minute? ...Now? ...I was silent in BETWEEN."],
  "home.talk.retreat.lilsis.mom.1a": ["lilsis", "Mommy, why can't chickens come up here?"],
  "home.talk.retreat.lilsis.mom.1b": ["mom", "It's your sister's room. Three rules. You have eleven."],   // PASS-17H: Mom's formality; one darling fewer
  "home.talk.retreat.lilsis.mom.2a": ["lilsis", "It smells like a flower shop up here. And a bit like a library."],
  "home.talk.retreat.lilsis.mom.2b": ["mom", "That's your sister, darling. Precisely."],   // PASS-17H: Mom's formality
  "home.talk.retreat.lilsis.bigsis.1a": ["lilsis", "Can I come up when it isn't visiting hours? Just my toe?"],
  "home.talk.retreat.lilsis.bigsis.1b": ["bigsis", "...One toe. For morale."],
  "home.talk.retreat.lilsis.bigsis.2a": ["lilsis", "Are you scared?"],
  "home.talk.retreat.lilsis.bigsis.2b": ["bigsis", "No. ...A little. Do not tell the room."],
  "home.talk.retreat.lilsis.bigsis.2c": ["lilsis", "I'll hold your hand, then. Not for me. For the ROOM."],

  // =====================================================================================================
  // IN ANY ROOM
  // =====================================================================================================
  // ---- what the one who is handed something says
  "home.give.studykey.mom": ["mom", "Thank you, darling. I'll do the honors."],   // PASS-17H: Mom's formality ('shall')
  "home.give.studykey.bigsis": ["bigsis", "Trip Headquarters. I accept the responsibility, and the tag."],   // PASS-19H1: shorter; one idea
  "home.give.studykey.lilsis": ["lilsis", "The key! I'm the key person, in CHARGE of the door."],   // PASS-19H1: emphasis; one idea
  "home.give.lilflash.mom": ["mom", "I'll keep it safe for you, sweetheart. You'll be wanting it for the closet under the stairs."],   // PASS-19H1: shorter
  "home.give.lilflash.bigsis": ["bigsis", "It is pink and slightly sticky, and I am holding it under protest. For her sake."],   // PASS-19H1: shorter
  "home.give.lilflash.lilsis": ["lilsis", "Hi, flashlight. You like ME best."],   // PASS-19H1: emphasis; shorter; one idea
  "home.give.batteries.mom": ["mom", "I'll hold them like a borrowed prop: carefully, not for long."],   // PASS-19H1: shorter
  "home.give.batteries.bigsis": ["bigsis", "They are not going back in the machine, so please do not ask me. A sacrifice, once made, stays made."],   // PASS-19H1: shorter
  "home.give.batteries.lilsis": ["lilsis", "Somebody else has my flashlight. They need to MEET."],   // PASS-19H1: emphasis; shorter
  // ---- batteries and flashlight in one pair of hands: whoever that is puts them in
  "home.flash.load.mom": ["mom", "In they go: a small pink spotlight. She'll want it back at once."],   // PASS-19H1: shorter; one idea
  "home.flash.load.bigsis": ["bigsis", "It lights. The Retreat did not go dark for nothing."],   // PASS-19H1: shorter
  "home.flash.load.lilsis": ["lilsis", "Click. ...It WORKS! Now the closet can't be dark at me."],   // PASS-19H1: emphasis; shorter
  // ---- her flashlight, shined at something while there is nothing in it
  "home.flash.dead": ["lilsis", "Click. Nothing. It needs batteries."],
  "home.give.pencil.mom": ["mom", "Your father's pencil, thoroughly chewed. That'll do nicely."],   // PASS-19H1: shorter
  "home.give.pencil.bigsis": ["bigsis", "I know exactly what Dad's pencil fits. I do not know how to do it. Mom does."],   // PASS-19H1: shorter; one idea
  "home.give.pencil.lilsis": ["lilsis", "I'll just hold Daddy's pencil and not fix anything. Probably."],   // PASS-19H1: emphasis; one idea
  "home.give.carkey.mom": ["mom", "Thank you. I am, after all, the only one with a license."],   // PASS-19H1: shorter
  "home.give.carkey.bigsis": ["bigsis", "I am thirteen and holding the car key. I am not driving. Yet."],   // PASS-19H1: shorter; one idea
  "home.give.carkey.lilsis": ["lilsis", "I call the front seat. I CALLED it. It's called."],   // PASS-19H1: emphasis

  // ---- carried things
  "item.note.mom": ["mom", "'The year of the best thing since.' Your sister knows the year of everything."],   // PASS-19H1: shorter; one idea
  "item.note.bigsis": ["bigsis", "Sliced bread, 1928. I am keeping this. It is a primary source."],
  "item.note.lilsis": ["lilsis", "Words. I'll give it to somebody who reads books with NO pictures."],
  "item.studykey.mom": ["mom", "The study key, tag and all. It smells faintly of piano."],   // PASS-19H1: shorter; one idea
  "item.studykey.bigsis": ["bigsis", "One brass key, formerly of the piano. Technically, the eighty-ninth."],   // PASS-19H1: shorter
  "item.studykey.lilsis": ["lilsis", "I got Daddy's key out of the piano. Me, with my arm."],   // PASS-19H1: emphasis; one idea
  "item.lilflash.mom": ["mom", "Pink, chunky and much loved. Hers to carry into the dark."],   // PASS-19H1: shorter
  "item.lilflash.bigsis": ["bigsis", "The button is sticky. I am not going to ask."],   // PASS-19H1: shorter; one idea
  "item.lilflash.lilsis": ["lilsis", "My flashlight. It only works when its batteries work."],   // PASS-19H1: emphasis; shorter
  "item.batteries.mom": ["mom", "They want a pink flashlight, and then they want to go home."],   // PASS-19H1: shorter
  "item.batteries.bigsis": ["bigsis", "Four double-As for her flashlight, and the Retreat is silent. I am fine."],   // PASS-19H1: shorter; one idea
  "item.batteries.lilsis": ["lilsis", "In my flashlight, then the closet. That's the WHOLE plan."],   // PASS-19H1: emphasis; shorter; one idea
  "item.pencil.mom": ["mom", "I've wound a great many cassettes with a pencil like this one. Musicals, mostly."],   // PASS-19H1: shorter
  "item.pencil.bigsis": ["bigsis", "You can wind a cassette with a pencil. Doing it is another matter."],   // PASS-19H1: 'Fun fact' rationed; shorter
  "item.pencil.lilsis": ["lilsis", "It's bitey at the end. That's where the thinking goes in."],   // PASS-19H1: shorter; one idea
  "item.carkey.mom": ["mom", "Two years in a cash box with the ketchup. It's earned a drive."],   // PASS-19H1: shorter
  "item.carkey.bigsis": ["bigsis", "Mom's spare car key. Liberated by the Constitution."],   // PASS-19H1: shorter; punch last
  "item.carkey.lilsis": ["lilsis", "Mommy does the driving. I do the BEEP."],   // PASS-19H1: emphasis; shorter; one idea

  // =====================================================================================================
  // HINTS: one from each of them for every puzzle. The one whose job it is says what to try; the others say whose job it is.
  // =====================================================================================================
  "hint.home.riddle.mom": ["mom", "Your father has locked his study, darlings, and taped a notice to the door. Let's go up and read it."],
  "hint.home.riddle.bigsis": ["bigsis", "The study is locked, and Dad left a notice on its door upstairs. It reads like a riddle, which means it is one."],
  "hint.home.riddle.lilsis": ["lilsis", "Daddy's door upstairs has a sign on it with SO many words. Words are my sister's favorite."],
  "hint.home.key.lilsis": ["lilsis", "The key's inside the piano, past the little wall by the pedals. My arm fits in there. Nobody else's does."],   // PASS-19H1: shorter (its words stay); one idea
  "hint.home.key.mom": ["mom", "The key's somewhere inside my piano, and my arms won't reach it. It wants someone small and brave."],   // PASS-19H1: shorter (its words stay); one idea
  "hint.home.key.bigsis": ["bigsis", "The key is lying on the hammers. My arm does not go inside a piano, ever. My sister fits, and knows it."],   // PASS-19H1: shorter (its words stay); one idea
  "hint.home.study.mom": ["mom", "We have the key to his study now. Whoever has it, darling, should try the door upstairs."],
  "hint.home.study.bigsis": ["bigsis", "One of us has the study key. Its door is upstairs, at the end of the landing."],
  "hint.home.study.lilsis": ["lilsis", "We got the KEY. Whoever's got it, put it in Daddy's door upstairs."],
  "hint.home.batteries.lilsis": ["lilsis", "The closet's too dark. I need my flashlight from my fort, and if it's dead, the music box has batteries."],
  "hint.home.batteries.bigsis": ["bigsis", "Her flashlight is of no use dead. The only batteries that size live in my sound machine, in the Retreat."],
  "hint.home.batteries.mom": ["mom", "No light, no closet, darling. A dead flashlight wants batteries, and your sister's sound machine has them."],
  "hint.home.router.lilsis": ["lilsis", "My flashlight WORKS! The internet's in the closet under the stairs. I fit."],
  "hint.home.router.mom": ["mom", "The router lives in the closet under the stairs. Her flashlight works now, so that's her cue."],   // PASS-17H: Mom's formality
  "hint.home.router.bigsis": ["bigsis", "The flashlight works; I paid for that in music. Now the router, in the closet under the stairs. That is hers."],
  "hint.home.note.bigsis": ["bigsis", "Dad always writes his passwords down, and never plainly. There is a yellow note on the monitor."],
  "hint.home.note.mom": ["mom", "Your father left a note on the monitor, darling: a riddle about a year. That's your sister's department."],   // PASS-17H: Mom's formality
  "hint.home.note.lilsis": ["lilsis", "There's a yellow sticky on Daddy's computer. It's all words, so it's for my sister."],
  "hint.home.login.mom": ["mom", "We have the internet back, and the password. I'll sit down at your father's computer myself."],   // PASS-17H: Mom's formality
  "hint.home.login.bigsis": ["bigsis", "The router is on and the password is 1928. After that, the computer asks about Mom's wedding. That is hers."],
  "hint.home.login.lilsis": ["lilsis", "I fixed the internet. My sister did the number. Now Mommy does the typing."],
  "hint.home.tape.mom": ["mom", "The answering machine spilled its tape. I'll wind it back in with your father's crossword pencil."],
  "hint.home.tape.bigsis": ["bigsis", "The tape wants winding back in with Dad's crossword pencil. Mom has the knack; I have only the theory."],
  "hint.home.tape.lilsis": ["lilsis", "The tape machine's tape fell out. NOT my fault this time. Mommy needs a pencil to wind it."],
  "hint.home.message.mom": ["mom", "The tape is wound, and there's one new message waiting on your father's machine. Let's hear it."],   // PASS-17H: Mom's formality
  "hint.home.message.bigsis": ["bigsis", "The tape is back in its cassette, and there is one new message on Dad's machine. We should play it."],
  "hint.home.message.lilsis": ["lilsis", "The tape's fixed and I didn't even do it. Press PLAY on the blinky machine."],
  "hint.home.vault.mom": ["mom", "Your father's vault wants the 'We the People' year, darlings. It's framed on our living-room wall."],   // PASS-17H: Mom's formality
  "hint.home.vault.bigsis": ["bigsis", "Dad's 'family vault' has the spare car key in it. The combination is a year Mom knows by heart."],
  "hint.home.vault.lilsis": ["lilsis", "Daddy's vault box has a clicky wheel. Mommy knows the 'We the People' number."],
  "hint.home.leave.mom": ["mom", "We know where that phone was last seen, girls. All that's left is the front door."],
  "hint.home.leave.bigsis": ["bigsis", "We have a location. The logical next step is the front door."],
  "hint.home.leave.lilsis": ["lilsis", "We found the dot! Let's go, the front door's right THERE."],   // PASS-19H1: emphasis; one idea
};
