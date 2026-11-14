// Act Six, "By Your Grace": Japan, spring 1830. The first leg: the arrival at Yui on Suruga Bay, Kihei's shop, puzzles #21
// to #24, the voyage, and the act's common lines (WRITE-20A: new in round twenty; briefs/WRITE-20.md, briefs/ROUND-20.md,
// and the design, briefs/out/edo-design.md, sections 7 and 8). MERGE-20 joins this file with WRITE-20B's edo-b.en.js.
//   "line.id": ["who", "What they say."]
//
// MOM ("mom"), BIG SISTER ("bigsis") and LITTLE SISTER ("lilsis") came through the coin door expecting the Son, and came
// out on a beach under Fuji. Nobody in the family lies, all act: every option the player can pick for them is true, and the
// comedy is in exactly true answers ("From the east."). Big Sister cannot read a thing in this country, for the first time
// in her life, and has about forty words of Japanese, all of them food; Little Sister learns one word, "arigatō", from
// Sankichi, and uses it on everyone. Mom asks nicely, and knows which adult to ask.
//
// THE PEOPLE OF YUI (PEOPLE-20 draws them; their cast ids are ROUND-20's): KIHEI ("kihei") the fishmonger, sixty this
// tiger year, in the red vest and hood his wife makes him wear, few words; O-TAMI ("tami") his wife, who runs the house,
// the shop and him, and has a baby who will not settle; SANKICHI ("sankichi") their grandson, nine, who can read, and asks
// questions in Little Sister's own rhythm; TOKUZŌ ("tokuzo") the headman's clerk, fussy, polite, very short-sighted;
// GONROKU ("gonroku") the captain, who speaks in weather and will not have women aboard; O-MASA ("masa") his wife, Kihei's
// sister, who speaks in verdicts; a NET-MENDER ("netmender") and a WOMAN WITH A BASKET ("basketwoman"). The cards are the
// narrator's. Nobody remarks that everyone understands everyone.
//
// JAPANESE WORDS, each glossed once, by its speaker or by Big Sister: "okage-sama de" (edo.shop.meal.13 and .14),
// "arigatō" (edo.sankichi.thanks.2), "Funadama" (edo.gonroku.no.2), "Kirishitan" (the board: edo.village.board.read.2),
// "saba" (edo.shop.meal.5). No "itadakimasu" or "gochisōsama": Kihei and O-Tami bow to the god-shelf before they eat, and
// say nothing (edo.shop.meal.10). The castle is not in this half.
//
// FACTS. Big Sister and Mom state only what the two fact files confirm (S/work-20-facts/facts-edo.md, S/work-20-factsB/
// facts-edo-2.md): the tiger cycle and 2010 (edo.when.solve.*), the Kan'ei Tsūhō and the Edo period (edo.shop.money.clue),
// Prussian blue new to the prints (edo.shop.print.clue), Edo's new hand-made sushi and the pressed kind here
// (edo.shop.meal.5, .6), okage-sama de (edo.shop.meal.14), Fuji white into the summer (edo.village.fuji.bigsis), married
// women's blackened teeth (edo.shop.tami.bigsis), Psalm 139 (edo.sail.1, .2). What the Japanese people say of their own
// time (the red clothes of a sixtieth year, the metal tiger, the thirteenth year of Bunsei, the Funadama's things in the
// mast, sandals at fifteen mon, the Tōkaidō west, twelve days to Osaka) is in the same files: S/work-20-writeA/ready.md
// lists each with its item. Nothing goes in as a fact that is not there.
//
// SCRIPTURE: Psalm 139:9-10, King James Version, word for word, in Mom's mouth at the stern rail (edo.sail.1 and .2, two boxes:
// the verse's semicolon ends the first); Big Sister says the reference (edo.sail.4), as only she may. Little Sister's grace
// at Kihei's table is her own words (edo.shop.meal.8, .9). Mom's lullaby for the baby is a tune with no words: a stage
// direction (edo.shop.baby.4 is what O-Tami says when it works), never a line.
//
// NOTHING FRIGHTENING: the board is read once (edo.village.board.read.*) and answered once (Mom: "Then we pray quietly
// here."); the clerk peers and apologizes; the captain grumbles and relents; the arrests in Osaka are one line of
// Gonroku's (edo.sail.osaka.3). Nobody is threatened, grabbed or shouted at.
//
// WRITE-21B (round twenty-one, the history pass): edo.map.far.himeji is changed (four days from the hills, not three),
// marked where it stands; the far lines for five legs are in edo-d.en.js (edo.map.far.<place>.<leg>).
//
// The box: one idea, the punch word last, at docs/WRITING.md's lengths (WRITE-25: rewritten to it in round twenty-five;
// 115 characters spoken, 150 the narrator's). S/work-20-writeA/ids.md says when every
// line is said, and which hooks and facts the trees (js/content/talk/edo-a.js) use.

