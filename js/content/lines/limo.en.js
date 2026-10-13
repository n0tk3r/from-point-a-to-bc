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
// Grandpa Joe's tune is his own, the Last Stop Rag. He hums it (limo.sing.1 to .3): no words, and no real song is sung,
// named or quoted. The third sector on the clipboard is under Jed's thumb, and nobody names it (decision 2).

export const lines = {
  // ---------- Cut-scene: Meanwhile, in a limousine (it opens the act) ----------
  // the long seat; Grandpa Joe in the ropes, and a seatbelt goes on over them
  "limo.open.1": ["suit1", "Seatbelt, sir. Regulations."],
  // the divider slides down: two pairs of dark shades in the mirror
  "limo.open.2": ["suit2", "Sir, you are being transported for questioning."],
  "limo.open.3": ["grandpajoe", "Son, I been questioned by a seven-year-old this mornin'. You ain't got anything she didn't."],
  "limo.open.4": ["suit2", "...Noted."],
  // the divider slides up; Ranger comes up from under the facing seat with the mirror shades on, and Grandpa Joe laughs
  "limo.open.5": ["grandpajoe", "Well, there you are. I wondered who'd got in."],
  "limo.open.6": ["grandpajoe", "All right, Ranger. You know what to do."],
  // Ranger's line in this act, wherever he answers and Grandpa Joe says what he means
  "limo.ranger.dots": ["ranger", "..."],

  // ---------- #14: Ranger's Ropes (the long seat). Divider down: a raccoon doing nothing. Divider up: furious. ----------
  // Ranger nibbles while the divider is down (nothing is lost; the suit is watching)
  "limo.ropes.chewing": ["suit1", "Sir, is the raccoon... chewing?"],
  "limo.ropes.grooming": ["grandpajoe", "He's groomin' me, son. It's affection."],
  // Grandpa Joe at the ropes
  "limo.ropes.joe": ["grandpajoe", "I'd need hands for that, and mine are busy bein' tied."],
  // talk does not put the divider up
  "limo.ropes.visual": ["suit2", "Sir, we are required to maintain visual."],
  // singing does: the lever (in dividerTree, js/content/talk/nevada.js)
  "limo.ropes.music": ["grandpajoe", "You boys like music?"],
  "limo.ropes.required": ["suit1", "Sir, we are required to..."],
  "limo.ropes.required.2": ["suit2", "Sir, not again, sir."],
  "limo.ropes.required.3": ["suit1", "Sir, we are asking you very nicely, sir."],
  // the Last Stop Rag, his own tune, hummed: loudly, badly, and the game's own notes under it
  "limo.sing.1": ["grandpajoe", "Hmm-hm-HMM, hm-hm-hmm... HMM-hm-hm-hmmm..."],
  "limo.sing.2": ["grandpajoe", "Hm-HMM-hm-hm! Hmm-hm-hmm-HMMM! Hm. Hm. HMMMM..."],
  "limo.sing.3": ["grandpajoe", "Hmm-hm-hm-HMM-hmm-hm-hm-hmmmmm... Here comes the good part, boys! HMMM-hm!"],
  "limo.ropes.stop": ["suit2", "Sir, please stop singing."],
  "limo.ropes.medical": ["grandpajoe", "Can't, son. It's a medical condition."],
  "limo.ropes.stop.2": ["suit2", "Sir. PLEASE, sir."],
  "limo.ropes.medical.2": ["grandpajoe", "Still a medical condition, son. Flares up in limousines."],
  // between strands the divider comes down once more, and Ranger sits on his work
  "limo.ropes.groomin": ["grandpajoe", "Groomin'."],
  // each nibble is a click; four strands, and the bow comes undone last
  "limo.ropes.nibble": ["ranger", "...!"],
  "limo.ropes.strand.1": ["grandpajoe", "That's one. Keep goin', partner."],
  "limo.ropes.strand.2": ["grandpajoe", "Two. You're a credit to your mask."],
  "limo.ropes.strand.3": ["grandpajoe", "Three. Easy, now. One to go."],
  "limo.ropes.strand.4": ["grandpajoe", "Four! Now the bow. Gentle. It's a trade like any other."],
  "limo.ropes.bow": ["grandpajoe", "...Well, I'll be. Hands. I'd near forgot I had 'em."],
  "limo.ropes.regs": ["grandpajoe", "Regulations."],                                                                   // he keeps the seatbelt on
  // the wrong ones at the wrong things
  "limo.phone.ranger.joe": ["grandpajoe", "That ain't for you. That's for later."],                                          // Ranger lifts the car phone, and it says nothing
  "limo.divider.ranger.joe": ["grandpajoe", "He says they wouldn't understand him. He's right. They don't understand ME."],      // Ranger at the suits
  "hint.limo.ropes.joe": ["grandpajoe", "Them boys don't want to look at me. I just got to give 'em a reason."],
  "hint.limo.ropes.ranger": ["grandpajoe", "He says he knows exactly what to do and I'm in the way."],                         // Ranger's hint is "..." (limo.ranger.dots), and this

  // ---------- the suits, through the divider (dividerTree in js/content/talk/nevada.js) ----------
  "limo.divider.sir": ["suit1", "Sir?"],
  "limo.divider.opt.where": ["grandpajoe", "Where you boys takin' me, anyhow?"],
  "limo.divider.where.joe": ["grandpajoe", "You said that. And I said the seven-year-old. We're goin' in circles, son."],
  "limo.divider.opt.office": ["grandpajoe", "What outfit are you boys with, anyhow?"],
  "limo.divider.office.1": ["suit1", "The Office Of Peculiar Sectors, sir. O. O. P. S."],
  "limo.divider.office.2": ["grandpajoe", "Oops."],
  "limo.divider.office.3": ["suit2", "It is pronounced O. O. P. S., sir."],
  "limo.divider.office.4": ["grandpajoe", "That's what I said."],
  "limo.divider.opt.what": ["grandpajoe", "Questionin' about what, exactly?"],
  "limo.divider.what.1": ["suit2", "Sir, we are not permitted to tell you what you will be asked."],
  "limo.divider.what.2": ["grandpajoe", "Then how'm I supposed to get my answers ready?"],
  "limo.divider.opt.regs": ["grandpajoe", "You boys got a rule for everything?"],
  "limo.divider.regs.1": ["suit2", "Sir, the regulations cover every situation, sir."],
  "limo.divider.regs.2": ["grandpajoe", "Got one for a raccoon?"],
  "limo.divider.regs.3": ["suit1", "...We are looking it up, sir."],
  "limo.divider.regs.4": ["suit1", "Sir, we are still looking up the raccoon."],
  "limo.divider.regs.5": ["suit2", "Sir, the raccoon is not in the index."],
  "limo.divider.opt.burger": ["grandpajoe", "And where's Jed's cheeseburger got to?"],
  "limo.divider.burger.1": ["suit1", "Lunch rides in the back, sir. Regulations."],
  "limo.divider.burger.jed": ["agent", "...I would still like the cheeseburger. For the record."],
  "limo.divider.opt.up": ["grandpajoe", "Y'all mind puttin' that window back up? I'm shy."],
  "limo.divider.opt.bye": ["grandpajoe", "Well. Y'all carry on."],
  "limo.divider.bye": ["suit1", "Thank you, sir. Maintaining visual, sir."],

  // ---------- #15: Jed's Lunch (the facing seat: the paper bag, the clipboard, a juice box) ----------
  "limo.lunch.bag.early": ["grandpajoe", "I can smell it from here. That's the cruelest thing they've done yet."],              // Grandpa Joe at the bag, before #14
  "limo.lunch.pickle": ["grandpajoe", "Ranger. ...Well. He's earned the pickle."],                                           // Ranger at the bag: the pickle is gone
  "limo.lunch.clipboard.joe": ["grandpajoe", "He says it's a clipboard. He's right. That's all it is, to a raccoon."],         // Ranger reads it with his paws
  "limo.lunch.juice": ["grandpajoe", "Apple. They're not monsters."],
  // Grandpa Joe reads the clipboard, and eats the cheeseburger while he does it
  "limo.lunch.burger": ["grandpajoe", "Jed can have the next one."],
  "limo.lunch.read.1": ["grandpajoe", "'Area closed. Elevated radiation.' Same as the fence. And a map. Three sectors. Forty-four. Nineteen twenty-one."],
  // NEVADA-12F: in the close-up the sheet is flat and the third circle is under the mustard thumbprint: nothing is folded
  "limo.lunch.read.2": ["grandpajoe", "And a third, with Jed's thumbprint square on top of it. In mustard. I ain't touchin' that."],
  "limo.lunch.read.3": ["grandpajoe", "And a column says WHAT OPENS THEM. Blank, all the way down. And in the margin: 'A COIN?? Ask Houston.'"],
  "limo.lunch.read.4": ["grandpajoe", "They got a map of holes and no idea how to open one."],
  "limo.lunch.read.5": ["grandpajoe", "And them little girls worked it out with a coin and a window."],
  // he tears the map off the clipboard and folds it small, and Ranger puts it in the bib pocket for him
  "limo.lunch.trade": ["grandpajoe", "That ain't stealin'. That's tradin'. They can have the banjo."],
  // and the divider slides down, and a hand passes back a receipt
  "limo.lunch.receipt.1": ["suit1", "Your receipt, sir. For the banjo. Regulations."],
  "limo.lunch.receipt.2": ["grandpajoe", "'RECEIVED: one banjo (damaged). one raccoon (unconfirmed).'"],
  "limo.lunch.receipt.3": ["grandpajoe", "Hear that, partner? You're unconfirmed."],
  "limo.lunch.receipt.4": ["grandpajoe", "He says he ain't never been so confirmed in his life."],
  // the limousine slows: a gate, and a very small building with a very long name on it
  "limo.lunch.slowing": ["grandpajoe", "We're slowin' down. ...Well, would you look at that. Long name for a little building."],
  "hint.limo.bag.joe": ["grandpajoe", "That clipboard's what they know, and that bag's what Jed wanted. I can read one and eat the other."],
  "hint.limo.bag.ranger": ["grandpajoe", "He says the bag's his business and the clipboard's mine. He'll take the pickle for his trouble."],
  // the act's card (the scene shows it as a card, not as lines; written here so that it is in one place)
  "limo.card.1": ["narrator", "THE OFFICE OF PECULIAR SECTORS"],
  "limo.card.2": ["narrator", "to be continued"],

  // ---------- every thing in the limousine: Grandpa Joe's look; Ranger's ("..."), and what Grandpa Joe says he means ----------
  "limo.divider.joe": ["grandpajoe", "A smoky window to the front. Two fellas behind it in dark shades, and one of 'em's eatin' somethin'."],
  "limo.divider.ranger": ["ranger", "..."],
  // NEVADA-12F: through the divider it is the one on the right who is eating, and it is a pink doughnut (divider-down.png)
  "limo.divider.ranger.look.joe": ["grandpajoe", "He says the one on the right has a doughnut, and he'd like to discuss it."],
  "limo.ropes.look.joe": ["grandpajoe", "Regulation rope, four strands and a bow. Tied neat. I'll give 'em that."],
  "limo.ropes.ranger": ["ranger", "..."],
  "limo.ropes.ranger.joe": ["grandpajoe", "He says he's seen tougher rope on a sack of birdseed."],
  // NEVADA-12F: once he is loose the ropes' cut-out is gone (Ranger keeps the bow): there is no heap to see
  "limo.ropes.look2.joe": ["grandpajoe", "Where my ropes was. Four strands and a bow, and a raccoon done every one."],          // once they are off
  "limo.ropes.ranger2.joe": ["grandpajoe", "He says he's keepin' the bow. It's his now."],
  "limo.bag.joe": ["grandpajoe", "A paper bag with a cheeseburger in it, and a grease spot the shape of a pickle."],
  "limo.bag.ranger": ["ranger", "..."],
  "limo.bag.ranger.joe": ["grandpajoe", "He says there's a pickle in it, and the pickle's spoken for."],
  // NEVADA-12F: no pen is painted on the clipboard; its sheet has a column of empty boxes down the side
  "limo.clipboard.joe": ["grandpajoe", "The office's clipboard. Papers, and a column of empty boxes. Jed's, I reckon."],
  "limo.clipboard.ranger": ["ranger", "..."],
  "limo.clipboard.ranger.joe": ["grandpajoe", "He says it smells of mustard and worry."],
  "limo.juice.joe": ["grandpajoe", "A juice box with a straw in it. Apple, by the picture."],
  "limo.juice.ranger": ["ranger", "..."],
  "limo.juice.ranger.joe": ["grandpajoe", "He says he'd trade for it. He'd trade for anything."],
  "limo.fridge.joe": ["grandpajoe", "A little icebox under the seat. Empty but for a light. Like Harold, only quieter."],
  "limo.fridge.ranger": ["ranger", "..."],
  "limo.fridge.ranger.joe": ["grandpajoe", "He says he checked. Twice. Nothin'."],
  "limo.phone.joe": ["grandpajoe", "A car phone, on a curly cord. Ain't seen one of them since Jolene's cousin struck it rich."],
  "limo.phone.ranger": ["ranger", "..."],
  "limo.phone.ranger.look.joe": ["grandpajoe", "He says it don't ring. He'd like it to."],
  "limo.ashtray.joe": ["grandpajoe", "An ashtray full of jelly beans. Somebody in that office has got their priorities straight."],
  "limo.ashtray.ranger": ["ranger", "..."],
  "limo.ashtray.ranger.joe": ["grandpajoe", "He says the black ones are his."],
  "limo.window.joe": ["grandpajoe", "Desert, goin' by. Same desert I been lookin' at for forty years, only faster."],
  "limo.window.ranger": ["ranger", "..."],
  "limo.window.ranger.joe": ["grandpajoe", "He says he never seen it from in here. He's takin' notes."],
  "limo.seat.joe": ["grandpajoe", "A long gray seat, softer than my rocker. Don't tell Jolene."],
  "limo.seat.ranger": ["ranger", "..."],
  "limo.seat.ranger.joe": ["grandpajoe", "He says it's a fine seat for sittin' on rope. He'd know."],
  // NEVADA-12F: true whatever has been fetched off it (the juice box, drunk, is no longer on the seat)
  "limo.facingseat.joe": ["grandpajoe", "The seat across. They set out lunch, paperwork and a beverage on it. That's an office."],
  "limo.facingseat.ranger": ["ranger", "..."],
  "limo.facingseat.ranger.joe": ["grandpajoe", "He says that seat's got everything a raccoon could want, and he wants all of it."],
  "limo.belt.joe": ["grandpajoe", "Seatbelt, over the ropes. They do things proper. I'll give 'em that too."],
  "limo.belt.ranger": ["ranger", "..."],
  "limo.belt.ranger.joe": ["grandpajoe", "He says he don't hold with seatbelts. He holds on with his hands."],

  // ---------- what the two of them say to each other (limo.talk.*; Ranger's part is limo.ranger.dots) ----------
  "limo.talk.joe.ranger.1a": ["grandpajoe", "You didn't have to come, partner."],
  "limo.talk.joe.ranger.1c": ["grandpajoe", "He says where I go, he goes. Even in a limousine. Especially in a limousine."],
  "limo.talk.joe.ranger.2a": ["grandpajoe", "A whole car full of dark shades, and yours are the only ones a man can see himself in."],
  "limo.talk.joe.ranger.2c": ["grandpajoe", "He says that's because he paid for his. Well. He traded."],
  "limo.talk.joe.ranger.3a": ["grandpajoe", "Hands, partner. Thank you kindly."],                                                // once the ropes are off (limo.loose)
  "limo.talk.joe.ranger.3c": ["grandpajoe", "He says don't mention it. He'll be mentionin' it himself, later."],
  "limo.talk.joe.ranger.4a": ["grandpajoe", "That map's comin' home with us, partner. Somebody ought to know what opens them holes."],   // once the map is his (limo.map)
  "limo.talk.joe.ranger.4c": ["grandpajoe", "He says the little girls know. He's right."],
  "limo.talk.ranger.joe.1c": ["grandpajoe", "I know, partner. I miss her too. She'll be changin' her hat about now."],
  "limo.talk.ranger.joe.2c": ["grandpajoe", "Them little girls? They'll be fine. They had their mama, and their mama had a plan."],

  // ---------- the things carried in this act (js/content/world.js, items): Grandpa Joe's and Ranger's looks, and the family's ----------
  "item.sectormap.grandpajoe": ["grandpajoe", "The office's map. Three holes in my desert, and a column for what opens 'em with nothin' in it."],
  "item.sectormap.ranger": ["ranger", "..."],
  "item.sectormap.ranger.joe": ["grandpajoe", "He says it smells of cheeseburger. That's my fault."],
  "item.sectormap.mom": ["mom", "A map of the desert with three sectors drawn on it, and a column for what opens them, quite empty."],
  "item.sectormap.bigsis": ["bigsis", "Three sectors. Two of them I know. The third is under a thumbprint. That will not do."],
  "item.sectormap.lilsis": ["lilsis", "A MAP! With HOLES on it! ...Not real holes. Drawing holes. Of the REAL holes."],
  "item.receipt.grandpajoe": ["grandpajoe", "'RECEIVED: one banjo (damaged). one raccoon (unconfirmed).' I aim to collect."],
  "item.receipt.ranger": ["ranger", "..."],
  "item.receipt.ranger.joe": ["grandpajoe", "He says he's confirmed. He'd like that wrote down."],
  "item.receipt.mom": ["mom", "A receipt for a banjo, from the government. One does like a paper trail."],
  "item.receipt.bigsis": ["bigsis", "'One raccoon (unconfirmed).' 'Ranger,' she noted, 'had never been more confirmed.'"],
  "item.receipt.lilsis": ["lilsis", "A receipt for a BANJO! You can get a banjo BACK with this. That's how receipts WORK."],
};
