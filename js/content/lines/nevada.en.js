// Act Four: the middle of Nevada, the next morning.
//   "line.id": ["who", "What they say."]
// docs/CHARACTERS.md says how each of them talks. Every fact Big Sister or her mother states is true (the tables are at
// the end of that file; the rows this act's new lines need there are written out in briefs/out/nevada-doc-changes.md).
//
// The door in time where the tracks stop is shut and cannot be seen until the last beat: nobody says the air
// wobbles or shimmers. It hums. What opens it is light, and the only one who has seen that happen is the
// old-timer, who tells it without knowing which part of his story matters (nevada.old.saw.1b and nevada.old.saw.2).
//
// MOM, AS SHE NOW IS, AND THE FAMILY'S FAITH (briefs/WEAVE.md; each group of lines is marked "woven" below).
//   - Mom says "A matter of record:" where her daughter says "Fun fact:", and what follows is true. So is every
//     other thing she states about her country: the sources are in briefs/out/facts-home.md.
//   - Scripture is quoted twice, word for word from the King James Version, each with its reference in the same line:
//     Matthew 22:21, its second sentence (nevada.coin.read.2d), and the first clause of Psalm 31:15 (nevada.gate.5b).
//     The psalm's clause ends on a colon in the King James text, so the quotation marks close before the line's own
//     colon. Do not "tidy" either of them. Franklin's seven words (nevada.flash.sun) are James Madison's, capital S and all.
//   - A hymn is named and not quoted (nevada.talk.lilsis.mom.3b). The prayer is their own words (nevada.pray.1, .2).
//   - "B.C." is explained at the Roman year (nevada.gate.2c and .2d come straight after nevada.gate.2), and nowhere else.
//   - "I TOLD you! Daddy's not lost! Daddy's EARLY!" (nevada.gate.4) is the author's line: it stays word for word, and
//     it stays Little Sister's last word. The check script (briefs/out/nevada-check.mjs) holds all of this.
//
// THE YEARS, AND THE CHICKENS (briefs/DATING.md: the author's two rules. The lines are marked "dating" or "chickens".)
//   - Every year before Christ is the Bible's own count, as Archbishop Ussher counted it. The notice seals sectors 44
//     and 1921. 1921 B.C. is on Big Sister's timeline: the year Abram went down into Egypt (Genesis 12:10), told in her
//     own words (nevada.gate.2b), and her mother knows the chapter (.2e: named, not quoted). From 1921 B.C. to A.D. 2026
//     is 3,946 years: "nearly four thousand" (nevada.gate.5). Nobody here uses any other count of the years.
//   - The doors open on years that matter. Big Sister notices it once, and does not know why (nevada.gate.2f). It is a
//     plant: nothing here pays it off.
//   - Little Sister loves chickens above everything, and is always right about them. The old-timer's hens are told of
//     and never seen (nevada.old.saw.3b), and she takes them as evidence (.3c). At the door it is she who hears the
//     chickens, before anybody smells a sausage (nevada.door.2b), and her mother confirms it (nevada.door.4). And she
//     misses General Feathers, who went with Daddy to keep an eye on him (nevada.talk.lilsis.mom.4a).
//
// LITTLE SISTER, CUTER AND MORE SPUNKY (the author, 7 October, evening: briefs/ROUND-3.md, section 6; briefs/RN-3.md).
//   She is seven: small, fearless, bossy, loving, certain about everything, chickens most of all; often right, never
//   babyish, never the butt of the joke. In this act she names everything (the Rock Wizard, Mister Gray, the Hummy Place,
//   a yellow spinny flower), counts the man in gray's questions on her fingers (and has toes too), gives orders (to him
//   as well), will not be left out, and is ready before anyone has finished explaining. Her loose tooth is not for sale:
//   it is waiting for Daddy to see it (as she says at home). One word comes out nearly right, and she sticks to it:
//   "radiator" (nevada.notice.lilsis, nevada.talk.bigsis.lilsis.1a). "I'm not scared. I'm BRAVE-scared." is hers from
//   the house. Word for word and where they were: "I TOLD you! Daddy's not lost! Daddy's EARLY!" (nevada.gate.4, the top
//   of the scene) and "That's EVIDENCE. Chickens KNOW." (nevada.old.saw.3c). Where her new words changed what was said
//   back, the reply changed too (nevada.agent.lil.6, nevada.talk.bigsis.lilsis.1d, nevada.talk.lilsis.mom.1b).

