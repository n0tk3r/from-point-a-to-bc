// Act Two: Rome, the Ides of March, 44 B.C. Every line the three Rome scenes use, the hints for the act's beats,
// and what is said on looking at the eight things the Son carries.
//   "line.id": ["who", "What they say."]
//
// Seventeen of these were in the game before the act was written, and are word for word as they were:
//   rome.arrive.1, rome.arrive.2, rome.arrive.3, rome.temple.look, rome.fountain.look, rome.fountain.take,
//   rome.fountain.again, rome.hole.look, rome.hole.use, rome.hole.coin, rome.hole.coin2, hint.rome.coin,
//   hint.rome.toss, item.coin.look, and (spoken in Act Four, not here) item.coin.mom, item.coin.bigsis,
//   item.coin.lilsis. Each is marked "kept" below. They are the standard for the Son's voice.
//   The act's check script (check-rome.mjs) holds them, and says so if one is changed.
//
// Speakers: son, the seven Romans (doorkeeper, soothsayer, senator, keeper, washer, urchin, clerk), and the date
// seller, a Jew from Judea who lives in Rome. The Son has a name for each of the Romans: the door guy, the chicken
// man, the snack guy, the laundry lady, the counting guy, and Walnut. The date seller he calls "mister".
// Nobody of the time ever uses a modern word; he never stops. (ROME-13W: and since round thirteen, the seven people of
// the bigger Rome: see "THE BIGGER ROME" below.)
//
// THE FAMILY'S FAITH, AND THE BIBLE'S HISTORY AS HISTORY (briefs/WEAVE.md). The Son is ten and has been to Sunday
// school all his life. Fifty-five lines carry it, each marked "woven" where its group begins:
//   - Scripture is quoted twice, word for word from the King James Version (the texts are in briefs/out/facts-home.md):
//     Micah 5:2, its first clause (rome.dateseller.ans.pray.2), and Numbers 6:24 (rome.dateseller.bless.1). Each ends
//     on the King James mark, a comma and a colon, because each verse runs on. Do not "tidy" them. (ROME-13W: five times
//     since round thirteen; the other three are across the river, in "THE BIGGER ROME" below.)
//   - Everything else from the Bible is the Son telling it in his own words: the tribute money (Matthew 22:17-21),
//     Caesar Augustus (Luke 2:1), the angels (Luke 2:9-14), Paul's road into Rome (Acts 28:15), Jericho (Joshua 6:20).
//   - "Not yet." is his tag for all of it, and it is said three times in the act and no more: at the fountain, to
//     the senator, and on a second look at the stepping stones. The check script counts them.
//   - He never says "early" about it: that word is Little Sister's, in Act Four.
//
// THE CHICKENS, AND THE YEARS (briefs/DATING.md, the author's two rules; briefs/WEAVE-2.md). Chickens are the thread
// through every era: a chicken notices a door in time before any person does. Four lines carry it here, each marked
// "chickens": the soothsayer's birds will not touch their grain, and he takes it for the worst of omens
// (rome.soothsayer.ans.birds.omen); they all stand facing the temple doors, and the boy notices it himself and thinks
// of his little sister, whose chicken is General Feathers and who says "Chickens KNOW." (rome.birdcage.doors.1, .2);
// and the date seller will not have his fortune told by hens (rome.dateseller.breakfast). Nobody explains it.
// The years: Rome's own date, 44 B.C., is the same in every count. No line here counts the years back to Egypt or to
// anything else before Christ; a year B.C. said in this act must be one of the Bible's count in DATING.md (the check
// script holds it).
//
// ROME-13W: THE BIGGER ROME (round thirteen: briefs/ROME-13.md and WRITE-13R.md; the design is briefs/out/rome2-design.md).
// Three new places, each with its own part below: the Forum (rome-forum), the Capitol (rome-capitol) and across the
// Tiber (rome-tiber). Three new puzzles, one in each of the act's chains: Nobody Will Show Him (A: the Gaul has the
// senator's toga), Juno's Geese (B: the keeper's boy and the breakfast, held on a statue's base by the sacred geese),
// and Interest Is Extra Wishes (C: the coin was Phyllis's wish, and he asks before he throws it away). And the heart of
// the faith thread, across the river: Eleazar, who prays toward Jerusalem and waits for the one God has promised.
// Seven new speakers, each with a name from the Son: gaul (Gaius Iulius Litumarus, a Gaul of Nemausus made a senator:
// "Big Senator"), phyllis (Fannia Phyllis, a Greek freedwoman who sells garlands: "the flower lady"), titus (the keeper's
// boy), anser (Titus Rubrius Anser, who feeds Juno's geese: "Mister Goose"), eleazar (the date seller's father-in-law,
// carried to Rome a captive nineteen years ago: "mister", then "Mister Eleazar"), mariam (his granddaughter, who keeps
// hens) and felix (Phyllis's son, a boatman bound for Corinth). Their talk is dialogue trees (js/content/talk/rome.js):
// the lines a tree says are here, each person's together, and the Son's choices in it are `rome.<who>.opt.<x>`.
// The old three places change only where ROME-13.md says ("What changes in the act as built"), each change marked
// ROME-13W where it stands; the writer's ids.md for the round (with its working papers) has every changed line's old
// words beside its new.
//   - Scripture is quoted five times now, all in the act's two quiet scenes, King James Version, exact (PASS-17R: and no
//     reference is said aloud since round seventeen: see below): the date seller's two, and across the river Isaiah 40:31 to its semicolon (rome.eleazar.heart.2),
//     Numbers 6:25 (rome.eleazar.bless.1) and Numbers 6:26 (rome.eleazar.last.son). So the priestly blessing goes three
//     ways: verse 24 from the date seller, 25 from his father-in-law, 26 from the boy. Everything else from the Bible is
//     told in a speaker's own words: Daniel 6:10, Psalm 55:17 and 122:6, Isaiah 9:7, 32:1 and 60:3, Numbers 15:38-39,
//     Deuteronomy 6:9, Acts 18:1-3 (and Luke 2:25, Simeon, whom the Son thinks of and does not name to the old man).
//   - "Not yet." is still said three times, and no new line uses it. "Chickens KNOW." is still said once, at the cage;
//     across the river Mariam's hens have their own words (four lines of the thread, marked "chickens"). "Early": never.
//   - Nobody knows what will happen in Pompey's hall today, and no line looks ahead to it: the Gaul goes to an ordinary
//     meeting. No year B.C. is named but 44; Rome's past is "long ago", "nineteen years ago", "a hundred years". The verses
//     the city sings about the Gauls are never quoted: the Gaul tells of them himself, in his own words.
//   - The Son wears no cap: his strange shoes and his hair are what the people of Rome notice.
//
// PASS-17R: THE DIALOGUE PASS (round seventeen: briefs/OFFICE-17.md, PASS-17.md; the design is
// briefs/out/office-hq-design.md, section 1). The author's rule of 16 October: chapter and verse are said aloud only
// when natural. Big Sister may cite one (she is not in this act); nobody else says a reference. So the Son no longer
// says "Micah 5:2!", "Numbers 6:24!", "Isaiah 40:31!", "Numbers 6:25!", "Numbers 6:26." or "Luke 2:1.": he says where
// he knows the words from (the Christmas program, the end of church, the fridge). The five quotations are King James,
// exact, as they were, and every reference is still in docs/CHARACTERS.md, "Scripture quoted in the game", and in
// docs/PUZZLES-rome.md. No Bible fact is tacked onto a look (the fig tree; the stepping stones); a few lines are truer
// to the picture (he wears no hat), shorter, or answer back. Each changed line is marked PASS-17R where it stands; the
// round's record (S/work-17-passR/changes.json) has every one's old words beside its new.

