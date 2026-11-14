// Act Five opens: Everybody's Grandpa. The inside of a gray limousine, driving. (NEVADA-12W: new in round twelve:
// briefs/NEVADA-12.md, briefs/WRITE-12.md, and briefs/out/nevada-expansion-design.md, "Act Five opens".)
//   "line.id": ["who", "What they say."]
//
// The first part of the game played by somebody who is not family, and the first part played by a raccoon. GRANDPA JOE
// ("grandpajoe") can talk to anybody and has his hands tied; RANGER ("ranger") cannot talk and has paws. Ranger's lines
// are always dots ("...", and "...!" when he is furious with a rope), and Grandpa Joe says what he means: a look of
// Ranger's at a thing is limo.<thing>.ranger, and Grandpa Joe's translation of it is limo.<thing>.ranger.joe.
//
// The men in gray (the backup: "suit1" to "suit4"; Jed is "agent", in the front) say sir to everybody, apologize while
// they do things, and follow regulations to the letter, which is their whole weakness. They are never frightening.
// Their office is the Office Of Peculiar Sectors, and they pronounce every letter of it.
//
// PASS-17N (round seventeen, the dialogue pass): a little more of Ranger (limo.juice.ranger.joe, and a new word between
// the two of them once Grandpa Joe is loose, limo.talk.ranger.joe.3c, in nevada-limo.js's talk). Every id is kept.
//
// Grandpa Joe's tune is his own, the Last Stop Rag. He hums it (limo.sing.1 to .3): no words, and no real song is sung,
// named or quoted. The third sector on the clipboard is under Jed's thumb, and nobody names it (decision 2).