export const lines = {
  // ---------- the middle of Nevada, the next morning ----------
  "nevada.arrive.1": ["mom", "Thirty-seven miles past Last Gas. This is where the map stops."],
  "nevada.arrive.2": ["bigsis", "Fun fact: Nevada became a state on the thirty-first of October, 1864. Halloween."],
  "nevada.arrive.2b": ["mom", "Reformation Day, darling. A matter of record: Martin Luther's ninety-five theses, 1517."],      // woven: her fact caps her daughter's
  "nevada.arrive.3": ["lilsis", "It's ALL dirt. Who ordered this much dirt? ...Okay. I'm ready. Where do I start looking for Daddy?"],
  "nevada.arrive.4": ["mom", "Somebody here saw something. We will ask nicely. Stay where I can see you, girls."],

  // ---------- chain A: the old-timer ----------
  "nevada.old.look.mom": ["mom", "A gentleman in a lawn chair, selling rocks and lemonade to a road with no cars on it. He will have seen whatever passed."],
  "nevada.old.look.bigsis": ["bigsis", "One witness. Elderly, seated, hat. He is pretending not to watch us. Badly."],
  "nevada.old.look.lilsis": ["lilsis", "A real wizard! White beard, magic hat, and he sells ROCKS. His name is the Rock Wizard. I just decided."],
  "nevada.old.lilsis.1": ["lilsis", "Mister! Did you see my daddy? He's THIS tall, he has a scratchy beard, and he's EARLY."],
  "nevada.old.lilsis.2": ["oldtimer", "Lemonade's a dollar, little miss. Stories are extra."],
  "nevada.old.lilsis.3": ["lilsis", "I don't HAVE a dollar. I have a loose tooth. But it's not for sale. It's waiting for Daddy."],
  "nevada.old.bigsis.1": ["bigsis", "Sir. Did you observe a red station wagon yesterday at approximately 5:47 p.m.?"],
  "nevada.old.bigsis.2": ["oldtimer", "Didn't see nothing. Been not seeing nothing out here for forty years."],
  "nevada.old.bigsis.3": ["bigsis", "That is a double negative. Technically, you saw something."],
  "nevada.old.bigsis.4": ["oldtimer", "Technically, I'm closed."],
  "nevada.old.mom.1": ["mom", "Good morning. Forgive us for troubling you. May I buy three lemonades, and a few minutes of your time?"],
  "nevada.old.mom.2": ["oldtimer", "Well, now. Forty years out here, and you're the first one to say good morning."],
  "nevada.old.mom.3": ["oldtimer", "Folks come asking about yesterday. Men in gray suits, mostly. I tell 'em I didn't see nothing."],
  "nevada.old.mom.4": ["mom", "And did you see nothing?"],
  "nevada.old.mom.5": ["oldtimer", "Depends who's asking. You kin to whoever was in that car?"],
  "nevada.old.mom.6": ["mom", "My husband and my son."],
  "nevada.old.mom.7": ["oldtimer", "Then tell me what they were driving. The gray suits couldn't."],
  "nevada.car.wagon": ["mom", "A red station wagon with wood on the sides and far too much luggage on the roof."],
  "nevada.car.sedan": ["mom", "A sensible silver sedan."],
  "nevada.car.black": ["mom", "A black car with dark windows."],
  "nevada.car.no.sedan": ["oldtimer", "No, ma'am. Nothing sensible came down this road yesterday."],
  "nevada.car.no.black": ["oldtimer", "That's what the gray suits drive. Try again."],
  // What he saw. The flash of low sun is the part that matters, and he does not know it.
  "nevada.old.saw.1": ["oldtimer", "That's the one. Red wagon, wood trim, cooler on the roof. Driver waved at me. Nobody waves anymore."],
  "nevada.old.saw.1b": ["oldtimer", "Sun was low. Hit the chrome on that wagon and threw a flash up ahead, like a signal mirror."],
  "nevada.old.saw.2": ["oldtimer", "Right where it landed, the sky opened up like a tin can. The road sign changed its mind. And that wagon drove straight in."],
  "nevada.old.saw.3": ["oldtimer", "Hour later the gray suits came and put up a fence. 'Radiation,' they say. Third piece of desert they've shut this year."],
  // chickens: his hens, out behind the shack, told of and never seen. To him they are one more odd thing about the week.
  "nevada.old.saw.3b": ["oldtimer", "Been a strange week. My hens quit laying the day the sky opened. Stand out back all day now, facing that fence."],
  "nevada.old.saw.3c": ["lilsis", "That's EVIDENCE. Chickens KNOW."],
  "nevada.old.saw.4": ["mom", "Thank you. You have been kinder than you needed to be."],
  "nevada.old.saw.5": ["oldtimer", "One more thing. This fell out of the sky this morning. Hit my hat. Seems like it's yours more than mine."],
  "nevada.old.saw.6": ["mom", "A silver coin. With a very serious gentleman on it."],
  "nevada.ask.flash": ["mom", "The flash of light, if you would. From the top."],                                            // woven: a stage manager asks for it again
  "nevada.ans.flash": ["oldtimer", "Low sun on bright chrome, ma'am. One flash, up ahead. And where it fell, the sky came open. Never seen the like."],
  "nevada.ask.fence": ["mom", "What is behind the fence?"],
  "nevada.ans.fence": ["oldtimer", "Used to be nothing. Now it's nothing with a fence around it."],
  "nevada.ask.areas": ["mom", "You said they have closed other places."],
  "nevada.ans.areas": ["oldtimer", "Three this year. Always the same sign. 'Elevated radiation.' Funny thing is, my old Geiger counter never clicks once."],
  "nevada.ask.bye": ["mom", "We must not keep you."],
  "nevada.ans.bye": ["oldtimer", "You ain't. I got all day. I got all decade."],
  "nevada.old.after.lilsis.1": ["oldtimer", "Your ma's good people. Lemonade's on the house, little miss."],
  "nevada.old.after.lilsis.2": ["lilsis", "On the house? WHERE'S the house? ...Thank you, Mister Rock Wizard. You're a GOOD wizard."],
  "nevada.old.after.bigsis.1": ["bigsis", "Sir. They say radiation. Do you own anything that measures it?"],
  "nevada.old.after.bigsis.2": ["oldtimer", "My daddy's Geiger counter. Clicked fine for him in fifty-seven. Hasn't clicked once this year."],
  "nevada.old.after.bigsis.3": ["bigsis", "Then somebody is lying, and it isn't the Geiger counter. Interesting."],
  "nevada.old.coin": ["mom", "He gave it to us, darling. It would be rude to give it back."],

  // ---------- chain B: the man in gray, and the notice ----------
  "nevada.agent.look.mom": ["mom", "A man in a gray suit, standing precisely in front of the one thing worth reading."],
  "nevada.agent.look.bigsis": ["bigsis", "Gray suit, gray tie, dark glasses. He is standing in front of that notice on purpose. That is called obstruction."],
  "nevada.agent.look.lilsis": ["lilsis", "He's ALL gray. Gray suit, gray tie, gray FROWN. I bet his dog's gray too. I'm naming him Mister Gray."],
  "nevada.agent.mom.1": ["mom", "Good morning. May we read the notice behind you?"],
  "nevada.agent.mom.2": ["agent", "There is no notice, ma'am."],
  "nevada.agent.mom.3": ["mom", "I can see all four corners of it."],
  "nevada.agent.mom.4": ["agent", "I can neither confirm nor deny a corner."],
  // woven: Mom's second try. Courtesy, for her, is General Washington's 110 rules. This gentleman has not read one.
  "nevada.agent.mom.5": ["mom", "A matter of record: by the time he was sixteen, General Washington had copied out 110 rules of civility."],
  "nevada.agent.mom.6": ["agent", "I can neither confirm nor deny General Washington."],
  "nevada.agent.mom.7": ["mom", "Then you have not read one of them. Good morning."],
  "nevada.agent.bigsis.1": ["bigsis", "Under what authority is this area closed?"],
  "nevada.agent.bigsis.2": ["agent", "I can neither confirm nor deny that it is an area."],
  "nevada.agent.bigsis.3": ["bigsis", "It has a fence."],
  "nevada.agent.bigsis.4": ["agent", "I can neither confirm nor deny the fence."],
  "nevada.agent.lil.1": ["lilsis", "Hi, Mister Gray! I have some questions. Number ONE: why is your tie gray?"],
  "nevada.agent.lil.2": ["agent", "Move along, little girl."],
  "nevada.agent.lil.3": ["lilsis", "That's not an ANSWER. Number two: is your car gray? Three: is your DOG gray? Four: do you HAVE a dog?"],
  "nevada.agent.lil.4": ["agent", "I can neither confirm nor deny a dog."],
  "nevada.agent.lil.5": ["lilsis", "Five: what's his NAME? Why are you standing THERE? Is it your turn? Do you get a snack? That's EIGHT fingers. I have TOES too."],
  "nevada.agent.lil.6": ["agent", "...Sir? It's me. I have a situation. No, sir. She is about seven. And she says she has toes."],
  "nevada.agent.lil.7": ["lilsis", "Who are you talking to? Is it your mommy? Tell her you're not DONE. ...Hi, Mister Gray's mommy!"],
  "nevada.agent.lil.8": ["bigsis", "'It was,' she noted, 'the finest interrogation she had ever witnessed.'"],
  "nevada.agent.busy": ["agent", "Sir, now she wants to know whose side the SUN is on. ...No, sir. I didn't have an answer either."],
  "nevada.agent.again.1": ["lilsis", "You stay RIGHT there. Next question. Why is the sky? Not why is it BLUE. Why IS it?"],
  "nevada.agent.again.2": ["agent", "...We are going to need a bigger department."],
  "nevada.agent.coin.1": ["agent", "I can neither confirm nor deny that that is a coin."],
  "nevada.agent.coin.2": ["agent", "If it were a coin, I would have to file a report. So it is not a coin."],

  "nevada.notice.blocked.mom": ["mom", "The gentleman is standing exactly in front of it. One admires the precision."],
  "nevada.notice.blocked.bigsis": ["bigsis", "I can read 'AREA CLOSED'. The small print is behind his jacket. That is not enough to work with."],
  "nevada.notice.blocked.lilsis": ["lilsis", "Mister Gray is standing in the WAY. I could ask him to move. I could ask him a LOT of things."],
  // dating: the notice reads SECTORS 44 AND 1921 (the close-up is notice() in js/art/kit.js)
  "nevada.notice.mom.1": ["mom", "'Area closed. Elevated radiation levels. Sectors 44 and 1921 sealed until further notice.'"],
  "nevada.notice.mom.2": ["mom", "Sectors. As though the desert had been numbered. Your sister should see this."],
  "nevada.notice.lilsis": ["lilsis", "It says... A, R, E, A. AREA! I can READ that. And a yellow spinny flower. 'Radiator levels.' That's bad, right?"],
  "nevada.notice.big.1": ["bigsis", "'Elevated radiation levels.' In Nevada, people will believe that. Fun fact: atomic bombs were tested out here from 1951 until 1992."],
  "nevada.notice.big.2": ["bigsis", "Which makes it a very good excuse. But look at the sectors. Forty-four. Nineteen twenty-one."],
  "nevada.notice.big.3": ["bigsis", "Nobody numbers sectors like that. Those aren't places, Mother. I think those are years."],
  "nevada.notice.again": ["bigsis", "Sector 44. Sector 1921. Years. I am almost certain. 'Almost' is the part I don't like."],

  // ---------- the coin ----------
  "nevada.coin.read.1": ["bigsis", "Mother. This is a Roman denarius. And that is Julius Caesar."],
  "nevada.coin.read.2": ["bigsis", "Fun fact: in 44 B.C., coins were struck in Rome with Caesar's own portrait. While he was alive."],
  // woven: it is the coin of the tribute money. Little Sister knows it from Sunday school, Big Sister has the fact,
  // and Mom has the verse: Matthew 22:21, King James Version, its second sentence, exact. (In Rome, in Act Two, her
  // son told the same story in his own words, with this same coin in his hand.)
  "nevada.coin.read.2b": ["lilsis", "It's the Caesar money from Sunday school!"],
  "nevada.coin.read.2c": ["bigsis", "The 'penny' they brought to Jesus was a denarius, like this one. Most likely with a later Caesar on it: Tiberius."],
  "nevada.coin.read.2d": ["mom", "'Render therefore unto Caesar the things which are Caesar's; and unto God the things that are God's.' Matthew 22:21."],
  "nevada.coin.read.3": ["bigsis", "And it isn't two thousand years old. Look at the edges. It is NEW. It has hardly been in a pocket."],
  "nevada.coin.read.4": ["mom", "A new coin, from 44 B.C., that fell out of the sky. In Nevada."],
  "nevada.coin.lilsis": ["lilsis", "I get to HOLD it? Finally! Hi, grumpy man. You're with ME now. I'm holding you with BOTH hands."],
  "nevada.coin.mom": ["mom", "Thank you, darling. I will keep it in my handbag, with everything else that matters."],
  "nevada.connect": ["bigsis", "Sector 44. A new coin from 44 B.C. It is the same forty-four. The holes don't go to places. They go to YEARS."],

  // ---------- the gate: where the tracks stop. Nothing to see but glass; and a hum ----------
  "nevada.tracks.look.mom": ["mom", "Tire tracks. They run out from under that fence and they simply... stop. At a patch of sand that has turned to glass."],
  "nevada.tracks.look.bigsis": ["bigsis", "It takes a furnace to turn sand into glass. Something here was very hot, very briefly."],
  "nevada.tracks.look.lilsis": ["lilsis", "The ground's all SHINY. And it hums, like a bee in a jar. But there's no bee. And no jar. It's the Hummy Place."],
  "nevada.tracks.early.mom": ["mom", "Not yet, darlings. I would like to understand it before any of us stands on it."],
  "nevada.tracks.early.bigsis": ["bigsis", "I have a theory. A theory is not a fact until I can footnote it."],
  "nevada.tracks.early.lilsis": ["lilsis", "I'll jump on it first. I'm the lightest, so it's SAFEST. ...Mommy's doing the eyebrow. That's a no."],
  // Her flashlight, from the blanket fort at home. Light opens doors in this story, and this light is too little:
  // in full morning sun its spot cannot even be seen. (Whoever is holding it, she is the one who says so.)
  "nevada.tracks.lilflash": ["lilsis", "CLICK. It's ON! ...Where's my spot? I can't even SEE my spot. The sun's got a WAY bigger flashlight."],
  // Going there once the coin and the notice are both read: each of them listens, and remembers the old man's flash.
  "nevada.hum.mom.1": ["mom", "It hums, darlings. Very quietly, and a little flat. Like your father when he is lost and will not say so."],      // woven: she hears pitch
  "nevada.hum.mom.2": ["mom", "The gentleman said a flash of low sun fell just here. I wonder what we have that flashes."],
  "nevada.hum.bigsis.1": ["bigsis", "It hums. Right here, over the glass, where there is nothing at all to hum."],
  "nevada.hum.bigsis.2": ["bigsis", "A flash of low sun fell here, and the sky opened. That is his whole story. So: we need a flash."],
  "nevada.hum.lilsis.1": ["lilsis", "It HUMS! Right THERE! There's nothing there and it HUMS! ...Hello? Daddy? Are you in there?"],
  "nevada.hum.lilsis.2": ["lilsis", "The Rock Wizard said the car went FLASH and the sky went OPEN. So we need a flash. I'm READY."],
  // The coin, held up in the low sun, by whichever of them has it.
  "nevada.gate.0": ["mom", "Places, girls."],                                                                               // woven: the stage manager, and they take their marks
  "nevada.gate.1": ["bigsis", "The tracks don't turn. They don't skid. They just stop."],
  // woven: first things first. Mom bows her head and the girls with her; nobody has to be told. In their own words.
  "nevada.pray.1": ["mom", "Father, You brought us this far. We do not understand what comes next, and You do. Keep us, and keep them. In Jesus' name."],
  "nevada.pray.2": ["lilsis", "And thank You for the lemonade. And tell Daddy we're COMING, so he doesn't have to be brave by himself. Amen."],
  // woven: only when it is Mom who holds the coin up. The seven words in quotation marks are Dr. Franklin's, as James
  // Madison wrote them down on the day the Constitution was signed (17 September 1787): capital S and full stop are his.
  // ("Carved" is right for the chair, and is outside the quotation marks: Madison's own word for the sun was "painted".)
  "nevada.flash.sun": ["mom", "Dr. Franklin said the sun carved on General Washington's chair was 'a rising and not a setting Sun.' So is this one."],
  "nevada.flash.mom": ["mom", "Stand back a little, darlings. I am about to do something your father would think of."],
  "nevada.flash.bigsis": ["bigsis", "A low sun. A new coin. And an old man's story. This is called an experiment."],
  "nevada.flash.lilsis": ["lilsis", "My turn! I'm gonna do a FLASH, like the car did! Everybody stand BACK. And WATCH."],
  // The door is open: the size of the coin. What comes through it is small, and settles nothing.
  "nevada.door.1": ["lilsis", "A HOLE! In the AIR! And it's littler than ME! ...I bet I could still FIT."],
  "nevada.door.2": ["bigsis", "'The air,' she noted, 'now had a hole in it. A hole exactly the size of the coin.'"],
  // chickens: they are the first thing she would notice anywhere, before anybody smells a sausage. (Said .2, .2b, .3, .4.)
  "nevada.door.2b": ["lilsis", "SHH! Everybody SHH! ...CHICKENS. Three! No, FOUR! I can hear CHICKENS in there!"],
  "nevada.door.3": ["lilsis", "It's a DIFFERENT sunny in there! And it smells like SAUSAGES!"],
  "nevada.door.4": ["mom", "Chickens. She is quite right. And sausages, and bread, and woodsmoke."],
  "nevada.door.5": ["bigsis", "It is morning in there, too. I do not think it is THIS morning."],
  "nevada.door.6": ["mom", "Then which morning, darling?"],
  "nevada.gate.2": ["bigsis", "Sector 44: forty-four B.C. The year Julius Caesar was killed, on the Ides of March."],
  // woven: what B.C. is, asked and answered at the Roman year, just before the reveal. It is what makes EARLY land.
  // (Said in the order .2, .2c, .2d, .2b, .2e, .2f, .3: the ids were not renumbered.)
  "nevada.gate.2c": ["lilsis", "Wait! What's B.C.? Somebody tell me QUICK."],
  "nevada.gate.2d": ["mom", "Before Christ, sweetheart. Before Jesus was born."],
  // dating: the second year is on her own timeline (the Bible's count, as Ussher counted it), and her mother knows the
  // chapter: Genesis 12, told and not quoted. Then, once, the pattern: both are years when something happened. She does
  // not know why. (A plant: nothing pays it off yet.)
  "nevada.gate.2b": ["bigsis", "Sector 1921: nineteen twenty-one B.C. It is on my timeline: the year Abram went down into Egypt."],
  "nevada.gate.2e": ["mom", "Genesis 12. I have known that chapter all my life, darling. I had never once thought of it as a morning."],
  "nevada.gate.2f": ["bigsis", "The Ides of March. Abram in Egypt. The holes open on years that MATTER. ...I don't know why."],
  "nevada.gate.3": ["bigsis", "They didn't crash, Mother. They didn't go anywhere. They went some WHEN."],
  "nevada.gate.4": ["lilsis", "I TOLD you! Daddy's not lost! Daddy's EARLY!"],                                              // the author's line: word for word, and the top of the scene
  // dating: from 1921 B.C. to A.D. 2026 is 3,946 years (there is no year 0)
  "nevada.gate.5": ["bigsis", "...Nearly four thousand years early. She was right. I need to sit down."],
  // woven: the family's answer to the whole story. Psalm 31:15, King James Version, its first clause, exact.
  "nevada.gate.5b": ["mom", "'My times are in thy hand': Psalm 31, verse 15. Every one of the times, darlings. Even that one."],
  "nevada.gate.6": ["mom", "Then we know where they are. And we have a door. It is only a little small."],
  "nevada.gate.7": ["mom", "Girls. We are going to go and bring them home."],

  // ---------- the rest of the lot ----------
  "nevada.car.look.mom": ["mom", "My car. It has never once taken a shortcut. It is the only vehicle in this family still in this century."],
  "nevada.car.look.bigsis": ["bigsis", "Mom's car. She parked it parallel to nothing. Perfectly."],
  "nevada.car.look.lilsis": ["lilsis", "I get the front seat going home. I called it. I called it in the DRIVEWAY. Those are the RULES."],
  "nevada.shack.mom": ["mom", "'Last Stop.' I do hope that is geography and not a prediction."],
  "nevada.shack.bigsis": ["bigsis", "A building held together by paint and optimism. Mostly optimism."],
  "nevada.shack.lilsis": ["lilsis", "They sell ROCKS. You can just FIND rocks. This is the best shop ever."],
  "nevada.pump.mom": ["mom", "A gas pump with no gas in it. There is a great deal of that about."],
  "nevada.pump.bigsis": ["bigsis", "'The pump,' she noted, 'had not served a customer in her lifetime. Or, by the look of it, in her mother's.'"],
  "nevada.pump.lilsis": ["lilsis", "It has a ball on its head. Like a lollipop for cars."],
  "nevada.stand.mom": ["mom", "'Lemonade, one dollar. Rocks, two dollars. Stories extra.' An honest price list."],
  "nevada.stand.bigsis": ["bigsis", "Quartz, sandstone, and one that is just a rock. I respect the honesty."],
  "nevada.stand.lilsis": ["lilsis", "Lemonade! Mommy! LEMONADE! ...Please."],
  "nevada.fence.mom": ["mom", "A fence, put up in a hurry by people who were not expecting an audience."],                  // woven: one word of the theatre
  "nevada.fence.bigsis": ["bigsis", "The posts are new, and the concrete around them is still dark. This fence went up yesterday."],
  "nevada.fence.lilsis": ["lilsis", "I could fit under that. I fit under EVERYTHING. ...I'm just SAYING."],

  // ---------- what they say to each other ----------
  "nevada.talk.mom.bigsis.1a": ["mom", "What do you make of it, darling?"],
  "nevada.talk.mom.bigsis.1b": ["bigsis", "It is too tidy. Real accidents are messy. This one has a fence and a sign."],
  "nevada.talk.mom.bigsis.2a": ["mom", "Two books in the car, darling, and you have not opened either. I am almost concerned."],
  "nevada.talk.mom.bigsis.2b": ["bigsis", "This is better than either of them. Do not tell them."],
  "nevada.talk.mom.bigsis.2c": ["mom", "Your secret is safe, darling."],
  "nevada.talk.mom.bigsis.coin.a": ["mom", "The gentleman gave me a coin. I would like your opinion of it."],
  "nevada.talk.mom.bigsis.coin.b": ["bigsis", "Then hand it over, Mother. I can't footnote what I can't hold."],
  // woven: once the coin has been read. Mom has the motto, and her daughter has the year: they keep score.
  "nevada.talk.mom.bigsis.quarter.a": ["mom", "A matter of record: Caesar put his own face on his money. Ours says 'In God We Trust.'"],
  "nevada.talk.mom.bigsis.quarter.b": ["bigsis", "Fun fact: first in 1864, on the two-cent piece. The year Nevada became a state. That half is mine."],
  "nevada.talk.mom.lilsis.1a": ["mom", "Drink your lemonade slowly, sweetheart."],
  "nevada.talk.mom.lilsis.1b": ["lilsis", "I AM drinking it slowly. I'm drinking it slowly really FAST."],
  "nevada.talk.mom.lilsis.2a": ["lilsis", "Mommy, is Daddy STILL in trouble?"],                                           // (she asked it at home too: "STILL" makes this the second time)
  "nevada.talk.mom.lilsis.2b": ["mom", "A little, sweetheart. But only with me, and only once he is home."],
  "nevada.talk.mom.lilsis.gray.a": ["mom", "That gentleman in gray will not move for me."],
  "nevada.talk.mom.lilsis.gray.b": ["lilsis", "Did you ask him enough times? You have to ask a LOT of times. I'll show you how. Watch me."],
  "nevada.talk.bigsis.mom.1a": ["bigsis", "For the record: I am not frightened. I am gathering data."],
  "nevada.talk.bigsis.mom.1b": ["mom", "Gather it close to me, please."],
  "nevada.talk.bigsis.mom.2a": ["bigsis", "Mom. If I turn out to be right about this, may I say so?"],
  "nevada.talk.bigsis.mom.2b": ["mom", "Once, darling. Graciously."],
  "nevada.talk.bigsis.mom.2c": ["bigsis", "...I'll practice."],
  "nevada.talk.bigsis.lilsis.2a": ["bigsis", "Stay where I can see you."],
  "nevada.talk.bigsis.lilsis.2b": ["lilsis", "You stay where I can see YOU. I'm the one with the boots."],
  "nevada.talk.bigsis.lilsis.gray.a": ["bigsis", "I need that man to look somewhere else for sixty seconds."],
  "nevada.talk.bigsis.lilsis.gray.b": ["lilsis", "Sixty SECONDS? I can do sixty HOURS. I'm very good at questions."],
  "nevada.talk.bigsis.lilsis.1a": ["lilsis", "What's radiator levels? Is it a car thing? Daddy's car has a radiator."],
  "nevada.talk.bigsis.lilsis.1b": ["bigsis", "Radiation. It's a kind of energy you can't see."],
  "nevada.talk.bigsis.lilsis.1c": ["lilsis", "Like me when I hide! Nobody EVER finds me. I'm the best hider in our whole house."],
  "nevada.talk.bigsis.lilsis.1d": ["bigsis", "That is, regrettably, true. We once looked for an hour. She was in the laundry basket, under the towels."],
  "nevada.talk.lilsis.mom.1a": ["lilsis", "Mommy, is the Rock Wizard a real wizard? Or is he Santa, on vacation? He has the beard for both."],
  "nevada.talk.lilsis.mom.1b": ["mom", "If he is Santa, darling, then we have been very good this year."],
  "nevada.talk.lilsis.mom.2a": ["lilsis", "Mommy, when we find Daddy, can I tell him I fixed the internet?"],
  "nevada.talk.lilsis.mom.2b": ["mom", "You may tell him first, before anybody says anything else at all."],
  "nevada.talk.lilsis.mom.2c": ["lilsis", "Even before 'hi'? ...Then I'll show him my tooth SECOND."],
  // woven: a hymn, named and not quoted
  "nevada.talk.lilsis.mom.3a": ["lilsis", "Mommy, you're humming. Is it the one with the loud part?"],
  "nevada.talk.lilsis.mom.3b": ["mom", "'O God, Our Help in Ages Past,' sweetheart. Every part of it is the loud part, if one means it."],
  // chickens: once the old-timer has told of his hens. The General went in Daddy's suitcase, to keep an eye on him.
  "nevada.talk.lilsis.mom.4a": ["lilsis", "Mommy, I miss General Feathers. But Daddy needs her MORE. She's keeping an eye on him. He has to do what she SAYS."],
  "nevada.talk.lilsis.mom.4b": ["mom", "Then he is well looked after, sweetheart. She outranks him."],
  "nevada.talk.lilsis.bigsis.2a": ["lilsis", "Are you scared? You can tell me. I won't tell anybody."],
  "nevada.talk.lilsis.bigsis.2b": ["bigsis", "No. ...A little. Hold my hand. It is for your sake, obviously."],
  "nevada.talk.lilsis.bigsis.2c": ["lilsis", "Okay. I'm holding it MIGHTILY. I'm not scared. I'm BRAVE-scared."],
  "nevada.talk.lilsis.bigsis.1a": ["lilsis", "I'm small but I'm MIGHTY. Feel my muscle. FEEL it."],
  "nevada.talk.lilsis.bigsis.1b": ["bigsis", "You are small but you are LOUD. It is a different thing."],
  "nevada.talk.lilsis.bigsis.1c": ["lilsis", "It's the SAME thing."],


  // ---------- hints: one from each of them for every puzzle ----------
  "hint.nevada.witness.mom": ["mom", "The gentleman in the lawn chair has had a front-row seat on this road for forty years. Nobody has asked him nicely."],      // woven: a theatre-goer's eye
  "hint.nevada.witness.bigsis": ["bigsis", "The old man is a witness, and he doesn't care for my questions. Mom could get a statue to talk."],
  "hint.nevada.witness.lilsis": ["lilsis", "The Rock Wizard won't tell ME. He wants a dollar. Mommy has dollars AND manners. Mommy should ask him."],
  "hint.nevada.coin.mom": ["mom", "I have a silver coin I cannot read. I should hand it to the one of us who can."],
  "hint.nevada.coin.bigsis": ["bigsis", "Mom is carrying a coin that fell out of the sky. I need to see it. In my own hands."],
  "hint.nevada.coin.lilsis": ["lilsis", "Mommy got a shiny money from the Rock Wizard. My sister knows ALL the olden-days stuff. Give it to HER."],
  "hint.nevada.distract.lilsis": ["lilsis", "Mister Gray is standing in front of the sign. I have SO many questions for him. All my fingers' worth."],
  "hint.nevada.distract.mom": ["mom", "That man will not move for courtesy. He has not yet met your little sister."],
  "hint.nevada.distract.bigsis": ["bigsis", "He can deflect one question. Can he deflect two hundred? I know someone who has two hundred."],
  "hint.nevada.notice.bigsis": ["bigsis", "The man in gray has his hands full. Now I can read that notice properly."],
  "hint.nevada.notice.mom": ["mom", "The notice is free at last. Your sister should be the one to read it. She reads between the lines."],
  "hint.nevada.notice.lilsis": ["lilsis", "I got Mister Gray out of the way! Now somebody who reads FAST has to go and read it. Go GO GO!"],
  "hint.nevada.tracks.mom": ["mom", "A flash of low sun opened the sky where the tracks stop. We have a low sun, and a very new coin."],
  "hint.nevada.tracks.bigsis": ["bigsis", "A flash of sun opened it once. The sun is low again, and the coin is new enough to flash. Where the tracks stop."],
  "hint.nevada.tracks.lilsis": ["lilsis", "The shiny money can do a FLASH, like the car did! At the Hummy Place, where the car tracks stop! I'm READY."],
};
