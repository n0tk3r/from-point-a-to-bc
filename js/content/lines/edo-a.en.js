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
// The round-nineteen box: at most 80 characters, one idea, the punch word last. S/work-20-writeA/ids.md says when every
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
  "edo.arrive.3": ["lilsis", "HERE. ...Where's here?"],
  // the bay, the boats, and across the water a white mountain filling a third of the sky
  "edo.arrive.4": ["lilsis", "This isn't ROME. Rome was supposed to have my brother in it."],
  "edo.arrive.5": ["bigsis", "That is Mount Fuji. Which makes this Japan, and not Rome by a very long way."],
  "edo.arrive.6": ["lilsis", "...Is he here?"],
  "edo.arrive.7": ["mom", "No, sweetheart. Not here."],
  // she looks at the closed air where the door was
  "edo.arrive.8": ["mom", "Then we keep going, girls. It's the one thing asked of us, and we're good at it."],
  // a gull; a rooster somewhere up the beach
  "edo.arrive.9": ["lilsis", "A rooster. ...All right. I can work with a rooster."],
  // the first villager to see them: a woman with a basket, who puts it down and goes
  "edo.arrive.10": ["basketwoman", "...Forgive me. I will come back for the basket."],
  "edo.arrive.11": ["mom", "We've made an impression, girls. Let's see if we can make a kinder one."],
  // the act's card (SCENES-20 shows it where the act begins; Big Sister's line joins it once #21 is solved, edo.when)
  "edo.card.title": ["narrator", "Act Six: By Your Grace"],
  "edo.card.when": ["bigsis", "Spring, 1830. Bunsei thirteen. The year of the metal tiger."],

  // ======================================================================================================
  // THE VILLAGE (edo-village): Yui on Suruga Bay, morning. A look from each of the three at every thing, and a use.
  // ======================================================================================================
  // Fuji, white and enormous across the bay
  "edo.village.fuji.mom": ["mom", "I've seen it on a thousand teacups. Not one of them was telling the truth."],
  "edo.village.fuji.bigsis": ["bigsis", "Fuji. Snow that far down the slopes means spring. It stays white into summer."],
  "edo.village.fuji.lilsis": ["lilsis", "That's the biggest thing I've ever SEEN. And I've seen Daddy's car."],
  "edo.village.fuji.use.mom": ["mom", "It's across the water, darling. Some things are best admired from a distance."],
  "edo.village.fuji.use.bigsis": ["bigsis", "One does not use a mountain. One is used by it."],
  "edo.village.fuji.use.lilsis": ["lilsis", "I tried to touch it. It's FURTHER than it looks."],
  // the bay
  "edo.village.bay.mom": ["mom", "Flat water, and a mountain standing in it upside down."],
  "edo.village.bay.bigsis": ["bigsis", "Suruga Bay, if that is Fuji. The sea goes the whole way round to Osaka."],
  "edo.village.bay.lilsis": ["lilsis", "It's the sea! I didn't bring my swimsuit. I didn't bring ANYTHING."],
  "edo.village.bay.use.mom": ["mom", "I'm not wading, sweetheart. Not in these shoes, and not in those."],
  "edo.village.bay.use.bigsis": ["bigsis", "It is April. The water is a fact I do not need to check."],
  "edo.village.bay.use.lilsis": ["lilsis", "It's COLD. I only put one toe in. The toe says no, and the toe's the boss."],
  // Gonroku's freighter at anchor, its one sail furled
  "edo.village.ship.mom": ["mom", "A ship at anchor, with one mast and nobody in a hurry on it."],
  "edo.village.ship.bigsis": ["bigsis", "One mast, one enormous sail, rolled up. A ship that goes where the wind says."],
  "edo.village.ship.lilsis": ["lilsis", "A BOAT. A big one. Boats go places. We need to go places."],
  "edo.village.ship.use.mom": ["mom", "It's half a mile out, darling. It'll have a captain. Captains have wives."],
  "edo.village.ship.use.bigsis": ["bigsis", "I cannot hail a ship. I can barely hail a bus."],
  "edo.village.ship.use.lilsis": ["lilsis", "Hey, BOAT. ...It's not listening. Boats are like that."],
  // the boats on their props, and the gap under one
  "edo.village.boats.mom": ["mom", "Fishing boats, pulled up on blocks like shoes left by a door."],
  "edo.village.boats.bigsis": ["bigsis", "Boats on props. Each one has a gap under it a seven-year-old would notice."],
  "edo.village.boats.lilsis": ["lilsis", "Boats on STILTS. There's a gap underneath. I noticed it first, before anybody."],
  "edo.village.boats.use.mom": ["mom", "Not ours, darling, and not going anywhere this morning. Nor, yet, are we."],
  "edo.village.boats.use.bigsis": ["bigsis", "I am not pushing a boat into the sea. Historically, that ends badly."],
  "edo.village.boats.use.lilsis": ["lilsis", "I pushed. It didn't go. It's a very SERIOUS boat."],
  "edo.village.underboat.mom": ["mom", "A gap under a boat. I know exactly who is looking at it."],
  "edo.village.underboat.bigsis": ["bigsis", "Sand, shade, barnacles. A crawl space with a view."],
  "edo.village.underboat.lilsis": ["lilsis", "I FIT. ...There's nothing under here but sand. Good sand, though."],
  "edo.village.underboat.use.mom": ["mom", "No, darling. A lady does not go under boats."],
  "edo.village.underboat.use.bigsis": ["bigsis", "I would fit. I decline. There is a difference."],
  "edo.village.underboat.use.lilsis": ["lilsis", "Been under. Came out. Nothing but a crab, and we're FRIENDS now."],
  // the net racks, and O-Masa at them
  "edo.village.nets.mom": ["mom", "Nets drying on bamboo, and a woman mending them who misses nothing."],
  "edo.village.nets.bigsis": ["bigsis", "Nets on racks. A net is mostly holes, arranged. I find that encouraging."],
  "edo.village.nets.lilsis": ["lilsis", "Nets! Like a GIANT spiderweb. For fish. Fish spiders."],
  "edo.village.nets.use.mom": ["mom", "They're her nets. We don't touch another woman's work."],
  "edo.village.nets.use.bigsis": ["bigsis", "I would only tangle it. I once tangled a phone charger inside a closed drawer."],
  "edo.village.nets.use.lilsis": ["lilsis", "I got my boot in it. I got my boot OUT of it. Nobody saw."],
  // the notice-board place at the village entrance: boards of dense writing under a little roof. Before Sankichi reads it:
  "edo.village.board.mom": ["mom", "Notices under a roof. A town that puts a roof on its rules means them."],
  "edo.village.board.bigsis": ["bigsis", "Writing. Columns of it. I cannot read it. I cannot read ANY of it."],
  "edo.village.board.bigsis.2": ["bigsis", "I am illiterate. So this is what illiterate feels like. ...I do not care for it."],
  "edo.village.board.lilsis": ["lilsis", "Signs! What do they say? ...Nobody knows. That's a first."],
  "edo.village.board.use.mom": ["mom", "I can't read it, and I won't pretend to. We'll ask someone who can."],
  "edo.village.board.use.bigsis": ["bigsis", "Ask the boy. He can read. ...I used to be able to read."],
  "edo.village.board.use.lilsis": ["lilsis", "I'll ask the boy. Boys who can read LOVE being asked."],
  // after Sankichi has read the Kirishitan board (edo.boardRead)
  "edo.village.board2.mom": ["mom", "The left one: silver, for telling on people who pray as we do. Now we know."],
  "edo.village.board2.bigsis": ["bigsis", "The Kirishitan board. A hundred and nineteen years old, by the look of it."],
  "edo.village.board2.bigsis.2": ["bigsis", "...I cannot read it, so that is a guess. I am allowed one."],
  "edo.village.board2.lilsis": ["lilsis", "That's the mean sign. I'm not looking at it. ...I looked. Still mean."],
  "edo.village.board2.use.mom": ["mom", "We leave it exactly as it is, girls. It isn't ours to answer."],
  "edo.village.board2.use.bigsis": ["bigsis", "Touching a government notice, in a country where I cannot read the fine print."],
  "edo.village.board2.use.lilsis": ["lilsis", "I'm not touching the mean sign. I'm touching the ROOF of it. That's allowed."],
  // the roofs, weighted with stones
  "edo.village.roofs.mom": ["mom", "Stones on the shingles to hold them down. Sensible people. I like them already."],
  "edo.village.roofs.bigsis": ["bigsis", "Stones on the roofs against the wind. Somebody here has thought about weather."],
  "edo.village.roofs.lilsis": ["lilsis", "Rocks on the roof! Did they fall UP?"],
  "edo.village.roofs.use.mom": ["mom", "Not a roof, darling. I have a daughter for that, and I'm not asking her."],
  "edo.village.roofs.use.bigsis": ["bigsis", "The stones are doing a job. I will not relieve them of it."],
  "edo.village.roofs.use.lilsis": ["lilsis", "I can't reach a single rock. ...Mommy said no, anyway."],
  // smoke from a kitchen
  "edo.village.smoke.mom": ["mom", "Woodsmoke. Somebody's cooking breakfast, and it isn't us. More's the pity."],
  "edo.village.smoke.bigsis": ["bigsis", "Smoke going straight up. No wind yet. Sailors mind that more than I do."],
  "edo.village.smoke.lilsis": ["lilsis", "Smoke means FOOD. I can smell it from here. Fish food."],
  "edo.village.smoke.use.mom": ["mom", "One can't do much with smoke but follow it."],
  "edo.village.smoke.use.bigsis": ["bigsis", "I tried to read it. There was nothing to read. That has been the morning."],
  "edo.village.smoke.use.lilsis": ["lilsis", "I sniffed it. It's fish. I was RIGHT."],
  // the hen yard, behind a low fence: every hen facing west along the coast
  "edo.village.hens.mom": ["mom", "Hens, every one of them facing the same way. I've seen this before. In Nevada."],
  "edo.village.hens.bigsis": ["bigsis", "Five hens in a row, every one facing west. I am not going to say it."],      // SCENES-20A: "Six": the yard has five (PAINT-20A; her names for them, edo.west.bye.6)
  "edo.village.hens.lilsis": ["lilsis", "Chickens! ...They're all looking the same way. Chickens KNOW."],
  "edo.village.hens.use.mom": ["mom", "They aren't mine to talk to, sweetheart. They're yours."],
  "edo.village.hens.use.bigsis": ["bigsis", "The hens do not listen to me. No hen ever has. It is a matter of record."],
  "edo.village.hens.use.lilsis": ["lilsis", "Hi, chickens. It's me. Where are you all LOOKING?"],
  "edo.village.fence.mom": ["mom", "A fence a hen could step over, and not one of them has."],
  "edo.village.fence.bigsis": ["bigsis", "A low fence. It is not keeping anything in. It is keeping a line."],
  "edo.village.fence.lilsis": ["lilsis", "A fence exactly my height. Somebody built it for ME."],
  "edo.village.fence.use.mom": ["mom", "I'll stand on this side of it, darling. The hens are on duty."],
  "edo.village.fence.use.bigsis": ["bigsis", "I could step over it. The hens would have opinions."],
  "edo.village.fence.use.lilsis": ["lilsis", "I'm leaning on it. That's what fences are FOR."],
  // the cherry by the shrine path, past its best, dropping petals
  "edo.village.cherry.mom": ["mom", "A cherry, nearly over. The petals are coming down like the end of a play."],
  "edo.village.cherry.bigsis": ["bigsis", "A cherry past its best. Cherries bloom here at the start of April. So: April."],
  "edo.village.cherry.lilsis": ["lilsis", "It's SNOWING pink. On my head. I'm keeping some."],
  "edo.village.cherry.use.mom": ["mom", "Don't shake it, girls. It has little enough left."],
  "edo.village.cherry.use.bigsis": ["bigsis", "I shook it. Forty petals, roughly. I counted in fours."],
  "edo.village.cherry.use.lilsis": ["lilsis", "I shook it! Now it's snowing MORE. You're welcome, everybody."],
  "edo.village.shrinepath.mom": ["mom", "A little path up the slope, swept this morning. Somebody's holy place."],
  "edo.village.shrinepath.bigsis": ["bigsis", "A path to a shrine. We are not going up it. It is not ours."],
  "edo.village.shrinepath.lilsis": ["lilsis", "A path! Where does it GO? ...Mommy says not today."],
  "edo.village.shrinepath.use.mom": ["mom", "Not today, girls. We're guests here, and guests stay where they're put."],
  "edo.village.shrinepath.use.bigsis": ["bigsis", "I will look from the bottom. Looking from the bottom offends no one."],
  "edo.village.shrinepath.use.lilsis": ["lilsis", "I went up THREE steps. Then I came back. That counts as visiting."],
  // the gulls
  "edo.village.gulls.mom": ["mom", "Gulls. The same gulls as home, as far as I can tell. They've not changed a note."],
  "edo.village.gulls.bigsis": ["bigsis", "Gulls. They sound exactly like gulls. Something here I can read."],
  "edo.village.gulls.lilsis": ["lilsis", "Seagulls! They're not chickens. But they're TRYING."],
  "edo.village.gulls.use.mom": ["mom", "I have nothing to feed them, and they know it."],
  "edo.village.gulls.use.bigsis": ["bigsis", "One does not use a gull. A gull uses you."],
  "edo.village.gulls.use.lilsis": ["lilsis", "I waved. One waved back. With its WHOLE body."],
  // Kihei's shop front, and its curtain (the noren) lifting in the wind
  "edo.village.shop.mom": ["mom", "A fish shop, open to the street, with a curtain for a door. We'll ask inside."],
  "edo.village.shop.bigsis": ["bigsis", "A shop. There is writing on the curtain. I can tell you it is blue."],
  "edo.village.shop.lilsis": ["lilsis", "A shop with a CURTAIN door! You just walk through it. I'm walking through it."],
  "edo.village.shop.use.mom": ["mom", "Heads down under the curtain, girls. We're going in politely."],
  "edo.village.shop.use.bigsis": ["bigsis", "In, through a curtain I cannot read. The theme of the day continues."],
  "edo.village.shop.use.lilsis": ["lilsis", "I'm going IN. It smells like fish. Good fish."],
  // the road: the Tōkaidō, along the shore; and the Satta pass rising to the west
  "edo.village.road.mom": ["mom", "A road along the shore, both ways. Two directions is one more than Nevada had."],
  "edo.village.road.bigsis": ["bigsis", "A road with proper traffic: a man, a hat, a horse. The main road, I would wager."],
  "edo.village.road.lilsis": ["lilsis", "A road! Is it the road to our house? ...It's not. I can tell by the dirt."],
  "edo.village.road.use.mom": ["mom", "We're not walking anywhere until we know which way, darling."],
  "edo.village.road.use.bigsis": ["bigsis", "Walking a road in a direction I cannot name. No. Not yet."],
  "edo.village.road.use.lilsis": ["lilsis", "I walked FIVE steps that way. It's still a road. I came back."],
  "edo.village.pass.mom": ["mom", "The road climbs over that hill and drops out of sight. West, I think."],
  "edo.village.pass.bigsis": ["bigsis", "A pass. The road goes up and over. The view from the top is probably famous."],
  "edo.village.pass.lilsis": ["lilsis", "A HILL. The road goes up it. I bet there's a snack at the top."],
  "edo.village.pass.use.mom": ["mom", "That's a long way up in a dress, sweetheart, and a longer way in sandals."],
  "edo.village.pass.use.bigsis": ["bigsis", "I will climb it when somebody tells me what is on the other side."],
  "edo.village.pass.use.lilsis": ["lilsis", "I started climbing. Mommy said not without her. I'm WAITING."],
  // the well
  "edo.village.well.mom": ["mom", "A well, with a bucket on a rope. Everyone here drinks from the same place."],
  "edo.village.well.bigsis": ["bigsis", "A well. Bucket, rope, pulley. The oldest machine I know how to work."],
  "edo.village.well.lilsis": ["lilsis", "A WELL. Can I shout in it? ...I shouted in it. It shouted back."],
  "edo.village.well.use.mom": ["mom", "I'd ask before I drew from somebody's well. There's a lady with a basket to ask."],
  "edo.village.well.use.bigsis": ["bigsis", "I drew half a bucket and put it back. I am not thirsty enough to be rude."],
  "edo.village.well.use.lilsis": ["lilsis", "The bucket's heavier than me. I'm small but mighty, and it's mightier."],
  // the sand
  "edo.village.sand.mom": ["mom", "Gray sand, and three sets of footprints that nobody here will recognize."],
  "edo.village.sand.bigsis": ["bigsis", "Our footprints end where the door was. A circle, and then nothing. Noted."],
  "edo.village.sand.lilsis": ["lilsis", "My boots make the BEST prints. Everybody else's are boring."],
  "edo.village.sand.use.mom": ["mom", "No castles today, darling. We have somewhere to be, even if I don't know where."],
  "edo.village.sand.use.bigsis": ["bigsis", "I wrote the date in it. Then I remembered that I do not know the date."],
  "edo.village.sand.use.lilsis": ["lilsis", "I drew a chicken. It's a GOOD chicken. The sea can have it."],
  // the villagers: a net-mender, and the woman with the basket
  "edo.village.netmender.mom": ["mom", "An old man mending a net, trying very hard not to look at us. He's bad at it."],
  "edo.village.netmender.bigsis": ["bigsis", "He has looked at us eleven times and mended one knot. I counted both."],
  "edo.village.netmender.lilsis": ["lilsis", "That man's fixing a net with his TOES. I want to learn that."],
  "edo.village.netmender.say.1": ["netmender", "Morning. ...Big morning. Big strangers. Big mountain. Same mountain."],
  "edo.village.netmender.say.2": ["netmender", "Forty years on this beach, and the mountain never once surprised me. You did."],
  "edo.village.netmender.say.3": ["netmender", "Ask Kihei. Kihei feeds everybody. Ask him before his wife asks you."],
  "edo.village.basketwoman.mom": ["mom", "The lady who left her basket. She's come back for it, and for a second look."],
  "edo.village.basketwoman.bigsis": ["bigsis", "She dropped her basket at the sight of us. In her place, I would have too."],
  "edo.village.basketwoman.lilsis": ["lilsis", "That's the basket lady! She came BACK. I knew she would."],
  "edo.village.basketwoman.say.1": ["basketwoman", "My basket. Thank you for not taking it. ...Most people would say something now."],
  "edo.village.basketwoman.say.2": ["basketwoman", "The tall one is taller than my husband. Do not tell him. He is proud of it."],
  "edo.village.basketwoman.say.3": ["basketwoman", "Kihei's wife will have you in a kimono before the fish is cut. Let her."],
  // Sankichi, beside the board; Tokuzō on his rounds; Gonroku by his boat; O-Masa at the racks; Kihei, when he is out front
  "edo.village.sankichi.mom": ["mom", "A boy by the notices, reading them. Out loud, to anyone who'll stand still."],
  "edo.village.sankichi.bigsis": ["bigsis", "A boy of about nine. He can read. I have never envied anyone more."],
  "edo.village.sankichi.lilsis": ["lilsis", "A boy! He's looking at my BOOTS. Everybody looks at my boots."],
  "edo.village.tokuzo.mom": ["mom", "A clerk with a paper, going door to door and squinting at each one."],
  "edo.village.tokuzo.bigsis": ["bigsis", "A man with a brush and a paper, peering. He cannot see us from there. Good."],
  "edo.village.tokuzo.lilsis": ["lilsis", "That man's squinting at EVERYTHING. He needs glasses. We should tell him."],
  "edo.village.gonroku.mom": ["mom", "The captain, by his boat, looking at the sky as if it owed him money."],
  "edo.village.gonroku.bigsis": ["bigsis", "The captain. He has been reading the sky for an hour and not liking the ending."],
  "edo.village.gonroku.lilsis": ["lilsis", "The boat man. He frowns at the SKY. The sky didn't do anything."],
  "edo.village.masa.mom": ["mom", "The woman at the nets. Everyone here looks to her before they do a thing."],
  "edo.village.masa.bigsis": ["bigsis", "She mends and watches. The captain glanced at her twice. She did not look back."],
  "edo.village.masa.lilsis": ["lilsis", "The net lady. She's the BOSS of the beach. I can tell. Bosses don't look up."],
  "edo.village.kihei.mom": ["mom", "The fishmonger, out front in a red vest and hood. Someone makes him wear that."],
  "edo.village.kihei.bigsis": ["bigsis", "A red vest and a red hood, in April. There will be a reason. There always is."],
  "edo.village.kihei.lilsis": ["lilsis", "A man in a red hat! He looks grumpy. Grumpy people give the best fish."],

  // ======================================================================================================
  // THE SHOP (edo-fishshop): inside Kihei's. The looks, and the uses, for each thing, for each of the three.
  // ======================================================================================================
  // Kihei at his cutting board
  "edo.shop.kihei.mom": ["mom", "Big hands, few words, a red hood. He's decided about us. I don't know which way."],
  "edo.shop.kihei.bigsis": ["bigsis", "He has said four words since we came in. All of them were 'Sit.'"],
  "edo.shop.kihei.lilsis": ["lilsis", "The fish man. He hasn't smiled ONCE. I'm going to fix that. It's my job now."],
  // O-Tami at her place (with the baby on her back, until it sleeps); married, teeth blackened: Big Sister's fact
  "edo.shop.tami.mom": ["mom", "She runs this shop, that man and a baby, and still has an eye to spare for us."],
  "edo.shop.tami.bigsis": ["bigsis", "Black teeth. Married women do that here. I read it once and did not believe it."],
  "edo.shop.tami.lilsis": ["lilsis", "The baby lady. She talks FAST. I like her. We're the same speed."],
  // the baby, on O-Tami's back (awake and fussing); then asleep in its basket
  "edo.shop.baby.mom": ["mom", "A baby who has not slept, on the back of a mother who hasn't either."],      // SCENES-20A: "in a basket": she is on O-Tami's back till she sleeps
  "edo.shop.baby.bigsis": ["bigsis", "A baby. It is not crying. It is thinking about it, out loud."],
  "edo.shop.baby.lilsis": ["lilsis", "A baby. Can I hold it? I'm good at holding. I carried an EGG all across Nevada."],
  "edo.shop.baby.use.mom": ["mom", "May I? ...Thank you. Come here, little one. We'll see about this."],
  "edo.shop.baby.use.bigsis": ["bigsis", "I offered to read to her. Then I remembered. ...Mom is better at babies anyway."],
  "edo.shop.baby.use.lilsis": ["lilsis", "I made my chicken face at her. She stopped crying to STARE. That's progress."],
  "edo.shop.baby2.mom": ["mom", "Asleep. In the middle of a sentence, as it happens. Mine."],
  "edo.shop.baby2.bigsis": ["bigsis", "Asleep. Mom hummed four bars and the whole shop went quiet. The cat, too."],
  "edo.shop.baby2.lilsis": ["lilsis", "Shh. She's asleep. Mommy did it. Mommy can do it to ANYBODY."],
  "edo.shop.baby2.use.mom": ["mom", "We're not waking her, girls. Not for anything on this earth."],
  "edo.shop.baby2.use.bigsis": ["bigsis", "I am not touching a sleeping baby. I have a sister. I know what happens."],
  "edo.shop.baby2.use.lilsis": ["lilsis", "I just LOOKED. Looking's allowed. ...I'm done looking."],
  // the cat, at her place; and once she has gone under the floor with the mackerel
  "edo.shop.cat.mom": ["mom", "A cat, watching the cutting board the way your father watches a grill."],
  "edo.shop.cat.bigsis": ["bigsis", "A cat with her eye on the mackerel. She has a plan. Cats always have a plan."],
  "edo.shop.cat.lilsis": ["lilsis", "A CAT! Hi, cat. ...She's not a chicken, but she's got a good face."],
  "edo.shop.cat.use.mom": ["mom", "I'm not picking up a working cat, darling. She's on duty."],
  "edo.shop.cat.use.bigsis": ["bigsis", "I put out a hand. She considered it, and declined. Fair."],
  "edo.shop.cat.use.lilsis": ["lilsis", "I petted her ONE time. She allowed it. We have an understanding."],
  "edo.shop.cat2.mom": ["mom", "The cat has gone under the floor with our lunch. I admire her nerve."],
  "edo.shop.cat2.bigsis": ["bigsis", "Under the floor with a whole mackerel. An excellent plan, perfectly executed."],
  "edo.shop.cat2.lilsis": ["lilsis", "She went under. With the fish. I know that gap. That gap is MINE."],
  // the tubs of fish
  "edo.shop.tubs.mom": ["mom", "Tubs of fish in water, and one of them keeps jumping. I'd rather it didn't."],
  "edo.shop.tubs.bigsis": ["bigsis", "Saba. That is mackerel. Of my forty words of Japanese, it is the most useful."],
  "edo.shop.tubs.lilsis": ["lilsis", "FISH. Alive ones. One jumped. He's my favorite. I'm calling him Jumpy."],
  "edo.shop.tubs.use.mom": ["mom", "I'm not putting my hand in a fish tub, darling. I have standards and no towel."],
  "edo.shop.tubs.use.bigsis": ["bigsis", "I touched one. It touched me back. We have both agreed not to do that again."],
  "edo.shop.tubs.use.lilsis": ["lilsis", "I tried to pet Jumpy. Jumpy JUMPED. That's his whole thing."],
  // the cutting board, and the mackerel on it
  "edo.shop.cuttingboard.mom": ["mom", "A long board, worn hollow, and a knife I intend to stay well away from."],
  "edo.shop.cuttingboard.bigsis": ["bigsis", "A cutting board worn into a valley down the middle. Decades of mackerel."],
  "edo.shop.cuttingboard.lilsis": ["lilsis", "That's where he CHOPS. I'm not allowed near chopping. ...I'm near it."],
  "edo.shop.cuttingboard.use.mom": ["mom", "No. That is his, and it is sharp, and we are guests."],
  "edo.shop.cuttingboard.use.bigsis": ["bigsis", "I do not touch other people's knives. It is nearly a rule of civility."],
  "edo.shop.cuttingboard.use.lilsis": ["lilsis", "I reached for the fish. The fish man made a NOISE. I stopped."],
  // the wooden sushi box and its press
  "edo.shop.sushibox.mom": ["mom", "A wooden box with a lid that fits inside it. For pressing something, I'd say."],
  "edo.shop.sushibox.bigsis": ["bigsis", "A box, a lid, a weight. A press. Whatever it makes, it makes it flat."],
  "edo.shop.sushibox.lilsis": ["lilsis", "A little wooden box. Is it a BED? For the fish?"],
  "edo.shop.sushibox.use.mom": ["mom", "I'd only press the wrong thing. We'll watch the man who knows how."],
  "edo.shop.sushibox.use.bigsis": ["bigsis", "I pressed the lid. It pressed nothing. It wants rice, fish and a man's weight."],
  "edo.shop.sushibox.use.lilsis": ["lilsis", "I pushed the lid down. Nothing happened. It needs FISH in it first."],
  // the hearth and its pot
  "edo.shop.hearth.mom": ["mom", "A fire in the floor, a pot over it, rice in the pot. Breakfast, for somebody."],
  "edo.shop.hearth.bigsis": ["bigsis", "A hearth sunk in the floor, and a pot of rice. Vinegared rice, by the smell."],
  "edo.shop.hearth.lilsis": ["lilsis", "A fire IN the floor! And a pot. It smells like rice and something sour."],
  "edo.shop.hearth.use.mom": ["mom", "I don't stir another woman's pot. We'll be offered, or we won't."],
  "edo.shop.hearth.use.bigsis": ["bigsis", "I warmed my hands. That is the entire extent of what I know to do with it."],
  "edo.shop.hearth.use.lilsis": ["lilsis", "I warmed my hands. Then my boots. The boots smelled a little. I stopped."],
  // the fish hung to dry
  "edo.shop.driedfish.mom": ["mom", "Fish hung up to dry, in rows, like washing nobody wants to wear."],
  "edo.shop.driedfish.bigsis": ["bigsis", "Dried fish. Bonito, perhaps. I would check, if I could read a label here."],
  "edo.shop.driedfish.lilsis": ["lilsis", "Flat fish on strings! They look SURPRISED."],
  "edo.shop.driedfish.use.mom": ["mom", "Not ours, darling. And not, I think, breakfast."],
  "edo.shop.driedfish.use.bigsis": ["bigsis", "I touched one. It is as hard as a shoe. A fish shoe."],
  "edo.shop.driedfish.use.lilsis": ["lilsis", "I poked one. It swung. They ALL swung. Like a fish wind chime."],
  // the print of Fuji pinned up, in the new blue (a design of the game's own): #21's third clue
  "edo.shop.print.mom": ["mom", "A picture of the mountain, pinned up. That blue is the bluest thing in the room."],
  "edo.shop.print.bigsis": ["bigsis", "A print. Fuji, and a sky in a deep, deep blue. That blue is not an old blue."],
  "edo.shop.print.lilsis": ["lilsis", "A picture of the big mountain! It's SO blue. Bluer than real."],
  "edo.shop.print.use.mom": ["mom", "I'm not taking a man's picture off his wall. We'll admire it where it hangs."],
  "edo.shop.print.use.bigsis": ["bigsis", "I looked closer. It is printed, not painted. Someone made hundreds of these."],
  "edo.shop.print.use.lilsis": ["lilsis", "I touched the blue. It didn't come off. It's REALLY in there."],
  // Kihei's word for it, the first time any of them looks (the scene says it once), and Big Sister's fact
  "edo.shop.print.kihei": ["kihei", "Everybody in Edo wants pictures of the mountain this year. In that new blue."],
  "edo.shop.print.clue": ["bigsis", "New. He said new. That is Prussian blue. Their printers have only just got it."],
  "edo.shop.print.clue.2": ["bigsis", "A picture, printed in a blue that is new this year. Hold that thought, everyone."],
  // the money box: strings of square-holed copper coins: #21's second clue
  "edo.shop.money.mom": ["mom", "A box of coins on strings, each with a square hole. Money you carry on a cord."],
  "edo.shop.money.bigsis": ["bigsis", "Copper coins with square holes, on cords. I have seen one in a museum case."],
  "edo.shop.money.lilsis": ["lilsis", "Money with HOLES in it! Like cereal. Can you eat it? ...No. I checked."],
  "edo.shop.money.use.mom": ["mom", "Another man's money box. We look. We don't touch. That's the whole of it."],
  "edo.shop.money.use.bigsis": ["bigsis", "I am not touching his money. I am barely touching his floor."],
  "edo.shop.money.use.lilsis": ["lilsis", "I didn't touch it. I WANTED to. Wanting's free."],
  "edo.shop.money.clue": ["bigsis", "Kan'ei Tsūhō. The label said Edo period: sixteen-thirties to eighteen-sixties."],
  "edo.shop.money.clue.2": ["bigsis", "So: a tiger year, in the Edo period. We are narrowing it down. Slowly."],
  // the god-shelf, high on the wall
  "edo.shop.godshelf.mom": ["mom", "A little shelf high up, kept very clean. Theirs. We'll leave it be."],
  "edo.shop.godshelf.bigsis": ["bigsis", "That is a shelf for a god. I am not going to touch it, and I will tell you why."],
  "edo.shop.godshelf.bigsis.2": ["bigsis", "Because it is not mine, and because I cannot read what it says."],
  "edo.shop.godshelf.lilsis": ["lilsis", "A tiny shelf up high with nothing on it but a cup. Is it for the CAT?"],
  "edo.shop.godshelf.use.mom": ["mom", "No, darling. It isn't ours, and we don't pretend about it."],
  "edo.shop.godshelf.use.bigsis": ["bigsis", "No. I said I would tell you why, and I did."],
  "edo.shop.godshelf.use.lilsis": ["lilsis", "I can't reach it anyway. It's for tall people's gods."],
  // the raised room at the back, with its step, where guests are fed
  "edo.shop.step.mom": ["mom", "A raised floor of straw mats, and a step up to it. Shoes off, I think."],
  "edo.shop.step.bigsis": ["bigsis", "A step up to a room of mats. Every pair of shoes stops at the step. Noted."],
  "edo.shop.step.lilsis": ["lilsis", "A step! You sit on it. I'm sitting on it. ...I'm REALLY sitting on it."],
  "edo.shop.step.use.mom": ["mom", "We sit when we're asked, girls. Not before."],
  "edo.shop.step.use.bigsis": ["bigsis", "I will sit when I am invited. I am not invited. I am standing."],
  "edo.shop.step.use.lilsis": ["lilsis", "I sat. Nobody said no. ...The cat sat too. We're a club."],
  // the open front: the street, the bay, Fuji in the opening
  "edo.shop.street.mom": ["mom", "The whole front of the shop is a window with no glass. Anyone can see in."],
  "edo.shop.street.bigsis": ["bigsis", "Street, bay, Fuji, framed. Everyone who passes gets the picture, and us in it."],
  "edo.shop.street.lilsis": ["lilsis", "You can see the mountain from INSIDE. This shop has the best wall."],
  "edo.shop.street.use.mom": ["mom", "I'll stand back from the street, darling. We're conspicuous enough as it is."],
  "edo.shop.street.use.bigsis": ["bigsis", "Standing in the opening would be standing on a stage. I am not dressed for it."],
  "edo.shop.street.use.lilsis": ["lilsis", "I waved at the street. A man squinted at me. I came back in."],
  // the noren, from inside
  "edo.shop.noren.mom": ["mom", "The curtain, from behind. The one thing in here that moves and isn't a fish."],
  "edo.shop.noren.bigsis": ["bigsis", "The curtain, backwards. I cannot read it backwards either. I checked."],
  "edo.shop.noren.lilsis": ["lilsis", "The curtain door! You can hide behind it. I found that out EARLY."],
  "edo.shop.noren.use.mom": ["mom", "Behind the curtain is the street, and in the street is a man with a paper."],
  "edo.shop.noren.use.bigsis": ["bigsis", "I looked out through the gap. Nobody looked back. That is the goal."],
  "edo.shop.noren.use.lilsis": ["lilsis", "I peeked through. The clerk man's out there. Squinting at a WALL."],
  // the straw sandals hung for sale; the sedge hats
  "edo.shop.sandals.mom": ["mom", "Straw sandals, hung in pairs. Her price, I imagine, is 'put them on.'"],
  "edo.shop.sandals.bigsis": ["bigsis", "Straw sandals. Flat, tied with cord. A pair would not last a week."],
  "edo.shop.sandals.lilsis": ["lilsis", "Shoes made of GRASS. Mine are made of boot. Boot is better."],
  "edo.shop.sandals.use.mom": ["mom", "I'd buy a pair, if I had a coin with a hole in it. We have three without."],      // SCENES-20A: "I have": the three pennies are Little Sister's (Mom says only what is so)
  "edo.shop.sandals.use.bigsis": ["bigsis", "I tried one against my foot. My foot is from another century. It showed."],
  "edo.shop.sandals.use.lilsis": ["lilsis", "I'm not swapping. They're my BOOTS. End of discussion."],
  "edo.shop.hats.mom": ["mom", "Wide hats of woven sedge. Whoever is under one of those is nobody's business."],
  "edo.shop.hats.bigsis": ["bigsis", "A sedge hat is a small roof. Under one, nobody is anybody in particular."],
  "edo.shop.hats.lilsis": ["lilsis", "Hats like UPSIDE-DOWN bowls. I want the biggest one."],
  "edo.shop.hats.use.mom": ["mom", "I'd be glad of one. I'll be gladder if it's offered."],
  "edo.shop.hats.use.bigsis": ["bigsis", "I tried one on. Suddenly I was nobody. I could get used to nobody."],
  "edo.shop.hats.use.lilsis": ["lilsis", "I put one on. It came down to my CHIN. I can see my feet, and that's all."],
  // O-Tami's clothes chest
  "edo.shop.chest.mom": ["mom", "A clothes chest, closed. Whatever's in it was folded by someone who means it."],
  "edo.shop.chest.bigsis": ["bigsis", "A chest. Clothes, by the smell of cedar. Old ones, kept for a reason."],
  "edo.shop.chest.lilsis": ["lilsis", "A big box! Is it treasure? ...It's clothes. Clothes aren't treasure. Usually."],
  "edo.shop.chest.use.mom": ["mom", "Another woman's chest stays shut until she opens it. She will, if we're patient."],
  "edo.shop.chest.use.bigsis": ["bigsis", "I do not open other people's drawers. Chests are large drawers."],
  "edo.shop.chest.use.lilsis": ["lilsis", "I lifted the lid ONE inch. The baby lady looked at me. I put it down."],
  // the gap under the raised floor: the cat's way, and Little Sister's
  "edo.shop.under.mom": ["mom", "A gap under the floor. Dark, dusty, and already spoken for."],
  "edo.shop.under.bigsis": ["bigsis", "A gap under the mats. Cat-sized. Also, regrettably, sister-sized."],
  "edo.shop.under.lilsis": ["lilsis", "A gap under the floor! I'd FIT. I haven't tried yet. I just know."],
  "edo.shop.under.use.mom": ["mom", "Absolutely not, darling. Not unless there's a reason."],
  "edo.shop.under.use.bigsis": ["bigsis", "I could get my head in. My head is not the part that worries me."],
  "edo.shop.under.use.lilsis": ["lilsis", "Nothing under there yet but dust and the cat's SPARE fish bones."],

  // ======================================================================================================
  // #22 OUT OF SIGHT, the scripted moments: the clerk's first pass (O-Tami pulls them in; the weather), the baby, the
  // kimonos, and Little Sister's boots. The clerk himself is tokuzoTree.
  // ======================================================================================================
  // (1) the first time Tokuzō turns into the street: O-Tami has the three of them in behind the noren in one movement
  "edo.shop.pass.1": ["tami", "In. In, in, in. Behind the curtain, all of you, and not a word."],
  "edo.shop.pass.2": ["lilsis", "Why are we--"],
  "edo.shop.pass.3": ["mom", "Because she asked us to, sweetheart, and when a lady asks that quickly, we go."],
  // she stands in the opening, her back to them, and talks to the clerk about the weather until he has gone by
  "edo.shop.pass.4": ["tami", "Good morning, clerk. A fine one. The wind has gone round to the west."],
  "edo.shop.pass.5": ["tokuzo", "Has it? ...So it has. Forgive me. Nothing unusual on your street, O-Tami?"],
  "edo.shop.pass.6": ["tami", "Fish, clerk, and wind. The same as every morning since my grandmother's day."],
  "edo.shop.pass.7": ["tokuzo", "Fish and wind. ...I will write 'nothing'. It is shorter."],
  // his back goes past the opening; she turns round
  "edo.shop.pass.8": ["tami", "The headman has had a paper. Strangers on the beach at dawn, in strange clothes."],
  "edo.shop.pass.9": ["tami", "I do not know any strangers. I know three travellers in want of proper clothes."],
  "edo.shop.pass.10": ["tami", "And I have a baby who has not slept in three days. Three days, every hour."],
  "edo.shop.pass.11": ["mom", "Then one thing at a time, if you'll let us. Which shall it be first?"],
  "edo.shop.pass.12": ["tami", "...Ask me again when I have slept."],
  // (2) the baby: Mom asks, and is handed the baby; she rocks her and hums a tune of her own, no words (a stage
  // direction, not a line); the baby sleeps in the middle of a sentence
  "edo.shop.baby.1": ["mom", "May I hold her? I've raised three. The arms never quite forget the shape."],
  "edo.shop.baby.2": ["tami", "Take her, with my blessing. Take her as far as Edo, if she will sleep there."],
  "edo.shop.baby.3": ["tami", "She will not have the hearth side, nor the street side, she will not--"],
  // asleep. O-Tami looks at Mom as at a sorceress
  "edo.shop.baby.4": ["tami", "...What did you DO."],
  "edo.shop.baby.5": ["mom", "I only found her key. She's a quarter-tone flat. So is my husband, bless him."],
  "edo.shop.baby.6": ["tami", "Do not stop humming. Do not ever leave. ...The chest. Come to the chest."],
  // (3) the kimonos, from her chest: Mom in emerald, Big Sister in indigo, Little Sister in pink; hats; sandals for two
  "edo.shop.dress.1": ["tami", "My mother's. She was not your height. Nobody is your height. Arms up."],
  "edo.shop.dress.2": ["mom", "Green. You've found me my own color, in a chest, in another century."],
  "edo.shop.dress.3": ["tami", "Indigo for the reader. It was long on me."],
  "edo.shop.dress.4": ["bigsis", "It ends at my knees."],
  "edo.shop.dress.5": ["tami", "Travellers tuck them up for the road anyway. You are only ahead of them."],
  "edo.shop.dress.6": ["tami", "Pink for the small one. And hats for all three. Keep your heads down under them."],
  "edo.shop.dress.7": ["tami", "Sandals. Fifteen mon a pair, good for a day or two of road. Yours, and yours."],
  "edo.shop.dress.8": ["lilsis", "What about ME?"],
  "edo.shop.dress.9": ["tami", "Nothing small enough. ...Off with the yellow ones, then. We will wrap your feet."],
  "edo.shop.dress.10": ["lilsis", "They're my BOOTS."],
  "edo.shop.dress.11": ["tami", "...So they are. Keep them. Nobody who sees them will believe their eyes anyway."],
  "edo.shop.dress.12": ["mom", "Thank you. Properly, and not for the last time."],
  "edo.shop.dress.13": ["tami", "Three travellers. Go and be travellers at the clerk before I think better of it."],
  // the three of them, dressed, looked at (the scene swaps story.see for these once edo.clothes is set)
  "edo.see.mom.bigsis": ["mom", "My eldest, in borrowed indigo, reading faces because she can't read signs."],
  "edo.see.mom.lilsis": ["mom", "My youngest: pink to the ankle, yellow boots beneath. Nobody will believe her."],
  "edo.see.bigsis.mom": ["bigsis", "Mom, in green, a head taller than every woman here. She has stopped apologizing."],
  "edo.see.bigsis.lilsis": ["bigsis", "My sister, in a kimono and rain boots. Two centuries at once, and happy in both."],
  "edo.see.lilsis.mom": ["lilsis", "Mommy in a green dress AGAIN. It's a different green dress. She's still Mommy."],
  "edo.see.lilsis.bigsis": ["lilsis", "My sister, in blue to her knees. She says it's too short. It's EXACTLY right."],
  // Little Sister in the street in her own clothes (before the kimonos: the wrong try)
  "edo.village.boots.lilsis": ["lilsis", "The boy says everybody's looking at my BOOTS. I think they're just jealous."],
  "edo.village.boots.mom": ["mom", "Then we'd better give them something duller to look at, sweetheart. Inside."],
  // #22 solved (tokuzoTree's end): the three of them, after he has gone home
  "edo.dressed.1": ["bigsis", "'From the east.' Mother. That was true."],
  "edo.dressed.2": ["mom", "It was, darling. Every syllable. That's the only reason you got away with it."],
  "edo.dressed.3": ["lilsis", "He didn't look at my boots ONCE. He can't see his own feet."],

  // ======================================================================================================
  // #21 WHERE, AND WHEN: Big Sister's solution, once the three clues are in (the red, the coins, the blue), said by her
  // whoever is playing; and the sum written down, if Dad's pencil meets the sticky note (not needed).
  // ======================================================================================================
  "edo.when.solve.1": ["bigsis", "A metal tiger. They come round once in sixty years, and the last one was 2010."],
  "edo.when.solve.2": ["bigsis", "Subtract sixty. Then sixty. Then sixty again: 1830."],
  "edo.when.solve.3": ["bigsis", "Edo coins: consistent. The new blue: consistent. It is 1830."],
  "edo.when.solve.4": ["lilsis", "Is 1830 good?"],
  "edo.when.solve.5": ["bigsis", "It is a year. A year is only a number until you know what happens in it."],
  "edo.when.solve.6": ["mom", "Then let's find out, girls. Politely, and one question at a time."],
  // the sum, written down with Dad's pencil on the sticky note (either on the other; any of the three can be holding them)
  "edo.when.sum.bigsis": ["bigsis", "2010, less sixty, less sixty, less sixty: 1830. Written down, it is a fact."],
  "edo.when.sum.mom": ["mom", "Your father's pencil, a sticky note and a date. He'd be pleased with all three."],
  "edo.when.sum.lilsis": ["lilsis", "I wrote 1830. It's the best 1830 anybody's ever written. Look at the 8."],
  // the sum tried before the clues are in
  "edo.when.sum.early": ["bigsis", "I would write the year down if I had one. I have a pencil and a feeling."],

  // ======================================================================================================
  // #23 KIHEI'S TABLE, the scripted meal (kiheiTree's hook `press` and after): the pressing, the grace, the bow, the
  // word, the title, the cat, the box. Nobody says itadakimasu: they bow to the god-shelf and say nothing.
  // ======================================================================================================
  // the pressing: rice, fish, lid, his weight on it, the cut (the player watches; Big Sister watches aloud)
  "edo.shop.meal.1": ["kihei", "Sit. Watch, if you like. Do not help."],
  "edo.shop.meal.2": ["lilsis", "I'm good at not helping. Ask my sister."],
  "edo.shop.meal.3": ["bigsis", "Rice into the box. Fish on the rice. Lid on the fish. And now he just... leans."],
  "edo.shop.meal.4": ["mom", "He's pressing it, like a flower in a book. Only this one you're allowed to eat."],
  "edo.shop.meal.5": ["bigsis", "Saba. Mackerel. That one I know. Pressed in a box, and cut like a cake."],
  "edo.shop.meal.6": ["bigsis", "In Edo, they have only lately begun to make it by hand, one piece at a time."],
  // on the step, in front of them; and he will take nothing for it
  "edo.shop.meal.7": ["kihei", "Eat first. Money is for after. There is no after for money today."],
  // Little Sister's grace, in her own words; Kihei and O-Tami wait, puzzled and polite
  "edo.shop.meal.8": ["lilsis", "Thank You for the fish, and for the fish man, and for his wife,"],
  "edo.shop.meal.9": ["lilsis", "and for the baby who's asleep now. Please keep her asleep. Amen."],
  // then they bow to the god-shelf, and say nothing, as their custom is
  "edo.shop.meal.10": ["mom", "Eat, girls. Slowly. ...All right. Not slowly."],
  // Little Sister, with the word from Sankichi (edo.arigato); Kihei's face does something nobody has seen it do
  "edo.shop.meal.11": ["lilsis", "Arigatō."],
  "edo.shop.meal.11.tami": ["tami", "...Husband. Your face."],
  "edo.shop.meal.11.kihei": ["kihei", "It does that."],
  // without the word yet (she comes back with it later: kiheiTree's `arigato`)
  "edo.shop.meal.11b": ["lilsis", "Thank you, fish man. I'll learn to say it YOUR way, and then I'll say it again."],
  // Mom thanks him properly; his answer gives the act its name, and Big Sister translates it once
  "edo.shop.meal.12": ["mom", "Thank you. You've fed three strangers who can't pay you, and asked us nothing."],
  "edo.shop.meal.13": ["kihei", "Okage-sama de."],
  "edo.shop.meal.14": ["bigsis", "It means 'thanks to you'. Or, more beautifully, 'by your grace'."],
  "edo.shop.meal.15": ["bigsis", "It is said when something good has happened and it was not only one's own doing."],
  // the cat takes a mackerel off the board and goes under the floor
  "edo.shop.meal.16": ["mom", "The cat has a mackerel."],
  "edo.shop.meal.17": ["kihei", "The cat always has a mackerel."],
  "edo.shop.meal.18": ["lilsis", "I FIT."],
  // under, and back, with the fish and a cobweb: that is how the family pays, in kind, by choice, after
  "edo.shop.meal.19": ["lilsis", "Got it. ...And a cobweb. The cobweb's free."],
  "edo.shop.meal.20": ["kihei", "...Nobody has ever got one back from that cat."],
  "edo.shop.meal.21": ["mom", "There. We've paid our way, after all. In fish."],
  "edo.shop.meal.22": ["kihei", "In MY fish."],
  "edo.shop.meal.23": ["mom", "After. As you said."],
  // O-Tami wraps the rest for the road (the sushibox)
  "edo.shop.meal.24": ["tami", "The rest goes with you. Do not argue. I am holding a baby, and I will win."],
  "edo.shop.meal.25": ["lilsis", "Arigatō. ...I said it to her too. It's for EVERYBODY now."],
  // Little Sister's pennies, offered to Kihei (kiheiTree, or the pennies used on him): the penny with no hole
  "edo.shop.penny.1": ["kihei", "No hole. How do you carry it?"],
  "edo.shop.penny.2": ["lilsis", "In my POCKET."],
  "edo.shop.penny.3": ["kihei", "Keep it in your pocket, then."],
  "edo.shop.penny.4": ["lilsis", "He gave it BACK. Grown-ups never give money back. I like him even more now."],
  // Little Sister comes back with the word, after the meal
  "edo.shop.arigato.1": ["lilsis", "Arigatō. For the fish. I've got the word now. The boy gave it to me."],
  "edo.shop.arigato.2": ["tami", "Husband. It is doing it again. Your face."],
  "edo.shop.arigato.3": ["kihei", "...Let it."],
  // the meal looked at, and after (the step, with the box and the cut pieces on it; then the empty step)
  "edo.shop.food.mom": ["mom", "Pressed mackerel on rice, cut square. Given, not sold. Eat it like a gift."],
  "edo.shop.food.bigsis": ["bigsis", "Pressed mackerel sushi. Sour, salt, cold fish. I may never eat anything else."],
  "edo.shop.food.lilsis": ["lilsis", "Fish on rice, in squares. Sour. I like sour. I had THREE."],
  "edo.shop.food.use.mom": ["mom", "One at a time, sweetheart. They're not going anywhere. ...They are. Slow down."],
  "edo.shop.food.use.bigsis": ["bigsis", "I took another. He nodded. I have never been so glad of a nod."],
  "edo.shop.food.use.lilsis": ["lilsis", "I'm eating it with my HANDS. The fish man does too. So it's manners."],

  // ======================================================================================================
  // #24 WEST: the hens (Little Sister's opening), Kihei's roads, Gonroku's no (gonrokuTree), O-Masa's question
  // (masaTree), and the goodbyes.
  // ======================================================================================================
  // Little Sister at the hen-yard fence: all of them facing west along the coast, as Jolene's faced the fence
  "edo.west.hens.1": ["lilsis", "They're all looking the same way. Every single one. That way."],
  "edo.west.hens.2": ["lilsis", "Chickens KNOW."],
  "edo.west.hens.3": ["bigsis", "West is a very large direction."],
  "edo.west.hens.4": ["mom", "Then we'll ask someone who knows the roads. Your fish man sees everything go by."],
  "edo.west.hens.again": ["lilsis", "Still west. They haven't moved. They're not going to move till WE do."],
  // the door they came through is gone (the ring on the sand: the arrival's mark, looked at)
  "edo.village.arrive.mom": ["mom", "This is where we came through. The air has healed over, like a pond."],
  "edo.village.arrive.bigsis": ["bigsis", "Where the door was. Nothing. Not a hum. We are going to have to find another."],
  "edo.village.arrive.lilsis": ["lilsis", "The door's GONE. I checked twice. Doors should stay where you leave them."],
  "edo.village.arrive.use.mom": ["mom", "I've tried the air, darling. It doesn't open from this side."],
  "edo.village.arrive.use.bigsis": ["bigsis", "I held the coin up. The sun is behind the mountain. Nothing. Noted, sadly."],
  "edo.village.arrive.use.lilsis": ["lilsis", "I knocked on the air. Nobody answered. The air's being RUDE."],
  // O-Masa goes down the beach to her husband (masaTree's hook `toGonroku`); what she says, the player hears the end of
  "edo.west.masa.1": ["masa", "...The Funadama is a lady. A lady likes company with manners."],
  // Gonroku, after a long look at the sea
  "edo.west.gonroku.1": ["gonroku", "...They sit in the stern, and they do not whistle."],
  "edo.west.gonroku.2": ["lilsis", "I can't whistle anyway. I've been TRYING for a year."],
  "edo.west.gonroku.3": ["bigsis", "The stern is the back. I know exactly one nautical term, and I have now used it."],
  "edo.west.gonroku.4": ["mom", "Thank you, both of you. We'll be no trouble, and quieter than you'd believe."],
  "edo.west.gonroku.5": ["gonroku", "The tide turns at first light. It waits for nobody, and I do not argue with it."],
  // the goodbyes: Kihei and O-Tami at the shop; Little Sister to the baby, the cat, and every hen by name
  "edo.west.bye.1": ["mom", "Thank you for the clothes, the table, the morning. I shan't forget one of them."],
  "edo.west.bye.2": ["tami", "Go west, and do not be tall at anybody. ...Come back when the baby can talk."],
  "edo.west.bye.3": ["kihei", "Stern. No whistling. Eat the box before it eats you."],
  "edo.west.bye.4": ["bigsis", "Thank you. I learned one word today and lost all the others. A fair trade."],
  "edo.west.bye.5": ["lilsis", "Bye, baby. Stay asleep. Bye, cat. Keep the OTHER fish."],
  "edo.west.bye.6": ["lilsis", "Bye, Peck. Bye, Dot. Bye, Other Dot. Bye, Fuji. Bye, Admiral. Bye, Jumpy."],
  "edo.west.bye.7": ["bigsis", "The hens do not have names."],
  "edo.west.bye.8": ["lilsis", "They do NOW. And Jumpy's a fish. He's an honorary chicken."],
  "edo.west.bye.9": ["sankichi", "Uncle Gonroku's boat? He never takes anybody. Never. ...Bring me back a story."],
  "edo.west.bye.10": ["lilsis", "I'll bring you back TWO. Arigatō for the word."],

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
  "edo.tami.first.1": ["tami", "Three of you, in that, on my street. ...Stand there. Do not be seen being tall."],
  // her menu
  "edo.tami.opt.clothes.mom": ["mom", "You said we needed proper clothes. I'd be very grateful for the loan."],
  "edo.tami.opt.clothes.big": ["bigsis", "About the clothes. I would very much like to stop being looked at."],
  "edo.tami.opt.clothes.lil": ["lilsis", "Do you have a dress in MY size? With pockets?"],
  "edo.tami.clothes.no.1": ["tami", "Dressing you takes two hands. I have a baby in one and this shop in the other."],
  "edo.tami.clothes.no.2": ["tami", "Get her to sleep, and I will dress you three like the lord's own daughters."],
  "edo.tami.clothes.no.lil": ["tami", "Pockets. ...No. Sleeves. Everything goes in the sleeves. You will like sleeves."],
  "edo.tami.clothes.yes": ["tami", "She is asleep, and I am a woman of my word. The chest. Quietly, now."],
  "edo.tami.clothes.done": ["tami", "You are dressed. What you do about the hair is between you and the hat."],
  "edo.tami.opt.baby.mom": ["mom", "May I try with the baby? I've had three. One of them was worse."],
  "edo.tami.opt.baby.big": ["bigsis", "I could read to the baby. ...I cannot read anything here. Never mind."],
  "edo.tami.opt.baby.lil": ["lilsis", "Can I hold the baby? I'm SEVEN. And a half."],
  "edo.tami.baby.big": ["tami", "She cannot read either. You would be good company for each other."],
  "edo.tami.baby.lil": ["tami", "Seven and a half may hold the basket, when she sleeps in it. That is the rule."],      // SCENES-20A: "The baby stays in it": she is on O-Tami's back till she sleeps
  "edo.tami.baby.lil.2": ["lilsis", "...I'll hold the basket. I'm a very good basket holder."],
  "edo.tami.baby.done": ["tami", "Asleep. Still asleep. Keep your voice down, and I will give you the shop."],
  "edo.tami.opt.red.mom": ["mom", "May I ask why your husband wears red? It suits him, but I'm curious."],
  "edo.tami.opt.red.big": ["bigsis", "Why does your husband wear red? The vest and the hood. In April."],
  "edo.tami.opt.red.lil": ["lilsis", "Why's the fish man in a red hat? Is he the BOSS?"],
  "edo.tami.red.1": ["tami", "He is sixty. A tiger year, the metal one, the same as the year he was born."],
  "edo.tami.red.2": ["tami", "When your own year comes round again, you are a baby again. So: red. All year."],
  "edo.tami.red.3": ["tami", "He hates it. I made the hood myself, so he hates the hood most of all."],
  "edo.tami.red.big": ["bigsis", "Sixty years, and the same sign comes round. A metal tiger. That I can work with."],
  "edo.tami.opt.clerk.mom": ["mom", "The clerk. What is he looking for, exactly?"],
  "edo.tami.opt.clerk.big": ["bigsis", "The man with the paper. What does the paper say?"],
  "edo.tami.opt.clerk.lil": ["lilsis", "Who's the squinty man?"],
  "edo.tami.clerk.1": ["tami", "Tokuzō, the headman's clerk. Writes what he sees, and cannot see past his brush."],
  "edo.tami.clerk.2": ["tami", "He wants to write 'nothing seen' and go home. Give him nothing. Be travellers."],
  "edo.tami.clerk.lil": ["tami", "Squinty is the word. He once asked my hen her name. Twice."],
  "edo.tami.opt.sushi.lil": ["lilsis", "Is the fish man going to make us food? I'm just ASKING."],
  "edo.tami.sushi.lil": ["tami", "He feeds anyone on that step. Sit on it and look hungry. You have the look."],
  "edo.tami.opt.bye.mom": ["mom", "We'll leave you to the baby."],
  "edo.tami.opt.bye.big": ["bigsis", "I will stop asking questions. For now."],
  "edo.tami.opt.bye.lil": ["lilsis", "I'm going to look at the cat."],
  "edo.tami.bye.mom": ["tami", "Nobody leaves me to the baby. The baby leaves me. ...Go on."],
  "edo.tami.bye.big": ["tami", "Ask more. Nobody in this house asks me anything. They only tell me."],
  "edo.tami.bye.lil": ["tami", "The cat will look back. Do not take it to heart. She does that to everyone."],

  // ---------- kiheiTree: Kihei. Sparse. ----------
  "edo.kihei.open": ["kihei", "...Sit."],
  "edo.kihei.opt.price.mom": ["mom", "What do you ask for a fish? I should tell you first that we can't pay."],
  "edo.kihei.price.1": ["kihei", "For a fish. ...Sit."],
  "edo.kihei.price.2": ["mom", "We have no money that's any good here. I'd rather you knew that now."],
  "edo.kihei.price.3": ["kihei", "I know. Sit."],
  "edo.kihei.opt.price.big": ["bigsis", "What does the mackerel cost? I ask for the record. We have nothing."],
  "edo.kihei.price.big": ["kihei", "The record can sit too."],
  "edo.kihei.opt.hungry.lil": ["lilsis", "We haven't eaten since Nevada. That's a LONG way. I don't know how far."],
  "edo.kihei.hungry.lil": ["kihei", "Sit."],
  "edo.kihei.opt.pennies.lil": ["lilsis", "I've got money. Three pennies. They're REAL. Look."],
  "edo.kihei.opt.red.mom": ["mom", "Your red vest. Is it for an occasion?"],
  "edo.kihei.opt.red.big": ["bigsis", "The red, the vest and the hood. I have a theory. I would prefer a fact."],
  "edo.kihei.opt.red.lil": ["lilsis", "Why are you wearing a red hat? Is it your birthday?"],
  "edo.kihei.red": ["kihei", "Ask my wife."],
  "edo.kihei.red.lil": ["kihei", "...Yes. All year. Ask my wife."],
  "edo.kihei.opt.print.big": ["bigsis", "The picture of the mountain. Where did it come from?"],
  "edo.kihei.opt.print.mom": ["mom", "That's a fine picture of the mountain. Was it a gift?"],
  "edo.kihei.print.1": ["kihei", "A pedlar. Everybody in Edo wants the mountain this year. In that new blue."],
  "edo.kihei.print.2": ["kihei", "I see the mountain every morning for nothing. I bought it anyway. The blue."],
  "edo.kihei.opt.west.mom": ["mom", "If we were going west, which way is west, and how far does it go?"],
  "edo.kihei.opt.west.big": ["bigsis", "West. What is west of here, and how does one get there?"],
  "edo.kihei.opt.west.lil": ["lilsis", "The chickens are looking WEST. What's west?"],
  "edo.kihei.west.1": ["kihei", "The road over the pass is the Tōkaidō. Kyoto. Osaka. The Inland Sea past that."],
  "edo.kihei.west.2": ["kihei", "A long way on sandals. Shorter by sea."],
  "edo.kihei.west.3": ["kihei", "My sister's husband's ship is in the bay. Osaka, morning tide. Dried bonito."],
  "edo.kihei.west.4": ["kihei", "He will not take you. ...Ask anyway. Ask the right one."],
  "edo.kihei.west.lil": ["kihei", "Hens here always look west. Wind comes from there. ...They might know. Ask them."],
  "edo.kihei.opt.arigato.lil": ["lilsis", "Arigatō."],
  "edo.kihei.opt.thanks.mom": ["mom", "Thank you. For all of it."],
  "edo.kihei.thanks.mom": ["kihei", "Okage-sama de. ...The girl told you what it means. She tells everybody."],
  "edo.kihei.opt.bye.mom": ["mom", "We'll be out from under your feet."],
  "edo.kihei.opt.bye.big": ["bigsis", "I will let you work."],
  "edo.kihei.opt.bye.lil": ["lilsis", "Bye, fish man. I'll be RIGHT here."],
  "edo.kihei.bye": ["kihei", "...Sit when you are back."],
  "edo.kihei.bye.lil": ["kihei", "I know."],

  // ---------- sankichiTree: Sankichi, nine, beside the board. He asks questions in Little Sister's own rhythm. ----------
  "edo.sankichi.open.lil": ["sankichi", "Are those your feet? The yellow. Are they feet or are they boots?"],
  "edo.sankichi.open.lil.2": ["lilsis", "They're BOOTS. My feet are inside. Are you the one who can read?"],
  "edo.sankichi.open.lil.3": ["sankichi", "I can read all of it. Can YOU read?"],
  "edo.sankichi.open.lil.4": ["lilsis", "Some. The three-letter ones. HEN. Not here, though. Here it's all squiggles."],
  "edo.sankichi.open.big": ["sankichi", "You are staring at the board. Can you read?"],
  "edo.sankichi.open.big.2": ["bigsis", "...I used to be able to read."],
  "edo.sankichi.open.mom": ["sankichi", "You are so tall. Taller than the headman. Is everyone tall where you come from?"],
  "edo.sankichi.open.mom.2": ["mom", "Not everybody, dear. But it does help my children find me in a crowd."],
  // the board: he reads the Kirishitan board aloud, once, because somebody asked (edo.boardRead); it is answered once
  "edo.sankichi.opt.board.lil": ["lilsis", "What does the sign say? The big one. Read it. Please."],
  "edo.sankichi.opt.board.big": ["bigsis", "Would you read me the board on the left? Any of it. All of it."],
  "edo.sankichi.opt.board.mom": ["mom", "What do the notices say? We're strangers, and we'd like to know the rules."],
  "edo.village.board.read.1": ["sankichi", "That one is the oldest. Older than Grandfather. It says 'Ordinance' at the top."],
  "edo.village.board.read.2": ["sankichi", "The Kirishitan sect is forbidden, as always. Tell on one and you get silver."],
  "edo.village.board.read.3": ["sankichi", "Five hundred pieces for a padre. A hundred for anyone who prays to their god."],
  "edo.village.board.read.4": ["sankichi", "Teacher says nobody has seen a padre in nearly two hundred years."],
  "edo.village.board.read.4b": ["sankichi", "The silver is still up there, though."],
  "edo.village.board.read.5": ["mom", "Then we pray quietly here."],
  "edo.village.board.read.6": ["lilsis", "That's MEAN."],
  "edo.village.board.read.7": ["mom", "It is."],
  "edo.village.board.read.again": ["sankichi", "I read you that one. The others are about poison and horses. Horses cost more."],
  // the year: a true answer that does not help (and the era for the card)
  "edo.sankichi.opt.year.big": ["bigsis", "What year is it? Exactly. Take your time."],
  "edo.sankichi.year.1": ["sankichi", "The thirteenth year of Bunsei. Everybody knows that."],
  "edo.sankichi.year.2": ["bigsis", "...I do not know what that is. I am writing it down anyway. Bunsei thirteen."],
  "edo.sankichi.year.3": ["sankichi", "You said you could not write."],
  "edo.sankichi.year.4": ["bigsis", "In my HEAD. I can still write in my head."],
  // the word: arigatō, for Little Sister (edo.arigato)
  "edo.sankichi.opt.thanks.lil": ["lilsis", "How do you say thank you? Here. I need it. I'm going to need it a LOT."],
  "edo.sankichi.thanks.1": ["sankichi", "You do not know thank you? What do you say when somebody gives you a fish?"],
  "edo.sankichi.thanks.2": ["sankichi", "Arigatō. It means thank you. Say it to Grandfather and watch his face."],
  "edo.sankichi.thanks.3": ["lilsis", "Arigatō. Arigatō. ...I've got it. It's MINE now."],
  "edo.sankichi.thanks.again": ["sankichi", "You have said it nine times. It still means thank you."],
  // questions back: his, in her rhythm, and hers
  "edo.sankichi.opt.questions.lil": ["lilsis", "My turn. One: got chickens? Two: can I see them? Three: what's your name?"],
  "edo.sankichi.questions.1": ["sankichi", "Five, by the fence. Yes. Sankichi."],      // SCENES-20A: "Six": the yard has five
  "edo.sankichi.questions.1b": ["sankichi", "My turn. One: what is a Nevada? Two: is it far? Three: why?"],
  "edo.sankichi.questions.2": ["lilsis", "A place. Yes. Because Daddy took a shortcut. ...You ask questions RIGHT."],
  "edo.sankichi.questions.3": ["sankichi", "You answer them right. Nobody answers mine. They say 'later'."],
  "edo.sankichi.opt.school.big": ["bigsis", "Where did you learn to read?"],
  "edo.sankichi.school.1": ["sankichi", "The temple school. Teacher hits the desk, not us. Mostly the desk."],
  "edo.sankichi.school.2": ["bigsis", "I would give a great deal for one morning at that desk."],
  "edo.sankichi.opt.boots.lil": ["lilsis", "Why does everybody look at my boots?"],
  "edo.sankichi.boots": ["sankichi", "Because they are yellow, and nobody's feet are yellow. ...May I touch one?"],
  "edo.sankichi.boots.2": ["lilsis", "One touch. The LEFT one. The right one's shy."],
  "edo.sankichi.opt.mom.mom": ["mom", "Is your grandfather the fishmonger? In the red?"],
  "edo.sankichi.mom": ["sankichi", "Grandmother made the hood. He says it itches. It does not. He only says it."],
  "edo.sankichi.opt.bye.lil": ["lilsis", "I have to go. Mommy's doing the signal."],
  "edo.sankichi.opt.bye.big": ["bigsis", "Thank you. You have been more use than the entire board."],
  "edo.sankichi.opt.bye.mom": ["mom", "Thank you, dear. Go and tell your grandmother we're coming in."],
  "edo.sankichi.bye.lil": ["sankichi", "What is the signal? ...Is it the eyebrows? My grandmother does the eyebrows."],
  "edo.sankichi.bye.big": ["sankichi", "The board cannot talk. I can. That is the whole difference."],
  "edo.sankichi.bye.mom": ["sankichi", "She knows. She knew before you did. She always does."],
  // things shown to him: the car key (he asks; Mom will not lie), the coin
  "edo.sankichi.key.1": ["sankichi", "What is it?"],
  "edo.sankichi.key.2": ["mom", "A key."],
  "edo.sankichi.key.3": ["sankichi", "To what?"],
  "edo.sankichi.key.4": ["mom", "To a cart that goes without a horse. It's at home. A long way east."],
  "edo.sankichi.key.5": ["sankichi", "...I am going to tell Teacher. He is going to hit the desk."],
  "edo.sankichi.coin.1": ["sankichi", "Whose face is that? It is not the lord. The lord has more chin."],
  "edo.sankichi.coin.2": ["bigsis", "A Roman's. He has been dead a very long time. ...Longer than that."],

  // ---------- tokuzoTree: Tokuzō, the headman's clerk. He peers. Nobody lies. ----------
  // before the kimonos: O-Tami's hand on Mom's sleeve, and the talk does not happen
  "edo.tokuzo.notyet": ["tami", "Not like that, dear. Not in that."],
  "edo.tokuzo.notyet.2": ["mom", "...No. Quite right. Not in this."],
  // dressed: he peers
  "edo.tokuzo.open.1": ["tokuzo", "Good morning. Forgive me. ...Forgive me. Travellers?"],
  "edo.tokuzo.opt.travellers.mom": ["mom", "We are. We're going west."],
  "edo.tokuzo.opt.travellers.big": ["bigsis", "Travellers. Yes. We have travelled a great deal since yesterday."],
  "edo.tokuzo.opt.travellers.lil": ["lilsis", "We're going on a BOAT. Probably. If the boat man says."],
  "edo.tokuzo.travellers.lil": ["tokuzo", "A boat. Going west. ...Children say the truest things. I will write 'west'."],
  "edo.tokuzo.from": ["tokuzo", "West. Good. ...From where, if I may?"],
  "edo.tokuzo.opt.from.big": ["bigsis", "From the east."],
  "edo.tokuzo.opt.from.mom": ["mom", "From a long way past Edo."],
  "edo.tokuzo.opt.from.lil": ["lilsis", "From our HOUSE."],
  "edo.tokuzo.from.big": ["tokuzo", "The east. ...Yes. Most people are. I will write 'the east'."],
  "edo.tokuzo.from.big.mom": ["mom", "..."],
  "edo.tokuzo.from.big.2": ["bigsis", "It is true, Mother. Every word of it."],
  "edo.tokuzo.from.mom": ["tokuzo", "Past Edo. Then you have come further than I ever have. I have been to Okitsu."],
  "edo.tokuzo.from.lil": ["tokuzo", "From your house. ...Everybody is, when you think about it. I will write 'house'."],
  "edo.tokuzo.tall": ["tokuzo", "You are very tall."],
  "edo.tokuzo.opt.tall.mom": ["mom", "I am."],
  "edo.tokuzo.opt.tall.big": ["bigsis", "She is. It runs in the family, up to a point. The point is me."],
  "edo.tokuzo.opt.tall.lil": ["lilsis", "She's the TALLEST. I'm the smallest. We average out."],
  "edo.tokuzo.tall.ans": ["tokuzo", "...So you are. Well. One cannot write 'tall'. There is no box for it."],
  // he writes it down, and goes home, pleased
  "edo.tokuzo.write.1": ["tokuzo", "'Travellers. Three. Going west.' Nothing seen. ...Good."],
  "edo.tokuzo.write.2": ["tokuzo", "Forgive me. A pleasant road to you. Mind the pass; it is steep."],
  "edo.tokuzo.write.3": ["tokuzo", "I am told the view from the top is wasted on the short-sighted."],
  // met again, after (if the scene keeps him on his rounds)
  "edo.tokuzo.after": ["tokuzo", "The travellers. Still west? ...Good. It is written. I shall not write it twice."],
  "edo.tokuzo.after.opt.mom": ["mom", "Still west."],
  "edo.tokuzo.after.mom": ["tokuzo", "Then nothing has changed, and nothing is my favorite thing to write."],
  "edo.tokuzo.after.opt.lil": ["lilsis", "Do you need glasses? We have them where I come from. ROUND ones."],
  "edo.tokuzo.after.lil": ["tokuzo", "Glasses. I have heard of them. They sound expensive. Squinting costs nothing."],

  // ---------- gonrokuTree: Gonroku, the captain. No women aboard. Every argument fails, and he speaks in weather. ----------
  "edo.gonroku.open": ["gonroku", "The wind is coming round. Rain behind it, two days off. ...You want something."],
  "edo.gonroku.opt.passage.mom": ["mom", "We'd like passage west, to Osaka. We can't pay. I'd still like to ask."],
  "edo.gonroku.no.1": ["gonroku", "Asked. No."],
  "edo.gonroku.no.2": ["gonroku", "The Funadama is the ship's own lady. She does not care for other women aboard."],
  "edo.gonroku.no.3": ["gonroku", "Sealed in the mast: dice, two dolls, coins, a woman's hair. She is particular."],
  "edo.gonroku.opt.hair.big": ["bigsis", "A woman's hair is in the mast. So a woman is aboard already. Technically."],
  "edo.gonroku.hair": ["gonroku", "Technically, she is the one who would mind. ...Clouds over the pass. No."],
  "edo.gonroku.opt.luck.lil": ["lilsis", "We aren't bad luck. We're GOOD luck. The hens like us. Hens can tell."],
  "edo.gonroku.luck": ["gonroku", "Hens do not sail. ...The wind is freshening. No."],
  "edo.gonroku.opt.quiet.mom": ["mom", "We'd sit very still, and say nothing, for twelve days. I have practice."],
  "edo.gonroku.quiet": ["gonroku", "Twelve days of still women is twelve days waiting for the other thing. No."],
  "edo.gonroku.opt.men.big": ["bigsis", "Is it a rule, or a feeling? I ask because feelings have exceptions."],
  "edo.gonroku.men": ["gonroku", "It is weather. You do not argue. You wait for it to change. ...It will not."],
  "edo.gonroku.opt.stern.lil": ["lilsis", "We'll sit in the very back, on the FLOOR. We won't touch the lady's mast."],
  "edo.gonroku.stern": ["gonroku", "In the stern. ...The stern is hers as well. The swell is getting up. No."],
  "edo.gonroku.opt.where.mom": ["mom", "Where do you sail, and when?"],
  "edo.gonroku.where": ["gonroku", "Osaka. First light. Bonito. Twelve days, if the wind is kind. It will not be."],
  "edo.gonroku.opt.wife.mom": ["mom", "And what does the Funadama like?"],
  "edo.gonroku.wife": ["gonroku", "Ask my wife. She knows what everybody likes. At the nets. Mind how you ask."],
  "edo.gonroku.opt.bye.mom": ["mom", "Then we'll leave you to your weather."],
  "edo.gonroku.opt.bye.big": ["bigsis", "I will come back with a better argument."],
  "edo.gonroku.opt.bye.lil": ["lilsis", "I'm going to ask the CHICKENS about you."],
  "edo.gonroku.bye.mom": ["gonroku", "Weather does not need leaving to. It comes anyway."],
  "edo.gonroku.bye.big": ["gonroku", "Bring one for the wind while you are at it."],
  "edo.gonroku.bye.lil": ["gonroku", "...Tell them the wind is westerly. They will know what it means."],
  // after O-Masa has spoken (edo.west): the terms
  "edo.gonroku.after.1": ["gonroku", "Stern. No whistling. First light. Three things. I have said them."],
  "edo.gonroku.after.opt.mom": ["mom", "We'll be there before the light is."],
  "edo.gonroku.after.mom": ["gonroku", "Everybody says that. The tide believes nobody."],
  "edo.gonroku.after.opt.lil": ["lilsis", "I promise not to whistle. I CAN'T whistle. Watch. ...See?"],
  "edo.gonroku.after.lil": ["gonroku", "...Keep not doing that. The wind is fair. Do not spoil it."],

  // ---------- masaTree: O-Masa, Kihei's sister, Gonroku's wife, at the net racks. Verdicts. Asked properly. ----------
  "edo.masa.open": ["masa", "You have been to my husband. I saw his shoulders. ...Well?"],
  "edo.masa.opt.favour.mom": ["mom", "Would you ask your husband to take us? He listens to you."],
  "edo.masa.favour": ["masa", "That is a favour. Favours I give my brother. Questions I will take from anybody."],
  "edo.masa.opt.unfair.big": ["bigsis", "Your husband's position is unreasonable. I say that with respect."],
  "edo.masa.unfair": ["masa", "He is a sailor. Reason is for the land. ...You are right, though."],
  "edo.masa.opt.boss.lil": ["lilsis", "Can you MAKE him take us? You're the boss of him. I can tell."],
  "edo.masa.boss": ["masa", "Nobody is the boss of a sailor. ...His wife is. Sit down; you are in my light."],
  "edo.masa.opt.nets.lil": ["lilsis", "What are you doing to the net? It's got HOLES."],
  "edo.masa.nets": ["masa", "A thousand holes with string round them, and it holds fish. Think about that."],
  "edo.masa.nets.2": ["lilsis", "...I'm thinking about it. It's a LOT."],
  "edo.masa.opt.brother.mom": ["mom", "Your brother fed us this morning and would take nothing. You should know."],
  "edo.masa.brother": ["masa", "My brother feeds folk. My husband ships fish. I married the wrong one for lunch."],
  "edo.masa.opt.lady.big": ["bigsis", "The Funadama. Is she real?"],
  "edo.masa.lady": ["masa", "She is real to him. That is what you would be sailing on. Not the sea. Him."],
  // before #22 and #23: she looks at them, and her verdict is not yet
  "edo.masa.opt.ask.mom": ["mom", "May I ask your advice? Not a favour. A question, properly."],
  "edo.masa.notdressed": ["masa", "Not in that. Nobody asks me anything properly in that. Ask my brother's wife."],
  "edo.masa.notfed": ["masa", "You have not eaten. I can hear it from here. My brother's step first. Then ask."],
  "edo.masa.notclerk": ["masa", "Half the village saw you come in. The clerk has not seen you go out. Him first."],
  // the lever: the question, properly asked; she looks at the three of them, their manners and their borrowed clothes
  "edo.masa.ask.1": ["masa", "Ask it."],
  "edo.masa.ask.2": ["mom", "What would the Funadama make of three women who sit still and have manners?"],
  "edo.masa.ask.3": ["masa", "..."],
  "edo.masa.ask.4": ["masa", "That is a question. ...Stay here, all three of you. Do not follow me."],
  // (she goes down the beach: masaTree's hook `toGonroku`, then edo.west.masa.1 and edo.west.gonroku.*)
  "edo.masa.opt.bye.mom": ["mom", "We'll let you mend."],
  "edo.masa.opt.bye.big": ["bigsis", "Thank you. I think."],
  "edo.masa.opt.bye.lil": ["lilsis", "Bye, net boss."],
  "edo.masa.bye.mom": ["masa", "Mending does not need letting. Go on."],
  "edo.masa.bye.big": ["masa", "You think a great deal. Try asking. It is quicker."],
  "edo.masa.bye.lil": ["masa", "...Net boss. I will keep that."],
  // after (edo.west): her last word
  "edo.masa.after": ["masa", "He said stern, and no whistling. He means the whistling. The rest is weather."],

  // ======================================================================================================
  // HINTS: hint.edo.<puzzle>.<who>. The one whose job it is says what to try; the others say whose job it is.
  // Staged where a puzzle is long (ids.md says which stage is which).
  // ======================================================================================================
  // #21 Where, And When (Big Sister's): staged by which clues are in (edo.clue.red, .coins, .blue)
  "hint.edo.when.bigsis": ["bigsis", "No sign will tell me the year. Things will: the red, the coins, that blue."],
  "hint.edo.when.bigsis.2": ["bigsis", "The fishmonger wears red for a reason, and his wife will know it. Ask her why."],
  "hint.edo.when.bigsis.3": ["bigsis", "His money box is right there. Coins carry their era with them. Look at those."],
  "hint.edo.when.bigsis.4": ["bigsis", "The print of the mountain is a very particular blue. He bought it. Ask him why."],
  "hint.edo.when.bigsis.5": ["bigsis", "Red, coins, blue. I have all three clues now. I can do this sum standing up."],
  "hint.edo.when.mom": ["mom", "The year is your sister's department, girls. Coins and colors are her books."],
  "hint.edo.when.lilsis": ["lilsis", "My sister does the when. I do the chickens. We have a SYSTEM."],
  // #22 Out Of Sight (Mom's): staged: before the first pass, before the baby, before the clothes, before the clerk
  "hint.edo.dressed.mom": ["mom", "Three women in our own clothes on a main street. We must be less interesting."],
  "hint.edo.dressed.mom.2": ["mom", "The baby won't sleep, and nothing happens till she does. I've had three. Let me."],
  "hint.edo.dressed.mom.3": ["mom", "The baby's asleep, and O-Tami said she'd dress us. Her clothes chest, I think."],
  "hint.edo.dressed.mom.4": ["mom", "Dressed, and not a moment too soon. Now the clerk, and only true answers."],
  "hint.edo.dressed.bigsis": ["bigsis", "The clothes are Mom's job. Nobody says no to Mom with a baby in her arms."],
  "hint.edo.dressed.lilsis": ["lilsis", "Mommy's doing the grown-ups. I'm keeping my BOOTS."],
  // #23 Kihei's Table (any): staged: before anyone has asked; the pennies tried; the meal done
  "hint.edo.fed.mom": ["mom", "We haven't eaten since Nevada. I'll ask the fishmonger his price, and be honest."],
  "hint.edo.fed.mom.2": ["mom", "He keeps saying 'Sit'. Darling, I think that's the price."],
  "hint.edo.fed.bigsis": ["bigsis", "Mom asks prices. I state facts. The fact is that I am hungry."],
  "hint.edo.fed.bigsis.2": ["bigsis", "He has said 'Sit' five times. In most languages, that is an invitation."],
  "hint.edo.fed.lilsis": ["lilsis", "I'll ask the fish man. Or sit on the step and LOOK hungry. I'm good at it."],
  "hint.edo.fed.lilsis.2": ["lilsis", "I offered my pennies. He gave them BACK. I think we're supposed to just sit."],
  // #24 West (Little Sister, then Mom): staged: the hens not seen; Gonroku not asked; Gonroku refused; O-Masa to ask
  "hint.edo.west.lilsis": ["lilsis", "The door's gone. When a door's gone, you ask the CHICKENS. They're by the fence."],
  "hint.edo.west.lilsis.2": ["lilsis", "The chickens say west. The fish man knows the roads. And he knows the boat man."],
  "hint.edo.west.lilsis.3": ["lilsis", "The boat man said no to EVERYTHING. Even the chickens. Mommy's turn."],
  "hint.edo.west.mom": ["mom", "Your sister's hens are pointing west. I'll ask the fishmonger about the roads."],
  "hint.edo.west.mom.2": ["mom", "The captain said to ask his wife, at the nets. A question, then, not a favour."],
  "hint.edo.west.mom.3": ["mom", "The ship's ours at first light. Goodbyes, girls. All of them, hens included."],
  "hint.edo.west.bigsis": ["bigsis", "The captain cannot be argued with. I tried. Mom asks the right person instead."],
  "hint.edo.west.bigsis.2": ["bigsis", "Everyone on that beach defers to the woman at the nets. So should we."],

  // ======================================================================================================
  // THE THINGS CARRIED (world.js items: sushibox, mirror, trowel), looked at by each of the three
  // ======================================================================================================
  "item.sushibox.mom": ["mom", "His sushi, wrapped for the road by a woman holding a baby. We'll make it last."],
  "item.sushibox.bigsis": ["bigsis", "Pressed mackerel sushi. The old way. Edo's new hand-made kind can wait."],
  "item.sushibox.lilsis": ["lilsis", "The fish box! I'm carrying it. I'm not eating it. ...I had ONE."],
  "item.mirror.mom": ["mom", "Her mirror. Pine and crane on the back. To be held up in the light, she said."],
  "item.mirror.bigsis": ["bigsis", "Bronze, slightly convex. The picture on its back shows in the light it throws."],
  "item.mirror.lilsis": ["lilsis", "The grandma's mirror. Heavy. There's a bird on the back. I'm being SO careful."],
  "item.trowel.mom": ["mom", "A trowel, for a cousin at Himeji. 'Say Jinsuke is well.' That's all we need say."],
  "item.trowel.bigsis": ["bigsis", "A trowel, worn bright, its handle shaped by one hand. It goes back to that hand."],
  "item.trowel.lilsis": ["lilsis", "A flat spoon for walls. For the cousin. I can't dig with it. I ASKED."],

  // ======================================================================================================
  // THE ACT'S STOCK REPLIES for the three (story.fallbacks, story.give, in Japan), and what the people of Yui say when
  // handed a thing they do not want (the scenes' useWith for the rest)
  // ======================================================================================================
  "edo.nope.mom.1": ["mom", "No, darling. Not in someone else's country."],
  "edo.nope.mom.2": ["mom", "I think not. We're guests, and guests don't."],
  "edo.nope.mom.3": ["mom", "A thought. We'll keep it as one."],
  "edo.nope.bigsis.1": ["bigsis", "That will not work. I would footnote why, but I cannot read the footnotes here."],
  "edo.nope.bigsis.2": ["bigsis", "No. Not in 1830, and not in any year I have tried."],
  "edo.nope.bigsis.3": ["bigsis", "'It did not,' she noted, 'work. Nothing here does, for me.'"],
  "edo.nope.lilsis.1": ["lilsis", "NO. It doesn't go. Not even in Japan."],
  "edo.nope.lilsis.2": ["lilsis", "Nope. I tried it the Japan way too."],
  "edo.nope.lilsis.3": ["lilsis", "That's silly. Arigatō for the idea, though."],
  "edo.look.mom.1": ["mom", "Nothing that needs us. Which, this morning, is a kindness."],
  "edo.look.bigsis.1": ["bigsis", "Unremarkable, and I cannot read it. Two for two."],
  "edo.look.lilsis.1": ["lilsis", "It's a thing. A Japan thing. Still boring. NEXT."],
  "edo.hint.none.mom": ["mom", "I haven't the faintest idea, my love. We'll look round, politely."],
  "edo.hint.none.bigsis": ["bigsis", "I do not know. I cannot even read my way to not knowing. Let us look round."],
  "edo.hint.none.lilsis": ["lilsis", "I dunno. Ask somebody tall. Mommy's the tallest one HERE."],
  "edo.give.mom.1": ["mom", "Would you take this, darling? Quietly."],
  "edo.give.bigsis.1": ["bigsis", "Here. It is yours now. Do not lose it in a sleeve."],
  "edo.give.lilsis.1": ["lilsis", "Hold this. It's IMPORTANT. Arigatō."],
  // the people of Yui, handed a thing they do not want
  "edo.give.no.kihei": ["kihei", "...No. Sit."],
  "edo.give.no.tami": ["tami", "I have a baby in one hand and a shop in the other. Where would I put it?"],
  "edo.give.no.sankichi": ["sankichi", "What is it? What does it do? Can I keep it? ...No? Then why show me?"],
  "edo.give.no.tokuzo": ["tokuzo", "Forgive me. I cannot take anything I cannot see. ...And I cannot see that."],
  "edo.give.no.gonroku": ["gonroku", "Not aboard. Nothing comes aboard she has not met. ...The wind is backing. No."],
  "edo.give.no.masa": ["masa", "Put it away. I have nets to mend, and you have asking to do."],
  // the egg, shown to Kihei (it is Little Sister's, from Nevada: she will not part with it here)
  "edo.shop.egg.kihei": ["kihei", "An egg. You have an egg and I have fish. Keep your egg."],
  "edo.shop.egg.lilsis": ["lilsis", "I wasn't GIVING it. I was showing. It's a Nevada egg. It's been places."],

  // ======================================================================================================
  // THE THREE OF THEM, to each other (the scene's `talk` for companions, in the first leg)
  // ======================================================================================================
  "edo.talk.mom.bigsis.read.a": ["mom", "You've gone quiet, darling."],
  "edo.talk.mom.bigsis.read.b": ["bigsis", "I cannot read a single thing here, Mother. Not a sign, not a label, not a price."],
  "edo.talk.mom.bigsis.read.c": ["mom", "Then read people. You can start with me. I'm an easy chapter."],
  "edo.talk.bigsis.mom.tall.a": ["bigsis", "Everyone looks at you, Mother. You are a head taller than every woman here."],
  "edo.talk.bigsis.mom.tall.b": ["mom", "I know, darling. I've decided to be tall on purpose. It reads better."],
  "edo.talk.mom.lilsis.boots.a": ["mom", "The boots stay, do they, sweetheart?"],
  "edo.talk.mom.lilsis.boots.b": ["lilsis", "The boots stay. They've been to Nevada. They can do Japan."],
  "edo.talk.lilsis.mom.son.a": ["lilsis", "Mommy, is my brother looking for US now? Since we came the wrong way?"],
  "edo.talk.lilsis.mom.son.b": ["mom", "He's looking for all of us, sweetheart. We'll be easier to find together."],
  "edo.talk.lilsis.bigsis.word.a": ["lilsis", "I know a Japan word now. Arigatō. How many do YOU know?"],
  "edo.talk.lilsis.bigsis.word.b": ["bigsis", "About forty. All of them are food. Not one of them is thank you."],
  "edo.talk.lilsis.bigsis.word.c": ["lilsis", "Then mine's the best one. Arigatō."],
  "edo.talk.bigsis.lilsis.hens.a": ["bigsis", "The hens here, too. All facing one way. I am not going to say they know."],
  "edo.talk.bigsis.lilsis.hens.b": ["lilsis", "You don't HAVE to say it. They know you know."],
  "edo.talk.mom.bigsis.lie.a": ["mom", "Darling, when the man asks, we tell him the truth. All we can, and nothing else."],
  "edo.talk.mom.bigsis.lie.b": ["bigsis", "'From the east' is the truth, Mother. It's just a very small piece of it."],
  "edo.talk.mom.bigsis.lie.c": ["mom", "A small true piece is still true. A large false one isn't. Keep them small."],
  "edo.talk.lilsis.mom.grace.a": ["lilsis", "Mommy, they didn't say grace. They bowed at the shelf and didn't say anything."],
  "edo.talk.lilsis.mom.grace.b": ["mom", "That's their thankful, sweetheart. Ours has more words. Yours especially."],

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
  "edo.masa.notroad": ["masa", "Walk up that road first. He will say you could have walked. Then ask me."],
  // ---- TALK-24 (10 November: "way too many dialogue choices in Japan"): the topics a talk's questions are gathered under ----
  "edo.gonroku.topic.case": ["bigsis", "We have more arguments. I have numbered them."],
  "edo.masa.topic.husband": ["mom", "May I ask about your husband, and his boat?"],
  "edo.masa.topic.chat": ["lilsis", "Can I ask about your net? And other things?"],
  "edo.tami.topic.asks.lil": ["lilsis", "I have three questions. They're IMPORTANT."],
};