export const lines = {
  // ---------- Cut-scene: Meanwhile, in a limousine (it opens the act) ----------
  // the long seat; Grandpa Joe in the ropes, and a seatbelt goes on over them
  "limo.open.1": ["suit1", "Seatbelt, sir. Regulations."],
  // the divider slides down: two pairs of dark shades in the mirror
  "limo.open.2": ["suit2", "Sir, you are being transported for questioning."],
  "limo.open.3": ["grandpajoe", "Been questioned once this mornin', son. By a seven-year-old."],
  "limo.open.4": ["suit2", "Noted."],
  // the divider slides up; Ranger comes up from under the facing seat with the mirror shades on, and Grandpa Joe laughs
  "limo.open.5": ["grandpajoe", "A stowaway. I might've known."],
  "limo.open.6": ["grandpajoe", "See to these ropes, partner. But only when nobody's lookin'."],
  // LETTER-17: then, quietly, with the divider up and the suits out of hearing (Ranger's "..." between): the promise he made
  // Mom at the wide door (nevada.through.joe.6: "Porch light on. However long it takes.")
  "limo.promise": ["grandpajoe", "I made that lady a promise, partner."],
  "limo.promise.joe": ["grandpajoe", "I know. Then we'd best get loose."],
  // Ranger's line in this act, wherever he answers and Grandpa Joe says what he means
  "limo.ranger.dots": ["ranger", "..."],

  // ---------- #14: Ranger's Ropes (the long seat). Divider down: a raccoon doing nothing. Divider up: furious. ----------
  // Ranger nibbles while the divider is down (nothing is lost; the suit is watching)
  "limo.ropes.chewing": ["suit1", "Sir, is the raccoon... chewing?"],
  "limo.ropes.grooming": ["grandpajoe", "He's groomin' me, son. It's affection."],
  // Grandpa Joe at the ropes
  "limo.ropes.joe": ["narrator", "Grandpa Joe would need his hands for that, and at present both of them are busy being tied."],
  // talk does not put the divider up
  "limo.ropes.visual": ["suit2", "Sir, we are required to maintain visual."],
  // singing does: the lever (in dividerTree, js/content/talk/nevada.js)
  "limo.ropes.music": ["grandpajoe", "You boys like music?"],
  "limo.ropes.required": ["suit1", "Sir, we are required to--"],
  "limo.ropes.required.2": ["suit2", "Sir. Not again."],
  "limo.ropes.required.3": ["suit1", "We are asking you very nicely, sir."],
  // the Last Stop Rag, his own tune, hummed: loudly, badly, and the game's own notes under it
  "limo.sing.1": ["grandpajoe", "Hmm-hm-hmm, hm-hm-hmm... hm-hm-hmmm..."],
  "limo.sing.2": ["grandpajoe", "Hmm-hm-hmm-hm-hmmm... Hm. Hm. Hmmmmm..."],
  "limo.sing.3": ["grandpajoe", "Hmm-hm-hm-hmmmmm... Here comes the good part, boys!"],
  "limo.ropes.stop": ["suit2", "Sir, please stop singing."],
  "limo.ropes.medical": ["grandpajoe", "Can't, son. It's a medical condition."],
  "limo.ropes.stop.2": ["suit2", "Sir. Please."],
  "limo.ropes.medical.2": ["grandpajoe", "Still a medical condition, son. Flares up in limousines."],
  // between strands the divider comes down once more, and Ranger sits on his work
  "limo.ropes.groomin": ["grandpajoe", "Groomin'."],
  // each nibble is a click; four strands, and the bow comes undone last
  "limo.ropes.nibble": ["ranger", "...!"],
  "limo.ropes.strand.1": ["grandpajoe", "That's one. Keep goin', partner."],
  "limo.ropes.strand.2": ["grandpajoe", "Two. You're a credit to your mask."],
  "limo.ropes.strand.3": ["grandpajoe", "Three. Easy now, there's one to go."],
  "limo.ropes.strand.4": ["grandpajoe", "Four. Now the bow, and gentle with it. It's a trade like any other."],
  "limo.ropes.bow": ["grandpajoe", "Well, I'll be. I'd near forgot I had hands."],
  "limo.ropes.regs": ["grandpajoe", "Regulations."],                                                                   // he keeps the seatbelt on
  // the wrong ones at the wrong things
  "limo.phone.ranger.joe": ["grandpajoe", "That ain't for you, partner. That's for later."],                                          // Ranger lifts the car phone, and it says nothing
  "limo.divider.ranger.joe": ["narrator", "Ranger considers a word with the men in front. They wouldn't understand him. They barely understand Grandpa Joe."],      // Ranger at the suits
  "hint.limo.ropes.joe": ["grandpajoe", "Those boys keep lookin' back at us. A little music at that divider might cure 'em of it."],
  "hint.limo.ropes.ranger": ["grandpajoe", "He says he'll see to the ropes himself, soon as I get those boys to quit lookin' back."],                         // Ranger's hint is "..." (limo.ranger.dots), and this

  // ---------- the suits, through the divider (dividerTree in js/content/talk/nevada.js) ----------
  "limo.divider.sir": ["suit1", "Sir?"],
  "limo.divider.opt.where": ["grandpajoe", "Where you boys takin' me, anyhow?"],
  "limo.divider.where.joe": ["grandpajoe", "You said that already. We're goin' in circles."],
  "limo.divider.opt.office": ["grandpajoe", "What outfit you boys with?"],
  "limo.divider.office.1": ["suit1", "The Office Of Peculiar Sectors, sir. O. O. P. S."],
  "limo.divider.office.2": ["grandpajoe", "Oops."],
  "limo.divider.office.3": ["suit2", "It is pronounced O. O. P. S., sir."],
  "limo.divider.office.4": ["grandpajoe", "That's what I said."],
  "limo.divider.opt.what": ["grandpajoe", "Questionin' about what, exactly?"],
  "limo.divider.what.1": ["suit2", "Sir, we are not permitted to tell you the questions."],
  "limo.divider.what.2": ["grandpajoe", "Then how am I supposed to get my answers ready?"],
  "limo.divider.opt.regs": ["grandpajoe", "You boys got a rule for everything?"],
  "limo.divider.regs.1": ["suit2", "The regulations cover every situation, sir."],
  "limo.divider.regs.2": ["grandpajoe", "Got one for a raccoon?"],
  "limo.divider.regs.3": ["suit1", "We are looking it up, sir."],
  "limo.divider.regs.4": ["suit1", "Sir, we are still looking up the raccoon."],
  "limo.divider.regs.5": ["suit2", "Sir, the raccoon is not in the index."],
  "limo.divider.opt.burger": ["grandpajoe", "Where'd Jed's cheeseburger get to?"],
  "limo.divider.burger.1": ["suit1", "Lunch rides in the back, sir. Regulations."],
  "limo.divider.burger.jed": ["agent", "I would still like the cheeseburger. For the record."],
  "limo.divider.opt.up": ["grandpajoe", "Would you boys mind puttin' that window back up? I'm shy."],
  "limo.divider.opt.bye": ["grandpajoe", "You boys carry on."],
  "limo.divider.bye": ["suit1", "Thank you, sir. Maintaining visual."],

  // ---------- #15: Jed's Lunch (the facing seat: the paper bag, the clipboard, a juice box) ----------
  "limo.lunch.bag.early": ["narrator", "Grandpa Joe can smell the cheeseburger from here, and with his hands tied that is all he can do about it."],              // Grandpa Joe at the bag, before #14
  "limo.lunch.pickle": ["grandpajoe", "Ranger. Oh, fine. He's earned the pickle."],                                           // Ranger at the bag: the pickle is gone
  "limo.lunch.clipboard.joe": ["narrator", "Ranger turns the clipboard over in his paws. To a raccoon it is only a clipboard. Reading is Grandpa Joe's job."],         // Ranger reads it with his paws
  "limo.lunch.juice": ["grandpajoe", "Apple. They're not monsters."],
  // Grandpa Joe reads the clipboard, and eats the cheeseburger while he does it
  "limo.lunch.burger": ["grandpajoe", "Jed can have the next one."],
  "limo.lunch.read.1": ["grandpajoe", "Same notice as the fence. Three sectors on the map: forty-four, nineteen twenty-one."],
  // NEVADA-12F: in the close-up the sheet is flat and the third circle is under the mustard thumbprint: nothing is folded
  "limo.lunch.read.2": ["grandpajoe", "And the third's under Jed's thumbprint, in mustard. I ain't touchin' that."],
  "limo.lunch.read.3": ["grandpajoe", "A column headed 'What opens them,' blank all the way down. And a note: 'A coin?? Ask Houston.'"],
  "limo.lunch.read.4": ["grandpajoe", "They got a map of holes, and no idea how to open one."],
  "limo.lunch.read.5": ["grandpajoe", "And those little girls worked it out with a coin and a window."],
  // he tears the map off the clipboard and folds it small, and Ranger puts it in the bib pocket for him
  "limo.lunch.trade": ["grandpajoe", "That ain't stealin', partner. That's a trade. They can have the banjo."],
  // and the divider slides down, and a hand passes back a receipt
  "limo.lunch.receipt.1": ["suit1", "Your receipt for the banjo, sir. Regulations."],
  "limo.lunch.receipt.2": ["grandpajoe", "'Received: one banjo, damaged. One raccoon, unconfirmed.'"],
  "limo.lunch.receipt.3": ["grandpajoe", "Hear that, partner? You're unconfirmed."],
  "limo.lunch.receipt.4": ["grandpajoe", "He says he ain't never been so confirmed in his life."],
  // the limousine slows: a gate, and a very small building with a very long name on it
  "limo.lunch.slowing": ["grandpajoe", "We're slowin' down. That's a long name for a little building."],
  "hint.limo.bag.joe": ["grandpajoe", "Jed's clipboard and Jed's lunch are on that seat. I can read one and eat the other, if Ranger fetches 'em."],
  "hint.limo.bag.ranger": ["grandpajoe", "He says the readin' is my business, so I'd best ask for it. He'll take the pickle."],
  // the act's card (the scene shows it as a card, not as lines; written here so that it is in one place)
  "limo.card.1": ["narrator", "THE OFFICE OF PECULIAR SECTORS"],
  "limo.card.2": ["narrator", "Desert Field Headquarters, the same afternoon"],      // SCENES-17: the arrival's card now (the demo ends at the Office's "Going Down")

  // ---------- every thing in the limousine: Grandpa Joe's look; Ranger's ("..."), and what Grandpa Joe says he means ----------
  "limo.divider.joe": ["narrator", "A smoked-glass divider, with two men in dark shades behind it. One of them is chewing something."],
  "limo.divider.ranger": ["ranger", "..."],
  // NEVADA-12F: through the divider it is the one on the right who is eating, and it is a pink doughnut (divider-down.png)
  "limo.divider.ranger.look.joe": ["narrator", "Ranger has noticed that the man on the right has a doughnut, and would like to discuss it."],
  "limo.ropes.look.joe": ["narrator", "Regulation rope around Grandpa Joe's wrists, four strands and a bow, tied very neatly. He will give them that."],
  "limo.ropes.ranger": ["ranger", "..."],
  "limo.ropes.ranger.joe": ["narrator", "Four strands and a bow. Ranger has seen tougher rope on a sack of birdseed."],
  // NEVADA-12F: once he is loose the ropes' cut-out is gone (Ranger keeps the bow): there is no heap to see
  "limo.ropes.look2.joe": ["narrator", "Where the ropes were. Four strands and a bow, and a raccoon undid every one of them."],          // once they are off
  "limo.ropes.ranger2.joe": ["narrator", "The ropes are done with. Ranger is keeping the bow, which is his now."],
  "limo.bag.joe": ["narrator", "A paper bag on the facing seat, with a cheeseburger in it and a grease spot the shape of a pickle."],
  "limo.bag.ranger": ["ranger", "..."],
  "limo.bag.ranger.joe": ["narrator", "Ranger can smell a pickle in the paper bag. As far as he is concerned, the pickle is spoken for."],
  // NEVADA-12F: no pen is painted on the clipboard; its sheet has a column of empty boxes down the side
  "limo.clipboard.joe": ["narrator", "The office's clipboard, on the facing seat: papers, and a column of empty boxes. It is probably Jed's."],
  "limo.clipboard.ranger": ["ranger", "..."],
  "limo.clipboard.ranger.joe": ["narrator", "Ranger sniffs the clipboard. It smells of mustard and worry."],
  "limo.juice.joe": ["narrator", "A juice box with the straw already in it. Apple, by the picture."],
  "limo.juice.ranger": ["ranger", "..."],
  "limo.juice.ranger.joe": ["narrator", "Ranger would trade for the juice box, if he had anything to trade. He looks away, as if he hadn't asked."],         // PASS-17N: Ranger: a beat of business in a look
  "limo.fridge.joe": ["narrator", "A little fridge under the facing seat, empty but for its light. It is like Harold the cooler, only quieter."],
  "limo.fridge.ranger": ["ranger", "..."],
  "limo.fridge.ranger.joe": ["narrator", "Ranger checks the little fridge, and then checks it again. There is nothing in it but the light."],
  "limo.phone.joe": ["narrator", "A car phone on a curly cord. Grandpa Joe has not seen one since Jolene's cousin got rich."],
  "limo.phone.ranger": ["ranger", "..."],
  "limo.phone.ranger.look.joe": ["narrator", "Ranger watches the car phone. It doesn't ring, and he would like it to."],
  "limo.ashtray.joe": ["narrator", "An ashtray full of jelly beans. Somebody at that office has his priorities in order."],
  "limo.ashtray.ranger": ["ranger", "..."],
  "limo.ashtray.ranger.joe": ["narrator", "Ranger sorts through the jelly beans in the ashtray. The black ones are his."],
  "limo.window.joe": ["narrator", "The desert, going by the window. Grandpa Joe has watched it for forty years, and never this fast."],
  "limo.window.ranger": ["ranger", "..."],
  "limo.window.ranger.joe": ["narrator", "Ranger presses his nose to the glass. He has never seen the desert from in here, and he is taking notes."],
  "limo.seat.joe": ["narrator", "A long gray seat, softer than Grandpa Joe's rocking chair. He would rather Jolene didn't hear that."],
  "limo.seat.ranger": ["ranger", "..."],
  "limo.seat.ranger.joe": ["narrator", "Ranger pats the long seat. It is a fine seat for sitting on rope, and he would know."],
  // NEVADA-12F: true whatever has been fetched off it (the juice box, drunk, is no longer on the seat)
  "limo.facingseat.joe": ["narrator", "The seat across the car holds lunch, paperwork and a beverage. That makes it an office."],
  "limo.facingseat.ranger": ["ranger", "..."],
  "limo.facingseat.ranger.joe": ["narrator", "The facing seat has everything a raccoon could want, and Ranger wants all of it."],
  "limo.belt.joe": ["narrator", "A seatbelt, buckled over the ropes. They do things properly, and Grandpa Joe will give them that too."],
  "limo.belt.ranger": ["ranger", "..."],
  "limo.belt.ranger.joe": ["narrator", "Ranger does not hold with seatbelts. He holds on with his hands."],

  // ---------- what the two of them say to each other (limo.talk.*; Ranger's part is limo.ranger.dots) ----------
  "limo.talk.joe.ranger.1a": ["grandpajoe", "You didn't have to come, partner."],
  "limo.talk.joe.ranger.1c": ["grandpajoe", "He says where I go, he goes. Even in a limousine. Especially in a limousine."],
  "limo.talk.joe.ranger.2a": ["grandpajoe", "A car full of dark shades, and yours are the only ones I can see myself in."],
  "limo.talk.joe.ranger.2c": ["grandpajoe", "He says that's because he paid for his. Well, he traded."],
  "limo.talk.joe.ranger.3a": ["grandpajoe", "I got my hands back, partner. Thank you kindly."],                                                // once the ropes are off (limo.loose)
  "limo.talk.joe.ranger.3c": ["grandpajoe", "He says don't mention it. He'll be mentionin' it himself, later."],
  "limo.talk.joe.ranger.4a": ["grandpajoe", "That map's comin' home with us. Somebody ought to know what opens those holes."],   // once the map is his (limo.map)
  "limo.talk.joe.ranger.4c": ["grandpajoe", "He says the little girls know. He's right."],
  "limo.talk.ranger.joe.1c": ["grandpajoe", "I know, partner. I miss her too. She'll be changin' her hat about now."],
  "limo.talk.ranger.joe.2c": ["grandpajoe", "Those little girls? They had their mama, and their mama had a plan."],
  "limo.talk.ranger.joe.3c": ["grandpajoe", "Yes, partner, four strands and a bow. Yes, all four. I was there."],            // PASS-17N: new: Ranger: 'He'll be mentionin' it himself, later' comes round

  // ---------- the things carried in this act (js/content/world.js, items): Grandpa Joe's and Ranger's looks, and the family's ----------
  "item.sectormap.grandpajoe": ["narrator", "The office's map: three holes in Grandpa Joe's desert, and a column for what opens them, left empty."],
  "item.sectormap.ranger": ["ranger", "..."],
  "item.sectormap.ranger.joe": ["narrator", "To Ranger the map smells of cheeseburger. That is Grandpa Joe's fault."],
  "item.sectormap.mom": ["narrator", "A map with three sectors of desert ringed in pen, and a column for what opens them. It is quite empty."],
  "item.sectormap.bigsis": ["narrator", "A map of three sectors. Big Sister knows two of them, and the third is under a thumbprint, which will not do."],
  "item.sectormap.lilsis": ["narrator", "A map with holes on it. Not real holes, Little Sister explains, but drawings of the real holes."],
  "item.receipt.grandpajoe": ["narrator", "A receipt: one banjo, damaged, and one raccoon, unconfirmed. Grandpa Joe aims to collect."],
  "item.receipt.ranger": ["ranger", "..."],
  "item.receipt.ranger.joe": ["narrator", "Ranger considers himself confirmed, and would like that written down."],
  "item.receipt.mom": ["narrator", "A receipt for a banjo, from the government. Mom does like a paper trail."],
  "item.receipt.bigsis": ["narrator", "The receipt lists one raccoon, unconfirmed. In Big Sister's view Ranger has never been more confirmed."],
  "item.receipt.lilsis": ["narrator", "A receipt for a banjo. Little Sister knows how receipts work: this is how the banjo comes back."],
  // ---- TALK-24 (10 November: dialogue trees with topics, every act): the topics a talk's questions are gathered under ----
  "limo.divider.topic.ride": ["grandpajoe", "Got some questions about this ride of ours."],
  "limo.divider.topic.outfit": ["grandpajoe", "Let's talk about you boys a spell."],
};
