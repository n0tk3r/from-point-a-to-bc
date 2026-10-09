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
// Nobody of the time ever uses a modern word; he never stops.
//
// THE FAMILY'S FAITH, AND THE BIBLE'S HISTORY AS HISTORY (briefs/WEAVE.md). The Son is ten and has been to Sunday
// school all his life. Fifty-five lines carry it, each marked "woven" where its group begins:
//   - Scripture is quoted twice, word for word from the King James Version (the texts are in briefs/out/facts-home.md):
//     Micah 5:2, its first clause (rome.dateseller.ans.pray.2), and Numbers 6:24 (rome.dateseller.bless.1). Each ends
//     on the King James mark, a comma and a colon, because each verse runs on. Do not "tidy" them.
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

export const lines = {
  // ================= rome-steps: the steps of the temple =================

  // ---------- arrival ----------
  "rome.arrive.out": ["doorkeeper", "And stay out. The treasury of the Roman People is not a nursery."],
  "rome.arrive.1": ["son", "Dad? ... This is NOT the rest stop. The rest stop had a vending machine."],                  // kept
  "rome.arrive.2": ["son", "Everyone here is wearing a bedsheet. Ten out of ten. Biggest sleepover in history."],        // kept
  "rome.arrive.4": ["son", "The humming door let me out INSIDE that building. Then it shut. Not even a goodbye hum."],
  "rome.arrive.5": ["son", "Then the big guy carried me out by my backpack. Like luggage. I'm carry-on."],
  "rome.arrive.3": ["son", "Okay. Operation Find Dad. Step one: snacks. Step two: also Dad."],                           // kept
  "rome.arrive.6": ["son", "Step three: get back in there. I'm adding a step. It's my operation."],
  "rome.arrive.7": ["son", "Step one is THAT way, past the bush. My nose is never wrong about snacks."],

  // ---------- the temple front, the doors, the doorkeeper ----------
  "rome.temple.look": ["son", "Giant stripy pillars. Dad would say they're holding up well. Seven out of ten. Would climb."],   // kept
  "rome.temple.use": ["son", "Would climb. Will not climb. The door guy can throw a lot farther than fourteen steps."],
  "rome.doors.look": ["son", "Giant doors, wide open, and I still can't get in. That's the most door a door can be."],
  "rome.doors.look2": ["son", "Wide open. And this time they're open for ME. Three out of three. I'm basically staff."],
  "rome.stairs.look": ["son", "Fourteen steps. I counted them on the way down. Upside down."],

  "rome.doorkeeper.look": ["son", "A door with arms, standing in front of a door. That's two doors. That's cheating."],
  "rome.doorkeeper.look2": ["son", "He hasn't blinked since he put me down. I'm not counting. ...Okay, I'm counting."],
  "rome.doorkeeper.hi.1": ["son", "Hi. Me again. I left a door in there. A hummy one. Can I go and get it?"],
  "rome.doorkeeper.hi.2": ["doorkeeper", "No."],
  "rome.doorkeeper.hi.3": ["son", "Do ANY kids get to go in?"],
  "rome.doorkeeper.rule.1": ["doorkeeper", "Boys go in. The boys who serve at the rites."],
  "rome.doorkeeper.rule.2": ["doorkeeper", "A boy. In a clean tunic. Carrying something for the god."],
  "rome.doorkeeper.rule.3": ["doorkeeper", "You are a boy. That is one out of three."],
  "rome.doorkeeper.rule.4": ["son", "He does scores! Out of THREE, though. Weird system."],
  "rome.doorkeeper.ask.rule": ["son", "What were the three things again?"],
  "rome.doorkeeper.ans.rule": ["doorkeeper", "A boy. A clean tunic. Something in his hands for the god. I will not sing it."],
  "rome.doorkeeper.ask.what": ["son", "What's in there, anyway?"],
  "rome.doorkeeper.ans.what.1": ["doorkeeper", "The god Saturn. And at his feet, the treasury of the Roman People."],
  "rome.doorkeeper.ans.what.2": ["son", "A church AND a bank. Dad would call that one-stop shopping."],
  "rome.doorkeeper.ask.dad": ["son", "Have you seen my dad? Tall, little beard, flowers on his shirt?"],
  "rome.doorkeeper.ans.dad.1": ["doorkeeper", "No."],
  "rome.doorkeeper.ans.dad.2": ["son", "He might be asking somebody for directions. ...No. He would NEVER."],
  "rome.doorkeeper.ans.dad.3": ["doorkeeper", "Then he is lost."],
  "rome.doorkeeper.ans.dad.4": ["son", "He's not lost. He's making good time. Somewhere."],
  "rome.doorkeeper.ask.bye": ["son", "Okay. Bye. Don't go anywhere."],
  "rome.doorkeeper.ans.bye": ["doorkeeper", "I never do."],
  "rome.doorkeeper.need.both": ["doorkeeper", "One out of three. I am not a difficult man. I am an exact one."],
  "rome.doorkeeper.need.gift.1": ["doorkeeper", "A clean tunic. Good. And for the god you bring two empty hands. Two out of three."],
  "rome.doorkeeper.need.gift.2": ["son", "My score went UP. I'm improving!"],
  "rome.doorkeeper.need.tunic.1": ["doorkeeper", "Incense for the god. Good. Carried by a boy dressed as I do not know what. Two out of three."],
  "rome.doorkeeper.need.tunic.2": ["son", "It's a hoodie. It's from the future. It was on sale."],
  "rome.doorkeeper.again": ["doorkeeper", "You again. In. Touch nothing again."],
  "rome.doorkeeper.toga": ["doorkeeper", "That is a senator's toga. Senators are down there. I am up here. We both prefer it."],
  "rome.doorkeeper.breakfast.1": ["doorkeeper", "I do not eat at the door. ...Is that the sausage from the street with the fountain?"],
  "rome.doorkeeper.breakfast.2": ["son", "It's the chicken man's."],
  "rome.doorkeeper.breakfast.3": ["doorkeeper", "Then it is the chicken man's."],
  "rome.doorkeeper.coin": ["doorkeeper", "One coin. For the treasury. It has others."],
  "rome.doorkeeper.quarter": ["doorkeeper", "That is not a coin. I do not know what it is. Put it away before I have to find out."],
  "rome.doorkeeper.phone": ["doorkeeper", "A small black door. It is shut. I approve."],

  // the gate: in the tunic, with the incense
  "rome.gate.1": ["son", "Tunic: ON. It goes over the hoodie. And the backpack. I'm a lumpy Roman."],
  "rome.gate.2": ["son", "One boy. One clean tunic. One box of holy smell for the god."],
  "rome.gate.3": ["doorkeeper", "...Three out of three."],
  "rome.gate.4": ["son", "YES."],
  "rome.gate.5": ["doorkeeper", "The cap."],
  "rome.gate.6": ["son", "The cap is load-bearing."],
  "rome.gate.7": ["doorkeeper", "...Go in. Walk. Touch nothing. The clerk is counting."],
  "rome.gate.8": ["son", "Operation Temple Kid is GO."],

  // ---------- the soothsayer and his sacred chickens ----------
  "rome.soothsayer.look": ["son", "An old guy in a bedsheet hoodie, with pet chickens. He looks like he read the last page first."],
  "rome.soothsayer.look2": ["son", "He keeps sighing at the steps. The steps don't care. Steps never do."],
  "rome.soothsayer.hi.1": ["soothsayer", "Beware the Ides of March."],
  "rome.soothsayer.hi.2": ["son", "Which one is Ides?"],
  "rome.soothsayer.hi.3": ["soothsayer", "Today."],
  "rome.soothsayer.hi.4": ["son", "Then it's a bit late to be-ware."],
  "rome.soothsayer.hi.5": ["soothsayer", "I said it in February, too. Nobody listened then, either."],
  "rome.soothsayer.ask.birds": ["son", "Why do you keep chickens in a cage?"],
  "rome.soothsayer.ans.birds.1": ["soothsayer", "They are sacred. When they feed well, the day is good. Today they will not touch a grain."],
  // chickens: he takes it for the worst of omens, which for a man selling omens on the Ides of March it is. (The id gives him a hand across his brow.)
  "rome.soothsayer.ans.birds.omen": ["soothsayer", "The worst omen there is, and on the Ides. I sell omens, boy. This one I could not give away."],
  "rome.soothsayer.ans.birds.2": ["son", "Maybe they're just not breakfast chickens."],
  "rome.soothsayer.ans.birds.3": ["soothsayer", "Nor am I, today. My bread and sausage come up from the cookshop by the fountain. Not this morning."],
  "rome.soothsayer.ans.birds.4": ["soothsayer", "I foresaw it. It did not help."],
  "rome.soothsayer.ans.birds.fed": ["soothsayer", "They feed. Look at them. I have decided not to ask them why."],
  "rome.soothsayer.ask.temple": ["son", "Can you get me into the temple?"],
  "rome.soothsayer.ans.temple.1": ["soothsayer", "I cannot get myself in. I have incense for Saturn that should have gone in at dawn."],
  "rome.soothsayer.ans.temple.2": ["soothsayer", "There are fourteen steps between it and him. My knees have foreseen every one."],
  "rome.soothsayer.ans.temple.3": ["son", "I could carry it! I'm great at steps. I've already done those ones."],
  "rome.soothsayer.ans.temple.4": ["soothsayer", "Not today. The birds will not feed, and I have no breakfast to tempt them. I send the god nothing."],
  "rome.soothsayer.ans.temple.fed": ["soothsayer", "You are carrying it. Do not drop it. I have not foreseen you dropping it, which is something."],
  "rome.soothsayer.ask.future": ["son", "Can you tell MY future?"],
  "rome.soothsayer.ans.future.1": ["soothsayer", "Give me your hand. ...Hm. A long road. You will be very late for supper."],
  "rome.soothsayer.ans.future.2": ["son", "He's GOOD."],
  "rome.soothsayer.ans.future.3": ["son", "Do I find my dad?"],
  "rome.soothsayer.ans.future.4": ["soothsayer", "The birds do not say. But boys who look, find. That is not prophecy. That is boys."],
  "rome.soothsayer.ask.bye": ["son", "Okay. Bye! Happy Ides!"],
  "rome.soothsayer.ans.bye": ["soothsayer", "It is not that kind of day."],
  "rome.soothsayer.fed.1": ["son", "Breakfast! From the snack guy. He says you owe him for eleven years."],
  "rome.soothsayer.fed.2": ["soothsayer", "I foresaw this sausage at dawn. It is the only thing I have foreseen all year that I wanted."],
  "rome.soothsayer.fed.3": ["soothsayer", "A few crumbs for the birds. ...They feed. Look at them feed."],
  "rome.soothsayer.fed.4": ["soothsayer", "A good omen. For somebody. It may even be you."],
  "rome.soothsayer.fed.5": ["soothsayer", "Take this incense in to the god, boy. Fourteen steps. My knees send their regards."],
  "rome.soothsayer.fed.6": ["son", "First a sausage, now a box of holy smell. I'm a delivery truck with a hat."],
  "rome.soothsayer.toga": ["soothsayer", "Not mine. Mine has known soup. That one has a future."],
  "rome.soothsayer.coin.1": ["soothsayer", "It is wet. I foresee that it came from a fountain."],
  "rome.soothsayer.coin.2": ["son", "WHOA. How did you..."],
  "rome.soothsayer.coin.3": ["soothsayer", "It is dripping on my foot."],
  "rome.soothsayer.quarter": ["soothsayer", "A bird, and a man with his hair tied back. I do not know this omen. I dislike that."],
  "rome.soothsayer.incense": ["soothsayer", "It goes UP the steps, boy. That is the whole of the favor."],

  "rome.birdcage.look": ["son", "Chickens in a cage. They've got the look Mom gets when Dad says 'shortcut'."],
  "rome.birdcage.look2": ["son", "Sacred chickens. I asked one what makes it sacred. It said nothing. Very professional."],
  "rome.birdcage.use": ["son", "Here, chick chick. ...Nothing. They can tell I don't have snacks. Chickens always know."],
  // chickens: they all stand facing the temple doors, where the door in time is. He notices it himself (the first time he
  // calls them, or the second time he looks, fed or not), and thinks of his little sister. He does not explain it.
  // (The ids give him a point up the steps, then both arms up for the General.)
  "rome.birdcage.doors.1": ["son", "...Huh. They're all facing up the steps. At the temple doors. Every single one. Chickens KNOW."],
  "rome.birdcage.doors.2": ["son", "That's what my little sister says. She has a chicken called General Feathers. The General outranks me."],
  "rome.birdcage.fed": ["son", "Now they're eating like it's a contest. Good omen! I don't know what for. It still counts."],
  "rome.birdcage.breakfast": ["son", "That's the old guy's breakfast. If I feed it to his chickens, he'll foresee me doing it."],

  // ---------- the senator ----------
  "rome.senator.look": ["son", "A man in a giant bedsheet, standing still in a hurry. Dad does that at red lights."],
  "rome.senator.look2": ["son", "Purple stripe, red shoes, pink face. He's a whole box of crayons."],
  "rome.senator.hi.1": ["senator", "Boy. Do you know who I am?"],
  "rome.senator.hi.2": ["son", "No. Do you know who I am?"],
  "rome.senator.hi.3": ["senator", "...No."],
  "rome.senator.hi.4": ["son", "Then we're tied."],
  "rome.senator.hi.5": ["senator", "I am a senator of Rome, and I am LATE, and my clean toga is still at the laundry."],
  "rome.senator.ask.late": ["son", "Late for what?"],
  "rome.senator.ans.late.1": ["senator", "The Senate meets today, in the hall beside Pompey's theater. I have a speech."],
  "rome.senator.ans.late.2": ["senator", "It is about drains. It is magnificent."],
  "rome.senator.ans.late.3": ["son", "How long is it?"],
  "rome.senator.ans.late.4": ["senator", "It ends when they agree with me."],
  "rome.senator.ask.toga": ["son", "You're already wearing a bedsheet. A really big one."],
  "rome.senator.ans.toga.1": ["senator", "This is YESTERDAY'S toga. It has an olive stain. Here. The Senate would look at nothing else."],
  "rome.senator.ans.toga.2": ["son", "I can't even see it."],
  "rome.senator.ans.toga.3": ["senator", "They would. Finding the stain on another man is most of what we do."],
  "rome.senator.ans.toga.4": ["senator", "The washerwoman by the fountain has had my best one for three days. THREE."],
  // woven: the great-nephew nobody thinks about is the Caesar Augustus of Luke 2:1. Nobody in Rome knows it this morning.
  "rome.senator.ask.caesar": ["son", "Does Caesar have a kid? A kid like that could get in ANYWHERE."],
  "rome.senator.ans.caesar.1": ["senator", "Caesar has no son. There is a great-nephew: Gaius Octavius, eighteen, off at his books in Apollonia."],
  "rome.senator.ans.caesar.2": ["senator", "Nobody gives the boy a thought. I mention him only because I am thorough."],
  "rome.senator.ans.caesar.3": ["son", "I know another Caesar! Caesar AUGUSTUS. Luke 2:1. He counts everybody. It's how the Christmas story starts."],
  "rome.senator.ans.caesar.4": ["senator", "Augustus. There is no such name. I know every name in Rome that matters."],
  "rome.senator.ans.caesar.5": ["son", "...Not yet."],
  "rome.senator.ask.dad": ["son", "Have you seen my dad? Little beard, shirt with flowers all over it?"],
  "rome.senator.ans.dad.1": ["senator", "Flowers. On a shirt. In the Forum. No. I would have made a speech about it."],
  "rome.senator.ans.dad.2": ["son", "Mom's made a few."],
  "rome.senator.ask.bye": ["son", "Good luck with the drains!"],
  "rome.senator.ans.bye": ["senator", "Luck is for men without speeches."],
  "rome.senator.toga.1": ["son", "Delivery! One clean bedsheet with a purple stripe. From the laundry lady."],
  "rome.senator.toga.2": ["senator", "A TOGA, boy. A bedsheet covers a man asleep. A toga covers a man who matters."],
  "rome.senator.toga.3": ["son", "It's really heavy for something with no pockets."],
  "rome.senator.toga.4": ["senator", "Rome thanks you. I, personally, am far too late."],
  "rome.senator.toga.5": ["senator", "To the Senate! They would never dare begin without me."],
  "rome.senator.toga.6": ["son", "Operation Bedsheet Delivery: complete. The laundry lady owes me one tunic."],
  "rome.senator.breakfast": ["senator", "I do not eat in the street. I am SEEN in the street."],
  "rome.senator.incense": ["senator", "Incense is for gods. I am only a senator. ...Only."],

  // ---------- the rest of the Forum ----------
  "rome.altar.look": ["son", "A stone barbecue wearing a flower necklace. Nothing's cooking. Smells nice, though. Six out of ten."],
  "rome.altar.use": ["son", "Dad says never touch a grill you didn't light. It's his only barbecue rule. He breaks it."],
  "rome.altar.incense": ["son", "The chicken man said take it IN to the god. This is the outside. I listen. Sometimes."],
  "rome.forum.look": ["son", "A whole downtown and not one car. Everybody's walking and yelling. It's recess for grown-ups."],
  "rome.forum.look2": ["son", "There's a temple on top of that hill, too. This city puts temples on everything. Like sprinkles."],
  "rome.stone.look": ["son", "S. P. Q. R. No vowels. You can't even sneeze that."],
  "rome.pigeons.look": ["son", "Pigeons. The exact same pigeons as at home. Maybe they time travel. It would explain a LOT."],
  "rome.pigeons.use": ["son", "I'm not chasing them. I chased one at a rest stop once and Dad had to apologize to a truck."],
  "rome.tripod.look": ["son", "A giant bronze cake stand. No cake. Rome keeps getting my hopes up."],
  "rome.board.look": ["son", "A notice board. Rows of tiny letters. Rome has terms and conditions. Nobody reads them here either."],
  "rome.tostreet.look": ["son", "The street smells of bread, sausage and one other thing. I'm choosing not to know the other thing."],
  "rome.cart.look": ["son", "A cart of fat sacks, parked at a tiny door under the temple. The treasury has a drive-through."],
  "rome.dog.look": ["son", "A dog! Asleep in the shade. I ask for one every birthday. Dad says we'll see. We never see."],
  "rome.dog.use": ["son", "Here, boy! ...He opened one eye. Then he shut it. Ten out of ten. Would adopt."],
  "rome.dog.breakfast": ["son", "One sausage and that dog is mine. But it's the chicken man's. Hardest thing I've ever NOT done."],

  // ================= rome-street: the shopping street =================

  "rome.street.arrive.1": ["son", "Whoa. A whole street of snacks and laundry."],
  // woven: he hears whose nose is on the new money, and works out when he is. (The era card has just told the
  // player "44 B.C."; this is where he catches up, and where everything he says "Not yet." about begins.)
  "rome.street.cry": ["keeper", "Hot sausage, hot bread, old silver, new silver, the new has Caesar's nose on it, I take every nose!"],
  "rome.street.bc.1": ["son", "Caesar? JULIUS Caesar? Big Sis has him on her timeline. Before the red mark. That whole side is B.C."],
  "rome.street.bc.2": ["son", "B.C. Before Christ. ...So Jesus hasn't been born."],
  "rome.street.bc.3": ["son", "So it's before Christmas. Not this Christmas. EVERY Christmas. All of them. The FIRST one."],
  "rome.street.bc.4": ["son", "Operation Don't Wreck Anything. I mean it. I've never been in front of anything this big."],
  "rome.street.arrive.2": ["son", "Step one, I can SMELL you."],
  "rome.toforum.look": ["son", "The big temple, way down there. The hum's inside. So's the door guy. One of them likes me."],

  // ---------- the snack bar and its keeper ----------
  "rome.snackbar.look": ["son", "A counter with giant soup jars sunk into it. Bread. Sausages. Garlic on a rope. Step one: FOUND."],
  "rome.snackbar.look2": ["son", "A stove, a pot, cups on a shelf, no front wall. It's a kitchen you can walk past. Best idea ever."],
  "rome.pricelist.look": ["son", "A menu, painted right on the wall. No pictures. How do you know what a thing LOOKS like?"],
  "rome.keeper.look": ["son", "He's cooking, talking and waving a spoon, all at once. He's like three dads."],
  "rome.keeper.look2": ["son", "He hasn't stopped talking since I got here. I don't think he's breathed. He might be part fish."],
  "rome.keeper.hi.1": ["keeper", "A customer, a small one, you are too thin, everybody is too thin, here, eat, eat."],
  "rome.keeper.hi.2": ["son", "Bread with cheese IN it. Step one: DONE. Nine out of ten. It only needs ketchup."],
  "rome.keeper.hi.3": ["keeper", "It needs what?"],
  "rome.keeper.hi.4": ["son", "Ketchup. It's tomatoes, but a sauce."],
  "rome.keeper.hi.5": ["keeper", "What is a tomato?"],
  "rome.keeper.hi.6": ["son", "...No tomatoes. Dad's been saving those little packets for years. He KNEW."],
  "rome.keeper.errand.1": ["keeper", "Never mind, you have legs, fast legs, take this to the old soothsayer on the temple steps."],
  "rome.keeper.errand.2": ["keeper", "Bread and a sausage, every morning, eleven years, my boy has not come, I cannot leave the pot."],
  "rome.keeper.errand.3": ["keeper", "Tell him he owes me for all eleven, he will say he foresaw it, he always foresaw it."],
  "rome.keeper.errand.4": ["son", "Operation Sausage Express. I won't eat it. I'll just THINK about eating it. That's allowed."],
  "rome.keeper.ask.pay": ["son", "How much do I owe you? I've got a quarter."],
  "rome.keeper.ans.pay.1": ["keeper", "Who is this? I know every consul's nose. That is not a consul."],
  "rome.keeper.ans.pay.2": ["son", "That's George. He's on all the quarters."],
  "rome.keeper.ans.pay.3": ["keeper", "I do not know George, I do not know his nose, keep him, you pay me later, everyone pays me later."],
  "rome.keeper.ans.pay.4": ["son", "He gave me a tab. I have a TAB. I'm telling everyone."],
  "rome.keeper.ask.pizza": ["son", "Do you have pizza?"],
  "rome.keeper.ans.pizza.1": ["keeper", "What is pizza?"],
  "rome.keeper.ans.pizza.2": ["son", "Flat bread. Cheese. Sauce."],
  "rome.keeper.ans.pizza.3": ["keeper", "Flat bread I have, cheese I have, what is the sauce?"],
  "rome.keeper.ans.pizza.4": ["son", "...Tomatoes."],
  "rome.keeper.ans.pizza.5": ["keeper", "This word again."],
  "rome.keeper.ask.owe": ["son", "Does everybody owe you money?"],
  "rome.keeper.ans.owe.1": ["keeper", "The senator, forty dinners, the washerwoman's husband, nine, the soothsayer, eleven years."],
  "rome.keeper.ans.owe.2": ["keeper", "The wall is for prices, my head is for debts, my head is very full."],
  "rome.keeper.ans.owe.3": ["son", "Dad owes me four dollars. I keep that in MY head too. There's plenty of room."],
  "rome.keeper.ask.dad": ["son", "Have you seen my dad? Little beard, flowers on his shirt, always making good time?"],
  "rome.keeper.ans.dad.1": ["keeper", "No, and I see everyone, everyone eats, if he is in Rome he will come here, so sit, wait, eat."],
  "rome.keeper.ans.dad.2": ["son", "That's the best plan anybody's had all day. It has snacks in it."],
  "rome.keeper.ask.bye": ["son", "Thanks for the snack! Best step one ever."],
  "rome.keeper.ans.bye": ["keeper", "Go, come back, bring the plate, there was no plate, go."],
  "rome.keeper.coin.1": ["keeper", "THAT nose I know, that is Caesar, struck this year, good silver, everybody knows that nose."],
  "rome.keeper.coin.2": ["son", "He looks like he needs a sausage."],
  "rome.keeper.coin.3": ["keeper", "Everybody needs a sausage, that is my whole trade."],
  "rome.keeper.coin.4": ["son", "I can't spend it, though. It's a borrowed wish. There are rules. Probably."],
  "rome.keeper.toga": ["keeper", "A senator's toga, in my shop, beside my sauce, out, out, I cannot pay to have it washed twice."],
  "rome.keeper.breakfast": ["keeper", "No, no, UP the street, the old one with the chickens, why are you still here, it is getting cold."],
  "rome.keeper.gum.1": ["son", "Want some gum? You chew it, but you never eat it."],
  "rome.keeper.gum.2": ["keeper", "Food that is never eaten, that is the saddest thing anyone has said at my counter."],

  // ---------- the washerwoman and her laundry ----------
  "rome.washer.look": ["son", "She folds a sheet in four moves. I've seen Dad fight one for ten minutes and lose."],
  "rome.washer.look2": ["son", "She's got arms like the door guy. I'd watch that arm wrestle. I'd bring snacks."],
  "rome.washer.hi.1": ["washer", "Mind the basket. Those are clean, and you are not."],
  "rome.washer.hi.2": ["son", "I'm travel dirty. It's different. It's got miles on it."],
  "rome.washer.hi.3": ["washer", "A pouch on the belly and a little awning on the head. Whoever dresses you enjoys a joke."],
  "rome.washer.hi.4": ["son", "That's my mom. You'd like her. You both look at my knees the same way."],
  "rome.washer.errand.1": ["washer", "Can you run? The senator's toga is dry, and he is up at the temple steps turning purple."],
  "rome.washer.errand.2": ["washer", "I cannot leave the tubs. Take it to him, and I will lend you a proper tunic for the day."],
  "rome.washer.errand.3": ["son", "Deal. Operation Bedsheet Delivery. I'll carry it by the corners."],
  "rome.washer.ask.white": ["son", "How do you get them so white?"],
  "rome.washer.ans.white.1": ["washer", "We tread them in the tubs with stale urine. Then rinse them. Then the sun does the rest."],
  "rome.washer.ans.white.2": ["son", "Urine. Like... PEE?"],
  "rome.washer.ans.white.3": ["washer", "Is there another kind?"],
  "rome.washer.ans.white.4": ["son", "You wash clothes in PEE. That's the best fact I've ever heard. Ten out of ten. ELEVEN."],
  "rome.washer.ans.white.5": ["son", "My sister's going to be so mad I knew it first."],
  "rome.washer.ans.white.6": ["son", "...Wait. This bedsheet I'm holding..."],
  "rome.washer.ans.white.7": ["washer", "Was rinsed. Twice."],
  "rome.washer.ans.white.8": ["son", "I'm going back to the corners."],
  "rome.washer.ask.tunic": ["son", "About that tunic..."],
  "rome.washer.ans.tunic": ["washer", "Toga first, then tunic. I have run a laundry for twenty years on 'first' and 'then'."],
  "rome.washer.ask.dad": ["son", "Have you seen my dad? Tall, little beard, flowers on his shirt?"],
  "rome.washer.ans.dad.1": ["washer", "Flowers. On a shirt. No. I would remember WASHING that."],
  "rome.washer.ans.dad.2": ["son", "That's what Mom says. Same face and everything."],
  "rome.washer.ask.bye": ["son", "Bye! I'll be careful with your bedsheets."],
  "rome.washer.ans.bye": ["washer", "Togas. Go on with you."],
  "rome.washer.tunic.1": ["son", "One bedsheet, delivered! He said Rome thanks you. He was too late to say it himself."],
  "rome.washer.tunic.2": ["washer", "That sounds like him. Here. My sister's boy has outgrown it. Bring it back clean."],
  "rome.washer.tunic.3": ["son", "A real Roman tunic. It's a dress with a belt. Nobody tell my school."],
  "rome.washer.toga": ["washer", "Not to ME. To HIM. Up the street, at the temple steps, the color of a plum."],
  "rome.washer.coin": ["washer", "That has been in the fountain. I wash cloth, child, not wishes."],
  "rome.washer.breakfast": ["washer", "Keep that away from the whites. One drip of sausage and I start the whole day again."],
  "rome.washer.tunic.back": ["washer", "Keep it till sundown. And keep it out of the sauce."],

  "rome.laundry.look": ["son", "Bedsheets all the way across the street. Either it's laundry or the sleepover put up decorations."],
  "rome.laundry.look2": ["son", "That big white one glows in the sun. So that's what a clean bedsheet looks like. I'd forgotten."],
  "rome.tunic.look": ["son", "A tunic my size, on the low line. It's a long T-shirt that gave up on sleeves."],
  "rome.tunic.hands": ["washer", "Hands off the line, child. Those are counted."],
  "rome.basket.look": ["son", "A basket of wet laundry. It's heavier than me. I can tell. It has that look."],
  "rome.basket.look2": ["son", "Now that I know what it was washed in, I'm going to admire it from over here."],
  "rome.basket.use.1": ["washer", "Not the basket, child."],
  "rome.basket.use.2": ["son", "I wasn't going to. ...I was a little going to."],

  // ---------- the fountain ----------
  "rome.fountain.look": ["son", "There's money at the bottom. People throw coins in the water here. On PURPOSE. I love this place."],   // kept
  "rome.fountain.take": ["son", "Operation Borrow-A-Wish is GO. Splish."],                                                           // kept
  "rome.fountain.again": ["son", "One wish is borrowing. Two is a crime spree."],                                                     // kept
  "rome.fountain.shiny": ["son", "Brand new, and SO shiny. I can see my face in it, next to the serious man. He's not happy about it."],
  "rome.fountain.wish.1": ["urchin", "That's somebody's wish, you know."],
  "rome.fountain.wish.2": ["son", "I'm only borrowing it. I'll pay it back with interest. Interest is extra wishes."],
  // woven: his first hard look at it. Matthew 22:17-21 in his own words (the verse itself is Mom's, in Act Four).
  "rome.fountain.caesar.1": ["son", "It says CAESAR on it. So that's the nose the snack guy yells about. It's the Caesar coin!"],
  "rome.fountain.caesar.2": ["son", "Like in the story! They ask Jesus about taxes, and He says, show me a coin. Whose picture is on it?"],
  "rome.fountain.caesar.3": ["son", "Caesar's. So Caesar gets his coin. And God gets what's God's. Which is everything. Me included."],
  "rome.fountain.caesar.4": ["son", "But Jesus is all grown up in that story. So this isn't that Caesar. Not yet."],
  "rome.fountain.toga": ["son", "Dunk a clean bedsheet in a fountain? The laundry lady has ARMS. I've seen them."],
  "rome.fountain.quarter": ["son", "Pay it back with a quarter? Somebody digs that up in two thousand years and has SO many questions."],
  "rome.fountain.phone": ["son", "It's already dead. It doesn't need to be drowned too."],
  "rome.fountain.coin": ["son", "Throw it back? I haven't even used the wish yet. I'm saving it for something big. Or small."],

  // ---------- the street boy ----------
  "rome.urchin.look": ["son", "A kid! My size! Playing marbles with walnuts. Finally, somebody who isn't a grown-up in a bedsheet."],
  "rome.urchin.look2": ["son", "He keeps looking at my shoes. They're good shoes. He's got good taste. He's got no shoes."],
  "rome.urchin.hi.1": ["urchin", "Your feet are on fire."],
  "rome.urchin.hi.2": ["son", "They light up when I stomp. Watch."],
  "rome.urchin.hi.3": ["urchin", "...Do it again."],
  "rome.urchin.hi.4": ["son", "Everybody says that. Except teachers."],
  "rome.urchin.hi.5": ["urchin", "I'm the best at nuts on this street. You're the best at feet. We should be friends."],
  "rome.urchin.hi.6": ["son", "Deal. I'm calling you Walnut."],
  "rome.urchin.ask.game": ["son", "How do you play the walnut game?"],
  "rome.urchin.ans.game.1": ["urchin", "You build a little castle of nuts. Then you throw one. Knock it down and they're yours."],
  "rome.urchin.ans.game.2": ["son", "Like bowling, except you keep the pins. And then you EAT the pins. Best sport ever."],
  "rome.urchin.ans.game.3": ["son", "...I missed the castle and hit a pigeon."],
  "rome.urchin.ans.game.4": ["urchin", "The pigeon's fine. That's two nuts you owe me."],
  "rome.urchin.ans.game.5": ["son", "One hour in Rome and I'm already in nut debt."],
  "rome.urchin.ask.temple": ["son", "Have you ever been inside the temple?"],
  "rome.urchin.ans.temple.1": ["urchin", "Me? You need a clean tunic and a father who knows somebody. I've got a tunic."],
  "rome.urchin.ans.temple.2": ["son", "I've got a father. I just don't know where. It's a long story. There's a tunnel in it."],
  "rome.urchin.ans.temple.3": ["urchin", "You lost your father? ...You can share the sausage man. Everybody does."],
  "rome.urchin.ask.help": ["son", "I'm stuck, Walnut. What would you do?"],
  "rome.urchin.ask.light": ["son", "Walnut. How do you get light onto a wall that's in the dark?"],
  "rome.urchin.ask.tiny": ["son", "There's a door in there the size of a coin. What do you DO with a door that small?"],
  "rome.urchin.tip.rule": ["urchin", "Aren't you the boy old Doorpost carried out? Ask him what he DOES let in. He loves a rule."],
  "rome.urchin.tip.toga": ["urchin", "A clean tunic? The laundry woman has a hundred. And never anybody to run things up the street."],
  "rome.urchin.tip.deliver": ["urchin", "That's the senator's toga. He's the big angry one at the foot of the temple steps. Run."],
  "rome.urchin.tip.tunic": ["urchin", "You did her job. So go and get your tunic. She keeps her word. She keeps everything."],
  "rome.urchin.tip.breakfast.1": ["urchin", "Something for the god? Old Gloom on the steps has incense. But hungry, he's no use to anybody."],
  "rome.urchin.tip.breakfast.2": ["urchin", "The sausage man sends his breakfast up every morning. Today it's still on the counter."],
  "rome.urchin.tip.incense": ["urchin", "That's old Gloom's breakfast going cold in your bag. He's the one with the chickens."],
  "rome.urchin.tip.inside": ["urchin", "Tunic. Incense. So GO. Before Doorpost thinks of a fourth rule."],
  "rome.urchin.tip.shiny.1": ["urchin", "Easy. Something shiny, in the sun. I do it to the sausage man with a pot lid. He hates it."],
  "rome.urchin.tip.shiny.2": ["urchin", "Shiniest things on this street are the new silver ones in the fountain. They flash like fish."],
  "rome.urchin.tip.spark": ["urchin", "You've got something shiny. Go and find where the sun comes in. I can't do EVERYTHING for you."],
  "rome.urchin.tip.toss": ["urchin", "A door the size of a coin? Then put a coin through it. What else fits?"],
  "rome.urchin.ask.bye": ["son", "See you, Walnut."],
  "rome.urchin.ans.bye": ["urchin", "Stomp when you go. So I can watch."],
  "rome.urchin.gum.1": ["son", "Want some gum? You chew it. You don't swallow it."],
  "rome.urchin.gum.2": ["urchin", "Then what's it for?"],
  "rome.urchin.gum.3": ["son", "...Nobody knows. It's minty, though."],
  "rome.urchin.gum.4": ["urchin", "It's fighting back. I LIKE it."],
  "rome.urchin.coin.1": ["urchin", "That's fountain silver. It's still wet."],
  "rome.urchin.coin.2": ["son", "It's a borrowed wish."],
  "rome.urchin.coin.3": ["urchin", "I've lived on this street my whole life and never once thought of BORROWING one."],
  "rome.urchin.phone.1": ["urchin", "A black tile."],
  "rome.urchin.phone.2": ["son", "It takes pictures. When it's alive."],
  "rome.urchin.phone.3": ["urchin", "Pictures of what?"],
  "rome.urchin.phone.4": ["son", "Mostly a donkey."],
  "rome.urchin.quarter.1": ["urchin", "There's a bird on the back. Is it worth a walnut?"],
  "rome.urchin.quarter.2": ["son", "It's worth twenty-five... honestly? Here? About a walnut."],
  "rome.urchin.toga": ["urchin", "A senator's toga! Don't let it touch the ground. Don't let it touch ME. I'm mostly ground."],
  "rome.urchin.breakfast": ["urchin", "That's old Gloom's. I can smell it from here. I'm being very brave about it."],

  // ---------- the date seller (woven: all of him) ----------
  // A Jew from Judea, about fifty, selling dates from Jericho on the right-hand pavement. Courteous, humorous,
  // unhurried, nobody's fool. He is part of no puzzle and gives nothing that is carried. He says nothing about
  // the Romans' gods, and nobody tells him anything about the future: the Son, for once, holds his tongue.
  "rome.dateseller.look": ["son", "A man with a beard and a basket of... giant raisins? He's the only one in Rome who isn't in a hurry."],
  "rome.dateseller.look2": ["son", "He keeps looking the same way, past the fountain and a long way off. Like he's waiting for somebody."],
  "rome.dateseller.hi.1": ["dateseller", "Dates, young sir. From Jericho, in Judea. There are none better: I have looked."],
  "rome.dateseller.hi.2": ["son", "Jericho? The Jericho with the WALLS?"],
  "rome.dateseller.hi.3": ["dateseller", "You know of the walls. In that hat. ...The same Jericho. The palms have done better than the walls."],
  "rome.dateseller.ask.try": ["son", "Can I try one? I'm between snacks."],
  "rome.dateseller.ans.try.1": ["dateseller", "For a boy who knows of Jericho, the first is a gift. Here."],
  "rome.dateseller.ans.try.2": ["son", "It's candy. It's candy that GROWS. Nine out of... OW. There's a rock in it!"],
  "rome.dateseller.ans.try.3": ["dateseller", "The stone. That part is a palm tree that has not begun. I ought to charge you for the tree."],
  "rome.dateseller.ans.try.4": ["son", "Nine out of ten. One off for the surprise rock."],
  "rome.dateseller.ask.god": ["son", "Everybody here has a statue to pray to. Which one's yours?"],
  "rome.dateseller.ans.god.1": ["dateseller", "None. We have one God: the God of Abraham, of Isaac and of Jacob. He made heaven and earth."],
  "rome.dateseller.ans.god.2": ["son", "Abraham, Isaac and Jacob? I KNOW them! That's who we pray to at my house!"],
  "rome.dateseller.ans.god.3": ["dateseller", "At your house. ...Then the world is larger than Rome has told me."],
  "rome.dateseller.ans.god.4": ["dateseller", "Rome finds us Jews very funny: a great Temple in Jerusalem, and no statue in it."],
  "rome.dateseller.ans.god.5": ["dateseller", "Pompey himself went in, nineteen years ago. He found no image. Not one."],
  "rome.dateseller.ans.god.6": ["dateseller", "I ask them how they would carve the One who made the stone. They buy their dates and go."],
  "rome.dateseller.ask.pray": ["son", "What do you pray for?"],
  "rome.dateseller.ans.pray.1": ["dateseller", "For the one who is promised. Every day, facing Jerusalem. The prophet Micah has told us his town:"],
  "rome.dateseller.ans.pray.2": ["dateseller", "'But thou, Bethlehem Ephratah, though thou be little among the thousands of Judah,'"],          // Micah 5:2, King James Version, the first clause: exact, comma and all
  "rome.dateseller.ans.pray.3": ["son", "Micah 5:2! That was my line in the Christmas program. ...Bethlehem. I know SO much about Bethlehem."],
  "rome.dateseller.ans.pray.4": ["son", "I've never wanted to tell anybody anything so much. It's not mine to tell. That news has its own angels."],
  "rome.dateseller.ans.pray.5": ["son", "Mister? It's going to be worth the wait. If I were you, I'd keep watching that town."],
  "rome.dateseller.ans.pray.6": ["dateseller", "...That was not a guess. I will not ask you what it was. But I will watch."],
  // (The id of the blessing is chosen with care: the engine picks each line's gesture from its id, and this one
  // gives him a hand laid on his chest. Renumber it and he may bless the boy with a shrug, or with a date in his hand.)
  "rome.dateseller.bless.1": ["dateseller", "And for you, young sir: 'The LORD bless thee, and keep thee:'"],                                   // Numbers 6:24, King James Version: exact, colon and all
  "rome.dateseller.bless.2": ["son", "Numbers 6:24! Pastor says that at the end of church. The very same words. ...Thanks, mister."],
  "rome.dateseller.ask.bye": ["son", "Bye, mister."],
  "rome.dateseller.ans.bye": ["dateseller", "Go well, young sir. Come any day but the seventh. That day I rest, and Rome always wants dates."],
  "rome.dateseller.quarter.1": ["dateseller", "A bird. An eagle? Whoever struck this was proud of his bird. ...It is not silver, young sir."],
  "rome.dateseller.quarter.2": ["dateseller", "A coin should go home. Every year we send our offering to the Temple in Jerusalem: the half-shekel."],
  "rome.dateseller.phone": ["dateseller", "A black stone, polished like a mirror. It shows me an old man selling dates. It is not wrong."],
  "rome.dateseller.toga": ["dateseller", "A senator's toga. I know the man. He buys the best dates in Rome and remembers them as cheaper."],
  "rome.dateseller.coin.1": ["dateseller", "Caesar. He has been a friend to us Jews of Rome: we may meet, and keep our fathers' customs."],
  "rome.dateseller.coin.2": ["dateseller", "But that is fountain silver, young sir. Somebody's wish. Not a price."],
  // chickens: the soothsayer's breakfast, shown to him. He will not have his fortune told by hens, thank you. (A small shrug.)
  "rome.dateseller.breakfast": ["dateseller", "The soothsayer's. Every day he offers to tell my fortune by his hens. Every day: not by hens, thank you."],

  // ---------- the rest of the street ----------
  "rome.stones.look": ["son", "Big stones to hop across the street, so your feet stay out of the... street. Good thinking, Rome."],
  "rome.stones.look2": ["son", "Paul walks into Rome on a road like this. The Appian Way: it's on my Bible map. The church comes out to meet him. Not yet."],   // woven: Acts 28:15
  "rome.cat.look": ["son", "A cat on a sill, ignoring a whole city. Cats were already like this. That's kind of comforting."],
  "rome.cat.use": ["son", "Here, kitty. ...Ignored. In a whole other century. Consistent. Ten out of ten."],
  "rome.shrine.look": ["son", "A tiny house in the wall, for a painted snake. With a night-light. He has a nicer room than me."],
  "rome.notices.look": ["son", "Red writing on the wall. MARCVS. They spelled Marcus with a V. Nobody tell Marcus."],
  "rome.notices.look2": ["son", "VOTA. If that means vote, somebody's running for something. If it doesn't, I've got nothing."],
  "rome.rufus.look": ["son", "RVFVS. Either that's Rufus, or it's the noise a dog makes when it's being fancy."],
  "rome.flats.look": ["son", "Four floors of balconies and no elevator. I can tell. Everyone up there has shopping-bag face."],
  "rome.jars.look": ["son", "Jars with pointy bottoms. They can't stand up on their own. Same, before breakfast."],
  "rome.wheel.look": ["son", "A wooden wheel as tall as me. No tire. Whoever rides that cart feels every single rock."],
  "rome.sign.look": ["son", "A sign with a jug and grapes on it. Pictures! Finally. Somebody in Rome gets it."],
  "rome.songbird.look": ["son", "A bird in a basket cage, singing its head off. The cat over there is a big fan. A BIG fan."],

  // ================= rome-temple: inside the temple, the treasury =================

  "rome.inside.1": ["clerk", "...four hundred and eleven, four hundred and twelve..."],
  "rome.inside.2": ["son", "Tunic: OFF. It itches like a sweater made of hay. Two out of ten. Romans are tough."],
  "rome.inside.3": ["son", "It's doing the hum again. Hi, door."],
  "rome.inside.4": ["son", "You're shut. AND invisible. But I can hear you. You're terrible at hide-and-seek."],
  "rome.inside.5": ["clerk", "...four hundred and... who is talking? No. Do not tell me. ...One. Two."],
  "rome.out.look": ["son", "The way out. Past the door guy. He likes me now. He hides it really well."],

  // ---------- the place that hums, and the sunlight ----------
  "rome.hole.look": ["son", "It hums. Dad says it's the wind. Dad says EVERYTHING is the wind. I have a list."],                   // kept
  "rome.hum.try.1": ["son", "In the big pointy place I shined my flashlight at the hum, and POP: door."],
  "rome.hum.try.2": ["son", "My flashlight got left behind. Fine. Phone light!"],
  "rome.hum.try.3": ["son", "Zero percent. It can't even be sad about it."],
  "rome.hum.try.4": ["son", "So the door likes light, and I'm all out. I need the kind you don't have to charge."],
  "rome.hum.again": ["son", "Still humming. Still shut. It wants light, and all the light in here is lying on the floor."],
  "rome.hum.coin": ["son", "Nothing. It's dark over here. A coin's only shiny where there's sun to be shiny WITH."],
  "rome.hum.gum": ["son", "I'm not sticking gum on a time door. I've seen what gum does to a desk."],
  "rome.hum.incense": ["son", "The holy smell is for the statue. The door likes light, not smells. I think. I'm new at doors."],
  "rome.sun.look": ["son", "A big patch of sunshine on the floor, from the doors. Free light. Just lying there, not being used."],
  "rome.sun.look2": ["son", "The sun's HERE. The hum's over THERE. Somebody needs to introduce them. Somebody shiny."],
  "rome.sun.use.1": ["son", "Warm. With something shiny I could bounce this anywhere. I do it with a spoon at breakfast."],
  "rome.sun.use.2": ["son", "Mom has asked me to stop. Twice a week."],
  "rome.sun.done": ["son", "The little door's open. I don't need to zap the counting guy twice."],
  "rome.sun.phone": ["son", "The screen's cracked. I get a hundred tiny lights going a hundred ways. Pretty. Useless."],
  "rome.sun.gum": ["son", "Paper wrappers. No foil. Whoever made this gum did not plan for time travel."],
  "rome.sun.quarter": ["son", "This quarter's been through the wash and two vending machines. No shine left. I need a NEW coin."],

  // the spark: a spot of sunlight off the coin, and a door the size of the coin
  "rome.spark.1": ["son", "Operation Tiny Sun. Sun, meet coin. Coin, meet wall."],
  "rome.spark.2": ["clerk", "...five hundred and six, five hundred and sev... AGH. My eye."],
  "rome.spark.3": ["son", "Sorry! Wrong wall!"],
  "rome.spark.4": ["clerk", "What was that light?"],
  "rome.spark.5": ["son", "The sun. It does that sometimes. It's a known sun thing."],
  "rome.spark.6": ["clerk", "...One. Two. Three."],
  "rome.spark.7": ["son", "Okay. Slowly. Tip... tip... a little left..."],
  "rome.spark.8": ["son", "POP! A door! A tiny one. It's exactly the size of the coin."],
  "rome.spark.9": ["son", "Little light, little door. That's only fair."],
  "rome.spark.10": ["son", "I can see through it! There's sky in there. Blue. Really far down. ...Why is the sky DOWN?"],

  // the door, once it is open, and the toss that ends the act
  "rome.door.look": ["son", "A door the size of a coin, with sky in it. My eye fits. The rest of me has to wait."],
  "rome.hole.use": ["son", "I'm not jumping in there again without a snack. That's a rule I made up just now and I stand by it."],   // kept
  "rome.hole.use2": ["son", "Also I'm bigger than a coin. That's the other rule. Physics made that one up."],
  "rome.hole.quarter": ["son", "Not the quarter. George is the only other American in Rome. We stick together."],
  "rome.hole.phone": ["son", "It won't fit. Also it's dead. A dead phone is not the message I want to send Dad."],
  "rome.hole.coin": ["son", "Heads, I find Dad. Tails, Dad finds me. Edge, we get a dog."],                                       // kept
  "rome.hole.coin2": ["son", "... It didn't come back down. Does that count as edge? Do we get the dog?"],                        // kept

  // ---------- the god, the treasure, the clerk ----------
  "rome.statue.look": ["son", "A giant grandpa statue with a blanket on his head and a hook knife. And yarn tied around his feet."],
  "rome.statue.look2": ["son", "Somebody tied his feet together. Either he's dangerous or he sleepwalks. Good thinking either way."],
  "rome.statue.use": ["son", "I'm not untying a god's feet. I can't even do my own laces without the bunny ears."],
  "rome.statue.incense.1": ["son", "Hi. This is from the chicken man outside. He says sorry about the steps. And beware of today."],
  "rome.statue.incense.2": ["clerk", "...sixty-one, sixty-two... IN the bowl, boy, not beside it. ...One."],
  "rome.statue.incense.3": ["son", "He didn't say thanks. Statues never do. One out of ten for manners. Nine for the beard."],
  "rome.statue.coin": ["son", "He's guarding a whole building of money. He doesn't need my wish. He needs his feet back."],
  "rome.statue.gum": ["son", "No gum for the statue. His feet are tied. He'd never get it off his shoe."],
  "rome.bowl.look": ["son", "A little table with a bowl, at the statue's feet. His snack bowl. It's empty. I know that feeling."],
  "rome.bowl.done": ["son", "The holy smell is in the snack bowl. Delivered. That's three for three, counting the sausage."],

  "rome.chests.look": ["son", "Treasure chests! Real locks! Down both walls. This is the best room I've ever been thrown out of."],
  "rome.chests.look2": ["son", "Sacks with seals. Chests with iron. Somebody here REALLY doesn't want to share."],
  "rome.chests.use.1": ["clerk", "Do not touch the Roman People's money."],
  "rome.chests.use.2": ["son", "I was only looking. With my hands."],
  "rome.chests.use.3": ["clerk", "...One."],
  "rome.bankcat.look": ["son", "A cat! Asleep on the treasure. SHE got in without a tunic. Nobody scores cats."],
  "rome.bankcat.use.1": ["son", "Hi, cat. ...She's purring. That's two things in here that hum."],
  "rome.bankcat.use.2": ["clerk", "...ninety, ninety-one... leave her. She is the one thing in this room I do not have to count."],
  "rome.bankcat.coin": ["son", "She's asleep on a whole chest of these. One more won't impress her."],
  "rome.table.look": ["son", "A scale, a lamp, wax pads for writing, and a mountain of silver. It's homework, but shiny."],
  "rome.table.use.1": ["clerk", "Away from the table. I have piles. The piles have an order."],
  "rome.table.use.2": ["son", "They look like piles."],
  "rome.table.use.3": ["clerk", "That is how I know you are not a clerk."],

  "rome.clerk.look": ["son", "He's counting a mountain of coins, one at a time. Like Dad doing taxes, if taxes never ended."],
  "rome.clerk.look2": ["son", "When I breathe loudly, he flinches. I'm trying to breathe quietly. ...He flinched. I'm bad at it."],
  "rome.clerk.hi.1": ["clerk", "...seven hundred and eight, seven hundred and nine..."],
  "rome.clerk.hi.2": ["son", "Hi!"],
  "rome.clerk.hi.3": ["clerk", "...seven hundred and... no. It is gone. It has gone."],
  "rome.clerk.hi.4": ["clerk", "You are the incense boy. The bowl is at the god's feet. I am at one. I am at one again."],
  "rome.clerk.again": ["clerk", "...two hundred and thirty... you. Of course. ...One."],
  "rome.clerk.ask.count": ["son", "What are you counting?"],
  "rome.clerk.ans.count.1": ["clerk", "The silver of the Roman People. Every denarius. Twice, so that the two counts agree."],
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
  "rome.clerk.ans.judea.1": ["clerk", "Accounts. Judea's: Antipater's, and his son Herod's, from Galilee, where the young man governs."],
  "rome.clerk.ans.judea.2": ["son", "Herod? KING Herod? The bad king in the Christmas story?"],
  "rome.clerk.ans.judea.3": ["clerk", "Herod is no king. He is a procurator's son with expensive tastes. I have the figures."],
  "rome.clerk.ans.judea.4": ["son", "...I'd count him twice. I'm just saying."],
  "rome.clerk.ask.dad": ["son", "Have you seen my dad?"],
  "rome.clerk.ans.dad.1": ["clerk", "Is he made of silver?"],
  "rome.clerk.ans.dad.2": ["son", "No."],
  "rome.clerk.ans.dad.3": ["clerk", "Then I have not counted him."],
  "rome.clerk.ask.bye": ["son", "I'll let you count."],
  "rome.clerk.ans.bye": ["clerk", "Everyone says that. ...One."],
  "rome.clerk.coin.1": ["clerk", "Is that one of mine?"],
  "rome.clerk.coin.2": ["son", "No! It's a wish."],
  "rome.clerk.coin.3": ["clerk", "Good. Wishes belong to the god. If I had to count those as well, I would lie down on the floor."],
  "rome.clerk.quarter": ["clerk", "It is not silver, it is not Roman, and I refuse to count it. Keep it away from the piles."],
  "rome.clerk.phone.1": ["clerk", "A writing tablet with no wax. What do you scratch on?"],
  "rome.clerk.phone.2": ["son", "You don't scratch it. You poke it. When it's alive."],
  "rome.clerk.phone.3": ["clerk", "...I was happier not knowing that."],
  "rome.clerk.incense": ["clerk", "For the god. Not for me. The bowl. Quietly."],

  "rome.brazier.look": ["son", "Hot coals in a bronze thing with feet. An indoor campfire. Nobody brought marshmallows. I checked."],
  "rome.brazier.use": ["son", "Hot. HOT. That is a looking-only campfire."],
  "rome.tablets.look": ["son", "Metal pages nailed to the wall. Tiny letters. ALL the rules. No pictures. Zero out of ten."],
  "rome.standards.look": ["son", "Poles with shiny badges on top. Parade stuff. They keep the parade in the bank."],
  "rome.rack.look": ["son", "Cubbies! Like at school, but with scrolls instead of lunches. Worst cubbies ever. Three out of ten."],

  // ================= carried things =================
  "item.toga.look": ["son", "The senator's bedsheet, folded like a flag. It weighs more than my backpack and does a lot less."],
  "item.tunic.look": ["son", "A tunic my size. I have to bring it back clean. The laundry lady has not seen how I eat."],
  "item.breakfast.look": ["son", "Bread and a sausage in a cloth. I'm not going to eat it. I'm going to smell it. Smelling is free."],
  "item.incense.look": ["son", "A little wooden box of holy smell. It rattles. I've decided not to open it. That's called growth."],
  "item.coin.look": ["son", "A coin with a serious man on it. He looks like he has never had a snack in his life."],              // kept
  "item.coin.mom": ["mom", "A silver coin with a stern gentleman on it. It looks old and it looks new. Your sister will know which."],     // kept (Act Four)
  "item.coin.bigsis": ["bigsis", "A denarius of Julius Caesar, struck in 44 B.C. and not a day older. I am not letting go of it."],        // kept (Act Four)
  "item.coin.lilsis": ["lilsis", "A money, with a grumpy man on it. He needs a snack."],                                                   // kept (Act Four)
  // his own things: looked at, tried on people, never the answer to anything
  "item.phone.look": ["son", "It died doing what it loved: taking four hundred pictures of a donkey."],
  "item.quarter.look": ["son", "My emergency quarter. Dad says it's for a pay phone. I've never seen a pay phone. I've seen ROME."],
  "item.gum.look": ["son", "Half a pack of gum. The other half is under the car seat. That's a problem for later. Or earlier."],

  // ================= hints: one for each puzzle, in his own voice =================
  "hint.rome.toga": ["son", "The door guy wants a kid in a clean tunic. The laundry lady on the street has a whole line of them."],
  "hint.rome.delivered": ["son", "I'm carrying a senator's bedsheet. He's the one standing still in a hurry, by the temple steps."],
  "hint.rome.tunic": ["son", "Bedsheet delivered. The laundry lady owes me one tunic. Time to collect."],
  "hint.rome.breakfast": ["son", "Something for the god: the chicken man has incense. And no breakfast. The snack bar has breakfast."],
  "hint.rome.incense": ["son", "The chicken man's breakfast is in my backpack. It's getting cold. So is he."],
  "hint.rome.coin": ["son", "That fountain is full of other people's wishes. I only need to borrow one."],                         // kept
  "hint.rome.inside": ["son", "Clean tunic: got it. Something for the god: got it. Time to show the door guy my score."],
  "hint.rome.spark": ["son", "The door likes light. There's sun on the temple floor and a shiny coin in my backpack. Bounce it!"],
  "hint.rome.toss": ["son", "The humming door ate me. Maybe it eats money too. For science."],                                    // kept
};
