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
  "rome.arrive.out": ["doorkeeper", "And stay out. This is the treasury of the Roman People, not a nursery for boys in strange shoes."],
  "rome.arrive.1": ["son", "Dad? This isn't the rest stop, because the rest stop had a vending machine."],                  // kept
  "rome.arrive.2": ["son", "Everyone here is wearing a bedsheet. It's the biggest sleepover in history."],        // kept
  "rome.arrive.5": ["son", "The big guy carried me out by my backpack, like a suitcase. I think I'm luggage now."],
  "rome.arrive.3": ["son", "Okay, Operation Find Dad. Step one is snacks, and step two is Dad, obviously."],                           // kept
  "rome.arrive.7": ["son", "Something past that bush smells fried and amazing. Step one is that way."],

  // ---------- the temple front, the doors, the doorkeeper ----------
  "rome.temple.look": ["narrator", "The temple of Saturn, on tall striped pillars at the top of the steps. The Son gives it seven out of ten."],   // kept
  "rome.temple.use": ["narrator", "The Son would love to climb it. The doorkeeper can throw a boy farther than fourteen steps, though, and has shown it."],
  "rome.doors.look": ["narrator", "Tall doors, standing wide open all day long. The Son is locked out of them anyway, by a man instead of a lock."],
  "rome.doors.look2": ["narrator", "The doors stand wide open, and this time they are open for him. The Son feels like one of the staff."],
  "rome.stairs.look": ["narrator", "Fourteen steps. The Son counted every one on the way down, upside down, hanging by his backpack."],

  "rome.doorkeeper.look": ["narrator", "The doorkeeper, a man about the size and shape of a door. That makes two doors for one temple, by the Son's count."],
  "rome.doorkeeper.look2": ["narrator", "The doorkeeper has not blinked since he set the Son down. The Son has been keeping watch on it."],
  "rome.doorkeeper.hi.1": ["son", "It's me again. I left a door in there, a humming one. Can I run in and get it?"],
  "rome.doorkeeper.hi.2": ["doorkeeper", "No."],
  "rome.doorkeeper.hi.3": ["son", "Do any kids ever get to go in? Even one, on his birthday?"],
  "rome.doorkeeper.rule.2": ["doorkeeper", "A boy who serves at the rites may enter, in a clean tunic, carrying something for the god. Not otherwise."],
  "rome.doorkeeper.rule.3": ["doorkeeper", "You are a boy, I grant you. That is one out of three."],
  "rome.doorkeeper.rule.4": ["son", "He gives scores out of three? My teacher at least goes up to a hundred."],
  "rome.doorkeeper.ask.rule": ["son", "What were the three things again? I'll write them on my hand."],
  "rome.doorkeeper.ans.rule": ["doorkeeper", "A boy, a clean tunic, and something in his hands for the god. I have now said it twice. I will not sing it."],
  "rome.doorkeeper.ask.what": ["son", "What's in there, anyway? Besides my door."],
  "rome.doorkeeper.ans.what.1": ["doorkeeper", "The god Saturn, and at his feet the treasury of the Roman People. That is why I stand where I stand."],
  "rome.doorkeeper.ans.what.2": ["son", "A church and a bank in one building. Dad would call that one-stop shopping."],
  "rome.doorkeeper.ask.dad": ["son", "Have you seen my dad? He's tall, with a little beard and flowers all over his shirt."],
  "rome.doorkeeper.ans.dad.1": ["doorkeeper", "No."],
  "rome.doorkeeper.ans.dad.2": ["son", "Maybe he stopped to ask for directions. No, he never would. He'd drive in circles for a week first."],
  "rome.doorkeeper.ans.dad.3": ["doorkeeper", "Then he is lost."],
  "rome.doorkeeper.ans.dad.4": ["son", "He's not lost. He's making good time, somewhere."],
  "rome.doorkeeper.ask.bye": ["son", "Don't go anywhere."],
  "rome.doorkeeper.ans.bye": ["doorkeeper", "I never do."],
  "rome.doorkeeper.need.both": ["doorkeeper", "Still one out of three: no clean tunic, and nothing for the god. I am not a difficult man, only an exact one."],
  "rome.doorkeeper.need.gift.1": ["doorkeeper", "A clean tunic. Good. But you have brought the god two empty hands, and that is two out of three."],
  "rome.doorkeeper.need.gift.2": ["son", "My score went up! Somebody tell my teacher."],
  "rome.doorkeeper.need.tunic.1": ["doorkeeper", "Incense. Good. But it is carried by a boy wearing I do not know what. Two out of three."],
  "rome.doorkeeper.need.tunic.2": ["son", "It's a hoodie. It's from the future, and it was on sale."],
  "rome.doorkeeper.again": ["doorkeeper", "You again. In you go, and touch nothing, again."],
  "rome.doorkeeper.toga": ["doorkeeper", "A senator's toga. Senators are down there and I am up here, and we both prefer it."],
  "rome.doorkeeper.breakfast.1": ["doorkeeper", "I do not eat at the door. Is that the sausage from the cookshop on the fountain street?"],
  "rome.doorkeeper.breakfast.2": ["son", "Sorry, it's the chicken man's. It's spoken for."],
  "rome.doorkeeper.breakfast.3": ["doorkeeper", "Then it is the chicken man's."],
  "rome.doorkeeper.coin": ["doorkeeper", "One coin, for the treasury of the Roman People. It has others, boy, several."],
  "rome.doorkeeper.quarter": ["doorkeeper", "That is not a coin. Put it away before I have to find out what it is."],
  "rome.doorkeeper.phone": ["doorkeeper", "A small black door, and it is shut. I approve."],
  // ROME-13W: the two new things carried, shown to him (the Gaul's toga, Phyllis's lamp)
  "rome.doorkeeper.gaultoga": ["doorkeeper", "That is not a toga, it is a large mistake. Take it off my steps."],
  "rome.doorkeeper.lamp": ["doorkeeper", "It is unlit, which is good. Nothing burns at this door that I did not light."],

  // the gate: in the tunic, with the incense
  "rome.gate.1": ["son", "Tunic on, over the hoodie and the backpack. I'm the lumpiest Roman in Rome."],
  "rome.gate.2": ["son", "One boy, one clean tunic, and one box of holy smell for the god."],
  "rome.gate.3": ["doorkeeper", "Three out of three."],
  "rome.gate.4": ["son", "YES."],
  "rome.gate.5": ["doorkeeper", "The hair."],
  "rome.gate.6": ["son", "It doesn't go down. I've tried, Mom's tried, and gravity's tried."],
  "rome.gate.7": ["doorkeeper", "Go in. Walk, do not run, and touch nothing. The clerk is counting, and he hates to begin again."],
  "rome.gate.8": ["son", "I'm walking. I'm touching nothing, mostly."],

  // ---------- the soothsayer and his sacred chickens ----------
  "rome.soothsayer.look": ["narrator", "An old man on the steps with a cage of chickens. He has the look of someone who read the last page first."],
  "rome.soothsayer.look2": ["narrator", "The soothsayer keeps sighing at the fourteen steps above him. The steps do not seem to mind."],
  "rome.soothsayer.hi.1": ["soothsayer", "Beware the Ides of March."],
  "rome.soothsayer.hi.2": ["son", "What's an Ides? Is that a day or a guy?"],
  "rome.soothsayer.hi.3": ["soothsayer", "Today."],
  "rome.soothsayer.hi.4": ["son", "Then it's a bit late to beware."],
  "rome.soothsayer.hi.5": ["soothsayer", "I said so all through February, too, and nobody listened then either. Mine is a lonely trade."],
  "rome.soothsayer.ask.birds": ["son", "Why are your chickens in a cage? Are they in trouble?"],
  "rome.soothsayer.ans.birds.1": ["soothsayer", "They are sacred. When they feed, the day is good, and today they have not touched one grain."],
  // chickens: he takes it for the worst of omens, which for a man selling omens on the Ides of March it is. (The id gives him a hand across his brow.)
  "rome.soothsayer.ans.birds.omen": ["soothsayer", "It is the worst omen, and on the Ides. I sell omens, and this one I could not give away."],
  "rome.soothsayer.ans.birds.2": ["son", "Maybe they're just not breakfast chickens. Some people aren't breakfast people."],
  "rome.soothsayer.ans.birds.3": ["soothsayer", "Nor am I, today. My bread and sausage come from the cookshop by the fountain, and nobody brought them."],
  "rome.soothsayer.ans.birds.4": ["soothsayer", "I foresaw it. It did not help."],
  "rome.soothsayer.ans.birds.fed": ["soothsayer", "They are feeding, look at them. I have decided not to ask them why."],
  "rome.soothsayer.ask.temple": ["son", "Can you get me into the temple? You look like you know people."],
  "rome.soothsayer.ans.temple.1": ["soothsayer", "I cannot get myself in, boy. My incense for Saturn should have gone up those steps at dawn."],
  "rome.soothsayer.ans.temple.2": ["soothsayer", "There are fourteen steps between it and him, and my knees have foreseen every one."],
  "rome.soothsayer.ans.temple.3": ["son", "I could carry it. I'm great at steps. I take the ones at school two at a time."],
  "rome.soothsayer.ans.temple.4": ["soothsayer", "Not today. The birds will not feed, and I have no breakfast to tempt them. Bring me that, and we shall see."],
  "rome.soothsayer.ans.temple.fed": ["soothsayer", "Do not drop it. I have not foreseen you dropping it, which is something."],
  "rome.soothsayer.ask.future": ["son", "Can you tell my future? I'll hold really still."],
  "rome.soothsayer.ans.future.1": ["soothsayer", "Give me your hand. A long road, and most of it strange. You will be very late for supper."],
  "rome.soothsayer.ans.future.2": ["son", "He's GOOD."],
  "rome.soothsayer.ans.future.3": ["son", "Do I find my dad? A yes or a no is fine, but a yes is better."],
  "rome.soothsayer.ans.future.4": ["soothsayer", "The birds do not say. But boys who look, find. That is not prophecy, that is boys."],
  "rome.soothsayer.ask.bye": ["son", "Happy Ides!"],
  "rome.soothsayer.ans.bye": ["soothsayer", "It is not that kind of day."],
  "rome.soothsayer.fed.1": ["son", "Breakfast delivery, from the snack guy. He says you've owed him for eleven years."],
  "rome.soothsayer.fed.2": ["soothsayer", "I foresaw this sausage. It is the first good thing I have foreseen all year."],
  "rome.soothsayer.fed.3": ["soothsayer", "A few crumbs for the birds, first. There, they feed, look at them feed."],
  "rome.soothsayer.fed.3.b": ["son", "See? Breakfast chickens."],  // PASS-19R1: new, after rome.soothsayer.fed.3
  "rome.soothsayer.fed.5": ["soothsayer", "Now take this incense in to the god for me. My knees send their regards."],
  "rome.soothsayer.fed.6": ["son", "First a sausage, now a box of holy smell. I'm a delivery truck in sneakers."],
  // ROME-13W: said in place of rome.soothsayer.fed.1 (as the choice and as the line) when the breakfast came down the hill
  // from Titus: the keeper no longer hands it over, so "From the snack guy" would not be true.
  "rome.soothsayer.fed.geese": ["son", "Breakfast! It's been up a hill and past some geese, but it's all here, mostly."],
  "rome.soothsayer.toga": ["soothsayer", "That is not mine. Mine has known soup, and that one has a future."],
  "rome.soothsayer.coin.1": ["soothsayer", "It is wet. I foresee that it came from a fountain."],
  "rome.soothsayer.coin.2": ["son", "Whoa. How did you know?"],
  "rome.soothsayer.coin.3": ["soothsayer", "It is dripping on my foot."],
  "rome.soothsayer.quarter": ["soothsayer", "A man with his hair tied back. I do not know this omen, and I dislike that."],
  "rome.soothsayer.incense": ["soothsayer", "It goes up the steps, boy. That is the whole of the favor."],
  // ROME-13W: the two new things carried, shown to him
  "rome.soothsayer.gaultoga": ["soothsayer", "That toga has a Gaul in its future. A large one."],
  "rome.soothsayer.lamp": ["soothsayer", "A lamp for a journey, a long one, over water. Not yours, I think."],

  "rome.birdcage.look": ["narrator", "Chickens in a cage. They have the look Mom gets when Dad says the word shortcut."],
  "rome.birdcage.look2": ["narrator", "The sacred chickens. Nothing about them shows what makes them sacred, and they are not telling."],
  "rome.birdcage.use": ["narrator", "The Son clucks at the cage. The chickens ignore him; they can tell he has no snacks."],
  // chickens: they all stand facing the temple doors, where the door in time is. He notices it himself (the first time he
  // calls them, or the second time he looks, fed or not), and thinks of his little sister. He does not explain it.
  // (The ids give him a point up the steps, then both arms up for the General.)
  "rome.birdcage.doors.1": ["son", "Hey, they're all facing the temple doors, every one of them. Chickens know things."],
  "rome.birdcage.doors.2": ["son", "My little sister says that. Her chicken, General Feathers, outranks me."],
  "rome.birdcage.fed": ["narrator", "The chickens are eating as if it were a contest. A good omen, for something."],
  "rome.birdcage.breakfast": ["narrator", "The breakfast is the soothsayer's. If the Son fed it to the chickens, the old man would foresee it."],

  // ---------- the senator ----------
  "rome.senator.look": ["narrator", "A man in a very large toga, standing still in a great hurry, the way Dad waits at red lights."],
  "rome.senator.look2": ["narrator", "A purple stripe, red shoes and a pink face. The Son thinks the senator looks like a whole box of crayons."],
  "rome.senator.hi.1": ["senator", "Boy. Do you know who I am?"],
  "rome.senator.hi.2": ["son", "No. Do you know who I am?"],
  "rome.senator.hi.3": ["senator", "No."],
  "rome.senator.hi.4": ["son", "Then we're tied."],
  "rome.senator.hi.5": ["senator", "I am a senator of Rome, and I am late. My clean toga is still at the laundry, where it has no business being."],
  "rome.senator.ask.late": ["son", "Late for what?"],
  "rome.senator.ans.late.1": ["senator", "The Senate meets today, in the hall beside Pompey's theater. I have a speech."],
  "rome.senator.ans.late.2": ["senator", "It is about drains. It is magnificent."],
  "rome.senator.ans.late.3": ["son", "How long is it?"],
  "rome.senator.ans.late.4": ["senator", "It ends when they agree with me."],
  "rome.senator.ask.toga": ["son", "You're already wearing a bedsheet. A really big one."],
  "rome.senator.ans.toga.1": ["senator", "This is yesterday's toga, boy. There is an olive stain on it, here, by the fold."],
  "rome.senator.ans.toga.2": ["son", "Where? I can't see it, and I'm looking really hard."],
  "rome.senator.ans.toga.3": ["senator", "The Senate would. Finding the stain on another man is most of what we do."],
  "rome.senator.ans.toga.4": ["senator", "The washerwoman by the fountain has had my best one for three days. Men have founded colonies in less."],
  // woven: the great-nephew nobody thinks about is the Caesar Augustus of Luke 2:1. Nobody in Rome knows it this morning.
  "rome.senator.ask.caesar": ["son", "Does Caesar have a kid? A kid like that could get in anywhere."],
  "rome.senator.ans.caesar.1": ["senator", "Caesar has no son. A great-nephew, Octavius, is at his books in Apollonia."],
  "rome.senator.ans.caesar.2": ["senator", "Nobody gives the boy a thought. I mention him only because I am thorough."],
  "rome.senator.ans.caesar.3": ["son", "I know another Caesar, Augustus. He counts everybody in the Christmas story."],      // PASS-17R: no reference aloud
  "rome.senator.ans.caesar.4": ["senator", "Augustus? There is no such name, and I know every name in Rome that matters."],
  "rome.senator.ans.caesar.5": ["son", "Not yet."],
  "rome.senator.ask.dad": ["son", "Have you seen my dad? Little beard, flowers all over his shirt?"],
  "rome.senator.ans.dad.1": ["senator", "Flowers, on a shirt, in the Forum? No. I would have made a speech about it."],
  "rome.senator.ans.dad.2": ["son", "Mom's made a few."],
  "rome.senator.ask.bye": ["son", "Good luck with the drains!"],
  "rome.senator.ans.bye": ["senator", "Luck is for men without speeches."],
  // ROME-13W (decision 12): was "Delivery! One clean bedsheet with a purple stripe. From the laundry lady." A senator's
  // toga is plain white; his mark is the broad stripe down his tunic. Said at the second delivery, the right toga's.
  "rome.senator.toga.1": ["son", "Delivery! One clean bedsheet from the laundry lady, like a cloud with a job."],
  "rome.senator.toga.2": ["senator", "A toga, boy. A bedsheet covers a man asleep. A toga covers a man who matters."],
  "rome.senator.toga.3": ["son", "It's really heavy for something with no pockets."],
  "rome.senator.toga.4": ["senator", "Rome thanks you. I, personally, am far too late."],
  "rome.senator.toga.5": ["senator", "To the Senate! They would never dare begin without me."],
  "rome.senator.toga.6": ["son", "Delivered. The laundry lady owes me one tunic."],
  "rome.senator.breakfast": ["senator", "I do not eat in the street. I am seen in the street."],
  "rome.senator.incense": ["senator", "Incense is for gods, and I am only a senator. Only."],

  // ---------- ROME-13W: the senator's turn (#2 Deliver It, the first time: decision 2) ----------
  // The first time the boy brings the toga it is the wrong one. He says wrong.1 (as the choice "give", and as the line,
  // in place of toga.1); the senator takes it, unfolds it, holds it up, turns from the boy and back: it is new, and it
  // reaches the ground twice. It is a Gaul's, and the Gaul has his. He hands the enormous one back (`toga` taken,
  // `gaultoga` given, rome.wrongToga) and stays, pacing. The second time, with his own, the old delivery as it is.
  "rome.senator.wrong.1": ["son", "Delivery. One bedsheet, folded by a professional."],
  "rome.senator.wrong.2": ["senator", "At last. Three days I have waited for this, so give it here, boy."],
  "rome.senator.wrong.3": ["senator", "But this toga is new. It has never been to the Senate, or to anything."],
  "rome.senator.wrong.4": ["senator", "And it reaches the ground. Twice."],
  "rome.senator.wrong.5": ["son", "Maybe it's a growing toga. Mom buys my clothes big so I can grow into them."],
  "rome.senator.wrong.6": ["senator", "The laundress fulled a toga for one of the dictator's new Gauls as well. So the Gaul has mine."],
  "rome.senator.wrong.7": ["senator", "He will be somewhere in the Forum, lost. They are always lost, these new men of his."],
  "rome.senator.wrong.8": ["son", "So I find the lost Gaul and swap the bedsheets. Easy, probably."],
  // the Gaul's toga shown to him again; and the lamp
  "rome.senator.gaultoga": ["senator", "Put that away, I have seen enough of it for one morning. Find the Gaul in the Forum."],
  "rome.senator.lamp": ["senator", "A lamp? It is morning, boy, as even I can see, and I am late."],

  // ---------- the rest of the Forum ----------
  "rome.altar.look": ["narrator", "A stone altar with a garland of flowers round it and nothing burning on it. To the Son it is a very sad barbecue."],
  "rome.altar.use": ["narrator", "The Son keeps his hands off. Dad's one barbecue rule is never to touch a grill somebody else lit, and Dad breaks it."],
  "rome.altar.incense": ["narrator", "The incense is for the god inside the temple, not for the altar out here."],
  "rome.forum.look": ["narrator", "The Forum, a whole downtown without one car in it. To the Son it looks like recess for grown-ups."],
  "rome.forum.look2": ["narrator", "The Forum, and a temple on the hill above it too. Rome puts temples on everything, like sprinkles."],
  "rome.stone.look": ["narrator", "A stone cut with four letters, S. P. Q. R., and not a vowel among them. The Son cannot even sneeze it."],
  "rome.pigeons.look": ["narrator", "Pigeons, the very same kind as at home. The Son wonders whether they time travel, which would explain a lot."],
  "rome.pigeons.use": ["narrator", "The Son does not chase them. The last time he chased pigeons, Dad had to apologize to a truck."],
  "rome.tripod.look": ["narrator", "A tall bronze tripod, like a giant cake stand with no cake on it. Rome keeps getting the Son's hopes up."],
  "rome.board.look": ["narrator", "A board of notices in very small letters. Rome has terms and conditions, and nobody reads them here either."],
  "rome.tostreet.look": ["narrator", "The street off the square smells of bread, sausage and one other thing the Son has decided not to ask about."],
  "rome.cart.look": ["narrator", "A cart of sacks, going in under the temple. The treasury seems to have a drive-through."],
  "rome.dog.look": ["narrator", "A dog, asleep in the sun. The Son asks for one every birthday, and Dad always says they will see."],
  "rome.dog.use": ["narrator", "The Son calls him. The dog opens one eye and shuts it again, and the Son would adopt him on the spot."],
  "rome.dog.breakfast": ["narrator", "The sausage is the soothsayer's. Not giving it to the dog is the hardest thing the Son has ever not done."],

  // ---------- ROME-13W: the two new ways (bottom edge into the Forum, right edge up to the Capitol), and the far view in two ----------
  // Until he has been to the street and worked out that it is B.C. (rome.knowsBC), each way, and each half of the far
  // view, says rome.steps.closed and he stays. The far view's lower half keeps its old looks (rome.forum.look, .look2);
  // the hill above it is a thing of its own: its first look before he has been up, its second once he has (rome.sawCapitol).
  "rome.steps.closed": ["son", "Snacks first. My nose has spoken."],
  "rome.hill.look": ["narrator", "The Capitol hill. The road up to it goes round the back of this temple; Rome hides its stairs."],
  "rome.hill.look2": ["narrator", "The Capitol. The Son has been up there now, and the geese send their regards."],

  // ================= rome-street: the shopping street =================

  "rome.street.arrive.1": ["son", "A whole street of snacks and laundry. Rome, you really get me."],
  // woven: he hears whose nose is on the new money, and works out when he is. (The era card has just told the
  // player "44 B.C."; this is where he catches up, and where everything he says "Not yet." about begins.)
  "rome.street.cry": ["keeper", "Hot sausage, hot bread, new silver with Caesar's nose on it, I take every nose!"],
  "rome.street.bc.1": ["son", "Julius Caesar? He's on my big sister's timeline, on the B.C. side."],
  "rome.street.bc.2": ["son", "B.C. means Before Christ. So it's before the first Christmas."],
  "rome.toforum.look": ["narrator", "The way back down to the temple, the hum and the doorkeeper. One of the three likes the Son."],

  // ---------- the snack bar and its keeper ----------
  "rome.snackbar.look": ["narrator", "A snack bar, with big soup jars sunk into its counter and bread stacked beside them. Step one, found."],
  "rome.snackbar.look2": ["narrator", "The shop has no front wall at all: a kitchen to walk past. The Son thinks it the best idea Rome has had."],
  "rome.pricelist.look": ["narrator", "A menu painted on the wall, with no pictures. The Son wonders how anyone knows what the food looks like."],
  "rome.keeper.look": ["narrator", "The keeper of the snack bar, cooking, talking and waving a spoon all at once. He is like three dads."],
  "rome.keeper.look2": ["narrator", "The keeper has not stopped talking since the Son arrived. It is possible he never has."],
  "rome.keeper.hi.1": ["keeper", "A customer, a small one, too thin, everybody is too thin, here, eat, eat."],
  "rome.keeper.hi.2": ["son", "Bread with cheese in it. Step one is done, but it needs ketchup."],
  "rome.keeper.hi.3": ["keeper", "It needs what?"],
  "rome.keeper.hi.4": ["son", "It's ketchup: tomatoes squished into a red sauce. You put it on everything."],
  "rome.keeper.hi.5": ["keeper", "What is a tomato?"],
  "rome.keeper.hi.6": ["son", "No tomatoes? Dad's been saving those little ketchup packets for years, like he knew."],
  // ROME-13W (#4 Take The Breakfast, changed: he no longer hands the breakfast over). His boy Titus took it at first
  // light and has not come back: every Ides the boy runs after the white ewe that goes up to Jupiter. Said in this
  // order: errand.1, .2, .ewe, .3, .4. (The old words of all four are in the writer's ids.md for the round.)
  "rome.keeper.errand.1": ["keeper", "Never mind, you have legs, good, I need legs, I have lost my boy, my Titus."],
  "rome.keeper.errand.2": ["keeper", "He took the old soothsayer's breakfast at first light, bread and a sausage."],
  "rome.keeper.errand.2.b": ["son", "Where did he go?"],  // PASS-19R1: new, after rome.keeper.errand.2
  "rome.keeper.errand.3": ["keeper", "Up to Jupiter's hill, after the white ewe. Bring down my boy and the breakfast."],
  "rome.keeper.errand.4": ["son", "Find the kid, find the sausage. I won't eat it, I'll just think about it."],
  "rome.keeper.ask.pay": ["son", "How much do I owe you? I've got a quarter."],
  "rome.keeper.ans.pay.1": ["keeper", "Who is this? I know every consul's nose, and that is not a consul."],
  "rome.keeper.ans.pay.2": ["son", "That's George. Back home, everybody knows that nose."],      // PASS-17R: answers him back; and not every quarter has George now (us.quarter)
  "rome.keeper.ans.pay.3": ["keeper", "I do not know George, keep him, pay me later, everyone pays me later."],
  "rome.keeper.ans.pay.4": ["son", "He gave me a tab. I have a tab, and I'm telling everyone."],
  "rome.keeper.ask.pizza": ["son", "Do you have pizza?"],
  "rome.keeper.ans.pizza.1": ["keeper", "What is pizza?"],
  "rome.keeper.ans.pizza.2": ["son", "Flat bread, cheese on top, and a sauce underneath. You eat it with your hands."],
  "rome.keeper.ans.pizza.3": ["keeper", "Flat bread I have, cheese I have, what is the sauce?"],
  "rome.keeper.ans.pizza.4": ["son", "Tomatoes."],
  "rome.keeper.ans.pizza.5": ["keeper", "This word again."],
  "rome.keeper.ask.owe": ["son", "Does everybody owe you money?"],
  "rome.keeper.ans.owe.1": ["keeper", "The senator owes me forty dinners, the soothsayer eleven years of breakfasts."],
  "rome.keeper.ans.owe.2": ["keeper", "The wall is for prices, my head is for debts, my head is very full."],
  "rome.keeper.ask.dad": ["son", "Have you seen my dad? Little beard, flowers on his shirt, always making good time?"],
  "rome.keeper.ans.dad.1": ["keeper", "No, and everyone eats here, if he is in Rome he will come, so sit, wait, eat."],
  "rome.keeper.ans.dad.2": ["son", "That's the best plan anybody's had all day. It has snacks in it."],
  "rome.keeper.ask.bye": ["son", "Best step one ever."],
  "rome.keeper.ans.bye": ["keeper", "Go, come back, bring the plate, there was no plate, go."],
  "rome.keeper.coin.1": ["keeper", "That nose I know, that is Caesar, struck this year, good silver."],
  "rome.keeper.coin.2": ["son", "He looks like he needs a sausage."],
  "rome.keeper.coin.3": ["keeper", "Everybody needs a sausage, that is my whole trade."],
  "rome.keeper.toga": ["keeper", "A senator's toga, beside my sauce, out, out, I cannot pay to wash it twice."],
  "rome.keeper.breakfast": ["keeper", "No, no, up the street with it, to the old one with the chickens, it is getting cold."],
  "rome.keeper.gum.1": ["son", "Want some gum? You chew it, but you never eat it."],
  "rome.keeper.gum.2": ["keeper", "Food that is never eaten. That is the saddest thing ever said at my counter."],

  // ---------- ROME-13W: the keeper and his boy (Juno's Geese) ----------
  // In place of the errand, if the boy has met Titus already (Titus said whose boy he is) but has not got the breakfast:
  "rome.keeper.met.1": ["son", "Found him! He's up the hill on a statue, with your breakfast. And there are geese, a lot of geese."],
  "rome.keeper.met.2": ["keeper", "Geese, every Ides the ewe, now geese, go back up, bring him down."],
  // In place of the errand, if the boy walks in already carrying the breakfast (he met Titus first, and the geese went):
  "rome.keeper.carrying.1": ["keeper", "My cloth, the old one's breakfast, where is my boy, where is my Titus?"],
  "rome.keeper.carrying.2": ["son", "He's on his way home. He was stuck on a statue with geese all round, so I did a stomp."],
  "rome.keeper.carrying.3": ["keeper", "Every Ides something, up the street with it, quick, before it is a lunch."],
  // The first time he is talked to once Titus is home (rome.metTitus and rome.hasBreakfast):
  "rome.keeper.titus.1": ["keeper", "My boy is home, he says your shoes frightened Juno's geese, have a sausage."],
  "rome.keeper.titus.2": ["son", "I won't even ask about the ketchup. I've grown as a person."],
  // the two new things carried, shown to him
  "rome.keeper.gaultoga": ["keeper", "That is not a toga, that is a tent, I cannot pay to wash a tent."],
  "rome.keeper.lamp": ["keeper", "For Felix, for Corinth, I know. Everybody eats here, so I hear everything."],

  // ---------- the washerwoman and her laundry ----------
  "rome.washer.look": ["narrator", "The washerwoman folds a sheet in four moves. Dad once fought one for ten minutes and lost."],
  "rome.washer.look2": ["narrator", "She has arms like the doorkeeper's. The Son would like to watch that arm wrestle, and would bring snacks."],
  "rome.washer.hi.1": ["washer", "Mind the basket. Those are clean, and you are not."],
  "rome.washer.hi.2": ["son", "I'm travel dirty. That's different, it's got miles on it."],
  "rome.washer.hi.3": ["washer", "A hood with no head in it. Whoever dresses you enjoys a joke."],      // PASS-17R: true to the picture (no cap; his hood is down)
  "rome.washer.hi.4": ["son", "That's my mom, and you'd like her. You both look at my knees the same way."],
  "rome.washer.errand.1": ["washer", "Can you run, child? The senator is up at the temple steps, turning purple for want of his toga."],
  "rome.washer.errand.2": ["washer", "I cannot leave the tubs. Take him his toga, and when you come back I will lend you a tunic."],
  "rome.washer.errand.3": ["son", "Deal. I'll carry it by the corners."],
  "rome.washer.ask.white": ["son", "How do you get them so white?"],
  "rome.washer.ans.white.1": ["washer", "We tread them in the tubs, in stale urine. Nothing whitens like it."],
  "rome.washer.ans.white.2": ["son", "Urine? You mean pee?"],
  "rome.washer.ans.white.3": ["washer", "Is there another kind?"],
  "rome.washer.ans.white.4": ["son", "Best fact ever. My sister will be so mad I knew it first."],
  "rome.washer.ans.white.6": ["son", "Wait. This bedsheet I'm holding..."],
  "rome.washer.ans.white.7": ["washer", "Was rinsed. Twice."],
  "rome.washer.ans.white.8": ["son", "I'm going back to the corners."],
  "rome.washer.ask.tunic": ["son", "About that tunic..."],
  "rome.washer.ans.tunic": ["washer", "Toga first, then tunic. I have run twenty years of laundry on 'first' and 'then'."],
  "rome.washer.ask.dad": ["son", "Seen my dad? Little beard, and a flowered shirt you'd definitely remember."],      // PASS-17R: was the doorkeeper's words exactly; now she answers it
  "rome.washer.ans.dad.1": ["washer", "Flowers on a shirt? No, I would remember washing that."],
  "rome.washer.ask.bye": ["son", "I'll be careful with your bedsheets."],
  "rome.washer.ans.bye": ["washer", "Togas. Go on with you."],
  "rome.washer.tunic.1": ["son", "Delivered. He said Rome thanks you, because he was too late to say it himself."],
  "rome.washer.tunic.2": ["washer", "That sounds like him. Here, my sister's boy outgrew this one, so bring it back clean."],
  "rome.washer.tunic.3": ["son", "A real Roman tunic. It's a dress with a belt, so nobody tell my school."],
  "rome.washer.toga": ["washer", "Not to me, to him. He is up at the temple steps, the color of a plum."],
  "rome.washer.coin": ["washer", "That has been in the fountain. I wash cloth, child, not wishes."],
  "rome.washer.breakfast": ["washer", "Keep that from the whites. One drip of sausage and I start the day again."],
  "rome.washer.tunic.back": ["washer", "Keep it till sundown. And keep it out of the sauce."],

  // ---------- ROME-13W: the washerwoman's mix-up (decision 2), shown the Gaul's toga ----------
  // The first time: mortified, briefly, and then brisk again. After that: .again.
  "rome.washer.gaultoga.1": ["son", "This isn't the senator's, it's a Gaul's. It reaches the ground twice."],
  "rome.washer.gaultoga.2": ["washer", "A big man came in the dark for 'the senator's toga'. I gave him the senator's."],
  "rome.washer.gaultoga.3": ["washer", "Twenty years on first and then, and I gave the wrong first."],
  "rome.washer.gaultoga.4": ["washer", "Find the Gaul, child, the big lost one with his knees out. Go."],
  "rome.washer.gaultoga.again": ["washer", "I know, child. Find the Gaul, and never say a word of it to my sister."],
  "rome.washer.lamp": ["washer", "Oil and wool do not mix, child. Keep that lamp away from my tubs."],

  "rome.laundry.look": ["narrator", "Togas hung to dry right across the street. It looks as though the sleepover put up decorations."],
  "rome.laundry.look2": ["narrator", "The white one on the line almost glows. So that is what clean looks like; the Son had forgotten."],
  "rome.tunic.look": ["narrator", "A boy's tunic on the line, about the Son's size: a long T-shirt that gave up on sleeves."],
  "rome.tunic.hands": ["washer", "Hands off the line, child. Those are counted."],
  "rome.basket.look": ["narrator", "A basket of wet laundry, which looks a good deal heavier than the Son."],
  "rome.basket.look2": ["narrator", "The basket of wet laundry. Knowing what it was washed in, the Son admires it from where he stands."],
  "rome.basket.use.1": ["washer", "Not the basket, child."],
  "rome.basket.use.2": ["son", "I wasn't going to. Well, I was a little going to."],

  // ---------- the fountain ----------
  "rome.fountain.look": ["narrator", "A street fountain with coins lying at the bottom. People here throw money into water on purpose, and the Son loves them for it."],   // kept
  "rome.fountain.take": ["son", "Operation Borrow-A-Wish is go. Splish."],                                                           // kept
  "rome.fountain.again": ["narrator", "One wish is borrowing. Two would be a crime spree, and the Son leaves the rest where they lie."],                                                     // kept
  "rome.fountain.shiny": ["son", "It's so shiny I can see my face in it, right next to the serious man's. He isn't happy about it."],
  "rome.fountain.wish.1": ["urchin", "That's somebody's wish, you know."],
  "rome.fountain.wish.2": ["son", "I'm only borrowing it. I'll pay it back with interest, and interest is extra wishes."],
  // ROME-13W (#7 Borrow A Wish, then decision 7): after the kept lines above, Walnut says whose wish it was, and the boy
  // answers (rome.knowsWish). Then his look at the coin, as before.
  "rome.fountain.wish.3": ["urchin", "It's Phyllis's, the garland woman by Castor's temple. It's for her boy."],
  "rome.fountain.wish.4": ["son", "Then I'll ask her. You can borrow a wish, but you can't throw one away."],
  // woven: his first hard look at it. Matthew 22:17-21 in his own words (the verse itself is Mom's, in Act Four).
  "rome.fountain.caesar.2": ["son", "It says Caesar on it. Like when Jesus asks whose picture is on the coin."],
  "rome.fountain.caesar.2.b": ["urchin", "Caesar's. Everybody knows that nose."],  // PASS-19R1: new, after rome.fountain.caesar.2
  "rome.fountain.caesar.3": ["son", "So Caesar gets his coin, and God gets what's God's. Me included."],
  "rome.fountain.caesar.4": ["son", "But Jesus is grown up in that story, so this isn't that Caesar. Not yet."],
  "rome.fountain.toga": ["narrator", "Dunking a clean toga in the fountain would be a mistake. The washerwoman has arms, and the Son has seen them."],
  "rome.fountain.quarter": ["narrator", "The Son keeps his quarter. Somebody would dig it up in two thousand years and have a great many questions."],
  "rome.fountain.phone": ["narrator", "The phone is already dead. It does not need to be drowned as well."],
  "rome.fountain.coin": ["narrator", "The Son does not throw it back. He is saving this wish for something big, or possibly something small."],

  // ---------- the street boy ----------
  "rome.urchin.look": ["narrator", "A boy about the Son's age, playing marbles with walnuts. At last, somebody who is not a grown-up."],
  "rome.urchin.look2": ["narrator", "The street boy keeps looking at the Son's shoes. He has good taste."],
  "rome.urchin.hi.1": ["urchin", "Your feet are on fire."],
  "rome.urchin.hi.2": ["son", "They light up when I stomp. Watch."],
  "rome.urchin.hi.3": ["urchin", "Do it again."],
  "rome.urchin.hi.4": ["son", "That one was free. From now on it's a walnut a stomp."],
  "rome.urchin.hi.5": ["urchin", "I'm the best at nuts on this street, and you're the best at feet. Friends?"],
  "rome.urchin.hi.6": ["son", "Deal. I'm calling you Walnut."],
  "rome.urchin.ask.game": ["son", "How do you play the walnut game?"],
  "rome.urchin.ans.game.1": ["urchin", "You build a castle of nuts and throw one at it. Knock it down and they're yours."],
  "rome.urchin.ans.game.2": ["son", "Like bowling, but you keep the pins. Then you eat the pins."],
  "rome.urchin.ans.game.3": ["son", "Oops. I missed the castle and hit a pigeon."],
  "rome.urchin.ans.game.4": ["urchin", "The pigeon's fine. That's two nuts you owe me."],
  "rome.urchin.ans.game.5": ["son", "One hour in Rome and I'm already in nut debt."],
  "rome.urchin.ask.temple": ["son", "Have you ever been inside the temple?"],
  "rome.urchin.ans.temple.1": ["urchin", "Me? You need a clean tunic and a father who knows somebody. I've got a tunic."],
  "rome.urchin.ans.temple.2": ["son", "I've got a father. I just don't know where he is. It's a long story with a tunnel in it."],
  "rome.urchin.ans.temple.3": ["urchin", "You lost your father? Then you can share the sausage man, like everybody does."],
  "rome.urchin.ask.help": ["son", "I'm stuck, Walnut. What would you do?"],
  "rome.urchin.ask.light": ["son", "Walnut. How do you get light onto a wall in the dark?"],
  "rome.urchin.ask.tiny": ["son", "There's a door in there the size of a coin. What do you do with that?"],
  "rome.urchin.tip.rule": ["urchin", "Ask old Doorpost what he does let in. He loves a rule."],
  "rome.urchin.tip.toga": ["urchin", "A clean tunic? The laundry woman across the street has a hundred, and nobody to run her errands."],
  "rome.urchin.tip.deliver": ["urchin", "That's the senator's toga. He's the angry one at the temple steps, the purple one. Run."],
  "rome.urchin.tip.tunic": ["urchin", "You did her job, so go and get your tunic. She keeps her word, that one."],
  "rome.urchin.tip.breakfast.1": ["urchin", "Something for the god? Old Gloom on the steps has incense. But he won't part with a thing on an empty belly."],
  // ROME-13W: re-worded (it was "...Today it's still on the counter."): the breakfast went up the hill with the keeper's boy.
  "rome.urchin.tip.breakfast.2": ["urchin", "The sausage man's boy took Old Gloom's breakfast up at first light. He never came back down."],
  "rome.urchin.tip.incense": ["urchin", "Old Gloom's breakfast is going cold in your bag. Take it to him, the old one with the chickens."],
  "rome.urchin.tip.inside": ["urchin", "You've got the tunic and the incense, so go on up the steps, before Doorpost thinks of a fourth rule."],
  "rome.urchin.tip.shiny.1": ["urchin", "Easy. Catch the sun on something shiny and throw it where you like. I do it to the sausage man."],
  "rome.urchin.tip.shiny.2": ["urchin", "The shiniest things on this street? New silver, lying in the fountain."],
  "rome.urchin.tip.spark": ["urchin", "You've got something shiny. Now find where the sun comes in, and bounce it."],
  "rome.urchin.tip.toss": ["urchin", "A door the size of a coin? Then put a coin through it. What else fits?"],
  // ROME-13W: his tips for the new beats, in the beats' order. tip.gaul also says where the Senate meets today, so that
  // the boy has heard it from him too (rome.knowsSenate). tip.gaul, .redeliver and .geese answer "I'm stuck, Walnut. What
  // would you do?"; tip.wish, .felix and .granted answer the door the size of a coin (rome.urchin.ask.tiny), as .toss does.
  "rome.urchin.tip.gaul": ["urchin", "Big Gaul, little toga? Tell him they meet in Pompey's hall, by the theater."],
  "rome.urchin.tip.redeliver": ["urchin", "Got the right toga? Run it to the senator at the temple steps, he's going purple."],
  "rome.urchin.tip.geese": ["urchin", "The Capitol geese scream at anything they've never seen before. Ask the Gauls. They found out."],   // FINAL-19: REVIEW-19's patch
  "rome.urchin.tip.wish": ["urchin", "Put a coin through. But that one's Phyllis's wish, so ask her first, at Castor's temple."],
  "rome.urchin.tip.felix": ["urchin", "The lamp comes first. Felix works the barges, over the stone bridge. He's big and sunburnt."],
  "rome.urchin.tip.granted": ["urchin", "Felix said yes? Then tell Phyllis before you throw anything, because it's her wish."],
  "rome.urchin.ask.bye": ["son", "See you, Walnut."],
  "rome.urchin.ans.bye": ["urchin", "Stomp when you go. So I can watch."],
  "rome.urchin.gum.1": ["son", "Want some gum? You chew it, but you don't swallow it."],
  "rome.urchin.gum.2": ["urchin", "Then what's it for?"],
  "rome.urchin.gum.3": ["son", "Nobody knows. It's minty, though."],
  "rome.urchin.gum.4": ["urchin", "It's fighting back. I like it."],
  "rome.urchin.coin.1": ["urchin", "That's fountain silver. It's still wet."],
  "rome.urchin.coin.2": ["son", "It's a borrowed wish."],
  "rome.urchin.coin.3": ["urchin", "My whole life on this street, and I never once thought of borrowing one."],
  "rome.urchin.phone.1": ["urchin", "A black tile."],
  "rome.urchin.phone.2": ["son", "It takes pictures, when it's alive."],
  "rome.urchin.phone.3": ["urchin", "Pictures of what?"],
  "rome.urchin.phone.4": ["son", "Mostly a donkey."],
  "rome.urchin.quarter.1": ["urchin", "There's a bird on the back. Is it worth a walnut?"],
  "rome.urchin.quarter.2": ["son", "It's worth twenty-five cents. Here, honestly, that's about a walnut."],
  "rome.urchin.toga": ["urchin", "A senator's toga! Don't let it touch me, I'm mostly ground."],
  "rome.urchin.breakfast": ["urchin", "That's Old Gloom's, I can smell it. I'm being very brave about it."],
  // ROME-13W: a game saved with the coin borrowed before Walnut said whose it was: he says so the next time the boy walks
  // into the street (rome.knowsWish). And the two new things carried, shown to him.
  "rome.urchin.wish.1": ["urchin", "That wish you borrowed is Phyllis's. The garland woman, at Castor's temple."],
  "rome.urchin.wish.2": ["son", "Then I'll ask her. Borrowing's fine, but throwing somebody's wish away isn't."],
  "rome.urchin.gaultoga": ["urchin", "That's a Gaul's. You could fit the Gaul and me in there."],
  "rome.urchin.lamp": ["urchin", "That's Phyllis's lamp. Don't drop it, she'd know from across the river."],

  // ---------- the date seller (woven: all of him) ----------
  // A Jew from Judea, about fifty, selling dates from Jericho on the right-hand pavement. Courteous, humorous,
  // unhurried, nobody's fool. He is part of no puzzle and gives nothing that is carried. He says nothing about
  // the Romans' gods, and nobody tells him anything about the future: the Son, for once, holds his tongue.
  "rome.dateseller.look": ["narrator", "A man selling what look to the Son like giant raisins. He is the only person in Rome not in a hurry."],
  "rome.dateseller.look2": ["narrator", "The date seller keeps looking a long way off, past the roofs, like a man who has been waiting for somebody for years."],
  "rome.dateseller.hi.1": ["dateseller", "Dates, young sir, from Jericho. There are none better in Rome: I have looked, and I have tasted."],
  "rome.dateseller.hi.2": ["son", "Jericho? The Jericho with the walls?"],
  "rome.dateseller.hi.3": ["dateseller", "You know of the walls? The palms of Jericho have done better than its walls, young sir."],      // PASS-17R: he wears no hat; his shoes are what Rome sees
  "rome.dateseller.ask.try": ["son", "Can I try one? I'm between snacks."],
  "rome.dateseller.ans.try.1": ["dateseller", "For a boy who knows of Jericho, the first one is a gift. Here. Mind your teeth."],
  "rome.dateseller.ans.try.2": ["son", "It's candy that grows on trees. Nine out of... ow! There's a rock in it."],
  "rome.dateseller.ans.try.3": ["dateseller", "The stone. That part is a palm tree not yet begun. By rights I ought to charge you for the tree."],
  "rome.dateseller.ask.god": ["son", "Everybody here prays to a statue. Which one's yours?"],
  "rome.dateseller.ans.god.1": ["dateseller", "None. We have one God, the God of Abraham, of Isaac and of Jacob."],
  "rome.dateseller.ans.god.2": ["son", "I know those guys! He's our God too, and we pray to Him at my house."],      // PASS-17R: they pray to Abraham's God, not to Abraham
  "rome.dateseller.ans.god.3": ["dateseller", "At your house. Then the world is larger than Rome has told me."],
  "rome.dateseller.ans.god.4": ["dateseller", "Rome finds us Jews very funny: a great Temple in Jerusalem, and no statue in it."],
  "rome.dateseller.ans.god.4.b": ["son", "Then what's in it?"],  // PASS-19R1: new, after rome.dateseller.ans.god.4
  "rome.dateseller.ans.god.5": ["dateseller", "Pompey himself went in, nineteen years ago, and he found no image. Not one."],
  "rome.dateseller.ans.god.6": ["dateseller", "How would they carve the One who made the stone? They buy their dates and go."],
  "rome.dateseller.ask.pray": ["son", "What do you pray for?"],
  "rome.dateseller.ans.pray.1": ["dateseller", "For the promised one, every day, facing Jerusalem. Micah has told us his town:"],
  "rome.dateseller.ans.pray.2": ["dateseller", "'But thou, Bethlehem Ephratah, though thou be little among the thousands of Judah,'"],          // Micah 5:2, King James Version, the first clause: exact, comma and all
  "rome.dateseller.ans.pray.3": ["son", "That was my line in the Christmas program! I know so much about Bethlehem."],      // PASS-17R: no reference aloud: where he knows it from
  "rome.dateseller.ans.pray.4": ["son", "I've never wanted to tell anybody something so much. But telling it is the angels' job, not mine."],      // PASS-17R: a boy's words for it
  "rome.dateseller.ans.pray.4.b": ["dateseller", "Young sir?"],  // PASS-19R1: new, after rome.dateseller.ans.pray.4
  "rome.dateseller.ans.pray.5": ["son", "It's going to be worth the wait, mister. Keep watching that town."],
  "rome.dateseller.ans.pray.6": ["dateseller", "That was not a guess. I will not ask you what it was. But I will watch."],
  // (The id of the blessing is chosen with care: the engine picks each line's gesture from its id, and this one
  // gives him a hand laid on his chest. Renumber it and he may bless the boy with a shrug, or with a date in his hand.)
  "rome.dateseller.bless.1": ["dateseller", "And for you, young sir: 'The LORD bless thee, and keep thee:'"],                                   // Numbers 6:24, King James Version: exact, colon and all
  "rome.dateseller.bless.2": ["son", "That's how church ends back home, the very same words. Thanks, mister."],      // PASS-17R: no reference aloud
  "rome.dateseller.ask.bye": ["son", "Bye, mister."],
  "rome.dateseller.ans.bye": ["dateseller", "Go well, and come any day but the seventh. I rest, and Rome always wants dates."],
  "rome.dateseller.quarter.1": ["dateseller", "An eagle? Whoever struck this was proud of his bird, though it is not silver."],
  "rome.dateseller.quarter.2": ["dateseller", "A coin should go home. Ours go to the Temple in Jerusalem: the half-shekel."],
  "rome.dateseller.phone": ["dateseller", "A black mirror. It shows an old man selling dates, and it is not wrong."],
  "rome.dateseller.toga": ["dateseller", "A senator's toga. He buys my best dates and remembers them as cheaper."],
  "rome.dateseller.coin.1": ["dateseller", "Caesar has been a friend to us Jews of Rome. We may meet, and keep our ways."],
  "rome.dateseller.coin.2": ["dateseller", "But that is fountain silver, young sir: somebody's wish, and not a price."],
  // chickens: the soothsayer's breakfast, shown to him. He will not have his fortune told by hens, thank you. (A small shrug.)
  "rome.dateseller.breakfast": ["dateseller", "The soothsayer's. He keeps offering to read my fortune by his hens. Not by hens, thank you."],
  // ROME-13W (woven): once, after his blessing (rome.dateseller.bless.2) or at his goodbye, whichever comes first. He is
  // in no puzzle; this points the way to his wife's father, across the river. And the two new things carried, shown to him.
  "rome.dateseller.eleazar": ["dateseller", "My wife's father Eleazar reads in the house of prayer over the river. Greet him."],
  "rome.dateseller.gaultoga": ["dateseller", "That toga could shelter a family. Mine, for instance."],
  "rome.dateseller.lamp": ["dateseller", "A good little lamp. Whoever it is for, may it light a good house."],

  // ---------- the rest of the street ----------
  "rome.stones.look": ["narrator", "Stepping stones across the street, so that feet stay out of whatever runs down it. Good thinking, Rome."],
  "rome.stones.look2": ["narrator", "Stepping stones in a Roman road. Paul comes into Rome by a road like this one day; it is a dotted line in the Son's Bible."],   // woven: Acts 28:15-16. PASS-17R: shorter, and his own (the map), not a lesson
  "rome.cat.look": ["narrator", "A cat, ignoring an entire city. Cats were already like this."],
  "rome.cat.use": ["narrator", "The Son calls the cat and is ignored, exactly as he would be in his own century."],
  "rome.shrine.look": ["narrator", "A little street shrine: a painted snake, a tiny house and a lamp burning. It is nicer than the Son's room."],
  "rome.notices.look": ["narrator", "A name painted on the wall: MARCVS. They spelled Marcus with a V, and the Son hopes nobody tells Marcus."],
  "rome.notices.look2": ["narrator", "Another notice says VOTA. Somebody is running for something; Rome has yard signs, only on walls."],
  "rome.rufus.look": ["narrator", "RVFVS, painted on the wall. That is Rufus, or else the noise a dog makes when it is being fancy."],
  "rome.flats.look": ["narrator", "Four floors of apartments and no elevator. Everyone up there has the face of someone carrying the shopping."],
  "rome.jars.look": ["narrator", "Tall jars with pointed bottoms, which cannot stand up on their own. Neither can the Son, before breakfast."],
  "rome.wheel.look": ["narrator", "A cart wheel as tall as the Son, with no tire on it. That cart must feel every stone."],
  "rome.sign.look": ["narrator", "A shop sign with a jug and grapes on it. Pictures: at last somebody in Rome understands."],
  "rome.songbird.look": ["narrator", "A bird in a cage, singing its head off. The cat is a great admirer of its work."],

  // ================= rome-temple: inside the temple, the treasury =================

  "rome.inside.1": ["clerk", "Four hundred and eleven, four hundred and twelve..."],
  "rome.inside.2": ["son", "Tunic off. It itches like a sweater made of hay, so Romans must be tough."],
  "rome.inside.4": ["son", "Hi, door. I can hear you, and you're terrible at hide-and-seek."],
  "rome.inside.5": ["clerk", "Four hundred and... who is talking? No, do not tell me. One. Two."],
  "rome.out.look": ["narrator", "The way out, past the doorkeeper. He likes the Son now, and hides it very well."],

  // ---------- the place that hums, and the sunlight ----------
  "rome.hole.look": ["narrator", "A place in the wall that hums. Dad says it is the wind; Dad says everything is the wind, and the Son keeps a list."],                   // kept
  "rome.hum.try.1": ["son", "Back in the big pointy place, I shined my flashlight at the hum, and pop: a door."],
  "rome.hum.try.2": ["son", "My flashlight got left behind. Fine, I'll use the phone light."],
  "rome.hum.try.2.b": ["clerk", "No lights near the silver. One."],  // PASS-19R1: new, after rome.hum.try.2
  "rome.hum.try.3": ["narrator", "The Son's phone is at zero percent. It cannot even be sad about it."],
  "rome.hum.try.4": ["son", "So the door likes light. I need a light that doesn't need charging."],
  "rome.hum.again": ["narrator", "The hum is still shut. It wants light, and all the light in here is lying on the floor in the sunny patch."],
  "rome.hum.coin": ["narrator", "It is too dark over here. A coin is only shiny when it has some sun to be shiny with."],
  "rome.hum.gum": ["narrator", "The Son is not sticking gum on a time door. He has seen what gum does to a desk."],
  "rome.hum.incense": ["narrator", "The incense is for the statue. The door likes light, and the Son is new at doors."],
  "rome.sun.look": ["narrator", "A patch of sunshine lying on the floor. It is free light, and nobody is using it."],
  "rome.sun.look2": ["narrator", "The sun is here and the hum is over there. Somebody shiny ought to introduce them."],
  "rome.sun.use.1": ["narrator", "The sunshine is warm on the Son's hand. Something shiny could bounce it onto the wall, as his spoon does at breakfast."],
  "rome.sun.use.2": ["narrator", "Mom has asked him to stop doing that with the spoon. She asks about twice a week."],
  "rome.sun.done": ["narrator", "The little door is open. There is no need to dazzle the clerk a second time."],
  "rome.sun.phone": ["narrator", "The cracked screen scatters a hundred tiny lights in every direction. It is pretty, and no use at all."],
  "rome.sun.gum": ["narrator", "The gum is wrapped in paper, not foil. It was not packed with time travel in mind."],
  "rome.sun.quarter": ["narrator", "The quarter has been through the wash and has no shine left. This wants a new coin, a bright one."],

  // the spark: a spot of sunlight off the coin, and a door the size of the coin
  "rome.spark.1": ["son", "Sun, meet coin. Coin, meet wall."],
  "rome.spark.2": ["clerk", "Five hundred and six, five hundred and sev... agh, my eye!"],
  "rome.spark.3": ["son", "Sorry. Wrong wall."],
  "rome.spark.4": ["clerk", "What was that light?"],
  "rome.spark.5": ["son", "It's the sun. It does that sometimes, it's a known sun thing."],
  "rome.spark.6": ["clerk", "One. Two. Three."],
  "rome.spark.8": ["son", "Pop! A door, a tiny one, exactly the size of the coin."],
  "rome.spark.10": ["son", "There's sky in there, really far down. Why is the sky down?"],

  // the door, once it is open, and the toss that ends the act
  "rome.door.look": ["narrator", "A door the size of a coin, with sky in it. The Son's eye fits; the rest of him will have to wait."],
  "rome.hole.use": ["narrator", "The Son is not jumping into a time door again without a snack. He made that rule up just now, and he stands by it."],   // kept
  "rome.hole.use2": ["narrator", "He is also a good deal bigger than a coin. Physics made that rule up."],
  "rome.hole.quarter": ["narrator", "Not the quarter. George is the only other American in Rome, and the two of them are sticking together."],
  "rome.hole.phone": ["narrator", "The phone will not fit, and a dead phone is not the message the Son wants to send Dad."],
  "rome.hole.coin": ["son", "Heads, I find Dad. Tails, Dad finds me. Edge, we get a dog."],                                       // kept
  "rome.hole.coin2": ["son", "It never came back down. Does that count as edge? Because then we get the dog."],                        // kept

  // ---------- ROME-13W: the toss waits for Phyllis's leave (#9, decision 7), and the lamp tried in here ----------
  // The coin used on the coin-sized door without rome.wishGranted: this line, and nothing else happens. With it, as above.
  "rome.hole.wish": ["son", "This is Phyllis's wish. I'm not throwing it through a door without asking."],
  "rome.hum.lamp": ["narrator", "The lamp is not lit, and it is not the Son's to light. It is a goodbye present."],
  "rome.hole.lamp": ["narrator", "Felix's lamp does not go through a time door. He would only end up lighting it in the wrong century."],
  "rome.sun.lamp": ["narrator", "The lamp is clay, and clay does not shine. The coin is the shiny one."],
  "rome.statue.lamp": ["narrator", "The lamp is for Felix. The god has plenty of things already."],
  "rome.clerk.lamp": ["clerk", "An unlit lamp, which in a treasury is the only good kind. One."],

  // ---------- the god, the treasure, the clerk ----------
  "rome.statue.look": ["narrator", "A huge statue of an old man holding a hooked knife, with wool tied round his feet."],
  "rome.statue.look2": ["narrator", "Somebody has tied the god's feet together. The Son supposes he is either dangerous or a sleepwalker."],
  "rome.statue.use": ["narrator", "The Son is not untying a god's feet. He still needs bunny ears to tie his own laces."],
  "rome.statue.incense.1": ["son", "This is from the chicken man, who's sorry about the steps. And beware of today."],
  "rome.statue.incense.2": ["clerk", "Sixty-one, sixty-two... in the bowl, boy, not beside it. One."],
  "rome.statue.coin": ["narrator", "A whole building full of money stands round him. The god does not need the Son's wish; he needs his feet."],
  "rome.statue.gum": ["narrator", "No gum for the statue. With his feet tied he would never get it off his shoe."],
  "rome.bowl.look": ["narrator", "The offering bowl at the god's feet. It is empty, and the Son knows that feeling."],
  "rome.bowl.done": ["narrator", "The incense sits in the bowl at the god's feet. That is three deliveries out of three, counting the sausage."],

  "rome.chests.look": ["narrator", "Treasure chests with real locks on them. It is the best room the Son has ever been thrown out of."],
  "rome.chests.look2": ["narrator", "Sacks with seals and chests bound in iron. Somebody really does not want to share."],
  "rome.chests.use.1": ["clerk", "Do not touch the Roman People's money."],
  "rome.chests.use.2": ["son", "I was only looking. With my hands."],
  "rome.chests.use.3": ["clerk", "One."],
  "rome.bankcat.look": ["narrator", "A cat asleep on the treasure. Nobody scores the cat out of three."],
  "rome.bankcat.use.1": ["narrator", "The Son says hello to the cat, and she purrs. That makes two things in here that hum."],
  "rome.bankcat.use.2": ["clerk", "Ninety-one... leave her be. She is the one thing in here I do not have to count."],
  "rome.bankcat.coin": ["narrator", "She is asleep on a chest full of them. One more coin will not impress her."],
  "rome.table.look": ["narrator", "The clerk's table: a scale, a lamp, wax tablets and a mountain of silver. It is homework, but shiny."],
  "rome.table.use.1": ["clerk", "Away from the table. I have piles, and the piles have an order."],
  "rome.table.use.2": ["son", "They look like piles."],
  "rome.table.use.3": ["clerk", "That is how I know you are not a clerk."],

  "rome.clerk.look": ["narrator", "The clerk, counting a mountain of coins one at a time. It is like Dad doing the taxes, forever."],
  "rome.clerk.look2": ["narrator", "When the Son breathes loudly, the clerk flinches. The Son breathes very quietly, and the clerk flinches anyway."],
  "rome.clerk.hi.1": ["clerk", "Seven hundred and eight, seven hundred and nine..."],
  "rome.clerk.hi.2": ["son", "Hi!"],
  "rome.clerk.hi.3": ["clerk", "Seven hundred and... no. It is gone. It has gone."],
  "rome.clerk.hi.4": ["clerk", "The incense boy. The bowl is at the god's feet, and I am at one. Again."],
  "rome.clerk.again": ["clerk", "Two hundred and thirty... you. Of course. One."],
  "rome.clerk.ask.count": ["son", "What are you counting?"],
  "rome.clerk.ans.count.1": ["clerk", "The silver of the Roman People. Every denarius, twice, so the counts agree."],
  "rome.clerk.ans.count.2": ["son", "Do they ever agree?"],
  "rome.clerk.ans.count.3": ["clerk", "They did once, in my second year. I think of it often."],
  "rome.clerk.ask.feet": ["son", "Why are the statue's feet tied up?"],
  "rome.clerk.ans.feet.1": ["clerk", "Bands of wool. They are untied once a year, at his festival in December."],
  "rome.clerk.ans.feet.2": ["son", "One day off a year? Even Dad gets two weeks."],
  "rome.clerk.ans.feet.3": ["clerk", "I get the same day he does. We do not spend it together."],
  "rome.clerk.ask.hum": ["son", "Do you hear a hum? Over by that wall?"],
  "rome.clerk.ans.hum.1": ["clerk", "Since dawn. First a hum, then a flash, then a noise like a boy falling over."],
  "rome.clerk.ans.hum.2": ["clerk", "I did not look up. I was at nine hundred."],
  "rome.clerk.ans.hum.3": ["son", "That was... probably the wind."],
  "rome.clerk.ans.hum.4": ["clerk", "That is what I decided."],
  // woven: the governor of Galilee is the King Herod of Matthew 2. Not this year. (This one does not get the tag: three is the limit.)
  "rome.clerk.ask.judea": ["son", "What's on all the wax pads?"],
  "rome.clerk.ans.judea.1": ["clerk", "Judea's accounts. Antipater's, and his son Herod's, who governs Galilee."],
  "rome.clerk.ans.judea.2": ["son", "Herod? You mean King Herod, the bad king in the Christmas story?"],
  "rome.clerk.ans.judea.3": ["clerk", "Herod is no king. He is a procurator's son with expensive tastes. I have the figures."],
  "rome.clerk.ans.judea.4": ["son", "I'd count him twice. I'm just saying."],
  "rome.clerk.ask.dad": ["son", "Have you seen my dad?"],
  "rome.clerk.ans.dad.1": ["clerk", "Is he made of silver?"],
  "rome.clerk.ans.dad.2": ["son", "No."],
  "rome.clerk.ans.dad.3": ["clerk", "Then I have not counted him."],
  "rome.clerk.ask.bye": ["son", "I'll let you count."],
  "rome.clerk.ans.bye": ["clerk", "Everyone says that. One."],
  "rome.clerk.coin.1": ["clerk", "Is that one of mine?"],
  "rome.clerk.coin.2": ["son", "No! It's a wish."],
  "rome.clerk.coin.3": ["clerk", "Good. If I had to count wishes as well, I would lie down on the floor."],
  "rome.clerk.quarter": ["clerk", "It is not silver, it is not Roman, and I refuse to count it."],
  "rome.clerk.phone.1": ["clerk", "A writing tablet with no wax. What do you scratch on?"],
  "rome.clerk.phone.2": ["son", "You don't scratch it, you poke it. When it's alive."],
  "rome.clerk.phone.3": ["clerk", "I was happier not knowing that."],
  "rome.clerk.incense": ["clerk", "That is for the god, not for me. Put it in the bowl, quietly."],

  "rome.brazier.look": ["narrator", "A brazier, burning like an indoor campfire. The Son has checked, and there are no marshmallows."],
  "rome.brazier.use": ["narrator", "It is hot, very hot. The Son decides this is a campfire for looking at only."],
  "rome.tablets.look": ["narrator", "Bronze tablets nailed to the wall, in very small letters. They seem to be all the rules there are."],
  "rome.standards.look": ["narrator", "Poles with shining badges on top, for carrying in parades. Rome keeps its parade in the bank."],
  "rome.rack.look": ["narrator", "The clerk's rack of cubbyholes, like the ones at school, with scrolls in place of lunches."],

  // ================= ROME-13W: rome-forum: the Forum, from its east end =================
  // The open heart of Rome, looking west along its length to the temple of Saturn at the far end, small, and the Capitol
  // above everything. Reached from the steps' bottom edge once he knows it is B.C.

  // ---------- arrival (the first time: rome.sawForum) ----------
  "rome.forum.arrive.1": ["son", "A church, a bank and a construction site. Ten out of ten, and eleven for the crane."],
  "rome.forum.arrive.2": ["son", "That's my temple, way down at the end. Hi, door guy! He never, ever waves back."],
  "rome.forum.arrive.3": ["son", "And there's a gold roof up on the hill. Rome doesn't do things halfway."],

  // ---------- the things in it (a second look where one is worth it) ----------
  "rome.forum.castor.look": ["narrator", "Castor's temple, with a front porch as high as a stage. Mom would put on a play there."],      // PASS-17R: his mother and the stage
  "rome.forum.castor.look2": ["narrator", "The flower lady has her place at the foot of the temple steps, where everybody in Rome walks past."],
  "rome.forum.castor.use": ["narrator", "The Son stays off the temple's porch. Somebody up there would make him say something."],
  "rome.forum.spring.look": ["narrator", "A stone pool with a spring rising in it: the street fountain's quiet cousin."],      // PASS-17R: shorter
  "rome.forum.spring.use": ["narrator", "The Son splashes his face. The water is very cold; he gives it two out of ten and is extremely awake."],      // PASS-17R: not every score is a ten
  "rome.forum.spring.coin": ["narrator", "Nobody moves somebody else's wish to a different pool. The Son keeps the coin."],
  "rome.forum.garlands.look": ["narrator", "Baskets of violets, and garlands woven of them. They smell like Grandma's bathroom."],      // PASS-17R: shorter
  "rome.forum.garlands.use": ["phyllis", "Hands off the garlands, child. Smell all you like with your nose. That part is free."],
  "rome.forum.tuscan.look": ["narrator", "A street going downhill toward the river. It smells of river, and a little of cows."],
  "rome.forum.julia.look": ["narrator", "A long hall of arches, half brand new and half scaffolding, like the Son's science project."],      // PASS-17R: shorter
  "rome.forum.scaffold.look": ["narrator", "Scaffolding on the end of the hall. Rome is under construction, all of it."],
  "rome.forum.scaffold.use": ["narrator", "Mom has a rule about climbing scaffolding. It is the same as her rule about climbing everything else."],
  "rome.forum.puteal.look": ["narrator", "A round stone ring in the pavement, like the top of a well with no well under it."],
  "rome.forum.puteal.use": ["narrator", "Everybody walks around it, so the Son does too. There is always a story behind a thing like that."],
  "rome.forum.table.look": ["narrator", "A table of coins with nobody minding it. Whoever owns it is plainly coming right back."],
  "rome.forum.table.use": ["narrator", "The Son does not touch the money. He has a wish to worry about already."],
  "rome.forum.table.coin": ["narrator", "The Son does not leave the coin on the money table. It is a wish, not a deposit."],
  "rome.forum.table.quarter": ["narrator", "Swapping George for silver while nobody is looking would work, which is exactly why the Son will not do it."],
  "rome.forum.statues.look": ["narrator", "Statues set up high where only pigeons can reach them. The pigeons are winning."],
  "rome.forum.rostra.look": ["narrator", "A long stone platform for speeches, with bronze ships' beaks along its front and statues addressing nobody."],
  "rome.forum.rostra.use": ["narrator", "If the Son made a speech it would be about snacks, and nobody would leave. He saves it for another day."],
  "rome.forum.saturn.look": ["narrator", "The temple of Saturn, far down at the end of the square. From here the doorkeeper is a dot."],
  "rome.forum.saturn.look2": ["narrator", "The dot has just folded its arms. The Son can tell, even from here."],
  "rome.forum.jupiter.look": ["narrator", "A temple with a gold roof, up on the hill, where it can be seen from everywhere in Rome."],
  "rome.forum.jupiter.look2": ["narrator", "The gold roof flashes in the sun. Whoever polishes it has the best job in Rome."],
  "rome.forum.moneta.look": ["narrator", "Another temple, on the hill's other peak. Rome sets out temples like candles on a cake."],
  "rome.forum.moneta.look2": ["narrator", "Two peaks, two temples. The Son would have put a snack bar on the second one."],
  "rome.forum.records.look": ["narrator", "A long row of arches built into the side of the hill, like an enormous filing cabinet."],
  "rome.forum.paullus.look": ["narrator", "A hall of columns with shops underneath. Rome, the Son is pleased to see, has a mall."],
  "rome.forum.paullus.look2": ["narrator", "Everyone in there is buying, selling or arguing about it. It is certainly a mall."],
  "rome.forum.site.look": ["narrator", "A wooden fence round a very large hole. Something stood here, and something else is going to."],      // PASS-17R: shorter (the picture shows the new stone)
  "rome.forum.site.look2": ["narrator", "Old stones are coming out and new ones going in. Rome is getting a new tooth."],
  "rome.forum.site.use": ["narrator", "The fence says keep out. Not in words; it is simply that kind of fence."],
  "rome.forum.crane.look": ["narrator", "A crane worked by a wheel that men walk inside, like a hamster's wheel, for a very strong hamster."],
  "rome.forum.crane.use": ["narrator", "The Son leaves the crane alone. It is a toy for grown-ups, the kind with no off switch."],
  "rome.forum.pigeons.look": ["narrator", "City pigeons, the same gang as the ones on the temple steps. They commute."],
  "rome.forum.pigeons.use": ["narrator", "The Son does not chase them. Nobody should chase commuters."],

  // ---------- the Gaul (NEW 2, Nobody Will Show Him; gaulTree) ----------
  // Gaius Iulius Litumarus, of Nemausus in the Province, made a senator by the dictator: careful, correct, a little
  // old-fashioned, every word chosen, like a man walking on ice; dry, never bitter for long. He tells Rome's joke about
  // himself before anybody else can, and nobody mocks him: the joke is Rome's. He is going to an ordinary meeting.
  "rome.gaul.look": ["narrator", "A giant of a man in a toga that stops at his knees, like Dad trying to fit into the Son's sleeping bag."],
  "rome.gaul.look2": ["narrator", "Every time the big man asks somebody a question, they walk faster. The Son thinks that is rude of Rome."],
  // four ways in
  "rome.gaul.opt.hi": ["son", "You look lost. I'm lost too, so do you want to be lost together?"],
  "rome.gaul.hi": ["gaul", "You stopped. In all this crowded square, you are the first who has."],
  "rome.gaul.opt.short": ["son", "Excuse me, sir? Your bedsheet's too short, and your knees are out."],
  "rome.gaul.short.1": ["gaul", "It is a toga, and my first. I was warned that togas were difficult."],
  "rome.gaul.short.2": ["gaul", "I was not warned that they were difficult in quite this particular way."],
  "rome.gaul.short.2.b": ["son", "You're doing great. From the knees up."],      // PASS-19R2: new (breaks a run of three; the Son swerves)
  "rome.gaul.opt.viking": ["son", "Whoa. Are you a Viking?"],
  "rome.gaul.viking": ["gaul", "I do not know that word. I am a Gaul, which in Rome is usually word enough."],
  "rome.gaul.opt.way": ["son", "Excuse me, sir. Which way is anywhere?"],
  "rome.gaul.way": ["gaul", "Child, of all the men in Rome, you have found the one who cannot tell you."],
  // who he is, the notice put up in the city (Suetonius's placard), and his question
  "rome.gaul.who.1": ["gaul", "I am Gaius Iulius Litumarus, of Nemausus in the Province. Lately, and to my own surprise, a senator of Rome."],
  "rome.gaul.who.son": ["son", "A senator? Then you're Big Senator, because I already know a regular-sized one."],
  "rome.gaul.who.2": ["gaul", "This is my first meeting. I asked twelve Romans the way. Twelve smiled, and walked faster."],
  "rome.gaul.who.3": ["gaul", "A notice has gone up: nobody is to show the new senator the way to the Senate. It is a joke, and I am it."],
  "rome.gaul.who.4": ["son", "A prank on the new kid, on his very first day? That's the worst kind of prank there is."],
  "rome.gaul.who.6": ["gaul", "So I ask you, child, as I asked them: where does the Senate meet today?"],
  "rome.gaul.again": ["gaul", "The boy who stops. Tell me, have you learned where the Senate meets today?"],
  // the wrong answers, as the Son's choices
  "rome.gaul.opt.house": ["son", "In the senate house, obviously."],
  "rome.gaul.house.1": ["gaul", "There is the senate house. At present it is a hole with men in it."],
  "rome.gaul.house.son": ["son", "So it's more of a senate hole."],
  "rome.gaul.house.2": ["gaul", "It is still a hole. I went and looked again. Holes are faithful in that way."],
  "rome.gaul.opt.capitol": ["son", "Up on the Capitol? The hill with the gold roof?"],
  "rome.gaul.capitol.1": ["gaul", "I have been up. There are geese."],
  "rome.gaul.capitol.2": ["gaul", "They did not show me the way either. They showed me the way down."],
  "rome.gaul.capitol.3": ["gaul", "The geese, child. I said the geese."],
  "rome.gaul.opt.geese": ["son", "Up on the Capitol? Past the attack chickens?"],
  "rome.gaul.geese.1": ["gaul", "So you have met them. Then you know why I came down again, and so quickly."],
  "rome.gaul.geese.2": ["gaul", "We do not speak of the geese, child. We have both been up there."],
  "rome.gaul.opt.caesar": ["son", "At Caesar's house? He's the boss of everything, right?"],
  "rome.gaul.caesar.1": ["gaul", "I have been there. Nine hundred senators at the door, and one porter."],
  "rome.gaul.caesar.son": ["son", "That's a long line."],
  "rome.gaul.caesar.2": ["gaul", "Still nine hundred. Still one porter."],
  "rome.gaul.opt.dunno": ["son", "I don't know, honestly. I'm new here."],
  "rome.gaul.dunno.1": ["gaul", "Then you are a true Roman, child. But you said it to my face, and I thank you."],
  "rome.gaul.dunno.2": ["gaul", "Still a true Roman. You are, at least, consistent."],
  "rome.gaul.dunno.3": ["gaul", "You are the most Roman person I have met today."],
  // the right one, once he has heard it (the senator's speech, or Walnut)
  "rome.gaul.opt.pompey": ["son", "In Pompey's hall, by his theater."],
  "rome.gaul.pompey": ["gaul", "Pompey's theater? The great stone one, with a temple perched on top of its seats?"],
  "rome.gaul.saw.son": ["son", "Yes! I saw it from the top of the hill."],
  "rome.gaul.saw": ["gaul", "From a boy who has seen it with his own eyes. That is more than the whole Senate gave me."],
  "rome.gaul.heard.son": ["son", "My senator told me. He's giving a speech there today, about drains."],
  "rome.gaul.heard": ["gaul", "A man does not invent a speech about drains. I believe you."],
  "rome.gaul.answered.1": ["gaul", "Pompey's hall. Of course it is. Even the Senate of Rome cannot meet in a hole."],
  "rome.gaul.answered.1.b": ["son", "So... I helped?"],      // PASS-19R2: new (breaks a run of three; sets up his thanks)
  "rome.gaul.answered.2": ["gaul", "The joke is spoiled, child, and I thank you for spoiling it."],
  "rome.gaul.welcome": ["gaul", "My guide returns. Pompey's hall, by the theater: I have not forgotten it."],
  // answered, and waiting: he will not cross Rome with his knees out
  "rome.gaul.opt.why": ["son", "So why are you still standing here? You know the way now."],
  "rome.gaul.why.1": ["gaul", "A new man must not arrive first. It looks keen. I will go when the others go, and not before."],
  "rome.gaul.why.2": ["gaul", "And I would rather not cross Rome with my knees out. Rome has seen enough of the knees of Gauls."],
  "rome.gaul.why.3": ["gaul", "My knees, child. We have spoken of my knees."],
  "rome.gaul.opt.remind": ["son", "Pompey's hall, by the theater. Just checking."],
  "rome.gaul.remind.1": ["gaul", "I say it to myself as I walk the fence. It is the Latin I am surest of."],
  "rome.gaul.remind.2": ["gaul", "You may stop checking, child. I will not stop saying it."],
  // the laugh: the city's song about Gauls, told by the Gaul himself, in his own words (the verses are never quoted)
  "rome.gaul.opt.song": ["son", "Why would anybody put up a notice like that?"],
  "rome.gaul.song.1": ["gaul", "It is very funny, if you are a Roman. There is a song about us, too."],
  "rome.gaul.song.2": ["gaul", "Trousers off, broad stripe on: that is the whole of it. Nine times I have heard it. It does not improve."],
  "rome.gaul.song.son": ["son", "You don't make up songs about the new kid. That's the first rule of anything."],
  "rome.gaul.song.3": ["gaul", "Rome is very old, child. It has had time to forget the first rule."],
  "rome.gaul.song.4": ["gaul", "Ten times now. I caught myself humming it this morning, so tell no one."],
  "rome.gaul.opt.mustache": ["son", "Can I just say? Ten out of ten on the mustache."],
  "rome.gaul.mustache.1": ["gaul", "In Gaul, every man of rank wears one. In Rome, the men shave their faces bare, and stare at mine."],
  "rome.gaul.mustache.son": ["son", "My dad tried a mustache once. Mom made it leave."],
  "rome.gaul.mustache.2": ["gaul", "Your mother and the Senate would understand each other."],
  // the togas: once he has the Gaul's toga AND has answered, in either order
  "rome.gaul.opt.swap": ["son", "Big Senator, that toga's my senator's, and I've got yours. Want to swap?"],
  "rome.gaul.swap.first": ["gaul", "First the Senate, child, and then my knees. Where does the Senate meet?"],
  "rome.gaul.swap.first.2": ["gaul", "My knees can wait, but the Senate will not wait for me. Where does it meet?"],
  "rome.gaul.swap.1": ["gaul", "So it fits. I had decided that Roman togas were made to be ridiculous."],
  "rome.gaul.swap.2": ["gaul", "There. Now I look like a senator, and all that is left is to be one."],
  "rome.gaul.swap.son": ["son", "Swapped. One senator-sized bedsheet, going back to my senator."],
  // his going
  "rome.gaul.leave.1": ["gaul", "If anyone asks, a Roman showed me the way."],
  "rome.gaul.leave.son": ["son", "I'm not a Roman."],
  "rome.gaul.leave.2": ["gaul", "Then nobody will be blamed."],
  // the ways out
  "rome.gaul.opt.bye": ["son", "I'll find out where they meet. Don't move, or only move a little."],
  "rome.gaul.bye.1": ["gaul", "I will move a little. Along the fence, and back."],
  "rome.gaul.bye.2": ["gaul", "Along the fence, and back. I am becoming very good at it."],
  "rome.gaul.opt.byewait": ["son", "I'll see what I can do about your knees. Don't go first!"],
  "rome.gaul.byewait.1": ["gaul", "I would not dream of it. Rome would put up a notice."],
  "rome.gaul.byewait.2": ["gaul", "I am not going first. I am barely going at all."],
  // things carried, shown to him (the Gaul's toga starts his talk)
  "rome.gaul.toga": ["gaul", "Another toga. This one they gave me, and I do not recommend it."],
  "rome.gaul.coin": ["gaul", "The dictator gave me his names. I did not expect to be given his face as well."],
  "rome.gaul.quarter": ["gaul", "A man with his hair tied back. In Nemausus we would call that short."],
  "rome.gaul.phone": ["gaul", "A small dark mirror. It shows a large man in a short toga, as I knew it would."],
  "rome.gaul.gum": ["gaul", "I am trying very hard to look like a senator. Chewing would not help."],
  "rome.gaul.breakfast": ["gaul", "A senator does not eat in the street, I am told. I am told a great deal."],
  "rome.gaul.incense": ["gaul", "For which god? I am still learning the names of the people."],
  "rome.gaul.lamp": ["gaul", "You carry it like an egg. Somebody loves whoever that lamp is for."],

  // ---------- Phyllis (NEW 4, Interest Is Extra Wishes, her side; phyllisTree) ----------
  // Fannia Phyllis, a Greek freedwoman, a widow, on her low stool among her baskets at the foot of Castor's temple. Fast
  // and warm, a seller's patter, sharp with fools, soft about her son. Anna Perenna's feast is today.
  "rome.phyllis.look": ["narrator", "A small woman in a nest of flowers, twisting them into garlands faster than the Son can tie his shoes."],      // PASS-17R: not every look is a ten
  "rome.phyllis.look2": ["narrator", "There is a bundle in the garland seller's lap, wrapped up like an egg. That one is plainly not for sale."],
  "rome.phyllis.look3": ["narrator", "The bundle is gone from her lap. She has a half-made garland there now, and her hands are going twice as fast."],
  "rome.phyllis.cry": ["phyllis", "Myrtle for your sweetheart, violets fresh this morning, garlands for Anna Perenna!"],
  "rome.phyllis.again": ["phyllis", "Back again? Violets do not keep, child, and neither does my patience with customers who only look."],
  "rome.phyllis.opt.anna": ["son", "Who's Anna Perenna? Do I need to get her a garland?"],
  "rome.phyllis.anna.1": ["phyllis", "Child, where were you raised? It is Anna Perenna's feast. Half the city picnics by the river today."],
  "rome.phyllis.anna.2": ["phyllis", "And every one of them wants a garland. I cannot leave my baskets for a moment."],
  "rome.phyllis.anna.3": ["phyllis", "It is still the busiest morning of the year. Buy, or stand aside for those who will."],
  "rome.phyllis.opt.sweetheart": ["son", "Myrtle for my sweetheart? I don't even have a dog."],
  "rome.phyllis.sweetheart.1": ["phyllis", "No dog and no sweetheart. Then violets for your mother. Every boy has one of those."],
  "rome.phyllis.sweetheart.son": ["son", "Mom would love violets. She's a really long way away, though."],
  "rome.phyllis.sweetheart.2": ["phyllis", "Then smell them for her, and tell her so. She will never know that you did not buy any."],
  "rome.phyllis.opt.son": ["son", "Do you have kids? I'm somebody's kid, just not anybody's from around here."],
  "rome.phyllis.son.1": ["phyllis", "One, and only one. Felix. He loads the barges across the river, below the stone bridge."],
  "rome.phyllis.son.2": ["phyllis", "His name is down for Corinth. The dictator is building it anew, for freedmen like me."],
  "rome.phyllis.son.2.b": ["son", "A whole city?"],      // PASS-19R2: new (breaks a run of three)
  "rome.phyllis.son.3": ["phyllis", "A city that has lain empty a hundred years. Imagine it, not a grandmother in the place."],
  "rome.phyllis.son.son": ["son", "Corinth rings a bell, a big one. It'll come to me."],
  "rome.phyllis.son.4": ["phyllis", "Felix and Corinth, Corinth and Felix. You are as bad as I am, child. I talk of nothing else."],
  "rome.phyllis.opt.twins": ["son", "Whose temple is that? The big one you're sitting under?"],
  "rome.phyllis.twins.1": ["phyllis", "Castor's, and his brother's: the Twins. Everybody in Rome knows that."],
  "rome.phyllis.twins.2": ["phyllis", "The city's true weights are kept inside. Nobody in this Forum can cheat you. Not even I."],
  "rome.phyllis.twins.son": ["son", "A temple that checks your groceries."],
  // the wish (the lever): the boy has the coin, and Walnut has said whose it was
  "rome.phyllis.opt.wish": ["son", "Walnut says the fountain wish was yours. I borrowed it, so I'm asking now."],
  "rome.phyllis.wish.1": ["phyllis", "My wish. Yes, it was mine. I threw it in at first light, for my boy."],
  "rome.phyllis.wish.2": ["phyllis", "The first new silver I had held in years, with the dictator's own head on it."],
  "rome.phyllis.wish.2.b": ["son", "What did you wish?"],      // PASS-19R2: new (want; breaks a run of four)
  "rome.phyllis.wish.3": ["phyllis", "I wished to give Felix this little lamp before he sails, so that he has a light in Corinth."],
  "rome.phyllis.wish.4": ["phyllis", "And to hear him say goodbye. But he cannot leave his barge, and I cannot leave my baskets."],
  "rome.phyllis.wish.again": ["phyllis", "The lamp is still in my lap, child, and Felix still across the river."],
  "rome.phyllis.opt.giveback": ["son", "Then you should have it back. Here, it's yours."],
  "rome.phyllis.giveback": ["phyllis", "A wish once thrown is not mine to take back, child. But it was for my boy. Remember that."],
  "rome.phyllis.giveback.2": ["phyllis", "Thrown is thrown, child. Put it away."],
  "rome.phyllis.opt.quarter": ["son", "Or I could pay you with a quarter. It's got a bird on it."],
  "rome.phyllis.quarter": ["phyllis", "A bird? For a wish? Child."],
  "rome.phyllis.quarter.2": ["phyllis", "Still a bird. Still a wish. Still no."],
  "rome.phyllis.opt.take": ["son", "I could take the lamp to him. I'm great at errands."],
  "rome.phyllis.take.1": ["phyllis", "Would you really? Then go down the Tuscan street, child, and over the stone bridge."],
  "rome.phyllis.take.2": ["phyllis", "Tell him his mother says to come to her before he sails. He will know the rest."],
  "rome.phyllis.lamped": ["son", "Lamp delivery. I'll carry it like an egg."],
  "rome.phyllis.opt.think": ["son", "Can I think about it? I think fast, mostly while walking."],
  "rome.phyllis.think": ["phyllis", "Think, then, and walk while you do it. Corinth will not wait for you to finish."],
  // the lamp on its way
  "rome.phyllis.waiting": ["phyllis", "Did you find him? He has my face, and his father's hurry."],
  "rome.phyllis.opt.where": ["son", "Where's Felix again? Just checking."],
  "rome.phyllis.where.1": ["phyllis", "Across the river, child, at the barges below the stone bridge."],
  "rome.phyllis.where.2": ["phyllis", "The Tuscan street, then the bridge, then the barges. Look for the big sunburnt one. That is mine."],
  "rome.phyllis.opt.lampback": ["son", "Do you want the lamp back? You could keep it till he comes."],
  "rome.phyllis.lampback": ["phyllis", "Then it would be my lamp, and my wish still wishing. Take it to him."],
  "rome.phyllis.opt.byewait": ["son", "Lamp delivery, back on."],
  "rome.phyllis.byewait": ["phyllis", "Mind it on the bridge."],
  // Felix's word, brought back: her leave (decision 7)
  "rome.phyllis.word": ["phyllis", "You found him? Then do not keep an old woman waiting, child, out with it."],
  "rome.phyllis.opt.news": ["son", "He'll come at the ninth hour. And he'll light it in Corinth."],
  "rome.phyllis.news.1": ["phyllis", "The ninth hour."],
  "rome.phyllis.news.2": ["phyllis", "Then the wish is answered, and it was a good one."],
  "rome.phyllis.news.2.b": ["son", "Can I keep borrowing the coin?"],      // PASS-19R2: new (want: he needs her leave for the toss; breaks a run of three)
  "rome.phyllis.news.3": ["phyllis", "Keep the coin, child. It has done its work, and it was borrowed honestly."],
  "rome.phyllis.opt.guess": ["son", "Guess!"],
  "rome.phyllis.guess": ["phyllis", "Child."],
  "rome.phyllis.granted.son": ["son", "Borrowed, and paid back with interest. I told Walnut interest is extra wishes."],
  "rome.phyllis.done": ["phyllis", "I sell twice as fast now, child. An answered wish is good for trade."],
  // the ways out
  "rome.phyllis.opt.bye": ["son", "I'll go stand over there and smell things for free."],
  "rome.phyllis.bye.1": ["phyllis", "Go on. The bees do the same, and I have never sold to a bee."],
  "rome.phyllis.bye.2": ["phyllis", "Mind my violets as you go."],
  // things carried, shown to her (the coin, the quarter and the lamp start her talk)
  "rome.phyllis.gaultoga": ["phyllis", "That is not a garland, child. That is a sail."],
  "rome.phyllis.toga": ["phyllis", "Keep that off my violets. Senators flatten enough of them."],
  "rome.phyllis.breakfast": ["phyllis", "Sausage, by my violets? Take it away, or they will smell of it all day."],

  // ================= ROME-13W: rome-capitol: the Capitol, the precinct of Jupiter Best and Greatest =================
  // The top of the hill: the great temple, the kings' statues, the sacred geese of Juno, and over the wall the whole
  // city. Reached from the steps' right edge once he knows it is B.C.

  // ---------- arrival (the first time: rome.sawCapitol) ----------
  "rome.capitol.arrive.1": ["son", "I'm up on the hill with the gold roof. Would climb, and did."],
  "rome.capitol.arrive.3": ["son", "And there's a kid on a statue, completely surrounded by geese. That's a whole situation."],

  // ---------- the things in it ----------
  // (The look at the theater is the boy seeing Pompey's theater without knowing its name: it sets rome.sawTheater, and
  // the Gaul names it later, when the boy can say "I saw it from the top of the hill!")
  "rome.capitol.temple.look": ["narrator", "Giant columns and a gold roof. Rome is showing off, and it is working."],
  "rome.capitol.temple.use": ["narrator", "The Son does not go in. Nobody walks into somebody's room without knocking, not even a god's."],
  "rome.capitol.name.look": ["narrator", "Big letters across the front: Q LVTATIVS CATVLVS. Rome is still out of U's."],
  "rome.capitol.roof.look": ["narrator", "A roof covered in gold. Somebody did that to a building on purpose."],
  "rome.capitol.doors.look": ["narrator", "Through the open doors, something huge and gold sits far at the back. The Son lets it sit."],
  "rome.capitol.altar.look": ["narrator", "A stone altar the size of a minivan. Dad would poke it."],
  "rome.capitol.altar.use": ["narrator", "The Son does not touch it. That is Dad's barbecue rule, the one Dad breaks."],
  "rome.capitol.altar.incense": ["narrator", "The incense is for Saturn, down the hill. This is the wrong god and the wrong altar."],
  "rome.capitol.chariot.look": ["narrator", "A bronze chariot with nobody driving it, like valet parking for gods."],
  "rome.capitol.chariot.use": ["narrator", "The chariot has no seats. It is standing room only, and the Son stays on the ground."],
  "rome.capitol.world.look": ["narrator", "A bronze man standing on a great bronze ball. Big Sister would have a footnote for it."],
  "rome.capitol.kings.look": ["narrator", "A row of old statues, the kings of Rome, and among them a man with his sword drawn. He looks busy."],
  "rome.capitol.kings.look2": ["narrator", "The kings look as if they own the hill and would like visitors off it."],
  "rome.capitol.brutus.look": ["narrator", "Words are scratched on the base of the man with the sword. In Rome, whatever stands still gets written on."],
  "rome.capitol.dictator.look": ["narrator", "The newest statue in the row is the man from the Son's coin. He is everywhere today."],
  "rome.capitol.tablets.look": ["narrator", "Bronze pages fixed to stone posts. Rome loves terms and conditions."],
  "rome.capitol.tablets.use": ["narrator", "They are in Latin, and tiny. To the Son, that is double homework."],
  "rome.capitol.pen.look": ["narrator", "A goose pen with no geese in it. They are all out on the job."],
  "rome.capitol.pen.use": ["narrator", "The gate is already open. The geese simply do not care to go in."],
  "rome.capitol.hut.look": ["narrator", "A round hut with a grass roof, right beside the biggest temple in Rome. Somebody's grandpa would not sell."],
  "rome.capitol.hut.use": ["narrator", "The Son knocks. Nobody has been home for a very long time."],
  "rome.capitol.view.look": ["narrator", "The river, an island with a temple on it, and the whole city: roofs all the way down."],
  "rome.capitol.theater.look": ["narrator", "Far off, a stone half-circle of seats with a temple on top. They are the biggest bleachers the Son has ever seen."],
  "rome.capitol.theater.look2": ["narrator", "The stone theater with the temple on top. A person would need a snack halfway up those seats."],
  "rome.capitol.janiculum.look": ["narrator", "A long hill across the river, green with trees that bring their own shade."],
  "rome.capitol.moneta.look": ["narrator", "The hill's two peaks, with a temple on each, like a camel that is very fond of temples."],

  // ---------- the geese (NEW 3, Juno's Geese: every wrong try, and the stomp) ----------
  // While they guard the statue's base, each wrong try gets a hiss. Once the goose-keeper has told his tale
  // (rome.knowsGeese) a click on them is the stomp. After it (rome.geeseGone) they are in their pen: .penned.
  "rome.geese.look": ["narrator", "Geese all round the foot of the statue. The boy on top is surrounded by attack chickens."],
  "rome.geese.look2": ["narrator", "Whenever the boy on the statue moves a foot, every neck comes out. It is an alarm that hisses."],
  "rome.geese.call": ["narrator", "The Son calls the geese, sweetly. They hiss back at him, in stereo."],
  "rome.geese.shoo": ["narrator", "The Son yells shoo. Nobody shoos; whatever frightens a goose, it is not a boy shouting at it."],
  "rome.geese.gum": ["narrator", "No gum for sacred geese. They would never get it off their beaks, and the Son would never hear the end of it."],
  "rome.geese.quarter": ["narrator", "The geese do not want a bird on a coin; they are birds. It would take something much stranger than that."],
  "rome.geese.coin": ["narrator", "Bribing geese would be a new low, even for the Son. The geese hiss at the idea."],
  "rome.geese.phone": ["narrator", "The geese hiss at the phone, which is more than the phone has done all day."],
  "rome.geese.toga": ["narrator", "A toga thrown over sacred geese would honk forever. The Son keeps it folded."],
  "rome.geese.gaultoga": ["narrator", "The Gaul's toga is big enough, but the Son would lose the geese, the toga and himself under it."],
  "rome.geese.lamp": ["narrator", "Not Felix's lamp. Phyllis would know somehow; mothers always do."],
  "rome.geese.tunic": ["narrator", "Waving the tunic at them would end with the Son returning a tunic and an apology."],
  // the stomp (the anser tree's `stomp` hook, or a click on the geese after the tale), in this order: the boy's line; his
  // sneakers flash; the geese run for their pen; Titus hops down; the breakfast; Titus runs home; the goose-keeper
  "rome.geese.stomp": ["son", "Anything strange? I'm the strangest thing in Rome. Watch my feet."],
  "rome.titus.down": ["titus", "I was not scared. I was sitting."],
  "rome.titus.give": ["titus", "Take it to old Arruns for me, I am going home before Father sends the geese after me."],
  "rome.titus.give.son": ["son", "One kid, one breakfast, zero geese."],
  "rome.titus.run": ["titus", "Your shoes are the best thing on this hill, and I have seen the gold roof!"],
  "rome.anser.last": ["anser", "That is the most noise they have made since the Gauls."],
  // afterwards: the geese (or their pen) looked at, and tried
  "rome.geese.penned": ["narrator", "Every goose is back in the pen, eating. They are professionals."],
  "rome.geese.penned.use": ["narrator", "The Son does not go near them. He and the geese had a moment, and it is over."],

  // ---------- Titus, the keeper's boy (titusTree) ----------
  // About eleven, on top of a statue base among the kings, the soothsayer's breakfast in a knotted cloth in his lap.
  // He talks like his father, without stopping for breath, and like a boy: boasting, then honest.
  "rome.titus.look": ["narrator", "A boy sitting on top of a statue's base, pretending he meant to be up there all along."],
  "rome.titus.look2": ["narrator", "The boy is pretending to be a statue. A goose looks at him, and he stops."],
  // ways in (the first, once his father has told the boy about him)
  "rome.titus.opt.sent": ["son", "Are you Titus? Your dad sent me, and he says the old one will be fainting."],
  "rome.titus.sent": ["titus", "Father sent you? Then he is in a state, he makes extra sausages when he is in a state."],
  "rome.titus.opt.stuck": ["son", "Are you stuck up there?"],
  "rome.titus.stuck.1": ["titus", "Stuck? Me? I am sitting, I like sitting, you can see the whole city from up here."],
  "rome.titus.stuck.2": ["titus", "I have been sitting since first light. On purpose. Mostly on purpose."],
  "rome.titus.stuck.2.b": ["son", "Mostly?"],      // PASS-19R2: new (breaks a run of five; the Son swerves)
  "rome.titus.opt.statue": ["son", "Whoa. A statue that blinks."],
  "rome.titus.statue": ["titus", "Statues do not have breakfasts, and I have one. It is not mine, but I have got it."],
  "rome.titus.opt.sausage": ["son", "Is that sausage? I can smell sausage from here."],
  "rome.titus.sausage": ["titus", "Do not look at it like that, it is not mine, it is the soothsayer's, and he is very old."],
  "rome.titus.opt.jump": ["son", "Just jump down. It's not that high."],
  "rome.titus.jump.1": ["titus", "Over them? They bite like Father does when you owe him money."],
  // whose boy he is, and whose breakfast (rome.knowsBoy)
  "rome.titus.who.1": ["titus", "I am Titus, Father keeps the cookshop by the fountain, everybody owes him, and he tells them so."],
  "rome.titus.who.1.b": ["son", "The snack bar! I've smelled it."],      // PASS-19R2: new (breaks a run of four)
  "rome.titus.who.2": ["titus", "This is old Arruns the soothsayer's breakfast, I was taking it to him, and then the ewe went by."],
  "rome.titus.who.3": ["titus", "Every Ides I go up after her, so I went, and then the geese came, and now I am sitting."],
  "rome.titus.again": ["titus", "Still sitting, still fine, did you bring anything that works on geese?"],
  "rome.titus.opt.geese": ["son", "What's the deal with the geese?"],
  "rome.titus.geese.1": ["titus", "They do not like feet. Watch."],
  "rome.titus.geese.2": ["titus", "See? Foot down, every neck out. I am not scared. I am only keeping my feet."],
  "rome.titus.geese.again": ["titus", "They still do not like feet, I checked again, do not make me check again."],
  "rome.titus.opt.ewe": ["son", "What ewe? You keep saying ewe."],
  "rome.titus.ewe.1": ["titus", "The Ides sheep, she goes up to Jupiter every single Ides, and I always go up after her."],
  "rome.titus.ewe.2": ["titus", "She had ribbons. She went up the hill like a senator."],
  "rome.titus.opt.father": ["son", "Does your dad know you're up here?"],
  "rome.titus.father.1": ["titus", "Father knows everything, and Father is going to talk at me for a week."],
  "rome.titus.father.2": ["titus", "Is he worried? He worries loud."],
  "rome.titus.father.3": ["titus", "Tell him I am fine. Do not tell him about the geese. Well, tell him a little about the geese."],
  "rome.titus.opt.jump2": ["son", "Seriously, jump. I'll catch you, probably."],
  "rome.titus.jump.2": ["titus", "You would catch me, they would catch you, and we would both be down there with them."],
  "rome.titus.jump.3": ["titus", "No."],
  "rome.titus.opt.help": ["son", "Want me to get you down?"],
  "rome.titus.help.1": ["titus", "I do not need getting down, I am fine, I am sitting, I like it up here."],
  "rome.titus.help.2": ["titus", "You could ask old Anser, though, he feeds them, he talks about them all day long."],
  "rome.titus.help.3": ["titus", "Old Anser, the one with the basket. Ask him about geese, and you will be there till sundown."],
  "rome.titus.opt.bye": ["son", "Stay right there. Sorry, you know what I mean."],
  "rome.titus.bye.1": ["titus", "I am not going anywhere. That is the whole trouble."],
  "rome.titus.bye.2": ["titus", "Still here."],
  // things carried, shown to him on his base
  "rome.titus.toga": ["titus", "Throw me a toga? I am not cold, I am stuck. No, I am not stuck, I am sitting."],
  "rome.titus.coin": ["titus", "New silver! Father would bite it, Father bites everything."],
  "rome.titus.quarter": ["titus", "A bird on a coin, that is lucky, unless it is a goose. Hide it, quick."],
  "rome.titus.gum": ["titus", "No, do not, a goose will catch it, and then it will have gum and opinions."],

  // ---------- the goose-keeper (anserTree: NEW 3's clue) ----------
  // Titus Rubrius Anser, about sixty, who feeds Juno's geese for the Republic. Mournful, devoted, full of the story of
  // the Gauls, which he tells to anyone, long ago and with no year: it is the instructions.
  "rome.anser.look": ["narrator", "A sad old man with a basket of grain and a long stick. He has plainly never once poked a goose with it."],
  "rome.anser.look2": ["narrator", "The goose-keeper counts his geese and gets a different number every time. Geese move."],
  // ways in (every one of his answers comes round to the night the geese saved the city)
  "rome.anser.opt.move": ["son", "Are those your geese? Can you move them, for the kid up there?"],
  "rome.anser.move.1": ["anser", "They are sacred birds, child. I feed them. I do not argue with them."],
  "rome.anser.move.2": ["anser", "Nobody argues with the geese that saved this city. Least of all the man who feeds them."],
  "rome.anser.opt.chickens": ["son", "Excuse me, sir. Are those attack chickens?"],
  "rome.anser.chickens.1": ["anser", "These are the sacred geese of Juno, child. They saved this city once, long ago."],
  "rome.anser.chickens.2": ["anser", "Attack chickens. I will not tell them you said that."],
  "rome.anser.opt.name": ["son", "What's your name? I'm collecting names, and so far I've got Walnut."],
  "rome.anser.name.1": ["anser", "Titus Rubrius Anser. Anser means goose."],
  "rome.anser.name.2": ["anser", "It was my grandfather's name long before it was my work. Nobody ever believes me."],
  "rome.anser.name.son": ["son", "A goose guy called Goose! Mister Goose goes right at the top of my collection."],      // PASS-17R: his collection of names comes round again
  "rome.anser.name.3": ["anser", "Mister Goose. I will bear it, child, for these geese saved the city."],
  "rome.anser.opt.feed": ["son", "Do you feed them every day? That's a lot of geese."],
  "rome.anser.feed.1": ["anser", "Every morning, on the Republic's grain. The Republic has fed them ever since they saved the city."],
  "rome.anser.feed.2": ["anser", "The Republic does not pay for their manners."],
  "rome.anser.again": ["anser", "The boy who collects names. The geese remember you, as they remember everybody."],
  // the tale (rome.knowsGeese): the Gauls who climbed the Capitol by night, and the geese that woke Manlius
  "rome.anser.opt.saved": ["son", "Wait, geese saved the city? How do geese save a city?"],
  "rome.anser.tale.1": ["anser", "Long ago, the Gauls took this city. All of it, every street, but this one hill."],
  "rome.anser.tale.2": ["anser", "One night they climbed the rock below that wall, so quietly that not even the dogs woke."],
  "rome.anser.tale.2.b": ["son", "Not even the dogs?"],      // PASS-19R2: new (breaks a run of six)
  "rome.anser.tale.3": ["anser", "But Juno's geese woke. They cried out, all of them at once, and they woke Manlius."],
  "rome.anser.tale.4": ["anser", "Manlius ran to the edge, and the Gauls went down faster than they came up."],
  "rome.anser.tale.4.b": ["son", "Attack chickens. I knew it."],      // PASS-19R2: new (breaks a run of six; the Son's name for them pays off)
  "rome.anser.tale.6": ["anser", "To this day, they cannot abide anything strange. They shout at it, and then they run."],
  "rome.anser.tale.son": ["son", "Anything strange. Hang on, I've got my thinking face on."],
  "rome.anser.tale.again.1": ["anser", "Gladly. Long ago, the Gauls took this city, all of it but this hill..."],
  "rome.anser.tale.again.son": ["son", "Geese, Gauls, Manlius, the edge of the hill. I remember."],
  "rome.anser.tale.again.2": ["anser", "You were listening. Thirty years I have told it, and nobody listens."],
  "rome.anser.tale.more": ["anser", "Long ago..."],
  "rome.anser.tale.more.son": ["son", "I'm going to stop asking you that. For both of us."],
  // the lever: the boy puts the tale to the test (the stomp, above)
  "rome.anser.opt.test": ["son", "Mister Goose? You might want to hold on to your basket."],
  "rome.anser.opt.move2": ["son", "Can you move them, though? Just a little, for the kid?"],
  "rome.anser.move.3": ["anser", "Thirty years I have fed them. I have never once won an argument."],
  "rome.anser.move.4": ["anser", "No, child."],
  "rome.anser.move.5": ["anser", "They are not my geese, child, they are Juno's, and she has not asked me."],
  "rome.anser.opt.dogs": ["son", "Who guards the hill at night? The geese?"],
  "rome.anser.dogs.1": ["anser", "Dogs, at night. The Republic keeps dogs against thieves, for all the good they do."],
  "rome.anser.dogs.2": ["anser", "Between you and me, the dogs sleep. The geese never do."],
  "rome.anser.dogs.3": ["anser", "The dogs are asleep, I expect, it being daytime. It is always the geese."],
  "rome.anser.opt.moneta": ["son", "What's that other temple? On the hill's other bump?"],
  "rome.anser.moneta.1": ["anser", "Juno's too: Juno Moneta, the Warner. They strike the city's money there."],
  "rome.anser.moneta.son": ["son", "Moneta, money-ta. I just figured out the word money!"],
  "rome.anser.moneta.2": ["anser", "I do not know what you have worked out, child, but you look very pleased with it."],
  "rome.anser.moneta.3": ["anser", "Moneta: the money, and the warning. Juno keeps an eye on both."],
  "rome.anser.opt.bye": ["son", "Say bye to the geese for me, Mister Goose. From a distance."],
  "rome.anser.bye.1": ["anser", "I will tell them. They will not care."],
  "rome.anser.bye.2": ["anser", "They still will not care."],
  // after the stomp
  "rome.anser.after": ["anser", "Back in their pen and eating, as if nothing had happened. That is geese. I am still shaking."],
  "rome.anser.opt.sorry": ["son", "Sorry about the noise, and the running, and the honking."],
  "rome.anser.sorry": ["anser", "Do not be sorry. Thirty years I have told that story, and today somebody used it."],
  "rome.anser.bye.after": ["anser", "Go gently, child. And not near my pen."],
  // things carried, shown to him
  "rome.anser.toga": ["anser", "Not over my geese. They would honk at the dark all day."],
  "rome.anser.coin": ["anser", "New silver, from Moneta's. My geese guard the hill, and Moneta guards the money."],
  "rome.anser.quarter": ["anser", "A bird on a coin, an eagle, I think. Juno would have preferred a goose."],
  "rome.anser.gum": ["anser", "Not for my geese, child. I mean it, I will tell the Republic."],
  "rome.anser.breakfast": ["anser", "The soothsayer's. Take it down before the geese remember it."],

  // ================= ROME-13W: rome-tiber: across the Tiber, below the stone bridge =================
  // The right bank, looking downstream: a lane of small houses where a Jewish family lives beside their house of prayer,
  // a hen yard, a landing and a barge, the river in the morning sun. The quiet place of the act (the faith thread).

  // ---------- arrival (the first time: rome.sawTiber): the old man at his window, praying; the hens in a row ----------
  "rome.tiber.arrive.1": ["son", "Boats, a girl with a lot of hens, and an old man at a window."],
  "rome.tiber.arrive.2": ["son", "He's praying, with his window open. Like Daniel."],
  "rome.tiber.arrive.3": ["son", "I'll wait till he's done. I'm getting good at waiting."],

  // ---------- the things in it ----------
  "rome.tiber.river.look": ["narrator", "The Tiber, brown and in a hurry, like a dog after a bath."],
  "rome.tiber.river.use": ["narrator", "The Son does not swim. He would come out browner than he went in, and in a different town."],      // PASS-17R: the look has "brown and in a hurry" already
  "rome.tiber.river.coin": ["narrator", "Things that go into the river stay in the river. The coin stays in the Son's pocket."],
  "rome.tiber.river.quarter": ["narrator", "The Son does not skip his quarter across the Tiber. George would never forgive him."],
  "rome.tiber.barge.look": ["narrator", "A long flat boat piled with bundles, like a floating table."],
  "rome.tiber.barge.use": ["narrator", "The Son stays off the barge. The boatman would only put him ashore again, politely, probably."],
  "rome.tiber.bales.look": ["narrator", "Rolls of papyrus wrapped in mats: paper, all the way from Egypt. Big Sister would sniff it."],
  "rome.tiber.bales.use": ["narrator", "The Son tries to lift a bale and cannot. That is why the boatman has those arms."],
  "rome.tiber.landing.look": ["narrator", "Stone steps that go right down into the water, like stairs for fish."],
  "rome.tiber.landing.use": ["narrator", "Mom would say no to going down to the water. She is not here, and it is still no."],
  "rome.tiber.farbank.look": ["narrator", "More hills and more temples on the far bank. Rome keeps going, as if it forgot where to stop."],
  "rome.tiber.road.look": ["narrator", "A long road running along the river. Somebody important lives down that way."],
  "rome.tiber.gardens.look": ["narrator", "A long garden wall beside the road. Somebody has a very big backyard."],
  "rome.tiber.house.look": ["narrator", "A plain little house with hens out in front. It is the old man's."],
  "rome.tiber.house.use": ["narrator", "The Son lifts a hand to knock, and lowers it again. Nobody knocks on somebody's praying."],
  "rome.tiber.doorpost.look": ["narrator", "A tiny case fixed to the doorpost, like a doorbell that does not ring."],
  "rome.tiber.doorpost.use": ["narrator", "The Son does not poke it. It is not his door, and the little case looks important in a quiet way."],
  "rome.tiber.window.look": ["narrator", "An upstairs window, open wide toward the river. An old man stands at it."],
  "rome.tiber.window.look2": ["narrator", "The old man's window, still open. He will be back at it at midday; he prays there three times a day."],
  "rome.tiber.prayerhouse.look": ["narrator", "A plain building with nothing painted on it, only a door and a bench. It is like a library, but for praying."],      // PASS-17R: a boy's way of putting it
  "rome.tiber.prayerhouse.use": ["narrator", "It is quiet in there, and the Son is not quiet. He stays outside."],
  "rome.tiber.bench.look": ["narrator", "A stone bench, good for waiting on. The Son is an expert at waiting by now."],
  "rome.tiber.bench.use": ["narrator", "The Son sits down. Sitting is the main part of waiting."],
  "rome.tiber.well.look": ["narrator", "A well. The Son has learned his lesson about coins and water."],
  "rome.tiber.well.coin": ["narrator", "No more wishes in water. The Son is taking a break from those."],
  "rome.tiber.figtree.look": ["narrator", "A fig tree in its first small leaves: a snack tree, still loading. The figs come in summer."],      // PASS-17R: no Bible fact tacked onto a look
  "rome.tiber.figtree.use": ["narrator", "There are no figs to pick yet, only baby leaves."],
  "rome.tiber.washing.look": ["narrator", "Washing on a line. The washerwoman in the street would have opinions about it."],

  // ---------- Mariam's hens (chickens: they stand in a row looking over the river at the city; nobody explains it) ----------
  "rome.hens.look": ["narrator", "Hens, all standing in a row and all facing the same way: over the river, at the city."],
  "rome.hens.look2": ["narrator", "The hens have not moved, not one of them, not even the one on the end, who is a wiggler."],
  "rome.hens.use": ["narrator", "The Son clucks at the hens. Not one head turns; they have somewhere to look."],
  "rome.hens.breakfast": ["narrator", "The breakfast is the soothsayer's, and the Son keeps it. The hens do not even turn round for a sausage."],

  // ---------- Eleazar (the faith thread: the design's 6.2; eleazarTree) ----------
  // About sixty-five, born in Jerusalem, carried to Rome a captive when Pompey took the city, long since freed; the date
  // seller's father-in-law. Slow, warm, grave, with a dry humor; calls the Son "child"; never preaches, never hurries,
  // listens more than he talks. He never names Jesus, never says when, never says the promised one is God, says nothing
  // against anybody's gods, and argues with nobody; the Son never tells him what is coming.
  // At his window: the boy waits (the scene), then the old man comes down to his bench.
  "rome.eleazar.look.window": ["narrator", "An old man at his upstairs window, praying. The Son is not going to bother him."],
  "rome.eleazar.look.window2": ["narrator", "The Son cannot hear any of the words. He decides that is all right, since God can."],      // PASS-17R: what a boy would say
  "rome.eleazar.wait": ["son", "I'm waiting. Look at me doing it."],
  "rome.eleazar.look": ["narrator", "The old man follows his scroll with one finger, the way the Son reads a hard chapter book."],
  "rome.eleazar.look2": ["narrator", "The old man keeps looking up across the river, and then back down at his scroll."],
  // the greeting, and the ways in
  "rome.eleazar.peace": ["eleazar", "Peace to you, child."],
  "rome.eleazar.opt.peace": ["son", "Peace to you too, mister."],
  "rome.eleazar.opt.waited": ["son", "I waited the whole time and didn't fidget once. Okay, I fidgeted once."],
  "rome.eleazar.waited": ["eleazar", "Twice. But very politely."],
  "rome.eleazar.opt.church": ["son", "Is that your church? The one with the bench?"],
  "rome.eleazar.church": ["eleazar", "A house of prayer."],
  "rome.eleazar.opt.yose": ["son", "Do you know the date seller? Beard, basket, very calm?"],
  "rome.eleazar.yose.1": ["eleazar", "That is Yose, my daughter's husband. Tell me, does he say the dates are selling?"],
  "rome.eleazar.yose.son": ["son", "He says Rome always wants dates."],
  "rome.eleazar.yose.2": ["eleazar", "He always says so."],
  "rome.eleazar.who.1": ["eleazar", "I am Eleazar. And who are you, child, who waits so well?"],
  "rome.eleazar.who.son.1": ["son", "My dad's lost. Or I am, one of us is. I'm waiting for him to find me."],
  "rome.eleazar.who.son.2": ["son", "He always comes. He's late sometimes, but he calls that making good time."],
  "rome.eleazar.who.2": ["eleazar", "A father who always comes. That is a good thing to wait for."],
  "rome.eleazar.again": ["eleazar", "You came back. Sit, child, if you like; the bench is long."],
  // the window: Daniel 6:10 and Psalm 55:17, told, not quoted
  "rome.eleazar.opt.window": ["son", "What were you doing at the window? With your eyes shut?"],
  "rome.eleazar.window.1": ["eleazar", "Praying toward Jerusalem, child, where the Temple is. Evening, and morning, and at midday."],
  "rome.eleazar.window.son": ["son", "Like Daniel, with the window open three times a day. No lions, though, right?"],      // PASS-17R: shorter, and a question to answer
  "rome.eleazar.window.2": ["eleazar", "No lions, child. Only Mariam. You have been well taught."],      // PASS-17R: he answers it (Mariam is boss of Grandfather)
  // how he came to Rome: told without bitterness, and a pause
  "rome.eleazar.opt.rome": ["son", "How did you end up in Rome? A wrong turn? My dad takes a lot of those."],
  "rome.eleazar.rome.1": ["eleazar", "When Pompey took Jerusalem, nineteen years ago, many of us were brought here."],
  "rome.eleazar.rome.2": ["eleazar", "I was bought, and I worked, and in time my master set me free."],
  "rome.eleazar.rome.2.b": ["son", "I'm glad he did."],      // PASS-19R2: new (breaks a run of three)
  "rome.eleazar.rome.3": ["eleazar", "Now I live where my people live. And I pray toward home."],
  "rome.eleazar.rome.son": ["son", "That's a long way from home. Me too."],
  "rome.eleazar.rome.4": ["eleazar", "Then we are neighbors in that, child."],
  // what he prays for: Isaiah 9:7 and 60:3, told in his own words; then the Son, to us (Luke 2:25, Simeon, not named to him)
  "rome.eleazar.opt.prayfor": ["son", "What do you pray for? If that's not private."],
  "rome.eleazar.prayfor.1": ["eleazar", "For Jerusalem's peace. And for the king God has promised, a son of David."],
  "rome.eleazar.prayfor.2": ["eleazar", "He will rule in righteousness, without end. The nations will come to his light."],
  "rome.eleazar.prayfor.2.b": ["son", "Everybody?"],      // PASS-19R2: new (breaks a run of four; the next line answers it)
  "rome.eleazar.prayfor.3": ["eleazar", "Greeks, Egyptians, Gauls, Romans. All of them, over there."],
  "rome.eleazar.prayfor.4": ["eleazar", "Even these. Even, perhaps, a boy in strange shoes."],
  "rome.eleazar.simeon": ["son", "There's an old man like him in my Bible. I'm so not saying anything."],
  // the heart, only after that one: Isaiah 40:31, QUOTED, King James Version, the first clause, to its semicolon
  "rome.eleazar.opt.heart": ["son", "What if he doesn't come in time? For you, I mean."],
  "rome.eleazar.heart.1": ["eleazar", "Then my grandchildren will. The promise does not depend on an old man's eyes."],
  "rome.eleazar.heart.2": ["eleazar", "Isaiah says it: 'But they that wait upon the LORD shall renew their strength;'"],          // Isaiah 40:31, King James Version, to its semicolon: exact
  "rome.eleazar.heart.son.1": ["son", "That's on our fridge! On a magnet, with an eagle. Mom reads it when Dad's late."],      // PASS-17R: no reference aloud: where he knows it from
  "rome.eleazar.heart.son.2": ["son", "Dad's late right now. I don't even know which year he's late in."],
  "rome.eleazar.heart.3": ["eleazar", "Then we are both waiting, child. Shall we wait together a little?"],
  "rome.eleazar.opt.together": ["son", "Yes. Together."],
  "rome.eleazar.opt.how": ["son", "I don't know the words you use."],
  "rome.eleazar.how": ["eleazar", "Use your own, child. He knows them all."],
  "rome.eleazar.opt.notnow": ["son", "Can we do it in a little bit? I should check on, um, everything."],
  "rome.eleazar.notnow": ["eleazar", "Whenever you come back. I am not going anywhere, and neither is the promise."],
  "rome.eleazar.opt.waitagain": ["son", "Mister Eleazar? Can we still wait together?"],
  "rome.eleazar.waitagain": ["eleazar", "Come, stand here beside me. We face the same way."],
  // the prayer, side by side, facing toward Jerusalem: the boy's head goes down and his hair stays up
  "rome.eleazar.prayer.son.1": ["son", "Dear God, please help Dad find me. And be with Mister Eleazar while he waits."],
  "rome.eleazar.prayer.son.2": ["son", "You know what he's waiting for. I know too. I didn't tell. Amen."],
  "rome.eleazar.amen": ["eleazar", "Amen."],
  "rome.eleazar.prayed": ["eleazar", "You pray like one who knows him well."],
  "rome.eleazar.prayed.son": ["son", "We talk a lot. Mostly at bedtime."],
  // the blessing: his hand on the boy's head (Genesis 48:14, shown); Numbers 6:25, QUOTED, King James Version, exact
  "rome.eleazar.bless.0": ["eleazar", "Come. Stand still a moment."],
  "rome.eleazar.bless.1": ["eleazar", "For you: 'The LORD make his face shine upon thee, and be gracious unto thee:'"],          // Numbers 6:25, King James Version: exact, colon and all
  "rome.eleazar.bless.son": ["son", "Pastor says that one. But you only did the middle, and I know all three."],      // PASS-17R: the design's own sample (office-hq-design.md, section 1): no reference aloud
  // only if the date seller blessed him (rome.dateseller.bless.2 has been said)
  "rome.eleazar.pieces.son": ["son", "The date seller gave me the first part! You two are doing it in pieces."],
  "rome.eleazar.pieces": ["eleazar", "Yose blessed you too? Then the blessing has walked all over Rome today."],
  // and the boy gives him the last part: Numbers 6:26, QUOTED, King James Version, exact
  "rome.eleazar.opt.last": ["son", "Mister Eleazar? Can I give you the last part?"],
  "rome.eleazar.last.son": ["son", "'The LORD lift up his countenance upon thee, and give thee peace.'"],          // Numbers 6:26, King James Version: exact. PASS-17R: the reference is no longer said after it
  "rome.eleazar.last": ["eleazar", "I will remember the day the blessing came back to me."],
  "rome.eleazar.go": ["eleazar", "Go in peace, child. And find your father."],
  // walking away, to us
  "rome.eleazar.walking": ["son", "I didn't tell him, because it wasn't mine to tell. But I prayed it, and that counts."],
  // a second talk, and every one after
  "rome.eleazar.later": ["eleazar", "I am still waiting. It is easier this morning."],
  // the tassels on his mantle (Numbers 15:38, told)
  "rome.eleazar.opt.tassels": ["son", "What are the strings on your blanket? With the blue in them?"],
  "rome.eleazar.tassels.1": ["eleazar", "It is not a blanket, child. The Law tells us to wear them, so that we remember."],
  "rome.eleazar.tassels.son": ["son", "Like a string on your finger! But holy."],
  "rome.eleazar.tassels.2": ["eleazar", "Yes. Very like that."],
  "rome.eleazar.opt.bye": ["son", "I should go look for Dad. Can I come back?"],
  "rome.eleazar.bye.1": ["eleazar", "The bench will be here. So will I."],
  "rome.eleazar.bye.2": ["eleazar", "Still here. Still the bench."],
  // things carried, shown to him
  "rome.eleazar.coin": ["eleazar", "Keep it safe, child. New silver has a way of walking off in Rome."],
  "rome.eleazar.quarter": ["eleazar", "An eagle, struck proud. Yose would say it is not silver, but it is a fine bird."],
  "rome.eleazar.lamp": ["eleazar", "A lamp for a long road. A gift is heavier than it looks."],
  "rome.eleazar.breakfast": ["eleazar", "The soothsayer's? Take it to him while it is warm."],

  // ---------- Mariam (mariamTree) ----------
  // About eight, the date seller's daughter, born in Rome; Eleazar's granddaughter. Certain about everything, especially
  // hens; bossy, fond, quick to laugh. Not Little Sister's double: her own girl.
  "rome.mariam.look": ["narrator", "A girl in a yard full of hens, with her hands on her hips. The Son knows that look; his little sister has one."],
  "rome.mariam.look2": ["narrator", "The girl has counted her hens again and got the same number. She does not look as if she trusts it."],
  "rome.mariam.opt.hens": ["son", "Are those your hens? They're very organized."],
  "rome.mariam.opt.hens2": ["son", "Why are your hens all staring the same way?"],
  // chickens: four lines of the thread, nobody explaining it (rome.sawHens)
  "rome.mariam.hens.1": ["mariam", "They are in a row. Since first light, every one of them, looking over the river at the city."],
  "rome.mariam.hens.2": ["mariam", "They will not eat. They will not lay. Hens are sensible. Something over there is not."],
  "rome.mariam.hens.2.b": ["son", "Maybe they're praying?"],      // PASS-19R2: new (breaks a run of three; her grandfather's saying answers it)
  "rome.mariam.hens.3": ["mariam", "Grandfather says hens do not pray. They only look."],
  "rome.mariam.hens.son": ["son", "They're looking at my door. From the other side of a whole river."],
  "rome.mariam.opt.name": ["son", "I'm collecting names. What's yours?"],
  "rome.mariam.name": ["mariam", "Mariam. And you are the boy with lights on his feet. That is better than a name."],
  "rome.mariam.opt.window": ["son", "Is that your grandpa? Up in the window?"],
  "rome.mariam.window": ["mariam", "He comes down when he has finished, and he does not hurry for anybody."],
  "rome.mariam.opt.bench": ["son", "Is that your grandpa? On the bench, with the scroll?"],
  "rome.mariam.bench": ["mariam", "Do not stand in his light. He says you are, even when you are not."],
  "rome.mariam.opt.boss": ["son", "Are you the boss of this yard?"],
  "rome.mariam.boss.1": ["mariam", "The yard, the hens, the water dish, and Grandfather. Mostly Grandfather."],
  "rome.mariam.boss.son": ["son", "My little sister would love you. You'd boss each other around all day and have the best time."],
  "rome.mariam.boss.2": ["mariam", "I am not bossy, I am in charge. It is different."],
  "rome.mariam.again": ["mariam", "Lights-on-his-feet! The hens are still looking."],
  "rome.mariam.opt.crouch": ["son", "Can you ask one what's wrong?"],
  "rome.mariam.crouch.1": ["mariam", "You do not ask a hen. You look her in the eye."],
  "rome.mariam.crouch.2": ["mariam", "She blinked. That means not sick, just busy."],
  "rome.mariam.crouch.3": ["mariam", "Still busy. You cannot hurry a hen, or a grandfather."],
  "rome.mariam.opt.family": ["son", "Do you live here with your grandpa?"],
  "rome.mariam.family.1": ["mariam", "Father sells dates in the city, from Jericho. They are the best."],
  "rome.mariam.family.2": ["mariam", "The first one free. Mother says we will be poor. Father says, then poor with friends."],
  "rome.mariam.dates.son": ["son", "The date seller? I know him. He gave me a date with a rock in it."],
  "rome.mariam.dates": ["mariam", "That is the stone, silly. It is a tree that has not started yet."],
  // the words of the Law on the doorpost (Deuteronomy 6:9, told in her own words)
  "rome.mariam.opt.doorpost": ["son", "What's the little case on your door?"],
  "rome.mariam.doorpost.1": ["mariam", "Words of the Law. It says to write them on the doorposts, so we do."],
  "rome.mariam.doorpost.son": ["son", "Like a note on the fridge! But on the door, and forever."],
  "rome.mariam.doorpost.2": ["mariam", "What is a fridge?"],
  "rome.mariam.doorpost.son2": ["son", "A cold cupboard. With magnets."],
  "rome.mariam.doorpost.3": ["mariam", "Words of the Law, and do not poke it. Everybody wants to poke it."],
  "rome.mariam.opt.bye": ["son", "Good luck with the hens."],
  "rome.mariam.bye.1": ["mariam", "They do not need luck. They need to finish looking."],
  "rome.mariam.bye.2": ["mariam", "Still looking."],
  // things carried, shown to her
  "rome.mariam.gaultoga": ["mariam", "That is not a blanket, that is a tent. Can the hens have it?"],
  "rome.mariam.coin": ["mariam", "Silver. Father would say: that is a lot of dates."],
  "rome.mariam.quarter": ["mariam", "A bird. Is it a hen? No, a hen has more sense than to sit on a coin."],
  "rome.mariam.gum": ["mariam", "Is it food? The hens will not eat today, and I am not a hen."],
  "rome.mariam.breakfast": ["mariam", "The hens will not want it. I tried figs, even figs."],
  "rome.mariam.lamp": ["mariam", "A lamp, for Felix? He is going to Corinth, he told the hens."],

  // ---------- Felix (NEW 4's middle; felixTree) ----------
  // Gaius Fannius Felix, about twenty-six, Phyllis's son, born free: a boatman on the barges between here and Ostia,
  // his name down for Corinth. Cheerful, impatient, soft about his mother, full of Corinth.
  "rome.felix.look": ["narrator", "A big sunburnt man loading the barge. He keeps looking over at the bridge."],      // PASS-17R: shorter
  "rome.felix.look2": ["narrator", "The boatman is whistling without a tune. It is just air with big plans."],
  // ways in (the first, when the boy is carrying his mother's lamp)
  "rome.felix.opt.felix": ["son", "Are you Felix? Phyllis's Felix, the tall sunburnt one in a hurry?"],
  "rome.felix.felix": ["felix", "All three. Who is asking, and how do you know my mother?"],
  "rome.felix.opt.carry": ["son", "What are you carrying? Is it heavy, and can I try?"],
  "rome.felix.carry": ["felix", "Papyrus. And no. You would end up in the river, and I would be the one explaining."],
  "rome.felix.opt.table": ["son", "Is that a boat? It looks like a table that floats."],
  "rome.felix.table": ["felix", "It is a barge, friend. A table does not go down to Ostia and back."],
  "rome.felix.opt.where": ["son", "Where does the boat go?"],
  "rome.felix.where": ["felix", "Down to Ostia, where the big ships wait. Soon, me with them."],
  "rome.felix.again": ["felix", "Back again? I am still carrying, so talk while I walk."],
  "rome.felix.opt.name": ["son", "Who are you? I'm collecting names."],
  "rome.felix.name": ["felix", "Felix. Gaius Fannius Felix, if you are writing it down."],
  "rome.felix.opt.ostia": ["son", "What's Ostia?"],
  "rome.felix.ostia.1": ["felix", "The port. The big ships wait off the shore."],
  "rome.felix.ostia.2": ["felix", "We bring the cargo up. Papyrus, linen, jars of everything."],
  "rome.felix.ostia.3": ["felix", "Ostia. Sea. Ships. Barges. Me. Up and down. That is the whole of it."],
  // Corinth (and the Son, to us, at the name: Acts 18:1-3 and the two letters, in his own words; then he stops himself)
  "rome.felix.opt.corinth": ["son", "What's in Corinth?"],
  "rome.felix.corinth.1": ["felix", "Nothing yet, and that is the beauty of it. The dictator is building it again."],
  "rome.felix.corinth.2": ["felix", "My name is down. A house of my own, in a city with a sea on each side."],
  "rome.felix.corinth.3": ["felix", "Corinth. A house. Two seas! Sorry."],
  "rome.felix.paul.son.1": ["son", "Corinth! Paul lives there one day, and makes tents, and there are two letters..."],
  "rome.felix.paul.son.2": ["son", "Nope. Operation Don't Wreck Anything."],
  "rome.felix.paul": ["felix", "Are you all right? You went funny."],
  "rome.felix.paul.son.3": ["son", "I'm fine. Corinth sounds great, and I'd move there."],
  "rome.felix.opt.mother": ["son", "Your mom's in the Forum, with the flowers."],
  "rome.felix.mother.1": ["felix", "Selling to half of Rome. She cannot leave her baskets today."],
  "rome.felix.mother.2": ["felix", "So I wave at the Forum. She cannot see me, but I wave anyway."],
  "rome.felix.mother.3": ["felix", "Tell her I am eating. She will ask; she always asks."],
  // the lamp (the lever: hook setDown, then lamp), his mother's wish, and his word
  "rome.felix.opt.lamp": ["son", "Special delivery! It's a lamp from your mom, for Corinth."],
  "rome.felix.gift.1": ["felix", "From her? But she cannot leave her baskets, so she sent you?"],
  "rome.felix.gift.son.1": ["son", "She threw a wish in the fountain for you. I sort of borrowed it. Long story."],
  "rome.felix.gift.2": ["felix", "She threw a coin in a fountain? For me?"],
  "rome.felix.gift.3": ["felix", "She never throws anything. She keeps string."],
  "rome.felix.gift.son.2": ["son", "She wants to hear you say you'll come. Before you go."],
  "rome.felix.opt.come": ["son", "Will you come and say goodbye?"],
  "rome.felix.word.1": ["felix", "Tell her I will come over the bridge at the ninth hour. Before the barge goes."],
  "rome.felix.word.2": ["felix", "And tell her I will light it in Corinth. The first night. In the first window."],
  "rome.felix.word.son": ["son", "Lamp delivered and promise picked up. For a two-way errand, I should start charging."],
  "rome.felix.opt.string": ["son", "String? Like, just regular string?"],
  "rome.felix.string": ["felix", "Every bit of string we ever had, in a jar, since before I was born."],
  "rome.felix.string.son": ["son", "My mom keeps rubber bands on the doorknob. It's a ball now."],
  "rome.felix.after": ["felix", "The ninth hour, I have not forgotten. I have told the bales twice."],
  "rome.felix.opt.bye": ["son", "I'll let you work, boat guy."],
  "rome.felix.bye.1": ["felix", "Mind the edge. The Tiber is cold, and I am busy."],
  "rome.felix.bye.2": ["felix", "Still busy."],
  "rome.felix.bye.after": ["felix", "The ninth hour! Tell her again, in case."],
  // things carried, shown to him (the lamp starts his talk)
  "rome.felix.gaultoga": ["felix", "That would make a fine sail. Not my business, though, I have bales."],
  "rome.felix.coin": ["felix", "New silver, by the river? Put it away before it goes for a swim."],
  "rome.felix.breakfast": ["felix", "Sausage, and not for me? Then do not wave it at a working man."],

  // ================= carried things =================
  "item.toga.look": ["narrator", "The senator's clean toga. It is heavier than the Son's backpack, and does a good deal less."],
  "item.tunic.look": ["narrator", "A boy's tunic, the Son's size, to be brought back clean. The washerwoman has not seen him eat."],
  "item.breakfast.look": ["narrator", "The soothsayer's breakfast: bread and a sausage, knotted up in a cloth. The Son is not eating it. Smelling is free."],
  "item.incense.look": ["narrator", "The soothsayer's box of incense, for the god. It rattles, and the Son has not opened it. He calls that growth."],
  "item.coin.look": ["narrator", "A new silver coin with a serious man on it. He looks as if he has never had a snack in his life."],              // kept
  "item.coin.mom": ["narrator", "A silver coin with a stern gentleman on it. It looks old and new at once; Big Sister will know which."],     // kept (Act Four)
  "item.coin.bigsis": ["narrator", "A denarius of Julius Caesar, struck in 44 B.C. and not a day older. Big Sister is not letting go of it."],        // kept (Act Four)
  "item.coin.lilsis": ["narrator", "A coin with a grumpy man on it. Little Sister thinks he needs a snack."],                                                   // kept (Act Four)
  // his own things: looked at, tried on people, never the answer to anything
  "item.phone.look": ["narrator", "The Son's phone. It died doing what it loved: taking four hundred pictures of a donkey."],
  "item.quarter.look": ["narrator", "An emergency quarter, for a pay phone. The Son has never seen a pay phone, though he has now seen Rome."],
  "item.gum.look": ["narrator", "Half a pack of gum. The other half is under the car seat, a problem for later, or possibly for earlier."],
  // ROME-13W: the two new things carried (world.js: gaultoga, lamp)
  "item.gaultoga.look": ["narrator", "The Gaul's toga, the size of a parachute. The Son could camp in it, with friends."],
  "item.lamp.look": ["narrator", "Phyllis's goodbye lamp for Felix, a little clay one. The Son carries it like an egg, a very important egg."],

  // ================= hints: one for each puzzle, in his own voice =================
  "hint.rome.toga": ["son", "The door guy wants a clean tunic. The laundry lady out on the street has a whole line of them."],
  "hint.rome.delivered": ["son", "This bedsheet belongs to the senator. He's the one in a hurry, back by the temple steps."],
  "hint.rome.tunic": ["son", "Bedsheet delivered. The laundry lady owes me one tunic, so I should go and collect."],
  "hint.rome.breakfast": ["son", "The chicken man has incense and no breakfast. The snack bar has breakfast. I smell a trade."],
  "hint.rome.incense": ["son", "The chicken man's breakfast is in my backpack. It's getting cold, and so is he."],
  "hint.rome.coin": ["son", "That fountain is full of other people's wishes. I only need to borrow one."],                         // kept
  "hint.rome.inside": ["son", "I've got a clean tunic and something for the god. Time to show the door guy."],
  "hint.rome.spark": ["son", "There's sun on the temple floor and a shiny coin in my backpack. I could bounce it at the hum."],
  "hint.rome.toss": ["son", "The humming door ate me. Maybe it eats money too. For science."],                                    // kept
  // ROME-13W: the new beats' hints. (hint.rome.delivered keeps its words and now speaks for the first delivery, the
  // wrong toga; hint.rome.breakfast keeps its words: the snack bar is still where to ask.) hint.rome.gaul is one line
  // that helps both before and after he has heard where the Senate meets.
  "hint.rome.gaul": ["son", "The lost Gaul in the Forum has the toga. He needs to know where the Senate meets, and my senator knows."],
  "hint.rome.delivered2": ["son", "It's the right bedsheet now, and the senator's at the temple steps. Delivery, take two."],
  "hint.rome.geese": ["son", "The breakfast is up the hill with a stuck kid. The sad guy with the basket knows all about geese."],
  "hint.rome.wish": ["son", "That coin was Phyllis's wish. I'd better ask her first, in the Forum, by the violets."],
  "hint.rome.felix": ["son", "Phyllis's lamp is for her boy, Felix. He loads barges across the river, below the stone bridge."],
  "hint.rome.granted": ["son", "Felix said yes. Back to the Forum to tell his mom, the flower lady."],
  // ---- TALK-24 (10 November: dialogue trees with topics, every act): the topics a talk's questions are gathered under ----
  "rome.gaul.topic.guess": ["son", "Let me guess where the Senate meets."],
  "rome.phyllis.topic.today": ["son", "Questions about today. Everybody's got garlands."],
  "rome.titus.topic.him": ["son", "Questions about you. Since you're not going anywhere."],
  "rome.anser.topic.more": ["son", "Random questions, though. I have a few."],
  "rome.mariam.topic.home": ["son", "Can I ask some nosy questions? Nice nosy."],
  "rome.clerk.topic.temple": ["son", "Questions about this place. It's so shiny."],
  "rome.senator.topic.him": ["son", "You look important. Can I ask about you?"],
};