export const lines = {
  // ======================================================================================================
  // CUT-SCENE: Meanwhile, in another time (edo-arrive.js). After Going Down's LAMPLIGHTER card: a card on black, the
  // tunnel, and out onto the beach at Yui at dawn, in a ring of light that closes behind them. Fuji across the water.
  // ======================================================================================================
  "edo.card.meanwhile.1": ["narrator", "Meanwhile"],                                    // SCENES-20A: was edo.card.meanwhile (Going Down reads .1 and .2: office-down.js)
  "edo.card.meanwhile.2": ["narrator", "in another time"],
  // they count off, as a stage manager's family does
  "edo.arrive.1": ["mom", "Places, girls."],
  "edo.arrive.2": ["bigsis", "Here."],
  "edo.arrive.3": ["lilsis", "Here! ...Where's here?"],
  // the bay, the boats, and across the water a white mountain filling a third of the sky
  "edo.arrive.4": ["lilsis", "This isn't Rome. Rome was supposed to have my brother in it."],
  "edo.arrive.5": ["bigsis", "That's Mount Fuji. So this is Japan, and Rome is a very long way from here."],
  "edo.arrive.6": ["lilsis", "Is he here?"],
  "edo.arrive.7": ["mom", "No, sweetheart. Not here."],
  // she looks at the closed air where the door was
  "edo.arrive.8": ["mom", "Then we keep going, girls. It's the one thing asked of us, and we're good at it."],
  // a gull; a rooster somewhere up the beach
  "edo.arrive.9": ["lilsis", "That's a rooster. All right, I can work with a rooster."],
  // the first villager to see them: a woman with a basket, who puts it down and goes
  "edo.arrive.10": ["basketwoman", "Forgive me. I'll come back for the basket."],
  "edo.arrive.11": ["mom", "We've made an impression, girls. Let's see if we can make a kinder one."],
  // the act's card (SCENES-20 shows it where the act begins; Big Sister's line joins it once #21 is solved, edo.when)
  "edo.card.title": ["narrator", "Act Six: By Your Grace"],
  "edo.card.when": ["bigsis", "Spring, 1830. Bunsei thirteen. The year of the metal tiger."],

  // ======================================================================================================
  // THE VILLAGE (edo-village): Yui on Suruga Bay, morning. A look from each of the three at every thing, and a use.
  // ======================================================================================================
  // Fuji, white and enormous across the bay
  "edo.village.fuji.mom": ["narrator", "Mount Fuji, white and enormous across the bay. Mom has seen it on a thousand teacups, and none did it justice."],
  "edo.village.fuji.bigsis": ["narrator", "Mount Fuji, across the bay. Snow that far down its slopes means spring, Big Sister notes, though it stays white into summer."],
  "edo.village.fuji.lilsis": ["narrator", "Mount Fuji, across the bay. It is the biggest thing Little Sister has ever seen, and she has seen Dad's car."],
  "edo.village.fuji.use.mom": ["narrator", "The mountain is miles away across the water. Mom is content to admire it from here."],
  "edo.village.fuji.use.bigsis": ["narrator", "Big Sister knows of nothing a person can do to a mountain except look at it. She looks."],
  "edo.village.fuji.use.lilsis": ["narrator", "Little Sister reaches out to touch the mountain. It turns out to be farther off than it looks."],
  // the bay
  "edo.village.bay.mom": ["narrator", "The bay lies flat and still, with the mountain standing upside down in it."],
  "edo.village.bay.bigsis": ["narrator", "Suruga Bay, if that mountain is Fuji. From here the sea runs all the way round to Osaka."],
  "edo.village.bay.lilsis": ["narrator", "The sea, flat and blue and right there. Little Sister didn't bring a swimsuit, or anything else."],
  "edo.village.bay.use.mom": ["narrator", "Mom isn't going wading. She has one pair of shoes in this century, and they're on her feet."],
  "edo.village.bay.use.bigsis": ["narrator", "It's April, and Big Sister doesn't need to put a hand in the bay to know it's cold."],
  "edo.village.bay.use.lilsis": ["narrator", "Little Sister puts one toe in the bay. The toe reports that it's freezing, and comes straight back out."],
  // Gonroku's freighter at anchor, its one sail furled
  "edo.village.ship.mom": ["narrator", "A ship lies at anchor out in the bay, with one tall mast and its great sail rolled up."],
  "edo.village.ship.bigsis": ["narrator", "A ship lies at anchor out in the bay, with one tall mast and its great sail rolled up."],
  "edo.village.ship.lilsis": ["narrator", "A ship lies at anchor out in the bay, with one tall mast and its great sail rolled up."],
  "edo.village.ship.use.mom": ["narrator", "The ship is half a mile out. It will have a captain, though, and captains have wives."],
  "edo.village.ship.use.bigsis": ["narrator", "Big Sister has trouble hailing a bus. A ship half a mile out is beyond her."],
  "edo.village.ship.use.lilsis": ["narrator", "Little Sister shouts hello to the ship. It's half a mile out, and it doesn't answer."],
  // the boats on their props, and the gap under one
  "edo.village.boats.mom": ["narrator", "Fishing boats, pulled up on wooden props above the tide like shoes left by a door."],
  "edo.village.boats.bigsis": ["narrator", "Fishing boats on props. Under the big one is a gap that any seven-year-old would notice."],
  "edo.village.boats.lilsis": ["narrator", "Fishing boats up on props. There's a gap under the big one, and Little Sister noticed it before anybody."],
  "edo.village.boats.use.mom": ["narrator", "The boats aren't the family's, and they aren't going anywhere this morning."],
  "edo.village.boats.use.bigsis": ["narrator", "Big Sister decides against pushing a stranger's boat into the sea. That kind of thing gets written down."],
  "edo.village.boats.use.lilsis": ["narrator", "Little Sister pushes the boat as hard as she can. It doesn't move an inch."],
  "edo.village.underboat.mom": ["narrator", "A low gap under the big boat, in the shade. Mom knows exactly which daughter is looking at it."],
  "edo.village.underboat.bigsis": ["narrator", "A gap under the boat, all sand, shade and barnacles. It's a crawl space with a sea view."],
  "edo.village.underboat.lilsis": ["narrator", "A gap under the big boat, exactly Little Sister's size. Most good places are."],
  "edo.village.underboat.use.mom": ["narrator", "Mom doesn't crawl under boats. She has a daughter who does it for the whole family."],
  "edo.village.underboat.use.bigsis": ["narrator", "Big Sister would fit under the boat, just. She chooses not to find out."],
  "edo.village.underboat.use.lilsis": ["narrator", "Little Sister crawls under and comes out again. There's nothing under there but sand and one crab, now a friend."],
  // the net racks, and O-Masa at them
  "edo.village.nets.mom": ["narrator", "Fishing nets drying on bamboo racks. The woman mending them doesn't miss a thing on this beach."],
  "edo.village.nets.bigsis": ["narrator", "Fishing nets on drying racks. A net is mostly holes, well organized, which Big Sister finds encouraging."],
  "edo.village.nets.lilsis": ["narrator", "Nets hung up to dry, like a giant spiderweb for fish."],
  "edo.village.nets.use.mom": ["narrator", "They're the net woman's work, and Mom wouldn't put a finger on another woman's work."],
  "edo.village.nets.use.bigsis": ["narrator", "Big Sister keeps her hands off the nets. She once tangled a phone charger inside a closed drawer."],
  "edo.village.nets.use.lilsis": ["narrator", "Little Sister gets a boot caught in the net, and gets it out again before anyone sees."],
  // the notice-board place at the village entrance: boards of dense writing under a little roof. Before Sankichi reads it:
  "edo.village.board.mom": ["narrator", "A board of notices with its own little roof. A town that puts a roof on its rules means them."],
  "edo.village.board.bigsis": ["narrator", "A notice board, covered in columns of brush writing. Big Sister can't read a single character of it."],
  "edo.village.board.bigsis.2": ["narrator", "For the first time since she was four, she can't read. She doesn't care for it at all."],
  "edo.village.board.lilsis": ["narrator", "Wooden signs, covered in writing. For once not even Big Sister knows what they say."],
  "edo.village.board.use.mom": ["narrator", "Mom can't read the board and won't pretend to. The boy standing beside it can."],
  "edo.village.board.use.bigsis": ["narrator", "Big Sister stares at the board, and it stays unreadable. The boy beside it can read it."],
  "edo.village.board.use.lilsis": ["narrator", "Little Sister can't read the board either. The boy next to it can, and boys who can read love being asked."],
  // after Sankichi has read the Kirishitan board (edo.boardRead)
  "edo.village.board2.mom": ["narrator", "The oldest board, on the left. It promises silver for telling on people who pray as the family does."],
  "edo.village.board2.bigsis": ["narrator", "The Kirishitan board. Big Sister puts it at a hundred and nineteen years old."],
  "edo.village.board2.bigsis.2": ["narrator", "She can't read it, so that is a guess. She allows herself one."],
  "edo.village.board2.lilsis": ["narrator", "The mean sign, the one about people who pray. Little Sister looks at it again, and it's still mean."],
  "edo.village.board2.use.mom": ["narrator", "Mom leaves the board exactly as it is. It isn't hers to answer."],
  "edo.village.board2.use.bigsis": ["narrator", "Big Sister doesn't touch a government notice in a country where she can't read the small print."],
  "edo.village.board2.use.lilsis": ["narrator", "Little Sister won't touch the mean sign. She pats its little roof instead, which has done nothing wrong."],
  // the roofs, weighted with stones
  "edo.village.roofs.mom": ["narrator", "Wooden shingle roofs, with stones laid on them to hold them down. Mom likes these people already."],
  "edo.village.roofs.bigsis": ["narrator", "Shingle roofs weighted with stones against the wind. Somebody here has thought hard about weather."],
  "edo.village.roofs.lilsis": ["narrator", "There are rocks on all the roofs. Little Sister would like to know how they got up there."],
  "edo.village.roofs.use.mom": ["narrator", "Mom doesn't climb roofs. She has a daughter who would, and she isn't about to suggest it."],
  "edo.village.roofs.use.bigsis": ["narrator", "The stones are holding the roofs down, and Big Sister lets them get on with it."],
  "edo.village.roofs.use.lilsis": ["narrator", "Little Sister can't reach a single rock. Mom has said no in any case."],
  // smoke from a kitchen
  "edo.village.smoke.mom": ["narrator", "Woodsmoke rises from the roofs. Somebody is cooking breakfast, and Mom wishes it were hers."],
  "edo.village.smoke.bigsis": ["narrator", "Smoke rises straight up from the roofs. There's no wind yet, which matters to sailors."],
  "edo.village.smoke.lilsis": ["narrator", "Smoke, which means food. Little Sister can smell it from here, and it's fish."],
  "edo.village.smoke.use.mom": ["narrator", "There isn't much Mom can do with smoke but follow it to breakfast."],
  "edo.village.smoke.use.bigsis": ["narrator", "Big Sister studies the smoke for information. There isn't any, which has been the pattern all morning."],
  "edo.village.smoke.use.lilsis": ["narrator", "Little Sister takes a long sniff of the smoke. It's fish, just as she said."],
  // the hen yard, behind a low fence: every hen facing west along the coast
  "edo.village.hens.mom": ["narrator", "Five hens at the fence, every one facing the same way. Mom has seen hens do this before, in Nevada."],
  "edo.village.hens.bigsis": ["narrator", "Five hens in a row at the fence, every one facing west. Big Sister refuses to comment."],      // SCENES-20A: "Six": the yard has five (PAINT-20A; her names for them, edo.west.bye.6)
  "edo.village.hens.lilsis": ["narrator", "Five hens at the fence, all looking the same way. Little Sister knows that chickens know things."],
  "edo.village.hens.use.mom": ["narrator", "The hens pay Mom no attention at all. They seem to be waiting for somebody shorter."],
  "edo.village.hens.use.bigsis": ["narrator", "The hens ignore Big Sister. No hen has ever listened to her, and she has stopped taking it personally."],
  "edo.village.hens.use.lilsis": ["lilsis", "Hi, chickens, it's me. What are you all looking at?"],
  "edo.village.fence.mom": ["narrator", "A low bamboo fence around the hen yard. A hen could step over it, and not one of them has."],
  "edo.village.fence.bigsis": ["narrator", "A low fence around the hen yard. It isn't keeping anything in so much as marking a line."],
  "edo.village.fence.lilsis": ["narrator", "A fence around the hen yard, exactly Little Sister's height. She takes it as an invitation."],
  "edo.village.fence.use.mom": ["narrator", "Mom stays on her own side of the fence. The hens look busy."],
  "edo.village.fence.use.bigsis": ["narrator", "Big Sister could step over the fence, but the hens would have opinions about it."],
  "edo.village.fence.use.lilsis": ["narrator", "Little Sister leans on the fence with both elbows, which is what a fence is for."],
  // the cherry by the shrine path, past its best, dropping petals
  "edo.village.cherry.mom": ["narrator", "A cherry tree, nearly finished blooming. Its petals come down like the end of a play."],
  "edo.village.cherry.bigsis": ["narrator", "A cherry tree just past its best. Cherries bloom here at the start of April, so Big Sister makes it April."],
  "edo.village.cherry.lilsis": ["narrator", "A cherry tree, snowing pink petals. Some land in Little Sister's hair, and she keeps them."],
  "edo.village.cherry.use.mom": ["narrator", "Mom won't shake the tree. It has few enough petals left."],
  "edo.village.cherry.use.bigsis": ["narrator", "Big Sister gives the trunk a small shake and counts what falls. About forty petals."],
  "edo.village.cherry.use.lilsis": ["narrator", "Little Sister shakes the tree, and it snows pink on everybody."],
  "edo.village.shrinepath.mom": ["narrator", "A little path up the slope, swept this morning. It leads to somebody's holy place."],
  "edo.village.shrinepath.bigsis": ["narrator", "A swept path leading up to a village shrine. It isn't the family's to climb."],
  "edo.village.shrinepath.lilsis": ["narrator", "A path going up the hill into the trees. Little Sister wants to know where it goes."],
  "edo.village.shrinepath.use.mom": ["narrator", "Mom keeps to the street. The family are guests here, and that path isn't theirs."],
  "edo.village.shrinepath.use.bigsis": ["narrator", "Big Sister looks up the path from the bottom, which can't offend anyone."],
  "edo.village.shrinepath.use.lilsis": ["narrator", "Little Sister goes up three steps, remembers what Mom said, and comes back down."],
  // the gulls
  "edo.village.gulls.mom": ["narrator", "Gulls, wheeling over the boats. They sound exactly like the gulls at home."],
  "edo.village.gulls.bigsis": ["narrator", "Gulls over the beach, sounding like gulls anywhere. It's the first thing here Big Sister can read."],
  "edo.village.gulls.lilsis": ["narrator", "Seagulls over the boats. They aren't chickens, but Little Sister can see they're trying."],
  "edo.village.gulls.use.mom": ["narrator", "Mom has nothing to feed the gulls, and the gulls seem to know it."],
  "edo.village.gulls.use.bigsis": ["narrator", "The gulls stay well out of Big Sister's reach, and keep an eye on her pockets."],
  "edo.village.gulls.use.lilsis": ["narrator", "Little Sister waves at the gulls. One of them tips a wing, and she counts that as a wave."],
  // Kihei's shop front, and its curtain (the noren) lifting in the wind
  "edo.village.shop.mom": ["narrator", "A fish shop, open to the street, with a short curtain for a door. It looks like the place to ask."],
  "edo.village.shop.bigsis": ["narrator", "A fish shop with a curtain across its doorway. There's writing on the curtain, and Big Sister can say it's blue."],
  "edo.village.shop.lilsis": ["narrator", "A shop with a curtain where the door should be. Anybody can just walk through it."],
  "edo.village.shop.use.mom": ["mom", "Heads down under the curtain, girls. We're going in politely."],
  "edo.village.shop.use.bigsis": ["narrator", "Big Sister ducks in under a curtain she can't read. That makes two things this morning."],
  "edo.village.shop.use.lilsis": ["narrator", "Little Sister walks in under the curtain without needing to duck. The shop smells of fish, the good kind."],
  // the road: the Tōkaidō, along the shore; and the Satta pass rising to the west
  "edo.village.road.mom": ["narrator", "A road along the shore, running off both ways. That's one more direction than Nevada had."],
  "edo.village.road.bigsis": ["narrator", "A road with real traffic on it: a man, a hat, a horse. Big Sister takes it for the main road."],
  "edo.village.road.lilsis": ["narrator", "A dirt road along the shore. Little Sister checks, and it isn't the road home."],
  "edo.village.road.use.mom": ["narrator", "Mom isn't walking anywhere until the family knows which way to go."],
  "edo.village.road.use.bigsis": ["narrator", "Big Sister won't set off down a road without knowing which direction is the right one."],
  "edo.village.road.use.lilsis": ["narrator", "Little Sister walks five steps along the road and comes back. Somebody should ask the chickens which way."],
  "edo.village.pass.mom": ["narrator", "The road climbs over a hill at the west end of the bay and drops out of sight."],
  "edo.village.pass.bigsis": ["narrator", "A pass, where the road goes up and over the hill. The view from the top is probably famous."],
  "edo.village.pass.lilsis": ["narrator", "A hill with the road going up it. Little Sister is fairly sure there's a snack at the top."],
  "edo.village.pass.use.mom": ["narrator", "It's a long climb, and Mom isn't starting it until she knows it's the right way."],
  "edo.village.pass.use.bigsis": ["narrator", "Big Sister will climb it when somebody can tell her what's on the other side."],
  "edo.village.pass.use.lilsis": ["narrator", "Little Sister starts up the hill. Mom says not without her, so she comes back and waits."],
  // the well
  "edo.village.well.mom": ["narrator", "The village well, with a bucket on a rope. Everyone here drinks from the same place."],
  "edo.village.well.bigsis": ["narrator", "A well with a bucket, a rope and a pulley. It's the oldest machine Big Sister knows how to work."],
  "edo.village.well.lilsis": ["narrator", "A well, deep and dark. Little Sister shouts into it, and it shouts back."],
  "edo.village.well.use.mom": ["narrator", "Mom wouldn't draw from someone else's well without asking. The woman with the basket would know."],
  "edo.village.well.use.bigsis": ["narrator", "Big Sister draws half a bucket and lowers it again. She isn't thirsty enough to be rude."],
  "edo.village.well.use.lilsis": ["narrator", "Little Sister hauls on the rope. The bucket is heavier than she is, and it wins."],
  // the sand
  "edo.village.sand.mom": ["narrator", "Gray sand, and three sets of footprints that nobody in Yui will recognize."],
  "edo.village.sand.bigsis": ["narrator", "Gray sand. The family's footprints begin in a small circle where the door was, with nothing behind them."],
  "edo.village.sand.lilsis": ["narrator", "Gray sand, with three sets of footprints in it. The ones from the yellow boots are plainly the best."],
  "edo.village.sand.use.mom": ["narrator", "There are no sandcastles today. The family has somewhere to be, even if Mom doesn't yet know where."],
  "edo.village.sand.use.bigsis": ["narrator", "Big Sister starts to write the date in the sand, and remembers she doesn't know it."],
  "edo.village.sand.use.lilsis": ["narrator", "Little Sister draws a chicken in the sand. It's a good one, and she leaves it for the sea."],
  // the villagers: a net-mender, and the woman with the basket
  "edo.village.netmender.mom": ["narrator", "An old man mending a net, trying hard not to stare at the family. He isn't good at it."],
  "edo.village.netmender.bigsis": ["narrator", "An old man mending a net. He has looked at the family eleven times and tied one knot."],
  "edo.village.netmender.lilsis": ["narrator", "An old man mending a net, holding it tight with his toes. Little Sister wants to learn how."],
  "edo.village.netmender.say.1": ["netmender", "Good morning. It's a big morning for Yui: big strangers, and the same old mountain."],
  "edo.village.netmender.say.2": ["netmender", "Forty years on this beach, and the mountain has never once surprised me. You three did."],
  "edo.village.netmender.say.3": ["netmender", "Go and ask Kihei, the fishmonger. He feeds everybody. Ask him before his wife asks you."],
  "edo.village.basketwoman.mom": ["narrator", "The woman who dropped her basket on the beach. She has come back for it, and for a second look."],
  "edo.village.basketwoman.bigsis": ["narrator", "The woman who dropped her basket at the sight of them. Big Sister can't say she blames her."],
  "edo.village.basketwoman.lilsis": ["narrator", "The basket lady, back again. Little Sister knew she'd come back."],
  "edo.village.basketwoman.say.1": ["basketwoman", "That's my basket, and thank you for not taking it. Most people would say something now."],
  "edo.village.basketwoman.say.2": ["basketwoman", "The tall one is taller than my husband. Don't tell him so. He's proud of his height."],
  "edo.village.basketwoman.say.3": ["basketwoman", "Kihei's wife will have you in kimonos before the fish is cut. Let her."],
  // Sankichi, beside the board; Tokuzō on his rounds; Gonroku by his boat; O-Masa at the racks; Kihei, when he is out front
  "edo.village.sankichi.mom": ["narrator", "A boy of about nine beside the notice boards, reading them aloud to anyone who stands still."],
  "edo.village.sankichi.bigsis": ["narrator", "A boy of about nine, reading the notice boards aloud. Big Sister has never envied anyone more."],
  "edo.village.sankichi.lilsis": ["narrator", "A boy by the signs, about the Son's size. He can't take his eyes off the yellow boots."],
  "edo.village.tokuzo.mom": ["narrator", "A clerk with a brush and a paper, going from door to door and squinting hard at each one."],
  "edo.village.tokuzo.bigsis": ["narrator", "A clerk with a brush and a paper, going from door to door and squinting hard at each one."],
  "edo.village.tokuzo.lilsis": ["narrator", "A clerk with a brush and a paper, going from door to door and squinting hard at each one."],
  "edo.village.gonroku.mom": ["narrator", "The ship's captain, standing by his boat at the water's edge. He looks at the sky as if it owed him money."],
  "edo.village.gonroku.bigsis": ["narrator", "The ship's captain, by his boat. He has been reading the sky for an hour and doesn't like how it ends."],
  "edo.village.gonroku.lilsis": ["narrator", "The captain, by his boat, frowning at the sky. Little Sister can't see what the sky did wrong."],
  "edo.village.masa.mom": ["narrator", "The woman mending nets at the racks. Everyone on the beach glances at her before doing anything."],
  "edo.village.masa.bigsis": ["narrator", "The woman at the net racks. The captain has glanced at her twice, and she hasn't looked back once."],
  "edo.village.masa.lilsis": ["narrator", "The net lady. She never looks up, which is how Little Sister can tell she's the boss of the beach."],
  "edo.village.kihei.mom": ["narrator", "The fishmonger, in front of his shop in a red vest and a red hood. Somebody makes him wear them."],
  "edo.village.kihei.bigsis": ["narrator", "The fishmonger, in a red vest and hood in April. Big Sister is sure there's a reason for the red."],
  "edo.village.kihei.lilsis": ["narrator", "The fish man, in a red hood, looking grumpy. In Little Sister's experience, grumpy people give the best food."],

  // ======================================================================================================
  // THE SHOP (edo-fishshop): inside Kihei's. The looks, and the uses, for each thing, for each of the three.
  // ======================================================================================================
  // Kihei at his cutting board
  "edo.shop.kihei.mom": ["narrator", "Kihei, the fishmonger, with big hands and very few words. He has made up his mind about the family already."],
  "edo.shop.kihei.bigsis": ["narrator", "Kihei, the fishmonger, in his red hood. He has said very little since they came in, and most of it was \"Sit.\""],
  "edo.shop.kihei.lilsis": ["narrator", "Kihei, the fish man. He hasn't smiled once, and Little Sister has made that her project."],
  // O-Tami at her place (with the baby on her back, until it sleeps); married, teeth blackened: Big Sister's fact
  "edo.shop.tami.mom": ["narrator", "O-Tami runs this shop, that man and a baby, and still has an eye to spare for three strangers."],
  "edo.shop.tami.bigsis": ["narrator", "O-Tami, the fishmonger's wife. Her teeth are blackened, as married women's are here. Big Sister had read of it."],
  "edo.shop.tami.lilsis": ["narrator", "O-Tami, the baby lady. She talks very fast, and so does Little Sister, so they get along."],
  // the baby, on O-Tami's back (awake and fussing); then asleep in its basket
  "edo.shop.baby.mom": ["narrator", "A baby who hasn't slept, tied on the back of a mother who hasn't either."],      // SCENES-20A: "in a basket": she is on O-Tami's back till she sleeps
  "edo.shop.baby.bigsis": ["narrator", "A baby on O-Tami's back. She isn't crying yet. She's thinking about it, out loud."],
  "edo.shop.baby.lilsis": ["narrator", "A baby, wide awake. Little Sister would like to hold her, and carried an egg across Nevada to prove she can."],
  "edo.shop.baby.use.mom": ["mom", "May I? Come here, little one, and we'll see about this."],
  "edo.shop.baby.use.bigsis": ["narrator", "Big Sister has nothing to offer a baby but a book, and no book. Babies are best left to Mom."],
  "edo.shop.baby.use.lilsis": ["narrator", "Little Sister makes her chicken face. The baby stops fussing to stare, then starts again. It's a job for Mom."],
  "edo.shop.baby2.mom": ["narrator", "The baby, asleep in her basket. She dropped off in the middle of her mother's sentence."],
  "edo.shop.baby2.bigsis": ["narrator", "The baby, asleep. Mom hummed four bars and the whole shop went quiet, the cat included."],
  "edo.shop.baby2.lilsis": ["narrator", "The baby, fast asleep. Mom did that, and Little Sister believes she could do it to anybody."],
  "edo.shop.baby2.use.mom": ["narrator", "The baby is asleep at last, and nobody in the family would wake her for anything on this earth."],
  "edo.shop.baby2.use.bigsis": ["narrator", "The baby is asleep at last, and nobody in the family would wake her for anything on this earth."],
  "edo.shop.baby2.use.lilsis": ["narrator", "The baby is asleep at last, and nobody in the family would wake her for anything on this earth."],
  // the cat, at her place; and once she has gone under the floor with the mackerel
  "edo.shop.cat.mom": ["narrator", "A cat, watching the cutting board the way Dad watches a grill."],
  "edo.shop.cat.bigsis": ["narrator", "A cat with her eye on the mackerel. She has a plan, as cats generally do."],
  "edo.shop.cat.lilsis": ["narrator", "A cat by the cutting board. She isn't a chicken, but Little Sister likes her face."],
  "edo.shop.cat.use.mom": ["narrator", "Mom leaves the cat where she is. That is a cat with work to do."],
  "edo.shop.cat.use.bigsis": ["narrator", "Big Sister holds out a hand. The cat considers it and declines."],
  "edo.shop.cat.use.lilsis": ["narrator", "Little Sister strokes the cat once. The cat allows it, once."],
  "edo.shop.cat2.mom": ["narrator", "The cat has gone under the raised floor with the family's lunch. Mom has to admire her nerve."],
  "edo.shop.cat2.bigsis": ["narrator", "The cat is under the raised floor with a whole mackerel. It was a good plan, and it worked."],
  "edo.shop.cat2.lilsis": ["narrator", "The cat went under the floor with the fish. Little Sister looks at the gap. It's exactly her size."],
  // the tubs of fish
  "edo.shop.tubs.mom": ["narrator", "Wooden tubs of live fish in water. One of them keeps jumping, and Mom would rather it didn't."],
  "edo.shop.tubs.bigsis": ["narrator", "Tubs of live mackerel. \"Saba\" is the most useful of Big Sister's forty words of Japanese, all of them food."],
  "edo.shop.tubs.lilsis": ["narrator", "Tubs of live fish. One keeps jumping, and Little Sister has named him Jumpy."],
  "edo.shop.tubs.use.mom": ["narrator", "Mom keeps her hands out of the fish tubs. She has standards, and no towel."],
  "edo.shop.tubs.use.bigsis": ["narrator", "Big Sister touches one fish with one finger. Both of them would rather not repeat it."],
  "edo.shop.tubs.use.lilsis": ["narrator", "Little Sister tries to pet Jumpy. Jumpy jumps, which is the only thing he does."],
  // the cutting board, and the mackerel on it
  "edo.shop.cuttingboard.mom": ["narrator", "A long cutting board, worn hollow, and a knife Mom means to stay well away from."],
  "edo.shop.cuttingboard.bigsis": ["narrator", "A cutting board worn into a valley down the middle by decades of mackerel."],
  "edo.shop.cuttingboard.lilsis": ["narrator", "The board where Kihei chops the fish. Little Sister isn't allowed near chopping, and is near it."],
  "edo.shop.cuttingboard.use.mom": ["narrator", "The board and the knife are Kihei's, and the knife is sharp. Mom leaves both alone."],
  "edo.shop.cuttingboard.use.bigsis": ["narrator", "Big Sister doesn't touch other people's knives. It is one of her better rules."],
  "edo.shop.cuttingboard.use.lilsis": ["narrator", "Little Sister reaches for the fish. Kihei makes a low noise in his throat, and she stops."],
  // the wooden sushi box and its press
  "edo.shop.sushibox.mom": ["narrator", "A wooden box with a lid that fits down inside it. Mom would say it's for pressing something."],
  "edo.shop.sushibox.bigsis": ["narrator", "A box, a lid and a weight stone: a press. Whatever it makes, it makes it flat."],
  "edo.shop.sushibox.lilsis": ["narrator", "A little wooden box with a lid. Little Sister wonders if it's a bed for the fish."],
  "edo.shop.sushibox.use.mom": ["narrator", "Mom would only press the wrong thing. Better to watch the man who knows how."],
  "edo.shop.sushibox.use.bigsis": ["narrator", "Big Sister presses the lid down on nothing. The box wants rice, fish and a grown man's weight."],
  "edo.shop.sushibox.use.lilsis": ["narrator", "Little Sister pushes the lid down. Nothing happens, because the box needs fish in it first."],
  // the hearth and its pot
  "edo.shop.hearth.mom": ["narrator", "A fire sunk in the floor, with a pot of rice over it. It's somebody's breakfast."],
  "edo.shop.hearth.bigsis": ["narrator", "A hearth sunk in the floor, with a pot of rice over it. Vinegared rice, by the smell."],
  "edo.shop.hearth.lilsis": ["narrator", "A fire right in the floor, with a pot on it. It smells of rice and something sour."],
  "edo.shop.hearth.use.mom": ["narrator", "Mom doesn't stir another woman's pot. The family will be offered some, or they won't."],
  "edo.shop.hearth.use.bigsis": ["narrator", "Big Sister warms her hands at the hearth. That is everything she knows how to do with it."],
  "edo.shop.hearth.use.lilsis": ["narrator", "Little Sister warms her hands, and then her boots. The boots begin to smell a little, so she stops."],
  // the fish hung to dry
  "edo.shop.driedfish.mom": ["narrator", "Fish hung up to dry in rows, like washing nobody wants to wear."],
  "edo.shop.driedfish.bigsis": ["narrator", "Dried fish on strings, bonito perhaps. Big Sister would know for certain if they came with rice."],
  "edo.shop.driedfish.lilsis": ["narrator", "Flat dried fish on strings. Every one of them looks surprised."],
  "edo.shop.driedfish.use.mom": ["narrator", "The dried fish aren't the family's, and Mom doubts they're anyone's idea of breakfast."],
  "edo.shop.driedfish.use.bigsis": ["narrator", "Big Sister taps one with a knuckle. It's as hard as a shoe."],
  "edo.shop.driedfish.use.lilsis": ["narrator", "Little Sister pokes one, and the whole row swings like a wind chime made of fish."],
  // the print of Fuji pinned up, in the new blue (a design of the game's own): #21's third clue
  "edo.shop.print.mom": ["narrator", "A picture of the mountain, pinned to the post. Its blue is the bluest thing in the room."],
  "edo.shop.print.bigsis": ["narrator", "A woodblock print of Fuji under a deep blue sky, pinned to the post. That blue is not an old blue."],
  "edo.shop.print.lilsis": ["narrator", "A picture of the big mountain, pinned to the post. It's bluer than the real one."],
  "edo.shop.print.use.mom": ["narrator", "Mom won't take a man's picture off his wall. It looks well where it hangs."],
  "edo.shop.print.use.bigsis": ["narrator", "Big Sister looks closer. It's printed, not painted, so somebody made hundreds of these."],
  "edo.shop.print.use.lilsis": ["narrator", "Little Sister touches the blue. None of it comes off on her finger."],
  // Kihei's word for it, the first time any of them looks (the scene says it once), and Big Sister's fact
  "edo.shop.print.kihei": ["kihei", "Everybody in Edo wants pictures of the mountain this year, in that new blue."],
  "edo.shop.print.clue": ["bigsis", "He said new. That's Prussian blue, and their printers have only just got it."],
  "edo.shop.print.clue.2": ["bigsis", "So it's a picture printed in a blue that's new this year. That narrows things down."],
  // the money box: strings of square-holed copper coins: #21's second clue
  "edo.shop.money.mom": ["narrator", "A box of copper coins on strings, each with a square hole. It is money that's carried on a cord."],
  "edo.shop.money.bigsis": ["narrator", "Copper coins with square holes, strung on cords. Big Sister has seen one like them in a museum case."],
  "edo.shop.money.lilsis": ["narrator", "Money with holes in it, like breakfast cereal. Little Sister has already checked whether it can be eaten."],
  "edo.shop.money.use.mom": ["narrator", "It's another man's money box. Mom looks, and doesn't touch."],
  "edo.shop.money.use.bigsis": ["narrator", "Big Sister isn't touching Kihei's money. She's barely touching his floor."],
  "edo.shop.money.use.lilsis": ["narrator", "Little Sister doesn't touch the money. She wants to, but wanting is free."],
  "edo.shop.money.clue": ["bigsis", "Kan'ei Tsūhō. The museum label said Edo period: the 1630s to the 1860s."],
  "edo.shop.money.clue.2": ["bigsis", "So it's a tiger year, in the Edo period. We're narrowing it down, slowly."],
  // the god-shelf, high on the wall
  "edo.shop.godshelf.mom": ["narrator", "A little shelf high on the wall, kept very clean. It belongs to the house, and Mom lets it be."],
  "edo.shop.godshelf.bigsis": ["narrator", "A small shelf high on the wall, for the household's god. Big Sister won't touch it."],
  "edo.shop.godshelf.bigsis.2": ["narrator", "It isn't hers, and she can't read what is written on it."],
  "edo.shop.godshelf.lilsis": ["narrator", "A tiny shelf up high, with nothing on it but a cup. Little Sister wonders if it's for the cat."],
  "edo.shop.godshelf.use.mom": ["narrator", "The shelf isn't the family's, and Mom won't pretend that it is."],
  "edo.shop.godshelf.use.bigsis": ["narrator", "Big Sister leaves the shelf alone. It isn't hers to touch."],
  "edo.shop.godshelf.use.lilsis": ["narrator", "The shelf is far too high for Little Sister to reach, and it isn't hers in any case."],
  // the raised room at the back, with its step, where guests are fed
  "edo.shop.step.mom": ["narrator", "A raised floor of straw mats, with a wooden step up to it. Shoes come off there, Mom guesses."],
  "edo.shop.step.bigsis": ["narrator", "A step up to a room floored with straw mats. Every pair of shoes in the house stops at the step."],
  "edo.shop.step.lilsis": ["narrator", "A wooden step up to the room with the mats. It's exactly the right height for sitting on."],
  "edo.shop.step.use.mom": ["narrator", "Mom will sit when she's asked to, and not before."],
  "edo.shop.step.use.bigsis": ["narrator", "Big Sister hasn't been invited to sit, so she stands."],
  "edo.shop.step.use.lilsis": ["narrator", "Little Sister sits down on the step. Nobody says no, and the cat comes and sits beside her."],
  // the open front: the street, the bay, Fuji in the opening
  "edo.shop.street.mom": ["narrator", "The whole front of the shop is open to the street, like a window with no glass. Anyone can see in."],
  "edo.shop.street.bigsis": ["narrator", "The street, the bay and Fuji, framed by the shop front. Everyone passing gets the picture, with the family in it."],
  "edo.shop.street.lilsis": ["narrator", "The open front of the shop, with the mountain in it. Little Sister thinks it's the best wall she's ever seen."],
  "edo.shop.street.use.mom": ["narrator", "Mom keeps back from the street. The family is conspicuous enough already."],
  "edo.shop.street.use.bigsis": ["narrator", "Standing in the shop front would be like standing on a stage, and Big Sister isn't dressed for one."],
  "edo.shop.street.use.lilsis": ["narrator", "Little Sister waves at the street. A man out there squints at her, and she comes back in."],
  // the noren, from inside
  "edo.shop.noren.mom": ["narrator", "The shop's door curtain, seen from behind. It's the only thing in here that moves and isn't a fish."],
  "edo.shop.noren.bigsis": ["narrator", "The door curtain, from the back. Big Sister can't read it backwards either."],
  "edo.shop.noren.lilsis": ["narrator", "The curtain door. Little Sister found out early how well a person can hide behind it."],
  "edo.shop.noren.use.mom": ["narrator", "Beyond the curtain is the street, and in the street is a clerk with a paper. Mom leaves it closed."],
  "edo.shop.noren.use.bigsis": ["narrator", "Big Sister looks out through the gap in the curtain. Nobody looks back, which is the idea."],
  "edo.shop.noren.use.lilsis": ["narrator", "Little Sister peeks through the curtain. The clerk is out there, squinting at a wall."],
  // the straw sandals hung for sale; the sedge hats
  "edo.shop.sandals.mom": ["narrator", "Straw sandals, hung up in pairs for sale to travellers."],
  "edo.shop.sandals.bigsis": ["narrator", "Straw sandals, flat and tied on with cord. A pair wouldn't last a week of walking."],
  "edo.shop.sandals.lilsis": ["narrator", "Shoes made of straw. Little Sister's are made of boot, and she knows which she prefers."],
  "edo.shop.sandals.use.mom": ["narrator", "Mom would buy a pair if she had a coin with a hole in it. The family has three pennies with none."],      // SCENES-20A: "I have": the three pennies are Little Sister's (Mom says only what is so)
  "edo.shop.sandals.use.bigsis": ["narrator", "Big Sister holds one against her foot. Her sneaker is from another century, and it shows."],
  "edo.shop.sandals.use.lilsis": ["narrator", "Little Sister isn't swapping her yellow boots for anything made of straw."],
  "edo.shop.hats.mom": ["narrator", "Wide hats of woven sedge. Whoever is under one of those is nobody's business."],
  "edo.shop.hats.bigsis": ["narrator", "Wide sedge hats, each one a small roof. Under one, a person could be anybody."],
  "edo.shop.hats.lilsis": ["narrator", "Hats like upside-down bowls. Little Sister wants the biggest."],
  "edo.shop.hats.use.mom": ["narrator", "Mom would be glad of a hat, and gladder if one were offered. She doesn't help herself."],
  "edo.shop.hats.use.bigsis": ["narrator", "Big Sister tries one on and is nobody in particular. She could get used to it. She hangs it back up."],
  "edo.shop.hats.use.lilsis": ["narrator", "Little Sister tries one on. It comes down to her chin, and all she can see is her own boots."],
  // O-Tami's clothes chest
  "edo.shop.chest.mom": ["narrator", "A clothes chest, closed. Whatever is in it was folded by someone who takes care."],
  "edo.shop.chest.bigsis": ["narrator", "A wooden chest that smells of cedar. Old clothes, Big Sister would say, kept for a reason."],
  "edo.shop.chest.lilsis": ["narrator", "A big wooden chest. It isn't treasure, only clothes, though Little Sister holds out some hope."],
  "edo.shop.chest.use.mom": ["narrator", "Another woman's chest stays shut until she opens it herself. O-Tami might, if the family is patient."],
  "edo.shop.chest.use.bigsis": ["narrator", "Big Sister doesn't open other people's drawers, and a chest is a large drawer. It's O-Tami's to open."],
  "edo.shop.chest.use.lilsis": ["narrator", "Little Sister lifts the lid one inch. O-Tami looks at her, and she puts it down again."],
  // the gap under the raised floor: the cat's way, and Little Sister's
  "edo.shop.under.mom": ["narrator", "A gap under the raised floor, dark and dusty. The cat considers it hers."],
  "edo.shop.under.bigsis": ["narrator", "A gap under the raised floor. It's cat-sized, and also, Big Sister notes, sister-sized."],
  "edo.shop.under.lilsis": ["narrator", "A gap under the floor. Little Sister hasn't tried it yet, but she knows she'd fit."],
  "edo.shop.under.use.mom": ["narrator", "Mom is not going under a floor, and nothing down there gives her a reason to."],
  "edo.shop.under.use.bigsis": ["narrator", "Big Sister could get her head in. The rest of her would be the problem."],
  "edo.shop.under.use.lilsis": ["narrator", "Little Sister crawls in and backs out. There's nothing under there yet but dust and some old fish bones."],

  // ======================================================================================================
  // #22 OUT OF SIGHT, the scripted moments: the clerk's first pass (O-Tami pulls them in; the weather), the baby, the
  // kimonos, and Little Sister's boots. The clerk himself is tokuzoTree.
  // ======================================================================================================
  // (1) the first time Tokuzō turns into the street: O-Tami has the three of them in behind the noren in one movement
  "edo.shop.pass.1": ["tami", "In. In, in, in. Behind the curtain, all of you, and not a word."],
  "edo.shop.pass.2": ["lilsis", "Why are we--"],
  "edo.shop.pass.3": ["mom", "Because she asked us to, and she asked in a hurry."],
  // she stands in the opening, her back to them, and talks to the clerk about the weather until he has gone by
  "edo.shop.pass.4": ["tami", "Good morning, clerk, and a fine one. The wind has gone round to the west."],
  "edo.shop.pass.5": ["tokuzo", "Has it? So it has. Forgive me, O-Tami, but is there anything unusual on your street?"],
  "edo.shop.pass.6": ["tami", "Fish, clerk, and wind. The same as every morning since my grandmother's day."],
  "edo.shop.pass.7": ["tokuzo", "Fish and wind. I'll write \"nothing\", since it's shorter."],
  // his back goes past the opening; she turns round
  "edo.shop.pass.8": ["tami", "The headman has had a paper. Strangers on the beach at dawn, in strange clothes."],
  "edo.shop.pass.9": ["tami", "I don't know any strangers. I know three travellers who need proper clothes."],
  "edo.shop.pass.10": ["tami", "And I have a baby who hasn't slept in three days. Not one whole hour in three days."],
  "edo.shop.pass.11": ["mom", "Then one thing at a time, if you'll let us. Which shall it be first?"],
  "edo.shop.pass.12": ["tami", "Ask me again when I've slept."],
  // (2) the baby: Mom asks, and is handed the baby; she rocks her and hums a tune of her own, no words (a stage
  // direction, not a line); the baby sleeps in the middle of a sentence
  "edo.shop.baby.1": ["mom", "May I hold her? I've raised three, and my arms still remember how."],
  "edo.shop.baby.2": ["tami", "Take her, with my blessing. Take her as far as Edo, if she'll sleep there."],
  "edo.shop.baby.3": ["tami", "She won't have the hearth side, she won't have the street side, she won't--"],
  // asleep. O-Tami looks at Mom as at a sorceress
  "edo.shop.baby.4": ["tami", "What did you do?"],
  "edo.shop.baby.5": ["mom", "I only found her key. She's a quarter-tone flat, and so is my husband, bless him."],
  "edo.shop.baby.6": ["tami", "Don't stop humming, and don't ever leave. Now come to the chest."],
  // (3) the kimonos, from her chest: Mom in emerald, Big Sister in indigo, Little Sister in pink; hats; sandals for two
  "edo.shop.dress.1": ["tami", "These were my mother's. She wasn't your height, but then nobody is your height. Arms up."],
  "edo.shop.dress.2": ["mom", "Green. You've found me my own color, in a chest, in another century."],
  "edo.shop.dress.3": ["tami", "Indigo for the reader. It was long on me."],
  "edo.shop.dress.4": ["bigsis", "It ends at my knees."],
  "edo.shop.dress.5": ["tami", "Travellers tuck them up for the road anyway. You're only ahead of them."],
  "edo.shop.dress.6": ["tami", "Pink for the small one, and hats for all three. Keep your heads down under them."],
  "edo.shop.dress.7": ["tami", "Sandals. Fifteen mon a pair, and good for a day or two of road. Yours, and yours."],
  "edo.shop.dress.8": ["lilsis", "What about me?"],
  "edo.shop.dress.9": ["tami", "I've nothing small enough. Off with the yellow ones, then, and we'll wrap your feet."],
  "edo.shop.dress.10": ["lilsis", "They're my BOOTS."],
  "edo.shop.dress.11": ["tami", "So they are. Keep them; nobody who sees them will believe their eyes anyway."],
  "edo.shop.dress.12": ["mom", "Thank you. I mean that properly, and I'll be saying it again."],
  "edo.shop.dress.13": ["tami", "Three travellers. Now go and be travellers at the clerk, before I think better of it."],
  // the three of them, dressed, looked at (the scene swaps story.see for these once edo.clothes is set)
  "edo.see.mom.bigsis": ["narrator", "Big Sister, in borrowed indigo that stops at her knees. She is reading faces today, since she can't read the signs."],
  "edo.see.mom.lilsis": ["narrator", "Little Sister, in pink to the ankle with yellow boots underneath. Nobody who sees her will believe it."],
  "edo.see.bigsis.mom": ["narrator", "Mom, in green, a head taller than every woman in Yui. She has stopped apologizing for it."],
  "edo.see.bigsis.lilsis": ["narrator", "Little Sister, in a kimono and rain boots. She is in two centuries at once and happy in both."],
  "edo.see.lilsis.mom": ["narrator", "Mom, in a green kimono. It's a different green from the dress at home, but she's still Mom."],
  "edo.see.lilsis.bigsis": ["narrator", "Big Sister, in blue down to her knees. She says it's too short. Little Sister thinks it's exactly right."],
  // Little Sister in the street in her own clothes (before the kimonos: the wrong try)
  "edo.village.boots.lilsis": ["lilsis", "The boy says everybody's looking at my boots. I think they're just jealous."],
  "edo.village.boots.mom": ["mom", "Then we'd better give them something duller to look at. Inside, sweetheart."],
  // #22 solved (tokuzoTree's end): the three of them, after he has gone home
  "edo.dressed.1": ["bigsis", "\"From the east.\" That was true, Mom."],
  "edo.dressed.2": ["mom", "It was, every syllable. That's the only reason you got away with it."],
  "edo.dressed.3": ["lilsis", "He didn't look at my boots once. I don't think he can see his own feet."],

  // ======================================================================================================
  // #21 WHERE, AND WHEN: Big Sister's solution, once the three clues are in (the red, the coins, the blue), said by her
  // whoever is playing; and the sum written down, if Dad's pencil meets the sticky note (not needed).
  // ======================================================================================================
  "edo.when.solve.1": ["bigsis", "A metal tiger. They come round once every sixty years, and the last one was 2010."],
  "edo.when.solve.2": ["bigsis", "Take away sixty, then sixty, then sixty again. That's 1830."],
  "edo.when.solve.3": ["bigsis", "The Edo coins fit, and so does the new blue. It's 1830."],
  "edo.when.solve.4": ["lilsis", "Is 1830 good?"],
  "edo.when.solve.5": ["bigsis", "It's a year. A year is only a number until you know what happens in it."],
  "edo.when.solve.6": ["mom", "Then let's find out, girls. Politely, and one question at a time."],
  // the sum, written down with Dad's pencil on the sticky note (either on the other; any of the three can be holding them)
  "edo.when.sum.bigsis": ["bigsis", "2010, less sixty, less sixty, less sixty: 1830. Now that it's on paper, it's a fact."],
  "edo.when.sum.mom": ["mom", "Your father's pencil, a sticky note and a date. He'd be pleased with all three."],
  "edo.when.sum.lilsis": ["lilsis", "I wrote 1830. It's the best 1830 anybody's ever written, especially the 8."],
  // the sum tried before the clues are in
  "edo.when.sum.early": ["bigsis", "I'd write the year down if I had one. So far I have a pencil and a feeling."],

  // ======================================================================================================
  // #23 KIHEI'S TABLE, the scripted meal (kiheiTree's hook `press` and after): the pressing, the grace, the bow, the
  // word, the title, the cat, the box. Nobody says itadakimasu: they bow to the god-shelf and say nothing.
  // ======================================================================================================
  // the pressing: rice, fish, lid, his weight on it, the cut (the player watches; Big Sister watches aloud)
  "edo.shop.meal.1": ["kihei", "Sit. Watch if you like, but don't help."],
  "edo.shop.meal.2": ["lilsis", "I'm good at not helping. Ask my sister."],
  "edo.shop.meal.3": ["bigsis", "Rice goes into the box, fish on the rice, the lid on the fish. And now he just leans on it."],
  "edo.shop.meal.4": ["mom", "He's pressing it, like a flower in a book. Only this one you're allowed to eat."],
  "edo.shop.meal.5": ["bigsis", "Saba, that's mackerel. I know that one. It's pressed in a box and cut like a cake."],
  "edo.shop.meal.6": ["bigsis", "In Edo they've only lately begun making it by hand, one piece at a time."],
  // on the step, in front of them; and he will take nothing for it
  "edo.shop.meal.7": ["kihei", "Eat first. Money is for after, and there's no after for money today."],
  // Little Sister's grace, in her own words; Kihei and O-Tami wait, puzzled and polite
  "edo.shop.meal.8": ["lilsis", "Thank You for the fish, and for the fish man, and for his wife,"],
  "edo.shop.meal.9": ["lilsis", "and for the baby who's asleep now. Please keep her asleep. Amen."],
  // then they bow to the god-shelf, and say nothing, as their custom is
  "edo.shop.meal.10": ["mom", "Eat slowly, girls. ...All right, not slowly."],
  // Little Sister, with the word from Sankichi (edo.arigato); Kihei's face does something nobody has seen it do
  "edo.shop.meal.11": ["lilsis", "Arigatō."],
  "edo.shop.meal.11.tami": ["tami", "Husband, your face."],
  "edo.shop.meal.11.kihei": ["kihei", "It does that."],
  // without the word yet (she comes back with it later: kiheiTree's `arigato`)
  "edo.shop.meal.11b": ["lilsis", "Thank you, fish man. I'll learn to say it your way, and then I'll say it again."],
  // Mom thanks him properly; his answer gives the act its name, and Big Sister translates it once
  "edo.shop.meal.12": ["mom", "Thank you. You've fed three strangers who can't pay you, and you've asked us nothing."],
  "edo.shop.meal.13": ["kihei", "Okage-sama de."],
  "edo.shop.meal.14": ["bigsis", "It means \"thanks to you\". Or \"by your grace\", which I like better."],
  "edo.shop.meal.15": ["bigsis", "People say it when something good has happened that wasn't only their own doing."],
  // the cat takes a mackerel off the board and goes under the floor
  "edo.shop.meal.16": ["mom", "The cat has a mackerel."],
  "edo.shop.meal.17": ["kihei", "The cat always has a mackerel."],
  "edo.shop.meal.18": ["lilsis", "I can fit under there!"],
  // under, and back, with the fish and a cobweb: that is how the family pays, in kind, by choice, after
  "edo.shop.meal.19": ["lilsis", "Got it. And a cobweb, but the cobweb's free."],
  "edo.shop.meal.20": ["kihei", "Nobody has ever got one back from that cat."],
  "edo.shop.meal.21": ["mom", "There. We've paid our way after all, in fish."],
  "edo.shop.meal.22": ["kihei", "In my fish."],
  "edo.shop.meal.23": ["mom", "After. As you said."],
  // O-Tami wraps the rest for the road (the sushibox)
  "edo.shop.meal.24": ["tami", "The rest goes with you, and don't argue. I'm holding a baby, and I'll win."],
  "edo.shop.meal.25": ["lilsis", "Arigatō. I said it to her too, so it's for everybody now."],
  // Little Sister's pennies, offered to Kihei (kiheiTree, or the pennies used on him): the penny with no hole
  "edo.shop.penny.1": ["kihei", "No hole. How do you carry it?"],
  "edo.shop.penny.2": ["lilsis", "In my pocket."],
  "edo.shop.penny.3": ["kihei", "Keep it in your pocket, then."],
  "edo.shop.penny.4": ["lilsis", "He gave it back. Grown-ups never give money back, so now I like him even more."],
  // Little Sister comes back with the word, after the meal
  "edo.shop.arigato.1": ["lilsis", "Arigatō, for the fish. The boy by the signs gave me the word."],
  "edo.shop.arigato.2": ["tami", "Husband, it's doing it again. Your face."],
  "edo.shop.arigato.3": ["kihei", "Let it."],
  // the meal looked at, and after (the step, with the box and the cut pieces on it; then the empty step)
  "edo.shop.food.mom": ["mom", "It was given, girls, not sold. Eat it like a gift."],
  "edo.shop.food.bigsis": ["bigsis", "Pressed mackerel sushi, sour and salty and cold. I may never eat anything else."],
  "edo.shop.food.lilsis": ["lilsis", "It's fish on rice, in squares. It's sour and I like sour, and I've had three."],
  "edo.shop.food.use.mom": ["mom", "One at a time, sweetheart. They're not going anywhere."],
  "edo.shop.food.use.bigsis": ["bigsis", "He nodded when I took another piece. I've never been so glad of a nod."],
  "edo.shop.food.use.lilsis": ["lilsis", "I'm eating with my hands. The fish man does too, so it's manners."],

  // ======================================================================================================
  // #24 WEST: the hens (Little Sister's opening), Kihei's roads, Gonroku's no (gonrokuTree), O-Masa's question
  // (masaTree), and the goodbyes.
  // ======================================================================================================
  // Little Sister at the hen-yard fence: all of them facing west along the coast, as Jolene's faced the fence
  "edo.west.hens.1": ["lilsis", "They're all looking the same way, every single one of them. That way."],
  "edo.west.hens.2": ["lilsis", "Chickens KNOW."],
  "edo.west.hens.3": ["bigsis", "West is a very large direction."],
  "edo.west.hens.4": ["mom", "Then we'll ask someone who knows the roads. Your fish man sees everything go by."],
  "edo.west.hens.again": ["narrator", "The hens are still facing west. Little Sister doesn't think they'll move until the family does."],
  // the door they came through is gone (the ring on the sand: the arrival's mark, looked at)
  "edo.village.arrive.mom": ["narrator", "The place where the family came through. The air has closed over without a mark, like a pond."],
  "edo.village.arrive.bigsis": ["narrator", "The spot where the door in time was. There's nothing there now, not even a hum. They'll need another."],
  "edo.village.arrive.lilsis": ["narrator", "The door is gone. Little Sister has checked twice, and feels doors ought to stay where they're left."],
  "edo.village.arrive.use.mom": ["narrator", "Mom puts a hand out into the empty air. It doesn't open from this side."],
  "edo.village.arrive.use.bigsis": ["narrator", "Big Sister holds the coin up where the door was. Nothing hums and nothing opens."],
  "edo.village.arrive.use.lilsis": ["narrator", "Little Sister knocks on the air. Nobody answers, which she considers rude."],
  // O-Masa goes down the beach to her husband (masaTree's hook `toGonroku`); what she says, the player hears the end of
  "edo.west.masa.1": ["masa", "The Funadama is a lady. A lady likes company with manners."],
  // Gonroku, after a long look at the sea
  "edo.west.gonroku.1": ["gonroku", "They sit in the stern, and they don't whistle."],
  "edo.west.gonroku.2": ["lilsis", "I can't whistle anyway. I've been trying for a year."],
  "edo.west.gonroku.3": ["bigsis", "The stern is the back. That's the one nautical term I know, and now I've used it."],
  "edo.west.gonroku.4": ["mom", "Thank you, both of you. We'll be no trouble, and very quiet."],
  "edo.west.gonroku.5": ["gonroku", "The tide turns at first light. It waits for nobody, and I don't argue with it."],
  // the goodbyes: Kihei and O-Tami at the shop; Little Sister to the baby, the cat, and every hen by name
  "edo.west.bye.1": ["mom", "Thank you for the clothes, the table and the morning. I won't forget any of them."],
  "edo.west.bye.2": ["tami", "Go west, and don't be tall at anybody. And come back when the baby can talk."],
  "edo.west.bye.3": ["kihei", "Keep to the stern and don't whistle. And eat the box before it eats you."],
  "edo.west.bye.4": ["bigsis", "Thank you. I learned one word today and lost all my others. I'd call it a fair trade."],
  "edo.west.bye.5": ["lilsis", "Bye, baby, stay asleep. Bye, cat, and you keep the other fish."],
  "edo.west.bye.6": ["lilsis", "Bye, Peck, Dot, Other Dot, Fuji and Admiral. And bye, Jumpy."],
  "edo.west.bye.7": ["bigsis", "The hens don't have names."],
  "edo.west.bye.8": ["lilsis", "They do now. And Jumpy's a fish, so he's an honorary chicken."],
  "edo.west.bye.9": ["sankichi", "You're going on Uncle Gonroku's boat? He never takes anybody. Bring me back a story, will you?"],
  "edo.west.bye.10": ["lilsis", "I'll bring you back two. Arigatō for the word."],

  // ======================================================================================================
  // CUT-SCENE: The Uttermost Parts (edo-sail.js). The ship at night under its one great sail; Big Sister asleep on a coil
  // of rope, Little Sister asleep on Big Sister; Mom at the stern rail. Then the card, and Osaka in three lines.
  // ======================================================================================================
  "edo.card.sail.title": ["narrator", "The Uttermost Parts"],
  // the box of sushi, earlier, at the rail, before the girls sleep (the thing eaten on the ship)
  "edo.sail.box.1": ["lilsis", "We ate the whole box of sushi, on a boat, at night. Best Tuesday ever."],
  "edo.sail.box.2": ["bigsis", "It isn't Tuesday. Nobody here even has Tuesdays, but it was a very good box."],
  // Mom, quietly, to the sea: Psalm 139:9-10, King James Version, word for word; the semicolon ends the first box
  "edo.sail.1": ["mom", "'If I take the wings of the morning, and dwell in the uttermost parts of the sea;"],
  "edo.sail.2": ["mom", "Even there shall thy hand lead me, and thy right hand shall hold me.'"],
  // Big Sister, not asleep
  "edo.sail.4": ["bigsis", "Psalm 139."],
  "edo.sail.5": ["mom", "Go to sleep, darling."],
  "edo.sail.6": ["bigsis", "We're in the uttermost parts."],
  "edo.sail.7": ["mom", "I know. So is His hand."],
  // the card: "Twelve days later" / "Osaka"; on the map, the portraits go along the coast by the sea path
  "edo.card.sail": ["narrator", "Twelve days later"],
  "edo.card.osaka": ["narrator", "Osaka"],
  // Osaka in three lines over the card: the river mouth, the crowds with ladles going east, a constable's man who looks
  // twice at three tall women in hats; and Gonroku (the arrests are his one line, as the brief has it)
  "edo.sail.osaka.1": ["bigsis", "Everyone has a ladle, and everyone is going east. We are going the other way."],
  "edo.sail.osaka.2": ["mom", "That man in the belt has looked at us twice. Hats down, girls. And we walk."],
  "edo.sail.osaka.3": ["gonroku", "The magistrates have been everywhere in Osaka since the Kirishitan trouble."],
  "edo.sail.osaka.3b": ["gonroku", "Go north, into the hills, until it's quiet."],
  "edo.sail.osaka.4": ["mom", "North, then. Thank you, Captain, for carrying us farther than you meant to."],
  "edo.sail.osaka.5": ["gonroku", "Twelve days of fair wind. I've never had twelve in a row. Don't tell the lady."],

  // ======================================================================================================
  // THE TALKS (js/content/talk/edo-a.js): O-Tami, Kihei, Sankichi, Tokuzō, Gonroku, O-Masa. An option is a line here,
  // said by the one it belongs to.
  // ======================================================================================================
  // ---------- tamiTree: O-Tami ----------
  // before the clerk's first pass (she has not met them properly): she looks them over
  "edo.tami.first.1": ["tami", "Three of you, dressed like that, on my street. Stand over there, and try not to be seen being tall."],
  // her menu
  "edo.tami.opt.clothes.mom": ["mom", "You said we needed proper clothes. I'd be very grateful for the loan of some."],
  "edo.tami.opt.clothes.big": ["bigsis", "About the clothes. I'd very much like to stop being stared at."],
  "edo.tami.opt.clothes.lil": ["lilsis", "Do you have a dress in my size? With pockets?"],
  "edo.tami.clothes.no.1": ["tami", "Dressing you takes two hands. I have a baby in one and this shop in the other."],
  "edo.tami.clothes.no.2": ["tami", "Get her to sleep, and I'll dress the three of you like the lord's own daughters."],
  "edo.tami.clothes.no.lil": ["tami", "No pockets. Everything goes in the sleeves, and you'll like sleeves."],
  "edo.tami.clothes.yes": ["tami", "She's asleep, and I'm a woman of my word. Come to the chest, quietly."],
  "edo.tami.clothes.done": ["tami", "You're dressed. What you do about the hair is between you and the hat."],
  "edo.tami.opt.baby.mom": ["mom", "May I try with the baby? I've had three, and one of them was worse."],
  "edo.tami.opt.baby.big": ["bigsis", "I could read to the baby. No, never mind, I can't read anything here."],
  "edo.tami.opt.baby.lil": ["lilsis", "Can I hold the baby? I'm seven and a half."],
  "edo.tami.baby.big": ["tami", "She can't read either. You'd be good company for each other."],
  "edo.tami.baby.lil": ["tami", "Seven and a half may hold the basket, once she's asleep in it. That's the rule."],      // SCENES-20A: "The baby stays in it": she is on O-Tami's back till she sleeps
  "edo.tami.baby.lil.2": ["lilsis", "Then I'll hold the basket. I'm a very good basket holder."],
  "edo.tami.baby.done": ["tami", "She's still asleep. Keep your voice down, and I'll give you the shop."],
  "edo.tami.opt.red.mom": ["mom", "May I ask why your husband wears red? It suits him, but I'm curious."],
  "edo.tami.opt.red.big": ["bigsis", "Why does your husband wear red? A vest and a hood, in April."],
  "edo.tami.opt.red.lil": ["lilsis", "Why's the fish man in a red hat? Is he the boss?"],
  "edo.tami.red.1": ["tami", "He's sixty. It's a tiger year, the metal one, the same as the year he was born."],
  "edo.tami.red.2": ["tami", "When your own year comes round again, you're a baby again. So he wears red, all year."],
  "edo.tami.red.3": ["tami", "He hates it. I made the hood myself, so he hates the hood most of all."],
  "edo.tami.red.big": ["bigsis", "Sixty years, and the same sign comes round again. A metal tiger. I can work with that."],
  "edo.tami.opt.clerk.mom": ["mom", "What is the clerk looking for, exactly?"],
  "edo.tami.opt.clerk.big": ["bigsis", "The man with the paper. What does his paper say?"],
  "edo.tami.opt.clerk.lil": ["lilsis", "Who's the squinty man?"],
  "edo.tami.clerk.1": ["tami", "Tokuzō, the headman's clerk. He writes down what he sees, and he can't see past his brush."],
  "edo.tami.clerk.2": ["tami", "He wants to write \"nothing seen\" and go home. So give him nothing to see. Be travellers."],
  "edo.tami.clerk.lil": ["tami", "Squinty is the word. He once asked my hen her name, and then asked her again."],
  "edo.tami.opt.sushi.lil": ["lilsis", "Is the fish man going to make us food? I'm only asking."],
  "edo.tami.sushi.lil": ["tami", "He feeds anyone who sits on that step. Sit on it and look hungry. You have the look."],
  "edo.tami.opt.bye.mom": ["mom", "We'll leave you to the baby."],
  "edo.tami.opt.bye.big": ["bigsis", "I'll stop asking questions, for now."],
  "edo.tami.opt.bye.lil": ["lilsis", "I'm going to look at the cat."],
  "edo.tami.bye.mom": ["tami", "Nobody leaves me to the baby, because the baby never leaves me. Go on, then."],
  "edo.tami.bye.big": ["tami", "Ask more. Nobody in this house asks me anything; they only tell me."],
  "edo.tami.bye.lil": ["tami", "The cat will look back at you. Don't take it to heart. She does that to everyone."],

  // ---------- kiheiTree: Kihei. Sparse. ----------
  "edo.kihei.open": ["kihei", "Sit."],
  "edo.kihei.opt.price.mom": ["mom", "What do you ask for a fish? I should tell you first that we can't pay."],
  "edo.kihei.price.1": ["kihei", "For a fish? Sit."],
  "edo.kihei.price.2": ["mom", "We have no money that's any good here. I'd rather you knew that now."],
  "edo.kihei.price.3": ["kihei", "I know. Sit."],
  "edo.kihei.opt.price.big": ["bigsis", "What does the mackerel cost? I'm asking for the record, since we have nothing."],
  "edo.kihei.price.big": ["kihei", "The record can sit too."],
  "edo.kihei.opt.hungry.lil": ["lilsis", "We haven't eaten since Nevada. That's a long way, but I don't know how far."],
  "edo.kihei.hungry.lil": ["kihei", "Sit."],
  "edo.kihei.opt.pennies.lil": ["lilsis", "I have money. Look, three pennies, and they're real ones."],
  "edo.kihei.opt.red.mom": ["mom", "Your red vest. Is it for an occasion?"],
  "edo.kihei.opt.red.big": ["bigsis", "The red vest and the hood. I have a theory, but I'd rather have a fact."],
  "edo.kihei.opt.red.lil": ["lilsis", "Why are you wearing a red hat? Is it your birthday?"],
  "edo.kihei.red": ["kihei", "Ask my wife."],
  "edo.kihei.red.lil": ["kihei", "Yes, all year. Ask my wife."],
  "edo.kihei.opt.print.big": ["bigsis", "The picture of the mountain. Where did it come from?"],
  "edo.kihei.opt.print.mom": ["mom", "That's a fine picture of the mountain. Was it a gift?"],
  "edo.kihei.print.1": ["kihei", "From a pedlar. Everybody in Edo wants the mountain this year, in that new blue."],
  "edo.kihei.print.2": ["kihei", "I see the mountain every morning for nothing. I bought it anyway, for the blue."],
  "edo.kihei.opt.west.mom": ["mom", "If we were going west, which way is it, and how far does it go?"],
  "edo.kihei.opt.west.big": ["bigsis", "What's west of here, and how does one get there?"],
  "edo.kihei.opt.west.lil": ["lilsis", "The chickens are all looking west. What's west?"],
  "edo.kihei.west.1": ["kihei", "The road over the pass is the Tōkaidō. It goes to Kyoto and Osaka. The Inland Sea is past that."],
  "edo.kihei.west.2": ["kihei", "It's a long way on sandals. It's shorter by sea."],
  "edo.kihei.west.3": ["kihei", "My sister's husband's ship is in the bay. He sails for Osaka on the morning tide, with dried bonito."],
  "edo.kihei.west.4": ["kihei", "He won't take you. Ask anyway, and ask the right one."],
  "edo.kihei.west.lil": ["kihei", "Hens here always look west. The wind comes from there. Still, they might know. Ask them."],
  "edo.kihei.opt.arigato.lil": ["lilsis", "Arigatō."],
  "edo.kihei.opt.thanks.mom": ["mom", "Thank you. For all of it."],
  "edo.kihei.thanks.mom": ["kihei", "Okage-sama de. The girl told you what it means; she tells everybody."],
  "edo.kihei.opt.bye.mom": ["mom", "We'll be out from under your feet."],
  "edo.kihei.opt.bye.big": ["bigsis", "I'll let you work."],
  "edo.kihei.opt.bye.lil": ["lilsis", "Bye, fish man. I'll be right here."],
  "edo.kihei.bye": ["kihei", "Sit when you're back."],
  "edo.kihei.bye.lil": ["kihei", "I know."],

  // ---------- sankichiTree: Sankichi, nine, beside the board. He asks questions in Little Sister's own rhythm. ----------
  "edo.sankichi.open.lil": ["sankichi", "Are those your feet, the yellow things? Are they feet, or are they boots?"],
  "edo.sankichi.open.lil.2": ["lilsis", "They're boots, and my feet are inside. Are you the one who can read?"],
  "edo.sankichi.open.lil.3": ["sankichi", "I can read all of it. Can you read?"],
  "edo.sankichi.open.lil.4": ["lilsis", "A little. I can read \"hen\", but here it's all squiggles."],
  "edo.sankichi.open.big": ["sankichi", "You're staring at the board. Can you read?"],
  "edo.sankichi.open.big.2": ["bigsis", "I used to be able to."],
  "edo.sankichi.open.mom": ["sankichi", "You're so tall, taller than the headman. Is everyone tall where you come from?"],
  "edo.sankichi.open.mom.2": ["mom", "Not everybody, dear. But it does help my children find me in a crowd."],
  // the board: he reads the Kirishitan board aloud, once, because somebody asked (edo.boardRead); it is answered once
  "edo.sankichi.opt.board.lil": ["lilsis", "What does the big sign say? Please read it to me."],
  "edo.sankichi.opt.board.big": ["bigsis", "Would you read me the board on the left? Any of it, or all of it."],
  "edo.sankichi.opt.board.mom": ["mom", "What do the notices say? We're strangers, and we'd like to know the rules."],
  "edo.village.board.read.1": ["sankichi", "That one is the oldest. It's older than Grandfather, and it says \"Ordinance\" at the top."],
  "edo.village.board.read.2": ["sankichi", "The Kirishitan sect is forbidden, as always. Tell on one and you get silver."],
  "edo.village.board.read.3": ["sankichi", "Five hundred pieces for a padre, and a hundred for anyone who prays to their god."],
  "edo.village.board.read.4": ["sankichi", "Teacher says nobody has seen a padre in nearly two hundred years."],
  "edo.village.board.read.4b": ["sankichi", "The silver is still up there, though."],
  "edo.village.board.read.5": ["mom", "Then we pray quietly here."],
  "edo.village.board.read.6": ["lilsis", "That's mean."],
  "edo.village.board.read.7": ["mom", "It is."],
  "edo.village.board.read.again": ["sankichi", "I read you that one already. The others are about poison and horses, and horses cost more."],
  // the year: a true answer that does not help (and the era for the card)
  "edo.sankichi.opt.year.big": ["bigsis", "What year is it, exactly? Take your time."],
  "edo.sankichi.year.1": ["sankichi", "The thirteenth year of Bunsei. Everybody knows that."],
  "edo.sankichi.year.2": ["bigsis", "I don't know what that is, but I'm writing it down anyway. Bunsei thirteen."],
  "edo.sankichi.year.3": ["sankichi", "You said you couldn't read. How can you write?"],
  "edo.sankichi.year.4": ["bigsis", "In my head. I can still write in my head."],
  // the word: arigatō, for Little Sister (edo.arigato)
  "edo.sankichi.opt.thanks.lil": ["lilsis", "How do you say thank you here? I'm going to need it a lot."],
  "edo.sankichi.thanks.1": ["sankichi", "You don't know thank you? What do you say when somebody gives you a fish?"],
  "edo.sankichi.thanks.2": ["sankichi", "Arigatō. It means thank you. Say it to Grandfather and watch his face."],
  "edo.sankichi.thanks.3": ["lilsis", "Arigatō, arigatō. I've got it now, and it's mine."],
  "edo.sankichi.thanks.again": ["sankichi", "You've said it nine times. It still means thank you."],
  // questions back: his, in her rhythm, and hers
  "edo.sankichi.opt.questions.lil": ["lilsis", "My turn. One: have you got chickens? Two: can I see them? Three: what's your name?"],
  "edo.sankichi.questions.1": ["sankichi", "Five, by the fence. Yes. Sankichi."],      // SCENES-20A: "Six": the yard has five
  "edo.sankichi.questions.1b": ["sankichi", "My turn. One: what is a Nevada? Two: is it far? Three: why?"],
  "edo.sankichi.questions.2": ["lilsis", "A place. Yes. Because Daddy took a shortcut. You ask questions the right way."],
  "edo.sankichi.questions.3": ["sankichi", "You answer them the right way. Nobody answers mine; they just say \"later\"."],
  "edo.sankichi.opt.school.big": ["bigsis", "Where did you learn to read?"],
  "edo.sankichi.school.1": ["sankichi", "At the temple school. Teacher hits the desk and not us, mostly."],
  "edo.sankichi.school.2": ["bigsis", "I'd give a great deal for one morning at that desk."],
  "edo.sankichi.opt.boots.lil": ["lilsis", "Why does everybody look at my boots?"],
  "edo.sankichi.boots": ["sankichi", "Because they're yellow, and nobody's feet are yellow. May I touch one?"],
  "edo.sankichi.boots.2": ["lilsis", "One touch, on the left one. The right one's shy."],
  "edo.sankichi.opt.mom.mom": ["mom", "Is your grandfather the fishmonger? In the red?"],
  "edo.sankichi.mom": ["sankichi", "Grandmother made the hood. He says it itches, but it doesn't; he only says so."],
  "edo.sankichi.opt.bye.lil": ["lilsis", "I have to go. Mommy's doing the signal."],
  "edo.sankichi.opt.bye.big": ["bigsis", "Thank you. You've been more use than the entire board."],
  "edo.sankichi.opt.bye.mom": ["mom", "Thank you, dear. Go and tell your grandmother we're coming in."],
  "edo.sankichi.bye.lil": ["sankichi", "What is the signal? Is it the eyebrows, like my grandmother's?"],
  "edo.sankichi.bye.big": ["sankichi", "The board can't talk, and I can. That's the whole difference."],
  "edo.sankichi.bye.mom": ["sankichi", "She knows already. She knew before you did; she always does."],
  // things shown to him: the car key (he asks; Mom will not lie), the coin
  "edo.sankichi.key.1": ["sankichi", "What is it?"],
  "edo.sankichi.key.2": ["mom", "A key."],
  "edo.sankichi.key.3": ["sankichi", "To what?"],
  "edo.sankichi.key.4": ["mom", "To a cart that goes without a horse. It's at home, a long way east."],
  "edo.sankichi.key.5": ["sankichi", "I'm going to tell Teacher. He's going to hit the desk."],
  "edo.sankichi.coin.1": ["sankichi", "Whose face is that? It isn't the lord, because the lord has more chin."],
  "edo.sankichi.coin.2": ["bigsis", "A Roman's. He's been dead a very long time, longer than you're thinking."],

  // ---------- tokuzoTree: Tokuzō, the headman's clerk. He peers. Nobody lies. ----------
  // before the kimonos: O-Tami's hand on Mom's sleeve, and the talk does not happen
  "edo.tokuzo.notyet": ["tami", "Not like that, dear. Not in that."],
  "edo.tokuzo.notyet.2": ["mom", "No, quite right. Not in this."],
  // dressed: he peers
  "edo.tokuzo.open.1": ["tokuzo", "Good morning. Forgive me, forgive me, but are you travellers?"],
  "edo.tokuzo.opt.travellers.mom": ["mom", "We are. We're going west."],
  "edo.tokuzo.opt.travellers.big": ["bigsis", "Travellers, yes. We've travelled a great deal since yesterday."],
  "edo.tokuzo.opt.travellers.lil": ["lilsis", "We're going on a boat, probably, if the boat man says yes."],
  "edo.tokuzo.travellers.lil": ["tokuzo", "A boat, going west. Children say the truest things, so I'll write \"west\"."],
  "edo.tokuzo.from": ["tokuzo", "West, good. And from where, if I may ask?"],
  "edo.tokuzo.opt.from.big": ["bigsis", "From the east."],
  "edo.tokuzo.opt.from.mom": ["mom", "From a long way past Edo."],
  "edo.tokuzo.opt.from.lil": ["lilsis", "From our house."],
  "edo.tokuzo.from.big": ["tokuzo", "The east. Yes, most people are, so I'll write \"the east\"."],
  "edo.tokuzo.from.big.mom": ["mom", "Well, now."],
  "edo.tokuzo.from.big.2": ["bigsis", "It's true, Mom. Every word of it."],
  "edo.tokuzo.from.mom": ["tokuzo", "Past Edo. Then you've come farther than I ever have. I have been to Okitsu, once."],
  "edo.tokuzo.from.lil": ["tokuzo", "From your house. Everybody is, when you think about it, so I'll write \"house\"."],
  "edo.tokuzo.tall": ["tokuzo", "You are very tall."],
  "edo.tokuzo.opt.tall.mom": ["mom", "I am."],
  "edo.tokuzo.opt.tall.big": ["bigsis", "She is. It runs in the family, up to a point, and the point is me."],
  "edo.tokuzo.opt.tall.lil": ["lilsis", "She's the tallest and I'm the smallest. We average out."],
  "edo.tokuzo.tall.ans": ["tokuzo", "So you are. Well, one can't write \"tall\", because there's no box for it."],
  // he writes it down, and goes home, pleased
  "edo.tokuzo.write.1": ["tokuzo", "\"Travellers, three, going west.\" Nothing seen, which is good."],
  "edo.tokuzo.write.2": ["tokuzo", "Forgive me, and a pleasant road to you. Mind the pass; it's steep."],
  "edo.tokuzo.write.3": ["tokuzo", "I'm told the view from the top is wasted on the short-sighted."],
  // met again, after (if the scene keeps him on his rounds)
  "edo.tokuzo.after": ["tokuzo", "The travellers, still going west? Good. It's written, and I won't write it twice."],
  "edo.tokuzo.after.opt.mom": ["mom", "Still west."],
  "edo.tokuzo.after.mom": ["tokuzo", "Then nothing has changed, and nothing is my favorite thing to write."],
  "edo.tokuzo.after.opt.lil": ["lilsis", "Do you need glasses? We have them where I come from, round ones."],
  "edo.tokuzo.after.lil": ["tokuzo", "Glasses, yes, I've heard of them. They sound expensive, and squinting costs nothing."],

  // ---------- gonrokuTree: Gonroku, the captain. No women aboard. Every argument fails, and he speaks in weather. ----------
  "edo.gonroku.open": ["gonroku", "The wind is coming round, with rain behind it, two days off. You want something."],
  "edo.gonroku.opt.passage.mom": ["mom", "We'd like passage west, to Osaka. We can't pay, but I'd still like to ask."],
  "edo.gonroku.no.1": ["gonroku", "You've asked. No."],
  "edo.gonroku.no.2": ["gonroku", "The Funadama is the ship's own lady. She doesn't care for other women aboard."],
  "edo.gonroku.no.3": ["gonroku", "Her things are sealed in the mast: dice, two dolls, coins, a woman's hair. She's particular."],
  "edo.gonroku.opt.hair.big": ["bigsis", "A woman's hair is in the mast. So there's a woman aboard already, technically."],
  "edo.gonroku.hair": ["gonroku", "Technically, she's the one who'd mind, and there are clouds building over the pass. No."],
  "edo.gonroku.opt.luck.lil": ["lilsis", "We aren't bad luck, we're good luck. The hens like us, and hens can tell."],
  "edo.gonroku.luck": ["gonroku", "Hens don't sail, and the wind is freshening. No."],
  "edo.gonroku.opt.quiet.mom": ["mom", "We'd sit very still and say nothing, the whole way. I've had practice."],
  "edo.gonroku.quiet": ["gonroku", "Twelve days of still women is twelve days of waiting for the other thing. No."],
  "edo.gonroku.opt.men.big": ["bigsis", "Is it a rule, or a feeling? I ask because feelings have exceptions."],
  "edo.gonroku.men": ["gonroku", "It's weather. You don't argue with weather. You wait for it to change, and it won't."],
  "edo.gonroku.opt.stern.lil": ["lilsis", "We'll sit in the very back, on the floor. We won't touch the lady's mast."],
  "edo.gonroku.stern": ["gonroku", "The stern is hers as well, and the swell is getting up. No."],
  "edo.gonroku.opt.where.mom": ["mom", "Where do you sail, and when?"],
  "edo.gonroku.where": ["gonroku", "Osaka, at first light, with bonito. Twelve days, if the wind is kind. It won't be."],
  "edo.gonroku.opt.wife.mom": ["mom", "And what does the Funadama like?"],
  "edo.gonroku.wife": ["gonroku", "Ask my wife. She knows what everybody likes. She's at the nets. Mind how you ask."],
  "edo.gonroku.opt.bye.mom": ["mom", "Then we'll leave you to your weather."],
  "edo.gonroku.opt.bye.big": ["bigsis", "I'll come back with a better argument."],
  "edo.gonroku.opt.bye.lil": ["lilsis", "I'm going to ask the chickens about you."],
  "edo.gonroku.bye.mom": ["gonroku", "Nobody leaves me to it. The weather comes anyway."],
  "edo.gonroku.bye.big": ["gonroku", "Bring one for the wind while you're at it."],
  "edo.gonroku.bye.lil": ["gonroku", "Tell them the wind is westerly. They'll know what that means."],
  // after O-Masa has spoken (edo.west): the terms
  "edo.gonroku.after.1": ["gonroku", "The stern, no whistling, and first light. That's three things, and I've said them."],
  "edo.gonroku.after.opt.mom": ["mom", "We'll be there before the light is."],
  "edo.gonroku.after.mom": ["gonroku", "Everybody says that. The tide believes nobody."],
  "edo.gonroku.after.opt.lil": ["lilsis", "I promise not to whistle. I can't anyway, watch."],
  "edo.gonroku.after.lil": ["gonroku", "Keep on not doing that. The wind is fair, so don't spoil it."],

  // ---------- masaTree: O-Masa, Kihei's sister, Gonroku's wife, at the net racks. Verdicts. Asked properly. ----------
  "edo.masa.open": ["masa", "You've been to my husband; I saw his shoulders. Well?"],
  "edo.masa.opt.favour.mom": ["mom", "Would you ask your husband to take us? He listens to you."],
  "edo.masa.favour": ["masa", "That's a favour. Favours I give my brother. Questions I'll take from anybody."],
  "edo.masa.opt.unfair.big": ["bigsis", "Your husband's position is unreasonable. I say that with respect."],
  "edo.masa.unfair": ["masa", "He's a sailor, and reason is for the land. You're right, though."],
  "edo.masa.opt.boss.lil": ["lilsis", "Can you make him take us? I can tell you're the boss of him."],
  "edo.masa.boss": ["masa", "Nobody is the boss of a sailor, except his wife. Sit down; you're in my light."],
  "edo.masa.opt.nets.lil": ["lilsis", "What are you doing to the net? It's full of holes."],
  "edo.masa.nets": ["masa", "A thousand holes with string round them, and it holds fish. Think about that."],
  "edo.masa.nets.2": ["lilsis", "I'm thinking about it. It's a lot to think about."],
  "edo.masa.opt.brother.mom": ["mom", "Your brother fed us this morning and would take nothing. I thought you should know."],
  "edo.masa.brother": ["masa", "My brother feeds people and my husband ships fish. I married the wrong one for lunch."],
  "edo.masa.opt.lady.big": ["bigsis", "The Funadama. Is she real?"],
  "edo.masa.lady": ["masa", "She's real to him. That's what you'd be sailing on: not the sea, him."],
  // before #22 and #23: she looks at them, and her verdict is not yet
  "edo.masa.opt.ask.mom": ["mom", "May I ask your advice? Not a favour, but a proper question."],
  "edo.masa.notdressed": ["masa", "Not in those clothes. Nobody asks me anything properly dressed like that. Go to my brother's wife."],
  "edo.masa.notfed": ["masa", "You haven't eaten. I can hear it from here. Sit on my brother's step first, and then ask."],
  "edo.masa.notclerk": ["masa", "Half the village saw you come in. The clerk hasn't seen you go out. See him first."],
  // the lever: the question, properly asked; she looks at the three of them, their manners and their borrowed clothes
  "edo.masa.ask.1": ["masa", "Ask it."],
  "edo.masa.ask.2": ["mom", "What would the Funadama make of three women who sit still and have manners?"],
  "edo.masa.ask.3": ["masa", "Hm."],
  "edo.masa.ask.4": ["masa", "That is a question. Stay here, all three of you, and don't follow me."],
  // (she goes down the beach: masaTree's hook `toGonroku`, then edo.west.masa.1 and edo.west.gonroku.*)
  "edo.masa.opt.bye.mom": ["mom", "We'll let you mend."],
  "edo.masa.opt.bye.big": ["bigsis", "Thank you. I think."],
  "edo.masa.opt.bye.lil": ["lilsis", "Bye, net boss."],
  "edo.masa.bye.mom": ["masa", "The mending gets done whether I'm let or not. Go on."],
  "edo.masa.bye.big": ["masa", "You think a great deal. Try asking instead; it's quicker."],
  "edo.masa.bye.lil": ["masa", "Net boss. I'll keep that."],
  // after (edo.west): her last word
  "edo.masa.after": ["masa", "He said the stern, and no whistling. He means the whistling; the rest is weather."],

  // ======================================================================================================
  // HINTS: hint.edo.<puzzle>.<who>. The one whose job it is says what to try; the others say whose job it is.
  // Staged where a puzzle is long (ids.md says which stage is which).
  // ======================================================================================================
  // #21 Where, And When (Big Sister's): staged by which clues are in (edo.clue.red, .coins, .blue)
  "hint.edo.when.bigsis": ["bigsis", "No sign will tell me the year, but things might: the red, the coins, that blue."],
  "hint.edo.when.bigsis.2": ["bigsis", "The fishmonger wears red for a reason, and his wife will know it. Ask O-Tami why."],
  "hint.edo.when.bigsis.3": ["bigsis", "His money box is right there in the shop. Coins carry their era with them, so look at those."],
  "hint.edo.when.bigsis.4": ["bigsis", "The print of the mountain in the shop is a very particular blue. Look at it, or ask Kihei."],
  "hint.edo.when.bigsis.5": ["bigsis", "Red, coins, blue. I have all three clues now, and I can do this sum standing up."],
  "hint.edo.when.mom": ["mom", "The year is your sister's to work out. She reads coins and colors the way she reads books."],
  "hint.edo.when.lilsis": ["lilsis", "My sister does the when and I do the chickens. We have a system."],
  // #22 Out Of Sight (Mom's): staged: before the first pass, before the baby, before the clothes, before the clerk
  "hint.edo.dressed.mom": ["mom", "Three women in our own clothes on a main street. We need to look like everyone else. Try the fish shop."],
  "hint.edo.dressed.mom.2": ["mom", "O-Tami can't dress us until her baby sleeps. I've had three. Let me try with the baby."],
  "hint.edo.dressed.mom.3": ["mom", "The baby's asleep, and O-Tami said she'd dress us. I'll ask her about the clothes again."],
  "hint.edo.dressed.mom.4": ["mom", "We're dressed. Now we talk to the clerk in the street, and give him only true answers."],
  "hint.edo.dressed.bigsis": ["bigsis", "The clothes are Mom's job. Nobody says no to Mom when she has a baby in her arms."],
  "hint.edo.dressed.lilsis": ["lilsis", "Mommy's doing the grown-ups and the clothes. I'm keeping my boots."],
  // #23 Kihei's Table (any): staged: before anyone has asked; the pennies tried; the meal done
  "hint.edo.fed.mom": ["mom", "We haven't eaten since Nevada. I'll ask the fishmonger his price, and tell him honestly we can't pay."],
  "hint.edo.fed.mom.2": ["mom", "He keeps saying \"Sit\". I think that's the price. Let's talk to him again and sit."],
  "hint.edo.fed.bigsis": ["bigsis", "Mom asks prices and I state facts. The fact is I'm hungry. Let's talk to the fishmonger."],
  "hint.edo.fed.bigsis.2": ["bigsis", "He's said \"Sit\" several times now. In most languages that's an invitation. Talk to him and accept."],
  "hint.edo.fed.lilsis": ["lilsis", "I'll ask the fish man for food. Or I'll show him my pennies. I've got three."],
  "hint.edo.fed.lilsis.2": ["lilsis", "I showed him my pennies and he gave them back. I think we're just supposed to sit. Ask him."],
  // #24 West (Little Sister, then Mom): staged: the hens not seen; Gonroku not asked; Gonroku refused; O-Masa to ask
  "hint.edo.west.lilsis": ["lilsis", "The door's gone. When a door's gone, you ask the chickens, and they're by the fence."],
  "hint.edo.west.lilsis.2": ["lilsis", "The chickens say west. The fish man knows the roads, and he knows the boat man. Ask him."],
  "hint.edo.west.lilsis.3": ["lilsis", "The boat man said no to everything, even the chickens. It's Mommy's turn to ask."],
  "hint.edo.west.mom": ["mom", "Your sister's hens are pointing west. I'll ask the fishmonger about the roads."],
  "hint.edo.west.mom.2": ["mom", "Captains have wives, and his is at the nets. I'll ask her a question, not a favour."],
  "hint.edo.west.mom.3": ["mom", "The ship's ours at first light. Time for goodbyes, girls, hens included. Then we go to the captain."],
  "hint.edo.west.bigsis": ["bigsis", "Arguing with the captain doesn't work. Let Mom ask him what his ship's lady does like."],
  "hint.edo.west.bigsis.2": ["bigsis", "Everyone on that beach defers to the woman at the nets. Mom should ask her a proper question."],

  // ======================================================================================================
  // THE THINGS CARRIED (world.js items: sushibox, mirror, trowel), looked at by each of the three
  // ======================================================================================================
  "item.sushibox.mom": ["narrator", "Kihei's pressed sushi, wrapped in a bamboo leaf by a woman holding a baby. Mom means to make it last."],
  "item.sushibox.bigsis": ["narrator", "Pressed mackerel sushi in a bamboo leaf, made the old way, in a box. Edo's new hand-made kind can wait."],
  "item.sushibox.lilsis": ["narrator", "The fish box. Little Sister is carrying it, not eating it. She has had one piece."],
  "item.mirror.mom": ["narrator", "The grandmother's bronze mirror, a pine and a crane on its back. It is to be held up in the light, she said."],
  "item.mirror.bigsis": ["narrator", "The grandmother's bronze mirror, slightly convex. The picture on its back shows in the light it throws."],
  "item.mirror.lilsis": ["narrator", "The grandmother's mirror, heavy, with a bird on the back. Little Sister is carrying it very carefully."],
  "item.trowel.mom": ["narrator", "A wall trowel, for a cousin at Himeji. \"Say Jinsuke is well\" is all the family needs to say."],
  "item.trowel.bigsis": ["narrator", "A trowel, worn bright, its handle shaped by one hand. It is going back to that hand."],
  "item.trowel.lilsis": ["narrator", "A flat trowel for plastering walls, for the cousin. Little Sister asked, and it isn't for digging."],

  // ======================================================================================================
  // THE ACT'S STOCK REPLIES for the three (story.fallbacks, story.give, in Japan), and what the people of Yui say when
  // handed a thing they do not want (the scenes' useWith for the rest)
  // ======================================================================================================
  "edo.nope.mom.1": ["narrator", "Mom thinks better of it. The family are guests in this country."],
  "edo.nope.mom.2": ["narrator", "Mom considers it, and decides a guest wouldn't."],
  "edo.nope.mom.3": ["narrator", "It's a thought, and Mom leaves it as one."],
  "edo.nope.bigsis.1": ["narrator", "Big Sister can't make that work, and can't read anything that might tell her why."],
  "edo.nope.bigsis.2": ["narrator", "That doesn't work here, or in any other century Big Sister has tried it."],
  "edo.nope.bigsis.3": ["narrator", "Big Sister tries it, and nothing comes of it. She makes a mental note."],
  "edo.nope.lilsis.1": ["narrator", "Little Sister gives it a good try. It doesn't go, not even in Japan."],
  "edo.nope.lilsis.2": ["narrator", "Little Sister tries it twice, the second time harder. Nothing happens."],
  "edo.nope.lilsis.3": ["narrator", "Little Sister decides that idea is silly, though she's glad somebody had it."],
  "edo.look.mom.1": ["narrator", "Nothing there that needs the family's attention, which this morning is a kindness."],
  "edo.look.bigsis.1": ["narrator", "Nothing remarkable there, as far as Big Sister can tell."],
  "edo.look.lilsis.1": ["narrator", "It's just a thing. Little Sister has already moved on to the next one."],
  "edo.hint.none.mom": ["mom", "I haven't the faintest idea, my love. Let's look around, politely."],
  "edo.hint.none.bigsis": ["bigsis", "I don't know. I can't even read my way to a guess here. Let's look around."],
  "edo.hint.none.lilsis": ["lilsis", "I don't know. Ask Mommy, she's the tallest one here."],
  "edo.give.mom.1": ["mom", "Would you take this for me? Quietly."],
  "edo.give.bigsis.1": ["bigsis", "Here, it's yours now. Don't lose it in a sleeve."],
  "edo.give.lilsis.1": ["lilsis", "Hold this for me. It's important."],
  // the people of Yui, handed a thing they do not want
  "edo.give.no.kihei": ["kihei", "No. Sit."],
  "edo.give.no.tami": ["tami", "I have a baby in one hand and a shop in the other. Where would I put it?"],
  "edo.give.no.sankichi": ["sankichi", "What is it, and what does it do? If I can't keep it, why show me?"],
  "edo.give.no.tokuzo": ["tokuzo", "Forgive me. I can't take anything I can't see, and I can't see that."],
  "edo.give.no.gonroku": ["gonroku", "Nothing comes aboard that she hasn't met, and the wind is backing. No."],
  "edo.give.no.masa": ["masa", "Put it away. I have nets to mend, and you have asking to do."],
  // the egg, shown to Kihei (it is Little Sister's, from Nevada: she will not part with it here)
  "edo.shop.egg.kihei": ["kihei", "An egg. You have an egg and I have fish, so keep your egg."],
  "edo.shop.egg.lilsis": ["lilsis", "I wasn't giving it, I was showing it. It's a Nevada egg, and it's been places."],

  // ======================================================================================================
  // THE THREE OF THEM, to each other (the scene's `talk` for companions, in the first leg)
  // ======================================================================================================
  "edo.talk.mom.bigsis.read.a": ["mom", "You've gone quiet, darling."],
  "edo.talk.mom.bigsis.read.b": ["bigsis", "I can't read a single thing here, Mom. Not a sign, not a label, not a price."],
  "edo.talk.mom.bigsis.read.c": ["mom", "Then read people. Start with me; I'm an easy chapter."],
  "edo.talk.bigsis.mom.tall.a": ["bigsis", "Everyone looks at you, Mom. You're a head taller than every woman here."],
  "edo.talk.bigsis.mom.tall.b": ["mom", "I know. I've decided to be tall on purpose, because it looks better that way."],
  "edo.talk.mom.lilsis.boots.a": ["mom", "The boots are staying, are they?"],
  "edo.talk.mom.lilsis.boots.b": ["lilsis", "The boots stay. They've been to Nevada, so they can do Japan."],
  "edo.talk.lilsis.mom.son.a": ["lilsis", "Mommy, is my brother looking for us now? Since we came the wrong way?"],
  "edo.talk.lilsis.mom.son.b": ["mom", "He's looking for all of us, sweetheart. We'll be easier to find together."],
  "edo.talk.lilsis.bigsis.word.a": ["lilsis", "I know a Japan word now: arigatō. How many do you know?"],
  "edo.talk.lilsis.bigsis.word.b": ["bigsis", "About forty, and all of them are food. Not one of them is thank you."],
  "edo.talk.lilsis.bigsis.word.c": ["lilsis", "Then mine's the best one. Arigatō."],
  "edo.talk.bigsis.lilsis.hens.a": ["bigsis", "The hens here are doing it too, all facing one way. I'm not going to say they know."],
  "edo.talk.bigsis.lilsis.hens.b": ["lilsis", "You don't have to say it. They know you know."],
  "edo.talk.mom.bigsis.lie.a": ["mom", "When the clerk asks, we tell him the truth. All we can, and nothing else."],
  "edo.talk.mom.bigsis.lie.b": ["bigsis", "\"From the east\" is the truth, Mom. It's just a very small piece of it."],
  "edo.talk.mom.bigsis.lie.c": ["mom", "A small true piece is still true, and a large false one isn't. Keep them small."],
  "edo.talk.lilsis.mom.grace.a": ["lilsis", "Mommy, they didn't say grace. They bowed at the shelf and didn't say anything."],
  "edo.talk.lilsis.mom.grace.b": ["mom", "That's their way of being thankful. Ours has more words, and yours especially."],

  // MERGE-20: the map's refusal for a place of a leg behind them (maps.js `far`, ENGINE-20's legs): Mom's, after her
  // first words in Japan.
  "edo.map.far.yui": ["mom", "Yui is twelve days back, by sea. We keep going."],
  // MERGE-20: the other two places the map can show from a leg that is not theirs: Osaka, faint beyond the bay before the
  // voyage (a place of the next leg); Himeji, faint beyond the hills (the next leg). Mom's, and true from where she stands.
  "edo.map.far.osaka": ["mom", "Osaka is a long way by sea. We'd need a ship, and a captain who says yes."],
  "edo.map.far.himeji": ["mom", "Himeji is four days' walk from here. When it's time, we'll walk it."],  // WRITE-21B: was "Himeji is three days' walk from here. When it's time, we'll walk it." (four days from the hills, not three; the per-leg lines are edo.map.far.himeji.<leg> (edo-d.en.js))

  // ======================================================================================================
  // SCENES-20A: new lines of the first leg's staging (one block, marked; WRITE-20A's rules: nobody in the family lies)
  // ======================================================================================================
  // #24's gate, the year not yet worked out (#21): the passage agreed, the boat at hand, and Big Sister will not go
  "edo.sail.notyet.bigsis": ["bigsis", "Not yet. I won't sail out of a year I can't name. The year first, then the sea."],
  // ---- SCENES-21A: lines added on the stage in phase B go below this line, and nowhere else in this file (MERGE-21) ----
  // SCENES-21A: O-Masa asked properly, dressed and fed, before they have tried the road west (round twenty-one: #25 after #24)
  "edo.masa.notroad": ["masa", "Walk up that road first, or he'll say you could have walked. Then ask me."],
  // ---- TALK-24 (10 November: "way too many dialogue choices in Japan"): the topics a talk's questions are gathered under ----
  "edo.gonroku.topic.case": ["bigsis", "We have more arguments. I've numbered them."],
  "edo.masa.topic.husband": ["mom", "May I ask about your husband, and his boat?"],
  "edo.masa.topic.chat": ["lilsis", "Can I ask about your net? And other things?"],
  "edo.tami.topic.asks.lil": ["lilsis", "I have three questions. They're important ones."],
};