export const lines = {
  // ================= rome-steps: the steps of the temple =================

  // ---------- arrival ----------
  "rome.arrive.out": ["doorkeeper", "And stay out. The treasury of the Roman People is not a nursery."],
  "rome.arrive.1": ["son", "Dad? ... This is NOT the rest stop. The rest stop had a vending machine."],                  // kept
  "rome.arrive.2": ["son", "Everyone here is wearing a bedsheet. Ten out of ten. Biggest sleepover in history."],        // kept
  "rome.arrive.5": ["son", "The big guy carried me out by my backpack. I'm carry-on."],
  "rome.arrive.3": ["son", "Okay. Operation Find Dad. Step one: snacks. Step two: also Dad."],                           // kept
  "rome.arrive.7": ["son", "Step one's past that bush. My nose is never wrong."],

  // ---------- the temple front, the doors, the doorkeeper ----------
  "rome.temple.look": ["son", "Giant stripy pillars. Dad would say they're holding up well. Seven out of ten. Would climb."],   // kept
  "rome.temple.use": ["son", "Would climb. Won't. The door guy throws farther than fourteen steps."],
  "rome.doors.look": ["son", "Giant doors, wide open, and I'm still locked out."],
  "rome.doors.look2": ["son", "Wide open, and this time for me. I'm basically staff."],
  "rome.stairs.look": ["son", "Fourteen steps. I counted them on the way down. Upside down."],

  "rome.doorkeeper.look": ["son", "A door with arms, guarding a door. That's cheating."],
  "rome.doorkeeper.look2": ["son", "He hasn't blinked since he dropped me. Not that I'm counting. Ninety-one."],
  "rome.doorkeeper.hi.1": ["son", "Me again. I left a door in there. A hummy one. Can I get it?"],
  "rome.doorkeeper.hi.2": ["doorkeeper", "No."],
  "rome.doorkeeper.hi.3": ["son", "Do ANY kids get to go in?"],
  "rome.doorkeeper.rule.2": ["doorkeeper", "A boy who serves the rites. In a clean tunic. With something for the god."],
  "rome.doorkeeper.rule.3": ["doorkeeper", "You are a boy. That is one out of three."],
  "rome.doorkeeper.rule.4": ["son", "He gives scores. Out of THREE. Weird system."],
  "rome.doorkeeper.ask.rule": ["son", "What were the three things again?"],
  "rome.doorkeeper.ans.rule": ["doorkeeper", "A boy. A clean tunic. Something in his hands for the god. I will not sing it."],
  "rome.doorkeeper.ask.what": ["son", "What's in there, anyway?"],
  "rome.doorkeeper.ans.what.1": ["doorkeeper", "The god Saturn. And at his feet, the treasury of the Roman People."],
  "rome.doorkeeper.ans.what.2": ["son", "A church AND a bank. Dad would call that one-stop shopping."],
  "rome.doorkeeper.ask.dad": ["son", "Seen my dad? Tall, little beard, flowers on his shirt?"],
  "rome.doorkeeper.ans.dad.1": ["doorkeeper", "No."],
  "rome.doorkeeper.ans.dad.2": ["son", "Maybe he's asking for directions. ...No. He'd NEVER."],
  "rome.doorkeeper.ans.dad.3": ["doorkeeper", "Then he is lost."],
  "rome.doorkeeper.ans.dad.4": ["son", "He's not lost. He's making good time. Somewhere."],
  "rome.doorkeeper.ask.bye": ["son", "Don't go anywhere."],
  "rome.doorkeeper.ans.bye": ["doorkeeper", "I never do."],
  "rome.doorkeeper.need.both": ["doorkeeper", "One out of three. I am not a difficult man. I am an exact one."],
  "rome.doorkeeper.need.gift.1": ["doorkeeper", "A clean tunic. Good. And for the god, two empty hands. Two out of three."],
  "rome.doorkeeper.need.gift.2": ["son", "My score went UP. I'm improving!"],
  "rome.doorkeeper.need.tunic.1": ["doorkeeper", "Incense. Good. Carried by a boy in I do not know what. Two out of three."],
  "rome.doorkeeper.need.tunic.2": ["son", "It's a hoodie. It's from the future. It was on sale."],
  "rome.doorkeeper.again": ["doorkeeper", "You again. In. Touch nothing again."],
  "rome.doorkeeper.toga": ["doorkeeper", "A senator's toga. Senators are down there. I am up here. We both prefer it."],
  "rome.doorkeeper.breakfast.1": ["doorkeeper", "I do not eat at the door. ...Is that the sausage from the fountain street?"],
  "rome.doorkeeper.breakfast.2": ["son", "It's the chicken man's."],
  "rome.doorkeeper.breakfast.3": ["doorkeeper", "Then it is the chicken man's."],
  "rome.doorkeeper.coin": ["doorkeeper", "One coin. For the treasury. It has others."],
  "rome.doorkeeper.quarter": ["doorkeeper", "That is not a coin. Put it away before I have to find out what it is."],
  "rome.doorkeeper.phone": ["doorkeeper", "A small black door. It is shut. I approve."],
  // ROME-13W: the two new things carried, shown to him (the Gaul's toga, Phyllis's lamp)
  "rome.doorkeeper.gaultoga": ["doorkeeper", "That is not a toga. That is a large mistake. Take it off my steps."],
  "rome.doorkeeper.lamp": ["doorkeeper", "Unlit. Good. Nothing burns at this door that I did not light."],

  // the gate: in the tunic, with the incense
  "rome.gate.1": ["son", "Tunic on. Over the hoodie. And the backpack. I'm a lumpy Roman."],
  "rome.gate.2": ["son", "One boy. One clean tunic. One box of holy smell for the god."],
  "rome.gate.3": ["doorkeeper", "...Three out of three."],
  "rome.gate.4": ["son", "YES."],
  "rome.gate.5": ["doorkeeper", "The hair."],
  "rome.gate.6": ["son", "It doesn't go down. I've tried. Mom's tried. Gravity's tried."],
  "rome.gate.7": ["doorkeeper", "...Go in. Walk. Touch nothing. The clerk is counting."],
  "rome.gate.8": ["son", "Walking. Touching nothing. Mostly."],

  // ---------- the soothsayer and his sacred chickens ----------
  "rome.soothsayer.look": ["son", "An old guy with pet chickens. He looks like he read the last page first."],
  "rome.soothsayer.look2": ["son", "He keeps sighing at the steps. Steps never care."],
  "rome.soothsayer.hi.1": ["soothsayer", "Beware the Ides of March."],
  "rome.soothsayer.hi.2": ["son", "Which one is Ides?"],
  "rome.soothsayer.hi.3": ["soothsayer", "Today."],
  "rome.soothsayer.hi.4": ["son", "Then it's a bit late to be-ware."],
  "rome.soothsayer.hi.5": ["soothsayer", "I said it in February, too. Nobody listened then, either."],
  "rome.soothsayer.ask.birds": ["son", "Why do you keep chickens in a cage?"],
  "rome.soothsayer.ans.birds.1": ["soothsayer", "They are sacred. When they feed, the day is good. Today, not one grain."],
  // chickens: he takes it for the worst of omens, which for a man selling omens on the Ides of March it is. (The id gives him a hand across his brow.)
  "rome.soothsayer.ans.birds.omen": ["soothsayer", "The worst omen, on the Ides. I sell omens. This one I could not give away."],
  "rome.soothsayer.ans.birds.2": ["son", "Maybe they're just not breakfast chickens."],
  "rome.soothsayer.ans.birds.3": ["soothsayer", "Nor am I. My bread and sausage come from the cookshop by the fountain."],
  "rome.soothsayer.ans.birds.4": ["soothsayer", "I foresaw it. It did not help."],
  "rome.soothsayer.ans.birds.fed": ["soothsayer", "They feed. Look at them. I have decided not to ask them why."],
  "rome.soothsayer.ask.temple": ["son", "Can you get me into the temple?"],
  "rome.soothsayer.ans.temple.1": ["soothsayer", "I cannot get myself in. My incense for Saturn should have gone in at dawn."],
  "rome.soothsayer.ans.temple.2": ["soothsayer", "There are fourteen steps between it and him. My knees have foreseen every one."],
  "rome.soothsayer.ans.temple.3": ["son", "I could carry it! I'm great at steps."],
  "rome.soothsayer.ans.temple.4": ["soothsayer", "Not today. The birds will not feed, and I have no breakfast to tempt them."],
  "rome.soothsayer.ans.temple.fed": ["soothsayer", "Do not drop it. I have not foreseen you dropping it. That is something."],
  "rome.soothsayer.ask.future": ["son", "Can you tell MY future?"],
  "rome.soothsayer.ans.future.1": ["soothsayer", "Your hand. ...A long road. You will be very late for supper."],
  "rome.soothsayer.ans.future.2": ["son", "He's GOOD."],
  "rome.soothsayer.ans.future.3": ["son", "Do I find my dad?"],
  "rome.soothsayer.ans.future.4": ["soothsayer", "The birds do not say. Boys who look, find. That is not prophecy. That is boys."],
  "rome.soothsayer.ask.bye": ["son", "Happy Ides!"],
  "rome.soothsayer.ans.bye": ["soothsayer", "It is not that kind of day."],
  "rome.soothsayer.fed.1": ["son", "Breakfast! From the snack guy. He says you owe him for eleven years."],
  "rome.soothsayer.fed.2": ["soothsayer", "I foresaw this sausage. The first good thing I have foreseen all year."],
  "rome.soothsayer.fed.3": ["soothsayer", "A few crumbs for the birds. ...They feed. Look at them feed."],
  "rome.soothsayer.fed.3.b": ["son", "See? Breakfast chickens."],  // PASS-19R1: new, after rome.soothsayer.fed.3
  "rome.soothsayer.fed.5": ["soothsayer", "Take this incense in to the god. My knees send their regards."],
  "rome.soothsayer.fed.6": ["son", "First a sausage, now holy smell. I'm a delivery truck."],
  // ROME-13W: said in place of rome.soothsayer.fed.1 (as the choice and as the line) when the breakfast came down the hill
  // from Titus: the keeper no longer hands it over, so "From the snack guy" would not be true.
  "rome.soothsayer.fed.geese": ["son", "Breakfast! It's been up a hill and past some geese."],
  "rome.soothsayer.toga": ["soothsayer", "Not mine. Mine has known soup. That one has a future."],
  "rome.soothsayer.coin.1": ["soothsayer", "It is wet. I foresee that it came from a fountain."],
  "rome.soothsayer.coin.2": ["son", "WHOA. How did you..."],
  "rome.soothsayer.coin.3": ["soothsayer", "It is dripping on my foot."],
  "rome.soothsayer.quarter": ["soothsayer", "A man with his hair tied back. I do not know this omen. I dislike that."],
  "rome.soothsayer.incense": ["soothsayer", "It goes UP the steps, boy. That is the whole of the favor."],
  // ROME-13W: the two new things carried, shown to him
  "rome.soothsayer.gaultoga": ["soothsayer", "That toga has a Gaul in its future. A large one."],
  "rome.soothsayer.lamp": ["soothsayer", "A lamp for a journey. A long one, over water. Not yours, I think."],

  "rome.birdcage.look": ["son", "Chickens in a cage. They've got the look Mom gets when Dad says 'shortcut'."],
  "rome.birdcage.look2": ["son", "Sacred chickens. I asked one what makes it sacred. No comment."],
  "rome.birdcage.use": ["son", "Here, chick chick. ...Nothing. They know I've got no snacks."],
  // chickens: they all stand facing the temple doors, where the door in time is. He notices it himself (the first time he
  // calls them, or the second time he looks, fed or not), and thinks of his little sister. He does not explain it.
  // (The ids give him a point up the steps, then both arms up for the General.)
  "rome.birdcage.doors.1": ["son", "...They're all facing the temple doors. Every one. Chickens KNOW."],
  "rome.birdcage.doors.2": ["son", "My little sister says that. Her chicken, General Feathers, outranks me."],
  "rome.birdcage.fed": ["son", "Now they're eating like it's a contest. Good omen. For something."],
  "rome.birdcage.breakfast": ["son", "It's the old guy's breakfast. If I feed his chickens, he'll foresee it."],

  // ---------- the senator ----------
  "rome.senator.look": ["son", "A man in a giant bedsheet, standing still in a hurry. Like Dad at red lights."],
  "rome.senator.look2": ["son", "Purple stripe, red shoes, pink face. He's a whole box of crayons."],
  "rome.senator.hi.1": ["senator", "Boy. Do you know who I am?"],
  "rome.senator.hi.2": ["son", "No. Do you know who I am?"],
  "rome.senator.hi.3": ["senator", "...No."],
  "rome.senator.hi.4": ["son", "Then we're tied."],
  "rome.senator.hi.5": ["senator", "I am a senator of Rome, I am LATE, and my clean toga is at the laundry."],
  "rome.senator.ask.late": ["son", "Late for what?"],
  "rome.senator.ans.late.1": ["senator", "The Senate meets today, in the hall beside Pompey's theater. I have a speech."],
  "rome.senator.ans.late.2": ["senator", "It is about drains. It is magnificent."],
  "rome.senator.ans.late.3": ["son", "How long is it?"],
  "rome.senator.ans.late.4": ["senator", "It ends when they agree with me."],
  "rome.senator.ask.toga": ["son", "You're already wearing a bedsheet. A really big one."],
  "rome.senator.ans.toga.1": ["senator", "This is YESTERDAY'S toga. It has an olive stain. Here."],
  "rome.senator.ans.toga.2": ["son", "I can't even see it."],
  "rome.senator.ans.toga.3": ["senator", "The Senate would. Finding the stain on another man is most of what we do."],
  "rome.senator.ans.toga.4": ["senator", "The washerwoman by the fountain has had my best one for three days. THREE."],
  // woven: the great-nephew nobody thinks about is the Caesar Augustus of Luke 2:1. Nobody in Rome knows it this morning.
  "rome.senator.ask.caesar": ["son", "Does Caesar have a kid? A kid like that could get in ANYWHERE."],
  "rome.senator.ans.caesar.1": ["senator", "Caesar has no son. A great-nephew, Octavius, is at his books in Apollonia."],
  "rome.senator.ans.caesar.2": ["senator", "Nobody gives the boy a thought. I mention him only because I am thorough."],
  "rome.senator.ans.caesar.3": ["son", "I know another Caesar! Augustus. He counts everybody in the Christmas story."],      // PASS-17R: no reference aloud
  "rome.senator.ans.caesar.4": ["senator", "Augustus. There is no such name. I know every name in Rome that matters."],
  "rome.senator.ans.caesar.5": ["son", "...Not yet."],
  "rome.senator.ask.dad": ["son", "Seen my dad? Little beard, flowers all over his shirt?"],
  "rome.senator.ans.dad.1": ["senator", "Flowers. On a shirt. In the Forum. No. I would have made a speech about it."],
  "rome.senator.ans.dad.2": ["son", "Mom's made a few."],
  "rome.senator.ask.bye": ["son", "Good luck with the drains!"],
  "rome.senator.ans.bye": ["senator", "Luck is for men without speeches."],
  // ROME-13W (decision 12): was "Delivery! One clean bedsheet with a purple stripe. From the laundry lady." A senator's
  // toga is plain white; his mark is the broad stripe down his tunic. Said at the second delivery, the right toga's.
  "rome.senator.toga.1": ["son", "Delivery! One clean bedsheet from the laundry lady. Like a cloud with a job."],
  "rome.senator.toga.2": ["senator", "A TOGA, boy. A bedsheet covers a man asleep. A toga covers a man who matters."],
  "rome.senator.toga.3": ["son", "It's really heavy for something with no pockets."],
  "rome.senator.toga.4": ["senator", "Rome thanks you. I, personally, am far too late."],
  "rome.senator.toga.5": ["senator", "To the Senate! They would never dare begin without me."],
  "rome.senator.toga.6": ["son", "Delivered. The laundry lady owes me one tunic."],
  "rome.senator.breakfast": ["senator", "I do not eat in the street. I am SEEN in the street."],
  "rome.senator.incense": ["senator", "Incense is for gods. I am only a senator. ...Only."],

  // ---------- ROME-13W: the senator's turn (#2 Deliver It, the first time: decision 2) ----------
  // The first time the boy brings the toga it is the wrong one. He says wrong.1 (as the choice "give", and as the line,
  // in place of toga.1); the senator takes it, unfolds it, holds it up, turns from the boy and back: it is new, and it
  // reaches the ground twice. It is a Gaul's, and the Gaul has his. He hands the enormous one back (`toga` taken,
  // `gaultoga` given, rome.wrongToga) and stays, pacing. The second time, with his own, the old delivery as it is.
  "rome.senator.wrong.1": ["son", "Delivery! One bedsheet, folded by a professional."],
  "rome.senator.wrong.2": ["senator", "At LAST. Three days. Give it here."],
  "rome.senator.wrong.3": ["senator", "...This toga is new. It has never been to the Senate. Or to ANYTHING."],
  "rome.senator.wrong.4": ["senator", "And it reaches the ground. Twice."],
  "rome.senator.wrong.5": ["son", "Maybe it's a growing toga. Mom buys all my clothes big."],
  "rome.senator.wrong.6": ["senator", "The laundress fulled a toga for one of the dictator's new Gauls. He has MINE."],
  "rome.senator.wrong.7": ["senator", "He will be in the Forum, lost. They are always lost."],
  "rome.senator.wrong.8": ["son", "Find the lost Gaul. Swap the bedsheets."],
  // the Gaul's toga shown to him again; and the lamp
  "rome.senator.gaultoga": ["senator", "Put that away. I have seen enough of it for one morning. Find the Gaul."],
  "rome.senator.lamp": ["senator", "A lamp. It is MORNING, boy. Even I can see that, and I am late."],

  // ---------- the rest of the Forum ----------
  "rome.altar.look": ["son", "A stone barbecue in a flower necklace. Nothing's cooking."],
  "rome.altar.use": ["son", "Dad's one barbecue rule: never touch a grill you didn't light. He breaks it."],
  "rome.altar.incense": ["son", "For the god. INSIDE."],
  "rome.forum.look": ["son", "A whole downtown and not one car. It's recess for grown-ups."],
  "rome.forum.look2": ["son", "A temple on that hill too. Rome puts temples on everything, like sprinkles."],
  "rome.stone.look": ["son", "S. P. Q. R. No vowels. You can't even sneeze that."],
  "rome.pigeons.look": ["son", "Same pigeons as at home. Maybe they time travel. It'd explain a LOT."],
  "rome.pigeons.use": ["son", "Not chasing them. Last time, Dad had to apologize to a truck."],
  "rome.tripod.look": ["son", "A giant bronze cake stand. No cake. Rome keeps getting my hopes up."],
  "rome.board.look": ["son", "Tiny letters. Rome has terms and conditions. Nobody reads them here either."],
  "rome.tostreet.look": ["son", "That street smells of bread, sausage and one other thing. I'm not asking."],
  "rome.cart.look": ["son", "Sacks, going in under the temple. The treasury has a drive-through."],
  "rome.dog.look": ["son", "A dog! I ask for one every birthday. Dad says we'll see. We never see."],
  "rome.dog.use": ["son", "Here, boy. ...He opened one eye and shut it. Would adopt."],
  "rome.dog.breakfast": ["son", "It's the chicken man's sausage. Hardest thing I've ever NOT done."],

  // ---------- ROME-13W: the two new ways (bottom edge into the Forum, right edge up to the Capitol), and the far view in two ----------
  // Until he has been to the street and worked out that it is B.C. (rome.knowsBC), each way, and each half of the far
  // view, says rome.steps.closed and he stays. The far view's lower half keeps its old looks (rome.forum.look, .look2);
  // the hill above it is a thing of its own: its first look before he has been up, its second once he has (rome.sawCapitol).
  "rome.steps.closed": ["son", "Snacks first. My nose has spoken."],
  "rome.hill.look": ["son", "The road up there goes round the back of this temple. Rome hides its stairs."],
  "rome.hill.look2": ["son", "I've BEEN up there. The geese say hi."],

  // ================= rome-street: the shopping street =================

  "rome.street.arrive.1": ["son", "Whoa. A whole street of snacks and laundry."],
  // woven: he hears whose nose is on the new money, and works out when he is. (The era card has just told the
  // player "44 B.C."; this is where he catches up, and where everything he says "Not yet." about begins.)
  "rome.street.cry": ["keeper", "Hot sausage, hot bread! New silver with Caesar's nose, I take every nose!"],
  "rome.street.bc.1": ["son", "JULIUS Caesar? He's on Big Sis's timeline. The B.C. side."],
  "rome.street.bc.2": ["son", "B.C. Before Christ. ...It's before the FIRST Christmas."],
  "rome.toforum.look": ["son", "Down there: the temple, the hum, and the door guy. One of them likes me."],

  // ---------- the snack bar and its keeper ----------
  "rome.snackbar.look": ["son", "Giant soup jars sunk in the counter, and bread. Step one: FOUND."],
  "rome.snackbar.look2": ["son", "No front wall. A kitchen you can walk past. Best idea ever."],
  "rome.pricelist.look": ["son", "A menu on the wall, and no pictures. How do you know what it LOOKS like?"],
  "rome.keeper.look": ["son", "Cooking, talking and waving a spoon, all at once. He's like three dads."],
  "rome.keeper.look2": ["son", "He hasn't stopped talking since I got here. He might be part fish."],
  "rome.keeper.hi.1": ["keeper", "A customer, a small one, too thin, everybody is too thin, here, eat, eat."],
  "rome.keeper.hi.2": ["son", "Bread with cheese in it. Step one: DONE. Needs ketchup."],
  "rome.keeper.hi.3": ["keeper", "It needs what?"],
  "rome.keeper.hi.4": ["son", "Ketchup. It's tomatoes, but a sauce."],
  "rome.keeper.hi.5": ["keeper", "What is a tomato?"],
  "rome.keeper.hi.6": ["son", "...No tomatoes. Dad's been saving those little packets for years. He KNEW."],
  // ROME-13W (#4 Take The Breakfast, changed: he no longer hands the breakfast over). His boy Titus took it at first
  // light and has not come back: every Ides the boy runs after the white ewe that goes up to Jupiter. Said in this
  // order: errand.1, .2, .ewe, .3, .4. (The old words of all four are in the writer's ids.md for the round.)
  "rome.keeper.errand.1": ["keeper", "Never mind, you have legs, good, I need legs, I have lost my boy, my Titus."],
  "rome.keeper.errand.2": ["keeper", "He took the old soothsayer's breakfast at first light, bread and a sausage."],
  "rome.keeper.errand.2.b": ["son", "Where did he go?"],  // PASS-19R1: new, after rome.keeper.errand.2
  "rome.keeper.errand.3": ["keeper", "Up to Jupiter's hill, after the white ewe. Bring down my boy and the breakfast."],
  "rome.keeper.errand.4": ["son", "Find the kid, find the sausage. I won't eat it. I'll just THINK about it."],
  "rome.keeper.ask.pay": ["son", "How much do I owe you? I've got a quarter."],
  "rome.keeper.ans.pay.1": ["keeper", "Who is this? I know every consul's nose. That is not a consul."],
  "rome.keeper.ans.pay.2": ["son", "That's George. Back home, EVERYBODY knows that nose."],      // PASS-17R: answers him back; and not every quarter has George now (us.quarter)
  "rome.keeper.ans.pay.3": ["keeper", "I do not know George, keep him, pay me later, everyone pays me later."],
  "rome.keeper.ans.pay.4": ["son", "He gave me a tab. I have a TAB. I'm telling everyone."],
  "rome.keeper.ask.pizza": ["son", "Do you have pizza?"],
  "rome.keeper.ans.pizza.1": ["keeper", "What is pizza?"],
  "rome.keeper.ans.pizza.2": ["son", "Flat bread. Cheese. Sauce."],
  "rome.keeper.ans.pizza.3": ["keeper", "Flat bread I have, cheese I have, what is the sauce?"],
  "rome.keeper.ans.pizza.4": ["son", "...Tomatoes."],
  "rome.keeper.ans.pizza.5": ["keeper", "This word again."],
  "rome.keeper.ask.owe": ["son", "Does everybody owe you money?"],
  "rome.keeper.ans.owe.1": ["keeper", "The senator owes forty dinners. The soothsayer, eleven years."],
  "rome.keeper.ans.owe.2": ["keeper", "The wall is for prices, my head is for debts, my head is very full."],
  "rome.keeper.ask.dad": ["son", "Seen my dad? Little beard, flowers on his shirt, always making good time?"],
  "rome.keeper.ans.dad.1": ["keeper", "No, and everyone eats here, if he is in Rome he will come, so sit, wait, eat."],
  "rome.keeper.ans.dad.2": ["son", "Best plan anybody's had all day. It has snacks in it."],
  "rome.keeper.ask.bye": ["son", "Best step one ever."],
  "rome.keeper.ans.bye": ["keeper", "Go, come back, bring the plate, there was no plate, go."],
  "rome.keeper.coin.1": ["keeper", "THAT nose I know, that is Caesar, struck this year, good silver."],
  "rome.keeper.coin.2": ["son", "He looks like he needs a sausage."],
  "rome.keeper.coin.3": ["keeper", "Everybody needs a sausage, that is my whole trade."],
  "rome.keeper.toga": ["keeper", "A senator's toga, beside my sauce, out, out, I cannot pay to wash it twice."],
  "rome.keeper.breakfast": ["keeper", "No, no, UP the street, the old one with the chickens, it is getting cold."],
  "rome.keeper.gum.1": ["son", "Want some gum? You chew it, but you never eat it."],
  "rome.keeper.gum.2": ["keeper", "Food that is never eaten. The saddest thing ever said at my counter."],

  // ---------- ROME-13W: the keeper and his boy (Juno's Geese) ----------
  // In place of the errand, if the boy has met Titus already (Titus said whose boy he is) but has not got the breakfast:
  "rome.keeper.met.1": ["son", "Found him! He's up the hill on a statue. With your breakfast. And geese."],
  "rome.keeper.met.2": ["keeper", "Geese, every Ides the ewe, now geese, go back up, bring him down."],
  // In place of the errand, if the boy walks in already carrying the breakfast (he met Titus first, and the geese went):
  "rome.keeper.carrying.1": ["keeper", "My cloth, the old one's breakfast, where is my boy, where is my Titus?"],
  "rome.keeper.carrying.2": ["son", "On his way home. He was stuck on a statue. There were geese. I did a stomp."],
  "rome.keeper.carrying.3": ["keeper", "Every Ides something. Up the street with it, quick, before it is a lunch."],
  // The first time he is talked to once Titus is home (rome.metTitus and rome.hasBreakfast):
  "rome.keeper.titus.1": ["keeper", "My boy is home. He says your shoes frightened Juno's geese. Have a sausage."],
  "rome.keeper.titus.2": ["son", "I won't even ask about the ketchup. I've grown as a person."],
  // the two new things carried, shown to him
  "rome.keeper.gaultoga": ["keeper", "That is not a toga, that is a tent, I cannot pay to wash a tent."],
  "rome.keeper.lamp": ["keeper", "For Felix, for Corinth. Everybody eats here, I hear everything."],

  // ---------- the washerwoman and her laundry ----------
  "rome.washer.look": ["son", "She folds a sheet in four moves. Dad fought one for ten minutes and lost."],
  "rome.washer.look2": ["son", "Arms like the door guy's. I'd watch that arm wrestle. I'd bring snacks."],
  "rome.washer.hi.1": ["washer", "Mind the basket. Those are clean, and you are not."],
  "rome.washer.hi.2": ["son", "I'm travel dirty. It's different. It's got miles on it."],
  "rome.washer.hi.3": ["washer", "A hood with no head in it. Whoever dresses you enjoys a joke."],      // PASS-17R: true to the picture (no cap; his hood is down)
  "rome.washer.hi.4": ["son", "That's my mom. You'd like her. You both look at my knees the same way."],
  "rome.washer.errand.1": ["washer", "Can you run? The senator is at the temple steps, turning purple."],
  "rome.washer.errand.2": ["washer", "I cannot leave the tubs. Take him his toga, and I will lend you a tunic."],
  "rome.washer.errand.3": ["son", "Deal. I'll carry it by the corners."],
  "rome.washer.ask.white": ["son", "How do you get them so white?"],
  "rome.washer.ans.white.1": ["washer", "We tread them in the tubs, with stale urine."],
  "rome.washer.ans.white.2": ["son", "Urine. Like... PEE?"],
  "rome.washer.ans.white.3": ["washer", "Is there another kind?"],
  "rome.washer.ans.white.4": ["son", "Best fact ever. My sister will be so mad I knew it first."],
  "rome.washer.ans.white.6": ["son", "...Wait. This bedsheet I'm holding..."],
  "rome.washer.ans.white.7": ["washer", "Was rinsed. Twice."],
  "rome.washer.ans.white.8": ["son", "I'm going back to the corners."],
  "rome.washer.ask.tunic": ["son", "About that tunic..."],
  "rome.washer.ans.tunic": ["washer", "Toga first, then tunic. Twenty years of laundry, on 'first' and 'then'."],
  "rome.washer.ask.dad": ["son", "Seen my dad? Little beard, flowered shirt. You'd remember the shirt."],      // PASS-17R: was the doorkeeper's words exactly; now she answers it
  "rome.washer.ans.dad.1": ["washer", "Flowers. On a shirt. No. I would remember WASHING that."],
  "rome.washer.ask.bye": ["son", "I'll be careful with your bedsheets."],
  "rome.washer.ans.bye": ["washer", "Togas. Go on with you."],
  "rome.washer.tunic.1": ["son", "Delivered! He said Rome thanks you. He was too late to say it himself."],
  "rome.washer.tunic.2": ["washer", "That sounds like him. Here: my sister's boy outgrew it. Bring it back clean."],
  "rome.washer.tunic.3": ["son", "A real Roman tunic. It's a dress with a belt. Nobody tell my school."],
  "rome.washer.toga": ["washer", "Not to me. To HIM. Up at the temple steps, the color of a plum."],
  "rome.washer.coin": ["washer", "That has been in the fountain. I wash cloth, child, not wishes."],
  "rome.washer.breakfast": ["washer", "Keep that from the whites. One drip of sausage and I start the day again."],
  "rome.washer.tunic.back": ["washer", "Keep it till sundown. And keep it out of the sauce."],

  // ---------- ROME-13W: the washerwoman's mix-up (decision 2), shown the Gaul's toga ----------
  // The first time: mortified, briefly, and then brisk again. After that: .again.
  "rome.washer.gaultoga.1": ["son", "This isn't the senator's. It's a Gaul's. It reaches the ground TWICE."],
  "rome.washer.gaultoga.2": ["washer", "A big man came in the dark for 'the senator's toga'. I gave him the senator's."],
  "rome.washer.gaultoga.3": ["washer", "Twenty years on first and then, and I gave the wrong first."],
  "rome.washer.gaultoga.4": ["washer", "Find the Gaul, child. Big, lost, knees out. Go."],
  "rome.washer.gaultoga.again": ["washer", "I KNOW, child. Find the Gaul. And never say a word of it to my sister."],
  "rome.washer.lamp": ["washer", "Oil and wool do not mix, child. Keep that lamp away from my tubs."],

  "rome.laundry.look": ["son", "Bedsheets right across the street. The sleepover put up decorations."],
  "rome.laundry.look2": ["son", "That white one glows. So that's what clean looks like. I'd forgotten."],
  "rome.tunic.look": ["son", "A tunic my size. A long T-shirt that gave up on sleeves."],
  "rome.tunic.hands": ["washer", "Hands off the line, child. Those are counted."],
  "rome.basket.look": ["son", "Wet laundry, heavier than me. I can tell. It has that look."],
  "rome.basket.look2": ["son", "Now I know what it was washed in, I'll admire it from here."],
  "rome.basket.use.1": ["washer", "Not the basket, child."],
  "rome.basket.use.2": ["son", "I wasn't going to. ...I was a little going to."],

  // ---------- the fountain ----------
  "rome.fountain.look": ["son", "There's money at the bottom. People throw coins in the water here. On PURPOSE. I love this place."],   // kept
  "rome.fountain.take": ["son", "Operation Borrow-A-Wish is GO. Splish."],                                                           // kept
  "rome.fountain.again": ["son", "One wish is borrowing. Two is a crime spree."],                                                     // kept
  "rome.fountain.shiny": ["son", "So shiny I can see my face, next to the serious man. He's not happy."],
  "rome.fountain.wish.1": ["urchin", "That's somebody's wish, you know."],
  "rome.fountain.wish.2": ["son", "I'm only borrowing it. I'll pay it back with interest. Interest is extra wishes."],
  // ROME-13W (#7 Borrow A Wish, then decision 7): after the kept lines above, Walnut says whose wish it was, and the boy
  // answers (rome.knowsWish). Then his look at the coin, as before.
  "rome.fountain.wish.3": ["urchin", "It's Phyllis's. The garland woman, by Castor's temple. It's for her boy."],
  "rome.fountain.wish.4": ["son", "Then I'll ask her. You can borrow a wish. You can't throw one away."],
  // woven: his first hard look at it. Matthew 22:17-21 in his own words (the verse itself is Mom's, in Act Four).
  "rome.fountain.caesar.2": ["son", "It says CAESAR. Like when Jesus asks whose picture is on the coin."],
  "rome.fountain.caesar.2.b": ["urchin", "Caesar's. Everybody knows that nose."],  // PASS-19R1: new, after rome.fountain.caesar.2
  "rome.fountain.caesar.3": ["son", "So Caesar gets his coin, and God gets what's God's. Me included."],
  "rome.fountain.caesar.4": ["son", "But Jesus is grown up in that story. This isn't that Caesar. Not yet."],
  "rome.fountain.toga": ["son", "Dunk a clean bedsheet? The laundry lady has ARMS. I've seen them."],
  "rome.fountain.quarter": ["son", "A quarter? Somebody digs that up in two thousand years. SO many questions."],
  "rome.fountain.phone": ["son", "It's already dead. It doesn't need to be drowned too."],
  "rome.fountain.coin": ["son", "Throw it back? I'm saving this wish for something big. Or small."],

  // ---------- the street boy ----------
  "rome.urchin.look": ["son", "A kid! Playing marbles with walnuts. Finally, somebody not grown up."],
  "rome.urchin.look2": ["son", "He keeps looking at my shoes. He's got good taste."],
  "rome.urchin.hi.1": ["urchin", "Your feet are on fire."],
  "rome.urchin.hi.2": ["son", "They light up when I stomp. Watch."],
  "rome.urchin.hi.3": ["urchin", "...Do it again."],
  "rome.urchin.hi.4": ["son", "That one was free. From now on it's a walnut a stomp."],
  "rome.urchin.hi.5": ["urchin", "I'm the best at nuts on this street. You're the best at feet. Friends?"],
  "rome.urchin.hi.6": ["son", "Deal. I'm calling you Walnut."],
  "rome.urchin.ask.game": ["son", "How do you play the walnut game?"],
  "rome.urchin.ans.game.1": ["urchin", "Build a castle of nuts. Throw one. Knock it down and they're yours."],
  "rome.urchin.ans.game.2": ["son", "Like bowling, but you keep the pins. Then you EAT the pins."],
  "rome.urchin.ans.game.3": ["son", "...I missed the castle and hit a pigeon."],
  "rome.urchin.ans.game.4": ["urchin", "The pigeon's fine. That's two nuts you owe me."],
  "rome.urchin.ans.game.5": ["son", "One hour in Rome and I'm already in nut debt."],
  "rome.urchin.ask.temple": ["son", "Have you ever been inside the temple?"],
  "rome.urchin.ans.temple.1": ["urchin", "Me? You need a clean tunic and a father who knows somebody. I've got a tunic."],
  "rome.urchin.ans.temple.2": ["son", "I've got a father. I just don't know where. There's a tunnel in it."],
  "rome.urchin.ans.temple.3": ["urchin", "You lost your father? ...You can share the sausage man. Everybody does."],
  "rome.urchin.ask.help": ["son", "I'm stuck, Walnut. What would you do?"],
  "rome.urchin.ask.light": ["son", "Walnut. How do you get light onto a wall in the dark?"],
  "rome.urchin.ask.tiny": ["son", "There's a door in there the size of a coin. What do you DO with that?"],
  "rome.urchin.tip.rule": ["urchin", "Ask old Doorpost what he DOES let in. He loves a rule."],
  "rome.urchin.tip.toga": ["urchin", "A clean tunic? The laundry woman has a hundred. And nobody to run errands."],
  "rome.urchin.tip.deliver": ["urchin", "That's the senator's toga. He's the angry one at the temple steps. Run."],
  "rome.urchin.tip.tunic": ["urchin", "You did her job. Go get your tunic. She keeps her word."],
  "rome.urchin.tip.breakfast.1": ["urchin", "Something for the god? Old Gloom on the steps has incense. But he's hungry."],
  // ROME-13W: re-worded (it was "...Today it's still on the counter."): the breakfast went up the hill with the keeper's boy.
  "rome.urchin.tip.breakfast.2": ["urchin", "The sausage man's boy took his breakfast up at first light. Never came back."],
  "rome.urchin.tip.incense": ["urchin", "Old Gloom's breakfast is going cold in your bag. The one with the chickens."],
  "rome.urchin.tip.inside": ["urchin", "Tunic. Incense. So GO. Before Doorpost thinks of a fourth rule."],
  "rome.urchin.tip.shiny.1": ["urchin", "Easy. Something shiny, in the sun. I do it to the sausage man."],
  "rome.urchin.tip.shiny.2": ["urchin", "The shiniest things on this street? New silver, in the fountain."],
  "rome.urchin.tip.spark": ["urchin", "You've got something shiny. Find where the sun comes in."],
  "rome.urchin.tip.toss": ["urchin", "A door the size of a coin? Then put a coin through it. What else fits?"],
  // ROME-13W: his tips for the new beats, in the beats' order. tip.gaul also says where the Senate meets today, so that
  // the boy has heard it from him too (rome.knowsSenate). tip.gaul, .redeliver and .geese answer "I'm stuck, Walnut. What
  // would you do?"; tip.wish, .felix and .granted answer the door the size of a coin (rome.urchin.ask.tiny), as .toss does.
  "rome.urchin.tip.gaul": ["urchin", "Big Gaul, little toga? Tell him they meet in Pompey's hall, by the theater."],
  "rome.urchin.tip.redeliver": ["urchin", "Right toga? Run it to the senator at the temple steps. He's going purple."],
  "rome.urchin.tip.geese": ["urchin", "The Capitol geese scream at anything they've never seen. The Gauls found out."],   // FINAL-19: REVIEW-19's patch
  "rome.urchin.tip.wish": ["urchin", "Put a coin through. But that's Phyllis's wish: ask her, at Castor's temple."],
  "rome.urchin.tip.felix": ["urchin", "First the lamp. Felix works the barges, over the stone bridge. Big. Sunburnt."],
  "rome.urchin.tip.granted": ["urchin", "Felix said yes? Tell Phyllis before you throw anything. It's her wish."],
  "rome.urchin.ask.bye": ["son", "See you, Walnut."],
  "rome.urchin.ans.bye": ["urchin", "Stomp when you go. So I can watch."],
  "rome.urchin.gum.1": ["son", "Want some gum? You chew it. You don't swallow it."],
  "rome.urchin.gum.2": ["urchin", "Then what's it for?"],
  "rome.urchin.gum.3": ["son", "...Nobody knows. It's minty, though."],
  "rome.urchin.gum.4": ["urchin", "It's fighting back. I LIKE it."],
  "rome.urchin.coin.1": ["urchin", "That's fountain silver. It's still wet."],
  "rome.urchin.coin.2": ["son", "It's a borrowed wish."],
  "rome.urchin.coin.3": ["urchin", "My whole life on this street, and I never once thought of BORROWING one."],
  "rome.urchin.phone.1": ["urchin", "A black tile."],
  "rome.urchin.phone.2": ["son", "It takes pictures. When it's alive."],
  "rome.urchin.phone.3": ["urchin", "Pictures of what?"],
  "rome.urchin.phone.4": ["son", "Mostly a donkey."],
  "rome.urchin.quarter.1": ["urchin", "There's a bird on the back. Is it worth a walnut?"],
  "rome.urchin.quarter.2": ["son", "It's worth twenty-five... honestly? Here? About a walnut."],
  "rome.urchin.toga": ["urchin", "A senator's toga! Don't let it touch me. I'm mostly ground."],
  "rome.urchin.breakfast": ["urchin", "Old Gloom's. I can smell it. I'm being very brave about it."],
  // ROME-13W: a game saved with the coin borrowed before Walnut said whose it was: he says so the next time the boy walks
  // into the street (rome.knowsWish). And the two new things carried, shown to him.
  "rome.urchin.wish.1": ["urchin", "That wish you borrowed is Phyllis's. The garland woman, at Castor's temple."],
  "rome.urchin.wish.2": ["son", "Then I'll ask her. Borrowing's fine. Throwing somebody's wish away is NOT."],
  "rome.urchin.gaultoga": ["urchin", "That's a Gaul's. You could fit the Gaul AND me in there."],
  "rome.urchin.lamp": ["urchin", "Phyllis's lamp. Don't drop it. She'd know from across the river."],

  // ---------- the date seller (woven: all of him) ----------
  // A Jew from Judea, about fifty, selling dates from Jericho on the right-hand pavement. Courteous, humorous,
  // unhurried, nobody's fool. He is part of no puzzle and gives nothing that is carried. He says nothing about
  // the Romans' gods, and nobody tells him anything about the future: the Son, for once, holds his tongue.
  "rome.dateseller.look": ["son", "A man selling... giant raisins? The only one in Rome not in a hurry."],
  "rome.dateseller.look2": ["son", "He keeps looking a long way off. Like he's waiting for somebody."],
  "rome.dateseller.hi.1": ["dateseller", "Dates, young sir. From Jericho. There are none better: I have looked."],
  "rome.dateseller.hi.2": ["son", "Jericho? The Jericho with the WALLS?"],
  "rome.dateseller.hi.3": ["dateseller", "You know of the walls? ...The palms have done better than the walls."],      // PASS-17R: he wears no hat; his shoes are what Rome sees
  "rome.dateseller.ask.try": ["son", "Can I try one? I'm between snacks."],
  "rome.dateseller.ans.try.1": ["dateseller", "For a boy who knows of Jericho, the first is a gift. Here."],
  "rome.dateseller.ans.try.2": ["son", "It's candy that GROWS. Nine out of... ow. There's a rock in it!"],
  "rome.dateseller.ans.try.3": ["dateseller", "The stone. That part is a palm tree not begun. I ought to charge for the tree."],
  "rome.dateseller.ask.god": ["son", "Everybody here prays to a statue. Which one's yours?"],
  "rome.dateseller.ans.god.1": ["dateseller", "None. We have one God, the God of Abraham, of Isaac and of Jacob."],
  "rome.dateseller.ans.god.2": ["son", "I know those guys! He's our God too. We pray to Him at my house."],      // PASS-17R: they pray to Abraham's God, not to Abraham
  "rome.dateseller.ans.god.3": ["dateseller", "At your house. ...Then the world is larger than Rome has told me."],
  "rome.dateseller.ans.god.4": ["dateseller", "Rome finds us Jews very funny: a great Temple in Jerusalem, and no statue in it."],
  "rome.dateseller.ans.god.4.b": ["son", "Then what's in it?"],  // PASS-19R1: new, after rome.dateseller.ans.god.4
  "rome.dateseller.ans.god.5": ["dateseller", "Pompey himself went in, nineteen years ago. He found no image. Not one."],
  "rome.dateseller.ans.god.6": ["dateseller", "How would they carve the One who made the stone? They buy their dates and go."],
  "rome.dateseller.ask.pray": ["son", "What do you pray for?"],
  "rome.dateseller.ans.pray.1": ["dateseller", "For the promised one, every day, facing Jerusalem. Micah has told us his town:"],
  "rome.dateseller.ans.pray.2": ["dateseller", "'But thou, Bethlehem Ephratah, though thou be little among the thousands of Judah,'"],          // Micah 5:2, King James Version, the first clause: exact, comma and all
  "rome.dateseller.ans.pray.3": ["son", "That was MY line in the Christmas program! ...I know so much about Bethlehem."],      // PASS-17R: no reference aloud: where he knows it from
  "rome.dateseller.ans.pray.4": ["son", "I've never wanted to tell anybody so much. It's the angels' job, not mine."],      // PASS-17R: a boy's words for it
  "rome.dateseller.ans.pray.4.b": ["dateseller", "Young sir?"],  // PASS-19R1: new, after rome.dateseller.ans.pray.4
  "rome.dateseller.ans.pray.5": ["son", "It's going to be worth the wait, mister. Keep watching that town."],
  "rome.dateseller.ans.pray.6": ["dateseller", "...That was not a guess. I will not ask you what it was. But I will watch."],
  // (The id of the blessing is chosen with care: the engine picks each line's gesture from its id, and this one
  // gives him a hand laid on his chest. Renumber it and he may bless the boy with a shrug, or with a date in his hand.)
  "rome.dateseller.bless.1": ["dateseller", "And for you, young sir: 'The LORD bless thee, and keep thee:'"],                                   // Numbers 6:24, King James Version: exact, colon and all
  "rome.dateseller.bless.2": ["son", "That's how church ends. The very same words. ...Thanks, mister."],      // PASS-17R: no reference aloud
  "rome.dateseller.ask.bye": ["son", "Bye, mister."],
  "rome.dateseller.ans.bye": ["dateseller", "Go well. Come any day but the seventh. I rest, and Rome always wants dates."],
  "rome.dateseller.quarter.1": ["dateseller", "An eagle? Whoever struck this was proud of his bird. ...It is not silver."],
  "rome.dateseller.quarter.2": ["dateseller", "A coin should go home. Ours go to the Temple in Jerusalem: the half-shekel."],
  "rome.dateseller.phone": ["dateseller", "A black mirror. It shows an old man selling dates. It is not wrong."],
  "rome.dateseller.toga": ["dateseller", "A senator's toga. He buys my best dates and remembers them as cheaper."],
  "rome.dateseller.coin.1": ["dateseller", "Caesar has been a friend to us Jews of Rome. We may meet, and keep our ways."],
  "rome.dateseller.coin.2": ["dateseller", "But that is fountain silver, young sir. Somebody's wish. Not a price."],
  // chickens: the soothsayer's breakfast, shown to him. He will not have his fortune told by hens, thank you. (A small shrug.)
  "rome.dateseller.breakfast": ["dateseller", "The soothsayer's. He offers my fortune by his hens. Not by hens, thank you."],
  // ROME-13W (woven): once, after his blessing (rome.dateseller.bless.2) or at his goodbye, whichever comes first. He is
  // in no puzzle; this points the way to his wife's father, across the river. And the two new things carried, shown to him.
  "rome.dateseller.eleazar": ["dateseller", "My wife's father Eleazar reads in the house of prayer over the river. Greet him."],
  "rome.dateseller.gaultoga": ["dateseller", "That toga could shelter a family. Mine, for instance."],
  "rome.dateseller.lamp": ["dateseller", "A good little lamp. Whoever it is for, may it light a good house."],

  // ---------- the rest of the street ----------
  "rome.stones.look": ["son", "Stones to hop on, so your feet stay out of the... street. Good thinking, Rome."],
  "rome.stones.look2": ["son", "Paul takes a road like this into Rome one day. Dotted line in my Bible. Not yet."],   // woven: Acts 28:15-16. PASS-17R: shorter, and his own (the map), not a lesson
  "rome.cat.look": ["son", "A cat, ignoring a whole city. Cats were already like this."],
  "rome.cat.use": ["son", "Here, kitty. ...Ignored, in a whole other century."],
  "rome.shrine.look": ["son", "A painted snake with a tiny house and a night-light. Nicer than my room."],
  "rome.notices.look": ["son", "MARCVS. They spelled Marcus with a V. Nobody tell Marcus."],
  "rome.notices.look2": ["son", "VOTA. Somebody's running for something."],
  "rome.rufus.look": ["son", "RVFVS. That's Rufus, or the noise a dog makes when it's being fancy."],
  "rome.flats.look": ["son", "Four floors and no elevator. Everyone up there has shopping-bag face."],
  "rome.jars.look": ["son", "Pointy-bottomed jars. They can't stand on their own. Same, before breakfast."],
  "rome.wheel.look": ["son", "A wheel as tall as me. No tire. That cart feels every rock."],
  "rome.sign.look": ["son", "A sign with a jug and grapes. Pictures! Finally, somebody in Rome gets it."],
  "rome.songbird.look": ["son", "A bird in a cage, singing its head off. The cat's a big fan. A BIG fan."],

  // ================= rome-temple: inside the temple, the treasury =================

  "rome.inside.1": ["clerk", "...four hundred and eleven, four hundred and twelve..."],
  "rome.inside.2": ["son", "Tunic off. It itches like a hay sweater. Romans are tough."],
  "rome.inside.4": ["son", "Hi, door. I can hear you. You're terrible at hide-and-seek."],
  "rome.inside.5": ["clerk", "...four hundred and... who is talking? No. Do not tell me. ...One. Two."],
  "rome.out.look": ["son", "The way out, past the door guy. He likes me now. He hides it well."],

  // ---------- the place that hums, and the sunlight ----------
  "rome.hole.look": ["son", "It hums. Dad says it's the wind. Dad says EVERYTHING is the wind. I have a list."],                   // kept
  "rome.hum.try.1": ["son", "In the big pointy place I shined my flashlight at the hum, and POP: door."],
  "rome.hum.try.2": ["son", "My flashlight got left behind. Fine. Phone light!"],
  "rome.hum.try.2.b": ["clerk", "...No lights near the silver. ...One."],  // PASS-19R1: new, after rome.hum.try.2
  "rome.hum.try.3": ["son", "Zero percent. It can't even be sad about it."],
  "rome.hum.try.4": ["son", "So the door likes light. I need the kind you don't charge."],
  "rome.hum.again": ["son", "Still shut. It wants light, and the light's all on the floor."],
  "rome.hum.coin": ["son", "Too dark here. A coin's only shiny with sun to be shiny WITH."],
  "rome.hum.gum": ["son", "I'm not sticking gum on a time door. I've seen what gum does to a desk."],
  "rome.hum.incense": ["son", "The holy smell's for the statue. The door likes light. I'm new at doors."],
  "rome.sun.look": ["son", "Sunshine on the floor. Free light, just lying there."],
  "rome.sun.look2": ["son", "Sun here, hum there. Somebody should introduce them. Somebody shiny."],
  "rome.sun.use.1": ["son", "Warm. Something shiny could bounce it. I do it with my spoon."],
  "rome.sun.use.2": ["son", "Mom has asked me to stop. Twice a week."],
  "rome.sun.done": ["son", "The little door's open. No need to zap the counting guy twice."],
  "rome.sun.phone": ["son", "Cracked screen. A hundred tiny lights going everywhere. Pretty. Useless."],
  "rome.sun.gum": ["son", "Paper wrappers, no foil. This gum didn't plan for time travel."],
  "rome.sun.quarter": ["son", "This quarter's been through the wash. No shine left. I need a NEW coin."],

  // the spark: a spot of sunlight off the coin, and a door the size of the coin
  "rome.spark.1": ["son", "Sun, meet coin. Coin, meet wall."],
  "rome.spark.2": ["clerk", "...five hundred and six, five hundred and sev... AGH. My eye."],
  "rome.spark.3": ["son", "Sorry. Wrong wall."],
  "rome.spark.4": ["clerk", "What was that light?"],
  "rome.spark.5": ["son", "The sun. It does that sometimes. It's a known sun thing."],
  "rome.spark.6": ["clerk", "...One. Two. Three."],
  "rome.spark.8": ["son", "POP! A door. A tiny one, exactly the size of the coin."],
  "rome.spark.10": ["son", "There's sky in there. Really far down. ...Why is the sky DOWN?"],

  // the door, once it is open, and the toss that ends the act
  "rome.door.look": ["son", "A coin-sized door with sky in it. My eye fits. The rest of me has to wait."],
  "rome.hole.use": ["son", "I'm not jumping in there again without a snack. That's a rule I made up just now and I stand by it."],   // kept
  "rome.hole.use2": ["son", "Also, I'm bigger than a coin. Physics made that rule up."],
  "rome.hole.quarter": ["son", "Not George. He's the only other American in Rome. We stick together."],
  "rome.hole.phone": ["son", "It won't fit. And a dead phone is not the message I want to send Dad."],
  "rome.hole.coin": ["son", "Heads, I find Dad. Tails, Dad finds me. Edge, we get a dog."],                                       // kept
  "rome.hole.coin2": ["son", "... It didn't come back down. Does that count as edge? Do we get the dog?"],                        // kept

  // ---------- ROME-13W: the toss waits for Phyllis's leave (#9, decision 7), and the lamp tried in here ----------
  // The coin used on the coin-sized door without rome.wishGranted: this line, and nothing else happens. With it, as above.
  "rome.hole.wish": ["son", "This is Phyllis's wish. I'm not throwing it through a door without asking."],
  "rome.hum.lamp": ["son", "It's not lit. And it's not mine. It's a goodbye present."],
  "rome.hole.lamp": ["son", "Post Felix's lamp through a time door? He'd light it in the wrong century."],
  "rome.sun.lamp": ["son", "It's clay. Clay doesn't shine. The coin's the shiny one."],
  "rome.statue.lamp": ["son", "It's for Felix. The statue's got plenty of stuff."],
  "rome.clerk.lamp": ["clerk", "An unlit lamp. In a treasury, that is the only good kind. ...One."],

  // ---------- the god, the treasure, the clerk ----------
  "rome.statue.look": ["son", "A giant grandpa statue with a hook knife. And yarn tied around his feet."],
  "rome.statue.look2": ["son", "Somebody tied his feet together. Either he's dangerous or he sleepwalks."],
  "rome.statue.use": ["son", "Untie a god's feet? I need bunny ears for my own laces."],
  "rome.statue.incense.1": ["son", "From the chicken man. He's sorry about the steps. And beware of today."],
  "rome.statue.incense.2": ["clerk", "...sixty-one, sixty-two... IN the bowl, boy, not beside it. ...One."],
  "rome.statue.coin": ["son", "A building full of money. He doesn't need my wish. He needs his feet."],
  "rome.statue.gum": ["son", "No gum for the statue. His feet are tied. He'd never get it off his shoe."],
  "rome.bowl.look": ["son", "The statue's snack bowl. Empty. I know that feeling."],
  "rome.bowl.done": ["son", "Holy smell, in the snack bowl. Three for three, counting the sausage."],

  "rome.chests.look": ["son", "Treasure chests with real locks. Best room I've ever been thrown out of."],
  "rome.chests.look2": ["son", "Sacks with seals. Chests with iron. Somebody REALLY doesn't want to share."],
  "rome.chests.use.1": ["clerk", "Do not touch the Roman People's money."],
  "rome.chests.use.2": ["son", "I was only looking. With my hands."],
  "rome.chests.use.3": ["clerk", "...One."],
  "rome.bankcat.look": ["son", "A cat asleep on the treasure. Nobody scores cats."],
  "rome.bankcat.use.1": ["son", "Hi, cat. ...She's purring. That's two things in here that hum."],
  "rome.bankcat.use.2": ["clerk", "...ninety-one... leave her. The one thing in here I do not have to count."],
  "rome.bankcat.coin": ["son", "She's asleep on a chest of these. One more won't impress her."],
  "rome.table.look": ["son", "A scale, a lamp, wax pads and a mountain of silver. Homework, but shiny."],
  "rome.table.use.1": ["clerk", "Away from the table. I have piles. The piles have an order."],
  "rome.table.use.2": ["son", "They look like piles."],
  "rome.table.use.3": ["clerk", "That is how I know you are not a clerk."],

  "rome.clerk.look": ["son", "He counts a mountain of coins, one by one. Like Dad doing taxes. Forever."],
  "rome.clerk.look2": ["son", "When I breathe loudly, he flinches. I'm breathing quietly. ...He flinched."],
  "rome.clerk.hi.1": ["clerk", "...seven hundred and eight, seven hundred and nine..."],
  "rome.clerk.hi.2": ["son", "Hi!"],
  "rome.clerk.hi.3": ["clerk", "...seven hundred and... no. It is gone. It has gone."],
  "rome.clerk.hi.4": ["clerk", "The incense boy. The bowl is at the god's feet. I am at one. Again."],
  "rome.clerk.again": ["clerk", "...two hundred and thirty... you. Of course. ...One."],
  "rome.clerk.ask.count": ["son", "What are you counting?"],
  "rome.clerk.ans.count.1": ["clerk", "The silver of the Roman People. Every denarius, twice, so the counts agree."],
  "rome.clerk.ans.count.2": ["son", "Do they ever agree?"],
  "rome.clerk.ans.count.3": ["clerk", "They did once. In my second year. I think of it often."],
  "rome.clerk.ask.feet": ["son", "Why are the statue's feet tied up?"],
  "rome.clerk.ans.feet.1": ["clerk", "Bands of wool. They are untied once a year, at his festival in December."],
  "rome.clerk.ans.feet.2": ["son", "ONE day off a year? Even Dad gets two weeks."],
  "rome.clerk.ans.feet.3": ["clerk", "I get the same day he does. We do not spend it together."],
  "rome.clerk.ask.hum": ["son", "Do you hear a hum? Over by that wall?"],
  "rome.clerk.ans.hum.1": ["clerk", "Since dawn. First a hum. Then a flash. Then a noise like a boy falling over."],
  "rome.clerk.ans.hum.2": ["clerk", "I did not look up. I was at nine hundred."],
  "rome.clerk.ans.hum.3": ["son", "That was... probably the wind."],
  "rome.clerk.ans.hum.4": ["clerk", "That is what I decided."],
  // woven: the governor of Galilee is the King Herod of Matthew 2. Not this year. (This one does not get the tag: three is the limit.)
  "rome.clerk.ask.judea": ["son", "What's on all the wax pads?"],
  "rome.clerk.ans.judea.1": ["clerk", "Judea's accounts. Antipater's, and his son Herod's, who governs Galilee."],
  "rome.clerk.ans.judea.2": ["son", "Herod? KING Herod? The bad king in the Christmas story?"],
  "rome.clerk.ans.judea.3": ["clerk", "Herod is no king. A procurator's son with expensive tastes. I have the figures."],
  "rome.clerk.ans.judea.4": ["son", "...I'd count him twice. I'm just saying."],
  "rome.clerk.ask.dad": ["son", "Have you seen my dad?"],
  "rome.clerk.ans.dad.1": ["clerk", "Is he made of silver?"],
  "rome.clerk.ans.dad.2": ["son", "No."],
  "rome.clerk.ans.dad.3": ["clerk", "Then I have not counted him."],
  "rome.clerk.ask.bye": ["son", "I'll let you count."],
  "rome.clerk.ans.bye": ["clerk", "Everyone says that. ...One."],
  "rome.clerk.coin.1": ["clerk", "Is that one of mine?"],
  "rome.clerk.coin.2": ["son", "No! It's a wish."],
  "rome.clerk.coin.3": ["clerk", "Good. If I had to count wishes as well, I would lie down on the floor."],
  "rome.clerk.quarter": ["clerk", "It is not silver, it is not Roman, and I refuse to count it."],
  "rome.clerk.phone.1": ["clerk", "A writing tablet with no wax. What do you scratch on?"],
  "rome.clerk.phone.2": ["son", "You don't scratch it. You poke it. When it's alive."],
  "rome.clerk.phone.3": ["clerk", "...I was happier not knowing that."],
  "rome.clerk.incense": ["clerk", "For the god. Not for me. The bowl. Quietly."],

  "rome.brazier.look": ["son", "An indoor campfire. No marshmallows. I checked."],
  "rome.brazier.use": ["son", "Hot. HOT. That is a looking-only campfire."],
  "rome.tablets.look": ["son", "Metal pages nailed to the wall. Tiny letters. ALL the rules."],
  "rome.standards.look": ["son", "Poles with shiny badges on top. Parade stuff. They keep the parade in the bank."],
  "rome.rack.look": ["son", "Cubbies, like at school, with scrolls instead of lunches. Worst cubbies ever."],

  // ================= ROME-13W: rome-forum: the Forum, from its east end =================
  // The open heart of Rome, looking west along its length to the temple of Saturn at the far end, small, and the Capitol
  // above everything. Reached from the steps' bottom edge once he knows it is B.C.

  // ---------- arrival (the first time: rome.sawForum) ----------
  "rome.forum.arrive.1": ["son", "Church, bank and construction site. Ten out of ten. Eleven for the crane."],
  "rome.forum.arrive.2": ["son", "Way down at the end, that's MY temple. Hi, door guy! ...He never waves."],
  "rome.forum.arrive.3": ["son", "Up on the hill, a gold roof. Rome does NOT do halfway."],

  // ---------- the things in it (a second look where one is worth it) ----------
  "rome.forum.castor.look": ["son", "A temple with a front porch like a stage. Mom would put on a play."],      // PASS-17R: his mother and the stage
  "rome.forum.castor.look2": ["son", "The flower lady's at the bottom. Best spot in town."],
  "rome.forum.castor.use": ["son", "Climb up? Somebody would make me say something."],
  "rome.forum.spring.look": ["son", "A stone pool with a spring in it. The fountain's quiet cousin."],      // PASS-17R: shorter
  "rome.forum.spring.use": ["son", "Splash my face? ...COLD. Two out of ten. I'm extremely awake."],      // PASS-17R: not every score is a ten
  "rome.forum.spring.coin": ["son", "You don't move somebody's wish to a different pool."],
  "rome.forum.garlands.look": ["son", "Purple flowers, and crowns of them. Smells like Grandma's bathroom."],      // PASS-17R: shorter
  "rome.forum.garlands.use": ["phyllis", "Hands off the merchandise, child. Smell with your nose. That part's free."],
  "rome.forum.tuscan.look": ["son", "A street going downhill. Smells like river. And a little like cows."],
  "rome.forum.julia.look": ["son", "Arches, half brand new, half scaffolding. Like my science project."],      // PASS-17R: shorter
  "rome.forum.scaffold.look": ["son", "Scaffolding on the end. Rome's under construction. All of it."],
  "rome.forum.scaffold.use": ["son", "Climb it? Mom has a rule about that. Same as her rule about everything."],
  "rome.forum.puteal.look": ["son", "A round stone ring in the pavement. A well with no well in it."],
  "rome.forum.puteal.use": ["son", "Everybody goes around it. So do I. There's always a story."],
  "rome.forum.table.look": ["son", "Coins on a table, and nobody minding it. Somebody's coming RIGHT back."],
  "rome.forum.table.use": ["son", "Not touching. I've got a wish to worry about."],
  "rome.forum.table.coin": ["son", "Leave the wish on the money table? It's a wish, not a deposit."],
  "rome.forum.table.quarter": ["son", "Swap George for silver while nobody's looking? That's why I won't."],
  "rome.forum.statues.look": ["son", "Statues up where only pigeons reach. The pigeons are winning."],
  "rome.forum.rostra.look": ["son", "A long stone stage, bronze beaks out front, and statues talking to nobody."],
  "rome.forum.rostra.use": ["son", "Make a speech? I'd talk about snacks. Nobody would leave."],
  "rome.forum.saturn.look": ["son", "That's MY temple, way down there. My door guy is a dot."],
  "rome.forum.saturn.look2": ["son", "The dot just folded its arms. I can tell from HERE."],
  "rome.forum.jupiter.look": ["son", "A gold roof on the hill, so you can see it from everywhere."],
  "rome.forum.jupiter.look2": ["son", "It flashes in the sun. Whoever polishes it has the best job in Rome."],
  "rome.forum.moneta.look": ["son", "Another temple. Rome does temples like candles on a cake."],
  "rome.forum.moneta.look2": ["son", "Two bumps, two temples. I'd put a snack bar on the second one."],
  "rome.forum.records.look": ["son", "A long row of arches built into the hill. A giant filing cabinet."],
  "rome.forum.paullus.look": ["son", "Columns, with shops underneath. Rome has a MALL."],
  "rome.forum.paullus.look2": ["son", "Buying, selling, or arguing about it. Definitely a mall."],
  "rome.forum.site.look": ["son", "A fence round a giant hole. Something was here. Something's GOING to be."],      // PASS-17R: shorter (the picture shows the new stone)
  "rome.forum.site.look2": ["son", "Old stones out, new stones in. Rome is getting a new tooth."],
  "rome.forum.site.use": ["son", "The fence says keep out. It doesn't SAY it. It's just that kind of fence."],
  "rome.forum.crane.look": ["son", "A crane with a wheel you walk inside. Like a hamster. A STRONG hamster."],
  "rome.forum.crane.use": ["son", "Not touching the crane. It's a REALLY grown-up toy."],
  "rome.forum.pigeons.look": ["son", "City pigeons. Same as the steps pigeons. They commute."],
  "rome.forum.pigeons.use": ["son", "Not chasing them. You don't chase commuters."],

  // ---------- the Gaul (NEW 2, Nobody Will Show Him; gaulTree) ----------
  // Gaius Iulius Litumarus, of Nemausus in the Province, made a senator by the dictator: careful, correct, a little
  // old-fashioned, every word chosen, like a man walking on ice; dry, never bitter for long. He tells Rome's joke about
  // himself before anybody else can, and nobody mocks him: the joke is Rome's. He is going to an ordinary meeting.
  "rome.gaul.look": ["son", "A giant guy in a too-short bedsheet. Like Dad in my sleeping bag."],
  "rome.gaul.look2": ["son", "He asks people something. They walk faster. Not nice, Rome."],
  // four ways in
  "rome.gaul.opt.hi": ["son", "Are you lost? I'm lost. We could be lost together."],
  "rome.gaul.hi": ["gaul", "...You stopped. In all this square, you are the first."],
  "rome.gaul.opt.short": ["son", "Excuse me? Your bedsheet's too short. Your knees are out."],
  "rome.gaul.short.1": ["gaul", "It is a toga. It is my first. I was told togas were difficult."],
  "rome.gaul.short.2": ["gaul", "I was not told they were difficult in this particular way."],
  "rome.gaul.short.2.b": ["son", "You're doing great. Mostly."],      // PASS-19R2: new (breaks a run of three; the Son swerves)
  "rome.gaul.opt.viking": ["son", "Whoa. Are you a VIKING?"],
  "rome.gaul.viking": ["gaul", "I do not know that word. I am a Gaul. For Rome, that is usually enough."],
  "rome.gaul.opt.way": ["son", "Excuse me, sir. Which way is... anywhere?"],
  "rome.gaul.way": ["gaul", "Child, you have found the one man in Rome who cannot tell you."],
  // who he is, the notice put up in the city (Suetonius's placard), and his question
  "rome.gaul.who.1": ["gaul", "Gaius Iulius Litumarus, of Nemausus. Lately, a senator of Rome."],
  "rome.gaul.who.son": ["son", "A senator! I'm calling you Big Senator."],
  "rome.gaul.who.2": ["gaul", "My first meeting. Twelve Romans I asked. Twelve smiled, and walked faster."],
  "rome.gaul.who.3": ["gaul", "A notice says nobody is to show the new senator the way. It is a joke. I am it."],
  "rome.gaul.who.4": ["son", "A prank on the new kid, on his first day. The worst kind."],
  "rome.gaul.who.6": ["gaul", "So I ask you: where does the Senate meet today?"],
  "rome.gaul.again": ["gaul", "The boy who stops. Where does the Senate meet today?"],
  // the wrong answers, as the Son's choices
  "rome.gaul.opt.house": ["son", "In the senate house!"],
  "rome.gaul.house.1": ["gaul", "There is the senate house. It is a hole with men in it."],
  "rome.gaul.house.son": ["son", "...So it's more of a senate hole."],
  "rome.gaul.house.2": ["gaul", "It is still a hole. I have looked again. Holes are like that."],
  "rome.gaul.opt.capitol": ["son", "Up on the Capitol? With the gold roof?"],
  "rome.gaul.capitol.1": ["gaul", "I have been up. There are geese."],
  "rome.gaul.capitol.2": ["gaul", "They did not show me the way either. They showed me the way down."],
  "rome.gaul.capitol.3": ["gaul", "The geese, child. I said the geese."],
  "rome.gaul.opt.geese": ["son", "Up on the Capitol? Past the attack chickens?"],
  "rome.gaul.geese.1": ["gaul", "You have met them. Then you know why I came down again."],
  "rome.gaul.geese.2": ["gaul", "We do not speak of the geese, child. We have both been up there."],
  "rome.gaul.opt.caesar": ["son", "At Caesar's house? He's the boss, right?"],
  "rome.gaul.caesar.1": ["gaul", "I have been there. Nine hundred senators and one porter."],
  "rome.gaul.caesar.son": ["son", "...That's a LONG line."],
  "rome.gaul.caesar.2": ["gaul", "Still nine hundred. Still one porter."],
  "rome.gaul.opt.dunno": ["son", "I don't know. Honestly. I'm new here."],
  "rome.gaul.dunno.1": ["gaul", "Then you are a true Roman. Thank you."],
  "rome.gaul.dunno.2": ["gaul", "Still a true Roman. You are very consistent."],
  "rome.gaul.dunno.3": ["gaul", "...You are the most Roman person I have met today."],
  // the right one, once he has heard it (the senator's speech, or Walnut)
  "rome.gaul.opt.pompey": ["son", "In Pompey's hall, by his theater."],
  "rome.gaul.pompey": ["gaul", "Pompey's theater? The stone one, with a temple on its seats?"],
  "rome.gaul.saw.son": ["son", "Yes! I saw it from the top of the hill."],
  "rome.gaul.saw": ["gaul", "From a boy who has seen it. That is more than the Senate gave me."],
  "rome.gaul.heard.son": ["son", "The senator told me. He's giving a speech there. About drains."],
  "rome.gaul.heard": ["gaul", "A man does not invent a speech about drains. I believe you."],
  "rome.gaul.answered.1": ["gaul", "Pompey's hall. Of course. Even Rome cannot meet in a hole."],
  "rome.gaul.answered.1.b": ["son", "So... I helped?"],      // PASS-19R2: new (breaks a run of three; sets up his thanks)
  "rome.gaul.answered.2": ["gaul", "The joke is spoiled, child, and I thank you for spoiling it."],
  "rome.gaul.welcome": ["gaul", "My guide. Pompey's hall, by the theater. I have not forgotten."],
  // answered, and waiting: he will not cross Rome with his knees out
  "rome.gaul.opt.why": ["son", "So why are you still here? You know the way now."],
  "rome.gaul.why.1": ["gaul", "A new man does not arrive first. It looks keen. I will go when the others go."],
  "rome.gaul.why.2": ["gaul", "I would rather not cross Rome with my knees out. Rome has seen enough."],
  "rome.gaul.why.3": ["gaul", "My knees, child. We have spoken of my knees."],
  "rome.gaul.opt.remind": ["son", "Pompey's hall, by the theater. Just checking."],
  "rome.gaul.remind.1": ["gaul", "I say it to myself as I walk. It is the Latin I am surest of."],
  "rome.gaul.remind.2": ["gaul", "You may stop checking, child. I will not stop saying it."],
  // the laugh: the city's song about Gauls, told by the Gaul himself, in his own words (the verses are never quoted)
  "rome.gaul.opt.song": ["son", "Why would anybody put up a notice like THAT?"],
  "rome.gaul.song.1": ["gaul", "It is funny, if you are a Roman. There is a song, too."],
  "rome.gaul.song.2": ["gaul", "Trousers off, broad stripe on. Nine times I have heard it. It does not improve."],
  "rome.gaul.song.son": ["son", "You don't make up songs about the new kid. That's the first rule."],
  "rome.gaul.song.3": ["gaul", "Rome is very old, child. It has had time to forget the first rule."],
  "rome.gaul.song.4": ["gaul", "Ten times now. I caught myself humming it this morning. Tell no one."],
  "rome.gaul.opt.mustache": ["son", "Can I just say? Ten out of ten on the mustache."],
  "rome.gaul.mustache.1": ["gaul", "In Gaul every man of rank wears one. In Rome they shave, and stare."],
  "rome.gaul.mustache.son": ["son", "My dad tried a mustache once. Mom made it leave."],
  "rome.gaul.mustache.2": ["gaul", "...Your mother and the Senate would understand each other."],
  // the togas: once he has the Gaul's toga AND has answered, in either order
  "rome.gaul.opt.swap": ["son", "Big Senator! That toga's my senator's. I've got yours. Swap?"],
  "rome.gaul.swap.first": ["gaul", "First the Senate. Then my knees. Where does the Senate meet, child?"],
  "rome.gaul.swap.first.2": ["gaul", "My knees can wait. The Senate will not. Where does it meet?"],
  "rome.gaul.swap.1": ["gaul", "...I had decided Roman togas were made to be ridiculous."],
  "rome.gaul.swap.2": ["gaul", "There. Now I look like a senator. All that is left is to be one."],
  "rome.gaul.swap.son": ["son", "Swapped. One bedsheet, senator-sized, for my senator."],
  // his going
  "rome.gaul.leave.1": ["gaul", "If anyone asks, a Roman showed me the way."],
  "rome.gaul.leave.son": ["son", "I'm not a Roman."],
  "rome.gaul.leave.2": ["gaul", "Then nobody will be blamed."],
  // the ways out
  "rome.gaul.opt.bye": ["son", "I'll find out where they meet. Don't move! Or move a LITTLE."],
  "rome.gaul.bye.1": ["gaul", "I will move a little. Along the fence, and back."],
  "rome.gaul.bye.2": ["gaul", "Along the fence, and back. I am becoming very good at it."],
  "rome.gaul.opt.byewait": ["son", "I'll see what I can do about your knees. Don't go first!"],
  "rome.gaul.byewait.1": ["gaul", "I would not dream of it. Rome would put up a notice."],
  "rome.gaul.byewait.2": ["gaul", "I am not going first. I am barely going at all."],
  // things carried, shown to him (the Gaul's toga starts his talk)
  "rome.gaul.toga": ["gaul", "Another toga. This one they gave me, and I do not recommend it."],
  "rome.gaul.coin": ["gaul", "He gave me his names. I did not expect his face as well."],
  "rome.gaul.quarter": ["gaul", "A man with his hair tied back. In Nemausus we would call that short."],
  "rome.gaul.phone": ["gaul", "A small dark mirror. It shows a large man in a short toga. I knew."],
  "rome.gaul.gum": ["gaul", "I am trying to look like a senator. Chewing would not help."],
  "rome.gaul.breakfast": ["gaul", "A senator does not eat in the street, I am told. I am told a great deal."],
  "rome.gaul.incense": ["gaul", "For which god? I am still learning the names of the people."],
  "rome.gaul.lamp": ["gaul", "Carried like an egg. Somebody loves whoever that is for."],

  // ---------- Phyllis (NEW 4, Interest Is Extra Wishes, her side; phyllisTree) ----------
  // Fannia Phyllis, a Greek freedwoman, a widow, on her low stool among her baskets at the foot of Castor's temple. Fast
  // and warm, a seller's patter, sharp with fools, soft about her son. Anna Perenna's feast is today.
  "rome.phyllis.look": ["son", "A little lady in a nest of flowers, making crowns. Fast."],      // PASS-17R: not every look is a ten
  "rome.phyllis.look2": ["son", "A bundle in her lap, wrapped like an egg. She hasn't sold that one."],
  "rome.phyllis.look3": ["son", "No bundle now. A half-made crown, and twice as fast."],
  "rome.phyllis.cry": ["phyllis", "Myrtle for your sweetheart. Garlands for Anna Perenna!"],
  "rome.phyllis.again": ["phyllis", "Back again? Violets don't keep, child. Nor do customers who only look."],
  "rome.phyllis.opt.anna": ["son", "Who's Anna Perenna? Do I need to get her a garland?"],
  "rome.phyllis.anna.1": ["phyllis", "Child! Anna Perenna's feast. Half the city picnics by the river today."],
  "rome.phyllis.anna.2": ["phyllis", "And every one wants a garland. I can't leave my baskets a moment."],
  "rome.phyllis.anna.3": ["phyllis", "Still the busiest morning. Buy, or stand aside for those who do."],
  "rome.phyllis.opt.sweetheart": ["son", "Myrtle for my sweetheart? I don't even have a DOG."],
  "rome.phyllis.sweetheart.1": ["phyllis", "No dog, no sweetheart. Then violets for your mother. Every boy has one."],
  "rome.phyllis.sweetheart.son": ["son", "...Mom would like that. She's a REALLY long way away."],
  "rome.phyllis.sweetheart.2": ["phyllis", "Then smell them for her. She'll never know you didn't buy any."],
  "rome.phyllis.opt.son": ["son", "Do you have kids? I'm somebody's kid. Just not anybody's from around here."],
  "rome.phyllis.son.1": ["phyllis", "One. Felix. He loads the barges across the river, below the stone bridge."],
  "rome.phyllis.son.2": ["phyllis", "His name is down for Corinth. The dictator builds it for freedmen, like me."],
  "rome.phyllis.son.2.b": ["son", "A whole city?"],      // PASS-19R2: new (breaks a run of three)
  "rome.phyllis.son.3": ["phyllis", "A city that has lain empty a hundred years. Imagine. Not a grandmother in it."],
  "rome.phyllis.son.son": ["son", "Corinth. That rings a bell. A big one. ...It'll come to me."],
  "rome.phyllis.son.4": ["phyllis", "Felix, Corinth. You're as bad as I am, child. I talk of nothing else."],
  "rome.phyllis.opt.twins": ["son", "Whose temple is that? The big one you're sitting under?"],
  "rome.phyllis.twins.1": ["phyllis", "Castor's, and his brother's. The Twins."],
  "rome.phyllis.twins.2": ["phyllis", "The city's true weights are in there. Nobody can cheat you. Not even me."],
  "rome.phyllis.twins.son": ["son", "A temple that checks your groceries."],
  // the wish (the lever): the boy has the coin, and Walnut has said whose it was
  "rome.phyllis.opt.wish": ["son", "Walnut says the fountain wish was yours. I borrowed it. I'm asking now."],
  "rome.phyllis.wish.1": ["phyllis", "...My wish. Yes. I threw it in at first light, for my boy."],
  "rome.phyllis.wish.2": ["phyllis", "The first new silver I have held in years. The dictator's own head on it."],
  "rome.phyllis.wish.2.b": ["son", "What did you wish?"],      // PASS-19R2: new (want; breaks a run of four)
  "rome.phyllis.wish.3": ["phyllis", "I wished to give Felix this little lamp before he sails. For Corinth."],
  "rome.phyllis.wish.4": ["phyllis", "And to hear him say goodbye. He can't leave his barge. I can't leave my baskets."],
  "rome.phyllis.wish.again": ["phyllis", "The lamp is still in my lap, child, and Felix still across the river."],
  "rome.phyllis.opt.giveback": ["son", "Then you should have it back. Here. It's yours."],
  "rome.phyllis.giveback": ["phyllis", "A wish once thrown is not mine to take back. But it was for my boy."],
  "rome.phyllis.giveback.2": ["phyllis", "Thrown is thrown, child. Put it away."],
  "rome.phyllis.opt.quarter": ["son", "Or I could pay you! With a quarter. It's got a bird on it."],
  "rome.phyllis.quarter": ["phyllis", "A bird? For a wish? Child."],
  "rome.phyllis.quarter.2": ["phyllis", "Still a bird. Still a wish. Still no."],
  "rome.phyllis.opt.take": ["son", "I could take the lamp to him! I'm great at errands."],
  "rome.phyllis.take.1": ["phyllis", "Would you? Down the Tuscan street, child, and over the stone bridge."],
  "rome.phyllis.take.2": ["phyllis", "Tell him his mother says come before he sails. He will know the rest."],
  "rome.phyllis.lamped": ["son", "Lamp delivery. I'll carry it like an egg."],
  "rome.phyllis.opt.think": ["son", "Can I think about it? I think fast. Mostly while walking."],
  "rome.phyllis.think": ["phyllis", "Think, then. But Corinth will not wait for you to finish."],
  // the lamp on its way
  "rome.phyllis.waiting": ["phyllis", "Did you find him? He has my face, and his father's hurry."],
  "rome.phyllis.opt.where": ["son", "Where's Felix again? Just checking."],
  "rome.phyllis.where.1": ["phyllis", "Across the river, child, at the barges below the stone bridge."],
  "rome.phyllis.where.2": ["phyllis", "The Tuscan street. The bridge. The barges. The big sunburnt one."],
  "rome.phyllis.opt.lampback": ["son", "Do you want the lamp back? You could keep it till he comes."],
  "rome.phyllis.lampback": ["phyllis", "Then it would be my lamp, and my wish still wishing. Take it to him."],
  "rome.phyllis.opt.byewait": ["son", "Lamp delivery, back on."],
  "rome.phyllis.byewait": ["phyllis", "Mind it on the bridge."],
  // Felix's word, brought back: her leave (decision 7)
  "rome.phyllis.word": ["phyllis", "You found him? Don't keep an old woman waiting, child."],
  "rome.phyllis.opt.news": ["son", "He'll come at the ninth hour. And he'll light it in Corinth."],
  "rome.phyllis.news.1": ["phyllis", "...The ninth hour."],
  "rome.phyllis.news.2": ["phyllis", "Then the wish is answered, and it was a good one."],
  "rome.phyllis.news.2.b": ["son", "Can I keep borrowing the coin?"],      // PASS-19R2: new (want: he needs her leave for the toss; breaks a run of three)
  "rome.phyllis.news.3": ["phyllis", "Keep the coin, child. It has done its work, and it was borrowed honestly."],
  "rome.phyllis.opt.guess": ["son", "Guess!"],
  "rome.phyllis.guess": ["phyllis", "Child."],
  "rome.phyllis.granted.son": ["son", "Borrowed. Paid back. With interest. I TOLD Walnut interest is extra wishes."],
  "rome.phyllis.done": ["phyllis", "I sell twice as fast now, child. An answered wish is good for trade."],
  // the ways out
  "rome.phyllis.opt.bye": ["son", "I'll go stand over there and smell things for free."],
  "rome.phyllis.bye.1": ["phyllis", "Go on. The bees do the same, and I have never sold to a bee."],
  "rome.phyllis.bye.2": ["phyllis", "Mind my violets as you go."],
  // things carried, shown to her (the coin, the quarter and the lamp start her talk)
  "rome.phyllis.gaultoga": ["phyllis", "That is not a garland, child. That is a sail."],
  "rome.phyllis.toga": ["phyllis", "Keep that off my violets. Senators flatten enough of them."],
  "rome.phyllis.breakfast": ["phyllis", "Sausage, by my violets? They'll smell of it all day."],

  // ================= ROME-13W: rome-capitol: the Capitol, the precinct of Jupiter Best and Greatest =================
  // The top of the hill: the great temple, the kings' statues, the sacred geese of Juno, and over the wall the whole
  // city. Reached from the steps' right edge once he knows it is B.C.

  // ---------- arrival (the first time: rome.sawCapitol) ----------
  "rome.capitol.arrive.1": ["son", "The temple on the hill! Would climb. DID climb."],
  "rome.capitol.arrive.3": ["son", "And a kid on a statue, surrounded by geese. A whole situation."],

  // ---------- the things in it ----------
  // (The look at the theater is the boy seeing Pompey's theater without knowing its name: it sets rome.sawTheater, and
  // the Gaul names it later, when the boy can say "I saw it from the top of the hill!")
  "rome.capitol.temple.look": ["son", "Giant columns, gold roof. Rome is showing off."],
  "rome.capitol.temple.use": ["son", "Go in? You don't just walk into somebody's room. Even a god's."],
  "rome.capitol.name.look": ["son", "Big letters across the front: Q LVTATIVS CATVLVS. Rome is STILL out of U's."],
  "rome.capitol.roof.look": ["son", "Somebody put a gold roof on a building. On PURPOSE."],
  "rome.capitol.doors.look": ["son", "Something huge and gold sits way in the back. I'll let it."],
  "rome.capitol.altar.look": ["son", "A stone barbecue the size of a minivan. Dad would poke it."],
  "rome.capitol.altar.use": ["son", "Not touching it. Dad's rule. The one he breaks."],
  "rome.capitol.altar.incense": ["son", "This is for Saturn, down the hill. Wrong god, wrong barbecue."],
  "rome.capitol.chariot.look": ["son", "A bronze chariot. Nobody driving. Valet parking for gods."],
  "rome.capitol.chariot.use": ["son", "Climb in? No seats. Standing room only."],
  "rome.capitol.world.look": ["son", "A bronze guy on a giant bronze ball. Big Sis would have a footnote."],
  "rome.capitol.kings.look": ["son", "A row of old statues, and one guy with a sword out. He looks busy."],
  "rome.capitol.kings.look2": ["son", "They look like they own the hill and they'd like you off it."],
  "rome.capitol.brutus.look": ["son", "Writing scratched on his base. In Rome, if it stands still, it gets written on."],
  "rome.capitol.dictator.look": ["son", "The new one in the row: the guy from my coin. He's EVERYWHERE today."],
  "rome.capitol.tablets.look": ["son", "Bronze pages on stone posts. Rome LOVES terms and conditions."],
  "rome.capitol.tablets.use": ["son", "Read them? They're in Latin. And tiny. That's double homework."],
  "rome.capitol.pen.look": ["son", "A goose pen with no geese in it. They're all out. Working."],
  "rome.capitol.pen.use": ["son", "Open the gate? It IS open. The geese just don't want to go in."],
  "rome.capitol.hut.look": ["son", "A round grass-roof hut by Rome's biggest temple. Somebody's grandpa won't sell."],
  "rome.capitol.hut.use": ["son", "Knock? ...Nobody's been home for a LONG time."],
  "rome.capitol.view.look": ["son", "The river, an island with a temple, and the whole city. All roofs."],
  "rome.capitol.theater.look": ["son", "A stone half-circle, a temple on top. Biggest bleachers EVER."],
  "rome.capitol.theater.look2": ["son", "You'd need a snack halfway up."],
  "rome.capitol.janiculum.look": ["son", "A long hill across the river. The trees bring their own shade."],
  "rome.capitol.moneta.look": ["son", "Two bumps, a temple on each. Like a camel that's really into temples."],

  // ---------- the geese (NEW 3, Juno's Geese: every wrong try, and the stomp) ----------
  // While they guard the statue's base, each wrong try gets a hiss. Once the goose-keeper has told his tale
  // (rome.knowsGeese) a click on them is the stomp. After it (rome.geeseGone) they are in their pen: .penned.
  "rome.geese.look": ["son", "Geese all round the statue. The kid's surrounded. By attack chickens."],
  "rome.geese.look2": ["son", "The kid moves a foot, every neck comes out. A hiss alarm."],
  "rome.geese.call": ["son", "Here, goosey goosey... They hissed at me. In stereo."],
  "rome.geese.shoo": ["son", "SHOO. ...They didn't shoo. They're not shooers."],
  "rome.geese.gum": ["son", "No gum for sacred geese. They'd never get it off their beaks."],
  "rome.geese.quarter": ["son", "They don't want a bird. They ARE birds."],
  "rome.geese.coin": ["son", "Bribing geese. That's a new low. Even for me."],
  "rome.geese.phone": ["son", "They hissed at the phone. That's more than it's done all day."],
  "rome.geese.toga": ["son", "A toga over sacred geese? They'd honk under it forever."],
  "rome.geese.gaultoga": ["son", "A Gaul's toga over them? I'd lose the geese, the toga, and me."],
  "rome.geese.lamp": ["son", "Not Felix's lamp. Phyllis would know. From across the river."],
  "rome.geese.tunic": ["son", "Wave the tunic? I'd bring back a tunic AND an apology."],
  // the stomp (the anser tree's `stomp` hook, or a click on the geese after the tale), in this order: the boy's line; his
  // sneakers flash; the geese run for their pen; Titus hops down; the breakfast; Titus runs home; the goose-keeper
  "rome.geese.stomp": ["son", "Anything strange? I'm the strangest thing in Rome. Watch my feet."],
  "rome.titus.down": ["titus", "I wasn't scared. I was SITTING."],
  "rome.titus.give": ["titus", "Take it to old Arruns, I'm going home before Father sends the geese."],
  "rome.titus.give.son": ["son", "One kid, one breakfast. Zero geese."],
  "rome.titus.run": ["titus", "Your shoes are the best thing on this hill, and I've seen the gold roof!"],
  "rome.anser.last": ["anser", "That is the most noise they have made since the Gauls."],
  // afterwards: the geese (or their pen) looked at, and tried
  "rome.geese.penned": ["son", "Every goose back in the pen, eating. Professionals."],
  "rome.geese.penned.use": ["son", "I'm not going near them. We had a moment. It's over."],

  // ---------- Titus, the keeper's boy (titusTree) ----------
  // About eleven, on top of a statue base among the kings, the soothsayer's breakfast in a knotted cloth in his lap.
  // He talks like his father, without stopping for breath, and like a boy: boasting, then honest.
  "rome.titus.look": ["son", "A kid on a statue, pretending he meant to be up there."],
  "rome.titus.look2": ["son", "He's pretending to be a statue. A goose looked at him. He stopped."],
  // ways in (the first, once his father has told the boy about him)
  "rome.titus.opt.sent": ["son", "Are you Titus? Your dad sent me. He says the old one will be fainting."],
  "rome.titus.sent": ["titus", "Father sent YOU? ...He's in a state, then. He makes extra sausages."],
  "rome.titus.opt.stuck": ["son", "Are you stuck up there?"],
  "rome.titus.stuck.1": ["titus", "Stuck? Me? I'm SITTING, I like sitting, I can see the whole city."],
  "rome.titus.stuck.2": ["titus", "I've been sitting since first light. On purpose. Mostly on purpose."],
  "rome.titus.stuck.2.b": ["son", "Mostly?"],      // PASS-19R2: new (breaks a run of five; the Son swerves)
  "rome.titus.opt.statue": ["son", "Whoa. A statue that blinks."],
  "rome.titus.statue": ["titus", "Statues don't have breakfasts. I've got one. ...Not mine. But I've got it."],
  "rome.titus.opt.sausage": ["son", "Is that... sausage? I can smell sausage from here."],
  "rome.titus.sausage": ["titus", "Don't look at it like that, it's not mine, it's the soothsayer's."],
  "rome.titus.opt.jump": ["son", "Just jump down! It's not THAT high."],
  "rome.titus.jump.1": ["titus", "Over THEM? They bite like Father's creditors."],
  // whose boy he is, and whose breakfast (rome.knowsBoy)
  "rome.titus.who.1": ["titus", "I'm Titus, Father keeps the snack bar by the fountain, everybody owes him."],
  "rome.titus.who.1.b": ["son", "The snack bar! I've smelled it."],      // PASS-19R2: new (breaks a run of four)
  "rome.titus.who.2": ["titus", "Old Arruns the soothsayer's breakfast, I was taking it, and the ewe went by."],
  "rome.titus.who.3": ["titus", "Every Ides I go after her, then the geese came, now I'm sitting."],
  "rome.titus.again": ["titus", "Still sitting, still FINE, did you bring anything for geese?"],
  "rome.titus.opt.geese": ["son", "What's the deal with the geese?"],
  "rome.titus.geese.1": ["titus", "They don't like feet. Watch."],
  "rome.titus.geese.2": ["titus", "See? Foot down, every neck out. I'm not scared. I'm keeping my feet."],
  "rome.titus.geese.again": ["titus", "Still don't like feet. I checked again. Don't make me check again."],
  "rome.titus.opt.ewe": ["son", "What ewe? You keep saying ewe."],
  "rome.titus.ewe.1": ["titus", "The Ides sheep, up to Jupiter every single Ides, and I go after her."],
  "rome.titus.ewe.2": ["titus", "She had ribbons. She went up the hill like a senator."],
  "rome.titus.opt.father": ["son", "Does your dad know you're up here?"],
  "rome.titus.father.1": ["titus", "Father knows everything, Father's going to talk at me for a WEEK."],
  "rome.titus.father.2": ["titus", "...Is he worried? He worries loud."],
  "rome.titus.father.3": ["titus", "Tell him I'm fine. Not about the geese. ...A little about the geese."],
  "rome.titus.opt.jump2": ["son", "Seriously, jump. I'll catch you. Probably."],
  "rome.titus.jump.2": ["titus", "You'd catch me, they'd catch you, and we'd both be down there. With THEM."],
  "rome.titus.jump.3": ["titus", "No."],
  "rome.titus.opt.help": ["son", "Want me to get you down?"],
  "rome.titus.help.1": ["titus", "I don't need getting down, I'm FINE, I'm sitting, I like it up here."],
  "rome.titus.help.2": ["titus", "...Ask old Anser, he feeds them, he talks about them all day."],
  "rome.titus.help.3": ["titus", "Old Anser, with the basket. Ask him about geese, you'll be there till sundown."],
  "rome.titus.opt.bye": ["son", "Stay right there. ...Sorry. You know what I mean."],
  "rome.titus.bye.1": ["titus", "I'm not going ANYWHERE. That's the whole thing."],
  "rome.titus.bye.2": ["titus", "Still here."],
  // things carried, shown to him on his base
  "rome.titus.toga": ["titus", "Throw me a toga? I'm not cold, I'm STUCK. ...I'm not stuck. I'm sitting."],
  "rome.titus.coin": ["titus", "New silver! Father would bite it, Father bites everything."],
  "rome.titus.quarter": ["titus", "A bird on a coin, that's lucky, unless it's a goose. Hide it."],
  "rome.titus.gum": ["titus", "No, don't, a goose will catch it, then it'll have gum AND opinions."],

  // ---------- the goose-keeper (anserTree: NEW 3's clue) ----------
  // Titus Rubrius Anser, about sixty, who feeds Juno's geese for the Republic. Mournful, devoted, full of the story of
  // the Gauls, which he tells to anyone, long ago and with no year: it is the instructions.
  "rome.anser.look": ["son", "A sad man with a stick. He's never once poked a goose."],
  "rome.anser.look2": ["son", "He counts the geese. Different number every time. Geese move."],
  // ways in (every one of his answers comes round to the night the geese saved the city)
  "rome.anser.opt.move": ["son", "Are those your geese? Can you move them? There's a kid up there."],
  "rome.anser.move.1": ["anser", "Sacred birds. I feed them. I do not argue with them."],
  "rome.anser.move.2": ["anser", "Nobody argues with the geese that saved the city. Least of all me."],
  "rome.anser.opt.chickens": ["son", "Excuse me, sir. Are those attack chickens?"],
  "rome.anser.chickens.1": ["anser", "The sacred geese of Juno, child. They saved this city once."],
  "rome.anser.chickens.2": ["anser", "...Attack chickens. I will not tell them you said that."],
  "rome.anser.opt.name": ["son", "What's your name? I'm collecting names. I've got Walnut."],
  "rome.anser.name.1": ["anser", "Titus Rubrius Anser. Anser means goose."],
  "rome.anser.name.2": ["anser", "It was my grandfather's name before it was my job. Nobody believes it."],
  "rome.anser.name.son": ["son", "A goose guy called Goose! Mister Goose. Top of my collection."],      // PASS-17R: his collection of names comes round again
  "rome.anser.name.3": ["anser", "...Mister Goose. These geese saved the city, child."],
  "rome.anser.opt.feed": ["son", "Do you feed them every day? That's a LOT of geese."],
  "rome.anser.feed.1": ["anser", "Every morning, on the Republic's grain. Since they saved the city."],
  "rome.anser.feed.2": ["anser", "The Republic does not pay for their manners."],
  "rome.anser.again": ["anser", "The boy who collects names. The geese remember everybody."],
  // the tale (rome.knowsGeese): the Gauls who climbed the Capitol by night, and the geese that woke Manlius
  "rome.anser.opt.saved": ["son", "Wait. Geese SAVED the city? How do geese save a city?"],
  "rome.anser.tale.1": ["anser", "Long ago, the Gauls took this city. All of it, but this hill."],
  "rome.anser.tale.2": ["anser", "One night they climbed the rock below that wall. Not even the dogs woke."],
  "rome.anser.tale.2.b": ["son", "Not even the dogs?"],      // PASS-19R2: new (breaks a run of six)
  "rome.anser.tale.3": ["anser", "But Juno's geese woke. They cried out, and woke Manlius."],
  "rome.anser.tale.4": ["anser", "Manlius ran to the edge, and the Gauls went down faster than they came up."],
  "rome.anser.tale.4.b": ["son", "Attack chickens. I knew it."],      // PASS-19R2: new (breaks a run of six; the Son's name for them pays off)
  "rome.anser.tale.6": ["anser", "They cannot abide anything strange. They shout at it, and then they run."],
  "rome.anser.tale.son": ["son", "Anything STRANGE. ...I've got my thinking face on."],
  "rome.anser.tale.again.1": ["anser", "Gladly. Long ago, the Gauls took this city, all of it but this hill..."],
  "rome.anser.tale.again.son": ["son", "Geese, Gauls, Manlius, the edge of the hill. I REMEMBER."],
  "rome.anser.tale.again.2": ["anser", "...You were listening. Thirty years, and nobody listens."],
  "rome.anser.tale.more": ["anser", "Long ago..."],
  "rome.anser.tale.more.son": ["son", "I'm going to stop asking you that. For both of us."],
  // the lever: the boy puts the tale to the test (the stomp, above)
  "rome.anser.opt.test": ["son", "Mister Goose? You might want to hold on to your basket."],
  "rome.anser.opt.move2": ["son", "Can you move them, though? Just a little? For the kid?"],
  "rome.anser.move.3": ["anser", "Thirty years I have fed them. I have never once won an argument."],
  "rome.anser.move.4": ["anser", "No, child."],
  "rome.anser.move.5": ["anser", "They are not my geese, child. They are Juno's. She has not asked me."],
  "rome.anser.opt.dogs": ["son", "Who guards the hill at night? The geese?"],
  "rome.anser.dogs.1": ["anser", "Dogs, at night. The Republic keeps dogs for thieves."],
  "rome.anser.dogs.2": ["anser", "Between you and me, the dogs sleep. The geese never do."],
  "rome.anser.dogs.3": ["anser", "The dogs. Asleep, I expect. It is daytime. It is always the geese."],
  "rome.anser.opt.moneta": ["son", "What's that other temple? On the hill's other bump?"],
  "rome.anser.moneta.1": ["anser", "Juno's too. Juno Moneta, the Warner. They make the money there."],
  "rome.anser.moneta.son": ["son", "Moneta. MONEY-ta. ...I just figured out the word money."],
  "rome.anser.moneta.2": ["anser", "I do not know what you figured out, child. You look very pleased."],
  "rome.anser.moneta.3": ["anser", "Moneta. The money, and the warning. Juno keeps an eye on both."],
  "rome.anser.opt.bye": ["son", "Say bye to the geese for me, Mister Goose. From a distance."],
  "rome.anser.bye.1": ["anser", "I will tell them. They will not care."],
  "rome.anser.bye.2": ["anser", "They still will not care."],
  // after the stomp
  "rome.anser.after": ["anser", "Back in their pen, eating. That is geese. I am still shaking."],
  "rome.anser.opt.sorry": ["son", "Sorry about the noise. And the running. And the honking."],
  "rome.anser.sorry": ["anser", "Do not be sorry. Thirty years I have told that story. Today somebody USED it."],
  "rome.anser.bye.after": ["anser", "Go gently, child. And not near my pen."],
  // things carried, shown to him
  "rome.anser.toga": ["anser", "Not over my geese. They would honk at the dark all day."],
  "rome.anser.coin": ["anser", "New silver, from Moneta's. My geese guard the hill. Moneta guards the money."],
  "rome.anser.quarter": ["anser", "A bird on a coin. An eagle, I think. Juno would have preferred a goose."],
  "rome.anser.gum": ["anser", "Not for my geese. I mean it. I will tell the Republic."],
  "rome.anser.breakfast": ["anser", "The soothsayer's. Take it down before the geese remember it."],

  // ================= ROME-13W: rome-tiber: across the Tiber, below the stone bridge =================
  // The right bank, looking downstream: a lane of small houses where a Jewish family lives beside their house of prayer,
  // a hen yard, a landing and a barge, the river in the morning sun. The quiet place of the act (the faith thread).

  // ---------- arrival (the first time: rome.sawTiber): the old man at his window, praying; the hens in a row ----------
  "rome.tiber.arrive.1": ["son", "Boats, a girl with a LOT of hens, and an old man at a window."],
  "rome.tiber.arrive.2": ["son", "He's praying. With his window open. Like Daniel."],
  "rome.tiber.arrive.3": ["son", "I'll wait till he's done. ...I'm getting good at waiting."],

  // ---------- the things in it ----------
  "rome.tiber.river.look": ["son", "Brown and in a hurry. Like a dog after a bath."],
  "rome.tiber.river.use": ["son", "Swim? I'd come out browner than I went in. And in a different town."],      // PASS-17R: the look has "brown and in a hurry" already
  "rome.tiber.river.coin": ["son", "Things that go in the river stay in the river."],
  "rome.tiber.river.quarter": ["son", "Skip a quarter across the Tiber? George would never forgive me."],
  "rome.tiber.barge.look": ["son", "A long flat boat piled with bundles. A floating table."],
  "rome.tiber.barge.use": ["son", "Climb aboard? The boat guy would put me off. Politely. Probably."],
  "rome.tiber.bales.look": ["son", "Rolls of papyrus wrapped in mats. Egyptian paper! Big Sis would sniff it."],
  "rome.tiber.bales.use": ["son", "Lift one? ...Nope. That's why the boat guy has those arms."],
  "rome.tiber.landing.look": ["son", "Stone steps that go right down into the water. Stairs for fish."],
  "rome.tiber.landing.use": ["son", "Go down to the water? Mom would say no. She's not here. Still no."],
  "rome.tiber.farbank.look": ["son", "More hills, more temples. Rome just keeps going."],
  "rome.tiber.road.look": ["son", "A long road along the river. Somebody fancy lives down there."],
  "rome.tiber.gardens.look": ["son", "A long garden wall. Somebody's got a REALLY big backyard."],
  "rome.tiber.house.look": ["son", "A plain little house, hens out front. The old man's."],
  "rome.tiber.house.use": ["son", "Knock? Not on somebody's praying."],
  "rome.tiber.doorpost.look": ["son", "A tiny case on the doorpost. Like a doorbell that doesn't ring."],
  "rome.tiber.doorpost.use": ["son", "Poke it? It's not my door. It looks important in a quiet way."],
  "rome.tiber.window.look": ["son", "An upstairs window, open wide toward the river."],
  "rome.tiber.window.look2": ["son", "His window, still open. He'll be back at midday. He's a three-times-a-day man."],
  "rome.tiber.prayerhouse.look": ["son", "Nothing painted. A door and a bench. Like a library, but for praying."],      // PASS-17R: a boy's way of putting it
  "rome.tiber.prayerhouse.use": ["son", "Go in? It's quiet in there. I'm not quiet."],
  "rome.tiber.bench.look": ["son", "A stone bench. Good for waiting. I'm an expert now."],
  "rome.tiber.bench.use": ["son", "I'll sit. Sitting is the main part of waiting."],
  "rome.tiber.well.look": ["son", "A well. I've learned about coins and water."],
  "rome.tiber.well.coin": ["son", "No more wishes in water. I'm on a break."],
  "rome.tiber.figtree.look": ["son", "A fig tree with baby leaves. A snack tree, still loading. Back in summer."],      // PASS-17R: no Bible fact tacked onto a look
  "rome.tiber.figtree.use": ["son", "Pick a fig? There aren't any yet. Just baby leaves."],
  "rome.tiber.washing.look": ["son", "Washing on a line. The laundry lady would have OPINIONS."],

  // ---------- Mariam's hens (chickens: they stand in a row looking over the river at the city; nobody explains it) ----------
  "rome.hens.look": ["son", "Hens, all in a row, all facing the same way. Over the river. At the city."],
  "rome.hens.look2": ["son", "They haven't moved. Not one. Not even the end one, and she's a wiggler."],
  "rome.hens.use": ["son", "Here, chick chick! ...Not one head turned. They've got somewhere to look."],
  "rome.hens.breakfast": ["son", "Not giving them the chicken man's breakfast. ...They didn't even turn round."],

  // ---------- Eleazar (the faith thread: the design's 6.2; eleazarTree) ----------
  // About sixty-five, born in Jerusalem, carried to Rome a captive when Pompey took the city, long since freed; the date
  // seller's father-in-law. Slow, warm, grave, with a dry humor; calls the Son "child"; never preaches, never hurries,
  // listens more than he talks. He never names Jesus, never says when, never says the promised one is God, says nothing
  // against anybody's gods, and argues with nobody; the Son never tells him what is coming.
  // At his window: the boy waits (the scene), then the old man comes down to his bench.
  "rome.eleazar.look.window": ["son", "An old man at his window, praying. I'm not going to bother him."],
  "rome.eleazar.look.window2": ["son", "I can't hear any words. That's okay. God can."],      // PASS-17R: what a boy would say
  "rome.eleazar.wait": ["son", "Waiting. I'm doing it. Look at me doing it."],
  "rome.eleazar.look": ["son", "He reads his scroll with a finger. Like me with a hard book."],
  "rome.eleazar.look2": ["son", "He keeps looking across the river, then back at his scroll."],
  // the greeting, and the ways in
  "rome.eleazar.peace": ["eleazar", "Peace to you, child."],
  "rome.eleazar.opt.peace": ["son", "Peace to you too, mister."],
  "rome.eleazar.opt.waited": ["son", "I waited the WHOLE time. I didn't fidget once. ...I fidgeted once."],
  "rome.eleazar.waited": ["eleazar", "Twice. But very politely."],
  "rome.eleazar.opt.church": ["son", "Is that your church? The one with the bench?"],
  "rome.eleazar.church": ["eleazar", "A house of prayer."],
  "rome.eleazar.opt.yose": ["son", "Do you know the date seller? Beard, basket, VERY calm?"],
  "rome.eleazar.yose.1": ["eleazar", "Yose. My daughter's husband. Does he say the dates are selling?"],
  "rome.eleazar.yose.son": ["son", "He says Rome always wants dates."],
  "rome.eleazar.yose.2": ["eleazar", "He always says so."],
  "rome.eleazar.who.1": ["eleazar", "I am Eleazar. And who are you, child, who waits so well?"],
  "rome.eleazar.who.son.1": ["son", "My dad's lost. Or I am. One of us is. I'm waiting for him to find me."],
  "rome.eleazar.who.son.2": ["son", "He always comes. He's late sometimes. He calls it making good time."],
  "rome.eleazar.who.2": ["eleazar", "A father who always comes. That is a good thing to wait for."],
  "rome.eleazar.again": ["eleazar", "You came back. Sit, child, if you like. The bench is long."],
  // the window: Daniel 6:10 and Psalm 55:17, told, not quoted
  "rome.eleazar.opt.window": ["son", "What were you doing at the window? With your eyes shut?"],
  "rome.eleazar.window.1": ["eleazar", "Toward Jerusalem, where the Temple is. Evening, morning and midday."],
  "rome.eleazar.window.son": ["son", "Like Daniel! Window open, three times a day. ...No lions, though. Right?"],      // PASS-17R: shorter, and a question to answer
  "rome.eleazar.window.2": ["eleazar", "No lions, child. Only Mariam. ...You have been well taught."],      // PASS-17R: he answers it (Mariam is boss of Grandfather)
  // how he came to Rome: told without bitterness, and a pause
  "rome.eleazar.opt.rome": ["son", "How did you end up in Rome? A wrong turn? My dad takes a LOT of those."],
  "rome.eleazar.rome.1": ["eleazar", "Pompey took Jerusalem nineteen years ago. Many of us were brought here."],
  "rome.eleazar.rome.2": ["eleazar", "I was bought, and I worked, and in time my master set me free."],
  "rome.eleazar.rome.2.b": ["son", "...I'm glad he did."],      // PASS-19R2: new (breaks a run of three)
  "rome.eleazar.rome.3": ["eleazar", "Now I live where my people live. And I pray toward home."],
  "rome.eleazar.rome.son": ["son", "That's a long way from home. ...Me too."],
  "rome.eleazar.rome.4": ["eleazar", "Then we are neighbors in that, child."],
  // what he prays for: Isaiah 9:7 and 60:3, told in his own words; then the Son, to us (Luke 2:25, Simeon, not named to him)
  "rome.eleazar.opt.prayfor": ["son", "What do you pray for? If that's not private."],
  "rome.eleazar.prayfor.1": ["eleazar", "For Jerusalem's peace. And for the king God has promised, a son of David."],
  "rome.eleazar.prayfor.2": ["eleazar", "He will rule in righteousness, without end. The nations will come to his light."],
  "rome.eleazar.prayfor.2.b": ["son", "Everybody?"],      // PASS-19R2: new (breaks a run of four; the next line answers it)
  "rome.eleazar.prayfor.3": ["eleazar", "Greeks. Egyptians. Gauls. Romans. All of them, over there."],
  "rome.eleazar.prayfor.4": ["eleazar", "Even these. Even, perhaps, a boy in strange shoes."],
  "rome.eleazar.simeon": ["son", "There's an old man like him in my Bible. ...I'm SO not saying anything."],
  // the heart, only after that one: Isaiah 40:31, QUOTED, King James Version, the first clause, to its semicolon
  "rome.eleazar.opt.heart": ["son", "What if he doesn't come in time? For you, I mean."],
  "rome.eleazar.heart.1": ["eleazar", "Then my grandchildren will. The promise does not depend on an old man's eyes."],
  "rome.eleazar.heart.2": ["eleazar", "Isaiah says it: 'But they that wait upon the LORD shall renew their strength;'"],          // Isaiah 40:31, King James Version, to its semicolon: exact
  "rome.eleazar.heart.son.1": ["son", "That's on our fridge! On a magnet, with an eagle. Mom reads it when Dad's late."],      // PASS-17R: no reference aloud: where he knows it from
  "rome.eleazar.heart.son.2": ["son", "Dad's late right now. I don't even know which year he's late in."],
  "rome.eleazar.heart.3": ["eleazar", "Then we are both waiting, child. Shall we wait together a little?"],
  "rome.eleazar.opt.together": ["son", "...Yes. Together."],
  "rome.eleazar.opt.how": ["son", "I don't know the words you use."],
  "rome.eleazar.how": ["eleazar", "Use your own, child. He knows them all."],
  "rome.eleazar.opt.notnow": ["son", "Can we do it in a little bit? I should check on... everything."],
  "rome.eleazar.notnow": ["eleazar", "Whenever you come back. I am not going anywhere, and neither is the promise."],
  "rome.eleazar.opt.waitagain": ["son", "Mister Eleazar? Can we still wait together?"],
  "rome.eleazar.waitagain": ["eleazar", "Come. Stand here, beside me. We face the same way."],
  // the prayer, side by side, facing toward Jerusalem: the boy's head goes down and his hair stays up
  "rome.eleazar.prayer.son.1": ["son", "Dear God, please help Dad find me. And be with Mister Eleazar while he waits."],
  "rome.eleazar.prayer.son.2": ["son", "You know what he's waiting for. I know too. I didn't tell. Amen."],
  "rome.eleazar.amen": ["eleazar", "Amen."],
  "rome.eleazar.prayed": ["eleazar", "You pray like one who knows him well."],
  "rome.eleazar.prayed.son": ["son", "We talk a lot. Mostly at bedtime."],
  // the blessing: his hand on the boy's head (Genesis 48:14, shown); Numbers 6:25, QUOTED, King James Version, exact
  "rome.eleazar.bless.0": ["eleazar", "Come. Stand still a moment."],
  "rome.eleazar.bless.1": ["eleazar", "For you: 'The LORD make his face shine upon thee, and be gracious unto thee:'"],          // Numbers 6:25, King James Version: exact, colon and all
  "rome.eleazar.bless.son": ["son", "Pastor says that one! ...You only did the middle. I know all three."],      // PASS-17R: the design's own sample (office-hq-design.md, section 1): no reference aloud
  // only if the date seller blessed him (rome.dateseller.bless.2 has been said)
  "rome.eleazar.pieces.son": ["son", "The date seller gave me the first part! You two are doing it in PIECES."],
  "rome.eleazar.pieces": ["eleazar", "Yose blessed you too? Then the blessing has walked all over Rome today."],
  // and the boy gives him the last part: Numbers 6:26, QUOTED, King James Version, exact
  "rome.eleazar.opt.last": ["son", "Mister Eleazar? Can I give you the last part?"],
  "rome.eleazar.last.son": ["son", "'The LORD lift up his countenance upon thee, and give thee peace.'"],          // Numbers 6:26, King James Version: exact. PASS-17R: the reference is no longer said after it
  "rome.eleazar.last": ["eleazar", "I will remember the day the blessing came back to me."],
  "rome.eleazar.go": ["eleazar", "Go in peace, child. And find your father."],
  // walking away, to us
  "rome.eleazar.walking": ["son", "I didn't tell him. It wasn't mine to tell. But I prayed it. That counts."],
  // a second talk, and every one after
  "rome.eleazar.later": ["eleazar", "I am still waiting. It is easier this morning."],
  // the tassels on his mantle (Numbers 15:38, told)
  "rome.eleazar.opt.tassels": ["son", "What are the strings on your blanket? With the blue in them?"],
  "rome.eleazar.tassels.1": ["eleazar", "Not a blanket, child. The Law says to wear them, to remember."],
  "rome.eleazar.tassels.son": ["son", "Like a string on your finger! But holy."],
  "rome.eleazar.tassels.2": ["eleazar", "...Yes. Very like that."],
  "rome.eleazar.opt.bye": ["son", "I should go look for Dad. Can I come back?"],
  "rome.eleazar.bye.1": ["eleazar", "The bench will be here. So will I."],
  "rome.eleazar.bye.2": ["eleazar", "Still here. Still the bench."],
  // things carried, shown to him
  "rome.eleazar.coin": ["eleazar", "Keep it safe, child. New silver has a way of walking off in Rome."],
  "rome.eleazar.quarter": ["eleazar", "An eagle, struck proud. Not silver, Yose would say. A fine bird."],
  "rome.eleazar.lamp": ["eleazar", "A lamp for a long road. A gift is heavier than it looks."],
  "rome.eleazar.breakfast": ["eleazar", "The soothsayer's? Take it to him while it is warm."],

  // ---------- Mariam (mariamTree) ----------
  // About eight, the date seller's daughter, born in Rome; Eleazar's granddaughter. Certain about everything, especially
  // hens; bossy, fond, quick to laugh. Not Little Sister's double: her own girl.
  "rome.mariam.look": ["son", "A girl in a yard of hens, hands on her hips. I know that face."],
  "rome.mariam.look2": ["son", "She counted the hens again. Same number. She looks suspicious."],
  "rome.mariam.opt.hens": ["son", "Are those your hens? They're very... organized."],
  "rome.mariam.opt.hens2": ["son", "Why are your hens all staring the same way?"],
  // chickens: four lines of the thread, nobody explaining it (rome.sawHens)
  "rome.mariam.hens.1": ["mariam", "They're in a ROW. Since first light, all looking over the river at the city."],
  "rome.mariam.hens.2": ["mariam", "They won't eat. They won't lay. Hens are sensible. Something over there is not."],
  "rome.mariam.hens.2.b": ["son", "Maybe they're praying?"],      // PASS-19R2: new (breaks a run of three; her grandfather's saying answers it)
  "rome.mariam.hens.3": ["mariam", "Grandfather says hens don't pray. They only look."],
  "rome.mariam.hens.son": ["son", "They're looking at my door. From the other side of a whole river."],
  "rome.mariam.opt.name": ["son", "I'm collecting names. What's yours?"],
  "rome.mariam.name": ["mariam", "Mariam. You're the boy with lights on his feet. That's better than a name."],
  "rome.mariam.opt.window": ["son", "Is that your grandpa? Up in the window?"],
  "rome.mariam.window": ["mariam", "He comes down when he has finished, and he does not hurry for anybody."],
  "rome.mariam.opt.bench": ["son", "Is that your grandpa? On the bench, with the scroll?"],
  "rome.mariam.bench": ["mariam", "Don't stand in his light. He says you are, even when you're not."],
  "rome.mariam.opt.boss": ["son", "Are you the boss of this yard?"],
  "rome.mariam.boss.1": ["mariam", "The yard, the hens, the water dish, and Grandfather. Mostly Grandfather."],
  "rome.mariam.boss.son": ["son", "My little sister would LOVE you. You'd be bossy at each other."],
  "rome.mariam.boss.2": ["mariam", "I'm not bossy. I'm in CHARGE. It's different."],
  "rome.mariam.again": ["mariam", "Lights-on-his-feet! The hens are still looking."],
  "rome.mariam.opt.crouch": ["son", "Can you ask one what's wrong?"],
  "rome.mariam.crouch.1": ["mariam", "You don't ASK a hen. You look her in the eye."],
  "rome.mariam.crouch.2": ["mariam", "...She blinked. That means not sick, just busy."],
  "rome.mariam.crouch.3": ["mariam", "Still busy. You can't hurry a hen. Or a grandfather."],
  "rome.mariam.opt.family": ["son", "Do you live here with your grandpa?"],
  "rome.mariam.family.1": ["mariam", "Father sells dates in the city. From Jericho. The BEST."],
  "rome.mariam.family.2": ["mariam", "First one free. Mother says we'll be poor. Father says, poor with friends."],
  "rome.mariam.dates.son": ["son", "The date seller! I know him. He gave me a date with a rock in it."],
  "rome.mariam.dates": ["mariam", "That's the stone, silly. It's a tree that hasn't started yet."],
  // the words of the Law on the doorpost (Deuteronomy 6:9, told in her own words)
  "rome.mariam.opt.doorpost": ["son", "What's the little case on your door?"],
  "rome.mariam.doorpost.1": ["mariam", "Words of the Law. It says to write them on the doorposts. So we do."],
  "rome.mariam.doorpost.son": ["son", "Like a note on the fridge! But on the door. And forever."],
  "rome.mariam.doorpost.2": ["mariam", "What's a fridge?"],
  "rome.mariam.doorpost.son2": ["son", "...A cold cupboard. With magnets."],
  "rome.mariam.doorpost.3": ["mariam", "Words of the Law. And don't poke it. Everybody wants to poke it."],
  "rome.mariam.opt.bye": ["son", "Good luck with the hens."],
  "rome.mariam.bye.1": ["mariam", "They don't need luck. They need to finish looking."],
  "rome.mariam.bye.2": ["mariam", "Still looking!"],
  // things carried, shown to her
  "rome.mariam.gaultoga": ["mariam", "That's not a blanket. That's a TENT. Can the hens have it?"],
  "rome.mariam.coin": ["mariam", "Silver! Father would say: that's a lot of dates."],
  "rome.mariam.quarter": ["mariam", "A bird! A hen? ...No. A hen has more sense than to sit on a coin."],
  "rome.mariam.gum": ["mariam", "Is it food? The hens won't eat today, and I'm not a hen."],
  "rome.mariam.breakfast": ["mariam", "The hens won't want it. I tried figs. FIGS."],
  "rome.mariam.lamp": ["mariam", "A lamp! For Felix? He's going to Corinth. He told the hens."],

  // ---------- Felix (NEW 4's middle; felixTree) ----------
  // Gaius Fannius Felix, about twenty-six, Phyllis's son, born free: a boatman on the barges between here and Ostia,
  // his name down for Corinth. Cheerful, impatient, soft about his mother, full of Corinth.
  "rome.felix.look": ["son", "A big sunburnt guy loading a boat. He keeps looking at the bridge."],      // PASS-17R: shorter
  "rome.felix.look2": ["son", "He's whistling. No tune. Just air with ambition."],
  // ways in (the first, when the boy is carrying his mother's lamp)
  "rome.felix.opt.felix": ["son", "Are you Felix? Phyllis's Felix? Tall, sunburnt, in a hurry?"],
  "rome.felix.felix": ["felix", "All three. Who's asking, and how do you know my mother?"],
  "rome.felix.opt.carry": ["son", "What are you carrying? Is it heavy? Can I try?"],
  "rome.felix.carry": ["felix", "Papyrus. And no. You'd end up in the river, and I'd be explaining."],
  "rome.felix.opt.table": ["son", "Is that a boat? It looks like a table that floats."],
  "rome.felix.table": ["felix", "It's a barge. A table doesn't go down to Ostia and back."],
  "rome.felix.opt.where": ["son", "Where does the boat go?"],
  "rome.felix.where": ["felix", "Down to Ostia, where the big ships wait. Soon, me with them."],
  "rome.felix.again": ["felix", "Back again? I'm still carrying. Talk while I walk."],
  "rome.felix.opt.name": ["son", "Who are you? I'm collecting names."],
  "rome.felix.name": ["felix", "Felix. Gaius Fannius Felix, if you're writing it down."],
  "rome.felix.opt.ostia": ["son", "What's Ostia?"],
  "rome.felix.ostia.1": ["felix", "The port. The big ships wait off the shore."],
  "rome.felix.ostia.2": ["felix", "We bring the cargo up. Papyrus, linen, jars of everything."],
  "rome.felix.ostia.3": ["felix", "Ostia. Sea. Ships. Barges. Me. Up and down. That's the whole of it."],
  // Corinth (and the Son, to us, at the name: Acts 18:1-3 and the two letters, in his own words; then he stops himself)
  "rome.felix.opt.corinth": ["son", "What's in Corinth?"],
  "rome.felix.corinth.1": ["felix", "Nothing yet! That's the beauty. The dictator's building it again."],
  "rome.felix.corinth.2": ["felix", "My name's down. A house of my own, in a city with a sea on each side."],
  "rome.felix.corinth.3": ["felix", "Corinth. A house. TWO seas! ...Sorry."],
  "rome.felix.paul.son.1": ["son", "Corinth! Paul lives there one day. He makes tents. There are TWO letters..."],
  "rome.felix.paul.son.2": ["son", "...Operation Don't Wreck Anything."],
  "rome.felix.paul": ["felix", "...Are you all right? You went funny."],
  "rome.felix.paul.son.3": ["son", "Fine! Corinth sounds great. Would move to."],
  "rome.felix.opt.mother": ["son", "Your mom's in the Forum! With the flowers."],
  "rome.felix.mother.1": ["felix", "Selling to half of Rome. She can't leave her baskets today."],
  "rome.felix.mother.2": ["felix", "So I wave at the Forum. She can't see me. I wave anyway."],
  "rome.felix.mother.3": ["felix", "Tell her I'm eating. She'll ask. She always asks."],
  // the lamp (the lever: hook setDown, then lamp), his mother's wish, and his word
  "rome.felix.opt.lamp": ["son", "Special delivery! A lamp from your mom. For Corinth."],
  "rome.felix.gift.1": ["felix", "...From her? She can't leave her baskets. She sent you?"],
  "rome.felix.gift.son.1": ["son", "She threw a wish in the fountain for you too. I sort of borrowed it."],
  "rome.felix.gift.2": ["felix", "She threw a coin in a fountain? For ME?"],
  "rome.felix.gift.3": ["felix", "...She never throws anything. She keeps string."],
  "rome.felix.gift.son.2": ["son", "She wants to hear you say you'll come. Before you go."],
  "rome.felix.opt.come": ["son", "Will you come and say goodbye?"],
  "rome.felix.word.1": ["felix", "Tell her I'll come over the bridge at the ninth hour. Before the barge goes."],
  "rome.felix.word.2": ["felix", "And tell her I'll light it in Corinth. The first night. In the first window."],
  "rome.felix.word.son": ["son", "Lamp delivered. And I'm taking a promise back. A two-way errand."],
  "rome.felix.opt.string": ["son", "String? Like, just regular string?"],
  "rome.felix.string": ["felix", "Every bit of string we ever had. In a jar. Since before I was born."],
  "rome.felix.string.son": ["son", "My mom keeps rubber bands. On the doorknob. It's a BALL now."],
  "rome.felix.after": ["felix", "The ninth hour. I haven't forgotten. I've told the bales twice."],
  "rome.felix.opt.bye": ["son", "I'll let you work, boat guy."],
  "rome.felix.bye.1": ["felix", "Mind the edge! The Tiber's cold, and I'm busy."],
  "rome.felix.bye.2": ["felix", "Still busy!"],
  "rome.felix.bye.after": ["felix", "Ninth hour! Tell her again, in case!"],
  // things carried, shown to him (the lamp starts his talk)
  "rome.felix.gaultoga": ["felix", "That'd make a fine sail. ...Not my business. I've got bales."],
  "rome.felix.coin": ["felix", "New silver, by the river? Put it away before it goes for a swim."],
  "rome.felix.breakfast": ["felix", "Sausage! ...Not for me? Don't wave it at a working man, then."],

  // ================= carried things =================
  "item.toga.look": ["son", "The senator's bedsheet. Heavier than my backpack, and it does a lot less."],
  "item.tunic.look": ["son", "A tunic my size, to bring back clean. The laundry lady hasn't seen me eat."],
  "item.breakfast.look": ["son", "Bread and a sausage in a cloth. Not eating it. Smelling is free."],
  "item.incense.look": ["son", "A box of holy smell. It rattles. I'm not opening it. That's called growth."],
  "item.coin.look": ["son", "A coin with a serious man on it. He looks like he has never had a snack in his life."],              // kept
  "item.coin.mom": ["mom", "A silver coin with a stern gentleman on it. It looks old and it looks new. Your sister will know which."],     // kept (Act Four)
  "item.coin.bigsis": ["bigsis", "A denarius of Julius Caesar, struck in 44 B.C. and not a day older. I am not letting go of it."],        // kept (Act Four)
  "item.coin.lilsis": ["lilsis", "A money, with a grumpy man on it. He needs a snack."],                                                   // kept (Act Four)
  // his own things: looked at, tried on people, never the answer to anything
  "item.phone.look": ["son", "It died doing what it loved: taking four hundred pictures of a donkey."],
  "item.quarter.look": ["son", "Emergency quarter, for a pay phone. Never seen a pay phone. I've seen ROME."],
  "item.gum.look": ["son", "Half a pack. The rest is under the car seat. A problem for later. Or earlier."],
  // ROME-13W: the two new things carried (world.js: gaultoga, lamp)
  "item.gaultoga.look": ["son", "The Gaul's toga. The size of a parachute. I could camp in it."],
  "item.lamp.look": ["son", "Phyllis's goodbye lamp for Felix. I'm carrying it like an egg."],

  // ================= hints: one for each puzzle, in his own voice =================
  "hint.rome.toga": ["son", "The door guy wants a clean tunic. The laundry lady on the street has lots."],
  "hint.rome.delivered": ["son", "The senator's bedsheet. He's the one in a hurry by the temple steps."],
  "hint.rome.tunic": ["son", "Bedsheet delivered. The laundry lady owes me one tunic. Time to collect."],
  "hint.rome.breakfast": ["son", "The chicken man has incense, and no breakfast. The snack bar has breakfast."],
  "hint.rome.incense": ["son", "The chicken man's breakfast is in my backpack. It's getting cold. So is he."],
  "hint.rome.coin": ["son", "That fountain is full of other people's wishes. I only need to borrow one."],                         // kept
  "hint.rome.inside": ["son", "Clean tunic, something for the god: got both. Time to show the door guy."],
  "hint.rome.spark": ["son", "Sun on the temple floor. A shiny coin in my backpack. Bounce it at the door."],
  "hint.rome.toss": ["son", "The humming door ate me. Maybe it eats money too. For science."],                                    // kept
  // ROME-13W: the new beats' hints. (hint.rome.delivered keeps its words and now speaks for the first delivery, the
  // wrong toga; hint.rome.breakfast keeps its words: the snack bar is still where to ask.) hint.rome.gaul is one line
  // that helps both before and after he has heard where the Senate meets.
  "hint.rome.gaul": ["son", "A lost Gaul in the Forum has the toga. My senator knows where the Senate meets."],
  "hint.rome.delivered2": ["son", "Right bedsheet now. The senator's at the temple steps. Delivery, take two."],
  "hint.rome.geese": ["son", "The breakfast's up the hill, with a stuck kid. Somebody there knows about geese."],
  "hint.rome.wish": ["son", "That's Phyllis's wish. I'll ask her first, in the Forum, by the violets."],
  "hint.rome.felix": ["son", "Phyllis's lamp is for her boy, Felix. He loads barges across the river."],
  "hint.rome.granted": ["son", "Felix said yes. Go tell his mom!"],
};
